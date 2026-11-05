#!/usr/bin/env python3
"""Fonte única do dossie-es 002 (Mossad): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (na pasta do vídeo). Conteúdo no topo; geração no fim (copiada do 001-cia).

Molde da bíblia (canais/dossie-es/biblia/roteiro.md): hook por anedota (o MiG iraquiano, 1966; o Atlas del Tiempo abre
com Eichmann, então Eichmann vira expediente, contado pelo homem cego que o encontrou) → 13 expedientes-objeto com título
falado → pagamento da anedota no expediente 7 (metade do vídeo) → cierre que volta ao MiG (museu de Hatzerim) + aforismo +
pergunta. Recorte 1949–1990, factual, atribuído; 1 frase neutra de contexto atual no cierre.
Fatos conferidos em 05/11/2026 (ver SOURCES.md, "Checagem de 05/11").

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (id I### na ordem de aparição) · "chave" reuso · "chave#enq" reuso com enquadramento
  + "@@TEXTO"      rótulo na tela (máquina de escrever; CAIXA ALTA, até ~28 caracteres)
Bloco: b(texto, *planos, card="BAGDAD, 1966", ideia=True) · capítulo: cap("5. La Casa")
Mapas (chave map_*): base sem texto nem pinos; pinos, setas e nomes no código (src/labels.jsx).
"""
import json, math, re
from pathlib import Path

WPS = 2.38           # palavras/s medidas no 001 (1.686 palavras em 706 s com pausas = 143 ppm)
BREAK, LONG = 0.35, 0.8
MAX_PLANO_INICIO = 3.0   # s por plano nos primeiros INICIO s (~20 cortes/min)
INICIO = 60.0
MAX_PLANO = 3.6      # s por plano depois (~17 cortes/min)
INEDITO_ATE = 180.0  # s: só imagens novas até aqui
JANELA = 60.0        # s: mesmo enquadramento da mesma imagem só depois disso
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "TODA la historia del Mossad"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# Personagens (descrição visual fixa; rostos "resembling", nunca foto)
REDFA = "a 1960s Iraqi Air Force pilot in his early thirties with short dark hair and a thick mustache, olive green flight suit"
BENGURION = "a 1950s Israeli prime minister resembling David Ben-Gurion, short stocky elderly man with a bald top and wild white hair on the sides, open-collar khaki shirt"
SHILOAH = "a 1949 Israeli diplomat in his forties with a dark mustache and round glasses, grey suit"
HAREL = "a short intense 1950s Israeli intelligence chief in his forties with receding dark hair and thick eyebrows, plain white open-collar shirt"
HERMANN = "a German man in his late fifties with very thick dark glasses, nearly blind, simple 1950s suit, holding a white cane"
SILVIA = "a young Argentine woman of about eighteen in a 1950s dress, dark hair"
BAUER = "a 1950s German prosecutor with wild grey hair and thick-rimmed glasses, dark suit, holding a cigarette"
EICHMANN = "a thin balding man of about fifty-four with glasses and a narrow face, worn 1960 civilian suit and tie"
AMIT = "a 1960s Israeli general in his early forties with short dark hair, khaki uniform without insignia"
CUKURS = "a strong-jawed man in his sixties with slicked-back grey hair, light 1960s suit"
COHEN = "a slim elegant man in his late thirties with dark hair and a thin mustache, tailored 1960s suit"
ZAMIR = "a 1970s Israeli intelligence chief in his late forties with thinning hair and a calm tired face, grey suit"
GOLDA = "an elderly Israeli prime minister resembling Golda Meir, grey hair pulled back in a bun, dark plain dress"
MARWAN = "a 1970s Egyptian man of about thirty with dark wavy hair, elegant tailored suit"
VANUNU = "a 1980s man in his early thirties with curly dark hair and a short beard, casual shirt"
OSTROVSKY = "a 1990 man in his early forties with short dark hair and a mustache, leather jacket"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, borders and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame"

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Irak, dieciséis de agosto de mil novecientos sesenta y seis. Un piloto de la fuerza aérea iraquí despega en un MiG veintiuno, el caza soviético más moderno de su tiempo.",
  "iraq_airbase|An Iraqi air base near Baghdad at dawn in 1966, a silver delta-wing Soviet jet fighter on the runway, palm trees and heat haze in the distance",
  f"redfa_cockpit|{REDFA} closing the canopy of a jet fighter cockpit, focused eyes, helmet on",
  "mig_takeoff|A silver delta-wing MiG-21 jet fighter taking off from a desert runway, afterburner glow, dust behind it",
  "pilot_map|A pilot's gloved hand holding a folded flight map on his knee inside a jet cockpit, desert below through the canopy",
  "mig_sky|A lone silver delta-wing jet fighter climbing over the brown Iraqi desert and the Euphrates river, seen from far away", card="IRAK, 16 DE AGOSTO DE 1966")
b("Es un vuelo de entrenamiento. Debería volver en minutos. En vez de eso, gira hacia el oeste.",
  "radar_room|Iraqi radar operators in a dim 1960s control room watching a green radar screen, one of them pointing, worried",
  "mig_turn|A delta-wing jet fighter banking sharply to the west over a desert, long shadow on the ground",
  "control_tower|A 1960s military control tower at an Iraqi base, an officer shouting into a radio microphone")
b("Vuela bajo, sobre Jordania. Y aterriza en Israel.",
  "mig_low|A silver jet fighter flying very low over rocky Jordanian desert hills, seen from far away",
  "mig_landed|A silver delta-wing MiG-21 parked on an Israeli airfield in 1966, ground crew in khaki running toward it, the pilot climbing down")
