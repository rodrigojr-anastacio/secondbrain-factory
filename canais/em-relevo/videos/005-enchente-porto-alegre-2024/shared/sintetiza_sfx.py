# Em Relevo 005 (15/11/2026): recria dl/sfx/*.wav (48 kHz mono) usados por mix_audio.py. Os WAV processados foram apagados pela limpeza de disco (classe A);
# gravações reais vêm de dl/sfx/raw (Wikimedia Commons, ver ../longo-01/pesquisa/MATERIAL-LIVRE.md) e o resto é SINTETIZADO aqui (numpy, sem licença de terceiros).
import subprocess, numpy as np
from pathlib import Path
R = Path(__file__).resolve().parent.parent; S = R / "dl/sfx"; RAW = S / "raw"; SR = 48000
rng = np.random.default_rng(5)
def salva(nome, x):
    x = (x / (np.abs(x).max() + 1e-9) * 0.9).astype(np.float32)
    subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", str(S / nome)], input=x.tobytes(), check=True)
def t_(d): return np.arange(int(d * SR)) / SR
def sino(f, d): return np.sin(2 * np.pi * f * t_(d))
def lp(x, a):   # passa-baixa de um polo, a (escalar ou vetor) em 0..1
    a = np.broadcast_to(a, x.shape); y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)): acc += a[i] * (x[i] - acc); y[i] = acc
    return y
def whoosh(d, f0, f1, pico=0.5):
    n = rng.standard_normal(int(d * SR)).astype(np.float32); u = np.linspace(0, 1, len(n))
    a = np.exp(-2 * np.pi * (f0 + (f1 - f0) * u) / SR) ; a = 1 - a   # frequência de corte varrendo f0 -> f1
    y = lp(n, a) - lp(n, a * 0.25)
    env = np.sin(np.pi * np.clip(u / (2 * pico) if False else np.where(u < pico, u / (2 * pico), 0.5 + (u - pico) / (2 * (1 - pico))), 0, 1)) ** 2
    return y * env
def conv(src, dst, ss=0, dur=None, af=None):
    cmd = ["ffmpeg", "-v", "quiet", "-y", "-ss", str(ss), "-i", str(RAW / src)] + (["-t", str(dur)] if dur else []) + (["-af", af] if af else []) + ["-ac", "1", "-ar", str(SR), str(S / dst)]
    subprocess.run(cmd, check=True)
# reais
conv("knock-wood-stephan.ogg", "toc-madeira-real-stephan.wav"); conv("storm-killiney-hill.ogg", "ambiente-vento-tempestade-killiney-60s.wav", 0, 60)
conv("typewriter-wws.ogg", "datilografia-maquina-wws-26s.wav", 0, 26); conv("paper-pages-stephan.ogg", "papel-paginas-stephan-20s.wav", 0, 20)
# sintetizados
for k, f in ((1, 210), (2, 260), (3, 320)):
    d = 0.25; e = np.exp(-t_(d) * 38); salva(f"toc-madeira-{k}.wav", (sino(f, d) + 0.5 * sino(f * 2.3, d)) * e + 0.15 * lp(rng.standard_normal(int(d * SR)).astype(np.float32), 0.3) * np.exp(-t_(d) * 120))
d = 0.45; salva("tum-abafado-1.wav", sino(68, d) * np.exp(-t_(d) * 11) * (1 - np.exp(-t_(d) * 400)))
d = 0.7; n = lp(rng.standard_normal(int(d * SR)).astype(np.float32), 0.35); salva("papel-colocando.wav", (n - lp(n, 0.02)) * np.sin(np.pi * np.linspace(0, 1, len(n))) ** 1.5)
salva("whoosh-curto-1.wav", whoosh(0.45, 400, 3500)); salva("whoosh-curto-2.wav", whoosh(0.6, 3000, 500)); salva("whoosh-medio.wav", whoosh(1.1, 300, 2600, 0.6)); salva("whoosh-longo.wav", whoosh(2.2, 200, 3000, 0.65))
salva("swish-whip-pan.wav", whoosh(0.28, 1500, 6000, 0.4))
for k, d in ((1, 2.0), (2, 2.6)):
    u = t_(d); f = 95 * np.exp(-u * 1.2) + 32; fase = 2 * np.pi * np.cumsum(f) / SR
    salva(f"impacto-boom-{k}.wav", np.sin(fase) * np.exp(-u * 2.2) * (1 - np.exp(-u * 300)) + 0.3 * lp(rng.standard_normal(len(u)).astype(np.float32), 0.04) * np.exp(-u * 3))
for k, d in ((1, 7.0), (2, 9.0)):
    u = t_(d); n = lp(rng.standard_normal(len(u)).astype(np.float32), 0.012); env = (1 - np.exp(-u * 2.5)) * np.exp(-u * (0.55 if k == 1 else 0.4)) * (1 + 0.5 * np.sin(u * 2.1 + k))
    salva(f"trovao-distante-{k}.wav", n * np.clip(env, 0, None))
print(sorted(p.name for p in S.glob("*.wav")))
