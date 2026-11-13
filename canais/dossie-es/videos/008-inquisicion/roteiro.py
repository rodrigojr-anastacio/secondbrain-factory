#!/usr/bin/env python3
"""Fonte única do dossie-es 008 (La Inquisición): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (na pasta do vídeo). Conteúdo no topo; geração no fim (copiada do 007-ss).

Molde da bíblia (canais/dossie-es/biblia/roteiro.md): hook por anedota (Francisco Maldonado da Silva no auto de fe de Lima,
23/01/1639: os livros escritos na cela pendurados no pescoço, o redemoinho que arranca o toldo, a irmã que o denunciou)
→ 14 expedientes-objeto com título falado → pagamento da anedota no expediente 12 ("La Complicidad"; a cronologia manda,
como no FBI 003) → cierre "Los Libros" que volta ao objeto do hook + aforismo + pergunta.
Separação fato × lenda negra explícita: tortura com regras (sem descrição gráfica), donzela de ferro, "Decíamos ayer",
"Eppur si muove", Llorente (31.912) × Henningsen-Contreras (44 mil processos; ~1,8% executados) e a faixa 3.000–5.000.
Ângulo América Latina: Maldonado (Tucumán/Chile/Lima), Don Carlos de Texcoco (1539, por que os indígenas ficaram fora do
tribunal), tribunais de Lima, México e Cartagena, familiares, 1649 no México, Hidalgo (1810), saque do arquivo de Lima (1813).
Imagens: nada de tortura nem corpos; fogueira só como fumaça "seen from far away, no people in the fire"; sambenito liso
(o nano-banana escreve texto em túnica pintada); nada de capuz pontudo (lembra KKK).
Fatos conferidos em 13/11/2026 (ver SOURCES.md e FATOS-revisao.md).

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (id I### na ordem de aparição) · "chave" reuso · "chave#enq" reuso com enquadramento
  + "@@TEXTO"      rótulo na tela (máquina de escrever; CAIXA ALTA, até ~28 caracteres)
Bloco: b(texto, *planos, card="LIMA, 1639", ideia=True) · capítulo: cap("5. El Sambenito")
Mapas (chave map_*): base sem texto nem pinos; pinos, setas e nomes no código (src/labels.jsx).
"""
import json, math, re
from pathlib import Path

WPS = 2.38           # palavras/s medidas no 001–007 (erro de 1–3%)
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
TITULO = "TODA la historia de la Inquisición"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

SEM = ", no lettering anywhere"   # objetos com capa, placa ou papel: o nano-banana inventa texto
FOGO = ", seen from far away, only a column of smoke and a distant glow, no people visible in the fire, no bodies"
VIOL = ", seen from far away, no bodies, no blood"
NOHOOD = ", no pointed hoods, no conical hats"
# sambenito liso: a túnica pintada com chamas/diabos convida texto e imagem gráfica
SAMB = "a plain coarse yellow penitent's tunic with a simple red diagonal cross, no other symbols"
# Personagens (descrição visual fixa; rostos "resembling", nunca foto)
MALDONADO = "a thin surgeon in his mid forties with a long untidy dark beard streaked with grey, hollow cheeks and intense dark eyes"
GUI = "a Dominican friar in his fifties with a tonsure, a white habit and a black cloak, a calm severe face"
TORQUEMADA = "a gaunt elderly Dominican friar in his sixties resembling Tomás de Torquemada, a white habit and a black cloak with the hood down, a hard thin face"
REYES = "a Spanish queen in her late twenties resembling Isabella of Castile, auburn hair under a simple crown and veil, and a Spanish king of the same age resembling Ferdinand of Aragon, short dark hair, both in rich late 15th century robes"
ZUMARRAGA = "an elderly Franciscan bishop in a plain brown habit with a gold pectoral cross, a white beard, 1539"
DONCARLOS = "a Nahua nobleman in his thirties with long black hair and a proud face, a white cotton cloak knotted at the shoulder, 1539"
FRAYLUIS = "a Spanish Augustinian friar in his mid forties in a black habit, a broad strong face and a stern look, 1572, resembling Fray Luis de León"
SALAZAR = "a Spanish priest in his late forties in a black cassock with a white collar, a thoughtful tired face, 1611"
GALILEO = "an elderly Italian scholar of seventy resembling Galileo Galilei, a white beard, a dark scholar's robe, 1633"
RIPOLL = "a Spanish village schoolteacher in his late forties in plain dark early 19th century clothes, a calm open face, 1826"
LLORENTE = "a Spanish priest in his sixties with grey hair in a plain black early 19th century cassock, writing with a quill at a desk by a window, 1817"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, borders and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame"

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Lima, mil seiscientos treinta y nueve. Un cirujano de Tucumán escucha su sentencia.",
  "lima_plaza|The main square of colonial Lima in 1639 packed with a huge crowd, wooden stands draped in dark cloth, a cathedral facade behind, harsh summer light, seen from above",
  f"maldonado_stand|{MALDONADO}, wearing {SAMB}, standing on a wooden platform before a crowd, hands tied in front, listening",
  "tribunal_stand|A row of inquisitors in black and white robes seated under a large dark canopy on a wooden stage in a colonial square, a green cross on a table, 1639" + SEM, card="LIMA, 1639")
b("Lleva al cuello los libros que escribió en la cárcel.",
  f"books_neck|Close-up of small handmade notebooks tied with string hanging from the neck of {MALDONADO}, worn yellow cloth, the pages covered with tiny unreadable handwriting" + SEM,
  "bone_pen|Close-up of a crude improvised pen carved from a thin sliver of bone beside a scrap of paper and a pot of black ink in a stone prison cell, candlelight" + SEM)
