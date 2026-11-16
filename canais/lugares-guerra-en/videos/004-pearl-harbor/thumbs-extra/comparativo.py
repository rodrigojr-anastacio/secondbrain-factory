#!/usr/bin/env python3
"""Prancha comparativa: thumbs atuais A/B/C (entrega/) + extras D/E (thumbs-extra/), cada uma a 320×180. Uso: comparativo.py <pasta_video>"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
v = os.path.abspath(sys.argv[1]); te = os.path.join(v, 'thumbs-extra')
MONO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', 'pesquisa', 'canal-clima-2026-11', 'identidade', 'fontes', 'IBMPlexMono-Bold.ttf')
f = ImageFont.truetype(MONO, 18)
itens = [(os.path.join(v, 'entrega', f'thumb-{x}.jpg'), f'{x} (atual)') for x in 'ABC'] + [(os.path.join(te, f'thumb-{x}.jpg'), f'{x} (nova)') for x in 'DE']
G, TW, TH, LH = 16, 320, 180, 28
cols = 3; rows = 2
m = Image.new('RGB', (cols * TW + (cols + 1) * G, rows * (TH + LH) + (rows + 1) * G), (245, 245, 245)); d = ImageDraw.Draw(m)
for i, (p, rot) in enumerate(itens):
    c, r = (i % cols, i // cols) if i < 3 else (i - 3, 1)
    x = G + c * (TW + G) + (0 if i < 3 else (TW + G) // 2); y = G + r * (TH + LH + G)
    m.paste(Image.open(p).convert('RGB').resize((TW, TH), Image.LANCZOS), (x, y + LH))
    d.text((x, y + 4), rot, font=f, fill=(20, 20, 20) if i < 3 else (200, 40, 40))
m.save(os.path.join(te, 'comparativo.jpg'), quality=90); print(os.path.join(te, 'comparativo.jpg'))
