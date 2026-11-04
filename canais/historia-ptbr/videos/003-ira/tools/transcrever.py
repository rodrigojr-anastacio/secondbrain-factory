"""QA da voz: transcreve public/audio/voz.wav e salva qa/transcricao.json (segmentos com tempo)."""
import json, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[1] if len(sys.argv) > 1 else "small", device="cpu", compute_type="int8", cpu_threads=2)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "public/audio/voz.wav", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
segs, _ = m.transcribe(np.frombuffer(raw, dtype=np.float32), language="pt", beam_size=1, vad_filter=False)
out = [{"ini": round(s.start, 2), "fim": round(s.end, 2), "texto": s.text.strip()} for s in segs]
json.dump(out, open("qa/transcricao.json", "w"), ensure_ascii=False, indent=0)
print(len(out), "segmentos")
