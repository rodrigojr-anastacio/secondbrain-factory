#!/bin/bash
# Pré-QA (VPS): bundle + 1 still por plano (70% do plano; DocGrifo com grifo também no fim) → preqa/stills/<quadro>.png + grades.
# Uso (na pasta do vídeo): bash tools/stills.sh [escala=0.5] [lista de quadros opcional]
set -e
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
ESC=${1:-0.5}
npx remotion bundle src/index.jsx --out-dir $HOME/cache/003-gettysburg/bundle --log=error >/dev/null
QS=${2:-$(python3 -c "
import json;t=json.load(open('src/timeline.json'))['planos'];q=[]
for p in t:
  q.append(p['from_']+int(p['dur']*0.7))
  if p['tipo']=='DocGrifo' and p.get('grifo'): q.append(p['from_']+p['dur']-4)
print(','.join(map(str,sorted(set(q)))))")}
rm -rf preqa/stills; mkdir -p preqa/stills
node ~/workspace/fabrica-youtube/tools/remotion_stills.cjs . $HOME/cache/003-gettysburg/bundle Video preqa/stills swangle $ESC $QS
~/workspace/fabrica-youtube/tools/.venv/bin/python tools/grade.py
