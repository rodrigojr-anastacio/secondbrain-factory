"""Métricas 28 d / 90 d por canal a partir de dados/canais-2026-11-14.json → resumo.json, videos-28d.csv, imprime resumo."""
import json, csv, statistics as S, datetime as dt, sys, os
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(f'{B}/dados/canais-2026-11-14.json'))
HOJE = dt.datetime.fromisoformat(d['gerado'])
DIAS = ['seg','ter','qua','qui','sex','sab','dom']
BRT = dt.timezone(dt.timedelta(hours=-3))
res = {}; rows = []
for g, canais in d['grupos'].items():
    for n, c in canais.items():
        vs = c['videos']; ins = max(c['inscritos'], 1)
        for v in vs:
            p = dt.datetime.fromisoformat(v['publicado']).astimezone(BRT)
            v['dia'] = DIAS[p.weekday()]; v['hora_brt'] = p.strftime('%H:%M'); v['data'] = p.strftime('%Y-%m-%d')
            v['vpd'] = round(v['views'] / max(v['idade_d'], 0.5)); v['v_por_insc'] = round(v['views'] / ins, 2)
        L28 = [v for v in vs if v['idade_d'] <= 28 and not v['short']]
        S28 = [v for v in vs if v['idade_d'] <= 28 and v['short']]
        L90 = [v for v in vs if v['idade_d'] <= 90 and not v['short']]
        prim = c.get('primeiro_video')
        idade = round((HOJE - dt.datetime.fromisoformat(prim)).days) if prim else None
        longos = [v for v in vs if not v['short']]
        r = {'grupo': g, 'canal': n, 'papel': c['papel'], 'handle': c['handle'], 'inscritos': c['inscritos'], 'views_total': c['views_total'],
             'idade_d_1o_video': idade, 'criado': c['criado'][:10], 'n_videos': c['n_videos'],
             'longos_28d': len(L28), 'shorts_28d': len(S28), 'longos_por_semana_28d': round(len(L28) / 4, 2),
             'dur_media_min_28d': round(S.mean([v['dur_s'] for v in L28]) / 60, 1) if L28 else None,
             'mediana_views_28d': int(S.median([v['views'] for v in L28])) if L28 else None,
             'mediana_views_shorts_28d': int(S.median([v['views'] for v in S28])) if S28 else None,
             'melhor_28d': max(L28, key=lambda v: v['views']) if L28 else None,
             'top5_90d': sorted(L90, key=lambda v: -v['views'])[:5],
             'dias_28d': {k: sum(1 for v in L28 if v['dia'] == k) for k in DIAS},
             'horas_28d': sorted(v['hora_brt'] for v in L28),
             'primeiras_semanas': [{'n': i+1, 'data': v['data'], 'dur_min': round(v['dur_s']/60, 1), 'views': v['views'], 'titulo': v['titulo']} for i, v in enumerate(longos[:12])] if prim else None,
             'longos_28d_lista': sorted(L28, key=lambda v: -v['views'])}
        res.setdefault(g, {})[n] = r
        for v in vs:
            if v['idade_d'] <= 90:
                rows.append({'grupo': g, 'canal': n, 'papel': c['papel'], 'inscritos': c['inscritos'], **{k: v[k] for k in ['id','data','dia','hora_brt','dur_s','short','titulo','views','likes','coments','idade_d','vpd','v_por_insc']}, 'em_28d': v['idade_d'] <= 28})
json.dump(res, open(f'{B}/dados/resumo.json', 'w'), ensure_ascii=False, indent=1)
with open(f'{B}/dados/videos-90d.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
def k(x): return f'{x/1000:.1f}k' if x and x >= 1000 else str(x)
for g, cs in res.items():
    print(f'\n######## {g}')
    for n, r in cs.items():
        m = r['melhor_28d']
        print(f"\n== {n} [{r['papel']}] {r['handle']} insc {k(r['inscritos'])} idade {r['idade_d_1o_video']}d (criado {r['criado']}) nvid {r['n_videos']} | 28d: {r['longos_28d']} longos ({r['longos_por_semana_28d']}/sem) {r['shorts_28d']} shorts | dur {r['dur_media_min_28d']} | med {k(r['mediana_views_28d'])} | dias {r['dias_28d']} | horas {r['horas_28d']}")
        for v in r['longos_28d_lista']:
            print(f"   28d {v['data']} {v['dia']} {v['hora_brt']} {v['dur_s']//60}m {k(v['views'])} vpd {v['vpd']} v/i {v['v_por_insc']} | {v['titulo'][:90]}")
        tops = [v for v in r['top5_90d'] if v['idade_d'] > 28]
        for v in tops: print(f"   90d {v['data']} {k(v['views'])} | {v['titulo'][:90]}")
        if r['primeiras_semanas'] and r['papel'] not in ('principal',) and r['idade_d_1o_video'] and r['idade_d_1o_video'] < 200:
            print('   início:', '; '.join(f"#{p['n']} {p['data'][5:]} {k(p['views'])}" for p in r['primeiras_semanas']))
