"""Lista completa de vídeos dos 2 canais de referência + descrições. Saída: dados/ref_videos.json, dados/descricoes/<id>.txt"""
import json, os, sys, statistics as stt
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, segundos, chunks
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = {"where-they-stood": "UCUt7wPSxHRObHObdAW-26JQ", "civil-war-fine-print": "UCE1gBqF9TF6JswS0zsxdGTg"}
yt = yt_client(); out = {}; un = 0
for nome, cid in REF.items():
    ch = yt.channels().list(part="snippet,statistics,contentDetails", id=cid).execute()["items"][0]; un += 1
    up = ch["contentDetails"]["relatedPlaylists"]["uploads"]; ids = []; tok = None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=50, pageToken=tok).execute(); un += 1
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]; tok = r.get("nextPageToken")
        if not tok: break
    vs = []
    for g in chunks(ids):
        for v in yt.videos().list(part="snippet,statistics,contentDetails,status", id=",".join(g)).execute()["items"]:
            sn, st, cd = v["snippet"], v.get("statistics", {}), v["contentDetails"]
            vs.append({"id": v["id"], "titulo": sn["title"], "pub": sn["publishedAt"], "views": int(st.get("viewCount", 0)), "likes": int(st.get("likeCount", 0) or 0),
                       "coments": int(st.get("commentCount", 0) or 0), "dur": segundos(cd["duration"]) if cd.get("duration") and "D" not in cd["duration"] else None,
                       "licensed": cd.get("licensedContent"), "tags": sn.get("tags", [])[:15]})
            open(os.path.join(BASE, "dados/descricoes", v["id"] + ".txt"), "w").write(sn.get("description", ""))
        un += 1
    vs.sort(key=lambda v: v["pub"])
    out[nome] = {"canal": {"id": cid, "titulo": ch["snippet"]["title"], "handle": ch["snippet"].get("customUrl"), "criado": ch["snippet"]["publishedAt"], "pais": ch["snippet"].get("country"),
                           "inscritos": int(ch["statistics"].get("subscriberCount", 0)), "views": int(ch["statistics"]["viewCount"]), "n_videos": int(ch["statistics"]["videoCount"]),
                           "descricao": ch["snippet"].get("description", "")}, "videos": vs}
json.dump(out, open(os.path.join(BASE, "dados/ref_videos.json"), "w"), ensure_ascii=False, indent=1)
print("unidades", un)
for n, d in out.items():
    print("==", n, d["canal"]["inscritos"], d["canal"]["views"], d["canal"]["n_videos"], d["canal"]["handle"], d["canal"]["criado"][:10])
    for v in d["videos"]:
        print(v["pub"][:10], f'{v["views"]:>9,} {v["likes"]:>6} {v["coments"]:>5} {(v["dur"] or 0)//60:>3}m {v["licensed"]} {v["id"]} {v["titulo"][:70]}')
