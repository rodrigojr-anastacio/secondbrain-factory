#!/usr/bin/env python3
"""Fonte única do dossie-es 001 (CIA): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (na pasta do vídeo). Conteúdo no topo; geração no fim (adaptada do historia-ptbr 003).

Padrão (historia-ptbr 003, 04/11/2026): hook por anedota (Guatemala, 1954) → 13 expedientes-objeto, título falado
("La Radio.") → cierre que volta à radio (Clinton, 1999) + aforismo + pergunta.
Texto em espanhol neutro latino-americano, ESCRITO PARA A FALA: frases de 4–14 palavras, números por extenso.
Fatos conferidos em 04/11/2026 (ver SOURCES.md, seção "Checagem de 04/11").

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (id I### na ordem de aparição) · "chave" reuso · "chave#enq" reuso com enquadramento
  + "@@TEXTO"      rótulo na tela (máquina de escrever; CAIXA ALTA, até ~28 caracteres)
Bloco: b(texto, *planos, card="CIUDAD DE GUATEMALA, 1954", ideia=True) · capítulo: cap("5. La Radio")
card = rótulo de cena [PANTALLA] (tira de papel em máquina de escrever, canto superior esquerdo).
Mapas (chave map_*): base sem texto nem pinos; pinos, setas e nomes no código (src/labels.jsx).
"""
import json, math, re
from pathlib import Path

WPS = 2.3            # palavras/s com as pausas entre frases (amostras Fish es: ~138 ppm)
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
TITULO = "TODA la historia de la CIA"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# Personagens (descrição visual fixa; rostos "resembling", nunca foto)
DONOVAN = "a stocky silver-haired American general in his late 50s resembling William 'Wild Bill' Donovan, 1940s US Army uniform"
TRUMAN = "a 1940s American president resembling Harry Truman, round glasses, grey double-breasted suit"
DULLES = "a 1950s CIA director resembling Allen Dulles, white mustache, round rimless glasses, pipe, tweed suit"
ARBENZ = "a 1950s Guatemalan president resembling Jacobo Arbenz, slim, combed-back light brown hair, dark suit"
CASTILLO = "a 1950s Guatemalan colonel with a thin mustache, khaki uniform and military cap"
MOSADDEQ = "an elderly bald Iranian prime minister resembling Mohammad Mosaddegh, long nose, grey suit"
KERMIT = "a 1950s American agent in his late 30s resembling Kermit Roosevelt Jr., glasses, light summer suit"
GOTTLIEB = "a thin 1950s American chemist with dark curly hair in a white lab coat"
OLSON = "a 1950s American scientist in his early 40s with receding hair, dark suit and tie"
KENNEDY = "a 1960s American president resembling John F. Kennedy, dark suit"
CASTRO = "a bearded Cuban revolutionary leader resembling Fidel Castro, olive green fatigues and cap"
ALLENDE = "a Chilean president resembling Salvador Allende, thick black-rimmed glasses, mustache, presidential sash"
NIXON = "a 1970 American president resembling Richard Nixon, dark suit"
HELMS = "a 1970 CIA director resembling Richard Helms, slicked-back grey hair, dark suit"
MUJ = "Afghan mujahideen fighters in pakol wool hats and shawls"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, borders and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame"

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Ciudad de Guatemala, junio de mil novecientos cincuenta y cuatro. Cada noche, una radio clandestina anuncia que miles de rebeldes avanzan sobre la capital.",
  "gt_city_night|Guatemala City at night in 1954, low colonial houses and a cathedral dome, volcanoes silhouetted behind, a few lit windows",
  "radio_family|A Guatemalan family in 1954 gathered around a wooden tube radio in a modest living room at night, worried faces, a volcano visible through the window",
  "radio_dial|Close-up of the glowing dial of a 1950s wooden tube radio at night, a hand turning the knob",
  "rebels_imagined|Hundreds of armed rebel soldiers marching through a dark jungle toward a city, dramatic and exaggerated like a propaganda vision", card="CIUDAD DE GUATEMALA, 1954")
b("Dice que transmite desde la selva. El presidente Jacobo Árbenz ya no sabe a quién creer. Su ejército, tampoco.",
  "jungle_antenna|A makeshift radio antenna hidden among tall jungle trees at night, a cable running to a tent",
  f"arbenz_desk|{ARBENZ} sitting at his desk in the presidential palace at night, listening to a radio, exhausted@@JACOBO ÁRBENZ",
  "officers_doubt|Guatemalan army officers in 1954 khaki uniforms whispering in a dim barracks corridor, distrustful looks",
  "army_trucks_idle|Guatemalan army trucks parked and idle at a barracks gate in 1954, soldiers sitting and waiting, nobody moving")
b("El veintisiete de junio, Árbenz renuncia.",
  "arbenz_resign|A 1950s president at a microphone in a palace room, reading a resignation speech from a sheet of paper, tired face, radio microphones",
  "palace_dawn|The green-stone National Palace of Guatemala at dawn, empty square, an atmosphere of defeat@@27 DE JUNIO DE 1954")
