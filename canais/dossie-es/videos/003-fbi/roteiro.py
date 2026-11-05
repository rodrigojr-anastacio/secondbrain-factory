#!/usr/bin/env python3
"""Fonte única do dossie-es 003 (FBI): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (na pasta do vídeo). Conteúdo no topo; geração no fim (copiada do 002-mossad).

Molde da bíblia (canais/dossie-es/biblia/roteiro.md): hook por anedota (o arrombamento de Media, Pensilvânia, na noite de
Ali × Frazier, 1971; os concorrentes em en abrem com a morte de Hoover, Dillinger no Biograph ou o 11-S) → 13 expedientes-objeto
com título falado → pagamento da anedota no expediente 10 ("Las Maletas") → cierre que volta à cerradura (os ladrões nunca presos,
revelados em 2014) + aforismo + pergunta. Recorte 1908–2001, factual, atribuído; 1 frase neutra de contexto (11-S) no cierre.
Ângulo América Latina: o Servicio de Inteligencia Especial (1940–1946), as "carpetas" de Puerto Rico e o caso Camarena (1985).
Fatos conferidos em 05/11/2026 (ver SOURCES.md).

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (id I### na ordem de aparição) · "chave" reuso · "chave#enq" reuso com enquadramento
  + "@@TEXTO"      rótulo na tela (máquina de escrever; CAIXA ALTA, até ~28 caracteres)
Bloco: b(texto, *planos, card="WASHINGTON, 1908", ideia=True) · capítulo: cap("5. El Espejo")
Mapas (chave map_*): base sem texto nem pinos; pinos, setas e nomes no código (src/labels.jsx).
"""
import json, math, re
from pathlib import Path

WPS = 2.38           # palavras/s medidas no 001/002 (143 ppm com pausas; erro de 1% no 002)
BREAK, LONG = 0.35, 0.8
MAX_PLANO_INICIO = 3.0   # s por plano nos primeiros INICIO s (~20 cortes/min)
INICIO = 60.0
MAX_PLANO = 3.6      # s por plano depois (~17 cortes/min)
INEDITO_ATE = 180.0  # s: só imagens novas até aqui
JANELA = 60.0        # s: mesmo enquadramento da mesma imagem só depois disso
HOOK_MAX = 35.0      # s: a bíblia pede hook de 25–35 s (o 002 estourou com 40 s)
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "TODA la historia del FBI"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# Personagens (descrição visual fixa; rostos "resembling", nunca foto)
BONAPARTE = "a 1908 American attorney general in his late fifties with a bald head, a grey mustache and round spectacles, dark frock coat"
HOOVER_J = "a stocky young American official of about twenty-five with slicked-back dark hair, a round face with a square jaw and a stiff white collar, dark 1919 suit"
HOOVER = "a stocky American bureau director in his forties resembling J. Edgar Hoover, slicked-back dark hair, heavy jaw, stern eyes, dark double-breasted 1930s suit"
HOOVER_V = "a heavy-set elderly American official in his seventies resembling J. Edgar Hoover, grey hair combed back, heavy jowls, stern face, dark suit"
DILLINGER = "a 1934 American gangster in his early thirties with a thin mustache and dark hair, straw boater hat, white shirt"
SEBOLD = "a German-American man in his early forties with light hair combed back and a calm face, plain grey 1941 suit"
DUQUESNE = "a tall lean man in his sixties with a long face and grey hair, elegant dark 1941 suit"
MLK = "an African American minister in his mid thirties resembling Martin Luther King Jr., short hair, thin mustache, dark suit and tie"
CORETTA = "an elegant African American woman in her late thirties with short wavy dark hair, 1964 dress"
FELT = "a tall distinguished American official in his late fifties with silver hair combed back, grey 1972 suit"
CAMARENA = "a Mexican-American federal agent in his late thirties with dark hair and a thick dark mustache, open-collar shirt, 1985"
HANSSEN = "a tall gaunt American man in his fifties with dark hair, a pale serious face and a dark suit, 2001"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, borders and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame"

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Media, Pensilvania. Ocho de marzo de mil novecientos setenta y uno. Millones de personas siguen la pelea del siglo: Muhammad Ali contra Joe Frazier.",
  "media_town|A small quiet American town in Pennsylvania at night in March 1971, a main street with brick buildings, a few lit windows, old cars parked",
  "boxing_radio|A 1971 living room at night, a family gathered around a radio and a small television showing a boxing ring, excited faces",
  "boxing_ring|Two heavyweight boxers in a crowded 1971 boxing ring under bright lights, seen from far away, a huge cheering crowd",
  "radio_bar|A 1971 small-town bar at night, men crowded around a radio on the counter listening to a boxing fight, beer glasses", card="MEDIA, PENSILVANIA, 1971")
b("En el pueblo, ocho personas fuerzan la cerradura de una pequeña oficina vacía. Llenan maletas con todos los documentos que encuentran.",
  "lock_pick|Close-up of gloved hands forcing the lock of an office door with a crowbar at night, a flashlight beam",
  "dark_office|A small dark 1971 government office at night, filing cabinets, desks, a flashlight beam crossing the room",
  "suitcases|Open suitcases being filled with paper files by several hands in a dark office, flashlight light",
  "empty_drawers|Open empty metal filing cabinet drawers in a dark office at night, a few papers on the floor")
