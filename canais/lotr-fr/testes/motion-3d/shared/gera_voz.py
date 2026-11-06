# Narração Kokoro ff_siwis 0.92 (canal lotr-fr) + timestamps por palavra (faster-whisper small).
import json, sys, numpy as np, soundfile as sf
from pathlib import Path
from kokoro import KPipeline
aqui = Path(__file__).parent
txt = (aqui / "roteiro.txt").read_text().strip()
pipe = KPipeline(lang_code="f", repo_id="hexgrad/Kokoro-82M")
partes = [a for _, _, a in pipe(txt, voice="ff_siwis", speed=0.92)]
pausa = np.zeros(int(24000 * 1.6), dtype=np.float32)
audio = np.concatenate([np.zeros(int(24000*0.25), dtype=np.float32), *partes, pausa])
(aqui.parent / "audio").mkdir(exist_ok=True)
sf.write(aqui.parent / "audio" / "narracao.wav", audio, 24000)
print(f"{len(audio)/24000:.2f}s")
