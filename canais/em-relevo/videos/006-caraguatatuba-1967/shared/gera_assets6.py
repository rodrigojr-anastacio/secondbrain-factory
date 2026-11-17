# Em Relevo 006 (17/11/2026): relevo do litoral norte de SP -> texturas A (satélite sintético por altura+sombra) e B (editorial navy),
# máscaras de declividade e blocos 3D cortados (dados/blocos3d.json). Fonte: AWS Terrain Tiles (Terrarium, SRTM/GMTED/GEBCO), z12.
# Saída em remotion/public/v6/ e dados/. Uso: tools/.venv/bin/python shared/gera_assets6.py
import math, io, json, os, urllib.request, numpy as np
from pathlib import Path
from PIL import Image, ImageFilter
Image.MAX_IMAGE_PIXELS = None
R = Path(__file__).resolve().parent.parent; PUB = R / "remotion/public/v6"; PUB.mkdir(parents=True, exist_ok=True)
CACHE = Path(os.environ.get("TMPDIR", str(Path.home() / "cache/tmp"))) / "relevo006"; CACHE.mkdir(parents=True, exist_ok=True)
LON0, LON1, LAT0, LAT1 = -46.30, -44.85, -24.00, -23.28   # oeste, leste, sul, norte
LATC = (LAT0 + LAT1) / 2; K = 2900.0                          # px por grau de latitude
W = int(round((LON1 - LON0) * K * math.cos(math.radians(LATC)))); H = int(round((LAT1 - LAT0) * K))
Z = 12; N = 2 ** Z
def tx(lon): return (lon + 180) / 360 * N
def ty(lat): return (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * N
def tile(x, y):
    f = CACHE / f"{Z}_{x}_{y}.png"
    if not f.exists(): f.write_bytes(urllib.request.urlopen(urllib.request.Request(f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{Z}/{x}/{y}.png", headers={"User-Agent": "emrelevo/1.0"}), timeout=60).read())
    a = np.asarray(Image.open(f).convert("RGB"), np.float32); return a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
x0, x1, y0, y1 = int(tx(LON0)) - 1, int(tx(LON1)) + 1, int(ty(LAT1)) - 1, int(ty(LAT0)) + 1
mos = np.zeros(((y1 - y0 + 1) * 256, (x1 - x0 + 1) * 256), np.float32)
for y in range(y0, y1 + 1):
    for x in range(x0, x1 + 1): mos[(y - y0) * 256:(y - y0 + 1) * 256, (x - x0) * 256:(x - x0 + 1) * 256] = tile(x, y)
print("mosaico", mos.shape, flush=True)
lons = np.linspace(LON0, LON1, W); lats = np.linspace(LAT1, LAT0, H)
px = (tx(lons) - x0) * 256 - 0.5; py = np.array([(ty(l) - y0) * 256 - 0.5 for l in lats])
def amostra(px, py):
    ix = np.clip(np.floor(px).astype(int), 0, mos.shape[1] - 2); iy = np.clip(np.floor(py).astype(int), 0, mos.shape[0] - 2)
    fx = np.clip(px - ix, 0, 1); fy = np.clip(py - iy, 0, 1)
    if px.ndim == 1: ix, iy, fx, fy = ix[None, :], iy[:, None], fx[None, :], fy[:, None]
    a = mos[iy, ix]; b = mos[iy, ix + 1]; c = mos[iy + 1, ix]; d = mos[iy + 1, ix + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy
z = amostra(px, py).astype(np.float32); print("alt", float(z.min()), float(z.max()), z.shape, flush=True)
# máscara terra/mar: NASA GIBS OSM_Land_Water_Map (o Terrarium tem ruído positivo de 0–4 m no mar costeiro)
MK = R / "work/v6/mask_OSM_Land_Water_Map.png"
if not MK.exists(): MK.write_bytes(urllib.request.urlopen(urllib.request.Request(f"https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?SERVICE=WMS&REQUEST=GetMap&VERSION=1.1.1&LAYERS=OSM_Land_Water_Map&STYLES=&FORMAT=image/png&SRS=EPSG:4326&BBOX={LON0},{LAT0},{LON1},{LAT1}&WIDTH={W}&HEIGHT={H}", headers={"User-Agent": "emrelevo/1.0"}), timeout=120).read())
def blur(a, r):
    k = int(max(1, round(r * 3))); x = np.arange(-k, k + 1); g = np.exp(-x ** 2 / (2 * r * r)); g /= g.sum(); a = a.astype(np.float32)
    a = np.pad(a, ((0, 0), (k, k)), mode="edge"); a = sum(g[i] * a[:, i:i + a.shape[1] - 2 * k] for i in range(2 * k + 1))
    a = np.pad(a, ((k, k), (0, 0)), mode="edge"); return sum(g[i] * a[i:i + a.shape[0] - 2 * k] for i in range(2 * k + 1)).astype(np.float32)
terra_m = blur((np.asarray(Image.open(MK).convert("L")) < 100).astype(np.float32), 3.0) > 0.5
prox = 8 + 260 * np.clip(1 - 2 * blur(terra_m.astype(np.float32), 35), 0, 1) ** 1.2        # profundidade de apoio (o Terrarium tem remendos planos no mar)
z = np.where(terra_m, np.maximum(z, 0.5), -np.maximum(np.clip(-z, 0, 400), prox)).astype(np.float32)
np.save(R / "work/v6/dem.npy", z)
def blur(a, r):
    k = int(max(1, round(r * 3))); x = np.arange(-k, k + 1); g = np.exp(-x ** 2 / (2 * r * r)); g /= g.sum(); a = a.astype(np.float32)
    a = np.pad(a, ((0, 0), (k, k)), mode="edge"); a = sum(g[i] * a[:, i:i + a.shape[1] - 2 * k] for i in range(2 * k + 1))
    a = np.pad(a, ((k, k), (0, 0)), mode="edge"); return sum(g[i] * a[i:i + a.shape[0] - 2 * k] for i in range(2 * k + 1)).astype(np.float32)
zs = blur(z, 1.2); mpp = 111320.0 / K          # metros por pixel (o mesmo em x e y por construção)
gy, gx = np.gradient(zs, mpp)
decliv = np.hypot(gx, gy) * 100                  # %
def sombra(zf, az=315.0, alt=38.0):
    gy_, gx_ = np.gradient(zs * zf, mpp); sl = np.arctan(np.hypot(gx_, gy_)); asp = np.arctan2(-gx_, -gy_)
    a, e = np.radians(az), np.radians(alt); return np.clip(np.sin(e) * np.cos(sl) + np.cos(e) * np.sin(sl) * np.cos(a - asp), 0, 1)
hs = sombra(2.2); hs2 = sombra(1.6, 300, 45)
rng = np.random.default_rng(6)
def hexc(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255
def rampa(v, pts):
    xs = np.array([p[0] for p in pts], np.float32); cs = np.stack([hexc(p[1]) for p in pts])
    return np.stack([np.interp(v, xs, cs[:, k]) for k in range(3)], -1)
mar = z <= 0.5
ruido = blur(rng.random((H, W), dtype=np.float32), 1.5) - 0.5
# A: satélite sintético (mata atlântica verde, planície clara, mar azul-verde)
terra = rampa(np.clip(z, 0, 1200), [(0, "#9CAA73"), (25, "#86A265"), (120, "#5F8B4B"), (400, "#41723F"), (800, "#335F38"), (1200, "#4C6B45")])
terra = terra * (0.62 + 0.62 * hs[..., None]) * (1 + 0.5 * ruido[..., None])
prof = np.clip(-z, 0, 400)
agua = rampa(prof, [(0, "#2C7A93"), (15, "#1C5F85"), (60, "#144673"), (400, "#0C2C52")])
agua = agua * (0.9 + 0.2 * hs2[..., None])
A = np.where(mar[..., None], agua, terra)
costa = blur(mar.astype(np.float32), 2.0); borda = np.clip(1 - np.abs(costa - 0.5) * 2, 0, 1) ** 3
A = A * (1 - 0.35 * borda[..., None]) + 0.35 * borda[..., None] * np.array([0.85, 0.92, 0.9], np.float32)
A = np.clip(A, 0, 1)
Image.fromarray((A * 255).astype(np.uint8)).save(PUB / "A.jpg", quality=90)
# B: relevo editorial (navy; terra em papel sombreado; curvas de nível a cada 100 m)
base = np.array([0x1F, 0x2A, 0x44], np.float32) / 255
terraB = rampa(hs ** 1.1, [(0, "#2A3453"), (0.45, "#6C6A66"), (0.7, "#B9A47F"), (1.0, "#EADFC6")])
alt_t = np.clip(z / 900, 0, 1)[..., None]
terraB = terraB * (0.72 + 0.28 * alt_t) * (1 - 0.0 * alt_t)
curva = (np.abs(((zs + 50) % 100) - 50) < (mpp * 0.0 + 1.6 + decliv * 0.0)).astype(np.float32); curva = blur(curva, 0.6) * (z > 20)
terraB = terraB * (1 - 0.22 * curva[..., None])
aguaB = base * (0.85 + 0.35 * np.clip(prof / 400, 0, 1)[..., None] * -1 + 0.35) * np.ones((H, W, 1), np.float32)
aguaB = np.clip(aguaB * (0.9 + 0.1 * hs2[..., None]), 0, 1)
B = np.where(mar[..., None], aguaB, terraB)
B = B * (1 - 0.5 * borda[..., None]) + 0.5 * borda[..., None] * np.array([0.95, 0.9, 0.78], np.float32)
Image.fromarray((np.clip(B, 0, 1) * 255).astype(np.uint8)).save(PUB / "B.jpg", quality=90)
# máscaras de declividade (coral): > 40 % (21,8°) e > 30° (58 %)
for nome, lim in (("decliv40", 40), ("decliv30g", 57.7)):
    m = np.clip((decliv - lim) / 12, 0, 1) * (~mar); m = blur(m, 1.0)
    rgba = np.zeros((H, W, 4), np.uint8); rgba[..., 0] = 232; rgba[..., 1] = 80; rgba[..., 2] = 91; rgba[..., 3] = (np.clip(m, 0, 1) * 215).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(PUB / f"{nome}.png")
    print(nome, "fração de terra >", lim, "%:", float((decliv[~mar] > lim).mean()))
json.dump({"bbox": [LON0, LON1, LAT0, LAT1], "w": W, "h": H, "k": K}, open(PUB / "geo6.json", "w"))
# camada IMERG (já em lon/lat no bbox do JSON) reamostrada para o nosso bbox
nj = json.load(open(R / "dados/nasa/litoral-2023.json")); bb = nj["bbox"]
im = Image.open(R / "dados/nasa/litoral-2023-camada.png").convert("RGBA"); iw, ih = im.size
cx0 = (LON0 - bb[0]) / (bb[2] - bb[0]) * iw; cx1 = (LON1 - bb[0]) / (bb[2] - bb[0]) * iw
cy0 = (bb[3] - LAT1) / (bb[3] - bb[1]) * ih; cy1 = (bb[3] - LAT0) / (bb[3] - bb[1]) * ih
im.crop((int(cx0), int(cy0), int(cx1), int(cy1))).resize((W, H), Image.NEAREST).save(PUB / "imerg.png")
# blocos 3D cortados: faixa de 2,8 km em volta do perfil (sai do mar a ~1,2 km antes da costa)
def bil(lon, lat):
    fx = (lon - LON0) / (LON1 - LON0) * (W - 1); fy = (LAT1 - lat) / (LAT1 - LAT0) * (H - 1)
    ix = int(np.clip(np.floor(fx), 0, W - 2)); iy = int(np.clip(np.floor(fy), 0, H - 2)); u, v = fx - ix, fy - iy
    return float((z[iy, ix] * (1 - u) + z[iy, ix + 1] * u) * (1 - v) + (z[iy + 1, ix] * (1 - u) + z[iy + 1, ix + 1] * u) * v)
perf = json.load(open(R / "dados/perfis.json"))["perfis"]; out = {}
for chave, p in (("cruzeiro", perf[1]), ("sahy", perf[2])):
    la0, lo0 = p["de"]; la1, lo1 = p["ate"]; Lkm = p["comprimento_km"]
    dxk = (lo1 - lo0) * 111.32 * math.cos(math.radians(la0)); dyk = (la1 - la0) * 111.32; n = math.hypot(dxk, dyk)
    ux, uy = dxk / n, dyk / n; vx, vy = -uy, ux           # u ao longo (mar → serra), v perpendicular
    ni, nj_, lw = 130, 15, 2.8; km0 = -1.2; km1 = min(n, 9.0 if chave == "sahy" else 9.4)
    rows = []
    for j in range(nj_):
        off = lw * j / (nj_ - 1); r = []   # j=0 = a linha do perfil (face do corte); o bloco se estende 2,8 km para o lado
        for i in range(ni):
            s = km0 + (km1 - km0) * i / (ni - 1)
            lon = lo0 + (s * ux + off * vx) / (111.32 * math.cos(math.radians(la0))); lat = la0 + (s * uy + off * vy) / 111.32
            r.append(round(max(bil(lon, lat), -25.0), 1))
        rows.append(r)
    out[chave] = {"nome": p["nome"], "km0": km0, "km1": km1, "largura_km": lw, "z": rows, "topo_m": p["topo_m"], "km_700": p["km_costa_ate_700m"]}
    print(chave, "max", max(max(r) for r in rows))
json.dump(out, open(PUB / "blocos3d.json", "w"))
