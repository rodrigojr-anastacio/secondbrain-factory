#!/usr/bin/env python3
"""Fonte única do dossie-es 007 (Las SS): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (na pasta do vídeo). Conteúdo no topo; geração no fim (copiada do 006-masones).

Molde da bíblia (canais/dossie-es/biblia/roteiro.md): hook por anedota (a morte de "Wolfgang Gerhard" em Bertioga, 1979,
que era Josef Mengele; o Archive abre com os anéis de caveira e usa o "criador de galinhas" como capítulo, por isso o
granjeiro da pauta virou o expediente 1) → 14 expedientes-objeto com título falado → pagamento da anedota no expediente 9
("La Rampa", logo após o CTA) e no 13 ("El Pasaporte") → cierre "La Tumba" que volta à cova de Embu + aforismo + pergunta.
Tom de dossiê frio, factual, sem glorificar; vítimas nomeadas pelo número documentado; nada gráfico.
Imagens: nenhuma suástica, runa, caveira ou insígnia (uniformes "without any insignia"); violência só "seen from far away,
no bodies, no blood"; campos só como arquitetura vazia ou de longe.
Ângulo América Latina: Mengele (Argentina, Paraguai, Brasil), Eichmann (liga com o 002 Mossad), Rauff no Chile, Barbie na
Bolívia, Priebke em Bariloche. Sessão: Gestapo (expediente 5), KGB/Mossad (cierre).
Fatos conferidos em 13/11/2026 (ver SOURCES.md).

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (id I### na ordem de aparição) · "chave" reuso · "chave#enq" reuso com enquadramento
  + "@@TEXTO"      rótulo na tela (máquina de escrever; CAIXA ALTA, até ~28 caracteres)
Bloco: b(texto, *planos, card="BERTIOGA, 1979", ideia=True) · capítulo: cap("5. El Organigrama")
Mapas (chave map_*): base sem texto nem pinos; pinos, setas e nomes no código (src/labels.jsx).
"""
import json, math, re
from pathlib import Path

WPS = 2.38           # palavras/s medidas no 001–006 (erro de 1–3%)
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
TITULO = "TODA la historia de las SS"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# Uniformes sempre sem insígnia (YouTube/anúncios e biblia/visual.md: nada de runas, suástica, caveira)
NOI = "without any insignia, badges, runes, skulls, armbands, medals or emblems, a completely plain chest and collar"
NEGRO = f"a plain black 1930s uniform {NOI}"
GRIS = f"a plain field-grey uniform {NOI}"
NOSYM = ", no swastikas, no runes, no skulls, no flags, no insignia, no symbols"
SEM = ", no lettering anywhere"   # objetos com capa, placa ou papel: o nano-banana inventa texto
VIOL = ", seen from far away, no bodies, no blood"
# Personagens (descrição visual fixa; rostos "resembling", nunca foto)
MENGELE_OLD = "a frail elderly man in his late sixties with thinning grey hair, a grey mustache and a tired face, a short-sleeved shirt, 1979"
MENGELE = f"a German doctor in his early thirties resembling Josef Mengele, dark slicked-back hair, a small gap between his front teeth, a long white doctor's coat buttoned over a dark shirt and tie, white gloves, 1943"
HIMMLER = f"a slim German man in his late twenties resembling Heinrich Himmler, round rimless glasses, a small mustache, short hair shaved at the sides, a weak chin, {NEGRO}"
HIMMLER45 = "a tired German man in his forties with round rimless glasses, clean-shaven, a black patch over his left eye, a worn civilian coat, 1945"
ROHM = "a stocky German man in his mid forties resembling Ernst Röhm, a round fleshy face with dueling scars, short hair, a plain brown shirt without insignia, 1934"
EICKE = f"a heavy-set German officer in his early forties with a fleshy face, a hard cold stare, {NEGRO}"
HEYDRICH = f"a tall German officer with thick short slicked-back blond hair, bareheaded, in his thirties resembling Reinhard Heydrich, a long narrow face, a high forehead, close-set eyes, a plain dark grey uniform {NOI}, plain sleeves without any patch or cuff band"
EICHMANN = f"a thin German officer in his mid thirties resembling Adolf Eichmann, a long nose, thin lips, receding dark hair, a plain dark civilian suit and tie, 1942"
JAGER = "a German man in his fifties with a stern lined face and short grey hair, a plain dark grey civilian jacket and tie, sitting at a desk, 1941"
PRIEBKE = "an elderly German man of eighty with white hair, large glasses and a grey sweater, standing on a snowy street in a Patagonian mountain town, 1994, no flags anywhere, no badges or pins on the sweater"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, borders and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame"

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Bertioga, Brasil, siete de febrero de mil novecientos setenta y nueve. Un anciano se mete al mar, sufre un derrame cerebral y se ahoga.",
  "bertioga|A wide tropical beach on the coast of São Paulo in 1979, green hills behind, a few beach houses, hot afternoon light, calm waves",
  f"old_man_sea|{MENGELE_OLD} walking alone into the sea on a tropical beach, seen from behind, afternoon",
  "waves|Close-up of waves breaking on a tropical beach, an empty straw hat floating on the foam, afternoon light",
  "beach_crowd|A small group of people on a tropical beach in 1979 pulling a man out of the water, seen from far away, no face visible", card="BERTIOGA, 1979")
b("Lo entierran en Embu con el nombre de Wolfgang Gerhard. Seis años después, la policía abre la tumba.",
  "embu_cemetery|A small hillside cemetery in a Brazilian town in 1979, simple white graves, a few mourners, overcast",
  "grave_plain|Close-up of a simple grey tombstone in a Brazilian cemetery with a blank plaque, wilted flowers" + SEM,
  "exhumation|Brazilian policemen and forensic workers digging up a grave in a hillside cemetery in 1985, a crowd of photographers with ordinary human faces behind a rope, seen from far away, blank tombstones without inscriptions, no lettering anywhere")
