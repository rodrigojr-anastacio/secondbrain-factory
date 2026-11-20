"""Etapa 2: videos.list + channels.list (1 unidade/50) -> dados/videos.json, dados/canais.json."""
import json, os, sys, re
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, segundos, chunks

D = os.path.join(os.path.dirname(__file__), "..", "dados")
yt = yt_client()
rows = [json.loads(l) for l in open(os.path.join(D, "busca.jsonl"))]
meta = {}
for r in rows:
    m = meta.setdefault(r["id"], {"grupos": set(), "queries": set(), "modos": set()})
    m["grupos"].add(r["grupo"]); m["queries"].add(r["query"]); m["modos"].add(r["modo"])

vids = {}
units = 0
for ch in chunks(list(meta)):
    res = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ch)).execute(); units += 1
    for v in res["items"]:
        s = v["statistics"]; sn = v["snippet"]
        vids[v["id"]] = {
            "id": v["id"], "titulo": sn["title"], "canal": sn["channelTitle"], "canal_id": sn["channelId"],
            "publicado": sn["publishedAt"], "views": int(s.get("viewCount", 0)), "likes": int(s.get("likeCount", 0) or 0),
            "comentarios": int(s.get("commentCount", 0) or 0), "duracao_s": segundos(v["contentDetails"].get("duration") or "PT0S"),
            "licensed": v["contentDetails"].get("licensedContent"), "idioma": sn.get("defaultAudioLanguage") or sn.get("defaultLanguage"),
            "grupos": sorted(meta[v["id"]]["grupos"]), "queries": sorted(meta[v["id"]]["queries"]), "modos": sorted(meta[v["id"]]["modos"]),
        }
cans = {}
for ch in chunks(sorted({v["canal_id"] for v in vids.values()})):
    res = yt.channels().list(part="snippet,statistics,contentDetails", id=",".join(ch)).execute(); units += 1
    for c in res["items"]:
        st = c["statistics"]
        cans[c["id"]] = {"id": c["id"], "nome": c["snippet"]["title"], "criado": c["snippet"]["publishedAt"],
                         "pais": c["snippet"].get("country"), "inscritos": int(st.get("subscriberCount", 0) or 0),
                         "views": int(st.get("viewCount", 0)), "n_videos": int(st.get("videoCount", 0)),
                         "uploads": c["contentDetails"]["relatedPlaylists"]["uploads"]}
json.dump(vids, open(os.path.join(D, "videos.json"), "w"), ensure_ascii=False)
json.dump(cans, open(os.path.join(D, "canais.json"), "w"), ensure_ascii=False)
print("videos", len(vids), "canais", len(cans), "unidades", units)
