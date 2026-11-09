#!/usr/bin/env python3
"""Fonte única do dossie-es 005 (KGB): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (na pasta do vídeo). Conteúdo no topo; geração no fim (copiada do 004-cosa-nostra).

Molde da bíblia (canais/dossie-es/biblia/roteiro.md): hook por anedota (o guarda-chuva de Georgi Markov, Londres, 1978; Te lo
Pinto abre com a fundação de 1917 e Atlas del Tiempo com Putin em Dresden, ambos transcritos em ref/) → 14 expedientes-objeto
com título falado → pagamento da anedota no expediente 11 ("El Paraguas") → cierre que volta à bolita + aforismo + pergunta.
Recorte 1917–1992; FSB em 1 frase neutra (brief). Factual, atribuído, sem glamourizar: vítimas com nome (Trotski, Markov,
os fuzilados de 1937–38, Sájarov).
Ângulo América Latina: Trotski e Mercader em Coyoacán (1940), Mercader morre em La Habana (1978), Feklisov e Cuba (1962),
Oswald na embaixada soviética da Cidade do México (1963), Allende no arquivo Mitrokhin (1970). Liga com CIA, FBI (Abel,
moeda oca) e Mossad (sessão). Fatos conferidos em 09/11/2026 (ver SOURCES.md).

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (id I### na ordem de aparição) · "chave" reuso · "chave#enq" reuso com enquadramento
  + "@@TEXTO"      rótulo na tela (máquina de escrever; CAIXA ALTA, até ~28 caracteres)
Bloco: b(texto, *planos, card="LONDRES, 1978", ideia=True) · capítulo: cap("5. La Bomba")
Mapas (chave map_*): base sem texto nem pinos; pinos, setas e nomes no código (src/labels.jsx).
"""
import json, math, re
from pathlib import Path

WPS = 2.38           # palavras/s medidas no 001–004 (erro de 1–3%)
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
TITULO = "TODA la historia de la KGB"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# Personagens (descrição visual fixa; rostos "resembling", nunca foto)
MARKOV = "a Bulgarian writer in his late forties with thick dark hair combed back, a broad tired face, a dark raincoat, 1978"
DZERZH = "a gaunt Polish revolutionary in his forties resembling Felix Dzerzhinsky, a pointed goatee and mustache, sunken cheeks, a long plain greatcoat without insignia, 1917"
LENIN = "a bald Russian revolutionary leader in his late forties resembling Lenin, a reddish goatee and mustache, a dark three-piece suit"
STALIN = "a Soviet leader in his late fifties resembling Stalin, thick grey hair, a thick mustache, a plain grey tunic without medals"
YEZHOV = "a very short thin Soviet official in his forties with dark hair and a narrow face, a plain military tunic without insignia, 1937"
BERIA = "a balding heavy Soviet official in his fifties resembling Lavrentiy Beria, round pince-nez glasses, a dark coat, 1953"
TROTSKY = "an elderly man of sixty resembling Leon Trotsky, wild white hair, a white goatee, round glasses, a light shirt, 1940"
MERCADER = "a dark-haired Spanish man in his late twenties with slicked-back hair and a thin face, a light raincoat, 1940"
FUCHS = "a thin German-born physicist in his thirties with round glasses, a high forehead and receding dark hair, a plain 1945 suit"
ABEL = "a thin balding man in his mid fifties with a long narrow face and a calm look, a worn jacket, an amateur painter's studio, 1957"
POWERS = "an American pilot in his early thirties with short dark hair and a square face, a winter coat, 1962"
FEKLISOV = "a heavyset Soviet diplomat in his late forties with thinning hair combed back and a round face, a dark suit and tie, 1962"
SCALI = "an American television journalist in his forties with dark hair and glasses, a grey suit, 1962"
OSWALD = "a thin young American man of twenty-three with receding brown hair and a narrow face, a plain shirt and dark slacks, 1963"
NECHIP = "a young Soviet diplomat in his early thirties with short dark hair, a dark suit, a serious face, 1963"
ANDROPOV = "a tall Soviet official in his fifties resembling Yuri Andropov, thinning swept-back grey hair, rimless glasses, a dark suit"
SAKHAROV = "an elderly balding Soviet physicist resembling Andrei Sakharov, a high forehead, glasses, a worn cardigan, 1980"
GORDIEVSKY = "a fit Soviet man in his mid forties with short brown hair and a square face, 1985"
KRYUCHKOV = "a Soviet official in his late sixties with grey hair, large glasses and a stern face, a dark suit, 1991"
MITROKHIN = "a quiet grey-haired Russian man around seventy with glasses and a lined face, a worn coat, 1992"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, borders and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame"

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Londres, septiembre de mil novecientos setenta y ocho. Un hombre espera el autobús junto al puente de Waterloo.",
  "london_78|London in September 1978 seen from the south bank of the Thames at dusk, Waterloo Bridge, red double-decker buses, grey sky",
  "bus_stop|A bus stop at the south end of Waterloo Bridge in 1978, commuters in raincoats waiting in the evening, grey light",
  f"markov_wait|{MARKOV} standing at a London bus stop with his hands in his pockets, looking at the traffic", card="LONDRES, 1978")
b("Siente un pinchazo en el muslo. Detrás, un desconocido recoge un paraguas y se sube a un taxi.",
  "sting|Close-up of a man's leg in dark trousers at a bus stop, the metal tip of a black closed umbrella touching the back of his thigh",
  "umbrella_pick|A man in a dark overcoat and hat seen from behind bending to pick up a black umbrella from the pavement on a London bridge, 1978",
  "taxi_away|A black London taxi pulling away from the curb on Waterloo Bridge at dusk, a man in a hat inside, seen from behind")
