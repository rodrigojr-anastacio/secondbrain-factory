"""Em Relevo (ajuste 14/11/2026): thumbs El Niño 2026 e Sul do Brasil sobre relevo/satélite REAL, stills do próprio vídeo longo-02
(Remotion LongoV2 soMapa=true, t=250 s e t=30 s; NASA Blue Marble + relevo ETOPO + anomalia NOAA OISST). Custo US$ 0.
Uso (raiz): tools/.venv/bin/python pesquisa/reembalagem-2026-11-14/thumbs/emrelevo2.py [nino|sul]"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
sys.path.insert(0, os.path.dirname(__file__))
from emrelevo import anton, texto, bezier, vinheta, YEL, CORAL, OUT
ST = f"{OUT}/stills"


def glow_line(im, pts, w, cor, glow=(255, 220, 80), gl=26, borda=(30, 20, 10)):
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line(pts, fill=glow + (200,), width=w + 34, joint="curve"); L = L.filter(ImageFilter.GaussianBlur(gl))
    im = Image.alpha_composite(im.convert("RGBA"), L)
    S = Image.new("RGBA", im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(S)
    ds.line([(x + 7, y + 9) for x, y in pts], fill=(0, 0, 0, 150), width=w + 8, joint="curve"); S = S.filter(ImageFilter.GaussianBlur(7))
    im = Image.alpha_composite(im, S); d = ImageDraw.Draw(im)
    d.line(pts, fill=borda, width=w + 10, joint="curve"); d.line(pts, fill=cor, width=w, joint="curve")
    return im


def cabeca(im, p0, p1, tam, cor, borda=(30, 20, 10)):
    d = ImageDraw.Draw(im); a = math.atan2(p1[1] - p0[1], p1[0] - p0[0]); x, y = p1
    tri = [(x + math.cos(a) * tam, y + math.sin(a) * tam), (x + math.cos(a + 2.35) * tam, y + math.sin(a + 2.35) * tam), (x + math.cos(a - 2.35) * tam, y + math.sin(a - 2.35) * tam)]
    d.polygon([(px + 6, py + 8) for px, py in tri], fill=(0, 0, 0)); d.polygon(tri, fill=cor, outline=borda, width=6)


def termometro(im, bx, by, H=330, W=64):
    d = ImageDraw.Draw(im); top = by - H
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((bx - 80, by - 22, bx + 80, by + 28), fill=(0, 0, 0, 170)); sh = sh.filter(ImageFilter.GaussianBlur(9))
    im = Image.alpha_composite(im.convert("RGBA"), sh); d = ImageDraw.Draw(im)
    d.rounded_rectangle((bx - W / 2 + 7, top + 7, bx + W / 2 + 7, by - 12 + 7), radius=W // 2, fill=(0, 0, 0))
    d.rounded_rectangle((bx - W / 2, top, bx + W / 2, by - 12), radius=W // 2, fill=(250, 250, 250), outline=(20, 20, 30), width=5)
    d.rounded_rectangle((bx - 10, top + 44, bx + 10, by - 30), radius=10, fill=(214, 28, 40))
    d.ellipse((bx - 38, by - 66, bx + 38, by + 10), fill=(214, 28, 40), outline=(20, 20, 30), width=5)
    d.ellipse((bx - 22, by - 52, bx - 6, by - 36), fill=(255, 160, 160))
    for k in range(1, 6): yy = top + 50 + k * 42; d.line((bx + 14, yy, bx + 26, yy), fill=(60, 60, 80), width=4)
    return im


def moldura(src, box, cor=(255, 255, 255)):
    w, h = box[2] - box[0], box[3] - box[1]
    return src.crop(box)


def nino():
    base = Image.open(f"{ST}/video-t250.jpg").resize((1280, 720), Image.LANCZOS)
    # cobre a faixa de rodapé do mapa (fonte/crédito) esticando o relevo logo acima
    im = base.convert("RGBA")
    # inset: satélite real da América do Sul (still t=30), recortado
    sa = Image.open(f"{ST}/video-t30.jpg").crop((830, 80, 1650, 900)).resize((300, 300), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (300, 300), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 299, 299), radius=34, fill=255)
    X, Y = 940, 380
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((X + 8, Y + 12, X + 308, Y + 312), radius=34, fill=(0, 0, 0, 190)); sh = sh.filter(ImageFilter.GaussianBlur(10))
    im = Image.alpha_composite(im, sh); im.paste(sa, (X, Y), m)
    d = ImageDraw.Draw(im); d.rounded_rectangle((X, Y, X + 300, Y + 300), radius=34, outline=(255, 255, 255), width=8)
    # termômetro cravado no Niño 3.4 (língua quente, centro ~ (520, 330))
    im = termometro(im, 745, 420)
    # seta amarela do termômetro até o recorte do Brasil
    p0 = (800, 270); p2 = (X - 14, Y + 100); p1 = (930, 250)
    pts = bezier(p0, p1, p2, 40)
    im = glow_line(im, pts, 30, YEL); cabeca(im, pts[-4], pts[-1], 62, YEL)
    f = anton(190); d = ImageDraw.Draw(im)
    x = texto(im, (40, 695), [("SÓ ", (255, 255, 255))], f, stroke=9)
    texto(im, (x, 695), [("2", YEL)], f, stroke=9)
    f2 = anton(150); texto(im, (x + d.textlength("2", font=f) + 20, 695), [("°C?", YEL)], f2, stroke=9)
    return vinheta(im.convert("RGB"), 0.25)


def sul():
    # still t=30 s: Andes extrudados (parede rosa) + satélite; recorte 16:9 com o Sul embaixo à direita
    src = Image.open(f"{ST}/video-t30.jpg")
    im = src.crop((200, 340, 1480, 1060)).convert("RGBA")
    W, H = im.size
    # fita ciano (rio de umidade): da Amazônia, rente à encosta dos Andes, até o Sul
    rota = [(700, 0), (660, 120), (650, 250), (690, 340), (790, 400), (940, 440), (1090, 450)]
    ar = np.array(rota, float); n = 400; u = np.linspace(0, 1, len(rota)); uu = np.linspace(0, 1, n)
    from numpy.polynomial import polynomial as _p
    xs = np.interp(uu, u, ar[:, 0]); ys = np.interp(uu, u, ar[:, 1]); k = 25
    xs = np.convolve(np.pad(xs, k, mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), mode="valid"); ys = np.convolve(np.pad(ys, k, mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), mode="valid")
    pts = list(zip(xs, ys))
    def stamp(layer, w, cor, off=(0, 0)):
        d = ImageDraw.Draw(layer)
        for x, y in pts: d.ellipse((x + off[0] - w / 2, y + off[1] - w / 2, x + off[0] + w / 2, y + off[1] + w / 2), fill=cor)
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); stamp(L, 120, (0, 230, 255, 200)); L = L.filter(ImageFilter.GaussianBlur(26)); im = Image.alpha_composite(im, L)
    S = Image.new("RGBA", im.size, (0, 0, 0, 0)); stamp(S, 78, (0, 0, 0, 150), (8, 12)); S = S.filter(ImageFilter.GaussianBlur(8)); im = Image.alpha_composite(im, S)
    for w, c in ((78, (4, 60, 80, 255)), (62, (40, 225, 250, 255)), (20, (200, 255, 255, 255))):
        T = Image.new("RGBA", im.size, (0, 0, 0, 0)); stamp(T, w, c); im = Image.alpha_composite(im, T)
    f = anton(138)
    texto(im, (36, 590), [("CULPA DOS", (255, 255, 255))], f, anchor="ls", stroke=9)
    texto(im, (36, 705), [("ANDES?", YEL)], f, anchor="ls", stroke=9)
    return vinheta(im.convert("RGB"), 0.25)


if __name__ == "__main__":
    for k in (sys.argv[1:] or ["nino", "sul"]):
        im = {"nino": nino, "sul": sul}[k](); p = f"{OUT}/{k}-thumb.jpg"; im.save(p, quality=90, optimize=True); print(p, os.path.getsize(p) // 1024, "KB")
