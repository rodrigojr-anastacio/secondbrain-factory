#!/usr/bin/env python3
"""Fonte única do 003-ira: roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

Estrutura (modelo History in Minutes / Archive in Minutes, estudo de 04/11/2026 em BRIEF.md):
  hook por anedota humana (≤ 10 s) → promessa do título + loop → capítulos-OBJETO de 1–2 palavras
  (falados na narração e mostrados na placa) → re-hook a cada ~60–90 s → fecho que volta à imagem do começo.

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (nome, lugar, data curta: até ~28 caracteres, CAIXA ALTA)
  ex.: "ciro_trono|Cyrus the Great on a throne...@@CIRO, O GRANDE"
Bloco: b(texto, *planos, card="559 a.C.")  · capítulo: cap("3. O Cilindro")
Voz: o texto é escrito PARA A FALA (frases curtas, vírgula de respiração, "…" na virada); o tts_fish.py --por-frase
gera frase a frase com 0,32 s entre elas. Não use [break] (a pausa entre frases já existe); [long-break] só antes
de revelação; tag de tom só onde a emoção muda (máx. ~1 a cada 2–3 blocos). Ver amostras-voz/LEIA.md.
"""
import json, math, re
from pathlib import Path

WPS = 2.4            # palavras por segundo com as pausas entre frases (A/B do hook: ~144 ppm)
BREAK, LONG = 0.35, 0.8
MAX_PLANO_INICIO = 3.0   # s por plano nos primeiros INICIO s (≈ 20 cortes/min, como o Archive in Minutes)
INICIO = 120.0
MAX_PLANO = 3.6      # s por plano depois (≈ 17 cortes/min)
INEDITO_ATE = 180.0  # s: só imagens novas até aqui
JANELA = 60.0        # s: mesmo enquadramento da mesma imagem só depois disso
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "A história INTEIRA do Irã"


B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None): B.append({"t": t, "s": list(s), "card": card})

# Personagens recorrentes (descrição visual fixa, repetida nos prompts):
#  FERDOWSI: Persian poet, white turban, simple blue robe (meia-idade: dark beard; velho: long white beard)
#  CIRO: square curled dark beard, tall flat-topped golden crown, long purple robe with wide sleeves
#  DARIO I: long square curled black beard, tall crenellated golden crown, saffron robe with wide sleeves
#  SHAPUR I: crown topped by a large round globe, curly tied beard, fluttering ribbons, pearl necklace
#  ISMAIL I: beardless 14-year-old, white turban wrapped around a tall red baton cap (Qizilbash taj)
#  NADER XÁ: thick black beard, tall red four-peaked hat with a feather plume
#  NASER AL-DIN XÁ: huge black curled mustache, black lambskin hat with a jeweled aigrette, dark frock coat
#  REZA XÁ: tall stern man, 1930s Iranian military uniform, peaked cap, short grey mustache
#  MOSSADEGH: elderly bald man with a long nose, grey suit (ou pijama na prisão)
#  M. REZA XÁ: slicked-back hair (escura em 1941, grisalha em 1971), military dress uniform with medals
#  KHOMEINI: elderly Shiite cleric, long white beard, black turban, black cloak, thick dark eyebrows
#  KHAMENEI: Shiite cleric, black (depois grey) beard, black turban, large glasses, brown cloak
FERD_M = "Ferdowsi, a middle-aged Persian poet with a dark beard, a white turban and a simple blue robe"
FERD_V = "Ferdowsi, an elderly Persian poet with a long white beard, a white turban and a simple blue robe"
CIRO = "Cyrus the Great, Achaemenid Persian king with a square curled dark beard, a tall flat-topped golden crown and a long purple robe with wide sleeves"
DARIO = "Darius the Great, Achaemenid Persian king with a long square curled black beard, a tall crenellated golden crown and a saffron robe with wide sleeves"
SHAPUR = "Shapur I, Sasanian Persian king with a crown topped by a large round globe, a curly tied beard, fluttering ribbons and a pearl necklace"
ISMAIL = "Shah Ismail I, a beardless 14-year-old Safavid boy king wearing a white turban wrapped around a tall red baton cap"
NADER = "Nader Shah, a stern 18th century Persian conqueror with a thick black beard and a tall red four-peaked hat with a feather plume"
NASER = "Naser al-Din Shah Qajar with a huge black curled mustache, a black lambskin hat with a jeweled aigrette and a dark frock coat"
REZA = "Reza Shah Pahlavi, a tall stern man in a 1930s Iranian military uniform with a peaked cap and a short grey mustache"
MOSSA = "Mohammad Mossadegh, an elderly bald Iranian prime minister with a long nose and a grey suit"
SHAH71 = "Mohammad Reza Shah in 1971 with slicked-back grey hair and a military dress uniform with medals"
KHOM = "Ayatollah Khomeini, an elderly Shiite cleric with a long white beard, a black turban, a black cloak and thick dark eyebrows"
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes"

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("[curious] Tus, ano mil e vinte, conta a lenda. Uma caravana carregada de riquezas entra por um portão da cidade.",
  "tus_gate_caravan|The walled medieval Persian city of Tus in the 11th century at dusk, mud-brick walls and a tall arched gate, a camel caravan loaded with heavy bundles and chests entering through the gate",
  "caravan_camels|Close view of camels in a caravan loaded with bulging bundles and wooden chests, a Persian camel driver in a turban leading them under a city gate arch@@TUS, PÉRSIA",
  "caravan_chests|Close view of an open wooden chest on a camel's back full of treasure, coins and precious cloth, a city gate behind", card="c. 1020 d.C.")
b("Pelo outro portão, sai o caixão do poeta. A fortuna era dele.",
  "funeral_gate|At the opposite gate of the same medieval Persian walled city, a small funeral procession of mourners in turbans carrying a simple wooden coffin draped in green cloth out of the city",
  "coffin_close|A simple wooden coffin carried on the shoulders of mourners, a reed pen and a stack of old manuscript pages tied with string on top of it@@O POETA")
b("Essa é a história inteira do Irã. E de como um país conquistado tantas vezes nunca deixa de ser ele mesmo.",
  "iran_landscape|Wide view of the Iranian plateau: a desert plain, snowy Zagros mountains behind, a turquoise dome of a mosque in a small oasis town",
  "persepolis_wide|The ruins of Persepolis at sunset, tall stone columns and the great double stairway with carved reliefs on a stone terrace@@PERSÉPOLIS",
  "tehran_today|Modern Tehran today with the tall Milad tower and the snowy Alborz mountains behind, a dense city with traffic@@TEERÃ, HOJE")