b("[serious] Ningún piloto occidental había volado uno. La fuga llevaba años en preparación. Y la había planeado el Mossad.",
  "mig_hangar|Engineers in white coats examining an open silver MiG jet fighter inside a dark hangar, inspection lamps",
  "israeli_jets|Two 1960s French-made delta-wing Mirage jet fighters escorting a silver MiG jet over green fields, seen from far away",
  "agents_tea|Two men in 1960s suits shaking hands in a dim hotel room, a photograph of a jet fighter on the table between them",
  "mossad_folder|A brown paper case file on a dark desk with a red circular stamp, a black and white photograph of a jet fighter clipped to it, lamp light")
b("Esta es toda la historia del Mossad. De una oficina sin nombre a uno de los servicios secretos más temidos del mundo.",
  "tel_aviv_night|Tel Aviv at night in the 1960s, white Bauhaus buildings, palm trees, a few lit windows, the sea behind",
  "map_middleeast|" + "the Middle East from above: the eastern Mediterranean coast on the left, Israel, Jordan, Syria, Iraq with the Tigris and Euphrates rivers on the right, Egypt and the Sinai at the bottom left, " + MAPA,
  "red_stamp|A hand slamming a red rubber stamp onto a brown paper case file, ink splash, dramatic close-up",
  "files_desk|A long dark desk covered with open brown case files and black and white photographs, a red stamp and a magnifying glass", ideia=True)

# ───────────────────────── 1. EL INSTITUTO ─────────────────────────
cap("1. El Instituto")
b("El Instituto. Israel nace en mayo de mil novecientos cuarenta y ocho, en guerra con los países árabes vecinos. Tiene espías, pero repartidos en servicios que compiten entre sí.",
  "israel_1948|Tel Aviv in May 1948, crowds in the street celebrating with blue and white flags without symbols, 1940s cars",
  "rival_offices|Two rival 1948 offices separated by a wall, men in shirtsleeves on telephones on each side, suspicious glances",
  "spy_1948|A 1948 man in a hat secretly photographing documents with a small camera in a dark office, a lamp",
  "radio_1948|A 1948 radio operator with headphones writing coded messages by candlelight",
  "jerusalem_1948|The old stone walls of Jerusalem in 1948 under a grey sky, sandbags and barbed wire", card="TEL AVIV, 1949")
b("El trece de diciembre de mil novecientos cuarenta y nueve, el primer ministro David Ben-Gurión crea un organismo para coordinarlos. Lo dirige un diplomático discreto, Reuven Shiloaj.",
  f"bengurion_desk|{BENGURION} signing a paper at a simple wooden desk, bookshelves behind@@DAVID BEN-GURIÓN",
  f"shiloah|{SHILOAH} standing by a window in a plain office with a closed briefcase@@REUVEN SHILOAJ",
  "cabinet_1949|Israeli ministers in 1949 around a modest wooden table in a plain room, cigarette smoke, papers",
  "order_1949|A typed 1949 government order on a desk with a fountain pen and a signature, no legible text@@13 DE DICIEMBRE DE 1949")
b("Su nombre completo es largo. Todos lo llaman Mossad. En hebreo, el Instituto.",
  "plain_door|A plain wooden office door in a 1950s Tel Aviv building with no sign at all, a man in a hat walking past",
  "hebrew_book|An old open Hebrew dictionary on a desk under a lamp, a pencil, letters too small to read",
  "card_index|A 1950s filing cabinet with an open drawer full of index cards, a hand pulling one out@@MOSSAD = \"EL INSTITUTO\"")
b("Responde solo ante el primer ministro. Durante décadas, Israel ni siquiera publica el nombre de su jefe.",
  "secret_phone|A black 1950s telephone on a desk in a dark office, a single lamp, a closed file with a red stamp",
  "shadow_chief|The silhouette of a man seen from behind standing in a dark office looking at a wall map, his face hidden",
  "blank_nameplate|A brass nameplate on an office desk with nothing engraved on it, an empty chair behind")
b("En mil novecientos cincuenta y dos llega al mando un hombre bajito y obsesivo, Isser Harel. Le dicen el pequeño Isser. Su primer gran caso no lo descubre un espía. Lo descubre un ciego.",
  f"harel_desk|{HAREL} leaning over a desk covered with files and photographs, a lamp, cigarette smoke@@ISSER HAREL",
  f"harel_window|{HAREL} looking out of a window at night, his reflection in the glass",
  "harel_files|Hundreds of index cards with small photographs of men spread on a table, a hand picking one, magnifying glass",
  "blind_glasses|A pair of very thick dark glasses and a white cane resting on a wooden table, close-up", ideia=True)

# ───────────────────────── 2. EL CIEGO ─────────────────────────
cap("2. El Ciego")
b("El Ciego. Coronel Suárez, provincia de Buenos Aires, mil novecientos cincuenta y siete. Lothar Hermann es un alemán de origen judío que huyó del nazismo. Está casi ciego.",
  "coronel_suarez|A quiet small town in the Argentine pampas in 1957, low white houses, a wide dirt street, a church tower and a horse cart",
  "pampa_road|A long straight dirt road across the flat Argentine pampa in 1957, a lone horse rider and telegraph poles",
  f"hermann|{HERMANN} sitting on a chair in a modest Argentine living room, listening carefully@@LOTHAR HERMANN", card="CORONEL SUÁREZ, 1957")
b("Su hija Silvia sale con un muchacho que presume de que su padre fue oficial nazi. El muchacho se apellida Eichmann.",
  f"silvia_date|{SILVIA} sitting with a young man in a 1950s Buenos Aires café, he is talking proudly, she looks uneasy",
  f"hermann_listen|{HERMANN} listening to his daughter at a kitchen table, his face tense",
  "proud_boy|A young man in a 1950s suit boasting at a café table, gesturing, a cigarette in his hand",
  "name_card|A small handwritten card with a single surname on it lying on a table next to thick dark glasses, unreadable scribble handwriting")
