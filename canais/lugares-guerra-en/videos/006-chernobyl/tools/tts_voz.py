"""TTS Fish com voz escolhida (para o TASS recriado, voz diferente da narração). Reusa tools/tts_fish.py e registra o custo."""
import sys, os, json, argparse
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
import tts_fish as T
ap = argparse.ArgumentParser(); ap.add_argument("entrada"); ap.add_argument("saida"); ap.add_argument("--voz", required=True)
ap.add_argument("--video", type=int); ap.add_argument("--modelo", default="s2.1-pro")
a = ap.parse_args(); a.canal = "lugares-guerra-en"
key = T.chave(); os.makedirs(a.saida, exist_ok=True); tot = 0
for bid, texto in T.blocos(a.entrada):
    p = os.path.join(a.saida, f"{bid}.mp3")
    if not os.path.exists(p):
        T.gerar(key, a.voz, a.modelo, None, texto, p); tot += len(texto.encode())
    print(bid, "ok", p)
if tot: T.registrar_custo(a, a.modelo, tot)
