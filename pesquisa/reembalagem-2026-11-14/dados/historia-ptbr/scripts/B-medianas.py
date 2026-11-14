import sys, os, json, csv, statistics, re
sys.path.insert(0, os.path.expanduser('~/workspace/fabrica-youtube/tools'))
from trends import yt_client
yt = yt_client()
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(base, 'B-busca-enriquecida.csv'))))
extra_ids = sys.argv[1].split(',') if len(sys.argv) > 1 else []
# vídeos extras (referências conhecidas fora da busca)
extra = []
if extra_ids:
    r = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(extra_ids)).execute()
    for it in r['items']:
        extra.append(dict(id=it['id'], canal=it['snippet']['channelTitle'], channel_id=it['snippet']['channelId'], views=it['statistics'].get('viewCount'), data=it['snippet']['publishedAt'][:10], dur=it['contentDetails']['duration'], titulo=it['snippet']['title']))
chans = {}
for r in rows:
    if int(r['idade_d']) <= 420 and int(r['views']) >= 20000:
        chans[r['channel_id']] = r['canal']
for e in extra: chans[e['channel_id']] = e['canal']
def secs(d):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d); a = [int(x or 0) for x in m.groups()]
    return a[0]*86400 + a[1]*3600 + a[2]*60 + a[3]
res = {}
for cid, nome in chans.items():
    up = 'UU' + cid[2:]
    try:
        pl = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50).execute()
    except Exception as ex:
        res[cid] = dict(canal=nome, erro=str(ex)[:80]); continue
    vids = [i['contentDetails']['videoId'] for i in pl['items']]
    if not vids: continue
    v = yt.videos().list(part='statistics,contentDetails', id=','.join(vids)).execute()['items']
    longos = [int(x['statistics'].get('viewCount', 0)) for x in v if secs(x['contentDetails'].get('duration','PT0S')) > 180][:30]
    res[cid] = dict(canal=nome, n_longos=len(longos), mediana_longos=statistics.median(longos) if longos else None)
json.dump(dict(medianas=res, extras=extra), open(os.path.join(base, 'B-medianas-canais.json'), 'w'), ensure_ascii=False, indent=1)
for cid, d in sorted(res.items(), key=lambda x: x[1].get('canal', '')): print(d)
for e in extra: print(e)