b("Adolf Eichmann organizó la deportación de millones de judíos a los campos de exterminio. Desde mil novecientos cincuenta vive en Argentina con otro nombre: Ricardo Klement.",
  "deportation_train|A long line of old wooden freight wagons on a railway track in a grey winter landscape in the 1940s, empty, seen from far away, somber",
  "klement_passport|A 1950s passport-like identity document lying open on a desk, a small photograph of a balding man with glasses, no legible text@@RICARDO KLEMENT",
  "ratline_ship|An ocean liner arriving at the port of Buenos Aires in 1950, passengers with suitcases coming down the gangway",
  "buenos_aires_50s|Buenos Aires in the 1950s, a wide avenue with trams, old cars and an obelisk in the distance")
b("Hermann le escribe a Fritz Bauer, un fiscal alemán. Bauer no confía en la policía de su país y le pasa el dato a Israel.",
  "letter_writing|An old man with thick dark glasses dictating a letter to his daughter at a table with a typewriter",
  f"bauer|{BAUER} reading a letter at his desk in a 1950s German office, piles of files@@FRITZ BAUER",
  "airmail|An airmail envelope with red and blue edges on a desk next to an Israeli diplomat's hat, no legible text")
b("Según varias versiones, el Mossad manda a un agente. Ve una casa pobre y concluye que un alto nazi no viviría así. Después conoce a Hermann y no le cree a un ciego.",
  "poor_house|A poor small house on an unpaved street on the outskirts of Buenos Aires in 1958, a stray dog, laundry hanging",
  "agent_doubt|A 1950s man in a hat standing in a dusty street looking at a poor house, shaking his head",
  "report_no|A short typed report on a desk with a large red circle stamp, an agent's hat next to it, no legible text",
  "file_drawer|A hand closing a filing cabinet drawer on a brown case file, dust in the lamp light")
b("El caso duerme casi dos años. Hasta que Bauer insiste. Entonces el Mossad vuelve a Buenos Aires.",
  "bauer_insist|A 1950s German prosecutor with wild grey hair pounding his fist on a desk in front of a visiting diplomat",
  "plane_ba|A 1960 propeller airliner landing at Buenos Aires airport at dusk",
  "dusty_file|A brown case file covered with dust on a shelf, a hand finally pulling it out, light falling on it", ideia=True)

# ───────────────────────── 3. LA CALLE GARIBALDI ─────────────────────────
cap("3. La Calle Garibaldi")
b("La Calle Garibaldi. San Fernando, en las afueras de Buenos Aires, once de mayo de mil novecientos sesenta. Son las ocho de la noche.",
  "garibaldi_night|A dark unpaved street on the outskirts of Buenos Aires at night in 1960, a single street lamp, low houses, a bus stop",
  "street_dogs|A lonely street lamp lighting a muddy corner of a poor Buenos Aires suburb at night in 1960, a dog barking, a distant train bridge",
  "bus_203|A 1960 Argentine city bus stopping at night on a dark road, its headlights on, a man getting off@@AUTOBÚS 203", card="SAN FERNANDO, 11 DE MAYO DE 1960")
b("Un hombre de cincuenta y cuatro años baja del autobús doscientos tres y camina hacia su casa. Lo esperan agentes del Mossad, junto a un auto con el capó levantado.",
  f"eichmann_walk|{EICHMANN} walking alone along a dark unpaved road at night, hands in his coat pockets",
  "car_hood|A 1950s black sedan parked on a dark road at night with its hood raised, two men pretending to fix the engine",
  "watch_time|A close-up of a man's wristwatch at night reading eight o'clock, a car window behind",
  "agents_wait|Two men in dark coats waiting in the shadows by a car at night, one checking his watch")
b("Lo derriban en segundos. Lo esconden nueve días en una casa alquilada. Allí admite quién es.",
  "the_grab|Shadows of men struggling by a car on a dark road at night, a hat falling to the ground, seen from far away",
  "safe_house|A modest rented house in a Buenos Aires suburb at night, all curtains closed, one dim light inside",
  f"eichmann_room|{EICHMANN} sitting on a bed in a bare room with a blindfold pushed up on his forehead, a guard's shadow on the wall@@ADOLF EICHMANN")
b("El veinte de mayo lo suben, drogado y vestido de tripulante, a un avión de la aerolínea israelí El Al. El avión había traído a la delegación israelí a los festejos por los ciento cincuenta años de la Revolución de Mayo argentina.",
  "elal_britannia|A 1960 four-engine propeller airliner in white and blue livery without lettering on a night runway at Buenos Aires airport, stairs at the door",
  "crew_disguise|Two men in airline crew uniforms supporting a drowsy third man in a crew uniform and cap up the stairs of an airliner at night",
  "may_celebration|Buenos Aires in May 1960 decorated for a national anniversary, light blue and white flags on the buildings, crowds@@20 DE MAYO DE 1960")
b("Tres días después, Ben-Gurión lo anuncia en el Knéset. Argentina protesta ante el Consejo de Seguridad de la ONU, que le pide a Israel una reparación.",
  f"knesset_1960|{BENGURION} speaking at a lectern in a crowded 1960 parliament hall, stunned faces",
  "un_council|The United Nations Security Council chamber in 1960, diplomats seated at the horseshoe table, a delegate speaking@@CONSEJO DE SEGURIDAD")
