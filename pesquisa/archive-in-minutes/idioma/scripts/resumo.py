"""Junta demanda + concorrência por idioma. Busca o país (channels.list, 1 un/50) dos canais do pool de demanda.
Saída: dados/resumo_idiomas.json e dados/paises_canais.json"""
import json, os, sys, collections, statistics
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import NUCLEO, temas, em_minutos, formula
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(BASE, "dados/demanda.json")))
C = json.load(open(os.path.join(BASE, "dados/concorrencia.json")))
CH = json.load(open(os.path.join(BASE, "dados/canais_api.json")))
V = json.load(open(os.path.join(BASE, "dados/videos_api.json")))
LANGS = list(D)
def med(xs): return int(statistics.median(xs)) if xs else 0
# país dos canais de demanda (top20 de cada tema)
pp = os.path.join(BASE, "dados/paises_canais.json")
paises = json.load(open(pp)) if os.path.exists(pp) else {}
need = set()
for l in LANGS:
    for t, x in D[l]["temas"].items():
        for r in x["top20"]:
            cid = V[r[5]]["channel_id"]
            if cid not in paises: need.add(cid)
if need:
    from trends import yt_client, chunks
    yt = yt_client(); un = 0
    for g in chunks(sorted(need)):
        for it in yt.channels().list(part="snippet,statistics", id=",".join(g), maxResults=50).execute().get("items", []):
            paises[it["id"]] = {"nome": it["snippet"]["title"], "pais": it["snippet"].get("country"), "inscritos": int(it["statistics"].get("subscriberCount", 0)),
                                "views": int(it["statistics"].get("viewCount", 0)), "n_videos": int(it["statistics"].get("videoCount", 0)),
                                "handle": it["snippet"].get("customUrl")}
        un += 1
    json.dump(paises, open(pp, "w"), ensure_ascii=False)
    print("channels.list unidades:", un, file=sys.stderr)
res = {}
for l in LANGS:
    dem = D[l]; tot = dem["total"]
    # teto: canais grandes no pool núcleo (soma de views dos vídeos do núcleo no top20)
    soma = collections.Counter(); pais_views = collections.Counter()
    for t, x in dem["temas"].items():
        for r in x["top20"]:
            cid = V[r[5]]["channel_id"]
            if t in NUCLEO: soma[cid] += r[0]
            pais_views[(paises.get(cid) or {}).get("pais") or "??"] += r[0]
    teto = [{"canal": (paises.get(c) or {}).get("nome"), "handle": (paises.get(c) or {}).get("handle"), "pais": (paises.get(c) or {}).get("pais"),
             "inscritos": (paises.get(c) or {}).get("inscritos"), "views_nucleo_top20": s} for c, s in soma.most_common(6)]
    totpv = sum(pais_views.values()) or 1
    cs = [o for o in C if o["lang"] == l]
    # molde exato: fórmula + organização + "N minutos" no título, canal majoritariamente na fórmula
    def molde(o):
        vids = CH[o["id"]]["videos"]
        return any(formula(v["titulo"], l) or formula(v["titulo"], "en") for v in vids) and \
               any((formula(v["titulo"], l) or formula(v["titulo"], "en")) and temas(v["titulo"]) and em_minutos(v["titulo"]) for v in vids) and o["pct_formula"] >= 40
    exatos = sorted([o for o in cs if molde(o)], key=lambda o: -(o["melhor_formula_org"] or {"views": 0})["views"])
    outros_org = [o for o in cs if o["classe"] in ("formula_org", "formula_org_parcial") and o not in exatos]
    form_outros = [o for o in cs if o["classe"] == "formula_outros"]
    def row(o):
        mf = o["melhor_formula_org"] or o["melhor"]
        return {"nome": o["nome"], "link": f"https://www.youtube.com/channel/{o['id']}", "handle": o["handle"], "pais": o["pais"], "inicio": o["inicio"],
                "primeiro_video_confirmado": o["primeiro_video"] is not None, "n_videos": o["n_videos"], "inscritos": o["inscritos"], "views": o["views"],
                "mediana_longos": o["mediana_longos"], "mediana_longos_7d": o["mediana_longos_7d"], "mediana_formula_org": o["mediana_formula_org"],
                "n_formula_org": o["n_formula_org"], "melhor": mf, "clone_desde_09_2026": o["clone_desde_09_2026"], "ultimo_video": o["ultimo_video"]}
    ex = [row(o) for o in exatos]
    clones = [r for r in ex if r["clone_desde_09_2026"]]
    res[l] = {
        "demanda": {"videos_unicos_no_pool": tot["videos_unicos"], "c4_mediana_top1": tot["c4_mediana_top1"], "c4_mediana_top10mediana": tot["c4_mediana_top10mediana"],
                    "c4_soma_top10": tot["c4_soma_top10"], "c4_ano_gt100k": tot["c4_ano_gt100k"], "c4_ano_gt1m": tot["c4_ano_gt1m"],
                    "nucleo7_mediana_top1": tot["nucleo7_mediana_top1"], "nucleo7_mediana_top10mediana": tot["nucleo7_mediana_top10mediana"],
                    "nucleo7_soma_top10": tot["nucleo7_soma_top10"], "nucleo7_ano_gt100k": tot["nucleo7_ano_gt100k"], "nucleo7_ano_gt1m": tot["nucleo7_ano_gt1m"],
                    "todos12_soma_top10": tot["soma_top10_todos_temas"], "todos12_ano_gt100k": tot["ano_gt100k"], "todos12_ano_gt1m": tot["ano_gt1m"],
                    "por_tema": {t: {k: x[k] for k in ("n", "top1", "top1_titulo", "top1_canal", "top10_mediana", "top10_soma", "ano_top1", "ano_top1_titulo", "ano_top1_canal",
                                                         "ano_top10_mediana", "ano_gt100k", "ano_gt1m")} for t, x in dem["temas"].items() if x["n"]},
                    "paises_dos_canais_pct_views_top20": {p: round(100 * v / totpv) for p, v in pais_views.most_common(8)},
                    "teto_canais": teto},
        "concorrencia": {"n_molde_exato": len(ex), "n_clones_desde_09_2026": len(clones),
                         "mediana_das_medianas_formula_org_clones": med([r["mediana_formula_org"] for r in clones]),
                         "n_molde_exato_mediana_gt5k": sum(r["mediana_formula_org"] > 5000 for r in ex),
                         "melhor_canal": ex[0] if ex else None, "canais_molde_exato": ex,
                         "n_formula_org_outro_molde": len(outros_org),
                         "formula_org_outro_molde": [row(o) for o in sorted(outros_org, key=lambda o: -o["mediana_formula_org"])[:12]],
                         "n_formula_outros_temas": len(form_outros),
                         "formula_outros_temas_top": [row(o) for o in sorted(form_outros, key=lambda o: -o["mediana_longos"])[:8]]}}
    print(l, "exatos", len(ex), "clones", len(clones), "med", res[l]["concorrencia"]["mediana_das_medianas_formula_org_clones"], ">5k", res[l]["concorrencia"]["n_molde_exato_mediana_gt5k"],
          "| paises", res[l]["demanda"]["paises_dos_canais_pct_views_top20"], file=sys.stderr)
json.dump(res, open(os.path.join(BASE, "dados/resumo_idiomas.json"), "w"), ensure_ascii=False, indent=1)