b("Desaparecen en la noche. Nunca los atraparán.",
  "car_leaves|A 1970s station wagon driving away down a dark small-town street at night, red tail lights, seen from behind")
b("[serious] La oficina era del FBI.",
  "fbi_door|A frosted glass office door in a 1971 building at night, a seal-shaped emblem painted on it without legible letters, a broken lock")
b("Esta es toda la historia del FBI. Y de los secretos que guardaba en esos archivos.",
  "files_desk|A long dark desk covered with open brown case files and black and white photographs, a red stamp and a magnifying glass",
  "red_stamp|A hand slamming a red rubber stamp onto a brown paper case file, ink splash, dramatic close-up",
  "washington_night|Washington at night seen from far away, the Capitol dome lit, the Potomac river, dark sky", ideia=True)

# ───────────────────────── 1. EL MEMORANDO ─────────────────────────
cap("1. El Memorando")
b("El Memorando. Washington, mil novecientos ocho. El Congreso le prohíbe al Departamento de Justicia usar agentes del Servicio Secreto. Muchos temen una policía secreta al estilo europeo.",
  "capitol_1908|The United States Capitol in Washington in 1908, horse carriages and early automobiles on the avenue, grey sky",
  "congress_1908|American congressmen in 1908 debating in a crowded wood-paneled chamber, one standing and pointing",
  "secret_service|Two men in bowler hats and dark 1908 coats walking out of a government building, folders under their arms",
  "senators_worry|Two 1908 American senators with white beards whispering in a marble corridor of the Capitol",
  "europe_police|A 1908 European secret policeman in a long coat watching a café from a street corner in the rain", card="WASHINGTON, 1908")
b("El fiscal general es Charles Bonaparte, sobrino nieto de Napoleón. Y decide crear su propia fuerza.",
  f"bonaparte|{BONAPARTE} sitting at a large desk in a wood-paneled office, writing with a fountain pen@@CHARLES BONAPARTE",
  "napoleon_portrait|An old oil portrait of Napoleon hanging in a dark wood-paneled American office, a desk lamp below",
  "justice_1908|The modest 1908 Department of Justice offices in Washington, clerks carrying stacks of folders up a staircase")
b("El veintiséis de julio firma un memorando. Reúne a treinta y cuatro agentes. La unidad todavía no tiene nombre.",
  "memo_1908|A typed 1908 memorandum on a desk with a fountain pen and a signature, no legible text@@26 DE JULIO DE 1908",
  "badge_1908|An old brass badge without any legible text lying on a dark desk next to a pocket watch, 1908",
  "agents_1908|A group of thirty men in 1908 suits and bowler hats standing in rows in a government hallway, serious faces@@34 AGENTES")
b("Al año siguiente los llaman Oficina de Investigación. Persiguen fraudes, quiebras bancarias y, desde mil novecientos diez, la trata de mujeres de un estado a otro.",
  "bureau_office|A modest 1909 office with a few desks, typewriters and men in shirtsleeves, a window onto Washington",
  "train_1910|A 1910 steam train arriving at an American station, a man in a bowler hat watching passengers",
  "mann_act|A 1910 railway platform at night, a federal agent in a bowler hat watching a nervous young woman with a suitcase",
  "bank_1910|A closed American bank in 1910 with a crowd of angry depositors outside, a policeman at the door")
b("En mil novecientos diecisiete entra al Departamento de Justicia un joven empleado, puntual y obsesivo con el orden. Se llama John Edgar Hoover.",
  f"hoover_young|{HOOVER_J} sitting at a tidy desk sorting index cards into perfect rows@@J. EDGAR HOOVER",
  "doj_1917|A 1917 Department of Justice hallway in Washington, a young clerk with slicked hair carrying a stack of files, older men in suits",
  "index_cards|Thousands of white index cards in long wooden drawers, a hand pulling one out, lamp light", ideia=True)

# ───────────────────────── 2. EL FICHERO ─────────────────────────
cap("2. El Fichero")
b("El Fichero. Mil novecientos diecinueve. Estallan bombas contra políticos y jueces en varias ciudades de Estados Unidos. Una explota frente a la casa del fiscal general, Mitchell Palmer.",
  "bomb_house|The damaged front of a brick townhouse in Washington in 1919 at night, broken windows, policemen with lanterns, seen from far away, no bodies",
  "newspaper_1919|A 1919 newspaper boy on a street corner holding up a newspaper with huge headlines made of unreadable shapes, a crowd",
  "bomb_city|A city street in 1919 at dawn with broken shop windows and smoke, police and onlookers, seen from far away, no bodies",
  "palmer|A 1919 American attorney general in his late forties with wavy hair and round glasses, standing grimly in front of his damaged house@@A. MITCHELL PALMER", card="WASHINGTON, 1919")
b("Palmer pone a Hoover, de veinticuatro años, al frente de una nueva división. Su tarea: vigilar a los radicales.",
  f"hoover_division|{HOOVER_J} standing in front of a wall of wooden filing drawers, arms crossed, proud",
  "radicals_meeting|A crowded 1919 workers' meeting in a smoky hall, a man speaking from a chair, red banners without letters",
  "surveil_1919|A 1919 man in a cap secretly listening at the back of a union hall, a notebook hidden in his newspaper")
