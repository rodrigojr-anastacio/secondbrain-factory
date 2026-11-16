# Compara takes de um bloco (Whisper small, com atempo do bloco) e imprime a semelhança normalizada. Uso: compara_takes.py b03 [b15 ...]
import json, sys, glob, subprocess, difflib, numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
from normaliza_pt import norm
A = Path(__file__).parent; BR = A.parent / "audio/eleven-brutos"
bl = {b["id"]: b for b in json.load(open(A / "blocos.json"))}
wm = WhisperModel("small", device="cpu", compute_type="int8")
at = lambda bid: 1.3 if int(bid[1:]) <= 6 else (1.25 if int(bid[1:]) == 7 else 1.2)
for bid in sys.argv[1:]:
    for f in sorted(glob.glob(str(BR / f"{bid}.take*.mp3"))):
        x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "quiet", "-i", f, "-af", f"atempo={at(bid)}", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
        segs, _ = wm.transcribe(x, language="pt"); txt = " ".join(s.text for s in segs)
        r = difflib.SequenceMatcher(None, norm(bl[bid]["fala"]), norm(txt), autojunk=False).ratio()
        print(Path(f).name, f"{r:.3f}", f"{len(x)/16000:.1f}s", txt.strip(), flush=True)
