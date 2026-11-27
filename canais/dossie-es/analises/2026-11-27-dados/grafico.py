"""Gera ../2026-11-27-retencao.png a partir de dados.json (rodar de analises/)."""
import json
from PIL import Image, ImageDraw, ImageFont
D=json.load(open('2026-11-27-dados/dados.json'));V=D['videos']
FP='/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
F=ImageFont.truetype(FP,17); FS=ImageFont.truetype(FP,14)
W,H,L,T,R,B=1100,620,70,60,170,60
im=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(im)
X=lambda p:L+(W-L-R)*p; Y=lambda y:T+(H-T-B)*(1-(y-0.2)/0.85)
for y in [0.2,0.4,0.6,0.8,1.0]:
    d.line([X(0),Y(y),X(1),Y(y)],fill='#ddd'); d.text((20,Y(y)-8),f"{int(y*100)}%",fill='#444',font=FS)
for p in [0,.25,.5,.75,1]: d.text((X(p)-10,H-B+8),f"{int(p*100)}%",fill='#444',font=FS)
d.text((L,15),"Dossier: retenção desde a publicação (Analytics API, dados até 24/11). Yakuza fora: o arquivo no ar é o do GRU.",fill='#000',font=F)
d.text((X(.42),H-25),"% do vídeo",fill='#444',font=FS)
sel=[('gmA0LkJqf_U','Cosa Nostra','#1A1A1A',4),('I_ehrH5Yrak','KGB','#2E3A46',2),('KxSpEtRs_h0','SS','#8a9aa9',2),('XYhZGpBGjQ0','Medellín','#c9a227',2),('lypeCOdLxjA','MI6','#4a7c59',2),('lznXz53WRo8','Núremberg','#B3261E',4)]
for k,(v,n,c,w) in enumerate(sel):
    r=V[v]['an']['retencao']['rows']
    d.line([(X(x[0]),Y(x[1])) for x in r],fill=c,width=w)
    d.line([W-R+15,T+20+k*26,W-R+45,T+20+k*26],fill=c,width=w); d.text((W-R+52,T+12+k*26),n,fill='#000',font=FS)
im.save('2026-11-27-retencao.png')
