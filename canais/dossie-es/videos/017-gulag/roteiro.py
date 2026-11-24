#!/usr/bin/env python3
"""Fonte única do dossie-es 017 (El Gulag): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py (na pasta do vídeo). Geração copiada do 015-gru.

Embalagem aprovada no crivo r3 (23/11/2026, EMBALAGEM.md/CRIVO.md):
  A/T1 "GULAG: la empresa de Stalin que necesitaba presos" + lingote em trapézio com estrela dentro de marmita de lata vazia, GULAG + sello ¿RENTABLE? (objeto-simbolo, controle)
  B/T2 "Cómo funcionaba el Gulag por dentro: plan, oro y mano de obra presa" + tabela de normas com 3 pães decrescentes e carimbo de estrela, NORMA (documento-evidencia)
  C/T3 "Republicanos y Franquistas, Presos en el Mismo Gulag | Expedientes de Stalin" + homem de telogreika e ushanka desce do navio em Barcelona, BARCELONA (cena-acao)
Ângulo (ANGULO.md): el Gulag como empresa (papeles: decreto, libro, oro, norma, memorándum, orden) y los hispanohablantes que se tragó
(marineros, pilotos, divisionarios, el mexicano Vadillo) hasta el Semíramis (1954) y Solzhenitsyn en TVE (1976).

Sintaxe dos planos (campo s): "chave|prompt" nova · "chave" reuso · "chave#enq" reuso com enquadramento · + "@@TEXTO" rótulo.
"""
import json, math, re
from pathlib import Path

WPS = 2.38           # palavras/s medidas no 001–015 (erro de 1–3%)
BREAK, LONG = 0.35, 0.8
MAX_PLANO_INICIO = 3.0   # s por plano nos primeiros INICIO s (~20 cortes/min)
INICIO = 60.0
MAX_PLANO = 3.6      # s por plano depois (~17 cortes/min)
INEDITO_ATE = 180.0  # s: só imagens novas até aqui
JANELA = 60.0        # s: mesmo enquadramento da mesma imagem só depois disso
HOOK_MAX = 40.0      # s: bíblia 25–35 s + frase-ponte pedida pela EMBALAGEM
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "GULAG: la empresa de Stalin que necesitaba presos"
TITULOS = ("T1 GULAG: la empresa de Stalin que necesitaba presos / "
           "T2 Cómo funcionaba el Gulag por dentro: plan, oro y mano de obra presa / "
           "T3 Republicanos y Franquistas, Presos en el Mismo Gulag | Expedientes de Stalin")
PROMESSA = ("El Gulag por dentro como una empresa del Estado soviético que funcionaba con presos (decreto para colonizar y explotar, "
            "oro en toneladas, la norma y los informes inflados, hasta su cierre 'por ineficiencia'), y los españoles de los dos bandos "
            "de la guerra civil que acabaron en sus campos, hasta el barco que los trajo a Barcelona en 1954.")

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Barcelona, dos de abril de mil novecientos cincuenta y cuatro. Un barco griego entra en el puerto.", card="BARCELONA, 1954")
b("A bordo vienen doscientos ochenta y seis españoles. No vuelven de una guerra. Vuelven de los campos de trabajo soviéticos.")
b("Unos habían luchado por Franco. Otros, contra él. Y durante años compartieron los mismos campos.")
b("Esta es TODA la historia del Gulag: la empresa de Stalin que necesitaba presos. Y la de los españoles que acabaron trabajando para ella. Para entender cómo llegaron ahí, hay que abrir sus papeles.", ideia=True)

# ───────────────────────── 1. EL DECRETO ─────────────────────────
cap("1. El Decreto")
b("El Decreto. Moscú, once de julio de mil novecientos veintinueve. Un decreto secreto del gobierno soviético fija una tarea para los presos con penas largas.", card="MOSCÚ, 1929")
b("No basta con encerrarlos. Irán a regiones remotas, casi vacías, para colonizarlas y explotar sus recursos naturales: madera, carbón, metales.")
b("El plan es modesto. Campos pequeños, cincuenta mil plazas para todo el país. Es la primera cifra de la empresa. Y se queda corta desde el primer invierno.")
b("Al año siguiente, la administración que dirige esos campos recibe su nombre definitivo. Por sus siglas en ruso: Gulag, Dirección General de Campos.")
b("Los historiadores discuten si se arrestaba para llenar los campos. Lo que dicen los papeles es que el plan contaba a los presos como mano de obra. Y su primera gran obra tuvo hasta un libro.", ideia=True)

# ───────────────────────── 2. EL LIBRO ─────────────────────────
cap("2. El Libro")
b("El Libro. Moscú, primavera de mil novecientos treinta y siete. Semión Firin, antiguo subjefe del Gulag, es arrestado. En agosto lo fusilan.", card="MOSCÚ, 1937")
b("Firin había editado, junto a Máximo Gorki y Leopold Averbaj, la historia oficial del canal del mar Blanco, escrita por treinta y seis autores soviéticos. Según el diario ruso Nóvaya Gazeta, tras su caída se retira la tirada.")
b("Para escribirlo, en agosto de mil novecientos treinta y tres, una brigada de unos ciento veinte escritores había recorrido la obra recién inaugurada. El libro la presenta como una escuela: los presos se reforjan trabajando.")
b("Lo que el libro no cuenta está en los registros del propio Gulag: unos doce mil presos fallecidos en la obra. Algunas estimaciones de historiadores duplican esa cifra.")
b("La empresa había aprendido algo: las obras también se enseñan. Once años después, invitaría a otro visitante a ver sus minas. Esta vez, desde Washington.", ideia=True)

# ───────────────────────── 3. EL ORO ─────────────────────────
cap("3. El Oro")
b("El Oro. Magadán, mayo de mil novecientos cuarenta y cuatro. Henry Wallace, vicepresidente de Estados Unidos, aterriza en Kolimá, en el extremo noreste soviético.", card="MAGADÁN, 1944")
b("Lo recibe Iván Nikíshov, jefe de Dalstrói, la empresa del Gulag que saca oro de la región. Le enseña escuelas, granjas y minas.")
b("Según presos que lo vivieron, las torres de vigilancia desaparecen esos días y los reclusos quedan encerrados. Años después, Wallace admitió que lo había impresionado demasiado el espectáculo.")
b("Detrás del espectáculo estaban las cifras. Entre mil novecientos veintiocho y mil novecientos treinta y tres, la región había dado menos de dos toneladas de oro. En mil novecientos treinta y siete, Dalstrói entrega cincuenta y una toneladas y media. A comienzos de mil novecientos cuarenta trabajan allí más de ciento noventa mil presos.")
b("En Moscú, los informes se medían en toneladas. Pero había una pregunta que ningún informe respondía: ¿era rentable? Dentro de los campos, la respuesta empezaba en una tabla.", ideia=True)

