"""Thumbs finais da reembalagem do 010 Medellín (19/11/2026): Par C (principal) e Par B, aprovados no crivo r3.
Bases nano-banana em bases/ (C4 = folha + mão com pena; B2 = helicóptero sobre fazenda antioquenha).
Todo texto no código: "EXTRADICIÓN", linhas datilografadas, risco vermelho, sello "¿RESCATE?" e aba (estilo do 012 thumbs-extra).
Uso: tools/.venv/bin/python -I canais/dossie-es/videos/010-cartel-medellin/reembalagem-2026-11-19/final/compose.py"""
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

R = os.path.expanduser("~/workspace/fabrica-youtube")
X = f"{R}/canais/dossie-es/videos/010-cartel-medellin/reembalagem-2026-11-19/final"
G = os.path.dirname(X)  # grades do tema (pasta da reembalagem)
FD = f"{R}/pesquisa/reembalagem-2026-11-14/thumbs/fonts"
PAPEL = (233, 223, 201); ROJO = (179, 38, 30); TINTA = (26, 26, 26); PASTA = (200, 164, 106)
DESK = (47, 57, 66); FOLHA = (248, 241, 222)


def bebas(sz): return ImageFont.truetype(f"{FD}/BebasNeue-Regular.ttf", sz)
def elite(sz): return ImageFont.truetype(f"{FD}/SpecialElite-Regular.ttf", sz)


def aba(im):
    d = ImageDraw.Draw(im); f = elite(30); s = "EXPEDIENTE Nº 010"; w = int(d.textlength(s, font=f)) + 56
    x1 = 1280 - 34; x0 = x1 - w
    d.rounded_rectangle((x0 + 4, -20 + 5, x1 + 4, 62 + 5), radius=14, fill=(0, 0, 0))
    d.rounded_rectangle((x0, -20, x1, 62), radius=14, fill=PASTA)
    d.text(((x0 + x1) / 2, 26), s, font=f, fill=TINTA, anchor="mm")


