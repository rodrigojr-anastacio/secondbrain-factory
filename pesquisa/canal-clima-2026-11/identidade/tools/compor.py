"""Compõe os finais da identidade do canal "Em Relevo" a partir de base/ (texto só no código). Grátis.
Uso: tools/.venv/bin/python pesquisa/canal-clima-2026-11/identidade/tools/compor.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(AQUI, *a)  # noqa: E731
# paleta dos vídeos (longo-01/shared/cues.json + Longo.jsx)
PAPEL, CORAL, NAVY, TINTA, BRANCO = (233, 220, 195), (232, 80, 91), (31, 42, 68), (43, 38, 34), (251, 248, 241)
PINO_CLARO, PINO = (255, 138, 143), (201, 48, 59)
ANTON, MONO_B, MONO_M = P("fontes", "Anton-Regular.ttf"), P("fontes", "IBMPlexMono-Bold.ttf"), P("fontes", "IBMPlexMono-Medium.ttf")
W, H, SW, SH = 2560, 1440, 1546, 423
SX, SY = (W - SW) // 2, (H - SH) // 2
TITULO = "EM RELEVO"
LINHA = "O QUE ESTÁ ACONTECENDO NO MUNDO, EXPLICADO NO MAPA"


# ---------- logos ----------
def logo(base, caixa, saida):
    """caixa = (cx, cy, lado) em px da base; recorta quadrado centrado no ícone e completa com a cor do fundo."""
    im = Image.open(P("base", f"{base}.jpg")).convert("RGB")
    n = im.size[0]
    cor = tuple(sum(im.getpixel(p)[k] for p in ((8, 8), (n - 9, 8), (8, n - 9), (n - 9, n - 9))) // 4 for k in range(3))
    cx, cy, lado = caixa
    can = Image.new("RGB", (lado, lado), cor)
    x0, y0 = cx - lado // 2, cy - lado // 2
    can.paste(im, (-x0, -y0))
    if x0 < 0 or y0 < 0 or x0 + lado > n or y0 + lado > n:  # emenda suave onde a base acabou
        m = Image.new("L", (lado, lado), 0)
        ImageDraw.Draw(m).rectangle((max(0, -x0), max(0, -y0), min(lado, n - x0) - 1, min(lado, n - y0) - 1), fill=255)
        can = Image.composite(can, Image.new("RGB", (lado, lado), cor), m.filter(ImageFilter.GaussianBlur(25)))
    out = can.resize((800, 800), Image.LANCZOS)
    out.save(saida, optimize=True)
    return out


def previa_logos(logos):
    pad, g, t = 40, 300, 98
    out = Image.new("RGB", (pad + len(logos) * (g + pad), g + t + 4 * pad), (245, 245, 245))
    d = ImageDraw.Draw(out)
    f = ImageFont.truetype(MONO_M, 18)
    for i, l in enumerate(logos):
        for tam, y in ((g, pad), (t, g + 2 * pad)):
            x = pad + i * (g + pad) + (g - tam) // 2
            m = Image.new("L", (tam, tam), 0)
            ImageDraw.Draw(m).ellipse((0, 0, tam - 1, tam - 1), fill=255)
            out.paste(l.resize((tam, tam), Image.LANCZOS), (x, y), m)
        d.text((pad + i * (g + pad) + g // 2, g + 2 * pad + t + 14), f"logo-{i + 1}  (300 px / 98 px)", fill=(90, 90, 90), font=f, anchor="mt")
    out.save(P("previa-logos.jpg"), quality=90)


# ---------- capas ----------
def base_capa(nome):
    return Image.open(P("base", f"{nome}.jpg")).convert("RGB").resize((W, H), Image.LANCZOS)  # 1344x768 já é 16:9


def tachinha(can, x, y, r=22):
    s = Image.new("RGBA", (4 * r, 4 * r), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    d.ellipse((r + 6, r + 10, 3 * r + 6, 3 * r + 10), fill=(0, 0, 0, 110))
    s = s.filter(ImageFilter.GaussianBlur(5))
    d = ImageDraw.Draw(s)
    for k in range(r, 0, -1):  # gradiente radial como no Longo.jsx
        a = k / r
        c = tuple(int(PINO_CLARO[i] * (1 - a) + PINO[i] * a) for i in range(3))
        off = int((r - k) * 0.35)
        d.ellipse((2 * r - k - off, 2 * r - k - off, 2 * r + k - off, 2 * r + k - off), fill=c + (255,))
    can.paste(s, (x - 2 * r, y - 2 * r), s)


def sombra(can, caixa, raio=0, desfoque=22, alfa=120, desloc=(0, 16)):
    m = Image.new("L", (W, H), 0)
    x0, y0, x1, y1 = caixa
    ImageDraw.Draw(m).rounded_rectangle((x0 + desloc[0], y0 + desloc[1], x1 + desloc[0], y1 + desloc[1]), raio, fill=alfa)
    return Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), can, m.filter(ImageFilter.GaussianBlur(desfoque)))


def linha_navy(can, cy, tam=40):
    """Faixa navy com mono caixa-alta (camada fixa dos vídeos), centrada em cy."""
    d = ImageDraw.Draw(can)
    f = ImageFont.truetype(MONO_B, tam)
    b = d.textbbox((0, 0), LINHA, font=f)
    lw, lh = b[2] - b[0], b[3] - b[1]
    cx = W // 2
    cx0, cx1 = cx - lw // 2 - 30, cx + lw // 2 + 30
    caixa = (cx0, cy - lh // 2 - 20, cx1, cy + lh // 2 + 20)
    can = sombra(can, caixa, 6, 14, 110, (0, 10))
    d = ImageDraw.Draw(can)
    d.rounded_rectangle(caixa, 6, fill=NAVY)
    d.text((cx - lw // 2, cy - lh // 2 - b[1]), LINHA, font=f, fill=BRANCO)
    return can, caixa


def dentro(*caixas):
    for c in caixas:
        assert c[0] >= SX and c[1] >= SY and c[2] <= SX + SW and c[3] <= SY + SH, ("fora da área segura", c)


def capa1():
    """Mapa-múndi de papel em relevo sobre o oceano navy; título coral com sombra + faixa navy."""
    can = base_capa("capa-a-2")
    # escurece o miolo para o título ler sobre o mapa
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse((SX - 260, SY - 120, SX + SW + 260, SY + SH + 120), fill=165)
    can = Image.composite(Image.new("RGB", (W, H), (14, 19, 32)), can, m.filter(ImageFilter.GaussianBlur(120)))
    d = ImageDraw.Draw(can)
    f = ImageFont.truetype(ANTON, 250)
    b = d.textbbox((0, 0), TITULO, font=f)
    tw, th = b[2] - b[0], b[3] - b[1]
    tx, ty = W // 2 - tw // 2, SY + 30
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).text((tx + 8, ty + 12 - b[1]), TITULO, font=f, fill=200)
    can = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), can, sh.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(can)
    d.text((tx, ty - b[1]), TITULO, font=f, fill=CORAL)
    can, faixa = linha_navy(can, ty + th + 68, 38)
    dentro((tx, ty, tx + tw, ty + th), faixa)
    tachinha(can, faixa[0] + 2, faixa[1] + 4, 20)
    can.save(P("capa-1.png"), optimize=True)
    return can


def capa2():
    """Quadro de cortiça com relevo de papel; título numa etiqueta de papel presa com tachinhas + faixa navy."""
    can = base_capa("capa-b-2")
    d = ImageDraw.Draw(can)
    f = ImageFont.truetype(ANTON, 205)
    b = d.textbbox((0, 0), TITULO, font=f)
    tw, th = b[2] - b[0], b[3] - b[1]
    # etiqueta de papel (rotacionada) com o título navy e o "RELEVO" coral
    ew, eh = tw + 120, th + 90
    et = Image.new("RGBA", (ew, eh), BRANCO + (255,))
    de = ImageDraw.Draw(et)
    de.rectangle((0, 0, ew - 1, eh - 1), outline=(214, 204, 186), width=3)
    x = 60
    em = "EM "
    de.text((x, 45 - b[1]), em, font=f, fill=NAVY)
    x += de.textlength(em, font=f)
    de.text((x, 45 - b[1]), "RELEVO", font=f, fill=CORAL)
    et = et.rotate(-1.2, resample=Image.BICUBIC, expand=True)
    ex, ey = W // 2 - et.size[0] // 2, SY + 6
    can = sombra(can, (ex + 10, ey + 10, ex + et.size[0] - 10, ey + et.size[1] - 10), 0, 26, 140, (6, 20))
    can.paste(et, (ex, ey), et)
    tachinha(can, ex + 40, ey + 34, 22)
    tachinha(can, ex + et.size[0] - 40, ey + 30, 22)
    can, faixa = linha_navy(can, ey + et.size[1] + 52, 38)
    dentro((ex, ey, ex + et.size[0], ey + et.size[1]), faixa)
    can.save(P("capa-2.png"), optimize=True)
    return can


def previa_capas(capas):
    out = []
    f = ImageFont.truetype(MONO_B, 32)
    for c in capas:
        c = c.copy()
        d = ImageDraw.Draw(c)
        d.rectangle((SX, SY, SX + SW, SY + SH), outline=(0, 255, 120), width=6)
        d.rectangle((0, SY, W - 1, SY + SH), outline=(255, 210, 0), width=4)
        d.text((SX + 12, SY + SH + 14), "area segura 1546x423 (verde) | desktop 2560x423 (amarelo) | TV = imagem inteira",
               fill=(255, 255, 255), font=f, stroke_width=3, stroke_fill=(0, 0, 0))
        out.append(c.resize((1280, 720), Image.LANCZOS))
    p = Image.new("RGB", (1280, 720 * len(out) + 20 * (len(out) - 1)), (255, 255, 255))
    for i, o in enumerate(out):
        p.paste(o, (0, i * 740))
    p.save(P("previa-capas.jpg"), quality=88)


if __name__ == "__main__":
    ls = [logo("logo-b-2", (512, 560, 900), P("logo-1.png")),
          logo("logo-a-1", (512, 500, 700), P("logo-2.png")),
          logo("logo-c-1", (520, 500, 860), P("logo-3.png"))]
    previa_logos(ls)
    previa_capas([capa1(), capa2()])
    print("ok")
