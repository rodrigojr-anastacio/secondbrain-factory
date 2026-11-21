"""Whisper bloco a bloco: audio/<id>.mp3 × texto do blocos.json (001-midway, 12/11/2026).
Uso: tools/.venv/bin/python tools/compara_voz.py [ids...]   (da pasta do vídeo)
Grava qa/whisper.json (transcrição, % e palavras com tempo) e imprime a % por bloco; < 93% = revisar."""
import difflib, json, os, re, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

V = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
D = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def ext(n):
    if n < 20: return U[n]
    if n < 100: return D[n // 10] + ("" if n % 10 == 0 else " " + U[n % 10])
    if n < 1000: return U[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + ext(n % 100))
    for v, nome in ((10**9, "billion"), (10**6, "million"), (1000, "thousand")):
        if n >= v: return ext(n // v) + " " + nome + ("" if n % v == 0 else " " + ext(n % v))


def ano(n):
    if 1100 <= n <= 2099 and n % 1000 >= 10 and not (2000 <= n <= 2009):
        a, b = divmod(n, 100)
        return ext(a) + " " + ("hundred" if b == 0 else ("oh " + U[b] if b < 10 else ext(b)))
    return ext(n)


def norm(t):
    t = t.lower().replace("*", "").replace("’", "'")
    t = re.sub(r"(\d),(\d{3})", r"\1\2", t)
    t = re.sub(r"(\d+)\.(\d+)", lambda m: m.group(1) + " point " + " ".join(U[int(c)] for c in m.group(2)), t)
    t = re.sub(r"(\d+)(st|nd|rd|th)\b", r"\1", t)
    t = re.sub(r"\$(\d+)", r"\1 dollars", t)
    t = re.sub(r"\d+", lambda m: ano(int(m.group())) if len(m.group()) == 4 else ext(int(m.group())), t)
    t = t.replace(" and ", " ").replace("-", " ").replace("percent", "%")
    for a, b in [("ah kah gee", "akagi"), ("fourth", "four"), ("first", "one"), ("sixth", "six"), ("eleventh", "eleven"),
                 ("thirteenth", "thirteen"), ("thirty first", "thirty one"), ("twenty fourth", "twenty four"), ("seventh", "seven")]:
        t = t.replace(a, b)
    return [w for w in re.findall(r"[a-z0-9']+", t) if w not in ("and", "the", "a", "uh")]


def main():
    blocos = json.load(open(f"{V}/blocos.json"))
    so = set(sys.argv[1:])
    out_p = f"{V}/qa/whisper.json"
    os.makedirs(f"{V}/qa", exist_ok=True)
    res = json.load(open(out_p)) if os.path.exists(out_p) else {}
    m = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=2)
    for b in blocos:
        if so and b["id"] not in so: continue
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{V}/audio/{b['id']}.mp3", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                             capture_output=True, check=True).stdout
        segs, _ = m.transcribe(np.frombuffer(raw, dtype=np.float32), language="en", beam_size=5, word_timestamps=True,
                              condition_on_previous_text=False, vad_filter=True)
        segs = list(segs)
        tr = " ".join(s.text.strip() for s in segs)
        palavras = [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for s in segs for w in s.words]
        r = difflib.SequenceMatcher(None, norm(b["texto"]), norm(tr)).ratio() * 100
        res[b["id"]] = dict(pct=round(r, 1), dur=round(len(raw) / 4 / 16000, 2), transcricao=tr, palavras=palavras)
        print(f"{b['id']} {r:5.1f}% {'  <<< REVISAR' if r < 93 else ''}", flush=True)
        json.dump(res, open(out_p, "w"), ensure_ascii=False, indent=0)
    ps = [v["pct"] for v in res.values()]
    tot = sum(v["dur"] for v in res.values())
    print(f"blocos {len(ps)} · mín {min(ps):.1f}% · média {sum(ps)/len(ps):.1f}% · áudio {tot/60:.1f} min")


if __name__ == "__main__":
    main()
