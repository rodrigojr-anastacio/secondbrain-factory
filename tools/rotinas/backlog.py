#!/usr/bin/env python
"""Backlog vivo da fábrica (tabela youtube.backlog) + calendário de publicação (14/11/2026, decisão do Rodrigo).

Fonte da verdade: youtube.backlog (DDL tools/db/schema_backlog.sql). O backlog.md de cada canal ganha uma seção
"Backlog vivo" GERADA por este script (entre marcadores); não edite essa seção à mão.

Calendário: 4 vídeos por canal por semana: seg, qua, sex + 1 no fim de semana, alternando sábado numa semana e
domingo na outra (semana de 16/11/2026 = sábado). O dia usado em cada semana fica em youtube.calendario_semanas.

Uso (tools/.venv/bin/python tools/rotinas/backlog.py …):
  listar [--canal X] [--todos]           temas e status
  calendario [--canal X] [--dias 14]     slots de publicação e o que ocupa cada um
  importar <arquivo.json> --canal X [--fonte F]   carga/atualização de temas (upsert por slug; congelados não mudam)
  add --canal X --tema T --slug S [--status ...] [--data AAAA-MM-DD] [--video-id N] [--pasta P] [--nota ...] --motivo M
  nota <id> --demanda D --encaixe E --urgencia U --motivo M      reavalia (recalcula a nota)
  descartar <id> --motivo M              tira da fila (proibido para em_producao/pronto/publicado)
  status <id> <status> --motivo M        muda status à mão (congelados só avançam)
  sync                                   youtube.videos → backlog (pronto/publicado, video_id pela pasta)
  agendar [--canal X]                    vence janelas, ordena pela nota e distribui os temas nos slots livres
  md [--canal X]                         reescreve a seção "Backlog vivo" do backlog.md
  tudo                                   sync + agendar + md (o que as rotinas chamam)
Regra de congelamento: item em_producao, pronto ou publicado nunca é trocado, reavaliado nem descartado.
"""
import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import psycopg
from psycopg.types.json import Jsonb

REPO = Path.home() / "workspace/fabrica-youtube"
DB = os.environ.get("FABRICA_DB", "dbname=vida")
TZ = ZoneInfo("America/Sao_Paulo")
REF_SEMANA = date(2026, 11, 16)   # segunda; nesta semana o fim de semana é SÁBADO, na seguinte DOMINGO, e assim por diante
HORIZONTE_DIAS = 14               # quantos dias à frente o agendar distribui temas
CONGELADOS = ("em_producao", "pronto", "publicado")
OCUPA_SLOT = ("em_producao", "pronto", "publicado")
DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]

# Canais da fábrica noturna (lotr-fr em stand-by, fora). Ordem = prioridade quando falta recurso no pré-voo.
CANAIS = {
    "historia-ptbr": dict(curto="historia", nome="História em minutos", videos="canais/historia-ptbr/videos",
                          md="canais/historia-ptbr/backlog.md", pasta_fmt="{n:03d}-{slug}"),
    "dossie-es": dict(curto="dossie", nome="Dossier en Minutos", videos="canais/dossie-es/videos",
                      md="canais/dossie-es/backlog.md", pasta_fmt="{n:03d}-{slug}"),
    "lugares-guerra-en": dict(curto="clearance", nome="Clearance Required", videos="canais/lugares-guerra-en/videos",
                              md="canais/lugares-guerra-en/backlog.md", pasta_fmt="{n:03d}-{slug}"),
    # Em Relevo não tem pasta canais/ própria: vídeos e regras moram em pesquisa/canal-clima-2026-11/ (longo-NN).
    "em-relevo": dict(curto="relevo", nome="Em Relevo", videos="pesquisa/canal-clima-2026-11",
                      md="canais/em-relevo/backlog.md", pasta_fmt="longo-{n:02d}"),
}
INI, FIM = "<!-- backlog-vivo:inicio (gerado por tools/rotinas/backlog.py; não edite à mão) -->", "<!-- backlog-vivo:fim -->"


def conectar(autocommit=True):
    return psycopg.connect(DB, autocommit=autocommit)


