#!/usr/bin/env python3
"""Fonte única do dossie-es 010 (El Cártel de Medellín): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (na pasta do vídeo). Conteúdo no topo; geração no fim (copiada do 009-gestapo).

Embalagem aprovada no crivo r3 (16/11/2026, EMBALAGEM.md/CRIVO.md):
  A/T1 "TODA la Historia del Cártel de Medellín en 14 Minutos | Su Guerra contra la Extradición" + algemas abertas, sello INTOCABLES
  B/T2 "CÁRTEL DE MEDELLÍN: La guerra por una sola palabra" + página datilografada com uma palavra tarjada, "ART. 35"
  C/T3 "Cómo el Cártel de Medellín tomó de rehén a todo un país" + helicópteros sobre a fazenda (de dia), "¿RESCATE?"
  Frase-âncora do hook: "Esta es TODA la historia del Cártel de Medellín. Y de la guerra que le hizo a un país entero por una sola palabra: extradición."
Ângulo (ANGULO.md): o cartel pelo lado do Estado e dos reféns; fio = a palavra "extradición" (tratado 1979 → sentença 1986 →
decreto 1989 → art. 35 de 1991 → Acto Legislativo 1997). Hook = Diana Turbay, 25/01/1991, pago no exp. 9 e no cierre.
Fora da manada (nenhuma transcrição em ref/): Tratado/Zea, Los Cinco (1985), El Juez, La Sentencia, Los Rehenes, La Operación,
El Sacerdote, o placar 51–13–5, o Acto Legislativo. Fatos obrigatórios da manada (Lara, Cano, Galán, Avianca, fuga, morte) só
como frase de contexto, nunca como cena principal.

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (id I### na ordem de aparição) · "chave" reuso · "chave#enq" reuso com enquadramento
  + "@@TEXTO"      rótulo na tela (máquina de escrever; CAIXA ALTA, até ~28 caracteres)
Bloco: b(texto, *planos, card="BOGOTÁ, 1986", ideia=True) · capítulo: cap("5. El Juez")
Mapas (chave map_*): base sem texto nem pinos; pinos, setas e nomes no código (src/labels.jsx).
"""
import json, math, re
from pathlib import Path

WPS = 2.38           # palavras/s medidas no 001–008 (erro de 1–3%)
BREAK, LONG = 0.35, 0.8
MAX_PLANO_INICIO = 3.0   # s por plano nos primeiros INICIO s (~20 cortes/min)
INICIO = 60.0
MAX_PLANO = 3.6      # s por plano depois (~17 cortes/min)
INEDITO_ATE = 180.0  # s: só imagens novas até aqui
JANELA = 60.0        # s: mesmo enquadramento da mesma imagem só depois disso
HOOK_MAX = 35.0      # s: a bíblia pede hook de 25–35 s
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "TODA la Historia del Cártel de Medellín | Su Guerra contra la Extradición"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK ─────────────────────────
SEM = ", no lettering anywhere"   # papéis, placas, capas: o nano-banana inventa texto
VIOL = ", seen from far away, no bodies, no blood"
NOARM = ", no weapons visible"
HELI = "plain dark green police helicopters without any markings, numbers or lettering"
PLANE = "a plain white airliner without any logo, airline name, tail emblem or lettering"
PAPER = "completely blank sheets of paper with no writing, no marks, no letters"
# Personagens (descrição visual fixa; rostos "resembling", nunca foto)
DIANA = "a Colombian woman journalist of forty with shoulder-length dark hair, an intelligent serious face, a simple light blouse and dark jacket, 1990, resembling Diana Turbay"
TURBAY = "an elderly Colombian statesman of about sixty-three with thick black-rimmed glasses, receding grey hair and a dark suit, 1979, resembling Julio César Turbay Ayala"
ZEA = "a Colombian government minister in his sixties with grey hair and a dark suit, 1980"
ESCOBAR = "a stocky Colombian man in his thirties with curly dark hair and a thick moustache, a short-sleeved shirt, resembling Pablo Escobar"
ORTEGA = "a Colombian congressman in his forties with dark hair and a dark suit and tie, 1983"
LARA = "a slim Colombian politician of thirty-five with dark wavy hair, a moustache and a dark suit, 1983, resembling Rodrigo Lara Bonilla"
BETANCUR = "a short white-haired Colombian president of about sixty with a kind round face and a dark suit, 1984, resembling Belisario Betancur"
LOPEZ = "a tall elderly Colombian former president of about seventy, bald, with glasses and a grey suit, 1984, resembling Alfonso López Michelsen"
BOTERO = "a Colombian businessman in his fifties with grey hair, glasses and a dark suit, 1985"
JUEZ = "a Colombian judge in his thirties with dark hair, glasses and a grey suit and tie, 1985"
BARCO = "an elderly Colombian president of about sixty-five with white hair, glasses and a calm serious face, a dark suit, resembling Virgilio Barco"
CANO = "a Colombian newspaper editor of about sixty with grey hair, glasses and a moustache, a white shirt and tie, resembling Guillermo Cano"
LEHDER = "a Colombian man in his late thirties with long dark hair and a beard, a rumpled shirt, 1987, resembling Carlos Lehder"
GALAN = "a tall Colombian politician of forty-six with dark hair and a strong jaw, a dark suit, 1989, resembling Luis Carlos Galán"
GAVIRIA = "a Colombian president in his early forties with dark hair and glasses, a dark suit, 1990, resembling César Gaviria"
SANTOS = "a young Colombian journalist of twenty-nine with curly dark hair and glasses, 1990, resembling Francisco Santos"
MONTOYA = "a Colombian woman in her sixties with short grey hair and a calm dignified face, 1990"
MARUJA = "an elegant Colombian woman in her mid-forties with short dark hair, 1990, resembling Maruja Pachón"
BEATRIZ = "a Colombian woman in her late thirties with long dark hair, 1990"
GH = "a very old Colombian Catholic priest of eighty-two with white hair and a thin lined face, wearing a black cassock, resembling Rafael García Herreros"
VILLAMIZAR = "a Colombian man in his late forties with dark hair and a moustache, a dark jacket, 1991, resembling Alberto Villamizar"
FABIO = "a heavy-set Colombian man in his forties with dark hair, a polo shirt, 1999"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, borders and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame, no ocean names"
ANDES = "steep green Andean mountains of Antioquia, Colombia, with coffee plants and banana trees"

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Copacabana, Antioquia. Enero de mil novecientos noventa y uno.",
  f"andes_day|Daytime wide shot of {ANDES} under low grey clouds, a small white farmhouse with a clay tile roof on a slope, 1991",
  f"heli_approach|Two {HELI} flying low over a green Andean valley in Antioquia, seen from far away, grey clouds", card="COPACABANA, 1991")
b("Helicópteros de la Policía sobre una finca. Los captores sacan corriendo a una secuestrada.",
  f"heli_farm|A police helicopter hovering low above a white farmhouse on a steep coffee slope, grass flattened by the rotor wind, {HELI}" + VIOL + NOARM,
  "run_slope|Tiny distant figures running down a steep coffee plantation slope among banana trees, one of them a woman held by the arm, seen from far away from above, no faces visible" + VIOL + NOARM)
b("Hay disparos. Ella muere esa misma tarde.",
  "hospital_corridor|An empty corridor of a 1991 Colombian public hospital in late afternoon light, a gurney against the wall, nobody on it, no signs" + SEM)
