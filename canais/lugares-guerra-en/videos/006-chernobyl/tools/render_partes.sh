#!/bin/bash
# Render do 006 em partes (Runpod), sequencial; pula parte que já tem mp4. Uso: tools/render_partes.sh (da raiz do repo)
cd ~/workspace/fabrica-youtube
V=$PWD/canais/lugares-guerra-en/videos/006-chernobyl
export TMPDIR=$HOME/cache/tmp PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
N=$(python3 -c "import json;print(json.load(open('$V/src/timeline.json'))['durationInFrames'])")
declare -a P=("0-7499" "7500-13099" "13100-18699" "18700-24299" "24300-$((N-1))")
for i in "${!P[@]}"; do
  n=$((i+1)); out=$V/out/parts/p$n.mp4
  [ -s "$out" ] && [ "$n" -le 1 ] && continue
  [ -s "$out" ] && continue
  for t in 1 2 3; do
    VIDEO=55 PROJETO=lugares-guerra-en MUDO=1 ENTRY=src/index.jsx REFS=$V/preqa/refs RFLAGS="--offthreadvideo-cache-size-in-bytes=1000000000" \
      tools/render_runpod.sh $V Video $out ${P[$i]} > $V/logs/render_p$n.log 2>&1 && break
    echo "parte $n tentativa $t falhou" >> $V/logs/render_partes.log
  done
  [ -s "$out" ] || { echo "parte $n FALHOU" >> $V/logs/render_partes.log; exit 1; }
  echo "parte $n ok $(date +%T)" >> $V/logs/render_partes.log
done
echo TODAS_OK >> $V/logs/render_partes.log