b("Cuatro días después, Georgi Markov está muerto. En su muslo hay una bolita de metal de menos de dos milímetros.",
  "hospital_78|An empty hospital bed in a London hospital ward in 1978, a drip stand, cold light from a window, no person",
  f"markov_face|{MARKOV} in portrait, serious face, a dim London street behind him@@GEORGI MARKOV",
  "pellet|Extreme close-up of a tiny metal sphere smaller than a pinhead on the tip of a fingertip in a forensic laboratory, cold light",
  "forensic_lab|A 1978 British forensic laboratory, a scientist in a white coat looking through a microscope, glass jars and lamps")
b("Esta es TODA la historia de la KGB. Y de cómo aprendió a alcanzar a sus enemigos en cualquier lugar del mundo.",
  "files_desk|A long dark desk covered with open brown case files and black and white photographs, a red stamp and a magnifying glass",
  "red_stamp|A hand slamming a red rubber stamp onto a brown paper case file, ink splash, dramatic close-up",
  "moscow_snow|A snowy Moscow street at night with a man in a fur hat walking alone past a lit government building, 1970s",
  "lubyanka_night|The massive yellow stone Lubyanka building in Moscow at night under snow, a few lit windows, an empty square, seen from far away", ideia=True)

# ───────────────────────── 1. LA COMISIÓN ─────────────────────────
cap("1. La Comisión")
b("La Comisión. Petrogrado, veinte de diciembre de mil novecientos diecisiete. Lenin lleva seis semanas en el poder y teme perderlo.",
  "petrograd_17|Petrograd in December 1917, a snowy street along a frozen canal, armed workers and sailors around a bonfire, red banners without text",
  "smolny|The Smolny Institute in Petrograd at night in December 1917, lit windows, armored cars and sentries in the snow",
  f"lenin_desk|{LENIN} at a desk covered with papers in a bare office lit by a lamp, a worried look, 1917", card="PETROGRADO, 1917")
b("Hay huelgas, sabotajes y oficiales del zar que conspiran. Así que crea una Comisión Extraordinaria. Por sus iniciales en ruso, la llaman Cheká.",
  "strike_17|Striking clerks in coats standing outside a closed government ministry in Petrograd in 1917, snow, soldiers watching",
  "tsar_officers|Three former Tsarist officers in greatcoats without insignia whispering in a dark Petrograd apartment, candle light",
  "leather_jacket|Close-up of a Cheka agent in a black leather jacket and a peaked cap loading papers into a satchel, lamp light, 1917",
  "cheka_door|A heavy wooden door of an office in Petrograd in 1917 with a sentry in a leather jacket and a rifle slung pointing down@@CHEKÁ")
b("La dirige Félix Dzerzhinski, un noble polaco que pasó más de diez años entre cárceles, trabajos forzados y destierro. Al principio, tiene unas pocas decenas de hombres.",
  f"dzerzh|{DZERZH} standing in a bare office in Petrograd, cold stare@@FÉLIX DZERZHINSKI",
  "siberia_exile|A line of political prisoners in chains walking through a snowy Siberian landscape in the early 1900s, guards on horseback, seen from far away",
  "typewriter_17|An old typewriter on a cluttered desk in 1917 with a stack of arrest warrants and a revolver in its holster, lamp light, unreadable",
  "few_men|About twenty men in leather jackets and greatcoats crowded in a small smoky office in 1917 Petrograd, a single lamp, papers everywhere")
b("Treinta de agosto de mil novecientos dieciocho. Lenin recibe dos disparos a la salida de una fábrica en Moscú. Sobrevive.",
  "factory_18|The courtyard of a Moscow factory in August 1918, a crowd of workers around a black car, seen from far away, no blood@@30 DE AGOSTO DE 1918",
  "car_18|A black 1918 car speeding through a Moscow street, passers-by turning their heads",
  "lenin_bed|a bald man with a goatee lying in a bed with a bandaged shoulder, doctors in white around him, Kremlin room, 1918",
  "kaplan|A young woman with dark hair and a pale face in a plain dark dress being held by two armed men in a factory yard, 1918")
b("Días después, un decreto lleva un nombre oficial: Terror Rojo. La Cheká puede detener y fusilar sin juicio. En pocos años, con sus tropas, suma más de doscientos mil hombres.",
  "decree|A 1918 printed decree pasted on a wall in Moscow, a crowd reading it in silence, the text made of unreadable shapes@@\"TERROR ROJO\"",
  "night_arrest|Men in leather jackets leading a man in a nightshirt out of an apartment building at night in 1918, a truck waiting, seen from far away",
  "execution_yard|An empty courtyard with a brick wall at dawn in 1918 Moscow, fresh snow, footprints, no people, no blood",
  "cheka_crowd|Rows of Cheka agents in leather jackets and caps in a large hall in 1920, seen from behind, a red banner without text", ideia=True)

# ───────────────────────── 2. EL EDIFICIO ─────────────────────────
cap("2. El Edificio")
b("El Edificio. Mil novecientos dieciocho. El gobierno se muda a Moscú, y la Cheká se instala en la plaza Lubianka, en la sede de una compañía de seguros.",
  "lubyanka_day|The large yellow brick Lubyanka building with a clock on the facade in Moscow around 1920, trams and horse carts in the square",
  "moscow_18|Moscow in 1918, the Kremlin walls and onion domes in winter, people in fur hats crossing a snowy street",
  "trucks_files|Horse carts and trucks unloading crates of documents in front of a grand building in Moscow, 1918",
  "insurance_hall|The grand marble entrance hall of a former insurance company in Moscow in 1918, now full of armed men and crates of files", card="MOSCÚ, 1918")
b("Su nombre se vuelve sinónimo del organismo. Lubianka significa interrogatorios, celdas y gente que entra y no vuelve a salir.",
  "corridor|A long dim basement corridor with heavy iron cell doors in the Lubyanka, a single bulb, a guard at the far end",
  "interrogation|A bare interrogation room in the 1920s, a lamp pointed at an empty chair, a man in a uniform smoking behind a desk",
  "cell_door|Close-up of a heavy iron cell door with a small peephole and a number painted on it, cold light",
  "night_window|A woman in a shawl standing at night in the snowy square looking up at the lit windows of the Lubyanka building")
