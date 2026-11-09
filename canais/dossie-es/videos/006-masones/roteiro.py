#!/usr/bin/env python3
"""Fonte única do dossie-es 006 (Masones): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (na pasta do vídeo). Conteúdo no topo; geração no fim (copiada do 005-kgb).

Molde da bíblia (canais/dossie-es/biblia/roteiro.md): hook por anedota (o desaparecimento de William Morgan, Batavia/Canandaigua,
1826; Academia Play abre com a taberna de 1717 e ninguém dos concorrentes transcritos em ref/ usa Morgan) → 14 expedientes-objeto
com título falado → pagamento da anedota no expediente 8 ("El Libro", logo após o CTA) → cierre "El Secreto" que volta ao
livro de Morgan + aforismo + pergunta.
Rigor fato × mito (brief): Barruel e os Illuminati, a fraude de Taxil e a cifra do arquivo de Salamanca são ditos como o que
são; nada de "dominam o mundo". Factual, atribuído, sem sensacionalismo.
Ângulo América Latina: Logia Lautaro (San Martín, Alvear, O'Higgins, 1812), Bolívar iniciado em Paris e o decreto de 1828,
escoceses × yorkinos no México, Massera e López Rega na lista da P2. Liga com Cosa Nostra (Calvi/Calò) e CIA (sessão).
Fatos conferidos em 09/11/2026 (ver SOURCES.md).

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (id I### na ordem de aparição) · "chave" reuso · "chave#enq" reuso com enquadramento
  + "@@TEXTO"      rótulo na tela (máquina de escrever; CAIXA ALTA, até ~28 caracteres)
Bloco: b(texto, *planos, card="BATAVIA, 1826", ideia=True) · capítulo: cap("5. La Biblia")
Mapas (chave map_*): base sem texto nem pinos; pinos, setas e nomes no código (src/labels.jsx).
"""
import json, math, re
from pathlib import Path

WPS = 2.38           # palavras/s medidas no 001–005 (erro de 1–3%)
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
TITULO = "TODA la historia de los Masones"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# Personagens (descrição visual fixa; rostos "resembling", nunca foto)
MORGAN = "a man in his early fifties with a weathered face, short receding dark hair and sideburns, a worn dark 1820s frock coat and a white cravat"
ASHMOLE = "an English gentleman scholar in his late twenties with long curled dark hair and a thin mustache, a plain dark 1640s doublet with a white linen collar"
ANDERSON = "a Scottish Presbyterian minister in his forties with a white powdered wig, a black clerical gown and white preaching bands, 1723"
CLEMENT = "a very old frail pope in his eighties, white zucchetto, red velvet mozzetta, a thin pale face, 1738"
WASHINGTON = "a tall American statesman in his late fifties resembling George Washington, powdered grey hair tied back, a plain dark brown civilian suit, 1789"
FRANKLIN = "an elderly American statesman in his seventies resembling Benjamin Franklin, long thin grey hair, small round spectacles, a plain brown coat, 1778"
VOLTAIRE = "a very thin old French writer in his eighties resembling Voltaire, a sharp nose, a sly smile, a long powdered wig, 1778"
BARRUEL = "a French priest in his fifties with a stern narrow face and grey hair, a black cassock, 1797"
WEISHAUPT = "a young German law professor in his late twenties with a powdered wig and a dark coat, 1776"
SANMARTIN = "a South American officer in his early thirties resembling José de San Martín, dark hair, thick sideburns, a dark blue 1812 cavalry uniform without insignia"
ALVEAR = "a young Argentine officer in his early twenties with curly dark hair, a dark 1812 uniform without insignia"
OHIGGINS = "a Chilean officer in his late thirties resembling Bernardo O'Higgins, a round face, light reddish hair, a dark uniform without insignia, 1817"
BOLIVAR = "a slim South American general in his mid forties resembling Simón Bolívar, dark curly hair, long sideburns, a thin face, a dark blue uniform with gold embroidery, 1828"
MANUELA = "a dark-haired woman in her early thirties resembling Manuela Sáenz, an 1820s dark dress, a determined face"
WIRT = "an American lawyer in his late fifties with curly grey hair and a broad face, a black 1830s suit and white high collar"
TAXIL = "a plump French journalist in his forties with a thick dark mustache and pomaded dark hair, a dark 1890s suit"
LEO = "an elderly thin pope in his late seventies resembling Pope Leo XIII, white cassock and zucchetto, a gaunt smiling face, 1887"
FRANCO = "a short Spanish general in his late forties resembling Francisco Franco, a thin mustache, receding hair, a plain military uniform without insignia, 1940"
GELLI = "an Italian businessman in his early sixties with slicked-back grey hair and dark-rimmed glasses, an elegant dark suit, 1981"
CALVI = "an Italian banker in his early sixties with a thick dark mustache, thinning dark hair and glasses, a grey suit, 1982"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, borders and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame"
SEM = ", no lettering anywhere"   # objetos com capa, placa ou papel: o nano-banana inventa texto

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Batavia, Nueva York, septiembre de mil ochocientos veintiséis. El albañil William Morgan anuncia un libro con los rituales secretos de los masones.",
  "batavia|A small American village in western New York in 1826, a muddy main street with wooden houses and a white church, autumn trees, grey sky",
  f"morgan_desk|{MORGAN} writing by candlelight at a rough wooden table covered with handwritten pages, a small room at night",
  "manuscript|Close-up of a stack of handwritten manuscript pages tied with string next to a quill and an inkwell, candle light, the handwriting unreadable",
  f"morgan_face|{MORGAN} in portrait, a nervous determined face, a dim wooden room behind him@@WILLIAM MORGAN", card="BATAVIA, 1826")
