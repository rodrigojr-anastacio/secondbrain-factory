# refs de padrões (bíblia) re-medidas via yt-dlp (Data API fora em 23/11/2026)
import json,subprocess,statistics,sys,os
Y=os.path.expanduser('~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp'); PX='socks5://127.0.0.1:40000'
def j(args,t=120):
    r=subprocess.run(['timeout',str(t),Y,'--proxy',PX,'--dump-json','--no-warnings',*args],capture_output=True,text=True)
    o=[]
    for l in r.stdout.splitlines():
        try:o.append(json.loads(l))
        except:pass
    return o
out={}; med={}
mp='medianas.json'; 
if os.path.exists(mp): med=json.load(open(mp))
for vid in sys.argv[1].split(','):
    d=j(['--skip-download',f'https://www.youtube.com/watch?v={vid}'],90)
    if not d: print(vid,'falhou'); continue
    d=d[0]; cid=d['channel_id']
    if cid not in med:
        e=j(['--flat-playlist','--playlist-end','40',f'https://www.youtube.com/channel/{cid}/videos'])
        lg=[int(x['view_count']) for x in e if x.get('view_count') and (x.get('duration') or 0)>=180][:30]
        if lg: med[cid]={'canal':d.get('channel'),'mediana':statistics.median(lg),'n':len(lg),'fonte':'yt-dlp aba /videos'}
    m=med.get(cid,{}).get('mediana')
    ud=d.get('upload_date') or ''
    out[vid]={'titulo':d.get('title'),'canal':d.get('channel'),'views':d.get('view_count'),'data':f'{ud[:4]}-{ud[4:6]}-{ud[6:]}','mediana':m,'xmed':round(d['view_count']/m,1) if m else None}
    print(vid,out[vid])
json.dump(med,open(mp,'w'),ensure_ascii=False,indent=1)
old=json.load(open('refs-padroes.json')) if os.path.exists('refs-padroes.json') else {}
old.update(out); json.dump(old,open('refs-padroes.json','w'),ensure_ascii=False,indent=1)