b("En Moscú circula un chiste: es el edificio más alto de la ciudad, porque desde el sótano ya se ve Siberia.",
  "whisper|Two Muscovite men in fur hats whispering on a snowy street corner and glancing over their shoulders, 1930s",
  "joke_laugh|Two men laughing nervously over glasses of tea at a kitchen table in a 1930s Moscow apartment, a radio on a shelf",
  "siberia_view|A frozen endless Siberian plain with a distant line of barbed wire and watchtowers under a grey sky")
b("La Cheká cambia de nombre: GPU, OGPU y, en mil novecientos treinta y cuatro, NKVD. Las siglas cambian. El edificio, no.",
  "signs_change|Workers on ladders replacing a plaque on a grand stone doorway in Moscow, three blank plaques leaning against the wall@@CHEKÁ · GPU · NKVD",
  "nkvd_officers|NKVD officers in tunics and blue-topped caps walking out of a grand doorway in 1930s Moscow, seen from far away",
  "lubyanka_30s|The Lubyanka building in Moscow in the 1930s at dusk, black cars parked in front, a guard at the door")
b("Y en mil novecientos treinta y siete, el Kremlin le pide algo nuevo: números.",
  f"stalin_desk|{STALIN} reading a typed list at a desk in a dark wood-paneled office, a green lamp, a pipe in an ashtray",
  "kremlin_37|The Kremlin towers in Moscow at night in 1937, a single lit window in a building inside the walls, snow",
  "typed_list|Close-up of a typed list of numbers in columns on a sheet of paper under a desk lamp, a red pencil, unreadable", ideia=True)

# ───────────────────────── 3. LA CUOTA ─────────────────────────
cap("3. La Cuota")
b("La Cuota. Treinta de julio de mil novecientos treinta y siete. El jefe del NKVD, Nikolái Yezhov, firma la orden número cero cero cuatro cuatro siete.",
  f"yezhov|{YEZHOV} signing a document with a fountain pen at a large desk, cold lamp light@@NIKOLÁI YEZHOV",
  "nkvd_hq_37|A long corridor of the NKVD headquarters in 1937 with officers carrying files, tall doors, cold electric light",
  "signature|Extreme close-up of a fountain pen signing at the bottom of a typed document, a red pencil line, unreadable",
  "order_doc|An official typed Soviet document with a stamp and a signature on a desk, the text made of unreadable shapes@@ORDEN Nº 00447", card="MOSCÚ, 1937")
b("No investiga ningún delito. Reparte cifras. Cada región recibe un número de personas que fusilar y otro que enviar a los campos de trabajo.",
  "quota_table|A large table of handwritten numbers in columns pinned to a wall in a Soviet office, a man in a tunic pointing at it, unreadable",
  "regional_office|A provincial NKVD office in 1937, officers in tunics reading telegrams at desks, a portrait frame on the wall without a face visible",
  "gulag_train|A long freight train of wooden boxcars crossing a snowy plain at dawn in 1937, guards on the roof, seen from far away")
b("En la primera tabla hay casi setenta y seis mil fusilamientos. Muchas regiones piden que les suban la cuota.",
  "telegram|A Soviet telegram form on a desk being stamped, a hand writing a number with a pencil, unreadable@@75.950",
  "wall_map_ussr|A large wall map of the Soviet Union in an office with small paper tags pinned on regions, an officer standing in front, 1937, no legible text",
  "officer_phone|A Soviet NKVD officer in a tunic talking on a black telephone in a dark office at night, a pile of files")
b("Entre mil novecientos treinta y siete y mil novecientos treinta y ocho, los registros soviéticos cuentan unas seiscientas ochenta mil ejecuciones. Es el Gran Terror.",
  "empty_chairs|Wide interior shot of a communal apartment kitchen in 1937 Moscow at dawn, a table with several empty chairs and untouched cups of tea, the scene fills the whole image",
  "truck_night|A closed black van driving through an empty Moscow street at night in 1937, snow falling, seen from far away@@1937–1938",
  "photo_wall|A wall covered with small black and white identity photographs of ordinary men and women, faded, a single candle below")
b("Y el terror devora a quien lo dirige. Yezhov es apartado, arrestado y fusilado. Su lugar lo ocupa Lavrenti Beria.",
  "yezhov_erased|A black and white group photograph on a table, one small man in it scratched out with ink, a magnifying glass",
  "yezhov_arrest|a very short thin man in a tunic being led down a corridor by two guards, 1939, seen from behind",
  f"beria|{BERIA} standing in a dark office looking at the viewer, a cold faint smile@@LAVRENTI BERIA")
b("Pero Stalin todavía tiene un enemigo vivo. Al otro lado del océano.",
  "trotsky_letters|Stacks of letters and newspapers on a desk in a sunny Mexican study, a typewriter, a pair of round glasses, 1940",
  "ocean_ship|A steamship crossing a dark Atlantic Ocean at night in 1940, a single light on deck, seen from far away", ideia=True)

# ───────────────────────── 4. EL PIOLET ─────────────────────────
cap("4. El Piolet")
b("El Piolet. Coyoacán, Ciudad de México, mil novecientos cuarenta. León Trotski, el gran rival de Stalin, vive exiliado en una casa de muros altos.",
  "coyoacan|A quiet street in Coyoacán, Mexico City in 1940, a house with high walls and a watchtower, jacaranda trees, dusty sunlight",
  f"trotsky|{TROTSKY} feeding rabbits in a garden with cactus inside high walls, Mexico 1940@@LEÓN TROTSKI",
  "guards_mx|Two young guards with rifles slung pointing down on a brick watchtower above a high wall in Mexico City, 1940", card="COYOACÁN, MÉXICO, 1940")
