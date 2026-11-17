#!/bin/bash
# Thumbs 1280×720 (< 500 KB cada): shared/thumbs6.sh -> entrega/thumb-A/B/C.jpg (+ thumbnail.jpg = A)
cd "$(dirname "$0")/.." || exit 1
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH TMPDIR=$HOME/cache/tmp
(cd remotion && npx remotion bundle src/index.js --out-dir=../work/bundle 2>&1 | tail -1)
mkdir -p entrega work/th
for v in A B C; do
  (cd remotion && npx remotion still ../work/bundle Thumb$v ../work/th/$v.png --gl=swangle 2>&1 | grep -i -E "error|exception" | head -3)
  ffmpeg -v error -y -i work/th/$v.png -vf scale=1280:720 -q:v 3 entrega/thumb-$v.jpg
done
cp entrega/thumb-A.jpg entrega/thumbnail.jpg; ls -la entrega
