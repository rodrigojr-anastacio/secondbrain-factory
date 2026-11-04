# Procedural "painterly" city scenes (PIL only, original, no real places).
import random, math, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance
W, H = 1920, 1140
OUT = 'public/img/'

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def sky(top, mid, bot, sun=None, sunc=(255, 230, 170)):
    im = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        c = lerp(top, mid, t / .55) if t < .55 else lerp(mid, bot, (t - .55) / .45)
        d.line([(0, y), (W, y)], fill=c)
    if sun:
        g = Image.new('L', (W, H)); gd = ImageDraw.Draw(g)
        for r in range(520, 0, -8): gd.ellipse([sun[0]-r, sun[1]-r, sun[0]+r, sun[1]+r], fill=int(255*(1-r/520)**2))
        im = Image.composite(Image.new('RGB', (W, H), sunc), im, g)
    # clouds
    cl = Image.new('L', (W, H)); cd = ImageDraw.Draw(cl)
    for _ in range(60):
        x, y = random.randint(-200, W), random.randint(0, int(H*.45)); w = random.randint(150, 600)
        cd.ellipse([x, y, x+w, y+w//4], fill=random.randint(40, 110))
    cl = cl.filter(ImageFilter.GaussianBlur(40))
    return Image.composite(Image.new('RGB', (W, H), lerp(mid, (255, 245, 225), .4)), im, cl)

def ridge(im, base, amp, col, rough=.5, seed=0, blur=2, peaks=None):
    random.seed(seed)
    pts, n = [], 64
    vals = [0]*(n+1); step = n
    vals[0] = random.random(); vals[n] = random.random()
    a = 1.0
    while step > 1:
        for i in range(0, n, step):
            vals[i+step//2] = (vals[i]+vals[i+step])/2 + (random.random()-.5)*a
        step //= 2; a *= rough
    for i, v in enumerate(vals):
        x = i*W/n; y = base - v*amp
        if peaks:
            for px, ph, pw in peaks: y -= ph*max(0, 1-abs(x-px)/pw)
        pts.append((x, y))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.polygon(pts + [(W, H), (0, H)], fill=col + (255,))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))
    return pts

def haze(im, y0, col, strength=150):
    g = Image.new('L', (W, H)); d = ImageDraw.Draw(g)
    for y in range(H): d.line([(0, y), (W, y)], fill=int(strength*max(0, 1-abs(y-y0)/260)))
    im.alpha_composite(Image.composite(Image.new('RGBA', (W, H), col+(255,)), Image.new('RGBA', (W, H), (0,0,0,0)), g))

def layer(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))

def building(d, x, y, w, h, wall, roof=None, tower=False, windows=(40, 30, 20), lit=False):
    d.rectangle([x, y-h, x+w, y], fill=wall)
    d.rectangle([x+w*.75, y-h, x+w, y], fill=lerp(wall, (40, 35, 40), .35))  # shadow side
    if roof == 'dome': d.ellipse([x, y-h-w*.5, x+w, y-h+w*.5], fill=wall)
    elif roof: d.polygon([(x-3, y-h), (x+w/2, y-h-w*(1.4 if tower else .6)), (x+w+3, y-h)], fill=roof)
    if h > 30:
        for wy in range(int(y-h+12), int(y-8), 22):
            for wx in range(int(x+6), int(x+w-6), 16):
                if random.random() < .5: d.rectangle([wx, wy, wx+4, wy+8], fill=(255, 200, 110) if lit and random.random() < .5 else windows)