b("Hoover copia el sistema de fichas de la Biblioteca del Congreso. En pocos meses tiene más de cien mil nombres.",
  "library_congress|The grand reading room of the Library of Congress in 1919 with its dome and card catalog cabinets",
  "card_typing|A 1919 woman typist filling in index cards with names on a typewriter, a stack of cards beside her",
  "fichero_wall|An enormous room full of wooden card-index cabinets from floor to ceiling, clerks pulling drawers, 1919@@150.000 NOMBRES")
b("El dos de enero de mil novecientos veinte, sus agentes hacen redadas en más de treinta ciudades. Detienen a miles de personas, muchas sin orden judicial. Semanas antes, cientos de extranjeros ya habían sido deportados, entre ellos la anarquista Emma Goldman.",
  "raids_1920|Federal agents in 1920 coats leading handcuffed men out of a tenement building at night in winter, snow, seen from far away@@2 DE ENERO DE 1920",
  "crowded_cell|A crowded 1920 jail hall full of detained immigrant men in coats, standing shoulder to shoulder, dim light",
  "deport_ship|An old steamship leaving New York harbor in winter 1919, people at the rails, grey sea@@EMMA GOLDMAN, DEPORTADA",
  "ellis_island|The Ellis Island immigration hall in 1920, detained immigrants with bundles waiting on benches, guards",
  "goldman|A determined woman in her fifties with round glasses and a dark 1919 dress standing at a ship's rail, defiant")
b("Jueces y abogados denuncian los abusos. Palmer cae en desgracia. Hoover no.",
  "lawyers_1920|A group of American lawyers in 1920 reading a thick printed report around a table, indignant",
  "palmer_fall|A 1920 American politician with round glasses alone in an empty office with packed boxes, defeated",
  "hoover_desk_1920|A stocky young American official with slicked-back dark hair working late alone at a desk covered with index cards, a single lamp, 1920", ideia=True)

# ───────────────────────── 3. EL DIRECTOR ─────────────────────────
cap("3. El Director")
b("El Director. En mil novecientos veinticuatro, la Oficina está desprestigiada. Se descubre que espió a senadores que investigaban la corrupción del gobierno.",
  "senate_1924|A 1924 United States Senate hearing room, senators at a long table, a witness at a microphone, journalists",
  "spy_window|A 1920s man in a hat secretly watching an office window from across a dark street, a notebook in his hand",
  "teapot_dome|A 1924 newspaper boy shouting on a Washington street, a crowd grabbing papers about a government oil scandal, headlines of unreadable shapes", card="WASHINGTON, 1924")
b("El nuevo fiscal general, Harlan Stone, busca a alguien que la limpie. El diez de mayo elige a Hoover. Tiene veintinueve años.",
  "hoover_door|A frosted glass office door with a painted title made of unreadable shapes, a young man with slicked hair opening it, 1924",
  "stone|A 1924 American attorney general in his early fifties, tall, broad-shouldered, with thinning hair, shaking hands across a desk@@HARLAN STONE",
  f"hoover_sworn|{HOOVER_J.replace('about twenty-five', 'twenty-nine')} standing straight in a 1924 office as an older man hands him a document@@10 DE MAYO DE 1924")
b("Despide a los agentes corruptos. Exige títulos de abogado o de contador, traje oscuro y camisa blanca. Y crea un archivo nacional de huellas dactilares.",
  "fired_agent|A 1924 agent in a rumpled suit leaving an office with a cardboard box, others watching",
  "fingerprints|A fingerprint card with ten inked fingerprints under a magnifying glass on a desk, 1920s",
  "fingerprint_hall|A huge 1920s hall where dozens of clerks in white shirts compare fingerprint cards at long tables")
b("Lo nombran de forma interina. Se quedará cuarenta y ocho años.",
  "agents_suits|A row of young 1925 federal agents in identical dark suits and white shirts standing at attention in a hallway",
  "calendar_pages|Old calendar pages flying in the wind over a dark desk with a nameplate, time passing", ideia=True)

# ───────────────────────── 4. EL CINE ─────────────────────────
cap("4. El Cine")
b("El Cine. En los años treinta, la Gran Depresión llena el país de asaltantes de bancos. El más famoso es John Dillinger.",
  "depression_bank|A 1933 small-town American bank with a crowd outside, men with hats, an old car speeding away, dust",
  f"dillinger|{DILLINGER} leaning on a 1930s black car, a confident smile@@JOHN DILLINGER",
  "wanted_poster|A 1934 wanted poster on a wooden wall with a photograph of a man with a thin mustache, no legible text", card="CHICAGO, 1934")
b("Chicago, veintidós de julio de mil novecientos treinta y cuatro. Dillinger sale del cine Biograph con dos mujeres. Una de ellas lo delató. Es Anna Sage, una inmigrante rumana que teme ser deportada. Para que los agentes la reconozcan, viste de naranja. Los periódicos la llamarán la mujer de rojo.",
  "biograph|A 1934 Chicago movie theater at night with a glowing marquee without letters, a crowd leaving after the show",
  "woman_orange|A woman in an orange dress walking out of a movie theater at night in 1934, nervous glance over her shoulder@@22 DE JULIO DE 1934",
  "ana_sage|A woman in her forties in a 1934 dress secretly talking with a federal agent in a parked car at night@@ANNA SAGE",
  "red_headline|A 1934 newspaper with a large photograph of a woman and a huge headline of unreadable shapes, on a café table")
