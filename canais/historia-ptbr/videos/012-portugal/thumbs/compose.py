"""Thumbs do 012-portugal (3 conceitos do EMBALAGEM.md r2): A rosto-emocao "CADÊ?"; B objeto-simbolo "700 ANOS" (P e E gravados no código);
C mapa-lugar/escala "PERNAMBUCO É MAIOR" (silhuetas de thumbs/escala.py + bonequinho recortado). Uso (pasta do vídeo): ../../../../tools/.venv/bin/python thumbs/compose.py"""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFilter
CP = os.path.abspath("../003-ira/v2-amostras/thumbs/base/compose.py")
src = open(CP).read().split("def t1")[0]
c = {"__file__": CP}; exec(src, c)
GOLD, WHITE, BLACK = c["GOLD"], c["WHITE"], c["BLACK"]
W, H = 1280, 720; B, F, D = "thumb-var", "thumb-var/final", "entrega"

def base(n): return Image.open(f"{B}/{n}.jpg").convert("RGB").resize((W, H), Image.LANCZOS)
def fit(d, s, maxw, hi, lo=50, fn="caslon"):
    for sz in range(hi, lo, -2):
        if d.textlength(s, font=c[fn](sz)) <= maxw: return c[fn](sz)
    return c[fn](lo)
def escurece_direita(im, w=520, a=215):
    ov = Image.new("L", im.size, 0); d = ImageDraw.Draw(ov)
    for i in range(w): d.line([(W - 1 - i, 0), (W - 1 - i, H - 1)], fill=int(a * (1 - i / w) ** 1.2))
    return Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ov)

def thumb_a():
    im = escurece_direita(base("thumb-A")); d = ImageDraw.Draw(im)
    f = fit(d, "CADÊ?", 520, 230)
    c["text"](im, (1255, 430), "CADÊ?", f, GOLD, stroke=10, anchor="rs")
    return im

def grava(im, ch, cx, cy, size):
    """letra gravada na pedra: sombra escura deslocada + realce claro embaixo (sem pedir letra à IA)."""
    f = c["caslon"](size); d = ImageDraw.Draw(im)
    d.text((cx + 3, cy + 4), ch, font=f, fill=(235, 235, 230), anchor="mm")
    d.text((cx, cy), ch, font=f, fill=(58, 58, 60), anchor="mm")

def thumb_b():
    im = base("thumb-B"); d = ImageDraw.Draw(im)
    # face frontal do marco (x ~ 310-570, y ~ 150-520 em 1280x720): "P" | "E" com um sulco vertical entre elas
    d.line([(452, 250), (452, 470)], fill=(95, 95, 98), width=4)
    grava(im, "P", 385, 360, 150); grava(im, "E", 520, 360, 150)
    im = escurece_direita(im, w=420, a=120); d = ImageDraw.Draw(im)
    f = fit(d, "700 ANOS", 560, 190)
    c["text"](im, (1255, 330), "700 ANOS", f, GOLD, stroke=9, anchor="rs")
    return im

def thumb_c():
    im = Image.open("thumbs/escala-base.png").convert("RGB").crop((60, 100, 1340, 820)); im = im.resize((W, H))
    man = Image.open(f"{B}/thumb-C-man.jpg").convert("RGB"); a = np.array(man).astype(int)
    mask = ((a[..., 0] > 200) & (a[..., 2] > 200) & (a[..., 1] < 90)).astype(np.uint8) * 255
    mk = Image.fromarray(255 - mask).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    bb = mk.point(lambda v: 255 if v > 128 else 0).getbbox(); man.putalpha(mk); man = man.crop(bb)
    mh = 190; man = man.resize((int(man.width * mh / man.height), mh), Image.LANCZOS)
    # Portugal (ouro) em coordenadas do recorte: x 597-775 → (x-60)*1280/1280; y (274-630)-100
    im.paste(man, (int(626 - man.width / 2), 400 - mh), man)
    d = ImageDraw.Draw(im)
    f = c["sans"](76)
    c["text"](im, (40, 50), "PERNAMBUCO", f, WHITE, stroke=8, shadow=7, anchor="la")
    c["text"](im, (40, 140), "É MAIOR", f, WHITE, stroke=8, shadow=7, anchor="la")
    return im

os.makedirs(F, exist_ok=True); os.makedirs(D, exist_ok=True); ims = []
for letra, fn in (("A", thumb_a), ("B", thumb_b), ("C", thumb_c)):
    im = fn(); im.save(f"{F}/{letra}.jpg", quality=90, optimize=True); im.save(f"{D}/thumb-{letra}.jpg", quality=90, optimize=True); ims.append(im)
    print(letra, im.size, os.path.getsize(f"{D}/thumb-{letra}.jpg") // 1024, "KB")
cel = Image.new("RGB", (3 * 320 + 4 * 12, 180 + 24), (15, 15, 15))
for i, im in enumerate(ims): cel.paste(im.resize((320, 180), Image.LANCZOS), (12 + i * 332, 12))
cel.save("thumbs/prancha-celular.jpg", quality=90)
g = Image.new("RGB", (3 * 640, 360))
for i, im in enumerate(ims): g.paste(im.resize((640, 360), Image.LANCZOS), (i * 640, 0))
g.save("thumbs/prancha.jpg", quality=88)
