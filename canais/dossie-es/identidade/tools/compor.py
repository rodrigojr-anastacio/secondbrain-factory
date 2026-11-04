"""Compõe os arquivos finais da identidade do dossie-es a partir de base/ (texto só no código).
Uso: tools/.venv/bin/python canais/dossie-es/identidade/tools/compor.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(AQUI, *a)  # noqa: E731
ARDOSIA, PAPEL, ROJO, TINTA = (46, 58, 70), (233, 223, 201), (179, 38, 30), (26, 26, 26)
BEBAS, ELITE = P("fontes", "BebasNeue-Regular.ttf"), P("fontes", "SpecialElite-Regular.ttf")
W, H, SW, SH = 2560, 1440, 1546, 423
SX, SY = (W - SW) // 2, (H - SH) // 2


# ---------- logos ----------
def logo(nome, saida):
    im = Image.open(P("base", f"{nome}.jpg")).convert("RGB")
    n = im.size[0]
    # o modelo desenhou o próprio círculo sobre branco: usamos a cor do círculo como fundo quadrado inteiro
    cor = im.getpixel((n // 2, int(n * 0.06)))
    fundo = Image.new("RGB", im.size, cor)
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).ellipse((n * 0.012, n * 0.012, n * 0.988, n * 0.988), fill=255)
    fundo.paste(im, (0, 0), m.filter(ImageFilter.GaussianBlur(2)))
    # zoom leve para o ícone ocupar mais o círculo (legível a 98 px)
    c = int(n * 0.08)
    fundo = fundo.crop((c, c, n - c, n - c)).resize((800, 800), Image.LANCZOS)
    fundo.save(saida, optimize=True)
    return fundo


def previa_logos(logos):
    t, pad = 98, 40
    W2 = pad + len(logos) * (t + pad)
    for escala in (1, 3):  # 98 px reais + ampliação 3x para conferir
        pass
    out = Image.new("RGB", (pad + 3 * (300 + pad), 300 + 98 + 3 * pad), (245, 245, 245))
    d = ImageDraw.Draw(out)
    for i, l in enumerate(logos):
        for tam, y in ((300, pad), (t, 300 + 2 * pad)):
            x = pad + i * (300 + pad) + (300 - tam) // 2
            m = Image.new("L", (tam, tam), 0)
            ImageDraw.Draw(m).ellipse((0, 0, tam - 1, tam - 1), fill=255)
            out.paste(l.resize((tam, tam), Image.LANCZOS), (x, y), m)
        d.text((pad + i * (300 + pad), 300 + 2 * pad + t + 6), f"logo-{i + 1}", fill=(90, 90, 90))
    out.save(P("previa-logos.jpg"), quality=90)


# ---------- capas ----------
def faixa(nome, y0, y1):
    im = Image.open(P("base", f"{nome}.jpg")).convert("RGB").crop((0, y0, 1344, y1))
    h = round(im.size[1] * W / 1344)
    return im.resize((W, h), Image.LANCZOS)


def fundo_capa(f, cor_fundo):
    """Cola a faixa ilustrada no centro vertical e completa em cima/embaixo com a própria borda desfocada."""
    can = Image.new("RGB", (W, H), cor_fundo)
    y = (H - f.size[1]) // 2
    borrada = f.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
    can.paste(Image.blend(borrada, Image.new("RGB", (W, H), cor_fundo), 0.55))
    m = Image.new("L", f.size, 255)
    dm = ImageDraw.Draw(m)
    for i in range(60):  # degradê nas bordas de cima/baixo da faixa
        a = int(255 * i / 60)
        dm.line((0, i, W, i), fill=a); dm.line((0, f.size[1] - 1 - i, W, f.size[1] - 1 - i), fill=a)
    can.paste(f, (0, y), m)
    return can


def vinheta_centro(can, forca=150):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse((SX - 60, SY + 10, SX + SW + 60, SY + SH - 10), fill=forca)
    m = m.filter(ImageFilter.GaussianBlur(90))
    return Image.composite(Image.new("RGB", (W, H), (16, 20, 25)), can, m)


def texto(can):
    d = ImageDraw.Draw(can)
    tit = "DOSSIER EN MINUTOS"
    f = ImageFont.truetype(BEBAS, 220)
    bw = d.textbbox((0, 0), tit, font=f)
    tw, th = bw[2] - bw[0], bw[3] - bw[1]
    cx = W // 2
    ty = SY + 40
    # sombra de tinta + título em papel
    d.text((cx - tw // 2 + 7, ty + 8 - bw[1]), tit, font=f, fill=(0, 0, 0))
    d.text((cx - tw // 2, ty - bw[1]), tit, font=f, fill=PAPEL)
    # sublinhado rojo sello
    ly = ty + th + 22
    d.rectangle((cx - tw // 2, ly, cx + tw // 2, ly + 9), fill=ROJO)
    # linha em máquina de escrever sobre tira de papel
    lin = "La historia completa de las organizaciones más secretas del mundo"
    fe = ImageFont.truetype(ELITE, 40)
    b2 = d.textbbox((0, 0), lin, font=fe)
    lw, lh = b2[2] - b2[0], b2[3] - b2[1]
    py = ly + 40
    tira = (cx - lw // 2 - 22, py, cx + lw // 2 + 22, py + lh + 30)
    d.rectangle((tira[0] + 6, tira[1] + 7, tira[2] + 6, tira[3] + 7), fill=(0, 0, 0))
    d.rectangle(tira, fill=PAPEL, outline=TINTA, width=3)
    d.text((cx - lw // 2, py + 15 - b2[1]), lin, font=fe, fill=TINTA)
    fim = tira[3] + 7
    assert tira[0] >= SX and tira[2] <= SX + SW and ty >= SY and fim <= SY + SH, ("fora da área segura", tira, ty, fim)
    assert cx - tw // 2 >= SX
    return can


def selo(can, x, y, r=78, ang=-14):
    """Sello rojo sem letras (anel duplo + estrela), carimbado em ângulo."""
    s = Image.new("RGBA", (2 * r + 20, 2 * r + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    c = r + 10
    d.ellipse((c - r, c - r, c + r, c + r), outline=ROJO + (225,), width=9)
    d.ellipse((c - r + 17, c - r + 17, c + r - 17, c + r - 17), outline=ROJO + (225,), width=4)
    import math
    pts = [(c + (r * 0.5 if i % 2 == 0 else r * 0.2) * math.sin(math.pi * i / 5),
            c - (r * 0.5 if i % 2 == 0 else r * 0.2) * math.cos(math.pi * i / 5)) for i in range(10)]
    d.polygon(pts, fill=ROJO + (225,))
    s = s.rotate(ang, resample=Image.BICUBIC)
    can.paste(s, (x - s.size[0] // 2, y - s.size[1] // 2), s)


def capa1():
    f = faixa("capa-a", 104, 664)
    can = vinheta_centro(fundo_capa(f, ARDOSIA), 110)
    can = texto(can)
    can.save(P("capa-1.png"), optimize=True)
    return can


def capa2():
    im = Image.open(P("base", "capa-b.jpg")).convert("RGB")
    # cobre as pseudoletras do bilhete preso no arquivo (x~283-325, y~312-322 na base)
    ImageDraw.Draw(im).rectangle((282, 309, 326, 324), fill=(150, 146, 120))
    im.save("/tmp/_capa-b-limpa.jpg", quality=95)
    f = Image.open("/tmp/_capa-b-limpa.jpg").crop((0, 224, 1344, 545))
    f = f.resize((W, round(f.size[1] * W / 1344)), Image.LANCZOS)
    can = vinheta_centro(fundo_capa(f, (14, 17, 21)), 190)
    can = texto(can)
    selo(can, SX + SW + 130, SY + SH // 2, r=92)  # fora do título; aparece no desktop e na TV
    can.save(P("capa-2.png"), optimize=True)
    return can


def previa_capas(capas):
    out = []
    for c in capas:
        c = c.copy()
        d = ImageDraw.Draw(c)
        d.rectangle((SX, SY, SX + SW, SY + SH), outline=(0, 255, 120), width=6)          # mobile + desktop mínimo
        d.rectangle((0, SY, W - 1, SY + SH), outline=(255, 210, 0), width=4)              # desktop máximo
        d.text((SX + 12, SY + SH + 10), "area segura 1546x423 (verde) | desktop 2560x423 (amarelo) | TV = imagem inteira",
               fill=(255, 255, 255), font=ImageFont.truetype(ELITE, 34))
        out.append(c.resize((1280, 720), Image.LANCZOS))
    p = Image.new("RGB", (1280, 720 * len(out) + 20 * (len(out) - 1)), (255, 255, 255))
    for i, o in enumerate(out):
        p.paste(o, (0, i * 740))
    p.save(P("previa-capas.jpg"), quality=88)


if __name__ == "__main__":
    ls = [logo(b, P(f"logo-{i}.png")) for i, b in enumerate(["logo-b", "logo-a", "logo-c"], 1)]
    previa_logos(ls)
    previa_capas([capa1(), capa2()])
    print("ok")