def carimbo(im, cx, cy, s, size, ang=-6):
    """igual ao 012: fundo vermelho, filete cor papel por dentro, texto cor papel (~6,5:1)."""
    f = bebas(size); d0 = ImageDraw.Draw(im); w = int(d0.textlength(s, font=f)) + 76; h = int(size * 0.92) + 30
    L = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((20, 20, w + 20, h + 20), fill=ROJO)
    d.rectangle((31, 31, w + 9, h + 9), outline=PAPEL, width=3)
    d.text(((w + 40) / 2, (h + 40) / 2 + 4), s, font=f, fill=PAPEL, anchor="mm")
    L = L.rotate(ang, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", L.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 128), mask=L.split()[3])
    im.paste(sh, (int(cx - L.width / 2 + 6), int(cy - L.height / 2 + 8)), sh)
    im.paste(L, (int(cx - L.width / 2), int(cy - L.height / 2)), L)
    bb = f.getbbox(s); return bb[3] - bb[1]  # altura real das letras (px)


def salvar(im, p):
    q = 92
    while True:
        im.save(p, quality=q, optimize=True)
        if os.path.getsize(p) < 1900 * 1024 or q < 60: break
        q -= 4
    print(p, im.size, os.path.getsize(p) // 1024, "KB")


def fit(im, dy=0):
    w = 1280; h = int(im.height * w / im.width); im = im.resize((w, h), Image.LANCZOS)
    y = (im.height - 720) // 2 + dy
    return im.crop((0, y, 1280, y + 720))


# ---------------------------------------------------------------- C
def C():
    """Folha em paisagem na mesa escura; a mão com a pena (base C4) vai para a direita (+245 px) e a folha
    é estendida à esquerda no código (a folha da base é lisa e uniforme, a emenda some). Coordenadas da base 1344x768."""
    b = Image.open(f"{X}/bases/C4.jpg").convert("RGB")
    DX, DY = 245, -6; W, H = 1344, 756
    cv = Image.new("RGB", (W, H), DESK)
    cut = 700  # da base só entra x >= 700 (mão, pena, borda direita da folha)
    d = ImageDraw.Draw(cv)
    top, bot, L = 101 + DY, 638 + DY, 60  # bordas da folha na base: topo 101–103, base 636–638
    # sombra suave da folha estendida + papel + borda de tinta (3 px, igual à base); a base entra por cima
    sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rectangle((L + 6, top + 8, cut + DX + 60, bot + 8), fill=110)
    sh = sh.filter(ImageFilter.GaussianBlur(6)); cv.paste((10, 12, 16), mask=sh)
    d.rectangle((L, top, cut + DX + 60, bot), fill=FOLHA)
    d.rectangle((L, top, cut + DX + 60, top + 2), fill=TINTA); d.rectangle((L, bot - 2, cut + DX + 60, bot), fill=TINTA)
    d.rectangle((L, top, L + 2, bot), fill=TINTA)
    # emenda: os primeiros 50 px da base entram em degradê sobre a folha desenhada
    part = b.crop((cut, 0, b.width, b.height))
    m = Image.new("L", part.size, 255); dm = ImageDraw.Draw(m)
    for x in range(50): dm.line((x, 0, x, part.height), fill=int(255 * x / 50))
    cv.paste(part, (cut + DX, DY), m)
    nib = (833 + DX, 381 + DY)  # ponta da pena na base C4 = (833, 381)

    # camada de tinta (multiply) só onde é papel claro e fora da mão
    ink = Image.new("L", (W, H), 0); di = ImageDraw.Draw(ink)
    rnd = random.Random(10)
    for y in (150, 196, 242):  # linhas datilografadas ilegíveis acima da palavra
        di.line((L + 55, y, min(1250, L + 55 + rnd.randint(820, 1150)), y), fill=95, width=8)
    for y in (500, 546, 592):  # abaixo da palavra: param antes da sombra da mão
        di.line((L + 55, y, L + 55 + rnd.randint(620, 900), y), fill=95, width=8)
    # a palavra: datilografia pesada (Special Elite + contorno), termina logo depois da ponta da pena
    txt = "EXTRADICIÓN"; x0 = L + 48; x1 = nib[0] + 18
    sz = 100
    while elite(sz + 2).getlength(txt) <= x1 - x0: sz += 2
    f = elite(sz); bb = f.getbbox(txt, anchor="ls")
    cap = -elite(sz).getbbox("E", anchor="ls")[1]
    base_y = nib[1] + cap // 2 + 4
    di.text((x0, base_y), txt, font=f, fill=255, anchor="ls", stroke_width=3, stroke_fill=255)
    # máscara do papel: claro e pouco saturado (exclui pele, pena, punho/manga) e a região da mão
    r, g, bl = cv.split()
    claro = r.point(lambda v: 255 if v > 150 else 0)
    quente = ImageChops.subtract(r, bl).point(lambda v: 255 if v < 40 else 0)
    papel = ImageChops.multiply(claro, quente)
    mao = Image.new("L", (W, H), 255); ImageDraw.Draw(mao).polygon(
        [(nib[0] + 6, nib[1] - 12), (W, nib[1] - 90), (W, H), (nib[0] + 40, H), (nib[0] + 40, nib[1] + 30)], fill=0)
    papel = ImageChops.multiply(papel, mao)
    ink = ImageChops.multiply(ink, papel)
    tinta = Image.new("RGB", (W, H), TINTA)
    cv = Image.composite(tinta, cv, ink)

    # risco de caneta vermelha: da esquerda da palavra até a ponta da pena, leve subida e tremor
    rk = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(rk)
    y_mid = base_y - cap * 0.42
    pts = []; n = 40; xa = x0 - 22
    for i in range(n + 1):
        t = i / n; x = xa + (nib[0] - xa) * t
        y = (y_mid + 10) * (1 - t) + nib[1] * t + 3.5 * random.Random(i).uniform(-1, 1) * (1 - t)
        pts.append((x, y))
    dr.line(pts, fill=255, width=30, joint="curve")
    dr.ellipse((xa - 15, pts[0][1] - 15, xa + 15, pts[0][1] + 15), fill=255)
    rk = rk.filter(ImageFilter.GaussianBlur(0.8))
    rk = ImageChops.multiply(rk, ImageChops.multiply(claro, mao))
    rk = rk.point(lambda v: int(v * 0.94))
    cv = Image.composite(Image.new("RGB", (W, H), ROJO), cv, rk)

    im = cv.resize((1280, 720), Image.LANCZOS)
    aba(im)
    print(f"C: palavra {sz}px de fonte na base ({sz * 1280 / W:.0f}px na thumb = {sz * 1280 / W / 720:.0%}), "
          f"altura das maiúsculas {cap * 1280 / W:.0f}px ({cap * 1280 / W / 720:.0%})")
    salvar(im, f"{X}/thumb-C.jpg"); return im


# ---------------------------------------------------------------- B
def B():
    im = fit(Image.open(f"{X}/bases/B2.jpg").convert("RGB"))
    alt = carimbo(im, 300, 615, "¿RESCATE?", 132, ang=-6)  # canto inferior esquerdo, sobre folhas e serra (livre)
    aba(im)
    print(f"B: letra do sello {alt}px = {alt / 720:.1%} da altura (condição >= 12%)")
    salvar(im, f"{X}/thumb-B.jpg"); return im


# ---------------------------------------------------------------- prancha
def na_grade(nossa, gap, w, h, base):
    g = Image.open(base).convert("RGB"); g.paste(nossa.resize((w, h), Image.LANCZOS), (w + gap, h + gap)); return g


def prancha(c, b):
    """3 grades do tema (12 de 12 com rosto de Escobar): no ar | C | B, cada uma com a nossa no centro (linha 2, col 2)."""
    cols = [("NO AR (CTR 0,6%)", Image.open(f"{G}/grade-tema-no-ar-320.jpg").convert("RGB"),
             Image.open(f"{G}/grade-tema-no-ar-160.jpg").convert("RGB")),
            ("C · Escobar le declaró la guerra a una PALABRA", na_grade(c, 6, 320, 180, f"{G}/grade-tema-no-ar-320.jpg"),
             na_grade(c, 4, 160, 90, f"{G}/grade-tema-no-ar-160.jpg")),
            ("B · Cómo Escobar tomó de rehén a todo un país", na_grade(b, 6, 320, 180, f"{G}/grade-tema-no-ar-320.jpg"),
             na_grade(b, 4, 160, 90, f"{G}/grade-tema-no-ar-160.jpg"))]
    g320 = cols[0][1].size; g160 = cols[0][2].size; pad = 24; lab = 40
    Wp = 3 * g320[0] + 4 * pad; Hp = pad + lab + g320[1] + pad + lab + g160[1] + pad
    P = Image.new("RGB", (Wp, Hp), (18, 18, 18)); d = ImageDraw.Draw(P)
    for i, (nome, a, s) in enumerate(cols):
        x = pad + i * (g320[0] + pad)
        d.text((x, pad + 6), nome + "  · 320×180", font=elite(26), fill=PAPEL)
        P.paste(a, (x, pad + lab))
        y2 = pad + lab + g320[1] + pad
        d.text((x, y2 + 6), "160×90 (celular)", font=elite(24), fill=(170, 170, 170))
        P.paste(s, (x, y2 + lab))
    # tamanho real ao lado: as 2 thumbs a 320 e 160 isoladas
    P.save(f"{X}/prancha.jpg", quality=88); print(f"{X}/prancha.jpg", P.size)


if __name__ == "__main__":
    c, b = C(), B()
    prancha(c, b)
