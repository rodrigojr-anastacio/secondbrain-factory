"""Tabela das referências citadas (views de 14/11/2026), unindo a busca desta pesquisa e o benchmark 90 d. Grava referencias.csv."""
import csv, json, os, statistics, sys
B = os.path.dirname(os.path.abspath(__file__)) + '/..'
busca = {x['id']: x for x in csv.DictReader(open(B + '/busca-enriquecida.csv'))}
bench_rows = [x for x in csv.DictReader(open(B + '/../../../benchmark-2026-11-14/dados/videos-90d.csv')) if x['short'] == 'False']
med_bench = {}
for c in {x['canal'] for x in bench_rows}:
    v = sorted([x for x in bench_rows if x['canal'] == c], key=lambda x: x['data'])[-30:]
    med_bench[c] = statistics.median(int(x['views']) for x in v)
bench = {x['id']: x for x in bench_rows}
ids = open(B + '/referencias-ids.txt').read().split()
out = []
for i in ids:
    if i in busca and busca[i]['mediana_canal']:
        x = busca[i]; med = float(x['mediana_canal']); fonte = 'busca 14/11'
    elif i in bench:
        x = bench[i]; med = med_bench[x['canal']]; fonte = 'benchmark 90d'
    elif i in busca:
        x = busca[i]; med = None; fonte = 'busca 14/11'
    else:
        print('faltou', i); continue
    v = int(x['views']); ins = int(x['inscritos'] or 0)
    out.append({'id': i, 'link': f'https://youtu.be/{i}', 'canal': x['canal'], 'inscritos': ins, 'views': v, 'data': x['data'],
                'v_por_insc': round(v / ins, 2) if ins else None, 'mediana_canal': med, 'acima_mediana': (v > med) if med else None,
                'titulo': x['titulo'], 'fonte': fonte})
with open(B + '/referencias.csv', 'w') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for r in out:
    print(f"{r['id']}|{r['canal']}|{r['inscritos']}|{r['views']}|{r['data']}|{r['v_por_insc']}|{r['mediana_canal']}|{r['acima_mediana']}|{r['titulo'][:80]}")
