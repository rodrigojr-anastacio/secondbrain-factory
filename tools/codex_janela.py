"""Janela de cota de imagens do Codex (ChatGPT Plus) e portão "um vídeo de cada vez" da fábrica noturna (24/11/2026).

Decisão do Rodrigo (24/11/2026): 2 vídeos por noite (dossie-es + historia-ptbr), sem recarregar a Gemini. Só a geração de
imagens é sequencial: o Dossier SEMPRE vai primeiro; quando ele termina as imagens, avisa e as imagens do História
começam na hora. Fallbacks do aviso: o 1º falhou/foi cancelado/travou, ou chegou o reset da janela, ou passou de
LIBERA_SEM_AVISO (02:00) sem o 1º ter começado as imagens. No 429 do Codex, espera o reset em vez de pagar.

Medido nos codex_log.jsonl (16, 22 e 23/11/2026): o limite de imagem NÃO é o % da janela de 5 h do painel. O 429 vem
como `usage_limit_reached`, limitId `imagegen_premium`, `limit_window_minutes: 1440` e `resets_at`/`resets_in_seconds`:
janela de 24 h contada da 1ª imagem depois do último reset; 270, 250 e 196 imagens até o limite (com 9–36% do 5 h).

Arquivos (em ~/cache/img_codex/, fora do git):
  janela.json          janela atual: inicio, imagens, por_video, limite_em, reset_em, reset_fonte, imagens_ate_limite
  noite-AAAA-MM-DD.json  gravado pelo noturna.py planejar: ordem das imagens, vídeos/jobs, estado das imagens de cada
                       canal (aguardando|gerando|concluido|falhou), liberado_em/liberado_por (o aviso "pode seguir")
  aguarda/<job>.json   marcador do img_codex.py para a fila (job sem cota ou com portão fechado): tipo limite|portao,
                       reset_em; o fila.py põe o job em `pausado_codex` e retoma com --resume quando liberar.
Eventos em ops.event_log (origem img_codex): codex_janela_inicio, codex_limite (imagens até o 429, horário do 429 e do
reset), codex_portao_liberado, codex_aguarda.

CLI (diagnóstico/teste): tools/.venv/bin/python tools/codex_janela.py status | portao --video <id> | liberar --noite D --motivo X
Testes simulados (sem chamar o Codex): tools/.venv/bin/python tools/test_codex_janela.py
"""
import argparse
import fcntl
import json
import os
import re
import sys
from contextlib import contextmanager
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Sao_Paulo")
DIR = Path(os.environ.get("IMG_CODEX_DIR", os.path.expanduser("~/cache/img_codex")))
JANELA_H = float(os.environ.get("CODEX_JANELA_H", "24"))  # medido: limit_window_minutes 1440
FOLGA_RESET_MIN = 10            # depois do reset, espera +10 min antes de retomar
TRAVADO_MIN = 45                # 1º vídeo "gerando" sem imagem nova há 45 min (e sem pausa de cota) = travou → libera
CAPACIDADE_MEDIDA = [270, 250, 196]   # imagens até o 429 por janela de 24 h (16, 22 e 23/11/2026; Hipótese até 3 noites medidas)
LIBERA_SEM_AVISO = "02:00"      # 1º vídeo nem começou as imagens até 02:00 → libera o 2º (a cota está livre)
FIM_NOITE_H = 14                # antes das 14:00 a "noite" é a de ontem
RE_RESET_EPOCH = re.compile(r'resets_at\W{0,6}(\d{10})')
RE_RESET_IN = re.compile(r'resets_in_seconds\W{0,6}(\d+)')
RE_RETRY = re.compile(r'retry[-_ ]after\W{0,6}(\d+)', re.I)
RE_JANELA = re.compile(r'limit_window_minutes\W{0,6}(\d+)')


def agora():
    f = os.environ.get("CODEX_JANELA_AGORA")  # testes: relógio fixo (ISO)
    return datetime.fromisoformat(f).astimezone(TZ) if f else datetime.now(TZ)


def _iso(d):
    return d.astimezone(TZ).isoformat(timespec="seconds") if d else None


def _dt(s):
    return datetime.fromisoformat(s).astimezone(TZ) if s else None


@contextmanager
def _travado(nome):
    DIR.mkdir(parents=True, exist_ok=True)
    with open(DIR / f".{nome}.lock", "a+") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        yield


def _ler(p, padrao=None):
    try:
        return json.loads(Path(p).read_text())
    except (OSError, ValueError):
        return padrao if padrao is not None else {}


def _gravar(p, d):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1, default=str))
    os.replace(tmp, p)


