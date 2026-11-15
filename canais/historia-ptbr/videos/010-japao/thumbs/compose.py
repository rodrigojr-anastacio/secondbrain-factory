"""Thumbs do 010-japao (conceito do EMBALAGEM.md: bonequinho com tocha no muro olhando o tufão por cima do ombro; "SÓ SORTE?" + pílula 1281).
A = base t-a-1 + "SÓ SORTE?" (T1); B = enquadramento mais fechado t-b-1 + "SÓ SORTE?" (T2); C = expressão de grito t-c-1 + "FOI O VENTO?".
Adaptado de 009-alemanha/thumbs/compose.py. Uso (pasta do vídeo): ../../../../tools/.venv/bin/python thumbs/compose.py"""
import os
from PIL import Image, ImageDraw
CP = os.path.abspath("../003-ira/v2-amostras/thumbs/base/compose.py")
src = open(CP).read().split("os.makedirs(V,exist_ok=True)")[0]
c = {"__file__": CP}; exec(src, c)
GOLD, WHITE = c["GOLD"], c["WHITE"]
B, D = "thumbs/base", "entrega"


def base(n): return Image.open(f"{B}/{n}.jpg").convert("RGB").resize((1280, 720), Image.LANCZOS)


def fit(d, s, maxw, hi, lo=60):
    for sz in range(hi, lo, -2):
        if d.textlength(s, font=c["caslon"](sz)) <= maxw: return c["caslon"](sz)
    return c["caslon"](lo)


def grad_right(im, w=620, a=200):
    ov = Image.new("L", im.size, 0); d = ImageDraw.Draw(ov)
    for i in range(w): d.line([(1279 - i, 0), (1279 - i, 719)], fill=int(a * (1 - i / w)))
    return Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ov)


def thumb(nome, l1, l2):
    im = c["grad"](base(nome), bottom=230, a=190); d = ImageDraw.Draw(im)
    f1 = fit(d, l1, 560, 150) if l1 else None; f2 = fit(d, l2, 640, 175)
    if l1:
        c["text"](im, (1255, 465), l1, f1, GOLD, stroke=10, anchor="rs")
        c["text"](im, (1255, 655), l2, f2, WHITE, stroke=10, anchor="rs")
    else:
        c["text"](im, (1255, 655), l2, f2, WHITE, stroke=10, anchor="rs")
    c["pill"](im, 640, 62, "1281", c["sans"](54))
    return im


T = [("t-a-1", "SÓ", "SORTE?", "thumb-A.jpg"), ("t-b-1", "SÓ", "SORTE?", "thumb-B.jpg"), ("t-c-1", "FOI O", "VENTO?", "thumb-C.jpg")]
os.makedirs(D, exist_ok=True); ims = []
for n, l1, l2, out in T:
    im = thumb(n, l1, l2); p = f"{D}/{out}"; im.save(p, quality=90, optimize=True); ims.append(im)
    print(p, im.size, os.path.getsize(p) // 1024, "KB")
cel = Image.new("RGB", (3 * 320 + 4 * 12, 180 + 24), (15, 15, 15))
for i, im in enumerate(ims): cel.paste(im.resize((320, 180), Image.LANCZOS), (12 + i * 332, 12))
cel.save("thumbs/prancha-celular.jpg", quality=90)
g = Image.new("RGB", (2 * 640, 2 * 360))
for i, im in enumerate(ims): g.paste(im.resize((640, 360), Image.LANCZOS), ((i % 2) * 640, (i // 2) * 360))
g.save("thumbs/prancha.jpg", quality=88)
