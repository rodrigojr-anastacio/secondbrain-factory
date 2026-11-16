#!/bin/bash
# Recorta os trechos reais (dl/, fora do git) em clipes 4:3 mudos 30 fps para remotion/public/clips/. Ver FONTES-E-LICENCAS.md.
cd "$(dirname "$0")/.." && O=remotion/public/clips && mkdir -p $O
c() { ffmpeg -v error -y -ss $2 -i dl/$1.mp4 -t $3 -an -vf "$4,scale=960:720,fps=30,setsar=1" -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p $O/$5.mp4 && echo "$5 ok"; }
c gm5vWBbuXyY 102.2 5.7 "crop=ih*0.88*4/3:ih*0.88:(iw-ih*0.88*4/3)/2+60:0" maringa
c okd61_o5xks 104 7 "crop=ih*0.79*4/3:ih*0.79:(iw-ih*0.79*4/3)/2:ih*0.05" chapeco
c ix8SSbAajAw 13.0 5.5 "crop=iw*0.75:ih:iw*0.125:0" santo-augusto
cp dl/goes-GOES-East_ABI_Band13_Clean_Infrared.png remotion/public/img/goes-ir.png
cp dl/goes-GOES-East_ABI_GeoColor.png remotion/public/img/goes-geocolor.png
