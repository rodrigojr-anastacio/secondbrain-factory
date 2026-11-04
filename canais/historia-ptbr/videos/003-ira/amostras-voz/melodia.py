"""Repetição melódica: correlação média entre os contornos de F0 (normalizados em tempo) dos trechos entre pausas.
Alto = todas as frases com a mesma "musiquinha" (sensação robótica). Uso: python melodia.py <wav>..."""
import sys, numpy as np, parselmouth
for f in sys.argv[1:]:
    s = parselmouth.Sound(f); p = s.to_pitch(time_step=0.01, pitch_floor=65, pitch_ceiling=350)
    f0, t = p.selected_array["frequency"], p.xs()
    it = s.to_intensity(time_step=0.01); I, ti = it.values[0], it.xs()
    sil = np.interp(t, ti, I) < (np.percentile(I, 95) - 25)
    # trechos = sequências de não-silêncio separadas por ≥ 25 frames (0,25 s) de silêncio
    tr, cur, gap = [], [], 0
    for k in range(len(t)):
        if sil[k]:
            gap += 1
            if gap >= 25 and cur: tr.append(cur); cur = []
        else:
            gap = 0; cur.append(k)
    if cur: tr.append(cur)
    med = np.median(f0[f0 > 0]); cont = []
    for c in tr:
        v = f0[c]; ok = v > 0
        if ok.sum() < 40: continue
        x = np.arange(len(v))[ok]; y = 12 * np.log2(v[ok] / med)
        cont.append(np.interp(np.linspace(x[0], x[-1], 20), x, y))
    C = np.corrcoef(np.array(cont)); n = len(cont)
    rep = (C.sum() - n) / (n * (n - 1))
    queda = np.mean([c[-4:].mean() - c[:4].mean() for c in cont])
    print(f"{f.split('/')[-1][:-4]:22s} trechos {n:2d}  repeticao_melodica {rep:.2f}  queda_media_st {queda:+.2f}")
