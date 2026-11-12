"""Rodada 4 (12/11/2026): candidatas O-T (+ reservas) da biblioteca Fish, hook B01 (Ah-kah-gee), s2.1-pro, por frase + 0,32 s.
Uso: tools/.venv/bin/python gerar4.py"""
import os, sys, time
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
import tts_fish as T
import gerar as G
TEXTO = G.TEXTO.replace("Akagi,", "Ah-kah-gee,")
VOZES = [("cand-narrator-maxn", "0327fdb5da9e4fd782899a8058c8ae2b"), ("cand-wnba-voiceover", "fb7ec16ca51a45a5a4db881244d7990a"),
         ("cand-atomic", "4c6a6762e4ac4bdebdb4fa8525d054a2"), ("cand-bii2", "9d1efa1645a34f219cfb0ac605960a14"),
         ("cand-jjk", "d6777f507ab84be0b6d8889b6d53d7fc"), ("cand-w2w", "4746f1b456494387993af9041d0516c4"),
         ("cand-heisty", "3054685dbece41229c5bb5efa05e77cb"), ("cand-news-reporter", "05aff7ff557d45d2ace9a639452451ea")]
if __name__ == "__main__":
    key = T.chave(); c0 = T.credito(key); total = 0; tmp = f"{G.AQUI}/tmp"; os.makedirs(tmp, exist_ok=True)
    try:
        for arq, voz in VOZES:
            try:
                partes = []
                for i, f in enumerate(T.frases(TEXTO)):
                    p = f"{tmp}/{arq}-{i}.mp3"
                    T.gerar(key, voz, G.MODELO, None, f, p); total += len(f.encode()); partes.append(T.ler(p))
                T.juntar(partes, 0.32, f"{tmp}/{arq}.mp3")
                G.norm(f"{tmp}/{arq}.mp3", f"{G.AQUI}/{arq}.mp3"); print("ok", arq, flush=True)
            except Exception as e: print("ERRO", arq, e, flush=True)
    finally:
        T.registrar_custo(type("A", (), {"canal": "lugares-guerra-en", "video": G.VID, "entrada": "voz-amostras/hook-B01 rodada 4 (O-T, biblioteca Fish)"})(), G.MODELO, total)
    time.sleep(8); print("credito fish antes/depois", c0, T.credito(key), "bytes", total)
