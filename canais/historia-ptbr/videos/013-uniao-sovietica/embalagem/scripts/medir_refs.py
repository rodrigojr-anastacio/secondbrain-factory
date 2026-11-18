"""Mede referências avulsas: views/data de hoje + mediana real do canal (últimos <=30 longos). Uso: medir_refs.py <pasta embalagem> id1,id2,..."""
import sys, os, json, csv, statistics, datetime, re
sys.path.insert(0, os.path.expanduser('~/workspace/fabrica-youtube/tools'))
from trends import yt_client
def seg(d):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d); dd,h,mi,s = [int(x or 0) for x in m.groups()]; return dd*86400+h*3600+mi*60+s
pasta, ids = sys.argv[1], sys.argv[2].split(',')
yt = yt_client(); med_p = f'{pasta}/medianas.json'; med = json.load(open(med_p)) if os.path.exists(med_p) else {}
vs = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids)).execute()['items']
hoje = datetime.date.today(); out = []
for v in vs:
    cid = v['snippet']['channelId']
    if cid not in med:
        c = yt.channels().list(part='contentDetails,snippet', id=cid).execute()['items'][0]
        pl = yt.playlistItems().list(part='contentDetails', playlistId=c['contentDetails']['relatedPlaylists']['uploads'], maxResults=50).execute()
        x = yt.videos().list(part='statistics,contentDetails', id=','.join(i['contentDetails']['videoId'] for i in pl['items'])).execute()['items']
        longos = [int(y['statistics'].get('viewCount', 0)) for y in x if seg(y['contentDetails'].get('duration','PT0S')) >= 180][:30]
        med[cid] = {'canal': c['snippet']['title'], 'mediana': statistics.median(longos), 'n': len(longos)}
    m = med[cid]; views = int(v['statistics'].get('viewCount', 0)); pub = v['snippet']['publishedAt'][:10]
    out.append({'id': v['id'], 'titulo': v['snippet']['title'], 'canal': m['canal'], 'views': views, 'data': pub,
                'idade_d': (hoje - datetime.date.fromisoformat(pub)).days, 'mediana_canal': m['mediana'], 'n_mediana': m['n'], 'x_mediana': round(views / m['mediana'], 1)})
json.dump(med, open(med_p, 'w'), ensure_ascii=False, indent=1)
f = f'{pasta}/refs-extra.csv'; velho = list(csv.DictReader(open(f))) if os.path.exists(f) else []
ja = {r['id'] for r in out}; todos = [r for r in velho if r['id'] not in ja] + out
w = csv.DictWriter(open(f, 'w'), fieldnames=list(out[0])); w.writeheader(); w.writerows(todos)
for r in out: print(f"{r['id']} {r['views']:>10,} {r['data']} {r['idade_d']:>4}d med {r['mediana_canal']:>10,.0f} {r['x_mediana']:>6}× {r['canal'][:22]} | {r['titulo'][:70]}")