def evento(tipo, sev, msg, det, ref=None):
    if os.environ.get("CODEX_JANELA_SEM_DB"):
        return
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from event_log import registrar
        registrar("img_codex", tipo, sev, msg, det, ref=ref)
    except Exception as e:  # noqa: BLE001
        print(f"[codex_janela] evento não gravado: {e}", file=sys.stderr)


# ---------------- janela de cota ----------------
def janela():
    """Estado da janela atual (vazio se expirou)."""
    j = _ler(DIR / "janela.json")
    if not j.get("inicio"):
        return {}
    fim = _dt(j.get("reset_em")) or (_dt(j["inicio"]) + timedelta(hours=JANELA_H))
    if agora() >= fim:
        return {}
    return j


def reset_previsto(j=None):
    """Reset conhecido (do 429) ou estimado (início + 24 h). None sem janela aberta."""
    j = janela() if j is None else j
    if not j:
        return None
    return _dt(j.get("reset_em")) or (_dt(j["inicio"]) + timedelta(hours=JANELA_H))


def janela_bruta():
    """janela.json como está (mesmo expirada): para saber o último reset conhecido."""
    return _ler(DIR / "janela.json")


def limite_ativo():
    """(True, reset_em) se o Codex acusou limite e o reset ainda não passou (+ folga)."""
    j = janela_bruta()
    if j.get("limite_em") and j.get("reset_em"):
        r = _dt(j["reset_em"]) + timedelta(minutes=FOLGA_RESET_MIN)
        if agora() < r:
            return True, r
    return False, None


def registrar_imagem(video=None, canal=None, n=1):
    """Chamar a cada imagem gerada pelo Codex: abre janela nova se não houver e conta."""
    with _travado("janela"):
        j = janela()
        novo = not j
        if novo:
            j = {"inicio": _iso(agora()), "imagens": 0, "por_video": {}, "limite_em": None, "reset_em": None,
                 "reset_fonte": "estimado"}
        j["imagens"] = j.get("imagens", 0) + n
        if video:
            k = str(video)
            j.setdefault("por_video", {})[k] = j["por_video"].get(k, 0) + n
        j["ultima"] = _iso(agora())
        _gravar(DIR / "janela.json", j)
    if novo:
        evento("codex_janela_inicio", "info", f"janela de imagens do Codex aberta ({canal or '-'} vídeo {video or '-'}); "
               f"reset estimado {reset_previsto(j):%d/%m %H:%M}", {"inicio": j["inicio"], "video": video, "canal": canal,
                                                                  "janela_h": JANELA_H})
    if video:
        _noite_atividade(video)
    return j


def ler_reset(texto="", falha_gen=None, cota=None):
    """Reset do limite a partir da falha do image_gen (resetsAt), da mensagem (resets_at, resets_in_seconds,
    retry-after) ou None. Devolve (datetime|None, fonte, janela_min|None)."""
    jm = RE_JANELA.search(texto or "")
    jmin = int(jm.group(1)) if jm else None
    if isinstance(falha_gen, dict) and str(falha_gen.get("resetsAt") or "").isdigit():
        return datetime.fromtimestamp(int(falha_gen["resetsAt"]), TZ), "falha_gen.resetsAt", jmin
    m = RE_RESET_EPOCH.search(texto or "")
    if m:
        return datetime.fromtimestamp(int(m.group(1)), TZ), "mensagem resets_at", jmin
    m = RE_RESET_IN.search(texto or "") or RE_RETRY.search(texto or "")
    if m:
        return agora() + timedelta(seconds=int(m.group(1))), "mensagem resets_in/retry-after", jmin
    if isinstance(cota, dict) and cota.get("limite_atingido") and cota.get("reset_5h"):
        return datetime.fromtimestamp(int(cota["reset_5h"]), TZ), "rollout reset_5h", jmin
    return None, None, jmin


