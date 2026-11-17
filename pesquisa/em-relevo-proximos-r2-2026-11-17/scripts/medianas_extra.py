import sys,json,glob,csv,statistics
sys.path.insert(0,'/home/hermes/workspace/fabrica-youtube/tools')
from trends import yt_client, segundos
snap=json.load(open('snap1.json'))['v']
med={}
for f in glob.glob('q/*/*/medianas.json'): med.update(json.load(open(f)))
falta={v['channel_id'] for v in snap.values()}-set(med)
yt=yt_client(); extra={}
chs=list(falta)
for i in range(0,len(chs),50):
    r=yt.channels().list(part='contentDetails,statistics,snippet',id=','.join(chs[i:i+50])).execute()
    for c in r['items']:
        try:
            pl=yt.playlistItems().list(part='contentDetails',playlistId=c['contentDetails']['relatedPlaylists']['uploads'],maxResults=50).execute()
            vs=[it['contentDetails']['videoId'] for it in pl['items']]
            out=yt.videos().list(part='statistics,contentDetails',id=','.join(vs)).execute()
            longos=[int(x['statistics'].get('viewCount',0)) for x in out['items'] if segundos(x['contentDetails'].get('duration','PT0S'))>=180][:30]
            if longos: extra[c['id']]={'canal':c['snippet']['title'],'mediana':statistics.median(longos),'n':len(longos),'inscritos':int(c['statistics'].get('subscriberCount',0) or 0)}
        except Exception as e: print('erro',c['snippet']['title'],e)
json.dump(extra,open('medianas_extra.json','w'),ensure_ascii=False,indent=1)
print(len(falta),len(extra))
