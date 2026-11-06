#!/usr/bin/env python3
"""Fonte única do dossie-es 004 (Cosa Nostra): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (na pasta do vídeo). Conteúdo no topo; geração no fim (copiada do 003-fbi).

Molde da bíblia (canais/dossie-es/biblia/roteiro.md): hook por anedota (o juramento da estampa queimada de Tommaso Buscetta,
Palermo, 1945; os concorrentes em es/en abrem com a origem na Sicília, os limões ou "imagina vivir…") → 13 expedientes-objeto com
título falado → pagamento da anedota no expediente 10 ("El Arrepentido") → cierre que volta à estampa (Riina preso em 1993) +
aforismo + 1 frase neutra de presente (Messina Denaro, 2023) + pergunta. Recorte 1860–1993, factual, atribuído, sem glamourizar:
vítimas e Estado (Petrosino, Ciaculli, Dalla Chiesa, Falcone, Borsellino e as escoltas).
Ângulo América Latina: La Habana (1946–1959, liga com o 001 CIA), Buscetta preso em São Paulo (1983). Apalachin liga com o 003 FBI.
Fatos conferidos em 05/11/2026 (ver SOURCES.md).

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (id I### na ordem de aparição) · "chave" reuso · "chave#enq" reuso com enquadramento
  + "@@TEXTO"      rótulo na tela (máquina de escrever; CAIXA ALTA, até ~28 caracteres)
Bloco: b(texto, *planos, card="PALERMO, 1945", ideia=True) · capítulo: cap("5. El Puerto")
Mapas (chave map_*): base sem texto nem pinos; pinos, setas e nomes no código (src/labels.jsx).
"""
import json, math, re
from pathlib import Path

WPS = 2.38           # palavras/s medidas no 001/002/003 (erro de 1–3%)
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
TITULO = "TODA la historia de la Cosa Nostra"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# Personagens (descrição visual fixa; rostos "resembling", nunca foto)
BUSCETTA_J = "a thin Sicilian youth of seventeen with dark wavy hair, dark serious eyes and a white shirt with rolled sleeves, 1945"
BUSCETTA = "a tanned Sicilian man in his mid fifties with dark hair combed back, a thin dark mustache and a tired hard face, open-collar shirt and light jacket, 1984"
PETROSINO = "a stocky Italian-American police detective in his late forties with a round face, a thick dark mustache, a bowler hat and a dark 1909 overcoat"
MORI = "a tall stern Italian prefect in his fifties with a shaved head, a thick grey mustache and a dark 1926 civilian overcoat, no insignia"
MASSERIA = "a short heavy Italian-American gangster boss in his forties with a round fleshy face, dark hair, expensive 1931 suit"
LUCIANO = "an Italian-American man in his thirties resembling Lucky Luciano, dark slicked-back hair, a slightly drooping right eyelid, a scar on his chin, elegant 1930s suit"
LUCIANO_V = "an Italian-American man in his late forties resembling Lucky Luciano, dark hair greying at the temples, a slightly drooping right eyelid, light 1946 suit"
LANSKY = "a small slim Jewish-American man in his forties with short dark hair, a long nose and a calm watchful face, linen 1950s suit"
FALCONE = "an Italian magistrate in his mid forties resembling Giovanni Falcone, dark hair, a thick dark mustache and a short dark beard, white shirt and dark tie"
BORSELLINO = "an Italian magistrate in his early fifties resembling Paolo Borsellino, receding grey hair, a grey mustache, a dark suit, a cigarette in his hand"
DALLA_CHIESA = "an Italian general in his early sixties with short grey hair and a grey mustache, a dark civilian suit, 1982"
RIINA = "a short stocky Sicilian man in his early sixties with a round heavy face, a thick neck, grey hair and a plain jacket, 1993"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, borders and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame"

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Palermo, mil novecientos cuarenta y cinco. Un muchacho de diecisiete años sostiene en las manos la estampa de un santo.",
  "palermo_45|Palermo in 1945 at dusk, narrow old street with baroque church domes, war-damaged buildings, a few people in dark clothes",
  "dark_room|A dim room lit by a single oil lamp in 1945 Sicily, several older men in dark suits standing around a wooden table, faces in shadow",
  f"youth_card|{BUSCETTA_J} holding a small printed holy card of a saint in both hands, older men around him in shadow, lamp light",
  "holy_card|Extreme close-up of a small old printed holy card of a Catholic saint held between two young hands, warm lamp light, no text", card="PALERMO, 1945")
b("Le pinchan un dedo. Su sangre cae sobre la imagen. Y la queman entre sus manos.",
  "finger_prick|Close-up of a young man's fingertip being pricked with a thorn, a single small drop of dark red falling onto a holy card, lamp light",
  "card_burning|Close-up of a small holy card of a saint burning in the cupped palms of two young hands, orange flame, dark background",
  "men_watching|Three older Sicilian men in dark 1940s suits watching in silence in a dark room, flame light on their faces")
b("Jura: si traiciono, que mi carne arda como arde este santo.",
  f"oath_face|{BUSCETTA_J} with a solemn face lit from below by a small flame burning in his hands@@\"QUE MI CARNE ARDA\"",
  "ashes|Black ashes of a burnt holy card falling from open hands onto a wooden table, a thin line of smoke")
b("Se llama Tommaso Buscetta. Cuarenta años después, se lo contará todo a un juez.",
  f"buscetta_court|{BUSCETTA} sitting alone at a witness table with a microphone in a large grey courtroom, 1986@@TOMMASO BUSCETTA",
  "judge_shadow|The silhouette of an Italian judge with a mustache and beard at a desk piled with files, a desk lamp, seen from behind")
b("Esta es TODA la historia de la Cosa Nostra. Y del juramento que la protegió durante un siglo.",
  "files_desk|A long dark desk covered with open brown case files and black and white photographs, a red stamp and a magnifying glass",
  "red_stamp|A hand slamming a red rubber stamp onto a brown paper case file, ink splash, dramatic close-up",
  "sicily_coast|The rocky coast of Sicily at dusk seen from the sea, a small fishing town with a church, dark mountains behind", ideia=True)

