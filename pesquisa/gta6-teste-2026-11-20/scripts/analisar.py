"""Etapa 4: corpus.csv + tabelas para o RELATORIO (dados/analise.json e stdout)."""
import json, os, csv, re, statistics, datetime as dt

B = os.path.join(os.path.dirname(__file__), "..")
D = os.path.join(B, "dados")
NOW = dt.datetime(2026, 11, 20, 18, tzinfo=dt.timezone.utc)  # 15:00 BRT
v = json.load(open(os.path.join(D, "videos.json"))); c = json.load(open(os.path.join(D, "canais.json")))
m = json.load(open(os.path.join(D, "medianas.json")))

def formato(t, dur):
    t = t.lower()
    if dur <= 180: return "short"
    if re.search(r"\b(review|gameplay|walkthrough|part \d|mission|first impression|i played|playing|live|stream|reaction|react|tips|tricks|guide|how to|best way|money|glitch|cheat|mod|ps5|xbox|unboxing|my |we |hours? in|day \d|1st|beginner|settings|i tried|i spent|i visited)", t):
        return "jogar/rosto"
    if re.search(r"\b(news|update|leak|leaked|trailer \d|countdown|official|confirmed|release date|pre-?load|price|rumou?r)", t) and not re.search(r"(history|story|explained|documentary|why|how)", t):
        return "news"
    if re.search(r"(real life|vs real|vs\.? real|irl|real world|real locations|in real|miami|florida|everglades|keys\b)", t):
        return "lugares-reais"
    if re.search(r"(history|story of|documentary|why .*(took|so long|delay)|how .*(made|became|rockstar)|rise|untold|inside|billion|budget|cost|record|hacker|leak|biggest|took \d+ years|years)", t):
        return "historia-hype"
    if re.search(r"(explained|lore|story|ending|every|secrets?|details|easter|things you|missed|hidden|map|theory|analysis|breakdown|facts)", t):
        return "explicativo/lista"
    return "outro"

rows = []
for x in v.values():
    pub = dt.datetime.fromisoformat(x["publicado"].replace("Z", "+00:00"))
    h = max((NOW - pub).total_seconds() / 3600, 1)
    ch = c.get(x["canal_id"], {}); md = m.get(x["canal_id"]) or {}
    med = md.get("mediana_longos") or md.get("mediana_todos")
    rows.append({
        "id": x["id"], "url": "https://youtu.be/" + x["id"], "titulo": x["titulo"], "canal": x["canal"], "canal_id": x["canal_id"],
        "inscritos": ch.get("inscritos"), "canal_criado": (ch.get("criado") or "")[:10], "publicado": x["publicado"][:16],
        "idade_h": round(h, 1), "idade_d": round(h / 24, 1), "views": x["views"], "views_h": round(x["views"] / h, 1),
        "views_d": round(x["views"] / h * 24), "mediana_canal": med, "x_mediana": round(x["views"] / med, 2) if med else None,
        "duracao_min": round(x["duracao_s"] / 60, 1), "formato": formato(x["titulo"], x["duracao_s"]),
        "gta6": int(bool(re.search(r"gta ?(6|vi)\b|grand theft auto (6|vi)\b|leonida|vice city", x["titulo"].lower()))),
        "gta5": int(bool(re.search(r"gta ?(5|v)\b|grand theft auto (5|v)\b|los santos|san andreas", x["titulo"].lower()))),
        "idioma": x["idioma"] or "", "grupos": "|".join(x["grupos"]), "queries": " | ".join(x["queries"]),
    })