def white_city(im, cx, base, tiers, w0, wall=(232, 226, 210), seed=1, spur=True, light=(255,240,215)):
    """Tiered white city against a mountain: tiers rings, top tower."""
    random.seed(seed); L = layer(); d = ImageDraw.Draw(L)
    th = 46
    for k in range(tiers):
        w = w0 * (1 - k/(tiers+1.5)); y = base - k*th
        shade = lerp(wall, (150, 145, 150), .25 - k*.03)
        d.rectangle([cx-w/2, y-th, cx+w/2, y], fill=shade)                    # wall ring
        d.rectangle([cx-w/2, y-th, cx+w/2, y-th+6], fill=light)               # lit parapet
        for _ in range(int(w/26)):
            bx = random.uniform(cx-w/2+8, cx+w/2-30); bw = random.randint(12, 26)
            building(d, bx, y-th, bw, random.randint(10, 30), lerp(wall, light, .3), roof=(170, 160, 150) if random.random()<.4 else None)
        d.rectangle([cx-10, y-24, cx+10, y-2], fill=(70, 60, 55))             # gate
    top = base - tiers*th
    d.rectangle([cx-14, top-170, cx+14, top], fill=light)                     # white tower
    d.polygon([(cx-16, top-170), (cx, top-215), (cx+16, top-170)], fill=(220, 215, 205))
    d.rectangle([cx+6, top-170, cx+14, top], fill=lerp(wall, (120, 120, 130), .3))
    if spur:  # stone prow cutting the city in two
        d.polygon([(cx-6, top+8), (cx+18, top+8), (cx+90, base+10), (cx+30, base+10)], fill=(205, 198, 185))
        d.polygon([(cx+18, top+8), (cx+90, base+10), (cx+70, base+10)], fill=(150, 145, 140))
    im.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.2)))

def water(im, y0, col, sky_im=None, ripple=(255, 235, 200)):
    L = layer(); d = ImageDraw.Draw(L)
    for y in range(int(y0), H): d.line([(0, y), (W, y)], fill=lerp(col, lerp(col, (10, 15, 25), .6), (y-y0)/(H-y0)) + (255,))
    random.seed(7)
    for _ in range(900):
        x = random.randint(0, W); y = random.randint(int(y0), H); l = random.randint(10, 80)
        d.line([(x, y), (x+l, y)], fill=ripple + (random.randint(30, 110),), width=2)
    im.alpha_composite(L.filter(ImageFilter.GaussianBlur(1)))

def ship(d, x, y, s, col=(40, 30, 25), sail=(225, 210, 180)):
    d.polygon([(x, y), (x+120*s, y), (x+100*s, y+22*s), (x+15*s, y+22*s)], fill=col)
    d.line([(x+60*s, y), (x+60*s, y-110*s)], fill=col, width=max(2, int(4*s)))
    d.polygon([(x+62*s, y-105*s), (x+110*s, y-40*s), (x+62*s, y-20*s)], fill=sail)
    d.polygon([(x+58*s, y-95*s), (x+20*s, y-35*s), (x+58*s, y-25*s)], fill=lerp(sail, (0,0,0), .15))

def columns_hall(im, n, col, light, seed=0, glow=None, roots=False):
    random.seed(seed); L = layer(); d = ImageDraw.Draw(L)
    vx, vy = W/2, H*.46
    for k in range(n, 0, -1):
        z = k/n; s = 1/(.25 + z*1.6)
        for side in (-1, 1):
            x = vx + side*(260*s + 40); w = 34*s; top = vy - 330*s; bot = vy + 420*s
            c = lerp(col, (10, 8, 12), z*.8)
            d.rectangle([x-w, top, x+w, bot], fill=c)
            d.rectangle([x-w, top, x-w*.5, bot], fill=lerp(c, light, .35 - z*.3))
            if roots:
                for r in range(4): d.line([(x, top+r*60*s), (x+side*random.randint(40, 160)*s, top-random.randint(40, 200)*s)], fill=lerp(c, (40, 60, 30), .4), width=max(2, int(10*s)))
        d.arc([vx-260*s-40, top-200*s, vx+260*s+40, top+220*s], 180, 360, fill=lerp(col, (10, 8, 12), z*.8), width=max(2, int(26*s)))
    if glow:
        g = Image.new('L', (W, H)); gd = ImageDraw.Draw(g)
        for r in range(400, 0, -10): gd.ellipse([vx-r*1.6, vy-r, vx+r*1.6, vy+r], fill=int(200*(1-r/400)**2))
        im.alpha_composite(Image.composite(Image.new('RGBA', (W, H), glow+(255,)), Image.new('RGBA', (W, H), (0,0,0,0)), g))
    im.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.5)))
    d2 = ImageDraw.Draw(im); d2.rectangle([0, vy+300, W, H], fill=None)

