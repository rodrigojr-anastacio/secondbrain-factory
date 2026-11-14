# B2: maquetes GRÁTIS (sem gerar imagem) das thumbs da rodada 2, a partir de bases/cenas que já existem.
# Só para conferir composição e leitura a 320x180; a base final é outra tomada (ver -v2.md).
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
V = '/home/hermes/workspace/fabrica-youtube/canais/historia-ptbr/videos'
FD = f'{V}/003-ira/v2-amostras/thumbs/base/fonts'
OUT = '/home/hermes/workspace/fabrica-youtube/pesquisa/reembalagem-2026-11-14/crivo/maquetes'
GOLD = (247, 194, 27); BLACK = (15, 12, 10); WHITE = (255, 255, 255)
def caslon(sz):
    f = ImageFont.truetype(f'{FD}/LibreCaslonText[wght].ttf', sz); f.set_variation_by_axes([700]); return f
def sans(sz):
    f = ImageFont.truetype(f'{FD}/OpenSans[wdth,wght].ttf', sz); f.set_variation_by_axes([800, 100]); return f
def fit(im):
    w = 1280; h = int(im.height * w / im.width); im = im.resize((w, h), Image.LANCZOS)
    if h < 720:
        h2 = 720; w2 = int(im.width * 720 / im.height); im = im.resize((w2, h2), Image.LANCZOS)
    x = (im.width - 1280) // 2; y = (im.height - 720) // 2; return im.crop((x, y, x + 1280, y + 720))
def grad(im, bottom=0, top=0, a=200):
    ov = Image.new('L', im.size, 0); d = ImageDraw.Draw(ov); W, H = im.size
    for i in range(bottom): d.line([(0, H-1-i), (W, H-1-i)], fill=int(a*(1-i/bottom)))
    for i in range(top): d.line([(0, i), (W, i)], fill=int(a*(1-i/top)))
    return Image.composite(Image.new('RGB', im.size, (0, 0, 0)), im, ov)
def text(im, xy, s, font, fill, stroke=10, anchor='la', shadow=10):
    d = ImageDraw.Draw(im)
    d.text((xy[0]+shadow, xy[1]+shadow), s, font=font, fill=BLACK, stroke_width=stroke, stroke_fill=BLACK, anchor=anchor)
    d.text(xy, s, font=font, fill=fill, stroke_width=stroke, stroke_fill=BLACK, anchor=anchor)
def pill(im, cx, cy, s, font):
    d = ImageDraw.Draw(im); b = d.textbbox((cx, cy), s, font=font, anchor='mm'); r = (b[0]-26, b[1]-14, b[2]+26, b[3]+14)
    d.rounded_rectangle((r[0]+7, r[1]+7, r[2]+7, r[3]+7), radius=16, fill=BLACK)
    d.rounded_rectangle(r, radius=16, fill=GOLD, outline=BLACK, width=6); d.text((cx, cy), s, font=font, fill=BLACK, anchor='mm')
def prancha(im, nome):
    im.save(f'{OUT}/{nome}.jpg', quality=88)
    small = im.resize((320, 180), Image.LANCZOS)
    P = Image.new('RGB', (1280 + 40 + 320, 720), (40, 40, 40)); P.paste(im, (0, 0)); P.paste(small, (1320, 270))
    ImageDraw.Draw(P).text((1320, 460), '320x180 (tamanho real no celular)', fill=WHITE)
    P.save(f'{OUT}/{nome}-prancha.jpg', quality=85)

# 003 Irã: base pronta c1-persia-ira-a (rei aquemênida x clérigo) + "MESMO PAÍS?" + pílula "2.500 ANOS"
im = fit(Image.open(f'{V}/003-ira/v2-amostras/thumbs/base/c1-persia-ira-a.png').convert('RGB')); im = grad(im, bottom=300, a=215)
d = ImageDraw.Draw(im); f = caslon(132); w1 = d.textlength('MESMO ', font=f); w2 = d.textlength('PAÍS?', font=f); x = (1280 - w1 - w2) / 2
text(im, (x, 692), 'MESMO', f, GOLD, anchor='ls'); text(im, (x + w1, 692), 'PAÍS?', f, WHITE, anchor='ls')
pill(im, 640, 62, '2.500 ANOS', sans(50)); prancha(im, 'historia-ptbr-003-ira-v2')

