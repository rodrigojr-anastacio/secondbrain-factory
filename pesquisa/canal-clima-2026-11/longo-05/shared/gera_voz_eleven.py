# longo 02 (09/11/2026; base: v2 do longo 01): narração ElevenLabs v3, voz "Fernanda", um request por bloco (fala_tts, com tags de emoção).
# Brutos em audio/eleven-brutos/<id>.mp3 (fora do git). Chave lida de ~/.segredos/elevenlabs/api_key (nunca impressa).
# Uso: gera_voz_eleven.py [--refaz] [ids...]   (sem ids = todos os que faltam)
import json, sys, time, urllib.request, urllib.error
from pathlib import Path
A = Path(__file__).parent; OUT = A.parent / "audio/eleven-brutos"; OUT.mkdir(parents=True, exist_ok=True)
VOZ, MODELO = "7iqXtOF3wl3pomwXFY7G", "eleven_v3"
KEY = (Path.home() / ".segredos/elevenlabs/api_key").read_text().strip()
args = sys.argv[1:]; refaz = "--refaz" in args; so = {a for a in args if not a.startswith("--")}

def req(url, body=None):
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    return urllib.request.urlopen(r, timeout=180)

def creditos():
    d = json.load(req("https://api.elevenlabs.io/v1/user/subscription"))
    return d["character_count"], d["character_limit"]

log = json.load(open(OUT / "log.json")) if (OUT / "log.json").exists() else {}
c0 = creditos(); print("créditos antes:", c0, flush=True)
for b in json.load(open(A / "blocos.json")):
    if so and b["id"] not in so: continue
    f = OUT / f"{b['id']}.mp3"
    if f.exists() and not refaz and not so: continue
    texto = " ".join(l.strip() for l in b["fala_tts"].split("\n") if l.strip())
    for tent in range(4):
        try:
            data = req(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}?output_format=mp3_44100_128",
                       {"text": texto, "model_id": MODELO, "voice_settings": {"stability": 0.0, "similarity_boost": 0.8}}).read()
            break
        except urllib.error.HTTPError as e:
            print(b["id"], "HTTP", e.code, e.read()[:300], flush=True); time.sleep(5 * (tent + 1))
    else:
        sys.exit(f"falhou {b['id']}")
    f.write_bytes(data)
    log.setdefault(b["id"], []).append({"chars": len(texto), "texto": texto, "quando": time.strftime("%H:%M:%S")})
    json.dump(log, open(OUT / "log.json", "w"), ensure_ascii=False, indent=1)
    print(b["id"], len(texto), "chars", flush=True)
c1 = creditos(); print("créditos depois:", c1, "usados nesta rodada:", c1[0] - c0[0], flush=True)