b("Un remolino arranca el toldo. Él mira al cielo: según la crónica, dice que el Dios de Israel viene a verlo cara a cara.",
  "awning|A large dark canvas awning being torn away by a sudden whirlwind over a crowded Spanish colonial square in Lima in the 1630s, ropes snapping, dust in the air, people looking up, men in wide-brimmed hats, dark doublets and capes, women in long dark mantos, 17th century Spanish clothing only, no tricorn hats",
  f"looks_up|{MALDONADO} looking up at the sky with a serene face, wind in his beard, dust swirling, low angle",
  "toldo_detail|Close-up of a torn dark canvas awning flapping violently against a bright sky, broken ropes whipping in the wind",
  "crowd_up|A crowd of 17th century Spaniards in a colonial square shielding their faces from a gust of wind, hats flying")
b("Ese mismo día muere en la hoguera. Lo había denunciado su propia hermana.",
  "smoke_lima|A column of dark smoke rising behind the low colonial houses of Lima at dusk" + FOGO,
  "sister|Wide interior shot filling the whole frame, a young woman in a 17th century Spanish dress and dark shawl sitting alone by a window with lowered eyes, a candle beside her, Chile, 1620s")
b("Esta es TODA la historia de la Inquisición. Y de cómo hizo de cada vecino un testigo.",
  "files_desk|A long dark desk covered with open brown case files tied with red string and old handwritten parchment documents, a red wax seal and a magnifying glass, lamp light" + SEM,
  "red_stamp|A hand slamming a red rubber stamp onto a brown paper case file, ink splash, dramatic close-up" + SEM,
  "neighbors|Two 17th century Spanish neighbors whispering behind a half-open wooden shutter, watching someone in the street, dusk", ideia=True)

# ───────────────────────── 1. EL MANUAL ─────────────────────────
cap("1. El Manual")
b("El Manual. Toulouse, sur de Francia, hacia mil trescientos veintitrés. Un fraile dominico, Bernardo Gui, termina un libro para inquisidores.",
  "toulouse|The medieval city of Toulouse in the 1320s, red brick towers and a church above the river, morning mist",
  f"gui_writing|{GUI} writing in a large book by candlelight in a stone cell, a stack of parchments beside him" + SEM,
  f"gui_face|{GUI} in portrait, looking up from his book, candlelight, dark background@@BERNARDO GUI", card="TOULOUSE, 1323")
b("Explica cómo interrogar a cada tipo de acusado. Qué preguntar. Qué respuestas son trampas. Cómo descubrir a quien finge.",
  "interrogation_med|A medieval Dominican friar questioning a frightened peasant across a wooden table in a bare stone room, a scribe writing, candlelight",
  "scribe_med|Close-up of a medieval scribe's hand writing an interrogation record on parchment with a quill" + SEM,
  "peasant_face|Close-up of a frightened medieval peasant man in a rough tunic, sweat on his brow, candlelight")
b("La Inquisición no nace en España. Toma forma aquí, hacia mil doscientos treinta. El papa envía frailes contra los cátaros, cristianos que rechazaban a la Iglesia de Roma.",
  "languedoc|The rolling hills of Languedoc in southern France in the 13th century, a fortified village on a hill, vineyards, morning light",
  "map_europa|" + MAPA + ", the western Mediterranean region with Spain and Portugal on the left, France in the upper center and Italy on the right, the sea in the lower part, all ocean and sea areas completely blank without names",
  "pope_med|A medieval pope in white robes handing a sealed parchment with a red wax seal to two Dominican friars kneeling before him in a dim hall, 1230s" + SEM,
  "cathars|A small group of medieval men and women in plain dark robes praying quietly in a stone farmhouse in southern France, firelight")
b("Gui condena a más de seiscientas personas en quince años. Unas cuarenta terminan en la hoguera.",
  "sentence_read|A medieval friar reading a sentence from a parchment to a crowd in a church square in Toulouse, people kneeling",
  "smoke_med|A thin column of smoke rising outside the walls of a medieval town under a grey sky" + FOGO)
b("Durante más de dos siglos, la Inquisición es un tribunal del papa. Hasta que dos reyes piden una propia.",
  "centuries_friars|A long line of Dominican friars in white and black walking through a cloister of a medieval monastery, candles, dusk",
  "castile_palace|A medieval Castilian royal palace courtyard with horseback riders and banners arriving, 1470s" + NOHOOD + "",
  f"reyes|{REYES}, standing side by side in a stone palace hall, torchlight, 1478@@ISABEL Y FERNANDO", ideia=True)

# ───────────────────────── 2. LA BULA ─────────────────────────
cap("2. La Bula")
b("La Bula. Roma, primero de noviembre de mil cuatrocientos setenta y ocho. El papa Sixto cuarto firma un documento. Se lo han pedido Isabel de Castilla y Fernando de Aragón.",
  "vatican_hall|A Renaissance papal audience hall in Rome with frescoed walls, envoys of the Spanish crown in rich robes kneeling before the papal throne, 1478",
  "rome_1478|Rome in 1478, old churches and ruins along the Tiber, golden evening light",
  "sixtus|An elderly pope in white and red robes resembling Pope Sixtus IV signing a parchment at a heavy desk in a Renaissance chamber",
  "bull_seal|Close-up of a parchment papal bull with a hanging lead seal on a red silk cord, lying on dark velvet" + SEM, card="ROMA, 1478")
b("Les permite nombrar a sus propios inquisidores. Esta Inquisición depende de la Corona, no solo de Roma.",
  "inquisitors_named|Two Spanish friars in white and black kneeling before a king and queen who hand them a sealed letter in a palace hall, 1480",
  "crown_cross|A golden royal crown and a wooden cross lying side by side on a dark table next to a sealed parchment, candlelight" + SEM,
  "court_castile|The royal court of Castile in 1478, nobles and clerics gathered in a vaulted hall around a throne")
