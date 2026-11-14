# B2: mosaicos da rodada 2 (nossa thumb no ar + maquete + referências dos padrões novos), com rótulo
import os
from PIL import Image, ImageDraw
B = '/home/hermes/workspace/fabrica-youtube/pesquisa/reembalagem-2026-11-14'
T = f'{B}/dados/historia-ptbr/thumbs'; M = f'{B}/crivo/maquetes'
sets = {
 'historia-ptbr-003-ira-v2': [(f'{T}/B-GkzMbsB0iH0.jpg', 'NOSSA no ar (COROA x TURBANTE)'), (f'{M}/historia-ptbr-003-ira-v2.jpg', 'MAQUETE v2 MESMO PAIS? + 2.500 ANOS'),
   (f'{T}/B2-n23GEcINbCg.jpg', 'T2 ref Rota Global 220k 28x'), (f'{T}/B2-iHEsS5GbpK4.jpg', 'T2 ref Wozzy 16,6k 13,8x'), (f'{T}/B2-WTAjmGoUZFg.jpg', 'T2 ref Dark Sigil 15,7k 6,3x'),
   (f'{T}/B2-34MWFK4pFZE.jpg', 'T2 ref HQ Imperio que Ressurgiu 54k 2,2x'), (f'{T}/B-3mwAf9TW1MU.jpg', 'thumb ref Brasil Paralelo 61,9k 4,8x'), (f'{T}/B-jvM3cR235yw.jpg', 'T1 ref Hist. Milenares 294k 7,2x'), (f'{T}/B2-urr9v7oM3O0.jpg', 'T1 ref Hist. Romanas NUNCA 125k 2,1x')],
 'historia-ptbr-007-russia-v2': [(f'{T}/B-3TwMYoxnF4k.jpg', 'NOSSA no ar (UM VIKING NO TRONO?)'), (f'{M}/historia-ptbr-007-russia-v2.jpg', 'MAQUETE v2 TUDO ISSO? (mapa, sem viking)'),
   (f'{T}/B-T6f2gWo9kS0.jpg', 'thumb ref Versed 33,9k 18,5x'), (f'{T}/B2-n23GEcINbCg.jpg', 'thumb ref Rota Global 220k 28x'), (f'{T}/B2-KG3m9FtuVmk.jpg', 'thumb ref Trendou 10k 1,4x'),
   (f'{T}/B-jvM3cR235yw.jpg', 'apoio Hist. Milenares (mapa+figura) 7,2x'), (f'{T}/B-wMFP6PadPmQ.jpg', 'T1 ref Alem do Mapa 28,4k 27x'), (f'{T}/B-XyX7Y-xyhyg.jpg', 'T1 ref Pablo Soncini 508k 11,9x'), (f'{T}/B-aMld6kMmcm4.jpg', 'clone pt (nao copiar) 254k')],
 'historia-ptbr-006-roma-v2': [(f'{T}/B-fkltw3XwQ0E.jpg', 'NOSSA no ar (ROMA HUMILHADA)'), (f'{M}/historia-ptbr-006-roma-v2-proxy.jpg', 'MAQUETE-PROXY v2 DE NOVO? + 410'),
   (f'{T}/B-cM9084oMpXc.jpg', 'thumb ref Hist. Romanas 189k 3,1x'), (f'{T}/B2-58Um0ZXSXx4.jpg', 'thumb+T2 ref Hist. do Mundo 289k 16,5x'), (f'{T}/B-IdvlTEQ72r8.jpg', 'thumb ref HEG bonequinho 238k 43x'),
   (f'{T}/B-EHLI2WZUtXs.jpg', 'apoio en Historically 10,7mi 1,9x'), (f'{T}/B-sLyfGzpuIGY.jpg', 'T2 ref HQ Fundacao a Queda 204k 8,1x'), (f'{T}/B-US27NANBd2g.jpg', 'T2 ref Epopeia 30k 1,5-3,9x'), (f'{T}/B-XyulPwDw1CE.jpg', 'clone/colisao HEG INTEIRA 73k')],
}
W, H = 480, 270
for nome, items in sets.items():
    im = Image.new('RGB', (W * 3, (H + 22) * 3), (20, 20, 20)); d = ImageDraw.Draw(im)
    for k, (f, lab) in enumerate(items):
        t = Image.open(f).convert('RGB'); r = t.width / t.height
        if r < 1.7: h = int(t.width / (16 / 9)); y = (t.height - h) // 2; t = t.crop((0, y, t.width, y + h))
        t = t.resize((W, H)); x0 = (k % 3) * W; y0 = (k // 3) * (H + 22); im.paste(t, (x0, y0 + 22)); d.text((x0 + 4, y0 + 5), lab, fill=(255, 220, 0))
    im.save(f'{B}/mosaicos/{nome}.jpg', quality=82); print(nome, os.path.getsize(f'{B}/mosaicos/{nome}.jpg'))
