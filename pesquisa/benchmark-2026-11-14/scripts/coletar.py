"""Benchmark 28 d das referências (14/11/2026). Data API (token lotr-fr, igual trends.py); só leitura.
Uso: tools/.venv/bin/python coletar.py <saida.json>"""
import json, sys, re, datetime as dt, os
sys.path.insert(0, '/home/hermes/workspace/fabrica-youtube/tools')
from trends import yt_client
HOJE = dt.datetime(2026, 11, 14, 12, tzinfo=dt.timezone.utc)
VID_RESOLVER = {  # canal descoberto por um vídeo que nos manda tráfego
 'History Easy Guide': 'sD0cIJ8JMYw', 'História Inteira': 'WcXwgbvbKMY', 'Toda História em Minutos': 'bVcbJkl-vC0',
 'Archivo en Minutos': 'ocy82l2nWhM', 'Archivo Desclasificado': 'CZdoq4448QQ',
}
GRUPOS = {
 'historia-ptbr': {
  'History in Minutes': ('UCYjRQ6T2BxBnJtPytI9OnNg', 'principal'), 'Genius History': ('UC-q0RDBWjYlYA2KkPzq0WSQ', 'principal'),
  'CountryCorns': ('UCKWRnsyYbPFgWclCF0_yOTw', 'similar'),
  'História em minutos (clone 08/2026)': ('UCuquAW2-sxlV0G4N9RuvqaQ', 'clone-pt'), 'A HISTORIA EM MINUTOS': ('UCSNvRxMppnEfGEHha2vM1Wg', 'clone-pt'),
  'History Easy Guide': (None, 'clone-pt'), 'História Inteira': (None, 'clone-pt'), 'Toda História em Minutos': (None, 'clone-pt'),
  'História em Minutos (clone 10/2026a)': ('UCyOrXqAEQpKKHreTYqOqdEw', 'clone-pt'), 'História em Minutos (clone 10/2026b)': ('UCvVuEJAqFAgqtn1IbA11UQw', 'clone-pt'),
  'História em Minutos (clone 10/2026c)': ('UCTJ5pQhUbm6CyszLfqR8Urg', 'clone-pt'), 'História em Minutos (5eT)': ('UC5eTe96eJuE4gkyJ5IQ5Fww', 'clone-pt'),
 },
 'dossie-es': {
  'Archive in Minutes': ('UCFp0Rk-ad8JD78Qw9nEJ29w', 'principal'), 'Atlas del Tiempo': ('UCku9KB11TReyHHC1kK9CCEw', 'principal'),
  'Te lo Pinto': ('UCrkONla60pQPsppl7PPDHyQ', 'similar'), 'Spies in Minutes': ('UC8a5fGoL5nfy5qdeup7mFGw', 'clone-en'),
  'Archivos en Minutos': ('UCbsAjBx3waufmBhdZSwFMGQ', 'clone-es'), 'Archivo en Minutos': (None, 'clone-es'),
  'Mapa del Ayer': ('UC4A_eQiXs8-ESgVmyxNUMGw', 'clone-es'), 'Historia Total': ('UC6ZUELsUCkrHF5ZO4m4hpMQ', 'clone-es'),
  'Archivo Desclasificado': (None, 'similar'),
 },
 'em-relevo': {
  'Mundo Entrópico': ('UCfM8cvYaVCsz9NgyKMRVFNw', 'principal'), 'Chão do Sul': ('UCQZJSIL-0P-eL25pwLLbJFg', 'principal'),
  'Mapa Verso': ('UC734965gYfz7LPY2QQ66cVg', 'similar'), 'The Last Day': ('UCN6XxorahzAiDNyRnI1of2g', 'clone-en'),
  'Um Documentário': ('UCcK9yDz5INb1Q9Tw82ICeVQ', 'similar'), 'Astrum Earth': ('UCWBtLCE-BnzZx3DneqDiXWQ', 'similar'),
  'Geografia con Geoff': ('UCcWOL02JEjNmxcU6UVDqEPg', 'similar'),
 },
 'lugares-guerra-en': {
  'Where They Stood': ('UCUt7wPSxHRObHObdAW-26JQ', 'principal'), 'Civil War Fine Print': ('UCE1gBqF9TF6JswS0zsxdGTg', 'principal'),
  'Ship Tales': ('UCBPScyNOC9MUXSvRIg6Rs1Q', 'clone-en'), 'Long After The Guns': ('UCXIMjn_vXy3W2_hb2c25HJw', 'clone-en'),
  'Forgotten Fleet': ('UCyL5J-lo3XuYPPOiXvzbAWw', 'similar'), 'Cloaked History': ('UCyTRQd_sRvD7yYBQLL2G66Q', 'similar'),
  'Insight Ship': ('UC85c3UiXENXF8KvSh61jk4A', 'similar'),
 },
 'nossos': {
  'historia-ptbr': ('UCpw08sVZG1QZp-3spPcwWxQ', 'nosso'), 'dossie-es': ('UCVCYqeuCwTWC7Lqez_qeWRA', 'nosso'),
  'em-relevo': ('UCXw-Q07-pIPlwMX9ypuLN0A', 'nosso'), 'lugares-guerra-en': ('UCou1N3ySJ_9mX6NY_pIM0Aw', 'nosso'),
 },
}
def seg(iso):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso or '')
    if not m: return 0
    d, h, mi, s = (int(x or 0) for x in m.groups()); return d*86400 + h*3600 + mi*60 + s
