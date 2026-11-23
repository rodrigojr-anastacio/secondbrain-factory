#!/usr/bin/env python3
"""Fallback do `pesquisa_embalagem.py enriquecer` SEM a Data API (23/11/2026: o projeto GCP dos tokens
OAuth foi apagado e toda chamada videos.list devolve 403 "Project … has been deleted").

Só yt-dlp via WARP (socks5://127.0.0.1:40000), custo zero, cota zero:
  - views/duração/canal: das buscas flat em <saida>/busca/*.jsonl (já gravadas pelo `buscar`);
  - data de publicação: yt-dlp completo, só nos top-N por views (lento, ~3–6 s cada);
  - mediana do canal: aba /videos do canal (flat, últimos 40, longos ≥ min-dur; views arredondadas pelo YouTube).
Grava o mesmo refs.csv e medianas.json do script original (o `thumbs` funciona igual).

Uso: tools/.venv/bin/python skills/embalagem/scripts/enriquecer_ytdlp.py <saida> [--dias 400] [--top 40] [--min-dur 180]
"""
import argparse, csv, datetime, json, os, statistics, subprocess

ROOT = os.path.expanduser('~/workspace/fabrica-youtube')
YTDLP = f'{ROOT}/tools/.venv/bin/yt-dlp'
PROXY = 'socks5://127.0.0.1:40000'


def ytdlp_json(args, timeout=120):
    r = subprocess.run(['timeout', str(timeout), YTDLP, '--proxy', PROXY, '--dump-json', '--no-warnings', *args],
                       capture_output=True, text=True)
    out = []
    for l in r.stdout.splitlines():
        try: out.append(json.loads(l))
        except Exception: pass
    return out


def main():
    p = argparse.ArgumentParser(); p.add_argument('saida'); p.add_argument('--dias', type=int, default=400)
    p.add_argument('--top', type=int, default=40); p.add_argument('--min-dur', type=int, default=180)
    a = p.parse_args(); a.saida = os.path.abspath(a.saida)
    hoje = datetime.date.today()
    vids, rank, consultas = {}, {}, {}
    for fn in sorted(os.listdir(f'{a.saida}/busca')):
        q = fn[:-6].replace('_', ' ')
        for i, l in enumerate(open(f'{a.saida}/busca/{fn}')):
            try: d = json.loads(l)
            except Exception: continue
            if not d.get('id') or not d.get('channel_id'): continue
            vids[d['id']] = d
            rank[d['id']] = min(rank.get(d['id'], 99), i + 1)
            consultas.setdefault(d['id'], set()).add(q)
    cand = sorted([v for v in vids.values() if (v.get('duration') or 0) >= a.min_dur],
                  key=lambda v: -(v.get('view_count') or 0))[:a.top]
    cache_p = f'{a.saida}/datas.json'
    datas = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
    for v in cand:
        if v['id'] in datas: continue
        full = ytdlp_json(['--skip-download', f"https://www.youtube.com/watch?v={v['id']}"], 90)
        if full:
            ud = full[0].get('upload_date')
            datas[v['id']] = {'data': f'{ud[:4]}-{ud[4:6]}-{ud[6:]}' if ud else '', 'views': full[0].get('view_count'),
                              'inscritos': full[0].get('channel_follower_count')}
            json.dump(datas, open(cache_p, 'w'), indent=1)
    med_p = f'{a.saida}/medianas.json'
    med = json.load(open(med_p)) if os.path.exists(med_p) else {}
    linhas = []
    for v in cand:
        dd = datas.get(v['id'], {})
        data = dd.get('data') or ''
        idade = (hoje - datetime.date.fromisoformat(data)).days if data else ''
        linhas.append({'id': v['id'], 'link': f"https://youtu.be/{v['id']}", 'titulo': v.get('title'), 'canal': v.get('channel'),
                       'channel_id': v['channel_id'], 'inscritos': dd.get('inscritos') or '', 'data': data, 'idade_d': idade,
                       'dur_s': int(v.get('duration') or 0), 'views': int(dd.get('views') or v.get('view_count') or 0),
                       'rank': rank[v['id']], 'consultas': ' | '.join(sorted(consultas[v['id']]))})
    janela = [l for l in linhas if l['idade_d'] != '' and l['idade_d'] <= a.dias]
    for cid in {l['channel_id'] for l in janela} - set(med):
        ents = ytdlp_json(['--flat-playlist', '--playlist-end', '40', f'https://www.youtube.com/channel/{cid}/videos'], 120)
        longos = [int(e['view_count']) for e in ents if e.get('view_count') and (e.get('duration') or 0) >= a.min_dur][:30]
        if longos:
            nome = next((l['canal'] for l in janela if l['channel_id'] == cid), '')
            med[cid] = {'canal': nome, 'mediana': statistics.median(longos), 'n': len(longos), 'fonte': 'yt-dlp aba /videos'}
            json.dump(med, open(med_p, 'w'), ensure_ascii=False, indent=1)
    for l in linhas:
        m = med.get(l['channel_id'])
        l['mediana_canal'] = m['mediana'] if m else ''
        l['n_mediana'] = m['n'] if m else ''
        l['x_mediana'] = round(l['views'] / m['mediana'], 1) if m and m['mediana'] else ''
        l['na_janela'] = l in janela
    linhas.sort(key=lambda l: (not l['na_janela'], -l['views']))
    with open(f'{a.saida}/refs.csv', 'w') as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)
    print(f'candidatos {len(linhas)} · na janela {len(janela)} · medianas {len(med)} · cota Data API 0 (yt-dlp)')
    for l in linhas:
        print(f"{l['views']:>10,} {l['x_mediana']!s:>6}× {l['data']} {(l['canal'] or '')[:22]:22} {(l['titulo'] or '')[:80]}  {l['link']}")


if __name__ == '__main__':
    main()
