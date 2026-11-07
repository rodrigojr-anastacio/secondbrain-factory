"""Thumbs v3 do 003-ira: 3 estilos para o "Testar e comparar" (BRIEF-historia-003-thumbs-v3, 07/11/2026).
1 HiM fiel ao print: panorama da Praça Naqsh-e Jahan (Isfahan), sem boneco; "IRÃ" serifa preta gigante + "4200 a.C. – 2026" no céu.
2 bonecos: Dario piscando com o cavalo relinchando (hook) + "TRAPAÇA?" + "522 a.C." em pílula.
3 mapa: o império aquemênida brilhando em ouro do Egito à Índia, Dario abraçando o mapa + "METADE DO MUNDO?" + "500 a.C.".
Uso (pasta do vídeo 003-ira): ../../../../tools/.venv/bin/python entrega/thumbs-v3/compose_v3.py
(funções de texto e fontes de v2-amostras/thumbs/base/compose.py)"""
import os
from PIL import Image, ImageDraw, ImageFilter
src = open("v2-amostras/thumbs/base/compose.py").read().split("os.makedirs(V,exist_ok=True)")[0]
c = {"__file__": os.path.abspath("v2-amostras/thumbs/base/compose.py")}; exec(src, c)
GOLD, WHITE, BLACK = c["GOLD"], c["WHITE"], c["BLACK"]
D = "entrega/thumbs-v3"; B = f"{D}/base"


def base(n):
    return Image.open(f"{B}/{n}.jpg").convert("RGB").resize((1280, 720), Image.LANCZOS)


def fit(d, s, maxw, hi, lo=60, fn=None):
    fn = fn or c["caslon"]
    for sz in range(hi, lo, -2):
        f = fn(sz)
        if d.textlength(s, font=f) <= maxw: return f
    return fn(lo)


def grad_right(im, w=560, a=210):
    ov = Image.new("L", im.size, 0); d = ImageDraw.Draw(ov)
    for i in range(w): d.line([(1279 - i, 0), (1279 - i, 719)], fill=int(a * (1 - i / w)))
    return Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ov)


def mais_ceu(im, extra=110):
    """A base tem pouco céu: empurra a cena para baixo (corta o pé) e completa o topo com o degradê do céu,
    continuando a cor da 1ª linha (mediana, sem nuvens) e escurecendo de leve para cima; emenda de 40 px."""
    import numpy as np
    a = np.asarray(im).astype(float)
    c0 = np.median(a[0:6], axis=(0, 1)); c1 = np.median(a[30:36], axis=(0, 1))
    passo = (c0 - c1) / 30.0  # variação por linha no topo da base
    out = np.zeros_like(a); out[extra:] = a[:720 - extra]
    for y in range(extra):
        out[y] = np.clip(c0 + passo * (extra - y) * 0.6, 0, 255)
    for k in range(40):  # emenda: mistura a cor lisa com a base nas primeiras 40 linhas
        t = k / 39.0; y = extra + k
        out[y] = out[y] * t + out[extra - 1] * (1 - t)
    return Image.fromarray(out.astype("uint8"))


def t1():
    im = mais_ceu(base("t1-him-isfahan-2")); d = ImageDraw.Draw(im)
    cx = 985
    f = fit(d, "IRÃ", 520, 250)
    fd = c["sans"](60)
    glow = Image.new("L", im.size, 0); g = ImageDraw.Draw(glow)
    g.text((cx, 252), "IRÃ", font=f, fill=255, anchor="ms", stroke_width=14)
    g.text((cx, 336), "4200 a.C. – 2026", font=fd, fill=255, anchor="ms", stroke_width=12)
    glow = glow.filter(ImageFilter.GaussianBlur(6))
    im = Image.composite(Image.new("RGB", im.size, (235, 245, 252)), im, glow); d = ImageDraw.Draw(im)
    d.text((cx, 252), "IRÃ", font=f, fill=BLACK, anchor="ms")
    d.text((cx, 336), "4200 a.C. – 2026", font=fd, fill=BLACK, anchor="ms")
    return im


def t2():
    im = grad_right(c["grad"](base("t2-bonecos-cavalo-1"), bottom=200, a=150), w=560, a=170); d = ImageDraw.Draw(im)
    f = fit(d, "TRAPAÇA?", 640, 190)
    c["text"](im, (1262, 694), "TRAPAÇA?", f, GOLD, stroke=10, anchor="rs")
    c["pill"](im, 1110, 62, "522 a.C.", c["sans"](50))
    return im


def t3():
    im = c["grad"](base("t3-mapa-imperio-2"), bottom=290, a=235); d = ImageDraw.Draw(im)
    w1, w2 = "METADE", "DO MUNDO?"
    for sz in range(150, 80, -2):
        f = c["caslon"](sz); a = d.textlength(w1, font=f); b = d.textlength(w2, font=f)
        tot = a + b + 36
        if tot <= 1200: break
    x = (1280 - tot) / 2
    c["text"](im, (x, 696), w1, f, GOLD, stroke=9, anchor="ls"); x += a + 36
    c["text"](im, (x, 696), w2, f, WHITE, stroke=9, anchor="ls")
    c["pill"](im, 1130, 62, "500 a.C.", c["sans"](50))
    return im


T = [(t1, "thumb-1-him.jpg"), (t2, "thumb-2-bonecos.jpg"), (t3, "thumb-3-mapa.jpg")]
ims = []
for fn, nome in T:
    im = fn(); p = f"{D}/{nome}"; im.save(p, quality=90, optimize=True); ims.append(im)
    print(p, im.size, os.path.getsize(p) // 1024, "KB")
cel = Image.new("RGB", (3 * 320 + 4 * 12, 180 + 24), (15, 15, 15))
for i, im in enumerate(ims): cel.paste(im.resize((320, 180), Image.LANCZOS), (12 + i * 332, 12))
cel.save(f"{D}/prancha-celular.jpg", quality=90)
g = Image.new("RGB", (3 * 640, 360))
for i, im in enumerate(ims): g.paste(im.resize((640, 360), Image.LANCZOS), (i * 640, 0))
g.save(f"{D}/prancha.jpg", quality=88)
