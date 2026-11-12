#!/usr/bin/env python
"""Busca arquivos no Wikimedia Commons com resolucao e licenca (curadoria dos candidatos).

Uso: tools/.venv/bin/python -I .../commons_busca.py "consulta 1" "consulta 2" ...  [N=8 no ambiente]
Imprime: titulo | largura x altura | licenca | data | URL da pagina do arquivo. Grava em commons_buscas.json.
"""
import json, os, sys, time
import requests

UA = {"User-Agent": "fabrica-pesquisa/0.1 (personal research; python-requests)"}
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "commons_buscas.json")
N = int(os.environ.get("N", "8"))


def busca(q):
    for t in range(4):
        r = requests.get("https://commons.wikimedia.org/w/api.php", headers=UA, timeout=60, params={
            "action": "query", "generator": "search", "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": N,
            "prop": "imageinfo", "iiprop": "size|extmetadata|url",
            "iiextmetadatafilter": "LicenseShortName|Artist|DateTimeOriginal|Credit", "format": "json"})
        if r.status_code == 429:
            time.sleep(15 * (t + 1)); continue
        j = r.json(); break
    out = []
    pages = sorted((j.get("query") or {}).get("pages", {}).values(), key=lambda p: p.get("index", 0))
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {})
        out.append({"titulo": p["title"], "w": ii.get("width"), "h": ii.get("height"),
                    "licenca": em.get("LicenseShortName", {}).get("value"),
                    "data": (em.get("DateTimeOriginal", {}).get("value") or "")[:30],
                    "url": ii.get("descriptionurl")})
    return out


dados = json.load(open(OUT)) if os.path.exists(OUT) else {}
for q in sys.argv[1:]:
    res = busca(q)
    dados[q] = res
    print("##", q)
    for i in res:
        print(f"  {i['titulo'][5:95]} | {i['w']}x{i['h']} | {i['licenca']} | {i['data'][:12]} | {i['url']}")
    time.sleep(1.5)
json.dump(dados, open(OUT, "w"), ensure_ascii=False, indent=1)
