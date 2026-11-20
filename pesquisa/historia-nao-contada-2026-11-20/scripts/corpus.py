#!/usr/bin/env python3
"""Monta corpus.csv: vídeo, canal, idade, views, mediana do canal, ×mediana, classe do título."""
import csv, datetime, json, os, re
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
v = json.load(open(f'{OUT}/dados/videos.json'))
c = json.load(open(f'{OUT}/dados/canais.json'))
hoje = datetime.date(2026, 11, 20)
GEN = re.compile(r"ningu[eé]m (te )?(conta|fala|sabe)|n[aã]o (te )?(contaram|contam|conta|ensinam|ensinaram|sabe)|n[aã]o contada|lado (sombrio|obscuro|oculto)|segredos?|escond|proibid|oculta|verdadeira hist|esquecid|"
                 r"untold|never (taught|told)|nobody (talks|tells|knows)|dark (side|history)|forgotten|hidden|secret|they don.t|"
                 r"nadie (te )?cuenta|no te (contaron|cuentan|ense)|oculta|olvidad|secret|prohibid", re.I)
COMPLETA = re.compile(r"complet|inteir|entire|full history|resumo|em \d+ minutos|in \d+ minutes|en \d+ minutos|toda la historia|do in[ií]cio|origem ao", re.I)
rows = []
for vid, x in v.items():
    if not x.get('consultas'):
        continue
    d = datetime.date.fromisoformat(x['publicado'])
    idade = (hoje - d).days
    ch = c.get(x['canal_id']) or {}
    med = ch.get('mediana_30') or 0
    t = x['titulo']
    classe = 'generica' if GEN.search(t) else ('completa' if COMPLETA.search(t) else 'outro')
    q = x['consultas']
    rows.append({'id': vid, 'url': f'https://youtu.be/{vid}', 'titulo': t, 'canal': x['canal'], 'canal_id': x['canal_id'],
                 'publicado': x['publicado'], 'idade_d': idade, 'views': x['views'], 'dur_min': round(x['dur_s'] / 60, 1),
                 'inscritos': ch.get('inscritos', ''), 'mediana_canal': med, 'n_longos': ch.get('n_longos', ''),
                 'x_mediana': round(x['views'] / med, 2) if med else '', 'classe_titulo': classe,
                 'idioma_consulta': q[0]['lang'], 'tipos_consulta': '|'.join(sorted({a['tipo'] for a in q})),
                 'paises': '|'.join(sorted({a['pais'] for a in q if a['pais']})), 'consultas': ' || '.join(sorted({a['q'] for a in q}))})
rows.sort(key=lambda r: -(r['x_mediana'] or 0))
with open(f'{OUT}/corpus.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
print(len(rows))