b("Los huesos son de Josef Mengele, médico de las SS en Auschwitz.",
  "skull_table|A forensic table under a bright lamp with an old skull and bones laid out, a measuring ruler, gloved hands, clinical light",
  f"mengele_face|{MENGELE} in portrait, a cold half smile, a dark background@@JOSEF MENGELE")
b("Esta es TODA la historia de las SS. Una escolta de doscientos ochenta hombres por la que pasó cerca de un millón.",
  "files_desk|A long dark desk covered with open brown case files and old black-and-white photographs, a red stamp and a magnifying glass, lamp light" + SEM,
  "red_stamp|A hand slamming a red rubber stamp onto a brown paper case file, ink splash, dramatic close-up" + SEM,
  "black_ranks|Rows of men in plain black uniforms standing at attention in a vast square at dusk, seen from far away, long shadows" + NOSYM,
  "boots_march|Close-up of black leather boots marching in step on cobblestones, low angle, grey light" + NOSYM, ideia=True)

# ───────────────────────── 1. EL GRANJERO ─────────────────────────
cap("1. El Granjero")
b("El Granjero. Múnich, mil novecientos veinticinco. El partido nazi crea una pequeña escolta para proteger a Hitler en sus mítines. La llama Schutzstaffel, escuadra de protección. Las SS.",
  "munich_1925|Munich in 1925, a crowded beer hall at night full of smoke, men at long wooden tables, seen from the back of the room" + NOSYM,
  "guards_door|Two men in plain dark caps and dark shirts guarding the door of a Munich beer hall at night, lantern light" + NOSYM,
  "rally_back|A small political meeting in a smoky hall in 1925, a speaker on a stage seen from far behind the crowd, his face not visible" + NOSYM,
  "guards_few|A handful of young men in plain black caps posing stiffly in a Munich courtyard in 1925, old photograph style" + NOSYM, card="MÚNICH, 1925")
b("Son unas decenas de hombres, a la sombra de las SA, la enorme milicia de camisas pardas.",
  "sa_crowd|A huge crowd of men in plain brown shirts marching through a German street in 1929, seen from above, no flags" + NOSYM,
  "black_vs_brown|A few men in plain black uniforms standing apart from a large group of men in brown shirts in a courtyard, 1929" + NOSYM,
  "brown_hall|A crowded meeting hall filled with men in plain brown shirts, a few men in black caps standing guard along the walls, 1928" + NOSYM)
b("En enero de mil novecientos veintinueve, la escolta recibe un nuevo jefe: Heinrich Himmler, de veintiocho años.",
  f"himmler_young|{HIMMLER} in portrait, an office with filing cabinets behind him, cold lamp light@@HEINRICH HIMMLER",
  "himmler_appointed|A thin young man with round rimless glasses receiving a folder from an older party official across a desk in a smoky office, 1929" + SEM,
  "office_1929|A small cramped party office in Munich in 1929, a desk piled with papers and index cards, a typewriter" + SEM, card="MÚNICH, 1929")
b("Estudió agronomía y tuvo una granja de gallinas que fracasó. Es miope, meticuloso y obsesionado con los registros.",
  "chicken_farm|A small poultry farm in Bavaria in the late 1920s, wooden henhouses, chickens in a muddy yard, a grey sky",
  f"himmler_farm|{HIMMLER.replace(NEGRO, 'a plain grey civilian suit')} feeding chickens in a muddy yard, a serious face",
  "ledger|Close-up of a thin man's hands writing tiny numbers in a ledger with a fountain pen, round glasses lying on the page" + SEM)
b("Hereda unos doscientos ochenta hombres. A finales de mil novecientos treinta y dos ya son más de cincuenta mil.",
  "few_men|About twenty men in plain black uniforms standing in a small Bavarian courtyard, seen from above, 1929" + NOSYM,
  "many_men|Thousands of men in plain black uniforms filling a huge stadium field in 1932, seen from far away from the stands" + NOSYM,
  "recruits_line|A long queue of young men in civilian suits waiting outside an office door on a German street in 1932, seen from far away, no flags, no banners" + SEM + NOSYM)
b("Para elegirlos, Himmler no mira solo el físico. Mira el árbol genealógico.",
  "family_tree|An old hand-drawn family tree on yellowed paper spread on a desk, a magnifying glass over it, the names unreadable" + SEM,
  "glasses_tree|Close-up of round rimless glasses resting on an old hand-drawn family tree document, lamp light" + SEM, ideia=True)

# ───────────────────────── 2. EL CERTIFICADO ─────────────────────────
cap("2. El Certificado")
b("El Certificado. Para entrar en las SS hay que probar una supuesta ascendencia aria hasta el año mil ochocientos. Los oficiales, hasta mil setecientos cincuenta.",
  "certificates|A stack of old church baptism certificates and marriage records on a desk in a 1930s office, a rubber stamp beside them" + SEM,
  "church_register|A village priest opening a huge leather parish register for a young man in a dark suit in a dim sacristy, 1934",
  "genealogy_clerk|A clerk in a 1930s office copying dates from an old parish book onto a blank form, a stack of files beside him" + SEM)
b("El candidato reúne actas de bautismo y registros de parroquia. Hasta la estatura cuenta.",
  "measure|A young blond man in a white shirt being measured against a height scale in a bare 1930s office, an official writing",
  "photo_profile|A 1930s office photographer with a large box camera photographing a young man in profile against a plain wall")
