"""Mosaico nosso x deles (dossie-es), 4 colunas: linhas 1 e 3 = nossas, 2 e 4 = referência no mesmo tema.
Uso: tools/.venv/bin/python -I pesquisa/gap-2026-11-14/scripts/dossie-es-mosaico.py
Gera mosaicos/mosaico-dossie-es.jpg (480x270 por thumb) e mosaico-dossie-es-celular.jpg (320x180), <= 1 MB."""
import os
from PIL import Image, ImageDraw, ImageFont

R = os.path.expanduser("~/workspace/fabrica-youtube")
T = f"{R}/pesquisa/gap-2026-11-14/dados/dossie-es/thumbs"
V = f"{R}/canais/dossie-es/videos"
OUT = f"{R}/pesquisa/gap-2026-11-14/mosaicos"

# (arquivo, rótulo)
NOSSOS1 = [(f"{T}/Qs-TusYCr-o.jpg", "NOSSO CIA · 178"), (f"{T}/it37m7pz0hI.jpg", "NOSSO Mossad · 412"),
           (f"{T}/E1Rgm7jbE0g.jpg", "NOSSO FBI · 102"), (f"{T}/I_ehrH5Yrak.jpg", "NOSSO KGB · 36")]
DELES1 = [(f"{T}/sIGKXDi6YY8.jpg", "Archive CIA · 216 mil"), (f"{T}/9LyvAHVecwY.jpg", "Atlas (es) Mossad · 86 mil"),
          (f"{T}/kEfEQYeY2I0.jpg", "Te lo Pinto FBI vs CIA · 182 mil"), (f"{T}/by7uTDjSx7Y.jpg", "Te lo Pinto KGB · 246 mil")]
NOSSOS2 = [(f"{V}/007-ss/out/thumbs/thumb-A.jpg", "NOSSO SS (15/11) · –"), (f"{T}/gmA0LkJqf_U.jpg", "NOSSO Cosa Nostra · 46"),
           (f"{T}/DBLonwmeQ7c.jpg", "NOSSO Masones · 0"), (f"{V}/008-inquisicion/entrega/thumb-A.jpg", "NOSSO Inquisición (16/11) · –")]
DELES2 = [(f"{T}/PmpWyltn08s.jpg", "Archive SS · 684 mil"), (f"{T}/AQiEQuk4PPk.jpg", "Te lo Pinto sicario (crimen) · 372 mil"),
          (f"{T}/dXRO17KlRUw.jpg", "Atlas (es) CIA vs KGB · 100 mil"), (f"{T}/oWkkPoYFC5o.jpg", "Te lo Pinto policía nazi · 200 mil")]
ROWS = [NOSSOS1, DELES1, NOSSOS2, DELES2]


def font(sz):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def build(w, h, lab, out):
    gap = 6
    W = 4 * w + 5 * gap
    H = 4 * (h + lab) + 5 * gap
    img = Image.new("RGB", (W, H), (20, 20, 20))
    d = ImageDraw.Draw(img)
    f = font(max(12, lab - 8))
    for r, row in enumerate(ROWS):
        y = gap + r * (h + lab + gap)
        bg = (40, 70, 140) if r % 2 == 0 else (120, 40, 40)
        for c, (p, t) in enumerate(row):
            x = gap + c * (w + gap)
            d.rectangle([x, y, x + w, y + lab], fill=bg)
            d.text((x + 6, y + 3), t, fill="white", font=f)
            if os.path.exists(p):
                im = Image.open(p).convert("RGB")
                # recorta para 16:9 (hqdefault vem com tarjas)
                iw, ih = im.size
                th = int(iw * 9 / 16)
                if th < ih:
                    top = (ih - th) // 2
                    im = im.crop((0, top, iw, top + th))
                img.paste(im.resize((w, h), Image.LANCZOS), (x, y + lab))
    q = 85
    while True:
        img.save(out, "JPEG", quality=q, optimize=True)
        if os.path.getsize(out) <= 1_000_000 or q <= 40:
            break
        q -= 5
    print(out, img.size, os.path.getsize(out), "q", q)


os.makedirs(OUT, exist_ok=True)
build(480, 270, 28, f"{OUT}/mosaico-dossie-es.jpg")
build(320, 180, 22, f"{OUT}/mosaico-dossie-es-celular.jpg")
