"""Gera src/mapa.json: caminho SVG da terra (Natural Earth 50m, domínio público) no recorte do Pacífico Norte
(lon 120E–200E contínuo, lat 12N–48N), projeção equiretangular em 1920x1080, mais pontos (Honolulu, Midway, Tóquio)."""
import json, sys
src, dst = sys.argv[1], sys.argv[2]
L0, L1, A0, A1, W, H = 120, 215, 8, 50, 1920, 1080
sx = W / (L1 - L0); sy = H / (A1 - A0); s = min(sx, sy)
ox = (W - (L1 - L0) * s) / 2; oy = (H - (A1 - A0) * s) / 2
def P(lon, lat):
    if lon < 0: lon += 360
    return round(ox + (lon - L0) * s, 1), round(oy + (A1 - lat) * s, 1)
paths = []
for f in json.load(open(src))["features"]:
    g = f["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    for poly in polys:
        ring = poly[0]
        media = sum(x for x, _ in ring) / len(ring)
        desl = 360 if media < 0 else 0  # o anel inteiro vai para o mesmo lado da costura (Eurásia fica em lon positiva)
        lons = [x + desl for x, _ in ring]; lats = [y for _, y in ring]
        if max(lons) < L0 - 5 or min(lons) > L1 + 5 or max(lats) < A0 - 5 or min(lats) > A1 + 5: continue
        pts = [(round(ox + (x + desl - L0) * s, 1), round(oy + (A1 - y) * s, 1)) for x, y in ring]
        paths.append("M" + "L".join(f"{x},{y}" for x, y in pts) + "Z")
pontos = {"Honolulu": P(-157.86, 21.31), "Midway": P(-177.37, 28.21), "Tokyo": P(139.69, 35.69)}
json.dump({"paths": paths, "pontos": pontos}, open(dst, "w"))
print(len(paths), pontos)
