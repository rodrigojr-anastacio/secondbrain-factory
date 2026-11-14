"""Mediana dos últimos ≤30 uploads longos (≥3 min) dos canais citados que faltaram. Só leitura (playlistItems + videos.list)."""
import sys, os, json, csv, statistics
sys.path.insert(0, os.path.expanduser('~/workspace/fabrica-youtube/tools'))
from trends import yt_client, segundos
B = os.path.dirname(os.path.abspath(__file__)) + '/..'
yt = yt_client()
dados = json.load(open(B + '/canais-medianas.json'))
rows = list(csv.DictReader(open(B + '/busca-enriquecida.csv')))
ids = sys.argv[1:]
cid_por_vid = {r['id']: r['channel_id'] for r in rows}
cota = 0
for vid in ids:
    cid = cid_por_vid[vid]
    if cid in dados['medianas']: continue
    up = dados['canais'][cid]['uploads']
    pl = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50).execute(); cota += 1
    vs = [it['contentDetails']['videoId'] for it in pl['items']]
    out = yt.videos().list(part='statistics,contentDetails', id=','.join(vs)).execute(); cota += 1
    longos = [int(x['statistics'].get('viewCount', 0)) for x in out['items'] if segundos(x['contentDetails'].get('duration', 'PT0S')) >= 180][:30]
    if longos: dados['medianas'][cid] = {'mediana': statistics.median(longos), 'n': len(longos)}
    print(dados['canais'][cid]['nome'], dados['medianas'].get(cid))
for r in rows:
    m = dados['medianas'].get(r['channel_id'])
    if m:
        r['mediana_canal'] = m['mediana']; r['n_mediana'] = m['n']; r['acima_mediana'] = int(r['views']) > m['mediana']
dados['cota_unidades'] += cota
json.dump(dados, open(B + '/canais-medianas.json', 'w'), ensure_ascii=False, indent=1)
with open(B + '/busca-enriquecida.csv', 'w') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('cota extra', cota)
