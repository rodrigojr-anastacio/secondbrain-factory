import re, subprocess, glob, os, difflib, json
import numpy as np
from faster_whisper import WhisperModel
A = os.path.dirname(os.path.abspath(__file__))
TEXTO = re.search(r"TEXTO = \((.*?)\)\nFISH", open(f"{A}/gerar.py").read(), re.S).group(1)
TEXTO = eval("(" + TEXTO + ")")
def n(t):
    t = t.lower().replace("c-v", "cv").replace("c.v.", "cv").replace("sōryū", "soryu")
    for a,b in [("92","ninety two"),("215","two hundred and fifteen"),("307","three hundred and seven"),("cvs","cv")]:
        t = re.sub(r"\b"+a+r"\b", b, t)
    t = re.sub(r"ah[ -]?kah[ -]?gee|akagi|a kagi|akaki", "akagi", t)
    return re.findall(r"[a-z0-9']+", t.replace("-", " "))
ref = n(TEXTO); nw = len(TEXTO.split())
m = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=2)
for f in sorted(glob.glob(f"{A}/*.mp3")):
    raw = subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True,check=True).stdout
    segs,_ = m.transcribe(np.frombuffer(raw,dtype=np.float32), language="en", beam_size=5)
    tr = " ".join(s.text.strip() for s in segs); h = n(tr)
    r = difflib.SequenceMatcher(None, ref, h).ratio()
    dur = len(raw)/4/16000
    lu = subprocess.run(["ffmpeg","-i",f,"-af","loudnorm=print_format=json","-f","null","-"],capture_output=True,text=True).stderr
    li = json.loads(lu[lu.rindex("{"):lu.rindex("}")+1])["input_i"]
    print(f"{os.path.basename(f)} | dur {dur:.1f}s | ppm {nw/dur*60:.0f} | whisper {r*100:.1f}% | LUFS {li}\n  {tr}")
