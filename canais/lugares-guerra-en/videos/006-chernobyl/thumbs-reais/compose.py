"""Thumbs reais A/B/C do 006 Chernobyl (21/11/2026, pedido do Rodrigo: "imagem real de Chernobyl, máscara de gás").
Base = FOTO REAL do Wikimedia Commons (fontes/, créditos em THUMBS-REAIS.md); texto SEMPRE no código (Anton, amarelo #FDD505).
Tratamento: dessaturação + contraste, grão, vinheta, acento amarelo-radiação.
Uso (da raiz do repo): tools/.venv/bin/python canais/lugares-guerra-en/videos/006-chernobyl/thumbs-reais/compose.py"""
import os, glob, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

R = os.path.expanduser("~/workspace/fabrica-youtube")
V = f"{R}/canais/lugares-guerra-en/videos/006-chernobyl"
X = f"{V}/thumbs-reais"
F = f"{X}/fontes"
ANTON = f"{R}/canais/lugares-guerra-en/identidade/fontes/Anton-Regular.ttf"
AMARELO = (253, 213, 5)
TINTA = (17, 20, 24)
W, H = 1280, 720


def fit(p, zoom=1.0, cx=0.5, cy=0.5):
    """recorta 16:9 centrado em (cx, cy) relativos da foto, com zoom."""
    im = Image.open(p).convert("RGB")
    esc = max(W / im.width, H / im.height) * zoom
    im = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
    x = min(max(0, int(im.width * cx - W / 2)), im.width - W)
    y = min(max(0, int(im.height * cy - H / 2)), im.height - H)
    return im.crop((x, y, x + W, y + H))


def grade(im, sat=0.55, contraste=1.25, brilho=0.95):
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Contrast(im).enhance(contraste)
    return ImageEnhance.Brightness(im).enhance(brilho)


def acento_amarelo(im, sat_base=0.25, limiar=40):
    """mantém só os tons amarelos/laranja saturados (gôndolas, filtro da máscara) e dessatura o resto."""
    hsv = im.convert("HSV"); h, s, v = hsv.split()
    # matiz amarelo-laranja: ~20°–60° → 14–43 na escala 0–255
    m = Image.eval(h, lambda x: 255 if 12 <= x <= 45 else 0)
    m = Image.composite(m, Image.new("L", im.size, 0), s.point(lambda x: 255 if x > limiar else 0))
    m = m.filter(ImageFilter.GaussianBlur(3))
    cinza = ImageEnhance.Color(im).enhance(sat_base)
    forte = ImageEnhance.Color(im).enhance(1.35)
    return Image.composite(forte, cinza, m)


def grao(im, forca=0.07, seed=7):
    random.seed(seed)
    n = Image.effect_noise((W, H), 48).convert("L")
    return Image.blend(im, Image.merge("RGB", (n, n, n)), forca)


def vinheta(im, forca=0.6, cx=0.5, cy=0.5, rx=820, ry=520):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse((W * cx - rx, H * cy - ry, W * cx + rx, H * cy + ry), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(170))
    return Image.composite(im, ImageEnhance.Brightness(im).enhance(1 - forca), m)


def escurecer(im, caixa, forca=0.55, raio=110):
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rectangle(caixa, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(raio))
    return Image.composite(ImageEnhance.Brightness(im).enhance(1 - forca), im, m)


def texto(im, linhas, x, y, tam, cor=AMARELO, alinhar="l", entre=0.92, contorno=0.07):
    """linhas empilhadas em Anton, contorno preto grosso + sombra; (x, y) = canto sup. esq. (ou dir. se alinhar='r')."""
    f = ImageFont.truetype(ANTON, tam)
    d0 = ImageDraw.Draw(im)
    sw = max(3, int(tam * contorno))
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(camada)
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sombra)
    yy = y; caixas = []
    for ln in linhas:
        tw = d0.textlength(ln, font=f)
        xx = x - tw if alinhar == "r" else (x - tw / 2 if alinhar == "c" else x)
        ds.text((xx + 8, yy + 10), ln, font=f, fill=(0, 0, 0, 200), stroke_width=sw, stroke_fill=(0, 0, 0, 200))
        d.text((xx, yy), ln, font=f, fill=cor, stroke_width=sw, stroke_fill=(0, 0, 0))
        caixas.append((xx, yy, xx + tw, yy + tam * 1.2))
        yy += int(tam * entre)
    sombra = sombra.filter(ImageFilter.GaussianBlur(9))
    im = Image.alpha_composite(im.convert("RGBA"), sombra)
    im = Image.alpha_composite(im, camada).convert("RGB")
    return im, caixas


