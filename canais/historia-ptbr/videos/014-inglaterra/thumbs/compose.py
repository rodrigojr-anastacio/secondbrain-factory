"""Thumbs do 014-inglaterra (3 conceitos do EMBALAGEM.md r3): A rosto-emocao "MINHA!"; B cena-acao rótulo "NATAL DE 1066"; C documento-evidencia "O PREÇO" (marcador).
Uso (pasta do vídeo): ../../../../tools/.venv/bin/python thumbs/compose.py"""
import os
from PIL import Image, ImageDraw
CP = os.path.abspath("../003-ira/v2-amostras/thumbs/base/compose.py")
src = open(CP).read().split("def t1")[0]
c = {"__file__": CP}; exec(src, c)
GOLD, WHITE, BLACK = c["GOLD"], c["WHITE"], c["BLACK"]
RED = (214, 30, 30)
W, H = 1280, 720; B, F, D = "thumb-var", "thumb-var/final", "entrega"
def base(n): return Image.open(f"{B}/{n}.jpg").convert("RGB").resize((W, H), Image.LANCZOS)
def grad_v(im, a, h0):
    ov = Image.new("L", im.size, 0); d = ImageDraw.Draw(ov)
    for y in range(h0, H): d.line([(0, y), (W, y)], fill=int(a * ((y - h0) / (H - h0)) ** 1.1))
    return Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ov)
def thumb_a():
    im = grad_v(base("thumb-A"), 150, 380)
    c["text"](im, (1250, 705), "MINHA!", c["caslon"](160), GOLD, stroke=11, anchor="rd")
    return im
def thumb_b():
    im = grad_v(base("thumb-B"), 215, 470)
    c["text"](im, (40, 700), "NATAL DE 1066", c["sans"](118), WHITE, stroke=11, anchor="ld")
    return im
def thumb_c():
    im = base("thumb-C")
    f = c["sans"](185); t = "O PREÇO"
    lay = Image.new("RGBA", (W, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((W // 2, 165), t, font=f, fill=RED, anchor="mm", stroke_width=16, stroke_fill=WHITE)
    lay = lay.rotate(5, resample=Image.BICUBIC, center=(W // 2, 165))
    im.paste(lay, (120, 20), lay)
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
