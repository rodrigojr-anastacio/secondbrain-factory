import sys,os,statistics,datetime,json
sys.path.insert(0,os.path.expanduser('~/workspace/fabrica-youtube/tools'))
from trends import yt_client, segundos
D=os.path.dirname(os.path.abspath(__file__))+'/canais-mapa'
yt=yt_client(); hoje=datetime.date.today(); out={}
for l in open(f'{D}/ids.txt'):
    cid,slug=l.split()
    pl=yt.playlistItems().list(part='contentDetails',playlistId='UU'+cid[2:],maxResults=50).execute()
    ids=[i['contentDetails']['videoId'] for i in pl['items']]
    vs=yt.videos().list(part='snippet,statistics,contentDetails',id=','.join(ids)).execute()['items']
    R=[]
    for v in vs:
        d=segundos(v['contentDetails']['duration'])
        if d<240: continue
        pub=v['snippet']['publishedAt'][:10]
        R.append(dict(views=int(v['statistics'].get('viewCount',0)),id=v['id'],titulo=v['snippet']['title'],data=pub,canal=v['snippet']['channelTitle']))
    if not R: continue
    m=statistics.median(r['views'] for r in R)
    for r in R: r['x']=round(r['views']/m,1) if m else 0
    out[slug]=dict(mediana=m,videos=R)
    print(f"\n## {slug} ({R[0]['canal']}) n={len(R)} mediana={m:,.0f}")
    for r in sorted(R,key=lambda r:-r['views'])[:8]:
        print(f"  {r['views']:>9,} {r['x']:6.1f}× {r['data']} {r['id']} {r['titulo'][:90]}")
json.dump(out,open(f'{D}/canais.json','w'),ensure_ascii=False,indent=1)
