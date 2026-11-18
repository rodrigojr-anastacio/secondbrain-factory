#!/usr/bin/env python3
"""012-portugal: silhuetas reais na MESMA escala (Pernambuco, Portugal continental, Espanha continental), compostas no código.
Fontes: Natural Earth 50m (domínio público) para PT/ES; malha do IBGE (UF 26) para Pernambuco. Projeção sinusoidal (equivalente, preserva área)
recentrada em cada forma (PE) e comum a PT+ES (posição relativa real). Saída: thumbs/escala-base.png (RGBA só silhuetas) e thumbs/escala.json (geometria em px).
Uso (pasta do vídeo): ../../../../tools/.venv/bin/python thumbs/escala.py"""
import json, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
K = 111.32
ne = json.load(open("/home/hermes/cache/nasa/ne_50m_admin_0_countries.geojson"))
ib = json.load(open("/home/hermes/cache/nasa/ibge-ufs.geojson"))

def polys(geom):
    if geom["type"] == "Polygon": return [geom["coordinates"][0]]
    return [p[0] for p in geom["coordinates"]]
def maior(ps):
    def area(r):
        a = np.array(r); return abs(np.sum(a[:-1, 0] * a[1:, 1] - a[1:, 0] * a[:-1, 1])) / 2
    return max(ps, key=area)
pt = maior(polys([f for f in ne["features"] if f["properties"]["ADMIN"] == "Portugal"][0]["geometry"]))
es = maior(polys([f for f in ne["features"] if f["properties"]["ADMIN"] == "Spain"][0]["geometry"]))
pe = maior(polys([f for f in ib["features"] if f["properties"]["codarea"] == "26"][0]["geometry"]))

def sin(ring, lon0):
    a = np.array(ring); return np.c_[(a[:, 0] - lon0) * np.cos(np.radians(a[:, 1])) * K, -a[:, 1] * K]   # km, y para baixo
def area_km2(xy):
    return abs(np.sum(xy[:-1, 0] * xy[1:, 1] - xy[1:, 0] * xy[:-1, 1])) / 2
lon0 = -5.0
PT, ES = sin(pt, lon0), sin(es, lon0)
a = np.array(pe); PE = sin(pe, a[:, 0].mean())
print("área km²: PE %.0f · PT %.0f · ES %.0f · ES/PT %.1f · PE/PT %.2f" % (area_km2(PE), area_km2(PT), area_km2(ES), area_km2(ES) / area_km2(PT), area_km2(PE) / area_km2(PT)))

W, H = 1536, 864
def montar(W=W, H=H, escala=None):
    # PT+ES juntos; PE à esquerda de PT, centro vertical de PT, com folga
    ptb = (PT[:, 0].min(), PT[:, 0].max(), PT[:, 1].min(), PT[:, 1].max())
    pecx = ptb[0] - 70 - (PE[:, 0].max() - PE[:, 0].min()) / 2
    pcy = (ptb[2] + ptb[3]) / 2
    PE2 = PE - np.array([PE[:, 0].mean() - pecx, PE[:, 1].mean() - pcy])
    allx = np.r_[PE2[:, 0], PT[:, 0], ES[:, 0]]; ally = np.r_[PE2[:, 1], PT[:, 1], ES[:, 1]]
    s = escala or 0.62 * H / (ES[:, 1].max() - ES[:, 1].min()) * 1.0
    x0 = PE2[:, 0].min(); cy = pcy
    f = lambda P: np.c_[(P[:, 0] - x0) * s + 90, (P[:, 1] - cy) * s + H / 2 + 20]
    return f(PE2), f(PT), f(ES), s
PE_, PT_, ES_, s = montar()
print("px/km", round(s, 3), "ES x máx", ES_[:, 0].max(), "PE caixa", PE_.min(0), PE_.max(0), "PT", PT_.min(0), PT_.max(0))

def pergaminho(W, H, seed=3):
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (H // 4, W // 4)); n = np.array(Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype("uint8")).resize((W, H), Image.BICUBIC)) / 255.0
    base = np.array([243, 232, 203], float); im = base[None, None, :] * (0.93 + 0.1 * n[..., None])
    yy, xx = np.mgrid[0:H, 0:W]; v = ((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2
    im *= (1 - 0.13 * v[..., None]); return Image.fromarray(np.clip(im, 0, 255).astype("uint8"))

def desenhar(W=W, H=H, partes=("PE", "PT", "ES")):
    im = pergaminho(W, H); d = ImageDraw.Draw(im)
    cores = {"PE": (88, 168, 74), "PT": (247, 194, 27), "ES": (74, 74, 80)}
    for nome, P in (("ES", ES_), ("PT", PT_), ("PE", PE_)):
        if nome not in partes: continue
        pts = [tuple(p) for p in P]
        sh = [(x + 7, y + 7) for x, y in pts]; d.polygon(sh, fill=(120, 100, 70))
        d.polygon(pts, fill=cores[nome]); d.line(pts + [pts[0]], fill=(10, 10, 10), width=7, joint="curve")
    return im

if __name__ == "__main__":
    im = desenhar(); im.save("thumbs/escala-base.png")
    json.dump({"PE": PE_.tolist(), "PT": PT_.tolist(), "ES": ES_.tolist(), "W": W, "H": H, "px_km": s}, open("thumbs/escala.json", "w"))
    im.convert("RGB").save("public/img/escala_pe_pt_es.jpg", quality=92)
    print("ok")
