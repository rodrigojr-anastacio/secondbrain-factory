#!/usr/bin/env python3
"""Fonte única do 013-uniao-sovietica (18/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

10º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
3º com ÂNGULO próprio (ANGULO.md): "a prateleira e o Plano" — cada plano resolve a urgência da vez e deixa a falta que o próximo promete resolver.
EMBALAGEM.md aprovada no crivo r3:
  A/T1 "A URSS chegou ao ESPAÇO. Por que faltava comida?" + thumb rosto-emocao (Iéltsin pasmo diante da fartura, “NEM O POLITBURO”)
  B/T2 "Como o PÃO explica a União Soviética inteira" + thumb objeto-simbolo (avoska vazia diante de prateleiras vazias, "VAI QUE…")
  C/T3 "URSS: o país que pôs o 1º homem no espaço e COMPRAVA trigo" + thumb numero-estatistica ("30 MIL / NA FILA")
Hook: Houston 1989 (controle de missão de manhã, supermercado à tarde, "nem o Politburo tem essa escolha") → 30 mil na fila da lanchonete
  americana (31/01/1990) → trigo de fora desde 1963 → PERGUNTA CENTRAL (≤ 0:45) → "essa é a história inteira… começa com uma promessa de pão".
Fio condutor: A PRATELEIRA. Cada era = uma urgência → o plano que a resolve → a falta que sobra.
  Peça 1 (cap. 3): o plano faz uma coisa enorme de cada vez (aço sim, prateleira depois).
  Peça 2 (cap. 5): foguete é uma ordem; vaca são mil decisões (Riazan).
  Peça 3 (cap. 7): a prateleira enche com dinheiro do petróleo (emprestada).
  Fecho: o foguete é uma ordem só; a prateleira são milhões de escolhas por dia.
"Guarde" único: os americanos da sopa de 1921 (ARA) → pago no cap. 9 (comida de fora de novo: lanchonete americana e reserva de Berlim).
Neutralidade: fomes (1921, 1932–33, 1946–47) e Novocherkassk com números como estimativa, sem humor sobre vítimas, sem imagem gráfica.
KGB/serviço secreto: fora (tema do dossie-es). Golpe e 25/12 em 1 frase cada (consenso da manada).

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1921") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006–012).
Imagens: Codex (canal.yaml visual.gerador: codex; fallback nano-banana). Prompts só de conteúdo; o estilo vem do canal.yaml.
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (006–012: ~128 ppm com pausas)
BREAK, LONG = 0.35, 0.8
MAX_PLANO_INICIO = 3.0   # s por plano nos primeiros INICIO s (~20 cortes/min)
INICIO = 120.0
MAX_PLANO = 3.6      # s por plano depois (~17 cortes/min)
INEDITO_ATE = 180.0  # s: só imagens novas até aqui
JANELA = 60.0        # s: mesmo enquadramento da mesma imagem só depois disso
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "A história INTEIRA da União Soviética"
PERGUNTA = "Como o país que chegou primeiro ao espaço não conseguia encher uma prateleira?"
PROMESSA = ("Por que o país que chegou primeiro ao espaço passou setenta anos sem conseguir encher a prateleira, contado da promessa de pão "
            "de 1917 à fila de 1990, plano por plano (EMBALAGEM.md r3).")
TITULOS = ('T1 "A URSS chegou ao ESPAÇO. Por que faltava comida?" / T2 "Como o PÃO explica a União Soviética inteira" / '
           'T3 "URSS: o país que pôs o 1º homem no espaço e COMPRAVA trigo"')

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None):
    ideia = t.startswith("§")
    n = sum(1 for x in B if "t" in x) + 1
    if not s: s = tuple(P.get(n, ()))
    assert s, f"N{n:03d} sem planos"
    B.append({"t": t.lstrip("§ ").strip(), "s": list(s), "card": card, "ideia": ideia})

# ───────── regras de prompt (Codex; fallback nano-banana) ─────────
# As refs de estilo vêm do Egito e vazam conteúdo (visual.md 010/011): toda cena leva URSS/EUA + SEMTXT; cenas com gente ou praça levam SEMBAND.
MAPA = ("painted like a blank parchment terrain map seen from directly above, only coastlines, seas, rivers, mountains and flat colored areas, "
        "completely blank with no writing anywhere, no letters, no words, no labels, no symbols, no compass, no border, no frame, no flags, no people")
SEMTXT = ", no readable writing, no letters anywhere, no numbers, no signs, no boards, no logos"
SEMBAND = ", no flags, no banners, no hammer and sickle, no red stars, no emblems"
GUERRA = ", no blood, no wounds, no bodies, no weapons fired, no violence shown"
URSS = (", strictly Russia and the Soviet Union of the time: birch trees, wooden izba houses, onion domes or plain Soviet buildings, snow or steppe, "
        "NO pyramids, NO palm trees, NO pharaoh headdress, NO turbans, NO crowns, NO desert dunes, NO Roman or Greek ruins")
EUA89 = ", strictly Houston, Texas in 1989: no pyramids, no palm-tree desert, no turbans, no crowns, no smartphones, no flat screens"
def ANO(a): return f", period-accurate {a}: clothes, cars and objects of that time only, no smartphones, no modern cars, no plastic packaging"
COMIDA = ", the food packages are plain colored shapes with no brand names, no logos, no letters"
# Personagens (regra da bíblia: nada de rosto descrito; "round-white-head cartoon …"; nomes reais só no rótulo do código)
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes, wearing an ordinary brown felt hat and a plain brown jacket"
IELTSIN = "a round-white-head cartoon tall Soviet politician of 1989 with a big swept-back white hair shape, a grey suit and a red tie"
HOOVER = "a round-white-head cartoon American official of 1921 with a short parted dark hair shape, a high white collar and a dark three-piece suit"
LENIN = "a round-white-head cartoon Lenin of 1921, bald, with a small pointed dark goatee shape, a dark suit and a dark cloth cap in his hand"
STALIN = "a round-white-head cartoon Stalin with a simple flat dark mustache shape and short dark swept-back hair, in a plain grey tunic without medals"
KHRUSH = "a round-white-head cartoon Khrushchev of 1957, stout and completely bald, in a plain dark suit with a small medal"
LARIONOV = "a round-white-head cartoon provincial Soviet party official of 1959, middle-aged, in a grey suit and a wide grey hat"
LIBERMAN = "a round-white-head cartoon elderly economics professor of 1962 with round glasses and a thin grey hair shape, in a brown tweed jacket"
KOSYGIN = "a round-white-head cartoon Soviet prime minister of 1965 with a simple dark combed hair shape and a serious dark suit"
GORBY = "a round-white-head cartoon Gorbachev of 1985, bald with a simple flat reddish birthmark shape on his head, in a dark suit"
CAMPON = "round-white-head cartoon Russian peasants of 1919 in simple linen shirts, felt boots and headscarves"
POVO80 = "round-white-head cartoon Soviet shoppers of the 1980s in grey and brown winter coats and fur hats"

# ───────── planos por bloco (N001…): imagem nova "chave|prompt", reuso "chave" ou "chave#enq"; "@@TEXTO" = rótulo ─────────
P = {}
# HOOK
P[1] = ["jsc_exterior|The Johnson Space Center campus in Houston in 1989: low modern office buildings, a big Saturn V rocket lying on its side on the lawn, palm-free green lawns and blue Texas sky" + EUA89 + SEMTXT + SEMBAND + "@@HOUSTON, 1989",
        f"ieltsin_arrives|{IELTSIN} stepping out of a dark car in front of a low modern building, curious, with American hosts in suits" + EUA89 + SEMTXT + SEMBAND,
        f"ieltsin_viewer|{IELTSIN} looking straight at the viewer with raised eyebrows, a hand pointing at his own chest, a sunny Texas parking lot behind" + EUA89 + SEMTXT + SEMBAND,
        "houston_road|A wide Texas highway of 1989 with big American cars and a low suburban skyline under a hot blue sky" + EUA89 + SEMTXT]
P[2] = [f"mission_control|{IELTSIN} standing in a 1980s NASA mission control room with rows of consoles and big blank screens, impressed but calm, hands behind his back" + EUA89 + SEMTXT + SEMBAND,
        "station_mockup|A full-size mock-up of a space station module in a huge hangar, cartoon visitors looking up at it" + EUA89 + SEMTXT + SEMBAND,
        "gagarin_memory|Symbolic scene: a small Soviet round capsule spacecraft orbiting a blue Earth, a tiny round-white-head cosmonaut waving from the round window, 1961" + SEMTXT + SEMBAND,
        "supermarket_parking|A low American suburban supermarket building of 1989 with a big parking lot and shopping carts, afternoon light" + EUA89 + SEMTXT,
        f"ieltsin_aisle|{IELTSIN} standing amazed in a bright 1989 American supermarket aisle overflowing with colorful cans, boxes, fruits and meat, mouth open, hands on his cheeks" + EUA89 + COMIDA + SEMTXT + SEMBAND,
        f"ieltsin_quote|Close view of {IELTSIN} holding up a single bright package in a supermarket and turning to his translator, astonished" + EUA89 + COMIDA + SEMTXT + SEMBAND + "@@BORIS IÉLTSIN"]
P[3] = ["pushkin_queue|A very long queue of round-white-head cartoon Muscovites in winter coats and fur hats winding around a snowy city square in January 1990, a modern glass-front fast food restaurant at the end with no logos" + URSS + ANO("1990") + SEMTXT + SEMBAND + "@@MOSCOU, 1990",
        "queue_closeup|Close view of happy, cold round-white-head cartoon Muscovites in fur hats waiting in a queue in the snow, breath steaming" + URSS + ANO("1990") + SEMTXT + SEMBAND,
        "burger_tray|A single tray with a hamburger, fries and a paper cup on a counter, plain packaging with no logos and no letters, a snowy window behind" + COMIDA + SEMTXT,
        "sputnik_shelf|Symbolic split scene: on the left a shiny Sputnik satellite with four long antennas in space, on the right a bare wooden shop shelf with one lonely can" + SEMTXT + SEMBAND,
        "grain_ship_port|A big cargo ship unloading grain with cranes into rail wagons at a cold Soviet port in the 1960s" + URSS + ANO("1963") + SEMTXT + SEMBAND,
        "wheat_sacks_foreign|Stacks of plain grain sacks on a dock being counted by a round-white-head cartoon Soviet clerk with a clipboard" + URSS + ANO("1963") + SEMTXT + SEMBAND]
P[4] = ["rocket_vs_shelf|Symbolic scene: a tall Soviet rocket launching on the left in a glow of fire and, on the right, a long empty grey shop shelf under fluorescent light" + SEMTXT + SEMBAND,
        f"guide_question|{GUIA} standing in an empty Soviet grocery store looking up at the bare shelves, scratching his head, comic" + URSS + SEMTXT + SEMBAND,
        "empty_shelf_hero|Close view of a long empty wooden grocery shelf of the 1980s Soviet Union with only three identical plain cans, cold fluorescent light" + URSS + COMIDA + SEMTXT]
P[5] = ["bread_loaf_light|A single round loaf of dark rye bread on a rough wooden table lit by a window, early 20th century Russian village" + URSS + SEMTXT,
        "map_ussr_blank|Map of the whole Soviet Union seen from above, the territory in a flat warm red-orange color and the rest of the world pale, " + MAPA,
        "petrograd_1917|A snowy Russian city street of 1917 with tram tracks, soldiers in grey greatcoats and crowds in winter clothes, no flags" + URSS + ANO("1917") + SEMTXT + SEMBAND]
# 1. A PROMESSA DO PÃO
P[6] = [f"requisition_door|Armed round-white-head cartoon Red Army men of 1919 in grey greatcoats and pointed cloth hats knocking at the door of a wooden izba in a Volga village, the peasant family worried" + URSS + ANO("1919") + SEMTXT + SEMBAND + GUERRA,
        "barn_emptied|Soldiers of 1919 carrying grain sacks out of a wooden barn onto a horse cart while round-white-head cartoon peasants watch helplessly" + URSS + ANO("1919") + SEMTXT + SEMBAND + GUERRA,
        "seed_sack|Close view of a small sack of seed grain being lifted from a peasant's hands by a soldier's glove" + URSS + SEMTXT + SEMBAND,
        "volga_village|A small wooden village on the high bank of the wide Volga river in 1919, autumn fields, birch trees" + URSS + ANO("1919") + SEMTXT + SEMBAND,
        "cart_leaving|A horse cart loaded with grain sacks leaving a village on a muddy road, peasants left behind at the gate" + URSS + ANO("1919") + SEMTXT + SEMBAND]
P[7] = [f"peasant_explains|A round-white-head cartoon old peasant in a linen shirt pleading and pointing at a field while a soldier shrugs and turns away" + URSS + ANO("1919") + SEMTXT + SEMBAND,
        "field_unsown|An empty unsown field in spring with a broken wooden plough and crows" + URSS + SEMTXT,
        "hungry_city|A cold Russian city of 1919 with round-white-head cartoon people in a long line in front of a closed bakery" + URSS + ANO("1919") + SEMTXT + SEMBAND,
        "army_train|A steam train of 1919 full of round-white-head cartoon soldiers in grey greatcoats, sacks of grain on the roof" + URSS + ANO("1919") + SEMTXT + SEMBAND]
P[8] = [f"lenin_speech|{LENIN} speaking passionately from a wooden platform to a crowd of workers and soldiers in 1917, arm raised" + URSS + ANO("1917") + SEMTXT + SEMBAND,
        "poster_blank|A big revolutionary poster of 1917 glued on a brick wall showing a peasant, a soldier and a worker holding a loaf of bread together, the poster has no letters at all" + URSS + SEMTXT + SEMBAND,
        "three_promises|Symbolic scene: three objects on a table, a white dove, a handful of black earth and a loaf of bread, warm light" + SEMTXT,
        "civil_war_map|Map of western Russia with arrows of two colors clashing across it, smoke shapes over the land, " + MAPA,
        "armored_train|A grey armored train of the Russian Civil War crossing the snowy steppe, smoke, no flags" + URSS + ANO("1919") + SEMTXT + SEMBAND + GUERRA,
        "grain_requisition_post|A requisition point in a village: grain sacks piled high under guard, a round-white-head cartoon commissar writing in a ledger with blank pages" + URSS + ANO("1920") + SEMTXT + SEMBAND]
P[9] = ["dry_volga_fields|Cracked dry fields along the Volga in the summer of 1921, withered wheat, a hot pale sky" + URSS + ANO("1921") + SEMTXT,
        "empty_bowls|Close view of several empty wooden bowls and spoons on a bare table in a peasant hut" + URSS + SEMTXT,
        "map_volga_famine|Map of European Russia with the Volga river basin shaded in dark brown, " + MAPA + "@@VOLGA",
        "refugees_road|Round-white-head cartoon peasant families of 1921 walking on a dusty road with bundles and carts, leaving their village, drawn with dignity, no suffering shown" + URSS + ANO("1921") + SEMTXT + SEMBAND,
        "silent_village|A silent abandoned village with shut wooden houses and an empty well under a grey sky" + URSS + SEMTXT]
P[10] = [f"hoover_desk|{HOOVER} at a big wooden desk in Washington reading a telegram with a frown, an American eagle-free plain office" + SEMTXT + SEMBAND + "@@HERBERT HOOVER",
         f"hoover_grumpy|{HOOVER} with crossed arms looking grumpy at a small cartoon figure of a Bolshevik commissar, comic" + SEMTXT + SEMBAND,
         "ara_ship|An American cargo steamship of 1921 arriving in a Baltic port loaded with crates and flour sacks, plain crates without letters" + ANO("1921") + SEMTXT + SEMBAND,
         f"hoover_child|{HOOVER} kneeling to hand a cup of milk to a small round-white-head cartoon child in a fur hat, warm and gentle" + URSS + ANO("1921") + SEMTXT + SEMBAND,
         "flour_train|A train of wagons loaded with flour sacks crossing a snowy Russian plain in 1922" + URSS + ANO("1922") + SEMTXT + SEMBAND]
P[11] = ["ara_kitchen|A large soup kitchen of 1922 in a Russian village hall: round-white-head cartoon American volunteers ladling soup into bowls for long lines of children" + URSS + ANO("1922") + SEMTXT + SEMBAND,
         "kitchen_children|Close view of round-white-head cartoon children in fur hats eating soup and white bread at a long table, smiling" + URSS + ANO("1922") + SEMTXT + SEMBAND,
         "ten_million|Symbolic scene: an endless line of soup bowls stretching to the horizon over a snowy Russian plain" + URSS + SEMTXT]
P[12] = [f"lenin_soup|{LENIN} looking uneasily at a steaming bowl of American soup on his desk in the Kremlin, comic" + URSS + ANO("1921") + SEMTXT + SEMBAND,
         "kremlin_1921|The Kremlin walls and onion-domed cathedrals in Moscow in 1921 under a grey winter sky, no red stars on the towers" + URSS + ANO("1921") + SEMTXT + SEMBAND,
         "enemy_soup|Symbolic scene: a pot of soup on a border line between two plain flags-free territories, one hand from each side holding the ladle, comic" + SEMTXT + SEMBAND]
# 2. UM PASSO ATRÁS
P[13] = ["nep_market|A busy open-air street market in Moscow in 1922: round-white-head cartoon traders selling white bread, boots and sausages from stalls and carts, crowds of buyers" + URSS + ANO("1922") + COMIDA + SEMTXT + SEMBAND,
         "nep_bread_stall|Close view of a market stall piled with white loaves, a round-white-head cartoon trader in a cap smiling at a customer" + URSS + ANO("1922") + SEMTXT + SEMBAND,
         "nep_boots|A trader holding up a pair of new leather boots to a delighted round-white-head cartoon buyer at a street market" + URSS + ANO("1922") + SEMTXT + SEMBAND,
         "nep_jail_ago|Symbolic comic scene: the same street trader one year earlier hiding a sausage under his coat from a passing patrol" + URSS + ANO("1921") + SEMTXT + SEMBAND]
P[14] = [f"lenin_steps_back|{LENIN} taking one step backwards on a painted line on the floor, hands raised, a group of party men surprised" + URSS + ANO("1921") + SEMTXT + SEMBAND,
         "tax_in_kind|A round-white-head cartoon peasant handing one sack to a clerk and keeping two sacks on his own cart, pleased" + URSS + ANO("1922") + SEMTXT + SEMBAND,
         "shelf_full_1922|A small Moscow shop of 1922 with full wooden shelves of bread, jars and sausages and a happy shopkeeper" + URSS + ANO("1922") + COMIDA + SEMTXT + SEMBAND]
P[15] = ["gosplan_office|A small plain office of 1921 in Moscow with three round-white-head cartoon clerks at wooden desks with abacuses and stacks of blank papers, a single window" + URSS + ANO("1921") + SEMTXT + SEMBAND + "@@GOSPLAN",
         "abacus_close|Close view of a wooden abacus and a pencil on a blank ledger" + SEMTXT,
         "gosplan_grows|Symbolic scene: a tiny plain office desk casting a giant shadow over a whole map of a country on the wall" + SEMTXT + SEMBAND,
         f"guide_note|{GUIA} tapping his temple knowingly next to a small office door, comic" + URSS + SEMTXT + SEMBAND]
P[16] = ["scissors|Symbolic scene: a giant pair of open scissors, one blade made of factory goods (a plough, boots, a kettle) going up and the other made of wheat ears going down" + SEMTXT,
         "plough_price|A round-white-head cartoon peasant staring shocked at a shiny new iron plough in a shop of 1923, holding a small sack of grain" + URSS + ANO("1923") + SEMTXT + SEMBAND]
P[17] = ["peasant_hoards|A round-white-head cartoon peasant closing the door of a barn full of grain sacks, winking at the viewer" + URSS + ANO("1927") + SEMTXT + SEMBAND,
         "barn_lock|Close view of a heavy padlock on a wooden barn door, a few wheat ears peeking out" + URSS + SEMTXT]
P[18] = ["state_buyer|A state grain purchase point with empty scales and a bored round-white-head cartoon official waiting, no peasants coming" + URSS + ANO("1928") + SEMTXT + SEMBAND,
         "bread_queue_1928|A long queue of round-white-head cartoon city people in front of a bakery in 1928, winter" + URSS + ANO("1928") + SEMTXT + SEMBAND,
         f"stalin_idea|{STALIN} in a dim Kremlin office with a pipe, looking at a map of farmland with a stern idea, smoke" + URSS + ANO("1928") + SEMTXT + SEMBAND + "@@STÁLIN",
         "harvest_good|Golden wheat fields of a good harvest in southern Russia, haystacks, 1926" + URSS + ANO("1926") + SEMTXT]
# 3. DOIS MAIS DOIS, CINCO
P[19] = ["poster_225|A 1931 Soviet propaganda poster on a factory wall: a giant bold red graphic 2 + 2 = 5 made of plain shapes, workers marching below" + URSS + ", the only characters are the big 2, plus, 2, equals, 5, no other letters" + SEMBAND,
         f"guide_poster|{GUIA} staring at a huge red 2 + 2 = 5 poster and counting on his fingers, confused, comic" + URSS + ", the only characters are 2 + 2 = 5, no other letters" + SEMBAND]
P[20] = ["workers_cheer|Enthusiastic round-white-head cartoon Soviet workers of 1931 in overalls cheering in front of a half-built factory with scaffolding" + URSS + ANO("1931") + SEMTXT + SEMBAND,
         "calendar_fast|Symbolic scene: five wall calendar sheets being squeezed into four by two hands, the sheets are blank grids with no numbers" + SEMTXT,
         "result_first|Symbolic comic scene: a round-white-head cartoon clerk writing the result of a sum on a blackboard before the numbers, the board has only plain shapes" + SEMTXT + SEMBAND]
P[21] = ["steel_mill|A gigantic new steel mill of the early 1930s with blast furnaces, chimneys and sparks, tiny workers" + URSS + ANO("1932") + SEMTXT + SEMBAND,
         "dam_build|A huge concrete dam under construction on a wide river with cranes and crowds of workers, 1932" + URSS + ANO("1932") + SEMTXT + SEMBAND,
         "tractor_line|A row of new identical tractors rolling out of a factory gate in 1931" + URSS + ANO("1931") + SEMTXT + SEMBAND,
         "shelf_later|Symbolic scene: an empty grocery shelf with a small blank paper tag hanging on it, dusty, in a 1930s Soviet shop" + URSS + SEMTXT]
P[22] = ["fields_merged|Aerial view of many small strip fields of family farms being merged into one huge collective field by tractors" + URSS + ANO("1930") + SEMTXT + SEMBAND,
         "kolkhoz_delivery|Round-white-head cartoon collective farmers of 1931 loading grain sacks onto a state truck while an official counts, nobody smiling" + URSS + ANO("1931") + SEMTXT + SEMBAND]
P[23] = ["spikelets_field|A harvested collective wheat field at dusk with a few fallen wheat ears on the ground and a wooden watchtower in the distance" + URSS + ANO("1932") + SEMTXT + SEMBAND,
         "spikelet_hand|Close view of a small hand picking up a single fallen wheat ear from the stubble" + URSS + SEMTXT,
         "watchtower|A guard on a tall wooden watchtower above a collective field, seen from below, grey sky" + URSS + ANO("1932") + SEMTXT + SEMBAND + GUERRA,
         "famine_empty_hut|The inside of an empty peasant hut with a cold stove, an empty bread box and a lit candle, quiet and sad, no people" + URSS + SEMTXT,
         "map_famine_1932|Map of the southern Soviet Union with Ukraine and Kazakhstan shaded in dark grey, " + MAPA]
P[24] = ["ration_card_bread|Close view of a plain paper ration card with empty squares being handed over a bakery counter in 1932" + URSS + ", the card has only empty squares and no letters or numbers" + SEMBAND,
         "avoska_pocket|A round-white-head cartoon Soviet man of the 1930s pulling a folded string net bag out of his coat pocket on a street, hopeful" + URSS + ANO("1935") + SEMTXT + SEMBAND,
         "avoska_hero|A single empty string net shopping bag with thick cream cord mesh hanging from a hook against a plain wall" + SEMTXT,
         "avoska_maybe|A round-white-head cartoon woman of the 1930s spotting a shop with a short queue and opening her string net bag, eyes lit up" + URSS + ANO("1935") + SEMTXT + SEMBAND]
P[25] = [f"stalin_merrier|{STALIN} speaking at a podium in a grand hall in 1935, smiling, hands raised, an audience of workers applauding" + URSS + ANO("1935") + SEMTXT + SEMBAND,
         "bakery_open|A Moscow bakery of 1935 with bread freely on the shelves and a round-white-head cartoon shop assistant tearing up a ration card" + URSS + ANO("1935") + COMIDA + SEMTXT + SEMBAND,
         "avoska_still|A round-white-head cartoon man walking out of an applauding hall with a string net bag still poking out of his pocket, deadpan" + URSS + ANO("1935") + SEMTXT + SEMBAND]
P[26] = ["one_big_thing|Symbolic scene: a giant steel girder lifted by a huge crane over a tiny empty grocery stall below, 1930s" + URSS + SEMTXT + SEMBAND,
         "next_plan_folder|Symbolic scene: a stack of thick blank planning folders on a desk, a small picture of a grocery shelf placed under the very last one" + SEMTXT,
         "door_knock_1941|A heavy wooden door shaking as something big knocks from outside, dramatic light, 1941" + SEMTXT + SEMBAND]
# 4. A FÁBRICA NO TREM
P[27] = ["factory_dismantled|Round-white-head cartoon workers of 1941 dismantling big machines in a factory hall and loading them onto flat rail wagons, urgent" + URSS + ANO("1941") + SEMTXT + SEMBAND,
         "machine_train|A long freight train carrying lathes and factory machines on open wagons through a birch forest toward the east, 1941" + URSS + ANO("1941") + SEMTXT + SEMBAND,
         "urals_rebuild|Workers rebuilding a factory in the snow at the foot of the Ural mountains, machines under the open sky, 1941" + URSS + ANO("1941") + SEMTXT + SEMBAND]
P[28] = ["map_evacuation|Map of the Soviet Union with many small arrows running from the west to the Ural mountains and beyond, " + MAPA + "@@URAIS",
         "night_trains|Many trains crossing a snowy plain at night toward the east, steam and small lights" + URSS + ANO("1941") + SEMTXT + SEMBAND]
P[29] = ["tanks_roll|Green tanks rolling out of a snowy factory gate in the Urals in 1942, no stars on the tanks, no flags" + URSS + ANO("1942") + SEMTXT + SEMBAND + GUERRA,
         "shelf_wartime|An empty shop shelf with a single blank wartime notice pinned to it, cold light, 1942" + URSS + SEMTXT]
P[30] = ["bread_queue_1943|Round-white-head cartoon women and old men of 1943 in a long silent queue with ration cards in front of a bakery in the snow" + URSS + ANO("1943") + SEMTXT + SEMBAND,
         "drought_1946|Parched cracked fields with stunted wheat under a burning sun in 1946" + URSS + ANO("1946") + SEMTXT,
         "village_postwar|A poor war-damaged village of 1946 with patched wooden houses and a few thin cows" + URSS + ANO("1946") + SEMTXT + SEMBAND]
P[31] = ["ruble_exchange|A bank counter of December 1947 where a round-white-head cartoon clerk takes a thick pile of old banknotes and gives back one thin note, plain notes without numbers" + URSS + ANO("1947") + SEMTXT + SEMBAND,
         "mattress_shrinks|Symbolic comic scene: a round-white-head cartoon man lifting his mattress and finding a tiny shrunken pile of banknotes, shocked" + URSS + ANO("1947") + SEMTXT + SEMBAND,
         "ration_end_shop|A 1947 Soviet shop with a few loaves and jars back on the shelves, shoppers with no ration cards" + URSS + ANO("1947") + COMIDA + SEMTXT + SEMBAND]
P[32] = ["victory_calm|A quiet postwar Moscow street of 1948 with rebuilt houses and a tram, people walking calmly" + URSS + ANO("1948") + SEMTXT + SEMBAND,
         f"guide_peace|{GUIA} sitting on a crate in an empty factory yard, chin in hand, wondering, comic" + URSS + SEMTXT + SEMBAND]
# 5. ALCANÇAR A AMÉRICA
P[33] = ["leningrad_1957|The embankment of Leningrad in 1957 with classical palaces along the Neva river" + URSS + ANO("1957") + SEMTXT + SEMBAND,
         f"khrush_leningrad|{KHRUSH} on a stage at an agricultural meeting in Leningrad in 1957, fist raised, shouting enthusiastically to a hall of farm officials" + URSS + ANO("1957") + SEMTXT + SEMBAND + "@@NIKITA KHRUSCHOV"]
P[34] = ["meat_milk_butter|Symbolic scene: a race track where a cartoon Soviet cow, a milk can and a butter block run against an American cow, comic" + SEMTXT + SEMBAND,
         "us_farm_plenty|An American dairy farm of the 1950s with fat cows, red barns and silos" + ANO("1957") + SEMTXT + SEMBAND]
P[35] = ["sputnik_orbit|The shiny Sputnik satellite with four long antennas orbiting above the blue Earth, 1957" + SEMTXT + SEMBAND,
         "butcher_empty|A Soviet butcher shop of 1957 with empty hooks and a bored round-white-head cartoon butcher, a queue outside" + URSS + ANO("1957") + SEMTXT + SEMBAND]
P[36] = [f"larionov_promise|{LARIONOV} at a podium in a provincial hall promising with three raised fingers, applause" + URSS + ANO("1959") + SEMTXT + SEMBAND + "@@RIAZAN, 1959",
         "ryazan_town|A provincial Russian town of 1959 with a kremlin wall, onion domes and wooden houses in winter" + URSS + ANO("1959") + SEMTXT + SEMBAND]
P[37] = ["meat_trucks|Trucks of 1959 loaded with meat carcass shapes covered by tarps driving into a provincial town at night, secretive" + URSS + ANO("1959") + SEMTXT + SEMBAND,
         "cows_led_away|Round-white-head cartoon farm workers leading a long line of dairy cows and calves away from a collective farm barn, sad farmer watching" + URSS + ANO("1959") + SEMTXT + SEMBAND,
         f"larionov_medal|{LARIONOV} receiving a gold star medal on a stage, beaming" + URSS + ANO("1959") + SEMTXT + SEMBAND]
P[38] = ["empty_barn_1960|An empty collective farm cow barn with empty stalls and scattered hay, 1960" + URSS + ANO("1960") + SEMTXT + SEMBAND,
         f"larionov_falls|{LARIONOV} alone in a dark office with an empty chair and a closed folder, his medal on the desk, sad, no violence" + URSS + ANO("1960") + SEMTXT + SEMBAND]
P[39] = [f"khrush_iowa|{KHRUSH} in a tall green Iowa cornfield in 1959 holding up a huge corn cob, delighted, with an American farmer in overalls" + ANO("1959") + SEMTXT + SEMBAND + "@@IOWA, 1959",
         "corn_everywhere|Symbolic map-like scene of the Soviet Union where small corn plants sprout everywhere, even in snowy northern areas, comic" + SEMTXT + SEMBAND,
         "corn_frozen|A sad thin corn plant frozen in a snowy Russian field, a round-white-head cartoon farmer shrugging" + URSS + ANO("1960") + SEMTXT + SEMBAND]
P[40] = ["rocket_order|Symbolic scene: a single red button on a control desk and a rocket rising beyond the window" + SEMTXT + SEMBAND,
         "seed_eaten|Symbolic scene: on the left a sack of seed grain carried away in 1919, on the right a breeding cow led away in 1959, same grey sky" + URSS + SEMTXT + SEMBAND,
         "volga_village", "cows_led_away#detalhe-centro"]
# 6. COMUNISMO COM DATA MARCADA
P[41] = ["congress_1961|A huge modern congress hall in the Kremlin in 1961 with thousands of round-white-head cartoon delegates and a speaker on a distant stage" + URSS + ANO("1961") + SEMTXT + SEMBAND,
         "agenda_1980|Close view of a desk diary with blank pages and a pencil circling an empty square, comic" + SEMTXT,
         f"khrush_program|{KHRUSH} reading a thick document at a podium, pointing to a bright future painted on the wall as a sunny city" + URSS + ANO("1961") + SEMTXT + SEMBAND]
P[42] = ["vostok_launch|A Soviet rocket launching from the steppe in April 1961 with a great plume, crowds of tiny workers watching" + URSS + ANO("1961") + SEMTXT + SEMBAND,
         "gagarin_parade|Round-white-head cartoon crowds celebrating in a Moscow street in 1961 holding up portraits shapes and flowers, a cosmonaut in a car" + URSS + ANO("1961") + SEMTXT + SEMBAND]
P[43] = ["price_tags|Close view of a butcher's counter in 1962 with blank price cards being replaced by bigger blank price cards" + URSS + ", cards completely blank" + SEMBAND,
         "butter_block|A block of butter on a scale with a counterweight being added, a shocked round-white-head cartoon housewife" + URSS + ANO("1962") + SEMTXT + SEMBAND]
P[44] = ["nevz_strike|Round-white-head cartoon factory workers of 1962 in work clothes walking out of a big locomotive factory gate on strike, arms crossed" + URSS + ANO("1962") + SEMTXT + SEMBAND + "@@NOVOCHERKASSK",
         "march_square|A crowd of workers marching peacefully toward a town square with an administrative building in 1962, soldiers in a line far away" + URSS + ANO("1962") + SEMTXT + SEMBAND + GUERRA,
         "empty_square_dawn|An empty town square at dawn with a fallen cap on the cobblestones and pigeons, silent, no people, no blood" + URSS + ANO("1962") + SEMTXT + SEMBAND]
P[45] = ["failed_harvest|A thin failed wheat harvest on dry steppe in 1963, dust blowing" + URSS + ANO("1963") + SEMTXT,
         "canada_port|A Canadian grain port in 1963 with tall grain elevators loading wheat into a ship, cold lake water" + ANO("1963") + SEMTXT + SEMBAND,
         "map_canada_ussr|World map centered on the North Atlantic with a dotted golden route from Canada across the ocean to a Soviet Baltic port, " + MAPA]
P[46] = ["bread_ocean|Symbolic scene: a loaf of bread sailing across the ocean on a tiny ship toward a Soviet family table" + SEMTXT + SEMBAND,
         "factory_tons|A Soviet factory of 1963 proudly weighing a giant pile of identical heavy boots on a big scale while customers outside shake their heads" + URSS + ANO("1963") + SEMTXT + SEMBAND,
         "scoreboard|Symbolic scene: an old wooden scoreboard with only plain blank tiles and one giant weight icon, a round-white-head cartoon official proud in front of it" + SEMTXT + SEMBAND]
# 7. A PRATELEIRA EMPRESTADA
P[47] = ["newspaper_read|A round-white-head cartoon man on a tram in 1962 reading a big newspaper with blank columns, eyebrows raised" + URSS + ANO("1962") + ", the newspaper is completely blank with only grey bars" + SEMBAND,
         f"liberman_paper|{LIBERMAN} at a desk covered with papers in Kharkov in 1962, writing an article with a fountain pen, a lamp" + URSS + ANO("1962") + SEMTXT + SEMBAND + "@@EVSEI LIBERMAN"]
P[48] = ["factory_bonus|A factory manager of 1965 receiving an envelope bonus while customers happily carry the factory's shoes away" + URSS + ANO("1965") + SEMTXT + SEMBAND,
         f"kosygin_reform|{KOSYGIN} presenting a plan at a long table in the Kremlin to grey-suited officials, some frowning" + URSS + ANO("1965") + SEMTXT + SEMBAND + "@@ALEXEI KOSSYGUIN",
         "reform_drawer|Symbolic scene: a thin reform folder being slowly pushed into a drawer by many hands, 1968" + SEMTXT + SEMBAND]
P[49] = ["us_wheat_1972|Huge American grain elevators and a long freight train of hopper cars in Kansas in 1972" + ANO("1972") + SEMTXT + SEMBAND,
         "ship_odessa|A big grain freighter unloading at a Soviet Black Sea port in 1972, cranes" + URSS + ANO("1972") + SEMTXT + SEMBAND]
P[50] = ["grain_deal_1975|Two round-white-head cartoon diplomats in dark suits shaking hands over a signed blank document with wheat ears on the table, 1975" + ANO("1975") + SEMTXT + SEMBAND,
         "corn_wheat_pile|A huge pile of yellow corn and golden wheat being poured from a chute into a ship's hold" + SEMTXT + SEMBAND,
         "contract_calendar|Symbolic scene: five blank calendar sheets with a small grain sack drawn on each one, pinned on a wall" + SEMTXT]
P[51] = ["shelf_70s|A Soviet grocery of the 1970s with modest but present goods on shelves and a calm queue" + URSS + ANO("1975") + COMIDA + SEMTXT + SEMBAND,
         "avoska_70s|A round-white-head cartoon woman of the 1970s with an orange string net bag holding two oranges and a loaf, walking past apartment blocks" + URSS + ANO("1978") + SEMTXT + SEMBAND,
         "olympics_1980|A big stadium of 1980 in Moscow with fireworks and a giant friendly cartoon bear mascot balloon, no logos, no rings" + URSS + ANO("1980") + SEMTXT + SEMBAND,
         "avoska_hero#detalhe-centro"]
P[52] = ["food_program|A round-white-head cartoon old Soviet leader of 1982 with thick dark eyebrow shapes signing yet another thick blank plan folder, a pile of earlier folders beside him" + URSS + ANO("1982") + SEMTXT + SEMBAND,
         "plans_tower|Symbolic comic scene: a tall wobbly tower of planning folders, each one patching a hole in the one below" + SEMTXT]
P[53] = ["outside_help|Symbolic scene: three hands from outside the frame filling an empty Soviet shop shelf, one with soup, one with wheat sacks, one with corn" + SEMTXT + SEMBAND,
         "ara_kitchen#detalhe-alto", "canada_port#médio-dir", "us_wheat_1972#médio-esq",
         "gift_with_tag|A big gift box with a blank tag tied with string being handed across a table by a hand in a suit sleeve" + SEMTXT]
# 8. O AÇÚCAR SUMIU
P[54] = ["vodka_shop_closed|A Soviet liquor shop of 1985 with a closed door and a long grumpy queue of men waiting for the opening hour" + URSS + ANO("1985") + SEMTXT + SEMBAND,
         f"gorby_alcohol|{GORBY} at a desk in 1985 pushing away a bottle of vodka with a firm hand, determined" + URSS + ANO("1985") + SEMTXT + SEMBAND + "@@MIKHAIL GORBATCHOV"]
P[55] = ["home_still|A round-white-head cartoon man in a tiny Soviet kitchen of 1986 secretly brewing in a big pot with copper tubes, a sugar sack beside him, comic" + URSS + ANO("1986") + SEMTXT + SEMBAND,
         "sugar_gone|An empty grocery shelf where sugar should be, a single paper bag fallen over, shoppers disappointed, 1987" + URSS + ANO("1987") + COMIDA + SEMTXT + SEMBAND,
         "sugar_coupon|Close view of a plain paper coupon with empty squares and a small drawn sugar cube shape, held by a hand in a woolly mitten" + URSS + ", no letters or numbers" + SEMBAND]
P[56] = ["budget_hole|Symbolic comic scene: a round-white-head cartoon finance official looking into a huge empty safe, coins rolling away" + URSS + SEMTXT + SEMBAND]
P[57] = ["oil_price_fall|Symbolic scene: a big oil barrel tumbling down a staircase, coins spilling out" + SEMTXT + SEMBAND,
         "chernobyl_plant|A nuclear power plant on flat land in April 1986 at dusk with a plume of smoke rising from one building, distant, no people" + URSS + ANO("1986") + SEMTXT + SEMBAND]
P[58] = ["butter_vs_sugar|Symbolic scene: an old 1957 butter-race poster shape faded on a wall above an empty sugar shelf in 1988" + URSS + SEMTXT + SEMBAND,
         "everyone_watching|Round-white-head cartoon Soviet families of 1988 watching an honest news report on a boxy TV set showing an empty shop, surprised" + URSS + ANO("1988") + SEMTXT + SEMBAND]
# 9. A VOLTA DE HOUSTON
P[59] = ["ieltsin_aisle#detalhe-centro",
         f"ieltsin_plane|{IELTSIN} sitting by the window of an airplane at night, thoughtful, looking down at the dark ocean" + ANO("1989") + SEMTXT + SEMBAND,
         f"ieltsin_moscow|{IELTSIN} walking through a grey Moscow street of 1989 past an empty shop window, serious" + URSS + ANO("1989") + SEMTXT + SEMBAND]
P[60] = ["leningrad_coupons|A Leningrad shop of 1989 where a round-white-head cartoon cashier tears coupons from a sheet with empty squares, tea and soap on the counter" + URSS + ANO("1989") + COMIDA + ", coupons with only empty squares, no letters" + SEMBAND + "@@LENINGRADO",
         "coupon_sheet|Close view of a plain sheet of ration coupons with only empty squares and small drawn shapes of a tea cup, a soap bar, a sugar cube and a cigarette" + ", no letters, no numbers" + SEMBAND]
P[61] = ["pushkin_square|Pushkin Square in Moscow on a snowy morning in January 1990 with the bronze statue of the poet on a pedestal and a modern glass-front restaurant behind, no logos" + URSS + ANO("1990") + SEMTXT + SEMBAND + "@@PRAÇA PÚCHKIN",
         "pushkin_queue#detalhe-alto",
         "counter_rush|Busy round-white-head cartoon young staff in plain uniforms serving a crowd at a long fast food counter, no logos" + URSS + ANO("1990") + COMIDA + SEMTXT + SEMBAND]
P[62] = ["four_rubles|Close view of a hand counting a few Soviet coins and a small plain banknote on a counter next to a sandwich box, no numbers on the money" + URSS + COMIDA + SEMTXT + SEMBAND,
         "queue_around|Aerial view of a long queue curling around a snowy city square like a snake, 1990" + URSS + ANO("1990") + SEMTXT + SEMBAND]
P[63] = ["berlin_reserve|A huge old warehouse in Berlin in 1990 stacked with crates and sacks of food reserves, round-white-head cartoon workers loading them" + ANO("1990") + SEMTXT + SEMBAND,
         "aid_train|A freight train loaded with food crates leaving Germany for the east in December 1990, snow" + ANO("1990") + SEMTXT + SEMBAND,
         "airlift_memory|Symbolic scene: a 1948 cargo propeller plane flying over the ruins of Berlin dropping supplies, sepia-tinted sky" + ANO("1948") + SEMTXT + SEMBAND]
P[64] = ["ara_kitchen#médio-esq", "aid_moscow|Round-white-head cartoon Muscovites of 1990 receiving food parcels from a truck in the snow" + URSS + ANO("1990") + SEMTXT + SEMBAND,
         "berlin_reserve#detalhe-centro"]
P[65] = ["republics_leave|Map of the Soviet Union with the borders of the fifteen republics as thin lines, some republics glowing and slightly drifting apart, " + MAPA,
         "why_stay|Symbolic scene: a big empty dinner table with fifteen chairs, several of them being pushed back" + SEMTXT + SEMBAND]
# 10. O ÚLTIMO PREÇO
P[66] = ["price_triple|A round-white-head cartoon woman in a 1991 Soviet bakery staring at a loaf whose blank price card has grown three times bigger overnight, comic shock" + URSS + ANO("1991") + SEMTXT + SEMBAND,
         "wake_price|A round-white-head cartoon man waking up in bed in 1991 and reading a blank newspaper with his hair standing up" + URSS + ANO("1991") + ", the newspaper is blank" + SEMBAND]
P[67] = ["shelves_still_empty|A long Soviet store of 1991 with all shelves empty and a few shoppers wandering" + URSS + ANO("1991") + SEMTXT + SEMBAND,
         "avoska_light|A round-white-head cartoon old woman of 1991 walking home along a snowy street swinging an almost empty string net bag" + URSS + ANO("1991") + SEMTXT + SEMBAND]
P[68] = ["tanks_august|Tanks parked calmly on a wide Moscow avenue in August 1991 with round-white-head cartoon citizens talking to the crews, no flags, no fighting" + URSS + ANO("1991") + SEMTXT + SEMBAND + GUERRA,
         "kremlin_dusk_1991|The Kremlin towers and walls at dusk in December 1991 with snow, an empty flagpole on the dome, quiet" + URSS + ANO("1991") + SEMTXT + SEMBAND]
P[69] = ["shelves_full_1992|A Moscow store of early 1992 suddenly full of goods on the shelves, and round-white-head cartoon shoppers staring at the price cards with shock" + URSS + ANO("1992") + COMIDA + SEMTXT + SEMBAND,
         "street_sellers_92|Round-white-head cartoon people of 1992 selling goods on a cold Moscow sidewalk from boxes" + URSS + ANO("1992") + SEMTXT + SEMBAND]
# FECHO
P[70] = ["rocket_vs_shelf#detalhe-centro", "seed_eaten#aberto", "outside_help#médio-dir",
         "next_plan_folder#detalhe-alto",
         f"guide_answer|{GUIA} standing between a model rocket and a grocery shelf, explaining with open hands" + URSS + SEMTXT + SEMBAND]
P[71] = ["avoska_hero#médio-esq", "pushkin_today|Pushkin Square in Moscow on a calm summer day of 2022 with the poet's statue and a modern restaurant with no logos, people walking" + ANO("2022") + SEMTXT + SEMBAND]
P[72] = [f"guide_end|{GUIA} holding an empty string net bag and waving at the viewer in a sunny modern street market, smiling" + SEMTXT + SEMBAND]

# ───────────────────────── HOOK (Houston, 1989) ─────────────────────────
cap("Hook")
b("[curious] Houston, setembro de mil novecentos e oitenta e nove. Imagine que você é Boris Iéltsin, deputado soviético, visitando os Estados Unidos.")
b("De manhã, o controle de missão da NASA. Nada de novo: o seu país pôs o primeiro homem no espaço. À tarde, um supermercado. E ele diz: nem o Politburo tem essa escolha.")
b("Quatro meses depois, em Moscou, cerca de trinta mil pessoas enfrentam a fila de uma lanchonete americana. Num só dia. E o país do Sputnik comprava trigo do exterior desde sessenta e três.")
b("[serious] Então fica a pergunta: como o país que chegou primeiro ao espaço não conseguia encher uma prateleira?")
b("Essa é a história inteira da União Soviética. E ela começa com uma promessa de pão.")

# ───────────────────────── 1. PAZ, TERRA E PÃO ─────────────────────────
cap("1. A promessa do pão")
b("§ Uma aldeia na beira do rio Volga, mil novecentos e dezenove. Homens armados batem na porta. Levam o trigo do celeiro. E levam também a semente da próxima safra.", card="1919")
b("Tente explicar a eles que aquilo era o plantio do ano que vem. Não adianta: a cidade tem fome, e o exército também.")
b("Dois anos antes, os bolcheviques tinham tomado o poder com um lema que cabia num cartaz: paz, terra e pão. Só que a paz virou guerra civil. E o pão virou requisição.")
b("§ Então veio a conta. Em mil novecentos e vinte e um, a fome cobre o Volga. Morrem milhões de pessoas; a estimativa mais citada fala em cerca de cinco milhões.")
b("E quem aparece com comida? Pense na ironia: Herbert Hoover, um americano que detestava os bolcheviques. Só que detestava mais ainda ver criança com fome.", card="1921")
b("No auge, as cozinhas americanas alimentam mais de dez milhões de pessoas por dia. Guarde esses americanos com comida.")
b("O problema é óbvio: um governo que prometeu pão não pode viver da sopa do país que ele chama de inimigo.")

# ───────────────────────── 2. O RECUO ─────────────────────────
cap("2. Um passo atrás")
b("§ Moscou, mil novecentos e vinte e dois. Num mercado de rua, você encontra pão branco, botas, salsicha. Um ano antes, vender isso na rua era crime.", card="1922")
b("Então Lênin recuou. A requisição virou imposto, e o camponês podia vender o que sobrava. A prateleira, por um momento, enche.")
b("No mesmo ano do recuo, nasce um escritório discreto para fazer contas: a Comissão Estatal de Planejamento, o Gosplan. Repare nesse nome: daqui a pouco, ele vai mandar em tudo.")
b("§ Mas aí aparece a tesoura. Os produtos da cidade ficam caros, o trigo fica barato. O que sai da fábrica custa quase três vezes o que custava antes da guerra.")
b("E o camponês responde como você responderia: segura o trigo no celeiro e espera um preço melhor.")
b("Em mil novecentos e vinte e oito, mesmo depois de safras boas, o Estado não consegue comprar grão. As cidades voltam a ter fila. E o homem que agora manda em Moscou, Stálin, tem outra ideia. O problema é que ela não cabe num mercado de rua.")

# ───────────────────────── 3. DOIS MAIS DOIS, CINCO ─────────────────────────
cap("3. Dois mais dois, cinco")
b("§ Olhe para este cartaz de mil novecentos e trinta e um. Em letras vermelhas enormes: dois mais dois igual a cinco.", card="1931")
b("A ideia é que o entusiasmo dos operários faz o plano de cinco anos sair em quatro. Matemática soviética: o resultado vem antes da conta.")
b("O Gosplan agora escreve o país inteiro em metas. Aço, carvão, represas, tratores. Primeiro a indústria pesada. A prateleira? Fica para o próximo plano.")
b("§ E a crise de vinte e oito ganha uma resposta de ferro: se o camponês segura o trigo, o Estado fica com a terra. As fazendas de família viram fazendas coletivas, e o grão passa a ser entregue, não vendido.")
b("[serious] Em agosto de trinta e dois, uma lei transforma em crime grave pegar espigas no campo coletivo, mesmo as que sobraram no chão. Imagine ser preso por catar trigo. Naquele ano e no seguinte, a fome deixa milhões de vítimas, sobretudo na Ucrânia e no Cazaquistão.", card="1932")
b("§ Se você morasse numa cidade, o pão vinha com cartão de racionamento. E o povo aprende a andar com uma sacola de rede no bolso: a avoska. O nome vem de avos, algo como vai que. Vai que aparece alguma coisa.")
b("Em mil novecentos e trinta e cinco, o cartão do pão acaba. E Stálin anuncia: a vida ficou melhor, camaradas. A vida ficou mais alegre. Repare que a sacola continua no bolso.", card="1935")
b("Aqui está a primeira peça da resposta: a prateleira é sempre o próximo plano. O de agora tem uma urgência maior. O problema é quando a urgência maior bate na porta.")

# ───────────────────────── 4. O PLANO VAI À GUERRA ─────────────────────────
cap("4. A fábrica no trem")
b("§ Verão de mil novecentos e quarenta e um. Imagine desmontar a sua fábrica parafuso por parafuso, pôr tudo num trem e remontar do outro lado dos Urais. No inverno.", card="1941")
b("Foi o que aconteceu quando a Alemanha invadiu. Em um ano e pouco, mais de mil e quinhentas grandes fábricas de armamento viajaram para o leste.")
b("Os tanques saem dessas fábricas remontadas no frio. E a prateleira, mais uma vez, fica para o próximo plano.")
b("§ Só que a prateleira paga a conta de novo. Olhe a fila do pão: voltou, e com cartão. E, depois da vitória, uma seca traz outra fome, em mil novecentos e quarenta e seis e quarenta e sete.")
b("Então, em dezembro de quarenta e sete, o racionamento acaba, junto com uma troca de moeda: dez rublos velhos por um novo. Quem escondia dinheiro no colchão descobriu que o colchão tinha encolhido.", card="1947")
b("O plano provou que vence uma guerra. Mas o que ele faz quando não tem guerra para vencer?")

# ───────────────────────── 5. ALCANÇAR A AMÉRICA ─────────────────────────
cap("5. Alcançar a América")
b("§ Leningrado, maio de mil novecentos e cinquenta e sete. Numa reunião sobre agricultura, Nikita Khruschov sobe ao palco e diz: vamos alcançar e ultrapassar a América.", card="1957")
b("Repare: não em foguetes. Em carne, leite e manteiga por habitante. Em poucos anos.")
b("Cinco meses depois, o Sputnik está em órbita. No céu, a América já foi alcançada. No açougue, ainda não.")
b("§ Riazan, mil novecentos e cinquenta e nove. O chefe local do partido, Alexei Larionov, promete triplicar a entrega de carne em um ano. E entrega.", card="1959")
b("Como? Você não vai gostar: comprando carne das regiões vizinhas e abatendo o rebanho às pressas, inclusive vacas leiteiras e de cria. Ganha medalha de herói.")
b("Mas, no ano seguinte, o rebanho da região cai quase dois terços. A carne some. Larionov cai em desgraça e morre poucos meses depois; a versão oficial fala em doença.")
b("§ Khruschov, enquanto isso, visita uma fazenda de milho em Iowa e volta encantado. Agora o país inteiro vai plantar milho. Só que o milho não nasce onde o plano manda; nasce onde o clima deixa.")
b("Segunda peça da resposta: quando a prateleira finalmente vira urgência, a pressa come a semente. Em dezenove, o trigo do plantio. Em cinquenta e nove, as vacas de cria. Só que semente comida não volta no ano seguinte.")

# ───────────────────────── 6. COMUNISMO EM 1980 ─────────────────────────
cap("6. Comunismo com data marcada")
b("§ Moscou, outubro de mil novecentos e sessenta e um. No congresso do partido, o novo programa promete: a base do comunismo estará pronta em mil novecentos e oitenta. Você pode marcar na agenda.", card="1961")
b("Naquele mesmo ano, Gagarin tinha dado a volta na Terra. Parecia que nada era impossível.")
b("§ Mas em maio de sessenta e dois, o governo aumenta o preço da carne em trinta por cento e o da manteiga em vinte e cinco.", card="1962")
b("[serious] Em Novocherkassk, operários de uma fábrica de locomotivas entram em greve. O exército atira. Morrem vinte e seis pessoas, e o país só fica sabendo mais de vinte e cinco anos depois.")
b("§ Aí, em sessenta e três, a colheita falha. E o país que pôs o primeiro homem em órbita faz a primeira grande compra de trigo no exterior: uns seis milhões e meio de toneladas do Canadá.", card="1963")
b("Pense nisso: dois anos depois de Gagarin, o pão de muita mesa soviética atravessava o oceano. E a fábrica soviética continuava ganhando prêmio pela tonelada produzida, não pelo que o povo queria comprar. Quem ia mudar esse placar?")

# ───────────────────────── 7. A PRATELEIRA EMPRESTADA ─────────────────────────
cap("7. A prateleira emprestada")
b("§ Uma resposta tinha saído no jornal. Kharkov, setembro de mil novecentos e sessenta e dois: um professor de economia, Evsei Liberman, publica no Pravda um artigo de título ousado. Plano, lucro, prêmio.", card="1962")
b("A ideia: a fábrica que vende o que o povo quer ganha prêmio. Parece óbvio para você. Em sessenta e cinco, o primeiro-ministro, Alexei Kossyguin, tenta aplicar. A partir de sessenta e oito, a reforma vai sendo esvaziada, sem barulho.", card="1965")
b("§ Então, em mil novecentos e setenta e dois, a União Soviética compra uns dezoito milhões de toneladas de grãos dos Estados Unidos. Os americanos com comida, de novo.", card="1972")
b("E aí você pergunta: foi só uma emergência? Não. Em setenta e cinco, Moscou assina com Washington um acordo de cinco anos: comprar, todo ano, no mínimo seis milhões de toneladas de trigo e milho americanos. A compra de emergência vira contrato.", card="1975")
b("§ A prateleira melhora. Só que a avoska continua no bolso. E a piada da época diz: prometeram o comunismo para oitenta; em oitenta, veio a Olimpíada.", card="1980")
b("Então, em oitenta e dois, o governo lança mais um plano, só para a comida: o Programa Alimentar. Mais um plano para consertar o que o plano anterior não fez.")
b("Terceira peça da resposta: quando a falta aperta de verdade, quem enche a prateleira é alguém de fora. Hoover em vinte e um, o Canadá em sessenta e três, os americanos em setenta e dois. Mas todo socorro tem dono.")

# ───────────────────────── 8. O AÇÚCAR SUMIU ─────────────────────────
cap("8. O açúcar sumiu")
b("§ Maio de mil novecentos e oitenta e cinco. O novo líder, Mikhail Gorbatchov, declara guerra à bebida. As lojas de vodca abrem mais tarde e vendem menos.", card="1985")
b("Mas o povo responde com o que tem em casa: destila a própria bebida. E para isso precisa de açúcar. Resultado: some o açúcar das lojas, e várias cidades passam a racioná-lo.")
b("Você já viu um governo perder dinheiro por vender menos vodca? Esse perdeu uns vinte bilhões de rublos em impostos.")
b("§ E o caixa, que já estava curto, leva mais dois golpes em mil novecentos e oitenta e seis: o preço do petróleo despenca, e explode um reator em Chernobyl.", card="1986")
b("Repare na volta que a história deu: o país que ia alcançar a América em manteiga agora não consegue pôr açúcar na loja. O problema é que, desta vez, todo mundo está vendo.")

# ───────────────────────── 9. DE VOLTA DE HOUSTON ─────────────────────────
cap("9. A volta de Houston")
b("§ Lembra do supermercado do Texas? Iéltsin volta para Moscou. Segundo um assessor, foi ali, entre as gôndolas, que desabou a última coisa que ele ainda acreditava no sistema.", card="1989")
b("E o que você encontraria em casa? Em Leningrado, chá e sabão passam a ser vendidos com talão. E aí entram na lista o açúcar, a vodca e o cigarro.")
b("§ Trinta e um de janeiro de mil novecentos e noventa. Na Praça Púchkin, em Moscou, abre a lanchonete americana do começo do vídeo. Cerca de trinta mil pessoas passam pelo balcão no primeiro dia.", card="1990")
b("Um sanduíche custa uns quatro rublos. Pense: mais de meio dia de salário. Mas mesmo assim a fila dá voltas na praça, no frio.")
b("§ Em dezembro de noventa, a Alemanha começa a mandar comida para Moscou. Parte vem da reserva de Berlim, um estoque criado por causa do bloqueio soviético de quarenta e oito.")
b("Lembra dos americanos com comida no Volga? Setenta anos depois, a comida de fora voltou. Só que agora vinha do estoque que existia por causa de Moscou.")
b("E um Estado que não consegue alimentar as próprias cidades fica sem resposta quando as repúblicas perguntam: por que ficar?")

# ───────────────────────── 10. O ÚLTIMO PLANO ─────────────────────────
cap("10. O último preço")
b("§ Dois de abril de mil novecentos e noventa e um. De um dia para o outro, o governo dobra os preços. Alguns triplicam. Imagine acordar e o seu pão custar o triplo.", card="1991")
b("Mesmo assim, as prateleiras continuam vazias. E a avoska, depois de sessenta anos no bolso, continua voltando para casa leve.")
b("§ Em agosto, uma tentativa de golpe fracassa em três dias. Em vinte e cinco de dezembro, a União Soviética deixa de existir.")
b("Aí, em janeiro de noventa e dois, a Rússia solta os preços. Em semanas, a prateleira enche. Cara, quase impossível de pagar. Mas enche.", card="1992")

# ───────────────────────── FECHO (≤ 45 s) ─────────────────────────
cap("Fecho")
b("§ Então, como o país que chegou primeiro ao espaço não conseguia encher uma prateleira? Porque a prateleira era sempre o próximo plano. E quando ela virava urgência, ou a pressa comia a semente, ou alguém de fora enchia.")
b("Talvez a pergunta certa nunca tenha sido por que faltava comida. Era quem decide o que vai na sua sacola. [break] Em dois mil e vinte e dois, a lanchonete da Praça Púchkin reabriu com outro nome.", card="2022")
b("[warm] Na sua casa, alguém tinha uma sacola do vai que? Conta nos comentários.")

# Grafia para a VOZ (o Fish lê como português). Conferir no teste de nomes (qa/pronuncia/).
# blocos.json leva "texto" (falado, vai ao Fish) e "tela" (grafia correta: legendas e SCRIPT).
FALA = [("Iéltsin", "Iéltsin"), ("Khruschov", "Khruchóv"), ("Kossyguin", "Kossíguin"), ("Gorbatchov", "Gorbatchóv"),
        ("Novocherkassk", "Novotcherkásk"), ("Riazan", "Riazã"), ("Larionov", "Larionóv"), ("Gosplan", "Gósplan"),
        ("avoska", "avóska"), ("avos", "ávos"), ("Púchkin", "Púchkin"), ("Herbert Hoover", "Hérbert Húver")]
def fala(t):
    for a, z in FALA: t = re.sub(r"(?<![\wÀ-ú])" + re.escape(a) + r"(?![\wÀ-ú])", z, t)
    return t

IDEIA = set()
THUMB = None   # thumbs nascem dos 3 conceitos aprovados no crivo (EMBALAGEM.md r3): arte na etapa 2 (skill thumbnail)

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
        blocos.append({"id": bid, "texto": fala(blk["t"]), "tela": blk["t"], "ideia": blk.get("ideia", False)})
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
                cenas.append({"id": ids[k], "prompt": prompts[k]})
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
        t += d

    total = t
    if THUMB: cenas.append(THUMB)
    reuso = [p for p in planos if not p["nova"]]
    apos = [p for p in planos if p["ini"] >= INEDITO_ATE]
    reuso_apos = [p for p in apos if not p["nova"]]
    words = sum(len(limpo(b_["tela"]).split()) for b_ in blocos)
    stats = {"palavras": words, "duracao_s": round(total), "planos": len(planos),
             "imagens_video": len(ids), "imagens_total": len(cenas),
             "reuso_pct": round(100 * len(reuso) / len(planos), 1),
             "reuso_pct_apos_3min": round(100 * len(reuso_apos) / max(1, len(apos)), 1),
             "plano_medio_s": round(total / len(planos), 2),
             "cortes_1o_min": sum(1 for p in planos if p["ini"] < 60), "rotulos": sum(1 for p in planos if p["rot"]),
             "capitulos": sum(1 for x in B if "cap" in x and x["cap"] not in ("Hook", "Fecho")), "avisos": avisos}

    (out / "blocos.json").write_text(json.dumps(blocos, ensure_ascii=False, indent=1) + "\n")
    (out / "cenas.json").write_text(json.dumps(cenas, ensure_ascii=False, indent=1) + "\n")
    (out / "storyboard.json").write_text(json.dumps({"stats": stats, "planos": planos}, ensure_ascii=False, indent=1) + "\n")
    (out / "SCRIPT.md").write_text(
        f"# {TITULO} em {round(total / 60)} minutos: roteiro\n\n"
        f"Pergunta central: {PERGUNTA}\n\nPromessa: {PROMESSA}\n\nTítulos: {TITULOS}\n\n"
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