b("Quedan bajo sospecha los conversos: judíos bautizados, muchos a la fuerza, tras las matanzas de mil trescientos noventa y uno.",
  "conversos|A Spanish family in late 15th century clothes leaving a church after mass in Seville, neighbors watching them from a doorway",
  "baptism_force|A crowd forcing a group of frightened Jewish men and women toward a church door in a 14th century Spanish street" + VIOL,
  "juderia|A narrow street of the old Jewish quarter of Seville in the 15th century, whitewashed walls, empty")
b("Se los acusa de seguir con el judaísmo en secreto. El tribunal los llama judaizantes.",
  "secret_candles|Close-up of two candles lit in secret behind a closed shutter in a 15th century Spanish house on a Friday evening, a woman's hands",
  "eyes_door|An eye watching through a crack in a wooden door into a dim room, 15th century Spain")
b("En mil cuatrocientos ochenta llegan a Sevilla los primeros inquisidores. Un año después, la ciudad ve su primer auto.",
  "seville_gate|The great city gate of Seville in 1480 with crowds, carts and guards, the Guadalquivir river beside it",
  "triana_castle|The old castle of Triana on the river bank opposite Seville in 1480, grey stone walls, boats on the river",
  "friars_seville|Two Dominican friars on mules arriving at the gates of Seville in 1480, the Giralda tower behind, autumn light", ideia=True)

# ───────────────────────── 3. EL PRIMER AUTO ─────────────────────────
cap("3. El Primer Auto")
b("El Primer Auto. Sevilla, seis de febrero de mil cuatrocientos ochenta y uno. Seis personas mueren en la hoguera a las afueras de la ciudad.",
  "seville_1481|Seville in 1481, the cathedral under construction and the Giralda tower above the city, grey winter morning",
  "procession|A solemn procession of friars carrying a green cross through a Seville street in 1481, condemned people in plain yellow tunics walking behind with candles, a silent crowd" + NOHOOD,
  "smoke_seville|A column of smoke rising in a field outside the walls of Seville at dawn" + FOGO, card="SEVILLA, 1481")
b("Es el primer auto de fe de la Inquisición española: una ceremonia pública en la que se leen las sentencias ante la multitud.",
  "scroll_reading|Close-up of a friar's hands in a wide black wool sleeve unrolling a long scroll on a wooden lectern, a crowd in 15th century clothing blurred behind, no suit, no cuffs, no buttons" + SEM + "",
  "auto_stage|A wooden stage in a Spanish town square with a notary reading sentences from a long scroll to a large crowd, 15th century" + SEM,
  "crowd_listen|Faces of a crowd of 15th century Spaniards listening in silence in a town square, men, women and children")
b("El tribunal no ejecuta a nadie. Entrega al condenado a la justicia del rey, que lo lleva a la hoguera. Lo llama «relajar».",
  "halberds|Close-up of royal guards' halberds and helmets in a crowded 15th century Spanish square, grey light",
  "handover|A friar in white and black stepping back as royal soldiers with halberds take a condemned man in a plain yellow tunic by the arms, a town square",
  "soldiers_walk|Royal soldiers with halberds leading a man in a plain yellow tunic out through a town gate, seen from behind")
b("En mil cuatrocientos ochenta y tres, un fraile dominico se convierte en inquisidor general: Tomás de Torquemada.",
  "monastery_avila|A severe stone Dominican monastery in Castile in the 1480s, cloister arches, cold winter light",
  f"torquemada|{TORQUEMADA} in portrait, a dark stone corridor behind him, cold light@@TOMÁS DE TORQUEMADA",
  f"torquemada_desk|{TORQUEMADA} reading documents at a long table in a monastery, candles" + SEM)
b("Según los historiadores, hasta mil quinientos treinta el tribunal envía a la hoguera a unas dos mil personas. Casi todos, conversos.",
  "converso_family|A frightened converso family in late 15th century clothes gathered around a table at night, a closed shutter, a single candle",
  "ledger_1500|Close-up of an old leather-bound register open on a desk, columns of handwritten names, a quill and a candle" + SEM,
  "town_smoke|A Spanish hill town seen from far away at dusk, a thin column of smoke rising near its walls" + FOGO)
b("Y en cada ciudad donde abre un tribunal se lee primero el mismo papel.",
  "town_church|A whitewashed Spanish village church with a bell tower on a dusty square in the early 16th century, villagers walking to the door",
  "edict_paper|Close-up of a long handwritten parchment edict nailed to the wooden door of a Spanish church" + SEM, ideia=True)

# ───────────────────────── 4. EL EDICTO ─────────────────────────
cap("4. El Edicto")
b("El Edicto. Cuando la Inquisición llega a un pueblo, reúne a los vecinos en la iglesia y lee el edicto de fe.",
  "bell_ring|A church bell ringing in a stone bell tower above a Spanish village, pigeons flying, early 16th century",
  "church_reading|Inside a crowded Spanish village church in the 16th century, a priest reading a long document from the pulpit to the villagers" + SEM,
  "villagers_pews|Spanish villagers in 16th century clothes sitting tense on church benches, glancing at each other")
b("El edicto enumera lo que el tribunal considera señales de judaísmo. Quien no come cerdo. Quien se pone ropa limpia el sábado.",
  "pork_plate|A plate of pork pushed aside untouched on a rustic 16th century Spanish table, a family eating bread",
  "clean_linen|A woman folding clean white linen shirts on a Saturday morning in a 16th century Spanish house, light through a small window")
b("Quien sepa de alguien así está obligado a denunciarlo. Según el edicto, callar también es delito.",
  "denounce|A man in 16th century clothes whispering into the ear of a seated notary in a dark office, the notary writing" + SEM,
  "notary_writes|Close-up of a notary's hand writing a denunciation on paper by candlelight" + SEM)
