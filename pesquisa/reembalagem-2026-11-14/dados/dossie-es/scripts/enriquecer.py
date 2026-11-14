"""videos.list + channels.list + mediana dos últimos 30 uploads (playlistItems) para os resultados da busca. Só leitura."""
import sys, os, json, glob, statistics, datetime, csv
sys.path.insert(0, os.path.expanduser('~/workspace/fabrica-youtube/tools'))
from trends import yt_client, segundos
BASE = os.path.dirname(os.path.abspath(__file__)) + '/..'
yt = yt_client()
HOJE = datetime.date(2026, 11, 14)
cota = 0
res = {}
for f in glob.glob(f'{BASE}/busca/*.jsonl'):
    tema = os.path.basename(f).split('__')[0]
    q = os.path.basename(f).split('__')[1][:-6].replace('_', ' ')
    for i, l in enumerate(open(f)):
        try: d = json.loads(l)
        except: continue
        r = res.setdefault(d['id'], {'temas': set(), 'consultas': set(), 'rank': 99})
        r['temas'].add(tema); r['consultas'].add(q); r['rank'] = min(r['rank'], i + 1)
ids = list(res)
vids = {}
for i in range(0, len(ids), 50):
    out = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50])).execute(); cota += 1
    for v in out['items']: vids[v['id']] = v
chs = {v['snippet']['channelId'] for v in vids.values()}
chinfo = {}
chl = list(chs)
for i in range(0, len(chl), 50):
    out = yt.channels().list(part='snippet,statistics,contentDetails', id=','.join(chl[i:i+50])).execute(); cota += 1
    for c in out['items']:
        chinfo[c['id']] = {'nome': c['snippet']['title'], 'inscritos': int(c['statistics'].get('subscriberCount', 0)),
                           'uploads': c['contentDetails']['relatedPlaylists']['uploads'], 'pais': c['snippet'].get('country')}
linhas = []
for vid, v in vids.items():
    sn, st = v['snippet'], v['statistics']
    pub = datetime.date.fromisoformat(sn['publishedAt'][:10])
    idade = (HOJE - pub).days
    dur = segundos(v['contentDetails'].get('duration','PT0S'))
    ch = chinfo.get(sn['channelId'], {})
    linhas.append({'id': vid, 'temas': '+'.join(sorted(res[vid]['temas'])), 'rank': res[vid]['rank'], 'titulo': sn['title'],
                   'canal': ch.get('nome'), 'channel_id': sn['channelId'], 'inscritos': ch.get('inscritos'), 'data': str(pub), 'idade_d': idade,
                   'dur_s': dur, 'views': int(st.get('viewCount', 0)), 'idioma': sn.get('defaultAudioLanguage') or sn.get('defaultLanguage')})
# mediana dos canais relevantes: vídeos ≤ 400 d, ≥ 3 min, top-12 por tema
rel = set()
for tema in {t for l in linhas for t in l['temas'].split('+')}:
    cand = sorted([l for l in linhas if tema in l['temas'] and l['idade_d'] <= 400 and l['dur_s'] >= 180], key=lambda l: -l['views'])[:12]
    rel |= {l['channel_id'] for l in cand}
medianas = {}
for cid in rel:
    up = chinfo[cid]['uploads']
    try:
        pl = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50).execute(); cota += 1
    except Exception as e:
        continue
    vs = [it['contentDetails']['videoId'] for it in pl['items']]
    out = yt.videos().list(part='statistics,contentDetails', id=','.join(vs)).execute(); cota += 1
    longos = [int(x['statistics'].get('viewCount', 0)) for x in out['items'] if segundos(x['contentDetails'].get('duration','PT0S')) >= 180][:30]
    if longos: medianas[cid] = {'mediana': statistics.median(longos), 'n': len(longos)}
for l in linhas:
    m = medianas.get(l['channel_id'])
    l['mediana_canal'] = m['mediana'] if m else None
    l['n_mediana'] = m['n'] if m else None
    l['acima_mediana'] = (l['views'] > m['mediana']) if m else None
    l['v_por_insc'] = round(l['views'] / l['inscritos'], 2) if l['inscritos'] else None
linhas.sort(key=lambda l: (l['temas'], -l['views']))
with open(f'{BASE}/busca-enriquecida.csv', 'w') as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)
json.dump({'medianas': medianas, 'canais': chinfo, 'cota_unidades': cota}, open(f'{BASE}/canais-medianas.json', 'w'), ensure_ascii=False, indent=1)
print('videos', len(linhas), 'canais', len(chinfo), 'medianas', len(medianas), 'cota', cota)