b("Eichmann es juzgado en Jerusalén y ejecutado en mil novecientos sesenta y dos. Pero el pequeño Isser ya tiene otra obsesión.",
  f"glass_booth|{EICHMANN} sitting inside a glass booth in a 1961 courtroom in Jerusalem, wearing headphones, rows of spectators@@JERUSALÉN, 1961",
  "newspapers_1960|A pile of 1960 newspapers from many countries with huge headlines made of unreadable shapes, a photo of a balding man with glasses",
  f"harel_window#detalhe-centro", ideia=True)

# ───────────────────────── 4. LAS CARTAS ─────────────────────────
cap("4. Las Cartas")
b("Las Cartas. En julio de mil novecientos sesenta y dos, Egipto exhibe misiles nuevos en un desfile en El Cairo. En su programa trabajan científicos alemanes, algunos del antiguo programa de cohetes de Hitler.",
  "cairo_parade|A 1962 military parade in Cairo, white missiles on trucks passing a crowd, minarets in the background",
  "german_scientists|German engineers in white coats around a rocket drawing in a 1962 workshop, a desert outside the window",
  "rocket_factory|A secret rocket factory in the Egyptian desert in 1962, hangars, a rocket body on a cradle", card="EL CAIRO, 1962")
b("Harel lo ve como una amenaza para la existencia de Israel. Y, según varias fuentes, el Mossad responde con sobres.",
  f"harel_desk#detalhe-centro",
  "envelopes|A stack of brown padded envelopes on a dark desk, one with a thin wire sticking out, ominous light@@OPERACIÓN DAMOCLES")
b("Una carta bomba estalla en una fábrica de cohetes cerca de El Cairo y mata a varios empleados egipcios. En Múnich, un empresario del programa desaparece sin dejar rastro. Otros reciben amenazas.",
  "factory_smoke|Smoke rising from a building in an Egyptian factory compound in 1962, seen from far away, people running",
  "munich_office|An empty 1962 office in Munich with an open door, a coat still on the hanger and a cold cup of coffee",
  "threat_phone|A German scientist at home at night answering a black telephone, his wife watching from the doorway, fear")
b("Pero Ben-Gurión no quiere romper con Alemania Occidental, que le vende armas a Israel en secreto. En marzo de mil novecientos sesenta y tres, Harel renuncia.",
  f"bengurion_angry|{BENGURION} standing behind his desk, firmly refusing, a stack of files in front of him",
  "resign_letter|A short typed resignation letter on a desk next to a pair of glasses, no legible text@@MARZO DE 1963")
b("Lo reemplaza un general, Meir Amit. Y el siguiente expediente vuelve a Sudamérica.",
  f"amit|{AMIT} at a desk covered with maps in a 1963 office, determined look@@MEIR AMIT",
  "map_southamerica|" + "South America from above, with Brazil, Uruguay and Argentina fully visible, the Río de la Plata estuary in the center, " + MAPA, ideia=True)

# ───────────────────────── 5. LA CASA ─────────────────────────
cap("5. La Casa")
b("La Casa. Herberts Cukurs fue un aviador famoso en Letonia. Durante la ocupación nazi, según sobrevivientes, participó en el asesinato de miles de judíos en Riga.",
  f"cukurs_pilot|{CUKURS.replace('in his sixties', 'in his thirties').replace('slicked-back grey hair', 'slicked-back blond hair').replace('light 1960s suit', '1930s leather aviator jacket')} next to a small propeller plane on a field in the 1930s",
  "riga_1941|The old town of Riga in 1941 under grey skies, church spires, empty streets, an oppressive atmosphere",
  f"cukurs|{CUKURS} standing on a dock by a seaplane in Brazil, tropical light@@HERBERTS CUKURS", card="RIGA, 1941")
b("Después de la guerra se instala en Brasil, en São Paulo. Nadie lo juzga.",
  "sao_paulo_60s|São Paulo in the early 1960s, modernist buildings and busy streets, a lake with small boats nearby",
  "seaplane_lake|A small seaplane on a calm lake near São Paulo at sunset, a wooden dock")
b("En mil novecientos sesenta y cuatro conoce a un empresario austríaco que le propone un negocio turístico en Uruguay. El empresario es un agente del Mossad.",
  "businessman|A well-dressed 1960s European businessman in a hotel lobby shaking hands with an older man, a briefcase on the floor",
  "brochure|A tourism brochure with a beach drawing and a business contract on a café table, two cups of coffee, no legible text")
b("El veintitrés de febrero de mil novecientos sesenta y cinco, Cukurs llega a una casa alquilada en Shangrilá, cerca de Montevideo. Allí lo esperan.",
  "shangrila_house|A quiet holiday house among pine trees in a seaside village near Montevideo in 1965, closed shutters, sandy road",
  "door_ajar|A wooden front door slightly open into a dark house, summer light outside, a footstep on the threshold@@SHANGRILÁ, URUGUAY", card="23 DE FEBRERO DE 1965")
b("Días después, la policía uruguaya encuentra su cuerpo en un baúl, con una nota firmada: Los que nunca olvidarán.",
  "police_uruguay|Uruguayan police officers in 1965 uniforms outside a holiday house, a police car, curious neighbours behind a rope",
  "trunk_note|A large closed wooden trunk on a tiled floor with a folded sheet of paper on top, seen from above, no legible text@@\"LOS QUE NUNCA OLVIDARÁN\"")
b("Que se sepa, es el único criminal de guerra nazi al que el Mossad mató. Mientras tanto, en Damasco, otro hombre de Israel acaba de caer.",
  "map_southamerica#detalhe-centro",
  "damascus_night|Damascus at night in 1965, domes and minarets, a dark apartment window with a faint light", ideia=True)