b("[serious] Los miles de rebeldes eran menos de quinientos. Y la radio… la operaba la CIA.",
  "few_rebels|A small group of about forty tired rebel soldiers with old rifles resting on a muddy jungle road, far fewer than expected@@MENOS DE 500",
  "radio_studio_cia|A 1950s American man in shirtsleeves speaking into a microphone in a small hidden radio studio, reel-to-reel tape machines, a folder with a red stamp on the table",
  "cia_folder|A brown paper case file on a dark desk with a red circular stamp, a fedora and a pair of glasses beside it, lamp light")
b("Esta es toda la historia de la CIA. Y de lo que hizo, una y otra vez, en América Latina.",
  "langley_hq|The white modernist CIA headquarters building in Langley among autumn trees, 1960s black sedans in the parking lot",
  "map_americas|" + "Latin America: from the southern United States and Mexico at the top, through Central America and the Caribbean, down to the southern tip of South America with Chile fully visible at the bottom, " + MAPA,
  "files_desk|A long dark desk covered with open brown case files and black and white photographs, a red stamp and a magnifying glass", ideia=True)

# ───────────────────────── 1. EL CORONEL ─────────────────────────
cap("1. El Coronel")
b("El Coronel. Para entender a la CIA, hay que empezar antes de que exista. En mil novecientos cuarenta y uno, Estados Unidos no tiene ningún servicio de espionaje en el exterior.",
  "washington_1941|Washington D.C. in 1941, the Capitol dome under a grey sky, 1940s cars and pedestrians in hats",
  "empty_office|An empty government office in 1941 with bare desks, an unplugged telephone and a blank world map on the wall",
  "roosevelt_desk|A 1940s American president resembling Franklin D. Roosevelt with a cigarette holder at his desk, signing a paper", card="WASHINGTON, 1941")
b("Roosevelt le encarga la tarea a un abogado de Nueva York, héroe de la Primera Guerra Mundial. Se llama William Donovan, y todos le dicen Wild Bill.",
  "lawyer_office|A 1930s Manhattan law office with wood panels, a window over skyscrapers, a man in a three-piece suit",
  f"donovan_ww1|{DONOVAN.replace('in his late 50s', 'in his 30s').replace('1940s US Army uniform', 'World War I officer uniform with a medal')} in a muddy trench in France in 1918",
  f"donovan_portrait|{DONOVAN} standing confidently in a 1940s office with a map of Europe behind him@@WILLIAM \"WILD BILL\" DONOVAN")
b("En junio de mil novecientos cuarenta y dos, su oficina se convierte en la OSS: la Oficina de Servicios Estratégicos.",
  "oss_building|A row of plain brick government buildings in Washington in 1942, men in uniform and suits walking in@@OSS · JUNIO DE 1942",
  "oss_staff|A busy 1942 office: young men and women at typewriters and maps, an officer giving orders")
b("La OSS lanza agentes en paracaídas detrás de las líneas nazis. Arma a la resistencia francesa. Falsifica documentos.",
  "parachute_night|Agents parachuting at night from a WWII bomber over the French countryside, moonlight",
  "resistance_arms|French resistance fighters in berets in a barn at night opening a parachuted container full of rifles@@RESISTENCIA FRANCESA",
  "forger_desk|A forger at a desk under a lamp copying a stamp on a fake identity card with a fine pen, magnifying glass")
b("Pero en septiembre de mil novecientos cuarenta y cinco, con la guerra terminada, el presidente Truman la disuelve. En Washington, muchos temen crear una Gestapo en tiempos de paz.",
  f"truman_sign|{TRUMAN} signing an order at his desk in the Oval Office in 1945@@HARRY TRUMAN",
  "oss_boxes|Workers carrying cardboard boxes of files out of a government office, an empty desk, autumn 1945",
  "senators_worry|Worried American congressmen in 1945 reading a newspaper in a marble corridor of the Capitol", ideia=True)
b("Ese miedo dura muy poco.",
  "soviet_shadow|A huge dark shadow of a Soviet soldier falling across a map of Europe on a wall, ominous")

# ───────────────────────── 2. LA LEY ─────────────────────────
cap("2. La Ley")
b("La Ley. La Unión Soviética ya no es aliada. Es el enemigo.",
  "iron_curtain|Soviet soldiers and barbed wire at a border in Central Europe in 1947, watchtower, grey winter",
  "kremlin_1947|The Kremlin in Moscow in 1947 with red stars on the towers, snow")
b("El veintiséis de julio de mil novecientos cuarenta y siete, Truman firma la Ley de Seguridad Nacional. Con ella nace la Agencia Central de Inteligencia.",
  "truman_plane|A 1940s presidential propeller plane on a runway in July 1947, an aide running up the stairs with a folder",
  "law_document|A typed 1947 law document on a desk with a fountain pen and a signature, an eagle seal embossed, no legible text@@LEY DE SEGURIDAD NACIONAL",
  "cia_birth|A plain government building door in Washington in 1947 with men in fedoras entering, a new brass plaque without text", card="26 DE JULIO DE 1947")
