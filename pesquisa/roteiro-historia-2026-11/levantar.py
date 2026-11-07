"""Lista todos os vídeos dos canais de referência (Data API, ~1 unidade por chamada). Saída: canais.json"""
import json, os, sys, datetime as dt
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, segundos, chunks
HANDLES = {"A": ["Inkexplainer96", "Kelevins", "Crayon_Capital"], "B": ["HistóriaNaMarra"], "C": ["Archlang", "breakdownwithpaints"]}
EXTRA = ["yV-Cwcy8K6A", "cjIvXfkF1S0"]
yt = yt_client(); hoje = dt.datetime.now(dt.timezone.utc); out = {}
for g, hs in HANDLES.items():
    for h in hs:
        r = yt.channels().list(part="snippet,statistics,contentDetails", forHandle=h).execute()
        if not r.get("items"): print("não achei", h); continue
        c = r["items"][0]; up = c["contentDetails"]["relatedPlaylists"]["uploads"]
        ids, tok = [], None
        while True:
            p = yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=50, pageToken=tok).execute()
            ids += [i["contentDetails"]["videoId"] for i in p["items"]]; tok = p.get("nextPageToken")
            if not tok or len(ids) >= 200: break
        vids = []
        for ch in chunks(ids):
            for v in yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ch)).execute()["items"]:
                pub = dt.datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
                vids.append(dict(id=v["id"], titulo=v["snippet"]["title"], pub=pub.date().isoformat(), idade_d=(hoje - pub).days,
                                 dur_s=segundos(v["contentDetails"]["duration"]), views=int(v["statistics"].get("viewCount", 0)),
                                 likes=int(v["statistics"].get("likeCount", 0)), coments=int(v["statistics"].get("commentCount", 0))))
        vids.sort(key=lambda x: x["pub"])
        out[h] = dict(grupo=g, id=c["id"], nome=c["snippet"]["title"], criado=c["snippet"]["publishedAt"][:10],
                      inscritos=int(c["statistics"].get("subscriberCount", 0)), views=int(c["statistics"]["viewCount"]), videos=vids)
        print(f"{g} {h} | {c['snippet']['title']} | {out[h]['inscritos']} insc | {len(vids)} vídeos")
        for v in vids: print(f"   {v['pub']} {v['id']} {v['views']:>9} {v['dur_s']//60:>3}:{v['dur_s']%60:02d} {v['titulo'][:80]}")
for v in yt.videos().list(part="snippet", id=",".join(EXTRA)).execute()["items"]:
    print("EXTRA", v["id"], v["snippet"]["channelTitle"], v["snippet"]["title"])
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "canais.json"), "w"), ensure_ascii=False, indent=1)
