#!/usr/bin/env python3
"""Maquetes de COMPOSIÇÃO (custo zero): recortes de quadros já gerados do próprio vídeo + texto no código.
Não são as thumbs finais (a arte nova só depois da aprovação do Rodrigo)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
V=os.path.abspath(os.path.dirname(__file__)+'/../..'); O=V+'/reembalagem-2026-11-19/maquetes'
F='/home/hermes/workspace/fabrica-youtube/canais/dossie-es/identidade/fontes/'
BEB=lambda s: ImageFont.truetype(F+'BebasNeue-Regular.ttf',s); SE=lambda s: ImageFont.truetype(F+'SpecialElite-Regular.ttf',s)
ARD=(46,58,70); PAP=(233,223,201); RED=(179,38,30); INK=(26,26,26)
W,H=1280,720
def img(i): return Image.open(f'{V}/imagens/{i}.jpg').convert('RGB')
def aba(c,txt='EXPEDIENTE Nº 010'):
    d=ImageDraw.Draw(c); f=SE(26); tw=d.textlength(txt,font=f)
    d.rounded_rectangle([W-tw-60,-12,W-14,52],10,fill=(164,128,82)); d.text((W-tw-37,10),txt,font=f,fill=INK)
def sello(c,txt,xy,size=120,ang=-6):
    f=BEB(size); d0=ImageDraw.Draw(c); tw=d0.textlength(txt,font=f); pad=26
    s=Image.new('RGBA',(int(tw+2*pad),int(size*1.05+pad)),(0,0,0,0)); d=ImageDraw.Draw(s)
    d.rectangle([0,0,s.width-1,s.height-1],fill=RED+(255,)); d.rectangle([7,7,s.width-8,s.height-8],outline=PAP+(255,),width=4)
    d.text((pad,pad*0.55),txt,font=f,fill=PAP); s=s.rotate(ang,expand=True,resample=Image.BICUBIC); c.paste(s,xy,s)
# A: Escobar (rosto real, traço do canal) + avião noturno ao fundo + SOLO IDA
a=Image.new('RGB',(W,H),ARD)
bg=img('I079').resize((W,H)); bg=ImageEnhance.Brightness(bg).enhance(0.8); a.paste(bg,(0,0))
esc=img('I065'); ew,eh=esc.size
face=esc.crop((int(ew*0.32),int(eh*0.05),int(ew*0.68),int(eh*0.95))).resize((600,H))
a.paste(face.crop((0,0,600,H)),(0,0))
g=Image.new('L',(160,H)); [ImageDraw.Draw(g).line([(x,0),(x,H)],fill=int(255*(1-x/160))) for x in range(160)]
a.paste(face.crop((440,0,600,H)),(440,0),g)
sello(a,'SOLO IDA',(700,420),130,-5); aba(a); a.save(O+'/A-maquete.jpg',quality=88)
# B: helicóptero sobre a casa (recorte ampliado) + ¿RESCATE?
b=img('I003'); bw,bh=b.size
b=b.crop((int(bw*0.18),int(bh*0.0),int(bw*0.86),int(bh*0.68))).resize((W,H))
sello(b,'¿RESCATE?',(720,470),110,-6); aba(b); b.save(O+'/B-maquete.jpg',quality=88)
# C: a palavra escondida, datilografada e riscada em vermelho, papel sobre mesa escura
c=Image.new('RGB',(W,H),(30,34,40))
p=Image.new('RGB',(1060,560),PAP); dp=ImageDraw.Draw(p)
for y in range(70,540,46):
    if 200<y<380: continue
    dp.line([(70,y),(990-((y*37)%180),y)],fill=(170,160,140),width=7)
f=SE(150); txt='EXTRADICIÓN'; tw=dp.textlength(txt,font=f); dp.text(((1060-tw)/2,205),txt,font=f,fill=INK)
dp.line([(40,330),(1020,262)],fill=RED,width=26)
p=p.rotate(3,expand=True,resample=Image.BICUBIC,fillcolor=(30,34,40)); c.paste(p,((W-p.width)//2,(H-p.height)//2+30))
aba(c); c.save(O+'/C-maquete.jpg',quality=88)
print('ok')
# ---- rodada 2 ----
# A2: ficha policial de Escobar presa ao expediente, carimbo DESTINO: EE.UU.
a=Image.new('RGB',(W,H),(32,40,50)); d=ImageDraw.Draw(a)
d.rectangle([60,70,820,760],fill=(164,128,82))               # pasta parda
card=Image.new('RGB',(560,640),PAP); dc=ImageDraw.Draw(card)
esc=img('I065'); ew,eh=esc.size
f2=esc.crop((int(ew*0.36),int(eh*0.06),int(ew*0.64),int(eh*0.62))).resize((500,500))
f2=ImageEnhance.Brightness(f2).enhance(0.85); card.paste(f2,(30,30))
dc.line([(30,560),(530,560)],fill=(150,140,120),width=6); dc.line([(30,600),(380,600)],fill=(150,140,120),width=6)
card=card.rotate(-3,expand=True,resample=Image.BICUBIC,fillcolor=(164,128,82)); a.paste(card,(150,40))
d=ImageDraw.Draw(a); d.rectangle([330,30,370,110],fill=(120,120,125))  # clipe
sello(a,'DESTINO: EE.UU.',(560,470),100,-8); aba(a); a.save(O+'/A2-maquete.jpg',quality=88)
# B2: helicóptero >= 40% da área sobre a casa, céu claro atrás
b=img('I003'); bw,bh=b.size
b=b.crop((int(bw*0.33),int(bh*0.08),int(bw*0.78),int(bh*0.58))).resize((W,H))
b=ImageEnhance.Contrast(b).enhance(1.25)
sello(b,'¿RESCATE?',(800,500),100,-6); aba(b); b.save(O+'/B2-maquete.jpg',quality=88)
# ---- rodada 3 ----
# A3: rosto de Escobar dominante (>=45% da altura) em tinta azul-ardósia (duotone), meia sombra,
#     e a SOMBRA VERMELHA de um jato cruzando o rosto (o voo que ele temia). Sem texto, sem documento.
from PIL import ImageOps
a=Image.new('RGB',(W,H),ARD)
esc=img('I065'); ew,eh=esc.size
f3=esc.crop((int(ew*0.39),int(eh*0.10),int(ew*0.61),int(eh*0.50))).resize((720,720))
f3=ImageOps.colorize(ImageOps.grayscale(f3),black=(16,22,30),white=PAP)
sh=Image.new('L',(720,720),0); ds=ImageDraw.Draw(sh)
for x in range(720): ds.line([(x,0),(x,720)],fill=int(max(0,min(170,(x-380)*0.9))))   # meia sombra à direita
f3=Image.composite(Image.new('RGB',(720,720),(16,22,30)),f3,sh)
a.paste(f3,(70,0))
jet=Image.new('RGBA',(W,H),(0,0,0,0)); dj=ImageDraw.Draw(jet)
cx,cy,s=760,250,1.0
body=[(-330,0),(-300,-18),(260,-22),(330,0),(260,22),(-300,18)]
wing=[(-40,-10),(60,-10),(-60,-230),(-120,-230)]; wing2=[(-40,10),(60,10),(-60,230),(-120,230)]
tail=[(-300,-12),(-250,-12),(-300,-95),(-330,-95)]; tail2=[(-300,12),(-250,12),(-300,95),(-330,95)]
import math
def tr(p,ang=-14):
    a_=math.radians(ang); return [(cx+x*math.cos(a_)-y*math.sin(a_), cy+x*math.sin(a_)+y*math.cos(a_)) for x,y in p]
for poly in (body,wing,wing2,tail,tail2): dj.polygon(tr(poly),fill=RED+(215,))
a.paste(jet,(0,0),jet); aba(a); a.save(O+'/A3-maquete.jpg',quality=88)
