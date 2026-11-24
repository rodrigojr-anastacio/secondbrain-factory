"""Extras da #1 (e1, 24/11/2026): folhas de personagem, capas das histórias, pôster, wallpapers e páginas de texto.

Prompts só de conteúdo (o estilo entra pelo visual/*.yaml). Personagens por token {CHAVE} (personagens.py).
Páginas de texto em espanhol LatAm neutro. Sem lista de e-mail, sem Kit, sem preço (decisão do Rodrigo, 24/11/2026).
"""

URL_CANAL = "https://www.youtube.com/channel/UCVCYqeuCwTWC7Lqez_qeWRA"  # canal.yaml (o handle pode mudar; QR pela URL fixa)

_SHEET = ("Character model sheet of one single {who}. The sheet shows the SAME person five times side by side on a plain "
          "light background: full body front view standing, full body three-quarter view, head close-up front, head "
          "close-up profile, and a small row of three head expressions (calm, worried, determined). Consistent face, "
          "proportions and clothing in every view, even neutral lighting")

FOLHAS = {
    "folha-araceli": _SHEET.format(who="woman, ARACELI: Spanish woman about 27 in 1942, oval face, large dark eyes, dark "
                                       "wavy shoulder-length 1940s hair, red lipstick, dark green fitted 1940s dress "
                                       "with a small brooch, cream coat over the arm in the full body views"),
    "folha-harris": _SHEET.format(who="man, TOMAS: British-Spanish art dealer about 35 in 1942, round friendly face, dark "
                                      "wavy hair combed back, dark eyes, clean-shaven, warm smile, brown tweed jacket, "
                                      "open collar or loose dark tie, a cigarette in one hand in the full body views"),
    "folha-kuhlenthal": _SHEET.format(who="man, KUHLENTHAL: German intelligence officer in civilian clothes about 34 in "
                                          "1941, very tall and thin, long narrow face, blond hair parted to the side, "
                                          "pale eyes, cold polite smile, civilian dark charcoal suit, no insignia, no "
                                          "uniform"),
    "folha-harriman": _SHEET.format(who="man, HARRIMAN: tall lean American diplomat about 53 in 1945, long narrow face, "
                                        "dark hair graying at the temples, heavy dark eyebrows, deep-set eyes, serious "
                                        "expression, dark three-piece suit, white shirt, dark tie"),
    "folha-theremin": _SHEET.format(who="man, THEREMIN: Russian inventor about 49 in 1945, slim, thin intelligent face, "
                                        "dark hair combed straight back, high forehead, tired kind eyes, clean-shaven, "
                                        "worn gray work jacket over a white shirt"),
    "folha-kennan": _SHEET.format(who="man, KENNAN: slim American diplomat about 48 in 1952, thin face, high forehead "
                                      "with receding hairline, short neat dark-blond hair, clean-shaven, thoughtful "
                                      "eyes, gray suit, dark tie, holding rimless reading glasses in one view"),
    "folha-pioneros": ("Character model sheet of a group of five Soviet schoolchildren in 1945 (the PIONEERS), aged 10 to "
                       "12, three girls and two boys, each shown full body front view side by side on a plain light "
                       "background, then their five head close-ups in a row: white shirts and blouses, dark shorts or "
                       "skirts, bright red neckerchiefs tied at the neck, neatly combed hair, girls with braids and big "
                       "white ribbons. Distinct but consistent faces, even neutral lighting"),
    "folha-nkvd": _SHEET.format(who="man, the NKVD man: Soviet security officer about 40 in 1945, broad square face, short "
                                    "dark hair, thick dark mustache, small cold eyes, long dark gray overcoat, dark fur "
                                    "hat in the full body views, no badges or insignia"),
}

