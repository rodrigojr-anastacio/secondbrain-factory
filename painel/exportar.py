#!/usr/bin/env python3
"""Exporta os dados do Painel da Fábrica (só leitura) para painel/dist/.

Lê o banco `vida` (apenas SELECT) e o repo; grava:
  painel/dist/data.json   tudo o que a página mostra
  painel/dist/thumbs/*.jpg  thumbs redimensionadas (~480 px, < 60 KB cada)

Uso (a partir de qualquer pasta):
  ~/workspace/fabrica-youtube/tools/.venv/bin/python ~/workspace/fabrica-youtube/painel/exportar.py

Idempotente: apaga e recria dist/thumbs e data.json. Não grava nada no banco.
"""
from __future__ import annotations

import datetime as dt
import decimal
import json
import os
import re
import shutil
import sys
from pathlib import Path

import psycopg
from PIL import Image

PAINEL = Path(__file__).resolve().parent
REPO = PAINEL.parent
WORKSPACE = REPO.parent
DIST = PAINEL / "dist"
THUMBS = DIST / "thumbs"
RELATORIOS = WORKSPACE / "relatorios"

THUMB_W = 480
THUMB_MAX = 60 * 1024
SALDO_ALERTA_USD = 10  # abaixo disso: alerta; abaixo de 0: crítico

# Fatos de exibição que o banco ainda não tem (dados pelo Rodrigo/orquestrador)
STATUS_EXIBICAO = {"lotr-fr": "stand-by"}
CANAIS_EXTRA = [
    # canal em teste, ainda sem linha em youtube.canais; gastos lançados nos projetos abaixo
    {"slug": "em-relevo", "nome": "Em Relevo (clima)", "idioma": "en/pt", "status": "em teste",
     "projetos": ["em-relevo", "clima"], "pesquisa": "pesquisa/canal-clima-2026-11"},
]
ORDEM_CANAIS = ["historia-ptbr", "dossie-es", "em-relevo", "lotr-fr"]


# ---------------------------------------------------------------- utilidades
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
TOKEN_RE = re.compile(r"\b(sk-[A-Za-z0-9_-]{12,}|ghp_[A-Za-z0-9]{20,}|xox[abp]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{30,}|ya29\.[0-9A-Za-z_-]+)")
CONN_RE = re.compile(r"postgres(ql)?://\S+")


def limpar(texto: str | None) -> str | None:
    """Tira de qualquer texto o que não pode ir para uma página publicada."""
    if texto is None:
        return None
    linhas = [ln for ln in texto.splitlines() if ".segredos" not in ln]
    t = "\n".join(linhas)
    t = EMAIL_RE.sub("[e-mail omitido]", t)
    t = TOKEN_RE.sub("[omitido]", t)
    t = CONN_RE.sub("[omitido]", t)
    t = t.replace(str(Path.home()) + "/workspace/", "~/workspace/").replace(str(Path.home()), "~")
    return t


def num(v):
    if isinstance(v, decimal.Decimal):
        f = float(v)
        return int(f) if f.is_integer() and abs(f) < 1e15 else round(f, 4)
    return v


def linhas(cur, sql, params=None):
    cur.execute(sql, params or ())
    cols = [c.name for c in cur.description]
    out = []
    for r in cur.fetchall():
        d = {}
        for c, v in zip(cols, r):
            if isinstance(v, (dt.date, dt.datetime)):
                v = v.isoformat()
            d[c] = num(v)
        out.append(d)
    return out


def ler(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO))
    except ValueError:
        try:
            return "~/workspace/" + str(p.relative_to(WORKSPACE))
        except ValueError:
            return p.name


# ---------------------------------------------------------------- thumbs
def gerar_thumb(src: Path, nome: str) -> dict | None:
    try:
        im = Image.open(src)
        im = im.convert("RGB")
    except Exception:  # noqa: BLE001
        return None
    if im.width > THUMB_W:
        h = round(im.height * THUMB_W / im.width)
        im = im.resize((THUMB_W, h), Image.LANCZOS)
    dest = THUMBS / f"{nome}.jpg"
    for q in (75, 68, 60, 52, 45):
        im.save(dest, "JPEG", quality=q, optimize=True, progressive=True)
        if dest.stat().st_size < THUMB_MAX:
            break
    return {"arquivo": f"thumbs/{dest.name}", "origem": rel(src), "w": im.width, "h": im.height}


