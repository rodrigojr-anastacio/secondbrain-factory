"""Amostra Chernobyl (Clearance Required, 21/11/2026): prepara mídia, mapa, mix de áudio e src/timeline.json.
Rodar da pasta da amostra: ~/workspace/fabrica-youtube/tools/.venv/bin/python -I tools/prep.py
Áudio real: ~/cache/tmp/chaudio/{tel,evac}.wav (Commons, PD-UA-exempt; ver AMOSTRA.md). Trilha e SFX: sintetizados aqui
(numpy), exceto a máquina de escrever (gravação do Commons usada no dossie-es/001-cia, mesma fonte)."""
import json, subprocess
from pathlib import Path
import numpy as np

R = Path(__file__).resolve().parent.parent
PUB = R / "public"; AUD = R / "audio"; SR = 48000; FPS = 30
CH = Path.home() / "cache/tmp/chaudio"
TYPE = Path.home() / "workspace/fabrica-youtube/canais/em-relevo/videos/006-caraguatatuba-1967/dl/sfx/raw/typewriter-wws.ogg"
rng = np.random.default_rng(7)

# ---------------- tempos (s) ----------------
T = dict(
    disp=(0.6, 4.8, 13.1),       # início na timeline, trecho do tel.wav
    glitch1=(8.9, 9.6),
    typed=9.6, board=10.9,
    N1=10.9, N2=15.9, glitch2=(17.5, 18.2), N3=18.8,
    run=(19.0, 36.0), N4=25.0, stamp=28.3,
    evac=(29.0, 55.0, 58.0),
    N5=32.3, tass=36.0, N6=42.1, fim=46.0,
)


def ler(p, ss=None, to=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + (["-to", str(to)] if to is not None else []) + \
          ["-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def db(x):
    return 10 ** (x / 20)


def norm_rms(x, alvo_db):
    r = np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2) + 1e-12)
    return x * db(alvo_db) / r


def fade(x, a=0.02, b=0.05):
    n = len(x); ia, ib = int(a * SR), int(b * SR)
    if ia: x[:ia] *= np.linspace(0, 1, ia)
    if ib: x[-ib:] *= np.linspace(1, 0, ib)
    return x


def lp(x, a):
    # passa-baixa aproximado (FFT): corte ~ a*SR/(2*pi)
    fc = a * SR / (2 * np.pi)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / max(fc, 1)) ** 4), len(x))


def bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    g = 1 / np.sqrt(1 + (lo / np.maximum(f, 1)) ** 8) / np.sqrt(1 + (f / hi) ** 8)
    return np.fft.irfft(X * g, len(x))


N = int(T["fim"] * SR)
voz = np.zeros(N); arq = np.zeros(N); musica = np.zeros(N); sfx = np.zeros(N)


def put(buf, t, x, g=1.0):
    i = int(t * SR); j = min(N, i + len(x))
    buf[i:j] += x[: j - i] * g


# ---------- áudio de época (real) ----------
d0, a, b = T["disp"]
disp = bp(ler(CH / "tel.wav", a, b), 120, 6000)
disp = fade(norm_rms(disp, -20), 0.05, 0.25)
put(arq, d0, disp)
e0, a, b = T["evac"]
evac = bp(ler(CH / "evac.wav", a - 0.1, b + 0.15), 100, 7000)
evac = fade(norm_rms(evac, -20), 0.15, 0.3)
put(arq, e0 - 0.1, evac)

# ---------- vozes ----------
tempos_voz = {}
for k in ["N1", "N2", "N3", "N4", "N5", "N6"]:
    x = ler(AUD / f"narr/{k}.mp3"); x = norm_rms(x, -19)
    put(voz, T[k], fade(x, 0.01, 0.05)); tempos_voz[k] = (T[k], T[k] + len(x) / SR)
tass = ler(AUD / "tass/T1.mp3")
# rádio dos anos 80: banda estreita + leve saturação, para marcar que é RECONSTRUÇÃO (não imita locutor)
tass = np.tanh(bp(tass, 250, 3800) * 3) ; tass = norm_rms(tass, -21)
put(voz, T["tass"], fade(tass, 0.02, 0.1)); tempos_voz["T1"] = (T["tass"], T["tass"] + len(tass) / SR)

