"""Thumbs extra D/E do 012 MI6 (19/11/2026): prédio do MI6 + agente de smoking (arquétipo, sem ator/marca).
Texto, carimbo e aba no código, no estilo do src/Thumbnail.jsx do 012 (carimbo vermelho com texto cor papel, aba parda).
Uso (da raiz do repo): tools/.venv/bin/python canais/dossie-es/videos/012-mi6/thumbs-extra/compose.py"""
import os
from PIL import Image, ImageDraw, ImageFont

R = os.path.expanduser("~/workspace/fabrica-youtube")
V = f"{R}/canais/dossie-es/videos/012-mi6"
X = f"{V}/thumbs-extra"
FD2 = f"{R}/pesquisa/reembalagem-2026-11-14/thumbs/fonts"
PAPEL = (233, 223, 201); ROJO = (179, 38, 30); TINTA = (26, 26, 26); PASTA = (200, 164, 106)
TEXTO = "LO INVENTARON"


def bebas(sz): return ImageFont.truetype(f"{FD2}/BebasNeue-Regular.ttf", sz)
def elite(sz): return ImageFont.truetype(f"{FD2}/SpecialElite-Regular.ttf", sz)


def fit(im, dx=0):
    w = 1280; h = int(im.height * w / im.width); im = im.resize((w, h), Image.LANCZOS)
    x = (im.width - 1280) // 2 + dx; y = (im.height - 720) // 2
    return im.crop((x, y, x + 1280, y + 720))


def aba(im):
    d = ImageDraw.Draw(im); f = elite(30); s = "EXPEDIENTE Nº 012"; w = int(d.textlength(s, font=f)) + 56
    x1 = 1280 - 34; x0 = x1 - w
    d.rounded_rectangle((x0 + 4, -20 + 5, x1 + 4, 62 + 5), radius=14, fill=(0, 0, 0))
    d.rounded_rectangle((x0, -20, x1, 62), radius=14, fill=PASTA)
    d.text(((x0 + x1) / 2, 26), s, font=f, fill=TINTA, anchor="mm")


def carimbo(im, cx, cy, s, size, ang=-5):
    """igual ao Carimbo do Thumbnail.jsx: fundo vermelho, filete cor papel por dentro, texto cor papel (~6,5:1)."""
    f = bebas(size); d0 = ImageDraw.Draw(im); w = int(d0.textlength(s, font=f)) + 76; h = int(size * 0.92) + 30
    L = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((20, 20, w + 20, h + 20), fill=ROJO)
    d.rectangle((31, 31, w + 9, h + 9), outline=PAPEL, width=3)
    d.text(((w + 40) / 2, (h + 40) / 2 + 4), s, font=f, fill=PAPEL, anchor="mm")
    L = L.rotate(ang, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", L.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 128), mask=L.split()[3])
    im.paste(sh, (int(cx - L.width / 2 + 6), int(cy - L.height / 2 + 8)), sh)
    im.paste(L, (int(cx - L.width / 2), int(cy - L.height / 2)), L)


def salvar(im, p):
    q = 92
    while True:
        im.save(p, quality=q, optimize=True)
        if os.path.getsize(p) < 1900 * 1024 or q < 60: break
        q -= 4
    print(p, im.size, os.path.getsize(p) // 1024, "KB")


def D():
    # agente de costas à esquerda, prédio ao entardecer no centro-direita; carimbo no céu acima do agente
    im = fit(Image.open(f"{X}/bases/D1.jpg").convert("RGB"))
    carimbo(im, 330, 118, TEXTO, 112, ang=-5)
    aba(im); salvar(im, f"{X}/thumb-D.jpg"); return im


def E():
    # agente em 3/4 à esquerda com o rosto na sombra, prédio grande atrás; carimbo no céu à direita, abaixo da aba
    im = fit(Image.open(f"{X}/bases/E1.jpg").convert("RGB"))
    carimbo(im, 960, 150, TEXTO, 104, ang=-5)
    aba(im); salvar(im, f"{X}/thumb-E.jpg"); return im


def prancha(ims):
    """5 thumbs A–E: linha 1 a 320x180, linha 2 a 160x90 (tamanho de celular), rótulo embaixo."""
    gap = 16; W = 5 * 320 + 6 * gap; H = gap + 180 + 34 + 90 + 34 + gap
    P = Image.new("RGB", (W, H), (18, 18, 18)); d = ImageDraw.Draw(P); f = elite(22)
    for i, (nome, im) in enumerate(ims):
        x = gap + i * (320 + gap)
        P.paste(im.resize((320, 180), Image.LANCZOS), (x, gap))
        d.text((x + 160, gap + 180 + 17), nome, font=f, fill=PAPEL, anchor="mm")
        P.paste(im.resize((160, 90), Image.LANCZOS), (x, gap + 180 + 34))
        d.text((x + 80, gap + 180 + 34 + 90 + 17), "160×90", font=elite(16), fill=(150, 150, 150), anchor="mm")
    P.save(f"{X}/prancha-celular.jpg", quality=90); print(f"{X}/prancha-celular.jpg", P.size)


if __name__ == "__main__":
    d, e = D(), E()
    abc = [(k, Image.open(f"{V}/thumb-var/final/{k}.jpg").convert("RGB")) for k in "ABC"]
    prancha(abc + [("D", d), ("E", e)])
