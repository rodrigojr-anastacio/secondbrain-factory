import sys,datetime,statistics,json
sys.path.insert(0,'/home/hermes/workspace/fabrica-youtube/tools')
from trends import yt_client, segundos
yt=yt_client(); cota=0
CH={'Where They Stood':('UCUt7wPSxHRObHObdAW-26JQ',40),'Forgotten Fleet':('UCyL5J-lo3XuYPPOiXvzbAWw',20),'Still Inside':('UC8kCQ7F8KwX1R2wMYZkzjYw',20),'The Staff Ride':('UC3au-kowYkcOfJWBXCju-2w',20)}
hoje=datetime.date.today()
for nome,(cid,n) in CH.items():
    up='UU'+cid[2:]
    r=yt.playlistItems().list(part='contentDetails',playlistId=up,maxResults=50).execute(); cota+=1
    ids=[i['contentDetails']['videoId'] for i in r['items']]
    v=yt.videos().list(part='snippet,statistics,contentDetails',id=','.join(ids)).execute()['items']; cota+=1
    vs=[(x['snippet']['publishedAt'][:10],int(x['statistics'].get('viewCount',0)),segundos(x['contentDetails']['duration']),x['snippet']['title'],x['id']) for x in v]
    vs.sort(reverse=True)
    med=statistics.median([x[1] for x in vs if x[2]>=180][:30] or [0])
    print(f'\n## {nome} (mediana últimos ≤30 longos: {med:.0f})')
    for d,vw,du,t,i in vs[:n]:
        print(f'{d} | {vw:>8} | {vw/med if med else 0:5.1f}x | {du//60}m | {t} | https://youtu.be/{i}')
print('\nCOTA',cota)
