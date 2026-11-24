"""Operación Garbo: roteiro quadro a quadro (e1, 24/11/2026). Fonte única: montar.py gera ROTEIRO.md, paginas e cenas."""
HISTORIA = "garbo"
TITULO = "OPERACIÓN GARBO"
CAPITULOS = {1: "EL HOMBRE QUE NADIE QUERÍA", 2: "LOS 27 FANTASMAS", 3: "ARACELI", 4: "LA NOCHE MÁS LARGA"}


def Q(id, chars, desc, prompt, textos, arte=None, arte_dir=None, reusa=None, foco=(0.5, 0.5)):
    return {"id": id, "chars": chars, "desc": desc, "prompt": prompt, "arte": arte, "arte_dir": arte_dir,
            "reusa": reusa, "foco": list(foco), "textos": textos}


PAGINAS = [
    # ================= CAPÍTULO 1: EL HOMBRE QUE NADIE QUERÍA =================
    {"n": 1, "cap": 1, "layout": "A5",
     "nota": "gancho: um civil sem experiência quer espionar os nazistas e é recusado; última linha vira a chave (os alemães)",
     "quadros": [
         Q("G0101", ["JUAN"], "Madri faminta, jan/1941: Juan diante da embaixada britânica (arte da v2).", None,
           [["legenda", "Madrid, enero de 1941."],
            ["legenda", "España pasa hambre. Europa está en guerra. Y un catalán de 28 años está a punto de tocar una puerta."]],
           arte="P101", arte_dir="arte-v2"),
         Q("G0102", ["JUAN"], "Juan oferece seus serviços ao diplomata britânico (arte da v2).", None,
           [["fala", "Quiero trabajar para ustedes. ¡Quiero espiar a los nazis!", "JUAN", "e"]],
           arte="P102", arte_dir="arte-v2"),
         Q("G0103", [], "O diplomata britânico, cético, recusa (arte da v2).", None,
           [["fala", "¿Usted? ¿Un civil sin ninguna experiencia?", "DIPLOMÁTICO", "e"],
            ["fala", "Lo siento, señor Pujol. No nos interesa.", "DIPLOMÁTICO", "d"]],
           arte="P103", arte_dir="arte-v2", foco=(0.5, 0.35)),
         Q("G0104", ["JUAN"], "Juan sai na chuva, recusado (arte da v2).", None,
           [["legenda", "Le dijeron que no. Volvería a intentarlo. Le volverían a decir que no."],
            ["sfx", "PLIC PLOC"]],
           arte="P104", arte_dir="arte-v2", foco=(0.5, 0.55)),
         Q("G0105", ["JUAN"], "Close de Juan pensando, com a ideia se formando (arte da v2).", None,
           [["pensa", "Si los ingleses no me quieren...", "JUAN", "e"],
            ["pensa", "...me querrán los alemanes.", "JUAN", "d"]],
           arte="P105", arte_dir="arte-v2", foco=(0.5, 0.62)),
     ]},
    {"n": 2, "cap": 1, "layout": "B5",
     "nota": "os alemães o recrutam (ALARIC); ele não vai à Inglaterra: inventa a Inglaterra de Lisboa e Berlim adora",
     "quadros": [
         Q("G0201", ["JUAN", "KUHLENTHAL"], "Bar de hotel em Madri: o oficial alemão passa dinheiro e tinta invisível a Juan (arte da v3).", None,
           [["legenda", "Así que fue a ver a los alemanes. Ellos sí lo quisieron."],
            ["fala", "Irá a Inglaterra y nos lo contará todo. Su nombre en clave será ALARIC.", "KÜHLENTHAL", "d"],
            ["fala", "Cuenten conmigo.", "JUAN", "e"]],
           arte="P201", arte_dir="arte", foco=(0.5, 0.35)),
         Q("G0202", ["JUAN"], "Juan no cais de Lisboa ensolarado, mala na mão, sorriso maroto (arte da v3).", None,
           [["legenda", "Julio de 1941. Pujol nunca llegó a Inglaterra."],
            ["legenda", "Se quedó en Lisboa."]],
           arte="P202", arte_dir="arte", foco=(0.55, 0.45)),
         Q("G0203", ["JUAN"], "Vista de cima: Juan na biblioteca afogado em guias, horários de trem e revistas (arte da v3).", None,
           [["pensa", "¿Cómo será Glasgow?", "JUAN", "d"],
            ["legenda", "Con una guía turística, horarios de trenes y revistas británicas, inventó Inglaterra entera… desde una biblioteca."]],
           arte="P203", arte_dir="arte"),
         Q("G0204", ["JUAN"], "Close: Juan escreve a carta com tinta invisível, sorrindo (arte da v3).", None,
           [["carta", "«En Glasgow hay hombres que harían cualquier cosa por un litro de vino.»"],
            ["sfx", "SCRITCH"],
            ["legenda", "Nunca había pisado Gran Bretaña."]],
           arte="P204", arte_dir="arte", foco=(0.55, 0.45)),
         Q("G0205", ["KUHLENTHAL"], "Escritório em Madri: os alemães leem a carta, encantados (arte da v3).", None,
           [["grito", "¡Este Alaric es un genio!", "ALEMÁN", "d"],
            ["fala", "¡Mándenlo todo a Berlín!", "KÜHLENTHAL", "e"],
            ["legenda", "Y en Londres, alguien empezaba a leer esos mismos mensajes…"]],
           arte="P205", arte_dir="arte", foco=(0.5, 0.35)),
     ]},
    {"n": 3, "cap": 1, "layout": "E6",
     "nota": "a farsa cresce: despesas inventadas, sub-agentes inventados; os ingleses interceptam e não entendem quem é o fantasma",
     "quadros": [
         Q("G0301", ["JUAN"],
           "Plano médio: Juan no quarto alugado em Lisboa, à noite, somando despesas com um horário de trens britânico aberto.",
           "Medium shot at night in a small rented room in Lisbon in 1941: {JUAN} at a wooden desk under a warm lamp, a thick "
           "railway timetable open beside him, adding up numbers on a sheet with a pencil and a cheeky grin, a few coins and "
           "banknotes on the desk, blue night through the window behind. Leave calm empty space in the upper left for a caption",
           [["legenda", "Cada viaje inventado tenía su boleto inventado. Las tarifas salían de un horario de trenes británico."],
            ["pensa", "Glasgow–Liverpool, primera clase… Berlín paga.", "JUAN", "d"]]),
         Q("G0302", ["KUHLENTHAL"],
           "Madri: Kühlenthal conta notas de dinheiro numa mesa e as coloca num envelope, satisfeito.",
           "Medium close-up in a dim office in Madrid in 1941 lit by a green desk lamp: {KUHLENTHAL} counting a stack of "
           "banknotes and sliding them into a thick envelope, a satisfied cold smile, a pile of opened letters beside him, "
           "a dark wall map behind with no readable names. Leave calm empty space in the upper right",
           [["fala", "Un agente tan productivo merece cada peseta.", "KÜHLENTHAL", "d"]]),
         Q("G0303", ["JUAN"],
           "Calha diagonal: Juan desenha num papel bonequinhos de homens de chapéu ligados por linhas, a rede que inventa.",
           "Close shot from above of {JUAN} at a desk at night drawing on a large sheet of paper: small sketched figures of men "
           "in hats connected by lines like a family tree, with no letters or words, his fountain pen in hand, warm lamp light, "
           "an ink bottle and cigarette smoke curling. His face visible on the right, amused",
           [["legenda", "Un espía solo no bastaba. Así que se inventó ayudantes."],
            ["pensa", "Un piloto holandés… un empleado del ministerio… un venezolano rico.", "JUAN", "d"]]),
         Q("G0304", [],
           "Londres: num escritório do MI5 com luz fria, oficiais britânicos leem uma interceptação, intrigados.",
           "Medium shot inside a cramped 1941 London intelligence office with cool gray daylight: two British officers in tweed "
           "and shirtsleeves lean over a desk reading decoded message sheets with no readable letters, one scratching his head, "
           "the other holding a magnifying glass, a teapot and cups, filing cabinets behind. Leave space at the top for a balloon",
           [["fala", "Los alemanes tienen un agente aquí que nunca hemos visto.", "OFICIAL BRITÁNICO", "e"],
            ["fala", "Y escribe tonterías… que Berlín se cree.", "OFICIAL BRITÁNICO", "d"]]),
         Q("G0305", ["ARACELI"],
           "Apartamento em Lisboa: Araceli, de pé, braços cruzados, olha pela janela para o rio, decidida.",
           "Medium shot in a modest Lisbon apartment at dusk: {ARACELI} standing by an open window with arms crossed, looking "
           "out at the river and the ships, determined and thoughtful, warm sunset light on her face, cool blue shadows in the "
           "room. She is on the right, leave calm empty space on the left",
           [["legenda", "Quien sí sabía todo era Araceli, su esposa."],
            ["pensa", "Si los ingleses no lo escuchan a él… me escucharán a mí.", "ARACELI", "d"]]),
         Q("G0306", ["JUAN"],
           "Vertical: Juan na porta, de chapéu, sem saber o que a esposa planeja; corredor escuro.",
           "Tall vertical shot of {JUAN} in trench coat and trilby leaving an apartment through a door into a dark stairwell, "
           "looking back over his shoulder with a puzzled little smile, warm light from the room behind him, cool blue stairwell "
           "ahead. Leave calm empty space at the top",
           [["fala", "¿Dijiste algo, querida?", "JUAN", "d"]]),
     ]},
    {"n": 4, "cap": 1, "layout": "C4",
     "nota": "Araceli procura os americanos (fev/1942); os ingleses enfim o querem: virada do cap. 1",
     "quadros": [
         Q("G0401", ["ARACELI"],
           "Grande: Araceli entra no escritório de um oficial naval americano em Lisboa; contraluz da janela.",
           "Wide shot inside an office in Lisbon in February 1942 with tall windows and backlight: {ARACELI} in a cream coat "
           "walking confidently toward a desk where a young American naval officer in a dark navy uniform rises from his chair, "
           "surprised. A ceiling fan, papers, a small flag-free wall. Araceli on the left, the officer on the right. Leave calm "
           "empty space in the upper left for captions",
           [["legenda", "Lisboa, febrero de 1942."],
            ["legenda", "Las versiones no coinciden: ella o él buscaron a un oficial de la Marina de Estados Unidos."],
            ["fala", "Mi marido engaña a los nazis. Y lo hace gratis. Escúchenlo.", "ARACELI", "e"]]),
         Q("G0402", [],
           "Close do oficial americano, boquiaberto, segurando o telefone.",
           "Close-up of a young American naval officer in a dark navy uniform holding a black telephone receiver to his ear, "
           "eyebrows raised in astonishment, a window with bright Lisbon light behind him. He is on the right, leave empty "
           "space on the left",
           [["fala", "¿Londres? Tienen que oír esto.", "OFICIAL", "d"],
            ["sfx", "RIIING"]]),
         Q("G0403", [],
           "Londres: um oficial britânico pega uma pasta com etiqueta vermelha em branco e sorri.",
           "Medium shot in a London intelligence office in 1942: a British officer in a brown suit holding up a buff file folder "
           "with a blank red label, smiling broadly, colleagues laughing behind him, cool gray light from a rainy window. Leave "
           "calm space at the top for a balloon",
           [["fala", "¡El fantasma tiene nombre! Un español en Lisboa.", "OFICIAL BRITÁNICO", "e"]]),
         Q("G0404", ["JUAN", "ARACELI"],
           "Faixa: no cais de Lisboa à noite, Juan e Araceli sobem num navio; luz quente das lanternas.",
           "Wide shot of a Lisbon dock at night in 1942: {JUAN} in trench coat and trilby and {ARACELI} in a cream coat walking "
           "up a gangway onto a small steamship, warm lantern light against deep blue night, a British sailor waiting at the top. "
           "Leave calm empty space in the upper left",
           [["legenda", "Los mismos ingleses que lo habían rechazado tres veces ahora lo querían en Londres."],
            ["fala", "Al fin, querida. ¡Al fin!", "JUAN", "e"]]),
     ]},
    # ================= CAPÍTULO 2: LOS 27 FANTASMAS =================
    {"n": 5, "cap": 2, "layout": "A5",
     "nota": "Londres, 24/04/1942: conhece Tomás Harris; recebe o codinome GARBO, 'el mejor actor del mundo'",
     "quadros": [
         Q("G0501", ["JUAN"],
           "Panorama: Londres de 1942 sob neblina, ônibus de dois andares, sacos de areia; Juan pequeno, de mala, olhando tudo.",
           "Wide panoramic shot of a foggy London street in spring 1942: red double-decker bus, sandbags piled against "
           "buildings, barrage balloons in the gray sky, people with gas mask boxes. {JUAN} small in the lower right with one "
           "suitcase, looking up in wonder. Leave calm empty sky in the upper left for captions",
           [["legenda", "Londres, 24 de abril de 1942."],
            ["pensa", "Así que esto es Inglaterra. Me la imaginaba mejor.", "JUAN", "d"]]),
         Q("G0502", ["HARRIS", "JUAN"],
           "Escritório discreto: Tomás Harris aperta a mão de Juan, caloroso.",
           "Medium shot in a modest London office with wooden shelves of paintings and art books: {HARRIS} shaking hands warmly "
           "with {JUAN} across a desk, both smiling, soft lamp light, a window with gray daylight. Harris on the left, Juan on "
           "the right. Leave empty space at the top",
           [["fala", "Tomás Harris. Hablo español. Y me encantan tus mentiras.", "TOMÁS", "e"]]),
         Q("G0503", ["JUAN"],
           "Vertical: close de Juan rindo, surpreso com o elogio.",
           "Tall vertical close-up of {JUAN} laughing with surprise, one hand on his chest, warm lamp light on his face, a dark "
           "wood bookshelf behind. Leave empty space at the top The background is softly out of focus, a framed small painting on the wall, cigarette smoke drifting in the warm light.",
           [["fala", "¿Mentiras? Yo las llamo literatura.", "JUAN", "d"]]),
         Q("G0504", ["HARRIS", "JUAN"],
           "Faixa: Harris e oficiais britânicos à mesa batizam o novo agente; um deles levanta a xícara de chá.",
           "Wide shot of a smoky London meeting room in 1942: {HARRIS} and three British officers in suits around a table with "
           "teacups, one officer raising his cup as a toast, {JUAN} at the head of the table looking pleased. Warm lamp light "
           "and cool window light. Leave space at the top",
           [["fala", "Un actor así merece un nombre de estrella.", "OFICIAL BRITÁNICO", "e"],
            ["fala", "El mejor actor del mundo: GARBO.", "OFICIAL BRITÁNICO", "d"]]),
         Q("G0505", ["JUAN"],
           "Faixa baixa: Juan diante de uma máquina de escrever, mãos prontas, a sombra dele na parede.",
           "Low wide shot of {JUAN} sitting at a typewriter in a small London room at night, cracking his knuckles with a sly "
           "smile, his long shadow cast on the wall behind by a warm lamp. Leave calm empty space on the left",
           [["legenda", "Desde ese día escribió con el MI5 a su lado. Ahora sus mentiras las aprobaba Londres."]]),
     ]},
    {"n": 6, "cap": 2, "layout": "G4",
     "nota": "a fábrica de fantasmas: Juan e Harris montam 27 agentes fictícios num quadro na parede",
     "quadros": [
         Q("G0601", ["HARRIS", "JUAN"],
           "Faixa: Harris e Juan diante de um grande quadro de cortiça cheio de fotos de rostos anônimos ligados por fios vermelhos.",
           "Wide shot of {HARRIS} and {JUAN} standing in front of a big cork wall board covered with many small blank sketched "
           "portraits of men and women connected by red strings, no letters or names, a desk lamp throwing warm light, both "
           "admiring their work, cigarette smoke. Leave calm empty space in the upper left",
           [["legenda", "Juntos construyeron la red de espías más grande de Gran Bretaña. Ninguno existía."]]),
         Q("G0602", [],
           "Coluna alta: muitos 'agentes' imaginários em silhueta, cada um num lugar (porto, fábrica, quartel), empilhados.",
           "Tall vertical montage of imaginary spies as dark silhouettes stacked one above the other, each in a small "
           "different setting: a sailor at a foggy harbor, a clerk at a ministry window, a pilot by a plane, a soldier at a "
           "barracks gate, a waiter in a café, a rich man in a car. Moody cool blue with warm accents, no faces",
           [["legenda", "27 agentes. Un marinero. Un funcionario. Un piloto. Un camarero. Un venezolano rico…"],
            ["legenda", "Los alemanes los llamaban la red ARABEL."]]),
         Q("G0603", ["JUAN"],
           "Juan, de chapéu de marinheiro brincando, faz a voz de um dos agentes; Harris ri ao fundo.",
           "Medium shot of {JUAN} jokingly holding a sailor cap over his chest as if playing a role, making a funny serious "
           "face, a desk covered with letters and a radio set behind him, a man in a brown tweed jacket laughing out of focus "
           "in the background. Leave empty space at the top",
           [["fala", "Cada uno escribe distinto, tiene su carácter… y sus caprichos.", "JUAN", "e"]]),
         Q("G0604", ["HARRIS"],
           "Harris com uma pilha de cartas e um cheque; as despesas dos fantasmas pagas por Berlim.",
           "Medium close-up of {HARRIS} holding up a German money transfer slip with no readable letters next to a tall stack "
           "of letters on a desk, grinning, warm lamp light, a filing cabinet behind. Leave empty space on the right Rain streaks the window behind him.",
           [["fala", "Y lo mejor: Berlín les paga el sueldo a todos.", "TOMÁS", "e"],
            ["sfx", "TAC TAC TAC"]]),
     ]},
    {"n": 7, "cap": 2, "layout": "B5",
     "nota": "o agente de Liverpool 'morre': obituário no jornal e pensão alemã para a viúva (humor)",
     "quadros": [
         Q("G0701", [],
           "Porto de Liverpool cinzento; um homem anônimo de capa vigia navios (o agente inventado).",
           "Wide shot of the gray foggy docks of Liverpool in 1942: warships and cargo ships, cranes, seagulls, a lone man in a "
           "long coat and flat cap seen from behind watching the ships, cool gray and blue light. Leave calm empty sky in the "
           "upper left",
           [["legenda", "Uno de los agentes vigilaba el puerto de Liverpool. Mejor dicho: no lo vigilaba, porque no existía."]]),
         Q("G0702", ["HARRIS", "JUAN"],
           "Juan e Harris debruçados na mesa: problema, o agente de Liverpool deveria ter visto um comboio.",
           "Medium shot of {HARRIS} and {JUAN} leaning over a desk with a nautical chart without names, worried expressions, "
           "a lamp lighting their faces, rain on the window. Harris on the left, Juan on the right. Leave empty space at the top",
           [["fala", "Debió ver salir el convoy. Si no lo informa, sospecharán.", "TOMÁS", "e"],
            ["fala", "Entonces… que se enferme. Muy grave.", "JUAN", "d"]]),
         Q("G0703", [],
           "Vertical: página de jornal com coluna de obituários, uma pequena nota emoldurada em vermelho (sem letras legíveis).",
           "Tall vertical close-up of a 1942 British newspaper page with columns of illegible tiny text and an obituary notice "
           "circled in red ink, a fountain pen and a cup of tea on the table, soft lamp light. No readable letters",
           [["legenda", "El agente «murió». Y salió su obituario en el periódico local."],
            ["sfx", "SNIF"]]),
         Q("G0704", ["KUHLENTHAL"],
           "Madri: Kühlenthal, solene, assina uma ordem; ao lado o recorte do obituário.",
           "Medium shot of {KUHLENTHAL} at his desk in Madrid signing a document with a solemn face, a newspaper clipping "
           "beside it, a cold lamp light, heavy curtains. Leave empty space on the left A telephone and a stamp pad on the desk, a tall window with closed shutters behind him, quiet cold mood.",
           [["fala", "Un héroe caído. Pagaremos una pensión a su viuda.", "KÜHLENTHAL", "d"]]),
         Q("G0705", ["JUAN", "HARRIS"],
           "Faixa: Juan e Harris brindam com taças, rindo, diante do cheque da 'viúva'.",
           "Wide shot of {JUAN} and {HARRIS} clinking small glasses of sherry and laughing in a London office at night, an "
           "envelope of money on the desk between them, warm lamp light against blue night window. Leave calm space in the "
           "upper right",
           [["legenda", "Los nazis le pagaban una pensión a la viuda de un espía que nunca había nacido."],
            ["fala", "¡Por la viuda!", "JUAN", "e"]]),
     ]},
    {"n": 8, "cap": 2, "layout": "C4",
     "nota": "sucesso total em Berlim… e Araceli sozinha num apartamento de Londres: virada do cap. 2",
     "quadros": [
         Q("G0801", [],
           "Grande: sala alemã de rádio/mapas; oficiais fixam alfinetes num mapa da Grã-Bretanha a partir das mensagens.",
           "Large wide shot of a German intelligence map room in 1943: officers in civilian suits pinning many small markers on "
           "a huge map of Britain with no names, telegraph operators at desks, a long table full of papers, cold electric light. "
           "No insignia, no flags, no portraits. Leave calm space at the top",
           [["legenda", "En Berlín, los informes de Alaric valían oro. Llegaban por cientos."],
            ["fala", "Si Alaric lo dice, es verdad.", "OFICIAL ALEMÁN", "d"]]),
         Q("G0802", ["JUAN"],
           "Juan trabalhando até tarde, máquina de escrever, cinzeiro cheio; luz da madrugada.",
           "Medium shot of {JUAN} typing furiously at a typewriter late at night in a London office, an overflowing ashtray, "
           "piles of letters, tired but happy, a warm lamp and the first blue light of dawn at the window. Leave space at the top",
           [["sfx", "TAC TAC TAC"]]),
         Q("G0803", ["ARACELI"],
           "Araceli sozinha num apartamento de Londres, sentada junto à janela com chuva, xícara intocada.",
           "Medium shot of {ARACELI} sitting alone by a rainy window in a small cold London flat, an untouched cup of tea in her "
           "hands, gray light, raindrops streaking the glass, sad homesick expression. She is on the left, leave space on the right",
           [["pensa", "Lluvia. Otra vez lluvia. Nadie habla español.", "ARACELI", "d"]]),
         Q("G0804", ["ARACELI", "JUAN"],
           "Faixa: Juan entra tarde em casa; Araceli de costas para ele, fria; a porta abre luz quente.",
           "Wide shot of a dim London flat at night: {JUAN} entering through a door with a briefcase, warm hallway light behind "
           "him, while {ARACELI} stands with her back to him by the dark window, arms crossed, cold blue light on her. Juan on "
           "the left, Araceli on the right. Leave calm space at the top",
           [["fala", "Juan, quiero volver a España.", "ARACELI", "d"],
            ["legenda", "Garbo engañaba a Hitler. Pero en casa, alguien ya no quería seguir con la función."]]),
     ]},
    # ================= CAPÍTULO 3: ARACELI =================
    {"n": 9, "cap": 3, "layout": "A5",
     "nota": "1943: a crise explode; Araceli ameaça ir à embaixada espanhola (põe tudo em risco)",
     "quadros": [
         Q("G0901", ["ARACELI", "JUAN"],
           "Faixa: discussão na sala; Araceli aponta para a porta, Juan tenta acalmá-la.",
           "Wide dramatic shot of a heated argument in a London flat at night in 1943: {ARACELI} pointing furiously at the door, "
           "{JUAN} raising both hands trying to calm her, an overturned chair, a warm lamp casting sharp shadows. Araceli on the "
           "left, Juan on the right. Leave calm space in the upper left",
           [["legenda", "Londres, 1943."],
            ["grito", "¡Si no me dejas ir, voy a la embajada de España!", "ARACELI", "e"]]),
         Q("G0902", ["JUAN"],
           "Close de Juan pálido, entendendo o tamanho do perigo.",
           "Close-up of {JUAN} turning pale in shock, eyes wide, a bead of sweat on his forehead, cold blue light from the "
           "window on one side of his face and warm lamp light on the other. Leave empty space on the left",
           [["pensa", "La embajada de España está llena de amigos de los alemanes.", "JUAN", "d"]]),
         Q("G0903", ["ARACELI"],
           "Vertical: Araceli pega o casaco e o chapéu, decidida.",
           "Tall vertical shot of {ARACELI} grabbing her cream coat and hat from a coat rack by the door, determined and teary, "
           "dramatic low angle, warm light from a hallway. Leave calm space at the top The flat behind her is dim and blue, an umbrella stand beside the door.",
           [["fala", "Lo digo en serio.", "ARACELI", "d"]]),
         Q("G0904", ["HARRIS", "JUAN"],
           "Faixa: madrugada no escritório; Harris ouve Juan, mãos no rosto; telefone fora do gancho.",
           "Wide shot of a London office before dawn: {HARRIS} listening with his hands over his face in worry while {JUAN} "
           "talks urgently, a telephone receiver off the hook on the desk, cold blue light from the window. Harris on the left, "
           "Juan on the right. Leave space at the top",
           [["legenda", "Una sola visita a esa embajada y los 27 fantasmas se esfumarían."],
            ["fala", "Si habla, se acaba todo. Todo.", "TOMÁS", "e"]]),
         Q("G0905", ["HARRIS"],
           "Faixa baixa: Harris acende um cigarro, com um brilho de ideia nos olhos.",
           "Low wide close-up of {HARRIS} lighting a cigarette with a match, the flame lighting his face warmly in a dark room, "
           "eyes narrowing with a clever idea. He is on the right, leave calm empty space on the left Smoke curls up.",
           [["fala", "A menos que… la asustemos con una historia mejor.", "TOMÁS", "d"],
            ["sfx", "FSSS"]]),
     ]},
    {"n": 10, "cap": 3, "layout": "E6",
     "nota": "o MI5 encena: Garbo 'demitido e preso' por culpa da ameaça dela",
     "quadros": [
         Q("G1001", ["HARRIS", "JUAN"],
           "Harris explica o plano a Juan com dois dedos, como num tabuleiro.",
           "Medium shot of {HARRIS} explaining a plan to {JUAN} in a dim office, moving two chess pieces on a desk, both leaning "
           "in conspiratorially, warm lamp light. Harris on the left, Juan on the right. Leave space at the top",
           [["fala", "Le diremos que te despidieron. Y que te detuvieron.", "TOMÁS", "e"]]),
         Q("G1002", ["JUAN"],
           "Juan hesita, culpado, olhando a foto de Araceli.",
           "Medium close-up of {JUAN} looking down at a small framed photo of a woman held in his hands, guilty and sad, lamp "
           "light, a dark background. Leave empty space on the left A desk with scattered letters and an ashtray in front of him, rain on the window behind, quiet melancholy mood in the small office.",
           [["pensa", "Perdóname, Araceli. Es para salvarnos a todos.", "JUAN", "d"]]),
         Q("G1003", ["ARACELI"],
           "Calha diagonal: Araceli abre a porta para um oficial britânico de chapéu que traz a notícia.",
           "Medium shot of {ARACELI} opening the door of her flat to a serious British officer in a long coat and hat holding "
           "his hat in his hands, morning cold light in the corridor, her face dropping in alarm. Araceli on the left, officer "
           "on the right. Leave space at the top",
           [["fala", "Señora, su marido ha sido detenido.", "OFICIAL BRITÁNICO", "d"],
            ["sfx", "TOC TOC"]]),
         Q("G1004", ["ARACELI"],
           "Close de Araceli em choque, mão na boca.",
           "Close-up of {ARACELI} in shock, one hand over her mouth, eyes filling with tears, cold blue light, a dark doorway "
           "behind her. Leave empty space on the right A coat rack and a small mirror on the wall beside the door, a draft lifting her hair slightly, the corridor beyond is gray and empty.",
           [["fala", "¿Detenido? ¿Por qué?", "ARACELI", "e"]]),
         Q("G1005", [],
           "Faixa: carro preto na chuva diante de um portão de campo de detenção cercado.",
           "Wide shot of a black 1940s car driving through rain toward the gates of a guarded detention camp in the English "
           "countryside, barbed wire fence, a sentry box with a lamp, gray dusk. No insignia. Leave calm sky at the top",
           [["legenda", "La llevaron a verlo. Él estaba «preso». Todo era teatro."]]),
         Q("G1006", ["JUAN"],
           "Vertical: Juan atrás de uma mesa nua, sob lâmpada, fazendo-se de abatido.",
           "Tall vertical shot of {JUAN} sitting behind a bare wooden table in a small bare room under a single hanging bulb, "
           "tie loosened, unshaven, playing the part of a broken prisoner, staring at the floor. Leave calm empty space at the top",
           [["legenda", "Nunca había actuado tan bien."]]),
     ]},
    {"n": 11, "cap": 3, "layout": "B5",
     "nota": "o reencontro na 'prisão'; Araceli promete não falar; o casal volta a ser equipe",
     "quadros": [
         Q("G1101", ["ARACELI", "JUAN"],
           "Faixa: Araceli entra na sala de visita; Juan levanta a cabeça.",
           "Wide shot of a bare visiting room under a hanging bulb: {ARACELI} entering through a door on the left with a British "
           "guard, {JUAN} at a table on the right slowly raising his head, cold light, long shadows. Leave calm space at the top",
           [["fala", "¡Juan!", "ARACELI", "e"],
            ["fala", "Me echaron, Araceli. Por lo de la embajada.", "JUAN", "d"]]),
         Q("G1102", ["ARACELI"],
           "Araceli chora, arrependida, segurando as mãos dele sobre a mesa.",
           "Close medium shot of {ARACELI} crying with regret, holding a man's hands across a wooden table, warm light from the "
           "bulb on her face. She is on the left, leave empty space on the right The table is bare and scratched, a guard's shadow on the wall.",
           [["fala", "Fue mi culpa. Te juro que no diré nada. Nunca.", "ARACELI", "e"]]),
         Q("G1103", ["HARRIS"],
           "Vertical: atrás de um vidro, Harris observa a cena e solta o ar, aliviado.",
           "Tall vertical shot of {HARRIS} watching through a small window in a door from a dark corridor, letting out a sigh "
           "of relief, cigarette smoke rising, the bright room visible through the glass. Leave calm space at the top Stark mood.",
           [["pensa", "Funcionó.", "TOMÁS", "d"]]),
         Q("G1104", ["JUAN", "ARACELI"],
           "Dias depois: Juan 'libertado' abraça Araceli na porta de casa.",
           "Medium shot of {JUAN} and {ARACELI} embracing tightly at the door of their London flat, she smiling through tears, "
           "warm hallway light. Juan on the left, Araceli on the right. Leave space at the top Rain has stopped outside, a little umbrella dripping by the door, cozy warm mood.",
           [["legenda", "Días después, «lo soltaron». Araceli no volvió a amenazar con nada."]]),
         Q("G1105", ["ARACELI", "JUAN"],
           "Faixa baixa: o casal à mesa da cozinha, Araceli ajudando a dobrar cartas; volta a cumplicidade.",
           "Low wide shot of {ARACELI} and {JUAN} at a small kitchen table at night folding letters together and smiling at each "
           "other, a kettle and teacups, warm lamp light against blue night window. Leave calm space on the left Cozy mood.",
           [["legenda", "Las versiones varían en los detalles. Lo seguro: el matrimonio y la red sobrevivieron."]]),
     ]},
    {"n": 12, "cap": 3, "layout": "D3",
     "nota": "1944: o plano do Dia D (Fortitude): Garbo será a peça-chave da maior mentira da guerra: virada do cap. 3",
     "quadros": [
         Q("G1201", ["HARRIS", "JUAN"],
           "Splash: sala de guerra britânica, enorme mapa do Canal da Mancha (sem nomes), oficiais; Harris e Juan no centro.",
           "Large wide dramatic shot of a secret British war room in 1944: a huge map of the English Channel coast with no "
           "names covered with markers and arrows pointing to two different coast points, senior British officers in uniform "
           "around a table, {HARRIS} and {JUAN} in the center being briefed, strong overhead lights and deep shadows. Leave calm "
           "empty space in the upper left for captions",
           [["legenda", "1944. Los Aliados preparan el desembarco más grande de la historia."],
            ["legenda", "Para que funcione, Hitler tiene que mirar al lugar equivocado."],
            ["fala", "Y quien se lo va a decir… es usted, señor Garbo.", "OFICIAL BRITÁNICO", "d"]]),
         Q("G1202", [],
           "Tanques e caminhões infláveis de borracha num campo inglês, soldados levantando um tanque com uma mão.",
           "Square shot of an English field at dawn with inflatable rubber tanks and fake trucks, two soldiers effortlessly "
           "lifting a rubber tank by hand, mist, a fake camp of tents. No insignia. Leave space at the top Gray soft morning light.",
           [["legenda", "Un ejército falso, con tanques de goma, frente a Calais."]]),
         Q("G1203", ["JUAN"],
           "Juan sorri diante do quadro de cortiça dos 27 agentes (reuso da arte da pág. 6 com outro recorte).", None,
           [["pensa", "Mis 27 fantasmas van a la guerra.", "JUAN", "d"]],
           reusa="G0601", foco=(0.7, 0.5)),
     ]},
    # ================= CAPÍTULO 4: LA NOCHE MÁS LARGA =================
    {"n": 13, "cap": 4, "layout": "A5",
     "nota": "noite de 5/6 jun 1944: Garbo avisa o desembarque às 3h (para ganhar crédito) e ninguém atende até as 8h",
     "quadros": [
         Q("G1301", [],
           "Faixa: casa londrina às escuras sob céu de tempestade, uma janela acesa no último andar.",
           "Wide shot of a dark London terrace house at night under a stormy sky in June 1944, rain, only one small window "
           "lit warmly on the top floor, a radio antenna wire on the roof. Leave calm empty sky in the upper left",
           [["legenda", "Noche del 5 al 6 de junio de 1944."],
            ["legenda", "El plan: avisar a los alemanes del desembarco… cuando ya fuera tarde para impedirlo."]]),
         Q("G1302", ["JUAN", "HARRIS"],
           "Juan ao transmissor de rádio com fones; Harris de pé atrás, olhando o relógio.",
           "Medium shot of {JUAN} wearing headphones at a radio transmitter tapping a telegraph key, {HARRIS} standing behind "
           "him checking his wristwatch, warm lamp and the green glow of radio dials. Juan on the left, Harris on the right. "
           "Leave space at the top",
           [["fala", "Las tres en punto. Ahora.", "TOMÁS", "d"],
            ["sfx", "BIP BIP BIP"]]),
         Q("G1303", [],
           "Vertical: Madri, uma sala de rádio alemã vazia; fones pendurados, cadeira vazia, relógio às 3h.",
           "Tall vertical shot of an empty radio room in Madrid at night: headphones hanging from an empty chair, a receiver "
           "glowing softly, a wall clock with hands at three o'clock, a half-eaten sandwich, nobody there. Cold blue light Silent mood.",
           [["legenda", "En Madrid, nadie contestaba."]]),
         Q("G1304", ["JUAN"],
           "Faixa: Juan exasperado, mãos na cabeça; relógio da parede marca 8h; luz do amanhecer.",
           "Wide shot of {JUAN} exasperated with both hands on his head beside the radio set, a wall clock showing eight "
           "o'clock, pale morning light flooding in through the window, empty coffee cups. Leave calm space in the upper right Tired mood.",
           [["legenda", "Respondieron a las ocho. Para entonces, las tropas ya estaban en las playas."],
            ["grito", "¡No puedo aceptar excusas ni negligencias!", "JUAN", "e"]]),
         Q("G1305", ["KUHLENTHAL"],
           "Faixa baixa: Kühlenthal envergonhado lendo a reclamação.",
           "Low wide shot of {KUHLENTHAL} reading a message in his Madrid office in morning light, embarrassed, loosening his "
           "collar, an operator with headphones looking down guiltily beside him. Leave calm space on the right Heavy curtains, a desk lamp switched off, a framed blank map on the wall behind them.",
           [["pensa", "Tenía razón. Alaric nos avisó y no lo escuchamos.", "KÜHLENTHAL", "e"]]),
     ]},
    {"n": 14, "cap": 4, "layout": "F1",
     "nota": "splash do clímax: amanhecer do Dia D na Normandia (sem corpos, sem sangue)",
     "quadros": [
         Q("G1401", [],
           "Splash vertical: amanhecer de 6/6/1944, centenas de navios e lanchas de desembarque se aproximando da costa; céu com aviões.",
           "Tall vertical epic splash: dawn on 6 June 1944 seen from a cliff top above a wide beach, hundreds of ships and "
           "landing craft approaching across a gray sea, dozens of planes in the cloudy sky, smoke on the horizon, golden first "
           "light breaking through the clouds. No bodies, no blood, distant scale. Leave calm sky at the top for captions",
           [["legenda", "6 de junio de 1944. Normandía."],
            ["legenda", "La verdad llegó a la playa. Ahora faltaba la mentira más importante."]]),
     ]},
    {"n": 15, "cap": 4, "layout": "E6",
     "nota": "9/6: a mensagem da 'diversão'; as divisões ficam em Calais; Cruz de Ferro (29/7) e MBE (25/11/1944)",
     "quadros": [
         Q("G1501", ["JUAN"],
           "Juan escreve à máquina a mensagem mais importante, concentrado, de madrugada.",
           "Medium shot of {JUAN} typing at a typewriter with intense concentration at night, a lamp lighting his face, a map "
           "without names with two arrows pinned on the wall behind him. Leave calm empty space at the top Cigarette smoke.",
           [["legenda", "9 de junio de 1944."],
            ["carta", "«Normandía es una distracción. El golpe principal será en Calais.»"]]),
         Q("G1502", [],
           "Berlim: uma mão segura a mensagem diante de um mapa; Hitler nunca de rosto, só a sombra da mão.",
           "Close square shot in a dark command room: a hand in a dark sleeve holding a telegram over a big map table with "
           "markers on the coast of northern France, the shadow of the hand stretching over the map, cold lamp light, no faces, "
           "no insignia. Leave space at the top",
           [["legenda", "El mensaje subió hasta el cuartel general de Hitler."]]),
         Q("G1503", [],
           "Calha diagonal: divisões blindadas alemãs paradas em Calais, tanques sob redes, tripulações esperando.",
           "Square shot of a column of German tanks parked and waiting under camouflage nets along a coastal road near Calais, "
           "crews sitting idle on the tanks looking at the empty sea, overcast light. No insignia, no flags. Leave space at the top",
           [["legenda", "Dos divisiones blindadas y diecinueve de infantería se quedaron esperando en Calais."],
            ["legenda", "Un ataque que nunca llegó."]]),
         Q("G1504", ["HARRIS", "JUAN"],
           "Harris e Juan em silêncio, olhando um mapa com alívio; Harris põe a mão no ombro dele.",
           "Medium shot of {HARRIS} placing a hand on the shoulder of {JUAN} as they both look at a war map on a wall with "
           "relief and quiet pride, warm afternoon light through a window. Harris on the left, Juan on the right. Leave space "
           "at the top",
           [["fala", "Lo lograste, Juan. Se lo creyeron.", "TOMÁS", "e"]]),
         Q("G1505", ["JUAN"],
           "Juan abre uma caixinha com uma cruz de ferro (sem suástica), rindo incrédulo.",
           "Square shot of {JUAN} opening a small dark box containing a black iron cross medal with a plain center and no "
           "swastika, laughing in disbelief, warm lamp light. Leave space at the top and left A crumpled wrapping paper and a ribbon lie on the desk, a dark window behind him.",
           [["legenda", "29 de julio de 1944: los alemanes le dieron la Cruz de Hierro."],
            ["pensa", "Por servicios a Alemania… ¡ja!", "JUAN", "d"]]),
         Q("G1506", ["JUAN"],
           "Vertical: Juan de terno, sozinho num salão britânico iluminado, recebendo uma medalha de fita (MBE).",
           "Tall vertical shot of {JUAN} in his best suit standing straight in a grand British palace hall, a small medal with a "
           "ribbon pinned to his lapel, soft golden light from tall windows, a modest proud smile. Leave calm space at the top",
           [["legenda", "Y el 25 de noviembre, el rey de Inglaterra, la Orden del Imperio Británico."],
            ["legenda", "Condecorado por los dos bandos."]]),
     ]},
    {"n": 16, "cap": 4, "layout": "G4",
     "nota": "epílogo: Angola 1949 (morte forjada) → Venezuela → 1984 → Caracas 1988; fecho: a sombra dos 27",
     "quadros": [
         Q("G1601", [],
           "Faixa: Angola, 1949; cemitério tropical sob sol, uma lápide simples, ninguém por perto.",
           "Wide shot of a small quiet tropical cemetery in Angola in 1949 under hot sunlight, palm trees, a simple stone grave "
           "marker with no readable letters, red earth, a lone vulture on a fence, long shadows. Leave calm sky in the upper left",
           [["legenda", "1949. Angola. Juan Pujol «murió» de malaria."],
            ["legenda", "Su última gran mentira."]]),
         Q("G1602", ["JUAN"],
           "Coluna alta: Juan mais velho (60s, cabelo grisalho) numa pequena livraria de vila venezuelana, montanhas verdes ao fundo.",
           "Tall vertical shot of {JUAN} older, about 70, gray hair and gray mustache, light linen shirt instead of a suit, "
           "standing in the doorway of a small colorful bookshop in a Venezuelan coastal village, green mountains and palm trees "
           "behind, bright warm tropical light. Leave calm space at the top",
           [["legenda", "En realidad vivía en Venezuela. Tranquilo. Anónimo."],
            ["pensa", "Aquí nadie busca a un espía muerto.", "JUAN", "d"]]),
         Q("G1603", ["JUAN"],
           "1984: um escritor britânico encontra o velho Juan; aperto de mãos numa varanda.",
           "Square shot of {JUAN} older, about 72, gray hair and gray mustache, light linen shirt, shaking hands with a "
           "middle-aged British writer in a blue blazer holding a notebook, on a sunny veranda in Caracas, both smiling. Juan on "
           "the left, writer on the right. Leave space at the top",
           [["legenda", "1984. El escritor Nigel West lo encontró."],
            ["fala", "¿Usted es Garbo?", "NIGEL WEST", "d"],
            ["fala", "Lo fui.", "JUAN", "e"]]),
         Q("G1604", ["JUAN"],
           "Close final: Juan idoso na luz do poente; atrás, na parede, a sombra dele se multiplica em 27 silhuetas de chapéu.",
           "Square shot of {JUAN} older, about 76, gray hair and gray mustache, sitting in a chair at sunset with a calm smile, "
           "and on the warm wall behind him his long shadow multiplies into a crowd of 27 dark silhouettes of men in hats and "
           "coats, as if keeping him company. Warm orange light against deep blue shadows. Leave calm space at the top",
           [["legenda", "Murió en Caracas el 10 de octubre de 1988."],
            ["legenda", "Nunca estuvo solo: lo acompañaban 27 espías que jamás existieron."]]),
     ]},
]
