#!/usr/bin/env python3
"""Fonte única do 015-argentina (23/11/2026): roteiro (+ planos, quando o storyboard for escrito).
Gera SCRIPT.md e blocos.json; com o storyboard escrito (PENDENTE = False), também cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

Vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
ÂNGULO próprio (ANGULO.md): "os 13 zeros: a conta que ninguém quer pagar" — desde o porto colonial, a Argentina briga por quem paga
a conta do Estado (Buenos Aires × províncias pela alfândega; campo × cidade; governo × credores). O dinheiro do pampa (couro, charque,
trigo, carne, soja) está no meio de cada briga: quem fica com ele, manda. Quando ninguém aceita pagar, a conta vai para quem não pode
recusar: quem tem o peso no bolso. Cada zero cortado é o recibo de uma briga não resolvida.
EMBALAGEM.md aprovada no crivo r5 (3/3):
  A/T1 "A Argentina já foi RICA. Por que apagou 13 zeros da moeda?" + thumb rosto-emocao (rapaz de 1992 com o maço de 1969, "VALE NADA")
  B/T2 "Argentina: como a CARNE e o TRIGO decidiram quem manda" + thumb conflito-xvy (produtor do pampa × tangueiro, "QUEM PAGA?" + "1946")
  C/T3 "Por que a Argentina trocou de dinheiro 4 vezes em 22 anos?" + thumb numero-estatistica ("13 ZEROS", tesoura na cédula)
Hook: a gaveta do avô em 1/1/1992 — maço de 1969 com cinta de 1 milhão, dinheiro de uma tropa vendida no pampa (≤ 0:25)
  → frase-âncora "em vinte e dois anos… quatro vezes… treze zeros" (≤ 0:30) → "entre os mais ricos do mundo" (passagem)
  → PERGUNTA CENTRAL "quem pagou por esses treze zeros?" (≤ 0:50; trocada no crivo de ângulo r2: a antiga "como um país rico apagou 13 zeros" era quase a do hfMz/HX4L) → "essa é a história inteira" + "quem paga a conta… o couro, a carne, o trigo… quem fica com esse dinheiro, manda" (≤ 1:00).
Peças da resposta: 1 (cap. 4, 1890) quem manda e não quer cobrar de quem tem imprime ou pede emprestado; 2 (cap. 7, 1952) a conta muda de
  lado, mas não some; 3 (cap. 9, 1989) quando ninguém aceita pagar, a conta para no bolso de quem segura o dinheiro. Fecho responde e reenquadra.
"Guarde" único: o maço do avô → volta no cap. 8 (1970: vira dez mil; 1983: vira um peso), no cap. 9 (1992: o 13º zero) e no fecho.
As 4 trocas com motivo: 1970 e 1983 (cap. 8), 1985 e 1992 (cap. 9).
Neutralidade: Rosas, Roca, Perón, golpes, ditadura 1976–83 (com seriedade, números com a fonte), Malvinas, Menem, Kirchner/Cobos, Milei (1 frase).

Sintaxe dos planos (campo s), igual ao 016/017:
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1992") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Storyboard: escreva os planos em P[n] (n = número do bloco) acima de "# __PLANOS__" e ponha PENDENTE = False.
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006–017).
Imagens: Codex (canal.yaml visual.gerador: codex; fallback gemini). Prompts só de conteúdo; o estilo vem do canal.yaml.
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (006–017: ~128–131 ppm com pausas)
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
TITULO = "A história INTEIRA da Argentina"
PERGUNTA = "Quem pagou por esses treze zeros?"
PROMESSA = ("Como a Argentina, que já esteve entre os países mais ricos do mundo, trocou de dinheiro 4 vezes em 22 anos e apagou 13 zeros "
            "da moeda: 200 anos de uma briga por quem paga a conta, com o dinheiro do pampa (couro, carne, trigo) no meio de cada briga "
            "(EMBALAGEM.md r5).")
TITULOS = ('T1 "A Argentina já foi RICA. Por que apagou 13 zeros da moeda?" / T2 "Argentina: como a CARNE e o TRIGO decidiram quem manda" / '
           'T3 "Por que a Argentina trocou de dinheiro 4 vezes em 22 anos?"')

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None):
    ideia = t.startswith("§")
    n = sum(1 for x in B if "t" in x) + 1
    if not s: s = tuple(P.get(n, ()))
    if not s and PENDENTE: s = (f"tmp{n:03d}|placeholder",)
    assert s, f"N{n:03d} sem planos"
    B.append({"t": t.lstrip("§ ").strip(), "s": list(s), "card": card, "ideia": ideia})

PENDENTE = False   # storyboard escrito (P abaixo), 23/11/2026

# ───────── regras de prompt (Codex; fallback gemini) ─────────
# As refs de estilo vêm do Egito e vazam conteúdo (visual.md 010/011/013/014/016/017): TODA cena leva o cenário ancorado
# (PAMPA/BAC/BA19/BA00/BA40/BA70/BA90/LON…) ou o fundo de estúdio (EST) + NAO_EG; SEMTXT e SEMBAND em todas (nada de bandeira:
# nem argentina, nem inglesa, nem espanhola, nem brasileira). Codex põe marcos fora de época (anti-padroes §3d): Obelisco só de 1936
# em diante (BA40+); antes, "NO Obelisco"; Londres de 1824 sem Big Ben (1859). Ditadura 1976–83 só por lugar/objeto (praça vazia,
# lenços brancos, cadeiras vazias), sem armas nem soldados; 1935 sem arma em cena. Milei não aparece (nem caricatura): 2026 = cidade.
# Cédulas e cintas SEMPRE em branco (CED): o "1.000.000" e os nomes das moedas vão em rótulo no código (@@).
NAO_EG = ", NO pyramids, NO pharaoh headdress, NO turbans, NO desert dunes, NO camels, NO palm trees, NO crowns, NO domes, NO minarets"
MAPA = ("painted like a blank parchment terrain map seen from directly above, only coastlines, rivers, mountains, seas and flat colored areas, "
        "completely blank with no writing anywhere, no letters, no words, no labels, no numbers, no symbols, no compass, no border, no frame, no flags, no people")
SEMTXT = ", no readable writing, no letters anywhere, no numbers, no signs, no boards, no logos"
SEMBAND = ", no flags of any kind (no Argentine, British, Spanish or Brazilian flags), no banners, no pennants, no coats of arms, no emblems, no insignia"
GUERRA = ", no blood, no wounds, no bodies, no weapons fired, no guns pointed at anyone, no violence shown"
CED = (", every banknote and paper band is completely blank: plain pastel paper rectangles with only a simple oval frame shape, "
       "no numbers, no portraits, no letters, no writing on the paper band")
EST = (", set on a plain solid pale-cream studio background with a simple wooden tabletop, nothing else in the background, "
       "bare round white heads, NO robes, NO ancient architecture" + NAO_EG)
PAMPA = (", strictly the Argentine pampas: endless flat green-gold grassland to a very low horizon, a lone ombú tree, scattered cattle, "
         "wide bright blue sky, NO mountains, NO cactus, NO jungle" + NAO_EG)
PRATA = ", the wide muddy brown Río de la Plata estuary, flat low reedy shoreline, NO mountains, NO cliffs" + NAO_EG
BAC = (", strictly colonial Buenos Aires before 1810: low whitewashed adobe houses with red tile roofs, dirt streets, a modest church tower, "
       "the muddy brown river, NO Obelisco, NO tall buildings, NO pink government palace" + NAO_EG)
BA19 = (", strictly 19th-century Buenos Aires: low colonial houses with flat roofs and iron window grilles, cobbled streets, horse carts, "
        "gas lamps, the wide brown river, NO Obelisco, NO skyscrapers, NO cars" + NAO_EG)
BA00 = (", strictly Buenos Aires between 1890 and 1935: Parisian-style stone buildings with mansard roofs, wide avenues with horse carriages, "
        "early trams and the first black cars, NO Obelisco, NO skyscrapers, NO modern cars" + NAO_EG)
BA40 = (", strictly Buenos Aires in the 1940s-50s: wide avenues, Parisian-style stone buildings, 1940s rounded cars and trams, "
        "the tall plain white Obelisco allowed in the distance, NO glass towers, NO modern cars" + NAO_EG)
BA70 = (", strictly Buenos Aires in the 1970s-80s: grey concrete apartment blocks mixed with older Parisian-style buildings, "
        "boxy 1970s cars, NO glass towers, NO smartphones, NO modern cars" + NAO_EG)
BA90 = (", strictly Buenos Aires in the 1990s-2000s: apartment buildings with balconies, older Parisian-style facades, 1990s cars, "
        "NO smartphones, NO flat screens" + NAO_EG)
BA26 = ", strictly present-day Buenos Aires: wide avenues, Parisian-style facades, a few modern glass towers, modern buses" + NAO_EG
INT = (", strictly an interior Argentine town of the 1820s (like Córdoba or Tucumán): low adobe houses, a colonial whitewashed church, "
       "dry hills behind" + NAO_EG)
AND = ", strictly the high Andes: barren reddish-brown mountains, no trees, thin cold air, llamas" + NAO_EG
SAL = (", strictly a 19th-century saladero on the Río de la Plata shore: long wooden racks of salted beef strips drying in the sun, "
       "low brick sheds, barrels of salt, flat land" + NAO_EG)
PAT = ", strictly the dry plains of northern Patagonia: low thorny bushes, yellow grass, wide grey-blue sky, NO snow peaks close" + NAO_EG
LON24 = (", strictly the City of London in the 1820s: dark stone bank buildings with columns, horse carriages, gas lamps, "
         "NO Big Ben, NO clock tower, NO neo-Gothic Parliament, NO Tower Bridge, NO red buses" + NAO_EG)
LON90 = (", strictly the City of London in 1890: massive dark stone bank buildings with columns, horse cabs and omnibuses, gas lamps, "
         "NO Tower Bridge, NO red double-decker buses, NO cars" + NAO_EG)
LON33 = ", strictly London in 1933: Whitehall stone government buildings, black 1930s taxis, men in bowler hats, NO modern cars" + NAO_EG
SALA = (", strictly the Argentine Senate chamber: semicircular rows of dark wooden benches, red carpet, a raised presiding desk, "
        "tall windows, NO flags" + NAO_EG)
MAD = ", strictly an 18th-century Madrid palace hall: red-brick and pale stone, tall windows, gilded furniture" + NAO_EG
def ANO(a): return f", period-accurate {a}: clothes, buildings, ships, cars and objects of that time only, no modern objects"
PAPEL = ", the paper is drawn as plain wavy lines, completely illegible, no letters, no words, no numbers"
def X(k, d, cen="", ano=None, band=True, guerra=False, papel=False, ced=False, rot=None):
    return (f"{k}|{d}{cen}" + (ANO(ano) if ano else "") + (PAPEL if papel else "") + (CED if ced else "") + SEMTXT
            + (SEMBAND if band else "") + (GUERRA if guerra else "") + (f"@@{rot}" if rot else ""))
def M(k, d, rot=None): return f"{k}|{d}, " + MAPA + NAO_EG + (f"@@{rot}" if rot else "")
# Personagens (bíblia: rosto nunca descrito; "round-white-head cartoon …"; nome de figura real só no rótulo do código)
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes, wearing an ordinary brown felt hat and a plain brown jacket"
NETO = "a round-white-head cartoon young man of 1992 Buenos Aires with curly dark hair and a denim jacket"
AVO = "a round-white-head cartoon Argentine cattle rancher of 1969 with a grey mustache shape, a light-brown short-brim country hat, a white shirt and a dark vest"
CONTRAB = "round-white-head cartoon Dutch sailors of 1650 in baggy breeches, loose shirts and wide-brim hats"
COLON = "round-white-head cartoon colonial Buenos Aires men of the 1600s in simple shirts, short capes and wide-brim hats"
BANQ = "a round-white-head cartoon London banker of 1824 in a dark tailcoat, a high white collar and a top hat"
BANQ90 = "a round-white-head cartoon London banker of 1890 with grey side-whiskers shape, a black frock coat and a top hat"
ROSAS = "a round-white-head cartoon Argentine governor of the 1830s with light hair and long sideburn shapes, a dark blue military coat and a plain red sash"
URQ = "a round-white-head cartoon Argentine caudillo general of 1852 with a dark beard shape, a dark military coat and a poncho over one shoulder"
ROCA = "a round-white-head cartoon Argentine general of 1879 with a big dark mustache and short beard shape, a plain dark blue military coat and a kepi cap"
INDIG = ("round-white-head cartoon Mapuche and Tehuelche people of the 1870s with straight black hair, woven ponchos and simple cloth headbands, "
         "drawn with dignity, no caricature, no feather headdresses")
CITY = "round-white-head cartoon City of London bankers of 1890 in black frock coats and top hats"
COLONOS = "round-white-head cartoon Italian and Spanish immigrant farmers of 1912 in flat caps, rough shirts and suspenders"
ROCAJR = "a round-white-head cartoon Argentine vice-president of 1933 with a thin mustache shape, a dark three-piece suit and a homburg hat"
RUNC = "a round-white-head cartoon British minister of 1933, bald, with a small grey mustache shape and a dark suit"
TORRE = "a round-white-head cartoon elderly Argentine senator of 1935 with a white beard shape and small round glasses, in a dark suit"
PERON = "a round-white-head cartoon Argentine president of 1946 with slicked-back black hair and a broad smile, in a plain light military-style jacket with no insignia"
FARM = "a round-white-head cartoon pampas wheat farmer of 1946 in a light-brown short-brim country hat, a white shirt with rolled sleeves and a dark vest"
OPER = "round-white-head cartoon Buenos Aires factory workers of 1947 in blue work overalls and flat caps"
RODR = "a round-white-head cartoon Argentine economy minister of 1975 with dark-rimmed glasses shape and a grey suit"
ALF = "a round-white-head cartoon Argentine president of 1985 with a thick dark mustache shape, combed-back grey hair and a dark suit"
MENEM = "a round-white-head cartoon Argentine president of 1991 with long dark sideburn shapes and a dark suit"
COBOS = "a round-white-head cartoon Argentine vice-president of 2008 with grey hair and glasses shape, in a dark suit"

P = {}
# HOOK (a gaveta do avô, 1/1/1992)
P[1] = [X("apt_1992", "A modest Buenos Aires apartment living room on New Year's morning 1992: light through a balcony door, an old wooden chest of drawers, a small 1990s TV, party streamers on the floor, nobody", BA90, "1992"),
        X("neto_drawer", f"{NETO} pulling open the top drawer of his late grandfather's old wooden chest of drawers, curious", BA90, "1992"),
        X("bundle_drawer", "Close view inside an old wooden drawer: a thick stack of old yellowed banknotes tied with one wide plain white paper band, next to an old pocket watch and reading glasses, nobody in the picture", BA90, "1992", ced=True, rot="1.000.000 PESOS"),
        X("neto_holds", f"{NETO} holding the thick stack of old yellowed banknotes tied with a plain white paper band with both hands in front of his chest, eyebrows raised, a nervous half-laugh, one sweat drop", BA90, "1992", ced=True),
        X("guide_drawer", f"{GUIA} sitting on the edge of an open wooden drawer like on a bench, beside a stack of old banknotes, waving at the viewer", BA90, ced=True)]
P[2] = [X("pampa_tropa", "A herd of cattle driven across the flat pampas by two riders on horseback at golden hour, dust in the air", PAMPA, "1969"),
        X("avo_sells", f"{AVO} shaking hands with a cattle buyer at a wooden corral gate on the pampas, the buyer handing him a thick stack of banknotes tied with a plain white paper band", PAMPA, "1969", ced=True),
        X("coin_vs_bundles", "A single tiny coin alone on one end of a long table, and at the other end a huge mountain of stacks of old yellowed banknotes tied with paper bands, nobody", EST, ced=True),
        X("neto_mountain", f"{NETO} standing next to a gigantic pile of banknote stacks taller than him, holding up one tiny coin between two fingers, puzzled", EST, ced=True)]
P[3] = [X("four_notes", "Four different old banknotes laid in a row on a wooden table, each a different pastel color (pink, green, blue, brown), each smaller than the previous, nobody", EST, ced=True),
        X("scissors_zeros", "A big pair of scissors cutting a long paper strip printed with a row of plain empty rings, the cut-off rings falling onto the table like confetti, nobody", EST, rot="13 ZEROS"),
        M("map_argentina", "Map of the southern tip of South America with Argentina in warm gold, the long Andes along the west, the wide Río de la Plata estuary in the northeast, neighboring countries in pale grey, the Atlantic in pale blue", rot="ARGENTINA")]
P[4] = [X("ba_1910", "A grand Buenos Aires avenue around 1910, Parisian-style stone buildings, elegant round-white-head cartoon people in hats and long dresses, horse carriages and early trams", BA00, "1910"),
        X("ship_1910", "A big steamship loading wheat sacks and frozen beef at the Buenos Aires docks around 1910, red-brick warehouses and cranes", BA00, "1910"),
        X("guide_question", f"{GUIA} sitting on a pile of old banknote stacks with a hand on his chin, puzzled", EST, ced=True),
        X("who_paid", "A long blank paper bill unrolling across a table, many hands reaching toward it from all sides, but every hand pulling back before touching it", EST, papel=True)]
P[5] = [X("port_vs_pampa", "A tug of war on a riverbank: on the left a round-white-head cartoon Buenos Aires port merchant of the 1850s in a frock coat, on the right a round-white-head cartoon gaucho in a poncho, both pulling the two ends of one long blank paper bill", BA19, "1850", papel=True),
        X("hides_stack", "A tall stack of dried cattle hides at a colonial riverside warehouse, ox carts unloading more", BAC, "1780"),
        X("beef_plant_1910", "Sides of beef hanging in a cold meat-packing plant around 1910, round-white-head cartoon workers in white coats and caps", BA00, "1910"),
        X("wheat_station", "Hundreds of wheat sacks piled at a small railway station on the flat pampas, a steam train waiting", PAMPA, "1910"),
        X("ombu_cattle", "Wide view of the flat pampas at sunset, a lone ombú tree, cattle grazing in golden grass, nobody", PAMPA, band=False),
        X("chair_power", "An empty high-backed carved wooden chair of power standing on top of a pile of cattle hides, wheat sacks and beef crates, nobody", EST),
        X("guide_manda", f"{GUIA} standing on the pampas pointing at a heavy chair of power that sits on a pile of hides and wheat sacks", PAMPA)]
P[6] = [X("drawer_close", f"{NETO} gently closing the drawer with the banknote stack inside, one finger raised as if saying 'wait'", BA90, "1992", ced=True),
        X("colonial_dusk", "A tiny colonial riverside settlement at dusk: a few low adobe houses, a modest church tower, small boats pulled up on the mud", BAC, "1650"),
        X("prata_shallow", "Wide view of the shallow brown Río de la Plata with no harbor at all, only mud flats and reeds, one ship anchored far away", PRATA, "1650")]
# 1. O PORTO QUE NÃO PODIA SER PORTO
P[7] = [X("dutch_ship_night", "A Dutch merchant sailing ship with plain cream sails anchored far from the shore of the wide brown Río de la Plata at night under the moon", PRATA, "1650"),
        X("rowboats_night", "Small rowboats going back and forth in the dark between an anchored sailing ship and the muddy shore, lanterns half covered by hands", PRATA, "1650"),
        X("unload_cloth", f"{CONTRAB} handing bolts of cloth and iron tools to {COLON} on the muddy shore at night", PRATA, "1650"),
        X("load_hides_night", f"{COLON} loading bundles of dried cattle hides into a rowboat at night, looking over their shoulders", PRATA, "1650"),
        X("silver_hidden", "Close view of a silver bar hidden inside a rolled-up dried cattle hide in a rowboat, moonlight glinting on the silver, nobody", PRATA, "1650"),
        M("map_potosi", "Map of southern South America, a silver dotted trail running from the high Andes in the north (today's Bolivia) down across the plains to the Río de la Plata estuary", rot="POTOSÍ → BUENOS AIRES"),
        X("potosi_mountain", "The great reddish cone-shaped silver mountain of Potosí with a colonial mining town at its foot, llama caravans carrying sacks", AND, "1650")]
P[8] = [X("royal_decree", "A Spanish royal decree with a big red wax seal on a dark wooden table in a colonial office, a quill beside it, nobody", BAC, "1650", papel=True),
        M("map_official_route", "Map of the Atlantic Ocean and South America with a long dotted route from Spain across the ocean to the narrow isthmus of Panama, then down the Pacific coast to Lima, then over the Andes down to the Río de la Plata", rot="ROTA OFICIAL"),
        X("lima_mules", "A colonial Spanish-American city square of 1650 with a stone cathedral with two bell towers and wooden balconies, a long mule train with boxes leaving the square", ", strictly colonial Lima of the 1600s: low houses with closed wooden balconies, dry hills behind" + NAO_EG, "1650"),
        X("mule_andes", "A long mule train loaded with wooden boxes crossing a steep barren Andes pass, round-white-head cartoon muleteers in ponchos", AND, "1650"),
        X("letter_loop", "A tiny folded paper letter flying in a huge looping dotted path across a blue ocean from one small shore to a faraway shore and back again, nobody", EST, papel=True)]
P[9] = [X("smuggle_street", f"A colonial Buenos Aires dirt street: {COLON} quietly buying foreign cloth and tools at a back door, a merchant looking left and right", BAC, "1680"),
        X("wild_cattle", "Huge herds of wild cattle roaming free across the empty flat pampas, no fences, no houses, nobody", PAMPA, "1680"),
        X("hunters_1700", "Round-white-head cartoon colonial cattle hunters (early gauchos) of 1700 on horseback in ponchos chasing wild cattle across the pampas, swinging bolas (stone balls on cords)", PAMPA, "1700", guerra=True),
        X("hides_drying", "Dozens of cattle hides stretched on wooden stakes drying in the sun on the open pampas, nobody", PAMPA, "1700"),
        X("hide_scale", "A round-white-head cartoon colonial merchant weighing one dried cattle hide on a big hanging scale in a dim adobe warehouse", BAC, "1700")]
P[10] = [X("king_1776", "A round-white-head cartoon Spanish king of 1776 in a white powdered wig and a blue coat, at a table in a palace hall, tapping a big blank map of South America with one finger", MAD, "1776", papel=True),
         M("map_viceroyalty", "Map of southern South America with one big region in warm gold covering present-day Argentina, Uruguay, Paraguay and Bolivia, the Río de la Plata estuary at its door, the rest of the continent in pale grey", rot="VICE-REINO DO RIO DA PRATA"),
         X("port_opens", "Several sailing ships arriving openly in daylight at colonial Buenos Aires on the brown river, round-white-head cartoon dock workers unloading crates", BAC, "1780"),
         X("aduana_building", "A colonial customs house in Buenos Aires: a low whitewashed building with arches and a big wooden door, ox carts loaded with hides waiting in line outside", BAC, "1780"),
         X("customs_clerk", "A round-white-head cartoon Spanish customs clerk of 1780 in a wig at a desk next to an iron strongbox, dropping silver coins into it", BAC, "1780"),
         X("cash_box", "Close view of a heavy iron colonial strongbox overflowing with silver coins on a wooden table, a big iron key beside it, nobody", EST)]
P[11] = [X("hides_one_door", "Long lines of ox carts loaded with cattle hides coming from every direction across the plains toward one single gate of a small walled customs house by the river", BAC, "1790"),
         X("key_door", "A big iron key in the lock of a heavy wooden customs house door, nobody", BAC, "1790"),
         X("cabildo_1810", "A round-white-head cartoon crowd of 1810 gathered in a rainy square in front of a white two-storey colonial town hall with arches and a small bell tower, some holding umbrellas", BAC, "1810"),
         X("viceroy_leaves", "A round-white-head cartoon Spanish viceroy of 1810 in a wig and an embroidered coat walking out of a colonial hall with his hat in his hand, offended", BAC, "1810"),
         X("provinces_door", "Round-white-head cartoon men of the Argentine interior in 1810 in ponchos and wide hats standing at a closed door with arms crossed", INT, "1810"),
         X("key_fight", "Several hands from all sides reaching for one big iron key hanging on a nail on a whitewashed wall", EST)]
# 2. A PRIMEIRA CONTA
P[12] = [X("london_1824", "The City of London in 1824: dark stone bank buildings with columns, horse carriages, round-white-head cartoon men in top hats and tailcoats", LON24, "1824"),
         X("baring_office", f"{BANQ} at a big desk in a wood-panelled bank office with stacks of printed bonds, quill in hand", LON24, "1824", papel=True, rot="BARING"),
         X("bonds_stack", "Close view of a stack of bond certificates with ornate borders but completely blank in the middle, tied with a ribbon, nobody", LON24, "1824", papel=True),
         X("investors_queue", "Round-white-head cartoon London investors of 1824 in top hats queuing at a bank counter to buy bonds", LON24, "1824", papel=True)]
P[13] = [X("plan_water", "An engineer's drawing on a table showing a planned harbor, small coastal towns and water pipes as simple sketched shapes, an oil lamp, nobody", BA19, "1824", papel=True),
         X("money_half", "A pile of gold coins being split in two on a bank table: the bigger half swept away by a banker's hand, the smaller half left behind", LON24, "1824"),
         X("half_bag", "A small bag of gold coins being unloaded from a sailing ship at Buenos Aires, a round-white-head cartoon official looking at how small it is, disappointed", BA19, "1825"),
         X("guide_half", f"{GUIA} holding a contract in one hand and only half of a torn banknote in the other, shocked", EST, papel=True, ced=True)]
P[14] = [M("map_banda", "Map of the Río de la Plata region: the small land east of the Uruguay river and north of the estuary (today's Uruguay) in warm gold, Brazil to the north in pale green, Argentina to the west in pale gold", rot="BANDA ORIENTAL"),
         X("war_1825", "Two small cavalry armies of 1825 facing each other far apart across a green rolling plain, smoke in the distance, round-white-head cartoon soldiers in plain dark uniforms and plain shakos", PAMPA, "1825", guerra=True),
         "money_half",
         X("guide_brazil", f"{GUIA} pointing at the viewer with a raised eyebrow, standing between two small toy armies on a table", EST)]
P[15] = [X("blockade_1826", "Imperial Brazilian sailing frigates of 1826 with plain sails lined up blocking the mouth of the brown Río de la Plata", PRATA, "1826"),
         X("hides_unsold", "Cattle hides piling up unsold in a Buenos Aires warehouse, a round-white-head cartoon merchant sitting on the pile with his head in his hands", BA19, "1826"),
         "cash_box",
         X("printing_paper", "A round-white-head cartoon official of 1826 cranking a wooden printing press that spits out plain paper notes, no coins anywhere", BA19, "1826", ced=True)]
P[16] = [X("bondholders_1827", "Round-white-head cartoon British bondholders of 1827 in top hats waving bond papers in front of a closed bank counter window, angry", LON24, "1827", papel=True),
         X("paper_refused", "A round-white-head cartoon Buenos Aires shopkeeper of 1827 holding out a fistful of paper notes that a baker refuses, shaking his head", BA19, "1827", ced=True),
         X("interior_1827", "Round-white-head cartoon men of an interior Argentine province in 1827 in ponchos in a dusty town square, pointing toward the far-away port", INT, "1827"),
         "key_fight"]
# 3. O DONO DA ALFÂNDEGA
P[17] = [X("saladero", "A saladero on the river shore: long wooden racks of salted beef strips (charque) drying in the sun, brick sheds, piles of salt, nobody", SAL, "1825", band=False),
         X("charque_workers", "Round-white-head cartoon workers of 1825 hanging strips of salted beef on drying racks next to barrels of salt", SAL, "1825"),
         X("charque_ship", "Barrels and bales of dried salted beef loaded onto a sailing ship at a wooden river pier", SAL, "1825"),
         X("plantation_meal", "Round-white-head cartoon enslaved African workers of the 1820s on a sugar plantation, drawn with dignity, no caricature, tired, receiving a simple meal of dried beef in a yard", ", strictly a Brazilian sugar plantation of the 1820s: green cane fields, a brick mill chimney, NO palm trees" + NAO_EG, "1825", guerra=True)]
P[18] = [X("rosas_saladero", f"{ROSAS} standing proudly in a saladero yard among drying racks of salted beef", SAL, "1829", rot="JUAN MANUEL DE ROSAS"),
         X("rosas_desk", f"{ROSAS} at a desk in a colonial government house in Buenos Aires signing papers", BA19, "1830", papel=True),
         X("guide_charque", f"{GUIA} at a rustic ranch kitchen table in southern Brazil with a plate of rice, beans and dried beef, eyebrows raised at the viewer", ", strictly a southern Brazilian ranch kitchen: wooden table, a wood stove, a window to green hills" + NAO_EG),
         "saladero"]
P[19] = [X("rosas_strongbox", f"{ROSAS} sitting on a big iron strongbox inside the customs house, arms crossed, refusing to share", BA19, "1835"),
         "aduana_building",
         X("blockade_1845", "French and British sailing warships of the 1840s anchored in a line blocking the port of Buenos Aires on the brown river", PRATA, "1845"),
         "printing_paper"]
P[20] = [X("urquiza", f"{URQ} on horseback in front of his army of gauchos on a green plain", PAMPA, "1852", rot="JUSTO JOSÉ DE URQUIZA"),
         X("caseros", "Two armies of 1852 far apart on a flat plain near Buenos Aires, cavalry charging in the distance, smoke, round-white-head cartoon soldiers", PAMPA, "1852", guerra=True),
         X("rosas_leaves", f"{ROSAS} wrapped in a dark cloak boarding a small boat toward a sailing ship at night, looking back sadly", PRATA, "1852"),
         M("map_split", "Map of Argentina with the province of Buenos Aires around the Río de la Plata colored in a different warm color from all the other provinces, a thin gap between them")]
P[21] = [X("ba_1880", "Barricades of carts and barrels in a cobbled Buenos Aires street of 1880, round-white-head cartoon militiamen in kepis crouched behind them, smoke in the distance", BA19, "1880", guerra=True),
         "key_door",
         X("roca_column", f"{ROCA} on horseback leading a long column of soldiers across the dry southern plains", PAT, "1879", guerra=True, rot="JULIO ROCA"),
         X("indig_hill", f"{INDIG} watching from a low hill as a column of soldiers passes far away on the plain, sad and dignified", PAT, "1879", guerra=True),
         M("map_south", "Map of Argentina with the vast southern plains and Patagonia shaded in warm gold and divided into a few very large plots by thin lines"),
         X("few_families", "A round-white-head cartoon wealthy landowner family of 1880 in fine clothes on the porch of a big estancia house, endless fenced pampas around them", PAMPA, "1880")]
P[22] = [X("party_1880", "A grand party hall in Buenos Aires of the 1880s with crystal chandeliers, round-white-head cartoon guests dancing, an unpaid blank bill lying on a silver tray in front", BA19, "1885", papel=True),
         "few_families"]
# 4. CADA BANCO COM SUA IMPRESSORA
P[23] = [X("boe_1890", "The Bank of England in 1890: a massive windowless stone building with columns on a busy street, gas lamps, horse cabs", LON90, "1890"),
         X("city_table", f"{CITY} gathered around a long table in a grand bank hall, each signing the same long guarantee paper", LON90, "1890", papel=True),
         X("baring_worried", f"{BANQ90} slumped at his desk among stacks of unsold bond papers, worried", LON90, "1890", papel=True)]
P[24] = [X("bonds_dust", "A tall pile of unsold bond certificates gathering dust in a London bank vault, cobwebs, nobody", LON90, "1890", papel=True),
         X("water_pipes", "Round-white-head cartoon workers laying big iron water pipes in a muddy Buenos Aires street of the 1880s", BA19, "1886"),
         "plan_water",
         "bonds_stack"]
P[25] = [X("provincial_bank", "Inside a small provincial bank of 1887 in an Argentine town, round-white-head cartoon clerks running a printing press that piles up banknotes", INT, "1887", ced=True),
         X("guide_presses", f"{GUIA} standing among many small printing presses, each one spitting out banknotes, arms wide open", EST, ced=True),
         "printing_paper"]
P[26] = [X("land_auction", "Round-white-head cartoon buyers of 1888 crowding around a land auction table set up on the open pampas, plots marked by wooden stakes", PAMPA, "1888", papel=True),
         X("paper_flood", "A flood of paper banknotes pouring out of a bank door into a cobbled Buenos Aires street of 1889, people trying to catch them", BA19, "1889", ced=True),
         X("parque_1890", "Round-white-head cartoon civilian rebels and soldiers of 1890 behind barricades in a Buenos Aires park with tall trees and an old brick arsenal, smoke", BA19, "1890", guerra=True),
         X("empty_chair_1890", "An empty presidential chair behind a desk in a government office of 1890, a resignation letter on the desk, nobody", BA19, "1890", papel=True)]
P[27] = [X("guide_piece1", f"{GUIA} placing the first piece of a big blank jigsaw puzzle on a table, smiling", EST),
         "who_paid",
         X("handcuff_press", "A wooden printing press with a big iron handcuff locked around its crank, nobody", EST)]
# 5. A ALGEMA DE OURO
P[28] = [X("congress_1899", "Round-white-head cartoon Argentine lawmakers of 1899 in frock coats voting by raising hands in a wood-panelled chamber", BA00, "1899", papel=True),
         X("gold_vault", "A bank vault with a neat pile of gold bars and beside it a stack of paper banknotes exactly as tall as the gold pile, nobody", EST, ced=True),
         "handcuff_press"]
P[29] = [X("beef_ship_1905", "A steamship with refrigerated holds being loaded with frozen beef at the Buenos Aires docks in 1905", BA00, "1905"),
         X("harvest_1905", "Round-white-head cartoon farm workers harvesting wheat with a steam threshing machine on the endless pampas", PAMPA, "1905"),
         M("map_trade", "Map of the Atlantic Ocean with dotted shipping lines from the Río de la Plata to the ports of Europe, small steamships along the lines"),
         "ba_1910"]
P[30] = [X("alcorta_town", "A small farming town of 1912: low brick houses, a railway line, a grain warehouse, wheat fields all around", PAMPA, "1912"),
         X("alcorta_hall", f"{COLONOS} crowding a simple hall, standing and shouting, one man on a chair speaking", PAMPA, "1912", rot="ALCORTA, SANTA FÉ"),
         X("landlord_1912", "A round-white-head cartoon absentee landlord of 1912 in a city suit counting rent money at a desk", BA00, "1912")]
P[31] = [X("tenant_pays", "A round-white-head cartoon tenant farmer of 1912 handing most of his wheat sacks to a landlord's agent, keeping only a few", PAMPA, "1912"),
         X("idle_plows", f"Plows and horses standing idle in an unplanted field, {COLONOS} sitting on the fence with arms crossed", PAMPA, "1912"),
         "alcorta_hall"]
P[32] = [X("gold_leaves", "Gold bars being carried out of a vault and loaded onto a ship, the vault left almost empty", BA00, "1914"),
         X("vault_shut", "A heavy round vault door being shut with a big padlock, nobody", EST),
         X("march_1930", "Round-white-head cartoon cadets and soldiers of 1930 marching in a column down a Buenos Aires avenue with Parisian buildings, crowds watching from the sidewalks", BA00, "1930", guerra=True),
         "gold_vault"]
# 6. A CARNE COM LETRA MIÚDA
P[33] = [X("london_1933", "London in 1933: Whitehall stone government buildings, black 1930s taxis, round-white-head cartoon men in bowler hats", LON33, "1933"),
         X("roca_runciman", f"{ROCAJR} and {RUNC} shaking hands across a table in a London government office, papers in front of them", LON33, "1933", papel=True, rot="ROCA E RUNCIMAN"),
         X("beef_london", "Crates of chilled beef being unloaded from a ship at a London dock in 1933", LON33, "1933")]
P[34] = [X("quota_split", "A big pile of beef carcasses split in two: a small part goes to a modest local meat plant on the left, the large rest goes to a huge foreign meat plant with a tall chimney on the right", BA00, "1933"),
         X("fine_print", "Close view of a contract with a magnifying glass over its last tiny lines, nobody", EST, papel=True),
         X("frigorifico", "A huge brick meat-packing plant of the 1930s on the Buenos Aires riverbank with a tall chimney and refrigerated ships at its pier", BA00, "1933"),
         "roca_runciman"]
P[35] = [X("rancher_cheap", "A round-white-head cartoon Argentine cattle rancher of 1935 at a meat plant gate receiving only a few coins for a big steer, frowning", PAMPA, "1935"),
         X("senate_1935", "Round-white-head cartoon senators of 1935 in dark suits seated in the chamber", SALA, "1935"),
         X("torre", f"{TORRE} standing at his bench speaking with a raised finger, holding papers", SALA, "1935", papel=True, rot="LISANDRO DE LA TORRE"),
         X("senate_chaos", "Round-white-head cartoon senators of 1935 ducking behind the benches, papers flying in the air, a commotion", SALA, "1935", guerra=True),
         X("empty_bench", "An empty wooden bench in the Senate chamber with a hat and scattered papers left on it, quiet light, nobody", SALA, "1935", papel=True, rot="ENZO BORDABEHERE")]
P[36] = [X("guide_serious", f"{GUIA} sitting alone on an empty wooden bench, serious, holding his hat in his hands", SALA),
         "empty_bench"]
P[37] = [X("pounds_vault", "Stacks of paper pound notes locked inside a London bank vault behind iron bars with a big padlock, nobody", LON33, "1942", ced=True),
         X("coup_1943", "Round-white-head cartoon soldiers of 1943 in plain uniforms standing calmly in a square in front of a pink government palace, people watching", BA40, "1943", guerra=True),
         X("colonel_window", "A round-white-head cartoon Argentine army colonel of 1943 with slicked-back black hair seen from behind at a tall window, looking out over the city", BA40, "1943"),
         "beef_ship_1905", "ombu_cattle"]
# 7. O CAMPO PAGA A CIDADE (cena forte de 1946: paga a Thumb B)
P[38] = [X("pergamino", "A small railway station on the pampas in late 1946: a low brick station, tall grain elevators, horse carts loaded with wheat sacks waiting in line", PAMPA, "1946"),
         X("farmer_cart", f"{FARM} arriving at the station with a horse cart full of wheat sacks, hopeful", PAMPA, "1946", rot="PERGAMINO"),
         X("iapi_desk", "A round-white-head cartoon government buyer of 1946 in a suit at a single desk on the station platform with a stamp and a ledger, a long line of farmers in front", PAMPA, "1946", papel=True, rot="IAPI"),
         X("peron_balcony", f"{PERON} smiling and waving from a balcony of a pink government palace", BA40, "1946", rot="JUAN PERÓN")]
P[39] = [X("low_price", f"A government buyer handing a small blank price slip to {FARM}, who stares at it in disbelief", PAMPA, "1946", papel=True),
         X("port_1947", "Cranes lifting wheat sacks into a big cargo ship at the port of Buenos Aires in 1947", BA40, "1947"),
         X("europe_queue", "A ration queue of round-white-head cartoon people in a war-damaged European city of 1947 waiting for bread", ", strictly a European city after the Second World War: damaged brick buildings, rubble cleared to the sides" + NAO_EG, "1947"),
         "iapi_desk"]
P[40] = [X("factory_1947", f"{OPER} cheering in a Buenos Aires factory, receiving pay envelopes among machines", BA40, "1947"),
         X("holiday_beach", "Round-white-head cartoon working families of 1948 enjoying paid holidays on a crowded Atlantic beach with striped umbrellas and a seafront of grand stone buildings", ", strictly Mar del Plata, Argentina, in the 1940s" + NAO_EG, "1948"),
         X("campo_cidade", f"ONE single continuous scene: on the left {FARM} standing in a golden wheat field handing a heavy bag of coins across to the right, where round-white-head cartoon Buenos Aires factory workers of 1947 in blue overalls receive it in front of a factory, the tall plain white Obelisco far in the background on the right", BA40, "1946"),
         X("central_bank", "A grand stone Central Bank building with columns in Buenos Aires in 1946, round-white-head cartoon officials carrying boxes in", BA40, "1946")]
P[41] = [X("fewer_fields", "A pampas farm where a farmer plants wheat only in one small corner and leaves the rest of the land as pasture", PAMPA, "1950"),
         X("drought", "Cracked dry earth on the pampas with withered wheat, a round-white-head cartoon farmer looking up at the empty sky", PAMPA, "1951"),
         X("radio_1952", "A round-white-head cartoon Argentine family of 1952 gathered around a big wooden radio in their kitchen, listening seriously", BA40, "1952"),
         X("dark_bread", "A loaf of dark brown bread on a simple kitchen table next to an empty plate, nobody", BA40, "1952"),
         "port_1947"]
P[42] = ["guide_piece1",
         X("warships_1955", "Grey warships of 1955 seen from far away on the brown Río de la Plata in front of Buenos Aires, smoke on the horizon, no ship firing", PRATA, "1955", guerra=True),
         X("pendulum", "A huge clock pendulum swinging over a miniature city, a long blank paper bill tied to its weight, nobody", EST, papel=True),
         "who_paid"]
# 8. O PÊNDULO (a gaveta volta: 1970 e 1983)
P[43] = [X("bank_1970", "Round-white-head cartoon people of 1970 queuing at a bank counter in Buenos Aires to exchange old banknotes for new ones", BA70, "1970", ced=True),
         X("note_1970", "A crisp new banknote next to an old yellowed one on a bank counter, nobody", BA70, "1970", ced=True, rot="PESO LEY · −2 ZEROS"),
         X("avo_1970", f"{AVO}, a bit older, at a bank window watching his thick banknote stack being swapped for a small thin stack", BA70, "1970", ced=True),
         "bundle_drawer"]
P[44] = [X("govt_hole", "A round-white-head cartoon government official of the 1960s shoveling paper banknotes into a big hole in the floor of a treasury office that never fills", BA70, "1965", ced=True),
         "scissors_zeros", "pendulum"]
P[45] = [X("rodrigo_tv", f"{RODR} at a microphone in a 1975 TV studio announcing a plan, papers in hand", BA70, "1975", papel=True, rot="CELESTINO RODRIGO"),
         X("gas_1975", "A 1975 Buenos Aires gas station with a long queue of boxy 1970s cars, a round-white-head cartoon attendant staring at the pump in shock", BA70, "1975"),
         X("strike_1975", "A general strike in 1975: round-white-head cartoon workers marching peacefully along a wide avenue, the tall plain white Obelisco in the distance, no banners", BA70, "1975")]
P[46] = [X("plaza_empty_1976", "The Plaza de Mayo in Buenos Aires at grey dawn in March 1976: the pink government palace closed, the square completely empty, nobody", BA70, "1976"),
         X("empty_chairs", "A row of empty wooden chairs in a dim room, a coat left on the back of each one, quiet, nobody", BA70, "1976"),
         X("white_scarves", "Simple white cloth headscarves laid in a circle on the paving stones of an empty square around a small white obelisk-shaped monument, nobody", BA70, "1977"),
         X("conadep_book", "A thick plain report book with a blank cover on a wooden desk under a lamp, nobody", BA70, "1984", papel=True, rot="CONADEP, 1984")]
P[47] = [X("debt_tower", "A stack of foreign loan contracts growing like a tower from small to huge on a desk, nobody", EST, papel=True),
         M("map_malvinas", "Map of the South Atlantic with the southern tip of Argentina and the Malvinas/Falkland islands to the east, the islands in warm gold", rot="MALVINAS, 1982"),
         X("bc_takes_debt", "Round-white-head cartoon businessmen of 1982 handing their own debt papers to a central bank official at a big desk, who takes them all", BA70, "1982", papel=True),
         X("guide_debt", f"{GUIA} holding a long bill with his own small portrait on it, surprised, pointing at himself", EST, papel=True),
         "central_bank"]
P[48] = [X("note_1983", "A new banknote of 1983 on a bank counter next to a pile of old ones, nobody", BA70, "1983", ced=True, rot="PESO ARGENTINO · −4 ZEROS"),
         X("bundle_coin", "Inside the old wooden drawer: the thick stack of yellowed banknotes tied with a plain paper band, and next to it one single small coin, nobody", BA70, "1983", ced=True),
         X("prices_1983", "A round-white-head cartoon shopkeeper of 1983 changing blank price tags on shelves again, tired", BA70, "1983"),
         "who_paid"]
# 9. O DÉCIMO TERCEIRO ZERO (1985 e 1992)
P[49] = [X("alfonsin_night", f"{ALF} signing a decree at night at a desk in a presidential office, a lamp on", BA70, "1985", papel=True),
         "alfonsin_night#detalhe-centro@@RAÚL ALFONSÍN",
         X("frozen_prices", "A supermarket of 1985 with frost and icicles covering the blank price tags, a round-white-head cartoon shopper amazed", BA70, "1985"),
         X("note_1985", "A new banknote of 1985 held up in a hand in front of a bank window, nobody else", BA70, "1985", ced=True, rot="AUSTRAL · −3 ZEROS"),
         "handcuff_press"]
P[50] = [X("farmer_1987", "A round-white-head cartoon pampas farmer of 1987 next to a grain silo with arms crossed, complaining", PAMPA, "1987"),
         X("strike_1987", "Round-white-head cartoon union workers of 1987 marching on a Buenos Aires avenue, no banners", BA70, "1987"),
         "govt_hole"]
P[51] = [X("market_1989", "A crowded Buenos Aires supermarket in July 1989: round-white-head cartoon employees re-pricing goods with labelling guns while shoppers hurry, all labels blank", BA70, "1989"),
         X("baskets_100_300", "Two identical small shopping baskets side by side; next to the second one a pile of banknotes three times taller than next to the first, nobody", EST, ced=True)]
P[52] = [X("bank_1990", "Round-white-head cartoon depositors of January 1990 crowding outside the closed glass doors of a Buenos Aires bank, shocked", BA90, "1990"),
         X("bonex", "A round-white-head cartoon depositor holding a long bond certificate with an ornate border instead of his money", BA90, "1990", papel=True),
         X("guide_wakes", f"{GUIA} waking up startled in bed, holding a bond paper", BA90, papel=True)]
P[53] = ["guide_piece1",
         X("hand_fading", "Close view of a hand gripping a few banknotes tightly while the notes slowly fade and shrink, nobody else", EST, ced=True),
         X("menem", f"{MENEM} at a podium in a government hall, one hand raised, announcing a law", BA90, "1991", rot="CARLOS MENEM"),
         X("one_to_one", "A balance scale with one blank pale blue banknote on one plate and one blank green banknote on the other, perfectly level, nobody", EST, ced=True)]
P[54] = [X("note_1992", "A crisp new banknote of 1992 on a bank counter, nobody", BA90, "1992", ced=True, rot="PESO CONVERSÍVEL · −4 ZEROS"),
         "bundle_drawer",
         X("zero_13", "One last plain empty ring falling from a long paper strip onto a pile of twelve others on the floor, a pair of scissors beside it, nobody", EST, rot="13º ZERO"),
         "neto_holds"]
P[55] = [X("vault_dollars", "A vault with shelves where each blank pale blue banknote sits next to a blank green banknote, but more and more shelves have only the blue ones, nobody", EST, ced=True),
         X("loan_1998", "Round-white-head cartoon Argentine officials of 1998 receiving bags of money from foreign bankers in a glass office", BA90, "1998")]
# 10. O PORTO DE HOJE
P[56] = [X("la_plata_2001", "A provincial government office in La Plata in 2001: 1990s computers and desks, a round-white-head cartoon clerk opening his pay envelope", ", strictly La Plata, Argentina, in 2001: tree-lined diagonal avenues, early-1900s public buildings" + NAO_EG, "2001"),
         X("patacon", "Close view of a colorful paper bond note with an ornate border held in a hand", EST, ced=True),
         X("bakery_2001", "A round-white-head cartoon baker of 2001 in a small neighborhood bakery accepting a colorful paper bond for bread, shrugging", BA90, "2001", ced=True)]
P[57] = [X("quasi_moneys", "A table covered with a dozen different colorful paper notes of different sizes, nobody", EST, ced=True),
         X("guide_voucher", f"{GUIA} paying for lunch at a café counter with a colorful paper voucher", BA90, "2001", ced=True),
         "patacon"]
P[58] = [X("five_chairs", "Five empty presidential chairs in a row in a government hall, quiet, nobody", BA90, "2001"),
         X("pots_2001", "Round-white-head cartoon people of December 2001 banging pots in front of a bank with closed metal shutters on a Buenos Aires street", BA90, "2001"),
         X("pesification", "A blank green banknote going into a machine and coming out as a pale blue banknote with a small coin dropping off, nobody", EST, ced=True),
         "hand_fading"]
P[59] = [X("grain_port", "Huge concrete grain silos and bulk ships at a river export port, trucks unloading soybeans onto conveyor belts", ", strictly the Paraná river grain ports near Rosario, Argentina" + NAO_EG, "2002"),
         X("soy_field", "An endless green soybean field on the pampas with a modern combine harvester", PAMPA, "2002"),
         "cash_box", "aduana_building"]
P[60] = [X("senate_2008", "Round-white-head cartoon senators of 2008 in modern suits in the chamber late at night, tired", SALA, "2008"),
         X("roadblock_2008", "Round-white-head cartoon farmers of 2008 blocking a pampas highway with tractors and pickup trucks, sitting around a small fire", PAMPA, "2008"),
         X("tie_vote", "A balance scale perfectly level with many identical small round-white-head figures on each plate, nobody else", EST),
         X("cobos", f"{COBOS} at the raised presiding desk of the Senate, leaning into a microphone, solemn", SALA, "2008", rot="JULIO COBOS")]
P[61] = [X("farmers_cheer", "Round-white-head cartoon farmers of 2008 cheering at dawn around their tractors on a pampas highway", PAMPA, "2008"),
         X("ba_2026", "Present-day Buenos Aires: a wide avenue with the tall plain white Obelisco, modern buses, ordinary people walking", BA26, "2026"),
         X("rosada_2026", "The pink government palace of Buenos Aires seen across a square on a sunny day, ordinary people walking, nobody prominent", BA26, "2026"),
         "who_paid"]
# FECHO
P[62] = [X("three_duels", "Three pairs of round-white-head cartoon figures in a row, each pair pulling the two ends of a blank paper bill: a 19th-century port merchant and a gaucho; a 1940s farmer and a factory worker; a man in a suit and a foreign banker in a top hat", EST, papel=True),
         "port_vs_pampa", "campo_cidade"]
P[63] = [X("drawer_light", "The old wooden drawer open with the stack of yellowed banknotes in a beam of afternoon light, an old country hat on the chest of drawers, nobody", BA90, ced=True),
         "avo_sells", "neto_holds"]
P[64] = [X("guide_end", f"{GUIA} sitting on an old wooden chest of drawers holding a stack of old banknotes, smiling at the viewer", BA90, ced=True),
         "ombu_cattle", "map_argentina"]
# __PLANOS__


# ───────────────────────── HOOK (a gaveta do avô, 1/1/1992) ─────────────────────────
cap("Hook")
b("[curious] Buenos Aires, primeiro de janeiro de noventa e dois. Imagine: você abre a gaveta do avô: um maço de cédulas com cinta, um milhão de pesos.", card="1992")
b("É o preço de uma tropa vendida no pampa em sessenta e nove. Hoje, você junta um centavo com cem mil maços desses.")
b("Porque, em vinte e dois anos, a Argentina trocou de dinheiro quatro vezes e apagou treze zeros.")
b("[serious] E isso num país que já esteve entre os mais ricos do mundo. Então fica a pergunta: quem pagou por esses treze zeros?")
b("§ Essa é a história inteira da Argentina. A resposta mora numa briga de duzentos anos: quem paga a conta. E quem paga quase sempre foi o pampa: o couro, a carne, o trigo. Quem fica com esse dinheiro, manda.")
b("Guarde esse maço: ele volta. E tudo começa num porto que nem podia ser porto.")

# ───────────────────────── 1. O PORTO QUE NÃO PODIA SER PORTO ─────────────────────────
cap("1. O porto que não podia ser porto")
b("§ Rio da Prata, por volta de mil seiscentos e cinquenta. É noite, e um navio holandês ancora longe da margem. Botes vão e voltam: descem tecidos e ferro, sobem couro de boi e, escondida no meio, prata de Potosí.", card="c. 1650")
b("Tudo proibido. A lei manda a mercadoria pelo caminho oficial: Panamá, Lima e meses em lombo de mula. Imagine mandar uma carta de São Paulo para o Rio passando por Lisboa.")
b("Então Buenos Aires vive de contrabando. E o pampa ajuda: o gado dos primeiros espanhóis virou rebanhos soltos. Ninguém criava esses bois, caçava. Mas só o couro tinha preço.")
b("§ Em mil setecentos e setenta e seis, a Espanha desiste de brigar com o mapa: cria o vice-reino do Rio da Prata e abre o porto. Nasce a alfândega, a caixa registradora de Buenos Aires.", card="1776")
b("Repare: o couro de meio continente agora paga imposto numa porta só. Quem tem a chave tem o dinheiro. Então, em maio de mil oitocentos e dez, Buenos Aires se livra do vice-rei. E a pergunta vira outra: de quem é a chave?", card="1810")

# ───────────────────────── 2. A PRIMEIRA CONTA ─────────────────────────
cap("2. A primeira conta")
b("§ Londres, julho de mil oitocentos e vinte e quatro. O banco Baring lança os títulos do primeiro empréstimo de Buenos Aires: um milhão de libras, a seis por cento.", card="1824")
b("Era para um porto, povoados e água encanada. Só que, descontados juros adiantados e comissões, chegou pouco mais da metade. Tente pegar um empréstimo e receber metade na assinatura.")
b("§ E nem essa metade virou porto. No fim de vinte e cinco, começa a guerra com o Império do Brasil pela Banda Oriental, o atual Uruguai. Se você é brasileiro, a primeira conta da Argentina foi gasta numa guerra contra o seu país.", card="1825")
b("A esquadra brasileira bloqueia o Prata, e o couro para de sair. Sem couro, a alfândega seca. Então o governo faz o que ainda vai fazer muitas vezes: imprime papel que não se troca por metal.")
b("Em vinte e sete, Buenos Aires para de pagar os ingleses: primeiro calote. A conta fica com o credor de Londres e com quem tinha papel no bolso. Mas o interior pergunta: e a nossa parte da alfândega?", card="1827")

# ───────────────────────── 3. O DONO DA ALFÂNDEGA ─────────────────────────
cap("3. O dono da alfândega")
b("§ Um saladeiro no Prata, anos de mil oitocentos e vinte. Carne salgada secando ao sol: o charque. Boa parte embarca para Cuba e para o Brasil, para alimentar gente escravizada.")
b("Um dos sócios de saladeiro é Juan Manuel de Rosas, governador de Buenos Aires desde vinte e nove. Se você já comeu charque gaúcho, saiba: um concorrente dele mandou na Argentina por uns vinte anos.", card="1829")
b("Rosas governa com a alfândega na mão: cerca de oitenta por cento da receita da província. E não divide com ninguém. Quando França e Inglaterra bloqueiam o porto, ele paga imprimindo papel.")
b("§ Mas quem fica do lado de fora acaba arrombando. Em cinquenta e dois, o caudilho Urquiza derrota Rosas com ajuda do Brasil, de novo. Só que Buenos Aires não aceita dividir e passa quase dez anos à parte.", card="1852")
b("A briga só acaba em oitenta, com combates nas ruas e milhares de mortos: o governo nacional fica com a alfândega. E a campanha de Julio Roca contra os povos indígenas do sul entrega milhões de hectares a poucas famílias.", card="1880")
b("Agora o porto era do país, e o pampa tinha dono. O problema era quem ia pagar a festa que vinha.")

# ───────────────────────── 4. CADA BANCO COM SUA IMPRESSORA ─────────────────────────
cap("4. Cada banco com sua impressora")
b("§ Londres, quinze de novembro de mil oitocentos e noventa. No Banco da Inglaterra, banqueiros da City assinam uma garantia de dezessete milhões de libras. Tudo para salvar o Baring, aquele de vinte e quatro.", card="1890")
b("O banco tinha se enchido de títulos argentinos. Só que ninguém mais comprava. O último encalhado era de água e esgoto para Buenos Aires. A água encanada de vinte e quatro: se você está contando, sessenta e seis anos de espera.")
b("§ Como se chega ali? Em oitenta e sete, uma lei deixa os bancos das províncias emitirem dinheiro. Imagine cada estado do Brasil com a sua impressora de reais.", card="1887")
b("Então as províncias tomam ouro emprestado em Londres, imprimem papel e emprestam para quem compra terra no pampa. A terra sobe, o papel se multiplica, e o ouro some. Em noventa, vem a Revolução do Parque, e o presidente renuncia.")
b("Lembra da nossa pergunta? Aqui está a primeira peça da resposta: quando quem manda não quer cobrar de quem tem, imprime ou pede emprestado. E a conta chega depois, com juros. Então, como amarrar a mão de quem imprime?")

# ───────────────────────── 5. A ALGEMA DE OURO ─────────────────────────
cap("5. A algema de ouro")
b("§ Buenos Aires, outubro de mil oitocentos e noventa e nove. Uma lei cria a Caixa de Conversão: o peso de papel fica preso ao ouro, e só se imprime papel novo quando entra ouro novo.", card="1899")
b("É uma algema na impressora. E funciona, porque o ouro está entrando: carne e trigo para a Europa. Se você fosse dono de terra no pampa, esses eram os seus anos: a Argentina fica entre os países mais ricos do mundo.")
b("§ Mas de quem é esse dinheiro? Junho de mil novecentos e doze, Alcorta, em Santa Fé. Mais de dois mil colonos lotam um salão: quase todos imigrantes italianos e espanhóis, quase nenhum dono da terra que planta.", card="1912")
b("O aluguel da terra come a colheita. Então eles decidem não plantar até o aluguel baixar: é o Grito de Alcorta. Imagine plantar o trigo que alimenta a Europa e não conseguir pagar o aluguel do chão.")
b("Só que a algema de ouro só segura quando o ouro chega. A Caixa fecha na guerra de catorze e, de novo, em vinte e nove. E, em setembro de trinta, os militares derrubam um presidente eleito. Quem ia comprar a carne agora?", card="1930")

# ───────────────────────── 6. A CARNE COM LETRA MIÚDA ─────────────────────────
cap("6. A carne com letra miúda")
b("§ Londres, primeiro de maio de mil novecentos e trinta e três. O vice-presidente Julio Roca, filho do general de oitenta, fecha um acordo com o ministro inglês Walter Runciman: a Inglaterra continua comprando carne argentina.", card="1933")
b("Mas com cota. E repare na letra miúda: no máximo quinze por cento dessa carne passa por frigoríficos argentinos. O resto fica com os estrangeiros. A Roca é atribuída a frase: a Argentina seria parte integrante do Império Britânico.")
b("§ Só que, aqui dentro, quem perde é o criador que vende o boi barato ao frigorífico. Em trinta e cinco, o senador Lisandro de la Torre denuncia o negócio. No último dia do debate, um policial atira contra ele e mata o colega que o protegia, Enzo Bordabehere.", card="1935")
b("Pense nisso: a briga pela carne chegou a tiros dentro do Congresso.")
b("Na Segunda Guerra, a Inglaterra segue comprando, mas paga em libras presas em Londres: a carne vai, e o dinheiro fica lá. Em quarenta e três, outro golpe. E dele sai um coronel com outra resposta para a pergunta de sempre: quem fica com o dinheiro do pampa?")

# ───────────────────────── 7. O CAMPO PAGA A CIDADE ─────────────────────────
cap("7. O campo paga a cidade")
b("§ Pergamino, no pampa, fim de mil novecentos e quarenta e seis. Imagine que você plantou trigo. Na estação, só existe um comprador: o IAPI, o instituto criado em maio pelo governo de Juan Perón.", card="1946")
b("O preço é o que o instituto marca, e é baixo. No porto, o mesmo trigo segue para uma Europa com fome, por muito mais. Você nunca vê essa diferença. Quem vê é o governo.")
b("Do outro lado da conta, nas fábricas de Buenos Aires, o operário ganha aumento, décimo terceiro e férias pagas. Quem paga? O campo. E Perón nacionaliza o Banco Central: agora quem manda também decide quanto dinheiro existe.")
b("§ Só que o campo não é bobo: com preço baixo, planta menos. Aí vêm as secas, e o trigo some. Em fevereiro de cinquenta e dois, o governo anuncia no rádio um plano de emergência: carne e farinha branca para fora, e pão escuro na cidade.", card="1952")
b("E aqui está a segunda peça da resposta: a conta muda de lado, mas não some. Em cinquenta e cinco, os militares derrubam Perón. E começa um pêndulo: cada governo empurra a conta para quem não está no poder.")

# ───────────────────────── 8. O PÊNDULO ─────────────────────────
cap("8. O pêndulo")
b("§ Buenos Aires, primeiro de janeiro de mil novecentos e setenta. Chega o peso lei, com dois zeros a menos. Lembra do maço do avô? Nesse dia, o milhão vira dez mil.", card="1970")
b("O motivo: quinze anos de pêndulo e de inflação encheram as cédulas de zeros. Repare: nenhum zero cai por capricho. Cada corte chega depois de anos imprimindo para tapar o buraco do governo.")
b("§ Em junho de setenta e cinco, a briga explode. Um pacote do ministro Celestino Rodrigo dobra o dólar e quase triplica a gasolina. Os sindicatos param o país, e o plano cai: é o rodrigazo.", card="1975")
b("[serious] Em março de setenta e seis, os militares tomam o poder outra vez. A ditadura faz desaparecer milhares de pessoas: cerca de trinta mil, segundo organismos de direitos humanos; quase nove mil casos registrados pela comissão oficial de oitenta e quatro.", card="1976")
b("§ E a dívida externa salta de uns oito para uns quarenta e cinco bilhões de dólares. Em oitenta e dois, ano da derrota nas Malvinas, o Banco Central passa a bancar boa parte da dívida das empresas. Se você nunca pegou um dólar emprestado, parabéns: passou a dever mesmo assim.", card="1982")
b("Então a inflação passa de cem por cento, e em junho de oitenta e três a segunda troca corta mais quatro zeros: o peso argentino. O milhão do avô vira um peso. Só que o dinheiro novo nasce com a pergunta velha: quem paga?", card="1983")

# ───────────────────────── 9. O DÉCIMO TERCEIRO ZERO ─────────────────────────
cap("9. O décimo terceiro zero")
b("§ Noite de catorze de junho de oitenta e cinco. Raúl Alfonsín, eleito na volta da democracia, assina o Plano Austral: preços e salários congelados de um dia para o outro. É a terceira troca: o austral, três zeros a menos e a promessa de não imprimir para pagar o governo.", card="1985")
b("Funciona por um tempo. Mas ninguém aceita a conta: o campo reclama do câmbio, os sindicatos fazem greve atrás de greve. Então a impressora volta.")
b("§ Em julho de oitenta e nove, os preços sobem quase duzentos por cento num mês. Pelos números do INDEC, se você gastava cem no mercado no começo do mês, no fim precisava de quase trezentos. ", card="1989")
b("Em janeiro de noventa, o governo novo faz o impensável: os depósitos a prazo nos bancos viram, à força, títulos em dólar para dez anos. É o Plano Bônex. Quem guardou dinheiro no banco acorda credor do Estado.", card="1990")
b("Lembra da nossa pergunta? Aqui entra a terceira peça: quando ninguém aceita pagar, a conta para no bolso de quem segura o dinheiro. Então, em noventa e um, o governo de Carlos Menem amarra a moeda ao dólar por lei: um para um.")
b("E, no primeiro de janeiro de noventa e dois, a quarta troca corta os últimos quatro zeros: nasce o peso conversível. Repare na gaveta do começo: o milhão do avô agora vale um décimo de milionésimo de peso. Caiu o décimo terceiro zero.", card="1992")
b("Só que, para cada peso, precisava existir um dólar. E, quando os dólares não chegam, a Argentina pega emprestado. O problema é que empréstimo vence.")

# ───────────────────────── 10. O PORTO DE HOJE ─────────────────────────
cap("10. O porto de hoje")
b("§ La Plata, agosto de dois mil e um. Um funcionário da província recebe parte do salário num papel colorido: o patacão, um bônus da província. Não é peso, mas a padaria aceita.", card="2001")
b("Logo há mais de uma dúzia de quase-moedas, perto de metade do dinheiro em papel do país. Se você já pagou o almoço com vale, entende: é a conta voltando para o bolso, em outra cor.")
b("§ Em dezembro, o país suspende a dívida e tem cinco presidentes em onze dias. Aí vem a pesificação: o depósito em dólar vira um peso e quarenta por dólar, e o dólar de verdade passa de três. A diferença fica, de novo, com quem segurava o dinheiro.")
b("Então o governo volta ao porto e recria o imposto sobre a exportação de grãos, as retenções. A soja do pampa vira o caixa do Estado, como você viu o couro fazer na velha alfândega.", card="2002")
b("§ Senado, madrugada de dezessete de julho de dois mil e oito. Depois de meses de estradas bloqueadas pelo campo contra retenções maiores, a votação empata: trinta e seis a trinta e seis. Desempata o vice-presidente Julio Cobos, do próprio governo. E ele diz: meu voto não é positivo.", card="2008")
b("O aumento cai: o campo, mais uma vez, decidiu quem manda. Em dois mil e vinte e seis, com Javier Milei, a inflação caiu para perto de dois por cento ao mês. Só que a pergunta continua na mesa: quem paga o ajuste?", card="2026")

# ───────────────────────── FECHO ─────────────────────────
cap("Fecho")
b("§ [warm] Então, quem pagou por esses treze zeros? Por duzentos anos, a Argentina brigou por quem paga a conta: o porto contra as províncias, o campo contra a cidade, o governo contra os credores.")
b("E, quando ninguém aceita pagar, a conta vai para quem não pode recusar: quem tem o peso no bolso. Como o avô da gaveta.")
b("Talvez a pergunta nunca tenha sido quanto vale o peso, e sim quem fica segurando ele. E você, o que acha? Conta nos comentários.")

# Grafias de voz (texto → Fish); a tela/legenda usa a grafia correta. Conferir no Whisper (voz.md).
FALA = [("Juan Manuel de Rosas", "Ruan Manuel de Rôssas"), ("Rosas", "Rôssas"), ("Potosí", "Potossí"), ("Baring", "Bêring"),
        ("Justo José de Urquiza", "Rústo Rossé de Urkíssa"), ("Entre Ríos", "Êntre Ríos"), ("Caseros", "Casêros"),
        ("Julio Roca", "Rúlio Rôca"), ("Roca", "Rôca"), ("Juárez Celman", "Ruárez Célman"), ("Alcorta", "Alcórta"),
        ("Walter Runciman", "Uólter Rânsiman"), ("Lisandro de la Torre", "Lissândro de la Tôrre"), ("Enzo Bordabehere", "Ênzo Bordabeêre"),
        ("Otto Niemeyer", "Óto Nímaier"), ("Pergamino", "Pergamíno"), ("IAPI", "iápi"), ("Juan Perón", "Ruan Perón"),
        ("Avellaneda", "Avechanêda"), ("Celestino Rodrigo", "Celestíno Rodrígo"), ("rodrigazo", "rodrigásso"),
        ("Carlos Menem", "Cárlos Mênem"), ("Julio Cobos", "Rúlio Côbos"), ("Javier Milei", "Raviér Miléi"),
        ("saladeiro", "saladêiro")]

def fala(t):
    for a, z in FALA: t = re.sub(r"(?<![\wÀ-ú])" + re.escape(a) + r"(?![\wÀ-ú])", z, t)
    return t

IDEIA = set()
THUMB = None   # thumbs nascem dos 3 conceitos aprovados no crivo (EMBALAGEM.md r5): arte na etapa 2 (skill thumbnail)

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
    if not PENDENTE:   # sem storyboard, não grava cenas/planos de placeholder
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
    if not PENDENTE: (out / "STORYBOARD.md").write_text("\n".join(linhas) + "\n")
    if PENDENTE:   # só o roteiro: as estatísticas de planos não valem
        stats = {k: stats[k] for k in ("palavras", "duracao_s", "capitulos")} | {"storyboard": "pendente"}
    print(json.dumps(stats, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
