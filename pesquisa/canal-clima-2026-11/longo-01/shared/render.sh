#!/bin/bash
# Render do longo em partes de 500 quadros (< 10 min cada; um render por vez na VPS) + junção com o mix.
# Uso: shared/render.sh <parte N|junta>   (bundle em work/bundle; refazer com REBUNDLE=1)
set -e
cd "$(dirname "$0")/../remotion"
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
N=$(python3 -c "import json,math;c=json.load(open('../shared/cues.json'));print(math.ceil(c['duracao']*c['fps']))")
Q=500; NP=$(( (N + Q - 1) / Q ))
mkdir -p ../work/partes
[ -n "$REBUNDLE" ] && npx remotion bundle --out-dir=../work/bundle >/dev/null 2>&1
if [ "$1" = "junta" ]; then
  : > ../work/partes/lista.txt
  for i in $(seq 0 $((NP-1))); do printf "file 'p%02d.mp4'\n" $i >> ../work/partes/lista.txt; done
  ffmpeg -v error -y -f concat -safe 0 -i ../work/partes/lista.txt -i ../audio/mix.wav -map 0:v -map 1:a -c:v copy -af "acompressor=threshold=0.06:ratio=4:attack=4:release=120:makeup=2.5,alimiter=limit=0.89:level=false,loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -shortest -movflags +faststart ../out/video.mp4
  echo "ok out/video.mp4"; exit 0
fi
i=$1; a=$((i*Q)); b=$(( (i+1)*Q-1 )); [ $b -ge $N ] && b=$((N-1))
while pgrep -af "^node .*remotion (render|still)" >/dev/null; do sleep 20; done
s=$(date +%s)
npx remotion render ../work/bundle Longo ../work/partes/p$(printf %02d $i).mp4 --frames=$a-$b --gl=swangle --concurrency=2 --muted --crf=18 2>&1 | grep -E -i "error|exception" | head -5 || true
echo "parte $i ($a-$b de $NP partes): $(( $(date +%s) - s )) s" | tee -a ../work/render-tempos.txt
