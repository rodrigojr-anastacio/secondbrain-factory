#!/bin/bash
# build_cues + bundle + stills: shared/rebundle_e_stills.sh <comp> <saida> <escala> <seg1> <seg2> ...   (nomes dos arquivos = quadro)
cd "$(dirname "$0")/.." || exit 1
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH TMPDIR=$HOME/cache/tmp
~/workspace/fabrica-youtube/tools/.venv/bin/python shared/build_cues.py | head -1
(cd remotion && npx remotion bundle src/index.js --out-dir=../work/bundle 2>&1 | tail -1)
COMP=$1; OUT=$2; ESC=$3; shift 3; mkdir -p "$OUT"
node ~/workspace/fabrica-youtube/tools/remotion_stills.cjs remotion work/bundle "$COMP" "$OUT" swangle "$ESC" "$(python3 -c "import sys;print(','.join(str(int(round(float(x)*30))) for x in sys.argv[1:]))" "$@")"