b("Se llama Diana Turbay. Periodista. Hija de un expresidente de Colombia.",
  f"diana_portrait|{DIANA} in portrait at her desk in a newsroom, looking at the viewer, 1990@@DIANA TURBAY",
  f"turbay_portrait|{TURBAY} in an official portrait in a wood-paneled office, a Colombian presidential sash without any text, 1979@@JULIO CÉSAR TURBAY")
b("En el gobierno de su padre se firmó el tratado que sus captores querían destruir.",
  f"treaty_sign|Close-up of hands signing a document with a black fountain pen on a dark wooden desk in Washington in 1979, {PAPER} except a single illegible scribbled line",
  "treaty_folder|A thick leather document folder tied with a ribbon on a polished desk under a green banker's lamp, 1979" + SEM,
  "handcuffs_desk|Close three-quarter view of a pair of open steel handcuffs lying on a dark wooden desk under a lamp, deep slate blue shadows" + SEM)
b("Esta es TODA la historia del Cártel de Medellín. Y de la guerra que le hizo a un país entero por una sola palabra: extradición.",
  "files_desk|A long dark desk covered with open brown case files tied with red string and black and white photographs, a red rubber stamp and a magnifying glass, lamp light" + SEM,
  "medellin_night|The city of Medellín in a deep Andean valley at night in the late 1980s, thousands of lights climbing the mountain slopes",
  "red_stamp|A hand slamming a red rubber stamp onto a brown paper case file, ink splash, dramatic close-up" + SEM,
  "bogota_capitol|The neoclassical stone Capitolio Nacional on Plaza de Bolívar in Bogotá under a grey sky, pigeons, 1980s, no inscriptions" + SEM, ideia=True)

# ───────────────────────── 1. EL TRATADO ─────────────────────────
cap("1. El Tratado")
b("El Tratado. Washington, catorce de septiembre de mil novecientos setenta y nueve. Colombia y Estados Unidos firman un tratado de extradición.",
  "washington_1979|Washington D.C. in September 1979, the white neoclassical government buildings along a wide avenue, autumn trees, 1970s cars",
  "state_room|A formal diplomatic signing room with tall windows, a long table with two chairs and two small unlabeled flags, 1979, no people" + SEM,
  "two_pens|Two black fountain pens laid side by side on a closed leather folder, 1979" + SEM, card="WASHINGTON, 1979")
b("En Bogotá gobierna Julio César Turbay. Resumido, el texto dice esto. Un colombiano acusado en Estados Unidos puede ser enviado allá para ser juzgado.",
  f"turbay_office|{TURBAY} sitting at a large desk in the presidential palace in Bogotá, reading papers, 1979" + SEM,
  "casa_narino|The Casa de Nariño presidential palace in Bogotá, white neoclassical facade, soldiers of the guard at the gate in dress uniform, 1979" + SEM,
  "us_court|The interior of an American federal courtroom in the late 1970s, wooden benches, an empty judge's bench, no flags with text" + SEM,
  "plane_stairs|A small airplane on a runway at dusk with its boarding stairs down, two men in suits walking toward it, 1980s, plain white fuselage without logo or lettering")
b("El narcotráfico figura entre los delitos del tratado. Para los traficantes que empiezan a llenar avionetas de cocaína rumbo a Florida, es una amenaza nueva: un juicio a miles de kilómetros de casa.",
  "airstrip_jungle|A small propeller plane taking off from a dirt airstrip cut in a Colombian jungle at dawn, 1979, plain fuselage without lettering",
  "map_caribe|" + MAPA + ", showing Colombia, the Caribbean Sea and Florida",
  "bales|Wrapped packages stacked inside the cabin of a small plane, seen from the cockpit door, dim light, 1979" + SEM,
  "miami_coast|The coast of South Florida seen from a small plane at night, city lights on the shoreline, 1979",
  "prison_wall|The long grey concrete wall and watchtower of an American federal prison under a pale sky, 1980" + SEM)
b("En mil novecientos ochenta, el Congreso aprueba el tratado con la Ley veintisiete. Pero esa ley no la firma el presidente, que está de viaje. Quien la firma, en su lugar, es un ministro delegatario: Germán Zea.",
  "congress_hall|The semicircular chamber of the Colombian Congress in 1980, dark wood desks, congressmen in suits, high windows" + SEM,
  "vote_hands|Congressmen raising their hands in a vote in a wood-paneled chamber, 1980",
  "plane_leaving|A presidential jet taking off from Bogotá airport in 1980, the Andes behind, plain white fuselage with no logo or lettering",
  f"zea_sign|{ZEA} signing a document at a desk in an empty ministry office, 1980" + SEM + "@@GERMÁN ZEA",
  "empty_chair|An empty presidential leather chair behind a large desk in a wood-paneled office, afternoon light, 1980")
b("Nadie lo advierte entonces. No es la firma del presidente.",
  f"signature_close|Extreme close-up of a fountain pen nib on {PAPER}, a fresh abstract ink stroke",
  "archive_box|A cardboard archive box being placed on a high shelf in a dusty government archive, 1980" + SEM, ideia=True)

# ───────────────────────── 2. EL PANFLETO ─────────────────────────
cap("2. El Panfleto")
b("El Panfleto. Cali, dos de diciembre de mil novecientos ochenta y uno. En pleno partido, una avioneta lanza miles de papeles sobre las tribunas del estadio Pascual Guerrero.",
  "stadium_cali|A packed football stadium in Cali, Colombia, during a night match in 1981, floodlights, crowds in the stands" + SEM,
  "plane_leaflets|A small propeller plane flying low over a football stadium, thousands of white papers falling from it over the crowd, 1981, plain fuselage without lettering",
  "leaflets_air|Thousands of small white papers fluttering down over stadium stands, fans raising their hands to catch them, floodlights, 1981" + SEM,
  "leaflet_hand|A fan's hand holding a small white leaflet seen from behind so no text is visible, stadium lights blurred behind" + SEM, card="CALI, 1981")
b("Anuncian un grupo nuevo: Muerte a Secuestradores, el MAS. Semanas antes, la guerrilla del eme diecinueve había secuestrado a Martha Nieves Ochoa. Es hermana de tres traficantes de Medellín.",
  "leaflets_ground|White leaflets scattered on the concrete steps of an empty stadium after a match, night" + SEM,
  "m19_car|A car speeding away on a street of Medellín at night in 1981, seen from behind, no license plate visible" + VIOL,
  "martha_house|A large family country house with a garden near Medellín, shutters closed, 1981, no people",
  "ochoa_brothers|Three Colombian brothers in their thirties in casual clothes standing together in silence in a hacienda courtyard, 1981, faces in shadow")
b("Según la revista Semana, el comunicado afirma que lo respaldan doscientos veintitrés jefes del narcotráfico. Dice que pondrán dinero y hombres para perseguir a los secuestradores.",
  "magazine_stand|A Colombian newsstand in 1981 with magazines hanging on strings, covers blurred and unreadable" + SEM,
  "meeting_table|A long table in a dim hacienda room surrounded by many men in shirts, seen from the end of the table, faces in shadow, 1981",
  "cash_case|An open briefcase on a table seen from a distance in half darkness, its content not visible, 1981",
  "jeeps_road|A line of jeeps driving on a dusty Antioquia mountain road at dusk, 1981, seen from far away" + NOARM)
