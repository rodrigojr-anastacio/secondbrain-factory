"""Monta comparativo-<canal>.jpg: esquerda = imagem atual do vídeo, direita = Codex (mesma cena). Uso: comparativo.py <nome> <pasta_ref> <pasta_codex> <rotulo_esq> <saida.jpg>"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

nome, ref, cod, rot, saida = sys.argv[1:6]
W, H, BAR = 640, 360, 34
ids = sorted(p.stem for p in Path(cod).glob("*.jpg"))
f = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", 22)
topo = 50
img = Image.new("RGB", (2 * W + 10, topo + len(ids) * (H + BAR)), "white")
d = ImageDraw.Draw(img)
d.text((10, 12), f"{nome}: {rot} (esq.)  x  Codex (dir.)", fill="black", font=f)
for i, cid in enumerate(ids):
    y = topo + i * (H + BAR)
    d.text((10, y + 5), cid, fill="black", font=f)
    for j, pasta in enumerate((ref, cod)):
        p = Path(pasta) / f"{cid}.jpg"
        if p.exists():
            img.paste(Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS), (j * (W + 10), y + BAR))
q = 82
while True:
    img.save(saida, "JPEG", quality=q, optimize=True)
    if Path(saida).stat().st_size <= 1_450_000 or q <= 40:
        break
    q -= 6
print(saida, Path(saida).stat().st_size, "q", q)
