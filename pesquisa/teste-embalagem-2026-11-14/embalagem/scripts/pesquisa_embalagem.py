#!/usr/bin/env python3
"""Pesquisa de embalagem (título + thumb) de um vídeo novo, custo zero.

Consolida os scripts da reembalagem de 14/11/2026 (pesquisa/reembalagem-2026-11-14/dados/*/scripts).
Só leitura no YouTube. Busca via yt-dlp **só pelo WARP** (socks5://127.0.0.1:40000), sem cota;
views/datas/medianas pela Data API (videos.list/channels.list/playlistItems = 1 unidade por chamada).
Nunca usa search.list. Nunca imprime tokens.

Uso (rode com tools/.venv/bin/python, a partir de qualquer pasta):
  pesquisa_embalagem.py buscar  <saida> --idioma es "templarios historia" "caballeros templarios" ...
  pesquisa_embalagem.py enriquecer <saida> [--dias 400] [--min-dur 180] [--top 15]
  pesquisa_embalagem.py thumbs <saida> [--top 9] [--nossos ID1,ID2]   # baixa thumbs + mosaico.jpg (≤ 1 MB)

<saida> = <pasta do vídeo>/embalagem (ou pesquisa/<teste>/embalagem). Grava:
  busca/*.jsonl, refs.csv (todas, com mediana do canal e ×med), medianas.json, thumbs/*.jpg, mosaico.jpg
"""
import argparse, csv, datetime, json, os, statistics, subprocess, sys

ROOT = os.path.expanduser('~/workspace/fabrica-youtube')
YTDLP = f'{ROOT}/tools/.venv/bin/yt-dlp'
PROXY = 'socks5://127.0.0.1:40000'
sys.path.insert(0, f'{ROOT}/tools')


def buscar(a):
    os.makedirs(f'{a.saida}/busca', exist_ok=True)
    for q in a.termos:
        f = f"{a.saida}/busca/{q.replace(' ', '_').replace('/', '-')}.jsonl"
        if os.path.exists(f) and os.path.getsize(f) > 0:
            print('já existe', f); continue
        with open(f, 'w') as out:
            subprocess.run(['timeout', '150', YTDLP, '--proxy', PROXY, '--extractor-args', f'youtube:lang={a.idioma}',
                            '--flat-playlist', '--dump-json', f'ytsearch{a.n}:{q}'], stdout=out, stderr=subprocess.DEVNULL)
        print(q, '->', sum(1 for _ in open(f)))


def enriquecer(a):
    from trends import yt_client, segundos
    yt = yt_client(); cota = 0
    hoje = datetime.date.today()
    rank, consultas = {}, {}
    for fn in sorted(os.listdir(f'{a.saida}/busca')):
        q = fn[:-6].replace('_', ' ')
        for i, l in enumerate(open(f'{a.saida}/busca/{fn}')):
            try: d = json.loads(l)
            except Exception: continue
            if not d.get('id'): continue
            rank[d['id']] = min(rank.get(d['id'], 99), i + 1)
            consultas.setdefault(d['id'], set()).add(q)
    ids = list(rank); vids = {}
    for i in range(0, len(ids), 50):
        out = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i + 50])).execute(); cota += 1
        for v in out['items']: vids[v['id']] = v
    chl = list({v['snippet']['channelId'] for v in vids.values()}); ch = {}
    for i in range(0, len(chl), 50):
        out = yt.channels().list(part='snippet,statistics,contentDetails', id=','.join(chl[i:i + 50])).execute(); cota += 1
        for c in out['items']:
            ch[c['id']] = {'nome': c['snippet']['title'], 'inscritos': int(c['statistics'].get('subscriberCount', 0) or 0),
                           'uploads': c['contentDetails']['relatedPlaylists']['uploads']}
    linhas = []
    for vid, v in vids.items():
        sn, st = v['snippet'], v['statistics']
        pub = datetime.date.fromisoformat(sn['publishedAt'][:10]); c = ch.get(sn['channelId'], {})
        linhas.append({'id': vid, 'link': f'https://youtu.be/{vid}', 'titulo': sn['title'], 'canal': c.get('nome'),
                       'channel_id': sn['channelId'], 'inscritos': c.get('inscritos'), 'data': str(pub),
                       'idade_d': (hoje - pub).days, 'dur_s': segundos(v['contentDetails'].get('duration', 'PT0S')),
                       'views': int(st.get('viewCount', 0)), 'rank': rank[vid], 'consultas': ' | '.join(sorted(consultas[vid]))})
    # mediana real (últimos ≤ 30 uploads longos) só dos canais que importam: top-N da janela
    janela = [l for l in linhas if l['idade_d'] <= a.dias and l['dur_s'] >= a.min_dur]
    rel = {l['channel_id'] for l in sorted(janela, key=lambda l: -l['views'])[:a.top]}
    med_path = f'{a.saida}/medianas.json'
    med = json.load(open(med_path)) if os.path.exists(med_path) else {}
    for cid in rel - set(med):
        try:
            pl = yt.playlistItems().list(part='contentDetails', playlistId=ch[cid]['uploads'], maxResults=50).execute(); cota += 1
            vs = [it['contentDetails']['videoId'] for it in pl['items']]
            out = yt.videos().list(part='statistics,contentDetails', id=','.join(vs)).execute(); cota += 1
        except Exception:
            continue
        longos = [int(x['statistics'].get('viewCount', 0)) for x in out['items']
                  if segundos(x['contentDetails'].get('duration', 'PT0S')) >= 180][:30]
        if longos: med[cid] = {'canal': ch[cid]['nome'], 'mediana': statistics.median(longos), 'n': len(longos)}
    for l in linhas:
        m = med.get(l['channel_id'])
        l['mediana_canal'] = m['mediana'] if m else ''
        l['n_mediana'] = m['n'] if m else ''
        l['x_mediana'] = round(l['views'] / m['mediana'], 1) if m and m['mediana'] else ''
        l['na_janela'] = l in janela
    linhas.sort(key=lambda l: (not l['na_janela'], -l['views']))
    with open(f'{a.saida}/refs.csv', 'w') as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)
    json.dump(med, open(med_path, 'w'), ensure_ascii=False, indent=1)
    print(f'vídeos {len(linhas)} · na janela {len(janela)} · medianas {len(med)} · cota {cota} unidades')
    for l in linhas[:a.top]:
        print(f"{l['views']:>10,} {l['x_mediana']!s:>6}× {l['data']} {l['canal'][:22]:22} {l['titulo'][:80]}  {l['link']}")


