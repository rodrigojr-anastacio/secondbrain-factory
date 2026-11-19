"""Thumbs do 013-uniao-sovietica (3 conceitos do EMBALAGEM.md r3): A rosto-emocao "NEM O POLITBURO" + pílula 1989; B objeto-simbolo "VAI QUE…";
C numero-estatistica "30 MIL / NA FILA". Uso (pasta do vídeo): ../../../../tools/.venv/bin/python thumbs/compose.py"""
import os
from PIL import Image, ImageDraw
CP = os.path.abspath("../003-ira/v2-amostras/thumbs/base/compose.py")
src = open(CP).read().split("def t1")[0]
c = {"__file__": CP}; exec(src, c)
GOLD, WHITE, BLACK = c["GOLD"], c["WHITE"], c["BLACK"]
W, H = 1280, 720; B, F, D = "thumb-var", "thumb-var/final", "entrega"
def base(n): return Image.open(f"{B}/{n}.jpg").convert("RGB").resize((W, H), Image.LANCZOS)
def grad_h(im, side, w, a):
    ov = Image.new("L", im.size, 0); d = ImageDraw.Draw(ov)
    for i in range(w):
        x = i if side == "l" else W - 1 - i
        d.line([(x, 0), (x, H - 1)], fill=int(a * (1 - i / w) ** 1.2))
    return Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ov)
def thumb_a():
    im = grad_h(base("thumb-A"), "r", 640, 200); d = ImageDraw.Draw(im)
    c["text"](im, (1250, 50), "NEM O", c["caslon"](96), WHITE, stroke=9, anchor="ra")
    c["text"](im, (1250, 155), "POLITBURO", c["caslon"](92), GOLD, stroke=9, anchor="ra")
    c["pill"](im, 1110, 640, "1989", c["sans"](60))
    return im
def thumb_b():
    im = grad_h(base("thumb-B"), "l", 640, 190)
    c["text"](im, (50, 90), "VAI", c["caslon"](210), WHITE, stroke=11, anchor="la")
    c["text"](im, (50, 300), "QUE…", c["caslon"](210), GOLD, stroke=11, anchor="la")
    return im
def thumb_c():
    im = grad_h(base("thumb-C"), "l", 700, 120)
    c["text"](im, (40, 40), "30 MIL", c["caslon"](220), GOLD, stroke=12, anchor="la")
    c["text"](im, (50, 290), "NA FILA", c["caslon"](135), WHITE, stroke=11, anchor="la")
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
