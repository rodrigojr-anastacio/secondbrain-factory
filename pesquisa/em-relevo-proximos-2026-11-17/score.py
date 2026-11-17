import csv,os,sys,statistics
D=sys.argv[1]
rows=[]
for t in sorted(os.listdir(f'{D}/scan')):
    f=f'{D}/scan/{t}/refs.csv'
    if not os.path.exists(f): continue
    R=[r for r in csv.DictReader(open(f)) if r['na_janela']=='True']
    for r in R:
        r['views']=int(r['views']); r['ins']=int(r['inscritos'] or 0); r['x']=float(r['x_mediana']) if r['x_mediana'] else None; r['id_']=int(r['idade_d'])
    v=[r['views'] for r in R]
    big=[r for r in R if r['x'] and r['x']>=5 and r['ins']<=500000 and r['views']>=20000]
    big90=[r for r in R if r['id_']<=90 and r['views']>=20000]
    top=sorted(R,key=lambda r:-r['views'])[:3]
    rows.append((t,len(R),sum(1 for x in v if x>=100000),sum(1 for x in v if x>=500000),len(big),len(big90),max(v) if v else 0, top, big))
rows.sort(key=lambda r:(-r[4],-r[2]))
print('tema | n12m | ≥100k | ≥500k | ≥5×med(peq/méd,≥20k) | ≥20k em 90d | max')
for t,n,a,b,c,d,m,top,big in rows:
    print(f'{t:14} {n:3} {a:3} {b:3} {c:3} {d:3} {m:>10,}')
for t,n,a,b,c,d,m,top,big in rows[:14]:
    print('\n##',t)
    for r in sorted(big,key=lambda r:-r['x'])[:6]:
        print(f"  {r['views']:>9,} {r['x']:>5}× ins{r['ins']:>8,} {r['data']} {r['canal'][:20]:20} {r['titulo'][:75]} {r['id']}")
