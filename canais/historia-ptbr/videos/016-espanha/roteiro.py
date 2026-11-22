#!/usr/bin/env python3
"""Fonte única do 016-espanha (21/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

13º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
6º com ÂNGULO próprio (ANGULO.md): "a costura" — o casamento de 1469 junta coroas, não países; o Novo Mundo é de Castela e o império
adia a costura; quando o dinheiro aperta, Madri costura à força (1624–1640, 1707–1717) e cada costura deixa alguém de fora
(foros bascos e navarros, a América de Cádis, os nacionalismos acelerados por 1898) até a costura assinada de 1978.
EMBALAGEM.md aprovada no crivo r3:
  A/T1 "A Espanha juntou meio mundo. Por que não juntava a si mesma?" + thumb rosto-emocao (rei com pilha de coroas, "REI DAS ESPANHAS")
  B/T2 "Por que a Espanha cobrava ALFÂNDEGA de si mesma até 1841?" + thumb conflito-xvy (fiscal castelhano × mercador navarro, "CASTELA × NAVARRA")
  C/T3 "Espanha: o império que ainda não era um país" + thumb objeto-simbolo (coroa partida e costurada, "1469")
Hook: Fernando disfarçado + licença falsa (1469) → "junta duas coroas… não dois países: lei, alfândega, moeda" (≤ 0:35) → PERGUNTA CENTRAL (≤ 0:50)
  → "rei das Espanhas, no plural, uma pilha de coroas" + "última alfândega de dentro só caiu em 1841" (≤ 1:05) → "essa é a história inteira".
Peças da resposta: 1 (cap. 4) nasceu de casamento, herança e acaso; 2 (cap. 6) quando o dinheiro apertou, costura à força arrebenta;
  3 (cap. 8) cada costura decide antes quem conta. Fecho: o mundo veio primeiro e pagou a conta.
"Guarde" único: o plural "Espanhas" → pago no cap. 5 (HISPANIARVM REX) e no fecho/cap. 10 (rei da Espanha, art. 56).
Neutralidade: Corpus de Sang, guerras carlistas, Guerra Civil, Franco, 2017 com contexto e sem lado. Mitos evitados: "Tanto monta" como lema
  dos dois, "catalães proibidos por lei de ir à América", "1898 criou os nacionalismos", "Bórgia trouxe a bula", "sol nunca se põe" como citação.

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1066") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006–014).
Imagens: Codex (canal.yaml visual.gerador: codex; fallback nano-banana). Prompts só de conteúdo; o estilo vem do canal.yaml.
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (006–014: ~128–130 ppm com pausas)
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
TITULO = "A história INTEIRA da Espanha"
PERGUNTA = "Por que a Espanha juntou meio mundo antes de conseguir juntar a si mesma?"
PROMESSA = ("Por que a Espanha juntou meio mundo antes de conseguir juntar a si mesma: o casamento de coroas, as alfândegas e moedas "
            "de dentro até 1717 e 1841, o rei das Espanhas no plural e cada costura que deixou alguém de fora (EMBALAGEM.md r3).")
TITULOS = ('T1 "A Espanha juntou meio mundo. Por que não juntava a si mesma?" / T2 "Por que a Espanha cobrava ALFÂNDEGA de si mesma até 1841?" / '
           'T3 "Espanha: o império que ainda não era um país"')

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
# As refs de estilo vêm do Egito e vazam conteúdo (visual.md 010/011/013/014): TODA cena leva o cenário ancorado (CAS/ARA/NAV/AND/MAD/SEV/...)
# + SEMTXT; cena com gente, navio ou praça leva SEMBAND (nunca bandeira de hoje, nem a vermelha-amarela antes de 1785, nem republicana/franquista/estelada).
# Mapas: MAPA (sem letras; rótulos no código via "@@"). X() monta o prompt na ordem: cena + cenário + época + papel + sem texto + sem bandeira + guerra.
MAPA = ("painted like a blank parchment terrain map seen from directly above, only coastlines, seas, rivers, mountains and flat colored areas, "
        "completely blank with no writing anywhere, no letters, no words, no labels, no symbols, no compass, no border, no frame, no flags, no people")
SEMTXT = ", no readable writing, no letters anywhere, no numbers, no signs, no boards, no logos"
SEMBAND = ", no flags of any kind, no banners, no pennants, no coats of arms, no emblems, no red and yellow striped cloth"
GUERRA = ", no blood, no wounds, no bodies, no weapons fired, no violence shown"
NAO_EG = ", NO pyramids, NO palm trees, NO pharaoh headdress, NO turbans, NO desert dunes, NO camels, NO Big Ben"
CAS = ", strictly Castile: dry high plateau, golden wheat fields, ochre stone castles and villages, deep blue sky" + NAO_EG
ARA = ", strictly Aragon and Catalonia: thick stone walls, plain Catalan Gothic church with buttresses, Mediterranean hills and sea" + NAO_EG
NAV = ", strictly Navarre and the Basque Country: green mountains, stone houses with red tile roofs, oak trees, the river Ebro, misty light" + NAO_EG
AND = (", strictly medieval al-Andalus (Cordoba, Seville, Granada): horseshoe arches, orange trees, patios with fountains, whitewashed houses, "
       "no Arabic writing on walls, no palm trees, no desert, no pyramids" + NAO_EG)
MAD = ", strictly Madrid: red-brick and pale stone palaces, a wide plaza, dry clear light" + NAO_EG
SEV = ", strictly Seville on the Guadalquivir river: whitewashed houses, orange trees, wooden sailing ships at a stone quay" + NAO_EG
CAD = ", strictly Cadiz: a walled port city on a narrow peninsula surrounded by the sea, whitewashed houses, low stone walls" + NAO_EG
FLA = ", strictly Flanders: red-brick gabled houses, canals, grey sky" + NAO_EG
AME = ", strictly colonial Spanish America: whitewashed stone town with red tile roofs, a plaza with a stone cathedral, green mountains behind" + NAO_EG
ATL = ", open Atlantic sea" + NAO_EG
IBE = ", strictly the Iberian peninsula: ochre plains, olive trees, rocky hills and small stone villages" + NAO_EG
LIS = ", strictly Lisbon: white buildings with tiled roofs on hills above the wide river Tagus" + NAO_EG
ITA = ", strictly Renaissance Rome: ochre walls, marble floors and round arches" + NAO_EG
MOD = ", ordinary modern everyday setting of today" + NAO_EG + ", NO crowns, NO safari helmet"
def ANO(a): return f", period-accurate {a}: clothes, buildings and objects of that time only, no modern objects"
PAPEL = ", the document is drawn as plain wavy lines, completely illegible, no letters, no words"
def X(k, d, cen="", ano=None, band=True, guerra=False, papel=False, rot=None):
    return (f"{k}|{d}{cen}" + (ANO(ano) if ano else "") + (PAPEL if papel else "") + SEMTXT + (SEMBAND if band else "")
            + (GUERRA if guerra else "") + (f"@@{rot}" if rot else ""))
def M(k, d, rot=None): return f"{k}|{d}, " + MAPA + (f"@@{rot}" if rot else "")
# Personagens (bíblia: rosto nunca descrito; "round-white-head cartoon …"; nome real de figura moderna só no rótulo do código)
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes, wearing an ordinary brown felt hat and a plain brown jacket"
FERN = "a round-white-head cartoon 17-year-old prince with short dark hair shape, disguised as a servant in a plain brown tunic and a hood"
FERNR = "a round-white-head cartoon young Prince Ferdinand with short dark hair shape and a fine dark blue tunic with gold trim"
FERNK = "a round-white-head cartoon King Ferdinand with short dark hair shape, a short flat dark beard shape, a plain gold crown and a dark blue robe"
ISAB = "a round-white-head cartoon young Queen Isabella with long reddish-brown hair under a light veil and a dark green dress with gold trim"
RECA = "a round-white-head cartoon Visigothic king with long braids, a short flat beard shape, a plain gold circlet and a heavy green cloak with a round gold brooch"
VISI = "round-white-head cartoon Visigothic nobles with long braids, plain tunics and cloaks with large round gold brooches"
BISP = "round-white-head cartoon bishops in white and gold robes with tall pointed hats"
FER1 = "a round-white-head cartoon old 11th-century king with a long flat white beard shape, a plain gold crown and a red cloak"
CARL1 = "a round-white-head cartoon teenage King Charles with straight blond hair shape, a black velvet cap and a fur-trimmed dark coat"
FIL2 = "a round-white-head cartoon King Philip II dressed entirely in black with a small white ruff and a thin gold chain"
JOANA = "a round-white-head cartoon young queen with long dark hair and a plain black dress"
OLIV = "a round-white-head cartoon Spanish minister of the 1620s with a thin mustache shape, a pointed black beard shape, a black cape and a flat white collar"
FIL4 = "a round-white-head cartoon young king of the 1620s in black clothes with a flat white collar and a pale thin mustache shape"
FIL5 = "a round-white-head cartoon king of 1707 with a white powdered wig, a blue coat with a gold ribbon across the chest"
FER7 = "a round-white-head cartoon king of 1814 with dark side-whiskers shape, a dark military coat with gold shoulder tassels"
MACIA = "a round-white-head cartoon elderly man with a big white mustache shape, a dark suit and a hat in his hand"
MERC = "a round-white-head cartoon Castilian wool merchant in a brown cap, a brown jerkin and a leather purse at his belt"
FISC = "a round-white-head cartoon customs officer with a black wide-brimmed hat, a dark vest and a ledger under his arm"
REI16 = "a round-white-head cartoon 16th-century Spanish king with a short flat beard shape, a red robe with a fur collar and a gold chain"

P = {}
# HOOK
P[1] = [X("road_night", "A dusty road across the dry Castilian plateau at night under a big moon, a small group of riders and mules far away, wheat fields on both sides", CAS, "1469", band=False),
        X("fern_disguised", f"{FERN} walking in front of a group of mule drivers carrying a basket and a lantern, glancing nervously over his shoulder", CAS, "1469", rot="FERNANDO DE ARAGÃO"),
        X("inn_servant", f"{FERN} serving wine at a long table to sleepy merchants in a roadside inn, head lowered, candles", CAS, "1469"),
        X("lantern_close", "Close view of a hand holding an iron lantern lighting a dark road, a hood and the rest in shadow", CAS, "1469", band=False)]
P[2] = [X("fern_reveal", f"{FERNR} pulling off a servant hood in a stable lit by one candle, a fine tunic showing beneath, smiling", CAS, "1469"),
        X("isabel_window", f"{ISAB} at a window of a stone palace in Valladolid, hands clasped, looking out at the dark road, one candle", CAS, "1469", rot="ISABEL DE CASTELA"),
        X("papal_license", "Close view of a papal bull: a large parchment with a round lead seal hanging from cords, a quill beside it, nobody in the picture", ITA, "1469", papel=True, band=False),
        X("dead_pope_tomb", "A simple marble papal tomb in a quiet Roman church with one burning candle and fresh flowers, nobody in the picture", ITA, "1464", band=False),
        X("forger_scribe", "A round-white-head cartoon scribe in a dim room copying a parchment with a sly smile, a seal and ink pot on the desk", CAS, "1469", papel=True)]
P[3] = [X("wedding_discreet", f"A discreet wedding in a small stone hall: {FERNR} and {ISAB} before a priest with only three witnesses and two candles, hands joined", CAS, "1469"),
        X("two_crowns", "Two gold crowns of different shapes side by side on a velvet cushion, one with castle-tower shapes and one with a high plain band, loosely linked by a thin red thread, nobody in the picture", CAS, band=False),
        X("border_barrier", "A toll barrier pole painted in black and white stripes lowered across a dry road between two stone border posts, a round-white-head cartoon guard on each side, a merchant with a donkey cart of wool bales waiting", CAS, "1470"),
        X("coins_two", "Two piles of different coins on a wooden table, big thin silver coins and small thick dark coins, a round-white-head cartoon money changer shrugging between them", CAS, "1470"),
        X("laws_two_books", "A round-white-head cartoon clerk holding two thick law books of different colors with a puzzled face, a pile of rolled charters at his feet", CAS, "1470", papel=True),
        M("map_half_country", "Map of the Iberian Peninsula where the central and eastern halves are shaded in two different flat colors with a thick stitched seam line between them, the rest pale")]
P[4] = [X("guide_question", f"{GUIA} standing on a dry Spanish hill at sunset looking at a ship on the sea with a puzzled hand on his chin", IBE),
        X("globe_half", "An old globe on a wooden table, half of it lit and half in shadow, a red thread running across the seam, nobody in the picture", band=False),
        X("ship_far", "A big sailing ship with plain cream sails leaving a Spanish harbour at sunrise, tiny figures on deck, the sea wide and empty ahead", SEV, "1492")]
P[5] = [X("king_stack", f"{REI16} with a wobbly tall stack of five different crowns on his head (one with flat castle towers, one with a high plain arch, one made of a chain of gold links, one with flower shapes, one simple band), holding the stack with both hands, annoyed eyes rolling upward", CAS, "1580"),
        X("crowns_pile", "Five different gold crowns piled in a crooked tower on a velvet cushion, ready to fall, nobody in the picture", CAS, band=False),
        X("plural_coin", "Close view of a large silver coin with the profile of a king in a ruff and a tiny cross, held between two fingers, plain rim without letters", CAS, "1580", band=False),
        X("ebro_customs_1840", f"A river customs house by the Ebro with a striped barrier pole, {FISC} opening a farmer's cart, green hills behind", NAV, "1840"),
        X("barrier_lifted", "The black and white striped barrier pole lifted at last beside a quiet stone customs hut, a road open to green hills, nobody in the picture", NAV, "1841", band=False),
        X("king_tired", f"{REI16} sitting on a throne scratching his head, a crooked stack of crowns on a small table beside him", CAS, "1580")]
P[6] = [X("guide_plural", f"{GUIA} holding up one finger toward the viewer, a thought bubble above him with a tiny stack of crowns", IBE),
        M("map_peninsula", "Map of the whole Iberian Peninsula with blank soft terrain, mountains in the north and a long sea coast"),
        X("peninsula_sunrise", "Wide view of a rugged Iberian landscape at sunrise, mountains, plains and several small stone villages far apart, no people", IBE, band=False),
        X("many_paths", "Several dirt roads leaving a central stone crossroads in different directions across the Iberian plateau, plain milestone stones, nobody in the picture", IBE, band=False)]
# 1. A COSTURA POR CIMA
P[7] = [X("toledo_589", "Toledo on its rocky hill above the river Tagus, a plain stone church with round arches, ochre walls", CAS, "589 AD", band=False),
        X("reca_council", f"{RECA} addressing {BISP} seated on benches inside a plain stone church, candles, one hand open", CAS, "589 AD", rot="RECAREDO"),
        X("bishops_nod", f"{BISP} raising their hands in agreement before a plain altar with a simple cross", CAS, "589 AD"),
        X("reca_cross", f"{RECA} kneeling at an altar placing his gold circlet on a cloth under a plain gold cross", CAS, "589 AD"),
        X("visigoth_nobles", f"{VISI} standing in a stone hall, listening", CAS, "589 AD")]
P[8] = [X("few_among_many", f"A small group of {VISI} standing among a huge crowd of round-white-head cartoon Hispano-Roman townspeople in plain tunics on a stone-paved town square", CAS, "580 AD"),
        X("roman_aqueduct", "An old Roman stone aqueduct with round arches crossing ochre fields in Hispania, farmers working below", CAS, "580 AD", band=False),
        X("latin_school", "A round-white-head cartoon teacher in a plain tunic teaching children sitting on the floor with wax tablets covered in plain wavy lines", CAS, "580 AD", papel=True),
        X("same_prayer", "A crowd of round-white-head cartoon people of different clothes kneeling together in rows in one stone church, one plain cross at the front", CAS, "589 AD"),
        X("village_mix", "A village market street where braided Visigoths and Hispano-Romans buy bread and cheese side by side, stone houses and ochre walls", CAS, "580 AD")]
P[9] = [X("jewish_family", "A round-white-head cartoon family in plain tunics and head scarves standing in front of their modest stone house, worried, holding a small oil lamp, no religious symbols", CAS, "640 AD"),
        X("king_decree", f"{RECA} on a wooden throne holding out a scroll toward a crowd, stern", CAS, "640 AD", papel=True),
        X("baptism_font", "A stone baptismal font in a church, a priest holding a jug and a reluctant family waiting in line, nervous faces", CAS, "640 AD"),
        X("two_doors", "Two doors side by side in an ochre stone wall, one open to a church and one shut, a round-white-head cartoon man standing before them thinking", CAS, "640 AD"),
        X("guide_imagine", f"{GUIA} in a modern living room with his arms crossed and one eyebrow raised, a thought bubble with a small stone church", band=False, cen=MOD)]
P[10] = [X("strait_boats", "Many small wooden boats crossing a narrow blue strait from a rocky coast to a green Iberian coast, tiny figures with round shields aboard seen from far", AND, "711", guerra=True),
         X("horsemen_far", "A long column of horsemen with round shields and spears seen from far as tiny figures on a dry hill, a dust cloud, quiet", AND, "711", guerra=True),
         X("visigoth_town_leaving", "A Visigothic stone town with an open gate, citizens carrying bundles along a road out of town, calm, no soldiers in sight", CAS, "712 AD", guerra=True),
         X("empty_throne_toledo", "An empty wooden throne in a stone hall of Toledo with a crown fallen on the floor and a map on a table, nobody in the picture", CAS, "712 AD", band=False),
         X("hourglass_window", "A big old wooden hourglass with sand almost run out on a stone window ledge overlooking green hills, nobody in the picture", IBE, band=False)]
P[11] = [M("map_alandalus", "Map of the Iberian Peninsula with all of the south and center shaded in a flat green and only a narrow northern strip of mountains shaded in grey-blue", "AL-ANDALUS"),
         X("cordoba_arches", "Inside a grand hall in Cordoba, a forest of double striped horseshoe arches in red and white stone, soft light, a few people walking", AND, "900", band=False),
         X("north_mountains", "Steep green mountains of northern Spain with a small stone village and a tiny stone church on a ridge, low clouds", NAV, "720 AD", band=False)]
P[12] = [X("hill_forts", "Several small stone fortresses on separate hilltops in the northern mountains, each with one small tower, mist in the valleys between", NAV, "800", band=False),
         X("lord_family", "A round-white-head cartoon medieval lord with his wife and four children of different heights standing in front of a stone castle", CAS, "900"),
         X("many_lords", "Four round-white-head cartoon medieval lords of different clothes each standing on their own hilltop looking at each other across the valleys", NAV, "900")]
# 2. A HERANÇA QUE SE PARTE
P[13] = [X("leon_1065", "León in winter: a stone Romanesque church and city walls, snow on the roofs and smoke from chimneys", CAS, "1065", band=False),
         X("fer1_dying", f"{FER1} lying in a bed in a stone chamber, pale, a priest and his three sons around him, candles", CAS, "1065", rot="FERNANDO I DE LEÃO"),
         X("sons_three", "Three round-white-head cartoon young princes of different heights standing in a row before their father's bed, each holding a different small object: a small crown, a sword hilt and a key", CAS, "1065"),
         X("divide_loaf", f"{FER1} cutting a big round loaf of bread into three pieces on a wooden table while his sons watch hungrily", CAS, "1065"),
         M("map_divide_1065", "Map of northwestern Iberia split into three flat colors for three brother kingdoms")]
P[14] = [X("brothers_quarrel", "Three round-white-head cartoon princes in medieval clothes pulling a rolled map in three directions in a castle hall, arguing", CAS, "1068", papel=True),
         X("brothers_field", "Two small armies of round-white-head cartoon knights in chain mail facing each other across a golden field, spears held upright, no fighting", CAS, "1070", guerra=True),
         X("three_chairs_empty", "A castle courtyard with three empty chairs in a row, one overturned, dim light, nobody in the picture", CAS, "1070", band=False)]
P[15] = [X("three_walls", "A dry plot of land divided by three stone walls in a row with a half-built house in the middle, a round-white-head cartoon family looking sadly at it", CAS),
         X("heirs_chest", "A round-white-head cartoon medieval king carrying a heavy map-shaped chest and handing a piece to each of his three heirs in a hall", CAS, "1070"),
         "map_divide_1065",
         "divide_loaf"]
P[16] = [X("deathbed_1157", "A round-white-head cartoon medieval king on his deathbed dividing a parchment map into two halves, two sons kneeling", CAS, "1157", papel=True),
         "map_divide_1065",
         X("crowns_reunited", "Two crowns being joined into one on a cushion by a bishop's hands in a stone cathedral, candles", CAS, "1230", band=False),
         "brothers_field",
         M("map_portugal_leaves", "Map of the Iberian Peninsula with the western coastal strip shaded in a separate flat green and a thin dotted line separating it from the rest", "PORTUGAL"),
         "three_walls"]
P[17] = [M("map_four_crowns", "Map of the Iberian Peninsula in four flat colors for four Christian kingdoms in the north and center, and a small separate southern corner in green", "GRANADA"),
         X("reconquista_march", "Round-white-head cartoon Castilian knights riding south across a golden plain toward a distant white town, no fighting", CAS, "1240", guerra=True),
         X("granada_hill", "Granada: a hilltop palace city with red walls and horseshoe-arch gates and orange trees, snowy mountains behind", AND, "1400", band=False),
         "map_alandalus",
         "crowns_reunited"]
# 3. DOIS NOIVOS, DOIS PAÍSES
P[18] = [X("road_wool_1480", f"A dry road in Castile with a train of mules loaded with wool bales heading east toward distant hills, {MERC} walking beside them", CAS, "1480"),
         X("customs_post_wool", f"{MERC} standing in front of a roadside customs post with a black and white striped barrier pole lowered, bales open on the ground, a customs officer inspecting them, a small stone border post", CAS, "1480", rot="ALFÂNDEGA"),
         X("pay_coins", f"{MERC} counting coins into the open hand of the customs officer, opened wool bales beside, annoyed", CAS, "1480"),
         "border_barrier"]
P[19] = [X("royal_couple_throne", f"{ISAB} and {FERNK} sitting side by side on two matching thrones in a stone hall, proud", CAS, "1480"),
         X("merc_irritated", f"{MERC} with his arms crossed staring at the lowered barrier pole, a toll officer shrugging", CAS, "1480"),
         X("two_seals", "Two different royal wax seals side by side on a table, a puzzled clerk with a quill looking at them", CAS, "1480", papel=True),
         "wedding_discreet", "pay_coins", "border_barrier"]
P[20] = [X("change_table", f"{MERC} at a money changer's table with two stacks of different coins and a small balance scale, the changer writing in a ledger", ARA, "1480", papel=True),
         X("coin_swap_close", "Close view of coins swapped across a wooden counter: a few big silver coins on one side and a huge heap of tiny coins on the other, hands only", ARA, "1480", band=False),
         X("barcelona_pastry", f"{MERC} holding out different coins to a baker with a tray of pastries in a Barcelona street, the baker scratching his head", ARA, "1480", rot="BARCELONA"),
         "coins_two", "change_table"]
P[21] = [X("cortes_castile", "A Castilian parliament hall with round-white-head cartoon nobles in plain dark clothes on wooden benches, a royal chair at the front", CAS, "1480"),
         X("cortes_aragon", "An Aragonese parliament in a Gothic stone hall with nobles in dark gowns, one holding a staff, serious", ARA, "1480"),
         "isabel_window",
         "royal_couple_throne", "laws_two_books"]
P[22] = [X("patchwork_kingdoms", "A patchwork quilt of different colored squares, each with a small different landscape of a castle, a harbour or a mountain, spread over a table, nobody in the picture", band=False),
         X("crown_stitched", "A gold crown split in two halves and held together by a thick coarse linen thread sewn across the break in big crude stitches, resting on a dark velvet cushion, nobody in the picture", CAS, band=False),
         "two_crowns"]
P[23] = [X("columbus_ships", "Three small sailing ships with cream sails crossing a wide blue ocean at dawn", ATL, "1492"),
         X("new_land_question", f"{FERNK} and {ISAB} looking at a big rolled map with a green island, both pointing at it, questioning each other", CAS, "1492", papel=True),
         "ship_far", "globe_half"]
# 4. O MUNDO É DE CASTELA
P[24] = [X("seville_quay_1503", "The quay of Seville with wooden ships being loaded with barrels and crates, officials with ledgers", SEV, "1503"),
         X("casa_contratacion", "Inside a trading house: round-white-head cartoon officials at long tables weighing chests and writing in big ledgers, a big world map on the wall", SEV, "1503", papel=True, rot="CASA DE CONTRATAÇÃO"),
         "ship_far",
         "columbus_ships"]
P[25] = [X("guide_post_counter", f"{GUIA} at a modern post office counter handing a parcel to a clerk", band=False, cen=MOD),
         X("one_counter", "A single wide wooden counter in Seville with a long queue of round-white-head cartoon merchants and crates, a huge ocean visible through the window", SEV, "1520"),
         "casa_contratacion", "seville_quay_1503"]
P[26] = [X("colonial_charter", f"{ISAB} signing a parchment with a quill, a small castle-shaped paperweight and a globe beside her", CAS, "1493", papel=True),
         X("barcelona_port_waits", "The port of Barcelona with a few ships tied up and a round-white-head cartoon Catalan merchant looking longingly across the sea", ARA, "1500", rot="BARCELONA"),
         "customs_post_wool",
         "columbus_ships"]
P[27] = [X("granada_surrender", "The red palace city of Granada on a hill, a Castilian court on horseback at the gate, a round-white-head cartoon Granadan king handing over a big iron key, quiet", AND, "1492", guerra=True),
         "globe_half",
         "granada_hill", "columbus_ships"]
P[28] = [X("isabel_deathbed", f"{ISAB} lying in bed in a plain stone chamber, pale, her daughter kneeling beside the bed holding her hand, candles", CAS, "1504"),
         X("joana_crown", f"{JOANA} sitting on a throne staring at nothing, a crown on a cushion beside her", CAS, "1504"),
         X("second_wedding", f"{FERNK} with a gray beard shape standing beside a young round-white-head cartoon French princess in a blue dress in a small chapel, a priest between them", CAS, "1505"),
         "royal_couple_throne"]
P[29] = [X("newborn_hope", f"{FERNK} looking into a cradle with hope, a soft glow of light on the cradle", CAS, "1509"),
         X("empty_cradle", "An empty small cradle with a white blanket and a single candle in a dark royal bedchamber, nobody in the picture", CAS, "1509", band=False),
         "two_crowns",
         "second_wedding", "crown_stitched"]
P[30] = [X("guide_piece1", f"{GUIA} holding up the first piece of a big jigsaw puzzle shaped like a crown, smiling", band=False, cen=MOD),
         "second_wedding",
         X("boy_prince_flemish", f"{CARL1} in a Flemish palace garden looking at a letter", FLA, "1516", papel=True),
         "wedding_discreet", "royal_couple_throne", "empty_cradle"]
# 5. O REI DE UMA LISTA
P[31] = [X("asturias_coast", "A steep green coast in Asturias with a fishing village of stone granaries on stilts, a grey sea, slate roofs", ", strictly Asturias: steep green hills, grey sea, stone houses with slate roofs" + NAO_EG, "1517", band=False),
         X("storm_fleet", "A fleet of sailing ships tossed by a storm, big waves, dark clouds, a few ships turning toward a rocky green coast", ATL, "1517"),
         X("fishermen_scared", "Round-white-head cartoon fishermen on a green cliff pointing at a forest of ship sails on the horizon with wide worried eyes, women pulling children indoors", ", strictly Asturias: steep green hills, grey sea, stone houses with slate roofs" + NAO_EG, "1517"),
         "boy_prince_flemish", "asturias_coast"]
P[32] = [X("carlos_young_king", f"{CARL1} wearing a gold crown too big for him in a Castilian hall, looking lost, courtiers watching", CAS, "1517", rot="CARLOS"),
         "crowns_pile",
         X("five_crowns_row", "Five different gold crowns in a row on a long table, each on its own cushion", CAS, band=False),
         "king_stack"]
P[33] = [X("long_signature", f"{CARL1} sitting at a desk writing with a quill on an extremely long parchment scroll that unrolls across the floor, tired", CAS, "1520", papel=True),
         "plural_coin",
         X("filipe2_black", f"{FIL2} sitting at a desk in a plain grey granite room, a large window with dry hills", CAS, "1580", rot="FILIPE II"),
         "long_signature"]
P[34] = [X("silver_arrives", "Wooden ships unloading heavy chests of silver bars at the Seville quay, officials counting", SEV, "1550"),
         X("castile_farmers_tax", "Round-white-head cartoon Castilian farmers handing sacks of grain and coins to a tax collector at a village door, wheat fields behind", CAS, "1560"),
         "seville_quay_1503",
         "casa_contratacion"]
P[35] = [M("map_world_empire", "Map of the whole world with Spain's territories (Iberia, the middle of the Americas, the Philippine islands and southern Italy) shaded in one flat gold color, the rest pale"),
         X("zaragoza_negotiation", "A round-white-head cartoon royal envoy with a leather folder bowing to seated Aragonese nobles in a Gothic hall, one refusing with a raised hand", ARA, "1570", papel=True),
         "silver_arrives", "cortes_aragon"]
P[36] = [X("perez_flight", "A round-white-head cartoon man in a dark cloak riding a mule along a road in the Pyrenean foothills at night, looking back", ARA, "1591"),
         X("fueros_shield", "A heavy old law book held up like a shield by Aragonese nobles in front of a Gothic building, a royal envoy outside the circle", ARA, "1591", papel=True),
         "filipe2_black",
         X("army_zaragoza", "A column of royal soldiers with pikes in plain dark clothes marching toward the walled city of Zaragoza across a plain, dust", ARA, "1591", guerra=True),
         X("justicia_empty_chair", "An empty tall carved judge's chair in a Gothic stone hall with a black cloth over it and a single candle, nobody in the picture", ARA, "1591", guerra=True, band=False),
         "cortes_aragon"]
P[37] = ["justicia_empty_chair",
         X("olivares_shadow", f"A tall figure in a black cape ({OLIV}) holding a rolled plan beside a young king, seen through a doorway of a Madrid palace", MAD, "1620", papel=True),
         "filipe2_black", "fueros_shield"]
# 6. A CONTA
P[38] = [X("madrid_christmas", "A Madrid palace and plaza at night in winter, lit windows and snow on the rooftops", MAD, "1624", band=False),
         "cortes_castile",
         X("olivares_memorial", f"{OLIV} handing a thick folded memorial to {FIL4} in a candle-lit Madrid study", MAD, "1624", papel=True, rot="OLIVARES"),
         "olivares_shadow"]
P[39] = [X("olivares_writing", f"{OLIV} at a desk writing by candlelight with a quill, a stack of rolled papers beside", MAD, "1624", papel=True),
         X("kingdoms_squeezed", "Five different colored small crowns being pressed into one big castle-shaped mould by a large hand, nobody else", band=False),
         "crown_stitched", "five_crowns_row", "olivares_memorial"]
P[40] = [X("castile_exhausted", "A thin tired Castilian farmer with an empty plate at a table and a bare field behind, a tax collector's shadow on the wall", CAS, "1620"),
         X("union_armas_table", "Round-white-head cartoon royal officials at a table dividing small wooden toy-like soldiers into piles for each kingdom, pushing a big pile toward one side", MAD, "1626", guerra=True),
         "kingdoms_squeezed",
         M("map_union_armas", "Map of the Iberian Peninsula with big Castile in gold and Catalonia, Portugal and Aragon smaller in other flat colors"),
         X("recruits_queue", "A line of round-white-head cartoon young recruits with plain pikes and bundles queuing in a village square in front of a recruiting officer", CAS, "1626", guerra=True),
         "castile_farmers_tax", "olivares_writing"]
P[41] = [X("guide_condo", f"{GUIA} in a modern apartment building lobby holding a clipboard of plain lines while neighbors cross their arms behind him", band=False, cen=MOD),
         X("catalonia_refuses", "Round-white-head cartoon Catalan councillors in dark gowns shaking their heads and crossing their arms in a Gothic council hall in Barcelona", ARA, "1626"),
         "union_armas_table"]
P[42] = [X("soldiers_billeted", "A Catalan farmhouse with a soldier's helmet and boots by the door and the farm family looking upset at the table", ARA, "1640", guerra=True),
         X("reapers_barcelona", "A crowd of round-white-head cartoon harvest workers with sickles held upright in a Barcelona street, a fountain, tense but not attacking", ARA, "1640", guerra=True),
         X("viceroy_flees", "The harbour of Barcelona at dusk with a small boat rowing away from the shore and a fancy cloak left behind on the quay, nobody else visible", ARA, "1640", guerra=True, band=False),
         X("lisbon_1640", "A Lisbon street with round-white-head cartoon townspeople celebrating and waving plain white cloths", LIS, "1640"),
         "catalonia_refuses"]
P[43] = [X("catalonia_france", "Round-white-head cartoon Catalan delegates in dark gowns kneeling before a round-white-head cartoon French king in a blue and gold robe with long curly hair shape, in a hall", ARA, "1641"),
         X("barcelona_siege", "The walled city of Barcelona surrounded by distant army tents, smoke far away, a quiet harbour", ARA, "1651", guerra=True),
         X("island_treaty", "A small island in a river with a wooden pavilion where round-white-head cartoon diplomats of two countries sit at a long table with a map between them, a bridge on each side", ", strictly the western Pyrenees: green hills and a wide river" + NAO_EG, "1659", papel=True),
         M("map_roussillon", "Map of the eastern Pyrenees with a strip of land shaded in a color that shifts from the Iberian side to the French side", "ROSSILHÃO"),
         "lisbon_1640"]
P[44] = [X("guide_piece2", f"{GUIA} holding the second jigsaw puzzle piece, a frayed thread hanging from it, worried", band=False, cen=MOD),
         "guide_question",
         "crown_stitched", "guide_piece1", "king_stack"]
P[45] = [M("map_europe_war", "Map of Western Europe with many small arrows of different colors converging on Iberia"),
         "barcelona_siege",
         "madrid_christmas"]
# 7. DIREITO DE CONQUISTA
P[46] = [X("madrid_1707", "A Madrid palace with a stone façade and tall windows in summer light, courtiers on the steps", MAD, "1707"),
         X("filipe5_sign", f"{FIL5} signing a big decree at a desk, a minister beside him holding the sand pot", MAD, "1707", papel=True, rot="FILIPE V"),
         X("laws_carried_away", "A pile of old law books being carried away by round-white-head cartoon clerks along a stone corridor", ARA, "1707", papel=True),
         "fueros_shield", "cortes_aragon", "kingdoms_squeezed"]
P[47] = [X("last_habsburg", "A round-white-head cartoon pale king in black sitting alone in a big room, an empty cradle beside the throne", MAD, "1700"),
         X("two_claimants", "Two round-white-head cartoon young men in elegant 1700 clothes, one in blue with a white powdered wig and one in a dark coat with a plain hat, glaring at each other across a map table", MAD, "1701", papel=True),
         M("map_succession", "Map of Europe shaded in two big flat colored blocks, one around France and Spain and another around central Europe"),
         "filipe5_sign", "cortes_aragon"]
P[48] = [X("barcelona_walls_1714", "The walled city of Barcelona under a heavy cloudy sky, the Gothic cathedral tower and the sea, smoke far off", ARA, "1714", guerra=True, band=False),
         "laws_carried_away",
         X("court_castilian", "A courtroom of 1716 where a judge speaks and round-white-head cartoon Catalan citizens look puzzled", ARA, "1716"),
         "barcelona_siege"]
P[49] = [X("customs_to_coast", "Black and white striped barrier poles being carried off a dry inland road by workers and loaded on a cart, the road now open, a donkey cart passing", CAS, "1717"),
         X("merc_passes", f"{MERC} leading his mules of wool bales along an open road, smiling, no barrier anywhere", CAS, "1717"),
         X("coast_customs", "A new customs house at the Mediterranean coast with a striped barrier pole and ships in the harbour", ARA, "1717"),
         "customs_post_wool", "merc_irritated"]
P[50] = [M("map_basque_navarre", "Map of northern Spain with the Basque provinces and Navarre shaded in a distinct green and the rest of Spain in a single beige", "NAVARRA E PAÍS BASCO"),
         X("basque_loyal", "Round-white-head cartoon Basque and Navarrese leaders with dark berets bowing politely to a king in blue in a stone hall", NAV, "1707"),
         X("basque_fueros_tree", "An old oak tree in a green Basque valley with a small stone hall beside it where leaders gather around a big old book", NAV, "1707", papel=True),
         X("two_buttons", "A big cloth sewn up tight with thick thread except for two loose buttons dangling, close view, nobody in the picture", band=False),
         "filipe5_sign", "kingdoms_squeezed"]
# 8. OS ESPANHÓIS DOS DOIS HEMISFÉRIOS
P[51] = [X("cadiz_1812", "The walled port city of Cadiz surrounded by sea, distant foreign ships and faint smoke on the horizon", CAD, "1812", guerra=True, band=False),
         X("napoleon_brother", "A round-white-head cartoon man in a gold-trimmed blue coat sitting uneasily on a throne in a Madrid palace, a big bicorne hat on his knees, courtiers whispering", MAD, "1808"),
         X("deputies_cadiz", "Round-white-head cartoon deputies in dark frock coats and white cravats sitting in a round hall writing, candles, a window with the sea", CAD, "1812", papel=True),
         "cadiz_1812"]
P[52] = [X("constitution_book", "A thick new book with a plain cover and a ribbon bookmark open on a lectern, a quill beside it, nobody in the picture", CAD, "1812", papel=True, band=False),
         M("map_four_cities", "Map of the world with four points joined by a thick red stitched line: Iberia, Peru, Mexico and the Philippines", "MADRI, LIMA, MÉXICO, MANILA"),
         X("four_peoples", "Round-white-head cartoon people of four regions drawn with dignity (a Madrid gentleman, a Peruvian townswoman in a poncho, a Mexican farmer in a wide straw hat, a Filipino fisherman in a plain shirt) standing shoulder to shoulder on a stone plaza, smiling", CAD, "1812"),
         "deputies_cadiz", "cadiz_1812"]
P[53] = [X("counters_swept", "Round-white-head cartoon clerks at a table placing wooden counters into rows on a board, a big pile of counters swept aside into a basket", CAD, "1812", papel=True),
         "cortes_castile",
         X("american_deputies_few", "Round-white-head cartoon deputies from America in a few seats at the back of a crowded hall of deputies, looking small", CAD, "1812"),
         "deputies_cadiz", "four_peoples", "constitution_book"]
P[54] = [X("citizen_gate", "A round-white-head cartoon man standing at a locked gate of a big hall, looking in at a lit room where a book lies on a table, his neighbors waiting behind him in the street", AME, "1812"),
         "four_peoples"]
P[55] = [X("fernando7_balcony", f"{FER7} on a balcony holding a thick book high, a crowd below clapping", MAD, "1814", papel=True),
         X("constitution_torn", "A big book torn in half with pages falling, a royal hand over it", MAD, "1814", papel=True),
         X("independence_march", "Round-white-head cartoon patriots in mixed civilian and military clothes marching with plain muskets in front of the Andes, no flags", AME, "1820", guerra=True),
         X("ayacucho_plain", "A high Andean plain at dawn with a wide valley and mountains, small armies far apart, an abandoned cannon in the foreground, no fighting", AME, "1824", guerra=True),
         X("ship_leaving_america", "A Spanish sailing ship leaving a colonial port with a few round-white-head cartoon officials aboard waving sadly, the town shrinking behind", AME, "1824"),
         "map_four_cities", "four_peoples"]
P[56] = [X("guide_piece3", f"{GUIA} holding all three jigsaw puzzle pieces in his hands, thoughtful", band=False, cen=MOD),
         X("counted_out", "A round-white-head cartoon man standing outside a closed door with a bundle, turning away along a long road at dusk", AME, "1820"),
         "two_buttons", "crown_stitched", "guide_piece2"]
# 9. O IMPOSTO QUE FICA EM BILBAO
P[57] = [X("ebro_bridge", "The wide river Ebro with an old stone bridge, a customs hut on the Navarrese bank and a green valley, a cart waiting", NAV, "1840", band=False),
         X("ebro_fiscal", f"{FISC} opening the canvas cover of a farmer's cart at a river bridge, a striped barrier pole lowered", NAV, "1840"),
         "customs_post_wool", "merc_irritated"]
P[58] = [X("carlist_men", "Round-white-head cartoon Basque countrymen in dark berets and plain brown jackets with old muskets standing on a green mountain pass in mist, no fighting", NAV, "1835", guerra=True),
         X("pretender_hill", "A round-white-head cartoon pretender prince in dark hunting clothes on a white horse on a green hill with a few followers, determined", NAV, "1834"),
         X("customs_to_pyrenees", "Striped barrier poles loaded onto carts and carried up a mountain road toward the Pyrenees by workers", NAV, "1841"),
         X("customs_basque_coast", "A customs house on the green Basque coast with fishing boats and a striped barrier pole", NAV, "1841"),
         "ebro_fiscal", "customs_to_coast"]
P[59] = [X("law_1876", "A decree being read aloud to a crowd of Basque leaders in dark berets in a stone hall, one raising a hand in protest", NAV, "1876", papel=True),
         X("agreement_1878", "A round-white-head cartoon Madrid minister in a frock coat shaking hands with a Basque leader in a beret over a table with a thick agreement", MAD, "1878", papel=True),
         X("province_chest", "Basque provincial officials in berets counting coins into a wooden chest in a stone town hall, then a small portion into a separate sack", NAV, "1880", papel=True),
         "basque_fueros_tree", "basque_loyal", "pretender_hill"]
P[60] = [X("bilbao_today", "A modern Basque city of today beside a river with bridges and a pedestrian walkway, people walking, grey-blue sky and green hills behind", MOD + ", Bilbao-like Basque city", band=False),
         X("bilbao_tax_form", "A round-white-head cartoon person in ordinary modern clothes at a kitchen table with a laptop and a tax form of plain lines, looking thoughtful", MOD, band=False, rot="BILBAO"),
         X("money_province_arrow", "A clean diagram: a coin goes into a small house-shaped provincial building and a smaller coin continues on to a big palace, drawn with arrows only", band=False),
         "province_chest", "map_basque_navarre"]
P[61] = [X("caribbean_ships_1898", "Warships with smoke trails near a Caribbean harbour with a stone fortress and low hills, far from the viewer, no people visible", ", strictly the Caribbean coast of Cuba: stone fortress and low green hills" + NAO_EG, "1898", guerra=True),
         X("treaty_paris_1898", "Round-white-head cartoon diplomats of two countries in dark frock coats signing a treaty at a long table, a big map of islands on the wall, one looking glum", ", strictly Paris in 1898: a grand room with tall windows" + NAO_EG, "1898", papel=True),
         X("officials_leave", "Round-white-head cartoon Spanish officials in light uniforms boarding a ship with trunks, looking defeated, a harbour behind them", AME, "1898"),
         "map_world_empire", "ship_leaving_america"]
P[62] = [X("arana_1895", "A round-white-head cartoon man with a dark beard shape and a beret in a small Bilbao meeting room speaking to a few men in dark coats, gas lamps", NAV, "1895", papel=True, rot="SABINO ARANA"),
         X("catalan_election_1900", "A Barcelona street with a ballot box on a table in a plaza and round-white-head cartoon voters queuing, modernist buildings with curved balconies", ARA, "1901"),
         M("map_cracked", "Map of the Iberian Peninsula cut by a thick zigzag crack with a thread pulled loosely through it"),
         X("empty_dock_cadiz", "An empty big dock in Cadiz with a few forgotten trunks and a single seagull, grey light", CAD, "1898", band=False),
         "two_buttons", "treaty_paris_1898", "map_basque_navarre"]
# 10. UMA À FORÇA, UMA ASSINADA
P[63] = [X("sant_jaume_1931", "A big square in Barcelona with a crowd of round-white-head cartoon people in hats looking up at a Gothic town hall balcony, joyful", ARA, "1931"),
         X("macia_balcony", f"{MACIA} on a Gothic town hall balcony with one hand raised, the crowd cheering below", ARA, "1931", rot="FRANCESC MACIÀ"),
         X("hats_in_air", "Close view of round-white-head cartoon people throwing their hats in the air in a Barcelona street", ARA, "1931"),
         X("basque_town_1936", "A Basque town hall in green hills with an old oak tree and a plain document pinned to the door, a small quiet crowd reading", NAV, "1936", papel=True, guerra=True),
         "agreement_1878", "cortes_aragon"]
P[64] = [X("empty_village_symbol", "A quiet village street with shuttered houses, a torn poster of plain shapes on a wall and a child's toy on the ground, nobody else", IBE, "1939", guerra=True, band=False),
         X("silhouette_balcony", "A dark silhouette of a uniformed man in a plain military cap seen from behind on a balcony above an empty plaza, no insignia, no medals, grey light", MAD, "1939", guerra=True, band=False),
         X("school_one_language", "A 1940s classroom with round-white-head cartoon children at wooden desks and a teacher pointing at a blackboard with plain shapes, one child covering his mouth", MAD, "1945"),
         X("palace_doors_chained", "The heavy doors of a Catalan Gothic government palace shut with a thick chain, nobody in the picture", ARA, "1939", band=False),
         "basque_town_1936",
         "sant_jaume_1931"]
P[65] = [X("transition_plaza", "A Madrid plaza with round-white-head cartoon people in 1970s clothes walking out of doors into sunlight, an old black car driving away", MAD, "1975"),
         X("cortes_1978", "A big parliament hall in Madrid with round-white-head cartoon deputies in 1970s suits on rows of benches, bright light", MAD, "1978"),
         X("signing_1978", "A long wooden table where round-white-head cartoon men and women in 1970s suits sign a thick constitution book", MAD, "1978", papel=True),
         X("one_sentence_rope", "A single long rope drawn as a sentence, tied in the middle by a knot, a small house on one end and a big house on the other, nobody in the picture", band=False),
         "two_buttons", "crown_stitched"]
P[66] = [X("polling_1978", "Round-white-head cartoon voters in 1978 clothes dropping paper ballots into a clear box in a school classroom polling station, a queue behind", MAD, "1978"),
         X("king_singular", "A round-white-head cartoon modern king in a plain dark suit standing alone with a single plain gold crown on a stand beside him", MAD, "2000"),
         "king_stack", "crown_stitched"]
P[67] = [M("map_17_regions", "Map of Spain divided into seventeen flat colored regions with thin borders, the Balearic and Canary islands as small insets", "17 COMUNIDADES"),
         X("stadium_scarves", "A modern football stadium stand with round-white-head cartoon supporters in many different colored scarves and shirts cheering together, no flags, no banners, no logos", MOD),
         X("referendum_2017", "A school gym in Catalonia with round-white-head cartoon people queuing with paper envelopes, a lone police van parked far away outside, no violence, no banners", MOD, band=True),
         X("court_modern", "A modern grey courthouse with steps and round-white-head cartoon lawyers in black robes with files hurrying up the stairs", MOD),
         "map_basque_navarre", "two_buttons", "stadium_scarves", "map_17_regions"]
# FECHO
P[68] = [X("guide_close", f"{GUIA} sitting on a stone wall in the Spanish countryside at golden hour looking at the viewer with a warm smile", CAS),
         X("world_first", "A big ship full of gold chests sailing away while a plain small stone house with a hole in its roof stands neglected on the shore", IBE, "1580"),
         "crown_stitched", "silver_arrives", "kingdoms_squeezed", "two_buttons"]
P[69] = ["papal_license", "polling_1978", "king_stack"]
P[70] = [X("needle_thread", "A big needle with thick thread resting on a worn cloth map of Iberia, soft light, nobody in the picture", IBE, band=False),
         "crown_stitched", "guide_close", "two_buttons"]
# __PLANOS__ (escritos acima)


# ───────────────────────── HOOK (o noivo disfarçado, 1469) ─────────────────────────
cap("Hook")
b("[curious] Castela, outubro de mil quatrocentos e sessenta e nove. Imagine que você é um príncipe de dezessete anos, viajando à noite disfarçado de criado.", card="1469")
b("Você é Fernando, herdeiro de Aragão, e vai casar escondido com Isabel, herdeira de Castela. Com uma licença do papa falsa, assinada por um papa morto havia cinco anos.")
b("O casamento junta duas coroas. Mas não junta dois países: cada lado fica com a sua lei, a sua alfândega, a sua moeda. E esse país pela metade logo ganha um mundo inteiro.")
b("[serious] Então fica a pergunta: por que a Espanha juntou meio mundo antes de conseguir juntar a si mesma?")
b("Porque, por séculos, o rei foi rei das Espanhas, no plural: uma pilha de coroas numa cabeça só. E a última alfândega de dentro só caiu em mil oitocentos e quarenta e um.")
b("Essa é a história inteira da Espanha. Guarde esse plural. E tudo começa numa península que nunca teve um dono só.")

# ───────────────────────── 1. A COSTURA POR CIMA ─────────────────────────
cap("1. A costura por cima")
b("§ Toledo, ano quinhentos e oitenta e nove. Recaredo, rei dos visigodos, reúne os bispos e diz: daqui em diante, uma fé só. Ele troca a sua pela dos súditos.", card="589")
b("Faz sentido, porque os visigodos eram poucos: uma minoria mandando em milhões de hispano-romanos, que falavam latim desde Roma. Rezar igual era o jeito de virar um povo.")
b("Só que toda costura por cima deixa alguém de fora. Nas décadas seguintes, reis de Toledo forçam judeus ao batismo. Imagine viver num reino que quer você igual, ou fora.")
b("§ Mas essa costura não aguenta o primeiro puxão. Em setecentos e onze, um exército do norte da África atravessa o estreito, e o reino visigodo cai em poucos anos.", card="711")
b("Quase toda a península vira al-Andalus. Se você olhar o mapa, aos cristãos sobra uma faixa de montanhas no norte.")
b("O problema é que, nessa faixa, ninguém vai ser dono de tudo. Vão ser vários donos. E cada um com filhos.")

# ───────────────────────── 2. A HERANÇA QUE SE PARTE ─────────────────────────
cap("2. A herança que se parte")
b("§ Leão, dezembro de mil e sessenta e cinco. Fernando Primeiro, o rei mais poderoso do norte cristão, está no fim da vida. Então faz o que todo pai rico fazia: divide a herança.", card="1065")
b("Castela para um filho, Leão para outro, a Galícia para o terceiro. Em poucos anos, os irmãos estão em guerra.")
b("Pense numa família que herda um terreno e, em vez de uma casa, levanta três muros. Era assim, porque o reino era patrimônio, e patrimônio se repartia.")
b("§ Aí cada geração junta e reparte de novo. Leão e Castela se separam em mil cento e cinquenta e sete e só voltam a se unir em mil duzentos e trinta. Portugal, nesse meio-tempo, vai embora de vez.", card="1157")
b("Enquanto a guerra contra al-Andalus desce para o sul, sobram quatro coroas cristãs, Portugal, Castela, Aragão e Navarra, e Granada, muçulmana. Mas sobra também o hábito: tudo o que se junta pode se partir no próximo enterro.")

# ───────────────────────── 3. DOIS NOIVOS, DOIS PAÍSES ─────────────────────────
cap("3. Dois noivos, dois países")
b("§ Estrada de Castela para Saragoça, mil quatrocentos e oitenta. Imagine que você é um mercador de lã. Na fronteira, uma alfândega: você para, abre os fardos e paga.", card="1480")
b("Até aí, normal. Só que, desde mil quatrocentos e setenta e nove, os dois lados têm os mesmos reis: Isabel e Fernando, o casal do casamento escondido. E mesmo assim você paga para passar de um reino deles para o outro.")
b("E, depois da cancela, muda o dinheiro. Em Castela se conta em maravedis; em Barcelona, em libras e soldos. Cem mil maravedis valiam seis mil e quatrocentos soldos. Tente pagar um pastel assim.")
b("§ Acontece que o casamento uniu pessoas, não leis. Cada reino ficou com as suas Cortes, os seus tribunais, os seus impostos. Em Castela, a dona da coroa era Isabel. Em Aragão, era Fernando.")
b("Os historiadores chamam isso de monarquia composta: vários países, cada um com o seu contrato. Funcionava, mas só enquanto ninguém pedisse demais.")
b("Então, em mil quatrocentos e noventa e dois, esse arranjo ganha um pedaço novo, do outro lado do Atlântico. O problema: de quem ele é?")

# ───────────────────────── 4. O MUNDO É DE CASTELA ─────────────────────────
cap("4. O mundo é de Castela")
b("§ Sevilha, janeiro de mil quinhentos e três. Os reis criam a Casa de Contratação: todo navio para as Índias sai dali e volta para ali, registrado, pesado e taxado.", card="1503")
b("Se você já mandou uma encomenda para fora, sabe que tudo passa por um balcão. A América inteira passava por um só, em Castela.")
b("Porque as terras que Colombo achou foram incorporadas à coroa de Castela, não à de Aragão. Para quem era de Barcelona, chegar à América era, na prática, bem mais difícil.")
b("Repare no calendário: no ano de Colombo, Castela também toma Granada, o último reino muçulmano da península. Um ano, dois troféus, e nenhum é da Espanha.")
b("§ Mas, em mil quinhentos e quatro, Isabel morre, e Castela vai para a filha, Joana. Fernando, viúvo, casa de novo, com uma princesa francesa, Germana de Foix.", card="1509")
b("Em três de maio de mil quinhentos e nove, nasce um menino. Se ele vivesse, herdaria Aragão, e as duas coroas provavelmente se separariam de novo. O bebê vive poucas horas.")
b("Aqui está a primeira peça da resposta: a Espanha não nasceu de um plano. Nasceu de um casamento, de uma herança e de um acaso. Só que o acaso entregou tudo a um rapaz que mal falava castelhano.")

# ───────────────────────── 5. O REI DE UMA LISTA ─────────────────────────
cap("5. O rei de uma lista")
b("§ Astúrias, setembro de mil quinhentos e dezessete. Uma frota desviada pela tempestade despeja, numa vila de pescadores, um rapaz criado em Flandres. Conta-se que os moradores, assustados com tanta vela, acharam que era um ataque.", card="1517")
b("É Carlos, neto de Isabel e Fernando, o novo rei. Ou melhor, os novos reis: de Castela, de Aragão, de Navarra, de Nápoles, das Índias.")
b("Imagine assinar o seu nome e precisar de uma linha inteira só para os títulos. As moedas do filho dele, Filipe Segundo, resumem em latim: rei das Espanhas.")
b("§ E quem pagava tudo isso? Castela. A prata da América entrava por Sevilha, os impostos castelhanos subiam, e as guerras na Europa engoliam os dois. Os outros reinos davam pouco.")
b("Era o império que ainda não era um país: o rei mandava do México às Filipinas, mas, para cobrar imposto em Saragoça, você imagina: precisava negociar.")
b("§ Em mil quinhentos e noventa e um, Filipe testa o limite. O ex-secretário Antonio Pérez foge para Aragão e se protege atrás do foro aragonês. Aí o rei manda um exército, e o Justiça de Aragão, o juiz que defendia os foros, é executado.", card="1591")
b("Mas Filipe não apaga os foros, só os aperta. O problema fica para o neto, e o neto tinha um ministro com um plano.")

# ───────────────────────── 6. A CONTA ─────────────────────────
cap("6. A conta")
b("§ Madri, Natal de mil seiscentos e vinte e quatro. Enquanto a corte festeja, o conde-duque de Olivares, ministro de Filipe Quarto, entrega um memorial secreto.", card="1624")
b("Olivares escreveu ao rei, sem rodeio: o negócio mais importante da sua monarquia é fazer-se rei da Espanha. Ou seja, reduzir os outros reinos ao estilo e às leis de Castela.")
b("Faz sentido para quem paga a conta, porque Castela estava exausta. Então, em mil seiscentos e vinte e seis, vem a União de Armas: cada reino manda soldados. Castela, quarenta e quatro mil. Catalunha e Portugal, que tinha o mesmo rei desde mil quinhentos e oitenta, dezesseis mil cada.")
b("Pense no seu condomínio, com o síndico decidindo sozinho a cota de cada apartamento. A Catalunha recusa.")
b("§ Em junho de mil seiscentos e quarenta, com soldados aquartelados nas casas, os ceifeiros que chegam a Barcelona se revoltam, e o vice-rei não sai vivo da fuga. Em dezembro, Portugal aclama um rei próprio.", card="1640")
b("Em janeiro seguinte, a Catalunha se põe sob o rei da França. Madri leva doze anos para retomar Barcelona e, em mil seiscentos e cinquenta e nove, entrega o Rossilhão aos franceses. Portugal não volta.")
b("Aqui está a segunda peça da resposta: quando o dinheiro apertou, Madri tentou costurar à força, e a costura arrebentou dos dois lados. Lembra da nossa pergunta? Ela acabou de ficar mais difícil.")
b("Só que a costura à força ia voltar. Desta vez, com uma guerra europeia inteira por trás.")

# ───────────────────────── 7. DIREITO DE CONQUISTA ─────────────────────────
cap("7. Direito de conquista")
b("§ Madri, vinte e nove de junho de mil setecentos e sete. Filipe Quinto, o primeiro rei Bourbon, assina um decreto que acaba com as leis de Aragão e de Valência. E o motivo vem escrito: o justo direito de conquista.", card="1707")
b("Como se chega aí? O último Habsburgo morreu sem filhos. Castela apoiou o neto do rei da França; boa parte de Aragão, um arquiduque austríaco. Aragão perdeu a guerra, então pagou com as leis.")
b("§ Barcelona resiste até onze de setembro de mil setecentos e catorze, data lembrada até hoje. Em mil setecentos e dezesseis, acabam as instituições catalãs, e o castelhano entra no tribunal.", card="1714")
b("E, em mil setecentos e dezessete, as alfândegas entre Castela e Aragão vão para a costa. Se você fosse aquele mercador de lã, agora passaria sem parar. Só levou duzentos e trinta e oito anos de fila.")
b("Mas repare em quem ficou fora da conquista: o País Basco e Navarra. Tinham apoiado Filipe, então não havia o que conquistar, e mantiveram foros, alfândegas e impostos próprios. O problema: a costura à força deixou, de propósito, dois botões soltos.")

# ───────────────────────── 8. OS ESPANHÓIS DOS DOIS HEMISFÉRIOS ─────────────────────────
cap("8. Os espanhóis dos dois hemisférios")
b("§ Cádis, março de mil oitocentos e doze. Napoleão pôs o irmão no trono em Madri, e a cidade está cercada. Lá dentro, deputados escrevem uma constituição.", card="1812")
b("O artigo primeiro é a costura mais ambiciosa de todas: a nação espanhola é a reunião de todos os espanhóis de ambos os hemisférios. Imagine: Madri, Lima, México e Manila, um país só.")
b("Só que a conta tinha um truque. O número de deputados vinha da população, mas quem tinha origem africana ficava fora da conta. Na América, era muita gente, então os americanos ficavam em minoria no país que dizia ser deles também.")
b("Imagine ser chamado de cidadão por uma lei que não conta os seus vizinhos.")
b("§ E a costura não pega. Fernando Sétimo volta ao trono, em mil oitocentos e catorze, e anula a constituição. Do outro lado do mar, as guerras de independência já corriam. Em mil oitocentos e vinte e quatro, em Ayacucho, cai o último grande exército espanhol da América do Sul.", card="1824")
b("Aqui está a terceira peça da resposta: toda vez que tentava costurar, a Espanha decidia antes quem contava. E quem não contava ia embora. O problema é que, dentro de casa, ainda havia dois botões soltos.")

# ───────────────────────── 9. O IMPOSTO QUE FICA EM BILBAO ─────────────────────────
cap("9. O imposto que fica em Bilbao")
b("§ Rio Ebro, mil oitocentos e quarenta. Entre Castela e Navarra, um fiscal ainda abre carroças e cobra. É a última alfândega da Espanha contra a própria Espanha.", card="1840")
b("Ela só cai em mil oitocentos e quarenta e um, depois de uma guerra civil em que muita gente de Navarra e do País Basco lutou por um pretendente que prometia os foros. Aí a alfândega vai para os Pireneus e para a costa.")
b("Mas o principal fica. Depois de outra guerra carlista, uma lei de mil oitocentos e setenta e seis acaba com as isenções bascas. Aí, dois anos depois, Madri faz um acordo: as províncias bascas recolhem os próprios impostos e repassam uma cota ao Estado.", card="1876")
b("Esse acordo existe até hoje. Se você mora em Bilbao, o seu imposto de renda não vai para Madri: vai para a sua província, que depois paga a cota. Navarra tem um igual.")
b("§ Então, em mil oitocentos e noventa e oito, a Espanha perde Cuba, Porto Rico e as Filipinas para os Estados Unidos. O que sobrava do mundo inteiro vai embora num ano.", card="1898")
b("O choque acelera o que já vinha: três anos antes, Sabino Arana tinha fundado um partido nacionalista basco, e na Catalunha o catalanismo vira força eleitoral. Se o império já não junta, por que continuar costurado? O problema agora era político, e ia dividir o país ao meio.")

# ───────────────────────── 10. UMA À FORÇA, UMA ASSINADA ─────────────────────────
cap("10. Uma à força, uma assinada")
b("§ Barcelona, catorze de abril de mil novecentos e trinta e um. Da sacada da prefeitura, Francesc Macià proclama a República Catalã. Ela dura três dias: depois de negociar com Madri, vira um governo autônomo, e o País Basco ganha o seu em plena guerra civil.", card="1931")
b("Mas a guerra termina em trinta e nove com Francisco Franco no poder, e a costura volta a ser à força: o lema é uma, grande e livre; os estatutos acabam, e as outras línguas saem da vida pública. São quase quarenta anos.", card="1939")
b("§ Então, quando Franco sai de cena, em setenta e cinco, a Espanha tenta outra coisa: uma costura assinada. A Constituição de setenta e oito fala, na mesma frase, da indissolúvel unidade da nação espanhola e da autonomia das nacionalidades e regiões.", card="1978")
b("Oitenta e sete por cento dos votantes disseram sim. E o título do rei, no artigo cinquenta e seis, fica no singular: rei da Espanha.")
b("Hoje são dezessete comunidades autônomas. Se você já viu bandeiras diferentes na mesma arquibancada na Espanha, viu essa história. E a costura segue sendo testada: em dois mil e dezessete, um referendo na Catalunha, suspenso pela Justiça, terminou com Madri assumindo o governo catalão por alguns meses. O problema mudou de forma, mas não de lugar.")

# ───────────────────────── FECHO ─────────────────────────
cap("Fecho")
b("§ [warm] Então, por que a Espanha juntou meio mundo antes de juntar a si mesma? Porque o mundo veio primeiro e pagou a conta: o rei não precisava costurar a casa. Quando faltou dinheiro, costurou à força, e cada ponto deixou alguém de fora.")
b("Começou com uma licença falsa e chegou a um papel votado por milhões: do rei das Espanhas ao rei da Espanha.")
b("Talvez a pergunta não seja por que ela rasga, mas por que nunca parou de negociar a costura. E você, o que acha? Conta nos comentários.")

FALA = [("Valladolid", "Valhadolíd"), ("Germana de Foix", "Germana de Fuá"), ("Recaredo", "Recarêdo"), ("Saragoça", "Saragóça"),
        ("Antonio Pérez", "Antônio Pérez"), ("Olivares", "Olivares"), ("Rossilhão", "Rossilhão"), ("Ayacucho", "Aiacútcho"),
        ("Bilbao", "Bilbáo"), ("Sabino Arana", "Sabíno Arâna"), ("Francesc Macià", "Francésc Maciá"), ("Bourbon", "Burbôn"),
        ("Habsburgo", "Rábsburgo"), ("al-Andalus", "al-Ândalus"), ("Flandres", "Flândres"), ("Ebro", "Ébro"), ("Cádis", "Cádis")]
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
