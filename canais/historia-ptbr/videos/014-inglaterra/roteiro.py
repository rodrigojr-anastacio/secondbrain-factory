#!/usr/bin/env python3
"""Fonte única do 014-inglaterra (20/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

11º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
4º com ÂNGULO próprio (ANGULO.md): "a coroa que vem de fora" — seis coroas para gente de fora; cada rei de fora paga com um pedaço de poder no papel;
o papel vira Parlamento, crédito, frota e império.
EMBALAGEM.md aprovada no crivo r3:
  A/T1 "A Inglaterra IMPORTAVA reis. Como mandou em 1/4 do mundo?" + thumb rosto-emocao (Jaime VI de manta xadrez se coroando, "MINHA!")
  B/T2 "Como reis de FORA deixaram a Inglaterra mais forte" + thumb cena-acao (coroação de Natal de 1066 com fogo lá fora, "NATAL DE 1066")
  C/T3 "Inglaterra, o país que dava a COROA a estrangeiros" + thumb documento-evidencia (Declaração de Direitos circulada, "O PREÇO")
Hook: Carey galopa 60 h (1603) → "o rei da Inglaterra agora é um escocês" (≤ 0:30) → PERGUNTA CENTRAL (≤ 0:50) → tomaram × receberam,
  Natal com fogo → o preço concreto (imposto só com licença) (≤ 1:00) → "essa é a história inteira… numa ilha que todo mundo atravessa".
Peças da resposta: 1 (cap. 3) rei que precisa de dinheiro precisa pedir, e quem é pedido aprende a cobrar; 2 (cap. 7) o papel que amarra
  o rei de fora deixa o país confiável para pedir emprestado; 3 (cap. 9) a coroa vem de fora, o poder fica dentro, no papel, e o papel paga a frota.
"Guarde" único: a promessa no estandarte de 1688 → paga no cap. 10 (juramento de Carlos III, 2023).
Neutralidade: execução de 1649, colonialismo e fome irlandesa com contexto, sem imagem gráfica. Mitos evitados: Jorge I "sem inglês",
  "saiu do gabinete pela língua", Walpole "primeiro-ministro" sem ressalva, ondas de Canuto (contada como lenda e no sentido original).

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1066") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006–013).
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
TITULO = "A história INTEIRA da Inglaterra"
PERGUNTA = "Como um país que vivia buscando rei lá fora acabou mandando em um quarto do mundo?"
PROMESSA = ("Como a Inglaterra entregou a coroa a gente de fora seis vezes, e como o preço cobrado de cada rei estrangeiro virou a força "
            "que mandou em um quarto do mundo (EMBALAGEM.md r3).")
TITULOS = ('T1 "A Inglaterra IMPORTAVA reis. Como mandou em 1/4 do mundo?" / T2 "Como reis de FORA deixaram a Inglaterra mais forte" / '
           'T3 "Inglaterra, o país que dava a COROA a estrangeiros"')

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None):
    ideia = t.startswith("§")
    n = sum(1 for x in B if "t" in x) + 1
    if not s: s = tuple(P.get(n, ()))
    if not s and PENDENTE: s = (f"tmp{n:03d}|placeholder",)
    assert s, f"N{n:03d} sem planos"
    B.append({"t": t.lstrip("§ ").strip(), "s": list(s), "card": card, "ideia": ideia})

PENDENTE = False   # storyboard escrito (P abaixo)

# ───────── regras de prompt (Codex; fallback nano-banana) ─────────
# As refs de estilo vêm do Egito e vazam conteúdo (visual.md 010/011/013): TODA cena leva o cenário ancorado (ING/ESC/FRA/EUA/MUNDO)
# + SEMTXT; cenas com gente, navio ou praça levam SEMBAND. Mapas: MAPA (sem letras; rótulos no código).
MAPA = ("painted like a blank parchment terrain map seen from directly above, only coastlines, seas, rivers, mountains and flat colored areas, "
        "completely blank with no writing anywhere, no letters, no words, no labels, no symbols, no compass, no border, no frame, no flags, no people")
SEMTXT = ", no readable writing, no letters anywhere, no numbers, no signs, no boards, no logos"
SEMBAND = ", no flags, no banners, no coats of arms, no emblems"
GUERRA = ", no blood, no wounds, no bodies, no weapons fired, no violence shown"
NAO_EG = ", NO pyramids, NO palm trees, NO pharaoh headdress, NO turbans, NO desert dunes, NO camels"
ING = ", strictly England: green fields, oak trees, grey stone and timber houses, cloudy sky" + NAO_EG
ESC = ", strictly Scotland: grey stone, heather hills, cold misty light" + NAO_EG
FRA = ", strictly northern France: green fields, stone castles, slate roofs" + NAO_EG
MOD = ", ordinary modern everyday setting of today" + NAO_EG + ", NO crowns, NO safari helmet"
LON = ", strictly London of the time, grey stone and brick buildings by the river Thames" + NAO_EG
def ANO(a): return f", period-accurate {a}: clothes, buildings and objects of that time only, no modern objects"
PAPEL = ", the document is drawn as plain wavy lines, completely illegible, no letters, no words"
COROA = "a gold English crown with arches, a small cross on top and a white ermine band"
# Personagens (bíblia: rosto nunca descrito; "round-white-head cartoon …"; nomes reais só no rótulo do código)
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes, wearing an ordinary brown felt hat and a plain brown jacket"
CAREY = "a round-white-head cartoon Elizabethan English nobleman with a short flat brown beard shape, a white ruff collar, a dark riding cloak and tall boots"
ELIZ = "a round-white-head cartoon elderly Queen Elizabeth I with a red curly wig shape, a big white ruff and a pearl-covered dress"
JAMES = "a round-white-head cartoon King James VI of Scotland with a short flat reddish beard shape, a dark doublet and a tall black hat"
CNUT = "a round-white-head cartoon Viking-age king with a simple flat blond beard shape, a plain gold circlet and a red cloak"
WILL1 = "a round-white-head cartoon Norman duke with short dark hair, a red cloak over chain mail"
JOHN = "a round-white-head cartoon medieval King John with a short flat dark beard shape and a simple gold crown"
HENRY2 = "a round-white-head cartoon 12th-century king with a short flat reddish beard shape, a simple gold crown and a green travelling cloak"
MONT = "a round-white-head cartoon 13th-century nobleman with short dark hair, chain mail and a plain white surcoat"
HENRY4 = "a round-white-head cartoon 14th-century king with a short flat forked brown beard shape, a gold crown and a long blue robe"
TUDOR = "a round-white-head cartoon 15th-century nobleman with shoulder-length dark hair, a black cap and a plain breastplate"
HENRY8 = "a round-white-head cartoon stout King Henry VIII with a short flat reddish beard shape, a wide flat black cap with a feather and a broad padded gold coat"
CHARLES1 = "a round-white-head cartoon King Charles I with long dark hair, a small pointed beard shape and a wide white lace collar"
HAMPDEN = "a round-white-head cartoon 17th-century English country gentleman with shoulder-length brown hair, a plain dark coat and a white collar"
WILL3 = "a round-white-head cartoon slim Dutch prince of 1688 with a long dark curly wig, a dark blue coat and an orange sash"
MARY2 = "a round-white-head cartoon young queen of 1689 with dark curled hair and a blue silk dress"
GEORGE1 = "a round-white-head cartoon King George I of 1714, middle-aged, with a white powdered wig and a plain blue coat"
WALPOLE = "a round-white-head cartoon stout 18th-century statesman with a white wig, a red coat and a silver star on the chest"
NAPO = "a round-white-head cartoon Napoleon with a black bicorne hat, a grey coat and a hand tucked in his waistcoat"
VICT = "a round-white-head cartoon young Queen Victoria with dark hair in a bun and a small crown"
ALBERT = "a round-white-head cartoon Prince Albert with dark side whiskers and a dark uniform"
GEORGE5 = "a round-white-head cartoon King George V with a short flat neat beard shape, in a dark naval uniform"
NEGOC = "a round-white-head cartoon very tall thin British economist of 1945 with a small mustache shape, a dark suit and a bowler hat"
REI23 = "a round-white-head cartoon elderly king of 2023 with thin white hair, in a gold coronation robe"
PARL = "round-white-head cartoon English members of parliament on wooden benches"

P = {}
# HOOK
P[1] = ["richmond_night|Richmond Palace by the Thames at night in March 1603, Tudor towers with many chimneys, a few lit windows, cold mist" + ING + ANO("1603") + SEMTXT + SEMBAND + "@@RICHMOND, 1603",
        f"queen_bed|A dim royal bedchamber of 1603 with a big four-poster bed and candles, courtiers with bowed heads standing quietly around it, the bed curtains half closed" + ING + ANO("1603") + SEMTXT + SEMBAND,
        f"carey_viewer|{CAREY} looking straight at the viewer in a candle-lit palace corridor, serious, holding his riding gloves" + ING + ANO("1603") + SEMTXT + SEMBAND + "@@ROBERT CAREY",
        "empty_throne_1603|An empty carved wooden throne in a Tudor hall, a small crown on a red cushion beside it, morning light" + ING + ANO("1603") + SEMTXT + SEMBAND,
        "stable_dawn|A stable yard at dawn, a groom holding a saddled horse ready, breath steaming in the cold" + ING + ANO("1603") + SEMTXT + SEMBAND]
P[2] = [f"carey_gallop|{CAREY} galloping hard on a brown horse along a muddy road at night under the moon, cloak flying" + ING + ANO("1603") + SEMTXT + SEMBAND,
        "map_london_edinburgh|Map of Great Britain with a thin dotted line running from London in the south to Edinburgh in the north, " + MAPA,
        f"carey_change_horse|{CAREY} jumping from a tired horse to a fresh one at a roadside inn, exhausted, mud on his boots" + ING + ANO("1603") + SEMTXT + SEMBAND,
        f"holyrood_arrival|{CAREY} covered in mud, kneeling before {JAMES} in a stone palace hall at night, candles" + ESC + ANO("1603") + SEMTXT + SEMBAND + "@@EDIMBURGO",
        "border_battle_ghost|Symbolic scene: on a hill on the border, two groups of round-white-head cartoon soldiers of the 1500s, English and Scottish, glaring at each other across a stream, spears held upright, no fighting" + ESC + ANO("1513") + SEMTXT + SEMBAND + GUERRA]
P[3] = [f"guide_question|{GUIA} standing on the white cliffs of the English coast looking at the sea with a puzzled hand on his chin" + ING + SEMTXT + SEMBAND,
        "map_empire_1920|Map of the whole world with about a quarter of the land shaded in a flat pink color across Canada, Africa, India and Australia, the rest pale, " + MAPA,
        "crown_from_sea|Symbolic scene: " + COROA + " floating over a grey sea toward a small green island, seen from above the waves, nobody in the picture" + ING + SEMTXT + SEMBAND,
        "tiny_island_globe|A small old globe on a wooden table with a tiny island lit by a ray of light, the rest of the globe in shadow, nobody in the picture" + ING + SEMTXT]
P[4] = [f"cnut_landing|Viking longships landing on a grey English beach, {CNUT} stepping onto the sand" + ING + ANO("1016") + SEMTXT + SEMBAND + GUERRA,
        f"william_landing|Norman ships with square sails landing horses on an English beach, {WILL1} on the shore" + ING + ANO("1066") + SEMTXT + SEMBAND + GUERRA,
        "coronation_fire_glimpse|Night view of an old Romanesque stone church with several wooden houses next to it on fire, orange glow, people running away safely" + LON + ANO("1066") + SEMTXT + SEMBAND + GUERRA,
        f"henry2_arrives|{HENRY2} arriving on horseback through a castle gate, welcomed by bowing English barons" + ING + ANO("1154") + SEMTXT + SEMBAND,
        f"william3_ship|{WILL3} standing on the deck of a big sailing ship of 1688 with plain orange pennants, the English coast ahead" + ING + ANO("1688") + SEMTXT + SEMBAND,
        f"george1_coach|{GEORGE1} stepping out of a gilded coach in front of an English palace, courtiers bowing" + LON + ANO("1714") + SEMTXT + SEMBAND]
P[5] = ["coins_on_table|A pile of gold and silver coins on a wooden table, a royal hand hovering over them but stopped by a parchment held up by other hands" + ING + ANO("1689") + PAPEL + SEMTXT + SEMBAND,
        f"william3_reads|{WILL3} reading a long parchment with a worried frown while men in wigs watch him" + LON + ANO("1689") + PAPEL + SEMTXT + SEMBAND,
        "quill_sign|Close view of a royal hand holding a quill over a long parchment, a red wax seal beside it" + ING + PAPEL + SEMTXT + SEMBAND,
        "tax_chest_locked|A heavy wooden tax chest with a big padlock and a parchment tied to it with a red ribbon, nobody in the picture" + ING + PAPEL + SEMTXT]
P[6] = ["map_britain_blank|Map of Great Britain and Ireland with the sea around, France and the Low Countries at the edge, " + MAPA,
        "island_ships_arriving|Bird's-eye view of a green island coast with small boats of many shapes arriving from every direction, nobody visible" + ING + SEMTXT + SEMBAND,
        f"guide_island|{GUIA} sitting on a rock on a green English cliff, waving at the viewer, sea behind" + ING + SEMTXT + SEMBAND]
# 1. A ILHA QUE TODO MUNDO ATRAVESSA
P[7] = [f"cnut_throne|{CNUT} sitting on a wooden throne in a timber Anglo-Saxon hall with a fire in the middle, warriors and English nobles around" + ING + ANO("1016") + SEMTXT + SEMBAND + "@@CANUTO",
        "map_north_sea_empire|Map of the North Sea with England, Denmark and Norway shaded in the same flat red color, the rest pale, " + MAPA,
        "longships_north_sea|Three Viking longships with striped sails crossing a grey North Sea under heavy clouds" + ANO("1016") + SEMTXT + SEMBAND + NAO_EG,
        f"cnut_crown_close|Close view of {CNUT} touching the gold circlet on his head, satisfied" + ING + ANO("1016") + SEMTXT + SEMBAND,
        "anglo_saxon_village|An Anglo-Saxon village of wooden houses with thatched roofs and a timber church, sheep and fields" + ING + ANO("1016") + SEMTXT + SEMBAND]
P[8] = ["roman_soldiers_beach|Round-white-head cartoon Roman legionaries with plain shields, no letters on the shields, wading ashore on a green English coast with white cliffs" + ING + ANO("43 AD") + SEMTXT + SEMBAND,
        "saxon_boats|Round-white-head cartoon Anglo-Saxon settlers in simple tunics arriving in long rowing boats on a muddy English river bank with their cows" + ING + ANO("450") + SEMTXT + SEMBAND,
        "viking_raid_coast|Viking longships approaching a quiet English coastal monastery at dawn, monks looking up from the field" + ING + ANO("800") + SEMTXT + SEMBAND + GUERRA,
        "alfred_king|A round-white-head cartoon Anglo-Saxon king with a short flat beard shape and a simple gold band, standing on a wooden palisade looking out over a marsh" + ING + ANO("878") + SEMTXT + SEMBAND + "@@ALFREDO, O GRANDE",
        "map_arrows_island|Map of Great Britain with five arrows of different colors coming from the sea and the continent toward the island, " + MAPA,
        "beach_many_footprints|A wet English beach covered in footprints of many different shoes and boots going inland, nobody in the picture" + ING + SEMTXT]
P[9] = [f"guide_class|{GUIA} in a modern classroom pointing at three simple drawings on a blank board: the sky with a cloud, an egg and a knife, no letters" + SEMTXT + SEMBAND + MOD,
        "viking_words|Symbolic scene: a Viking warrior handing an egg and a knife to a smiling English farmer, a big sky with clouds above them" + ING + ANO("900") + SEMTXT + SEMBAND,
        "rune_stone_field|A tall old carved stone in an English field with simple decorative swirls and no letters, morning mist" + ING + SEMTXT]
P[10] = [f"cnut_beach_throne|{CNUT} seated on a wooden throne placed on a wet beach at the water's edge, courtiers in fine clothes around him" + ING + ANO("1020") + SEMTXT + SEMBAND,
         f"courtiers_flatter|Round-white-head cartoon courtiers of 1020 bowing and smiling to {CNUT}, one of them pointing proudly at the sea" + ING + ANO("1020") + SEMTXT + SEMBAND,
         f"cnut_wet_feet|{CNUT} with the waves washing over his feet and his robe, looking calmly back at his surprised courtiers, raising one finger as if teaching" + ING + ANO("1020") + SEMTXT + SEMBAND,
         f"cnut_arrogant_myth|Comic symbolic scene: {CNUT} on a beach shouting at a huge wave with an angry face, drawn inside a thought bubble" + ING + SEMTXT + SEMBAND,
         "medieval_chronicler|A round-white-head cartoon medieval monk writing a chronicle by candlelight in a stone room, the page with plain wavy lines" + ING + ANO("1130") + PAPEL + SEMTXT + SEMBAND,
         "waves_on_throne|Close view of waves running around the wooden legs of an empty throne on the sand" + ING + SEMTXT,
         "courtiers_shocked|Round-white-head cartoon courtiers of 1020 with open mouths, holding up their wet robes on a beach" + ING + ANO("1020") + SEMTXT + SEMBAND,
         f"cnut_crown_off|{CNUT} taking off his gold circlet and holding it low, humble, on the beach" + ING + ANO("1020") + SEMTXT + SEMBAND]
P[11] = [f"cnut_smaller|{CNUT} kneeling humbly before a small stone altar in an English church, his crown placed on the altar" + ING + ANO("1030") + SEMTXT + SEMBAND,
         "english_nobles_nod|Round-white-head cartoon Anglo-Saxon nobles nodding in approval at the back of a church" + ING + ANO("1030") + SEMTXT + SEMBAND]
P[12] = ["cnut_tomb|A simple stone tomb in a quiet English cathedral with a small gold circlet carved on top, candles" + ING + ANO("1035") + SEMTXT + SEMBAND,
         "sons_quarrel|Two round-white-head cartoon young Viking-age princes pulling a red cloak from opposite sides, comic quarrel" + ING + ANO("1036") + SEMTXT + SEMBAND,
         "edward_crowned|A round-white-head cartoon pious English king with a long flat white beard shape and a gold crown, praying in a church" + ING + ANO("1042") + SEMTXT + SEMBAND,
         f"william_across_channel|{WILL1} standing on a French cliff looking across the sea toward England with his arms crossed" + FRA + ANO("1060") + SEMTXT + SEMBAND,
         "map_channel|Map of the English Channel with southern England and Normandy facing each other across the water, " + MAPA + "@@NORMANDIA"]
# 2. GRITOS EM DUAS LÍNGUAS
P[13] = ["westminster_1066_ext|The old Romanesque Westminster Abbey of 1066 by the Thames in winter, round arches, a low square tower, snow on the roofs, no Gothic spires" + LON + ANO("1066") + SEMTXT + SEMBAND + "@@WESTMINSTER, 1066",
         "hastings_aftermath_symbol|Symbolic scene: a dented Norman helmet and a broken Saxon shield lying on a grassy hill at sunset, nobody in the picture" + ING + ANO("1066") + SEMTXT + SEMBAND + GUERRA,
         f"william_robing|{WILL1} being dressed in a red coronation robe by two monks inside a stone church, nervous" + LON + ANO("1066") + SEMTXT + SEMBAND + "@@GUILHERME DA NORMANDIA",
         "abbey_interior_crowd|Inside a Romanesque church of 1066 with round arches and thick columns, crowded with English and Norman nobles holding candles" + LON + ANO("1066") + SEMTXT + SEMBAND]
P[14] = ["bishop_french|A round-white-head cartoon Norman bishop with a mitre raising his hands and calling out to the crowd inside a Romanesque church" + LON + ANO("1066") + SEMTXT + SEMBAND,
         "archbishop_english|A round-white-head cartoon old English archbishop with a white beard shape and a mitre repeating the question to the crowd" + LON + ANO("1066") + SEMTXT + SEMBAND,
         "crowd_shouting_yes|A crowd of round-white-head cartoon nobles inside a church raising their arms and shouting with joy" + LON + ANO("1066") + SEMTXT + SEMBAND,
         "crown_descends|Close view of a bishop's hands lowering " + COROA + " onto the head of a seated man in a red cloak, candlelight" + LON + ANO("1066") + SEMTXT + SEMBAND]
P[15] = ["norman_guards_outside|Round-white-head cartoon Norman soldiers with conical helmets and kite shields standing outside a church door in the snow, hearing loud shouts, alarmed" + LON + ANO("1066") + SEMTXT + SEMBAND,
         "houses_fire|Wooden houses next to an old stone church catching fire at dusk, orange flames and smoke, people running away safely" + LON + ANO("1066") + SEMTXT + SEMBAND + GUERRA,
         "church_empties|People rushing out of a church door into the snowy street, smoke in the sky, the inside nearly empty" + LON + ANO("1066") + SEMTXT + SEMBAND + GUERRA,
         f"william_trembling|{WILL1} sitting alone on a throne in a nearly empty church, crown on his head, trembling, orange light coming through the door" + LON + ANO("1066") + SEMTXT + SEMBAND,
         "chronicler_orderic|A round-white-head cartoon medieval monk writing at a desk in a Norman abbey, looking up as if remembering, page with plain wavy lines" + FRA + ANO("1120") + PAPEL + SEMTXT + SEMBAND]
P[16] = [f"guide_applause|{GUIA} in a modern theatre clapping happily at a speaker talking in a foreign language, confused smile" + SEMTXT + SEMBAND + MOD,
         "guards_misunderstand|Comic scene: a round-white-head cartoon Norman guard with a cupped hand at his ear outside a church door, frowning, sound lines coming from the door" + LON + ANO("1066") + SEMTXT + SEMBAND]
P[17] = ["motte_castle|A Norman wooden castle on a high earth mound with a stockade, and a stone keep being built nearby, English workers carrying stones" + ING + ANO("1070") + SEMTXT + SEMBAND,
         "norman_lords_land|Round-white-head cartoon Norman knights receiving rolled land charters from the king in a hall" + ING + ANO("1070") + PAPEL + SEMTXT + SEMBAND,
         "domesday_counting|Round-white-head cartoon royal clerks in an English village counting pigs, cows and ploughs, writing on parchment, peasants watching" + ING + ANO("1086") + PAPEL + SEMTXT + SEMBAND,
         "domesday_book|A huge old leather-bound book open on a wooden table, the pages with plain wavy lines, nobody in the picture" + ING + PAPEL + SEMTXT,
         "fiscal_chickens|Comic scene: a round-white-head cartoon medieval clerk kneeling in a farmyard counting chickens one by one with a quill, a peasant woman with hands on hips" + ING + ANO("1086") + PAPEL + SEMTXT + SEMBAND]
P[18] = ["norman_court_french|A Norman royal court in a stone hall: nobles talking at a long table, an English servant carrying a tray looking lost" + ING + ANO("1100") + SEMTXT + SEMBAND,
         "money_crossing_channel|Symbolic scene: a small ship crossing the Channel from England to France loaded with chests of coins, nobody visible" + SEMTXT + SEMBAND + NAO_EG,
         "map_angevin|Map of England and the western half of France shaded in the same flat red color, the rest of France pale, " + MAPA]
# 3. O REI PRESO NA ILHA
P[19] = ["rouen_1204|The walled medieval city of Rouen on the river Seine in June 1204 with a big Romanesque cathedral and stone walls, French soldiers at the open gates" + FRA + ANO("1204") + SEMTXT + SEMBAND,
         "keys_handed|Round-white-head cartoon town leaders of Rouen handing a big iron key to a French knight at the gate" + FRA + ANO("1204") + SEMTXT + SEMBAND,
         f"john_bad_news|{JOHN} receiving a letter from a messenger in an English castle and throwing up his hands in despair" + ING + ANO("1204") + PAPEL + SEMTXT + SEMBAND + "@@JOÃO"]
P[20] = [f"henry2_portrait|{HENRY2} riding through a French town with a big retinue, people bowing" + FRA + ANO("1160") + SEMTXT + SEMBAND + "@@HENRIQUE II",
         "le_mans_cathedral|The medieval town of Le Mans with its Romanesque cathedral on a hill, timber houses" + FRA + ANO("1133") + SEMTXT + SEMBAND + "@@LE MANS",
         "map_angevin#médio-esq"]
P[21] = [f"john_island|{JOHN} standing alone on the white cliffs of Dover looking toward France across the sea, sulking" + ING + ANO("1205") + SEMTXT + SEMBAND,
         "tax_collectors|Round-white-head cartoon royal tax collectors loading sacks of coins onto a cart in front of worried barons and farmers" + ING + ANO("1210") + SEMTXT + SEMBAND,
         "empty_chest_john|An open royal treasure chest, empty except for one coin, in a dim castle room" + ING + SEMTXT]
P[22] = ["barons_angry|Round-white-head cartoon English barons in chain mail arguing loudly around a table in a castle hall" + ING + ANO("1215") + SEMTXT + SEMBAND,
         f"runnymede_tent|{JOHN} sitting unhappily under a tent in a green meadow by the river, barons standing around him holding a long parchment" + ING + ANO("1215") + PAPEL + SEMTXT + SEMBAND,
         "seal_wax|Close view of a big royal wax seal being pressed onto a parchment" + ING + PAPEL + SEMTXT + SEMBAND,
         "pope_annuls|A round-white-head cartoon medieval pope in white tearing a parchment in half in a Roman-style palace room" + ANO("1215") + PAPEL + SEMTXT + SEMBAND + ", NO pyramids, NO palm trees"]
P[23] = [f"montfort_portrait|{MONT} on horseback in front of an English army camp, determined" + ING + ANO("1264") + SEMTXT + SEMBAND + "@@SIMON DE MONTFORT",
         "parliament_1265|Inside a medieval hall at Westminster: barons in fine robes and, for the first time, plainly dressed townsmen and knights sitting on benches together" + LON + ANO("1265") + SEMTXT + SEMBAND,
         "townsmen_arrive|Round-white-head cartoon medieval townsmen in simple tunics and hats walking into a stone hall, a little shy" + LON + ANO("1265") + SEMTXT + SEMBAND]
P[24] = [f"guide_piece1|{GUIA} holding up the first piece of a big jigsaw puzzle shaped like a crown, smiling" + SEMTXT + SEMBAND + MOD,
         "king_asks_money|Comic scene: a round-white-head cartoon medieval king holding out an empty purse to a group of townsmen, who hold out a parchment in return" + ING + ANO("1265") + PAPEL + SEMTXT + SEMBAND,
         f"guide_favor|{GUIA} in a modern kitchen holding a cake while a neighbor asks him for a favor, both smiling, ordinary modern clothes" + SEMTXT + SEMBAND + MOD]
P[25] = ["french_speaking_parliament|Medieval nobles in a stone hall arguing, speech bubbles with simple pictures of a French castle, no letters" + LON + ANO("1300") + SEMTXT + SEMBAND]
# 4. A LÍNGUA VOLTA
P[26] = ["parliament_1362|A medieval English parliament in a stone hall at Westminster with a king on a raised seat and lords and commoners on benches" + LON + ANO("1362") + SEMTXT + SEMBAND,
         "court_english|A medieval English courtroom: a judge in red robes listening to a peasant speaking, the peasant relieved" + ING + ANO("1362") + SEMTXT + SEMBAND,
         "statute_french|Close view of a medieval scribe writing a long parchment with a smug little smile, plain wavy lines" + ING + ANO("1362") + PAPEL + SEMTXT + SEMBAND]
P[27] = ["peasant_confused_court|A round-white-head cartoon medieval English peasant in a courtroom scratching his head while lawyers in robes talk over him" + ING + ANO("1350") + SEMTXT + SEMBAND,
         "hundred_years_war|Symbolic scene: English longbowmen and French knights facing each other across a muddy field, no fighting" + FRA + ANO("1346") + SEMTXT + SEMBAND + GUERRA,
         "map_france_war|Map of France with English-held areas in flat red shrinking toward the coast, " + MAPA]
P[28] = [f"henry4_claims|{HENRY4} standing in front of parliament in Westminster Hall, speaking with his hand on his chest" + LON + ANO("1399") + SEMTXT + SEMBAND + "@@HENRIQUE IV",
         "calais_walls|The walled port of Calais with English ships in the harbour, the rest of the French coast behind in shadow" + FRA + ANO("1453") + SEMTXT + SEMBAND,
         "soldiers_return|Tired round-white-head cartoon English soldiers of 1453 boarding ships to go home, carts with empty barrels" + FRA + ANO("1453") + SEMTXT + SEMBAND + GUERRA]
P[29] = ["roses_conflict|Symbolic scene: a red rose and a white rose on thorny stems crossed like swords over a green English hill" + ING + SEMTXT + SEMBAND,
         "two_families_table|Two groups of round-white-head cartoon 15th-century nobles, one with red roses and one with white roses pinned to their coats, glaring at each other across a table" + ING + ANO("1460") + SEMTXT + SEMBAND]
P[30] = [f"tudor_exile|{TUDOR} looking out of a castle window in Brittany at the sea, waiting" + FRA + ANO("1480") + SEMTXT + SEMBAND + "@@HENRIQUE TUDOR",
         "milford_landing|Ships landing soldiers on a rocky Welsh shore at sunset, mercenaries with pikes stepping onto the beach" + ANO("1485") + SEMTXT + SEMBAND + GUERRA + ", strictly Wales: green rocky coast" + NAO_EG,
         "crown_in_bush|Symbolic scene: " + COROA + " caught in a hawthorn bush on a battlefield at sunset, nobody in the picture" + ING + SEMTXT + SEMBAND]
P[31] = [f"tudor_desk|{TUDOR}, now king with a crown, counting coins at a desk with a ledger, suspicious" + ING + ANO("1495") + PAPEL + SEMTXT + SEMBAND]
# 5. O REI FORTE QUE PRECISOU DO PAPEL
P[32] = [f"henry8_angry|{HENRY8} in a rich palace room crumpling a letter with a red papal seal, furious" + LON + ANO("1529") + PAPEL + SEMTXT + SEMBAND + "@@HENRIQUE VIII",
         "papal_letter|Close view of a parchment with a red seal and a ribbon lying on a marble floor" + PAPEL + SEMTXT + SEMBAND + NAO_EG,
         f"henry8_waiting|{HENRY8} tapping his foot impatiently on his throne, looking at a big hourglass" + LON + ANO("1529") + SEMTXT + SEMBAND]
P[33] = [f"henry8_parliament|{HENRY8} entering a hall full of {PARL}, raising one hand" + LON + ANO("1529") + SEMTXT + SEMBAND,
         "rome_chain_broken|Symbolic scene: a heavy iron chain between a small English church and a distant hill city breaks in the middle, nobody in the picture" + ING + SEMTXT + SEMBAND]
P[34] = ["parliament_shadow|Symbolic scene: in a Tudor hall, the shadow of the parliament benches on the wall grows bigger than the throne" + LON + ANO("1534") + SEMTXT + SEMBAND,
         "monastery_empty|An empty stone abbey with no roof in a green English valley, sheep grazing in the nave" + ING + ANO("1540") + SEMTXT + SEMBAND,
         "gentry_buy_land|Round-white-head cartoon Tudor gentlemen in black coats paying gold coins to a royal clerk for a land deed in front of an abbey" + ING + ANO("1540") + PAPEL + SEMTXT + SEMBAND]
P[35] = [f"guide_keys|{GUIA} handing a ring of house keys to a smiling neighbor at the door of a modern house, potted plants beside" + SEMTXT + SEMBAND + MOD,
         f"guide_keys_gone|{GUIA} knocking on a neighbor's door with an awkward smile, the neighbor now relaxed on a sofa inside, modern house" + SEMTXT + SEMBAND + MOD]
P[36] = [f"elizabeth_throne|{ELIZ} on a throne in a rich Tudor hall, holding a scepter, proud" + LON + ANO("1588") + SEMTXT + SEMBAND + "@@ELIZABETH I",
         "armada_storm|Spanish galleons of 1588 scattered by a storm in a grey sea, small English ships in the distance" + ANO("1588") + SEMTXT + SEMBAND + GUERRA + NAO_EG,
         "carey_gallop#médio-dir"]
P[37] = [f"james_divine|{JAMES} pointing up at the sky with a halo of light around him, confident, in a Scottish palace" + ESC + ANO("1603") + SEMTXT + SEMBAND]
# 6. O NOME RECUSADO
P[38] = [f"james_commons|{JAMES}, now with " + COROA + ", standing before the House of Commons in a dark wooden chamber, arms open, asking" + LON + ANO("1604") + SEMTXT + SEMBAND,
         "commons_no|Round-white-head cartoon members of the House of Commons of 1604 on green benches shaking their heads, some with crossed arms" + LON + ANO("1604") + SEMTXT + SEMBAND,
         "map_great_britain_one|Map of Great Britain with England and Scotland shaded in two different flat colors and a dotted line between them, " + MAPA]
P[39] = ["holyrood_arrival#médio-esq",
         "secret_letters|A secret letter being hidden inside a hollow book by a candle, nobody visible" + ESC + ANO("1601") + PAPEL + SEMTXT + SEMBAND,
         f"james_surprised|{JAMES} sitting on a throne with an offended open mouth, a parchment in his lap" + LON + ANO("1604") + PAPEL + SEMTXT + SEMBAND]
P[40] = ["buckinghamshire_manor|An English country manor house of brick in Buckinghamshire with green hills and sheep" + ING + ANO("1637") + SEMTXT + SEMBAND,
         f"hampden_refuses|{HAMPDEN} at his door politely refusing to hand coins to a royal tax collector holding a ledger" + ING + ANO("1637") + PAPEL + SEMTXT + SEMBAND + "@@JOHN HAMPDEN",
         "ship_money_ship|A big English warship of the 1630s in a harbour, paid for by the new tax, sailors on deck" + ING + ANO("1637") + SEMTXT + SEMBAND,
         "court_seven_five|Twelve round-white-head cartoon judges in red robes and wigs sitting in two groups, seven on the left and five on the right, in a court hall" + LON + ANO("1638") + SEMTXT + SEMBAND]
P[41] = [f"charles1_alone|{CHARLES1} sitting alone in a huge empty parliament chamber with dust on the benches" + LON + ANO("1635") + SEMTXT + SEMBAND + "@@CARLOS I",
         f"guide_condo|{GUIA} at a modern apartment building lobby reading a notice on the wall about a new fee, frowning, the notice blank" + SEMTXT + SEMBAND + MOD,
         "scots_army|Round-white-head cartoon Scottish soldiers of 1640 marching over a heather hill with pikes" + ESC + ANO("1640") + SEMTXT + SEMBAND + GUERRA]
P[42] = ["civil_war_field|Symbolic scene: two armies of the English Civil War facing each other across a green field, one in plain armour and one with feathered hats, no fighting" + ING + ANO("1642") + SEMTXT + SEMBAND + GUERRA,
         "banqueting_house|The Banqueting House in Whitehall on a cold January morning of 1649, a crowd waiting silently in front, a black-draped wooden platform without people" + LON + ANO("1649") + SEMTXT + SEMBAND + GUERRA]
P[43] = [f"guide_piece_question|{GUIA} holding a jigsaw puzzle piece and looking at an empty throne with a puzzled face" + LON + SEMTXT + SEMBAND,
         "restoration_parade|A joyful parade in London in 1660 welcoming a king in a carriage, people waving hats" + LON + ANO("1660") + SEMTXT + SEMBAND,
         "catholic_king|A round-white-head cartoon King James II with a long dark wig praying with a rosary in a chapel, Protestant bishops watching worried" + LON + ANO("1687") + SEMTXT + SEMBAND]
# 7. A INVASÃO POR CONVITE
P[44] = ["brixham_landing|A Dutch fleet of 1688 anchored in a Devon bay with green hills, soldiers in boats rowing ashore, plain orange pennants" + ING + ANO("1688") + SEMTXT + SEMBAND,
         "standard_orange|A big plain orange standard with a simple white border carried by a round-white-head cartoon Dutch soldier on a beach, no letters on the flag" + ING + ANO("1688") + SEMTXT,
         "standard_promise|Close view of an old silk banner waving in the wind, embroidered only with a simple decorative border and blank space, no letters" + ING + SEMTXT]
P[45] = [f"william3_beach|{WILL3} stepping onto an English beach from a rowing boat, raising his hat" + ING + ANO("1688") + SEMTXT + SEMBAND + "@@GUILHERME DE ORANGE",
         "invitation_letter_seven|A secret letter being sealed with seven different wax seals on a table by candlelight" + ING + ANO("1688") + PAPEL + SEMTXT + SEMBAND,
         "james2_flees|A round-white-head cartoon king with a long dark wig hurrying onto a small boat at night on the Thames, holding his crown under his arm" + LON + ANO("1688") + SEMTXT + SEMBAND]
P[46] = ["banqueting_reading|Inside a grand Whitehall hall in 1689, a clerk reading a long parchment aloud before a prince and princess standing under a canopy, lords listening" + LON + ANO("1689") + PAPEL + SEMTXT + SEMBAND,
         "declaration_clause|Close view of a long parchment with one line underlined in red, plain wavy lines" + PAPEL + SEMTXT + SEMBAND + ING]
P[47] = [f"william3_map_france|{WILL3} pointing at a map of France on a table with generals around him" + LON + ANO("1694") + SEMTXT + SEMBAND,
         "merchants_meeting|Round-white-head cartoon London merchants of 1694 in wigs signing a subscription book in a hall, coins on the table" + LON + ANO("1694") + PAPEL + SEMTXT + SEMBAND + "@@BANCO DA INGLATERRA"]
P[48] = ["king_runs_debt|Comic scene: a round-white-head cartoon king running away with a bag of money while merchants chase him with bills" + ING + ANO("1650") + PAPEL + SEMTXT + SEMBAND,
         "parliament_pays|Members of parliament of 1700 handing back coins with interest to merchants across a table, everyone calm" + LON + ANO("1700") + SEMTXT + SEMBAND,
         f"guide_bank|{GUIA} at a modern bank counter smiling as a clerk hands him a small paper with a down arrow drawing, no letters" + SEMTXT + SEMBAND + MOD]
P[49] = [f"guide_piece2|{GUIA} fitting a second jigsaw piece into the first one, both pieces showing a crown and a parchment" + SEMTXT + SEMBAND + MOD,
         "queen_anne_grief|A round-white-head cartoon queen of 1714 in a dark dress sitting sadly by a window, an empty cradle beside her" + LON + ANO("1714") + SEMTXT + SEMBAND,
         "map_hanover|Map of north-western Europe with Britain on the left and a small area of northern Germany highlighted across the sea, " + MAPA + "@@HANÔVER"]
# 8. O REI QUE PRECISA DE LICENÇA
P[50] = ["act_settlement_writing|Members of parliament of 1701 writing a long list on a parchment at a big table, one of them counting on his fingers" + LON + ANO("1701") + PAPEL + SEMTXT + SEMBAND,
         "no_leave_island|Symbolic scene: a gold crown on a small island with a closed gate at the pier, nobody in the picture" + ING + SEMTXT + SEMBAND]
P[51] = [f"guide_boss_list|{GUIA} in a modern office handing a very long paper list to a new boss with a briefcase, the paper blank" + SEMTXT + SEMBAND + MOD,
         f"george1_arrives|{GEORGE1} stepping off a boat at Greenwich with German attendants, English lords bowing" + LON + ANO("1714") + SEMTXT + SEMBAND + "@@JORGE I",
         f"george1_hanover|{GEORGE1} in a travelling coach looking happily at a German town with half-timbered houses" + ANO("1716") + SEMTXT + SEMBAND + ", strictly northern Germany" + NAO_EG]
P[52] = ["cabinet_empty_chair|Ministers of 1720 around a table with an empty royal chair at the head" + LON + ANO("1720") + SEMTXT + SEMBAND,
         f"walpole_head|{WALPOLE} sitting at the head of a table full of papers, confident, ministers listening" + LON + ANO("1721") + PAPEL + SEMTXT + SEMBAND + "@@ROBERT WALPOLE",
         f"walpole_refuses|{WALPOLE} waving his hand in refusal with an offended face while a man offers him a fancy title scroll" + LON + ANO("1730") + PAPEL + SEMTXT + SEMBAND]
P[53] = ["navy_dockyard|A huge 18th-century English dockyard with warships being built, many workers" + ING + ANO("1750") + SEMTXT + SEMBAND]
P[54] = ["seven_years_ships|English warships of the 1750s sailing in a line on a blue sea" + ANO("1759") + SEMTXT + SEMBAND + GUERRA + NAO_EG,
         "map_1763|Map of the world with Britain, eastern North America including Canada and parts of India shaded in flat pink, " + MAPA]
# 9. A MEDALHA QUE FICOU NA FRANÇA
P[55] = ["medal_closeup|A bronze medal on dark velvet, showing a simple relief of a strong man wrestling a sea creature, no letters visible, warm light, nobody in the picture" + SEMTXT + NAO_EG,
         f"napoleon_medal|{NAPO} holding up a medal proudly in a tent" + FRA + ANO("1804") + SEMTXT + SEMBAND]
P[56] = [f"guide_banner|{GUIA} proudly holding a champion's sash before a football final, a stadium behind, the sash blank" + SEMTXT + SEMBAND + MOD,
         "boulogne_camp|A huge military camp on the cliffs of Boulogne in 1804 with rows of tents and flat-bottomed boats on the beach, looking toward England" + FRA + ANO("1804") + SEMTXT + SEMBAND + "@@BOULOGNE",
         "trafalgar|British and French warships of 1805 in battle lines with smoke on a blue sea, no flags" + ANO("1805") + SEMTXT + SEMBAND + GUERRA + NAO_EG + "@@TRAFALGAR"]
P[57] = ["stamp_tax_colonies|Round-white-head cartoon American colonists of 1765 in a Boston street reading a notice and shaking their fists, the notice blank" + ANO("1765") + SEMTXT + SEMBAND + ", strictly colonial Boston: brick houses" + NAO_EG,
         "map_america_leaves|Map of the North Atlantic with the thirteen American colonies changing from pink to a different flat color, " + MAPA]
P[58] = ["factory_chimneys|An English industrial town of the 1850s with brick factories and tall smoking chimneys, a canal with barges" + ING + ANO("1850") + SEMTXT + SEMBAND,
         "map_empire_1920#aberto"]
P[59] = ["famine_symbol|Symbolic scene: an empty potato basket and an empty rice bowl side by side on a bare wooden table, grey light, nobody in the picture" + SEMTXT + NAO_EG,
         "india_crowd_dignity|Round-white-head cartoon Indian villagers of the 1870s standing with dignity in a dry field, drawn without caricature, no suffering shown" + ANO("1876") + SEMTXT + SEMBAND + ", strictly India, NO pyramids, NO pharaoh headdress, NO camels" ]
P[60] = [f"victoria_albert|{VICT} and {ALBERT} at home by a fireplace, talking warmly, a Christmas tree in the corner" + LON + ANO("1850") + SEMTXT + SEMBAND + "@@VITÓRIA E ALBERTO"]
P[61] = [f"guide_piece3|{GUIA} fitting the third jigsaw piece: a ship, completing a crown, a parchment and a ship" + SEMTXT + SEMBAND + MOD,
         "crown_outside_paper_inside|Symbolic scene: a crown arriving through an open window from outside, while inside the room a long parchment sits on the table under lamp light" + LON + PAPEL + SEMTXT + SEMBAND,
         "map_1914|Map of Europe with Britain and Germany shaded in two strong flat colors facing each other across the North Sea, " + MAPA]
# 10. A CONTA CHEGA
P[62] = ["washington_1945|Washington D.C. in autumn 1945 with a white neoclassical government building and big American cars of the 1940s" + ANO("1945") + SEMTXT + SEMBAND + NAO_EG,
         f"negotiator|{NEGOC} sitting across a table from American officials, tired, papers everywhere" + ANO("1945") + PAPEL + SEMTXT + SEMBAND + NAO_EG]
P[63] = [f"george5_rename|{GEORGE5} at a desk signing a document while a courtier removes an old painted sign from the wall, the sign blank" + LON + ANO("1917") + PAPEL + SEMTXT + SEMBAND + "@@JORGE V",
         "windsor_castle|Windsor Castle with its round tower on a green hill by the Thames, summer" + ING + SEMTXT + SEMBAND + "@@WINDSOR"]
P[64] = ["india_1947|Round-white-head cartoon Indian crowds celebrating in a city street in August 1947, drawn with dignity, no caricature" + ANO("1947") + SEMTXT + SEMBAND + ", strictly India, NO pyramids, NO pharaoh headdress, NO camels",
         "map_empire_shrinking|Map of the world with only a few small pink spots left, the rest pale, " + MAPA,
         "brussels_join|Round-white-head cartoon diplomats of 1973 shaking hands around a round table in a modern European conference room" + ANO("1973") + SEMTXT + SEMBAND + NAO_EG]
P[65] = ["last_payment|A modern office of 2006 with a computer screen showing a simple completed progress bar, a cup of tea beside it, no letters" + LON + ANO("2006") + SEMTXT + SEMBAND,
         f"guide_receipt|{GUIA} holding a very long old receipt that unrolls across the floor of a modern living room, amazed" + SEMTXT + SEMBAND + MOD]
P[66] = ["westminster_2023|Westminster Abbey in London on a grey May morning of 2023, crowds behind barriers, a golden carriage passing" + LON + ANO("2023") + SEMTXT + SEMBAND,
         "family_tree_symbol|Symbolic scene: a big old family tree drawn as branches with small round portraits, from a man in a white wig at the root to a modern man at the top, no names" + SEMTXT + SEMBAND + NAO_EG,
         f"king2023_oath|{REI23} with his hand on a big book at an altar inside a Gothic abbey, taking an oath" + LON + ANO("2023") + SEMTXT + SEMBAND]
P[67] = ["standard_promise#detalhe-centro",
         "parliament_today|The Houses of Parliament by the Thames today with the big clock tower, people walking on the bridge" + LON + ANO("2023") + SEMTXT + SEMBAND,
         "king_parliament_balance|Symbolic scene: an old balance scale with a small gold crown on one side and a heavy rolled parchment on the other, the parchment side lower" + SEMTXT + SEMBAND + ING]
# FECHO
P[68] = ["carey_gallop#detalhe-centro", "crown_from_sea#médio-dir", "quill_sign#aberto",
         "paper_credit_fleet|Symbolic scene in three steps from left to right: a parchment, then a stack of gold coins, then a big sailing warship, connected by arrows of light, no letters" + SEMTXT + SEMBAND + ING,
         "map_empire_1920#detalhe-alto",
         f"guide_answer|{GUIA} standing between a small crown on a stool and a big parchment on a lectern, explaining with open hands" + LON + SEMTXT + SEMBAND]
P[69] = ["william_trembling#detalhe-centro", "westminster_today_abbey|The old Westminster Abbey and the Houses of Parliament side by side seen from across the street on a sunny day, red buses passing" + LON + ANO("2023") + SEMTXT + SEMBAND]
P[70] = [f"guide_end|{GUIA} waving goodbye at the viewer on a London bridge, the Thames behind, smiling" + LON + SEMTXT + SEMBAND]


# ───────────────────────── HOOK (Carey, 1603) ─────────────────────────
cap("Hook")
b("[curious] Palácio de Richmond, março de mil seiscentos e três. Imagine que você é Robert Carey, um nobre inglês. A rainha Elizabeth acabou de morrer, sem filhos.", card="1603")
b("Você monta e galopa para o norte. Sessenta horas, até Edimburgo, para dar a notícia: o rei da Inglaterra agora é um escocês. O vizinho da guerra de sempre.")
b("[serious] E aí fica a pergunta: como um país que vivia buscando rei lá fora acabou mandando em um quarto do mundo?")
b("Porque não foi a primeira vez. Um dinamarquês e um normando tomaram a coroa à força; o normando, coroado num Natal em que a vizinhança pegava fogo. Um francês, um holandês e um alemão a receberam.")
b("E cada um pagou um preço. Um deles teve de aceitar, por escrito, que não cobraria um centavo de imposto sem pedir licença.")
b("Essa é a história inteira da Inglaterra. E começa numa ilha que todo mundo atravessa.")

# ───────────────────────── 1. A ILHA QUE TODO MUNDO ATRAVESSA ─────────────────────────
cap("1. A ilha que todo mundo atravessa")
b("§ Mil e dezesseis. Um dinamarquês, Canuto, senta no trono da Inglaterra. Ele também manda na Dinamarca e na Noruega: a ilha vira província de um império do mar do Norte.", card="1016")
b("Não era novidade. Antes dele, atravessaram o mar os romanos, depois os anglos e os saxões, depois os vikings. Alfredo, o Grande, segurou os vikings no sul. Mas a ilha seguia sendo onde todo mundo desembarcava.")
b("Só que deixava marca. Se você já disse sky, egg ou knife, falou palavras dos vikings.")
b("§ Conta uma lenda, escrita uns cem anos depois, que Canuto mandou o mar recuar. A versão que você conhece é a do rei arrogante. Só que a lenda original diz o contrário: ele molha os pés de propósito, para mostrar aos bajuladores que rei nenhum manda nas ondas.")
b("Repare no recado: rei de fora, para ser aceito, tinha de parecer menor.")
b("Canuto morre em mil e trinta e cinco, os filhos brigam e a coroa volta para um inglês. O problema é que, do outro lado do canal, um parente normando achava que ela era dele.")

# ───────────────────────── 2. GRITOS EM DUAS LÍNGUAS ─────────────────────────
cap("2. Gritos em duas línguas")
b("§ Abadia de Westminster, Natal de mil e sessenta e seis. Guilherme da Normandia, que venceu em Hastings dois meses antes, vai ser coroado.", card="1066")
b("Lá dentro, um bispo pergunta em francês se aceitam o novo rei, e um arcebispo repete em inglês. A igreja inteira grita que sim.")
b("Só que, do lado de fora, os guardas normandos não entendem os gritos. Acham que é revolta e põem fogo nas casas vizinhas. A igreja esvazia, e um cronista conta que Guilherme terminou a cerimônia tremendo.")
b("Já aplaudiu um discurso numa língua que você não entende? Aqueles guardas fizeram o contrário: ouviram aplauso e entenderam ataque.")
b("§ Então o normando faz o que conquistador faz: castelo de pedra e terra para os seus. Vinte anos depois, manda contar o reino inteiro, até os porcos, num livro de impostos. Imagine o fiscal contando as suas galinhas.")
b("E a corte fala francês por uns três séculos. O problema: o rei da Inglaterra agora também era senhor na França, e o dinheiro atravessava o canal na direção errada.")

# ───────────────────────── 3. O REI PRESO NA ILHA ─────────────────────────
cap("3. O rei preso na ilha")
b("§ Ruão, junho de mil duzentos e quatro. A capital da Normandia se rende ao rei da França. O rei João perde a terra de onde a família tinha vindo.", card="1204")
b("João era filho de Henrique Segundo, um francês nascido em Le Mans, que herdou a Inglaterra por acordo e chegou a mandar em metade da França.")
b("Agora imagine o problema dele: preso na ilha, querendo a Normandia de volta e sem dinheiro. A solução de sempre? Imposto. E mais imposto.")
b("§ Então os barões se cansam. Em mil duzentos e quinze, obrigam João a aceitar a Magna Carta: imposto extraordinário, só com o conselho do reino. O papa anula em semanas, mas o papel volta, reeditado, várias vezes.", card="1215")
b("Mas quem dá o passo seguinte é outro estrangeiro. Simon de Montfort, nobre nascido na França e cunhado do rei, lidera uma revolta. Em mil duzentos e sessenta e cinco, chama para o parlamento não só barões, mas gente das cidades.", card="1265")
b("Aqui está a primeira peça da resposta: rei que precisa de dinheiro precisa pedir. E quem é pedido aprende a cobrar. Você mesmo: quando alguém te pede um favor grande, não pede nada em troca?")
b("O problema é que esse país que cobrava o rei ainda fazia isso em francês.")

# ───────────────────────── 4. A LÍNGUA VOLTA ─────────────────────────
cap("4. A língua volta")
b("§ Westminster, mil trezentos e sessenta e dois. O Parlamento aprova uma lei: nos tribunais, a partir de agora, se fala inglês. O detalhe é ótimo: a lei foi escrita em francês.", card="1362")
b("Imagine ser julgado numa língua que você não entende: era a vida do camponês inglês. E havia um motivo a mais, porque a Inglaterra estava em guerra com a França, a Guerra dos Cem Anos.")
b("§ Em mil trezentos e noventa e nove, Henrique Quarto reivindica o trono diante do Parlamento. Em inglês. Só que a guerra termina, em mil quatrocentos e cinquenta e três, com quase tudo perdido na França.", card="1399")
b("Então a briga vira caseira: Lancaster contra York, trinta anos de Guerra das Rosas.")
b("E quem ganha? Mais um que vinha de fora. Henrique Tudor, criado no exílio, desembarca em Gales em mil quatrocentos e oitenta e cinco, com mercenários franceses, e vence.", card="1485")
b("O novo rei chega com uma meta: nunca mais depender de barão. O problema é que, para isso, a família dele também ia precisar do Parlamento.")

# ───────────────────────── 5. O REI FORTE QUE PRECISOU DO PAPEL ─────────────────────────
cap("5. O rei forte que precisou do papel")
b("§ Londres, mil quinhentos e vinte e nove. Henrique Oitavo, filho do Tudor, quer anular o casamento, e o papa diz não. Imagine o rei mais poderoso da Inglaterra esperando licença de Roma.", card="1529")
b("Então ele faz uma coisa nova: em vez de brigar sozinho, chama o Parlamento. Por sete anos, lei após lei, o Parlamento corta os laços com Roma. Em mil quinhentos e trinta e quatro, faz do rei o chefe da Igreja da Inglaterra.", card="1534")
b("Só que repare: se uma lei do Parlamento muda até a religião do país, o que ela não pode mudar? E as terras dos mosteiros, vendidas, vão parar com gente que senta no Parlamento.")
b("Pense em emprestar a chave da sua casa para alguém regar as plantas. Depois, vai ser difícil pedir de volta.")
b("§ A filha de Henrique, Elizabeth, reina quase quarenta e cinco anos, enfrenta a Armada espanhola e nunca se casa. E voltamos ao galope do começo: sem herdeiro, a coroa vai para o vizinho do norte.", card="1588")
b("O problema: o escocês que chegava acreditava que rei só presta contas a Deus.")

# ───────────────────────── 6. O NOME RECUSADO ─────────────────────────
cap("6. O nome recusado")
b("§ Londres, abril de mil seiscentos e quatro. O novo rei, Jaime, pede à Câmara dos Comuns um título novo: rei da Grã-Bretanha. E os Comuns dizem não.", card="1604")
b("Lembra do escocês do começo? Ele esperava esse trono havia anos, e trocava até cartas secretas com o ministro da rainha. Só não esperava o não. Assume o título por proclamação, mas o recado estava dado.")
b("§ Buckinghamshire, mil seiscentos e trinta e sete. O fidalgo John Hampden se recusa a pagar vinte xelins da taxa dos navios, que o filho de Jaime, Carlos Primeiro, cobra sem Parlamento. Perde no tribunal por sete votos a cinco. E vira herói.", card="1637")
b("Carlos governa onze anos sem Parlamento. Imagine o síndico cobrando taxa extra sem assembleia por onze anos. Até que, em mil seiscentos e quarenta, falta dinheiro para guerrear com os escoceses, e a assembleia volta. Agora ponha exércitos nessa reunião.", card="1640")
b("[serious] O resultado é uma guerra civil. Em mil seiscentos e quarenta e nove, o rei é julgado e executado em Londres. E por onze anos a Inglaterra fica sem rei.", card="1649")
b("Lembra da nossa pergunta? Ela acabou de ficar mais estranha: o país que vai mandar no mundo está sem rei nenhum. Em mil seiscentos e sessenta, a monarquia volta. O problema é que, quando o rei seguinte vira católico, a ilha protestante vai procurar outro. Lá fora.", card="1660")

# ───────────────────────── 7. A INVASÃO POR CONVITE ─────────────────────────
cap("7. A invasão por convite")
b("§ Novembro de mil seiscentos e oitenta e oito. Na costa sul da Inglaterra, desembarca um exército holandês. Nos estandartes, segundo os relatos, em vez de ameaça, uma promessa: as liberdades da Inglaterra e a religião protestante.", card="1688")
b("Quem chegava era Guilherme de Orange, holandês e genro do rei. Convidado: sete ingleses poderosos tinham escrito pedindo que viesse. O rei católico, Jaime Segundo, foge para a França. Guarde essa promessa no estandarte.")
b("§ Então, em fevereiro de mil seiscentos e oitenta e nove, Guilherme e a mulher, Maria, ouvem a leitura de uma declaração: sem o Parlamento, o rei não cobra imposto nem mantém exército em tempo de paz. E aceitam a coroa.", card="1689")
b("E aqui muda tudo. Guilherme queria guerra contra a França, e guerra custa caro. Em mil seiscentos e noventa e quatro, um grupo de comerciantes funda o Banco da Inglaterra e empresta ao governo um milhão e duzentas mil libras, a oito por cento.", card="1694")
b("Por que emprestar? Porque um rei sozinho podia dar calote. Um Parlamento de proprietários e comerciantes, os próprios credores, pagava. É como o seu crédito no banco: se você paga em dia, o juro cai.")
b("Segunda peça da resposta: o papel que amarrava o rei de fora deixou o país confiável para pedir emprestado. O problema é que a rainha Ana morre sem filhos vivos, e a lei manda buscar o próximo protestante na Alemanha.")

# ───────────────────────── 8. O REI QUE PRECISA DE LICENÇA ─────────────────────────
cap("8. O rei que precisa de licença")
b("§ Mil setecentos e um. O Parlamento escreve as regras para um rei que ainda nem chegou. Protestante. Nada de guerra pelas terras dele lá fora sem o Parlamento. E nem sair da ilha sem licença.", card="1701")
b("Imagine o seu chefe novo chegando com a lista do que ele não pode fazer. Assim chega, em mil setecentos e catorze, Jorge de Hanôver. Fala pouco inglês e prefere o francês. Dois anos depois, pede para visitar a terra dele, e o Parlamento revoga a cláusula.", card="1714")
b("§ Com o tempo, Jorge deixa de ir às reuniões com os ministros. Aí quem senta na cabeceira é Robert Walpole, chefe do Tesouro por vinte e um anos: o que hoje chamamos de primeiro-ministro. Ele mesmo recusava o título; soava como ofensa.", card="1721")
b("Então o crédito barato vira navio. A dívida do país se multiplica por mais de dez em menos de cem anos. Quase tudo vira frota.")
b("Em mil setecentos e sessenta e três, a Grã-Bretanha, já unida à Escócia, vence a França e fica com o Canadá e o caminho da Índia. Só que essa conta também precisava de alguém para pagar.", card="1763")

# ───────────────────────── 9. A MEDALHA QUE FICOU NA FRANÇA ─────────────────────────
cap("9. A medalha que ficou na França")
b("§ Agora olhe para esta medalha francesa de mil oitocentos e quatro. A inscrição diz: descida na Inglaterra, cunhada em Londres. Foi feita antes da invasão. A invasão nunca veio.", card="1804")
b("É como você mandar bordar a faixa de campeão antes da final. Napoleão tinha um exército enorme em Boulogne. Mas a frota paga com a dívida venceu em Trafalgar, em mil oitocentos e cinco, e a medalha ficou na França.", card="1805")
b("Vinte anos antes, a mesma conta tinha custado a América. Londres taxou as colônias, e os colonos responderam com o velho argumento inglês: sem representação, sem imposto. Em mil setecentos e oitenta e três, eles se foram.")
b("§ Então o crédito, a frota e o carvão das fábricas fazem o resto. No começo do século vinte, o império britânico ocupa perto de um quarto das terras do mundo, com uns quatrocentos e cinquenta milhões de pessoas.", card="1922")
b("[serious] Muita gente pagou caro por esse império, da Índia à Irlanda: fomes, guerras e governos que ninguém escolheu.")
b("E no trono, no auge? A rainha Vitória, neta de um rei de Hanôver, casada com o príncipe alemão Alberto. Em casa, os dois falavam alemão.")
b("Terceira peça da resposta: a coroa vinha de fora, mas o poder ficava do lado de dentro, no papel. E foi o papel que pagou a frota. O problema é que, em mil novecentos e catorze, o inimigo passa a ser justamente a Alemanha.", card="1914")

# ───────────────────────── 10. A CONTA ─────────────────────────
cap("10. A conta chega")
b("§ Washington, mil novecentos e quarenta e cinco. A guerra acabou, e o país que emprestou ao mundo por dois séculos agora pede: quase quatro bilhões de dólares aos americanos.", card="1945")
b("No meio do caminho, em mil novecentos e dezessete, o rei Jorge Quinto tinha trocado o nome alemão da família por um bem inglês: Windsor. A coroa de fora agora queria parecer de dentro.", card="1917")
b("§ Então o império encolhe. A Índia fica independente em mil novecentos e quarenta e sete. Em setenta e três, o país entra no mercado comum europeu; em dois mil e dezesseis, vota para sair.", card="1947")
b("Só que a conta demorou: a última parcela foi paga em vinte e nove de dezembro de dois mil e seis. Imagine quitar em dois mil e seis uma conta de quarenta e cinco.", card="2006")
b("§ Seis de maio de dois mil e vinte e três. Carlos Terceiro, descendente direto daquele Jorge de Hanôver, é coroado em Westminster. Antes da coroa, faz um juramento: governar os seus povos segundo as leis e os costumes deles.", card="2023")
b("Lembra da promessa no estandarte de mil seiscentos e oitenta e oito? Você acabou de ouvi-la de novo. Quem promete é o rei; quem cobra é o Parlamento.")

# ───────────────────────── FECHO (≤ 45 s) ─────────────────────────
cap("Fecho")
b("§ Então, como um país que vivia buscando rei lá fora acabou mandando em um quarto do mundo? Porque cada rei de fora chegava precisando dos ingleses e pagava com um pedaço de poder escrito no papel. O papel virou crédito; o crédito, frota; a frota, império.")
b("Talvez a pergunta certa nunca tenha sido por que eles importavam reis. Era por que podiam: o rei já não era quem mandava. [break] Hoje, o Parlamento continua a poucos passos da abadia onde Guilherme tremeu.")
b("[warm] Qual desses reis de fora você não conhecia? Conta nos comentários.")

# Grafia para a VOZ (o Fish lê como português). Conferir no teste de nomes (qa/pronuncia/).
# blocos.json leva "texto" (falado, vai ao Fish) e "tela" (grafia correta: legendas e SCRIPT).
FALA = [("Robert Carey", "Róbert Kéri"), ("Richmond", "Rítchmond"), ("Canuto", "Canúto"), ("sky, egg ou knife", "scái, égue ou náife"),
        ("Westminster", "Uéstminster"), ("Hastings", "Hêistings"), ("Ruão", "Ruão"), ("Le Mans", "Le Mã"), ("Simon de Montfort", "Simón de Monfór"),
        ("Calais", "Calê"), ("Lancaster", "Lâncaster"), ("York", "Iórque"), ("Tudor", "Túdor"), ("Orange", "Orânge"),
        ("Hanôver", "Hanôver"), ("Walpole", "Uólpol"), ("Boulogne", "Bulônhe"), ("Trafalgar", "Trafalgár"), ("Windsor", "Uíndsor"),
        ("Washington", "Uóchinton"), ("John Hampden", "Djón Rêmpden"), ("Buckinghamshire", "Bâkinghamxer")]
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
