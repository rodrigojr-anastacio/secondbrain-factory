"""Baixa thumbs (nossas 4 + referências) e monta mosaicos nosso x deles. Uso: python -I em-relevo-thumbs.py"""
import os, subprocess, io
from PIL import Image, ImageDraw, ImageFont
B = os.path.expanduser("~/workspace/fabrica-youtube/pesquisa/gap-2026-11-14")
T = f"{B}/dados/em-relevo/thumbs"
FONT = os.path.expanduser("~/workspace/fabrica-youtube/pesquisa/canal-clima-2026-11/identidade/fontes/IBMPlexMono-Bold.ttf")
NOSSOS = [("bG6-E4qjXYc", "NOSSO Sul/tornados 15"), ("FeSLzHvlkbo", "NOSSO El Niño 14"),
          ("I5KpDKy6r3E", "NOSSO Seca 1877 (agend.)"), ("2WH4ducITO0", "NOSSO 1983 (agend.)")]
REFS = [("xpBOF8FXXHM", "Chão do Sul 736k"), ("CMHf4Cqpcrs", "M.Entrópico SC 447k"),
        ("EGVFIQtvflg", "M.Entrópico RS 259k"), ("muqkMyx-sGA", "Chão do Sul 158k"),
        ("flm2yJ4mHhc", "M.Entrópico PR 202k"), ("ZVgiR9yIcGo", "Um Doc. Miyako 6,9M"),
        ("vfIaNeGVaVo", "Last Day Nepal 5,2M"), ("pm0Pgr5BlqA", "Chão do Sul 87k")]
def get(vid):
    p = f"{T}/{vid}.jpg"
    if os.path.exists(p) and os.path.getsize(p) > 5000: return p
    for q in ("maxresdefault", "hqdefault"):
        for prox in ([], ["--socks5-hostname", "127.0.0.1:40000"]):
            r = subprocess.run(["curl", "-sf", "-m", "30", *prox, "-o", p, f"https://i.ytimg.com/vi/{vid}/{q}.jpg"])
            if r.returncode == 0 and os.path.getsize(p) > 5000: return p
    return None
def tile(vid, lab, w, h, fs):
    p = get(vid)
    im = Image.open(p).convert("RGB") if p else Image.new("RGB", (w, h), "gray")
    # recorta 16:9 (hqdefault tem tarja preta)
    W, H = im.size; th = int(W * 9 / 16)
    if H > th: im = im.crop((0, (H - th) // 2, W, (H - th) // 2 + th))
    im = im.resize((w, h), Image.LANCZOS)
    d = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, fs)
    tw = d.textlength(lab, font=f)
    d.rectangle((0, h - fs - 8, tw + 10, h), fill=(0, 0, 0))
    d.text((5, h - fs - 5), lab, font=f, fill=(255, 230, 0) if lab.startswith("NOSSO") else (255, 255, 255))
    return im
def mosaic(w, h, fs, gap, out, cols=4):
    rows = [NOSSOS, REFS[:4], REFS[4:8]]
    M = Image.new("RGB", (cols * w + (cols + 1) * gap, len(rows) * h + (len(rows) + 1) * gap), (30, 30, 30))
    for r, row in enumerate(rows):
        for c, (vid, lab) in enumerate(row):
            M.paste(tile(vid, lab, w, h, fs), (gap + c * (w + gap), gap + r * (h + gap)))
    for q in (85, 75, 65, 55):
        M.save(out, quality=q)
        if os.path.getsize(out) <= 1_000_000: break
    print(out, M.size, os.path.getsize(out))
mosaic(480, 270, 18, 8, f"{B}/mosaicos/mosaico-em-relevo.jpg")
mosaic(320, 180, 13, 6, f"{B}/mosaicos/mosaico-em-relevo-celular.jpg")
