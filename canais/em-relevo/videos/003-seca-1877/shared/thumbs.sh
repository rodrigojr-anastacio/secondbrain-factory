#!/bin/bash
# Thumbs 1280×720 (< 2 MB): render da composição Thumb<v> em 1920×1080 e redução. Uso: shared/thumbs.sh
cd "$(dirname "$0")/../remotion"; export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
for v in 1 2 3; do
  npx remotion still ../work/bundle Thumb$v ../work/thumb-$v-full.png --gl=swangle 2>&1 | grep -i -E "error|exception" | head -3
  ffmpeg -v error -y -i ../work/thumb-$v-full.png -vf scale=1280:720 -q:v 3 ../out/thumb-$v.jpg
done
ls -la ../out/thumb-*.jpg