def salvar(im, p):
    q = 94
    while True:
        im.save(p, quality=q, optimize=True)
        if os.path.getsize(p) < 1900 * 1024 or q < 60: break
        q -= 4
    print(p, im.size, os.path.getsize(p) // 1024, "KB")


def bandeira_suecia(im, x, y, w):
    """selo pequeno: bandeira da Suécia (azul + cruz amarela) com borda preta e leve inclinação."""
    h = int(w * 10 / 16)
    b = Image.new("RGB", (w, h), (0, 106, 167)); d = ImageDraw.Draw(b)
    t = max(4, h // 5); cxr = int(w * 5 / 16)
    d.rectangle((cxr, 0, cxr + t, h), fill=(254, 204, 2)); d.rectangle((0, h // 2 - t // 2, w, h // 2 + t // 2), fill=(254, 204, 2))
    b = ImageOps.expand(b, border=5, fill=(0, 0, 0)).convert("RGBA").rotate(-6, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", b.size, (0, 0, 0, 0)); sh.putalpha(b.split()[3].point(lambda a: a * 0.7))
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    im = im.convert("RGBA"); im.alpha_composite(sh, (x + 6, y + 8)); im.alpha_composite(b, (x, y))
    return im.convert("RGB")


def selo(im, x, y, tam=40, ang=-7):
    """selo "RESTRICTED" vermelho pequeno inclinado: a marca do canal (biblia/thumb.md §3)."""
    f = ImageFont.truetype(ANTON, tam); txt = "RESTRICTED"
    tw = int(ImageDraw.Draw(im).textlength(txt, font=f)); pad = tam // 3
    s_ = Image.new("RGBA", (tw + 2 * pad + 8, int(tam * 1.45) + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(s_)
    d.rectangle((4, 4, s_.width - 5, s_.height - 5), fill=(200, 24, 30, 235), outline=(255, 255, 255, 235), width=3)
    d.text((s_.width // 2, s_.height // 2), txt, font=f, fill=(255, 255, 255), anchor="mm")
    s_ = s_.rotate(ang, expand=True, resample=Image.BICUBIC)
    im = im.convert("RGBA"); im.alpha_composite(s_, (int(x), int(y))); return im.convert("RGB")


# ---------- A: máscara de gás pendurada na escola de Pripyat (close dominante) + "67 HOURS" ----------
def A():
    im = fit(f"{F}/a4.jpg", zoom=1.75, cx=0.50, cy=0.42)
    im = acento_amarelo(grade(im, sat=1.0, contraste=1.22, brilho=0.92), sat_base=0.22, limiar=45)
    im = escurecer(im, (0, 0, 430, 720), 0.65, raio=110)
    im = vinheta(im, 0.55, cx=0.68, cy=0.45)
    im = grao(im)
    im, _ = texto(im, ["67"], 40, 40, 330)
    im, _ = texto(im, ["HOURS"], 46, 420, 178)
    im = selo(im, 52, 18, 38)
    salvar(im, f"{X}/thumb-A.jpg"); return im


# ---------- B (r2 do crivo): dosímetro amarelo real diante da usina + "ON A SHOE" + selo da Suécia ----------
# r1 reprovou o reator cinza com guindaste (repetia a thumb mais vista do tema e tinha 2 focos). Herói agora = o detector
# (Terra-P em mão, zona de exclusão, usina ao fundo; Jennifer Boyer, CC BY 2.0): o objeto que mede radiação, como o
# detector de Forsmark que pegou o sapato emprestado.
def B():
    im = fit(f"{F}/d2.jpg", zoom=1.12, cx=0.62, cy=0.30)
    im = grade(im, sat=1.0, contraste=1.3, brilho=0.95)
    cor = acento_amarelo(im, sat_base=0.15, limiar=120)
    md = Image.new("L", (W, H), 0); ImageDraw.Draw(md).rounded_rectangle((419, 238, 680, H), radius=70, fill=255)
    im = Image.composite(cor, ImageEnhance.Color(im).enhance(0.15), md.filter(ImageFilter.GaussianBlur(2)))  # cor só no detector
    nitida = im.filter(ImageFilter.UnsharpMask(radius=4, percent=110, threshold=3))  # realça a silhueta da usina ao fundo
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rectangle((420, 60, W, 330), fill=255)
    im = Image.composite(nitida, im, m.filter(ImageFilter.GaussianBlur(40)))
    im = escurecer(im, (560, 420, W, H), 0.55, raio=90)
    im = vinheta(im, 0.45, cx=0.45, cy=0.45)
    im = grao(im)
    im, cx = texto(im, ["ON A SHOE"], W - 36, 520, 150, alinhar="r")
    im = bandeira_suecia(im, int(cx[0][0]) - 4, 440, 96)
    im = selo(im, W - 290, 450, 38)
    salvar(im, f"{X}/thumb-B.jpg"); return im


# ---------- C: roda-gigante real de Pripyat (contra-plongée) + "TEMPORARY" ----------
def C():
    im = fit(f"{F}/c3.jpg", zoom=1.0, cx=0.5, cy=0.5)
    im = acento_amarelo(grade(im, sat=1.0, contraste=1.2, brilho=0.9), sat_base=0.18, limiar=60)
    im = escurecer(im, (0, 520, W, 720), 0.6, raio=90)
    im = vinheta(im, 0.5, cx=0.5, cy=0.4)
    im = grao(im)
    im, _ = texto(im, ["“TEMPORARY”"], W / 2, 520, 168, alinhar="c")
    im = selo(im, 34, 26, 38)
    salvar(im, f"{X}/thumb-C.jpg"); return im


def vizinhas():
    fs = sorted(glob.glob(f"{V}/embalagem/thumbs/**/*.jpg", recursive=True) + glob.glob(f"{V}/embalagem/thumbs/**/*.webp", recursive=True))
    out = []
    for f in fs:
        try:
            im = Image.open(f).convert("RGB")
            if im.width / im.height < 1.6:
                h = int(im.width * 9 / 16); y = (im.height - h) // 2; im = im.crop((0, y, im.width, y + h))
            out.append(im)
        except Exception: pass
    return out[:15]


def prancha(novas):
    """linha 1: A/B/C reais a 320x180; linha 2: a 160x90; bloco 3: as 3 (borda amarela) no meio das thumbs do tema (160x90)."""
    gap = 14; f = ImageFont.truetype(ANTON, 22); fp = ImageFont.truetype(ANTON, 16)
    viz = vizinhas()
    grade_ = viz[:5] + [novas[0][1]] + viz[5:10] + [novas[1][1]] + viz[10:15] + [novas[2][1]]
    cols = 6; rows = (len(grade_) + cols - 1) // cols
    Wp = max(3 * 320 + 4 * gap, cols * 160 + (cols + 1) * gap) + 200
    Hp = gap + 180 + 34 + 90 + 40 + 30 + rows * (90 + gap) + gap
    P = Image.new("RGB", (Wp, Hp), (18, 18, 18)); d = ImageDraw.Draw(P)
    for i, (nome, im) in enumerate(novas):
        x = gap + i * (320 + gap + 60)
        P.paste(im.resize((320, 180), Image.LANCZOS), (x, gap)); d.text((x, gap + 186), f"{nome} · 320×180", font=f, fill=AMARELO)
        P.paste(im.resize((160, 90), Image.LANCZOS), (x, gap + 222)); d.text((x + 170, gap + 260), "160×90", font=fp, fill=(150, 150, 150))
    y0 = gap + 222 + 90 + 36
    d.text((gap, y0 - 4), "A/B/C (borda amarela) entre thumbs do tema (embalagem/thumbs), 160×90", font=fp, fill=(170, 170, 170))
    y0 += 26
    for k, im in enumerate(grade_):
        r, c = divmod(k, cols); x = gap + c * (160 + gap); y = y0 + r * (90 + gap)
        P.paste(im.resize((160, 90), Image.LANCZOS), (x, y))
        if any(im is t[1] for t in novas): d.rectangle((x - 3, y - 3, x + 162, y + 92), outline=AMARELO, width=3)
    P.save(f"{X}/prancha.jpg", quality=90); print(f"{X}/prancha.jpg", P.size)


if __name__ == "__main__":
    a, b, c = A(), B(), C()
    prancha([("A", a), ("B", b), ("C", c)])
