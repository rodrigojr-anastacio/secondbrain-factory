"""videos.list (1 unidade por 50 ids) para todos os vídeos da busca: título ORIGINAL, data, idioma do áudio, views, duração.
Saída: dados/videos_api.json"""
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, segundos, chunks
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ids = sorted({json.loads(l)["id"] for l in open(os.path.join(BASE, "dados/busca.jsonl")) if json.loads(l).get("id")})
yt = yt_client(); un = 0; out = {}
for g in chunks(ids):
    r = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(g), maxResults=50).execute(); un += 1
    for it in r.get("items", []):
        sn, st = it["snippet"], it.get("statistics", {})
        d = it["contentDetails"].get("duration")
        out[it["id"]] = {"titulo": sn["title"], "canal": sn["channelTitle"], "channel_id": sn["channelId"], "pub": sn["publishedAt"][:10],
                         "audio": sn.get("defaultAudioLanguage"), "lang": sn.get("defaultLanguage"), "views": int(st.get("viewCount", 0)),
                         "dur_s": segundos(d) if d else 0, "live": sn.get("liveBroadcastContent")}
json.dump(out, open(os.path.join(BASE, "dados/videos_api.json"), "w"), ensure_ascii=False)
print("ids:", len(ids), "ok:", len(out), "unidades:", un, file=sys.stderr)
