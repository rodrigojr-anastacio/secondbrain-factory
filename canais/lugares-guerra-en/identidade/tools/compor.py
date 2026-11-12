# Gera avatar-1..3.png, banner-1..2.jpg e previa-recortes.jpg. Tudo em código (PIL), sem IA. Grátis.
import json, math, random, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(D, *a)
YEL=(0xFD,0xD5,0x05); CY=(0x2B,0xCE,0xE2); RUST=(0xC8,0x56,0x1E); NAVY=(0x0E,0x2A,0x3B); PAPER=(0xED,0xE6,0xD6)
ANTON=lambda s: ImageFont.truetype(P("fontes","Anton-Regular.ttf"), s)
MONO=lambda s: ImageFont.truetype(P("fontes","IBMPlexMono-Bold.ttf"), s)
SS=2  # supersampling

def atoll(d, cx, cy, r, w, col, seed=3):
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.28) for _ in range(3)]
    pts_o, pts_i = [], []
    n = 240
    for i in range(n+1):
        a = 2*math.pi*i/n
        k = 1 + .07*math.sin(3*a+ph[0]) + .04*math.sin(5*a+ph[1]) + .02*math.sin(9*a+ph[2])
        pts_o.append((cx+r*k*math.cos(a), cy+r*k*.9*math.sin(a)))
    # anel com abertura (passe) entre 20 e 50 graus
    for i in range(n):
        a = 360*i/n
        if 25 < a < 48: continue
        a0 = 2*math.pi*i/n
        k = 1 + .07*math.sin(3*a0+ph[0]) + .04*math.sin(5*a0+ph[1]) + .02*math.sin(9*a0+ph[2])
        x, y = cx+r*k*math.cos(a0), cy+r*k*.9*math.sin(a0)
        d.ellipse([x-w/2, y-w/2, x+w/2, y+w/2], fill=col)
    # ilhota dentro da lagoa
    d.ellipse([cx-w*.55, cy-w*.2, cx+w*.55, cy+w*.5], fill=col)

def arc_text(img, text, cx, cy, r, mid_deg, font, col, top=True, spacing=0):
    # escreve o texto ao longo do círculo, centrado em mid_deg (graus, 0 = direita, -90 = topo)
    d = ImageDraw.Draw(img)
    widths = [d.textlength(c, font=font) + spacing for c in text]
    total = sum(widths)
    ang_total = total / r
    a = math.radians(mid_deg) - (ang_total/2 if top else -ang_total/2)
    for c, wd in zip(text, widths):
        step = wd / r
        am = a + (step/2 if top else -step/2)
        tile = Image.new("RGBA", (int(font.size*2), int(font.size*2)), (0,0,0,0))
        ImageDraw.Draw(tile).text((tile.width/2, tile.height/2), c, font=font, fill=col, anchor="mm")
        rot = -math.degrees(am) - 90 if top else -math.degrees(am) + 90
        tile = tile.rotate(rot, resample=Image.BICUBIC, expand=True)
        x, y = cx + r*math.cos(am), cy + r*math.sin(am)
        img.alpha_composite(tile, (int(x - tile.width/2), int(y - tile.height/2)))
        a += step if top else -step

def avatar(n):
    S = 800*SS
    img = Image.new("RGBA", (S, S), NAVY+(255,))
    d = ImageDraw.Draw(img)
    c = S/2
    if n == 1:   # carimbo circular: texto no anel, atol no centro
        for rr, w in ((372, 14), (212, 8)):
            d.ellipse([c-rr*SS, c-rr*SS, c+rr*SS, c+rr*SS], outline=YEL, width=w*SS)
        arc_text(img, "CLEARANCE", c, c, 292*SS, -90, ANTON(110*SS), YEL, True, 10*SS)
        arc_text(img, "REQUIRED", c, c, 292*SS, 90, ANTON(110*SS), YEL, False, 10*SS)
        for ang in (180, 0):
            x = c + 292*SS*math.cos(math.radians(ang)); y = c
            d.polygon([(x-18*SS,y),(x,y-18*SS),(x+18*SS,y),(x,y+18*SS)], fill=RUST)
        atoll(d, c, c, 120*SS, 36*SS, CY)
    elif n == 2:  # disco amarelo cheio, texto empilhado em azul-noite, atol em ciano
        d.ellipse([c-380*SS, c-380*SS, c+380*SS, c+380*SS], fill=YEL)
        d.ellipse([c-350*SS, c-350*SS, c+350*SS, c+350*SS], outline=NAVY, width=6*SS)
        atoll(d, c, c-135*SS, 78*SS, 26*SS, NAVY, seed=5)
        d.text((c, c+20*SS), "CLEARANCE", font=ANTON(138*SS), fill=NAVY, anchor="mm")
        d.rectangle([c-250*SS, c+92*SS, c+250*SS, c+100*SS], fill=RUST)
        d.text((c, c+185*SS), "REQUIRED", font=ANTON(138*SS), fill=NAVY, anchor="mm")
    else:         # monograma CR sobre atol gigante
        atoll(d, c, c, 300*SS, 70*SS, CY, seed=9)
        d.ellipse([c-380*SS, c-380*SS, c+380*SS, c+380*SS], outline=YEL, width=10*SS)
        d.text((c, c+6*SS), "CR", font=ANTON(330*SS), fill=YEL, anchor="mm", stroke_width=14*SS, stroke_fill=NAVY)
        d.rectangle([c-150*SS, c+170*SS, c+150*SS, c+180*SS], fill=RUST)
    img = img.convert("RGB").resize((800, 800), Image.LANCZOS)
    img.save(P(f"avatar-{n}.png"))
    return img

