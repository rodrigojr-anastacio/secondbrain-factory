#!/usr/bin/env python3
"""Fonte única do dossie-es 009 (La Gestapo): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (na pasta do vídeo). Conteúdo no topo; geração no fim (copiada do 008-inquisicion).

Embalagem aprovada no crivo r1 (15/11/2026, EMBALAGEM.md/CRIVO.md):
  T1 "GESTAPO: La policía secreta de Hitler y sus hombres en Sudamérica" · T2 "Cómo funcionaba la Gestapo: del sótano de
  Berlín a un nombre falso en Bolivia" · thumb: sobretudo de couro vazio no cabide + janela andina + sello "1983".
  Frase-âncora do hook: "Esta es TODA la historia de la Gestapo. Y de cómo sus hombres llegaron a Sudamérica."
Molde da bíblia (canais/dossie-es/biblia/roteiro.md): hook por anedota (La Paz, 1983: o empresário "Klaus Altmann" preso por
uma dívida, expulso e trancado em Montluc; era Klaus Barbie) → 14 expedientes-objeto com título falado → hook pago no
expediente 13 ("La Celda") → cierre "La Deuda" (volta ao objeto do hook) + aforismo + pergunta.
Não repete capítulos/anedotas do Archive (pbIzG1QvoWs; ref/archive-gestapo.txt): viúva e a piada, carimbo do correio,
granjeiro, pilar de Elser, curva de Praga, Orquestra Vermelha, Rosa Branca, maleta de Stauffenberg, porão-museu como cierre.
Fio Sudamérica: Olga Benário/Brasil (4), Eichmann/Argentina (5), Barbie (7, 8, 10–13), Priebke/Bariloche (14).
Tema nazista: sem suástica, runas, águia, braçadeira ou bandeira; sem corpos; vocabulário de vítima (asesinar, deportar).

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (id I### na ordem de aparição) · "chave" reuso · "chave#enq" reuso com enquadramento
  + "@@TEXTO"      rótulo na tela (máquina de escrever; CAIXA ALTA, até ~28 caracteres)
Bloco: b(texto, *planos, card="LA PAZ, 1983", ideia=True) · capítulo: cap("5. La Oficina")
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
TITULO = "GESTAPO: La policía secreta de Hitler y sus hombres en Sudamérica"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

SEM = ", no lettering anywhere"   # papéis, placas, capas: o nano-banana inventa texto
NOINS = ", no insignia, no armbands, no eagles, no swastikas, no runes, no flags, no badges"
VIOL = ", seen from far away, no bodies, no blood"
# figurino Gestapo: civil, sem nada que vire símbolo
COAT = "a long black leather coat with a belt and a dark fedora hat"
# Personagens (descrição visual fixa; rostos "resembling", nunca foto)
ALTMANN = "a stocky German businessman of nearly seventy with thinning grey hair combed back, heavy eyelids, a thin mouth and a dark suit and tie, 1983, resembling Klaus Barbie in old age"
BARBIE = "a short German officer of thirty with slicked-back dark hair, a narrow face and cold pale eyes, wearing a dark civilian suit and tie, 1943, resembling the young Klaus Barbie"
GORING = "a heavy-set German politician of forty in a light grey uniform-like suit without any insignia, a broad face, 1933, resembling Hermann Göring"
DIELS = "a thin German official in his early thirties with dark hair and a scarred cheek, a dark civilian suit, 1933, resembling Rudolf Diels"
HIMMLER = "a slight German man in his early thirties with round rimless glasses, a small moustache and a receding chin, a dark civilian suit, 1934, resembling Heinrich Himmler"
HEYDRICH = "a tall German man of thirty with a long narrow face, blond hair combed back and a high forehead, a dark civilian suit, 1934, resembling Reinhard Heydrich"
MULLER = "a stocky German police detective in his late thirties with a square face, short dark hair and a hard stare, a grey civilian suit, 1936, resembling Heinrich Müller"
OLGA = "a young German woman of twenty-eight with short dark wavy hair and a determined face, a simple dark 1930s dress, visibly pregnant, resembling Olga Benário"
EICHMANN = "a thin balding German man in his late forties with glasses and a narrow face, a plain grey suit, 1950s Argentina, resembling Adolf Eichmann"
MOULIN = "a French man in his forties wearing a dark felt hat tilted to one side and a scarf around his neck, a calm face, 1943, resembling Jean Moulin"
BEATE = "a determined German woman in her early thirties with short blond hair and a dark coat, 1972"
PRIEBKE = "a tall thin German man of eighty with white hair, glasses and a beige windbreaker, standing on a sidewalk in a mountain town, 1994, resembling Erich Priebke"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, borders and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame"

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("La Paz, mil novecientos ochenta y tres. La policía detiene a un empresario alemán.",
  "lapaz_1983|The city of La Paz, Bolivia, in 1983 seen from above, red brick houses climbing the steep sides of a deep valley, the snow-capped Illimani mountain behind, cold morning light",
  f"altmann_arrest|{ALTMANN} being escorted out of an office building by two Bolivian plainclothes policemen in 1980s suits, a city street in La Paz, plain stone walls with no plaques, no signs, no lettering anywhere",
  "police_car|A 1980s Bolivian police car parked on a steep cobbled street of La Paz, a policeman at the door, morning" + SEM, card="LA PAZ, 1983")
b("Se llama Klaus Altmann. Le reclaman una deuda de diez mil dólares.",
  f"altmann_face|{ALTMANN} in portrait, sitting behind a desk with a calm unreadable expression, 1983@@KLAUS ALTMANN",
  "debt_papers|Stack of blank cream-colored sheets of paper on a wooden desk seen from a few steps away, a red ink stamp pad and a pen beside it, every sheet completely empty, no writing, no marks, no signs" + SEM)
b("Días después, lo expulsan a Francia.",
  "plane_night|A military transport propeller plane on a dark runway at night, floodlights, a man in a suit escorted up the stairs between guards")
b("Lo encierran en Lyon, en la cárcel de Montluc. Allí, cuarenta años antes, él encerraba a sus víctimas.",
  "montluc|The grim stone walls and heavy gate of the old Montluc military prison in Lyon, France, grey winter light",
  "cell_door|A heavy old prison cell door with a small barred window in a stone corridor, a single bulb",
  f"barbie_young|{BARBIE} standing in a dim prison corridor in 1943, hands behind his back, looking at the viewer" + NOINS)
b("En Lyon no lo llamaban Altmann. Lo llamaban Klaus Barbie, jefe de la Gestapo.",
  f"old_young|Split portrait: on the left {ALTMANN}, on the right {BARBIE}, the same cold eyes, dark background" + NOINS,
  "coat_hook|A long black leather coat with a belt hanging alone on a wooden coat hanger on a bare wall, dramatic side light, no person" + NOINS)
b("Esta es TODA la historia de la Gestapo. Y de cómo sus hombres llegaron a Sudamérica.",
  "files_desk|A long dark desk covered with open brown case files tied with red string and black and white photographs, a red rubber stamp and a magnifying glass, lamp light" + SEM,
  "red_stamp|A hand slamming a red rubber stamp onto a brown paper case file, ink splash, dramatic close-up" + SEM,
  "andes_road|A lonely road winding through the high Andes plateau towards snowy mountains, an old 1950s car on it, wide landscape", ideia=True)

# ───────────────────────── 1. EL SÓTANO ─────────────────────────
cap("1. El Sótano")
b("El Sótano. Berlín, veintiséis de abril de mil novecientos treinta y tres. Hermann Göring, ministro del Interior de Prusia, crea una nueva policía política.",
  "berlin_1933|A wide Berlin street in 1933 with grand stone buildings, trams and black cars, grey spring light" + NOINS,
  f"goring|{GORING} signing a document at a large desk in a ministry office, 1933" + NOINS + SEM,
  f"goring_face|{GORING} in portrait, a smug confident look, dark background@@HERMANN GÖRING",
  "ministry_door|The heavy carved wooden doors of a Prussian ministry in Berlin in 1933, a guard in a long coat beside them" + NOINS + SEM, card="BERLÍN, 1933")
b("La llaman Policía Secreta del Estado. En alemán, Geheime Staatspolizei. Gestapo.",
  f"diels|{DIELS} standing in a long office corridor with filing cabinets, 1933@@RUDOLF DIELS",
  "gestapo_men|Three German plainclothes policemen in long dark leather coats and fedoras walking side by side on a Berlin pavement in 1933, seen from a low angle" + NOINS)
b("Se instala en la calle Prinz Albrecht, número ocho. Arriba, oficinas. En el sótano, celdas.",
  "prinz_albrecht|A large grey neoclassical stone building on a Berlin street in 1933, tall windows, a black car at the entrance" + NOINS + SEM,
  "basement_corridor|A narrow basement corridor with a row of small cell doors under bare electric bulbs, whitewashed brick walls, 1933",
  "cell_inside|Inside a small bare basement cell: a wooden plank bed, a bucket and a tiny high window, cold light, empty")
b("No hace falta un juez. Tras el incendio del Reichstag, en febrero, un decreto permite la llamada custodia protectora.",
  "reichstag_fire|The Reichstag building in Berlin burning at night in February 1933, the glass dome glowing orange, smoke, crowds watching from far away",
  "fire_ruin|The burnt-out glass dome of the Reichstag at dawn after the fire, smoke still rising, February 1933" + SEM + ", no inscription on the building",
  "decree|Close-up of a printed government decree on official paper lying on a desk next to a fountain pen" + SEM)
b("Es decir: encerrar a cualquiera sin cargos, sin abogado y sin fecha de salida.",
  "arrest_night|Plainclothes policemen in leather coats taking a man in pajamas and a coat out of an apartment building at night, a neighbor watching from a window" + NOINS,
  "detainee|A frightened man in his thirties in a rumpled shirt sitting on a wooden bench in a bare police room, 1933")
b("En unos meses, decenas de miles de opositores pasan por sótanos, cuarteles y los primeros campos. Sobre todo, comunistas y socialistas.",
  "truck_prisoners|An open truck full of arrested men in civilian clothes guarded by men in dark coats on a Berlin street, 1933" + NOINS,
  "camp_gate|The wooden gate and barbed-wire fence of an early 1933 detention camp in the German countryside, a watchtower, grey sky, no people" + NOINS + SEM,
  "lists|A gloved hand holding a clipboard seen from behind so only the back of the board and the hand are visible, dim office, no paper visible" + SEM)
b("Pero esa policía es de Göring. Y otro hombre la quiere: Heinrich Himmler, el jefe de las SS.",
  f"himmler_shadow|{HIMMLER} watching from a doorway in the half dark, glasses glinting" + NOINS,
  "goring_himmler|Two German officials in dark civilian suits facing each other across a desk in a tense silence, a closed folder between them, 1934" + NOINS + SEM,
  "card_drawer|A long wooden drawer of an index card cabinet pulled open, hundreds of small cards with photos, lamp light" + SEM, ideia=True)

# ───────────────────────── 2. EL FICHERO ─────────────────────────
cap("2. El Fichero")
b("El Fichero. Abril de mil novecientos treinta y cuatro. Göring le cede la Gestapo a Himmler.",
  f"handover|{GORING} handing a thick folder to {HIMMLER} across a desk in a dark wood office, 1934" + NOINS + SEM,
  f"himmler_face|{HIMMLER} in portrait, a cold neutral face, dark background@@HEINRICH HIMMLER",
  "ss_hq|A grand old stone palace building in Berlin in 1934 with black cars at the entrance and men in dark coats on the steps" + NOINS + SEM, card="BERLÍN, 1934")
b("Al frente pone a su número dos, Reinhard Heydrich, de treinta años, que venía del servicio de inteligencia de las SS.",
  f"heydrich|{HEYDRICH} in portrait standing by a tall window in an office, a cold stare@@REINHARD HEYDRICH",
  f"heydrich_desk|{HEYDRICH} reading index cards at a desk under a green lamp" + NOINS + SEM,
  "sd_files|Close-up of a stack of thin intelligence folders tied with string on a dark desk, a fountain pen on top" + SEM)
b("Su herramienta es el papel. Cada opositor, cada sospechoso y cada rumor terminan en una ficha.",
  "card_hands|Close-up of hands typing a small index card on a black typewriter, a photo clipped to it" + SEM,
  "card_room|A large hall full of tall wooden filing cabinets with clerks pulling drawers, 1930s Berlin office" + SEM,
  "photo_clip|Close-up of a small black and white ID photo of a man paper-clipped to an index card" + SEM)
b("En febrero de mil novecientos treinta y seis, una ley prusiana decide que los tribunales administrativos no pueden revisar las órdenes de la Gestapo.",
  "court_empty|An empty German courtroom of the 1930s with dark wood benches and a judge's bench, dusty light",
  "law_page|Close-up of an official law gazette page lying on a judge's desk next to a gavel" + SEM,
  "judge_shadow|A German judge in a black robe and cap sitting alone at his bench with his hands folded, a closed file in front of him, 1936" + SEM)
b("Ese mismo año, Himmler pasa a ser jefe de toda la policía alemana.",
  "police_parade|Rows of German uniformed policemen in shakos standing in a Berlin square in 1936, seen from far away" + NOINS,
  "police_cars|A row of black 1930s police cars parked in front of a Berlin police headquarters, men in coats walking past" + NOINS + SEM)
b("El trabajo diario queda en manos de Heinrich Müller, un detective de Múnich que había pasado años persiguiendo comunistas.",
  f"muller|{MULLER} in portrait in an office, a hard stare@@HEINRICH MÜLLER",
  f"muller_files|{MULLER} going through a pile of files with two assistants in a smoky office" + NOINS + SEM,
  "munich_1930|A street in Munich in the 1920s with tram lines and old facades, a policeman in a long coat on the corner, rainy, no street signs, no shop signs, no signboards, no lettering anywhere" + NOINS)
b("Con tanto poder, uno imagina un ejército de agentes. Los números dicen otra cosa.",
  "army_shadow|Long shadows of men in hats stretching across a cobbled street at sunset, seen from above",
  "empty_office|A small provincial police office of the 1930s with only three desks and a typewriter, empty chairs", ideia=True)

# ───────────────────────── 3. LA DENUNCIA ─────────────────────────
cap("3. La Denuncia")
b("La Denuncia. Würzburg, Baviera, mil novecientos treinta y nueve. La Gestapo tiene veintidós funcionarios para toda la región: más de ochocientos cuarenta mil habitantes.",
  "wurzburg|The old Bavarian city of Würzburg in 1937, the river Main, an old stone bridge with statues and church towers, autumn",
  "wurzburg_office|A small Gestapo office in a provincial German town, a few men in suits at desks, a wall map, 1937" + NOINS + SEM,
  "crowd_wurzburg|A busy market square in a Bavarian town in 1937 full of people, seen from above", card="WÜRZBURG, 1939")
b("Unos diecinueve mil expedientes de esa oficina sobrevivieron. El historiador Robert Gellately los estudió.",
  "archive_boxes|Rows of old cardboard archive boxes on metal shelves in a quiet archive, dust in the light" + SEM,
  "historian|A historian with reading glasses studying old typed documents at a long archive table, a lamp, 1980s" + SEM)
b("Descubrió que muchos casos no empezaban con un espía. Empezaban con una carta o una visita: un ciudadano que denunciaba a otro.",
  "letter_write|A woman at a kitchen table in a 1930s German apartment writing a letter by lamplight, glancing at the wall" + SEM,
  "letter_desk|A handwritten letter in an envelope placed on a police officer's desk, a hand reaching for it" + SEM,
  "visit|A middle-aged man in a hat speaking in a low voice to a police officer across a counter in a 1930s German police station")
b("La portera denuncia al inquilino. El empleado, a su jefe. La esposa, al marido del que quiere separarse.",
  "concierge|A stern concierge woman watching from her window in the entrance hall of a Berlin apartment building, 1930s",
  "office_worker|A clerk in a 1930s office looking sideways at his boss behind a glass door",
  "wife|A woman standing at the door of an apartment watching her husband leave down the stairs, a cold look, 1930s")
b("Una ley de diciembre de mil novecientos treinta y cuatro castiga hasta un comentario contra el régimen.",
  "pub_whisper|Two men whispering at a table in a smoky 1930s German beer hall, a third man at the next table listening, nobody holds a newspaper, no posters on the walls, no lettering anywhere",
  "ear_wall|Close-up of a woman's ear pressed against a thin apartment wall, flowered wallpaper",
  "radio_joke|A small group of German workers laughing quietly around a 1930s radio set in a factory canteen, one of them glancing over his shoulder")
b("La propia Gestapo se queja de que muchas denuncias son falsas: venganzas, peleas de vecinos, celos.",
  "pile_letters|A tall pile of opened letters and envelopes on a police desk, an officer rubbing his eyes" + SEM,
  "neighbors_argue|Two neighbors arguing on a staircase landing of a German tenement building in the 1930s")
b("La Gestapo no necesitaba vigilar a todos. Le bastaba con que los vecinos se vigilaran entre sí.",
  "windows_watch|A courtyard of a Berlin tenement building at dusk, several windows with silhouettes watching, curtains half open",
  "curtain|Close-up of a hand pulling back a lace curtain to look out at the street, 1930s")
b("Y a veces, los presos llegaban de mucho más lejos. En barco, desde Sudamérica.",
  "ship_sea|A 1930s German passenger steamship crossing the Atlantic ocean at dusk, smoke from its funnels" + NOINS + SEM, ideia=True)

# ───────────────────────── 4. EL BARCO ─────────────────────────
cap("4. El Barco")
b("El Barco. Río de Janeiro, septiembre de mil novecientos treinta y seis. La policía brasileña sube a una prisionera a un barco alemán, el La Coruña.",
  "rio_1936|The harbor of Rio de Janeiro in 1936 with Sugarloaf mountain behind, ships at the quay, tropical light",
  "ship_quay|A German steamship docked at a quay in Rio de Janeiro in 1936, Brazilian policemen in 1930s uniforms escorting a woman up the gangway" + NOINS + SEM,
  "map_atlantico|" + MAPA + ", the whole Atlantic ocean with South America on the left and Europe and Africa on the right, all sea areas completely blank", card="RÍO DE JANEIRO, 1936")
b("Es Olga Benário, comunista alemana, de veintiocho años. Está embarazada de siete meses.",
  f"olga|{OLGA} in portrait, looking straight ahead with a calm defiant face, 1936@@OLGA BENÁRIO",
  f"olga_cabin|{OLGA} sitting alone in a small ship cabin with a round porthole, a hand on her belly, dim light")
b("Había llegado a Brasil con el líder comunista Luis Carlos Prestes. Preparaban un levantamiento en mil novecientos treinta y cinco. Fracasó.",
  "prestes|A Brazilian man in his late thirties with a dark beard and moustache and a serious face, 1935, resembling Luís Carlos Prestes@@LUÍS CARLOS PRESTES",
  "barracks_1935|Soldiers fighting around a barracks in Rio de Janeiro in November 1935, smoke" + VIOL)
b("El gobierno de Getulio Vargas decide entregarla a Alemania. El Supremo Tribunal Federal rechaza el recurso para salvarla.",
  "vargas|A short Brazilian president in his fifties with glasses and a white suit at a desk, 1936, resembling Getúlio Vargas" + SEM,
  "supreme_court|The neoclassical building of the Brazilian Supreme Court in Rio de Janeiro in 1936, columns, judges entering" + SEM)
b("Según el biógrafo Fernando Morais, la policía de Filinto Müller y la Gestapo intercambiaban información sobre los comunistas.",
  "telegrams|Close-up of telegrams and typed reports being exchanged across a desk between two hands" + SEM,
  "filinto|A Brazilian police chief in his late thirties in a dark suit with slicked hair, 1936, resembling Filinto Müller@@FILINTO MÜLLER")
b("En Hamburgo la espera la Gestapo. Su hija, Anita, nace en noviembre en una cárcel de mujeres de Berlín.",
  "hamburg_port|The port of Hamburg in October 1936, cranes, grey water, men in long leather coats waiting on the quay" + NOINS,
  "prison_berlin|A red brick women's prison in Berlin in 1936, high walls, a small barred window with light")
b("A los catorce meses, la abuela consigue llevársela. Olga nunca sale.",
  "grandmother|An elderly Brazilian woman in black holding a little girl wrapped in a blanket, leaving a prison gate in 1938")
b("En mil novecientos cuarenta y dos es asesinada con gas en Bernburg, uno de los centros donde el régimen asesinaba a enfermos y prisioneros.",
  "bernburg|A plain brick hospital-like building behind trees in a German town in 1942, grey sky, no people" + SEM)
b("Para entonces, la Gestapo ya era parte de una oficina mucho más grande.",
  "map_europa|" + MAPA + ", the whole of Europe from Spain to Russia and from Norway to the Mediterranean, all sea areas completely blank", ideia=True)

# ───────────────────────── 5. LA OFICINA ─────────────────────────
cap("5. La Oficina")
b("La Oficina. Berlín, veintisiete de septiembre de mil novecientos treinta y nueve. La guerra lleva casi cuatro semanas.",
  "berlin_1939|Berlin in September 1939, a grey government street with black cars and passers-by in coats" + NOINS, card="BERLÍN, 1939")
b("Himmler une la Gestapo, la policía criminal y el servicio de inteligencia de las SS. Nace la Oficina Central de Seguridad del Reich. La dirige Heydrich.",
  "three_doors|Three heavy office doors side by side in a long government corridor in Berlin, one of them open" + SEM,
  "organigram|Close-up of a hand drawing an organization chart with boxes and lines on a large sheet of paper" + SEM,
  "heydrich#médio-dir")
b("La Gestapo pasa a ser su Departamento Cuatro, bajo Müller.",
  "muller#detalhe-centro")
b("Dentro, una sección pequeña, la IV B4, organiza la persecución de los judíos. La dirige Adolf Eichmann.",
  "eichmann_office|A small office in Berlin in 1941 with a desk covered in railway timetables and typed lists, a man's back in a grey uniform-like suit" + NOINS + SEM,
  "eichmann_young|A thin German official in his mid thirties with a narrow face and a receding hairline at a desk, 1941, resembling Adolf Eichmann@@ADOLF EICHMANN")
b("Desde ahí se preparan las listas y los trenes que llevan a los judíos de Europa a los campos de exterminio.",
  "train_station|A crowd of families with suitcases being herded onto freight cars at a European railway station, guards in long coats" + VIOL + NOINS,
  "freight_cars|A long line of closed wooden freight wagons on a railway track in fog, 1942, no people")
b("En mil novecientos cincuenta, Eichmann llega a Buenos Aires con otro nombre: Ricardo Klement.",
  "buenos_aires|Buenos Aires in 1950, a wide avenue with old cars and buses, an obelisk in the distance, sunny",
  f"klement|{EICHMANN} getting off a bus in a quiet suburb of Buenos Aires in the late 1950s, carrying a briefcase@@RICARDO KLEMENT", card="BUENOS AIRES, 1950")
b("Vive diez años en Argentina, hasta que el Mossad lo atrapa en mil novecientos sesenta. Esa operación ya está en nuestro expediente del Mossad.",
  "garibaldi|A modest one-storey brick house in a suburb of Buenos Aires at night, a single street lamp, 1960",
  "car_night|A black car parked in the dark on an unpaved suburban street, headlights off, 1960")
b("No fue el único hombre de la Gestapo que llegó a Sudamérica.",
  "coat_hook#detalhe-centro", ideia=True)

# ───────────────────────── 6. LA NIEBLA ─────────────────────────
cap("6. La Niebla")
b("La Niebla. Siete de diciembre de mil novecientos cuarenta y uno. Hitler lo ordena y el mariscal Wilhelm Keitel firma las instrucciones: el decreto Noche y Niebla.",
  "keitel|A German field marshal in his late fifties with a stiff face and a grey uniform without any insignia signing a paper at a desk, 1941, resembling Wilhelm Keitel" + NOINS + SEM,
  "fog_road|A country road in northern France disappearing into thick fog at night, a single car with dim headlights", card="1941")
b("En Francia, Bélgica y Holanda, los sospechosos de resistencia son llevados en secreto a Alemania.",
  "night_arrest_fr|Men in long leather coats leading a French man out of a farmhouse into a car at night, fog" + NOINS,
  "map_europa#médio-esq",
  "closed_truck|A covered military truck driving into thick fog at night" + NOINS)
b("Sus familias no reciben ninguna noticia. Ni dónde están, ni si siguen con vida.",
  "mother_wait|A French woman in her fifties standing at the window of a village house in fog, holding a photograph",
  "empty_chair|An empty chair at a set dinner table in a French kitchen, a plate and a candle")
b("Keitel lo explica por escrito: para sembrar el terror, la familia no debe saber qué pasó con el detenido.",
  "keitel_paper|A folded sheet of blank paper with a fountain pen resting on it, on a dark desk, lamp light, the paper is empty, no writing, no signature" + SEM)
b("Lo aplican la Gestapo y la policía de seguridad. Hasta abril de mil novecientos cuarenta y cuatro, al menos seis mil seiscientas personas desaparecen así.",
  "fog_figures|A line of prisoners in civilian coats walking into fog between guards, seen from far away" + VIOL + NOINS,
  "folder_nn|A thin brown case file lying alone on a dark desk in a cold office, lamp light" + SEM)
b("En Lyon, ese terror tiene la cara de un oficial de veintinueve años.",
  "barbie_young#médio-esq", ideia=True)

# ───────────────────────── 7. EL HOTEL ─────────────────────────
cap("7. El Hotel")
b("El Hotel. Lyon, noviembre de mil novecientos cuarenta y dos. Los alemanes ocupan el sur de Francia. La Gestapo se instala en el Hotel Terminus, junto a la estación.",
  "lyon_1942|The city of Lyon in winter 1942, the two rivers, bridges and the hill of Fourvière with its basilica, grey light",
  "hotel_terminus|A grand early 20th century hotel facade next to a railway station in Lyon in 1942, black cars outside, men in long leather coats at the door" + NOINS + SEM, card="LYON, 1942")
b("Al frente de la sección de la Gestapo en Lyon está Klaus Barbie.",
  f"barbie_office|{BARBIE} sitting behind a desk in a hotel room turned into an office, a lamp, papers" + NOINS + SEM,
  "barbie_young#detalhe-centro")
b("Había entrado al servicio de inteligencia de las SS en mil novecientos treinta y cinco. Antes de Lyon, persiguió a judíos y opositores en Ámsterdam.",
  "amsterdam|A canal in Amsterdam in 1941 with tall narrow brick houses, bicycles, grey sky",
  "amsterdam_raid|Men in long coats checking papers of passers-by on a bridge over an Amsterdam canal, 1941" + NOINS)
b("En Lyon persigue a la Resistencia. El veintiuno de junio de mil novecientos cuarenta y tres, sus hombres irrumpen en una casa de Caluire.",
  "caluire|A two-storey doctor's house with a garden in a quiet suburb of Lyon in June 1943, black cars stopping in front",
  "door_burst|Men in long leather coats bursting through the door of a house into a waiting room" + NOINS)
b("Detienen a Jean Moulin, el enviado de De Gaulle que había unido a la Resistencia francesa.",
  f"moulin|{MOULIN} in portrait, looking off to the side, 1943@@JEAN MOULIN",
  f"moulin_arrest|{MOULIN} being led out of a house in handcuffs between two men in leather coats" + NOINS)
b("Moulin muere el ocho de julio, tras las torturas, en un tren hacia Alemania. Según los historiadores, no entregó a nadie.",
  "moulin_hat|Close-up of a dark felt hat and a scarf lying on a wooden chair in an empty room, cold light")
b("Según los testimonios de su juicio, Barbie torturaba con sus propias manos. Los sobrevivientes lo llamaron el Carnicero de Lyon.",
  "interrogation|A bare interrogation room with a table, a lamp and an empty chair, a man's shadow on the wall" + NOINS,
  "survivor|An elderly French woman in the 1980s looking at an old photograph, a serious face")
b("Si te gustan estos expedientes, suscríbete. Porque una de las pruebas que más pesaron contra Barbie no fue un testimonio. Fue un papel.",
  "telex_machine|An old 1940s teleprinter machine seen from the side in lamp light, a short strip of completely blank paper curling out of it, no characters printed, no buttons with symbols" + SEM, ideia=True)

# ───────────────────────── 8. EL TÉLEX ─────────────────────────
cap("8. El Télex")
b("El Télex. Izieu, un pueblo en las montañas al este de Lyon. Seis de abril de mil novecientos cuarenta y cuatro, por la mañana.",
  "izieu|A large stone farmhouse on a green hillside above a valley in the French Alps foothills, a fountain in the yard, spring morning",
  "izieu_valley|A peaceful green valley in the mountains of southeastern France in spring, morning mist", card="IZIEU, 1944")
b("En un hogar infantil viven escondidos niños judíos.",
  "classroom|A simple village classroom with small wooden desks, children's drawings on the wall, empty, morning light")
b("Llegan camiones. Se llevan a cuarenta y cuatro niños y a siete adultos.",
  "breakfast|A long wooden table set with bowls for breakfast in a farmhouse kitchen, chairs pushed back, nobody there",
  "trucks_izieu|Two military trucks driving up a dusty country road toward a farmhouse in the hills, seen from far away" + NOINS,
  "empty_yard|The empty yard of a farmhouse with a stone fountain, a child's shoe left on the ground")
b("Esa noche, Barbie firma un télex para París. Informa de la redada en el hogar de Izieu.",
  "telex_strip|Close-up of a long strip of completely blank teleprinter paper curling over a dark desk, only faint perforation dots along the edges, no characters, no writing, no signature" + SEM,
  "barbie_sign|Close-up of a man's hand signing a typed message at a desk at night, a lamp" + SEM)
b("Casi todos son asesinados en Auschwitz. Ninguno de los niños sobrevive. De los adultos, solo vuelve una mujer.",
  "rails|Railway tracks disappearing into the distance under a grey sky, a single signal light",
  "drawing|A child's drawing of a house and mountains pinned on a wooden wall, faded colors" + SEM)
b("El télex queda en los archivos. Décadas después, será una de las pruebas que más pesen contra él.",
  "archive_boxes#detalhe-alto")
b("Pero primero, la Gestapo tiene que perder la guerra.",
  "berlin_ruins|The ruins of Berlin in 1945, burnt-out buildings and rubble under a pale sky, smoke rising", ideia=True)

# ───────────────────────── 9. LAS CENIZAS ─────────────────────────
cap("9. Las Cenizas")
b("Las Cenizas. Primavera de mil novecientos cuarenta y cinco. En toda Alemania, las oficinas de la Gestapo queman sus archivos.",
  "burning_files|Men in coats throwing armfuls of files into a fire in a courtyard, papers flying, smoke" + NOINS,
  "ashes|Close-up of burnt paper and ashes blowing across a stone courtyard", card="1945")
b("En los últimos días, sus agentes asesinan a presos en sus propias cárceles.",
  "prison_yard|An empty prison yard with high brick walls at dawn, an open gate" + VIOL)
b("Himmler se envenena tras ser capturado por los británicos. Heinrich Müller desaparece en Berlín y nunca lo encuentran.",
  "himmler_face#detalhe-centro",
  "muller_empty|An empty office chair behind a desk covered in dust and fallen plaster in a ruined Berlin office, 1945" + SEM)
b("En Núremberg, en mil novecientos cuarenta y seis, el tribunal internacional declara a la Gestapo organización criminal.",
  "nuremberg|The courtroom of the Nuremberg trials in 1946, judges at a long bench, defendants in two rows, military police in white helmets" + NOINS + SEM,
  "verdict|Close-up of a judge's hands holding a blank folded sheet, a Nuremberg courtroom desk behind, a wooden gavel only, no electronics, no writing" + SEM, card="NÚREMBERG, 1946")
b("Pero condenar a una organización no es juzgar a sus hombres. La mayoría nunca pisa un tribunal. Muchos vuelven a ser policías en Alemania Occidental.",
  "west_police|A West German police station in the 1950s, officers in new uniforms at desks, a calendar on the wall" + NOINS + SEM,
  "ex_agent|A middle-aged man in a 1950s suit and hat walking calmly down a German street seen from behind, plain house facades with every shop window and sign blank, no signs, no shop names, no lettering anywhere" + SEM)
b("Y a algunos les llega una oferta de trabajo. Viene de los Estados Unidos.",
  "us_jeep|A US Army jeep parked in a ruined German street in 1947, two American soldiers smoking" + SEM, ideia=True)

# ───────────────────────── 10. EL CONTRATO ─────────────────────────
cap("10. El Contrato")
b("El Contrato. Alemania ocupada, mil novecientos cuarenta y siete. El servicio de contrainteligencia del Ejército de Estados Unidos recluta a un informante: Klaus Barbie.",
  "cic_office|A small American military office in occupied Germany in 1947, an American officer in uniform interviewing a German man in a suit" + SEM,
  f"barbie_1947|{BARBIE.replace('1943', '1947')}, in a worn suit, sitting across a table from an American officer" + NOINS, card="ALEMANIA, 1947")
b("Francia lo busca por crímenes de guerra. Pero los estadounidenses quieren lo que él sabe de los comunistas.",
  "wanted|Close-up of a French arrest warrant on a desk next to a black and white photograph" + SEM,
  "dollar_envelope|An envelope with banknotes passed under a table between two hands, 1940s" + SEM)
b("Lo dice un informe del Departamento de Justicia de Estados Unidos, de mil novecientos ochenta y tres. Sus agentes lo protegieron y ocultaron a Francia dónde estaba. Después, lo ayudaron a escapar.",
  "report_1983|Close-up of a thick typed government report with a plain cover lying on a desk, 1983" + SEM,
  "us_officers|Two American intelligence officers in 1950 talking quietly in a corridor, one holding a folder" + SEM)
b("En mil novecientos cincuenta y uno, le consiguen documentos con otro nombre.",
  "new_papers|Close-up of a hand placing an identity booklet on top of a travel document on a table, an ink stamp beside it, both booklets have plain blank dark covers with no emblem, no text, no writing inside" + SEM, ideia=True)

# ───────────────────────── 11. LA RUTA ─────────────────────────
cap("11. La Ruta")
b("La Ruta. Génova, marzo de mil novecientos cincuenta y uno. Barbie, su esposa y sus dos hijos suben a un barco hacia Buenos Aires.",
  "genoa|The port of Genoa in 1951 with an ocean liner at the quay, cranes and the hills of the city behind",
  "family_ship|A German man in a hat, a woman and two small children walking up the gangway of an ocean liner, 1951, seen from behind", card="GÉNOVA, 1951")
b("Sus papeles dicen Klaus Altmann.",
  "altmann_papers|Close-up of an old travel document held in a man's hand on the deck of a ship, the sea behind" + SEM)
b("En Génova lo recibe un sacerdote croata, Krunoslav Draganović. Según el informe, ya había sacado de Europa a otros fugitivos. Es la llamada ruta de las ratas.",
  "priest_rome|A Catholic priest in a black cassock and glasses in his late forties in a Roman office full of papers, 1951, resembling Krunoslav Draganović@@KRUNOSLAV DRAGANOVIĆ",
  "map_atlantico#médio-dir")
b("De Buenos Aires sigue a Bolivia. En mil novecientos cincuenta y siete recibe la nacionalidad boliviana.",
  "train_andes|An old steam train crossing the high Andes plateau with snowy mountains behind, 1951",
  "lapaz_1983#médio-esq")
b("Tiene un aserradero, luego una naviera. Y trato con ministros y generales.",
  "sawmill|A sawmill in the Bolivian lowland jungle in the 1950s, logs and workers, green forest",
  f"altmann_generals|{ALTMANN.replace('nearly seventy', 'fifty-five').replace('1983', '1968')} shaking hands with Bolivian army officers at a reception" + NOINS)
b("Según investigaciones posteriores, asesoró a los servicios de seguridad de varios gobiernos militares.",
  "military_office|A Bolivian military office in the 1970s with officers around a table and a man in a civilian suit speaking" + NOINS + SEM)
b("Durante veinte años, nadie lo molesta en Bolivia. Hasta que alguien en Europa compara unas fotos.",
  "two_photos|Two black and white portrait photographs side by side on a table under a magnifying glass" + SEM, ideia=True)

# ───────────────────────── 12. LA FOTO ─────────────────────────
cap("12. La Foto")
b("La Foto. Mil novecientos setenta y uno. Un fiscal de Múnich tiene fotos de un tal Klaus Altmann, que vive en Bolivia.",
  "prosecutor|A German prosecutor in his fifties in a grey suit at a desk in a Munich office in 1971, holding a black and white photograph" + SEM,
  "photo_altmann|Close-up of a black and white photograph of an older man in a suit lying among papers" + SEM, card="1971")
b("Beate y Serge Klarsfeld, una pareja que persigue a criminales nazis, las comparan con las del oficial de Lyon. Para ellos, es el mismo hombre.",
  f"beate|{BEATE} at a desk covered in files in a Paris apartment, a telephone, 1971@@BEATE KLARSFELD",
  "two_photos#detalhe-centro",
  "old_young#médio-dir")
b("Beate viaja a Bolivia. En mil novecientos setenta y dos se encadena a un banco de una plaza de La Paz para exigir que lo entreguen.",
  "lapaz_square|A square in central La Paz in 1972 with colonial buildings, pigeons and passers-by in ponchos and suits",
  f"beate_chain|{BEATE} sitting on a park bench in La Paz with a chain around her wrist, holding a blank sign, passers-by looking" + SEM, card="LA PAZ, 1972")
b("El gobierno del general Hugo Banzer se niega.",
  "banzer|A Bolivian general in his late forties in a uniform without insignia at a desk, 1973, resembling Hugo Banzer" + NOINS + SEM)
b("Altmann sigue en La Paz, con su nombre falso y sus negocios.",
  f"altmann_interview|{ALTMANN.replace('1983', '1972')} being interviewed in his living room, a TV camera and a microphone in front of him" + SEM,
  "tv_camera|Close-up of a 1970s television camera with its red light on in a dim room" + SEM)
b("En mil novecientos ochenta, un golpe lleva al poder al general Luis García Meza. Según investigaciones periodísticas, Altmann ayudó a organizar a los paramilitares del golpe.",
  "coup_1980|Armed men in civilian clothes and soldiers in a street of La Paz in July 1980, smoke" + VIOL + NOINS,
  "paramilitary|A group of men in dark sunglasses and leather jackets beside a car in La Paz, 1980, seen from far away" + NOINS)
b("Pero en mil novecientos ochenta y dos, Bolivia vuelve a la democracia.",
  "democracy|A crowd celebrating with Bolivian people in a square in La Paz in October 1982, sunny, seen from above" + NOINS + SEM, ideia=True)

# ───────────────────────── 13. LA CELDA ─────────────────────────
cap("13. La Celda")
b("La Celda. Enero de mil novecientos ochenta y tres. El nuevo gobierno detiene a Altmann por la deuda.",
  "altmann_arrest#médio-dir",
  "debt_papers#detalhe-centro", card="LA PAZ, 1983")
b("El cuatro de febrero lo expulsa del país. Un avión lo deja en la Guayana Francesa. De ahí lo llevan a Lyon.",
  "plane_night#médio-esq",
  "plane_window|View through an airplane window of clouds and the dark Atlantic ocean below at dawn",
  "cayenne|A tropical airport runway in French Guiana with palm trees and a small terminal at night, 1983")
b("Vuelve a Montluc, la cárcel donde la Gestapo encerraba a sus víctimas en mil novecientos cuarenta y tres.",
  "montluc#detalhe-centro",
  "cell_door#médio-dir")
b("Ese mismo año, Estados Unidos reconoce que lo protegió y pide disculpas a Francia.",
  "report_1983#detalhe-centro")
b("Mayo de mil novecientos ochenta y siete. Juicio en Lyon. Durante semanas declaran sobrevivientes. El télex de Izieu está entre las pruebas.",
  "trial_lyon|A large French courtroom in 1987 with judges in red robes, lawyers in black robes and a packed public gallery" + SEM,
  "witness|An elderly woman testifying at a witness stand in a French courtroom in 1987, a microphone in front of her",
  "telex_strip#detalhe-alto", card="LYON, 1987")
b("El cuatro de julio, el tribunal lo condena a cadena perpetua por crímenes contra la humanidad. Muere bajo custodia en mil novecientos noventa y uno.",
  f"barbie_trial|{ALTMANN.replace('1983', '1987')} sitting in the dock of a French courtroom behind glass, expressionless" + SEM)
b("Bolivia lo tuvo treinta y dos años. Argentina tenía a otro.",
  "andes_road#detalhe-centro", ideia=True)

# ───────────────────────── 14. LA ENTREVISTA ─────────────────────────
cap("14. La Entrevista")
b("La Entrevista. San Carlos de Bariloche, Argentina, mil novecientos noventa y cuatro. Un equipo de la televisión estadounidense aborda en la calle a un anciano.",
  "bariloche|The mountain town of San Carlos de Bariloche in Argentina with Alpine-style wooden houses by a blue lake and snowy peaks, 1994",
  "tv_crew|A television crew with a camera and a boom microphone approaching an old man on a sidewalk of a mountain town, 1994" + SEM, card="BARILOCHE, 1994")
b("Es Erich Priebke, de ochenta años. Vive allí desde hace décadas. Preside la asociación del colegio alemán de la ciudad.",
  f"priebke|{PRIEBKE} in portrait, looking at the camera with mild surprise@@ERICH PRIEBKE",
  "school|A German-style school building with a pitched roof in Bariloche, children's coats on hooks by the door" + SEM)
b("En mil novecientos cuarenta y cuatro era capitán de la policía de seguridad de las SS en Roma. Su oficina, en la calle Tasso, era para los romanos la Gestapo.",
  "via_tasso|An apartment building in Rome in 1944 with shuttered windows, a black car at the door, a guard in a long coat" + NOINS + SEM,
  "rome_1944|A quiet street in Rome in 1944 with old ochre buildings, passers-by hurrying" + NOINS)
b("Ante la cámara admite que participó en la masacre de las Fosas Ardeatinas: trescientas treinta y cinco personas fusiladas como represalia.",
  "ardeatine|The entrance to old quarry caves in the countryside outside Rome, dark openings in the rock, 1944, no people",
  "microphone|Close-up of a television microphone held toward an old man's face, his mouth set hard, plain wall behind him, no signs" + SEM)
b("Argentina lo extradita a Italia en mil novecientos noventa y cinco. Lo condenan a cadena perpetua, que cumple en arresto domiciliario. Muere en Roma en dos mil trece, con cien años.",
  "plane_1995|A passenger airplane taking off from an airport with mountains behind, 1995, plain white fuselage with no airline name, no logo, no tail emblem, no lettering anywhere",
  "rome_window|An old man's silhouette behind the shutters of an apartment window in Rome, evening")
b("Hombres de la Gestapo vivieron décadas en Sudamérica. A uno, al final, lo sacaron de allí con una excusa: una deuda.",
  "coat_hook#médio-dir", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. La Deuda")
b("La Deuda. La Paz, mil novecientos ochenta y tres. A Klaus Altmann lo detuvieron por una deuda de diez mil dólares.",
  "lapaz_1983#aberto",
  "debt_papers#detalhe-alto", card="LA PAZ, 1983")
b("La deuda fue solo el pretexto. Lo que Francia juzgó fue Lyon. Fue Izieu.",
  "izieu#médio-dir", "montluc#aberto")
b("La Gestapo nunca tuvo muchos agentes. Tuvo vecinos que hablaban. Y después, gobiernos que miraron hacia otro lado.",
  "windows_watch#detalhe-centro", "coat_hook#aberto", ideia=True)
b("Y tú, ¿sabías que hombres de la Gestapo vivieron décadas en Sudamérica? ¿Cuál de estos expedientes te sorprendió más? Déjalo en los comentarios.",
  "folder_close|A hand closing a thick brown case file with a red circular stamp on a dark desk, lamp light" + SEM,
  "red_stamp#médio-esq", "andes_road#aberto")

# a 1ª prova do 001 (04/11) saiu com moldura de papel: todo prompt leva sangria explícita
SANGRIA = ", full-bleed illustration filling the entire frame edge to edge, no border, no margin, no white frame, no panel outline"

# Thumbs (EMBALAGEM.md aprovado no crivo r1): sobretudo de couro vazio no cabide, janela andina pequena, metade superior direita livre
# para "GESTAPO" e o sello "1983" (texto no código). Nada de pessoa, insígnia ou vermelho na base.
COAT_T = "a long black leather trench coat of a 1940s secret policeman with a belt and wide lapels, glossy highlights on the leather, hanging empty on a wooden coat hanger from a single iron hook on the wall, a dark fedora hat on the same hook"
THUMBS = [
    {"id": "thumb-A", "prompt": f"Ink graphic novel illustration: {COAT_T}, filling the LEFT half of the frame from top to bottom; to the right of the coat, in the lower right quarter, a small narrow window showing the snow-capped peak of the Illimani mountain and red brick rooftops of La Paz in daylight; the UPPER RIGHT part of the image is a plain empty pale beige paper-textured wall; muted slate blue shadows, absolutely no red color, no person, no blood" + NOINS + SEM},
    {"id": "thumb-B", "prompt": f"Ink graphic novel illustration: close view of {COAT_T}, the coat large and dominant on the LEFT 60% of the frame; the RIGHT side is a plain empty pale beige paper-textured wall with, near the bottom right corner, a small window with the snowy Andes mountains; strong side light, deep black leather against pale wall, absolutely no red color, no person, no blood" + NOINS + SEM},
    {"id": "thumb-C", "prompt": f"Ink graphic novel illustration: {COAT_T}, on the LEFT half of the frame, beside a tall window in late afternoon light showing a steep street of La Paz, Bolivia, with colonial balconies and the snowy Illimani mountain far behind; the UPPER RIGHT part of the image is plain empty pale beige wall; muted slate blue and sepia, absolutely no red color, no person, no blood" + NOINS + SEM},
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
