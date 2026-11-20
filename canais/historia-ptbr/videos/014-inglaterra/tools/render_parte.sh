#!/bin/bash
# uso: tools/render_parte.sh N A B  (Runpod, parte N dos quadros A-B, mudo)
V=~/workspace/fabrica-youtube/canais/historia-ptbr/videos/013-uniao-sovietica
cd ~/workspace/fabrica-youtube
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH TMPDIR=$HOME/cache/tmp
VIDEO=50 PROJETO=historia-ptbr MUDO=1 ENTRY=src/index.jsx BUNDLE=$HOME/cache/013-uniao-sovietica/bundle REFS=$V/qa/refs \
  tools/render_runpod.sh $V Urss $V/out/partes/p$1.mp4 $2-$3