b("Su misión parece técnica: reunir y analizar información para el presidente. Pero la ley incluye una frase vaga.",
  "analysts_1947|1940s intelligence analysts in shirtsleeves reading reports and marking maps with pencils in a smoky room",
  "report_president|A thin folder with a red stamp delivered on a silver tray to the president's desk",
  "magnifier_clause|A magnifying glass over one paragraph of a typed legal document, the rest of the page blurred, no legible text")
b("La agencia podrá cumplir otras funciones y deberes relacionados con la inteligencia. En esa frase cabe casi todo. Y la CIA la va a usar para casi todo.",
  "open_door|A dark corridor with many doors opening at once, light coming out of each, mysterious@@\"OTRAS FUNCIONES Y DEBERES\"",
  "toolbox_spy|An open spy briefcase on a table full of cash, a pistol, a radio transmitter, fake passports and a small camera")

# ───────────────────────── 3. LAS MALETAS ─────────────────────────
cap("3. Las Maletas")
b("Las Maletas. La primera gran prueba llega en Italia. En abril de mil novecientos cuarenta y ocho hay elecciones, y el Partido Comunista puede ganarlas.",
  "rome_1948|Rome in April 1948, a crowded piazza with election posters on the walls, Vespas and old Fiat cars, St Peter's dome behind",
  "communist_rally|A huge communist rally in an Italian piazza in 1948 with red flags (no symbols) and a speaker on a balcony",
  "map_atlantic|" + "the North Atlantic ocean with the east coast of the United States on the left and Western Europe and Italy on the right, " + MAPA, card="ROMA, ABRIL DE 1948")
b("La CIA responde con dinero en efectivo. Maletas de billetes para los democristianos y sus aliados.",
  "suitcase_cash|An open leather suitcase stuffed with bundles of banknotes on a hotel bed in Rome, a man in a hat closing the curtains",
  "handover|Two men in 1940s suits exchanging a heavy briefcase in a dark Roman alley at night@@DINERO DE LA CIA")
b("Desde Estados Unidos llegan miles de cartas de italoestadounidenses a sus familias. Y hay propaganda por todas partes.",
  "letters_writing|An Italian-American grandmother in a Brooklyn kitchen in 1948 writing a letter to Italy, a photo of her village on the table",
  "letters_pile|A huge pile of airmail envelopes in a post office sorting room in 1948",
  "posters_wall|A wall in Rome covered with 1948 election posters with cartoon drawings and no legible text, people reading them")
b("Los democristianos ganan con casi la mitad de los votos. En Washington, la conclusión es peligrosa.",
  "ballot_count|Italian election officials counting paper ballots on long tables in 1948, piles of ballots@@48,5 % DE LOS VOTOS",
  "dc_victory|Christian Democrat supporters celebrating in a Roman street in 1948 waving white flags with a shield (no text)")
b("Se puede cambiar el rumbo de un país sin disparar un solo tiro. Y sin que nadie se entere.",
  "chess_globe|A hand in a dark suit sleeve moving a chess piece on a board painted like a world map, dramatic light",
  "shh_office|A 1940s official in a dark office putting a finger to his lips, a closed file with a red stamp on his desk", ideia=True)

# ───────────────────────── 4. EL PETRÓLEO ─────────────────────────
cap("4. El Petróleo")
b("El Petróleo. En mil novecientos cincuenta y uno, el primer ministro de Irán, Mohammad Mosaddeq, nacionaliza el petróleo. Hasta entonces estaba en manos de una compañía británica.",
  "abadan_refinery|The huge Abadan oil refinery in Iran in 1951, tall chimneys and storage tanks, flames, workers",
  f"mosaddeq_speech|{MOSADDEQ} speaking passionately in the Iranian parliament in 1951@@MOHAMMAD MOSADDEQ",
  "map_iran|" + "Iran and the Persian Gulf with the Caspian Sea above, unnamed seas and unnamed lands, a cartographer's blank base map without any writing, " + MAPA,
  "british_leave|British oil company engineers in khaki shorts boarding a ship with suitcases at an Iranian port, Iranian crowds watching", card="TEHERÁN, 1951")
b("Londres pide ayuda a Washington. Y en agosto de mil novecientos cincuenta y tres, un agente de la CIA reparte dinero en Teherán.",
  "churchill_phone|An elderly British prime minister with a cigar on a telephone in a London office in 1953, rain on the window",
  "tehran_1953|Tehran in August 1953, a dusty avenue with old buses, horse carts and mountains behind")
