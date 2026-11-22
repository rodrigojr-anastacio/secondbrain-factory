#!/usr/bin/env python3
"""Fonte única do dossie-es 014 (La Yakuza): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py (na pasta do vídeo). Geração copiada do 013-nuremberg.

Embalagem aprovada no crivo r3 (21/11/2026, EMBALAGEM.md/CRIVO.md):
  A/T1 "YAKUZA: la mafia que tenía su nombre en la puerta" + letreiro arrancado, YAKUZA + sello ¿LEGAL? (objeto-simbolo, controle)
  B/T2 "Cómo la Yakuza pasó de trabajar para Japón a ser su enemiga" + 184.000 riscado sobre salão de tatame vazio, HOY 17.600 (numero-estatistica)
  C/T3 "Japón, 1992: la Yakuza tuvo que esconder su nombre" + homem em contraluz rasgando o cartão com o emblema, rótulo YAKUZA (cena-acao)
Ângulo (ANGULO.md): la mafia que no se escondía (ser yakuza nunca foi crime; o Estado a usou à vista e depois a apagou com papéis).

Sintaxe dos planos (campo s): "chave|prompt" nova · "chave" reuso · "chave#enq" reuso com enquadramento · + "@@TEXTO" rótulo.
"""
import json, math, re
from pathlib import Path

WPS = 2.38           # palavras/s medidas no 001–013 (erro de 1–3%)
BREAK, LONG = 0.35, 0.8
MAX_PLANO_INICIO = 3.0   # s por plano nos primeiros INICIO s (~20 cortes/min)
INICIO = 60.0
MAX_PLANO = 3.6      # s por plano depois (~17 cortes/min)
INEDITO_ATE = 180.0  # s: só imagens novas até aqui
JANELA = 60.0        # s: mesmo enquadramento da mesma imagem só depois disso
HOOK_MAX = 40.0      # s: EMBALAGEM: frase-âncora até 0:40
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "YAKUZA: la mafia que tenía su nombre en la puerta"
TITULOS = ("T1 YAKUZA: la mafia que tenía su nombre en la puerta / "
           "T2 Cómo la Yakuza pasó de trabajar para Japón a ser su enemiga / "
           "T3 Japón, 1992: la Yakuza tuvo que esconder su nombre")
PROMESSA = ("En Japón, ser yakuza nunca fue delito: durante un siglo la mafia tuvo oficinas con su nombre en la puerta y trabajó a la vista "
            "para ministros, gobiernos y empresas, hasta que Japón inventó leyes y contratos para borrarla de la vista; de 184.000 miembros a 17.600.")

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Tokio, mayo de mil novecientos noventa y dos. Frente a su casa, cinco hombres atacan con cuchillos al cineasta Juzo Itami.", card="TOKIO, 1992")
b("Días antes, Itami había estrenado una película que enseña a no pagarle a la yakuza.")
b("Los grupos de la yakuza tenían oficinas, emblema y tarjetas con su nombre. Pertenecer a la yakuza no era delito. Hoy tampoco.")
b("Esta es TODA la historia de la Yakuza: la mafia que no se escondía, porque trabajaba para el poder. De ciento ochenta y cuatro mil miembros y asociados… a diecisiete mil seiscientos.", ideia=True)

# ───────────────────────── 1. EL MINISTRO ─────────────────────────
cap("1. El Ministro")
b("El Ministro. Tokio, cuatro de octubre de mil novecientos diecinueve. El ministro del Interior, Takejiro Tokonami, reúne a treinta y seis grandes jefes de apuestas.", card="TOKIO, 1919")
b("Vienen de un mundo viejo de tahúres y vendedores ambulantes. Según la explicación más aceptada, su nombre sale de una de las peores manos de un juego de cartas: ocho, nueve y tres. Ya, ku, za.")
b("Un mes después nace la Gran Sociedad de la Esencia Nacional de Japón. Promete defender al emperador y combatir a los rojos. Dice tener seiscientos mil miembros. La cifra la da ella misma.")
b("Según el politólogo Masao Maruyama, sus hombres actúan como rompehuelgas y atacan a sindicatos y a campesinos.")
b("No la organiza un jefe criminal. La organiza un ministro. La próxima vez que el Estado los necesite, el intermediario saldrá de una cárcel.", ideia=True)

# ───────────────────────── 2. LA CELDA ─────────────────────────
cap("2. La Celda")
b("La Celda. Tokio, veinticuatro de diciembre de mil novecientos cuarenta y ocho. De la prisión de Sugamo salen, sin juicio, varios sospechosos de crímenes de guerra.", card="TOKIO, 1948")
b("Uno es Yoshio Kodama, ultranacionalista. Durante la guerra compró materiales en China para la Marina Imperial. Otro, ese mismo día, es Nobusuke Kishi, exministro del gobierno de guerra.")
b("Según los periodistas David Kaplan y Alec Dubro, Kodama sale con un compromiso: ayudar a la ocupación estadounidense contra los comunistas.")
b("Afuera, los mercados negros de la posguerra están en manos de bandas. En Kobe, el joven jefe Kazuo Taoka convierte al Yamaguchi-gumi en el que reparte el trabajo en el puerto.")
b("Ocho años después, Kishi es primer ministro. Y en mil novecientos sesenta, según un historiador, recurre a Kodama.", ideia=True)

# ───────────────────────── 3. LA VISITA ─────────────────────────
cap("3. La Visita")
b("La Visita. Tokio, junio de mil novecientos sesenta. El presidente Eisenhower debe llegar el diecinueve. Las calles están llenas de protestas contra el tratado de seguridad con Estados Unidos.", card="TOKIO, 1960")
b("Según el historiador Nick Kapur, el gobierno de Kishi le pide a Kodama una fuerza privada para proteger la visita.")
b("Según Kapur, el plan de movilización prevé ciento cuarenta y seis mil ochocientos setenta y nueve hombres. Son derechistas y yakuza. La policía calcula que, como mucho, podrían reunirse unos ciento veinte mil.")
b("El dieciséis de junio, el gobierno pide aplazar la visita, y la visita se cancela. Aun así, la yakuza nunca fue tan grande. En mil novecientos sesenta y tres, según cifras policiales citadas por la prensa, suma ciento ochenta y cuatro mil miembros y asociados.")
b("Ya no son tahúres de feria. Ahora están también sobre los escenarios.", ideia=True)

