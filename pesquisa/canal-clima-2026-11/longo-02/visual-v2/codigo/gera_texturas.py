# Visual v2 (Em Relevo 002): gera as texturas de cor dos estilos A/B/C e os mapas de altura a partir de work/v2/
# (NASA Blue Marble via GIBS + NOAA ETOPO 2022) -> remotion/public/v2/
#   <estilo>_<regiao>.jpg  cor (relevo sombreado já "assado" na textura)
#   alt_<regiao>.png       altura em 16 bits (R = alto, G = baixo), metros em [-11000, 7000]
# Uso: python3 gera_texturas.py [A B C]
import sys
from pathlib import Path
import numpy as np
import json
from PIL import Image, ImageFilter, ImageDraw

Image.MAX_IMAGE_PIXELS = None
RAIZ = Path(__file__).resolve().parents[2]
WK, PUB = RAIZ / "work" / "v2", RAIZ / "remotion" / "public" / "v2"
PUB.mkdir(parents=True, exist_ok=True)
# (lon0, lon1, lat0, lat1, largura final da textura, passo do ETOPO em minutos)
REG = {"br_largo": (-140.0, 20.0, -75.0, 35.0, 6144, 6), "br_det": (-84.0, -28.0, -40.0, 8.0, 8192, 2), "pac": (85.0, 310.0, -45.0, 65.0, 6144, 6)}
ESTILOS = [a for a in sys.argv[1:] if a in "ABC"] or ["A", "B", "C"]
# fase 2: REGIOES=pac python3 gera_texturas.py A B  -> só as regiões pedidas
import os
if os.environ.get("REGIOES"): REG = {k: v for k, v in REG.items() if k in os.environ["REGIOES"].split(",")}
rng = np.random.default_rng(7)


