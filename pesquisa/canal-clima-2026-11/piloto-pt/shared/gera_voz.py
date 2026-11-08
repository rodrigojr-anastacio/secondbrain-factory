# Narração Kokoro pt-BR por bloco (grátis). Uso: gera_voz.py <voz> <velocidade> <pasta_saida>
import json, sys, numpy as np, soundfile as sf
from pathlib import Path
from kokoro import KPipeline
voz, vel, out = sys.argv[1], float(sys.argv[2]), Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
pipe = KPipeline(lang_code="p", repo_id="hexgrad/Kokoro-82M")
for b in json.load(open(Path(__file__).parent / "blocos.json")):
    a = np.concatenate([x for _, _, x in pipe(b["fala"], voice=voz, speed=vel)])
    sf.write(out / f"{b['id']}.wav", a, 24000)
    print(b["id"], f"{len(a)/24000:.2f}s", flush=True)