def finish(im, name, warm=(255, 225, 170)):
    rgb = im.convert('RGB')
    # brush texture: directional noise + slight posterised smear
    n = Image.effect_noise((W//2, H//2), 40).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1))
    rgb = ImageChops.overlay(rgb, Image.merge('RGB', (n, n, n)))
    rgb = rgb.filter(ImageFilter.ModeFilter(5)).filter(ImageFilter.SMOOTH_MORE)
    canvas = Image.effect_noise((W, H), 18).convert('RGB')
    rgb = Image.blend(rgb, ImageChops.multiply(rgb, ImageEnhance.Brightness(canvas).enhance(2.2)), .18)
    # varnish warmth + vignette
    rgb = Image.blend(rgb, ImageChops.multiply(rgb, Image.new('RGB', (W, H), warm)), .25)
    v = Image.new('L', (W, H), 0); vd = ImageDraw.Draw(v)
    for r in range(0, 60): vd.rectangle([r*14, r*9, W-r*14, H-r*9], fill=int(255*min(1, r/40)))
    v = v.filter(ImageFilter.GaussianBlur(80))
    rgb = Image.composite(rgb, ImageEnhance.Brightness(rgb).enhance(.35), v)
    rgb.save(OUT + name + '.jpg', quality=90)

# ---------------------------------------------------------------- scenes
def minas_tirith(name, sun, seed):
    random.seed(seed)
    im = sky((70, 90, 130), (235, 180, 120), (200, 140, 100), sun=sun).convert('RGBA')
    ridge(im, 560, 260, (120, 110, 130), .55, seed+1, 6, peaks=[(1250, 260, 420)])         # Mindolluin
    ridge(im, 620, 160, (95, 88, 100), .55, seed+2, 3, peaks=[(1000, 200, 300)])
    haze(im, 640, (230, 190, 150), 120)
    white_city(im, 960, 900, 7, 760, seed=seed)
    ridge(im, 940, 30, (70, 75, 55), .6, seed+3, 2)                                       # Pelennor
    haze(im, 980, (220, 180, 140), 60)
    finish(im, name)

def gondolin():
    im = sky((60, 100, 160), (190, 210, 230), (230, 220, 200), sun=(960, 300)).convert('RGBA')
    ridge(im, 520, 250, (150, 160, 185), .6, 11, 5, peaks=[(200, 200, 260), (1700, 230, 300)])
    L = layer(); d = ImageDraw.Draw(L)  # snow caps
    ridge(im, 700, 200, (90, 100, 120), .6, 12, 3, peaks=[(150, 260, 380), (1780, 280, 380)])
    haze(im, 760, (210, 220, 230), 120)
    ridge(im, 860, 40, (90, 120, 70), .5, 13, 3)                                          # green vale
    white_city(im, 960, 830, 4, 640, wall=(240, 240, 235), seed=14, spur=False, light=(255, 255, 250))
    finish(im, 'gen_gondolin', warm=(240, 240, 235))

def osgiliath():
    im = sky((80, 90, 120), (240, 190, 130), (230, 160, 110), sun=(1500, 380)).convert('RGBA')
    ridge(im, 600, 120, (110, 100, 120), .5, 21, 6)
    haze(im, 640, (240, 200, 160), 140)
    water(im, 760, (150, 120, 110))
    random.seed(22); L = layer(); d = ImageDraw.Draw(L)
    for side, x0, x1 in ((0, 0, 640), (1, 1280, W)):
        for _ in range(26):
            bx = random.uniform(x0, x1-40); building(d, bx, 770, random.randint(30, 70), random.randint(40, 200), (200, 190, 175), roof='dome' if random.random() < .3 else (150, 120, 100))
    building(d, 1120, 770, 70, 330, (215, 205, 190), roof='dome')                     # star-dome
    for k in range(5):                                                                  # arched bridge
        x = 560 + k*150; d.rectangle([x, 720, x+150, 745], fill=(185, 175, 160)); d.chord([x+20, 735, x+130, 830], 180, 360, fill=(110, 125, 140))
        d.rectangle([x-8, 735, x+8, 790], fill=(160, 150, 135))
    im.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.2)))
    finish(im, 'gen_osgiliath')

