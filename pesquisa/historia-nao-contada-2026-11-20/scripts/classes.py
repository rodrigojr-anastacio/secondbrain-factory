#!/usr/bin/env python3
"""Recorte "história de país" do corpus e comparação genérica × fato específico × completa (pt, 7–730 dias, ≥5 min)."""
import csv, re, statistics as st, json
R = list(csv.DictReader(open('corpus.csv')))
PAIS = re.compile(r"egit|faraó|cleópatra|índia|india|china|chin[eê]s|brasil|nordeste|recife|ir[ãa]\b|persa|pérsia|r[uú]ssia|fran[çc]a|roma\b|romano|alemanha|prússia|jap[ãa]o|inglaterra|portugal|espanha|holand|império|imp[ée]rio|reino|viking|czar|samurai|macau|aiat", re.I)
FORA = re.compile(r"viagem|vida real|4k|lugares|morar|morando|trump|cheguei|pior pa[ií]s|podcast|cortes?\b|primocast|b[ií]blia|josé|jesus|deus|filme|stand|trap|novela|futebol|guia|turismo|hoje|2025|2026|not[ií]cia|guerra contra|bomba|expulsa|para dormir|dormir|relax", re.I)
GEN = re.compile(r"ningu[eé]m (te )?(conta|explica|fala|sabe)|n[aã]o (te )?(contaram|contam|ensinam|ensinaram)|n[aã]o contada|lado (sombrio|obscuro|oculto|secreto)|segredo|escond|proibid|oculta|verdadeira hist|esquecid|nunca aprendeu|que voc[eê] n[aã]o sabia|desconhecid", re.I)
COMP = re.compile(r"complet|inteir|toda a hist|em \d+ minutos|resumo|\d[\d.]* anos em|da funda|das origens|do in[ií]cio|hist[óo]ria d[aoe] \w+ *(\||$)", re.I)
FATO = re.compile(r"por ?que|como |quando|antes d|o dia|quase|nunca|achava|virou|se mudou|foi |era |eram |n[aã]o era|at[eé] ", re.I)
S = []
for r in R:
    if r['idioma_consulta'] != 'pt' or not r['x_mediana'] or not (7 <= int(r['idade_d']) <= 730) or float(r['dur_min']) < 5:
        continue
    t = r['titulo']
    if not PAIS.search(t) or FORA.search(t):
        continue
    cl = 'generica' if GEN.search(t) else 'completa' if COMP.search(t) else 'fato_especifico' if FATO.search(t) else 'outro'
    r['classe2'] = cl; S.append(r)
res = {}
for cl in ['generica', 'fato_especifico', 'completa', 'outro']:
    X = [r for r in S if r['classe2'] == cl]
    xs = [float(r['x_mediana']) for r in X]
    peq = {r['canal'] for r in X if float(r['x_mediana']) >= 3 and r['inscritos'] and int(r['inscritos']) <= 500000}
    res[cl] = {'n': len(X), 'mediana_x': round(st.median(xs), 2) if xs else None, 'pct_3x': round(100 * sum(x >= 3 for x in xs) / len(xs)) if xs else None,
               'mediana_views': int(st.median([int(r['views']) for r in X])) if X else None, 'canais_peq_med_3x': len(peq)}
    print(cl, res[cl])
json.dump(res, open('dados/classes_resumo.json', 'w'), indent=1)
with open('dados/recorte_historia_pais.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['classe2', 'x_mediana', 'views', 'idade_d', 'inscritos', 'mediana_canal', 'dur_min', 'canal', 'titulo', 'url'], extrasaction='ignore')
    w.writeheader(); w.writerows(sorted(S, key=lambda r: (r['classe2'], -float(r['x_mediana']))))
for cl in ['generica', 'fato_especifico']:
    print('==', cl)
    for r in sorted([r for r in S if r['classe2'] == cl], key=lambda r: -float(r['x_mediana']))[:15]:
        print(f"  {float(r['x_mediana']):7.1f}|{int(r['views']):>9}|{r['idade_d']:>4}d|ins={r['inscritos']:>8}|{r['canal'][:20]:20}|{r['titulo'][:80]}|{r['id']}")