# ───────────────────────── 4. LA CANTANTE ─────────────────────────
cap("4. La Cantante")
b("La Cantante. Tokio, treinta y uno de diciembre de mil novecientos setenta y tres. La televisión pública NHK emite su gran concurso musical de fin de año, el Kohaku.", card="TOKIO, 1973")
b("Por primera vez en dieciocho años, no aparece Hibari Misora, la cantante más famosa del país. Ese año, su hermano había sido procesado por actividades ligadas a una organización criminal.")
b("Hibari nunca fue acusada de nada. Pero, según los periodistas Kaplan y Dubro, durante años el Yamaguchi-gumi de Kazuo Taoka se encargó de la seguridad de sus conciertos.")
b("La yakuza estaba en el escenario, a la vista de todos. Y Kodama, el hombre de la celda, ya cobraba de una empresa estadounidense que fabrica aviones.", ideia=True)

# ───────────────────────── 5. LOS RECIBOS ─────────────────────────
cap("5. Los Recibos")
b("Los Recibos. Washington, febrero de mil novecientos setenta y seis. Un subcomité del Senado de Estados Unidos investiga los pagos de la empresa Lockheed en el extranjero.", card="WASHINGTON, 1976")
b("Aparece un nombre japonés: Yoshio Kodama, su asesor secreto en Japón. Según la revista Time, recibió más de siete millones de dólares desde mil novecientos sesenta.")
b("Entre los papeles hay recibos por unos dos millones de dólares, de noviembre de mil novecientos setenta y dos. Ese mismo mes, la aerolínea japonesa ANA acepta comprar aviones TriStar de Lockheed por ciento treinta millones.")
b("El escándalo alcanzará al ex primer ministro Kakuei Tanaka, detenido en julio. Kodama, convaleciente de un derrame cerebral, se queda en su casa de Tokio. Hasta allí va a buscarlo un avión.", ideia=True)

# ───────────────────────── 6. EL AVIÓN ─────────────────────────
cap("6. El Avión")
b("El Avión. Tokio, veintitrés de marzo de mil novecientos setenta y seis. Mitsuyasu Maeno, actor de veintinueve años, alquila una avioneta Piper en el aeródromo de Chofu.", card="TOKIO, 1976")
b("Va vestido de piloto kamikaze, con la cinta del sol naciente en la frente. Sobrevuela el barrio de Setagaya y da dos vueltas sobre la casa de Kodama.")
b("Después se lanza contra ella, gritando vivas al emperador. El avión choca contra el segundo piso. Maeno muere. Kodama, en otra habitación, sale ileso.")
b("Maeno también era ultranacionalista. Según la prensa de la época, se sentía traicionado: su ídolo cobraba de una empresa extranjera.")
b("El padrino de los nacionalistas, el amigo de los ministros, queda a la vista de todo el país. En los años ochenta, una guerra por la sucesión del Yamaguchi-gumi deja al menos treinta y seis muertos, según el periodista David Kaplan. Y Japón decide mirar a la yakuza de otra manera.", ideia=True)

# ───────────────────────── 7. EL LETRERO ─────────────────────────
cap("7. El Letrero")
b("El Letrero. Japón, primero de marzo de mil novecientos noventa y dos. Entra en vigor la ley contra los grupos violentos. No prohíbe ser yakuza.", card="JAPÓN, 1992")
b("Las comisiones de seguridad pública de cada prefectura pueden designar a un grupo como violento. Sus miembros no pueden, por ejemplo, exigir dinero en nombre del grupo.")
b("Hasta entonces, el nombre del grupo estaba en la puerta y en las tarjetas de visita. Según el Libro Blanco de la Policía de ese año, de ciento ocho oficinas del Yamaguchi-gumi revisadas, cuarenta y una quitan el letrero y el emblema. Y hay jefes que borran el nombre del grupo de sus tarjetas.")
b("En mayo, Juzo Itami estrena su película. Días después llegan los cinco hombres. En noviembre, el Yamaguchi-gumi, ya el mayor del país, demanda a la comisión de Hyogo para anular su designación. Después retira la demanda.")
b("Itami tarda tres meses en recuperarse y vuelve a filmar. Dos de sus atacantes reciben penas de seis y cinco años. En mil novecientos noventa y siete, Itami muere al caer de un edificio. La policía concluye que fue un suicidio. El periodista Jake Adelstein sostiene otra versión, que nunca se ha probado.", ideia=True)
b("Si te interesan estos expedientes, suscríbete. Porque la ley tenía un límite: las grandes empresas seguían pagando.")

# ───────────────────────── 8. LA ASAMBLEA ─────────────────────────
cap("8. La Asamblea")
b("La Asamblea. Japón, veintisiete de junio de mil novecientos noventa y siete. Dos mil trescientas cincuenta y cinco empresas celebran su junta de accionistas el mismo día.", card="JAPÓN, 1997")
b("No es casualidad. Así se defienden de los sokaiya: extorsionistas que compran unas pocas acciones y amenazan con reventar la junta con escándalos si no se les paga. Según la policía, muchos trabajan con la yakuza.")
b("Con todas las juntas a la vez, los sokaiya no pueden estar en todas. Ese mismo mes, la fiscalía investiga al banco Dai-Ichi Kangyo, uno de los mayores del país, por préstamos a un sokaiya, Ryuichi Koike.")
b("Su expresidente del consejo, Tadashi Okuda, será condenado, con pena suspendida, por un préstamo ilegal de once mil ochocientos millones de yenes. Los bancos también pagaban. Y en Estados Unidos, el FBI hará su propio trato.", ideia=True)

# ───────────────────────── 9. EL HÍGADO ─────────────────────────
cap("9. El Hígado")
b("El Hígado. Los Ángeles, julio de dos mil uno. En el hospital de la Universidad de California, un paciente japonés recibe un trasplante de hígado.", card="LOS ÁNGELES, 2001")
b("Es Tadamasa Goto, jefe del Goto-gumi, el grupo de los hombres que atacaron a Itami.")
b("Según el diario Los Angeles Times, Goto entró en Estados Unidos con una visa obtenida con ayuda del FBI, a cambio de información sobre la yakuza. Él y otro yakuza donaron cien mil dólares al hospital.")
b("Un exjefe de la unidad asiática del FBI dijo después que el FBI no le consiguió la operación y que Goto no entregó nada importante. En dos mil ocho, el Yamaguchi-gumi lo expulsa. En dos mil nueve, Goto se ordena sacerdote budista.")
b("En casa, el poder ya no los protege. Algunos buscan negocio mucho más lejos. Hasta Sudamérica.", ideia=True)