b("En diciembre de mil novecientos treinta y uno, Himmler da otra orden. Ningún miembro puede casarse sin permiso. La novia también tiene que probar su árbol genealógico.",
  "couple|A young German couple in 1930s clothes sitting nervously across a desk from an official in a plain black uniform who reads their papers" + NOSYM,
  "bride_papers|Close-up of a woman's hands handing over a folder of documents across a desk, a wedding ring box beside it" + SEM,
  "wedding_34|A small German civil wedding in 1934, a bride in a simple white dress and a groom in a plain black uniform signing a register" + NOSYM + SEM,
  "approval_letter|Close-up of a typed letter with an ink stamp being slid into an envelope, lamp light" + SEM)
b("Una oficina de las SS, la de Raza y Asentamiento, revisa cada expediente.",
  "race_office|A long 1930s office with rows of clerks at desks and tall filing cabinets, folders stacked everywhere, cold light" + SEM,
  "stamp_file|A clerk stamping an approval on a file in a 1930s office, a pile of folders on his left" + SEM)
b("Es una teoría racial sin ninguna base científica. Sobre esa mentira se forma la orden. Y en mil novecientos treinta y cuatro, recibe su primera orden de matar.",
  "fake_science|A chart of human head shapes drawn in ink pinned to a wall in a dim 1930s classroom, a pointer resting below it, no text" + SEM,
  "lecture_race|A 1930s lecture hall with young men in plain black uniforms listening to a professor at a blackboard, faces in shadow" + NOSYM + SEM,
  "torch_hall|Young men in plain black uniforms standing in silence in a torchlit stone hall at night, seen from behind" + NOSYM,
  "elite_line|A line of young men in plain black uniforms standing at attention in a dark hall, faces in shadow" + NOSYM, ideia=True)

# ───────────────────────── 3. LOS CUCHILLOS ─────────────────────────
cap("3. Los Cuchillos")
b("Los Cuchillos. Junio de mil novecientos treinta y cuatro. Las SA tienen ya millones de miembros. Su jefe, Ernst Röhm, quiere convertirlas en el nuevo ejército de Alemania.",
  f"rohm|{ROHM} in portrait, a confident smirk, a smoky room behind him@@ERNST RÖHM",
  "sa_parade|Endless columns of men in plain brown shirts marching across a field in 1934, seen from far away" + NOSYM,
  f"rohm_speech|{ROHM} standing in the back of an open car with both hands gripping the windshield, speaking to a crowd of men in brown shirts, nobody raising an arm" + NOSYM,
  "army_officers|German army officers in grey uniforms watching a brown-shirt parade with cold faces, 1934" + NOSYM, card="ALEMANIA, 1934")
b("El ejército y los grandes empresarios desconfían de él. Hitler decide.",
  "generals_34|Bareheaded older German generals without caps, in plain grey tunics with plain collars, talking quietly around a table in a dark office, 1934" + NOSYM,
  "phone_34|Close-up of a black 1930s telephone being picked up in a dark office at night")
b("Al amanecer del treinta de junio, Hitler llega en persona a un hotel de Bad Wiessee, donde descansa Röhm. Lo detiene en su habitación.",
  "hotel_lake|A Bavarian lakeside hotel at dawn in 1934, mountains behind, black cars arriving in front, mist on the lake",
  "hotel_corridor|Armed men in plain dark uniforms walking fast down a hotel corridor at dawn, seen from behind" + NOSYM,
  "rohm_bed|A hotel room at dawn, a heavy man in pajamas sitting up in bed as men in dark coats burst through the door, seen from the doorway", card="BAD WIESSEE, 1934")
b("En tres días, hombres de las SS y de la Gestapo asesinan a decenas de jefes de las SA y a viejos rivales de Hitler. Hay al menos ochenta y cinco muertos documentados.",
  "night_cars|Black cars racing through a German city at night in 1934, headlights on wet cobblestones",
  "arrest_night|Men in dark coats dragging a man out of a house at night" + VIOL,
  "list_names|Close-up of a typed list of names with some lines crossed out in red pencil, on a desk under a lamp, the names unreadable" + SEM,
  "barracks_yard|An empty brick barracks courtyard at dawn in Berlin with a bare wall, a thin haze, no people")
b("A Röhm le dejan una pistola en la celda para que se mate. Se niega. Lo matan dos oficiales de las SS. Uno de ellos es Theodor Eicke.",
  "cell_pistol|A bare prison cell with a single pistol on a small table under a barred window, cold light",
  "stadelheim|A grim stone prison building in Munich at dusk in 1934, high walls and barred windows",
  "cell_door|Two officers in plain black uniforms standing in front of a prison cell door in a stone corridor, seen from behind" + NOSYM,
  f"eicke|{EICKE} in portrait, a prison corridor behind him@@THEODOR EICKE")
b("Tres semanas después, Hitler premia a las SS: dejan de depender de las SA. Y Eicke recibe su recompensa: la inspección de todos los campos de concentración.",
  "black_ranks2|A massive formation of men in plain black uniforms on a parade ground in 1934, seen from high above" + NOSYM,
  "camp_gate_far|A wooden watchtower and barbed wire fence of a 1930s camp seen from far away across a grey field, empty, no people", ideia=True)

# ───────────────────────── 4. EL REGLAMENTO ─────────────────────────
cap("4. El Reglamento")
b("El Reglamento. Dachau, cerca de Múnich, marzo de mil novecientos treinta y tres. Himmler, jefe de la policía de Múnich, anuncia a la prensa un campo de concentración. Dice que es para presos políticos.",
  "dachau_factory|A disused brick factory with tall chimneys near a small Bavarian town in 1933, a new barbed wire fence around it, grey sky",
  "press_33|Journalists in 1930s suits and hats taking notes in a Munich police office as an official reads a statement" + NOSYM, card="DACHAU, 1933")
