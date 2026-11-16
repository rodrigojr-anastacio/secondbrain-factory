# Malhas IBGE (PR/SC/RS + municípios; demais UFs) + Natural Earth 50 m (países) -> shared/geo.json em coordenadas da cena
# (x leste, z sul). Longo 02: caixa até 6,5°N (Roraima/Amapá); municípios do vídeo 2; Monitor de Secas (S2, ago/set 2026);
# maquete do Pacífico inteiro ("pac": outra mesa, longe do Brasil, escala própria, lon 95°E→295°E).
import json, math
from pathlib import Path
D = Path(__file__).parent.parent / "dados"
LON0, LAT0, K = -52.0, -27.6, 1.4
CL = math.cos(math.radians(27.6))
def P(lon, lat): return [round((lon - LON0) * CL * K, 4), round(-(lat - LAT0) * K, 4)]
BOX = (-82.0, -33.0, -44.0, 6.5)  # lon0 lon1 lat0 lat1

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

def clip(poly, box=BOX):
    def cl(pts, inside, inter):
        out = []
        for i in range(len(pts)):
            c, p = pts[i], pts[i - 1]
            if inside(c):
                if not inside(p): out.append(inter(p, c))
                out.append(c)
            elif inside(p): out.append(inter(p, c))
        return out
    ix = lambda v: (lambda p, c: [v, p[1] + (c[1] - p[1]) * (v - p[0]) / (c[0] - p[0])])
    iy = lambda v: (lambda p, c: [p[0] + (c[0] - p[0]) * (v - p[1]) / (c[1] - p[1]), v])
    pts = poly
    for ins, it in [(lambda q: q[0] >= box[0], ix(box[0])), (lambda q: q[0] <= box[1], ix(box[1])),
                    (lambda q: q[1] >= box[2], iy(box[2])), (lambda q: q[1] <= box[3], iy(box[3]))]:
        if not pts: break
        pts = cl(pts, ins, it)
    return pts

