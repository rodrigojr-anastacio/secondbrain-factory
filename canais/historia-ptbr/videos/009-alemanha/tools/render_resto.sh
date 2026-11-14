#!/bin/bash
V=~/workspace/fabrica-youtube/canais/historia-ptbr/videos/009-alemanha
for spec in "4 15630 20839" "5 20840 26049" "6 26050 31258"; do
  set -- $spec
  for t in 1 2 3; do
    [ -s $V/out/partes/p$1.mp4 ] && break
    $V/tools/render_parte.sh $1 $2 $3 > $V/logs/render_p$1.log 2>&1
    grep -aq RENDER_OK $V/logs/render_p$1.log && break
  done
done
echo FIM > $V/logs/render_resto.fim
