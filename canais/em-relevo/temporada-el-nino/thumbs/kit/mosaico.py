"""Mosaico 'como no sugerido': nossas amostras × thumbs que performam no tema (320×180 + título + canal · views). 28/11/2026."""
import os, textwrap
from PIL import Image, ImageDraw, ImageFont
B = os.path.expanduser("~/workspace/fabrica-youtube/canais/em-relevo/temporada-el-nino")
F = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F2 = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
itens = [
 ("thumbs/e1-A-costa-encostou.jpg", "O Pacífico passou 1997 e 2015: o que o Super El Niño já faz com o Brasil", "NOSSO E1 · Par A", True),
 ("mercado/thumbs/A_DD4hC8UoQ.jpg", "O SUPER El Niño Visto do Espaço: o Que Vai Acontecer com o Brasil", "Cosmos Brutal · 100 mil", False),
 ("thumbs/e1-B-escala-mar-quente.jpg", "Super El Niño: o mar quente de 2026 já é maior que o Brasil inteiro", "NOSSO E1 · Par B", True),
 ("mercado/thumbs/GIlODBvMMKE.jpg", "O Pacífico está PARTINDO o BRASIL em DOIS", "CanalSingularidade · 2,2 mi", False),
 ("mercado/thumbs/gkkqmtbOwmE.jpg", "O El Niño de 2026 NÃO é o Que Você Pensa", "Sou curioso?! · 1,1 mi", False),
 ("thumbs/e1-C-globo-2026-contorno-2015.jpg", "Super El Niño: o mar quente de 2026 já é o dobro do último recorde", "NOSSO E1 · Par C", True),
 ("mercado/thumbs/LXQmVHzwhSU.jpg", "O Que Destruiu Tupanciretã Pode Voltar — e o Super El Niño Explica Por Quê", "Radar do Planeta · 151 mil", False),
 ("mercado/thumbs/BAf4EYZ1AGk.jpg", "Super EL NIÑO NO BRASIL: o que esperar?", "Paulo Jubilut · 5,9 mi", False),
 
 ("mercado/thumbs/753EunXU8LM.jpg", "EL NIÑO VAI CASTIGAR O BRASIL? O ALERTA DE SACANI!", "Cosmos Oculto · 318 mil", False),
 ("mercado/thumbs/oGWX6AVkKZo.jpg", "O El Niño NÃO é o Que Pensávamos Que Fosse", "Miranda Verso · 1,7 mi", False),
 ("thumbs/r002-mesma-causa.jpg", "Super El Niño: por que falta chuva em Manaus e sobra em Santa Catarina", "NOSSO 002 reembalado", True),
 ("mercado/thumbs/1iAw3SROEnA.jpg", "El Niño: como a passagem do fenômeno se tornou um desastre global", "BBC News Brasil · 1,5 mi", False),
 ("mercado/thumbs/p59XASLA-2A.jpg", "É assim que o Super EL NIÑO vai Atingir cada estado do Brasil", "Capital Financeiro · 972 mil", False),
 ("mercado/thumbs/y55u6AnLkK8.jpg", "🔴ALERTA: SÉRGIO SACANI EXPLICA O SUPER EL NIÑO E AS CHUVAS DE SETEMBRO", "FrameCast BR · 2,4 mi", False),
 ("mercado/thumbs/FeSLzHvlkbo.jpg", "El Niño 2026 vai ser o mais forte da história?", "NOSSO 002 hoje · 163 views", True),
]
cw, ch, th = 320, 180, 64; pad = 14; cols = 4; rows = (len(itens) + cols - 1) // cols
g = Image.new("RGB", (cols * (cw + pad) + pad, rows * (ch + th + pad) + pad), (15, 15, 15)); d = ImageDraw.Draw(g)
ft = ImageFont.truetype(F, 13); fc = ImageFont.truetype(F2, 12)
for k, (p, t, c, nosso) in enumerate(itens):
    x = pad + (k % cols) * (cw + pad); y = pad + (k // cols) * (ch + th + pad)
    im = Image.open(os.path.join(B, p)).convert("RGB").resize((cw, ch), Image.LANCZOS); g.paste(im, (x, y))
    if nosso: d.rectangle([x - 4, y - 4, x + cw + 3, y + ch + 3], outline=(255, 214, 64), width=3)
    linhas = textwrap.wrap(t.replace("🔴", ""), 40)[:2]
    for i, l in enumerate(linhas): d.text((x, y + ch + 6 + i * 16), l, font=ft, fill=(241, 241, 241))
    d.text((x, y + ch + 42), c, font=fc, fill=(255, 214, 64) if nosso else (170, 170, 170))
g.save(os.path.join(B, "mosaico-sugerido.jpg"), quality=90); print(g.size)
