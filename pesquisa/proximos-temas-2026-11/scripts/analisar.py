"""Demanda por tema (pt / es) a partir de busca.jsonl + videos_api.json + canais_api.json.
Conta vídeo para (lang, tema) se: idioma = lang, título cita o tema (regex), duração >= 4 min, não ficção/jogo.
12 meses = publicado >= 2025-11-09; recentes = >= 2026-08-11 e > 100 mil. Saída: dados/demanda.json + stdout."""
import json, os, re, statistics, sys, collections
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/pesquisa/archive-in-minutes/idioma/scripts"))
from comum import idioma, ficcao
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = json.load(open(f"{BASE}/dados/videos_api.json")); C = json.load(open(f"{BASE}/dados/canais_api.json"))
D12, D90, NOVO = "2025-11-09", "2026-08-11", "2025-11-09"
R = lambda p: re.compile(p, re.I)
T = {"pt": {
 "roma": R(r"\broma\b|roman[oa]s?\b|c[ée]sar\b|imp[ée]rio romano"), "japao": R(r"jap[ãa]o|japon[eê]s|samurai|xogun"),
 "russia": R(r"r[úu]ssia|russo|czar|sovi[ée]t|urss"), "ucrania": R(r"ucr[âa]nia|ucranian"),
 "britanico": R(r"brit[âa]nic|inglaterra|reino unido|ingl[eê]s"), "grecia": R(r"gr[ée]cia|grego|esparta|atenas"),
 "otomano": R(r"otoman|turquia|turco"), "portugal": R(r"portugal|portugu[eê]s"), "eua": R(r"estados unidos|\beua\b|am[ée]rica do norte|americanos"),
 "mongois": R(r"mong[óo]i|mongol|genghis|gengis"), "israel": R(r"israel|judeu|palestin"), "alemanha": R(r"alemanha|alem[ãa]|pr[úu]ssia"),
 "franca": R(r"fran[çc]a|franc[eê]s"), "espanha": R(r"espanha|espanh"), "coreia": R(r"coreia"), "mexico": R(r"m[ée]xico|asteca|maias?\b"),
 "argentina": R(r"argentin"), "bizancio": R(r"bizan|constantinopla"), "vikings": R(r"viking|n[óo]rdic"), "mesopotamia": R(r"mesopot|sum[ée]ri|babil"),
 "incas": R(r"\bincas?\b"), "italia": R(r"it[áa]lia"), "cartago": R(r"cartago|an[íi]bal"), "africa": R(r"[áa]frica")},
 "es": {
 "kgb": R(r"\bkgb\b"), "templarios": R(r"templari"), "inquisicion": R(r"inquisici"), "masoneria": R(r"mas[oó]n"), "jesuitas": R(r"jesuit"),
 "condor": R(r"c[óo]ndor"), "illuminati": R(r"illuminati|iluminati"), "opusdei": R(r"opus dei"), "yakuza": R(r"yakuza"),
 "asesinos": R(r"asesinos|hashash|alamut"), "guardiasuiza": R(r"guardia suiza"), "mafiarusa": R(r"mafia rusa|bratva"),
 "stasi": R(r"\bstasi\b"), "gestapo": R(r"gestapo"), "ss": R(r"\bss\b|schutzstaffel"), "kkk": R(r"ku klux|\bkkk\b"), "eta": R(r"\beta\b"),
 "hospitalarios": R(r"orden de malta|hospitalari"), "navyseals": R(r"navy seal|\bsas\b|fuerzas especiales"), "pinkerton": R(r"pinkerton"),
 "camorra": R(r"camorra|ndrangheta|'ndrangheta"), "triadas": R(r"tr[íi]ada"), "dina": R(r"\bdina\b"), "spetsnaz": R(r"spetsnaz|nkvd"),
 "vaticano": R(r"vaticano"), "legion": R(r"legi[óo]n extranjera"), "rosacruces": R(r"rosacruz|rosacruc"), "ninjas": R(r"ninja")}}
