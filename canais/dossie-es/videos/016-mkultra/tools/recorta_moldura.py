#!/usr/bin/env python3
"""Recorta a moldura de papel que o nano-banana às vezes desenha (15% do lote de 04/11) e reenquadra em 16:9, 1344x768.
Uso: <venv>/python tools/recorta_moldura.py imagens/ I002 I007 ...   (original vai para imagens-orig/)"""
import shutil, subprocess, sys
from pathlib import Path
import numpy as np
W, H = 1344, 768
pasta = Path(sys.argv[1]); orig = pasta.parent / "imagens-orig"; orig.mkdir(exist_ok=True)
for i in sys.argv[2:]:
    p = pasta / f"{i}.jpg"; o = orig / f"{i}.jpg"
    if not o.exists(): shutil.copy2(p, o)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(o), "-vf", "format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    w0, h0 = map(int, subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(o)],
                                     capture_output=True, text=True).stdout.strip().split(","))
    g = np.frombuffer(raw, np.uint8).reshape(h0, w0).astype(float)
    fundo = np.median(np.concatenate([g[:4].ravel(), g[-4:].ravel()]))
    dif = np.abs(g - fundo) > 40
    linhas = np.where(dif.mean(1) > 0.5)[0]; cols = np.where(dif.mean(0) > 0.5)[0]
    y0, y1, x0, x1 = linhas[0] + 4, linhas[-1] - 4, cols[0] + 4, cols[-1] - 4   # 4 px para dentro: some o traço do quadro
    w, h = x1 - x0, y1 - y0
    if w / h > W / H: nw = int(h * W / H); x0 += (w - nw) // 2; w = nw
    else: nh = int(w * H / W); y0 += (h - nh) // 2; h = nh
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(o), "-vf", f"crop={w}:{h}:{x0}:{y0},scale={W}:{H}:flags=lanczos", "-q:v", "2", str(p)], check=True)
    print(i, f"recorte {w}x{h} de {w0}x{h0} ({100 * w / w0:.0f}% da largura)")