b("En febrero de mil novecientos ochenta y dos, Martha Nieves vuelve a casa. Según varios historiadores, los grandes traficantes aprenden de ese episodio que, unidos, pueden presionar a cualquiera.",
  "house_door|The front door of a country house opening at dawn, warm light inside, a woman's silhouette on the threshold, 1982",
  "history_books|A stack of history books and newspapers on a library table, lamp light, 1980s" + SEM,
  "hands_table|Many men's hands resting on a dark table around a single closed folder, dim light" + SEM,
  "medellin_day|Medellín in 1982 seen from the hills, brick neighborhoods climbing the slopes of the valley, factories and the river, daylight")
b("Los hermanos Ochoa. Gonzalo Rodríguez Gacha. Carlos Lehder. Y un contrabandista criado en Envigado, Pablo Escobar. Ese grupo ya tiene dinero y armas. Ahora le falta una cosa: que el tratado nunca los alcance.",
  "ochoa_hacienda|A large white hacienda with a red tile roof among palm trees in the Magdalena valley, 1982, horses in a corral, no people close",
  "gacha|A Colombian man in his thirties with a round face, dark hair and a hat, a short-sleeved shirt, standing in a rural farmyard, 1982, resembling Gonzalo Rodríguez Gacha@@GONZALO RODRÍGUEZ GACHA",
  f"lehder_young|{LEHDER} on a tropical airstrip by a small plane, sunglasses pushed up, 1982@@CARLOS LEHDER",
  f"escobar_envigado|{ESCOBAR} standing on a street of Envigado in 1982, arms crossed, neighbors walking past@@PABLO ESCOBAR",
  "constitution_old|A leather-bound Colombian legal code on a shelf in a dark study, 1982" + SEM, ideia=True)

# ───────────────────────── 3. EL CHEQUE ─────────────────────────
cap("3. El Cheque")
b("El Cheque. Bogotá, mil novecientos ochenta y tres. En la Cámara de Representantes, un congresista muestra la copia de un cheque de un millón de pesos.",
  "camara_1983|The plenary chamber of the Colombian House of Representatives in 1983 during a heated session, congressmen standing, photographers" + SEM,
  f"ortega_cheque|{ORTEGA} standing at his desk in the chamber holding up a small paper slip seen from behind, other congressmen turning to look, 1983" + SEM,
  "cheque_close|Close-up of a hand holding a blank bank cheque photocopy, nothing written on it, flash of a camera" + SEM,
  "photographers|Press photographers with flash cameras crowding the gallery of a parliament chamber, 1983", card="BOGOTÁ, 1983")
b("Lo giró Evaristo Porras, un traficante de Leticia. Según el congresista, el dinero llegó al nuevo ministro de Justicia, Rodrigo Lara Bonilla. Lara explica que entró a una sociedad familiar como pago de un negocio.",
  "leticia|The river port of Leticia on the Amazon River in Colombia in 1983, wooden boats and stilt houses, humid jungle, daylight",
  f"lara_portrait|{LARA} in portrait in a ministry office, a determined look@@RODRIGO LARA BONILLA",
  f"lara_speech|{LARA} speaking firmly at a lectern in the chamber, one hand raised, 1983" + SEM,
  "ledger|An open accounting ledger with blank columns on a desk beside a calculator and a coffee cup, 1983" + SEM,
  "camara_wide|Wide shot of the Colombian Congress chamber from the public gallery, all congressmen looking toward one speaker, 1983")
b("El congresista es Jairo Ortega. Su suplente en la Cámara se llama Pablo Escobar.",
  f"ortega_portrait|{ORTEGA} in portrait at his desk in the chamber@@JAIRO ORTEGA",
  f"escobar_congress|{ESCOBAR} in a dark suit and tie sitting in the back row of a parliament chamber, a faint smile, 1983")
b("Lara contraataca: denuncia el dinero de la droga en la política. Y señala a Escobar. En octubre, Escobar pierde la inmunidad. Poco después se retira de la política.",
  f"lara_desk|{LARA} reading reports at night in a ministry office, a stack of folders, 1983",
  "lara_speech#médio-dir",
  "newspapers_press|A printing press running in a 1983 newspaper plant, sheets of newsprint flying through the rollers, unreadable" + SEM,
  "escobar_congress#detalhe-centro",
  "empty_seat|An empty leather seat in the back row of a parliament chamber, a nameplate removed, 1983" + SEM)
b("El treinta de abril de mil novecientos ochenta y cuatro, asesinan a Lara Bonilla en Bogotá. Belisario Betancur, que hasta entonces había negado las solicitudes de Estados Unidos, empieza a firmar extradiciones.",
  "lara_car|A white Mercedes-Benz car stopped on a residential street of north Bogotá at night in 1984, police lights in the distance, broken side window, seen from far away, no people" + VIOL,
  "funeral_crowd|A huge silent crowd with umbrellas in the Plaza de Bolívar in Bogotá for a funeral, 1984, seen from above" + SEM,
  f"betancur|{BETANCUR} signing a document at his desk in the presidential palace, a grave face, 1984" + SEM + "@@BELISARIO BETANCUR",
  "handcuffs_desk#médio-dir", ideia=True)

# ───────────────────────── 4. LOS PRIMEROS ─────────────────────────
cap("4. Los Primeros")
b("Los Primeros. Ciudad de Panamá, mayo de mil novecientos ochenta y cuatro. Escobar y Jorge Luis Ochoa, que han salido de Colombia, se reúnen con el expresidente Alfonso López Michelsen.",
  "panama_city|Panama City in 1984, modern hotel towers on the bay, palm trees, humid haze",
  "hotel_suite|A 1980s hotel suite with a view of the sea, two armchairs facing a sofa, a coffee table with cups, curtains half drawn",
  f"lopez|{LOPEZ} sitting in an armchair in a hotel suite, listening with his hands folded, 1984@@ALFONSO LÓPEZ MICHELSEN",
  card="PANAMÁ, 1984")
b("Según López Michelsen, le ofrecen un trato: desmontar el negocio y repatriar su dinero, a cambio de que no haya extradición.",
  f"escobar_offer|{ESCOBAR} in a light suit leaning forward on a sofa, talking, a younger Colombian man beside him, hotel suite, 1984",
  "lab_jungle|A clandestine laboratory of wooden huts in a jungle clearing being dismantled, plastic barrels, seen from far away, 1984" + SEM)
b("El gobierno no acepta. Y el cinco de enero de mil novecientos ochenta y cinco, por primera vez, Colombia entrega a cinco de sus ciudadanos a la justicia de Estados Unidos.",
  "tarmac_agents|American and Colombian agents in suits waiting on an airport tarmac at night under floodlights, 1985, seen from far away",
  "betancur#médio-esq",
  "bogota_airport_night|The El Dorado airport of Bogotá at night in 1985, a military cordon on the tarmac around a plain white plane without logo or lettering",
  "five_men|Five Colombian men in civilian clothes walking in a line toward a plane at night, escorted by agents, seen from behind, 1985")
b("Uno de ellos es Hernán Botero Moreno, que había presidido el Atlético Nacional, el club de fútbol de Medellín. Lo acusan de lavar más de cincuenta millones de dólares del narcotráfico. Pasará diecisiete años en prisión.",
  f"botero|{BOTERO} in portrait, a tired face, 1985@@HERNÁN BOTERO MORENO",
  "stadium_medellin|The Atanasio Girardot football stadium in Medellín in the early 1980s seen from the hills, green pitch, crowds" + SEM,
  "bank_counter|The counter of a 1980s bank with stacks of blank deposit slips and a calculator, no logos" + SEM,
  "us_prison_cell|A narrow American prison cell in the 1980s with a metal bunk and a small window, empty")