def rings(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    return [p[0] for p in polys]
def area(r): return 0.5 * sum(r[i - 1][0] * r[i][1] - r[i][0] * r[i - 1][1] for i in range(len(r)))

geo = {"proj": {"lon0": LON0, "lat0": LAT0, "k": K, "cos": CL}, "estados": {}, "mun": [], "destaque": {}, "vizinhos": [], "cidades": {}}
for uf, sig in [(41, "PR"), (42, "SC"), (43, "RS")]:
    rs = [dp([P(*c) for c in r], 0.012) for r in rings(json.load(open(D / f"uf{uf}.json"))["features"][0]["geometry"])]
    geo["estados"][sig] = [r for r in rs if abs(area(r)) > 0.02]
DEST = {"4115200": "MARINGÁ", "4204202": "CHAPECÓ", "4219507": "XANXERÊ", "4215000": "RIO NEGRINHO", "4307203": "ERVAL GRANDE",
        "4317806": "SANTO AUGUSTO", "4313706": "PALMEIRA DAS MISSÕES", "4301925": "BARRA DO RIO AZUL", "4310702": "ITATIBA DO SUL",
        "4206405": "GUARACIABA", "4122156": "RIO BONITO DO IGUAÇU", "4119400": "PIRAÍ DO SUL", "4109401": "GUARAPUAVA", "4120903": "QUEDAS DO IGUAÇU",
        "4204905": "DIONÍSIO CERQUEIRA", "4202404": "BLUMENAU", "4312609": "MUÇUM", "4306809": "ENCANTADO", "4307807": "ESTRELA", "4311403": "LAJEADO",
        "4128203": "UNIÃO DA VITÓRIA"}
for uf in (41, 42, 43):
    for f in json.load(open(D / f"uf{uf}-mun.json"))["features"]:
        for r in rings(f["geometry"]):
            pr = dp([P(*c) for c in r], 0.006)
            geo["mun"].append(pr)
            cod = f["properties"]["codarea"]
            if cod in DEST:
                geo["destaque"].setdefault(DEST[cod], []).append(pr)
                cx = sum(p[0] for p in pr) / len(pr); cz = sum(p[1] for p in pr) / len(pr)
                geo["cidades"][DEST[cod]] = [round(cx, 3), round(cz, 3)]
AMAZ = {"11", "12", "13", "14", "15", "16", "17", "51", "21"}   # Amazônia Legal (para o tom verde do bloco 26)
for f in json.load(open(D / "br-ufs.json"))["features"]:
    cod = f["properties"]["codarea"]
    if cod in ("41", "42", "43"): continue
    for r in rings(f["geometry"]):
        c = clip(r)
        if len(c) > 3: geo["vizinhos"].append({"nome": cod, "br": True, "amaz": cod in AMAZ, "anel": dp([P(*q) for q in c], 0.03)})
for f in json.load(open(D / "ne110.json"))["features"]:
    a3 = f["properties"]["ADM0_A3"]
    if a3 in ("ARG", "PRY", "URY", "BOL", "CHL", "PER", "ECU", "COL", "VEN", "GUY", "SUR", "FRA"):
        for r in rings(f["geometry"]):
            c = clip(r)
            if len(c) > 3:
                pr = dp([P(*q) for q in c], 0.03)
                if abs(area(pr)) > 0.08: geo["vizinhos"].append({"nome": a3, "br": False, "amaz": False, "anel": pr})
for nome, (lon, lat) in {"CURITIBA": (-49.27, -25.43), "FLORIANÓPOLIS": (-48.55, -27.59), "PORTO ALEGRE": (-51.22, -30.03),
                         "SAN JUSTO": (-60.59, -30.79), "MANAUS": (-60.02, -3.12), "ASSUNÇÃO": (-57.58, -25.28), "BUENOS AIRES": (-58.38, -34.6),
                         "BOA VISTA": (-60.67, 2.82), "MACAPÁ": (-51.07, 0.03), "SÃO PAULO": (-46.63, -23.55), "BRASÍLIA": (-47.88, -15.79),
                         "RECIFE": (-34.88, -8.05), "SALVADOR": (-38.5, -12.97), "PAITA": (-81.11, -5.09), "LIMA": (-77.04, -12.05),
                         "BELO HORIZONTE": (-43.94, -19.92), "CUIABÁ": (-56.1, -15.6)}.items():
    geo["cidades"][nome] = P(lon, lat)
# crista dos Andes (lon, lat, altura relativa) — desenho didático, não DEM
geo["andes"] = [P(lo, la) + [h] for lo, la, h in [(-78.6, 0.0, 0.8), (-78.0, -3.5, 0.75), (-77.3, -8.5, 0.95), (-75.5, -12.5, 0.9), (-72.5, -14.8, 1.0),
                (-69.8, -16.6, 1.15), (-68.6, -19.5, 1.1), (-68.0, -22.5, 1.15), (-68.4, -25.5, 1.05), (-69.0, -28.5, 1.2), (-69.9, -31.5, 1.3),
                (-70.0, -33.0, 1.35), (-70.4, -35.5, 1.0), (-70.9, -38.5, 0.8), (-71.4, -42.5, 0.6)]]
# silhuetas 2D (painel Brasil × EUA): equiretangular, lon/lat em graus com cos da latitude média, sem projeção da cena
sil = {}
for f in json.load(open(D / "ne110.json"))["features"]:
    a3 = f["properties"]["ADM0_A3"]
    if a3 in ("BRA", "USA"):
        latm = -14 if a3 == "BRA" else 39; cm = math.cos(math.radians(latm))
        rs = []
        for r in rings(f["geometry"]):
            if a3 == "USA" and not (-125 < r[0][0] < -66 and 24 < r[0][1] < 50): continue  # só os 48 contíguos
            pr = dp([[round(q[0] * cm, 3), round(-q[1], 3)] for q in r], 0.15)
            if abs(area(pr)) > 1.0: rs.append(pr)
        sil[a3] = rs
geo["silhuetas"] = sil
# Monitor de Secas (ANA): só a categoria S2 (seca grave), ago e set/2026
geo["secas"] = {}
for mes in ("08", "09"):
    rs = []
    for f in json.load(open(D / f"monitor-secas-2026-{mes}.json"))["features"]:
        if f["properties"]["categoria"] != "S2": continue
        for r in rings(f["geometry"]):
            pr = dp([P(*q) for q in clip(r)], 0.02)
            if len(pr) > 3 and abs(area(pr)) > 0.05: rs.append(pr)
    geo["secas"][mes] = rs
# maquete do Pacífico: lon 95°E..295°E (lon < 0 vira +360), lat −35..35; outra mesa em x0 = −400
PAC = {"x0": -400.0, "z0": 0.0, "k": 0.36, "lonc": 195.0}
def P2(lon, lat):
    l = lon % 360
    return [round(PAC["x0"] + (l - PAC["lonc"]) * PAC["k"], 3), round(PAC["z0"] - lat * PAC["k"], 3)]
geo["pac"] = PAC; geo["pac_terras"] = []
for f in json.load(open(D / "ne110.json"))["features"]:
    for r in rings(f["geometry"]):
        r2 = [[q[0] % 360, q[1]] for q in r]
        if max(q[0] for q in r2) - min(q[0] for q in r2) > 180: continue   # anel que cruza o meridiano 0 (fora da caixa)
        c = clip(r2, (95.0, 295.0, -35.0, 35.0))
        if len(c) > 3:
            pr = dp([P2(*q) for q in c], 0.05)
            if len(pr) > 3 and abs(area(pr)) > 0.15: geo["pac_terras"].append({"nome": f["properties"]["ADM0_A3"], "anel": pr})
json.dump(geo, open(Path(__file__).parent / "geo.json", "w"), separators=(",", ":"), ensure_ascii=False)
xs = [p[0] for v in geo["vizinhos"] for p in v["anel"]]; zs = [p[1] for v in geo["vizinhos"] for p in v["anel"]]
print("viz x", min(xs), max(xs), "z", min(zs), max(zs), "viz", len(geo["vizinhos"]), "mun", len(geo["mun"]))
print({k: v for k, v in geo["cidades"].items()})
print((Path(__file__).parent / "geo.json").stat().st_size, "bytes; silhuetas", {k: len(v) for k, v in sil.items()})