# ───────────────────────── 6. EL ESPÍA ─────────────────────────
cap("6. El Espía")
b("El Espía. Kamel Amin Tabet es un empresario sirio que vuelve a Damasco desde Buenos Aires. Da fiestas. Se hace amigo de oficiales y políticos.",
  f"cohen_party|{COHEN} raising a glass at an elegant evening party in a Damascus apartment, officers in uniform laughing around him@@KAMEL AMIN TABET",
  "damascus_street|A busy street in Damascus in 1962, old cars, a souk entrance, men in suits and keffiyehs", card="DAMASCO, 1962")
b("En realidad se llama Eli Cohen. Nació en Egipto y espía para Israel. Había construido su personaje en Argentina, entre la comunidad árabe de Buenos Aires.",
  f"cohen_mirror|{COHEN} looking at himself in a mirror while adjusting his tie, a second face reflected in shadow@@ELI COHEN",
  "ba_community|A 1961 Arab community club in Buenos Aires, men playing backgammon and drinking coffee, a portrait on the wall")
b("Durante tres años envía a Israel, en código morse, lo que oye en los salones de Damasco.",
  "morse_key|A hand tapping a telegraph morse key hidden inside a wooden cabinet, headphones, a dim lamp",
  "antenna_window|A thin wire antenna hidden along a window frame of an apartment at night, the city beyond")
b("En enero de mil novecientos sesenta y cinco, la contrainteligencia siria detecta sus transmisiones y lo detiene.",
  "radio_truck|A 1960s radio direction-finding truck with a rotating antenna on its roof parked in a dark Damascus street",
  "arrest_door|Syrian security officers bursting through an apartment door at night, a radio transmitter on a table")
b("El dieciocho de mayo lo ahorcan en público, en la plaza Marjeh. Su unidad, de la inteligencia militar, después pasa al Mossad.",
  "marjeh_square|The Marjeh square in Damascus at dawn in 1965, a monument column in the center, a silent crowd seen from far away, no bodies@@18 DE MAYO DE 1965",
  "empty_chair|An empty chair next to a silent radio transmitter in a dark room, dust in the light")
b("Israel ha perdido a su hombre en Damasco. Pero un año después, un piloto iraquí le trae algo mejor.",
  "mig_sky#médio-dir", ideia=True)

b("Si te gustan estos expedientes, suscríbete. Y ahora volvemos a ese avión.",
  "folder_stack|A tall stack of brown case files with red stamps on a desk, the top one slightly open, mysterious light inside")

# ───────────────────────── 7. EL MIG ─────────────────────────
cap("7. El MiG")
b("El MiG. El piloto iraquí se llama Munir Redfa. Es cristiano y, según su propio relato, no lo dejan ascender y le ordenan bombardear aldeas kurdas.",
  f"redfa|{REDFA} standing by a jet fighter on an airfield, troubled face@@MUNIR REDFA",
  "kurdish_village|A Kurdish mountain village of stone houses in northern Iraq in the 1960s, seen from far away from the air, peaceful", card="BAGDAD, 1966")
b("El jefe del Mossad, Meir Amit, quiere un MiG veintiuno desde hace años. Agentes del Mossad contactan a Redfa. Le ofrecen dinero, una vida nueva y sacar a su familia de Irak.",
  f"amit#médio-esq",
  "secret_meeting|Two men talking quietly at a café table in a European city in 1966, rain on the window, an envelope between them",
  "family_escape|An Iraqi family with suitcases climbing into a car at night, a mother holding a child, a driver waiting")
b("Al aterrizar, el avión recibe un nuevo número: cero cero siete. Los pilotos israelíes lo prueban hasta conocer cada debilidad. Después, Israel lo presta a Estados Unidos.",
  "mig_007|A silver MiG-21 jet fighter with Israeli blue Star of David roundels and a large painted number 007 on its nose, on an airfield@@MIG-21 Nº 007",
  "test_flight|A silver MiG-21 and an Israeli Mirage flying side by side in a mock dogfight over the desert, seen from far away",
  "us_cargo|A silver jet fighter being rolled into a huge US military cargo plane at night, American ground crew")
b("En junio de mil novecientos sesenta y siete estalla la Guerra de los Seis Días. Israel la gana. Y el Mossad parece infalible.",
  "six_day_war|Israeli Mirage jets flying low over the Sinai desert at dawn in June 1967, seen from far away, dust clouds@@JUNIO DE 1967",
  "jerusalem_1967|The Old City of Jerusalem in 1967 with soldiers in khaki walking near the old stone walls, golden light")
b("Cinco años después, en Múnich, descubre que no lo es.",
  "munich_rain|The Olympic stadium of Munich in 1972 with its tent-like transparent roof under dark rain clouds", ideia=True)

# ───────────────────────── 8. MÚNICH ─────────────────────────
cap("8. Múnich")
b("Múnich. Cinco de septiembre de mil novecientos setenta y dos, Juegos Olímpicos. Un comando palestino de Septiembre Negro entra en la villa olímpica y toma como rehenes al equipo israelí.",
  "olympic_village|The 1972 Munich Olympic village apartment blocks at night, a balcony, a masked silhouette seen from far away",
  "tv_crowd|Crowds and TV cameras behind a police line in Munich in 1972, worried faces, 1970s clothes", card="MÚNICH, 5 DE SEPTIEMBRE DE 1972")
b("El jefe del Mossad, Zvi Zamir, vuela a Alemania. Desde el aeródromo militar, ve fracasar el rescate de la policía alemana.",
  f"zamir|{ZAMIR} standing in a dark airfield control tower at night, watching through the window@@ZVI ZAMIR",
  "airfield_night|Two helicopters on a dark military airfield at night under floodlights, seen from far away, tense atmosphere")
