#!/usr/bin/env python3
"""Gera entrega/pacote/youtube.txt (3 títulos pareados às thumbs, descrição, capítulos reais, fontes, créditos, tags) e checklist-publicacao.txt.
Padrão de 14/11/2026 (skill pacote-youtube): sem menção a IA e sem palavras vetadas no youtube.txt. Uso: python3 tools/pacote.py"""
import json, re
from pathlib import Path
V = Path(__file__).resolve().parent.parent
caps = json.load(open(V / "qa/capitulos.json"))
fm = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
cap_txt = "\n".join(f"{fm(c['t'])} {c['titulo']}" for c in caps)
T = V / "entrega/pacote"; T.mkdir(parents=True, exist_ok=True)
txt = f"""TITLES (Test & compare) — paired with the thumbnails
A: Why Are There Still Bullet Holes at Pearl Harbor?           → thumb-A.jpg ("ON PURPOSE")
B: The Pearl Harbor Wall Tourists Aren't Allowed to See        → thumb-B.jpg ("ON PURPOSE")
C: What's Still Behind the Gate at Hickam Field?               → thumb-C.jpg ("ON PURPOSE")
Default when uploading: title A + thumbnail A.

DESCRIPTION
If you like places history left behind, subscribe, like the video and share it with someone who has stood at Pearl Harbor.

Look closely at this wall: bullet and shrapnel strikes from one morning in 1941, never patched. It belongs to a working headquarters on an active base, and an ordinary visitor can't walk up to it. We follow the paperwork (an Air Force fact sheet, a National Historic Landmark nomination, a federal law) to find out who decided the marks should stay, what else sits behind the same gate, and what a tourist does get to see.

CHAPTERS
{cap_txt}

SOURCES
- U.S. Air Force / Pacific Air Forces, Hickam Field and PACAF Headquarters history fact sheets and the PACAF "staff ride" material.
- National Park Service, National Register of Historic Places Inventory—Nomination Form, "Hickam Field" (National Historic Landmark, 1984–85).
- National Archives (NARA), dispatch 596244 and U.S. Navy film records NAID 76168, 76169, 76171 and 77339; Naval History and Heritage Command, "Ford Island" and Pearl Harbor attack pages.
- Commander, Navy Installations Command, Joint Base Pearl Harbor-Hickam history and Visitor Control Center pages.
- Public Law 116-9, section 2206 (Pearl Harbor National Memorial boundaries); National Park Service, Pearl Harbor National Memorial and USS Utah Memorial pages and FAQ.
- DVIDS (Defense Visual Information Distribution Service): PACAF, JBPHH and Defense POW/MIA Accounting Agency news releases; Pearl Harbor Aviation Museum, Hangar 79 and Ford Island pages; Honolulu Star-Advertiser reporting on the USS Utah and USS Arizona memorials; HABS/HAER documentation, Library of Congress.

CREDITS
Photos, film and documents: U.S. National Archives (80-G collection and NAID 76168/76169/76171/77339), Naval History and Heritage Command, U.S. Air Force, U.S. Navy, DVIDS, National Park Service, Library of Congress (HABS/HAER), and public-domain files on Wikimedia Commons. Maps: Natural Earth (schematic, positions approximate). U.S. government works are in the public domain. Photographs show the buildings and ceremonies; no casualties are shown.
Music: original, made for this channel.

TAGS
Pearl Harbor, Hickam Field, Pearl Harbor bullet holes, Pearl Harbor 1941, Pacific Air Forces, Joint Base Pearl Harbor-Hickam, USS Utah Memorial, Ford Island, National Historic Landmark, Hale Makai barracks, places you can't visit, WWII history, December 7 1941

CATEGORY: Education · LANGUAGE: English (US)
"""
ban = re.compile(r"\b(dead|death|died|dies|killed|murder\w*|assassinat\w*|massacre|shocking|AI|synthetic|artificial)\b", re.I)
bad = ban.findall(txt)
assert not bad, bad
assert all(len(l) <= 100 for l in txt.splitlines() if l[:2] in ("A:", "B:", "C:")) 
(T / "youtube.txt").write_text(txt)
(T / "checklist-publicacao.txt").write_text("""CHECKLIST DE PUBLICAÇÃO (Rodrigo) — fora da descrição
- Idioma do vídeo: English (US). Categoria: Education. Não é para crianças.
- Studio → Atributos → Uso de IA / conteúdo alterado ou sintético: SIM (voz sintética; mídia histórica é real).
- Título A + thumb A como padrão; B e C (com as thumbs B e C) no "Testar e comparar".
- Legendas: legendas.srt (English). Vídeo: video.mp4 1080p (nunca a versão do Telegram).
- Publicação planejada: quarta 18/11/2026.
""")
print(len(txt), "bytes;", len(caps), "capítulos")