b("Los primeros presos son comunistas, socialdemócratas y sindicalistas. Después llegarán judíos, romaníes, homosexuales y testigos de Jehová.",
  "prisoners_truck|An open truck carrying men in civilian clothes through a gate at dusk in 1933, seen from far away, faces not visible",
  "barracks_empty|Rows of empty wooden prison barracks in a camp at dawn, mud and puddles, mist, no people")
b("En octubre, Eicke escribe un reglamento. Fija los castigos: palizas, celdas de aislamiento y pena de muerte para quien proteste o intente huir.",
  "rules_paper|A typed rulebook of several pages on a desk with a fountain pen and a rubber stamp, harsh lamp light" + SEM,
  f"eicke_desk|{EICKE} writing at a desk in a bare office at night, a lamp lighting his face")
b("Dachau se convierte en el modelo. Sus guardias, las unidades Calavera, se entrenan ahí y luego dirigen los demás campos.",
  "guard_tower|A wooden guard tower with a searchlight over a barbed wire fence at night, a guard in a plain dark uniform seen from far away" + NOSYM,
  "guards_train|Young guards in plain dark uniforms being lectured in a bare camp courtyard by an officer, seen from behind" + NOSYM)
b("Entre esos guardias está un hombre que años después será comandante de Auschwitz: Rudolf Höss.",
  f"hoss|A bareheaded German guard in his early thirties with a narrow plain face and short dark hair, no cap, {NEGRO}, standing by a barbed wire fence@@RUDOLF HÖSS")
b("Pero para vigilar a un país entero, los campos no alcanzan. Hace falta la policía.",
  "berlin_street_36|A Berlin street in 1936 at night, a police car parked under a street lamp, people hurrying past" + NOSYM, ideia=True)

# ───────────────────────── 5. EL ORGANIGRAMA ─────────────────────────
cap("5. El Organigrama")
b("El Organigrama. Berlín, diecisiete de junio de mil novecientos treinta y seis. Hitler nombra a Himmler jefe de toda la policía alemana.",
  "berlin_hq|A massive grey stone government building on a Berlin street in 1936, black cars in front, overcast, no flags" + NOSYM,
  f"himmler_police|{HIMMLER} standing behind a large desk in a grand office, two police officers standing at attention before him with their arms straight down at their sides, seen from the side, nobody saluting, no raised arms" + NOSYM, card="BERLÍN, 1936")
b("Su hombre clave es Reinhard Heydrich, expulsado de la marina por romper una promesa de matrimonio. Dirige el SD, el servicio de inteligencia de las SS.",
  f"heydrich|{HEYDRICH} in portrait, a cold stare, a dark office behind him@@REINHARD HEYDRICH",
  "navy_ship|A German navy cruiser in a grey harbor in 1930, sailors on deck, seen from far away" + NOSYM,
  "sd_files|An intelligence office in 1937 with men reading reports under green lamps, cabinets full of folders" + SEM)
b("En septiembre de mil novecientos treinta y nueve, todo se une en una sola oficina: la Oficina Central de Seguridad del Reich.",
  "org_chart|An ink-drawn organizational chart of boxes connected by lines on a large sheet pinned to a wall, all boxes blank" + SEM,
  "rsha_hall|A long grey corridor of a Berlin government building in 1939 with men in suits carrying folders" + NOSYM, card="BERLÍN, 1939")
b("Bajo ese techo están la Gestapo, la policía criminal y el SD. Un mismo jefe para espiar, detener y mandar a un campo sin juicio.",
  "gestapo_desk|A Gestapo officer in a dark suit interrogating a nervous civilian across a desk in a bare office, a lamp between them",
  "card_index|Endless wooden drawers of index cards in a dim archive, a clerk filing a card" + SEM,
  "night_arrest|Two men in long leather coats knocking on an apartment door at night, a frightened woman opening it, seen from the stairwell")
b("La Gestapo merece su propio expediente. Lo que importa aquí es el organigrama. Y en la cima están las SS.",
  "org_top|Close-up of the top box of an ink-drawn organizational chart lit by a single lamp, all boxes blank, red pencil circle around it" + SEM,
  "stamp_red2|A heavy red stamp pressed on a brown folder on a dark desk, lamp light" + SEM)
b("Pero años antes, Himmler ya había buscado otra cosa para su orden: un castillo.",
  "castle_far|A triangular hilltop castle with three towers above a forest in Westphalia at dusk, seen from far away", ideia=True)

# ───────────────────────── 6. EL CASTILLO ─────────────────────────
cap("6. El Castillo")
b("El Castillo. Wewelsburg, Westfalia, mil novecientos treinta y cuatro. Himmler alquila un castillo triangular del siglo diecisiete por un marco al año.",
  "castle_close|A triangular 17th century castle with round towers on a hill above a German village in 1934, morning mist",
  f"himmler_castle|{HIMMLER} walking through the courtyard of an old castle with architects holding rolled plans" + NOSYM, card="WEWELSBURG, 1934")
b("Quiere convertirlo en un centro para la cúpula de la orden: una escuela de oficiales, con salas de ceremonias y una cripta.",
  "crypt|A round stone crypt with a domed ceiling and a sunken circular floor, lit by a single shaft of light, empty, no symbols",
  "hall_pillars|A grand round hall with stone pillars inside an old castle tower, cold light from tall windows, empty, no symbols on the floor")
b("Para las obras usa presos de un campo construido al lado. Mueren más de mil doscientos.",
  "camp_castle|Prisoners in striped clothes carrying stones up a hill towards a castle, guards with rifles watching" + VIOL,
  "stones|Close-up of rough stone blocks and a broken wheelbarrow in the mud at a construction site, rain")
