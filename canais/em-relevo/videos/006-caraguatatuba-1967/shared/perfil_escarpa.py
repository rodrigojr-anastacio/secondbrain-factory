# Perfil da escarpa da Serra do Mar acima de Caraguatatuba e São Sebastião (AWS Terrain Tiles terrarium z12, SRTM/ETOPO).
# Saída: dados/perfis.json. Uso: tools/.venv/bin/python shared/perfil_escarpa.py
import math, io, json, urllib.request, os
from pathlib import Path
from PIL import Image
Z = 12; N = 2 ** Z
CACHE = Path(os.environ.get("TMPDIR", str(Path.home() / "cache/tmp"))) / "relevo006"; CACHE.mkdir(parents=True, exist_ok=True)
def tile(x, y):
    f = CACHE / f"{Z}_{x}_{y}.png"
    if not f.exists():
        f.write_bytes(urllib.request.urlopen(urllib.request.Request(f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{Z}/{x}/{y}.png", headers={"User-Agent": "emrelevo/1.0"}), timeout=60).read())
    return Image.open(f).convert("RGB")
def alt(lat, lon):
    fx = (lon + 180) / 360 * N; fy = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * N
    x, y = int(fx), int(fy); px, py = int((fx - x) * 256), int((fy - y) * 256)
    r, g, b = tile(x, y).getpixel((px, py)); return r * 256 + g + b / 256 - 32768
def perfil(nome, a, b, n=240):
    pts = []
    d = 6371 * math.radians(math.hypot(b[0] - a[0], (b[1] - a[1]) * math.cos(math.radians(a[0]))))
    for i in range(n + 1):
        t = i / n; la = a[0] + (b[0] - a[0]) * t; lo = a[1] + (b[1] - a[1]) * t
        pts.append({"km": round(d * t, 3), "alt": round(alt(la, lo), 1), "lat": round(la, 5), "lon": round(lo, 5)})
    mar = next((p for p in pts if p["alt"] > 2), pts[0])
    top = max(pts, key=lambda p: p["alt"])
    # primeiro ponto >= 700 m e a distância da costa até ele
    p700 = next((p for p in pts if p["alt"] >= 700), None)
    dec = max(math.degrees(math.atan((pts[i+4]["alt"] - pts[i]["alt"]) / ((pts[i+4]["km"] - pts[i]["km"]) * 1000))) for i in range(len(pts) - 4))
    return {"nome": nome, "de": a, "ate": b, "comprimento_km": round(d, 2), "costa_km": mar["km"], "topo_m": top["alt"], "topo_km": top["km"],
            "km_costa_ate_topo": round(top["km"] - mar["km"], 2), "km_costa_ate_700m": round(p700["km"] - mar["km"], 2) if p700 else None,
            "declividade_max_media_400m_graus": round(dec, 1), "pontos": pts}
# do mar para o interior, perpendicular à costa
PERFIS = [
    perfil("Caraguatatuba (centro → serra, via vale do Santo Antônio)", (-23.625, -45.400), (-23.540, -45.470)),
    perfil("Caraguatatuba (Morro do Cruzeiro → crista)", (-23.630, -45.420), (-23.570, -45.490)),
    perfil("São Sebastião (Barra do Sahy → crista)", (-23.772, -45.690), (-23.690, -45.700)),
]
out = Path(__file__).resolve().parent.parent / "dados" / "perfis.json"; out.parent.mkdir(exist_ok=True)
json.dump({"fonte": "AWS Terrain Tiles (Mapzen terrarium; SRTM/ETOPO), z12 (~30 m no equador)", "perfis": PERFIS}, open(out, "w"), ensure_ascii=False)
for p in PERFIS:
    print(p["nome"], "| topo", p["topo_m"], "m a", p["km_costa_ate_topo"], "km da costa | 700 m a", p["km_costa_ate_700m"], "km | decliv. máx", p["declividade_max_media_400m_graus"], "°")
    print("   ", [(q["km"], int(q["alt"])) for q in p["pontos"][::20]])