b("En mayo, un comando armado ametralla su dormitorio de madrugada. Lo encabeza el pintor David Alfaro Siqueiros. Trotski y su esposa se salvan tirándose al suelo.",
  "raid_night|Armed men in police-style uniforms climbing out of cars in front of a walled house at night in Mexico 1940, seen from far away",
  "bullet_wall|A bedroom wall riddled with bullet holes at night, a bed and a toppled lamp, moonlight through a window, no people",
  "siqueiros|A Mexican painter in his forties with dark curly hair and a strong jaw, in a dark coat, a painter's studio with large murals@@DAVID ALFARO SIQUEIROS")
b("Veinte de agosto. Un visitante conocido de la casa, novio de una militante trotskista estadounidense, le pide que revise un artículo.",
  f"mercader|{MERCADER} walking through a garden gate with a raincoat over his arm on a sunny afternoon, 1940",
  f"study|{TROTSKY} reading typed pages at a desk in a book-lined study, a man in a raincoat standing behind him, 1940", card="20 DE AGOSTO DE 1940")
b("Mientras Trotski lee, el hombre saca de su gabardina un piolet de alpinista y lo golpea en la cabeza. Trotski muere al día siguiente.",
  "ice_axe|Close-up of the steel head of a mountaineering ice axe half hidden under a folded raincoat, desk lamp light",
  "study_after|An empty book-lined study with scattered papers on the floor and an overturned chair, afternoon light, no blood, no body",
  "ambulance_mx|A 1940 ambulance and a crowd of people outside a walled house in Coyoacán, seen from far away")
b("El asesino es Ramón Mercader, un comunista español reclutado por el NKVD. Pasa veinte años preso en México. Al salir, Moscú lo condecora como Héroe de la Unión Soviética.",
  f"mercader_jail|{MERCADER} older, in his forties, sitting in a Mexican prison cell with a book, barred window@@RAMÓN MERCADER",
  "mx_trial|A crowded Mexican courtroom in 1943, a dark-haired young man in a suit standing silent before the judge, reporters taking notes",
  "medal|Close-up of a gold star medal on a red ribbon in an open velvet box on a dark table")
b("Muere en La Habana, en mil novecientos setenta y ocho. El mismo año del paraguas de Londres.",
  "havana_78|Havana in 1978 at dusk, the Malecón seawall with waves, old American cars and faded colonial buildings",
  "umbrella_closeup|A closed black umbrella leaning against a stone wall on a wet London street at night, lamp light", ideia=True)

# ───────────────────────── 5. LA BOMBA ─────────────────────────
cap("5. La Bomba")
b("La Bomba. En la Segunda Guerra Mundial, el mayor secreto del planeta es estadounidense: la bomba atómica.",
  "los_alamos|Los Alamos laboratory in the New Mexico desert in 1945, wooden barracks, mesas and pine trees, a water tower",
  "trinity|A distant mushroom cloud rising over a flat desert at dawn in 1945, seen from very far away", card="LOS ÁLAMOS, 1945")
b("La inteligencia soviética entra desde dentro. Klaus Fuchs, un físico de Los Álamos nacido en Alemania, pasa a Moscú detalles de la bomba de plutonio.",
  f"fuchs|{FUCHS} at a blackboard covered with equations in a wooden laboratory hut, 1945@@KLAUS FUCHS",
  f"fuchs_hand|{FUCHS} handing a thick envelope to a man in a hat on a bridge in Santa Fe, New Mexico, at dusk, seen from far away")
b("Veintinueve de agosto de mil novecientos cuarenta y nueve. En Kazajistán, la Unión Soviética detona su primera bomba atómica, años antes de lo que esperaba Washington.",
  "steppe_test|A tall steel tower on an empty Kazakh steppe at dawn in 1949, a distant bright flash on the horizon, seen from very far away@@29 DE AGOSTO DE 1949",
  "kurchatov|A bearded Soviet nuclear physicist in his forties with a long black beard in a control bunker, looking through a narrow window, 1949",
  "washington_49|A worried American official reading a report at a desk in a Washington office in 1949, the Capitol dome through the window")
b("Su diseño se parece mucho al de la bomba de Nagasaki. El espionaje no ganó la carrera solo, pero les ahorró tiempo.",
  "blueprints|Two sets of technical blueprints of a round device laid side by side on a table, lamp light, no legible text",
  "soviet_physicists|Soviet physicists in suits around a table with papers and a chalkboard in a Soviet laboratory in 1948")
b("Y el hombre que supervisa ese proyecto atómico es el mismo que manda en la policía secreta: Beria.",
  "beria#médio-dir", ideia=True)

# ───────────────────────── 6. EL ESCUDO ─────────────────────────
cap("6. El Escudo")
b("El Escudo. Marzo de mil novecientos cincuenta y tres. Muere Stalin. Beria controla la policía secreta y parece su heredero. Los demás líderes le tienen miedo.",
  "stalin_funeral|A huge silent crowd in dark coats in a snowy Moscow street in March 1953, black mourning flags without emblems, seen from far away",
  f"beria_kremlin|{BERIA} walking alone through a long Kremlin corridor with red carpet, other officials stepping aside", card="MOSCÚ, 1953")
b("En junio, en una reunión en el Kremlin, sus propios colegas lo arrestan. En diciembre, lo fusilan.",
  "kremlin_meeting|A long table in a Kremlin meeting room in 1953, Soviet leaders in dark suits standing up, a general entering through a door",
  "beria_glasses|A pair of round pince-nez glasses lying on an empty chair in a dark room, a single beam of light")
b("Para que nadie vuelva a acumular tanto poder, la policía secreta queda bajo la vigilancia del Partido.",
  "khrushchev|A bald stocky Soviet leader in his late fifties in a dark suit speaking at a podium in a grand hall, 1954, no flags with emblems",
  "party_hall|A grand Soviet party congress hall in the 1950s with rows of delegates, seen from the back, a stage far away, no flags with emblems")