b("Himmler también funda la Ahnenerbe, un instituto que busca pruebas de un supuesto pasado ario glorioso. Llega a mandar una expedición al Tíbet.",
  "ahnenerbe|A 1930s research office full of old books, maps, skulls in glass cases and ancient pottery, scholars in suits" + SEM,
  "tibet|A small caravan of European explorers in 1938 with horses crossing a high Himalayan pass, snow peaks behind")
b("Esa misma ciencia falsa, unos años después, servirá para justificar el asesinato en masa.",
  "glasses_book|A pair of round rimless glasses lying on a closed old book on a dark desk, cold light", ideia=True)

# ───────────────────────── 7. EL INFORME ─────────────────────────
cap("7. El Informe")
b("El Informe. Septiembre de mil novecientos treinta y nueve. Alemania invade Polonia. Detrás del ejército entran grupos especiales de las SS y la policía: los Einsatzgruppen.",
  "poland_39|German army columns of trucks and horse carts crossing a Polish plain in September 1939, smoke on the horizon, seen from far away" + NOSYM,
  "einsatz_trucks|Open trucks with men in plain grey uniforms driving into a Polish village behind the army, dust" + NOSYM, card="POLONIA, 1939")
b("Su misión: asesinar a maestros, sacerdotes, nobles y políticos. A cualquiera que pueda dirigir una resistencia.",
  "teachers|A group of Polish civilians in coats, a priest among them, lined up in a town square under guard" + VIOL,
  "school_empty|An empty Polish village classroom in 1939, a chalkboard wiped clean, an overturned chair")
b("En junio de mil novecientos cuarenta y uno, Alemania invade la Unión Soviética. Los Einsatzgruppen avanzan detrás del ejército. Ahora asesinan a los judíos: hombres, mujeres y niños.",
  "east_front|A vast Soviet wheat field in June 1941 with columns of trucks on a dirt road, smoke far away, seen from above" + NOSYM,
  "shtetl|A small Jewish village street in Ukraine in 1941, wooden houses, empty and silent, a door left open")
b("En el barranco de Babi Yar, cerca de Kiev, asesinan a treinta y tres mil setecientos setenta y un judíos en dos días de septiembre. Ellos mismos anotan la cifra.",
  "babi_yar|A deep grassy ravine on the edge of a city under a grey September sky, abandoned suitcases and coats on the edge, no people, no bodies",
  "suitcases|Close-up of a pile of abandoned leather suitcases and shoes in the grass, grey light, no people", card="KIEV, 1941")
b("El primero de diciembre, el coronel de las SS Karl Jäger firma un informe para sus jefes. Es una tabla: fecha, lugar, asesinados. Su comando, sobre todo en Lituania, suma ciento treinta y siete mil trescientas cuarenta y seis personas.",
  f"jager|{JAGER}, signing a typed document@@KARL JÄGER",
  "table_doc|Close-up of a closed thick grey binder tied with string on a cold office desk next to a fountain pen and a rubber stamp, frost on the window behind" + SEM,
  "typewriter_41|An old typewriter in a cold office in 1941 with a sheet half typed, frost on the window, the text unreadable" + SEM, card="KAUNAS, 1941")
b("Hasta mil novecientos cuarenta y tres, los Einsatzgruppen asesinan a más de un millón de personas. Pero en Berlín ya planean matar a una escala mayor.",
  "east_snow|A frozen empty field in the Soviet Union in winter, a line of bare trees, a grey sky, no people",
  "berlin_lake|A grand villa on the shore of a lake near Berlin in winter, bare trees, snow on the lawn, black cars arriving", ideia=True)

# ───────────────────────── 8. LA VILLA ─────────────────────────
cap("8. La Villa")
b("La Villa. Wannsee, a orillas de un lago de Berlín, veinte de enero de mil novecientos cuarenta y dos. Heydrich preside una reunión de quince participantes.",
  "villa_room|An elegant dining room in a lakeside villa in 1942 with a long table, men in suits and uniforms seated around it, winter light from tall windows" + NOSYM,
  f"heydrich_table|{HEYDRICH} at the head of a long polished table, papers in front of him" + NOSYM, card="WANNSEE, 1942")
b("Dura unos noventa minutos. El tema: coordinar la llamada solución final, el asesinato de los judíos de Europa.",
  "cognac|Close-up of cognac glasses and an ashtray on a polished table next to typed papers, men's sleeves, winter light" + SEM,
  "europe_map_table|A large blank map of Europe spread on a polished table with men's hands pointing at it" + SEM)
b("El acta la escribe un oficial de las SS, Adolf Eichmann. Enumera once millones de judíos. De treinta copias, solo una sobrevive a la guerra.",
  f"eichmann|{EICHMANN} writing notes at the corner of a long table@@ADOLF EICHMANN",
  "protocol|Close-up of a thin stapled typed document on a desk with a red stamp in the corner, the text unreadable" + SEM)
b("Cuatro meses después, en Praga, dos paracaidistas checoslovacos atacan el automóvil de Heydrich con una granada. Muere días después, el cuatro de junio.",
  "prague_curve|A tram curve on a Prague street in 1942, an open black car slowing down, smoke from an explosion behind it" + VIOL,
  "paratroopers|Two young men in civilian coats hiding behind a tram stop in Prague, tense faces, morning", card="PRAGA, 1942")
b("La maquinaria que Heydrich coordinó siguió funcionando sin él.",
  "rail_tracks|Railway tracks running into the fog across a flat winter plain, no people", ideia=True)
b("Si te gustan estos expedientes, suscríbete. Volvemos a Josef Mengele.",
  "red_stamp#detalhe-centro", "bertioga#médio-dir")