b("Mueren los once miembros del equipo israelí. También un policía alemán y cinco de los ocho secuestradores.",
  "eleven_candles|Eleven candles burning in a row on a dark table, a folded Olympic program beside them@@11 ISRAELÍES",
  "memorial_stadium|A memorial ceremony in the 1972 Munich Olympic stadium, flags at half mast, a silent crowd")
b("Según historiadores y periodistas, la primera ministra Golda Meir aprueba entonces una campaña para matar a los responsables.",
  f"golda|{GOLDA} sitting at the head of a long table with grim men in suits, a cigarette, heavy silence@@GOLDA MEIR",
  "photo_wall|A wall with black and white photographs of men pinned in rows, a red string, a hand crossing one out, no legible text")
b("El dieciséis de octubre, en Roma, matan a tiros a Wael Zuaiter, un traductor palestino, en la entrada de su edificio. El ataque se atribuye al Mossad. Israel lo acusaba de pertenecer a Septiembre Negro. Su entorno siempre lo negó.",
  "rome_entrance|The entrance hall of an apartment building in Rome at night in 1972, a dropped grocery bag and a book on the floor, no people, no blood@@ROMA, 16 DE OCTUBRE DE 1972",
  "map_europe|" + "Western Europe and the Mediterranean from above, from Norway and Scandinavia at the top to Italy, Cyprus and Lebanon at the bottom right, " + MAPA)
b("La lista se acorta en París, en Chipre, en Beirut. Pero el hombre más buscado, Alí Hasán Salameh, sigue libre. Hasta que un equipo cree verlo en un pueblo de Noruega.",
  "paris_street|A Paris street at night in 1972 with a parked car and a lit café, a man in a coat walking away",
  "salameh_photo|A blurry black and white surveillance photograph of a handsome man with sunglasses pinned to a board, a red circle around him@@ALÍ HASÁN SALAMEH",
  "norway_village|A small Norwegian town in summer 1973, wooden houses, a lake and green mountains, long evening light", ideia=True)

# ───────────────────────── 9. EL CAMARERO ─────────────────────────
cap("9. El Camarero")
b("El Camarero. Lillehammer, Noruega, veintiuno de julio de mil novecientos setenta y tres. Un hombre sale del cine con su esposa, que está embarazada.",
  "cinema_exit|A small-town cinema in Norway at night in 1973, a couple walking out under the marquee lights without letters",
  "couple_walk|A young couple walking along a quiet Norwegian street at night, the woman visibly pregnant, warm street lamps", card="LILLEHAMMER, 21 DE JULIO DE 1973")
b("Caminan hacia el autobús. Un auto se detiene junto a ellos. Le disparan varias veces.",
  "car_stops|A 1970s car stopping beside a bus stop on an empty Norwegian street at night, its headlights glaring",
  "bus_stop_empty|An empty bus stop on a quiet street at night after an incident, a woman's scarf on the ground, no body, no blood")
b("Se llamaba Ahmed Bujiki. Era un camarero marroquí. No tenía nada que ver con Múnich. El Mossad había confundido a un inocente con Salameh.",
  "waiter|A young Moroccan waiter in a white jacket carrying a tray in a modest Norwegian hotel restaurant in 1973@@AHMED BUJIKI",
  "two_photos|Two black and white photographs side by side on a table, two different dark-haired men who look slightly alike, a magnifying glass")
b("La policía noruega detiene a seis miembros del equipo. Varios son condenados. En mil novecientos noventa y seis, Israel indemniza a la viuda y a la hija, sin admitir responsabilidad.",
  "norway_court|A 1974 Norwegian courtroom, defendants on a bench, a judge, journalists taking notes",
  "compensation|A sealed envelope and a short typed document on a dark desk, an official pen, no legible text@@1996: INDEMNIZACIÓN")
b("A Salameh lo matan en Beirut en mil novecientos setenta y nueve, con un coche bomba. Pero antes, el Mossad recibe un aviso decisivo.",
  "beirut_street|A Beirut street in 1979 with tall apartment buildings and palm trees, smoke rising in the distance seen from far away@@BEIRUT, 1979",
  "phone_ring|A black telephone ringing on a desk at night, a hand reaching for it", ideia=True)

# ───────────────────────── 10. EL ÁNGEL ─────────────────────────
cap("10. El Ángel")
b("El Ángel. El Mossad tiene un agente en el corazón de Egipto: Ashraf Marwan, yerno del fallecido presidente Nasser y asesor del nuevo presidente, Sadat. En sus archivos lo llaman el Ángel.",
  f"marwan|{MARWAN} walking out of a presidential palace in Cairo in 1973, a briefcase in his hand, wide horizontal street scene@@ASHRAF MARWAN",
  "cairo_palace|A presidential palace in Cairo in the early 1970s with guards at the gate, palm trees",
  "angel_file|A brown case file on a dark desk with a red stamp and a small black and white photo of an elegant young man@@\"EL ÁNGEL\"", card="EL CAIRO, 1973")
b("El cinco de octubre de mil novecientos setenta y tres, Marwan pide una reunión urgente en Londres. Zamir vuela esa misma tarde.",
  "london_night|London at night in 1973, a wet street with black cabs and red buses, a tall apartment building",
  f"zamir_plane|{ZAMIR} looking out of an airplane window at night, a folder on his lap@@LONDRES, 5 DE OCTUBRE DE 1973")
b("Cerca de la medianoche, Marwan le dice que Egipto y Siria atacarán al día siguiente.",
  f"marwan_meeting|{MARWAN} and {ZAMIR} talking face to face in a dim London apartment at night, a lamp between them",
  "clock_midnight|A wall clock showing almost midnight in a dark room, a cup of tea untouched")
