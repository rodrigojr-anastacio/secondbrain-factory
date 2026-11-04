"""Concorrência por subnicho: canais com título forte (alto) no subnicho, por janela de publicação. Fora da manada (países/impérios/serviços secretos)."""
import json, os, re, collections, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "scripts"))
from classificar import KW
# palavras-chave extras de empresas (marcas citadas nos títulos encontrados)
KW = dict(KW)
KW["empresas_marcas"] += r"|walmart|costco|nintendo|tesla|nvidia|tsmc|chatgpt|facebook|instagram|apple|microsoft|amazon|toyota|rolls-royce|spacex|elon musk|buffett|rockefeller|morgan|onlyfans|target\b|ted\b|pepsi|singer|coca"
v = json.load(open(os.path.join(BASE, "dados/videos_formato.json")))
res = {}
for sub, rx in KW.items():
    for jan in (120, 365):
        xs = [x for x in v if x["forca_titulo"] == "alto" and not x["manada"] and (x.get("idade_dias") or 9999) <= jan and (x.get("dur_s") or 0) >= 240 and re.search(rx, x["title"].lower())]
        chs = collections.defaultdict(list)
        for x in xs: chs[x["channel"]].append(x)
        res.setdefault(sub, {})[jan] = {
            "videos": len(xs), "canais": len(chs),
            "canais_com_50k": sum(1 for c in chs.values() if max(y["views"] for y in c) >= 50_000),
            "videos_100k": sum(1 for x in xs if x["views"] >= 100_000),
            "mediana_views": sorted(x["views"] for x in xs)[len(xs)//2] if xs else 0,
            "top": [(x["views"], x["channel"], x["title"][:60]) for x in sorted(xs, key=lambda x: -x["views"])[:5]]}
json.dump(res, open(os.path.join(BASE, "dados/concorrencia.json"), "w"), ensure_ascii=False, indent=1)
for sub, d in sorted(res.items(), key=lambda kv: -kv[1][365]["videos_100k"]):
    a, b = d[120], d[365]
    print(f"{sub:22} 120d: vid={a['videos']:3} canais={a['canais']:3} c50k={a['canais_com_50k']:2} v100k={a['videos_100k']:2} med={a['mediana_views']:>7} | 365d: vid={b['videos']:3} canais={b['canais']:3} c50k={b['canais_com_50k']:2} v100k={b['videos_100k']:2} med={b['mediana_views']:>7}")
