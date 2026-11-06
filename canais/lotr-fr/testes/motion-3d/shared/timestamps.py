# Timestamps por palavra com faster-whisper; alinha às palavras do roteiro (texto do roteiro prevalece).
import json, re
from pathlib import Path
from faster_whisper import WhisperModel
aqui = Path(__file__).parent
m = WhisperModel("small", device="cpu", compute_type="int8")
import subprocess, numpy as np
pcm = subprocess.run(["ffmpeg","-v","quiet","-i",str(aqui.parent/"audio"/"narracao.wav"),"-ar","16000","-ac","1","-f","f32le","-"],capture_output=True).stdout
segs, _ = m.transcribe(np.frombuffer(pcm, np.float32), language="fr", word_timestamps=True)
ws = [w for s in segs for w in s.words]
rot = (aqui/"roteiro.txt").read_text().split()
print(len(ws), len(rot))
for w in ws: print(f"{w.start:6.2f} {w.end:6.2f} {w.word}")
json.dump([{"w": w.word.strip(), "s": round(w.start,3), "e": round(w.end,3)} for w in ws], open(aqui/"whisper.json","w"), ensure_ascii=False, indent=0)