b("Se llama Kermit Roosevelt, y es nieto de un expresidente. Paga multitudes que gritan en las calles. Paga periódicos. Paga oficiales.",
  f"kermit|{KERMIT} in a dim Tehran villa counting bundles of Iranian banknotes on a table@@KERMIT ROOSEVELT",
  "paid_crowd|A shouting crowd marching in a Tehran street in 1953 with sticks and portraits held high, dust",
  "newspaper_press|An old printing press in Tehran printing newspapers in 1953, a man slipping an envelope to the editor")
b("El diecinueve de agosto, Mosaddeq cae. El sha vuelve al poder, y lo conserva hasta mil novecientos setenta y nueve.",
  "tanks_tehran|Military tanks parked on a wide Tehran avenue in August 1953, soldiers standing guard and a crowd watching, dusty summer light@@19 DE AGOSTO DE 1953",
  "shah_throne|The Shah of Iran on an ornate throne in a mirrored palace hall, 1970s")
b("Washington tarda casi medio siglo en reconocerlo. En dos mil trece, documentos de la propia CIA lo dicen sin rodeos: el golpe se hizo bajo la dirección de la CIA.",
  "archive_boxes|Endless shelves of grey archive boxes in a government archive, a single lamp",
  "declass_doc|A declassified document with black redaction bars and a red DECLASSIFIED-style stamp shape without letters, on a desk in 2013@@DESCLASIFICADO, 2013", ideia=True)

# ───────────────────────── 5. LA RADIO ─────────────────────────
cap("5. La Radio")
b("La Radio. Un año después, el mismo método llega a América Latina. En Guatemala, Árbenz impulsa una reforma agraria y expropia tierras sin cultivar.",
  "gt_fields|Guatemalan Maya peasants in 1952 receiving land titles at a rural table, green hills and a volcano",
  f"arbenz_reform|{ARBENZ} addressing a crowd of peasants from a balcony in 1952, cheering@@REFORMA AGRARIA, 1952", card="GUATEMALA, 1954")
b("La mayor afectada es una empresa estadounidense: la United Fruit Company.",
  "banana_plantation|An endless banana plantation in Guatemala in the 1950s with workers carrying bunches and a railway@@UNITED FRUIT COMPANY",
  "banana_ship|A white banana cargo ship at a Caribbean port in the 1950s, bananas loaded by conveyor")
b("La CIA monta la operación PB Success. Entrena a un pequeño ejército de exiliados, al mando del coronel Carlos Castillo Armas.",
  "map_central|" + "Central America and the Caribbean: southern Mexico, Guatemala, Honduras, Nicaragua, Cuba and Florida, " + MAPA,
  "training_camp|A secret training camp in the Honduran jungle in 1954, exiles in mixed uniforms practicing with rifles, an American instructor@@OPERACIÓN PBSUCCESS",
  f"castillo|{CASTILLO} standing in front of his men in a jungle camp@@CARLOS CASTILLO ARMAS")
b("Aviones sin bandera bombardean la capital. Y la radio, la Voz de la Liberación, convierte a unos cientos de hombres en un ejército imparable.",
  "planes_unmarked|Two unmarked WWII propeller fighter planes with no insignia flying low over Guatemala City, smoke rising",
  "radio_mic|A vintage microphone in a dark room with a red ON AIR lamp shape without letters, a hand holding a script@@LA VOZ DE LA LIBERACIÓN",
  "listeners_fear|Frightened Guatemalan soldiers listening to a radio in a barracks at night")
b("Árbenz cae. Guatemala entra en décadas de gobiernos militares y en una guerra civil con más de doscientos mil muertos y desaparecidos.",
  "arbenz_exile|A 1950s former president in a suit walking toward an airplane with his family, guarded by soldiers, sad",
  "memorial_candles|Hundreds of candles and flowers in front of a long wall of small photographs of missing people in a Guatemalan town square, women in traditional Maya clothes mourning@@MÁS DE 200.000 VÍCTIMAS")
b("Guarda esa radio. Vamos a volver a ella.",
  "radio_dust|An old wooden tube radio on a shelf covered with dust, a single beam of light")
b("Si quieres más expedientes como este, suscríbete. Porque el que sigue es el más extraño de todos.",
  "folder_stack|A tall stack of brown case files with red stamps on a desk, the top one slightly open, mysterious light inside")

# ───────────────────────── 6. EL ÁCIDO ─────────────────────────
cap("6. El Ácido")
b("El Ácido. Mientras tanto, la CIA tiene miedo de algo que no puede ver: el control de la mente.",
  "brain_fear|A 1950s American official staring at a medical illustration of a human brain pinned to a wall, paranoid shadows",
  "pow_korea|American prisoners of war in Korea in 1953 in a camp, blank stares", ideia=True)
b("En abril de mil novecientos cincuenta y tres, el director Allen Dulles aprueba un programa secreto: MK Ultra. Lo dirige un químico, Sidney Gottlieb.",
  f"dulles|{DULLES} signing a document at a desk with a green lamp@@ALLEN DULLES",
  f"gottlieb|{GOTTLIEB} holding a small glass vial up to the light in a 1950s laboratory@@SIDNEY GOTTLIEB",
  "mkultra_file|A thick brown file folder on a lab bench next to test tubes and a red stamp, no legible text@@MKULTRA", card="WASHINGTON, 1953")
