#!/bin/bash
# Render do vídeo (1080p30 H.264 + AAC) e versão Telegram (720p, ≤ 45 MB). Rode na pasta do vídeo.
set -e
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
npx remotion render src/index.jsx Egito out/video.mp4 --codec=h264 --crf=20 --audio-codec=aac --audio-bitrate=192k --concurrency=2 --log=info
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/video.mp4)
VB=$(python3 -c "print(int(42*8192/$D-96))")
ffmpeg -loglevel error -y -i out/video.mp4 -c:v libx264 -preset medium -b:v ${VB}k -maxrate $((VB*2))k -bufsize $((VB*4))k -vf scale=1280:720 -pass 1 -passlogfile qa/x264 -an -f mp4 /dev/null
ffmpeg -loglevel error -y -i out/video.mp4 -c:v libx264 -preset medium -b:v ${VB}k -maxrate $((VB*2))k -bufsize $((VB*4))k -vf scale=1280:720 -pass 2 -passlogfile qa/x264 -c:a aac -b:a 96k -movflags +faststart out/video-telegram.mp4
echo RENDER_OK