b("Lo encierran en la cárcel de Canandaigua por una deuda de menos de tres dólares. Esa noche alguien la paga. En la puerta, unos hombres lo suben a la fuerza a un carruaje.",
  "jail_1826|A small stone county jail in a New York village at night in 1826, a single lantern by the heavy wooden door",
  "coins|Close-up of a few old silver coins and copper cents placed on a wooden counter by a hand, lantern light",
  "jail_door|The heavy wooden door of a small jail opening at night, a man in a dark coat stepping out into the lantern light, seen from behind",
  "seized|Two men in dark coats and hats grabbing a man by the arms in a dark village street at night, seen from far away, no weapons",
  "carriage_night|A closed black horse-drawn carriage speeding away on a dirt road at night under the moon, dust behind it, 1826")
b("Nadie volvió a ver a William Morgan.",
  "lantern_out|Wide shot of the open door of a small stone village jail at night, a lantern on the doorstep going out with a thin trail of smoke, the dark street around it",
  "empty_road|An empty dirt road through dark woods at dawn in 1826, carriage wheel tracks in the mud, mist")
b("Esta es TODA la historia de los Masones. Y de por qué su secreto despierta sospechas desde hace tres siglos.",
  "files_desk|A long dark desk covered with open brown case files and old engravings, a red stamp and a magnifying glass, lamp light",
  "square_compass|A worn brass square and compass laid crossed on an old leather-bound book on a dark wooden table, candle light, dramatic close-up",
  "red_stamp|A hand slamming a red rubber stamp onto a brown paper case file, ink splash, dramatic close-up",
  "lodge_dark|The interior of an old Masonic lodge room at night, a black and white checkered floor, two tall columns, empty wooden chairs, a single candle", ideia=True)

# ───────────────────────── 1. LA LOGIA ─────────────────────────
cap("1. La Logia")
b("La Logia. Europa, siglo trece. Una catedral tarda décadas en levantarse. Los canteros, los que tallan la piedra, viajan de obra en obra.",
  "cathedral_build|A gothic cathedral under construction in the 13th century, wooden scaffolding and cranes, stonemasons at work, seen from far away",
  "masons_road|A group of medieval stonemasons with tools on their backs walking along a country road towards a distant town with a half-built cathedral",
  "quarry|Medieval workers cutting large limestone blocks in a quarry, ropes and wooden sledges, dust in the sunlight",
  "carving|A medieval stonemason carving a gothic stone capital with a chisel and mallet, stone dust in the light", card="EUROPA, SIGLO XIII")
b("Junto a la obra montan una cabaña de madera para trabajar, comer y guardar herramientas. En inglés la llaman lodge. En español, logia.",
  "lodge_hut|A wooden workshop hut leaning against the wall of a gothic cathedral under construction, stonemasons resting inside, tools hanging on the walls",
  "tools_wall|Medieval stonemason tools hanging on a wooden wall: a square, a compass, a mallet, chisels and a plumb line, warm light",
  "hut_meal|Medieval stonemasons eating bread and drinking from wooden cups at a rough table inside a wooden hut, evening light",
  "hut_door|The open door of a medieval wooden workshop hut, a master mason looking out at the cathedral scaffolding@@LODGE · LOGIA")
b("Su oficio es un secreto profesional: cómo trazar un arco, cómo cortar la piedra para que aguante siglos.",
  "tracing|A medieval master mason drawing the lines of a gothic arch with a large compass on a plaster tracing floor",
  "arch|A gothic pointed stone arch being assembled on a wooden frame by stonemasons, seen from below",
  "stone_cut|Close-up of hands measuring a cut block of limestone with an iron square, chisel marks visible")
b("En Escocia, en mil quinientos noventa y ocho, el maestro de obras del rey, William Schaw, pone por escrito las reglas de los canteros. En el siglo siguiente ya se habla de su contraseña secreta: la Palabra del Masón.",
  "schaw|A Scottish royal official in his fifties in a dark late 16th century doublet and ruff, writing at a desk in a stone castle room",
  "schaw_castle|A Scottish royal castle on a rock in 1598 under grey clouds, a small town below, seen from far away",
  "statutes|Close-up of a handwritten 16th century parchment document with a wax seal on a wooden desk, the writing unreadable" + SEM,
  "whisper_word|Two Scottish stonemasons in 16th century clothes, one whispering in the other's ear at the door of a stone building, dusk",
  "handshake|Close-up of two rough hands in a firm handshake, the sleeves of 16th century work clothes, dark background", card="ESCOCIA, 1598")
b("Pero las catedrales se terminan. Y las logias empiezan a aceptar a gente que nunca tocó una piedra.",
  "cathedral_done|A finished gothic cathedral towering over a medieval town at sunset, the scaffolding gone",
  "masons_leave|Medieval stonemasons packing their tools and walking away from a finished cathedral at dawn",
  "gentlemen_enter|Three English gentlemen in 17th century cloaks and hats entering a stone building at night, a mason holding the door with a lantern", ideia=True)

# ───────────────────────── 2. EL DIARIO ─────────────────────────
cap("2. El Diario")
b("El Diario. Warrington, Inglaterra, dieciséis de octubre de mil seiscientos cuarenta y seis. Un erudito llamado Elias Ashmole escribe una línea en su diario.",
  "warrington|A small English market town in Lancashire in 1646, timber-framed houses, a muddy street, an autumn sky",
  f"ashmole_write|{ASHMOLE} writing in a small leather diary with a quill at a desk by a window",
  "diary|Close-up of an open 17th century leather diary with one handwritten line, a quill beside it, the writing unreadable", card="WARRINGTON, 1646")
