#!/usr/bin/env python3
"""Fonte única do dossie-es 015 (El GRU): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py (na pasta do vídeo). Geração copiada do 014-yakuza.

Embalagem aprovada no crivo r3 (22/11/2026, EMBALAGEM.md/CRIVO.md):
  A/T1 "El Empresario Uruguayo que Espiaba para Moscú | Expedientes Secretos del GRU" + matrioska (empresário → oficial soviético), GRU + sello GULAG (objeto-simbolo, controle)
  B/T2 "GRU: la fábrica rusa de latinoamericanos" + Putin aperta a mão de um homem na pista de Vnukovo, ¿BRASILEÑO? (cena-acao)
  C/T3 "Cómo el GRU convirtió a sus espías en uruguayos, peruanos y brasileños" + 3 passaportes com a janela da foto vazia, NUNCA NACIERON (documento-evidencia)
Ângulo (ANGULO.md): los latinoamericanos que el GRU fabricó (uruguayo 1936–42, peruana 2005–18, brasileños 2022, "fantasmas" 2025).

Sintaxe dos planos (campo s): "chave|prompt" nova · "chave" reuso · "chave#enq" reuso com enquadramento · + "@@TEXTO" rótulo.
"""
import json, math, re
from pathlib import Path

WPS = 2.38           # palavras/s medidas no 001–014 (erro de 1–3%)
BREAK, LONG = 0.35, 0.8
MAX_PLANO_INICIO = 3.0   # s por plano nos primeiros INICIO s (~20 cortes/min)
INICIO = 60.0
MAX_PLANO = 3.6      # s por plano depois (~17 cortes/min)
INEDITO_ATE = 180.0  # s: só imagens novas até aqui
JANELA = 60.0        # s: mesmo enquadramento da mesma imagem só depois disso
HOOK_MAX = 47.0      # s: EMBALAGEM: frase-âncora (com a pista de Moscou) até ~0:45
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "El Empresario Uruguayo que Espiaba para Moscú | Expedientes Secretos del GRU"
TITULOS = ("T1 El Empresario Uruguayo que Espiaba para Moscú | Expedientes Secretos del GRU / "
           "T2 GRU: la fábrica rusa de latinoamericanos / "
           "T3 Cómo el GRU convirtió a sus espías en uruguayos, peruanos y brasileños")
PROMESSA = ("La historia entera del GRU, de 1918 a hoy, contada por los latinoamericanos falsos que fabricó: un 'empresario uruguayo' "
            "en Bruselas (1939), una 'peruana' en Nápoles (2018) y dos 'brasileños' en La Haya y Noruega (2022), y cómo se armó y cayó cada identidad.")

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Bruselas, mil novecientos cuarenta y uno. Un joven empresario uruguayo, Vincente Sierra, dirige una empresa de importación y exportación.", card="BRUSELAS, 1941")
b("Su mejor cliente es la Organización Todt, la constructora de obras del régimen nazi. En los papeles, es un hombre de negocios más.")
b("Pero Vincente Sierra no es uruguayo. Su pasaporte se emitió en Nueva York. Es oficial de la inteligencia militar soviética.")
b("Esta es TODA la historia del GRU, el espionaje militar ruso. Y de los latinoamericanos falsos que, según gobiernos e investigadores, fabricó: un uruguayo, una peruana, dos brasileños. A uno de ellos, Putin lo esperaría en la pista de un aeropuerto de Moscú.", ideia=True)

# ───────────────────────── 1. EL MARINERO ─────────────────────────
cap("1. El Marinero")
b("El Marinero. Berlín, junio de mil novecientos treinta y tres. Johnny de Graaf, un exmarinero alemán, entra en la embajada británica.", card="BERLÍN, 1933")
b("Según sus biógrafos, Moscú lo había formado como oficial de inteligencia militar. Ese servicio lo creó el Ejército Rojo en noviembre de mil novecientos dieciocho.")
b("De Graaf ya no cree. Los británicos lo convierten en agente doble.")
b("En mil novecientos treinta y cinco, Moscú lo envía a Brasil para ayudar a preparar un levantamiento comunista. Según sus biógrafos, lo que él sabe pasa por los británicos y llega al gobierno de Getúlio Vargas.")
b("En noviembre, el levantamiento fracasa en pocos días. Años después, otra red del mismo servicio usará otra cobertura: los negocios.", ideia=True)

# ───────────────────────── 2. EL IMPERMEABLE ─────────────────────────
cap("2. El Impermeable")
b("El Impermeable. Bruselas, marzo de mil novecientos treinta y nueve. Un comerciante que se hace llamar Adam Mikler abre la sección de exportación de una empresa de impermeables.", card="BRUSELAS, 1939")
b("Es Leopold Trepper, de la inteligencia militar soviética. La empresa es la fachada de una red de espionaje en Europa occidental.")
b("En julio llega el refuerzo: Anatoli Gurévich, de veinticinco años. Antes estuvo en la guerra civil española, como traductor en un submarino republicano. Trae un pasaporte uruguayo a nombre de Vincente Sierra. En Moscú, la purga de Stalin ya había fusilado al jefe del servicio, Yan Bérzin.")
b("En mayo de mil novecientos cuarenta, Alemania ocupa Bélgica y se queda con la empresa de impermeables. Gurévich monta otra, la Simexco. Los alemanes le dan teléfono y fax. Y la Organización Todt se convierte en su mejor cliente.", ideia=True)

# ───────────────────────── 3. LA RADIO ─────────────────────────
cap("3. La Radio")
b("La Radio. Bruselas, trece de diciembre de mil novecientos cuarenta y uno. En el número ciento uno de la rue des Atrébates, los alemanes entran en una casa.", card="BRUSELAS, 1941")
b("Llevaban tiempo siguiendo una señal de radio. Dentro hay un transmisor. Al día siguiente detienen a otro agente, Mijaíl Makárov, que usaba el nombre falso de Carlos Álamo.")
b("Vincente Sierra escapa a Francia con su pasaporte uruguayo. Mientras huye, en Moscú, el servicio que lo mandó estrena las tres letras de este expediente: GRU.")
b("En Marsella, en noviembre, la policía francesa detiene a Gurévich y lo entrega a los alemanes. Le proponen seguir transmitiendo a Moscú, con mensajes dictados desde Berlín.")
b("Gurévich acepta. Según los archivos británicos, no entrega a sus agentes. Sobrevive a la guerra, y vuelve a casa.", ideia=True)

# ───────────────────────── 4. LA CONDENA ─────────────────────────
cap("4. La Condena")
b("La Condena. Moscú, enero de mil novecientos cuarenta y siete. Un tribunal soviético juzga a Anatoli Gurévich por traición.", card="MOSCÚ, 1947")
b("Lo condenan por haber transmitido para los alemanes: veinte años de Gulag, en los campos de Vorkuta, en el Ártico.")
b("Sale en mil novecientos cincuenta y cinco. Su país no lo rehabilita hasta que la Unión Soviética ya se deshace. Muere en San Petersburgo en dos mil nueve, a los noventa y cinco años.")
b("El uruguayo de Bruselas terminó en un campo soviético. Pero el GRU no había terminado con América Latina.", ideia=True)

