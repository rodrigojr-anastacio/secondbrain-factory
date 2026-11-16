#!/usr/bin/env python3
"""Thumbs extra D/E do 005 (16/11/2026), compostas em PIL (alternativa sem Remotion da biblia/thumb.md), US$ 0.
D = cena-acao (foto aérea real do Mercado Público ilhado, 05/05/2024) · E = antes-depois (Sentinel-2/HLS 21/04 × 06/05/2024)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
AQUI = os.path.dirname(os.path.abspath(__file__))
FAB = os.path.abspath(os.path.join(AQUI, '..', '..', '..', '..', '..'))
FONTES = os.path.join(FAB, 'pesquisa', 'canal-clima-2026-11', 'identidade', 'fontes')
ANTON = os.path.join(FONTES, 'Anton-Regular.ttf'); MONO = os.path.join(FONTES, 'IBMPlexMono-Bold.ttf')
FOTOS = os.path.join(AQUI, '..', 'dl', 'fotos')
AMARELO, BRANCO, CONTORNO, NAVY, CORAL = (255, 210, 63), (251, 248, 241), (14, 20, 38), (31, 42, 68), (232, 80, 91)
W, H = 1920, 1080

def escurece(im, caixa, alfa=150, raio=110):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rectangle(caixa, fill=alfa)
    return Image.composite(Image.new('RGB', im.size, (8, 12, 28)), im, m.filter(ImageFilter.GaussianBlur(raio)))

def linha(im, txt, x, y, tam, cor, centro=False):
    f = ImageFont.truetype(ANTON, tam); sw = 14
    if centro: x = x - int(f.getlength(txt)) // 2
    sh = Image.new('L', im.size, 0); ImageDraw.Draw(sh).text((x, y + 12), txt, font=f, fill=160, stroke_width=sw, stroke_fill=160)
    im.paste(Image.new('RGB', im.size, (0, 0, 0)), (0, 0), sh.filter(ImageFilter.GaussianBlur(12)))
    ImageDraw.Draw(im).text((x, y), txt, font=f, fill=cor, stroke_width=sw, stroke_fill=CONTORNO)

def etiqueta(im, txt, x, y, fundo, cor=BRANCO, tam=64, centro=False):
    f = ImageFont.truetype(MONO, tam); w = int(f.getlength(txt)) + 48; h = int(tam * 1.45)
    if centro: x -= w // 2
    d = ImageDraw.Draw(im); d.rectangle((x + 6, y + 8, x + w + 6, y + h + 8), fill=(0, 0, 0)); d.rectangle((x, y, x + w, y + h), fill=fundo)
    d.text((x + 24, y + int(tam * 0.12)), txt, font=f, fill=cor)

def salvar(im, nome):
    out = os.path.join(AQUI, nome); im.resize((1280, 720), Image.LANCZOS).save(out, quality=90, optimize=True)
    print(out, os.path.getsize(out) // 1024, 'KB')

# D: foto aérea real em tela cheia (Mercado Público ilhado, água marrom). Texto curto no topo esquerdo.
im = Image.open(os.path.join(FOTOS, 'video', 'mercado-publico-ilhado-aereo-2024-05-05.jpg')).convert('RGB')
im = im.crop((0, 170, 1920, 1250)).resize((W, H), Image.LANCZOS)
im = ImageEnhance.Color(im).enhance(1.15); im = ImageEnhance.Contrast(im).enhance(1.08)
im = escurece(im, (0, 0, 1250, 560), alfa=175)
linha(im, 'VEIO DE', 56, 20, 290, AMARELO)
linha(im, 'LONGE', 56, 300, 290, BRANCO)
salvar(im, 'thumb-D.jpg')

# E: antes × depois do mesmo recorte de satélite (delta do Jacuí + Guaíba + Porto Alegre), Sentinel-2/HLS.
cx = (230, 0, 230 + 820, 922)   # 820×922 ≈ 960×1080 (sem a faixa preta da passagem)
paineis = []
for arq in ('hls-sentinel2-porto-alegre-guaiba-antes-2024-04-21.jpg', 'hls-sentinel2-porto-alegre-alagada-2024-05-06.jpg'):
    p = Image.open(os.path.join(FOTOS, 'satelite', arq)).convert('RGB').crop(cx).resize((960, 1080), Image.LANCZOS)
    p = ImageEnhance.Brightness(p).enhance(1.18); p = ImageEnhance.Color(p).enhance(1.25); p = ImageEnhance.Contrast(p).enhance(1.12)
    paineis.append(p)
im = Image.new('RGB', (W, H)); im.paste(paineis[0], (0, 0)); im.paste(paineis[1], (960, 0))
d = ImageDraw.Draw(im); d.rectangle((951, 0, 969, H), fill=BRANCO)
im = escurece(im, (300, 0, 1620, 300), alfa=150, raio=90)
linha(im, 'SÓ 15 DIAS?', 960, 6, 250, AMARELO, centro=True)
etiqueta(im, '21 ABR', 40, 930, NAVY)
etiqueta(im, '6 MAI', 1000, 930, CORAL)
salvar(im, 'thumb-E.jpg')
