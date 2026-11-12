"""Amostras de voz do hook B01 do piloto Midway (id 30). Uso: tools/.venv/bin/python gerar.py
Fish por frase (A, B) + bloco (extras); ElevenLabs Brian (C). Mede cobranca do Fish e registra custo."""
import json, os, subprocess, sys, time, urllib.request
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
import tts_fish as T
from db import tentar
AQUI = os.path.dirname(os.path.abspath(__file__))
VID = 30
TEXTO = ('This page was typed in June 1942, and somebody stamped it SECRET. It\'s Admiral Chester Nimitz\'s report to Washington on a battle three weeks old. '
         'Read line A. "Four C-V sunk. Akagi, Kaga, Soryu, Hiryu. With the loss of all their planes and many of their personnel." '
         'Four Japanese aircraft carriers, gone. Now do the math at the bottom. "Ninety-two officers and two hundred and fifteen men." The American cost. '
         'Three hundred and seven. Remember that number. The subject line reads: Battle of Midway. That place is still out there, in the middle of the Pacific. And you\'re not allowed to go.')
FISH = {"adrian": "bf322df2096a46f18c579d0baa36f41d", "ethan": "536d3a5e000945adb7038665781a4aca"}
MODELO = "s2.1-pro"

def norm(src, dst):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-af", "loudnorm=I=-16:TP=-1.5:LRA=7", "-ar", "44100", "-b:a", "192k", dst], check=True)

def fish(nome, voz, modo):
    key = T.chave(); tmp = f"{AQUI}/tmp"; os.makedirs(tmp, exist_ok=True)
    if modo == "frase":
        partes, nbytes = [], 0
        for i, f in enumerate(T.frases(TEXTO)):
            p = f"{tmp}/{nome}-{i}.mp3"
            T.gerar(key, voz, MODELO, None, f, p); nbytes += len(f.encode()); partes.append(T.ler(p))
        T.juntar(partes, 0.32, f"{tmp}/{nome}-{modo}.mp3")
    else:
        T.gerar(key, voz, MODELO, None, TEXTO, f"{tmp}/{nome}-{modo}.mp3"); nbytes = len(TEXTO.encode())
    return nbytes

def eleven():
    k = open(os.path.expanduser("~/.segredos/elevenlabs/api_key")).read().strip()
    corpo = {"text": TEXTO, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0, "speed": 0.95}}
    req = urllib.request.Request("https://api.elevenlabs.io/v1/text-to-speech/nPczCjzI2devNBz1zQrb?output_format=mp3_44100_128",
        data=json.dumps(corpo).encode(), headers={"xi-api-key": k, "Content-Type": "application/json"}, method="POST")
    os.makedirs(f"{AQUI}/tmp", exist_ok=True)
    open(f"{AQUI}/tmp/brian.mp3", "wb").write(urllib.request.urlopen(req, timeout=300).read())
    return len(TEXTO)

if __name__ == "__main__":
    key = T.chave(); c0 = T.credito(key); total = 0
    try:
        for nome, voz in FISH.items():
            for modo in ("frase", "bloco"):
                total += fish(nome, voz, modo)
    finally:
        T.registrar_custo(type("A", (), {"canal": "lugares-guerra-en", "video": VID, "entrada": "voz-amostras/hook-B01 (Adrian, Ethan; frase+bloco)"})(), MODELO, total)
    nch = eleven()
    def reg(con):
        con.execute("INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, ref_tipo, ref_id, notas)"
                    " VALUES ('youtube','lugares-guerra-en','ElevenLabs','tts eleven_multilingual_v2 amostra Brian (Midway hook)',%s,'caracteres',0,'USD',0,'youtube.video',%s,%s)",
                    (nch, VID, "amostra de voz; custo 0 pela assinatura Starter (lançamento 51); consome do contador do plano"))
    tentar(reg)
    time.sleep(8); print("credito fish antes/depois", c0, T.credito(key), "bytes", total)
    for src, dst in [("adrian-frase", "A-fish-adrian"), ("ethan-frase", "B-fish-ethan"), ("brian", "C-elevenlabs-brian"),
                     ("adrian-bloco", "extra-fish-adrian-bloco"), ("ethan-bloco", "extra-fish-ethan-bloco")]:
        norm(f"{AQUI}/tmp/{src}.mp3", f"{AQUI}/{dst}.mp3")