# ───────────────────────── 9. LA RAMPA ─────────────────────────
cap("9. La Rampa")
b("La Rampa. Auschwitz-Birkenau, Polonia ocupada, mayo de mil novecientos cuarenta y tres. Llega un nuevo médico de las SS: Josef Mengele, de treinta y dos años.",
  "birkenau|A long brick gatehouse with a railway line running through its arch across a flat winter plain, a watchtower, grey sky, empty, no people",
  f"mengele_arrive|{MENGELE} stepping off a train onto an empty platform with a small plain brown suitcase, a dark civilian overcoat over his white coat, seen from the side, no flags", card="AUSCHWITZ, 1943")
b("Las SS administran el campo. Los trenes llegan a una rampa. Ahí, los médicos de las SS hacen la selección. A un lado, el trabajo forzado. Al otro, las cámaras de gas.",
  "ramp|A railway ramp at night under floodlights, a freight train stopped, a crowd of people in coats seen from far away, faces not visible",
  "gloved_hand|Close-up of a white-gloved hand pointing left, the sleeve of a plain grey uniform, floodlit night, out-of-focus crowd behind" + NOSYM)
b("Mengele selecciona a gemelos, casi todos niños, para experimentos criminales y sin valor científico.",
  "twins|Two small twin children in plain clothes holding hands, seen from behind in a bare corridor, cold light, no faces",
  "lab_cold|A cold bare medical room in 1944 with a metal table, glass jars and instruments, no people")
b("En Auschwitz, las SS asesinan a cerca de un millón cien mil personas. Casi un millón son judíos.",
  "shoes_pile|A huge pile of old worn shoes in a dim room, grey light, no people",
  "barracks_snow|Rows of brick barracks in snow seen from far away, a line of watchtowers, no people")
b("Por allí pasaron unos ocho mil miembros de las SS. Después de la guerra, solo unos ochocientos fueron juzgados.",
  "guards_far|A group of men in plain grey uniforms walking along a barbed wire fence seen from far away, backs to the camera" + NOSYM,
  "court_few|A nearly empty courtroom with only a few defendants in suits on a long bench, 1947")
b("En enero de mil novecientos cuarenta y cinco, con los soviéticos cerca, Mengele se va del campo. Se lleva sus notas.",
  "notes_case|A man's gloved hands packing notebooks into a leather suitcase in a dark office at night, snow at the window" + SEM,
  "snow_road|A lone figure in a long coat walking away on a snowy road at dawn, seen from behind", ideia=True)

# ───────────────────────── 10. EL PUEBLO ─────────────────────────
cap("10. El Pueblo")
b("El Pueblo. Las SS también tienen su propio ejército: las Waffen-SS. Nacen de la guardia personal de Hitler. En total pasan por ellas unos novecientos mil hombres, muchos de ellos extranjeros.",
  "waffen|Soldiers in plain field-grey uniforms and helmets marching along a muddy road in 1943, seen from far away" + NOSYM,
  "tanks_far|A column of tanks crossing a snowy plain in 1943, seen from far away, no markings" + NOSYM)
b("Oradour-sur-Glane, Francia, diez de junio de mil novecientos cuarenta y cuatro. Cuatro días después del desembarco de Normandía, llega una compañía de la división Das Reich.",
  "oradour_day|A quiet French village street on a sunny June day in 1944, stone houses, a tram line, a church tower",
  "trucks_village|Military trucks with soldiers in plain field-grey uniforms entering a French village square, villagers watching from doorways" + NOSYM, card="ORADOUR, 1944")
b("Reúnen a los habitantes. Encierran a los hombres en graneros. A las mujeres y a los niños, en la iglesia.",
  "square_gather|Villagers gathered in a French village square in 1944 surrounded by soldiers" + VIOL,
  "church_doors|The closed wooden doors of a small French village church, soldiers standing in front, seen from far away" + NOSYM)
b("Matan a más de seiscientas cuarenta personas. Después queman el pueblo.",
  "oradour_smoke|A French village burning, black smoke rising over the roofs and the church tower" + VIOL)
b("Francia decidió no reconstruirlo. Las ruinas siguen ahí, como las dejaron.",
  "ruins|The roofless stone ruins of a French village street today, a rusted car and a sewing machine in an empty house, green grass",
  "ruins_church|The ruined roofless stone church of a French village under a quiet sky today, ivy on the walls")
b("En abril de mil novecientos cuarenta y cinco, el hombre que dirigió todo esto prepara su salida.",
  "glasses_book#detalhe-centro", ideia=True)

# ───────────────────────── 11. EL PARCHE ─────────────────────────
cap("11. El Parche")
b("El Parche. Abril de mil novecientos cuarenta y cinco. Con Berlín rodeado, Himmler negocia a espaldas de Hitler con un diplomático sueco, el conde Folke Bernadotte. Ofrece rendirse a los aliados occidentales.",
  "lubeck_night|A dim consulate room in Lübeck at night in April 1945, candles because of a blackout, two men talking across a table",
  "bernadotte|A tall Swedish aristocrat in his late forties with thinning hair and a long face, a grey suit and a Red Cross armband, 1945@@FOLKE BERNADOTTE", card="LÜBECK, 1945")
b("Cuando Hitler se entera, lo destituye de todos sus cargos y ordena detenerlo. Dos días después, se suicida.",
  "bunker|A cramped concrete bunker corridor lit by bare bulbs, papers on the floor, empty",
  "radio_45|An old military radio receiver in a bunker room, a hand turning the dial, dim light")
b("Himmler se afeita el bigote, se pone un parche en el ojo y usa los papeles falsos de un sargento: Heinrich Hitzinger.",
  "razor|Close-up of a straight razor and a small mirror on a sink in a farmhouse, dim light",
  f"himmler_patch|{HIMMLER45} in portrait, a nervous face, a grey sky behind him@@HEINRICH HITZINGER",
  "fake_papers|Close-up of a worn military pay book and identity papers in a man's hand, the text unreadable" + SEM)