b("El acusado no sabe quién lo denunció. Sus bienes quedan embargados desde el día del arresto. Si lo condenan, el tribunal se los queda.",
  "arrest_night|Officers of the Inquisition with lanterns knocking at a house door at night in a Spanish town, a family in nightclothes inside",
  "inventory|A clerk making an inventory of furniture, silver and books in an empty house, officers carrying chests out" + SEM)
b("La tortura existía, con reglas y un médico presente. Según los historiadores, se aplicaba a una minoría, menos que en muchos tribunales civiles. Seguía siendo tortura.",
  "dungeon_empty|An empty stone dungeon corridor with iron doors and a single torch, no people",
  "doctor_waits|A 16th century physician in black waiting on a bench in a stone corridor, holding his bag, looking at the floor")
b("Y las doncellas de hierro de los museos son invenciones posteriores. El castigo más común era otro.",
  "museum_iron|A dusty 19th century museum room with glass cases and odd metal objects, visitors looking, gaslight", ideia=True)

# ───────────────────────── 5. EL SAMBENITO ─────────────────────────
cap("5. El Sambenito")
b("El Sambenito. Una túnica amarilla con una cruz roja en forma de equis.",
  f"sambenito|A man in {SAMB} standing alone in a church doorway, villagers staring at him, 16th century Spain",
  "tunic_close|Close-up of a coarse yellow cloth tunic with a red diagonal cross folded on a wooden chest" + SEM)
b("El penitente la lleva puesta en público durante meses o años.",
  f"market|A man wearing {SAMB} walking through a Spanish market, people turning away from him",
  f"mass_samb|A man in {SAMB} kneeling apart from the others at the back of a village church during mass")
b("Cuando termina la pena, el sambenito no desaparece. Se cuelga en la iglesia del pueblo, con el nombre y el delito del condenado.",
  "hung_tunics|A row of old yellow tunics with red crosses hanging high on the stone wall of a Spanish village church, small blank wooden plaques beneath them, dim light" + SEM,
  "child_looks|A small boy in 16th century clothes looking up at old yellow tunics hanging on a church wall")
b("Ahí queda para siempre. La vergüenza pasa a los hijos y a los nietos.",
  "family_shame|A 16th century Spanish family walking past their neighbors in a village street, heads lowered, neighbors whispering")
b("Por eso, en español, a quien carga con una mala fama se le cuelga un sambenito.",
  "hung_tunics#detalhe-centro")

b("Y rige otro filtro, que la época llama limpieza de sangre. Para muchos cargos hay que probar que no se desciende de judíos ni de musulmanes.",
  "pureza|A young man in a black 16th century suit standing before a panel of officials who examine old genealogical documents at a long table" + SEM,
  "genealogy|An old hand-drawn family tree on yellowed parchment spread on a desk, a magnifying glass over it, the names unreadable" + SEM, ideia=True)

# ───────────────────────── 6. EL DECRETO ─────────────────────────
cap("6. El Decreto")
b("El Decreto. Granada, treinta y uno de marzo de mil cuatrocientos noventa y dos. Isabel y Fernando firman la expulsión de los judíos que no se bauticen.",
  "alhambra|The Alhambra palace in Granada in 1492, red walls on the hill, the snowy Sierra Nevada behind, spring light",
  "signing|A Spanish queen and king seated at a table in a Moorish palace hall signing a parchment, courtiers standing behind, 1492" + SEM, card="GRANADA, 1492")
b("Tienen hasta finales de julio para irse. No pueden llevarse oro ni plata.",
  "leaving|Jewish families with carts, mules and bundles leaving a Spanish town through its gate in summer 1492, seen from behind",
  "keys|Close-up of an old man's hand holding a large iron house key, a cart behind him, 1492")
b("Los historiadores no coinciden en cuántos se fueron: entre unas cuarenta mil y más de cien mil personas.",
  "keys#detalhe-centro",
  "port_1492|A crowded Spanish harbor in 1492, families boarding small sailing ships with their bundles, seen from far away",
  "map_exilio|" + MAPA + ", the whole Mediterranean with Spain and Portugal at the far left edge, Italy, Greece and Turkey in the middle, Morocco and North Africa below, all sea areas completely blank without names")
b("Otros se bautizan para quedarse. Y cada nuevo bautizado es, para el tribunal, un sospechoso más.",
  "baptism_group|A priest baptizing a line of Jewish men and women at a church font in 1492, their faces sad",
  "eyes_door#detalhe-centro")
b("Ese mismo año, Colón llega a las Antillas. En América, antes que el tribunal, actuará un obispo.",
  "caravels|Three small sailing ships of 1492 on the open Atlantic Ocean at dawn, seen from far away",
  "map_atlantico|" + MAPA + ", the Atlantic Ocean between Spain and the Americas, Mexico and the Caribbean on the left", ideia=True)

# ───────────────────────── 7. EL CACIQUE ─────────────────────────
cap("7. El Cacique")
b("El Cacique. Ciudad de México, treinta de noviembre de mil quinientos treinta y nueve. Muere en la hoguera don Carlos Ometochtzin, señor indígena de Texcoco.",
  "mexico_1539|Mexico City in 1539, a new Spanish square with a church under construction on top of Aztec ruins, volcanoes in the distance",
  f"don_carlos|{DONCARLOS} in portrait, a colonial wall behind him@@DON CARLOS DE TEXCOCO",
  "smoke_mexico|A column of smoke rising over a crowded colonial square in early Mexico City" + FOGO, card="MÉXICO, 1539")
b("Lo juzga el obispo fray Juan de Zumárraga, con poderes de inquisidor.",
  "texcoco|The lakeside town of Texcoco in the 1530s, low white houses, old temple platforms and fields, the lake behind",
  f"zumarraga|{ZUMARRAGA} seated in a carved chair in a bare colonial hall, reading a document, no lettering anywhere@@FRAY JUAN DE ZUMÁRRAGA")
