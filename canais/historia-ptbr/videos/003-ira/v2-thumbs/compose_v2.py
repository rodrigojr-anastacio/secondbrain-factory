"""Thumbs v2 do 003 (padrão COROA × TURBANTE aprovado pelo Rodrigo em 05/11/2026): conflito cara a cara, bonequinhos com raiva,
raio no meio, datas em pílula no topo e 2 palavras grandes embaixo (Libre Caslon 700, a 1ª em ouro, a 2ª em branco).
Uso (pasta do vídeo): tools/.venv/bin/python v2-thumbs/compose_v2.py"""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, "v2-amostras/thumbs/base")
import importlib.util
spec = importlib.util.spec_from_file_location("c", "v2-amostras/thumbs/base/compose.py")
src = open("v2-amostras/thumbs/base/compose.py").read().split("os.makedirs(V,exist_ok=True)")[0]   # só as funções
c = {"__file__": os.path.abspath("v2-amostras/thumbs/base/compose.py")}; exec(src, c)
GOLD, WHITE = c["GOLD"], c["WHITE"]
def thumb(base, w1, w2, datas, saida):
    im = Image.open(f"v2-thumbs/base/{base}.jpg").convert("RGB").resize((1280, 720), Image.LANCZOS)
    im = c["grad"](im, bottom=300, a=230)
    d = ImageDraw.Draw(im); fx = c["sans"](90)
    for sz in range(150, 80, -2):
        f = c["caslon"](sz); a = d.textlength(w1, font=f); b = d.textlength(w2, font=f); wx = d.textlength("×", font=fx)
        tot = a + b + wx + 60
        if tot <= 1200: break
    x = (1280 - tot) / 2
    c["text"](im, (x, 696), w1, f, GOLD, stroke=9, anchor="ls"); x += a + 30
    c["text"](im, (x, 684), "×", fx, WHITE, stroke=7, anchor="ls"); x += wx + 30
    c["text"](im, (x, 696), w2, f, WHITE, stroke=9, anchor="ls")
    c["pill"](im, 640, 58, datas, c["sans"](52))
    im.save(saida, quality=90, optimize=True); print(saida, os.path.getsize(saida) // 1024, "KB", sz)
    return im
T = [("t1-coroa-turbante-2", "COROA", "TURBANTE", "1891 · 1979", "entrega/thumb-1-coroa-turbante.jpg"),
     ("t2-persia-roma-1", "PÉRSIA", "ROMA", "260 d.C.", "entrega/thumb-2-persia-roma.jpg"),
     ("t3-petroleo-cia-1", "PETRÓLEO", "CIA", "1953", "entrega/thumb-3-petroleo-cia.jpg")]
ims = [thumb(*t) for t in T]
cel = Image.new("RGB", (3 * 320 + 4 * 12, 180 + 24), (15, 15, 15))
for i, im in enumerate(ims): cel.paste(im.resize((320, 180), Image.LANCZOS), (12 + i * 332, 12))
cel.save("v2-thumbs/prancha-celular.jpg", quality=90)
g = Image.new("RGB", (3 * 640, 360))
for i, im in enumerate(ims): g.paste(im.resize((640, 360), Image.LANCZOS), (i * 640, 0))
g.save("v2-thumbs/prancha.jpg", quality=88)
