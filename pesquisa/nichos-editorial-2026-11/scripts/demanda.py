"""Demanda e porta aberta por nicho × idioma -> dados/demanda.json, dados/porta.json + impressão.
Longo = > 180 s. Porta aberta (proxy) = canal criado há < 12 meses com longo >= 100 mil no nicho; o 1º vídeo é conferido em canais.py."""
import json, os, statistics as stt, datetime as dt, collections
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = [json.loads(l) for l in open(os.path.join(BASE, "dados", "busca.jsonl"))]
V = json.load(open(os.path.join(BASE, "dados", "videos_api.json")))
C = json.load(open(os.path.join(BASE, "dados", "canais_api.json")))
hoje = dt.date(2026, 11, 11)
def idade(v): return (hoje - dt.date.fromisoformat(v["publicado"])).days
def longo(v): return (v.get("dur") or 0) > 180
porq = collections.defaultdict(lambda: {"rel": [], "todos": set()})
for r in rows:
    if r["id"] not in V: continue
    k = (r["nicho"], r["lang"], r["q"])
    if r["ordem"] == "relevancia": porq[k]["rel"].append(r["id"])
    porq[k]["todos"].add(r["id"])
consultas = []
for (n, l, q), d in porq.items():
    rel = [V[i]["views"] for i in d["rel"][:10]]
    vs = [V[i] for i in d["todos"]]
    consultas.append({"nicho": n, "lang": l, "q": q, "mediana_top10": int(stt.median(rel)) if rel else 0,
                      "ano_100k_longos": sum(1 for v in vs if idade(v) <= 365 and longo(v) and v["views"] >= 100_000),
                      "d90_100k_longos": sum(1 for v in vs if idade(v) <= 90 and longo(v) and v["views"] >= 100_000),
                      "d90_100k_todos": sum(1 for v in vs if idade(v) <= 90 and v["views"] >= 100_000)})
agg = {}
for n, l in {(c["nicho"], c["lang"]) for c in consultas}:
    cs = [c for c in consultas if c["nicho"] == n and c["lang"] == l]
    ids = set().union(*[porq[(n, l, c["q"])]["todos"] for c in cs])
    vs = [dict(V[i], id=i) for i in ids]
    r90 = sorted([v for v in vs if idade(v) <= 90 and longo(v)], key=lambda v: -v["views"])
    novos = collections.defaultdict(list)
    for v in vs:
        c = C.get(v["channel_id"])
        if c and (hoje - dt.date.fromisoformat(c["criado"])).days <= 365 and longo(v) and v["views"] >= 100_000:
            novos[v["channel_id"]].append(v)
    agg[f"{n}|{l}"] = {"nicho": n, "lang": l, "mediana_das_medianas": int(stt.median([c["mediana_top10"] for c in cs])),
                       "d90_100k_longos": sum(1 for v in r90 if v["views"] >= 100_000),
                       "ano_100k_longos": sum(1 for v in vs if idade(v) <= 365 and longo(v) and v["views"] >= 100_000),
                       "top90": [(v["views"], v["publicado"], v["canal"], v["titulo"][:80], v["id"]) for v in r90[:5]],
                       "canais_novos_hit": [{"channel_id": cid, "nome": C[cid]["nome"], "criado": C[cid]["criado"], "inscritos": C[cid]["inscritos"],
                                             "views_canal": C[cid]["views"], "n_videos": C[cid]["n_videos"],
                                             "melhor": max(vv, key=lambda x: x["views"])["views"], "titulo": max(vv, key=lambda x: x["views"])["titulo"][:80]}
                                            for cid, vv in sorted(novos.items(), key=lambda kv: -max(x["views"] for x in kv[1]))]}
json.dump(consultas, open(os.path.join(BASE, "dados", "demanda_consultas.json"), "w"), ensure_ascii=False, indent=1)
json.dump(agg, open(os.path.join(BASE, "dados", "demanda.json"), "w"), ensure_ascii=False, indent=1)
print("nicho      lang  med_med10   ano100kL  d90_100kL  novos_hit")
for a in sorted(agg.values(), key=lambda a: (a["nicho"], ["en", "es", "pt", "fr", "de"].index(a["lang"]))):
    print(f'{a["nicho"]:10} {a["lang"]:4} {a["mediana_das_medianas"]:>10,} {a["ano_100k_longos"]:>9} {a["d90_100k_longos"]:>9} {len(a["canais_novos_hit"]):>9}')
