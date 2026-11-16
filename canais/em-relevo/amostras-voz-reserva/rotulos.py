"""Rótulos falados do todas.mp3 com Kokoro pf_dora (local, grátis). Rodar com ~/tts/venv-kokoro/bin/python."""
import os, numpy as np, soundfile as sf
from kokoro import KPipeline
AQUI = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(AQUI, "brutos"), exist_ok=True)
pipe = KPipeline(lang_code="p", repo_id="hexgrad/Kokoro-82M")
for k, t in {"REF": "Referência: Fernanda, a voz atual.", **{L: f"Amostra {L}." for L in "ABCDEF"}}.items():
    a = np.concatenate([x for _, _, x in pipe(t, voice="pf_dora", speed=1)])
    sf.write(os.path.join(AQUI, "brutos", f"rotulo-{k}.wav"), a, 24000)
    print(k, len(a) / 24000)