# ---------------- banner ----------------
W, H = 2560, 1440
LON0, LON1, LAT1 = 118, 232, 41
K = W/(LON1-LON0); LAT0 = LAT1 - H/K
def proj(lon, lat):
    if lon < 0: lon += 360
    return ((lon-LON0)*K, (LAT1-lat)*K)
PLACES = [("MIDWAY",-177.4,28.2),("BIKINI",165.4,11.6),("ENEWETAK",162.3,11.5),("WAKE",166.6,19.3),("TINIAN",145.6,15.0),
          ("IWO JIMA",141.3,24.8),("GUADALCANAL",160.0,-9.6),("PELELIU",134.25,7.0),("PEARL HARBOR",-157.97,21.35)]
SAFE = (507, 508, 2053, 931)  # 1546x423 centrada

def mapa(land=(24,66,86), bg=(10,32,46), grid=(20,52,70)):
    img = Image.new("RGB", (W*1, H*1), bg)
    d = ImageDraw.Draw(img)
    for lon in range(120, 232, 10):
        x = proj(lon, 0)[0]; d.line([(x,0),(x,H)], fill=grid, width=2)
    for lat in range(-20, 41, 10):
        y = proj(0, lat)[1]; d.line([(0,y),(W,y)], fill=grid, width=2)
    gj = json.load(open(P("fontes","ne_50m_land.geojson")))
    for f in gj["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            ring = poly[0]
            lons = [p[0] for p in ring]
            if max(lons) - min(lons) > 180:  # cruza o antimeridiano: reposiciona só o lado oeste
                pts = [proj(p[0] if p[0] > 0 else p[0]+360, p[1]) for p in ring]
                pts = [(x, y) for x, y in pts]
            else:
                pts = [proj(*p) for p in ring]
            if max(p[0] for p in pts) < -50 or min(p[0] for p in pts) > W+50: continue
            if max(p[1] for p in pts) < -50 or min(p[1] for p in pts) > H+50: continue
            if max(p[0] for p in pts) - min(p[0] for p in pts) > W*1.2: continue
            d.polygon(pts, fill=land, outline=(40, 92, 116))
    return img

def dots(img, labels=True, only_outside_safe=False):
    glow = Image.new("RGBA", (W, H), (0,0,0,0)); gd = ImageDraw.Draw(glow)
    d = ImageDraw.Draw(img)
    for name, lo, la in PLACES:
        x, y = proj(lo, la)
        gd.ellipse([x-34,y-34,x+34,y+34], fill=CY+(110,))
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    img.paste(glow, (0,0), glow)
    d = ImageDraw.Draw(img)
    for name, lo, la in PLACES:
        x, y = proj(lo, la)
        d.ellipse([x-13,y-13,x+13,y+13], fill=CY, outline=NAVY, width=4)
        inside = SAFE[0]-30 < x < SAFE[2]+30 and SAFE[1]-30 < y < SAFE[3]+30
        if labels and not inside:
            d.text((x+24, y-14), name, font=MONO(26), fill=PAPER)

def veil(img, box, alpha=170, rad=30):
    ov = Image.new("RGBA", img.size, (0,0,0,0))
    ImageDraw.Draw(ov).rounded_rectangle(box, radius=rad, fill=NAVY+(alpha,))
    img.paste(ov, (0,0), ov)

def check_safe(box):
    x0,y0,x1,y1 = box
    assert x0 >= SAFE[0] and y0 >= SAFE[1] and x1 <= SAFE[2] and y1 <= SAFE[3], ("texto fora da área segura", box, SAFE)

def banner(n):
    img = mapa()
    img = img.convert("RGB")
    d = ImageDraw.Draw(img)
    if n == 1:   # título à esquerda da área segura, slogan embaixo; pontos sem rótulo no centro (rótulos fora)
        dots(img, labels=True)
        veil(img, (SAFE[0]-10, SAFE[1]-10, SAFE[2]+10, SAFE[3]+10))
        d = ImageDraw.Draw(img)
        t = "CLEARANCE REQUIRED"
        f = ANTON(160); bb = d.textbbox((SAFE[0]+40, SAFE[1]+20), t, font=f)
        check_safe(bb); d.text((SAFE[0]+40, SAFE[1]+20), t, font=f, fill=YEL)
        d.rectangle([SAFE[0]+40, SAFE[1]+250, SAFE[0]+40+330, SAFE[1]+260], fill=RUST)
        s = "WHERE THE RECORD GOES."
        f2 = MONO(54); bb = d.textbbox((SAFE[0]+40, SAFE[1]+285), s, font=f2)
        check_safe(bb); d.text((SAFE[0]+40, SAFE[1]+285), s, font=f2, fill=PAPER)
    else:        # carimbo à esquerda, título e slogan à direita; pontos com rótulos fora da área segura
        dots(img, labels=True)
        veil(img, (SAFE[0]-10, SAFE[1]-10, SAFE[2]+10, SAFE[3]+10))
        av = Image.open(P("avatar-1.png")).convert("RGBA").resize((340, 340), Image.LANCZOS)
        mask = Image.new("L", (340,340), 0); ImageDraw.Draw(mask).ellipse([0,0,339,339], fill=255)
        ax, ay = SAFE[0]+30, SAFE[1]+(423-340)//2
        img.paste(av, (ax, ay), mask)
        d = ImageDraw.Draw(img)
        tx = ax + 340 + 50
        for i, t in enumerate(("CLEARANCE", "REQUIRED")):
            f = ANTON(150); y = SAFE[1]+14+i*140
            bb = d.textbbox((tx, y), t, font=f); check_safe(bb); d.text((tx, y), t, font=f, fill=YEL)
        s = "READ THE FILE. SEE THE GROUND."
        f2 = MONO(40); y = SAFE[1]+330
        bb = d.textbbox((tx, y), s, font=f2); check_safe(bb); d.text((tx, y), s, font=f2, fill=CY)
    img.save(P(f"banner-{n}.jpg"), quality=90, optimize=True)
    return img

def previa(banners):
    PW = 1280
    sc = PW/W
    tiles = []
    for i, b in enumerate(banners, 1):
        t = b.resize((PW, int(H*sc)), Image.LANCZOS).convert("RGB")
        dd = ImageDraw.Draw(t, "RGBA")
        dd.rectangle([0,0,PW,t.height], outline=(255,255,255))
        # TV = tudo; desktop = faixa 2560x423 central; celular = 1546x423 central
        cy0 = (H-423)/2*sc; cy1 = (H+423)/2*sc
        dd.rectangle([0, cy0, PW, cy1], outline=(255,220,0), width=3)
        dd.rectangle([SAFE[0]*sc, SAFE[1]*sc, SAFE[2]*sc, SAFE[3]*sc], outline=(0,255,0), width=3)
        dd.text((10,10), f"banner-{i}: TV = tudo | amarelo = desktop 2560x423 | verde = celular/area segura 1546x423", fill=(255,255,255))
        tiles.append(t)
        # recorte real do celular
        m = b.crop(SAFE).resize((773, 211), Image.LANCZOS)
        tiles.append(m)
    h = sum(t.height for t in tiles) + 20*(len(tiles)+1)
    out = Image.new("RGB", (PW+40, h), (30,30,30)); y = 20
    for t in tiles:
        out.paste(t, (20, y)); y += t.height + 20
    out.save(P("previa-recortes.jpg"), quality=88)
    # prévia dos avatares (circulo 98px)
    av = Image.new("RGB", (3*340+40, 340+130), (30,30,30))
    for i in range(1,4):
        a = Image.open(P(f"avatar-{i}.png")).convert("RGB")
        m = Image.new("L", (800,800), 0); ImageDraw.Draw(m).ellipse([0,0,799,799], fill=255)
        a.putalpha(m) if False else None
        big = a.resize((300,300), Image.LANCZOS); mb = m.resize((300,300))
        av.paste(big, (20+(i-1)*340, 20), mb)
        sm = a.resize((98,98), Image.LANCZOS); ms = m.resize((98,98))
        av.paste(sm, (20+(i-1)*340+100, 340+10), ms)
    av.save(P("previa-avatares.jpg"), quality=90)

if __name__ == "__main__":
    for i in (1,2,3): avatar(i)
    bs = [banner(i) for i in (1,2)]
    previa(bs)
    for f in sorted(os.listdir(D)):
        if f.endswith(("png","jpg")): print(f, os.path.getsize(P(f))//1024, "KB")
