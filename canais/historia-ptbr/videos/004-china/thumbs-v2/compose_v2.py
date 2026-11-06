"""Thumbs v2 do 004-china: 3 estilos para o "Testar e comparar" (BRIEF-historia-004-thumbs-v2, 06/11/2026).
4 bonecos: Qin assustado com a pílula de mercúrio + "IMORTAL?"   5 HiM: personagem + panorama + NOME preto + datas no céu
6 túmulo: porta do túmulo fechado com mercúrio vazando + "NUNCA ABERTO".
Uso (pasta do vídeo): tools/.venv/bin/python thumbs-v2/compose_v2.py   (funções de texto de thumbs/base/compose.py)"""
import os
from PIL import Image, ImageDraw, ImageFilter
src = open("thumbs/base/compose.py").read().split("os.makedirs(V,exist_ok=True)")[0]
c = {"__file__": os.path.abspath("thumbs/base/compose.py")}; exec(src, c)
GOLD, WHITE, BLACK = c["GOLD"], c["WHITE"], c["BLACK"]
B = "thumbs-v2/base"; OUT = "entrega/thumbs-v2"; os.makedirs(OUT, exist_ok=True)

def base(n, flip=False):
    im = Image.open(f"{B}/{n}.jpg").convert("RGB").resize((1280, 720), Image.LANCZOS)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im

def grad_right(im, w=560, a=210):
    ov = Image.new("L", im.size, 0); d = ImageDraw.Draw(ov)
    for i in range(w): d.line([(1279 - i, 0), (1279 - i, 719)], fill=int(a * (1 - i / w)))
    return Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ov)

def fit(d, s, maxw, hi, lo=60, fn=None):
    fn = fn or c["caslon"]
    for sz in range(hi, lo, -2):
        f = fn(sz)
        if d.textlength(s, font=f) <= maxw: return f
    return fn(lo)

def t4():
    im = grad_right(base("t4-bonecos-imortal-b-2"), w=520, a=200); d = ImageDraw.Draw(im)
    f = fit(d, "IMORTAL?", 650, 190)
    c["text"](im, (1262, 694), "IMORTAL?", f, GOLD, stroke=10, anchor="rs")
    c["pill"](im, 1135, 62, "210 a.C.", c["sans"](50))
    return im

def t5():
    im = base("t5-him-panorama-1"); d = ImageDraw.Draw(im)
    # padrão HiM: NOME em serifa preta gigante + datas em sans preta, no céu livre do canto superior direito
    f = fit(d, "CHINA", 560, 230)
    glow = Image.new("L", im.size, 0); g = ImageDraw.Draw(glow)
    g.text((930, 205), "CHINA", font=f, fill=255, anchor="ms", stroke_width=14)
    fd = c["sans"](64); g.text((930, 300), "1600 a.C. – 2026", font=fd, fill=255, anchor="ms", stroke_width=12)
    glow = glow.filter(ImageFilter.GaussianBlur(6))
    im = Image.composite(Image.new("RGB", im.size, (235, 245, 252)), im, glow); d = ImageDraw.Draw(im)
    d.text((930, 205), "CHINA", font=f, fill=BLACK, anchor="ms")
    d.text((930, 300), "1600 a.C. – 2026", font=fd, fill=BLACK, anchor="ms")
    return im

def t6():
    im = c["grad"](base("t6-tumulo-fechado-1"), bottom=290, a=235); d = ImageDraw.Draw(im)
    fa = c["caslon"](150)
    for sz in range(160, 80, -2):
        fa = c["caslon"](sz)
        tot = d.textlength("NUNCA", font=fa) + d.textlength("ABERTO", font=fa) + 40
        if tot <= 1200: break
    x = (1280 - tot) / 2
    c["text"](im, (x, 696), "NUNCA", fa, GOLD, stroke=9, anchor="ls"); x += d.textlength("NUNCA", font=fa) + 40
    c["text"](im, (x, 696), "ABERTO", fa, WHITE, stroke=9, anchor="ls")
    c["pill"](im, 640, 58, "2.200 ANOS", c["sans"](50))
    return im

T = [(t4, "thumb-4-bonecos.jpg"), (t5, "thumb-5-him.jpg"), (t6, "thumb-6-tumulo.jpg")]
ims = []
for fn, nome in T:
    im = fn(); p = f"{OUT}/{nome}"; im.save(p, quality=90, optimize=True); ims.append(im)
    print(p, im.size, os.path.getsize(p) // 1024, "KB")
cel = Image.new("RGB", (3 * 320 + 4 * 12, 180 + 24), (15, 15, 15))
for i, im in enumerate(ims): cel.paste(im.resize((320, 180), Image.LANCZOS), (12 + i * 332, 12))
cel.save("thumbs-v2/prancha-celular.jpg", quality=90)
g = Image.new("RGB", (3 * 640, 360))
for i, im in enumerate(ims): g.paste(im.resize((640, 360), Image.LANCZOS), (i * 640, 0))
g.save("thumbs-v2/prancha.jpg", quality=88)
