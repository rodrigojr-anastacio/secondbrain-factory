# Folha de contato: grade6.py <pasta de pngs> <saida.jpg> [colunas=3] (ordem numérica do nome = quadro; rótulo = segundos)
import sys, glob, os
from PIL import Image, ImageDraw
d, out = sys.argv[1], sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 3
fs = sorted(glob.glob(d + "/*.png"), key=lambda f: int(os.path.basename(f)[:-4]))
w, h = 640, 360; rows = (len(fs) + cols - 1) // cols; sh = Image.new("RGB", (cols * w, rows * h), "black")
for i, f in enumerate(fs):
    im = Image.open(f).convert("RGB").resize((w, h)); dr = ImageDraw.Draw(im); q = int(os.path.basename(f)[:-4])
    dr.rectangle((0, 0, 150, 26), fill="black"); dr.text((6, 6), f"{q/30:.1f}s q{q}", fill="yellow"); sh.paste(im, ((i % cols) * w, (i // cols) * h))
sh.save(out, quality=85); print(out, len(fs))
