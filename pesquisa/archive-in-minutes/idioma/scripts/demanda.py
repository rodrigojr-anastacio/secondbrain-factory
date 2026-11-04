"""Demanda por idioma e tema a partir do pool de vídeos da busca (todas as consultas) + videos_api.
Vídeo conta para (idioma, tema) se: idioma(áudio ou título) = idioma, título ORIGINAL cita o tema, duração >= 4 min.
Saída: dados/demanda.json e dados/candidatos_formula.json (canais com título na fórmula, por idioma)."""
import json, os, statistics, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import idioma, temas, formula, em_minutos, TEMA_RE, ficcao, NUCLEO
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = json.load(open(os.path.join(BASE, "dados/videos_api.json")))
LANGS = ["en", "es", "pt", "fr", "de", "it", "ru", "tr", "hi", "ja", "pl", "ar"]
ANO = "2026-01-01"
MIN_S = 240
C4 = ["kgb", "cia", "mossad", "gestapo"]  # temas buscados em TODOS os idiomas (comparável)
pool = collections.defaultdict(dict)  # (lang, tema) -> {id: v}
form = collections.defaultdict(lambda: collections.defaultdict(list))  # lang -> channel -> [v]
for vid, v in V.items():
    if v["live"] not in (None, "none") or v["dur_s"] < MIN_S: continue
    l = idioma(v)
    if ficcao(v["titulo"], v["canal"]):
        if l in LANGS and formula(v["titulo"], l): pass
        else: continue
    if l not in LANGS: continue
    v = {**v, "id": vid, "idioma": l, "ano": v["pub"] >= ANO, "temas": temas(v["titulo"])}
    for t in v["temas"]: pool[(l, t)][vid] = v
    if formula(v["titulo"], l):
        form[l][v["channel_id"]].append(v)
def med(xs): return int(statistics.median(xs)) if xs else 0
out = {}
for l in LANGS:
    por_tema = {}
    vids_l = {}
    for t in TEMA_RE:
        vs = sorted(pool.get((l, t), {}).values(), key=lambda v: -v["views"])
        vids_l.update({v["id"]: v for v in vs})
        ano = [v for v in vs if v["ano"]]
        top10 = [v["views"] for v in vs[:10]]
        por_tema[t] = {"n": len(vs), "top1": vs[0]["views"] if vs else 0,
                       "top1_titulo": vs[0]["titulo"] if vs else None, "top1_canal": vs[0]["canal"] if vs else None, "top1_id": vs[0]["id"] if vs else None,
                       "top10_soma": sum(top10), "top10_mediana": med(top10),
                       "ano_n": len(ano), "ano_top1": ano[0]["views"] if ano else 0, "ano_top1_titulo": ano[0]["titulo"] if ano else None,
                       "ano_top1_canal": ano[0]["canal"] if ano else None, "ano_top1_id": ano[0]["id"] if ano else None,
                       "ano_top10_mediana": med([v["views"] for v in ano[:10]]),
                       "ano_gt100k": sum(v["views"] > 100_000 for v in ano), "ano_gt1m": sum(v["views"] > 1_000_000 for v in ano),
                       "top20": [(v["views"], v["pub"], round(v["dur_s"] / 60), v["titulo"][:90], v["canal"], v["id"]) for v in vs[:20]]}
    allv = list(vids_l.values()); ano = [v for v in allv if v["ano"]]
    out[l] = {"temas": por_tema,
              "total": {"videos_unicos": len(allv),
                        "mediana_top1_por_tema": med([d["top1"] for d in por_tema.values() if d["n"]]),
                        "mediana_top10mediana_por_tema": med([d["top10_mediana"] for d in por_tema.values() if d["n"]]),
                        "soma_top10_todos_temas": sum(d["top10_soma"] for d in por_tema.values()),
                        "c4_mediana_top1": med([por_tema[t]["top1"] for t in C4]),
                        "c4_mediana_top10mediana": med([por_tema[t]["top10_mediana"] for t in C4]),
                        "c4_soma_top10": sum(por_tema[t]["top10_soma"] for t in C4),
                        "c4_ano_gt100k": len({v["id"] for t in C4 for v in pool.get((l, t), {}).values() if v["ano"] and v["views"] > 100_000}),
                        "c4_ano_gt1m": len({v["id"] for t in C4 for v in pool.get((l, t), {}).values() if v["ano"] and v["views"] > 1_000_000}),
                        "nucleo7_mediana_top1": med([por_tema[t]["top1"] for t in NUCLEO]),
                        "nucleo7_mediana_top10mediana": med([por_tema[t]["top10_mediana"] for t in NUCLEO]),
                        "nucleo7_soma_top10": sum(por_tema[t]["top10_soma"] for t in NUCLEO),
                        "nucleo7_ano_gt100k": len({v["id"] for t in NUCLEO for v in pool.get((l, t), {}).values() if v["ano"] and v["views"] > 100_000}),
                        "nucleo7_ano_gt1m": len({v["id"] for t in NUCLEO for v in pool.get((l, t), {}).values() if v["ano"] and v["views"] > 1_000_000}),
                        "ano_videos": len(ano), "ano_gt100k": sum(v["views"] > 100_000 for v in ano), "ano_gt1m": sum(v["views"] > 1_000_000 for v in ano),
                        "ano_soma_views": sum(v["views"] for v in ano),
                        "ano_top": [(v["views"], v["pub"], v["titulo"][:80], v["canal"], v["id"]) for v in sorted(ano, key=lambda v: -v["views"])[:8]]}}
    t = out[l]["total"]
    print(f"{l}: vids={t['videos_unicos']} medTop1={t['mediana_top1_por_tema']} medTop10med={t['mediana_top10mediana_por_tema']} somaTop10={t['soma_top10_todos_temas']} "
          f"ano={t['ano_videos']} >100k={t['ano_gt100k']} >1m={t['ano_gt1m']} | C4 medTop1={t['c4_mediana_top1']} medTop10med={t['c4_mediana_top10mediana']} soma={t['c4_soma_top10']} ano>100k={t['c4_ano_gt100k']} >1m={t['c4_ano_gt1m']} | N7 medTop1={t['nucleo7_mediana_top1']} medTop10med={t['nucleo7_mediana_top10mediana']} soma={t['nucleo7_soma_top10']} ano>100k={t['nucleo7_ano_gt100k']} >1m={t['nucleo7_ano_gt1m']}", file=sys.stderr)
json.dump(out, open(os.path.join(BASE, "dados/demanda.json"), "w"), ensure_ascii=False, indent=1)
cand = {l: [{"channel_id": c, "canal": vs[0]["canal"], "n_formula_no_pool": len(vs), "org": sum(bool(v["temas"]) for v in vs),
             "min": sum(em_minutos(v["titulo"]) for v in vs), "exemplos": [(v["views"], v["pub"], v["titulo"][:80]) for v in sorted(vs, key=lambda v: -v["views"])[:3]]}
            for c, vs in sorted(d.items(), key=lambda x: -max(v["views"] for v in x[1]))] for l, d in form.items()}
json.dump(cand, open(os.path.join(BASE, "dados/candidatos_formula.json"), "w"), ensure_ascii=False, indent=1)
for l, cs in cand.items(): print(l, "canais com título-fórmula:", len(cs), file=sys.stderr)