b("Gregos, árabes, turcos e mongóis tomam esta terra. Todos vão embora… ou acabam virando persas.",
  "conquerors_march|Four armies marching into a Persian valley one after the other: Greek hoplites with round shields, Arab horsemen with lances, Turkic horse archers, Mongol cavalry with fur hats",
  "conquerors_leave|A Greek hoplite, an Arab rider, a Turkic archer and a Mongol horseman walking away over a hill at sunset, seen from behind",
  "conquerors_persian|A Mongol warrior and a Turkic soldier sitting on a Persian carpet in a garden, now wearing Persian silk robes, reading a book of poetry and drinking tea, smiling@@OS CONQUISTADORES")
b("[serious] E o que salva o Irã… está dentro daquele caixão.",
  "coffin_dark|A plain wooden coffin lying in a dim room lit by a single oil lamp, mysterious mood",
  "coffin_light|A soft golden light glowing from the cracks of a closed plain wooden coffin in a dark room, mysterious")

# ───────────────────────── 1. O TÚNEL ─────────────────────────
cap("1. O Túnel")
b("O Túnel. O planalto do Irã é uma tigela de montanhas, com deserto no meio, e pouca chuva.",
  "map_plateau|Simple illustrated map of the Iranian plateau ringed by mountains, the Zagros range on the west and the Alborz range in the north, two large pale deserts in the center, the Caspian Sea at the top and the Persian Gulf at the bottom, no labels, no text",
  "plateau_bowl|Wide aerial view of a high desert basin ringed by brown mountains, white salt flats shining in the middle@@PLANALTO IRANIANO",
  "lut_desert|The Lut desert in Iran: giant wind-carved sand ridges under a burning sun, completely empty@@DESERTO DE LUT")
b("Então os antigos persas vão buscar a água embaixo da terra. São os qanats, túneis de quilômetros, tão bem inclinados que a água da montanha desce sozinha.",
  "qanat_digger|Ancient Persian well diggers lowering a man into a deep vertical shaft with a wooden windlass and a rope, desert around",
  "qanat_tunnel|Inside a narrow underground tunnel dug in rock, a thin stream of clear water flowing along the floor, a digger holding an oil lamp",
  "qanat_cutaway|Cutaway illustration of a qanat: groundwater under a mountain, a long gently sloping underground tunnel with vertical shafts to the surface, water coming out into green fields of a desert village, no text@@QANATS",
  "qanat_outlet|Clear water flowing out of a stone tunnel mouth into an irrigation channel in a desert village, children splashing")
b("Alguns correm há mais de dois mil anos. E guardam até gelo para o verão, em cúpulas de barro.",
  "qanat_wells_aerial|Aerial view of a long line of round well mouths dotting the desert from the foot of the mountains to a green village, like a dotted line@@GONABAD",
  "yakhchal|A huge cone-shaped mud-brick ice house in the Iranian desert with a long high shade wall beside it, blue sky@@YAKHCHAL",
  "yakhchal_inside|Inside a domed mud-brick ice house, blocks of ice stored in a deep pit, a worker with a pickaxe, cool blue light")
b("No fim do túnel, a água vira um jardim murado. Em persa antigo, pairidaêza. [amazed] A palavra passa pelo grego e pelo latim, e chega ao português como paraíso.",
  "persian_garden|A walled Persian garden with four water channels crossing in the middle, cypress and pomegranate trees and a small pavilion",
  "garden_wall|Ancient Persian gardeners building a high mud-brick wall around an orchard with pomegranate trees@@PAIRIDAÊZA",
  "xenophon|An ancient Greek writer in a tunic writing on a scroll inside a Persian garden, amazed by the trees@@PARÁDEISOS, EM GREGO",
  "paradise_word|A Brazilian family today in a lush green garden, a child pointing at the flowers, bright sunny day@@PARAÍSO")
b("Na beira do planalto, em Susa, tem gente vivendo desde uns quatro mil e duzentos antes de Cristo. São os elamitas, com uma escrita que ninguém consegue ler.",
  "susa_ancient|The ancient city of Susa on a hill at the edge of a green plain, mud-brick houses and a high temple platform, a river and palm trees@@SUSA",
  "elamite_king|An Elamite king with a round cap and a long braided beard, in a fringed robe, standing in a mud-brick temple courtyard@@OS ELAMITAS",
  "elamite_tablet|A clay tablet and a carved stone covered with mysterious geometric signs, in a museum case",
  "scholar_puzzled|A scholar scratching his head in front of a clay tablet with strange signs under a glass dome", card="4200 a.C.")
b("Até dois mil e vinte e dois. Uma equipe liderada por um arqueólogo francês decifra boa parte dela.",
  "silver_beaker|An ancient silver beaker with lines of small incised geometric signs around it, lit in a museum case@@ELAMITA LINEAR",
  "decipher_joy|A modern archaeologist jumping with joy in a museum storeroom holding up a photo of an ancient inscription@@DECIFRADO",
  "desset_lab|A modern archaeologist with a beard studying photos of an ancient silver beaker on a laptop, a notebook full of sketches of signs@@FRANÇOIS DESSET", card="2022")
b("Por volta de mil e quinhentos antes de Cristo, chega gente nova do norte. E ela traz um nome.",
  "steppe_riders|A group of Bronze Age herders with horses, ox wagons and cattle coming down from northern grasslands into the mountains of Iran",
  "herders_camp|Bronze Age Iranian herders setting up felt tents in a green mountain valley, sheep and horses, a campfire@@POVOS IRANIANOS",
  "nomad_elder|A Bronze Age Indo-Iranian elder with a long beard and a felt cap pointing at the land ahead, his people behind him", card="c. 1500 a.C.")

# ───────────────────────── 2. O NOME ─────────────────────────
cap("2. O Nome")
b("O Nome. Esses povos se chamam de árias, algo como os nobres. E a terra deles vira a terra dos árias, o Irã.",
  "name_valley|Bronze Age Iranian herders standing on a hill overlooking a vast green valley, their leader raising his wooden staff proudly",
  "airya_proud|An ancient Iranian tribal leader in a felt cap and wool tunic speaking proudly to his people around a fire@@ÁRIA = NOBRE",
  "herders_horses|Bronze Age Iranian horsemen on a ridge at sunset, the wind in their long hair, proud@@OS ÁRIAS",
  "map_iran_name|Simple illustrated map of the Iranian plateau glowing in warm golden light as one land, mountains around it, the Caspian Sea above and the Persian Gulf below, no labels, no text")
