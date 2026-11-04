import re, requests
print('words',len(open('script_fr.txt').read().split()))
api='https://commons.wikimedia.org/w/api.php'
for q in ['filetype:video ocean waves','filetype:video sailing ship','filetype:video sea waves sunset','filetype:video fog forest','filetype:video green hills landscape','filetype:video forest walking']:
 p={'action':'query','generator':'search','gsrsearch':q,'gsrnamespace':6,'gsrlimit':10,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':1280,'format':'json'}
 r=requests.get(api,params=p,headers={'User-Agent':'HermesVideoPilot/1.0'},timeout=30); r.raise_for_status()
 print('\nQUERY',q)
 for page in r.json().get('query',{}).get('pages',{}).values():
  ii=page.get('imageinfo',[{}])[0]; m=ii.get('extmetadata',{})
  print(page.get('title'),'|',m.get('LicenseShortName',{}).get('value'),'|',ii.get('url'),'|',ii.get('thumburl'))
