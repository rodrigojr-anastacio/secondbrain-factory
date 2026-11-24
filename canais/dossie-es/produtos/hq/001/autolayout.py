"""Posição automática dos balões olhando a arte (e2, 24/11/2026).

O montar.py põe os textos em posições fixas (rascunho); com as artes prontas, isto aqui reposiciona cada balão:
- rostos detectados na arte (OpenCV Haar: frente + perfil; cache em rostos.json) viram zonas a evitar;
- balão e legenda ficam inteiros dentro do quadro (polígono incluso) e sem encostar uns nos outros;
- ordem de leitura: cada fala abaixo/à direita da anterior; lado preferido = 4º elemento do texto (e/d/c);
- rabicho aponta para a boca do rosto do lado de quem fala (sem rosto: mantém o alvo do rascunho);
- legendas tentam os 4 cantos e ficam no que não tapa rosto.
Ajuste fino manual continua valendo: o dict do 5º elemento do texto no roteiro (pos/alvo/larg/px) prevalece.
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
HQ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(HQ, "src"))
import diagramar as dg  # noqa: E402

K = dg.K
_D = ImageDraw.Draw(Image.new("RGB", (10, 10)))
CACHE = os.path.join(AQUI, "rostos.json")
_rostos = None
MARGEM = 18        # px da página entre balão e borda do quadro
FOLGA = 14         # px entre textos


def _cache():
    global _rostos
    if _rostos is None:
        _rostos = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    return _rostos


def salvar_cache():
    if _rostos is not None:
        json.dump(_rostos, open(CACHE, "w"), indent=0)


def rostos(arq):
    """Retângulos [x, y, w, h] (px da imagem) dos rostos; cache por caminho + mtime."""
    c = _cache()
    chave = "%s|%d" % (os.path.relpath(arq, HQ), int(os.path.getmtime(arq)))
    if chave in c:
        return c[chave]
    import cv2
    im = cv2.imread(arq, 0)
    h, w = im.shape
    mn = (max(24, w // 30), max(24, w // 30))
    fr = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    pr = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
    caixas = [list(map(int, r)) for r in fr.detectMultiScale(im, 1.1, 5, minSize=mn)]
    caixas += [list(map(int, r)) for r in pr.detectMultiScale(im, 1.1, 5, minSize=mn)]
    flip = cv2.flip(im, 1)
    caixas += [[w - int(x) - int(ww), int(y), int(ww), int(hh)] for x, y, ww, hh in pr.detectMultiScale(flip, 1.1, 5, minSize=mn)]
    # funde sobrepostos (frente e perfil do mesmo rosto)
    out = []
    for r in sorted(caixas, key=lambda r: -r[2] * r[3]):
        if all(_inter(r, o) < 0.4 * r[2] * r[3] for o in out):
            out.append(r)
    c[chave] = out
    return out


def _inter(a, b):
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[0] + a[2], b[0] + b[2]), min(a[1] + a[3], b[1] + b[3])
    return max(0, x2 - x1) * max(0, y2 - y1)


def _dentro_poly(px, py, poly):
    dentro = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1 + 1e-9) + x1:
            dentro = not dentro
    return dentro


class Geo:
    """Geometria do quadro na página (igual ao diagramar.Painel) para converter imagem ↔ página."""

    def __init__(self, painel, slot, arq):
        self.box = slot["rect"] if "rect" in slot else None
        self.poly = slot.get("poly")
        if self.poly:
            xs, ys = [p[0] for p in self.poly], [p[1] for p in self.poly]
            self.box = [min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)]
        self.x, self.y, self.w, self.h = self.box
        im = Image.open(arq)
        self.W0, self.H0 = im.size
        z = painel.get("zoom", 1.0)
        s = max(self.w / self.W0, self.h / self.H0) * z
        self.s = s
        self.sw, self.sh = self.W0 * s, self.H0 * s
        fx, fy = painel.get("foco", [0.5, 0.5])
        self.ox = min(max(fx * self.sw - self.w / 2, 0), self.sw - self.w)
        self.oy = min(max(fy * self.sh - self.h / 2, 0), self.sh - self.h)

    def img2pag(self, u, v):        # u, v em fração da imagem
        return self.x + u * self.sw - self.ox, self.y + v * self.sh - self.oy

    def pag2img(self, X, Y):
        return (X - self.x + self.ox) / self.sw, (Y - self.y + self.oy) / self.sh

    def pag2frac(self, X, Y):
        return (X - self.x) / self.w, (Y - self.y) / self.h

    def rosto_pag(self, r):
        X, Y = self.img2pag(r[0] / self.W0, r[1] / self.H0)
        return [X, Y, r[2] * self.s, r[3] * self.s]

    def contem_rect(self, r, m=MARGEM):
        x, y, w, h = r
        if x < self.x + m or y < self.y + m or x + w > self.x + self.w - m or y + h > self.y + self.h - m:
            return False
        if self.poly:
            for px, py in ((x, y), (x + w, y), (x, y + h), (x + w, y + h), (x + w / 2, y), (x + w / 2, y + h),
                           (x, y + h / 2), (x + w, y + h / 2)):
                if not _dentro_poly(px, py, self.poly):
                    return False
        return True

    def contem_elipse(self, cx, cy, a, b, m=MARGEM):
        if not (self.x + m <= cx - a and cx + a <= self.x + self.w - m and self.y + m <= cy - b
                and cy + b <= self.y + self.h - m):
            return False
        if self.poly:
            for i in range(12):
                t = 2 * math.pi * i / 12
                if not _dentro_poly(cx + (a + m) * math.cos(t), cy + (b + m) * math.sin(t), self.poly):
                    return False
        return True


def medida(e):
    """Tamanho em px da página: balões → semi-eixos (a, b) da elipse com folga das bolhas; legendas → (w, h)."""
    t = e["tipo"]
    if t in ("fala", "grito", "pensa"):
        f = dg.fonte("fala", e.get("px", 36))
        linhas = dg.quebrar(e["texto"].upper(), f, e.get("larg", 360) * K, _D)
        tw, th, _ = dg.bloco(_D, linhas, f)
        if t == "pensa":
            a, b = (tw / 2 + 22 * K) * 1.12, (th / 2 + 18 * K) * 1.30
            r = (a + b) * 0.16
            a, b = a * 0.92 + r, b * 0.88 + r
        else:
            a, b = (tw / 2 + 20 * K) * 1.10, (th / 2 + 14 * K) * 1.28
            if t == "grito":
                a, b = a * 1.18, b * 1.18
        return a / K + 5, b / K + 5
    if t in ("legenda", "carta"):
        px = e.get("px", 30)
        f = dg.fonte("carta" if t == "carta" else "fala", px)
        texto = e["texto"] if t == "carta" else e["texto"].upper()
        pad = 16 * K
        larg = e.get("larg", 600) * K
        linhas = dg.quebrar(texto, f, larg - 2 * pad, _D)
        tw, th, _ = dg.bloco(_D, linhas, f, 1.08)
        return min(larg, tw + 2 * pad + 10 * K) / K, (th + 2 * pad - 6 * K) / K
    return None


def _custo_rostos(r, faces, peso=1.0):
    c = 0.0
    for f in faces:
        i = _inter(r, f)
        if i:
            c += 4000 * peso * i / (f[2] * f[3])
    return c


def _sobrepoe(r, ocupados):
    return any(_inter([r[0] - FOLGA, r[1] - FOLGA, r[2] + 2 * FOLGA, r[3] + 2 * FOLGA], o) > 0 for o in ocupados)


def layout_quadro(painel, slot, arq, textos):
    """Reposiciona os textos de UM quadro (lista de dicts do livro.json, na ordem do roteiro)."""
    if not os.path.exists(arq) or not textos:
        return textos
    g = Geo(painel, slot, arq)
    faces = [g.rosto_pag(r) for r in rostos(arq)]
    faces = [f for f in faces if _inter(f, g.box) > 0.5 * f[2] * f[3]]
    ocupados = []
    # 1) legendas/cartas: cantos, na ordem; mantêm o canto do rascunho se não taparem rosto
    n_leg = 0
    for e in textos:
        if e["tipo"] not in ("legenda", "carta"):
            continue
        manual = e.get("_manual", set())
        w, h = medida(e)
        if "pos" in manual:
            X, Y = g.img2pag(0, 0)[0] * 0 + g.x + e["pos"][0] * g.w, g.y + e["pos"][1] * g.h
            ocupados.append([X, Y, w, h])
            n_leg += 1
            continue
        m = 10
        cantos = {"TL": (g.x + m, g.y + m), "TR": (g.x + g.w - w - m, g.y + m),
                  "BL": (g.x + m, g.y + g.h - h - m), "BR": (g.x + g.w - w - m, g.y + g.h - h - m)}
        ordem = (["TL", "TR", "BL", "BR"] if n_leg == 0 else ["BL", "BR", "TR", "TL"] if n_leg == 1
                 else ["TR", "BR", "TL", "BL"])
        melhor, mc = None, 1e18
        for k, nome in enumerate(ordem):
            X, Y = cantos[nome]
            r = [X, Y, w, h]
            if g.poly and not g.contem_rect(r, 0):
                # quadro diagonal: desliza para dentro até caber
                for dx in range(0, int(g.w / 2), 20):
                    rr = [X + (dx if nome in ("TL", "BL") else -dx), Y, w, h]
                    if g.contem_rect(rr, 0):
                        r = rr
                        break
                else:
                    continue
            c = k * 120 + _custo_rostos(r, faces, 1.5) + (1e6 if _sobrepoe(r, ocupados) else 0)
            if c < mc:
                melhor, mc = r, c
        if melhor:
            e["pos"] = list(g.pag2frac(melhor[0], melhor[1]))
            ocupados.append(melhor)
        n_leg += 1
    # 2) balões, em ordem de leitura
    falas = [e for e in textos if e["tipo"] in ("fala", "grito", "pensa")]
    ant = None
    usados_rosto = {}
    for i, e in enumerate(falas):
        manual = e.get("_manual", set())
        a, b = medida(e)
        lado = e.get("lado", "c")
        if "pos" in manual:
            cx, cy = g.x + e["pos"][0] * g.w, g.y + e["pos"][1] * g.h
            ocupados.append([cx - a, cy - b, 2 * a, 2 * b])
            ant = (cx, cy)
            continue
        # rosto de quem fala
        alvo_face = None
        if faces:
            grandes = sorted(faces, key=lambda f: -f[2] * f[3])[:3]
            if lado == "e":
                alvo_face = min(grandes, key=lambda f: f[0] + f[2] / 2)
            elif lado == "d":
                alvo_face = max(grandes, key=lambda f: f[0] + f[2] / 2)
            else:
                alvo_face = usados_rosto.get(e.get("quem")) or grandes[0]
            if e.get("quem") in usados_rosto:
                alvo_face = usados_rosto[e["quem"]]
            usados_rosto[e.get("quem")] = alvo_face
        if "alvo" in manual:   # alvo manual (boca de quem fala) guia também a posição do balão
            boca = g.img2pag(*e["alvo"])
            alvo_face = None
        elif alvo_face:
            fx, fy, fw, fh = alvo_face
            boca = (fx + fw / 2, fy + fh * (0.30 if e["tipo"] == "pensa" else 0.80))
        else:
            boca = g.img2pag(*e["alvo"]) if e.get("alvo") else (g.x + g.w / 2, g.y + g.h * 0.7)
        melhor, mc = None, 1e18
        passo = 24
        for cy in range(int(g.y + b + MARGEM), int(g.y + g.h - b - MARGEM) + 1, passo):
            for cx in range(int(g.x + a + MARGEM), int(g.x + g.w - a - MARGEM) + 1, passo):
                if not g.contem_elipse(cx, cy, a, b):
                    continue
                r = [cx - a * 0.92, cy - b * 0.92, 2 * a * 0.92, 2 * b * 0.92]
                if _sobrepoe(r, ocupados):
                    continue
                c = _custo_rostos(r, faces)
                # perto da cabeça de quem fala (de preferência acima/ao lado), rabicho de tamanho razoável
                dist = math.hypot(cx - boca[0], cy - boca[1]) - (a + b) / 2
                c += 0.9 * max(0, dist - 140) + 3 * max(0, 40 - dist)
                if cy > boca[1] and e["tipo"] != "pensa":
                    c += 0.6 * (cy - boca[1])   # balão abaixo da boca lê pior
                # lado preferido
                fxr = (cx - g.x) / g.w
                if lado == "e":
                    c += 300 * max(0, fxr - 0.5)
                elif lado == "d":
                    c += 300 * max(0, 0.5 - fxr)
                # topo do quadro é bom para balão
                c += 0.15 * (cy - g.y)
                # ordem de leitura: depois do anterior (mais abaixo ou mais à direita)
                if ant:
                    if cy < ant[1] - 20 and cx < ant[0] + 40:
                        c += 900
                    elif cy < ant[1] - 20:
                        c += 0.8 * (ant[1] - cy)
                if c < mc:
                    melhor, mc = (cx, cy), c
        if not melhor:
            continue   # não coube: fica o do rascunho (aparece na revisão visual)
        cx, cy = melhor
        e["pos"] = list(g.pag2frac(cx, cy))
        ocupados.append([cx - a, cy - b, 2 * a, 2 * b])
        ant = (cx, cy)
        if "alvo" not in manual:
            # ponta do rabicho: perto da boca, recuada 25% do rosto na direção do balão (não tapa a boca)
            if alvo_face:
                # ponta na borda do rosto (caixa +10%), na linha boca → balão: aponta para a boca sem tapar o rosto
                vx, vy = cx - boca[0], cy - boca[1]
                n = math.hypot(vx, vy) or 1
                ux, uy = vx / n, vy / n
                fx, fy, fw, fh = alvo_face
                x0, x1 = fx - 0.05 * fw, fx + 1.05 * fw
                y0, y1 = fy - 0.05 * fh, fy + 1.05 * fh
                ts = []
                for lim, comp, base in ((x0, ux, boca[0]), (x1, ux, boca[0]), (y0, uy, boca[1]), (y1, uy, boca[1])):
                    if abs(comp) > 1e-6:
                        t = (lim - base) / comp
                        if t > 0:
                            ts.append(t)
                t = (min(ts) if ts else 0.3 * fh) + 6
                tx, ty = boca[0] + ux * t, boca[1] + uy * t
                if ((tx - cx) / a) ** 2 + ((ty - cy) / b) ** 2 < 1.1:   # borda caiu dentro do balão: encurta
                    tx, ty = boca[0] + ux * t * 0.5, boca[1] + uy * t * 0.5
            else:
                tx, ty = boca
                vx, vy = tx - cx, ty - cy
                n = math.hypot(vx, vy) or 1
                lim = max(a, b) + 160
                if n > lim:
                    tx, ty = cx + vx / n * lim, cy + vy / n * lim
            e["alvo"] = list(g.pag2img(tx, ty))
    # 3) onomatopeias: não tapam balão, legenda nem rosto
    for e in textos:
        if e["tipo"] != "sfx" or "pos" in e.get("_manual", set()):
            continue
        px = e.get("px", 90)
        w, h = px * len(e["texto"]) * 0.62 + 20, px * 1.25
        x0, y0 = g.x + e["pos"][0] * g.w, g.y + e["pos"][1] * g.h
        melhor, mc = None, 1e18
        for cy in range(int(g.y + h / 2 + 20), int(g.y + g.h - h / 2 - 20) + 1, 24):
            for cx in range(int(g.x + w / 2 + 20), int(g.x + g.w - w / 2 - 20) + 1, 24):
                r = [cx - w / 2, cy - h / 2, w, h]
                if g.poly and not g.contem_rect(r, 10):
                    continue
                if _sobrepoe(r, ocupados):
                    continue
                c = _custo_rostos(r, faces, 1.5) + 0.5 * math.hypot(cx - x0, cy - y0)
                if c < mc:
                    melhor, mc = (cx, cy), c
        if melhor:
            e["pos"] = list(g.pag2frac(*melhor))
            ocupados.append([melhor[0] - w / 2, melhor[1] - h / 2, w, h])
    return textos
