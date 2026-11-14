"""Rodada 2 (crivo): enriquece ids (busca2/*.jsonl + ids extra) com videos.list e calcula a mediana REAL
dos últimos ≤50 uploads (≥3 min) de cada canal relevante (views ≥ 15 mil ou canal pedido). Só leitura.
Saída: r2-videos.csv e r2-medianas.json."""
import sys, os, json, glob, csv, statistics, datetime
sys.path.insert(0, os.path.expanduser('~/workspace/fabrica-youtube/tools'))
from trends import yt_client, segundos
B = os.path.dirname(os.path.abspath(__file__)) + '/..'
yt = yt_client(); cota = 0
ids = set()
for f in glob.glob(B + '/busca2/*.jsonl'):
    for l in open(f):
        try: ids.add(json.loads(l)['id'])
        except Exception: pass
ids |= set(open(B + '/r2-ids-extra.txt').read().split()) if os.path.exists(B + '/r2-ids-extra.txt') else set()
ids = sorted(ids)
vids = {}
for i in range(0, len(ids), 50):
    r = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50])).execute(); cota += 1
    for x in r['items']:
        vids[x['id']] = dict(id=x['id'], titulo=x['snippet']['title'], canal=x['snippet']['channelTitle'], channel_id=x['snippet']['channelId'],
            data=x['snippet']['publishedAt'][:10], views=int(x['statistics'].get('viewCount', 0)), dur_s=segundos(x['contentDetails']['duration']),
            idioma=x['snippet'].get('defaultAudioLanguage') or x['snippet'].get('defaultLanguage') or '')
medf = B + '/r2-medianas.json'
med = json.load(open(medf)) if os.path.exists(medf) else {}
hoje = datetime.date(2026, 11, 14)
pedir = {v['channel_id'] for v in vids.values() if v['views'] >= 15000 and (hoje - datetime.date.fromisoformat(v['data'])).days <= 420}
pedir |= set(open(B + '/r2-canais-extra.txt').read().split()) if os.path.exists(B + '/r2-canais-extra.txt') else set()
for cid in sorted(pedir - set(med)):
    up = 'UU' + cid[2:]
    try:
        pl = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50).execute(); cota += 1
    except Exception as e:
        print('erro', cid, e); continue
    vs = [it['contentDetails']['videoId'] for it in pl['items']]
    out = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(vs)).execute(); cota += 1
    longos = [int(x['statistics'].get('viewCount', 0)) for x in out['items'] if segundos(x['contentDetails'].get('duration', 'PT0S')) >= 180]
    nome = out['items'][0]['snippet']['channelTitle'] if out['items'] else cid
    if longos: med[cid] = {'nome': nome, 'mediana': statistics.median(longos), 'n': len(longos)}
json.dump(med, open(medf, 'w'), ensure_ascii=False, indent=1)
rows = []
for v in vids.values():
    m = med.get(v['channel_id'])
    v['mediana_canal'] = m['mediana'] if m else ''
    v['n_med'] = m['n'] if m else ''
    v['x_med'] = round(v['views'] / m['mediana'], 1) if m and m['mediana'] else ''
    rows.append(v)
rows.sort(key=lambda r: -r['views'])
with open(B + '/r2-videos.csv', 'w') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('cota', cota, 'videos', len(rows), 'canais med', len(med))