def hoje():
    return datetime.now(TZ).date()


def calc_nota(d, e, u):
    try:
        return round((float(d) * float(e) * float(u)) ** (1 / 3), 1)
    except (TypeError, ValueError):
        return None


# ---------------- calendário ----------------
def segunda(d):
    return d - timedelta(days=d.weekday())


def dia_fds(con, d, registrar=True):
    """'sab' ou 'dom' para a semana de d (registrado em youtube.calendario_semanas na 1ª consulta)."""
    s = segunda(d)
    r = con.execute("SELECT dia_fds FROM youtube.calendario_semanas WHERE semana_ini=%s", (s,)).fetchone()
    if r:
        return r[0]
    v = "sab" if ((s - REF_SEMANA).days // 7) % 2 == 0 else "dom"
    if registrar:
        con.execute("INSERT INTO youtube.calendario_semanas (semana_ini, dia_fds, obs) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
                    (s, v, "alternância automática (ref.: semana de 16/11/2026 = sábado)"))
    return v


def eh_slot(con, d):
    wd = d.weekday()
    if wd in (0, 2, 4):
        return True
    if wd == 5:
        return dia_fds(con, d) == "sab"
    if wd == 6:
        return dia_fds(con, d) == "dom"
    return False


def slots(con, ini, fim):
    d, out = ini, []
    while d <= fim:
        if eh_slot(con, d):
            out.append(d)
        d += timedelta(days=1)
    return out


def fmt_d(d):
    return f"{DIAS[d.weekday()]} {d:%d/%m}" if d else "-"


# ---------------- leitura/escrita ----------------
COLS = ("id,canal_slug,tema,slug,angulo,titulo_candidato,evidencias,demanda,encaixe,urgencia,nota,janela_ate,riscos,"
        "status,data_prevista,video_id,pasta,fonte,motivo,mudou_em")


def itens(con, where="true", args=()):
    cur = con.execute(f"SELECT {COLS} FROM youtube.backlog WHERE {where} ORDER BY canal_slug, nota DESC NULLS LAST, id", args)
    names = [d.name for d in cur.description]
    return [dict(zip(names, r)) for r in cur.fetchall()]


def mudar(con, item_id, motivo, **campos):
    """Atualiza campos + status, registra motivo, data e histórico."""
    atual = con.execute("SELECT status, data_prevista FROM youtube.backlog WHERE id=%s", (item_id,)).fetchone()
    if not atual:
        raise SystemExit(f"backlog id {item_id} não existe")
    hist = {"em": datetime.now(TZ).isoformat(timespec="minutes"), "de": atual[0], "para": campos.get("status", atual[0]),
            "motivo": motivo}
    if "data_prevista" in campos and campos["data_prevista"] != atual[1]:
        hist["data"] = str(campos["data_prevista"]) if campos["data_prevista"] else None
    sets = ", ".join(f"{k}=%s" for k in campos)
    vals = [Jsonb(v) if isinstance(v, (list, dict)) else v for v in campos.values()]
    con.execute(f"UPDATE youtube.backlog SET {sets}{', ' if sets else ''}motivo=%s, mudou_em=now(), "
                "historico = historico || %s::jsonb WHERE id=%s", (*vals, motivo, json.dumps([hist]), item_id))


def proximo_numero(con, canal):
    """Maior número já usado (banco, pastas e backlog) + 1."""
    cfg = CANAIS[canal]
    n = con.execute("SELECT COALESCE(max(numero),0) FROM youtube.videos WHERE canal_slug=%s", (canal,)).fetchone()[0]
    rx = re.compile(r"^longo-(\d+)" if cfg["pasta_fmt"].startswith("longo") else r"^(\d{3})-")
    base = REPO / cfg["videos"]
    if base.is_dir():
        for p in base.iterdir():
            m = rx.match(p.name)
            if m and p.is_dir():
                n = max(n, int(m.group(1)))
    for (pasta,) in con.execute("SELECT pasta FROM youtube.backlog WHERE canal_slug=%s AND pasta IS NOT NULL", (canal,)).fetchall():
        m = rx.match(Path(pasta).name)
        if m:
            n = max(n, int(m.group(1)))
    return n + 1


# ---------------- operações ----------------
def importar(con, arquivo, canal, fonte=None):
    dados = json.loads(Path(arquivo).read_text())
    fonte = fonte or str(Path(arquivo).resolve().relative_to(REPO)) if str(Path(arquivo).resolve()).startswith(str(REPO)) else (fonte or arquivo)
    n_ins = n_upd = n_cong = 0
    for t in dados:
        nota = t.get("nota") or calc_nota(t.get("demanda"), t.get("encaixe"), t.get("urgencia"))
        ex = con.execute("SELECT id, status FROM youtube.backlog WHERE canal_slug=%s AND slug=%s", (canal, t["slug"])).fetchone()
        campos = dict(tema=t["tema"], angulo=t.get("angulo"), titulo_candidato=t.get("titulo_candidato"),
                      evidencias=t.get("evidencias") or [], demanda=t.get("demanda"), encaixe=t.get("encaixe"),
                      urgencia=t.get("urgencia"), nota=nota, janela_ate=t.get("janela_ate") or None, riscos=t.get("riscos"), fonte=fonte)
        if ex and ex[1] in CONGELADOS:
            n_cong += 1
            continue
        if ex:
            if ex[1] == "descartado":
                campos["status"] = "proposto"
            mudar(con, ex[0], f"atualizado pela pesquisa ({fonte})", **campos)
            n_upd += 1
        else:
            con.execute("INSERT INTO youtube.backlog (canal_slug,tema,slug,angulo,titulo_candidato,evidencias,demanda,encaixe,urgencia,nota,"
                        "janela_ate,riscos,fonte,motivo,historico) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (canal, t["tema"], t["slug"], campos["angulo"], campos["titulo_candidato"], Jsonb(campos["evidencias"]),
                         campos["demanda"], campos["encaixe"], campos["urgencia"], nota, campos["janela_ate"], campos["riscos"], fonte,
                         f"entrou pela pesquisa ({fonte})",
                         Jsonb([{"em": datetime.now(TZ).isoformat(timespec="minutes"), "para": "proposto", "motivo": f"pesquisa {fonte}"}])))
            n_ins += 1
    print(f"{canal}: {n_ins} novos, {n_upd} atualizados, {n_cong} congelados (não mexidos)")