CAPAS = {
    "garbo": {
        "id": "KG01", "chars": ["JUAN"],
        "desc": "Capa da Garbo: Juan de capa e chapéu numa rua molhada de Lisboa à noite, de frente, sorriso de canto, "
                "segurando uma carta; atrás, na parede iluminada pelo poste, a sombra dele se multiplica em 27 "
                "silhuetas de espiões de chapéu. Terço de cima escuro (título).",
        "prompt": "Vertical comic book story cover illustration: {JUAN} standing on a rainy cobblestone street of Lisbon "
                  "at night in 1942, facing the viewer from the waist up, a sly confident half smile, holding a sealed "
                  "envelope near his chest, warm street lamp on the right. On the tall wet wall behind him his shadow "
                  "multiplies into a crowd of about twenty-seven dark silhouettes of men in hats and long coats, all "
                  "slightly different. The TOP 35 PERCENT of the image is calm dark blue night sky with rain streaks "
                  "(space for a title), the bottom 12 percent dark wet street. Warm lamp light against cool blue night",
        "pagina": {"expediente": "EXPEDIENTE 1", "titulo": "OPERACIÓN\nGARBO",
                   "subtitulo": "EL ESPAÑOL QUE ENGAÑÓ A HITLER",
                   "rodape": "MADRID · LISBOA · LONDRES · NORMANDÍA  ·  1941–1944"},
    },
    "lacosa": {
        "id": "KC01", "chars": [],
        "desc": "Capa de La Cosa: o selo de madeira (águia) pendurado na parede escura do estudo de Spaso House, um "
                "feixe azul frio entrando pela janela e acertando a águia; embaixo, em primeiro plano, a silhueta de um "
                "homem de fones de ouvido de costas, num furgão. Terço de cima escuro (título).",
        "prompt": "Vertical comic book story cover illustration: a dark wood-paneled study in Moscow at night, on the "
                  "wall a large hand-carved wooden replica of the Great Seal of the United States: a wooden eagle with "
                  "spread wings holding a striped shield on its chest, warm polished wood. A thin cold blue beam of "
                  "light enters through the tall window and hits the eagle's beak, where a tiny metal glint shines. In "
                  "the lower foreground, seen from behind, the dark silhouette of a man wearing big headphones sitting "
                  "in the back of a parked van with glowing radio dials. The TOP 35 PERCENT of the image is calm dark "
                  "shadow (space for a title). Warm lamp light against cold blue night. No flags, no text",
        "pagina": {"expediente": "EXPEDIENTE 2", "titulo": "LA COSA",
                   "subtitulo": "EL REGALO QUE ESCUCHÓ SIETE AÑOS",
                   "rodape": "MOSCÚ · 1945–1952  ·  NUEVA YORK · 1960"},
    },
}

POSTER = {
    "id": "PO01", "orient": "retrato", "chars": ["JUAN"],
    "prompt": "Tall vertical poster key art split by a bold diagonal from upper right to lower left into two scenes. "
              "UPPER LEFT: {JUAN} in trench coat and trilby under a warm street lamp on a rainy 1940s street at night, "
              "his shadow on the wall multiplying into a crowd of dark silhouettes of spies in hats. LOWER RIGHT: a "
              "dark wood-paneled study, a large hand-carved wooden replica of the Great Seal of the United States (a "
              "wooden eagle with spread wings holding a striped shield) on the wall, hit by a thin cold blue beam "
              "through the window. Plenty of calm dark space at the very top and very bottom. Warm against cold light. "
              "No text, no flags",
}

