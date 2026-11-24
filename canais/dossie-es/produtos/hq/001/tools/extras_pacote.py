"""Peças do pacote da #1 (e2, 24/11/2026): QR do canal, pôsteres A3 (A e C, com e sem título), 6 wallpapers,
miniatura do pôster para a página "TU PÓSTER" e prévias ≤ 1 MB.

Ajuste do Rodrigo (24/11): 2 pôsteres próprios (A = mural do espião, C = cartaz vintage), título pequeno composto no
código ou nenhum (as 2 versões de cada); ele escolhe qual vai para o pacote (padrão: C até ele escolher).
Uso (raiz do repo): tools/.venv/bin/python canais/dossie-es/produtos/hq/001/tools/extras_pacote.py [--poster C]
Saída: 001/pacote/ (fora do git) + 001/qr-canal.png e 001/poster-miniatura.jpg (usados pelo livro).
"""
import argparse
import os
import sys

import qrcode
from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 001/
HQ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(HQ, "src"))
sys.path.insert(0, AQUI)
import diagramar as dg  # noqa: E402
from hq import marca  # noqa: E402
import extras as EX  # noqa: E402

PAC = os.path.join(AQUI, "pacote")
PREV = os.path.join(AQUI, "previas")
A3 = (3508, 4961)
VERM, CREME, NOITE = (179, 38, 30), (233, 223, 201), (14, 22, 40)


def previa(im, nome, larg=1200):
    p = im.convert("RGB")
    p = p.resize((larg, round(p.height * larg / p.width)), Image.LANCZOS)
    q = 88
    while True:
        p.save(os.path.join(PREV, nome), "JPEG", quality=q, optimize=True, progressive=True)
        if os.path.getsize(os.path.join(PREV, nome)) <= 1_000_000 or q <= 50:
            break
        q -= 6
    print(nome, os.path.getsize(os.path.join(PREV, nome)) // 1024, "KB")


def ampliar(caminho, W, H, foco=(0.5, 0.5)):
    """Cobre WxH (LANCZOS + nitidez, caminho escolhido na v2; Real-ESRGAN estraga a arte)."""
    im = Image.open(caminho).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=max(1, s), percent=70, threshold=2))
    ox = min(max(int(foco[0] * im.width - W / 2), 0), im.width - W)
    oy = min(max(int(foco[1] * im.height - H / 2), 0), im.height - H)
    return im.crop((ox, oy, ox + W, oy + H))


def qr():
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=24, border=2)
    q.add_data(EX.URL_CANAL)
    q.make(fit=True)
    im = q.make_image(fill_color="black", back_color="white").convert("RGB")
    im.save(os.path.join(AQUI, "qr-canal.png"))
    print("qr-canal.png", im.size, EX.URL_CANAL)


def titulo_poster(im, estilo):
    """Título pequeno e elegante: 'EXPEDIENTES SECRETOS' + linha fina + 'DOSSIER EN MINUTOS · …'."""
    im = im.convert("RGBA")
    W, H = im.size
    if estilo == "A":   # mural escuro: escurece só o topo para o título respirar
        from hq import gradiente
        im = gradiente(im.convert("RGB"), 0.0, 0.17, 200, cima=True)
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(cam)
    px1 = 190 if estilo == "C" else 150
    f1, f2 = dg.fonte("titulo", px1), dg.fonte("titulo", 70)
    t1, t2 = "EXPEDIENTES SECRETOS", "DOSSIER EN MINUTOS  ·  HISTORIAS REALES DE ESPIONAJE"
    if estilo == "C":
        cor1, cor2, contorno, y1 = NOITE + (255,), VERM + (255,), None, int(H * 0.06)
    else:
        cor1, cor2, contorno, y1 = CREME + (245,), VERM + (255,), (0, 0, 0, 200), int(H * 0.035)
    sw = 3 if contorno else 0
    bb = d.textbbox((0, 0), t1, font=f1, stroke_width=sw)
    w1 = bb[2] - bb[0]
    x1 = (W - w1) / 2 - bb[0]
    d.text((x1, y1 - bb[1]), t1, font=f1, fill=cor1, stroke_width=sw, stroke_fill=contorno)
    ly = y1 + (bb[3] - bb[1]) + 45
    d.line([((W - w1) / 2 + 240, ly), ((W + w1) / 2 - 240, ly)], fill=cor2, width=5)
    b2 = d.textbbox((0, 0), t2, font=f2, stroke_width=sw)
    y2 = int(H * 0.895) if estilo == "C" else ly + 45
    d.text(((W - (b2[2] - b2[0])) / 2 - b2[0], y2 - b2[1]), t2, font=f2, fill=cor2, stroke_width=sw,
           stroke_fill=contorno)
    im.alpha_composite(cam)
    return im.convert("RGB")


