"""Append V2 image credits to ASSET_CREDITS.md and asset_credits.json (idempotent)."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENTRIES = [
    {
        'file': 'bag_end_hobbiton.jpg',
        'title': 'File:Bag End at Hobbiton, New Zealand.jpg',
        'page': 'https://commons.wikimedia.org/wiki/File:Bag_End_at_Hobbiton,_New_Zealand.jpg',
        'author': 'May0313 (Wikimedia Commons user); file description: "Photographed by Eggie, 2025"',
        'license': 'CC BY 4.0',
        'license_url': 'https://creativecommons.org/licenses/by/4.0',
        'credit': 'Own work',
        'description': 'View of Bag End, the iconic hobbit hole of Bilbo and Frodo Baggins. This photo was taken by the Eggie at the Hobbiton Movie Set, Matamata, New Zealand. Photographed by Eggie, 2025',
        'source_url': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/59/Bag_End_at_Hobbiton%2C_New_Zealand.jpg/1920px-Bag_End_at_Hobbiton%2C_New_Zealand.jpg',
        'type': 'image',
        'original_dimensions': '5995x8992',
        'downloaded_dimensions': '1920x2880',
        'downloaded_bytes': 2011807,
        'sha256': '42ee4c9430b7e2ba0ba099540daadaf2361448bfc7fe1615e64c856bdf87d4b9',
        'verified': 'Local file is byte-identical to the Commons 1920px thumbnail (checked 2026-10-30).',
        'file_modified': False,
        'usage_v2': 'Photo of a real location (Hobbiton Movie Set), not a film still. Shown in Remotion with a circular mask, controlled crop/pan and push-in (beats 1-2); the image file itself is unmodified.',
    },
    {
        'file': 'sam_illustration.jpg',
        'title': 'File:Hobbit drawing from lucie schrimpf.jpg',
        'page': 'https://commons.wikimedia.org/wiki/File:Hobbit_drawing_from_lucie_schrimpf.jpg',
        'author': 'Lucie Vergne (artist; signature on the work reads "Lucie Schrimpf"); uploaded by Charliewendiga',
        'artist_url': 'https://www.instagram.com/lucievergne',
        'license': 'CC BY-SA 4.0',
        'license_url': 'https://creativecommons.org/licenses/by-sa/4.0',
        'credit': 'artist Lucie Vergne',
        'description': "Hobbit - Sam Gamegie par l'artiste Lucie Vergne",
        'date': '2021-05-02',
        'source_url': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/d/da/Hobbit_drawing_from_lucie_schrimpf.jpg/1280px-Hobbit_drawing_from_lucie_schrimpf.jpg',
        'type': 'image',
        'original_dimensions': '1839x1899',
        'downloaded_dimensions': '1280x1322',
        'downloaded_bytes': 727588,
        'sha256': 'd5645cae72f1dc4eea3a90e26c29a340ddbd251f19a0f17dae35cf730b7df76d',
        'verified': 'Local file is byte-identical to the Commons 1280px thumbnail (checked 2026-10-30).',
        'file_modified': False,
        'usage_v2': 'Fan art (not an official illustration). Shown whole in its own frame in beat 3: no crop, recolour, retouch, background removal; signature visible. Only the surrounding frame/backplate is animated. On-screen credit line included.',
        'share_alike_note': 'CC BY-SA 4.0: credit the artist, link the licence, indicate any changes, and license any adaptation of this artwork under CC BY-SA 4.0 (or a compatible licence). The video uses the artwork unaltered as a separate framed element; this entry does not place the rest of the video under CC BY-SA. Character rights in Tolkien\'s works are separate and not granted by this licence.',
    },
]

json_path = os.path.join(ROOT, 'asset_credits.json')
data = json.load(open(json_path, encoding='utf-8'))
have = {d.get('file') for d in data}
added = [e for e in ENTRIES if e['file'] not in have]
data.extend(added)
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('asset_credits.json: appended', [e['file'] for e in added])

MD = """

## V2 additions (composition `LotR1MinPilotV2`)

### Images
- **bag_end_hobbiton.jpg** — File:Bag End at Hobbiton, New Zealand.jpg; May0313 (Wikimedia Commons; the file description reads "Photographed by Eggie, 2025"); CC BY 4.0 (https://creativecommons.org/licenses/by/4.0). Source: https://commons.wikimedia.org/wiki/File:Bag_End_at_Hobbiton,_New_Zealand.jpg. The local file is the unmodified 1920×2880 Commons thumbnail (byte-identical). Photo of the Hobbiton Movie Set (a real location), not a film still. In the video it is masked, cropped and moved in Remotion; the file itself is unchanged.
- **sam_illustration.jpg** — File:Hobbit drawing from lucie schrimpf.jpg ("Hobbit - Sam Gamegie par l'artiste Lucie Vergne", 2021); artist **Lucie Vergne** (https://www.instagram.com/lucievergne; the signature on the drawing reads "Lucie Schrimpf"); uploaded by Charliewendiga; **CC BY-SA 4.0** (https://creativecommons.org/licenses/by-sa/4.0). Source: https://commons.wikimedia.org/wiki/File:Hobbit_drawing_from_lucie_schrimpf.jpg. The local file is the unmodified 1280×1322 Commons thumbnail (byte-identical). Fan art, not an official illustration.
  - Shown whole in its own frame (beat 3): no crop, recolour, retouch or background removal, signature visible; only the frame/backplate moves. On-screen credit: "Fan art « Sam Gamegie » — Lucie Vergne, CC BY-SA 4.0".
  - CC BY-SA 4.0 conditions to keep: credit the artist, link the licence, say whether changes were made (none to the artwork), and license any *adaptation of this artwork* under CC BY-SA 4.0 or a compatible licence. This credit does **not** place the whole video under CC BY-SA. Rights in Tolkien's characters are separate and not granted by this licence.

Suggested description credit: "Bag End, Hobbiton — photo May0313 (Eggie), CC BY 4.0, via Wikimedia Commons. Fan art « Sam Gamegie » — Lucie Vergne, CC BY-SA 4.0, via Wikimedia Commons."

### Original elements made for V2
- Schematic map, ship, ring, Red Book, family icons, Sam/Elanor silhouettes, timeline, paper/grain textures: original SVG/CSS drawn in `src/v2/VideoV2.jsx`.
- Ambient bed and SFX (`public/assets/v2/*.wav`): original, synthesised by `scripts_v2/make_audio_v2.py` (no samples or external music).
- `ambient.wav` (V1) is not used in V2.

### Fonts (V2)
- Cinzel and Cormorant Garamond, SIL Open Font License 1.1, loaded via `@remotion/google-fonts`. DejaVu (bundled) is the fallback.
"""
md_path = os.path.join(ROOT, 'ASSET_CREDITS.md')
md = open(md_path, encoding='utf-8').read()
if '## V2 additions' not in md:
    with open(md_path, 'a', encoding='utf-8') as f:
        f.write(MD)
    print('ASSET_CREDITS.md: appended V2 section')
