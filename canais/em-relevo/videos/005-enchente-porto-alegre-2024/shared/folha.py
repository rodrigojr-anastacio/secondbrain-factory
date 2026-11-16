# folha de contato: folha.py saida.jpg <pasta> q1 q2 ... (frames) ; 3 colunas 640x360
import sys
from PIL import Image, ImageDraw
out, pasta, qs = sys.argv[1], sys.argv[2], sys.argv[3:]
W = Image.new("RGB", (1920, 360 * ((len(qs) + 2) // 3)), "white"); d = ImageDraw.Draw(W)
for i, q in enumerate(qs):
    im = Image.open(f"{pasta}/{q}.png").convert("RGB").resize((640, 360)); x, y = (i % 3) * 640, (i // 3) * 360
    W.paste(im, (x, y)); d.rectangle([x, y, x + 90, y + 24], fill="black"); d.text((x + 5, y + 5), f"{int(q)/30:.1f}s", fill="white")
W.save(out, quality=80)
