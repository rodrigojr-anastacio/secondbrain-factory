"""Thumbs do 017-cuba (EMBALAGEM r3): A rosto-emocao "SEM COMPRADOR"; B numero-estatistica "5× O PREÇO"; C mapa-lugar sem texto.
Uso (pasta do vídeo): ../../../../tools/.venv/bin/python thumbs/compose.py"""
import os
from PIL import Image, ImageDraw
CP = os.path.abspath("../003-ira/v2-amostras/thumbs/base/compose.py")
src = open(CP).read().split("def t1")[0]
c = {"__file__": CP}; exec(src, c)
GOLD, WHITE, BLACK = c["GOLD"], c["WHITE"], c["BLACK"]
W, H = 1280, 720; B, F, D = "thumb-var", "thumb-var/final", "entrega"
def base(n): return Image.open(f"{B}/{n}.jpg").convert("RGB").resize((W, H), Image.LANCZOS)
def thumb_a():
    im = base("thumb-A")
    ov = Image.new("L", im.size, 0); d = ImageDraw.Draw(ov)
    for y in range(380, H): d.line([(560, y), (W, y)], fill=int(150 * ((y - 380) / (H - 380))))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ov)
    c["text"](im, (1255, 600), "SEM", c["caslon"](92), GOLD, stroke=10, anchor="rd")
    c["text"](im, (1255, 700), "COMPRADOR", c["caslon"](84), WHITE, stroke=10, anchor="rd")
    return im
def thumb_b():
    im = base("thumb-B")
    c["text"](im, (40, 500), "5×", c["sans"](400), GOLD, stroke=18, anchor="ld")
    c["text"](im, (60, 690), "O PREÇO", c["sans"](130), WHITE, stroke=11, anchor="ld")
    return im
def thumb_c(): return base("thumb-C")
os.makedirs(F, exist_ok=True); os.makedirs(D, exist_ok=True); ims = []
for l, fn in (("A", thumb_a), ("B", thumb_b), ("C", thumb_c)):
    im = fn(); im.save(f"{F}/{l}.jpg", quality=88, optimize=True); im.save(f"{D}/thumb-{l}.jpg", quality=88, optimize=True); ims.append(im)
    print(l, im.size, os.path.getsize(f"{D}/thumb-{l}.jpg") // 1024, "KB")
cel = Image.new("RGB", (3 * 320 + 4 * 12, 204), (15, 15, 15))
for i, im in enumerate(ims): cel.paste(im.resize((320, 180), Image.LANCZOS), (12 + i * 332, 12))
cel.save("thumbs/prancha-celular.jpg", quality=90)
g = Image.new("RGB", (3 * 640, 360))
for i, im in enumerate(ims): g.paste(im.resize((640, 360), Image.LANCZOS), (i * 640, 0))
g.save("thumbs/prancha.jpg", quality=88)
