import requests, json, sys, re, time, os
api='https://commons.wikimedia.org/w/api.php'
H={'User-Agent':'LotrCidadesVideo/1.0 (personal educational project)'}
items = json.load(open(sys.argv[1]))  # {key: "File title"}
out = sys.argv[2]; credits = {}
if os.path.exists('assets_credits.json'): credits = json.load(open('assets_credits.json'))
strip = lambda s: re.sub(r'\s+',' ',re.sub('<[^>]+>','',s or '')).strip()
for key, title in items.items():
    if key in credits and os.path.exists(f'{out}/{key}.jpg'): continue
    time.sleep(3)
    p={'action':'query','titles':'File:'+title,'prop':'imageinfo','iiprop':'url|size|extmetadata','iiurlwidth':1920,'format':'json'}
    r=requests.get(api,params=p,headers=H,timeout=30)
    if r.status_code!=200: print('ERR',key,r.status_code); continue
    pg=list(r.json()['query']['pages'].values())[0]
    if 'imageinfo' not in pg: print('MISSING',key,title); continue
    ii=pg['imageinfo'][0]; m=ii['extmetadata']
    url = ii.get('thumburl') or ii['url']
    for attempt in range(4):
        time.sleep(3)
        d=requests.get(url,headers=H,timeout=120)
        if d.status_code==200: break
        time.sleep(15)
    if d.status_code!=200: print('DLERR',key,d.status_code); continue
    open(f'{out}/{key}.raw','wb').write(d.content)
    os.system(f'ffmpeg -loglevel error -y -i "{out}/{key}.raw" -q:v 2 "{out}/{key}.jpg" && rm "{out}/{key}.raw"')
    credits[key]={'title':title,'page':ii['descriptionurl'],'artist':strip(m.get('Artist',{}).get('value')),
      'license':strip(m.get('LicenseShortName',{}).get('value')),'license_url':m.get('LicenseUrl',{}).get('value',''),
      'date':strip(m.get('DateTimeOriginal',{}).get('value'))[:40],'orig_size':f"{ii['width']}x{ii['height']}"}
    print('OK',key,credits[key]['license'],credits[key]['artist'][:50],flush=True)
    json.dump(credits,open('assets_credits.json','w'),ensure_ascii=False,indent=1)