# ───────────────────────── 1. EL NOMBRE ─────────────────────────
cap("1. El Nombre")
b("El Nombre. Sicilia, mil ochocientos sesenta. Garibaldi desembarca con mil voluntarios. Al año siguiente, la isla ya forma parte del nuevo Reino de Italia.",
  "garibaldi|Garibaldi's red-shirted volunteers landing from two old steamships on a Sicilian beach in 1860, seen from far away, smoke on the horizon@@1860: LOS MIL",
  "bourbon_soldiers|Bourbon soldiers in white uniforms retreating through a Palermo street in 1860, barricades, smoke in the distance, seen from far away",
  "palermo_1860|Palermo in 1860, a crowded square with baroque buildings, people waving tricolor flags without emblems",
  "map_sicily|" + "The triangular island of Sicily alone in the center of a plain blue sea, the whole island fully visible, no other islands, no other land, only plain green and brown terrain without red marks, " + MAPA, card="SICILIA, 1860")
b("El nuevo Estado está lejos. En el campo casi no hay jueces ni policías. Y alrededor de Palermo crecen huertos de limones que valen una fortuna.",
  "country_road|A lonely dusty country road in 1860s Sicily, dry hills, a single rider on a mule, no town in sight",
  "conca_doro|The plain of the Conca d'Oro around Palermo in the 1870s seen from a hill, endless citrus groves, the city and the sea beyond",
  "lemon_grove|Lush lemon groves at the foot of the mountains around Palermo in the 1870s, stone walls and irrigation channels, golden light",
  "lemon_crates|Wooden crates full of lemons being loaded onto a sailing ship in the port of Palermo in the 1870s, dockworkers")
b("Los dueños contratan guardianes armados. Pronto, esos guardianes cobran a todos: al que protegen y al que amenazan.",
  "guardian|A Sicilian rural guard in a flat cap and a dark cloak walking along a stone wall of a lemon grove at night, a rifle slung on his back pointing down",
  "two_farmers|A Sicilian guard in a flat cap receiving money from a nervous farmer in front of a farmhouse, 1870s",
  "burned_trees|Burnt lemon trees in a grove at dawn, smoke rising, a farmer staring at the damage, 1870s")
b("En mil ochocientos sesenta y tres, una obra de teatro de Palermo lleva una palabra en el título: mafiusi. Dos años después, un informe del gobierno usa por primera vez la palabra mafia.",
  "playbill|An old 1863 theater playbill pasted on a stone wall in Palermo, decorative borders, the text made of unreadable shapes",
  "theater_1863|A small 19th century theater in Palermo, actors on stage dressed as prisoners in a jail, an audience in the dark",
  "report_1865|An old handwritten 19th century government report on a desk with a quill pen and a wax seal, no legible text@@1865: \"MAFFIA\"",
  "prefect_desk|A 19th century Italian official with side whiskers writing a letter at a desk by candlelight")
b("A finales de siglo, el jefe de la policía de Palermo, Ermanno Sangiorgi, describe en un informe ocho clanes en Palermo, con jefes, reglas y rituales de iniciación. Casi nadie le hace caso.",
  "ritual_sketch|A 19th century police notebook open on a desk, a pencil sketch of men around a table with a candle, the handwriting made of unreadable shapes",
  "sangiorgi|An Italian police chief in his sixties with white side whiskers and a dark uniform-like coat, reading a thick report at his desk, 1898@@ERMANNO SANGIORGI",
  "eight_files|Eight thin brown files laid out in a row on a desk, each with a small hand-drawn sketch of a face clipped on, lamp light@@8 CLANES",
  "dusty_shelf|A thick report gathering dust on a high shelf in an old ministry archive, cobwebs")
b("Mientras tanto, cientos de miles de sicilianos emigran a Estados Unidos. Algunos llevan consigo el negocio.",
  "emigrant_ship|A crowded emigrant steamship leaving the port of Palermo around 1905, families with bundles at the rails",
  "ellis_island|Immigrants with bundles and suitcases arriving at Ellis Island in New York around 1905, the hall full of people", ideia=True)

# ───────────────────────── 2. EL DETECTIVE ─────────────────────────
cap("2. El Detective")
b("El Detective. Nueva York, principios del siglo veinte. En los barrios italianos, los comerciantes reciben cartas: o pagas, o te matamos. Muchas las firma la Mano Negra.",
  "tenement_night|A narrow Little Italy tenement staircase at night in 1908, a shopkeeper slipping a letter under a door, gas light",
  "little_italy|Mulberry Street in New York's Little Italy around 1905, pushcarts, laundry lines and crowded tenements",
  "black_hand_letter|An extortion letter on a shop counter with a crude black hand print drawn on it and a small dagger sketch, no legible text@@LA MANO NEGRA",
  "shopkeeper|An Italian immigrant baker in an apron reading a letter in his shop in 1908 New York, frightened", card="NUEVA YORK, 1908")
b("El policía que las persigue es Joe Petrosino, un inmigrante italiano que llegó de niño. Dirige una unidad especial de agentes que hablan italiano.",
  f"petrosino|{PETROSINO} standing on a Little Italy street corner, watching the crowd@@JOE PETROSINO",
  f"petrosino_disguise|{PETROSINO} disguised as a street laborer with a cap, pretending to read a newspaper on a crowded New York sidewalk, 1907",
  "italian_squad|Five Italian-American plainclothes detectives in bowler hats and overcoats in a 1908 New York police station, a chalkboard")
b("En mil novecientos nueve viaja en secreto a Palermo. Quiere los antecedentes penales de mafiosos que viven en Nueva York, para deportarlos. Pero un periódico de Nueva York publica su viaje.",
  "palermo_port_09|The port of Palermo in February 1909, a steamship docked, porters and carriages, Monte Pellegrino behind",
  f"petrosino_ship|{PETROSINO} standing alone at the rail of a transatlantic steamship at night, 1909",
  "archive_palermo|An old courthouse archive in Palermo in 1909, a man in a bowler hat leafing through criminal records by window light",
  "newspaper_leak|A 1909 New York newspaper on a café table with headlines made of unreadable shapes and a small portrait of a mustached detective")