def harbour(name, top, mid, bot, sun, wall, dark=False, seed=30):
    im = sky(top, mid, bot, sun=sun).convert('RGBA')
    ridge(im, 640, 160, lerp(wall, (60, 50, 50), .5), .5, seed, 6, peaks=[(300, 160, 260)])
    haze(im, 680, mid, 120)
    water(im, 720, lerp(mid, (40, 60, 90), .5))
    random.seed(seed+1); L = layer(); d = ImageDraw.Draw(L)
    for _ in range(40):
        bx = random.uniform(0, 820); building(d, bx, 730, random.randint(30, 80), random.randint(40, 170), wall, roof=lerp(wall, (90, 50, 30), .5), lit=dark)
    building(d, 760, 730, 60, 300, lerp(wall, (255, 255, 255), .2), roof=lerp(wall, (60, 40, 30), .5), tower=True, lit=dark)
    d.rectangle([600, 722, 1300, 736], fill=lerp(wall, (60, 50, 40), .4))             # mole
    for i in range(6): ship(d, 900 + i*170 + random.randint(-30, 30), 780 + i*28, .9 + i*.15, sail=(60, 30, 30) if dark else (230, 215, 185))
    im.alpha_composite(L.filter(ImageFilter.GaussianBlur(1)))
    finish(im, name)

def rock_fortress(name, seed, waterfall=True):
    im = sky((50, 70, 90), (170, 160, 140), (120, 110, 100), sun=(1600, 200)).convert('RGBA')
    ridge(im, 450, 200, (110, 95, 85), .6, seed, 4)
    L = layer(); d = ImageDraw.Draw(L)
    d.polygon([(0, 260), (900, 330), (980, H), (0, H)], fill=(120, 100, 85))          # cliff face
    d.polygon([(700, 320), (900, 330), (980, H), (760, H)], fill=(90, 75, 65))
    for k in range(6):                                                                    # carved terraces & doors
        y = 420 + k*95
        d.rectangle([80, y, 760, y+14], fill=(160, 140, 120))
        for x in range(140, 720, 120):
            d.rectangle([x, y-70, x+46, y], fill=(150, 130, 110)); d.chord([x, y-92, x+46, y-48], 180, 360, fill=(150, 130, 110))
            d.rectangle([x+12, y-58, x+34, y], fill=(30, 22, 18))
    d.rectangle([330, 860, 520, 1000], fill=(25, 18, 15)); d.chord([330, 790, 520, 930], 180, 360, fill=(25, 18, 15))   # great doors
    im.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.5)))
    ridge(im, 520, 120, (85, 95, 80), .6, seed+2, 3)
    haze(im, 600, (200, 190, 170), 70)
    water(im, 980, (90, 110, 110), ripple=(220, 230, 230))
    L = layer(); d = ImageDraw.Draw(L)
    d.polygon([(980, 1000), (1920, 940), (1920, H), (980, H)], fill=(60, 70, 55))
    d.rectangle([380, 975, 1100, 1000], fill=(140, 125, 105))                          # bridge over the Narog
    im.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.2)))
    finish(im, name)

def cavern(name, col, light, glow, seed, roots=False):
    im = Image.new('RGBA', (W, H), lerp(col, (0, 0, 0), .7) + (255,))
    columns_hall(im, 8, col, light, seed, glow=glow, roots=roots)
    L = layer(); d = ImageDraw.Draw(L)
    for y in range(int(H*.72), H): d.line([(0, y), (W, y)], fill=lerp(lerp(col, (0, 0, 0), .5), light, .12*(y-H*.72)/(H*.28)) + (255,))
    d.polygon([(W/2-60, H*.72), (W/2+60, H*.72), (W/2+420, H), (W/2-420, H)], fill=lerp(col, light, .25) + (255,))   # causeway
    im.alpha_composite(L.filter(ImageFilter.GaussianBlur(2)))
    finish(im, name, warm=lerp(light, (255, 255, 255), .3))

