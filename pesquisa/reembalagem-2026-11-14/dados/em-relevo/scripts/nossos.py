import sys, json
sys.path.insert(0,'/home/hermes/workspace/fabrica-youtube/tools')
from trends import yt_client
yt=yt_client()
r=yt.videos().list(part='snippet,contentDetails,statistics',id='bG6-E4qjXYc,FeSLzHvlkbo').execute()
out=[]
for it in r['items']:
    out.append(dict(id=it['id'],title=it['snippet']['title'],pub=it['snippet']['publishedAt'],dur=it['contentDetails']['duration'],views=it['statistics'].get('viewCount'),ch=it['snippet']['channelId'],desc=it['snippet']['description'][:400],tags=it['snippet'].get('tags')))
print(json.dumps(out,ensure_ascii=False,indent=1))
json.dump(out,open('/home/hermes/workspace/fabrica-youtube/pesquisa/reembalagem-2026-11-14/dados/em-relevo/nossos.json','w'),ensure_ascii=False,indent=1)