b("Dice que ese día lo hicieron masón, junto con un coronel, Henry Mainwaring.",
  f"ashmole_face|{ASHMOLE} in portrait, a calm intelligent face, candle light@@ELIAS ASHMOLE",
  "manor|The interior of an English country manor house in 1646, a group of gentlemen in dark doublets gathered around a table with candles",
  "aprons|A row of plain white lambskin aprons laid on a wooden table in a candlelit 17th century room")
b("Ashmole no es cantero. Es uno de los primeros masones aceptados con registro en Inglaterra: entra por las ideas, no por el oficio.",
  "scholar_books|A 17th century English scholar's study full of books, astrolabes, globes and alchemical jars",
  "accepted|A group of English gentlemen in 17th century clothes standing in a circle in a candlelit room, one wearing a white apron for the first time",
  f"ashmole_lodge|{ASHMOLE} wearing a white apron for the first time among older gentlemen in a candlelit room",
  "two_worlds|A stonemason in work clothes and a gentleman in a velvet doublet facing each other across a table with a compass on it")
b("Años después, su colección dará origen al Ashmolean de Oxford, considerado el primer museo universitario del mundo.",
  "ashmolean|The facade of a 17th century stone museum building in Oxford in the 1680s, visitors in period clothes at the door",
  "oxford_1683|Oxford in the 1680s, honey-colored college towers and spires seen across meadows, morning light",
  "cabinet|A cabinet of curiosities in the 1680s, shelves with shells, fossils, coins and stuffed animals")
b("En las décadas siguientes, nobles, científicos y comerciantes llenan las logias. Las herramientas se vuelven símbolos: la escuadra, la rectitud; el compás, la medida.",
  "lodge_crowd|A crowded lodge room in early 18th century London, gentlemen in powdered wigs and white aprons seated around a long table",
  "square_close|A brass stonemason's square resting on an open book, dramatic candle light, dark background",
  "compass_close|A brass drawing compass standing open on a dark wooden table, candle light reflecting on the metal",
  "symbols_floor|A black and white checkered lodge floor with a square and compass laid at its center, candle light, seen from above")
b("Les falta una sola cosa: una organización.",
  "lodge_empty|An empty 17th century tavern back room with chairs pushed back from a table and blown-out candles, morning light", ideia=True)

# ───────────────────────── 3. LA TABERNA ─────────────────────────
cap("3. La Taberna")
b("La Taberna. Londres, veinticuatro de junio de mil setecientos diecisiete. Cuatro logias se reúnen en una taberna junto a la catedral de San Pablo: El Ganso y la Parrilla.",
  "london_1717|London in 1717 seen from the Thames, the dome of St Paul's Cathedral rising over the rooftops, sailing boats on the river",
  "tavern_out|The front of a narrow 18th century London tavern at dusk, a hanging painted sign showing a goose and a gridiron, no lettering, St Paul's dome behind",
  "tavern_in|The crowded upstairs room of a London tavern in 1717, gentlemen in wigs and long coats with pints of ale around a table, candle light",
  "toast|Gentlemen in 1717 wigs raising glasses in a toast in a smoky candlelit tavern room", card="LONDRES, 1717")
b("Allí fundan la Gran Logia de Londres y eligen a su primer Gran Maestro, Anthony Sayer.",
  "sayer|A modest English gentleman in his forties in a plain brown coat and a simple wig, standing at the head of a tavern table, being applauded",
  "election|Gentlemen in wigs raising their hands to vote in a candlelit tavern room in 1717",
  "grand_master|An English gentleman wearing a white apron and a ceremonial collar receiving a gilded square on a cord from another man, candle light")
b("Casi todo lo que se sabe de esa reunión viene de un libro publicado veinte años después. Algunos historiadores dudan incluso de la fecha.",
  "old_book|An old 18th century leather-bound book lying open on a desk, a magnifying glass over its pages, the print unreadable" + SEM,
  "date_doubt|Close-up of a quill circling an ink smudge in red on an old parchment page covered with illegible scribbles, candle light" + SEM,
  "historian|A modern historian with glasses examining an old book in a quiet archive reading room, lamp light")
b("En mil setecientos veintitrés, el pastor James Anderson publica las Constituciones: en la logia no se discute de religión ni de política.",
  f"anderson|{ANDERSON} writing at a desk in a London study with books and a quill@@JAMES ANDERSON",
  "constitutions|A printed 1723 book with a plain leather cover lying on a table next to a square and compass, candle light" + SEM,
  "printing|A London printing press in 1723, a printer pulling the lever, freshly printed sheets hanging to dry")
b("Solo se pide obedecer la ley moral y no ser ateo. Anderson llama a Dios el Gran Arquitecto del Universo. Para la época, es una idea atrevida.",
  "architect|An old engraving-style ink image of a giant hand holding a compass over a sphere of the world among clouds, dark background, no text",
  "starry_ceiling|A man in an 18th century wig looking up at a painted starry ceiling in a candlelit lodge room",
  "candle_book|A single candle beside an open book and a brass compass on a lodge altar, the rest of the room in darkness" + SEM,
  "mixed_men|An Anglican, a Presbyterian and a Quaker gentleman in 1720s clothes sitting together at a lodge table, candle light")
b("En pocos años hay logias en París, en Madrid, en Roma. Y Roma se entera.",
  "madrid_1728|A quiet street in Madrid in 1728 at night, a gentleman in a cloak knocking on the door of a house",
  "vatican_1738|St Peter's Basilica in Rome in the 1730s seen from the square, carriages and clergy, grey morning light", ideia=True)