b("Los agentes lo esperan en la calle. Intenta huir. Lo matan en el callejón.",
  "agents_street|Men in 1934 suits and fedoras waiting in the shadows of a Chicago street at night, one lighting a cigarette",
  "alley|A dark Chicago alley at night in 1934, a fallen straw boater hat on the cobblestones, policemen at the end, seen from far away, no body")
b("Ese año, el Congreso autoriza a los agentes a portar armas y hacer arrestos. En mil novecientos treinta y cinco, la Oficina recibe su nombre definitivo: Oficina Federal de Investigación. F, B, I.",
  "gun_badge|A 1934 revolver and a federal badge without legible text on a wooden desk, a lamp",
  "fbi_building|A neoclassical government building in Washington in 1935, men in fedoras walking up the steps",
  "gmen_comic|A 1930s newsstand full of pulp comic magazines showing heroic agents with guns, colorful covers without legible text@@F.B.I., 1935")
b("Hoover convierte a sus agentes en héroes de radio, cine e historietas. Y los prepara para otra guerra.",
  f"hoover_radio|{HOOVER} speaking into a 1930s radio microphone in a studio, confident",
  "radio_family|A 1930s family listening to a large wooden radio in their living room at night, the children amazed", ideia=True)

# ───────────────────────── 5. EL ESPEJO ─────────────────────────
cap("5. El Espejo")
b("El Espejo. Nueva York, mil novecientos cuarenta y uno. William Sebold es un alemán nacionalizado estadounidense. Los nazis lo reclutaron como espía.",
  "times_square_41|Times Square in New York in 1941, crowds, yellow cabs and lit billboards without legible letters, early evening",
  f"sebold|{SEBOLD} sitting alone in a modest New York office, waiting@@WILLIAM SEBOLD", card="NUEVA YORK, 1941")
b("Pero Sebold se lo contó todo al FBI. Ahora trabaja para los dos lados.",
  "double_agent|A man in a grey 1941 suit shaking hands with two different men in a dim hallway, one on each side of him",
  "shortwave|A hidden shortwave radio transmitter in a 1941 country house attic, a man with headphones tapping a key")
b("Recibe a los espías nazis en una oficina cerca de Times Square. Detrás de un espejo, el FBI los filma. El jefe de la red, Fritz Duquesne, lleva cuarenta años espiando a los británicos.",
  f"mirror_office|{SEBOLD} talking with {DUQUESNE} across a desk in a small 1941 office, a large wall mirror behind them",
  "behind_mirror|An FBI agent behind a two-way mirror filming a meeting in the next room with a 1940s movie camera, headphones on@@DETRÁS DEL ESPEJO",
  "film_reel|A 1941 film reel and a spool of audio wire on a table in a dark room, a lamp",
  f"duquesne|{DUQUESNE} smoking a cigarette by a window in a New York apartment, a cold smile@@FRITZ DUQUESNE")
b("En junio, el FBI detiene a treinta y tres espías de la red. Todos son condenados. Según el FBI, es la mayor red de espionaje desmantelada en la historia de Estados Unidos.",
  "arrests_41|FBI agents in 1941 fedoras escorting a handcuffed man out of a New York apartment building, seen from far away",
  "courtroom_41|A crowded 1941 New York courtroom, a long row of defendants on benches, a judge@@33 CONDENADOS")
b("Seis meses después, Estados Unidos entra en la guerra. Y Hoover ya tiene agentes donde nadie los espera: en América Latina.",
  "pearl_newspaper|A man reading a newspaper with a huge black headline made of unreadable shapes on a New York street in December 1941",
  "map_latam|" + "Mexico, Central America and South America from above, the whole of Latin America fully visible, the Caribbean in the upper middle, " + MAPA, ideia=True)

# ───────────────────────── 6. EL SERVICIO ─────────────────────────
cap("6. El Servicio")
b("El Servicio. En junio de mil novecientos cuarenta, el presidente Roosevelt le encarga al FBI el espionaje en América Latina. Nace el Servicio de Inteligencia Especial.",
  "roosevelt|A 1940 American president resembling Franklin Roosevelt, with pince-nez glasses and a cigarette holder, signing a paper at his desk@@FRANKLIN D. ROOSEVELT",
  f"hoover_map|{HOOVER} pointing at a large map of the Americas on his office wall, two agents listening", card="WASHINGTON, 1940")
b("Cientos de agentes viajan al sur disfrazados de vendedores, periodistas y empresarios.",
  "agent_ship|A man in a white 1940s linen suit with a suitcase walking down a ship gangway in a tropical port, palm trees",
  "rio_1942|Rio de Janeiro in 1942, the bay and Sugarloaf mountain, Art Deco buildings, an agent in a hat on the promenade",
  "buenos_aires_42|Buenos Aires in 1942, a wide avenue with trams and old cars, a man in a raincoat reading a newspaper at a café")
b("Buscan radios clandestinas, contrabando de materiales de guerra y redes alemanas en México, Brasil, Argentina y Chile.",
  "radio_hunt|Two men in 1940s hats with a portable radio direction finder on a rooftop of a Latin American city at night",
  "port_contraband|Dockworkers unloading crates in a South American port in 1942, an agent in a hat secretly taking notes",
  "mexico_42|A busy street in Mexico City in 1942, colonial buildings, a man in a suit watching from a doorway")
