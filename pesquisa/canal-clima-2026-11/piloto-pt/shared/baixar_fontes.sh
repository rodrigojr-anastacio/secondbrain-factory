#!/bin/bash
# Fontes OFL (fora do git) para remotion/public/fonts.
cd "$(dirname "$0")/../remotion" && mkdir -p public/fonts && cd public/fonts
for u in ofl/anton/Anton-Regular.ttf ofl/ibmplexmono/IBMPlexMono-Medium.ttf ofl/ibmplexmono/IBMPlexMono-Bold.ttf; do
  curl -sL -o "$(basename "$u")" "https://github.com/google/fonts/raw/main/$u"
done
curl -sL -o PlayfairDisplay-Italic.ttf "https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay-Italic%5Bwght%5D.ttf"