b("Trece de marzo de mil novecientos cincuenta y cuatro. Nace un nombre nuevo: Comité de Seguridad del Estado. En ruso, KGB.",
  "kgb_folder|A plain blank brown paper case file without any writing on a dark desk being opened by a hand, a red stamp beside it, lamp light, no lettering anywhere@@13 DE MARZO DE 1954",
  "lubyanka_54|The Lubyanka building in Moscow in 1954 in winter sunlight, black Pobeda cars in front, people hurrying past")
b("Su emblema: un escudo y una espada. Y para entonces, sus espías ya viven en Estados Unidos como vecinos cualquiera.",
  "shield_sword|A large metal emblem of a plain shield with a vertical sword on a dark stone wall, no letters, no star, dramatic light",
  "suburb_50s|A quiet street of brownstone houses in Brooklyn in the 1950s, a man in a hat walking a dog", ideia=True)

# ───────────────────────── 7. LA MONEDA ─────────────────────────
cap("7. La Moneda")
b("La Moneda. Brooklyn, mil novecientos cincuenta y tres. Un repartidor de periódicos recibe una moneda de cinco centavos. Se le cae y se parte en dos.",
  "newsboy|A teenage American newspaper delivery boy in a cap counting coins on the stairs of a Brooklyn apartment building in 1953",
  "brooklyn_stairs|The stone front stairs of a Brooklyn apartment building in 1953 in summer, a coin glinting on a step",
  "coin_split|Extreme close-up of a small nickel coin split open in two halves on a stone step, a tiny rolled film inside", card="NUEVA YORK, 1953")
b("Es hueca. Dentro hay un microfilm con columnas de números. El FBI tarda cuatro años en saber de quién es.",
  "microfilm|A tiny strip of microfilm under a magnifying glass showing columns of tiny numbers, laboratory light",
  "fbi_lab|FBI cryptographers in shirtsleeves working at desks with papers and adding machines in a 1950s office")
b("En mil novecientos cincuenta y siete, un espía soviético entra en la embajada estadounidense de París y se entrega. Y lleva al FBI hasta un pintor aficionado de Brooklyn.",
  "defector|A nervous man in a raincoat walking into an American embassy in Paris in 1957, a Marine guard at the door",
  "hotel_latham|A shabby 1950s New York hotel corridor at dawn, two FBI agents in hats knocking on a door",
  f"abel_studio|{ABEL} painting at an easel in a cluttered Brooklyn studio full of canvases, 1957")
b("Es un coronel de la KGB que se hace llamar Rudolf Abel. Lo condenan a treinta años de cárcel.",
  f"abel_arrest|{ABEL} in a hotel room being handcuffed by two FBI agents in hats, 1957@@RUDOLF ABEL",
  "courtroom_57|A 1957 American federal courtroom with wood panels, a judge at the bench, a thin man standing beside his lawyer")
b("Pero en mil novecientos sesenta y dos, en un puente de Berlín, lo cambian por un piloto estadounidense derribado sobre la Unión Soviética: Francis Gary Powers.",
  "glienicke|A steel bridge over a frozen river near Berlin at dawn in February 1962, two groups of men in coats facing each other in the middle, seen from far away@@BERLÍN, 1962",
  f"powers|{POWERS} walking across a bridge in the winter fog@@FRANCIS GARY POWERS")
b("Ese mismo año, la Guerra Fría llega a una isla del Caribe.",
  "cuba_coast|The coast of Cuba seen from the sea in 1962, palm trees and green hills, a grey warship on the horizon", ideia=True)

# ───────────────────────── 8. EL ALMUERZO ─────────────────────────
cap("8. El Almuerzo")
b("El Almuerzo. Octubre de mil novecientos sesenta y dos. Estados Unidos descubre misiles nucleares soviéticos en Cuba. El mundo está al borde de una guerra nuclear.",
  "missile_photo|An aerial reconnaissance photograph of a missile site in a Cuban jungle clearing, trucks and long tubes, seen from high above, black and white",
  "kennedy_room|A tense meeting of American officials in suits around a long table in the White House in October 1962, photographs spread on the table",
  "tv_crowd|A crowd of Americans watching a television in a shop window in October 1962, worried faces", card="WASHINGTON, 1962")
b("El viernes veintiséis, el jefe de la KGB en Washington, Alexandr Feklisov, invita a almorzar a un periodista de la televisión estadounidense, John Scali.",
  "restaurant|A busy classic Washington restaurant in 1962 with wood panels and framed pictures, two men at a corner table",
  f"feklisov|{FEKLISOV} at a restaurant table leaning forward and speaking quietly@@ALEXANDR FEKLISOV",
  f"scali|{SCALI} listening at a restaurant table, writing on a small notepad@@JOHN SCALI")
b("Le plantea una salida: Moscú retira los misiles y Washington promete no invadir Cuba. Esa misma tarde, Scali lo cuenta en el Departamento de Estado.",
  "napkin|Close-up of a paper napkin on a restaurant table with a pencil, two coffee cups, the writing made of unreadable shapes",
  "state_dept|An American official in shirtsleeves listening to a journalist in a Washington office at dusk, 1962")
b("Todavía se discute si hablaba por orden de Moscú o por su cuenta. Pero el acuerdo final se parece mucho a lo que dijo en esa mesa.",
  "relief|A man in a suit exhaling with relief beside a radio in a Washington office in 1962, evening light",
  "ships_turn|Soviet cargo ships with long canvas-covered cargo on deck sailing away on a calm sea, an American destroyer following at a distance")
b("En Cuba, mientras tanto, la KGB ya tiene un aliado. Según historiadores del espionaje, ayudó a formar y entrenar a los servicios de inteligencia de Fidel Castro.",
  "havana_62|Havana in 1962, a busy street with old cars, militia members in olive uniforms, colonial buildings",
  "training|Young Cuban men in olive uniforms taking notes in a classroom while a Soviet instructor in a suit points at a blackboard, 1962")