b("Según el propio FBI, identifican a más de ochocientos espías del Eje.",
  "spy_files|A row of brown case files with small photographs of men clipped to them on a desk, a red stamp@@887 ESPÍAS DEL EJE",
  "radio_seized|Policemen in 1940s uniforms carrying a seized radio transmitter out of a house in a Latin American city")
b("Cuando termina la guerra, Hoover quiere hacer espionaje en todo el mundo. No lo consigue. En mil novecientos cuarenta y siete, ese trabajo pasa a una agencia nueva: la CIA.",
  f"hoover_angry|{HOOVER} standing behind his desk with a furious face, a document in his fist",
  "cia_folder|A brown case file with a red circular stamp being handed from one man's hand to another's across a desk@@1947: LA CIA", ideia=True)

b("Si te gustan estos expedientes, suscríbete. Y ahora, la reunión que el FBI no vio venir.",
  "folder_stack|A tall stack of brown case files with red stamps on a desk, the top one slightly open, mysterious light inside")

# ───────────────────────── 7. LA REUNIÓN ─────────────────────────
cap("7. La Reunión")
b("La Reunión. Durante años, Hoover repite que en Estados Unidos no existe una mafia organizada.",
  f"hoover_press|{HOOVER_V.replace('in his seventies', 'in his early sixties')} speaking firmly to reporters in his office, 1950s",
  "mob_restaurant|A smoky 1950s Italian restaurant in New York, men in expensive suits whispering at a corner table", card="APALACHIN, 1957")
b("Apalachin, Nueva York, catorce de noviembre de mil novecientos cincuenta y siete. Un policía estatal ve demasiados autos de lujo en la casa de campo de un empresario.",
  "apalachin_house|A large country stone house on a wooded hill in upstate New York in November 1957, many shiny black luxury cars parked outside@@14 DE NOVIEMBRE DE 1957",
  "trooper|A 1957 New York state trooper in a grey uniform and campaign hat looking at parked luxury cars with suspicion")
b("Bloquean el camino. Los invitados huyen por el bosque con trajes caros.",
  "roadblock|A 1957 police roadblock on a country road, state troopers stopping a black Cadillac",
  "woods_run|Men in expensive suits and fedoras running through bare autumn woods, seen from far away")
b("Detienen a más de cincuenta jefes de la mafia de todo el país. Casi todos dicen lo mismo: vinieron a visitar a un amigo enfermo. El FBI no sabía nada.",
  "mob_lineup|A row of men in expensive 1957 suits standing in a small police station, sullen faces, a policeman taking notes",
  "headline_57|A 1957 newspaper on a desk with a huge headline made of unreadable shapes and a photo of a country house")
b("Hoover reacciona rápido. Crea un programa contra los grandes capos y empieza a usar micrófonos ocultos.",
  "microphone|A tiny hidden microphone under a restaurant table, wires running down the leg, 1950s",
  "wiretap|Two FBI agents with headphones listening to a reel-to-reel tape recorder in a dark apartment, 1960s")
b("En mil novecientos sesenta y tres, el mafioso Joseph Valachi declara ante el Senado, en televisión. Le da un nombre: la Cosa Nostra. Pero el FBI ya tiene en la mira a otro enemigo.",
  "valachi|A 1963 Senate hearing with TV cameras, a gray-haired mobster at the witness table with a microphone@@JOSEPH VALACHI",
  "tv_1963|A 1963 family watching a black and white television showing a Senate hearing", ideia=True)

# ───────────────────────── 8. EL PROGRAMA ─────────────────────────
cap("8. El Programa")
b("El Programa. En mil novecientos cincuenta y seis, el FBI lanza en secreto el COINTELPRO, un programa de contrainteligencia.",
  "secret_memo|A typed 1956 memorandum stamped in red on a dark desk, a fountain pen, no legible text@@COINTELPRO, 1956",
  f"hoover_old_desk|{HOOVER_V.replace('in his seventies', 'in his early sixties')} reading a secret memo at his desk under a lamp, a flag in the corner", card="WASHINGTON, 1956")
b("Según una comisión del Senado, su objetivo no era investigar delitos. Era infiltrar, desacreditar y desarticular grupos políticos.",
  "infiltrator|A man in a 1960s jacket sitting in the back row of a crowded political meeting, secretly taking notes",
  "forged_letter|A hand typing an anonymous letter on a typewriter at night, a stack of envelopes")
b("Primero, el Partido Comunista. Después, el movimiento por los derechos civiles, los opositores a la guerra de Vietnam y las Panteras Negras.",
  "civil_rights_march|A large peaceful 1963 civil rights march in Washington, crowds with signs without legible letters, seen from far away",
  "antiwar|A 1960s anti-war protest on a university campus, students with signs without letters, police in the background",
  "panthers|Young men and women in black berets and leather jackets standing in a row on a 1968 city street")
