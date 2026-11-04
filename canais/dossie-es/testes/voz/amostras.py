"""Amostras curtas do hook em espanhol em várias vozes Fish (custo em financas.consumo, ref = vídeo 7).
Uso (a partir de tools/): .venv/bin/python ../canais/dossie-es/testes/voz/amostras.py"""
import os, sys, types
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
import tts_fish as tf
VOZES = {
    "dio-historias": "ac594943984a47e7a827416eb263c7b1",
    "marcus": "93dc4e3a1a494d58ad0f50f712b8b152",
    "arnold": "4a6a697943254f63ab3143877712ceed",
    "narrador-documental-latino": "c87656721dda48a7906f990f036ce76f",
    "voz-grave": "3a42f62c3af240438066d7e927414dea",
    "locutor-k": "3f45a7fd7a614655a61eb7027b955783",
    "natgeo-espana": "85398a2a5ec24078aae24829fb03425d",
}
base = os.path.dirname(os.path.abspath(__file__))
texto = open(os.path.join(base, "hook-es.txt")).read().strip()
key = tf.chave(); total = 0
for nome, vid in VOZES.items():
    dest = os.path.join(base, f"{nome}.mp3")
    if os.path.exists(dest):
        continue
    tf.gerar(key, vid, "s2.1-pro", 1.0, texto, dest)
    total += len(texto.encode()); print("ok", nome)
if total:
    tf.registrar_custo(types.SimpleNamespace(canal="dossie-es", video=7, entrada="testes/voz/hook-es.txt"), "s2.1-pro", total)
