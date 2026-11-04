#!/bin/bash
set -e
cd /home/hermes/workspace/lotr-cidades
F=out/cidades-fr.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $F)
# Telegram: target ~40 MB total -> video kbps = 40*8192/D - 96
VB=$(python3 -c "print(int(40*8192/$D-96))")
ffmpeg -loglevel error -y -i $F -c:v libx264 -preset medium -b:v ${VB}k -maxrate $((VB*2))k -bufsize $((VB*4))k -vf scale=1280:720 -pass 1 -an -f mp4 /dev/null
ffmpeg -loglevel error -y -i $F -c:v libx264 -preset medium -b:v ${VB}k -maxrate $((VB*2))k -bufsize $((VB*4))k -vf scale=1280:720 -pass 2 -c:a aac -b:a 96k -movflags +faststart out/cidades-fr-telegram.mp4
rm -f ffmpeg2pass-0.log*
# contact sheet: 20 frames evenly spaced
mkdir -p qa/cs && rm -f qa/cs/*
for i in $(seq 0 19); do t=$(python3 -c "print(round(($i+0.5)*$D/20,2))"); ffmpeg -loglevel error -y -ss $t -i $F -frames:v 1 -vf "scale=480:270,drawtext=fontfile=/home/hermes/workspace/lotr-pilot/public/assets/DejaVuSans.ttf:text='$t s':x=6:y=6:fontsize=16:fontcolor=yellow:box=1:boxcolor=black" qa/cs/$(printf %02d $i).png; done
ffmpeg -loglevel error -y -i qa/cs/%02d.png -vf tile=4x5 -frames:v 1 qa/contact_sheet.jpg
for f in $F out/cidades-fr-telegram.mp4; do echo "== $f"; ffprobe -v error -show_entries format=duration,size,bit_rate:stream=codec_name,width,height,r_frame_rate,sample_rate,channels -of default=nw=1 $f; done
echo "== audio"; ffmpeg -hide_banner -i $F -af "ebur128=peak=true,volumedetect" -f null - 2>&1 | grep -E "I:|LRA:|Peak:|max_volume|mean_volume" | tail -6
echo "== silence >2.5s"; ffmpeg -hide_banner -i $F -af silencedetect=n=-45dB:d=2.5 -f null - 2>&1 | grep silence_ | head