b("Doce de marzo de mil novecientos nueve. Plaza Marina, Palermo. De noche, Petrosino espera junto a un jardín. Lo matan a tiros.",
  "piazza_marina|Piazza Marina in Palermo at night in 1909, the iron railings of a garden with huge fig trees, gas lamps, rain@@12 DE MARZO DE 1909",
  "fallen_hat|A bowler hat lying on wet cobblestones under a gas lamp at night, people running in the distance, no body",
  "piazza_police|Policemen with lanterns gathering at the iron railings of a dark garden square at night, seen from far away, no body")
b("El principal sospechoso, el jefe mafioso Vito Cascio Ferro, nunca es condenado por el crimen. En Nueva York, una multitud enorme acompaña el funeral.",
  "acquittal|A 1909 Palermo courtroom, a judge signing a document, a bearded man in an elegant suit smiling slightly in the dock",
  "cascio_ferro|A tall Sicilian man in his late forties with a long dark beard and an elegant 1909 suit, a cold look, in a Palermo café@@VITO CASCIO FERRO",
  "funeral_ny|A huge funeral procession on a New York street in April 1909, a horse-drawn hearse, crowds lining the sidewalks, seen from far away")
b("En Sicilia, la mafia parece intocable. Hasta que llega un hombre enviado por Mussolini.",
  "shepherd_watch|A Sicilian shepherd on a rocky hillside watching a road below in the 1920s, a dog, wind, dusk",
  "sicily_village|A Sicilian hill town of stone houses at dawn in the 1920s, a church bell tower, mule paths", ideia=True)

# ───────────────────────── 3. EL PREFECTO ─────────────────────────
cap("3. El Prefecto")
b("El Prefecto. Mil novecientos veinticinco. Mussolini no tolera otro poder en Italia. Nombra prefecto de Palermo a Cesare Mori, un policía conocido por su mano dura.",
  "mussolini_desk|A huge empty marble office in Rome in 1925 with a single desk at the far end, a man in a dark suit seated, seen from the doorway, no flags",
  "rome_1925|A grand government palace balcony in Rome in 1925, a crowd in the square below, seen from far away, no flags with emblems",
  f"mori|{MORI} standing in a Palermo government office with his arms crossed@@CESARE MORI",
  "palermo_1925|The port of Palermo in 1925, steamships, carts and Monte Pellegrino behind", card="PALERMO, 1925")
b("En enero de mil novecientos veintiséis, rodea el pueblo de Gangi con cientos de policías y soldados. Corta las comunicaciones. Toma como rehenes a mujeres e hijos de los buscados.",
  "night_siege|Soldiers and carabinieri with lanterns climbing the stone alleys of a Sicilian hill town at night in winter 1926, seen from below",
  "gangi|The hill town of Gangi in Sicily in winter 1926, stone houses piled on a hilltop, soldiers and policemen surrounding it on the slopes, seen from far away@@GANGI, ENERO DE 1926",
  "water_cut|A dry stone fountain in a Sicilian village square in winter, women with empty jugs, soldiers in the background",
  "hostages|Sicilian women in black shawls and old men waiting under guard in a village square, soldiers with rifles slung, 1926")
b("Uno a uno, los hombres se entregan. En pocos años, miles de personas son detenidas. Según los historiadores, muchas sin pruebas, y algunas bajo tortura.",
  "surrender|Bearded Sicilian men walking down from a hill town with their hands raised, toward policemen, seen from far away, 1926",
  "mass_trial|A huge 1928 Italian courtroom with dozens of defendants in a long iron cage, carabinieri guards",
  "prison_corridor|A long dark prison corridor in Sicily in the 1920s, barred doors, a guard with keys")
b("En mil novecientos veintinueve, Mussolini retira a Mori. La propaganda fascista declara derrotada a la mafia. No lo está.",
  f"mori_leaves|{MORI} leaving an office with a leather briefcase, alone on a staircase, 1929",
  "newspaper_29|A 1929 Italian newspaper on a table with a huge triumphant headline made of unreadable shapes")
b("Muchos jefes esperan su momento en la cárcel o en el exilio. Y al otro lado del océano, una ley había convertido el alcohol en oro.",
  "prisoner_window|An old Sicilian prisoner with a grey mustache watching the sky through the bars of a cell window, patient",
  "whisky_gold|Bottles of whisky glowing like gold in the light of a lamp in a hidden 1920s cellar, wooden crates", ideia=True)

# ───────────────────────── 4. EL RESTAURANTE ─────────────────────────
cap("4. El Restaurante")
b("El Restaurante. Estados Unidos, mil novecientos veinte. Entra en vigor la Ley Seca: se prohíbe fabricar y vender alcohol. Las bandas lo contrabandean y se hacen ricas.",
  "barrels_poured|Federal agents in 1920 pouring barrels of beer into a city gutter, a crowd watching@@LEY SECA, 1920",
  "speakeasy|A crowded 1920s New York speakeasy behind a hidden door, jazz musicians, smoke, dim golden light",
  "smuggle_truck|A 1920s truck loaded with wooden crates driving at night under a bridge in New York, men in caps watching", card="ESTADOS UNIDOS, 1920")
b("En Nueva York, dos jefes sicilianos se disputan el poder: Joe Masseria y Salvatore Maranzano. La llaman la guerra de Castellammare.",
  f"masseria|{MASSERIA} sitting at the head of a restaurant table, napkin tucked in his collar@@JOE MASSERIA",
  "maranzano|A tall elegant Sicilian boss in his forties with a stern face and round glasses, in a 1930 office with books@@SALVATORE MARANZANO",
  "ny_1930|A New York street in 1930 at night, elevated train tracks, old cars, wet asphalt")