b("La palabra ya no es un papel en Washington. Es un vuelo que sale de Bogotá. Y los capos empiezan a llamarse a sí mismos los Extraditables. Su blanco siguiente serán los jueces.",
  f"plane_night_takeoff|{PLANE} taking off from Bogotá at night, the lights of the city below, 1985",
  "communique|A typewriter with a blank sheet of paper in a dark room, a single bulb, 1985" + SEM,
  "courthouse|The facade of an old Colombian courthouse in Bogotá with stone columns, 1985, no inscription" + SEM, ideia=True)

# ───────────────────────── 5. EL JUEZ ─────────────────────────
cap("5. El Juez")
b("El Juez. Bogotá, veintitrés de julio de mil novecientos ochenta y cinco. Asesinan al juez Tulio Manuel Castro Gil.",
  "bogota_street_1985|A grey street of central Bogotá in 1985, buses and taxis, office workers with umbrellas" + SEM,
  "taxi_door|A taxi stopped by the curb with its rear door open on a rainy Bogotá street, police cars arriving, seen from far away, no people near" + VIOL,
  card="BOGOTÁ, 1985")
b("Nueve meses antes, él había llamado a juicio a Pablo Escobar por el asesinato de Lara Bonilla.",
  "escobar_summons|A court summons of blank pages being stamped on a clerk's counter, 1984",
  f"juez_desk|{JUEZ} working at a desk piled with case files in a small courtroom office, 1984" + SEM + "@@TULIO MANUEL CASTRO GIL",
  "files_desk#detalhe-alto")
b("No es el único. Muchos jueces que llevan procesos contra el cártel denuncian amenazas en casa, por teléfono y por correo. A sus familias también.",
  "phone_ring|An old rotary telephone ringing on a nightstand in a dark bedroom, a woman sitting up in bed, 1985",
  "envelope|A plain white envelope slipped under an apartment door, seen from inside, morning light" + SEM)
b("En noviembre, la guerrilla del eme diecinueve toma el Palacio de Justicia. En la toma y en la operación militar para recuperarlo mueren once magistrados de la Corte Suprema. Si el cártel tuvo algo que ver, todavía se discute.",
  "tanks_square|Armored vehicles in the stone Plaza de Bolívar in Bogotá, soldiers taking cover behind them, smoke in the air, November 1985, seen from far away, no bodies, no blood",
  "magistrates_portraits|A wall of framed black and white portraits of judges in a court hallway, one frame empty, 1986",
  "palacio_smoke|The Palace of Justice on Plaza de Bolívar in Bogotá with black smoke rising from its windows, armored vehicles in the square, November 1985" + VIOL,
  "palacio_ruin|The burnt-out facade of the Palace of Justice in Bogotá the morning after, blackened windows, soldiers far away" + VIOL + SEM,
  "empty_bench|A row of eleven empty high-backed judges' chairs in a dim courtroom, 1985")
b("La Corte que debe decidir sobre el tratado queda diezmada. Un año después, la nueva Corte decide.",
  "court_corridor|A long marble corridor of a provisional courthouse in Bogotá, 1986, judges walking far away",
  "empty_bench#médio-dir",
  "new_judges|Judges in black robes walking into a provisional courtroom, seen from behind, 1986", ideia=True)

# ───────────────────────── 6. LA SENTENCIA ─────────────────────────
cap("6. La Sentencia")
b("La Sentencia. Bogotá, doce de diciembre de mil novecientos ochenta y seis. La Corte Suprema declara inconstitucional la ley que aprobó el tratado.",
  "court_session|A session of the Colombian Supreme Court in 1986, judges in black robes around a long table, papers, lamp light" + SEM,
  "gavel_paper|A thick bound ruling with blank pages lying on a judge's table, reading glasses on top, 1986" + SEM, card="BOGOTÁ, 1986")
b("La Corte encuentra un defecto de forma. El problema no es lo que dice el tratado. Es quién firmó la ley: aquel ministro delegatario, en mil novecientos ochenta.",
  "law_book|An old leather-bound law book open on a judge's desk with blank pages, reading glasses, 1986",
  "zea_sign#detalhe-centro",
  "signature_close#detalhe-alto",
  "archive_box#aberto")
b("Dos días después, el presidente Virgilio Barco vuelve a firmar la ley. Esta vez, él mismo.",
  f"barco_sign|{BARCO} signing a document at the presidential desk with a fountain pen, aides behind him, 1986" + SEM + "@@VIRGILIO BARCO")
b("Tres días más tarde asesinan en Bogotá a Guillermo Cano, director de El Espectador, el diario que llevaba años denunciando al cártel.",
  f"cano|{CANO} in portrait in a newspaper office at night, typewriters behind him@@GUILLERMO CANO",
  "cano_car|A small car stopped at the exit of a newspaper building on a Bogotá avenue at night, December 1986, police lights, seen from far away, no people" + VIOL + SEM)
b("Con la ley firmada de nuevo, el cuatro de febrero de mil novecientos ochenta y siete, la Policía captura a Carlos Lehder en una finca cerca de Guarne, en Antioquia. En menos de veinticuatro horas viaja en un avión rumbo a Estados Unidos.",
  f"lehder_plane_window|{LEHDER} looking out of a small plane window at the clouds, handcuffed hands in his lap, 1987",
  "tampa_arrival|Agents escorting a bearded handcuffed man across an American airport tarmac in bright sunshine, 1987, seen from far away",
  "finca_guarne|A country house among pine trees in the green hills of Guarne, Antioquia, at dawn, police jeeps arriving, 1987" + NOARM,
  f"lehder_arrest|{LEHDER} in handcuffs being walked to a jeep by plainclothes police, rural yard, 1987" + NOARM,
  "plane_dea|A twin-engine plane on a runway at dawn with its stairs down, men in windbreakers escorting a handcuffed man aboard, seen from far away, plain fuselage without logo or lettering")
b("Pero en junio de mil novecientos ochenta y siete, la Corte anula también la nueva ley, por un vicio de trámite. La extradición queda otra vez en el aire. Y la violencia se intensifica.",
  "court_ruling2|Judges in black robes leaving a courtroom in silence, seen from behind, June 1987",
  "court_session#médio-dir",
  "medellin_night#detalhe-centro", ideia=True)

# ───────────────────────── 7. EL ESTADO DE SITIO ─────────────────────────
cap("7. El Estado de Sitio")
b("El Estado de Sitio. Bogotá, dieciocho de agosto de mil novecientos ochenta y nueve. El presidente Virgilio Barco firma, bajo estado de sitio, el decreto mil ochocientos sesenta.",
  "ministers_night|Colombian ministers in suits arguing around a table in the presidential palace at night, 1989, cigarette smoke",
  f"barco_night|{BARCO} at his desk late at night with ministers standing around him, a single lamp, 1989" + SEM,
  "decree_desk|A decree of blank pages with a fountain pen on top lying on a presidential desk at night, 1989" + SEM, card="BOGOTÁ, 1989")
b("La extradición ya no necesita una ley aprobada por el Congreso. Basta una decisión del gobierno.",
  "congress_empty|The empty chamber of the Colombian Congress at night, rows of dark wood desks, 1989",
  "handcuffs_desk#detalhe-alto")
