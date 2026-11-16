# VOZ PROVISÓRIA (09/11/2026): a chave da ElevenLabs deu 401 (ver ../BLOQUEIO.md). Kokoro pf_dora (local, grátis), um wav por bloco
# em audio/kokoro-brutos/<id>.wav (frases juntadas com 0,35 s). Só serve para montar/testar a edição; a final é ElevenLabs v3 "Fernanda".
import json, sys, numpy as np, soundfile as sf
from pathlib import Path
from kokoro import KPipeline
A = Path(__file__).parent; out = A.parent / "audio/kokoro-brutos"; out.mkdir(parents=True, exist_ok=True)
so = set(sys.argv[1:])
pipe = KPipeline(lang_code="p", repo_id="hexgrad/Kokoro-82M")
for b in json.load(open(A / "blocos.json")):
    if so and b["id"] not in so: continue
    partes = []
    for frase in (l for l in b["fala"].split("\n") if l.strip()):
        partes.append(np.concatenate([x for _, _, x in pipe(frase, voice="pf_dora", speed=1.12 if b["marcha"] == 1 else 1.02, split_pattern=None)]))
        partes.append(np.zeros(int(24000 * 0.35), np.float32))
    sf.write(out / f"{b['id']}.wav", np.concatenate(partes[:-1]), 24000)
    print(b["id"], flush=True)
