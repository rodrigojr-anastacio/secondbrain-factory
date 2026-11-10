# Visual v2 (Em Relevo 002): baixa as bases de mapa de licença livre para work/v2/.
#  - Imagem: NASA GIBS WMS (Blue Marble Next Generation e Blue Marble Shaded Relief + Bathymetry), domínio público (NASA).
#  - Relevo/batimetria: NOAA NCEI ETOPO 2022 (60 arc-sec, superfície), domínio público, via OPeNDAP (THREDDS).
# Uso: python3 baixa_bases.py   (idempotente: pula o que já existe)
import io, struct, sys, time, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
OUT = Path(__file__).resolve().parents[2] / "work" / "v2"
OUT.mkdir(parents=True, exist_ok=True)

# regiões: (lon0, lon1, lat0, lat1, largura da textura, passo ETOPO em minutos)
REG = {
    "br_largo": (-140.0, 20.0, -75.0, 35.0, 8192, 6),
    "br_det":   (-84.0, -28.0, -40.0, 8.0, 8192, 2),
    "pac":      (95.0, 295.0, -45.0, 45.0, 8192, 6),
}
GIBS = "https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi"
CAMADAS = {"bm": "BlueMarble_NextGeneration", "bmsr": "BlueMarble_ShadedRelief_Bathymetry"}
ETOPO = "https://www.ngdc.noaa.gov/thredds/dodsC/global/ETOPO2022/60s/60s_surface_elev_netcdf/ETOPO_2022_v1_60s_N90W180_surface.nc"


def get(url, tent=4):
    for k in range(tent):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                return r.read()
        except Exception as e:
            print("  falhou", k, e, file=sys.stderr); time.sleep(5 * (k + 1))
    raise RuntimeError(url)


def wms(camada, lon0, lon1, lat0, lat1, w, h):
    # GIBS aceita até ~ 4096 px por pedido; ladrilha em blocos e costura
    img = Image.new("RGB", (w, h))
    BX = 4096
    nx, ny = -(-w // BX), -(-h // BX)
    for j in range(ny):
        for i in range(nx):
            px0, px1 = i * w // nx, (i + 1) * w // nx
            py0, py1 = j * h // ny, (j + 1) * h // ny
            a0 = lon0 + (lon1 - lon0) * px0 / w; a1 = lon0 + (lon1 - lon0) * px1 / w
            b1 = lat1 - (lat1 - lat0) * py0 / h; b0 = lat1 - (lat1 - lat0) * py1 / h
            if a1 > 180 and a0 < 180:   # cruza o antimeridiano: dois pedidos
                pm = round(px0 + (180 - a0) / (a1 - a0) * (px1 - px0))
                img.paste(wms(camada, a0, 180, b0, b1, pm - px0, py1 - py0), (px0, py0))
                img.paste(wms(camada, -180, a1 - 360, b0, b1, px1 - pm, py1 - py0), (pm, py0))
                continue
            if a0 >= 180: a0 -= 360; a1 -= 360
            u = (f"{GIBS}?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS={camada}&SRS=EPSG:4326&STYLES="
                 f"&BBOX={a0:.5f},{b0:.5f},{a1:.5f},{b1:.5f}&WIDTH={px1 - px0}&HEIGHT={py1 - py0}&FORMAT=image/jpeg")
            img.paste(Image.open(io.BytesIO(get(u))).convert("RGB"), (px0, py0))
    return img


def etopo(lon0, lon1, lat0, lat1, passo):
    # índices da grade de 1' (centro de célula): lat = -90 + (i+0.5)/60, lon = -180 + (j+0.5)/60
    i0, i1 = int((lat0 + 90) * 60), int((lat1 + 90) * 60) - 1
    partes = []
    for a, b in ([(lon0, 180.0), (-180.0, lon1 - 360)] if lon1 > 180 else [(lon0, lon1)]):
        j0, j1 = int((a + 180) * 60), min(21599, int((b + 180) * 60) - 1)
        u = f"{ETOPO}.dods?z.z%5B{i0}:{passo}:{i1}%5D%5B{j0}:{passo}:{j1}%5D"
        raw = get(u)
        k = raw.index(b"\nData:\n") + 7
        n = struct.unpack(">I", raw[k:k + 4])[0]
        ni, nj = len(range(i0, i1 + 1, passo)), len(range(j0, j1 + 1, passo))
        assert n == ni * nj, (n, ni, nj)
        z = np.frombuffer(raw[k + 8:k + 8 + 4 * n], dtype=">f4").reshape(ni, nj).astype(np.float32)
        partes.append(z)
    z = np.concatenate(partes, axis=1)
    return z[::-1]   # norte em cima


for nome, (lon0, lon1, lat0, lat1, w, passo) in REG.items():
    h = round(w * (lat1 - lat0) / (lon1 - lon0))
    for ch, camada in CAMADAS.items():
        f = OUT / f"{nome}_{ch}.jpg"
        if f.exists(): continue
        t = time.time(); wms(camada, lon0, lon1, lat0, lat1, w, h).save(f, quality=93)
        print(f"{f.name} {w}x{h} {time.time() - t:.0f}s")
    f = OUT / f"{nome}_etopo.npy"
    if not f.exists():
        t = time.time(); z = etopo(lon0, lon1, lat0, lat1, passo); np.save(f, z)
        print(f"{f.name} {z.shape} min {z.min():.0f} max {z.max():.0f} {time.time() - t:.0f}s")
print("ok")