def sync(con):
    """youtube.videos → backlog: liga video_id pela pasta e avança pronto/publicado."""
    n = 0
    for it in itens(con, "pasta IS NOT NULL AND video_id IS NULL"):
        r = con.execute("SELECT id FROM youtube.videos WHERE canal_slug=%s AND pasta=%s ORDER BY id DESC LIMIT 1", (it["canal_slug"], it["pasta"])).fetchone()
        if r:
            mudar(con, it["id"], "vídeo criado em youtube.videos (sync pela pasta)", video_id=r[0])
            n += 1
    for it in itens(con, "video_id IS NOT NULL AND status IN ('em_producao','pronto','agendado')"):
        st, pub = con.execute("SELECT status, publicado_em FROM youtube.videos WHERE id=%s", (it["video_id"],)).fetchone()
        if st == "publicado" and it["status"] != "publicado":
            mudar(con, it["id"], "publicado (youtube.videos)", status="publicado", data_prevista=pub or it["data_prevista"])
            n += 1
        elif st == "pronto" and it["status"] in ("em_producao", "agendado"):
            mudar(con, it["id"], "vídeo pronto (youtube.videos)", status="pronto")
            n += 1
    return n


def agendar(con, canal=None, ref=None):
    """Vence janelas, ordena pela nota e distribui proposto/agendado nos slots livres dos próximos HORIZONTE_DIAS."""
    ref = ref or hoje()
    canais = [canal] if canal else list(CANAIS)
    amanha = ref + timedelta(days=1)
    for c in canais:
        for it in itens(con, "canal_slug=%s AND status IN ('proposto','agendado') AND janela_ate IS NOT NULL AND janela_ate < %s", (c, amanha)):
            mudar(con, it["id"], f"perdeu a janela (janela_ate {it['janela_ate']:%d/%m})", status="descartado", data_prevista=None)
        ocupados = {r[0] for r in con.execute("SELECT data_prevista FROM youtube.backlog WHERE canal_slug=%s AND status IN ('em_producao','pronto','publicado') "
                                              "AND data_prevista >= %s", (c, amanha)).fetchall()}
        livres = [d for d in slots(con, amanha, ref + timedelta(days=HORIZONTE_DIAS)) if d not in ocupados]
        resto = itens(con, "canal_slug=%s AND status IN ('proposto','agendado')", (c,))   # já em ordem de nota
        fila = []
        for k, d in enumerate(livres):   # pela nota, mas o tema cuja janela fecha antes do próximo slot fura a fila
            if not resto:
                break
            prox = livres[k + 1] if k + 1 < len(livres) else None
            urg = [it for it in resto if it["janela_ate"] and prox and it["janela_ate"] < prox and it["janela_ate"] >= d]
            esc = urg[0] if urg else resto[0]
            resto.remove(esc)
            fila.append(esc)
        fila += resto
        for i, it in enumerate(fila):
            d = livres[i] if i < len(livres) else None
            st = "agendado" if d else "proposto"
            if it["data_prevista"] != d or it["status"] != st:
                mudar(con, it["id"], f"agendar: ordem pela nota ({it['nota']})" if d else "agendar: sem slot nos próximos 14 dias",
                      status=st, data_prevista=d)