# ───────────────────────── 4. LA BULA ─────────────────────────
cap("4. La Bula")
b("La Bula. Roma, veintiocho de abril de mil setecientos treinta y ocho. El papa Clemente doce firma la bula In eminenti.",
  f"clement|{CLEMENT} seated at a desk in a Vatican room, a cardinal handing him a parchment",
  "bull_seal|Close-up of a lead papal seal hanging by a cord from a parchment document on a velvet table" + SEM, card="ROMA, 1738")
b("Todo católico que entre en una logia queda excomulgado.",
  "excommunication|A priest at a pulpit reading a parchment to a silent congregation in a dark baroque church in 1738",
  "candle_out|Close-up of a hand snuffing out a church candle, smoke rising, dark background")
b("El texto da sus motivos: en las logias se reúnen hombres de cualquier religión y se juran silencio. Y si no hicieran el mal, dice la bula, no odiarían tanto la luz.",
  "oath|A man kneeling with his hand on a book in a dark candlelit lodge room, other men in aprons around him in shadow",
  "silence|Close-up of a man in an 18th century wig holding a finger to his lips, candle light",)
b("En España, la Inquisición persigue a los masones. En mil setecientos cincuenta y uno, el rey Fernando sexto prohíbe las logias.",
  "inquisition|An 18th century Spanish Inquisition tribunal room, three judges in black at a long table with a cross, a man standing before them",
  "fernando_decree|A Spanish king in his late thirties in an 18th century court dress and wig signing a decree at a gilded desk",)
b("Pero la prohibición no las frena. En Francia y en las colonias inglesas, las logias se llenan de hombres que pronto harán revoluciones.",
  "colonial_lodge|A lodge room in colonial Philadelphia in the 1750s, men in plain coats and white aprons around a table with candles",
  "revolution_hint|A crowd of American colonists gathered under a large tree at night with torches, 1770s, seen from far away", ideia=True)

# ───────────────────────── 5. LA BIBLIA ─────────────────────────
cap("5. La Biblia")
b("La Biblia. Nueva York, treinta de abril de mil setecientos ochenta y nueve. George Washington jura como primer presidente de Estados Unidos.",
  "federal_hall|Federal Hall in New York on 30 April 1789, a huge crowd in the street below a balcony with columns, flags without symbols",
  f"washington_oath|{WASHINGTON} on a balcony with his right hand raised and his left hand on a large open Bible held by another man@@GEORGE WASHINGTON", card="NUEVA YORK, 1789")
b("No encuentran una Biblia a tiempo, así que traen una de una logia cercana. Y le toma el juramento el Gran Maestro de los masones de Nueva York.",
  "running_bible|A man in an 18th century coat hurrying through a New York street carrying a large leather Bible on a red velvet cushion",
  "bible_cushion|Close-up of a large old leather Bible resting on a crimson velvet cushion, gold edges, warm light" + SEM,)
b("Washington era masón desde los veinte años. Benjamin Franklin también. En París, en mil setecientos setenta y ocho, Franklin acompaña al anciano Voltaire en su iniciación.",
  "young_washington|A young American man of twenty in a 1750s Virginia coat standing in a candlelit lodge room wearing a white apron",
  f"franklin|{FRANKLIN} entering a Paris lodge room with an elegant crowd in wigs, candle light@@BENJAMIN FRANKLIN",
  f"voltaire|{VOLTAIRE} leaning on the arm of an old man in spectacles in a crowded Paris lodge room, candle light",)
b("Hubo masones entre los Padres Fundadores. Y también entre los oficiales del rey británico. En las logias circulaban ideas nuevas.",
  "redcoats|British army officers in red coats sitting around a table in a candlelit tent, 1777",
  "debate|Men in 18th century clothes debating passionately around a candlelit table covered with pamphlets" + SEM)
b("Pronto, alguien las acusará de haberlo planeado todo.",
  "shadow_finger|The shadow of a man pointing his finger cast on a wall covered with old pamphlets, candle light", ideia=True)

# ───────────────────────── 6. EL ABATE ─────────────────────────
cap("6. El Abate")
b("El Abate. Londres, mil setecientos noventa y siete. Un sacerdote francés exiliado, Augustin Barruel, publica una obra en varios tomos.",
  f"barruel|{BARRUEL} writing furiously at a desk piled with papers in a small London room, candle light@@AUGUSTIN BARRUEL",
  "barruel_books|A stack of four thick leather-bound volumes on a desk next to an inkwell and a quill" + SEM, card="LONDRES, 1797")
b("Su tesis: la Revolución Francesa no fue una revuelta popular, sino un complot de los masones y de una sociedad secreta: los Iluminados de Baviera.",
  "bastille|The storming of the Bastille in 1789, a crowd with pikes and flags before the fortress walls, smoke, seen from far away, no blood",
  "guillotine_far|A Paris square in 1793 with a guillotine on a scaffold seen from far away, a crowd, grey sky, no blood, no bodies",
  "plot_table|Shadowy men in wigs whispering around a candlelit table with a map, seen through a half-open door, theatrical",)
b("Los Iluminados existieron. Los fundó un profesor, Adam Weishaupt, en mil setecientos setenta y seis. Pero el gobierno de Baviera los prohibió entre mil setecientos ochenta y cuatro y mil setecientos ochenta y cinco.",
  f"weishaupt|{WEISHAUPT} lecturing to a few students in a wood-paneled classroom@@ADAM WEISHAUPT",
  "bavaria_decree|A Bavarian official in a 1785 coat reading a decree to soldiers in front of a townhouse" + SEM,)
b("Cuando estalló la Revolución, llevaban años disueltos. Y muchos masones franceses terminaron en la guillotina. Entre ellos, el duque de Orleans, que había sido Gran Maestro y meses antes había renunciado a la masonería.",
  "orleans|A French duke in his mid forties in an elegant dark coat being led to a cart by revolutionary guards, Paris 1793",
  "cart|A wooden cart carrying prisoners through a crowded Paris street in 1793, seen from far away",)
