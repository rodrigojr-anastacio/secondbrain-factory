"""Duração, pal/min e Whisper (small, pt) de cada bruto contra o texto. Grava qa.json."""
import json, os, re, subprocess, sys, difflib, unicodedata
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from gerar import TEXTOS, VOZES  # noqa
from faster_whisper import WhisperModel
sys.path.insert(0, os.path.join(AQUI, "../videos/005-enchente-porto-alegre-2024/shared"))
import normaliza_pt
def norm(s):
    s = unicodedata.normalize("NFKD", s.lower()); s = "".join(c for c in s if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", s)
def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout)
import numpy as np
def pcm(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True,check=True).stdout
    return np.frombuffer(raw,dtype=np.float32)
m = WhisperModel("small", device="cpu", compute_type="int8")
out = json.load(open(os.path.join(AQUI,"qa.json"))) if os.path.exists(os.path.join(AQUI,"qa.json")) else {}
for L in (sys.argv[1:] or VOZES):
    r = {}
    for parte, txt in TEXTOS.items():
        p = os.path.join(AQUI, "brutos", f"{L}-{parte}.mp3")
        segs, _ = m.transcribe(pcm(p), language="pt")
        t = " ".join(s.text for s in segs)
        a, b = normaliza_pt.norm(txt), normaliza_pt.norm(t)
        r[parte] = {"dur": round(dur(p),2), "ppm": round(len(txt.split())/dur(p)*60), "whisper": round(difflib.SequenceMatcher(None,a,b).ratio(),3),
                    "perg": t.count("?"), "texto": t.strip()}
    out[L] = r
    print(L, {k:(v["dur"],v["ppm"],v["whisper"],v["perg"]) for k,v in r.items()}, flush=True)
json.dump(out, open(os.path.join(AQUI,"qa.json"),"w"), ensure_ascii=False, indent=1)