WALLPAPERS = [  # W01 (desktop Garbo) e W02 (celular Garbo) já existem na amostra v3 (arte/W01.jpg, arte/W02.jpg)
    {"id": "W03", "orient": "paisagem", "chars": [],
     "prompt": "Wide cinematic key art: a dark wood-paneled study in Moscow at night, a large hand-carved wooden replica "
               "of the Great Seal of the United States (a wooden eagle with spread wings holding a striped shield, "
               "warm polished wood) hanging on the right third of the wall above a desk with a green lamp; a thin cold "
               "blue beam enters through the tall window on the left and hits the eagle. Calm dark space on the left "
               "half. No flags, no text"},
    {"id": "W04", "orient": "retrato", "chars": [],
     "prompt": "Tall vertical key art: close view of a large hand-carved wooden eagle with spread wings holding a "
               "striped shield (a wooden replica of the Great Seal of the United States) on a dark paneled wall, small "
               "in the lower third, a thin cold blue beam coming from the top of the image and touching its beak, a "
               "tiny copper capsule glinting inside. Upper two thirds calm dark blue shadow with faint dust in the "
               "beam. No text"},
    {"id": "W05", "orient": "paisagem", "chars": ["JUAN"],
     "prompt": "Wide cinematic key art: {JUAN} seen from behind on the right third, standing at a tall window of a dark "
               "1944 London room at night, looking at a huge wall map of the English Channel coast lit by a desk lamp, "
               "dozens of small model boats and arrows pointing to the wrong place; outside, searchlights over the "
               "blue city. Calm dark space on the left. No text, no letters on the map"},
    {"id": "W06", "orient": "retrato", "chars": ["THEREMIN"],
     "prompt": "Tall vertical key art: {THEREMIN} small in the lower third, at a cluttered workbench in a dim locked "
               "laboratory with barred windows at night, holding up a tiny copper cylinder with a thin antenna "
               "against a single hanging bulb; behind him, tall shadow shapes of radio equipment. Upper two thirds "
               "calm dark space with the barred window and cold moonlight. No text"},
]

CAPA_GERAL = {"tipo": "imagem", "saida": "capa", "img": "capa.png", "rotulo": "CAPA GERAL",
              "placeholder": "capa.png (job dossie-hq-cta-e-hotmart)"}

CREDITOS = {
    "tipo": "texto", "saida": "creditos", "titulo": "EXPEDIENTES SECRETOS #1",
    "blocos": [
        {"t": "p", "texto": "Dos historias reales de espionaje que no están en el canal.", "centro": True},
        {"t": "h", "texto": "CRÉDITOS"},
        {"t": "p", "texto": "Guion, edición y diseño: Dossier en Minutos."},
        {"t": "p", "texto": "Ilustraciones generadas con inteligencia artificial y editadas a mano. Los textos, "
                            "globos y la diagramación se hicieron uno por uno, sin IA en las letras."},
        {"t": "p", "texto": "Tipografías: Bangers, Comic Neue, Bebas Neue (SIL Open Font License) y Special Elite "
                            "(Apache 2.0)."},
        {"t": "h", "texto": "AVISO"},
        {"t": "p", "texto": "Estas historias se basan en hechos reales y documentados. Para contarlas en cómic nos "
                            "tomamos libertades dramáticas: los diálogos, algunas escenas y el aspecto de los "
                            "personajes son recreaciones. Al final te contamos qué es real y qué inventamos, con las "
                            "fuentes."},
        {"t": "p", "texto": "Las personas reales que aparecen ya fallecieron y se retratan con respeto. Ningún escudo "
                            "ni sello oficial se usa como marca de este producto."},
        {"t": "pequeno", "texto": "© 2026 Dossier en Minutos. Edición digital. Prohibida su reventa o distribución. "
                                  "Uso personal."},
    ],
}


def sumario(itens, pag_real):
    blocos = []
    for titulo, pag, sub in itens:
        if sub:
            blocos.append({"t": "h", "texto": "%s  ·  p. %d" % (titulo, pag)})
            blocos.append({"t": "item", "texto": sub.capitalize()})
        else:
            blocos.append({"t": "item", "texto": "%s  ·  p. %d" % (titulo.strip(), pag)})
    blocos += [{"t": "h", "texto": "LO QUE ES REAL  ·  p. %d" % pag_real},
               {"t": "h", "texto": "PÓSTER Y FONDOS DE PANTALLA  ·  p. %d" % (pag_real + 2)}]
    return {"tipo": "texto", "saida": "sumario", "titulo": "ÍNDICE", "blocos": blocos}