b("Los historiadores no han hallado pruebas de ese complot. Pero el libro de Barruel se traduce a varios idiomas. Nace una teoría que llega hasta hoy.",
  "translations|Many copies of the same thick book in different bindings stacked on a bookseller's table in 1800" + SEM,
  "reader|A man reading a thick book by candlelight with a worried face, early 19th century", ideia=True)

# ───────────────────────── 7. LA FRAGATA ─────────────────────────
cap("7. La Fragata")
b("La Fragata. Buenos Aires, nueve de marzo de mil ochocientos doce. Desde Londres llega la fragata George Canning.",
  "frigate|A British merchant frigate with full sails arriving in the brown waters of the Río de la Plata in 1812, small boats around it",
  "bsas_1812|Buenos Aires in 1812 seen from the river, low white colonial houses, church towers, carts in the shallow water",
  "map_lautaro|A map of the Atlantic Ocean showing western Europe, the British Isles, the Iberian peninsula, Africa and the whole of South America, " + MAPA, card="BUENOS AIRES, 1812")
b("A bordo vienen oficiales que habían luchado en el ejército español contra Napoleón. Uno se llama José de San Martín. Otro, Carlos María de Alvear.",
  f"sanmartin|{SANMARTIN} standing on the deck of a ship looking at the coast@@JOSÉ DE SAN MARTÍN",
  f"alvear|{ALVEAR} on the deck of a ship beside other officers@@CARLOS MARÍA DE ALVEAR")
b("Poco después fundan una sociedad secreta: la Logia Lautaro. Sus miembros juran trabajar por la independencia de América.",
  "lautaro_oath|Young South American officers in dark uniforms with their hands on a sword laid on a table, a candlelit colonial room, 1812",
  "sword_oath|Close-up of several hands placed one on top of another over the hilt of a sword, candle light@@LOGIA LAUTARO")
b("En Buenos Aires, la logia ayuda a derribar un gobierno. Por ella pasan, según los historiadores, Bernardo O'Higgins, en Chile, y otros jefes de la independencia del sur.",
  f"ohiggins|{OHIGGINS} standing before the Andes with an army behind him@@BERNARDO O'HIGGINS",
  "andes_army|An army of soldiers and mules crossing a high mountain pass in the Andes in 1817, snow, seen from far away")
b("¿Era una logia masónica? Los historiadores no se ponen de acuerdo: copiaba ritos masónicos, pero su fin era político.",
  "archive_doubt|A historian's desk with old letters, a magnifying glass and a candle, the handwriting unreadable" + SEM,
  "ritual_politics|A candlelit room split between a lodge altar with a compass on one side and a map of South America on the other")
b("Simón Bolívar, según la tradición masónica, se había iniciado en una logia de París en mil ochocientos cinco.",
  f"bolivar_young|A young South American aristocrat of twenty-two in an elegant 1805 Parisian coat, dark curly hair, standing in a Paris lodge room wearing an apron",
  "paris_1805|Paris in 1805, an elegant street at dusk with carriages, a young man entering a townhouse", ideia=True)
b("Si te gustan estos expedientes, suscríbete. Y ahora, volvemos a Batavia.",
  "red_stamp#detalhe-centro", "batavia#médio-dir")

# ───────────────────────── 8. EL LIBRO ─────────────────────────
cap("8. El Libro")
b("El Libro. Mil ochocientos veintiséis. William Morgan iba a publicar los rituales con un impresor del pueblo, David Miller. Alguien intentó incendiar la imprenta.",
  "press_1826|A small village printing shop in 1826, a wooden hand press, stacks of paper, a printer in an apron",
  "fire_press|A small wooden printing shop in a village at night with flames at its back door, men running with buckets, seen from far away",
  f"morgan_desk#médio-esq", card="BATAVIA, 1826")
b("Según los juicios posteriores, a Morgan se lo llevaron al fuerte Niágara, en la frontera con Canadá. Ahí se pierde su rastro.",
  "fort_niagara|Fort Niagara at night in 1826, a stone fortress on the shore of Lake Ontario, a single lit window",
  "lake_ontario|The dark waters of the Niagara River flowing into Lake Ontario at night, mist, no people")
b("El libro sale igual, ese mismo año. Y se vende como nunca.",
  "book_morgan|A small printed book from 1826 with a plain cover lying on a wooden counter, a crowd of hands reaching for copies" + SEM,
  "readers_1826|Men in 1820s clothes reading the same small book in a village store, shocked faces")
b("Varios masones son condenados por el secuestro, con penas de pocos meses a poco más de dos años. Por asesinato, nadie: nunca se confirmó un cuerpo.",
  "trial_1826|A crowded 1820s American courtroom, a judge at a high bench, defendants in dark coats, spectators in the gallery",
  "body_shore|A lonely lake shore at dawn with a group of men standing around something hidden in the reeds, seen from far away, no body visible",)
b("La sospecha de que los masones se protegen entre sí, jueces incluidos, indigna al país. Nace el Partido Antimasónico, el primer gran partido de Estados Unidos fuera de los dos principales.",
  "anger|An angry crowd of farmers and townspeople at a meeting in a village church in 1828, a man shouting from a pulpit",
  "party_meeting|A political rally in a New York town square in 1830, banners without text, a speaker on a wooden platform@@PARTIDO ANTIMASÓNICO")
b("En mil ochocientos treinta y uno, el partido celebra en Baltimore la primera convención nacional del país para elegir candidato a presidente. El elegido, William Wirt, había sido masón.",
  "baltimore|A crowded hall in Baltimore in 1831, delegates in black coats voting by raising their hands",
  f"wirt|{WIRT} standing at a lectern, a surprised crowd before him@@WILLIAM WIRT",)
