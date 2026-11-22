#!/bin/bash
V=~/workspace/fabrica-youtube/canais/historia-ptbr/videos/014-inglaterra
for spec in "1 0 1799" "2 1800 3599" "3 3600 5399" "4 5400 7199" "5 7200 8999" "6 9000 10799" "7 10800 12599" "8 12600 14399" "9 14400 16199" "10 16200 17999" "11 18000 19799" "12 19800 21599" "13 21600 23399" "14 23400 25199" "15 25200 26999" "16 27000 28799" "17 28800 30413"; do
  set -- $spec
  for t in 1 2 3; do
    [ -s $V/out/partes/p$1.mp4 ] && break
    $V/tools/render_parte.sh $1 $2 $3 > $V/logs/render_p$1.log 2>&1
    grep -aq RENDER_OK $V/logs/render_p$1.log && break
  done
done
echo FIM > $V/logs/render_resto.fim
