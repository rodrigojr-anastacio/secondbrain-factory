#!/usr/bin/env python3
"""Fonte única do 008-franca (13/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

3º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
Molde History in Minutes (narrativa contínua). Referência de código: videos/006-roma e 007-russia.
  hook: Soissons, 486: o vaso quebrado com o machado e, um ano depois, a cabeça do guerreiro rachada por Clóvis (Gregório de Tours, II.27)
  → 1.300 anos depois a França corta a cabeça do próprio rei → PERGUNTA CENTRAL (≤ 0:50) → "Essa é a história inteira da França"
  → 1 "guarde" (o machado) → a Gália (problema da era 1)
  → 10 eras, cada uma: problema herdado → cena no presente → ≤ 3 fatos → solução → novo problema
  → fecho ≤ 45 s: responde, reenquadra e pergunta para os comentários.
Fio condutor: O MACHADO DE SOISSONS (a lâmina que impõe o rei) e REIMS (onde Clóvis é batizado e os reis são sagrados).
  Volta em Reims 1429 (Joana leva o rei para ser sagrado onde Clóvis foi batizado), em 1793 (a guilhotina: a lâmina agora desce
  sobre o rei; e a Santa Ampola de Reims é quebrada, como o vaso) e no fecho. A resposta montada em 3 peças:
  a França sobreviveu porque juntou tudo numa coroa (peça 1, era 5); o rei virou o Estado, e a culpa ganhou um endereço só (peça 2, era 7);
  cortaram a cabeça, mas guardaram a máquina, e o trono vazio sempre foi ocupado de novo (peça 3, era 9).
Pergunta volta: era 5 (1ª peça), era 7 (2ª peça), era 8 ("lembra da nossa pergunta?"), era 9 (3ª peça), fecho (resposta).
Neutralidade: fecha na Quinta República (1958) e na reconciliação com a Alemanha; nada de política atual.

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="486") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006/007).
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (006/007: 128 ppm com pausas)
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
TITULO = "A história INTEIRA da França"
PERGUNTA = "Como o país que nasceu do machado de um rei acabou cortando a cabeça de outro, e por que, mesmo assim, nunca conseguiu viver sem alguém no trono?"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None):
    ideia = t.startswith("§")
    B.append({"t": t.lstrip("§ ").strip(), "s": list(s), "card": card, "ideia": ideia})

# Mapas sem texto (rótulos no código, src/labels.jsx) e regra de "sem escrita" (o nano-banana inventa letras em placas, escudos e estandartes)
MAPA = ("painted like a blank parchment terrain map seen from directly above, only coastlines, rivers, mountains and flat colored areas, "
        "completely blank with no writing anywhere, no letters, no words, no labels, no symbols, no compass, no border, no frame")
SEMTXT = ", no readable writing, no letters anywhere, no signs, no boards"
SEMBAND = ", no flags, no letters on shields or banners"
SEMMOD = ", no modern objects, no tricolor flags"      # 005/007: o nano-banana põe bandeira atual em cena de época
SANG = ", no blood, no gore"
# Personagens (regra da bíblia: nada de rosto descrito; "round-white-head cartoon …")
FRANCO = "round-white-head cartoon Frankish warriors of the 5th century with long hair, simple flat long mustache shapes, short belted tunics, round wooden shields and small throwing axes"
CLOVIS = "a round-white-head cartoon young Frankish king with long blond hair, a simple flat blond mustache shape, a red cloak and a plain thin gold circlet"
BISPO = "a round-white-head cartoon early medieval bishop with a simple flat white beard shape, a tall white mitre, white and gold robes and a crozier"
GAUL = "round-white-head cartoon Gaulish Celtic warriors with simple flat big drooping mustache shapes, checked trousers, long swords and tall oval shields"
VERC = "a round-white-head cartoon young Gaulish chief with long hair, a simple flat big drooping mustache shape, a plain bronze helmet with no wings, a gold torc and a red cloak"
LEG = "round-white-head cartoon Roman legionaries in red tunics, segmented iron armor, iron helmets and curved red rectangular shields"
CESAR = "a round-white-head cartoon Roman general, bald, with a laurel wreath, a red general's cloak and bronze armor"
CMAGNO = "a round-white-head cartoon old emperor with a simple flat long white beard shape, a heavy golden crown with a cross and a blue and gold robe"
VIKING = "round-white-head cartoon Viking warriors with simple flat blond beard shapes, conical iron helmets and plain round wooden shields"
HUGO = "a round-white-head cartoon early medieval king with a simple flat short brown beard shape, a small plain gold crown and a plain blue cloak"
FELIPE = "a round-white-head cartoon medieval king with a simple flat short brown beard shape, a gold crown and a blue surcoat with small gold lily flowers over chain mail"
LEONOR = "a round-white-head cartoon medieval queen with a simple gold crown over a white veil and a long green gown"
INGL = "round-white-head cartoon medieval English longbowmen in padded jackets and simple steel caps holding tall longbows"
CAVF = "round-white-head cartoon French medieval knights in shining plate armor on horses with blue horse cloths with small gold lily flowers"
JOANA = "a round-white-head cartoon teenage girl with short dark bowl-cut hair in shining plate armor holding a plain white banner"
CARLOS7 = "a round-white-head cartoon thin young French king of the 15th century, beardless, with a tall dark fur hat and a long red robe"
HENR4 = "a round-white-head cartoon French king of 1590 with a simple flat short pointed grey beard and mustache shape, a black hat with a white plume and a black doublet with a white ruff"
HUG = "round-white-head cartoon French Protestant townspeople of the 1570s in plain black clothes with white collars"
LUIS14 = "a round-white-head cartoon French king of the 17th century with a huge curly black wig, a blue ermine-lined cloak with gold lily flowers and shoes with red heels"
NOBRES = "round-white-head cartoon French nobles of the 17th century with big curly wigs, lace collars, silk coats and feathered hats"
LUIS16 = "a round-white-head cartoon chubby French king of the 1780s with a powdered white wig with side curls, a blue coat with a silver star and a blue sash"
MARIA = "a round-white-head cartoon queen of the 1780s with a very tall powdered white hairstyle decorated with feathers and a pale pink silk gown"
SANSC = "round-white-head cartoon Parisian revolutionaries of 1789 with red caps, striped trousers, simple jackets and long pikes"
CAMPF = "round-white-head cartoon French peasants of the 1780s in simple linen shirts, wooden clogs and straw hats, women with white bonnets"
NAPO = "a round-white-head cartoon short French general of 1800 with straight dark hair, a black bicorne hat worn sideways and a dark blue coat with gold epaulettes"
NAPOI = "a round-white-head cartoon French emperor with a golden laurel wreath and a red velvet ermine coronation robe with golden bees"
NAP3 = "a round-white-head cartoon French emperor of the 1860s with a simple flat long waxed mustache shape, a small pointed goatee shape and a dark military coat"
PRUS = "round-white-head cartoon Prussian soldiers of 1870 in dark blue coats and spiked leather helmets"
POILU = "round-white-head cartoon French soldiers of 1916 in pale horizon-blue greatcoats and round steel helmets"
GENERAL = "a very tall round-white-head cartoon French general of the 1940s with a big nose shape, a round flat-topped kepi and a khaki uniform"
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes"

# ───────────────────────── HOOK (Soissons, 486: o vaso e o machado) ─────────────────────────
cap("Hook")
b("[serious] Soissons, quatrocentos e oitenta e seis. Imagine você entre guerreiros francos, diante do saque de uma batalha.",
  f"soissons_loot|{FRANCO} gathered around a big pile of loot on the ground after a battle: golden cups, coins, cloth and weapons, a Roman town with walls behind, smoke in the sky" + SEMBAND,
  f"franks_cheer|{FRANCO} cheering and raising axes after a victory on a field near an old Roman town, morning light" + SEMBAND,
  "roman_town_soissons|An old Roman walled town in northern Gaul at the end of the 5th century with smoke rising after a battle, Frankish riders at the gate" + SEMBAND,
  "loot_close|Close view of a pile of treasure on the grass: golden plates, silver coins, silk and a beautiful tall church vase decorated with gold in the middle, dramatic light" + SEMTXT,
  card="486")
b("Na pilha, um vaso precioso de igreja. O rei Clóvis pede o vaso para devolver a um bispo. Só que um guerreiro racha o vaso com o machado e diz: o rei só leva o que a sorte der.",
  f"clovis_asks|{CLOVIS} pointing at a precious golden church vase on the pile of loot while his warriors watch" + SEMBAND + "@@CLÓVIS",
  f"bishop_waits|{BISPO} waiting at a distance with folded hands and a hopeful face, Frankish warriors around",
  "axe_vase|A round-white-head cartoon Frankish warrior with long hair and a simple flat mustache shape smashing a golden church vase with a small axe, pieces flying, the other warriors shocked, comic but tense" + SEMTXT,
  "vase_broken|Close view of a dented broken golden church vase lying on the grass next to an axe, symbolic, dramatic light" + SEMTXT,
  "vase_reflection|Close view of a precious golden church vase decorated with gems and engraved crosses, a warrior's hand reaching for it, dramatic light" + SEMTXT,
  "warrior_defiant|A round-white-head cartoon Frankish warrior with long hair and a simple flat mustache shape holding a small axe and pointing at his chest defiantly, other warriors shocked behind him, comic" + SEMBAND,
  f"clovis_silent|{CLOVIS} standing very still with a cold silent stare, his warriors whispering behind him")
b("Um ano depois, na revista da tropa, Clóvis joga o machado desse guerreiro no chão. Quando o homem se abaixa, o rei racha a cabeça dele: [slightly dramatic] assim você fez com o vaso em Soissons.",
  f"troop_review|{CLOVIS} walking along a long line of {FRANCO} standing at attention on a field in early spring, inspecting their weapons" + SEMBAND,
  "spring_field|A field in early spring with lines of Frankish warriors, tents and horses, a cold blue morning sky" + SEMBAND,
  "axe_thrown|A round-white-head cartoon Frankish king throwing a warrior's small axe onto the ground, the warrior bending down to pick it up, dramatic, comic style",
  "clovis_walks|Close view of a round-white-head cartoon Frankish king with long blond hair walking slowly along a line of warriors and stopping in front of one of them, tense" + SEMBAND,
  "axe_raised|The dark silhouette of a Frankish king raising a small axe against a bright spring sky, seen from below, dramatic, symbolic" + SANG,
  "warriors_gasp|Round-white-head cartoon Frankish warriors with wide eyes and open mouths in shock, all looking at the same spot on the ground, comic" + SANG,
  card="487")
b("§ [serious] Mil e trezentos anos depois, a França corta a cabeça do próprio rei. Então, a pergunta: como o país que nasceu do machado de um rei acabou cortando a cabeça de outro, e por que, mesmo assim, nunca conseguiu viver sem alguém no trono?",
  "guillotine_square|A tall guillotine on a wooden platform in a huge Paris square in winter 1793, a big crowd of round-white-head cartoon revolutionaries with red caps around it, grey sky" + SANG,
  "king_head_crowd|A huge crowd of round-white-head cartoon Parisian revolutionaries in red caps shouting and raising pikes in a winter square, 1793" + SANG + SEMTXT,
  f"empty_throne|A golden throne with a blue velvet cushion decorated with gold lily flowers standing empty in a huge golden palace hall, light from tall windows, symbolic",
  "axe_to_blade|Symbolic scene: an old Frankish axe on the left and the slanted blade of a guillotine on the right, both hanging on a stone wall, warm light" + SEMTXT,
  f"napoleon_crown|{NAPOI.replace('a round', 'A round')}, raising a golden crown above his own head in a big cathedral, priests watching surprised",
  "revolution_crowd_cap|A round-white-head cartoon Parisian revolutionary in a red cap holding up a royal crown with a shocked face in front of a cheering crowd, 1793" + SEMTXT,
  f"general_podium|{GENERAL}, standing at a podium in a big hall of 1958 raising both arms, a crowd of round-white-head cartoon people applauding" + SEMTXT + SEMBAND)
b("Essa é a história inteira da França. Guarde esse machado: ele volta. E tudo começa numa terra que ainda nem se chamava França.",
  "map_france_hook|Map of today's France between the Atlantic Ocean, the English Channel, the Rhine, the Alps, the Mediterranean and the Pyrenees, painted soft blue, the neighbors pale beige, " + MAPA,
  "axe_kept|An old Frankish throwing axe resting on a wooden table by a window, a single beam of light falling on it, symbolic" + SEMTXT,
  "sword_crown|Symbolic scene: a golden crown resting on an old axe on a stone, warm light, nothing else" + SEMTXT,
  "gaul_landscape|A wide green landscape of hills, oak forests and a winding river in ancient Gaul, small round thatched huts with smoke, misty morning")

# ───────────────────────── 1. A GÁLIA ─────────────────────────
cap("1. Uma terra que não era um país")
b("Olhe para esse mapa há dois mil e cem anos. Dezenas de povos celtas, cada um com o seu chefe, os seus deuses e as suas brigas. Os romanos chamavam todos de gauleses, mas um país, aquilo não era.",
  "map_gaul_tribes|Map of ancient Gaul between the Atlantic Ocean, the Mediterranean Sea, the Rhine river and the Alps, divided into many small areas of different colors like a patchwork, " + MAPA,
  f"gaul_chiefs_argue|Several {GAUL} chiefs arguing loudly around a fire in a big thatched hall, pointing at each other, comic",
  "gaul_boar|Round-white-head cartoon Gaulish warriors roasting a boar on a fire and arguing about who gets the biggest piece, comic",
  "druid_oak|A round-white-head cartoon druid with a simple flat long white beard shape in a white robe cutting mistletoe from an oak tree with a golden sickle, villagers watching",
  "celtic_gods|A carved wooden statue of a Celtic god with antlers in a sacred forest clearing, Gaulish villagers leaving offerings, misty",
  f"gaul_village|A Gaulish village of round thatched huts inside a wooden palisade on a hill, {GAUL} training, pigs and children running, sunny",
  "gaul_tribes_map_close|Round-white-head cartoon Gaulish warriors of several different tribes with different colored shields shouting at each other across a small river, comic" + SEMBAND,
  card="séc. I a.C.")
b("Aí aparece um general romano com dívidas e ambição: Júlio César. Ele joga tribo contra tribo e, em seis anos, engole quase tudo. [curious] Depois escreve o relato da guerra ele mesmo, falando de si na terceira pessoa.",
  f"caesar_tent|{CESAR}, studying a big blank map on a table in a military tent, rubbing his hands, comic" + SEMTXT + "@@JÚLIO CÉSAR",
  "roman_camp|A big square Roman army camp with tents in rows and a wooden palisade on a hill in Gaul, smoke from fires, evening" + SEMBAND,
  f"legions_march|A long column of {LEG} marching on a road through the green hills of Gaul" + SEMBAND,
  f"caesar_tribes|{CESAR}, shaking hands with one Gaulish chief while secretly pointing a finger at another Gaulish chief behind his back, comic",
  "caesar_writing|A round-white-head cartoon Roman general, bald, with a laurel wreath writing on a scroll in his tent and smiling at himself in a small bronze mirror, comic" + SEMTXT,
  "caesar_debts|A round-white-head cartoon Roman general, bald, with a laurel wreath, looking at a very long unrolled bill with a nervous face, comic" + SEMTXT,
  card="58 a.C.")
b("§ Só no fim os gauleses se unem, atrás de um chefe jovem, Vercingetórix. Ele se tranca na fortaleza de Alésia. César cerca a colina com uma muralha para dentro e outra para fora. Imagine estar lá em cima: a comida acabando, e o socorro preso do outro lado.",
  f"vercingetorix|{VERC}, raising a sword in front of a crowd of {GAUL} who cheer with shields" + SEMBAND + "@@VERCINGETÓRIX",
  "alesia_walls|Aerial view of a hill fortress surrounded by two long rings of Roman wooden walls with towers and ditches, one ring facing in and one facing out, green countryside",
  "alesia_inside|Inside a Gaulish hilltop fortress: thatched huts, empty grain baskets, a thin dog and worried families, grey sky",
  "alesia_hunger|Round-white-head cartoon Gaulish warriors and families sitting tired and hungry on the walls of a hilltop fortress looking down at Roman camps, sunset",
  "caesar_tower|A round-white-head cartoon Roman general, bald, with a laurel wreath standing on a wooden tower looking at the hill fortress with a satisfied face",
  "relief_army|A huge Gaulish relief army on the horizon stopped by Roman walls with sharp stakes, Roman legionaries on towers" + SEMBAND,
  "vercingetorix_walls|A round-white-head cartoon young Gaulish chief with a red cloak standing on the walls of a hilltop fortress looking at the Roman walls below, worried",
  "stakes|Close view of rows of sharp wooden stakes and deep ditches in front of a Roman wooden wall with a tower, cloudy sky",
  card="52 a.C.")
b("Vercingetórix se rende. E aqui está o paradoxo: a derrota cria a base da França. Roma traz estradas, cidades e o latim. [curious] O francês descende da língua de César, e o português que você fala também.",
  f"surrender|{VERC}, laying his sword at the feet of {CESAR} sitting on a chair in front of the legions" + SEMBAND,
  "roman_gaul_city|A Roman city in Gaul with a stone amphitheater, a temple with columns, a long stone aqueduct and paved roads, sunny",
  "latin_school|A round-white-head cartoon Roman teacher in a toga teaching Gaulish children in checked trousers in a stone courtyard" + SEMTXT,
  "roman_road|A straight paved Roman road through the green fields of Gaul with a milestone, a cart and travelers, sunny" + SEMTXT,
  "lutetia|The small Roman town of Lutetia on an island in the river Seine with a few stone buildings, a wooden bridge and boats, green fields around")
b("Mas o império envelhece. No século cinco, povos germânicos atravessam o Reno. E alguém vai ter que mandar nessa terra.",
  "rhine_crossing|Columns of round-white-head cartoon Germanic warriors and families with wagons crossing a wide river into a Roman province, Roman fort abandoned on the bank" + SEMBAND,
  "germanic_wagons|Germanic families with ox wagons and cattle moving along a broken Roman road in Gaul, a ruined milestone, autumn" + SEMTXT,
  "roman_ruins|A Roman villa in Gaul with a collapsed roof and grass growing in the courtyard, crows on a broken column, grey sky")

# ───────────────────────── 2. CLÓVIS ─────────────────────────
cap("2. Um rei que escolheu o deus certo")
b("Reims, por volta do ano quinhentos. Clóvis, o do machado, entra numa igreja para ser batizado pelo bispo Remígio. Repare na escolha: os outros reis germânicos eram cristãos de outra vertente, a ariana, que os bispos chamavam de heresia.",
  f"reims_baptism|{CLOVIS} kneeling in a big stone baptismal font inside an early medieval church in Reims while {BISPO} pours water on his head, candles, warriors watching",
  "reims_church|A big early medieval stone church in the city of Reims with Roman walls around it, crowds of round-white-head cartoon people arriving, morning",
  "remi_blessing|A round-white-head cartoon old bishop with a simple flat white beard shape and a white mitre raising his hand to bless a kneeling Frankish king, candles and incense" + "@@REMÍGIO",
  "frankish_warriors_church|Round-white-head cartoon Frankish warriors with long hair waiting outside a stone church in Reims, some curious, some bored, comic" + SEMBAND,
  "heresy_debate|Two round-white-head cartoon early medieval bishops in white mitres arguing angrily with a Germanic priest over an open book, comic" + SEMTXT,
  f"arian_kings|Two round-white-head cartoon Germanic kings in different crowns looking jealous at a third king being baptized in the distance, comic",
  card="c. 500")
b("Clóvis vira católico, como os bispos e o povo que ele governava. Então os bispos, que tinham a única administração que sobrou de Roma, passam a trabalhar para ele.",
  "bishops_clerks|Round-white-head cartoon early medieval bishops and clerks writing on parchments in a stone office, a Frankish king nodding behind them" + SEMTXT,
  f"clovis_map|{CLOVIS} placing his hand on a big map of Gaul painted orange from the north to the Pyrenees, warriors cheering",
  "map_franks|Map of Gaul with a large orange area growing from the north toward the Pyrenees mountains, the Atlantic Ocean and the Mediterranean Sea, " + MAPA)
b("[curious] Quem conta essa história, e a do vaso, é um bispo, Gregório de Tours, quase cem anos depois. Bispo nenhum ia perder um rei tão bom de propaganda.",
  "gregory_writes|A round-white-head cartoon early medieval bishop with a simple flat white beard shape writing a big book by candlelight in a stone room, smiling slyly" + SEMTXT + "@@GREGÓRIO DE TOURS",
  "book_drawing|An open medieval book on a wooden desk showing only one big colorful drawing of a golden vase, the rest of the pages completely blank, a candle" + SEMTXT)
b("§ Séculos depois, um arcebispo de Reims espalha uma lenda: no batismo de Clóvis, uma pomba desceu do céu com um frasco de óleo. É a Santa Ampola. Com ela, quase todo rei francês vai ser ungido em Reims, como Clóvis.",
  "dove_ampoule|A white dove flying down from a beam of light in an old church carrying a tiny glass bottle in its beak, a bishop looking up amazed, golden light",
  "ampoule_close|Close view of a tiny old glass bottle with golden oil inside a golden reliquary on a velvet cushion, candles, symbolic" + SEMTXT,
  "anointing|A round-white-head cartoon medieval king kneeling in a huge Gothic cathedral while an archbishop puts a drop of holy oil on his forehead, crowds watching")
b("[curious] E tem mais: o nome Clóvis, em latim, virou Luís. A contagem dos reis Luís da França chega a dezoito. Imagine o drama de um professor de história com tanto Luís.",
  "louis_line|A comic long line of round-white-head cartoon French kings of different centuries all wearing crowns, waiting in a queue, a confused cartoon teacher counting them" + SEMTXT,
  "teacher_desk|A round-white-head cartoon modern history teacher scratching his head in front of a blackboard covered only with many little drawings of crowns, comic" + SEMTXT)
b("Só que os francos tinham um costume: o reino era dividido entre os filhos, como herança de fazenda. E irmão com reino vizinho não fica em paz por muito tempo.",
  "kingdom_split|A comic symbolic scene: an old Frankish king cutting a big round cake shaped like a map into four pieces for four sons who stare at each other jealously" + SEMTXT,
  "brothers_fight|Four round-white-head cartoon Frankish princes with long hair fighting with swords and shields in a muddy field, comic" + SEMBAND + SANG)

# ───────────────────────── 3. CARLOS MAGNO ─────────────────────────
cap("3. Um império que coube numa vida")
b("Depois de séculos de briga, uma família junta tudo de novo. Roma, Natal do ano oitocentos: o papa põe uma coroa de imperador na cabeça de Carlos Magno.",
  f"charlemagne_crowned|{CMAGNO} kneeling in front of the altar of a huge old basilica in Rome while the Pope places a crown on his head, Christmas candles" + "@@CARLOS MAGNO",
  "rome_basilica|A huge old basilica in Rome with a long nave of columns full of round-white-head cartoon nobles and priests on Christmas night",
  f"charlemagne_throne|{CMAGNO}, sitting on a simple stone throne in a palace chapel with an octagonal dome, advisers around him",
  card="800")
b("O império dele vai dos Pirineus até o meio da Alemanha. [curious] Ele mal sabia escrever e, segundo o biógrafo dele, guardava tabuinhas debaixo do travesseiro para treinar as letras. Repare no rei de copas do baralho francês: ele tem nome, Charles. É ele.",
  "map_charlemagne|Map of Western Europe with a big empire painted golden from the Pyrenees mountains to central Germany and northern Italy, " + MAPA,
  "playing_card|Close view of a big old French playing card showing a king of hearts with a white beard and a crown, red hearts in the corners, on a wooden table" + SEMTXT,
  "wax_tablets|A round-white-head cartoon old emperor with a simple flat long white beard shape in bed at night secretly practicing letters on a small wax tablet, a candle, comic" + SEMTXT,
  f"charlemagne_horse|{CMAGNO} riding a big white horse at the head of an army of knights through a forest" + SEMBAND)
b("§ Só que o costume franco volta. Em oitocentos e quarenta e três, em Verdun, os netos dele cortam o império em três fatias. A do oeste vai virar a França. A do leste, a Alemanha. E a do meio, motivo de briga por mil anos.",
  "verdun_treaty|Three round-white-head cartoon young medieval kings sitting at a long table signing a parchment, looking suspiciously at each other" + SEMTXT,
  "map_verdun|Map of Western Europe split into three long vertical bands: a blue band in the west, a yellow band in the middle and a red band in the east, " + MAPA,
  "middle_slice|Symbolic scene: two round-white-head cartoon medieval kings pulling the same long middle slice of a map-shaped cake in opposite directions, comic" + SEMTXT,
  card="843")
b("E a fatia do oeste nasce fraca. Os vikings sobem os rios e saqueiam até Paris. O rei não consegue defender ninguém, então cada senhor ergue o próprio castelo. Se você morasse ali, quem ia te proteger era o senhor do castelo, não um rei distante. E quem tem castelo não obedece rei.",
  f"vikings_seine|Viking longships with striped sails rowing up the river Seine toward a small island town with wooden walls, villagers running" + SEMBAND,
  "paris_siege_vikings|Round-white-head cartoon Parisians defending wooden walls and a bridge against Vikings with axes, 9th century, smoke" + SEMBAND,
  "castle_motte|A small wooden castle on top of a round earth mound with a palisade, a proud round-white-head cartoon lord with arms crossed at the gate",
  card="885")

# ───────────────────────── 4. OS CAPETOS ─────────────────────────
cap("4. O rei que mandava numa ilha")
b("Ano novecentos e oitenta e sete. Os grandes senhores escolhem um rei: Hugo Capeto. Imagine o reino dele: uma faixa entre Paris e Orléans. Muito duque mandava mais do que o rei.",
  f"hugh_elected|{HUGO} being raised on a shield by a group of powerful round-white-head cartoon nobles in fur cloaks, looking a little nervous" + SEMBAND + "@@HUGO CAPETO",
  "map_capet|Map of the land of France around the year 1000 with only a small blue patch around Paris and Orléans and big areas of other colors around it, " + MAPA,
  f"dukes_laugh|Round-white-head cartoon rich medieval dukes in big castles laughing at a small king with a little crown standing on a tiny island in a river, comic",
  card="987")
b("Mas os Capetos tinham uma arma secreta: filhos homens. Por mais de trezentos anos, cada rei deixou um filho vivo para herdar. [curious] Tente achar outra família real da época com essa sorte.",
  "father_son|A round-white-head cartoon old medieval king proudly crowning his young son while he is still alive, in a church, nobles watching",
  "royal_cradles|A comic line of royal cradles with tiny baby crowns over each one in a castle room, a proud medieval king smiling",
  "family_tree|A painted family tree on an old wall with small round portraits of crowned kings connected by golden branches, all in one straight line" + SEMTXT)
b("§ Só que, em mil cento e cinquenta e dois, uma mulher muda o mapa. Leonor da Aquitânia se separa do rei da França e casa com Henrique, que logo vira rei da Inglaterra. De repente, o rei inglês tem mais terra na França do que o próprio rei francês.",
  f"eleanor|{LEONOR} walking out of a French castle with her head held high while a sad young French king watches from a window@@LEONOR DA AQUITÂNIA",
  f"eleanor_henry|{LEONOR} and a round-white-head cartoon young English king with a simple flat short red beard shape getting married in a cathedral",
  "map_angevin|Map of France in the 12th century with a huge red area covering the whole west from the north coast to the Pyrenees and a small blue area around Paris, " + MAPA,
  card="1152")
b("O filho do rei traído, Filipe Augusto, toma de volta a Normandia e, em Bouvines, derrota ingleses e alemães juntos. Ele já não assina rei dos francos. Assina rei da França. Mas os ingleses não tinham desistido.",
  f"philip_bouvines|{FELIPE} on a horse in the middle of a big medieval battle on a summer field, knights charging" + SEMBAND + "@@FILIPE AUGUSTO",
  "seal_change|A medieval clerk pressing a big wax seal on a parchment in a royal office, a king watching proudly" + SEMTXT,
  "english_angry|A round-white-head cartoon medieval English king with a crown stamping his foot angrily on a cliff looking across the sea at France, comic",
  card="1214")

# ───────────────────────── 5. A GUERRA DOS CEM ANOS ─────────────────────────
cap("5. Uma guerra do tamanho de três gerações")
b("Mil trezentos e vinte e oito. O último Capeto direto morre sem filho, e o rei da Inglaterra, sobrinho dele, quer a coroa. Os nobres franceses dizem não. Então começa a Guerra dos Cem Anos. Pense nisso: uma guerra que começa com o seu bisavô e acaba com o seu bisneto.",
  "dead_king_no_son|A round-white-head cartoon French king lying in state on a bed with candles around him, nobles whispering and looking at an empty cradle",
  "crown_tug|Two round-white-head cartoon medieval kings, one in a blue cloak with gold lilies and one in a red cloak with gold lions, pulling the same crown in opposite directions, comic" + SEMTXT,
  "generations|A comic symbolic scene: a medieval great-grandfather, grandfather, father and little son all in armor standing in a line, each one older than the next, all with the same sword",
  card="1337")
b("Mas ela começa como um desastre para a França. Em Crécy, os arqueiros ingleses derrubam a cavalaria francesa. Aí chega a Peste Negra e mata talvez um terço do país. Em Azincourt, de novo, os cavaleiros afundam na lama.",
  f"crecy|{INGL} shooting a cloud of arrows at {CAVF} falling from their horses on a hillside" + SEMBAND,
  "black_death|A medieval French town street with closed doors marked with simple crosses, a cart, a doctor with a long beak mask walking alone, gloomy" + SEMTXT,
  f"agincourt_mud|{CAVF} stuck in deep mud on a rainy field, struggling and falling, English archers in the distance" + SEMBAND,
  card="1346")
b("Em mil quatrocentos e vinte, um tratado entrega a França ao rei inglês. Metade do país obedece Londres. O herdeiro francês, Carlos, não consegue nem ser coroado: Reims está nas mãos do inimigo.",
  "map_1420|Map of France in 1420 with the whole north painted red, a red area in the southwest, and a small blue area in the center and south, " + MAPA,
  f"dauphin_sad|{CARLOS7} sitting sad and alone in a cold castle hall without a crown, looking out the window",
  card="1420")
b("§ Aí aparece uma camponesa de dezessete anos, Joana. Ela diz que ouve vozes de santos. Veste armadura, ajuda a libertar Orléans e leva Carlos até Reims. Ali, onde Clóvis foi batizado, ele é ungido rei.",
  f"joan_voices|{JOANA.replace('in shining plate armor holding a plain white banner', 'in a simple red peasant dress')} in a field with sheep, looking up at a beam of golden light from the clouds" + "@@JOANA D'ARC",
  f"joan_orleans|{JOANA} on a white horse leading French soldiers to attack an English wooden fort by a river" + SEMBAND,
  f"reims_coronation|{CARLOS7} kneeling in front of the altar of the huge Gothic cathedral of Reims being crowned, {JOANA} standing behind him with her banner",
  card="1429")
b("Os ingleses capturam Joana e a queimam em Ruão. Mas, em mil quatrocentos e cinquenta e três, saem da França, menos de Calais.",
  "rouen_tower|A medieval stone tower in the city of Rouen at dusk, a small white banner on the ground in front of it, symbolic, sad",
  "english_leave|English soldiers boarding ships in a French harbor and leaving, round-white-head cartoon French townspeople watching from the walls" + SEMBAND,
  card="1453")
b("E aqui está a primeira peça da resposta. Para vencer, o rei ganha imposto fixo e um exército só dele. A França sobreviveu porque juntou tudo numa coroa. O problema é que uma coroa só não une uma fé dividida.",
  "piece_one|A big golden puzzle piece being placed into a puzzle that shows a small blue map of France with a crown in the middle, symbolic" + SEMTXT,
  "royal_army|A long line of French soldiers of the 15th century in matching blue uniforms marching in front of a royal castle" + SEMBAND,
  "tax_chest|A round-white-head cartoon royal tax collector filling a big iron chest with coins in a village square, peasants grumbling" + SEMTXT)

# ───────────────────────── 6. GUERRAS DE RELIGIÃO ─────────────────────────
cap("6. Paris bem vale uma missa")
b("Paris, agosto de mil quinhentos e setenta e dois. A cidade está em festa: uma princesa católica casa com Henrique de Navarra, um dos chefes dos protestantes, os huguenotes. Seis dias depois, na noite de São Bartolomeu, os sinos tocam.",
  "royal_wedding|A royal wedding in front of the Notre-Dame cathedral in Paris in 1572, a round-white-head cartoon princess and a young prince with a simple flat beard shape, crowds celebrating",
  f"huguenots_guests|{HUG} arriving happily in Paris for a wedding, carrying gifts, unaware",
  "night_bells|The bell tower of a church in Paris at night ringing, dark streets below, ominous moonlight",
  card="1572")
b("[serious] Imagine acordar com esses sinos. Católicos matam milhares de protestantes, primeiro em Paris, depois pelo país. Somando tudo, são mais de trinta anos de guerra em que o inimigo pode ser o seu vizinho.",
  "night_massacre|Dark narrow streets of Paris at night with torches, round-white-head cartoon people running and hiding in doorways, white crosses painted on doors, dramatic" + SANG,
  "neighbors_war|Two round-white-head cartoon French neighbors of the 1570s glaring at each other over a fence, one holding a rosary and one holding a black book, comic but tense" + SEMTXT)
b("§ Aí o trono cai no colo justamente de Henrique, o protestante. Só que Paris, católica, não abre as portas. Então ele se converte, e a tradição põe na boca dele uma frase: [curious] Paris bem vale uma missa.",
  f"henry_gates|{HENR4} on horseback in front of the closed gates of Paris with an army behind him, Parisians on the walls shaking their fists" + SEMBAND + "@@HENRIQUE IV",
  f"henry_mass|{HENR4} kneeling in a church taking communion, with a tiny sly smile, comic",
  card="1593")
b("Com o Édito de Nantes, ele dá liberdade aos protestantes em várias cidades, e, conta-se, queria que todo camponês tivesse uma galinha na panela no domingo. Mas um fanático o mata a facadas. E os nobres voltam a desafiar a coroa.",
  "edict|A round-white-head cartoon king signing a big parchment with a red seal while a Catholic priest and a Protestant pastor shake hands awkwardly, comic" + SEMTXT,
  "chicken_pot|A happy round-white-head cartoon French peasant family of 1600 around a pot with a chicken on a Sunday table, a small cottage, warm light",
  "carriage_street|A royal carriage stopped in a narrow crowded street in Paris in 1610, a man in a dark cloak running away, guards shouting" + SANG,
  card="1598")

# ───────────────────────── 7. LUÍS XIV ─────────────────────────
cap("7. O rei que virou o Estado")
b("Paris, uma noite de mil seiscentos e quarenta e nove. Com a cidade revoltada, a família real foge às escondidas. No meio dela, um menino de dez anos: Luís, o Décimo Quarto. Repare nesse menino. Ele nunca vai esquecer essa noite.",
  "night_escape|A royal family escaping from a Paris palace at night in a dark carriage, a round-white-head cartoon boy king of ten looking back worried through the window",
  "fronde_barricade|Barricades in narrow Paris streets in 1648 with round-white-head cartoon Parisians and nobles in feathered hats shouting" + SEMBAND,
  f"boy_king|A round-white-head cartoon boy king of ten with long brown curly hair and a small crown frowning seriously on a big throne" + "@@LUÍS XIV",
  card="1649")
b("Então, adulto, ele constrói Versalhes, e põe os nobres para morar lá, perto dos olhos dele. Imagine o duque mais poderoso do reino disputando a honra de segurar a camisa do rei de manhã.",
  "versailles|The palace of Versailles seen from the gardens with long fountains, geometric flower beds and a huge golden facade, sunny",
  f"king_lever|{LUIS14} sitting on a big bed in a golden bedroom while {NOBRES} compete to hand him his shirt and shoes, comic",
  "hall_mirrors|The Hall of Mirrors of Versailles with huge chandeliers, golden statues and tall mirrors, round-white-head cartoon courtiers bowing",
  card="1682")
b("Ele reina setenta e dois anos e usa salto alto vermelho. [curious] A frase o Estado sou eu ele provavelmente nunca disse, mas ela resume o reinado. Só que ele proíbe os protestantes, uns duzentos mil fogem, e ele faz guerra atrás de guerra.",
  "red_heels|Close view of elegant shoes with red heels and big buckles stepping on a marble floor, the hem of a blue cloak with gold lilies, comic" + SEMTXT,
  f"sun_king|{LUIS14}, posing proudly with one hand on his hip in front of a golden sun emblem on the wall" + SEMTXT,
  "huguenots_flee|Round-white-head cartoon Protestant families with carts of furniture and tools leaving a French town by the road at dawn, sad",
  card="1685")
b("§ E aqui está a segunda peça da resposta. Quando tudo gira em volta de um homem, a culpa também ganha um endereço só. Só que o Estado que podia tudo estava ficando sem dinheiro.",
  "piece_two|A second golden puzzle piece placed next to the first, showing a golden palace with a single crown on top, symbolic" + SEMTXT,
  "empty_treasury|A huge royal treasury room with only a few coins left at the bottom of big open chests, a worried round-white-head cartoon minister with a candle" + SEMTXT)

# ───────────────────────── 8. A REVOLUÇÃO ─────────────────────────
cap("8. O preço do pão")
b("Julho de mil setecentos e oitenta e oito. Uma chuva de granizo destrói as colheitas, e vem um inverno gelado. Na primavera, o pão come mais da metade do salário de um trabalhador de Paris. Imagine gastar metade do que você ganha só no pão.",
  f"hailstorm|A violent hailstorm destroying golden wheat fields, {CAMPF} running for shelter, dark sky" + SEMMOD,
  "frozen_seine|The river Seine frozen in Paris in winter 1789 with round-white-head cartoon people walking on the ice, snow on old roofs",
  "bread_line|A long line of round-white-head cartoon hungry Parisian women in bonnets in front of a bakery with an empty window, cold morning" + SEMTXT,
  card="1788")
b("O rei, Luís Dezesseis, falido também por ter pago a guerra da independência americana, convoca os Estados Gerais. Em julho de mil setecentos e oitenta e nove, Paris toma a Bastilha. [curious] Lá dentro havia sete presos.",
  f"louis16|{LUIS16}, looking worried at a huge pile of bills on a desk in Versailles" + SEMTXT + "@@LUÍS XVI",
  f"bastille|{SANSC} storming the tall stone towers of the Bastille fortress with smoke and a crowd, July 1789" + SEMMOD,
  "seven_prisoners|Seven confused round-white-head cartoon prisoners in old clothes walking out of a dark prison gate into a cheering crowd, comic",
  card="1789")
b("§ Dois anos depois, o rei tenta fugir disfarçado. Conta-se que um funcionário do correio o reconhece pelo rosto impresso numa nota de dinheiro. [serious] Lembra da nossa pergunta? Agora ela fica difícil: o rei virou suspeito.",
  f"varennes|A dark carriage stopped at night in a small French village by round-white-head cartoon villagers with lanterns, a chubby man in a plain servant's coat trying to hide his face",
  "banknote_face|Close view of an old paper banknote with only a small oval portrait of a chubby man in a wig, held next to the face of the same man in a carriage, comic" + SEMTXT,
  card="1791")
b("Em janeiro de mil setecentos e noventa e três, a lâmina desce sobre Luís Dezesseis. Lembra do machado de Soissons? Agora ele cai sobre o rei. E, em Reims, um revolucionário quebra a Santa Ampola em praça pública.",
  "guillotine_close|A tall guillotine on a wooden scaffold under a cold January sky in Paris, soldiers with drums around it, a silent crowd, symbolic" + SANG,
  "axe_returns|The old Frankish throwing axe from the beginning resting on a wooden table next to a small model of a guillotine, a beam of light, symbolic" + SEMTXT,
  "ampoule_broken|A round-white-head cartoon revolutionary in a red cap smashing a tiny glass bottle on the stone base of a statue in a square of Reims, a crowd watching, the cathedral behind",
  card="1793")
b("Vem o Terror: milhares de guilhotinados. Os revolucionários inventam até o metro e o quilo. Você compra arroz por quilo por causa deles. Mas, sem rei, quem ia pôr ordem nisso tudo?",
  "terror_tribunal|A revolutionary tribunal in a dark hall with stern judges in tricolor sashes and a frightened prisoner, papers everywhere" + SEMTXT,
  "meter_bar|Round-white-head cartoon French scientists of the 1790s measuring a long metal bar and weighing a small metal cylinder on a scale in a laboratory" + SEMTXT,
  "rice_market|A round-white-head cartoon Brazilian shopper in a modern supermarket holding a bag of rice and looking at a kitchen scale, comic" + SEMTXT)

# ───────────────────────── 9. NAPOLEÃO E O SÉCULO XIX ─────────────────────────
cap("9. O trono que nunca ficou vazio")
b("Então aparece um general da Córsega, Napoleão Bonaparte, que dá um golpe em mil setecentos e noventa e nove. Cinco anos depois, em Notre-Dame, com o papa ao lado, ele mesmo põe a coroa na cabeça. [curious] O papa veio de Roma para assistir.",
  f"napoleon_coup|{NAPO}, standing confidently in a crowded hall of politicians in 1799, soldiers with bayonets at the door" + SEMMOD + "@@NAPOLEÃO",
  f"notre_dame_coronation|{NAPOI} crowning himself in the huge Gothic Notre-Dame cathedral, the Pope sitting behind him looking surprised, nobles watching",
  "pope_travel|A round-white-head cartoon Pope in white robes in a carriage on a long muddy road through France, looking tired, comic",
  "pope_shrug|A round-white-head cartoon Pope in white robes sitting with his hands open and a resigned face, comic",
  card="1804")
b("Ele cria o Código Civil e põe um chefe nomeado por Paris, o prefeito, em cada canto do país. Em mil oitocentos e sete, invade Portugal, e a corte portuguesa foge… para o Brasil. Você conhece o resto.",
  "code_civil|A big heavy law book on a desk in a French office of 1804 with clerks copying it by candlelight" + SEMTXT,
  "prefects|Round-white-head cartoon French officials in dark coats with sashes arriving in many small towns of France by carriage" + SEMTXT,
  "court_flees|Portuguese royal ships leaving the port of Lisbon in a hurry in 1807, round-white-head cartoon nobles carrying chests, French soldiers on a hill" + SEMBAND,
  card="1807")
b("§ Napoleão cai em Waterloo. E aqui está a terceira peça da resposta. Os franceses cortaram a cabeça do rei, mas guardaram a máquina que ele montou. E o trono vazio sempre achava alguém: os reis voltam, caem de novo em mil oitocentos e trinta e em mil oitocentos e quarenta e oito, e um sobrinho de Napoleão vira imperador.",
  "waterloo|A big battle on a muddy field in Belgium in 1815 with French cavalry charging lines of British soldiers in red coats, smoke" + SEMBAND,
  "piece_three|A third golden puzzle piece fitting into a puzzle that shows an empty throne with a line of different people waiting to sit on it, symbolic" + SEMTXT,
  "throne_carousel|A comic symbolic scene: a golden throne on a carousel with a king, a man in a red cap, an emperor and another king taking turns sitting on it" + SEMTXT,
  f"napoleon3|{NAP3}, standing proudly in front of new wide Paris boulevards with stone buildings" + "@@NAPOLEÃO III",
  card="1815")
b("Só que esse sobrinho vai à guerra contra a Prússia e é capturado em Sedan. No cerco de Paris, os parisienses chegam a comer os elefantes do zoológico. Em mil oitocentos e setenta e um, os alemães proclamam o império deles no Salão dos Espelhos, em Versalhes. O vizinho do outro lado da fatia agora era um gigante.",
  f"sedan|{NAP3} surrendering his sword to {PRUS} in a field, smoke in the distance" + SEMBAND,
  "mirrors_german|The Hall of Mirrors of Versailles full of {PRUS} raising swords and cheering, a round-white-head cartoon German emperor with a big white beard shape in the middle".replace("{PRUS}", PRUS) + SEMBAND,
  "zoo_elephant|A sad elephant in an empty Paris zoo enclosure in the snowy winter of 1870, round-white-head cartoon hungry Parisians in coats looking at it, gloomy",
  "map_alsace|Map of France and Germany in 1871 with France in blue and Germany in grey and the region of Alsace and Lorraine in the east colored grey with a dark outline, " + MAPA,
  card="1871")

# ───────────────────────── 10. AS GUERRAS E A QUINTA REPÚBLICA ─────────────────────────
cap("10. Do Salão dos Espelhos ao general")
b("Verdun, mil novecentos e dezesseis: a mesma cidade do tratado dos netos de Carlos Magno, na mesma fronteira mal resolvida. Imagine dez meses de bombardeio numa trincheira. A França sai vencedora, e o tratado de paz é assinado… no mesmo Salão dos Espelhos.",
  f"verdun_trench|{POILU} in a muddy trench under a grey sky with shell craters and broken trees behind" + SEMBAND + SANG,
  "verdun_moon|A landscape of mud full of shell craters and broken tree trunks like the surface of the moon, grey sky, no people",
  "treaty_1919|Round-white-head cartoon diplomats in dark suits signing a treaty at a long table in the Hall of Mirrors of Versailles in 1919, photographers" + SEMTXT,
  card="1916")
b("Vinte e um anos depois, os alemães voltam e tomam a França em seis semanas. Pense: seis semanas. Um marechal velho governa o que sobrou, colaborando com Berlim. E um general quase desconhecido fala pelo rádio, de Londres: [slightly dramatic] a chama da resistência francesa não vai se apagar.",
  "tanks_france|German tanks of 1940 rolling through a French village road past a church, frightened villagers" + SEMBAND,
  "old_marshal|A round-white-head cartoon very old French marshal with a simple flat white mustache shape and a kepi sitting stiffly at a desk in a hotel room" + SEMTXT,
  f"bbc_radio|{GENERAL} speaking into a big old microphone in a London radio studio of 1940" + SEMTXT,
  card="1940")
b("§ Em mil novecentos e quarenta e quatro, Paris é libertada. E, em mil novecentos e cinquenta e oito, esse general, De Gaulle, cria a Quinta República: um presidente com tanto poder que os próprios franceses falam em monarca republicano.",
  "paris_liberation|A joyful crowd of round-white-head cartoon Parisians celebrating in a big avenue in August 1944 with soldiers on jeeps, flowers thrown" + SEMTXT,
  f"de_gaulle_1958|{GENERAL}, now in a dark civilian suit, standing in a golden palace hall while officials bow politely" + SEMTXT + "@@DE GAULLE",
  "crown_shadow|A round-white-head cartoon president in a dark suit standing in front of a wall where his shadow wears a crown, symbolic, comic" + SEMTXT,
  card="1958")
b("Desde então, o Brasil já trocou de Constituição duas vezes. A França continua com a mesma, remendada. E o vizinho da fatia do leste virou o sócio da Europa.",
  "two_constitutions|A comic symbolic scene: a round-white-head cartoon man holding two thick books in one hand and a single old book in the other hand, comparing them" + SEMTXT,
  "handshake|A round-white-head cartoon French president and a German chancellor of 1963 shaking hands warmly in a palace, symbolic" + SEMTXT + SEMBAND)

# ───────────────────────── FECHO (≤ 45 s) ─────────────────────────
cap("Fecho")
b("§ E a resposta da nossa pergunta: o machado de Clóvis criou uma coroa que juntou tudo. Por isso, quando a lâmina cortou a cabeça do rei, a máquina continuou de pé, procurando alguém para sentar no trono.",
  "axe_final|The old Frankish throwing axe from the beginning resting next to a small golden crown on a wooden table by a window looking at Paris at dusk, symbolic" + SEMTXT,
  "piece_final|A finished golden puzzle showing the whole story of France from a Gaulish village to the Eiffel Tower, symbolic" + SEMTXT,
  "throne_waiting|An empty golden throne with gold lily flowers in a dark hall with a single beam of light on it and a long shadow of a person approaching, symbolic")
b("[warm] Talvez a pergunta nunca tenha sido como os franceses se livraram dos reis. E sim por que eles sempre quiseram alguém mandando tanto.",
  "paris_sunset|Paris at sunset seen from above with the Seine, the Notre-Dame cathedral and the Eiffel Tower in warm light, peaceful")
b("E para você: qual foi o momento em que a França podia ter virado outra coisa? Conta aí nos comentários.",
  f"guide_comment|{GUIA} sitting on a stone bench by the Seine in Paris, holding a small old axe and looking at it thoughtfully" + SEMTXT,
  "reims_cathedral|The huge Gothic cathedral of Reims at dusk with warm lights, round-white-head cartoon people walking in front")

# Grafia para a VOZ (o Fish lê como português). Conferir no teste de nomes (qa/pronuncia/).
# blocos.json leva "texto" (falado, vai ao Fish) e "tela" (grafia correta: legendas e SCRIPT).
FALA = [("Soissons", "Suassôn"), ("Clóvis", "Clóvis"), ("Remígio", "Remígio"), ("Vercingetórix", "Vercingetórix"),
        ("Alésia", "Alézia"), ("Reims", "Rrãns"), ("Verdun", "Verdân"), ("Capeto", "Capêto"), ("Capetos", "Capêtos"),
        ("Orléans", "Orleã"), ("Bouvines", "Buvíne"), ("Crécy", "Crecí"), ("Azincourt", "Azancúr"), ("Calais", "Calê"),
        ("Ruão", "Ruão"), ("Navarra", "Navárra"), ("Nantes", "Nânt"), ("Versalhes", "Versálhes"), ("Bastilha", "Bastílha"),
        ("Bonaparte", "Bonapárte"), ("Notre-Dame", "Notrrí Dâm"), ("Waterloo", "Uóterlu"), ("Sedan", "Sedã"),
        ("De Gaulle", "De Gól"), ("Córsega", "Córsega"), ("Leonor", "Leonôr")]
def fala(t):
    for a, z in FALA: t = re.sub(r"(?<![\wÀ-ú])" + re.escape(a) + r"(?![\wÀ-ú])", z, t)
    return t

IDEIA = set()
THUMB = None
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
        f"Pergunta central: {PERGUNTA}\n\n"
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
