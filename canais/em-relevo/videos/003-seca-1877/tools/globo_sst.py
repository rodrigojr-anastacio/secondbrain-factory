"""Textura equirretangular de globo a partir de dados/sst_1877_global.json (idx dez/1877) ou do OISST de 2026 (sst_comparativo, Pacífico 100-290E só).
Uso: python -I globo_sst.py <pasta_longo03> 1877|2026"""
import sys, os, json
import numpy as np
from PIL import Image, ImageDraw
ROOT, QUAL = sys.argv[1], sys.argv[2]
W, H = 2048, 1024
if QUAL == '1877':
    d = json.load(open(os.path.join(ROOT, 'dados/sst_1877_global.json'))); g = np.array(d['grades'][1], dtype=float)
    lon0, lat0 = d['lon0'], d['lat0']
else:
    d = json.load(open(os.path.join(ROOT, 'dados/sst_comparativo_global.json'))); g = np.array(d['grades'][-1], dtype=float)
    lon0, lat0 = d['lon0'], d['lat0']
g = np.where(g == None, np.nan, g).astype(float)
ny, nx = g.shape
full = np.full((181, 361), np.nan)
for j in range(ny):
    for i in range(nx):
        la = int(round(lat0 + j * d['passo'])); lo = int(round(lon0 + i * d['passo']))
        if -90 <= la <= 90 and -180 <= lo <= 180: full[la + 90, lo + 180] = g[j, i]
a = full[::-1]
def hexrgb(h): return np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], dtype=np.float32)
SEA, CORAL, WINE, BLUE = map(hexrgb, ['#C9D6D8', '#E8505B', '#8E1F2F', '#3D6A9E'])
stops = [(-3.0, BLUE), (-0.5, SEA), (0.5, SEA), (2.0, CORAL), (4.0, WINE)]
vv = np.nan_to_num(a, nan=0.0); out = np.empty(a.shape + (3,), np.float32)
for c in range(3): out[..., c] = np.interp(vv, [s[0] for s in stops], [s[1][c] for s in stops])
img = Image.fromarray(out.clip(0, 255).astype(np.uint8), 'RGB').resize((W, H), Image.BILINEAR)
S = 2
mask = Image.new('L', (W*S, H*S), 0); lines = Image.new('L', (W*S, H*S), 0)
dm, dl = ImageDraw.Draw(mask), ImageDraw.Draw(lines)
geo = json.load(open(os.path.join(ROOT, 'dados/ne110.json')))
px = lambda ring: [((x+180)/360*W*S, (90-y)/180*H*S) for x, y in ring]
for ft in geo['features']:
    gg = ft['geometry']; polys = [gg['coordinates']] if gg['type'] == 'Polygon' else gg['coordinates']
    for p in polys:
        dm.polygon(px(p[0]), fill=255)
        for hole in p[1:]: dm.polygon(px(hole), fill=0)
        for ring in p: dl.line(px(ring) + px(ring[:1]), fill=255, width=S)
mask = mask.resize((W, H), Image.LANCZOS); lines = lines.resize((W, H), Image.LANCZOS)
img = Image.composite(Image.new('RGB', (W, H), '#DCCDB0'), img, mask)
img = Image.composite(Image.new('RGB', (W, H), '#9C8662'), img, lines)
o = os.path.join(ROOT, f'remotion/public/sat/globo-{QUAL}.jpg'); img.save(o, quality=90); print(o)
