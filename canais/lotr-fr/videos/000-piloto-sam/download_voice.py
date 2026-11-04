import requests
from pathlib import Path
root=Path('/home/hermes/.hermes/cache/scratch/piper-models/fr_FR-siwis-medium'); root.mkdir(parents=True,exist_ok=True)
base='https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/'
for name in ['fr_FR-siwis-medium.onnx','fr_FR-siwis-medium.onnx.json','MODEL_CARD']:
 p=root/name
 with requests.get(base+name,stream=True,timeout=180) as r:
  r.raise_for_status()
  with p.open('wb') as f:
   for c in r.iter_content(1024*1024):
    if c:f.write(c)
 print(name,p.stat().st_size)
print((root/'MODEL_CARD').read_text())
