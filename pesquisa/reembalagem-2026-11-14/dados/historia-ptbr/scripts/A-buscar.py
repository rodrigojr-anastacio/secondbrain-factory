"""Busca yt-dlp via WARP (0 cota) para Egito/Índia/China/Brasil (historia-ptbr, pesquisador A).
2 ordens: relevância (ytsearch40) e 'este ano por views' (sp=CAMSAggF). Saída: ../A-busca.jsonl"""
import json, os, sys, subprocess, urllib.parse
from concurrent.futures import ThreadPoolExecutor
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YTDLP = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
Q = {
 ("pt","egito"): ["história do egito", "história do egito antigo", "a história inteira do egito", "egito antigo documentário", "por que o egito"],
 ("pt","india"): ["história da índia", "a história inteira da índia", "história da índia antiga", "por que a índia"],
 ("pt","china"): ["história da china", "a história inteira da china", "história da china antiga", "por que a china"],
 ("pt","brasil"): ["história do brasil", "a história inteira do brasil", "história do brasil resumo", "por que o brasil", "como o brasil"],
 ("en","egito"): ["history of egypt", "entire history of egypt"],
 ("en","india"): ["history of india", "entire history of india"],
 ("en","china"): ["history of china", "entire history of china"],
 ("en","brasil"): ["history of brazil"],
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
with open(os.path.join(BASE, "A-busca.jsonl"), "w") as f, ThreadPoolExecutor(4) as ex:
    for (l, t, q, o), vs in ex.map(rodar, qs):
        if vs is None: erros += 1; print("ERRO", q, o, file=sys.stderr); continue
        for i, v in enumerate(vs): f.write(json.dumps({"lang": l, "tema": t, "q": q, "ordem": o, "pos": i, **v}, ensure_ascii=False) + "\n")
print("erros", erros, file=sys.stderr)
