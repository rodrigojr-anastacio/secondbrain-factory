# Claude Code implementation brief — V3

Build the approved V3 pilot as an independent Remotion composition. Read `STORYBOARD_V3.md`, `script_fr_v3.txt`, `ASSET_CREDITS_V3.md`, `SOURCES_V3.md`, `REFERENCIAS.md`, the existing V2 composition, and local Remotion skills before editing.

## Preserve

- Do not edit, overwrite, rename, or delete `src/Video.jsx`, `src/v2/**`, `out/lotr-pilot-v2-fr.mp4`, `script_fr.txt`, `public/assets/narration.wav`, or any V1/V2 asset.
- Add a separate composition `LotR1MinPilotV3` in a new `src/v3/VideoV3.jsx`; make only the minimal registration change in `src/index.jsx`.
- Do not use film footage. The official YouTube download required sign-in and was not bypassed. Use only the already licensed/project assets and original vector animation.
- Do not fetch new images/audio or add dependencies.

## Inputs

- French narration: `public/assets/v3/narration_v3.mp3` (60.552 s; 24 kHz mono).
- Original music: `public/assets/v3/music_bed_v3.wav` (60 s; 22.05 kHz stereo). Keep it perceptible but clearly under narration. The bed must fade and duck around speech; do not use Howard Shore or any film score.
- Licensed media: `assets/bag_end_hobbiton.jpg`, `assets/sam_illustration.jpg`, `assets/hills.jpg`, `assets/book.jpg`, `assets/ship_archive.webm`, `assets/fog.webm`, `assets/waves.mp4` (paths relative to `public/`). Existing credit/license notes are in `ASSET_CREDITS_V3.md`.
- Fonts/dependencies in the project already include Remotion 4.0.539, `@remotion/media`, `@remotion/google-fonts`, Cinzel and Cormorant Garamond.

## Composition

- 1920×1080, 30 fps, 61 seconds / 1830 frames; preserve the final 0.55 s of narration and a quiet tail.
- Implement the 15-beat schedule in `STORYBOARD_V3.md`: varied visual durations, frequent relevant inserts, controlled movement, and genuinely slower/sparser treatment around Rosie’s death and the final question.
- Include phrase-level French captions using `@remotion/captions`-compatible JSON at `src/v3/captions_fr.json`, plus `out/lotr-pilot-v3-fr.srt`. Base the cue times on the measured silence boundaries below; do not invent word-level timings:
  - 0.333–2.780: `Frodon a pris la mer vers l’Ouest.`
  - 3.939–4.515: `Sam, lui, est rentré.`
  - 4.698–6.298: `À cent deux ans, pourquoi part-il à son tour ?`
  - 7.423–14.621: `Dans la Comté, il a retrouvé Rosie, élevé leurs enfants, poursuivi le Livre Rouge.`
  - 14.970–18.166: `Après plus de soixante ans ensemble, Rosie meurt.`
  - 19.287–23.114: `Le 22 septembre, Sam quitte Cul-de-Sac.`
  - 24.255–31.781: `Aux Collines des Tours, il confie le Livre à Elanor.`
  - 32.071–44.488: `Selon la tradition familiale, il rejoint les Havres Gris, traverse la mer — dernier Porteur de l’Anneau à partir.`
  - 45.598–48.912: `Mais Tolkien ne raconte pas leurs retrouvailles.`
  - 50.012–53.442: `Deux départs. Une vie entre eux.`
  - 54.556–59.544: `Et vous… vous imaginez qu’ils se sont retrouvés ?`
- Make subtitles readable but less kinetic than V2: phrase cards with soft fades, no word-by-word flashing.

## Canonical map requirements

- Draw an original schematic SVG map, visibly marked `CARTE SCHÉMATIQUE — NON À L’ÉCHELLE`.
- Correct west-to-east relationships: the Shire and Westmarch are east of the Tower Hills; Grey Havens/Mithlond are in Lindon at the eastern end of the Gulf of Lhûn. Label the places in French and include Sindarin/alternate names in smaller text where useful.
- Show a solid route from the Shire toward the Tower Hills/Emyn Beraid and handover to Elanor; show onward travel to the Grey Havens as a dotted, explicitly tradition-based continuation. Do not depict an exact route unsupported by the text.
- Show the crossing of Belegaer in a separate sea panel. Do not put Aman/Valinor beside the north-west map.

## Attribution and validation

- Keep Lucie Vergne’s fan art whole, unaltered, signature visible, and credit visible.
- Use CC-licensed photos with the edits disclosed in the V3 credit note; never describe a Hobbiton location photo or the 1897 ship footage as a film still.
- Render `out/lotr-pilot-v3-fr.mp4` and produce the matching SRT. Do not publish or commit.
- Run the Remotion composition listing and render with the existing `LD_LIBRARY_PATH=/home/hermes/.hermes/cache/scratch/remotion-libs/root/usr/lib/x86_64-linux-gnu` workaround. Inspect several frames (hook, family, map, Grey Havens, ending) and fix any overlap, unreadable label, or incorrect map direction before reporting completion.
