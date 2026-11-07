"""Métricas de texto das transcrições e dos nossos SCRIPT.md: ppm, palavras/frase, perguntas/min, 'you/você' por 100 palavras, marcadores de virada."""
import re, sys, glob, os
D = os.path.dirname(os.path.abspath(__file__))
VIR = {"en": r"\b(but|then|so|which means|because|and then|here's|here is|turns out|problem)\b", "pt": r"\b(mas|então|só que|porque|aí|e aí|acontece que|o problema)\b"}
YOU = {"en": r"\b(you|your|you're|you've)\b", "pt": r"\b(você|vocês|seu|sua|imagine|pense)\b"}
def stats(txt, dur_min, lang):
    body = re.sub(r"^\[\d+:\d+\]\s*", "", txt, flags=re.M); body = re.sub(r"^#.*$", "", body, flags=re.M)
    w = body.split(); sents = [s for s in re.split(r"[.!?]+\s", body) if s.strip()]
    q = body.count("?"); low = body.lower()
    return dict(pal=len(w), ppm=len(w)/dur_min, ppf=len(w)/max(1,len(sents)), perg_min=q/dur_min,
                you100=100*len(re.findall(YOU[lang], low))/len(w), vir100=100*len(re.findall(VIR[lang], low))/len(w))
rows = []
for f in sorted(glob.glob(f"{D}/transcricoes/*.txt")):
    t = open(f).read(); m = re.search(r"duração: (\d+):(\d+)", t); dur = int(m[1]) + int(m[2])/60
    lang = "pt" if "Whisper small, pt" in t else "en"; v = re.search(r"views: (\d+)", t)[1]
    rows.append((os.path.basename(f)[:-4], int(v), dur, stats(t, dur, lang)))
for nome, dur, p in [("NOSSO 001-egito", 17.0, "001-egito"), ("NOSSO 002-india", 19.45, "002-india"), ("NOSSO 003-ira", 18.0, "003-ira"), ("NOSSO 004-china", 16.23, "004-china")]:
    t = open(os.path.expanduser(f"~/workspace/fabrica-youtube/canais/historia-ptbr/videos/{p}/SCRIPT.md")).read()
    t = re.sub(r"^(#|>|\||---).*$", "", t, flags=re.M); t = re.sub(r"\[[^\]]*\]|\*\*|`|<[^>]*>", "", t)
    rows.append((nome, 0, dur, stats(t, dur, "pt")))
print(f"{'video':42} {'views':>9} {'min':>5} {'pal':>5} {'ppm':>4} {'p/fr':>5} {'?/min':>5} {'voce%':>5} {'vir%':>5}")
for n, v, d, s in rows:
    print(f"{n:42} {v:>9} {d:5.1f} {s['pal']:>5} {s['ppm']:4.0f} {s['ppf']:5.1f} {s['perg_min']:5.2f} {s['you100']:5.2f} {s['vir100']:5.2f}")
