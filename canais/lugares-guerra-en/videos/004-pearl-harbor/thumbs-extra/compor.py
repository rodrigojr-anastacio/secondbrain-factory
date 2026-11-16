#!/usr/bin/env python3
"""Thumbs extra D/E do 004-pearl-harbor (16/11/2026): base nano-banana (sem texto) + texto composto aqui (Anton, amarelo #FDD505, contorno tinta, selo RESTRICTED)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(AQUI, '..', 'thumbs', 'proj', 'public', 'fonts')
ANTON = os.path.join(FONTES, 'Anton-Regular.ttf'); MONO = os.path.join(FONTES, 'IBMPlexMono-Bold.ttf')
AMARELO, TINTA = (253, 213, 5), (17, 20, 24)
W, H = 1920, 1080

def base(nome, crop=None):
    im = Image.open(os.path.join(AQUI, 'bases', nome)).convert('RGB')
    if crop: im = im.crop(crop)
    return im.resize((W, H), Image.LANCZOS)

def escurece(im, caixa, alfa=150, raio=120):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rectangle(caixa, fill=alfa)
    m = m.filter(ImageFilter.GaussianBlur(raio))
    return Image.composite(Image.new('RGB', im.size, (0, 0, 0)), im, m)

def texto(im, linhas, x, y, tams, cor=AMARELO):
    d = ImageDraw.Draw(im)
    sombra = Image.new('L', im.size, 0); ds = ImageDraw.Draw(sombra)
    yy = y; pos = []
    for l, t in zip(linhas, tams):
        f = ImageFont.truetype(ANTON, t); pos.append((l, f, yy))
        ds.text((x, yy + 12), l, font=f, fill=150, stroke_width=t // 13, stroke_fill=150)
        yy += int(t * 1.0)
    sombra = sombra.filter(ImageFilter.GaussianBlur(10))
    im.paste(Image.new('RGB', im.size, (0, 0, 0)), (0, 0), sombra)
    for l, f, yy2 in pos:
        d.text((x, yy2), l, font=f, fill=cor, stroke_width=f.size // 13, stroke_fill=TINTA)
    return yy

def selo(im, x, y):
    f = ImageFont.truetype(MONO, 44); txt = 'RESTRICTED'
    bw = int(f.getlength(txt)) + 44; bh = 72
    s = Image.new('RGBA', (bw + 20, bh + 20), (0, 0, 0, 0)); ds = ImageDraw.Draw(s)
    ds.rectangle((10, 10, 10 + bw, 10 + bh), fill=(215, 38, 30, 240), outline=(170, 20, 15, 255), width=5)
    ds.text((32, 18), txt, font=f, fill=(255, 255, 255, 255))
    s = s.rotate(3, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', s.size, (0, 0, 0, 0)); sh.putalpha(s.split()[3].point(lambda a: a // 2))
    im.paste((0, 0, 0), (x, y + 8), sh.split()[3]); im.paste(s, (x, y), s)

def salvar(im, nome):
    out = os.path.join(AQUI, nome); im.resize((1280, 720), Image.LANCZOS).save(out, quality=90, optimize=True)
    print(out, os.path.getsize(out) // 1024, 'KB')

# D: panorama aéreo do porto (battleship row + explosão + bombardeiro mergulhando). D4 veio com moldura branca: recorte 16:9 dentro do conteúdo.
im = base('D4.jpg', crop=(252, 78, 252 + 1067, 78 + 600))
im = escurece(im, (0, 0, 820, 640), alfa=140)
y = texto(im, ['7:55', 'AM'], 60, 30, [330, 210])
selo(im, 66, y + 30)
salvar(im, 'thumb-D.jpg')

# E: ângulo baixo em Hickam: caça vindo na direção da câmera, rajada no quartel art déco, hangar explodindo.
im = base('E1.jpg')
im = escurece(im, (0, 0, 760, 520), alfa=120)
y = texto(im, ['NEVER', 'FIXED'], 54, 24, [230, 230])
selo(im, 60, y + 24)
salvar(im, 'thumb-E.jpg')
