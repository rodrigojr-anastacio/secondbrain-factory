"""HQ colorida "Expedientes Secretos #1" (v3, 23/11/2026): copiado da v2 (produtos/manga/src/diagramar.py) com
painel em polígono ("poly": calhas diagonais, pedido de diagramação mais dinâmica). Resto igual à v2.

Diagramação original do mangá "Operación Garbo": painéis sem texto (Codex) + balões, legendas e onomatopeias no código.

Por quê no código: a IA inventa letras; aqui o texto é tipografia de verdade (fontes OFL), revisável e traduzível.
Entrada: paginas.json (layout em px de uma página 6×9 pol. a 300 dpi = 1800×2700). Saída em ../:
  pagina-N.png (300 dpi, para o PDF), pagina-N.jpg (prévia ≤ 1 MB), capa.jpg, amostra.pdf.

Uso: ~/workspace/fabrica-youtube/tools/.venv/bin/python diagramar.py [paginas.json]
     ~/workspace/fabrica-youtube/tools/.venv/bin/python diagramar.py --livro ../001/livro.json   (PDF inteiro; ver LIVRO)
Painel: "arte_dir" opcional por painel (relativo a ../); sem o .jpg → placeholder cinza com id + "placeholder".
Coordenadas dos balões: "pos" = centro do balão em fração do retângulo do painel (pode vazar do painel);
"alvo" = ponta do rabicho em fração da IMAGEM original do painel (a boca do personagem), convertido pelo recorte.
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.abspath(os.path.join(AQUI, ".."))
F = os.path.join(AQUI, "fontes")
K = 2  # desenha em 2× e reduz (antialias)
W, H = 1800, 2700
PAPEL = {"manga": (255, 255, 255), "cor": (233, 223, 201)}
VERMELHO = (179, 38, 30)
PRETO = (17, 17, 17)


def fonte(nome, px):
    arq = {"fala": "ComicNeue-Bold.ttf", "fala-it": "ComicNeue-BoldItalic.ttf", "sfx": "Bangers-Regular.ttf",
           "titulo": "BebasNeue-Regular.ttf", "carta": "SpecialElite-Regular.ttf"}[nome]
    return ImageFont.truetype(os.path.join(F, arq), int(px * K))


def quebrar(texto, f, largura, d):
    linhas = []
    for par in texto.split("\n"):
        atual = ""
        for p in par.split():
            teste = (atual + " " + p).strip()
            if d.textlength(teste, font=f) <= largura or not atual:
                atual = teste
            else:
                linhas.append(atual)
                atual = p
        linhas.append(atual)
    return linhas


def bloco(d, linhas, f, entrelinha=1.12):
    asc, desc = f.getmetrics()
    lh = (asc + desc) * entrelinha
    larg = max(d.textlength(l, font=f) for l in linhas)
    return larg, lh * len(linhas), lh


def escrever(d, cx, cy, linhas, f, lh, cor=PRETO, alinhar="centro", x0=None):
    y = cy - lh * len(linhas) / 2
    for l in linhas:
        lw = d.textlength(l, font=f)
        x = cx - lw / 2 if alinhar == "centro" else x0
        d.text((x, y), l, font=f, fill=cor)
        y += lh


class Painel:
    def __init__(self, p, arte):
        self.poly = None
        if "poly" in p:  # polígono em px da página; o retângulo vira a caixa envolvente
            xs, ys = [q[0] for q in p["poly"]], [q[1] for q in p["poly"]]
            p = dict(p, rect=[min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)])
            self.poly = [(q[0] * K, q[1] * K) for q in p["poly"]]
        self.x, self.y, self.w, self.h = [v * K for v in p["rect"]]
        arq = os.path.join(arte, p["img"] + ".jpg")
        if not os.path.exists(arq):  # e1 (24/11/2026): arte ainda não gerada → placeholder cinza do tamanho do quadro
            self.placeholder(p)
            return
        im = Image.open(arq).convert("RGB")
        self.W0, self.H0 = im.size
        z = p.get("zoom", 1.0)
        s = max(self.w / self.W0, self.h / self.H0) * z
        self.sw, self.sh = self.W0 * s, self.H0 * s
        fx, fy = p.get("foco", [0.5, 0.5])
        self.ox = min(max(fx * self.sw - self.w / 2, 0), self.sw - self.w)
        self.oy = min(max(fy * self.sh - self.h / 2, 0), self.sh - self.h)
        im = im.resize((round(self.sw), round(self.sh)), Image.LANCZOS)
        self.im = im.crop((round(self.ox), round(self.oy), round(self.ox) + round(self.w), round(self.oy) + round(self.h)))

    def placeholder(self, p):
        w, h = round(self.w), round(self.h)
        im = Image.new("RGB", (w, h), (158, 158, 158))
        d = ImageDraw.Draw(im)
        for i in range(-h, w, 60 * K):  # hachura leve para não parecer arte pronta
            d.line([(i, h), (i + h, 0)], fill=(150, 150, 150), width=2 * K)
        fid = fonte("titulo", 64 if w > 700 * K else 44)
        d.text((24 * K, 14 * K), p["img"] + "  ·  " + p.get("orient", ""), font=fid, fill=(60, 60, 60))
        txt = p.get("placeholder", "")
        if txt:
            f = ImageFont.truetype(os.path.join(F, "ComicNeue-Regular.ttf"), int(30 * K))
            linhas = quebrar(txt, f, w - 48 * K, d)
            y = 90 * K
            for ln in linhas:
                if y > h - 40 * K:
                    break
                d.text((24 * K, y), ln, font=f, fill=(45, 45, 45))
                y += 36 * K
        self.im, self.W0, self.H0 = im, w, h
        self.sw, self.sh, self.ox, self.oy = w, h, 0, 0

    def img2pag(self, u, v):
        return self.x + u * self.sw - self.ox, self.y + v * self.sh - self.oy

    def frac2pag(self, a, b):
        return self.x + a * self.w, self.y + b * self.h


def balao_fala(d, cx, cy, linhas, f, lh, tx, ty, estilo, grito=False):
    tw, th, _ = bloco(d, linhas, f)
    a, b = (tw / 2 + 20 * K) * 1.10, (th / 2 + 14 * K) * 1.28
    s = 5 * K
    # rabicho: base em 2 pontos do contorno virados para o alvo
    ang = math.atan2(ty - cy, tx - cx)
    abre = 0.22
    p1 = (cx + a * 0.8 * math.cos(ang - abre), cy + b * 0.8 * math.sin(ang - abre))
    p2 = (cx + a * 0.8 * math.cos(ang + abre), cy + b * 0.8 * math.sin(ang + abre))
    cauda = [p1, (tx, ty), p2]
    if grito:  # balão de grito: estrela
        pts = []
        n = 22
        for i in range(n * 2):
            r = 1.18 if i % 2 == 0 else 0.98
            t = math.pi * i / n
            pts.append((cx + a * r * math.cos(t), cy + b * r * math.sin(t)))
        d.polygon(pts, fill="white", outline=PRETO, width=s)
        d.polygon(cauda, fill="white", outline=PRETO, width=s)
        d.polygon([(cx + (x - cx) * 0.93, cy + (y - cy) * 0.93) for x, y in pts], fill="white")
    else:
        d.ellipse((cx - a - s, cy - b - s, cx + a + s, cy + b + s), fill=PRETO)
        d.line(cauda, fill=PRETO, width=s * 2, joint="curve")
        d.polygon(cauda, fill="white")
        d.ellipse((cx - a, cy - b, cx + a, cy + b), fill="white")
    escrever(d, cx, cy, linhas, f, lh)


def balao_pensa(d, cx, cy, linhas, f, lh, tx, ty):
    tw, th, _ = bloco(d, linhas, f)
    a, b = (tw / 2 + 22 * K) * 1.12, (th / 2 + 18 * K) * 1.30
    s = 4 * K
    n = 14
    bolhas = []
    for i in range(n):
        t = 2 * math.pi * i / n
        r = (a + b) * 0.16
        bolhas.append((cx + a * 0.92 * math.cos(t), cy + b * 0.88 * math.sin(t), r))
    for x, y, r in bolhas:
        d.ellipse((x - r - s, y - r - s, x + r + s, y + r + s), fill=PRETO)
    d.ellipse((cx - a - s, cy - b - s, cx + a + s, cy + b + s), fill=PRETO)
    for x, y, r in bolhas:
        d.ellipse((x - r, y - r, x + r, y + r), fill="white")
    d.ellipse((cx - a, cy - b, cx + a, cy + b), fill="white")
    # trilha de bolinhas até o personagem
    ang = math.atan2(ty - cy, tx - cx)
    ex, ey = cx + a * 1.05 * math.cos(ang), cy + b * 1.05 * math.sin(ang)
    for i, r in enumerate((18, 12, 8)):
        k = 0.25 + 0.3 * i
        x, y = ex + (tx - ex) * k, ey + (ty - ey) * k
        r *= K
        d.ellipse((x - r - s, y - r - s, x + r + s, y + r + s), fill=PRETO)
        d.ellipse((x - r, y - r, x + r, y + r), fill="white")
    escrever(d, cx, cy, linhas, f, lh)


def legenda(d, x, y, larg, texto, estilo, carta=False, px=30):
    f = fonte("carta" if carta else "fala", px)
    if not carta:
        texto = texto.upper()
    pad = 16 * K
    linhas = quebrar(texto, f, larg - 2 * pad, d)
    tw, th, lh = bloco(d, linhas, f, 1.08)
    w = min(larg, tw + 2 * pad + (10 * K if estilo == "cor" else 0))
    h = th + 2 * pad - 6 * K
    fundo = (245, 240, 228) if carta else ((233, 223, 201) if estilo == "cor" else (255, 255, 255))
    d.rectangle((x, y, x + w, y + h), fill=fundo, outline=PRETO, width=4 * K)
    x_txt = x + pad
    if estilo == "cor" and not carta:
        d.rectangle((x + 4 * K, y + 4 * K, x + 14 * K, y + h - 4 * K), fill=VERMELHO)
        x_txt += 10 * K
    yy = y + pad - 4 * K
    for l in linhas:
        d.text((x_txt, yy), l, font=f, fill=PRETO)
        yy += lh
    return h


def sfx(base, x, y, texto, px, rot, cor):
    f = fonte("sfx", px)
    tmp = Image.new("RGBA", (int(px * K * len(texto) * 0.9 + 80 * K), int(px * K * 1.8)), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.text((40 * K, 20 * K), texto, font=f, fill=cor, stroke_width=int(px * K * 0.09), stroke_fill="white")
    tmp = tmp.rotate(rot, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(tmp, (int(x - tmp.width / 2), int(y - tmp.height / 2)))


def pagina(pg, estilo_padrao):
    estilo = pg.get("estilo", estilo_padrao)
    arte = os.path.join(SAIDA, pg.get("arte", "arte"))
    base = Image.new("RGBA", (W * K, H * K), PAPEL[estilo] + (255,))
    d = ImageDraw.Draw(base)
    paineis = {}
    for p in pg["paineis"]:
        pn = Painel(p, os.path.join(SAIDA, p["arte_dir"]) if p.get("arte_dir") else arte)
        paineis[p["img"]] = pn
        if pn.poly:
            m = Image.new("L", base.size, 0)
            ImageDraw.Draw(m).polygon(pn.poly, fill=255)
            camada = Image.new("RGB", base.size)
            camada.paste(pn.im, (round(pn.x), round(pn.y)))
            base.paste(camada, (0, 0), m)
            d.line(pn.poly + [pn.poly[0]], fill=PRETO, width=7 * K, joint="curve")
        else:
            base.paste(pn.im, (round(pn.x), round(pn.y)))
            d.rectangle((pn.x, pn.y, pn.x + pn.w, pn.y + pn.h), outline=PRETO, width=7 * K)
    for e in pg.get("textos", []):
        t = e["tipo"]
        pn = paineis.get(e.get("painel"))
        if t in ("fala", "grito", "pensa"):
            px = e.get("px", 36)
            f = fonte("fala", px)
            linhas = quebrar(e["texto"].upper(), f, e.get("larg", 360) * K, d)
            _, _, lh = bloco(d, linhas, f)
            cx, cy = pn.frac2pag(*e["pos"])
            tx, ty = pn.img2pag(*e["alvo"])
            if t == "pensa":
                balao_pensa(d, cx, cy, linhas, f, lh, tx, ty)
            else:
                balao_fala(d, cx, cy, linhas, f, lh, tx, ty, estilo, grito=(t == "grito"))
        elif t in ("legenda", "carta"):
            x, y = pn.frac2pag(*e["pos"])
            legenda(d, x, y, e.get("larg", 600) * K, e["texto"], estilo, carta=(t == "carta"), px=e.get("px", 30))
        elif t == "sfx":
            x, y = pn.frac2pag(*e["pos"])
            cor = VERMELHO if e.get("cor") == "vermelho" else PRETO
            sfx(base, x, y, e["texto"], e.get("px", 90), e.get("rot", 8), cor)
            d = ImageDraw.Draw(base)
    # cabeçalho e rodapé
    ft = fonte("titulo", 34)
    if pg.get("cabecalho"):
        d.text((80 * K, 62 * K), pg["cabecalho"], font=ft, fill=VERMELHO if estilo == "manga" else PRETO)
    if pg.get("numero"):
        n = str(pg["numero"])
        d.text(((W - 80) * K - d.textlength(n, font=ft), (H - 72) * K), n, font=ft, fill=PRETO)
        marca = "DOSSIER EN MINUTOS"
        d.text((80 * K, (H - 72) * K), marca, font=fonte("titulo", 26), fill=(120, 120, 120))
    return base.convert("RGB").resize((W, H), Image.LANCZOS)


def capa(c):
    base = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 255))
    im = Image.open(os.path.join(SAIDA, c["img"])).convert("RGB")
    s = max(W * K / im.width, H * K / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    ox = (im.width - W * K) // 2
    oy = int((im.height - H * K) * c.get("foco_y", 0.5))
    base.paste(im.crop((ox, oy, ox + W * K, oy + H * K)), (0, 0))
    # escurece o topo para o título
    grad = Image.new("L", (1, H * K))
    for y in range(H * K):
        t = max(0.0, 1 - y / (H * K * 0.42))
        grad.putpixel((0, y), int(235 * t ** 1.3))
    sombra = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 255))
    sombra.putalpha(grad.resize((W * K, H * K)))
    base.alpha_composite(sombra)
    d = ImageDraw.Draw(base)
    ft = fonte("titulo", 44)
    topo = "DOSSIER EN MINUTOS  ·  EXPEDIENTE ESPECIAL Nº 1"
    d.text(((W * K - d.textlength(topo, font=ft)) / 2, 48 * K), topo, font=ft, fill=(233, 223, 201))
    for i, (txt, px) in enumerate((("OPERACIÓN", 210), ("GARBO", 330))):
        f = fonte("sfx", px)
        y = (175 if i == 0 else 355) * K
        x = (W * K - d.textlength(txt, font=f)) / 2
        d.text((x + 12 * K, y + 12 * K), txt, font=f, fill=VERMELHO, stroke_width=10 * K, stroke_fill=VERMELHO)
        d.text((x, y), txt, font=f, fill="white", stroke_width=10 * K, stroke_fill=PRETO)
    sub = "EL ESPAÑOL QUE ENGAÑÓ A HITLER"
    fs = fonte("titulo", 92)
    d.text(((W * K - d.textlength(sub, font=fs)) / 2, 720 * K), sub, font=fs, fill=(233, 223, 201),
           stroke_width=3 * K, stroke_fill=PRETO)
    # carimbo
    car = Image.new("RGBA", (760 * K, 170 * K), (0, 0, 0, 0))
    dc = ImageDraw.Draw(car)
    dc.rectangle((8 * K, 8 * K, 752 * K, 162 * K), outline=VERMELHO, width=9 * K)
    fc = fonte("titulo", 104)
    t = "HECHOS REALES"
    dc.text(((760 * K - dc.textlength(t, font=fc)) / 2, 26 * K), t, font=fc, fill=VERMELHO)
    car = car.rotate(-9, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(car, (int(W * K - car.width - 60 * K), int(H * K - car.height - 260 * K)))
    rod = "UN MANGA DE ESPIONAJE  ·  MADRID · LISBOA · LONDRES · NORMANDÍA  ·  1941–1944"
    fr = fonte("titulo", 38)
    d.rectangle((0, (H - 120) * K, W * K, H * K), fill=(17, 17, 17, 255))
    d.text(((W * K - d.textlength(rod, font=fr)) / 2, (H - 92) * K), rod, font=fr, fill=(233, 223, 201))
    return base.convert("RGB").resize((W, H), Image.LANCZOS)


def salvar_previa(im, nome, larg=1200):
    p = im.resize((larg, round(im.height * larg / im.width)), Image.LANCZOS)
    q = 88
    while True:
        p.save(os.path.join(SAIDA, nome), "JPEG", quality=q, optimize=True, progressive=True)
        if os.path.getsize(os.path.join(SAIDA, nome)) <= 1_000_000 or q <= 50:
            break
        q -= 6
    print(nome, p.size, os.path.getsize(os.path.join(SAIDA, nome)) // 1024, "KB")


LIVRO = """
Modo livro (e1 da #1, 24/11/2026): `diagramar.py --livro <livro.json>` monta o PDF inteiro (capa, créditos, sumário,
capas das histórias, páginas de quadros, "Lo que es real", pôster, final, contracapa). Arte que ainda não existe vira
placeholder cinza com o id e a descrição do quadro. Tipos de página ("tipo"):
  quadros (padrão)  = página de HQ igual às da amostra (paineis + textos)
  imagem            = página inteira com uma imagem pronta ("img": caminho relativo a ../) ou placeholder
  capa_historia     = arte de página inteira ("img") + título da história, "EXPEDIENTE N", ano/lugar, carimbo
  texto             = papel + título + blocos [{"t": "h"|"p"|"carta"|"item", "texto": ...}] + "caixa" opcional
                      (placeholder de miniatura/QR: {"rotulo", "rect"})