b("Quince de abril de mil novecientos treinta y uno. Masseria come en un restaurante de Coney Island con su lugarteniente, Charles Luciano. Según la versión más conocida, Luciano se levanta para ir al baño. Entran varios hombres armados. Masseria muere a tiros.",
  "coney_restaurant|A 1931 Italian restaurant in Coney Island with checkered tablecloths, two men playing cards at a corner table@@15 DE ABRIL DE 1931",
  f"luciano|{LUCIANO} getting up from a restaurant table, buttoning his jacket, not looking back@@CHARLES \"LUCKY\" LUCIANO",
  "restaurant_door|The front door of a 1931 restaurant swinging open, the shadows of several men in hats on the floor",
  "empty_table|An empty restaurant table with an overturned chair and scattered playing cards, seen from far away, no body, no blood")
b("Cinco meses después, Maranzano es asesinado en su oficina por hombres disfrazados de agentes del gobierno.",
  "fake_agents|Four men in long coats and fedoras walking quickly through a 1931 Manhattan office lobby, showing badges",
  "park_avenue|A tall 1931 office building on Park Avenue in New York at dusk, seen from the street")
b("Luciano no se proclama jefe de jefes. Crea un consejo, la Comisión, donde las cinco familias de Nueva York y los grupos de otras ciudades resuelven sus conflictos.",
  "commission_table|Seven men in 1930s suits around a long table in a dark private room, smoke, faces half in shadow@@LA COMISIÓN",
  "five_chairs|Five empty leather chairs around a dark wooden table in a private room, an ashtray and a lamp")
b("En mil novecientos treinta y seis, el fiscal Thomas Dewey logra que lo condenen a entre treinta y cincuenta años de cárcel. Pero la guerra le dará una salida.",
  "dewey|A young American prosecutor in his thirties with a dark mustache and slicked hair, addressing a jury in 1936@@THOMAS DEWEY",
  "prison_luciano|A grim stone prison in upstate New York in winter, high walls and a watchtower", ideia=True)

# ───────────────────────── 5. EL PUERTO ─────────────────────────
cap("5. El Puerto")
b("El Puerto. Nueva York, febrero de mil novecientos cuarenta y dos. El transatlántico Normandie se incendia en el muelle. La Marina teme sabotajes nazis en el puerto.",
  "normandie|A huge ocean liner burning and listing at a New York pier in February 1942, black smoke, fireboats spraying water, seen from far away@@EL NORMANDIE, 1942",
  "navy_officers|Two US Navy intelligence officers in 1942 uniforms studying a map of the New York harbor on a table",
  "docks_42|New York docks in 1942, longshoremen unloading cargo from ships, cranes, winter fog", card="NUEVA YORK, 1942")
b("Los muelles los controla la mafia. Así que la inteligencia naval busca un acuerdo con el preso más famoso del país: Lucky Luciano.",
  "longshoremen|Longshoremen in caps on a New York pier in 1942, a man in a good coat watching them from a doorway",
  f"luciano_prison|{LUCIANO} in a grey prison shirt sitting at a table in a visiting room, two men in suits across from him, 1942")
b("Desde la cárcel, hace correr la voz: los estibadores deben vigilar el puerto. La operación se llama Inframundo.",
  "whisper_docks|Two dockworkers whispering on a foggy pier at night, a ship's hull behind them",
  "secret_file_42|A brown US Navy file stamped in red on a desk, a fountain pen, no legible text@@OPERACIÓN INFRAMUNDO")
b("Julio de mil novecientos cuarenta y tres. Los aliados desembarcan en Sicilia. Los historiadores todavía discuten si la mafia ayudó a la invasión.",
  "husky|Allied landing craft and soldiers coming ashore on a Sicilian beach in July 1943, ships on the horizon, seen from far away@@JULIO DE 1943",
  "jeep_village|American soldiers in a jeep driving into a Sicilian village in 1943, villagers watching from doorways")
b("Lo que sí está documentado: el gobierno militar aliado nombra alcaldes a varios mafiosos. Calogero Vizzini, jefe de Villalba, se convierte en alcalde de su pueblo.",
  "amgot_office|An American army officer at a desk in a requisitioned Sicilian town hall in 1943, a line of local men waiting",
  "vizzini|A heavy elderly Sicilian man in his sixties with a big belly, suspenders, thick glasses and a cap, standing on a village street@@CALOGERO VIZZINI",
  "villalba|A small dusty Sicilian village of stone houses on a hill in 1943, a church and a square")
b("En mil novecientos cuarenta y seis, Luciano queda libre, con la condición de ser deportado a Italia. No se queda allí mucho tiempo.",
  f"luciano_ship|{LUCIANO_V} on the deck of a cargo ship leaving New York harbor in February 1946, the skyline behind him",
  "naples_46|The port of Naples in 1946, war-damaged buildings and ships, Mount Vesuvius in the haze", ideia=True)

# ───────────────────────── 6. EL HOTEL ─────────────────────────
cap("6. El Hotel")
b("El Hotel. La Habana, diciembre de mil novecientos cuarenta y seis. Luciano llega a Cuba en secreto.",
  "havana_46|Havana's Malecón seawall in 1946 at sunset, 1940s cars, waves splashing, the city behind",
  f"luciano_havana|{LUCIANO_V} in a white linen suit on a hotel terrace in Havana with palm trees, looking at the sea", card="LA HABANA, 1946")
b("En el Hotel Nacional reúne a jefes de la mafia estadounidense. Su plan, según los investigadores: dirigir los negocios desde la isla, a ciento cincuenta kilómetros de Florida.",
  "hotel_nacional|The Hotel Nacional in Havana in 1946, a grand 1930s building with twin towers above the sea, palm trees, old cars@@HOTEL NACIONAL",
  "havana_meeting|Men in white and grey 1940s suits around a long table in a hotel suite with tall windows over the sea, cigars, ceiling fans",
  "map_atlantic|" + "The North Atlantic ocean from above: the east coast of North America with Florida and Cuba at the left, Europe and the Mediterranean with Italy and Sicily at the right, " + MAPA)
