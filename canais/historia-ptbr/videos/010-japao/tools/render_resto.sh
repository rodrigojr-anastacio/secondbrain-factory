#!/bin/bash
V=~/workspace/fabrica-youtube/canais/historia-ptbr/videos/010-japao
for spec in "1 0 6921" "2 6922 13843" "3 13844 20765" "4 20766 27687"; do
  set -- $spec
  for t in 1 2 3; do
    [ -s $V/out/partes/p$1.mp4 ] && break
    $V/tools/render_parte.sh $1 $2 $3 > $V/logs/render_p$1.log 2>&1
    grep -aq RENDER_OK $V/logs/render_p$1.log && break
  done
done
echo FIM > $V/logs/render_resto.fim
