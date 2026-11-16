# v2 (08/11/2026): junta a narração ElevenLabs v3 (audio/eleven-brutos/<id>.mp3) -> audio/narracao.wav + shared/tempos.json + shared/whisper.json.
# Velocidade (v3 não tem parâmetro): atempo no ffmpeg. Hook b01–b06 1,3×; b07 (passagem) 1,25×; resto 1,2× (brief v2).
# Cada bloco é transcrito sozinho (faster-whisper small) para: tempos por palavra, início/fim de cada frase, conferência ≥ 95% e tag falada.
# Saída da conferência: work/confere_voz_v2.txt. Uso: monta_audio_v2.py
import json, re, subprocess, unicodedata, difflib, numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
from normaliza_pt import norm as nn
A = Path(__file__).parent; R = A.parent; SR = 44100; BR = R / "audio/eleven-brutos"
def atempo(bid):
    n = int(bid[1:]); return 1.3 if n <= 6 else (1.25 if n == 7 else 1.2)
GAP_BLOCO = {1: 0.42, 1.5: 0.6, 2: 0.7}
GAP_CAP = 1.35
INICIO, FIM = 0.15, 2.5
TAGS = {"serious", "curious", "intrigued", "serio", "curioso", "intrigado"}

def n(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", " ", s).split()
def carrega(bid):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "quiet", "-i", str(BR / f"{bid}.mp3"), "-af", f"atempo={atempo(bid)}", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                        capture_output=True).stdout, np.float32).copy()
def apara(a):
    env = np.convolve(np.abs(a), np.ones(441) / 441, "same") > 0.006
    i0, i1 = np.argmax(env), len(a) - np.argmax(env[::-1])
    return a[max(0, i0 - int(0.03 * SR)): min(len(a), i1 + int(0.08 * SR))]

wm = WhisperModel("small", device="cpu", compute_type="int8")
def transcreve(a):
    x = np.interp(np.arange(0, len(a), SR / 16000), np.arange(len(a)), a).astype(np.float32)
    segs, _ = wm.transcribe(x, language="pt", word_timestamps=True)
    return [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)} for s in segs for w in s.words]

blocos = json.load(open(A / "blocos.json"))
partes = [np.zeros(int(SR * INICIO), np.float32)]; t = INICIO; tempos = []; whisper = []; rel = []; ruins = []
for bi, b in enumerate(blocos):
    a = apara(carrega(b["id"])); ws = transcreve(a)
    frases = [l for l in b["fala"].split("\n") if l.strip()]
    fw = [(k, w) for k, fr in enumerate(frases) for w in n(fr)]           # palavras do roteiro com o índice da frase
    cw = [(i, x) for i, w in enumerate(ws) for x in n(w["w"])]             # palavras do Whisper (com o índice da palavra)
    sm = difflib.SequenceMatcher(None, [w for _, w in fw], [x for _, x in cw], autojunk=False)
    mapa = {}
    for blk in sm.get_matching_blocks():
        for j in range(blk.size): mapa[blk.a + j] = cw[blk.b + j][0]
    # semelhança com números normalizados (o Whisper escreve "250 km", o roteiro "duzentos e cinquenta quilômetros")
    r = difflib.SequenceMatcher(None, nn(b["fala"]), nn(" ".join(w["w"] for w in ws)), autojunk=False).ratio()
    dur = len(a) / SR
    fr_t = []
    for k in range(len(frases)):
        idx = [mapa[i] for i, (kk, _) in enumerate(fw) if kk == k and i in mapa]
        if idx: fr_t.append([ws[min(idx)]["s"], ws[max(idx)]["e"]])
        else: fr_t.append(None)
    for k in range(len(frases)):                                         # frase sem casamento: interpola
        if fr_t[k] is None:
            s0 = fr_t[k - 1][1] if k and fr_t[k - 1] else 0.0
            s1 = next((fr_t[j][0] for j in range(k + 1, len(frases)) if fr_t[j]), dur)
            fr_t[k] = [s0, s1]
    fr_t[0][0] = 0.0; fr_t[-1][1] = dur
    tb = {"id": b["id"], "s": round(t, 3), "e": round(t + dur, 3), "atempo": atempo(b["id"]),
          "frases": [{"s": round(t + s0, 3), "e": round(t + s1, 3), "txt": fr} for (s0, s1), fr in zip(fr_t, frases)]}
    for w in ws: whisper.append({**w, "s": round(w["s"] + t, 3), "e": round(w["e"] + t, 3)})
    tag = [w["w"] for w in ws if n(w["w"]) and n(w["w"])[0] in TAGS]
    perg = [fr for fr in frases if fr.rstrip().endswith("?")]
    txt_wh = " ".join(w["w"] for w in ws)
    rel.append(f"{b['id']} x{atempo(b['id'])} {dur:5.1f}s ratio={r:.3f} tags_faladas={tag} perguntas={len(perg)} '?' no whisper={txt_wh.count('?')}\n  ROTEIRO: {b['fala'].replace(chr(10), ' / ')}\n  WHISPER: {txt_wh}")
    if r < 0.95 or tag: ruins.append((b["id"], round(r, 3), tag))
    partes.append(a); t += dur; tempos.append(tb)
    if bi < len(blocos) - 1:
        prox = blocos[bi + 1]
        g = GAP_BLOCO[b["marcha"]] if prox["cap"] == b["cap"] or prox["cap"].split(" ·")[0] == b["cap"].split(" ·")[0] else GAP_CAP
        partes.append(np.zeros(int(SR * g), np.float32)); t += g
    print(b["id"], f"{r:.3f}", tag or "", flush=True)
partes.append(np.zeros(int(SR * FIM), np.float32))
audio = np.concatenate(partes)
subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", str(R / "audio/narracao.wav")], input=audio.astype(np.float32).tobytes(), check=True)
json.dump({"duracao": round(len(audio) / SR, 3), "blocos": tempos}, open(A / "tempos.json", "w"), ensure_ascii=False, indent=1)
json.dump(whisper, open(A / "whisper.json", "w"), ensure_ascii=False)
# palavras por minuto: hook (b01–b06), passagem (b07), resto (b08–b51); tempo de fala do bloco + pausas entre blocos do trecho
def ppm(ids):
    sel = [(b, tb) for b, tb in zip(blocos, tempos) if b["id"] in ids]
    pal = sum(len(re.findall(r"\w+", b["fala"])) for b, _ in sel)
    return pal, sel[-1][1]["e"] - sel[0][1]["s"], pal / (sel[-1][1]["e"] - sel[0][1]["s"]) * 60
ids = [b["id"] for b in blocos]
res = {"hook b01–b06": ppm(ids[:6]), "passagem b07": ppm(ids[6:7]), "resto b08–b51": ppm(ids[7:])}
media = sum(float(l.split("ratio=")[1].split()[0]) * len(n(b["fala"])) for l, b in zip(rel, blocos)) / sum(len(n(b["fala"])) for b in blocos)
cab = [f"duração {len(audio)/SR/60:.2f} min; fala termina em {tempos[-1]['e']:.1f}s; Whisper × roteiro ponderado {media:.3f}"] + \
      [f"{k}: {p} palavras em {s:.1f}s = {v:.0f} pal/min" for k, (p, s, v) in res.items()] + [f"abaixo de 0,95 ou com tag falada: {ruins}"]
open(R / "work/confere_voz_v2.txt", "w").write("\n".join(cab + rel))
print("\n".join(cab))