def registrar_limite(video=None, canal=None, texto="", falha_gen=None, cota=None):
    """429 do Codex: grava horário do limite, reset e nº de imagens na janela; devolve o reset (datetime)."""
    reset, fonte, jmin = ler_reset(texto, falha_gen, cota)
    with _travado("janela"):
        j = janela() or {"inicio": None, "imagens": 0, "por_video": {}}
        ja = bool(j.get("limite_em"))
        if not reset:
            ini = _dt(j.get("inicio"))
            reset = (ini + timedelta(hours=JANELA_H)) if ini else agora() + timedelta(hours=JANELA_H)
            fonte = "estimado (início + %g h)" % JANELA_H if ini else "estimado (agora + %g h)" % JANELA_H
        if not j.get("inicio"):  # janela aberta antes deste registro existir: início = reset − janela
            j["inicio"] = _iso(reset - timedelta(minutes=jmin or JANELA_H * 60))
        if not ja:
            j.update(limite_em=_iso(agora()), imagens_ate_limite=j.get("imagens", 0))
        j.update(reset_em=_iso(reset), reset_fonte=fonte)
        if jmin:
            j["janela_min"] = jmin
        _gravar(DIR / "janela.json", j)
    if not ja:
        evento("codex_limite", "aviso",
               f"Codex sem cota de imagem ({canal or '-'} vídeo {video or '-'}): {j.get('imagens', 0)} imagens na janela "
               f"aberta {_dt(j['inicio']):%d/%m %H:%M}; reset {reset:%d/%m %H:%M} ({fonte}); espera o reset, sem fallback pago",
               {"video": video, "canal": canal, "inicio_janela": j["inicio"], "imagens_ate_limite": j.get("imagens", 0),
                "por_video": j.get("por_video"), "limite_em": j["limite_em"], "reset_em": j["reset_em"],
                "reset_fonte": fonte, "janela_min": jmin, "cota": cota})
    return reset


# ---------------- noite (ordem das imagens) ----------------
def noite_atual(t=None):
    t = t or agora()
    return (t - timedelta(days=1)).date() if t.hour < FIM_NOITE_H else t.date()


def arq_noite(noite):
    return DIR / f"noite-{noite:%Y-%m-%d}.json"


def gravar_noite(noite, ordem, videos):
    """noturna.py planejar: ordem = canais na ordem das imagens; videos = {canal: {video, e1, e2, pasta, prazo}}."""
    with _travado("noite"):
        p = arq_noite(noite)
        d = _ler(p) or {"noite": f"{noite:%Y-%m-%d}", "criado_em": _iso(agora()), "imagens": {}, "liberado_em": None,
                        "liberado_por": None}
        d["ordem"] = [c for c in ordem if c in videos or c in d.get("videos", {})]
        d.setdefault("videos", {}).update(videos)
        for c in videos:  # vídeo novo (ou substituto da embalagem reprovada) recomeça "aguardando"
            d["imagens"][c] = {"estado": "aguardando"}
        for c in d["ordem"]:
            d["imagens"].setdefault(c, {"estado": "aguardando"})
        _gravar(p, d)
    return d


def noite_do_video(video):
    """(noite_dict, canal, path) do registro de noite (últimos 3 dias) que tem este vídeo; ou (None, None, None)."""
    if not video:
        return None, None, None
    hoje = agora().date()
    for k in range(0, 4):
        p = arq_noite(hoje - timedelta(days=k))
        d = _ler(p)
        for canal, v in (d.get("videos") or {}).items():
            if str(v.get("video")) == str(video):
                return d, canal, p
    return None, None, None


def noite_do_job(nome):
    hoje = agora().date()
    for k in range(0, 4):
        p = arq_noite(hoje - timedelta(days=k))
        d = _ler(p)
        for canal, v in (d.get("videos") or {}).items():
            if nome in (v.get("e1"), v.get("e2")):
                return d, canal, p
    return None, None, None


def _noite_atividade(video):
    d, canal, p = noite_do_video(video)
    if not d:
        return
    with _travado("noite"):
        d = _ler(p)
        im = d.setdefault("imagens", {}).setdefault(canal, {})
        if im.get("estado") in (None, "aguardando"):
            im.update(estado="gerando", inicio=_iso(agora()))
        im["ultima"] = _iso(agora())
        _gravar(p, d)


def marcar_imagens(video, estado, motivo=""):
    """img_codex.py: estado das imagens do vídeo na noite (gerando|concluido|falhou). O 1º da ordem concluído/falho
    libera o 2º na hora (o aviso "pode seguir")."""
    d, canal, p = noite_do_video(video)
    if not d:
        return None
    with _travado("noite"):
        d = _ler(p)
        im = d.setdefault("imagens", {}).setdefault(canal, {})
        if im.get("estado") != estado:
            im.update(estado=estado, **({"fim": _iso(agora())} if estado in ("concluido", "falhou") else {}))
            if motivo:
                im["motivo"] = motivo
        _gravar(p, d)
    if estado in ("concluido", "falhou") and d.get("ordem") and d["ordem"][0] == canal:
        liberar(date.fromisoformat(d["noite"]), f"{canal}: imagens {estado}" + (f" ({motivo})" if motivo else ""))
    return d


