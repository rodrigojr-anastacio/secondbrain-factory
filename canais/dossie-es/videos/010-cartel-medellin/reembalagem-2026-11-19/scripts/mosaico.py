#!/usr/bin/env python3
"""Grade 4x3 (nossa no centro, linha 2 col 2) a 160x90 e 320x180, ou mosaico rotulado.
Uso: mosaico.py <saida_sem_ext> <nossa.jpg|-> id1,id2,... [--rotulos]"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
D=os.path.dirname(os.path.abspath(__file__))+'/../thumbs'
out,nossa,ids=sys.argv[1],sys.argv[2],sys.argv[3].split(',')
def get(v):
    f=f'{D}/{v}.jpg'
    if not os.path.exists(f) or os.path.getsize(f)<3000:
        subprocess.run(['curl','-s','--max-time','30','--socks5-hostname','127.0.0.1:40000','-o',f,f'https://i.ytimg.com/vi/{v}/hqdefault.jpg'])
    im=Image.open(f).convert('RGB'); w,h=im.size
    if abs(w/h-16/9)>0.05: nh=int(w*9/16); im=im.crop((0,(h-nh)//2,w,(h-nh)//2+nh))
    return im
ims=[get(v) for v in ids]
if nossa!='-': ims.insert(5,Image.open(nossa).convert('RGB'))
cols=4
for W,H,g in ((160,90,4),(320,180,6)):
    n=len(ims); rows=(n+cols-1)//cols
    img=Image.new('RGB',(cols*W+(cols-1)*g,rows*H+(rows-1)*g),'white')
    for i,im in enumerate(ims): img.paste(im.resize((W,H)),((i%cols)*(W+g),(i//cols)*(H+g)))
    img.save(f'{out}-{W}.jpg',quality=88)
print(out,len(ims))
