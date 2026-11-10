#!/bin/bash
# Mede s/quadro do render 1080p (mesmos parâmetros do shared/render.sh: swangle, concurrency 2) para o mapa atual e os estilos v2.
# Uso: mede_tempo.sh <quadro_inicial> <n_quadros> <estilos...>   (estilo "-" = mapa atual)   -> anexa em visual-v2/tempos.txt
cd "$(dirname "$0")/../../remotion"
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
A=$1; N=$2; shift 2; B=$((A + N - 1))
for E in "$@"; do
  while pgrep -af "^node .*remotion (render|still)" >/dev/null; do sleep 15; done
  if [ "$E" = "-" ]; then PROPS='{"estilo":null,"fotos":"grande"}'; else PROPS="{\"estilo\":\"$E\",\"fotos\":\"grande\",\"perf\":${PERF:-null}}"; fi
  s=$(date +%s.%N)
  npx remotion render ../work/bundle-v2 LongoV2 ../work/v2/mede.mp4 --frames=$A-$B --gl=swangle --concurrency=2 --muted --crf=18 --props="$PROPS" --timeout=240000 2>&1 | grep -E -i "error|exception" | head -3
  d=$(python3 -c "import time;print(round(time.time()-$s,1))")
  echo "estilo=$E perf=${PERF:-} quadros=$A-$B total=${d}s s/quadro=$(python3 -c "print(round($d/$N,3))")" | tee -a ../visual-v2/tempos.txt
done
