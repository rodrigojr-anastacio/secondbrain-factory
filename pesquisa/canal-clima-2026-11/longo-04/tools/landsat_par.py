# Recorte em falsa-cor (B4,B3,B2 do Landsat 4 MSS) da mesma janela em duas datas: União da Vitória antes × durante a cheia de 1983.
# uso: python tools/landsat_par.py <pasta das bandas> <saida_dir>
import sys, math, re, numpy as np
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
src, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
def utm(lat, lon, zone=22):  # WGS84 -> UTM (northing negativo no sul, convenção USGS)
    a=6378137.0; f=1/298.257223563; e2=f*(2-f); k0=0.9996; lon0=math.radians(-183+6*zone)
    la, lo = math.radians(lat), math.radians(lon); ep2=e2/(1-e2)
    N=a/math.sqrt(1-e2*math.sin(la)**2); T=math.tan(la)**2; C=ep2*math.cos(la)**2; A=math.cos(la)*(lo-lon0)
    M=a*((1-e2/4-3*e2**2/64-5*e2**3/256)*la-(3*e2/8+3*e2**2/32+45*e2**3/1024)*math.sin(2*la)+(15*e2**2/256+45*e2**3/1024)*math.sin(4*la)-(35*e2**3/3072)*math.sin(6*la))
    x=k0*N*(A+(1-T+C)*A**3/6+(5-18*T+T*T+72*C-58*ep2)*A**5/120)+500000
    y=k0*(M+N*math.tan(la)*(A*A/2+(5-T+9*C+4*C*C)*A**4/24+(61-58*T+T*T+600*C-330*ep2)*A**6/720))
    return x, y
CX, CY = utm(-26.235, -51.075)   # centro: União da Vitória / Porto União
W, H = 1200, 675                 # px de 60 m -> 72 × 40,5 km
for mtl in sorted(src.glob("*_MTL.txt")):
    t = mtl.read_text(); sid = mtl.name[:-8]
    ulx = float(re.search(r"CORNER_UL_PROJECTION_X_PRODUCT = ([\d.-]+)", t).group(1)) - 30
    uly = float(re.search(r"CORNER_UL_PROJECTION_Y_PRODUCT = ([\d.-]+)", t).group(1)) + 30
    col = int((CX-ulx)/60) - W//2; row = int((uly-CY)/60) - H//2
    bands = []
    for b in ("B4", "B3", "B2"):
        im = np.array(Image.open(src/f"{sid}_{b}.TIF")).astype(float)
        pad = np.zeros((im.shape[0]+2*H, im.shape[1]+2*W)); pad[H:H+im.shape[0], W:W+im.shape[1]] = im
        c = pad[row+H:row+2*H, col+W:col+2*W]
        v = c[c > 0]; lo, hi = (np.percentile(v, 1), np.percentile(v, 99.3)) if v.size else (0, 1)
        bands.append(np.clip((c-lo)/(hi-lo+1e-6), 0, 1) ** 0.85)
    rgb = (np.dstack(bands)*255).astype(np.uint8)
    data = re.search(r"_(\d{8})_", sid).group(1)
    Image.fromarray(rgb).resize((1920, 1080), Image.LANCZOS).save(out/f"landsat4-uv-{data}-par.jpg", quality=90)
    print(sid, "col,row", col, row, "cobertura", round(float((bands[0]>0).mean()),3))
