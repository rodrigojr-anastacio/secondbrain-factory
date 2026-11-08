"""Autocomplete do YouTube (via WARP, grátis) para sementes de clima -> dados/autocomplete.json"""
import json, os, re, subprocess, time, urllib.parse
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GL = {"pt": "BR", "en": "US", "es": "MX", "fr": "FR", "de": "DE"}
S = {"pt": ["tornado", "tornado em", "tornado no brasil", "por que tantos", "ciclone", "el niño", "enchente", "o que está acontecendo com o clima", "como se forma",
            "maiores desastres", "tragédia de", "granizo", "corredor dos tornados", "clima no sul", "tempestade"],
     "en": ["tornado", "brazil tornado", "why are there so many", "el niño", "extreme weather", "deadliest", "the day the", "disaster explained", "how do tornadoes",
            "strongest hurricane", "flood"],
     "es": ["tornado en", "por qué hay tantos", "el niño", "clima extremo", "desastre de", "cómo se forma", "huracán", "tragedia de"]}
res = {}
for lang, seeds in S.items():
    for q in seeds:
        url = "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode({"client": "youtube", "ds": "yt", "hl": lang, "gl": GL[lang], "oe": "utf-8", "q": q})
        r = subprocess.run(["curl", "-s", "-m", "20", "--socks5-hostname", "127.0.0.1:40000", url], capture_output=True)
        m = re.search(r"\((\[.*\])\)\s*$", r.stdout.decode("utf-8", "replace"), re.S)
        res[f"{lang}|{q}"] = [s[0] for s in json.loads(m.group(1))[1]] if m else None
        time.sleep(0.5)
json.dump(res, open(os.path.join(BASE, "dados", "autocomplete.json"), "w"), ensure_ascii=False, indent=1)
for k, v in res.items(): print(k, "→", "; ".join((v or [])[:8]))
