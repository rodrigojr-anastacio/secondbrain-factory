# Prévias esquemáticas (grátis, PIL, sem IA) das thumbs r2 do Em Relevo.
# Não é a arte final: só prova a leitura a 320x180 (1 foco, texto, contraste) ao lado das thumbs do nicho.
import json, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

R = '/home/hermes/workspace/fabrica-youtube/pesquisa/'
B = R + 'reembalagem-2026-11-14/'
G = R + 'canal-clima-2026-11/longo-02/'
ANTON = R + 'canal-clima-2026-11/identidade/fontes/Anton-Regular.ttf'
NAVY = (20, 28, 48); NAVY2 = (31, 42, 68); CORAL = (232, 80, 91); AMAR = (255, 210, 63)
LAND = (92, 84, 70); LAND_B = (60, 54, 46)
W, H = 1280, 720

ne = json.load(open(G + 'dados/ne110.json'))
ufs = json.load(open(G + 'dados/br-ufs.json'))

def polys(geom):
    if geom['type'] == 'Polygon':
        return [geom['coordinates'][0]]
    return [p[0] for p in geom['coordinates']]

def country(name):
    for f in ne['features']:
        if f['properties']['ADMIN'] == name:
            return polys(f['geometry'])
    raise KeyError(name)

def uf(code):
    for f in ufs['features']:
        if str(f['properties']['codarea']) == str(code):
            return polys(f['geometry'])
    raise KeyError(code)

def texto(dr, xy, partes, size, anchor='la', stroke=10):
    f = ImageFont.truetype(ANTON, size)
    x, y = xy
    for t, cor in partes:
        dr.text((x, y), t, font=f, fill=cor, stroke_width=stroke, stroke_fill=(0, 0, 0))
        x += dr.textlength(t, font=f)