def candidatos_thumb(canal: str, pasta: Path) -> list[Path]:
    """Principal primeiro (a que está no ar / out/thumbnail), depois variantes (máx. 3)."""
    principal: list[Path] = []
    galeria = REPO / "conhecimento" / "thumbnails" / f"{canal}-{pasta.name}.jpg"
    if galeria.exists():
        principal.append(galeria)
    else:
        for n in ("thumbnail.jpg", "thumbnail.png"):
            if (pasta / "out" / n).exists():
                principal.append(pasta / "out" / n)
                break
    variantes: list[Path] = []
    for d in (pasta / "entrega", pasta / "out"):
        if not d.is_dir():
            continue
        achadas = sorted(p for p in d.iterdir() if re.match(r"thumb[-_].+\.(jpg|png)$", p.name, re.I))
        # se houver jpg e png do mesmo nome, fica o jpg
        vistos = set()
        for p in achadas:
            if p.stem in vistos:
                continue
            vistos.add(p.stem)
            variantes.append(p)
        if variantes:
            break
    return (principal + variantes)[:4]


# ---------------------------------------------------------------- pesquisas
def titulo_md(md: str, fallback: str) -> str:
    for ln in md.splitlines():
        m = re.match(r"#\s+(.+)", ln.strip())
        if m:
            return m.group(1).strip()
    return fallback


def data_doc(p: Path) -> str:
    m = re.search(r"(20\d\d-\d\d-\d\d)", str(p))
    if m and re.search(r"(20\d\d-\d\d-\d\d)", p.name):
        return m.group(1)
    return dt.date.fromtimestamp(p.stat().st_mtime).isoformat()


def coletar_pesquisas() -> list[dict]:
    arquivos: list[tuple[Path, str]] = []
    pesq = REPO / "pesquisa"
    for d in sorted(pesq.iterdir()):
        if not d.is_dir():
            continue
        if d.name in ("tendencias", "palavras-chave", "metricas"):
            for p in d.glob("*.md"):
                arquivos.append((p, d.name))
            continue
        for nome in ("RELATORIO.md", "LEVANTAMENTO.md", "IDIOMA.md", "PADRAO.md"):
            for p in [d / nome, *d.glob(f"*/{nome}")]:
                if p.exists() and "node_modules" not in p.parts:
                    arquivos.append((p, "nicho/estudo"))
    for rot in ("tendencias", "palavras-chave", "metricas"):
        d = RELATORIOS / rot
        if d.is_dir():
            for p in d.glob("*.md"):
                arquivos.append((p, f"rotina {rot}"))
    docs, vistos, conteudos = [], set(), set()
    # caminhos do repo primeiro: a cópia em ~/workspace/relatorios (mesmo texto) é descartada
    arquivos.sort(key=lambda a: 0 if REPO in a[0].parents else 1)
    for p, origem in arquivos:
        if p in vistos:
            continue
        vistos.add(p)
        md = limpar(ler(p)) or ""
        if not md.strip() or md.strip() in conteudos:
            continue
        conteudos.add(md.strip())
        r = rel(p)
        docs.append({
            "id": re.sub(r"[^a-z0-9]+", "-", r.lower()).strip("-"),
            "titulo": titulo_md(md, p.stem),
            "data": data_doc(p),
            "origem": origem,
            "caminho": r,
            "palavras": len(md.split()),
            "md": md,
        })
    docs.sort(key=lambda d: (d["data"], d["caminho"]), reverse=True)
    return docs


