#!/bin/bash
# uso: tools/render_parte.sh N A B  (Runpod, parte N dos quadros A-B, mudo)
V=~/workspace/fabrica-youtube/canais/historia-ptbr/videos/009-alemanha
cd ~/workspace/fabrica-youtube
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH TMPDIR=$HOME/cache/tmp
VIDEO=37 PROJETO=historia-ptbr MUDO=1 ENTRY=src/index.jsx BUNDLE=$HOME/cache/009-alemanha/bundle REFS=$V/qa/refs \
  tools/render_runpod_local009.sh $V Alemanha $V/out/partes/p$1.mp4 $2-$3
