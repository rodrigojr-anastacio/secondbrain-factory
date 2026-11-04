"""Classifica os canais de canais_api.json por idioma e fórmula. Saída: dados/concorrencia.json (+ resumo no stderr)."""
import json, os, sys, collections, statistics, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import idioma, temas, formula, em_minutos
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = json.load(open(os.path.join(BASE, "dados/canais_api.json")))
HOJE = dt.date(2026, 11, 4)
def med(xs): return int(statistics.median(xs)) if xs else 0
out = []
for c in CH.values():
    longos = [v for v in c["videos"] if v["dur_s"] > 180]
    if not longos: continue
    langs = collections.Counter(idioma(v) for v in longos)
    lang = langs.most_common(1)[0][0]
    for v in longos:
        v["f"] = formula(v["titulo"], lang) or formula(v["titulo"], "en")
        v["org"] = bool(temas(v["titulo"])); v["min"] = em_minutos(v["titulo"])
        v["idade"] = (HOJE - dt.date.fromisoformat(v["pub"])).days
    fm = [v for v in longos if v["f"]]
    fo = [v for v in fm if v["org"]]
    primeiro = min(v["pub"] for v in c["videos"]) if c["lista_completa"] and c["videos"] else None
    inicio = primeiro or c["criado"]
    pct = round(100 * len(fm) / len(longos))
    if fo and pct >= 40: cls = "formula_org"
    elif fo: cls = "formula_org_parcial"
    elif fm and pct >= 40: cls = "formula_outros"
    else: cls = "outro_formato"
    mad = [v for v in longos if v["idade"] >= 7]  # vídeos com >= 7 dias (mediana "madura")
    best = max(longos, key=lambda v: v["views"])
    out.append({"id": c["id"], "nome": c["nome"], "handle": c["handle"], "pais": c["pais"], "lang": lang, "langs": dict(langs), "classe": cls,
                "antigo_dados_json": c["antigo"], "criado": c["criado"], "primeiro_video": primeiro, "inicio": inicio,
                "clone_desde_09_2026": inicio >= "2026-09-01", "lista_completa": c["lista_completa"],
                "n_videos": c["n_videos"], "n_longos_vistos": len(longos), "n_formula": len(fm), "n_formula_org": len(fo), "pct_formula": pct,
                "views": c["views"], "inscritos": c["inscritos"],
                "mediana_longos": med([v["views"] for v in longos]), "mediana_longos_7d": med([v["views"] for v in mad]),
                "mediana_formula": med([v["views"] for v in fm]), "mediana_formula_org": med([v["views"] for v in fo]),
                "melhor": {"views": best["views"], "titulo": best["titulo"], "id": best["id"], "pub": best["pub"]},
                "melhor_formula_org": (lambda b: {"views": b["views"], "titulo": b["titulo"], "id": b["id"], "pub": b["pub"]})(max(fo, key=lambda v: v["views"])) if fo else None,
                "ultimo_video": max(v["pub"] for v in c["videos"])})
json.dump(out, open(os.path.join(BASE, "dados/concorrencia.json"), "w"), ensure_ascii=False, indent=1)
for l in ["en", "es", "pt", "fr", "de", "it", "pl", "ru", "tr", "hi", "ja", "ar"]:
    cs = sorted([o for o in out if o["lang"] == l and o["classe"] in ("formula_org", "formula_org_parcial", "formula_outros")], key=lambda o: -o["mediana_longos"])
    print(f"== {l}: formula_org={sum(o['classe']=='formula_org' for o in cs)} parcial={sum(o['classe']=='formula_org_parcial' for o in cs)} outros={sum(o['classe']=='formula_outros' for o in cs)}", file=sys.stderr)
    for o in cs:
        if o["classe"] == "formula_outros" and o["mediana_longos"] < 3000: continue
        mo = o["melhor_formula_org"] or o["melhor"]
        print(f"  {o['classe'][:14]:14} {o['nome'][:26]:26} {o['pais'] or '--'} ini={o['inicio']} v={o['n_videos']} f={o['n_formula']}/{o['n_formula_org']} pct={o['pct_formula']} "
              f"med={o['mediana_longos']} med7={o['mediana_longos_7d']} medFO={o['mediana_formula_org']} subs={o['inscritos']} best={mo['views']} {mo['titulo'][:45]}", file=sys.stderr)