# ───────────────────────── 5. LA REVISTA ─────────────────────────
cap("5. La Revista")
b("La Revista. Washington, mayo de mil novecientos sesenta y uno. Georgui Bolshakov, editor de una revista soviética en inglés, conoce a Robert Kennedy, el fiscal general y hermano del presidente.", card="WASHINGTON, 1961")
b("Bolshakov es coronel del GRU. Según los historiadores, durante más de un año se reúnen muchas veces. Es un canal secreto entre Jruschov y los Kennedy.")
b("En el verano y el otoño de mil novecientos sesenta y dos, Bolshakov transmite el mensaje de Moscú: las armas que la Unión Soviética envía a Cuba son defensivas. El catorce de octubre, un avión espía estadounidense fotografía misiles en la isla.")
b("Ese mismo otoño, la KGB detiene a otro coronel del GRU, Oleg Penkovski, que espiaba para Occidente.")
b("Los Kennedy concluyeron que habían usado a Bolshakov para engañarlos. Si él lo sabía, nunca se supo. Pero en Cuba, el GRU se queda. Y se queda a escuchar.", ideia=True)

# ───────────────────────── 6. LA ANTENA ─────────────────────────
cap("6. La Antena")
b("La Antena. Lourdes, al sur de La Habana. Desde los años sesenta, un campo de antenas soviético apunta al norte, a menos de ciento cincuenta kilómetros de los cayos de Florida.", card="LOURDES, CUBA")
b("Según el diario Izvestia, en mil novecientos noventa y ocho daba más de la mitad de la inteligencia electrónica rusa sobre Estados Unidos.")
b("En mil novecientos noventa y uno, la KGB se disuelve y se reparte en varios servicios. El GRU no. Conserva su nombre, su estructura y la base de Lourdes, que comparte con otros servicios rusos. En el año dos mil viven allí entre mil y mil quinientos rusos.")
b("En dos mil uno, Putin anuncia que la cierra. Para entonces, según la justicia rusa, un coronel del GRU ya había pasado años entregando secretos a Occidente. Y todo había empezado en España.", ideia=True)
b("Si te interesan estos expedientes, suscríbete. Porque aquel coronel empezó con una propuesta de negocios.")

# ───────────────────────── 7. EL VINO ─────────────────────────
cap("7. El Vino")
b("El Vino. Madrid, mil novecientos noventa y cinco. Serguéi Skripal, oficial del GRU en la agregaduría militar rusa, recibe, según el diario británico The Times, una propuesta de negocios: exportar vino a Rusia.", card="MADRID, 1995")
b("Ese negocio, dice el diario, era la puerta de entrada del servicio secreto británico, el MI6. En sus archivos, Skripal recibe un nombre en clave: Forthwith.")
b("Según la justicia rusa, durante años entrega nombres de colegas. Lo detienen en Moscú en dos mil cuatro. Catorce años después, ya canjeado y viviendo en Inglaterra, sobrevive a un ataque con un agente nervioso en Salisbury.")
b("Mientras tanto, el GRU seguía fabricando identidades. Una de ellas bailaba con oficiales de la OTAN.", ideia=True)

# ───────────────────────── 8. EL BAILE ─────────────────────────
cap("8. El Baile")
b("El Baile. Nápoles, años dos mil diez. En las fiestas de gala de la OTAN y de los marines estadounidenses aparece una joyera que dice ser peruana: María Adela Kuhfeldt Rivera.", card="NÁPOLES, 2015")
b("Una coronel estadounidense de las fuerzas navales en Europa oye su historia: una madre peruana que la dejó de niña en la Unión Soviética. Y se pregunta: ¿por qué alguien abandonaría a un hijo allí? En dos mil dieciocho, la joyera se ofrece a pagar la cuota anual de todos los socios de su club Lions, fundado por un oficial de la OTAN.")
b("La historia tenía otro agujero. En Lima había presentado una partida de bautismo de mil novecientos setenta y ocho, de una parroquia que se fundó en mil novecientos ochenta y siete. Perú descubrió el fraude y nunca le dio la nacionalidad.")
b("Pero ella ya tenía otros papeles: un pasaporte ruso con el mismo nombre hispano. Según Bellingcat, su nombre real es Olga Kolóbova, y es oficial del GRU. En dos mil dieciocho desaparece de Nápoles. Nadie la ha juzgado, y nunca ha respondido.", ideia=True)

# ───────────────────────── 9. LA CARTA ─────────────────────────
cap("9. La Carta")
b("La Carta. Washington, dos mil veinte. Entre los graduados de una maestría de la Universidad Johns Hopkins hay un brasileño: Viktor Muller Ferreira.", card="WASHINGTON, 2020")
b("Su vida inventada cabe en una carta de cuatro páginas. Dice que creció en Niterói, junto a Río de Janeiro, que su madre murió de neumonía y que lo crió una tía. La recuerda como una mujer diminuta, de pelo gris, ojos bondadosos y manos suaves.")
b("Según el New York Times, la brasileña que figura como su madre en el certificado de nacimiento nunca tuvo hijos. Uno de sus profesores, Eugene Finkel, diría después: me siento enojado, estúpido, ingenuo, cansado. Me engañaron.", ideia=True)

# ───────────────────────── 10. LOS MENSAJES ─────────────────────────
cap("10. Los Mensajes")
b("Los Mensajes. Washington, marzo de dos mil veintitrés. La fiscalía de Estados Unidos acusa a Viktor Muller Ferreira de haber actuado como agente de Rusia sin declararlo. Y cita sus mensajes a Moscú.", card="WASHINGTON, 2023")
b("Según la denuncia, a fines de dos mil veintiuno informa sobre lo que Washington haría si Rusia invadía Ucrania. Habla con expertos de dos centros de estudios para saber qué le aconsejan al gobierno. En otro mensaje escribe: ahora estamos en la liga de los grandes.")
b("Para entonces ya lo habían descubierto. En abril de dos mil veintidós, al llegar a La Haya para una pasantía en la Corte Penal Internacional, los neerlandeses lo devuelven a Brasil. Según su servicio de inteligencia, su nombre real es Serguéi Cherkásov, oficial del GRU.")
b("En Brasil lo condenan por falsificar documentos. Él niega ser espía. En julio de dos mil veintiséis, Brasil decreta su expulsión, para cuando termine su condena. Y en el norte de Noruega, otro supuesto brasileño estudiaba las amenazas híbridas.", ideia=True)

# ───────────────────────── 11. LA PISTA ─────────────────────────
cap("11. La Pista")
b("La Pista. Tromsø, Noruega, veinticuatro de octubre de dos mil veintidós. En una carretera nevada, camino de la universidad, la policía detiene a un investigador invitado: José Assis Giammaria, que dice ser brasileño.", card="TROMSØ, 2022")
b("Había estudiado ciencia política en Ottawa y estudios estratégicos en Calgary, en Canadá. Según Bellingcat, lo delataron una contraseña repetida y la foto de una licencia de conducir rusa. Su nombre real sería Mijaíl Mikushin, coronel del GRU. Un año después, ante el tribunal, admite que es ruso.")
b("Ankara, primero de agosto de dos mil veinticuatro. Rusia y Occidente intercambian prisioneros. Noruega entrega a Mikushin. Esa noche, su avión aterriza en el aeropuerto de Vnukovo, en Moscú.")
b("En la pista hay alfombra roja y guardia de honor. La televisión transmite en directo. Putin espera al pie de la escalera y estrecha la mano de los que bajan. Les dice: quiero felicitarlos a todos por volver a la patria. Y les promete condecoraciones del Estado.")
b("El brasileño de Tromsø vuelve a ser un coronel ruso, recibido por su presidente. Para entonces, en Brasil, la policía ya sabía cómo se fabrica un brasileño.", ideia=True)

