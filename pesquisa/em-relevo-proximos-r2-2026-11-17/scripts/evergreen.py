"""Cruza snap1/snap2 (views agora) com idade -> views/dia hoje vs. média da vida; agrega por pergunta -> evergreen.csv e banco.csv."""
import json,glob,csv,datetime,statistics
s1=json.load(open('snap1.json')); s2=json.load(open('snap3.json'))
t1=datetime.datetime.fromisoformat(s1['ts']); t2=datetime.datetime.fromisoformat(s2['ts']); h=(t2-t1).total_seconds()/3600
med={}; ins={}
for f in glob.glob('q/*/*/medianas.json'): med.update(json.load(open(f)))
for f in glob.glob('q/*/*/refs.csv'):
    for r in csv.DictReader(open(f)): ins[r['channel_id']]=int(r['inscritos'] or 0)
for k,v in json.load(open('medianas_extra.json')).items(): med[k]=v; ins[k]=v['inscritos']
PT=lambda t: any(w in t.lower() for w in (' o ',' a ',' do ',' da ','por que','porque','não','pode','brasil','e se','barragens','tsunami no','ferrovias','trens')) and not any(w in t.lower() for w in ('¿','why','what','the ','warum'))
hoje=t2.date(); linhas=[]
for l in open('evidencias.tsv'):
    slug,ids=l.rstrip('\n').split('\t')
    for i in ids.split():
        a=s1['v'].get(i); b=s2['v'].get(i)
        if not a or not b: continue
        pub=datetime.date.fromisoformat(a['pub'][:10]); idade=max((hoje-pub).days,1)
        vd_hoje=round((b['views']-a['views'])/h*24) if h>0 else ''
        vd_med=round(b['views']/idade)
        m=med.get(a['channel_id'],{}).get('mediana')
        linhas.append({'pergunta':slug,'id':i,'link':f'https://youtu.be/{i}','titulo':a['titulo'],'canal':a['canal'],'inscritos':ins.get(a['channel_id'],''),
            'idioma':'pt' if PT(a['titulo']) else 'en/es','data':str(pub),'idade_d':idade,'views':b['views'],'views_dia_media':vd_med,'views_dia_hoje':vd_hoje,
            'hoje_sobre_media':round(vd_hoje/vd_med,2) if vd_med and vd_hoje!='' else '','mediana_canal':m or '','x_mediana':round(b['views']/m,1) if m else ''})
with open('evergreen.csv','w') as f:
    w=csv.DictWriter(f,fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)
agg={}
for r in linhas:
    a=agg.setdefault(r['pergunta'],{'n':0,'n_1ano_100k':0,'canais_1ano_100k':set(),'anos_hits':set(),'pt_1ano_100k':0,'vivos':0,'soma_hoje_1ano':0})
    a['n']+=1
    if r['idade_d']>=365 and r['views']>=100000:
        a['n_1ano_100k']+=1; a['canais_1ano_100k'].add(r['canal']); a['anos_hits'].add(r['data'][:4])
        if r['idioma']=='pt': a['pt_1ano_100k']+=1
        a['soma_hoje_1ano']+=r['views_dia_hoje'] or 0
        if r['hoje_sobre_media']!='' and r['hoje_sobre_media']>=0.3: a['vivos']+=1
json.dump({k:{**v,'canais_1ano_100k':len(v['canais_1ano_100k']),'anos_hits':sorted(v['anos_hits'])} for k,v in agg.items()},open('evergreen_agg.json','w'),ensure_ascii=False,indent=1)
print(f'janela entre snapshots: {h:.2f} h')
for k,v in sorted(agg.items(),key=lambda x:-x[1]['soma_hoje_1ano']):
    print(f"{k:22} ≥1ano&≥100k={v['n_1ano_100k']:2} canais={len(v['canais_1ano_100k']):2} pt={v['pt_1ano_100k']:2} anos={','.join(sorted(v['anos_hits']))} vivos(hoje≥0,3×média)={v['vivos']} soma_views/dia_hoje={v['soma_hoje_1ano']:,}")
