#!/usr/bin/env python3
"""Gera entrega/pacote/youtube.txt (3 títulos pareados às thumbs, descrição, capítulos reais, fontes, créditos, tags). Uso: python3 tools/pacote.py"""
import json
from pathlib import Path
V = Path(__file__).resolve().parent.parent
caps = json.load(open(V / "qa/capitulos.json"))
fm = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
cap_txt = "\n".join(f"{fm(c['t'])} {c['titulo']}" for c in caps)
T = V / "entrega/pacote"; T.mkdir(parents=True, exist_ok=True)
txt = f"""TITLES (Test & compare) — paired with the thumbnails
A: The Gettysburg Photos You Weren't Supposed to See          → thumb-A.jpg ("THEY MOVED HIM")
B: Why Is the Same Dead Soldier in Two Gettysburg Photos?     → thumb-B.jpg ("SAME MAN / 40 YARDS")
C: What Happened to the Real "Harvest of Death"?              → thumb-C.jpg ("WRONG ARMY")
Default when uploading: title A + thumbnail A; put B and C in "Test & compare" with their pairs.

DESCRIPTION
Look at the most famous photograph of the Gettysburg dead: a young soldier behind a stone wall, a rifle against the rock. The man who sold it wrote a story to go with it. Most of that story does not hold up, and the same photographer's other plates show why.
We read the captions from Alexander Gardner's 1866 Sketch Book line by line, set the plates side by side, and follow the evidence: a body moved about forty yards, a rifle that was probably a prop, a row of dead sold as Confederates in one plate and as "our own men" in the next, and a November 19 photograph where Abraham Lincoln was hiding in plain sight.

If you have walked the Devil's Den, or you know a family story from Gettysburg, tell us in the comments.

CHAPTERS
{cap_txt}

SOURCES
- Alexander Gardner, Gardner's Photographic Sketch Book of the War (1866), plates 36, 37, 40 and 41 and their text pages (Library of Congress).
- Library of Congress, "Civil War Photographs: Does the Camera Ever Lie?" and "The Case of the Moved Body" (American Memory, Civil War Photographs Collection).
- National Archives, "The true story behind the Gettysburg sharpshooter" (2013) and the Prologue pieces on the Brady photograph of November 19, 1863 (NAID 111-B-4975) and Josephine Cobb (1952).
- William A. Frassanito, Gettysburg: A Journey in Time (1975), as cited by the National Archives and the National Park Service.
- National Park Service, Gettysburg National Military Park: "Then & Now" stereo comparisons, battle overview, Soldiers' National Cemetery pages, and the 2015 news release on remains found in 1996.
- Abraham Lincoln, Gettysburg Address, Bliss and Nicolay copies (Library of Congress).
- T. Ditterline, "Field of Gettysburg, July 1st, 2nd & 3rd, 1863" (Library of Congress); J. Warren Gilbert, "Gettysburg and Vicinity" (1922).

CREDITS
Photos and documents: Library of Congress (Prints & Photographs Division, Civil War Photographs, HAER, Carol M. Highsmith Archive, Geography and Map Division), U.S. National Archives (111-B-4975, 64-NA-1595), National Park Service, Gettysburg National Military Park, U.S. Army National Guard (2015), U.S. Navy (2013), Internet Archive (Gardner's Sketch Book scans), Wikimedia Commons (public-domain files and one CC0 photo). Maps: Natural Earth; T. Ditterline (1863).
U.S. government works and works from before 1930 are in the public domain; "No known restrictions on publication" per the Library of Congress. On-screen dates and places only; full credits are listed here. Photographs of the dead are shown with respect and without close-ups. Music: original, made for this channel.
Narration voice is synthetic (AI text-to-speech).

TAGS
Gettysburg, Gettysburg photos, Alexander Gardner, Harvest of Death, Home of a Rebel Sharpshooter, Devil's Den, Timothy O'Sullivan, Civil War photography, Library of Congress, Civil War history, Gettysburg Address, Lincoln at Gettysburg, Frassanito, restricted documents, 1863

CATEGORY: Education · LANGUAGE: English (US)

REMINDER FOR UPLOAD (Rodrigo)
- Video language: English. "Altered or synthetic content": YES (synthetic narration voice). Not made for kids.
- Upload the 3 thumbnails in "Test & compare" (A main) and the title alternatives if the test is available.
- Upload legendas.srt as English subtitles. Use video.mp4 (1080p).
- Publication planned for Monday 11/16 (Gettysburg Address anniversary is 11/19).
"""
(T / "youtube.txt").write_text(txt)
print(len(txt), "bytes;", len(caps), "capítulos")