# ───────────────────────── 12. LOS FANTASMAS ─────────────────────────
cap("12. Los Fantasmas")
b("Los Fantasmas. Washington, marzo de dos mil veintidós. El general Glen VanHerck, jefe del Comando Norte, dice ante el Senado de Estados Unidos que México tiene la mayor concentración de miembros del GRU en el mundo.", card="WASHINGTON, 2022")
b("López Obrador responde que no tiene información. En Brasil, la Policía Federal buscaba otra cosa: fantasmas.")
b("Según una investigación del New York Times, son personas con un certificado de nacimiento brasileño auténtico y ningún otro rastro. Aparecen de pronto, ya adultas, y sacan la credencial de elector, los documentos del servicio militar y el pasaporte.")
b("En algunos registros civiles basta con dos testigos que digan que el bebé tiene un padre brasileño. Así, según el Times, la policía desenmascaró al menos a nueve oficiales rusos. De la mayoría, nadie ha dicho a qué servicio pertenecen.")
b("En dos mil veinticinco, una investigación británica concluye que el ataque de Salisbury tuvo que autorizarlo Putin. Rusia lo niega. Y la vieja idea del uruguayo de Bruselas se sigue usando.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. El Pasaporte")
b("El Pasaporte. Nueva York, abril de mil novecientos treinta y seis. Se emite un pasaporte uruguayo a nombre de Vincente Sierra. El hombre que lo usará es un oficial soviético.", card="NUEVA YORK, 1936")
b("Ochenta y seis años después, otro oficial del GRU aterriza en Europa con un certificado de nacimiento de Río de Janeiro. Entre los dos, una falsa peruana bautizada en una parroquia que todavía no existía.")
b("Más de una vez, un detalle los delató: una radio que transmitía demasiado, una parroquia demasiado joven, una madre que nunca tuvo hijos.")
b("El GRU nunca necesitó que América Latina lo quisiera. Le bastaba con sus papeles.", ideia=True)
b("Y tú, ¿cuántos latinoamericanos fabricados crees que nunca fueron descubiertos? Déjalo en los comentarios.")

# ───────────────────────── STORYBOARD (planos por bloco, na ordem dos blocos) ─────────────────────────
SEM = ", no lettering anywhere, every sign blank"
NOINS = ", no flags, no insignia, no badges, no emblems, no armbands, no medals"
NOFLAG = ", no flags"
FAR = ", seen from far away, no bodies, no blood"
ILEG = "the writing only as faint completely illegible blurred lines, no readable letters"
BLANK = "completely blank sheets of paper, no writing at all"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame, no ocean names"
# Personagens ("resembling", nunca foto; roupa civil sem insígnias; adultos realistas)
GUR39 = "a slim young man of about twenty-five in 1939 resembling Anatoli Gurevich, dark wavy hair, high forehead, pale linen summer suit, tie and panama hat"
GUR41 = "a slim man of about twenty-eight in 1941 resembling Anatoli Gurevich, dark wavy hair, high forehead, dark three-piece business suit and tie, bareheaded"
GUR47 = "a gaunt man of about thirty-three in 1947 resembling Anatoli Gurevich, short cropped hair, tired eyes, plain worn dark coat"
GUR55 = "a thin man of about forty-one in 1955 resembling Anatoli Gurevich, greying hair, plain worn winter coat"
GUR09 = "an elderly man of about ninety-five resembling Anatoli Gurevich, thin white hair, cardigan"
GRAAF = "a rugged German ex-sailor of about thirty in 1933 resembling Johnny de Graaf, short fair hair, plain dark civilian coat, no cap"
TREPPER = "a man of about thirty-five in 1939 resembling Leopold Trepper, strong jaw, thick dark hair swept back, civilian suit and raincoat"
MAKAROV = "a slim man of about thirty-five in 1941 resembling Mikhail Makarov, dark hair, plain overcoat"
BOLSH = "a Soviet man of about thirty-nine in 1961 resembling Georgi Bolshakov, broad face, light brown hair, dark Western suit and tie"
RFK = "a man of about thirty-six in 1961 resembling Robert F. Kennedy, boyish face, thick brown hair, dark suit"
PENK = "a Soviet man of about forty-four in 1962 resembling Oleg Penkovsky, receding hair, dark overcoat"
KHRU = "a Soviet leader of the early 1960s resembling Nikita Khrushchev, bald, stocky, smiling, dark suit"
PUTIN01 = "a Russian president of 2001 resembling Vladimir Putin, forty-nine, short light hair, dark suit and tie"
PUTIN24 = "a man resembling Vladimir Putin in 2024, seventy-one, thin pale hair, dark suit and tie, serious face"
SKRIP = "a stocky Russian man of about forty-four in 1995 resembling Sergei Skripal, short hair, civilian suit"
KOLO = "an elegant woman of about forty in the 2010s resembling Olga Kolobova, long dark hair, dark eyes, evening dress and a silver necklace (an illustration, not a photograph)"
CHERK20 = "a man of about thirty-five in 2020 resembling Sergei Cherkasov, short dark hair, light stubble, friendly face, dark jacket"
CHERK22 = "a man of about thirty-seven in 2022 resembling Sergei Cherkasov, short dark hair, light stubble, tense face, dark jacket"
MIKU = "a man of about forty-four in 2022 resembling Mikhail Mikushin, short brown hair, athletic build, dark winter parka"
VANHERCK = "a man of about sixty resembling General Glen VanHerck, short grey hair, strong jaw, dark business suit and tie, no insignia, no medals"
AMLO = "a man of about sixty-nine resembling Andres Manuel Lopez Obrador, white hair, dark suit, calm face"

