"""Rodada 3 (12/11/2026): amostras I-N, vozes da biblioteca do Fish no hook B01 (Akagi fonetico), s2.1-pro, por frase + 0,32 s.
Uso: tools/.venv/bin/python gerar3.py"""
import os, sys, time
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
import tts_fish as T
import gerar as G
TEXTO = G.TEXTO.replace("Akagi,", "Ah-kah-gee,")
assert "Ah-kah-gee" in TEXTO
VOZES = [("I-fish-calm-storyteller", "e686ae649ee44f219a108aacba206c1a"), ("J-fish-slax", "9032b5f2e2554b5a957ad655c052af16"),
         ("K-fish-documentary", "c3958f083c2d407982263c77cfa831e3"), ("L-fish-deep-godmode", "bb742915b1fa41b389a850b11efae0c8"),
         ("M-fish-f1-uk", "59b8d12e87724010a34190047391be4f"), ("N-fish-eldrin-uk", "6428df0a468d47409d97d61acbe10876")]
if __name__ == "__main__":
    key = T.chave(); c0 = T.credito(key); total = 0; tmp = f"{G.AQUI}/tmp"; os.makedirs(tmp, exist_ok=True)
    try:
        for arq, voz in VOZES:
            partes = []
            for i, f in enumerate(T.frases(TEXTO)):
                p = f"{tmp}/{arq}-{i}.mp3"
                T.gerar(key, voz, G.MODELO, None, f, p); total += len(f.encode()); partes.append(T.ler(p))
            T.juntar(partes, 0.32, f"{tmp}/{arq}.mp3")
            G.norm(f"{tmp}/{arq}.mp3", f"{G.AQUI}/{arq}.mp3"); print("ok", arq, flush=True)
    finally:
        T.registrar_custo(type("A", (), {"canal": "lugares-guerra-en", "video": G.VID, "entrada": "voz-amostras/hook-B01 rodada 3 (I-N, biblioteca Fish)"})(), G.MODELO, total)
    time.sleep(8); print("credito fish antes/depois", c0, T.credito(key), "bytes", total)
