"""Compõe os finais da identidade do historia-ptbr a partir de base/ (texto só no código, nenhuma letra da IA).
Uso (da raiz da fábrica): tools/.venv/bin/python canais/historia-ptbr/identidade/tools/compor.py
Saída em identidade/: logo-1..3.png (800x800), capa-1..2.png (2560x1440, < 6 MB), previa-logos.jpg, previa-capas.jpg.
O script falha (assert) se qualquer texto da capa sair da área segura 1546x423.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(AQUI, *a)  # noqa: E731
OURO, TINTA, PAPIRO, BRANCO = (247, 194, 27), (28, 20, 12), (244, 228, 190), (255, 255, 255)
W, H, SW, SH = 2560, 1440, 1546, 423
SX, SY = (W - SW) // 2, (H - SH) // 2
TITULO = "HISTÓRIA EM MINUTOS"
TAGLINE = "A história inteira de cada país, contada em minutos"


def caslon(sz):
    f = ImageFont.truetype(P("fontes", "LibreCaslonText[wght].ttf"), sz); f.set_variation_by_axes([700]); return f


def sans(sz):
    f = ImageFont.truetype(P("fontes", "OpenSans[wdth,wght].ttf"), sz); f.set_variation_by_axes([800, 100]); return f


# ---------- logos ----------
# (base, zoom: fração do lado mantida, centro x/y em fração) — o zoom faz o ícone ocupar o círculo (legível a 48 px)
LOGOS = [("logo-a-1", 0.80, 0.50, 0.50), ("logo-b-2", 0.86, 0.50, 0.53), ("logo-c-1", 0.92, 0.50, 0.50)]


def logo(nome, z, cx, cy, saida):
    im = Image.open(P("base", f"{nome}.jpg")).convert("RGB")
    n = im.size[0]
    cor = im.getpixel((8, 8))
    lado = int(n * z)
    x0 = max(0, min(n - lado, int(cx * n - lado / 2))); y0 = max(0, min(n - lado, int(cy * n - lado / 2)))
    out = im.crop((x0, y0, x0 + lado, y0 + lado)).resize((800, 800), Image.LANCZOS)
    # fundo uniforme: as bordas do quadrado (fora do círculo) recebem a cor chapada, sem ruído de JPEG
    m = Image.new("L", (800, 800), 0); ImageDraw.Draw(m).ellipse((4, 4, 796, 796), fill=255)
    fundo = Image.new("RGB", (800, 800), cor); fundo.paste(out, (0, 0), m.filter(ImageFilter.GaussianBlur(3)))
    fundo.save(saida, optimize=True)
    return fundo


def previa_logos(logos):
    tams, pad = (300, 98, 48), 40
    col = 300 + pad
    out = Image.new("RGB", (pad + len(logos) * col, pad + 300 + pad + 98 + pad + 48 + pad + 30), (245, 245, 245))
    d = ImageDraw.Draw(out)
    for i, l in enumerate(logos):
        y = pad
        for t in tams:
            x = pad + i * col + (300 - t) // 2
            m = Image.new("L", (t, t), 0); ImageDraw.Draw(m).ellipse((0, 0, t - 1, t - 1), fill=255)
            out.paste(l.resize((t, t), Image.LANCZOS), (x, y), m)
            y += t + pad
        d.text((pad + i * col + 120, y - 10), f"logo-{i + 1}", fill=(80, 80, 80), font=sans(24))
    # faixa escura: como o avatar aparece no tema escuro do app
    esc = Image.new("RGB", (out.size[0], 48 + 2 * 20), (15, 15, 15))
    for i, l in enumerate(logos):
        m = Image.new("L", (48, 48), 0); ImageDraw.Draw(m).ellipse((0, 0, 47, 47), fill=255)
        esc.paste(l.resize((48, 48), Image.LANCZOS), (pad + i * col + 126, 20), m)
    tudo = Image.new("RGB", (out.size[0], out.size[1] + esc.size[1]))
    tudo.paste(out, (0, 0)); tudo.paste(esc, (0, out.size[1]))
    tudo.save(P("previa-logos.jpg"), quality=90)


# ---------- capas ----------
def encaixa(nome, dy, escala=None):
    """Base na largura total do banner, deslocada dy px para baixo; o que sobra em cima/embaixo vira borda esticada e desfocada."""
    im = Image.open(P("base", f"{nome}.jpg")).convert("RGB")
    k = escala or W / im.size[0]
    im = im.resize((round(im.size[0] * k), round(im.size[1] * k)), Image.LANCZOS)
    x = (W - im.size[0]) // 2
    can = Image.new("RGB", (W, H))
    fundo = im.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(30))
    can.paste(fundo)
    if dy > 0:  # completa o topo esticando as primeiras linhas (céu)
        topo = im.crop((0, 0, im.size[0], 12)).resize((im.size[0], dy + 12), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
        can.paste(topo, (x, 0))
    falta = H - (dy + im.size[1])
    if falta > 0:  # completa o pé esticando as últimas linhas (chão)
        pe = im.crop((0, im.size[1] - 12, im.size[0], im.size[1])).resize((im.size[0], falta + 12), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
        can.paste(pe, (x, H - falta - 12))
    can.paste(im, (x, dy))
    return can


def sombra_texto(can, xy, s, font, fill, stroke=0, sfill=TINTA, sombra=8, anchor="mm"):
    d = ImageDraw.Draw(can)
    if sombra:
        d.text((xy[0] + sombra, xy[1] + sombra), s, font=font, fill=TINTA, stroke_width=stroke, stroke_fill=TINTA, anchor=anchor)
    d.text(xy, s, font=font, fill=fill, stroke_width=stroke, stroke_fill=sfill, anchor=anchor)
    return d.textbbox(xy, s, font=font, stroke_width=stroke, anchor=anchor)


def dentro(*caixas):
    for b in caixas:
        assert b[0] >= SX and b[2] <= SX + SW and b[1] >= SY and b[3] <= SY + SH, ("texto fora da área segura", b)


def placa_titulo(can, cy, linhas, tam, larg_max):
    """Placa de papiro claro com sombra chapada (o cartão do canal) e o título em tinta escura; MINUTOS em ouro com contorno."""
    d = ImageDraw.Draw(can)
    f = caslon(tam)
    while max(d.textlength(l, font=f) for l in linhas) > larg_max:
        tam -= 2; f = caslon(tam)
    alt = tam * 1.12
    larg = max(d.textlength(l, font=f) for l in linhas)
    cx = W // 2
    caixa = (cx - larg / 2 - 46, cy - alt * len(linhas) / 2 - 26, cx + larg / 2 + 46, cy + alt * len(linhas) / 2 + 30)
    d.rounded_rectangle([v + 12 for v in caixa], radius=22, fill=TINTA)
    d.rounded_rectangle(caixa, radius=22, fill=PAPIRO, outline=TINTA, width=7)
    bbs = [caixa]
    for i, l in enumerate(linhas):
        y = cy - alt * (len(linhas) - 1) / 2 + i * alt
        # palavra MINUTOS em ouro com contorno de tinta; o resto em tinta
        if "MINUTOS" in l:
            a, _, _ = l.partition("MINUTOS")
            wa, wm = d.textlength(a, font=f), d.textlength("MINUTOS", font=f)
            x0 = cx - (wa + wm) / 2
            d.text((x0, y), a, font=f, fill=TINTA, anchor="lm")
            d.text((x0 + wa, y), "MINUTOS", font=f, fill=OURO, stroke_width=5, stroke_fill=TINTA, anchor="lm")
        else:
            d.text((cx, y), l, font=f, fill=TINTA, anchor="mm")
    bbs[0] = (caixa[0], caixa[1], caixa[2] + 12, caixa[3] + 12)
    return bbs[0]


def pilula(can, cx, cy, s, tam):
    d = ImageDraw.Draw(can); f = sans(tam)
    b = d.textbbox((cx, cy), s, font=f, anchor="mm")
    r = (b[0] - 30, b[1] - 16, b[2] + 30, b[3] + 16)
    d.rounded_rectangle([v + 8 for v in r], radius=18, fill=TINTA)
    d.rounded_rectangle(r, radius=18, fill=OURO, outline=TINTA, width=6)
    d.text((cx, cy), s, font=f, fill=TINTA, anchor="mm")
    return (r[0], r[1], r[2] + 8, r[3] + 8)


def capa1():
    """Desfile das eras (Egito → hoje) com os marcos no horizonte; placa do título sobre os marcos, cabeças na faixa segura."""
    can = encaixa("capa-a-1", -70)
    b1 = placa_titulo(can, SY + 84, [TITULO], 112, SW - 200)
    b2 = pilula(can, W // 2, b1[3] + 38, TAGLINE, 38)
    dentro(b1, b2)
    can.save(P("capa-1.png"), optimize=True)
    return can


def capa2():
    """Livro aberto com o mundo da história saindo das páginas, bonequinhos das eras dos dois lados; título em 2 linhas no céu."""
    can = encaixa("capa-b-2", 190)
    b1 = placa_titulo(can, SY + 148, ["HISTÓRIA", "EM MINUTOS"], 104, 700)
    b2 = pilula(can, W // 2, b1[3] + 42, TAGLINE, 40)
    dentro(b1, b2)
    can.save(P("capa-2.png"), optimize=True)
    return can


def previa_capas(capas):
    linhas = []
    for c in capas:
        tv = c.resize((1280, 720), Image.LANCZOS)
        d = ImageDraw.Draw(tv)
        s = 0.5
        d.rectangle((SX * s, SY * s, (SX + SW) * s, (SY + SH) * s), outline=(0, 230, 110), width=4)
        d.rectangle((0, SY * s, 1279, (SY + SH) * s), outline=(255, 210, 0), width=3)
        d.text((10, 10), "TV = imagem inteira | amarelo = desktop | verde = celular (área segura)", fill=BRANCO,
               font=sans(20), stroke_width=3, stroke_fill=(0, 0, 0))
        desk = c.crop((0, SY, W, SY + SH)).resize((1280, round(SH * 1280 / W)), Image.LANCZOS)
        cel = c.crop((SX, SY, SX + SW, SY + SH)).resize((640, round(SH * 640 / SW)), Image.LANCZOS)
        lin = Image.new("RGB", (1280 + 20 + 640, 720), (30, 30, 30))
        lin.paste(tv, (0, 0))
        dd = ImageDraw.Draw(lin)
        dd.text((1300, 20), "desktop (2560x423)", fill=BRANCO, font=sans(22))
        lin.paste(desk.resize((640, round(desk.size[1] * 640 / 1280))), (1300, 56))
        dd.text((1300, 230), "celular (1546x423)", fill=BRANCO, font=sans(22))
        lin.paste(cel, (1300, 266))
        dd.text((1300, 460), "celular real (~360 px)", fill=BRANCO, font=sans(22))
        lin.paste(cel.resize((360, round(cel.size[1] * 360 / 640))), (1300, 496))
        linhas.append(lin)
    p = Image.new("RGB", (linhas[0].size[0], 720 * len(linhas) + 20 * (len(linhas) - 1)), (255, 255, 255))
    for i, o in enumerate(linhas):
        p.paste(o, (0, i * 740))
    p.save(P("previa-capas.jpg"), quality=88)


if __name__ == "__main__":
    ls = [logo(b, z, cx, cy, P(f"logo-{i}.png")) for i, (b, z, cx, cy) in enumerate(LOGOS, 1)]
    previa_logos(ls)
    previa_capas([capa1(), capa2()])
    for n in ("logo-1", "logo-2", "logo-3", "capa-1", "capa-2"):
        print(n, os.path.getsize(P(f"{n}.png")) // 1024, "KB")