# ───────────────────────── 10. EL AEROPUERTO ─────────────────────────
cap("10. El Aeropuerto")
b("El Aeropuerto. Buenos Aires, veintisiete de marzo de dos mil diez. En Ezeiza, la policía detiene a un japonés que embarca hacia su país con tres kilos de cocaína.", card="BUENOS AIRES, 2010")
b("Se llama Hirasawa. Según contó después a la revista InSight Crime, pasó unos treinta años en la yakuza, casi todos en el Yamaguchi-gumi. Había venido a Sudamérica a comprar droga para venderla en Japón.")
b("Lo condenan a cuatro años y nueve meses. Año y medio después, la sentencia se anula y lo deportan.")
b("En dos mil veinticuatro, la policía japonesa detiene a un alto miembro del Sumiyoshi-kai, de setenta y seis años, por unos quince kilos de droga estimulante enviados desde México. Se investiga un vínculo con un cártel. No está probado.")
b("En Japón, el cerco ya no lo pone solo la policía. Lo ponen los contratos.", ideia=True)

# ───────────────────────── 11. EL CONTRATO ─────────────────────────
cap("11. El Contrato")
b("El Contrato. Tokio, veintitrés de agosto de dos mil once. Shinsuke Shimada, uno de los presentadores más famosos de la televisión japonesa, anuncia que se retira. Admite su relación con un yakuza.", card="TOKIO, 2011")
b("Poco más de un mes después, el primero de octubre, Tokio y Okinawa completan la lista: las cuarenta y siete prefecturas ya tienen ordenanzas contra la yakuza.")
b("Las empresas no pueden pagarles ni ayudarlos a sabiendas. En los contratos aparece una cláusula: quien firma declara no pertenecer a un grupo violento.")
b("El Estado que la había usado ya no necesita prohibirla. Le basta con que nadie firme con ella. Diez años después, un tribunal va más lejos.", ideia=True)

# ───────────────────────── 12. LA SENTENCIA ─────────────────────────
cap("12. La Sentencia")
b("La Sentencia. Fukuoka, veinticuatro de agosto de dos mil veintiuno. Un tribunal condena a muerte a Satoru Nomura, jefe del Kudo-kai, el único grupo de Japón designado como especialmente peligroso.", card="FUKUOKA, 2021")
b("Lo declara responsable de ordenar cuatro ataques contra ciudadanos. Entre ellos, el asesinato en mil novecientos noventa y ocho del exjefe de una cooperativa de pescadores. Es la primera pena de muerte para un jefe de la yakuza.")
b("Según la prensa, Nomura le advierte al juez que se arrepentirá de esto toda su vida. En dos mil veinticuatro, un tribunal superior lo absuelve de ese asesinato y cambia la pena por cadena perpetua. El caso sigue en el Supremo.")
b("Nomura había gobernado su grupo desde una sede con su emblema, en Kitakyushu. Esa puerta ya no existe.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. La Puerta")
b("La Puerta. Kitakyushu, noviembre de dos mil diecinueve. La ciudad, un centro contra la yakuza, el dueño del edificio y el propio Kudo-kai firman un acuerdo: la sede se derribará. El terreno termina en manos de una organización que ayuda a personas sin hogar.", card="KITAKYUSHU, 2019")
b("A finales de dos mil veinticinco, según la Agencia Nacional de Policía, la yakuza suma diecisiete mil seiscientos miembros y asociados. En mil novecientos sesenta y tres eran ciento ochenta y cuatro mil.")
b("Juzo Itami enseñó en una película a cerrarle la puerta a la yakuza. Mucho antes, se la habían abierto un ministro en mil novecientos diecinueve, un primer ministro en mil novecientos sesenta y las grandes empresas.")
b("La yakuza nunca se escondió del poder. Se escondió cuando el poder dejó de necesitarla.", ideia=True)
b("Y tú, ¿quién crees que necesitaba más al otro: la yakuza al Estado, o el Estado a la yakuza? Déjalo en los comentarios.")

# ───────────────────────── STORYBOARD (planos por bloco, na ordem dos blocos) ─────────────────────────
SEM = ", no lettering anywhere, every sign blank"
NOINS = ", no flags, no insignia, no badges, no emblems, no armbands, no medals"
FAR = ", seen from far away, no bodies, no blood"
ILEG = "the writing only as faint completely illegible blurred lines, no readable letters"
BLANK = "completely blank sheets of paper, no writing at all"
NOTAT = ", no tattoos visible, long sleeves"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame, no ocean names"
# Personagens ("resembling", nunca foto; sem insígnias; adultos realistas)
ITAMI = "a Japanese film director of about fifty-nine in 1992 resembling Juzo Itami, glasses, short grey hair, casual jacket"
TOKO = "a Japanese politician of about fifty-three in 1919 resembling Tokonami Takejiro, moustache, dark Western frock coat"
BOSS19 = "Japanese gambling bosses of 1919 in dark kimono and haori jackets"
KODAMA48 = "a lean Japanese man of about thirty-seven in 1948 resembling Yoshio Kodama, shaved head, plain dark civilian coat"
KODAMA60 = "a Japanese man of about forty-nine in 1960 resembling Yoshio Kodama, shaved head, dark suit, stern face"
KODAMA76 = "an elderly Japanese man of about sixty-five in 1976 resembling Yoshio Kodama, shaved head, grey kimono"
KISHI = "a thin Japanese man of about fifty-two in 1948 resembling Nobusuke Kishi, prominent ears, plain dark civilian coat"
KISHI60 = "a Japanese prime minister of about sixty-three in 1960 resembling Nobusuke Kishi, prominent ears, dark suit"
TAOKA = "a Japanese man of about thirty-three in 1946 resembling Kazuo Taoka, short hair, round face, open-collar shirt and dark jacket"
EISEN = "a man resembling Dwight D. Eisenhower in 1960, bald, smiling, dark suit"
HIBARI = "a Japanese female singer of about thirty-six in 1973 resembling Hibari Misora, short dark hair, elegant kimono"
TANAKA = "a Japanese politician of about fifty-eight in 1976 resembling Kakuei Tanaka, glasses, toothbrush moustache, dark suit"
MAENO = "a young Japanese man of about twenty-nine in 1976, short hair, wearing a WWII-style leather flying helmet and goggles, a plain white headband with a red sun circle, plain flight jacket without insignia"
GOTO = "a Japanese man of about fifty-nine in 2001 resembling Tadamasa Goto, short grey hair, glasses, dark suit, stern face"
HIRA = "a middle-aged Japanese man in a plain dark jacket" + NOTAT
SHIMADA = "a Japanese TV presenter of about fifty-five in 2011 resembling Shinsuke Shimada, dark suit, serious face"
NOMURA = "a Japanese man of about seventy-four in 2021 resembling Satoru Nomura, short grey hair, plain dark suit"
OKUDA = "a Japanese banker of about sixty-seven in 1997, grey hair, glasses, dark suit"
YAKU92 = "Japanese men in dark suits of 1992, short hair, plain lapels" + NOTAT