# ───────────────────────── 4. LA NORMA ─────────────────────────
cap("4. La Norma")
b("La Norma. Moscú, trece de marzo de mil novecientos cincuenta. El gobierno soviético decide pagar un salario a los presos de los campos.", card="MOSCÚ, 1950")
b("Hasta entonces, la paga era la comida. Según Applebaum, la escala nació en Solovkí en los años veinte: en trabajo pesado, quien cumplía la norma podía recibir ochocientos gramos de pan. A los inválidos, la mitad. Y para cumplirla en el papel, presos y jefes inflaban los informes: lo llamaban tufta.")
b("Había existido otro incentivo: días de condena descontados por buen trabajo. Según el historiador Oleg Jlevniuk, Beria los suprimió en mil novecientos treinta y nueve.")
b("A comienzos de los años cincuenta, más de la cuarta parte de los presos que trabajaban a destajo no alcanzaba la norma. Los propios dirigentes ya preferían trabajadores libres, que rendían más y no necesitaban guardias. El salario fue un último intento.")
b("En total, según el directorio de la organización rusa Memorial que cita Applebaum, hubo al menos cuatrocientos setenta y seis complejos de campos. En algunos acabaron españoles que habían llegado como aliados.", ideia=True)

# ───────────────────────── 5. LOS MARINEROS ─────────────────────────
cap("5. Los Marineros")
b("Los Marineros. Odesa, primavera de mil novecientos treinta y nueve. La guerra civil española acaba de terminar. En la Unión Soviética siguen las tripulaciones de tres mercantes de la República. Se llaman Cabo San Agustín, Juan Sebastián Elcano e Inocencio Figaredo. Años después, algunos compartirán campo con sus enemigos de la guerra.", card="ODESA, 1939")
b("Habían traído suministros para la República. Son doscientos cincuenta hombres sin un país al que volver. Ese verano, unos ciento treinta marineros de los barcos retenidos salen por Estambul. Los demás se quedan.")
b("Piden irse a México, a Francia, adonde sea. Según la historiadora Luiza Iordache, para Moscú un extranjero que quería marcharse era un sospechoso.")
b("A finales de junio de mil novecientos cuarenta y uno, días después de la invasión alemana, Lavrenti Beria ordena internar en Norilsk a los marineros y pilotos españoles que pedían salir. Ninguno fue juzgado.")
b("Norilsk, por encima del círculo polar, era una mina de níquel del Gulag. Allí la empresa los pone a trabajar. Según Iordache, más de veinte republicanos españoles fallecen en los campos antes de mil novecientos cincuenta y cuatro.", ideia=True)
b("Si te interesan estos expedientes, suscríbete. Porque con los marineros cayeron también los alumnos de una escuela de pilotos.")

# ───────────────────────── 6. LOS PILOTOS ─────────────────────────
cap("6. Los Pilotos")
b("Los Pilotos. Kirovabad, Azerbaiyán soviético, enero de mil novecientos treinta y nueve. Llega la última expedición de jóvenes españoles a una escuela de aviación militar.", card="KIROVABAD, 1939")
b("Entre todas las promociones son unos ciento cincuenta o doscientos alumnos. Vinieron a aprender a volar para la República. Cuando terminan, la República ya no existe.")
b("Los intentos de enviarlos a México fracasan. Moscú les ofrece trabajo en fábricas. Unos aceptan; otros piden marcharse.")
b("En enero de mil novecientos cuarenta detienen a ocho: ocho años por actividades antisoviéticas. Según Iordache, solo cuatro sobrevivieron. En junio de mil novecientos cuarenta y uno, al capitán Federico Gonzalo lo condenan a quince años por negarse a suscribir el empréstito del Estado.")
b("Mientras tanto, la guerra vaciaba los campos. En mil novecientos cuarenta y dos, según los certificados del propio Gulag, fallecen más de trescientos cincuenta mil presos. Y en mil novecientos cuarenta y tres llegaron españoles del otro bando.", ideia=True)

# ───────────────────────── 7. EL NÚMERO ─────────────────────────
cap("7. El Número")
b("El Número. Krasni Bor, cerca de Leningrado, diez de febrero de mil novecientos cuarenta y tres. La División Azul, los voluntarios que Franco envió a luchar junto a Alemania, recibe una gran ofensiva soviética. A sus soldados los llaman divisionarios.", card="KRASNI BOR, 1943")
b("Entre los capturados está Constante Vicente Giráldez. Según su hija, pierde la vista de un ojo. En sus papeles militares figura un número: doce mil ciento veintitrés.")
b("Según los historiadores, los divisionarios capturados van de unos trescientos setenta a casi quinientos. Llegan como prisioneros de guerra. A muchos los condenan y los envían a campos de trabajo.")
b("Según Iordache, a finales de los años cuarenta, republicanos y divisionarios conviven en los mismos campos. Uno de ellos fue Karagandá, en Kazajistán. Allí, según su hija, Constante Vicente acaba haciendo pan para los oficiales del campo.")
b("Hombres de los dos bandos de la guerra civil comparten ahora campo. Pero no todos los presos que hablaban español eran españoles. Uno era mexicano.", ideia=True)

# ───────────────────────── 8. LA EMBAJADA ─────────────────────────
cap("8. La Embajada")
b("La Embajada. Moscú, diecinueve de junio de mil novecientos cuarenta y siete. Un hombre vestido de campesino se presenta en la embajada de México y pide asilo.", card="MOSCÚ, 1947")
b("Es Evelio Vadillo, comunista de Ciudad del Carmen, en Campeche. Su partido lo había enviado a Moscú en mil novecientos treinta y cinco. Un año después lo detienen: cinco años de campo y cinco de destierro en Kazajistán.")
b("El embajador Luciano Joublanc Rivas lo recibe. Pero Moscú no deja salir a Vadillo. En mil novecientos cincuenta vuelve a prisión: veinte años, acusado de espiar para México.")
b("Lo liberan en mil novecientos cincuenta y cinco. El dieciséis de octubre, por fin, vuelve a México. Un libro reciente cuenta su caso con un título exacto: Veinte años en el Gulag.")
b("Vadillo sale dos años después de un cambio que lo movió todo en Moscú: la muerte de Stalin.", ideia=True)

# ───────────────────────── 9. EL MEMORÁNDUM ─────────────────────────
cap("9. Las Obras")
b("Las Obras. Moscú, doce de marzo de mil novecientos cincuenta y tres. Una semana después de la muerte de Stalin, Lavrenti Beria cancela más de veinte grandes obras del Gulag.", card="MOSCÚ, 1953")
b("Canales, presas, un ferrocarril por la tundra ártica entre Salejard e Ígarka. Ese mes, Beria informa a la dirección del partido de cuántos presos hay: más de dos millones y medio.")
b("El veintisiete de marzo, una amnistía libera a cerca de un millón, casi todos por delitos comunes. En junio, según Applebaum, Beria dice querer liquidar el trabajo forzado por su ineficiencia económica.")
b("Esa fue la respuesta del propio régimen a la pregunta del oro: la empresa no era rentable. Pero los españoles seguían dentro. Un año después, un barco fue a buscarlos.", ideia=True)

