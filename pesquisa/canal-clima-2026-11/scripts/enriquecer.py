"""Data API (só leitura): videos.list e channels.list dos resultados da busca. ~1 un/50 ids.
Saída: dados/videos_api.json, dados/canais_api.json"""
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, segundos, chunks
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = [json.loads(l) for l in open(os.path.join(BASE, "dados", "busca.jsonl"))]
vids = sorted({r["id"] for r in rows if r.get("id")})
yt = yt_client(); un = 0; V = {}
for g in chunks(vids):
    for it in yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(g), maxResults=50).execute().get("items", []):
        sn, st, cd = it["snippet"], it.get("statistics", {}), it["contentDetails"]
        V[it["id"]] = {"titulo": sn["title"], "canal": sn["channelTitle"], "channel_id": sn["channelId"], "publicado": sn["publishedAt"][:10],
                       "views": int(st.get("viewCount", 0)), "likes": int(st.get("likeCount", 0) or 0), "coments": int(st.get("commentCount", 0) or 0),
                       "dur": segundos(cd["duration"]) if cd.get("duration") and "D" not in cd["duration"] else None,
                       "licensed": cd.get("licensedContent"), "lang": sn.get("defaultAudioLanguage") or sn.get("defaultLanguage"), "cat": sn.get("categoryId")}
    un += 1
chs = sorted({v["channel_id"] for v in V.values()}); C = {}
for g in chunks(chs):
    for it in yt.channels().list(part="snippet,statistics,contentDetails", id=",".join(g), maxResults=50).execute().get("items", []):
        sn, st = it["snippet"], it["statistics"]
        C[it["id"]] = {"nome": sn["title"], "handle": sn.get("customUrl"), "criado": sn["publishedAt"][:10], "pais": sn.get("country"),
                       "views": int(st.get("viewCount", 0)), "inscritos": int(st.get("subscriberCount", 0) or 0), "n_videos": int(st.get("videoCount", 0)),
                       "uploads": it["contentDetails"]["relatedPlaylists"]["uploads"]}
    un += 1
json.dump(V, open(os.path.join(BASE, "dados", "videos_api.json"), "w"), ensure_ascii=False)
json.dump(C, open(os.path.join(BASE, "dados", "canais_api.json"), "w"), ensure_ascii=False)
print(len(V), "vídeos,", len(C), "canais,", un, "unidades")
