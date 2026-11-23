"""Amostra da HQ colorida "Expedientes Secretos #1" (v3, 23/11/2026): capa, 2 páginas, wallpapers e amostra.pdf.

Artes sem texto pelo Codex (gerar.py + visual-hq.yaml); todo texto composto aqui (fontes OFL em fontes/LEIA.md).
Páginas: diagramar.py (da v2, com painel em polígono) lendo paginas.json.
Uso: ~/workspace/fabrica-youtube/tools/.venv/bin/python hq.py   (saída em ../)
"""
import json
import os

from PIL import Image, ImageDraw, ImageFilter

import diagramar as dg

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(AQUI, ".."))
VERM, PRETO, PAPEL = (179, 38, 30), (17, 17, 17), (233, 223, 201)
K = 2


def ampliar(arq, W, H, foco=(0.5, 0.5)):
    """Cobre WxH (LANCZOS + nitidez, o caminho escolhido na v2; Real-ESRGAN estraga a arte)."""
    im = Image.open(os.path.join(OUT, "arte", arq)).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=max(1, s), percent=70, threshold=2))
    ox = min(max(int(foco[0] * im.width - W / 2), 0), im.width - W)
    oy = min(max(int(foco[1] * im.height - H / 2), 0), im.height - H)
    return im.crop((ox, oy, ox + W, oy + H))


def gradiente(im, de, ate, forca, cima=True):
    W, H = im.size
    m = Image.new("L", (1, H), 0)
    for y in range(H):
        f = y / H
        t = (ate - f) / (ate - de) if cima else (f - de) / (ate - de)
        m.putpixel((0, y), int(forca * min(1, max(0, t)) ** 1.2))
    cam = Image.new("RGBA", (W, H), (8, 10, 18, 255))
    cam.putalpha(m.resize((W, H)))
    b = im.convert("RGBA")
    b.alpha_composite(cam)
    return b


def caixa_legenda(d, x, y, larg, titulo, texto, px_t, px):
    """Legenda colorida estilo HQ: caixa papel + barra vermelha (mesma linguagem das páginas)."""
    ft, f = dg.fonte("titulo", px_t), dg.fonte("fala", px)
    pad = 22 * K
    linhas = dg.quebrar(texto.upper(), f, larg - 2 * pad - 14 * K, d)
    _, th, lh = dg.bloco(d, linhas, f, 1.05)
    h = pad + px_t * K * 1.0 + 8 * K + th + pad
    d.rectangle((x + 10 * K, y + 10 * K, x + larg + 10 * K, y + h + 10 * K), fill=PRETO)
    d.rectangle((x, y, x + larg, y + h), fill=PAPEL, outline=PRETO, width=5 * K)
    d.rectangle((x + 6 * K, y + 6 * K, x + 20 * K, y + h - 6 * K), fill=VERM)
    d.text((x + pad + 14 * K, y + pad - 4 * K), titulo, font=ft, fill=VERM)
    yy = y + pad + px_t * K * 1.0 + 4 * K
    for l in linhas:
        d.text((x + pad + 14 * K, yy), l, font=f, fill=PRETO)
        yy += lh
    return h