# ───────────────────────── 10. EL BARCO ─────────────────────────
cap("10. El Barco")
b("El Barco. Odesa, comienzos de mil novecientos cincuenta y cuatro. España y la Unión Soviética no tienen relaciones. La Cruz Roja francesa fleta un barco griego: el Semíramis.", card="ODESA, 1954")
b("Suben doscientos ochenta y seis españoles: más de doscientos divisionarios y unos treinta marineros y pilotos republicanos. También cuatro antiguos niños de la guerra.")
b("Durante la travesía, sus llamadas por radio a las familias se oyen en toda España. El dos de abril, a las cinco y treinta y cinco de la tarde, atracan en Barcelona.")
b("Según la revista Time, una multitud sube a bordo y algunas mujeres se desmayan. Cada uno había pasado entre diez y dieciséis años en campos soviéticos.")
b("En el puerto los recibe el general Muñoz Grandes, antiguo jefe de la División Azul. Según Time, en los campos quedaban todavía unos doscientos españoles. Y el Gulag aún no tenía el libro que lo haría famoso.", ideia=True)

# ───────────────────────── 11. LA ENTREVISTA ─────────────────────────
cap("11. La Entrevista")
b("La Entrevista. Madrid, marzo de mil novecientos setenta y seis. Franco ha muerto hace cuatro meses. En el programa Directísimo, de Televisión Española, José María Íñigo entrevista a un escritor ruso expulsado de su país: Alexandr Solzhenitsyn.", card="MADRID, 1976")
b("Su Archipiélago Gulag había salido en París en mil novecientos setenta y tres, y en español al año siguiente. En México, Octavio Paz lo defendió en la revista Plural.")
b("Para entonces, el Gulag ya no existía con ese nombre: una orden de enero de mil novecientos sesenta lo había disuelto.")
b("En el estudio, Solzhenitsyn les dice a los españoles, textualmente: «Vosotros no sabéis qué es el comunismo». Parte de la prensa de izquierda lo ataca. El novelista Juan Marsé lo llama «chorizo de las letras»: ladrón de las letras.")
b("De los españoles que volvieron en mil novecientos cincuenta y cuatro quedaba otra prueba, más callada: unas fotos.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. Las Fotos")
b("Las Fotos. Barcelona, dos de abril de mil novecientos cincuenta y cuatro. En el muelle, entre la multitud, el fotógrafo Carlos Pérez de Rozas retrata a los que bajan del Semíramis.", card="BARCELONA, 1954")
b("Hoy esas fotos están en el Archivo Fotográfico de Barcelona. Muestran a los que volvieron, hombres de los dos bandos, bajando del mismo barco.")
b("Siete décadas después, en dos mil veinticinco, un libro reconstruye el destino de los marineros republicanos en los campos soviéticos.")
b("Los historiadores discuten si el Gulag buscaba culpables o brazos. Sus papeles contaban brazos. Y los encontró en todas partes: entre sus enemigos, entre sus aliados y entre los que solo querían volver a casa.", ideia=True)
b("Y tú, ¿sabías que hubo españoles en el Gulag? ¿Conoces alguna historia así en tu familia? Déjalo en los comentarios.")

# ───────────────────────── STORYBOARD (planos por bloco, na ordem dos blocos) ─────────────────────────
SEM = ", no lettering anywhere, every sign blank"
NOINS = ", no flags, no insignia, no badges, no emblems, no armbands, no medals"
NOFLAG = ", no flags"
FAR = ", seen from far away, no bodies, no blood"
ILEG = "the writing only as faint completely illegible blurred lines, no readable letters"
BLANK = "completely blank sheets of paper, no writing at all"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, rivers and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame, no ocean names"
PRESOS = "prisoners in grey quilted padded jackets and caps with ear flaps, faces ordinary and tired, adults of different ages"
GUARD = "a guard in a long plain greatcoat without any insignia, bareheaded or in a plain fur hat"
# Personagens ("resembling", nunca foto; roupa civil sem insígnias; adultos realistas)
FIRIN = "a Soviet official of about forty in 1937 resembling Semyon Firin, round face, short dark hair, plain dark tunic without insignia"
GORKI = "an elderly Russian writer of the early 1930s resembling Maxim Gorky, tall and thin, bushy moustache, short grey hair, dark suit"
WALLACE = "an American politician of about fifty-five in 1944 resembling Henry A. Wallace, lean face, wavy greying hair, light raincoat over a suit"
NIKI = "a stocky Soviet official of about forty-five in 1944 resembling Ivan Nikishov, heavy face, short hair, plain dark tunic without insignia, bareheaded"
BERIA = "a Soviet official of about fifty-four in 1953 resembling Lavrentiy Beria, bald head, round pince-nez glasses, dark civilian suit and tie"
VADI35 = "a Mexican man of about thirty-one in 1935 resembling Evelio Vadillo, dark wavy hair, thin moustache, dark suit and tie"
VADI47 = "a gaunt Mexican man of about forty-three in 1947, dark hair turning grey, worn padded peasant jacket and cloth cap"
JOUB = "a Mexican diplomat of about fifty in 1947 resembling Luciano Joublanc Rivas, receding hair, round glasses, grey three-piece suit"
GIRAL = "a young Spanish soldier of about twenty-two in 1943, dark hair, bandaged head over one eye, plain winter coat without insignia, bareheaded"
GIRAL48 = "a Spanish man of about twenty-seven in 1948, dark hair, one eye half closed, grey quilted padded jacket, white baker's apron"
MUNOZ = "a Spanish general of about fifty-eight in 1954 resembling Agustín Muñoz Grandes, thin face, small moustache, dark civilian overcoat and hat, no insignia"
SOLZH = "a Russian writer of about fifty-seven in 1976 resembling Aleksandr Solzhenitsyn, long beard without moustache trimmed, high forehead, dark suit"
INIGO = "a Spanish television host of about thirty-four in 1976 resembling José María Íñigo, thick curly hair and a thick dark moustache, wide-collar shirt and jacket"
PAZ = "a Mexican poet of about sixty in 1974 resembling Octavio Paz, wavy grey hair, dark eyes, tweed jacket"
MARSE = "a Spanish novelist of about forty-three in 1976 resembling Juan Marsé, curly dark hair, sharp face, open-collar shirt"
ROZAS = "a Spanish press photographer of about sixty in 1954, hat and raincoat, holding a large 1950s press camera with a flash bulb"
PILOTO = "a young Spanish man of about twenty in 1939 in a plain leather flying jacket and cap without insignia"
MARINO = "a Spanish merchant sailor of about thirty in 1939, dark wool sweater and cap without any badge"