b("Washington lo descubre. El jefe antidrogas, Harry Anslinger, presiona: Estados Unidos dejará de enviar medicamentos con narcóticos a Cuba mientras Luciano siga allí. En febrero de mil novecientos cuarenta y siete, lo arrestan. Cuba lo expulsa.",
  "anslinger|A heavy-set bald American official in his fifties in a dark suit, speaking on a telephone in a Washington office, 1947@@HARRY ANSLINGER",
  "medicine_crates|Wooden crates of medicine with red crosses stacked on a dock in Havana, a customs officer stopping them",
  "deported|Two Cuban policemen escorting a man in a linen suit up the gangway of a ship in Havana harbor, 1947")
b("Pero su socio, Meyer Lansky, se queda. Con el dictador Fulgencio Batista, La Habana se llena de casinos y hoteles de lujo.",
  f"lansky|{LANSKY} standing in a luxurious 1950s casino in Havana, watching the roulette tables@@MEYER LANSKY",
  "batista|A 1950s Cuban general in his fifties with dark wavy hair and a broad face, in a white uniform without insignia, smiling at a reception",
  "casino_havana|A glittering 1950s Havana casino at night, roulette and card tables, elegant gamblers, chandeliers")
b("El uno de enero de mil novecientos cincuenta y nueve triunfa la revolución. Poco después, Fidel Castro cierra los casinos. La mafia pierde la isla.",
  "revolution|Bearded Cuban rebels in olive uniforms riding on a truck through a Havana street in January 1959, cheering crowds@@1 DE ENERO DE 1959",
  "casino_closed|An empty 1959 Havana casino with overturned chairs and tables covered with sheets, sunlight through tall windows")
b("Y según una comisión del Senado de Estados Unidos, en mil novecientos sesenta la CIA pide ayuda a jefes de la mafia para envenenar a Castro. El plan fracasa.",
  "poison_pills|A small glass vial of white pills on a dark table next to a cigar box, lamp light, ominous",
  "cia_mob|Two American men in 1960 suits meeting secretly in a Miami hotel room with closed blinds, one handing an envelope to the other", ideia=True)

b("Si te gustan estos expedientes, suscríbete. Y ahora, las dos reuniones de mil novecientos cincuenta y siete.",
  "folder_stack|A tall stack of brown case files with red stamps on a desk, the top one slightly open, mysterious light inside")

# ───────────────────────── 7. LAS REUNIONES ─────────────────────────
cap("7. Las Reuniones")
b("Las Reuniones. Palermo, octubre de mil novecientos cincuenta y siete. En el Grand Hotel et des Palmes se reúnen durante varios días jefes sicilianos y estadounidenses. Entre ellos, Joseph Bonanno, jefe de una de las cinco familias de Nueva York.",
  "des_palmes|The facade of an elegant 19th century grand hotel on a Palermo avenue with palm trees in 1957, black cars at the entrance, blank signs",
  "hotel_lunch|Sicilian and American men in 1950s suits at a long lunch table in an ornate hotel dining room with mirrors, waiters",
  "bonanno|An Italian-American boss in his early fifties with neat greying hair and a cultured calm face, elegant 1957 suit, in a hotel lobby@@JOSEPH BONANNO", card="PALERMO, 1957")
b("Según investigadores italianos, hablan de heroína. Y los estadounidenses aconsejan a los sicilianos crear su propia Comisión.",
  "heroin_packets|Small packets of white powder wrapped in paper inside an open wooden crate of oranges, close-up, dark",
  "sicily_commission|Older Sicilian men in dark suits around a table in a country farmhouse, a lamp, faces in shadow")
b("Un mes después, la policía irrumpe en otra reunión: Apalachin, Nueva York. Más de cincuenta jefes son detenidos. El FBI, que negaba que existiera la mafia, ya no puede negarlo.",
  "apalachin|A large country stone house on a wooded hill in upstate New York in November 1957, many shiny black luxury cars parked outside@@APALACHIN, 14/11/1957",
  "woods_run|Men in expensive suits and fedoras running through bare autumn woods, seen from far away",
  "mob_lineup|A row of men in expensive 1957 suits standing in a small police station, sullen faces, a policeman taking notes")
b("En Sicilia, en cambio, la nueva Comisión trabaja en silencio. Y Palermo está a punto de cambiar de cara.",
  "palermo_old|Palermo in the late 1950s, elegant Art Nouveau villas with gardens along a wide avenue, palm trees", ideia=True)

# ───────────────────────── 8. EL CEMENTO ─────────────────────────
cap("8. El Cemento")
b("El Cemento. Palermo, finales de los años cincuenta. La ciudad crece sin control. Se derriban villas históricas, a veces de noche, y en su lugar se levantan bloques de cemento.",
  "villa_demolish|An elegant Art Nouveau villa being demolished at night by workers with lamps, dust, Palermo late 1950s",
  "concrete_blocks|Rows of new grey concrete apartment blocks replacing orange groves at the edge of Palermo in the 1960s, cranes",
  "cranes|Construction cranes over half-built concrete towers in Palermo at dusk in the early 1960s", card="PALERMO, 1959")
b("Según la comisión antimafia del Parlamento, la mayoría de los permisos de construcción de esos años quedan en manos de unos pocos nombres, simples prestanombres.",
  "permits|A stack of stamped building permits on a city hall desk, a hand signing one after another, no legible text",
  "front_men|Five ordinary-looking men in cheap 1960s suits waiting on a bench in a city hall corridor, holding folders")
b("En el ayuntamiento gobiernan el alcalde Salvo Lima y Vito Ciancimino, a cargo de las obras públicas. Ciancimino será condenado décadas después por asociación mafiosa. La prensa lo llamará el saqueo de Palermo.",
  "city_hall|A Palermo city hall office in 1960, two politicians in dark suits looking at a large city plan on a table",
  "ciancimino|A Sicilian politician in his late thirties with dark wavy hair and thick black-framed glasses, smiling, 1960@@VITO CIANCIMINO",
  "headline_sack|A folded 1960s newspaper on a café table showing only a large photograph of grey concrete buildings, no headline, no text")
