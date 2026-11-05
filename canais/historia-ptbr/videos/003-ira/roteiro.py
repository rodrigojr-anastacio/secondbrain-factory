#!/usr/bin/env python3
"""Fonte única do 003-ira v2 (05/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

Molde History in Minutes (canais/historia-ptbr/biblia/roteiro.md e v2-amostras/ESTRUTURA-ROTEIRO.md):
  hook (anedota do cavalo de Dario: TESTE pedido pelo Rodrigo em 05/11) → "Essa é a história inteira do Irã" → promessa em lista
  → "guarde esse cavalo" → 10 eras ligadas por "mas… então…" (título-frase só na placa, nunca falado) → fecho que paga o cavalo
  e volta ao jardim de Ferdowsi. Fio condutor: a língua e o paraíso; fio secundário: o turbante contra a coroa.

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (nome/lugar que o espectador precisa guardar; com moderação)
Bloco: b(texto, *planos, card="559 a.C.") · texto que começa com "§ " abre ideia nova (~0,9 s antes) · capítulo: cap("3. Título-frase")
Voz (decisão do Rodrigo, 05/11): Fish drama-3, 1 chamada por bloco (técnica da amostra B2), gaps 0,35/0,9/1,5 s no build.py,
tags de tom só onde a emoção muda. Texto "contado": alterna pergunta, frase longa com vírgula de respiração e frase curta na virada.
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (amostra B2: ~125 ppm com as pausas)
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
TITULO = "A história INTEIRA do Irã"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None):
    ideia = t.startswith("§")
    B.append({"t": t.lstrip("§ ").strip(), "s": list(s), "card": card, "ideia": ideia})

# Personagens (descrição visual fixa; figuras modernas sem nome no prompt, o nome vai no rótulo do código)
MAPA = ("painted like a blank parchment terrain map seen from directly above, only coastlines, rivers, mountains and flat colored areas, "
        "completely blank with no writing anywhere, no letters, no words, no labels, no symbols, no compass, no border, no frame")
DARIO = "Darius, a round-white-head cartoon Persian nobleman with a simple flat black beard shape, a soft felt cap and a saffron robe"
DARIO_REI = "Darius the Great as a round-white-head cartoon king with a simple flat black beard shape, a tall golden crown and a saffron robe"
CIRO = "Cyrus the Great as a round-white-head cartoon king with a simple flat dark beard shape, a tall flat-topped golden crown and a purple robe"
SHAPUR = "Shapur I as a round-white-head cartoon king with a simple flat beard shape, a crown topped by a big round globe and fluttering ribbons"
FERD_M = "Ferdowsi as a round-white-head cartoon poet with a simple flat dark beard shape, a white turban and a simple blue robe"
FERD_V = "Ferdowsi as an old round-white-head cartoon poet with a simple flat white beard shape, a white turban and a simple blue robe"
ISMAIL = "a beardless round-white-head cartoon boy king wearing a white turban wrapped around a tall red cap"
NADER = "a round-white-head cartoon conqueror king with a simple flat black beard shape and a tall red four-peaked hat with a feather"
NASER = "a round-white-head cartoon shah with a huge curled black mustache shape, a black lambskin hat with a jewel and a dark frock coat"
REZA = "a tall round-white-head cartoon king in a 1930s military uniform with a peaked cap and a small grey mustache shape"
MOSSA = "an old bald round-white-head cartoon prime minister with a long nose and a grey suit"
XA = "a round-white-head cartoon shah with slicked-back grey hair and a military dress uniform with medals and a blue sash"
CLERIGO = "an old round-white-head cartoon cleric with a simple flat white beard shape, a black turban and a black cloak"
LIDER = "a round-white-head cartoon cleric with a simple flat grey beard shape, a black turban, big round glasses and a brown cloak"
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes"

# ───────────────────────── HOOK (teste: anedota do cavalo de Dario) ─────────────────────────
cap("Hook")
b("[curious] Pérsia, quinhentos e vinte e dois antes de Cristo. Seis nobres têm um problema: quem vai governar o maior império do mundo? A solução é… estranha.",
  "nobles_night|Six ancient Persian noblemen in long robes and soft felt caps arguing around a low table in a palace hall at night, oil lamps, worried faces",
  "empty_throne|An empty golden Achaemenid throne in a hall of stone columns at night, moonlight, a crown resting on the seat",
  "nobles_point|Six ancient Persian noblemen in felt caps all pointing at each other, comic argument, palace at night",
  "palace_lamps|Oil lamps flickering on carved stone columns of an ancient Persian palace at night, long shadows",
  "empire_vast|A vast ancient landscape from a mountain top: deserts, rivers, a far Egyptian pyramid on the left and snowy mountains on the right, morning haze", card="522 a.C.")
b("Ao nascer do sol, os seis vão sair a cavalo, e o dono do cavalo que relinchar primeiro vira rei.",
  "dawn_riders|Six Persian noblemen on horses waiting in a line outside a walled ancient city at dawn, the sun about to rise",
  "horse_ear|Close view of a white horse's head with ears up at dawn, a Persian rider's hand on the reins",
  "sun_rising|The sun rising over a rocky plain outside an ancient walled city, golden light, six tiny riders in silhouette",
  "nobles_waiting|Six ancient Persian riders glancing nervously at each other's horses at sunrise, comic suspense")
b("Um deles se chama Dario, e Dario tem um cavalariço esperto. Na noite anterior, ele leva o cavalo até aquele lugar exato, junto com uma égua.",
  f"darius_noble|{DARIO}, standing next to his white horse in a stable, confident@@DARIO",
  "groom_whisper|A clever ancient Persian stable groom with a small beard and a sly grin whispering a plan, in a stable at night, lantern light@@O CAVALARIÇO",
  "groom_night|An ancient Persian stable groom leading a white horse and a brown mare by ropes across a dark field outside a city wall at night, stars",
  "groom_grin|Close view of the sly ancient Persian stable groom grinning in the moonlight, finger on his lips, comic",
  "mare_tied|A brown mare tied to a stake in an empty field at night, the groom tiptoeing away, comic and sneaky")
b("De manhã, o cavalo passa por ali, sente o cheiro… e relincha.",
  "horse_sniff|A white horse with a Persian rider stopping in an empty field at sunrise and sniffing the air, curious",
  "mare_smell|Close view of a white horse nostrils flaring, sniffing the ground in the grass at dawn, comic",
  "horse_neigh|A white horse rearing and neighing loudly at sunrise while five other Persian noblemen on horses look shocked, mouths open")
b("[amazed] Dario vira rei de um império que ia do Egito até a fronteira da Índia. Um império escolhido, literalmente, por um cavalo. Pelo menos, é assim que Heródoto conta.",
  f"darius_crowned|{DARIO_REI}, sitting on a golden throne, smiling, his white horse peeking in through a palace door behind him@@DARIO I",
  "map_empire|Map of the ancient Persian empire stretching from Egypt and Anatolia to the Indus river, the empire painted in warm gold and the rest pale, " + MAPA,
  "horse_proud|A white horse wearing a small golden crown, standing proudly in a palace courtyard with stone columns, comic",
  "persian_bow|Five Persian noblemen bowing down before a man on a white horse at sunrise",
  "herodotus|An ancient Greek historian with a curly beard and a himation writing on a scroll at a desk, a white horse drawn in the margin, smug@@HERÓDOTO")
b("§ [serious] Essa é a história inteira do Irã. Um país invadido por gregos, árabes, mongóis e turcos, e que, toda vez, acabou ensinando os invasores a viver como persas.",
  "iran_landscape|Wide view of the Iranian plateau: a desert plain, snowy Zagros mountains behind, a turquoise dome of a mosque in a small oasis town",
  "conquerors_march|Four armies marching into a Persian valley one after the other: Greek hoplites with round shields, Arab horsemen with lances, Turkic horse archers, Mongol cavalry with fur hats",
  "conquerors_persian|A Greek hoplite, an Arab warrior, a Turkic soldier and a Mongol archer sitting on a red Persian carpet in a garden, now wearing Persian silk robes, drinking tea from small glasses and reading books of poetry, smiling",
  "tehran_today|Modern Tehran today with the tall Milad tower and the snowy Alborz mountains behind, a dense city with traffic@@TEERÃ, HOJE")
b("No caminho, tem um rei que devolvia os deuses dos vencidos, um imperador romano capturado vivo, o caixão de um poeta que salvou uma língua… e um contrato de tabaco que derrubou uma coroa, oitenta e oito anos antes de derrubar outra.",
  "gods_return|Babylonian priests happily carrying statues of their gods back into a temple in a joyful procession, a Persian king watching kindly",
  "valerian_kneel|An old Roman emperor in a purple cloak and laurel wreath kneeling before a Persian king on horseback with a globe crown, shocked",
  "coffin_light|A soft golden light glowing from the cracks of a closed plain wooden coffin in a dark room, mysterious",
  "tobacco_crown|A pile of tobacco leaves and a jeweled royal crown toppled over beside it on a wooden table, dramatic light",
  "kid_shocked|A Persian round-headed boy reading a big old book of stories by lamplight, mouth open in surprise",
  "two_crowns|Two royal crowns falling, an old jeweled Persian crown and a 20th century imperial crown, tumbling through the air, dramatic")
b("§ E o que esse cavalo tem a ver com o Irã de hoje? Guarde esse cavalo. Ele volta no final.",
  "horse_tehran|A white ancient Persian horse standing in a modern Tehran street at dusk, people walking by, surreal and curious",
  "horse_map|A white horse standing on top of a giant blank parchment map of Persia, looking forward into the future, magical light",
  "horse_wink|Close view of a white horse looking straight at the viewer with one eye winking, warm sunrise light, comic")

# ───────────────────────── 1. UM PARAÍSO NO DESERTO ─────────────────────────
cap("1. Um paraíso no deserto")
b("Mas, antes de qualquer rei, alguém precisou achar água. O planalto do Irã é uma tigela de montanhas, com deserto no meio e pouca chuva. Como é que se vive aqui?",
  "map_plateau|Simple illustrated map of the Iranian plateau ringed by mountains, the Zagros range on the west and the Alborz range in the north, two large pale deserts in the center, the Caspian Sea at the top and the Persian Gulf at the bottom, " + MAPA,
  "plateau_bowl|Wide aerial view of a high desert basin ringed by brown mountains, white salt flats shining in the middle",
  "dry_riverbed|A cracked dry riverbed in an Iranian desert valley, a single thorny bush, heat haze",
  "lut_desert|The Lut desert in Iran: giant wind-carved sand ridges under a burning sun, completely empty@@DESERTO DE LUT",
  "thirsty_traveler|An ancient Persian traveler with an empty water skin looking out over a dry desert under a hot sun, puzzled", card="c. 4200 a.C.")
b("Os antigos persas foram buscar a água embaixo da terra. São os qanats, túneis de quilômetros, tão bem inclinados que a água da montanha desce sozinha. Alguns correm há mais de dois mil anos.",
  "qanat_digger|Ancient Persian well diggers lowering a man into a deep vertical shaft with a wooden windlass and a rope, desert around",
  "qanat_tunnel|Inside a narrow underground tunnel dug in rock, a thin stream of clear water flowing along the floor, a digger holding an oil lamp",
  "qanat_cutaway|Cutaway illustration of a qanat: groundwater under a mountain, a long gently sloping underground tunnel with vertical shafts to the surface, water coming out into green fields of a desert village@@QANATS",
  "qanat_wells_aerial|Aerial view of a long line of round well mouths dotting the desert from the foot of the mountains to a green village, like a dotted line",
  "qanat_village|A green oasis village with orchards and wheat fields in the middle of a brown desert, water channels everywhere",
  "qanat_outlet|Clear water flowing out of a stone tunnel mouth into an irrigation channel in a desert village, children splashing")
b("Onde o túnel terminava, a água virava um jardim murado, que em persa antigo se chamava pairidaêza. Guarde essa palavra. Ela passou pelo grego, passou pelo latim… e chegou ao português como paraíso.",
  "persian_garden|A walled Persian garden with four water channels crossing in the middle, cypress and pomegranate trees and a small pavilion",
  "garden_wall|Ancient Persian gardeners building a high mud-brick wall around an orchard with pomegranate trees@@PAIRIDAÊZA",
  "xenophon|An ancient Greek traveler in a tunic walking amazed inside a lush walled Persian garden, looking up at the fruit trees",
  "roman_garden|A Roman scholar in a toga reading a scroll under a fig tree in a garden, a small fountain",
  "paradise_word|A Brazilian family today in a lush green garden, a child pointing at the flowers, bright sunny day@@PARAÍSO")
b("§ Só que os persas não foram os primeiros daqui. Em Susa, já tinha gente desde uns quatro mil e duzentos antes de Cristo: os elamitas, com uma escrita que ninguém conseguia ler… até dois mil e vinte e dois.",
  "susa_ancient|The ancient city of Susa on a hill at the edge of a green plain, mud-brick houses and a high temple platform, a river and palm trees@@SUSA",
  "elamite_king|An Elamite king with a round cap and a long braided beard, in a fringed robe, standing in a mud-brick temple courtyard@@OS ELAMITAS",
  "elamite_tablet|A clay tablet with only simple abstract dots and straight scratches (no real letters or characters), lying in a museum case",
  "susa_people|Ancient Elamite potters and farmers at work in the mud-brick streets of Susa, painted pottery with simple animal patterns",
  "scholar_puzzled|A scholar scratching his head in front of a clay tablet with strange marks under a glass dome, comic")
b("Uma equipe liderada por um arqueólogo francês decifrou boa parte dela. O primeiro povo desta história só voltou a falar agora.",
  "silver_beaker|An ancient silver beaker with rows of small incised geometric marks around it, lit in a museum case",
  "decipher_joy|A modern archaeologist with a beard jumping with joy in a museum storeroom holding up a photo of an ancient inscription@@DECIFRADO EM 2022",
  "desset_lab|A modern archaeologist with a beard studying photos of an ancient silver beaker on a laptop, a notebook full of sketched marks, plain walls with no posters and no writing anywhere",
  "elamite_speak|A ghostly ancient Elamite figure rising from a clay tablet and opening his mouth to speak, a modern scholar listening, magical")
b("§ Por volta de mil e quinhentos antes de Cristo, chegou gente nova do norte, e ela trouxe… um nome. Eles se chamavam de árias, os nobres, e a terra deles virou a terra dos árias: o Irã.",
  "steppe_riders|A group of Bronze Age herders with horses, ox wagons and cattle coming down from northern grasslands into the mountains of Iran",
  "airya_proud|An ancient Iranian tribal leader in a felt cap and wool tunic speaking proudly to his people around a fire@@ÁRIA = NOBRE",
  "map_iran_name|Map of the Iranian plateau glowing in warm golden light as one land, mountains around it, the Caspian Sea above and the Persian Gulf below, " + MAPA, card="c. 1500 a.C.")
b("E por que o mundo diz Pérsia? Porque é um apelido grego, tirado de uma província do sul, Pars. Guarde isso, porque daqui a mais de três mil anos um rei vai pedir ao mundo que largue o apelido.",
  "greek_geographer|An ancient Greek geographer in a himation drawing on a scroll and pointing at one southern region, smug@@APELIDO GREGO",
  "map_pars|Map of Iran with one southern province by the Persian Gulf highlighted in gold and the rest pale, " + MAPA,
  "pars_province|A fertile plain in southern Iran with villages and a river below the Zagros hills, seen from above@@PARS",
  "future_king|A ghostly vision in the clouds of a stern 1930s king in military uniform, floating above ancient herders on a hill")
b("E foi de Pars que saiu o homem que juntou meio mundo num império só.",
  "cyrus_young|Young Cyrus the Great, a Persian prince with a short dark curled beard and a soft felt cap, riding a horse across the plains at the head of horsemen",
  "world_known|An ancient landscape seen from a mountain top by a young Persian prince: far away a Greek city, a Babylonian ziggurat and Egyptian pyramids")

# ───────────────────────── 2. O REI QUE DEVOLVIA DEUSES ─────────────────────────
cap("2. O rei que devolvia deuses")
b("Ele se chamava Ciro. Virou rei em quinhentos e cinquenta e nove antes de Cristo e, em vinte anos, engoliu a Média, a Lídia e a Babilônia.",
  f"cyrus_throne|{CIRO}, sitting on a throne in a hall with stone columns@@CIRO, O GRANDE",
  "croesus|King Croesus of Lydia in rich robes surrounded by gold coins, looking worried as Persian soldiers arrive",
  "babylon_gate|Ancient Persian soldiers marching into Babylon through the blue glazed Ishtar Gate decorated with yellow dragons and bulls@@BABILÔNIA", card="559 a.C.")
b("Mas, em vez de esmagar os vencidos, deixou cada povo com seus deuses e sua língua. Os judeus exilados na Babilônia voltaram para casa, e, na Bíblia, Isaías chama Ciro de messias.",
  "gods_return",
  "exiles_return|Ancient Jewish families with donkeys and carts leaving Babylon on a road toward the west, joyful",
  "isaiah_scroll|An ancient Hebrew prophet with a white beard holding a scroll, a vision of a Persian king in the clouds behind him@@ISAÍAS 45", card="539 a.C.")
b("§ Ele registrou isso num barril de argila, o Cilindro de Ciro, que você talvez conheça como a primeira carta de direitos humanos… [curious] Não é.",
  "cylinder_clay|Ancient Babylonian scribes pressing wedge marks into a wet clay barrel-shaped cylinder",
  "cylinder_museum|A small beige baked-clay cylinder shaped like a rugby ball, the size of a forearm, lying on its side, covered in tiny wedge marks, alone in a glass case in a museum@@CILINDRO DE CIRO",
  "cylinder_reading|A museum curator with glasses holding a magnifying glass over a small beige clay cylinder shaped like a rugby ball, raising an eyebrow")
b("É uma peça de fundação, enterrada num muro, e quase todo o texto é o rei se elogiando. Guarde esse cilindro: quem fez dele uma lenda foi um rei do século vinte.",
  "buried_wall|Ancient workers placing a small clay cylinder inside the foundation of a mud-brick city wall in Babylon",
  f"cyrus_proud|{CIRO}, puffing his chest proudly while a bored scribe writes long praise on clay, comic@@PROPAGANDA REAL")
b("§ Mas um império desse tamanho precisava virar uma máquina. E quem fez isso foi aquele rei escolhido pelo cavalo. Lembra? Dario.",
  "machine_gears|An ancient Persian empire shown as a giant machine of wooden gears with roads and messengers, a king turning a big wheel",
  "darius_crowned", "horse_proud")
b("É lenda, claro. Mas o que Dario construiu é real: províncias com governadores, os sátrapas, imposto fixo, e uma estrada de uns dois mil e quinhentos quilômetros.",
  "map_satrapies|Map of the ancient Persian empire from Egypt and Anatolia to the Indus river divided into many softly colored provinces, " + MAPA,
  "satrap|A Persian provincial governor in a rich robe and tall hat sitting on a stool collecting tax baskets of grain and silver from villagers@@SÁTRAPAS",
  "map_royal_road|Map with a long golden road winding from the Aegean coast across Anatolia and Mesopotamia to western Iran, small round dots along it, " + MAPA,
  "relay_station|An ancient Persian royal road relay station: a stone building with stables, a courier jumping from a tired horse onto a fresh one@@ESTRADA REAL")
b("Pela estimativa mais repetida, e discutida, quase metade da humanidade vivia ali. Só uns gregos teimosos não queriam entrar… e foram eles que contaram a história.",
  "crowds_empire|A huge crowd of peoples of the ancient Persian empire standing together: Egyptians, Babylonians, Lydians, Indians, Scythians@@44% DA HUMANIDADE?",
  "greek_hills|Ancient Greek hoplites with bronze crested helmets and round shields standing on a rocky hill by the sea, arms crossed, defiant",
  "herodotus")

# ───────────────────────── 3. OS DOIS OLHOS DO MUNDO ─────────────────────────
cap("3. Os dois olhos do mundo")
b("Maratona, Termópilas, os trezentos de Esparta… quase tudo o que você sabe dessas guerras foi escrito pelo outro lado. Inclusive o cavalo de Dario, contado por um grego.",
  "thermopylae|Spartan soldiers holding a narrow mountain pass by the sea against a huge ancient Persian army@@TERMÓPILAS, 480 A.C.",
  "greek_writer|An ancient Greek historian writing on a scroll with a smug face while an ancient Persian soldier peeks over his shoulder, annoyed@@A VERSÃO GREGA",
  "horse_neigh", card="490 a.C.")
b("Para a Pérsia, a Grécia era uma fronteira chata. O coração do império era Persépolis, com colunas de uns vinte metros.",
  "xerxes_bored|An Achaemenid Persian king with a long square curled beard and a tall golden crown yawning on his throne while a messenger reports, comic",
  "persepolis_glory|Persepolis in its glory around 500 BC: a huge stone terrace with tall columns topped by double bull capitals, grand staircases, people arriving@@PERSÉPOLIS",
  "apadana_relief|Stone relief on a staircase wall at Persepolis: a long line of carved foreign delegations bringing gifts, people looking at it")
b("§ Só que os gregos não esqueceram. Em trezentos e trinta e um antes de Cristo, Alexandre, o Grande, venceu o último Dario em Gaugamela, e, no ano seguinte, Persépolis queimou.",
  "alexander|Alexander the Great, a young beardless Macedonian king with wild hair, bronze armor and a plumed helmet, charging on his black horse@@ALEXANDRE",
  "persepolis_fire|The palaces of Persepolis burning at night, flames rising among the columns, Macedonian soldiers watching", card="331 a.C.")
b("Mas os gregos não seguraram o planalto. Quem tomou a terra de volta foi um povo de arqueiros a cavalo, os partos.",
  "persepolis_wide|The ruins of Persepolis at sunset, tall stone columns and the great double stairway on a stone terrace",
  "parthian_riders|Parthian horse archers in tunics, trousers and soft caps galloping across a plain with bows@@OS PARTOS")
b("§ Eles governaram o Irã por quase cinco séculos. E, em cinquenta e três antes de Cristo, o homem mais rico de Roma, Marco Crasso, veio testá-los.",
  "crassus|Marcus Crassus, a rich old Roman general with a bald head and a red cloak, pointing east greedily, legionaries behind@@MARCO CRASSO", card="53 a.C.")
b("Em Carras, os arqueiros cercaram as legiões, fingiram fugir e atiraram para trás, virados na sela: o tiro do parto. Crasso morreu ali, e diz a lenda que os partos derramaram ouro derretido na boca dele.",
  "arrows_rain|Parthian horse archers circling Roman legionaries in a square formation in the desert, arrows raining down@@CARRAS",
  "parthian_shot|A Parthian horse archer at full gallop turning backwards in the saddle and shooting an arrow behind him@@O TIRO DO PARTO",
  "molten_gold|A Parthian warrior holding a clay pot of glowing molten gold over a fallen Roman helmet lying in the sand, legend mood, no blood")
b("Mas o golpe mais humilhante contra Roma ainda estava por vir… e ficou gravado na rocha.",
  "rock_cliff|A tall sheer cliff face in southern Iran at sunset with carved niches high up, mysterious")
b("§ Em duzentos e vinte e quatro, assumiu uma dinastia que vinha, de novo, de Pars: os sassânidas. Roma e Pérsia viraram os dois olhos do mundo.",
  "ardashir|Ardashir I, first Sasanian Persian king, with a curly tied beard and a crown topped by a large round globe with fluttering ribbons, being crowned by a priest@@OS SASSÂNIDAS",
  "map_pars",
  "two_eyes|A Roman emperor and a Sasanian Persian king standing on two sides of a round world, staring at each other, equal size", card="224 d.C.")
b("E, em duzentos e sessenta, o rei Shapur Primeiro fez o que ninguém tinha feito. Capturou vivo um imperador romano, Valeriano, e mandou esculpir a cena num penhasco de Naqsh-e Rostam, onde ela está até hoje.",
  f"shapur|{SHAPUR}, riding a horse at the head of armored cavalry@@SHAPUR I",
  "valerian_captured|Old Roman emperor Valerian in a purple cloak and laurel wreath being taken prisoner by Sasanian soldiers, shocked@@VALERIANO",
  "naqsh_relief|A huge rock relief carved into a cliff: a Sasanian king on horseback, a Roman emperor kneeling before him@@NAQSH-E ROSTAM", card="260 d.C.")
b("Mas dois olhos que vivem se encarando cansam. Pérsia e Roma se esgotaram em guerras… e, do deserto, veio quem ninguém esperava.",
  "tired_empires|A Roman soldier and a Persian soldier sitting exhausted back to back on a battlefield, broken spears, sunset",
  "desert_army|Arab horsemen and camel riders appearing over a desert dune at dawn with plain banners")

# ───────────────────────── 4. O IMPÉRIO CAI, A LÍNGUA FICA ─────────────────────────
cap("4. O império cai, a língua fica")
b("Eram exércitos árabes, unidos pelo islã. Em seiscentos e trinta e seis, eles venceram os persas em Qadisiya, e, seis anos depois, em Nahavand, o exército sassânida acabou.",
  "qadisiya|Battle of al-Qadisiyya: Arab cavalry on horses and camels fighting Sasanian war elephants and armored riders on a dusty plain@@QADISIYA",
  "desert_army", card="636 d.C.")
b("O último rei, Yazdegerd Terceiro, fugiu por anos, até que, segundo a crônica, foi morto num moinho perto de Merv… pelo próprio moleiro.",
  "yazdegerd_flee|The young last Sasanian king with a small beard and a winged crown fleeing on horseback through a cold dark landscape@@YAZDEGERD III",
  "mill|An old stone watermill by a river at night, a lantern glowing inside, ominous@@MERV, 651")
b("§ [serious] O império caiu em quinze anos. Mas o Irã não virou árabe.",
  "ctesiphon|The Sasanian palace at Ctesiphon with its giant brick arch, abandoned and dusty")
b("Egito, Síria e Iraque passaram a falar árabe. O Irã adotou o islã, devagar, ao longo de séculos… mas ficou com a própria língua. Por quê?",
  "map_arabic|Geographic relief map of the lands from the Nile to the Persian Gulf, the western lands painted soft green and the Iranian plateau on the right painted warm orange, " + MAPA,
  "grandma_stories|A Persian family in the 9th century at home, children listening to their grandmother telling stories by a lamp@@O PERSA RESISTE")
b("Boa parte da resposta cabe num livro. Por volta de novecentos e setenta e sete, em Tus, um proprietário de terras chamado Ferdowsi começou o Shahnameh, o Livro dos Reis.",
  "book_glow|A thick old closed leather-bound book with a plain cover and gold corner decorations on a wooden stand glowing softly in a dark room",
  f"shahnameh_start|{FERD_M}, starting to write a big book at a low desk on a carpet in a country house near a walled city@@FERDOWSI",
  "tus_gate|The walled medieval Persian city of Tus in the 11th century at dusk, mud-brick walls and two tall arched gates@@TUS", card="c. 977")
b("Ele juntou os mitos e os reis do Irã de antes do islã, heróis, dragões, o pássaro Simurgh, em uns cinquenta mil dísticos. Era o país inteiro guardado num poema.",
  "rostam_dragon|The Persian legendary hero Rostam in a tiger-skin coat and a helmet fighting a green dragon@@ROSTAM",
  "simurgh|The giant mythical bird Simurgh with long colorful feathers carrying a baby on a mountain peak@@SIMURGH",
  "manuscript_pages|Open pages of an ornate Persian manuscript book with gold borders and a painted miniature of a king, the writing areas shown as decorative wavy lines")
b("§ Levou mais de trinta anos. Ferdowsi terminou velho e pobre, e dedicou a obra a um sultão turco, Mahmud de Ghazni, que, conta a lenda, pagou mal.",
  f"ferdowsi_old|{FERD_V}, worn robe, finishing a huge manuscript in a poor bare room, tired",
  "mahmud|A Turkic sultan with a short beard, a large turban with a jewel and a rich brocade robe on a throne, bored@@MAHMUD DE GHAZNI",
  f"silver_coins|{FERD_V}, looking offended at a small bag of silver coins handed to him by a court messenger")
b("Anos depois, arrependido, o sultão mandou a fortuna: uma caravana de anil, um corante azul que valia sessenta mil dinares.",
  "indigo_caravan|A camel caravan loaded with bales of deep blue indigo dye crossing a desert road toward a walled city, a merchant opening one bale to show bright blue cakes@@ANIL",
  "caravan_camels|Close view of camels loaded with bulging blue bundles, a Persian camel driver in a turban leading them under a city gate arch")
b("Ela entrou por um portão de Tus enquanto, pelo outro portão, saía o caixão do poeta. E a filha dele recusou o presente.",
  "tus_gate",
  "funeral_gate|At the gate of a medieval Persian walled city, a small funeral procession of mourners in turbans carrying a simple wooden coffin draped in green cloth out of the city",
  "daughter|A Persian woman in a headscarf and long dress refusing with a raised hand the blue bundles offered by the sultan's messengers@@A FILHA")
b("§ [warm] O que estava naquele caixão era maior que a fortuna. Era a língua. Mil anos depois, um aluno iraniano ainda entende boa parte dos versos dele.",
  "coffin_light",
  "schoolkids_reading|Iranian schoolchildren today in a classroom reading aloud from a big illustrated book of epic poems, a teacher smiling",
  "manuscript_pages")
b("A língua estava a salvo… mas, dois séculos depois, chegou do leste um exército que não lia poemas.",
  "mongol_horizon|A huge Mongol cavalry army appearing on the eastern horizon of a Persian plain, dust clouds, fur hats")

# ───────────────────────── 5. OS CONQUISTADORES DIGERIDOS ─────────────────────────
cap("5. Os conquistadores digeridos")
b("Em mil duzentos e dezenove, chegaram os mongóis de Gengis Khan. Nishapur, Merv, Herat… cidades inteiras foram arrasadas.",
  "genghis|A Mongol ruler with a thin beard, a fur-trimmed hat and leather armor on horseback looking over a burning city@@GENGIS KHAN",
  "nishapur_ruin|The ruins of a destroyed medieval Persian city with smoke rising, broken walls and domes@@NISHAPUR",
  card="1219")
b("Lembra dos túneis do começo? Talvez o pior estrago tenha sido esse: sem gente para cuidar, muitos qanats secaram.",
  "qanat_tunnel",
  "qanat_collapsed|A collapsed qanat shaft in the desert half filled with sand, a dry channel and a dead orchard nearby@@OS QANATS SECAM")
b("§ E aí aconteceu algo bem iraniano. Em duas gerações, os conquistadores falavam persa, contratavam vizires persas e erguiam mesquitas persas.",
  "ilkhan_court|A Mongol ruler in a Persian-style palace court, wearing a Mongol hat with a Persian silk robe, listening to a Persian vizier holding a book@@ILKHANATO",
  "mongol_mosque|Mongol and Persian builders together raising a mosque with a huge turquoise dome, scaffolding, 14th century")
b("[amazed] O Irã não venceu os mongóis… ele os digeriu. A língua estava salva. Faltava a fé, e quem mudou a fé foi um menino.",
  "conquerors_persian",
  "boy_horizon|A small boy in a red cap standing on a hill looking at a Persian city at dawn, determined")

# ───────────────────────── 6. O MENINO QUE MUDOU A FÉ ─────────────────────────
cap("6. O menino que mudou a fé")
b("Em mil quinhentos e um, um garoto de catorze anos entrou em Tabriz à frente de um exército. Era Ismail.",
  f"ismail_tabriz|{ISMAIL}, entering the city of Tabriz on a horse at the head of warriors with tall red caps@@ISMAIL",
  "qizilbash|Warriors with tall red caps wrapped in white turbans, swords and lances, cheering@@QIZILBASH", card="1501")
b("Ele se coroou xá e impôs o islã xiita a um país que, na maioria, era sunita. Como se converte um país inteiro?",
  f"ismail_crowned|{ISMAIL}, being crowned on a throne in a palace hall@@TABRIZ",
  "puzzled_crowd|A crowd of Persian townspeople in 1501 looking at each other puzzled in a city square")
b("Ismail trouxe clérigos xiitas do Líbano, perseguiu quem resistia e, em um século, o Irã virou xiita. A fronteira religiosa de hoje vem muito desse adolescente, que, aliás, escrevia poemas… em turco.",
  "clerics_lebanon|Shiite clerics with turbans and books arriving by camel from the green mountains of Lebanon@@CLÉRIGOS DO LÍBANO",
  "map_shia_sunni|Map of the Middle East with Iran painted warm green and the neighboring lands painted pale sand, a clear border line, " + MAPA,
  f"ismail_poet|{ISMAIL}, writing poetry by lamplight in a palace garden at night@@POETA, EM TURCO")
b("§ O bisneto dele, Shah Abbas, levou a capital para Isfahan, tão rica que os iranianos diziam: Isfahan é metade do mundo.",
  "abbas|A Persian king with a very long drooping black mustache and no beard, a turban with a feather plume and a rich robe@@SHAH ABBAS",
  "naqsh_jahan|The huge Naqsh-e Jahan square in Isfahan in the 1600s with blue-tiled domes, arcades, polo players and merchants@@ISFAHAN", card="1598")
b("Então a metade do mundo caiu. Em mil setecentos e vinte e dois, afegãos tomaram Isfahan, e, atrás do último grande conquistador, vieram reis que foram vendendo o país aos pedaços.",
  "isfahan_falls|Afghan warriors entering a gate of Isfahan, frightened Persian citizens@@1722",
  "selling_pieces|A Persian king in a jeweled robe handing pieces of a map like slices of cake to foreign gentlemen in top hats, comic")

# ───────────────────────── 7. A COROA À VENDA ─────────────────────────
cap("7. A coroa à venda")
b("Esse conquistador era Nader Xá. Em mil setecentos e trinta e nove, ele saqueou Délhi e levou o Koh-i-Noor, o diamante que o nosso vídeo da Índia segue até Londres.",
  f"nader|{NADER}, on horseback in front of his army@@NADER XÁ",
  f"kohinoor|{NADER}, holding up a huge shining diamond in amazement@@KOH-I-NOOR", card="1739")
b("Depois dele, os reis Qajar perderam duas guerras para a Rússia e, com elas, o sul do Cáucaso. E um xá que não vence… passa a vender.",
  "qajar_king|A Persian shah of the early 1800s with a very long black beard, a tall black lambskin hat with a jeweled aigrette and a jeweled robe@@DINASTIA QAJAR",
  "map_caucasus|Map of the Caucasus mountains between the Black Sea and the Caspian Sea, the southern Caucasus lands shaded red, the north of Iran below, " + MAPA,
  "shah_sale|A Persian shah sitting at a market stall with a sign-less awning, selling things to British gentlemen, comic")
b("Em mil oitocentos e noventa, Naser al-Din Xá vendeu a um britânico o monopólio do tabaco do país inteiro.",
  f"naser_shah|{NASER}, signing a document at a desk while a British gentleman in a top hat smiles@@NASER AL-DIN XÁ",
  "tobacco_field|A Persian tobacco field with farmers harvesting leaves, a British clerk counting with a notebook", card="1890")
b("§ Então, em mil oitocentos e noventa e um, um grande clérigo xiita proibiu o fumo… e o Irã, que fumava muito, parou.",
  "cleric_fatwa|A senior Shiite cleric with a white beard and a black turban sitting on a carpet, raising a finger to issue a ruling, students around@@MIRZA SHIRAZI",
  "bazaar_closed|A long covered Persian bazaar with all shops closed and empty, merchants standing with crossed arms, water pipes put away@@BOICOTE", card="1891")
b("Em semanas, o contrato caiu. Um turbante venceu uma coroa. Guarde esse tabaco, porque a coroa não aprendeu, e o próximo contrato era muito maior.",
  f"shah_cancels|{NASER}, tearing up a document, annoyed",
  "turban_crown|A black cleric's turban and a jeweled royal crown facing each other on a table, the crown tipped over",
  "tobacco_crown")

# ───────────────────────── 8. O PETRÓLEO ASSINADO PARA FORA ─────────────────────────
cap("8. O petróleo assinado para fora")
b("Em mil novecentos e um, um milionário britânico, William D'Arcy, ganhou o direito de procurar petróleo. Por sete anos, nada.",
  "darcy|A plump Victorian British millionaire with a white mustache in a suit studying a blank map@@WILLIAM D'ARCY",
  "drilling_dry|An early 1900s wooden oil derrick in a barren Persian valley, tired British engineers and Persian workers, nothing coming out", card="1901")
b("Até que, em Masjed Soleyman, a sonda acertou. Dali nasceu a empresa que hoje se chama BP, e quase tudo já estava assinado para fora.",
  "oil_gusher|A black oil gusher shooting up from a wooden derrick in the Persian hills at dawn, workers celebrating@@MASJED SOLEYMAN",
  "oil_feet|A Persian man looking down at black oil bubbling between his feet, while a British businessman behind him holds up a long contract", card="1908")
b("§ Em mil novecentos e vinte e cinco, um oficial cossaco virou rei, Reza Xá, e modernizou o país à força: ferrovia, universidade, exército.",
  f"reza_shah|{REZA}, standing in a palace hall@@REZA XÁ",
  "railway|A 1930s steam train crossing a high stone bridge in the Iranian mountains, workers cheering", card="1925")
b("Dez anos depois, ele fez aquele pedido. Lembra do apelido? O mundo agora devia dizer Irã, e não Pérsia.",
  f"reza_letter|{REZA}, handing a sealed letter to foreign diplomats in a palace hall@@1935",
  "map_iran_name",
  "airya_proud")
b("Em mil novecentos e quarenta e um, britânicos e soviéticos invadiram e tiraram Reza Xá do trono. Ficou o filho, Mohammad Reza.",
  "invasion_1941|British and Soviet soldiers with tanks meeting on a dusty Iranian road in 1941@@1941",
  "young_shah|A young 21-year-old Persian shah with slicked-back dark hair in a military uniform, nervously taking an oath@@MOHAMMAD REZA XÁ")
b("§ E o petróleo seguia nas mãos de fora, até que, em mil novecentos e cinquenta e um, o primeiro-ministro Mossadegh o nacionalizou.",
  f"mossadegh|{MOSSA}, giving a passionate speech to a cheering crowd@@MOSSADEGH",
  "oil_ours|Iranian oil workers raising their fists in joy in front of a refinery, 1951", card="1951")
b("Em agosto de cinquenta e três, um golpe derrubou Mossadegh, com propaganda e multidões pagas.",
  "coup_tanks|Tanks and soldiers in the streets of Tehran in August 1953, a crowd running@@AGOSTO DE 1953",
  "paid_crowd|A man secretly handing banknotes to a group of men holding blank placards in a 1950s street, sneaky")
b("[serious] Por sessenta anos, isso foi negado… até que, em dois mil e treze, a CIA admitiu em documentos: o golpe foi feito sob direção dela. Muitos historiadores veem aqui a raiz da desconfiança entre o Irã e os Estados Unidos.",
  f"mossadegh_arrest|{MOSSA}, sitting alone in pajamas under house arrest in a village house, sad",
  "cia_docs|A stack of declassified documents with blacked-out lines on a desk in a modern archive, a hand lifting one page@@CIA, 2013",
  "distrust|Two men in suits at the two ends of a very long table, arms crossed, glaring at each other, cold light", card="2013")
b("E o xá que o golpe manteve no trono resolveu dar uma festa.",
  "party_invite|A golden invitation card with a royal crown emblem on a velvet tray, champagne glasses, no text")

# ───────────────────────── 9. O TURBANTE CONTRA A COROA ─────────────────────────
cap("9. O turbante contra a coroa")
b("Mil novecentos e setenta e um. Entre as colunas que Alexandre queimou, o xá comemorou dois mil e quinhentos anos de monarquia, com comida vinda de Paris, enquanto muitas aldeias nem tinham luz.",
  "party_tents|A luxurious tent city set up next to the ruins of Persepolis in 1971, golden tents and lights, guests in gowns and uniforms arriving",
  f"shah_1971|{XA}, greeting foreign kings in front of a golden tent@@O XÁ",
  "banquet|A lavish banquet in a huge tent, French waiters serving silver plates, champagne and chandeliers",
  "village_dark|A poor Iranian village at night with mud houses lit only by oil lamps", card="1971")
b("E lembra do cilindro? Foi nessa época que o xá o apresentou ao mundo como a primeira carta de direitos humanos.",
  f"shah_cylinder|{XA}, presenting a small beige clay cylinder shaped like a rugby ball on a velvet cushion at a ceremony",
  "cylinder_museum")
b("§ De longe, um clérigo exilado chamou aquilo de festa do diabo. Era Ruhollah Khomeini, e os sermões dele entravam no Irã em fitas cassete.",
  f"khomeini_exile|{CLERIGO}, speaking in a modest room with a carpet, in exile@@KHOMEINI",
  "cassettes|Hands secretly passing cassette tapes in a crowded Tehran bazaar in the 1970s@@FITAS CASSETE")
b("[serious] Lembra do tabaco? De novo, um turbante enfrentou uma coroa. Em janeiro de mil novecentos e setenta e nove, o xá saiu do Irã para não voltar.",
  "turban_crown",
  "protests_1978|Huge crowds of men and women marching in the streets of Tehran in 1978, raised fists, the white Azadi tower in the background",
  f"shah_leaves|{XA} and his wife walking toward a plane at an airport, sad, winter@@JANEIRO DE 1979", card="1979")
b("Duas semanas depois, Khomeini voltou de Paris, e o país virou uma República Islâmica. No fim do ano, estudantes tomaram a embaixada americana: cinquenta e dois reféns, presos por quatrocentos e quarenta e quatro dias.",
  f"khomeini_plane|{CLERIGO}, stepping down the stairs of a passenger plane at an airport, a huge crowd waiting",
  "embassy|Young students climbing over the gate of a walled embassy compound in Tehran in 1979, no flags@@EMBAIXADA DOS EUA",
  "hostages|Blindfolded men standing in a courtyard guarded by young students, tense, 1979")
b("§ No ano seguinte, Saddam Hussein invadiu. Foram oito anos de guerra, com estimativas a partir de meio milhão de mortos, e o Iraque usou armas químicas.",
  "saddam|An Iraqi leader with a thick black mustache and an olive military uniform pointing at a blank map@@SADDAM HUSSEIN",
  "trenches|Soldiers in muddy trenches in a flat marshland, barbed wire, smoke@@1980–1988",
  "gas_masks|Soldiers putting on gas masks as a yellow cloud drifts over the trenches", card="1980")
b("Meninos voluntários atravessaram campos minados, alguns, segundo relatos, com chaves de plástico no pescoço. Diziam que elas abriam o paraíso.",
  "plastic_keys|Close-up of a small cheap plastic key on a string hanging on a dusty shirt, sad mood, no face visible@@CHAVES DE PLÁSTICO",
  "persian_garden#detalhe-centro")
b("Em mil novecentos e oitenta e oito, Khomeini aceitou o cessar-fogo e disse que era como beber veneno. Morreu no ano seguinte, e quem assumiu foi Ali Khamenei.",
  f"poison_cup|{CLERIGO}, holding a small cup with a grim face, signing a paper@@CESSAR-FOGO",
  f"khamenei|{LIDER}, standing in a hall in 1989@@ALI KHAMENEI", card="1988")

# ───────────────────────── 10. DE PAI PARA FILHO ─────────────────────────
cap("10. De pai para filho")
b("Só que agora o turbante era o governo… e os protestos passaram a ser contra ele. Em dois mil e nove, uma eleição contestada pôs milhões nas ruas.",
  "turban_throne|A black cleric's turban resting on a royal throne in an empty palace hall",
  "green_movement|A huge peaceful crowd in Tehran wearing green wristbands and green scarves, a silent march@@ELEIÇÃO DE 2009", card="2009")
b("Em setembro de dois mil e vinte e dois, Mahsa Amini, de vinte e dois anos, morreu sob custódia da polícia da moralidade. Tinha sido presa por causa do véu.",
  "candle_scarf|A single white candle and flowers on a Tehran sidewalk at night, a headscarf laid beside them, mourning@@MAHSA AMINI",
  "police_van|A white police van parked on a Tehran street at night, people looking at it with fear", card="2022")
b("O país explodiu. Mulheres tiraram o lenço e cortaram o cabelo em público, com um lema das mulheres curdas: mulher, vida, liberdade.",
  "scarves_up|Iranian women in a street protest waving their headscarves in the air, men beside them",
  "hair_cut|A woman seen from behind cutting a lock of her own long hair with scissors in public, a crowd around her, defiant",
  "kurdish_women|Kurdish women in traditional colorful dresses marching in a mountain town@@MULHER, VIDA, LIBERDADE")
b("Segundo ONGs, mais de quinhentas pessoas morreram, e cerca de vinte mil foram presas. O regime aguentou.",
  "arrests|Riot police in black detaining protesters in a Tehran street at night, motorcycles, all shop signs completely blank with no letters@@CERCA DE 20 MIL PRESOS",
  "empty_street|An empty Tehran street at dawn after protests, a lost headscarf on the ground")
b("§ A pressão seguinte veio de fora, pelo céu. Em junho de dois mil e vinte e cinco, Irã e Israel travaram uma guerra de doze dias, que terminou num cessar-fogo.",
  "night_sky|A night sky over Tehran with streaks of light, the city below and the Alborz mountains in silhouette",
  "missiles_night|Missiles and interceptor trails crossing a night sky over a mountainous landscape, flashes on the horizon@@GUERRA DE 12 DIAS", card="2025")
b("Ele não durou. Em vinte e oito de fevereiro de dois mil e vinte e seis, um ataque dos Estados Unidos e de Israel matou Ali Khamenei.",
  "tehran_strike|Smoke rising over a district of Tehran seen from far away, the Alborz mountains behind, grey day",
  "empty_chair|An empty ornate armchair in a quiet hall with a black cleric's cloak and large glasses folded on it, soft light", card="28/02/2026")
b("Oito dias depois, a Assembleia dos Especialistas escolheu o novo líder supremo… o filho dele, Mojtaba Khamenei.",
  "assembly|An assembly of elderly Shiite clerics in black and white turbans seated in rows in a large hall, voting by raising hands@@ASSEMBLEIA DOS ESPECIALISTAS",
  "mojtaba|A middle-aged Shiite cleric with a grey-black beard, a black turban and glasses standing in a hall, serious@@MOJTABA KHAMENEI", card="08/03/2026")
b("[serious] Uma revolução feita contra a monarquia hereditária acabou passando o poder de pai para filho. Até a gravação deste vídeo, não há acordo de paz.",
  "father_son|An old black turban and a younger black turban side by side on a table, a beam of light on them",
  "city_waiting|Tehran today at dusk, people on a street looking at their phones with worried faces@@ATÉ A GRAVAÇÃO")

# ───────────────────────── FECHO (paga o cavalo e o paraíso) ─────────────────────────
cap("Fecho")
b("§ [warm] E o cavalo? Lembra dele? Há mais de dois mil e quinhentos anos, o Irã escolheu um rei pelo relincho de um cavalo… com uma ajudinha do cavalariço.",
  "horse_neigh", "groom_whisper", "horse_wink")
b("Depois, o Irã foi governado por quem venceu na espada, por quem herdou a coroa, por quem falou do púlpito. E, agora, por um filho escolhido numa sala de clérigos.",
  "conquerors_march", "qajar_king", "khomeini_exile", "assembly")
b("Quem escolhe quem governa o Irã? Desde aquele cavalo, essa pergunta nunca teve uma resposta tranquila.",
  "horse_tehran", "empty_throne")
b("§ Mas tem uma coisa que nenhum rei e nenhum invasor escolheu. Volte a Tus. O túmulo de Ferdowsi fica num jardim, com água correndo em canais: um pequeno paraíso.",
  "ferdowsi_tomb|The white stone mausoleum of Ferdowsi in Tus, Iran: a square monument with columns on a stepped base, surrounded by a garden with pools and water channels@@TÚMULO DE FERDOWSI",
  "persian_garden")
b("O império caiu, a fé mudou, o nome sumiu e voltou, a coroa caiu para o turbante… e a língua de Ferdowsi segue viva. Tão viva que você fala persa sem saber: paraíso, laranja, azul, bazar, caravana. E xeque, que vem de xá, o rei.",
  "schoolkids_reading@@1000 ANOS DEPOIS",
  "oranges|A Brazilian street market stall with piles of oranges, blue tiles on the wall behind, people shopping@@LARANJA, AZUL, BAZAR",
  "caravan_camels@@CARAVANA = KARVAN",
  "chess|A chess game on a table with the black king toppled over, an old Persian man in robes and a modern Brazilian kid playing@@XEQUE = XÁ, O REI")
b("Exércitos conquistam o Irã… e a língua do Irã conquista os exércitos.",
  "conquerors_persian", "persepolis_wide")
b("E você? Qual palavra persa você já disse hoje sem perceber? Conta aqui nos comentários.",
  f"guide_comment|{GUIA} sitting under a pomegranate tree in a Persian garden, thinking, holding an orange",
  "ferdowsi_tomb")

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
        blocos.append({"id": bid, "texto": blk["t"], "ideia": blk.get("ideia", False)})
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
    words = sum(len(limpo(b_["texto"]).split()) for b_ in blocos)
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
