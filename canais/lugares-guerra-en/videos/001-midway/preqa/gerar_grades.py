#!/usr/bin/env python3
"""Pré-QA do storyboard (pré-render): um quadro-chave por plano do storyboard.json, simulado em PIL (Ficha, Número,
grifo, rótulos de mapa, cartelas), e grades por ~2 min. Só stills na VPS; nada de render de vídeo.
Uso: cd <pasta do vídeo> && ~/workspace/fabrica-youtube/tools/.venv/bin/python preqa/gerar_grades.py
Saída: preqa/quadros/Pxxx.jpg (1280x720) e preqa/grade_NN_<ini>-<fim>.jpg (3 colunas, quadro reduzido a 640 px, tempo no canto).
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None
V = Path(__file__).resolve().parent.parent
M = V / "midia"
OUT = V / "preqa"
QD = OUT / "quadros"
QD.mkdir(parents=True, exist_ok=True)
FONTES = Path.home() / "workspace/fabrica-youtube/pesquisa/canal-clima-2026-11/identidade/fontes"
W, H = 1280, 720
AMARELO, TINTA, AREIA, MAR = (253, 213, 5), (17, 20, 24), (217, 203, 168), (14, 42, 59)


def fonte(nome, tam):
    for p in [FONTES / nome, Path("/usr/share/fonts/truetype/liberation") / "LiberationSansNarrow-Bold.ttf"]:
        if p.exists():
            return ImageFont.truetype(str(p), tam)
    return ImageFont.load_default()


ANTON = lambda t: fonte("Anton-Regular.ttf", t)
MONOB = lambda t: fonte("IBMPlexMono-Bold.ttf", t)
MONO = lambda t: fonte("IBMPlexMono-Medium.ttf", t)
COND = lambda t: ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf", t)
_cache = {}


def abrir(arq, crop=None):
    k = (arq, crop)
    if k not in _cache:
        im = Image.open(M / arq)
        im.draft("RGB", (4000, 4000))
        im = im.convert("RGB")
        if crop:
            x, y, w, h = crop
            im = im.crop((int(x * im.width), int(y * im.height), int((x + w) * im.width), int((y + h) * im.height)))
        _cache[k] = im
    return _cache[k]


def enquadra(im, cx, cy, z):
    """Recorte 16:9 'cover' com zoom z centrado em (cx, cy) (frações), como o KenBurns do Remotion."""
    iw, ih = im.size
    if iw / ih > W / H:
        bh, bw = ih, ih * W / H
    else:
        bw, bh = iw, iw * H / W
    vw, vh = bw / z, bh / z
    x0 = min(max(cx * iw - vw / 2, 0), iw - vw)
    y0 = min(max(cy * ih - vh / 2, 0), ih - vh)
    return im.crop((int(x0), int(y0), int(x0 + vw), int(y0 + vh))).resize((W, H), Image.LANCZOS), vw


def ficha(d, linhas):
    if not linhas:
        return
    fs = [MONOB(22), MONO(16), MONO(16)]
    ws = [d.textlength(l, font=f) for l, f in zip(linhas, fs)]
    bw, bh = max(ws) + 34, 24 + 22 * len(linhas) + 8
    x, y = 40, H - 36 - bh
    d.rectangle((x, y, x + bw, y + bh), fill=(17, 20, 24, 220))
    d.rectangle((x, y, x + 5, y + bh), fill=AMARELO)
    yy = y + 10
    for l, f, c in zip(linhas, fs, [(255, 255, 255), (201, 205, 210), (201, 205, 210)]):
        d.text((x + 18, yy), l, font=f, fill=c)
        yy += 30 if f is fs[0] else 22


def numero_sobre(d, valor, rotulo):
    fv, fr = ANTON(76), COND(30)
    w = max(d.textlength(valor, font=fv), d.textlength(rotulo, font=fr)) + 44
    x1, y1 = W - 40, H - 36
    x0, y0 = x1 - w, y1 - 132
    d.rectangle((x0, y0, x1, y1), fill=(17, 20, 24, 225))
    d.rectangle((x1 - 5, y0, x1, y1), fill=AMARELO)
    d.text((x1 - 22, y0 + 8), valor, font=fv, fill=AMARELO, anchor="ra")
    d.text((x1 - 22, y0 + 96), rotulo, font=fr, fill=(255, 255, 255), anchor="ra")


def fundo():
    im = Image.new("RGB", (W, H), TINTA)
    d = ImageDraw.Draw(im)
    for r in range(0, 700, 20):
        c = int(42 - 30 * r / 700)
        d.ellipse((W / 2 - 900 + r, H / 2 - 520 + r * 0.58, W / 2 + 900 - r, H / 2 + 520 - r * 0.58), fill=(c, c + 4, c + 9))
    return im


def q_kb(p):
    im = abrir(p["arq"], tuple(p["crop"]) if p.get("crop") else None)
    de, pa = p["de"], p["para"]
    cx, cy, z = [(a + b) / 2 for a, b in zip(de, pa)]
    fr, vw = enquadra(im, cx, cy, z)
    p["_px_fonte"] = round(vw)
    return fr


def q_filme(p):
    t = p["tin"] + min(p["dur"] * p.get("vel", 1), p["tout"] - p["tin"]) / 2
    tmp = QD / "_f.png"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", str(M / p["arq"]), "-frames:v", "1", str(tmp)], check=True)
    im = Image.open(tmp).convert("RGB")
    p["_px_fonte"] = im.width
    return enquadra(im, 0.5, 0.5, 1.0)[0]


def q_doc(p):
    im = abrir(p["arq"])
    iw, ih = im.size
    if not p.get("grifo") and p.get("regiao"):
        x, y, w, h = p["regiao"]
        fr, vw = enquadra(im.crop((int(x * iw), int(y * ih), int((x + w) * iw), int((y + h) * ih))), 0.5, 0.5, 1.0)
        p["_px_fonte"] = round(vw)
        return fr
    if not p.get("grifo"):
        bg = fundo()
        s = (H - 60) / ih if iw / ih < W / H else (W - 80) / iw
        pg = im.resize((int(iw * s), int(ih * s)), Image.LANCZOS)
        bg.paste(pg, ((W - pg.width) // 2, (H - pg.height) // 2))
        p["_px_fonte"] = iw
        return bg
    g = p["grifo"]
    x0 = min(r[0] for r in g); x1 = max(r[0] + r[2] for r in g)
    y0 = min(r[1] for r in g); y1 = max(r[1] + r[3] for r in g)
    # zoom: a linha grifada ocupa ~78% da largura (no máx. 4x a página inteira) e fica a 42% da altura
    lw = (x1 - x0) * iw
    vw = max(lw / 0.78, iw / 4.2, 1100)
    vw = min(vw, iw)
    vh = vw * H / W
    cx, cy = (x0 + x1) / 2 * iw, (y0 + y1) / 2 * ih
    bx = min(max(cx - vw / 2, 0), iw - vw)
    by = min(max(cy - 0.42 * vh, 0), max(ih - vh, 0))
    fr = im.crop((int(bx), int(by), int(bx + vw), int(by + vh))).resize((W, H), Image.LANCZOS)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    s = W / vw
    for r in g:
        od.rectangle(((r[0] * iw - bx) * s - 4, (r[1] * ih - by) * s - 2, ((r[0] + r[2]) * iw - bx) * s + 4, ((r[1] + r[3]) * ih - by) * s + 2),
                     fill=(255, 225, 77, 140))
    fr = Image.alpha_composite(fr.convert("RGBA"), ov).convert("RGB")
    p["_px_fonte"] = round(vw)
    return fr


def q_num(p):
    im = fundo()
    d = ImageDraw.Draw(im)
    d.text((W / 2, H / 2 - 40), p["valor"], font=ANTON(190), fill=AMARELO, anchor="mm")
    d.text((W / 2, H / 2 + 110), p["rotulo"], font=COND(48), fill=(255, 255, 255), anchor="mm")
    return im


GEO = None


def q_mapa(p, pontos):
    global GEO
    if GEO is None:
        GEO = json.load(open(M / "mapa_base_ne50m_land.geojson"))["features"]
    pts = [pontos[n] for n in p["pontos"]]
    lons = [x for x, _ in pts]; lats = [y for _, y in pts]
    mn = 6 if any('WRECK' in n for n in p['pontos']) else 12
    span = max(max(lons) - min(lons), (max(lats) - min(lats)) * W / H, mn) * 1.6
    clon, clat = (max(lons) + min(lons)) / 2, (max(lats) + min(lats)) / 2
    lon0, lat_top = clon - span / 2, clat + span * H / W / 2
    sc = W / span
    pr = lambda lo, la: ((lo - lon0) * sc, (lat_top - la) * sc)
    im = Image.new("RGB", (W, H), MAR)
    d = ImageDraw.Draw(im)
    for f in GEO:
        gm = f["geometry"]
        aneis = [gm["coordinates"][0]] if gm["type"] == "Polygon" else [pl[0] for pl in gm["coordinates"]]
        for ring in aneis:
            for off in (0, 360):
                xy = [pr(c[0] + off, c[1]) for c in ring]
                if max(x for x, _ in xy) < 0 or min(x for x, _ in xy) > W:
                    continue
                if len(xy) > 2:
                    d.polygon(xy, fill=AREIA)
    fora = [n for n, (lo, la) in pontos.items() if n in p["pontos"] and not (120 <= lo <= 215 and 8 <= la <= 50)]
    for a, b, rot in p.get("linhas", []):
        xa, ya = pr(*pontos[a]); xb, yb = pr(*pontos[b])
        if (xa, ya) == (xb, yb):
            d.ellipse((xa - 26, ya - 26, xa + 26, ya + 26), outline=AMARELO, width=4)
        else:
            d.line((xa, ya, xb, yb), fill=AMARELO, width=6)
        if rot:
            d.text(((xa + xb) / 2, (ya + yb) / 2 - 30), rot, font=COND(36), fill=AMARELO, anchor="mm", stroke_width=3, stroke_fill=TINTA)
    for n in p["pontos"]:
        x, y = pr(*pontos[n])
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=AMARELO, outline=TINTA, width=3)
        k = p["pontos"].index(n)
        esq = x > W - 260 or "KAGA" in n
        dy = {1: -40, 2: 6, 3: 46}.get(k, 6) if "WRECK" in n else 6
        d.text((x - 16 if esq else x + 16, y + dy), n, font=COND(30), fill=(255, 255, 255), stroke_width=3, stroke_fill=TINTA,
               anchor="ra" if esq else "la")
    if p.get("selo"):
        selo(d, p["selo"])
    if fora:
        d.text((20, H - 40), "fora do recorte mapa_base_pacifico.json: " + ", ".join(fora), font=MONO(18), fill=(255, 120, 120))
    if p.get("nota") and "Número" in p.get("nota", ""):
        numero_sobre(d, "~40", "PEOPLE LIVE THERE")
    return im


def selo(d, txt):
    f = MONOB(22)
    w = d.textlength(txt, font=f) + 24
    d.rectangle((W - 40 - w, 34, W - 40, 72), outline=AMARELO, width=3, fill=TINTA)
    d.text((W - 40 - w / 2, 53), txt, font=f, fill=AMARELO, anchor="mm")


def q_cartela(p):
    im = fundo()
    d = ImageDraw.Draw(im)
    y = H / 2 - 40 * len(p["linhas"])
    for i, l in enumerate(p["linhas"]):
        d.text((W / 2, y + 80 * i), l, font=MONOB(40 if i else 46), fill=(255, 255, 255) if i else AMARELO, anchor="mm")
    if "DEPTH" in p["linhas"][0]:
        # perfil esquemático: superfície (y=120) a 5.600 m (y=640); marcadores nas profundidades do SCRIPT/SOURCES
        im = Image.new("RGB", (W, H), MAR)
        d = ImageDraw.Draw(im)
        z = lambda m: 120 + m / 5600 * 520
        d.rectangle((0, 0, W, 120), fill=(40, 70, 95))  # faixa do céu
        d.line((0, 120, W, 120), fill=(200, 220, 235), width=3)
        d.polygon([(0, z(5200)), (300, z(5050)), (520, z(5450)), (800, z(5350)), (1050, z(5500)), (W, z(5250)), (W, H), (0, H)], fill=AREIA)
        for m in (1000, 2000, 3000, 4000, 5000):
            d.line((60, z(m), 90, z(m)), fill=(200, 210, 220), width=2)
            d.text((96, z(m) - 12), f"{m:,} M", font=MONO(18), fill=(200, 210, 220))
        alvo = [("YORKTOWN · ~3 MI", 330, 5000), ("KAGA · ~5,400 M", 640, 5400), ("AKAGI", 900, 5450)]
        if "ROV" in " ".join(p["linhas"]):
            d.line((W - 340, 120, W - 340, z(5150)), fill=AMARELO, width=4)
            d.text((W - 328, z(2600)), "ROV DIVES > 5,100 M (2023)", font=COND(28), fill=AMARELO)
        for nome, x, m in alvo:
            d.ellipse((x - 10, z(m) - 10, x + 10, z(m) + 10), fill=AMARELO, outline=TINTA, width=3)
            d.text((x, z(m) - 40), nome, font=COND(30), fill=(255, 255, 255), anchor="mm", stroke_width=3, stroke_fill=TINTA)
        d.text((W / 2, 84), p["linhas"][1], font=MONOB(30), fill=AMARELO, anchor="mm")
        d.text((W / 2, H - 30), "SCHEMATIC · NOT TO SCALE · POSITIONS APPROXIMATE", font=MONO(18), fill=(30, 40, 50), anchor="mm")
        if p.get("selo"):
            selo(d, p["selo"])
        return im
    if p.get("selo"):
        selo(d, p["selo"])
    return im


def q_ea(p):
    a = enquadra(abrir(p["arq"]), 0.5, 0.5, 1.1)[0].convert("L").convert("RGB")
    b = enquadra(abrir(p["arq2"]), 0.5, 0.5, 1.1)[0]
    im = a.copy()
    im.paste(b.crop((W // 2, 0, W, H)), (W // 2, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((W // 2 - 3, 0, W // 2 + 3, H), fill=AMARELO)
    d.text((40, 30), p["rot1"], font=ANTON(80), fill=(255, 255, 255), stroke_width=4, stroke_fill=TINTA)
    d.text((W - 40, 30), p["rot2"], font=ANTON(80), fill=AMARELO, anchor="ra", stroke_width=4, stroke_fill=TINTA)
    p["_px_fonte"] = min(abrir(p["arq"]).width, abrir(p["arq2"]).width)
    return im


def q_card(p):
    im = fundo()
    d = ImageDraw.Draw(im)
    d.text((W / 2, 280), "CLEARANCE REQUIRED", font=ANTON(120), fill=AMARELO, anchor="mm")
    d.text((W / 2, 390), "WE GO WHERE THE RECORD GOES", font=MONOB(36), fill=(255, 255, 255), anchor="mm")
    d.text((W / 2, 480), "SUBSCRIBE", font=COND(44), fill=(255, 255, 255), anchor="mm")
    return im


def fmt(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def main():
    sb = json.load(open(V / "storyboard.json"))
    planos, pontos = sb["planos"], {k: tuple(v) for k, v in sb["pontos"].items()}
    baixa = []
    for p in planos:
        t = p["tipo"]
        im = {"KenBurns": q_kb, "Filme": q_filme, "DocGrifo": q_doc, "Número": q_num, "Cartela": q_cartela,
              "EntaoAgora": q_ea, "Card": q_card}.get(t)
        im = q_mapa(p, pontos) if t == "Mapa2D" else im(p)
        im = im.convert("RGBA")
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        if p.get("ficha"):
            ficha(d, p["ficha"])
        if p.get("num"):
            numero_sobre(d, p["num"][0], p["num"][1])
        im = Image.alpha_composite(im, ov).convert("RGB")
        p["_img"] = im
        px = p.get("_px_fonte")
        if px and t in ("KenBurns", "DocGrifo") and px < W:
            baixa.append(f"{p['id']} {p['arq']}: janela de {px} px de largura na fonte (< 1280: amplia)")
        im.save(QD / f"{p['id']}.jpg", quality=86)
    # grades por ~2 min
    CW, CH, COLS = 640, 360, 3
    grupos, atual, lim = [], [], 120
    for p in planos:
        if p["inicio"] >= lim and atual:
            grupos.append(atual); atual = []; lim += 120
        atual.append(p)
    grupos.append(atual)
    nomes = []
    for gi, g in enumerate(grupos, 1):
        rows = (len(g) + COLS - 1) // COLS
        S = Image.new("RGB", (COLS * CW, rows * CH), (0, 0, 0))
        for i, p in enumerate(g):
            th = p["_img"].resize((CW - 6, CH - 6), Image.LANCZOS)
            d = ImageDraw.Draw(th)
            lab = f"{p['id']} {fmt(p['inicio'])} {p['dur']:.1f}s {p['tipo']}{' REUSO' if p.get('reuso') else ''}"
            d.rectangle((0, 0, d.textlength(lab, font=MONOB(17)) + 12, 26), fill=(0, 0, 0))
            d.text((6, 3), lab, font=MONOB(17), fill=AMARELO)
            S.paste(th, ((i % COLS) * CW + 3, (i // COLS) * CH + 3))
        nome = OUT / f"grade_{gi:02d}_{fmt(g[0]['inicio']).replace(':', 'm')}-{fmt(g[-1]['inicio'] + g[-1]['dur']).replace(':', 'm')}.jpg"
        S.save(nome, quality=82)
        nomes.append(nome.name)
    (QD / "_f.png").unlink(missing_ok=True)
    print("\n".join(nomes))
    print(f"{len(planos)} quadros em preqa/quadros/")
    for b in baixa:
        print("RESOLUÇÃO:", b)


if __name__ == "__main__":
    main()