b("Treinta de junio de mil novecientos sesenta y tres. Ciaculli, en las afueras de Palermo. Un auto abandonado explota cuando lo revisan. Mueren siete hombres: carabineros y artificieros del ejército.",
  "ciaculli|An abandoned small 1960s car parked on a dirt road among citrus groves on the outskirts of Palermo, a hot summer day@@CIACULLI, 30/06/1963",
  "ciaculli_smoke|A column of black smoke rising from a citrus grove outside Palermo in 1963, seen from very far away, no bodies",
  "carabinieri_caps|Seven military caps of Italian carabinieri and soldiers lined up on a flag-draped table at a funeral, candles")
b("El Estado reacciona: cientos de detenidos. La Comisión de la mafia se disuelve. Por unos años.",
  "raid_63|Italian police and carabinieri in 1963 leading handcuffed men out of a farmhouse at dawn, seen from far away",
  "empty_farmhouse|An empty Sicilian farmhouse room with a table and chairs covered in dust, a lamp turned off", ideia=True)

# ───────────────────────── 9. LA GUERRA ─────────────────────────
cap("9. La Guerra")
b("La Guerra. En los años setenta, la heroína refinada en Sicilia llega a Estados Unidos. El dinero es enorme. Y un clan del interior lo quiere todo: los corleoneses de Salvatore Riina.",
  "lab_heroin|A hidden clandestine laboratory in a Sicilian farmhouse in the 1970s, glass flasks and steam, men in masks, dim light",
  "corleone|The town of Corleone in Sicily, stone houses below a huge rocky cliff, dry hills, 1970s",
  f"riina_70s|{RIINA.replace('early sixties', 'mid forties').replace('grey hair', 'dark hair').replace('1993', '1978')} sitting in a farmhouse kitchen, a cold stare@@SALVATORE RIINA", card="PALERMO, 1981")
b("Veintitrés de abril de mil novecientos ochenta y uno. Matan a Stefano Bontade, uno de los jefes más poderosos de Palermo. Menos de tres semanas después, a su aliado Salvatore Inzerillo.",
  "bontade_car|An expensive 1981 car stopped at a traffic light on a Palermo street at night, its window shattered, seen from far away, no body@@23 DE ABRIL DE 1981",
  "bontade|An elegant Sicilian boss in his early forties with dark hair and a refined face, in a 1980 suit at a party@@STEFANO BONTADE",
  "funeral_81|Mourners in black walking behind a coffin up a Palermo church staircase in 1981, police watching")
b("Empieza una masacre. En dos años, según los investigadores, cientos de mafiosos, familiares y testigos son asesinados o desaparecen.",
  "white_sheets|A long row of black-bordered funeral notices on a Palermo wall in 1982, blank paper without legible text",
  "missing_photos|A table covered with small black and white photographs of missing men, a police inspector looking at them",
  "palermo_82|A Palermo street at night in 1982, police cars with blue lights, onlookers behind a barrier, seen from far away")
b("El Estado envía a Palermo al general Carlo Alberto Dalla Chiesa, que había combatido el terrorismo. El tres de septiembre de mil novecientos ochenta y dos, lo matan en su auto junto a su esposa y su escolta. Llevaba cien días en el cargo.",
  f"dalla_chiesa|{DALLA_CHIESA} standing in an office in Palermo, a map of the city on the wall behind him@@CARLO ALBERTO DALLA CHIESA",
  "a112|A small white 1980s car stopped in a Palermo street at night, doors open, police lights around it, seen from far away, no bodies@@3 DE SEPTIEMBRE DE 1982",
  "sign_honest|A hand-written cardboard sign tied to a lamp post on a Palermo street at night, unreadable writing, candles below")
b("Diez días después, el Parlamento convierte en delito pertenecer a la mafia. Y uno de los perdedores de la guerra está escondido en Brasil.",
  "parliament_82|The Italian Chamber of Deputies in Rome in 1982, deputies voting in a semicircular hall, seen from above",
  "sao_paulo_83|São Paulo in 1983 at dusk, dense skyscrapers and avenues, seen from a high window", ideia=True)

# ───────────────────────── 10. EL ARREPENTIDO ─────────────────────────
cap("10. El Arrepentido")
b("El Arrepentido. São Paulo, octubre de mil novecientos ochenta y tres. La policía brasileña detiene a un siciliano que vive con documentos falsos. Es Tommaso Buscetta, mafioso y traficante de heroína.",
  "arrest_brazil|Brazilian federal police officers in 1983 leading a tanned man in a light jacket out of an apartment building in São Paulo, seen from far away",
  f"buscetta|{BUSCETTA} sitting in a bare Brazilian police office, handcuffed, looking at the floor@@TOMMASO BUSCETTA",
  "fake_passport|A fake passport and identity papers spread on a police desk under a lamp, no legible text", card="SÃO PAULO, 1983")
b("Durante la guerra, los corleoneses mataron a su hermano, a su yerno y a dos de sus hijos, entre otros familiares.",
  "family_photos|A row of small framed family photographs of young and old Sicilian men on a dark dresser, a black ribbon, a candle",
  f"buscetta_grief|{BUSCETTA} alone at a barred window, his face in shadow, grief")
b("En mil novecientos ochenta y cuatro, antes de ser extraditado a Italia, intenta suicidarse con veneno. Sobrevive.",
  "extradition_plane|A plane on a runway at night in Brazil in 1984, police cars beside it, a man escorted up the stairs, seen from far away",
  "hospital_84|A hospital bed with a man under a sheet and a police guard at the door, 1984, cold light")
b("En Roma lo espera un juez de Palermo: Giovanni Falcone.",
  f"falcone|{FALCONE} sitting across a table in a bare Rome interrogation room, a notebook in front of him@@GIOVANNI FALCONE")
