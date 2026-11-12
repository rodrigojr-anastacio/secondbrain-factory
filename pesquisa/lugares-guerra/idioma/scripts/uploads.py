"""Uploads recentes (até MAX_PAGES x 50) de canais candidatos + videos.list. Saída: dados/uploads.json (cache incremental). Uso: uploads.py <lista.json chave...>"""
import json, os, sys, time
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, segundos, chunks
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAXP = int(os.environ.get("MAX_PAGES", "2")); LIM = int(os.environ.get("LIMITE_S", "500"))
C = json.load(open(os.path.join(BASE, "dados/canais_lista.json")))
cand = json.load(open(os.path.join(BASE, "dados/cand_conc.json")))
ids = []
for k in sys.argv[1:]: ids += cand[k]
fn = os.path.join(BASE, "dados/uploads.json"); out = json.load(open(fn)) if os.path.exists(fn) else {}
yt = yt_client(); un = 0; t0 = time.time()
for cid in ids:
    if cid in out or cid not in C: continue
    if time.time() - t0 > LIM: break
    up = C[cid]["uploads"]; vi, tok, p = [], None, 0
    while p < MAXP:
        try: r = yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=50, pageToken=tok).execute()
        except Exception as e: print("erro", C[cid]["nome"], str(e)[:60], file=sys.stderr); break
        un += 1; p += 1; vi += [i["contentDetails"]["videoId"] for i in r.get("items", [])]; tok = r.get("nextPageToken")
        if not tok: break
    vs = []
    for g in chunks(vi):
        for it in yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(g)).execute().get("items", []):
            d = it["contentDetails"].get("duration")
            vs.append({"id": it["id"], "titulo": it["snippet"]["title"], "pub": it["snippet"]["publishedAt"][:10], "views": int(it.get("statistics", {}).get("viewCount", 0)), "dur_s": segundos(d) if d and "D" not in d else 0})
        un += 1
    out[cid] = {"completo": tok is None, "videos": vs}
    json.dump(out, open(fn, "w"), ensure_ascii=False)
print("canais com uploads:", len(out), "unidades:", un, file=sys.stderr)