b("MK Ultra prueba drogas, sobre todo LSD, en personas que muchas veces no saben nada.",
  "lsd_drop|A dropper releasing a single clear drop into a glass of liquid, close-up",
  "test_subject|A man in a 1950s hospital gown sitting on a bed in a white room, confused, a scientist taking notes behind a window")
b("En noviembre de ese año, Frank Olson, un bacteriólogo que trabaja para el ejército, bebe una copa con LSD sin saberlo. Nueve días después, cae por la ventana de un hotel de Nueva York.",
  f"olson|{OLSON} at a lakeside cabin table in November 1953 raising a small glass of liqueur among colleagues@@FRANK OLSON",
  "hotel_window|The facade of a tall 1950s New York hotel at night, one window on a high floor open with the curtain blowing out, no people@@NUEVA YORK, 28 DE NOVIEMBRE DE 1953")
b("Su familia tardará veintidós años en saber la verdad sobre la droga. Y nunca aceptará la versión del suicidio.",
  "olson_family|A widow and three small children in a 1950s suburban living room looking at a framed photograph, sad",
  "newspaper_1975|A 1975 man reading a newspaper at a kitchen table, shocked, the headline illegible")
b("En mil novecientos setenta y tres, el director de la CIA ordena destruir los archivos de MK Ultra. Pero miles de documentos, mal archivados, sobreviven.",
  "shredding|Boxes of documents being fed into an incinerator in a basement in 1973, flames",
  "misfiled_box|A forgotten cardboard box of financial records on the wrong shelf of a huge archive, a beam of light on it@@MILES DE DOCUMENTOS")

# ───────────────────────── 7. LA FOTO ─────────────────────────
cap("7. La Foto")
b("La Foto. La CIA no solo conspira. También mira. Su avión espía, el U dos, vuela tan alto que los soviéticos no pueden alcanzarlo.",
  "u2_sky|A black U-2 spy plane with very long thin wings flying above the clouds at the edge of space, dark blue sky@@AVIÓN ESPÍA U-2",
  "u2_camera|Inside the belly of a spy plane, a huge aerial camera with big lenses pointing down", ideia=True)
b("Hasta el primero de mayo de mil novecientos sesenta. Un misil derriba el avión del piloto Francis Gary Powers sobre la Unión Soviética. Powers sobrevive, y pasa casi dos años preso.",
  "u2_hit|A U-2 spy plane falling from a very high sky trailing a thin line of smoke above snowy Soviet plains, seen from far away",
  "powers_trial|A young American pilot in a plain suit standing in a Moscow courtroom in 1960, Soviet judges@@FRANCIS GARY POWERS", card="UNIÓN SOVIÉTICA, 1 DE MAYO DE 1960")
b("Pero el U dos sigue volando. El catorce de octubre de mil novecientos sesenta y dos, fotografía Cuba desde el aire.",
  "u2_cuba|A U-2 spy plane flying high over the green island of Cuba and the blue Caribbean sea",
  "film_reel|Rolls of aerial reconnaissance film being unloaded from a plane on a runway at dawn", card="CUBA, 14 DE OCTUBRE DE 1962")
b("En esas fotos, los analistas de la CIA encuentran rampas para misiles nucleares soviéticos.",
  "analysts_lightbox|CIA photo analysts in 1962 bent over a lightbox with magnifiers studying black and white aerial photographs",
  "missile_site|A black and white aerial reconnaissance photograph of a missile launch site in a Cuban field, long tents and trucks")
b("Durante trece días, el mundo está más cerca que nunca de una guerra nuclear. Esa vez, la inteligencia funcionó: Kennedy supo a tiempo lo que había en la isla.",
  f"kennedy_photos|{KENNEDY} looking at large aerial photographs on an easel in the White House cabinet room with advisers@@13 DÍAS",
  "navy_blockade|American navy destroyers on the open sea forming a blockade line in October 1962, grey sky")

# ───────────────────────── 8. LA BAHÍA ─────────────────────────
cap("8. La Bahía")
b("La Bahía. Un año y medio antes, la misma agencia había firmado su peor fracaso.",
  "bay_calm|A quiet Caribbean bay at dawn in Cuba with mangroves and a sandy beach, calm water, ominous", ideia=True)
b("El diecisiete de abril de mil novecientos sesenta y uno, unos mil cuatrocientos exiliados cubanos, entrenados y armados por la CIA, desembarcan en la Bahía de Cochinos. Quieren derrocar a Fidel Castro.",
  "exiles_training|Cuban exile volunteers training in a jungle camp in Guatemala in 1960 with an American instructor@@BRIGADA 2506",
  "landing_boats|Landing craft full of armed Cuban exiles approaching a beach at dawn, a burning ship in the background",
  f"castro_tank|{CASTRO} standing next to a tank at the Bay of Pigs in 1961, directing troops@@FIDEL CASTRO", card="BAHÍA DE COCHINOS, 17 DE ABRIL DE 1961")
