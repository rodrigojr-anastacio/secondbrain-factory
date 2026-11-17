# Em Relevo 006: mix = narração + trilha Kevin MacLeod (ducking) + SFX nas peças (toc nos pinos/colunas, tum nos números, papel nas fotos/docs, whoosh nos cortes de câmera/estilo).
# Base: mix_audio.py do 005, adaptado ao cues.json do motor 2D. Saída: audio/mix.wav (48 kHz).
import json, subprocess, numpy as np
from pathlib import Path
A = Path(__file__).parent; R = A.parent; SR = 48000
def carrega(p, ss=0, dur=None, filtro=None):
    cmd = ["ffmpeg", "-v", "quiet", "-ss", str(ss), "-i", str(p)] + (["-t", str(dur)] if dur else []) + (["-af", filtro] if filtro else []) + ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).copy()
db = lambda x: 10 ** (x / 20)
voz = carrega(R / "audio/narracao.wav"); c = json.load(open(A / "cues.json"))
N = int(c["duracao"] * SR) + SR; voz = np.pad(voz, (0, max(0, N - len(voz))))[:N]
sfx = np.zeros(N, np.float32); S = R / "dl/sfx"
def norm(x): return x / (np.abs(x).max() + 1e-9)
TOC = [norm(carrega(S / "toc-madeira-real-stephan.wav", 0.485, 0.14, "highpass=f=500,afade=t=out:st=0.03:d=0.11"))] + [norm(carrega(S / f"toc-madeira-{k}.wav")) for k in (1, 3)]
TUM = norm(carrega(S / "tum-abafado-1.wav", filtro="lowpass=f=900")); PAPEL = norm(carrega(S / "papel-colocando.wav"))
WH = {k: norm(carrega(S / f"{k}.wav")) for k in ("whoosh-curto-1", "whoosh-medio", "whoosh-longo", "swish-whip-pan", "impacto-boom-1")}
TECLA = norm(carrega(S / "datilografia-maquina-wws-26s.wav", 2.0, 2.5))
def put(sig, t, g):
    i = int(t * SR)
    if 0 <= i < N: s = sig[: N - i]; sfx[i:i + len(s)] += db(g) * s
n = {"toc": 0, "tum": 0, "papel": 0, "whoosh": 0}
for k, a in enumerate(c["anc"]):
    if a["k"] in ("pino", "coluna"): put(TOC[k % 3], a["t0"] + 0.3, -20); n["toc"] += 1
for x in c["numero"]:
    if not x.get("oculto"): put(TUM, x["t"], -29); n["tum"] += 1
for x in c["cenas"]:
    if x["k"] in ("foto", "doc", "dupla", "ficha1967", "cortica", "card", "citacao"): put(PAPEL, x["t0"], -24); n["papel"] += 1
    elif x["k"] in ("bloco", "cortina", "resposta", "fases", "pluv", "postos", "lama", "casca_esq"): put(WH["whoosh-medio"], x["t0"] - 0.3, -22); n["whoosh"] += 1
for h in c["hud"]:
    if h["k"] in ("cartao", "pergunta"): put(TECLA[: int(SR * 1.4)] * np.linspace(1, 0.3, int(SR * 1.4)), h["t0"] + 0.1, -30)
    if h["k"] == "ficha": put(TUM, h["t0"], -27)
    if h["k"] == "selo_grande": put(WH["impacto-boom-1"], h["t0"], -20)
for a, b in zip(c["camera"][:-1], c["camera"][1:]):   # cortes de câmera (par com Δt ≈ 1 ms): whoosh curto
    if b["t"] - a["t"] < 0.01 and b["t"] > 1: put(WH["whoosh-curto-1"], b["t"] - 0.15, -23); n["whoosh"] += 1
t = {b["id"]: b for b in json.load(open(A / "tempos.json"))["blocos"]}
mus = np.zeros(N, np.float32)
for arq, t0, t1 in (("Echoes_of_Time.mp3", 0, t["b14"]["s"] - 0.8), ("Ossuary_6_Air.mp3", t["b14"]["s"] - 0.8, t["b34"]["s"] - 1.0), ("Frozen_Star.mp3", t["b34"]["s"] - 1.0, c["duracao"])):
    dur = t1 - t0 + 3; x = carrega(R / "dl/musica" / arq)
    if len(x) < dur * SR: x = np.tile(x, int(dur * SR / len(x)) + 1)
    x = x[: int(dur * SR)]; m = len(x); f = np.ones(m, np.float32); fi = int(2.5 * SR); f[:fi] = np.linspace(0, 1, fi); f[-int(3 * SR):] = np.linspace(1, 0, int(3 * SR))
    x = x / (np.sqrt((x ** 2).mean()) + 1e-9) * 0.1 * f; i0 = int(t0 * SR); s = x[: N - i0]; mus[i0:i0 + len(s)] += s
env = np.sqrt(np.convolve(voz ** 2, np.ones(int(0.08 * SR)) / int(0.08 * SR), "same")); ativo = (env > 0.01).astype(np.float32)
sol = np.zeros_like(ativo); k = np.exp(-1 / (0.6 * SR)); acc = 0.0
for i in range(0, N, 480): acc = max(ativo[i], acc * k ** 480); sol[i:i + 480] = acc
g = db(-21) * (1 - 0.55 * sol); fim = int(c["fim_fala"] * SR); g[fim:] = np.linspace(g[fim], db(-14), N - fim)
mix = voz + sfx + mus * g; mix /= max(1.0, np.abs(mix).max() / 0.95)
subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", str(R / "audio/mix.wav")], input=mix.astype(np.float32).tobytes(), check=True)
print("mix", round(N / SR, 2), "s;", n)
