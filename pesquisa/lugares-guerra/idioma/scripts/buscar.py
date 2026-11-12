"""Executa consultas (grupo: conc|dem|idi) via yt-dlp + WARP (0 cota). Append em dados/busca_<grupo>.jsonl; retoma pulando o que já foi feito.
Uso: buscar.py <grupo> [N_threads] [limite_s]"""
import json, os, sys, subprocess, urllib.parse, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import queries
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YTDLP = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
SP = {"ano_views": "&sp=CAMSAggF", "data": "&sp=CAI%253D", "relevancia": ""}
grupo = sys.argv[1]; nth = int(sys.argv[2]) if len(sys.argv) > 2 else 4; limite = int(sys.argv[3]) if len(sys.argv) > 3 else 520
N = 30 if grupo != "dem" else 25
fn = os.path.join(BASE, f"dados/busca_{grupo}.jsonl")
feitos = set()
if os.path.exists(fn):
    for l in open(fn): b = json.loads(l); feitos.add((b["lang"], b["q"], b["ordem"]))
its = [i for i in getattr(queries, grupo)() if (i[1], i[4], i[5]) not in feitos]
# consultas sem resultado também contam como feitas: marcador
t0 = time.time(); erros = 0
def rodar(it):
    if time.time() - t0 > limite: return it, "SKIP"
    g, l, tema, tipo, q, o = it
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + SP[o]
    for _ in range(2):
        try:
            r = subprocess.run([YTDLP, "--proxy", "socks5://127.0.0.1:40000", "--extractor-args", f"youtube:lang={l if l in ('en','es','pt','fr','de','it','ru','pl','ja','tr') else 'en'}", "--flat-playlist", "-J",
                                "--playlist-end", str(N), url], capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired: continue
        if r.returncode == 0:
            return it, [{k: e.get(k) for k in ("id", "title", "channel", "channel_id", "view_count", "duration")} for e in json.loads(r.stdout).get("entries") or []]
    return it, None
n_ok = 0
with open(fn, "a") as f, ThreadPoolExecutor(nth) as ex:
    for it, vs in ex.map(rodar, its):
        g, l, tema, tipo, q, o = it
        if vs == "SKIP": continue
        if vs is None: erros += 1; print("ERRO", l, q, o, file=sys.stderr); continue
        n_ok += 1
        if not vs: f.write(json.dumps({"grupo": g, "lang": l, "tema": tema, "tipo": tipo, "q": q, "ordem": o, "pos": -1, "id": None}, ensure_ascii=False) + "\n")
        for i, v in enumerate(vs): f.write(json.dumps({"grupo": g, "lang": l, "tema": tema, "tipo": tipo, "q": q, "ordem": o, "pos": i, **v}, ensure_ascii=False) + "\n")
        f.flush()
print(f"{grupo}: pendentes {len(its)} ok {n_ok} erros {erros} t={int(time.time()-t0)}s", file=sys.stderr)
