"""Thumbs cine D/E/F do 013 Núremberg (21/11/2026): estilo pôster de cinema (refs do Rodrigo em refs/), base fotorrealista
(google/nano-banana-2.1 via gerar_bases.py), título "NÚREMBERG" em Cinzel (OFL) espaçada, creme/dourado, SEMPRE no código.
Uso (da raiz do repo): tools/.venv/bin/python canais/dossie-es/videos/013-nuremberg/thumbs-extra/compose.py"""
import os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageStat

R = os.path.expanduser("~/workspace/fabrica-youtube")
V = f"{R}/canais/dossie-es/videos/013-nuremberg"
X = f"{V}/thumbs-extra"
FD = f"{R}/pesquisa/reembalagem-2026-11-14/thumbs/fonts"
OURO_A, OURO_B = (240, 224, 186), (196, 162, 98)   # creme → dourado (degradê vertical)
TITULO = "NÚREMBERG"


def cinzel(sz, peso="Bold"):
    f = ImageFont.truetype(f"{FD}/Cinzel.ttf", sz)
    try: f.set_variation_by_name(peso)
    except Exception: pass
    return f


def fit(p, corte_lat=0.0, dx=0, dy=0, zoom=1.0):
    im = Image.open(p).convert("RGB")
    if corte_lat:
        c = int(im.width * corte_lat); im = im.crop((c, 0, im.width - c, im.height))
    esc = max(1280 / im.width, 720 / im.height) * zoom
    im = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
    x = (im.width - 1280) // 2 + dx; y = (im.height - 720) // 2 + dy
    return im.crop((x, y, x + 1280, y + 720))


def grade(im, sat=0.85, contraste=1.06):
    im = ImageEnhance.Color(im).enhance(sat); im = ImageEnhance.Contrast(im).enhance(contraste)
    return im