def glow_line(img, pts, cor, larg):
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line(pts, fill=cor + (150,), width=int(larg * 2.4), joint='curve')
    lay = lay.filter(ImageFilter.GaussianBlur(larg * 0.8))
    d = ImageDraw.Draw(lay)
    d.line(pts, fill=cor + (255,), width=larg, joint='curve')
    d.line(pts, fill=(235, 255, 255, 255), width=max(2, larg // 3), joint='curve')
    img.alpha_composite(lay)

# ---------------- SUL: Cone Sul oblíquo de sudeste, parede dos Andes + rio invisível ----------------
def sul():
    lon0, lon1, lat0, lat1 = -75.0, -31.0, -37.0, -14.5
    def P(lon, lat):
        # mapa -> normalizado; perspectiva leve (câmera baixa vinda do sul/sudeste: longe = mais estreito)
        u = (lon - lon0) / (lon1 - lon0); v = (lat1 - lat) / (lat1 - lat0)
        s = 0.80 + 0.28 * v
        x = W * (0.42 + (u - 0.42) * s)
        y = H * (0.02 + 0.98 * math.copysign(abs(v) ** 1.12, v))
        return (x, y)
    img = Image.new('RGBA', (W, H), NAVY + (255,)); dr = ImageDraw.Draw(img)
    # gradiente leve no oceano
    for i in range(H):
        c = tuple(int(NAVY[k] + (NAVY2[k] - NAVY[k]) * i / H) for k in range(3))
        dr.line([(0, i), (W, i)], fill=c)
    for n in ['Brazil', 'Argentina', 'Paraguay', 'Uruguay', 'Bolivia', 'Chile', 'Peru']:
        for p in country(n):
            dr.polygon([P(*q) for q in p], fill=LAND, outline=LAND_B)
    # Sul em bloco coral (laje simples, sem camadas)
    for code in (41, 42, 43):
        for p in uf(code):
            pts = [P(*q) for q in p]
            dr.polygon([(x, y + 16) for x, y in pts], fill=(120, 30, 40))
    for code in (41, 42, 43):
        for p in uf(code):
            dr.polygon([P(*q) for q in p], fill=CORAL, outline=(150, 40, 50))
    # parede dos Andes (crista erguida)
    ridge = [(-71.5, -12.5), (-69.5, -16.5), (-68.0, -20), (-67.6, -23.5), (-68.4, -27.5), (-69.6, -31), (-70.0, -34), (-70.6, -38)]
    base = [P(lo, la) for lo, la in ridge]
    for i in range(len(base) - 1):
        (x0, y0), (x1, y1) = base[i], base[i + 1]
        h0 = 250 * (0.5 + 0.6 * (y0 / H)); h1 = 250 * (0.5 + 0.6 * (y1 / H))
        dr.polygon([(x0 - 70, y0), (x1 - 70, y1), (x1, y1 - h1), (x0, y0 - h0)], fill=(52, 40, 32))
        dr.polygon([(x0, y0 - h0), (x1, y1 - h1), (x1 + 80, y1), (x0 + 80, y0)], fill=(168, 128, 88))
        dr.polygon([(x0 - 22, y0 - h0 + 40), (x0, y0 - h0), (x1, y1 - h1), (x1 + 26, y1 - h1 + 44)], fill=(240, 240, 236))
    # rio invisível: entra grosso pela borda de cima, desce colado à parede e vira para o Sul
    rio = [(-65.0, -10.0), (-64.6, -16), (-64.0, -20.5), (-62.6, -24.2), (-59.8, -26.4), (-56.5, -27.4), (-53.8, -27.6)]
    pts = [P(*q) for q in rio]
    pts[0] = (pts[0][0], -40)
    glow_line(img, pts, (60, 220, 255), 50)
    # ponta de seta no fim do rio
    dr = ImageDraw.Draw(img)
    (xa, ya), (xb, yb) = pts[-2], pts[-1]
    ang = math.atan2(yb - ya, xb - xa); L = 70
    dr.polygon([(xb + L * math.cos(ang), yb + L * math.sin(ang)),
                (xb + 45 * math.cos(ang + 2.2), yb + 45 * math.sin(ang + 2.2)),
                (xb + 45 * math.cos(ang - 2.2), yb + 45 * math.sin(ang - 2.2))], fill=(200, 250, 255))
    texto(dr, (800, 26), [('CULPA DOS', (255, 255, 255))], 122)
    texto(dr, (850, 165), [('ANDES?', AMAR)], 150)
    return img.convert('RGB')

# ---------------- EL NIÑO: Pacífico navy liso, só a língua quente, termômetro cravado + seta ----------------
def elnino():
    sst = json.load(open(G + 'shared/sst_pacifico.json'))
    grid = sst['grades'][-1]; lon0g, lat0g = sst['lon0'], sst['lat0']
    L0, L1, A0, A1 = -172.0, -33.0, -36.0, 18.0
    def P(lon, lat):
        u = (lon - L0) / (L1 - L0); v = (A1 - lat) / (A1 - A0)
        s = 0.78 + 0.3 * v   # câmera alta, oblíqua leve de noroeste
        x = W * (0.5 + (u - 0.5) * s * 1.02) + 30
        y = H * (0.05 + 0.95 * math.copysign(abs(v) ** 1.05, v))
        return (x, y)
    img = Image.new('RGBA', (W, H), NAVY + (255,)); dr = ImageDraw.Draw(img)
    # língua quente: só células >= 1,5 °C (o resto do oceano fica navy liso)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    for j, row in enumerate(grid):
        lat = lat0g + j
        for i, val in enumerate(row):
            if val is None or val < 2.0 or abs(lat) > 12: continue
            lon = lon0g + i; lon = lon - 360 if lon > 180 else lon
            if lon < L0: continue
            c = (232, 70, 40) if val >= 3.0 else (245, 125, 40)
            if val >= 3.5: c = (210, 30, 40)
            (x0, y0), (x1, y1) = P(lon - .5, lat + .5), P(lon + .5, lat - .5)
            dl.rectangle([x0, y0, x1 + 1, y1 + 1], fill=c + (255,))
    lay = lay.filter(ImageFilter.GaussianBlur(3))
    img.alpha_composite(lay); dr = ImageDraw.Draw(img)
    for n in ['Argentina', 'Paraguay', 'Uruguay', 'Bolivia', 'Chile', 'Peru', 'Colombia', 'Venezuela', 'Ecuador', 'Guyana', 'Suriname', 'Panama', 'Costa Rica', 'Nicaragua']:
        for p in country(n):
            dr.polygon([P(*q) for q in p], fill=LAND, outline=LAND_B)
    for p in country('Brazil'):
        dr.polygon([P(*q) for q in p], fill=CORAL, outline=(150, 40, 50))
    # termômetro cravado na língua (Niño 3.4, ~ -145, 0)
    bx, by = P(-140, -1)
    tw, th = 46, 250
    dr.rounded_rectangle([bx - tw / 2, by - th, bx + tw / 2, by], radius=tw / 2, fill=(250, 250, 250), outline=(0, 0, 0), width=6)
    dr.ellipse([bx - 44, by - 30, bx + 44, by + 58], fill=(210, 30, 40), outline=(0, 0, 0), width=6)
    dr.rounded_rectangle([bx - 11, by - th + 40, bx + 11, by], radius=10, fill=(210, 30, 40))
    for k in range(5):
        yy = by - 70 - k * 45; dr.line([(bx + 6, yy), (bx + 23, yy)], fill=(0, 0, 0), width=4)
    # seta amarela da língua até o Brasil
    sx, sy = P(-118, -3); ex, ey = P(-68, -8)
    dr.line([(sx, sy), ((sx + ex) / 2, sy - 70), (ex - 40, ey - 10)], fill=AMAR, width=26, joint='curve')
    ang = math.atan2((ey - 10) - (sy - 70), (ex - 40) - (sx + ex) / 2)
    tx, ty = ex - 40, ey - 10
    dr.polygon([(tx + 60 * math.cos(ang), ty + 60 * math.sin(ang)),
                (tx + 42 * math.cos(ang + 2.1), ty + 42 * math.sin(ang + 2.1)),
                (tx + 42 * math.cos(ang - 2.1), ty + 42 * math.sin(ang - 2.1))], fill=AMAR)
    texto(dr, (40, 400), [('SÓ ', (255, 255, 255)), ('2 °C?', AMAR)], 230, stroke=12)
    return img.convert('RGB')

def label_font(s=15):
    return ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationMono-BoldItalic.ttf', s)

def thumb(i):
    t = Image.open(B + f'dados/em-relevo/thumbs/{i}.jpg').convert('RGB'); w, h = t.size
    return t.crop((0, int(h * .125), w, int(h * .875)))

def painel(prev, refs, out, titulo):
    cols = [('NOSSA ATUAL', thumb(refs[0][0]))] + [('PRÉVIA R2', prev)] + [(l, thumb(i)) for i, l in refs[1:]]
    tw, th = 320, 180
    img = Image.new('RGB', (len(cols) * (tw + 8) + 8, th + 36 + 360 + 40), (12, 12, 12)); dr = ImageDraw.Draw(img)
    dr.text((8, 4), titulo, fill='white', font=label_font(16))
    for k, (l, t) in enumerate(cols):
        x = 8 + k * (tw + 8)
        img.paste(t.resize((tw, th), Image.LANCZOS), (x, 26))
        dr.text((x, 26 + th + 3), l, fill='yellow' if 'R2' in l else 'white', font=label_font(14))
    img.paste(prev.resize((640, 360), Image.LANCZOS), (8, th + 70))
    dr.text((660, th + 74), 'Prévia a 640×360 (esquema PIL, sem IA;\nnão é a arte final: a final é relevo 3D\nno estilo do canal). Linha de cima = 320×180,\no tamanho real no celular.', fill=(200, 200, 200), font=label_font(15))
    img.save(out, quality=85); print(out, img.size)

if __name__ == '__main__':
    s = sul(); s.save(B + 'dados/em-relevo/r2/previa-sul-1280.jpg', quality=90)
    painel(s, [('bG6-E4qjXYc', ''), ('x_xE2HyxQE0', 'Além do Mapa 64 mil'), ('CMHf4Cqpcrs', 'Mundo Entrópico 448 mil')],
           B + 'mosaicos/em-relevo-sul-previa.jpg', 'Em Relevo · Sul · thumb r2 "CULPA DOS ANDES?" ao lado das 2 que o crivo mandou comparar')
    e = elnino(); e.save(B + 'dados/em-relevo/r2/previa-el-nino-1280.jpg', quality=90)
    painel(e, [('FeSLzHvlkbo', ''), ('IGgMxhMxHao', 'Olá, Ciência! 1,5 mi'), ('BAf4EYZ1AGk', 'Jubilut 5,9 mi')],
           B + 'mosaicos/em-relevo-el-nino-previa.jpg', 'Em Relevo · El Niño · thumb r2 "SÓ 2 °C?" ao lado dos 2 Pacíficos vermelhos mais vistos do tema')
