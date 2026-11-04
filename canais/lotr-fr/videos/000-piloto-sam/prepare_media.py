import html,json,re,requests
from pathlib import Path
ROOT=Path('/home/hermes/workspace/lotr-pilot')
ASSET=ROOT/'public'/'assets'; ASSET.mkdir(parents=True,exist_ok=True)
FILES=[
 ('waves','File:Ocean surface waves.ogv','video'),
 ('ship_archive','File:S.S. Coptic Sailing Away (1897).webm','video'),
 ('fog','File:Morning Fog on Lake BRoll 10s.webm','video'),
 ('hills','File:Green Hills Landscape PLC-LS-2.jpg','image'),
 ('book','File:Pages of an old book fluttering in the breeze near a sunlit window during the afternoon.jpg','image'),
]
S=requests.Session(); S.headers['User-Agent']='Hermes-LotR-Pilot/1.0 (personal educational video prototype)'
credits=[]
def clean(x):
 x=html.unescape(re.sub('<[^>]+>',' ',x or ''))
 return ' '.join(x.split())
for slug,title,kind in FILES:
 r=S.get('https://commons.wikimedia.org/w/api.php',params={'action':'query','titles':title,'prop':'imageinfo','iiprop':'url|size|extmetadata','iiurlwidth':1920,'format':'json'},timeout=30); r.raise_for_status()
 page=next(iter(r.json()['query']['pages'].values()))
 if 'imageinfo' not in page: raise RuntimeError(f'No imageinfo: {title}')
 ii=page['imageinfo'][0]; m=ii.get('extmetadata',{})
 source=ii.get('url') if kind=='video' else ii.get('thumburl') or ii.get('url')
 ext='.'+('ogv' if slug=='waves' else 'webm' if kind=='video' else 'jpg')
 dest=ASSET/f'{slug}{ext}'
 with S.get(source,stream=True,timeout=120) as d:
  d.raise_for_status()
  with dest.open('wb') as f:
   for chunk in d.iter_content(1024*1024):
    if chunk: f.write(chunk)
 credits.append({'file':dest.name,'title':page.get('title'),'page':ii.get('descriptionurl'),'author':clean(m.get('Artist',{}).get('value')),'license':clean(m.get('LicenseShortName',{}).get('value')),'license_url':clean(m.get('LicenseUrl',{}).get('value')),'credit':clean(m.get('Credit',{}).get('value')),'description':clean(m.get('ImageDescription',{}).get('value')),'source_url':source,'type':kind,'original_bytes':ii.get('size'),'downloaded_bytes':dest.stat().st_size})
 print(dest.name,dest.stat().st_size,'bytes',credits[-1]['license'],credits[-1]['author'])
(ROOT/'asset_credits.json').write_text(json.dumps(credits,ensure_ascii=False,indent=2))
md=['# Visual asset credits','','Each item was fetched from Wikimedia Commons. Attribution is retained for the video description.','']
for c in credits:
 md += [f"- **{c['file']}** — {c['title']}; {c['author'] or 'author not listed'}; {c['license']}. Source: {c['page']}."]
md += ['', '## Synthetic voice', 'Piper `fr_FR-siwis-medium`, model card states CC-BY 4.0. Source: https://huggingface.co/rhasspy/piper-voices/tree/main/fr/fr_FR/siwis/medium.']
(ROOT/'ASSET_CREDITS.md').write_text('\n'.join(md)+'\n')
