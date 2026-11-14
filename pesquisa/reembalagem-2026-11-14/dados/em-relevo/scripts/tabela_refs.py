import json,csv
B='/home/hermes/workspace/fabrica-youtube/pesquisa/reembalagem-2026-11-14/dados/em-relevo/'
d=json.load(open(B+'busca-enriquecida.json'))['videos']; m=json.load(open(B+'medianas-canais.json'))
ex=json.load(open(B+'busca-extra.json'))
for L in ex['buscas'].values():
    for x in L: d.setdefault(x['id'],x)
med={v['nome']:v['mediana_longos'] for v in m.values()}
med.update({k:v[0] for k,v in ex['medianas'].items()})
bench={'xpBOF8FXXHM':('Chão do Sul',6620,'2026-10-24',735720,'Por que a Região Sul é o OPOSTO das outras regiões do Brasil?'),
'it5Vsv851Rc':('Mundo Entrópico',66000,'2026-09-11',511982,'Por que Existem Duas Guianas? (E o BRASIL Ficou com Uma)'),
'CMHf4Cqpcrs':('Mundo Entrópico',66000,'2026-10-30',447469,'O que está ACONTECENDO com SANTA CATARINA?!'),
'EGVFIQtvflg':('Mundo Entrópico',66000,'2026-10-23',258897,'Por que o RIO GRANDE DO SUL Vai Começar a ENCOLHER?'),
'pm0Pgr5BlqA':('Chão do Sul',6620,'2026-10-25',86860,'Tem um oceano escondido no Sul do Brasil que ninguém vê (Aquífero Guarani)'),
'31bbFdLrWaQ':('Mundo Entrópico',66000,'2026-08-28',104209,'O Nordeste Não É O Que Você Pensa...'),
'ZVgiR9yIcGo':('Um Documentário',130000,'2026-08-24',6923656,'A TRAGÉDIA DE MIYAKO: A cidade apagada por um Tsunami em poucos minutos'),
'GtUfbKNR_vA':('Um Documentário',130000,'2026-08-18',5315591,'A TRAGÉDIA DE YUNGAY: A cidade soterrada por uma montanha em três minutos')}
sul=['5UTQ4KrtVGc','7GE2xL75W7Q','obG4EMWkCcA','h04CSUPoKX0','j0aoIeu8Q3E','x_xE2HyxQE0','TfTiDfsKK04','_-eh-KSyaLU','9w1f8S44OpY','Kzo1yKN-O3w','0IsV6I7cI00','GflY4TuNV30','v7xUCFOQdxM','xpBOF8FXXHM','it5Vsv851Rc','CMHf4Cqpcrs','EGVFIQtvflg','pm0Pgr5BlqA','GtUfbKNR_vA','ZVgiR9yIcGo']
eln=['BAf4EYZ1AGk','mgPN8B-B7tg','tWhcTTC-pyw','_b_sGbjSVZQ','G27YUk3pVw8','ypzxfNnCVio','IGgMxhMxHao','C82XkHQNL4g','gkkqmtbOwmE','CCRYhINqJ3A','vXAT5va1NXI','6Wtb6MMWRZc','QJR4bu6BYHY','GnEXgEaYz1M','BpIY4ex2u6E','5445iKrArbY','0VYUw2UIUow','31bbFdLrWaQ']
w=csv.writer(open(B+'referencias.csv','w')); w.writerow(['video_nosso','id','link','canal','inscritos','views','data','v_por_insc','mediana_longos_canal','x_mediana','titulo'])
for nome,L in [('sul',sul),('el-nino',eln)]:
    for i in L:
        if i in bench: c,ins,dt,vw,t=bench[i]
        else: x=d[i]; c,ins,dt,vw,t=x['canal'],x['inscritos'],x['data'],x['views'],x['titulo']
        md=next((v for k,v in med.items() if k and c.startswith(k[:14])),None)
        w.writerow([nome,i,f'https://youtu.be/{i}',c,ins,vw,dt,round(vw/ins,2) if ins else '',md,round(vw/md,1) if md else '',t])
        print(nome,i,c[:20],ins,vw,dt,md,round(vw/md,1) if md else '-',t[:60])