b("Guarde esse nome. Daqui a uns três mil anos, um rei vai pedir ao mundo para usá-lo de novo.",
  "remember_stone|Close view of an ancient scribe's hands carving into a stone slab that glows softly, no letters visible",
  "future_king|A ghostly vision in the clouds of a 1930s king in military uniform, floating above ancient herders on a hill@@3 MIL ANOS DEPOIS",
  "diplomat_letter|A 1930s diplomat at a desk next to a globe, opening a letter with a big red royal wax seal")
b("Porque Pérsia não é o nome que eles se dão. É um apelido grego, tirado de uma província do sul, Pars, a atual Fars.",
  "greek_geographer|An ancient Greek geographer in a himation drawing a map on a scroll and pointing at one southern region@@APELIDO GREGO",
  "map_pars|Simple illustrated map of Iran with one southern province near the Persian Gulf highlighted in gold, the rest pale, no labels, no text",
  "pars_province|An ancient province in southern Iran: a fertile plain with villages and a river below the Zagros hills, seen from above@@PARS",
  "fars_landscape|Green and golden plains of the Fars province in southern Iran with the Zagros hills, sheep grazing, a shepherd@@FARS, HOJE")
b("E é de Pars que sai o homem que vai juntar meio mundo num império só.",
  "cyrus_young|Young Cyrus the Great, a Persian prince with a short dark curled beard and a soft felt cap, riding a horse across the Fars plains at the head of horsemen@@CIRO",
  "world_known|An ancient landscape seen from a mountain top by a young Persian prince: far away a Greek city, a Babylonian ziggurat and Egyptian pyramids")

# ───────────────────────── 3. O CILINDRO ─────────────────────────
cap("3. O Cilindro")
b("O Cilindro. Em quinhentos e cinquenta e nove antes de Cristo, Ciro vira rei. Em vinte anos, ele engole a Média, a Lídia e a Babilônia.",
  f"cyrus_throne|{CIRO}, sitting on a throne in a hall with stone columns",
  "median_capital|Ancient Persian soldiers entering the Median capital Ecbatana, a fortified city with walls on a hill@@MÉDIA",
  "croesus|King Croesus of Lydia in rich robes surrounded by gold coins, looking worried as Persian soldiers arrive@@LÍDIA",
  "babylon_gate|Ancient Persian soldiers marching into Babylon through the blue glazed Ishtar Gate decorated with yellow dragons and bulls@@BABILÔNIA", card="559 a.C.")
b("Ele deixa os povos com seus deuses e suas línguas. Os judeus exilados na Babilônia podem voltar para casa. Na Bíblia, Isaías chama Ciro de messias.",
  "gods_return|Babylonian priests carrying statues of their gods back into a temple in a joyful procession@@TOLERÂNCIA",
  "exiles_return|Ancient Jewish families with donkeys and carts leaving Babylon on a road toward the west, joyful@@VOLTA A JERUSALÉM",
  f"cyrus_temple|{CIRO}, respectfully visiting a temple, bowing to priests",
  "isaiah_scroll|An ancient Hebrew prophet with a white beard holding a scroll, a vision of a Persian king in the clouds behind him@@ISAÍAS 45", card="539 a.C.")
b("Ele registra isso num barril de argila, o Cilindro de Ciro. Você talvez já tenha ouvido que é a primeira carta de direitos humanos.",
  "cylinder_clay|Ancient Babylonian scribes pressing cuneiform wedges into a wet clay barrel cylinder",
  "cylinder_museum|The Cyrus Cylinder, a barrel-shaped clay cylinder covered in tiny cuneiform wedges, in a glass case in a museum@@CILINDRO DE CIRO",
  "un_replica|A replica of a barrel-shaped clay cylinder displayed in a glass case in a modern international building hallway, diplomats walking by@@A FAMA",
  "cylinder_reading|A museum curator with glasses reading a clay cylinder with a magnifying glass, raising an eyebrow")
b("[curious] Não é. É uma peça de fundação, enterrada num muro, e quase todo o texto é o rei se elogiando.",
  "buried_wall|Ancient workers placing a clay cylinder inside the foundation of a city wall in Babylon",
  f"cyrus_proud|{CIRO}, puffing his chest proudly while a scribe writes, comic@@PROPAGANDA REAL",
  "cylinder_scribe|A bored Babylonian scribe writing long flattering praise on clay while a king listens with satisfaction")
b("Essa fama nasce no século vinte, com o último xá.",
  f"shah_cylinder|{SHAH71}, presenting a replica of a barrel-shaped clay cylinder at a ceremony@@1971",
  "cylinder_stage|A huge illuminated replica of a barrel-shaped clay cylinder on a stage with spotlights, a crowd applauding")
b("Mas, sem o mito, sobra algo raro no mundo antigo: devolver deuses e povos para casa. E o império de Ciro vai virar uma máquina.",
  "pasargadae|The tomb of Cyrus the Great at Pasargadae: a simple stepped stone house-shaped tomb on an open plain@@PASÁRGADA",
  "machine_gears|An ancient Persian empire shown as a giant machine of wooden gears with roads and messengers, a king turning a big wheel",
  "cyrus_throne@@CIRO, O GRANDE")

# ───────────────────────── 4. O CAVALO ─────────────────────────
cap("4. O Cavalo")
b("O Cavalo. Em quinhentos e vinte e dois antes de Cristo, sete nobres persas precisam escolher um rei. Conta Heródoto que eles decidem no cavalo.",
  "seven_nobles|Seven ancient Persian noblemen in long robes and soft felt caps arguing around a low table in a palace at night",
card="522 a.C.")
b("Vira rei o dono do primeiro cavalo a relinchar ao nascer do sol. O cavalariço de Dario dá um jeitinho, e o dele relincha primeiro.",
  "groom_trick|A clever ancient Persian stable groom secretly whispering to a horse in a stable at night, sneaky and comic@@O CAVALARIÇO",
  "horse_neigh|A white horse rearing and neighing loudly at sunrise while six other Persian noblemen on horses look shocked",
  f"darius_king|{DARIO}, smiling on his white horse at sunrise@@DARIO I")
