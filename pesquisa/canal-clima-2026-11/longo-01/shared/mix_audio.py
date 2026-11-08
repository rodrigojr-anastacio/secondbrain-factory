# Mix final do longo 01: narração + trilha (Kevin MacLeod, CC BY 4.0) com ducking sob a voz + SFX livres (dl/sfx; ver FONTES-E-LICENCAS.md).
# SFX (pedido do Rodrigo, 08/11): pino = "toc" seco de madeira (sem bip); número = "tum" abafado bem baixo; whoosh/papel como no piloto;
# transições com SFX coerente. Saída: audio/mix.wav (48 kHz; loudnorm −14 LUFS na junção do render.sh).
import json, subprocess, numpy as np, soundfile as sf
from pathlib import Path
A = Path(__file__).parent; R = A.parent; SR = 48000
def carrega(p, ss=0, dur=None, filtro=None):
    cmd = ["ffmpeg", "-v", "quiet", "-ss", str(ss), "-i", str(p)] + (["-t", str(dur)] if dur else []) + (["-af", filtro] if filtro else []) + ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).copy()
db = lambda x: 10 ** (x / 20)
voz = carrega(R / "audio/narracao.wav")
c = json.load(open(A / "cues.json"))
N = int(c["duracao"] * SR) + SR; voz = np.pad(voz, (0, max(0, N - len(voz))))[:N]
mix = voz.copy(); sfx = np.zeros(N, np.float32)
S = R / "dl/sfx"
def norm(x): return x / (np.abs(x).max() + 1e-9)
TOC = [norm(carrega(S / "toc-madeira-real-stephan.wav", 0.485, 0.14, "highpass=f=500,afade=t=out:st=0.03:d=0.11"))] + [norm(carrega(S / f"toc-madeira-{k}.wav")) for k in (1, 3)]
TUM = norm(carrega(S / "tum-abafado-1.wav", filtro="lowpass=f=900"))
PAPEL = norm(carrega(S / "papel-colocando.wav"))
WH = {k: norm(carrega(S / f"{k}.wav")) for k in ("whoosh-curto-1", "whoosh-curto-2", "whoosh-medio", "whoosh-longo", "swish-whip-pan", "impacto-boom-1", "impacto-boom-2")}
TECLA = norm(carrega(S / "datilografia-maquina-wws-26s.wav", 2.0, 2.5))
TROVAO = norm(carrega(S / "trovao-distante-1.wav")); TROVAO2 = norm(carrega(S / "trovao-distante-2.wav"))
VENTO = norm(carrega(S / "ambiente-vento-tempestade-killiney-60s.wav"))
def put(sig, t, g_db, alvo=None):
    alvo = sfx if alvo is None else alvo
    i = int(t * SR)
    if i >= N or i < 0: return
    s = sig[: N - i]; alvo[i:i + len(s)] += db(g_db) * s
contagem = {"pino": 0, "numero": 0, "papel": 0, "trans": 0}
for k, p in enumerate(c["pinos"]):
    put(TOC[k % 3], p["t"] + 0.33, -24 if p.get("pequeno") else -19); contagem["pino"] += 1
for n in c["numero"]:
    if not n.get("oculto"): put(TUM, n["t"], -30); contagem["numero"] += 1
for m in c["midia"]: put(PAPEL, m["t0"], -24); contagem["papel"] += 1
for it in c["cortica"]["itens"]: put(PAPEL, it["t"], -25); put(TOC[0], it["t"] + 0.15, -22)
for m in c["manchetes"]: put(PAPEL, m["t0"], -23)
for g in c["graficos"]: put(PAPEL, g["t0"], -26)
for k in c["cartoes"] + [c["pergunta"]]: put(TECLA[: int(SR * min(2.4, 0.04 * len(k["texto"]) + 0.5))] * np.linspace(1, 0.3, int(SR * min(2.4, 0.04 * len(k["texto"]) + 0.5))), k["t0"] + 0.1, -30)
for k in c["cartoes"]:
    if k.get("carimbo"): put(WH["impacto-boom-2"], k["carimbo"]["t"], -24)
for e in c["caixas"]["estados"]:
    if e.get("volta"): put(WH["whoosh-curto-1"], e["t"] - 0.1, -24)
