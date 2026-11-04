#!/bin/bash
# Render do vídeo (1080p30 H.264 + AAC). Rode na pasta do vídeo. (002: sem versão do Telegram, a pedido do Rodrigo.)
set -e
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
npx remotion render src/index.jsx India out/video.mp4 --codec=h264 --crf=20 --audio-codec=aac --audio-bitrate=192k --concurrency=2 --log=info
echo RENDER_OK