b("[amazed] É lenda. Mas o que Dario constrói é real. Províncias com governadores, os sátrapas, e imposto fixo. E uma estrada de uns dois mil e quinhentos quilômetros.",
  "map_satrapies|Simple illustrated map of the Achaemenid Persian empire from Egypt and Anatolia in the west to the Indus river in the east, divided into many colored provinces, no labels, no text",
"map_royal_road|Simple illustrated map of a long golden road from the Aegean coast across Anatolia and Mesopotamia to western Iran with small stations along it, no labels, no text")
b("O correio do rei cruza essa estrada trocando de cavalo. E um elogio de Heródoto a esses mensageiros está gravado num correio de Nova York.",
  "relay_station|An ancient Persian royal road relay station: a stone building with stables, a courier jumping from a tired horse onto a fresh one@@ESTRADA REAL",
"ny_post|The grand classical facade of the James A. Farley post office building in New York with a long row of tall columns, blank stone frieze@@NOVA YORK")
b("Pela estimativa mais repetida, e discutida, quase metade da humanidade vive ali. Só uns gregos teimosos não querem entrar.",
  "crowds_empire|A huge crowd of peoples of the ancient Persian empire standing together: Egyptians, Babylonians, Lydians, Indians, Scythians@@44% DA HUMANIDADE?",
  "greek_hills|Ancient Greek hoplites with bronze crested helmets and round shields standing on a rocky hill by the sea, defiant@@OS GREGOS")

# ───────────────────────── 5. AS COLUNAS ─────────────────────────
cap("5. As Colunas")
b("As Colunas. Maratona, Termópilas, os trezentos de Esparta. Quase tudo o que você sabe dessas guerras foi escrito pelo outro lado.",
  "marathon|Battle of Marathon: Greek hoplites charging ancient Persian soldiers with long robes and wicker shields on a beach",
  "thermopylae|Spartan soldiers holding a narrow mountain pass by the sea against a huge ancient Persian army@@TERMÓPILAS, 480 A.C.",
  "greek_writer|An ancient Greek historian writing on a scroll with a smug face while an ancient Persian soldier peeks over his shoulder@@A VERSÃO GREGA")
b("Para a Pérsia, a Grécia é uma fronteira chata. O coração do império é Persépolis. Colunas de uns vinte metros, e povos do mundo inteiro esculpidos na pedra.",
  "xerxes_bored|Xerxes, Achaemenid Persian king with a long square curled beard and a tall golden crown, yawning on his throne while a messenger reports, comic@@XERXES",
  "persepolis_glory|Persepolis in its glory around 500 BC: a huge stone terrace with tall columns topped by double bull capitals, grand staircases, people arriving@@PERSÉPOLIS")
b("Em trezentos e trinta e um antes de Cristo, Alexandre, o Grande, vence o último Dario em Gaugamela. No ano seguinte, Persépolis queima.",
  "alexander|Alexander the Great, a young beardless Macedonian king with wild hair, bronze armor and a plumed helmet, charging on his black horse@@ALEXANDRE",
  "persepolis_fire|The palaces of Persepolis burning at night, flames rising among the columns, Macedonian soldiers watching@@330 A.C.",
  "persepolis_wide")
b("As colunas continuam de pé. Mas os gregos não seguram o planalto. Quem toma a terra de volta é um povo de arqueiros a cavalo.",
  "persepolis_wide@@PERSÉPOLIS, HOJE",
  "parthian_riders|Parthian horse archers in tunics, trousers and soft caps galloping across a plain with bows@@OS PARTOS")

# ───────────────────────── 6. A FLECHA ─────────────────────────
cap("6. A Flecha")
b("A Flecha. Os partos governam o Irã por quase cinco séculos. Em cinquenta e três antes de Cristo, Marco Crasso, o homem mais rico de Roma, vem testá-los.",
  "parthian_riders",
  "crassus|Marcus Crassus, a rich old Roman general with a bald head and a red cloak, pointing east greedily, legionaries behind@@MARCO CRASSO", card="53 a.C.")
b("Em Carras, os arqueiros partos cercam as legiões. Eles fingem fugir e atiram para trás, virados na sela. É o famoso tiro do parto.",
  "arrows_rain|Parthian horse archers circling Roman legionaries in a square formation in the desert, arrows raining down@@CARRAS",
  "parthian_shot|A Parthian horse archer at full gallop turning backwards in the saddle and shooting an arrow behind him@@O TIRO DO PARTO",
  "parthian_riders")
b("Crasso morre ali. Diz a lenda que os partos derramam ouro derretido na boca dele. E o golpe mais humilhante contra Roma ainda está por vir.",
  "molten_gold|A Parthian warrior holding a clay pot of glowing molten gold over a fallen Roman helmet lying in the sand, legend mood, no blood@@DIZ A LENDA",
  "crassus",
  "rock_cliff|A tall sheer cliff face in southern Iran at sunset with carved niches high up, mysterious")

# ───────────────────────── 7. A ROCHA ─────────────────────────
cap("7. A Rocha")
b("A Rocha. Em duzentos e vinte e quatro, assume uma dinastia nova, os sassânidas. Roma e Pérsia viram os dois olhos do mundo.",
  "ardashir|Ardashir I, first Sasanian Persian king, with a curly tied beard and a crown topped by a large round globe with fluttering ribbons, being crowned by a priest",
  "two_eyes|A Roman emperor and a Sasanian Persian king standing on two sides of a round world, facing each other, equal size@@OS SASSÂNIDAS", card="224 d.C.")
b("Em duzentos e sessenta, o rei Shapur Primeiro faz o que ninguém tinha feito. Ele captura vivo um imperador romano, Valeriano.",
  f"shapur|{SHAPUR}, riding a horse at the head of armored cavalry@@SHAPUR I",
  "valerian_captured|Old Roman emperor Valerian in a purple cloak and laurel wreath being taken prisoner by Sasanian soldiers, shocked@@VALERIANO", card="260 d.C.")
b("E manda esculpir a cena num penhasco, em Naqsh-e Rostam, onde ela está até hoje.",
  "naqsh_relief|A huge rock relief carved into a cliff: a Sasanian king on horseback, one Roman emperor kneeling before him and another Roman held by the wrist@@NAQSH-E ROSTAM",
  "rock_cliff")
