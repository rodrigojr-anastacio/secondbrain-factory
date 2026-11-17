import csv,re,sys,glob
pat=re.compile(sys.argv[2],re.I); seen=set(); R=[]
for f in glob.glob(f'q/{sys.argv[1]}/*/refs.csv'):
    for r in csv.DictReader(open(f)):
        if r['id'] in seen or int(r['dur_s'] or 0)<180: continue
        seen.add(r['id']); R.append(r)
n=int(sys.argv[3]) if len(sys.argv)>3 else 20
for r in sorted(R,key=lambda r:-int(r['views'])):
    if pat.search(r['titulo']):
        v=int(r['views']);a=max(int(r['idade_d']),1)
        print(f"{v:>10,} {r['data']} {v//a:>6,}/d {r['x_mediana'] or '-':>6}x {int(r['inscritos'] or 0):>10,} {r['id']} {r['canal'][:18]:18} {r['titulo'][:80]}")
        n-=1
        if not n: break
