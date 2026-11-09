"""Thumbs do 007-russia (padrão de entrega do 005, biblia/thumb.md): 1 bonecos (o viking recebe a coroa, 862), 2 HiM (Pedro, o Grande), 3 mito do inverno (Napoleão, 1812). Adaptado de 006-roma/thumbs/compose.py.
Uso (pasta do vídeo): ../../../../tools/.venv/bin/python thumbs/compose.py
Funções de texto e fontes de 003-ira/v2-amostras/thumbs/base/compose.py (mesmo código do compose_v3 do Irã)."""
import os
from PIL import Image, ImageDraw, ImageFilter
CP = os.path.abspath("../003-ira/v2-amostras/thumbs/base/compose.py")
src = open(CP).read().split("os.makedirs(V,exist_ok=True)")[0]
c = {"__file__": CP}; exec(src, c)
GOLD, WHITE, BLACK = c["GOLD"], c["WHITE"], c["BLACK"]
B, D = "thumbs/base", "entrega"


def base(n): return Image.open(f"{B}/{n}.jpg").convert("RGB").resize((1280, 720), Image.LANCZOS)


def fit(d, s, maxw, hi, lo=60, fn=None):
    fn = fn or c["caslon"]
    for sz in range(hi, lo, -2):
        if d.textlength(s, font=fn(sz)) <= maxw: return fn(sz)
    return fn(lo)


def grad_right(im, w=560, a=210):
    ov = Image.new("L", im.size, 0); d = ImageDraw.Draw(ov)
    for i in range(w): d.line([(1279 - i, 0), (1279 - i, 719)], fill=int(a * (1 - i / w)))
    return Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ov)


def t1():   # bonecos: o viking pega a coroa oferecida pelo ancião eslavo (862)
    im = grad_right(c["grad"](base("t1-bonecos-1"), bottom=230, a=160), w=560, a=170); d = ImageDraw.Draw(im)
    f1 = fit(d, "UM VIKING", 560, 150); f2 = fit(d, "NO TRONO?", 600, 150)
    c["text"](im, (1255, 520), "UM VIKING", f1, WHITE, stroke=10, anchor="rs")
    c["text"](im, (1262, 694), "NO TRONO?", f2, GOLD, stroke=10, anchor="rs")
    c["pill"](im, 1140, 62, "862", c["sans"](54))
    return im


def t2():   # HiM: panorama claro da Rússia + bonequinho Pedro, o Grande, com contorno de adesivo + RÚSSIA no céu
    im = base("t2-him-1")
    cx = 960; f = fit(ImageDraw.Draw(im), "RÚSSIA", 560, 190); fd = c["sans"](54)
    glow = Image.new("L", im.size, 0); g = ImageDraw.Draw(glow)
    g.text((cx, 175), "RÚSSIA", font=f, fill=255, anchor="ms", stroke_width=14)
    g.text((cx, 245), "862 – 2026", font=fd, fill=255, anchor="ms", stroke_width=12)
    glow = glow.filter(ImageFilter.GaussianBlur(6))
    im = Image.composite(Image.new("RGB", im.size, (235, 245, 252)), im, glow); d = ImageDraw.Draw(im)
    d.text((cx, 175), "RÚSSIA", font=f, fill=BLACK, anchor="ms")
    d.text((cx, 245), "862 – 2026", font=fd, fill=BLACK, anchor="ms")
    return im


def t3():   # mito: Napoleão congelando, o "General Inverno" soprando, Moscou em chamas (o vídeo responde: quem venceu foi a distância)
    im = grad_right(c["grad"](base("t3-inverno-3"), bottom=230, a=170), w=520, a=170); d = ImageDraw.Draw(im)
    f1 = fit(d, "O INVERNO", 520, 150); f2 = fit(d, "VENCEU?", 520, 170)
    c["text"](im, (1255, 520), "O INVERNO", f1, WHITE, stroke=10, anchor="rs")
    c["text"](im, (1262, 694), "VENCEU?", f2, GOLD, stroke=10, anchor="rs")
    c["pill"](im, 1130, 62, "1812", c["sans"](54))
    return im


T = [(t1, "thumb-1-bonecos.jpg"), (t2, "thumb-2-him.jpg"), (t3, "thumb-3-inverno.jpg")]
os.makedirs(D, exist_ok=True); ims = []
for fn, nome in T:
    im = fn(); p = f"{D}/{nome}"; im.save(p, quality=90, optimize=True); ims.append(im)
    print(p, im.size, os.path.getsize(p) // 1024, "KB")
cel = Image.new("RGB", (3 * 320 + 4 * 12, 180 + 24), (15, 15, 15))
for i, im in enumerate(ims): cel.paste(im.resize((320, 180), Image.LANCZOS), (12 + i * 332, 12))
cel.save("thumbs/prancha-celular.jpg", quality=90)
g = Image.new("RGB", (2 * 640, 2 * 360))
for i, im in enumerate(ims): g.paste(im.resize((640, 360), Image.LANCZOS), ((i % 2) * 640, (i // 2) * 360))
g.save("thumbs/prancha.jpg", quality=88)
