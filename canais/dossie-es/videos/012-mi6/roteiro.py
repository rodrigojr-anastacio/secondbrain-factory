#!/usr/bin/env python3
"""Fonte única do dossie-es 012 (El MI6): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (na pasta do vídeo). Conteúdo no topo; geração no fim (copiada do 011-templarios).

Embalagem aprovada no crivo r3 (18/11/2026, EMBALAGEM.md/CRIVO.md):
  A/T1 "MI6: el plan nazi para Sudamérica que nadie escribió en Berlín" + máquina de escrever no escuro, sello NUEVA YORK (objeto-simbolo, controle)
  B/T2 "Cómo el MI6 engañó a un presidente, a un país y a sí mismo" + rosto de Roosevelt aos microfones, folha riscada, ¿SABÍA? (rosto-emocao, TESTE personagem)
  C/T3 "El Complot Nazi que Nunca Existió | Expedientes Secretos del MI6" + o mapa em 5 blocos sendo traçado, 14 → 5 (mapa-lugar)
  Frase-âncora do hook: "Esta es TODA la historia del MI6. Y de los papeles con que movió el mundo."
Ângulo (ANGULO.md): a história inteira contada pelos papéis que o MI6 fabricou, vazou ou fez sumir; miolo nas Américas (BSC 1940–41).
Fora da manada: El Diario, El Telegrama, La Carta (Zinoviev), El Pasaporte, La Isla, La Firma, El Mapa, La Aerolínea, El Registro, El Misil.
Fatos obrigatórios da manada (1909, Philby, Iraque/Chilcot, 1992) só como contexto curto, nunca como cena principal na ordem deles.

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (id I### na ordem de aparição) · "chave" reuso · "chave#enq" reuso com enquadramento
  + "@@TEXTO"      rótulo na tela (máquina de escrever; CAIXA ALTA, até ~28 caracteres)
Bloco: b(texto, *planos, card="WASHINGTON, 1941", ideia=True) · capítulo: cap("5. La Isla")
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
HOOK_MAX = 36.0      # s: a bíblia pede hook de 25–35 s (EMBALAGEM: frase-âncora até 0:35)
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "MI6: el plan nazi para Sudamérica que nadie escribió en Berlín"
TITULOS = ("T1 MI6: el plan nazi para Sudamérica que nadie escribió en Berlín / "
           "T2 Cómo el MI6 engañó a un presidente, a un país y a sí mismo / "
           "T3 El Complot Nazi que Nunca Existió | Expedientes Secretos del MI6")
PROMESSA = ("Toda la historia del MI6 contada por los papeles que fabricó, filtró o hizo desaparecer, empezando por el plan "
            "nazi para Sudamérica que Roosevelt anunció por radio en 1941 y que, según los historiadores, salió de una "
            "oficina británica en Nueva York.")

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Washington, veintisiete de octubre de mil novecientos cuarenta y uno. El presidente Roosevelt habla por radio al país.", card="WASHINGTON, 1941")
b("Dice tener un mapa secreto, hecho en Alemania por el gobierno de Hitler. Catorce países de Sudamérica y Centroamérica se reducen a cinco estados vasallos. Uno incluye el canal de Panamá.")
b("Berlín lo llama falsificación. Según los historiadores, lo era: el mapa salió de una oficina británica en Nueva York.")
b("Esta es TODA la historia del MI6. Y de los papeles con que movió el mundo.", ideia=True)

# ───────────────────────── 1. EL DIARIO ─────────────────────────
cap("1. El Diario")
b("El Diario. Londres, siete de octubre de mil novecientos nueve. Un oficial de la Armada, Mansfield Cumming, anota en su diario su primer día completo de trabajo.", card="LONDRES, 1909")
b("Fue a la oficina, se quedó todo el día, no vio a nadie y no había nada que hacer.")
b("Cumming dirige la sección exterior de una nueva Oficina del Servicio Secreto, creada por un gobierno preocupado por los espías alemanes. La sección interior será el MI5. La suya, el MI6. Casi no tiene personal ni presupuesto.")
b("El servicio secreto más famoso del mundo nace casi con una página en blanco. Siete años después, un papel cambia una guerra. Y no es obra del MI6.", ideia=True)

# ───────────────────────── 2. EL TELEGRAMA ─────────────────────────
cap("2. El Telegrama")
b("El Telegrama. Enero de mil novecientos diecisiete. Berlín envía un mensaje cifrado a su representante en México, a través de su embajada en Washington. Propone a México una alianza si Estados Unidos entra en la guerra.", card="MÉXICO, 1917")
b("A cambio, dinero y ayuda para recuperar Texas, Nuevo México y Arizona. Lo descifran en Londres, en la Sala Cuarenta de la Armada británica, no en la oficina de Cumming.")
b("Para ocultar que leen los telegramas alemanes, consiguen una copia en Ciudad de México. El primero de marzo, el telegrama sale en la prensa estadounidense.")
b("Dos días después, el jefe de la diplomacia alemana, Arthur Zimmermann, admite que es auténtico. En abril, Estados Unidos entra en la guerra. No fue la única razón, pero pesó.")
b("En Londres queda la lección: un papel bien colocado puede mover a Washington. Antes de aplicarla, otro papel les estalla en las manos.", ideia=True)

# ───────────────────────── 3. LA CARTA ─────────────────────────
cap("3. La Carta")
b("La Carta. Riga, otoño de mil novecientos veinticuatro. La delegación del MI6 en Letonia envía a Londres la copia de una carta atribuida a Grigori Zinóviev, jefe de la Internacional Comunista.", card="RIGA, 1924")
b("La carta pide a los comunistas británicos preparar la revolución. Llega en plena campaña electoral, con un gobierno laborista que acaba de firmar tratados con Moscú.")
b("El veinticinco de octubre, el diario Daily Mail la publica en portada. Moscú dice que es falsa. Cuatro días después, los laboristas pierden las elecciones.")
b("En mil novecientos noventa y nueve, la historiadora del Foreign Office Gill Bennett concluyó que es imposible saber quién la escribió. Lo más probable, según ella, es que la encargaran exiliados rusos.")
b("Y que oficiales de los servicios secretos británicos la filtraran a los conservadores y a la prensa. Un país votó con un papel falso sobre la mesa.", ideia=True)

# ───────────────────────── 4. EL PASAPORTE ─────────────────────────
cap("4. El Pasaporte")
b("El Pasaporte. Nueva York, junio de mil novecientos cuarenta. Llega un millonario canadiense, William Stephenson, piloto en la Primera Guerra Mundial. Su cargo es modesto: oficial de control de pasaportes.", card="NUEVA YORK, 1940")
b("Es la cobertura clásica del MI6 en el extranjero. Meses antes, esa oficina tenía nueve personas. Stephenson la convierte en la Coordinación de Seguridad Británica, la BSC.")
b("Cientos de personas trabajan para ella desde la oficina tres mil seiscientos tres del Rockefeller Center. Gran Bretaña está sola frente a Hitler. Estados Unidos es neutral.")
b("Según su propia historia interna, la BSC tiene dos misiones: localizar agentes nazis en el continente y lograr que Washington entre en la guerra.")
b("Para cumplir las dos misiones necesita papeles. Y muchos de los que cruzan el Atlántico pasan por una isla.", ideia=True)

# ───────────────────────── 5. LA ISLA ─────────────────────────
cap("5. La Isla")
b("La Isla. Bermudas, mil novecientos cuarenta y uno. En el hotel Princess de Hamilton, cerca de mil censores británicos abren las cartas que viajan entre América y Europa.", card="BERMUDAS, 1941")
b("Cada bolsa de correo que hace escala en la isla se abre, se lee y se vuelve a cerrar. Algunas cartas pasan por pruebas químicas.")
b("Según el oficial de la BSC Montgomery Hyde, una censora, Nadya Gardner, sospecha de unas cartas firmadas por un tal Joe K. Propone probarlas con yodo. Aparece una escritura oculta sobre barcos y aviones.")
b("Las cartas pasan al FBI. En agosto cae en Estados Unidos la red de espías de Kurt Ludwig.")
b("La censura no solo caza espías. También guarda copias de cartas auténticas. Según el propio Hyde, una de ellas, la de un militar boliviano, servirá de modelo.", ideia=True)

# ───────────────────────── 6. LA FIRMA ─────────────────────────
cap("6. La Firma")
b("La Firma. La Paz, julio de mil novecientos cuarenta y uno. El gobierno del general Peñaranda recibe una carta por medio del representante de Estados Unidos.", card="LA PAZ, 1941")
b("Aparece firmada por el mayor Elías Belmonte, agregado aéreo de Bolivia en Berlín, y dirigida al representante alemán en La Paz, Ernst Wendler. Según la carta, se acerca el momento de dar un golpe de Estado.")
b("El gobierno boliviano declara el estado de sitio, cierra periódicos, detiene a dirigentes políticos y expulsa al diplomático alemán.")
b("En mil novecientos sesenta y dos, Hyde contó su versión: la carta era falsa, obra de los británicos. Relatos posteriores añaden un laboratorio en Toronto y una máquina de escribir hecha para imitar la de Belmonte.")
b("En dos mil veinticuatro, un estudio académico la puso en duda: no encontró pruebas en los archivos. Tres meses después, otro papel sale de Toronto.", ideia=True)

# ───────────────────────── 7. EL MAPA ─────────────────────────
cap("7. El Mapa")
b("El Mapa. Toronto, otoño de mil novecientos cuarenta y uno. Según el museo de la inteligencia militar británica, allí funciona un laboratorio secreto, la Estación M, dirigido por un autor de canciones, Eric Maschwitz.", card="TORONTO, 1941")
b("Según la misma fuente, la idea fue de un agente de la BSC, Ivar Bryce. El mapa se fabrica en dos días, envejecido y manchado como si hubiera viajado, y llega a Roosevelt a través del director del FBI.")
b("¿Lo sabía Roosevelt? Según el historiador Nicholas Cull, en un borrador del discurso tachó la frase que decía: un mapa de autenticidad indudable. Por radio dijo únicamente: un mapa secreto. Nadie sabe si fue engañado o si solo dudaba.")
b("Berlín lo niega. Después de la guerra, en los archivos alemanes capturados no aparece ningún mapa así. No hay rastro de ese complot nazi para Sudamérica: según los historiadores, nunca existió.")
b("Cuarenta y un días después del discurso, Japón ataca Pearl Harbor.", ideia=True)
b("Si te está gustando este expediente, suscríbete. Porque ese mismo año, la BSC dirige otro papel contra Brasil.")

# ───────────────────────── 8. LA AEROLÍNEA ─────────────────────────
cap("8. La Aerolínea")
b("La Aerolínea. Río de Janeiro, finales de mil novecientos cuarenta y uno. La aerolínea italiana LATI une Roma con Brasil. Según Londres y Washington, transporta agentes, valijas diplomáticas y mercancías del Eje.", card="RÍO DE JANEIRO, 1941")
b("La compañía tiene aliados en el gobierno de Getúlio Vargas, así que las quejas oficiales no funcionan. Según la propia BSC, sus agentes fabrican una carta de la dirección de LATI que insulta al presidente Vargas. Y logran que le llegue.")
b("En diciembre, tras Pearl Harbor y con la presión de Estados Unidos, Vargas ordena expropiar LATI y la compañía alemana Cóndor. La carta no fue la única razón. Pero la BSC se atribuyó el mérito.")
b("Estados Unidos ya está en guerra, pero por Pearl Harbor, no por los papeles de la BSC. Y mientras el MI6 fabrica papeles para engañar a otros, una traición crece dentro de su propia casa.", ideia=True)

# ───────────────────────── 9. EL COMUNICADO ─────────────────────────
cap("9. El Comunicado")
b("El Comunicado. Londres, siete de noviembre de mil novecientos cincuenta y cinco. En la Cámara de los Comunes, el jefe de la diplomacia británica, Harold Macmillan, habla de un antiguo oficial del MI6.", card="LONDRES, 1955")
b("No tengo razones, dice, para concluir que el señor Philby haya traicionado nunca los intereses de este país.")
b("El señor Philby es Kim Philby. La inteligencia soviética lo reclutó en mil novecientos treinta y cuatro. Desde mil novecientos cuarenta y cuatro dirigió la sección del MI6 que debía combatir a los soviéticos.")
b("En mil novecientos cincuenta y uno, dos diplomáticos amigos suyos huyen a Moscú y las sospechas caen sobre él. El papel de Macmillan lo exculpa en público. En enero de mil novecientos sesenta y tres, desde Beirut, Philby huye a la Unión Soviética.")
b("El servicio que engañaba a otros con papeles estaba engañado por dentro. Y al año siguiente del comunicado, otro papel desaparece para proteger al servicio.", ideia=True)

# ───────────────────────── 10. EL REGISTRO ─────────────────────────
cap("10. El Registro")
b("El Registro. Portsmouth, abril de mil novecientos cincuenta y seis. El crucero soviético Ordzhonikidze llega con Nikita Jruschov y Nikolái Bulganin, en visita oficial a Gran Bretaña. El gobierno de Anthony Eden quiere que nada la arruine.", card="PORTSMOUTH, 1956")
b("El diecinueve de abril, un buzo veterano, el comandante Lionel Crabb, se sumerge en el puerto para examinar el casco del crucero, en una misión del MI6. No vuelve a la superficie.")
b("Del libro de registro de su hotel desaparecen las páginas con su nombre y el del hombre que lo acompañaba. El Almirantado anuncia que no regresó de unas pruebas de equipo submarino.")
b("Moscú protesta. Eden dice en privado que la operación se hizo sin su autorización. Los primeros documentos del caso no se hicieron públicos hasta dos mil seis.")
b("Ahora, para proteger al servicio, alguien arranca páginas. Veinticinco años después, el papel que fracasa es una advertencia.", ideia=True)

# ───────────────────────── 11. EL MISIL ─────────────────────────
cap("11. El Misil")
b("El Misil. Londres, julio de mil novecientos ochenta y uno. El Comité Conjunto de Inteligencia, que reúne lo que saben el MI6 y los demás servicios, escribe que no se puede descartar un intento argentino de tomar las Malvinas por la fuerza.", card="LONDRES, 1981")
b("El dos de abril de mil novecientos ochenta y dos, tropas argentinas desembarcan en las islas. Un año después, el informe oficial Franks no culpa al gobierno de Margaret Thatcher por la decisión argentina.", card="MALVINAS, 1982")
b("En la guerra, lo que más preocupa a Londres es el misil francés Exocet. Argentina tiene pocos y busca más. Según el historiador Lawrence Freedman, que escribió por encargo del gobierno británico, agentes británicos se hacen pasar por compradores en el mercado de armas, para que Argentina no consiga más.")
b("Según Londres, no los consiguió. En setenta y cuatro días, el conflicto dejó más de novecientos muertos entre argentinos, británicos y habitantes de las islas.")
b("Esta vez el engaño no fue de documentos, sino de identidades falsas. Veinte años después, un dossier del gobierno británico, apoyado en informes del MI6, ayuda a llevar a su país a otra guerra.", ideia=True)

# ───────────────────────── 12. EL INFORME ─────────────────────────
cap("12. El Informe")
b("El Informe. Londres, seis de julio de dos mil dieciséis. Tras siete años de investigación, John Chilcot presenta su informe sobre la participación británica en la guerra de Irak, que empezó en dos mil tres.", card="LONDRES, 2016")
b("Concluye que lo que se afirmaba sobre las armas de destrucción masiva de Sadam Husein se presentó con una certeza injustificada. Parte de los informes del MI6 venía de fuentes poco comprobadas. Algunos se retiraron después.")
b("Las armas nunca aparecieron.")
b("Como en mil novecientos diecisiete y en mil novecientos cuarenta y uno, un papel pesó en una decisión de guerra. Pero esta vez, el país convencido con certezas injustificadas era el propio.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. El Mapa")
b("El Mapa. Hoy el MI6 tiene página web y publica ofertas de empleo. Su existencia no se reconoció oficialmente hasta mil novecientos noventa y dos. En dos mil veinticinco, por primera vez, lo dirige una mujer.", card="LONDRES, HOY")
b("Del mapa de Roosevelt no hay rastro en los archivos alemanes. Según los historiadores, salió de la inteligencia británica en Nueva York. Según el museo militar británico, de un laboratorio en Toronto.")
b("En más de un siglo, el MI6 robó secretos, como cualquier servicio. Pero muchas de sus historias más conocidas giran en torno a papeles: los que escribió, los que filtró y los que hizo desaparecer.")
b("Un espía roba documentos. En estos expedientes, el MI6 aprendió algo más útil: a escribirlos.", ideia=True)
b("Y tú, ¿crees que hoy un documento falso todavía podría cambiar una guerra? Déjalo en los comentarios.")

# ───────────────────────── STORYBOARD (planos por bloco, na ordem dos blocos) ─────────────────────────
SEM = ", no lettering anywhere"      # papéis, placas, capas: o nano-banana inventa texto
VIOL = ", seen from far away, no bodies, no blood"
NOARM = ", no weapons pointed at anyone"
NOINS = ", no flags, no insignia, no eagles, no swastikas, no badges"
ILEG = "the writing only as faint completely illegible blurred lines, no readable letters"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, rivers and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame, no ocean names"
FORGED = "an old travel-stained paper map of South America and Central America down from Panama, the continent divided into five large flat zones of muted ink colors (slate blue, olive, sepia, ochre, grey) with thick borders that ignore the real countries, no labels, no text, no letters, no symbols, no flags, no insignia"
# Personagens (descrição visual fixa; "resembling", nunca foto; sem insígnias inventadas)
FDR = "a man resembling Franklin D. Roosevelt in 1941, aged about sixty, pince-nez glasses, dark grey suit"
CUMMING = "a man resembling Mansfield Cumming in 1909, aged about fifty, clean-shaven with a strong jaw and a monocle, dark civilian suit"
ZIMM = "a German official of about sixty resembling Arthur Zimmermann in 1917, bald with a moustache, dark frock coat, plain civilian clothes"
ZINOV = "a man resembling Grigory Zinoviev in 1924, about forty, thick curly dark hair, round face, dark jacket"
STEPH = "a short wiry man of about forty-three resembling William Stephenson in 1940, dark hair combed back, dark double-breasted suit"
HYDE = "a British man of about thirty-five resembling Harford Montgomery Hyde in 1941, round glasses, dark hair, civilian suit"
GARDNER = "a young woman of about twenty-five in 1941, wavy dark hair, cardigan and blouse"
BELM = "a Bolivian air force major of about thirty-six in 1941, dark hair and a thin moustache, plain military tunic without any insignia"
PENAR = "a Bolivian general of about fifty-five resembling Enrique Peñaranda in 1941, moustache, plain khaki uniform without insignia"
WENDL = "a German diplomat of about forty-five in 1941, grey suit, plain civilian clothes without any badge"
MASCH = "an elegant British man of about forty resembling Eric Maschwitz in 1941, dark parted hair, tweed jacket"
BRYCE = "a tall handsome British man of about thirty-four resembling Ivar Bryce in 1941, light grey suit"
HOOVER = "a stocky man of about forty-six resembling J. Edgar Hoover in 1941, dark suit"
VARGAS = "a short stout man of about fifty-eight resembling Getúlio Vargas in 1941, round face, combed-back grey hair, light suit"
MACM = "a tall man of about sixty-one resembling Harold Macmillan in 1955, moustache, dark three-piece suit"
PHILBY = "a man of about forty-three resembling Kim Philby in 1955, dark hair, tweed jacket, tie"
CRABB = "a small wiry man of about forty-six resembling Lionel Crabb in 1956, moustache, in a dark rubber frogman diving suit"
EDEN = "a tall elegant man of about fifty-eight resembling Anthony Eden in 1956, moustache, dark suit"
KHRU = "a bald stocky man of about sixty-two resembling Nikita Khrushchev in 1956, dark suit"
THATCH = "a woman of about fifty-six resembling Margaret Thatcher in 1982, blond helmet hairstyle, dark blue suit"
CHILC = "an elderly British man of about seventy-seven resembling Sir John Chilcot in 2016, white hair, glasses, dark suit"
SB = [
 # N001 Washington, 27/10/1941, Roosevelt por radio
 [f"fdr_radio|{FDR} speaking at a wooden podium into three 1940s radio microphones without any lettering, hotel banquet hall behind, warm stage light", "mayflower_hall|Wide shot of a grand 1941 hotel banquet hall in Washington, round tables with white cloths, guests in evening dress and naval officers listening, chandeliers" + NOINS, "radio_family|An American family in 1941 gathered around a wooden console radio in a living room at night, listening seriously"],
 # N002 mapa secreto; 14 países → 5; Panamá
 [f"secret_map|{FORGED}, lying on a dark wooden desk under lamp light", "map_14|" + MAPA + ", showing South America and Central America with the real country borders as thin lines", f"fdr_close|Close-up of {FDR}, grave determined face, speaking", "panama_canal|The Panama Canal locks in 1941 seen from above, a cargo ship inside a lock, jungle around", "border_ink|Close-up of a fountain pen nib drawing a thick dark ink border line across an old paper map, no labels, no letters"],
 # N003 Berlín lo llama falsificación; oficina británica en Nueva York
 ["berlin_ministry|A massive stone government building in Berlin in 1941 at dusk, plain facade" + NOINS, "ny_office_night|A lit office window high in a 1941 New York skyscraper at night, a man working at a desk covered with papers, seen from outside", "rockefeller_1941|The bronze Atlas statue holding an armillary sphere in front of an art deco skyscraper at Rockefeller Center, New York, 1941, daytime, pedestrians in hats" + SEM],
 # N004 Esta es TODA la historia del MI6
 ["case_file|A brown cardboard case folder on a dark desk, the corner of an old map sticking out of it, a red rubber stamp and a desk lamp" + SEM, "red_stamp|A hand slamming a red rubber stamp onto a brown paper case file, ink splash, dramatic close-up" + SEM, "typewriter_dark|A 1940s black typewriter alone on a dark wooden desk, a single completely blank sheet of paper in the roller, a strong cone of warm desk-lamp light from the upper left, deep slate-blue darkness around, no brand name" + SEM],
 # N005 El Diario. Londres, 7/10/1909, Cumming anota su primer día
 ["london_1909|A London street in Whitehall in 1909, horse-drawn cabs and early motor cars, men in bowler hats, grey autumn light", f"cumming_desk|{CUMMING} sitting alone at a bare wooden desk in a small empty office, 1909@@MANSFIELD CUMMING", f"diary_open|An open leather-bound diary on a desk with a fountain pen, a few handwritten lines with {ILEG}, 1909", "office_door|A plain wooden office door at the end of a quiet London corridor, 1909, closed, no sign" + SEM],
 # N006 fue a la oficina… no vio a nadie… nada que hacer
 ["empty_office|A small bare office in 1909 with one desk, one empty chair and a window with grey light, dust in the air", f"cumming_window|{CUMMING} standing at a window looking out at rainy London rooftops, 1909", "wall_clock|Close-up of an office wall clock with Roman numerals in an empty room, 1909"],
 # N007 sección exterior; gobierno preocupado por espías alemanes; MI5/MI6; sin personal ni presupuesto
 [f"cumming_portrait|Medium shot of {CUMMING} adjusting his monocle, 1909", "spy_fever|A crowd of Londoners at a newsstand in 1909 reading newspapers with worried faces, the newspapers only as grey blocks" + SEM, "parliament_1909|The Houses of Parliament in London seen from the Thames in 1909, a steam boat on the river", "two_officers|An army officer and a naval officer shaking hands in a wood-panelled office in 1909, plain uniforms without medals", "ledger_empty|An almost empty account ledger with a few coins beside it on a desk, 1909, " + ILEG, "cumming_alone|A lone man in a dark suit walking up a dim stairway of a London office building, seen from behind, 1909"],
 # N008 página en blanco; siete años después un papel cambia una guerra
 ["blank_page|A single blank page of a leather diary under warm lamp light, a fountain pen resting beside it", "diary_close|A hand closing a leather-bound diary on a desk, 1909", "telegraph_room|A 1917 telegraph room with operators wearing headphones at long tables of equipment", "telegram_blank|A completely blank yellowed telegram form on a desk beside a pencil, 1917" + SEM],
 # N009 El Telegrama. Enero 1917, Berlín → representante en México vía Washington; alianza
 ["berlin_1917|A Berlin government street in winter 1917, grey buildings, snow, a horse-drawn carriage", f"zimmermann|{ZIMM} at a desk dictating to a secretary, 1917@@ARTHUR ZIMMERMANN", "telegraph_key|Close-up of a hand tapping a brass telegraph key, 1917", "map_americas|" + MAPA + ", showing Mexico and the southern United States", "embassy_1917|A stately embassy building in Washington in 1917 in winter, plain facade" + NOINS],
 # N010 Texas, Nuevo México, Arizona; Sala Cuarenta
 ["rio_grande|Wide desert landscape of the Rio Grande border between Mexico and Texas in 1917, mesas, no people", "gold_coins|A stack of gold coins and banknotes on a wooden table, 1917", "room40|British men in suits decoding messages at long tables covered with papers in a smoky wood-panelled room of the Admiralty, 1917@@SALA 40", "codebook|A thick codebook open beside pencil worksheets with columns of numbers, " + ILEG],
 # N011 copia en Ciudad de México; prensa estadounidense
 ["mexico_telegraph|The interior of a telegraph office in Mexico City in 1917, clerks at counters, arched windows", "copy_hand|A hand copying a telegram by lamp light at night, " + ILEG, "newsboys_1917|American newsboys selling newspapers on a busy street corner in 1917, the newspapers only as grey blocks" + SEM],
 # N012 Zimmermann admite; abril, EE. UU. en guerra
 [f"zimm_press|{ZIMM} speaking to a group of reporters in a hall, 1917", "congress_1917|The chamber of the United States Congress in 1917 during a crowded session, wide shot", "troopship_1917|American soldiers boarding a troopship in New York harbor in 1917, seen from far away", "ny_harbor_1917|New York harbor in 1917 with a troopship leaving past the skyline, grey morning"],
 # N013 la lección: un papel bien colocado mueve a Washington; otro papel les estalla
 ["whitehall_1917|British officials reading a telegram together in a wood-panelled London office, 1917", "capitol_1917|The United States Capitol in Washington in 1917, winter light", "sealed_envelope|An envelope with a red wax seal on a dark desk, 1924" + SEM],
 # N014 La Carta. Riga 1924, delegación del MI6, carta atribuida a Zinóviev
 ["riga_1924|The old town of Riga in autumn 1924, church spires, cobbled street, people in coats", "riga_office|A British officer in a small office in Riga in 1924 handing a sealed envelope to a courier", f"zinoviev|{ZINOV}, portrait in a dim office, 1924@@GRIGORI ZINÓVIEV", "letter_typed|A typed letter on a desk with a signature scrawl at the bottom, " + ILEG + ", 1924"],
 # N015 revolución; campaña electoral; gobierno laborista, tratados con Moscú
 ["workers_hall|A crowded British workers' meeting hall in 1924, a speaker at the front, no symbols, no banners with text", "election_street|A London street in October 1924 with blank election posters on the walls and people walking" + SEM, "macdonald|A man of about fifty-eight resembling Ramsay MacDonald in 1924, moustache, speaking at a podium", "treaty_table|Diplomats signing documents at a long table in a London government room, 1924"],
 # N016 Daily Mail en portada; Moscú dice falsa; laboristas pierden
 ["printing_press|A newspaper printing press rolling at night in 1924, workers checking sheets", "front_page|A 1924 newspaper front page lying on a table, the headlines only as large black illegible blocks" + SEM, "polling_station|Voters queuing at a 1924 polling station in a school hall in England"],
 # N017 1999, Gill Bennett: imposible saber; exiliados rusos
 ["bennett|A British woman historian of about fifty in 1999 reading old files at a table in a government records room@@GILL BENNETT", "archive_boxes|Grey archive boxes stacked on metal shelves in a government archive", "emigre_cafe|Russian émigré men in heavy coats talking at a table in a 1920s Berlin café", "forger_desk|A forger's desk in 1924 with pens, ink bottles, a magnifying glass and papers, " + ILEG],
 # N018 oficiales la filtran a los conservadores y a la prensa; un país votó con un papel falso
 ["club_room|Men in suits reading newspapers in a smoky London gentlemen's club room, 1924", "ballot_hand|A hand dropping a folded ballot paper into a wooden ballot box, 1924", "front_page#detalhe-centro", "polling_station#médio-dir"],
 # N019 El Pasaporte. Nueva York, junio 1940, Stephenson
 ["ny_harbor_1940|New York harbor in June 1940, an ocean liner arriving past the Manhattan skyline", f"stephenson|{STEPH} standing on the deck of a liner looking at Manhattan, 1940@@WILLIAM STEPHENSON", "camel_1918|A First World War Sopwith Camel biplane flying over fields in 1918, seen from far away, no markings", "passport_desk|A consulate desk with a pile of plain passports and a rubber stamp, 1940" + SEM],
 # N020 cobertura del MI6; nueve personas; BSC
 ["passport_desk#detalhe-centro", "small_office|Nine people working crowded together in a small cramped office in 1939", f"steph_window|{STEPH} looking down from a high skyscraper window over Manhattan, 1940", "bsc_typists|Dozens of women typists working in rows in a large office in 1941"],
 # N021 oficina 3603 del Rockefeller Center; Gran Bretaña sola; EE. UU. neutral
 ["rockefeller_1941#aberto", "office_3603|The corridor of an art deco skyscraper in 1941, a closed office door with a plain frosted glass panel" + SEM + "@@OFICINA 3603", "blitz_skyline|The London skyline at night in 1940 with searchlights and distant smoke, seen from far away", "radio_family#médio-esq"],
 # N022 dos misiones: agentes nazis en el continente; Washington en guerra
 ["agent_pier|A man in a trench coat photographing ships from a New York pier in 1941, seen from behind" + NOINS, "capitol_1941|The United States Capitol in Washington in 1941, autumn", "stephenson#médio-dir"],
 # N023 necesita papeles; cruzan el Atlántico por una isla
 ["mail_seaplane|Canvas mail sacks being unloaded from a large flying boat at a wooden dock, 1941", "clipper|A Boeing 314 flying boat floating at a dock in a turquoise bay in 1941, plain silver livery without lettering or logos", "map_atlantic|" + MAPA + ", showing the Atlantic Ocean between North America and Europe with the small islands of Bermuda"],
 # N024 La Isla. Bermudas 1941, hotel Princess, mil censores
 ["princess_hotel|A large pink colonial hotel on the waterfront of Hamilton, Bermuda, in 1941, palm trees, small boats", "censors_room|Hundreds of censors, mostly young women, at long tables opening letters in a hotel ballroom in 1941@@HOTEL PRINCESS", "steam_letter|Close-up of hands opening a letter over a jet of steam, 1941", "clipper#médio-dir"],
 # N025 cada bolsa se abre, se lee, se cierra; pruebas químicas
 ["mail_bags|Canvas mail bags emptied onto long tables, piles of envelopes, 1941", "chem_test|A woman censor brushing a clear chemical onto a letter in a small laboratory corner, 1941", "steam_letter#detalhe-centro"],
 # N026 según Hyde, Nadya Gardner, Joe K, yodo, escritura oculta
 [f"hyde|{HYDE} in an office in Bermuda, 1941@@MONTGOMERY HYDE", f"gardner|{GARDNER} examining a letter under a desk lamp, frowning@@NADYA GARDNER", "iodine|Close-up of a brush spreading brown iodine on a letter, faint brown lines appearing, " + ILEG, "hidden_lines|A letter where faint brown hidden lines of writing appear between the normal lines, " + ILEG],
 # N027 las cartas pasan al FBI; cae la red de Ludwig
 ["fbi_office|FBI agents in a 1941 office examining letters with magnifying glasses", "arrest_road|Two FBI agents in hats stopping a man beside a car on a mountain road in 1941, seen from far away" + NOARM, "agent_pier#médio-esq"],
 # N028 guarda copias de cartas auténticas; la de un militar boliviano, modelo
 ["copy_cabinet|An open filing cabinet drawer packed with photostat copies of letters, 1941", "real_letter|A genuine typed letter on plain official paper with a signature, " + ILEG + ", 1941", "censors_room#detalhe-centro", "copy_cabinet#detalhe-alto"],
 # N029 La Firma. La Paz, julio 1941, Peñaranda recibe la carta por el representante de EE. UU.
 ["la_paz_1941|The city of La Paz in 1941 in its canyon, the snow-capped Illimani mountain behind", f"penaranda|{PENAR} at his desk in a government office, 1941@@ENRIQUE PEÑARANDA", "us_minister|An American diplomat of about fifty in a dark suit handing an envelope to a Bolivian minister in an office, 1941", "la_paz_1941#detalhe-centro"],
 # N030 firmada por Belmonte, agregado en Berlín; a Wendler; golpe de Estado
 [f"belmonte|{BELM}, portrait in a Berlin office, 1941@@ELÍAS BELMONTE", "berlin_ministry#detalhe-alto", f"wendler|{WENDL} in an office in La Paz, 1941@@ERNST WENDLER", "coup_letter|Close-up of a typed letter on a desk, " + ILEG + ", a signature at the bottom", "signature|Extreme close-up of an ink signature scrawl at the bottom of a typed letter, no readable letters"],
 # N031 estado de sitio, periódicos cerrados, detenidos, expulsión
 ["la_paz_soldiers|Bolivian soldiers standing guard in a La Paz street in 1941, seen from far away" + NOARM, "closed_press|A newspaper office in La Paz in 1941 with its shutters closed and a guard at the door" + SEM, "train_departure|A German diplomat in a grey suit boarding a train at a mountain railway station, 1941" + NOINS],
 # N032 1962, Hyde: carta falsa; relatos: laboratorio en Toronto y máquina hecha a medida
 ["hyde#médio-dir", "toronto_lab|A basement laboratory in 1941 with chemists at benches, ink bottles, typewriters and magnifying lamps@@ESTACIÓN M", "custom_typewriter|A technician assembling a typewriter on a workbench, its keys and type bars spread out, 1941" + SEM, "typewriter_dark#detalhe-centro", "casa_loma|The Casa Loma castle in Toronto in 1941, autumn trees"],
 # N033 2024, estudio académico: no encontró pruebas; otro papel sale de Toronto
 ["scholar_2024|A researcher in a modern archive reading room looking through old folders, 2024", "archive_boxes#médio-esq", "casa_loma#médio-dir"],
 # N034 El Mapa. Toronto, otoño 1941, Estación M, Maschwitz
 [f"maschwitz|{MASCH} in a basement workshop, 1941@@ERIC MASCHWITZ", "toronto_lab#detalhe-centro", "custom_typewriter#detalhe-centro", "graphologist|A man with a magnifying glass studying handwriting on a sheet under a lamp, 1941"],
 # N035 Bryce; dos días; envejecido, manchado; llega a Roosevelt por el director del FBI
 [f"bryce|{BRYCE} in a New York office, 1941@@IVAR BRYCE", f"drawing_map|A hand with a fountain pen drawing thick borders on {FORGED}", f"aging_map|A technician dabbing tea stains and rubbing the edges of {FORGED}", f"hoover|{HOOVER} at his desk holding a brown envelope, 1941@@DIRECTOR DEL FBI", "white_house_1941|The White House in Washington in autumn 1941"],
 # N036 ¿Lo sabía? borrador tachado: "de autenticidad indudable" → "un mapa secreto"
 ["draft_speech|A typed speech page on a desk with one whole line struck through with a thick red pencil stroke, " + ILEG, f"fdr_desk|{FDR} at his desk in the Oval Office editing a typed speech with a pencil, 1941", "fdr_close#detalhe-centro", "fdr_radio#detalhe-alto", f"fdr_doubt|{FDR} looking down at a folded paper with a doubtful expression, 1941"],
 # N037 Berlín lo niega; archivos capturados; complot nunca existió
 ["berlin_ministry#médio-esq", "captured_archives|Allied soldiers sorting crates of captured documents in a large hall in 1945" + NOINS, "secret_map#detalhe-centro", "empty_drawer|An empty pulled-out archive drawer in a dim records room"],
 # N038 41 días después, Pearl Harbor
 ["pearl_harbor|Columns of black smoke rising over the harbor of Pearl Harbor on 7 December 1941, seen from far away, no bodies, no blood", "fdr_radio#médio-dir"],
 # N039 CTA; la BSC dirige otro papel contra Brasil
 ["case_file#detalhe-centro", "rio_bay_1941|The bay of Rio de Janeiro in 1941 with the Sugarloaf mountain", "red_stamp#aberto"],
 # N040 La Aerolínea. Río, finales de 1941, LATI Roma–Brasil
 ["rio_1941|Downtown Rio de Janeiro in 1941, avenues with palm trees and trams", "lati_plane|A 1941 Italian three-engine airliner parked on an airfield in Brazil, plain livery without any lettering, flags or emblems", "diplomatic_bags|Sealed diplomatic bags being loaded into the hold of an airliner, 1941", "lati_plane#detalhe-centro"],
 # N041 aliados en el gobierno de Vargas; la BSC fabrica una carta que insulta a Vargas
 [f"vargas|{VARGAS} in his office, 1941@@GETÚLIO VARGAS", "rio_1941#médio-dir", "lati_letter|A typed letter on letterhead paper, " + ILEG + ", a signature, 1941", "cafe_handover|Two men in a Rio café in 1941 sliding an envelope across a table", f"vargas_reading|{VARGAS} reading a letter with an angry face, 1941"],
 # N042 diciembre: Vargas expropia LATI y Cóndor; no fue la única razón
 ["grounded_plane|An airliner on the ground guarded by Brazilian soldiers in 1941, seen from far away" + NOARM, "condor_plane|A German Junkers trimotor airliner on an airfield in Brazil in 1941, plain livery without any lettering, flags or emblems", "pearl_harbor#médio-esq", "vargas#detalhe-centro", "lati_letter#detalhe-centro"],
 # N043 EE. UU. en guerra por Pearl Harbor; una traición crece dentro del MI6
 ["us_march|American soldiers marching on a city street in early 1942, seen from far away", "ny_office_night#detalhe-centro", "blitz_skyline#médio-dir", "shadow_man|A man in a trench coat walking away down a dark London street at night in 1944, face hidden in shadow"],
 # N044 El Comunicado. Londres, 7/11/1955, Macmillan en los Comunes
 ["commons_1955|The House of Commons chamber in 1955, full green benches", f"macmillan|{MACM} standing at the dispatch box with papers, 1955@@HAROLD MACMILLAN", "westminster_1955|The Palace of Westminster in London in November 1955, fog over the Thames", "dispatch_box|Close-up of a wooden dispatch box with typed papers on it, " + ILEG],
 # N045 "No tengo razones…"
 ["macmillan#detalhe-centro", "statement_paper|A hand holding a typed statement page, " + ILEG, "commons_1955#detalhe-centro"],
 # N046 Kim Philby: reclutado 1934; desde 1944 dirige la sección contra los soviéticos
 [f"philby|{PHILBY}, portrait, calm smile@@KIM PHILBY", f"philby_office|{PHILBY.replace('forty-three', 'thirty-two')} reading files at a desk in a 1944 London office", "file_stack|A stack of brown files tied with string on a desk, 1944" + SEM, "statement_paper#detalhe-alto"],
 # N047 1951 dos diplomáticos huyen; Macmillan lo exculpa; 1963 Beirut, huye
 ["ferry_night|A cross-Channel ferry leaving a harbour at night in 1951, two men in coats on deck seen from behind", "philby#médio-esq", "macmillan#médio-dir", "beirut_1963|The Beirut seafront in January 1963, palm trees and hotels", "freighter_night|A Soviet cargo ship leaving Beirut harbour at night, 1963", "shadow_man#detalhe-centro"],
 # N048 engañado por dentro; al año siguiente otro papel desaparece
 ["office_1950s|A grey London office building at dusk in the 1950s, a few lit windows", "shadow_man#médio-dir", "hotel_register|An open old hotel register on a reception counter, the stub of a torn-out page visible, " + ILEG],
 # N049 El Registro. Portsmouth, abril 1956, Ordzhonikidze con Jruschov y Bulganin; Eden
 ["cruiser|A large Soviet cruiser anchored in Portsmouth harbour in April 1956, grey sky" + NOINS, f"khrushchev|{KHRU} and a white-bearded man waving from the deck of a warship, 1956@@NIKITA JRUSCHOV", "cruiser#médio-dir", f"eden|{EDEN} in a London office, 1956@@ANTHONY EDEN", "downing_1956|Downing Street in London in 1956, a policeman at the door of number 10" + SEM],
 # N050 19 de abril, Crabb se sumerge; no vuelve
 [f"crabb|{CRABB} on a jetty at dawn, 1956@@LIONEL CRABB", "frogman_dive|A frogman slipping into dark harbour water at dawn beside a wooden jetty, 1956", "hull_underwater|Underwater view of the huge dark hull of a warship in murky green water", "ripples|Calm harbour water surface with fading ripples at dawn, no people"],
 # N051 páginas del registro desaparecen; Almirantado: pruebas de equipo
 ["hotel_register#detalhe-centro", "sally_port|A small old seaside hotel in Portsmouth in 1956, white facade", "torn_page|A hand tearing pages out of an old hotel register, " + ILEG, "admiralty|The Admiralty building in London in 1956, grey day"],
 # N052 Moscú protesta; Eden sin autorización; documentos 2006
 ["kremlin_1956|The Kremlin walls and towers in Moscow in spring 1956", "eden#detalhe-centro", "archives_2006|A modern national archives reading room in 2006 with file boxes on trolleys", "archive_boxes#detalhe-centro"],
 # N053 alguien arranca páginas; 25 años después, el papel que fracasa
 ["torn_page#médio-dir", "hotel_register#aberto", "south_atlantic|A grey South Atlantic sea with rocky islands on the horizon under low clouds"],
 # N054 El Misil. Londres, julio 1981, Comité Conjunto de Inteligencia
 ["jic_room|British officials around a long conference table in a Whitehall room in 1981, papers and ashtrays", "jic_paper|A typed assessment page on a desk with a plain red band across the top, " + ILEG, "jic_room#detalhe-centro", "map_south|" + MAPA + ", showing the southern tip of South America and the islands in the South Atlantic to the east", f"thatcher|{THATCH} at a desk reading papers, 1981@@MARGARET THATCHER"],
 # N055 2/4/1982 desembarco; informe Franks
 ["landing_1982|Small landing craft approaching a rocky shore at dawn in 1982, seen from far away, no fighting" + NOARM, "stanley_1982|A small town of houses with coloured roofs on a windswept harbour in 1982, grey sky", "franks_report|A thick bound report lying on a desk in 1983" + SEM, "thatcher#médio-dir"],
 # N056 Exocet; Freedman: agentes como compradores
 ["exocet|A French anti-ship missile resting on a transport cradle in a hangar, no markings", "jet_airfield|A Super Étendard jet on an airfield seen from far away, 1982, no markings", "arms_office|Men in suits shaking hands in a dimly lit arms dealer's office in 1982", "fake_buyer|A man in a suit with a briefcase waiting in a hotel lobby in 1982", "fake_buyer#detalhe-baixo", "freedman|A British historian of about fifty-six writing at a desk surrounded by files, 2005@@LAWRENCE FREEDMAN"],
 # N057 no los consiguió; 74 días; más de 900 muertos
 ["empty_crate|An empty missile crate in a warehouse, its lid open" + SEM, "ships_far|Grey warships on a rough sea seen from very far away, 1982, no smoke", "crosses_hill|A windswept hill with rows of simple white crosses under a grey sky, seen from far away, no names"],
 # N058 identidades falsas; 20 años después, dossier del gobierno con informes del MI6
 ["fake_buyer#detalhe-centro", "dossier_2002|A government dossier with a plain cover on a desk in 2002" + SEM, "downing_2002|Downing Street in London at night in 2002, lit windows" + SEM, "commons_2003|The House of Commons chamber in 2003, full benches"],
 # N059 El Informe. 6/7/2016, Chilcot, siete años
 [f"chilcot|{CHILC} speaking at a lectern in a conference hall, 2016@@JOHN CHILCOT", "report_volumes|A row of twelve thick bound report volumes on a table" + SEM, "chilcot#médio-dir", "iraq_road|A desert road in Iraq in 2003 with a military convoy seen from very far away" + NOARM, "westminster_2016|The Palace of Westminster in London in summer 2016"],
 # N060 certeza injustificada; fuentes poco comprobadas; informes retirados
 ["empty_bunker|An empty concrete bunker in the desert with its doors open, sunlight inside", "sis_report|A typed intelligence report with a red stripe across the top on a desk, " + ILEG, "draft_speech#médio-esq", "inspectors|Weapons inspectors in white protective suits looking into an empty warehouse, seen from far away"],
 # N061 Las armas nunca aparecieron.
 ["empty_bunker#detalhe-centro"],
 # N062 como en 1917 y 1941, un papel pesó en una decisión de guerra; esta vez el propio país
 ["room40#detalhe-centro", "secret_map#médio-esq", "dossier_2002#detalhe-centro", "commons_2003#médio-esq"],
 # N063 El Mapa. Hoy: web, empleo; reconocido en 1992; 2025 una mujer
 ["laptop_site|A laptop on a modern office desk showing a plain website layout with no readable text", "laptop_site#detalhe-centro", "thames_dusk|The River Thames in London today at dusk, city lights", "commons_1992|The House of Commons chamber in 1992 during a session", "woman_chief|A woman of about forty-eight in a dark suit walking down a modern corridor in 2025, face partly in shadow"],
 # N064 del mapa no hay rastro en archivos alemanes; inteligencia británica en NY; laboratorio en Toronto
 ["secret_map#aberto", "captured_archives#detalhe-centro", "rockefeller_1941#detalhe-alto", "casa_loma#detalhe-centro"],
 # N065 más de un siglo; papeles: escribió, filtró, hizo desaparecer
 ["diary_open#detalhe-centro", "letter_typed#médio-dir", "hotel_register#detalhe-baixo", "draft_speech#detalhe-centro", "case_file#médio-esq"],
 # N066 Un espía roba documentos… a escribirlos
 ["typewriter_dark#detalhe-alto", "blank_page#médio-dir"],
 # N067 Y tú, ¿crees…?
 ["typewriter_end|A typewriter on a dark desk beside an old map of South America with coloured zones, a desk lamp switching off" + SEM, "folder_close|A hand closing a thick brown case file with a red circular stamp on a dark desk, lamp light" + SEM, "secret_map#detalhe-alto"],
]
_textos = [x for x in B if "t" in x]
assert len(SB) == len(_textos), f"SB {len(SB)} x blocos {len(_textos)}"
for _blk, _s in zip(_textos, SB): _blk["s"] = _s

# Thumbs (EMBALAGEM.md aprovado no crivo r3): texto (NUEVA YORK, ¿SABÍA?, 14 → 5, aba) no Thumbnail.jsx.
THUMBS = [
    {"id": "thumb-A", "prompt": "Ink graphic novel illustration: a 1940s black typewriter alone on a dark wooden desk, seen three-quarters from above, a single completely blank white sheet of paper in the roller, a strong cone of warm desk-lamp light from the upper left making a bright rim of light on the metal keys and carriage, the white sheet is the brightest area of the image, the typewriter occupies the LEFT 55 percent of the frame, deep slate-blue darkness around, RIGHT third empty dark wall, no brand name, no other objects, no papers, no people, no lettering, no numbers, no hex codes"},
    {"id": "thumb-B", "prompt": "Ink graphic novel illustration: close medium shot of a man resembling Franklin D. Roosevelt in 1941, aged about sixty, pince-nez glasses, dark grey suit, his face large in the LEFT half of the frame taking about half the image height, two small dark 1940s radio microphones without any lettering in the lower foreground, holding in his left hand at chest height a single cream sheet of speech paper with lines of text drawn only as faint illegible strokes and one whole line struck through with a clean thick red ink stroke that does not drip, grave confident expression with eyes glancing sideways at the sheet, hotel banquet hall with heavy slate-blue curtains and blurred chandeliers, warm stage light from above, RIGHT third plain dark curtain, no map, no typewriter, no flags, no insignia, no readable letters anywhere, no hex codes"},
    {"id": "thumb-C", "prompt": "Ink graphic novel illustration: an old travel-stained paper map of South America and Central America down from Panama lying flat on a dark wooden desk under lamp light, filling the LEFT two thirds of the frame, the continent divided into five large flat zones of muted ink colors that alternate light and dark between neighbours (pale ochre next to dark slate blue, light sepia next to olive, grey), thick dark borders that ignore the real countries, a fountain pen nib entering from the right finishing one border line in deep red ink, correct coastline of South America and the isthmus of Panama, no other land masses, RIGHT third dark empty desk, no labels, no text, no letters, no numbers, no symbols, no flags, no insignia, no arrows, no hex codes"},
]
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
