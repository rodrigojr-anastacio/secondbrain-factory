"""Reembalagem 14/11/2026: compõe as thumbs novas (texto, pílulas, sello e aba no código; bases sem texto).
Uso (da raiz do repo): tools/.venv/bin/python pesquisa/reembalagem-2026-11-14/thumbs/compose.py [slug ...]
Saída: <pasta do vídeo>/reembalagem-2026-11-14/thumb-nova.jpg (1280x720). Fontes de historia-ptbr em 003-ira/.../fonts."""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

R = os.path.expanduser("~/workspace/fabrica-youtube")
V = f"{R}/canais/historia-ptbr/videos"
DV = f"{R}/canais/dossie-es/videos"
FD = f"{V}/003-ira/v2-amostras/thumbs/base/fonts"
FD2 = f"{R}/pesquisa/reembalagem-2026-11-14/thumbs/fonts"
GOLD = (247, 194, 27); BLACK = (15, 12, 10); WHITE = (255, 255, 255)
PAPEL = (233, 223, 201); ROJO = (179, 38, 30); TINTA = (26, 26, 26); PASTA = (200, 164, 106)


def caslon(sz):
    f = ImageFont.truetype(f"{FD}/LibreCaslonText[wght].ttf", sz); f.set_variation_by_axes([700]); return f
def sans(sz):
    f = ImageFont.truetype(f"{FD}/OpenSans[wdth,wght].ttf", sz); f.set_variation_by_axes([800, 100]); return f
def bebas(sz): return ImageFont.truetype(f"{FD2}/BebasNeue-Regular.ttf", sz)
def elite(sz): return ImageFont.truetype(f"{FD2}/SpecialElite-Regular.ttf", sz)
def anton(sz): return ImageFont.truetype(f"{R}/pesquisa/canal-clima-2026-11/identidade/fontes/Anton-Regular.ttf", sz)


def fit(im):
    w = 1280; h = int(im.height * w / im.width); im = im.resize((w, h), Image.LANCZOS)
    if h < 720:
        w2 = int(im.width * 720 / im.height); im = im.resize((w2, 720), Image.LANCZOS)
    x = (im.width - 1280) // 2; y = (im.height - 720) // 2
    return im.crop((x, y, x + 1280, y + 720))


def grad(im, bottom=0, top=0, a=200):
    ov = Image.new("L", im.size, 0); d = ImageDraw.Draw(ov); W, H = im.size
    for i in range(bottom): d.line([(0, H - 1 - i), (W, H - 1 - i)], fill=int(a * (1 - i / bottom)))
    for i in range(top): d.line([(0, i), (W, i)], fill=int(a * (1 - i / top)))
    return Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ov)


def text(im, xy, s, font, fill, stroke=10, anchor="la", shadow=10):
    d = ImageDraw.Draw(im)
    d.text((xy[0] + shadow, xy[1] + shadow), s, font=font, fill=BLACK, stroke_width=stroke, stroke_fill=BLACK, anchor=anchor)
    d.text(xy, s, font=font, fill=fill, stroke_width=stroke, stroke_fill=BLACK, anchor=anchor)


def two(im, y, a, b, font, ca=GOLD, cb=WHITE, cx=None, x=None, anchor="ls", stroke=10):
    """duas cores na mesma linha (a + b); centrado em cx ou começando em x."""
    d = ImageDraw.Draw(im); wa = d.textlength(a, font=font); wb = d.textlength(b, font=font)
    x0 = x if x is not None else cx - (wa + wb) / 2
    text(im, (x0, y), a, font, ca, anchor="ls", stroke=stroke); text(im, (x0 + wa, y), b, font, cb, anchor="ls", stroke=stroke)
    return x0, wa + wb


