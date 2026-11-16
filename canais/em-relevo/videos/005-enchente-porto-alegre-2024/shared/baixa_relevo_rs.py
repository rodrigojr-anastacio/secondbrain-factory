# Em Relevo 005 (15/11/2026): terreno regional do RS. Baixa tiles Terrarium (AWS Open Data "Terrain Tiles", SRTM/GMTED, z=10, ~130 m)
# e cor Blue Marble Next Generation (NASA GIBS WMS) para a caixa do RS e grava work/v2/br_det_etopo.npy (metros, grade equiretangular) e br_det_bm.jpg.
# Caixa: lon -58..-48, lat -34.5..-26.5 (REGIOES.br_det do 005). Uso: python3 baixa_relevo_rs.py
import math, io, sys, urllib.request, numpy as np
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
OUT = Path(__file__).resolve().parent.parent / "work/v2"; OUT.mkdir(parents=True, exist_ok=True)
LON0, LON1, LAT0, LAT1 = -58.0, -48.0, -34.5, -26.5
Z = 10; N = 2 ** Z
def tx(lon): return (lon + 180) / 360 * N
def ty(lat): return (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * N
x0, x1, y0, y1 = int(tx(LON0)), int(tx(LON1)), int(ty(LAT1)), int(ty(LAT0))
tiles = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]
print(len(tiles), "tiles", flush=True)
def get(xy):
    x, y = xy
    for _ in range(4):
        try:
            d = urllib.request.urlopen(urllib.request.Request(f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{Z}/{x}/{y}.png", headers={"User-Agent": "emrelevo/1.0"}), timeout=60).read()
            a = np.asarray(Image.open(io.BytesIO(d)).convert("RGB"), np.float32)
            return xy, a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
        except Exception as e: err = e
    raise SystemExit(f"falhou {xy} {err}")
mos = np.zeros(((y1 - y0 + 1) * 256, (x1 - x0 + 1) * 256), np.float32)
with ThreadPoolExecutor(8) as ex:
    for (x, y), z in ex.map(get, tiles): mos[(y - y0) * 256:(y - y0 + 1) * 256, (x - x0) * 256:(x - x0 + 1) * 256] = z
print("mosaico", mos.shape, flush=True)
NX, NY = 4096, 3277
lons = np.linspace(LON0, LON1, NX); lats = np.linspace(LAT1, LAT0, NY)
px = (tx(lons) - x0) * 256 - 0.5
py = np.array([(ty(l) - y0) * 256 - 0.5 for l in lats])
ix, iy = np.clip(np.floor(px).astype(int), 0, mos.shape[1] - 2), np.clip(np.floor(py).astype(int), 0, mos.shape[0] - 2)
fx, fy = (px - ix)[None, :], (py - iy)[:, None]
a = mos[np.ix_(iy, ix)]; b = mos[np.ix_(iy, ix + 1)]; c = mos[np.ix_(iy + 1, ix)]; d = mos[np.ix_(iy + 1, ix + 1)]
z = (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy
print("alt min/max", float(z.min()), float(z.max()), flush=True)
np.save(OUT / "br_det_etopo.npy", z.astype(np.float32))
W = 4096; H = round(W * (LAT1 - LAT0) / (LON1 - LON0))
url = f"https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?SERVICE=WMS&REQUEST=GetMap&VERSION=1.1.1&LAYERS=BlueMarble_NextGeneration&STYLES=&FORMAT=image/jpeg&SRS=EPSG:4326&BBOX={LON0},{LAT0},{LON1},{LAT1}&WIDTH={W}&HEIGHT={H}"
im = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "emrelevo/1.0"}), timeout=180).read())).convert("RGB")
print("bm", im.size); im.save(OUT / "br_det_bm.jpg", quality=92)
