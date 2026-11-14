"""Monta a entrega da reembalagem (14/11/2026): titulos.txt por vídeo, cópias em entrega/, TITULOS.md e mosaico-novas.jpg.
Uso (raiz do repo): tools/.venv/bin/python pesquisa/reembalagem-2026-11-14/thumbs/entrega.py"""
import os, re, shutil
from PIL import Image, ImageDraw, ImageFont
R = os.path.expanduser("~/workspace/fabrica-youtube"); P = f"{R}/pesquisa/reembalagem-2026-11-14"; E = f"{P}/entrega"
H, D = "canais/historia-ptbr/videos", "canais/dossie-es/videos"
CL = "pesquisa/canal-clima-2026-11"
# (canal, video, cabeçalho no PROPOSTAS, pasta, thumb atual)
V = [
 ("historia-ptbr", "001-egito", "## 001 Egito", f"{H}/001-egito", "dados/historia-ptbr/A-thumbs/g847Td0Plsk.jpg"),
 ("historia-ptbr", "002-india", "## 002 Índia", f"{H}/002-india", "dados/historia-ptbr/A-thumbs/MV5SSjoccqE.jpg"),
 ("historia-ptbr", "003-ira", "## 003 Irã", f"{H}/003-ira", "thumbs/atuais/historia-ptbr-003-ira.jpg"),
 ("historia-ptbr", "004-china", "## 004 China", f"{H}/004-china", "dados/historia-ptbr/A-thumbs/-sx6xAkQbA0.jpg"),
 ("historia-ptbr", "005-brasil", "## 005 Brasil", f"{H}/005-brasil", "dados/historia-ptbr/A-thumbs/3aA7eUzwfeg.jpg"),
 ("historia-ptbr", "006-roma", "## 006 Roma", f"{H}/006-roma", "thumbs/atuais/historia-ptbr-006-roma.jpg"),
 ("historia-ptbr", "007-russia", "## 007 Rússia", f"{H}/007-russia", "thumbs/atuais/historia-ptbr-007-russia.jpg"),
 ("dossie-es", "001-cia", "## 001 CIA", f"{D}/001-cia", "dados/dossie-es/thumbs-r2/Qs-TusYCr-o.jpg"),
 ("dossie-es", "002-mossad", "## 002 Mossad", f"{D}/002-mossad", "dados/dossie-es/thumbs-r2/it37m7pz0hI.jpg"),
 ("dossie-es", "003-fbi", "## 003 FBI", f"{D}/003-fbi", "dados/dossie-es/thumbs-r2/E1Rgm7jbE0g.jpg"),
 ("dossie-es", "004-cosa-nostra", "## 004 Cosa Nostra", f"{D}/004-cosa-nostra", "dados/dossie-es/thumbs-r2/gmA0LkJqf_U.jpg"),
 ("dossie-es", "005-kgb", "## 005 KGB", f"{D}/005-kgb", "thumbs/atuais/dossie-es-005-kgb.jpg"),
 ("dossie-es", "006-masones", "## 006 Masones", f"{D}/006-masones", "dados/dossie-es/thumbs-r2/DBLonwmeQ7c.jpg"),
 ("em-relevo", "el-nino-2026", "## El Niño 2026", f"{CL}/longo-02", "dados/em-relevo/thumbs/FeSLzHvlkbo.jpg"),
 ("em-relevo", "sul-do-brasil", "## Sul do Brasil (tornados)", f"{CL}/longo-01", "dados/em-relevo/thumbs/bG6-E4qjXYc.jpg"),
]
EM = {"el-nino-2026": "nino", "sul-do-brasil": "sul"}
txt = open(f"{P}/PROPOSTAS.md").read().split("\n")
def titulos(head):
    i = txt.index(head); out = {}
    for l in txt[i + 1:i + 40]:
        m = re.match(r"\*\*Título ([12]):\*\* \*\*(.+?)\*\*", l)
        if m: out[m.group(1)] = m.group(2)
    return out
os.makedirs(E, exist_ok=True); linhas = []; pares = []
for canal, vid, head, pasta, atual in V:
    pd = f"{R}/{pasta}/reembalagem-2026-11-14"; os.makedirs(pd, exist_ok=True)
    if vid in EM: shutil.copy(f"{P}/thumbs/em-relevo/{EM[vid]}-thumb.jpg", f"{pd}/thumb-nova.jpg")
    t = titulos(head); assert len(t) == 2, head
    for k, s in t.items(): assert len(s) <= 100, (vid, k, len(s))
    nota = ""
    if vid == "sul-do-brasil": nota = '\nNota (se usar o T2): renomear o capítulo 4:35 para "4:35 O rio invisível e a parede dos Andes".\n'
    open(f"{pd}/titulos.txt", "w").write(f"T1: {t['1']}\nT2: {t['2']}\n{nota}")
    dst = f"{E}/{canal}-{vid}.jpg"; shutil.copy(f"{pd}/thumb-nova.jpg", dst)
    assert os.path.getsize(dst) < 2 * 1024 * 1024
    linhas.append(f"| {canal} {vid} | {t['1']} ({len(t['1'])}) | {t['2']} ({len(t['2'])}) | `entrega/{canal}-{vid}.jpg` |")
    pares.append((f"{canal} {vid}", f"{P}/{atual}", f"{pd}/thumb-nova.jpg"))
open(f"{E}/TITULOS.md", "w").write("# Reembalagem: títulos e thumbs novas (14/11/2026)\n\nFonte: `../PROPOSTAS.md` (aprovada pelo Rodrigo em 14/11). 1 thumb + 2 títulos por vídeo; caracteres entre parênteses. Sul do Brasil: se usar o T2, renomear o capítulo 4:35 para \"4:35 O rio invisível e a parede dos Andes\".\n\n| Vídeo | T1 | T2 | Thumb nova |\n|---|---|---|---|\n" + "\n".join(linhas) + "\n")
# mosaico: 2 pares (atual | nova) por linha, células 320x180
f = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 15)
w, h, lh = 320, 180, 20; cols = 2; rows = (len(pares) + 1) // 2
M = Image.new("RGB", (cols * (2 * w + 12) + 12, rows * (h + lh + 8) + 8), (18, 18, 18)); d = ImageDraw.Draw(M)
for i, (n, a, b) in enumerate(pares):
    x = 8 + (i % cols) * (2 * w + 12); y = 8 + (i // cols) * (h + lh + 8)
    d.text((x, y + 1), f"{n}:  atual (esq.) × nova (dir.)", fill=(247, 194, 27), font=f)
    for j, p in enumerate((a, b)):
        M.paste(Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS), (x + j * (w + 4), y + lh))
q = 85; p = f"{E}/mosaico-novas.jpg"
while True:
    M.save(p, quality=q, optimize=True)
    if os.path.getsize(p) <= 1_000_000 or q < 40: break
    q -= 5
print(p, M.size, os.path.getsize(p) // 1024, "KB")
