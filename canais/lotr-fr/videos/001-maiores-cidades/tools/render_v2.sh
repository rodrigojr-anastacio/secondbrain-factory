#!/bin/bash
cd /home/hermes/workspace/lotr-cidades
npx remotion render src/index.jsx CidadesFR out/cidades-fr.mp4 --log=error > qa/render_v2.log 2>&1 || { echo RENDER_FAIL >> qa/render_v2.log; exit 1; }
bash tools/finish.sh > qa/finish_v2.log 2>&1
cp qa/contact_sheet.jpg out/contact-sheet.jpg
# named-city contact sheet (1 frame per named-city shot)
python3 - <<'EOF'
import json, subprocess
from PIL import Image, ImageDraw
t = json.load(open('src/timeline.json')); fps = t['fps']
sel = [s for s in t['shots'] if s.get('img', '') and str(s.get('img')).startswith('gen_')]
tiles = []
for k, s in enumerate(sel):
    ts = (s['from'] + s['dur'] / 2) / fps; f = 'qa/cs/city_%02d.png' % k
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(ts), '-i', 'out/cidades-fr.mp4', '-frames:v', '1', '-vf', 'scale=480:270', f], check=True)
    im = Image.open(f).convert('RGB'); ImageDraw.Draw(im).text((6, 6), '%.0fs %s' % (ts, s['img']), fill=(255, 255, 0)); tiles.append(im)
cols = 5; rows = (len(tiles) + cols - 1) // cols
sh = Image.new('RGB', (cols * 480, rows * 270))
for i, im in enumerate(tiles): sh.paste(im, ((i % cols) * 480, (i // cols) * 270))
sh.save('out/contact-sheet-cidades.jpg', quality=85)
EOF
ffmpeg -v error -i out/cidades-fr.mp4 -f null - > qa/decode_main.log 2>&1; echo "decode main rc=$?" >> qa/finish_v2.log
ffmpeg -v error -i out/cidades-fr-telegram.mp4 -f null - > qa/decode_tg.log 2>&1; echo "decode tg rc=$?" >> qa/finish_v2.log
sha256sum out/*.mp4 out/*.srt out/thumbnail.png public/audio/mix.wav >> qa/finish_v2.log
echo DONE >> qa/finish_v2.log