b("Ese mismo día, en Soacha, asesinan a Luis Carlos Galán, el candidato favorito a la presidencia. Cinco días después, los Extraditables declaran la guerra total al Estado.",
  "soacha_square|The main square of Soacha at night with a crowd and a wooden stage, campaign flags without text, 1989, seen from far away",
  f"galan_rally|{GALAN} on a stage at a night rally in a town square, crowds with flags without text, seen from far away, 1989" + SEM + "@@LUIS CARLOS GALÁN",
  "empty_stage|An empty wooden stage in a town square at night after a rally, a fallen microphone stand, scattered papers" + VIOL + SEM,
  "communique#detalhe-centro")
b("Siguen meses de atentados: un avión de Avianca derribado en pleno vuelo, con ciento diez muertos, la sede del DAS en Bogotá, bancos, centros comerciales. La justicia los atribuyó al cártel. En Medellín asesinan a cientos de policías.",
  "shattered_glass|Shattered shop windows along a Bogotá street after an explosion, dust in the air, nobody in the street, 1989",
  "mall_police|Soldiers guarding the entrance of a Medellín shopping center in 1990, shoppers passing",
  "smoke_mountain|A column of black smoke rising from a green mountainside near Bogotá, seen from very far away, November 1989, no wreckage visible",
  "das_building|A damaged office building in Bogotá with all its windows blown out, smoke and dust in the street, seen from far away, December 1989" + VIOL + SEM,
  "police_station|A small police station on a Medellín street at night with sandbags at the door, a lone policeman, 1990" + SEM + NOARM)
b("El Estado responde en los tribunales. Desde noviembre de mil novecientos noventa, en los procesos de narcotráfico hay jueces sin rostro: su identidad queda en reserva, para que nadie pueda amenazarlos.",
  "courtroom_screen|A Colombian courtroom with a large frosted glass partition in front of the judge's bench, lawyers at tables, 1991",
  "faceless_judge|A judge sitting behind a dark one-way glass screen in a courtroom, only a silhouette visible, a microphone in front, 1990",
  "voice_mic|Close-up of a microphone and a voice-distorting device on a courtroom table, 1990" + SEM)
b("Pero el cártel recurre a otra forma de presión, más cruel que una bomba: el secuestro.",
  "dark_room|A small bare room with a mattress on the floor and a boarded window, a single bulb, 1990, no people", ideia=True)
b("Si este expediente te muestra una Colombia que no conocías, suscríbete. Cada semana abrimos uno nuevo. Ahora, volvemos a Diana Turbay.",
  "case_board|A cork board with blank photographs, strings and pins in a dim office, 1990",
  "files_desk#médio-dir",
  "diana_portrait#detalhe-centro")

# ───────────────────────── 8. LOS REHENES ─────────────────────────
cap("8. Los Rehenes")
b("Los Rehenes. Bogotá, treinta de agosto de mil novecientos noventa. Diana Turbay dirige la revista Hoy por Hoy y el noticiero Criptón. Sale de viaje con cinco personas de su equipo.",
  f"diana_studio|{DIANA} presenting a news program in a television studio, studio lights, 1990",
  f"diana_newsroom|{DIANA} in a busy 1990 television newsroom, monitors and editing desks, talking with colleagues" + SEM,
  "team_van|A small team of journalists with a TV camera and bags loading a van on a Bogotá street at dawn, 1990" + SEM, card="BOGOTÁ, 1990")
b("Le han prometido una entrevista con el cura Manuel Pérez, jefe de la guerrilla del ELN. Es una trampa. Según reconstruyó García Márquez, los esperan hombres de los Extraditables.",
  "mountain_road|A van driving on a winding mountain road in Antioquia, 1990, seen from far away",
  "men_waiting|Silhouettes of men waiting by a jeep at a bend of a mountain road, dusk, faces not visible" + NOARM,
  "gabo_books|A worn copy of a novel with a plain cover, no title, on a wooden table beside reading glasses" + SEM)
b("El diecinueve de septiembre secuestran a Francisco Santos, jefe de redacción de El Tiempo. Y a Marina Montoya, hermana del secretario general de la Presidencia del gobierno anterior.",
  f"santos|{SANTOS} in portrait in a newspaper office@@FRANCISCO SANTOS",
  "car_street|A car blocked by another car on a Bogotá street at evening, doors open, seen from far away, 1990" + VIOL,
  f"montoya|{MONTOYA} in portrait@@MARINA MONTOYA")
b("En noviembre secuestran a Maruja Pachón, directora de Focine y cuñada de Luis Carlos Galán. Y a Beatriz Villamizar, cuñada de Maruja.",
  f"maruja|{MARUJA} in portrait@@MARUJA PACHÓN",
  f"beatriz|{BEATRIZ} in portrait@@BEATRIZ VILLAMIZAR")
b("No los eligen al azar. Todos tienen vínculos con el poder. García Márquez lo cuenta en Noticia de un secuestro: los rehenes eran su forma de presionar al gobierno.",
  "gabo_portrait|An older Colombian writer with grey curly hair and a grey moustache, writing at a desk by a window, resembling Gabriel García Márquez@@GABRIEL GARCÍA MÁRQUEZ",
  "hostage_room|A small dim room with two mattresses, a television set on a chair and a boarded window, 1990",
  "tv_flicker|An old television set glowing in a dark room, the screen showing only static, 1990")
b("Desde septiembre, el nuevo presidente, César Gaviria, ofrece una salida. Quien se entregue y confiese un delito tendrá rebaja de pena y no será extraditado. Al cártel no le basta. Quiere que nadie, nunca, pueda ser extraditado.",
  f"gaviria_palace|{GAVIRIA} walking through a colonnade of the presidential palace with aides, 1990",
  "surrender_doc|A thick government decree of blank pages with an official seal of plain wax on a desk, 1990",
  f"gaviria|{GAVIRIA} speaking on television from the presidential palace, 1990" + SEM + "@@CÉSAR GAVIRIA",
  "decree_desk#médio-esq",
  "handcuffs_desk#aberto", ideia=True)

# ───────────────────────── 9. LA OPERACIÓN ─────────────────────────
cap("9. La Operación")
b("La Operación. Copacabana, veinticinco de enero de mil novecientos noventa y uno. Volvemos a la finca de la montaña.",
  "valley_morning|The Aburrá valley north of Medellín in the morning, mist over the green mountains of Copacabana, 1991",
  "andes_day#médio-esq",
  "farmhouse_close|A white farmhouse with a clay tile roof and a wooden balcony on a steep Antioquia slope, morning mist, 1991, no people", card="COPACABANA, 1991")
b("La familia no sabía nada de la operación. Diana había pedido a los suyos que evitaran cualquier intento de rescatarla por la fuerza.",
  "family_room|A worried elderly couple sitting in an elegant living room in Bogotá by a telephone, 1991, seen from the doorway",
  f"diana_letter|{DIANA} writing a letter by hand at a small table in a bare room, 1990" + SEM)
b("Ese día llega un grupo de élite de la Policía con helicópteros. El gobierno dirá que no buscaban a Diana, sino a hombres del cártel.",
  "heli_cockpit|View from inside a police helicopter cockpit over green Andean slopes, the pilot's gloved hands, no instruments with text, 1991",
  "heli_approach#médio-dir",
  "police_slope|Police officers in dark uniforms advancing in a line through a coffee plantation on a slope, seen from far away, 1991" + NOARM)
