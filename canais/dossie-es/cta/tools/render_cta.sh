#!/usr/bin/env bash
# Renderiza o cta-hq.mp4 (15 s, 1080p30) na VPS (~30 s) e refaz a prévia cta-hq-frames.jpg.
# Uso (de qualquer lugar): canais/dossie-es/cta/tools/render_cta.sh   (rode antes tools/build_cta.py se mudou voz/capa)
set -euo pipefail
C="$(cd "$(dirname "$0")/.." && pwd)"
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
: "${TMPDIR:=$HOME/cache/tmp}"; W="$TMPDIR/cta-render"; mkdir -p "$W"   # nunca /tmp (tmpfs = RAM)
cd "$C"
[ -d node_modules ] || cp -al ../videos/017-gulag/node_modules node_modules
npx remotion bundle src/index.jsx --out-dir "$W/bundle" --log=error
npx remotion render "$W/bundle" CTA "$W/cta-hq.mp4" --concurrency=2 --gl=swangle --codec=h264 --audio-codec=aac --audio-bitrate=192k --log=error
cp "$W/cta-hq.mp4" "$C/cta-hq.mp4"
rm -rf "$W/fr"; mkdir -p "$W/fr"
ffmpeg -v error -i "$C/cta-hq.mp4" -vf "fps=4/3,scale=480:270" "$W/fr/%02d.jpg"
~/workspace/fabrica-youtube/tools/.venv/bin/python - "$W/fr" "$C/cta-hq-frames.jpg" <<'PY'
import glob, sys
from PIL import Image, ImageDraw
fs = sorted(glob.glob(sys.argv[1] + "/*.jpg"))[:20]; W, H = 480, 270
g = Image.new("RGB", (W * 4, H * 5), "black"); d = ImageDraw.Draw(g)
for k, f in enumerate(fs):
    x, y = (k % 4) * W, (k // 4) * H; g.paste(Image.open(f), (x, y)); d.text((x + 6, y + 4), f"{k * 0.75:.2f}s", fill="yellow")
g.save(sys.argv[2], quality=82, optimize=True)
PY
ffprobe -v error -show_entries format=duration -of csv=p=0 "$C/cta-hq.mp4"