b("Un año después, la KGB recibe en México a un visitante inesperado.",
  "mexico_city|Mexico City in 1963 seen from a rooftop, the Paseo de la Reforma, old cars and jacaranda trees", ideia=True)

# ───────────────────────── 9. LA EMBAJADA ─────────────────────────
cap("9. La Embajada")
b("La Embajada. Ciudad de México, finales de septiembre de mil novecientos sesenta y tres. Un joven estadounidense entra en la embajada soviética y pide una visa urgente.",
  "embassy_mx|The gate of a large walled embassy compound in Mexico City in 1963, a guard booth, trees, afternoon light",
  f"oswald|{OSWALD} standing at a reception desk in an embassy, nervous, holding papers", card="CIUDAD DE MÉXICO, 1963")
b("Lo reciben oficiales de la KGB con cargo de diplomáticos. Uno de ellos, Oleg Nechiporenko, contará después que el joven estaba alterado y que puso un revólver sobre la mesa.",
  f"nechip|{NECHIP} sitting behind a desk in a small office, watching carefully@@OLEG NECHIPORENKO",
  "embassy_office|A small embassy office in Mexico City in 1963, a desk, a portrait frame without a visible face, venetian blinds, afternoon light",
  "revolver_table|A small revolver lying on a wooden office desk next to a passport, two hands in the frame, tense, no blood")
b("No le dan la visa. Se llama Lee Harvey Oswald. Ocho semanas después, en Dallas, es detenido por el asesinato del presidente John F. Kennedy.",
  f"oswald_leave|{OSWALD} walking out of an embassy gate onto a sunny street, seen from behind@@LEE HARVEY OSWALD",
  "dallas|Dealey Plaza in Dallas in November 1963 seen from far away, a tall brick book depository building, empty lawns, no people, no cars")
b("La CIA vigilaba esa embajada con cámaras ocultas. Ninguna investigación oficial encontró pruebas de que la KGB participara en el asesinato.",
  "cia_camera|A hidden camera with a long lens behind a curtain in an apartment window across the street from an embassy, 1963",
  "files_jfk|A stack of thick government report volumes on a library table, lamp light, no legible text", ideia=True)

# ───────────────────────── 10. EL HOSPITAL ─────────────────────────
cap("10. El Hospital")
b("El Hospital. Mil novecientos sesenta y siete. Yuri Andrópov se convierte en jefe de la KGB. Lo será durante quince años, más que nadie.",
  f"andropov|{ANDROPOV} at a long desk in a dark office, hands folded, watching@@YURI ANDRÓPOV",
  "kgb_office|A large dark Soviet office in 1967 with a long conference table, heavy curtains and a row of telephones", card="MOSCÚ, 1967")
b("Once años antes, como embajador en Budapest, vio cómo los tanques soviéticos aplastaban la revolución húngara. Según sus biógrafos, aprendió una lección: la disidencia hay que cortarla pronto.",
  "budapest_56|Soviet tanks in a smoky street of Budapest in November 1956, damaged buildings, seen from far away, no bodies",
  f"andropov_window|{ANDROPOV} younger, in his early forties, watching from an embassy window at night, smoke outside, 1956")
b("Crea un departamento solo para eso, la Quinta Dirección. Y la KGB recurre cada vez más a un arma: el diagnóstico.",
  "fifth_dir|Rows of filing cabinets and officers at desks reading intercepted letters in a Soviet office, 1970s",
  "diagnosis|Close-up of a doctor's hand signing a medical form with a fountain pen, a rubber stamp beside it, unreadable")
b("Hay disidentes que terminan en hospitales psiquiátricos, diagnosticados con esquizofrenia lenta, una enfermedad que casi solo existía en la Unión Soviética. Según los propios disidentes, a menudo el único síntoma era disentir.",
  "psych_ward|A grim Soviet psychiatric hospital ward in the 1970s, iron beds in a row, barred windows, a man sitting on a bed staring",
  "injection|Close-up of a nurse preparing a syringe on a metal tray in a grim Soviet hospital in the 1970s, cold light",
  "psych_building|A grey psychiatric hospital building behind a tall fence in winter, 1970s Soviet Union, medium distance, the scene fills the whole image")
b("Ni la fama protege. En mil novecientos ochenta, Andréi Sájarov, padre de la bomba de hidrógeno soviética y Nobel de la Paz, es desterrado a Gorki, una ciudad cerrada.",
  f"sakharov|{SAKHAROV} sitting at a small kitchen table in a plain apartment, a guard visible through the window@@ANDRÉI SÁJAROV",
  "gorky|A grey Soviet city of apartment blocks by a wide frozen river in 1980, a black car parked in front of one building")
b("Pero contra los enemigos que viven en Occidente, la KGB tiene otros métodos.",
  "umbrella_closeup#detalhe-centro", ideia=True)
b("Si te gustan estos expedientes, suscríbete. Y ahora, volvemos al puente de Waterloo.",
  "london_78#médio-esq", ideia=True)

# ───────────────────────── 11. EL PARAGUAS ─────────────────────────
cap("11. El Paraguas")
b("El Paraguas. Georgi Markov era un escritor búlgaro exiliado en Londres. En la BBC y en Radio Europa Libre se burlaba del dictador de Bulgaria, Todor Zhivkov.",
  f"markov_bbc|{MARKOV} speaking into a microphone in a 1970s radio studio, headphones, a red on-air light",
  "radio_mic|A vintage radio studio microphone in a dark booth with a blank red warning lamp glowing, 1978, no lettering anywhere",
  "zhivkov|A Bulgarian communist leader in his sixties with grey hair and a round face, a dark suit, on a podium, 1978@@TODOR ZHIVKOV", card="PUENTE DE WATERLOO, 1978")
