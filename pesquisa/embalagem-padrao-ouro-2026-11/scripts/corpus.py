#!/usr/bin/env python3
"""Corpus do padrão ouro de embalagem (17/11/2026). Só leitura, custo zero.

Por canal: uploads dos últimos 2 anos (playlistItems + videos.list = 1 unidade/50), só vídeos longos
(>= 180 s), top N por views + 10 mais recentes, mediana real (últimos 30 longos com >= 7 dias),
×mediana, thumbs maxresdefault via WARP, mosaico por canal (jpg < 2 MB) + versão 160x90.
Nunca usa search.list. Nunca imprime tokens. Tudo grava em $TMPDIR/disco, nunca /tmp.

Uso (tools/.venv/bin/python):
  corpus.py <grupo> <rotulo>=<@handle|UCid|busca:texto> [...] [--top 25]
Saída: corpus/<rotulo>.json, corpus/<rotulo>.csv, ../mosaicos/<rotulo>.jpg e <rotulo>-160.jpg, thumbs/<rotulo>/*.jpg
"""
import argparse, csv, datetime, json, os, statistics, subprocess, sys
ROOT = os.path.expanduser('~/workspace/fabrica-youtube')
OUT = f'{ROOT}/pesquisa/embalagem-padrao-ouro-2026-11'
YTDLP = f'{ROOT}/tools/.venv/bin/yt-dlp'
sys.path.insert(0, f'{ROOT}/tools')
from trends import yt_client, segundos  # noqa

CAMPOS = ['grupo', 'canal', 'canal_id', 'inscritos', 'mediana_30', 'selecao', 'video_id', 'publicado', 'dur_s',
          'views', 'x_mediana', 'titulo', 'n_chars', 'thumb']


def resolve(yt, alvo):
    if alvo.startswith('UC'):
        r = yt.channels().list(part='snippet,statistics,contentDetails', id=alvo).execute()
    elif alvo.startswith('@'):
        r = yt.channels().list(part='snippet,statistics,contentDetails', forHandle=alvo).execute()
    else:  # busca:texto -> 1º resultado yt-dlp via WARP -> canal do vídeo
        q = alvo.split(':', 1)[1]
        p = subprocess.run(['timeout', '120', YTDLP, '--proxy', 'socks5://127.0.0.1:40000', '--flat-playlist',
                            '--print', 'id', f'ytsearch1:{q}'], capture_output=True, text=True)
        vid = p.stdout.strip().splitlines()[0]
        cid = yt.videos().list(part='snippet', id=vid).execute()['items'][0]['snippet']['channelId']
        r = yt.channels().list(part='snippet,statistics,contentDetails', id=cid).execute()
    c = r['items'][0]
    return c['id'], c['snippet']['title'], int(c['statistics'].get('subscriberCount', 0) or 0), \
        c['contentDetails']['relatedPlaylists']['uploads']


