import json
p = 'src/timeline.json'; t = json.load(open(p)); S = t['shots']
M = {0: 'gen_minas_tirith', 74: 'gen_minas_tirith', 78: 'gen_minas_tirith2', 76: 'gen_minas_tirith2', 79: 'gen_minas_tirith', 77: 'gen_minas_tirith2', 6: 'gen_minas_tirith2',
     1: 'gen_khazad_dum', 47: 'gen_khazad_dum', 51: 'gen_khazad_dum2', 70: 'gen_khazad_dum2', 72: 'gen_khazad_dum2',
     2: 'gen_osgiliath', 60: 'gen_osgiliath', 64: 'gen_osgiliath', 3: 'gen_umbar', 81: 'gen_umbar', 82: 'gen_pelargir',
     15: 'gen_falas', 20: 'gen_nogrod', 24: 'gen_menegroth', 25: 'gen_menegroth', 26: 'gen_menegroth',
     30: 'gen_nargothrond', 31: 'gen_nargothrond2', 35: 'gen_gondolin', 87: 'gen_tirion', 93: 'gen_armenelos'}
for i, im in M.items():
    S[i]['img'] = im; S[i]['credit'] = 'Illustration générée · originale'
first = min(c['from'] for c in t['crown']); n = 0
for s in S:
    if s['kind'] == 'map' and s['from'] + s['dur'] > first and s.get('kw'):
        s['kw'] = None; n += 1
json.dump(t, open(p, 'w'), ensure_ascii=False)
rows = ['# STORYBOARD (v2)\n', '| # | t (s) | type | image | mot-clé | crédit |', '|---|---|---|---|---|---|']
for i, s in enumerate(S):
    kw = ' · '.join(x for x in (s.get('kw') or []) if x) or '-'
    rows.append('| %d | %.1f | %s | %s | %s | %s |' % (i, s['from'] / t['fps'], s['kind'], s.get('img') or '-', kw, s.get('credit') or '-'))
open('STORYBOARD.md', 'w').write('\n'.join(rows) + '\n')
print('maps kw nulled', n)
