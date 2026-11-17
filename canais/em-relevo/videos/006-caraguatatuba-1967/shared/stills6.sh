#!/bin/bash
# Stills do 006 na VPS: shared/stills6.sh <saida> <escala> <seg1> <seg2> ...  (rebundle automático se REBUNDLE=1)
cd "$(dirname "$0")/.." || exit 1
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH TMPDIR=$HOME/cache/tmp
[ -n "$REBUNDLE" ] && (cd remotion && npx remotion bundle src/index.js --out-dir=../work/bundle 2>&1 | tail -1)
OUT=$1; ESC=$2; shift 2; mkdir -p "$OUT"
node ../../../../tools/remotion_stills.cjs remotion work/bundle Longo6 "$OUT" swangle "$ESC" "$(python3 -c "import sys;print(','.join(str(int(round(float(x)*30))) for x in sys.argv[1:]))" "$@")"
