# B2: para cada vídeo-referência: videos.list (views/data/título) + mediana real do canal
# (últimos 50 uploads via playlistItems + videos.list; mediana de todos e só longos > 3 min). Sem search.list.
import sys, os, json, re, statistics
sys.path.insert(0, os.path.expanduser('~/workspace/fabrica-youtube/tools'))
from trends import yt_client
yt = yt_client()
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ids = sys.argv[1].split(',')
def secs(d):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d); a = [int(x or 0) for x in m.groups()]
    return a[0]*86400 + a[1]*3600 + a[2]*60 + a[3]
vids = {}
for i in range(0, len(ids), 50):
    for it in yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i+50])).execute()['items']: vids[it['id']] = it
cache_f = os.path.join(base, 'B2-medianas-canais.json')
cache = json.load(open(cache_f)) if os.path.exists(cache_f) else {}
for v in vids.values():
    cid = v['snippet']['channelId']
    if cid in cache: continue
    pl = yt.playlistItems().list(part='contentDetails', playlistId='UU' + cid[2:], maxResults=50).execute()
    up = [i['contentDetails']['videoId'] for i in pl['items']]
    st = yt.videos().list(part='statistics,contentDetails', id=','.join(up)).execute()['items']
    todos = [int(x['statistics'].get('viewCount', 0)) for x in st]
    longos = [int(x['statistics'].get('viewCount', 0)) for x in st if secs(x['contentDetails'].get('duration', 'PT0S')) > 180]
    ch = yt.channels().list(part='statistics', id=cid).execute()['items'][0]['statistics']
    cache[cid] = dict(canal=v['snippet']['channelTitle'], inscritos=int(ch.get('subscriberCount', 0)), n=len(todos), mediana_todos=statistics.median(todos) if todos else None,
                      n_longos=len(longos), mediana_longos=statistics.median(longos) if longos else None)
json.dump(cache, open(cache_f, 'w'), ensure_ascii=False, indent=1)
out_f = os.path.join(base, 'B2-referencias.json')
refs = json.load(open(out_f)) if os.path.exists(out_f) else {}
for vid, v in vids.items():
    c = cache[v['snippet']['channelId']]; views = int(v['statistics'].get('viewCount', 0))
    med = max(x for x in (c['mediana_todos'], c['mediana_longos']) if x is not None)
    refs[vid] = dict(id=vid, canal=c['canal'], inscritos=c['inscritos'], views=views, data=v['snippet']['publishedAt'][:10], titulo=v['snippet']['title'],
                     dur=secs(v['contentDetails']['duration']), mediana_todos=c['mediana_todos'], n=c['n'], mediana_longos=c['mediana_longos'], n_longos=c['n_longos'],
                     x_mediana=round(views / med, 1) if med else None)
    r = refs[vid]
    print(f"{vid} | {r['canal'][:24]} | {r['inscritos']} insc | {views} | {r['data']} | med50 {r['mediana_todos']} (n{r['n']}) | medlongos {r['mediana_longos']} (n{r['n_longos']}) | {r['x_mediana']}x | {r['titulo'][:80]}")
json.dump(refs, open(out_f, 'w'), ensure_ascii=False, indent=1)
