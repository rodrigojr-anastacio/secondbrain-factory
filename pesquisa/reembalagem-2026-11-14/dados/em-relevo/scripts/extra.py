import sys, json, re, statistics, datetime
sys.path.insert(0,'/home/hermes/workspace/fabrica-youtube/tools')
from trends import yt_client
yt=yt_client(); B='/home/hermes/workspace/fabrica-youtube/pesquisa/reembalagem-2026-11-14/dados/em-relevo/'
def dur(s):
    m=re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?',s or 'PT0S'); dd,h,mi,se=[int(x or 0) for x in m.groups()]; return dd*86400+h*3600+mi*60+se
res={}
for f in ['17','18','19']:
    ids=[json.loads(l)['id'] for l in open(B+f'busca/{f}.jsonl')]
    r=yt.videos().list(part='snippet,contentDetails,statistics',id=','.join(ids)).execute()['items']
    chs=list({i['snippet']['channelId'] for i in r})
    ci={c['id']:int(c['statistics'].get('subscriberCount',0)) for c in yt.channels().list(part='statistics',id=','.join(chs)).execute()['items']}
    res[f]=[]
    for i in r:
        x=dict(id=i['id'],titulo=i['snippet']['title'],canal=i['snippet']['channelTitle'],ch=i['snippet']['channelId'],data=i['snippet']['publishedAt'][:10],dur_s=dur(i['contentDetails'].get('duration')),views=int(i['statistics'].get('viewCount',0)),inscritos=ci.get(i['snippet']['channelId'],0))
        res[f].append(x)
    print('==',f)
    for x in sorted(res[f],key=lambda x:-x['views'])[:14]:
        print(f"{x['views']:>9} {x['inscritos']:>8} {x['data']} {x['dur_s']//60}m {x['id']} {x['canal'][:22]} | {x['titulo'][:95]}")
# medianas extra
def mediana(cid):
    up='UU'+cid[2:]
    ids=[i['contentDetails']['videoId'] for i in yt.playlistItems().list(part='contentDetails',playlistId=up,maxResults=50).execute()['items']]
    vs=yt.videos().list(part='statistics,contentDetails',id=','.join(ids)).execute()['items']
    l=[int(v['statistics'].get('viewCount',0)) for v in vs if dur(v['contentDetails'].get('duration'))>=180][:30]
    return statistics.median(l) if l else None, len(l)
r=yt.videos().list(part='snippet',id='ZVgiR9yIcGo,RtxANcgG_Ig,J4vI8IWCFMk,B5wO2fViQwc').execute()['items']
med={}
for i in r:
    med[i['snippet']['channelTitle']]=mediana(i['snippet']['channelId']); print(i['snippet']['channelTitle'],med[i['snippet']['channelTitle']])
json.dump(dict(buscas=res,medianas=med),open(B+'busca-extra.json','w'),ensure_ascii=False,indent=1)
