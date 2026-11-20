# Confere views/data e mediana real (últimos ≤30 longos) das referências de padrão. Uso: python refs_padroes.py id1,id2,...
import sys, json, csv, statistics, datetime, os
sys.path.insert(0, os.path.expanduser('~/workspace/fabrica-youtube/tools'))
from trends import yt_client, segundos
yt = yt_client(); ids = sys.argv[1].split(','); cota = 0
vids = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids)).execute()['items']; cota += 1
chs = {c['id']: c for c in yt.channels().list(part='snippet,contentDetails', id=','.join({v['snippet']['channelId'] for v in vids})).execute()['items']}; cota += 1
med = {}
for cid, c in chs.items():
    pl = yt.playlistItems().list(part='contentDetails', playlistId=c['contentDetails']['relatedPlaylists']['uploads'], maxResults=50).execute(); cota += 1
    vs = [it['contentDetails']['videoId'] for it in pl['items']]
    out = yt.videos().list(part='statistics,contentDetails', id=','.join(vs)).execute(); cota += 1
    longos = [int(x['statistics'].get('viewCount', 0)) for x in out['items'] if segundos(x['contentDetails'].get('duration','PT0S')) >= 180][:30]
    med[cid] = statistics.median(longos) if longos else None
hoje = datetime.date.today(); rows = []
for v in vids:
    m = med[v['snippet']['channelId']]; views = int(v['statistics'].get('viewCount', 0)); pub = v['snippet']['publishedAt'][:10]
    rows.append(dict(id=v['id'], canal=chs[v['snippet']['channelId']]['snippet']['title'], views=views, data=pub,
                     idade_d=(hoje - datetime.date.fromisoformat(pub)).days, mediana=m, x=round(views / m, 1) if m else '', titulo=v['snippet']['title']))
with open('refs-padroes.csv', 'w') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(r['id'], r['canal'][:22], f"{r['views']:,}", r['data'], r['idade_d'], r['mediana'], r['x'], r['titulo'][:60])
print('cota', cota)
