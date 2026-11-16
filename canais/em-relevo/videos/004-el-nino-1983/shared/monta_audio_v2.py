# Longo 02 (09/11/2026; base: monta_audio_v2 do longo 01): junta a narração -> audio/narracao.wav + shared/tempos.json + shared/whisper.json.
# VOZ=eleven (padrão; audio/eleven-brutos/<id>.mp3) ou VOZ=kokoro (provisória; audio/kokoro-brutos/<id>.wav, sem atempo).
# Velocidade ElevenLabs (v3 não tem parâmetro): atempo. Hook b01–b06 1,36×; resto 1,1× (nesta geração a Fernanda veio mais rápida: com 1,4/1,2 dava 178/190 pal/min; alvo ~173 nos dois, pendência 1 do QA-v2 do vídeo 1).
# SLOT [ATUALIZAR 12/11]: os blocos com "atualizar" (b19–b21) ocupam uma janela de duração FIXA (shared/slot.json, gravado na 1ª
# montagem com ElevenLabs = fala + 1,5 s de folga). Em 12/11, a voz nova é encaixada na mesma janela (silêncio no fim ou atempo extra
# se passar), então tudo depois do slot fica com os mesmos tempos e só as partes de render do slot precisam ser refeitas.
# Cada bloco é transcrito sozinho (faster-whisper small) para: tempos por palavra, início/fim de cada frase, conferência ≥ 95% e tag falada.
# Saída da conferência: work/confere_voz_v2.txt. Uso: monta_audio_v2.py
import json, re, subprocess, unicodedata, difflib, numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
from normaliza_pt import norm as nn
import os
A = Path(__file__).parent; R = A.parent; SR = 44100
VOZ = os.environ.get("VOZ", "eleven")
BR = R / ("audio/eleven-brutos" if VOZ == "eleven" else "audio/kokoro-brutos"); EXT = ".mp3" if VOZ == "eleven" else ".wav"
EXTRA = {}   # atempo extra por bloco (encaixe no slot)
def atempo(bid):
    if VOZ != "eleven": return round(1.0 * EXTRA.get(bid, 1.0), 4)
    n = int(bid[1:]); return round((1.36 if n <= 6 else 1.1) * EXTRA.get(bid, 1.0), 4)
GAP_BLOCO = {1: 0.42, 1.5: 0.6, 2: 0.7}
GAP_CAP = 1.35
INICIO, FIM = 0.15, 2.5
TAGS = {"serious", "curious", "intrigued", "serio", "curioso", "intrigado"}

def n(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", " ", s).split()
def carrega(bid):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "quiet", "-i", str(BR / f"{bid}{EXT}"), "-af", f"atempo={atempo(bid)}", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
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
SLOT_IDS = [b["id"] for b in blocos if b.get("atualizar")]
SLOTF = A / "slot.json"; slot_fix = json.load(open(SLOTF))["dur"] if SLOTF.exists() else None
GAP_SLOT = GAP_BLOCO[2]
cache = {}
def bloco_audio(bid):
    if bid not in cache: cache[bid] = apara(carrega(bid))
    return cache[bid]
if SLOT_IDS and slot_fix:   # encaixe: se a fala do slot passar da janela (−0,4 s), acelera os blocos do slot por igual
    fala = sum(len(bloco_audio(i)) / SR for i in SLOT_IDS) + GAP_SLOT * (len(SLOT_IDS) - 1)
    if fala > slot_fix - 0.4:
        k = fala / (slot_fix - 0.4)
        for i in SLOT_IDS: EXTRA[i] = k; cache.pop(i, None)
        print(f"slot: fala {fala:.2f}s > janela {slot_fix:.2f}s; atempo extra {k:.3f}", flush=True)
partes = [np.zeros(int(SR * INICIO), np.float32)]; t = INICIO; tempos = []; whisper = []; rel = []; ruins = []; slot = None
for bi, b in enumerate(blocos):
    if SLOT_IDS and b["id"] == SLOT_IDS[0]: slot = {"s": round(t, 3), "ids": SLOT_IDS}
    a = bloco_audio(b["id"]); ws = transcreve(a)
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
    if SLOT_IDS and b["id"] == SLOT_IDS[-1]:   # fecha a janela fixa do slot
        usado = t - slot["s"]; alvo = slot_fix or round(usado + 1.5, 3)
        if VOZ == "eleven" and not slot_fix: json.dump({"dur": alvo, "ids": SLOT_IDS, "criado": "montagem ElevenLabs"}, open(SLOTF, "w"))
        pad = max(0.0, alvo - usado); partes.append(np.zeros(int(SR * pad), np.float32)); t += pad
        slot.update({"e": round(t, 3), "dur": round(alvo, 3), "fala": round(usado, 3)})
    if bi < len(blocos) - 1:
        prox = blocos[bi + 1]
        g = GAP_BLOCO[b["marcha"]] if prox["cap"] == b["cap"] or prox["cap"].split(" ·")[0] == b["cap"].split(" ·")[0] else GAP_CAP
        partes.append(np.zeros(int(SR * g), np.float32)); t += g
    print(b["id"], f"{r:.3f}", tag or "", flush=True)
partes.append(np.zeros(int(SR * FIM), np.float32))
audio = np.concatenate(partes)
subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", str(R / "audio/narracao.wav")], input=audio.astype(np.float32).tobytes(), check=True)
json.dump({"duracao": round(len(audio) / SR, 3), "voz": VOZ, "slot": slot, "blocos": tempos}, open(A / "tempos.json", "w"), ensure_ascii=False, indent=1)
json.dump(whisper, open(A / "whisper.json", "w"), ensure_ascii=False)
# palavras por minuto: hook (b01–b06), passagem (b07), resto (b08–b51); tempo de fala do bloco + pausas entre blocos do trecho
def ppm(ids):
    sel = [(b, tb) for b, tb in zip(blocos, tempos) if b["id"] in ids]
    pal = sum(len(re.findall(r"\w+", b["fala"])) for b, _ in sel)
    return pal, sel[-1][1]["e"] - sel[0][1]["s"], pal / (sel[-1][1]["e"] - sel[0][1]["s"]) * 60
ids = [b["id"] for b in blocos]
res = {"hook b01–b07": ppm(ids[:7]), "passagem b07": ppm(ids[7:8]), "resto b08–b48": ppm(ids[8:])}
media = sum(float(l.split("ratio=")[1].split()[0]) * len(n(b["fala"])) for l, b in zip(rel, blocos)) / sum(len(n(b["fala"])) for b in blocos)
cab = [f"voz {VOZ}; slot {slot}", f"duração {len(audio)/SR/60:.2f} min; fala termina em {tempos[-1]['e']:.1f}s; Whisper × roteiro ponderado {media:.3f}"] + \
      [f"{k}: {p} palavras em {s:.1f}s = {v:.0f} pal/min" for k, (p, s, v) in res.items()] + [f"abaixo de 0,95 ou com tag falada: {ruins}"]
open(R / f"work/confere_voz_{VOZ}.txt", "w").write("\n".join(cab + rel))
print("\n".join(cab))