def grao(im, forca=10, seed=13):
    random.seed(seed)
    n = Image.effect_noise((1280, 720), 40).convert("L").point(lambda v: 128 + (v - 128) * forca // 40)
    return Image.blend(im, Image.merge("RGB", (n, n, n)), 0.0).__class__.composite(im, im, n) if False else \
        Image.eval(Image.blend(im, Image.merge("RGB", (n, n, n)), 0.06), lambda v: v)


def vinheta(im, forca=0.55, cx=0.5, cy=0.5):
    m = Image.new("L", (1280, 720), 0); d = ImageDraw.Draw(m)
    d.ellipse((int(1280 * cx) - 900, int(720 * cy) - 560, int(1280 * cx) + 900, int(720 * cy) + 560), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(160))
    escuro = ImageEnhance.Brightness(im).enhance(1 - forca)
    return Image.composite(im, escuro, m)


def escurecer(im, caixa, forca=0.5, raio=120):
    """escurece uma região (fundo do título) com borda suave."""
    m = Image.new("L", (1280, 720), 0); ImageDraw.Draw(m).rectangle(caixa, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(raio))
    return Image.composite(ImageEnhance.Brightness(im).enhance(1 - forca), im, m)


def titulo(im, cx, cy, tam, espaco, texto=TITULO, peso="Bold", wmax=None):
    """texto espaçado letra a letra, degradê creme→dourado, sombra suave (sem contorno pesado); encolhe até caber em wmax."""
    d0 = ImageDraw.Draw(im)
    while True:
        f = cinzel(tam, peso)
        larg = [d0.textlength(c, font=f) for c in texto]; W = sum(larg) + espaco * (len(texto) - 1)
        if not wmax or W <= wmax: break
        tam -= 2; espaco = max(2, espaco * tam // (tam + 2))
    print("  título", texto, "tam", tam, "larg", int(W))
    asc, desc = f.getmetrics(); H = asc + desc + 40
    m = Image.new("L", (int(W) + 40, H), 0); d = ImageDraw.Draw(m); x = 20
    for c, w in zip(texto, larg):
        d.text((x, 20), c, font=f, fill=255); x += w + espaco
    ox, oy = int(cx - m.width / 2), int(cy - m.height / 2)
    sombra = m.filter(ImageFilter.GaussianBlur(10))
    preto = Image.new("RGB", m.size, (0, 0, 0))
    im.paste(preto, (ox + 3, oy + 5), sombra.point(lambda v: int(v * 0.85)))
    g = Image.new("RGB", m.size); dg = ImageDraw.Draw(g)
    for yy in range(m.height):
        t = min(1, max(0, (yy - 20) / max(1, asc)))
        dg.line((0, yy, m.width, yy), fill=tuple(int(a + (b - a) * t) for a, b in zip(OURO_A, OURO_B)))
    im.paste(g, (ox, oy), m)
    return W


def filete(im, cx, y, w, cor=OURO_B):
    d = ImageDraw.Draw(im); d.line((cx - w / 2, y, cx + w / 2, y), fill=cor, width=2)


def salvar(im, p):
    q = 93
    while True:
        im.save(p, quality=q, optimize=True)
        if os.path.getsize(p) < 1900 * 1024 or q < 60: break
        q -= 4
    print(p, im.size, os.path.getsize(p) // 1024, "KB")


def limpar_patch_E2():
    """r2/crivo: o PM saiu com bandeira francesa no ombro da farda americana; pinta o patch liso com a cor da manga."""
    im = Image.open(f"{X}/bases/E2.jpg").convert("RGB")
    cor = tuple(int(v) for v in ImageStat.Stat(im.crop((2565, 940, 2610, 990))).median)
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((2548, 882, 2606, 936), radius=10, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(4))
    lisa = Image.new("RGB", im.size, cor)
    lisa = Image.blend(lisa, im.filter(ImageFilter.GaussianBlur(14)), 0.35)
    im = Image.composite(lisa, im, m); im.save(f"{X}/bases/E2-fix.jpg", quality=95)


def clarear(im, caixa, forca=1.15, raio=60):
    m = Image.new("L", (1280, 720), 0); ImageDraw.Draw(m).ellipse(caixa, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(raio))
    return Image.composite(ImageEnhance.Brightness(im).enhance(forca), im, m)


def D():
    # r2: close de Göring à direita, túnica sem insígnias (como no julgamento), fones no pescoço; título à esquerda
    im = grade(fit(f"{X}/bases/D2.jpg", dx=10))
    im = escurecer(im, (0, 90, 760, 300), 0.4)
    im = vinheta(im, 0.4, cx=0.66)
    im = grao(im)
    titulo(im, 418, 190, 124, 4, peso="Black", wmax=770)
    salvar(im, f"{X}/thumb-D.jpg"); return im


def E():
    # r2 (composição própria): de dentro do banco dos réus, por trás de um réu com fones, rumo à bancada dos juízes
    limpar_patch_E2()
    im = grade(fit(f"{X}/bases/E2-fix.jpg"), sat=0.85)
    im = escurecer(im, (150, 0, 1130, 150), 0.5, raio=80)
    im = vinheta(im, 0.5, cy=0.6)
    im = grao(im)
    titulo(im, 700, 86, 128, 6, peso="Black", wmax=900)
    salvar(im, f"{X}/thumb-E.jpg"); return im


def F():
    # r2: banco dos réus, Göring de fones na frente (centro-direita), 2 réus atrás na sombra; título no alto
    im = grade(fit(f"{X}/bases/F2.jpg", zoom=1.18, dx=40, dy=50))
    im = escurecer(im, (100, 0, 1180, 190), 0.45, raio=90)
    im = vinheta(im, 0.4, cx=0.62, cy=0.62)
    im = clarear(im, (820, 170, 1100, 450), 1.15)
    im = grao(im)
    titulo(im, 600, 76, 128, 6, peso="Black", wmax=900)
    salvar(im, f"{X}/thumb-F.jpg"); return im


def prancha(ims, viz):
    """linha 1: as 3 atuais + D/E/F a 320x180; linha 2: idem a 160x90; linha 3: D/E/F no meio de thumbs do tema (160x90)."""
    from PIL import ImageFont as IF
    gap = 14; n = len(ims); W = n * 320 + (n + 1) * gap
    rot = cinzel(20, "Regular")
    H = gap + 180 + 30 + 90 + 30 + 20 + 2 * (90 + gap) + gap + 30
    P = Image.new("RGB", (W, H), (18, 18, 18)); d = ImageDraw.Draw(P)
    for i, (nome, im) in enumerate(ims):
        x = gap + i * (320 + gap)
        P.paste(im.resize((320, 180), Image.LANCZOS), (x, gap)); d.text((x + 160, gap + 195), nome, font=rot, fill=OURO_A, anchor="mm")
        P.paste(im.resize((160, 90), Image.LANCZOS), (x, gap + 210)); d.text((x + 240, gap + 255), "160×90", font=rot, fill=(140, 140, 140), anchor="mm")
    y0 = gap + 210 + 90 + 40
    d.text((gap, y0 - 14), "D/E/F (borda dourada) entre thumbs do tema e da grade do canal (embalagem/thumbs), 160x90", font=cinzel(16, "Regular"), fill=(170, 170, 170))
    grade_ = viz[:6] + [ims[-3][1]] + viz[6:9] + [ims[-2][1]] + viz[9:12] + [ims[-1][1]]
    cols = W // (160 + gap)
    for k, im in enumerate(grade_[:2 * cols]):
        r, c = divmod(k, cols); x = gap + c * (160 + gap); y = y0 + 10 + r * (90 + gap)
        P.paste(im.resize((160, 90), Image.LANCZOS), (x, y))
        if any(im is t[1] for t in ims[-3:]): d.rectangle((x - 3, y - 3, x + 162, y + 92), outline=OURO_B, width=3)
    P.save(f"{X}/prancha.jpg", quality=90); print(f"{X}/prancha.jpg", P.size)


def vizinhas():
    import glob
    fs = sorted(glob.glob(f"{V}/embalagem/thumbs/**/*.jpg", recursive=True) + glob.glob(f"{V}/embalagem/thumbs/**/*.webp", recursive=True))
    out = []
    for f in fs[:14]:
        try:
            im = Image.open(f).convert("RGB")
            if im.width / im.height < 1.6:  # hqdefault 4:3 com faixas pretas: recorta o 16:9 do meio
                h = int(im.width * 9 / 16); y = (im.height - h) // 2; im = im.crop((0, y, im.width, y + h))
            out.append(im)
        except Exception: pass
    return out


if __name__ == "__main__":
    d, e, f = D(), E(), F()
    abc = [(f"{k} (atual)", Image.open(f"{V}/out/thumb-{k}.jpg").convert("RGB")) for k in "ABC"]
    prancha(abc + [("D", d), ("E", e), ("F", f)], vizinhas())