b("El plan suponía que el pueblo cubano se levantaría. No lo hace. Y Kennedy no envía el apoyo aéreo que esperaban.",
  "empty_village|An empty Cuban village street in 1961, closed shutters, nobody coming out",
  f"kennedy_no|{KENNEDY} standing alone at a window of the Oval Office at night, his back turned, tense")
b("En tres días, más de cien invasores mueren. Casi mil doscientos caen prisioneros.",
  "prisoners_line|A long line of captured invaders with hands up walking under guard on a dusty Cuban road@@CASI 1.200 PRISIONEROS",
  "prisoners_trucks|Captured exiles seated in the back of military trucks guarded by Cuban militiamen")
b("Allen Dulles, el director que creyó en el plan, deja la CIA ese mismo año. A fines de mil novecientos sesenta y dos, Cuba libera a los prisioneros a cambio de alimentos y medicinas.",
  f"dulles_leaves|{DULLES} leaving an office building carrying a box of personal items, autumn 1961",
  "food_ship|A cargo ship being loaded with crates of baby food and medicine at a Florida port in December 1962@@ALIMENTOS Y MEDICINAS", ideia=True)

# ───────────────────────── 9. LOS PUROS ─────────────────────────
cap("9. Los Puros")
b("Los Puros. La CIA no se rinde con Castro. Ahora busca matarlo.",
  f"castro_cigar|{CASTRO} smoking a long cigar in Havana in 1960, smiling",
  "havana_1960|The Havana seafront Malecón in 1960 with classic American cars and waves splashing", card="LA HABANA, 1960-1965")
b("Un comité del Senado documentará después al menos ocho planes entre mil novecientos sesenta y mil novecientos sesenta y cinco. Entre ellos, una caja de puros envenenados y un traje de buceo contaminado con hongos.",
  "senate_report|A thick bound US Senate report on a wooden table under a lamp, a pen and glasses@@AL MENOS 8 PLANES",
  "cigar_box|An open wooden box of Cuban cigars on a lab bench, a gloved hand injecting one with a syringe",
  "diving_suit|A black rubber diving suit laid out on a laboratory table, a scientist with tweezers and a petri dish")
b("Para alguno de esos planes, la agencia pide ayuda a la Mafia, que había perdido sus casinos en La Habana.",
  "casino_havana|A glamorous 1950s Havana casino with roulette tables and men in white dinner jackets",
  "mafia_meeting|Three 1960s mobsters in sharkskin suits meeting a man in a grey suit at a Miami hotel bar, cigarette smoke@@LA MAFIA")
b("Ninguno funciona. Castro muere en dos mil dieciséis, de viejo, a los noventa años. Cuba asegura que sobrevivió a más de seiscientos intentos de asesinato.",
  "old_castro|A very old bearded man in a tracksuit sitting in a garden chair, frail, Cuban flag in the background",
  "havana_mourning|Crowds in Havana's Revolution Square in 2016 holding portraits, mourning@@MÁS DE 600 INTENTOS, SEGÚN CUBA")

# ───────────────────────── 10. LA ORDEN ─────────────────────────
cap("10. La Orden")
b("La Orden. Chile, mil novecientos setenta. El socialista Salvador Allende gana la elección presidencial.",
  "santiago_1970|Santiago de Chile in 1970, a crowded avenue with Andes mountains behind, election celebration",
  f"allende|{ALLENDE} waving to a cheering crowd from a balcony in 1970@@SALVADOR ALLENDE", card="SANTIAGO DE CHILE, 1970", ideia=True)
b("El quince de septiembre, el presidente Nixon recibe en la Casa Blanca al director de la CIA, Richard Helms. Las notas de Helms resumen la orden en una frase: hacer que la economía chilena grite.",
  f"nixon_helms|{NIXON} talking to {HELMS} in the Oval Office in 1970@@RICHARD HELMS",
  "helms_notes|Handwritten notes on a yellow legal pad with a pen on a desk, the handwriting illegible, close-up@@\"QUE LA ECONOMÍA GRITE\"")
b("Durante tres años, la CIA gasta millones de dólares en la oposición y en periódicos.",
  "chile_press|A Chilean newspaper printing press in 1972 running at full speed, stacks of papers",
  "empty_shelves|Empty shelves in a Chilean grocery store in 1972 with a long queue of women outside")
b("El once de septiembre de mil novecientos setenta y tres, los militares bombardean el palacio de La Moneda. Allende muere. Empieza la dictadura de Pinochet.",
  "moneda_smoke|The neoclassical La Moneda palace in Santiago with black smoke rising from its roof, jet fighters overhead, seen from a distance@@11 DE SEPTIEMBRE DE 1973",
  "junta_1973|Four Chilean generals in dark uniforms and sunglasses sitting at a table, 1973")