SB = [
 # N001 Tokio 1992, cinco hombres atacan a Itami frente a su casa
 ["itami_street|Night, a narrow residential street in Setagaya, Tokyo, in 1992, a low wall and the gate of a modest two-storey house lit by one warm street lamp, wet asphalt" + SEM,
  f"itami_walk|{ITAMI} walking home at night along a quiet Tokyo residential street in 1992, lit by a street lamp" + SEM,
  "five_shadows|Five long dark shadows of men stretching across a wet Tokyo street at night toward a house gate, only the shadows visible, no faces" + FAR + SEM],
 # N002 película que enseña a no pagarle a la yakuza
 [f"itami_set|{ITAMI} directing on a film set in 1992, holding a script, a heavy film camera on a tripod beside him, studio lights",
  "cinema_1992|A Japanese cinema entrance in 1992 at dusk with people queuing, a large blank film poster frame, warm lobby lights" + SEM,
  "film_reel|Close-up of a 35mm film reel and canister on a wooden editing table, warm lamp light" + SEM],
 # N003 oficinas, emblema y tarjetas; no era delito
 ["office_front|A small Japanese gang office front in 1992: a dark wooden door, a tall vertical blank wooden signboard beside it, a blank round emblem plate above the door, a security camera, daytime" + SEM,
  "business_card|Extreme close-up of a white business card held between two fingers of a man in a dark suit, a small blank round emblem in the corner, " + ILEG,
  "emblem_plate|Close-up of a round polished metal emblem plate mounted on a dark wooden door, the plate abstract geometric and blank, no letters, no kanji",
  "law_book|A thick Japanese law code book lying open on a desk, a magnifying glass on it, " + ILEG],
 # N004 TODA la historia; trabajaba para el poder; 184.000 → 17.600
 ["case_file|A brown cardboard case folder on a dark desk under a lamp, a red rubber stamp beside it" + SEM,
  "red_stamp|A hand slamming a red rubber stamp onto a brown paper case file, dramatic close-up" + SEM,
  "diet_building|The National Diet Building in Tokyo at dusk, grey sky, seen from the avenue" + SEM,
  "tatami_full|A large traditional Japanese meeting hall in the 1960s filled with rows of men in dark suits kneeling on cushions, seen from behind, faces not visible" + NOTAT + SEM,
  "tatami_empty|The same large traditional Japanese meeting hall today completely empty, rows of empty cushions on the tatami, cold light" + SEM],
 # N005 El Ministro. Tokio 1919; Tokonami reúne a 36 jefes
 [f"toko_office|{TOKO} standing in a Western-style ministry office in Tokyo in 1919, tall windows, heavy desk" + SEM + "@@TAKEJIRO TOKONAMI",
  f"toko_meeting|{TOKO} at the head of a long table, facing {BOSS19} seated along both sides, Tokyo 1919, gas lamps" + SEM,
  "bosses_arrive|Japanese men in dark kimono and haori arriving by rickshaw at a Western-style government building in Tokyo, 1919, autumn" + SEM,
  "tokyo_1919|A Tokyo street in 1919 with trams, rickshaws and men in bowler hats and kimono" + SEM],
 # N006 mundo viejo de tahúres y vendedores; 8-9-3
 ["gambling_den|An Edo-period gambling den at night, men in kimono kneeling around a white cloth, dice cups, lantern light" + NOTAT + SEM,
  "festival_stalls|Street vendors at a Japanese temple festival in the 1800s, wooden stalls, paper lanterns, crowds" + SEM,
  "hanafuda_cards|Close-up of three traditional Japanese playing cards face up on a dark wooden table, simple abstract patterns, no numbers, no letters",
  "dice_cup|Close-up of a bamboo dice cup lifted over two dice on a white cloth, lantern light",
  "lantern_alley|A narrow Edo-period alley at night with paper lanterns, men in kimono walking away" + SEM,
  "tahur_hands|Close-up of old weathered hands shuffling small traditional playing cards on a wooden floor, lantern light"],
 # N007 Gran Sociedad de la Esencia Nacional; emperador; 600 mil
 ["society_founding|A crowded hall in Tokyo in 1919, rows of men in kimono and suits listening to a speaker at a podium, a plain white banner without writing" + SEM + NOINS,
  "imperial_palace|The moat and stone walls of the Imperial Palace in Tokyo in 1919, pine trees, grey sky" + SEM,
  "membership_ledger|A thick 1919 membership ledger open on a desk, columns of " + ILEG + ", an ink brush beside it",
  "society_march|Men in dark kimono and headbands marching in a Tokyo street in 1920" + FAR + SEM],
 # N008 rompehuelgas, sindicatos, campesinos
 ["strike_factory|Striking workers gathered outside a Japanese factory gate in 1920, plain cloth banners without writing" + SEM,
  "strikebreakers|Men in dark kimono with wooden staves confronting a crowd of workers outside a factory in 1920" + FAR + SEM,
  "farmers_field|Japanese tenant farmers in 1920 standing in a rice field facing men in dark coats on the dyke" + FAR],
 # N009 no un jefe criminal: un ministro; intermediario saldrá de una cárcel
 ["toko_portrait|Portrait of " + TOKO + ", stern, in his ministry office, side light",
  "prison_gate|The high grey walls and iron gate of Sugamo Prison in Tokyo in the late 1940s, winter, a US Army jeep parked outside" + SEM + NOINS,
  "cell_bars|Inside a bare prison cell in 1948, a thin mattress, light through the barred window" + SEM],
 # N010 La Celda. Tokio 24/12/1948; Sugamo; salen sin juicio
 ["sugamo_exit|Winter morning, 24 December 1948, the gate of Sugamo Prison opening, several Japanese men in civilian coats walking out" + SEM + NOINS + "@@PRISIÓN DE SUGAMO",
  "gi_guard|An American military policeman seen from behind at a prison gate in 1948, plain helmet, arms down" + NOINS,
  "release_papers|A desk in a prison office in 1948, release forms and a fountain pen, " + BLANK,
  "winter_road|A frosty road outside Tokyo in December 1948, bare trees, a black car waiting" + SEM],
 # N011 Kodama ultranacionalista; compró materiales en China para la Marina; Kishi
 [f"kodama48|{KODAMA48} walking out of a prison gate, looking straight ahead, winter 1948@@YOSHIO KODAMA",
  "china_warehouse|A wartime warehouse in Shanghai in the early 1940s full of crates of metals and supplies, Japanese civilians checking lists" + SEM,
  "crates_tungsten|Close-up of open wooden crates of grey metal ore in a dim warehouse" + SEM,
  f"kishi48|{KISHI} walking out of a prison gate on a cold morning, 1948@@NOBUSUKE KISHI"],
 # N012 Kaplan y Dubro: compromiso, ocupación contra comunistas
 ["occupation_hq|The Dai-Ichi Life building in Tokyo in 1948 used as the occupation headquarters, American cars outside" + SEM + NOINS,
  "officer_desk|An American intelligence officer in a plain khaki shirt without insignia at a desk in 1948, talking to a Japanese man in a civilian coat, cigarette smoke",
  "red_flags_far|A leftist rally in Tokyo in 1948 with plain red flags without symbols" + FAR + SEM],
 # N013 mercados negros; Taoka y el puerto de Kobe
 ["black_market|A crowded postwar black market under railway tracks in Tokyo in 1946, makeshift stalls, people in worn coats" + SEM,
  "market_men|Men in loose suits standing guard at the entrance of a postwar black market in 1946, arms crossed" + NOTAT + SEM,
  f"taoka_port|{TAOKA} standing on a dock at the port of Kobe in 1946, dockworkers unloading cargo behind him@@KAZUO TAOKA",
  "kobe_docks|Dockworkers carrying sacks off a cargo ship at Kobe port in the late 1940s, cranes, grey sky" + SEM],
 # N014 Kishi primer ministro; 1960 recurre a Kodama
 [f"kishi_pm|{KISHI60} speaking at a podium in the Diet in 1957, microphones" + SEM + NOINS,
  f"kodama60|{KODAMA60} sitting at a low table in a traditional room, smoking, 1960",
  "phone_1960|Close-up of a black 1960 telephone on a lacquered table, a hand lifting the receiver" + SEM],
 # N015 La Visita. junio 1960, Eisenhower debe llegar; protestas Anpo
 ["anpo_protest|Massive crowds of protesters filling the streets around the Diet building in Tokyo in June 1960, plain banners without writing" + FAR + SEM + "@@TOKIO, JUNIO DE 1960",
  f"eisen_portrait|Portrait of {EISEN}, 1960, official setting" + NOINS + "@@DWIGHT EISENHOWER",
  "students_line|Japanese university students in white shirts linking arms in a street protest in 1960" + SEM,
  "riot_police|A line of Japanese riot police with plain helmets and shields facing protesters in Tokyo, 1960" + FAR + NOINS],
 # N016 Kapur: Kishi pide a Kodama una fuerza privada
 [f"kishi_kodama|{KISHI60} and {KODAMA60} talking quietly in a dim traditional Japanese room, low table, sake cups" + SEM,
  "kapur_book|A history book lying open on a desk, footnotes, " + ILEG + ", reading glasses beside it",
  "airport_1960|Haneda Airport in 1960, an empty welcome area with ropes and a red carpet, rain" + SEM],
 # N017 plan 146.879 hombres; policía 120 mil
 ["mobilization_plan|A typed mobilization plan from 1960 on a desk, tables of numbers rendered as " + ILEG + ", a pencil and an ashtray",
  "men_trucks|Rows of trucks full of men in dark work clothes and headbands lined up in a Tokyo street at dawn, 1960" + FAR + SEM,
  "police_count|A Japanese police officer in 1960 at a desk with a mechanical adding machine and stacks of papers" + NOINS + SEM,
  "crowd_men|A dense crowd of men in dark clothes waiting along a Tokyo avenue in 1960" + FAR + SEM],
 # N018 aplazar la visita; cancelada; 1963 184.000
 ["cancel_telegram|A 1960 telegram lying on a desk under a lamp, " + ILEG,
  "empty_carpet|An empty red carpet at an airport in the rain, rolled-up ropes, no one there, 1960",
  "eisen_plane|A 1960 propeller airliner turning away over the sea, grey clouds, plain fuselage without any logo" + SEM,
  "hall_1963|A 1963 gathering of hundreds of Japanese men in dark suits in a banquet hall, seen from the balcony, faces small and indistinct" + NOTAT + SEM],
 # N019 ya no tahúres; escenarios
 ["stage_lights|An empty Japanese concert stage in the late 1960s, a single microphone stand under a spotlight, red curtain",
  "audience_1970|A packed concert hall audience in Japan around 1970 seen from the stage, warm light"],
 # N020 La Cantante. 31/12/1973 NHK Kohaku
 ["nhk_hall|A large Japanese TV concert hall on New Year's Eve 1973, a bright stage split into red and white sides, TV cameras" + SEM + "@@NHK, 31 DE DICIEMBRE DE 1973",
  "tv_family|A Japanese family in 1973 watching a TV broadcast of a music show in their living room, kotatsu table" + SEM,
  "tv_cameras|Heavy 1970s television studio cameras pointed at a stage, technicians with headsets" + SEM],
 # N021 no aparece Hibari; hermano procesado
 [f"hibari_portrait|Portrait of {HIBARI} on stage under a spotlight, holding a microphone, 1973@@HIBARI MISORA",
  "empty_chair|An empty chair with a folded kimono on it in a dressing room backstage, mirror with bulbs",
  "court_1973|A Japanese courtroom in 1973, a defendant in a dark suit standing before the judges, seen from behind" + SEM + NOINS],
 # N022 nunca acusada; Kaplan y Dubro: seguridad de los conciertos
 [f"hibari_stage|{HIBARI} singing on a large stage in the 1960s, an orchestra behind her",
  "security_men|Japanese men in dark suits and sunglasses standing at the side of a concert stage in the 1960s, arms crossed" + NOTAT,
  "concert_crowd|A crowd of fans outside a Japanese concert hall in the 1960s, men in dark suits holding them back" + SEM],
 # N023 yakuza en el escenario; Kodama cobra de empresa de aviones
 [f"kodama_money|{KODAMA60} counting stacks of banknotes at a low table, 1960s, lamp light",
  "tristar_hangar|A large wide-body jet airliner of the early 1970s with three engines in a hangar, plain white fuselage without any logo or lettering" + SEM,
  "us_office|An American corporate office in the 1970s, a man in a suit signing papers, aircraft models on the shelf" + SEM],
 # N024 Los Recibos. Washington 1976, subcomité del Senado, Lockheed
 ["senate_hearing|A US Senate subcommittee hearing room in February 1976, senators behind a long dais, witnesses at a table with microphones" + SEM + "@@WASHINGTON, 1976",
  "capitol|The US Capitol in Washington on a winter day in 1976" + SEM,
  "documents_box|A cardboard box overflowing with subpoenaed documents on a hearing room table, " + ILEG],
 # N025 Kodama asesor secreto; Time: más de 7 millones
 [f"kodama_shadow|{KODAMA60} in a dark room, half of his face in shadow, 1970s",
  "time_magazine|A 1976 news magazine lying on a desk, its cover only a photograph of an airliner, no title, no letters",
  "dollar_stacks|Stacks of US dollar banknotes in an open briefcase on a desk, 1970s"],
 # N026 recibos por dos millones, nov 1972; ANA compra TriStar 130 millones
 ["receipts|Close-up of four small paper receipts with red seal stamps on a desk, 1972, " + ILEG,
  "seal_stamp|A hand pressing a traditional red name seal onto a paper receipt, close-up, the seal mark abstract",
  "tristar_runway|A wide-body three-engine airliner of 1972 on a runway at dawn, plain white fuselage without any logo" + SEM],
 # N027 Tanaka detenido en julio; Kodama convaleciente; un avión
 [f"tanaka_arrest|{TANAKA} walking between plain-clothes officers to a car in July 1976, photographers flashing" + SEM,
  "flashbulbs|A crowd of Japanese press photographers with flash cameras in 1976" + SEM,
  "kodama_house|A large traditional Japanese house with a garden wall in Setagaya, Tokyo, 1976, morning" + SEM],
 # N028 El Avión. 23/3/1976, Maeno alquila Piper en Chofu
 ["chofu_airfield|A small airfield in Chofu, Tokyo, in March 1976, light propeller planes parked on the apron" + SEM + "@@CHOFU, 1976",
  "piper|A small single-engine Piper Cherokee light aircraft on a runway, plain white without any registration or lettering",
  f"maeno_cockpit|{MAENO} sitting in the cockpit of a small plane, determined face@@MITSUYASU MAENO"],
 # N029 vestido de kamikaze; Setagaya; dos vueltas
 [f"maeno_headband|Close-up of {MAENO}, tying the headband, in the cockpit",
  "plane_city|A small propeller plane flying low over the rooftops of a Tokyo residential district, morning haze" + FAR,
  "plane_circle|A small propeller plane circling above a large traditional Japanese house with a garden" + FAR],
 # N030 se lanza; choca segundo piso; Maeno muere; Kodama ileso
 ["plane_dive|A small propeller plane diving toward the roof of a large traditional house" + FAR,
  "smoke_house|Black smoke rising from the second floor of a large traditional Japanese house, fire trucks arriving" + FAR,
  "firemen|Firemen spraying water on a smoking house in Tokyo in 1976" + FAR + SEM],
 # N031 Maeno ultranacionalista; traicionado
 [f"maeno_portrait|Portrait of {MAENO}, staring ahead, grey morning light",
  f"kodama_window|{KODAMA76} looking out of a window, his face reflected in the glass",
  "nationalist_flagless|A small ultranationalist street rally in the 1970s, loudspeaker van, plain banners without writing" + FAR + SEM],
 # N032 padrino a la vista; guerra Yama-Ichi ≥36 muertos; Japón mira de otra manera
 ["tv_news_1976|A 1976 TV set in a Japanese living room showing only a photograph of a smoking house" + SEM,
  "newsstand|A Tokyo newsstand in 1976 with stacks of newspapers showing only photographs, " + ILEG,
  "kobe_night|A street in Kobe at night in the mid-1980s, police cars with lights, an empty sidewalk" + FAR + SEM],
 # N033 El Letrero. 1/3/1992, ley; no prohíbe ser yakuza
 ["diet_vote|The chamber of the Japanese Diet in session in 1991, members in dark suits voting" + SEM + NOINS + "@@JAPÓN, 1992",
  "law_gazette|A Japanese official gazette page of 1991 on a desk, " + ILEG + ", a red seal",
  "calendar_march|A wall in a Japanese police office in March 1992, a blank calendar page, a clock" + SEM],
 # N034 comisiones de seguridad pública designan; prohibido exigir dinero en nombre del grupo
 ["commission_room|A Japanese prefectural public safety commission meeting in 1992, officials around a table" + SEM + NOINS,
  "designation_doc|A designation order document with a red official seal, " + ILEG,
  "shop_owner|A frightened Japanese restaurant owner behind his counter in 1992 facing a man in a dark suit seen from behind" + NOTAT + SEM],
 # N035 nombre en la puerta y tarjetas; Libro Blanco: 41 de 108 quitan letrero y emblema; tarjetas
 ["sign_removal|Two men in work clothes taking down a tall vertical blank wooden signboard from beside an office door, 1992" + SEM,
  "white_paper|A thick Japanese government white paper of 1992 open on a desk at a page with a statistical table rendered as " + ILEG,
  "pale_rectangle|A plain wall beside an office door with a paler rectangle and four screw holes where a sign used to hang" + SEM],
 # N036 Itami estrena; llegan los cinco hombres; noviembre Yamaguchi-gumi demanda a la comisión de Hyogo
 ["itami_premiere|" + ITAMI + " at a film premiere in May 1992, photographers, a blank backdrop" + SEM + "@@JUZO ITAMI",
  "kobe_court|The Kobe District Court building in 1992, grey day" + SEM,
  "lawyers_file|Japanese lawyers in dark suits carrying files up the steps of a courthouse, 1992" + SEM],
 # N037 Itami se recupera, vuelve a filmar; penas 6 y 5; muere 1997; Adelstein
 ["itami_hospital|" + ITAMI + " sitting in a hospital bed by a window, a bandage on his cheek, reading a script",
  "itami_camera|" + ITAMI + " looking through the viewfinder of a film camera on a set, 1993",
  "tokyo_court97|A Tokyo High Court courtroom in 1997, judges at the bench, two defendants seen from behind" + SEM + NOINS],
 # N038 CTA; la ley tenía un límite: empresas seguían pagando
 ["corporate_lobby|The lobby of a large Japanese corporation in the 1990s, marble, men in suits passing" + SEM,
  "cash_briefcase|An open briefcase of yen banknotes on a conference table in a corporate office" + SEM],
 # N039 La Asamblea. 27/6/1997, 2.355 empresas el mismo día
 ["agm_hall|A large Japanese shareholders' meeting in 1997, executives seated on a stage behind a long table, rows of shareholders" + SEM + "@@27 DE JUNIO DE 1997",
  "clocks_ten|A wall of identical clocks all showing ten o'clock in a Tokyo office lobby" + SEM,
  "many_halls|A montage-like wide view of a Tokyo business district in 1997 with many office towers, morning rush" + SEM],
 # N040 sokaiya: pocas acciones, amenazan; según la policía trabajan con la yakuza
 ["sokaiya_stand|A man in a dark suit standing up and shouting in the audience of a shareholders' meeting, executives on stage looking nervous, 1990s" + NOTAT + SEM,
  "share_certificate|A single old Japanese share certificate on a desk, ornate border, " + ILEG,
  "exec_nervous|A Japanese company president on stage gripping a microphone, sweating, 1990s"],
 # N041 sokaiya no pueden estar en todas; fiscalía investiga Dai-Ichi Kangyo; Koike
 ["prosecutors_raid|Japanese prosecutors in dark suits carrying cardboard boxes out of a bank headquarters in 1997, press cameras" + SEM,
  "bank_hq|The headquarters tower of a major Japanese bank in Tokyo in 1997" + SEM,
  "loan_ledger|A bank loan ledger open on a desk with columns of numbers rendered as " + ILEG],
 # N042 Okuda condenado, pena suspendida; 11.800 millones; bancos pagaban; FBI
 [f"okuda_bow|{OKUDA} bowing deeply in front of press cameras in 1997" + SEM,
  "verdict_court|A Tokyo courtroom in 1999, a banker standing before the judges" + SEM + NOINS,
  "yen_mountain|A mountain of bundled Japanese yen banknotes in a vault"],
 # N043 El Hígado. Los Ángeles 2001, UCLA, trasplante
 ["ucla_hospital|A large modern university hospital in Los Angeles in 2001, palm trees, sunny day" + SEM + "@@LOS ÁNGELES, 2001",
  "surgery_room|Surgeons in an operating room under bright lights, seen from the door, no blood" + SEM,
  "cooler_box|A medical transport cooler being carried down a hospital corridor" + SEM],
 # N044 Goto, jefe del Goto-gumi
 [f"goto_portrait|Portrait of {GOTO}, cold expression, 2001@@TADAMASA GOTO",
  f"goto_car|{GOTO} stepping out of a black car in front of a building in Japan" + SEM],
 # N045 LA Times: visa con ayuda del FBI; 100 mil dólares
 ["visa_passport|A passport open on a consular desk with a visa page, a rubber stamp in the air, " + ILEG,
  "fbi_meeting|Two American agents in plain suits meeting a Japanese man in a hotel room, curtains drawn" + SEM,
  "donation_check|A check being handed over a desk in a hospital office, " + ILEG],
 # N046 exjefe FBI: no consiguió la operación, nada importante; expulsión 2008; sacerdote 2009
 ["agent_interview|A retired American FBI agent being interviewed in his living room, grey hair, plain shirt" + SEM,
  "expulsion_letter|A folded formal letter on washi paper beside a brush and inkstone, " + ILEG,
  f"goto_monk|{GOTO} with a shaved head in black Buddhist priest robes kneeling in a temple hall, 2009"],
 # N047 en casa el poder no los protege; buscan negocio lejos, Sudamérica
 ["world_globe|An old desk globe turned to South America, lamp light",
  "plane_night|A long-haul airliner taking off at night, plain fuselage without any logo" + SEM],
 # N048 El Aeropuerto. Ezeiza 27/3/2010, 3 kilos de cocaína
 ["ezeiza|The international departures hall of Ezeiza airport in Buenos Aires in 2010, travelers with luggage" + SEM + "@@EZEIZA, 2010",
  "xray_bag|An airport X-ray screen showing a suitcase with dense packages inside, a security officer watching" + SEM,
  f"hira_arrest|{HIRA} being stopped by Argentine airport police at a departure gate" + SEM + NOINS],
 # N049 Hirasawa; InSight Crime; 30 años Yamaguchi-gumi; comprar droga
 [f"hira_cell|{HIRA} sitting on a bunk in an Argentine prison cell, light through a small window",
  "interview_prison|A journalist with a notebook talking to a prisoner across a table in a prison visiting room" + SEM,
  "andes_flight|An airliner flying over the Andes mountains, plain fuselage without any logo" + SEM],
 # N050 condena 4 años 9 meses; anulada; deportado
 ["argentine_court|An Argentine courtroom in 2010, judges behind the bench, wood panelling" + SEM + NOINS,
  "deport_gate|A man escorted by two officers through an empty airport corridor toward a gate" + SEM + NOINS],
 # N051 2024 Sumiyoshi-kai 76 años; 15 kilos desde México; vínculo con cártel no probado
 ["cargo_terminal|An air cargo terminal at night in Japan, customs officers inspecting a large roll of industrial conveyor belt" + SEM,
  "customs_find|Japanese customs officers cutting open a hidden compartment in industrial machinery, finding packages of white crystals" + SEM,
  "old_man_arrest|An elderly Japanese man in his seventies being escorted into a police car at night, 2024" + SEM],
 # N052 cerco: los contratos
 ["contract_pile|A stack of Japanese contracts on a desk with a pen and a name seal, " + ILEG,
  "signing_hand|A hand hesitating above the signature line of a contract, " + ILEG],
 # N053 El Contrato. 23/8/2011 Shimada anuncia que se retira
 [f"shimada_press|{SHIMADA} at a press conference in August 2011, bowing before dozens of cameras and microphones" + SEM + "@@SHINSUKE SHIMADA",
  "tv_studio_2011|A bright Japanese TV variety show studio in 2011, empty presenter's seat" + SEM,
  "camera_flashes|A wall of press camera flashes at a news conference in Tokyo, 2011" + SEM],
 # N054 1/10/2011 Tokio y Okinawa completan: 47 prefecturas con ordenanzas
 ["japan_map|" + MAPA + ", showing the whole Japanese archipelago",
  "tokyo_govt|The Tokyo Metropolitan Government Building in 2011, autumn" + SEM,
  "okinawa_street|A street in Naha, Okinawa, in 2011, sunny" + SEM],
 # N055 empresas no pueden pagar ni ayudar; cláusula: no pertenecer
 ["clause_contract|Close-up of a rental contract with a highlighted clause and a checkbox, " + ILEG,
  "bank_counter|A Japanese bank counter in 2011, a clerk sliding a form to a customer in a dark suit" + SEM,
  "real_estate|A Japanese real estate agency window with blank listing cards, a man looking in" + SEM],
 # N056 Estado que la había usado; nadie firme; tribunal va más lejos
 ["empty_office|An empty gang office in 2015, chairs stacked, a blank wall, dust" + SEM,
  "court_fukuoka|The Fukuoka District Court building in 2021, overcast" + SEM],
 # N057 La Sentencia. Fukuoka 24/8/2021 Nomura condenado a muerte; Kudo-kai
 ["fukuoka_court|Inside a modern Japanese courtroom in 2021, three judges in black robes at the bench" + SEM + NOINS + "@@FUKUOKA, 2021",
  f"nomura_court|{NOMURA} standing in the dock of a Japanese courtroom, seen from the side@@SATORU NOMURA",
  "press_outside|Japanese reporters and TV crews waiting outside a courthouse on a summer day, 2021" + SEM],
 # N058 cuatro ataques; asesinato 1998 ex jefe cooperativa de pescadores; primera pena de muerte
 ["fishing_port|A fishing port in Kitakyushu in 1998 at dawn, small boats moored" + SEM,
  "fishing_coop|A fishermen's cooperative office building by a harbor in the late 1990s" + SEM,
  "judge_reads|A Japanese judge in a black robe reading a verdict aloud from papers at the bench" + SEM + NOINS],
 # N059 "se arrepentirá"; 2024 perpetua; Supremo
 [f"nomura_turn|{NOMURA} turning his head toward the judges in a courtroom, cold stare",
  "high_court|The Fukuoka High Court building in March 2024" + SEM,
  "supreme_court|The Supreme Court of Japan building in Tokyo, granite, overcast" + SEM],
 # N060 sede con su emblema en Kitakyushu; esa puerta ya no existe
 ["kudo_hq|A large fortified headquarters building of a gang in Kitakyushu in 2019, tall wall, security cameras, a heavy gate with a blank round emblem" + SEM,
  "heavy_gate|Close-up of a heavy steel gate of a building, security camera above, blank emblem plate"],
 # N061 La Puerta. Kitakyushu nov 2019 acuerdo; demolición; ONG sin hogar
 ["agreement_sign|Officials in suits signing an agreement at a table in a Japanese city hall in 2019, cameras" + SEM + "@@KITAKYUSHU, 2019",
  "demolition|An excavator demolishing a large concrete building behind a fence" + FAR + SEM,
  "rubble_gate|A heavy steel gate lying among concrete rubble on a demolition site" + SEM],
 # N062 2025: 17.600; 1963: 184.000
 ["npa_report|A Japanese police annual report open on a desk at a bar chart rendered as " + ILEG,
  "old_members|Two elderly Japanese men in dark suits sitting on a park bench, seen from behind, autumn leaves" + NOTAT,
  "hall_dust|A traditional meeting hall with dust on the empty cushions, light through shutters" + SEM],
 # N063 Itami enseñó a cerrar la puerta; la abrieron un ministro, un primer ministro, empresas
 ["door_closing|A hand closing a wooden sliding door, close-up, warm light",
  "itami_old|" + ITAMI + " at his desk at night writing a script, a lamp, 1990s, " + ILEG,
  "door_opening|A wooden gate of a traditional Japanese house slowly opening onto a garden"],
 # N064 nunca se escondió del poder; se escondió cuando dejó de necesitarla
 ["shutter_down|A man in a dark suit pulling down the metal shutter of a small office at dusk, seen from behind" + SEM,
  "blank_door|A plain closed office door with a pale rectangle on the wall beside it, dim light" + SEM],
 # N065 pregunta
 ["case_closed|A brown case folder being closed on a dark desk, a red stamp beside it" + SEM],
]

