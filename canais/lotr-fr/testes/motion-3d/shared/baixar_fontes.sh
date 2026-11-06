#!/bin/bash
# Fontes OFL usadas no teste (ficam fora do git). Depois: hard link para remotion/public/fonts e rode hyperframes/sync.sh.
cd "$(dirname "$0")" && mkdir -p fonts && cd fonts
for u in ofl/anton/Anton-Regular.ttf ofl/ibmplexmono/IBMPlexMono-Medium.ttf ofl/ibmplexmono/IBMPlexMono-Bold.ttf; do
  curl -sL -o "$(basename "$u")" "https://github.com/google/fonts/raw/main/$u"
done