SB = [
 # N001 Barcelona 1954: un barco griego entra en el puerto
 ["bcn_port_1954|Barcelona harbour in 1954 on a bright spring afternoon, a dark-hulled steamer entering the port, the Columbus monument column in the distance, cranes and warehouses" + SEM + NOFLAG + "@@BARCELONA, 1954",
  "ship_bow|Close view of the bow of a 1950s dark-hulled passenger steamer cutting through calm harbour water, gulls" + SEM + NOFLAG,
  "quay_crowd_wait|A crowd of Spanish men and women in 1950s coats waiting on a stone quay, some on tiptoe, looking toward an approaching ship" + SEM + NOFLAG],
 # N002 286 españoles; vuelven de los campos de trabajo soviéticos
 ["deck_men|Men in worn grey quilted padded jackets and fur caps with ear flaps crowding the deck rail of a steamer, looking at a sunny port" + SEM + NOFLAG,
  "camp_snow_far|A Soviet labour camp in deep snow seen from far away, wooden barracks, a plain fence and a watchtower under a grey sky" + FAR + SEM,
  "padded_jacket|Close view of a worn grey quilted padded labour-camp jacket hanging on a nail in a wooden barrack, a plain white number patch sewn on the chest, " + ILEG],
 # N003 unos por Franco, otros contra él; los mismos campos
 ["two_men_rail|Two Spanish men of about forty in grey padded jackets standing side by side at a ship's rail, not looking at each other, sunny harbour behind" + SEM + NOFLAG,
  "barrack_bunks|Interior of a crowded wooden labour-camp barrack with double bunks, men sitting on the bunks in padded jackets, dim light from a small window" + SEM,
  "two_caps_bench|Two different worn caps lying side by side on a rough wooden bench in a barrack, one military field cap without badge and one civilian cloth cap" + SEM],
 # N004 frase-ancla: TODA la historia del Gulag; la empresa; papeles
 ["dossier_desk|A brown cardboard dossier on a dark desk under a green lamp, a red rubber stamp beside it" + SEM,
  "ussr_map|" + MAPA + ", showing the whole Soviet Union from the Baltic to the Pacific, Europe on the left",  # o código desenha pontos de campos e pinos em Moscú, Kolimá, Norilsk, Karagandá
  "gold_bowl|A dented tin prisoner bowl on a frosted plank, empty of food, with a single trapezoid gold bar lying inside it, an aluminium spoon beside it, dark background",
  "ledger_rows|Top-down view of an old ledger book open on a desk with long columns of numbers, " + ILEG + ", an abacus with wooden beads beside it",
  "papers_stack|A tall stack of old typed documents tied with string on an archive shelf, a single desk lamp, " + ILEG],
 # N005 Moscú 11/07/1929: decreto secreto
 ["moscow_1929|A Moscow street in summer 1929 with old stone buildings, a tram, horse carts and people in caps and light coats, the Kremlin towers in the distance" + SEM + NOFLAG + "@@MOSCÚ, 1929",
  "decree_desk|A typed government decree on a desk in a 1929 Soviet office, a round red rubber stamp mark at the bottom, " + ILEG,
  "officials_table|Four Soviet officials in plain dark tunics without insignia around a long table covered with green cloth in a high-ceilinged office, papers in front of them" + NOINS + SEM,
  "pen_sign|Close view of a hand signing a typed document with a dip pen, an inkwell beside it, " + ILEG],
 # N006 regiones remotas: colonizar y explotar madera, carbón, metales
 ["taiga_empty|An endless empty taiga landscape with a frozen river and no people, low grey sky, seen from a hill" + SEM,
  "timber_logs|A huge pile of felled pine logs on a frozen river bank in the north, axes stuck in a stump, nobody around" + SEM,
  "coal_hill|A coal mine pithead and black spoil heap in a snowy treeless northern landscape in the 1930s, seen from far away" + SEM],
 # N007 cincuenta mil plazas; se queda corta
 ["small_camp|A small new labour camp of a few wooden barracks inside a plain fence in a forest clearing in 1929, smoke from one chimney" + SEM,
  "plan_number|Top-down view of a typed planning sheet with a single short column of numbers and a red pencil lying on it, " + ILEG,
  "train_wagons|A long freight train of closed wooden wagons standing at a snowy siding in the north, guards walking along it" + FAR + SEM + NOINS,
  "crowded_yard|A labour camp yard in winter crowded with many prisoners in padded jackets lined up in rows, seen from far away" + FAR + SEM],
 # N008 nombre definitivo: Gulag, Dirección General de Campos
 ["gulag_office|The facade of a grey stone Soviet government building in Moscow in 1930, tall windows, a plain closed door, a black car parked" + SEM + NOFLAG,
  "nameplate_blank|A plain blank brass plate beside a heavy wooden office door in a Soviet ministry corridor, completely blank plate, no lettering",
  "card_files|Rows of wooden card-index drawers in a long Soviet archive room, one drawer pulled open, index cards with " + ILEG],
 # N009 historiadores discuten; el plan contaba presos como mano de obra; un libro
 ["historians_books|A long wooden library table with thick history books and folders open, reading lamps, an empty chair" + SEM,
  "workers_column|A column of prisoners in padded jackets marching to work at dawn through snow, guards with dogs at the sides" + FAR + SEM + NOINS,
  "worksite_plan|A Soviet engineer's drawing board with a large plan of a canal lock, rulers and pencils, " + ILEG,
  "canal_dig|Hundreds of prisoners digging a huge canal trench through granite and forest in 1932, wooden scaffolds and wheelbarrows, seen from far away" + FAR + SEM,
  "book_closed|A thick heavy book with a plain dark cloth cover lying closed on a desk, no title, no lettering, a desk lamp"],
 # N010 Moscú 1937: Firin arrestado; fusilado en agosto
 ["moscow_1937_night|A Moscow street at night in spring 1937, a black car stopped in front of an apartment building, one lit window" + SEM + NOFLAG + "@@MOSCÚ, 1937",
  f"firin_portrait|{FIRIN}, standing in an office with a tired, worried face, papers on the desk behind him" + NOINS + "@@SEMIÓN FIRIN",
  "corridor_men|Two men in long dark coats walking down a dim corridor of a Soviet office building toward a door at night, seen from behind" + NOINS + SEM],
 # N011 libro editado con Gorki y Averbaj; 36 autores; se retira la tirada
 [f"gorki_desk|{GORKI} sitting at a writing desk covered with manuscript pages, reading glasses in hand" + "@@MÁXIMO GORKI",
  "book_open|A thick 1934 Soviet book lying open, one page with a large idealised drawing of a canal lock with a steamer, the other page " + ILEG,
  "manuscripts_pile|A pile of typed manuscript chapters from many authors on a big editorial table, pencils and paper clips, " + ILEG,
  "books_boxes|Stacks of identical thick books being packed into wooden crates in a dim warehouse by two workers" + SEM,
  "library_empty_shelf|A library shelf with a visible gap where several books have been removed, dust outline on the shelf" + SEM],
 # N012 brigada de 120 escritores recorre la obra; "reforjarse trabajando"
 ["writers_steamer|A small white steamer full of writers in light summer suits and hats on deck, sailing through a new canal lock in August 1933, forest banks" + SEM + NOFLAG,
  "writers_notes|Two writers in summer suits on a steamer deck taking notes in notebooks, looking at the canal banks" + SEM,
  "canal_lock|A newly built wooden canal lock gate with water flowing, granite walls, northern forest around, summer 1933" + SEM,
  "poster_worker|A heroic painted poster style scene of a smiling prisoner holding a shovel in front of a canal, sunrise behind him, no lettering",
  "brigade_lineup|A brigade of prisoners standing in a line on a canal bank while an official speaks to them, summer, seen from far away" + FAR + SEM + NOINS],
 # N013 lo que el libro no cuenta: unos doce mil fallecidos; estimaciones duplican
 ["registry_book|A thick registry book open on a camp office desk, long handwritten columns, " + ILEG + ", an oil lamp",
  "canal_birches|A quiet stretch of the White Sea canal today, still dark water, birch trees and grey granite banks, no people" + SEM,
  "wooden_posts|A clearing in a northern pine forest with rows of small plain wooden posts half hidden in moss, misty morning" + SEM,
  "numbers_red|Close view of a typed table with a column of numbers and one row underlined in red pencil, " + ILEG],
 # N014 las obras también se enseñan; otro visitante, desde Washington
 ["guided_tour|An official in a plain dark coat pointing out a new canal to a group of visitors in hats on a wooden platform, 1933" + SEM + NOINS,
  "washington_1944|The United States Capitol dome in Washington in 1944 seen across a wide avenue, 1940s cars" + SEM + NOFLAG,
  "plane_1944|A 1940s twin-engine propeller transport plane flying over snowy mountains and a frozen coast, plain bare metal without any marking"],
 # N015 Magadán, mayo 1944: Henry Wallace aterriza en Kolimá
 ["magadan_1944|The port town of Magadan in spring 1944, wooden houses and a few stone buildings on a grey bay, snow patches on the hills" + SEM + NOFLAG + "@@MAGADÁN, 1944",
  f"wallace_plane|{WALLACE} stepping down from a propeller plane on a muddy airfield, officials in dark coats waiting" + NOINS + SEM + "@@HENRY WALLACE",
  "kolyma_map|" + MAPA + ", showing the far north-east of the Soviet Union, the Sea of Okhotsk and the Kolyma river basin"],  # o código desenha o pino em Magadán
 # N016 Nikíshov, jefe de Dalstrói; escuelas, granjas y minas
 [f"nikishov_wallace|{NIKI} shaking hands with {WALLACE} in front of a wooden administration building" + NOINS + SEM + "@@IVÁN NIKÍSHOV",
  "show_school|A tidy wooden schoolroom with children at desks and a smiling teacher, flowers on the windowsill, 1944" + SEM,
  "show_greenhouse|A large greenhouse in a cold northern town with neat rows of tomato plants, two women workers in clean aprons" + SEM,
  "gold_mine_open|An open-cast gold mine in Kolyma in 1944, terraced pits, sluices and wooden ore carts, workers small in the distance" + FAR + SEM],
 # N017 torres desaparecen, reclusos encerrados; el espectáculo
 ["tower_removed|A wooden watchtower being taken down by two workmen with ropes beside a fence, dusk" + SEM,
  "locked_barrack|The closed door of a wooden barrack secured with a heavy padlock and a wooden bar, faces of prisoners behind a small frosted window" + SEM,
  "stage_curtain|A small provincial theatre stage with a red curtain half open, empty rows of seats, 1940s" + SEM,
  f"wallace_later|{WALLACE} a few years older, sitting alone at a desk with a typewriter, looking out of a window, thoughtful" + SEM],
 # N018 cifras: <2 t (1928–33); 51,5 t (1937); >190 mil presos (1940)
 ["gold_nuggets|Close view of a prospector's pan with a few small gold nuggets on dark wet gravel, cold light",
  "gold_bars_crate|Rows of gold bars stacked in an open wooden crate in a guarded vault, cold neutral light, no markings",
  "kolyma_road|A gravel road winding through bare Kolyma mountains in winter, a truck with a canvas cover, seen from far away" + SEM,
  "steamer_hold|A crowded ship's hold lit by a hanging lamp, prisoners sitting shoulder to shoulder on wooden planks" + SEM,
  "mine_shift|A shift of prisoners in padded jackets walking up from a gold mine pit at dusk, mountains behind" + FAR + SEM],
 # N019 informes en toneladas; ¿era rentable?; una tabla
 ["kremlin_office|A large Kremlin-style office with wood panelling, a long desk with telephones and stacks of reports, empty chair" + SEM + NOFLAG,
  "report_scale|A brass balance scale on an office desk beside a pile of typed reports, " + ILEG,
  "abacus_close|Close view of a wooden Russian abacus with some beads pushed to one side, on a pile of papers",
  "norm_table|Top-down view of a typed Soviet labour-camp ration norm table on yellowed paper, three wide rows of " + ILEG + ", a round red stamp with a five-pointed star in the corner, pieces of dark rye bread of decreasing size on the right column"],
 # N020 Moscú 13/03/1950: salario a los presos
 ["moscow_1950|A Moscow avenue in winter 1950 with large Stalin-era buildings, trolleybuses and people in heavy coats" + SEM + NOFLAG + "@@MOSCÚ, 1950",
  "pay_window|A small wooden cashier's window in a camp office, a clerk counting a few banknotes for a prisoner in a padded jacket" + SEM,
  "coins_table|A few Soviet coins and worn banknotes on a rough wooden table next to a tin mug" + SEM],
 # N021 la paga era la comida; escala de Solovkí; 800 g; inválidos la mitad; tufta
 ["bread_line|Prisoners in padded jackets lining up at a small hatch where a cook hands out bread rations, steam, winter" + SEM,
  "bread_scale|A kitchen scale weighing a dark rye bread ration, a knife beside it" + SEM,
  "solovki_monastery|The Solovetsky monastery walls of white stone on an island in the White Sea, grey sky, 1920s" + SEM,
  "clerk_report|A camp clerk at a desk at night writing numbers into a report while a foreman leans over his shoulder, oil lamp" + SEM + NOINS,
  "report_pile|A thick pile of production reports on a desk with a red pencil tick on the top one, " + ILEG],
 # N022 días de condena descontados; Beria los suprime en 1939
 ["calendar_sheets|A pile of torn-off tear-off calendar sheets on a barrack windowsill, the sheets blank without numbers",
  f"beria_desk|{BERIA} seated at a large desk signing a paper, a green lamp, heavy curtains" + SEM + "@@LAVRENTI BERIA",
  "door_close|A heavy wooden camp gate closing in the snow, a guard pushing it" + SEM + NOINS],
 # N023 >1/4 no alcanza la norma; preferían trabajadores libres
 ["weak_workers|Exhausted prisoners resting on their shovels in a snowy quarry, a foreman with a notebook" + FAR + SEM,
  "foreman_book|Close view of a foreman's notebook with ticks and crosses in rows, " + ILEG + ", a mitten beside it",
  "free_workers|Free workers in their own coats and caps building a railway in the 1950s, no guards, no fence" + SEM],
 # N024 476 complejos (Memorial/Applebaum); españoles llegados como aliados
 ["camps_dots_map|" + MAPA + ", the Soviet Union seen whole, slightly tilted on a dark desk",  # o código desenha muitos pontos vermelhos de campos
  "memorial_archive|A modern archive room with grey boxes on metal shelves and a long table with folders, a researcher's lamp" + SEM,
  "spanish_ship_odessa|A Spanish merchant steamer moored at the port of Odessa in 1939, grand staircase and buildings on the hill behind" + SEM + NOFLAG],
 # N025 Odesa 1939: tripulaciones de tres mercantes republicanos; compartirán campo con sus enemigos
 ["odessa_1939|The port of Odessa in spring 1939, cargo ships at the quays, cranes and the city on the hill" + SEM + NOFLAG + "@@ODESA, 1939",
  "three_ships|Three old merchant steamers moored side by side in a Soviet port, rust streaks on the hulls, no names visible, no flags" + SEM,
  f"sailors_deck|A group of Spanish merchant sailors in dark wool sweaters and caps without badges leaning on the rail of a moored ship, waiting" + SEM + NOFLAG,
  "enemies_hint|Two groups of men in padded jackets in a camp yard in winter, standing apart and glancing at each other" + FAR + SEM],
 # N026 suministros; 250 hombres; ~130 salen por Estambul; los demás se quedan
 ["supplies_unload|Dock workers unloading crates and sacks from a merchant ship in a Black Sea port, 1938" + SEM + NOFLAG,
  "sailors_bunks|Spanish sailors sitting on bunks in a crowded ship's crew quarters, bags packed, waiting" + SEM,
  "istanbul_1939|The Bosphorus in Istanbul in 1939 with mosques and minarets on the skyline, a steamer passing" + SEM + NOFLAG],
 # N027 piden irse a México, a Francia; extranjero que quería marcharse = sospechoso
 [f"letter_request|{MARINO} writing a letter at a small table in a cabin, an envelope ready" + SEM,
  "embassy_queue|Men in worn coats queuing at the closed gate of a foreign embassy in Moscow in winter 1940" + SEM + NOFLAG,
  "officer_file|A Soviet security officer in a plain dark tunic without insignia reading a personal file at a desk, a lamp" + NOINS + SEM],
 # N028 junio 1941: Beria ordena internar en Norilsk; ninguno juzgado
 ["june_1941|A Soviet street in June 1941 with people gathered around a loudspeaker on a pole, worried faces" + SEM + NOFLAG,
  "order_typed|A short typed order on a single sheet with a round red stamp, a signature scrawl at the bottom, " + ILEG,
  "arrest_quay|Two plainclothes men leading a Spanish sailor along a quay toward a black car" + SEM + NOINS,
  "norilsk_map|" + MAPA + ", showing northern Siberia, the Yenisei river and the Taymyr peninsula"],  # o código desenha o pino em Norilsk
 # N029 Norilsk, mina de níquel; la empresa los pone a trabajar; >20 republicanos fallecen
 ["norilsk_mine|The Norilsk nickel mine in the 1940s above the Arctic Circle, smokestacks, wooden headframes and snow, seen from far away" + SEM + "@@NORILSK",
  "polar_night|Prisoners in padded jackets walking in a column under the polar night, lamps on poles, deep snow" + FAR + SEM,
  "ore_cart|A mine ore cart full of grey rock being pushed by two prisoners along rails in a tunnel lit by a lamp" + SEM],
 # N030 CTA: suscríbete; alumnos de una escuela de pilotos
 ["folder_stamp|A brown dossier folder being stamped with a red rubber stamp on a desk" + SEM,
  "biplane_field|Training biplanes lined up on a dusty airfield in the Caucasus in 1938, mountains behind, plain bare metal without any marking"],
 # N031 Kirovabad, enero 1939: última expedición de jóvenes españoles
 ["kirovabad_1939|A Caucasus town in winter 1939 with low houses and poplar trees, snowy mountains behind, a military airfield on the edge" + SEM + NOFLAG + "@@KIROVABAD, 1939",
  "trainees_arrive|Young Spanish men with suitcases climbing down from a train at a small station in the Caucasus, winter" + SEM + NOFLAG,
  f"pilot_cockpit|{PILOTO} sitting in the open cockpit of a training biplane, an instructor beside him on the wing" + NOINS],
 # N032 150–200 alumnos; vinieron a volar para la República; ya no existe
 ["classroom_flight|A classroom with young men in plain jackets at desks, an instructor pointing at a drawing of an airplane wing on a blackboard" + SEM,
  "radio_news|Young men gathered around a 1930s radio set in a dormitory, shocked faces" + SEM],
 # N033 México fracasa; trabajo en fábricas; unos aceptan, otros piden marcharse
 ["factory_floor|A 1940 Soviet factory floor with lathes and workers in overalls, a young Spaniard among them at a machine" + SEM,
  "suitcase_bed|A packed suitcase on a narrow dormitory bed, a coat folded on top" + SEM],
 # N034 enero 1940: ocho detenidos, 8 años; solo 4 sobreviven; Gonzalo, 15 años por el empréstito
 ["butyrka_gate|The massive gate and round towers of an old Moscow prison at night in winter, a black van entering" + SEM,
  "cell_bench|A bare prison cell with a wooden bench and a small barred window high up, four young men sitting in silence" + SEM,
  "kotlas_camp|A labour camp on a frozen river in the Russian north, log barracks and smoke, seen from far away" + FAR + SEM,
  "loan_bond|A Soviet state loan subscription form on a table with a pen beside it, " + ILEG],
 # N035 la guerra vacía los campos; 1942 >350 mil fallecen (certificados)
 ["war_train|A Soviet military train with tanks under tarpaulins passing a snowy station in 1942" + SEM + NOINS,
  "certificate_pile|A pile of small printed certificates on a camp office desk, " + ILEG + ", a pen and an inkwell",
  "empty_bunks|A wooden barrack with many empty bunks, one blanket folded, winter light through a frosted window" + SEM],
 # N036 Krasni Bor, 10/02/1943: la División Azul; ofensiva soviética
 ["krasny_bor|A snowy battlefield near Leningrad in February 1943, shattered birch trees and trenches, smoke on the horizon" + FAR + SEM + "@@KRASNI BOR, 1943",
  "trench_snow|Soldiers in white-grey winter coats crouching in a snowy trench, breath steaming, helmets without any marking" + SEM + NOINS,
  "leningrad_map|" + MAPA + ", showing the region around Leningrad and the Gulf of Finland"],  # o código desenha o pino em Krasni Bor
 # N037 Constante Vicente Giráldez; pierde la vista de un ojo; número 12123
 [f"giral_captured|{GIRAL} sitting in the snow among other captured soldiers, a guard in a greatcoat behind" + NOINS + "@@CONSTANTE VICENTE",
  "military_card|An old military identity card with a small blank photo window, the rest " + ILEG + ", lying on a wool blanket",
  "pow_column|A long column of prisoners of war walking through snow with guards, seen from far away" + FAR + SEM + NOINS],
 # N038 370–500 divisionarios; prisioneros de guerra; condenados a campos
 ["pow_camp|A prisoner-of-war camp in Russia in winter with wooden barracks and a double fence" + FAR + SEM,
  "tribunal_room|A small Soviet military tribunal room, three judges in plain dark tunics without insignia behind a table, a defendant standing" + NOINS + SEM],
 # N039 conviven en los mismos campos (Iordache); Karagandá; el panadero
 ["karaganda_camp|A large labour camp on the flat steppe of Kazakhstan, rows of barracks, a mine headframe in the distance, dust and snow" + FAR + SEM + "@@KARAGANDÁ",
  "two_groups_yard|Two Spanish men in padded jackets sharing a cigarette by a barrack wall, one with a military bearing, one older" + SEM,
  f"baker_oven|{GIRAL48} pulling white loaves out of a brick oven in a camp bakery, steam" + SEM],
 # N040 dos bandos comparten campo; no todos eran españoles; uno era mexicano
 ["shared_table|Men in padded jackets eating soup at a long barrack table, elbows touching" + SEM,
  "mexico_city_1935|Mexico City in 1935, the Palacio de Bellas Artes and a busy avenue with old cars and trams" + SEM + NOFLAG],
 # N041 Moscú 19/06/1947: hombre vestido de campesino pide asilo en la embajada de México
 ["moscow_1947|A quiet Moscow street in June 1947 with old mansions and lime trees" + SEM + NOFLAG + "@@MOSCÚ, 1947",
  f"vadillo_gate|{VADI47} standing at the gate of an elegant embassy mansion, looking over his shoulder" + SEM + NOFLAG,
  "embassy_hall|The entrance hall of an elegant 19th-century embassy mansion with a staircase and a guard at a desk" + SEM + NOFLAG],
 # N042 Evelio Vadillo, Ciudad del Carmen, Campeche; Moscú 1935; detenido 1936; destierro en Kazajistán
 [f"vadillo_1935|{VADI35} on the deck of a ship leaving a tropical port with palm trees" + SEM + "@@EVELIO VADILLO",
  "carmen_port|The waterfront of Ciudad del Carmen in Campeche in the 1930s, fishing boats and palm trees, colonial houses" + SEM + NOFLAG,
  "alma_ata|A Central Asian town at the foot of snowy mountains in the late 1930s, poplar-lined dirt streets" + SEM + NOFLAG],
 # N043 embajador Joublanc Rivas; Moscú no lo deja salir; 1950 veinte años por espiar para México
 [f"joublanc_office|{JOUB} listening gravely to {VADI47} in an embassy office with a desk and tall windows" + SEM + NOFLAG + "@@LUCIANO JOUBLANC RIVAS",
  "visa_denied|A diplomatic note on a desk with a red pencil line across it, " + ILEG,
  "vladimir_prison|An old fortress-like prison of white stone in a Russian provincial town in winter, 1950" + SEM],
 # N044 liberado 1955; 16/10 vuelve a México; libro "Veinte años en el Gulag"
 ["airport_mexico|A 1950s airport in Mexico City, a propeller airliner and a thin grey-haired man walking down the stairs with a small suitcase, plain airliner without any logo" + SEM,
  "book_vadillo|A recent paperback book lying on a wooden desk, plain cover with a faded photograph of barbed wire, no title, no lettering"],
 # N045 sale dos años después de la muerte de Stalin
 ["mourning_crowd|A huge crowd in heavy coats in a Moscow square in March 1953, black ribbons, seen from far away" + SEM + NOFLAG,
  "empty_chair_office|An empty high-backed chair behind a large desk in a dim Kremlin office, a single telephone" + SEM],
 # N046 12/03/1953: Beria cancela más de veinte obras
 ["moscow_1953|The Kremlin walls and towers in Moscow on a grey March day in 1953, snow on the ground" + SEM + NOFLAG + "@@MOSCÚ, 1953",
  f"beria_cancel|{BERIA} drawing a thick line through a list on a typed document with a red pencil" + SEM,
  "project_drawings|Rolled-up engineering drawings of canals and dams stacked in a corner of an office, dusty" + SEM],
 # N047 canales, presas, ferrocarril Salejard–Ígarka; más de dos millones y medio de presos
 ["tundra_rail|An unfinished railway line running straight across the flat Arctic tundra in summer, rails on wooden sleepers, a small locomotive standing still, no people" + SEM,
  "memo_figure|A typed memorandum page with one long number underlined, " + ILEG + ", a fountain pen across it"],
 # N048 amnistía 27/03: cerca de un millón, casi todos comunes; Beria: ineficiencia
 ["camp_gate_open|An open labour camp gate in spring snow, men with small bundles walking out, seen from behind" + SEM,
  "station_released|A crowded railway station in Siberia in 1953 full of men in padded jackets with bundles, waiting for trains" + SEM],
 # N049 respuesta del régimen: no era rentable; españoles seguían dentro; un barco
 ["gold_bowl_dark|A dented tin prisoner bowl with a gold bar inside, in near darkness, a single ray of cold light",
  "barrack_bunks#detalhe-centro"],
 # N050 Odesa, comienzos de 1954: Cruz Roja francesa fleta el Semíramis
 ["odessa_1954|The port of Odessa in early 1954, a passenger steamer with a dark hull at the quay, the city stairs behind, snow patches" + SEM + NOFLAG + "@@ODESA, 1954",
  "red_cross_staff|Two French Red Cross officials in civilian coats with plain white armbands checking a list on a quay" + SEM,
  "semiramis_side|The side of a dark-hulled 1950s passenger steamer with a white superstructure and a single funnel, no name visible, no flags" + SEM],
 # N051 286 españoles: divisionarios, marineros y pilotos, cuatro antiguos niños de la guerra
 ["gangway_board|Men in padded jackets and fur caps climbing a gangway onto a steamer, carrying wooden suitcases" + SEM + NOFLAG,
  "deck_mixed|Men of different ages on a ship's deck, some younger in old military coats without insignia, some older in civilian padded jackets" + SEM + NOFLAG],
 # N052 llamadas por radio a las familias; 2 de abril, 17:35, Barcelona
 ["ship_radio|A ship's radio room, a man in a padded jacket speaking into a microphone while an operator adjusts dials" + SEM,
  "family_radio|A Spanish family in a 1950s kitchen gathered around a radio, a mother with her hand over her mouth" + SEM,
  "bcn_docking|A steamer docking at Barcelona quay in the late afternoon, ropes thrown, the Columbus monument column in the distance" + SEM + NOFLAG],
 # N053 Time: multitud sube a bordo; mujeres se desmayan; 10–16 años en campos
 ["crowd_board|A crowd surging up a gangway onto a ship, people embracing men in padded jackets" + SEM + NOFLAG,
  "woman_faint|A woman in a 1950s coat fainting into the arms of relatives on a crowded quay" + SEM],
 # N054 Muñoz Grandes; ~200 españoles aún en los campos; el libro que lo haría famoso
 [f"munoz_quay|{MUNOZ} on the quay shaking hands with a returning man in a padded jacket, officials behind" + SEM + NOFLAG + "@@MUÑOZ GRANDES",
  "camp_remaining|A labour camp barrack in Kazakhstan in spring 1954, a few Spanish men watching the empty road" + FAR + SEM,
  "typewriter_dark|A typewriter on a kitchen table at night, a sheet of paper in it, " + ILEG + ", a cup of tea"],
 # N055 Madrid, marzo 1976: Directísimo, Íñigo entrevista a Solzhenitsyn
 ["madrid_1976|Madrid in March 1976, the Gran Vía with 1970s cars and people in coats" + SEM + NOFLAG + "@@MADRID, 1976",
  "tv_studio|A 1970s Spanish television studio with big cameras on pedestals, studio lights and a small audience" + SEM,
  f"solzh_inigo|{SOLZH} seated opposite {INIGO} on a television set, an interpreter beside them" + SEM + "@@ALEXANDR SOLZHENITSYN"],
 # N056 Archipiélago: París 1973, español 1974; Octavio Paz lo defendió en Plural
 ["paris_1973|A Paris street in winter 1973 with a bookshop window display of stacked books" + SEM,
  "archipelago_books|A stack of thick books with plain covers on a bookshop counter in 1974, no titles, no lettering",
  f"paz_desk|{PAZ} writing at a desk in a book-lined study in Mexico City" + SEM + "@@OCTAVIO PAZ"],
 # N057 orden de enero de 1960: el Gulag disuelto
 ["order_1960|A short typed order on a single sheet with a round stamp on an office desk, " + ILEG,
  "camp_ruins|The ruins of an abandoned labour camp in the tundra, collapsed barracks and a leaning watchtower, summer grass" + SEM],
 # N058 «Vosotros no sabéis qué es el comunismo»; prensa de izquierda; Marsé
 ["solzh_closeup|" + SOLZH + ", speaking intensely, one hand raised, television studio lights behind him" + SEM,
  f"marse_cafe|{MARSE} reading a magazine with a sarcastic smile at a café table" + SEM + "@@JUAN MARSÉ"],
 # N059 otra prueba más callada: unas fotos
 ["photos_box|An old cardboard box full of black and white photographs, prints spread out on a table under a lamp, the images too small to see"],
 # N060 Las Fotos: Barcelona, 2 de abril de 1954; Pérez de Rozas retrata a los que bajan
 [f"rozas_quay|{ROZAS} raising his camera on a crowded Barcelona quay, a steamer behind" + SEM + NOFLAG + "@@CARLOS PÉREZ DE ROZAS",
  "flash_moment|A burst of camera flash light catching a man in a padded jacket at the bottom of a ship's gangway" + SEM],
 # N061 Archivo Fotográfico de Barcelona; hombres de los dos bandos, mismo barco
 ["archive_bcn|A photographic archive reading room in Barcelona, an archivist in white gloves holding a black and white print" + SEM,
  "print_gangway|A black and white photograph print showing men in padded jackets coming down a ship's gangway, lying on a light table"],
 # N062 2025: libro sobre los marineros republicanos
 ["book_2025|A new hardback book lying on a desk beside an old photograph of a merchant ship, plain cover, no title, no lettering"],
 # N063 culpables o brazos; sus papeles contaban brazos; enemigos, aliados, volver a casa
 ["hands_shovels|Many hands of prisoners in worn mittens gripping shovel handles, close view" + SEM,
  "man_home|A man in a worn padded jacket standing alone at the door of a whitewashed Spanish village house, seen from behind" + SEM + NOFLAG],
 # N064 pregunta final
 ["dossier_close|A brown dossier being closed on a dark desk under a green lamp" + SEM,
  "bcn_port_1954#médio-dir"],
]

