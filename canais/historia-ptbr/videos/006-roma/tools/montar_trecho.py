#!/usr/bin/env python3
"""Junta blocos da narração (audio/N###.mp3) com os gaps do build.py, para medir um trecho com o medir.py.
Uso (na pasta do vídeo): tools/.venv/bin/python v2-voz/montar_trecho.py <saida.mp3> N001 N009"""
import json, os, sys, subprocess
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "tools"))
from tts_fish import ler, aparar, SR  # noqa: E402
saida, a, z = sys.argv[1], sys.argv[2], sys.argv[3]
bl = json.load(open("blocos.json"))
G, GI, GC = (float(x) for x in os.environ.get("GAPS", "0.35,0.9,1.5").split(","))   # 006: GAPS=0.25,0.6,1.2 testa a regra 10
caps = {p["bloco"] for p in json.load(open("storyboard.json"))["planos"] if "capítulo:" in p["nota"]}
sel = [b for b in bl if a <= b["id"] <= z]
partes, cham = [np.zeros(int(0.25 * SR), dtype=np.float32)], []
for i, b in enumerate(sel):
    g = 0 if i == 0 else GC if b["id"] in caps else GI if b.get("ideia") else G
    partes += [np.zeros(int(g * SR), dtype=np.float32), aparar(ler(f"audio/{b['id']}.mp3"), cauda=0.15)]
    cham.append({"texto": b["texto"], "gap_antes_s": g})
y = np.concatenate(partes + [np.zeros(int(0.5 * SR), dtype=np.float32)])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "pipe:0", "-b:a", "192k", saida],
               input=y.astype(np.float32).tobytes(), check=True)
json.dump({"chamadas": cham}, open(Path(saida).with_suffix(".json"), "w"), ensure_ascii=False, indent=1)
print(saida, round(len(y) / SR, 1), "s")
