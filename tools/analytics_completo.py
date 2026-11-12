"""Analytics completo dos canais (YouTube Analytics API v2 + Data API) → youtube.analytics_* e relatório em
~/workspace/relatorios/metricas/AAAA-MM-DD.md. Roda a cada 3 dias (fabrica-analytics.timer).

Uso (a partir de tools/):
  .venv/bin/python analytics_completo.py [--canais historia-ptbr dossie-es em-relevo lotr-fr] [--desde AAAA-MM-DD] [--sem-reporting]
Cota: Analytics API tem cota própria (por projeto, bem acima do uso); Data API ≈ 10 unidades/canal. Nunca imprime token.
"""
import argparse
import datetime as dt
import os
import sys
import unicodedata

from googleapiclient.discovery import build

from _paths import TOOLS, TOKENS
from db import conectar
from report import creds_for

PADRAO = ["historia-ptbr", "dossie-es", "em-relevo", "lotr-fr"]
REL = os.path.expanduser("~/workspace/relatorios/metricas")
VID_METRICAS = ["views", "engagedViews", "estimatedMinutesWatched", "averageViewDuration", "averageViewPercentage",
                "subscribersGained", "subscribersLost", "likes", "dislikes", "comments", "shares",
                "videosAddedToPlaylists", "cardClicks", "cardImpressions", "cardClickRate"]
COL = ["views", "engaged_views", "minutos", "duracao_media_s", "pct_media", "inscritos_ganhos", "inscritos_perdidos",
       "likes", "dislikes", "comentarios", "compartilhamentos", "adicionados_playlist", "card_cliques", "card_impressoes", "card_ctr"]


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if c.isalnum())


def q(ya, **kw):
    """Consulta Analytics; devolve (cabeçalhos, linhas) ou None se a API recusar (erro registrado, sem parar)."""
    try:
        r = ya.reports().query(ids="channel==MINE", **kw).execute()
        return [c["name"] for c in r.get("columnHeaders", [])], r.get("rows", [])
    except Exception as e:  # noqa: BLE001
        msg = str(e).replace("\n", " ")[:160]
        print(f"   [aviso] {kw.get('dimensions','')}/{kw.get('metrics','')[:40]}: {msg}", file=sys.stderr)
        return None


def sincronizar_videos(con, slug, yt):
    """Data API: grava channel_id e youtube_id que faltam (sem apagar nada). Devolve {video_id: (titulo, publicado)}."""
    ch = yt.channels().list(part="id,contentDetails", mine=True).execute()["items"][0]
    con.execute("UPDATE canais SET channel_id=%s WHERE slug=%s AND channel_id IS NULL", (ch["id"], slug))
    up = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, tok = [], None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=50, pageToken=tok).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        tok = r.get("nextPageToken")
        if not tok:
            break
    info = {}
    for i in range(0, len(ids), 50):
        for v in yt.videos().list(part="snippet,contentDetails", id=",".join(ids[i:i + 50])).execute()["items"]:
            info[v["id"]] = (v["snippet"]["title"], v["snippet"]["publishedAt"][:10])
    sem_id = {r[0]: norm(r[1]) for r in con.execute("SELECT id,titulo FROM videos WHERE canal_slug=%s AND youtube_id IS NULL", (slug,))}
    for vid, (titulo, pub) in info.items():
        if con.execute("SELECT 1 FROM videos WHERE youtube_id=%s", (vid,)).fetchone():
            continue
        n = norm(titulo)
        alvo = next((i for i, t in sem_id.items() if t == n or t[:30] == n[:30]), None)
        if alvo:
            con.execute("UPDATE videos SET youtube_id=%s, publicado_em=%s, status='publicado', atualizado_em=now() WHERE id=%s", (vid, pub, alvo))
            sem_id.pop(alvo)
            print(f"   youtube_id gravado em videos.id={alvo} ({titulo[:50]})")
        else:
            con.execute("INSERT INTO videos (canal_slug,titulo,status,youtube_id,publicado_em) VALUES (%s,%s,'publicado',%s,%s)", (slug, titulo, vid, pub))
            print(f"   vídeo novo no banco: {titulo[:50]}")
    return info


