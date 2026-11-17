"""Grades do pré-QA: preqa/stills/<quadro>.png → preqa/grade_r_NN.jpg (4 colunas, 24 por grade, tempo e plano no canto)."""
import glob, json, os
from PIL import Image, ImageDraw, ImageFont
V = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tl = json.load(open(f"{V}/src/timeline.json"))["planos"]
def plano(q):
    for p in tl:
        if p["from_"] <= q < p["from_"] + p["dur"]: return p
fs = sorted(glob.glob(f"{V}/preqa/stills/*.png"), key=lambda x: int(os.path.basename(x)[:-4]))
for g in glob.glob(f"{V}/preqa/grade_r_*.jpg"): os.remove(g)
fonte = ImageFont.truetype(f"{V}/public/fonts/IBMPlexMono-Bold.ttf", 18)
CW, CH, COLS, POR = 480, 270, 4, 24
for gi in range(0, len(fs), POR):
    lote = fs[gi:gi + POR]; rows = (len(lote) + COLS - 1) // COLS
    S = Image.new("RGB", (CW * COLS, CH * rows))
    for i, f in enumerate(lote):
        q = int(os.path.basename(f)[:-4]); p = plano(q)
        im = Image.open(f).convert("RGB").resize((CW - 4, CH - 4)); d = ImageDraw.Draw(im)
        lab = f"{q // 1800}:{q // 30 % 60:02d} {p['id']} {p['tipo']}"
        d.rectangle((0, 0, d.textlength(lab, font=fonte) + 10, 24), fill=(0, 0, 0)); d.text((5, 2), lab, font=fonte, fill=(253, 213, 5))
        S.paste(im, ((i % COLS) * CW, (i // COLS) * CH))
    S.save(f"{V}/preqa/grade_r_{gi // POR + 1:02d}.jpg", quality=82)
print(len(fs), "stills;", (len(fs) + POR - 1) // POR, "grades")