b("Lo acusan de «hereje dogmatizante»: de decir a los suyos que dejaran la fe de los españoles.",
  f"carlos_speaks|{DONCARLOS} speaking passionately to a small group of Nahua men in white cloaks at night by a fire",
  "witnesses|Nahua witnesses in white cloaks standing before a Spanish friar and a scribe in a colonial room, 1539" + SEM)
b("En España la sentencia cae mal. La Corona reprende a Zumárraga. Pocos años después, él pierde esos poderes.",
  "council_indies|Spanish officials of the Council of the Indies in black robes reading a letter around a table in a dark Madrid hall" + SEM,
  "letter_seal|Close-up of a folded letter with a red wax seal on a dark wooden table" + SEM)
b("Cuando el Santo Oficio se instala en América, los indígenas quedan fuera de su jurisdicción, por ser nuevos en la fe. Siguen bajo la justicia de los obispos.",
  "native_church|Nahua men and women in white cloaks attending mass in an open chapel in 16th century Mexico",
  "bishop_native|A colonial bishop's notary questioning a Nahua man in a small parish office, a friar translating" + SEM)
b("El tribunal perseguirá a otros: españoles, portugueses de origen converso, mestizos y africanos.",
  "colonial_street|A busy colonial street in 16th century Mexico City with Spaniards, mestizos and enslaved Africans carrying loads, a church behind",
  "dominican_watch|A Dominican friar watching the crowd from the steps of a colonial church")
b("Mientras tanto, en España, el tribunal vigila también otra cosa: los libros.",
  "books_pile|A pile of old leather books on a stone floor in a dim hall, a friar's hand picking one up" + SEM, ideia=True)

# ───────────────────────── 8. EL ÍNDICE ─────────────────────────
cap("8. El Índice")
b("El Índice. Valladolid, mil quinientos cincuenta y nueve. El inquisidor general Fernando de Valdés publica una lista de libros prohibidos.",
  "valladolid|Valladolid in 1559, a stone plaza with arcades and church towers, overcast sky",
  "valdes|An elderly Spanish archbishop in a black cassock and red cap examining a printed list at a desk piled with books" + SEM,
  "index_book|Close-up of a thin printed book opened on a table, rows of tiny unreadable printed titles, some crossed out in ink" + SEM, card="VALLADOLID, 1559")
b("Entran Biblias en lengua común, obras de Erasmo y hasta el Lazarillo de Tormes.",
  "bibles|Old Bibles and printed books being stacked into a wooden crate by friars in a library" + SEM,
  "censor_ink|Close-up of a censor's hand crossing out lines in a printed book with black ink" + SEM,
  "bookshop|A 16th century Spanish bookshop with books on wooden shelves, a friar inspecting them while the bookseller watches")
b("Ni los frailes se salvan. En mil quinientos setenta y dos, fray Luis de León, profesor en Salamanca, es detenido. Entre los cargos: haber traducido el Cantar de los Cantares.",
  "salamanca|The University of Salamanca in 1572, golden sandstone courtyard, students in black gowns",
  f"fray_luis|{FRAYLUIS} in portrait, a lecture hall behind him@@FRAY LUIS DE LEÓN",
  f"luis_arrest|Officers leading {FRAYLUIS} out of a stone university building, students watching")
b("Pasa casi cinco años preso y sale absuelto. Según la tradición, vuelve a su aula y dice: «Decíamos ayer». No hay prueba de que lo dijera.",
  "luis_cell|A friar in a black habit writing by a small barred window in a stone prison cell, candlelight",
  "lecture_hall|An old wooden university lecture hall in Salamanca with rows of benches full of students and a high pulpit, a friar in black climbing to it, warm light")
b("El tribunal ya controla lo que se lee en España. El rey quiere lo mismo al otro lado del mar.",
  "map_atlantico#médio-esq", ideia=True)

# ───────────────────────── 9. EL TRIBUNAL ─────────────────────────
cap("9. El Tribunal")
b("El Tribunal. Felipe segundo lleva el Santo Oficio a América. Abre en Lima en mil quinientos setenta y en México en mil quinientos setenta y uno.",
  "philip|An austere Spanish king in his forties in black clothes resembling Philip II, signing a document at a desk in a dark room" + SEM,
  "lima_1570|Colonial Lima in 1570, a new grid of low adobe houses and churches by the river, dry hills behind",
  "tribunal_hall|The audience hall of the Inquisition in colonial Lima, a long table with a green cross and candles under a carved wooden ceiling, empty" + SEM, card="LIMA, 1570")
b("El de Lima vigila casi toda la Sudamérica española, de Quito a Chile y el Río de la Plata.",
  "map_sudamerica|" + MAPA + ", the whole of South America and Panama, with plain empty blue oceans on both sides, no ocean names, no lettering anywhere on the water")
b("En mil seiscientos diez abre un tercero en Cartagena de Indias, el gran puerto de esclavos del Caribe.",
  "cartagena|The walled port of Cartagena de Indias in the 17th century, ships in the bay, fortress walls, tropical light",
  "cartagena_port|Enslaved Africans being unloaded from a ship at the docks of Cartagena in the 17th century, seen from far away, Spanish officials watching")
b("Ahí persigue sobre todo lo que llama brujería, además de blasfemia y bigamia. Entre los acusados hay muchos africanos, esclavizados y libres.",
  "accused_women|Two African women in simple colonial clothes standing before inquisitors at a table in a hot whitewashed room in Cartagena, a scribe writing" + SEM,
  "herbs|Close-up of dried herbs, small bones and a clay bowl on a wooden table, evidence in a colonial courtroom" + SEM)
