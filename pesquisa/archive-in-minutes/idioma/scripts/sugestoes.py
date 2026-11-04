"""Autocomplete do YouTube (suggestqueries, via WARP) como proxy de busca por idioma. Saída: dados/sugestoes.json"""
import json, os, sys, time, urllib.parse, urllib.request
import socket
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GL = {"en": "US", "es": "MX", "pt": "BR", "fr": "FR", "de": "DE", "it": "IT", "ru": "RU", "tr": "TR", "hi": "IN", "ja": "JP", "pl": "PL", "ar": "EG"}
ORGS = ["kgb", "cia", "mossad", "stasi", "gestapo", "mi6", "fbi", "mafia"]
HIST = {"en": "history of the {}", "es": "historia de la {}", "pt": "história da {}", "fr": "histoire du {}", "de": "geschichte der {}", "it": "storia del {}",
        "ru": "история {}", "tr": "{} tarihi", "hi": "{} history in hindi", "ja": "{}の歴史", "pl": "historia {}", "ar": "تاريخ {}"}
PALAVRA = {"en": "histor", "es": "histori", "pt": "histór", "fr": "histoir", "de": "geschicht", "it": "stori", "ru": "истори", "tr": "tarih", "hi": "histor",
           "ja": "歴史", "pl": "histori", "ar": "تاريخ"}
EXTRA = {"es": ["toda la historia de", "la historia completa de"], "pt": ["a história inteira", "a história completa da"], "en": ["the entire history of"],
         "fr": ["toute l'histoire de", "l'histoire complète"], "de": ["die ganze geschichte", "die komplette geschichte"], "it": ["tutta la storia", "la storia completa"]}
import subprocess
def sug(q, hl):
    url = "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode({"client": "youtube", "ds": "yt", "hl": hl, "gl": GL[hl], "q": q})
    for _ in range(3):
        try:
            raw = subprocess.run(["curl", "-s", "-m", "20", "--socks5-hostname", "127.0.0.1:40000", url], capture_output=True, timeout=30).stdout.decode("utf-8", "replace")
            js = json.loads(raw[raw.index("(") + 1: raw.rindex(")")])
            return [s[0] for s in js[1]]
        except Exception as e:
            err = str(e); time.sleep(2)
    return None
out = {}
for hl in GL:
    d = {}
    for o in ORGS:
        s = sug(o, hl); h = sug(HIST[hl].format(o), hl)
        d[o] = {"sug_org": s, "n_org": len(s) if s is not None else None,
                "n_org_com_historia": sum(PALAVRA[hl] in x.lower() for x in s) if s else 0,
                "consulta_hist": HIST[hl].format(o), "sug_hist": h, "n_hist": len(h) if h is not None else None}
        time.sleep(0.3)
    for q in EXTRA.get(hl, []):
        s = sug(q, hl); d["extra:" + q] = {"sug": s, "n": len(s) if s is not None else None}
    out[hl] = d
    print(hl, {o: (d[o]["n_org"], d[o]["n_org_com_historia"], d[o]["n_hist"]) for o in ORGS}, file=sys.stderr)
json.dump(out, open(os.path.join(BASE, "dados/sugestoes.json"), "w"), ensure_ascii=False, indent=1)
