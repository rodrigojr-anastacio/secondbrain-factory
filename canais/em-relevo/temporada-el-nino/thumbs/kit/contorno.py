"""Contornos (Natural Earth 50m, domínio público; UFs IBGE) projetados no globo ortográfico de globo.py."""
import json, os, numpy as np
from PIL import Image, ImageDraw, ImageFilter
import globo
NE = os.path.expanduser("~/cache/nasa/ne_50m_admin_0_countries.geojson"); UF = os.path.expanduser("~/cache/nasa/ibge-ufs.geojson")
def _aneis(g):
    ps = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    return [p[0] for p in ps]
def pais(nome="Brazil"):
    for f in json.load(open(NE))["features"]:
        if f["properties"]["NAME"] == nome: return _aneis(f["geometry"])
def ufs(codigos=None):
    out = []
    for f in json.load(open(UF))["features"]:
        if codigos is None or f["properties"]["codarea"] in codigos: out += _aneis(f["geometry"])
    return out
def desenha(im, aneis, cam, cor=(255, 255, 255), larg=6, brilho=True, preencher=None):
    W, H = im.size; cam = dict(cam, W=W, H=H)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for r in aneis:
        pts = [globo.tela(x, y, **cam) for x, y in r]
        if preencher: d.polygon(pts, fill=preencher)
        d.line(pts + [pts[0]], fill=cor + (255,), width=larg, joint="curve")
    if brilho:
        g = lay.filter(ImageFilter.GaussianBlur(larg * 2.2)); im.alpha_composite(g); im.alpha_composite(g)
    im.alpha_composite(lay)
