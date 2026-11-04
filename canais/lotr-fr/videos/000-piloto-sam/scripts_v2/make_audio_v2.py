"""Synthesise the ORIGINAL V2 ambient bed and SFX (no external samples).

Deterministic (seeded). Writes mono 16-bit WAVs to public/assets/v2/.
Ducking/fades are applied in Remotion (src/v2/VideoV2.jsx), not here.
"""
import array
import math
import os
import random
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'public', 'assets', 'v2')
os.makedirs(OUT, exist_ok=True)
rng = random.Random(1954)


def save(name, data, sr, peak):
    m = max(abs(x) for x in data) or 1.0
    g = peak / m
    pcm = array.array('h', (int(max(-1.0, min(1.0, x * g)) * 32767) for x in data))
    with wave.open(os.path.join(OUT, name), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())
    print(f'{name}: {len(data) / sr:.2f}s @ {sr} Hz, peak {20 * math.log10(peak):.1f} dBFS')


# --- Ambient bed: slow D / Bm / G / A pad + soft filtered wind, 60 s -------
SR = 22050
N = SR * 60
bed = [0.0] * N
CHORDS = [(73.42, 110.0, 185.0), (61.74, 92.5, 146.83), (98.0, 146.83, 246.94), (110.0, 164.81, 277.18)]
SEG, XF = 7.5, 2.0
for k in range(8):
    chord = CHORDS[k % 4]
    a, b = k * SEG - XF / 2, (k + 1) * SEG + XF / 2
    i0, i1 = max(0, int(a * SR)), min(N, int(b * SR))
    for fi, f in enumerate(chord):
        amp = (0.5, 0.35, 0.22)[fi]
        w1 = 2 * math.pi * f / SR
        lfo = 2 * math.pi * (0.07 + 0.03 * fi) / SR
        ph = rng.random() * 6.28
        for i in range(i0, i1):
            t = i / SR
            e = min(1.0, (t - a) / XF, (b - t) / XF)
            if e <= 0:
                continue
            e = 0.5 - 0.5 * math.cos(math.pi * e)
            bed[i] += amp * e * (math.sin(w1 * i + ph) + 0.18 * math.sin(2 * w1 * i + ph)) * (0.8 + 0.2 * math.sin(lfo * i))
lp = lp2 = 0.0
for i in range(N):
    lp += 0.02 * (rng.uniform(-1, 1) - lp)
    lp2 += 0.02 * (lp - lp2)
    bed[i] += 6.0 * lp2 * (0.6 + 0.4 * math.sin(2 * math.pi * 0.05 * i / SR))
for i in range(N):
    t = i / SR
    bed[i] *= min(1.0, t / 2.0, (60 - t) / 3.0)
save('bed_v2.wav', bed, SR, 0.5)

SR2 = 44100


def whoosh(dur=1.0):
    n = int(dur * SR2)
    out, lp, lp2 = [], 0.0, 0.0
    for i in range(n):
        x = i / n
        c = 0.01 + 0.22 * math.sin(math.pi * x) ** 3
        lp += c * (rng.uniform(-1, 1) - lp)
        lp2 += c * (lp - lp2)
        out.append(lp2 * math.sin(math.pi * x) ** 2)
    return out


def page(dur=0.6):
    n = int(dur * SR2)
    out, lp, sm = [], 0.0, 0.0
    for i in range(n):
        x = i / n
        s = rng.uniform(-1, 1)
        lp += 0.15 * (s - lp)
        burst = 2.5 if rng.random() < 0.015 else 1.0
        sm += 0.5 * ((s - lp) - sm)
        out.append(sm * burst * math.sin(math.pi * min(1.0, x * 1.3)) ** 2 * (1 - x) ** 0.5)
    return out


def impact(dur=1.4):
    n = int(dur * SR2)
    out, ph = [], 0.0
    for i in range(n):
        t = i / SR2
        ph += 2 * math.pi * (45 + 50 * math.exp(-t * 8)) / SR2
        out.append(math.sin(ph) * math.exp(-t * 3.2) + rng.uniform(-1, 1) * math.exp(-t * 60) * 0.35)
    return out


def sea(dur=6.4):
    n = int(dur * SR2)
    out, lp, lp2 = [], 0.0, 0.0
    for i in range(n):
        t = i / SR2
        lp += 0.03 * (rng.uniform(-1, 1) - lp)
        lp2 += 0.03 * (lp - lp2)
        swell = 0.55 + 0.45 * math.sin(2 * math.pi * t / 3.2 - 1.5)
        out.append((0.6 * lp + 2 * lp2) * swell * min(1.0, t / 1.0, (dur - t) / 1.5))
    return out


save('sfx_whoosh.wav', whoosh(), SR2, 0.7)
save('sfx_page.wav', page(), SR2, 0.7)
save('sfx_impact.wav', impact(), SR2, 0.7)
save('sfx_sea.wav', sea(), SR2, 0.7)