REAL_GARBO = [
    {"t": "h", "texto": "OPERACIÓN GARBO: LO REAL"},
    {"t": "item", "texto": "Juan Pujol García (Barcelona, 1912 – Caracas, 1988) se ofreció a los británicos en Madrid "
                           "desde enero de 1941 y lo rechazaron. Entonces se ofreció a los alemanes."},
    {"t": "item", "texto": "Los alemanes lo llamaron ALARIC. Desde Lisboa inventó informes sobre Gran Bretaña con una "
                           "guía turística, horarios de trenes, revistas y noticieros. Lo de Glasgow y el litro de vino "
                           "es real."},
    {"t": "item", "texto": "En abril de 1942 los británicos lo llevaron a Londres. El MI5 lo llamó GARBO y su oficial "
                           "fue Tomás Harris. Juntos mantuvieron una red de 27 agentes que no existían (hay fuentes "
                           "que cuentan 22)."},
    {"t": "item", "texto": "El agente inventado de Liverpool «murió», salió una nota en el periódico y los alemanes le "
                           "pagaron una pensión a su «viuda»."},
    {"t": "item", "texto": "El 6 de junio de 1944 avisó del desembarco a las 3 de la mañana; nadie respondió hasta las "
                           "8. El 9 de junio convenció a Berlín de que Normandía era una distracción, y muchas "
                           "divisiones se quedaron esperando en Calais."},
    {"t": "item", "texto": "Recibió la Cruz de Hierro (29/7/1944) y la orden del Imperio Británico, MBE (25/11/1944). "
                           "En 1949 fingió su muerte en Angola y se fue a Venezuela. En 1984 lo encontró el escritor "
                           "Nigel West."},
    {"t": "h", "texto": "LO QUE INVENTAMOS"},
    {"t": "pequeno", "texto": "Los diálogos y pensamientos; el aspecto de Araceli, Tomás Harris y del oficial alemán; "
                              "las escenas del bar, de la oficina alemana y de la sala de radio; los detalles de la "
                              "pelea de 1943 con Araceli y del falso arresto (la crisis existió; lo que se dijeron, "
                              "no lo sabemos)."},
    {"t": "h", "texto": "FUENTES"},
    {"t": "pequeno", "texto": "MI5, «Agent GARBO». Tomás Harris, Garbo: The Spy Who Saved D-Day (2000). Juan Pujol y "
                              "Nigel West, Operation Garbo (1985). Ben Macintyre, Double Cross (2012). Archivos "
                              "KV 2/39–42, National Archives (Kew)."},
]

REAL_COSA = [
    {"t": "h", "texto": "LA COSA: LO REAL"},
    {"t": "item", "texto": "En agosto de 1945 un grupo de Pioneros soviéticos le regaló al embajador W. Averell Harriman "
                           "un Gran Sello de Estados Unidos tallado en madera. Lo colgó en el estudio de su residencia, "
                           "Spaso House."},
    {"t": "item", "texto": "Adentro había un micrófono sin pilas ni cables: un cilindro con una membrana y una antena "
                           "que solo «despertaba» cuando lo iluminaban con ondas de radio desde afuera."},
    {"t": "item", "texto": "Lo diseñó Léon Theremin, el inventor del instrumento musical, cuando estaba preso en un "
                           "laboratorio secreto del sistema de campos soviético. En 1947 recibió el Premio Stalin."},
    {"t": "item", "texto": "Escuchó durante siete años y tres embajadores. En 1951 un operador de radio británico oyó "
                           "voces estadounidenses en una frecuencia soviética."},
    {"t": "item", "texto": "En septiembre de 1952, con George F. Kennan como embajador, técnicos del Departamento de "
                           "Estado lo encontraron mientras Kennan leía un texto en voz alta como carnada."},
    {"t": "item", "texto": "El 26 de mayo de 1960, tras el derribo del avión espía U-2, el embajador Henry Cabot Lodge "
                           "mostró en el Consejo de Seguridad de la ONU una réplica del sello. La moción soviética "
                           "perdió 7 a 2. Hoy hay una réplica en el Museo Criptológico de la NSA."},
    {"t": "h", "texto": "LO QUE INVENTAMOS"},
    {"t": "pequeno", "texto": "Los diálogos; cuántos niños fueron y qué dijeron; el agente del NKVD es un personaje "
                              "inventado que representa a quienes escuchaban; las conversaciones que se oyen; la "
                              "escena exacta en que Theremin recibe el encargo; las herramientas usadas para abrir el "
                              "sello."},
    {"t": "h", "texto": "FUENTES"},
    {"t": "pequeno", "texto": "CIA, «Compromise of the Great Seal» (2020). NSA, «The Thing and I» y «Cold War: Great "
                              "Seal». Crypto Museum, «The Thing». George F. Kennan, Memoirs 1950–1963 (1972)."},
]


