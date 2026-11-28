"""Texto de thumb do Em Relevo (temporada El Niño, 28/11/2026): Anton com contorno grosso + sombra; etiqueta Plex Mono."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = os.path.expanduser("~/workspace/fabrica-youtube/pesquisa/canal-clima-2026-11/identidade/fontes")
ANTON = f"{F}/Anton-Regular.ttf"
def _plex():
    for n in os.listdir(F):
        if "PlexMono" in n and "Bold" in n and n.endswith("ttf"): return f"{F}/{n}"
    return ANTON
def palavra(im, txt, xy, tam=200, cor=(255, 214, 64), contorno=(14, 20, 38), esp=16, ancora="la", sombra=True, rot=0):
    f = ImageFont.truetype(ANTON, tam)
    camada = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(camada)
    if sombra:
        s = Image.new("RGBA", im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(s)
        ds.text((xy[0] + 10, xy[1] + 14), txt, font=f, fill=(0, 0, 0, 170), anchor=ancora, stroke_width=esp, stroke_fill=(0, 0, 0, 170))
        s = s.filter(ImageFilter.GaussianBlur(10)); im.alpha_composite(s)
    d.text(xy, txt, font=f, fill=cor, anchor=ancora, stroke_width=esp, stroke_fill=contorno)
    if rot: camada = camada.rotate(rot, center=xy, resample=Image.BICUBIC)
    im.alpha_composite(camada); return d.textbbox(xy, txt, font=f, anchor=ancora, stroke_width=esp)
def etiqueta(im, txt, xy, tam=54, fundo=(232, 80, 91), cor=(251, 248, 241), pad=(22, 12), ancora="la"):
    f = ImageFont.truetype(_plex(), tam); d = ImageDraw.Draw(im)
    b = d.textbbox(xy, txt, font=f, anchor=ancora); r = (b[0] - pad[0], b[1] - pad[1], b[2] + pad[0], b[3] + pad[1])
    d.rounded_rectangle(r, 10, fill=fundo); d.text(xy, txt, font=f, fill=cor, anchor=ancora); return r