yt = yt_client(); custo = 0
def call(req):
    global custo; custo += 1; return req.execute()
r = call(yt.videos().list(part='snippet', id=','.join(VID_RESOLVER.values())))
vid2cid = {i['id']: i['snippet']['channelId'] for i in r['items']}
for g in GRUPOS.values():
    for n, (cid, papel) in list(g.items()):
        if cid is None: g[n] = (vid2cid.get(VID_RESOLVER[n]), papel)
out = {'gerado': HOJE.isoformat(), 'grupos': {}}
for grupo, canais in GRUPOS.items():
    out['grupos'][grupo] = {}
    for nome, (cid, papel) in canais.items():
        if not cid: print('sem id', nome, file=sys.stderr); continue
        ch = call(yt.channels().list(part='snippet,statistics,contentDetails', id=cid))['items'][0]
        up = ch['contentDetails']['relatedPlaylists']['uploads']
        nvid = int(ch['statistics'].get('videoCount', 0))
        ids, tok, paginas, fim = [], None, 0, False
        # pequenos: tudo (até 600) p/ achar o 1º vídeo; grandes: só até passar 90 dias
        while True:
            pr = call(yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50, pageToken=tok)); paginas += 1
            for it in pr['items']:
                ids.append((it['contentDetails']['videoId'], it['contentDetails'].get('videoPublishedAt')))
            tok = pr.get('nextPageToken')
            ult = ids[-1][1] if ids else None
            velho = ult and (HOJE - dt.datetime.fromisoformat(ult.replace('Z', '+00:00'))).days > 95
            if not tok or paginas >= 12 or (velho and nvid > 600): break
        completo = not tok
        vids = []
        for i in range(0, len(ids), 50):
            lote = [x[0] for x in ids[i:i+50]]
            vr = call(yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(lote)))
            for v in vr['items']:
                pub = dt.datetime.fromisoformat(v['snippet']['publishedAt'].replace('Z', '+00:00'))
                st = v['statistics']; d = seg(v['contentDetails'].get('duration'))
                vids.append({'id': v['id'], 'titulo': v['snippet']['title'], 'publicado': pub.isoformat(),
                    'dur_s': d, 'short': d <= 180, 'views': int(st.get('viewCount', 0)), 'likes': int(st.get('likeCount', 0) or 0),
                    'coments': int(st.get('commentCount', 0) or 0), 'idade_d': round((HOJE - pub).total_seconds()/86400, 2),
                    'thumb': (v['snippet']['thumbnails'].get('maxres') or v['snippet']['thumbnails'].get('high') or {}).get('url'),
                    'lang': v['snippet'].get('defaultAudioLanguage')})
        vids.sort(key=lambda x: x['publicado'])
        out['grupos'][grupo][nome] = {'cid': cid, 'papel': papel, 'handle': ch['snippet'].get('customUrl'),
            'criado': ch['snippet']['publishedAt'], 'inscritos': int(ch['statistics'].get('subscriberCount', 0)),
            'views_total': int(ch['statistics'].get('viewCount', 0)), 'n_videos': nvid, 'lista_completa': completo,
            'primeiro_video': vids[0]['publicado'] if (vids and completo) else None, 'videos': vids}
        print(grupo, nome, ch['statistics'].get('subscriberCount'), len(vids), 'completo' if completo else '', file=sys.stderr)
out['custo_unidades'] = custo
json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('unidades', custo, file=sys.stderr)
