# Semiarido (lista IBGE 2022) + malhas municipais IBGE -> dados/semiarido.json (dissolvido e simplificado)
import json, openpyxl, os
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
D = "dl/dados/"
semi = {str(r[0]) for r in list(openpyxl.load_workbook(D + "lista_municipios_Semiarido_2022.xlsx").active.iter_rows(values_only=True))[1:]}
sel, found, ce, ce_semi = [], set(), [], []
for uf in (21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32):
    for f in json.load(open(D + f"mun{uf}.json"))["features"]:
        c = str(f["properties"]["codarea"]); g = shape(f["geometry"]).buffer(0)
        if c in semi: sel.append(g); found.add(c)
        if uf == 23:
            ce.append(g)
            if c in semi: ce_semi.append(g)
print("achados", len(found), "de", len(semi))
dis = lambda gs: unary_union([g.buffer(0.004) for g in gs]).buffer(-0.004).simplify(0.01)
def rnd(o):
    if isinstance(o, float): return round(o, 3)
    if isinstance(o, (list, tuple)): return [rnd(x) for x in o]
    if isinstance(o, dict): return {k: rnd(v) for k, v in o.items()}
    return o
feat = lambda g, p: {"type": "Feature", "properties": p, "geometry": rnd(mapping(g))}
out = {"type": "FeatureCollection", "metadata": {"fonte": "IBGE: lista de municipios do Semiarido (Situacao 2022, 1477 municipios; mesma lista da SUDENE 2021) + malhas municipais IBGE API v3 (qualidade minima), dissolvidas e simplificadas a 0,01 grau", "acesso": "2026-11-13", "municipios": len(found)},
       "features": [feat(dis(sel), {"nome": "Semiarido brasileiro (IBGE/SUDENE 2022)", "n_municipios": len(found)}),
                    feat(dis(ce_semi), {"nome": "Semiarido no Ceara", "n_municipios": len(ce_semi)}),
                    feat(dis(ce), {"nome": "Ceara (contorno)", "n_municipios": len(ce)})]}
json.dump(out, open("dados/semiarido.json", "w"), separators=(",", ":"))
print(os.path.getsize("dados/semiarido.json") // 1024, "KB", len(ce_semi), len(ce))
