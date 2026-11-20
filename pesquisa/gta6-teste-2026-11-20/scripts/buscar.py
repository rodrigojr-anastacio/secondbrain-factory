"""Etapa 1: buscas yt-dlp (via WARP) -> dados/busca.jsonl (ids + query)."""
import json, subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor

YTDLP = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
OUT = os.path.join(os.path.dirname(__file__), "..", "dados", "busca.jsonl")
PROXY = "socks5://127.0.0.1:40000"

Q = {
    # geral / hype
    "geral": ["GTA 6", "GTA 6 launch", "GTA 6 sales record", "GTA 6 review", "GTA 6 gameplay", "GTA 6 news",
              "GTA 6 first impressions", "GTA 6 secrets", "GTA 6 easter eggs", "GTA 6 map size", "GTA 6 map explained",
              "GTA 6 things you missed", "GTA 6 documentary", "GTA 6 explained"],
    # lugares reais
    "lugares": ["GTA 6 real life locations", "GTA 6 vs real life", "GTA 6 Vice City vs Miami", "GTA 6 Leonida real places",
                "GTA 6 Everglades real", "GTA 6 Florida Keys real", "GTA 6 map vs Florida", "GTA 6 military base Florida",
                "GTA 6 real places comparison", "Vice City real Miami locations"],
    # historia do hype
    "hype": ["why GTA 6 took so long", "GTA 6 development history", "GTA 6 leak 2022 story", "GTA 6 hacker Arion Kurtaj",
             "GTA 6 budget cost", "history of GTA 6", "GTA 6 delay story", "Rockstar Games history documentary",
             "GTA 6 trailer record views", "how GTA 6 made 2 billion"],
    # lore / real
    "lore": ["GTA 6 Jason Lucia real story", "GTA 6 Bonnie and Clyde real couple", "GTA 6 Florida man real",
             "GTA 6 real crimes inspired", "GTA 6 story explained", "GTA 6 lore explained", "GTA 6 Florida memes real",
             "real people GTA 6 parodies", "GTA 6 Lucia Jason story explained"],
    # evergreen GTA 5
    "gta5": ["GTA 5 real life locations", "GTA 5 Los Santos vs Los Angeles", "GTA V vs real life",
             "GTA 5 history documentary", "GTA 5 lore explained", "GTA San Andreas real life locations"],
}

def run(args):
    grupo, q, modo = args
    n = 40
    import urllib.parse
    url = (f"ytsearch{n}:{q}" if modo == "rel" else
           "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(q) + "&sp=EgIIBQ%253D%253D")
    try:
        p = subprocess.run([YTDLP, "--proxy", PROXY, "--flat-playlist", "-J", "--no-warnings", "--playlist-end", str(n), url],
                           capture_output=True, text=True, timeout=180)
        d = json.loads(p.stdout)
        return [{"id": e["id"], "grupo": grupo, "query": q, "modo": modo, "titulo": e.get("title"),
                 "canal": e.get("channel"), "canal_id": e.get("channel_id")} for e in d.get("entries", []) if e.get("id")]
    except Exception as ex:
        print("ERRO", q, modo, ex, file=sys.stderr)
        return []

jobs = []
for g, qs in Q.items():
    for q in qs:
        jobs.append((g, q, "rel"))
        if g != "gta5":
            jobs.append((g, q, "mes"))
with ThreadPoolExecutor(6) as ex, open(OUT, "w") as f:
    tot = 0
    for res in ex.map(run, jobs):
        for r in res:
            f.write(json.dumps(r, ensure_ascii=False) + "\n"); tot += 1
print("linhas", tot, "buscas", len(jobs))
