import requests,json
files=[
'File:Ocean surface waves 03.ogv',
'File:LARGE SAILING SHIPS AT SEA, 4K • ISOT PURJELAIVAT MERELLÄ.webm',
'File:Adjara2025walking-summer-forest.webm',
'File:Pages of an old book fluttering in the breeze near a sunlit window during the afternoon.jpg',
'File:Green Hills Landscape PLC-LS-2.jpg',
'File:Sunset Sailing on the Tall Ship Inland Seas (48312103756).jpg'
]
for title in files:
 r=requests.get('https://commons.wikimedia.org/w/api.php',params={'action':'query','titles':title,'prop':'imageinfo','iiprop':'url|size|extmetadata','iiurlwidth':1600,'format':'json'},headers={'User-Agent':'HermesVideoPilot/1.0'},timeout=30); r.raise_for_status()
 p=next(iter(r.json()['query']['pages'].values()))
 if 'imageinfo' not in p: print('MISSING',title); continue
 ii=p['imageinfo'][0]; m=ii.get('extmetadata',{})
 print(json.dumps({'title':p.get('title'),'page':ii.get('descriptionurl'),'url':ii.get('url'),'thumb':ii.get('thumburl'),'size':ii.get('size'),'width':ii.get('width'),'height':ii.get('height'),'license':m.get('LicenseShortName',{}).get('value'),'artist':m.get('Artist',{}).get('value'),'credit':m.get('Credit',{}).get('value'),'usageTerms':m.get('UsageTerms',{}).get('value'),'licenseUrl':m.get('LicenseUrl',{}).get('value')},ensure_ascii=False))
