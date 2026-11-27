"""Bolha máfias/organizações (27/11/2026): demanda em es nos últimos 12 meses via Data API (readonly).
Rodar de tools/: .venv/bin/python ../canais/dossie-es/analises/2026-11-27-bolha-dados/buscar.py
Grava demanda.json ao lado. Custo: ~100 unidades por termo (search.list).
"""
import datetime as dt, json, os, re, statistics, sys
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from googleapiclient.discovery import build  # noqa
from report import creds_for  # noqa

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demanda.json")
TERMOS = {
 "cinco-familias": "las cinco familias de nueva york mafia",
 "luciano": "lucky luciano",
 "capone-outfit": "al capone mafia chicago",
 "falcone-maxiproceso": "giovanni falcone maxiproceso mafia",
 "stasi": "stasi policía secreta",
 "odessa": "odessa nazis sudamérica",
 "murder-inc": "murder inc mafia",
 "mafia-rusa": "mafia rusa",
 "ndrangheta": "ndrangheta",
 "camorra": "camorra mafia napoles",
 "triadas": "triadas chinas mafia",
 "mafia-albanesa": "mafia albanesa",
 "hells-angels": "hells angels",
 "zetas": "los zetas cartel",
 "sinaloa": "cartel de sinaloa historia",
 "cali": "cartel de cali",
 "conexion-francesa": "conexion francesa mafia corsa heroina",
 "ms13": "mara salvatrucha ms13 historia",
 "mafia-judia": "mafia judía meyer lansky",
 "corleoneses": "toto riina corleoneses",
 "mafia-generica": "historia de la mafia",
}
ES = re.compile(r"\b(la|el|los|las|de|del|que|cómo|como|historia|por|una|un|y)\b", re.I)
c = creds_for("dossie-es")
yt = build("youtube", "v3", credentials=c, cache_discovery=False)
desde = (dt.datetime.utcnow() - dt.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")

def dur(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0

res = {}
for slug, q in TERMOS.items():
    try:
        r = yt.search().list(part="id", q=q, type="video", order="viewCount", relevanceLanguage="es",
                             publishedAfter=desde, maxResults=50).execute()
    except Exception as e:  # noqa
        print("erro", slug, str(e)[:200]); continue
    ids = [i["id"]["videoId"] for i in r.get("items", [])]
    vids = []
    if ids:
        for v in yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids)).execute()["items"]:
            sn = v["snippet"]; lang = (sn.get("defaultAudioLanguage") or sn.get("defaultLanguage") or "")
            t = sn["title"]
            es = lang.startswith("es") or (not lang and len(ES.findall(t)) >= 1 and not re.search(r"\b(the|of|and|how|o|do|da|não)\b", t, re.I))
            d = dur(v["contentDetails"]["duration"])
            vids.append({"id": v["id"], "titulo": t, "canal": sn["channelTitle"], "pub": sn["publishedAt"][:10],
                         "views": int(v["statistics"].get("viewCount", 0)), "dur": d, "lang": lang, "es": es})
    longos = sorted([x for x in vids if x["es"] and x["dur"] >= 300], key=lambda x: -x["views"])
    top10 = longos[:10]
    res[slug] = {"q": q, "n_longos_es": len(longos), "top": longos[:12],
                 "mediana_top10": int(statistics.median([x["views"] for x in top10])) if top10 else 0,
                 "max": top10[0]["views"] if top10 else 0,
                 "acima_100k": sum(1 for x in longos if x["views"] >= 100_000)}
    print(f"{slug:22} n={len(longos):2} med10={res[slug]['mediana_top10']:>9,} max={res[slug]['max']:>10,} >100k={res[slug]['acima_100k']}")
json.dump({"lido_em": dt.datetime.now().isoformat(), "desde": desde, "res": res}, open(OUT, "w"), ensure_ascii=False, indent=1)
