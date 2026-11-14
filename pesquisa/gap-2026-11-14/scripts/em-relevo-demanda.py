"""Demanda rápida (US$ 0): busca do YouTube via yt-dlp + WARP, top-15 por relevância; mediana de views e nº >=100 mil.
Uso: python -I em-relevo-demanda.py saida.json"""
import json, subprocess, sys, statistics, os
VENV = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin")
Q = ["aquífero guarani", "por que neva no sul do brasil", "furacão catarina 2004", "enchente rio grande do sul 2024",
     "seca de 1877", "el niño 1983 enchente", "geada negra 1975", "ciclone bomba sul", "litoral do rio grande do sul",
     "lagoa dos patos", "cânions do sul do brasil", "tornado no brasil", "por que o sul do brasil", "clima do sul do brasil",
     "el niño 2026"]
res = []
for q in Q:
    r = subprocess.run([f"{VENV}/yt-dlp", "--proxy", "socks5://127.0.0.1:40000", "--flat-playlist", "-J", "--no-warnings",
                        f"ytsearch15:{q}"], capture_output=True, text=True, timeout=180)
    try: ents = json.loads(r.stdout).get("entries", [])
    except Exception: ents = []
    v = [(e.get("view_count") or 0, e.get("title"), e.get("channel"), e.get("duration")) for e in ents]
    longos = [x for x in v if (x[3] or 0) > 180]
    vs = [x[0] for x in longos] or [0]
    top = sorted(longos, reverse=True)[:3]
    res.append({"q": q, "n_longos": len(longos), "mediana_longos": int(statistics.median(vs)), "n_100k": sum(1 for x in vs if x >= 100000), "top3": top})
    print(q, len(longos), int(statistics.median(vs)), sum(1 for x in vs if x >= 100000), top[:1])
json.dump(res, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
