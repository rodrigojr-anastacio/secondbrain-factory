"""Amostras de thumb da temporada Super El Niño (Em Relevo, 28/11/2026). US$ 0, sem IA de imagem.
Dados reais: NASA Blue Marble NG (GIBS, domínio público), NOAA OISST v2.1 anomalia diária (26/11/2026 e 26/11/2015),
NASA GPM IMERG V07 anomalia de chuva 01/10–25/11/2026 (tools/nasa_chuva.py), Natural Earth / IBGE.
Uso (raiz do repo): tools/.venv/bin/python canais/em-relevo/temporada-el-nino/thumbs/kit/gera_thumbs.py
Saída: canais/em-relevo/temporada-el-nino/thumbs/*.jpg (1280×720) + *-320.jpg."""
import os, sys, json, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import globo, contorno, texto

R = os.path.expanduser("~/workspace/fabrica-youtube")
OUT = f"{R}/canais/em-relevo/temporada-el-nino/thumbs"
D = os.path.expanduser("~/cache/tmp/elnino")
W, H = 1920, 1080
AMARELO = (255, 214, 64); BRANCO = (251, 248, 241); CORAL = (232, 80, 91); TINTA = (14, 20, 38)


def cm_brasa(a):
    stops = [(1.5, (1.0, 0.55, 0.05), 0.0), (2.1, (1.0, 0.45, 0.02), 0.85), (2.9, (0.98, 0.12, 0.04), 0.95), (4.0, (1.0, 0.86, 0.3), 1.0)]
    rgb = np.zeros(a.shape + (3,), np.float32); al = np.zeros(a.shape, np.float32); x = np.nan_to_num(a, nan=-9)
    for (v0, c0, a0), (v1, c1, a1) in zip(stops[:-1], stops[1:]):
        m = (x >= v0) & (x < v1); t = ((x - v0) / (v1 - v0))[m][:, None]
        rgb[m] = np.array(c0) * (1 - t) + np.array(c1) * t; al[m] = a0 * (1 - t[:, 0]) + a1 * t[:, 0]
    m = x >= stops[-1][0]; rgb[m] = stops[-1][1]; al[m] = 1
    return rgb, al


globo.cmap_quente = cm_brasa
BASE = dict(textura="BlueMarble_NextGeneration.jpg", sat=1.35, brilho=1.2, oceano_claro=0.7)


