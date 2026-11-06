import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
V='/home/hermes/workspace/fabrica-youtube/canais/historia-ptbr/videos/003-ira/v2-amostras/thumbs'
FD=os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts')
GOLD=(247,194,27); BLACK=(15,12,10); WHITE=(255,255,255)
def caslon(sz):
    f=ImageFont.truetype(f'{FD}/LibreCaslonText[wght].ttf',sz); f.set_variation_by_axes([700]); return f
def sans(sz):
    f=ImageFont.truetype(f'{FD}/OpenSans[wdth,wght].ttf',sz); f.set_variation_by_axes([800,100]); return f
def base(name, shift=0, zoom=1.0, flip=False):
    im=Image.open(f'{V}/base/{name}.png').convert('RGB')
    if flip: im=im.transpose(Image.FLIP_LEFT_RIGHT)
    w=int(1280*zoom); h=int(im.height*w/im.width); im=im.resize((w,h),Image.LANCZOS)
    x=(w-1280)//2; y=max(0,min(h-720,(h-720)//2+shift)); return im.crop((x,y,x+1280,y+720))
def grad(im, top=None, bottom=None, left=None, right=None, a=200):
    ov=Image.new('L',im.size,0); d=ImageDraw.Draw(ov); W,H=im.size
    if bottom:
        for i in range(bottom): d.line([(0,H-1-i),(W,H-1-i)],fill=int(a*(1-i/bottom)))
    if top:
        for i in range(top): d.line([(0,i),(W,i)],fill=int(a*(1-i/top)))
    if left:
        for i in range(left): d.line([(i,0),(i,H)],fill=int(a*(1-i/left)))
    return Image.composite(Image.new('RGB',im.size,(0,0,0)),im,ov)
def text(im, xy, s, font, fill, stroke=10, sfill=BLACK, shadow=10, anchor='la'):
    d=ImageDraw.Draw(im)
    if shadow:
        d.text((xy[0]+shadow,xy[1]+shadow),s,font=font,fill=BLACK,stroke_width=stroke,stroke_fill=BLACK,anchor=anchor)
    d.text(xy,s,font=font,fill=fill,stroke_width=stroke,stroke_fill=sfill,anchor=anchor)
    return d.textbbox(xy,s,font=font,stroke_width=stroke,anchor=anchor)
def pill(im, cx, cy, s, font, fg=BLACK, bg=GOLD, padx=26, pady=14, anchor='mm'):
    d=ImageDraw.Draw(im); b=d.textbbox((cx,cy),s,font=font,anchor=anchor)
    r=(b[0]-padx,b[1]-pady,b[2]+padx,b[3]+pady)
    d.rounded_rectangle((r[0]+7,r[1]+7,r[2]+7,r[3]+7),radius=16,fill=BLACK)
    d.rounded_rectangle(r,radius=16,fill=bg,outline=BLACK,width=6)
    d.text((cx,cy),s,font=font,fill=fg,anchor=anchor); return r
def arrow(im, p0, p1, w=34, color=GOLD):
    import math
    d=ImageDraw.Draw(im); ang=math.atan2(p1[1]-p0[1],p1[0]-p0[0]); L=w*2.2
    tip=p1; bx=(p1[0]-L*math.cos(ang),p1[1]-L*math.sin(ang))
    l=(bx[0]+w*1.3*math.sin(ang),bx[1]-w*1.3*math.cos(ang)); r=(bx[0]-w*1.3*math.sin(ang),bx[1]+w*1.3*math.cos(ang))
    for col,ww,off in ((BLACK,w+16,8),(BLACK,w+16,0),(color,w,0)):
        o=off; d.line([(p0[0]+o,p0[1]+o),(bx[0]+o,bx[1]+o)],fill=col,width=ww)
        k=8 if col==BLACK else 0
        tri=[(tip[0]+o+k*math.cos(ang),tip[1]+o+k*math.sin(ang)),(l[0]+o,l[1]+o),(r[0]+o,r[1]+o)]
        if col==BLACK: d.polygon(tri,fill=BLACK,outline=BLACK,width=10)
        else: d.polygon(tri,fill=color)

def t1():
    im=base('c1-persia-ira-a'); im=grad(im,bottom=300,a=210)
    f=caslon(138)
    text(im,(290,700),'PÉRSIA',f,GOLD,stroke=10,anchor='ms')
    text(im,(1020,700),'IRÃ',f,WHITE,stroke=10,anchor='ms')
    arrow(im,(612,650),(782,650),w=30)
    return im
def t2():
    im=base('c2-caixao-b'); im=grad(im,top=330,a=190)
    f=caslon(132)
    text(im,(36,26),'SALVOU',f,WHITE,stroke=10,anchor='lt')
    text(im,(36,176),'O IRÃ?',f,GOLD,stroke=10,anchor='lt')
    arrow(im,(250,345),(250,470),w=30)
    return im
def t3():
    im=base('c3-turbante-coroa-a'); im=grad(im,bottom=280,a=225)
    d=ImageDraw.Draw(im); fx=sans(90)
    for sz in range(120,80,-2):
        f=caslon(sz); w1=d.textlength('COROA',font=f); w2=d.textlength('TURBANTE',font=f); wx=d.textlength('×',font=fx)
        tot=w1+w2+wx+2*30
        if tot<=1200: break
    x=(1280-tot)/2
    text(im,(x,694),'COROA',f,GOLD,stroke=9,anchor='ls'); x+=w1+30
    text(im,(x,682),'×',fx,WHITE,stroke=7,anchor='ls'); x+=wx+30
    text(im,(x,694),'TURBANTE',f,WHITE,stroke=9,anchor='ls'); print('t3 size',sz)
    pill(im,640,62,'1891 · 1979',sans(50))
    return im
def t4():
    im=base('c4-viraram-persas-b',zoom=1.10,shift=40)
    f=caslon(138)
    d=ImageDraw.Draw(im)
    text(im,(640,150),'VIRARAM',f,BLACK,stroke=8,sfill=WHITE,shadow=0,anchor='ms')
    b=d.textbbox((640,300),'PERSAS',font=f,anchor='ms')
    d.rectangle((b[0]-28+8,b[1]-8+8,b[2]+28+8,b[3]+22+8),fill=BLACK)
    d.rectangle((b[0]-28,b[1]-8,b[2]+28,b[3]+22),fill=GOLD,outline=BLACK,width=6)
    text(im,(640,300),'PERSAS',f,BLACK,stroke=0,shadow=0,anchor='ms')
    return im
os.makedirs(V,exist_ok=True)
outs=[]
for i,fn in enumerate([t1,t2,t3,t4],1):
    im=fn(); p=f'{V}/thumb-{i}.jpg'; im.save(p,quality=90,optimize=True); outs.append(im); print(p,os.path.getsize(p)//1024,'KB',im.size)
grid=Image.new('RGB',(1280+12,720+12),'white')
for i,im in enumerate(outs): grid.paste(im.resize((640,360),Image.LANCZOS),((i%2)*652,(i//2)*372))
grid.save(f'{V}/prancha-4-thumbs.jpg',quality=88)
cel=Image.new('RGB',(4*320+5*12,180+24),(15,15,15))
for i,im in enumerate(outs): cel.paste(im.resize((320,180),Image.LANCZOS),(12+i*332,12))
cel.save(f'{V}/prancha-4-thumbs-celular.jpg',quality=90)
