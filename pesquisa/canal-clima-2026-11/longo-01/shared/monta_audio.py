# Junta as frases da Kokoro com pausas controladas -> audio/narracao.wav + shared/tempos.json (blocos e frases).
# 2 marchas (Rodrigo, 08/11): marcha 1 = piloto (vel 1,1 + atempo 1,05, pausas curtas); 1.5 = transição; 2 = mais calma
# (vel 1,02 sem atempo, pausas maiores entre ideias). Perguntas: subida de tom no fim (rubberband com rampa de pitch).
import json, re, subprocess, numpy as np, soundfile as sf
from pathlib import Path
A = Path(__file__).parent; R = A.parent; SR = 24000
ATEMPO = {1: 1.05, 1.5: 1.02, 2: 1.0}
GAP_FRASE = {1: 0.20, 1.5: 0.32, 2: 0.5}
GAP_BLOCO = {1: 0.42, 1.5: 0.6, 2: 0.75}
GAP_CAP = 1.35          # troca de capítulo: espaço para a transição de cinema
INICIO, FIM = 0.15, 2.5

def ff(a, filtro):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "quiet", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", filtro,
                                         "-f", "f32le", "-ar", str(SR), "-ac", "1", "-"], input=a.astype(np.float32).tobytes(), capture_output=True).stdout, np.float32)

def apara(a):
    env = np.abs(a) > 0.01
    i0, i1 = np.argmax(env), len(a) - np.argmax(env[::-1])
    return a[max(0, i0 - int(0.03 * SR)): min(len(a), i1 + int(0.06 * SR))]

def pergunta(a, frase):
    # rampa de pitch nos últimos ~0,5 s: sim/não sobe mais; pergunta com "que/qual/até" sobe menos
    sobe = 1.10 if re.match(r"^(Isso|E o aquecimento)", frase) else 1.07
    d = len(a) / SR; t0 = max(0, d - 0.55)
    n = 6; cmds = ";".join(f"{t0 + 0.5 * i / n:.3f} rubberband pitch {1 + (sobe - 1) * (i / n):.4f}" for i in range(n + 1))
    y = ff(a, f"asendcmd=c='{cmds}',rubberband=pitch=1.0:formant=preserved:transients=smooth")
    return y if abs(len(y) - len(a)) < SR * 0.2 and np.abs(y).max() > 0.01 else a

blocos = json.load(open(A / "blocos.json"))
partes = [np.zeros(int(SR * INICIO), np.float32)]; t = INICIO; tempos = []
for bi, b in enumerate(blocos):
    m = b["marcha"]; frases = [l for l in b["fala"].split("\n") if l.strip()]
    tb = {"id": b["id"], "s": round(t, 3), "frases": []}
    for k, fr in enumerate(frases):
        a, _ = sf.read(R / "work/voz" / f"{b['id']}-{k}.wav", dtype="float32")
        if ATEMPO[m] != 1.0: a = ff(a, f"atempo={ATEMPO[m]}")
        a = apara(a)
        if fr.rstrip().endswith("?"): a = apara(pergunta(a, fr))
        tb["frases"].append({"s": round(t, 3), "e": round(t + len(a) / SR, 3), "txt": fr})
        partes.append(a); t += len(a) / SR
        if k < len(frases) - 1:
            g = GAP_FRASE[m] + (0.12 if fr.rstrip().endswith("?") else 0)
            partes.append(np.zeros(int(SR * g), np.float32)); t += g
    tb["e"] = round(t, 3); tempos.append(tb)
    if bi < len(blocos) - 1:
        prox = blocos[bi + 1]
        g = GAP_CAP if prox["cap"].split(" ·")[0] != b["cap"].split(" ·")[0] and not (b["cap"].startswith("DIA") and prox["cap"].startswith("DIA") and False) else GAP_BLOCO[m]
        if prox["cap"] == b["cap"]: g = GAP_BLOCO[m]
        partes.append(np.zeros(int(SR * g), np.float32)); t += g
partes.append(np.zeros(int(SR * FIM), np.float32))
audio = np.concatenate(partes)
(R / "audio").mkdir(exist_ok=True)
sf.write(R / "audio/narracao.wav", audio, SR)
json.dump({"duracao": round(len(audio) / SR, 3), "blocos": tempos}, open(A / "tempos.json", "w"), ensure_ascii=False, indent=1)
# palavras por minuto por marcha (só tempo de fala + pausas internas do bloco)
pal = {1: [0, 0], 1.5: [0, 0], 2: [0, 0]}
for b, tb in zip(blocos, tempos):
    pal[b["marcha"]][0] += len(re.findall(r"\w+", b["fala"])); pal[b["marcha"]][1] += tb["e"] - tb["s"]
print(f"total {len(audio)/SR/60:.2f} min; fala termina em {tempos[-1]['e']:.1f}s")
for m, (n, s) in pal.items(): print(f"marcha {m}: {n} palavras em {s:.1f}s = {n/s*60:.0f} pal/min")