b("O império segue a religião de Zaratustra: fogo sagrado, céu, inferno e um julgamento final.",
  "fire_temple|A Sasanian fire temple: a domed stone building with a sacred fire burning on an altar inside, priests in white with mouth veils@@ZOROASTRISMO")
b("Muitos estudiosos veem ecos disso no judaísmo e no cristianismo. Mas Pérsia e Roma se esgotam em guerras. E do deserto vem quem ninguém espera.",
"desert_army|Arab horsemen and camel riders appearing over a desert dune at dawn with plain banners@@DO DESERTO",
  "two_eyes")

# ───────────────────────── 8. O MOINHO ─────────────────────────
cap("8. O Moinho")
b("O Moinho. Em seiscentos e trinta e seis, exércitos árabes, unidos pelo islã, vencem os persas em Qadisiya. Seis anos depois, em Nahavand, o exército sassânida acaba.",
  "qadisiya|Battle of al-Qadisiyya: Arab cavalry on horses and camels fighting Sasanian war elephants and armored riders on a dusty plain",
"desert_army@@NAHAVAND, 642", card="636 d.C.")
b("O último rei, Yazdegerd Terceiro, foge por anos. Em seiscentos e cinquenta e um, segundo a crônica, é morto num moinho perto de Merv, pelo próprio moleiro.",
  "yazdegerd_flee|Yazdegerd III, the young last Sasanian king with a small beard and a winged crown, fleeing on horseback through a cold dark landscape@@YAZDEGERD III",
  "mill|An old stone watermill by a river near Merv at night, a lantern glowing inside@@MERV, 651")
b("[serious] O império cai em quinze anos. Mas o Irã não vira árabe.",
  "ctesiphon|The Sasanian palace at Ctesiphon with its giant brick arch, abandoned and dusty@@CTESIFONTE")
b("Egito, Síria e Iraque passam a falar árabe. O Irã adota o islã, devagar, ao longo de séculos. Mas não a língua.",
  "map_arabic|Simple illustrated map of the Middle East and North Africa, the lands from Morocco to Iraq colored in one green and the Iranian plateau colored in a different orange, no labels, no text",
  "grandma_stories|A Persian family in the 9th century at home, children listening to their grandmother telling stories by a lamp@@O PERSA RESISTE")
b("E boa parte do motivo cabe num livro.",
  "book_glow|A thick old handwritten Persian manuscript book on a wooden stand glowing softly in a dark room")

# ───────────────────────── 9. O POEMA ─────────────────────────
cap("9. O Poema")
b("O Poema. Por volta de novecentos e setenta e sete, em Tus, vive um proprietário de terras chamado Ferdowsi. Ele começa o Shahnameh, o Livro dos Reis.",
  "tus_gate_caravan",
  f"shahnameh_start|{FERD_M}, starting to write a big book at a low desk on a carpet in a country house near the walled city of Tus@@FERDOWSI",
  "book_glow@@SHAHNAMEH", card="c. 977")
b("Ele junta os mitos e os reis do Irã de antes do islã. Heróis, dragões, o pássaro Simurgh. São uns cinquenta mil dísticos, quase sem palavras árabes.",
  "rostam_dragon|The Persian legendary hero Rostam in a tiger-skin coat and a helmet fighting a green dragon@@ROSTAM",
  "simurgh|The giant mythical bird Simurgh with long colorful feathers carrying a baby on a mountain peak@@SIMURGH",
  "manuscript_pages|Open pages of an ornate Persian manuscript book with gold borders and a painted miniature of a king, the writing areas shown as decorative wavy lines@@50 MIL DÍSTICOS")
b("Leva mais de trinta anos. Ele termina velho e pobre, e dedica a obra a um sultão turco, Mahmud de Ghazni.",
  f"ferdowsi_old|{FERD_V}, worn robe, finishing a huge manuscript in a poor bare room, tired@@C. 1010",
  "mahmud|Sultan Mahmud of Ghazni, a Turkic ruler with a short beard, a large turban with a jewel and a rich brocade robe, on a throne, bored@@MAHMUD DE GHAZNI")
b("Conta a lenda que o sultão paga mal. Anos depois, arrependido, manda a fortuna. Lembra da caravana?",
  f"silver_coins|{FERD_V}, looking offended at a small bag of silver coins handed to him by a court messenger",
  "tus_gate_caravan@@LEMBRA DA CARAVANA?")
b("Na versão mais antiga, a carga nem é ouro. É anil, um corante azul, que vale sessenta mil dinares.",
  "indigo_bales|Camels loaded with bales of deep blue indigo dye, a merchant opening one to show the bright blue cakes@@ANIL")
b("Ela entra por um portão de Tus enquanto o corpo do poeta sai pelo outro. E a filha dele recusa o presente.",
  "funeral_gate",
  "daughter|Ferdowsi's daughter, a Persian woman in a headscarf and long dress, refusing with a raised hand the bundles offered by the sultan's messengers@@A FILHA",
  "coffin_close")
b("[warm] Era isso que estava no caixão. [long-break] Não o ouro. A língua. Mil anos depois, um aluno iraniano ainda entende boa parte dos versos dele.",
  "coffin_light",
  "schoolkids_reading|Iranian schoolchildren today in a classroom reading aloud from a big illustrated book of Persian epic poems, a teacher smiling@@O PERSA VIVO",
  "manuscript_pages")
b("E o persa Al-Khwarizmi escreve, em árabe, o livro que dá nome à álgebra. E o nome dele vira algoritmo.",
  "alkhwarizmi|Al-Khwarizmi, a 9th century Persian scholar with a black beard and a white turban, drawing geometric squares on a large sheet in a library in Baghdad@@AL-KHWARIZMI",
  "phone_algorithm|A Brazilian teenager scrolling on a smartphone at home, a ghostly medieval Persian scholar in a turban smiling behind her@@ALGORITMO")
b("Se você gosta de histórias inteiras em poucos minutos, se inscreva. Porque dois séculos depois, chega do leste um exército que não lê poemas.",
  f"guide_subscribe|{GUIA} waving happily in front of an old map of Persia without text",
  "mongol_horizon|A huge Mongol cavalry army appearing on the eastern horizon of a Persian plain, dust clouds, fur hats@@OS MONGÓIS")

