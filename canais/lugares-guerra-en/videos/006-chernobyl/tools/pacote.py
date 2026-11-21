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
A: Why Is America Digging Up Japanese Soldiers on Tarawa?      → thumb-A.jpg ("SAME HOLE") | title pattern: Why Is [country] Digging Up X? | thumb pattern: objeto-simbolo
B: The Soldiers America Wasn't Looking for on Tarawa           → thumb-B.jpg ("WHOSE?") | title pattern: The X They Weren't Supposed to Find | thumb pattern: cena-acao
C: What's Still Under Tarawa Besides the Marines?              → thumb-C.jpg ("1943 · NOW") | title pattern: What's Still Under X? | thumb pattern: antes-depois
Default when uploading: title A + thumbnail A.

DESCRIPTION
If you like places history left behind, subscribe, like the video and share it with someone who knows the Pacific story.

The Defense Department runs a DNA project for one small island: Betio, in Tarawa Atoll. Of 243 distinct DNA profiles its scientists have read, 124 trace to Asian lineages. The American search is for about 374 Marines and sailors still missing, but the ground gives back Japanese and Korean men too, buried in the same craters and trenches. We follow the official papers (a 1947 Marine Corps history, a POW/MIA fact sheet, a federal science paper) to find out how both sides ended up in the same ground, what happens to the men who turn up, and what is still under the town that grew on top.

CHAPTERS
{cap_txt}

SOURCES
- Taylor, Scott, Koehl, Trask and Maijanen (Defense POW/MIA Accounting Agency), "The Tarawa Project Part I," Forensic Anthropology 2(2), 2019.
- Defense POW/Missing Personnel Office, Tarawa Fact Sheet; Defense POW/MIA Accounting Agency news releases and casualty data for the Battle of Tarawa.
- Capt. James R. Stockman, "The Battle for Tarawa" (USMC Historical Section, 1947), including Appendix C; Joseph H. Alexander, "Across the Reef: The Marine Assault on Tarawa" (USMC History and Museums Division, 1993); Bernard C. Nalty, "The United States Marines in the Gilberts Campaign" (1962).
- DVIDS (Defense Visual Information Distribution Service) releases and photographs on the 2019 and 2023 Betio recoveries and the repatriation ceremonies.
- National Archives (NARA) and U.S. Navy film records NAID 75861, 75866 and 77026; Naval History and Heritage Command.

CREDITS
Photos, film and documents: U.S. National Archives (NARA), U.S. Navy, U.S. Marine Corps, U.S. Army Air Forces, U.S. Coast Guard, Defense POW/MIA Accounting Agency, Defense POW/Missing Personnel Office, DVIDS (photos by Cpl. Taryn Escott, Sgt. Melanye Martinez, Sgt. Therese Edwards and MC1 Amara Timberlake), NASA (ISS Expedition 53 photograph by Randolph Bresnik), and public-domain files on Wikimedia Commons. USMC historical monographs via HyperWar and the Marine Corps History Division. Maps: Natural Earth (schematic, positions approximate). U.S. government works are in the public domain. Photographs show the work of recovery teams, places and ceremonies; no remains are shown.
Music: original, made for this channel.

TAGS
Tarawa, Betio, Battle of Tarawa, Tarawa 1943, Tarawa Atoll, Kiribati, Defense POW/MIA Accounting Agency, DPAA, History Flight, Marines still missing, WWII Pacific, WWII history, places you can't visit, Japanese soldiers WWII

CATEGORY: Education · LANGUAGE: English (US)
"""
ban = re.compile(r"\b(dead|death|died|dies|killed|murder\w*|assassinat\w*|massacre|shocking|AI|synthetic|artificial)\b", re.I)
bad = ban.findall(txt)
assert not bad, bad
(T / "youtube.txt").write_text(txt)
(T / "checklist-publicacao.txt").write_text("""CHECKLIST DE PUBLICAÇÃO (Rodrigo) — fora da descrição
- Idioma do vídeo: English (US). Categoria: Education. Não é para crianças.
- Studio → Atributos → Uso de IA / conteúdo alterado ou sintético: SIM (voz sintética; mídia histórica é real).
- Título A + thumb A como padrão; B e C (com as thumbs B e C) no "Testar e comparar".
- Legendas: legendas.srt (English). Vídeo: video.mp4 1080p (nunca a versão do Telegram).
- Janela sugerida: qua 18/11 ou sex 20/11/2026 (o dia é seu; aniversário da batalha 20-23/11).
- Conferir antes de publicar: número do laboratório (B01), linha do DPMO (B01c), little or nothing de 1947 (B08a), Choi (B17); doc Taylor 2019 = licença da revista (se houver dúvida, trocar por Cartela).
""")
print(len(txt), "bytes;", len(caps), "capítulos")