b("Buscetta rompe su juramento. Según su propio relato, explica las familias, los jefes, la Comisión, los rituales. Y el nombre que usan los propios mafiosos: Cosa Nostra. Nuestra cosa.",
  "card_burning#detalhe-centro",
  "organigram|A large hand-drawn organization chart of a criminal structure pinned on a wall, names replaced by small sketched faces, red strings@@\"COSA NOSTRA\"",
  f"falcone_notes|{FALCONE} writing quickly on a yellow legal pad, piles of typed pages beside him, cigarette smoke")
b("Falcone llena miles de páginas. Con ellas prepara un juicio que nadie creía posible.",
  "pages_stack|Huge stacks of typed pages and binders filling a small magistrate's office in Palermo, a lamp, late night", ideia=True)

# ───────────────────────── 11. LA PIZZERÍA ─────────────────────────
cap("11. La Pizzería")
b("La Pizzería. Abril de mil novecientos ochenta y cuatro. En Estados Unidos, el FBI detiene a decenas de personas en varios estados. Según la fiscalía, usaban pizzerías para distribuir heroína traída de Sicilia.",
  "pizzeria|A small American pizzeria at night in 1984, neon in the window without legible letters, a man carrying boxes to the back",
  "fbi_raid_84|FBI agents in plain dark jackets leading a man in an apron out of a small restaurant at dawn in 1984, blank shop sign, no lettering anywhere, seen from far away",
  "flour_bags|Flour sacks in the storage room of a pizzeria, one cut open revealing small packets wrapped in plastic, close-up", card="NUEVA YORK, 1984")
b("La llaman la Conexión de la Pizza. Uno de los fiscales es Louis Freeh, que años después dirigirá el FBI.",
  "freeh_84|A young American federal prosecutor in his thirties with short dark hair and glasses, standing in a courtroom, 1985@@LOUIS FREEH",
  "court_ny_85|A crowded 1985 New York federal courtroom, many defendants at long tables, lawyers and a judge")
b("El principal acusado es Gaetano Badalamenti, antiguo jefe de la Comisión siciliana, detenido en Madrid. Buscetta declara contra él.",
  "badalamenti|A Sicilian man in his early sixties with grey hair and a heavy tired face, in a dark suit in a courtroom@@GAETANO BADALAMENTI",
  "madrid_84|A street in central Madrid in 1984, old buildings with balconies, a police car, evening",
  f"buscetta_ny|{BUSCETTA} testifying in an American courtroom, behind a microphone, U.S. marshals beside him")
b("En mil novecientos ochenta y siete, Badalamenti es condenado a cuarenta y cinco años de prisión. Según la fiscalía, la red movió heroína por unos mil seiscientos millones de dólares.",
  "verdict_87|A judge reading a verdict in a 1987 New York courtroom, defendants standing@@45 AÑOS",
  "cash_heroin|Stacks of dollar bills next to small plastic packets of white powder on a dark table under a lamp@@1.600 MILLONES DE DÓLARES")
b("Mientras tanto, en Palermo, se termina un tribunal a prueba de bombas.",
  "bunker_ext|A massive windowless concrete courthouse building next to an old prison wall in Palermo, 1986, armored vehicles outside", ideia=True)

# ───────────────────────── 12. EL BÚNKER ─────────────────────────
cap("12. El Búnker")
b("El Búnker. Palermo, diez de febrero de mil novecientos ochenta y seis. Junto a la cárcel del Ucciardone se abre una sala blindada, construida para este juicio.",
  "aula_bunker|A huge octagonal green courtroom with rows of steel cages along the walls, hundreds of seats, a judges' bench, 1986@@MAXIPROCESO",
  "soldiers_court|Italian soldiers with rifles slung guarding the entrance of a concrete courthouse in Palermo in 1986, armored cars",
  "ucciardone|The old Ucciardone prison in Palermo, thick yellowish walls and a gate, 1986", card="PALERMO, 1986")
b("Hay cuatrocientos setenta y cinco acusados. Muchos siguen el juicio desde jaulas de acero. Algunos gritan. Otros fingen locura.",
  "cages|Men in shirts and jackets shouting and gripping the bars of steel cages in a courtroom, 1986@@475 ACUSADOS",
  "lawyers_86|Dozens of Italian lawyers in black robes crowding a courtroom, papers flying, 1986",
  "defendant_madness|A defendant in a courtroom cage climbing the bars and shouting, guards looking up, 1986")
b("Buscetta declara frente a sus antiguos compañeros.",
  f"buscetta_maxi|{BUSCETTA} speaking into a microphone at a witness table, the steel cages full of men behind him, 1986")
b("Dieciséis de diciembre de mil novecientos ochenta y siete. Después de casi dos años, la sentencia: más de trescientos condenados y diecinueve cadenas perpetuas.",
  "sentence_87|An Italian presiding judge reading a sentence from a thick document in a huge courtroom, everyone standing@@16 DE DICIEMBRE DE 1987",
  "sentence_pages|A thick bound court sentence of thousands of pages on a table, a red ribbon, a gavel@@19 CADENAS PERPETUAS")
b("Por primera vez, un tribunal acepta que la Cosa Nostra es una sola organización, con una cúpula. En enero de mil novecientos noventa y dos, la Corte de Casación confirma las condenas.",
  "cassazione|The Palace of Justice in Rome, a massive white 19th century building on the Tiber river, 1992@@CORTE DE CASACIÓN, 1992",
  "falcone_rome|" + f"{FALCONE.replace('mid forties', 'early fifties')} walking along a corridor in a Rome ministry, files under his arm, two bodyguards behind him")
b("Según los fiscales, Riina decide matar a los jueces.",
  "riina_shadow|" + f"{RIINA} in shadow at a dark farmhouse table, only half of his face lit, cold eyes", ideia=True)