b("Zamir llama a Tel Aviv de madrugada. Es Yom Kipur. El país está en silencio.",
  "zamir_phone|A man in a grey suit speaking urgently into a hotel room telephone at night, rain on the window",
  "empty_road|An empty highway in Israel on the day of Yom Kippur 1973, no cars at all, a quiet town in the distance")
b("Egipto y Siria atacan a las dos de la tarde, horas antes de lo previsto. Los reservistas israelíes no alcanzan a movilizarse a tiempo.",
  "sinai_1973|Egyptian soldiers crossing a wide canal in rubber boats under a hazy sky in October 1973, seen from far away@@6 DE OCTUBRE DE 1973",
  "reservists|Israeli reservists in civilian clothes running to buses with rifles and bags in a city street, urgency")
b("Hasta hoy se discute si Marwan era leal a Israel o un agente doble de Egipto. Murió en Londres en dos mil siete, al caer de un balcón, en circunstancias que nunca se aclararon. Después de la guerra, el Mossad cambia. Y a veces, su misión es rescatar.",
  "london_balcony|A tall elegant London apartment building in daylight with a high balcony, a police tape at the entrance below, no body",
  "two_faces|An elegant Egyptian man in a 1970s suit standing in a dim room by a window, half of his face in warm light and half in deep shadow, wide interior shot",
  "red_sea_coast|The Red Sea coast of Sudan seen from the air, turquoise water, coral reefs and empty desert", ideia=True)

# ───────────────────────── 11. EL HOTEL ─────────────────────────
cap("11. El Hotel")
b("El Hotel. Costa de Sudán, en el mar Rojo, principios de los años ochenta. Un pequeño hotel de buceo abre para turistas europeos.",
  "arous_resort|A small 1980s diving resort of white bungalows on an empty beach of the Red Sea in Sudan, palm umbrellas, turquoise water",
  "divers|European tourists in 1980s diving gear on a wooden boat in turquoise water, a smiling instructor", card="SUDÁN, 1981")
b("Los instructores son agentes del Mossad. Los turistas no lo saben.",
  "instructor|A tanned 1980s diving instructor with a mustache checking an air tank on a beach, his eyes looking at the horizon",
  "map_redsea|" + "the Red Sea from above, with Egypt and Israel at the top, Sudan on the left coast, Saudi Arabia on the right and Ethiopia at the bottom left, " + MAPA)
b("De noche, salen en camiones hacia los campos de refugiados. Allí esperan miles de judíos etíopes que huyeron a pie del hambre y de la guerra.",
  "trucks_night|Two old trucks with their headlights off driving across a dark desert at night, stars above",
  "refugee_camp|A vast refugee camp of tents and huts in eastern Sudan in the early 1980s at dusk, Ethiopian families, smoke from cooking fires",
  "walking_family|An Ethiopian family walking barefoot across a dry landscape carrying bundles, seen from far away, dawn light")
b("Los llevan a la playa y lanchas de la marina israelí los recogen en la oscuridad.",
  "beach_boats|Inflatable boats arriving on a dark beach at night, people wading into the water helped by men, moonlight",
  "ship_night|A navy ship waiting offshore on the Red Sea at night with its lights off, seen from far away")
b("Según los relatos publicados, así salen de Sudán miles de personas. Después vienen los puentes aéreos, como la Operación Moisés, entre mil novecientos ochenta y cuatro y ochenta y cinco.",
  "airlift|Ethiopian families climbing the stairs of a large passenger airplane at night on a desert airstrip@@OPERACIÓN MOISÉS, 1984",
  "arrival_israel|Ethiopian families stepping off an airplane at dawn in Israel, an elderly man kneeling to touch the ground")
b("Mientras unos agentes rescatan a desconocidos, otros persiguen a un técnico israelí que quiere contar un secreto.",
  "dimona_night|A large silver dome of a nuclear research center in the Negev desert at night, fences and searchlights, seen from far away", ideia=True)

# ───────────────────────── 12. LA MANO ─────────────────────────
cap("12. La Mano")
b("La Mano. Mordejái Vanunu trabajó nueve años como técnico en la central nuclear de Dimona, en el desierto del Néguev.",
  f"vanunu_work|{VANUNU} in a white technician coat in a control room with old analog panels@@MORDEJÁI VANUNU",
  "dimona_day|A nuclear research center with a silver dome in the Negev desert in daylight, fences, sand dunes", card="DIMONA, 1985")
b("En mil novecientos ochenta y seis le cuenta al diario británico The Sunday Times que allí Israel fabrica armas nucleares. Tiene fotos.",
  "film_rolls|Two rolls of photographic film and a handful of black and white photos of industrial machinery on a table",
  "newsroom_1986|A busy 1986 London newspaper newsroom, journalists at typewriters and early computers, cigarette smoke@@THE SUNDAY TIMES, LONDRES")
b("En Londres conoce a una turista estadounidense que se presenta como Cindy. Ella lo convence de viajar a Roma.",
  "cindy|A blonde woman in a 1980s trench coat smiling at a man in a London square, pigeons, autumn light@@\"CINDY\"",
  "train_rome|A couple sitting in an airplane window seat, the woman resting her head on the man's shoulder, he smiles")
b("El treinta de septiembre, en un apartamento de Roma, lo esperan agentes del Mossad. Lo drogan y lo llevan por mar a Israel.",
  "rome_apartment|The dark hallway of a Rome apartment in 1986, a door opening, shadows of men waiting inside@@ROMA, 30 DE SEPTIEMBRE DE 1986",
  "ship_sea|A cargo ship sailing across the Mediterranean at night, seen from far away")
