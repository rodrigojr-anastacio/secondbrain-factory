#!/usr/bin/env python3
"""Fonte única do 007-russia (09/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

2º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
Molde History in Minutes (narrativa contínua). Referência de código: videos/006-roma e 005-brasil.
  hook: 862, a Crônica dos Tempos Passados: as tribos chamam os varegues: "nossa terra é grande e rica, mas não há ordem nela. Venham reinar sobre nós."
  → PERGUNTA CENTRAL (≤ 0:50) → "Essa é a história inteira da Rússia" → 1 "guarde" (a frase de 862) → o rio (problema da era 1)
  → 10 eras, cada uma: problema herdado → cena no presente → ≤ 3 fatos → solução → novo problema
  → fecho ≤ 45 s: responde, reenquadra e pergunta para os comentários.
Fio condutor: A FRASE DE 862 ("grande e rica, mas sem ordem"). Volta em 1054 (irmãos brigando), 1610 (Tempo das Dificuldades:
  de novo sem ordem, e de novo a Rússia chama alguém, Miguel Romanov) e 1991 (cabia de novo). A resposta montada em 3 peças:
  planície sem muralha → defender = avançar (peça 1, era 4); terra demais e gente de menos → prender o camponês (peça 2, era 6);
  invasor nunca derrubou a Rússia, a ordem sempre rachou por dentro (peça 3, era 10).
Pergunta volta: era 4 (1ª peça), era 6 (2ª peça), era 9 ("lembra da nossa pergunta?"), era 10 (3ª peça), fecho (resposta).
Neutralidade (brief): termina em 1991 + 1 frase neutra; nada de guerra atual nem juízo sobre governos recentes; Kiev só como o berço comum
  da Rus de Kiev (russos, ucranianos e bielorrussos).

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="862") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006).
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (006: 128 ppm com pausas)
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
TITULO = "A história INTEIRA da Rússia"
PERGUNTA = "Como uma terra que precisou chamar estrangeiros para pôr ordem nela virou o maior país do mundo, e por que essa ordem sempre custou tão caro?"

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
SEMMES = ", no minarets, no mosques"   # 006: "domes" puxa mesquita otomana
# Personagens (regra da bíblia: nada de rosto descrito; "round-white-head cartoon …")
ESL = "round-white-head cartoon early medieval Slavic villagers in white linen tunics with red embroidery, simple fur hats and bark shoes"
VAR = "round-white-head cartoon Viking Varangian warriors with simple flat blond beard shapes, conical iron helmets and plain round wooden shields"
RURIK = "a round-white-head cartoon Viking prince with a simple flat red beard shape, a conical iron helmet and a red cloak"
VLAD = "a round-white-head cartoon medieval prince with a simple flat brown beard shape, a round fur-trimmed red cap and a long red embroidered robe"
IARO = "an old round-white-head cartoon medieval prince with a simple flat grey beard shape, a fur-trimmed cap and a blue embroidered robe"
MONG = "round-white-head cartoon Mongol horse archers in fur-trimmed pointed hats and leather lamellar armor on small steppe horses"
KHAN = "a round-white-head cartoon Mongol khan with a simple thin flat mustache shape, a fur-trimmed pointed golden hat and a silk robe"
KALITA = "a round-white-head cartoon medieval Russian prince with a simple flat brown beard shape, a fur-trimmed cap and a long robe, holding a big fat leather money pouch"
IVAN3 = "a round-white-head cartoon medieval Russian grand prince with a simple flat long dark beard shape, a fur-trimmed golden cap and a heavy brocade robe"
IVAN4 = ("a round-white-head cartoon Russian tsar with a simple flat long pointed black beard shape, a golden fur-trimmed cap with a small cross on top, "
         "a dark brocade robe and a tall wooden staff, suspicious frowning eyes")
CAMP = "round-white-head cartoon Russian peasants in simple linen shirts with rope belts and bark shoes, women with headscarves"
COSS = "round-white-head cartoon Cossacks with simple flat long mustache shapes, tall fur hats, red long coats and old muskets"
BOYAR = "round-white-head cartoon Russian nobles with simple flat long beard shapes, very tall fur hats and long heavy brocade coats"
PEDRO = "a very tall round-white-head cartoon young tsar with short dark curly hair, a simple flat small black mustache shape and a green European military coat"
CATA = "a round-white-head cartoon empress with powdered grey hair, a small diamond crown, a blue sash over a white silk gown"
NAPO = "a round-white-head cartoon French emperor with a black bicorne hat and a grey overcoat"
FRAN = "round-white-head cartoon French soldiers in blue coats, white cross belts and tall black shakos"
RUS1812 = "round-white-head cartoon Russian soldiers of 1812 in dark green coats and black shakos"
ALEX2 = "a round-white-head cartoon Russian tsar with a simple flat big brown mustache and sideburns shape, a white military tunic with gold epaulettes"
NIC2 = "a round-white-head cartoon Russian tsar with a simple flat neat short brown beard and mustache shape, a plain khaki military tunic"
OPER = "round-white-head cartoon Russian factory workers of 1905 in dark caps and long coats, women with headscarves"
REV = "a round-white-head cartoon revolutionary leader, bald, with a simple flat small pointed reddish beard shape, a dark suit and a flat worker cap"
STAL = "a round-white-head cartoon Soviet leader with a simple flat thick black mustache shape, combed-back black hair and a plain grey military tunic"
SOV = "round-white-head cartoon Soviet soldiers of the 1940s in khaki uniforms and helmets"
GORB = "a round-white-head cartoon Soviet politician, bald, with a small reddish birthmark shape on the top of the head and a grey suit"
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes"
INV = "snowy winter, white snow on the ground"

# ───────────────────────── HOOK (862: "nossa terra é grande e rica, mas não há ordem nela") ─────────────────────────
cap("Hook")
b("[serious] Oitocentos e sessenta e dois. Florestas sem fim, rios gelados e tribos que não param de brigar.",
  f"forest_tribes|Endless dark pine forests and a wide cold river in the north of Eastern Europe in the 9th century, small wooden villages with smoke, misty dawn",
  f"tribes_fight|Two groups of {ESL} shouting and shaking sticks and axes at each other across a small stream in a forest, comic but tense",
  f"village_burn|A small wooden palisade village in a clearing of a pine forest with one hut burning, villagers running with buckets",
  card="862")
b("Imagine que você mora ali. Clã contra clã, e ninguém manda em ninguém. Então os chefes mandam um recado para o outro lado do mar, para guerreiros escandinavos, os varegues:",
  f"elders_argue|Old village elders, {ESL}, sitting around a fire in a log hall all talking at the same time and pointing at each other, chaos, comic",
  f"envoys_boat|Three Slavic envoys in fur hats rowing a small wooden boat across a grey northern sea toward misty land",
  f"varangians_hall|{VAR} sitting in a long wooden Viking hall with a fire in the middle, drinking from horns, surprised by visitors at the door",
  f"envoys_bow|Slavic envoys in fur hats bowing in front of {RURIK} sitting on a carved wooden chair in a Viking hall" + SEMBAND,
  f"map_sea_route|Map of the Baltic Sea with Scandinavia on the left and the forests of Eastern Europe on the right, a dotted line of a boat route crossing the sea, " + MAPA)
b("[slightly dramatic] Nossa terra é grande e rica, mas não há ordem nela. Venham reinar sobre nós.",
  "rich_land|A huge rich land seen from a hill: golden fields, endless forests, rivers full of fish, beehives and furs piled in a village, sunny",
  f"rurik_arrives|{RURIK} stepping off a Viking longship onto a riverbank, Slavic villagers welcoming him with bread and salt" + SEMBAND + "@@RÚRIK",
  "longships_river|Several Viking longships with striped sails rowing up a wide forest river in Eastern Europe, golden light" + SEMBAND)
b("[curious] Um condomínio contratando síndico viking. Pelo menos, é o que contam monges uns duzentos e cinquenta anos depois, e os historiadores discutem até hoje quanto disso aconteceu.",
  f"viking_syndic|A comic modern analogy: {RURIK} with a clipboard standing in the hall of a modern apartment building while round-white-head cartoon residents argue" + SEMTXT,
  "monk_chronicle|A round-white-head cartoon medieval Orthodox monk with a simple flat long beard shape writing a chronicle by candlelight in a wooden monastery cell" + SEMTXT,
  "historians_debate|Three round-white-head cartoon modern historians with glasses arguing around a table covered with old books and a big map, comic" + SEMTXT,
  "chronicle_page|An open medieval book on a wooden desk showing only one big colorful drawing of Viking ships on a river, the rest of the pages completely blank, a candle" + SEMTXT,
  f"monk_yawn|A round-white-head cartoon young Orthodox monk falling asleep over a huge old book at night, the candle almost gone, comic" + SEMTXT)
b("§ [serious] Mas aquela frase vira uma pergunta que atravessa mil anos: como uma terra que precisou chamar estrangeiros para pôr ordem nela virou o maior país do mundo, e por que essa ordem sempre custou tão caro?",
  "map_russia_hook|Map of the northern half of Europe and Asia with the huge territory of Russia painted red from the Baltic Sea to the Pacific Ocean, the other lands pale, the seas blue, " + MAPA,
  "kremlin_snow|The red brick walls and towers of the Moscow Kremlin with golden onion domes behind them in the snow, crowds of round-white-head cartoon people, winter",
  f"tsar_throne|{IVAN4.replace('a round', 'A round')}, sitting on a golden throne, nobles bowing deeply in front of him",
  f"peasants_field|{CAMP} pulling a heavy wooden plow in a muddy field under a grey sky, tired, a nobleman on a horse watching",
  "red_square_parade|A giant parade of tanks and marching soldiers on a huge cobbled square in front of red brick walls and colorful onion domes, 1960s, round-white-head cartoon crowds" + SEMBAND,
  f"plain_invaders|Symbolic scene of a huge flat plain with tiny armies coming toward the center from every direction, no mountains to stop them, dramatic sky" + SEMBAND)
b("Essa é a história inteira da Rússia. Guarde aquela frase: grande e rica, mas sem ordem. Ela volta. E tudo começa pelo único caminho que havia ali. A água.",
  "plain_endless|A vast flat plain of forests, swamps and meadows stretching to the horizon with no mountains at all, a wide slow river winding through it, big sky",
  "phrase_kept|An old parchment scroll tied with a red string resting on a wooden table by a window looking at a snowy forest, a single beam of light, symbolic" + SEMTXT,
  "river_dawn|A wide slow river in a misty northern forest at dawn, reflections of pine trees on the calm water, a single wooden boat",
  f"birch_forest|A birch forest by a calm river with golden autumn leaves, peaceful, no people",
  f"viking_prow|Close view of the carved dragon head prow of a Viking longship gliding on a misty forest river")

# ───────────────────────── 1. O RIO ─────────────────────────
cap("1. A estrada era o rio")
b("Olhe para essa terra de cima: uma planície enorme, sem montanha, sem muralha natural. Só floresta, pântano… e rios largos e lentos, que ligam o mar Báltico ao mar Negro.",
  "map_rivers|Map of Eastern Europe from the Baltic Sea in the north to the Black Sea in the south, flat green plains and forests, long blue rivers running north to south, " + MAPA,
  "swamp_forest|A flat swampy birch forest with still dark water and reeds, mosquitoes, a heron, grey sky",
  "aerial_river|Aerial view of a huge flat green land with a wide winding river and many small lakes, no mountains anywhere",
  f"varangian_lookout|A round-white-head cartoon Viking lookout standing at the prow of a longship pointing ahead at a wide river between endless forests",
  f"flat_meadow|An endless flat meadow with wildflowers and a far forest line under a huge sky, a lonely wooden cart, no mountains",
  card="séc. IX")
b("Para os varegues, isso era uma rodovia. Eles descem de barco com peles, mel e gente escravizada para vender em Constantinopla. E, onde o rio fica raso, arrastam o barco por terra. [curious] Tente isso com o seu carro.",
  f"boats_furs|{VAR} in a longship loaded with furs, barrels of honey and blocks of wax rowing down a forest river" + SEMBAND,
  "portage|Round-white-head cartoon Viking traders dragging a wooden boat over land on log rollers between two rivers, sweating, comic",
  "constantinople_market|The rich market of Constantinople by the sea in the 10th century with Byzantine merchants in silk, Viking traders selling furs, classical columns and a big church with a low wide dome in the distance" + SEMMES,
  "silver_hoard|An archaeologist round-white-head cartoon digging up a clay pot full of shiny silver coins in a forest" + SEMTXT,
  f"honey_wax|Round-white-head cartoon Slavic villagers collecting wild honey from hollow trees in the forest, smoke, bees",
  f"car_portage|A comic modern analogy: a round-white-head cartoon family pushing their small car across a muddy field between two roads, sweating",
  f"byzantine_gold|Byzantine merchants in silk paying Viking traders with gold coins and silk cloth on a marble quay by the sea" + SEMMES)
b("§ Os sucessores de Rúrik descem o rio Dniepre e tomam Kiev, em oitocentos e oitenta e dois. Kiev, hoje capital da Ucrânia, vira o centro da Rus de Kiev, o berço comum de russos, ucranianos e bielorrussos.",
  "kiev_hill|The early medieval wooden city of Kiev on high green hills above the wide Dnieper river, wooden walls and towers, boats on the river, sunny",
  "map_kievan_rus|Map of Eastern Europe with a large area from the Baltic Sea to the edge of the southern steppe painted orange, a wide river running south, " + MAPA,
  f"oleg_kiev|{VAR} with a Viking leader landing boats at the riverside of a wooden hill town, the town gate opening" + SEMBAND,
  "three_brothers|Three round-white-head cartoon children in medieval Slavic embroidered clothes sitting together under a big old oak tree, warm light, symbolic",
  f"dnieper_boats|A fleet of Viking longships sailing down the wide Dnieper river past high green hills" + SEMBAND,
  f"kiev_gate|The wooden gate of medieval Kiev with guards, merchants entering with carts, sunny",
  card="882")
b("Só que essa terra pagã ficava entre vizinhos com um deus só e uma Igreja para pôr ordem nas coisas. O problema era escolher qual.",
  "pagan_idol|A tall carved wooden pagan idol on a hill above a river, Slavic villagers leaving offerings of bread and flowers, cloudy sky",
  "neighbors_faiths|Symbolic scene: four round-white-head cartoon envoys in very different clothes (a Muslim scholar with a turban, a Jewish merchant, a Latin priest, a Byzantine priest) waiting in line at a wooden palace door, comic" + SEMTXT,
  "map_neighbors|Map of Europe and the Near East with Eastern Europe painted pale orange in the middle, the Byzantine lands to the south painted purple and the lands of the Islamic world to the southeast painted green, " + MAPA,
  f"pagan_priest|A round-white-head cartoon pagan Slavic priest with a simple flat white beard shape and a staff making a fire offering under an old oak, villagers watching")

# ───────────────────────── 2. A FÉ ─────────────────────────
cap("2. Um príncipe escolhe um deus")
b("Kiev, novecentos e oitenta e oito. O príncipe Vladimir quer uma religião para o país. Então faz quase uma entrevista de emprego com muçulmanos, judeus e cristãos.",
  f"vladimir_throne|{VLAD}, sitting on a wooden throne in a hall of logs, listening with a bored face to visitors, guards around@@VLADIMIR",
  "job_interview|A comic scene: a medieval prince sitting behind a table like a job interviewer while envoys of different religions in very different clothes present themselves one by one" + SEMTXT,
  f"kiev_palace|A medieval wooden palace of a prince in Kiev with carved roofs, guards at the door, envoys arriving on horses",
  f"envoys_line|A long line of envoys in very different exotic clothes carrying gifts waiting in front of a wooden palace, comic",
  card="988")
b("O islã, ele recusa por um motivo bem prático. Segundo a crônica, Vladimir diz: [slightly dramatic] beber é a alegria da Rus, não podemos viver sem isso.",
  f"vladimir_drink|{VLAD}, raising a big golden cup of mead at a noisy feast, his warriors cheering with horns of drink, comic",
  "feast_hall|A loud medieval feast in a wooden hall with long tables, roasted meat, barrels and round-white-head cartoon warriors singing",
  f"envoy_shocked|A round-white-head cartoon Muslim scholar with a turban looking shocked as a medieval prince laughs and raises a huge cup, comic",
  f"mead_barrel|Round-white-head cartoon servants rolling huge barrels of mead into a medieval feast hall, comic")
b("§ Mas os enviados que voltam de Constantinopla contam que, dentro da igreja de Santa Sofia, não sabiam se estavam no céu ou na terra. Então Vladimir escolhe o cristianismo ortodoxo e manda batizar o povo de Kiev no rio.",
  "hagia_sophia_in|Inside a huge Byzantine Christian cathedral of the 10th century with one giant golden dome, golden mosaics of Christ, the Virgin Mary and angels on every wall, light pouring from the windows of the dome, round-white-head cartoon envoys in fur hats looking up amazed, only Christian mosaics, no round medallions, no green discs, no Arabic writing, no minarets",
  "baptism_dnieper|A mass baptism in the wide Dnieper river: crowds of round-white-head cartoon people of Kiev standing in the water while Orthodox priests bless them from the bank",
  "idol_river|Round-white-head cartoon people pulling a big wooden pagan idol into a river with ropes, comic",
  f"envoys_amazed|Close view of three round-white-head cartoon medieval envoys in fur hats with open mouths and wide eyes looking up in amazement, golden light falling on their faces, behind them only a golden mosaic of a Christian angel with wings, no round medallions, no green discs, no writing",
  f"byzantine_choir|Byzantine Orthodox priests in golden robes singing with candles and incense in a huge church full of light",
  f"dnieper_crosses|Orthodox priests holding crosses blessing the wide Dnieper river at sunrise while crowds wade in, wide view")
b("[curious] Repare numa foto da Rússia: as igrejas de cúpula, os ícones dourados e até o alfabeto cirílico vieram junto com essa escolha.",
  "icons_church|Inside a medieval Orthodox church full of golden icons and candles, a round-white-head cartoon priest with a simple flat long beard shape swinging incense",
  "cyrillic_scribe|A round-white-head cartoon monk carefully copying a book with colorful decorated pages, the pages showing only colorful ornaments and drawings" + SEMTXT,
  "sophia_kiev|A big medieval stone cathedral with many small rounded domes in the early city of Kiev, sunny, round-white-head cartoon people walking")
b("Kiev fica rica. Só que o poder era repartido entre irmãos, primos e sobrinhos, e eles brigavam mais entre si do que com qualquer inimigo. Repare: uma terra grande, rica… e de novo sem ordem. Bem na hora em que, do leste, vinha o pior inimigo possível.",
  "princes_brawl|A comic brawl of round-white-head cartoon medieval princes in fur caps pulling each other's beards and robes at a long table, a small crown rolling on the floor",
  "map_split_rus|Map of Eastern Europe with many small patches of different colors like a patchwork, rivers and forests, " + MAPA,
  "steppe_storm|A huge cloud of dust on the horizon of a flat grassy steppe under a dark stormy sky, the shapes of thousands of riders, ominous")

# ───────────────────────── 3. OS MONGÓIS E MOSCOU ─────────────────────────
cap("3. A cidade que cobrava para o cã")
b("Riazan, inverno de mil duzentos e trinta e sete. Repare nos rios: congelados, viram estrada para os trenós. Mas, naquele inverno, quem vem pelo gelo é o exército mongol de Batu, neto de Gengis Khan.",
  f"frozen_river_sleds|Horse sleds of {CAMP} traveling on a wide frozen river between snowy forests, {INV}",
  f"mongols_ice|A huge army of {MONG} riding fast on a frozen river through snowy forests, {INV}" + SEMBAND,
  "ryazan_walls|The wooden walls and towers of a medieval Russian town on a snowy hill, round-white-head cartoon defenders watching an army on the frozen river below",
  card="1237")
b("Riazan cai, depois Vladimir, depois dezenas de cidades. Em mil duzentos e quarenta, Kiev é arrasada. Numa planície, você não tem onde se esconder.",
  "town_burning_snow|A medieval wooden Russian town burning on a snowy hill at night, Mongol riders around it, no gore" + SEMBAND,
  "map_mongols|Map of Eurasia with the huge Mongol empire painted golden yellow from China to Eastern Europe, a big golden arrow pointing west into the forests of Eastern Europe, " + MAPA,
  "kiev_ruins|The ruins of a burned medieval stone cathedral and wooden walls on a hill above a river, smoke, crows, grey sky",
  card="1240")
b("§ Os mongóis da Horda Dourada não querem governar aldeia. Querem tributo. Então fazem o que todo império faz: terceirizam. O príncipe russo vai até o cã e volta com licença para governar e cobrar os vizinhos.",
  f"khan_tent|{KHAN}, sitting on cushions in a huge round felt tent decorated with gold, a Russian prince kneeling in front of him",
  "license_scroll|A Mongol official handing a small golden tablet on a cord to a kneeling Russian prince in a fur cap, symbolic" + SEMTXT,
  "tribute_wagons|A long caravan of wagons loaded with silver and furs going from Russian forests to a big camp of felt tents on the steppe")
b("E quem vira o melhor cobrador é uma cidadezinha de madeira sem importância. Moscou. O príncipe dela, Ivan, tinha o apelido de Kalita, a bolsa de dinheiro. [curious] Parte do tributo ia para o cã. Parte, ao que tudo indica, ficava em casa.",
  "moscow_wood|A small wooden fortress town with a log wall on a hill by a small river in a pine forest, 14th century, a few small churches, sunny",
  f"kalita|{KALITA}, smiling and patting the money pouch, coins falling out of it@@IVAN KALITA",
  "coins_split|Two piles of silver coins on a table being divided by a hand, one big pile going into a chest marked with a Mongol tent symbol and one small pile secretly slipping into a pouch, comic" + SEMTXT,
  card="1325")
b("Imagine o vizinho que cobra o condomínio de todo mundo e, aos poucos, vai comprando os apartamentos. Moscou ainda atrai o chefe da Igreja para morar lá. Agora tem dinheiro e fé.",
  "neighbor_buys|A comic modern analogy: a smiling round-white-head cartoon man with a money bag putting a SOLD sticker shape on apartment doors in a building hallway while neighbors stare" + SEMTXT,
  "metropolitan_moscow|An old round-white-head cartoon Orthodox church leader in a white hood and golden robes arriving in a small wooden Moscow, bells ringing")
b("O problema é que tudo isso ela devia a um senhor estrangeiro. E um dia ia ter que dizer não.",
  "moscow_prince_khan|A Russian prince in a fur cap looking with clenched fists at the shadow of a Mongol khan on a wall, dramatic")

# ───────────────────────── 4. TERCEIRA ROMA ─────────────────────────
cap("4. Dois exércitos e um rio")
b("Rio Ugra, mil quatrocentos e oitenta. Imagine você na margem: de um lado, o exército de Moscou; do outro, o da Grande Horda. Eles se encaram por semanas. Ninguém atravessa.",
  f"ugra_standoff|Two armies on opposite banks of a small river in autumn: Russian soldiers in red coats and pointed helmets on one side, {MONG} on the other, both just staring" + SEMBAND,
  "ugra_waiting|A bored round-white-head cartoon Russian soldier yawning on the riverbank, an equally bored Tatar rider yawning on the other bank, comic",
  card="1480")
b("[curious] E aí os tártaros dão meia-volta e vão embora. Mais de dois séculos de domínio acabam assim: com dois exércitos olhando um para o outro sobre a água.",
  f"tatars_leave|{MONG} turning their horses around and riding away from a river in the autumn rain, the Russian soldiers on the other bank confused")
b("§ Do lado de Moscou estava Ivan Terceiro, casado com a sobrinha do último imperador de Constantinopla, que os turcos tinham tomado em mil quatrocentos e cinquenta e três. Então Moscou adota a águia de duas cabeças e, anos depois, um monge escreve: [slightly dramatic] duas Romas caíram, Moscou é a terceira, e uma quarta não haverá.",
  f"ivan3_sophia|{IVAN3} and a round-white-head cartoon Byzantine princess with a pearl crown standing side by side in a golden hall@@IVAN III",
  "constantinople_fall|The great walls of Constantinople by the sea under cannon smoke in 1453, Ottoman soldiers with tall white hats attacking" + SEMBAND,
  "double_eagle|A golden double-headed eagle emblem carved on a stone wall of a Russian palace, sunlight, symbolic" + SEMTXT,
  "monk_three_romes|A round-white-head cartoon old monk with a simple flat long white beard shape pointing to three small domed cities drawn on parchment, two of them crossed out" + SEMTXT,
  card="1453")
b("§ E aqui está a primeira peça da resposta. Moscou continuava numa planície sem muralha, com inimigos a oeste, ao sul e ao leste. Então a defesa que parecia funcionar era avançar até o próximo rio, a próxima fortaleza.",
  "piece_one|A big golden puzzle piece being placed into a puzzle that shows a small map of a forest land, a round-white-head cartoon Russian prince holding it, symbolic" + SEMTXT,
  "map_moscow_threats|Map of Eastern Europe with a small red area in the middle and arrows coming toward it from the west, the south and the east, flat plains with no mountains, " + MAPA,
  "border_fort|Round-white-head cartoon Russian soldiers building a new wooden fort with a watchtower on the bank of a river at the edge of the steppe")
b("Só que, quando você empurra a fronteira, ganha um vizinho novo. E um motivo novo para continuar. Para isso, Moscou queria um governante com poder total.",
  "border_push|A comic symbolic scene in the 15th century: a round-white-head cartoon medieval Russian soldier in a red long coat and a pointed iron helmet pushing a wooden border fence forward across a green plain and meeting a new surprised neighbor in medieval clothes on the other side, no stars, no modern uniforms")

# ───────────────────────── 5. IVAN, O TERRÍVEL ─────────────────────────
cap("5. O primeiro czar")
b("Moscou, mil quinhentos e quarenta e sete. Um rapaz de dezesseis anos é coroado com um título novo: czar, que vem de César. Ele vai ficar conhecido como Ivan, o Terrível.",
  f"ivan4_coronation|A young round-white-head cartoon prince of sixteen with no beard being crowned with a golden fur-trimmed cap inside a golden Orthodox cathedral, priests and nobles around",
  f"ivan4_portrait|{IVAN4}, standing in a dark hall with painted walls, looking sideways with suspicion@@IVAN, O TERRÍVEL",
  "caesar_tsar|A comic symbolic scene: a Roman bust with a laurel wreath and a Russian tsar in a fur cap looking at each other like relatives" + SEMTXT,
  card="1547")
b("Ele toma Kazan dos tártaros e ergue a catedral de São Basílio, aquela das cúpulas coloridas que você já viu em cartão-postal. Mas depois desconfia de todo mundo e solta uma tropa vestida de preto, que mata nobres e saqueia cidades inteiras.",
  "kazan_siege|A Russian army besieging a walled Tatar city with towers on a river, cannons smoking, 1552" + SEMBAND,
  "saint_basil|Saint Basil's Cathedral in Moscow with its colorful striped and checkered onion domes under a blue sky, round-white-head cartoon people in 16th century clothes in front",
  "black_riders|Riders in long black cloaks on black horses galloping through a snowy village at night, a broom tied to each saddle, frightened villagers hiding, no gore",
  card="1552")
b("[serious] Num acesso de raiva, ele bate com o bastão na cabeça do próprio filho, o herdeiro, que morre dias depois.",
  "ivan_rage|A dark palace room with a tall wooden staff fallen on a carpet and a toppled chair, the shadow of a man holding his head in despair on the wall, dramatic, no blood",
  card="1581")
b("§ Enquanto isso, a leste dos montes Urais, os cossacos de Iermak entram na Sibéria atrás de peles. Pele de zibelina valia quase como dinheiro.",
  f"yermak|{COSS} led by a Cossack chief with a simple flat black beard shape in a breastplate, crossing low wooded mountains on foot with boats on their shoulders@@IERMAK",
  "furs_pile|A huge pile of dark sable, red fox and white ermine furs in a wooden trading house, a merchant counting them",
  "taiga|The endless Siberian taiga forest with a wide river, low mountains far behind, a small group of boats on the river, golden autumn",
  card="1582")
b("Em mil seiscentos e trinta e nove, eles chegam ao oceano Pacífico: o norte da Ásia inteiro em menos de sessenta anos. Na mesma época, o Brasil ainda era quase só o litoral.",
  f"pacific_coast|{COSS} standing on a rocky beach looking at the wide Pacific Ocean, cheering, a small wooden boat behind them",
  "map_siberia|Map of northern Asia from the Ural mountains to the Pacific Ocean with a red line of small forts along the rivers going east to the ocean, " + MAPA,
  "brazil_coast|A small Portuguese colonial town of the 1600s on the Brazilian coast with a white church and sugar mills, the dense green forest behind untouched, sunny" + SEMBAND,
  card="1639")
b("Só que Ivan tinha matado o herdeiro mais capaz. Quando o último filho dele morre, em mil quinhentos e noventa e oito, a família de Rúrik acaba. E o trono fica vazio.",
  "empty_throne_dust|An empty golden throne covered in dust and cobwebs in a dark Kremlin hall, a single candle, symbolic",
  card="1598")

# ───────────────────────── 6. FOME, ROMANOV E SERVIDÃO ─────────────────────────
cap("6. O vulcão e a corrente")
b("Peru, fevereiro de mil e seiscentos. O vulcão Huaynaputina explode, e as cinzas esfriam o hemisfério norte.",
  "volcano_peru|A huge volcano exploding in the Andes mountains of Peru, a giant column of ash rising into the sky, llamas running",
  card="1600")
b("Do outro lado do mundo, na Rússia, chove o verão inteiro e gela cedo. A colheita se perde três anos seguidos, e talvez dois milhões de pessoas morrem de fome.",
  f"rain_rye|{CAMP} looking at a field of green rye flattened by rain under a heavy grey sky, sad",
  "frost_field|A field of unripe rye covered with early white frost in summer, a lone peasant kneeling, dawn",
  "famine_village|A poor wooden Russian village in a cold grey autumn with empty barns and thin people waiting in line for bread, sad, no gore",
  card="1601")
b("§ Com fome e sem rei, vem o Tempo das Dificuldades: impostores dizendo ser o filho morto de Ivan, revoltas e, em mil seiscentos e dez, os poloneses no Kremlin. Uma terra grande, rica… e, de novo, sem ordem.",
  "impostor|A round-white-head cartoon young man in a fake golden cap pointing at himself proudly in front of a confused crowd, comic",
  "poles_kremlin|Polish hussar soldiers with feathered wings on their backs standing on the red brick walls of the Kremlin" + SEMBAND,
  card="1610")
b("Então um comerciante, Minin, e um príncipe, Pojarski, juntam uma milícia e expulsam os poloneses. Em mil seiscentos e treze, uma assembleia escolhe um czar de dezesseis anos: Miguel Romanov. [curious] Como em oitocentos e sessenta e dois, a Rússia chamou alguém para pôr ordem.",
  "minin_pozharsky|A round-white-head cartoon merchant with a simple flat beard shape and a prince in armor raising their arms to a crowd of volunteers with spears in a town square",
  "michael_romanov|A shy round-white-head cartoon teenage boy being crowned tsar in a golden cathedral, nobles and priests around him@@MIGUEL ROMANOV",
  card="1613")
b("§ E aqui está a segunda peça da resposta. Era terra demais para gente de menos. Se a vida apertava, o camponês fugia para a fronteira. Então, em mil seiscentos e quarenta e nove, uma lei prende o camponês ao dono da terra, ele e os filhos, para sempre.",
  "piece_two|A second golden puzzle piece placed next to the first, showing a huge empty land and a few tiny people, symbolic" + SEMTXT,
  f"peasant_flees|A round-white-head cartoon peasant family with a cart running away at night across a field toward a dark forest, the moon above",
  "serf_chain|A symbolic scene: a peasant in a linen shirt with a long iron chain going from his ankle to a big wooden manor house on a hill, sad",
  "law_book|A big heavy law book with a red seal on a wooden table in a Kremlin office, clerks with quills around it" + SEMTXT,
  card="1649")
b("Imagine não poder mudar de emprego nem de cidade, nem você, nem os seus netos. A ordem tinha um preço, e quem pagava era o camponês. Mas a Rússia tinha outro problema: estava ficando para trás.",
  "grandpa_kids|A round-white-head cartoon peasant grandfather with a white beard shape and his small grandchildren looking at the same muddy field through a fence, sad",
  "west_ships|A busy Dutch harbor in the 1600s full of big sailing ships and windmills, a small Russian cart passing by looking old, symbolic" + SEMBAND)

# ───────────────────────── 7. PEDRO, O GRANDE ─────────────────────────
cap("7. O czar que foi aprender carpintaria")
b("Holanda, mil seiscentos e noventa e sete. Num estaleiro, um carpinteiro novato chamado Pedro Mikhailov aprende a fazer navio. Ele tem mais de dois metros. [curious] Ninguém desconfia de nada. Ou todo mundo finge.",
  f"peter_shipyard|{PEDRO}, wearing a simple worker shirt, sawing a plank in a Dutch shipyard, much taller than all the other workers, comic",
  "dutch_workers|Round-white-head cartoon Dutch shipyard workers whispering and pointing at a giant new worker behind his back, comic",
  "dutch_yard|A 17th century Dutch shipyard with a big wooden ship being built, windmills and canals behind, sunny" + SEMBAND,
  card="1697")
b("É o czar Pedro, o Grande, viajando disfarçado pela Europa. E ele volta convencido de que a Rússia está séculos atrás.",
  f"peter_portrait|{PEDRO}, standing proudly with a sword in front of a window showing big sailing ships@@PEDRO, O GRANDE")
b("§ A prova vem em mil e setecentos: em Narva, um exército sueco bem menor esmaga o dele. Então Pedro derrete sinos de igreja para fazer canhões e, nove anos depois, em Poltava, derrota a Suécia.",
  "narva|A battle in a snowstorm where a small Swedish army in blue coats breaks a much bigger Russian army, 1700" + SEMBAND,
  "bells_cannons|Round-white-head cartoon workers melting big church bells in a foundry and pouring the bronze into cannon molds, sparks",
  "poltava|A big battle on a summer plain with Russian infantry in green coats advancing and Swedish soldiers retreating, cannon smoke" + SEMBAND,
  card="1700")
b("No meio disso, num pântano à beira do Báltico, ele ergue uma capital nova, de pedra e canais: São Petersburgo. Olhe o preço: milhares de trabalhadores forçados morrem na obra.",
  "swamp_workers|Hundreds of round-white-head cartoon forced workers digging canals and driving wooden piles into a foggy swamp, sad",
  "petersburg|The new city of Saint Petersburg in the 18th century with stone palaces along canals and a river, a tall thin golden spire, ships, sunny",
  card="1703")
b("E cria um imposto sobre a barba. Quem quisesse manter a barba pagava e andava com uma moedinha de recibo. Imagine ter que mostrar o comprovante da sua barba.",
  f"beard_cut|{PEDRO}, cutting the long beard of a shocked old Russian noble with big scissors, other nobles holding their beards in fear, comic",
  "beard_token|Close view of a small copper token with a simple engraving of a beard on it in the palm of a bearded man, symbolic" + SEMTXT)
b("Só que a conta disso tudo caiu nas costas de quem já estava preso à terra. A Rússia se modernizava em cima e apertava embaixo.",
  "palace_vs_field|Split view: on top a bright ballroom with nobles in European wigs dancing, below a muddy field where peasants pull a plow in the rain, symbolic",
  "tax_peasant|A round-white-head cartoon tax collector in a European coat taking the last coins and a goat from a poor peasant family in front of a wooden hut")

# ───────────────────────── 8. CATARINA E NAPOLEÃO ─────────────────────────
cap("8. O inverno que levou a fama")
b("São Petersburgo, mil setecentos e sessenta e dois. Uma princesa alemã derruba o próprio marido, o czar, e assume o trono. Ela vai ser Catarina, a Grande.",
  f"catherine_coup|{CATA}, riding a white horse in a green military uniform in front of cheering guard soldiers in a palace square" + SEMBAND,
  f"catherine_throne|{CATA}, sitting on a golden throne in a huge bright palace hall@@CATARINA, A GRANDE",
  card="1762")
b("Catarina anexa a Crimeia e ajuda a dividir a Polônia até ela sumir do mapa. Mas, no Volga, um cossaco chamado Pugachev lidera uma revolta enorme dizendo ser o marido morto dela. [curious] Ela não reconheceu.",
  "black_sea_fleet|Russian sailing warships in a sunny bay of the Black Sea with white cliffs, 1780s" + SEMBAND,
  "map_poland|Map of Central and Eastern Europe with a land in the middle being cut into three pieces like a cake by three hands with knives, " + MAPA,
  "pugachev|A round-white-head cartoon Cossack with a simple flat black beard shape wearing a fake crown and a red coat, proudly leading a crowd of rebels with pitchforks",
  "catherine_eyeroll|A round-white-head cartoon empress with powdered grey hair rolling her eyes while reading a letter, comic" + SEMTXT,
  card="1783")
b("§ Mil oitocentos e doze. Imagine seiscentos mil homens atravessando a fronteira atrás de Napoleão. Ele quer uma grande batalha. Só que os russos recuam e vão queimando o que deixam para trás.",
  f"napoleon_niemen|{NAPO}, on a white horse watching his huge army cross a river on wooden bridges in summer" + SEMBAND + "@@NAPOLEÃO",
  f"grande_armee|An endless column of {FRAN} marching on a dusty road through a flat summer plain" + SEMBAND,
  "scorched_earth|Russian peasants and soldiers setting fire to a wheat field and a village before leaving, smoke, summer",
  card="1812")
b("Imagine marchar no calor, com fome e tifo: dezenas de milhares morrem antes de qualquer frio. Napoleão entra em Moscou, encontra a cidade vazia… e ela pega fogo. Ele espera um mês por uma paz que não vem.",
  f"sick_soldiers|Exhausted {FRAN} lying in the dust by a road in the summer heat, thirsty and sick, no gore",
  f"empty_moscow|{NAPO}, standing alone in an empty Moscow square with onion domes, looking around confused, comic",
  "moscow_fire|Old Moscow burning at night, flames over wooden houses and onion domes, French soldiers watching from the Kremlin walls" + SEMBAND,
  "napoleon_waits|A round-white-head cartoon French emperor in a bicorne hat sitting at a window drumming his fingers, an empty letter tray, a calendar of pages flying, comic" + SEMTXT)
b("Só então ele recua, e aí, sim, chega o inverno. Dos seiscentos mil, a grande maioria não volta. O inverno levou a fama, mas quem venceu foi a distância.",
  f"retreat_snow|The French army retreating through a terrible snowstorm, {FRAN} wrapped in blankets, frozen cannons, {INV}" + SEMBAND,
  "map_napoleon|Map of Eastern Europe with a thick tan band going from the west to a point in the east and a thin black band coming back, " + MAPA,
  "general_winter|A comic giant old man made of snow and ice with a white beard shape wearing a Russian military coat, blowing cold wind over tiny French soldiers")
b("Em mil oitocentos e catorze, soldados russos desfilam em Paris. E a vitória convenceu o czar de que o sistema funcionava. Mas não funcionava.",
  f"cossacks_paris|{COSS} on horseback in a Paris street of 1814 with stone buildings, Parisians watching curiously" + SEMBAND,
  "tsar_proud|A round-white-head cartoon Russian tsar of 1814 in a white uniform with gold epaulettes smiling proudly in front of a victory parade" + SEMBAND,
  card="1814")

# ───────────────────────── 9. LIVRES, MAS DEVENDO ─────────────────────────
cap("9. Livres, mas devendo")
b("Crimeia, mil oitocentos e cinquenta e quatro. Ingleses e franceses chegam em navios a vapor; os reforços russos, a pé, porque não há trem até o sul. A mesma distância que derrotou Napoleão agora derrota a Rússia.",
  "steam_ships|British and French steam warships with smoking chimneys arriving in a bay of Crimea, 1854" + SEMBAND,
  f"muddy_march|{RUS1812.replace('of 1812', 'of the 1850s')} marching through deep mud on an endless road with carts stuck, rain, exhausted",
  "sevastopol|The besieged port city of Sevastopol with stone forts under cannon fire and smoke over the sea" + SEMBAND,
  card="1854")
b("§ Em mil oitocentos e sessenta e um, o czar Alexandre Segundo liberta mais de vinte milhões de servos. Pense nisso: o Brasil só aboliria a escravidão vinte e sete anos depois.",
  f"alexander_decree|{ALEX2}, signing a big decree at a desk in a palace office@@ALEXANDRE II",
  "serfs_read|A crowd of round-white-head cartoon Russian peasants listening to a priest reading a decree in front of a village church, some crying with joy, winter" + SEMTXT,
  "brazil_1888|Round-white-head cartoon Black Brazilian people drawn with dignity celebrating in the street of Rio de Janeiro in 1888, colonial buildings, flowers thrown" + SEMBAND,
  card="1861")
b("Só que a liberdade vinha com dívida: o camponês tinha que pagar pela terra em prestações, por quarenta e nove anos. [serious] Lembra da nossa pergunta? Ela ficou mais difícil: a ordem afrouxava, e ninguém ficava satisfeito.",
  "debt_peasant|A round-white-head cartoon peasant holding a tiny piece of land in one hand and a very long paper bill unrolling to the floor in the other, shocked, comic" + SEMTXT,
  "angry_students|Round-white-head cartoon students and workers arguing passionately in a smoky basement around a table with papers, 1870s" + SEMTXT)
b("Em mil oitocentos e oitenta e um, revolucionários matam Alexandre com uma bomba, e os herdeiros dele concluem que reformar é perigoso.",
  "bomb_canal|A street along a canal in Saint Petersburg in winter with a cloud of white smoke near an overturned imperial carriage, guards running, no gore",
  card="1881")
b("§ Domingo, janeiro de mil novecentos e cinco. Operários marcham até o palácio do czar com ícones e retratos dele. Os soldados atiram. Para muita gente, ali morreu a ideia do czar como pai.",
  f"bloody_sunday_march|A peaceful march of {OPER} carrying Orthodox icons and portraits through snowy streets toward a big green and white palace, {INV}",
  "soldiers_fire|A line of soldiers with rifles in front of a palace in the snow, smoke from the guns, people fleeing, dramatic, no gore",
  "broken_portrait|A broken framed portrait of a tsar lying in the snow, symbolic" + SEMTXT,
  card="1905")
b("Aí vem a Primeira Guerra: milhões de mortos e falta de pão. Em fevereiro de mil novecentos e dezessete, os soldados se recusam a atirar nos protestos, e Nicolau Segundo abdica. Trezentos anos de Romanov acabam em poucos dias.",
  f"ww1_trench|{SOV.replace('of the 1940s in khaki uniforms and helmets', 'of 1915 in grey-green greatcoats and caps')} in a muddy trench with few rifles, cold and tired" + SEMBAND,
  "bread_line|A long line of round-white-head cartoon women in headscarves waiting in the snow in front of a closed bakery in Petrograd, 1917" + SEMTXT,
  f"nicholas_abdicates|{NIC2}, signing a paper sadly in a train carriage, officers watching@@NICOLAU II",
  card="1917")
b("Em outubro, os bolcheviques de Lênin tomam o poder. [curious] Detalhe: pelo nosso calendário, a Revolução de Outubro foi em novembro. Mas o problema era o de sempre: quem ia pôr ordem nessa terra enorme?",
  f"lenin_speech|{REV}, giving a passionate speech from the top of an armored car to a crowd of soldiers and workers with red flags without symbols@@LÊNIN",
  "winter_palace|Russian revolutionary soldiers in long grey greatcoats and sailors in striped shirts and black caps running into the courtyard of a big green and white palace at night, searchlights, 1917, no flags, no tricolor flags",
  "calendar_joke|A comic scene: two old paper wall calendar pages with only empty grid squares and red crosses, no words, no letters, no month names, and a round-white-head cartoon Russian worker of 1917 in a flat cap and grey coat scratching his head" + SEMTXT)

# ───────────────────────── 10. A ORDEM DE FERRO ─────────────────────────
cap("10. A ordem de ferro")
b("Lênin leva a capital de volta para Moscou e, depois de uma guerra civil, nasce a União Soviética. Os czares saem, mas quase todo o território fica. O império trocou de bandeira.",
  "civil_war_train|An armored train with a plain red star on the front crossing a snowy plain, soldiers in long coats on top, 1919",
  "map_ussr|Map of the northern half of Europe and Asia with the huge territory of the Soviet Union painted deep red, the other lands pale, " + MAPA,
  "flag_change|Symbolic scene: a golden double-headed eagle flag being lowered and a plain red flag with a small golden hammer and sickle being raised over red brick walls" + SEMTXT,
  card="1922")
b("Imagine que você é um camponês em mil novecentos e trinta. O Estado leva a sua terra e o seu gado para a fazenda coletiva. Stálin quer fazer em dez anos a indústria que outros fizeram em cem.",
  f"collectivization|Soviet officials in leather coats taking cows and sacks of grain from a crying peasant family in front of their wooden hut, sad, no violence",
  f"stalin_plan|{STAL}, pointing at a big chart with a red line going up in an office full of officials" + SEMTXT + "@@STÁLIN",
  "factory_build|A gigantic steel factory being built on an empty steppe with cranes, smoke and thousands of round-white-head cartoon workers, 1930s",
  card="1930")
b("Saem fábricas e cidades inteiras. Mas a fome de mil novecentos e trinta e dois mata milhões, sobretudo na Ucrânia e no Cazaquistão, e os expurgos mandam centenas de milhares para o fuzilamento ou o Gulag.",
  "empty_fields|An empty grey village with abandoned huts and an empty wheat field under a cold sky, very sad, no people, no gore",
  "gulag|A prison labor camp in the snowy Siberian taiga with wooden barracks, barbed wire fences and watchtowers, a line of prisoners in grey coats, sad, no gore",
  "night_arrest|A black car parked at night in front of an apartment building, one lit window with a frightened family, ominous" + SEMTXT,
  card="1932")
b("§ Em mil novecentos e quarenta e um, Hitler repete Napoleão: atravessa a planície. A União Soviética perde uns vinte e sete milhões de pessoas. Pense: é mais gente do que mora hoje em Minas Gerais. E, mesmo assim, chega a Berlim.",
  "tanks_plain|Endless columns of grey tanks advancing across a flat summer plain toward a burning horizon, 1941" + SEMBAND,
  f"stalingrad|{SOV} in the snowy ruins of a big destroyed city on a river, {INV}, no gore" + SEMBAND,
  "berlin_1945|Soviet soldiers celebrating on the roof of a big damaged stone building in a ruined city, a red flag without symbols, 1945",
  card="1941")
b("Em mil novecentos e sessenta e um, Iúri Gagárin vira o primeiro homem no espaço. Na decolagem, ele diz: [amazed] vamos lá!",
  "gagarin|A round-white-head cartoon smiling cosmonaut in an orange spacesuit with a round white helmet, waving, inside a small round spaceship cabin" + SEMTXT + "@@IÚRI GAGÁRIN",
  "vostok_launch|A tall white rocket launching from a flat steppe in a cloud of fire and smoke, crowds watching from far away, 1961" + SEMTXT,
  card="1961")
b("§ E aqui está a terceira peça. Repare: invasores entraram muitas vezes, mas nenhum ficou de vez. Quem derrubou cada ordem russa foi a própria Rússia, por dentro: em mil seiscentos e dez, em mil novecentos e dezessete… e estava para acontecer de novo.",
  "piece_three|A third golden puzzle piece fitting into a puzzle that shows a giant red land cracking from the inside, symbolic" + SEMTXT,
  "matryoshka_crack|A big painted Russian nesting doll with a crack running down the middle, smaller dolls peeking out from inside, symbolic" + SEMTXT,
  "invaders_leave|Symbolic scene: three tiny figures, a Mongol rider, a French emperor in a bicorne hat and a grey tank, all moving away from a huge snowy land, comic" + SEMBAND)
b("Nos anos oitenta, Gorbatchov tenta abrir o sistema, e ele desmonta. No Natal de mil novecentos e noventa e um, a bandeira vermelha desce do Kremlin, e a União Soviética vira quinze países. A Rússia continua sendo o maior país do mundo, mas sem o império em volta.",
  f"gorbachev|{GORB}, opening a big heavy rusty door and light pouring in, surprised officials behind him@@GORBATCHOV",
  "flag_down|A plain red flag with a small golden hammer and sickle being lowered from a flagpole on a dome of the Kremlin at night in the snow, December 1991" + SEMTXT,
  "map_15|Map of the northern half of Europe and Asia: only the territory of the former Soviet Union is colored, split into fifteen countries of different colors with a huge red Russia across the north from the Baltic to the Pacific, all other lands pale beige, no people, no figures, " + MAPA,
  card="1991")

# ───────────────────────── FECHO (≤ 45 s) ─────────────────────────
cap("Fecho")
b("§ Naquele Natal, a frase de oitocentos e sessenta e dois cabia de novo: grande e rica, mas sem ordem. E a resposta da nossa pergunta: numa planície sem muralha, a ordem sempre veio de cima, e quem pagou foi quem estava embaixo.",
  "phrase_return|The old parchment scroll tied with a red string from the beginning, now untied and open on a table next to a window with a snowy Moscow skyline at night, symbolic" + SEMTXT,
  "piece_final|A finished golden puzzle showing the whole story of Russia from Viking boats on a river to a rocket in space, symbolic" + SEMTXT,
  "pyramid_people|A symbolic pyramid of round-white-head cartoon people: a crowned ruler sitting on top and many peasants and workers holding everything up at the bottom")
b("[warm] Talvez a pergunta nunca tenha sido como a Rússia ficou tão grande. E sim como uma terra tão grande consegue ter ordem sem que ela custe tão caro.",
  "plain_sunset|The vast flat Russian plain with birch forests and a wide river at sunset, a small village with a wooden church, peaceful")
b("E para você: em que momento a Rússia podia ter virado outra coisa? Conta aí nos comentários.",
  f"guide_comment|{GUIA} sitting on a fallen old wooden sign by a river with birch trees, holding a small painted nesting doll, thinking" + SEMTXT,
  "saint_basil_snow|Saint Basil's Cathedral with colorful onion domes in light snow at dusk, warm lights, round-white-head cartoon people walking")

# Grafia para a VOZ (o Fish lê como português). Conferir no teste de nomes (qa/pronuncia/).
# blocos.json leva "texto" (falado, vai ao Fish) e "tela" (grafia correta: legendas e SCRIPT).
FALA = [("Rúrik", "Rúrik"), ("Dniepre", "Dniépre"), ("Vladimir", "Vladímir"), ("Iaroslav", "Iarosláv"), ("Riazan", "Riazã"),
        ("Batu", "Batú"), ("Kalita", "Kalitá"), ("Ugra", "Ugrá"), ("Ivan", "Ivã"), ("Kazan", "Kazã"), ("Iermak", "Iermák"),
        ("Huaynaputina", "Uainaputina"), ("Minin", "Mínin"), ("Pojarski", "Pojárski"), ("Romanov", "Románof"),
        ("Mikhailov", "Mirráilof"), ("Poltava", "Poltáva"), ("Pugachev", "Pugatchóf"), ("Gorbatchov", "Gorbatchóv"), ("czar", "tzar"), ("czares", "tzares"),
        ("Iúri", "Iúri"), ("Gulag", "Gulág"), ("Gengis Khan", "Gêngis Cã")]
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