FORM = {"pt": R(r"hist[óo]ria (inteira|completa)|toda a hist[óo]ria|em \d+ minutos"), "es": R(r"toda la historia|historia completa|historia entera|en \d+ minutos")}
EXTRA_FIC = R(r"\b(fnaf|god of war|assassin|creed|total war|civilization|age of empires|aoe|eu4|hearts of iron|hoi4|mount|bannerlord|crusader kings|ck3|fortnite|free fire|zelda|pok[eé]mon|lol|league of)\b|\bjogo|\bjuego|\bserie\b|\bs[ée]rie\b|cap[íi]tulo \d|episodio \d|\bep\.? ?\d|novela|\breels?\b|#shorts")
HIST = {"pt": R(r"hist[óo]ri|imp[ée]rio|antig|origem|document[áa]ri|dinastia|civiliza|reino|funda[çc]|guerra|batalha|\\brei\\b|rainha|imperador|czar|samurai|medieval|s[ée]culo|como .{0,30}(surgiu|nasceu|caiu|virou|se tornou|dominou|conquist)|por que .{0,40}(caiu|nunca|existe|dominou)|\\b(1[0-9]{3}|[0-9]{2,3} a\\.? ?c)"),
        "es": R(r"histori|imperio|origen|documental|orden|secret|sociedad|guerra|edad media|medieval|siglo|caballer|qu[ée] (era|fue|pas[óo])|c[óo]mo (naci|surgi|cay|se cre)|verdad|oscur|misterio|poder")}
RUIDO = R(r"copa|fifa|futebol|f[úu]tbol|sele[çc]|melhores momentos|compacto|\\bgol|\\bvs?\\.? |\\bx\\s|vlog|entrei|explorei|entramos|chegamos|viagem|viaje|\\btour\\b|4k|\\bviver\\b|vida real|podcast|cortes|\\bcorte\\b|rotina|adotei|presos|reag|react|motogp|f1\\b|noticia|not[íi]cia|hoje|ao vivo|en vivo|urgente|[úu]ltima hora|\\b202[56]\\b")
def med(xs): return int(statistics.median(xs)) if xs else 0
pool = collections.defaultdict(dict)
for vid, v in V.items():
    if v["live"] not in (None, "none") or v["dur_s"] < 240: continue
    if ficcao(v["titulo"], v["canal"]) or EXTRA_FIC.search(v["titulo"]): continue
    l = idioma(v)
    if l not in ("pt", "es"): continue
    for t, rx in T[l].items():
        if rx.search(v["titulo"]) and (l == "es" or HIST[l].search(v["titulo"])) and not RUIDO.search(v["titulo"]) and not RUIDO.search(v["canal"]): pool[(l, t)][vid] = {**v, "id": vid}
out = {}
for l in ("pt", "es"):
    for t in T[l]:
        vs = sorted(pool[(l, t)].values(), key=lambda v: -v["views"])
        a12 = [v for v in vs if v["pub"] >= D12]; rec = [v for v in vs if v["pub"] >= D90 and v["views"] > 100_000]
        mold = [v for v in vs if FORM[l].search(v["titulo"])]
        porta = []
        for v in a12:
            c = C.get(v["channel_id"], {})
            if c.get("criado", "0") >= NOVO and v["views"] > 100_000: porta.append(v)
        # concentração: canais distintos no top-10 12m
        cs = collections.Counter(v["canal"] for v in a12[:10])
        d = {"n": len(vs), "n12": len(a12), "med_top10_12m": med([v["views"] for v in a12[:10]]), "med_top10_total": med([v["views"] for v in vs[:10]]),
             "top1": (vs[0]["views"], vs[0]["titulo"], vs[0]["canal"], vs[0]["pub"]) if vs else None,
             "rec_gt100k": len(rec), "rec": [(v["views"], v["pub"], v["titulo"][:80], v["canal"]) for v in rec[:5]],
             "ano_gt100k": sum(v["views"] > 100_000 for v in a12),
             "molde": [(v["views"], v["pub"], v["titulo"][:80], v["canal"], C.get(v["channel_id"], {}).get("criado"), C.get(v["channel_id"], {}).get("insc")) for v in mold[:8]],
             "molde_12m_gt50k": sum(1 for v in mold if v["pub"] >= D12 and v["views"] > 50_000),
             "porta": [(v["views"], v["pub"], v["titulo"][:80], v["canal"], C[v["channel_id"]]["criado"], C[v["channel_id"]]["insc"]) for v in porta[:5]],
             "canais_top10_12m": len(cs),
             "top10_12m": [(v["views"], v["pub"], round(v["dur_s"]/60), v["titulo"][:80], v["canal"], v["id"]) for v in a12[:10]]}
        out[f"{l}:{t}"] = d
json.dump(out, open(f"{BASE}/dados/demanda.json", "w"), ensure_ascii=False, indent=1)
for l in ("pt", "es"):
    print(f"\n== {l} ==  tema | n12 | med12 | medTot | ano>100k | rec>100k | molde12m>50k | porta")
    for k, d in sorted(((k, d) for k, d in out.items() if k.startswith(l)), key=lambda x: -x[1]["med_top10_12m"]):
        print(f"{k:18} {d['n12']:4} {d['med_top10_12m']:>10,} {d['med_top10_total']:>10,} {d['ano_gt100k']:3} {d['rec_gt100k']:3} {d['molde_12m_gt50k']:3} {len(d['porta'])}")
