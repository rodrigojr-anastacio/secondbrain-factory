"""Demanda no nicho clima extremo: buscas nativas via yt-dlp + WARP (0 cota).
Ordens: relevancia (all-time), mes_views (sp=CAMSAggE), ano_views (sp=CAMSAggF).
Uso: buscar.py <lang,...>  -> dados/busca.jsonl (append)"""
import json, os, sys, subprocess, urllib.parse
from concurrent.futures import ThreadPoolExecutor
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YTDLP = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
N = 25
Q = {
 "pt": [("brasil", "tornado santa catarina"), ("brasil", "tornados no brasil"), ("brasil", "por que tantos tornados no brasil"),
        ("brasil", "clima no sul do brasil"), ("brasil", "ciclone extratropical"), ("brasil", "enchente rio grande do sul"),
        ("brasil", "corredor dos tornados brasil"), ("geral", "eventos climáticos extremos"), ("geral", "como se forma um tornado"),
        ("geral", "maiores desastres naturais da história"), ("geral", "furacão explicado"), ("geral", "o que está acontecendo com o clima"),
        ("geral", "tornado mais forte do mundo"), ("geral", "fenômenos naturais impressionantes")],
 "en": [("brasil", "tornadoes in brazil"), ("brasil", "brazil tornado 2026"), ("geral", "extreme weather explained"),
        ("geral", "how tornadoes form"), ("geral", "deadliest natural disasters in history"), ("geral", "hurricane explained"),
        ("geral", "why is the weather so extreme"), ("geral", "strongest tornado ever recorded"), ("geral", "natural disaster documentary"),
        ("geral", "what happened tornado outbreak"), ("geral", "tornado alley explained"), ("geral", "weather phenomena explained")],
 "es": [("brasil", "tornado en brasil"), ("brasil", "tornados en argentina"), ("geral", "clima extremo"), ("geral", "por qué hay tantos tornados"),
        ("geral", "cómo se forma un tornado"), ("geral", "desastres naturales más grandes de la historia"), ("geral", "huracán explicado"),
        ("geral", "fenómenos naturales explicados"), ("geral", "qué está pasando con el clima"), ("geral", "dana valencia explicada")],
 "fr": [("brasil", "tornade brésil"), ("geral", "phénomènes météo extrêmes"), ("geral", "comment se forme une tornade"),
        ("geral", "pires catastrophes naturelles de l'histoire"), ("geral", "ouragan expliqué"), ("geral", "climat extrême pourquoi")],
 "de": [("brasil", "Tornado Brasilien"), ("geral", "Extremwetter erklärt"), ("geral", "wie entsteht ein Tornado"),
        ("geral", "schlimmste Naturkatastrophen der Geschichte"), ("geral", "Hurrikan erklärt"), ("geral", "Unwetter Doku")],
 "hi": [("geral", "tornado kaise banta hai"), ("geral", "natural disasters in hindi")],
 "it": [("geral", "come si forma un tornado"), ("geral", "peggiori disastri naturali")],
 "pl": [("geral", "jak powstaje tornado")],
}
SP = {"relevancia": "", "mes_views": "&sp=CAMSAggE", "ano_views": "&sp=CAMSAggF"}
def rodar(item):
    lang, grupo, q, ordem = item
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + SP[ordem]
    for _ in range(2):
        try:
            r = subprocess.run([YTDLP, "--proxy", "socks5://127.0.0.1:40000", "--extractor-args", f"youtube:lang={lang}", "--flat-playlist", "-J",
                                "--playlist-end", str(N), url], capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            continue
        if r.returncode == 0:
            return item, [{k: e.get(k) for k in ("id", "title", "channel", "channel_id", "view_count", "duration")} for e in json.loads(r.stdout).get("entries") or []]
    return item, None
langs = sys.argv[1].split(",")
qs = [(l, g, q, o) for l in langs for g, q in Q[l] for o in SP]
erros = 0
with ThreadPoolExecutor(6) as ex, open(os.path.join(BASE, "dados", "busca.jsonl"), "a") as f:
    for (lang, grupo, q, ordem), res in ex.map(rodar, qs):
        if res is None:
            erros += 1; print("ERRO", lang, q, ordem, file=sys.stderr); continue
        for pos, e in enumerate(res):
            f.write(json.dumps({"lang": lang, "grupo": grupo, "q": q, "ordem": ordem, "pos": pos, **e}, ensure_ascii=False) + "\n")
print(len(qs), "consultas,", erros, "erros")
