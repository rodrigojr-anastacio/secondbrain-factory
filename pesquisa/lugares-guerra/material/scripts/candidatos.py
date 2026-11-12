#!/usr/bin/env python
"""Levanta itens concretos (URL, licenca, resolucao) para os temas candidatos a piloto.

Uso: tools/.venv/bin/python -I pesquisa/lugares-guerra/material/scripts/candidatos.py [tema ...]
Saida: pesquisa/lugares-guerra/material/candidatos_brutos.json (curadoria manual vai para o MATERIAL.md).
"""
import json, os, sys, time
import requests, urllib3

urllib3.disable_warnings()
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "candidatos_brutos.json")
UA_BOT = {"User-Agent": "fabrica-pesquisa/0.1 (personal research; python-requests)"}
UA_WEB = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/120", "Accept": "application/json"}
COMMONS = "https://commons.wikimedia.org/w/api.php"

CONSULTAS = {
    "midway": {"nara": ["Midway Atoll", "Battle of Midway", "Midway Island"], "nhhc": ["Battle of Midway", "Midway Atoll"],
               "ia": ['"Battle of Midway"', '"Midway Island"', '"Midway Atoll"'],
               "commons_atual": ['"Midway Atoll" insource:dvidshub', '"Midway Atoll" insource:"fws"', '"Midway Atoll" Landsat']},
    "corregidor": {"nara": ["Corregidor"], "nhhc": ["Corregidor"], "ia": ['"Corregidor"'],
                   "commons_atual": ['"Corregidor" insource:dvidshub', 'Corregidor Malinta tunnel', 'Corregidor Battery']},
    "tinian": {"nara": ["Tinian"], "nhhc": ["Tinian"], "ia": ['"Tinian"'],
               "commons_atual": ['"Tinian" insource:dvidshub', 'Tinian North Field', 'Tinian bomb pit']},
    "bikini": {"nara": ["Operation Crossroads", "Bikini Atoll"], "nhhc": ["Operation Crossroads", "Bikini"],
               "ia": ['"Operation Crossroads"', '"Bikini Atoll"', '"Bikini" AND "atomic"'],
               "commons_atual": ['"Bikini Atoll" insource:dvidshub', '"Bikini Atoll" Landsat', '"Bikini Atoll" 20'],
               },
}


def get(url, params=None, headers=UA_BOT, verify=True):
    for t in range(4):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=60, verify=verify)
            if r.status_code == 429:
                time.sleep(15 * (t + 1)); continue
            r.raise_for_status()
            return r.json()
        except Exception as e:  # noqa: BLE001
            err = e; time.sleep(5)
    raise RuntimeError(str(err)[:200])


def nara(frase, tipo, n=15):
    j = get("https://catalog.archives.gov/proxy/records/search",
            {"q": f'"{frase}"', "availableOnline": "true", "typeOfMaterials": tipo, "limit": n}, headers=UA_WEB)
    out = []
    for h in j["body"]["hits"]["hits"]:
        rec = h["_source"]["record"]
        objs = rec.get("digitalObjects") or []
        out.append({"naId": rec.get("naId"), "titulo": rec.get("title"), "id_local": rec.get("localIdentifier"),
                    "uso": (rec.get("useRestriction") or {}).get("status"),
                    "serie": next((a.get("title") for a in rec.get("ancestors", []) if a.get("levelOfDescription") == "series"), None),
                    "url": f"https://catalog.archives.gov/id/{rec.get('naId')}",
                    "objetos": [{"url": o.get("objectUrl"), "tipo": o.get("objectType"), "bytes": o.get("objectFileSize")} for o in objs[:3]]})
    return out


def nhhc(frase, n=20):
    j = get("https://www.history.navy.mil/content/history/nhhc/search/jcr:content.results.json",
            {"q": frase, "hitsPerPage": n, "docType": "photograph"}, headers=UA_WEB, verify=False)
    return [{"titulo": h["pageTitle"], "resumo": h.get("excerpt", "")[:200],
             "url": "https://www.history.navy.mil" + h["URL"].replace("/content/history/nhhc", "")}
            for h in (j.get("resultsFound") or {}).get("hits", [])]


def ia(q, n=15):
    j = get("https://archive.org/advancedsearch.php",
            {"q": f"({q}) AND mediatype:movies", "fl[]": ["identifier", "title", "year", "downloads", "licenseurl", "collection"],
             "sort[]": "downloads desc", "rows": n, "output": "json"})
    return [{"id": d["identifier"], "titulo": d.get("title"), "ano": d.get("year"), "downloads": d.get("downloads"),
             "licenca": d.get("licenseurl"), "colecao": d.get("collection"),
             "url": "https://archive.org/details/" + d["identifier"]} for d in j["response"]["docs"]]


def commons(q, n=15):
    j = get(COMMONS, {"action": "query", "generator": "search", "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": n,
                      "prop": "imageinfo", "iiprop": "size|extmetadata|url", "iiextmetadatafilter": "LicenseShortName|Artist|DateTimeOriginal|Credit",
                      "format": "json"})
    time.sleep(1.5)
    out = []
    for p in (j.get("query") or {}).get("pages", {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {})
        out.append({"titulo": p["title"], "w": ii.get("width"), "h": ii.get("height"),
                    "licenca": em.get("LicenseShortName", {}).get("value"),
                    "data": (em.get("DateTimeOriginal", {}).get("value") or "")[:40],
                    "url": ii.get("descriptionurl")})
    return out


def main():
    temas = sys.argv[1:] or list(CONSULTAS)
    dados = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for t in temas:
        c = CONSULTAS[t]
        so_nara = os.environ.get("SO_NARA")
        r = dados.get(t, {}) if so_nara else {}
        r.update({"nara_fotos": {}, "nara_filmes": {}, "nara_textual": {}, "nara_mapas": {}})
        r["erros"] = {}
        if not so_nara:
            r.update({"nhhc": {}, "ia": {}, "commons_atual": {}})
        for f in c["nara"]:
            for chave, tipo in [("nara_fotos", "Photographs and other Graphic Materials"), ("nara_filmes", "Moving Images"),
                                ("nara_textual", "Textual Records"), ("nara_mapas", "Maps and Charts")]:
                try:
                    r[chave][f] = nara(f, tipo, 20 if chave == "nara_fotos" else 10)  # o proxy so aceita 1/10/20/50/100
                except Exception as e:  # noqa: BLE001
                    r["erros"][f"{chave}:{f}"] = str(e)
                time.sleep(1)
        for f in ([] if so_nara else c["nhhc"]):
            try:
                r["nhhc"][f] = nhhc(f)
            except Exception as e:  # noqa: BLE001
                r["erros"]["nhhc:" + f] = str(e)
        for q in ([] if so_nara else c["ia"]):
            try:
                r["ia"][q] = ia(q)
            except Exception as e:  # noqa: BLE001
                r["erros"]["ia:" + q] = str(e)
        for q in ([] if so_nara else c["commons_atual"]):
            try:
                r["commons_atual"][q] = commons(q)
            except Exception as e:  # noqa: BLE001
                r["erros"]["commons:" + q] = str(e)
        dados[t] = r
        json.dump(dados, open(OUT, "w"), ensure_ascii=False, indent=1)
        print(t, "ok", r["erros"], flush=True)


if __name__ == "__main__":
    main()