def evid_principal(it):
    ev = it["evidencias"] or []
    if not ev:
        return "-"
    e = ev[0]
    txt = f"{e.get('fonte', '')}: {e.get('numero', '')}".strip(": ")
    return f"[{txt}]({e['link']})" if e.get("link", "").startswith("http") else txt


def gerar_md(con, canal):
    cfg = CANAIS[canal]
    ref = hoje()
    L = [INI, "", f"## Backlog vivo ({datetime.now(TZ):%d/%m/%Y %H:%M})", "",
         "Fonte da verdade: tabela `youtube.backlog` (DDL `tools/db/schema_backlog.sql`); esta seção é espelho, gerada por "
         "`tools/rotinas/backlog.py md`. Reordenação seg/qui depois do garimpo (rotina `backlog`); a produção noturna "
         "(`tools/rotinas/noturna.py`) pega o 1º item agendado na véspera de cada publicação. "
         "Nota = (demanda × encaixe × urgência)^(1/3). Item em produção ou além é congelado.", "",
         "### Calendário (próximos 14 dias)", "", "| data | tema | status |", "|---|---|---|"]
    por_data = {}
    for it in itens(con, "canal_slug=%s AND data_prevista IS NOT NULL AND status <> 'descartado'", (canal,)):
        por_data.setdefault(it["data_prevista"], []).append(it)
    for d in slots(con, ref, ref + timedelta(days=HORIZONTE_DIAS)):
        its = por_data.get(d, [])
        if its:
            for it in its:
                L.append(f"| {fmt_d(d)} | {it['tema']} | {it['status']} |")
        else:
            L.append(f"| {fmt_d(d)} | — (vaga) | |")
    L += ["", "### Temas (ordem da fila)", "", "| id | tema | nota (D·E·U) | status | publicação | janela | evidência principal |", "|---|---|---|---|---|---|---|"]
    ordem = {"em_producao": 0, "agendado": 1, "proposto": 2}
    ativos = sorted(itens(con, "canal_slug=%s AND status IN ('em_producao','agendado','proposto')", (canal,)),
                    key=lambda i: (ordem[i["status"]], i["data_prevista"] or date(2100, 1, 1), -(float(i["nota"] or 0))))
    for it in ativos:
        dd = f"{float(it['demanda'] or 0):g}·{float(it['encaixe'] or 0):g}·{float(it['urgencia'] or 0):g}" if it["demanda"] is not None else "-"
        L.append(f"| {it['id']} | {it['tema']} | {it['nota'] if it['nota'] is not None else '-'} ({dd}) | {it['status']} | {fmt_d(it['data_prevista'])} | "
                 f"{it['janela_ate'].strftime('%d/%m') if it['janela_ate'] else 'perene'} | {evid_principal(it)} |")
    feitos = itens(con, "canal_slug=%s AND status IN ('pronto','publicado') AND data_prevista >= %s", (canal, ref - timedelta(days=7)))
    if feitos:
        L += ["", "Prontos/publicados recentes: " + "; ".join(f"{i['tema']} ({i['status']}, {fmt_d(i['data_prevista'])})" for i in sorted(feitos, key=lambda x: x["data_prevista"]))]
    desc = con.execute("SELECT tema, motivo, mudou_em FROM youtube.backlog WHERE canal_slug=%s AND status='descartado' ORDER BY mudou_em DESC LIMIT 5", (canal,)).fetchall()
    if desc:
        L += ["", "Descartados recentes: " + "; ".join(f"{t} ({m}, {e.astimezone(TZ):%d/%m})" for t, m, e in desc)]
    L += ["", FIM]
    bloco = "\n".join(L)
    p = REPO / cfg["md"]
    if p.exists():
        txt = p.read_text()
    else:
        p.parent.mkdir(parents=True, exist_ok=True)
        txt = (f"# Backlog — {cfg['nome']}\n\nOs arquivos do canal (regras, roteiros, vídeos `longo-NN/`) moram em `{cfg['videos']}/`; "
               "este arquivo existe só para o espelho do backlog vivo.\n")
    if INI in txt and FIM in txt:
        txt = txt[:txt.index(INI)] + bloco + txt[txt.index(FIM) + len(FIM):]
    else:
        linhas = txt.split("\n")
        # depois do título e do 1º parágrafo
        k = 1
        while k < len(linhas) and linhas[k].strip() == "":
            k += 1
        while k < len(linhas) and linhas[k].strip() != "":
            k += 1
        linhas[k:k] = ["", bloco, ""]
        txt = "\n".join(linhas)
    p.write_text(txt)
    return p


