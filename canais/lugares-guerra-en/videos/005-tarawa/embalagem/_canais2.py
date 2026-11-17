import sys,datetime,statistics
sys.path.insert(0,'/home/hermes/workspace/fabrica-youtube/tools')
from trends import yt_client, segundos
yt=yt_client(); cota=0
CH={'Long After The Guns':'UCXIMjn_vXy3W2_hb2c25HJw','Hallowed Ground Today':'UCDcjufNGwP21m4BjluLHvMQ','Untold War Archives':'UC6JMkTezp7k1EyA3BWL5YXw','The Steel Record':'UCSGyfIp98QRoR13zWwxitkg','War Documents':'UCW9U_ta2TtQ2jqgdQnS1H1Q','The Burned Records':'UCnIDvncRe-f3dd0wTKzPU7g','Markets of the Past':'UCPDCiU00ugujWP8H2HMbiFA','InsideWorldWarTwo':'UCzG5opghptFgBPxyTDLys9g','Absolute History':'UCr5qeBG9g7bGtMGyHG2GzbQ','Like Stories of Old':'UCs7nPQIEba0T3tGOWWsZpJQ'}
for nome,cid in CH.items():
    r=yt.playlistItems().list(part='contentDetails',playlistId='UU'+cid[2:],maxResults=50).execute(); cota+=1
    ids=[i['contentDetails']['videoId'] for i in r['items']]
    v=yt.videos().list(part='snippet,statistics,contentDetails',id=','.join(ids)).execute()['items']; cota+=1
    vs=sorted([(x['snippet']['publishedAt'][:10],int(x['statistics'].get('viewCount',0)),segundos(x['contentDetails']['duration']),x['snippet']['title']) for x in v],reverse=True)
    lg=[x[1] for x in vs if x[2]>=180][:30]
    med=statistics.median(lg) if lg else 0
    print(f'## {nome} mediana({len(lg)}) = {med:.0f}')
    for d,vw,du,t in sorted(vs,key=lambda x:-x[1])[:6]: print(f'   {d} {vw:>8} {vw/med if med else 0:5.1f}x {t[:100]}')
print('COTA',cota)
