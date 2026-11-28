"""Thumbs E1 rodada 3 (28/11/2026): A = bloco oblíquo da costa do Peru/Andes com a água em brasa; B = escala sem texto grande; C = globo único 2026 com contorno tracejado de 2015."""
import os, sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import globo, contorno, texto
from gera_thumbs import cm_brasa, salva, BASE, D, W, H, AMARELO, BRANCO, TINTA, e1_b2
globo.cmap_quente = cm_brasa
Image.MAX_IMAGE_PIXELS = None

def bil(M, fi, fj):
    i0 = np.clip(np.floor(fi).astype(int), 0, M.shape[0] - 2); j0 = np.floor(fj).astype(int) % M.shape[1]; j1 = (j0 + 1) % M.shape[1]
    ti = np.clip(fi - i0, 0, 1); tj = fj - np.floor(fj)
    return M[i0, j0] * (1 - ti) * (1 - tj) + M[i0 + 1, j0] * ti * (1 - tj) + M[i0, j1] * (1 - ti) * tj + M[i0 + 1, j1] * ti * tj

def e1_a3():
    lon0, lon1, lat0, lat1, ppd = -105.0, -34.0, -32.0, 8.0, 40
    w, h = int((lon1 - lon0) * ppd), int((lat1 - lat0) * ppd)
    lo = lon0 + (np.arange(w) + 0.5) / ppd; la = lat1 - (np.arange(h) + 0.5) / ppd
    LO, LA = np.meshgrid(lo, la)
    sr = np.asarray(Image.open(f"{D}/BlueMarble_ShadedRelief_Bathymetry.jpg").convert("RGB"), np.float32) / 255
    ng = np.asarray(Image.open(f"{D}/BlueMarble_NextGeneration.jpg").convert("RGB"), np.float32) / 255
    th, tw, _ = sr.shape
    u = ((LO + 180) / 360 * tw).astype(int) % tw; v = ((90 - LA) / 180 * th).astype(int)
    A = np.load(f"{D}/anom_f.npy"); OC = np.load(f"{D}/oceano.npy")
    fi = (LA + 89.875) / 0.5; fj = ((LO % 360) - 0.125) / 0.5
    a = bil(A, fi, fj); oce = np.clip((bil(OC, fi, fj) - 0.35) / 0.4, 0, 1)[..., None]
    terra = 0.55 * sr[v, u] + 0.45 * ng[v, u]; g = terra.mean(-1, keepdims=True); terra = np.clip((g + (terra - g) * 1.35) * 1.25, 0, 1)
    mar = np.ones_like(terra) * np.array([40, 120, 200]) / 255 * (0.85 + 0.3 * sr[v, u].mean(-1, keepdims=True))
    img = terra * (1 - oce) + mar * oce
    rgb, al = cm_brasa(a); al = (al * oce[..., 0])[..., None]
    img = img * (1 - al) + rgb * al
    flat = Image.fromarray((img * 255).astype(np.uint8)).convert("RGBA")
    # Brasil contornado no raster plano
    d = ImageDraw.Draw(flat)
    for r in contorno.pais("Brazil"):
        pts = [((x - lon0) * ppd, (lat1 - y) * ppd) for x, y in r]; d.line(pts + [pts[0]], fill=(255, 255, 255, 255), width=10, joint="curve")
    # câmera oblíqua: raster vira chão inclinado; horizonte no alto
    quad = [(-520, -40), (W + 520, -40), (W + 40, H + 30), (-40, H + 30)]  # TL,TR,BR,BL na tela
    coef = globo_hom(quad, [(0, 0), (w, 0), (w, h), (0, h)])
    chao = flat.transform((W, H), Image.PERSPECTIVE, tuple(coef), Image.BICUBIC, fillcolor=(0, 0, 0, 0))
    ceu = np.linspace(0, 1, H)[:, None, None] * np.ones((1, W, 1)); ceu = (np.array([150, 200, 245]) * (1 - ceu) + np.array([230, 242, 252]) * ceu)
    im = Image.fromarray(ceu.astype(np.uint8)).convert("RGBA")
    # névoa de horizonte
    hz = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dh = ImageDraw.Draw(hz)
    im.alpha_composite(chao)
    for k in range(120):
        dh.line([(0, k), (W, k)], fill=(225, 238, 252, int(120 * (1 - k / 120))))
    im.alpha_composite(hz)
    texto.palavra(im, "ENCOSTOU", (W - 60, 1040), tam=290, cor=AMARELO, ancora="rs", esp=18)
    salva(im, "e1-A-costa-encostou")

def globo_hom(dst, src):
    Am = []; B = []
    for (x, y), (u, v) in zip(dst, src):
        Am.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u); Am.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return np.linalg.solve(np.array(Am, float), np.array(B, float))

def e1_c3():
    cam = dict(lon0=-118.0, lat0=-2.0, raio=0.95, cx=0.50, cy=0.62)
    im, (latd, lond, dentro, R) = globo.render_globo(W=W, H=H, **{**BASE, "oceano_claro": 0.75}, **cam, fundo=(226, 238, 252), atm=(160, 205, 255))
    im = im.convert("RGBA")
    A15 = np.load(f"{D}/anom2015_f.npy"); OC = np.load(f"{D}/oceano.npy")
    fi = (latd + 89.875) / 0.5; fj = ((lond % 360) - 0.125) / 0.5
    m = (bil(A15, fi, fj) >= 2.0) & (bil(OC, fi, fj) > 0.5) & dentro & (np.abs(latd) < 20)
    mi = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)).point(lambda p: 255 if p > 128 else 0)
    ed = np.asarray(mi.filter(ImageFilter.FIND_EDGES)) > 0
    yy, xx = np.nonzero(ed)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for y, x in zip(yy, xx):
        if ((x // 14) + (y // 14)) % 2 == 0: d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 255, 255, 255))
    sh = lay.filter(ImageFilter.GaussianBlur(3)); im.alpha_composite(Image.eval(sh, lambda p: p)); im.alpha_composite(lay)
    contorno.desenha(im, contorno.pais("Brazil"), cam, larg=6)
    # etiqueta pequena "2015" junto do tracejado
    texto.etiqueta(im, "2015", (int(np.median(xx[yy < np.percentile(yy, 15)])) if len(xx) else 600, int(np.percentile(yy, 5)) - 50), tam=64, fundo=(255, 255, 255), cor=(30, 40, 60))
    salva(im, "e1-C-globo-2026-contorno-2015")

if __name__ == "__main__":
    for q in sys.argv[1:] or ["e1_a3", "e1_c3"]: globals()[q]()