def f(x, t=float):
    return None if x is None else t(x)


def coletar_video(con, ya, slug, vid, ini, fim):
    # por dia (tenta o conjunto completo; se a API recusar, tira métricas opcionais)
    mets = list(VID_METRICAS)
    res = None
    for tentativa in range(4):
        res = q(ya, startDate=ini, endDate=fim, dimensions="day", metrics=",".join(mets), filters=f"video=={vid}", sort="day")
        if res:
            break
        mets = [m for m in mets if not m.startswith("card") and m != "engagedViews"] if tentativa == 0 else \
               [m for m in mets if m not in ("dislikes", "videosAddedToPlaylists")] if tentativa == 1 else ["views", "estimatedMinutesWatched", "averageViewDuration", "averageViewPercentage"]
    n = 0
    if res:
        hd, rows = res
        for r in rows:
            d = dict(zip(hd, r))
            vals = [f(d.get(m)) for m in VID_METRICAS]
            con.execute(
                "INSERT INTO analytics_video_dia (canal_slug,video_id,data," + ",".join(COL) + ") VALUES (%s,%s,%s," + ",".join(["%s"] * len(COL)) + ")"
                " ON CONFLICT (video_id,data) DO UPDATE SET " + ",".join(f"{c}=EXCLUDED.{c}" for c in COL) + ",atualizado_em=now()",
                (slug, vid, d["day"], *vals))
            n += 1
    # retenção
    res = q(ya, startDate=ini, endDate=fim, dimensions="elapsedVideoTimeRatio", metrics="audienceWatchRatio,relativeRetentionPerformance", filters=f"video=={vid}")
    if res:
        for r in res[1]:
            con.execute("INSERT INTO analytics_retencao (canal_slug,video_id,ratio,audiencia_ratio,retencao_relativa) VALUES (%s,%s,%s,%s,%s)"
                        " ON CONFLICT (video_id,ratio) DO UPDATE SET audiencia_ratio=EXCLUDED.audiencia_ratio, retencao_relativa=EXCLUDED.retencao_relativa, atualizado_em=now()",
                        (slug, vid, r[0], r[1], r[2]))
    # tráfego por dia
    res = q(ya, startDate=ini, endDate=fim, dimensions="day,insightTrafficSourceType", metrics="views,estimatedMinutesWatched", filters=f"video=={vid}")
    if res:
        for r in res[1]:
            con.execute("INSERT INTO analytics_trafego (canal_slug,video_id,data,origem,views,minutos) VALUES (%s,%s,%s,%s,%s,%s)"
                        " ON CONFLICT (video_id,data,origem) DO UPDATE SET views=EXCLUDED.views, minutos=EXCLUDED.minutos, atualizado_em=now()",
                        (slug, vid, r[0], r[1], r[2], r[3]))
    # detalhe de tráfego
    for tipo in ("RELATED_VIDEO", "YT_SEARCH", "EXT_URL", "PLAYLIST", "YT_CHANNEL", "NOTIFICATION", "SHORTS", "HASHTAGS"):
        res = q(ya, startDate=ini, endDate=fim, dimensions="insightTrafficSourceDetail", metrics="views,estimatedMinutesWatched",
                filters=f"video=={vid};insightTrafficSourceType=={tipo}", sort="-views", maxResults=25)
        if res:
            for r in res[1]:
                con.execute("INSERT INTO analytics_trafego_detalhe (canal_slug,video_id,tipo,detalhe,views,minutos) VALUES (%s,%s,%s,%s,%s,%s)"
                            " ON CONFLICT (video_id,tipo,detalhe) DO UPDATE SET views=EXCLUDED.views, minutos=EXCLUDED.minutos, atualizado_em=now()",
                            (slug, vid, tipo, r[0], r[1], r[2]))
    # público (acumulado) do vídeo
    publico(con, ya, slug, vid, ini, fim, f"video=={vid}")
    return n


