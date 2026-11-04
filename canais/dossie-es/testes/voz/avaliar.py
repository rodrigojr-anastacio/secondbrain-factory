"""Avalia as amostras: duração, palavras/min, similaridade Whisper × texto e se alguma tag foi falada."""
import difflib, glob, json, os, re, subprocess
import numpy as np
from faster_whisper import WhisperModel
base = os.path.dirname(os.path.abspath(__file__))
ref = re.sub(r"\[[^\]]+\]", "", open(os.path.join(base, "hook-es.txt")).read()).strip()
norm = lambda s: re.sub(r"[^a-záéíóúñü0-9 ]", "", s.lower()).split()
m = WhisperModel("small", device="cpu", compute_type="int8")
res = {}
for f in sorted(glob.glob(os.path.join(base, "*.mp3"))):
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
    segs, _ = m.transcribe(np.frombuffer(pcm, np.int16).astype(np.float32) / 32768, language="es")
    txt = " ".join(s.text for s in segs).strip()
    sim = difflib.SequenceMatcher(None, norm(ref), norm(txt)).ratio()
    lufs = subprocess.run(["ffmpeg", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", lufs)
    res[os.path.basename(f)] = {"dur_s": round(dur, 1), "ppm": round(len(norm(ref)) / dur * 60), "sim": round(sim, 3),
                                "tag_falada": any(t in txt.lower() for t in ("serious", "dramatic")), "lufs": i[-1] if i else None, "whisper": txt}
json.dump(res, open(os.path.join(base, "avaliacao.json"), "w"), ensure_ascii=False, indent=1)
for k, v in res.items():
    print(k, v["dur_s"], v["ppm"], v["sim"], v["tag_falada"], v["lufs"])
