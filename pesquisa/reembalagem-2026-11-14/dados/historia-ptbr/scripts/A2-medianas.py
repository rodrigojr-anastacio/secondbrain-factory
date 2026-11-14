"""Rodada 2: videos.list dos ids + mediana real do canal (últimos 50 uploads: todos e só longos > 3 min, >= 3 dias).
Uso: A2-medianas.py id1 id2 ...  Saída: ../A2-refs.json (acumula) e ../A2-refs.csv"""
import json, os, sys, statistics, csv, datetime as dt
sys.path.insert(0, os.path.expanduser('~/workspace/fabrica-youtube/tools'))
from trends import yt_client, segundos
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
yt = yt_client(); hoje = dt.datetime(2026, 11, 14, tzinfo=dt.timezone.utc)
pj = os.path.join(BASE, 'A2-refs.json'); DB = json.load(open(pj)) if os.path.exists(pj) else {'videos': {}, 'canais': {}}
ids = [i for i in sys.argv[1:] if i not in DB['videos']]
for k in range(0, len(ids), 50):
    r = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[k:k+50])).execute()
    for it in r['items']:
        DB['videos'][it['id']] = {'titulo': it['snippet']['title'], 'canal': it['snippet']['channelTitle'], 'canal_id': it['snippet']['channelId'],
            'data': it['snippet']['publishedAt'][:10], 'views': int(it['statistics'].get('viewCount', 0)), 'dur_s': segundos(it['contentDetails'].get('duration', 'PT0S')),
            'idioma': it['snippet'].get('defaultAudioLanguage') or it['snippet'].get('defaultLanguage')}
chs = sorted({v['canal_id'] for v in DB['videos'].values()} - set(DB['canais']))
for k in range(0, len(chs), 50):
    r = yt.channels().list(part='contentDetails,statistics', id=','.join(chs[k:k+50])).execute()
    for it in r['items']:
        DB['canais'][it['id']] = {'uploads': it['contentDetails']['relatedPlaylists']['uploads'], 'inscritos': int(it['statistics'].get('subscriberCount', 0))}
for ch, c in DB['canais'].items():
    if 'med_todos50' in c: continue
    try:
        r = yt.playlistItems().list(part='contentDetails', playlistId=c['uploads'], maxResults=50).execute()
        vs = yt.videos().list(part='statistics,contentDetails,snippet', id=','.join(x['contentDetails']['videoId'] for x in r['items'])).execute()['items']
    except Exception as e:
        c['erro'] = str(e)[:80]; continue
    todos, longos = [], []
    for it in vs:
        pub = dt.datetime.fromisoformat(it['snippet']['publishedAt'].replace('Z', '+00:00')); v = int(it['statistics'].get('viewCount', 0))
        todos.append(v)
        if segundos(it['contentDetails'].get('duration', 'PT0S')) > 180 and (hoje - pub).days >= 3: longos.append(v)
    c.update(n_todos=len(todos), med_todos50=statistics.median(todos) if todos else None, n_longos=len(longos), med_longos=statistics.median(longos) if longos else None)
json.dump(DB, open(pj, 'w'), ensure_ascii=False, indent=1)
with open(os.path.join(BASE, 'A2-refs.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['id', 'link', 'canal', 'inscritos', 'views', 'data', 'dur_min', 'med_todos50', 'n_todos', 'med_longos', 'n_longos', 'x_med_todos', 'x_med_longos', 'titulo'])
    for i, v in DB['videos'].items():
        c = DB['canais'].get(v['canal_id'], {}); mt, ml = c.get('med_todos50'), c.get('med_longos')
        w.writerow([i, f'https://youtu.be/{i}', v['canal'], c.get('inscritos'), v['views'], v['data'], v['dur_s'] // 60, mt, c.get('n_todos'), ml, c.get('n_longos'),
                    round(v['views'] / mt, 1) if mt else '', round(v['views'] / ml, 1) if ml else '', v['titulo']])