SB = [
 # N001 Bruselas 1941: Vincente Sierra, empresa de importación y exportación
 ["brussels_1941|A busy Brussels commercial street in 1941, tall Belgian townhouses, a tram, men in overcoats" + SEM + NOFLAG + "@@BRUSELAS, 1941",
  f"vincente_desk|{GUR41} sitting behind a desk in an import-export office in Brussels in 1941, shipping crates and a wall map behind him" + SEM + "@@VINCENTE SIERRA",
  "crates_warehouse|Wooden shipping crates stacked in a Brussels warehouse in 1941, ropes, a hand cart, crates without any stencil" + SEM],
 # N002 su mejor cliente: la Organización Todt
 ["todt_site|A huge concrete bunker construction site on the Atlantic coast in 1941, cranes and scaffolding, workers in overalls, seen from a distance" + NOINS + SEM,
  f"todt_contract|{GUR41} signing a contract at a desk in Brussels in 1941 opposite two German civilians in long leather coats" + NOINS + SEM,
  "cement_trucks|A long line of trucks loaded with cement bags on a Belgian road in 1941, overcast sky" + NOINS + SEM,
  "papers_desk|A businessman's desk in 1941 with " + BLANK + ", a fountain pen and a brass lamp"],
 # N003 no es uruguayo: pasaporte de Nueva York; oficial soviético
 ["passport_open|A worn passport open on a desk under a lamp, the photo page showing only a faint blurred portrait sketch and the rest " + ILEG + ", a rubber stamp beside it",
  "nyc_1936|A New York City street in 1936 with skyscrapers, an elevated railway, black taxis and passers-by in hats and overcoats" + SEM + "@@NUEVA YORK, 1936",
  f"sierra_shadow|{GUR41} standing at a dark window at night, half of his face in shadow, a plain olive tunic without insignia hanging on a coat hook behind him"],
 # N004 frase-ancla: TODA la historia del GRU; uruguayo, peruana, brasileños; Putin en la pista
 ["dossier_desk|A brown cardboard dossier on a dark desk under a green lamp, a red rubber stamp beside it" + SEM,
  # world_map: o código desenha pinos em Moscú, Bruselas, Montevideo, Nápoles, Río de Janeiro e La Haya (planisfério centrado no Atlântico)
  "world_map|" + MAPA + ", showing the whole world in a simple Atlantic-centered projection, Europe and Russia on the right and the Americas on the left",
  "gru_hq|A modern glass-and-concrete military intelligence headquarters complex in Moscow seen from a street at dusk, a high fence" + SEM + NOFLAG,
  "four_passports|Top-down view of four plain passports fanned out on a dark wooden table, covers dark blue, burgundy, green and black, no emblem and no lettering, desk lamp light",
  f"woman_gala|{KOLO} laughing at a glittering ballroom party, chandeliers behind her, guests in evening wear",
  f"student_gown|{CHERK20} in an academic cap and gown holding a diploma tube, smiling stiffly on a university lawn",
  f"putin_tarmac|Night on an airport tarmac under cold floodlights, a red carpet, {PUTIN24} stepping forward to shake the hand of a man in a plain jacket, the last steps of a boarding stair on the left, no airplane visible" + NOINS],
 # N005 Berlín 1933: De Graaf entra en la embajada británica
 ["berlin_1933|Wilhelmstrasse in Berlin in June 1933, grand government buildings, a black car, people in hats and light summer coats" + SEM + NOINS,
  f"degraaf_door|{GRAAF} climbing the steps of a grand diplomatic building in Berlin in 1933, glancing over his shoulder" + NOINS + "@@JOHNNY DE GRAAF",
  "embassy_gate|A wrought-iron gate and stone entrance of an embassy in Berlin in 1933, a doorbell panel, a brass plaque completely blank" + SEM + NOINS],
 # N006 Moscú lo formó; el servicio nace en noviembre de 1918
 ["soviet_school|A Soviet military training classroom of the late 1920s, young men seen from behind in plain olive tunics without insignia, a blackboard with a blank map" + SEM + NOINS,
  "petrograd_1918|A column of workers and soldiers in greatcoats walking along a snowy Petrograd street in November 1918, plain caps without any badge, blank banners" + FAR + SEM + NOINS + "@@NOVIEMBRE DE 1918",
  "order_1918|A typed order of 1918 on rough paper pinned to a wall, " + ILEG + ", a red pencil beside it",
  "kremlin_1918|The Moscow Kremlin walls in November 1918 under a grey sky, snow on the ground" + NOFLAG + SEM],
 # N007 De Graaf ya no cree; los británicos lo vuelven agente doble
 [f"degraaf_meeting|{GRAAF} sitting across a table from a British intelligence officer in a plain dark civilian suit in a dim London office in 1933, tea cups",
  "two_envelopes|Close-up of a man's two hands each holding an identical plain blank envelope, lamp light, dark coat sleeves, no lettering"],
 # N008 1935: Brasil, levantamiento comunista; Vargas
 ["rio_1935|Rio de Janeiro in 1935, the harbour with Sugarloaf Mountain, trams and 1930s cars" + SEM + "@@RÍO DE JANEIRO, 1935",
  f"degraaf_ship|{GRAAF} on the deck of an ocean liner arriving in Rio de Janeiro in 1935, Sugarloaf behind him",
  "barracks_1935|A Brazilian army barracks courtyard in Rio in 1935, soldiers in plain khaki gathering" + FAR + NOINS,
  "vargas|A Brazilian president of the 1930s resembling Getulio Vargas, short, round face, grey hair, dark suit, at a desk in a palace office" + SEM + NOINS + "@@GETÚLIO VARGAS",
  "secret_letter|Two men at a dim Rio cafe table, one passing a blank sheet of paper folded in his hand to the other, 1935" + SEM],
 # N009 noviembre: el levantamiento fracasa; otra red usará los negocios
 ["rio_smoke|Smoke rising over a Rio de Janeiro barracks district in November 1935, grey sky" + FAR + NOINS,
  "arrests_1935|Brazilian police escorting men with hands behind their backs along a Rio street at dawn in 1935, seen from behind" + NOINS + SEM,
  "blank_nameplate|A brass nameplate beside a door of a commercial office in Brussels in 1938, completely blank" + SEM],
 # N010 Bruselas 1939: Adam Mikler, empresa de impermeables
 ["brussels_1939|A rainy Brussels boulevard in March 1939 with Art Nouveau buildings, trams and umbrellas" + SEM + NOFLAG,
  f"trepper_office|{TREPPER} behind a desk in a raincoat company office in Brussels in 1939, shelves of folded raincoats, rain on the window" + SEM + "@@ADAM MIKLER",
  "raincoat_rack|Rows of beige raincoats hanging on racks in a Brussels warehouse in 1939" + SEM,
  "ledger_hand|A hand writing in a thick ledger with " + ILEG + ", ink pen, lamp light, 1939"],
 # N011 es Trepper; la empresa es fachada de una red
 [f"trepper_window|{TREPPER} standing at a window looking down at a rainy Brussels street, hands behind his back, 1939" + "@@LEOPOLD TREPPER",
  "radio_attic|A hidden shortwave radio transmitter on a table under a sloped attic roof, headset, a single lamp" + SEM,
  # europe_map: o código desenha o pino de Bruselas e linhas finas até Paris, Amsterdã e Berlim (rede de Europa ocidental)
  "europe_map|" + MAPA + ", showing western Europe: Belgium in the center with France, the Netherlands and Germany around it"],
 # N012 julio 1939: Gurévich, traductor en un submarino, pasaporte uruguayo; purga y Bérzin
 [f"gur_arrives|{GUR39} stepping off a steam train with a leather suitcase on a Brussels station platform in July 1939" + "@@ANATOLI GURÉVICH",
  "spain_sub|The control room of a 1930s submarine, a young translator in a plain civilian sweater beside a bearded captain, pipes and dials" + SEM + NOINS,
  "passport_closed|A closed dark-blue passport with a plain cover, no emblem and no lettering, on a Brussels hotel desk beside a pale panama hat",
  "moscow_night_1938|A grey Moscow building at night in 1938, a black car parked outside, one lit window, snow" + FAR + SEM + NOFLAG,
  "berzin|A Soviet intelligence chief of the 1930s resembling Yan Berzin, round glasses, receding hair, plain dark civilian jacket, at a desk" + SEM + NOINS + "@@YAN BÉRZIN",
  "empty_chair|An empty chair at a desk in a Moscow office, a file folder pushed aside, a lamp still on, 1938" + SEM],
 # N013 mayo 1940: Alemania ocupa Bélgica; Simexco; Todt su mejor cliente
 ["refugees_1940|Belgian refugees on a country road in May 1940 with carts, bicycles and mattresses, a distant column of tanks on the horizon" + FAR + NOINS,
  "brussels_occupied|An almost empty Brussels boulevard in May 1940, shutters closed, a few people walking fast, grey light" + SEM + NOINS,
  f"gur_signboard|{GUR41} hanging a blank company signboard above a Brussels office door, 1940" + SEM,
  "simexco_office|A modern office in Brussels in 1940, a telephone and a teleprinter on a desk, a Belgian secretary typing" + SEM,
  "todt_visit|Two German civilian officials in long leather coats shaking hands with a businessman in an office in Brussels, 1940" + NOINS + SEM],
 # N014 Bruselas 13/12/1941: rue des Atrébates 101
 ["rue_atrebates|A quiet residential street in Brussels in December 1941 at dusk, brick terraced houses, bare trees, a black car outside one house, every sign blank" + SEM + NOINS + "@@RUE DES ATRÉBATES 101",
  "house_door|A brick townhouse front door in Brussels at dusk in December 1941, the shadows of several men in overcoats approaching on the steps" + FAR + SEM,
  "radio_set|A clandestine radio transmitter hidden in an open suitcase on a table, a Morse key, wires, 1941" + SEM,
  "radio_van|A black unmarked van with a rotating loop antenna on its roof parked on a Brussels street at night, 1941" + SEM],
 # N015 siguiendo la señal; Makárov (Carlos Álamo)
 ["listening_room|A radio direction-finding room in 1941, men in civilian suits with headphones, a wall of dials and a map" + SEM + NOINS,
  "attic_found|An attic room in Brussels with a radio transmitter on the floor, boxes, a lamp knocked over, signs of a hurried exit" + SEM,
  f"makarov|{MAKAROV} on a Brussels street at night looking over his shoulder, 1941" + "@@MIJAÍL MAKÁROV",
  "false_id|A forged identity card of 1941 on a table, only a faint sketch instead of a photo and the rest " + ILEG + ", an ink pad beside it"],
 # N016 Sierra escapa a Francia; Moscú estrena GRU
 [f"sierra_train|{GUR41} on a night train to France, collar up, face half-lit through the window, 1941",
  "french_border|A rural Franco-Belgian border road on a winter night in 1941 with a barrier and a single lantern, empty" + SEM + NOINS,
  "moscow_1942|Moscow in the winter of 1942 seen from a window, snowy rooftops and Kremlin towers, barrage balloons far away" + NOFLAG + SEM,
  "frosted_door|A heavy wooden door of a Moscow office building with an empty frosted glass panel and a plain dark metal plate, completely blank" + SEM],
 # N017 Marsella nov. 1942: detenido y entregado a los alemanes
 ["marseille_1942|The Old Port of Marseille in November 1942, fishing boats, the basilica on the hill, a grey day" + SEM + NOINS + "@@MARSELLA, 1942",
  f"gur_arrest|{GUR41} stopped on a Marseille street by two French policemen in dark capes and kepis, 1942" + FAR + NOINS,
  f"gur_interrogation|{GUR41} sitting across from two German civilians in leather coats in a bare interrogation room, a radio set on the table, 1942" + NOINS + SEM],
 # N018 acepta transmitir; no entrega a sus agentes; sobrevive
 [f"gur_transmit|{GUR41} tapping a Morse key in a dim room while a German civilian stands behind him holding a blank sheet of paper, 1943" + NOINS + SEM,
  "ruined_train|A steam train crossing a ruined European landscape in the summer of 1945, grey sky" + FAR + NOINS],
 # N019 Moscú 1947: tribunal por traición
 ["moscow_court|A Soviet courtroom in January 1947, three judges in dark civilian suits behind a long table under a bare lamp, a defendant seen from behind, a plain wall" + SEM + NOINS,
  f"gur47_dock|{GUR47} standing in the dock with his head bowed, 1947" + SEM,
  "moscow_winter_47|A snowy Moscow street in January 1947 with a black car and a few passers-by in heavy coats" + SEM + NOFLAG],
 # N020 veinte años de Gulag, Vorkuta, Ártico
 ["vorkuta_tundra|The Arctic tundra near Vorkuta in winter, endless snow under a grey sky, a few low wooden barracks and a watchtower far at the horizon" + FAR + NOFLAG + "@@VORKUTÁ",
  "vorkuta_train|A narrow-gauge railway through snowy tundra with a lone small locomotive and a line of smoke, 1950" + FAR + SEM,
  "sentence_paper|A sentence document on a desk with a red stamp, " + ILEG],
 # N021 sale en 1955; rehabilitado tarde; muere en 2009
 [f"gur55|{GUR55} walking out through a gate into a landscape of melting spring snow, carrying a small bundle" + SEM,
  "st_petersburg_2009|Saint Petersburg in autumn 2009, a canal with pastel buildings, golden light" + SEM + NOFLAG + "@@SAN PETERSBURGO, 2009",
  f"gur09|{GUR09} sitting in an armchair by a window in a Saint Petersburg apartment, hands on a cane, soft light"],
 # N022 el uruguayo terminó en un campo soviético; el GRU no había terminado con América Latina
 ["panama_hat|A pale panama hat resting alone on a bare wooden table in a snow-lit room, a lamp",
  "passport_closed#detalhe-centro",
  "vorkuta_tundra#detalhe-baixo"],
 # N023 Washington mayo 1961: Bolshakov conoce a Robert Kennedy
 ["washington_1961|Washington DC in spring 1961, Pennsylvania Avenue with the Capitol dome far away, black sedans, people in hats" + SEM + NOFLAG,
  f"bolshakov_magazine|{BOLSH} in a small Washington office editing magazine page layouts at a desk, pages completely blank, 1961" + SEM + "@@GEORGUI BOLSHAKOV",
  f"rfk_office|{RFK} at his desk at the Justice Department in 1961, jacket off and sleeves rolled up, framed photographs on the wall showing only faint blurred shapes" + SEM + "@@ROBERT KENNEDY"],
 # N024 coronel del GRU; canal secreto Jruschov-Kennedy
 [f"bolshakov_walk|{BOLSH} and {RFK} walking together through a leafy Washington park in 1961, quiet conversation",
  "backchannel_phone|A black rotary telephone and a plain notebook on a desk at night, a cigarette burning in an ashtray, 1961",
  f"khrushchev|{KHRU} at a desk in a Kremlin office in 1961" + SEM + NOFLAG + "@@NIKITA JRUSCHOV"],
 # N025 1962: armas defensivas; 14 de octubre avión espía fotografía misiles
 ["cuba_ships|Soviet cargo ships on the Atlantic in 1962 with large covered crates on deck, tarpaulins" + FAR + NOFLAG,
  "cuban_dock|Large tarpaulin-covered crates stacked on a Cuban dock at dawn, palm trees, 1962" + SEM + NOINS,
  "u2_flight|A high-altitude spy plane, long thin wings and dark plain fuselage without any markings, flying above clouds over a green island in October 1962" + NOINS + "@@14 DE OCTUBRE DE 1962",
  "recon_photos|A table with blown-up aerial reconnaissance photographs of an island, a magnifying glass and a pointer, only faint indistinct shapes, no captions" + SEM],
 # N026 la KGB detiene a Penkovski
 [f"penkovsky|{PENK} walking on a Moscow street at night, a dark car following behind him, autumn 1962" + SEM + "@@OLEG PENKOVSKI",
  "lubyanka_1962|A grey neo-baroque office building in Moscow at night, a few lit windows, 1962" + SEM + NOFLAG],
 # N027 los Kennedy se sienten engañados; el GRU se queda en Cuba
 [f"rfk_night|{RFK} alone at his desk at night, head in his hand, a lamp, a telephone, 1962",
  f"bolshakov_leaving|{BOLSH} walking away down a long corridor in a Washington building, seen from behind, 1962",
  "havana_1962|Havana's seafront wall in 1962, old American cars, sea spray, palm trees" + SEM],
 # N028 Lourdes: campo de antenas, a menos de 150 km de Florida
 ["lourdes_antennas|A vast field of giant dish antennas and tall radio masts on flat green Cuban land south of Havana, a security fence, palm trees, seen from far away" + FAR + NOINS + "@@LOURDES, CUBA",
  # caribbean_map: o código desenha o pino de Lourdes, os Cayos de Florida e uma linha tracejada de ~150 km
  "caribbean_map|" + MAPA + ", showing Cuba and the Florida Keys with the Gulf of Mexico and the Bahamas",
  "dish_close|Close-up of a large parabolic dish antenna against a tropical sky, rust streaks"],
 # N029 Izvestia 1998: más de la mitad de la inteligencia electrónica
 ["listening_hall|A hall of technicians at consoles with headphones in 1990s Russia, banks of old equipment, green screens" + SEM + NOINS,
  "newspapers_1998|A stack of Russian newspapers on a desk with only blurred photographs and " + ILEG + ", 1998"],
 # N030 1991: la KGB se disuelve; el GRU conserva todo; 1.000-1.500 rusos en 2000
 ["lubyanka_1991|The Lubyanka headquarters in Moscow at dusk in August 1991, a crowd gathering outside seen from far away, blank banners" + FAR + SEM + NOFLAG,
  "folder_cut|A hand cutting a large brown folder into several smaller folders with scissors on a desk, lamp light, 1991",
  "gru_door|A closed grey door with a completely blank brass plate in a Moscow military building corridor, 1991" + SEM,
  "lourdes_families|Russian families walking in a Cuban compound of white apartment blocks, children, laundry on lines, palm trees, 2000" + SEM,
  "lourdes_antennas#médio-dir"],
 # N031 2001: Putin anuncia el cierre; un coronel del GRU; España
 [f"putin01|{PUTIN01} at a press microphone in the Kremlin in 2001" + SEM + NOFLAG + "@@VLADIMIR PUTIN",
  "antennas_dusk|The antenna field at dusk with one dish in silhouette, lights off, an empty road, Cuba" + FAR + NOINS,
  "madrid_skyline|The Madrid skyline in the 1990s at golden hour, Gran Via buildings and rooftops" + SEM],
 # N032 CTA: suscríbete; propuesta de negocios
 ["proposal_folder|A business proposal folder lying open on a desk beside a glass of red wine and a pen, the pages completely blank, Madrid 1995" + SEM,
  "wine_bottles|A rack of wine bottles with completely blank labels in a cellar, lamp light" + SEM],
 # N033 Madrid 1995: Skripal; propuesta de exportar vino
 ["madrid_1995|Paseo de la Castellana in Madrid in 1995 with embassy buildings, trees and mid-1990s cars" + SEM + NOFLAG,
  f"skripal95|{SKRIP} walking along a Madrid avenue in 1995 in a civilian suit, a briefcase in hand" + "@@SERGUÉI SKRIPAL",
  "wine_proposal|A Spanish businessman in a restaurant offering a glass of red wine to a Russian man in a civilian suit, Madrid 1995, small plates of tapas, a blank menu" + SEM],
 # N034 puerta de entrada del MI6; Forthwith
 ["safehouse_madrid|A quiet Madrid apartment interior in 1995, two men in suits talking in low voices by a window with drawn curtains, a bottle of wine on the table" + SEM,
  "file_forthwith|A thin secret service file on a desk, its cover a plain blank label and a single faint illegible code word, lamp light",
  "london_riverside|A green and cream riverside government building on the Thames in London at dusk, 1990s, lit windows" + SEM + NOFLAG],
 # N035 justicia rusa; 2004 detenido; canje; Salisbury (sugerido)
 [f"skripal04|{SKRIP} aged fifty-three arrested outside an apartment block in Moscow in 2004, plain-clothes men around him, evening, grey sky" + FAR + NOINS + SEM,
  "swap_apron|A foggy airport apron at dawn in July 2010 with two jets parked far apart and an empty stretch of tarmac between them" + SEM + NOINS,
  "salisbury_bench|An empty park bench in a quiet shopping area of Salisbury in March 2018, police tape fluttering across the path, the cathedral spire in the background, early evening, nobody there" + SEM + "@@SALISBURY, 2018",
  "perfume_bottle|A small sealed perfume bottle without a label inside a transparent evidence bag on a metal table in a laboratory, seen from across the room" + FAR + SEM],
 # N036 el GRU seguía fabricando identidades; una bailaba con oficiales de la OTAN
 ["gala_hall|A grand ballroom with chandeliers, a live orchestra and couples dancing under warm light, wide view from the balcony" + SEM,
  "woman_gala#médio-dir"],
 # N037 Nápoles 2010s: fiestas de gala de la OTAN y marines; joyera peruana
 ["naples_2010s|The Bay of Naples with Vesuvius in the distance at sunset, a palm-lined waterfront and a palace" + SEM + NOFLAG,
  f"kolo_gala|{KOLO} chatting with guests at a lavish gala in a Naples palace ballroom, people in evening wear and dark suits, champagne glasses, chandeliers" + "@@MARÍA ADELA KUHFELDT RIVERA",
  "jewelry_case|A velvet display case of silver and gemstone necklaces under a glass counter in a boutique in Naples" + SEM,
  "woman_gala#detalhe-alto"],
 # N038 coronel estadounidense; madre peruana; Lions Club
 ["navy_colonel|An American woman of about fifty-five in a dark formal dress with a pearl necklace at a gala dinner table, listening with a puzzled look" + NOINS,
  f"kolo_story|{KOLO} telling a sad story at a dinner table, hand over her heart, guests listening around her",
  "child_ussr|A little girl standing alone in the courtyard of a Soviet apartment block in the early 1980s, grey buildings, snow, holding a doll",
  "peru_mother|A Peruvian woman seen from behind walking away down a Lima street in 1980 carrying a suitcase, a small girl's hand-drawn doll left on a step" + SEM,
  "lions_dinner|A charity dinner in an Italian hotel hall in 2018, tables with white cloths, a banner without writing, a small golden lion statuette on the podium" + SEM + NOFLAG,
  "kolo_gala#detalhe-centro"],
 # N039 partida de bautismo de 1978; parroquia de 1987; Perú descubre el fraude
 ["lima_church|A small colonial parish church in a Lima district, whitewashed facade with a wooden door and a bell, sunny, no plaque, no signs" + SEM + "@@LIMA, PERÚ",
  "baptism_record|An old baptism register open on a priest's desk, columns of entries as " + ILEG + ", a candle",
  "peru_office|A migration office counter in Lima in 2018, an official shaking his head over a form handed over by a woman seen from behind, bare wall" + SEM],
 # N040 pasaporte ruso; Bellingcat: Olga Kolóbova; 2018 desaparece
 ["two_passports|Two plain passports side by side on a table, one dark red and one dark blue, covers with no emblem and no lettering, lamp light",
  "jewelry_closed|The metal shutter of a jewelry boutique pulled down at night in Naples, a single streetlight" + SEM,
  "gala_empty_chair|An empty chair at a gala table with a folded napkin, ballroom lights dimmed, glasses left behind" + SEM],
 # N041 Washington 2020: Johns Hopkins; Viktor Muller Ferreira
 ["jhu_building|A modern graduate school building in Washington DC in spring 2020, an almost empty plaza with tulips" + SEM,
  "graduation_class|Rows of graduates in caps and gowns on a lawn seen from behind on a sunny day, 2020" + SEM,
  "student_gown#médio-esq@@VIKTOR MULLER FERREIRA"],
 # N042 la carta de cuatro páginas; Niterói; tía
 ["letter_four|Four typed sheets of a letter fanned on a desk under a lamp, the text as " + ILEG,
  "niteroi_bay|Niteroi seen across Guanabara Bay with Sugarloaf and the Rio skyline in the distance, a ferry crossing, late afternoon" + SEM + "@@NITERÓI, BRASIL",
  "aunt_portrait|A tiny elderly Brazilian woman with grey hair, kind eyes and gentle hands, in a modest living room with a sewing machine, soft light",
  "child_aunt|A small boy in a modest Niteroi living room holding his aunt's hand, warm afternoon light" + SEM],
 # N043 NYT: la madre del certificado nunca tuvo hijos; Eugene Finkel
 ["birth_certificate|A Brazilian birth certificate on a registry desk, ornate border, the fields as " + ILEG + ", a rubber stamp",
  "woman_doorway|An elderly Brazilian woman in the doorway of a modest apartment in Rio, shaking her head, bare walls without photographs" + SEM,
  "finkel|A university professor of about fifty with glasses and short dark hair in a lecture hall in Washington, rubbing his forehead, tired and angry, empty seats" + SEM + "@@EUGENE FINKEL"],
 # N044 Washington marzo 2023: acusación; mensajes a Moscú
 ["doj_building|The US Department of Justice headquarters in Washington on a grey March day in 2023, limestone facade and columns" + SEM + NOFLAG,
  "indictment|A thick federal indictment document on a table with a metal paper clip, the pages as " + ILEG,
  "chat_screen|A laptop in a dark room showing a messaging conversation as " + ILEG + ", a hand on the keyboard, only the screen glow"],
 # N045 fines de 2021: informa; dos centros de estudios; liga de los grandes
 [f"viktor_laptop|{CHERK20} typing at a laptop in a Washington apartment at night, city lights behind him, late 2021",
  "think_tank|A Washington think tank conference room in late 2021, experts seated around a table, glass walls, a blank screen" + SEM,
  # ukraine_map: o código desenha um pino em Kiev e uma seta curta vinda de Moscú
  "ukraine_map|" + MAPA + ", showing eastern Europe with Ukraine and western Russia",
  "chess_board|A chess board seen from above with all pieces in place, a hand moving a rook, lamp light"],
 # N046 abril 2022: La Haya; CPI; devuelto a Brasil; Cherkásov
 ["hague_icc|The International Criminal Court building in The Hague, glass and steel with a tall tower, April 2022, spring light" + SEM + NOFLAG + "@@LA HAYA, 2022",
  f"cherk_schiphol|{CHERK22} at a passport control booth at Schiphol airport, a Dutch officer in a plain dark jacket behind the glass examining his passport" + NOINS + SEM,
  "flight_back|An airliner flying low over the Atlantic at sunrise, plain white fuselage without any logo" + SEM,
  f"cherk_escorted|{CHERK22} escorted by two plainclothes Dutch officers through an airport corridor with a suitcase" + NOINS + SEM],
 # N047 condenado en Brasil por falsificar documentos; expulsión; Noruega
 ["brazil_court|A Brazilian federal courtroom in Brasilia, a judge at the bench, a defendant seen from behind, wood and beige walls" + SEM + NOINS,
  f"cherk_visit|{CHERK22} in a plain grey shirt sitting in a prison visiting room behind a glass partition, hands on the counter" + SEM + NOINS,
  "norway_fjord|A fjord in northern Norway in autumn with first snow on the peaks and a small town on the shore" + SEM + NOFLAG],
 # N048 Tromsø 24/10/2022: carretera nevada; investigador invitado
 ["tromso_road|A snowy road at dawn in Tromso, Norway, in October 2022, snow banks, a bridge and mountains with first snow, a dark car with a plain police car behind it with blue lights" + SEM + NOINS + "@@TROMSØ, NORUEGA",
  f"mikushin_car|{MIKU} driving a car on a snowy road at dawn, glancing in the mirror, blue lights reflected on his face" + "@@JOSÉ ASSIS GIAMMARIA",
  "police_stop|Norwegian police officers in plain dark jackets stepping out of a car on a snowy road at dawn" + NOINS + SEM],
 # N049 Ottawa y Calgary; Bellingcat: contraseña y licencia; Mikushin; admite
 ["ottawa_parliament|Parliament Hill in Ottawa in autumn, Gothic stone towers and copper roofs, golden leaves" + SEM + NOFLAG,
  "calgary_winter|The Calgary skyline in winter with the tall tower in the distance, snow on the ground, crisp light" + SEM + NOFLAG,
  "password_note|A yellow sticky note on a monitor with the same short scribble written three times as " + ILEG + ", a login box showing only dots",
  "driving_license|A plastic driver's license card on a table, a small photo of a man and only faint illegible lines, no logo, no emblem",
  "tromso_court|A Norwegian courtroom in autumn 2023, wood panels, a man in a dark suit standing and speaking, judges seen from the side" + SEM + NOINS + "@@MIJAÍL MIKUSHIN"],
 # N050 Ankara 1/8/2024: canje; Noruega entrega; avión a Vnúkovo
 ["ankara_night|An airport in Ankara at night in August 2024, two plain jets parked on the apron under floodlights, buses and cars, no markings" + SEM + NOFLAG,
  "swap_buses|Dark buses with curtained windows driving across an airport apron at night" + FAR + SEM,
  f"mikushin_handover|{MIKU} in a plain waiting room at night with a small bag, standing between two men in civilian coats" + SEM,
  "plane_vnukovo|A plain white jet flying over the lights of Moscow at night approaching to land, no logo" + SEM],
 # N051 pista de Vnúkovo: alfombra roja, guardia, TV, Putin al pie de la escalera
 ["vnukovo_carpet|A red carpet laid on an airport tarmac at night under floodlights, a boarding stair at the far end, a distant honor guard of soldiers in plain long grey greatcoats and fur hats without any badge, TV cameras on tripods" + FAR + SEM + NOINS + "@@VNÚKOVO, MOSCÚ",
  f"putin_stair|{PUTIN24} standing at the foot of a boarding stair on a night tarmac, facing the steps, hands at his sides, floodlights" + SEM,
  "tv_crew|TV crews with cameras and a reporter's light at the edge of an airport tarmac at night, breath fogging in the cold" + SEM,
  "returnees_stairs|A small group of men and women in plain winter jackets descending the boarding stairs of a plane at night, seen from far away, floodlights, a red carpet below" + FAR + SEM,
  f"putin_handshake|{PUTIN24} shaking hands with a man in a plain jacket seen from behind at the foot of boarding steps, night, camera flashes" + SEM,
  "putin_tarmac#detalhe-centro"],
 # N052 el brasileño vuelve a ser coronel ruso; en Brasil la policía ya sabía
 ["brazil_police_hq|The Brazilian Federal Police headquarters building in Brasilia at dusk, glass and concrete" + SEM + NOFLAG,
  "evidence_table|A table of seized documents and passports in a Brazilian police office, plain covers, " + BLANK,
  "mikushin_car#médio-dir",
  "putin_handshake#detalhe-alto"],
 # N053 Washington marzo 2022: VanHerck; Senado; México
 ["senate_room22|A US Senate hearing room in March 2022, a long dais, a witness table with microphones, visitors seated behind" + SEM + NOINS + "@@SENADO DE EE. UU.",
  f"vanherck|{VANHERCK} testifying at a witness table in front of microphones, a stack of papers, stern look" + SEM + "@@GLEN VANHERCK",
  # mexico_map: o código desenha o pino da Cidade do México
  "mexico_map|" + MAPA + ", showing Mexico and the southern United States"],
 # N054 López Obrador responde; la Policía Federal busca fantasmas
 [f"amlo|{AMLO} at a morning press conference in the National Palace in Mexico City, speaking calmly and gesturing with one hand" + SEM + "@@LÓPEZ OBRADOR",
  "pf_cards|A dim police office wall with blank index cards joined by strings, silhouettes without faces on the cards" + SEM],
 # N055 NYT: certificado auténtico, aparecen ya adultas, credencial, servicio militar
 ["faceless_man|A faceless man in a dark coat standing in a queue in a Brazilian registry office in the early morning, his face turned away" + SEM,
  "id_stack|A neat stack of identity documents on a wooden desk, a plain voter card, a military service booklet and a passport, all with plain covers and blank pages",
  "late_registration|A Brazilian civil registry (cartorio) counter, an adult man filling in a form while the clerk watches, shelves of large registry books" + SEM],
 # N056 dos testigos; nueve oficiales rusos; nadie dice el servicio
 ["two_witnesses|An old man and an old woman standing before a registry clerk who writes in a large register, a small-town Brazilian registry office, wooden counter, ceiling fan" + SEM,
  "nine_cards|Nine blank identity cards laid in a three-by-three grid on a dark table, the photo windows empty, no lettering",
  "archive_cabinets|A wall of file cabinets in a government archive, blank folder tabs, a single open drawer, dim light" + SEM],
 # N057 2025: investigación británica; Putin autorizó; Rusia lo niega
 ["uk_inquiry|A British public inquiry hearing room in 2025, a panel at a long table, wood panels, a blank screen" + SEM + NOINS + "@@REINO UNIDO, 2025",
  "kremlin_2025|The Kremlin and the Moskva river at dusk in autumn 2025" + NOFLAG + SEM,
  "salisbury_bench#detalhe-baixo",
  "putin_stair#médio-esq"],
 # N058 Nueva York abril 1936: pasaporte uruguayo a nombre de Sierra
 ["nyc_passport_office|A passport office of the 1930s in Manhattan, a clerk behind a wooden counter stamping a booklet, a ceiling fan, a man in a white linen suit waiting" + SEM,
  "stamp_press|A hand pressing a rubber stamp onto a passport page, close-up, ink pad, 1936, the page blank except faint lines, " + ILEG,
  "nyc_1936#detalhe-alto",
  "passport_closed#médio-esq"],
 # N059 86 años después: certificado de Río; entre los dos, la falsa peruana
 ["amsterdam_arrival|An airliner landing at a Dutch airport in April 2022 in morning light, plain white fuselage without any logo, flat green fields" + SEM,
  "birth_certificate#detalhe-centro",
  "kolo_gala#detalhe-alto",
  "lima_church#médio-esq",
  "cherk_schiphol#médio-esq"],
 # N060 un detalle los delató: radio, parroquia, madre
 ["radio_set#detalhe-centro",
  "lima_church#detalhe-alto",
  "woman_doorway#médio-esq"],
 # N061 el GRU nunca necesitó que América Latina lo quisiera; le bastaba con sus papeles
 ["papers_pile|A heap of identity papers of different colors and sizes piled on a dark table, all blank, lamp light" + SEM,
  "four_passports#detalhe-centro"],
 # N062 pregunta final
 ["lone_passport|Top-down view of a single dark passport lying open on empty dark wood, the photo window empty, a single spotlight, no lettering",
  "dossier_desk#médio-dir"],
]

