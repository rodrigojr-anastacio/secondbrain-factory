import requests, time, json, os, re, sys
H={'User-Agent':'LotrCidadesVideo/1.0 (personal educational project; contact rodrigo)'}
credits=json.load(open('assets_credits.json'))
strip = lambda s: re.sub(r'\s+',' ',re.sub('<[^>]+>','',s or '')).strip()
for key,title,w in [('zundert_kd',"Bloemencorso Zundert 2024 - Khazad-Dûm.jpg",1280),('numenor_map',"Map of Númenor.png",960)]:
    p={'action':'query','titles':'File:'+title,'prop':'imageinfo','iiprop':'url|size|extmetadata','iiurlwidth':w,'format':'json'}
    ii=list(requests.get('https://commons.wikimedia.org/w/api.php',params=p,headers=H).json()['query']['pages'].values())[0]['imageinfo'][0]
    m=ii['extmetadata']
    for i in range(3):
        r=requests.get(ii['thumburl'],headers=H)
        print(key,r.status_code,len(r.content),flush=True)
        if r.status_code==200:
            open(f'public/img/{key}.raw','wb').write(r.content); os.system(f'ffmpeg -loglevel error -y -i public/img/{key}.raw -q:v 2 public/img/{key}.jpg && rm public/img/{key}.raw')
            credits[key]={'title':title,'page':ii['descriptionurl'],'artist':strip(m.get('Artist',{}).get('value')),'license':strip(m.get('LicenseShortName',{}).get('value')),'license_url':m.get('LicenseUrl',{}).get('value',''),'date':'','orig_size':f"{ii['width']}x{ii['height']}"}
            break
        time.sleep(20)
json.dump(credits,open('assets_credits.json','w'),ensure_ascii=False,indent=1)
