#!/usr/bin/env python3
"""Gera entrega/pacote/youtube.txt (bloco TESTAR E COMPARAR com os 3 pares, descrição, capítulos reais, fontes, créditos, tags) e checklist-publicacao.txt.
006-chernobyl (21/11/2026). Padrão de 14/11/2026 (skill pacote-youtube): sem menção a IA e sem palavras vetadas no youtube.txt. Uso: python3 tools/pacote.py"""
import json, re
from pathlib import Path
V = Path(__file__).resolve().parent.parent
caps = json.load(open(V / "qa/capitulos.json"))
fm = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
cap_txt = "\n".join(f"{fm(c['t'])} {c['titulo']}" for c in caps)
T = V / "entrega/pacote"; T.mkdir(parents=True, exist_ok=True)
var = json.load(open(V / "embalagem/variantes.json"))
bloco = "TITLES (Test & compare) — paired with the thumbnails\n" + "\n".join(
    f"{v['letra']}: {v['titulo']}  → thumb-{v['letra']}.jpg (\"{v['thumb_texto']}\") | title pattern: {v['padrao_titulo']} | thumb pattern: {v['padrao_thumb']}" for v in var)
txt = f"""{bloco}
Default when uploading: title A + thumbnail A.

DESCRIPTION
If you like places history closed behind a fence, and the official papers that explain why, subscribe, like the video and share it with someone who has wondered how the world found out.

At 01:23:40 on 26 April 1986, an emergency shutdown button was pressed in Reactor Four at Chernobyl. At 21:00 on 28 April, the Soviet evening news read five sentences about it. Between the two: 67 hours, 36 minutes, 20 seconds. This video runs that clock hour by hour and shows what exists for each mark: the fire dispatch calls and the Pripyat city radio announcement (both recorded), the reactor log in the IAEA's INSAG-7 report, the order for 1,125 buses, the director's report that called the city's situation normal, the alarm that went off at a Swedish power plant, the Politburo notes, and a CIA commentary from the day after. Then it asks why the zone that radio announcer called temporary is still closed.

CHAPTERS
{cap_txt}

SOURCES
- IAEA, "INSAG-7: The Chernobyl Accident: Updating of INSAG-1" (Safety Series 75-INSAG-7, 1992): Table I-I (operating log), §I-4.6.3, §II-2.3.4.
- V. P. Bryukhanov, report "On the accident at the V. I. Lenin Chernobyl NPP", 26 April 1986; Order of the Ministry of Motor Transport of the Ukrainian SSR on the evacuation of Pripyat, 27 April 1986 (Wilson Center Digital Archive, documents 208405 and 208406).
- Politburo session of 28 April 1986 (Archive of the President of the Russian Federation; English translation by S. Savranskaya, National Security Archive); original text, Gorbachev Foundation (gorby.ru).
- UPI Archives, 28 April 1986; CIA "Spot Commentary: Soviet Nuclear Accident", 29 April 1986 (Foreign Relations of the United States 1981-88, vol. V, doc. 220); Law of Ukraine No. 791a-XII of 27 February 1991.
- Recorded audio: fire-service dispatch calls of 26 April 1986 and Pripyat city radio announcement of 27 April 1986, via pripyat.com / Wikimedia Commons.
- Landsat 5 image of 29 April 1986 (U.S. Geological Survey); KH-9 Hexagon image of 29 January 1984 (U.S. Geological Survey); Sveriges Radio and press reports on the Forsmark alarm.

CREDITS
Film: Ukrkinokhronika, 1986 (V. Shevchenko and other newsreel footage); Ukrtelefilm, 1982 (via Gosteleradiofond); Vremya, Soviet Central Television, 28 April 1986; ABC News, 28 April 1986; CBS Evening News, 29 April 1986; VOA News. Photos: Yuri Yevsyukov, "Pripyat" (Mystetstvo, Kyiv, 1986); Nationaal Archief / Anefo (CC0); IAEA Imagebank (CC BY-SA 2.0); Public Chamber of Russia, oprf.ru (CC BY 4.0); Eamonn Butler (CC BY 2.0); Quintin Soloviev (CC BY 4.0); Wendelin Jacober (CC0); hnapel (CC0); Video: Carl Willis (CC BY 3.0); CNES 1986, Spot World Heritage (Licence Ouverte 2.0); NASA (public domain); U.S. Geological Survey. Maps: Natural Earth (schematic, positions approximate). Documents are shown for commentary and study, with the source on screen. The 28 April 1986 TASS bulletin is a reconstruction: the text is read by a generated voice and is not the original broadcast; the video says so on screen. No remains or injured people are shown.
Music: original, made for this channel.

TAGS
Chernobyl, Chernobyl 1986, Chernobyl timeline, Chernobyl hour by hour, Pripyat, Pripyat evacuation, Chernobyl Forsmark, Chernobyl Sweden, Chernobyl cover-up, Chernobyl exclusion zone, INSAG-7, Soviet Union 1986, Cold War history, places you can't visit

CATEGORY: Education · LANGUAGE: English (US)
"""
ban = re.compile(r"\b(dead|death|died|dies|killed|murder\w*|assassinat\w*|massacre|shocking|AI|synthetic|artificial)\b", re.I)
bad = ban.findall(txt)
assert not bad, bad
(T / "youtube.txt").write_text(txt)
(T / "checklist-publicacao.txt").write_text("""CHECKLIST DE PUBLICAÇÃO (Rodrigo) — fora da descrição
- CONTENT ID (importante): suba primeiro como NÃO LISTADO e espere a checagem de direitos do Studio antes de publicar. O vídeo usa áudios do Commons (muitos reuploads),
  cinejornais soviéticos (Ukrkinokhronika, Ukrtelefilm/Gosteleradiofond, Vremya), ABC/CBS e VOA: risco médio-alto de reclamação; todos com crédito na tela e na descrição.
  Se houver reivindicação: contestar como uso documental (trechos curtos, sem som nos filmes, crítica/comentário) ou trocar o trecho reivindicado (há reservas).
- Idioma do vídeo: English (US). Categoria: Education. Não é para crianças.
- Studio → Atributos → Uso de IA / conteúdo alterado ou sintético: SIM (voz sintética da narração; boletim TASS reconstruído, rotulado na tela; mídia de época é real).
- Título A + thumb A como padrão; B e C (com as thumbs B e C) no "Testar e comparar".
- Legendas: legendas.srt (English; inclui as legendas traduzidas dos áudios de época). Vídeo: video.mp4 1080p (nunca a versão do Telegram).
- Janela sugerida: dom 22/11 ou seg 23/11 (produzido no sábado; suba NÃO LISTADO antes e espere o Content ID). O dia é seu; a fábrica só sugere a janela.
- Conferir antes de publicar: legenda em russo do despacho (Ivankov, 0:55 do A3) é nossa tradução; hora do Vremya (21:00 = hora do programa; só fonte jornalística); Wilson Center pede contato para uso comercial (NPIHP@wilsoncenter.org); 34 fotos do livro de Yevsyukov (1986) com crédito na tela.
""")
print(len(txt), "bytes;", len(caps), "capítulos")
