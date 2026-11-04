"""Demanda por idioma no nicho Dossiê: buscas nativas via yt-dlp + WARP (0 cota).
Cada consulta roda em 2 ordens: relevância (all-time) e "este ano por views" (sp=CAMSAggF).
Saída: dados/busca.jsonl (1 linha por resultado)."""
import json, os, sys, subprocess, urllib.parse
from concurrent.futures import ThreadPoolExecutor
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YTDLP = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
N = 30
TEMAS = ["kgb", "cia", "mossad", "stasi", "gestapo", "ss", "mi6", "fbi", "mafia", "templarios", "legiao", "cartel"]
Q = {
 "en": ["history of the KGB", "history of the CIA", "history of Mossad", "history of the Stasi", "history of the Gestapo", "history of the SS",
        "history of MI6", "history of the FBI", "history of the mafia", "history of the Knights Templar", "history of the French Foreign Legion", "history of the drug cartels"],
 "es": ["historia de la KGB", "historia de la CIA", "historia del Mossad", "historia de la Stasi", "historia de la Gestapo", "historia de las SS",
        "historia del MI6", "historia del FBI", "historia de la mafia", "historia de los templarios", "historia de la legión extranjera", "historia de los cárteles"],
 "pt": ["história da KGB", "história da CIA", "história do Mossad", "história da Stasi", "história da Gestapo", "história da SS",
        "história do MI6", "história do FBI", "história da máfia", "história dos templários", "história da legião estrangeira", "história dos cartéis"],
 "fr": ["histoire du KGB", "histoire de la CIA", "histoire du Mossad", "histoire de la Stasi", "histoire de la Gestapo", "histoire de la SS",
        "histoire du MI6", "histoire du FBI", "histoire de la mafia", "histoire des templiers", "histoire de la légion étrangère", "histoire des cartels"],
 "de": ["Geschichte des KGB", "Geschichte der CIA", "Geschichte des Mossad", "Geschichte der Stasi", "Geschichte der Gestapo", "Geschichte der SS",
        "Geschichte des MI6", "Geschichte des FBI", "Geschichte der Mafia", "Geschichte der Templer", "Geschichte der Fremdenlegion", "Geschichte der Drogenkartelle"],
 "it": ["storia del KGB", "storia della CIA", "storia del Mossad", "storia della Stasi", "storia della Gestapo", "storia delle SS",
        "storia dell'MI6", "storia dell'FBI", "storia della mafia", "storia dei templari", "storia della legione straniera", "storia dei cartelli della droga"],
}
FORMULA = {
 "en": ["the entire history of the KGB", "the entire history of the CIA", "the entire history of the mafia", "the entire history of in minutes"],
 "es": ["toda la historia de la KGB", "la historia completa de la CIA", "toda la historia del Mossad en minutos", "toda la historia de en minutos"],
 "pt": ["a história inteira da KGB", "a história completa da CIA", "toda a história do Mossad", "a história inteira em minutos"],
 "fr": ["toute l'histoire du KGB", "l'histoire complète de la CIA", "toute l'histoire du Mossad", "toute l'histoire de en minutes"],
 "de": ["die ganze Geschichte des KGB", "die komplette Geschichte der CIA", "die ganze Geschichte der Stasi", "die ganze Geschichte in Minuten"],
 "it": ["tutta la storia del KGB", "la storia completa della CIA", "tutta la storia del Mossad", "tutta la storia in minuti"],
}
# exploratórios: (tema, consulta)
EXPL = {
 "ru": [("kgb", "история КГБ"), ("cia", "история ЦРУ"), ("mossad", "история Моссада"), ("gestapo", "история гестапо"), ("formula", "вся история КГБ")],
 "tr": [("kgb", "KGB'nin tarihi"), ("cia", "CIA'in tarihi"), ("mossad", "Mossad'ın tarihi"), ("gestapo", "Gestapo tarihi"), ("formula", "KGB'nin tüm tarihi")],
 "hi": [("kgb", "KGB का इतिहास"), ("cia", "CIA का इतिहास"), ("mossad", "Mossad history in hindi"), ("gestapo", "Gestapo history in hindi"), ("formula", "KGB history in hindi")],
 "ja": [("kgb", "KGBの歴史"), ("cia", "CIAの歴史"), ("mossad", "モサドの歴史"), ("gestapo", "ゲシュタポの歴史")],
 "pl": [("kgb", "historia KGB"), ("cia", "historia CIA"), ("mossad", "historia Mossadu"), ("gestapo", "historia Gestapo"), ("formula", "cała historia KGB")],
 "ar": [("kgb", "تاريخ الكي جي بي"), ("cia", "تاريخ المخابرات الأمريكية CIA"), ("mossad", "تاريخ الموساد"), ("gestapo", "تاريخ الجستابو")],
}
def itens():
    for lang, qs in Q.items():
        for tema, q in zip(TEMAS, qs): yield lang, tema, "tema", q
        for q in FORMULA[lang]: yield lang, "formula", "formula", q
    for lang, l in EXPL.items():
        for tema, q in l: yield lang, tema, "explor", q
def rodar(item):
    lang, tema, tipo, q, ordem = item
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + ("&sp=CAMSAggF" if ordem == "ano_views" else "")
    for _ in range(2):
        try:
            r = subprocess.run([YTDLP, "--proxy", "socks5://127.0.0.1:40000", "--extractor-args", f"youtube:lang={lang}", "--flat-playlist", "-J",
                                "--playlist-end", str(N), url], capture_output=True, text=True, timeout=150)
        except subprocess.TimeoutExpired:
            continue
        if r.returncode == 0:
            return item, [{k: e.get(k) for k in ("id", "title", "channel", "channel_id", "view_count", "duration")} for e in json.loads(r.stdout).get("entries") or []]
    return item, None
qs = [(*i, o) for i in itens() for o in ("relevancia", "ano_views")]
erros = 0
with open(os.path.join(BASE, "dados/busca.jsonl"), "w") as f, ThreadPoolExecutor(4) as ex:
    for (lang, tema, tipo, q, o), vs in ex.map(rodar, qs):
        if vs is None: erros += 1; print("ERRO", lang, q, o, file=sys.stderr); continue
        for i, v in enumerate(vs):
            f.write(json.dumps({"lang": lang, "tema": tema, "tipo": tipo, "q": q, "ordem": o, "pos": i, **v}, ensure_ascii=False) + "\n")
print("consultas:", len(qs), "erros:", erros, file=sys.stderr)
