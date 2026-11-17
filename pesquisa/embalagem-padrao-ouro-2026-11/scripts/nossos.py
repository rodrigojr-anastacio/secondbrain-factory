#!/usr/bin/env python3
"""Embalagens no ar dos nossos canais ativos: título ao vivo (videos.list), thumb maxres via WARP, CTR (alcance_diario)."""
import csv, os, subprocess, sys
ROOT=os.path.expanduser('~/workspace/fabrica-youtube'); OUT=f'{ROOT}/pesquisa/embalagem-padrao-ouro-2026-11'
sys.path.insert(0,f'{ROOT}/tools')
from trends import yt_client
import psycopg
con=psycopg.connect('dbname=vida')
q="""select v.canal_slug,v.id,v.numero,v.youtube_id,
 (select sum(impressoes) from youtube.alcance_diario a where a.video_id=v.youtube_id) impr,
 (select round(100*sum(impressoes*ctr)/nullif(sum(impressoes),0),2) from youtube.alcance_diario a where a.video_id=v.youtube_id) ctr
 from youtube.videos v where v.youtube_id is not null and v.canal_slug in ('historia-ptbr','dossie-es','em-relevo','lugares-guerra-en') order by 1,v.numero nulls last"""
rows=con.execute(q).fetchall(); yt=yt_client(); info={}
ids=[r[3] for r in rows]
for i in range(0,len(ids),50):
    for v in yt.videos().list(part='snippet,statistics,status,contentDetails',id=','.join(ids[i:i+50])).execute()['items']:
        info[v['id']]=v
os.makedirs(f'{OUT}/thumbs/nossos',exist_ok=True)
w=csv.writer(open(f'{OUT}/corpus/nossos.csv','w',newline=''))
w.writerow(['canal','video_db','numero','video_id','status','publicado','views','impressoes','ctr_pct','titulo_ao_vivo','n_chars','thumb'])
for c,vid,num,y,impr,ctr in rows:
    v=info.get(y)
    if not v: w.writerow([c,vid,num,y,'indisponivel','','',impr,ctr,'','','']); continue
    f=f'{OUT}/thumbs/nossos/{c}-{num or vid}-{y}.jpg'
    for qq in ('maxresdefault','hqdefault'):
        subprocess.run(['curl','-s','--max-time','30','--socks5-hostname','127.0.0.1:40000','-o',f,f'https://i.ytimg.com/vi/{y}/{qq}.jpg'])
        if os.path.getsize(f)>3000: break
    t=v['snippet']['title']
    w.writerow([c,vid,num,y,v['status']['privacyStatus'],v['snippet']['publishedAt'][:10],v['statistics'].get('viewCount'),impr,ctr,t,len(t),os.path.relpath(f,OUT)])
print('ok',len(rows),len(info))
