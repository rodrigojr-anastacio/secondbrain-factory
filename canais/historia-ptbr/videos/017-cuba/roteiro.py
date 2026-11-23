#!/usr/bin/env python3
"""Fonte única do 017-cuba (22/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

14º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
7º com ÂNGULO próprio (ANGULO.md): "quem compra, manda" — uma ilha de um produto só precisa de preço garantido; cada comprador
(a Coroa em 1717, os EUA em 1891/1902/1934, a URSS em 1960/1964/1972, a Venezuela em 2000) garantiu o preço cobrando uma cláusula,
e cada cláusula empurrou Cuba para o próximo comprador. Resposta NÃO é a "mesada" do Riqueza e Ruína nem o fecho com Martí do HistoDarias.
EMBALAGEM.md aprovada no crivo r3:
  A/T1 "Cuba adoçava o MUNDO. Por que dependia de um país só?" + thumb rosto-emocao (guajiro em pânico sobre sacos, "SEM COMPRADOR")
  B/T2 "Por que Cuba só trocava de COMPRADOR? E o que cobravam?" + thumb numero-estatistica ("5× O PREÇO")
  C/T3 "Cuba: como o AÇÚCAR decidiu quem mandava na ilha" + thumb mapa-lugar (ilha amarrada por corda, sem texto)
Hook: julho de 1960, 700 mil t sem comprador (≤ 0:20) → Moscou compra as mesmas 3 dias depois (≤ 0:30) → "quase cinco vezes o preço"
  + "cada um cobrou outra coisa" + Espanha/EUA/URSS/Venezuela (≤ 0:45) → PERGUNTA CENTRAL (≤ 0:50) → "essa é a história inteira".
Peças da resposta: 1 (cap. 8) o comprador que paga bem pede que você continue vendendo o mesmo; 2 (cap. 9) quanto melhor o preço,
  mais caro sair. Fecho: só um gigante garante preço; cada garantia veio com uma cláusula; Cuba escolhia de quem depender.
"Guarde" único: as 700 mil toneladas → pagas no cap. 7 (trocam de mão em 72 h) e no fecho (mudaram de cláusula).
Neutralidade: Fidel, Batista, Baía dos Porcos, mísseis, embargo, 2026 em fatos dos dois lados, sem adjetivo.

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1960") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006–016).
Imagens: Codex (canal.yaml visual.gerador: codex; fallback nano-banana). Prompts só de conteúdo; o estilo vem do canal.yaml.
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (006–016: ~128–130 ppm com pausas)
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
TITULO = "A história INTEIRA de Cuba"
PERGUNTA = "Por que Cuba sempre dependeu de um país só para comprar o que ela produz?"
PROMESSA = ("Por que Cuba sempre dependeu de um país só para comprar o que ela produz, e o que cada comprador cobrou por isso: "
            "as 700 mil toneladas de 1960 que trocam de mão em 3 dias, o preço de quase cinco vezes o mercado, a Coroa, os EUA, "
            "a URSS e a Venezuela (EMBALAGEM.md r3).")
TITULOS = ('T1 "Cuba adoçava o MUNDO. Por que dependia de um país só?" / T2 "Por que Cuba só trocava de COMPRADOR? E o que cobravam?" / '
           'T3 "Cuba: como o AÇÚCAR decidiu quem mandava na ilha"')

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
# As refs de estilo vêm do Egito e vazam conteúdo (visual.md 010/011/013/014/016): TODA cena leva o cenário ancorado (CUB/HAV/WAS/MOS…)
# + SEMTXT; cena com gente, navio ou praça leva SEMBAND (nada de bandeira: nem a cubana antes de 1902, nem a americana, nem a soviética).
# Palmeira: só a palma real cubana (tronco reto cinza) quando o cenário é Cuba; nunca tamareira/deserto. Morte e guerra só sugeridas (GUERRA).
MAPA = ("painted like a blank parchment terrain map seen from directly above, only coastlines, seas, islands and flat colored areas, "
        "completely blank with no writing anywhere, no letters, no words, no labels, no symbols, no compass, no border, no frame, no flags, no people")
SEMTXT = ", no readable writing, no letters anywhere, no numbers, no signs, no boards, no logos"
SEMBAND = ", no flags of any kind, no banners, no pennants, no coats of arms, no emblems, no red stars, no hammer and sickle"
GUERRA = ", no blood, no wounds, no bodies, no weapons fired, no violence shown"
NAO_EG = ", NO pyramids, NO pharaoh headdress, NO turbans, NO desert dunes, NO camels, NO date palms, NO crowns"
CUB = ", strictly Cuba in the Caribbean: green rolling hills, tall Cuban royal palms with straight smooth grey trunks, sugarcane fields, red earth, humid blue sky" + NAO_EG
ORI = ", strictly eastern Cuba around 1600: a small colonial village of wooden houses with palm-thatched roofs, a modest stone church, cattle pastures, green mountains behind" + NAO_EG
HAV = ", strictly colonial Havana: low pastel stone houses with red tile roofs and wooden balconies, a narrow harbor bay guarded by the stone Morro castle" + NAO_EG
HAV20 = ", strictly 20th-century Havana: pastel neoclassical buildings with columns and arcades, a seafront wall along the sea, old American cars" + NAO_EG
ING = ", strictly a Cuban sugar mill (ingenio/central): tall brick chimney, wooden cane carts pulled by oxen, a boiling house, green cane fields around" + NAO_EG
WAS = ", strictly Washington D.C.: white neoclassical government buildings with columns and a dome, wide avenues, leafy trees, NO skyscrapers, NO Big Ben" + NAO_EG
NYB = ", strictly a 19th-century American port city (Boston/New York): red-brick warehouses, wooden wharves, tall-masted ships" + NAO_EG
MAD = ", strictly 18th-century Madrid: red-brick and pale stone palace halls, tall windows, dry clear light" + NAO_EG
MOS = ", strictly Moscow in the Soviet era: wide grey avenues, massive grey Stalin-era buildings, onion domes far away, snow on the ground" + NAO_EG
CAR = ", strictly Caracas, Venezuela: the green Ávila mountain behind, modern 2000s concrete buildings, red-roofed hillside houses" + NAO_EG
MOD = ", ordinary modern everyday setting of today" + NAO_EG + ", NO safari helmet"
SEA = ", open Caribbean sea, turquoise water" + NAO_EG
def ANO(a): return f", period-accurate {a}: clothes, buildings, ships, cars and objects of that time only, no modern objects"
PAPEL = ", the document is drawn as plain wavy lines, completely illegible, no letters, no words"
def X(k, d, cen="", ano=None, band=True, guerra=False, papel=False, rot=None):
    return (f"{k}|{d}{cen}" + (ANO(ano) if ano else "") + (PAPEL if papel else "") + SEMTXT + (SEMBAND if band else "")
            + (GUERRA if guerra else "") + (f"@@{rot}" if rot else ""))
def M(k, d, rot=None): return f"{k}|{d}, " + MAPA + (f"@@{rot}" if rot else "")
# Personagens (bíblia: rosto nunca descrito; "round-white-head cartoon …"; nome de figura moderna só no rótulo do código)
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes, wearing an ordinary brown felt hat and a plain brown jacket"
DONO = "a round-white-head cartoon Cuban warehouse owner of 1960 with a thin mustache shape, a white guayabera shirt and a straw hat"
PIR = "a round-white-head cartoon French pirate captain of 1604 with a wide plain dark hat, a long brown coat and high boots"
BISPO = "a round-white-head cartoon Spanish bishop of 1604 in a plain purple robe and a simple white mitre"
VIZ = "round-white-head cartoon villagers of 1604 eastern Cuba in plain linen shirts and straw hats"
VEG = "round-white-head cartoon tobacco farmers of 1717 in loose white shirts and straw hats"
REI = "a round-white-head cartoon Spanish king of 1717 with a long curly dark wig and a blue coat with gold trim"
ESCR = "a round-white-head cartoon colonial clerk of 1717 in a dark coat with a quill"
CAPT = "a round-white-head cartoon American sea captain of 1805 in a blue coat and a round hat"
ATK = "a round-white-head cartoon Boston sugar merchant of the 1880s with grey side-whiskers shape, a dark frock coat and a top hat"
MARTI = "a round-white-head cartoon slim man of 1891 with a big dark mustache shape, a black suit and a black bow tie"
DIPL = "round-white-head cartoon diplomats of 1891 in dark frock coats around a long table"
CONG = "round-white-head cartoon American congressmen of the 1890s in dark suits"
ROOS = "a round-white-head cartoon American president of 1934 with small round glasses shape, a dark suit, seated at a big desk"
EISEN = "a round-white-head cartoon bald American president of 1960 in a grey suit, seated at a desk"
KHRU = "a round-white-head cartoon bald stout Soviet leader of 1960 in a grey suit"
MIKO = "a round-white-head cartoon Soviet official of 1960 with a small dark mustache shape, a dark overcoat and a hat"
FID = "a round-white-head cartoon bearded revolutionary leader in an olive-green uniform and an olive cap"
CHAV = "a round-white-head cartoon Venezuelan president of 2000 with short dark hair in a dark suit and a red tie"
CIA = "round-white-head cartoon government analysts of the early 1980s in shirt sleeves and ties, with desk calculators and paper charts"
CANE = "round-white-head cartoon Cuban sugarcane cutters in straw hats and work clothes"

P = {}
# HOOK (1960)
P[1] = [X("havana_port_1960", "Havana harbor in 1960 seen from the water, the stone Morro castle at the entrance, cargo ships at the quay, warm morning light", HAV20, "1960"),
        X("warehouse_sacks", f"{DONO} standing proudly inside a huge warehouse stacked to the ceiling with burlap sugar sacks", HAV20, "1960"),
        X("sacks_closeup", "Close view of stacked burlap sugar sacks in a warehouse, a few grains of white sugar spilling from one corner, nobody in the picture", HAV20, "1960", band=False),
        X("ship_loading_us", "Dock workers carrying sugar sacks up a gangway into a big grey cargo ship, cranes overhead", HAV20, "1960"),
        X("guide_imagine", f"{GUIA} sitting on a sugar sack on a Havana quay, waving at the viewer", HAV20, "1960")]
P[2] = [X("eisen_signs", f"{EISEN} signing a paper at a desk in a white government office, pen in hand, serious", WAS, "1960", papel=True, rot="EISENHOWER"),
        X("dono_shock", f"{DONO} in the doorway of his full sugar warehouse holding a telegram, mouth open in shock", HAV20, "1960", papel=True),
        X("ship_leaves_empty", "A big empty cargo ship leaving Havana harbor without cargo, the dock behind it piled with unsold sugar sacks", HAV20, "1960"),
        X("khru_telegram", f"{KHRU} dictating a message to a secretary at a typewriter in a grand Moscow office, one finger raised", MOS, "1960", papel=True, rot="KHRUSHCHEV"),
        X("sacks_new_ship", "Dock workers in Havana carrying the same sugar sacks toward a different cargo ship with a dark red hull", HAV20, "1960")]
P[3] = [X("scale_price", "An old merchant's balance scale with one small sugar sack on one plate outweighing a big pile of gold coins on the other, nobody in the picture", band=False),
        X("hand_paper_string", "A hand offering a bag of coins while the other hand pulls back a long contract paper with a string tied to it, plain background", papel=True, band=False),
        X("spain_buyer", "A round-white-head cartoon Spanish royal official of the 1700s in a wig weighing tobacco leaves on a scale at a colonial Havana warehouse", HAV, "1720"),
        X("us_buyer", "A round-white-head cartoon American businessman of 1910 in a straw boater hat counting sugar sacks on a Havana dock with a notebook", HAV20, "1910"),
        X("soviet_buyer", "A round-white-head cartoon Soviet trade official of 1970 in a grey coat and fur hat inspecting sugar sacks on a snowy dock", MOS, "1970"),
        X("venezuela_buyer", "A round-white-head cartoon Venezuelan official of 2000 in a light suit shaking hands next to oil barrels on a sunny Caribbean pier", CAR, "2000")]
P[4] = [X("guide_question", f"{GUIA} standing on the Havana seafront wall at sunset with a puzzled hand on his chin, looking out to sea", HAV20),
        M("map_cuba_caribbean", "Map of the Caribbean with the long island of Cuba in the center lit in warm gold, Florida just to the north, the sea around in pale blue"),
        X("one_door", "A single heavy wooden door at the end of a long empty colonial corridor, warm light under it, nobody in the picture", HAV, band=False),
        X("cuba_tied_rope", "Aerial cartoon view of the long island of Cuba lying across a calm blue sea, green with cane fields and smoking mill chimneys, a thick rope looped around its middle rising straight up out of the picture", SEA, band=False)]
P[5] = [X("island_aerial", "Wide aerial view of the green Cuban coastline with long white beaches, mangroves and mountains in the distance", CUB, band=False),
        X("sacks_count", "Rows and rows of sugar sacks stacked on a long quay stretching into the distance, nobody in the picture", HAV20, "1960", band=False),
        X("spanish_ships_arrive", "Three small Spanish sailing ships of 1492 with plain cream sails anchored off a green Cuban coast with royal palms", SEA, "1492"),
        X("gold_pan_empty", "A round-white-head cartoon Spanish conquistador in a plain metal helmet kneeling in a river, looking disappointed at an empty pan", CUB, "1515"),
        X("taino_village", "A Taíno village of round thatched huts (bohíos) in a clearing among royal palms, round-white-head cartoon people with straight black hair, simple cotton clothes, drawn with dignity, no caricature", CUB, "1492")]
# 1. A ILHA QUE FICOU SEM OURO
P[6] = [X("bayamo_1604", "A small colonial village of wooden houses with palm-thatched roofs and a modest stone church by a river in eastern Cuba", ORI, "1604", band=False),
        X("pirate_ship_coast", "A French pirate sailing ship with plain grey sails anchored in a quiet river mouth among mangroves", ORI, "1604"),
        X("bishop_farm", f"{BISPO} visiting a cattle farm, chatting with a farmer under a palm-thatched porch", ORI, "1604"),
        X("pirate_takes_bishop", f"{PIR} leading {BISPO} away by the arm toward a rowboat, the bishop looking indignant, no weapons drawn", ORI, "1604", rot="GILBERTO GIRÓN"),
        X("ransom_note", "Close view of a folded ransom letter with a wax seal on a rough wooden table, a candle beside it", ORI, "1604", papel=True, band=False)]
P[7] = [X("villagers_shrug", f"{VIZ} on the riverbank watching a foreign ship calmly, one of them shrugging", ORI, "1604"),
        X("hides_trade", "Round-white-head cartoon villagers loading stacks of dried cattle hides into a rowboat while foreign sailors hand over cloth and tools", ORI, "1604"),
        X("hides_stack", "A big stack of dried cattle hides under a palm-thatched shed, nobody in the picture", ORI, "1604", band=False),
        X("night_smuggle", "A small boat sliding silently at night toward a foreign ship anchored offshore, a lantern covered with a hand", ORI, "1604"),
        X("royal_decree_cuba", "A royal Spanish decree with a big red wax seal unrolled on a table in a colonial office, a quill beside it", HAV, "1600", papel=True, band=False),
        X("spanish_galleon", "A single large Spanish galleon with cream sails and a high stern sailing toward a Spanish port", SEA, "1600"),
        X("guide_repare", f"{GUIA} peeking from behind a palm-thatched house, pointing at a foreign ship, finger on lips", ORI)]
P[8] = [X("empty_east_coast", "An empty bay on the east coast of Cuba with no ships at all, only waves and mangroves", ORI, "1604", band=False),
        X("rotting_hides", "Round-white-head cartoon farmer holding his nose next to a pile of hides going bad under the sun", ORI, "1604"),
        X("deal_beach", "A round-white-head cartoon villager and a foreign sailor shaking hands on a beach next to a pile of hides", ORI, "1604"),
        X("coins_hand", "Close view of silver coins of mixed foreign origin dropping into a rough farmer's palm", ORI, "1604", band=False)]
P[9] = [X("ransom_paid", f"{VIZ} carrying baskets of food, hides and coins to the pirates on a beach", ORI, "1604"),
        X("ambush_jungle", f"{VIZ} hiding behind trees and tall grass watching the pirate camp, tense, no weapons fired", ORI, "1604", guerra=True),
        X("bishop_free", f"{BISPO} walking back into the village, welcomed by happy {VIZ}", ORI, "1604"),
        X("poet_writing", "A round-white-head cartoon colonial clerk of 1608 in a dark coat writing a long poem by candlelight at a wooden desk", ORI, "1608", papel=True),
        X("poem_book", "An old leather book open on a desk with long columns of plain wavy lines and a feather quill, nobody in the picture", ORI, "1608", papel=True, band=False),
        X("guide_book", f"{GUIA} holding up an old book with a proud smile and a raised eyebrow", ORI)]
P[10] = [X("gold_river_dry", "A dry riverbed in the Cuban hills with abandoned wooden sluices and pans, nobody in the picture", CUB, "1540", band=False),
         X("taino_dignity", "Round-white-head cartoon Taíno people with straight black hair walking away into the forest at dusk, sad but dignified, simple cotton clothes, no caricature", CUB, "1530", guerra=True),
         X("empty_bohio", "An empty round thatched hut in a forest clearing, a woven basket left at the door, quiet light", CUB, "1540", band=False),
         X("havana_fleet_bay", "Many Spanish sailing ships anchored in the narrow bay of colonial Havana under the stone Morro castle", HAV, "1600"),
         X("gold_chest_ship", "Sailors loading heavy wooden chests onto a galleon at a stone quay in Havana", HAV, "1600")]
P[11] = [X("spanish_official_think", "A round-white-head cartoon Spanish official of 1700 in a wig sitting at a desk in Madrid, chin on hand, looking at a map of Cuba", MAD, "1700"),
         X("tobacco_leaf_light", "A single big green tobacco leaf glowing in a beam of light on a wooden table, nobody in the picture", band=False),
         X("tobacco_field", "A green tobacco field in western Cuba with a palm-thatched drying barn and red earth", CUB, "1710", band=False)]
# 2. O COMPRADOR POR DECRETO
P[12] = [X("jesus_monte_1717", f"{VEG} gathering angrily in a dusty village square with a small stone church outside Havana, fists raised, no weapons raised", CUB, "1717", rot="JESÚS DEL MONTE"),
         X("vegueros_march", f"{VEG} marching along a red dirt road between tobacco fields toward the walls of Havana", CUB, "1717"),
         X("veguero_face", "A round-white-head cartoon tobacco farmer in a straw hat, angry, holding a bundle of dried tobacco leaves", CUB, "1717"),
         X("madrid_decree", f"{REI} signing a decree at a gilded table in a Madrid palace", MAD, "1717", papel=True, rot="FILIPE V"),
         X("ship_decree", "A Spanish sailing ship entering Havana harbor past the Morro castle", HAV, "1717")]
P[13] = [X("factoria", "A big colonial warehouse in Havana with arches where tobacco bales are weighed, a royal clerk at a desk", HAV, "1720"),
         X("one_buyer_counter", f"{ESCR} behind a single wooden counter with a scale, a long queue of tobacco farmers with bales in front of him", HAV, "1720"),
         X("price_fixed", f"{ESCR} writing a low number on a slate with a smug face, a farmer staring in disbelief", HAV, "1720"),
         X("king_scale", f"{REI} sitting on a huge tobacco bale like a throne, holding a small scale", MAD, "1720"),
         X("bales_seal", "Tobacco bales stamped with a plain red royal seal shape in a warehouse, nobody in the picture", HAV, "1720", band=False)]
P[14] = [X("guide_door", f"{GUIA} knocking at a single small door in a long blank colonial wall, shrugging at the viewer", HAV),
         X("drying_barn", "Inside a tobacco drying barn: rows of leaves hanging from wooden poles, light through the slats", CUB, "1720", band=False),
         X("farmer_harvest", "A round-white-head cartoon tobacco farmer cutting leaves in a field at dawn", CUB, "1720"),
         X("revolt_1723", f"{VEG} uprooting tobacco plants in a field in protest, soldiers watching from a distance, no violence", CUB, "1723", guerra=True),
         "factoria"]
P[15] = [X("company_office", "A colonial merchant company office in Havana with ledgers, a big counter and bales of tobacco, sugar and hides", HAV, "1740"),
         X("company_ship", "A heavy merchant sailing ship loading crates and bales at Havana quay for Spain", HAV, "1740"),
         "one_buyer_counter",
         "madrid_decree"]
P[16] = [X("contract_clause", "Close view of an old contract on parchment with a long thin ribbon tied to its last line, a quill, nobody in the picture", band=False, papel=True),
         X("coast_coves", "A long wild Cuban coastline with many hidden coves and small beaches, a tiny boat in one of them", CUB, "1750", band=False),
         X("smugglers_tobacco", "Round-white-head cartoon smugglers loading tobacco bales into a rowboat in a hidden cove at night", CUB, "1750"),
         X("british_havana", "British warships anchored in Havana bay with redcoat soldiers walking on the quay, locals watching curiously, no fighting", HAV, "1762", guerra=True),
         "factoria", "ship_decree"]
P[17] = [X("war_ships_sea", "Two fleets of sailing warships far apart on a stormy sea, smoke on the horizon, no ships sinking", SEA, "1800", guerra=True),
         "spanish_galleon",
         "coast_coves"]
# 3. SEISCENTOS NAVIOS
P[18] = [X("havana_1805", "Colonial Havana in 1805 seen from the bay, pastel houses, church towers, the Morro castle", HAV, "1805"),
         X("port_opens", "A round-white-head cartoon Spanish official of 1805 opening a big wooden harbor gate with both hands, ships waiting outside", HAV, "1805", rot="1805"),
         X("many_ships_bay", "Dozens of small American merchant sailing ships crowding into Havana bay, masts like a forest", HAV, "1805"),
         X("captain_lands", f"{CAPT} stepping onto the Havana quay with a big smile, sailors unloading barrels behind him", HAV, "1805"),
         X("flour_barrels", "Barrels of flour and bolts of cloth piled on the Havana quay next to sugar boxes, nobody in the picture", HAV, "1805", band=False)]
P[19] = [M("map_florida_cuba", "Map of Florida and Cuba with the narrow strait between them and a thin dotted line of a sea route crossing it", "150 KM"),
         X("molasses_casks", "Round-white-head cartoon dock workers rolling wooden casks of molasses up a plank into an American ship", HAV, "1805"),
         "havana_1805",
         "many_ships_bay"]
P[20] = [X("st_domingue_fire", "Smoke rising over burning sugarcane fields and a sugar mill on a Caribbean island at night, seen from far away, nobody visible", CUB, "1791", band=False, guerra=True),
         X("sugar_price_up", "A round-white-head cartoon European merchant of 1795 staring at a tiny cone of sugar on a scale, surprised", NYB, "1795"),
         X("cane_expands", "New sugarcane fields being planted on cleared hills in Cuba, a new brick chimney rising", ING, "1810"),
         X("enslaved_dignity", "Round-white-head cartoon enslaved Africans cutting sugarcane under a hot sun, drawn with dignity, tired faces, no chains shown, no violence, no caricature", ING, "1820"),
         X("mill_boiling", "Inside a sugar boiling house: big copper kettles steaming, workers stirring with long paddles", ING, "1830"),
         X("sugar_boxes", "Wooden crates of sugar stacked high on an oxcart heading to the port", ING, "1830", band=False)]
P[21] = [X("planter_letter", "A round-white-head cartoon Cuban planter of 1850 in a white suit reading a letter with a ship drawing on it at his veranda", ING, "1850", papel=True),
         X("ships_to_north", "Sugar ships leaving Havana heading north on a calm sea", HAV, "1850")]
P[22] = [X("atkins_office", f"{ATK} at a desk in a Boston counting house with ledgers and a window on tall-masted ships", NYB, "1884", rot="EDWIN ATKINS"),
         X("loan_handshake", f"{ATK} handing a bundle of banknotes to a worried Cuban planter in a white suit", NYB, "1880"),
         X("soledad_mill", "A big Cuban sugar mill with a tall brick chimney among cane fields near the sea at Cienfuegos", ING, "1884", rot="SOLEDAD"),
         X("deed_signed", "Close view of a property deed being signed with a fountain pen, a stack of unpaid bills beside it", papel=True, band=False),
         "ships_to_north"]
P[23] = [X("spanish_governor", "A round-white-head cartoon Spanish governor of 1885 in a white uniform with a sash standing on a Havana palace balcony", HAV, "1885"),
         X("creditor_owner", f"{ATK} standing in front of the sugar mill with keys in his hand, workers looking at him", ING, "1885"),
         "planter_letter",
         "loan_handshake"]
# 4. A BANDEIRA DE UM, O COMPRADOR DE OUTRO
P[24] = [X("conference_1891", f"{DIPL} in a grand hall in Washington, papers on the table, chandeliers", WAS, "1891"),
         X("marti_notes", f"{MARTI} sitting at the long conference table taking notes with a pencil, attentive", WAS, "1891", rot="JOSÉ MARTÍ"),
         X("ny_exile", f"{MARTI} walking in a snowy 1890s New York street with a newspaper under his arm", NYB, "1890"),
         "map_florida_cuba"]
P[25] = [X("marti_writing", f"{MARTI} writing at a small desk by a window at night, lamp lit, focused", NYB, "1891", papel=True),
         "marti_notes",
         X("buyer_seller", "Two round-white-head cartoon figures: one standing tall with arms crossed, the other bowing and holding a basket of goods", band=False),
         "scale_price"]
P[26] = [X("ten_years_war", "Round-white-head cartoon Cuban rebels of 1868 in white clothes and straw hats on horseback in the hills, far away, no fighting", CUB, "1868", guerra=True),
         X("tariff_book", "A thick American law book open on a desk in the Capitol with a sugar cube on top of it", WAS, "1890", papel=True, band=False),
         "marti_notes"]
P[27] = [X("treaty_1891", "Round-white-head cartoon American and Spanish diplomats of 1891 signing a paper at a table in Madrid", MAD, "1891", papel=True),
         X("sugar_record", "Sugar mills working full steam, chimneys smoking, oxcarts lined up with cane, busy and prosperous", ING, "1893"),
         X("congress_vote", f"{CONG} raising their hands in a vote inside the domed Capitol chamber", WAS, "1894"),
         X("tax_stamp", "A big rubber stamp coming down on a sugar crate on an American dock", NYB, "1894", band=False)]
P[28] = [X("mill_stopped", "A silent sugar mill with a cold chimney and empty oxcarts, cane fields uncut", ING, "1895", band=False),
         X("workers_idle", f"{CANE} sitting idle on a fence with machetes on the ground, worried", ING, "1895"),
         "tax_stamp",
         "congress_vote"]
P[29] = [X("war_1895", "Round-white-head cartoon Cuban insurgents of 1895 in white clothes and straw hats riding through tall grass at dawn, far away, no fighting", CUB, "1895", guerra=True),
         X("marti_horse", f"{MARTI} on a white horse in the Cuban countryside, seen from behind, riding toward the hills", CUB, "1895"),
         X("dos_rios", "A quiet river crossing in eastern Cuba with a single white horse standing alone, soft evening light, nobody else", ORI, "1895", band=False, guerra=True),
         X("us_ships_1898", "American steel warships of 1898 painted white sailing in line toward the Cuban coast", SEA, "1898", guerra=True),
         X("spain_leaves", "Spanish soldiers of 1898 in striped uniforms boarding ships to leave Havana, a quiet crowd watching", HAV, "1898"),
         X("pen_handover", "A hand in a Spanish officer's sleeve passing a fountain pen to a hand in an American businessman's sleeve over a map of Cuba", band=False),
         "tariff_book"]
# 5. VINTE POR CENTO
P[30] = [X("havana_1902", "Havana in 1902 with a crowd celebrating in a plaza in front of a colonial palace, hats in the air", HAV, "1902"),
         X("treaty_1902", "Round-white-head cartoon Cuban and American officials of 1902 signing a treaty at a table in a Havana palace", HAV, "1902", papel=True),
         X("discount_20", "A sugar crate on an American customs scale with a big round discount tag hanging from it", NYB, "1903", band=False)]
P[31] = [X("gift_box", "A gift box with a ribbon opened on a table, a second hidden paper attached under the ribbon", papel=True, band=False),
         X("constitution_annex", "A thick bound constitution on a desk with an extra page glued at the end with a red ribbon", HAV, "1901", papel=True, band=False),
         M("map_guantanamo", "Map of eastern Cuba with the deep bay of Guantánamo lit in yellow", "GUANTÁNAMO"),
         "treaty_1902"]
P[32] = [X("two_doors_house", "A colonial Cuban house with a sugar crate entering through the front door and a paper scroll sneaking in through the back door", HAV, "1903", band=False),
         "gift_box",
         "discount_20"]
P[33] = [X("us_buys_mill", "Round-white-head cartoon American businessmen in 1910s suits and boater hats touring a Cuban sugar mill with plans", ING, "1915"),
         "soledad_mill",
         X("big_central", "A giant modern sugar mill of the 1920s with several chimneys and a company town around it", ING, "1924"),
         "atkins_office"]
P[34] = [X("price_chart_up", "A round-white-head cartoon broker of 1920 in a stock exchange room staring at a chalk board line shooting up then crashing down, the board has only lines", NYB, "1920"),
         X("bank_closed", "A closed bank door in Havana with a crowd of worried round-white-head cartoon people in 1920 clothes outside", HAV20, "1920"),
         "deed_signed",
         "big_central"]
# 6. O MESMO MÊS
P[35] = [X("roosevelt_signs", f"{ROOS} signing a bill with a fountain pen, aides standing around", WAS, "1934", papel=True, rot="ROOSEVELT"),
         X("quota_ledger", "A big ledger open on a desk in Washington with columns of plain lines, a ruler and a pencil, sugar cubes beside it", WAS, "1934", papel=True, band=False),
         X("sugar_pie", "Several piles of sugar of different sizes on a long table, each with a blank paper label, an official measuring them with a ruler", WAS, "1934", band=False)]
P[36] = [X("treaty_1934", "Round-white-head cartoon Cuban and American diplomats of 1934 shaking hands over a signed treaty in a Washington office", WAS, "1934", papel=True),
         "constitution_annex",
         X("guantanamo_bay", "A calm deep bay with low dry hills and a small naval station with grey ships", ORI, "1934"),
         "quota_ledger"]
P[37] = [X("same_month_calendar", "A wall calendar of May with two days circled, hanging in a 1930s office, the calendar grid has no numbers and no month name, only empty squares", WAS, "1934", band=False),
         X("mill_owner_camaguey", "A round-white-head cartoon sugar mill owner of 1934 in a white suit reading a newspaper, scratching his head, on a veranda", ING, "1934", rot="CAMAGÜEY"),
         "quota_ledger",
         "roosevelt_signs"]
P[38] = [X("cane_cutters", f"{CANE} cutting tall cane with machetes in a field under a hot sun", ING, "1940"),
         X("number_sky", "A huge blank paper slip floating in the sky over Cuban cane fields like a cloud, farmers looking up", ING, "1940", band=False),
         "workers_idle",
         "quota_ledger"]
P[39] = [X("havana_1950s", "A 1950s Havana street with old American cars, neon-free shop awnings, people in light clothes", HAV20, "1955"),
         X("palace_1952", "Military trucks parked in front of the presidential palace in Havana at dawn, quiet, no fighting", HAV20, "1952", guerra=True, rot="GOLPE DE BATISTA"),
         X("rebels_1959", "Round-white-head cartoon young bearded rebels in olive-green uniforms riding on a jeep into Havana, crowd cheering", HAV20, "1959"),
         X("paper_tear", f"{FID} holding a paper slip about to tear it in two, determined", HAV20, "1959", papel=True)]
# 7. SETECENTAS MIL TONELADAS
P[40] = [X("expo_1960", "A big exhibition hall in Havana with tractors, machines and a model of a satellite on display, crowds of curious visitors in 1960 clothes", HAV20, "1960"),
         X("miko_ribbon", f"{MIKO} cutting a ribbon at the entrance of an exhibition, smiling", HAV20, "1960", rot="MIKOYAN"),
         X("tractor_kids", "Round-white-head cartoon children climbing on a big red tractor at an exhibition, parents laughing", HAV20, "1960")]
P[41] = [X("cooperative_crowd", "A crowd of round-white-head cartoon farmers at a rice cooperative in 1960 shouting with raised arms, cheerful", CUB, "1960"),
         X("miko_repeats", f"{MIKO} raising one hand and repeating to the crowd, amused", CUB, "1960"),
         X("trade_signing", f"{MIKO} and {FID} signing an agreement at a long table, photographers around", HAV20, "1960", papel=True),
         X("million_sacks", "A long line of trucks loaded with sugar sacks heading to the port", CUB, "1960")]
P[42] = [X("guide_harder", f"{GUIA} scratching his head in front of a blackboard with two arrows pointing in opposite directions", HAV20),
         X("land_reform", "Round-white-head cartoon officials in olive uniforms measuring land with a chain in a big cane field, farmers watching", CUB, "1959"),
         X("refinery_1960", "An oil refinery by the sea in Havana with storage tanks and a gate where soldiers in olive uniforms stand, calm", HAV20, "1960"),
         "refinery_1960"]
P[43] = [X("quota_weapon", "A paper slip folded into the shape of a sword lying on a Washington desk", WAS, "1960", band=False),
         X("same_sacks_two_ships", "The same pile of sugar sacks on a Havana quay between two cargo ships, one leaving, one arriving", HAV20, "1960"),
         X("havana_rally_1960", "A huge rally in a Havana plaza in 1960, a speaker on a stage reading a telegram aloud, crowd cheering", HAV20, "1960", papel=True),
         X("clock_72", "An old wall clock with its hands spinning fast in a dockside office, sugar sacks behind", HAV20, "1960", band=False),
         "warehouse_sacks", "eisen_signs", "khru_telegram", "dono_shock"]
P[44] = [X("bay_pigs", "A swampy Cuban beach at dawn with landing boats abandoned in the shallow water, smoke far away, nobody visible", CUB, "1961", guerra=True, rot="BAÍA DOS PORCOS"),
         X("embargo_chain", "A big padlock and chain on a dock gate in front of the sea, cargo cranes standing still", HAV20, "1962", band=False),
         X("missile_crisis", "A tense meeting room in Washington with round-white-head cartoon men in suits looking at aerial photographs of a field, 1962", WAS, "1962", guerra=True),
         X("new_buyer_bill", f"{KHRU} holding out a long bill to {FID}, both seated at a table", MOS, "1962", papel=True),
         "same_sacks_two_ships"]
# 8. SEIS CENTAVOS
P[45] = [X("moscow_1964", "Moscow in winter 1964: Red Square with snow, onion domes and a grey sky, round-white-head cartoon people in fur hats", MOS, "1964"),
         X("fidel_moscow", f"{FID} walking in the snow beside {KHRU}, both waving, in Moscow", MOS, "1964"),
         X("contract_six", "A thick contract on a desk with a fountain pen and six shiny small coins lined up beside it", MOS, "1964", papel=True, band=False),
         X("price_wave", "A wavy line going up and down on graph paper next to a straight flat line, on a desk, nobody in the picture", band=False)]
P[46] = [X("guide_dream", f"{GUIA} lying in a hammock with a contented smile and a thought bubble of neat stacks of coins", CUB),
         "contract_six",
         X("stairs_sacks", "Sugar sacks stacked like a staircase going up, each step higher than the last, nobody in the picture", band=False),
         "contract_six"]
P[47] = [X("volunteers_bus", "Buses full of round-white-head cartoon city volunteers of 1969 in work clothes going to the cane fields, waving", CUB, "1969"),
         X("whole_country_field", "Thousands of round-white-head cartoon people cutting cane across endless fields under a big sky, workers, students and soldiers side by side", CUB, "1970"),
         "volunteers_bus"]
P[48] = [X("harvest_meter", "A giant thermometer-shaped gauge drawn on a wall beside a sugar mill, the level stopping just below the top, workers looking up", ING, "1970"),
         X("mill_full_steam", "A 1970 sugar mill working day and night, lights on, smoke rising, trucks lined up", ING, "1970"),
         X("plaza_speech", f"{FID} speaking at a microphone on a stage before a huge crowd in a Havana plaza, serious", HAV20, "1970"),
         "cane_cutters",
         "whole_country_field", "harvest_meter"]
P[49] = [X("price_tied_qty", "A golden price tag tied with rope to a heavy sugar sack, on a plain background", band=False),
         "cane_expands",
         X("guide_piece1", f"{GUIA} placing a first puzzle piece on a table with a satisfied nod", HAV20),
         "stairs_sacks"]
# 9. QUASE CINCO VEZES O PREÇO
P[50] = [X("cia_room", f"{CIA} in an office with a window on Washington, one of them squinting at a calculator in disbelief", WAS, "1983", rot="CIA"),
         X("calculator_close", "Close view of a 1980s desk calculator next to a sugar cube and a pencil, nobody in the picture", WAS, "1983", band=False),
         X("five_times", "Five gold coins stacked beside a single sugar sack on one side, one gold coin beside an identical sugar sack on the other", band=False),
         "scale_price"]
P[51] = [X("comecon_hall", "A big conference hall in Moscow with delegates of many countries in 1970s suits around a round table", MOS, "1972"),
         X("division_labor", "A conveyor belt where each round-white-head cartoon worker adds one item: a sugar sack, a nickel ingot, a crate of oranges", band=False),
         X("convenio_rubles", "A stack of plain paper banknotes with no writing tied with string, a padlock attached to the string", band=False),
         X("ship_oil_sugar", "A Soviet freighter in Havana unloading oil drums and machines while sugar sacks are loaded on the other side", HAV20, "1980")]
P[52] = [X("guide_paris", f"{GUIA} at a fancy hotel reception desk in Paris offering a small paper coupon, the receptionist raising an eyebrow", MOD),
         "convenio_rubles",
         X("bloc_trains", "Freight wagons full of sugar heading east on a snowy railway", MOS, "1985"),
         "ship_oil_sugar"]
P[53] = [X("guide_piece2", f"{GUIA} placing a second puzzle piece next to the first, looking at the viewer", HAV20),
         "one_door",
         "convenio_rubles", "five_times"]
P[54] = [X("ussr_ends", "A big grey Soviet government building at night in Moscow with its lights switching off one by one, snow falling", MOS, "1991", rot="1991"),
         X("blackout_havana", "A Havana street at night in a blackout, people sitting on doorsteps with candles", HAV20, "1992"),
         X("ration_queue", "A queue of round-white-head cartoon people with ration books outside a small shop in Havana, patient", HAV20, "1993", papel=True),
         "ration_queue",
         X("ship_never_came", "An empty dock in Havana with weeds growing, no ships, gulls flying", HAV20, "1992", band=False)]
P[55] = [X("harvest_half", "A sugar mill with only one chimney smoking and half its cane fields overgrown with weeds", ING, "1993"),
         X("empty_wallet", "An empty wallet open on a kitchen table in a Havana apartment, a cup of coffee beside it", HAV20, "1993", band=False),
         "blackout_havana",
         "ship_never_came"]
# 10. PETRÓLEO POR JALECO
P[56] = [X("caracas_2000", "Caracas in 2000 with the green Ávila mountain behind modern buildings, sunny", CAR, "2000"),
         X("fidel_chavez_sign", f"{FID} and {CHAV} signing an agreement at a table with cameras flashing", CAR, "2000", papel=True, rot="FIDEL CASTRO E HUGO CHÁVEZ"),
         X("tanker_venezuela", "A big oil tanker sailing from a Venezuelan port across the Caribbean", SEA, "2000"),
         X("doctors_board", "Round-white-head cartoon Cuban doctors and teachers in white coats boarding a plane with bags", MOD, "2003")]
P[57] = [X("guide_change", f"{GUIA} holding a sugar cube in one hand and a doctor's stethoscope in the other, comparing them", MOD),
         X("clinic_hills", "A small clinic on a hillside neighborhood of Caracas with a Cuban doctor in a white coat greeting patients", CAR, "2005"),
         X("barrels_line", "Rows of oil barrels lined up on a Havana dock in the sun", HAV20, "2005", band=False)]
P[58] = [X("mill_rusting", "An old sugar mill with a rusting chimney and weeds growing on the rails, cane carts abandoned", ING, "2010", band=False),
         X("sugar_imported", "Sacks of imported sugar being unloaded from a foreign ship in a modern Cuban port", HAV20, "2024"),
         "mill_rusting"]
P[59] = [X("oil_pump_still", "An oil pump jack standing still in a Venezuelan oil field at sunset, nobody around", CAR, "2018", band=False),
         "tanker_venezuela",
         X("tanker_turns", "An oil tanker turning around at sea, away from a Caribbean island on the horizon", SEA, "2026", band=False),
         X("empty_fuel_station", "A modern Havana fuel station with empty pumps and a long line of old cars waiting", HAV20, "2026"),
         "barrels_line"]
P[60] = [X("harvest_tiny", "A tiny pile of sugarcane in front of a huge empty sugar mill yard, one small truck", ING, "2025", band=False),
         X("counter_empty", "A long wooden market counter on a Havana dock with nobody on the other side, a single sugar sack on top", HAV20, "2025", band=False),
         X("night_havana_dark", "Havana at night seen from the sea with most windows dark and only a few lights", HAV20, "2026", band=False),
         "cuba_tied_rope"]
# FECHO
P[61] = [X("guide_close", f"{GUIA} sitting on the Havana seawall at golden hour, looking at the viewer with a calm smile", HAV20),
         X("giants_line", "Four huge shadowy figures standing in a row on the horizon over the sea, each holding the end of the same rope tied to a small island", SEA, band=False),
         "factoria", "discount_20", "quota_ledger", "convenio_rubles", "doctors_board"]
P[62] = [X("fine_print", "Extreme close view of an old contract's last line with a magnifying glass over tiny wavy lines, sugar grains on the paper", papel=True, band=False),
         "same_sacks_two_ships", "sacks_closeup"]
P[63] = [X("guide_wave_end", f"{GUIA} waving goodbye from a small boat in Havana harbor at sunset, the Morro castle behind", HAV20),
         "fine_print", "cuba_tied_rope"]
# __PLANOS__ (escritos acima)


# ───────────────────────── HOOK (as 700 mil toneladas, 1960) ─────────────────────────
cap("Hook")
b("[curious] Havana, julho de mil novecentos e sessenta. Imagine que você tem um armazém no porto, cheio de sacos de açúcar até o teto. Esse açúcar já tem comprador: os Estados Unidos.", card="1960")
b("Aí, no dia seis, Washington corta a cota de Cuba: setecentas mil toneladas ficam sem comprador. Três dias depois, chega um recado: Moscou se oferece para comprar exatamente essas setecentas mil.")
b("E um dia ia pagar quase cinco vezes o preço do mercado. Só que nenhum comprador de Cuba cobrou só em dinheiro. Nem a Espanha, nem os Estados Unidos, nem os soviéticos, nem a Venezuela.")
b("[serious] Então fica a pergunta: por que Cuba sempre dependeu de um país só para comprar o que ela produz?")
b("Essa é a história inteira de Cuba. Guarde essas setecentas mil toneladas: elas voltam. E tudo começa com uma ilha que, para azar de quem chegou, quase não tinha ouro.")

# ───────────────────────── 1. A ILHA QUE FICOU SEM OURO ─────────────────────────
cap("1. A ilha que ficou sem ouro")
b("§ Bayamo, leste de Cuba, mil seiscentos e quatro. Um pirata francês, Gilberto Girón, sequestra o bispo da ilha numa fazenda perto da cidade. E pede resgate.", card="1604")
b("Repare que ninguém em Bayamo estranha um navio francês por ali. A cidade vivia de vender couro a navios estrangeiros. E isso era crime, porque a lei espanhola dizia: Cuba só vende para a Espanha, nos navios da Espanha.")
b("Só que esses navios quase não passavam pelo leste, e couro não espera. Então o povo vendia para quem aparecesse.")
b("Os moradores pagam o resgate e depois emboscam o pirata. Um escrivão escreve um poema sobre o caso, que hoje é tido como a primeira obra da literatura cubana. Tente ganhar fama literária com um sequestro.")
b("§ Era o jeito de uma ilha que tinha ficado sem ouro: o pouco que havia acabou em poucas décadas, junto com a maior parte dos taínos, levados por guerra, trabalho forçado e epidemias.")
b("O problema é que a Espanha não queria só proibir. Queria comprar. E, um século depois, ela acha o produto certo.")

# ───────────────────────── 2. O COMPRADOR POR DECRETO ─────────────────────────
cap("2. O comprador por decreto")
b("§ Arredores de Havana, julho de mil setecentos e dezessete. Plantadores de tabaco, os vegueros, se juntam no povoado de Jesús del Monte. Estão furiosos com uma lei que chegou de Madri.", card="1717")
b("A lei, de abril, cria o estanco do tabaco: daqui em diante, todo o fumo de Cuba só pode ser vendido a um comprador, o rei. Pelo preço que o rei marcar.")
b("Imagine que você planta, colhe, seca as folhas, e só existe uma porta para bater. Os vegueros se levantam em dezessete, de novo em vinte e outra vez em vinte e três. Mas o estanco fica.")
b("§ Então Madri vai além. Em mil setecentos e quarenta, uma companhia de Havana ganha o monopólio do comércio com a Espanha: um único balcão para quase tudo.", card="1740")
b("Mas o comprador único tinha uma cláusula embutida: o preço era sempre o dele. E preço baixo, numa ilha de litoral enorme, vira contrabando. Nem os onze meses de Havana nas mãos dos ingleses, em sessenta e dois, mudam a regra.")
b("O problema é que, a cada guerra da Espanha, a regra afrouxava. E alguém do lado de fora estava esperando.")

# ───────────────────────── 3. O VIZINHO EM CHAMAS ─────────────────────────
cap("3. Seiscentos navios")
b("§ Havana, mil oitocentos e cinco. A Espanha está em guerra com a Inglaterra, e os navios espanhóis não chegam. Então o governo abre os portos de Cuba a navios neutros. Em poucos meses, uns seiscentos navios americanos atracam em Havana.", card="1805")
b("Repare quem chegou primeiro quando a porta abriu: o vizinho do norte, a uns cento e cinquenta quilômetros. Ele traz farinha e tecido, e leva açúcar e melaço.")
b("E chegam na hora certa. Desde a revolução dos escravizados de noventa e um, o açúcar de São Domingos, a colônia francesa que mais produzia no mundo, sumiu do mercado. O preço sobe, e Cuba planta cana como nunca, com centenas de milhares de africanos trazidos à força.")
b("Se você plantasse cana em Cuba em meados do século dezenove, o seu melhor cliente já não falava espanhol. Falava inglês.")
b("§ Só que comprador grande também empresta. Nos anos de mil oitocentos e oitenta, Edwin Atkins, um comerciante de açúcar de Boston, fica com a usina Soledad, perto de Cienfuegos, para acertar uma dívida antiga.")
b("A bandeira em Havana continua espanhola. Mas o comprador já tinha virado credor, e o credor começava a virar dono. E aí aparece o problema de sempre: e se esse comprador mudasse de ideia?")

# ───────────────────────── 4. A BANDEIRA DE UM, O COMPRADOR DE OUTRO ─────────────────────────
cap("4. A bandeira de um, o comprador de outro")
b("§ Um cubano exilado em Nova York toma notas num congresso de países da América, em Washington, em mil oitocentos e noventa e um. Ele está ali como delegado do Uruguai e se chama José Martí.", card="1891")
b("Em maio, ele escreveu numa revista: [break] o povo que compra, manda. O povo que vende, serve. E o povo que quer morrer vende a um povo só.")
b("Martí sabia do que falava. Cuba já tinha perdido uma guerra de dez anos pela independência. E agora o açúcar dela dependia de uma lei americana.")
b("§ Porque, naquele ano, um acordo entre Washington e Madri deixa o açúcar cubano entrar nos Estados Unidos quase sem imposto. A ilha bate recorde de produção. Aí, em noventa e quatro, o Congresso americano muda a lei e volta a cobrar quarenta por cento.", card="1894")
b("Em dois anos, as vendas para os Estados Unidos caem pela metade. Usina parada é gente sem trabalho no campo. Imagine depender de uma lei votada num país onde você nem vota.")
b("Em fevereiro de noventa e cinco, a guerra recomeça, organizada justamente por Martí, que cai em combate três meses depois. A luta segue, e em noventa e oito os Estados Unidos entram nela. Uma tarifa votada em Washington tinha ajudado a reacender a guerra. A Espanha sai de Cuba. Só que quem fica com a caneta é o comprador.", card="1895")

# ───────────────────────── 5. VINTE POR CENTO ─────────────────────────
cap("5. Vinte por cento")
b("§ Havana, dezembro de mil novecentos e dois. Cuba, independente havia sete meses, assina com os Estados Unidos um tratado de reciprocidade. O açúcar cubano ganha vinte por cento de desconto na tarifa americana.", card="1902")
b("Parece presente. Só que vem junto com outro papel, a Emenda Platt, posta na Constituição cubana: ela dá a Washington o direito de intervir na ilha e uma base em Guantánamo.")
b("Ou seja, o desconto entra pela porta da frente, e a cláusula, pela dos fundos. Repare que ninguém precisou de exército para isso: bastou o preço.")
b("§ Então o desconto atrai dinheiro. Empresas americanas compram usinas, terras e ferrovias. Antes da Primeira Guerra, tinham pouco mais de um terço da capacidade das usinas. Em mil novecentos e vinte e quatro, quase dois terços.", card="1924")
b("No meio do caminho, em vinte, o preço do açúcar sobe às nuvens e despenca em poucos meses. Bancos cubanos quebram, e credores americanos ficam com mais usinas. Cuba produzia. Mas a decisão morava em outro lugar.")

# ───────────────────────── 6. O MESMO MÊS ─────────────────────────
cap("6. O mesmo mês")
b("§ Franklin Roosevelt pega a caneta em nove de maio de mil novecentos e trinta e quatro e assina uma lei de cotas: o governo americano passa a decidir quanto açúcar cada fornecedor pode vender aos Estados Unidos.", card="1934")
b("Vinte dias depois, os dois países assinam um tratado que acaba com a Emenda Platt. Guantánamo fica. E a cláusula sai da Constituição para morar num número: a cota.")
b("Pense na cena: num mesmo mês, Cuba ganha o direito de não ser invadida e perde o direito de decidir quanto vende. Tente explicar essa vitória a um usineiro de Camagüey.")
b("§ Então, por vinte e cinco anos, a ilha vive em torno de um número escrito em Washington. Se você cortava cana, era a cota que decidia quantos meses do ano você teria trabalho.")
b("Governos caem e sobem nesse meio-tempo. Em cinquenta e dois, Fulgencio Batista dá um golpe. Mas o número continua lá. E, em cinquenta e nove, chega ao poder alguém que promete rasgá-lo.")

# ───────────────────────── 7. SETECENTAS MIL TONELADAS ─────────────────────────
cap("7. Setecentas mil toneladas")
b("§ Havana, fevereiro de mil novecentos e sessenta. Anastas Mikoyan, vice de Khrushchev, inaugura uma exposição soviética: máquinas, tratores e muita gente curiosa.", card="1960")
b("Numa visita a uma cooperativa, a multidão gritou para ele: e armas e aviões também! Mikoyan repete a frase. Dias depois, assina um acordo: a União Soviética vai comprar um milhão de toneladas de açúcar por ano.")
b("Lembra da nossa pergunta? Aqui ela fica mais difícil. Porque, nesses meses, o governo de Fidel Castro desapropria terras, e as refinarias americanas, que se recusam a processar petróleo soviético, são tomadas.")
b("§ Aí vem o dia seis de julho, e a cota, cláusula de Washington por vinte e cinco anos, vira arma: Eisenhower corta as setecentas mil toneladas que faltavam. Três dias depois, Khrushchev oferece comprar exatamente as mesmas. Se você é o dono daquele armazém do começo, o seu açúcar troca de comprador em setenta e duas horas.")
b("Em sessenta e um, exilados treinados pelos Estados Unidos são derrotados na Baía dos Porcos. Em sessenta e dois, vêm o embargo total e a crise dos mísseis. O comprador novo tinha chegado. Só que ele também ia cobrar.", card="1962")

# ───────────────────────── 8. SEIS CENTAVOS ─────────────────────────
cap("8. Seis centavos")
b("§ Moscou, janeiro de mil novecentos e sessenta e quatro. Fidel Castro vai à União Soviética e volta com um contrato: Moscou compra açúcar cubano por anos, a seis centavos de dólar a libra. Preço fixo, num mercado que sobe e desce.", card="1964")
b("Preço fixo é o sonho de qualquer produtor. Imagine saber hoje quanto você vai receber por cada saco daqui a seis anos. E as quantidades sobem ano a ano, até cinco milhões de toneladas em setenta.")
b("Só que preço fixo vinha com volume fixo. Para entregar o que o contrato pedia, e ainda ter açúcar para vender ao resto do mundo, Cuba põe o país inteiro no canavial.")
b("§ Para mil novecentos e setenta, a meta é de dez milhões de toneladas. A safra dá cerca de oito milhões e meio, a maior da história de Cuba. Em vinte e seis de julho, Fidel diz em público que a meta não foi cumprida e assume a responsabilidade.", card="1970")
b("E aqui está a primeira peça da resposta: o preço garantido vinha amarrado a uma quantidade. Quem garante o seu preço decide o que você planta. Só que esse preço ainda ia subir muito.")

# ───────────────────────── 9. QUASE CINCO VEZES O PREÇO ─────────────────────────
cap("9. Quase cinco vezes o preço")
b("§ Analistas da CIA, em Washington, fazem no começo dos anos oitenta uma conta que parece errada: Moscou paga cerca de quarenta e dois centavos por libra de açúcar cubano, quase cinco vezes o preço do mercado mundial.", card="1983")
b("Desde setenta e dois, Cuba está no Comecon, o bloco econômico soviético, com um papel na divisão de trabalho. Olhe qual: açúcar, níquel e frutas cítricas. Só que o pagamento vinha, em grande parte, em rublos de convênio, uma moeda que só comprava dentro do bloco.")
b("Tente pagar um hotel em Paris com o vale do mercadinho da sua rua. Era isso: Cuba vendia caro, mas só podia gastar com quem comprava. Em oitenta e nove, mais de oitenta por cento das exportações cubanas iam para o bloco socialista.")
b("Lembra da pergunta? A segunda peça está aqui: o comprador pagava bem, mas na moeda dele. Cada dólar que Cuba deixava de ganhar era uma porta de saída a menos.")
b("§ Então, em mil novecentos e noventa e um, o comprador simplesmente deixa de existir. A União Soviética acaba, e com ela o preço, o petróleo e os rublos que só valiam lá dentro. Cuba entra no que o governo chamou de Período Especial: apagões, comida racionada, ônibus parados.", card="1991")
b("Sem o preço de Moscou, a safra cai quase à metade em dois anos. E, sem dólares, a ilha precisava de alguém que pagasse com o que ela já não podia comprar: petróleo. O problema era achar quem.")

# ───────────────────────── 10. PETRÓLEO POR JALECO ─────────────────────────
cap("10. Petróleo por jaleco")
b("§ Caracas, trinta de outubro de dois mil. Fidel Castro e Hugo Chávez assinam um convênio: a Venezuela manda cinquenta e três mil barris de petróleo por dia, em condições especiais. E Cuba paga com gente: médicos, professores, técnicos.", card="2000")
b("Repare na mudança: o comprador novo não queria açúcar. Queria serviço. Depois, chegam a uns cem mil barris por dia, e perto de trinta mil cubanos trabalham na Venezuela, a maioria na saúde.")
b("E o açúcar? Sem o preço antigo, ele encolhe safra após safra. Tente achar outro país que já foi o maior exportador de açúcar do mundo e hoje compra açúcar de fora.")
b("§ Mas um comprador que paga com petróleo depende do próprio petróleo. A Venezuela entra em crise, e os barris diminuem. Em janeiro de dois mil e vinte e seis, depois que forças americanas capturam Nicolás Maduro, o petróleo venezuelano para de chegar.", card="2026")
b("Em dois mil e vinte e cinco, a ilha que já colheu oito milhões e meio de toneladas colheu menos de cento e cinquenta mil. O problema de sempre voltou, agora sem ninguém do outro lado do balcão.")

# ───────────────────────── FECHO ─────────────────────────
cap("Fecho")
b("§ [warm] Então, por que Cuba sempre dependeu de um país só? Porque quem vive de um produto precisa de preço garantido, e só um gigante garante preço. E cada garantia veio com uma cláusula que, quando apertava, só deixava uma saída, outro gigante: o estanco, a tarifa, a cota, o rublo, os médicos.")
b("As setecentas mil toneladas de mil novecentos e sessenta não mudaram de dono. Mudaram de cláusula.")
b("Talvez a pergunta certa nunca tenha sido quem comprava Cuba, e sim o que vinha escrito em letra miúda. E você, o que acha? Conta nos comentários.")

FALA = [("Bayamo", "Baiámo"), ("Gilberto Girón", "Rilbérto Rirón"), ("Girón", "Rirón"), ("Jesús del Monte", "Rerús del Mônte"),
        ("vegueros", "veguêros"), ("Cienfuegos", "Cienfuêgos"), ("Atkins", "Átkins"), ("Camagüey", "Camaguêi"), ("Mikoyan", "Mikoián"), ("Khrushchev", "Krushóv"),
        ("Comecon", "Cômecon"), ("Hugo Chávez", "Úgo Tcháves"), ("Fulgencio Batista", "Fulrrêncio Batísta"), ("Eisenhower", "Áisen-rauer"),
        ("Roosevelt", "Rúsvelt"), ("Guantánamo", "Guantánamo"), ("Nicolás Maduro", "Nicolás Madúro"), ("taínos", "taínos")]
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