# ---------- trilha (drone sintetizado) ----------
t = np.arange(N) / SR
drone = (np.sin(2 * np.pi * 55 * t) * 0.5 + np.sin(2 * np.pi * 82.4 * t + 0.3) * 0.25 + np.sin(2 * np.pi * 110.3 * t) * 0.12)
drone *= 1 + 0.25 * np.sin(2 * np.pi * 0.11 * t)
ar = lp(rng.standard_normal(N), 0.004) * 6
pulso = np.zeros(N)
for k in np.arange(T["run"][0], T["run"][1], 1.6):   # pulso grave lento enquanto o relógio corre
    i = int(k * SR); d = int(0.5 * SR); u = np.arange(d) / SR
    pulso[i:i + d] += np.sin(2 * np.pi * 48 * u) * np.exp(-u * 7) * 0.8
mus = norm_rms(drone + ar, -30) + pulso * db(-26)
env = np.zeros(N)
def rampa(t0, t1, v0, v1):
    i, j = int(t0 * SR), int(t1 * SR); env[i:j] = np.linspace(v0, v1, j - i)
env[:] = 0
rampa(T["board"], T["board"] + 2.5, 0, 1); env[int((T["board"] + 2.5) * SR):] = 1
rampa(T["evac"][0] - 0.4, T["evac"][0], 1, 0.08); env[int(T["evac"][0] * SR):int((T["evac"][0] + 3.0) * SR)] = 0.08
rampa(T["evac"][0] + 3.0, T["evac"][0] + 3.6, 0.08, 1)
rampa(T["tass"] - 0.3, T["tass"], 1, 0.35); env[int(T["tass"] * SR):int((T["tass"] + 5.8) * SR)] = 0.35
rampa(T["tass"] + 5.8, T["tass"] + 6.3, 0.35, 1)
rampa(T["fim"] - 1.2, T["fim"], 1, 0)
musica = mus * env

# ---------- SFX ----------
def estatica(d, g=1.0):
    n = rng.standard_normal(int(d * SR)); x = bp(n, 800, 7000) * (0.6 + 0.4 * np.sign(np.sin(np.linspace(0, 90, len(n)))))
    return fade(norm_rms(x, -30) * g, 0.05, 0.1)
put(sfx, 0.0, estatica(1.0) * np.linspace(0.3, 1, int(1.0 * SR)))
put(sfx, T["glitch1"][0], estatica(0.7, db(4)))
put(sfx, T["glitch2"][0], estatica(0.7, db(2)))
# tum surdo quando o sinal cai (sem explosão de filme)
d = 1.4; u = np.arange(int(d * SR)) / SR
put(sfx, T["glitch2"][0] + 0.05, np.sin(2 * np.pi * (60 * np.exp(-u * 1.5) + 28) * u) * np.exp(-u * 3) * db(-14))
# máquina de escrever (data datilografada e teletipo do TASS)
tw = ler(TYPE); tw = norm_rms(tw, -27)
put(sfx, T["typed"], fade(tw[: int(1.25 * SR)].copy(), 0.01, 0.1))
put(sfx, T["N4"] + 0.2, fade(tw[int(3 * SR): int(4.6 * SR)].copy(), 0.01, 0.1), db(-4))
put(sfx, T["tass"], fade(tw[int(6 * SR): int(9.5 * SR)].copy(), 0.01, 0.2), db(-6))
# tique do relógio: 1/s no relógio congelado; 2/s abafado enquanto corre
def tique(g):
    d = 0.06; u = np.arange(int(d * SR)) / SR
    return (np.sin(2 * np.pi * 2400 * u) + 0.5 * np.sin(2 * np.pi * 5100 * u)) * np.exp(-u * 90) * g
for k in np.arange(T["typed"], T["N3"], 1.0):
    put(sfx, k, tique(db(-22)))