def poster(letra):
    arte = os.path.join(HQ, "arte-001", "posteres", "PO%s.jpg" % letra)
    base = ampliar(arte, *A3)
    saidas = {}
    for versao, im in (("sem-titulo", base), ("com-titulo", titulo_poster(base, letra))):
        nome = "poster-%s-%s" % (letra, versao)
        im.save(os.path.join(PAC, nome + ".png"), dpi=(300, 300), optimize=True)
        im.save(os.path.join(PAC, nome + ".pdf"), "PDF", resolution=300, quality=92)
        previa(im, nome + ".jpg", 1000)
        saidas[versao] = im
    return saidas


def wallpapers():
    lista = [("W01", os.path.join(HQ, "arte", "W01.jpg"), "desktop"),
             ("W02", os.path.join(HQ, "arte", "W02.jpg"), "celular"),
             ("W03", os.path.join(HQ, "arte-001", "W03.jpg"), "desktop"),
             ("W04", os.path.join(HQ, "arte-001", "W04.jpg"), "celular"),
             ("W05", os.path.join(HQ, "arte-001", "W05.jpg"), "desktop"),
             ("W06", os.path.join(HQ, "arte-001", "W06.jpg"), "celular")]
    for i, (wid, arq, tipo) in enumerate(lista, 1):
        if tipo == "desktop":   # marca no canto inferior direito (ícones do Windows à esquerda)
            im = ampliar(arq, 3840, 2160).convert("RGBA")
            cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
            marca(ImageDraw.Draw(cam), 3840 - 90, 2160 - 210, 34 * 2)
        else:                   # relógio no topo livre; marca embaixo, acima da barra de gestos
            im = ampliar(arq, 1440, 3120).convert("RGBA")
            cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
            marca(ImageDraw.Draw(cam), 720, 3120 - 300, 30 * 2, alinhar="centro")
        im.alpha_composite(cam)
        im = im.convert("RGB")
        nome = "wallpaper-%d-%s-%s.jpg" % (i, tipo, "3840x2160" if tipo == "desktop" else "1440x3120")
        im.save(os.path.join(PAC, nome), "JPEG", quality=94, optimize=True)
        if wid in ("W03", "W04"):
            previa(im, "wallpaper-%s-%s.jpg" % (wid, tipo), 1000 if tipo == "desktop" else 700)
        print(nome)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--poster", default="C", choices=["A", "C"], help="pôster do pacote/miniatura (padrão C)")
    ap.add_argument("--so", help="qr,posteres,wallpapers,miniatura (vírgula)")
    a = ap.parse_args()
    os.makedirs(PAC, exist_ok=True)
    os.makedirs(PREV, exist_ok=True)
    so = set((a.so or "qr,posteres,wallpapers,miniatura").split(","))
    if "qr" in so:
        qr()
    if "posteres" in so:
        for letra in ("A", "C"):
            poster(letra)
    if "miniatura" in so:
        im = Image.open(os.path.join(PAC, "poster-%s-com-titulo.png" % a.poster))
        im.thumbnail((1200, 1800), Image.LANCZOS)
        im.convert("RGB").save(os.path.join(AQUI, "poster-miniatura.jpg"), "JPEG", quality=90)
        print("poster-miniatura.jpg ←", a.poster)
    if "wallpapers" in so:
        wallpapers()


if __name__ == "__main__":
    main()
