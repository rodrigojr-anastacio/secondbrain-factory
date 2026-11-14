"""Mediana de views dos últimos ~30 uploads longos (> 3 min, ≥ 3 dias) de cada canal das referências.
playlistItems (1 un.) + videos.list (1 un.) por canal. Saída: ../A-medianas.json e ../A-refs.csv"""
import json, os, sys, statistics, csv, datetime as dt
sys.path.insert(0, os.path.expanduser('~/workspace/fabrica-youtube/tools'))
from trends import yt_client, segundos
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = {
 'egito': 'apCvzsTn1qY GPt6u5mj74E nqX6vUmUNkA 7MDyiuw9wYI dPfV5_tDCzo yvWJVYTlIK0 alBh1Urra80 VCnluiYBm70 nF5MqHOzKiI cIx3xlhp8oQ 145bmb7lY3s 1LImwJdMRaA VQPzrVMHWlg WajgNhbbeHM y_JlppsyFok 47Kni-dhYZc',
 'india': 'CMMgNPVqU5k guiOxLd8X3M z4FQoGlOKUQ DKsoFxY3evU QtWeAxjZZHg aTMlPlcAzns zMemC8hSMO8 088WI1DJHac p9IIGdg91fE syocq98pAy8 lsnVzqwSjtk 3zHMKPpSHWA z0l8Dm5f2pY',
 'china': 'deEXaVt3EgE NCr1f_SUsLk GSFdoWs0NYo SYsIldcDB_w 12n3uoyIbvQ jS_Ca-opiHM tzfbDkQx7Hw As5HdY_D-uI 78iv9U6GV6c fXuWQg7uJKg Fbz4QYZ5XrI wuhnBi8jNl0 EOA5-VFVI-g jpT0bK1EpUM',
 'brasil': 'qWPL11MOzOg QTjecFwrzbs sD0cIJ8JMYw WcXwgbvbKMY iCiM_67Vj7w jPkK_uwJXJs s63x3TssYnI V3lV3IlA9hk p0t7j7ish_E CExWqlfYHkU UfGD0lqHObI RH30MX3g5Rg EpkMOT35IQ8',
 'padrao': 'HCzD29KIlo4 52TY3RdXIaM uEDDMWJ04Vo XyX7Y-xyhyg kZ3YWuGWF0k 9-MUCj3AJ80 5n_KfzZcN3s',
}
yt = yt_client()
V = json.load(open(os.path.join(BASE, 'A-videos.json')))
C = json.load(open(os.path.join(BASE, 'A-canais.json')))
falta = [i for t in REFS.values() for i in t.split() if i not in V]
if falta: print('FALTA', falta)
chs = sorted({V[i]['canal_id'] for t in REFS.values() for i in t.split() if i in V})
pm = os.path.join(BASE, 'A-medianas.json'); MED = json.load(open(pm)) if os.path.exists(pm) else {}
hoje = dt.datetime(2026, 11, 14, tzinfo=dt.timezone.utc); un = 0
for ch in chs:
    if ch in MED: continue
    up = C[ch]['uploads']
    try:
        r = yt.playlistItems().list(part='contentDetails', playlistId=up, maxResults=50).execute(); un += 1
    except Exception as e:
        MED[ch] = {'erro': str(e)[:80]}; continue
    ids = [x['contentDetails']['videoId'] for x in r['items']]
    r = yt.videos().list(part='statistics,contentDetails,snippet', id=','.join(ids), maxResults=50).execute(); un += 1
    longs = []
    for it in r['items']:
        pub = dt.datetime.fromisoformat(it['snippet']['publishedAt'].replace('Z', '+00:00'))
        if segundos(it['contentDetails'].get('duration','PT0S')) > 180 and (hoje - pub).days >= 3:
            longs.append((pub, int(it['statistics'].get('viewCount', 0))))
    longs.sort(reverse=True); longs = longs[:30]
    MED[ch] = {'nome': C[ch]['nome'], 'n': len(longs), 'mediana': statistics.median([v for _, v in longs]) if longs else None}
json.dump(MED, open(pm, 'w'), ensure_ascii=False, indent=1)
with open(os.path.join(BASE, 'A-refs.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['tema', 'id', 'link', 'canal', 'inscritos', 'views', 'data', 'idade_d', 'v_por_insc', 'mediana_canal', 'n_mediana', 'acima_mediana', 'dur_min', 'titulo'])
    for t, s in REFS.items():
        for i in s.split():
            if i not in V: continue
            v = V[i]; m = MED.get(v['canal_id'], {})
            med = m.get('mediana')
            w.writerow([t, i, f'https://youtu.be/{i}', v['canal'], v['inscritos'], v['views'], v['data'], v['idade_d'], v['v_por_insc'], med, m.get('n'), ('sim' if med is not None and v['views'] > med else 'não' if med is not None else '?'), v['dur_s'] // 60, v['titulo']])
print('unidades', un)