def hexc(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255


def rampa(v, pontos):
    xs = np.array([p[0] for p in pontos], np.float32); cs = np.stack([hexc(p[1]) for p in pontos])
    return np.stack([np.interp(v, xs, cs[:, k]) for k in range(3)], -1)


def redim(a, w, h, metodo=Image.BICUBIC):
    return np.asarray(Image.fromarray(a.astype(np.float32), mode="F").resize((w, h), metodo))


def sombra(z, passo_min, lat0, lat1, zf, az=315.0, alt=40.0):
    # hillshade clássico (Horn simplificado); z em metros, grade em graus
    ny, nx = z.shape
    lat = np.linspace(lat1, lat0, ny)[:, None]
    dy = passo_min / 60 * 111320.0; dx = dy * np.cos(np.radians(lat))
    gy, gx = np.gradient(z * zf)
    gx = gx / dx; gy = -gy / dy
    a, e = np.radians(az), np.radians(alt)
    slope = np.arctan(np.hypot(gx, gy)); aspect = np.arctan2(-gx, gy)
    hs = np.sin(e) * np.cos(slope) + np.cos(e) * np.sin(slope) * np.cos(a - aspect)
    return np.clip(hs, 0, 1)


def ruido(w, h, escala, amp):
    n = rng.random((max(2, h // escala), max(2, w // escala)), dtype=np.float32)
    return (redim(n, w, h) - 0.5) * 2 * amp


def borda(mask, w_px):
    # linha de costa: diferença entre a máscara e ela borrada (sem scipy)
    m = Image.fromarray((mask * 255).astype(np.uint8))
    b = np.asarray(m.filter(ImageFilter.GaussianBlur(w_px)), np.float32) / 255
    return np.clip(1 - np.abs(b - 0.5) * 2, 0, 1) ** 2   # pico na transição


def satur(c, k):
    l = c.mean(-1, keepdims=True); return np.clip(l + (c - l) * k, 0, 1)


# rios e lagos (Natural Earth 10 m, domínio público) pintados na textura
COR_RIO = {"A": ("#2F6E96", 0.55), "B": ("#5F8FAE", 0.95), "C": ("#3C7680", 0.9)}
NE_RIOS = json.load(open(WK / "ne_10m_rivers_lake_centerlines.geojson"))["features"]
NE_LAGOS = json.load(open(WK / "ne_10m_lakes.geojson"))["features"]


def rios(out, nome, E, lon0, lon1, lat0, lat1, W, H):
    pxg = W / (lon1 - lon0)   # px por grau
    m = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(m)
    P = lambda c: ((c[0] - lon0) * pxg, (lat1 - c[1]) * pxg)
    def dentro(cs): return any(lon0 - 1 < c[0] < lon1 + 1 and lat0 - 1 < c[1] < lat1 + 1 for c in cs[::5] + cs[-1:])
    for f in NE_RIOS:
        g, sr = f["geometry"], f["properties"].get("scalerank", 10) or 10
        if not g or sr > (9 if pxg > 100 else 6): continue
        linhas = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
        larg = max(1, round((0.045 - 0.0035 * sr) * pxg))
        for l in linhas:
            if len(l) > 1 and dentro(l): dr.line([P(c) for c in l], fill=255, width=larg, joint="curve")
    for f in NE_LAGOS:
        g = f["geometry"]
        if not g: continue
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for pl in polys:
            if dentro(pl[0]): dr.polygon([P(c) for c in pl[0]], fill=255)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(0.7)), np.float32)[..., None] / 255 * COR_RIO[E][1]
    return (out * (1 - a) + hexc(COR_RIO[E][0]) * 255 * a).astype(np.uint8)


for nome, (lon0, lon1, lat0, lat1, W, passo) in REG.items():
    H = round(W * (lat1 - lat0) / (lon1 - lon0))
    z = np.load(WK / f"{nome}_etopo.npy")
    # altura (independe do estilo): 16 bits, resolução da grade ETOPO
    zz = np.clip((z + 11000) / 18000 * 65535, 0, 65535).astype(np.uint32)
    alt = np.stack([zz >> 8, zz & 255, np.zeros_like(zz)], -1).astype(np.uint8)
    Image.fromarray(alt).save(PUB / f"alt_{nome}.png")
    # campos na resolução da textura
    zT = redim(z, W, H)
    terra = (zT > 0).astype(np.float32)
    hs_t = redim(sombra(z, passo, lat0, lat1, 2.2 if passo > 2 else 3.0), W, H)       # relevo de terra exagerado
    hs_m = redim(sombra(np.minimum(z, 0), passo, lat0, lat1, 0.9), W, H)                  # batimetria (suave)
    flat = np.sin(np.radians(40))
    print(nome, W, H, "campos ok", flush=True)
    costa_b = {E: borda(terra, (1.6 if W > 7000 else 1.2) if E == "B" else (1.4 if W > 7000 else 1.0)) for E in ESTILOS if E in "BC"}
    if "C" in ESTILOS:
        halo = np.asarray(Image.fromarray((terra * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(W / 260)), np.float32) / 255
        nC1, nC2, nC3, nC4, nC5 = ruido(W, H, 220, 0.05), ruido(W, H, 40, 0.025), ruido(W, H, 180, 0.035), ruido(W, H, 30, 0.02), ruido(W, H, 2, 0.022)
    if "B" in ESTILOS: nB = ruido(W, H, 3, 0.018)
    for E in ESTILOS:
        out = np.zeros((H, W, 3), np.uint8)
        if E in "AB":
            bm8 = np.asarray(Image.open(WK / f"{nome}_bm.jpg").convert("RGB").resize((W, H), Image.LANCZOS))
            bm_l = bm8.astype(np.float32).mean(-1) / 255
            oc_bm = (((bm8[..., 2].astype(np.int16) > bm8[..., 0].astype(np.int16) + 5) & (bm_l < 0.22)) | (bm_l < 0.12))   # pixels quase pretos da costa também são mar
            perto = np.asarray(Image.fromarray(((zT < 0) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(W / 1400)), np.float32) > 8   # a poucos km do mar do ETOPO
            oc_bm = ((oc_bm & perto) | (zT < -60)).astype(np.uint8) * 255   # floresta escura longe da costa não vira mar
            ocA = np.asarray(Image.fromarray(oc_bm).filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
            del bm_l, oc_bm
        for r0 in range(0, H, 768):
            sl = slice(r0, min(H, r0 + 768))
            zc, tc, hst, hsm = zT[sl], terra[sl][..., None], hs_t[sl], hs_m[sl]
            d = np.clip(-zc, 0, 8000)
            if E == "A":   # satélite realista: Blue Marble (cor real) + sombreado ETOPO + oceano azul com batimetria
                bm = bm8[sl].astype(np.float32) / 255; oc = ocA[sl][..., None]
                fs = np.clip(hst / flat, 0.35, 1.55)[..., None]
                land = satur(np.clip((bm * 1.18) ** 0.92, 0, 1), 1.18) * (0.25 + 0.75 * fs)
                mar = rampa(d, [(0, "#4FA3C0"), (60, "#3B93B6"), (200, "#2A78A3"), (1200, "#1C5788"), (3500, "#163F6E"), (6000, "#10305A")])
                mar = mar * np.clip(0.55 + 0.6 * (hsm / flat), 0.6, 1.25)[..., None]
                mar = mar * 0.85 + bm * 0.6 * 0.15 + 0.01
                cor = land * (1 - oc) + mar * oc
            elif E == "B":   # relevo sombreado editorial na paleta do canal (papel, coral, navy)
                land = rampa(zc, [(0, "#EFE3C8"), (150, "#E8D7B4"), (500, "#DDC59B"), (1000, "#CFAE80"), (2000, "#B88F65"), (3500, "#9A7658"), (4800, "#B9A898"), (6000, "#F4EFE8")])
                fs = np.clip(hst / flat, 0.25, 1.45)[..., None]
                land = land * (0.18 + 0.82 * fs) + 0.035 * (fs - 1)
                bmB = satur(bm8[sl].astype(np.float32) / 255 * 1.35, 0.75)    # 28% da cor real (floresta, cerrado, deserto) sob o relevo
                land = land * 0.72 + np.clip(bmB, 0, 1) * (0.3 + 0.7 * fs) * 0.28
                mar = rampa(d, [(0, "#9CBBC6"), (120, "#7FA4B6"), (600, "#56809E"), (2000, "#3A5F82"), (4000, "#2A4366"), (6500, "#1F2A44")])
                mar = mar * np.clip(0.7 + 0.42 * (hsm / flat), 0.75, 1.15)[..., None]
                costa = costa_b["B"][sl][..., None]
                cor = land * tc + mar * (1 - tc)
                cor = cor * (1 - 0.55 * costa) + hexc("#2B2622") * 0.55 * costa + nB[sl][..., None]
            else:   # C: pergaminho cartográfico (papel envelhecido + mar verde-azulado de tinta)
                papel = hexc("#E2CB9A") + nC1[sl][..., None] * hexc("#8A6A3A") + nC2[sl][..., None]
                fs = np.clip(hst / flat, 0.45, 1.3)[..., None]
                land = papel * (0.45 + 0.55 * fs) * (1 - 0.18 * np.clip(zc / 4000, 0, 1))[..., None]
                mar = rampa(d, [(0, "#6FA3A3"), (300, "#4F8C92"), (2500, "#3C7680"), (6000, "#2E6170")])
                mar = mar + 0.10 * halo[sl][..., None] + nC3[sl][..., None] + nC4[sl][..., None]
                costa = costa_b["C"][sl][..., None]
                cor = land * tc + mar * (1 - tc)
                cor = cor * (1 - 0.7 * costa) + hexc("#3A2A1C") * 0.7 * costa + nC5[sl][..., None]
            out[sl] = (np.clip(cor, 0, 1) * 255).astype(np.uint8)
        if E in "AB": del bm8
        if E == "A": del ocA
        if nome != "pac": out = rios(out, nome, E, lon0, lon1, lat0, lat1, W, H)
        im = Image.fromarray(out)
        if E == "A": im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=60, threshold=2))
        im.save(PUB / f"{E}_{nome}.jpg", quality=90)
        print(" ", E, nome, flush=True)
print("ok")
