# Junta stills em grade (conferência): grade.py saida.jpg s1 s2 ...  (lê work/stills/s-<t>.jpg)
import sys
from PIL import Image, ImageDraw
out, ts = sys.argv[1], sys.argv[2:]
W = Image.new("RGB", (1920, 360 * ((len(ts) + 2) // 3)), "white"); d = ImageDraw.Draw(W)
for i, t in enumerate(ts):
    im = Image.open(f"work/stills/s-{t}.jpg").resize((640, 360)); W.paste(im, ((i % 3) * 640, (i // 3) * 360))
    d.rectangle([(i % 3) * 640, (i // 3) * 360, (i % 3) * 640 + 70, (i // 3) * 360 + 26], fill="black"); d.text(((i % 3) * 640 + 6, (i // 3) * 360 + 6), f"{t}s", fill="white")
W.save(out, quality=82)