b("El cinco de octubre, el periódico publica la historia. Vanunu ya está preso y nadie sabe dónde.",
  "newspaper_print|A huge rotary printing press running at night, newspapers flowing out with large headlines made of unreadable shapes",
  "prison_cell|A small bare prison cell with a narrow bed and a high window, a man sitting with his head in his hands")
b("Semanas después, lo llevan en una camioneta al tribunal. Aprieta la mano contra la ventanilla. En la palma había escrito que lo secuestraron en Roma.",
  "van_window|A man's open palm pressed against the window of a police van, handwritten ink letters on the palm made of unreadable scribbles, photographers outside",
  "photographers|Press photographers with 1980s cameras crowding around a police van, flashes@@SECUESTRADO EN ROMA")
b("Lo condenan a dieciocho años de prisión y los cumple todos. Israel, hasta hoy, no confirma ni niega tener armas nucleares. Cuatro años después, el Mossad tiene un problema nuevo: uno de los suyos quiere contarlo todo.",
  "court_1988|A 1988 courtroom in Israel, a bearded man standing between guards as the verdict is read@@18 AÑOS",
  "typewriter_night|A typewriter with a half-written page on a kitchen table at night, a cup of coffee, a man's hands", ideia=True)

# ───────────────────────── 13. EL LIBRO ─────────────────────────
cap("13. El Libro")
b("El Libro. Septiembre de mil novecientos noventa. Victor Ostrovsky, un exagente del Mossad nacido en Canadá, publica sus memorias.",
  f"ostrovsky|{OSTROVSKY} sitting at a table with a stack of new hardcover books with plain dark covers@@VICTOR OSTROVSKY",
  "book_cover|A hardcover book with a plain dark blue cover lying on a desk under a lamp, no title, no letters", card="NUEVA YORK, 1990")
b("Israel le pide a un juez de Nueva York que prohíba el libro. Dice que pone en peligro a sus agentes. El juez lo prohíbe.",
  "ny_court|A New York courthouse with stone columns in 1990, lawyers walking up the steps with briefcases",
  "judge_gavel|A judge's gavel coming down on a wooden desk next to a hardcover book@@PROHIBIDO")
b("Menos de dos días después, un tribunal de apelación levanta la prohibición. Y el escándalo convierte el libro en el primero de la lista de más vendidos del New York Times.",
  "bookstore|A 1990 bookstore window in New York with a huge pyramid of the same dark blue book, people looking in@@Nº 1 EN VENTAS",
  "readers|People reading the same dark blue hardcover book on a New York subway train in 1990")
b("Muchas de sus afirmaciones nunca se confirmaron. Pero la lección queda: intentar callar un secreto puede hacerlo más ruidoso.",
  "file_burning|A brown case file with a red stamp half open, papers flying out in the wind, dramatic light",
  "berlin_wall_1990|People with hammers chipping away at a graffiti-covered concrete wall in Berlin in 1990, crowds, celebration, seen from far away")
b("Al año siguiente, la Unión Soviética desaparece. Y aquí se cierra este expediente.",
  "folder_close|A hand closing a thick brown case file with a red circular stamp on a dark desk, lamp light", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. El MiG")
b("El MiG. Hoy, el MiG veintiuno de Munir Redfa está en el museo de la Fuerza Aérea de Israel, en Hatzerim, en el desierto del Néguev. Todavía lleva pintado el número cero cero siete.",
  "museum_mig|A silver MiG-21 jet fighter with the painted number 007 on its nose displayed outdoors in an air force museum in the Negev desert, other old planes behind, sunny day@@HATZERIM, DESIERTO DEL NÉGUEV",
  "museum_detail|Close-up of the nose of an old silver jet fighter with a faded painted number 007, sun-bleached metal")
b("Redfa nunca volvió a Irak.",
  "old_pilot|An elderly man with a grey mustache looking at an old black and white photograph of a young pilot next to a jet, a window with rain")
b("El Mossad cumple setenta y seis años, en un Medio Oriente que sigue en conflicto.",
  "tel_aviv_night#aberto",
  "sealed_boxes|Rows of sealed archive boxes with red stamps disappearing into darkness")
b("El Mossad nunca fue grande. Lo grande fueron los secretos que cupieron en una sola persona: un ciego, un piloto, un técnico.",
  "blind_glasses#detalhe-centro", "mig_landed#médio-dir", "van_window#detalhe-centro", ideia=True)
b("Y tú, ¿qué expediente del Mossad crees que todavía no conocemos? Déjalo en los comentarios.",
  "files_desk", "mossad_folder#aberto")

# a 1ª prova (04/11) saiu com moldura de papel: todo prompt leva sangria explícita
SANGRIA = ", full-bleed illustration filling the entire frame edge to edge, no border, no margin, no white frame, no panel outline"

THUMBS = [
    {"id": "thumb-A", "prompt": "A 1960s Israeli intelligence agent in half body on the LEFT third of the frame, dark suit and thin tie, holding a brown case folder with a red circular stamp, behind him a silver delta-wing jet fighter on a desert airfield; the RIGHT half of the image is plain empty pale sky, no signage, no lettering"},
    {"id": "thumb-B", "prompt": "A thin balding man with glasses in a 1960 civilian suit seen in half body on the LEFT third of the frame, walking on a dark unpaved suburban street at night under a single street lamp, a bus far behind; the RIGHT half of the image is plain dark empty night sky, no signage, no lettering"},
    {"id": "thumb-C", "prompt": "A silver delta-wing MiG-21 jet fighter flying low on the LEFT third of the frame over a brown desert, seen from the side, plain bare silver metal tail and fuselage without any flag, roundel or marking, a tense pilot's face in shadow in the lower left corner; the RIGHT half of the image is plain empty hazy sky, no signage, no lettering, no insignia"},
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
