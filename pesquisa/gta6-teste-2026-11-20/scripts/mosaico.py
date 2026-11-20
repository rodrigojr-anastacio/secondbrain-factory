"""Mosaico: 15 thumbs que mais performam (views/dia, 7 d) + 15 brechas (canais < 250 mil, >= 5x mediana, 30 d)."""
import json, os, subprocess
from PIL import Image, ImageDraw, ImageFont
B = os.path.join(os.path.dirname(__file__), ".."); D = os.path.join(B, "dados"); T = os.path.join(B, "thumbs")
a = json.load(open(os.path.join(D, "analise.json")))
top = [r for r in a["top7"] if r["formato"] != "short"][:15]
br = [r for r in a["brechas"] if r["id"] not in {t["id"] for t in top}][:15]
sel = [("TOP", r) for r in top] + [("BRECHA", r) for r in br]
def baixar(i):
    p = os.path.join(T, i + ".jpg")
    if not os.path.exists(p):
        subprocess.run(["curl", "-s", "--max-time", "40", "--socks5-hostname", "127.0.0.1:40000", "-o", p,
                        f"https://i.ytimg.com/vi/{i}/hqdefault.jpg"])
    return p
W, H = 320, 180; LH = 34; cols = 5
font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 12)
fs = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 11)
rows = (len(sel) + cols - 1) // cols
img = Image.new("RGB", (cols * W, rows * (H + LH) + 30), (20, 20, 20)); d = ImageDraw.Draw(img)
d.text((8, 8), "GTA 6 · linhas 1-3: mais views/dia (7 d) · linhas 4-6: brechas (canal < 250 mil inscr., >= 5x mediana, 30 d) · 20/11/2026", font=font, fill=(255, 220, 0))
for k, (tag, r) in enumerate(sel):
    x, y = (k % cols) * W, 30 + (k // cols) * (H + LH)
    try:
        t = Image.open(baixar(r["id"])).convert("RGB")
        tw, th = t.size; t = t.crop((0, (th - tw * 9 // 16) // 2, tw, (th + tw * 9 // 16) // 2)).resize((W, H))
        img.paste(t, (x, y))
    except Exception: pass
    v = r["views"]; vs = f"{v/1e6:.1f}M" if v >= 1e6 else f"{v/1e3:.0f}k"
    ins = r["inscritos"] or 0; ins = f"{ins/1e6:.1f}M" if ins >= 1e6 else f"{ins/1e3:.1f}k"
    d.text((x + 4, y + H + 2), f"{tag} {vs} · {r['idade_d']}d · x{r['x_mediana']} · {ins} insc", font=font, fill=(255, 255, 255) if tag == "TOP" else (120, 230, 255))
    d.text((x + 4, y + H + 18), r["titulo"][:48], font=fs, fill=(200, 200, 200))
img.save(os.path.join(B, "mosaico.jpg"), quality=82)
img.resize((img.width // 2, img.height // 2)).save(os.path.join(B, "mosaico-320.jpg"), quality=80)
print(os.path.getsize(os.path.join(B, "mosaico.jpg")))