THUMBS = [
    {"id": "thumb-A", "prompt": "Ink graphic novel illustration: a thick vertical wooden office signboard, completely blank wood with no writing, leaning on the floor against a plain cream plaster wall, two bent screws on the floor, above it on the wall a paler rectangle and four screw holes where it used to hang, the edge of a dark wooden Japanese gate at the left edge, the signboard occupies the LEFT half of the frame, RIGHT half empty plain cream wall, strong black ink outlines, no people, no text, no letters, no kanji, absolutely NO red color, no hex codes"},
    {"id": "thumb-B", "prompt": "Ink graphic novel illustration: a large empty traditional Japanese meeting hall with tatami floor, two long rows of about twenty empty floor cushions, nobody there, a plain empty alcove at the back, cold side light, wide shot from the entrance, the upper left third of the image darker and plain for text, muted slate blue and sepia, no people, no text, no calligraphy, no scrolls with writing, absolutely NO red color, no hex codes"},
    {"id": "thumb-C", "prompt": "Ink graphic novel illustration: a man in a dark suit and white shirt seen from the chest up, standing in front of a bright frosted glass window, strong backlight so the window is the brightest area, his face hidden in shadow, both hands at his chest tearing in half a plain white business card, the two halves visibly separating, the card large in frame with only a small round abstract geometric emblem in the center, no letters, no kanji, no writing on the card, muted slate and sepia palette, no tattoos, no weapons, no other people, no text, no hex codes"},
]

_textos = [x for x in B if "t" in x]
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