b("Los captores la sacan corriendo. Recibe un disparo en la espalda. La versión oficial culpa a los secuestradores. Otras versiones no descartan que el disparo viniera de la propia operación.",
  "coffee_path|A narrow muddy path between coffee plants on a steep slope, broken branches, no people, 1991",
  "run_slope#detalhe-centro",
  "banana_leaves|Banana leaves shaking violently in the wind of a helicopter, a slope of coffee plants, no people",
  "heli_farm#detalhe-alto")
b("La llevan en helicóptero a Medellín. Muere en el Hospital General, al final de la tarde.",
  "heli_valley|A single plain dark helicopter flying over the valley of Medellín at sunset, seen from far away",
  "hospital_corridor#médio-dir")
b("Días después, los Extraditables anuncian que han ejecutado a Marina Montoya. Y el país entiende que la guerra por una palabra ya alcanza a cualquiera.",
  "nydia|An elegant Colombian woman in her sixties with blond hair, a dark coat, a grieving determined face, 1991, resembling Nydia Quintero@@NYDIA QUINTERO",
  "montoya#médio-dir",
  "candles|Rows of candles burning on a church step in Bogotá at night, January 1991, people's legs passing", ideia=True)

# ───────────────────────── 10. EL SACERDOTE ─────────────────────────
cap("10. El Sacerdote")
b("El Sacerdote. Bogotá, mayo de mil novecientos noventa y uno. Rafael García Herreros tiene ochenta y dos años y un programa de televisión de pocos minutos: El Minuto de Dios.",
  "minuto_dios|A small brick church of a working-class neighborhood in Bogotá at evening, 1991, no inscriptions",
  f"gh_tv|{GH} speaking to a television camera in a small studio, a simple cross on the wall behind, 1991" + SEM + "@@RAFAEL GARCÍA HERREROS",
  "tv_studio|A small 1991 television studio with one camera and studio lights, seen from behind the camera" + SEM, card="BOGOTÁ, 1991")
b("Desde la pantalla le habla a Pablo Escobar. Le pide que se entregue.",
  "tv_living|A family living room in Colombia at night, a television showing an old priest, people watching from the sofa, 1991" + SEM,
  f"escobar_hiding|{ESCOBAR} in his early forties, heavier, with a beard, watching a small television in a hideout room, 1991")
b("Alberto Villamizar, el esposo de Maruja Pachón, lleva meses negociando por su cuenta para salvarla. Y busca al sacerdote.",
  f"villamizar|{VILLAMIZAR} in portrait in his apartment, a tired determined face@@ALBERTO VILLAMIZAR",
  f"villamizar_gh|{VILLAMIZAR} talking with {GH} in a modest parish office, 1991")
b("Según el relato de García Márquez, Escobar acepta que el sacerdote sea el testigo de su entrega.",
  "embrace|A woman embracing her husband in the doorway of an apartment at night, seen from the corridor, 1991",
  "letter_hand|A hand-written letter on lined paper being folded and put into an envelope, seen from a few steps away, no readable words" + SEM,
  "gabo_books#detalhe-centro")
b("El veinte de mayo, tras seis meses de cautiverio, los captores liberan a Maruja Pachón. Ese mismo día, también a Francisco Santos.",
  "gh_escobar_meet|An old priest in a black cassock walking up a muddy mountain path at night with two men holding flashlights, seen from behind, 1991",
  "release_street|A woman walking alone on a dark Bogotá street at night toward the headlights of a waiting car, May 1991, seen from behind",
  "maruja#médio-dir",
  "santos#médio-esq")
b("Pero Escobar todavía no se entrega. Espera una sola cosa. Una frase escrita en otra parte de Bogotá.",
  "radio_listen|A man listening to a small radio by a window in a dark hideout, his face in shadow, 1991",
  "escobar_hiding#detalhe-centro",
  "assembly_hall|The large hall of the Colombian National Constituent Assembly in 1991, delegates at long tables, a high ceiling", ideia=True)

# ───────────────────────── 11. EL ARTÍCULO ─────────────────────────
cap("11. El Artículo")
b("El Artículo. Bogotá, diecinueve de junio de mil novecientos noventa y uno. La Asamblea Nacional Constituyente escribe una Constitución nueva para Colombia.",
  "assembly_wide|The National Constituent Assembly of Colombia in session in June 1991, delegates of all kinds including indigenous representatives, seen from the gallery" + SEM,
  "constitution_draft|A thick draft constitution of blank pages on a table with many pens and coffee cups, 1991" + SEM, card="BOGOTÁ, 1991")
b("Ese día vota un artículo cuya frase central dice: «Se prohíbe la extradición de colombianos por nacimiento».",
  "typewriter_line|Close-up of a typewriter carriage with a blank sheet of paper, keys in motion, 1991" + SEM,
  "redacted_page|Extreme close-up of an old typewritten sheet of completely blank paper on a desk, one thick black bar across the middle, lamp light" + SEM)
b("Cincuenta y uno a favor. Trece en contra. Cinco abstenciones.",
  "vote_board|Delegates raising their hands in a vote in a large assembly hall, 1991",
  "assembly_hall#detalhe-centro")
b("Horas después, un helicóptero aterriza en una cárcel nueva en las montañas de Envigado, sobre Medellín. De él baja Pablo Escobar. Se entrega junto al sacerdote García Herreros y a Alberto Villamizar.",
  "catedral_mountain|A newly built prison compound of low brick buildings and a fence high on a forested mountain above the valley of Medellín, evening, 1991",
  f"heli_landing|A plain white helicopter without markings landing on a mountain clearing beside a prison fence at dusk, figures stepping out, seen from far away, 1991",
  f"escobar_surrender|{ESCOBAR} in his early forties stepping out of a helicopter beside an old priest in a cassock, seen from a distance at dusk, 1991")
b("Según investigaciones posteriores, el lugar lo había escogido él. La llamaban La Catedral.",
  "catedral_gate|The gate of a mountain prison with a simple fence and a guard hut, mist and pine trees, 1991" + SEM + NOARM,
  "catedral_mountain#detalhe-alto")
b("La extradición, la palabra por la que el cártel hizo la guerra, quedaba prohibida en la nueva Constitución. Por un tiempo, parecieron intocables.",
  "constitution_book|A small new copy of a national constitution with a plain blue cover and no letters on a wooden table, 1991",
  "redacted_page#detalhe-centro",
  "handcuffs_desk#detalhe-baixo", ideia=True)

# ───────────────────────── 12. LA FUGA ─────────────────────────
cap("12. La Fuga")
b("La Fuga. Envigado, julio de mil novecientos noventa y dos. Tras las denuncias de que Escobar ordenaba asesinatos desde La Catedral, el gobierno decide trasladarlo.",
  "catedral_night|A mountain prison compound at night surrounded by army trucks with headlights, fog, July 1992, seen from far away" + NOARM,
  "soldiers_fog|Soldiers in a line among pine trees in thick night fog on a mountain, seen from behind" + NOARM, card="ENVIGADO, 1992")
b("En la noche del veintiuno al veintidós de julio, Escobar escapa con varios de sus hombres, aunque la cárcel está rodeada por el Ejército. Es un duro golpe para el Estado.",
  "army_trucks|Army trucks with headlights on a muddy mountain road at night, fog, 1992",
  "fence_hole|A gap in a prison fence among pine trees at night, fog, footprints in the mud, no people",
  "empty_cell_catedral|An empty prison room with a bed, a bookshelf and a television, lights on, nobody inside, 1992")
