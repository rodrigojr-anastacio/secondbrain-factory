"""Busca no YouTube via WARP (yt-dlp, 0 cota): top N por consulta com views. Uso: busca.py saida.json 'consulta1' 'consulta2' ..."""
import json, subprocess, sys, concurrent.futures as cf
YT='/home/hermes/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp'
def q(s, n=20):
    r=subprocess.run([YT,'--proxy','socks5://127.0.0.1:40000','--flat-playlist','-J',f'ytsearch{n}:{s}'],capture_output=True,text=True,timeout=240)
    try: d=json.loads(r.stdout)
    except Exception: return s,[]
    return s,[{'id':e['id'],'t':e.get('title'),'v':e.get('view_count'),'canal':e.get('channel'),'dur':e.get('duration')} for e in d.get('entries',[])]
out={}
with cf.ThreadPoolExecutor(4) as ex:
    for s,vs in ex.map(q, sys.argv[2:]): out[s]=vs
json.dump(out,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
for s,vs in out.items():
    vv=sorted([v['v'] or 0 for v in vs],reverse=True)[:10]
    med=vv[len(vv)//2] if vv else 0
    print(f"\n### {s} | med top10 {med:,} | n={len(vs)}")
    for v in sorted(vs,key=lambda v:-(v['v'] or 0))[:6]:
        print(f"  {v['v'] or 0:>10,} {int(v['dur'] or 0)//60:>3}m {(v['canal'] or '')[:22]:22} {(v['t'] or '')[:75]}")
