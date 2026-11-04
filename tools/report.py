"""Métricas de um canal: resumo, últimos vídeos e retenção.

Uso:
  ~/workspace/fabrica-youtube/tools/.venv/bin/python ~/workspace/fabrica-youtube/tools/report.py <canal>                 # resumo + últimos 10 vídeos (desde a publicação)
  ~/workspace/fabrica-youtube/tools/.venv/bin/python ~/workspace/fabrica-youtube/tools/report.py <canal> --retencao ID   # curva de retenção de um vídeo
  ~/workspace/fabrica-youtube/tools/.venv/bin/python ~/workspace/fabrica-youtube/tools/report.py --canais                # canais com login feito
  ~/workspace/fabrica-youtube/tools/.venv/bin/python ~/workspace/fabrica-youtube/tools/report.py --coletar               # grava no banco as métricas do dia de todos os canais (usado pelo timer diário)
Obs.: CTR/impressões da thumbnail não existem na API; só no YouTube Studio.
Os dados do Analytics chegam com 1–3 dias de atraso.
"""
import argparse
import datetime as dt
import os
import re
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from _paths import TOKENS
from db import conectar



def creds_for(nome):
    path = os.path.join(TOKENS, f"{nome}.json")
    if not os.path.exists(path):
        sys.exit(f"Sem login para '{nome}'. Rode auth.py {nome} primeiro.")
    creds = Credentials.from_authorized_user_file(path)
    if not creds.valid:
        creds.refresh(Request())
        with open(path, "w") as f:
            f.write(creds.to_json())
    return creds


def dur(iso):
    h, m, s = (int(x) if x else 0 for x in re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso).groups())
    return h * 3600 + m * 60 + s


def mmss(sec):
    sec = int(sec or 0)
    return f"{sec // 60}:{sec % 60:02d}"


def resumo(nome):
    creds = creds_for(nome)
    yt = build("youtube", "v3", credentials=creds)
    ya = build("youtubeAnalytics", "v2", credentials=creds)
    ch = yt.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()["items"][0]
    st = ch["statistics"]
    print(f"# {ch['snippet']['title']}  —  {st.get('subscriberCount', '?')} inscritos · "
          f"{st.get('viewCount')} views · {st.get('videoCount')} vídeos\n")

    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    items = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=10).execute()["items"]
    ids = [i["contentDetails"]["videoId"] for i in items]
    if not ids:
        print("Nenhum vídeo publicado.")
        return
    vids = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids)).execute()["items"]

    hoje = dt.date.today().isoformat()
    inicio = min(v["snippet"]["publishedAt"][:10] for v in vids)
    rep = ya.reports().query(
        ids="channel==MINE", startDate=inicio, endDate=hoje, dimensions="video",
        metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments",
        filters="video==" + ",".join(ids), maxResults=50,
    ).execute()
    cols = [c["name"] for c in rep.get("columnHeaders", [])]
    an = {r[0]: dict(zip(cols, r)) for r in rep.get("rows", [])}

    print(f"{'publicado':<11} {'dur':>6} {'views':>7} {'likes':>6} {'coment':>6} {'méd.assist':>10} {'%assist':>7} {'+insc':>6}  título / id")
    for v in sorted(vids, key=lambda v: v["snippet"]["publishedAt"], reverse=True):
        s, a = v["statistics"], an.get(v["id"], {})
        print(f"{v['snippet']['publishedAt'][:10]:<11} {mmss(dur(v['contentDetails']['duration'])):>6} "
              f"{s.get('viewCount', '0'):>7} {s.get('likeCount', '0'):>6} {s.get('commentCount', '0'):>6} "
              f"{mmss(a.get('averageViewDuration')):>10} {round(a.get('averageViewPercentage') or 0):>6}% "
              f"{a.get('subscribersGained', 0):>6}  {v['snippet']['title']}  [{v['id']}]")
    print("\n(views/likes/comentários: tempo real · assistido/inscritos: Analytics, atraso de 1–3 dias)")


