"""Demanda por idioma: para cada idioma, 5 temas nativos (relevância + ano_views): top10 mediana, >100k em 2026, prova da fórmula, clones.
Filtros: dur >= 4 min, não live, idioma do vídeo = idioma da consulta (áudio/língua; senão script/palavras), título cita o tema. Saída: dados/demanda_idioma.json"""
import json, os, re, statistics as st, collections, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = json.load(open(os.path.join(BASE, "dados/videos_api.json")))
SW = {"en": [" the ", " of ", " and ", " why ", " what ", " was ", " how "], "es": [" el ", " los ", " las ", " del ", "qué", " por ", " una ", "ción", "ñ", " y "], "pt": [" da ", " do ", " dos ", "ã", "õ", "ç", " não ", " uma ", " em ", "ção"],
      "fr": [" le ", " les ", " du ", " des ", "l'", "l’", " à ", " et ", " une ", " est ", "è"], "de": [" der ", " die ", " das ", " und ", "ü", "ö", "ä", "ß", " ein", " wie ", " ist "],
      "it": [" della ", " dei ", " delle ", " il ", "perché", " gli ", " è ", "zione"], "pl": ["ł", "ś", "ż", "ą", "ę", " nie ", " się "], "tr": ["ı", "ş", "ğ", " ve ", " bir "]}
def lang(v):
    a = (v.get("audio") or v.get("lang") or "")[:2].lower()
    if a and a != "zx": return a
    t = " " + v["titulo"].lower() + " "
    if re.search(r"[Ѐ-ӿ]", t): return "ru"
    if re.search(r"[぀-ヿ一-鿿]", t): return "ja"
    sc = {k: sum(t.count(w) for w in ws) for k, ws in SW.items()}; k, s = max(sc.items(), key=lambda x: x[1])
    return k if s > 0 else None
TEMA_RX = [r"iwo|ivo ?jima|иводзим|硫黄島|硫磺", r"pearl harbo|перл|真珠湾", r"omaha|normand|нормандия|ノルマンディ|d-day|dia d|jour j|desembarco|desembarque|landung", r"hiroshima|hiroszima|хиросим|広島|原爆|atomic|atómic|atômic|atomi", r"area ?51|zona ?51|strefa ?51|зона ?51|エリア51|área ?51"]
FORM = {"en": r"can.?t (you )?(visit|go)|not allowed|off.?limits|forbidden|still (under|there|buried|left)|what.?s (still|left)", "es": r"no puedes visitar|no se puede (visitar|entrar)|prohibid|todav[ií]a|a[uú]n (queda|hay)|por qu[eé] (nadie|casi nadie|no)|lo que (a[uú]n|todav)",
        "pt": r"n[aã]o pode visitar|ningu[eé]m (pode|consegue)|proibid|ainda (existe|est[aá])|por que (ningu[eé]m|n[aã]o|quase)|o que (ainda|restou)", "fr": r"on ne peut pas|interdit|pourquoi (on|personne|l.[iî]le)|ce qu.il reste|encore (sous|l[aà])|toujours",
        "de": r"warum darf|nicht besuchen|verboten|gesperrt|sperrgebiet|noch heute|warum (niemand|kein)", "it": r"non si pu[oò]|vietat|perch[eé] non|cosa c.è ancora|ancora", "ru": r"почему нельзя|запрещ|закрыт|до сих пор", "pl": r"dlaczego nie|zakazan|nadal|wci[aą][zż]", "ja": r"なぜ行けない|立入禁止|今も|上陸できない", "tr": r"neden ziyaret|yasak"}
pool = collections.defaultdict(dict); allv = collections.defaultdict(dict)
for l in open(os.path.join(BASE, "dados/busca_idi.jsonl")):
    b = json.loads(l)
    if b.get("id") in V: allv[b["lang"]][b["id"]] = V[b["id"]]; pool[(b["lang"], b["tema"])][b["id"]] = V[b["id"]]
def med(x): return int(st.median(x)) if x else 0
out = {}
import importlib.util; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import queries
for l, d in queries.IDI.items():
    r = {"temas": {}}; rows = []
    for i, t in enumerate(d["temas"]):
        rx = re.compile(TEMA_RX[i], re.I)
        vs = [dict(v, id=k) for k, v in pool[(l, t)].items() if v["dur_s"] >= 240 and v["live"] in (None, "none") and lang(v) == l and rx.search(v["titulo"])]
        vs.sort(key=lambda v: -v["views"]); a26 = [v for v in vs if v["pub"] >= "2026-01-01"]
        r["temas"][t] = {"n": len(vs), "top1": vs[0]["views"] if vs else 0, "top1_t": vs[0]["titulo"][:70] if vs else "", "top10_med": med([v["views"] for v in vs[:10]]), "gt100k_2026": sum(v["views"] > 1e5 for v in a26), "gt100k": sum(v["views"] > 1e5 for v in vs), "n2026": len(a26)}
        rows += vs
    fr = re.compile(FORM[l], re.I)
    # vídeos de fórmula (consultas "formula" + todos os vídeos do idioma cujo título casa FORM e cita um dos 5 temas)
    tema_all = re.compile("|".join(TEMA_RX), re.I)
    fv = {k: dict(v, id=k) for k, v in allv[l].items() if v["dur_s"] >= 240 and lang(v) == l and fr.search(v["titulo"]) and tema_all.search(v["titulo"]) and v["live"] in (None, "none")}
    fl = sorted(fv.values(), key=lambda v: -v["views"])
    new = [v for v in fl if v["pub"] >= "2026-09-27"]
    r["formula"] = {"n": len(fl), "n_clones_desde_0927": len(new), "mediana_clones": med([v["views"] for v in new]), "max_clone": max([v["views"] for v in new], default=0),
                    "canais_clones": len({v["channel_id"] for v in new}), "top_2026": [(v["views"], v["pub"], v["titulo"][:70], v["canal"]) for v in sorted([v for v in fl if v["pub"] >= "2026-01-01"], key=lambda v: -v["views"])[:4]],
                    "clones_ex": [(v["views"], v["pub"], v["titulo"][:70], v["canal"]) for v in sorted(new, key=lambda v: -v["views"])[:4]]}
    meds = [t["top10_med"] for t in r["temas"].values() if t["n"]]
    r["resumo"] = {"mediana_top10_5temas": med(meds), "soma_gt100k_2026": sum(t["gt100k_2026"] for t in r["temas"].values()), "soma_gt100k": sum(t["gt100k"] for t in r["temas"].values()), "n_videos": len(rows)}
    loc = [dict(v, id=k) for k, v in pool[(l, "local")].items() if v["dur_s"] >= 240 and lang(v) == l]
    loc.sort(key=lambda v: -v["views"])
    r["local"] = {"n": len(loc), "top10_med": med([v["views"] for v in loc[:10]]), "gt100k_2026": sum(v["views"] > 1e5 and v["pub"] >= "2026-01-01" for v in loc), "top3": [(v["views"], v["pub"], v["titulo"][:70], v["canal"]) for v in loc[:3]]}
    out[l] = r
json.dump(out, open(os.path.join(BASE, "dados/demanda_idioma.json"), "w"), ensure_ascii=False, indent=1)
for l, r in out.items():
    print(l, r["resumo"], "| formula n", r["formula"]["n"], "clones", r["formula"]["n_clones_desde_0927"], "med", r["formula"]["mediana_clones"], "max", r["formula"]["max_clone"], "| local", r["local"]["n"], r["local"]["top10_med"])
    print("   ", {t: (v["top10_med"], v["gt100k_2026"], v["n"]) for t, v in r["temas"].items()})