b("Los tribunales tienen una red de colaboradores civiles, los llamados familiares. Vigilan y denuncian.",
  "familiar|A prosperous colonial merchant in a black suit with a small green cross medal on his chest, watching a street from a balcony, 17th century Lima",
  "familiar_tells|A man in a black 17th century suit reporting quietly to an inquisitor at a doorway at night, a lantern")
b("Si te gustan estos expedientes, suscríbete. Cada semana abrimos uno nuevo.",
  "folder_open|A hand opening a thick brown case file on a dark desk under lamp light, old documents inside" + SEM)
b("Ese mismo año, mil seiscientos diez, en el norte de España, el tribunal abre su mayor proceso por brujería.",
  "pyrenees|The green misty mountains of Navarre in northern Spain, a small stone village in a valley, 1610", ideia=True)

# ───────────────────────── 10. LAS BRUJAS ─────────────────────────
cap("10. Las Brujas")
b("Las Brujas. Logroño, noviembre de mil seiscientos diez. Un auto de fe juzga a vecinos de Zugarramurdi, un pueblo de Navarra, acusados de brujería.",
  "logrono|The town of Logroño in 1610 by the river Ebro, a stone bridge and church towers, a crowd gathering",
  "zugarramurdi|A small Basque village of stone houses with wooden balconies near a large cave in green hills, 1610",
  "cave|The wide mouth of a large natural cave in green hills in the Basque country, mist, no people", card="LOGROÑO, 1610")
b("Seis son quemados en persona. Otros cinco, que murieron en la cárcel, arden en efigie: muñecos que los representan.",
  "smoke_logrono|Smoke rising beyond the rooftops of Logroño on a cold November day" + FOGO,
  "effigies|Rough life-size straw and cloth figures dressed in plain yellow tunics, carried on poles through a crowd, 1610" + NOHOOD)
b("Uno de los inquisidores, Alonso de Salazar y Frías, recorre la región durante meses.",
  f"salazar|{SALAZAR} in portrait, mountains behind him@@ALONSO DE SALAZAR Y FRÍAS",
  f"salazar_ride|{SALAZAR} riding a mule along a mountain path in Navarre with a secretary, mist")
b("Escucha a unas mil ochocientas personas que confiesan o acusan. Muchos son niños.",
  f"salazar_listen|{SALAZAR} listening to a Basque peasant woman in a village house, a secretary writing, children waiting at the door" + SEM,
  "children_line|A line of Basque village children in 1611 waiting outside a stone house, some holding their mothers' hands")
b("Su informe dice que no encontró ni una prueba. Y concluye que no hubo brujos ni embrujados hasta que se empezó a hablar y escribir de ellos.",
  "report_salazar|Close-up of a thick handwritten report tied with string on a desk, a quill and a candle" + SEM)
b("En mil seiscientos catorce, la Suprema, el consejo del tribunal, adopta sus criterios. Desde entonces, en España casi no se quema a nadie por brujería. En el resto de Europa, los tribunales, sobre todo civiles, ejecutan a decenas de miles. Y en Roma, otra Inquisición juzgará a un hombre por mirar al cielo.",
  "suprema|A council of elderly clerics in black around a long table in a Madrid hall reading a report by candlelight" + SEM,
  "europe_witch|A German town square in the early 17th century with a crowd gathered, smoke rising behind the houses" + FOGO, ideia=True)

# ───────────────────────── 11. EL TELESCOPIO ─────────────────────────
cap("11. El Telescopio")
b("El Telescopio. Roma, veintidós de junio de mil seiscientos treinta y tres. Galileo Galilei, de sesenta y nueve años, se arrodilla ante la Inquisición romana.",
  "rome_1633|Rome in 1633, the dome of Saint Peter's above the rooftops, summer light",
  f"galileo_kneel|{GALILEO} kneeling in a white penitent's shirt before a row of cardinals in red seated in a vaulted hall@@GALILEO GALILEI", card="ROMA, 1633")
b("Galileo había defendido que la Tierra gira alrededor del Sol. Lo obligan a abjurar y lo condenan a prisión. La pena se convierte en arresto domiciliario hasta su muerte.",
  "telescope|Close-up of an old brass and leather telescope on a wooden table beside drawings of the moon" + SEM,
  "solar_system|An old hand-drawn diagram of the sun at the center with planets in circles on yellowed paper" + SEM,
  f"galileo_villa|{GALILEO} sitting alone by the window of a villa in the Tuscan hills at dusk")
b("Treinta y tres años antes, la misma Inquisición había condenado a la hoguera, en Roma, al filósofo Giordano Bruno.",
  "campo_fiori|A Roman square at dawn in 1600 with a crowd, smoke rising in the middle" + FOGO)
b("Según la leyenda, al levantarse, Galileo murmura: «Y sin embargo, se mueve». La frase aparece impresa por primera vez en mil setecientos cincuenta y siete.",
  "galileo_kneel#detalhe-centro",
  "old_print|Close-up of an old 18th century printed book open on a desk, unreadable lines of print" + SEM)
b("En mil novecientos noventa y dos, el papa Juan Pablo segundo reconoce que los teólogos que juzgaron a Galileo se equivocaron.",
  "pope_1992|An elderly pope in white robes speaking at a podium in a grand Vatican hall, 1992, seen from far away")
b("Seis años después de Galileo, en Lima, un auto de fe paraliza la ciudad. Volvemos al cirujano de Tucumán.",
  "lima_plaza#médio-dir", ideia=True)

