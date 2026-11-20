#!/usr/bin/env python3
"""Pesquisa "a história que ninguém conta" (historia-ptbr, 20/11/2026). Só leitura, custo zero.

1. Buscas yt-dlp via WARP (ytsearch, flat) para as consultas de consultas.json → dados/busca/<q>.jsonl
2. videos.list (data, views, duração) dos resultados → dados/videos.json
3. Mediana real de cada canal (últimos 30 longos com >= 7 dias; playlistItems + videos.list) → dados/canais.json
Nunca usa search.list. Nunca imprime tokens. Nada em /tmp.
Uso: tools/.venv/bin/python coleta.py [buscas|videos|canais|tudo]
"""
import concurrent.futures as cf, datetime, hashlib, json, os, statistics, subprocess, sys
ROOT = os.path.expanduser('~/workspace/fabrica-youtube')
OUT = f'{ROOT}/pesquisa/historia-nao-contada-2026-11-20'
D = f'{OUT}/dados'
YTDLP = f'{ROOT}/tools/.venv/bin/yt-dlp'
sys.path.insert(0, f'{ROOT}/tools')
from trends import yt_client, segundos  # noqa

N = int(os.environ.get('N', '40'))


def qfile(q, lang):
    return f'{D}/busca/{lang}-' + hashlib.md5(q.encode()).hexdigest()[:10] + '.jsonl'


def busca(item):
    q, lang = item['q'], item['lang']
    f = qfile(q, lang)
    if os.path.exists(f) and os.path.getsize(f) > 100:
        return q, 'cache'
    hl = {'pt': 'pt', 'es': 'es', 'en': 'en'}[lang]
    p = subprocess.run(['timeout', '200', YTDLP, '--proxy', 'socks5://127.0.0.1:40000', '--extractor-args',
                        f'youtube:lang={hl}', '--flat-playlist', '--dump-json', f'ytsearch{N}:{q}'],
                       capture_output=True, text=True)
    linhas = []
    for l in p.stdout.splitlines():
        try:
            d = json.loads(l)
        except Exception:
            continue
        linhas.append(json.dumps({k: d.get(k) for k in ('id', 'title', 'channel', 'channel_id', 'view_count', 'duration')},
                                 ensure_ascii=False))
    with open(f, 'w') as fh:
        fh.write('\n'.join(linhas))
    return q, len(linhas)


def buscas():
    os.makedirs(f'{D}/busca', exist_ok=True)
    cons = json.load(open(f'{OUT}/scripts/consultas.json'))
    with cf.ThreadPoolExecutor(4) as ex:
        for q, n in ex.map(busca, cons):
            print(q, n, flush=True)


def videos():
    cons = json.load(open(f'{OUT}/scripts/consultas.json'))
    ids = {}
    for c in cons:
        f = qfile(c['q'], c['lang'])
        if not os.path.exists(f):
            continue
        for pos, l in enumerate(open(f).read().splitlines()):
            if not l.strip():
                continue
            d = json.loads(l)
            if (d.get('duration') or 0) < 180:
                continue
            ids.setdefault(d['id'], []).append({'q': c['q'], 'lang': c['lang'], 'tipo': c['tipo'],
                                                'pais': c.get('pais', ''), 'pos': pos + 1})
    cache = json.load(open(f'{D}/videos.json')) if os.path.exists(f'{D}/videos.json') else {}
    falta = [i for i in ids if i not in cache]
    yt = yt_client()
    for i in range(0, len(falta), 50):
        for v in yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(falta[i:i + 50])).execute()['items']:
            cache[v['id']] = {'titulo': v['snippet']['title'], 'canal': v['snippet']['channelTitle'],
                              'canal_id': v['snippet']['channelId'], 'publicado': v['snippet']['publishedAt'][:10],
                              'views': int(v['statistics'].get('viewCount', 0) or 0),
                              'dur_s': segundos(v['contentDetails'].get('duration','PT0S')),
                              'idioma': v['snippet'].get('defaultAudioLanguage') or v['snippet'].get('defaultLanguage') or ''}
    for k, v in cache.items():
        if k in ids:
            v['consultas'] = ids[k]
    json.dump(cache, open(f'{D}/videos.json', 'w'), ensure_ascii=False, indent=0)
    print('videos', len(cache), 'novos', len(falta))


def mediana_canal(yt, cid):
    r = yt.channels().list(part='statistics,contentDetails', id=cid).execute()
    if not r.get('items'):
        return None
    c = r['items'][0]
    upl = c['contentDetails']['relatedPlaylists']['uploads']
    ids, tok = [], None
    for _ in range(int(os.environ.get('PAGINAS','1'))):
        try:
            rr = yt.playlistItems().list(part='contentDetails', playlistId=upl, maxResults=50, pageToken=tok).execute()
        except Exception:
            break
        ids += [it['contentDetails']['videoId'] for it in rr['items']]
        tok = rr.get('nextPageToken')
        if not tok:
            break
        # basta ter ~30 longos; checa depois
        if len(ids) >= 100:
            break
    hoje = datetime.date.today()
    longos = []
    for i in range(0, len(ids), 50):
        for v in yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i + 50])).execute()['items']:
            if segundos(v['contentDetails'].get('duration','PT0S')) < 180:
                continue
            d = v['snippet']['publishedAt'][:10]
            if (hoje - datetime.date.fromisoformat(d)).days < 7:
                continue
            longos.append((d, int(v['statistics'].get('viewCount', 0) or 0)))
    longos.sort(reverse=True)
    l30 = [x[1] for x in longos[:30]]
    return {'inscritos': int(c['statistics'].get('subscriberCount', 0) or 0),
            'videos_total': int(c['statistics'].get('videoCount', 0) or 0),
            'mediana_30': statistics.median(l30) if l30 else 0, 'n_longos': len(l30),
            'primeiro_longo_amostra': longos[-1][0] if longos else ''}


def canais():
    vs = json.load(open(f'{D}/videos.json'))
    corte = datetime.date.today() - datetime.timedelta(days=730)
    alvo = sorted({v['canal_id'] for v in vs.values()
                   if datetime.date.fromisoformat(v['publicado']) >= corte and v.get('consultas')})
    cache = json.load(open(f'{D}/canais.json')) if os.path.exists(f'{D}/canais.json') else {}
    falta = [c for c in alvo if c not in cache]
    print('canais alvo', len(alvo), 'faltam', len(falta), flush=True)
    import threading
    loc = threading.local()

    def um(cid):
        if not hasattr(loc, 'yt'):
            loc.yt = yt_client()
        try:
            return cid, mediana_canal(loc.yt, cid)
        except Exception as e:
            return cid, {'erro': str(e)[:120]}
    with cf.ThreadPoolExecutor(8) as ex:
        for n, (cid, r) in enumerate(ex.map(um, falta)):
            cache[cid] = r
            if n % 50 == 0:
                json.dump(cache, open(f'{D}/canais.json', 'w'), indent=0)
                print(n, flush=True)
    json.dump(cache, open(f'{D}/canais.json', 'w'), indent=0)
    print('canais', len(cache))


if __name__ == '__main__':
    etapa = sys.argv[1] if len(sys.argv) > 1 else 'tudo'
    if etapa in ('buscas', 'tudo'):
        buscas()
    if etapa in ('videos', 'tudo'):
        videos()
    if etapa in ('canais', 'tudo'):
        canais()
