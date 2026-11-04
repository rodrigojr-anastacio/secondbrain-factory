from pathlib import Path
import subprocess
ROOT=Path('/home/hermes/workspace/lotr-pilot')
text=' '.join((ROOT/'script_fr.txt').read_text().split())
model=Path('/home/hermes/.hermes/cache/scratch/piper-models/fr_FR-siwis-medium/fr_FR-siwis-medium.onnx')
config=model.with_suffix('.onnx.json')
out=ROOT/'public/assets/narration.wav'
cmd=['/home/hermes/.hermes/cache/scratch/piper-env/bin/piper','-m',str(model),'-c',str(config),'-f',str(out),'--length-scale','1.10','--sentence-silence','0.12']
r=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=180)
print('exit',r.returncode,'stdout',r.stdout[:500],'stderr',r.stderr[:1500])
if r.returncode: raise SystemExit(r.returncode)
print('audio',out.stat().st_size,'bytes','words',len(text.split()))
