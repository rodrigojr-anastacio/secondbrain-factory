import sys, json, statistics, re
sys.path.insert(0,'/home/hermes/workspace/fabrica-youtube/tools')
from trends import yt_client
yt=yt_client()
B='/home/hermes/workspace/fabrica-youtube/pesquisa/reembalagem-2026-11-14/dados/em-relevo/r2/'
def dur(s):
    m=re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?',s or 'PT0S'); dd,h,mi,se=[int(x or 0) for x in m.groups()]; return dd*86400+h*3600+mi*60+se
# resolve channel ids from video ids given
vids=sys.argv[1].split(',')
r=yt.videos().list(part='snippet',id=','.join(vids)).execute()
cids=list(dict.fromkeys(it['snippet']['channelId'] for it in r['items']))
out={}
for cid in cids:
    c=yt.channels().list(part='statistics,contentDetails,snippet',id=cid).execute()['items'][0]
    up=c['contentDetails']['relatedPlaylists']['uploads']
    pl=yt.playlistItems().list(part='contentDetails',playlistId=up,maxResults=50).execute()
    ids=[i['contentDetails']['videoId'] for i in pl['items']]
    vs=yt.videos().list(part='snippet,statistics,contentDetails',id=','.join(ids)).execute()['items']
    rows=[dict(id=v['id'],t=v['snippet']['title'],d=v['snippet']['publishedAt'][:10],v=int(v['statistics'].get('viewCount',0)),s=dur(v['contentDetails']['duration'])) for v in vs]
    longos=[x for x in rows if x['s']>180]
    med=statistics.median([x['v'] for x in longos]) if longos else None
    out[cid]=dict(nome=c['snippet']['title'],insc=int(c['statistics'].get('subscriberCount',0)),n_uploads=len(rows),n_longos=len(longos),mediana_longos=med,videos=rows)
    print(f"\n### {c['snippet']['title']} insc={out[cid]['insc']} uploads={len(rows)} longos={len(longos)} mediana_longos={med}")
    for x in sorted(longos,key=lambda x:-x['v']):
        print(f"  {x['id']} {x['d']} {x['v']:>9} {x['v']/med:5.1f}x | {x['t'][:95]}")
json.dump(out,open(B+'uploads-'+sys.argv[2]+'.json','w'),ensure_ascii=False,indent=1)
