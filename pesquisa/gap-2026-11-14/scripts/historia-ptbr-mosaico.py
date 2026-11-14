"""Mosaico de thumbs historia-ptbr (nossas) x referências no mesmo tema.
Uso: tools/.venv/bin/python -I pesquisa/gap-2026-11-14/scripts/historia-ptbr-mosaico.py
Baixa as thumbs (i.ytimg direto; se falhar, via WARP) para dados/historia-ptbr/thumbs/ e grava
mosaicos/mosaico-historia-ptbr.jpg (480x270 por thumb) e mosaico-historia-ptbr-celular.jpg (320x180), ambos <= 1 MB.
Layout: 3 blocos; em cada bloco, linha de cima = nossas, linha de baixo = deles (mesmo tema, mesma coluna)."""
import os, io, subprocess
from PIL import Image, ImageDraw, ImageFont

FAB = os.path.expanduser("~/workspace/fabrica-youtube")
GAP = f"{FAB}/pesquisa/gap-2026-11-14"
TH = f"{GAP}/dados/historia-ptbr/thumbs"
VID = f"{FAB}/canais/historia-ptbr/videos"
os.makedirs(TH, exist_ok=True)
os.makedirs(f"{GAP}/mosaicos", exist_ok=True)

# (tema, nosso: (id ou caminho local, rótulo), deles: (id, rótulo))
PARES = [
    ("Egito", ("g847Td0Plsk", "NÓS Egito 380"), ("VQPzrVMHWlg", "HiM Egito 571 mil")),
    ("Índia", ("MV5SSjoccqE", "NÓS Índia 251"), ("p9IIGdg91fE", "HiM Índia 641 mil")),
    ("Irã", ("GkzMbsB0iH0", "NÓS Irã 23"), ("XVwr1Rm_9jc", "HiM Pérsia 91 mil")),
    ("China", ("-sx6xAkQbA0", "NÓS China 147"), ("Fbz4QYZ5XrI", "Genius China 553 mil")),
    ("Brasil", ("3aA7eUzwfeg", "NÓS Brasil 53"), ("sD0cIJ8JMYw", "HEG Brasil 22 mil")),
    ("Roma", ("fkltw3XwQ0E", "NÓS Roma 2"), ("XyulPwDw1CE", "HEG Roma 73 mil")),
    ("Rússia", ("3TwMYoxnF4k", "NÓS Rússia 17"), ("aMld6kMmcm4", "Clone pt Rússia 254 mil")),
    ("França", (f"{VID}/008-franca/entrega/thumb-A.jpg", "NÓS França (15/11)"), ("7amJtj96T0w", "Clone pt França 188 mil")),
    ("Alemanha", (f"{VID}/009-alemanha/entrega/thumb-A.jpg", "NÓS Alemanha (16/11)"), ("wrPmVXTr91s", "Genius Alemanha 271 mil")),
]


def baixar(vid):
    dst = f"{TH}/{vid}.jpg"
    if os.path.exists(dst) and os.path.getsize(dst) > 5000:
        return dst
    for q in ("maxresdefault", "hqdefault"):
        url = f"https://i.ytimg.com/vi/{vid}/{q}.jpg"
        for proxy in ([], ["--proxy", "socks5h://127.0.0.1:40000"]):
            r = subprocess.run(["curl", "-sfL", "--max-time", "30", *proxy, "-o", dst, url])
            if r.returncode == 0 and os.path.getsize(dst) > 5000:
                return dst
    raise SystemExit(f"falhou {vid}")


def carregar(ref):
    p = ref if ref.startswith("/") else baixar(ref)
    im = Image.open(p).convert("RGB")
    # corta barras pretas do hqdefault (4:3) para 16:9
    w, h = im.size
    if abs(w / h - 16 / 9) > 0.05:
        nh = int(w * 9 / 16); top = (h - nh) // 2
        im = im.crop((0, top, w, top + nh))
    return im


def fonte(px):
    for f in ("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
              f"{VID}/003-ira/v2-amostras/thumbs/base/fonts/OpenSans-ExtraBold.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, px)
    return ImageFont.load_default()


def mosaico(tw, th, saida, fpx):
    lab = int(fpx * 1.6); gap = 8; cols = 3; blocos = 3
    W = cols * tw + (cols + 1) * gap
    bh = 2 * (th + lab) + 3 * gap
    H = blocos * bh + (blocos - 1) * gap * 2
    img = Image.new("RGB", (W, H), (20, 20, 20)); d = ImageDraw.Draw(img); f = fonte(fpx)
    for i, (tema, nos, deles) in enumerate(PARES):
        b, c = divmod(i, cols)
        x = gap + c * (tw + gap); y0 = b * (bh + gap * 2) + gap
        for r, (ref, rot) in enumerate((nos, deles)):
            y = y0 + r * (th + lab + gap)
            cor = (255, 210, 40) if r == 0 else (120, 220, 255)
            d.text((x + 2, y + 2), rot, font=f, fill=cor)
            img.paste(carregar(ref).resize((tw, th), Image.LANCZOS), (x, y + lab))
    q = 88
    while True:
        buf = io.BytesIO(); img.save(buf, "JPEG", quality=q, optimize=True)
        if buf.tell() <= 1_000_000 or q < 40:
            break
        q -= 6
    open(saida, "wb").write(buf.getvalue())
    print(saida, img.size, buf.tell() // 1024, "KB q", q)


mosaico(480, 270, f"{GAP}/mosaicos/mosaico-historia-ptbr.jpg", 20)
mosaico(320, 180, f"{GAP}/mosaicos/mosaico-historia-ptbr-celular.jpg", 15)
