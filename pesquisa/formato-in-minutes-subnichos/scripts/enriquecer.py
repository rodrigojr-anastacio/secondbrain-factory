"""Estatísticas em lote via API (videos.list e channels.list, 1 unidade por 50 ids). Só leitura; não grava no banco."""
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, segundos, chunks
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
yt = yt_client(); unidades = 0
vids = json.load(open(os.path.join(BASE, "dados/videos_formato.json")))
porid = {v["id"]: v for v in vids}
for g in chunks(list(porid)):
    r = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(g)).execute(); unidades += 1
    for it in r.get("items", []):
        v = porid[it["id"]]; st = it["statistics"]; sn = it["snippet"]
        v.update(channel_id=sn["channelId"], channel=sn["channelTitle"], publicado=sn["publishedAt"], views=int(st.get("viewCount", 0)), likes=int(st.get("likeCount", 0) or 0),
                 comentarios=int(st.get("commentCount", 0) or 0), dur_s=(segundos(it["contentDetails"]["duration"]) if "duration" in it["contentDetails"] else None),
                 idioma_audio=sn.get("defaultAudioLanguage"), thumb=sn["thumbnails"].get("high", {}).get("url"))
chs = {}
for g in chunks(sorted({v["channel_id"] for v in vids if v.get("channel_id")})):
    r = yt.channels().list(part="snippet,statistics,contentDetails", id=",".join(g)).execute(); unidades += 1
    for it in r.get("items", []):
        st = it["statistics"]
        chs[it["id"]] = {"id": it["id"], "nome": it["snippet"]["title"], "criado": it["snippet"]["publishedAt"],
                         "pais": it["snippet"].get("country"), "custom": it["snippet"].get("customUrl"),
                         "inscritos": int(st.get("subscriberCount", 0) or 0), "views": int(st.get("viewCount", 0)),
                         "n_videos": int(st.get("videoCount", 0)), "uploads": it["contentDetails"]["relatedPlaylists"]["uploads"]}
json.dump(vids, open(os.path.join(BASE, "dados/videos_formato.json"), "w"), ensure_ascii=False, indent=0)
json.dump(chs, open(os.path.join(BASE, "dados/canais_api.json"), "w"), ensure_ascii=False, indent=0)
print("unidades de cota gastas:", unidades, "vídeos", len(vids), "canais", len(chs))
