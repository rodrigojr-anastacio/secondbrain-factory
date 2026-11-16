# ERSSTv5 (NOAA PSL) -> Nino3.4 mensal + grades de anomalia (1991-2020) no formato do longo-02/sst_*.json
import h5py, numpy as np, json, csv, datetime
from pathlib import Path
R = Path(__file__).parent.parent
f = h5py.File(R/"dl/dados/sst.mnmean.nc")
lat = f["lat"][:]; lon = f["lon"][:]; t = f["time"][:]   # t = dias desde 1800-01-01
if lat[0] > lat[-1]:
    lat = lat[::-1]; flip = True
else: flip = False
sst = f["sst"][:].astype("float64")
if flip: sst = sst[:, ::-1, :]
fv = f["sst"].attrs.get("missing_value", -9.96921e36)
sst[(sst > 1e30) | (sst < -100) | (sst == fv)] = np.nan
base = datetime.date(1800, 1, 1)
dts = [base + datetime.timedelta(days=int(x)) for x in t]
yr = np.array([d.year for d in dts]); mo = np.array([d.month for d in dts])
print(dts[0], dts[-1], sst.shape)
clim = np.stack([np.nanmean(sst[(mo == m) & (yr >= 1991) & (yr <= 2020)], axis=0) for m in range(1, 13)])
anom = sst - clim[mo - 1]
# Nino3.4: 5S-5N, 170W-120W (190-240E)
la = (lat >= -5) & (lat <= 5); lo = (lon >= 190) & (lon <= 240)
w = np.cos(np.deg2rad(lat[la]))[:, None] * np.ones(lo.sum())[None, :]
sub = anom[:, la][:, :, lo]
nino = np.array([np.nansum(s * w) / np.sum(w * ~np.isnan(s)) for s in sub])
with open(R/"dados/nino34-1870-2026.csv", "w", newline="") as o:
    c = csv.writer(o); c.writerow(["ano_mes", "anomalia_c"])
    for d, v in zip(dts, nino):
        if d.year >= 1854: c.writerow([f"{d.year}-{d.month:02d}", f"{v:.2f}"])
# resumo: media NDJ (nov-jan) por evento e maximo mensal
def idx(y, m): return [i for i, d in enumerate(dts) if d.year == y and d.month == m][0]
def ndj(y): return float(np.mean([nino[idx(y, 11)], nino[idx(y, 12)], nino[idx(y + 1, 1)]])) if y < 2026 else float(np.mean([nino[idx(2026, 9)], nino[idx(2026, 10)]]))
res = []
for y in sorted(set(yr)):
    if y < 2026 and y < dts[-1].year: pass
rows = []
for y in range(1854, 2026):
    try: rows.append((y, ndj(y)))
    except IndexError: pass
rows.sort(key=lambda r: -r[1])
print("TOP NDJ:", [(y, round(v, 2)) for y, v in rows[:12]])
mx = []
for y in range(1854, 2027):
    ii = [i for i, d in enumerate(dts) if d.year == y]
    j = max(ii, key=lambda i: nino[i]); mx.append((y, dts[j].month, nino[j]))
mx.sort(key=lambda r: -r[2]); print("TOP mensal:", [(y, m, round(v, 2)) for y, m, v in mx[:12]])
print("ultimos", [(f"{d.year}-{d.month}", round(v, 2)) for d, v in list(zip(dts, nino))[-8:]])
for y in (1877, 1878): print(y, [round(nino[idx(y, m)], 2) for m in range(1, 13)])
json.dump({"ndj": [[y, round(v, 2)] for y, v in rows], "max_mensal": [[y, m, round(float(v), 2)] for y, m, v in mx]}, open(R/"dl/dados/nino_resumo.json", "w"))
# --- grades
def interp(g, lon0, lat0, nx, ny):
    # g: (lat,lon) ERSST 2 graus (lon 0..358); bilinear para 1 grau; lon em 0..360
    out = [[None] * nx for _ in range(ny)]
    for j in range(ny):
        la_ = lat0 + j
        fj = (la_ - lat[0]) / 2.0; j0 = int(np.floor(fj)); wj = fj - j0
        if j0 < 0 or j0 + 1 >= len(lat): continue
        for i in range(nx):
            lo_ = (lon0 + i) % 360
            fi = lo_ / 2.0; i0 = int(np.floor(fi)) % 180; i1 = (i0 + 1) % 180; wi = fi - np.floor(fi)
            v = np.array([[g[j0, i0], g[j0, i1]], [g[j0 + 1, i0], g[j0 + 1, i1]]])
            ww = np.array([[(1 - wj) * (1 - wi), (1 - wj) * wi], [wj * (1 - wi), wj * wi]])
            ok = ~np.isnan(v)
            if ww[ok].sum() < 0.5: continue
            out[j][i] = round(float((v[ok] * ww[ok]).sum() / ww[ok].sum()), 2)
    return out
def grade(ym_list, nome, fonte_extra):
    gs = []
    for y, m in ym_list: gs.append(anom[idx(y, m)])
    pac = {"fonte": "NOAA ERSSTv5 (NCEI) anomalia mensal vs. climatologia 1991-2020, via NOAA PSL THREDDS; grade nativa 2 graus interpolada bilinearmente para 1 grau (null onde sem dado/gelo). " + fonte_extra,
           "camada": "psl.noaa.gov Datasets/noaa.ersst.v5/sst.mnmean.nc :: sst (anomalia calculada)", "lon0": 100, "lat0": -30, "passo": 1, "nx": 191, "ny": 61,
           "obs": "cada data = media do mes (rotulo AAAA-MM-15); mesmo formato de longo-02/shared/sst_pacifico.json; resolucao real 2 graus",
           "datas": [f"{y}-{m:02d}-15" for y, m in ym_list], "grades": [interp(g, 100, -30, 191, 61) for g in gs]}
    glo = dict(pac, lon0=-179, lat0=-89, nx=360, ny=179, grades=[interp(g, -179, -89, 360, 179) for g in gs],
               obs="mesmo formato de longo-02/shared/sst_global.json (lon -179..180, lat -89..89, linhas de lat -89 para +89); resolucao real 2 graus", camada=pac["camada"])
    return pac, glo
def dump(o, p): json.dump(o, open(R/p, "w"), separators=(",", ":"))
EXT = "Antes de 1900 os dados sao esparsos (reconstrucao estatistica): padrao de grande escala, nao detalhe local."
pac, glo = grade([(1877, 11), (1877, 12), (1878, 1), (1878, 2)], "1877", EXT)
dump(pac, "dados/sst_1877.json"); dump(glo, "dl/dados/sst_1877_global.json")
comp = [(1877, 12), (1982, 12), (1997, 12), (2015, 12), (2023, 12), (2026, 10)]
pac2, glo2 = grade(comp, "comp", "Comparativo: dez/1877, dez/1982, dez/1997, dez/2015, dez/2023 e out/2026 (ultimo mes disponivel).")
dump(pac2, "dados/sst_comparativo.json"); dump(glo2, "dados/sst_comparativo_global.json")
import os
for p in ["dados/sst_1877.json","dl/dados/sst_1877_global.json","dados/sst_comparativo.json","dados/sst_comparativo_global.json"]: print(p, os.path.getsize(R/p)//1024, "KB")
# pico Pacifico: anomalia maxima na caixa niño em cada
for (y, m) in comp: print(y, m, "nino34", round(nino[idx(y, m)], 2))
