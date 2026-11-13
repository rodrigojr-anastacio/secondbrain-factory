"""Puxa os últimos ~60 vídeos (views) + datas do RSS de cada canal de referência, via WARP."""
import json, subprocess, sys, re, urllib.request, concurrent.futures as cf
P='socks5://127.0.0.1:40000'
YT='/home/hermes/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp'
CANAIS={
 'hist':{'History in Minutes':'UCYjRQ6T2BxBnJtPytI9OnNg','Genius History':'UC-q0RDBWjYlYA2KkPzq0WSQ','CountryCorns':'UCKWRnsyYbPFgWclCF0_yOTw',
   'Historia em Minutos (5eT)':'UC5eTe96eJuE4gkyJ5IQ5Fww','A HISTORIA EM MINUTOS':'UCSNvRxMppnEfGEHha2vM1Wg','Historia em Minutos (TJ5)':'UCTJ5pQhUbm6CyszLfqR8Urg',
   'Historia em minutos (uqu)':'UCuquAW2-sxlV0G4N9RuvqaQ','Historia em Minutos (vVu)':'UCvVuEJAqFAgqtn1IbA11UQw','Historia em Minutos (yOr)':'UCyOrXqAEQpKKHreTYqOqdEw'},
 'dos':{'Archive in Minutes':'UCFp0Rk-ad8JD78Qw9nEJ29w','Atlas del Tiempo':'UCku9KB11TReyHHC1kK9CCEw','Te lo Pinto':'UCrkONla60pQPsppl7PPDHyQ','Historia Total':'UC6ZUELsUCkrHF5ZO4m4hpMQ'},
 'rel':{'Mundo Entropico':'UCfM8cvYaVCsz9NgyKMRVFNw','Chao do Sul':'UCQZJSIL-0P-eL25pwLLbJFg','Mapa Verso':'UC734965gYfz7LPY2QQ66cVg','The Last Day':'UCN6XxorahzAiDNyRnI1of2g','Astrum Earth':'UCWBtLCE-BnzZx3DneqDiXWQ','Geografia con Geoff':'UCcWOL02JEjNmxcU6UVDqEPg'},
 'cr':{'Where They Stood':'UCUt7wPSxHRObHObdAW-26JQ','Civil War Fine Print':'UCE1gBqF9TF6JswS0zsxdGTg'},
 'nossos':{'historia-ptbr':'UCpw08sVZG1QZp-3spPcwWxQ','dossie-es':'UCVCYqeuCwTWC7Lqez_qeWRA','em-relevo':'UCXw-Q07-pIPlwMX9ypuLN0A','clearance':'UCou1N3ySJ_9mX6NY_pIM0Aw'},
}
def rss(cid):
    op=urllib.request.build_opener()
    try:
        import socks  # noqa
    except ImportError: pass
    r=subprocess.run(['curl','-s','--max-time','40','--socks5-hostname','127.0.0.1:40000',f'https://www.youtube.com/feeds/videos.xml?channel_id={cid}'],capture_output=True,text=True)
    return dict(re.findall(r'<yt:videoId>([\w-]+)</yt:videoId>.*?<published>([\d-]+)T',r.stdout,re.S))
def get(nome,cid,n=60):
    r=subprocess.run([YT,'--proxy',P,'--flat-playlist','-J','--playlist-end',str(n),f'https://www.youtube.com/channel/{cid}/videos'],capture_output=True,text=True,timeout=300)
    try: d=json.loads(r.stdout)
    except Exception: return {'nome':nome,'erro':r.stderr[-300:]}
    datas=rss(cid)
    vs=[{'id':e['id'],'t':e.get('title'),'v':e.get('view_count'),'dur':e.get('duration'),'data':datas.get(e['id'])} for e in d.get('entries',[])]
    return {'nome':nome,'cid':cid,'insc':d.get('channel_follower_count'),'videos':vs}
out={}
jobs=[(g,n,c) for g,m in CANAIS.items() for n,c in m.items()]
with cf.ThreadPoolExecutor(4) as ex:
    fs={ex.submit(get,n,c):(g,n) for g,n,c in jobs}
    for f in cf.as_completed(fs):
        g,n=fs[f]; out.setdefault(g,{})[n]=f.result(); print(g,n,len(out[g][n].get('videos',[])),out[g][n].get('insc'),file=sys.stderr)
json.dump(out,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
