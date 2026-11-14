import sys, json
from PIL import Image, ImageDraw, ImageFont
B='/home/hermes/workspace/fabrica-youtube/pesquisa/reembalagem-2026-11-14/'
d=json.load(open(B+'dados/em-relevo/busca-enriquecida.json'))['videos']
lab={'bG6-E4qjXYc':'NOSSO Sul · 15 views','FeSLzHvlkbo':'NOSSO El Niño · 14 views','xpBOF8FXXHM':'Chão do Sul 736 mil','CMHf4Cqpcrs':'Mundo Entrópico 447 mil'}
def label(i):
    if i in lab: return lab[i]
    v=d.get(i); 
    return f"{v['canal'][:18]} {v['views']/1000:.0f} mil" if v['views']<1e6 else f"{v['canal'][:18]} {v['views']/1e6:.1f} mi"
def mos(ids,out,cols=4):
    W,H=480,270; rows=(len(ids)+cols-1)//cols
    img=Image.new('RGB',(cols*W,rows*(H+28)),'black'); dr=ImageDraw.Draw(img)
    try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20)
    except: f=ImageFont.load_default()
    for k,i in enumerate(ids):
        t=Image.open(B+f'dados/em-relevo/thumbs/{i}.jpg').convert('RGB')
        w,h=t.size; t=t.crop((0,int(h*0.125),w,int(h*0.875))).resize((W,H))
        x=(k%cols)*W; y=(k//cols)*(H+28)
        img.paste(t,(x,y)); dr.text((x+6,y+H+3),label(i),fill='yellow' if 'NOSSO' in label(i) else 'white',font=f)
    img.save(out,quality=82); print(out)
mos(['bG6-E4qjXYc','5UTQ4KrtVGc','7GE2xL75W7Q','h04CSUPoKX0','j0aoIeu8Q3E','x_xE2HyxQE0','xpBOF8FXXHM','CMHf4Cqpcrs','_-eh-KSyaLU','TfTiDfsKK04','GflY4TuNV30','v7xUCFOQdxM'],B+'mosaicos/em-relevo-sul.jpg')
mos(['FeSLzHvlkbo','ypzxfNnCVio','gkkqmtbOwmE','CCRYhINqJ3A','C82XkHQNL4g','IGgMxhMxHao','vXAT5va1NXI','GnEXgEaYz1M','BpIY4ex2u6E','BAf4EYZ1AGk','mgPN8B-B7tg','_b_sGbjSVZQ'],B+'mosaicos/em-relevo-el-nino.jpg')