b("En Puerto Rico, persigue al movimiento independentista. En el año dos mil, ante el Congreso, el director del FBI, Louis Freeh, hablará de acciones ilegales graves, tal vez criminales, en la isla.",
  "san_juan|Old San Juan in Puerto Rico in the 1960s, colorful colonial houses, blue cobblestones, the sea@@SAN JUAN, PUERTO RICO",
  "carpetas|Shelves full of thick old paper dossiers tied with string in a dusty archive room@@LAS \"CARPETAS\"",
  "freeh|An American FBI director in his fifties with short dark hair and glasses testifying at a congressional hearing table in 2000@@LOUIS FREEH, 2000")
b("Y uno de los hombres más vigilados por el FBI es un pastor de Atlanta.",
  "atlanta_church|A brick Baptist church in Atlanta in 1964 with a white steeple, people in Sunday clothes on the steps", ideia=True)

# ───────────────────────── 9. LA CARTA ─────────────────────────
cap("9. La Carta")
b("La Carta. Con permiso del fiscal general Robert Kennedy, el FBI intercepta los teléfonos de Martin Luther King. Por su cuenta, pone micrófonos en sus hoteles.",
  f"mlk|{MLK} speaking from a church pulpit, raised hand, intense@@MARTIN LUTHER KING JR.",
  "hotel_bug|An FBI technician hiding a microphone behind a hotel room lamp, 1964",
  "phone_tap|A 1960s telephone junction box with alligator clips and wires, a man's hand with a screwdriver", card="ATLANTA, 1964")
b("En noviembre de mil novecientos sesenta y cuatro, King gana el Premio Nobel de la Paz. Ese mes le envían un paquete anónimo. Semanas después, lo abre su esposa, Coretta.",
  "nobel|A 1964 newspaper photo of a minister receiving a medal on a stage in Oslo, a crowd applauding, no legible text",
  f"coretta|{CORETTA} opening a brown cardboard package at a kitchen table, curious@@CORETTA SCOTT KING",
  "package|A brown cardboard package with a reel of audio tape and a typed letter inside, on a table")
b("Hay una cinta con grabaciones de su vida privada. Y una carta.",
  "tape_reel|A reel of audio tape on a wooden table under a lamp, close-up, ominous",
  "letter_typed|A typed anonymous letter on a table under a lamp, no legible text")
b("Dice, entre otras cosas: Solo te queda una cosa por hacer. Tú sabes cuál es.",
  "letter_close|Close-up of the bottom of a typed letter with no signature, unreadable typewriter text, a red pencil mark@@\"TÚ SABES CUÁL ES\"")
b("King la lee como una invitación al suicidio. Y sospecha del FBI. En mil novecientos setenta y cinco, la comisión Church del Senado confirma que la carta salió del propio FBI.",
  f"mlk_worry|{MLK} reading a letter alone in a dim office, his head in his hand",
  "church_committee|A 1975 United States Senate committee hearing, senators at a long table, a large stack of documents@@COMISIÓN CHURCH, 1975")
b("Pero en mil novecientos sesenta y cuatro nadie fuera del FBI sabe que estos programas existen. Hasta la noche de la pelea.",
  "boxing_ring#detalhe-centro", ideia=True)

# ───────────────────────── 10. LAS MALETAS ─────────────────────────
cap("10. Las Maletas")
b("Las Maletas. Los ocho de Media son pacifistas contra la guerra de Vietnam. Pasan días leyendo los papeles en una granja. Según un análisis publicado después, solo uno de cada cien documentos trata del crimen organizado. Cuatro de cada diez tratan de vigilancia política.",
  "farmhouse|An old farmhouse in rural Pennsylvania at night in 1971, a single light in the window, snow on the fields",
  "reading_files|Several young people in 1971 clothes sitting on the floor of a farmhouse room, reading piles of documents by lamplight",
  "sorting_piles|Documents sorted into piles on a farmhouse floor, one huge pile and one tiny pile, a hand placing a sheet, lamp light@@1% CRIMEN ORGANIZADO", card="PENSILVANIA, 1971")
b("Se llaman a sí mismos la Comisión Ciudadana para Investigar al FBI. Mandan copias a periódicos y a congresistas.",
  "envelopes_mail|A pile of brown envelopes addressed by hand being dropped into a blue mailbox at night, no legible text",
  "post_newsroom|A 1971 newspaper newsroom, an editor reading photocopied documents at his desk, journalists around him")
b("El fiscal general pide que no se publiquen. El Washington Post los publica.",
  "attorney_phone|A 1971 American official on a telephone in his office, angry, a city at night through the window",
  "printing_press|A huge rotary printing press running at night, newspapers flowing out with large headlines made of unreadable shapes@@24 DE MARZO DE 1971")
b("Un memorando pide a los agentes entrevistar a los activistas para aumentar la paranoia. Que crean que hay un agente del FBI detrás de cada buzón.",
  "mailbox|A lonely blue mailbox on a street corner at night, a man in a coat watching it from the shadows@@\"DETRÁS DE CADA BUZÓN\"",
  "paranoia|A young activist in 1971 looking nervously out of a window through the blinds at night")
b("En otro papel aparece una palabra que nadie conocía: COINTELPRO. Hoover cierra el programa en abril. Pero el secreto ya se escapó: un periodista demanda al FBI y obtiene los documentos.",
  "routing_slip|A small typed routing slip on a desk with one word circled in red, unreadable typewriter text, magnifying glass",
  "journalist_court|A 1973 journalist in a suit walking out of a courthouse holding a thick stack of documents, triumphant",
  f"hoover_old_desk#médio-dir")
