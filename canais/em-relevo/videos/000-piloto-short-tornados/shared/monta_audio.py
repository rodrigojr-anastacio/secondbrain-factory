# Apara silêncio de cada bloco, aplica atempo opcional e junta com pausas controladas -> audio/narracao.wav + tempos.json
import json, sys, subprocess, numpy as np, soundfile as sf
from pathlib import Path
aqui = Path(__file__).parent; raiz = aqui.parent
TEMPO = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
PAUSA = {"b01": 0.30, "b02": 0.30, "b03": 0.35, "b04": 0.55, "b05": 0.45, "b06": 0.55, "b07": 0.25, "b08": 0.35, "b09": 0.45, "b10": 0.0}
INICIO, FIM = 0.15, 0.9
SR = 24000
partes, tempos, t = [np.zeros(int(SR * INICIO), np.float32)], [], INICIO
for b in json.load(open(aqui / "blocos.json")):
    a, sr = sf.read(raiz / "work/voz" / f"{b['id']}.wav", dtype="float32")
    if TEMPO != 1.0:
        a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "quiet", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={TEMPO}",
                                          "-f", "f32le", "-"], input=a.tobytes(), capture_output=True).stdout, np.float32)
    env = np.abs(a) > 0.01
    i0, i1 = np.argmax(env), len(a) - np.argmax(env[::-1])
    a = a[max(0, i0 - int(0.03 * SR)): min(len(a), i1 + int(0.06 * SR))]
    tempos.append({"id": b["id"], "s": round(t, 3), "e": round(t + len(a) / SR, 3)})
    partes += [a, np.zeros(int(SR * PAUSA[b["id"]]), np.float32)]
    t += len(a) / SR + PAUSA[b["id"]]
partes.append(np.zeros(int(SR * FIM), np.float32))
audio = np.concatenate(partes)
(raiz / "audio").mkdir(exist_ok=True)
sf.write(raiz / "audio/narracao.wav", audio, SR)
json.dump({"duracao": round(len(audio) / SR, 3), "blocos": tempos}, open(aqui / "tempos.json", "w"), indent=1)
print(f"total {len(audio)/SR:.2f}s; fala termina em {tempos[-1]['e']:.2f}s")
