"""Pôster A3 300 dpi, wallpapers e teaser a partir das artes já ampliadas pelo Real-ESRGAN (grátis, CPU).

Pré-requisito (fora do git, ~9 min no CPU via lavapipe para o pôster; ~1 min por wallpaper):
  RE=~/cache/realesrgan/realesrgan-ncnn-vulkan   (release v0.2.5.0 do xinntao/Real-ESRGAN, roda sem GPU via Vulkan lavapipe)
  $RE -i arte/K01.jpg -o $TMPDIR/manga/K01-x4anime.png -n realesrgan-x4plus-anime -t 256
  $RE -i W01.jpg -o $TMPDIR/manga/W01-x3.png -n realesr-animevideov3 -s 3 ; idem W02 recortado (W02c) → W02-x3.png
Uso: ~/workspace/fabrica-youtube/tools/.venv/bin/python extras.py
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(AQUI, ".."))
TMP = os.path.join(os.environ.get("TMPDIR") or os.path.expanduser("~/cache/tmp"), "manga")
F = os.path.join(AQUI, "fontes")
VERM, PRETO, PAPEL = (179, 38, 30), (17, 17, 17), (233, 223, 201)


def ampliar(arq, fator):
    """LANCZOS + nitidez. Escolhido em 23/11/2026 no lugar do Real-ESRGAN: os 3 modelos testados (x4plus, x4plus-anime,
    animevideov3) transformam a retícula do mangá em textura de "labirinto" (comparacao-poster-100pct.jpg)."""
    im = Image.open(os.path.join(OUT, "arte", arq)).convert("RGB")
    im = im.resize((im.width * fator, im.height * fator), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=2 * fator / 2, percent=80, threshold=2))


def fnt(arq, px):
    return ImageFont.truetype(os.path.join(F, arq), int(px))


def centro(d, y, txt, f, W, **kw):
    d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, **kw)


def previa(im, nome, larg):
    p = im.copy()
    p.thumbnail((larg, larg * 3))
    q = 88
    while True:
        p.save(os.path.join(OUT, nome), "JPEG", quality=q, optimize=True, progressive=True)
        if os.path.getsize(os.path.join(OUT, nome)) <= 1_000_000 or q <= 28:
            break
        q -= 6
    print(nome, p.size, os.path.getsize(os.path.join(OUT, nome)) // 1024, "KB")


def gradiente_topo(im, frac, forca=235):
    W, H = im.size
    g = Image.linear_gradient("L").resize((1, H))  # 0 em cima → 255 embaixo
    g = g.point(lambda v: int(forca * max(0.0, 1 - (v / 255) / frac) ** 1.3))
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    camada.putalpha(g.resize((W, H)))
    base = im.convert("RGBA")
    base.alpha_composite(camada)
    return base


def poster():
    W, H = 3508, 4961  # A3 a 300 dpi
    art = ampliar("K01.jpg", 4)  # 4096×6144
    h = round(art.width * H / W)
    oy = round((art.height - h) * 0.35)
    art = art.crop((0, oy, art.width, oy + h)).resize((W, H), Image.LANCZOS)
    im = gradiente_topo(art, 0.36)
    d = ImageDraw.Draw(im)
    s = W / 1800
    centro(d, 70 * s, "DOSSIER EN MINUTOS  ·  EXPEDIENTE ESPECIAL Nº 1", fnt("BebasNeue-Regular.ttf", 44 * s), W, fill=PAPEL)
    for txt, px, y in (("OPERACIÓN", 200, 165), ("GARBO", 320, 335)):
        f = fnt("Bangers-Regular.ttf", px * s)
        x = (W - d.textlength(txt, font=f)) / 2
        d.text((x + 12 * s, y * s + 12 * s), txt, font=f, fill=VERM, stroke_width=int(10 * s), stroke_fill=VERM)
        d.text((x, y * s), txt, font=f, fill="white", stroke_width=int(10 * s), stroke_fill=PRETO)
    centro(d, 690 * s, "EL ESPAÑOL QUE ENGAÑÓ A HITLER", fnt("BebasNeue-Regular.ttf", 88 * s), W, fill=PAPEL,
           stroke_width=int(3 * s), stroke_fill=PRETO)
    d.rectangle((0, H - 110 * s, W, H), fill=PRETO)
    centro(d, H - 86 * s, "JUAN PUJOL GARCÍA, «GARBO»  ·  BARCELONA 1912 – CARACAS 1988  ·  27 ESPÍAS QUE NUNCA EXISTIERON",
           fnt("BebasNeue-Regular.ttf", 40 * s), W, fill=PAPEL)
    im = im.convert("RGB")
    im.save(os.path.join(OUT, "poster-A3.png"), dpi=(300, 300), optimize=True)
    print("poster-A3.png", im.size, os.path.getsize(os.path.join(OUT, "poster-A3.png")) // 1024, "KB")
    previa(im, "poster-preview.jpg", 1200)
    return im


def wallpapers():
    d1 = ampliar("W01.jpg", 3)
    W, H = 3840, 2160
    h = round(d1.width * H / W)
    oy = (d1.height - h) // 2
    d1 = d1.crop((0, oy, d1.width, oy + h)).resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(d1)
    f = fnt("Bangers-Regular.ttf", 120)
    d.text((150, 1880), "OPERACIÓN GARBO", font=f, fill=(235, 235, 235), stroke_width=6, stroke_fill=PRETO)
    d.text((158, 2010), "DOSSIER EN MINUTOS", font=fnt("BebasNeue-Regular.ttf", 58), fill=VERM)
    d1.save(os.path.join(OUT, "wallpaper-desktop.png"), optimize=True)
    previa(d1, "wallpaper-desktop.jpg", 3840)  # 3840 px; reduz a qualidade até ≤ 1 MB

    c1 = ampliar("W02.jpg", 3)
    nw = round(c1.height * 1440 / 3120)
    x = (c1.width - nw) // 2
    c1 = c1.crop((x, 0, x + nw, c1.height)).resize((1440, 3120), Image.LANCZOS)
    d = ImageDraw.Draw(c1)
    f = fnt("Bangers-Regular.ttf", 96)
    centro(d, 2960, "OPERACIÓN GARBO", f, 1440, fill=(240, 240, 240), stroke_width=5, stroke_fill=PRETO)
    c1.save(os.path.join(OUT, "wallpaper-celular.png"), optimize=True)
    previa(c1, "wallpaper-celular.jpg", 1440)


def teaser():
    """1280×720 para post na aba Comunidade / imagem do Short (16:9)."""
    W, H = 1280, 720
    im = Image.new("RGB", (W, H), PRETO)
    capa = Image.open(os.path.join(OUT, "capa.png")).convert("RGB")
    capa.thumbnail((440, 660))
    im.paste(capa, (70, 30))
    p2 = Image.open(os.path.join(OUT, "pagina-1.png")).convert("RGB").rotate(-6, expand=True, fillcolor=PRETO)
    p2.thumbnail((360, 540))
    d = ImageDraw.Draw(im)
    centro_x = 560
    d.text((centro_x, 70), "NUEVO · MANGA", font=fnt("BebasNeue-Regular.ttf", 64), fill=VERM)
    d.text((centro_x, 140), "OPERACIÓN", font=fnt("Bangers-Regular.ttf", 110), fill="white", stroke_width=4, stroke_fill=PRETO)
    d.text((centro_x, 260), "GARBO", font=fnt("Bangers-Regular.ttf", 170), fill="white", stroke_width=4, stroke_fill=VERM)
    d.text((centro_x, 450), "El español que engañó a Hitler,", font=fnt("ComicNeue-Bold.ttf", 44), fill=PAPEL)
    d.text((centro_x, 505), "contado con viñetas y bocadillos.", font=fnt("ComicNeue-Bold.ttf", 44), fill=PAPEL)
    d.rectangle((centro_x, 600, centro_x + 520, 660), outline=VERM, width=5)
    d.text((centro_x + 22, 606), "HECHOS REALES · 1941–1944", font=fnt("BebasNeue-Regular.ttf", 48), fill=VERM)
    previa(im, "teaser.jpg", 1280)


def comparacao(poster_im):
    """Recorte a 100 % (o que sai na impressão A3 a 300 dpi) do rosto: Real-ESRGAN × LANCZOS × Gemini 4K nativa."""
    W, H = 3508, 4961
    cx, cy, r = 0.5, 0.40, 450  # região do rosto (fração da imagem, raio em px do A3)

    def a3(im, oyf=0.35):
        h = round(im.width * H / W)
        oy = round((im.height - h) * oyf)
        return im.crop((0, oy, im.width, oy + h)).resize((W, H), Image.LANCZOS)
    esr = a3(Image.open(os.path.join(TMP, "K01-x4anime.png")).convert("RGB"))
    g4 = a3(Image.open(os.path.join(OUT, "arte-gemini4k", "K01.jpg")).convert("RGB"))
    lz = a3(ampliar("K01.jpg", 4))
    tiras = []
    for nome, im, (fx, fy) in (("Codex + LANCZOS + nitidez (ESCOLHIDO, grátis)", lz, (cx, cy)),
                               ("Codex + Real-ESRGAN anime x4 (labirinto na retícula)", esr, (cx, cy)),
                               ("Gemini 4K nativa (US$ 0,12; outra arte)", g4, (0.5, 0.31))):
        x, y = int(fx * W), int(fy * H)
        t = im.crop((x - r, y - r, x + r, y + r))
        d = ImageDraw.Draw(t)
        d.rectangle((0, 0, 2 * r, 60), fill=PRETO)
        d.text((14, 8), nome, font=fnt("BebasNeue-Regular.ttf", 44), fill="white")
        tiras.append(t)
    comp = Image.new("RGB", (2 * r * len(tiras) + 20 * (len(tiras) - 1), 2 * r), "white")
    for i, t in enumerate(tiras):
        comp.paste(t, (i * (2 * r + 20), 0))
    previa(comp, "comparacao-poster-100pct.jpg", 2400)


if __name__ == "__main__":
    p = poster()
    wallpapers()
    teaser()
    comparacao(p)
