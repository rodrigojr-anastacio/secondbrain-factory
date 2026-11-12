"""Amostras D-H (12/11/2026): mais 5 vozes ElevenLabs no hook B01, Akagi em grafia fonetica. Uso: tools/.venv/bin/python gerar2.py"""
import json, os, sys, urllib.request
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from db import tentar
import gerar as G
TEXTO = G.TEXTO.replace("Akagi,", "Ah-kah-gee,")
assert "Ah-kah-gee" in TEXTO
VOZES = [("D-eleven-adam", "pNInz6obpgDQGcFmaJgB", "Adam"), ("E-eleven-bill", "pqHfZKP75CvOlQylNhV4", "Bill"),
         ("F-eleven-flint", "qAZH0aMXY8tw1QufPN0D", "Flint"), ("G-eleven-george-uk", "JBFqnCBsd6RMkjVDRZzb", "George"),
         ("H-eleven-daniel-uk", "onwK4e9ZLuTAKqWW03F9", "Daniel")]
def eleven(vid):
    k = open(os.path.expanduser("~/.segredos/elevenlabs/api_key")).read().strip()
    corpo = {"text": TEXTO, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0, "speed": 0.95}}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
        data=json.dumps(corpo).encode(), headers={"xi-api-key": k, "Content-Type": "application/json"}, method="POST")
    return urllib.request.urlopen(req, timeout=300).read()
if __name__ == "__main__":
    os.makedirs(f"{G.AQUI}/tmp", exist_ok=True)
    for arq, vid, nome in VOZES:
        open(f"{G.AQUI}/tmp/{arq}.mp3", "wb").write(eleven(vid))
        G.norm(f"{G.AQUI}/tmp/{arq}.mp3", f"{G.AQUI}/{arq}.mp3")
        def reg(con, nome=nome):
            con.execute("INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, ref_tipo, ref_id, notas)"
                        " VALUES ('youtube','lugares-guerra-en','ElevenLabs',%s,%s,'caracteres',0,'USD',0,'youtube.video',%s,%s)",
                        (f"tts eleven_multilingual_v2 amostra {nome} (Midway hook)", len(TEXTO), G.VID, "amostra de voz; custo 0 pela assinatura Starter; consome do contador do plano"))
        tentar(reg); print("ok", arq)
