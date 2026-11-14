"""Mosaico por vídeo: nossa thumb no 1º quadro (borda azul) + referências (borda vermelha), com canal e views. ≤ 1 MB."""
import csv, os, sys
from PIL import Image, ImageDraw, ImageFont
B = os.path.dirname(os.path.abspath(__file__)) + '/..'
OUT = os.path.abspath(B + '/../../mosaicos')
info = {x['id']: x for x in csv.DictReader(open(B + '/busca-enriquecida.csv'))}
bench = {x['id']: x for x in csv.DictReader(open(B + '/../../../benchmark-2026-11-14/dados/videos-90d.csv'))}
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
except: font = ImageFont.load_default()
W, H = 480, 270
for linha in open(B + '/thumbs/lista.txt'):
    p = linha.split(); nome, ids = p[0], p[1:]
    cols = 3; rows = (len(ids) + cols - 1) // cols
    m = Image.new('RGB', (cols * W, rows * (H + 30)), 'white'); d = ImageDraw.Draw(m)
    for k, vid in enumerate(ids):
        im = Image.open(f'{B}/thumbs/{vid}.jpg').convert('RGB')
        w, h = im.size; ch = int(w * 9 / 16); im = im.crop((0, (h - ch) // 2, w, (h - ch) // 2 + ch)).resize((W - 8, H - 8))
        x, y = (k % cols) * W, (k // cols) * (H + 30)
        d.rectangle([x, y, x + W - 1, y + H - 1], fill='#1f5fbf' if k == 0 else '#b3261e'); m.paste(im, (x + 4, y + 4))
        r = info.get(vid) or bench.get(vid) or {}
        lab = 'NOSSA (dossie-es)' if k == 0 else f"{(r.get('canal') or '?')[:22]} · {int(r.get('views', 0)):,} v".replace(',', '.')
        d.text((x + 6, y + H + 4), lab, fill='black', font=font)
    f = f'{OUT}/dossie-es-{nome}.jpg'; q = 85
    while True:
        m.save(f, quality=q)
        if os.path.getsize(f) < 1_000_000 or q < 40: break
        q -= 10
    print(f, os.path.getsize(f))