DIMS_PUBLICO = [("ageGroup,gender", "ageGroup_gender", "viewerPercentage"), ("country", "country", "views,estimatedMinutesWatched"),
                ("city", "city", "views,estimatedMinutesWatched"), ("deviceType", "deviceType", "views,estimatedMinutesWatched"),
                ("operatingSystem", "operatingSystem", "views,estimatedMinutesWatched"),
                ("playbackLocationType", "playbackLocationType", "views,estimatedMinutesWatched"),
                ("subscribedStatus", "subscribedStatus", "views,estimatedMinutesWatched"),
                ("creatorContentType", "creatorContentType", "views,estimatedMinutesWatched")]


def publico(con, ya, slug, vid, ini, fim, filtro):
    for dims, nome, mets in DIMS_PUBLICO:
        kw = dict(startDate=ini, endDate=fim, dimensions=dims, metrics=mets)
        if filtro:
            kw["filters"] = filtro
        if "city" in dims or "country" in dims:
            kw.update(sort="-views", maxResults=25)
        res = q(ya, **kw)
        if not res:
            continue
        hd, rows = res
        for r in rows:
            nd = dims.count(",") + 1
            chave = "|".join(str(x) for x in r[:nd])
            d = dict(zip(hd[nd:], r[nd:]))
            con.execute("INSERT INTO analytics_publico (canal_slug,video_id,dimensao,chave,views,minutos,viewer_pct) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                        " ON CONFLICT (canal_slug,video_id,dimensao,chave) DO UPDATE SET views=EXCLUDED.views, minutos=EXCLUDED.minutos, viewer_pct=EXCLUDED.viewer_pct, atualizado_em=now()",
                        (slug, vid or "", nome, chave, f(d.get("views"), int), f(d.get("estimatedMinutesWatched")), f(d.get("viewerPercentage"))))


def resolver_relacionados(con, yt, slug):
    """Título/canal dos vídeos que nos sugerem (Data API, 1 unidade por 50)."""
    ids = [r[0] for r in con.execute("SELECT DISTINCT detalhe FROM analytics_trafego_detalhe WHERE canal_slug=%s AND tipo='RELATED_VIDEO' AND detalhe_titulo IS NULL", (slug,))]
    for i in range(0, len(ids), 50):
        try:
            for v in yt.videos().list(part="snippet", id=",".join(ids[i:i + 50])).execute()["items"]:
                con.execute("UPDATE analytics_trafego_detalhe SET detalhe_titulo=%s, detalhe_canal=%s WHERE tipo='RELATED_VIDEO' AND detalhe=%s",
                            (v["snippet"]["title"], v["snippet"]["channelTitle"], v["id"]))
        except Exception as e:  # noqa: BLE001
            print(f"   [aviso] resolver relacionados: {str(e)[:120]}", file=sys.stderr)


def receita(con, ya, slug, ini, fim):
    res = q(ya, startDate=ini, endDate=fim, dimensions="day", metrics="estimatedRevenue,cpm")
    if not res:
        return False
    for r in res[1]:
        con.execute("INSERT INTO analytics_receita (canal_slug,data,receita_usd,cpm_usd) VALUES (%s,%s,%s,%s)"
                    " ON CONFLICT (canal_slug,data) DO UPDATE SET receita_usd=EXCLUDED.receita_usd, cpm_usd=EXCLUDED.cpm_usd, atualizado_em=now()", (slug, *r))
    return True