b("En Nueva York, cientos de logias cierran sus puertas.",
  "closed_lodge|A boarded-up two-story lodge building on a New York village street in 1830, a padlock on the door, snow",
  "lodge_dust|An abandoned lodge room with dust on the chairs and a fallen banner without symbols, grey light", ideia=True)

# ───────────────────────── 9. EL DECRETO ─────────────────────────
cap("9. El Decreto")
b("El Decreto. Bogotá, veinticinco de septiembre de mil ochocientos veintiocho. Un grupo de conjurados entra de noche en el palacio para matar a Simón Bolívar.",
  "bogota_1828|Bogotá in 1828 at night, a colonial street with balconies, the mountains dark behind, a few lanterns",
  "conspirators|A group of armed men in cloaks entering a colonial palace courtyard at night, seen from far away, no shooting",
  f"bolivar|{BOLIVAR} in portrait, tired and grave, candle light@@SIMÓN BOLÍVAR", card="BOGOTÁ, 1828")
b("Bolívar escapa por una ventana. Manuela Sáenz entretiene a los atacantes.",
  "window_escape|A man in a dark coat climbing out of a colonial palace window at night into a dark street, seen from behind",
  f"manuela|{MANUELA} standing in a dark palace corridor facing armed men with a candle in her hand@@MANUELA SÁENZ",)
b("Seis semanas después, el ocho de noviembre, Bolívar firma un decreto: quedan prohibidas todas las sociedades secretas en la Gran Colombia.",
  f"bolivar_sign|{BOLIVAR} signing a document at a desk lit by candles, a stern face",
  "lodge_sealed|Soldiers closing the doors of a colonial meeting house at night, one fixing a wax seal on the door")
b("El hombre que se inició en una logia de París cierra las logias de su país.",
  "bolivar_young#médio-dir", "bolivar_sign#detalhe-centro")
b("En México, mientras tanto, las logias se convierten en partidos: los escoceses, más conservadores, contra los yorkinos, más radicales. El representante de Estados Unidos, Joel Poinsett, impulsa a los yorkinos.",
  "mexico_1826|Mexico City in 1826, the cathedral and the main square, carriages and people in colonial clothes",
  "poinsett|An American diplomat in his late forties in a dark 1825 coat, a long face and dark hair, handing papers to Mexican gentlemen@@JOEL POINSETT")
b("Pero el siguiente golpe contra la masonería no vendrá de un gobierno. Vendrá de un farsante.",
  "jester_shadow|The shadow of a man laughing cast on a Paris wall covered with posters at night, no text", ideia=True)

# ───────────────────────── 10. LA CONFESIÓN ─────────────────────────
cap("10. La Confesión")
b("La Confesión. París, mil ochocientos ochenta y cinco. Léo Taxil, un periodista que se burlaba de la Iglesia, anuncia que se ha convertido al catolicismo.",
  "paris_1885|Paris in 1885, a boulevard with gas lamps, omnibuses and newspaper kiosks, evening",
  f"taxil|{TAXIL} kneeling in prayer in a church with a pious expression@@LÉO TAXIL", card="PARÍS, 1885")
b("Durante doce años publica libros contra los masones: dice que adoran a Lucifer en ceremonias secretas, dirigidas por una sacerdotisa.",
  "taxil_books|A bookshop window in Paris in 1890 full of lurid illustrated books with plain covers, people looking" + SEM,
  "fake_ritual|A theatrical engraving-style ink illustration of hooded figures around an altar with candles in a dark vault, melodramatic, no symbols",)
b("Los libros se venden por miles. En mil ochocientos ochenta y siete, el papa León trece lo recibe en audiencia.",
  f"leo|{LEO} receiving a plump man with a mustache in a Vatican audience room, the man bowing",
  "vatican_1887|A Vatican audience hall in 1887 with Swiss Guards at the doors, red curtains")
b("El diecinueve de abril de mil ochocientos noventa y siete, Taxil convoca una conferencia en París para presentar a su testigo principal, la sacerdotisa Diana Vaughan.",
  "hall_1897|A packed lecture hall in Paris in 1897, priests and journalists in rows, an empty stage with a table and a lamp",
  "journalists|Journalists in bowler hats with notebooks waiting in a Paris hall, gas light", card="PARÍS, 1897")
b("Sube al escenario y confiesa: todo era mentira. La sacerdotisa satánica no existía. Se había burlado de la Iglesia durante doce años.",
  "confession|A plump man with a thick mustache speaking on a stage in front of a shocked audience in 1897, some standing up",
  "uproar|An uproar in a Paris lecture hall in 1897, men shouting and waving canes, chairs knocked over",
  "taxil_smile|Close-up of a plump man with a thick dark mustache smiling under gas light@@\"TODO ERA MENTIRA\"")
b("Sale del salón entre el escándalo. Pero sus libros siguen circulando y todavía hoy se citan como si fueran verdad.",
  "police_escort|French policemen in 1897 képis escorting a man in a dark coat out of a hall through an angry crowd at night",
  "books_today|A row of old worn leather-bound books on a wooden shelf in a modern living room, warm lamp light, plain spines" + SEM, ideia=True)

# ───────────────────────── 11. EL SEUDÓNIMO ─────────────────────────
cap("11. El Seudónimo")
b("El Seudónimo. En los años veinte y treinta, las dictaduras de Europa disuelven las logias: Mussolini en Italia, Hitler en Alemania.",
  "rome_1925|Blackshirt militiamen marching in a Rome street in 1925, seen from far away, no symbols, no insignia",
  "germany_1935|German police in 1935 carrying boxes of files and ceremonial objects out of a grand lodge building, seen from far away, no symbols, no insignia",)