def liberar(noite, motivo):
    p = arq_noite(noite)
    with _travado("noite"):
        d = _ler(p)
        if not d or d.get("liberado_em"):
            return False
        d.update(liberado_em=_iso(agora()), liberado_por=motivo)
        _gravar(p, d)
    seg = d["ordem"][1] if len(d.get("ordem", [])) > 1 else None
    evento("codex_portao_liberado", "info", f"noite {noite:%d/%m}: imagens de {seg or '-'} liberadas ({motivo})",
           {"noite": d["noite"], "motivo": motivo, "ordem": d.get("ordem")}, ref=(d["videos"].get(seg) or {}).get("e2") if seg else None)
    return True


def _status_job(nome):
    if not nome or os.environ.get("CODEX_JANELA_SEM_DB"):
        return _ler(DIR / "test-status.json").get(nome) if nome else None  # testes
    try:
        import psycopg
        with psycopg.connect(os.environ.get("FABRICA_DB", "dbname=vida"), autocommit=True) as con:
            r = con.execute("SELECT status FROM ops.fila_jobs WHERE nome=%s", (nome,)).fetchone()
            return r[0] if r else None
    except Exception:  # noqa: BLE001
        return None


def portao(video):
    """Pode gerar imagens deste vídeo agora? → (ok, motivo, retomar_em|None).
    1) limite ativo da cota → espera o reset; 2) 2º da noite → espera o aviso do 1º (com fallbacks)."""
    lim, r = limite_ativo()
    if lim:
        return False, f"Codex sem cota de imagem até {r:%d/%m %H:%M} (reset + {FOLGA_RESET_MIN} min)", r
    d, canal, _ = noite_do_video(video)
    if not d or len(d.get("ordem", [])) < 2 or d["ordem"][0] == canal or canal not in d["ordem"]:
        return True, "sem portão (1º da noite ou fora da fábrica noturna)", None
    return _portao_noite(d)


def _portao_noite(d):
    if d.get("liberado_em"):
        return True, f"liberado {_dt(d['liberado_em']):%H:%M} ({d.get('liberado_por')})", None
    noite = date.fromisoformat(d["noite"])
    pri = d["ordem"][0]
    v1 = d["videos"].get(pri) or {}
    im = (d.get("imagens") or {}).get(pri) or {}
    t = agora()
    motivo = None
    s1, s2 = _status_job(v1.get("e1")), _status_job(v1.get("e2"))
    if im.get("estado") in ("concluido", "falhou"):
        motivo = f"{pri}: imagens {im['estado']}"
    elif s1 in ("falhou", "bloqueado", "cancelado") or s2 in ("falhou", "bloqueado", "cancelado", "concluido"):
        motivo = f"{pri}: e1 {s1}, e2 {s2}"
    elif im.get("estado") == "gerando" and im.get("ultima") and s2 != "pausado_codex" \
            and t - _dt(im["ultima"]) > timedelta(minutes=TRAVADO_MIN):
        motivo = f"{pri}: sem imagem nova há {TRAVADO_MIN}+ min (travou)"
    else:
        jb = janela_bruta()
        r = _dt(jb.get("reset_em")) or (_dt(jb["inicio"]) + timedelta(hours=JANELA_H) if jb.get("inicio") else None)
        if r and im.get("estado") == "gerando" and _dt(im.get("inicio")) and _dt(im["inicio"]) < r \
                and t >= r + timedelta(minutes=FOLGA_RESET_MIN):
            motivo = f"reset da janela ({r:%H:%M}) sem aviso de {pri}"
        h, m = map(int, LIBERA_SEM_AVISO.split(":"))
        corte = datetime.combine(noite + timedelta(days=1), datetime.min.time()).replace(hour=h, minute=m, tzinfo=TZ)
        if not motivo and im.get("estado") in (None, "aguardando") and t >= corte:
            motivo = f"{pri} não começou as imagens até {LIBERA_SEM_AVISO}"
    if motivo:
        liberar(noite, motivo)
        return True, f"liberado agora ({motivo})", None
    r = reset_previsto()
    return False, f"aguardando o aviso de {pri} (imagens: {im.get('estado', 'aguardando')})", r


def portao_job(nome):
    """fila.py antes de iniciar um job: o e2 do 2º vídeo da noite só sobe com o portão aberto. → (ok, motivo)."""
    d, canal, _ = noite_do_job(nome)
    if not d or len(d.get("ordem", [])) < 2 or d["ordem"][0] == canal or canal not in d["ordem"]:
        return True, ""
    if nome != (d["videos"].get(canal) or {}).get("e2"):
        return True, ""
    ok, motivo, _ = _portao_noite(d)
    if ok:
        lim, r = limite_ativo()
        if lim:
            return False, f"Codex sem cota até {r:%d/%m %H:%M}"
    return ok, motivo