def processar(con, slug, desde):
    creds = creds_for(slug)
    yt = build("youtube", "v3", credentials=creds)
    ya = build("youtubeAnalytics", "v2", credentials=creds)
    info = sincronizar_videos(con, slug, yt)
    if not info:
        return None
    ini = desde or min(p for _, p in info.values())
    fim = dt.date.today().isoformat()
    print(f"== {slug}: {len(info)} vídeos, {ini} → {fim}")
    for vid in info:
        n = coletar_video(con, ya, slug, vid, ini, fim)
        print(f"   {vid}: {n} dias")
    publico(con, ya, slug, "", ini, fim, None)
    resolver_relacionados(con, yt, slug)
    tem_receita = receita(con, ya, slug, ini, fim)
    tot = con.execute("SELECT coalesce(sum(views),0), coalesce(sum(minutos),0), coalesce(sum(inscritos_ganhos-inscritos_perdidos),0), count(DISTINCT video_id)"
                      " FROM analytics_video_dia WHERE canal_slug=%s", (slug,)).fetchone()
    return dict(ini=ini, fim=fim, tot=tot, receita=tem_receita, info=info)


def secao(con, slug, nome, meta, anterior):
    L = [f"## {nome} (`{slug}`)"]
    views, minutos, subs, nv = meta["tot"]
    L.append(f"- Acumulado desde {meta['ini']}: **{views} views**, {float(minutos)/60:.1f} h assistidas, {subs:+d} inscritos líquidos, {nv} vídeos com dados.")
    if anterior:
        L.append(f"- Desde a última rodada: {views - anterior[0]:+d} views, {float(minutos - anterior[1])/60:+.1f} h, {subs - anterior[2]:+d} inscritos.")
    else:
        L.append("- Primeira rodada: sem comparação.")
    r = con.execute("SELECT sum(pct_media*views)/nullif(sum(views),0), sum(duracao_media_s*views)/nullif(sum(views),0) FROM analytics_video_dia WHERE canal_slug=%s", (slug,)).fetchone()
    if r[0] is not None:
        L.append(f"- Retenção média (ponderada por views): {float(r[0]):.1f}% do vídeo, {float(r[1])/60:.1f} min por view.")
    L.append("- Por vídeo (views | ret.% | inscr. | likes):")
    for t, v, p, s, lk in con.execute(
            "SELECT coalesce(vi.titulo,a.video_id), sum(a.views), sum(a.pct_media*a.views)/nullif(sum(a.views),0), sum(a.inscritos_ganhos-a.inscritos_perdidos), sum(a.likes)"
            " FROM analytics_video_dia a LEFT JOIN videos vi ON vi.youtube_id=a.video_id WHERE a.canal_slug=%s GROUP BY 1 ORDER BY 2 DESC", (slug,)):
        L.append(f"  - {t[:55]}: {v} | {float(p or 0):.1f}% | {s} | {lk}")
    org = con.execute("SELECT origem, sum(views) FROM analytics_trafego WHERE canal_slug=%s GROUP BY 1 ORDER BY 2 DESC LIMIT 6", (slug,)).fetchall()
    tv = sum(o[1] for o in org) or 1
    if org:
        L.append("- Origem de tráfego: " + "; ".join(f"{o} {v} ({100*v/tv:.0f}%)" for o, v in org))
    rel = con.execute("SELECT coalesce(detalhe_titulo,detalhe), coalesce(detalhe_canal,'?'), sum(views) FROM analytics_trafego_detalhe WHERE canal_slug=%s AND tipo='RELATED_VIDEO' GROUP BY 1,2 ORDER BY 3 DESC LIMIT 3", (slug,)).fetchall()
    L.append("- Top 3 vídeos que nos sugerem: " + ("; ".join(f"“{t[:50]}” ({c}) {v}" for t, c, v in rel) if rel else "nenhum ainda"))
    bus = con.execute("SELECT detalhe, sum(views) FROM analytics_trafego_detalhe WHERE canal_slug=%s AND tipo='YT_SEARCH' GROUP BY 1 ORDER BY 2 DESC LIMIT 5", (slug,)).fetchall()
    L.append("- Top termos de busca: " + ("; ".join(f"{t} ({v})" for t, v in bus) if bus else "nenhum ainda"))
    pa = con.execute("SELECT chave, views FROM analytics_publico WHERE canal_slug=%s AND video_id='' AND dimensao='country' ORDER BY views DESC NULLS LAST LIMIT 3", (slug,)).fetchall()
    if pa:
        L.append("- Países: " + "; ".join(f"{c} {v}" for c, v in pa))
    idade = con.execute("SELECT chave, viewer_pct FROM analytics_publico WHERE canal_slug=%s AND video_id='' AND dimensao='ageGroup_gender' ORDER BY viewer_pct DESC NULLS LAST LIMIT 3", (slug,)).fetchall()
    if idade:
        L.append("- Público (idade|gênero): " + "; ".join(f"{c} {float(p):.0f}%" for c, p in idade))
    al = con.execute("SELECT sum(impressoes), sum(impressoes*ctr)/nullif(sum(impressoes),0), max(data) FROM alcance_diario WHERE canal_slug=%s AND fonte LIKE 'channel_reach%%' AND impressoes IS NOT NULL", (slug,)).fetchone()
    L.append(f"- Impressões/CTR (Reporting API): {al[0]} impressões, CTR {100*float(al[1]):.2f}% (até {al[2]})" if al[0] else "- Impressões/CTR: ainda sem relatório da Reporting API (os primeiros saem 12–13/11/2026).")
    L.append(f"- Receita: {'consultada (ver youtube.analytics_receita)' if meta['receita'] else 'indisponível (canal não monetizado ou sem escopo)'}.")
    return "\n".join(L)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--canais", nargs="*", default=PADRAO)
    p.add_argument("--desde")
    p.add_argument("--sem-reporting", action="store_true")
    a = p.parse_args()
    with conectar() as con:
        con.execute(open(os.path.join(TOOLS, "db", "schema_analytics.sql")).read())
        con.execute(open(os.path.join(TOOLS, "db", "schema_alcance.sql")).read())
        if not a.sem_reporting:
            try:
                import reporting
                reporting.baixar(con)
            except Exception as e:  # noqa: BLE001
                print(f"[aviso] Reporting API: {str(e)[:200]}", file=sys.stderr)
        secoes = []
        for slug in a.canais:
            if not os.path.exists(os.path.join(TOKENS, f"{slug}.json")):
                print(f"== {slug}: sem token, pulando")
                continue
            try:
                ant = con.execute("SELECT views,minutos,inscritos_liquidos FROM analytics_rodadas WHERE canal_slug=%s ORDER BY rodada DESC LIMIT 1", (slug,)).fetchone()
                meta = processar(con, slug, a.desde)
                if not meta:
                    continue
                nome = con.execute("SELECT nome FROM canais WHERE slug=%s", (slug,)).fetchone()[0]
                secoes.append(secao(con, slug, nome, meta, ant))
                v, m, s, n = meta["tot"]
                con.execute("INSERT INTO analytics_rodadas (canal_slug,views,minutos,inscritos_liquidos,videos) VALUES (%s,%s,%s,%s,%s)", (slug, v, m, s, n))
            except Exception as e:  # noqa: BLE001
                print(f"== {slug}: ERRO {type(e).__name__}: {str(e)[:200]}", file=sys.stderr)
                secoes.append(f"## {slug}\n- ERRO nesta rodada: {type(e).__name__}")
    os.makedirs(REL, exist_ok=True)
    hoje = dt.date.today().isoformat()
    path = os.path.join(REL, f"{hoje}.md")
    with open(path, "w") as fh:
        fh.write(f"# Métricas completas — {hoje}\n\nFonte: YouTube Analytics API v2 + Reporting API (impressões/CTR, 1–2 dias de atraso). Dados em `youtube.analytics_*` e `youtube.alcance_diario`.\n\n" + "\n\n".join(secoes) + "\n")
    print("relatório:", path)


if __name__ == "__main__":
    main()