b("Un año después, Hoover muere. Y empieza una carrera por sus archivos.",
  "flag_half|An American flag at half-mast in front of a government building in Washington in May 1972, grey sky", ideia=True)

# ───────────────────────── 11. EL GARAJE ─────────────────────────
cap("11. El Garaje")
b("El Garaje. Dos de mayo de mil novecientos setenta y dos. Hoover muere a los setenta y siete años. Su secretaria durante cincuenta y cuatro años, Helen Gandy, destruye sus archivos personales.",
  f"hoover_dead|An empty large office with a dark desk, a leather chair and an American flag, morning light, a pair of reading glasses on the desk@@2 DE MAYO DE 1972",
  "shredder|An elderly secretary in a 1972 dress feeding papers into a paper shredder in a dim office, boxes of files around her@@HELEN GANDY", card="WASHINGTON, 1972")
b("Seis semanas después, cinco hombres son detenidos dentro del edificio Watergate.",
  "watergate|The curving modern Watergate building in Washington at night in 1972, a few lit windows, a police car outside",
  "burglars_72|Five men in suits with rubber gloves being arrested by police in a dark office at night in 1972, flashlights")
b("El número dos del FBI, Mark Felt, se reúne de madrugada con un reportero del Washington Post en un estacionamiento subterráneo.",
  f"felt|{FELT} standing in a dark underground parking garage at night, lit by a single fluorescent light@@MARK FELT",
  "garage|A young reporter with longish hair in a 1972 trench coat waiting in an empty underground parking garage at 2 a.m., concrete pillars")
b("Le confirma pistas que llegan hasta la Casa Blanca. En mil novecientos setenta y cuatro, el presidente Nixon renuncia. La identidad de Felt se sabrá en dos mil cinco, treinta y tres años después.",
  "white_house|The White House at night in 1974, a single lit window, rain",
  "helicopter_74|A presidential helicopter lifting off from the White House lawn in August 1974, seen from far away@@AGOSTO DE 1974")
b("Un año después, la comisión Church revela décadas de abusos. Desde entonces, un director del FBI solo puede quedarse diez años.",
  "church_committee#médio-dir",
  "files_stack|Huge stacks of declassified documents on a long table in a hearing room, a senator reading one@@MÁXIMO: 10 AÑOS")
b("En los años ochenta, el FBI recibe una misión nueva: las drogas. Y una de sus pruebas más importantes sale de una casa en México.",
  "map_mexico|" + "Mexico and the southern United States from above, the whole of Mexico fully visible with the Pacific coast and the Gulf of Mexico, " + MAPA, ideia=True)

# ───────────────────────── 12. LA CASA ─────────────────────────
cap("12. La Casa")
b("La Casa. Guadalajara, siete de febrero de mil novecientos ochenta y cinco. Enrique Camarena, agente de la DEA, sale del consulado de Estados Unidos para comer con su esposa.",
  "guadalajara|The historic center of Guadalajara in 1985, the cathedral with its yellow twin spires, a busy street, old cars",
  f"camarena|{CAMARENA} walking out of a consulate building in Guadalajara in the afternoon@@ENRIQUE \"KIKI\" CAMARENA", card="GUADALAJARA, 7 DE FEBRERO DE 1985")
b("Unos hombres lo suben a un auto. Desaparece.",
  "kidnap_car|A 1980s car door slamming shut on a sunny street in Guadalajara, men in sunglasses, seen from far away")
b("Un mes después, su cuerpo aparece en un rancho de Michoacán. Lo habían torturado.",
  "rancho|A remote ranch in the hills of Michoacán in 1985, dry fields, a dirt road, police vehicles seen from far away, no bodies",
  "camarena_photo|A framed photograph of a smiling man with a thick mustache on a table with flowers and a candle")
b("El FBI manda un equipo forense. Su experto en cabellos y fibras vincula el crimen con una casa de Guadalajara, en la calle Lope de Vega. Según los fiscales, allí interrogaron a Camarena.",
  "forensic_team|American forensic experts in 1985 with cases and evidence bags arriving at a walled house in Guadalajara, Mexican police at the gate",
  "microscope|A 1980s FBI laboratory, a technician looking through a comparison microscope at hairs and fibers, evidence envelopes@@LABORATORIO DEL FBI",
  "lope_de_vega|A walled house with a heavy metal gate on a residential street in Guadalajara in 1985, bougainvillea over the wall@@CALLE LOPE DE VEGA")
b("En México, el narcotraficante Rafael Caro Quintero es condenado por el crimen. En Estados Unidos, el testimonio del experto es clave en tres juicios. En mil novecientos noventa y siete, el inspector general del Departamento de Justicia critica con dureza el laboratorio del FBI.",
  "mexico_court|A 1989 Mexican courtroom, a defendant in a dark shirt behind bars, lawyers and journalists@@RAFAEL CARO QUINTERO",
  "trial_la|A 1988 federal courtroom in Los Angeles, a forensic expert testifying next to an enlarged photograph of fibers",
  "ig_report|A thick government report with a plain cover on a desk, a hand turning the pages, critical notes in red pencil@@INFORME DE 1997")
b("Pero el peor enemigo del FBI no estaba en México. Estaba adentro.",
  "fbi_corridor|A long empty corridor inside a federal office building at night, a single man walking away at the end", ideia=True)

