"""channels.list para todos os canais das buscas conc + idi (1 un/50). Saída: dados/canais_lista.json (cache incremental)."""
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, chunks
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = json.load(open(os.path.join(BASE, "dados/videos_api.json")))
fn = os.path.join(BASE, "dados/canais_lista.json"); out = json.load(open(fn)) if os.path.exists(fn) else {}
ids = set()
for g in ("conc", "idi", "dem"):
    for l in open(os.path.join(BASE, f"dados/busca_{g}.jsonl")):
        b = json.loads(l)
        if b.get("id") in V: ids.add(V[b["id"]]["channel_id"])
ids = sorted(ids - set(out)); yt = yt_client(); un = 0
for g in chunks(ids):
    for it in yt.channels().list(part="snippet,statistics,contentDetails", id=",".join(g), maxResults=50).execute().get("items", []):
        sn, st = it["snippet"], it["statistics"]
        out[it["id"]] = {"id": it["id"], "nome": sn["title"], "handle": sn.get("customUrl"), "criado": sn["publishedAt"][:10], "pais": sn.get("country"), "views": int(st.get("viewCount", 0)),
                         "inscritos": int(st.get("subscriberCount", 0)) if not st.get("hiddenSubscriberCount") else None, "n_videos": int(st.get("videoCount", 0)), "uploads": it["contentDetails"]["relatedPlaylists"]["uploads"]}
    un += 1
json.dump(out, open(fn, "w"), ensure_ascii=False)
print("canais:", len(out), "unidades:", un, file=sys.stderr)
