"""Baixa thumbs das referências (Clearance Required) e monta mosaico nosso × deles.
Uso: tools/.venv/bin/python -I pesquisa/gap-2026-11-14/scripts/lugares-guerra-en-mosaico.py
"""
import os, shutil, subprocess, urllib.request
from PIL import Image, ImageDraw, ImageFont

R = os.path.expanduser("~/workspace/fabrica-youtube")
D = f"{R}/pesquisa/gap-2026-11-14/dados/lugares-guerra-en/thumbs"
M = f"{R}/pesquisa/gap-2026-11-14/mosaicos"
os.makedirs(D, exist_ok=True); os.makedirs(M, exist_ok=True)
V = f"{R}/canais/lugares-guerra-en/videos"

NOSSOS = [  # (arquivo local, rótulo)
    (f"{V}/001-midway/out/thumb-A.jpg", "NOSSO Midway A (no ar) · 12 views"),
    (f"{V}/001-midway/out/thumb-B.jpg", "NOSSO Midway B"),
    (f"{V}/001-midway/out/thumb-C.jpg", "NOSSO Midway C"),
    (f"{V}/002-bikini/thumbs/thumb-A.jpg", "NOSSO Bikini A · agendado"),
    (f"{V}/002-bikini/thumbs/thumb-B.jpg", "NOSSO Bikini B"),
    (f"{V}/002-bikini/thumbs/thumb-C.jpg", "NOSSO Bikini C"),
    (f"{V}/003-gettysburg/thumbs/thumb-A.jpg", "NOSSO Gettysburg A · agendado"),
    (f"{V}/003-gettysburg/thumbs/thumb-B.jpg", "NOSSO Gettysburg B"),
    (f"{V}/003-gettysburg/thumbs/thumb-C.jpg", "NOSSO Gettysburg C"),
]
DELES = [  # (id, rótulo)
    ("hEsjPdO3YQM", "WTS Iwo Jima · 4,58 mi"),
    ("X6hVKPefGbs", "FF USS Arizona · 1,16 mi"),
    ("2X3gH8jud_Q", "CWFP Lincoln · 1,09 mi"),
    ("NIys6UZBr-M", "Ship Tales 900 men · 944 mil"),
    ("V_uUqr3K2jM", "FF PT-109 · 550 mil"),
    ("82yxT4SiAyA", "LATG Wake · 529 mil"),
    ("5hzi3ocfB44", "FF Pink Sub · 447 mil"),
    ("2dUsSNmsiVw", "Ship Tales Alabama · 395 mil"),
    ("28GoBGMdlF0", "WTS Omaha · 348 mil"),
    ("D0mwYK5g1Ms", "WTS Normandy · 136 mil"),
    ("kZbPoOfx2M0", "WTS Hacksaw · 95 mil"),
    ("gnzKt88W5hg", "WTS B-52 Hanoi · 54 mil (4 d)"),
    ("XAf-lLEfZjk", "LATG Tinian · 21 mil"),
    ("Nr0x7alVzyk", "WTS Cheyenne (flop) · 5 mil"),
    ("0VBceJJszuw", "LATG Mulberry (flop) · 521"),
]


def baixar(vid):
    dst = f"{D}/ref-{vid}.jpg"
    if os.path.exists(dst) and os.path.getsize(dst) > 5000:
        return dst
    for q in ("maxresdefault", "hqdefault"):
        url = f"https://i.ytimg.com/vi/{vid}/{q}.jpg"
        try:
            data = urllib.request.urlopen(url, timeout=30).read()
        except Exception:
            data = subprocess.run(["curl", "-s", "--max-time", "40", "--socks5-hostname", "127.0.0.1:40000", url],
                                  capture_output=True).stdout
        if len(data) > 5000:
            open(dst, "wb").write(data)
            return dst
    raise SystemExit(f"falhou {vid}")


def fonte(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def carregar(path, w, h):
    im = Image.open(path).convert("RGB")
    # corta letterbox do hqdefault (4:3 com faixas)
    iw, ih = im.size
    if abs(iw / ih - 16 / 9) > 0.05:
        nh = int(iw * 9 / 16); top = (ih - nh) // 2
        im = im.crop((0, top, iw, top + nh))
    return im.resize((w, h), Image.LANCZOS)


def mosaico(tw, th, cols, nome, fs):
    lab = fs + 10
    nos = [(p, l) for p, l in NOSSOS if os.path.exists(p)]
    for p, _ in nos:
        shutil.copy(p, f"{D}/nosso-{p.split('/')[-3]}-{os.path.basename(p)}")
    refs = [(baixar(v), l) for v, l in DELES]
    pad, head = 6, fs + 18
    rows_n = -(-len(nos) // cols); rows_r = -(-len(refs) // cols)
    W = cols * (tw + pad) + pad
    H = head + rows_n * (th + lab + pad) + head + rows_r * (th + lab + pad) + pad
    img = Image.new("RGB", (W, H), (20, 20, 24)); d = ImageDraw.Draw(img); f = fonte(fs); fh = fonte(fs + 4)
    y = 4
    d.text((pad, y), "CLEARANCE REQUIRED (nosso): A/B/C de cada vídeo", fill=(253, 213, 5), font=fh); y += head
    for blocos, cor in ((nos, (253, 213, 5)), (refs, (120, 220, 240))):
        for i, (p, l) in enumerate(blocos):
            r, c = divmod(i, cols)
            x = pad + c * (tw + pad); yy = y + r * (th + lab + pad)
            img.paste(carregar(p, tw, th), (x, yy))
            d.text((x, yy + th + 2), l, fill=cor, font=f)
        y += -(-len(blocos) // cols) * (th + lab + pad)
        if blocos is nos:
            d.text((pad, y + 2), "REFERÊNCIAS (90 d): melhores + 2 flops", fill=(120, 220, 240), font=fh); y += head
    out = f"{M}/{nome}"
    for q in (88, 80, 72, 64, 56):
        img.save(out, "JPEG", quality=q, optimize=True)
        if os.path.getsize(out) <= 1_000_000:
            break
    print(out, img.size, os.path.getsize(out))


mosaico(480, 270, 3, "mosaico-lugares-guerra-en.jpg", 18)
mosaico(320, 180, 3, "mosaico-lugares-guerra-en-celular.jpg", 13)
