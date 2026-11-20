#!/usr/bin/env python3
"""Baixa thumbs (via WARP) e monta mosaico.jpg (320×180 por célula, legenda com views e ×med) e mosaico-320.jpg (160×90)."""
import csv, json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDS = sys.argv[1].split(',')
rows = {r['id']: r for r in csv.DictReader(open(f'{OUT}/corpus.csv'))}
os.makedirs(f'{OUT}/thumbs', exist_ok=True)
for i in IDS:
    f = f'{OUT}/thumbs/{i}.jpg'
    if not os.path.exists(f) or os.path.getsize(f) < 2000:
        subprocess.run(['curl', '-s', '-m', '30', '--proxy', 'socks5h://127.0.0.1:40000', '-o', f, f'https://i.ytimg.com/vi/{i}/hqdefault.jpg'])
def grade(w, h, nome, leg=True):
    cols = 6; lin = (len(IDS) + cols - 1) // cols; lh = 34 if leg else 0
    M = Image.new('RGB', (cols * w, lin * (h + lh)), 'white'); d = ImageDraw.Draw(M)
    try: fn = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    except Exception: fn = ImageFont.load_default()
    for k, i in enumerate(IDS):
        x, y = (k % cols) * w, (k // cols) * (h + lh)
        try:
            im = Image.open(f'{OUT}/thumbs/{i}.jpg').convert('RGB')
            W, H = im.size; c = (H - W * 9 // 16) // 2
            im = im.crop((0, c, W, c + W * 9 // 16)).resize((w, h))
            M.paste(im, (x, y))
        except Exception:
            pass
        if leg:
            r = rows.get(i, {})
            xm = r.get('x_mediana') or '?'
            d.text((x + 3, y + h + 2), f"{int(r.get('views') or 0):,} | {xm}x | {i}", fill='black', font=fn)
            d.text((x + 3, y + h + 17), (r.get('titulo') or '')[:46], fill='black', font=fn)
    M.save(f'{OUT}/{nome}', quality=82)
grade(320, 180, 'mosaico.jpg')
grade(160, 90, 'embalagem/mosaico-320.jpg', leg=False)
print(os.path.getsize(f'{OUT}/mosaico.jpg'))
