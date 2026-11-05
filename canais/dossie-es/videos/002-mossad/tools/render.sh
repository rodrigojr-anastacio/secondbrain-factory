#!/bin/bash
# Render em partes (cada chamada < 10 min, regra headless: nada em background), sem áudio; depois junta e põe o mix.
# Uso (na pasta do vídeo): tools/render.sh parte <ini> <fim> <n>   → out/partes/p<n>.mp4
#                          tools/render.sh juntar                  → out/video.mp4 (H.264 + AAC 192k)
set -e
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
mkdir -p out/partes
if [ "$1" = parte ]; then
  npx remotion render src/index.jsx Mossad out/partes/p$4.mp4 --frames=$2-$3 --muted --codec=h264 --crf=20 --concurrency=2 --log=error
  echo PARTE_OK $4
elif [ "$1" = juntar ]; then
  ls out/partes/p*.mp4 | sort -V | sed "s|^out/partes/|file '|; s|$|'|" > out/partes/lista.txt
  ffmpeg -v error -y -f concat -safe 0 -i out/partes/lista.txt -i public/audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out/video.mp4
  echo RENDER_OK
fi
