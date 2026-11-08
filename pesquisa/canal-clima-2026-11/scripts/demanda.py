"""Resumo da demanda por consulta e idioma -> dados/demanda.json + impressão."""
import json, os, statistics as stt, datetime as dt
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = [json.loads(l) for l in open(os.path.join(BASE, "dados", "busca.jsonl"))]
V = json.load(open(os.path.join(BASE, "dados", "videos_api.json")))
C = json.load(open(os.path.join(BASE, "dados", "canais_api.json")))
hoje = dt.date(2026, 11, 8)
def idade(v): return (hoje - dt.date.fromisoformat(v["publicado"])).days
out = {}
for r in rows:
    k = (r["lang"], r["q"]); d = out.setdefault(k, {"lang": r["lang"], "grupo": r["grupo"], "q": r["q"], "rel": [], "mes": [], "ano": []})
    v = V.get(r["id"])
    if not v: continue
    d[{"relevancia": "rel", "mes_views": "mes", "ano_views": "ano"}[r["ordem"]]].append(r["id"])
res = []
for (lang, q), d in out.items():
    rel = [V[i]["views"] for i in d["rel"][:10]]
    longos_ano = [V[i] for i in set(d["ano"] + d["rel"]) if idade(V[i]) <= 365]
    mes = [V[i] for i in set(d["mes"] + d["rel"] + d["ano"]) if idade(V[i]) <= 31]
    r90 = [V[i] for i in set(d["mes"] + d["rel"] + d["ano"]) if idade(V[i]) <= 90]
    top = sorted(r90, key=lambda v: -v["views"])[:3]
    res.append({"lang": lang, "grupo": d["grupo"], "q": q, "mediana_top10": int(stt.median(rel)) if rel else 0,
                "ano_100k": sum(1 for v in longos_ano if v["views"] >= 100_000), "mes_100k": sum(1 for v in mes if v["views"] >= 100_000),
                "mes_max": max([v["views"] for v in mes], default=0),
                "top90": [(v["views"], v["publicado"], v["canal"], v["titulo"][:70], v["dur"]) for v in top]})
json.dump(res, open(os.path.join(BASE, "dados", "demanda.json"), "w"), ensure_ascii=False, indent=1)
for x in sorted(res, key=lambda x: (x["lang"], -x["mediana_top10"])):
    print(f'{x["lang"]} | {x["q"][:42]:42} | med10 {x["mediana_top10"]:>9,} | ano≥100k {x["ano_100k"]:>2} | mês≥100k {x["mes_100k"]:>2} | mêsmax {x["mes_max"]:>9,}')