def retencao(nome, video):
    creds = creds_for(nome)
    ya = build("youtubeAnalytics", "v2", credentials=creds)
    yt = build("youtube", "v3", credentials=creds)
    v = yt.videos().list(part="snippet,contentDetails", id=video).execute()["items"][0]
    total = dur(v["contentDetails"]["duration"])
    rep = ya.reports().query(
        ids="channel==MINE", startDate=v["snippet"]["publishedAt"][:10], endDate=dt.date.today().isoformat(),
        dimensions="elapsedVideoTimeRatio", metrics="audienceWatchRatio,relativeRetentionPerformance",
        filters=f"video=={video}",
    ).execute()
    rows = rep.get("rows", [])
    if not rows:
        print("Sem dados de retenção ainda (o Analytics leva 1–3 dias e precisa de algumas views).")
        return
    print(f"# Retenção — {v['snippet']['title']} ({mmss(total)})")
    print(f"{'tempo':>6} {'retidos':>8} {'vs. similares':>13}")
    for ratio, watch, rel in rows[::5]:
        print(f"{mmss(ratio * total):>6} {watch * 100:>7.0f}% {rel:>12.2f}  {'#' * int(min(watch, 1.5) * 40)}")


def coletar():
    """Snapshot diário de todos os canais com login que estão cadastrados em youtube.canais."""
    hoje = dt.date.today()
    with conectar() as con:
        slugs = [r[0] for r in con.execute("SELECT slug FROM canais WHERE status <> 'arquivado'")]
        for slug in slugs:
            if not os.path.exists(os.path.join(TOKENS, f"{slug}.json")):
                print(f"- {slug}: sem login, pulado")
                continue
            creds = creds_for(slug)
            yt = build("youtube", "v3", credentials=creds)
            ya = build("youtubeAnalytics", "v2", credentials=creds)
            ch = yt.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()["items"][0]
            st = ch["statistics"]
            con.execute("UPDATE canais SET channel_id=%s WHERE slug=%s AND channel_id IS NULL", (ch["id"], slug))
            con.execute("INSERT INTO metricas_canal VALUES (%s,%s,%s,%s,%s) ON CONFLICT (channel_id,data) DO UPDATE SET"
                        " inscritos=EXCLUDED.inscritos, views=EXCLUDED.views, videos=EXCLUDED.videos",
                        (ch["id"], hoje, int(st.get("subscriberCount", 0) or 0), int(st["viewCount"]), int(st["videoCount"])))
            up = ch["contentDetails"]["relatedPlaylists"]["uploads"]
            ids = [i["contentDetails"]["videoId"] for i in
                   yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=50).execute()["items"]]
            if not ids:
                continue
            vids = yt.videos().list(part="snippet,statistics", id=",".join(ids)).execute()["items"]
            inicio = min(v["snippet"]["publishedAt"][:10] for v in vids)
            rep = ya.reports().query(ids="channel==MINE", startDate=inicio, endDate=hoje.isoformat(), dimensions="video",
                                     metrics="estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained",
                                     filters="video==" + ",".join(ids), maxResults=200).execute()
            cols = [c["name"] for c in rep.get("columnHeaders", [])]
            an = {r[0]: dict(zip(cols, r)) for r in rep.get("rows", [])}
            for v in vids:
                s, a = v["statistics"], an.get(v["id"], {})
                con.execute(
                    "INSERT INTO metricas_video VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (youtube_id,data) DO UPDATE SET"
                    " views=EXCLUDED.views, likes=EXCLUDED.likes, comentarios=EXCLUDED.comentarios,"
                    " media_assistida_s=EXCLUDED.media_assistida_s, pct_assistido=EXCLUDED.pct_assistido,"
                    " minutos_assistidos=EXCLUDED.minutos_assistidos, inscritos_ganhos=EXCLUDED.inscritos_ganhos",
                    (v["id"], hoje, int(s.get("viewCount", 0)), int(s.get("likeCount", 0)), int(s.get("commentCount", 0)),
                     a.get("averageViewDuration"), a.get("averageViewPercentage"), a.get("estimatedMinutesWatched"),
                     a.get("subscribersGained")))
            print(f"- {slug}: {len(vids)} vídeos gravados ({hoje})")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("canal", nargs="?")
    p.add_argument("--retencao", metavar="VIDEO_ID")
    p.add_argument("--canais", action="store_true")
    p.add_argument("--coletar", action="store_true")
    a = p.parse_args()
    if a.coletar:
        coletar()
        return
    if a.canais or not a.canal:
        print("Canais com login:", ", ".join(f[:-5] for f in sorted(os.listdir(TOKENS)) if f.endswith(".json")) or "nenhum")
        return
    retencao(a.canal, a.retencao) if a.retencao else resumo(a.canal)


if __name__ == "__main__":
    main()
