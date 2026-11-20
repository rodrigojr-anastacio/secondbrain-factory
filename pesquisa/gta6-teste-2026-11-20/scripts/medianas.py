"""Etapa 3: mediana de views dos últimos 50 uploads longos (> 180 s, idade ≥ 3 d) de cada canal relevante.
playlistItems (1 un.) + videos.list (1 un.) por canal. Incremental: dados/medianas.json."""
import json, os, sys, datetime as dt, statistics
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, segundos

D = os.path.join(os.path.dirname(__file__), "..", "dados")
NOW = dt.datetime(2026, 11, 20, 15, tzinfo=dt.timezone.utc)
v = json.load(open(os.path.join(D, "videos.json"))); c = json.load(open(os.path.join(D, "canais.json")))
def age(p): return (NOW - dt.datetime.fromisoformat(p.replace("Z", "+00:00"))).total_seconds() / 86400
alvo = {x["canal_id"] for x in v.values() if age(x["publicado"]) <= 45 and "gta" in x["titulo"].lower()}
alvo |= {x["canal_id"] for x in v.values() if "gta5" in x["grupos"]}
path = os.path.join(D, "medianas.json")
med = json.load(open(path)) if os.path.exists(path) else {}
yt = yt_client(); units = 0
for i, cid in enumerate(sorted(alvo)):
    if cid in med or cid not in c: continue
    try:
        pl = yt.playlistItems().list(part="contentDetails", playlistId=c[cid]["uploads"], maxResults=50).execute(); units += 1
        ids = [it["contentDetails"]["videoId"] for it in pl.get("items", [])]
        if not ids: med[cid] = None; continue
        res = yt.videos().list(part="statistics,contentDetails,snippet", id=",".join(ids)).execute(); units += 1
        longos = [int(x["statistics"].get("viewCount", 0)) for x in res["items"]
                  if segundos(x["contentDetails"].get("duration") or "PT0S") > 180 and age(x["snippet"]["publishedAt"]) >= 3]
        todos = [int(x["statistics"].get("viewCount", 0)) for x in res["items"] if age(x["snippet"]["publishedAt"]) >= 3]
        med[cid] = {"mediana_longos": statistics.median(longos) if longos else None, "n_longos": len(longos),
                    "mediana_todos": statistics.median(todos) if todos else None, "n": len(todos)}
    except Exception as ex:
        print("ERRO", cid, ex, file=sys.stderr); med[cid] = None
    if i % 50 == 0:
        json.dump(med, open(path, "w")); print(i, len(alvo), units, flush=True)
json.dump(med, open(path, "w"))
print("fim", len(med), "unidades", units)