b("En mayo, un control británico cerca de Bremervörde lo detiene. No saben quién es.",
  "checkpoint|A British army checkpoint on a muddy country road in northern Germany in May 1945, soldiers checking papers of refugees",
  "refugees|Columns of German refugees and soldiers in civilian coats walking on a road in May 1945, carts, seen from far away" + NOSYM, card="BREMERVÖRDE, 1945")
b("Ya en un campo británico, se quita el parche y dice su nombre. Lo llevan a Lüneburg. El veintitrés de mayo, en el examen médico, muerde una cápsula de cianuro.",
  "patch_off|A man taking off a black eye patch in front of British officers in a bare interrogation room, seen from behind",
  "capsule|Close-up of a tiny glass capsule between two fingers of a man in a plain grey civilian coat with plain sleeves, dark background" + NOSYM,
  "doctor_45|A British army doctor kneeling next to a man lying on the floor of a bare room" + VIOL, card="LÜNEBURG, 1945")
b("Himmler no llega a un juicio. Pero su organización sí se sentará en el banquillo.",
  "empty_dock|An empty wooden defendants' bench in a large courtroom with wood paneling, morning light", ideia=True)

# ───────────────────────── 12. LA SENTENCIA ─────────────────────────
cap("12. La Sentencia")
b("La Sentencia. Núremberg, primero de octubre de mil novecientos cuarenta y seis. El Tribunal Militar Internacional lee su veredicto.",
  "nuremberg|The Nuremberg courtroom in 1946, judges at a long bench under bright lights, defendants in two rows with headphones, seen from the gallery" + NOSYM,
  "judges|Four judges in black robes at a high bench reading a verdict, microphones in front of them, 1946", card="NÚREMBERG, 1946")
b("El tribunal juzga a personas, pero también a organizaciones. Declara criminales a las SS, con pocas excepciones.",
  "verdict_paper|Close-up of a thick typed verdict document with a heavy red stamp, on a judge's bench" + SEM,
  "headphones|Close-up of a defendant's hands holding translation headphones in a courtroom, 1946")
b("Quien entró o siguió como voluntario después de septiembre de mil novecientos treinta y nueve, sabiendo de sus crímenes, puede ser juzgado por ello.",
  "membership|A pile of old membership cards and folders spread on an evidence table in a courtroom, an evidence tag, the text unreadable" + SEM)
b("Después, en el juicio de los Einsatzgruppen, catorce acusados son condenados a muerte. Solo cuatro son ejecutados.",
  "ohlendorf|A German man in his late thirties in a dark suit standing in the dock wearing headphones, listening to the verdict, 1948",
  "prison_yard|An empty prison yard at dawn with high walls, 1951")
b("Pero miles de miembros de las SS nunca se sientan ante un juez. A muchos les basta un pasaporte.",
  "passport|Close-up of an old closed plain grey booklet with a small photo of a man in a suit clipped to it, lying on a plain paper slip, no words, no letters, no numbers anywhere", ideia=True)

# ───────────────────────── 13. EL PASAPORTE ─────────────────────────
cap("13. El Pasaporte")
b("El Pasaporte. Génova, mil novecientos cuarenta y nueve. Un hombre llamado Helmut Gregor sube a un barco rumbo a Buenos Aires. Lleva un documento de viaje de la Cruz Roja.",
  "genoa|The port of Genoa in 1949, an old ocean liner at the quay, passengers with suitcases climbing the gangway, summer light",
  "gangway|A man in a light suit and a hat with one suitcase walking up a ship's gangway, seen from behind", card="GÉNOVA, 1949")
b("Es Josef Mengele. Pasó más de tres años escondido en una granja de Baviera, trabajando como peón.",
  "mengele_farm|A man in his late thirties with dark hair working as a farmhand in a Bavarian field with a pitchfork, a farmhouse behind, 1947",
  "mengele_face#médio-dir")
b("No es el único. Por las llamadas rutas de las ratas escapan cientos de criminales nazis. Los ayudan algunos clérigos y redes de simpatizantes. Muchos llegan a Sudamérica.",
  "map_ruta|" + MAPA + ", the Atlantic Ocean between Europe and South America, Italy on the upper right and the whole of South America on the left",
  "monastery|A dim monastery corridor in Rome in 1948, a priest handing an envelope to a man in a coat" + SEM)
b("El gobierno de Perón recibe a muchos de ellos en Argentina. Adolf Eichmann llega en mil novecientos cincuenta. Su captura está en nuestro expediente del Mossad.",
  "buenos_aires|Buenos Aires port in 1950, ocean liners and cranes, the city skyline behind, morning",
  "eichmann_bsas|A thin balding man in his forties with glasses and a cheap suit stepping off an old bus without any number or lettering on a dusty Buenos Aires suburban street, 1960")
b("Walter Rauff, el oficial de las SS a cargo de los camiones de gas, vive en Chile hasta su muerte en mil novecientos ochenta y cuatro. Chile nunca lo extradita.",
  "santiago|Santiago de Chile in the 1970s, a quiet residential street with the Andes behind, a parked car",
  "rauff|An elderly German man in his seventies with grey hair and dark glasses sitting in a garden in Santiago, 1983@@WALTER RAUFF")
b("Klaus Barbie, jefe de la Gestapo en Lyon, vive en Bolivia con otro nombre y asesora a gobiernos militares. En mil novecientos ochenta y tres lo expulsan a Francia.",
  "la_paz|La Paz, Bolivia, in the 1970s, the city in its bowl-shaped valley with the snowy Illimani mountain behind",
  "barbie|A bald stocky German man in his sixties with a grey mustache in a dark suit, being escorted off a plain white plane without any logo, number or lettering by police, 1983@@KLAUS BARBIE")
