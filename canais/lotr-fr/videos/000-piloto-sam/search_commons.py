import requests, json
api='https://commons.wikimedia.org/w/api.php'
queries=['sailing ship sea sunset','old book open pages','green rolling hills landscape','harbor boat ocean']
for q in queries:
 p={'action':'query','generator':'search','gsrsearch':q,'gsrnamespace':6,'gsrlimit':8,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':1280,'format':'json'}
 r=requests.get(api,params=p,headers={'User-Agent':'HermesVideoPilot/1.0 (educational demo)'},timeout=30); r.raise_for_status(); j=r.json()
 print('\nQUERY',q)
 for page in j.get('query',{}).get('pages',{}).values():
  ii=page.get('imageinfo',[{}])[0]; meta=ii.get('extmetadata',{})
  def v(k): return meta.get(k,{}).get('value','').replace('\n',' ')[:200]
  print(json.dumps({'title':page.get('title'),'url':ii.get('thumburl') or ii.get('url'),'filepage':ii.get('descriptionurl'),'width':ii.get('width'),'height':ii.get('height'),'license':v('LicenseShortName'),'artist':v('Artist'),'credit':v('Credit'),'desc':v('ImageDescription')},ensure_ascii=False))
