import csv,os,sys
for s in sorted(os.listdir('q')):
  for k in ('pt','int'):
    f=f'q/{s}/{k}/refs.csv'
    R=[r for r in csv.DictReader(open(f)) if int(r['dur_s'] or 0)>=180]
    R.sort(key=lambda r:-int(r['views']))
    print(f'\n## {s}/{k}')
    for r in R[:int(sys.argv[1]) if len(sys.argv)>1 else 9]:
        v=int(r['views']);a=max(int(r['idade_d']),1)
        print(f"{v:>10,} {a:>5}d {v//a:>7,}/d {r['x_mediana'] or '-':>5}x {int(r['inscritos'] or 0):>9,} {r['id']} {r['canal'][:16]:16} {r['titulo'][:70]}")
