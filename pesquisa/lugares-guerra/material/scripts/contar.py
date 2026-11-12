#!/usr/bin/env python
"""Conta material publico por tema em fontes gratuitas (sem chave paga).

Uso: tools/.venv/bin/python -I pesquisa/lugares-guerra/material/scripts/contar.py [id_tema ...]
Saida: pesquisa/lugares-guerra/material/contagens.json (acrescenta/atualiza por tema).

Fontes:
- NARA: endpoint publico do catalogo (catalog.archives.gov/proxy/records/search), so itens online,
  com agregacao por tipo de material. (A API v2 oficial exige x-api-key.)
- Wikimedia Commons: categorias (diretos + 1 nivel de subcategorias) e busca por frase em File:,
  mais proxies de DVIDS e LoC (arquivos do Commons cuja fonte cita dvidshub / loc.gov).
- Internet Archive: advancedsearch, mediatype movies / image / texts.
- NHHC: busca JSON do site (history.navy.mil), total e so fotografias.
- Smithsonian Open Access: api.si.edu com DEMO_KEY (limite baixo; pode falhar).
- LoC / Chronicling America / DVIDS: bloqueados para a VPS (Cloudflare / AWS WAF; DVIDS API exige key).
"""
import json, os, sys, time
import requests, urllib3

urllib3.disable_warnings()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from temas import TEMAS  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "contagens.json")
UA_BOT = {"User-Agent": "fabrica-pesquisa/0.1 (personal research; python-requests)"}
UA_WEB = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
          "Accept": "application/json"}
COMMONS = "https://commons.wikimedia.org/w/api.php"


def get(url, params=None, headers=UA_BOT, tries=4, verify=True):
    err = "falhou"
    for t in range(tries):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=60, verify=verify)
            if r.status_code == 429:
                err = "HTTP 429 (limite)"; time.sleep(15 * (t + 1)); continue
            r.raise_for_status()
            return r.json()
        except Exception as e:  # noqa: BLE001
            err = str(e)[:200]
            time.sleep(5 * (t + 1))
    raise RuntimeError(err)


def orq(frases):
    return " OR ".join(f'"{f}"' for f in frases)


def nara(t):
    # o endpoint nao aceita OR entre frases entre aspas: soma frase a frase (teto; pode duplicar)
    out = {"total_online": 0, "fotos": 0, "filmes": 0, "textual": 0, "mapas": 0, "por_frase": {}}
    for f in t["frases"]:
        j = get("https://catalog.archives.gov/proxy/records/search",
                {"q": f'"{f}"', "availableOnline": "true", "limit": 1}, headers=UA_WEB)
        b = j["body"]
        tipos = {x["key"]: x["doc_count"] for x in b["aggregations"]["typeOfMaterials"]["buckets"]}
        d = {"total_online": b["hits"]["total"]["value"],
             "fotos": tipos.get("Photographs and other Graphic Materials", 0),
             "filmes": tipos.get("Moving Images", 0),
             "textual": tipos.get("Textual Records", 0),
             "mapas": tipos.get("Maps and Charts", 0)}
        out["por_frase"][f] = d
        for k in d:
            out[k] += d[k]
        time.sleep(1)
    return out


def commons_cats(cats):
    total, detalhe = 0, {}
    for c in cats:
        info = get(COMMONS, {"action": "query", "prop": "categoryinfo", "titles": "Category:" + c, "format": "json"})
        p = next(iter(info["query"]["pages"].values()))
        direto = (p.get("categoryinfo") or {}).get("files", 0)
        subs = get(COMMONS, {"action": "query", "list": "categorymembers", "cmtitle": "Category:" + c,
                             "cmtype": "subcat", "cmlimit": 200, "format": "json"})["query"]["categorymembers"]
        nsub = 0
        titulos = [s["title"] for s in subs]
        for i in range(0, len(titulos), 50):
            ci = get(COMMONS, {"action": "query", "prop": "categoryinfo", "titles": "|".join(titulos[i:i + 50]), "format": "json"})
            nsub += sum((pp.get("categoryinfo") or {}).get("files", 0) for pp in ci["query"]["pages"].values())
            time.sleep(1)
        detalhe[c] = {"diretos": direto, "subcats": len(titulos), "arquivos_subcats_1nivel": nsub}
        total += direto + nsub
        time.sleep(1)
    return total, detalhe