# ---------------- CLI ----------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="c", required=True)
    p = sp.add_parser("listar"); p.add_argument("--canal"); p.add_argument("--todos", action="store_true")
    p = sp.add_parser("calendario"); p.add_argument("--canal"); p.add_argument("--dias", type=int, default=14)
    p = sp.add_parser("importar"); p.add_argument("arquivo"); p.add_argument("--canal", required=True); p.add_argument("--fonte")
    p = sp.add_parser("add")
    for a in ("--canal", "--tema", "--slug", "--motivo"):
        p.add_argument(a, required=True)
    p.add_argument("--status", default="proposto"); p.add_argument("--data"); p.add_argument("--video-id", type=int); p.add_argument("--pasta")
    p.add_argument("--angulo"); p.add_argument("--titulo"); p.add_argument("--janela"); p.add_argument("--riscos")
    p.add_argument("--demanda", type=float); p.add_argument("--encaixe", type=float); p.add_argument("--urgencia", type=float)
    p.add_argument("--evidencias", help="JSON (lista) ou caminho de arquivo .json")
    p = sp.add_parser("nota"); p.add_argument("id", type=int); p.add_argument("--demanda", type=float, required=True)
    p.add_argument("--encaixe", type=float, required=True); p.add_argument("--urgencia", type=float, required=True); p.add_argument("--motivo", required=True)
    p.add_argument("--janela"); p.add_argument("--evidencias")
    p = sp.add_parser("descartar"); p.add_argument("id", type=int); p.add_argument("--motivo", required=True)
    p = sp.add_parser("status"); p.add_argument("id", type=int); p.add_argument("status"); p.add_argument("--motivo", required=True)
    sp.add_parser("sync")
    p = sp.add_parser("agendar"); p.add_argument("--canal")
    p = sp.add_parser("md"); p.add_argument("--canal")
    sp.add_parser("tudo")
    a = ap.parse_args()

    def ev(x):
        if not x:
            return None
        return json.loads(Path(x).read_text()) if os.path.exists(x) else json.loads(x)

    with conectar() as con:
        if a.c == "listar":
            w = "true" if a.todos else "status <> 'descartado' AND (status NOT IN ('publicado') OR data_prevista >= current_date - 7)"
            args = ()
            if a.canal:
                w += " AND canal_slug=%s"; args = (a.canal,)
            for it in itens(con, w, args):
                print(f"{it['id']:>4} {it['canal_slug']:<18} {str(it['nota'] or '-'):>4} {it['status']:<12} {fmt_d(it['data_prevista']):<10} {it['tema']}")
        elif a.c == "calendario":
            ref = hoje()
            for c in ([a.canal] if a.canal else CANAIS):
                print(f"== {c}")
                occ = {}
                for it in itens(con, "canal_slug=%s AND data_prevista IS NOT NULL AND status<>'descartado'", (c,)):
                    occ.setdefault(it["data_prevista"], []).append(f"{it['tema']} [{it['status']}]")
                for d in slots(con, ref, ref + timedelta(days=a.dias)):
                    print(f"  {fmt_d(d)} ({dia_fds(con, d)}-semana): {', '.join(occ.get(d, ['— vaga']))}")
        elif a.c == "importar":
            importar(con, a.arquivo, a.canal, a.fonte)
        elif a.c == "add":
            nota = calc_nota(a.demanda, a.encaixe, a.urgencia)
            r = con.execute("INSERT INTO youtube.backlog (canal_slug,tema,slug,angulo,titulo_candidato,evidencias,demanda,encaixe,urgencia,nota,janela_ate,riscos,"
                            "status,data_prevista,video_id,pasta,motivo,historico) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                            "ON CONFLICT (canal_slug, slug) DO NOTHING RETURNING id",
                            (a.canal, a.tema, a.slug, a.angulo, a.titulo, Jsonb(ev(a.evidencias) or []), a.demanda, a.encaixe, a.urgencia, nota,
                             a.janela, a.riscos, a.status, a.data, a.video_id, a.pasta, a.motivo,
                             Jsonb([{"em": datetime.now(TZ).isoformat(timespec="minutes"), "para": a.status, "motivo": a.motivo}]))).fetchone()
            print(f"ok id {r[0]}" if r else f"já existe {a.canal}/{a.slug} (use nota/status)")
        elif a.c in ("nota", "descartar", "status"):
            st = con.execute("SELECT status FROM youtube.backlog WHERE id=%s", (a.id,)).fetchone()
            if not st:
                raise SystemExit("id não existe")
            if a.c == "nota":
                if st[0] in CONGELADOS:
                    raise SystemExit(f"id {a.id} está {st[0]}: congelado")
                campos = dict(demanda=a.demanda, encaixe=a.encaixe, urgencia=a.urgencia, nota=calc_nota(a.demanda, a.encaixe, a.urgencia))
                if a.janela:
                    campos["janela_ate"] = a.janela
                if a.evidencias:
                    campos["evidencias"] = ev(a.evidencias)
                if st[0] == "descartado":
                    campos["status"] = "proposto"
                mudar(con, a.id, a.motivo, **campos)
            elif a.c == "descartar":
                if st[0] in CONGELADOS:
                    raise SystemExit(f"id {a.id} está {st[0]}: congelado, não descarto")
                mudar(con, a.id, a.motivo, status="descartado", data_prevista=None)
            else:
                ordem = ["proposto", "agendado", "em_producao", "pronto", "publicado"]
                if st[0] in CONGELADOS and (a.status not in ordem or ordem.index(a.status) < ordem.index(st[0])):
                    raise SystemExit(f"id {a.id} está {st[0]}: congelado (só avança)")
                mudar(con, a.id, a.motivo, status=a.status)
            print("ok")
        elif a.c == "sync":
            print(f"sync: {sync(con)} mudança(s)")
        elif a.c == "agendar":
            agendar(con, a.canal)
            print("ok")
        elif a.c == "md":
            for c in ([a.canal] if a.canal else CANAIS):
                print(gerar_md(con, c).relative_to(REPO))
        elif a.c == "tudo":
            sync(con)
            agendar(con)
            for c in CANAIS:
                print(gerar_md(con, c).relative_to(REPO))


if __name__ == "__main__":
    main()
