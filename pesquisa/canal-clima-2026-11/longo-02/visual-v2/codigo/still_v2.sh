#!/bin/bash
# Stills do visual v2: still_v2.sh <estilo A|B|C|-> <saida_prefixo> <segundos...>  -> visual-v2/<prefixo>-<i>.jpg (1280x720)
# estilo "-" = mapa de papel atual (fotos grandes). Bundle próprio em work/bundle-v2 (REBUNDLE=1 para refazer); não mexe no work/bundle do render aprovado.
cd "$(dirname "$0")/../../remotion"
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
[ -n "$REBUNDLE" -o ! -d ../work/bundle-v2 ] && npx remotion bundle --out-dir=../work/bundle-v2 >/dev/null 2>&1
E=$1; PRE=$2; shift 2
if [ "$E" = "-" ]; then PROPS='{"estilo":null,"fotos":"grande"}'; else PROPS="{\"estilo\":\"$E\",\"fotos\":\"grande\"}"; fi
i=1
for s in "$@"; do
  while pgrep -af "^node .*remotion (render|still)" >/dev/null; do sleep 15; done
  f=$(python3 -c "print(round($s*30))")
  t0=$(date +%s.%N)
  npx remotion still ../work/bundle-v2 LongoV2 ../work/v2/tmp.png --frame=$f --gl=swangle --props="$PROPS" --timeout=240000 2>&1 | grep -i -E "error|exception" | head -3
  ffmpeg -v error -y -i ../work/v2/tmp.png -vf scale=1280:720:flags=lanczos -q:v 3 ../visual-v2/$PRE-$i.jpg
  echo "$PRE-$i t=$s ${E} $(python3 -c "import time;print(round(time.time()-$t0,1))") s"
  i=$((i+1))
done
