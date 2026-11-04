import requests
files=['File:S.S. Coptic Sailing Away (1897).webm','File:Sailing Vessel Alhambra video 12-11-2021.webm','File:Ocean surface waves.ogv','File:Morning Fog on Lake BRoll 10s.webm','File:Green Hill in Libmanan.jpg','File:Old Pharmacy Book (14631955230).jpg']
for title in files:
 r=requests.get('https://commons.wikimedia.org/w/api.php',params={'action':'query','titles':title,'prop':'imageinfo','iiprop':'url|size|extmetadata','iiurlwidth':1200,'format':'json'},headers={'User-Agent':'HermesVideoPilot/1.0'},timeout=30);r.raise_for_status(); p=next(iter(r.json()['query']['pages'].values())); ii=p.get('imageinfo',[{}])[0]; m=ii.get('extmetadata',{})
 print(p.get('title'),'|',ii.get('size'),'bytes',ii.get('width'),ii.get('height'),'|',m.get('LicenseShortName',{}).get('value'),'|',ii.get('url'),'|',ii.get('thumburl'))
