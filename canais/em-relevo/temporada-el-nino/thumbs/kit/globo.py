"""Globo ortográfico com textura NASA Blue Marble (domínio público) + anomalia real de TSM NOAA OISST v2.1 (26/11/2026).
Base para as thumbs da temporada El Niño do Em Relevo (28/11/2026). US$ 0.
Uso: from globo import render_globo  -> PIL.Image
Dados em $TMPDIR/elnino (anom.npy 0,5°, textura world*.jpg)."""
import os, numpy as np
from PIL import Image, ImageFilter
D = os.path.expanduser("~/cache/tmp/elnino")
Image.MAX_IMAGE_PIXELS = None

def _tex(nome):
    return np.asarray(Image.open(os.path.join(D, nome)).convert("RGB"), dtype=np.float32) / 255.0

def cmap_quente(a):
    """anomalia °C -> (rgb, alfa). <0,8 transparente; 1 laranja; 2 vermelho-laranja; 3+ vermelho vivo/amarelo no núcleo."""
    stops = [(0.8, (1.00, 0.78, 0.20), 0.0), (1.2, (1.00, 0.62, 0.05), 0.70), (2.0, (1.00, 0.33, 0.02), 0.88),
             (3.0, (0.93, 0.08, 0.05), 0.95), (4.5, (1.00, 0.85, 0.25), 1.0)]
    rgb = np.zeros(a.shape + (3,), np.float32); al = np.zeros(a.shape, np.float32)
    x = np.nan_to_num(a, nan=-9)
    for (v0, c0, a0), (v1, c1, a1) in zip(stops[:-1], stops[1:]):
        m = (x >= v0) & (x < v1); t = ((x - v0) / (v1 - v0))[m][:, None]
        rgb[m] = np.array(c0) * (1 - t) + np.array(c1) * t; al[m] = a0 * (1 - t[:, 0]) + a1 * t[:, 0]
    m = x >= stops[-1][0]; rgb[m] = stops[-1][1]; al[m] = 1.0
    return rgb, al

def render_globo(W=1920, H=1080, lon0=-95.0, lat0=-8.0, raio=1.0, cx=0.5, cy=0.5, textura="world.topo.bathy.200412.3x5400x2700.jpg",
                 anom=True, anom_forca=1.0, oceano_claro=0.0, anom_arquivo="anom_f.npy", extra=None, oceano_cor=(40, 120, 200), brilho=1.12, sat=1.25, fundo=(8, 14, 32), atm=(120, 190, 255), luz=(-0.35, 0.25)):
    """raio em frações da altura (1.0 = diâmetro = 2H, globo maior que a tela)."""
    tex = _tex(textura); th, tw, _ = tex.shape
    R = raio * H; yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    X = (xx - cx * W) / R; Y = -(yy - cy * H) / R; r2 = X * X + Y * Y; dentro = r2 <= 1
    Z = np.sqrt(np.clip(1 - r2, 0, 1))
    la0, lo0 = np.radians(lat0), np.radians(lon0)
    lat = np.arcsin(np.clip(Z * np.sin(la0) + Y * np.cos(la0), -1, 1))
    lon = lo0 + np.arctan2(X, Z * np.cos(la0) - Y * np.sin(la0))
    latd = np.degrees(lat); lond = (np.degrees(lon) + 180) % 360 - 180
    u = ((lond + 180) / 360 * tw).astype(int) % tw; v = np.clip(((90 - latd) / 180 * th).astype(int), 0, th - 1)
    img = tex[v, u]
    # realce: brilho + saturação
    g = img.mean(-1, keepdims=True); img = np.clip((g + (img - g) * sat) * brilho, 0, 1)
    if anom:
        A = np.load(os.path.join(D, anom_arquivo)); OC = np.load(os.path.join(D, "oceano.npy"))  # 0,5°, lat -89.875.., lon 0.125..
        fi = (latd + 89.875) / 0.5; fj = ((lond % 360) - 0.125) / 0.5
        i0 = np.clip(np.floor(fi).astype(int), 0, A.shape[0] - 2); j0 = np.floor(fj).astype(int) % A.shape[1]; j1 = (j0 + 1) % A.shape[1]
        ti = np.clip(fi - i0, 0, 1); tj = fj - np.floor(fj)
        bil = lambda M: (M[i0, j0] * (1 - ti) * (1 - tj) + M[i0 + 1, j0] * ti * (1 - tj) + M[i0, j1] * (1 - ti) * tj + M[i0 + 1, j1] * ti * tj)
        a = bil(A); oce = np.clip((bil(OC) - 0.35) / 0.4, 0, 1)
        # suaviza bordas: blur do campo
        if oceano_claro > 0:
            k = (oce * oceano_claro)[..., None]; img = img * (1 - k) + (np.array(oceano_cor) / 255 * (0.75 + 0.5 * img.mean(-1, keepdims=True) / max(img.mean(), 1e-3) * 0.5)) * k
        crgb, cal = cmap_quente(a); cal *= anom_forca * oce
        ci = Image.fromarray((np.dstack([crgb, cal[..., None]]) * 255).astype(np.uint8), "RGBA").filter(ImageFilter.GaussianBlur(1.2))
        c = np.asarray(ci, np.float32) / 255; img = img * (1 - c[..., 3:]) + c[..., :3] * c[..., 3:]
    if extra is not None: img = extra(img, latd, lond)
    # luz/limbo
    lx, ly = luz; n = np.dstack([X, Y, Z]); L = np.array([lx, ly, 0.9]); L /= np.linalg.norm(L)
    sh = np.clip((n @ L), 0, 1) * 0.55 + 0.6; img = np.clip(img * sh[..., None], 0, 1)
    limbo = np.clip((np.sqrt(r2) - 0.82) / 0.18, 0, 1)[..., None]
    img = img * (1 - 0.35 * limbo) + np.array(atm) / 255 * 0.35 * limbo
    out = np.ones((H, W, 3), np.float32) * np.array(fundo) / 255
    # halo atmosférico fora do disco
    rr = np.sqrt(r2); halo = np.clip(1 - (rr - 1) / 0.06, 0, 1) * (rr > 1)
    out = out * (1 - halo[..., None] * 0.8) + np.array(atm) / 255 * halo[..., None] * 0.8
    out[dentro] = img[dentro]
    return Image.fromarray((out * 255).astype(np.uint8)), (latd, lond, dentro, R)

def tela(lon, lat, W=1920, H=1080, lon0=-95.0, lat0=-8.0, raio=1.0, cx=0.5, cy=0.5):
    """lon/lat -> pixel (para setas/rótulos)."""
    la, lo = np.radians(lat), np.radians(lon); la0, lo0 = np.radians(lat0), np.radians(lon0)
    x = np.cos(la) * np.sin(lo - lo0); y = np.cos(la0) * np.sin(la) - np.sin(la0) * np.cos(la) * np.cos(lo - lo0)
    R = raio * H; return cx * W + x * R, cy * H - y * R
