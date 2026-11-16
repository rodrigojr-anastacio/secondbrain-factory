"""Monta as amostras finais: Fernanda recortada do 005 (referência) e cada voz Fish com o ritmo casado ao da Fernanda
(atempo = duração Fish ÷ duração Fernanda no mesmo trecho, limitado a 1,0–1,5; a Fernanda do 005 já tem atempo 1,36 no hook
e 1,1 no corpo). Hook + 0,8 s + transição; loudnorm −16 LUFS; mp3 mono 128k. Junta tudo em todas.mp3 com rótulos falados."""
import json, os, subprocess
AQUI = os.path.dirname(os.path.abspath(__file__))
NARR = os.path.join(AQUI, "../videos/005-enchente-porto-alegre-2024/audio/narracao.wav")
TMP = os.path.join(os.environ.get("TMPDIR", os.path.expanduser("~/cache/tmp")), "amostras-voz-reserva"); os.makedirs(TMP, exist_ok=True)
NOMES = {"A": "A-fish-energica-drama3", "B": "B-fish-documental-drama3", "C": "C-fish-natasha-drama3",
         "D": "D-fish-jovem-clara-drama3", "E": "E-fish-masculina-drama3", "F": "F-fish-natasha-s21pro"}
TRECHO = {"hook": (0.0, 45.75), "trans": (272.95, 281.70)}  # shared/tempos.json do 005: b01 0,15–b04 45,44; b20 273,15–281,39
def ff(*a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
APARA = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
SIL = os.path.join(TMP, "sil08.wav"); ff("-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "0.8", SIL)
def junta(partes, destino, mp3=True):
    lst = os.path.join(TMP, "lista.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in partes))
    ff("-f", "concat", "-safe", "0", "-i", lst, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "1", *(["-b:a", "128k"] if mp3 else []), destino)
info = {}
# referência
ref = []
for parte, (s, e) in TRECHO.items():
    p = os.path.join(TMP, f"REF-{parte}.wav"); ff("-ss", str(s), "-to", str(e), "-i", NARR, "-af", APARA, "-ar", "44100", "-ac", "1", p); ref.append(p)
alvo = {k: dur(p) for k, p in zip(TRECHO, ref)}
junta([ref[0], SIL, ref[1]], os.path.join(AQUI, "REF-fernanda-eleven-v3.mp3"))
info["REF"] = {"dur": {k: round(v, 2) for k, v in alvo.items()}}
for L, nome in NOMES.items():
    ps, fat = [], {}
    for parte in TRECHO:
        bruto = os.path.join(AQUI, "brutos", f"{L}-{parte}.mp3")
        a = os.path.join(TMP, f"{L}-{parte}-a.wav"); ff("-i", bruto, "-af", APARA, "-ar", "44100", "-ac", "1", a)
        f = min(1.5, max(1.0, dur(a) / alvo[parte])); fat[parte] = round(f, 3)
        b = os.path.join(TMP, f"{L}-{parte}-b.wav"); ff("-i", a, "-af", f"atempo={f:.4f}", b); ps.append(b)
    junta([ps[0], SIL, ps[1]], os.path.join(AQUI, f"{nome}.mp3"))
    info[L] = {"arquivo": f"{nome}.mp3", "atempo": fat, "dur_final": round(dur(os.path.join(AQUI, f"{nome}.mp3")), 1)}
# todas.mp3
seq = []
for k, arq in [("REF", "REF-fernanda-eleven-v3.mp3")] + [(L, f"{n}.mp3") for L, n in NOMES.items()]:
    r = os.path.join(TMP, f"rot-{k}.wav"); ff("-i", os.path.join(AQUI, "brutos", f"rotulo-{k}.wav"), "-ar", "44100", "-ac", "1", r)
    x = os.path.join(TMP, f"x-{k}.wav"); ff("-i", os.path.join(AQUI, arq), "-ar", "44100", "-ac", "1", x)
    seq += [r, SIL, x, SIL, SIL]
junta(seq, os.path.join(AQUI, "todas.mp3"))
info["todas_dur"] = round(dur(os.path.join(AQUI, "todas.mp3")), 1)
json.dump(info, open(os.path.join(AQUI, "monta.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps(info, ensure_ascii=False))
