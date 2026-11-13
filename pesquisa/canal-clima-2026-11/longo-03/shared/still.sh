#!/bin/bash
# Stills de conferência: shared/still.sh <segundos...> -> work/stills/s-<seg>.jpg (bundle único em work/bundle; refazer com REBUNDLE=1)
cd "$(dirname "$0")/../remotion"
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
mkdir -p ../work/stills
[ -n "$REBUNDLE" ] && npx remotion bundle --out-dir=../work/bundle >/dev/null 2>&1
for s in "$@"; do
  f=$(python3 -c "print(round($s*30))")
  npx remotion still ../work/bundle LongoV3 ../work/stills/s-$s.jpg --frame=$f --gl=swangle --jpeg-quality=80 2>&1 | grep -i -E "error|exception" | head -3
done