def pill(im, cx, cy, s, font):
    d = ImageDraw.Draw(im); b = d.textbbox((cx, cy), s, font=font, anchor="mm"); r = (b[0] - 26, b[1] - 14, b[2] + 26, b[3] + 14)
    d.rounded_rectangle((r[0] + 7, r[1] + 7, r[2] + 7, r[3] + 7), radius=16, fill=BLACK)
    d.rounded_rectangle(r, radius=16, fill=GOLD, outline=BLACK, width=6); d.text((cx, cy), s, font=font, fill=BLACK, anchor="mm")


def fitfont(d, s, maxw, hi, lo, fn):
    for sz in range(hi, lo, -2):
        if d.textlength(s, font=fn(sz)) <= maxw: return fn(sz)
    return fn(lo)


def feather(im, x, w=70, cor=PAPEL):
    """suaviza uma emenda vertical (fim da ilustração e começo do papel liso) em x."""
    ov = Image.new("L", im.size, 0); d = ImageDraw.Draw(ov)
    for i in range(w): d.line([(x - w + i, 0), (x - w + i, im.height)], fill=int(255 * (i / w) ** 1.6))
    d.rectangle((x, 0, im.width, im.height), fill=255)
    return Image.composite(Image.new("RGB", im.size, cor), im, ov)


