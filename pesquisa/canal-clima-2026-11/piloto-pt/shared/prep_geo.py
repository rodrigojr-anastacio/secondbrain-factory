# Malhas IBGE (PR/SC/RS, municípios) + Natural Earth 50m (vizinhos) -> geo.json em coordenadas da cena (x leste, z sul).
import json, math
from pathlib import Path
D = Path(__file__).parent.parent / "dados"
LON0, LAT0, K = -52.0, -27.6, 1.4
CL = math.cos(math.radians(27.6))
def P(lon, lat): return [round((lon - LON0) * CL * K, 4), round(-(lat - LAT0) * K, 4)]
BOX = (-66.0, -40.0, -37.5, -17.5)  # lon0 lon1 lat0 lat1

def dp(pts, eps):
    if len(pts) > 3 and pts[0] == pts[-1]:
        m = len(pts) // 2
        return dp(pts[:m + 1], eps)[:-1] + dp(pts[m:], eps)
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1e-9
    i, dm = 0, 0
    for j in range(1, len(pts) - 1):
        d = abs(dy * pts[j][0] - dx * pts[j][1] + b[0] * a[1] - b[1] * a[0]) / L
        if d > dm: i, dm = j, d
    if dm > eps: return dp(pts[:i + 1], eps)[:-1] + dp(pts[i:], eps)
    return [a, b]

def clip(poly):
    def cl(pts, inside, inter):
        out = []
        for i in range(len(pts)):
            c, p = pts[i], pts[i - 1]
            if inside(c):
                if not inside(p): out.append(inter(p, c))
                out.append(c)
            elif inside(p): out.append(inter(p, c))
        return out
    def ix(v):
        return lambda p, c: [v, p[1] + (c[1] - p[1]) * (v - p[0]) / (c[0] - p[0])]
    def iy(v):
        return lambda p, c: [p[0] + (c[0] - p[0]) * (v - p[1]) / (c[1] - p[1]), v]
    pts = poly
    for ins, it in [(lambda q: q[0] >= BOX[0], ix(BOX[0])), (lambda q: q[0] <= BOX[1], ix(BOX[1])),
                    (lambda q: q[1] >= BOX[2], iy(BOX[2])), (lambda q: q[1] <= BOX[3], iy(BOX[3]))]:
        if not pts: break
        pts = cl(pts, ins, it)
    return pts

def rings(geom, outer_only=True):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    return [p[0] for p in polys] if outer_only else [r for p in polys for r in p]

def area(r): return 0.5 * sum(r[i - 1][0] * r[i][1] - r[i][0] * r[i - 1][1] for i in range(len(r)))

geo = {"proj": {"lon0": LON0, "lat0": LAT0, "k": K, "cos": CL}, "estados": {}, "mun": [], "destaque": {}, "vizinhos": [], "cidades": {}}
for uf, sig in [(41, "PR"), (42, "SC"), (43, "RS")]:
    rs = [dp([P(*c) for c in r], 0.012) for r in rings(json.load(open(D / f"uf{uf}.json"))["features"][0]["geometry"])]
    geo["estados"][sig] = [r for r in rs if abs(area(r)) > 0.02]
DEST = {"4115200": "MARINGÁ", "4204202": "CHAPECÓ", "4219507": "XANXERÊ", "4215000": "RIO NEGRINHO", "4307203": "ERVAL GRANDE",
        "4317806": "SANTO AUGUSTO", "4313706": "PALMEIRA DAS MISSÕES"}
for uf in (41, 42, 43):
    for f in json.load(open(D / f"uf{uf}-mun.json"))["features"]:
        for r in rings(f["geometry"]):
            pr = dp([P(*c) for c in r], 0.006)
            geo["mun"].append(pr)
            cod = f["properties"]["codarea"]
            if cod in DEST:
                geo["destaque"].setdefault(DEST[cod], []).append(pr)
                if DEST[cod] not in geo["cidades"] or abs(area(pr)) > 0:
                    cx = sum(p[0] for p in pr) / len(pr); cz = sum(p[1] for p in pr) / len(pr)
                    geo["cidades"][DEST[cod]] = [round(cx, 3), round(cz, 3)]
for f in json.load(open(D / "br-ufs.json"))["features"]:
    if f["properties"]["codarea"] in ("50", "35", "31", "52", "33"):
        for r in rings(f["geometry"]):
            c = clip(r)
            if len(c) > 3: geo["vizinhos"].append({"nome": f["properties"]["codarea"], "br": True, "anel": dp([P(*q) for q in c], 0.02)})
for f in json.load(open(D / "ne110.json"))["features"]:
    a3 = f["properties"]["ADM0_A3"]
    if a3 in ("ARG", "PRY", "URY", "BOL", "CHL"):
        for r in rings(f["geometry"]):
            c = clip(r)
            if len(c) > 3:
                pr = dp([P(*q) for q in c], 0.02)
                if abs(area(pr)) > 0.05: geo["vizinhos"].append({"nome": a3, "br": False, "anel": pr})
for nome, (lon, lat) in {"CURITIBA": (-49.27, -25.43), "FLORIANÓPOLIS": (-48.55, -27.59), "PORTO ALEGRE": (-51.22, -30.03)}.items():
    geo["cidades"][nome] = P(lon, lat)
json.dump(geo, open(Path(__file__).parent / "geo.json", "w"), separators=(",", ":"), ensure_ascii=False)
xs = [p[0] for r in sum(geo["estados"].values(), []) for p in r]; zs = [p[1] for r in sum(geo["estados"].values(), []) for p in r]
print("sul x", min(xs), max(xs), "z", min(zs), max(zs), "mun", len(geo["mun"]), "pts", sum(len(r) for r in geo["mun"]), "viz", len(geo["vizinhos"]))
print(geo["cidades"])
print((Path(__file__).parent / "geo.json").stat().st_size)
