import os, sys, json, base64, io, urllib.request
from PIL import Image
F='/home/hermes/workspace/fabrica-youtube/canais/historia-ptbr/videos'
OUT=F+'/003-ira/v2-amostras/thumbs/base'; os.makedirs(OUT,exist_ok=True)
MODEL='fal-ai/nano-banana/edit'
def key():
    for l in open(os.path.expanduser('~/.segredos/fal.env')):
        if l.startswith('FAL_KEY='): return l.split('=',1)[1].strip()
def datauri(p):
    im=Image.open(p).convert('RGB'); im.thumbnail((1024,1024)); b=io.BytesIO(); im.save(b,'JPEG',quality=88)
    return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
REFS=[datauri(F+'/001-egito/imagens/I041.jpg'), datauri(F+'/002-india/imagens/I041.jpg')]
PRE=("Use the two attached images ONLY as the art-style reference: hand-drawn educational cartoon, thick clean black outlines, "
     "flat bright colors, soft cel shading, characters are simple people with ROUND WHITE HEADS, dot eyes and simple expressive faces. "
     "Do not copy their scenes. Draw a NEW image, a bold YouTube thumbnail illustration, wide 16:9: ")
SUF=(" Few big elements, strong contrast, characters drawn LARGE and close to the camera so they read at small size. "
     "Absolutely no text, no letters, no numbers, no words, no signs, no watermark.")
P=json.load(open(sys.argv[1]))
ids=sys.argv[2:]
k=key(); n=0
for c in P:
    if c['id'] not in ids: continue
    body={'prompt':PRE+c['prompt']+SUF,'image_urls':REFS,'num_images':1,'aspect_ratio':'16:9','output_format':'png'}
    req=urllib.request.Request('https://fal.run/'+MODEL,data=json.dumps(body).encode(),method='POST',
        headers={'Authorization':'Key '+k,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=300) as r: d=json.load(r)
        url=d['images'][0]['url']; dst=f"{OUT}/{c['id']}.png"; urllib.request.urlretrieve(url,dst); n+=1
        print(c['id'],'OK',Image.open(dst).size)
    except Exception as e:
        print(c['id'],'ERRO',str(e)[:200], (e.read()[:600] if hasattr(e,'read') else ''))
print('GERADAS',n)