def sello(im, cx, cy, s, size, ang=-7, fundo=(233, 223, 201, 235)):
    f = bebas(size); d0 = ImageDraw.Draw(im); w = int(d0.textlength(s, font=f)) + 70; h = int(size * 1.0) + 40
    L = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((14, 14, w + 26, h + 26), fill=fundo, outline=ROJO, width=9)
    d.rectangle((26, 26, w + 14, h + 14), outline=ROJO, width=3)
    d.text(((w + 40) / 2, (h + 40) / 2 + 3), s, font=f, fill=ROJO, anchor="mm")
    L = L.rotate(ang, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", L.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 90), mask=L.split()[3])
    im.paste(sh, (int(cx - L.width / 2 + 6), int(cy - L.height / 2 + 7)), sh)
    im.paste(L, (int(cx - L.width / 2), int(cy - L.height / 2)), L)


def aba(im, n):
    d = ImageDraw.Draw(im); f = elite(34); s = f"EXPEDIENTE Nº {n:03d}"; w = int(d.textlength(s, font=f)) + 56
    x1 = 1280 - 34; x0 = x1 - w
    d.rounded_rectangle((x0 + 5, -20 + 6, x1 + 5, 66 + 6), radius=14, fill=(0, 0, 0))
    d.rounded_rectangle((x0, -20, x1, 66), radius=14, fill=PASTA, outline=(156, 122, 67), width=3)
    d.text(((x0 + x1) / 2, 28), s, font=f, fill=TINTA, anchor="mm")


def dossie(base, sigla, n, selo_txt, selo_xy, selo_sz, out, cx=985, seam=None, sigla_y=330, ang=-7, maxw=560, hi=420):
    im = fit(Image.open(base).convert("RGB"))
    if seam: im = feather(im, seam[0], seam[1])
    d = ImageDraw.Draw(im); ls = sigla.split("\n"); f = fitfont(d, max(ls, key=len), maxw, hi if len(ls) == 1 else 260, 120, bebas)
    for i, l in enumerate(ls):
        d.text((cx, sigla_y + (i - (len(ls) - 1) / 2) * f.size * 0.95), l, font=f, fill=TINTA, anchor="mm")
    sello(im, selo_xy[0], selo_xy[1], selo_txt, selo_sz, ang=ang)
    aba(im, n)
    return im


def salvar(im, pasta, nome="thumb-nova.jpg"):
    os.makedirs(f"{pasta}/reembalagem-2026-11-14", exist_ok=True)
    p = f"{pasta}/reembalagem-2026-11-14/{nome}"
    q = 90
    while True:
        im.save(p, quality=q, optimize=True)
        if os.path.getsize(p) < 900 * 1024 or q < 60: break
        q -= 5
    print(p, im.size, os.path.getsize(p) // 1024, "KB")
    return p


# ---------------- historia-ptbr ----------------
def egito():
    im = fit(Image.open(f"{V}/001-egito/reembalagem-2026-11-14/base/e1.jpg").convert("RGB"))
    im = grad(im, bottom=300, a=215); d = ImageDraw.Draw(im)
    f = fitfont(d, "JÁ ERA ANTIGA", 740, 150, 60, caslon)
    two(im, 690, "JÁ ERA ", "ANTIGA", f, x=40)
    pill(im, 640, 56, "2560 a.C. · 30 a.C.", sans(40))
    return im, f"{V}/001-egito"


def india():
    im = fit(Image.open(f"{V}/002-india/reembalagem-2026-11-14/base/i2.jpg").convert("RGB"))
    im = grad(im, bottom=250, a=215); d = ImageDraw.Draw(im)
    f = caslon(124); wa = d.textlength("CHUVA", font=f); wm = d.textlength(" × ", font=f); wb = d.textlength("CANHÃO", font=f)
    x = 640 - (wa + wm + wb) / 2
    text(im, (x, 700), "CHUVA", f, GOLD, anchor="ls"); text(im, (x + wa, 700), " × ", f, WHITE, anchor="ls"); text(im, (x + wa + wm, 700), "CANHÃO", f, WHITE, anchor="ls")
    pill(im, 640, 62, "1757", sans(54))
    return im, f"{V}/002-india"


def ira():
    im = fit(Image.open(f"{V}/003-ira/v2-amostras/thumbs/base/c1-persia-ira-a.png").convert("RGB")); im = grad(im, bottom=300, a=215)
    f = caslon(132); two(im, 692, "MESMO ", "PAÍS?", f, cx=640)
    pill(im, 640, 62, "2.500 ANOS", sans(50))
    return im, f"{V}/003-ira"


def china():
    return Image.open(f"{V}/004-china/entrega/thumbs-v2/thumb-4-bonecos.jpg").convert("RGB"), f"{V}/004-china"


def brasil():
    def prep(p, s, cx_src, cx_dst):
        im = Image.open(p).convert("RGB"); w = int(1280 * s); h = int(im.height * w / im.width)
        im = im.resize((w, h), Image.LANCZOS); x0 = int(cx_src * w - cx_dst)
        c = Image.new("RGB", (1280, 720), (0, 0, 0)); c.paste(im, (-x0, (720 - h) // 2)); return c
    b = f"{V}/005-brasil/reembalagem-2026-11-14/base"
    L = prep(f"{b}/b1511a.jpg", 1.2, 0.66, 330); Rr = prep(f"{b}/b2026a.jpg", 1.2, 0.34, 950)
    mask = Image.new("L", (1280, 720), 0); ImageDraw.Draw(mask).polygon([(0, 0), (800, 0), (560, 720), (0, 720)], fill=255)
    im = Image.composite(L, Rr, mask); d = ImageDraw.Draw(im)
    d.line([(800, 0), (560, 720)], fill=BLACK, width=26); d.line([(800, 0), (560, 720)], fill=(255, 224, 40), width=14)
    im = grad(im, bottom=250, a=215); d = ImageDraw.Draw(im)
    f = caslon(128); two(im, 700, "NADA ", "MUDOU?", f, cx=640)
    pill(im, 640, 62, "1511 · 2026", sans(52))
    return im, f"{V}/005-brasil"


def roma():
    im = fit(Image.open(f"{V}/006-roma/reembalagem-2026-11-14/base/r1.jpg").convert("RGB"))
    ov = Image.new("L", im.size, 0); d = ImageDraw.Draw(ov)
    for i in range(540): d.line([(1279 - i, 0), (1279 - i, 719)], fill=int(150 * (1 - i / 540)))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ov)
    fn = fitfont(ImageDraw.Draw(im), "NOVO?", 530, 190, 60, caslon)   # ≥ 20 px de respiro da mão (borda dir. ~650 px)
    text(im, (1250, 300), "DE", fn, GOLD, anchor="rs"); text(im, (1250, 300 + int(fn.size * 1.05)), "NOVO?", fn, WHITE, anchor="rs")
    pill(im, 1090, 620, "410", sans(60))
    return im, f"{V}/006-roma"


def russia():
    m = Image.open(f"{V}/007-russia/imagens/I017.jpg").convert("RGB"); r, g, b = m.split()
    mask = ImageChops.multiply(r.point(lambda v: 255 if v > 170 else 0), ImageChops.multiply(g.point(lambda v: 255 if v < 110 else 0), b.point(lambda v: 255 if v < 110 else 0)))
    mask = mask.filter(ImageFilter.MedianFilter(5))
    dark = Image.blend(m, Image.new("RGB", m.size, (12, 18, 38)), 0.78); red = Image.blend(m, Image.new("RGB", m.size, (150, 12, 18)), 0.35)
    comp = Image.composite(red, dark, mask)
    edge = mask.filter(ImageFilter.MaxFilter(11)); edge = ImageChops.subtract(edge, mask).filter(ImageFilter.GaussianBlur(2))
    comp = Image.composite(Image.new("RGB", m.size, GOLD), comp, edge)
    glow = mask.filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.GaussianBlur(18)); glow = ImageChops.subtract(glow, mask).point(lambda v: int(v * 0.6))
    comp = Image.composite(Image.new("RGB", m.size, (255, 170, 40)), comp, glow)
    im = fit(comp)
    text(im, (40, 160), "TUDO", caslon(150), GOLD, anchor="ls"); text(im, (40, 310), "ISSO?", caslon(150), WHITE, anchor="ls")
    return im, f"{V}/007-russia"


# ---------------- dossie-es ----------------
def cia():
    return dossie(f"{DV}/001-cia/reembalagem-2026-11-14/base/cia1.jpg", "CIA", 1, "FALSA", (400, 360), 84, None, ang=-9), f"{DV}/001-cia"
def mossad():
    return dossie(f"{DV}/002-mossad/reembalagem-2026-11-14/base/mossad1.jpg", "MOSSAD", 2, "FUGA", (400, 470), 90, None, seam=(795, 90), maxw=520, sigla_y=300), f"{DV}/002-mossad"
def fbi():
    im = dossie(f"{DV}/003-fbi/reembalagem-2026-11-14/base/fbi5.jpg", "FBI", 3, "¿QUIÉNES?", (270, 628), 84, None, seam=(850, 50))
    d = ImageDraw.Draw(im); d.text((270, 250), "FBI", font=bebas(230), fill=(18, 18, 18), anchor="mm")   # "FBI" pintado no vidro
    return im, f"{DV}/003-fbi"
def cosa():
    return dossie(f"{DV}/004-cosa-nostra/reembalagem-2026-11-14/base/cosa2.jpg", "COSA\nNOSTRA", 4, "TRAIDOR", (445, 500), 90, None, maxw=560), f"{DV}/004-cosa-nostra"
def kgb():
    return dossie(f"{DV}/005-kgb/reembalagem-2026-11-14/base/kgb2.jpg", "KGB", 5, "SIN CULPABLE", (260, 610), 80, None), f"{DV}/005-kgb"
def masones():
    return dossie(f"{DV}/006-masones/reembalagem-2026-11-14/base/masones2.jpg", "MASONES", 6, "RITUALES", (430, 455), 90, None, seam=(1000, 60), maxw=520, sigla_y=300), f"{DV}/006-masones"


T = dict(egito=egito, india=india, ira=ira, china=china, brasil=brasil, roma=roma, russia=russia,
         cia=cia, mossad=mossad, fbi=fbi, cosa=cosa, kgb=kgb, masones=masones)
if __name__ == "__main__":
    for k in (sys.argv[1:] or T):
        r = T[k]()
        im, pasta = r
        if isinstance(im, tuple): im = im[0]
        salvar(im, pasta)