b("En el año dos mil, un informe oficial de Estados Unidos concluye que la CIA no instigó ese golpe. Pero sabía que se preparaba. Y, según el mismo informe, probablemente dio la impresión de aprobarlo.",
  "hinchey_report|A slim government report with a blue cover on a desk in the year 2000, reading glasses@@INFORME HINCHEY, 2000",
  "nod_shadow|The shadow of a man nodding on a wall behind a desk with a closed file, ambiguous")

# ───────────────────────── 11. LAS JOYAS ─────────────────────────
cap("11. Las Joyas")
b("Las Joyas. En diciembre de mil novecientos setenta y cuatro, el periodista Seymour Hersh revela en el diario The New York Times que la CIA espió a miles de ciudadanos estadounidenses.",
  "reporter_typing|A 1970s investigative reporter's hands typing on a typewriter in a busy newsroom at night, coffee and cigarettes",
  "nyt_presses|Newspapers rolling off huge printing presses at night in 1974, the front page illegible@@NEW YORK TIMES, 22/12/1974",
  "protesters_watched|A 1960s anti-war protest in an American city, a man in a parked car photographing the protesters secretly", ideia=True)
b("Era justo lo que su propia ley le prohibía.",
  "law_again|The old 1947 law document in a glass case, a crack across the glass")
b("Dentro de la agencia ya existía una lista de sus pecados: unas setecientas páginas que los propios agentes llamaban las joyas de la familia.",
  "jewels_box|A thick stack of typed pages tied with string inside an open jewelry box lined with red velvet@@\"LAS JOYAS DE LA FAMILIA\"",
  "cia_safe|A heavy steel safe being opened in a dark CIA office, a thick folder inside")
b("En mil novecientos setenta y cinco, el Senado abre la caja con el Comité Church. MK Ultra. Los planes contra Castro. Chile.",
  "church_hearing|A 1975 US Senate hearing room, senators at a long elevated table, photographers and microphones@@COMITÉ CHURCH, 1975",
  "dart_gun|A senator holding up a strange pistol at a hearing in 1975, flashbulbs going off")
b("Por primera vez, la CIA es investigada en público. Nacen comités permanentes para vigilarla. Y la agencia nunca vuelve a ser invisible.",
  "tv_hearing|A family in 1975 watching a Senate hearing on a color television",
  "langley_light|The CIA headquarters building at night lit by bright searchlights, as if exposed")

# ───────────────────────── 12. EL MISIL ─────────────────────────
cap("12. El Misil")
b("El Misil. En diciembre de mil novecientos setenta y nueve, la Unión Soviética invade Afganistán. En Washington, muchos ven la oportunidad de darle a Moscú su propio Vietnam.",
  "soviet_tanks_afg|A long column of Soviet tanks and trucks on a mountain road in Afghanistan in winter 1979, snow",
  "map_afghanistan|" + "Central Asia with Afghanistan in the center, the Soviet Union to the north, Iran to the west and Pakistan to the east, " + MAPA, ideia=True)
b("Con dinero estadounidense, y otro tanto de Arabia Saudita, la CIA arma a los guerrilleros afganos: los muyahidines.",
  "saudi_money|A desk in a luxurious Riyadh office with stacks of US dollars and a teapot, two men in robes and an American in a suit",
  f"mujahideen|{MUJ} on a rocky mountain ridge with rifles, valley below@@LOS MUYAHIDINES")
b("En mil novecientos ochenta y seis les entrega su arma más famosa: el misil Stinger, que se dispara desde el hombro y derriba helicópteros.",
  f"stinger|{MUJ} aiming a shoulder-launched missile tube at the sky from behind rocks@@MISIL STINGER",
  "helicopter_hit|A Soviet military helicopter trailing smoke over a distant Afghan mountain valley, seen from very far away", card="AFGANISTÁN, 1986")
b("En mil novecientos ochenta y nueve, los soviéticos se retiran. Para muchos, es la operación más exitosa de la historia de la agencia.",
  "soviet_withdraw|Soviet tanks crossing a bridge out of Afghanistan in February 1989, soldiers waving flags@@15 DE FEBRERO DE 1989",
  "cia_celebrate|CIA officers in a 1980s office raising glasses of champagne in front of a map, smiling")
b("Pero en Afganistán quedan armas, campos de entrenamiento y combatientes de todo el mundo islámico. Entre ellos, un saudí millonario. Se llama Osama bin Laden.",
  "abandoned_camp|An abandoned training camp in Afghan mountains with tents and stacks of old weapons, dusk",
  "binladen_silhouette|A tall thin bearded man in a turban and camouflage jacket seen from behind on a mountain ridge at dusk, silhouette, face not visible@@OSAMA BIN LADEN")

