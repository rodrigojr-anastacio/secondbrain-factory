"""Demanda en por tema: pool = resultados das 5 consultas do tema; filtros: duração >= 4 min, não live, título cita o tema (regex), idioma en.
Saída: dados/demanda_en.json + tabela no stdout."""
import json, os, re, statistics as st, sys, collections
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = json.load(open(os.path.join(BASE, "dados/videos_api.json")))
RX = {"iwo jima": r"iwo", "midway": r"midway", "corregidor": r"corregidor", "tinian": r"tinian", "bikini": r"bikini", "hashima": r"hashima|battleship island|gunkanjima",
 "pearl harbor": r"pearl harbo|uss arizona", "omaha": r"omaha|normandy|d-day|dday", "okinawa": r"okinawa", "peleliu": r"peleliu", "truk": r"truk|chuuk", "kwajalein": r"kwajalein",
 "wake": r"wake island", "guadalcanal": r"guadalcanal", "alcatraz": r"alcatraz", "johnston": r"johnston atoll|johnston island", "diego garcia": r"diego garcia", "area 51": r"area 51|area51",
 "cheyenne": r"cheyenne mountain|norad", "camp century": r"camp century|iceworm", "runit": r"runit|enewetak|eniwetok", "pointe du hoc": r"pointe du hoc", "gettysburg": r"gettysburg",
 "antietam": r"antietam", "fort sumter": r"fort sumter|sumter", "lincoln": r"lincoln", "appomattox": r"appomattox", "andersonville": r"andersonville", "north brother": r"north brother",
 "fort jefferson": r"fort jefferson|dry tortugas", "bastogne": r"bastogne", "hiroshima": r"hiroshima|nagasaki", "chernobyl": r"chernobyl|pripyat", "falklands": r"falkland|malvinas"}
# pontuação de idioma en: título ascii-ish
def en(v):
    a = (v.get("audio") or v.get("lang") or "")[:2].lower()
    if a: return a == "en"
    return not re.search(r"[^\x00-\x7f’‘“”–—…]", v["titulo"])
pool = collections.defaultdict(dict)
for l in open(os.path.join(BASE, "dados/busca_dem.jsonl")):
    b = json.loads(l)
    if b.get("id") and b["id"] in V: pool[b["tema"]][b["id"]] = V[b["id"]]
ANO = "2025-11-12"; out = {}
def med(x): return int(st.median(x)) if x else 0
for k, rx in RX.items():
    r = re.compile(rx, re.I)
    vs = [dict(v, id=i) for i, v in pool[k].items() if v["dur_s"] >= 240 and v["live"] in (None, "none") and en(v) and r.search(v["titulo"])]
    vs.sort(key=lambda v: -v["views"]); ano = [v for v in vs if v["pub"] >= ANO]
    BAT = re.compile(r"battle|invasion|campaign|attack|\bwar\b|1941|1942|1943|1944|1945|assault|raid|massacre|surrender|assassinat|killed|shot|operation|d-day|history buffs|animated|vs\.?|\bwwii\b|world war|mrbeast|i spent|escape|how to|vlog|travel guide|full movie|reaction|prank", re.I)
    lug = [v for v in vs if not BAT.search(v["titulo"])]; lug_ano = [v for v in lug if v["pub"] >= ANO]
    why = [v for v in vs if re.search(r"can.?t (you )?(visit|go|enter|land)|not allowed|off.?limits|forbidden|banned|why .*(still|no one)", v["titulo"], re.I)]
    out[k] = {"n": len(vs), "top10_med": med([v["views"] for v in vs[:10]]), "top1": vs[0]["views"] if vs else 0, "top1_t": vs[0]["titulo"][:80] if vs else "", "top1_c": vs[0]["canal"] if vs else "", "top1_id": vs[0]["id"] if vs else "",
              "gt100k": sum(v["views"] > 1e5 for v in vs), "gt100k_ano": sum(v["views"] > 1e5 for v in ano), "gt1m": sum(v["views"] > 1e6 for v in vs), "ano_n": len(ano), "ano_top10_med": med([v["views"] for v in ano[:10]]),
              "lug_n": len(lug), "lug_top10_med": med([v["views"] for v in lug[:10]]), "lug_gt100k_ano": sum(v["views"] > 1e5 for v in lug_ano), "lug_gt100k": sum(v["views"] > 1e5 for v in lug), "lug_top3": [(v["views"], v["pub"], v["titulo"][:70], v["canal"], v["id"]) for v in lug[:3]], "why_n": len(why), "why_top": [(v["views"], v["pub"], v["titulo"][:70], v["canal"]) for v in sorted(why, key=lambda v: -v["views"])[:3]],
              "top5": [(v["views"], v["pub"], v["titulo"][:70], v["canal"], v["id"]) for v in vs[:5]]}
json.dump(out, open(os.path.join(BASE, "dados/demanda_en.json"), "w"), ensure_ascii=False, indent=1)
print("== por 'lugar hoje' (sem batalha/ataque/vlog)")
for k, d in sorted(out.items(), key=lambda x: -x[1]["lug_top10_med"]): print(f'{k:14} n={d["lug_n"]:>3} med10={d["lug_top10_med"]:>9,} >100k={d["lug_gt100k"]:>3} ano={d["lug_gt100k_ano"]:>3} top: {d["lug_top3"][0][0] if d["lug_top3"] else 0:,} {d["lug_top3"][0][2] if d["lug_top3"] else ""} [{d["lug_top3"][0][3] if d["lug_top3"] else ""}]')
print(f'{"tema":14} {"n":>3} {"top10med":>9} {"top1":>10} {">100k":>5} {">100k/ano":>9} {">1m":>4} {"why":>3}  top1')
for k, d in sorted(out.items(), key=lambda x: -x[1]["top10_med"]):
    print(f'{k:14} {d["n"]:>3} {d["top10_med"]:>9,} {d["top1"]:>10,} {d["gt100k"]:>5} {d["gt100k_ano"]:>9} {d["gt1m"]:>4} {d["why_n"]:>3}  {d["top1_t"]} [{d["top1_c"]}]')