# ───────────────────────── 10. A ÁGUA ─────────────────────────
cap("10. A Água")
b("A Água. Em mil duzentos e dezenove, chegam os mongóis de Gengis Khan. Nishapur, Merv, Herat. Cidades inteiras são arrasadas.",
  "genghis|Genghis Khan on horseback, a Mongol ruler with a thin beard, a fur-trimmed hat and leather armor, looking over a burning city",
  "nishapur_ruin|The ruins of a destroyed medieval Persian city with smoke rising, broken walls and domes@@NISHAPUR", card="1219")
b("Em mil duzentos e cinquenta e oito, cai Bagdá. O número de mortos ainda é discutido. Mas o pior estrago talvez seja a água: sem gente para cuidar, muitos qanats secam.",
  "baghdad_1258|A Mongol army besieging Baghdad, catapults throwing stones at the city walls by the Tigris river@@BAGDÁ, 1258",
  "qanat_collapsed|A collapsed qanat shaft in the desert half filled with sand, a dry channel and a dead orchard nearby@@OS QANATS SECAM",
  "qanat_outlet@@SEM MANUTENÇÃO")
b("E aí acontece algo bem iraniano. Em duas gerações, os conquistadores falam persa, contratam vizires persas e erguem mesquitas persas.",
  "ilkhan_court|A Mongol Ilkhan ruler in a Persian-style palace court, wearing a Mongol hat with a Persian silk robe, listening to a Persian vizier holding a book@@ILKHANATO")
b("[amazed] O Irã não vence os mongóis. Ele os digere. Dois séculos e meio depois, um garoto muda a fé do país inteiro.",
  "conquerors_persian")

# ───────────────────────── 11. O MENINO ─────────────────────────
cap("11. O Menino")
b("O Menino. Em mil e quinhentos e um, um garoto de catorze anos entra em Tabriz à frente de um exército. O nome dele é Ismail.",
  f"ismail_tabriz|{ISMAIL}, entering the city of Tabriz on a horse at the head of warriors with tall red caps",
  "qizilbash|Qizilbash warriors with tall red caps wrapped in white turbans, swords and lances, cheering@@QIZILBASH",
card="1501")
b("Ele se coroa xá e impõe o islã xiita. O problema é que o país, na maioria, é sunita.",
  f"ismail_crowned|{ISMAIL}, being crowned on a throne in a Tabriz palace hall@@TABRIZ")
b("Ele traz clérigos xiitas do Líbano e persegue quem resiste. Em um século, o país vira xiita.",
  "clerics_lebanon|Shiite clerics with turbans and books arriving by camel from the green mountains of Lebanon@@CLÉRIGOS DO LÍBANO",
  "qizilbash")
b("A fronteira entre xiitas e sunitas de hoje tem muito a ver com esse adolescente. Que, aliás, escreve poemas em turco.",
  "map_shia_sunni|Simple illustrated map of the Middle East with Iran colored in one color and the neighboring countries in another, a clear border line, no labels, no text",
  f"ismail_poet|{ISMAIL}, writing poetry by lamplight in a palace garden at night@@POETA, EM TURCO")
b("Seu bisneto, Shah Abbas, leva a capital para Isfahan. Os iranianos dizem que Isfahan é metade do mundo.",
  "abbas|Shah Abbas I, Safavid Persian king with a very long drooping black mustache and no beard, a turban with a feather plume and a rich robe@@SHAH ABBAS",
  "naqsh_jahan|The huge Naqsh-e Jahan square in Isfahan in the 1600s with blue-tiled domes, arcades, polo players and merchants@@ISFAHAN",
card="1598")
b("Depois, essa metade do mundo desmorona. E o que vem a seguir começa com um diamante e termina com um narguilé.",
  "isfahan_falls|Afghan warriors entering a gate of Isfahan in 1722, frightened Persian citizens@@1722",
  "diamond_hookah|A big shining diamond and an old Persian water pipe side by side on a carpet")

# ───────────────────────── 12. O TABACO ─────────────────────────
cap("12. O Tabaco")
b("O Tabaco. Primeiro, o diamante. Em mil setecentos e trinta e nove, Nader Xá invade a Índia e saqueia Délhi.",
  f"nader|{NADER}, on horseback in front of his army",
card="1739")
b("Ele leva o Koh-i-Noor. Se você viu o nosso vídeo da Índia, sabe onde esse diamante vai parar.",
  f"kohinoor|{NADER}, holding up a huge diamond in amazement@@KOH-I-NOOR",
  "diamond_hookah@@NOSSO VÍDEO DA ÍNDIA")
b("Depois dele, os reis Qajar perdem duas guerras para a Rússia, e com elas o sul do Cáucaso.",
  "qajar_king|A Qajar shah of the early 1800s with a very long black beard, a tall black lambskin hat with a jeweled aigrette and a jeweled robe@@DINASTIA QAJAR",
  "map_caucasus|Simple illustrated map of the Caucasus region between the Black Sea and the Caspian Sea, the southern Caucasus lands shaded in red as lost, the north of Iran below, no labels, no text")
b("Em mil oitocentos e noventa, o xá vende a um britânico o monopólio do tabaco do país inteiro.",
  f"naser_shah|{NASER}, signing a document at a desk@@NASER AL-DIN XÁ",
card="1890")
b("Em mil oitocentos e noventa e um, um grande clérigo xiita proíbe o fumo. E o Irã, que fuma muito, para.",
  "cleric_fatwa|A senior Shiite cleric with a white beard and a black turban sitting on a carpet, raising a finger to issue a ruling, students around@@MIRZA SHIRAZI",
  "bazaar_closed|A long covered Persian bazaar with all shops closed and empty, merchants standing with crossed arms, water pipes put away@@BOICOTE", card="1891")
b("Até as mulheres do palácio, dizem, param de fumar. Em semanas, o contrato cai. Um turbante vence uma coroa. Guarde esse tabaco.",
f"shah_cancels|{NASER}, tearing up a document, annoyed@@1892",
  "turban_crown|A black cleric's turban and a jeweled royal crown facing each other on a table, the crown slightly tipped over")

# ───────────────────────── 13. O POÇO ─────────────────────────
cap("13. O Poço")
b("O Poço. Em mil novecentos e um, um britânico, William D'Arcy, ganha o direito de procurar petróleo no Irã. Por sete anos, nada.",
  "darcy|William Knox D'Arcy, a plump Victorian British millionaire with a white mustache in a suit, studying a map without text",
  "drilling_dry|An early 1900s wooden oil derrick in a barren Persian valley, tired British engineers and Persian workers, nothing coming out@@WILLIAM D'ARCY", card="1901")