def commons_soma(frases, extra=""):
    # CirrusSearch nao combina bem OR + insource: soma frase a frase (teto)
    return sum(commons_busca(f'"{f}"' + (" " + extra if extra else "")) for f in frases)


def commons_busca(q):
    j = get(COMMONS, {"action": "query", "list": "search", "srsearch": q, "srnamespace": 6, "srlimit": 1,
                      "srinfo": "totalhits", "format": "json"})
    time.sleep(1.5)
    return j["query"]["searchinfo"]["totalhits"]


def ia(t, mediatype):
    q = "(" + " OR ".join(f'title:("{f}") OR subject:("{f}") OR description:("{f}")' for f in t["frases"]) + f") AND mediatype:{mediatype}"
    j = get("https://archive.org/advancedsearch.php", {"q": q, "fl[]": "identifier", "rows": 0, "output": "json"})
    return j["response"]["numFound"]


def nhhc(t, doctype=None):
    tot = 0
    for f in t["frases"]:
        p = {"q": f, "hitsPerPage": 1}
        if doctype:
            p["docType"] = doctype
        j = get("https://www.history.navy.mil/content/history/nhhc/search/jcr:content.results.json", p,
                headers=UA_WEB, verify=False)
        tot += (j.get("resultsFound") or {}).get("totalMatches", 0)  # sem resultado = sem a chave
        time.sleep(1)
    return tot  # soma por frase (pode duplicar)


def smithsonian(t):
    j = get("https://api.si.edu/openaccess/api/v1.0/search",
            {"q": f'"{t["frases"][0]}" AND online_media_type:Images', "rows": 0, "api_key": "DEMO_KEY"}, tries=1)
    return j["response"]["rowCount"]


def main():
    ids = sys.argv[1:]
    dados = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for t in TEMAS:
        if ids and t["id"] not in ids:
            continue
        r = {"nome": t["nome"], "frases": t["frases"], "cats": t["cats"], "erros": {}}
        etapas = {
            "nara": lambda: nara(t),
            "commons_cats": lambda: commons_cats(t["cats"]),
            "commons_frase": lambda: commons_soma(t["frases"]),
            "commons_dvids": lambda: commons_soma(t["frases"], "insource:dvidshub"),
            "commons_loc": lambda: commons_soma(t["frases"], 'insource:"loc.gov"'),
            "commons_nara": lambda: commons_soma(t["frases"], 'insource:"archives.gov"'),
            "ia_movies": lambda: ia(t, "movies"),
            "ia_image": lambda: ia(t, "image"),
            "ia_texts": lambda: ia(t, "texts"),
            "nhhc_total": lambda: nhhc(t),
            "nhhc_fotos": lambda: nhhc(t, "photograph"),
            "smithsonian_img": lambda: smithsonian(t),
        }
        if not os.environ.get("SI"):  # DEMO_KEY = 10 req/hora: so com SI=1
            etapas.pop("smithsonian_img")
        for k, fn in etapas.items():
            try:
                v = fn()
                if k == "commons_cats":
                    r["commons_cats_total"], r["commons_cats_detalhe"] = v
                else:
                    r[k] = v
            except Exception as e:  # noqa: BLE001
                r["erros"][k] = str(e)[:200]
        r["lido_em"] = time.strftime("%Y-%m-%d %H:%M")
        dados[t["id"]] = r
        json.dump(dados, open(OUT, "w"), ensure_ascii=False, indent=1)
        print(t["id"], {k: v for k, v in r.items() if k not in ("commons_cats_detalhe", "frases", "cats", "nome")}, flush=True)


if __name__ == "__main__":
    main()
