import sys,json,datetime,os
sys.path.insert(0,'/home/hermes/workspace/fabrica-youtube/tools')
from trends import yt_client
ids=[]
for l in open('evidencias.tsv'):
    ids+=l.split('\t')[1].split()
ids=list(dict.fromkeys(ids)); yt=yt_client(); out={}
for i in range(0,len(ids),50):
    r=yt.videos().list(part='statistics,snippet',id=','.join(ids[i:i+50])).execute()
    for v in r['items']: out[v['id']]={'views':int(v['statistics'].get('viewCount',0)),'pub':v['snippet']['publishedAt'],'titulo':v['snippet']['title'],'canal':v['snippet']['channelTitle'],'channel_id':v['snippet']['channelId']}
ts=datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump({'ts':ts,'v':out},open(sys.argv[1],'w'),ensure_ascii=False,indent=0)
print(ts,len(ids),len(out))
