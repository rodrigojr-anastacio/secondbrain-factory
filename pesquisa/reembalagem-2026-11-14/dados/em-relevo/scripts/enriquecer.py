import sys, json, glob, statistics, datetime, re, csv
sys.path.insert(0,'/home/hermes/workspace/fabrica-youtube/tools')
from trends import yt_client
yt=yt_client()
BASE='/home/hermes/workspace/fabrica-youtube/pesquisa/reembalagem-2026-11-14/dados/em-relevo/'
queries=['por que o sul do brasil tem tantos tornados','corredor de tornados brasil','tornados no sul do brasil','tornado santa catarina','tornado rio bonito do iguaçu','como se forma um tornado supercélula','beco dos tornados américa do sul','tornado alley south america','el niño 2026','super el niño','el niño mais forte da história','el niño brasil verão','o que é el niño','el niño 2026 brasil chuva sul seca norte','super el nino 2026 strongest','el niño 2026 más fuerte de la historia']
hits={}
for i,q in enumerate(queries,1):
    for line in open(BASE+f'busca/{i:02d}.jsonl'):
        d=json.loads(line); hits.setdefault(d['id'],[]).append(q)
ids=list(hits)
def dur(s):
    m=re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?',s); d,h,mi,se=[int(x or 0) for x in m.groups()]; return d*86400+h*3600+mi*60+se
vids={}
for k in range(0,len(ids),50):
    r=yt.videos().list(part='snippet,contentDetails,statistics',id=','.join(ids[k:k+50])).execute()
    for it in r['items']:
        vids[it['id']]=dict(id=it['id'],titulo=it['snippet']['title'],canal=it['snippet']['channelTitle'],ch=it['snippet']['channelId'],data=it['snippet']['publishedAt'][:10],dur_s=dur(it['contentDetails'].get('duration','PT0S')),views=int(it['statistics'].get('viewCount',0)),lang=it['snippet'].get('defaultAudioLanguage',''),buscas=hits[it['id']])
chs=list({v['ch'] for v in vids.values()})
chinfo={}
for k in range(0,len(chs),50):
    r=yt.channels().list(part='statistics,contentDetails,snippet',id=','.join(chs[k:k+50])).execute()
    for it in r['items']:
        chinfo[it['id']]=dict(nome=it['snippet']['title'],insc=int(it['statistics'].get('subscriberCount',0)),uploads=it['contentDetails']['relatedPlaylists']['uploads'])
hoje=datetime.date(2026,11,14)
for v in vids.values():
    c=chinfo.get(v['ch'],{}); v['inscritos']=c.get('insc',0)
    v['idade_d']=(hoje-datetime.date.fromisoformat(v['data'])).days
    v['v_por_insc']=round(v['views']/v['inscritos'],2) if v['inscritos'] else None
json.dump(dict(videos=vids,canais=chinfo),open(BASE+'busca-enriquecida.json','w'),ensure_ascii=False,indent=1)
print(len(vids),len(chinfo))