def thumbs(a):
    from PIL import Image, ImageDraw, ImageFont
    todas = list(csv.DictReader(open(f'{a.saida}/refs.csv')))
    if a.ids:  # curadoria: só os ids pedidos, na ordem dada (tira filmes, idioma errado etc.)
        por_id = {r['id']: r for r in todas}
        rows = [por_id[i] for i in a.ids.split(',') if i in por_id]
    else:
        rows = [r for r in todas if r['na_janela'] == 'True'][:a.top]
    nossos = [x for x in (a.nossos or '').split(',') if x]
    os.makedirs(f'{a.saida}/thumbs', exist_ok=True)
    lista = [(v, 'NOSSO') for v in nossos] + [(r['id'], f"{(r['canal'] or '?')[:20]} · {int(r['views']):,} v · {r['x_mediana']}×".replace(',', '.')) for r in rows]
    for vid, _ in lista:
        f = f'{a.saida}/thumbs/{vid}.jpg'
        if not os.path.exists(f):
            subprocess.run(['curl', '-s', '--max-time', '30', '--socks5-hostname', '127.0.0.1:40000', '-o', f,
                            f'https://i.ytimg.com/vi/{vid}/hqdefault.jpg'])
    try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    except Exception: font = ImageFont.load_default()
    W, H, cols = 480, 270, 3
    nrow = (len(lista) + cols - 1) // cols
    m = Image.new('RGB', (cols * W, nrow * (H + 28)), 'white'); d = ImageDraw.Draw(m)
    for k, (vid, lab) in enumerate(lista):
        try: im = Image.open(f'{a.saida}/thumbs/{vid}.jpg').convert('RGB')
        except Exception: continue
        w, h = im.size; c = int(w * 9 / 16); im = im.crop((0, (h - c) // 2, w, (h - c) // 2 + c)).resize((W - 8, H - 8))
        x, y = (k % cols) * W, (k // cols) * (H + 28)
        d.rectangle([x, y, x + W - 1, y + H - 1], fill='#1f5fbf' if lab == 'NOSSO' else '#b3261e'); m.paste(im, (x + 4, y + 4))
        d.text((x + 6, y + H + 3), lab, fill='black', font=font)
    f, q = f'{a.saida}/{a.nome}.jpg', 85
    while True:
        m.save(f, quality=q)
        if os.path.getsize(f) < 1_000_000 or q < 40: break
        q -= 10
    # prévia de celular: o mesmo mosaico reduzido para cada quadro ter ~320 px de largura
    m.resize((cols * 320, int(nrow * (H + 28) * 320 / W))).save(f'{a.saida}/{a.nome}-320.jpg', quality=80)
    print(f, os.path.getsize(f), '·', len(lista), 'quadros')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); s = p.add_subparsers(dest='cmd', required=True)
    b = s.add_parser('buscar'); b.add_argument('saida'); b.add_argument('termos', nargs='+'); b.add_argument('--idioma', default='es'); b.add_argument('--n', type=int, default=30)
    e = s.add_parser('enriquecer'); e.add_argument('saida'); e.add_argument('--dias', type=int, default=400); e.add_argument('--min-dur', type=int, default=180); e.add_argument('--top', type=int, default=15)
    t = s.add_parser('thumbs'); t.add_argument('saida'); t.add_argument('--top', type=int, default=9); t.add_argument('--nossos', default=''); t.add_argument('--ids', default=''); t.add_argument('--nome', default='mosaico')
    a = p.parse_args(); a.saida = os.path.abspath(a.saida)
    {'buscar': buscar, 'enriquecer': enriquecer, 'thumbs': thumbs}[a.cmd](a)
