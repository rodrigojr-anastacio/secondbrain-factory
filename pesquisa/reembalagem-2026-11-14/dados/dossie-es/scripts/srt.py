import sys,re
t=open(sys.argv[1]).read().strip().split('\n\n')
out=[]
for b in t:
    l=b.split('\n')
    if len(l)<3: continue
    m=re.match(r'(\d+):(\d+):(\d+)',l[1]); s=int(m[1])*3600+int(m[2])*60+int(m[3])
    out.append(f'{s//60}:{s%60:02d} '+' '.join(l[2:]))
print('\n'.join(out))
