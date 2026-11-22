"""Thumbs do 016-espanha (EMBALAGEM r3): A rosto-emocao "REI DAS ESPANHAS"; B conflito-xvy "CASTELA × NAVARRA"; C objeto-simbolo pílula "1469".
Uso (pasta do vídeo): ../../../../tools/.venv/bin/python thumbs/compose.py"""
import os
from PIL import Image, ImageDraw
CP = os.path.abspath("../003-ira/v2-amostras/thumbs/base/compose.py")
src = open(CP).read().split("def t1")[0]
c = {"__file__": CP}; exec(src, c)
GOLD, WHITE, BLACK = c["GOLD"], c["WHITE"], c["BLACK"]
YEL = (247, 194, 27)
W, H = 1280, 720; B, F, D = "thumb-var", "thumb-var/final", "entrega"
def base(n): return Image.open(f"{B}/{n}.jpg").convert("RGB").resize((W, H), Image.LANCZOS)
def grad_v(im, a, h0):
    ov = Image.new("L", im.size, 0); d = ImageDraw.Draw(ov)
    for y in range(h0, H): d.line([(0, y), (W, y)], fill=int(a * ((y - h0) / (H - h0)) ** 1.1))
    return Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ov)
def thumb_a():
    im = base("thumb-A")
    c["text"](im, (1255, 250), "REI DAS", c["caslon"](100), WHITE, stroke=10, anchor="rd")
    c["text"](im, (1255, 380), "ESPANHAS", c["caslon"](112), GOLD, stroke=11, anchor="rd")
    return im
def thumb_b():
    im = grad_v(base("thumb-B"), 225, 450)
    f = c["sans"](112); y = 690
    parts = [("CASTELA", GOLD), (" × ", WHITE), ("NAVARRA", WHITE)]
    tot = sum(f.getlength(t) for t, _ in parts); x = (W - tot) / 2
    for t, col in parts:
        c["text"](im, (x, y), t, f, col, stroke=10, anchor="ld"); x += f.getlength(t)
    return im
def thumb_c():
    im = base("thumb-C"); d = ImageDraw.Draw(im); f = c["sans"](150); t = "1469"
    bb = d.textbbox((0, 0), t, font=f); w, h = bb[2] - bb[0], bb[3] - bb[1]
    x0, y0 = 45, 270
    d.rounded_rectangle((x0, y0, x0 + w + 80, y0 + h + 90), 28, fill=YEL, outline=BLACK, width=10)
    d.text((x0 + 40 - bb[0], y0 + 35 - bb[1]), t, font=f, fill=BLACK)
    return im
os.makedirs(F, exist_ok=True); ims = []
for l, fn in (("A", thumb_a), ("B", thumb_b), ("C", thumb_c)):
    im = fn(); im.save(f"{F}/{l}.jpg", quality=90, optimize=True); im.save(f"{D}/thumb-{l}.jpg", quality=90, optimize=True); ims.append(im)
    print(l, im.size, os.path.getsize(f"{D}/thumb-{l}.jpg") // 1024, "KB")
cel = Image.new("RGB", (3 * 320 + 4 * 12, 204), (15, 15, 15))
for i, im in enumerate(ims): cel.paste(im.resize((320, 180), Image.LANCZOS), (12 + i * 332, 12))
cel.save("thumbs/prancha-celular.jpg", quality=90)
g = Image.new("RGB", (3 * 640, 360))
for i, im in enumerate(ims): g.paste(im.resize((640, 360), Image.LANCZOS), (i * 640, 0))
g.save("thumbs/prancha.jpg", quality=88)
