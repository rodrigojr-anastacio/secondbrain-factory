"""Thumbs do 015-argentina (EMBALAGEM r5): A rosto-emocao "VALE NADA" + cinta 1.000.000; B conflito-xvy "QUEM PAGA?" + pílula 1946; C numero-estatistica "13 ZEROS".
Uso (pasta do vídeo): ../../../../tools/.venv/bin/python thumbs/compose.py"""
import os
from PIL import Image, ImageDraw
CP = os.path.abspath("../003-ira/v2-amostras/thumbs/base/compose.py")
src = open(CP).read().split("def t1")[0]
c = {"__file__": CP}; exec(src, c)
GOLD, WHITE, BLACK = c["GOLD"], c["WHITE"], c["BLACK"]
W, H = 1280, 720; B, F, D = "thumb-var", "thumb-var/final", "entrega"
def base(n): return Image.open(f"{B}/{n}.jpg").convert("RGB").resize((W, H), Image.LANCZOS)
def shade(im, y0, amax, x0=0):
    ov = Image.new("L", im.size, 0); d = ImageDraw.Draw(ov)
    for y in range(y0, H): d.line([(x0, y), (W, y)], fill=int(amax * ((y - y0) / (H - y0))))
    return Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ov)
def thumb_a():
    im = shade(base("thumb-A"), 380, 150, 560)
    # cinta de papel sobre o maço, com o número no código (≥ 25% da largura)
    cw, ch = 360, 96
    fita = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(fita)
    d.rounded_rectangle([0, 0, cw - 1, ch - 1], 8, fill=(250, 248, 240, 255), outline=(40, 30, 20, 255), width=5)
    f = c["sans"](72); d.text((cw // 2, ch // 2 + 2), "1.000.000", font=f, fill=(150, 20, 20, 255), anchor="mm")
    fita = fita.rotate(4, expand=True, resample=Image.BICUBIC)
    im.paste(fita, (255, 455), fita)
    c["text"](im, (1255, 600), "VALE", c["caslon"](100), WHITE, stroke=10, anchor="rd")
    c["text"](im, (1255, 705), "NADA", c["caslon"](100), GOLD, stroke=10, anchor="rd")
    return im
def thumb_b():
    im = shade(base("thumb-B"), 470, 190)
    c["pill"](im, W // 2, 52, "1946", c["sans"](60))
    x = c["text"](im, (W // 2, 700), "QUEM PAGA?", c["caslon"](112), WHITE, stroke=10, anchor="md")
    # "QUEM" em ouro: redesenha a primeira palavra
    f = c["caslon"](112); wq = ImageDraw.Draw(im).textlength("QUEM ", font=f); wt = ImageDraw.Draw(im).textlength("QUEM PAGA?", font=f)
    c["text"](im, (W // 2 - wt / 2, 700), "QUEM", f, GOLD, stroke=10, shadow=0, anchor="ld")
    return im
def thumb_c():
    im = base("thumb-C")
    c["text"](im, (50, 400), "13", c["caslon"](330), GOLD, stroke=14, anchor="ld")
    c["text"](im, (60, 570), "ZEROS", c["caslon"](170), WHITE, stroke=12, anchor="ld")
    return im
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
