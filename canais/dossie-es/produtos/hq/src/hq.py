"""Amostra da HQ colorida "Expedientes Secretos #1" (v3, 23/11/2026): capa, 2 páginas, wallpapers e amostra.pdf.

Artes sem texto pelo Codex (gerar.py + visual-hq.yaml); todo texto composto aqui (fontes OFL em fontes/LEIA.md).
Páginas: diagramar.py (da v2, com painel em polígono) lendo paginas.json.
Uso: ~/workspace/fabrica-youtube/tools/.venv/bin/python hq.py [--capa]   (saída em ../; --capa = só capas + Hotmart)
"""
import json
import os
import sys

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


VIDEOS = os.path.abspath(os.path.join(AQUI, "..", "..", "..", "videos"))


def arte_dupla(W, H, cima, baixo):
    """Capa genérica (#2, #3… do CTA): 2 artes 16:9 de vídeos já prontos, separadas por calha diagonal (igual à #1)."""
    def cobrir(arq, w, h):
        im = Image.open(os.path.join(VIDEOS, arq)).convert("RGB")
        s = max(w / im.width, h / im.height)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=max(1, s), percent=60, threshold=2))
        return im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))
    base = cobrir(baixo, W, int(H * 0.62))
    out = Image.new("RGB", (W, H), PRETO)
    out.paste(cobrir(cima, W, int(H * 0.62)), (0, 0))
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon([(0, H * 0.56), (W, H * 0.40), (W, H), (0, H)], fill=255)
    out.paste(base, (0, H - base.height), m.crop((0, H - base.height, W, H)))
    d = ImageDraw.Draw(out)
    d.line([(0, H * 0.56), (W, H * 0.40)], fill=PRETO, width=18 * K)
    return out