def coleta(yt, grupo, rotulo, alvo, top):
    cid, nome, insc, upl = resolve(yt, alvo)
    hoje = datetime.date.today(); corte = hoje - datetime.timedelta(days=int(os.environ.get('DIAS', '730')))
    ids, tok = [], None
    while True:
        r = yt.playlistItems().list(part='contentDetails', playlistId=upl, maxResults=50, pageToken=tok).execute()
        fim = False
        for it in r['items']:
            d = it['contentDetails'].get('videoPublishedAt', '')[:10]
            if d and datetime.date.fromisoformat(d) < corte:
                fim = True; continue
            ids.append(it['contentDetails']['videoId'])
        tok = r.get('nextPageToken')
        if fim or not tok or len(ids) > 600:
            break
    vs = []
    for i in range(0, len(ids), 50):
        for v in yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i + 50])).execute()['items']:
            dur = segundos(v['contentDetails']['duration'])
            if dur < 180:
                continue
            vs.append({'video_id': v['id'], 'publicado': v['snippet']['publishedAt'][:10], 'dur_s': dur,
                       'views': int(v['statistics'].get('viewCount', 0) or 0), 'titulo': v['snippet']['title']})
    vs.sort(key=lambda x: x['publicado'], reverse=True)
    maduros = [v for v in vs if (hoje - datetime.date.fromisoformat(v['publicado'])).days >= 7][:30]
    med = statistics.median([v['views'] for v in maduros]) if maduros else 0
    topv = sorted(vs, key=lambda x: -x['views'])[:top]
    rec = vs[:10]
    sel = {}
    for v in topv: sel[v['video_id']] = dict(v, selecao='top')
    for v in rec:
        if v['video_id'] in sel: sel[v['video_id']]['selecao'] = 'top+recente'
        else: sel[v['video_id']] = dict(v, selecao='recente')
    linhas = []
    tdir = f'{OUT}/thumbs/{rotulo}'; os.makedirs(tdir, exist_ok=True)
    for v in sel.values():
        f = f'{tdir}/{v["video_id"]}.jpg'
        if not os.path.exists(f) or os.path.getsize(f) < 3000:
            for q in ('maxresdefault', 'hqdefault'):
                subprocess.run(['curl', '-s', '--max-time', '30', '--socks5-hostname', '127.0.0.1:40000', '-o', f,
                                f'https://i.ytimg.com/vi/{v["video_id"]}/{q}.jpg'])
                if os.path.exists(f) and os.path.getsize(f) > 3000: break
        linhas.append(dict(v, grupo=grupo, canal=nome, canal_id=cid, inscritos=insc, mediana_30=int(med),
                           x_mediana=round(v['views'] / med, 2) if med else '', n_chars=len(v['titulo']),
                           thumb=os.path.relpath(f, OUT)))
    linhas.sort(key=lambda x: (x['selecao'] == 'recente', -x['views']))
    with open(f'{OUT}/corpus/{rotulo}.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS); w.writeheader()
        for l in linhas: w.writerow({k: l.get(k, '') for k in CAMPOS})
    json.dump({'canal': nome, 'canal_id': cid, 'inscritos': insc, 'mediana_30': med, 'longos_2a': len(vs),
               'coletado': str(hoje)}, open(f'{OUT}/corpus/{rotulo}.json', 'w'), ensure_ascii=False, indent=1)
    mosaico(rotulo, nome, med, [l for l in linhas if l['selecao'] != 'recente'][:16])
    print(f'{rotulo}: {nome} | insc {insc} | longos 2a {len(vs)} | mediana {int(med)} | sel {len(linhas)}')


def mosaico(rotulo, nome, med, linhas):
    from PIL import Image, ImageDraw, ImageFont
    try:
        fnt = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', 18)
        fh = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', 26)
    except Exception:
        fnt = fh = ImageFont.load_default()
    W, H, cols = 480, 270, 4
    rows = (len(linhas) + cols - 1) // cols
    img = Image.new('RGB', (W * cols, 40 + rows * (H + 50)), 'white'); d = ImageDraw.Draw(img)
    d.text((10, 6), f'{nome} · top por views (2 anos, longos) · mediana {int(med):,}'.replace(',', '.'), fill='black', font=fh)
    small = []
    for i, l in enumerate(linhas):
        x, y = (i % cols) * W, 40 + (i // cols) * (H + 50)
        try:
            t = Image.open(f'{OUT}/{l["thumb"]}').convert('RGB').resize((W, H))
        except Exception:
            t = Image.new('RGB', (W, H), 'gray')
        img.paste(t, (x, y)); small.append(t.resize((160, 90)))
        d.text((x + 4, y + H + 2), f'{l["views"]/1e6:.1f} mi · {l["x_mediana"]}x med · {l["publicado"]}', fill='black', font=fnt)
        d.text((x + 4, y + H + 24), l['titulo'][:44], fill='#333', font=fnt)
    img.save(f'{OUT}/mosaicos/{rotulo}.jpg', quality=78, optimize=True)
    if small:
        s = Image.new('RGB', (160 * cols + 6 * (cols - 1), 90 * ((len(small) + cols - 1) // cols) + 6 * (((len(small) + cols - 1) // cols) - 1)), 'white')
        for i, t in enumerate(small):
            s.paste(t, ((i % cols) * 166, (i // cols) * 96))
        s.save(f'{OUT}/mosaicos/{rotulo}-160.jpg', quality=85)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('grupo'); ap.add_argument('alvos', nargs='+'); ap.add_argument('--top', type=int, default=25)
    a = ap.parse_args(); yt = yt_client()
    for x in a.alvos:
        rot, alvo = x.split('=', 1)
        try:
            coleta(yt, a.grupo, rot, alvo, a.top)
        except Exception as e:
            print(f'{rot}: ERRO {type(e).__name__}: {str(e)[:200]}')
