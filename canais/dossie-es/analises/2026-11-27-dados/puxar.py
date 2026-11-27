"""Diagnóstico Dossier 27/11/2026: puxa Analytics API (readonly) por vídeo e grava dados.json ao lado.
Rodar de tools/: .venv/bin/python ../canais/dossie-es/analises/2026-11-27-dados/puxar.py
"""
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from googleapiclient.discovery import build  # noqa: E402
from report import creds_for  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados.json")
HOJE = dt.date.today().isoformat()
c = creds_for("dossie-es")
yt = build("youtube", "v3", credentials=c, cache_discovery=False)
ya = build("youtubeAnalytics", "v2", credentials=c, cache_discovery=False)


def q(**kw):
    try:
        r = ya.reports().query(ids="channel==MINE", **kw).execute()
        return {"cols": [h["name"] for h in r.get("columnHeaders", [])], "rows": r.get("rows", [])}
    except Exception as e:  # noqa: BLE001
        print("aviso", kw.get("dimensions"), str(e)[:200], file=sys.stderr)
        return None


ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
up = ch["contentDetails"]["relatedPlaylists"]["uploads"]
ids, tok = [], None
while True:
    r = yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=50, pageToken=tok).execute()
    ids += [i["contentDetails"]["videoId"] for i in r["items"]]
    tok = r.get("nextPageToken")
    if not tok:
        break
vids = {}
for v in yt.videos().list(part="snippet,contentDetails,status,statistics", id=",".join(ids)).execute()["items"]:
    vids[v["id"]] = {"titulo": v["snippet"]["title"], "publicado": v["snippet"]["publishedAt"],
                     "status": v["status"]["privacyStatus"], "duracao": v["contentDetails"]["duration"],
                     "views_contador": v["statistics"].get("viewCount")}

dados = {"lido_em": dt.datetime.now().isoformat(), "videos": vids, "canal": {}}
ini = "2026-11-01"
dados["canal"]["dia"] = q(startDate=ini, endDate=HOJE, dimensions="day", metrics="views,estimatedMinutesWatched,subscribersGained", sort="day")
dados["canal"]["dia_video"] = q(startDate=ini, endDate=HOJE, dimensions="day,video", metrics="views", sort="day", maxResults=200)
dados["canal"]["dia_inscrito"] = q(startDate=ini, endDate=HOJE, dimensions="day,subscribedStatus", metrics="views", sort="day")
for vid, info in vids.items():
    if info["status"] != "public":
        continue
    pub = info["publicado"][:10]
    d = info.setdefault("an", {})
    f = f"video=={vid}"
    d["dia"] = q(startDate=pub, endDate=HOJE, dimensions="day", metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained", filters=f, sort="day")
    d["trafego_dia"] = q(startDate=pub, endDate=HOJE, dimensions="day,insightTrafficSourceType", metrics="views,estimatedMinutesWatched", filters=f, sort="day")
    d["inscrito"] = q(startDate=pub, endDate=HOJE, dimensions="subscribedStatus", metrics="views,averageViewPercentage,averageViewDuration", filters=f)
    d["retencao"] = q(startDate=pub, endDate=HOJE, dimensions="elapsedVideoTimeRatio", metrics="audienceWatchRatio,relativeRetentionPerformance", filters=f)
    d["retencao_organico"] = q(startDate=pub, endDate=HOJE, dimensions="elapsedVideoTimeRatio", metrics="audienceWatchRatio", filters=f + ";audienceType==ORGANIC")
    fim7 = min(HOJE, (dt.date.fromisoformat(pub) + dt.timedelta(days=6)).isoformat())
    for nome, fim in (("tudo", HOJE), ("7d", fim7)):
        d[f"sugerido_{nome}"] = q(startDate=pub, endDate=fim, dimensions="insightTrafficSourceDetail", metrics="views,estimatedMinutesWatched",
                                  filters=f + ";insightTrafficSourceType==RELATED_VIDEO", sort="-views", maxResults=25)
    d["busca"] = q(startDate=pub, endDate=HOJE, dimensions="insightTrafficSourceDetail", metrics="views", filters=f + ";insightTrafficSourceType==YT_SEARCH", sort="-views", maxResults=15)
    d["pais"] = q(startDate=pub, endDate=HOJE, dimensions="country", metrics="views,averageViewPercentage", filters=f, sort="-views", maxResults=10)
    d["idade"] = q(startDate=pub, endDate=HOJE, dimensions="ageGroup,gender", metrics="viewerPercentage", filters=f)
    print("ok", vid, info["titulo"][:40], file=sys.stderr)
json.dump(dados, open(OUT, "w"), ensure_ascii=False, indent=1)
print(OUT)
