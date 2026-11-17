#!/bin/bash
V=~/workspace/fabrica-youtube/canais/historia-ptbr/videos/011-estados-unidos
for spec in "1 0 7108" "2 7109 10708" "3 10709 14308" "4 14309 17908" "5 17909 21508" "6 21509 25108" "7 25109 28435"; do
  set -- $spec
  for t in 1 2 3; do
    [ -s $V/out/partes/p$1.mp4 ] && break
    $V/tools/render_parte.sh $1 $2 $3 > $V/logs/render_p$1.log 2>&1
    grep -aq RENDER_OK $V/logs/render_p$1.log && break
  done
done
echo FIM > $V/logs/render_resto.fim