def menegroth():
    im = sky((30, 50, 40), (90, 120, 80), (40, 60, 35), sun=(960, 500), sunc=(230, 220, 160)).convert('RGBA')
    random.seed(41); L = layer(); d = ImageDraw.Draw(L)
    for _ in range(36):                                                                  # beech trunks of Neldoreth
        x = random.uniform(0, W); w = random.uniform(14, 60); c = lerp((60, 55, 45), (20, 25, 18), random.random())
        d.rectangle([x, 0, x+w, 760], fill=c)
        d.ellipse([x-200, -80, x+w+200, random.randint(150, 330)], fill=lerp((60, 90, 40), (20, 40, 20), random.random()))
    d.polygon([(0, 560), (520, 430), (1400, 430), (W, 560), (W, H), (0, H)], fill=(105, 100, 90))   # hill of the caves
    d.chord([760, 520, 1160, 900], 180, 360, fill=(25, 22, 20)); d.rectangle([760, 710, 1160, 900], fill=(25, 22, 20))
    d.rectangle([800, 720, 1120, 900], fill=(255, 210, 140))                           # lit doors
    d.rectangle([790, 700, 830, 900], fill=(140, 135, 120)); d.rectangle([1090, 700, 1130, 900], fill=(140, 135, 120))
    for k in range(3): d.rectangle([520 + k*20, 1000 + k*30, 1400 - k*20, 1015 + k*30], fill=(160, 150, 130))   # stone bridge
    water(im, 1040, (40, 60, 50))
    im.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.6)))
    finish(im, 'gen_menegroth', warm=(240, 230, 190))

def tirion():
    im = sky((30, 40, 90), (200, 190, 220), (250, 230, 200), sun=(1500, 330), sunc=(255, 245, 210)).convert('RGBA')
    ridge(im, 560, 200, (140, 150, 180), .5, 51, 6)
    haze(im, 650, (240, 235, 240), 120)
    L = layer(); d = ImageDraw.Draw(L)
    d.polygon([(560, 960), (900, 520), (1080, 520), (1400, 960)], fill=(170, 165, 150))   # green hill Túna
    d.polygon([(1080, 520), (1400, 960), (1240, 960)], fill=(110, 115, 100))
    im.alpha_composite(L)
    white_city(im, 990, 720, 4, 300, wall=(245, 245, 240), seed=52, spur=False, light=(255, 255, 255))
    water(im, 960, (140, 150, 180))
    finish(im, 'gen_tirion', warm=(245, 240, 235))

def armenelos():
    im = sky((60, 90, 140), (240, 200, 150), (220, 180, 140), sun=(500, 360)).convert('RGBA')
    ridge(im, 620, 260, (110, 120, 140), .5, 61, 6, peaks=[(1450, 340, 260)])          # Meneltarma
    haze(im, 700, (240, 210, 170), 140)
    ridge(im, 860, 60, (90, 110, 70), .5, 62, 3)
    random.seed(63); L = layer(); d = ImageDraw.Draw(L)
    for _ in range(50):
        bx = random.uniform(400, 1500); building(d, bx, 860, random.randint(30, 70), random.randint(40, 180), (225, 215, 195), roof='dome' if random.random() < .25 else (130, 90, 70))
    building(d, 900, 860, 110, 260, (240, 235, 220), roof='dome')                     # King's House
    building(d, 1060, 860, 40, 420, (245, 240, 230), roof=(200, 180, 150), tower=True)
    for t in (700, 1250): d.ellipse([t, 700, t+60, 760], fill=(70, 120, 60))
    d.ellipse([1030, 760, 1090, 830], fill=(250, 250, 240))                            # white tree
    im.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.2)))
    finish(im, 'gen_armenelos')

def nogrod():
    rock_fortress('gen_nogrod_ext', 71)
    cavern('gen_nogrod', (110, 70, 45), (255, 150, 70), (255, 120, 40), 72)

if __name__ == '__main__':
    minas_tirith('gen_minas_tirith', (1500, 360), 1)
    minas_tirith('gen_minas_tirith2', (400, 300), 5)
    gondolin(); osgiliath(); menegroth(); tirion(); armenelos()
    harbour('gen_umbar', (40, 30, 60), (200, 90, 60), (90, 40, 40), (1500, 430), (190, 160, 120), dark=True, seed=31)
    harbour('gen_pelargir', (80, 120, 170), (240, 210, 170), (200, 180, 150), (1400, 420), (220, 210, 190), seed=33)
    harbour('gen_falas', (70, 110, 150), (220, 220, 210), (170, 190, 200), (1600, 380), (215, 215, 205), seed=35)
    rock_fortress('gen_nargothrond', 81)
    rock_fortress('gen_nargothrond2', 85)
    cavern('gen_khazad_dum', (90, 85, 95), (190, 210, 255), (120, 160, 255), 91)
    cavern('gen_khazad_dum2', (70, 60, 60), (230, 120, 60), (200, 70, 30), 92)
    cavern('gen_nogrod', (110, 70, 45), (255, 150, 70), (255, 120, 40), 72)
    print('ok')