# ---------------------------------------------------------------- principal
def main() -> int:
    t0 = dt.datetime.now()
    hoje = dt.date.today()
    mes_atual = hoje.replace(day=1)
    con = psycopg.connect(os.environ.get("FABRICA_DB", "dbname=vida"))
    con.read_only = True
    cur = con.cursor()

    canais_db = linhas(cur, "select slug, nome, channel_id, idioma, nicho, status from youtube.canais where status <> 'arquivado'")
    videos = linhas(cur, """
        select v.id, v.canal_slug, v.numero, v.titulo, v.status, v.pasta, v.youtube_id, v.publicado_em,
               v.duracao_s, v.biblia_versao, v.criado_em::date as criado_em, v.atualizado_em::date as atualizado_em,
               c.custo_direto_brl, c.rateio_fixo_brl, c.custo_total_brl
          from youtube.videos v left join financas.custo_por_video c on c.id = v.id
         order by v.canal_slug, v.numero""")
    claude = {r["video_id"]: r for r in linhas(cur, """
        select video_id, sum(custo_usd_equivalente) as usd, sum(execucoes) as execucoes
          from youtube.custo_claude_por_video group by video_id""")}
    studio = {r["youtube_id"]: r for r in linhas(cur, "select * from youtube.studio_ultimo")}
    api = {r["youtube_id"]: r for r in linhas(cur, """
        select distinct on (youtube_id) youtube_id, data, views, likes, comentarios, pct_assistido
          from youtube.metricas_video order by youtube_id, data desc""")}
    canal_api = {r["channel_id"]: r for r in linhas(cur, """
        select distinct on (channel_id) channel_id, data, inscritos, views, videos
          from youtube.metricas_canal order by channel_id, data desc""")}
    resumo_mensal = linhas(cur, """
        select projeto, mes, total_brl from financas.resumo_mensal
         where dominio = 'youtube' and mes <= %s order by mes desc, total_brl desc""", (mes_atual,))
    custo_mensal = linhas(cur, """
        select projeto, categoria, fornecedor, mes, valor_brl from financas.custo_mensal
         where dominio = 'youtube' and mes <= %s order by mes desc, valor_brl desc""", (mes_atual,))
    saldos = linhas(cur, "select fornecedor, moeda, recarregado, consumido, saldo from financas.saldo_pre_pago order by saldo")
    medias = linhas(cur, """
        select canal_slug, count(*) as videos, avg(custo_direto_brl) as direto_medio_brl,
               avg(custo_total_brl) as total_medio_brl, sum(custo_direto_brl) as direto_total_brl
          from financas.custo_por_video where custo_direto_brl > 0 group by canal_slug""")
    kw = linhas(cur, """
        (select data, idioma, termo, destino, origem, categoria, score, mediana_top10, recentes_100k,
                tendencia, porta_aberta, validado
           from youtube.palavras_chave_ultima where validado order by score desc nulls last limit 40)
        union all
        (select data, idioma, termo, destino, origem, categoria, score, mediana_top10, recentes_100k,
                tendencia, porta_aberta, validado
           from youtube.palavras_chave_ultima where not validado and destino <> 'novo-canal'
          order by score desc nulls last limit 30)""")
    gar_exec = linhas(cur, "select id, executado_em, canais_vistos, candidatos, relatorio_md from youtube.garimpo_execucoes order by id desc limit 1")
    garimpo = []
    if gar_exec:
        garimpo = linhas(cur, """
            select g.titulo, g.url, g.pais, g.formula, g.decisao, s.videos, s.views, s.inscritos,
                   s.media_views, s.score, s.idade_dias
              from youtube.garimpo_snapshots s join youtube.garimpo_canais g using (channel_id)
             where s.execucao_id = %s order by s.score desc nulls last limit 25""", (gar_exec[0]["id"],))
        for e in gar_exec:
            e["relatorio_md"] = rel(Path(e["relatorio_md"])) if e.get("relatorio_md") else None
    con.close()

    # thumbs
    if THUMBS.exists():
        shutil.rmtree(THUMBS)
    THUMBS.mkdir(parents=True)
    for v in videos:
        v["claude_usd_equiv"] = claude.get(v["id"], {}).get("usd")
        v["studio"] = studio.get(v["youtube_id"]) if v["youtube_id"] else None
        v["api"] = api.get(v["youtube_id"]) if v["youtube_id"] else None
        v["youtube_url"] = f"https://www.youtube.com/watch?v={v['youtube_id']}" if v["youtube_id"] else None
        v["titulo"] = limpar(v["titulo"])
        v.pop("notas", None)
        v["thumbs"] = []
        if v["pasta"] and v["status"] != "arquivado":
            pasta = REPO / v["pasta"]
            for i, src in enumerate(candidatos_thumb(v["canal_slug"], pasta)):
                t = gerar_thumb(src, f"{v['id']:03d}-{i}")
                if t:
                    t["principal"] = i == 0 and (src.name.startswith("thumbnail") or "conhecimento" in src.parts)
                    v["thumbs"].append(t)

    # canais e resumo
    gasto_mes = {}
    for r in resumo_mensal:
        if r["mes"] == mes_atual.isoformat():
            gasto_mes[r["projeto"]] = r["total_brl"]
    canais = []
    for c in canais_db:
        vs = [v for v in videos if v["canal_slug"] == c["slug"]]
        st = [v["studio"] for v in vs if v["studio"]]
        imp = sum(s["impressoes"] or 0 for s in st) if st else None
        ctr = (sum((s["impressoes"] or 0) * float(s["ctr_pct"] or 0) for s in st) / imp) if st and imp else None
        ca = canal_api.get(c["channel_id"]) if c["channel_id"] else None
        canais.append({
            "slug": c["slug"], "nome": limpar(c["nome"]), "idioma": c["idioma"], "nicho": limpar(c["nicho"]),
            "status": STATUS_EXIBICAO.get(c["slug"], "ativo" if c["status"] == "em preparação" and any(v["status"] == "publicado" for v in vs) else c["status"]),
            "youtube_url": f"https://www.youtube.com/channel/{c['channel_id']}" if c["channel_id"] else None,
            "publicados": sum(1 for v in vs if v["status"] == "publicado"),
            "prontos": sum(1 for v in vs if v["status"] == "pronto"),
            "em_producao": sum(1 for v in vs if v["status"] in ("roteiro", "producao", "qa")),
            "ideias_db": sum(1 for v in vs if v["status"] == "ideia"),
            "studio_28d": {
                "periodo_inicio": st[0]["periodo_inicio"], "periodo_fim": st[0]["periodo_fim"],
                "exportado_em": st[0]["exportado_em"], "videos": len(st),
                "impressoes": imp, "ctr_pct": round(ctr, 2) if ctr is not None else None,
                "views": sum(s["views"] or 0 for s in st),
            } if st else None,
            "api": ca,
            "gasto_mes_brl": gasto_mes.get(c["slug"]),
        })
    for e in CANAIS_EXTRA:
        g = [gasto_mes[p] for p in e["projetos"] if p in gasto_mes]
        canais.append({
            "slug": e["slug"], "nome": e["nome"], "idioma": e["idioma"], "nicho": "clima extremo no mapa 3D",
            "status": e["status"], "youtube_url": None, "publicados": 0, "prontos": 0, "em_producao": 0,
            "ideias_db": 0, "studio_28d": None, "api": None,
            "gasto_mes_brl": round(sum(g), 2) if g else None, "pesquisa": e["pesquisa"],
            "sem_registro_no_banco": True,
        })
    canais.sort(key=lambda c: ORDEM_CANAIS.index(c["slug"]) if c["slug"] in ORDEM_CANAIS else 99)

    for s in saldos:
        s["nivel"] = "critico" if (s["saldo"] or 0) < 0 else ("alerta" if (s["saldo"] or 0) < SALDO_ALERTA_USD else "ok")

    backlogs = []
    for c in canais_db:
        p = REPO / "canais" / c["slug"] / "backlog.md"
        if p.exists():
            backlogs.append({"canal": c["slug"], "nome": limpar(c["nome"]), "caminho": rel(p),
                             "atualizado": dt.date.fromtimestamp(p.stat().st_mtime).isoformat(),
                             "md": limpar(ler(p))})
    backlogs.sort(key=lambda b: ORDEM_CANAIS.index(b["canal"]) if b["canal"] in ORDEM_CANAIS else 99)

    meses = sorted({r["mes"] for r in resumo_mensal}, reverse=True)
    gastos = {
        "meses": [{
            "mes": m,
            "total_brl": round(sum(r["total_brl"] for r in resumo_mensal if r["mes"] == m), 2),
            "por_projeto": [r for r in resumo_mensal if r["mes"] == m],
            "itens": [r for r in custo_mensal if r["mes"] == m],
        } for m in meses],
        "saldos": saldos,
        "media_por_video": medias,
        "nota": "Só o domínio youtube de financas (fixos rateados + consumo pago). Custo do Claude é equivalente a preço de lista; o real está no Claude Max (fixo).",
    }

    data = {
        "gerado_em": dt.datetime.now().astimezone().isoformat(timespec="minutes"),
        "mes_atual": mes_atual.isoformat(),
        "saldo_alerta_usd": SALDO_ALERTA_USD,
        "canais": canais,
        "videos": [v for v in videos],
        "backlogs": backlogs,
        "pesquisas": coletar_pesquisas(),
        "palavras_chave": kw,
        "garimpo": {"execucao": gar_exec[0] if gar_exec else None, "canais": garimpo},
        "gastos": gastos,
    }
    DIST.mkdir(exist_ok=True)
    txt = json.dumps(data, ensure_ascii=False, separators=(",", ":"), default=str)
    txt = limpar(txt)  # segunda passada de segurança
    (DIST / "data.json").write_text(txt, encoding="utf-8")

    total = sum(f.stat().st_size for f in DIST.rglob("*") if f.is_file())
    n_thumbs = len(list(THUMBS.glob("*.jpg")))
    maior = max((f.stat().st_size for f in THUMBS.glob("*.jpg")), default=0)
    print(f"data.json {len(txt)/1024:.0f} KB · {n_thumbs} thumbs (maior {maior/1024:.0f} KB) · "
          f"dist {total/1024/1024:.2f} MB · {(dt.datetime.now()-t0).total_seconds():.1f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
