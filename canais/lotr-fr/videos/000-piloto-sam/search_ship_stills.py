import requests,html,re
api='https://commons.wikimedia.org/w/api.php'; s=requests.Session(); s.headers['User-Agent']='HermesVideoPilot/1.0'
for q in ['filetype:bitmap tall ship sailing at sea','filetype:bitmap sailing ship ocean horizon','filetype:bitmap sailing vessel underway sea']:
 p={'action':'query','generator':'search','gsrsearch':q,'gsrnamespace':6,'gsrlimit':12,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':1200,'format':'json'}
 j=s.get(api,params=p,timeout=30).json(); print('\n',q)
 for x in j.get('query',{}).get('pages',{}).values():
  ii=x.get('imageinfo',[{}])[0]; m=ii.get('extmetadata',{}); lic=m.get('LicenseShortName',{}).get('value','')
  if any(z in lic.lower() for z in ['public domain','cc0','cc by']):
   print(x.get('title'),'|',lic,'|',ii.get('thumburl'),'|',ii.get('descriptionurl'))