b("La bolita de su muslo tenía dos agujeros diminutos. Los forenses británicos no hallaron rastro del veneno, pero concluyeron que probablemente era ricina, un veneno sin antídoto.",
  "pellet_holes|Extreme macro close-up of a tiny metal sphere with two microscopic drilled holes, on a glass slide, cold light",
  "porton|British scientists in white coats examining samples in a 1978 government laboratory, glass equipment@@RICINA")
b("Según los investigadores, la operación fue del servicio secreto búlgaro. Y el exgeneral de la KGB Oleg Kalugin afirmó después que Andrópov aprobó la ayuda y que el veneno salió de un laboratorio de la KGB.",
  "sofia|Sofia, Bulgaria, in 1978, a grey government building with columns, a black car in front, seen from far away",
  "kalugin|A Soviet KGB general in his forties with a sharp face and dark hair, in a dark civilian suit, 1978@@OLEG KALUGIN",
  "poison_lab|A secret Soviet laboratory in the 1970s, a technician in a white coat handling a tiny vial with tweezers under a lamp")
b("Menos de dos semanas antes, en el metro de París, otro exiliado búlgaro, Vladimir Kostov, había sentido el mismo pinchazo. Sobrevivió.",
  "paris_metro|A crowded Paris metro station escalator in August 1978, a man in a suit turning around, surprised")
b("Nadie fue condenado jamás.",
  "bridge_empty|Waterloo Bridge in London on a rainy night, an empty bus stop, a closed black umbrella left on the pavement", ideia=True)
b("La KGB era temida en Occidente. Pero algunos de sus enemigos más peligrosos estaban dentro.",
  "kgb_folder#detalhe-centro", ideia=True)

# ───────────────────────── 12. LA BOLSA ─────────────────────────
cap("12. La Bolsa")
b("La Bolsa. Mayo de mil novecientos ochenta y cinco. Oleg Gordievski, coronel de la KGB en Londres, lleva once años trabajando en secreto para el MI6 británico. Y lo llaman a Moscú.",
  f"gordievsky|{GORDIEVSKY} in a dark suit in a London office, reading a telegram with a worried face@@OLEG GORDIEVSKI",
  "london_embassy|The Soviet embassy in London on a grey day in 1985, a tall stately building behind a fence, seen from across the street",
  "aeroflot|A plain white airliner without any logo, lettering or flag on a wet tarmac in May 1985, a man in a coat climbing the stairs, seen from far away, no lettering anywhere", card="MOSCÚ, 1985")
b("Allí lo drogan y lo interrogan. Sospechan de él, pero todavía no tienen pruebas.",
  "dacha|A wooden Soviet dacha in a birch forest in summer 1985, a black Volga car in front",
  "brandy|Two glasses of brandy on a table in a dark room, a man slumped in a chair in the background, out of focus")
b("Una tarde de julio, se queda quieto en una esquina de Moscú con una bolsa de un supermercado británico. Un agente británico pasa a su lado comiendo una barra de chocolate. Es la señal.",
  f"jogging|{GORDIEVSKY} in a tracksuit jogging alone along a wide Moscow avenue in summer 1985, glancing back over his shoulder",
  "plastic_bag|A man standing still on a Moscow street corner at dusk holding a plain plastic shopping bag, another man walking past eating a chocolate bar, seen from across the street, no logo")
b("Días después sale a correr, despista a sus vigilantes y viaja hacia la frontera. Cruza a Finlandia en el maletero de un coche de diplomáticos británicos, mientras los perros de los guardias rodean el coche.",
  "border|A Soviet border checkpoint in a pine forest in July 1985, a barrier, guards and dogs around a dark diplomatic car@@FRONTERA CON FINLANDIA",
  "trunk|The inside of a dark car trunk, a man curled up under a blanket, a thin line of light")
b("La KGB lo condena a muerte en ausencia. Quien probablemente lo delató fue un oficial de la CIA que vendía secretos a Moscú: Aldrich Ames.",
  "ames|An American CIA officer in his forties with a mustache and large glasses, a grey suit, 1985@@ALDRICH AMES",
  "dead_drop|A hand leaving a package under a small wooden footbridge in a park at dusk, seen from far away")
b("Seis años después, quien se derrumba es la propia KGB.",
  "lubyanka_night#detalhe-alto", ideia=True)

# ───────────────────────── 13. LA ESTATUA ─────────────────────────
cap("13. La Estatua")
b("La Estatua. Agosto de mil novecientos noventa y uno. El jefe de la KGB, Vladímir Kriuchkov, encabeza con otros un golpe contra Mijaíl Gorbachov. Dura tres días y fracasa.",
  f"kryuchkov|{KRYUCHKOV} at a table with other grim officials at a press conference, microphones@@VLADÍMIR KRIUCHKOV",
  "tanks_91|Tanks on a Moscow avenue in August 1991 surrounded by a crowd of civilians, people climbing on them, seen from far away", card="MOSCÚ, 1991")
b("La noche del veintidós de agosto, una multitud rodea la Lubianka. En el centro de la plaza está la estatua de Félix Dzerzhinski, el fundador de la Cheká.",
  "crowd_91|A huge crowd at night in Lubyanka Square in Moscow in August 1991, people with tricolor flags, the yellow building behind",
  "tricolor|A young Muscovite waving a large white-blue-red flag at night in August 1991, floodlights, a crowd behind",
  "statue|A tall bronze statue of a man in a long greatcoat on a high pedestal in a square at night, floodlights, a crowd around@@22 DE AGOSTO DE 1991")
b("Una grúa la levanta por el cuello y la arranca del pedestal. La gente aplaude.",
  "crane|A large crane lifting a bronze statue of a man in a greatcoat by a cable around its neck off a pedestal at night, a crowd cheering",
  "empty_pedestal|An empty stone pedestal in a city square at dawn, flowers and papers on the ground")
