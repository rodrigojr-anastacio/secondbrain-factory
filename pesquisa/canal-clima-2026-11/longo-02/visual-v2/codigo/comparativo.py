# Grade comparativa: linhas = atual, A, B, C; colunas = Pacífico, Brasil inteiro, zoom regional (Manaus) -> visual-v2/comparativo.jpg
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
V = Path(__file__).resolve().parents[1]; F = V.parent / "remotion/public/fonts"
fA, fM = ImageFont.truetype(str(F / "Anton-Regular.ttf"), 44), ImageFont.truetype(str(F / "IBMPlexMono-Bold.ttf"), 22)
linhas = [("atual", "ATUAL", "maquete de papel"), ("estilo-A", "A", "satélite real"), ("estilo-B", "B", "relevo editorial"), ("estilo-C", "C", "pergaminho")]
cols = ["PACÍFICO (1:10)", "BRASIL INTEIRO (5:40)", "ZOOM REGIONAL · MANAUS (0:11)"]
w, h, L, T = 640, 360, 230, 50
g = Image.new("RGB", (L + 3 * w + 4 * 6, T + 4 * h + 5 * 6), "#1F1A18"); d = ImageDraw.Draw(g)
for j, c in enumerate(cols): d.text((L + 6 + j * (w + 6) + 12, 12), c, font=fM, fill="#E9DCC3")
for i, (pre, nome, sub) in enumerate(linhas):
    y = T + 6 + i * (h + 6)
    d.text((18, y + h / 2 - 50), nome, font=fA, fill="#E8505B"); d.text((18, y + h / 2 + 8), sub, font=fM, fill="#E9DCC3")
    for j in range(3):
        g.paste(Image.open(V / f"{pre}-{j + 1}.jpg").resize((w, h), Image.LANCZOS), (L + 6 + j * (w + 6), y))
g.save(V / "comparativo.jpg", quality=88); print(g.size)