def salva(im, nome):
    im = im.convert("RGB").resize((1280, 720), Image.LANCZOS)
    im.save(f"{OUT}/{nome}.jpg", quality=90)
    im.resize((320, 180), Image.LANCZOS).save(f"{OUT}/{nome}-320.jpg", quality=92)
    print(nome, os.path.getsize(f"{OUT}/{nome}.jpg") // 1024, "KB")


def globo_com_brasil(cam, anom="anom_f.npy", larg=7, **kw):
    im, _ = globo.render_globo(W=W, H=H, anom_arquivo=anom, **{**BASE, **kw}, **cam)
    im = im.convert("RGBA")
    contorno.desenha(im, contorno.pais("Brazil"), cam, cor=(255, 255, 255), larg=larg)
    return im


# ---------- E1 · A: globo claro, língua em brasa encostando no Brasil + "+3,5 °C" (mapa-lugar, controle) ----------
def e1_a():
    cam = dict(lon0=-84.0, lat0=-4.0, raio=1.2, cx=0.42, cy=0.70)
    im = globo_com_brasil(cam)
    texto.palavra(im, "ENCOSTOU", (60, 40), tam=300, cor=AMARELO, ancora="la", esp=18)
    salva(im, "e1-A-globo-encostou")


# ---------- E1 · B: curva real do Niño 3.4, 2026 disparando acima de 1982/1997/2015 (documento-evidencia) ----------
def serie(nome):
    t = open(f"{D}/{nome}.ascii").read().splitlines(); vals = {}
    for ln in t:
        m = re.match(r'^\[(\d+)\]\[(\d+)\], (.*)$', ln)
        if m:
            v = np.array([float(x) for x in m.group(3).split(',')]); v[np.abs(v) > 100] = np.nan
            vals.setdefault(int(m.group(1)), []).append(np.nanmean(v))
    return [float(np.mean(vals[k])) for k in sorted(vals)]


def e1_b():
    im = Image.new("RGBA", (W, H), (236, 244, 252, 255)); d = ImageDraw.Draw(im)
    # fundo: leve gradiente céu claro
    g = np.linspace(0, 1, H)[:, None, None]; arr = (np.array([224, 238, 252]) * (1 - g) + np.array([250, 252, 255]) * g) * np.ones((1, W, 1))
    im = Image.fromarray(arr.astype("uint8")).convert("RGBA"); d = ImageDraw.Draw(im)
    x0, x1, y0, y1 = 110, 1480, 1010, 330   # área do gráfico; eixo y: 1,6 → 3,8 °C
    def Y(v): return y0 - ((v - 1.6) / 2.2) * (y0 - y1)
    for v in (2, 3):
        d.line([(x0, Y(v)), (x1, Y(v))], fill=(180, 196, 214), width=3)
    series = {"1982": serie("n34_1982")[:30], "1997": serie("n34_1997")[:30], "2015": serie("n34_2015")[:30]}
    cores = {"1982": (150, 160, 175), "1997": (120, 135, 155), "2015": (85, 100, 125)}
    f = ImageFont.truetype(texto.ANTON, 92)
    for k, s in series.items():
        pts = [(x0 + i * (x1 - x0) / 29, Y(v)) for i, v in enumerate(s)]
        d.line(pts, fill=cores[k], width=16, joint="curve")
        d.text((x1 + 18, pts[-1][1]), k, font=f, fill=cores[k], anchor="lm")
    s26 = serie("n34_2026")  # 07–26/11 (20 dias) → posiciona do dia 7 ao 26
    pts = [(x0 + (6 + i) * (x1 - x0) / 29, Y(v)) for i, v in enumerate(s26)]
    glow = Image.new("RGBA", im.size, (0, 0, 0, 0)); dg = ImageDraw.Draw(glow)
    dg.line(pts, fill=(255, 90, 30, 255), width=60, joint="curve"); glow = glow.filter(ImageFilter.GaussianBlur(22))
    im.alpha_composite(glow); d = ImageDraw.Draw(im)
    d.line(pts, fill=(226, 30, 30), width=26, joint="curve")
    d.ellipse([pts[-1][0] - 26, pts[-1][1] - 26, pts[-1][0] + 26, pts[-1][1] + 26], fill=(226, 30, 30))
    texto.palavra(im, "2026", (pts[0][0] - 10, pts[0][1] - 60), tam=260, cor=(226, 30, 30), contorno=(255, 255, 255), esp=14, ancora="ls")
    salva(im, "e1-B-curva-recorde")


# ---------- E1 · C: dois globos, 26/11/2015 × 26/11/2026 (antes-depois) ----------
def e1_c():
    cam = dict(lon0=-120.0, lat0=0.0, raio=0.52)
    a, _ = globo.render_globo(W=960, H=1080, anom_arquivo="anom2015_f.npy", cx=0.5, cy=0.58, **{**BASE, "oceano_claro": 0.75}, **cam, fundo=(232, 242, 252), atm=(160, 205, 255))
    b, _ = globo.render_globo(W=960, H=1080, anom_arquivo="anom_f.npy", cx=0.5, cy=0.58, **{**BASE, "oceano_claro": 0.75}, **cam, fundo=(232, 242, 252), atm=(160, 205, 255))
    camc = dict(cam, cx=0.5, cy=0.58)
    a = a.convert("RGBA"); b = b.convert("RGBA")
    contorno.desenha(a, contorno.pais("Brazil"), camc, larg=5); contorno.desenha(b, contorno.pais("Brazil"), camc, larg=5)
    im = Image.new("RGBA", (W, H), (232, 242, 252, 255)); im.paste(a, (0, 0)); im.paste(b, (960, 0))
    d = ImageDraw.Draw(im); d.rectangle([954, 0, 966, H], fill=(255, 255, 255))
    texto.palavra(im, "2015", (480, 40), tam=200, cor=BRANCO, contorno=TINTA, ancora="ma", esp=14)
    texto.palavra(im, "2026", (1440, 40), tam=200, cor=AMARELO, contorno=TINTA, ancora="ma", esp=14)
    salva(im, "e1-C-2015x2026")


# ---------- 002 · A: América do Sul de perto, língua quente batendo na costa + "JÁ CHEGOU" (mapa-lugar) ----------
def r002_a():
    cam = dict(lon0=-70.0, lat0=-12.0, raio=1.55, cx=0.52, cy=0.55)
    im = globo_com_brasil(cam, larg=9)
    texto.palavra(im, "JÁ CHEGOU", (1880, 1040), tam=250, cor=AMARELO, ancora="rs", esp=18)
    salva(im, "r002-A-globo-ja-chegou")


# ---------- 002 · B: Brasil de satélite com a chuva real out–nov/2026 (IMERG): Norte seco × Sul encharcado (conflito-xvy) ----------
def camada_imerg():
    im = np.asarray(Image.open(f"{D}/imerg/br-out-nov-anomalia-camada.png").convert("RGBA"), np.float32) / 255
    pg = [float(x) for x in open(f"{D}/imerg/br-out-nov-anomalia-camada.pgw").read().split()]
    seco = im[..., 0] > im[..., 2] + 0.05; molh = im[..., 2] > im[..., 0] + 0.05
    rgb = np.zeros(im.shape[:2] + (3,), np.float32); rgb[seco] = (1.0, 0.50, 0.08); rgb[molh] = (0.10, 0.55, 1.0)
    al = np.clip((im[..., 3] - 0.30) * 1.9, 0, 0.92) * (seco | molh)
    return rgb, al, pg


def r002_b():
    rgb, al, pg = camada_imerg(); dx, _, _, dy, x0, y0 = pg
    def extra(img, latd, lond):
        j = ((lond - x0) / dx).astype(int); i = ((latd - y0) / dy).astype(int)
        ok = (i >= 0) & (i < rgb.shape[0]) & (j >= 0) & (j < rgb.shape[1])
        a = np.zeros(latd.shape, np.float32); c = np.zeros(latd.shape + (3,), np.float32)
        a[ok] = al[i[ok], j[ok]]; c[ok] = rgb[i[ok], j[ok]]
        ai = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)); a = np.asarray(ai, np.float32) / 255
        return img * (1 - a[..., None]) + c * a[..., None]
    cam = dict(lon0=-53.0, lat0=-14.5, raio=1.62, cx=0.40, cy=0.50)
    im, _ = globo.render_globo(W=W, H=H, anom=True, anom_forca=0.0, extra=extra, **{**BASE}, **cam, fundo=(40, 110, 190))
    im = im.convert("RGBA"); contorno.desenha(im, contorno.pais("Brazil"), cam, cor=(255, 255, 255), larg=8)
    texto.palavra(im, "MESMA", (1880, 60), tam=250, cor=AMARELO, ancora="ra", esp=16)
    texto.palavra(im, "CAUSA?", (1880, 1020), tam=250, cor=AMARELO, ancora="rs", esp=16)
    salva(im, "r002-mesma-causa")




