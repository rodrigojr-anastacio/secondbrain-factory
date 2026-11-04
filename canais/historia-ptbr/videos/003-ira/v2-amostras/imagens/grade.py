"""Monta as grades da bancada (1 linha por modelo, nome e preço escritos). Uso: python grade.py"""
import json, os
from PIL import Image, ImageDraw, ImageFont
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(AQUI, "../thumbs/base/fonts/OpenSans[wdth,wght].ttf")
res = json.load(open(os.path.join(AQUI, "resultados.json")))
testados = [(k, v) for k, v in res.items() if v.get("status") == "testado"]
W, H, LAB = 840, 473, 330
f1, f2 = ImageFont.truetype(F, 30), ImageFont.truetype(F, 24)
def linha(img_paths, t1, t2, fundo=(250, 246, 235)):
    im = Image.new("RGB", (LAB + 2 * W + 30, H + 20), fundo); d = ImageDraw.Draw(im)
    d.multiline_text((15, 40), t1, font=f1, fill=(20, 20, 20), spacing=6)
    d.multiline_text((15, 260), t2, font=f2, fill=(90, 50, 0), spacing=6)
    for i, p in enumerate(img_paths):
        im.paste(Image.open(p).convert("RGB").resize((W, H)), (LAB + i * (W + 10), 10))
    return im
base = os.path.join(AQUI, "../../")
ref = linha([base + "../001-egito/imagens/I041.jpg", base + "../002-india/imagens/I041.jpg"],
            "REFERÊNCIA\ngpt-image-2 medium\n(OpenAI direto)", "Egito e Índia\n~US$ 0,055/img", (255, 225, 140))
def quebra(s, n=20):
    out, cur = [], ""
    for w in s.replace("/", "/ ").split():
        if len(cur) + len(w) > n: out.append(cur); cur = ""
        cur += w + " "
    return "\n".join(out + [cur]).replace("/ ", "/")
linhas = [linha([f"amostras/{k}-I002.jpg", f"amostras/{k}-I007.jpg"], quebra(k),
                f"US$ {v['preco_img']:.3f}/img\n{v['cenas']['I002']['resolucao']}\n{quebra(v['endpoint'], 24)}") for k, v in testados]
for g, grupo in enumerate([linhas[:6], linhas[6:]], 1):
    rows = [ref] + grupo
    out = Image.new("RGB", (rows[0].width, sum(r.height for r in rows)), "white"); y = 0
    for r in rows: out.paste(r, (0, y)); y += r.height
    out = out.resize((2000, int(out.height * 2000 / out.width)))
    out.save(os.path.join(AQUI, f"grade-{g}.jpg"), quality=82); print(f"grade-{g}.jpg", out.size)
