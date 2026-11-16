# Baixa séries históricas da ANA (HidroWeb webservice, sem login) e grava dados/ana_<cod>_<tipo>.json (dias).
# uso: python3 shared/baixa_ana.py <codEstacao> <tipo 1=cota 2=chuva 3=vazão> <dd/mm/aaaa ini> <dd/mm/aaaa fim>
import sys, json, re, urllib.request, xml.etree.ElementTree as ET, calendar
from pathlib import Path
cod, tipo, ini, fim = sys.argv[1:5]
url = f"http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica?codEstacao={cod}&dataInicio={ini}&dataFim={fim}&tipoDados={tipo}&nivelConsistencia="
x = urllib.request.urlopen(url, timeout=120).read()
root = ET.fromstring(x)
pref = {"1": "Cota", "2": "Chuva", "3": "Vazao"}[tipo]
dias = {}
for s in root.iter("SerieHistorica"):
    g = {c.tag: c.text for c in s}
    dh = g.get("DataHora", "")[:10]; a, m = int(dh[:4]), int(dh[5:7])
    cons = g.get("NivelConsistencia")
    for d in range(1, calendar.monthrange(a, m)[1] + 1):
        v = g.get(f"{pref}{d:02d}")
        if v is None: continue
        k = f"{a}-{m:02d}-{d:02d}"
        if k in dias and cons == "1": continue  # prefere consistido (2)
        dias[k] = float(v)
out = Path(__file__).resolve().parent.parent / "dados" / f"ana_{cod}_{pref.lower()}.json"
json.dump({"fonte": f"ANA HidroWeb, estação {cod}, tipoDados={tipo} ({pref}); {url}", "unidade": "cm" if tipo == "1" else ("mm" if tipo == "2" else "m3/s"),
           "dias": dict(sorted(dias.items()))}, open(out, "w"), indent=0)
vals = sorted(dias.items(), key=lambda kv: -kv[1])[:5]
print(out.name, len(dias), "dias; maiores:", vals)
