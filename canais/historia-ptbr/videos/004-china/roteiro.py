#!/usr/bin/env python3
"""Fonte única do 004-china (05/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

Molde History in Minutes (canais/historia-ptbr/biblia/roteiro.md; referência de código: videos/003-ira v2):
  hook (anedota do elixir de Qin Shi Huang: o homem que queria viver para sempre e o túmulo que ninguém abriu)
  → "Essa é a história inteira da China" → pergunta central ("morreu mais vezes que qualquer país… e sempre voltou. Como?")
  → promessa em lista → "guarde essa ideia (o Céu dá, o Céu tira) e esse túmulo fechado"
  → 10 eras ligadas por "mas… então…" (título-frase só na placa, nunca falado)
  → fecho que paga o túmulo fechado e o Mandato do Céu.
Fio condutor: o MANDATO DO CÉU (o Céu dá o direito de mandar e pode tirar; os sinais são enchente, fome e revolta).
Fio secundário: a máquina que sobrevive às famílias (uma escrita, um centro, a prova de seleção). Loops: túmulo, escrita, papel-moeda, prata, Puyi.

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="221 a.C.") · texto que começa com "§ " abre ideia nova (~0,9 s antes) · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco (técnica B2 do 003), gaps 0,35/0,9/1,5 s no build.py, tags de tom só onde a emoção muda.
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (003 v2: 2.282 palavras em 18:01 com as pausas)
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
TITULO = "A história INTEIRA da China"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None):
    ideia = t.startswith("§")
    B.append({"t": t.lstrip("§ ").strip(), "s": list(s), "card": card, "ideia": ideia})

# Mapas sem texto (rótulos no código, src/labels.jsx) e regra de "sem escrita" em objetos com inscrição
MAPA = ("painted like a blank parchment terrain map seen from directly above, only coastlines, rivers, mountains and flat colored areas, "
        "completely blank with no writing anywhere, no letters, no words, no labels, no symbols, no compass, no border, no frame")
SEMTXT = ", no readable writing, no Chinese characters, no letters anywhere"
# Personagens (regra da bíblia: nada de rosto descrito; "round-white-head cartoon …"; figuras modernas sem nome no prompt)
QIN = "Qin Shi Huang as a round-white-head cartoon emperor with a simple flat black beard shape, a flat black board crown with hanging bead strings in front and a black robe with red trim"
QIN_OLD = "Qin Shi Huang as a tired older round-white-head cartoon emperor with a simple flat grey beard shape, a flat black board crown with hanging bead strings and a black robe with red trim"
SHANG_KING = "a round-white-head cartoon Bronze Age Shang king with a simple flat beard shape, a tall bronze headdress and a dark robe with bronze ornaments"
ZHOU_KING = "a round-white-head cartoon Zhou king with a simple flat beard shape, a tall black hat and a red robe"
CONFUCIO = "Confucius as an old round-white-head cartoon teacher with a simple flat long white beard shape, a black scholar cap and a plain grey robe"
LIU = "Liu Bang as a round-white-head cartoon village official with a simple flat beard shape, a simple straw hat and a patched brown tunic"
HAN_EMP = "a round-white-head cartoon Han emperor with a simple flat beard shape, a flat black board crown with bead strings and a yellow robe"
WU = "Wu Zetian as a round-white-head cartoon empress with a tall golden phoenix headdress and a red and gold robe"
ZHU = "a round-white-head cartoon beggar monk with a shaved round head, a patched grey robe and a wooden begging bowl"
ZHU_EMP = "a round-white-head cartoon Ming emperor with a shaved look under a black winged hat, a simple flat beard shape and a yellow dragon robe"
ZHENG = "Admiral Zheng He as a big round-white-head cartoon admiral with a red official robe and a black winged hat"
LIN = "Lin Zexu as a round-white-head cartoon Qing official with a simple flat beard shape, a round red-tasseled hat and a blue robe with a square badge"
HONG = "Hong Xiuquan as a round-white-head cartoon scholar with a simple flat beard shape, a yellow headscarf and a yellow robe"
PUYI = "a tiny round-white-head cartoon boy emperor, about three years old, in a huge yellow dragon robe and a small round hat, sitting on a giant throne"
PUYI_OLD = "an old round-white-head cartoon gardener with round glasses and a plain blue worker jacket, watering flowers"
LIDER49 = "a round-white-head cartoon communist leader with a big forehead, combed-back black hair and a grey buttoned tunic suit"
DENG = "a short round-white-head cartoon old leader with short grey hair and a dark buttoned suit"
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes"

# ───────────────────────── HOOK (anedota do elixir de Qin Shi Huang) ─────────────────────────
cap("Hook")
b("[serious] China, duzentos e dez antes de Cristo. O homem mais poderoso da Terra está morrendo… e ele tem um plano para não morrer.",
  f"qin_sick|{QIN_OLD}, lying pale and sick on a bed in a dark palace room, servants with lanterns around him, worried",
  "palace_night|A huge ancient Chinese palace of wood and black roof tiles at night under the moon, lanterns glowing, guards on the walls",
  f"qin_plan|{QIN_OLD}, sitting up in bed with a sly determined look, pointing a finger upward, lamplight",
  "elixir_bottle|A small glowing gourd bottle and a bowl of shiny silver pills on a lacquered table in candlelight, mysterious" + SEMTXT, card="210 a.C.")
b("Ele unificou a China. Agora, só quer uma coisa: viver para sempre.",
  "map_unified|Map of ancient China as one united land painted in black and gold between the Yellow River and the Yangtze river, the rest pale, " + MAPA,
  f"qin_forever|{QIN}, standing on a palace terrace looking at the stars with open arms, dreaming",
  "hourglass_qin|An ancient Chinese bronze water clock dripping in a dark palace hall, dramatic light")
b("Mandou navios atrás da ilha dos imortais. Nunca voltaram. Então, os médicos lhe deram pílulas… de mercúrio.",
  "ships_immortals|Ancient Chinese wooden ships with square sails leaving the coast at dawn, carrying many young boys and girls, heading for misty islands far away",
  "immortal_island|A magical misty island with mountains floating in the clouds, a palace on top, glowing peaches, dreamy",
  "doctor_pills|An ancient Chinese court alchemist with a long sleeved robe proudly offering a tray of shiny silver pills to an emperor, comic suspense",
  "mercury_drop|Close view of a drop of shiny liquid mercury rolling on a bronze plate, silver reflections")
b("[amazed] Morreu aos quarenta e nove anos. Tinha prometido uma dinastia de dez mil gerações… ela durou quinze anos.",
  "qin_dead|An empty imperial bed with the black board crown with bead strings lying on the pillow, servants bowing, dark room",
  "ten_thousand|An endless line of tiny cartoon emperors with black board crowns stretching to the horizon in a dream cloud, then the line is cut short after a few figures",
  "palace_fall|An ancient Chinese palace burning at night, rebels with spears running through the gate",
  "fish_cart|An ancient Chinese imperial carriage on a dusty road followed by a cart piled high with salted fish, officials holding their noses, comic")
b("E o túmulo dele, guardado por um exército de barro… ninguém abriu até hoje.",
  "terracotta_rows|Rows and rows of terracotta warriors standing in an excavation pit, warm light, archaeologists tiny in the distance",
  "tomb_mound|A huge green pyramid-shaped hill covered in pomegranate trees in a flat plain, mountains behind, a quiet modern fence around it",
  "terracotta_face|Close view of a cartoon terracotta warrior statue with a round head and a calm clay face, dust in the light")
b("§ [serious] Essa é a história inteira da China: o país que morreu mais vezes do que qualquer outro… e sempre voltou. Como?",
  "dynasties_parade|A parade of many Chinese emperors from different ages in different robes and crowns walking one after another across a long bridge, each one falling off and the next one taking his place, comic",
  "china_shatter|A big porcelain vase painted with a map-like landscape cracked into pieces and floating apart, then glued back together with gold lines, dramatic",
  "great_wall_wide|The Great Wall of China winding over green mountains at sunrise, wide view",
  "shanghai_today|Modern Shanghai skyline today with tall towers by the river at dusk, boats on the water")
b("No caminho: reis que faziam perguntas aos avós mortos, a única mulher que reinou como imperador… e o último imperador, que virou jardineiro.",
  f"shang_ask|{SHANG_KING} holding a cracked turtle shell over a fire, ghostly ancestors in the smoke above him",
  f"wu_throne|{WU}, sitting alone on the dragon throne, confident, ministers bowing",
  "fleet_giant|A fleet of gigantic ancient Chinese treasure ships with many red sails on the open ocean, small ships around them",
  "fleet_home|Giant Chinese treasure ships rotting at anchor in a harbor, sails folded, grass growing on the dock",
  "puyi_garden|An old round-white-head cartoon gardener with round glasses watering flowers in a botanical garden, a little imperial dragon crown on the ground beside him, ironic")
b("§ E tudo gira em torno de uma ideia: o Céu dá o direito de mandar… e o Céu pode tirar. Guarde essa ideia, e esse túmulo fechado.",
  "crown_float|An ancient Chinese imperial crown floating in a beam of golden light between storm clouds, symbolic",
  "terracotta_dark|Terracotta warriors standing in the dark with a single lantern light, watching over a closed hill, mysterious",
  "heaven_gives|A golden ray of light from the clouds falling on a Chinese king kneeling on a hill, his people around him",
  "heaven_takes|Dark storm clouds over an ancient Chinese palace, lightning, a flooded river and a crown falling",
  "tomb_door|A closed ancient stone door deep underground, with a bronze lock shaped like a dragon, faint silver glow from the cracks" + SEMTXT)

# ───────────────────────── 1. PERGUNTAS PARA OS MORTOS ─────────────────────────
cap("1. Perguntas para os mortos")
b("Antes de qualquer imperador, havia um rio: o Amarelo, cor de barro, que dava a colheita… e afogava aldeias inteiras.",
  "map_rivers|Map of eastern China with the Yellow River painted ochre yellow in the north and the Yangtze river painted blue in the south, mountains in the west, the sea on the east, " + MAPA,
  "yellow_river|The Yellow River in China: a wide muddy ochre river winding through yellow loess hills, terraced fields",
  "loess_farmers|Ancient Chinese farmers with hoes planting millet on yellow soil terraces beside a muddy river",
  "river_flood|A muddy yellow river bursting its banks and flooding a village of thatched huts, people fleeing with baskets", card="c. 1600 a.C.")
b("A lenda conta que um herói chamado Yu domou as enchentes e, por isso, ganhou o direito de reinar. Lenda ou não, a ideia ficou: quem doma as águas merece mandar.",
  "yu_dig|A legendary Chinese hero with a straw hat and a shovel leading workers digging channels to drain a great flood, heroic@@YU, O GRANDE",
  "dyke_ruler|An ancient Chinese ruler standing on a river dyke giving orders while hundreds of workers carry baskets of earth",
  "yu_years|A tired legendary Chinese hero walking past his own house while his family waves at the door, rain falling, comic and touching",
  "flood_tamed|Calm green fields and canals where a flood used to be, farmers celebrating a hero on their shoulders")
b("§ A primeira dinastia que a gente consegue ler é a dos Shang. E o jeito de ler é estranho: ossos.",
  "shang_bronze|Shang dynasty craftsmen pouring molten bronze into clay molds to make a big ritual cauldron, sparks and glow",
  f"shang_king|{SHANG_KING}, sitting in a wooden hall with bronze cauldrons around him@@OS SHANG",
  "shang_city|An ancient Shang capital city of rammed-earth walls and thatched wooden halls beside a river, bronze workers and chariots",
  "bones_pile|A pile of old turtle shells and ox shoulder bones covered in scratched lines on a dark table" + SEMTXT)
b("O rei queria saber se ia chover, se a colheita vinha, se a guerra dava certo. E perguntava… aos avós mortos.",
  "shang_harvest|Shang farmers looking at thin millet crops and then up at their king on a terrace, hopeful",
  "shang_rain|A worried Shang king looking up at a cloudless sky over dry fields",
  "ancestors_ghost|Friendly ghostly ancestors in old robes floating in incense smoke above a bronze altar, listening",
  "shang_war|Shang bronze age chariots and soldiers with halberds lining up for battle, the king pointing")
b("Os adivinhos esquentavam um casco de tartaruga até ele rachar. O rei lia a rachadura, e a pergunta era gravada no próprio osso.",
  "read_crack|A Shang king and a diviner leaning over a cracked turtle shell by firelight, reading it with serious faces",
  "shell_fire|An ancient Chinese diviner pressing a hot bronze rod against a turtle shell, smoke rising, a crack appearing",
  "crack_close|Close view of a turtle shell with a fresh crack running across it in firelight" + SEMTXT,
  "carve_bone|An ancient scribe carving small marks into an ox shoulder bone with a bronze knife, concentrated" + SEMTXT)
b("§ Três mil anos depois, em mil oitocentos e noventa e nove, farmácias de Pequim vendiam esses ossos moídos como remédio: ossos de dragão.",
  "pharmacy_old|An old Chinese pharmacy around 1899 with wooden drawers, jars and a pharmacist grinding bones with a mortar" + SEMTXT,
  "dragon_bones|A paper packet of medicine opened on a counter, revealing pieces of old bone with scratched marks, a small cartoon dragon drawn on the paper" + SEMTXT,
  "scholar_sick|A Qing dynasty scholar with a round hat sick in bed with fever, looking at a piece of bone with wide eyes@@OSSOS DE DRAGÃO", card="1899")
b("Conta a história que um estudioso doente olhou o remédio… e viu escrita. A escrita mais antiga da China.",
  "scholar_magnifier|A Qing scholar holding a magnifying glass over a piece of old bone, amazed, mouth open",
  "bones_museum|Many oracle bone fragments in a museum glass case, visitors looking at them" + SEMTXT,
  "writing_tree|A tree whose roots are old scratched bones and whose branches turn into brushes and books, symbolic" + SEMTXT)
b("E ela nunca parou. Uma criança chinesa de hoje ainda reconhece alguns desses sinais. Guarde essa escrita.",
  "kid_reading|A modern Chinese schoolgirl with a backpack looking at an old bone in a museum and pointing, delighted",
  "brush_today|A modern Chinese student painting with a brush and black ink on white paper at a school desk" + SEMTXT,
  "thread_glow|A long golden thread running through many ancient Chinese objects, from a bone to a scroll to a modern book, symbolic")
b("Mas os Shang tinham um vizinho que queria o trono. E ele precisava de uma boa desculpa.",
  "shang_feast|A Shang king feasting carelessly in his hall with wine and music, unaware",
  "zhou_plot|Zhou nobles around a campfire at night pointing at a map drawn in the dirt, plotting",
  "zhou_watch|Zhou dynasty warriors on a hilltop at dusk looking down at a Shang city, their leader stroking his beard, scheming")

# ───────────────────────── 2. O CÉU MUDA DE IDEIA ─────────────────────────
cap("2. O Céu muda de ideia")
b("Por volta de mil e quarenta e seis antes de Cristo, os Zhou derrubaram os Shang. Mas derrubar um rei à força faz de você… um ladrão.",
  "zhou_gate|Zhou soldiers pouring through the broken gate of a Shang palace, bronze cauldrons tipped over",
  "muye_battle|A big Bronze Age battle on a plain: Zhou chariots charging against a Shang army, dust and banners with no writing",
  f"zhou_king|{ZHOU_KING}, standing over a broken Shang bronze cauldron, looking a little guilty@@OS ZHOU",
  "thief_look|A Zhou king sneaking away holding a Shang crown, peasants pointing at him, comic", card="c. 1046 a.C.")
b("Então eles inventaram uma explicação genial: o Mandato do Céu. O Céu escolhe um governante justo. Quando ele fica cruel ou preguiçoso, o Céu muda de ideia.",
  "mandate_scroll|A golden scroll of light coming down from the clouds to a Zhou king on a mountain, heavenly glow" + SEMTXT,
  "lazy_king|A lazy cruel Shang king lounging on cushions eating grapes while dark clouds gather over his palace",
  "heaven_change|Golden light from the sky leaving one king and moving to another man on a far hill, symbolic@@MANDATO DO CÉU")
b("E como saber? Pelos sinais: enchente, seca, fome… e revolta. Se tudo isso aparece, o Céu já foi embora.",
  "signs_flood|A village half underwater in a muddy flood, people on the rooftops",
  "signs_drought|Cracked dry fields under a burning sun, a starving family with empty bowls",
  "signs_revolt|Angry ancient Chinese peasants with pitchforks and torches marching to a palace gate")
b("§ A ideia tinha uma brecha: quem ganhasse a guerra podia dizer que o Céu tinha mudado de lado. E todo mundo usou essa brecha, por três mil anos.",
  "loophole|Two ancient Chinese generals on opposite hills both pointing at the same sky, each claiming heaven, comic")
b("Os Zhou deixaram também o nome mais antigo da China, num vaso de bronze: Zhongguo, o país do meio.",
  "he_zun|An ancient bronze wine vessel with animal masks on it in a museum case, lit dramatically" + SEMTXT,
  "scrap_yard|A 1960s Chinese scrapyard with piles of metal junk, a worker holding up an ancient bronze vessel, surprised@@ZHONGGUO = PAÍS DO MEIO")
b("§ Mas os Zhou foram perdendo a força, e o reino se partiu em séculos de guerra.",
  "map_warring|Map of ancient China divided into seven large colored regions with mountains and rivers between them, " + MAPA,
  "warring_states|Armies of the warring states of China clashing with crossbows, chariots and halberds in a valley", card="475 a.C.")
b("No meio desse caos, Confúcio ensinava que a ordem começa no dever: filho com pai, súdito com rei… e rei com o povo.",
  f"confucius|{CONFUCIO}, teaching a small group of students under a tree@@CONFÚCIO")
b("Os rivais foram se engolindo, até que o mais duro de todos resolveu acabar com a brincadeira.",
  "seven_kings|Seven ancient Chinese kings at a round table glaring at each other, one in black at the end smiling coldly",
  "qin_army|A huge disciplined army in black armor marching in perfect rows out of a mountain pass, crossbows raised")

# ───────────────────────── 3. UM IMPERADOR, UM PADRÃO ─────────────────────────
cap("3. Um imperador, um padrão")
b("Era o reino de Qin. Em duzentos e vinte e um antes de Cristo, o rei Ying Zheng venceu o último rival e virou o Primeiro Imperador.",
  f"qin_young|{QIN}, younger and stern, standing on a war chariot in front of his black army@@YING ZHENG",
  f"qin_title|{QIN}, sitting on a raised throne while hundreds of officials bow down in a vast hall@@QIN SHI HUANG", card="221 a.C.")
b("É dele, provavelmente, que vem o nome China. Qin.",
  "map_unified",
  "name_travel|Merchants with camels carrying a glowing word westward along a desert road from China to Persia and India, symbolic" + SEMTXT)
b("§ E tratou a China como um sistema: uma só escrita, uma só moeda, os mesmos pesos, e até a mesma largura de eixo nas carroças.",
  "one_script|Ancient Chinese scribes copying the same simple marks on bamboo strips in a big hall, all identical" + SEMTXT,
  "coins_qin|Round bronze ancient Chinese coins with square holes in the middle stacked on a table",
  "cart_axles|Ancient Chinese carts all with the same wheel width rolling in the same grooves on a road, an official measuring with a stick, comic")
b("Ligou muralhas, abriu estradas… e queimou os livros de que não gostava.",
  "wall_build|Thousands of workers building a rammed-earth wall over mountains under guards, ancient China",
  "book_burning|Qin soldiers throwing bundles of bamboo books into a big bonfire while scholars cry")
b("§ Lembra do homem do começo? Ele tinha vencido todo mundo. Só faltava vencer a morte.",
  f"qin_mirror|{QIN_OLD}, looking at his grey beard in a bronze mirror, worried",
  "skeleton_shadow|The shadow of a skeleton on the palace wall behind a powerful emperor, dramatic")
b("Morreu numa viagem. Os ministros esconderam a morte e, para disfarçar o cheiro do corpo, puseram uma carroça de peixe salgado junto da dele.",
  "fish_cart",
  "ministers_secret|Two ancient Chinese ministers whispering in a dark tent beside a covered carriage, scheming",
  "summer_road|A long imperial procession on a hot dusty summer road, flags, sweat, flies around a carriage")
b("Foi enterrado num túmulo que, segundo o historiador Sima Qian, tinha rios de mercúrio. E isso pode não ser lenda: o solo em cima tem mercúrio muito acima do normal.",
  "tomb_inside|Imagined inside of a huge ancient Chinese underground tomb: a giant map of mountains with silver rivers of mercury flowing, a ceiling with pearls as stars" + SEMTXT,
  "sima_qian|An ancient Chinese historian with a simple flat beard shape writing on bamboo strips by lamplight" + SEMTXT + "@@SIMA QIAN")
b("§ O exército de barro só apareceu em mil novecentos e setenta e quatro, achado por camponeses cavando um poço.",
  "farmers_well|Chinese farmers in 1974 digging a well in a dry field, one holding up a broken clay head, shocked",
  "terracotta_rows",
  "terracotta_faces|A line of cartoon terracotta warrior statues with round heads, each one with a different simple face and hairstyle, comic", card="1974")
b("Mas o império não sobreviveu ao dono. Um ano depois, a China estava em revolta. O Céu… tinha mudado de ideia.",
  "palace_fall",
  "storm_qin|Dark storm clouds over the Qin palace, rebels gathering on the hills with torches")

# ───────────────────────── 4. O CAMPONÊS E A SEDA ─────────────────────────
cap("4. A máquina sem o tirano")
b("Quem pegou o trono foi um homem de origem humilde, Liu Bang. Ele manteve a máquina de Qin… mas tirou o chicote.",
  f"liu_bang|{LIU}, standing at the head of a rebel army of peasants@@LIU BANG",
  f"liu_crowned|{LIU.replace('a simple straw hat and a patched brown tunic', 'a new black board crown and a red robe')}, on a throne looking surprised to be there, comic", card="202 a.C.")
b("Foi a dinastia Han, que durou quatro séculos. Até hoje, a maioria dos chineses se chama de povo Han.",
  "han_court|A Han dynasty court with officials in black robes and tall hats, an emperor on a raised platform@@DINASTIA HAN",
  "han_people_today|A modern crowd of Chinese people on a busy street today, families and students")
b("§ Os Han mandaram um enviado para o oeste, e, dali, nasceram as rotas que a gente chama de Rota da Seda.",
  "zhang_qian|An ancient Chinese envoy on a horse with a long staff and a few companions crossing a snowy mountain pass@@ZHANG QIAN",
  "map_silk|Map of Asia and Europe with a long golden caravan route from China across Central Asia and Persia to the Mediterranean, " + MAPA)
b("Roma enlouqueceu pela seda. E, por séculos, ninguém lá fora sabia como ela era feita: de um bichinho.",
  "rome_silk|Rich Roman ladies in a villa admiring a shining silk dress, a senator frowning at the price",
  "silkworm|Close view of white silkworms eating mulberry leaves and spinning cocoons, cute and detailed")
b("Os Han também transformaram o papel em algo para escrever. E, no ano dois, contaram cinquenta e sete milhões de pessoas.",
  "paper_make|Ancient Chinese workers making paper: pulp in a tub, a screen lifted, sheets drying on a wall",
  "crowd_han|A busy Han dynasty market crowd with stalls, carts and many people@@57 MILHÕES", card="2 d.C.")
b("§ Mas a corte foi apodrecendo por dentro. Os camponeses passavam fome, e, em cento e oitenta e quatro, uma revolta enorme levantou um grito.",
  "court_rot|Han court officials and eunuchs whispering and taking bribes behind a weak young emperor",
  "yellow_turbans|A huge peasant rebel army wearing yellow headscarves marching with spears and banners with no writing@@TURBANTES AMARELOS", card="184")
b("[slightly dramatic] O Céu azul está morto. Agora é a vez do Céu amarelo. Era o Mandato do Céu… usado contra o imperador.",
  "blue_yellow_sky|A sky split in two: a dark dead blue half and a rising bright yellow half over a crowd of rebels, symbolic",
  "han_emperor_scared|A scared young Han emperor peeking out from behind a curtain while yellow-scarfed rebels shout outside")
b("Em duzentos e vinte, os Han caíram, e a China se partiu em pedaços por quase quatro séculos.",
  "china_pieces|Three rival Chinese kingdoms' armies with different colored flags facing each other across a river",
  "map_broken|Map of China broken into several separate colored pieces with cracks between them, " + MAPA)

# ───────────────────────── 5. QUEBRAR E COLAR DE NOVO ─────────────────────────
cap("5. O segredo da China")
b("E aqui está o segredo da China. Quando Roma se partiu no ocidente, ninguém juntou os pedaços de novo. Quando a China se partia… alguém sempre juntava.",
  "rome_broken|Ruins of a Roman forum overgrown with grass, broken columns, a shepherd with goats",
  "china_glue|An ancient Chinese craftsman gluing a broken porcelain vase with gold, smiling")
b("Porque a máquina sobrevivia às famílias: uma escrita que todos liam, a ideia de um só centro… e uma prova.",
  "dialects|Ancient Chinese people from different regions talking and not understanding each other, then all reading the same scroll and nodding" + SEMTXT,
  "one_center|A tall imperial palace in the center of a round plain with roads coming from every direction",
  "thread_glow")
b("§ Em quinhentos e oitenta e nove, a dinastia Sui reuniu tudo, cavou o Grande Canal e começou a escolher funcionários por exame escrito.",
  "sui_canal|Thousands of workers digging a huge canal across a flat plain, boats waiting@@GRANDE CANAL",
  "exam_cells|Rows of tiny exam cells with nervous candidates writing with brushes, an examiner walking past" + SEMTXT, card="589")
b("§ Depois veio a dinastia Tang, e a capital, Chang'an, virou talvez a maior cidade do mundo.",
  "changan|The Tang dynasty capital Chang'an: a huge grid city with wide avenues, pagodas and walls, seen from above@@CHANG'AN",
  "tang_market|A busy Tang market with Persian merchants, Indian monks, Arab traders, camels and lanterns", card="618")
b("E, nessa corte, uma concubina chamada Wu Zetian foi subindo, até mandar no império por trás do marido. Então fez o impensável.",
  f"wu_young|{WU.replace('a tall golden phoenix headdress', 'a simple flower hairpin')}, a young concubine in the palace, smart and watchful@@WU ZETIAN",
  f"wu_behind|{WU}, sitting behind a silk screen behind a weak emperor, whispering orders")
b("[amazed] Em seiscentos e noventa, ela mesma sentou no trono como imperador. Foi a única mulher a fazer isso na história da China.",
  "wu_throne",
  "ministers_faint|Tang ministers fainting and dropping their tablets in surprise in a palace hall, comic",
  f"wu_proud|{WU}, standing on the palace balcony looking over the capital, proud", card="690")
b("E o Mandato do Céu? Ele nunca disse que precisava ser homem.",
  "heaven_wink|A big friendly cloud in the sky with a small smile shining golden light on an empress, comic")
b("§ Mas, em setecentos e cinquenta e cinco, o general An Lushan se revoltou, e a dinastia Tang nunca mais foi a mesma.",
  "an_lushan|A huge rebel general on a big horse leading an army through a burning city gate@@AN LUSHAN",
  "tang_ruin|A ruined Tang city with burned houses and refugees walking south", card="755")

# ───────────────────────── 6. INVENTARAM O FUTURO ─────────────────────────
cap("6. A China que inventou o futuro")
b("Do caos saiu a dinastia Song, talvez a China mais inventiva de todas. As moedas de ferro eram tão pesadas que os mercadores trocavam recibos de papel.",
  "song_city|A bustling Song dynasty riverside city with a big arched bridge, boats, shops and crowds",
  "iron_coins|A Chinese merchant struggling to carry a huge heavy string of iron coins on his back, comic", card="960")
b("Em mil e vinte e quatro, o governo assumiu os recibos: era o primeiro papel-moeda oficial do mundo. Guarde esse papel.",
  "paper_money|An official Song dynasty paper banknote with simple printed patterns and red seals, held up to the light" + SEMTXT,
  "money_press|Song government workers printing paper money with wooden blocks in a workshop" + SEMTXT, card="1024")
b("§ Os Song deixaram ainda a fórmula mais antiga da pólvora, a bússola nos navios e os tipos móveis.",
  "gunpowder|Song alchemists mixing powder in a bowl, a small explosion of smoke and sparks blowing their hats off, comic",
  "compass|A Song sailor on a ship deck holding a simple compass, a magnetic needle floating in a bowl of water")
b("Mas era ruim de espada. E, no norte, os cavaleiros estavam olhando.",
  "song_soldiers|Song dynasty soldiers looking nervous and unready on a city wall, one dropping his spear",
  "steppe_watch|Mongol horsemen with fur hats on a grassy hill at sunset looking toward a Chinese city")
b("§ Os mongóis de Gengis Khan começaram a guerra, e o neto dele, Kublai Khan, terminou: em mil duzentos e setenta e nove, a China inteira era mongol.",
  "genghis|Genghis Khan as a round-white-head cartoon Mongol khan with a simple flat beard shape and a fur hat, on a horse with his army@@GENGIS KHAN",
  "kublai|Kublai Khan as a round-white-head cartoon emperor with a simple flat beard shape, a Mongol fur-trimmed hat and a golden robe on a Chinese-style throne@@KUBLAI KHAN", card="1279")
b("Kublai mudou a capital para a cidade que hoje chamamos de Pequim e deu ao governo um nome chinês. O conquistador também queria o Mandato do Céu.",
  "khanbaliq|A great walled Mongol capital city with palaces and a big square plain around it, yurts outside the walls@@PEQUIM",
  "mongol_mandate|A Mongol khan raising his arms toward a golden sky, trying to catch the heavenly light, comic")
b("Só que os mongóis imprimiram papel-moeda demais, e ele virou pó. E, em mil trezentos e quarenta e quatro, o rio Amarelo transbordou de novo.",
  "inflation|A Mongol-era Chinese market street where people push wheelbarrows piled with paper money to buy one small bread, comic, plain stalls without any signs or banners" + SEMTXT,
  "river_flood#aberto", card="1344")
b("Os camponeses foram obrigados a refazer os diques, com fome. Enchente, fome, revolta… o Céu estava falando de novo.",
  "dyke_labor|Starving Chinese peasants forced to carry earth to rebuild river dykes under Mongol guards with whips",
  "red_turbans|A peasant rebel army with red headscarves rising up with farm tools and torches@@TURBANTES VERMELHOS")

# ───────────────────────── 7. A FROTA QUE VOLTOU ─────────────────────────
cap("7. A frota que voltou para casa")
b("Dessa revolta saiu um órfão que tinha sido monge mendigo, Zhu Yuanzhang. Em mil trezentos e sessenta e oito, ele expulsou os mongóis e fundou a dinastia Ming.",
  f"zhu_beggar|{ZHU}, walking alone on a muddy road in the rain, hungry@@ZHU YUANZHANG",
  f"zhu_emperor|{ZHU_EMP}, on the dragon throne, the Mongols fleeing north in the background@@DINASTIA MING", card="1368")
b("De mendigo a Filho do Céu. Na China, isso era possível… desde que você vencesse.",
  "beggar_to_king|A wooden beggar's bowl and a Chinese imperial crown (a flat black board with hanging bead strings) side by side on a red cushion in a Chinese palace, symbolic, no people")
b("§ E os Ming pensaram grande. A partir de mil quatrocentos e cinco, o almirante Zheng He levou frotas enormes até a costa da África.",
  f"zheng_he|{ZHENG}, standing on the deck of a giant treasure ship, pointing at the horizon@@ZHENG HE",
  "fleet_giant",
  "map_zhenghe|Map of the Indian Ocean from China to East Africa with a long red dotted sea route along the coasts of Southeast Asia, India and Arabia, " + MAPA, card="1405")
b("Uns noventa anos antes de Cabral chegar ao Brasil. Voltaram até com uma girafa, que a corte achou que era um animal sagrado.",
  "cabral_small|A small Portuguese caravel next to a gigantic Chinese treasure ship, the Portuguese sailors looking up amazed, comic size comparison",
  "crew_huge|Thousands of Chinese sailors on the deck of a huge treasure ship, cooking, fishing, working the sails")
b("§ Então… as viagens pararam. A China, no auge, deu as costas para o oceano.",
  "fleet_home",
  "court_closing|Ming court officials closing a big wooden door facing the sea, the ocean behind it, symbolic")
b("Em vez de navios, muralhas: quase toda a Grande Muralha que se visita hoje é Ming. E não, ela não se vê do espaço a olho nu.",
  "ming_wall|Ming soldiers and workers building a stone and brick Great Wall with watchtowers along a steep mountain ridge",
  "tourists_wall|Tourists walking on the Great Wall today taking selfies, mountains around",
  "great_wall_wide")
b("§ Mas muralha não para o clima. No século dezessete, uma pequena era do gelo trouxe frio e seca, e a fome encheu os exércitos rebeldes.",
  "snow_fields|Frozen Chinese fields with dead crops, peasants in rags in the cold",
  "signs_drought",
  "rebels_ming|A peasant rebel army marching toward Beijing under a grey sky", card="1627")
b("Em mil seiscentos e quarenta e quatro, os rebeldes tomaram Pequim, e o último imperador Ming se enforcou numa colina atrás do palácio.",
  "beijing_fall|Rebels pouring through a gate of Beijing, smoke over the Forbidden City",
  "coal_hill|A lonely tree on a small hill behind the Forbidden City at dawn, a crown left on the ground, sad and quiet", card="1644")
b("Seca, fome e revolta, tudo de uma vez. E, do norte, já vinha outro povo atrás do Mandato.",
  "manchu_riders|Manchu horsemen with fur-trimmed hats and banners riding through a mountain pass toward Beijing")

# ───────────────────────── 8. O SÉCULO DA HUMILHAÇÃO ─────────────────────────
cap("8. O século da humilhação")
b("Eram os manchus, que fundaram a última dinastia, a Qing. Todo homem teve de raspar a testa e usar trança… ou perder a cabeça.",
  "qing_emperor|A round-white-head cartoon Manchu emperor with a simple flat thin mustache shape, a round red-tasseled hat and a yellow dragon robe@@DINASTIA QING",
  "queue_barber|A street barber shaving the front of a nervous man's head and leaving a long braid at the back, a Manchu soldier watching, comic", card="1644")
b("§ Por um tempo, a China Qing foi enorme e rica. O mundo queria chá, seda e porcelana, e pagava em prata.",
  "map_qing|Map of the large Qing empire including Tibet, Xinjiang and Mongolia painted in yellow, neighbors pale, " + MAPA,
  "tea_trade|European merchants buying tea chests and porcelain at a Chinese port, paying with silver coins")
b("A Grã-Bretanha cansou de perder prata e achou algo que os chineses comprariam: ópio.",
  "opium_ship|A British merchant ship unloading wooden chests of opium at night onto small Chinese boats, sneaky",
  "opium_den|A dark opium den with sleepy men lying on mats with long pipes, smoke in the air")
b("§ Em mil oitocentos e trinta e nove, a China destruiu mais de mil toneladas de ópio, e a Grã-Bretanha respondeu com canhoneiras.",
  f"lin_zexu|{LIN}, standing firm at a beach watching workers dump opium into trenches with salt and lime@@LIN ZEXU",
  "gunboats|British steam gunboats firing cannons at Chinese wooden junks near a coastal fort", card="1839")
b("A China perdeu e entregou Hong Kong. Os chineses chamam os cem anos seguintes de século da humilhação.",
  "treaty_sign|Qing officials signing a treaty on a British warship with British officers around, humiliated" + SEMTXT,
  "map_hongkong|Map of the southern Chinese coast with one small island near a river mouth highlighted in red, " + MAPA, card="1842")
b("§ Então veio o pior, de dentro. Um homem reprovado nos exames imperiais teve visões e acordou certo de que era o irmão mais novo de Jesus.",
  "exam_fail|A young Chinese scholar in a blue robe crying on the steps of an exam hall while other candidates celebrate in the background, comic and sad, no boards, no signs" + SEMTXT,
  f"hong_vision|{HONG}, in a fever dream seeing a glowing bearded figure in the clouds giving him a sword@@HONG XIUQUAN")
b("Chamou o movimento de Reino Celestial da Grande Paz. Celestial: o Céu, de novo. A guerra durou catorze anos e matou de vinte a trinta milhões de pessoas.",
  "taiping_army|A huge Taiping rebel army with long hair, red and yellow headscarves and banners with no writing, marching", card="1851")
b("§ Em mil novecentos e onze, o Céu mudou de ideia pela última vez: veio a revolução. E o imperador era um menino, Puyi, que tinha subido ao trono com dois anos.",
  "revolution_1911|Revolutionary soldiers in 1911 cutting off their long braids with scissors and raising rifles in the streets of a Chinese city, no flags",
  f"puyi_boy|{PUYI}, crying while officials bow@@PUYI", card="1911")
b("Em fevereiro de mil novecentos e doze, aos seis anos, ele abdicou. Dois mil anos de imperadores acabaram com uma criança. Guarde esse nome.",
  "puyi_six|A small six-year-old cartoon boy emperor in a yellow robe playing with a toy while adults read a document over him" + SEMTXT,
  "empty_dragon|An empty imperial dragon throne in a huge red hall with dust floating in a ray of light", card="1912")

# ───────────────────────── 9. O CÉU VERMELHO ─────────────────────────
cap("9. Sem imperador, sem paz")
b("Sem imperador, a república se desfez em senhores da guerra. E, em mil novecentos e trinta e sete, o Japão invadiu.",
  "warlords|Several Chinese warlords in 1920s uniforms with big hats arguing over a map on a table" + SEMTXT,
  "japan_invade|1930s Japanese army tanks and soldiers advancing through a Chinese town, smoke", card="1937")
b("Em Nanquim, as tropas japonesas fizeram um massacre que a China calcula em trezentos mil mortos.",
  "memorial|A quiet memorial wall with flowers and candles, people bowing their heads" + SEMTXT,
  "two_flags|Two old men from China and Japan sitting back to back on a bench, not talking, cherry blossoms and pine trees")
b("§ Depois da guerra contra o Japão, nacionalistas e comunistas lutaram entre si.",
  "nationalists|1940s Chinese nationalist soldiers in grey-blue uniforms and helmets marching",
  "communists|1940s Chinese communist guerrillas in padded jackets and caps walking through mountains")
b("E, em mil novecentos e quarenta e nove, os comunistas de Mao venceram, e os nacionalistas fugiram para Taiwan.",
  f"mao_1949|{LIDER49}, speaking on the Tiananmen gate tower balcony to a huge crowd with red flags with no writing@@MAO TSÉ-TUNG, 1949",
  "map_taiwan|Map of the southeastern Chinese coast and the island of Taiwan across a strait, the island highlighted, " + MAPA, card="1949")
b("Mao quis fazer do país uma potência industrial em poucos anos: o Grande Salto Adiante, com fornos de aço no quintal das casas.",
  "backyard_furnace|Chinese villagers in 1958 melting pots and pans in a small backyard furnace, smoke everywhere",
  "fields_empty|Abandoned rice fields with unharvested crops while villagers work at furnaces in the distance", card="1958")
b("[serious] Veio a pior fome da história. As estimativas vão de quinze a cinquenta e cinco milhões de mortos.",
  "famine|A very poor Chinese village in a dry landscape, thin people with empty bowls, sad and quiet",
  "grain_seized|Officials carrying sacks of grain away from a starving village, villagers watching")
b("§ E, em mil novecentos e cinquenta e nove, um prisioneiro foi perdoado e mandado trabalhar no Jardim Botânico de Pequim.",
  "prisoner_free|A thin old round-white-head cartoon prisoner with round glasses walking out of a prison gate holding a small bag",
  "botanical|A botanical garden greenhouse in Beijing with plants and flowers, gardeners at work", card="1959")
b("Era Puyi. O último Filho do Céu agora era jardineiro.",
  "puyi_garden",
  f"puyi_old|{PUYI_OLD}, smiling at a flower, a faint ghost of a little boy emperor behind him@@PUYI, JARDINEIRO")
b("Depois vieram dez anos de Revolução Cultural, com escolas fechadas e alunos denunciando professores.",
  "cultural_rev|Teenagers in green uniforms with red armbands shouting at a frightened old teacher wearing a tall paper hat",
  "school_closed|A closed school with a chained gate and an empty schoolyard, leaves blowing", card="1966")
b("§ Em mil novecentos e setenta e seis, um terremoto arrasou Tangshan e matou, pelos números oficiais, duzentas e quarenta e duas mil pessoas.",
  "tangshan|A city flattened by a huge earthquake at night, collapsed buildings and rescuers with lanterns@@TANGSHAN",
  "rescuers|Chinese soldiers and citizens digging through rubble to save people at dawn", card="1976")
b("Muita gente lembrou da ideia antiga: grandes desastres avisam que o Céu está mudando de ideia. Seis semanas depois… Mao morreu.",
  "heaven_takes",
  "mao_funeral|A huge crowd in Tiananmen square in mourning with white flowers and black armbands")

# ───────────────────────── 10. A FÁBRICA DO MUNDO ─────────────────────────
cap("10. A fábrica do mundo")
b("Quem assumiu foi Deng Xiaoping, o da frase famosa: não importa a cor do gato, desde que ele cace o rato.",
  f"deng|{DENG}, smiling and playing cards with a cat at his feet@@DENG XIAOPING",
  "cat_mouse|A black cat and a white cat both chasing a mouse across a factory floor, comic", card="1978")
b("Em mil novecentos e oitenta, uma cidade pequena ao lado de Hong Kong virou a primeira zona econômica especial: Shenzhen.",
  "shenzhen_1980|A small Chinese town with low houses, rice fields and a river in 1980, a few construction cranes appearing@@SHENZHEN, 1980",
  "shenzhen_today|The huge modern skyline of Shenzhen today with tall glass towers at night", card="1980")
b("§ Hoje, Shenzhen tem quase dezoito milhões de pessoas, e a China foi de uns cinco para uns trinta por cento da indústria do mundo.",
  "factory|A giant modern factory with rows of workers and robots assembling electronics",
  "containers|A huge Chinese container port with cranes and colorful containers, ships")
b("Segundo o Banco Mundial, quase oitocentos milhões de chineses saíram da pobreza extrema em quarenta anos.",
  "village_then_now|Split image: a poor Chinese village with mud houses on the left and the same place with modern apartment buildings on the right",
  "family_today|A happy Chinese family having dinner in a modern apartment")
b("§ A política não abriu do mesmo jeito. Em mil novecentos e oitenta e nove, o exército tirou os manifestantes da Praça da Paz Celestial, e o número de mortos é disputado até hoje.",
  "tiananmen|A huge square in Beijing in 1989 full of student protesters with banners with no writing, tents",
  "tanks_square|Army tanks rolling on a wide avenue in Beijing at night, empty streets", card="1989")
b("Desde dois mil e doze, quem manda é Xi Jinping, que tirou o limite de mandatos.",
  "leader_today|A round-white-head cartoon leader with black hair and a dark suit standing at a podium in a vast modern Chinese assembly hall with a red curtain, rows of delegates, a big red star on the ceiling, no gothic windows@@XI JINPING")
b("§ Hoje, a China fabrica a maior parte dos carros elétricos do planeta e trouxe amostras do lado oculto da Lua. Mas, em dois mil e vinte e cinco, nasceram só sete milhões e novecentos mil bebês, e o país encolheu pelo quarto ano seguido.",
  "ev_factory|Rows of new electric cars coming off a production line in a modern Chinese factory",
  "moon_far|An unmanned robotic Chinese lunar lander with solar panels and a robotic arm scooping grey soil on the far side of the Moon, black starry sky with no Earth and no moon visible, no people, no astronauts",
  "few_babies|A big empty maternity ward with only one baby in a crib, a nurse looking around, comic and sad",
  "elderly_park|Many elderly Chinese people doing tai chi in a park in the morning, very few young people", card="2025")

# ───────────────────────── FECHO (paga o túmulo e o Mandato do Céu) ─────────────────────────
cap("Fecho")
b("§ [warm] E aquele túmulo? Continua fechado. Os arqueólogos preferem esperar: ninguém sabe preservar o que tem lá dentro… e tem o mercúrio.",
  "tomb_mound",
  "archaeologists_wait|Modern Chinese archaeologists sitting on a bench in front of a large green burial hill, drinking tea, patiently waiting",
  "tomb_door")
b("Qin Shi Huang queria viver para sempre, e não conseguiu. Prometeu dez mil gerações no trono, e teve quinze anos.",
  "qin_forever",
  "ten_thousand")
b("Mas uma coisa dele sobreviveu: a ideia de uma China só, com uma escrita e um centro. As famílias passaram. A ideia ficou.",
  "thread_glow",
  "kid_reading",
  "great_wall_wide")
b("§ Hoje, ninguém fala em Mandato do Céu. Mas a pergunta continua a mesma de três mil anos atrás: o que acontece quando o Céu muda de ideia?",
  "beijing_today|Modern Beijing today: the old Temple of Heaven with its round blue roof in front of modern towers, a sunny day@@TEMPLO DO CÉU",
  "heaven_gives")
b("E você? Se fosse você, abria o túmulo do Primeiro Imperador ou deixava fechado? Conta aqui nos comentários.",
  f"guide_comment|{GUIA} standing in front of a grassy Chinese burial hill with pine trees and a closed stone gate at its foot, holding a lantern and scratching its head, thinking, terracotta warriors peeking from the side",
  "terracotta_face")


# Grafia para a VOZ (o Fish lê como português): nomes chineses reescritos para soar perto do mandarim, como se diz no Brasil.
# blocos.json leva "texto" (falado, vai ao Fish) e "tela" (grafia correta: legendas e SCRIPT). Teste de pronúncia em qa/pronuncia/.
FALA = [("Qin Shi Huang", "Tchin Chi Ruang"), ("Qin", "Tchin"), ("Qing", "Tching"), ("Zhou", "Djou"), ("Shang", "Xang"),
        ("Zhongguo", "Djong-guô"), ("Ying Zheng", "Ing Djêng"), ("Sima Qian", "Sima Tchién"), ("Zhu Yuanzhang", "Dju Iuan-djang"),
        ("Zheng He", "Djêng Rrâ"), ("Wu Zetian", "Wu Dzê-tiên"), ("Chang'an", "Tchang-an"), ("Sui", "Suêi"), ("Puyi", "Pu-í"),
        ("Tangshan", "Tang-xan"), ("Shenzhen", "Xen-djen"), ("Deng Xiaoping", "Dâng Chiau-ping"), ("Xi Jinping", "Chi Djin-ping"),
        ("Liu Bang", "Liu Bang"), ("Han", "Rran"), ("Yu", "Iú"), ("Lushan", "Lu-xan")]
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