THUMBS = [
    {"id": "thumb-A", "prompt": "Ink graphic novel illustration: a large Russian matryoshka nesting doll opened in half on a dark slate table, centered in the left half of the frame, front view, the outer shell painted as a 1930s businessman in a white linen suit with a tie and a panama hat, its top half lifted and tilted open, a smaller doll rising from the lower half painted as a Soviet officer in a plain olive tunic with a small red star on the cap, the inner officer doll at least one third of the frame height and clearly readable, warm table lamp light from the left, plain dark slate-blue background, the entire right half of the frame completely empty plain dark slate, no lettering, no flags, no emblems, no logos, no text, no letters, no hex codes"},
    {"id": "thumb-B", "prompt": "Ink graphic novel illustration: night on an airport tarmac under cold floodlights, close medium shot, a man resembling Vladimir Putin in a dark suit and tie in three-quarter profile, his face large and filling at least one third of the frame height, shaking hands with a man in a plain jacket seen from behind in shadow, the handshake in the exact center of the frame, only the bottom steps of a boarding stair visible at the left edge, no airplane visible, no soldiers, no honor guard, floodlight halo in the night sky behind his head on the right, the lower right third of the frame empty dark tarmac, no lettering, no flags, no emblems, no logos, no text, no letters, no hex codes"},
    {"id": "thumb-C", "prompt": "Ink graphic novel illustration: top-down view of three plain passports fanned out like a hand of cards on a dark wooden desk, covers dark navy blue, burgundy and dark green with no emblem, no crest and no lettering at all, the top passport open at the photo page with a completely empty blank photo window and the data fields as nothing but empty space, a desk lamp light coming from one corner with soft shadows, absolutely no words, no numbers, no letters, no text, no flags, no logos, no hex codes"},
]

_textos = [x for x in B if "t" in x]
if SB:
    assert len(SB) == len(_textos), f"SB {len(SB)} x blocos {len(_textos)}"
    for _blk, _s in zip(_textos, SB): _blk["s"] = _s

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
        f"# {TITULO}: roteiro\n\nPromessa: {PROMESSA}\n\nTítulos: {TITULOS}\n\n"
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
