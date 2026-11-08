#!/bin/bash
# Render em partes (< 10 min cada; um render por vez na VPS) + mux da narração. Uso: shared/render.sh Shorts|Longo <saida.mp4> [parte]
set -e
cd "$(dirname "$0")/../remotion"
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
COMP=$1; OUT=$2; SO=$3
N=$(python3 -c "import json,math;c=json.load(open('../shared/cues.json'));print(math.ceil(c['duracao']*c['fps']))")
mkdir -p ../work/partes
PARTES=("0-599" "600-1199" "1200-$((N-1))")
for i in 0 1 2; do
  [ -n "$SO" ] && [ "$SO" != "$i" ] && continue
  while pgrep -af "^node .*remotion (render|still)" >/dev/null; do sleep 20; done
  s=$(date +%s)
  npx remotion render $COMP ../work/partes/$COMP-$i.mp4 --frames=${PARTES[$i]} --gl=swangle --concurrency=2 --muted --crf=18 2>&1 | tail -1
  echo "$COMP parte $i (${PARTES[$i]}): $(( $(date +%s) - s )) s" | tee -a ../work/render-tempos.txt
done
if [ -z "$SO" ] || [ "$SO" = "junta" ]; then
  printf "file '%s'\n" $COMP-0.mp4 $COMP-1.mp4 $COMP-2.mp4 > ../work/partes/$COMP.txt
  ffmpeg -v error -y -f concat -safe 0 -i ../work/partes/$COMP.txt -i ../audio/mix.wav -map 0:v -map 1:a -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -shortest -movflags +faststart "../$OUT"
  echo "ok $OUT"
fi
