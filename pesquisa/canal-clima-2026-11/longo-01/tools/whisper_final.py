# Whisper (small) no áudio do out/video.mp4 -> qa/transcricao.json + comparação com o roteiro por bloco (qa/voz_diff.txt)
import json, re, subprocess, unicodedata, difflib, numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
R = Path(__file__).parent.parent
pcm = np.frombuffer(subprocess.run(["ffmpeg", "-v", "quiet", "-i", str(R / "out/video.mp4"), "-ar", "16000", "-ac", "1", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(pcm, language="pt", word_timestamps=True)
ws = [{"w": w.word.strip(), "s": round(w.start, 3), "p": round(w.probability, 3)} for s in segs for w in s.words]
json.dump(ws, open(R / "qa/transcricao.json", "w"), ensure_ascii=False)
def n(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", " ", s).split()
bl = json.load(open(R / "shared/blocos.json")); tp = {b["id"]: b for b in json.load(open(R / "shared/tempos.json"))["blocos"]}
# compara com o texto da TELA (números em algarismos, como o Whisper escreve) e com a fala; fica o maior
out, tot = [], []
for b in bl:
    t = tp[b["id"]]; c = n(" ".join(w["w"] for w in ws if t["s"] - 0.4 <= w["s"] <= t["e"] + 0.1))
    r = max(difflib.SequenceMatcher(None, n(b["fala"]), c).ratio(), difflib.SequenceMatcher(None, n(b["tela"].replace("|", " ")), c).ratio())
    tot.append((r, len(n(b["fala"]))))
    out.append(f"{b['id']} {r:.2f} | {' '.join(c)}")
media = sum(r * k for r, k in tot) / sum(k for _, k in tot)
open(R / "qa/voz_diff.txt", "w").write(f"semelhança ponderada {media:.3f}\n" + "\n".join(out))
print(f"semelhança ponderada Whisper × roteiro: {media:.3f}; piores:", sorted((round(r, 2), b["id"]) for (r, _), b in zip(tot, bl))[:6])
