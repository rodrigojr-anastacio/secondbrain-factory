# B2: enriquece as buscas B2-ytsearch-*.jsonl (videos.list + channels.list), sem search.list
import sys, os, json, glob, csv, datetime
sys.path.insert(0, os.path.expanduser('~/workspace/fabrica-youtube/tools'))
from trends import yt_client
yt = yt_client()
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = {}
for f in sorted(glob.glob(os.path.join(base, 'raw', 'B2-ytsearch-*.jsonl'))):
    q = os.path.basename(f)[len('B2-ytsearch-'):-6]
    for line in open(f):
        try: d = json.loads(line)
        except: continue
        if d.get('id') and len(d['id']) == 11:
            rows.setdefault(d['id'], set()).add(q)
ids = list(rows); vids = {}
for i in range(0, len(ids), 50):
    for it in yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50])).execute()['items']: vids[it['id']] = it
chs = list({v['snippet']['channelId'] for v in vids.values()}); chinfo = {}
for i in range(0, len(chs), 50):
    for it in yt.channels().list(part='statistics', id=','.join(chs[i:i+50])).execute()['items']: chinfo[it['id']] = it
hoje = datetime.datetime(2026, 11, 14, tzinfo=datetime.timezone.utc); out = []
for vid, it in vids.items():
    s = it['snippet']; st = it['statistics']
    subs = int(chinfo.get(s['channelId'], {}).get('statistics', {}).get('subscriberCount', 0) or 0)
    pub = datetime.datetime.fromisoformat(s['publishedAt'].replace('Z', '+00:00'))
    out.append(dict(id=vid, busca='+'.join(sorted(rows[vid])), canal=s['channelTitle'], channel_id=s['channelId'], inscritos=subs,
        views=int(st.get('viewCount', 0)), data=pub.date().isoformat(), idade_d=(hoje - pub).days, dur=it['contentDetails']['duration'],
        idioma=s.get('defaultAudioLanguage') or s.get('defaultLanguage') or '', titulo=s['title']))
out.sort(key=lambda r: -r['views'])
with open(os.path.join(base, 'B2-busca-enriquecida.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out))
