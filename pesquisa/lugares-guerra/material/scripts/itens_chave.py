#!/usr/bin/env python
"""3-5 itens-chave com URL por tema (automatico; conferir antes de usar).

Por tema: 2 filmes PD do Internet Archive (colecoes de governo / newsreel / Prelinger, ordenados por downloads),
1 foto NARA online "Unrestricted", 1 foto NHHC e 1 foto atual do DVIDS via Commons (com resolucao).
Uso: tools/.venv/bin/python -I .../itens_chave.py [id ...]   -> itens_chave.json
"""
import json, os, sys, time
import requests, urllib3

urllib3.disable_warnings()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from temas import TEMAS  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "itens_chave.json")
UA = {"User-Agent": "fabrica-pesquisa/0.1 (personal research; python-requests)"}
UAW = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/120", "Accept": "application/json"}
COLS = "collection:(FedFlix OR usgovfilms OR prelinger OR universal_newsreels OR wwIIarchive OR nasa OR militaryfilms)"


def get(url, params, headers=UA, verify=True):
    for t in range(4):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=60, verify=verify)
            if r.status_code == 429:
                time.sleep(15 * (t + 1)); continue
            if not r.text.lstrip().startswith("{"):
                time.sleep(5); continue
            return r.json()
        except Exception:  # noqa: BLE001
            time.sleep(5)
    return None


def ia(t):
    q = "(" + " OR ".join(f'title:("{f}") OR subject:("{f}")' for f in t["frases"]) + f") AND mediatype:movies AND {COLS}"
    j = get("https://archive.org/advancedsearch.php", {"q": q, "fl[]": ["identifier", "title", "year", "licenseurl", "collection"],
                                                         "sort[]": "downloads desc", "rows": 2, "output": "json"})
    return [{"fonte": "Internet Archive", "titulo": d.get("title"), "ano": d.get("year"),
             "licenca_declarada": d.get("licenseurl"), "colecao": [c for c in d.get("collection", []) if not c.startswith("fav-")][:3],
             "url": "https://archive.org/details/" + d["identifier"]} for d in (j or {}).get("response", {}).get("docs", [])]


def nara(t):
    for f in t["frases"]:
        j = get("https://catalog.archives.gov/proxy/records/search", {"q": f'"{f}"', "availableOnline": "true",
                "typeOfMaterials": "Photographs and other Graphic Materials", "limit": 10}, headers=UAW)
        for h in (j or {}).get("body", {}).get("hits", {}).get("hits", []):
            rec = h["_source"]["record"]
            if (rec.get("useRestriction") or {}).get("status") == "Unrestricted" and "No caption" not in rec.get("title", ""):
                return [{"fonte": "NARA", "titulo": rec.get("title"), "id_local": rec.get("localIdentifier"),
                         "licenca": "Unrestricted (obra federal)", "url": f"https://catalog.archives.gov/id/{rec.get('naId')}"}]
        time.sleep(1)
    return []


def nhhc(t):
    j = get("https://www.history.navy.mil/content/history/nhhc/search/jcr:content.results.json",
            {"q": t["frases"][0], "hitsPerPage": 3, "docType": "photograph"}, headers=UAW, verify=False)
    hits = ((j or {}).get("resultsFound") or {}).get("hits", [])
    return [{"fonte": "NHHC", "titulo": h["pageTitle"], "licenca": "PD salvo indicacao",
             "url": "https://www.history.navy.mil" + h["URL"].replace("/content/history/nhhc", "")} for h in hits[:1]]


def dvids(t):
    j = get("https://commons.wikimedia.org/w/api.php", {
        "action": "query", "generator": "search", "gsrsearch": f'"{t["frases"][0]}" insource:dvidshub', "gsrnamespace": 6,
        "gsrlimit": 1, "prop": "imageinfo", "iiprop": "size|extmetadata", "iiextmetadatafilter": "LicenseShortName|DateTimeOriginal",
        "format": "json"})
    time.sleep(1.5)
    out = []
    for p in ((j or {}).get("query") or {}).get("pages", {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        out.append({"fonte": "DVIDS via Commons (atual)", "titulo": p["title"], "resolucao": f"{ii.get('width')}x{ii.get('height')}",
                    "licenca": ii.get("extmetadata", {}).get("LicenseShortName", {}).get("value"),
                    "url": "https://commons.wikimedia.org/wiki/" + p["title"].replace(" ", "_")})
    return out


def main():
    ids = sys.argv[1:]
    dados = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for t in TEMAS:
        if ids and t["id"] not in ids:
            continue
        itens = ia(t) + nara(t) + nhhc(t) + dvids(t)
        dados[t["id"]] = itens
        json.dump(dados, open(OUT, "w"), ensure_ascii=False, indent=1)
        print(t["id"], len(itens), flush=True)


if __name__ == "__main__":
    main()