# ───────────────────────── 12. LA COMPLICIDAD ─────────────────────────
cap("12. La Complicidad")
b("La Complicidad. Francisco Maldonado da Silva nació en Tucumán hacia mil quinientos noventa y dos. Su padre, médico portugués de familia conversa, ya había pasado por la Inquisición.",
  "tucuman|A small Spanish colonial town in Tucumán at the end of the 16th century, adobe houses, a church, green mountains behind",
  f"maldonado_young|A young man in his twenties with a short dark beard reading an old book by candlelight in a modest colonial room, 1610s",
  f"maldonado_face|{MALDONADO} in portrait, a stone wall behind him@@FRANCISCO MALDONADO DA SILVA")
b("Lo crían católico. Pero de joven lee, estudia y decide volver, en secreto, a la fe de sus abuelos.",
  "maldonado_young#detalhe-centro",
  "old_books|Old Latin books open on a table in a colonial house, a candle burning low" + SEM)
b("En Chile se lo confiesa a su hermana Isabel. Ella lo denuncia, empujada por su confesor. En mil seiscientos veintisiete, lo detienen.",
  "sister#médio-esq",
  "concepcion_arrest|Two 17th century Spanish officers in leather jerkins and plain steel morion helmets arresting a bearded surgeon in a plain linen shirt in his doorway in a small Chilean colonial town, his wife and child watching, 1627, no red cross, no bag, no modern uniform", card="CHILE, 1627")
b("Pasa casi doce años preso. Ayuna, discute con los teólogos y no se retracta.",
  f"cell_writing|{MALDONADO} writing with a bone pen in a dim stone prison cell, thin from fasting",
  "theologians|Three theologians in black and white robes arguing with a gaunt bearded prisoner across a table in a prison room" + SEM,
  "bone_pen#detalhe-centro")
b("Al mismo auto llegan decenas de portugueses de Lima. El tribunal los acusa de una supuesta conspiración judía, que llama la complicidad grande. Entre ellos, el rico mercader Manuel Bautista Pérez.",
  "merchants|Wealthy Portuguese merchants in black 17th century suits being led in a line through a Lima street by officers",
  "perez_house|A grand colonial mansion in Lima with carved wooden balconies, men in 17th century leather jerkins and plain steel morion helmets carrying out chests of silver, 1635, no bicorn hats, no green coats")
b("El veintitrés de enero de mil seiscientos treinta y nueve, el tribunal entrega a la hoguera a once personas. Entre ellas, Maldonado y Bautista Pérez. Confisca fortunas enteras.",
  "lima_plaza#detalhe-alto", "smoke_lima#médio-esq", "inventory#detalhe-centro")
b("Diez años después, en la Ciudad de México, el gran auto de fe de mil seiscientos cuarenta y nueve juzga a ciento nueve personas. Tomás Treviño de Sobremonte es el único que va vivo a la hoguera.",
  "mexico_1649|The vast main square of Mexico City in 1649 filled with tens of thousands of people around wooden stands, the cathedral under construction",
  "smoke_mexico#detalhe-centro", card="MÉXICO, 1649")
b("En el siglo dieciocho los autos se vuelven raros. Pero el tribunal sigue en pie hasta el siglo diecinueve. Y su última víctima es un maestro.",
  "schoolhouse|A small whitewashed village schoolhouse in the Valencia countryside in the 1820s, a teacher at the door, children arriving, morning light", ideia=True)

# ───────────────────────── 13. EL MAESTRO ─────────────────────────
cap("13. El Maestro")
b("El Maestro. Valencia, veintiséis de julio de mil ochocientos veintiséis. Cayetano Ripoll, un maestro de escuela, es ahorcado.",
  "valencia|Wide cinematic shot of a Valencia street in 1826 with a gothic tower rising behind rooftops, summer morning, a silent crowd of townspeople filling the foreground, detailed background on every side, nothing on a white background",
  f"ripoll|{RIPOLL} in portrait, a simple classroom behind him@@CAYETANO RIPOLL", card="VALENCIA, 1826")
b("Lo acusan de deísmo: de enseñar a sus alumnos sin misa ni oraciones. Lo juzga una Junta de Fe, que muchos ven como la Inquisición con otro nombre. Es la última ejecución por herejía en España.",
  "classroom_1826|A simple village classroom in 1826 in Spain, children on benches, a teacher at a blackboard with simple drawings" + SEM,
  "newspapers|Readers in a Paris café of 1826 reading newspapers with shocked faces" + SEM)
b("Para entonces, el tribunal ya se tambalea. Napoleón lo suprime en mil ochocientos ocho, y las Cortes de Cádiz, en mil ochocientos trece. Fernando séptimo lo restaura en mil ochocientos catorce.",
  "napoleon_troops|French soldiers of 1808 marching through the gate of a Spanish city, seen from far away",
  "cadiz|The Cortes of Cádiz in session in 1812, deputies in a crowded church hall, a speaker at a podium",
  "ferdinand7|A Spanish king in his thirties resembling Ferdinand VII, a heavy jaw, in a dark coat with a sash, standing in a palace")
b("En América, en mil ochocientos diez, un edicto de la Inquisición de México acusa de hereje al cura Miguel Hidalgo, que acababa de iniciar la guerra de independencia.",
  "hidalgo|An elderly Mexican priest with white hair resembling Miguel Hidalgo, in a black cassock, ringing a church bell at dawn, 1810@@MIGUEL HIDALGO",
  "edict_hidalgo|An edict nailed to a church door in a Mexican town in 1810, people gathering to read it" + SEM)
b("Y en Lima, en mil ochocientos trece, al conocerse la abolición, una multitud entra en la sede del tribunal. Según el escritor Ricardo Palma, saquea su archivo.",
  "lima_sack|A crowd bursting into the colonial courtyard of the Inquisition building in Lima in 1813, papers flying in the air, people carrying bundles of documents",
  "papers_floor|Old handwritten documents scattered on a stone floor in an empty colonial hall" + SEM, card="LIMA, 1813")