def capa():
    W, H = 1800 * K, 2700 * K
    base = gradiente(ampliar("K01.jpg", W, H, (0.5, 0.5)), 0.0, 0.34, 225)
    d = ImageDraw.Draw(base)
    # faixa da marca
    d.rectangle((0, 0, W, 118 * K), fill=PRETO)
    d.rectangle((0, 118 * K, W, 128 * K), fill=VERM)
    fm = dg.fonte("titulo", 62)
    d.text((70 * K, 28 * K), "DOSSIER EN MINUTOS", font=fm, fill=PAPEL)
    ed = "EDICIÓN DIGITAL  ·  DIC 2026"
    d.text((W - 70 * K - d.textlength(ed, font=fm), 28 * K), ed, font=fm, fill=PAPEL)
    # selo de número/preço (canto do gibi)
    sx, sy, sw, sh = 70 * K, 175 * K, 250 * K, 300 * K
    d.rectangle((sx + 10 * K, sy + 10 * K, sx + sw + 10 * K, sy + sh + 10 * K), fill=PRETO)
    d.rectangle((sx, sy, sx + sw, sy + sh), fill=PAPEL, outline=PRETO, width=6 * K)
    d.rectangle((sx, sy, sx + sw, sy + 70 * K), fill=VERM)
    f1 = dg.fonte("titulo", 54)
    dg.escrever(d, sx + sw / 2, sy + 37 * K, ["EXPEDIENTE"], f1, 56 * K, cor="white")
    f2 = dg.fonte("sfx", 170)
    t = "#1"
    d.text((sx + (sw - d.textlength(t, font=f2)) / 2, sy + 70 * K), t, font=f2, fill=PRETO)
    f3 = dg.fonte("titulo", 50)
    dg.escrever(d, sx + sw / 2, sy + 262 * K, ["US$ 6,99"], f3, 52 * K, cor=VERM)
    # título
    ft = dg.fonte("sfx", 250)
    for i, txt in enumerate(("EXPEDIENTES", "SECRETOS")):
        y = (150 + i * 245) * K
        x0 = 360 * K
        larg = W - x0 - 70 * K
        tw = d.textlength(txt, font=ft)
        f = ft if tw <= larg else dg.fonte("sfx", 250 * larg / tw)
        x = x0 + (larg - d.textlength(txt, font=f)) / 2
        d.text((x + 14 * K, y + 14 * K), txt, font=f, fill=VERM, stroke_width=12 * K, stroke_fill=VERM)
        d.text((x, y), txt, font=f, fill="white", stroke_width=12 * K, stroke_fill=PRETO)
    sub = "2 HISTORIAS REALES DE ESPIONAJE QUE NO ESTÁN EN EL CANAL"
    fs = dg.fonte("titulo", 58)
    d.text(((W - d.textlength(sub, font=fs)) / 2 + 145 * K, 690 * K), sub, font=fs, fill=PAPEL,
           stroke_width=3 * K, stroke_fill=PRETO)
    # chamadas das 2 histórias
    caixa_legenda(d, W - 760 * K, 1300 * K, 690 * K, "+ LA COSA  ·  MOSCÚ, 1945",
                  "Unos niños regalan al embajador de EE. UU. un escudo tallado. Escondía un micrófono sin pilas.",
                  52, 34)
    caixa_legenda(d, 70 * K, 2140 * K, 820 * K, "OPERACIÓN GARBO  ·  1941–1944",
                  "El español que inventó 27 espías que nunca existieron… y engañó a Hitler.", 60, 38)
    # carimbo
    car = Image.new("RGBA", (640 * K, 150 * K), (0, 0, 0, 0))
    dc = ImageDraw.Draw(car)
    dc.rectangle((8 * K, 8 * K, 632 * K, 142 * K), fill=(233, 223, 201, 225), outline=VERM, width=9 * K)
    fc = dg.fonte("titulo", 96)
    t = "HECHOS REALES"
    dc.text(((640 * K - dc.textlength(t, font=fc)) / 2, 22 * K), t, font=fc, fill=VERM)
    car = car.rotate(9, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(car, (int(W - car.width - 60 * K), int(2200 * K)))
    # rodapé
    d.rectangle((0, H - 100 * K, W, H), fill=PRETO)
    rod = "2 HISTORIETAS DE ESPIONAJE  ·  +36 PÁGINAS  ·  PÓSTER + 6 WALLPAPERS"
    fr = dg.fonte("titulo", 44)
    d.text(((W - d.textlength(rod, font=fr)) / 2, H - 78 * K), rod, font=fr, fill=PAPEL)
    return base.convert("RGB").resize((W // K, H // K), Image.LANCZOS)


def marca(d, x, y, px, alinhar="dir"):
    f1, f2 = dg.fonte("titulo", px), dg.fonte("titulo", px * 0.62)
    t1, t2 = "DOSSIER EN MINUTOS", "EXPEDIENTES SECRETOS #1"
    w = max(d.textlength(t1, font=f1), d.textlength(t2, font=f2))
    x0 = x - w if alinhar == "dir" else (x - w / 2 if alinhar == "centro" else x)
    for t, f, dy, cor in ((t1, f1, 0, (233, 223, 201, 215)), (t2, f2, px * 2 * 0.98, (179, 38, 30, 235))):
        tw = d.textlength(t, font=f)
        xx = x0 + (w - tw) if alinhar == "dir" else (x0 + (w - tw) / 2 if alinhar == "centro" else x0)
        d.text((xx, y + dy), t, font=f, fill=cor, stroke_width=2, stroke_fill=(0, 0, 0, 160))


def wallpapers():
    # desktop 3840×2160: marca discreta no canto inferior direito (os ícones ficam à esquerda no Windows)
    im = ampliar("W01.jpg", 3840, 2160).convert("RGBA")
    camada = Image.new("RGBA", im.size, (0, 0, 0, 0))
    marca(ImageDraw.Draw(camada), 3840 - 90, 2160 - 210, 34 * 2)
    im.alpha_composite(camada)
    im = im.convert("RGB")
    im.save(os.path.join(OUT, "wallpaper-desktop.png"))
    dg.salvar_previa(im, "wallpaper-desktop.jpg", 3840)
    # celular 1440×3120: relógio no topo (céu escuro livre), marca embaixo, acima da barra de gestos
    im = ampliar("W02.jpg", 1440, 3120, (0.5, 0.5)).convert("RGBA")
    camada = Image.new("RGBA", im.size, (0, 0, 0, 0))
    marca(ImageDraw.Draw(camada), 720, 3120 - 300, 30 * 2, alinhar="centro")
    im.alpha_composite(camada)
    im = im.convert("RGB")
    im.save(os.path.join(OUT, "wallpaper-celular.png"))
    dg.salvar_previa(im, "wallpaper-celular.jpg", 1440)


def main():
    folhas = []
    c = capa()
    c.save(os.path.join(OUT, "capa.png"), dpi=(300, 300))
    dg.salvar_previa(c, "capa.jpg")
    folhas.append(c)
    wallpapers()
    cfg = json.load(open(os.path.join(AQUI, "paginas.json")))
    dg.SAIDA = OUT
    for pg in cfg["paginas"]:
        im = dg.pagina(pg, "cor")
        im.save(os.path.join(OUT, pg["saida"] + ".png"), dpi=(300, 300))
        dg.salvar_previa(im, pg["saida"] + ".jpg")
        folhas.append(im)
    pdf = os.path.join(OUT, "amostra.pdf")
    folhas[0].save(pdf, "PDF", resolution=300, save_all=True, append_images=folhas[1:], quality=88)
    print("amostra.pdf", len(folhas), "páginas", os.path.getsize(pdf) // 1024, "KB")


if __name__ == "__main__":
    main()
