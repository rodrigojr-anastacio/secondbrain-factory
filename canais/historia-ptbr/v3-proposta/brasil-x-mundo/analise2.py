import json,re,statistics as st,sys
FMT=re.compile(r"como era|assim era|assim foi|como (as pessoas|os \w+|eram) (viviam|vivia|sobreviv)|um dia (na vida|como|inteiro)|sobreviv|\bvocê\b|sua vida|vida (de|no|na|dos|das|em)|viver (no|na|em)|\b1\d\d\d\s*[:|—-]|instantes antes|momentos antes|o dia em que|\bera (o|a) vida",re.I)
BR=re.compile(r"brasil|brasileir|rio de janeiro|são paulo|sao paulo|salvador|recife|bahia|minas|ouro preto|vila rica|colonial|império do brasil|dom pedro|d\. pedro|pedro ii|dom joão|1808|bandeirant|tropeir|cabral|engenho|cangaç|lampião|canudos|amazôn|seringuei|sertão|pracinha|\bfeb\b|petrópolis|paulista|carioca|favela|tupi|guarani|indígena|índios|nordest|sorocaba|santos dumont|getúlio|ditadura|carapicuíba|londrina|caraguatatuba|joelma|alagoas|óbidos|curitiba|porto alegre|belém|manaus|fortaleza|brasília",re.I)
REC=re.compile(r"anos (50|60|70|80|90)|19[5-9]\d|20[0-2]\d|nostalgia|ditadura|instantes antes|momentos antes",re.I)
def cls(t):
    if BR.search(t): return "BR-recente" if REC.search(t) else "BR-historico"
    return "MUNDO"
def stats(l):
    vs=sorted([x["views"] for x in l],reverse=True)
    if not vs: return "n=0"
    small=[x for x in l if (x.get("subs") or 0)<50000 and x["views"]>=100000]
    top10=vs[:10]
    return f'n={len(l):3} canais={len({x["cid"] for x in l}):3} mediana={int(st.median(vs)):>7} p75={vs[len(vs)//4]:>7} >=100k={sum(1 for x in vs if x>=100000):3} ({round(100*sum(1 for x in vs if x>=100000)/len(vs))}%) peq<50k&>=100k={len(small):2} mediana_top10={int(st.median(top10)):>7}'
def run(nome,L):
    print("=====",nome)
    G={}
    for v in L: G.setdefault(cls(v["titulo"]),[]).append(v)
    for k in ["MUNDO","BR-historico","BR-recente"]: print(f"  {k:13}",stats(G.get(k,[])))
    return G
# 1) busca balanceada nova
V=json.load(open("vids.json"))
L=[v for v in V.values() if v["data"]>="2026-01-01" and v["seg"]>=300 and (not v["lang"] or v["lang"].startswith("pt")) and FMT.search(v["titulo"]) and (v["subs"] or 0)<1000000]
G1=run("busca balanceada 28/11 (36 termos 18×18, filtro 'este ano', formato, pt, ≥5 min, canal <1 mi)",L)
# 2) corpus antigo
C=json.load(open("/home/hermes/cache/tmp/v3pesq/corpus.json"))
G2=run("corpus 846 (12 meses, formato; viés: 2/3 das buscas eram de tema BR)",C)
C26=[x for x in C if x["data"]>="2026-01-01"]
run("corpus 846 só 2026",C26)
for nome,G in [("nova",G1)]:
  for k in ["MUNDO","BR-historico"]:
    print("--- top",k,nome)
    for v in sorted(G[k],key=lambda x:-x["views"])[:20]:
        print(f'  {v["views"]:>8} {v["subs"] or 0:>7} {v["data"]} {v["canal"][:20]:20} {v["titulo"][:85]}')