b("En diciembre, la Unión Soviética desaparece y la KGB queda dividida en varios servicios. El de seguridad interior acabará llamándose FSB.",
  "flag_down|A red flag without emblems being lowered from a pole over the Kremlin at night, December 1991, seen from far away",
  "split_files|Piles of brown case files being divided into separate stacks on a long table by men in suits, 1991")
b("Meses después, un jubilado entra en una embajada con una bolsa llena de papeles.",
  "riga_street|A cobbled street in the old town of Riga, Latvia in 1992, church spires, an old man walking with a bag", ideia=True)

# ───────────────────────── 14. EL ARCHIVISTA ─────────────────────────
cap("14. El Archivista")
b("El Archivista. Riga, Letonia, marzo de mil novecientos noventa y dos. Vasili Mitrojin entra en la embajada británica. En una bolsa vieja trae notas copiadas a mano.",
  f"mitrokhin|{MITROKHIN} standing at a reception window of an embassy holding a cloth bag@@VASILI MITROJIN",
  "bag_notes|A worn cloth bag open on a table with bundles of folded handwritten papers inside, lamp light, unreadable", card="RIGA, 1992")
b("Durante años fue archivista de la inteligencia exterior de la KGB. Leía expedientes secretos y copiaba lo que podía. Escondía las notas en los zapatos.",
  f"archive_kgb|{MITROKHIN} younger, in his fifties, reading files alone among tall shelves in a Soviet archive, 1975",
  "shoe_notes|Close-up of a man's hand slipping a small folded note into a shoe under a desk")
b("En casa las pasaba a limpio y las escondía en bidones de leche, bajo el suelo de su casa de campo. Así durante doce años.",
  "milk_churn|An old metal milk churn full of rolled papers half buried under the wooden floor of a country house, a lamp",
  "dacha_night|A small wooden Russian country house at night, a single lit window, birch trees")
b("Los británicos lo sacan del país con su familia y miles de páginas. Es una de las mayores filtraciones de inteligencia de la historia.",
  "suitcases|Old suitcases full of papers being loaded into the trunk of a car at night, seen from far away",
  "pages_desk|Thousands of handwritten pages in piles on a long table in a British office, an analyst reading")
b("Entre ellas aparece América Latina. Según esas notas, la KGB entregó dinero a la campaña de Salvador Allende en Chile, en mil novecientos setenta. La misma elección en la que la CIA pagaba propaganda contra él.",
  "santiago_70|Santiago de Chile in 1970, a crowded campaign rally in a street, the Andes behind, banners without text, seen from far away",
  "money_envelope|A thick envelope of banknotes passed under a café table, two pairs of hands, 1970",
  "map_world|" + "A world map showing Europe, the Atlantic Ocean and the whole of the Americas, " + MAPA)
b("Y en mil novecientos noventa y nueve, sus notas revelan a una espía británica de ochenta y siete años. Había pasado secretos atómicos a Moscú durante décadas.",
  "norwood|An elderly British woman of eighty-seven with white hair and glasses standing at the garden gate of a modest suburban house, 1999",
  "bexleyheath|A quiet suburban London street of semi-detached brick houses in 1999, autumn leaves, a parked car",
  "reporters|A crowd of reporters with cameras outside a small brick house in a London suburb in 1999", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. La Bolita")
b("La Bolita. La Cheká nació con unas decenas de hombres. La KGB llegó a tener cientos de miles.",
  "few_men#médio-dir", "cheka_crowd#detalhe-centro")
b("Pero el arma más recordada de aquellos años medía menos de dos milímetros.",
  "pellet#detalhe-centro", ideia=True)
b("La KGB no necesitaba estar en todas partes. Le bastaba con que todos creyeran que podía estar.",
  "ear_wall|A man in a dark Soviet apartment pressing his ear to the wall, listening, a single lamp, 1970s",
  "whisper#médio-esq", "files_desk#detalhe-alto", ideia=True)
b("Hoy, el edificio amarillo de la Lubianka sigue en pie.",
  "lubyanka_today|The yellow Lubyanka building in Moscow today in winter, an empty pedestal-less square, modern cars, grey sky",
  "folder_close|A hand closing a thick brown case file with a red circular stamp on a dark desk, lamp light")
b("Y tú, ¿qué es más peligroso en una policía secreta: lo que hace o el miedo que provoca? Déjalo en los comentarios. Y el otro lado de la Guerra Fría, el expediente completo de la CIA, está aquí.",
  "red_stamp#médio-esq", "bridge_empty#aberto")

# a 1ª prova do 001 (04/11) saiu com moldura de papel: todo prompt leva sangria explícita
SANGRIA = ", full-bleed illustration filling the entire frame edge to edge, no border, no margin, no white frame, no panel outline"

# Thumbs (biblia/thumb.md): personagem à esquerda com objeto que conta o tema, metade direita livre.
THUMBS = [
    {"id": "thumb-A", "prompt": "A Soviet KGB officer in his fifties in half body on the LEFT third of the frame, dark 1970s overcoat and fur hat without insignia, holding a closed black umbrella with its metal tip pointing forward, cold stare at the viewer, behind him the yellow Lubyanka building in Moscow at dusk with snow; the RIGHT half of the image is plain empty dark winter sky, no signage, no lettering"},
    {"id": "thumb-B", "prompt": "A Soviet KGB officer in his forties in half body on the LEFT third of the frame, long dark coat and fedora, holding a thick brown case file against his chest, menacing stare at the viewer, behind him a dark Moscow street at night with a lit window; the RIGHT half of the image is plain dark empty wall in shadow, no signage, no lettering"},
    {"id": "thumb-C", "prompt": "A tall bronze statue of a gaunt man in a long greatcoat being lifted off its pedestal by a crane cable at night on the LEFT third of the frame, a crowd below with raised hands, floodlights, the yellow Lubyanka building behind; the RIGHT half of the image is plain dark empty night sky, no signage, no lettering"},
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
