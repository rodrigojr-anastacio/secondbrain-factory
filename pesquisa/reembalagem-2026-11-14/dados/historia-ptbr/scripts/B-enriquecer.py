import sys, os, json, glob, csv, datetime, statistics
sys.path.insert(0, os.path.expanduser('~/workspace/fabrica-youtube/tools'))
from trends import yt_client
yt = yt_client()
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = {}
for f in sorted(glob.glob(os.path.join(base, 'raw', 'B-ytsearch-*.jsonl'))):
    q = os.path.basename(f)[len('B-ytsearch-'):-6]
    for line in open(f):
        try: d = json.loads(line)
        except: continue
        if d.get('id') and len(d['id']) == 11:
            rows.setdefault(d['id'], {'id': d['id'], 'busca': set()})['busca'].add(q)
ids = list(rows)
vids = {}
for i in range(0, len(ids), 50):
    r = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50])).execute()
    for it in r['items']: vids[it['id']] = it
chs = {v['snippet']['channelId'] for v in vids.values()}
chs = list(chs); chinfo = {}
for i in range(0, len(chs), 50):
    r = yt.channels().list(part='statistics,snippet,contentDetails', id=','.join(chs[i:i+50])).execute()
    for it in r['items']: chinfo[it['id']] = it
hoje = datetime.datetime(2026, 11, 14, tzinfo=datetime.timezone.utc)
out = []
for vid, it in vids.items():
    s = it['snippet']; st = it['statistics']; c = chinfo.get(s['channelId'], {})
    subs = int(c.get('statistics', {}).get('subscriberCount', 0) or 0)
    pub = datetime.datetime.fromisoformat(s['publishedAt'].replace('Z', '+00:00'))
    views = int(st.get('viewCount', 0))
    out.append(dict(id=vid, busca='+'.join(sorted(rows[vid]['busca'])), canal=s['channelTitle'], channel_id=s['channelId'],
        inscritos=subs, views=views, data=pub.date().isoformat(), idade_d=(hoje - pub).days,
        v_por_insc=round(views / subs, 2) if subs else None, dur=it['contentDetails']['duration'],
        idioma=s.get('defaultAudioLanguage') or s.get('defaultLanguage') or '', titulo=s['title'],
        uploads=c.get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads')))
out.sort(key=lambda r: -r['views'])
with open(os.path.join(base, 'B-busca-enriquecida.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out), 'videos', len(chinfo), 'canais')