for k in np.arange(T["run"][0], T["run"][1], 0.5):
    put(sfx, k, tique(db(-30)))
# papel assentando nas entradas do mural
def papel(g=1.0):
    d = 0.5; n = rng.standard_normal(int(d * SR)); x = bp(n, 1500, 9000) * np.sin(np.pi * np.linspace(0, 1, len(n))) ** 2
    return norm_rms(x, -32) * g
for k in [T["board"], 13.5, T["N3"], T["N4"], T["N5"], 33.6, T["tass"]]:
    put(sfx, k, papel())
# carimbo
d = 0.35; u = np.arange(int(d * SR)) / SR
put(sfx, T["stamp"], (np.sin(2 * np.pi * 95 * u) * np.exp(-u * 25) + 0.4 * bp(rng.standard_normal(len(u)), 300, 3000) * np.exp(-u * 40)) * db(-12))

mix = voz + arq + musica + sfx
mix = np.tanh(mix * 1.0)
(PUB / "audio").mkdir(parents=True, exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f64le", "-ar", str(SR), "-ac", "1", "-i", "-",
                "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(PUB / "audio/mix.wav")],
               input=mix.astype(np.float64).tobytes(), check=True)

# ---------- forma de onda (para a tela) ----------
def onda(x, t0):
    hop = SR // FPS; n = len(x) // hop
    r = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1)); r = r / (r.max() + 1e-9)
    return {"inicio": t0, "rms": [round(float(v), 3) for v in r]}
ondas = {"disp": onda(disp, d0), "evac": onda(evac, e0 - 0.1), "tass": onda(tass, T["tass"])}

# ---------- imagens ----------
def ff(src, dst, vf):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(PUB / "img" / src), "-vf", vf, "-q:v", "3", str(PUB / "img" / dst)], check=True)
ff("controlroom.jpg", "controlroom-painel.jpg", "crop=1920:900:0:120")
ff("anefo6456.jpg", "anefo6456-s.jpg", "scale=1400:-1")
ff("kh9-1984.jpg", "kh9-s.jpg", "scale=2800:-1")
ff("insag7-p65.png", "insag7-p65.jpg", "scale=1100:-1")

# ---------- mapa da Europa (Natural Earth 50m, PD) ----------
geo = json.load(open(Path.home() / "cache/nasa/ne_50m_admin_0_countries.geojson"))
LON0, LON1, LAT0, LAT1 = 4.0, 42.0, 44.0, 67.0; MW, MH = 1100, 800
k = np.cos(np.radians(55)); sx = MW / ((LON1 - LON0) * k)
def prj(lon, lat):
    return ((lon - LON0) * k * sx, MH - (lat - LAT0) * sx * (MH / ((LAT1 - LAT0) * sx)) * ((LAT1 - LAT0) * sx / MH))
def prj(lon, lat):
    x = (lon - LON0) * k * sx; y = (LAT1 - lat) * sx
    return round(x, 1), round(y, 1)
paths = []
for f in geo["features"]:
    g = f["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    nome = f["properties"].get("ADMIN", "")
    for poly in polys:
        ring = poly[0]
        if not any(LON0 - 5 < lo < LON1 + 5 and LAT0 - 5 < la < LAT1 + 5 for lo, la in ring):
            continue
        pts = [prj(lo, la) for lo, la in ring[::2]]
        paths.append({"pais": nome, "d": "M" + "L".join(f"{x},{y}" for x, y in pts) + "Z"})
mapa = {"w": MW, "h": round((LAT1 - LAT0) * sx), "paths": paths,
        "chernobyl": prj(30.10, 51.39), "forsmark": prj(18.17, 60.40), "moscou": prj(37.62, 55.75)}

tl = {"fps": FPS, "durationInFrames": int(T["fim"] * FPS), "T": T, "voz": tempos_voz, "ondas": ondas, "mapa": mapa}
json.dump(tl, open(R / "src/timeline.json", "w"))
print(json.dumps({"dur": T["fim"], "voz": tempos_voz, "mapa_h": mapa["h"], "paths": len(paths)}, indent=1))
