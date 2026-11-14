"""Busca yt-dlp via WARP (0 cota) para Egito/Índia/China/Brasil (historia-ptbr, pesquisador A).
2 ordens: relevância (ytsearch40) e 'este ano por views' (sp=CAMSAggF). Saída: ../A-busca3.jsonl"""
import json, os, sys, subprocess, urllib.parse
from concurrent.futures import ThreadPoolExecutor
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YTDLP = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
Q = {
 ("pt","india"): ["companhia das índias orientais", "koh-i-noor diamante história", "como a inglaterra dominou a índia", "por que a índia é pobre", "índia mil anos de história"],
 ("pt","padrao"): ["mil anos de história em minutos", "o dia em que o brasil", "por que nunca abriram", "a história inteira em minutos", "como um império"],
}
def rodar(item):
    lang, tema, q, ordem = item
    alvo = f"ytsearch40:{q}" if ordem == "relevancia" else "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + "&sp=CAMSAggF"
    for _ in range(2):
        r = subprocess.run([YTDLP, "--proxy", "socks5://127.0.0.1:40000", "--flat-playlist", "-J", "--playlist-end", "40", alvo], capture_output=True, text=True, timeout=180)
        if not r.returncode: break
    if r.returncode: return item, None
    return item, [{k: e.get(k) for k in ("id", "title", "channel", "channel_id", "view_count", "duration")} for e in json.loads(r.stdout).get("entries") or []]
qs = [(l, t, q, o) for (l, t), qq in Q.items() for q in qq for o in ("relevancia", "ano_views")]
print(len(qs), "consultas", file=sys.stderr)
erros = 0
with open(os.path.join(BASE, "A-busca3.jsonl"), "w") as f, ThreadPoolExecutor(4) as ex:
    for (l, t, q, o), vs in ex.map(rodar, qs):
        if vs is None: erros += 1; print("ERRO", q, o, file=sys.stderr); continue
        for i, v in enumerate(vs): f.write(json.dumps({"lang": l, "tema": t, "q": q, "ordem": o, "pos": i, **v}, ensure_ascii=False) + "\n")
print("erros", erros, file=sys.stderr)
