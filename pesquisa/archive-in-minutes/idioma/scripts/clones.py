"""Descoberta de canais da fórmula (clones) por idioma: busca "fórmula + organização" ordenada por DATA DE ENVIO (sp=CAI%3D)
e por relevância, via yt-dlp + WARP (0 cota). Saída: dados/busca_clones.jsonl"""
import json, os, sys, subprocess, urllib.parse
from concurrent.futures import ThreadPoolExecutor
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YTDLP = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
ORGS = {"kgb": "KGB", "cia": "CIA", "mossad": "Mossad", "stasi": "Stasi", "gestapo": "Gestapo", "ss": "SS", "mi6": "MI6"}
MOLDE = {"en": "entire history of the {} in minutes", "es": "historia completa de la {} en minutos", "pt": "história inteira da {} em minutos",
         "fr": "histoire complète {} en minutes", "de": "ganze Geschichte der {} in Minuten", "it": "intera storia {} in minuti",
         "pl": "cała historia {} w minut", "ru": "вся история {} за минут", "tr": "{} tüm tarihi dakikada", "ja": "{}の全歴史",
         "ar": "التاريخ الكامل {}", "hi": "{} complete history in hindi"}
NATIVO = {"ru": {"kgb": "КГБ", "cia": "ЦРУ", "mossad": "Моссад", "stasi": "Штази", "gestapo": "гестапо", "ss": "СС", "mi6": "МИ-6"},
          "ja": {"mossad": "モサド", "gestapo": "ゲシュタポ", "stasi": "シュタージ"}}
EXTRA = {"es": ["toda la historia de la KGB en minutos", "toda la historia de en minutos"], "pt": ["a história completa da KGB em minutos", "toda a história em minutos"],
         "fr": ["toute l'histoire du KGB en minutes"], "de": ["die gesamte Geschichte des KGB in Minuten"], "it": ["tutta la storia del KGB in minuti"],
         "en": ["the entire history of the mafia in minutes"]}
def itens():
    for l, m in MOLDE.items():
        orgs = ORGS if l in ("en", "es", "pt", "fr", "de", "it", "pl") else {k: ORGS[k] for k in ("kgb", "cia", "mossad", "gestapo")}
        for k, o in orgs.items():
            q = m.format(NATIVO.get(l, {}).get(k, o))
            yield l, k, q, "data"
            if l in ("es", "pt", "fr", "de", "it"): yield l, k, q, "relevancia"
        for q in EXTRA.get(l, []): yield l, "extra", q, "data"
def rodar(item):
    l, k, q, o = item
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + ("&sp=CAI%253D" if o == "data" else "")
    for _ in range(2):
        try:
            r = subprocess.run([YTDLP, "--proxy", "socks5://127.0.0.1:40000", "--extractor-args", f"youtube:lang={l}", "--flat-playlist", "-J",
                                "--playlist-end", "40", url], capture_output=True, text=True, timeout=150)
        except subprocess.TimeoutExpired:
            continue
        if r.returncode == 0:
            return item, [{x: e.get(x) for x in ("id", "title", "channel", "channel_id", "view_count", "duration")} for e in json.loads(r.stdout).get("entries") or []]
    return item, None
its = list(itens()); erros = 0
with open(os.path.join(BASE, "dados/busca_clones.jsonl"), "w") as f, ThreadPoolExecutor(4) as ex:
    for (l, k, q, o), vs in ex.map(rodar, its):
        if vs is None: erros += 1; print("ERRO", l, q, file=sys.stderr); continue
        for i, v in enumerate(vs): f.write(json.dumps({"lang": l, "tema": k, "q": q, "ordem": o, "pos": i, **v}, ensure_ascii=False) + "\n")
print("consultas:", len(its), "erros:", erros, file=sys.stderr)
