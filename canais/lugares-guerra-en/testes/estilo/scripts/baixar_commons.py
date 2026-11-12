"""Baixa arquivos do Wikimedia Commons (versão reduzida a N px) e grava licença/autor/URL em public/img/licencas.json."""
import json, sys, os, requests
H = {"User-Agent": "fabrica-youtube-teste/1.0 (pesquisa de material de dominio publico)"}
API = "https://commons.wikimedia.org/w/api.php"
out = sys.argv[1]; largura = int(sys.argv[2]); pares = sys.argv[3:]  # nome_local=File:Titulo
lic = {}
lp = os.path.join(out, "licencas.json")
if os.path.exists(lp): lic = json.load(open(lp))
for p in pares:
    local, titulo = p.split("=", 1)
    r = requests.get(API, params={"action": "query", "titles": titulo, "prop": "imageinfo", "iiprop": "url|extmetadata|size",
                                  "iiurlwidth": largura, "format": "json"}, headers=H, timeout=60).json()
    pg = next(iter(r["query"]["pages"].values()))
    if "imageinfo" not in pg: print("FALTA", titulo); continue
    ii = pg["imageinfo"][0]; md = ii.get("extmetadata", {})
    url = ii.get("thumburl") or ii["url"]
    img = requests.get(url, headers=H, timeout=120).content
    open(os.path.join(out, local), "wb").write(img)
    lic[local] = {"arquivo": titulo, "pagina": ii.get("descriptionurl"), "original_px": f'{ii["width"]}x{ii["height"]}',
                  "licenca": md.get("LicenseShortName", {}).get("value"), "autor": md.get("Artist", {}).get("value", "")[:200],
                  "credito": md.get("Credit", {}).get("value", "")[:200]}
    print(local, ii["width"], ii["height"], lic[local]["licenca"])
json.dump(lic, open(lp, "w"), ensure_ascii=False, indent=1)
