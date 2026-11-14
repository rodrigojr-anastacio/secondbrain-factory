import sys, json, statistics, re
sys.path.insert(0,'/home/hermes/workspace/fabrica-youtube/tools')
from trends import yt_client
yt=yt_client()
B='/home/hermes/workspace/fabrica-youtube/pesquisa/reembalagem-2026-11-14/dados/em-relevo/'
d=json.load(open(B+'busca-enriquecida.json'))
nomes=["Professor Vulcano","Natureza Sinistra","Além do Mapa","PBS Terra","Prof. Rogerdautry","Canal Vilão","Cosmos Oculto","Sou curioso?!","Refúgio Cortes","Olá, Ciência!","100% Atômico","Prof. JeanGrafia | Gabaritando Geografia","Fatos Desconhecidos","Investidor Sardinha | Raul Sena","Paulo Jubilut","Manual do Mundo","SpaceCast","Sacani Cortes","Astrum Earth","StarTalk","The Secrets of the Universe","O Cara Explica","William Batista TV","Lucas Moura - Brazil Storm Chaser","Arquivo da Tragédia","Will Bratton","Brasil Urgente","Band Paraná","g1","Ei Nerd","Pânico Retrô"]
chans={}
for cid,c in d['canais'].items():
    for n in nomes:
        if c['nome'].startswith(n[:14]): chans[cid]=c
# + Chão do Sul e Mundo Entrópico
r=yt.videos().list(part='snippet',id='xpBOF8FXXHM,CMHf4Cqpcrs,2WH4ducITO0').execute()
extra=[it['snippet']['channelId'] for it in r['items']]
r=yt.channels().list(part='statistics,contentDetails,snippet',id=','.join(extra)).execute()
for it in r['items']:
    chans[it['id']]=dict(nome=it['snippet']['title'],insc=int(it['statistics'].get('subscriberCount',0)),uploads=it['contentDetails']['relatedPlaylists']['uploads'])
def dur(s):
    m=re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?',s or 'PT0S'); dd,h,mi,se=[int(x or 0) for x in m.groups()]; return dd*86400+h*3600+mi*60+se
out={}
for cid,c in chans.items():
    try:
        pl=yt.playlistItems().list(part='contentDetails',playlistId=c['uploads'],maxResults=50).execute()
    except Exception as e:
        print('erro',c['nome'],e); continue
    ids=[i['contentDetails']['videoId'] for i in pl['items']]
    vs=yt.videos().list(part='statistics,contentDetails',id=','.join(ids)).execute()['items']
    longos=[int(v['statistics'].get('viewCount',0)) for v in vs if dur(v['contentDetails'].get('duration'))>=180][:30]
    todos=[int(v['statistics'].get('viewCount',0)) for v in vs][:30]
    out[cid]=dict(nome=c['nome'],insc=c['insc'],n_longos=len(longos),mediana_longos=statistics.median(longos) if longos else None,mediana_todos=statistics.median(todos) if todos else None)
    print(f"{c['nome'][:30]:30} {c['insc']:>9} n={len(longos):2} med_longos={out[cid]['mediana_longos']} med_todos={out[cid]['mediana_todos']}")
json.dump(out,open(B+'medianas-canais.json','w'),ensure_ascii=False,indent=1)
