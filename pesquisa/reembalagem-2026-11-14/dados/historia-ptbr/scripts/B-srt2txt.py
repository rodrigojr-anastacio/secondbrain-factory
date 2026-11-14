import sys,re
t=open(sys.argv[1],encoding='utf-8').read().strip().split('\n\n')
for b in t:
    l=b.strip().split('\n')
    if len(l)<3: continue
    ts=l[1].split(' --> ')[0][:8]
    print(ts[3:],' '.join(l[2:]))
