#!/bin/bash
# busca yt-dlp via WARP (sem cota), títulos em es
Y=/home/hermes/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp
OUT=$(dirname "$0")/../busca
while IFS='|' read -r tema q; do
  [ -z "$q" ] && continue
  f="$OUT/${tema}__$(echo "$q" | tr ' ' '_' ).jsonl"
  [ -s "$f" ] && continue
  timeout 120 $Y --proxy socks5://127.0.0.1:40000 --extractor-args "youtube:lang=es" --flat-playlist --dump-json "ytsearch30:$q" > "$f" 2>/dev/null
  echo "$tema | $q -> $(wc -l < "$f")"
done
