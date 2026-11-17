"""Thumbs do 011-estados-unidos (3 conceitos do EMBALAGEM.md r3): A rosto-emocao "IGUAIS?"; B objeto-simbolo "LIBERDADE"; C antes-depois "1776" | "2026".
Adaptado de 010-japao/thumbs/compose.py (usa os helpers do 003-ira). Uso (pasta do vídeo): ../../../../tools/.venv/bin/python thumbs/compose.py"""
import os
from PIL import Image, ImageDraw
CP = os.path.abspath("../003-ira/v2-amostras/thumbs/base/compose.py")
src = open(CP).read().split("os.makedirs(V,exist_ok=True)")[0]
c = {"__file__": CP}; exec(src, c)
GOLD, WHITE = c["GOLD"], c["WHITE"]
B, F, D = "thumb-var", "thumb-var/final", "entrega"
W, H = 1280, 720


def base(n): return Image.open(f"{B}/{n}.jpg").convert("RGB").resize((W, H), Image.LANCZOS)


def fit(d, s, maxw, hi, lo=50):
    for sz in range(hi, lo, -2):
        if d.textlength(s, font=c["caslon"](sz)) <= maxw: return c["caslon"](sz)
    return c["caslon"](lo)


def escurece_direita(im, w=520, a=215):
    ov = Image.new("L", im.size, 0); d = ImageDraw.Draw(ov)
    for i in range(w): d.line([(W - 1 - i, 0), (W - 1 - i, H - 1)], fill=int(a * (1 - i / w) ** 1.2))
    return Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ov)


def thumb_a():
    im = escurece_direita(base("thumb-A")); d = ImageDraw.Draw(im)
    f = fit(d, "IGUAIS?", 520, 190)
    c["text"](im, (1255, 430), "IGUAIS?", f, GOLD, stroke=10, anchor="rs")
    return im


def thumb_b():
    im = escurece_direita(base("thumb-B"), w=420, a=170); d = ImageDraw.Draw(im)
    f = fit(d, "LIBERDADE", 600, 160)
    c["text"](im, (1265, 400), "LIBERDADE", f, GOLD, stroke=8, anchor="rs")
    return im


def thumb_c():
    a, b = base("thumb-C1"), base("thumb-C2")
    im = Image.new("RGB", (W, H)); im.paste(a.crop((0, 0, W // 2, H)), (0, 0)); im.paste(b.crop((W // 2, 0, W, H)), (W // 2, 0))
    d = ImageDraw.Draw(im); d.rectangle([W // 2 - 5, 0, W // 2 + 5, H], fill=(255, 255, 255))
    im = c["grad"](im, bottom=230, a=200)
    fs = c["sans"](150)
    c["text"](im, (W // 4, 690), "1776", fs, WHITE, stroke=10, anchor="ms")
    c["text"](im, (3 * W // 4, 690), "2026", fs, WHITE, stroke=10, anchor="ms")
    return im


os.makedirs(F, exist_ok=True); os.makedirs(D, exist_ok=True); ims = []
for letra, fn in (("A", thumb_a), ("B", thumb_b), ("C", thumb_c)):
    im = fn(); im.save(f"{F}/{letra}.jpg", quality=90, optimize=True); im.save(f"{D}/thumb-{letra}.jpg", quality=90, optimize=True); ims.append(im)
    print(letra, im.size, os.path.getsize(f"{D}/thumb-{letra}.jpg") // 1024, "KB")
cel = Image.new("RGB", (3 * 320 + 4 * 12, 180 + 24), (15, 15, 15))
for i, im in enumerate(ims): cel.paste(im.resize((320, 180), Image.LANCZOS), (12 + i * 332, 12))
cel.save("thumbs/prancha-celular.jpg", quality=90)
g = Image.new("RGB", (2 * 640, 2 * 360))
for i, im in enumerate(ims): g.paste(im.resize((640, 360), Image.LANCZOS), ((i % 2) * 640, (i // 2) * 360))
g.save("thumbs/prancha.jpg", quality=88)