# 007 Rússia: mapa da cena I017 (Rússia em vermelho) escurecido fora da Rússia + borda dourada + "TUDO ISSO?", sem viking e sem pílula
m = Image.open(f'{V}/007-russia/imagens/I017.jpg').convert('RGB'); r, g, b = m.split()
mask = ImageChops.multiply(r.point(lambda v: 255 if v > 170 else 0), ImageChops.multiply(g.point(lambda v: 255 if v < 110 else 0), b.point(lambda v: 255 if v < 110 else 0)))
mask = mask.filter(ImageFilter.MedianFilter(5))
dark = Image.blend(m, Image.new('RGB', m.size, (12, 18, 38)), 0.78)
red = Image.blend(m, Image.new('RGB', m.size, (150, 12, 18)), 0.35)
comp = Image.composite(red, dark, mask)
edge = mask.filter(ImageFilter.MaxFilter(11)); edge = ImageChops.subtract(edge, mask).filter(ImageFilter.GaussianBlur(2))
comp = Image.composite(Image.new('RGB', m.size, GOLD), comp, edge)
glow = mask.filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.GaussianBlur(18)); glow = ImageChops.subtract(glow, mask).point(lambda v: int(v * 0.6))
comp = Image.composite(Image.new('RGB', m.size, (255, 170, 40)), comp, glow)
im = fit(comp); im = grad(im, bottom=0, top=0)
text(im, (40, 160), 'TUDO', caslon(150), GOLD, anchor='ls'); text(im, (40, 310), 'ISSO?', caslon(150), WHITE, anchor='ls')
prancha(im, 'historia-ptbr-007-russia-v2')

# 006 Roma: PROXY do senador (recorte do senador em desespero da base t1-bonecos-1, mãos na cabeça), close, Roma escura atrás + "DE NOVO?" + "410"
s = Image.open(f'{V}/006-roma/thumbs/base/t1-bonecos-1.jpg').convert('RGB'); W, H = s.size
crop = s.crop((int(W*0.37), int(H*0.20), int(W*0.60), int(H*0.62)))  # senador do peito para cima
bg = Image.open(f'{V}/006-roma/thumbs/base/t3-queda-1.jpg').convert('RGB'); bg = fit(bg).filter(ImageFilter.GaussianBlur(10))
bg = Image.blend(bg, Image.new('RGB', bg.size, (10, 8, 6)), 0.45)
ch = 680; cw = int(crop.width * ch / crop.height); crop = crop.resize((cw, ch), Image.LANCZOS)
cr, cg, cb = crop.split()
sky = ImageChops.subtract(cb, cr).point(lambda v: 255 if v > 25 else 0).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(3))
fade = Image.linear_gradient('L').rotate(90).resize(crop.size).point(lambda v: 0 if v > 60 else 255 - v * 4)  # funde a borda direita
alpha = ImageChops.subtract(Image.new('L', crop.size, 255), sky)
alpha = ImageChops.multiply(alpha, Image.linear_gradient('L').rotate(90).resize(crop.size).point(lambda v: 255 if v > 40 else v * 6))
im = bg.copy(); im.paste(crop, (40, 720 - ch), alpha)
im = grad(im, bottom=0)
text(im, (1240, 250), 'DE', caslon(170), GOLD, anchor='rs'); text(im, (1240, 440), 'NOVO?', caslon(170), WHITE, anchor='rs')
pill(im, 1080, 560, '410', sans(56))
prancha(im, 'historia-ptbr-006-roma-v2-proxy')
print('ok')
