"""videos.list (1 un/50 ids) para todos os vídeos das buscas. Saída: dados/videos_api.json (cache incremental). Imprime unidades gastas."""
import json, os, sys, glob
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, segundos, chunks
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fn = os.path.join(BASE, "dados/videos_api.json")
out = json.load(open(fn)) if os.path.exists(fn) else {}
ids = set()
for f in glob.glob(os.path.join(BASE, "dados/busca_*.jsonl")):
    for l in open(f):
        b = json.loads(l)
        if b.get("id"): ids.add(b["id"])
ids = sorted(ids - set(out)); yt = yt_client(); un = 0
for g in chunks(ids):
    r = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(g), maxResults=50).execute(); un += 1
    for it in r.get("items", []):
        sn, st = it["snippet"], it.get("statistics", {}); d = it["contentDetails"].get("duration")
        out[it["id"]] = {"titulo": sn["title"], "canal": sn["channelTitle"], "channel_id": sn["channelId"], "pub": sn["publishedAt"][:10], "audio": sn.get("defaultAudioLanguage"),
                         "lang": sn.get("defaultLanguage"), "views": int(st.get("viewCount", 0)), "dur_s": segundos(d) if d and "D" not in d else 0, "live": sn.get("liveBroadcastContent")}
json.dump(out, open(fn, "w"), ensure_ascii=False)
print("novos ids:", len(ids), "total:", len(out), "unidades:", un, file=sys.stderr)