Chaves do livro: "saida_dir" (pngs/jpgs, relativo a ../), "pdf" (relativo a ../), "larg_pdf" (px por página no PDF).
"""


def _cobrir(arq, w, h, rotulo, desc=""):
    if arq and os.path.exists(arq):
        im = Image.open(arq).convert("RGB")
        s = max(w / im.width, h / im.height)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        return im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))
    pn = Painel.__new__(Painel)
    pn.w, pn.h = w, h
    pn.placeholder({"img": rotulo, "placeholder": desc})
    return pn.im


def pagina_imagem(pg):
    im = _cobrir(os.path.join(SAIDA, pg["img"]) if pg.get("img") else None, W * K, H * K,
                 pg.get("rotulo", "IMAGEN"), pg.get("placeholder", ""))
    return im.resize((W, H), Image.LANCZOS)


def pagina_capa_historia(pg):
    base = _cobrir(os.path.join(SAIDA, "arte-001", pg["img"] + ".jpg") if pg.get("img") else None, W * K, H * K,
                   pg.get("img", "CAPA"), pg.get("placeholder", "")).convert("RGBA")
    grad = Image.new("L", (1, H * K))
    for y in range(H * K):
        t = max(0.0, 1 - y / (H * K * 0.38))
        b = max(0.0, (y / (H * K) - 0.82) / 0.18)
        grad.putpixel((0, y), int(230 * max(t ** 1.3, b ** 1.2)))
    sombra = Image.new("RGBA", (W * K, H * K), (8, 10, 18, 255))
    sombra.putalpha(grad.resize((W * K, H * K)))
    base.alpha_composite(sombra)
    d = ImageDraw.Draw(base)
    ft = fonte("titulo", 48)
    topo = pg.get("topo", "EXPEDIENTES SECRETOS #1")
    d.text(((W * K - d.textlength(topo, font=ft)) / 2, 60 * K), topo, font=ft, fill=(233, 223, 201))
    exp = pg.get("expediente", "")
    fe = fonte("titulo", 70)
    d.text(((W * K - d.textlength(exp, font=fe)) / 2, 140 * K), exp, font=fe, fill=VERMELHO)
    y = 240 * K
    for txt in pg["titulo"].split("\n"):
        px = 300 if len(txt) <= 8 else 230
        f = fonte("sfx", px)
        while d.textlength(txt, font=f) > (W - 160) * K:
            px -= 10
            f = fonte("sfx", px)
        x = (W * K - d.textlength(txt, font=f)) / 2
        d.text((x + 12 * K, y + 12 * K), txt, font=f, fill=VERMELHO, stroke_width=10 * K, stroke_fill=VERMELHO)
        d.text((x, y), txt, font=f, fill="white", stroke_width=10 * K, stroke_fill=PRETO)
        y += int(px * 1.02) * K
    sub = pg.get("subtitulo", "")
    fs = fonte("titulo", 76)
    d.text(((W * K - d.textlength(sub, font=fs)) / 2, y + 20 * K), sub, font=fs, fill=(233, 223, 201),
           stroke_width=3 * K, stroke_fill=PRETO)
    rod = pg.get("rodape", "")
    fr = fonte("titulo", 54)
    d.text(((W * K - d.textlength(rod, font=fr)) / 2, (H - 150) * K), rod, font=fr, fill=(233, 223, 201))
    car = Image.new("RGBA", (620 * K, 150 * K), (0, 0, 0, 0))
    dc = ImageDraw.Draw(car)
    dc.rectangle((8 * K, 8 * K, 612 * K, 142 * K), outline=VERMELHO, width=8 * K)
    fc = fonte("titulo", 90)
    t = "HECHOS REALES"
    dc.text(((620 * K - dc.textlength(t, font=fc)) / 2, 22 * K), t, font=fc, fill=VERMELHO)
    car = car.rotate(-8, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(car, (int(W * K - car.width - 70 * K), int(H * K - car.height - 260 * K)))
    return base.convert("RGB").resize((W, H), Image.LANCZOS)


def pagina_texto(pg):
    escuro = pg.get("escuro", False)
    fundo, tinta = ((17, 17, 17), (233, 223, 201)) if escuro else (PAPEL["cor"], PRETO)
    base = Image.new("RGB", (W * K, H * K), fundo)
    d = ImageDraw.Draw(base)
    y = 160 * K
    if pg.get("titulo"):
        f = fonte("titulo", pg.get("px_titulo", 120))
        for ln in quebrar(pg["titulo"], f, (W - 240) * K, d):
            d.text(((W * K - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=VERMELHO)
            y += int(pg.get("px_titulo", 120) * 1.0) * K
        d.line([(300 * K, y + 20 * K), ((W - 300) * K, y + 20 * K)], fill=VERMELHO, width=5 * K)
        y += 70 * K
    x0, larg = 150 * K, (W - 300) * K
    for b in pg.get("blocos", []):
        t = b.get("t", "p")
        px = b.get("px", {"h": 62, "p": 42, "carta": 36, "item": 38, "pequeno": 31}[t])
        f = fonte("titulo", px) if t == "h" else (fonte("carta", px) if t == "carta" else
                                                  ImageFont.truetype(os.path.join(F, "ComicNeue-Bold.ttf" if t != "pequeno" else "ComicNeue-Regular.ttf"), int(px * K)))
        cor = VERMELHO if t == "h" else tinta
        recuo = 34 * K if t == "item" else 0
        texto = ("•  " + b["texto"]) if t == "item" else b["texto"]
        linhas = quebrar(texto, f, larg - recuo, d)
        _, _, lh = bloco(d, linhas, f, 1.15)
        for ln in linhas:
            if b.get("centro"):
                d.text(((W * K - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=cor)
            else:
                d.text((x0 + recuo, y), ln, font=f, fill=cor)
            y += lh
        y += (14 if t in ("item", "pequeno") else 30) * K
    for cx in pg.get("caixas", []):
        x, yy, w, h = [v * K for v in cx["rect"]]
        img = cx.get("img")
        im = _cobrir(os.path.join(SAIDA, img) if img else None, round(w), round(h), cx.get("rotulo", ""),
                     cx.get("placeholder", ""))
        base.paste(im, (round(x), round(yy)))
        d.rectangle((x, yy, x + w, yy + h), outline=tinta, width=5 * K)
    for tl in pg.get("textos_livres", []):  # texto posicionado (ex.: link ao lado do QR); {"pos":[x,y],"larg","texto","px","cor"}
        f = fonte("titulo", tl.get("px", 44))
        x, yy = tl["pos"][0] * K, tl["pos"][1] * K
        cor = VERMELHO if tl.get("cor") == "vermelho" else tinta
        for ln in quebrar(tl["texto"], f, tl.get("larg", 700) * K, d):
            d.text((x, yy), ln, font=f, fill=cor)
            yy += int(tl.get("px", 44) * 1.15) * K
        if tl.get("sublinhado"):
            d.line([(x, yy + 4 * K), (x + min(tl.get("larg", 700) * K, d.textlength(tl["texto"], font=f)), yy + 4 * K)],
                   fill=cor, width=3 * K)
    if pg.get("numero"):
        ft = fonte("titulo", 34)
        n = str(pg["numero"])
        d.text(((W - 80) * K - d.textlength(n, font=ft), (H - 72) * K), n, font=ft, fill=tinta)
    return base.resize((W, H), Image.LANCZOS)


def livro(arq):
    cfg = json.load(open(arq))
    pasta = os.path.join(SAIDA, cfg.get("saida_dir", "001/rascunho"))
    os.makedirs(pasta, exist_ok=True)
    larg = cfg.get("larg_pdf", 1200)
    folhas = []
    for i, pg in enumerate(cfg["paginas"], 1):
        tipo = pg.get("tipo", "quadros")
        if tipo == "quadros":
            im = pagina(pg, cfg.get("estilo", "cor"))
        elif tipo == "imagem":
            im = pagina_imagem(pg)
        elif tipo == "capa_historia":
            im = pagina_capa_historia(pg)
        else:
            im = pagina_texto(pg)
        nome = "p%02d-%s" % (i, pg.get("saida", tipo))
        p = im.resize((larg, round(H * larg / W)), Image.LANCZOS)
        p.save(os.path.join(pasta, nome + ".jpg"), "JPEG", quality=82, optimize=True)
        folhas.append(p)
        print(nome, flush=True)
    pdf = os.path.join(SAIDA, cfg.get("pdf", "001/rascunho.pdf"))
    folhas[0].save(pdf, "PDF", resolution=larg / 6, save_all=True, append_images=folhas[1:], quality=82)
    print(os.path.relpath(pdf, SAIDA), len(folhas), "páginas", os.path.getsize(pdf) // 1024, "KB")


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--livro":
        return livro(sys.argv[2])
    cfg = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "paginas.json")))
    folhas = []
    c = capa(cfg["capa"])
    c.save(os.path.join(SAIDA, "capa.png"), dpi=(300, 300))
    salvar_previa(c, "capa.jpg")
    folhas.append(c)
    for pg in cfg["paginas"]:
        im = pagina(pg, cfg.get("estilo", "manga"))
        im.save(os.path.join(SAIDA, pg["saida"] + ".png"), dpi=(300, 300))
        salvar_previa(im, pg["saida"] + ".jpg")
        folhas.append(im)
    pdf = os.path.join(SAIDA, "amostra.pdf")
    folhas[0].save(pdf, "PDF", resolution=300, save_all=True, append_images=folhas[1:], quality=90)
    print("amostra.pdf", len(folhas), "páginas", os.path.getsize(pdf) // 1024, "KB")


if __name__ == "__main__":
    main()
