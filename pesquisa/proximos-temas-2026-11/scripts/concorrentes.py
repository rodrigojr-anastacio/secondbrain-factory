"""Uploads dos concorrentes no molde (yt-dlp via WARP) + videos.list para título original, data e views. Saída: dados/concorrentes.json"""
import json, os, sys, subprocess
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, segundos, chunks
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YTDLP = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
CH = {"pt": {"Crônicas de Ferro": "UCKx1OcYY6zFNl8v05ujzjsA", "Genius History": "UC-q0RDBWjYlYA2KkPzq0WSQ", "History in Minutes (en)": "UCYjRQ6T2BxBnJtPytI9OnNg",
             "CountryCorns": "UCKWRnsyYbPFgWclCF0_yOTw", "História em minutos (clone 08/2026)": "UCuquAW2-sxlV0G4N9RuvqaQ", "História na Marra": "UCintxLG3w6pzNQ7Dh8w3-CQ",
             "História em Minutos (clone 10/2026a)": "UCyOrXqAEQpKKHreTYqOqdEw", "História em Minutos (clone 10/2026b)": "UCvVuEJAqFAgqtn1IbA11UQw",
             "História em Minutos (clone 10/2026c)": "UCTJ5pQhUbm6CyszLfqR8Urg", "Era Humana": "UC3eSoWi534-hqfJfWKSkzTQ"},
      "es": {"Atlas del Tiempo": "UCku9KB11TReyHHC1kK9CCEw", "Te lo Pinto": "UCrkONla60pQPsppl7PPDHyQ", "Archivos en Minutos": "UCbsAjBx3waufmBhdZSwFMGQ",
             "Mapa del Ayer": "UC4A_eQiXs8-ESgVmyxNUMGw", "Aprendes Mientras Duermes": "UCCST8_H3CCGBGwufX8XbSzg", "Archive in Minutes (en)": "UCFp0Rk-ad8JD78Qw9nEJ29w",
             "Spies in Minutes (en)": "UC8a5fGoL5nfy5qdeup7mFGw"}}
yt = yt_client(); un = 0; out = {}
for l, d in CH.items():
    for nome, cid in d.items():
        r = subprocess.run([YTDLP, "--proxy", "socks5://127.0.0.1:40000", "--flat-playlist", "-J", "--playlist-end", "300", f"https://www.youtube.com/channel/{cid}/videos"], capture_output=True, text=True, timeout=300)
        ids = [e["id"] for e in (json.loads(r.stdout).get("entries") or [])] if not r.returncode else []
        vs = []
        for g in chunks(ids):
            rr = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(g), maxResults=50).execute(); un += 1
            for it in rr.get("items", []):
                dd = it["contentDetails"].get("duration")
                vs.append({"id": it["id"], "titulo": it["snippet"]["title"], "pub": it["snippet"]["publishedAt"][:10], "views": int(it.get("statistics", {}).get("viewCount", 0)), "dur_s": segundos(dd) if dd else 0})
        out[nome] = {"lang": l, "channel_id": cid, "videos": sorted(vs, key=lambda v: -v["views"])}
        print(nome, len(ids), file=sys.stderr)
json.dump(out, open(f"{BASE}/dados/concorrentes.json", "w"), ensure_ascii=False, indent=1)
print("unidades", un, file=sys.stderr)
