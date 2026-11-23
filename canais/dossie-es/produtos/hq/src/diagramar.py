"""HQ colorida "Expedientes Secretos #1" (v3, 23/11/2026): copiado da v2 (produtos/manga/src/diagramar.py) com
painel em polígono ("poly": calhas diagonais, pedido de diagramação mais dinâmica). Resto igual à v2.

Diagramação original do mangá "Operación Garbo": painéis sem texto (Codex) + balões, legendas e onomatopeias no código.

Por quê no código: a IA inventa letras; aqui o texto é tipografia de verdade (fontes OFL), revisável e traduzível.
Entrada: paginas.json (layout em px de uma página 6×9 pol. a 300 dpi = 1800×2700). Saída em ../:
  pagina-N.png (300 dpi, para o PDF), pagina-N.jpg (prévia ≤ 1 MB), capa.jpg, amostra.pdf.

Uso: ~/workspace/fabrica-youtube/tools/.venv/bin/python diagramar.py [paginas.json]
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
        im = Image.open(os.path.join(arte, p["img"] + ".jpg")).convert("RGB")
        self.W0, self.H0 = im.size
        z = p.get("zoom", 1.0)
        s = max(self.w / self.W0, self.h / self.H0) * z
        self.sw, self.sh = self.W0 * s, self.H0 * s
        fx, fy = p.get("foco", [0.5, 0.5])
        self.ox = min(max(fx * self.sw - self.w / 2, 0), self.sw - self.w)
        self.oy = min(max(fy * self.sh - self.h / 2, 0), self.sh - self.h)
        im = im.resize((round(self.sw), round(self.sh)), Image.LANCZOS)
        self.im = im.crop((round(self.ox), round(self.oy), round(self.ox) + round(self.w), round(self.oy) + round(self.h)))

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
        pn = Painel(p, arte)
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


def main():
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
