#!/usr/bin/env python3
"""QA das imagens geradas: tela preta (luminância média < 15, filtro do fal), moldura (borda clara e lisa em volta) e faixa preta (letterbox).
Uso: <venv>/python tools/checa_imagens.py imagens/  → lista os ids suspeitos (apague e regere)."""
import subprocess, sys
from pathlib import Path
import numpy as np

def ler(p, w=336, h=192):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w).astype(float)

ruins = []
for p in sorted(Path(sys.argv[1]).glob("*.jpg")):
    g = ler(p); h, w = g.shape; m = 3   # faixa de ~1,5% nas bordas (molduras finas)
    faixas = [g[:m], g[-m:], g[:, :m], g[:, -m:]]
    lisas = sum(1 for f in faixas if f.std() < 22 and f.mean() > 135)
    motivo = []
    if g.mean() < 15: motivo.append(f"preta ({g.mean():.0f})")
    if lisas >= 2: motivo.append(f"moldura ({lisas} bordas lisas e claras)")
    # 002 (05/11): sem "paper grain" no estilo, a moldura virou faixa preta (letterbox) em cima e embaixo
    pretas = sum(1 for f in faixas if f.mean() < 14 and f.std() < 6)
    if pretas >= 2 and g.mean() >= 15: motivo.append(f"faixa preta ({pretas} bordas)")
    if motivo: ruins.append(p.stem); print(p.stem, ", ".join(motivo))
print(f"{len(ruins)} suspeitas: {' '.join(ruins)}")