# ---------------- marcador para a fila ----------------
def marcar_aguarda(tipo, motivo, reset_em=None, video=None, canal=None, faltando=None):
    """img_codex.py (código de saída 4): grava aguarda/<FILA_JOB>.json para o fila.py pausar o job (pausado_codex)."""
    job = os.environ.get("FILA_JOB")
    det = {"tipo": tipo, "motivo": motivo, "reset_em": _iso(reset_em), "video": video, "canal": canal,
           "faltando": faltando, "em": _iso(agora()), "job": job}
    if job:
        _gravar(DIR / "aguarda" / f"{job}.json", det)
    evento("codex_aguarda", "aviso", f"{canal or '-'} vídeo {video or '-'}: imagens em espera ({motivo})", det, ref=job)
    return det


def ler_aguarda(job):
    return _ler(DIR / "aguarda" / f"{job}.json") or None


def limpar_aguarda(job):
    (DIR / "aguarda" / f"{job}.json").unlink(missing_ok=True)


def pode_retomar(job, prazo=None, apos_prazo=False):
    """fila.py: job em pausado_codex pode voltar? → (ok, motivo, retomar_em). Reset depois do prazo do job só retoma
    com apos_prazo (padrão: não; fica retomável com `fila.sh retomar <nome>`)."""
    m = ler_aguarda(job) or {}
    video = m.get("video")
    lim, r = limite_ativo()
    if lim:
        if prazo and r > prazo and not apos_prazo:
            return False, f"reset {r:%d/%m %H:%M} depois do prazo {prazo.astimezone(TZ):%d/%m %H:%M}: retome com fila.sh retomar", None
        return False, f"aguarda o reset {r:%d/%m %H:%M}", r
    if m.get("tipo") == "limite" and m.get("reset_em"):
        r = _dt(m["reset_em"]) + timedelta(minutes=FOLGA_RESET_MIN)
        if agora() < r:
            if prazo and r > prazo and not apos_prazo:
                return False, f"reset {r:%d/%m %H:%M} depois do prazo: retome com fila.sh retomar", None
            return False, f"aguarda o reset {r:%d/%m %H:%M}", r
    if video:
        ok, motivo, r = portao(video)
        return ok, motivo, r
    return True, "sem trava", None


def status_txt():
    j = janela()
    L = []
    if j:
        L.append(f"janela aberta {_dt(j['inicio']):%d/%m %H:%M}: {j.get('imagens', 0)} imagens; reset "
                 f"{reset_previsto(j):%d/%m %H:%M} ({j.get('reset_fonte')})" + (f"; LIMITE desde {_dt(j['limite_em']):%d/%m %H:%M}" if j.get("limite_em") else ""))
    else:
        L.append("sem janela aberta (a próxima imagem abre uma de %g h)" % JANELA_H)
    for k in range(0, 3):
        n = noite_atual() - timedelta(days=k)
        d = _ler(arq_noite(n))
        if d:
            im = d.get("imagens", {})
            L.append(f"noite {d['noite']}: ordem {' → '.join(d.get('ordem', []))}; "
                     + "; ".join(f"{c} {im.get(c, {}).get('estado')}" for c in d.get("ordem", []))
                     + (f"; liberado {_dt(d['liberado_em']):%H:%M} ({d['liberado_por']})" if d.get("liberado_em") else "; não liberado"))
    for p in sorted((DIR / "aguarda").glob("*.json")) if (DIR / "aguarda").is_dir() else []:
        m = _ler(p)
        L.append(f"aguarda: {p.stem} ({m.get('tipo')}: {m.get('motivo')})")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="c", required=True)
    sp.add_parser("status")
    p = sp.add_parser("portao"); p.add_argument("--video", required=True)
    p = sp.add_parser("liberar"); p.add_argument("--noite", required=True); p.add_argument("--motivo", default="manual")
    a = ap.parse_args()
    if a.c == "status":
        print(status_txt())
    elif a.c == "portao":
        ok, motivo, r = portao(a.video)
        print(("ABERTO" if ok else "FECHADO") + f": {motivo}" + (f" (retomar ~{r:%d/%m %H:%M})" if r else ""))
        sys.exit(0 if ok else 4)
    elif a.c == "liberar":
        print("liberado" if liberar(date.fromisoformat(a.noite), a.motivo) else "já estava liberado (ou noite sem registro)")


if __name__ == "__main__":
    main()