# ---------- E1 · B (r2): escala — a mancha de mar ≥ 3 °C acima do normal (26/11/2026) × o Brasil, mesma escala (projeção sinusoidal, igual-área) ----------
def e1_b2():
    A = np.load(f"{D}/anom_f.npy"); OC = np.load(f"{D}/oceano.npy")
    lat = -89.875 + 0.5 * np.arange(A.shape[0]); lon = 0.125 + 0.5 * np.arange(A.shape[1])
    s = 15.0  # px por grau (no equador)
    # mancha: Pacífico tropical 150E–80W, 20S–20N, >= 3 °C
    LA, LO = np.meshgrid(lat, lon, indexing="ij"); box = (LA > -20) & (LA < 20) & (LO > 150) & (LO < 285)
    m = box & (A >= 3.0) & (OC > 0)
    cx_lon = float(np.average(LO[m])); cy_lat = float(np.average(LA[m]))  # centróide da mancha
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = np.linspace(0, 1, H)[:, None, None]; bg = (np.array([214, 234, 252]) * (1 - g) + np.array([246, 251, 255]) * g) * np.ones((1, W, 1))
    im = Image.fromarray(bg.astype("uint8")).convert("RGBA")
    ox, oy = W * 0.5, H * 0.42
    def P(lo, la): return ox + (lo - cx_lon) * np.cos(np.radians(la)) * s, oy - (la - cy_lat) * s
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    ii, jj = np.where(m)
    for i, j in zip(ii, jj):
        x, y = P(lon[j], lat[i]); r = 0.5 * s * np.cos(np.radians(lat[i])) / 2 + 1.5
        v = A[i, j]; c = (255, int(max(40, 200 - (v - 3) * 120)), 20, 255)
        d.rectangle([x - r, y - s / 4 - 1, x + r, y + s / 4 + 1], fill=c)
    lay = lay.filter(ImageFilter.GaussianBlur(2.2))
    glow = lay.filter(ImageFilter.GaussianBlur(18)); im.alpha_composite(glow); im.alpha_composite(lay)
    # Brasil com textura de satélite, mesma escala, centrado sobre a mancha
    tex = Image.open(f"{D}/BlueMarble_NextGeneration.jpg").convert("RGB"); tw, th = tex.size
    br = contorno.pais("Brazil"); blon, blat = -53.0, -14.0
    bx, by = W * 0.36, H * 0.40
    def Q(lo, la): return bx + (lo - blon) * np.cos(np.radians(la)) * s, by - (la - blat) * s
    mask = Image.new("L", (W, H), 0); dm = ImageDraw.Draw(mask)
    for r in br: dm.polygon([Q(x, y) for x, y in r], fill=255)
    # textura projetada (inversa aproximada)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); la = blat - (yy - by) / s; lo = blon + (xx - bx) / (s * np.cos(np.radians(la)))
    u = ((lo + 180) / 360 * tw).astype(int) % tw; v = np.clip(((90 - la) / 180 * th).astype(int), 0, th - 1)
    T = np.asarray(tex, np.float32)[v, u] / 255; gm = T.mean(-1, keepdims=True); T = np.clip((gm + (T - gm) * 1.4) * 1.25, 0, 1)
    tim = Image.fromarray((T * 255).astype(np.uint8)).convert("RGBA"); tim.putalpha(mask)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(mask.filter(ImageFilter.GaussianBlur(14)).point(lambda p: p * 0.55))
    im.alpha_composite(sh, (10, 16)); im.alpha_composite(tim)
    ol = Image.new("RGBA", (W, H), (0, 0, 0, 0)); do = ImageDraw.Draw(ol)
    for r in br: pts = [Q(x, y) for x, y in r]; do.line(pts + [pts[0]], fill=(255, 255, 255, 255), width=7, joint="curve")
    im.alpha_composite(ol)
    texto.palavra(im, "MAR QUENTE", (W * 0.70, H * 0.80), tam=150, cor=BRANCO, contorno=(150, 20, 10), ancora="mm", esp=12)  # r3: sem "MAIOR" (o título diz)
    print("área >=3 °C (M km²):", round(float(np.nansum(((111.2 * 0.5) ** 2 * np.cos(np.radians(LA)))[m]) / 1e6), 1))
    salva(im, "e1-B-escala-mar-quente")


if __name__ == "__main__":
    qual = sys.argv[1:] or ["e1_a", "e1_b2", "e1_c", "r002_b"]
    for q in qual: globals()[q]()
