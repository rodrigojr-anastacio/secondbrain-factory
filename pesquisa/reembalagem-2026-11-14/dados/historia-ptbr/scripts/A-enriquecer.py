"""videos.list + channels.list (só leitura, ~1 unidade/50 ids) dos resultados de A-busca.jsonl.
Saída: ../A-videos.json (id -> dados) e ../A-canais.json (canal -> inscritos, uploads)."""
import json, os, sys, datetime as dt
sys.path.insert(0, os.path.expanduser('~/workspace/fabrica-youtube/tools'))
from trends import yt_client, segundos, chunks
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
yt = yt_client()
ids = []
for l in [x for f in ('A-busca.jsonl','A-busca2.jsonl','A-busca3.jsonl') for x in open(os.path.join(BASE, f))]:
    d = json.loads(l)
    if d['id'] and d['id'] not in ids and (d.get('view_count') or 0) >= 3000: ids.append(d['id'])
_old = json.load(open(os.path.join(BASE,'A-videos.json'))) if os.path.exists(os.path.join(BASE,'A-videos.json')) else {}
ids = [i for i in ids if i not in _old]
extra = sys.argv[1:]  # ids extras
for e in extra:
    if e not in ids: ids.append(e)
vids = {}
hoje = dt.datetime(2026, 11, 14, tzinfo=dt.timezone.utc)
for c in chunks(ids):
    r = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(c), maxResults=50).execute()
    for it in r['items']:
        s = it['snippet']; pub = dt.datetime.fromisoformat(s['publishedAt'].replace('Z', '+00:00'))
        vids[it['id']] = dict(id=it['id'], titulo=s['title'], canal=s['channelTitle'], canal_id=s['channelId'],
            data=pub.date().isoformat(), idade_d=(hoje - pub).days, views=int(it['statistics'].get('viewCount', 0)),
            dur_s=segundos(it['contentDetails']['duration']), idioma=s.get('defaultAudioLanguage') or s.get('defaultLanguage'))
chs = sorted({v['canal_id'] for v in vids.values()})
canais = {}
for c in chunks(chs):
    r = yt.channels().list(part='snippet,statistics,contentDetails', id=','.join(c), maxResults=50).execute()
    for it in r['items']:
        canais[it['id']] = dict(nome=it['snippet']['title'], inscritos=int(it['statistics'].get('subscriberCount', 0)),
            uploads=it['contentDetails']['relatedPlaylists']['uploads'], pais=it['snippet'].get('country'))
for v in vids.values():
    v['inscritos'] = canais.get(v['canal_id'], {}).get('inscritos')
    v['v_por_insc'] = round(v['views'] / v['inscritos'], 2) if v['inscritos'] else None
old = {}
p = os.path.join(BASE, 'A-videos.json')
if os.path.exists(p): old = json.load(open(p))
old.update(vids); json.dump(old, open(p, 'w'), ensure_ascii=False, indent=1)
pc = os.path.join(BASE, 'A-canais.json'); oc = json.load(open(pc)) if os.path.exists(pc) else {}
oc.update(canais); json.dump(oc, open(pc, 'w'), ensure_ascii=False, indent=1)
print(len(vids), 'vídeos', len(canais), 'canais; unidades ~', len(list(chunks(ids))) + len(list(chunks(chs))))
