#!/usr/bin/env python3
"""006-roma (de 005-brasil): escolhe a melhor tomada por bloco do hook (audio/ + qa/hook/takeN) pela menor repetição melódica nos 60 s iniciais (medir.melodia). Uso (pasta do vídeo): tools/.venv/bin/python tools/escolher_tomadas.py"""
import json, sys, random, subprocess, itertools
import numpy as np
sys.path.insert(0, "tools"); sys.path.insert(0, "../../../../tools")
from tts_fish import ler, aparar, SR
from medir import melodia
bl = json.load(open("blocos.json"))[:6]
caps = {p["bloco"] for p in json.load(open("storyboard.json"))["planos"] if "capítulo:" in p["nota"]}
src = {"a": "audio", "b": "qa/hook/take2", "c": "qa/hook/take3", "d": "qa/hook/take4"}
cache = {}
def get(t, i): 
    k=(t,i)
    if k not in cache: cache[k] = aparar(ler(f"{src[t]}/{bl[i]['id']}.mp3"), cauda=0.15)
    return cache[k]
def montar(combo):
    partes=[np.zeros(int(0.25*SR),dtype=np.float32)]
    for i,t in enumerate(combo):
        g = 0 if i==0 else 0.6 if bl[i].get("ideia") else 0.25   # gaps novos do 006
        partes += [np.zeros(int(g*SR),dtype=np.float32), get(t,i)]
    y=np.concatenate(partes)[:60*SR]
    subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","pipe:0","/tmp/c.wav"],input=y.astype(np.float32).tobytes(),check=True)
    return melodia("/tmp/c.wav")["repeticao_melodica"]
random.seed(1)
res=[]
combos={tuple(random.choice("abcd") for _ in range(6)) for _ in range(200)} | {tuple(x*6) for x in "abcd"}
for c in combos:
    r=montar(c); res.append((r,"".join(c)))
res.sort(); print(res[:8]); print("todos a/b/c:", [x for x in res if len(set(x[1]))==1])
