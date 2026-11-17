#!/usr/bin/env python3
"""Teste da grade: nossa thumb + 11 concorrentes do tema (busca yt-dlp via WARP, custo zero), a 160x90 e 320x180.
Uso: grade.py <rotulo> <nosso_video_id> <idioma> "<consulta>"  → grades/<rotulo>-160.jpg, -320.jpg, -refs.json"""
import json, os, subprocess, sys
from PIL import Image
ROOT=os.path.expanduser('~/workspace/fabrica-youtube'); OUT=f'{ROOT}/pesquisa/embalagem-padrao-ouro-2026-11'
YT=f'{ROOT}/tools/.venv/bin/yt-dlp'
rot,nosso,lang,q=sys.argv[1:5]
os.makedirs(f'{OUT}/grades/thumbs',exist_ok=True)
p=subprocess.run(['timeout','150',YT,'--proxy','socks5://127.0.0.1:40000','--extractor-args',f'youtube:lang={lang}','--flat-playlist','--dump-json',f'ytsearch40:{q}'],capture_output=True,text=True)
vs=[]
for l in p.stdout.splitlines():
    try: d=json.loads(l)
    except Exception: continue
    if d.get('id')==nosso or not d.get('duration') or d['duration']<180: continue
    vs.append({'id':d['id'],'titulo':d.get('title'),'canal':d.get('channel'),'views':d.get('view_count') or 0})
vs=sorted(vs,key=lambda x:-x['views'])[:11]
def thumb(v):
    f=f'{OUT}/grades/thumbs/{v}.jpg'
    if not os.path.exists(f) or os.path.getsize(f)<3000:
        subprocess.run(['curl','-s','--max-time','30','--socks5-hostname','127.0.0.1:40000','-o',f,f'https://i.ytimg.com/vi/{v}/hqdefault.jpg'])
    im=Image.open(f).convert('RGB'); w,h=im.size
    if abs(w/h-16/9)>0.05:  # hqdefault 4:3 com tarjas: corta para 16:9
        nh=int(w*9/16); im=im.crop((0,(h-nh)//2,w,(h-nh)//2+nh))
    return im
ids=[v['id'] for v in vs]; ids.insert(5,nosso)
for W,H,g in ((160,90,4),(320,180,6)):
    img=Image.new('RGB',(4*W+3*g,3*H+2*g),'white')
    for i,v in enumerate(ids[:12]):
        img.paste(thumb(v).resize((W,H)),((i%4)*(W+g),(i//4)*(H+g)))
    img.save(f'{OUT}/grades/{rot}-{W}.jpg',quality=88)
json.dump({'consulta':q,'nosso':nosso,'posicao_nossa':'linha 2, coluna 2','concorrentes':vs},open(f'{OUT}/grades/{rot}-refs.json','w'),ensure_ascii=False,indent=1)
print(rot,len(vs))