b("Empieza la persecución. La Policía refuerza su Bloque de Búsqueda. Y aparece otro grupo ilegal, Los Pepes, formado por antiguos socios y rivales de Escobar, que asesinan a sus allegados.",
  "search_bloc|Colombian police officers studying a map pinned to a wall in a makeshift operations room, radios on the table, 1993" + SEM,
  "radio_antenna|A radio direction-finding antenna on the roof of a van on a Medellín street, 1993" + SEM,
  "burned_house|A burned country house in the hills near Medellín, charred walls, seen from far away, 1993, no people" + VIOL)
b("El dos de diciembre de mil novecientos noventa y tres, Escobar muere en Medellín durante un operativo de la Policía. Acababa de cumplir cuarenta y cuatro años.",
  "police_street|Police cars blocking a residential street in Medellín in the afternoon, neighbors watching from windows, December 1993, seen from far away, no bodies, no blood",
  "rooftops|The red tile rooftops of a middle-class neighborhood of Medellín in the afternoon, December 1993, police far away on a street, no people on the roofs" + VIOL,
  "medellin_day#detalhe-centro")
b("Para entonces, Rodríguez Gacha había muerto en un operativo policial, en mil novecientos ochenta y nueve. Y Lehder seguía preso en Estados Unidos.",
  "miami_court|An American federal courthouse with steps and columns under bright Florida sun, 1990s, no inscription",
  "gacha#médio-dir",
  "us_prison_cell#detalhe-centro")
