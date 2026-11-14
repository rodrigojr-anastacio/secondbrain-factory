"""Mosaico por vídeo: nossa thumb atual (amarelo) + referências do tema (azul = acima da mediana do canal, cinza = não).
Uso: A-mosaico.py <tema> <nosso_id> <saida.jpg> <id1> <id2> ..."""
import csv, os, sys
from PIL import Image, ImageDraw, ImageFont
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tema, nosso, saida, ids = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
R = {r['id']: r for r in csv.DictReader(open(os.path.join(BASE, 'A-refs.csv')))}
F = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
font = ImageFont.truetype(F, 17) if os.path.exists(F) else ImageFont.load_default()
W, H, LH, COLS = 480, 270, 46, 3
tiles = [(nosso, None)] + [(i, R.get(i)) for i in ids]
rows = (len(tiles) + COLS - 1) // COLS
img = Image.new('RGB', (COLS * W, rows * (H + LH)), (18, 18, 18)); d = ImageDraw.Draw(img)
def fmt(n):
    n = int(n); return f'{n/1e6:.1f} mi'.replace('.', ',') if n >= 1e6 else f'{n/1e3:.0f} mil' if n >= 1e3 else str(n)
for k, (i, r) in enumerate(tiles):
    x, y = (k % COLS) * W, (k // COLS) * (H + LH)
    p = os.path.join(BASE, 'A-thumbs', f'{i}.jpg')
    t = Image.open(p).convert('RGB'); tw, th = t.size; c = (th - tw * 9 // 16) // 2
    t = t.crop((0, c, tw, th - c)).resize((W - 6, H - 6)); img.paste(t, (x + 3, y + LH + 3))
    if r is None:
        lab1, lab2, cor = 'NÓS (thumb no ar)', '', (247, 194, 27)
    else:
        cor = (110, 190, 255) if r['acima_mediana'] == 'sim' else (150, 150, 150)
        lab1 = f"{r['canal'][:22]} · {fmt(r['views'])} · {r['data'][2:]}"
        lab2 = (r['titulo'][:46] + ('…' if len(r['titulo']) > 46 else ''))
    d.text((x + 6, y + 3), lab1, fill=cor, font=font); d.text((x + 6, y + 23), lab2, fill=(220, 220, 220), font=font)
img.save(saida, quality=78, optimize=True)
q = 78
while os.path.getsize(saida) > 1_000_000 and q > 40:
    q -= 8; img.save(saida, quality=q, optimize=True)
print(saida, os.path.getsize(saida))
