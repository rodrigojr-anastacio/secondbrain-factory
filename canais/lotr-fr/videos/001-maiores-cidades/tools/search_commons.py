import requests, json, sys, re
api='https://commons.wikimedia.org/w/api.php'
H={'User-Agent':'LotrCidadesVideo/1.0 (personal educational project; rodrigo)'}
for q in sys.argv[1:]:
    p={'action':'query','generator':'search','gsrsearch':q,'gsrnamespace':6,'gsrlimit':12,'prop':'imageinfo','iiprop':'url|size|extmetadata','format':'json'}
    import time; time.sleep(5); r=requests.get(api,params=p,headers=H,timeout=30)
    if r.status_code!=200: print("ERR",r.status_code); continue
    j=r.json()
    print('\n##',q)
    for page in j.get('query',{}).get('pages',{}).values():
        ii=page.get('imageinfo',[{}])[0]; m=ii.get('extmetadata',{})
        v=lambda k: re.sub('<[^>]+>','',m.get(k,{}).get('value',''))[:60].replace('\n',' ')
        if ii.get('width',0)<1000: continue
        print(f"{page['title'][5:][:70]} | {ii.get('width')}x{ii.get('height')} | {v('LicenseShortName')} | {v('Artist')}")