b("El Cártel de Medellín se desmorona. Pero la extradición sigue prohibida en la Constitución.",
  "closed_files|Stacks of closed brown case files tied with string on a long table in an archive, dust in a beam of light",
  "files_desk#detalhe-baixo",
  "redacted_page#aberto", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. La Palabra")
b("La Palabra. Bogotá, dieciséis de diciembre de mil novecientos noventa y siete. El Congreso aprueba el Acto Legislativo número uno. La extradición de colombianos vuelve a la Constitución.",
  "congress_vote97|Congressmen raising their hands in a vote in the Colombian Capitol chamber, December 1997",
  "congress_1997|The Colombian Congress chamber in session in December 1997, congressmen voting, Christmas season light" + SEM,
  "bogota_capitol#médio-dir", card="BOGOTÁ, 1997")
b("No es retroactiva. Pero en mil novecientos noventa y nueve capturan a Fabio Ochoa, hermano de Martha Nieves, acusado de seguir traficando después de esa fecha. En septiembre de dos mil uno lo extraditan a Estados Unidos.",
  "operation_milenio|Police officers in dark windbreakers escorting a man into a building at night, flashes of cameras, 1999, seen from far away",
  f"fabio_arrest|{FABIO} escorted by Colombian police officers in an airport hallway, October 1999" + NOARM + SEM + "@@FABIO OCHOA",
  f"plane_2001|{PLANE} on a runway at dawn in 2001, a police cordon around it")
b("Desde entonces, Colombia ha extraditado a miles de personas. Según El Tiempo, solo entre dos mil diez y dos mil veinte fueron cerca de mil novecientas.",
  "diana_archive|A framed black and white photograph of a woman journalist on a shelf among books, a small candle beside it, no text",
  "plane_night_takeoff#detalhe-centro",
  "handcuffs_desk#médio-esq")
b("Diana Turbay no alcanzó a verlo. Murió casi siete años antes, secuestrada, en la guerra contra un tratado firmado durante el gobierno de su padre.",
  "memorial_wall|A long wall with hundreds of small blank plaques in a Medellín memorial park, flowers at its base, no names readable",
  "diana_portrait#médio-dir",
  "turbay_portrait#detalhe-centro",
  "treaty_folder#aberto")
b("Durante más de seis años, la Constitución prohibió la extradición. La violencia de esa guerra costó la vida a cientos de policías, jueces, periodistas y civiles. Y al final, la palabra volvió.",
  "medellin_today|Medellín today seen from the hills at dusk, cable cars crossing over the neighborhoods, city lights",
  "candles#médio-dir",
  "empty_bench#detalhe-centro",
  "andes_day#aberto", ideia=True)
b("Y tú, ¿qué crees que aprendió Colombia de esta guerra? ¿Qué parte de esta historia no conocías? Déjalo en los comentarios.",
  "typewriter_end|A typewriter with a blank sheet on a dark desk, a lamp switching off",
  "folder_close|A hand closing a thick brown case file with a red circular stamp on a dark desk, lamp light" + SEM,
  "red_stamp#médio-esq", "bogota_capitol#aberto")

# Thumbs (EMBALAGEM.md aprovado no crivo r3): A algemas abertas em close sobre mesa escura (sigla MEDELLÍN cor papel + sello
# INTOCABLES no código); B página datilografada em branco ocupando o quadro (tarja preta, linhas e "ART. 35" no código, sem
# carimbo vermelho); C de dia, helicópteros sobre a fazenda branca na montanha ("¿RESCATE?" em sello com fundo papel no código).
THUMBS = [
    {"id": "thumb-A", "prompt": "Ink graphic novel illustration: close three-quarter view of a large pair of open steel handcuffs lying on a dark wooden desk, one cuff hanging over the edge, strong desk lamp light from upper left, bright metallic shine, deep slate blue dark background, the handcuffs occupy the LEFT 60 percent of the frame, the RIGHT side is empty dark background, no paper, no text, no lettering, no numbers, absolutely NO red color, no blood, no weapons"},
    {"id": "thumb-B", "prompt": "Ink graphic novel illustration: extreme close-up of a single old typewritten sheet of cream paper filling almost the entire frame, slightly tilted, completely blank paper with no letters, no words, no marks, soft warm lamp light, only a thin dark edge of desk visible at the right border, no stamp, no red color, no text, no lettering"},
    {"id": "thumb-C", "prompt": f"Ink graphic novel illustration: daytime wide shot of {ANDES} under low grey clouds, a white farmhouse with a clay tile roof large in the LEFT third of the frame occupying at least a third of the image height, two dark police helicopters without any markings flying low over the coffee slope near the house, tiny distant figures running among the coffee plants, no weapons visible, no bodies, no blood, the RIGHT half is open pale sky, no text, no lettering"},
]
# a 1ª prova do 001 (04/11) saiu com moldura de papel: todo prompt leva sangria explícita
SANGRIA = ", full-bleed illustration filling the entire frame edge to edge, no border, no margin, no white frame, no panel outline"
# ───────────────────────── geração ─────────────────────────
TAG = re.compile(r"\[[^\]]*\]\s*")   # [break], [long-break], [emphasis] e as tags de tom ([curious] etc.)
def limpo(t): return re.sub(r"\s+", " ", TAG.sub("", t)).strip()
def falado(t):
    n = 0
    for w in limpo(t).split():
        d = re.sub(r"\D", "", w)
        n += (5 if len(d) == 4 else 3 if len(d) == 3 else 2 if d else 1) if d and d == w.strip(".,:;?!") else 1
    return n
def dur(t): return falado(t) / WPS + t.count("[break]") * BREAK + t.count("[long-break]") * LONG + 0.1
def fmt(s): return f"{int(s // 60)}:{s % 60:04.1f}"

def main():
    out = Path(__file__).parent
    blocos, cenas, prompts, planos, script, avisos = [], [], {}, [], [], []
    ids, uso = {}, {}              # chave -> I###; (chave, enq) -> último início
    t, n = 0.0, 0
    for blk in B:
        if "cap" in blk:
            script.append(f"\n## {blk['cap']}\n"); cap_atual = blk["cap"]; marca_cap = True; continue
        n += 1; bid = f"N{n:03d}"
        blocos.append({"id": bid, "texto": blk["t"], "ideia": blk["ideia"]})
        script.append(f"**[{bid}]** {limpo(blk['t'])}\n")
        d = dur(blk["t"])
        specs = []
        for s in blk["s"]:
            s, _, rot = s.partition("@@")
            if "|" in s:
                k, p = s.split("|", 1)
                assert k not in prompts, f"chave repetida {k}"
                prompts[k] = p; specs.append((k, None, rot or None))
            else:
                k, _, e = s.partition("#"); assert k in prompts, f"{bid}: chave {k} sem prompt antes"
                specs.append((k, e or None, rot or None))
        if not specs:   # roteiro antes do storyboard: bloco ainda sem planos
            avisos.append(f"{bid}: sem planos"); prompts.setdefault("_tbd", "TBD"); specs = [("_tbd", None, None)]
        need = math.ceil(d / (MAX_PLANO_INICIO if t < INICIO else MAX_PLANO))
        if len(specs) < need:
            if t + d <= INEDITO_ATE + 5:
                avisos.append(f"{bid} ({fmt(t)}): faltam planos novos ({len(specs)}/{need})")
            else:
                proprias = [k for k, _, _ in specs] or [planos[-1]["chave"]]
                i = 0
                while len(specs) < need:
                    specs.insert(min(2 * i + 1, len(specs)), (proprias[i % len(proprias)], None, None)); i += 1
        palavras = limpo(blk["t"]).split()
        cada = d / len(specs)
        for j, (k, e, rot) in enumerate(specs):
            ini = t + j * cada
            nova = k not in ids
            if nova:
                ids[k] = f"I{len(ids) + 1:03d}"
                cenas.append({"id": ids[k], "prompt": prompts[k] + SANGRIA})
                enq, mov = "aberto", MOV_NOVO[len(ids) % len(MOV_NOVO)]
            else:
                if ini < INEDITO_ATE: avisos.append(f"{bid} ({fmt(ini)}): reuso antes de 3:00 ({k})")
                cand = [e] if e else ENQ
                livres = [c for c in cand if ini - uso.get((k, c), -1e9) >= JANELA]
                nunca = [c for c in livres if (k, c) not in uso]
                if planos and planos[-1]["chave"] == k:   # mesmo plano anterior: evita repetir o recorte
                    nunca = [c for c in nunca if c != planos[-1]["enq"]]
                enq = (nunca or livres or cand)[0]
                if not livres: avisos.append(f"{bid} ({fmt(ini)}): {k}/{enq} repetido em < {JANELA:.0f}s")
                mov = MOV_ENQ[enq]
            uso[(k, enq)] = ini
            a, z = round(j * len(palavras) / len(specs)), round((j + 1) * len(palavras) / len(specs))
            nota = []
            if marca_cap and j == 0: nota.append(f"capítulo: {cap_atual}"); marca_cap = False
            if blk["card"] and j == 0: nota.append(f"cartão de data: {blk['card']}")
            if rot: nota.append(f"rótulo: {rot}")
            if rot and len(rot) > 30: avisos.append(f"{bid}: rótulo longo ({rot})")
            if cada < 1.8 or cada > MAX_PLANO + 0.5: avisos.append(f"{bid}: plano de {cada:.1f}s")
            planos.append({"plano": len(planos) + 1, "ini": round(ini, 2), "fim": round(ini + cada, 2),
                           "bloco": bid, "trecho": " ".join(palavras[a:z]), "chave": k, "imagem": ids[k],
                           "nova": nova, "enq": enq, "mov": mov, "rot": rot, "nota": "; ".join(nota)})
        if cap_atual == "Hook" and t + d > HOOK_MAX: avisos.append(f"{bid}: hook passa de {HOOK_MAX:.0f}s ({fmt(t + d)})")
        t += d

    total = t
    cenas.extend({"id": t["id"], "prompt": t["prompt"] + SANGRIA} for t in THUMBS)
    reuso = [p for p in planos if not p["nova"]]
    apos = [p for p in planos if p["ini"] >= INEDITO_ATE]
    reuso_apos = [p for p in apos if not p["nova"]]
    words = sum(len(limpo(b_["texto"]).split()) for b_ in blocos)
    stats = {"palavras": words, "duracao_s": round(total), "planos": len(planos),
             "imagens_video": len(ids), "imagens_total": len(cenas),
             "reuso_pct": round(100 * len(reuso) / len(planos), 1),
             "reuso_pct_apos_3min": round(100 * len(reuso_apos) / max(1, len(apos)), 1),
             "plano_medio_s": round(total / len(planos), 2),
             "cortes_1o_min": sum(1 for p in planos if p["ini"] < 60), "rotulos": sum(1 for p in planos if p["rot"]),
             "capitulos": sum(1 for x in B if "cap" in x and x["cap"][0].isdigit()), "avisos": avisos}

    (out / "blocos.json").write_text(json.dumps(blocos, ensure_ascii=False, indent=1) + "\n")
    (out / "cenas.json").write_text(json.dumps(cenas, ensure_ascii=False, indent=1) + "\n")
    (out / "storyboard.json").write_text(json.dumps({"stats": stats, "planos": planos}, ensure_ascii=False, indent=1) + "\n")
    (out / "SCRIPT.md").write_text(
        f"# {TITULO} en {round(total / 60)} minutos: roteiro\n\n"
        f"Gerado por `roteiro.py` (fonte única; edite lá). {words} palavras, ~{fmt(total)} estimados a {WPS*60:.0f} ppm (com as pausas entre frases).\n"
        "Os blocos [Nxxx] são os mesmos de `blocos.json` (lá com as tags do Fish).\n" + "\n".join(script))
    linhas = [f"# Storyboard: {TITULO}",
              "",
              f"Gerado por `roteiro.py`. {len(planos)} planos em ~{fmt(total)} (média de {stats['plano_medio_s']} s), "
              f"{len(ids)} imagens únicas no vídeo + thumb-base, reuso de {stats['reuso_pct']}% "
              f"({stats['reuso_pct_apos_3min']}% depois dos 3 min; 0% antes).",
              "",
              "Tempos estimados a 150 ppm; o render deve reescalar cada bloco pela duração real do áudio. "
              "Enquadramentos: aberto = imagem inteira; médio-esq/dir = ~1,4x no terço; detalhe-* = ~1,8–2x na região. "
              "Cartões de data e rótulos de mapa são feitos no código (serifa), sobre a imagem.",
              "",
              "| plano | tempo | bloco | narração | imagem | nova/reuso | enquadramento | movimento | nota |",
              "|---|---|---|---|---|---|---|---|---|"]
    for p in planos:
        linhas.append(f"| {p['plano']} | {fmt(p['ini'])}–{fmt(p['fim'])} | {p['bloco']} | {p['trecho']} | "
                      f"{p['imagem']} `{p['chave']}` | {'nova' if p['nova'] else 'reuso'} | {p['enq']} | {p['mov']} | {p['nota']} |")
    (out / "STORYBOARD.md").write_text("\n".join(linhas) + "\n")
    print(json.dumps(stats, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
