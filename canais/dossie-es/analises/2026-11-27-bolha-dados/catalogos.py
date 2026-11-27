"""Catálogo dos canais da vizinhança (clones do formato + canais de máfia em es), Data API readonly.
Rodar de tools/: .venv/bin/python ../canais/dossie-es/analises/2026-11-27-bolha-dados/catalogos.py
Grava catalogos.json ao lado (custo ~1 unidade por chamada)."""
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from googleapiclient.discovery import build  # noqa
from report import creds_for  # noqa
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "catalogos.json")
SEMENTES = {"Archivo en Minutos": "1F7enXW5lvY", "La Historia Completa": "rwr5n--tsPg", "Archivo del Tiempo": "NARXeDbTF6g",
            "Atlas del Tiempo": "ufBVdt1y0bA", "Archive in Minutes (en)": "EQaNals3Czw", "Era Span": "lj7E82AFpz4",
            "militares informados": "QYGTAelfT9Q", "Pioneros y Leyendas": "Az5Je5FyHos", "Cruzada Hostil": "mjRbyUf9gXU",
            "La Era del Hampa": "99bCQU9biak", "Relato Mafioso": "uLms3r1-KvI"}
yt = build("youtube", "v3", credentials=creds_for("dossie-es"), cache_discovery=False)
out = {}
for nome, vid in SEMENTES.items():
    ch = yt.videos().list(part="snippet", id=vid).execute()["items"][0]["snippet"]["channelId"]
    c = yt.channels().list(part="contentDetails,statistics,snippet", id=ch).execute()["items"][0]
    up = c["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, tok = [], None
    while len(ids) < 250:
        r = yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=50, pageToken=tok).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        tok = r.get("nextPageToken")
        if not tok: break
    vids = []
    for i in range(0, len(ids), 50):
        for v in yt.videos().list(part="snippet,statistics", id=",".join(ids[i:i+50])).execute()["items"]:
            vids.append({"id": v["id"], "titulo": v["snippet"]["title"], "pub": v["snippet"]["publishedAt"][:10],
                         "views": int(v["statistics"].get("viewCount", 0))})
    vids.sort(key=lambda x: -x["views"])
    out[nome] = {"channelId": ch, "inscritos": c["statistics"].get("subscriberCount"), "n": len(vids), "videos": vids}
    print(f"== {nome} ({c['statistics'].get('subscriberCount')} insc, {len(vids)} vídeos)")
    for x in vids[:25]:
        print(f"   {x['views']:>9,} {x['pub']} {x['titulo'][:90]}")
json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
