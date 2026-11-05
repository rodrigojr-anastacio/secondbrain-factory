#!/usr/bin/env python3
"""Recorta margem branca lateral/inferior (pillarbox claro) que sobra depois do recorta_moldura.py e reenquadra em 16:9 (cover).
Uso: <venv>/python tools/recorta_branco.py imagens/ I035 I050 ...  (003-fbi, 05/11/2026)"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image
W, H = 1344, 768
for i in sys.argv[2:]:
    p = Path(sys.argv[1]) / f"{i}.jpg"; im = Image.open(p).convert("RGB"); g = np.asarray(im.convert("L")).astype(float)
    cols = np.where((g < 225).mean(0) > 0.15)[0]; rows = np.where((g < 225).mean(1) > 0.15)[0]
    x0, x1, y0, y1 = cols[0] + 3, cols[-1] - 3, rows[0] + 3, rows[-1] - 3
    w, h = x1 - x0, y1 - y0
    if w / h > W / H: nw = int(h * W / H); x0 += (w - nw) // 2; w = nw
    else: nh = int(w * H / W); y0 += (h - nh) // 2; h = nh
    im.crop((x0, y0, x0 + w, y0 + h)).resize((W, H), Image.LANCZOS).save(p, quality=92)
    print(i, f"{w}x{h} ({100*w/im.width:.0f}%)")
