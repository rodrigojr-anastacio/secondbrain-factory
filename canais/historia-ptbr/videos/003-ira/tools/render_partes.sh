#!/bin/bash
# Render em partes (cada comando < 10 min no harness headless): só vídeo, por faixa de frames; depois junta e põe o mix.
# Uso (pasta do vídeo): tools/render_partes.sh <inicio> <fim>   → out/partes/p<inicio>.mp4
#                       tools/render_partes.sh juntar            → out/video.mp4 (concat sem reencode + mix.wav em AAC)
set -e
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
mkdir -p out/partes
if [ "$1" = juntar ]; then
  ls out/partes/p*.mp4 | sort | sed 's/^/file /;s/file out\/partes\//file /' > out/partes/lista.txt
  ffmpeg -v error -y -f concat -safe 0 -i out/partes/lista.txt -i public/audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out/video.mp4
  echo JUNTAR_OK; exit 0
fi
npx remotion render src/index.jsx Ira out/partes/p$(printf %06d $1).mp4 --frames=$1-$2 --muted --codec=h264 --crf=20 --concurrency=2 --log=error
echo PARTE_OK $1-$2
