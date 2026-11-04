import subprocess, sys, os, wave, json, numpy as np, tempfile, shutil
from faster_whisper import WhisperModel
vid, out = sys.argv[1], sys.argv[2]
tmp = tempfile.mkdtemp()
NODE = os.path.expanduser("~/.hermes/tools/node-26.12.1-linux-x64/bin/node")
subprocess.run([os.path.dirname(sys.executable)+"/yt-dlp","-q","--no-warnings","--proxy","socks5://127.0.0.1:40000","--js-runtimes",f"node:{NODE}","-f","ba/b","-x","--audio-format","mp3","-o",f"{tmp}/a.%(ext)s",f"https://www.youtube.com/watch?v={vid}"],check=True)
src = [f for f in os.listdir(tmp) if f.startswith("a.")][0]
subprocess.run(["ffmpeg","-v","error","-y","-i",f"{tmp}/{src}","-ac","1","-ar","16000",f"{tmp}/a.wav"],check=True)
w = wave.open(f"{tmp}/a.wav"); a = np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
m = WhisperModel("small", device="cpu", compute_type="int8")
segs,info = m.transcribe(a, language=(sys.argv[3] if len(sys.argv)>3 else None), vad_filter=True)
lines=[f"[{int(s.start)//60}:{int(s.start)%60:02d}] {s.text.strip()}" for s in segs]
open(out,"w").write("\n".join(lines)+"\n")
shutil.rmtree(tmp)
print(len(lines), "segmentos;", sum(len(l.split()) for l in lines), "palavras")
