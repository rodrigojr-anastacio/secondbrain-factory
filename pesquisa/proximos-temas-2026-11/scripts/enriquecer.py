"""videos.list + channels.list (1 unidade por 50 ids). Saída: dados/videos_api.json, dados/canais_api.json"""
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, segundos, chunks
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ids = sorted({json.loads(l)["id"] for l in open(os.path.join(BASE, "dados/busca.jsonl")) if json.loads(l).get("id")})
yt = yt_client(); un = 0; out = {}
for g in chunks(ids):
    r = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(g), maxResults=50).execute(); un += 1
    for it in r.get("items", []):
        sn, st = it["snippet"], it.get("statistics", {}); d = it["contentDetails"].get("duration")
        out[it["id"]] = {"titulo": sn["title"], "canal": sn["channelTitle"], "channel_id": sn["channelId"], "pub": sn["publishedAt"][:10],
                         "audio": sn.get("defaultAudioLanguage"), "lang": sn.get("defaultLanguage"), "views": int(st.get("viewCount", 0)),
                         "dur_s": segundos(d) if d else 0, "live": sn.get("liveBroadcastContent")}
json.dump(out, open(os.path.join(BASE, "dados/videos_api.json"), "w"), ensure_ascii=False)
chs = sorted({v["channel_id"] for v in out.values()}); cout = {}
for g in chunks(chs):
    r = yt.channels().list(part="snippet,statistics", id=",".join(g), maxResults=50).execute(); un += 1
    for it in r.get("items", []):
        cout[it["id"]] = {"titulo": it["snippet"]["title"], "criado": it["snippet"]["publishedAt"][:10], "pais": it["snippet"].get("country"),
                          "insc": int(it["statistics"].get("subscriberCount", 0)), "videos": int(it["statistics"].get("videoCount", 0)), "views": int(it["statistics"].get("viewCount", 0))}
json.dump(cout, open(os.path.join(BASE, "dados/canais_api.json"), "w"), ensure_ascii=False)
print("videos", len(ids), len(out), "canais", len(chs), len(cout), "unidades", un, file=sys.stderr)