b("Mengele pasa de Argentina a Paraguay y luego a Brasil. Nunca lo encuentran con vida.",
  "map_ruta#detalhe-centro",
  "sao_paulo_70|A modest house on a quiet street in a São Paulo suburb in the 1970s, a garden wall, palm trees", ideia=True)

# ───────────────────────── 14. LA ENTREVISTA ─────────────────────────
cap("14. La Entrevista")
b("La Entrevista. Bariloche, Argentina, mayo de mil novecientos noventa y cuatro. Un equipo de la televisión estadounidense busca a un vecino respetado de la ciudad: Erich Priebke.",
  "bariloche|San Carlos de Bariloche in 1994, wooden alpine-style houses by a blue lake with snowy Andes behind",
  "tv_crew|An American television crew with a large video camera and a microphone on a snowy street in a mountain town, 1994", card="BARILOCHE, 1994")
b("Preside la asociación cultural que sostiene la escuela alemana. Durante la guerra fue capitán de las SS en Roma.",
  "school_bariloche|A wooden German-style school building in a Patagonian town, children playing in the snow",
  "rome_44|Rome in 1944 under occupation, an empty street at dusk, soldiers in plain grey uniforms at a corner" + NOSYM)
b("En marzo de mil novecientos cuarenta y cuatro participó en la matanza de las Fosas Ardeatinas: trescientas treinta y cinco personas asesinadas.",
  "caves|The dark entrance of old quarry caves on the outskirts of Rome, empty, a grey sky, no people",
  "memorial|A long row of identical stone tombs in a quiet underground memorial, soft light, no people", card="ROMA, 1944")
b("Ante la cámara, Priebke no lo niega. Dice que cumplía órdenes.",
  f"priebke|{PRIEBKE}, speaking calmly to a microphone held towards him@@ERICH PRIEBKE",
  "camera_eye|Wide shot of a 1990s television camera on a tripod on a snowy street, its lens reflecting the mountains, a Patagonian town behind")
b("Argentina lo extradita a Italia en mil novecientos noventa y cinco. En mil novecientos noventa y ocho lo condenan a cadena perpetua. Muere en Roma en dos mil trece, a los cien años, bajo arresto domiciliario.",
  "plane_95|A passenger plane on a snowy runway in Patagonia with police cars beside it, 1995",
  "rome_court2|A Rome courtroom in 1998, an old man with white hair and glasses in the dock, judges in robes")
b("Cumplir órdenes. La misma excusa que el tribunal de Núremberg había rechazado medio siglo antes.",
  "judges#detalhe-centro", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. La Tumba")
b("La Tumba. Embu, São Paulo, seis de junio de mil novecientos ochenta y cinco. Los forenses exhuman los restos de Wolfgang Gerhard ante decenas de periodistas.",
  "exhumation#médio-esq",
  "skull_lift|A forensic doctor holding up an old skull to cameras in a hillside cemetery, photographers' flashes, 1985", card="EMBU, 1985")
b("Expertos de Brasil, Alemania y Estados Unidos los examinan. En mil novecientos noventa y dos, una prueba de ADN lo confirma: es Mengele.",
  "forensic_team|A team of forensic experts in white coats examining bones on a table in a lab in 1985",
  "dna|Close-up of DNA test films with black bands on a light box in a lab, 1992")
b("Su familia no los reclama. Desde dos mil dieciséis, los huesos sirven para enseñar medicina forense en la Universidad de São Paulo.",
  "classroom|Medical students in white coats around a table with bones in a university forensic lab today, bright light",
  "skull_table#detalhe-centro")
b("El régimen al que servían las SS prometía durar mil años. Duró doce. Y el médico que decidía en la rampa quién vivía y quién moría terminó como material de estudio.",
  "ramp#aberto", "black_ranks#médio-esq", "waves#detalhe-centro", ideia=True)
b("Y tú, ¿crees que la justicia llegó tarde o que nunca llegó? Déjalo en los comentarios. Si quieres saber cómo atraparon a Eichmann, aquí tienes el expediente completo del Mossad.",
  "folder_close|A hand closing a thick brown case file with a red circular stamp on a dark desk, lamp light" + SEM,
  "red_stamp#médio-esq", "bertioga#aberto")

# a 1ª prova do 001 (04/11) saiu com moldura de papel: todo prompt leva sangria explícita
SANGRIA = ", full-bleed illustration filling the entire frame edge to edge, no border, no margin, no white frame, no panel outline"

# Thumbs (biblia/thumb.md + brief: nada de suástica/runas em destaque nem vítimas): personagem à esquerda com objeto que conta o tema, metade direita livre.
THUMBS = [
    {"id": "thumb-A", "prompt": f"A cold German officer in his thirties in half body on the LEFT third of the frame, bareheaded with short hair shaved at the sides, no cap, {NEGRO}, round rimless glasses, holding an open brown file folder with a black-and-white portrait photo clipped to it, stern stare at the viewer, behind him a dark grey stone hall with tall windows; the RIGHT half of the image is plain dark empty grey wall in shadow" + NOSYM + SEM},
    {"id": "thumb-B", "prompt": f"{MENGELE_OLD.replace(', 1979', '')}, wearing a straw hat and dark sunglasses, in half body on the LEFT third of the frame, looking over his shoulder suspiciously, holding an old grey passport, behind him a tropical beach with palm trees and a calm sea at sunset; the RIGHT half of the image is plain empty orange-grey sunset sky" + NOSYM + SEM},
    {"id": "thumb-C", "prompt": f"A German officer in his thirties seen in half body on the LEFT third of the frame, {NEGRO}, bareheaded with slicked-back hair, no cap, plain black collar without patches, his face half in deep shadow, black leather gloves, pulling on one glove, behind him long rows of men in plain black uniforms standing in formation in a foggy square; the RIGHT half of the image is plain dark empty foggy sky" + NOSYM + SEM},
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
