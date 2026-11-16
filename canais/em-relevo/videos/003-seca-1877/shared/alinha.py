# Tempos por palavra da narração (faster-whisper small, pt) -> shared/whisper.json (a legenda usa o texto do roteiro; ver build_cues.py)
import json, subprocess, numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
A = Path(__file__).parent
pcm = np.frombuffer(subprocess.run(["ffmpeg", "-v", "quiet", "-i", str(A.parent / "audio/narracao.wav"), "-ar", "16000", "-ac", "1", "-f", "f32le", "-"],
                                   capture_output=True).stdout, np.float32)
segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(pcm, language="pt", word_timestamps=True)
ws = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)} for s in segs for w in s.words]
json.dump(ws, open(A / "whisper.json", "w"), ensure_ascii=False)
print(len(ws), "palavras")
