"""Baixa thumbs dos 3 melhores e 3 piores longos (28 d, idade >= 3 d p/ os piores) das referências principais e monta 1 grade por canal."""
import json, os, subprocess, sys
from PIL import Image, ImageDraw
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(f'{B}/dados/canais-2026-11-14.json'))
T = f'{B}/thumbs'; os.makedirs(T, exist_ok=True)
sel = {}
for g, cs in d['grupos'].items():
    if g == 'nossos': continue
    for n, c in cs.items():
        if c['papel'] != 'principal' and n not in ('Long After The Guns', 'Ship Tales', 'History Easy Guide', 'História em minutos (clone 08/2026)', 'Archivo Desclasificado', 'Te lo Pinto'): continue
        L = [v for v in c['videos'] if v['idade_d'] <= 28 and not v['short']]
        top = sorted(L, key=lambda v: -v['views'])[:3]
        piores = sorted([v for v in L if v['idade_d'] >= 3 and v not in top], key=lambda v: v['views'])[:3]
        sel[n] = [('TOP', v) for v in top] + [('PIOR', v) for v in piores]
for n, vs in sel.items():
    ims = []
    for tag, v in vs:
        f = f"{T}/{v['id']}.jpg"
        if not os.path.exists(f):
            subprocess.run(['curl', '-s', '--max-time', '30', '--socks5-hostname', '127.0.0.1:40000', '-o', f, v['thumb'] or f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg"])
        try: im = Image.open(f).convert('RGB').resize((480, 270))
        except Exception: im = Image.new('RGB', (480, 270), 'gray')
        c = Image.new('RGB', (480, 300), 'white'); c.paste(im, (0, 0))
        ImageDraw.Draw(c).text((4, 274), f"{tag} {v['views']:,} | {v['titulo'][:62]}", fill='black')
        ims.append(c)
    W = Image.new('RGB', (480 * 3, 300 * ((len(ims) + 2) // 3)), 'white')
    for i, im in enumerate(ims): W.paste(im, ((i % 3) * 480, (i // 3) * 300))
    slug = ''.join(ch if ch.isalnum() else '-' for ch in n.lower())
    W.save(f'{T}/grade-{slug}.jpg', quality=80); print(slug, len(ims))
json.dump({n: [(t, v['id'], v['views'], v['titulo']) for t, v in vs] for n, vs in sel.items()}, open(f'{B}/dados/thumbs-selecao.json', 'w'), ensure_ascii=False, indent=1)