# ───────────────────────── 13. EL PARQUE ─────────────────────────
cap("13. El Parque")
b("El Parque. Vienna, Virginia, dieciocho de febrero de dos mil uno. Un agente veterano del FBI deja un paquete bajo una pasarela de madera, en un parque.",
  "foxstone|A small wooden footbridge over a creek in a wooded suburban park in Virginia in winter at dusk, bare trees",
  f"hanssen_bridge|{HANSSEN} in a dark overcoat crouching under a wooden footbridge, hiding a package wrapped in a plastic bag@@ROBERT HANSSEN", card="VIENNA, VIRGINIA, 2001")
b("Se llama Robert Hanssen. Trabaja en contrainteligencia: su oficio es cazar espías soviéticos.",
  f"hanssen_office|{HANSSEN} working at a desk with a computer and stacks of classified folders in a 1990s office",
  "kgb_files|Old Soviet-style case files with red covers and a small photograph clipped to one, on a dark desk")
b("Pero desde mil novecientos setenta y nueve vende secretos a Moscú: primero a la inteligencia militar soviética, después a la KGB y, por último, a Rusia. Recibe más de un millón cuatrocientos mil dólares en efectivo, diamantes y depósitos en Moscú.",
  "cash_diamonds|A bundle of hundred dollar bills and a small pouch of loose diamonds on a dark table under a lamp@@1,4 MILLONES DE DÓLARES",
  "moscow_night|The Kremlin towers in Moscow at night under snow, red stars lit")
b("Durante veintidós años, los rusos ni siquiera saben su nombre. Firma sus cartas con un alias: Ramón García. El FBI tampoco sabe quién es.",
  "anonymous_letter|An envelope with no name on it and a typed letter in a dark car at night, a gloved hand",
  "mole_hunt|FBI agents in the 1990s around a table covered with photos of suspects, one photo face down")
b("Lo descubren gracias a un exagente ruso. Según la prensa, el FBI le compra el expediente del topo por siete millones de dólares. Dentro hay una bolsa de plástico con sus huellas.",
  "mole_file|A thick Soviet-style dossier with a red cover lying next to a plain plastic garbage bag in an evidence envelope, a magnifying glass@@EL EXPEDIENTE DEL TOPO",
  "arrest_park|FBI agents in raid jackets without legible letters surrounding a man in an overcoat in a wooded park at dusk, seen from far away")
b("Siete meses después de su arresto, los atentados del once de septiembre cambian la misión del FBI: ya no basta con perseguir delitos, hay que prevenir ataques. Hanssen recibe cadena perpetua. Y aquí se cierra este expediente.",
  "prison_cell|A small bare concrete prison cell with a narrow bed and a high window, cold light",
  "memorial_lights|Two vertical beams of white light rising into the night sky over the New York skyline, seen from far away",
  "folder_close|A hand closing a thick brown case file with a red circular stamp on a dark desk, lamp light", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. La Cerradura")
b("La Cerradura. El FBI pone a cientos de agentes a buscar a los ladrones de Media. Cinco años después, el caso prescribe. Ni un solo arresto.",
  "lock_pick#detalhe-centro",
  "agents_search|FBI agents in 1971 suits knocking on the door of a suburban house, a woman answering cautiously",
  "case_closed|A brown case file stamped in red lying in an archive box, the box lid closing, dust@@CASO CERRADO, 1976")
b("En dos mil catorce, varios de ellos cuentan su historia por primera vez. Ya tienen canas.",
  "old_burglars|Three elderly people with grey hair sitting on a porch looking at an old black and white photograph of young people, warm light")
b("El FBI pasó medio siglo abriendo los archivos de los demás. Lo que lo cambió fue que alguien abriera los suyos.",
  "fichero_wall#detalhe-centro", "suitcases#médio-dir", "files_desk#detalhe-alto", ideia=True)
b("Y tú, ¿qué expediente del FBI crees que sigue cerrado? Déjalo en los comentarios. Y si quieres saber qué hizo la CIA en América Latina, su expediente completo está aquí.",
  "folder_stack#médio-esq", "cia_folder#aberto")

# a 1ª prova do 001 (04/11) saiu com moldura de papel: todo prompt leva sangria explícita
SANGRIA = ", full-bleed illustration filling the entire frame edge to edge, no border, no margin, no white frame, no panel outline"

THUMBS = [
    {"id": "thumb-A", "prompt": f"{HOOVER} in half body on the LEFT third of the frame, holding a thick brown case folder with a red circular stamp against his chest, stern stare at the viewer, behind him a neoclassical Washington government building with columns at dusk; the RIGHT half of the image is plain empty pale evening sky, no signage, no lettering"},
    {"id": "thumb-B", "prompt": "A burglar in a dark 1971 coat and gloves seen in half body on the LEFT third of the frame, holding a flashlight and an open suitcase overflowing with paper files, inside a dark government office with filing cabinets, dramatic flashlight beam; the RIGHT half of the image is plain dark empty wall in shadow, no signage, no lettering"},
    {"id": "thumb-C", "prompt": f"{HOOVER_V} in half body on the LEFT third of the frame, pulling an index card out of a huge wall of wooden card-index drawers, suspicious eyes looking at the viewer, warm lamp light; the RIGHT half of the image is plain dark empty background, no signage, no lettering"},
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
