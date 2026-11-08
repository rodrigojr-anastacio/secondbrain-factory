# Narração Kokoro pf_dora (grátis), uma frase por arquivo: work/voz/<bloco>-<k>.wav.
# Velocidade por marcha (Rodrigo): 1 = igual ao piloto (1,1; o atempo 1,05 entra no monta_audio), 1.5 = transição, 2 = mais calma.
# Uso: gera_voz.py [ids...]  (sem ids = todos)
import json, sys, numpy as np, soundfile as sf
from pathlib import Path
from kokoro import KPipeline
A = Path(__file__).parent; out = A.parent / "work/voz"; out.mkdir(parents=True, exist_ok=True)
VEL = {1: 1.1, 1.5: 1.02, 2: 0.88}
so = set(sys.argv[1:])
pipe = KPipeline(lang_code="p", repo_id="hexgrad/Kokoro-82M")
for b in json.load(open(A / "blocos.json")):
    if so and b["id"] not in so: continue
    for k, frase in enumerate(l for l in b["fala"].split("\n") if l.strip()):
        a = np.concatenate([x for _, _, x in pipe(frase, voice="pf_dora", speed=VEL[b["marcha"]], split_pattern=None)])
        sf.write(out / f"{b['id']}-{k}.wav", a, 24000)
    print(b["id"], flush=True)