b("El quince de julio de mil ochocientos treinta y cuatro, la Inquisición española queda abolida para siempre.",
  "decree_1834|A Spanish official in 1834 sealing a printed decree with red wax at a desk" + SEM)
b("Lo que deja no son solo cenizas. Deja papeles.",
  "archive_rows|A vast old archive room with endless shelves of bundled documents tied with string, dust in the light" + SEM, ideia=True)

# ───────────────────────── 14. EL ARCHIVO ─────────────────────────
cap("14. El Archivo")
b("El Archivo. París, mil ochocientos diecisiete. Juan Antonio Llorente, que había sido secretario de la Inquisición, publica su historia del tribunal.",
  "paris_1817|Paris in 1817, the Seine with stone bridges and old buildings, grey morning",
  f"llorente|{LLORENTE}@@JUAN ANTONIO LLORENTE", card="PARÍS, 1817")
b("Calcula casi treinta y dos mil quemados en persona. La cifra recorre Europa y alimenta la llamada leyenda negra.",
  "llorente_book|Close-up of thick old printed volumes stacked on a desk in a 19th century study" + SEM,
  "black_legend|A 19th century European engraver's workshop with dark dramatic prints of inquisition scenes pinned on the walls, no readable text" + SEM)
b("En mil novecientos ochenta y seis, los historiadores Gustav Henningsen y Jaime Contreras estudian los resúmenes de unos cuarenta y cuatro mil procesos, entre mil quinientos cuarenta y mil setecientos.",
  "historians|Two historians in 1970s clothes reading old bundled documents at a long table in a Spanish archive, lamp light" + SEM,
  "archive_rows#médio-dir")
b("Menos de dos de cada cien terminan en la hoguera en persona. Los cálculos modernos del total en España van de unos tres mil a unos diez mil ejecutados.",
  "abacus_counts|Close-up of a historian's hand writing tallies in a notebook beside an open bundle of old documents" + SEM,
  "ledger_1500#detalhe-centro")
b("En América, los tres tribunales juntos envían a la hoguera a menos de cien personas.",
  "map_sudamerica#detalhe-centro")
b("Menos que la leyenda. Pero el número no mide el miedo. Según el historiador Ricardo García Cárcel, unas ciento cincuenta mil personas pasaron por sus procesos.",
  "neighbors#médio-dir", "villagers_pews#detalhe-centro")
b("En el año dos mil, el papa Juan Pablo segundo pidió perdón por la intolerancia y la violencia que algunos cristianos usaron al servicio de la verdad.",
  "vatican|Saint Peter's Square in the Vatican today seen from far away, morning light",
  "pope_2000|An elderly pope in white robes praying before a large crucifix in Saint Peter's Basilica, 2000, seen from far away")
b("Y en Lima, la sede del tribunal sigue en pie.",
  "tribunal_hall#médio-esq", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. Los Libros")
b("Los Libros. Lima, hoy. En la sede del antiguo tribunal, junto a la plaza Bolívar, funciona un museo.",
  "lima_today|The colonial building of the old Inquisition in central Lima today, a white facade with columns on a square with palm trees, sunny",
  "museum_today|Visitors walking through the old audience hall of the Inquisition museum in Lima today, a carved wooden ceiling", card="LIMA, HOY")
b("Los libros que Maldonado llevaba al cuello ardieron con él. Lo que sabemos de su vida viene de los papeles del propio tribunal, que lo anotaba todo.",
  "books_neck#detalhe-centro", "files_desk#médio-esq")
b("La leyenda exageró las cifras. Pero el daño no se mide solo en muertos. Durante tres siglos, la Inquisición enseñó que cualquiera podía ser un testigo. Incluso tu hermana.",
  "sister#detalhe-centro", "neighbors#detalhe-alto", "awning#aberto", ideia=True)
b("Y tú, ¿qué te sorprendió más: lo que la leyenda exageró o lo que confirman los archivos? Déjalo en los comentarios. Y si quieres otro expediente, aquí tienes el de los masones.",
  "folder_close|A hand closing a thick brown case file with a red circular stamp on a dark desk, lamp light" + SEM,
  "red_stamp#médio-esq", "lima_plaza#aberto")

# a 1ª prova do 001 (04/11) saiu com moldura de papel: todo prompt leva sangria explícita
SANGRIA = ", full-bleed illustration filling the entire frame edge to edge, no border, no margin, no white frame, no panel outline"

# Thumbs (biblia/thumb.md): personagem à esquerda com objeto que conta o tema, metade direita livre; nada de capuz pontudo nem fogueira com gente.
THUMBS = [
    {"id": "thumb-A", "prompt": f"{TORQUEMADA}, in half body on the LEFT third of the frame, holding up a rolled parchment with a large red wax seal, cold stare at the viewer, behind him a dark candlelit stone tribunal hall with a green cross on a table; the RIGHT half of the image is plain dark empty stone wall in shadow" + NOHOOD + SEM},
    {"id": "thumb-B", "prompt": "A Spanish man in a black 17th century suit and white ruff in half body on the LEFT third of the frame, whispering behind his hand toward the viewer with a sly look, a folded paper note in his other hand, behind him a dim colonial street at night with a lantern and a half-open shutter; the RIGHT half of the image is plain empty dark night wall" + NOHOOD + SEM},
    {"id": "thumb-C", "prompt": f"{MALDONADO}, wearing {SAMB}, two small old hand-sewn leather-bound books hanging from his neck on cords (no spiral binding, no modern notebooks), in half body on the LEFT third of the frame, looking up at the sky with a defiant face, wind in his beard, behind him a crowd in 17th century Spanish colonial clothing in a plaza of Lima with a cathedral and a dark awning torn by the wind; the RIGHT half of the image is plain empty pale dusty sky" + NOHOOD + SEM},
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