b("Em mil novecentos e oito, em Masjed Soleyman, a sonda acerta. Dali nasce a empresa que hoje se chama BP. E quase tudo já está assinado para fora.",
  "oil_gusher|A black oil gusher shooting up from a wooden derrick in the Persian hills at dawn, workers celebrating@@MASJED SOLEYMAN",
"oil_feet|A Persian man looking down at black oil bubbling between his feet, while a British businessman behind him holds up a contract@@O CONTRATO", card="1908")
b("Em mil novecentos e vinte e cinco, um oficial cossaco vira rei, Reza Xá. Ferrovia, universidade, exército moderno, tudo à força.",
  f"reza_shah|{REZA}, standing in a palace hall@@REZA XÁ",
card="1925")
b("Em mil novecentos e trinta e cinco, ele faz um pedido. Lembra do nome? O mundo agora deve dizer Irã, e não Pérsia.",
  f"reza_letter|{REZA}, handing a sealed letter to foreign diplomats in a palace hall@@1935",
  "map_iran_name",
  "name_valley@@TERRA DOS ÁRIAS", card="1935")
b("Seis anos depois, britânicos e soviéticos invadem e o tiram do trono. Fica o filho, Mohammad Reza.",
  "invasion_1941|British and Soviet soldiers with tanks meeting on a dusty Iranian road in 1941@@1941",
  "young_shah|Young Mohammad Reza Shah, 21 years old, with slicked-back dark hair, in a military uniform, nervously taking an oath@@MOHAMMAD REZA XÁ")
b("Em mil novecentos e cinquenta e um, o primeiro-ministro Mossadegh nacionaliza o petróleo. Em agosto de cinquenta e três, um golpe o derruba, com propaganda e multidões pagas.",
  f"mossadegh|{MOSSA}, giving a passionate speech to a crowd@@MOSSADEGH",
"coup_tanks|Tanks and soldiers in the streets of Tehran in August 1953, a crowd running@@AGOSTO DE 1953")
b("Por sessenta anos, isso é negado. [long-break] Em dois mil e treze, a CIA admite em documentos: o golpe foi feito sob direção dela.",
  "mossadegh_arrest|Mohammad Mossadegh, an elderly bald man with a long nose, sitting alone in pajamas under house arrest in a village house, sad@@PRISÃO DOMICILIAR",
  "cia_docs|A stack of declassified documents with blacked-out lines on a desk in a modern archive, a hand lifting one page@@CIA, 2013", card="2013")
b("Muitos historiadores veem aqui a raiz da desconfiança entre Irã e Estados Unidos. E o xá que fica vai dar uma festa.",
  "cia_docs",
  "young_shah")

# ───────────────────────── 14. AS FITAS ─────────────────────────
cap("14. As Fitas")
b("As Fitas. Mil novecentos e setenta e um. O xá comemora dois mil e quinhentos anos de monarquia nas ruínas de Persépolis.",
  "party_tents|A luxurious tent city set up next to the ruins of Persepolis in 1971, golden tents and lights, guests in gowns and uniforms arriving",
  f"shah_1971|{SHAH71}, greeting foreign kings in front of a golden tent@@O XÁ",
  "persepolis_wide", card="1971")
b("Comida vinda de Paris, enquanto muitas aldeias nem têm luz elétrica.",
  "banquet|A lavish banquet in a huge tent, French waiters serving silver plates, champagne and chandeliers@@MAXIM'S DE PARIS",
  "village_dark|A poor Iranian village at night in 1971 with mud houses lit only by oil lamps")
b("De longe, um clérigo exilado chama aquilo de festa do diabo. É Ruhollah Khomeini, e seus sermões entram no Irã em fitas cassete.",
  f"khomeini_exile|{KHOM}, speaking in a modest room with a carpet, in exile@@KHOMEINI",
  "cassettes|Hands secretly passing cassette tapes in a crowded Tehran bazaar in the 1970s@@FITAS CASSETE")
b("[serious] Lembra do tabaco? De novo, um turbante enfrenta uma coroa. Em janeiro de mil novecentos e setenta e nove, o xá sai do Irã para não voltar.",
  "turban_crown@@LEMBRA DO TABACO?",
  "protests_1978|Huge crowds of men and women marching in the streets of Tehran in 1978, raised fists, the white Azadi tower in the background@@TEERÃ, 1978",
  "shah_leaves|Mohammad Reza Shah with grey slicked-back hair and his wife walking toward a plane at an airport, sad, winter@@JANEIRO DE 1979", card="1979")
b("Em fevereiro, Khomeini volta de Paris. Em abril, o país vira uma República Islâmica.",
  f"khomeini_plane|{KHOM}, stepping down the stairs of a passenger plane at Tehran airport, a huge crowd waiting@@FEVEREIRO DE 1979")
b("Em novembro, estudantes tomam a embaixada americana. Cinquenta e dois reféns ficam presos por quatrocentos e quarenta e quatro dias.",
  "embassy|Young students climbing over the gate of a walled embassy compound in Tehran in 1979, no flags@@EMBAIXADA DOS EUA")
b("No ano seguinte, Saddam Hussein invade. A guerra Irã–Iraque dura oito anos, e as estimativas começam em meio milhão de mortos.",
  "saddam|Saddam Hussein, Iraqi leader with a thick black mustache and an olive military uniform, pointing at a map without text@@SADDAM HUSSEIN",
  "trenches|Soldiers in muddy trenches in a flat marshland during the Iran–Iraq war, barbed wire, smoke@@1980–1988", card="1980")
b("O Iraque usa armas químicas. Meninos voluntários atravessam campos minados, alguns, segundo relatos, com chaves de plástico no pescoço.",
  "gas_masks|Iranian soldiers putting on gas masks as a yellow cloud drifts over the trenches@@ARMAS QUÍMICAS",
  "plastic_keys|Close-up of a small cheap plastic key on a string around a boy's neck, dust, sad mood, no face visible@@CHAVES DE PLÁSTICO")
b("Diziam que elas abriam o paraíso. Em mil novecentos e oitenta e oito, Khomeini aceita o cessar-fogo, e diz que é como beber veneno.",
  "paradise_word#detalhe-centro",
  "khomeini_exile@@CESSAR-FOGO", card="1988")
