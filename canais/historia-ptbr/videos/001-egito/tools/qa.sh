#!/bin/bash
# QA do render: specs, contact sheet (20 frames), cortes no 1º minuto, telas pretas, áudio. Rode na pasta do vídeo.
F=out/video.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $F)
echo "== duração: $D s"
for f in $F out/video-telegram.mp4; do echo "== $f"; ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,sample_rate,channels -of default=nw=1 $f; done
mkdir -p qa/cs
for i in $(seq 0 19); do t=$(python3 -c "print(round(($i+0.5)*$D/20,2))"); ffmpeg -loglevel error -y -ss $t -i $F -frames:v 1 -vf "scale=480:270" qa/cs/$(printf %02d $i).png; done
ffmpeg -loglevel error -y -i qa/cs/%02d.png -vf tile=5x4 -frames:v 1 -q:v 3 out/contact-sheet.jpg
echo "== cortes no 1º minuto (scene > 0.3)"
ffmpeg -hide_banner -t 60 -i $F -vf "select='gt(scene,0.3)',showinfo" -an -f null - 2>&1 | grep -c "pts_time"
echo "== telas pretas (>= 0.2 s)"
ffmpeg -hide_banner -i $F -vf "blackdetect=d=0.2:pix_th=0.08" -an -f null - 2>&1 | grep -c black_start
echo "== áudio"
ffmpeg -hide_banner -i $F -af "ebur128=peak=true" -vn -f null - 2>&1 | grep -E "^\s+(I|LRA|Peak):" | tail -3
echo "== silêncios > 1,5 s"
ffmpeg -hide_banner -i $F -af silencedetect=n=-50dB:d=1.5 -vn -f null - 2>&1 | grep silence_start
