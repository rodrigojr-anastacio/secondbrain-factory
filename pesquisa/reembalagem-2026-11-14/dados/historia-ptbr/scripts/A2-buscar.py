"""Rodada 2 (reescrita): buscas yt-dlp via WARP (0 cota): colisão dos títulos e referências novas.
Uso: A2-buscar.py <saida.jsonl> "q1" "q2" ...  (ytsearch30 por relevância + 'este ano por views')"""
import json, os, sys, subprocess, urllib.parse
from concurrent.futures import ThreadPoolExecutor
YTDLP = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
out, qs = sys.argv[1], sys.argv[2:]
def rodar(item):
    q, ordem = item
    alvo = f"ytsearch30:{q}" if ordem == "rel" else "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + "&sp=CAMSAggF"
    for _ in range(2):
        r = subprocess.run([YTDLP, "--proxy", "socks5://127.0.0.1:40000", "--flat-playlist", "-J", "--playlist-end", "30", alvo], capture_output=True, text=True, timeout=180)
        if not r.returncode: break
    if r.returncode: return item, None
    return item, [{k: e.get(k) for k in ("id", "title", "channel", "channel_id", "view_count", "duration")} for e in json.loads(r.stdout).get("entries") or []]
items = [(q, o) for q in qs for o in ("rel", "ano")]
with open(out, "a") as f, ThreadPoolExecutor(4) as ex:
    for (q, o), vs in ex.map(rodar, items):
        if vs is None: print("ERRO", q, o, file=sys.stderr); continue
        for i, v in enumerate(vs): f.write(json.dumps({"q": q, "ordem": o, "pos": i, **v}, ensure_ascii=False) + "\n")
