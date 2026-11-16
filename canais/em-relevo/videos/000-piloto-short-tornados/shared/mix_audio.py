# Mix final: narração + SFX sintetizados no código (pop de pino/etiqueta, whoosh nas viradas de câmera, clique da tachinha)
# + drone grave discreto. Tudo gerado aqui (sem licença de terceiros). Saída: audio/mix.wav (loudnorm -14 LUFS no render.sh).
import json, numpy as np, soundfile as sf
from pathlib import Path
A = Path(__file__).parent; R = A.parent
SR = 48000
voz, sr = sf.read(R / "audio/narracao.wav", dtype="float32")
voz = np.interp(np.arange(int(len(voz) * SR / sr)) / SR, np.arange(len(voz)) / sr, voz).astype(np.float32)
c = json.load(open(A / "cues.json")); tempos = json.load(open(A / "tempos.json"))
N = len(voz); mix = voz.copy()
rng = np.random.default_rng(7)
def env(n, a, d): t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def pop():
    n = int(0.12 * SR); t = np.arange(n) / SR
    f = 900 * np.exp(-t * 30) + 380
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.03)).astype(np.float32)
def clique():
    n = int(0.05 * SR); return (rng.standard_normal(n) * env(n, 0.0005, 0.006)).astype(np.float32)
def whoosh(d=0.7):
    n = int(d * SR); x = rng.standard_normal(n).astype(np.float32)
    k = np.hanning(n) ** 1.5
    # passa-banda simples variando: média móvel de janela variável
    y = np.convolve(x, np.ones(9) / 9, "same") - np.convolve(x, np.ones(60) / 60, "same")
    return (y * k).astype(np.float32)
def put(sig, t, g):
    i = int(t * SR)
    if i >= N: return
    s = sig[: N - i]; mix[i:i + len(s)] += g * s
for p in c["pinos"]: put(pop(), p["t"] + 0.33, 0.20 if p.get("pequeno") else 0.30)
for k in c["clipes"]: put(clique(), k["t0"] + 0.05, 0.35); put(pop(), k["t0"], 0.18)
for n in c["numero"]:
    if not n.get("oculto"): put(pop(), n["t"], 0.16)
for it in c["caixas"]["itens"]: put(pop(), it["t"], 0.22)
put(pop(), c["manchete"]["t0"], 0.2); put(pop(), c["cta"]["t0"], 0.25)
for b in ("b02", "b03", "b04", "b07"):
    t = next(x["s"] for x in tempos["blocos"] if x["id"] == b); put(whoosh(0.8), max(0, t - 0.35), 0.22)
# drone grave (55 Hz + 82,5 Hz com batimento lento), -30 dB sob a voz, fade in/out
t = np.arange(N) / SR
drone = 0.5 * np.sin(2 * np.pi * 55 * t) + 0.3 * np.sin(2 * np.pi * 82.5 * t + 0.4 * np.sin(2 * np.pi * 0.13 * t))
drone *= (0.8 + 0.2 * np.sin(2 * np.pi * 0.21 * t)) * np.minimum(1, t / 1.5) * np.minimum(1, (N / SR - t) / 1.5)
mix += 0.03 * drone.astype(np.float32)
mix /= max(1.0, np.abs(mix).max() / 0.95)
sf.write(R / "audio/mix.wav", mix, SR)
print("mix", round(N / SR, 2), "s")