THUMBS = [
    {"id": "thumb-A", "prompt": "Ink graphic novel illustration: a dented round tin prisoner bowl with a wire handle and a white painted camp number on its side, empty of any food, a single trapezoid-shaped gold bar (classic bullion shape, top narrower than base, sloped sides) lying inside it with a five-pointed Soviet star embossed on its top, flat ochre ink colour with hard white highlights on the edges, an aluminium spoon lying beside the bowl on a rough frosted wooden plank, the bowl in the left half of the frame in slight high angle, plain dark slate-blue background, the entire right half of the frame completely empty plain dark slate, cold neutral light, no warm glow, no lettering, no text, no letters, no numbers other than the painted camp number, no blood, no red, no hex codes"},
    {"id": "thumb-B", "prompt": "Ink graphic novel illustration: top-down view of a typed Soviet 1930s labour-camp ration norm table on yellowed cream paper lying on a dark wooden desk, three wide table rows with typewritten lines as faint completely illegible blurred texture, a large round red rubber stamp with a clear five-pointed star in the upper left corner of the sheet, on the right column of each row a piece of dark rye bread: a large chunk on the first row, a medium piece on the second, a thin slice on the third, the upper right area of the frame plain dark desk, no hands, no faces, no legible lettering, no hex codes"},
    {"id": "thumb-C", "prompt": "Ink graphic novel illustration: Barcelona harbour in 1954 on a bright Mediterranean afternoon, a man seen from behind, large in the frame (almost half its height), in a grey quilted Soviet labour-camp padded jacket and a fur ushanka hat with ear flaps down, carrying a wooden suitcase, walking down the gangway of a dark-hulled steamer, one hand on the rope rail, below on the quay a small crowd with raised arms and no detailed faces, the Columbus monument column in the background against a pale clear sky, the sky the brightest area behind the man, the lower right corner calm water, no flags, no lettering, no text, no hex codes"},
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
