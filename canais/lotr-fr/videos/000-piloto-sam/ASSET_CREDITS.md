# Visual asset credits

Each item was fetched from Wikimedia Commons. Attribution is retained for the video description.

- **waves.ogv** — File:Ocean surface waves.ogv; Mostafameraji; CC0. Source: https://commons.wikimedia.org/wiki/File:Ocean_surface_waves.ogv.
- **ship_archive.webm** — File:S.S. Coptic Sailing Away (1897).webm; James H. White; Public domain. Source: https://commons.wikimedia.org/wiki/File:S.S._Coptic_Sailing_Away_(1897).webm.
- **fog.webm** — File:Morning Fog on Lake BRoll 10s.webm; Alabama Extension; CC0. Source: https://commons.wikimedia.org/wiki/File:Morning_Fog_on_Lake_BRoll_10s.webm.
- **hills.jpg** — File:Green Hills Landscape PLC-LS-2.jpg; Shadowmeld Photography; CC BY-SA 4.0. Source: https://commons.wikimedia.org/wiki/File:Green_Hills_Landscape_PLC-LS-2.jpg.
- **book.jpg** — File:Pages of an old book fluttering in the breeze near a sunlit window during the afternoon.jpg; Shixart1985; CC BY 2.0. Source: https://commons.wikimedia.org/wiki/File:Pages_of_an_old_book_fluttering_in_the_breeze_near_a_sunlit_window_during_the_afternoon.jpg.

## Fonts
- `DejaVuSans.ttf` and `DejaVuSans-Bold.ttf` are bundled for deterministic text rendering. DejaVu fonts are based on Bitstream Vera; copyright (c) 2003 Bitstream, Inc.; DejaVu changes are public domain. Full license is in `public/assets/DEJAVU-LICENSE.txt`.

## Synthetic voice
Piper `fr_FR-siwis-medium`, model card states CC-BY 4.0. Source: https://huggingface.co/rhasspy/piper-voices/tree/main/fr/fr_FR/siwis/medium.


## V2 additions (composition `LotR1MinPilotV2`)

### Images
- **bag_end_hobbiton.jpg** — File:Bag End at Hobbiton, New Zealand.jpg; May0313 (Wikimedia Commons; the file description reads "Photographed by Eggie, 2025"); CC BY 4.0 (https://creativecommons.org/licenses/by/4.0). Source: https://commons.wikimedia.org/wiki/File:Bag_End_at_Hobbiton,_New_Zealand.jpg. The local file is the unmodified 1920×2880 Commons thumbnail (byte-identical). Photo of the Hobbiton Movie Set (a real location), not a film still. In the video it is masked, cropped and moved in Remotion; the file itself is unchanged.
- **sam_illustration.jpg** — File:Hobbit drawing from lucie schrimpf.jpg ("Hobbit - Sam Gamegie par l'artiste Lucie Vergne", 2021); artist **Lucie Vergne** (https://www.instagram.com/lucievergne; the signature on the drawing reads "Lucie Schrimpf"); uploaded by Charliewendiga; **CC BY-SA 4.0** (https://creativecommons.org/licenses/by-sa/4.0). Source: https://commons.wikimedia.org/wiki/File:Hobbit_drawing_from_lucie_schrimpf.jpg. The local file is the unmodified 1280×1322 Commons thumbnail (byte-identical). Fan art, not an official illustration.
  - Shown whole in its own frame (beat 3): no crop, recolour, retouch or background removal, signature visible; only the frame/backplate moves. On-screen credit: "Fan art « Sam Gamegie » — Lucie Vergne, CC BY-SA 4.0".
  - CC BY-SA 4.0 conditions to keep: credit the artist, link the licence, say whether changes were made (none to the artwork), and license any *adaptation of this artwork* under CC BY-SA 4.0 or a compatible licence. This credit does **not** place the whole video under CC BY-SA. Rights in Tolkien's characters are separate and not granted by this licence.

Suggested YouTube description credit (copy/paste): "Bag End at Hobbiton — photo by May0313 (photographed by Eggie, 2025), via Wikimedia Commons, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/): https://commons.wikimedia.org/wiki/File:Bag_End_at_Hobbiton,_New_Zealand.jpg. Fan art « Sam Gamegie » — Lucie Vergne (signature: Lucie Schrimpf), via Wikimedia Commons, CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/): https://commons.wikimedia.org/wiki/File:Hobbit_drawing_from_lucie_schrimpf.jpg. Fan art shown in full and unmodified."

### Original elements made for V2
- Schematic map, ship, ring, Red Book, family icons, Sam/Elanor silhouettes, timeline, paper/grain textures: original SVG/CSS drawn in `src/v2/VideoV2.jsx`.
- Ambient bed and SFX (`public/assets/v2/*.wav`): original, synthesised by `scripts_v2/make_audio_v2.py` (no samples or external music).
- `ambient.wav` (V1) is not used in V2.

### Fonts (V2)
- Cinzel and Cormorant Garamond, SIL Open Font License 1.1, loaded via `@remotion/google-fonts`. DejaVu (bundled) is the fallback.