b("Ele morre no ano seguinte. O novo líder supremo é Ali Khamenei.",
  "khamenei|Ali Khamenei in 1989, a Shiite cleric with a black beard, a black turban, large glasses and a brown cloak@@ALI KHAMENEI", card="1989")

# ───────────────────────── 15. O LENÇO ─────────────────────────
cap("15. O Lenço")
b("O Lenço. Em dois mil e nove, uma eleição contestada põe milhões nas ruas.",
  "green_movement|A huge peaceful crowd in Tehran in 2009 wearing green wristbands and green scarves, a silent march",
  "tehran_today@@ELEIÇÃO DE 2009", card="2009")
b("Setembro de dois mil e vinte e dois. Mahsa Amini, de vinte e dois anos, morre sob custódia da polícia da moralidade.",
  "candle_scarf|A single white candle and flowers on a Tehran sidewalk at night, a headscarf laid beside them, mourning@@MAHSA AMINI",
card="2022")
b("Ela tinha sido presa por causa do véu. O país explode. Mulheres tiram o lenço e cortam o cabelo em público.",
  "scarves_up|Iranian women in a street protest waving their headscarves in the air, men beside them",
  "hair_cut|A woman seen from behind cutting a lock of her own long hair with scissors in public, a crowd around her, defiant@@PROTESTOS")
b("O lema vem do movimento das mulheres curdas. Mulher, vida, liberdade. Mais de quinhentas pessoas morrem, segundo ONGs, e cerca de vinte mil são presas.",
  "kurdish_women|Kurdish women in traditional colorful dresses marching in a mountain town in western Iran@@MULHER, VIDA, LIBERDADE",
  "arrests|Riot police in black detaining protesters in a Tehran street at night, motorcycles@@CERCA DE 20 MIL PRESOS",
  "scarves_up@@MAIS DE 500 MORTOS")
b("Três anos depois, a guerra chega pelo céu.",
  "night_sky|A night sky over Tehran with streaks of light, the city below and the Alborz mountains in silhouette")

# ───────────────────────── 16. O FILHO ─────────────────────────
cap("16. O Filho")
b("O Filho. Junho de dois mil e vinte e cinco. Irã e Israel travam uma guerra de doze dias, que termina num cessar-fogo.",
  "missiles_night|Missiles and interceptor trails crossing a night sky over a mountainous landscape, flashes on the horizon",
card="2025")
b("Ele não dura. Vinte e oito de fevereiro de dois mil e vinte e seis. Um ataque dos Estados Unidos e de Israel mata Ali Khamenei.",
  "tehran_strike|Smoke rising over a district of Tehran seen from far away, the Alborz mountains behind, grey day@@TEERÃ",
  "empty_chair|An empty ornate armchair in a quiet hall with a black cleric's cloak folded on it, soft light@@37 ANOS NO PODER", card="28/02/2026")
b("Oito dias depois, a Assembleia dos Especialistas escolhe o novo líder supremo. [long-break] É o filho dele, Mojtaba Khamenei.",
  "assembly|An assembly of elderly Shiite clerics in black and white turbans seated in rows in a large hall, voting by raising hands@@ASSEMBLEIA DOS ESPECIALISTAS",
  "mojtaba|Mojtaba Khamenei, a middle-aged Shiite cleric with a grey-black beard, a black turban and glasses, standing in a hall, serious@@MOJTABA KHAMENEI", card="08/03/2026")
b("[serious] Uma revolução feita contra a monarquia hereditária acaba passando o poder de pai para filho. Até a gravação deste vídeo, não há acordo de paz.",
"turban_crown@@DE PAI PARA FILHO",
  "city_waiting|Tehran today at dusk, people on a street looking at their phones with worried faces@@ATÉ A GRAVAÇÃO")

# ───────────────────────── FECHO ─────────────────────────
cap("Fecho")
b("[warm] Agora volte a Tus. O túmulo de Ferdowsi fica num jardim, com água correndo em canais. Um pequeno paraíso.",
  "ferdowsi_tomb|The white stone mausoleum of Ferdowsi in Tus, Iran: a square monument with columns on a stepped base, surrounded by a garden with pools and water channels",
"persian_garden")
b("O império cai, a religião muda, a fronteira encolhe, o nome some e volta. E a língua de Ferdowsi segue viva.",
  "conquerors_leave", "map_plateau", "schoolkids_reading@@1000 ANOS DEPOIS")
b("Tão viva que você fala persa sem saber. Paraíso, laranja, azul, bazar. E xeque, que vem de xá, o rei.",
  "oranges|A Brazilian street market stall with piles of oranges, blue tiles on the wall behind, people shopping@@LARANJA, AZUL, BAZAR",
  "chess|A chess game on a table with the black king toppled over, an old Persian man in robes and a modern Brazilian kid playing@@XEQUE = XÁ, O REI")
b("E aquela fila de camelos do começo, entrando por um portão de Tus, também tem nome persa: caravana, de karvan.",
  "caravan_chests", "tus_gate_caravan@@CARAVANA = KARVAN", "caravan_camels")
b("Exércitos conquistam o Irã. A língua do Irã conquista os exércitos.",
  "conquerors_persian", "persepolis_wide")
b("E você? Qual palavra persa você já disse hoje sem perceber? Conta aqui nos comentários.",
  f"guide_comment|{GUIA} sitting under a pomegranate tree in a Persian garden, thinking, holding an orange",
  "ferdowsi_tomb")

# blocos que abrem uma ideia nova (o build.py põe ~0,9 s antes deles; antes de capítulo já são ~1,5 s)
IDEIA = {3, 9, 10, 12, 14, 18, 19, 25, 26, 29, 30, 34, 38, 42, 47, 48, 51, 52, 53, 56, 59, 61, 62, 65, 66, 67, 72, 73, 75, 76, 79, 80, 81, 84, 89, 92, 96, 98, 101, 102}

THUMB = {"id": "thumb-base", "qualidade": "high",
         "prompt": "The ruins of Persepolis filling the left third of the frame: the Gate of All Nations with two giant human-headed winged bull statues and tall stone columns on a stone terrace, warm golden afternoon light, mountains behind; the right half of the image is open clear blue sky with a few small white clouds and lots of empty space, no people, no text"}

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
        blocos.append({"id": bid, "texto": blk["t"], "ideia": n in IDEIA})
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
    cenas.append(THUMB)
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