# ───────────────────────── 13. LA AUTOPISTA ─────────────────────────
cap("13. La Autopista")
b("La Autopista. Veintitrés de mayo de mil novecientos noventa y dos. Falcone aterriza en Palermo con su esposa, la jueza Francesca Morvillo. Tres autos blindados los llevan hacia la ciudad.",
  "punta_raisi|A small Italian airport by the sea and mountains near Palermo in May 1992, a plane on the runway, late afternoon",
  "morvillo|An Italian magistrate woman in her mid forties with short blonde hair and a calm elegant face, 1992@@FRANCESCA MORVILLO",
  "convoy|Three armored sedans driving fast in a convoy on a coastal highway in Sicily in May 1992, the sea and mountains", card="CAPACI, 1992")
b("Bajo el asfalto, cerca de Capaci, hay unos quinientos kilos de explosivos. Desde una colina, un mafioso aprieta un botón.",
  "culvert|A drainage tunnel under a Sicilian highway, dark barrels inside, seen from the dry ditch, 1992",
  "hill_watcher|A man hidden among dry bushes on a hillside above a coastal highway, holding a small remote control, seen from behind",
  "capaci_blast|A huge cloud of dust and smoke rising from a highway near the sea in Sicily, seen from very far away, no bodies@@23 DE MAYO DE 1992")
b("Mueren Falcone, Morvillo y tres policías de su escolta: Antonio Montinaro, Rocco Dicillo y Vito Schifani.",
  "capaci_crater|A highway torn open by a massive crater, wrecked cars at a distance, rescue workers, seen from far away, no bodies",
  "five_candles|Five candles burning in front of five small framed photographs on a table, flowers@@MONTINARO · DICILLO · SCHIFANI")
b("Cincuenta y siete días después, el diecinueve de julio, un auto bomba explota en la vía D'Amelio, frente a la casa de la madre del juez Paolo Borsellino. Era amigo y compañero de Falcone. Mueren él y cinco agentes de su escolta.",
  f"borsellino|{BORSELLINO} standing on a balcony in Palermo, smoking, looking at the city@@PAOLO BORSELLINO",
  "via_damelio|A residential street in Palermo with apartment buildings in July 1992, smoke rising, burned cars, firemen, seen from far away, no bodies@@VÍA D'AMELIO, 19/07/1992",
  "escort_tribute|A row of police caps on a table with white flowers and candles, 1992")
b("Palermo cuelga sábanas blancas de los balcones. El Estado envía miles de soldados a Sicilia.",
  "white_sheets_balconies|White bedsheets hanging from the balconies of a whole Palermo apartment building in 1992, a quiet street",
  "soldiers_92|Italian army soldiers patrolling a Palermo street in 1992, armored vehicles, people walking past")
b("Y empieza a buscar en serio al hombre que llevaba veinticuatro años escondido.",
  "riina_shadow#médio-dir", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. La Estampa")
b("La Estampa. Palermo, quince de enero de mil novecientos noventa y tres. Los carabineros detienen a Salvatore Riina en un auto, en plena ciudad. Era prófugo desde mil novecientos sesenta y nueve.",
  "riina_arrest|Plainclothes carabinieri officers surrounding a small car at a Palermo roundabout on a winter morning in 1993, seen from far away@@15 DE ENERO DE 1993",
  f"riina_93|{RIINA} seen in medium shot from the waist up, sitting in a bare carabinieri office, expressionless face clearly visible, 1993@@SALVATORE RIINA", card="PALERMO, 1993")
b("Recibirá varias cadenas perpetuas y morirá preso en dos mil diecisiete. Buscetta había muerto en el año dos mil, en Estados Unidos, protegido por el gobierno.",
  "cell_93|A small bare prison cell with a narrow bed and a high window, cold light",
  "grave_usa|A quiet American cemetery at dusk with a simple grave without a legible name, a single flower")
b("Durante un siglo, la Cosa Nostra sobrevivió al Estado italiano, a Mussolini y al FBI. Lo que no resistió fue que uno de los suyos rompiera el juramento.",
  "holy_card#detalhe-centro", "ashes#médio-dir", "files_desk#detalhe-alto", ideia=True)
b("Hoy sigue existiendo, más débil y más silenciosa. Su último gran prófugo, Matteo Messina Denaro, fue detenido en dos mil veintitrés.",
  "palermo_today|Palermo today at dawn seen from Monte Pellegrino, the cathedral domes and the port, calm sea",
  "folder_close|A hand closing a thick brown case file with a red circular stamp on a dark desk, lamp light")
b("Y tú, ¿crees que una organización así puede desaparecer? Déjalo en los comentarios. Y si quieres ver cómo la CIA y el FBI se cruzaron con la mafia, sus expedientes completos están aquí.",
  "folder_stack#médio-esq", "casino_havana#aberto")

# a 1ª prova do 001 (04/11) saiu com moldura de papel: todo prompt leva sangria explícita
SANGRIA = ", full-bleed illustration filling the entire frame edge to edge, no border, no margin, no white frame, no panel outline"

# Thumbs (biblia/thumb.md): personagem à esquerda com objeto que conta o tema, metade direita livre. Sem arma (brief).
THUMBS = [
    {"id": "thumb-A", "prompt": "A Sicilian mafia boss in his fifties in half body on the LEFT third of the frame, dark 1950s double-breasted suit and fedora, holding a small burning holy card of a saint in his open palm, cold stare at the viewer, behind him a Sicilian hill town and baroque church at dusk; the RIGHT half of the image is plain empty dusk sky, no signage, no lettering"},
    {"id": "thumb-B", "prompt": f"{FALCONE} in half body on the LEFT third of the frame, holding a thick stack of court files tied with a red ribbon against his chest, determined stare at the viewer, behind him a steel cage courtroom; the RIGHT half of the image is plain dark empty wall in shadow, no signage, no lettering"},
    {"id": "thumb-C", "prompt": "A Sicilian man in his fifties in a dark 1950s suit in half body on the LEFT third of the frame, pressing his index finger on his lips in a gesture of silence, menacing stare at the viewer, behind him a narrow old Palermo street at night with a gas lamp; the RIGHT half of the image is plain dark empty night sky, no signage, no lettering"},
]

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