b("En España, el primero de marzo de mil novecientos cuarenta, Francisco Franco firma la Ley de Represión de la Masonería y el Comunismo.",
  f"franco|{FRANCO} signing a document at a large desk in a dim office in 1940@@FRANCISCO FRANCO",
  "madrid_1940|Madrid in 1940, a grey avenue with few cars and soldiers, damaged buildings", card="MADRID, 1940")
b("Un tribunal especial juzga a miles de personas. En Salamanca, un archivo reúne unas ochenta mil fichas de supuestos masones. En mil novecientos treinta y seis, no pasaban de cinco mil.",
  "tribunal|A Spanish military tribunal in 1941, three officers at a long table under a crucifix, a civilian standing before them",
  "card_index|Endless wooden drawers of index cards in a dim archive in Salamanca, a clerk filing a card",)
b("Y entre mil novecientos cuarenta y seis y mil novecientos cincuenta y uno, un columnista que firma como Jakim Boor publica artículos contra los masones en el diario Arriba.",
  "typewriter_40s|An old typewriter in a dark office in 1946 with a sheet of paper half typed, a lamp, the text unreadable",
  "anon_writer|The silhouette of a man typing at night in a dark office, only his hands and the typewriter lit")
b("Jakín y Boaz son los nombres de las dos columnas a la entrada de un templo masónico. Y detrás de Jakim Boor, según los historiadores, estaba el propio Franco.",
  "two_columns|Two tall bronze columns at the entrance of a dark lodge temple, a checkered floor between them, candle light",
  "franco_writing|A short Spanish general with a thin mustache writing by hand at night at a desk lamp, seen from the side",)
b("El tribunal funciona hasta mil novecientos sesenta y cuatro. En Italia, en cambio, el escándalo estalló dentro de una logia.",
  "archive_closed|An archive room with shelves of bundled files tied with string, a heavy door closing, 1963",
  "italy_hint|A Tuscan hill town at dusk in the 1970s, cypress trees and a villa with lit windows", ideia=True)

# ───────────────────────── 12. LA LISTA ─────────────────────────
cap("12. La Lista")
b("La Lista. Castiglion Fibocchi, Italia, diecisiete de marzo de mil novecientos ochenta y uno. Unos jueces que investigan a un banquero mandan registrar la fábrica de Licio Gelli.",
  "factory_81|A modern textile factory building in a Tuscan town in 1981, Italian police cars parked in front, morning",
  f"gelli|{GELLI} in portrait, a cold smile, a dark office behind him@@LICIO GELLI", card="CASTIGLION FIBOCCHI, 1981")
b("En una caja fuerte y una maleta encuentran una lista de novecientos sesenta y dos nombres. Figuran como miembros de una logia llamada Propaganda Dos: la P2. El Gran Oriente de Italia ya la había desautorizado.",
  "safe|An open office safe full of plain manila folders, a gloved hand pulling out a plain blank envelope, flashlight beam" + SEM,
  "list|Close-up of typed lists of names on several sheets spread on a desk, the names unreadable, a magnifying glass" + SEM + "@@962 NOMBRES")
b("Hay ministros, diputados, generales, los jefes de los servicios secretos, banqueros, periodistas. Y un empresario que años después será primer ministro, y que negó haber participado en ella: Silvio Berlusconi.",
  "parliament|The Italian parliament chamber in Rome in 1981, deputies in suits, seen from the gallery",
  "generals|Italian generals in 1981 uniforms without insignia at a long meeting table",)
b("La lista cruza el Atlántico: en ella aparecen el almirante argentino Emilio Massera y José López Rega, ministro de Perón.",
  "bsas_70s|Buenos Aires in the 1970s, the Casa Rosada and the Plaza de Mayo, grey sky, seen from far away",
  "admiral|An Argentine admiral in his fifties in a white naval uniform without insignia, a hard face, 1976",
  "rega|A balding Argentine politician in his sixties with glasses and a dark suit, 1974, an ornate office")
b("Cuando se publica, el gobierno italiano cae. Una comisión del Parlamento concluye que la P2 buscaba condicionar la vida política del país.",
  "newspapers_81|Italian newspaper kiosk in Rome in 1981 with newspapers hanging, people reading, the headlines unreadable" + SEM,
  "commission|An Italian parliamentary commission in 1984, members seated at a horseshoe table with microphones and files")
b("Otro de los nombres es el de un banquero: Roberto Calvi.",
  "banker_back|A man in a grey suit seen from behind walking alone across a marble bank hall, 1982", ideia=True)

# ───────────────────────── 13. EL PUENTE ─────────────────────────
cap("13. El Puente")
b("El Puente. Londres, dieciocho de junio de mil novecientos ochenta y dos. Por la mañana, un empleado de correos ve a un hombre colgado bajo el puente de Blackfriars.",
  "blackfriars|Blackfriars Bridge in London at dawn in 1982, the Thames at low tide, mist, seen from far away, no body visible",
  "clerk|A London office worker in a 1982 raincoat stopping on the embankment and staring at the river, dawn", card="LONDRES, 1982")
b("Es Calvi, presidente del Banco Ambrosiano. La prensa lo llamaba el banquero de Dios, por sus negocios con el banco del Vaticano.",
  f"calvi|{CALVI} in portrait, anxious face, a bank office behind him@@ROBERTO CALVI",
  "ambrosiano|The stone facade of a large Milan bank in 1982, people at the entrance, no signage, no lettering",)
