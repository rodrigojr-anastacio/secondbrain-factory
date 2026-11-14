"""Rotina semanal de reembalagem (padrão Lutz): parte determinística, sem IA. 14/11/2026.

Subcomandos (rodar com tools/.venv/bin/python, de qualquer pasta):
  preparar [--data AAAA-MM-DD] [--teste] [--limite N]
      baixa a Reporting API, fotografa título/thumb no ar, escolhe a fonte de impressões/CTR, mede retenção, classifica os
      vídeos nos 3 padrões, aplica o ciclo de vida de youtube.reembalagem e grava
      ~/workspace/relatorios/reembalagem/dados/<data>[-teste].json e .md (entrada do agente; prompts/reembalagem.md).
      --teste: não grava nada em youtube.reembalagem e, se não houver candidato elegível, simula até --limite (padrão 1)
      candidatos do padrão 1 ignorando a quarentena (marcados "simulacao").
  registrar --json <dados.json> --youtube-id X --t1 .. --t2 .. --padrao-t1 .. --padrao-t2 .. --thumb .. --porque .. --crivo ..
      grava a sugestão aprovada no crivo (status sugerido, métricas "antes" do JSON).
  marcar --youtube-id X --aplicado AAAA-MM-DD [--notas ..]   marca a troca na mão (quando a detecção não pega, ex.: A/B)
  semear-lote                                                 registra os 15 da reembalagem de 14/11 (idempotente)
  placar                                                      estado de cada vídeo na tabela
Limiares e ciclo: docstring de classificar() e ciclo_de_vida(); explicados também em prompts/reembalagem.md.
Nunca imprime token.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import statistics as st
import subprocess
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
from googleapiclient.discovery import build  # noqa: E402

from _paths import FABRICA, TOKENS  # noqa: E402
from db import conectar  # noqa: E402
from report import creds_for  # noqa: E402

CANAIS = ["historia-ptbr", "dossie-es", "em-relevo", "lugares-guerra-en"]
SAIDA = os.path.expanduser("~/workspace/relatorios/reembalagem")
WARP = "socks5h://127.0.0.1:40000"

# ---- limiares (documentados em prompts/reembalagem.md) ----
MIN_IMP = 300            # abaixo disso: "sem dados suficientes"
MIN_IDADE = 7            # dias no ar
NICHO_CTR = (4.0, 8.0)   # faixa comum de documentário (Hipótese, pesquisa/benchmark-2026-11-14/RELATORIO.md §4)
NICHO_RET = (35.0, 50.0)
REF_CTR_PADRAO, REF_RET_PADRAO = 5.0, 42.0   # quando o canal tem < 3 vídeos com MIN_IMP
JANELA = 28
MIN_DIAS_API = 21        # dias da janela que a Reporting API precisa cobrir para ser a fonte principal
STUDIO_VALIDADE = 10     # export do Studio vale até 10 dias
QUARENTENA = 21
SILENCIO_SUGERIDO = 28   # 4 semanas
ENVELHECIDO_DIAS, ENVELHECIDO_IMP_SEM = 90, 100
MAX_PROPOSTAS = 5
MELHORA_REL, MELHORA_PP = 1.15, 0.5   # melhorou = CTR depois ≥ 1,15× antes E +0,5 pp, com ≥ MIN_IMP depois
QUEDA_FORTE = 0.7        # CTR atual < 0,7× referência = piorou muito


def d(s):
    return s if isinstance(s, dt.date) else dt.date.fromisoformat(str(s)[:10])


def migrar(con):
    con.execute(open(os.path.join(TOOLS, "db", "schema_reembalagem.sql")).read())
    con.execute(open(os.path.join(TOOLS, "db", "schema_alcance.sql")).read())


def norm(t):
    return re.sub(r"\s+", " ", (t or "").strip()).casefold()


# ------------------------------------------------------------------ coleta
def sha1_thumb(url):
    if not url:
        return None
    try:
        out = subprocess.run(["curl", "-sf", "--max-time", "30", "--proxy", WARP, url], capture_output=True, timeout=40)
        return hashlib.sha1(out.stdout).hexdigest() if out.returncode == 0 and out.stdout else None
    except Exception:  # noqa: BLE001
        return None


def dur_s(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0


def fotografar(con, slug, hoje, avisos):
    """Data API (token do próprio canal): vídeos longos públicos + título/thumb no ar → embalagem_snapshot."""
    try:
        yt = build("youtube", "v3", credentials=creds_for(slug))
        ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
        up, ids, tok = ch["contentDetails"]["relatedPlaylists"]["uploads"], [], None
        while True:
            r = yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=50, pageToken=tok).execute()
            ids += [i["contentDetails"]["videoId"] for i in r["items"]]
            tok = r.get("nextPageToken")
            if not tok:
                break
        vids = []
        for i in range(0, len(ids), 50):
            vids += yt.videos().list(part="snippet,status,contentDetails", id=",".join(ids[i:i + 50])).execute()["items"]
    except Exception as e:  # noqa: BLE001
        avisos.append(f"{slug}: Data API falhou ({type(e).__name__}: {str(e)[:120]})")
        return []
    out = []
    for v in vids:
        if v["status"].get("privacyStatus") != "public" or dur_s(v["contentDetails"].get("duration")) <= 60:
            continue
        th = v["snippet"].get("thumbnails", {})
        url = (th.get("maxres") or th.get("high") or th.get("default") or {}).get("url")
        sha = sha1_thumb(url)
        if re.search(r"\(\d*\s*$|\(\d{2,3}\)", v["snippet"]["title"]):
            avisos.append(f"{slug}: título no ar parece colado com sobra (\"{v['snippet']['title']}\", {v['id']}): conferir no Studio")
        row = {"youtube_id": v["id"], "canal_slug": slug, "titulo": v["snippet"]["title"], "thumb_url": url,
               "thumb_sha1": sha, "publicado_em": v["snippet"]["publishedAt"], "duracao_s": dur_s(v["contentDetails"]["duration"])}
        con.execute("INSERT INTO embalagem_snapshot (youtube_id,data,canal_slug,titulo,thumb_url,thumb_sha1,privacidade,publicado_em)"
                    " VALUES (%s,%s,%s,%s,%s,%s,'public',%s) ON CONFLICT (youtube_id,data) DO UPDATE SET titulo=EXCLUDED.titulo,"
                    " thumb_url=EXCLUDED.thumb_url, thumb_sha1=COALESCE(EXCLUDED.thumb_sha1, embalagem_snapshot.thumb_sha1)",
                    (v["id"], hoje, slug, row["titulo"], url, sha, row["publicado_em"]))
        out.append(row)
    return out


def analytics_janela(slug, ini, fim, avisos):
    """Analytics API: views, % média assistida e duração média por vídeo na janela."""
    try:
        ya = build("youtubeAnalytics", "v2", credentials=creds_for(slug))
        r = ya.reports().query(ids="channel==MINE", startDate=str(ini), endDate=str(fim), dimensions="video",
                               metrics="views,estimatedMinutesWatched,averageViewPercentage,averageViewDuration",
                               sort="-views", maxResults=200).execute()
        return {row[0]: {"views": row[1], "minutos": row[2], "ret": round(row[3], 2), "dur_media_s": row[4]} for row in r.get("rows", [])}
    except Exception as e:  # noqa: BLE001
        avisos.append(f"{slug}: Analytics API falhou ({type(e).__name__}: {str(e)[:120]})")
        return {}


def alcance_api(con, slug, ini, fim):
    rows = con.execute("SELECT video_id, sum(impressoes), sum(impressoes*ctr), count(DISTINCT data), min(data), max(data)"
                       " FROM alcance_diario WHERE canal_slug=%s AND fonte='channel_reach_basic_a1' AND data BETWEEN %s AND %s"
                       " GROUP BY 1", (slug, ini, fim)).fetchall()
    return {r[0]: {"imp": int(r[1] or 0), "ctr": round(float(r[2] or 0) / float(r[1]) * 100, 2) if r[1] else None,
                   "dias": r[3], "ini": str(r[4]), "fim": str(r[5])} for r in rows}


def escolher_fonte(con, slug, hoje):
    """API se cobrir ≥ MIN_DIAS_API dos 28 dias; senão o export do Studio mais recente (≤ 10 dias); senão API parcial."""
    mx = con.execute("SELECT max(data) FROM alcance_diario WHERE canal_slug=%s AND fonte='channel_reach_basic_a1'", (slug,)).fetchone()[0]
    dias_api = 0
    if mx:
        ini = mx - dt.timedelta(days=JANELA - 1)
        dias_api = con.execute("SELECT count(DISTINCT inicio) FROM reporting_relatorios WHERE canal_slug=%s AND tipo='channel_reach_basic_a1'"
                               " AND inicio BETWEEN %s AND %s", (slug, ini, mx)).fetchone()[0]
        if dias_api >= MIN_DIAS_API:
            return {"fonte": "reporting_api", "ini": str(ini), "fim": str(mx), "dias_api": dias_api}
    s = con.execute("SELECT exportado_em, periodo_inicio, periodo_fim FROM studio_video WHERE canal_slug=%s"
                    " ORDER BY exportado_em DESC, periodo_fim DESC LIMIT 1", (slug,)).fetchone()
    if s and (hoje - s[0]).days <= STUDIO_VALIDADE:
        return {"fonte": "studio", "exportado_em": str(s[0]), "ini": str(s[1]), "fim": str(s[2]), "dias_api": dias_api,
                "api_ultimo_dia": str(mx) if mx else None}
    fim = mx or (hoje - dt.timedelta(days=3))
    return {"fonte": "reporting_api_parcial", "ini": str(fim - dt.timedelta(days=JANELA - 1)), "fim": str(fim), "dias_api": dias_api}


HOJE = dt.date.today()   # trocado por preparar(--data)


def metricas_canal(con, slug, vids, fonte, avisos):
    ini, fim = d(fonte["ini"]), d(fonte["fim"])
    an = analytics_janela(slug, ini, fim, avisos)
    api = alcance_api(con, slug, ini, fim)
    studio = {}
    if fonte["fonte"] == "studio":
        for r in con.execute("SELECT youtube_id, impressoes, ctr_pct, pct_visualizada, views FROM studio_video"
                             " WHERE canal_slug=%s AND exportado_em=%s AND periodo_fim=%s", (slug, fonte["exportado_em"], fim)):
            studio[r[0]] = {"imp": r[1], "ctr": float(r[2]) if r[2] is not None else None,
                            "ret": float(r[3]) if r[3] is not None else None, "views": r[4]}
    out = []
    for v in vids:
        vid = v["youtube_id"]
        pub = d(v["publicado_em"])
        m = {"fonte": fonte["fonte"], "ini": fonte["ini"], "fim": fonte["fim"]}
        if fonte["fonte"] == "studio" and vid in studio:
            s = studio[vid]
            m.update(imp=s["imp"], ctr=s["ctr"], ret=s["ret"], views=s["views"], ret_fonte="studio")
        else:
            a = api.get(vid, {})
            if fonte["fonte"] == "studio":
                m.update(fonte="reporting_api_parcial", ini=a.get("ini"), fim=a.get("fim"))
            m.update(imp=a.get("imp"), ctr=a.get("ctr"), dias_api=a.get("dias"))
            x = an.get(vid, {})
            m.update(ret=x.get("ret"), views=x.get("views"), ret_fonte="analytics_api")
        dias_no_ar = max(1, (d(m["fim"] or fim) - max(pub, d(m["ini"] or ini))).days + 1) if m.get("imp") is not None else None
        m["dias_no_ar_janela"] = dias_no_ar
        m["imp_dia"] = round(m["imp"] / dias_no_ar, 1) if m.get("imp") and dias_no_ar else None
        m["api_parcial"] = api.get(vid)          # sempre, para comparar
        m["analytics"] = an.get(vid)
        out.append({**v, "idade_dias": (HOJE - pub).days, "metricas": m})
    return out


# ------------------------------------------------------------------ classificação
def classificar(videos_canal):
    """Limiares RELATIVOS ao canal, com piso do nicho:
    ref_ctr / ref_ret = mediana do canal entre vídeos com ≥ MIN_IMP impressões (≥ 3 vídeos; senão 5,0% / 42%).
    alvo_ctr = max(ref_ctr, 4,0%) (piso do nicho documentário 4–8%).
    CTR baixo: < 0,8×ref_ctr OU < 4,0%.  CTR alto/ok: ≥ 0,9×ref_ctr E ≥ 4,0%.
    Retenção alta: ≥ 0,9×ref_ret OU ≥ 50% (topo da faixa do nicho).  Retenção baixa: < 0,85×ref_ret E < 40%.
    Views baixas: impressões/dia no ar < 0,5× a mediana do canal (o YouTube não está testando o vídeo).
    P1 = CTR baixo + retenção alta (trocar embalagem) · P2 = CTR alto + retenção baixa (conteúdo) ·
    P3 = CTR ok + retenção alta + views baixas (tema não fura a bolha) · fraco_nos_dois = CTR baixo + retenção baixa.
    Prioridade P1 = cliques perdidos ≈ impressões × (alvo_ctr − CTR)."""
    ok = [v["metricas"] for v in videos_canal if (v["metricas"].get("imp") or 0) >= MIN_IMP and v["metricas"].get("ctr") is not None]
    ctrs = [m["ctr"] for m in ok]
    rets = [m["ret"] for m in ok if m.get("ret") is not None]
    impd = [m["imp_dia"] for m in ok if m.get("imp_dia")]
    ref = {"n_videos_ref": len(ok),
           "ref_ctr": round(st.median(ctrs), 2) if len(ctrs) >= 3 else REF_CTR_PADRAO,
           "ref_ret": round(st.median(rets), 2) if len(rets) >= 3 else REF_RET_PADRAO,
           "ref_imp_dia": round(st.median(impd), 1) if len(impd) >= 3 else None,
           "ref_origem": "mediana do canal" if len(ctrs) >= 3 else "padrão do nicho (canal com < 3 vídeos com dados)"}
    ref["alvo_ctr"] = max(ref["ref_ctr"], NICHO_CTR[0])
    for v in videos_canal:
        m = v["metricas"]
        imp, ctr, ret = m.get("imp") or 0, m.get("ctr"), m.get("ret")
        c = {"padrao": None, "motivo": ""}
        if v["idade_dias"] < MIN_IDADE:
            c.update(padrao="novo", motivo=f"{v['idade_dias']} d no ar (< {MIN_IDADE})")
        elif imp < MIN_IMP or ctr is None or ret is None:
            c.update(padrao="sem_dados", motivo=f"{imp} impressões (< {MIN_IMP})" if imp < MIN_IMP else "sem CTR ou retenção")
        else:
            ctr_baixo = ctr < 0.8 * ref["ref_ctr"] or ctr < NICHO_CTR[0]
            ctr_ok = ctr >= 0.9 * ref["ref_ctr"] and ctr >= NICHO_CTR[0]
            ret_alta = ret >= 0.9 * ref["ref_ret"] or ret >= NICHO_RET[1]
            ret_baixa = ret < 0.85 * ref["ref_ret"] and ret < 40
            views_baixas = bool(ref["ref_imp_dia"] and m.get("imp_dia") is not None and m["imp_dia"] < 0.5 * ref["ref_imp_dia"])
            txt = f"CTR {ctr:.2f}% (ref {ref['ref_ctr']:.2f}%) · ret {ret:.1f}% (ref {ref['ref_ret']:.1f}%) · {m.get('imp_dia')} impr/dia (ref {ref['ref_imp_dia']})"
            if ctr_baixo and ret_alta:
                c.update(padrao="1-embalagem")
            elif ctr_ok and ret_baixa:
                c.update(padrao="2-conteudo")
            elif ctr_ok and ret_alta and views_baixas:
                c.update(padrao="3-tema")
            elif ctr_baixo and ret_baixa:
                c.update(padrao="fraco_nos_dois")
            else:
                c.update(padrao="ok")
            c["motivo"] = txt
            c["cliques_perdidos"] = round(imp * max(0.0, ref["alvo_ctr"] - ctr) / 100, 1)
        v["classe"] = c
    return ref


# ------------------------------------------------------------------ ciclo de vida
def ultima(con, yid):
    r = con.execute("SELECT * FROM reembalagem WHERE youtube_id=%s ORDER BY sugerido_em DESC, id DESC LIMIT 1", (yid,))
    row = r.fetchone()
    return dict(zip([c.name for c in r.description], row)) if row else None


def n_tentativas(con, yid):
    return con.execute("SELECT count(*) FROM reembalagem WHERE youtube_id=%s AND status <> 'descartado' AND"
                       " status <> 'sugerido'", (yid,)).fetchone()[0]


def janela_api(con, slug, yid, ini, fim):
    r = con.execute("SELECT sum(impressoes), sum(impressoes*ctr), count(DISTINCT data) FROM alcance_diario WHERE canal_slug=%s"
                    " AND video_id=%s AND fonte='channel_reach_basic_a1' AND data BETWEEN %s AND %s", (slug, yid, ini, fim)).fetchone()
    return (int(r[0]), round(float(r[1]) / float(r[0]) * 100, 3), r[2]) if r[0] else (0, None, r[2])


def ciclo_de_vida(con, v, hoje, api_fim, gravar, eventos):
    """Devolve (elegivel: bool, estado: str, tentativa: int). Regras:
    sem histórico → elegível · sugerido < 4 sem → bloqueado (lembrete 1× após 7 d); ≥ 4 sem → só se o CTR cair < 0,7× o de antes
    aplicado → quarentena 21 d; depois mede antes × depois (mesmo nº de dias; API) → melhorou | nao_melhorou
    melhorou → encerrado (volta só se o CTR cair < 0,7× o de depois) · nao_melhorou → 2ª tentativa com padrão diferente
    2ª tentativa sem melhora → embalagem_nao_e_problema (sai para sempre) · > 90 d e < 100 impr/sem → envelhecido."""
    yid, slug, m = v["youtube_id"], v["canal_slug"], v["metricas"]
    u = ultima(con, yid)
    # detecção da troca (título/thumb diferente do registrado na sugestão)
    if u and u["status"] == "sugerido":
        snaps = con.execute("SELECT data, titulo, thumb_sha1 FROM embalagem_snapshot WHERE youtube_id=%s AND data > %s ORDER BY data",
                            (yid, u["sugerido_em"])).fetchall()
        for sd, tit, sha in snaps:
            mt = u["titulo_antes"] and norm(tit) != norm(u["titulo_antes"])
            mh = u["thumb_antes_sha1"] and sha and sha != u["thumb_antes_sha1"]
            if mt or mh:
                por = "titulo+thumb" if mt and mh else ("titulo" if mt else "thumb")
                eventos.append({"youtube_id": yid, "evento": "troca_detectada", "data": str(sd), "por": por, "titulo_novo": tit})
                if gravar:
                    con.execute("UPDATE reembalagem SET status='aplicado', aplicado_em=%s, detectado_por=%s, titulo_depois=%s,"
                                " atualizado_em=now() WHERE id=%s", (sd, por, tit, u["id"]))
                u.update(status="aplicado", aplicado_em=sd, detectado_por=por)
                break
    if u and u["status"] == "aplicado":
        dias = (hoje - d(u["aplicado_em"])).days
        if dias < QUARENTENA:
            return False, f"quarentena até {d(u['aplicado_em']) + dt.timedelta(days=QUARENTENA):%d/%m} (trocado em {d(u['aplicado_em']):%d/%m})", 0
        # medir: mesmo nº de dias antes e depois, até o último dia da API
        n_antes = ((d(u["antes_fim"]) - d(u["antes_inicio"])).days + 1) if u["antes_inicio"] else JANELA
        dep_ini = d(u["aplicado_em"]) + dt.timedelta(days=1)
        dep_fim = min(dep_ini + dt.timedelta(days=n_antes - 1), api_fim) if api_fim else None
        if not dep_fim or dep_fim < dep_ini:
            return False, "aguardando dados da Reporting API para medir", 0
        n = (dep_fim - dep_ini).days + 1
        imp_d, ctr_d, _ = janela_api(con, slug, yid, dep_ini, dep_fim)
        a_ini, a_fim = d(u["aplicado_em"]) - dt.timedelta(days=n), d(u["aplicado_em"]) - dt.timedelta(days=1)
        imp_a, ctr_a, dias_a = janela_api(con, slug, yid, a_ini, a_fim)
        fonte_a = f"reporting_api {a_ini:%d/%m}–{a_fim:%d/%m}"
        if dias_a < n * 0.75 or ctr_a is None:   # API não cobre o antes: usa o que foi gravado na sugestão
            imp_a, ctr_a, fonte_a = u["antes_impressoes"], float(u["antes_ctr"]) if u["antes_ctr"] is not None else None, u["antes_fonte"]
        if imp_d < MIN_IMP and dias < 42:
            return False, f"medindo: {imp_d} impressões em {n} d depois da troca (< {MIN_IMP})", 0
        melhorou = bool(ctr_d is not None and ctr_a is not None and imp_d >= MIN_IMP
                        and ctr_d >= ctr_a * MELHORA_REL and ctr_d - ctr_a >= MELHORA_PP)
        novo = "melhorou" if melhorou else ("embalagem_nao_e_problema" if u["tentativa"] >= 2 else "nao_melhorou")
        eventos.append({"youtube_id": yid, "evento": "medicao", "status": novo, "antes": {"imp": imp_a, "ctr": ctr_a, "fonte": fonte_a},
                        "depois": {"imp": imp_d, "ctr": ctr_d, "ini": str(dep_ini), "fim": str(dep_fim), "dias": n},
                        "aplicado_em": str(u["aplicado_em"]), "tentativa": u["tentativa"]})
        if gravar:
            con.execute("UPDATE reembalagem SET status=%s, depois_inicio=%s, depois_fim=%s, depois_impressoes=%s, depois_ctr=%s,"
                        " depois_retencao=%s, depois_fonte='reporting_api', medido_em=%s, atualizado_em=now() WHERE id=%s",
                        (novo, dep_ini, dep_fim, imp_d, ctr_d, (v.get("metricas") or {}).get("ret"), hoje, u["id"]))
        u.update(status=novo, depois_ctr=ctr_d)
    # envelhecido
    pub = d(v["publicado_em"])
    if (hoje - pub).days > ENVELHECIDO_DIAS:
        imp7, _, _ = janela_api(con, slug, yid, (api_fim or hoje) - dt.timedelta(days=6), api_fim or hoje)
        if imp7 < ENVELHECIDO_IMP_SEM:
            return False, f"envelhecido (> {ENVELHECIDO_DIAS} d e {imp7} impr na última semana)", 0
    if not u:
        return True, "elegível (nunca reembalado)", 1
    ctr = m.get("ctr")
    if u["status"] == "sugerido":
        idade = (hoje - d(u["sugerido_em"])).days
        if idade < SILENCIO_SUGERIDO:
            lembrar = idade >= 7 and not u["lembrete_em"]
            if lembrar and gravar:
                con.execute("UPDATE reembalagem SET lembrete_em=%s WHERE id=%s", (hoje, u["id"]))
            return False, ("LEMBRETE: " if lembrar else "") + f"sugerido em {d(u['sugerido_em']):%d/%m}, não aplicado", 0
        if ctr is not None and u["antes_ctr"] and ctr < QUEDA_FORTE * float(u["antes_ctr"]):
            return True, f"sugerido em {d(u['sugerido_em']):%d/%m} e o CTR caiu forte ({ctr:.2f}% vs {float(u['antes_ctr']):.2f}%)", u["tentativa"]
        return False, f"sugerido em {d(u['sugerido_em']):%d/%m}, não aplicado (silêncio)", 0
    if u["status"] == "melhorou":
        if ctr is not None and u["depois_ctr"] and ctr < QUEDA_FORTE * float(u["depois_ctr"]) and (m.get("imp") or 0) >= MIN_IMP:
            t = n_tentativas(con, yid) + 1
            return (t <= 2), f"melhorou antes, mas o CTR caiu forte ({ctr:.2f}%)", t
        return False, "encerrado: a reembalagem melhorou o CTR", 0
    if u["status"] == "nao_melhorou":
        return True, f"2ª tentativa (a 1ª, padrões '{u['padrao_t1']}' / '{u['padrao_t2']}', não melhorou): usar padrão diferente", 2
    if u["status"] == "embalagem_nao_e_problema":
        return False, "fora da rotina: 2 reembalagens sem melhora (embalagem não é o problema)", 0
    if u["status"] == "aplicado":
        return False, "aplicado (medindo)", 0
    return False, f"status {u['status']}", 0


def achar_pasta(con, v):
    r = con.execute("SELECT id, pasta, titulo FROM videos WHERE youtube_id=%s", (v["youtube_id"],)).fetchone()
    vid, pasta = (r[0], r[1]) if r else (None, None)
    if not pasta:
        try:
            out = subprocess.run(["git", "-C", FABRICA, "grep", "-l", v["youtube_id"], "--", "canais", "pesquisa/canal-clima-2026-11"],
                                 capture_output=True, text=True, timeout=30).stdout.split()
            cands = [re.match(r"(.*/(?:videos/\d{3}[^/]*|longo-\d+))/", p) for p in out]
            pasta = next((c.group(1) for c in cands if c), None)
        except Exception:  # noqa: BLE001
            pasta = None
    srt = None
    if pasta:
        for sub in ("out/legendas.srt", "entrega/legendas.srt", "legendas.srt"):
            if os.path.exists(os.path.join(FABRICA, pasta, sub)):
                srt = os.path.join(pasta, sub)
                break
    return vid, pasta, srt


# ------------------------------------------------------------------ preparar
def placar(con):
    rows = con.execute("SELECT status, count(*) FROM reembalagem GROUP BY 1").fetchall()
    return {s: n for s, n in rows}


def validacao_studio(con, slug, avisos):
    """Compara o export do Studio mais recente com a Analytics API (views, % assistida) e a Reporting API (impressões/CTR) na mesma janela."""
    s = con.execute("SELECT exportado_em, periodo_inicio, periodo_fim FROM studio_video WHERE canal_slug=%s ORDER BY exportado_em DESC LIMIT 1", (slug,)).fetchone()
    if not s:
        return None
    exp, ini, fim = s
    an = analytics_janela(slug, ini, fim, avisos)
    api = alcance_api(con, slug, ini, fim)
    linhas = []
    for yid, imp, ctr, ret, views in con.execute("SELECT youtube_id, impressoes, ctr_pct, pct_visualizada, views FROM studio_video"
                                                 " WHERE canal_slug=%s AND exportado_em=%s AND periodo_fim=%s ORDER BY impressoes DESC NULLS LAST", (slug, exp, fim)):
        a, r = an.get(yid, {}), api.get(yid, {})
        linhas.append({"youtube_id": yid, "studio": {"views": views, "ret": float(ret) if ret is not None else None, "imp": imp,
                                                     "ctr": float(ctr) if ctr is not None else None},
                       "analytics_api": {"views": a.get("views"), "ret": a.get("ret")},
                       "reporting_api": {"imp": r.get("imp"), "ctr": r.get("ctr"), "dias": r.get("dias")}})
    dias = con.execute("SELECT count(DISTINCT data) FROM alcance_diario WHERE canal_slug=%s AND fonte='channel_reach_basic_a1' AND data BETWEEN %s AND %s",
                       (slug, ini, fim)).fetchone()[0]
    return {"exportado_em": str(exp), "ini": str(ini), "fim": str(fim), "dias_reporting_na_janela": dias, "videos": linhas}


def preparar(a):
    global HOJE
    hoje = HOJE = d(a.data) if a.data else dt.date.today()
    gravar = not a.teste
    suf = "-teste" if a.teste else ""
    os.makedirs(os.path.join(SAIDA, "dados"), exist_ok=True)
    avisos, eventos = [], []
    with conectar() as con:
        migrar(con)
        try:
            import reporting
            reporting.criar_jobs(con, verboso=False)
            reporting.baixar(con)
        except Exception as e:  # noqa: BLE001
            avisos.append(f"Reporting API: download falhou ({type(e).__name__}: {str(e)[:120]})")
        canais, todos = {}, []
        for slug in CANAIS:
            if not os.path.exists(os.path.join(TOKENS, f"{slug}.json")):
                avisos.append(f"{slug}: sem token")
                continue
            vids = fotografar(con, slug, hoje, avisos)
            if not vids:
                canais[slug] = {"videos": 0}
                continue
            fonte = escolher_fonte(con, slug, hoje)
            vs = metricas_canal(con, slug, vids, fonte, avisos)
            ref = classificar(vs)
            api_fim = con.execute("SELECT max(data) FROM alcance_diario WHERE canal_slug=%s AND fonte='channel_reach_basic_a1'", (slug,)).fetchone()[0]
            for v in vs:
                el, estado, tent = ciclo_de_vida(con, v, hoje, api_fim, gravar, eventos)
                v["ciclo"] = {"elegivel": el, "estado": estado, "tentativa": tent}
                v["video_id"], v["pasta"], v["legendas"] = achar_pasta(con, v)
                u = ultima(con, v["youtube_id"])
                v["historico"] = None if not u else {k: (str(u[k]) if u[k] is not None else None) for k in
                                                     ("status", "origem", "tentativa", "sugerido_em", "aplicado_em", "t1", "t2", "padrao_t1", "padrao_t2", "thumb_conceito")}
            canais[slug] = {"videos": len(vs), "fonte": fonte, "limiares": ref,
                            "validacao_studio": validacao_studio(con, slug, avisos)}
            todos += vs
        p1 = sorted([v for v in todos if v["classe"]["padrao"] == "1-embalagem" and v["ciclo"]["elegivel"]],
                    key=lambda v: -v["classe"].get("cliques_perdidos", 0))[:MAX_PROPOSTAS]
        simulacao = False
        if a.teste:
            lim = a.limite or 1
            if not p1:
                p1 = sorted([v for v in todos if v["classe"]["padrao"] == "1-embalagem"], key=lambda v: -v["classe"].get("cliques_perdidos", 0))[:lim]
                simulacao = bool(p1)
            p1 = p1[:lim]
        dados = {
            "data": str(hoje), "modo": "teste" if a.teste else "completo", "simulacao": simulacao,
            "limiares": {"min_impressoes": MIN_IMP, "min_idade_dias": MIN_IDADE, "nicho_ctr": NICHO_CTR, "nicho_ret": NICHO_RET,
                         "janela_dias": JANELA, "min_dias_api": MIN_DIAS_API, "quarentena": QUARENTENA, "max_propostas": MAX_PROPOSTAS,
                         "regras": classificar.__doc__, "ciclo": ciclo_de_vida.__doc__},
            "canais": canais,
            "candidatos_p1": [v["youtube_id"] for v in p1],
            "padrao2": [v["youtube_id"] for v in todos if v["classe"]["padrao"] == "2-conteudo"],
            "padrao3": [v["youtube_id"] for v in todos if v["classe"]["padrao"] == "3-tema"],
            "fraco_nos_dois": [v["youtube_id"] for v in todos if v["classe"]["padrao"] == "fraco_nos_dois"],
            "lembretes": [{"youtube_id": v["youtube_id"], "estado": v["ciclo"]["estado"]} for v in todos if v["ciclo"]["estado"].startswith("LEMBRETE")],
            "eventos": eventos, "placar": placar(con), "avisos": avisos,
            "videos": todos,
        }
    base = os.path.join(SAIDA, "dados", f"{hoje}{suf}")
    with open(base + ".json", "w") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=1, default=str)
    with open(base + ".md", "w") as fh:
        fh.write(markdown(dados))
    print(base + ".json")


def pct(x, nd=2):
    return "—" if x is None else f"{x:.{nd}f}%".replace(".", ",")


def markdown(D):
    L = [f"# Dados da reembalagem · {D['data']} ({D['modo']}{', SIMULAÇÃO' if D['simulacao'] else ''})", ""]
    if D["avisos"]:
        L += ["**Avisos:** " + "; ".join(D["avisos"]), ""]
    L += ["## Fonte por canal", "| Canal | Fonte | Janela | Dias da Reporting API | Ref. CTR | Ref. ret. | Ref. impr/dia | Origem da ref. |", "|---|---|---|---|---|---|---|---|"]
    for slug, c in D["canais"].items():
        if not c.get("videos"):
            L.append(f"| {slug} | sem vídeos públicos | | | | | | |")
            continue
        f, r = c["fonte"], c["limiares"]
        nome = {"studio": f"Studio (export {f.get('exportado_em')})", "reporting_api": "Reporting API", "reporting_api_parcial": "Reporting API parcial"}[f["fonte"]]
        L.append(f"| {slug} | {nome} | {f['ini']} → {f['fim']} | {f.get('dias_api', 0)} | {pct(r['ref_ctr'])} | {pct(r['ref_ret'], 1)} | {r['ref_imp_dia'] or '—'} | {r['ref_origem']} |")
    L += ["", "## Vídeos", "| Canal | Vídeo | Título no ar | Idade | Impr. | CTR | Ret. | Impr/dia | Fonte | Padrão | Cliques perdidos | Ciclo |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for v in sorted(D["videos"], key=lambda v: (v["canal_slug"], -(v["metricas"].get("imp") or 0))):
        m, c = v["metricas"], v["classe"]
        L.append(f"| {v['canal_slug']} | [{v['youtube_id']}](https://youtu.be/{v['youtube_id']}) | {v['titulo']} | {v['idade_dias']} d | {m.get('imp') or 0} | {pct(m.get('ctr'))} | "
                 f"{pct(m.get('ret'), 1)} | {m.get('imp_dia') or '—'} | {m['fonte']} | {c['padrao']} | {c.get('cliques_perdidos', '—')} | {v['ciclo']['estado']} |")
    L += ["", f"**Candidatos ao padrão 1 (máx. {MAX_PROPOSTAS}, por cliques perdidos):** " + (", ".join(D["candidatos_p1"]) or "nenhum")]
    L += [f"**Padrão 2:** {', '.join(D['padrao2']) or 'nenhum'} · **Padrão 3:** {', '.join(D['padrao3']) or 'nenhum'} · **Fraco nos dois:** {', '.join(D['fraco_nos_dois']) or 'nenhum'}"]
    L += ["", "## Placar (youtube.reembalagem)", ", ".join(f"{k}: {n}" for k, n in sorted(D["placar"].items())) or "vazio"]
    if D["eventos"]:
        L += ["", "## Eventos desta semana"] + [f"- {json.dumps(e, ensure_ascii=False, default=str)}" for e in D["eventos"]]
    L += ["", "## Validação: Studio × APIs (mesma janela do export)"]
    for slug, c in D["canais"].items():
        vs = (c.get("validacao_studio") or {})
        if not vs:
            continue
        L += [f"### {slug} · Studio {vs['exportado_em']} ({vs['ini']} → {vs['fim']}) · dias da Reporting API na janela: {vs['dias_reporting_na_janela']}",
              "| Vídeo | Views Studio | Views Analytics | Ret. Studio | Ret. Analytics | Impr. Studio | Impr. Reporting | CTR Studio | CTR Reporting |", "|---|---|---|---|---|---|---|---|---|"]
        for x in vs["videos"]:
            s, an, rp = x["studio"], x["analytics_api"], x["reporting_api"]
            L.append(f"| {x['youtube_id']} | {s['views']} | {an['views']} | {pct(s['ret'], 1)} | {pct(an['ret'], 1)} | {s['imp']} | {rp['imp']} ({rp['dias'] or 0} d) | {pct(s['ctr'])} | {pct(rp['ctr'])} |")
    return "\n".join(L) + "\n"


# ------------------------------------------------------------------ registrar / marcar / lote
def registrar(a):
    D = json.load(open(a.json))
    v = next(x for x in D["videos"] if x["youtube_id"] == a.youtube_id)
    m = v["metricas"]
    snap_sha = None
    with conectar() as con:
        migrar(con)
        r = con.execute("SELECT thumb_sha1 FROM embalagem_snapshot WHERE youtube_id=%s ORDER BY data DESC LIMIT 1", (a.youtube_id,)).fetchone()
        snap_sha = r[0] if r else None
        tent = max(1, v["ciclo"].get("tentativa") or 1)
        rid = con.execute(
            "INSERT INTO reembalagem (youtube_id,canal_slug,video_id,tentativa,origem,padrao_lutz,sugerido_em,relatorio,titulo_antes,thumb_antes_sha1,"
            " t1,t2,padrao_t1,padrao_t2,thumb_conceito,porque,crivo,status,antes_inicio,antes_fim,antes_impressoes,antes_ctr,antes_retencao,antes_fonte)"
            " VALUES (%s,%s,%s,%s,'rotina','1-embalagem',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'sugerido',%s,%s,%s,%s,%s,%s) RETURNING id",
            (a.youtube_id, v["canal_slug"], v.get("video_id"), tent, D["data"], a.relatorio, v["titulo"], snap_sha, a.t1, a.t2, a.padrao_t1,
             a.padrao_t2, a.thumb, a.porque, a.crivo, m.get("ini"), m.get("fim"), m.get("imp"), m.get("ctr"), m.get("ret"), m.get("fonte"))).fetchone()[0]
    print(f"registrado id {rid} ({a.youtube_id}, tentativa {tent})")


def marcar(a):
    with conectar() as con:
        migrar(con)
        u = ultima(con, a.youtube_id)
        if not u:
            sys.exit("vídeo sem sugestão registrada")
        con.execute("UPDATE reembalagem SET status='aplicado', aplicado_em=%s::date, detectado_por='manual', notas=concat_ws(' | ', notas, %s::text),"
                    " atualizado_em=now() WHERE id=%s", (a.aplicado, a.notas, u["id"]))
    print(f"id {u['id']} marcado como aplicado em {a.aplicado}")


def semear_lote(a):
    """Os 15 vídeos reembalados em 14/11/2026 (pesquisa/reembalagem-2026-11-14/entrega/TITULOS.md): aplicado em 14/11 via
    'Testar e comparar' (aprovado pelo Rodrigo), quarentena até 05/12; 'antes' = Studio 28 d até 13/11 (export de 14/11)."""
    tab = open(os.path.join(FABRICA, "pesquisa/reembalagem-2026-11-14/entrega/TITULOS.md")).read()
    mapa = {"001-egito": "g847Td0Plsk", "002-india": "MV5SSjoccqE", "003-ira": "GkzMbsB0iH0", "004-china": "-sx6xAkQbA0",
            "005-brasil": "3aA7eUzwfeg", "006-roma": "fkltw3XwQ0E", "007-russia": "3TwMYoxnF4k", "001-cia": "Qs-TusYCr-o",
            "002-mossad": "it37m7pz0hI", "003-fbi": "E1Rgm7jbE0g", "004-cosa-nostra": "gmA0LkJqf_U", "005-kgb": "I_ehrH5Yrak",
            "006-masones": "DBLonwmeQ7c", "el-nino-2026": "FeSLzHvlkbo", "sul-do-brasil": "bG6-E4qjXYc"}
    n = 0
    with conectar() as con:
        migrar(con)
        for linha in tab.splitlines():
            mm = re.match(r"\| (historia-ptbr|dossie-es|em-relevo) (\S+) \| (.+) \| `entrega/(\S+)` \|$", linha)
            if not mm:
                continue
            slug, chave, meio, thumb = mm.groups()
            yid = mapa[chave]
            # T1 e T2: as duas últimas colunas "texto (N)"; o T1 do dossie pode ter " | " dentro
            partes = [p.strip() for p in meio.split(" | ")]
            t2 = re.sub(r"\s*\(\d+\)$", "", partes[-1])
            t1 = re.sub(r"\s*\(\d+\)$", "", " | ".join(partes[:-1]))
            if con.execute("SELECT 1 FROM reembalagem WHERE youtube_id=%s AND origem='reembalagem-2026-11-14'", (yid,)).fetchone():
                continue
            s = con.execute("SELECT impressoes, ctr_pct, pct_visualizada, periodo_inicio, periodo_fim FROM studio_video WHERE youtube_id=%s"
                            " AND exportado_em='2026-11-14' ORDER BY periodo_fim DESC LIMIT 1", (yid,)).fetchone() or (None,) * 5
            vid = con.execute("SELECT id, titulo FROM videos WHERE youtube_id=%s", (yid,)).fetchone()
            tit = (vid[1],) if vid else None   # título original (youtube.videos), antes do lote
            con.execute(
                "INSERT INTO reembalagem (youtube_id,canal_slug,video_id,tentativa,origem,padrao_lutz,sugerido_em,relatorio,titulo_antes,t1,t2,"
                " thumb_conceito,status,aplicado_em,detectado_por,antes_inicio,antes_fim,antes_impressoes,antes_ctr,antes_retencao,antes_fonte,notas)"
                " VALUES (%s,%s,%s,1,'reembalagem-2026-11-14','1-embalagem','2026-11-14','pesquisa/reembalagem-2026-11-14/PROPOSTAS.md',%s,%s,%s,%s,"
                " 'aplicado','2026-11-14','lote',%s,%s,%s,%s,%s,'studio 2026-11-14',%s)",
                (yid, slug, vid[0] if vid else None, tit[0] if tit else None, t1, t2, f"pesquisa/reembalagem-2026-11-14/entrega/{thumb}",
                 s[3], s[4], s[0], s[1], s[2], "lote aprovado pelo Rodrigo em 14/11 (Testar e comparar); quarentena até 05/12"))
            n += 1
    print(f"lote 14/11: {n} vídeos registrados")


def mostrar_placar(a):
    with conectar() as con:
        migrar(con)
        for r in con.execute("SELECT canal_slug, youtube_id, tentativa, origem, status, sugerido_em, aplicado_em, antes_ctr, depois_ctr"
                             " FROM reembalagem ORDER BY canal_slug, sugerido_em"):
            print(r)
        print(placar(con))


def main():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)
    x = sp.add_parser("preparar")
    x.add_argument("--data")
    x.add_argument("--teste", action="store_true")
    x.add_argument("--limite", type=int)
    x = sp.add_parser("registrar")
    for k in ("json", "youtube-id", "t1", "t2", "padrao-t1", "padrao-t2", "thumb", "porque", "crivo", "relatorio"):
        x.add_argument("--" + k, required=k in ("json", "youtube-id", "t1", "t2", "thumb"))
    x = sp.add_parser("marcar")
    x.add_argument("--youtube-id", required=True)
    x.add_argument("--aplicado", required=True)
    x.add_argument("--notas")
    sp.add_parser("semear-lote")
    sp.add_parser("placar")
    a = p.parse_args()
    {"preparar": preparar, "registrar": registrar, "marcar": marcar, "semear-lote": semear_lote, "placar": mostrar_placar}[a.cmd](a)


if __name__ == "__main__":
    main()
