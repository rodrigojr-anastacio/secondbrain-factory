import sys, os
from PIL import Image, ImageDraw, ImageFont
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
saida = sys.argv[1]; itens = [a.split('|') for a in sys.argv[2:]]  # id|rotulo
W, H, LH = 480, 270, 34
cols = 3; rows = (len(itens) + cols - 1) // cols
img = Image.new('RGB', (cols * W, rows * (H + LH)), (20, 20, 20))
d = ImageDraw.Draw(img)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', 17)
except: f = ImageFont.load_default()
for i, (vid, rot) in enumerate(itens):
    t = Image.open(os.path.join(base, 'thumbs', f'B-{vid}.jpg')).convert('RGB')
    t = t.crop((0, 45, 480, 315)) if t.size == (480, 360) else t.resize((W, H))
    x, y = (i % cols) * W, (i // cols) * (H + LH)
    img.paste(t, (x, y))
    cor = (255, 200, 0) if i == 0 else (120, 180, 255)
    d.rectangle([x, y + H, x + W - 1, y + H + LH - 1], fill=(35, 35, 35))
    d.text((x + 6, y + H + 7), rot[:46], fill=cor, font=f)
img.save(saida, quality=80, optimize=True)
print(saida, os.path.getsize(saida))