b("Lleva ladrillos en los bolsillos y unos catorce mil dólares en tres monedas. Semanas después, su banco quiebra con un agujero de más de mil millones de dólares.",
  "bricks|Close-up of broken bricks and stones on a grey morning embankment next to a pile of folded banknotes of different colors, evidence tags without text",
  "bank_crash|Angry clients crowding the closed doors of a Milan bank in 1982, a security guard in front",)
b("Primero se dijo suicidio. En dos mil dos, un peritaje concluyó que fue asesinato. En dos mil siete, un tribunal de Roma juzgó a cinco acusados, entre ellos Pippo Calò, de la Cosa Nostra. Todos fueron absueltos por falta de pruebas.",
  "inquest|A British coroner's court in 1982, a coroner at a bench, lawyers and journalists",
  "forensic|A forensic expert in a lab in 2002 examining an old jacket and a rope under bright light",
  "rome_court|A Rome courtroom in 2007 with a cage for defendants, judges in black robes and lawyers, seen from the public seats")
b("Su muerte sigue sin culpables.",
  "thames_dawn|The river Thames at dawn, empty bridges in the mist, seagulls", ideia=True)

# ───────────────────────── 14. LA DECLARACIÓN ─────────────────────────
cap("14. La Declaración")
b("La Declaración. Roma, noviembre de dos mil veintitrés. El Vaticano responde a un obispo de Filipinas: un católico sigue sin poder ser masón.",
  "vatican_2023|St Peter's Square in Rome in 2023 at dusk, tourists and pilgrims, modern streetlights",
  "letter_2023|Close-up of an official letter with a Vatican coat of arms embossed in plain relief, a pen on a desk, the text unreadable" + SEM, card="ROMA, 2023")
b("Es la misma postura de mil setecientos treinta y ocho, casi trescientos años después.",
  "clement#médio-dir", "bull_seal#detalhe-centro")
b("Con los años, la masonería se abrió: muchas logias tienen página web y organizan visitas.",
  "open_doors|A grand Masonic hall building in London today with its doors open, tourists entering, a sunny day, no signage",
  "tour|A guided tour group of modern tourists inside an ornate lodge room with a checkered floor, taking photos",)
b("Se calcula que hay unos seis millones de masones en el mundo. En Estados Unidos eran más de cuatro millones a finales de los años cincuenta. Hoy son menos de novecientos mil.",
  "world_lodges|An antique globe on a dark wooden desk in a candlelit lodge room, a brass square and compass beside it",
  "us_1959|A 1959 American Masonic parade on a small town main street, men in aprons and hats, flags without symbols",
  "lodge_old|A small-town American lodge room today with a few elderly men in aprons around a table, many empty chairs")
b("Y sigue dividida. La masonería inglesa exige creer en Dios y solo admite hombres. El Gran Oriente de Francia no exige creer en Dios, y desde dos mil diez permite iniciar mujeres.",
  "english_lodge|Men in dark suits and white aprons in a formal English lodge meeting today, an open Bible on the altar",
  "french_lodge|Men and women in dark clothes and aprons seated together in a modern French lodge room, candle light")

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. El Secreto")
b("El Secreto. El libro de William Morgan se sigue imprimiendo. Cualquiera puede leerlo.",
  "book_morgan#detalhe-centro", "bookstore|A modern bookstore shelf with old-style books with plain spines, a hand pulling one out" + SEM)
b("Y ni siquiera fue el primero en revelarlos: en Londres, en mil setecientos treinta, ya se habían publicado los grados y las contraseñas masónicas.",
  "pamphlet_1730|A thin 1730 printed pamphlet on a London bookseller's counter, gentlemen in wigs leafing through copies" + SEM,
  "london_1717#médio-esq")
b("El secreto de los masones lleva casi trescientos años a la venta. Lo que nunca se agotó fue el miedo a lo que podían esconder.",
  "square_compass#detalhe-centro", "lodge_dark#médio-dir", "empty_road#aberto", ideia=True)
b("Y tú, ¿crees que una sociedad discreta es un peligro, o el peligro está en lo que imaginamos de ella? Déjalo en los comentarios. Y si quieres seguir con otro expediente, aquí tienes el completo de la Cosa Nostra.",
  "folder_close|A hand closing a thick brown case file with a red circular stamp on a dark desk, lamp light",
  "red_stamp#médio-esq", "carriage_night#aberto")

# a 1ª prova do 001 (04/11) saiu com moldura de papel: todo prompt leva sangria explícita
SANGRIA = ", full-bleed illustration filling the entire frame edge to edge, no border, no margin, no white frame, no panel outline"

# Thumbs (biblia/thumb.md): personagem à esquerda com objeto que conta o tema, metade direita livre. Símbolo: esquadro e compasso.
THUMBS = [
    {"id": "thumb-A", "prompt": "An 18th century Freemason in his fifties in half body on the LEFT third of the frame, powdered wig, dark coat and a white lambskin apron, holding a large brass square and compass crossed in front of his chest, stern stare at the viewer, behind him a candlelit lodge room with a black and white checkered floor and two tall columns; the RIGHT half of the image is plain dark empty wall in shadow, no symbols on the wall, no signage, no lettering"},
    {"id": "thumb-B", "prompt": "A man in his early fifties with sideburns and a worn dark 1820s frock coat in half body on the LEFT third of the frame, clutching a thick bundle of handwritten pages against his chest, frightened look over his shoulder, behind him a black horse-drawn carriage on a dark village road at night under the moon; the RIGHT half of the image is plain dark empty night sky, no signage, no lettering"},
    {"id": "thumb-C", "prompt": "A large worn brass square and compass emblem lying crossed on an old leather book on the LEFT third of the frame, lit by a single candle, a man's hand in a dark sleeve with a signet ring resting beside it, dark wooden table; the RIGHT half of the image is plain dark empty shadow, no symbols, no signage, no lettering"},
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