# ───────────────────────── 13. EL ERROR ─────────────────────────
cap("13. El Error")
b("El Error. El once de septiembre de dos mil uno, la red de Bin Laden derriba las Torres Gemelas.",
  "towers_smoke|Two tall beams of pale blue light rising into the night sky from lower Manhattan, a memorial of light seen from across the river, quiet and solemn@@NUEVA YORK, 11/09/2001",
  "dust_street|Rescue workers walking through grey dust in a Manhattan street, silhouettes, no injuries shown", ideia=True)
b("La comisión que investigó los atentados concluye que hubo señales. Pero nadie las conectó a tiempo.",
  "corkboard|A cork board covered with photos, maps and papers but with the red strings between them cut and hanging loose@@COMISIÓN DEL 11-S",
  "unread_memo|A memo with a red stamp lying unread under a pile of papers on a crowded desk, close-up")
b("Un año después llega el segundo gran error. La CIA respalda la tesis de que Irak tiene armas de destrucción masiva. En dos mil tres, Estados Unidos invade Irak.",
  "sat_photo|A grainy satellite photo of trucks near a desert building, analyst's red circles drawn on it",
  "baghdad_2003|American tanks entering Baghdad in 2003 under a hazy sky, palm trees")
b("Las armas nunca aparecen. En dos mil cuatro, un informe del Senado concluye que esas conclusiones no estaban respaldadas por la información disponible.",
  "empty_bunker|American soldiers with flashlights searching an empty concrete bunker in the Iraqi desert, nothing inside@@LAS ARMAS NUNCA APARECEN",
  "senate_2004|A Senate report from 2004 on a desk with a highlighted page, illegible text")
b("Una agencia nacida para que nadie sorprenda a Estados Unidos falló en las dos cosas que más importaban.",
  "langley_rain|The CIA headquarters building in Langley under heavy rain, grey sky, the flag wet")

# ───────────────────────── CIERRE: LA DISCULPA ─────────────────────────
cap("Cierre. La Disculpa")
b("Volvamos a la radio. Marzo de mil novecientos noventa y nueve. Un presidente de Estados Unidos, Bill Clinton, está en Ciudad de Guatemala.",
  "radio_dust#detalhe-centro",
  "gt_city_1999|Guatemala City in 1999 with modern buildings and volcanoes behind, motorcade on an avenue",
  "clinton_back|A tall grey-haired American president in a dark suit seen from behind at a podium in a Guatemalan palace hall, cameras in front@@BILL CLINTON", card="CIUDAD DE GUATEMALA, 10 DE MARZO DE 1999", ideia=True)
b("Frente a las cámaras, reconoce que apoyar a las fuerzas militares y de inteligencia que reprimieron a los guatemaltecos fue un error. Y que no debe repetirse.",
  "cameras_press|A row of 1999 television cameras and photographers at a press conference",
  "maya_women_listen|Guatemalan Maya women in traditional clothes listening to a speech on a small radio in a village, 1999@@\"FUE UN ERROR\"")
b("En dos mil once, el Estado de Guatemala le pide perdón a la familia de Jacobo Árbenz. Cincuenta y siete años después de la radio.",
  "apology_2011|A ceremony in a Guatemalan palace courtyard in 2011, an elderly man receiving a framed document, applause@@20 DE OCTUBRE DE 2011",
  "arbenz_photo|A faded black and white framed photograph of a 1950s president on a table with flowers")
b("La CIA cumple setenta y nueve años. Sigue en Langley, Virginia. Y casi todo lo que hace hoy seguirá en secreto durante décadas.",
  "langley_hq",
  "sealed_boxes|Rows of sealed archive boxes with red stamps disappearing into darkness@@LANGLEY, VIRGINIA")
b("Una radio derribó un gobierno. Hicieron falta cuarenta y cinco años para que alguien pidiera perdón.",
  "radio_dial#detalhe-centro", "radio_family#médio-dir", ideia=True)
b("Y tú, ¿qué crees que dirán algún día los archivos de hoy? Déjalo en los comentarios.",
  "files_desk", "cia_folder#aberto")

# a 1ª prova (04/11) saiu com moldura de papel: todo prompt leva sangria explícita
SANGRIA = ", full-bleed illustration filling the entire frame edge to edge, no border, no margin, no white frame, no panel outline"

THUMBS = [
    {"id": "thumb-A", "prompt": "A 1950s American intelligence agent in a fedora and trench coat in half body on the LEFT third of the frame, holding a brown case folder with a red circular stamp, the white modernist CIA headquarters building behind him; the RIGHT half of the image is plain empty pale sky, no signage, no lettering"},
    {"id": "thumb-B", "prompt": "A 1950s wooden tube radio glowing on a table at night on the LEFT third of the frame, a window behind it showing a volcano, the shadow of a man in a fedora on the wall; the RIGHT half of the image is a plain dark empty wall, no signage, no lettering"},
    {"id": "thumb-C", "prompt": "A 1950s American intelligence agent in a fedora seen in half body on the LEFT third, leaning over a desk with a large old paper map of the Americas, a lamp; the RIGHT half of the image is a plain empty dark wall, no signage, no lettering, no pins"},
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
