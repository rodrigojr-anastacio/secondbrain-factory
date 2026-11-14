"""Primeiros ~75 s de um vídeo do YouTube: baixa só o trecho (via WARP) e transcreve com Whisper local.
(ffmpeg não passa pelo SOCKS: baixa o áudio inteiro de menor bitrate e corta.)
Uso: tools/.venv/bin/python -I pesquisa/gap-2026-11-14/scripts/hook60.py <VIDEO_ID> <saida.txt> [idioma] [segundos]
Grava também <saida>.thumb.jpg (maxres) e <saida>.json (n de segmentos, palavras, ritmo).
Trava global: só 1 transcrição por vez na VPS (2 vCPU)."""
import subprocess, sys, os, wave, json, tempfile, shutil, fcntl, urllib.request
import numpy as np
vid, out = sys.argv[1], sys.argv[2]
lang = sys.argv[3] if len(sys.argv) > 3 else None
secs = int(sys.argv[4]) if len(sys.argv) > 4 else 75
PROXY = "socks5://127.0.0.1:40000"
VENV = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin")
NODE = os.path.expanduser("~/.hermes/tools/node-26.12.1-linux-x64/bin/node")
base = os.environ.get("TMPDIR", os.path.expanduser("~/cache/tmp"))
os.makedirs(base, exist_ok=True)
lock = open(os.path.join(base, "gap-whisper.lock"), "w")
fcntl.flock(lock, fcntl.LOCK_EX)
tmp = tempfile.mkdtemp(dir=base)
try:
    subprocess.run([f"{VENV}/yt-dlp", "-q", "--no-warnings", "--proxy", PROXY, "--js-runtimes", f"node:{NODE}",
                    "-f", "wa/ba/b", "-o", f"{tmp}/a.%(ext)s",
                    f"https://www.youtube.com/watch?v={vid}"], check=True, timeout=600)
    src = [f for f in os.listdir(tmp) if f.startswith("a.")][0]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{tmp}/{src}", "-t", str(secs), "-ac", "1", "-ar", "16000", f"{tmp}/a.wav"], check=True)
    w = wave.open(f"{tmp}/a.wav"); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)
    segs, info = m.transcribe(a, language=lang, vad_filter=True)
    segs = list(segs)
    lines = [f"[{int(s.start)//60}:{int(s.start)%60:02d}] {s.text.strip()}" for s in segs]
    open(out, "w").write("\n".join(lines) + "\n")
    words = sum(len(s.text.split()) for s in segs)
    json.dump({"id": vid, "segundos": secs, "segmentos": len(segs), "palavras": words,
               "palavras_por_min": round(words / (secs / 60), 1)}, open(out + ".json", "w"))
    print(len(lines), "segmentos;", words, "palavras")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
    fcntl.flock(lock, fcntl.LOCK_UN)
try:
    op = urllib.request.build_opener()
    for q in ("maxresdefault", "hqdefault"):
        try:
            data = op.open(f"https://i.ytimg.com/vi/{vid}/{q}.jpg", timeout=30).read()
            open(out + ".thumb.jpg", "wb").write(data); break
        except Exception:
            pass
except Exception:
    pass