for it in c["caixas"]["itens"]: put(TUM, it["t"], -27)
TR = {"nuvem": [("whoosh-longo", -0.9, -15)], "whip": [("swish-whip-pan", -0.12, -14), ("whoosh-curto-2", -0.3, -19)], "luz": [("whoosh-medio", -0.6, -22)],
      "corte": [("impacto-boom-1", 0.0, -14)], "orbital": [("whoosh-longo", -0.9, -17)], "rack": [("whoosh-medio", -0.5, -21)],
      "match": [("impacto-boom-2", 0.0, -18), ("whoosh-curto-1", -0.35, -21)], "whip_v": [("swish-whip-pan", -0.12, -14), ("whoosh-curto-2", -0.3, -19)],
      "match_funil": [("impacto-boom-1", 0.0, -18)], "zoomout": [("whoosh-longo", -0.8, -17)]}
for x in c["transicoes"]:
    for nome, dt, g in TR[x["tipo"]]: put(WH[nome], x["t"] + dt, g)
    contagem["trans"] += 1
# câmera rápida dentro dos blocos (corte de chave > 3 unidades em < 1,5 s): whoosh curto
cam = c["camera"]
for a, b in zip(cam[:-1], cam[1:]):
    d = sum((a["alvo"][i] - b["alvo"][i]) ** 2 for i in range(3)) ** 0.5
    if not b.get("corte") and d > 3.0 and b["t"] - a["t"] < 2.5: put(WH["whoosh-curto-1"], a["t"], -25)
# ambiente de tempestade baixo nos dias de tornado + trovões distantes
blocos = {b["id"]: b for b in json.load(open(A / "tempos.json"))["blocos"]}
def amb(t0, t1, g):
    i0, i1 = int(t0 * SR), min(N, int(t1 * SR)); n = i1 - i0
    v = np.tile(VENTO, n // len(VENTO) + 1)[:n] * np.minimum(1, np.minimum(np.arange(n), n - np.arange(n)) / (1.5 * SR))
    sfx[i0:i1] += db(g) * v
amb(blocos["b08"]["s"] - 1, blocos["b18"]["e"], -33)
put(TROVAO, blocos["b08"]["s"] - 0.8, -26); put(TROVAO2, blocos["b11"]["s"] + 0.5, -27); put(TROVAO, blocos["b17"]["s"] - 0.5, -25); put(TROVAO2, blocos["b29"]["s"], -29)
# trilha: 3 faixas Kevin MacLeod com crossfade nas viradas de capítulo
mus = np.zeros(N, np.float32)
FAIXAS = [("Echoes_of_Time.mp3", 0, blocos["b19"]["s"] - 0.8), ("Ossuary_6_Air.mp3", blocos["b19"]["s"] - 0.8, blocos["b37"]["s"] - 1.0), ("Frozen_Star.mp3", blocos["b37"]["s"] - 1.0, c["duracao"])]
for arq, t0, t1 in FAIXAS:
    dur = t1 - t0 + 3
    x = carrega(R / "dl/musica" / arq, 0, None)
    if len(x) < dur * SR: x = np.tile(x, int(dur * SR / len(x)) + 1)
    x = x[: int(dur * SR)]; n = len(x)
    f = np.ones(n, np.float32); fi = int(2.5 * SR); f[:fi] = np.linspace(0, 1, fi); f[-int(3 * SR):] = np.linspace(1, 0, int(3 * SR))
    x = x / (np.sqrt((x ** 2).mean()) + 1e-9) * 0.1 * f
    i0 = int(t0 * SR); s = x[: N - i0]; mus[i0:i0 + len(s)] += s
# ducking: envelope da voz (janela 80 ms, ataque rápido, soltura de 600 ms)
env = np.sqrt(np.convolve(voz ** 2, np.ones(int(0.08 * SR)) / int(0.08 * SR), "same"))
ativo = (env > 0.01).astype(np.float32)
sol = np.zeros_like(ativo); k = np.exp(-1 / (0.6 * SR)); acc = 0.0
for i in range(0, N, 480):  # resolução de 10 ms
    acc = max(ativo[i], acc * k ** 480); sol[i:i + 480] = acc
musica_g = db(-21) * (1 - 0.55 * sol)
fim = int(c["fim_fala"] * SR); musica_g[fim:] = np.linspace(musica_g[fim], db(-14), N - fim)  # trilha sobe no fim
mix = voz + sfx + mus * musica_g
mix /= max(1.0, np.abs(mix).max() / 0.95)
sf.write(R / "audio/mix.wav", mix, SR)
print("mix", round(N / SR, 2), "s;", contagem)