rows.sort(key=lambda r: -r["views_d"])
with open(os.path.join(B, "corpus.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def en(r): return (r["idioma"] or "en").startswith("en") or r["idioma"] == ""
g6 = [r for r in rows if r["gta6"] and en(r) and r["formato"] != "short"]
rec30 = [r for r in g6 if r["idade_d"] <= 30]
rec7 = [r for r in g6 if r["idade_d"] <= 7]
out = {}
def tab(lst, n=15):
    return [{k: r[k] for k in ("id", "titulo", "canal", "inscritos", "views", "idade_d", "views_d", "x_mediana", "duracao_min", "formato")} for r in lst[:n]]
out["top7"] = tab(sorted(rec7, key=lambda r: -r["views_d"]), 25)
out["top30"] = tab(sorted(rec30, key=lambda r: -r["views_d"]), 25)
# por formato (30 d)
fmt = {}
for r in rec30:
    fmt.setdefault(r["formato"], []).append(r)
out["formatos30"] = {k: {"n": len(l), "mediana_views": statistics.median([r["views"] for r in l]),
                         "mediana_views_d": statistics.median([r["views_d"] for r in l]),
                         "mediana_xmed": statistics.median([r["x_mediana"] for r in l if r["x_mediana"]] or [0]),
                         "pct_5x": round(100 * sum(1 for r in l if (r["x_mediana"] or 0) >= 5) / len(l))} for k, l in fmt.items()}
# brechas: canais pequenos/médios (< 250k inscritos), >= 5x mediana, 30 d
br = [r for r in rec30 if (r["x_mediana"] or 0) >= 5 and (r["inscritos"] or 0) < 250000 and r["views"] >= 5000]
out["brechas"] = tab(sorted(br, key=lambda r: -r["x_mediana"]), 40)
out["brechas_por_formato"] = {}
for r in br: out["brechas_por_formato"][r["formato"]] = out["brechas_por_formato"].get(r["formato"], 0) + 1
# por grupo de busca (30 d), outliers
for g in ("lugares", "hype", "lore", "geral"):
    l = [r for r in rec30 if g in r["grupos"]]
    out["grupo_" + g] = {"n": len(l), "mediana_views": statistics.median([r["views"] for r in l]) if l else 0,
                         "n_5x": sum(1 for r in l if (r["x_mediana"] or 0) >= 5),
                         "top": tab(sorted(l, key=lambda r: -r["views_d"]), 12)}
# evergreen GTA 5 (> 1 ano)
g5 = [r for r in rows if r["gta5"] and r["idade_d"] > 365 and r["formato"] != "short" and en(r)]
for r in g5: r["views_d_vida"] = r["views_d"]
out["gta5_evergreen"] = tab(sorted(g5, key=lambda r: -r["views"]), 20)
fg5 = {}
for r in g5: fg5.setdefault(r["formato"], []).append(r["views"])
out["gta5_formatos"] = {k: {"n": len(l), "mediana": statistics.median(l)} for k, l in fg5.items()}
# GTA 6 antigos (> 180 d) que seguiram acumulando: lugares/historia
old6 = [r for r in g6 if r["idade_d"] > 180]
fo = {}
for r in old6: fo.setdefault(r["formato"], []).append(r["views"])
out["gta6_antigos_formatos"] = {k: {"n": len(l), "mediana": statistics.median(l)} for k, l in fo.items()}
out["gta6_antigos_top"] = tab(sorted([r for r in old6 if r["formato"] in ("lugares-reais", "historia-hype", "explicativo/lista")], key=lambda r: -r["views"]), 15)
# saturação
sat = {}
for f in os.listdir(D):
    if f.startswith("sat-"):
        try: sat[f] = len(json.load(open(os.path.join(D, f)))["entries"])
        except Exception: pass
out["saturacao"] = sat
out["n"] = {"corpus": len(rows), "gta6_en_longos": len(g6), "rec30": len(rec30), "rec7": len(rec7)}
json.dump(out, open(os.path.join(D, "analise.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: out[k] for k in ("n", "formatos30", "brechas_por_formato", "saturacao", "gta5_formatos", "gta6_antigos_formatos")}, ensure_ascii=False, indent=1))
for g in ("lugares", "hype", "lore", "geral"):
    print(g, {k: out["grupo_" + g][k] for k in ("n", "mediana_views", "n_5x")})
