#!/usr/bin/env python3
"""Fonte única do dossie-es 013 (Juicios de Núremberg): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py (na pasta do vídeo). Geração copiada do 012-mi6.

Embalagem aprovada no crivo r3 (20/11/2026, EMBALAGEM.md/CRIVO.md):
  A/T1 fórmula + fones sobre creme, NÚREMBERG + sello SIN NOMBRE (objeto-simbolo, controle)
  B/T2 "Cómo Núremberg le puso nombre al crimen que no tenía nombre" + fiscal lendo a acusação sob refletor, sem texto (cena-acao)
  C/T3 "Núremberg: de la sala 600 a los tribunales de América Latina" + mapa atlântico, fio vermelho, HASTA AQUÍ (mapa-lugar)
Ângulo (ANGULO.md): las palabras de Núremberg (o tribunal que inventou o que ia julgar) e o destino delas na América Latina.

Sintaxe dos planos (campo s): "chave|prompt" nova · "chave" reuso · "chave#enq" reuso com enquadramento · + "@@TEXTO" rótulo.
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
TITULO = "TODA la historia de los Juicios de Núremberg en 14 minutos"
TITULOS = ("T1 TODA la historia de los Juicios de Núremberg en 14 minutos / "
           "T2 Cómo Núremberg le puso nombre al crimen que no tenía nombre / "
           "T3 Núremberg: de la sala 600 a los tribunales de América Latina")
PROMESSA = ("Núremberg tuvo que inventar lo que iba a juzgar (las palabras genocidio y crímenes contra la humanidad, "
            "la regla contra 'cumplía órdenes', hasta la sala y la traducción; genocidio, de Lemkin, entró en la acusación pero no en la sentencia) y esas reglas acabaron alcanzando a "
            "criminales y dictadores en América Latina.")

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Núremberg, octubre de mil novecientos cuarenta y seis. En un hotel, un fiscal estadounidense ve a un abogado polaco muy afectado.", card="NÚREMBERG, 1946")
b("Es Raphael Lemkin. La guerra le quitó a cuarenta y nueve familiares. Para ese crimen, inventó una palabra.")
b("Se leyó en voz alta el primer día del juicio. En la sentencia, ni una vez. La palabra es genocidio.")
b("Esta es TODA la historia de los juicios de Núremberg. Y de las palabras que viajaron desde allí hasta América Latina.", ideia=True)

# ───────────────────────── 1. LA PALABRA ─────────────────────────
cap("1. La Palabra")
b("La Palabra. Washington, mil novecientos cuarenta y cuatro. Lemkin es un jurista judío polaco. Huyó de la invasión alemana en mil novecientos treinta y nueve.", card="WASHINGTON, 1944")
b("En un libro sobre la ocupación nazi de Europa, propone un término nuevo. Une la raíz griega genos, pueblo o raza, con la terminación latina cidio, matar.")
b("Para Lemkin, genocidio es la destrucción de una nación o de un grupo étnico. No solo matar personas. Borrar a un pueblo entero.")
b("Tres años antes, Churchill había dicho por radio que el mundo estaba ante un crimen sin nombre. Ahora el nombre existe.")
b("Falta que un tribunal se atreva a usarlo. Y otro jurista busca otra palabra. Estudió Derecho en la misma universidad que Lemkin.", ideia=True)

# ───────────────────────── 2. EL JARDÍN ─────────────────────────
cap("2. El Jardín")
b("El Jardín. Cambridge, veintinueve de julio de mil novecientos cuarenta y cinco. Robert Jackson, el fiscal jefe estadounidense, almuerza en casa del profesor Hersch Lauterpacht. Después, hablan en el jardín.", card="CAMBRIDGE, 1945")
b("Según el jurista y escritor Philippe Sands, en el jardín Jackson le pide ayuda con una pregunta: cómo llamar lo que los nazis hicieron con millones de civiles.")
b("Lauterpacht le propone un nombre: crímenes contra la humanidad.")
b("Lauterpacht estudió en Leópolis, la ciudad que los alemanes llamaban Lemberg. Lemkin también. Según Sands, casi toda la familia de Lauterpacht fue asesinada allí.")
b("Y uno de los futuros acusados gobernó la Polonia ocupada, Leópolis incluida: Hans Frank.")
b("Diez días después del almuerzo, esa expresión entra en un documento firmado por cuatro potencias.", ideia=True)

# ───────────────────────── 3. LA CARTA ─────────────────────────
cap("3. La Carta")
b("La Carta. Londres, agosto de mil novecientos cuarenta y cinco. Su artículo ocho cabe en una frase. Haber actuado por orden de un gobierno o de un superior no libra a nadie de responsabilidad.", card="LONDRES, 1945")
b("Como máximo, podrá reducir la pena. Las cuatro potencias aliadas firman esa Carta el ocho de agosto. Define tres crímenes: contra la paz, de guerra y contra la humanidad.")
b("En los meses siguientes, diecinueve países se adhieren al acuerdo. Entre ellos, Venezuela, Uruguay, Paraguay, Panamá, Honduras y Haití.")
b("Guarda esa regla de las órdenes. Cuarenta y dos años después, en Buenos Aires, alguien la escribirá al revés. Pero antes, la regla necesita una sala.", ideia=True)

# ───────────────────────── 4. LA SALA ─────────────────────────
cap("4. La Sala")
b("La Sala. Núremberg, verano de mil novecientos cuarenta y cinco. Un capitán estadounidense de treinta y tres años, Dan Kiley, recibe un encargo: preparar la sala seiscientos del Palacio de Justicia.", card="NÚREMBERG, 1945")
b("Kiley es arquitecto y sirve en el servicio de inteligencia de su país. La sala es demasiado pequeña para lo que viene.")
b("Kiley derriba una pared y eleva el techo. La sala duplica su tamaño. Instala cabinas de vidrio para intérpretes y camarógrafos. Y una galería para doscientos cincuenta periodistas.")
b("Según contó Kiley, en la obra trabajaron presos que habían sido miembros de las SS, junto a civiles alemanes. Las butacas de terciopelo rojo salieron de un cine cercano.")
b("Para Kiley no era un juicio cualquiera: lo iba a mirar el mundo entero. Y en esa sala, la primera palabra importante se iba a decir en francés.", ideia=True)

# ───────────────────────── 5. EL MICRÓFONO ─────────────────────────
cap("5. El Micrófono")
b("El Micrófono. Núremberg, veinte de noviembre de mil novecientos cuarenta y cinco, primer día del juicio. Un fiscal francés, Pierre Mounier, lee ante el micrófono el cargo de crímenes de guerra.", card="NÚREMBERG, 1945")
b("Ahí está la palabra de Lemkin: genocidio. La acusación habla del exterminio de grupos raciales y nacionales. Sobre todo, de judíos, polacos y gitanos.")
b("En ese mismo instante, la palabra suena en otras tres lenguas. Detrás de un vidrio, los intérpretes de Léon Dostert traducen mientras Mounier habla.")
b("Dostert, antiguo intérprete del general Eisenhower, probó a unos setecientos candidatos. Solo sirvió uno de cada veinte. Después, la ONU copiará el sistema.")
b("Pero una acusación también puede volverse contra quien acusa. Unos meses después, un abogado alemán lo demuestra con un cuestionario.", ideia=True)

# ───────────────────────── 6. EL CUESTIONARIO ─────────────────────────
cap("6. El Cuestionario")
b("El Cuestionario. Once de mayo de mil novecientos cuarenta y seis. Un oficial de la Marina estadounidense le hace preguntas por escrito al almirante Chester Nimitz, que había comandado la flota del Pacífico.", card="ESTADOS UNIDOS, 1946")
b("Las preguntas las pidió Otto Kranzbühler, abogado del almirante Karl Dönitz, el sucesor de Hitler. A Dönitz se lo acusa, entre otros cargos, de hundir barcos sin aviso.")
b("Nimitz responde bajo juramento: el siete de diciembre de mil novecientos cuarenta y uno, el jefe de operaciones navales ordenó la guerra submarina sin restricciones contra Japón.")
b("La sentencia cita esa respuesta y una orden británica de mil novecientos cuarenta. Y escribe que la pena de Dönitz no se fija por esas violaciones. Recibe diez años por otros cargos.")
b("El tribunal solo juzga a los vencidos: será una de sus críticas más repetidas. Pero no finge que los vencedores no tengan expedientes. Y en octubre, un hombre espera de la sentencia otra cosa: su palabra.", ideia=True)

# ───────────────────────── 7. EL HOTEL ─────────────────────────
cap("7. El Hotel")
b("El Hotel. Núremberg, primeros días de octubre de mil novecientos cuarenta y seis. Volvemos al hotel del principio, el Grand Hotel. El fiscal Henry King contó que allí vio a Lemkin muy afectado.", card="NÚREMBERG, 1946")
b("Los jueces acaban de leer la sentencia, tras doscientos dieciocho días de audiencias. Condenan a muerte a doce acusados, Bormann entre ellos, en ausencia, y absuelven a tres. Los demás van a prisión.")
b("Diez de esas condenas se ejecutan el dieciséis de octubre. Hermann Göring se había quitado la vida la noche anterior, en su celda.")
b("La sentencia condena crímenes contra la humanidad, pero solo los ligados a la guerra. Lo que el régimen hizo antes contra judíos y otros grupos queda fuera. Y la palabra genocidio no aparece ni una vez.")
b("Según el jurista William Schabas, Lemkin llamó a ese veredicto el día más negro de su vida. Su palabra había entrado en la sala, pero no en la sentencia.", ideia=True)
b("Si te interesan estos expedientes, suscríbete. Porque lo que viene ahora se cuenta mucho menos: Núremberg no terminó en esa sala.")

# ───────────────────────── 8. EL CÓDIGO ─────────────────────────
cap("8. El Código")
b("El Código. Núremberg, nueve de diciembre de mil novecientos cuarenta y seis. Empieza la serie de juicios que siguen al principal, ahora ante tribunales militares estadounidenses.", card="NÚREMBERG, 1946")
b("El primero sienta en el banquillo a veintitrés acusados, casi todos médicos. Se los acusa de experimentos con prisioneros de los campos, sin su consentimiento. Muchos de ellos murieron o quedaron mutilados.")
b("En agosto de mil novecientos cuarenta y siete, dieciséis son culpables y siete condenados a muerte. Con la sentencia nace un texto de diez puntos: el Código de Núremberg.")
b("Su primera frase dice: el consentimiento voluntario del sujeto humano es absolutamente esencial. La ética médica todavía empieza ahí, con las víctimas de aquellos experimentos.")
b("Otra regla inventada en Núremberg. Mientras tanto, Lemkin recorre pasillos, delegado por delegado, con su palabra.", ideia=True)

# ───────────────────────── 9. LA CONVENCIÓN ─────────────────────────
cap("9. La Convención")
b("La Convención. París, nueve de diciembre de mil novecientos cuarenta y ocho. La ONU aprueba la Convención para la Prevención y la Sanción del Delito de Genocidio.", card="PARÍS, 1948")
b("Define el genocidio como los actos cometidos para destruir, total o parcialmente, a un grupo nacional, étnico, racial o religioso.")
b("La palabra que el tribunal no escribió ahora es un delito internacional. Entra en vigor en enero de mil novecientos cincuenta y uno.")
b("Pero una ley solo sirve si alguien la aplica. Y varios de los responsables de esos crímenes cruzaron el océano.", ideia=True)

# ───────────────────────── 10. LA FÁBRICA ─────────────────────────
cap("10. La Fábrica")
b("La Fábrica. São Bernardo do Campo, Brasil, años sesenta. En la planta de Volkswagen trabaja un austríaco llamado Franz Stangl. Usa su propio nombre.", card="SÃO PAULO, 1967")
b("Stangl había sido comandante de Sobibor y después de Treblinka, dos campos de exterminio donde fueron asesinados cientos de miles de judíos. Huyó por Italia y Siria y llegó a Brasil en mil novecientos cincuenta y uno.")
b("El veintiocho de febrero de mil novecientos sesenta y siete, la policía brasileña lo detiene en São Paulo, tras una pista de Simon Wiesenthal. En junio, Brasil lo extradita a Alemania Occidental.")
b("En diciembre de mil novecientos setenta, un tribunal de Düsseldorf lo condena a cadena perpetua. Según esa sentencia, en Treblinka fueron asesinadas al menos cuatrocientas mil personas.")
b("Stangl murió en prisión en mil novecientos setenta y uno. Brasil lo entregó. En Chile, la respuesta fue otra.", ideia=True)

# ───────────────────────── 11. EL PLAZO ─────────────────────────
cap("11. El Plazo")
b("El Plazo. Santiago de Chile, mil novecientos sesenta y tres. Alemania Occidental pide la extradición de Walter Rauff, antiguo oficial de las SS.", card="SANTIAGO, 1963")
b("Según la fiscalía alemana, Rauff dirigió el uso de camiones en los que se asfixiaba a las víctimas con gas. Así fueron asesinadas unas noventa y siete mil personas.")
b("La Corte Suprema de Chile rechaza la extradición. Según la ley chilena, el delito ya había prescrito: el plazo era de quince años.")
b("En mil novecientos sesenta y ocho, la ONU aprueba otra convención: los crímenes de guerra y contra la humanidad no prescriben. Para el caso Rauff, llegó tarde.")
b("Rauff murió libre en Santiago, en mil novecientos ochenta y cuatro. En Argentina, el obstáculo no fue un plazo. Fue una ley.", ideia=True)

# ───────────────────────── 12. LA LEY ─────────────────────────
cap("12. La Ley")
b("La Ley. Buenos Aires, mil novecientos ochenta y cinco. Nueve excomandantes de la dictadura militar se sientan en el banquillo, acusados de secuestros, torturas y asesinatos. La prensa habla del Núremberg argentino.", card="BUENOS AIRES, 1985")
b("El fiscal Julio César Strassera cierra su alegato con una frase: señores jueces, nunca más. En diciembre, cinco de los nueve son condenados.")
b("Quedan cientos de oficiales por juzgar. En mil novecientos ochenta y seis, una ley pone plazo a las denuncias. Al año siguiente, tras un levantamiento militar, llega la Ley de Obediencia Debida.")
b("Presume que casi todos los oficiales de menor rango actuaron cumpliendo órdenes y, por eso, no pueden ser castigados. Es la defensa que el artículo ocho de Núremberg había rechazado en mil novecientos cuarenta y cinco.")
b("En dos mil tres, el Congreso la anula. En dos mil cinco, la Corte Suprema la declara inconstitucional y los juicios se reabren. En otro país, la palabra de Lemkin llega a un tribunal nacional, contra un exdictador.", ideia=True)

# ───────────────────────── 13. LA JUEZA ─────────────────────────
cap("13. La Jueza")
b("La Jueza. Ciudad de Guatemala, diez de mayo de dos mil trece. La jueza Yassmín Barrios lee la sentencia contra el exdictador Efraín Ríos Montt.", card="GUATEMALA, 2013")
b("El tribunal lo declara culpable de genocidio contra el pueblo maya ixil, por mil setecientas setenta y una víctimas documentadas, y de delitos contra los deberes de humanidad. Ochenta años de prisión.")
b("Según la radio pública estadounidense NPR, era la primera vez que un país condenaba por genocidio a uno de sus propios exjefes de Estado.")
b("Diez días después, la Corte de Constitucionalidad anula la sentencia por defectos de procedimiento, no por inocencia. El juicio vuelve a empezar y Ríos Montt muere en dos mil dieciocho sin un nuevo veredicto.")
b("Pero la palabra ya se había escrito en una sentencia de su propio país. Sesenta y siete años después de faltar en la de Núremberg.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. La Palabra")
b("La Palabra. Nueva York, agosto de mil novecientos cincuenta y nueve. Raphael Lemkin muere de un ataque al corazón, a los cincuenta y nueve años, sin dinero.", card="NUEVA YORK, 1959")
b("Según el periodista A. M. Rosenthal, del New York Times, a su entierro fueron siete personas.")
b("Núremberg no inventó el crimen. Le puso nombre ante un tribunal: crímenes contra la humanidad en la sentencia, genocidio en la acusación. Y sus reglas terminaron en salas de Buenos Aires y de Guatemala.")
b("El crimen era viejo. Lo nuevo fue tener una palabra para él.", ideia=True)
b("Y tú, ¿crees que ponerle nombre a un crimen ayuda a que no se repita? Déjalo en los comentarios.")

# ───────────────────────── STORYBOARD (planos por bloco, na ordem dos blocos) ─────────────────────────
SEM = ", no lettering anywhere"
NOINS = ", no flags, no insignia, no eagles, no swastikas, no badges, no armbands"
FAR = ", seen from far away, no bodies, no blood"
ILEG = "the writing only as faint completely illegible blurred lines, no readable letters"
BLANK = "completely blank sheets of paper, no writing at all"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, rivers and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame, no ocean names"
# Personagens (descrição visual fixa; "resembling", nunca foto; sem insígnias)
LEMKIN = "a man resembling Raphael Lemkin in 1946, about forty-six, balding with dark hair at the sides, long oval face, dark three-piece suit"
KING = "a young American lawyer of about twenty-seven in 1946, short dark hair, plain dark suit"
JACKSON = "a man resembling Robert H. Jackson in 1945, about fifty-three, receding grey hair, round face, dark suit"
LAUT = "a man resembling Hersch Lauterpacht in 1945, about forty-eight, bald head, round glasses, dark suit"
FRANK = "a man resembling Hans Frank in 1945, about forty-five, dark slicked-back hair, plain grey civilian suit"
KILEY = "a young American army captain resembling Dan Kiley in 1945, about thirty-three, lean face, short hair, plain khaki uniform without any insignia"
MOUNIER = "a French prosecutor of about forty in 1945 wearing a black French magistrate's robe with a white jabot"
DOSTERT = "a man resembling Léon Dostert in 1945, about forty, dark hair, round face, plain khaki uniform without insignia"
NIMITZ = "a man resembling Admiral Chester Nimitz in 1946, about sixty, white hair, plain dark naval uniform without medals or insignia"
DONITZ = "a man resembling Karl Dönitz in 1946, about fifty-four, thin face, receding hair, plain dark civilian suit"
KRANZ = "a German defense lawyer of about thirty-seven in 1946, dark hair, plain dark jacket without insignia"
STANGL = "a man of about fifty-nine in 1967 resembling Franz Stangl, grey hair combed back, plain light work shirt"
STRASS = "a man resembling Julio César Strassera in 1985, about fifty-two, glasses, moustache, dark suit and tie"
BARRIOS = "a Guatemalan female judge of about fifty in 2013, short dark hair, black judge's robe"
RIOS = "an elderly man of about eighty-six resembling Efraín Ríos Montt in 2013, white hair, glasses, dark suit"
CHURCH = "a man resembling Winston Churchill in 1941, bald, bow tie, dark suit"
SB = [
 # N001 Núremberg, oct 1946; hotel; fiscal ve a Lemkin muy afectado
 ["hotel_lobby|A 1946 hotel lobby in a half-ruined German city, worn armchairs, a reception desk, officers and civilians passing, grey autumn light through tall windows" + SEM + NOINS,
  f"king_sees|{KING} stopping in a hotel corridor and looking with concern at a man sitting alone in an armchair, 1946",
  f"lemkin_chair|{LEMKIN} sitting alone in a worn hotel armchair, head bowed, hands clasped, devastated expression, 1946@@RAPHAEL LEMKIN"],
 # N002 Lemkin; 49 familiares; inventó una palabra
 [f"lemkin_close|Close-up of {LEMKIN}, eyes wet, staring into nothing, soft window light",
  "family_photos|A small pile of old family photographs on a hotel table, faded portraits of a mother, a father and children from the 1930s, faces soft and indistinct",
  f"lemkin_writing|{LEMKIN} writing at a small desk at night under a lamp, " + ILEG],
 # N003 se leyó el primer día; en la sentencia ni una vez; genocidio
 ["court600_wide|Wide view of the Nuremberg courtroom 600 in 1945, wood panelling, judges' bench, rows of defendants with white-helmeted military police behind them, bright film lights" + NOINS + SEM,
  "judgment_pages|A thick bound court judgment of 1946 lying open on a dark desk, " + ILEG + ", a fountain pen beside it",
  "red_circle_empty|Close-up of a typed page with an empty gap in a line where a word is missing, a red pencil hovering over the gap, " + ILEG],
 # N004 Esta es TODA la historia… América Latina
 ["case_file|A brown cardboard case folder on a dark desk under a lamp, a red rubber stamp beside it" + SEM,
  "red_stamp|A hand slamming a red rubber stamp onto a brown paper case file, dramatic close-up" + SEM,
  "atlantic_map|" + MAPA + ", showing the whole Atlantic Ocean with Europe at the top right and Central and South America at the left"],
 # N005 La Palabra. Washington 1944; jurista judío polaco; huyó 1939
 ["washington_1944|Washington D.C. in 1944, a quiet avenue with government buildings and early winter trees, people in coats and hats",
  f"lemkin_library|{LEMKIN} at a long library table piled with law books in 1944, reading intently",
  "warsaw_1939|Refugees leaving a Polish city in September 1939 on a road, carts and suitcases, smoke on the horizon" + FAR,
  "train_north|A crowded 1939 passenger train crossing a snowy northern landscape at dusk"],
 # N006 un libro; término nuevo; genos + cidio
 ["book_1944|A thick new hardcover book of 1944 lying on a desk, plain dark blue cloth cover" + SEM,
  f"lemkin_manuscript|Close-up of the hands of {LEMKIN} correcting a typewritten manuscript with a pencil, " + ILEG,
  "greek_latin|Two old dictionaries lying open side by side on a desk, one with Greek-looking letters and one with Latin, " + ILEG,
  "typewriter_word|A 1940s typewriter with a single sheet in the roller, the keys mid-strike, lamp light" + SEM],
 # N007 destrucción de una nación o grupo étnico; borrar a un pueblo
 ["empty_village|An empty village street in occupied Eastern Europe in the 1940s, open doors, abandoned belongings on the ground, no people" + FAR,
  "empty_synagogue|The interior of an abandoned wooden synagogue in Eastern Europe, empty benches, dust in the light, no people",
  "erased_portraits|A wall of old framed family portraits with several frames empty, dim light",
  f"lemkin_window|{LEMKIN} standing at a window in Washington at night, looking out, 1944"],
 # N008 Churchill por radio: crimen sin nombre; ahora el nombre existe
 [f"churchill_radio|{CHURCH} speaking into a 1940s radio microphone without any lettering at a desk, 1941",
  "radio_listeners|A family listening to a wooden radio in a dim living room in 1941",
  "word_on_paper|Close-up of a sheet of paper with one single handwritten word, " + ILEG + ", lamp light"],
 # N009 falta un tribunal; otro jurista busca otra palabra; misma universidad
 ["empty_courtroom|An empty grand courtroom in shadow, empty judges' bench, dust in a beam of light" + NOINS,
  "lwow_university|The neo-classical main building of the University of Lwów in the 1920s, students with books on the steps" + SEM,
  "law_students|Law students in a 1920s European lecture hall taking notes, a professor at the lectern"],
 # N010 El Jardín. Cambridge 29/7/1945; Jackson almuerza con Lauterpacht; jardín
 ["cambridge_1945|A quiet Cambridge street in summer 1945, brick houses with gardens, bicycles",
  f"lunch_table|{JACKSON} and {LAUT} sitting at a modest lunch table in an English dining room, 1945, conversation",
  f"garden_walk|{JACKSON} and {LAUT} walking in a small English garden in summer 1945, talking seriously@@ROBERT JACKSON",
  f"laut_portrait|Medium shot of {LAUT} in his garden, thoughtful, 1945@@HERSCH LAUTERPACHT"],
 # N011 Sands; Jackson pide ayuda: cómo llamar lo que hicieron con millones de civiles
 ["sands_book|A modern hardcover history book lying on a wooden table beside an old photograph" + SEM,
  f"jackson_question|Close-up of {JACKSON} speaking with an open hand, in a garden, 1945",
  "civilians_deported|A long line of civilians with bundles walking along a railway in the 1940s, guards in the distance" + FAR + NOINS,
  "garden_bench|An empty garden bench under an apple tree in an English garden, summer light"],
 # N012 crímenes contra la humanidad
 [f"laut_speaks|{LAUT} speaking calmly, one finger raised, garden behind him, 1945",
  "notebook_phrase|A small notebook open on a garden table with a short handwritten phrase, " + ILEG],
 # N013 Leópolis/Lemberg; Lemkin también; familia de Lauterpacht asesinada
 ["lwow_street|A street of Lwów in the 1930s, trams, baroque facades, people in coats" + SEM,
  "lwow_empty|The same kind of city street in Lwów in 1943, empty and grey, shutters closed, no people",
  "laut_family_photo|An old family photograph of a 1930s Jewish family on a table, faces soft and indistinct, a candle beside it"],
 # N014 Hans Frank gobernó la Polonia ocupada
 [f"frank_portrait|{FRANK}, cold expression, standing in an ornate castle office, 1941" + NOINS + "@@HANS FRANK",
  "krakow_castle|The Wawel castle in Kraków in 1941 under a grey sky" + NOINS],
 # N015 diez días después; documento firmado por cuatro potencias
 ["four_pens|Four fountain pens lying beside a bound treaty document on a conference table, " + ILEG,
  "london_1945|London in August 1945, a government building on a sunny day, people passing, bomb damage on one side" + SEM],
 # N016 La Carta. Londres, agosto 1945; artículo ocho; órdenes no libran
 ["charter_doc|A typed legal charter of 1945 on a desk, one paragraph marked with a thin red line in the margin, " + ILEG,
  "conference_room|A London conference room in 1945, four delegations of lawyers around a long table" + NOINS,
  "officer_orders|A German officer at a desk handing a typed order to a subordinate, 1942, faces in shadow" + NOINS + ", " + ILEG,
  "order_paper|Close-up of a typed military order with an official stamp, " + ILEG + NOINS],
 # N017 reducir la pena; firman el 8/8; tres crímenes
 ["signing_table|Hands signing a document with a fountain pen at a conference table, 1945, other hands waiting with pens" + SEM,
  "four_delegates|Four lawyers in suits standing for a formal photograph in a London office, 1945" + NOINS,
  "scales_justice|A bronze statue of Justice with scales in a dim hall",
  "three_folders|Three brown case folders lying side by side on a dark desk, a red string around each" + SEM],
 # N018 diecinueve países; Venezuela, Uruguay, Paraguay, Panamá, Honduras, Haití
 ["latam_map|" + MAPA + ", showing Central America, the Caribbean and South America",
  "telegrams|A stack of diplomatic telegrams of 1945 on a desk, " + ILEG,
  "embassy_desk|A Latin American diplomat in 1945 signing a document at a desk in an embassy office" + NOINS + SEM],
 # N019 guarda la regla; Buenos Aires 42 años; la regla necesita una sala
 ["buenos_aires_1987|Buenos Aires in 1987, the Congress building dome at dusk, traffic" + SEM,
  "rule_page_turn|A hand turning a page of a law book upside down on a desk, " + ILEG,
  "palace_justice|The Nuremberg Palace of Justice in 1945, a large stone building standing intact among ruins" + NOINS + SEM,
  "courtroom_door|Tall wooden double doors of a courtroom, closed, 1945"],
 # N020 La Sala. verano 1945; Kiley recibe un encargo: preparar la sala 600
 [f"kiley_portrait|{KILEY} standing in a dusty large room holding rolled blueprints, 1945@@DAN KILEY",
  "blueprints|Architectural blueprints of a courtroom spread on a table with a T-square and pencils, " + ILEG,
  "palace_justice#detalhe-centro", f"kiley_walk|{KILEY} walking through the bomb-damaged corridors of a large stone courthouse with an American officer, 1945"],
 # N021 arquitecto; inteligencia; sala demasiado pequeña
 [f"kiley_drawing|{KILEY} drawing at a drafting table, 1945",
  "small_courtroom|An old wood-panelled German courtroom of modest size before renovation, 1945, empty"],
 # N022 derriba una pared; techo; cabinas de vidrio; galería 250 periodistas
 ["wall_demolition|Workers knocking down a wall inside a large wood-panelled hall, dust in the air, 1945" + NOINS,
  "glass_booths|Glass booths being installed in the corner of a large courtroom, 1945, workmen with tools",
  "press_gallery|A long press gallery with rows of seats for journalists in a courtroom, 1945, empty"],
 # N023 presos ex-SS y civiles; butacas de terciopelo rojo de un cine
 ["workers_prisoners|Workmen in plain grey prisoner clothing carrying planks in a courtroom under construction, a US guard watching, 1945" + NOINS,
  "red_seats|A row of red velvet cinema seats being carried into a courtroom, 1945", "cinema_ruin|A half-ruined German cinema auditorium in 1945 with rows of red velvet seats, daylight through a broken roof"],
 # N024 lo iba a mirar el mundo; la primera palabra importante en francés
 ["film_lights|Large film spotlights mounted high on a courtroom wall, switched on, 1945",
  "court600_wide#detalhe-alto", "camera_booth|A film cameraman behind a large 1940s camera inside a glass booth high on a courtroom wall"],
 # N025 El Micrófono. 20/11/1945; Pierre Mounier lee el cargo de crímenes de guerra
 [f"mounier_mic|{MOUNIER} standing at a wooden lectern reading a document into a 1940s microphone, courtroom behind in shadow, lit by a strong white spotlight from above@@PIERRE MOUNIER",
  "indictment_page|A typed indictment page of 1945 held in hands at a lectern, " + ILEG,
  "defendants_listen|Two rows of defendants in a 1945 courtroom listening with headphones, seen from behind and far away, military police in white helmets" + NOINS],
 # N026 la palabra de Lemkin: genocidio; judíos, polacos y gitanos
 [f"mounier_close|Close-up of {MOUNIER} speaking into the microphone, serious",
  "victims_memorial|A memorial wall of thousands of small candles in the dark",
  "lemkin_writing#detalhe-centro"],
 # N027 en otras tres lenguas; detrás de un vidrio, intérpretes de Dostert
 ["interpreters_booth|Interpreters with headphones speaking into microphones inside a glass booth in a 1945 courtroom, seen from the side",
  "headphones_desk|A pair of black 1940s bakelite headphones on a courtroom desk"],
 # N028 Dostert; 700 candidatos; uno de cada veinte; ONU
 [f"dostert_portrait|{DOSTERT} interviewing a candidate across a desk, 1945@@LÉON DOSTERT",
  "candidates_line|A line of men and women waiting on chairs in a corridor for an interview, 1945",
  "un_hall|A large international assembly hall of the late 1940s, delegates with headphones at long curved desks" + NOINS + SEM],
 # N029 acusación contra quien acusa; un abogado alemán, un cuestionario
 ["questionnaire|A typed questionnaire on a desk with numbered questions, " + ILEG,
  "mounier_mic#detalhe-alto", f"kranz_desk|{KRANZ} at a desk at night writing questions on a typewriter, 1946"],
 # N030 El Cuestionario. 11/5/1946; preguntas por escrito a Nimitz
 [f"nimitz_desk|{NIMITZ} reading a typed sheet at a desk in a naval office, 1946@@CHESTER NIMITZ",
  "navy_officer|A US Navy officer in plain uniform without insignia handing papers across a desk, 1946",
  "pacific_fleet|US warships in a line on the Pacific Ocean in 1944, seen from far away"],
 # N031 Kranzbühler, abogado de Dönitz; hundir barcos sin aviso
 [f"kranz_portrait|{KRANZ} standing in a courtroom with a folder, 1946@@OTTO KRANZBÜHLER",
  f"donitz_dock|{DONITZ} sitting in the dock of a 1946 courtroom with headphones, expressionless" + NOINS + "@@KARL DÖNITZ",
  "uboat_sea|A submarine on the surface of a grey Atlantic sea at dawn" + FAR + NOINS],
 # N032 Nimitz bajo juramento: 7/12/1941 guerra submarina irrestricta contra Japón
 [f"nimitz_oath|{NIMITZ} raising his right hand to take an oath in an office, 1946",
  "sub_pacific|An American submarine sailing on a calm Pacific sea at sunset" + FAR + NOINS,
  "answer_sheet|A typed answer sheet with a signature at the bottom, " + ILEG],
 # N033 la sentencia cita; orden británica 1940; pena no se fija por esas violaciones; diez años
 ["judges_bench|The judges' bench of a 1946 courtroom seen from below, four empty high-backed chairs" + NOINS,
  "british_order|A typed British Admiralty order of 1940 on a desk, " + ILEG,
  "donitz_dock#médio-dir", "sentence_quote|Close-up of a typed paragraph in a bound judgment with one sentence marked by a thin red line in the margin, " + ILEG],
 # N034 solo juzga a los vencidos; vencedores con expedientes; en octubre su palabra
 ["two_folders|Two stacks of case folders on a desk, one tall and one short, lamp light" + SEM,
  "court600_wide#médio-esq",
  "lemkin_chair#detalhe-centro", "victors_vanquished|Two empty chairs facing each other across a bare table in a dim room, one in light and one in shadow", "scales_justice#detalhe-alto"],
 # N035 El Hotel. octubre 1946; Grand Hotel; King lo vio muy afectado
 ["grand_hotel|The facade of a large old hotel in Nuremberg in 1946, partly damaged, US jeeps parked in front" + SEM + NOINS,
  "king_sees#médio-dir",
  "lemkin_close#detalhe-alto", f"king_portrait|{KING} in a hotel corridor, looking back over his shoulder, 1946@@HENRY T. KING"],
 # N036 sentencia; 218 días; doce a muerte, Bormann ausente; tres absueltos
 ["judge_reading|A judge in a dark robe reading a verdict at the bench of a 1946 courtroom under bright lights" + NOINS,
  "empty_dock_seat|An empty seat in the front row of a courtroom dock, 1946",
  "defendants_listen#detalhe-centro", "verdict_audience|The press gallery of a 1946 courtroom full of journalists taking notes, headphones on" + NOINS],
 # N037 diez condenas el 16/10; Göring la noche anterior
 ["prison_corridor|A long dim prison corridor with closed cell doors at night, 1946, a guard far away",
  "cell_door|A closed prison cell door with a small square hatch, night, 1946"],
 # N038 crímenes contra la humanidad solo ligados a la guerra; lo de antes fuera; genocidio ni una vez
 ["judgment_pages#detalhe-alto",
  "broken_shop|A Jewish-owned shop with broken windows in a German city street in 1938, morning, no people" + SEM,
  "red_circle_empty#médio-esq", "cht_wording|A typed legal paragraph with the words crossed out by a single thin pencil line, " + ILEG, "pre_war_line|A long line of Jewish families with suitcases at a German railway station in 1938, guards far away" + FAR + NOINS],
 # N039 Schabas: el día más negro; su palabra entró en la sala, no en la sentencia
 [f"lemkin_dark|{LEMKIN} sitting alone in a dark hotel room, only a window light on his face, 1946",
  "court600_wide#detalhe-baixo", "night_rain_window|Rain on a hotel window at night, the lights of a ruined city blurred behind"],
 # N040 CTA: suscríbete; Núremberg no terminó en esa sala
 ["case_file#detalhe-centro",
  "courtroom_door#médio-dir", "newsroom_1946|Journalists typing fast in a crowded 1946 press room, papers everywhere" + SEM],
 # N041 El Código. 9/12/1946; juicios siguientes; tribunales militares estadounidenses
 ["doctors_trial|Defendants in a 1946 courtroom, a row of middle-aged men in plain suits, some formerly doctors, military police behind" + NOINS,
  "us_judges|Three American judges at a bench in 1946, wood panelling" + NOINS, "nuremberg_winter|The Nuremberg Palace of Justice in winter 1946, snow on the roof, guards at the gate" + NOINS + SEM],
 # N042 23 acusados médicos; experimentos sin consentimiento; muertos o mutilados
 ["medical_files|Medical files and X-ray envelopes stacked on a courtroom exhibit table, 1946, " + ILEG,
  "empty_barrack|An empty camp barrack with wooden bunks, cold light, no people" + FAR,
  "surgical_tools|Old surgical instruments laid out on a cloth in a dim room, no blood"],
 # N043 agosto 1947; 16 culpables, 7 a muerte; código de diez puntos
 ["verdict_doctors|A judge reading a verdict in a courtroom, 1947, defendants listening with headphones" + NOINS,
  "ten_points|A typed document with ten short numbered paragraphs, " + ILEG, "doctors_headphones|A row of defendants in plain suits listening with headphones in a 1947 courtroom, faces stern" + NOINS],
 # N044 consentimiento voluntario; ética médica; víctimas
 ["consent_form|A patient's hand signing a consent form on a clipboard in a modern hospital, " + ILEG,
  "ten_points#detalhe-alto", "research_lab|A modern medical research laboratory with a doctor explaining a form to a seated volunteer"],
 # N045 otra regla; Lemkin recorre pasillos, delegado por delegado
 [f"lemkin_corridor|{LEMKIN} walking alone down a long corridor of an international organization building, late 1940s, carrying a briefcase"],
 # N046 La Convención. París, 9/12/1948; ONU aprueba
 ["paris_1948|The Palais de Chaillot in Paris in December 1948, cold winter light, the Eiffel Tower behind" + SEM,
  "un_vote|Delegates raising their hands to vote in a large assembly hall in 1948" + NOINS + SEM,
  f"lemkin_assembly|{LEMKIN} watching from a gallery seat in an assembly hall, 1948, emotional"],
 # N047 definición: destruir total o parcialmente a un grupo
 ["convention_text|A printed international convention booklet of 1948 lying open, " + ILEG,
  "atlantic_map#detalhe-alto", "group_silhouettes|Silhouettes of a crowd of people of different ages standing together against a pale sky"],
 # N048 delito internacional; en vigor enero 1951
 ["un_vote#detalhe-centro",
  "seal_ribbon|A treaty document with a red wax seal and ribbon, " + ILEG, "ratification|A diplomat signing a ratification document in 1950, a small flagless desk, lamp light" + SEM],
 # N049 una ley sirve si alguien la aplica; responsables cruzaron el océano
 ["ship_port|A passenger liner leaving a European port in 1949, people at the rails, grey sky" + SEM,
  "atlantic_map#médio-esq", "ratline_map|" + MAPA + ", showing Europe, the Mediterranean and the South Atlantic down to Brazil and Argentina"],
 # N050 La Fábrica. São Bernardo, Brasil, años 60; Volkswagen; Stangl con su nombre
 ["vw_plant|A large car factory assembly line in Brazil in the 1960s, workers in overalls, rows of small beetle-shaped cars without logos" + SEM,
  f"stangl_work|{STANGL} working at a factory desk with papers, 1966@@FRANZ STANGL"],
 # N051 comandante de Sobibor y Treblinka; cientos de miles de judíos; huyó por Italia y Siria; Brasil 1951
 ["treblinka_stones|The memorial field of thousands of standing granite stones at Treblinka today, overcast sky, no people",
  "forest_rails|Railway tracks ending in a pine forest in Poland, mist, no people" + FAR,
  "rome_1948|A street in Rome in 1948, a man with a suitcase walking away" + SEM,
  "ship_brazil|A ship arriving at the port of Santos, Brazil, in 1951, tropical hills behind"],
 # N052 28/2/1967 detenido en São Paulo; Wiesenthal; extraditado en junio
 ["sp_police|Brazilian police officers in 1967 leading a grey-haired man out of a house at night" + NOINS,
  "wiesenthal_files|A cluttered office desk covered with files and index cards in Vienna, 1967, " + ILEG,
  "plane_1967|A 1960s propeller airliner on a runway at night, plain white livery without logo" + SEM],
 # N053 Düsseldorf dic 1970 perpetua; al menos 400 mil
 ["dusseldorf_court|A West German courtroom in 1970, modern wood panelling, judges in black robes" + NOINS,
  f"stangl_dock|{STANGL} older, sitting in a courtroom dock in 1970, expressionless",
  "treblinka_stones#detalhe-alto", "verdict_1970|A West German judge in a black robe reading a verdict in 1970, journalists in the gallery" + NOINS],
 # N054 murió en prisión 1971; Brasil lo entregó; en Chile otra respuesta
 ["prison_window|A barred prison window with grey light, 1971",
  "andes|The Andes mountains seen from Santiago de Chile at dusk"],
 # N055 El Plazo. Santiago 1963; extradición de Rauff
 ["santiago_1963|Downtown Santiago de Chile in 1963, the Supreme Court building, people walking" + SEM,
  "rauff_back|An elderly man in a dark suit seen from behind, walking along a street in Santiago in the 1960s@@WALTER RAUFF"],
 # N056 camiones de gas; 97 mil
 ["gray_truck|A grey 1940s closed cargo truck parked alone on a muddy road at dusk, empty, no people" + FAR,
  "candles_names|Rows of small memorial candles on a stone floor, dim light", "jta_archive|Old newspaper clippings of the 1960s spread on a desk, " + ILEG],
 # N057 Corte Suprema rechaza; prescrito; 15 años
 ["chile_court|Judges of a 1963 Chilean supreme court in black robes at a bench, wood panelling" + NOINS,
  "hourglass|An hourglass on a judge's desk with the last sand falling, " + ILEG],
 # N058 1968 ONU otra convención: no prescriben; llegó tarde
 ["un_1968|A large 1960s international assembly hall seen from the back, rows of delegates seated at curved desks under a high ceiling" + NOINS + SEM,
  "hourglass#detalhe-centro", "signature_1968|A diplomat signing a treaty at the United Nations in 1968, pen and blue folder" + SEM],
 # N059 Rauff murió libre en Santiago, 1984; en Argentina una ley
 ["santiago_house|A quiet suburban house in Santiago de Chile in the 1980s, closed gate, afternoon",
  "buenos_aires_1987#detalhe-centro", "santiago_1984|Santiago de Chile in 1984, a quiet avenue with trees and the Andes behind" + SEM],
 # N060 La Ley. Buenos Aires 1985; nueve excomandantes; secuestros, torturas, asesinatos
 ["juntas_court|A crowded Argentine federal courtroom in 1985, six judges at a high bench, defendants in suits seated in the front" + NOINS,
  "mothers_plaza|Women with white headscarves walking in a circle in the Plaza de Mayo in Buenos Aires, 1985, holding photographs" + SEM, "juntas_defendants|Former military commanders in civilian suits sitting in a row in a 1985 courtroom, seen from behind" + NOINS],
 # N061 Strassera: nunca más; cinco de los nueve condenados
 [f"strassera|{STRASS} standing and speaking in a courtroom, intense expression, 1985@@JULIO CÉSAR STRASSERA",
  "verdict_1985|Judges reading a verdict in a crowded Argentine courtroom, 1985, the audience standing" + NOINS],
 # N062 cientos de oficiales; 1986 ley pone plazo; 1987 levantamiento; Obediencia Debida
 ["officers_files|Hundreds of case files stacked on shelves in an Argentine court archive, 1986" + SEM,
  "barracks_1987|Argentine soldiers in plain uniforms with painted faces inside a military barracks, 1987, seen from far away" + NOINS,
  "congress_vote|Argentine congressmen voting in the Chamber of Deputies, 1987" + NOINS + SEM],
 # N063 presume que actuaron cumpliendo órdenes; la defensa que el art. 8 rechazó
 ["order_paper#detalhe-centro",
  "charter_doc#detalhe-alto",
  "mothers_plaza#detalhe-centro", "obedience_law|A printed law gazette of 1987 open on a desk, " + ILEG, "missing_photos|Black and white photographs of young people pinned on a board, faces soft and indistinct, white headscarves below"],
 # N064 2003 anulación; 2005 Corte Suprema; juicios reabren; palabra de Lemkin a tribunal nacional
 ["congress_2003|The Argentine Congress building in Buenos Aires in 2003, daytime, crowds outside" + SEM,
  "argentina_court_2005|Argentine supreme court justices in a formal chamber, 2005" + NOINS,
  "guatemala_map|" + MAPA + ", showing Central America and southern Mexico", "courts_reopen|People celebrating outside a courthouse in Buenos Aires in 2005, holding photographs" + SEM],
 # N065 La Jueza. Guatemala 10/5/2013; Yassmín Barrios; Ríos Montt
 [f"barrios|{BARRIOS} reading a verdict at the bench of a crowded courtroom in Guatemala City, 2013@@YASSMÍN BARRIOS",
  f"rios_montt|{RIOS} sitting at the defense table listening, 2013@@EFRAÍN RÍOS MONTT"],
 # N066 genocidio contra el pueblo maya ixil; 1.771 víctimas; 80 años
 ["ixil_women|Maya Ixil women in traditional red embroidered huipiles standing in a courtroom audience, 2013",
  "ixil_mountains|Green mountains of the Ixil region of Guatemala with mist, a small village below",
  "courtroom_2013|A courtroom in Guatemala City in 2013 full of people standing and applauding" + SEM],
 # N067 NPR: primera vez que un país condena por genocidio a un exjefe de Estado
 ["radio_studio|A modern radio studio with a microphone and headphones on a desk, red on-air light" + SEM,
  "barrios#detalhe-centro", "newspaper_2013|A stack of 2013 newspapers on a table, the front pages only as blurred photographs and grey blocks" + SEM],
 # N068 anulada 10 días después; no por inocencia; murió 2018 sin veredicto
 ["cc_guatemala|A modern constitutional court chamber in Guatemala, judges at a bench, 2013" + NOINS,
  "rios_montt#médio-dir",
  "ixil_mountains#detalhe-alto", "ixil_protest|Ixil women holding photographs of relatives outside a court in Guatemala City, 2013" + SEM],
 # N069 la palabra escrita en una sentencia de su país; 67 años
 ["judgment_pages#médio-dir",
  "lemkin_writing#detalhe-alto", "ixil_candles|Candles and flowers on a stone in a Guatemalan highland village at dusk"],
 # N070 Cierre. La Palabra. Nueva York ago 1959; Lemkin muere sin dinero
 ["ny_1959|A New York street in 1959, yellow taxis and office buildings, summer afternoon" + SEM,
  f"lemkin_old|{LEMKIN} older, about fifty-nine, sitting alone in a small cluttered apartment with books and papers, 1959", "un_building_1959|The United Nations headquarters building in New York in 1959 seen from the East River"],
 # N071 siete personas en el entierro
 ["funeral_seven|Seven people in dark clothes standing at a grave in a New York cemetery, 1959, seen from far away, grey sky"],
 # N072 Núremberg no inventó el crimen; le puso nombre; reglas en Buenos Aires y Guatemala
 ["court600_wide#aberto",
  "juntas_court#detalhe-centro",
  "courtroom_2013#médio-esq", "hague_court|The modern International Criminal Court building in The Hague on a grey day, no flags" + SEM, "gavel|A wooden judge's gavel resting on a bench under a single light"],
 # N073 el crimen era viejo; lo nuevo fue tener una palabra
 ["word_on_paper#detalhe-centro", "old_book_word|An old dictionary open on a desk with one entry lit by a beam of light, " + ILEG],
 # N074 pregunta final
 ["case_file#médio-esq",
  "red_stamp#detalhe-centro", "lemkin_portrait|Ink portrait of " + LEMKIN + ", looking straight ahead, plain dark background"],
]
_textos = [x for x in B if "t" in x]
assert len(SB) == len(_textos), f"SB {len(SB)} x blocos {len(_textos)}"
for _blk, _s in zip(_textos, SB): _blk["s"] = _s

# Thumbs (EMBALAGEM.md aprovado no crivo r3): texto (NÚREMBERG, SIN NOMBRE, HASTA AQUÍ, aba, fio e pontos do mapa) no Thumbnail.jsx.
THUMBS = [
    {"id": "thumb-A", "prompt": "Ink graphic novel illustration: a pair of 1940s black bakelite headphones with a clearly visible curved headband and two round ear cups, short coiled cord, lying alone on plain cream paper, only the top edge of a dark wooden courtroom railing at the bottom of the frame, strong black ink outlines, the headphones occupy the LEFT half of the frame, RIGHT half empty plain cream paper, no microphone, no people, no text, no letters, no numbers, absolutely NO red color, no hex codes"},
    {"id": "thumb-B", "prompt": "Ink graphic novel illustration: a 1945 courtroom, a single prosecutor in a dark suit standing at a wooden lectern reading a document aloud, seen three-quarters from behind, occupying the LEFT 40 percent of the frame, lit by one strong white spotlight from above so that the beam of light behind and around him is the brightest area of the whole image, the rest of the large courtroom in deep slate-blue shadow, only the faint outline of the judges' bench far behind, no faces visible, no flags, no insignia, no swastika, no text, no letters, no hex codes"},
    {"id": "thumb-C", "prompt": "Ink graphic novel illustration: a dark old map of the whole Atlantic Ocean in slate blue and sepia ink, Europe clearly visible at the top right, Africa at the right edge, Central America and South America at the left, the ocean filling the middle so that South America does not fill the frame, correct coastlines, no labels, no text, no letters, no lines, no arrows, no pins, no markers, no red color, no hex codes"},
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
