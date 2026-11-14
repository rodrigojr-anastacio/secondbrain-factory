"""Em Relevo: bases + thumbs do El Niño 2026 e do Sul do Brasil (reembalagem 14/11/2026), 100% com dados reais, custo US$ 0.
- El Niño: anomalia diária NOAA OISST v2.1 (longo-02/shared/sst_pacifico.json, 08/11/2026) >= 2 °C em laranja/vermelho sobre oceano navy
  liso, países do Natural Earth (longo-02/dados/ne110.json), Brasil em coral; câmera oblíqua (homografia); termômetro, seta e texto no código.
- Sul: Cone Sul (Natural Earth + estados IBGE PR/SC/RS em coral), Andes como parede extrudada com cume branco (crista de longo-02/shared/geo.json),
  fita ciano (rio de umidade) colada à encosta, sem ponta de seta.
Uso (raiz do repo): tools/.venv/bin/python pesquisa/reembalagem-2026-11-14/thumbs/emrelevo.py [nino|sul]"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

R = os.path.expanduser("~/workspace/fabrica-youtube")
L2 = f"{R}/pesquisa/canal-clima-2026-11/longo-02"
ANTON = f"{R}/pesquisa/canal-clima-2026-11/identidade/fontes/Anton-Regular.ttf"
NAVY = (20, 31, 56); NAVY2 = (14, 22, 42); CORAL = (232, 80, 91); YEL = (255, 214, 64)
OUT = f"{R}/pesquisa/reembalagem-2026-11-14/thumbs/em-relevo"
os.makedirs(OUT, exist_ok=True)


def anton(sz): return ImageFont.truetype(ANTON, sz)


def homografia(dst, src):
    """coeficientes PIL (saída->entrada): dst = 4 pontos na saída; src = 4 pontos na entrada."""
    A = []; B = []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return np.linalg.solve(np.array(A, float), np.array(B, float))


def proj_pt(coef, u, v):
    """entrada (u,v) -> saída (x,y): inverte a homografia."""
    a, b, c, d, e, f, g, h = coef
    M = np.array([[a, b, c], [d, e, f], [g, h, 1.0]]); Mi = np.linalg.inv(M); p = Mi @ np.array([u, v, 1.0]); return p[0] / p[2], p[1] / p[2]


class Plano:
    """raster plano (lon/lat -> pixel) + homografia para a tela 2x."""
    def __init__(self, lon0, lon1, lat0, lat1, ppd, quad):
        self.lon0, self.lon1, self.lat0, self.lat1, self.ppd = lon0, lon1, lat0, lat1, ppd
        self.W = int((lon1 - lon0) * ppd); self.H = int((lat1 - lat0) * ppd)
        self.quad = quad  # onde ficam TL,TR,BR,BL do raster na tela 2560x1440
        self.coef = homografia(quad, [(0, 0), (self.W, 0), (self.W, self.H), (0, self.H)])

    def px(self, lon, lat): return ((lon - self.lon0) * self.ppd, (self.lat1 - lat) * self.ppd)
    def tela(self, lon, lat, alt=0.0):
        x, y = self.px(lon, lat); X, Y = proj_pt(self.coef, x, y); return X, Y - alt
    def warp(self, im): return im.transform((2560, 1440), Image.PERSPECTIVE, tuple(self.coef), Image.BICUBIC, fillcolor=NAVY)


def aneis(feature, wrap360=False):
    g = feature["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    out = []
    for p in polys:
        ring = p[0]
        if wrap360: ring = [[(x + 360 if x < 0 else x), y] for x, y in ring]
        out.append(ring)
    return out


def desenha_terra(pl, im, feats, cores, wrap360=False, contorno=None):
    d = ImageDraw.Draw(im)
    for f in feats:
        cor = cores(f)
        for ring in aneis(f, wrap360):
            xs = [x for x, _ in ring]
            if max(xs) - min(xs) > 180: continue
            pts = [pl.px(x, y) for x, y in ring]
            d.polygon(pts, fill=cor, outline=contorno)


def fundo_navy(W, H):
    a = np.linspace(0, 1, H)[:, None, None]
    c0 = np.array(NAVY, float); c1 = np.array(NAVY2, float)
    arr = (c0 * (1 - a) + c1 * a) * np.ones((1, W, 1)); return Image.fromarray(arr.astype("uint8"))


def vinheta(im, forca=0.35):
    W, H = im.size; y, x = np.ogrid[:H, :W]; r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    k = 1 - forca * np.clip(r - 0.6, 0, 1) ** 1.5
    return Image.fromarray((np.asarray(im).astype(float) * k[..., None]).clip(0, 255).astype("uint8"))


def seta(d, pts, larg, cor, cabeca=True, borda=(25, 20, 10)):
    for off, c in ((6, borda), (0, cor)):
        d.line([(x + off * 0.4, y + off * 0.5) for x, y in pts], fill=c, width=larg + (8 if c == borda else 0), joint="curve")
    if cabeca:
        (x0, y0), (x1, y1) = pts[-2], pts[-1]; a = math.atan2(y1 - y0, x1 - x0); s = larg * 2.2
        tri = [(x1 + math.cos(a) * s * 0.9, y1 + math.sin(a) * s * 0.9),
               (x1 + math.cos(a + 2.5) * s, y1 + math.sin(a + 2.5) * s), (x1 + math.cos(a - 2.5) * s, y1 + math.sin(a - 2.5) * s)]
        d.polygon([(x + 5, y + 6) for x, y in tri], fill=borda); d.polygon(tri, fill=cor, outline=borda)


def bezier(p0, p1, p2, n=40): return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]


def texto(im, xy, partes, fonte, anchor="ls", stroke=8, gap=0):
    """partes = [(texto, cor), ...] na mesma linha."""
    d = ImageDraw.Draw(im); x, y = xy
    for s, cor in partes:
        d.text((x + 7, y + 8), s, font=fonte, fill=(0, 0, 0), stroke_width=stroke, stroke_fill=(0, 0, 0), anchor=anchor)
        d.text((x, y), s, font=fonte, fill=cor, stroke_width=stroke, stroke_fill=(10, 14, 28), anchor=anchor)
        x += d.textlength(s, font=fonte) + gap
    return x


# ------------------------------------------------------------------ El Niño
def nino():
    ne = json.load(open(f"{L2}/dados/ne110.json"))["features"]
    sst = json.load(open(f"{L2}/shared/sst_pacifico.json")); g = np.array([[np.nan if v is None else v for v in row] for row in sst["grades"][-1]], float)
    lon0, lon1, lat0, lat1, ppd = 160, 335, -42, 34, 20
    quad = [(60, 300), (2560, 250), (2760, 1560), (-700, 1700)]
    pl = Plano(lon0, lon1, lat0, lat1, ppd, quad)
    im = Image.new("RGB", (pl.W, pl.H), NAVY)
    brasil = lambda f: CORAL if f["properties"].get("ADMIN") == "Brazil" else (44, 58, 92)
    desenha_terra(pl, im, ne, brasil, wrap360=True, contorno=(70, 86, 128))
    # língua quente: anomalia >= 2 °C (grade 1°, lon 100..290, lat -30..30) -> bilinear -> cor
    nx, ny = g.shape[1], g.shape[0]; lons = sst["lon0"] + np.arange(nx); lats = sst["lat0"] + np.arange(ny)
    a = np.nan_to_num(g, nan=-9); big = np.array(Image.fromarray(a.astype("float32")).resize((nx * 8, ny * 8), Image.BILINEAR))
    # grade de pixels do raster
    xs = lon0 + (np.arange(pl.W) + 0.5) / ppd; ys = lat1 - (np.arange(pl.H) + 0.5) / ppd
    ix = ((xs - lons[0]) / (nx - 1) * (nx * 8 - 1)); iy = ((ys - lats[0]) / (ny - 1) * (ny * 8 - 1))
    okx = (ix >= 0) & (ix <= nx * 8 - 1); oky = (iy >= 0) & (iy <= ny * 8 - 1)
    val = np.full((pl.H, pl.W), -9.0, float)
    val[np.ix_(oky, okx)] = big[np.ix_(iy[oky].astype(int), ix[okx].astype(int))]
    t = np.clip((val - 2.0) / 3.0, 0, 1)
    c0 = np.array([255, 160, 40], float); c1 = np.array([226, 40, 40], float); c2 = np.array([150, 15, 40], float)
    col = np.where(t[..., None] < 0.5, c0 + (c1 - c0) * (t[..., None] * 2), c1 + (c2 - c1) * ((t[..., None] - 0.5) * 2))
    alpha = np.clip((val - 1.85) / 0.35, 0, 1)
    land = np.asarray(im).astype(float)
    # só no oceano: não pinta onde a terra (cor != navy) já está
    ocean = (np.abs(land - np.array(NAVY)).sum(-1) < 60)
    alpha = alpha * ocean
    im = Image.fromarray((land * (1 - alpha[..., None]) + col * alpha[..., None]).astype("uint8"))
    fade = np.ones((pl.H, 1, 1)); n = int(pl.H * 0.16); fade[:n, 0, 0] = np.linspace(0, 1, n) ** 1.3
    im = Image.fromarray((np.asarray(im).astype(float) * fade + np.array(NAVY, float) * (1 - fade)).astype("uint8"))
    tela = pl.warp(im).filter(ImageFilter.GaussianBlur(0.6))
    d = ImageDraw.Draw(tela)
    # termômetro cravado no Niño 3.4 (centro ~ 190–240 E, equador)
    bx, by = pl.tela(215, 0.0)
    H_T, W_T = 600, 104
    top = by - H_T
    d.ellipse((bx - 70, by - 18, bx + 70, by + 26), fill=(10, 14, 30))                    # sombra / tachinha
    d.rounded_rectangle((bx - W_T / 2 + 8, top + 8, bx + W_T / 2 + 8, by - 20 + 8), radius=39, fill=(0, 0, 0))
    d.rounded_rectangle((bx - W_T / 2, top, bx + W_T / 2, by - 20), radius=39, fill=(250, 250, 250), outline=(20, 20, 30), width=7)
    d.rounded_rectangle((bx - 15, top + 70, bx + 15, by - 40), radius=15, fill=(214, 28, 40))   # mercúrio
    d.ellipse((bx - 62, by - 100, bx + 62, by + 24), fill=(214, 28, 40), outline=(20, 20, 30), width=7)   # bulbo grosso
    d.ellipse((bx - 36, by - 78, bx - 8, by - 50), fill=(255, 150, 150))
    for k in range(1, 6):   # marcas
        yy = top + 80 + k * 70; d.line((bx + 20, yy, bx + 36, yy), fill=(60, 60, 80), width=5)
    # seta amarela grossa até o Brasil (arco sobre o mapa)
    bz = pl.tela(308, -14)
    p0 = (bx + 70, by - 300); p2 = (bz[0] - 130, bz[1] - 50); p1 = ((p0[0] + p2[0]) / 2, min(p0[1], p2[1]) - 260)
    seta(d, bezier(p0, p1, p2), 44, YEL)
    im = tela.resize((1280, 720), Image.LANCZOS)
    im = vinheta(im, 0.3)
    base = f"{OUT}/nino-base.jpg"; im.save(base, quality=92)
    # texto: terço inferior esquerdo, sobre o navy
    f = anton(190); x = texto(im, (46, 690), [("SÓ ", (255, 255, 255))], f, stroke=9)
    texto(im, (x, 690), [("2", YEL)], f, stroke=9)
    f2 = anton(150); texto(im, (x + ImageDraw.Draw(im).textlength("2", font=f) + 22, 690), [("°C?", YEL)], f2, stroke=9)
    return im


# ------------------------------------------------------------------ Sul do Brasil
def sul():
    ne = json.load(open(f"{L2}/dados/ne110.json"))["features"]
    ufs = json.load(open(f"{L2}/dados/br-ufs.json"))["features"]
    geo = json.load(open(f"{L2}/shared/geo.json"))
    lon0, lon1, lat0, lat1, ppd = -84, -34, -45, 2, 30
    # câmera baixa vinda do sul/sudeste: borda sul (BL/BR) larga e perto; borda norte estreita e longe
    quad = [(700, 150), (2420, 190), (3250, 1470), (-760, 1500)]
    pl = Plano(lon0, lon1, lat0, lat1, ppd, quad)
    im = fundo_navy(pl.W, pl.H).convert("RGB")
    nome = lambda f: f["properties"].get("ADMIN")
    def terra(f):
        n = nome(f)
        if n == "Brazil": return (150, 128, 100)
        return (118, 104, 86)
    desenha_terra(pl, im, [f for f in ne if nome(f) in ("Brazil", "Argentina", "Chile", "Uruguay", "Paraguay", "Bolivia", "Peru", "Colombia", "Venezuela", "Ecuador", "Suriname", "Guyana", "Falkland Islands")], terra, contorno=(60, 48, 38))
    # Sul em coral (PR 41, SC 42, RS 43)
    sulf = [u for u in ufs if u["properties"]["codarea"] in ("41", "42", "43")]
    d0 = ImageDraw.Draw(im)
    for u in sulf:
        for ring in aneis(u): d0.polygon([pl.px(x, y) for x, y in ring], fill=CORAL, outline=(120, 30, 40))
    tela = pl.warp(im); tela = Image.fromarray(np.asarray(tela))
    d = ImageDraw.Draw(tela)
    # Andes: crista (lon,lat) convertida da geo.json (x/(cos*k), lat0 - y/k), restrita a lat -43..-4
    k, cos, la0, lo0 = geo["proj"]["k"], geo["proj"]["cos"], geo["proj"]["lat0"], geo["proj"]["lon0"]
    cr = [(lo0 + x / (cos * k), la0 - y / k, h) for x, y, h in geo["andes"]]
    cr = [c for c in cr if -43 <= c[1] <= -6]
    # interpola
    pts = []
    for (a, b) in zip(cr[:-1], cr[1:]):
        for i in range(40):
            t = i / 40; pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t))
    pts.append(cr[-1])
    pts.sort(key=lambda p: p[1])   # sul -> norte: o do sul é o mais perto
    def ruido(lat): return 0.5 + 0.5 * (0.6 * math.sin(lat * 0.55) + 0.3 * math.sin(lat * 1.35 + 1) + 0.1 * math.sin(lat * 3.1 + 2))
    def altura(h, lat=0): return 215 * h * (0.78 + 0.45 * ruido(lat))
    # parede: quadriláteros do pé (terra) à crista (altura), face leste; do norte (longe) para o sul (perto)
    for (a, b) in reversed(list(zip(pts[:-1], pts[1:]))):
        pa = pl.tela(a[0], a[1]); pb = pl.tela(b[0], b[1])
        # largura de base do maciço: 3° para leste
        pa2 = pl.tela(a[0] + 2.2, a[1]); pb2 = pl.tela(b[0] + 2.2, b[1])
        ha, hb = altura(a[2], a[1]), altura(b[2], b[1]); ta = (pa[0], pa[1] - ha); tb = (pb[0], pb[1] - hb)
        ca, cb = 0.2 + 0.1 * ruido(a[1] * 1.5), 0.2 + 0.1 * ruido(b[1] * 1.5)
        d.polygon([pa2, pb2, pb, pa], fill=(104, 78, 54))                                   # encosta leste
        d.polygon([pa, pb, tb, ta], fill=(78, 56, 40))                                     # parede
        d.polygon([ta, tb, (tb[0], tb[1] + hb * (ca + 0.1)), (ta[0], ta[1] + ha * (ca + 0.1))], fill=(244, 244, 250))   # cume branco largo
        d.line([ta, tb], fill=(255, 255, 255), width=5)
        d.polygon([pa, pb, (pb[0] - 30, pb[1]), (pa[0] - 30, pa[1])], fill=(34, 24, 18))    # sombra a oeste
    # fita ciano colada à encosta: da Amazônia (entra por cima) desce pelo pé da encosta e acerta o Sul
    rota = [(-66, 0), (-69.5, -8), (-68.0, -15), (-64.5, -21), (-61.5, -26), (-57.5, -28.5), (-53.5, -29.0)]
    fita = []
    for (a, b) in zip(rota[:-1], rota[1:]):
        for i in range(10):
            t = i / 10; fita.append(pl.tela(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, 22))
    fita.append(pl.tela(*rota[-1], 22))
    fita = [(fita[0][0], -40)] + fita if False else fita
    glow = Image.new("RGBA", tela.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.line(fita, fill=(0, 230, 255, 170), width=130, joint="curve"); glow = glow.filter(ImageFilter.GaussianBlur(26))
    tela = Image.alpha_composite(tela.convert("RGBA"), glow); d = ImageDraw.Draw(tela)
    d.line(fita, fill=(5, 70, 90), width=116, joint="curve"); d.line(fita, fill=(40, 225, 250), width=100, joint="curve"); d.line(fita, fill=(190, 255, 255), width=34, joint="curve")
    # entrada pela borda de cima
    topo = fita[0]
    dx, dy = fita[0][0] - fita[12][0], fita[0][1] - fita[12][1]; n = math.hypot(dx, dy); k2 = (topo[1] + 80) / max(-dy / n, 0.2) / 1.0
    ext = (topo[0] + dx / n * k2, topo[1] + dy / n * k2); d.line([ext, topo], fill=(40, 225, 250), width=100); d.line([ext, topo], fill=(190, 255, 255), width=34)
    tela = tela.convert("RGB").resize((1280, 720), Image.LANCZOS)
    tela = vinheta(tela, 0.3)
    tela.save(f"{OUT}/sul-base.jpg", quality=92)
    f = anton(138)
    texto(tela, (1250, 590), [("CULPA DOS", (255, 255, 255))], f, anchor="rs", stroke=9)
    texto(tela, (1250, 705), [("ANDES?", YEL)], f, anchor="rs", stroke=9)
    return tela


if __name__ == "__main__":
    for k in (sys.argv[1:] or ["nino", "sul"]):
        im = {"nino": nino, "sul": sul}[k]()
        p = f"{OUT}/{k}-thumb.jpg"; im.save(p, quality=90, optimize=True); print(p, os.path.getsize(p) // 1024, "KB")