def paginas_fim(ultima):
    n = ultima
    return [
        {"tipo": "texto", "saida": "real-1", "titulo": "LO QUE ES REAL", "px_titulo": 100, "blocos": REAL_GARBO,
         "numero": n + 1},
        {"tipo": "texto", "saida": "real-2", "titulo": "LO QUE ES REAL", "px_titulo": 100, "blocos": REAL_COSA,
         "numero": n + 2},
        {"tipo": "texto", "saida": "poster", "titulo": "TU PÓSTER", "numero": n + 3,
         "blocos": [{"t": "p", "texto": "En el archivo .zip viene el póster en tamaño A3 (300 dpi), listo para "
                                        "imprimir, y 6 fondos de pantalla: 3 para el celular y 3 para la computadora.",
                     "centro": True}],
         "caixas": [{"rect": [450, 700, 900, 1350], "img": "001/poster-miniatura.jpg", "rotulo": "PÓSTER",
                     "placeholder": "miniatura do pôster A3 (PO01 + título), gerada na e2"}]},
        # página final (ajuste do Rodrigo, 24/11/2026): QR + CTA de inscrição + link clicável ao lado
        {"tipo": "texto", "saida": "final", "titulo": "¿AÚN NO TE SUSCRIBISTE?", "numero": n + 4,
         "blocos": [{"t": "p", "texto": "Suscríbete a Dossier en Minutos para no perderte los nuevos videos y los "
                                        "próximos Expedientes Secretos.", "centro": True},
                    {"t": "h", "texto": "¿QUÉ EXPEDIENTE QUIERES EN EL #2?"},
                    {"t": "p", "texto": "Déjalo en los comentarios del canal. Leemos todos y el más pedido puede ser "
                                        "el próximo expediente.", "centro": True}],
         "caixas": [{"rect": [180, 900, 640, 640], "img": "001/qr-canal.png", "rotulo": "QR",
                     "placeholder": "QR do canal: " + URL_CANAL}],
         "textos_livres": [{"pos": [880, 990], "larg": 760, "px": 64, "cor": "vermelho",
                            "texto": "ESCANEA EL CÓDIGO O TOCA EL ENLACE:"},
                           {"pos": [880, 1190], "larg": 760, "px": 50, "sublinhado": True,
                            "texto": "DOSSIER EN MINUTOS EN YOUTUBE"},
                           {"pos": [880, 1310], "larg": 760, "px": 40,
                            "texto": "Toca aquí para abrir el canal y suscribirte."}],
         "links": [{"rect": [180, 900, 1460, 640], "url": URL_CANAL}]},
        {"tipo": "texto", "saida": "contracapa", "escuro": True, "titulo": "DOSSIER EN MINUTOS", "px_titulo": 130,
         "blocos": [{"t": "p", "texto": "Historias reales de espionaje, una organización por expediente.",
                     "centro": True},
                    {"t": "p", "texto": "EXPEDIENTES SECRETOS #1 · Operación Garbo · La Cosa", "centro": True}],
         "caixas": [{"rect": [650, 1500, 500, 500], "img": "001/qr-canal.png", "rotulo": "QR",
                     "placeholder": "QR do canal"}]},
    ]
