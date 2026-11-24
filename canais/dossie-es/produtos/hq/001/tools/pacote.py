"""Pacote final da #1 (e2, 24/11/2026): PDF final 6×9 pol. (1600 px/página) com link clicável, zip e prévias.

Pré-requisitos: artes em arte-001/, `montar.py` rodado (livro.json) e `tools/extras_pacote.py` (pôsteres, wallpapers,
QR, miniatura). Uso (raiz do repo):
  tools/.venv/bin/python canais/dossie-es/produtos/hq/001/tools/pacote.py [--poster C]
Saída em 001/pacote/: Expedientes-Secretos-1.pdf, Expedientes-Secretos-1.zip (PDF + pôster png/pdf + 6 wallpapers +
LEEME.txt) e prévias em 001/previas/.
"""
import argparse
import glob
import json
import os
import sys
import zipfile

from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from pypdf.generic import RectangleObject

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HQ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(HQ, "src"))
import diagramar as dg  # noqa: E402

PAC = os.path.join(AQUI, "pacote")
PREV = os.path.join(AQUI, "previas")
NOME = "Expedientes-Secretos-1"
LEEME = """EXPEDIENTES SECRETOS #1 · Dossier en Minutos

Gracias por tu compra. En este archivo encontrarás:

- Expedientes-Secretos-1.pdf: el cómic completo (Operación Garbo + La Cosa), {pags} páginas.
  Se lee bien en el celular, la tableta o la computadora.
- poster-A3.png y poster-A3.pdf: el póster en tamaño A3 (29,7 × 42 cm) a 300 dpi, listo para imprimir.
- wallpapers/: 6 fondos de pantalla (3 para el celular en 1440×3120 y 3 para la computadora en 3840×2160).

Uso personal. Prohibida su reventa o distribución.
¿Qué expediente quieres en el #2? Déjalo en los comentarios del canal: youtube.com/channel/UCVCYqeuCwTWC7Lqez_qeWRA
"""


def pdf_final():
    livro = json.load(open(os.path.join(AQUI, "livro.json")))
    livro["saida_dir"] = "001/final"
    livro["pdf"] = "001/pacote/%s-sem-link.pdf" % NOME
    livro["larg_pdf"] = 1600
    tmp = os.path.join(AQUI, "livro-final.json")
    json.dump(livro, open(tmp, "w"), ensure_ascii=False)
    dg.livro(tmp)
    os.remove(tmp)
    # link clicável nas páginas com "links" (rect em px da página 1800×2700 → pontos do PDF)
    src = os.path.join(PAC, "%s-sem-link.pdf" % NOME)
    r = PdfReader(src)
    w = PdfWriter(clone_from=r)
    for i, pg in enumerate(livro["paginas"]):
        for ln in pg.get("links", []):
            mb = w.pages[i].mediabox
            sx, sy = float(mb.width) / dg.W, float(mb.height) / dg.H
            x, y, ww, hh = ln["rect"]
            rect = (x * sx, float(mb.height) - (y + hh) * sy, (x + ww) * sx, float(mb.height) - y * sy)
            w.add_annotation(page_number=i, annotation=Link(rect=RectangleObject(rect), url=ln["url"]))
            print("link p.%d" % (i + 1), ln["url"])
    w.add_metadata({"/Title": "Expedientes Secretos #1", "/Author": "Dossier en Minutos"})
    final = os.path.join(PAC, NOME + ".pdf")
    with open(final, "wb") as f:
        w.write(f)
    os.remove(src)
    print(NOME + ".pdf", len(r.pages), "páginas", os.path.getsize(final) // 1024, "KB")
    return len(r.pages)


def previas_paginas():
    pasta = os.path.join(AQUI, "final")
    for nome in ("p01-capa", "p05-garbo-01", "p11-garbo-07", "p30-lacosa-09"):
        arq = os.path.join(pasta, nome + ".jpg")
        if not os.path.exists(arq):
            continue
        im = Image.open(arq).convert("RGB")
        im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
        q = 86
        while True:
            im.save(os.path.join(PREV, "pagina-" + nome + ".jpg"), "JPEG", quality=q, optimize=True)
            if os.path.getsize(os.path.join(PREV, "pagina-" + nome + ".jpg")) <= 1_000_000 or q < 50:
                break
            q -= 6
        print("prévia", nome)


def zipar(poster, pags):
    z = os.path.join(PAC, NOME + ".zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(os.path.join(PAC, NOME + ".pdf"), NOME + ".pdf")
        zf.write(os.path.join(PAC, "poster-%s-com-titulo.png" % poster), "poster-A3.png")
        zf.write(os.path.join(PAC, "poster-%s-com-titulo.pdf" % poster), "poster-A3.pdf")
        for wp in sorted(glob.glob(os.path.join(PAC, "wallpaper-*.jpg"))):
            zf.write(wp, "wallpapers/" + os.path.basename(wp))
        zf.writestr("LEEME.txt", LEEME.format(pags=pags))
    print(os.path.basename(z), os.path.getsize(z) // (1024 * 1024), "MB", "· pôster", poster)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--poster", default="C", choices=["A", "C"])
    ap.add_argument("--so-zip", action="store_true", help="só refaz o zip (troca de pôster)")
    a = ap.parse_args()
    os.makedirs(PAC, exist_ok=True)
    os.makedirs(PREV, exist_ok=True)
    if a.so_zip:
        pags = len(PdfReader(os.path.join(PAC, NOME + ".pdf")).pages)
    else:
        pags = pdf_final()
        previas_paginas()
    zipar(a.poster, pags)


if __name__ == "__main__":
    main()
