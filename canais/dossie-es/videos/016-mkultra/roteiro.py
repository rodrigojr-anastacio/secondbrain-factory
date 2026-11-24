#!/usr/bin/env python3
"""Fonte única do dossie-es 016 (MKUltra): roteiro + planos. Gera SCRIPT.md, blocos.json e, quando o storyboard
estiver preenchido (SB/THUMBS), cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py (na pasta do vídeo). Maquinaria de geração copiada do 015-gru (que veio do 014-yakuza).

Embalagem aprovada no crivo r5 (24/11/2026, EMBALAGEM.md/CRIVO.md):
  A/T1 "TODA la historia de MKUltra en 13 minutos | Del laboratorio de la CIA a América Latina" + cogumelos e vela + MKULTRA (objeto-simbolo, controle)
  B/T2 "Cómo la CIA buscó en América Latina la droga del control mental" + cientista com saco de piule + "10 LIBRAS" (cena-acao)
  C/T3 "MKULTRA: lo que la CIA vino a buscar a México… y lo que dejó" + "stress" riscado/"deplore" sobre bandeira de Honduras (documento-evidencia)
Ângulo (ANGULO.md): lo que la CIA vino a buscar a América Latina (semillas 1952, hongos 1955–56, selva 1966) y lo que dejó (químicos contra Castro 1960–61, curso y manual de Honduras 1983–97).

Sintaxe dos planos (campo s): "chave|prompt" nova · "chave" reuso · "chave#enq" reuso com enquadramento · + "@@TEXTO" rótulo.
ROTEIRO v3 + STORYBOARD (24/11/2026): crivo de ângulo r3 aprovado; planos (SB) e bases das thumbs (THUMBS) preenchidos.
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
HOOK_MAX = 50.0      # s: EMBALAGEM: frase-âncora ≤ 0:35 e linha de promessa (último bloco do hook) ≤ 0:50
ANCORA_MAX = 35.0    # s: fim do bloco da frase-âncora
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "TODA la historia de MKUltra en 13 minutos | Del laboratorio de la CIA a América Latina"
TITULOS = ("T1 TODA la historia de MKUltra en 13 minutos | Del laboratorio de la CIA a América Latina / "
           "T2 Cómo la CIA buscó en América Latina la droga del control mental / "
           "T3 MKULTRA: lo que la CIA vino a buscar a México… y lo que dejó")
PROMESSA = ("La historia entera de MKUltra contada por lo que la CIA vino a buscar a América Latina (las semillas de México, "
            "los hongos de Huautla, las plantas de la Amazonía, los químicos que preparó para Fidel Castro) y por lo que dejó "
            "(un método de interrogatorio en un manual usado en Honduras, corregido a mano).")

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Huautla de Jiménez, Oaxaca, verano de mil novecientos cincuenta y seis. Es de noche. María Sabina canta en mazateco.", card="HUAUTLA, 1956")
b("Los hongos pasan de mano en mano. Un químico de Delaware los mastica. No siente éxtasis. Dirá después que se sintió desorientado.")
b("Se llama James Moore. Y desde hace tres años trabaja bajo contrato para la CIA.")
b("Esta es TODA la historia de MKUltra. De lo que la CIA vino a buscar a América Latina… y de lo que dejó.", ideia=True)
b("Las semillas de México, los hongos de Huautla, los químicos que preparó para Fidel Castro y un manual en Honduras.")

# ───────────────────────── 1. LAS SEMILLAS ─────────────────────────
cap("1. Las Semillas")
b("Las Semillas. Washington, octubre de mil novecientos cincuenta y dos. A la CIA le aterra una idea que llega de la guerra de Corea: el lavado de cerebro.", card="WASHINGTON, 1952", ideia=True)
b("Para defenderse, y tener su propia arma, crea el proyecto Bluebird, luego llamado Artichoke. Su jefe, Morse Allen, oye en una reunión el nombre de un arbusto mexicano: el piule.")
b("Pueblos indígenas usan sus semillas en ceremonias religiosas. Allen envía a México a un joven científico de la agencia, cuyo nombre no aparece en los papeles publicados.")
b("Llega entre diciembre de mil novecientos cincuenta y dos y comienzos del cincuenta y tres. Se hace pasar por investigador de plantas anestésicas. Prueba muestras en la sierra, al sur de la capital.", card="MÉXICO, 1953")
b("En febrero ya tiene sacos llenos. Según el periodista John Marks, entre ellos, diez libras de piule.")
b("Antes de irse, oye hablar de unos hongos especiales que solo salen con las lluvias del verano.", ideia=True)

# ───────────────────────── 2. LA GRANJA ─────────────────────────
cap("2. La Granja")
b("La Granja. Pensilvania, veinticuatro de junio de mil novecientos cincuenta y tres. Morse Allen visita Toughkenamon, la mayor zona productora de champiñones del mundo.", card="PENSILVANIA, 1953", ideia=True)
b("En abril, el director Allen Dulles había aprobado un programa nuevo, con dinero fuera de la contabilidad normal: MKUltra.")
b("A los productores no les gusta cultivar hongos tóxicos: perderían clientes. Pero, según Marks, el patriotismo gana. Cultivarán el hongo que pida el gobierno.")
b("Dos días después, Allen firma un memorando: Hongos, variedades narcóticas y venenosas. Ya hay presupuesto y granja. Falta el hongo.")
b("En noviembre, la CIA pone LSD, sin avisarle, en la copa de licor de Frank Olson, científico del Ejército. Nueve días después, Olson cae desde el décimo piso de un hotel de Nueva York.", ideia=True)

# ───────────────────────── 3. LA VELADA ─────────────────────────
cap("3. La Velada")
b("La Velada. Huautla, veintinueve de junio de mil novecientos cincuenta y cinco. Un banquero de Nueva York entra de noche en una casa de adobe.", card="HUAUTLA, 1955", ideia=True)
b("Es Robert Gordon Wasson, vicepresidente de J. P. Morgan y aficionado a los hongos. Con él, un fotógrafo y una veintena de mazatecos. María Sabina dirige la ceremonia.")
b("Wasson se describirá como uno de los primeros hombres blancos en comer los hongos sagrados. Ella los llama los niños santos.")
b("Wasson viaja por su cuenta. Pero un botánico de la Ciudad de México envía un informe del viaje. Según Marks, llega a la sede de la CIA… y a un químico que cobra de la agencia.", ideia=True)

# ───────────────────────── 4. LA BOLSA ─────────────────────────
cap("4. La Bolsa")
b("La Bolsa. Delaware, mil novecientos cincuenta y seis. James Moore le escribe a Wasson una carta que, según el banquero, llega de la nada.", card="DELAWARE, 1956", ideia=True)
b("Quiere estudiar los hongos mexicanos. Y conoce, dice, una fundación que podría ayudar. El Fondo Geschickter aporta dos mil dólares.")
b("Según Marks, ese fondo era un canal de la CIA, y la búsqueda del hongo se vuelve el subproyecto cincuenta y ocho de MKUltra. Marks no dice que Wasson supiera de dónde salía el dinero.")
b("En Huautla duermen en el suelo de tierra. Todos disfrutan, menos Moore: tiene un resfriado terrible, pasan hambre, le pica todo el cuerpo.")
b("En la velada de María Sabina, los demás ven maravillas. Él no. Wasson dirá que parecía un marinero de agua dulce en alta mar.")
b("Poco después, Moore vuelve a Delaware con una bolsa de hongos. Y se encierra en su laboratorio a buscar el principio activo.", ideia=True)

# ───────────────────────── 5. LA REVISTA ─────────────────────────
cap("5. La Revista")
b("La Revista. Nueva York, trece de mayo de mil novecientos cincuenta y siete. La revista Life publica diecisiete páginas de Wasson con fotos a color.", card="NUEVA YORK, 1957", ideia=True)
b("Un editor le pone al artículo un título que Wasson no quería: En busca del hongo mágico.")
b("Mientras tanto, el micólogo francés Roger Heim cultiva los hongos en París y manda muestras a Albert Hofmann, el químico suizo que descubrió el LSD.")
b("En marzo de mil novecientos cincuenta y ocho, Hofmann publica el resultado: psilocibina. La CIA pagó parte de la expedición. La molécula la presenta un laboratorio suizo.")
b("Y el artículo atrae a México oleadas de visitantes. Uno de ellos, de vacaciones, es un psicólogo de Harvard: Timothy Leary.", ideia=True)
b("Si te interesan estos expedientes, suscríbete. Porque mientras la CIA buscaba en la sierra mexicana, su laboratorio ya preparaba químicos para un solo hombre: Fidel Castro.")

# ───────────────────────── 6. EL ESTUDIO ─────────────────────────
cap("6. El Estudio")
b("El Estudio. Washington, mil novecientos sesenta. Fidel Castro gobierna Cuba con discursos de horas por radio y televisión.", card="WASHINGTON, 1960", ideia=True)
b("Según el Comité Church del Senado, que cita un informe interno de la CIA, entre marzo y agosto la agencia estudia cómo sabotearlos. Los planes salen de la División de Servicios Técnicos: el laboratorio de la CIA, la misma división que administraba MKUltra.")
b("Un funcionario recuerda haber discutido rociar el estudio desde donde transmite Castro con una sustancia de efectos parecidos al LSD. Se descarta: no es fiable.")
b("Otro plan: poner sales de talio en sus zapatos durante un viaje, para que se le caiga la barba. Lo prueban en animales. Castro cancela el viaje.")
b("Y el laboratorio impregna una caja de puros con un químico que desorienta, para que Castro fume uno antes de un discurso.", ideia=True)

# ───────────────────────── 7. LOS PUROS ─────────────────────────
cap("7. Los Puros")
b("Los Puros. Dieciséis de agosto de mil novecientos sesenta. Un funcionario de la CIA recibe una caja de los puros favoritos de Castro.", card="AGOSTO DE 1960", ideia=True)
b("La orden ya no es humillarlo. Es tratarlos con una toxina botulínica tan potente, según el Comité Church, que bastaba con llevarse un puro a la boca.")
b("El siete de octubre están listos. El trece de febrero de mil novecientos sesenta y uno, se entregan a una persona no identificada. Y el registro, dice el comité, no revela si se intentó hacerlos llegar a Castro.")
b("El comité halló pruebas de al menos ocho complots de la CIA contra la vida de Castro entre mil novecientos sesenta y sesenta y cinco. Castro murió en dos mil dieciséis, a los noventa años. Para entonces, en la estación de la CIA en México, ya esperaba otro encargo.", ideia=True)

# ───────────────────────── 8. LA SILLA ─────────────────────────
cap("8. La Silla")
b("La Silla. Ciudad de México, julio de mil novecientos sesenta y tres. Washington pide a la estación de la CIA un candidato para un experimento de hipnosis rápida.", card="CIUDAD DE MÉXICO, 1963", ideia=True)
b("Eligen a un agente de poca monta que, al parecer, los soviéticos habían convertido en agente doble. Lo citan con una excusa: los jefes quieren darle más dinero.")
b("El plan: tumbar su silla hacia atrás, de golpe, y que en ese instante entre un hipnotizador traído de California.")
b("Los oficiales tumban la silla. El hipnotizador se queda paralizado. No pasa nada. Le dicen al agente que oyeron un ruido y quisieron protegerlo. Él se lo cree.")
b("Así se lo contó a Marks uno de los participantes. Ese mismo mes, un informe del inspector general de la CIA concluye que las drogas de MKUltra casi no se usan en operaciones.", ideia=True)

# ───────────────────────── 9. LA SELVA ─────────────────────────
cap("9. La Selva")
b("La Selva. Iquitos, Perú, mil novecientos sesenta y seis. MKUltra ya se llama MKSearch. Y la búsqueda de plantas sigue.", card="IQUITOS, 1966", ideia=True)
b("J. C. King, exjefe de la división de la CIA para el hemisferio occidental, funda con apoyo de la agencia una empresa en apariencia privada: la Amazon Natural Drug Company.")
b("Según Marks, King recorre los ríos en su casa flotante, con un vaso de whisky. En sus oficinas de Iquitos trabajan al menos dos paramilitares de la CIA.")
b("Envían a Estados Unidos una liana paralizante, base del curare, y cultivan yagé, la ayahuasca. Un botánico de Harvard trabaja con ellos sin saber nada de la CIA.")
b("En mil novecientos setenta y dos, la CIA cierra MKSearch. En enero de mil novecientos setenta y tres, por orden verbal del director Richard Helms, se destruyen los archivos de MKUltra.", ideia=True)

# ───────────────────────── 10. LAS CUENTAS ─────────────────────────
cap("10. Las Cuentas")
b("Las Cuentas. Universidad de Delaware. El químico de la velada de Huautla, James Moore, sigue cobrando de la CIA. Y le pasa sus cuentas.", card="LAS CUENTAS DE MOORE", ideia=True)
b("Según Marks: mil ciento cuarenta y siete dólares en hongos. Cuatrocientos treinta y tres en mescalina. Y doce mil dólares por un cuarto de tonelada de fluothane, un anestésico.")
b("Cuentas así, papeles de dinero, son casi todo lo que queda del programa: siete cajas de carpetas financieras olvidadas en un archivo de registros retirados, que en mil novecientos setenta y siete llegan al Senado con ciento cuarenta y nueve subproyectos, cuarenta y cuatro universidades y el nombre del psiquiatra Ewen Cameron, en Montreal, cuyos pacientes demandarían después a la CIA.")
b("Mientras Moore facturaba hongos, otra oficina de la CIA escribía lo que había aprendido sobre interrogar. Según el historiador Alfred McCoy, en julio de mil novecientos sesenta y tres ese método quedó codificado en un manual secreto: KUBARK.")
b("Veinte años después, secciones del KUBARK reaparecen en otro manual de la CIA, de mil novecientos ochenta y tres. Para saber de dónde salió, hay que ir a Honduras.", ideia=True)

# ───────────────────────── 11. EL CURSO ─────────────────────────
cap("11. El Curso")
b("El Curso. Honduras, mil novecientos ochenta y tres. Una abogada, Inés Murillo, lleva semanas detenida sin orden judicial. Un día, a su celda entra un oficial de la CIA.", card="HONDURAS, 1983", ideia=True)
b("Lo sabemos porque la propia CIA lo admitió. En mil novecientos ochenta y ocho, Richard Stolz, subdirector de operaciones de la agencia, reconoce esa visita ante el Senado. Murillo pasó casi ochenta días detenida ilegalmente.")
b("La había detenido el Batallón tres dieciséis, una unidad secreta del ejército hondureño. El Comisionado Nacional de Derechos Humanos documentó ciento ochenta y cuatro casos de desaparición.")
b("En esas mismas audiencias, Stolz describe el curso que la CIA dio ese año a militares hondureños: tres semanas de clase y dos de práctica, con presos reales. Asegura que el maltrato físico se rechazó.")
b("Y de ese curso salieron papeles.", ideia=True)

# ───────────────────────── 12. LA TACHADURA ─────────────────────────
cap("12. La Tachadura")
b("La Tachadura. Entre mil novecientos ochenta y cuatro y ochenta y cinco, alguien abre un manual de interrogatorio de la CIA y, en la segunda página, corrige la frase a pluma.", card="MANUAL DE 1983", ideia=True)
b("La frase original, en inglés, decía «we do not stress»: no ponemos énfasis en las técnicas coercitivas, pero queremos que sepas usarlas bien.")
b("Encima escribe «deplore»: deploramos esas técnicas, y queremos que las conozcas para que las evites. Debajo, la frase original se sigue leyendo.")
b("Según un informe del Senado, el manual nació de las notas del curso de Honduras. Habla de celdas sin ventanas y de arrestos de madrugada, para causar el máximo malestar mental.")
b("Esa página tachada sale a la luz recién en enero de mil novecientos noventa y siete, cuando el Baltimore Sun amenaza con demandar a la CIA para obtenerla. En Honduras, el juez Roy Medina dice que confirma una verdad que su país conocía desde hacía mucho.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. Los Niños Santos")
b("Los Niños Santos. Huautla, otoño de mil novecientos sesenta y dos. Albert Hofmann sube a la sierra con Wasson. Trae pastillas de psilocibina.", card="HUAUTLA, 1962", ideia=True)
b("María Sabina las prueba de noche. Al amanecer, dice que tienen el mismo poder que los hongos. La casa de la velada de mil novecientos cincuenta y cinco ya no existe: según Hofmann, la quemaron, probablemente vecinos molestos porque reveló el secreto a extraños.")
b("Años después, en el testimonio que recogió Álvaro Estrada, ella contó que desde que llegaron los extranjeros, los niños santos perdieron su pureza.")
b("La CIA vino a América Latina a buscar una droga para abrir la mente. Lo que dejó fue un manual para quebrarla.", ideia=True)
b("Y tú, ¿qué pesa más en esta historia: lo que la CIA vino a buscar, o lo que dejó? Déjalo en los comentarios.")

# ───────────────────────── STORYBOARD (planos por bloco, na ordem dos blocos) ─────────────────────────
# Preenchido na etapa storyboard (skill storyboard): uma lista de planos por bloco de texto, na ordem.
SEM = ", no lettering anywhere, every sign blank"
NOINS = ", no flags, no insignia, no badges, no emblems, no armbands, no medals"
NOFLAG = ", no flags"
FAR = ", seen from far away, no bodies, no blood"
ILEG = "the writing only as faint completely illegible blurred lines, no readable letters"
BLANK = "completely blank sheets of paper, no writing at all"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, borders as thin lines and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame, no ocean names"
# Lugares (fidelidade)
HUAUTLA = "Huautla de Jimenez, a Mazatec mountain town in the Sierra Mazateca of Oaxaca, Mexico, adobe houses with tin and thatched roofs clinging to steep green slopes, mist and cloud forest"
ADOBE_INT = "the dim interior of a small adobe house in Huautla, Oaxaca, at night, packed earth floor, a simple altar table with saint images as blank faded prints, a single beeswax candle as the only light (small flame, no golden halo)"
SIERRA_MX = "dry pine-and-oak mountains south of Mexico City in early 1953, a dirt track, maguey agave plants, a small village of whitewashed adobe houses with clay tile roofs"
TOUGH = "the mushroom-growing country of Toughkenamon, Chester County, Pennsylvania, in 1953, rows of long low windowless cinder-block mushroom houses with ventilation chimneys, green fields"
HAVANA = "Havana in 1960, the Malecon seafront with pastel colonial facades and 1950s American cars"
IQUITOS = "Iquitos, Peru, in 1966, an Amazon river town, wooden stilt houses and floating houses on the brown river, old tiled rubber-boom buildings, dense jungle on the far bank"
TEGUS = "Tegucigalpa, Honduras, in 1983, a hilly city of low colonial buildings with red tile roofs, pine-covered mountains around, a whitewashed colonial cathedral with two bell towers"
# Personagens ("resembling" só para rostos conhecidos; os sem retrato público ficam genéricos)
SABINA = "a small Mazatec woman of about sixty resembling Maria Sabina, dark hair parted in the middle, a long white embroidered huipil dress with red and blue embroidery, barefoot"
WASSON = "an American banker of about fifty-seven in 1955 resembling R. Gordon Wasson, balding with grey hair, round glasses, tweed jacket and tie"
MOORE = "a slim young American chemist of about thirty in 1956, short dark hair, plain glasses, khaki shirt and field jacket"
MOORE_LAB = "a slim young American chemist of about thirty in 1956, short dark hair, plain glasses, white lab coat"
SCIENTIST = "a young American scientist in the early 1950s, light felt fedora and khaki field jacket, face mostly in the shadow of the hat brim"
ALLEN = "an American security officer in his forties in 1952, short dark hair, dark suit and tie, stern face"
DULLES = "an American official of about sixty in 1953 resembling Allen Dulles, white moustache, round glasses, tweed suit, holding a pipe"
HEIM = "a French scientist of about sixty in 1957 resembling Roger Heim, grey hair, glasses, white lab coat"
HOFMANN57 = "a Swiss chemist of about fifty-two in 1958 resembling Albert Hofmann, dark hair combed back, high forehead, white lab coat"
HOFMANN62 = "a Swiss chemist of about fifty-six in 1962 resembling Albert Hofmann, dark hair combed back, high forehead, dark sweater and jacket"
LEARY = "an American psychologist of about thirty-nine in 1960 resembling Timothy Leary, short hair, smiling, white shirt with rolled sleeves"
CASTRO = "a Cuban leader of about thirty-three in 1960 resembling Fidel Castro, full black beard, plain olive green fatigues without any insignia"
KING = "an older American businessman of about sixty-five in 1966, white hair, light tropical suit, holding a glass of whisky"
HELMS = "an American official of about sixty in 1973 resembling Richard Helms, slicked-back grey hair, dark suit and tie"
CAMERON = "a Scottish-Canadian psychiatrist of about fifty-five resembling Ewen Cameron, grey hair, round face, white coat"
MURILLO = "a young Honduran woman of about twenty-four in 1983, long dark hair, tired face, plain blouse"
STOLZ = "an American intelligence official of about sixty-two in 1988, grey hair, glasses, dark suit and tie"
MEDINA = "a Honduran judge of about fifty in 1997, dark hair with grey temples, dark suit and tie"
TECH = "a CIA laboratory technician in 1960, white lab coat, rubber gloves, face turned away"

SB = [
 # N001 Huautla 1956, de noche, María Sabina canta
 ["huautla_night|" + HUAUTLA + ", at night, a few windows lit by candles, wide view" + SEM + "@@HUAUTLA, OAXACA",
  "velada_sabina|" + ADOBE_INT + ", " + SABINA + " kneeling and singing with closed eyes, a few Mazatec men and women sitting on mats in the shadows",
  "sabina_close|Close-up of " + SABINA + " singing in candlelight, eyes closed, hands raised slightly"],
 # N002 los hongos pasan de mano en mano; químico de Delaware los mastica; desorientado
 ["mushrooms_pass|Close-up of brown-skinned hands passing pairs of small brown Psilocybe mushrooms on a banana leaf in a dark adobe room, candlelight",
  "moore_chews|" + ADOBE_INT + ", " + MOORE + " sitting cross-legged on a mat among Mazatec villagers, chewing a mushroom with a doubtful face",
  "moore_dizzy|Close-up of " + MOORE + " in a dark adobe room, sweating, eyes unfocused and disoriented, the candle flame doubled behind him",
  "mats_shadows|Straw mats and blankets on the packed earth floor of a dark adobe house at night, a single candle, shadows of seated people on the wall"],
 # N003 James Moore, contrato con la CIA
 ["moore_portrait|Medium portrait of " + MOORE + " in a dim adobe doorway at night, looking out at the dark mountains" + "@@JAMES MOORE",
  "cia_contract|A typed contract on a dark desk, " + ILEG + ", a fountain pen and a plain manila folder, cold desk lamp light",
  "dc_1953|Low temporary wooden office buildings along the Reflecting Pool in Washington in 1953, the Washington Monument behind, grey sky" + SEM + NOFLAG + "@@CIA, WASHINGTON"],
 # N004 frase-ancla
 ["dossier_desk|A brown cardboard dossier on a dark desk under a green-shaded lamp, a red rubber stamp beside it, a few small dark seeds scattered on the desk" + SEM,
  # americas_map: pinos no código — Huautla, Ciudad de México, La Habana, Iquitos, Tegucigalpa
  "americas_map|" + MAPA + ", showing Mexico, Central America, the Caribbean and northern South America",
  "huautla_dawn|" + HUAUTLA + ", at dawn, mist rising from the valley, wide view" + SEM,
  "seeds_hand|Close-up of an open palm full of small dark brown seeds, cool morning light, a canvas sack in the background"],
 # N005 linha de promessa: semillas, hongos, químicos para Castro, manual en Honduras
 ["seed_pile|A pile of small dark brown seeds spilling from an open canvas sack onto a striped Mexican sarape, cool daylight",
  "cigar_box_lab|An open wooden box of Cuban cigars on a white laboratory bench beside glass vials and a dropper, cold fluorescent light" + SEM,
  "manual_pen|A typewritten page on a desk with one line struck through in blue ink, " + ILEG + ", a blue ballpoint pen lying beside it, a folded Honduran flag partly visible (turquoise-white-turquoise stripes)"],
 # N006 Las Semillas. Washington 1952, lavado de cerebro (Corea)
 ["korea_pow|American prisoners of war in padded winter coats sitting in rows in a bare wooden hall in North Korea in 1952, listening to a lecture" + NOINS + SEM,
  "dc_night_1952|The Reflecting Pool and temporary office buildings of Washington at night in October 1952, a few lit windows" + SEM + NOFLAG + "@@WASHINGTON, 1952",
  "brainwash_report|A stack of typed intelligence reports on a desk, " + ILEG + ", a photograph clipped on top showing only a blurred face, cold light",
  "officers_meeting|Three American officials in dark suits around a small table in a smoky 1952 office, one pointing at a folder" + NOINS],
 # N007 Bluebird → Artichoke; Morse Allen oye el nombre del piule
 ["bluebird_files|Two plain manila folders on a desk, one on top of the other, a red rubber stamp and an ink pad beside them" + SEM,
  "allen_desk|" + ALLEN + " sitting at a desk in a 1952 government office, listening intently, notebook open" + "@@MORSE ALLEN",
  "experts_meeting|A meeting of drug experts in 1952, four men in suits at a long table with glass beakers and botanical books, one leaning forward to speak" + NOINS,
  "piule_plant|A botanical drawing style close-up of a flowering morning glory vine with white trumpet flowers and small round seed pods, Rivea corymbosa, on a sunlit wall in Mexico" + "@@PIULE",
  "allen_note|Close-up of a hand writing in a small notebook with a fountain pen, " + ILEG],
 # N008 semillas en ceremonias; Allen envía a un joven científico sin nombre
 ["seeds_ritual|A Mazatec healer's hands grinding small seeds on a stone metate beside a candle in a dim adobe room",
  "ceremony_seeds|A small indigenous ceremony in rural Mexico at night, an elderly man offering a gourd bowl, seated villagers in white cotton clothes",
  "scientist_packs|" + SCIENTIST + " packing a suitcase with glass sample jars and a botanical press in a Washington apartment in 1952",
  "name_redacted|A typed travel document on a desk with one line fully covered by a thick black bar, " + ILEG],
 # N009 llega dic/1952–1953; investigador de anestésicas; prueba muestras en la sierra
 ["mx_1953|Paseo de la Reforma in Mexico City in early 1953, the golden-winged Angel of Independence column, 1950s cars, pedestrians in hats" + SEM + NOFLAG + "@@CIUDAD DE MÉXICO",
  "scientist_market|" + SCIENTIST + " at a village market stall in the mountains, looking at baskets of dried plants and seeds held by an indigenous vendor woman in a rebozo",
  "sierra_1953|" + SIERRA_MX + ", wide view, cool dry morning light" + SEM,
  "sample_test|" + SCIENTIST + " kneeling beside a camp table in the mountains, dropping seeds into a glass test tube, a small field notebook open"],
 # N010 febrero: sacos llenos; diez libras de piule (Marks)  [paga a Thumb B]
 ["sacks_full|Several full canvas sacks lined up against a whitewashed adobe wall in a Mexican mountain village, maguey plants nearby, hard cold side light",
  "scientist_sack|Tight medium shot in profile of " + SCIENTIST + ", glancing back over his shoulder, a canvas sack full of seeds on his shoulder close to the camera, whitewashed adobe wall and maguey plants behind, hard cold side light, no warm glow",
  "scale_seeds|An old hanging brass market scale weighing a sack of small dark seeds, an indigenous vendor's hand on the sack, cool light"],
 # N011 oye hablar de hongos que salen con las lluvias
 ["vendor_talks|An elderly indigenous Mexican man in a straw hat talking quietly to " + SCIENTIST + " under a tiled porch, gesturing toward the mountains",
  "rain_mountains|Rain clouds pouring over the green mountains of Oaxaca in summer, mist in the valleys" + SEM,
  "wild_mushrooms|Small brown mushrooms with slender stems growing from wet grass and dung in a rainy Oaxacan meadow, close-up"],
 # N012 La Granja. Pensilvania 1953, Toughkenamon
 ["tough_wide|" + TOUGH + ", wide view on a June afternoon" + SEM + "@@TOUGHKENAMON, PENSILVANIA",
  "allen_car|A black 1953 sedan driving along a country road between mushroom houses in Pennsylvania, two men in hats inside" + SEM,
  "mush_beds|The dark interior of a 1953 mushroom house, long wooden shelves of compost beds covered with white button mushrooms, dim bulbs"],
 # N013 abril: Dulles aprueba MKUltra, dinero fuera de la contabilidad
 ["dulles_sign|" + DULLES + " signing a document at a desk in 1953, " + ILEG + ", a pipe resting in an ashtray" + "@@ALLEN DULLES",
  "cash_envelopes|Plain envelopes thick with banknotes in an open steel cash box on a desk, no ledger, cold light" + SEM,
  "mkultra_folder|A single plain manila folder lying alone on a dark wooden desk under a lamp, a red rubber stamp beside it" + SEM],
 # N014 productores reticentes; patriotismo; cultivarán lo que pida el gobierno
 ["growers_meet|Three Pennsylvania mushroom farmers in work jackets and caps in a farm office, arms crossed, facing two men in dark suits across a table" + NOINS,
  "handshake_farm|A handshake between a mushroom farmer in a work jacket and a man in a dark suit outside a cinder-block mushroom house" + NOINS,
  "grower_tray|A farmer's hands holding a wooden tray of strange dark mushrooms in a dim mushroom house"],
 # N015 memorando Hongos narcóticos y venenosos; falta el hongo
 ["memo_type|A typewriter in a 1953 office typing a memorandum, " + ILEG + ", a cup of coffee beside it",
  "mush_drawings|Botanical illustrations of several poisonous mushrooms pinned to a cork board in a government office, no labels",
  "empty_tray|An empty wooden mushroom tray on a shelf in a dark mushroom house, a single bulb above"],
 # N016 Olson: LSD en el licor, cae del décimo piso
 ["deep_creek|A rustic log lodge by a lake at night in November 1953, warm windows shown in cool tones, a few cars parked" + SEM,
  "liqueur_glass|Close-up of a small glass of Cointreau liqueur on a wooden table, a hand pouring a few drops from a tiny vial into it, dark room",
  "olson_portrait|Medium portrait of a man of about forty-three in 1953 resembling Frank Olson, receding dark hair, glasses, suit and tie, worried face" + "@@FRANK OLSON",
  "hotel_window|The facade of a tall Manhattan hotel at night in 1953 seen from the street far below, one high window with a torn shade blowing in the wind" + FAR + SEM],
 # N017 La Velada. Huautla 1955, banquero entra en una casa de adobe
 ["huautla_1955|" + HUAUTLA + ", on a rainy night in June 1955, a narrow muddy path between adobe houses" + SEM + "@@HUAUTLA, 1955",
  "wasson_door|" + WASSON + " ducking through the low doorway of an adobe house at night, a Mazatec man holding a candle for him",
  "adobe_ext|A small adobe house with a thatched roof on a steep slope at night, candlelight through the doorway, cloud forest around" + SEM],
 # N018 Wasson, J.P. Morgan; fotógrafo, veintena de mazatecos; María Sabina
 ["wasson_portrait|Medium portrait of " + WASSON + " in a New York office in 1955, bookshelves of mushroom books behind him" + SEM + "@@R. GORDON WASSON",
  "photographer|An American photographer in 1955 with a large flash camera kneeling in a dark adobe room, villagers sitting on mats around",
  "mazatecs_circle|About twenty Mazatec men and women sitting in a circle on mats inside a candlelit adobe house at night, quiet faces",
  "sabina_leads|" + SABINA + " standing before a small altar in candlelight, holding mushrooms in the smoke of copal incense"],
 # N019 primeros hombres blancos en comer los hongos; niños santos
 ["wasson_eats|" + WASSON + " sitting on a mat in a dark adobe room, holding a pair of small mushrooms in his palm, hesitating",
  "ninos_santos|Pairs of small Psilocybe mushrooms arranged on banana leaves before a candle on an altar, dark adobe room" + "@@LOS NIÑOS SANTOS",
  "sabina_close#detalhe-centro"],
 # N020 Wasson por su cuenta; botánico envía informe; llega a la CIA y a un químico
 ["wasson_travel|" + WASSON + " riding a mule along a mountain trail in Oaxaca with a Mazatec guide on foot" + SEM,
  "botanist_letter|A botanist in a Mexico City office in 1955 sealing a letter in a plain envelope at a desk covered with dried plant specimens",
  "moore_reads|" + MOORE_LAB + " reading a typed report in a university laboratory, glassware behind him, frowning with interest"],
 # N021 La Bolsa. Delaware 1956, carta "de la nada"
 ["udel_1956|The brick Georgian buildings and white cupola of the University of Delaware campus in Newark in 1956, students walking" + SEM + NOFLAG + "@@DELAWARE, 1956",
  "moore_writes|" + MOORE_LAB + " typing a letter at a desk in a small university office at night",
  "letter_arrives|" + WASSON + " opening an envelope at his desk in New York, surprised expression"],
 # N022 estudiar los hongos; una fundación; Fondo Geschickter 2.000 dólares
 ["moore_proposal|" + MOORE + " in a jacket and tie sitting across a desk from " + WASSON + ", gesturing as he explains, New York office",
  "check_2000|A bank check on a desk, " + ILEG + ", a fountain pen beside it, cold light"],
 # N023 fondo = canal de la CIA; subproyecto 58; Marks no dice que Wasson supiera
 ["money_flow|A shadowy hand passing a plain envelope across a desk to another hand, dark office, only hands visible",
  "sub58_folder|A plain manila folder with a thin red string tie on a desk, a red rubber stamp beside it, cold light" + SEM + "@@SUBPROYECTO 58",
  "marks_book|An American journalist in his thirties in the late 1970s at a cluttered desk stacked with photocopied documents, reading with a pencil" + SEM + "@@JOHN MARKS"],
 # N024 Huautla 1956: duermen en el suelo; resfriado, hambre, picazón
 ["expedition_arrives|A small expedition of foreigners with mules and canvas bags arriving at " + HUAUTLA + ", in summer 1956" + SEM,
  "floor_sleep|Several foreigners sleeping in blankets on the packed earth floor of an adobe house, " + MOORE + " awake, shivering",
  "moore_cold|Close-up of " + MOORE + " with a red nose, sniffling and scratching his arm, miserable in a dark adobe room"],
 # N025 en la velada, los demás ven maravillas; él no; marinero de agua dulce
 ["velada_1956|" + ADOBE_INT + ", " + SABINA + " singing, foreigners and villagers sitting on mats with eyes closed in wonder",
  "moore_sick|" + MOORE + " clutching his stomach on a mat in a dark adobe room, pale and dizzy, the others serene around him",
  "sea_metaphor|A small rowing boat tossed on dark stormy waves at night, a lone man clinging to the side, ink illustration"],
 # N026 vuelve a Delaware con una bolsa de hongos; laboratorio
 ["moore_bag|" + MOORE + " carrying a cloth bag of dried mushrooms down a muddy mountain trail in Oaxaca, looking back",
  "moore_lab|" + MOORE_LAB + " alone in a university laboratory at night, grinding dried mushrooms in a mortar, glass flasks bubbling"],
 # N027 La Revista. Nueva York 1957, Life 17 páginas
 ["ny_1957|A Manhattan street corner in May 1957, a newsstand with stacks of magazines whose covers are completely blank, yellow taxis, passers-by in hats" + SEM + "@@NUEVA YORK, 1957",
  "life_spread|A large picture magazine open on a table showing full-page color photographs of a candlelit mushroom ceremony, the page text as " + ILEG],
 # N028 título que Wasson no quería: En busca del hongo mágico
 ["editor_title|A magazine editor in shirtsleeves in a 1957 office writing on a layout sheet with a thick pencil, " + ILEG,
  "wasson_annoyed|" + WASSON + " frowning at an open magazine at his desk in New York, glasses pushed up"],
 # N029 Heim cultiva en París; muestras a Hofmann
 ["heim_lab|" + HEIM + " in a Paris laboratory tending glass jars of growing mushrooms on shelves" + "@@ROGER HEIM",
  "parcel_basel|A small wrapped parcel tied with string on a laboratory bench in Basel, Switzerland, glass vials around it" + SEM],
 # N030 1958: Hofmann publica psilocibina; la CIA pagó; laboratorio suizo
 ["hofmann_lab|" + HOFMANN57 + " in a Swiss laboratory holding up a small glass vial of white crystals to the light" + "@@ALBERT HOFMANN",
  "crystals|Close-up of white crystals in a small glass dish on a laboratory bench, cold light" + "@@PSILOCIBINA",
  "moore_empty|" + MOORE_LAB + " staring at an empty glass flask in his Delaware laboratory, disappointed"],
 # N031 oleadas de visitantes; Timothy Leary
[
  "foreigners_town|Foreign visitors with cameras walking through the steep streets of Huautla, villagers watching from doorways" + SEM,
  "leary|" + LEARY + " sitting by a swimming pool at a hotel in Cuernavaca, Mexico, sunlight, a plate of mushrooms on a table" + "@@TIMOTHY LEARY"],
 # N032 CTA + re-hook: el laboratorio preparaba químicos para Fidel Castro
 ["subscribe_dossier|A brown cardboard dossier opening on a dark desk, a red rubber stamp lifting from it" + SEM,
  "sierra_1953#médio-esq",
  "castro_speech|" + CASTRO + " speaking passionately into a cluster of 1960 microphones at night, a crowd below, seen from the side" + NOINS,
  "lab_bottles|Rows of glass bottles and vials on a laboratory shelf in Washington in 1960, cold light, one bottle with a red cap" + SEM],
 # N033 El Estudio. Washington 1960; Castro gobierna con discursos por radio y TV
 ["dc_1960|Washington in 1960, the Capitol dome at dusk seen from the Mall, bare trees" + SEM + NOFLAG + "@@WASHINGTON, 1960",
  "havana_1960|" + HAVANA + ", seen from a rooftop at dusk" + SEM + NOFLAG + "@@LA HABANA"],
 # N034 Comité Church cita informe interno; mar–ago; División de Servicios Técnicos
 ["church_1975|A U.S. Senate committee hearing room in 1975, senators behind a long wooden dais, microphones, wood paneling" + NOFLAG + SEM + "@@COMITÉ CHURCH, 1975",
  "tsd_lab|The laboratory of the CIA Technical Services Division in 1960, workbenches with chemical glassware, a lock-picking set and miniature cameras, cold light" + SEM,
  "tsd_men|Two CIA technicians in white lab coats leaning over a workbench, one holding a small glass vial up to the light" + NOINS],
 # N035 rociar el estudio con sustancia tipo LSD; se descarta
 ["studio_empty|An empty 1960 radio and television studio in Havana at night, a vintage microphone on a desk, a heavy studio camera, cables on the floor" + SEM + NOFLAG,
  "aerosol|A glass atomizer bottle with a rubber squeeze bulb standing on a laboratory bench next to a vial, cold light, nobody touching it"],
 # N036 sales de talio en los zapatos; barba; animales; cancela el viaje
 ["shoes_thallium|A pair of black leather shoes on a laboratory bench, a gloved hand sprinkling white powder into one of them",
  "beard_castro|Close-up of " + CASTRO + " stroking his thick black beard, looking sideways",
  "lab_animals|Laboratory cages with white rabbits on a shelf in a 1960 lab, a technician taking notes, cold light" + SEM],
 # N037 caja de puros impregnada con químico que desorienta
 ["cigars_close|Close-up of a row of fat Cuban cigars in an open cedar box, a glass dropper hovering above one of them, gloved fingers",
  "tech_cigars|" + TECH + " carefully re-sealing an open cedar cigar box on a lab bench under a lamp",
  "castro_cigar|" + CASTRO + " holding an unlit cigar backstage before a speech, papers in his other hand, a microphone stand nearby" + NOINS],
 # N038 Los Puros. 16 ago 1960: funcionario recibe caja de puros favoritos
 ["cigar_handover|Two men in suits in a 1960 office, one handing a sealed cedar cigar box to the other across a desk, only their torsos visible" + SEM + "@@16 DE AGOSTO DE 1960",
  "cigar_box_closed|A sealed cedar box of Cuban cigars on a dark desk, its label completely blank, a single lamp" + SEM,
  "tech_cigars#médio-dir"],
 # N039 toxina botulínica; bastaba con llevarse un puro a la boca
[
  "syringe_cigar|Close-up of a fine needle injecting a single cigar on a white tray, gloved hands, harsh cold light",
  "cigar_mouth|Silhouette of a bearded man raising a cigar toward his lips in a dark doorway, backlit, face not visible",
  "cigar_box_lab#detalhe-centro"],
 # N040 7 oct listos; 13 feb 1961 entregados a persona no identificada; registro no revela
[
  "night_handoff|A shadowy handoff of a small wrapped package between two figures under a streetlight at night, faces hidden" + SEM + "@@13 DE FEBRERO DE 1961",
  "record_blank|An open file folder on a desk, the page inside completely blank under a lamp, " + BLANK,
  "church_1975#detalhe-alto"],
 # N041 al menos ocho complots 1960–65; Castro murió en 2016 a los 90; estación de México espera otro encargo
 ["plots_board|A cork board in a dim office with eight index cards pinned in a row, connected by red string, " + ILEG,
  "castro_old|A frail elderly man of about ninety resembling Fidel Castro in 2016, white beard, tracksuit jacket, sitting in a chair" + NOINS,
  "castro_speech#detalhe-centro",
  "mx_station|A modest office building in Mexico City in 1963 with venetian blinds, a black car parked outside, jacaranda trees" + SEM + NOFLAG],
 # N042 La Silla. Ciudad de México 1963; hipnosis rápida
 ["mx_1963|Paseo de la Reforma in Mexico City in 1963, the golden-winged Angel of Independence column, modern office towers and 1960s cars" + SEM + NOFLAG + "@@CIUDAD DE MÉXICO, 1963",
  "cable_desk|A teletype cable sheet torn off a machine in a dim office, " + ILEG + ", a hand holding it",
  "hypno_watch|A pocket watch swinging on a chain in front of a dark background, ink illustration"],
 # N043 agente de poca monta, doble; excusa: más dinero
 ["small_agent|A nervous Mexican man of about thirty-five in a cheap suit in a 1963 cafe, smoking, glancing at the door",
  "money_offer|A thick envelope of banknotes pushed across a table toward a nervous man's hands, 1963 office" + SEM],
 # N044 tumbar la silla hacia atrás y que entre el hipnotizador de California
 ["chair_room|A bare 1963 office room with a single wooden chair in the middle, a door on the side, venetian blinds casting stripes" + SEM,
  "hypnotist_waits|An American man in a suit waiting tensely behind a half-open door in a dim corridor, hand on the doorknob"],
 # N045 tumban la silla; hipnotizador paralizado; no pasa nada; ruido
 ["chair_tilt|Two officers in suits tipping a wooden chair backwards with a startled man in it, 1963 office, motion lines",
  "hypnotist_frozen|An American man in a suit frozen in a doorway, mouth open, unable to move",
  "agent_believes|The nervous Mexican man straightening his tie and nodding, the two officers smiling awkwardly beside him"],
 # N046 lo contó a Marks un participante; informe del inspector general 1963: drogas casi no se usan
 ["marks_book#médio-dir",
  "ig_1963|A typed inspector general report on a desk in 1963, " + ILEG + ", a red pencil mark in the margin" + "@@INFORME DEL INSPECTOR GENERAL"],
 # N047 La Selva. Iquitos 1966; MKSearch
 ["iquitos_wide|" + IQUITOS + ", wide view from the river" + SEM + NOFLAG + "@@IQUITOS, PERÚ, 1966",
  "amazon_canoe|A dugout canoe with two men paddling along a brown Amazon tributary, dense jungle walls on both sides" + SEM],
 # N048 J.C. King; Amazon Natural Drug Company
 ["king_portrait|" + KING + " on the veranda of a wooden house in the Peruvian Amazon" + "@@J. C. KING",
  "andc_office|A small company office in Iquitos in 1966, a ceiling fan, crates of dried plants, a sign above the door completely blank" + SEM],
 # N049 casa flotante con whisky; dos paramilitares de la CIA
[
  "king_whisky|" + KING + " sitting in a wicker chair on the deck of a houseboat, raising a glass of whisky, jungle behind",
  "paramilitaries|Two tough American men in khaki shirts and sunglasses in a jungle office in Iquitos, maps on the wall completely blank" + NOINS + SEM],
 # N050 liana paralizante (curare); yagé/ayahuasca; botánico de Harvard
 ["curare_vine|A thick twisting jungle liana climbing a tree in the Amazon, a man cutting it with a machete",
  "ayahuasca_pot|A clay pot of dark ayahuasca brew boiling over a fire in a jungle hut, chopped vine pieces beside it",
  "harvard_botanist|An American botanist in his fifties in a jungle camp in 1966, pressing leaves into a plant press, unaware, peaceful" + "@@BOTÁNICO DE HARVARD"],
 # N051 1972 cierre MKSearch; ene 1973 Helms ordena destruir archivos
 ["helms_order|" + HELMS + " speaking quietly to an aide in a Langley office in 1973" + "@@RICHARD HELMS",
  "files_burn|Cardboard boxes of files being fed into an industrial shredder in a basement in 1973, paper strips everywhere" + SEM + "@@ENERO DE 1973"],
 # N052 Las Cuentas. Universidad de Delaware; Moore sigue cobrando; le pasa sus cuentas
 ["udel_1956#detalhe-alto",
  "moore_bills|" + MOORE_LAB + ", older now, sitting at his desk in a Delaware laboratory office writing figures on invoice forms, " + ILEG,
  "invoice_stack|A small stack of typed invoices clipped together on a desk, " + ILEG + ", a fountain pen"],
 # N053 1.147 hongos, 433 mescalina, 12.000 por un cuarto de tonelada de fluothane
 ["mush_jars|Glass jars of dried mushrooms on a laboratory shelf in Delaware, cold light, labels completely blank" + SEM,
  "mescaline|Small brown glass bottles of mescaline powder on a lab bench, a scale beside them, labels completely blank" + SEM,
  "fluothane_drums|A row of metal drums of anesthetic liquid stacked in a university storeroom, a hand truck nearby, drums without any lettering" + SEM + "@@FLUOTHANE"],
 # N054 papeles de dinero: siete cajas en archivo de registros retirados; 1977 Senado: 149 subproyectos, 44 universidades, Cameron
 ["seven_boxes|Seven cardboard archive boxes stacked in a dim retired records warehouse, dust in the air, boxes without any lettering" + SEM + "@@7 CAJAS",
  "senate_1977|A U.S. Senate hearing room in August 1977, a witness table with microphones before a raised dais, photographers" + NOFLAG + SEM + "@@SENADO, 1977",
  "allan_memorial|The Allan Memorial Institute in Montreal, a grey stone mansion on the slope of Mount Royal, winter" + SEM + NOFLAG + "@@MONTREAL",
  "cameron|" + CAMERON + " standing in a hospital corridor in the 1950s, clipboard in hand" + "@@EWEN CAMERON"],
 # N055 otra oficina escribía lo aprendido sobre interrogar; McCoy; KUBARK jul/1963
[
  "mccoy|An American historian of about sixty in 2006 with grey hair and a beard, in a book-lined study" + SEM + "@@ALFRED McCOY",
  "kubark_manual|A thick typed manual bound with metal fasteners lying on a dark desk, cover completely blank, a red rubber stamp beside it" + SEM + "@@KUBARK, 1963"],
 # N056 veinte años después secciones reaparecen en manual de 1983; hay que ir a Honduras
[
  "honduras_map|" + MAPA + ", showing Central America with Honduras in the center",
  "tegus_wide|" + TEGUS + ", wide view in 1983" + SEM + NOFLAG + "@@TEGUCIGALPA"],
 # N057 El Curso. Honduras 1983; Inés Murillo detenida; entra un oficial de la CIA
 ["cell_murillo|" + MURILLO + " sitting on a thin mattress in a bare concrete cell, light from a high barred window" + "@@INÉS MURILLO",
  "cell_door|A heavy metal cell door opening in a dark corridor, a man in civilian clothes stepping in, face in shadow",
  "cia_officer|An American man in a short-sleeved shirt and slacks standing in a bare cell doorway, notebook in hand, face in shadow" + NOINS],
 # N058 1988 Stolz reconoce la visita ante el Senado; ~80 días detenida
 ["stolz|" + STOLZ + " testifying at a witness table with microphones in a Senate hearing room in 1988" + NOFLAG + SEM + "@@RICHARD STOLZ",
  "transcript|A typed hearing transcript on a table, " + ILEG + ", a pair of reading glasses",
  "senate_1977#detalhe-centro"],
 # N059 Batallón 3-16; Comisionado Nacional: 184 desaparecidos
 ["jeep_night|A military jeep with its headlights on in a Tegucigalpa street at night, men in plain civilian clothes beside it, no insignia" + NOINS + SEM + "@@BATALLÓN 3-16",
  "photos_wall|A wall covered with small black-and-white portrait photographs of missing people, faces only as blurred sketches, candles below"],
 # N060 Stolz describe el curso: 3 semanas de clase y 2 de práctica, presos reales; rechazó el maltrato físico
 ["classroom|A plain classroom in a Honduran military base in 1983, men in olive fatigues without insignia at desks, an American instructor at a blackboard with nothing written" + NOINS + SEM,
  "stolz#médio-dir"],
 # N061 y de ese curso salieron papeles
 ["notes_course|A pile of handwritten course notes and typed pages on a classroom desk, " + ILEG],
 # N062 La Tachadura. 1984–85: alguien corrige la frase a pluma, segunda página
 ["manual_1983|A typed training manual open on a desk at its second page, " + ILEG + ", cold neutral light" + "@@MANUAL DE 1983",
  "pen_corrects|Close-up of a hand with a blue ballpoint pen striking through a typed line on a page, " + ILEG,
  "manual_pen#detalhe-centro",
  "desk_1984|An office desk in 1984 with a typewriter, an ashtray and a single open manual under a lamp" + SEM],
 # N063 «we do not stress»: no ponemos énfasis, pero queremos que sepas usarlas
[
  "page_full|A yellowed typewritten page filling the frame, " + ILEG + ", a few lines bracketed in pencil"],
 # N064 encima escribe «deplore»; la frase original se sigue leyendo
 ["handwrite|Close-up of a hand writing a single word in blue ink above a struck-through typed line, " + ILEG,
  "struck_line|Extreme close-up of a typed line crossed out with a blue pen stroke, still visible beneath, " + ILEG],
 # N065 informe del Senado: nació de las notas del curso; celdas sin ventanas; arrestos de madrugada
[
  "windowless_cell|A windowless concrete cell with a single bare bulb, completely empty" + SEM,
  "dawn_arrest|A dark street of low houses at dawn, a car with its headlights on stopped in front of a door, figures standing by it" + FAR + SEM],
 # N066 enero 1997 Baltimore Sun amenaza con demandar; página sale; juez Roy Medina
 ["sun_newsroom|A newspaper newsroom in Baltimore in 1997, reporters at computer desks, stacks of papers, monitors" + SEM + "@@BALTIMORE SUN, 1997",
  "medina|" + MEDINA + " speaking in a wood-paneled office in Tegucigalpa, a Honduran flag folded on a shelf behind him (turquoise-white-turquoise stripes with five stars)" + "@@JUEZ ROY MEDINA",
  "tegus_wide#detalhe-baixo"],
 # N067 Cierre. Huautla 1962: Hofmann sube con Wasson; pastillas de psilocibina
 ["huautla_1962|" + HUAUTLA + ", in autumn 1962, two foreigners with walking sticks climbing a steep path with a Mazatec guide" + SEM + "@@HUAUTLA, 1962",
  "hofmann62|" + HOFMANN62 + " holding a small glass bottle of pink pills in an adobe house" + "@@ALBERT HOFMANN",
  "pills|Close-up of small pink pills in an open palm beside a candle, dark adobe room"],
 # N068 María Sabina las prueba; mismo poder; la casa de 1955 ya no existe, quemada
 ["sabina_old|" + SABINA + ", older, swallowing a pill at night in candlelight, Hofmann and Wasson sitting nearby",
  "dawn_sabina|" + SABINA + " standing in an adobe doorway at dawn, mist on the mountains, calm face",
  "burned_house|The charred remains of a small adobe house on a mountain slope in Huautla, blackened walls, no people" + SEM,
  "adobe_ext#médio-esq"],
 # N069 testimonio a Álvaro Estrada: los niños santos perdieron su pureza
 ["estrada|A young Mazatec man of about thirty in the 1970s with a tape recorder, listening to an elderly woman in a huipil on a porch",
  "sabina_late|A frail elderly Mazatec woman resembling Maria Sabina in the 1970s, deep wrinkles, white huipil, sitting alone on a doorstep looking at the mountains"],
 # N070 la CIA vino a buscar una droga para abrir la mente; dejó un manual para quebrarla
 ["mush_and_manual|A pair of small mushrooms on a banana leaf beside a typed manual with a struck-through line, both on a dark table, cold light, " + ILEG,
  "huautla_dawn#detalhe-centro"],
 # N071 pregunta final
 ["dossier_close|A brown cardboard dossier closing on a dark desk under a lamp, a few dark seeds beside it" + SEM,
  "americas_map#médio-esq"],
]

THUMBS =[
    {"id": "thumb-A", "prompt": "Ink graphic novel illustration: four sacred Psilocybe mushrooms arranged in two pairs on a banana leaf, in the left half of the frame, a lit beeswax candle behind them as the only light source with a small flame and no golden halo spreading, on a Mazatec embroidered cloth with birds and flowers in red and blue thread, on a dark wooden table, cool neutral shadows, the entire right half of the frame plain empty dark slate-blue, no lettering, no logos, no text, no letters, no hex codes"},
    {"id": "thumb-B", "prompt": "Ink graphic novel illustration: tight medium shot in profile of a young American scientist in the early 1950s, light felt fedora and khaki field jacket, glancing back over his shoulder, his face almost entirely hidden in the hard black shadow of the hat brim (only the jaw lit), carrying on his shoulder a canvas sack full of seeds, close to the camera so it fills the right-center foreground (a sack of about ten pounds, not a huge coffee sack), a large smooth blank light area of canvas facing the viewer, a few small dark brown seeds (never red) spilling from its tied mouth, behind him an out-of-focus whitewashed adobe wall with his hard shadow and large maguey agave plants against a pale mountain sky, hard cold side light from the right, deep ink shadows, dry season morning, no warm or golden glow, no lettering, no logos, no text, no letters, no hex codes"},
    {"id": "thumb-C", "prompt": "Ink graphic novel illustration: close-up of a slightly tilted yellowed typewritten page occupying about two thirds of the frame, resting on a folded flag of Honduras (horizontal turquoise-blue, white and turquoise-blue stripes with five small turquoise-blue stars on the white stripe, the stars visible at the lower left, outside the page), the lines on the page left as faint blank gray bars with no readable letters, a blue ballpoint pen lying beside the page (not writing), cool neutral desk light from the left, no stamps, no legible letters, no logos, no text, no hex codes"},
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
    if not SB:   # roteiro antes do storyboard: só SCRIPT.md + blocos.json (+ mapa de tempos para conferir a EMBALAGEM)
        tt, linhas_t, capa = 0.0, [], None
        for blk in B:
            if "cap" in blk: capa = blk["cap"]; linhas_t.append(f"{fmt(tt)}  {capa}"); continue
            d_ = dur(blk["t"]); linhas_t.append(f"   {fmt(tt)}–{fmt(tt + d_)}  {limpo(blk['t'])[:70]}"); tt += d_
        (out / "SCRIPT.md").write_text(
            f"# {TITULO}: roteiro\n\nPromessa: {PROMESSA}\n\nTítulos: {TITULOS}\n\n"
            f"Gerado por `roteiro.py` (fonte única; edite lá). {words} palavras, ~{fmt(total)} estimados a {WPS*60:.0f} ppm (com as pausas entre frases).\n"
            "Os blocos [Nxxx] são os mesmos de `blocos.json` (lá com as tags do Fish). Storyboard ainda não feito.\n" + "\n".join(script))
        print("\n".join(linhas_t)); print(json.dumps({"palavras": words, "duracao": fmt(total), "blocos": len(blocos)}, ensure_ascii=False))
        return
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
