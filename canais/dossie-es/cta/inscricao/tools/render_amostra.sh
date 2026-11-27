#!/usr/bin/env bash
# Render da amostra do CTA de inscrição na VPS (~23 s, 1080p30; curto, por isso não vai ao Runpod) + Whisper/botão + prévia.
# Uso (raiz do repo): tools/.venv/bin/python canais/dossie-es/cta/inscricao/tools/amostra.py && canais/dossie-es/cta/inscricao/tools/render_amostra.sh
set -euo pipefail
I="$(cd "$(dirname "$0")/.." && pwd)"; R="$(cd "$I/../../../.." && pwd)"; PY="$R/tools/.venv/bin/python"
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
: "${TMPDIR:=$HOME/cache/tmp}"; export TMPDIR; W="$TMPDIR/cta-inscricao-amostra"   # nunca /tmp (tmpfs = RAM)
"$PY" "$I/inscricao.py" montar "$W" || true          # a posição 55–70% não vale num clipe de 23 s
cp "$I/BotonSuscribete.jsx" "$W/src/"
cd "$W"
npx remotion render src/index.jsx INQ out/mudo.mp4 --muted --codec=h264 --crf=18 --concurrency=2 --log=error
ffmpeg -v error -y -i out/mudo.mp4 -i public/audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out/video.mp4
"$PY" "$I/inscricao.py" qa "$W" --sem-posicao
cp out/video.mp4 "$I/amostra.mp4"
rm -rf fr; mkdir fr
"$PY" - "$W" "$I/amostra-frames.jpg" <<'PY'
import json, subprocess, sys
from PIL import Image, ImageDraw
W, dst = sys.argv[1], sys.argv[2]
r = json.load(open(f"{W}/qa/cta-inscricao.json"))
a, z = r["from"] / 30, (r["from"] + r["dur"]) / 30
ts = [a - 3.0, a - 1.0] + [a + (z - a) * k / 13 for k in range(14)] + [z + 0.6, z + 2.0, z + 3.5, z + 5.0]
w, h = 480, 270; g = Image.new("RGB", (w * 4, h * 5), "black"); d = ImageDraw.Draw(g)
for k, t in enumerate(ts[:20]):
    f = f"{W}/fr/{k:02d}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, t):.2f}", "-i", f"{W}/out/video.mp4", "-frames:v", "1", "-vf", f"scale={w}:{h}", f], check=True)
    x, y = (k % 4) * w, (k // 4) * h; g.paste(Image.open(f), (x, y)); d.text((x + 6, y + 4), f"{t:.1f}s", fill="yellow")
g.save(dst, quality=80, optimize=True)
PY
ls -la "$I/amostra.mp4" "$I/amostra-frames.jpg"
