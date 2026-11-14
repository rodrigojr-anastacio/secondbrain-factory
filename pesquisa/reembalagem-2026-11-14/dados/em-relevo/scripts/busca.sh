#!/bin/bash
# ytsearch via WARP (sem cota). Uso: busca.sh <arquivo_saida_prefixo> "<termo>"
YTDLP=/home/hermes/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp
out=$1; shift
$YTDLP --proxy socks5://127.0.0.1:40000 --flat-playlist --dump-json "ytsearch25:$*" 2>/dev/null > "$out"
echo "$* -> $(wc -l < "$out")"