def capa(numero=1, arte=None, historias=True):
    """Capa da edição. numero=1: a real (arte K01 + chamadas das 2 histórias).
    numero>1 com arte=(cima, baixo): capa genérica de edição futura para o CTA (sem nome de história; o vídeo põe
    o carimbo CLASIFICADO por cima). Definições do Rodrigo de 24/11/2026: sem preço, sem data, sem rodapé."""
    W, H = 1800 * K, 2700 * K
    bg = ampliar("K01.jpg", W, H, (0.5, 0.5)) if arte is None else arte_dupla(W, H, *arte)
    base = gradiente(bg, 0.0, 0.34, 225)
    d = ImageDraw.Draw(base)
    # faixa da marca
    d.rectangle((0, 0, W, 118 * K), fill=PRETO)
    d.rectangle((0, 118 * K, W, 128 * K), fill=VERM)
    fm = dg.fonte("titulo", 62)
    d.text((70 * K, 28 * K), "DOSSIER EN MINUTOS", font=fm, fill=PAPEL)
    ed = "EDICIÓN DIGITAL"
    d.text((W - 70 * K - d.textlength(ed, font=fm), 28 * K), ed, font=fm, fill=PAPEL)
    # selo de número (canto do gibi), sem preço
    sx, sy, sw, sh = 70 * K, 175 * K, 250 * K, 250 * K
    d.rectangle((sx + 10 * K, sy + 10 * K, sx + sw + 10 * K, sy + sh + 10 * K), fill=PRETO)
    d.rectangle((sx, sy, sx + sw, sy + sh), fill=PAPEL, outline=PRETO, width=6 * K)
    d.rectangle((sx, sy, sx + sw, sy + 70 * K), fill=VERM)
    f1 = dg.fonte("titulo", 54)
    dg.escrever(d, sx + sw / 2, sy + 37 * K, ["EXPEDIENTE"], f1, 56 * K, cor="white")
    f2 = dg.fonte("sfx", 170)
    t = f"#{numero}"
    d.text((sx + (sw - d.textlength(t, font=f2)) / 2, sy + 72 * K), t, font=f2, fill=PRETO)
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
    sub = "2 HISTORIAS REALES DE ESPIONAJE QUE NO ESTÁN EN EL CANAL" if numero == 1 else "HISTORIAS REALES DE ESPIONAJE QUE NO ESTÁN EN EL CANAL"
    fs = dg.fonte("titulo", 58)
    d.text(((W - d.textlength(sub, font=fs)) / 2 + 145 * K, 690 * K), sub, font=fs, fill=PAPEL,
           stroke_width=3 * K, stroke_fill=PRETO)
    # chamadas das 2 histórias (rodapé removido em 24/11: a de baixo e o carimbo descem para ocupar o espaço)
    if numero == 1 and historias:
        caixa_legenda(d, W - 760 * K, 1300 * K, 690 * K, "+ LA COSA  ·  MOSCÚ, 1945",
                      "Unos niños regalan al embajador de EE. UU. un escudo tallado. Escondía un micrófono sin pilas.",
                      52, 34)
        caixa_legenda(d, 70 * K, 2330 * K, 820 * K, "OPERACIÓN GARBO  ·  1941–1944",
                      "El español que inventó 27 espías que nunca existieron… y engañó a Hitler.", 60, 38)
    elif historias:
        # edição futura: nenhuma história nomeada (não prometer o que não existe); texto tarjado
        for (x, y, larg, tit) in ((W - 760 * K, 1300 * K, 690 * K, 0.42),
                                  (70 * K, 2330 * K, 820 * K, 0.5)):
            h = 200 * K
            d.rectangle((x + 10 * K, y + 10 * K, x + larg + 10 * K, y + h + 10 * K), fill=PRETO)
            d.rectangle((x, y, x + larg, y + h), fill=PAPEL, outline=PRETO, width=5 * K)
            d.rectangle((x + 6 * K, y + 6 * K, x + 20 * K, y + h - 6 * K), fill=VERM)
            fx = dg.fonte("titulo", 56)
            d.text((x + 50 * K, y + 18 * K), "EXPEDIENTE  ·", font=fx, fill=VERM)
            x1 = x + 50 * K + d.textlength("EXPEDIENTE  ·  ", font=fx)
            d.rectangle((x1, y + 34 * K, x1 + (larg - 90 * K) * tit, y + 72 * K), fill=VERM)   # nome tarjado
            for j, fr in enumerate((0.86, 0.62)):
                yy = y + (100 + j * 50) * K
                d.rectangle((x + 50 * K, yy, x + 50 * K + (larg - 90 * K) * fr, yy + 30 * K), fill=PRETO)
    # carimbo
    car = Image.new("RGBA", (640 * K, 150 * K), (0, 0, 0, 0))
    dc = ImageDraw.Draw(car)
    dc.rectangle((8 * K, 8 * K, 632 * K, 142 * K), fill=(233, 223, 201, 225), outline=VERM, width=9 * K)
    fc = dg.fonte("titulo", 96)
    t = "HECHOS REALES"
    dc.text(((640 * K - dc.textlength(t, font=fc)) / 2, 22 * K), t, font=fc, fill=VERM)
    car = car.rotate(9, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(car, (int(W - car.width - 60 * K), int(2400 * K)))
    return base.convert("RGB").resize((W // K, H // K), Image.LANCZOS)


# capas genéricas das edições futuras (só para o CTA do vídeo; troque a arte quando a edição existir)
CAPAS_FUTURAS = {
    2: ("005-kgb/imagens/I060.jpg", "012-mi6/imagens/I050.jpg"),
    3: ("015-gru/imagens/I110.jpg", "003-fbi/imagens/I030.jpg"),
}


def hotmart(c):
    """Imagem do produto na Hotmart: quadrada (a ajuda pede JPG/PNG/GIF ≤ 5 MB, de preferência 600×600).
    Gera 1200×1200 (nítida em tela retina) e 600×600, capa centralizada sobre a própria arte desfocada."""
    pasta = os.path.join(OUT, "hotmart")
    os.makedirs(pasta, exist_ok=True)
    L = 1200
    fundo = c.resize((L, round(c.height * L / c.width)), Image.LANCZOS).crop((0, 300, L, 300 + L))
    fundo = fundo.filter(ImageFilter.GaussianBlur(28))
    fundo = Image.blend(fundo, Image.new("RGB", fundo.size, (8, 10, 18)), 0.55)
    h = 1110
    cap = c.resize((round(c.width * h / c.height), h), Image.LANCZOS)
    x, y = (L - cap.width) // 2, (L - h) // 2
    sombra = Image.new("RGBA", (L, L), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rectangle((x + 14, y + 16, x + cap.width + 14, y + h + 16), fill=(0, 0, 0, 170))
    fundo = fundo.convert("RGBA")
    fundo.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(10)))
    fundo = fundo.convert("RGB")
    fundo.paste(cap, (x, y))
    for lado in (1200, 600):
        im = fundo.resize((lado, lado), Image.LANCZOS)
        im.save(os.path.join(pasta, f"produto-{lado}.jpg"), "JPEG", quality=92, optimize=True)
        im.save(os.path.join(pasta, f"produto-{lado}.png"))
    print("hotmart", [f for f in sorted(os.listdir(pasta))])


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


def capas():
    """Só as capas (24/11/2026): capa.png/.jpg, hotmart/ e as capas genéricas #2/#3 do CTA (capa-2/3.png)."""
    c = capa()
    c.save(os.path.join(OUT, "capa.png"), dpi=(300, 300))
    dg.salvar_previa(c, "capa.jpg")
    hotmart(c)
    for n, arte in CAPAS_FUTURAS.items():
        im = capa(n, arte)
        im.save(os.path.join(OUT, f"capa-{n}.png"))
        dg.salvar_previa(im, f"capa-{n}.jpg")
    return c


def main():
    folhas = []
    c = capas()
    if "--capa" in sys.argv:
        return
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
