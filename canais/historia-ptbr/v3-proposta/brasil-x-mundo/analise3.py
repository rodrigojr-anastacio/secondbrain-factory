import json,re,statistics as st
exec(open("analise2.py").read().split("def run")[0])
V=json.load(open("vids.json")); B=json.load(open("busca.json"))
C=json.load(open("/home/hermes/cache/tmp/v3pesq/corpus.json"))
ok=lambda v: v["data"]>="2026-01-01" and v["seg"]>=300 and (not v.get("lang") or v["lang"].startswith("pt")) and FMT.search(v["titulo"]) and (v.get("subs") or 0)<1000000
print("== por termo, só vídeos no formato e canal<1mi ==")
for b in B:
    l=[V[i] for i in b["ids"] if i in V and ok(V[i])]
    if l: print(b["grupo"],f'{b["termo"][:55]:55}',stats(l))
U={v["id"]:v for v in list(V.values())+C if ok(v)}
YOU=re.compile(r"\bvocê\b|\bsua vida\b|\bseu dia\b",re.I)
print("== 2a pessoa (união nova+corpus) ==")
G={}
for v in U.values():
    if YOU.search(v["titulo"]): G.setdefault(cls(v["titulo"]),[]).append(v)
for k,l in G.items():
    print(k,stats(l))
    for v in sorted(l,key=lambda x:-x["views"])[:8]: print(f'   {v["views"]:>8} {v.get("subs") or 0:>7} {v["canal"][:20]:20} {v["titulo"][:80]}')
print("== total união ==")
G={}
for v in U.values(): G.setdefault(cls(v["titulo"]),[]).append(v)
for k,l in G.items(): print(k,stats(l))
