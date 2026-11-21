#!/usr/bin/env python3
"""Áudios de época do 006-chernobyl (A1…A6) → audio/epoca/A#.wav + audio/epoca/epoca.json (duração, forma de onda por quadro, legendas com tempo).
Fontes reais (Commons, PD-UA-exempt) em ~/cache/tmp/chaudio/{tel,evac}.wav; A5 = voz sintética (Fish) lendo o texto TASS (RECONSTRUCTION).
Cortes: cada ponta é ajustada para o ponto de menor energia (±0,35 s) para não cortar sílaba. Tempos das frases = Whisper ru/en conferido na etapa 2 (21/11/2026).
Rodar da pasta do vídeo: ~/workspace/fabrica-youtube/tools/.venv/bin/python tools/epoca.py"""
import json, subprocess
from pathlib import Path
import numpy as np

V = Path(__file__).resolve().parent.parent
CH = Path.home() / "cache/tmp/chaudio"
SR, FPS = 48000, 30
OUT = V / "audio/epoca"; OUT.mkdir(parents=True, exist_ok=True)


def ler(p, ss=None, to=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + (["-to", str(to)] if to is not None else []) + \
          ["-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).astype(np.float64)


def bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    g = 1 / np.sqrt(1 + (lo / np.maximum(f, 1)) ** 8) / np.sqrt(1 + (f / hi) ** 8)
    return np.fft.irfft(X * g, len(x))


def norm_rms(x, alvo_db):
    r = np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2) + 1e-12)
    return x * 10 ** (alvo_db / 20) / r


def fade(x, a=0.02, b=0.05):
    ia, ib = int(a * SR), int(b * SR)
    if ia: x[:ia] *= np.linspace(0, 1, ia)
    if ib: x[-ib:] *= np.linspace(1, 0, ib)
    return x


def snap(x, t, jan=0.35):
    """ponto de menor energia (janelas de 20 ms) em t ± jan, sobre o sinal x (SR)."""
    w = int(0.02 * SR); a = max(0, int((t - jan) * SR)); b = min(len(x) - w, int((t + jan) * SR))
    if b <= a: return t
    best = min(range(a, b, w // 2), key=lambda i: float(np.mean(x[i:i + w] ** 2)))
    return (best + w // 2) / SR


# fonte → lista de trechos (a, b) na fonte; legendas = (a_src, b_src, original, inglês)
ESPEC = {
    "A1": dict(src="tel", banda=(120, 6000), trechos=[(4.8, 13.1)], snap=False,
               leg=[(5.3, 11.2, "«Взрыв на главном корпусе, 3–4 блок.»", "Explosion at the main building, units three and four."),
                    (11.28, 12.5, "«А там люди есть?»", "Are there people there?"),
                    (12.58, 13.1, "«Да.»", "Yes.")]),
    "A2": dict(src="evac", banda=(100, 7000), trechos=[(54.9, 57.95)], snap=False,
               leg=[(55.0, 58.0, "«…провести временную эвакуацию…»", "…to carry out a TEMPORARY evacuation…")]),
    "A3": dict(src="tel", banda=(120, 6000), trechos=[(24.9, 32.0), (42.5, 52.4)], snap=True,
               leg=[(25.3, 31.7, "«Алло, Припять… 3-й и 4-й блок горит крыша…»", "Hello, Pripyat… units three and four, the roof is burning…"),
                    (42.8, 44.9, "«Алло, Иванков?»", "Hello, Ivankov?"),
                    (45.5, 52.2, "«…на атомную станцию высылайте…»", "…send [the crews] to the nuclear plant…")]),
    "A4": dict(src="evac", banda=(100, 7000), trechos=[(11.4, 32.45), (51.8, 61.8), (126.3, 134.5)], snap=True,
               leg=[(11.4, 19.3, "«Уважаемые товарищи, городской совет народных депутатов сообщает…»", "Dear comrades! The City Council of People's Deputies announces that…"),
                    (19.4, 26.3, "", "…due to the accident at the Chernobyl nuclear power station, in the city of Pripyat…"),
                    (26.4, 32.2, "", "…unfavourable radiation conditions are developing."),
                    (52.0, 61.8, "«…необходимость провести временную эвакуацию…»", "…it has become necessary to carry out a TEMPORARY evacuation of the city's residents…"),
                    (126.3, 134.5, "«…временно оставляя своё жильё, не забудьте закрыть окна…»", "Comrades, when TEMPORARILY leaving your homes, please do not forget to close the windows…")]),
    "A5": dict(src="tass", trechos=[(0.0, 13.95)], snap=False,
               leg=[(0.0, 2.95, "", "An accident has occurred at the Chernobyl nuclear power station."),
                    (3.5, 5.55, "", "One of the atomic reactors has been damaged."),
                    (6.2, 9.2, "", "Measures are being taken to eliminate the consequences of the accident."),
                    (9.6, 11.6, "", "Those affected are being given assistance."),
                    (12.1, 13.9, "", "A government commission has been set up.")]),
    "A6": dict(src="tel", banda=(120, 6000), trechos=[(11.1, 13.3)], snap=False,
               leg=[(11.28, 12.5, "«А там люди есть?»", "Are there people there?"),
                    (12.58, 13.1, "«Да.»", "Yes.")]),
}
FONTES = {"tel": CH / "tel.wav", "evac": CH / "evac.wav", "tass": V / "audio/epoca/tass/T5.mp3"}
res = {}
for k, e in ESPEC.items():
    x = ler(FONTES[e["src"]])
    if e["src"] == "tass":
        x = np.tanh(bp(x, 250, 3800) * 3)   # rádio dos anos 80: banda estreita + leve saturação (marca a reconstrução; não imita locutor)
        alvo = -21
    else:
        x = bp(x, *e["banda"]); alvo = -20
    partes, mapa, off = [], [], 0.0
    for a, b in e["trechos"]:
        if e["snap"]:
            a, b = snap(x, a), snap(x, b)
        seg = x[int(a * SR):int(b * SR)].copy()
        if partes:
            partes.append(np.zeros(int(0.25 * SR))); off += 0.25
        mapa.append((a, b, off)); off += len(seg) / SR
        partes.append(seg)
    y = np.concatenate(partes)
    y = fade(norm_rms(y, alvo), 0.05 if k not in ("A5",) else 0.02, 0.2)
    peak = np.max(np.abs(y)); y = y * min(1.0, 0.89 / (peak + 1e-9))
    hop = SR // FPS; n = len(y) // hop
    r = np.sqrt(np.mean(y[: n * hop].reshape(n, hop) ** 2, axis=1)); r = r / (r.max() + 1e-9)
    wav = OUT / f"{k}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", str(wav)],
                   input=y.astype(np.float32).tobytes(), check=True)
    leg = []
    for a, b, o, en in e["leg"]:
        for sa, sb, so in mapa:
            if sa - 0.5 <= a <= sb + 0.5:
                ra = max(0.0, so + (a - sa)); rb = min(len(y) / SR, so + (min(b, sb + 0.4) - sa)); leg.append([round(ra, 2), round(rb, 2), o, en]); break
        else:
            raise SystemExit(f"{k}: legenda {a}-{b} fora dos trechos")
    res[k] = dict(dur=round(len(y) / SR, 3), trechos=[(round(a, 2), round(b, 2)) for a, b, _ in mapa], leg=leg, onda=[round(float(v), 3) for v in r])
    print(k, res[k]["dur"], res[k]["trechos"])
json.dump(res, open(OUT / "epoca.json", "w"), ensure_ascii=False)
