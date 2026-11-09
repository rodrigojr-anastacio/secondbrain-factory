#!/usr/bin/env python3
"""Fonte única do 006-roma (09/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

1º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
Molde History in Minutes (narrativa contínua). Referência de código: videos/005-brasil e 004-china.
  hook: 390 a.C., Breno joga a espada na balança do resgate: "ai dos vencidos" (Lívio 5.48)
  → PERGUNTA CENTRAL (≤ 0:50) → "Essa é a história inteira de Roma" → 1 "guarde" (a espada na balança) → o brejo (problema da era 1)
  → 10 eras, cada uma: problema herdado → cena no presente → ≤ 3 fatos → solução → novo problema
  → fecho ≤ 45 s: responde, reenquadra (os vencidos ficaram com Roma: o latim na sua boca) e pergunta para os comentários.
Fio condutor: A BALANÇA DO "AI DOS VENCIDOS". Roma aprende a regra de Breno ao contrário: em vez de cobrar ouro do vencido, faz dele
  romano (peça 1 da resposta); depois para de dividir (Gracos, aliados, Sila), vira a mão que pesa (Cartago, Gália); fica grande demais
  (peça 2); paga resgate de novo (Alarico, 408: cinco vezes o ouro de Breno) e vira a vencida (peça 3, 410/476).
Pergunta volta: era 3 (1ª peça), era 5 ("lembra da nossa pergunta?"), era 8 (2ª peça), era 10 (pergunta do começo, 3ª peça), fecho (resposta).

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="390 a.C.") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py em teste no 006 (regra 10 da v2).
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (004/005: ~126–129 ppm com pausas)
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
TITULO = "A história INTEIRA de Roma"
PERGUNTA = "Como uma cidade que pagou resgate aos bárbaros virou a dona do mundo e, oitocentos anos depois, virou a vencida?"

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
# Personagens (regra da bíblia: nada de rosto descrito; "round-white-head cartoon …")
LEG = "round-white-head cartoon Roman legionaries in red tunics, segmented iron armor, plain red curved rectangular shields and bronze helmets"
SEN = "round-white-head cartoon Roman senators in white togas with a red border stripe"
GAUL = "round-white-head cartoon Gaulish warriors with long orange and brown hair, simple flat mustache shapes, checkered trousers and long swords"
BRENO = "a big round-white-head cartoon Gaulish chieftain with a simple flat long orange mustache shape, long orange braids, a bronze helmet with small wings and a checkered cloak"
TARQ = "an arrogant round-white-head cartoon Etruscan king with a simple flat black beard shape, a golden wreath and a purple embroidered robe"
CAMILO = "a round-white-head cartoon old Roman general with short grey hair, bronze armor and a red cloak"
ANIBAL = "a round-white-head cartoon Carthaginian general with a simple flat short black curly beard shape, a black eye patch, a bronze breastplate and a purple cloak"
CIPIAO = "a young round-white-head cartoon Roman general, clean shaven with short brown hair, a bronze muscle cuirass and a red cloak"
CATAO = "an old grumpy round-white-head cartoon Roman senator, bald on top with short white hair at the sides, in a plain white toga"
TIBERIO = "a young round-white-head cartoon Roman tribune with short dark hair in a plain white toga"
MARIO = "a tough round-white-head cartoon Roman general with short grey hair and a plain battered bronze armor"
SILA = "a round-white-head cartoon Roman general with blond hair, a red cloak and a cold proud look"
CESAR = "a round-white-head cartoon Roman general with thin short hair and a green laurel wreath, a red cloak over bronze armor"
CESAR_JOVEM = "a young round-white-head cartoon Roman nobleman with short dark hair in an elegant white tunic with a purple border"
VERC = "a round-white-head cartoon Gaulish king with a simple flat long blond mustache shape, long blond hair and a bronze helmet with wings"
CLEO = "a round-white-head cartoon Egyptian queen with a black bob haircut, a golden cobra crown and a white linen dress"
OTAV = "a young round-white-head cartoon Roman ruler with short neat light-brown hair, a white toga with a purple border and a laurel wreath"
AUG_VELHO = "an old round-white-head cartoon Roman emperor with short white hair, a white toga with a purple border and a laurel wreath"
ANTONIO = "a round-white-head cartoon Roman general with curly dark hair and a simple flat short beard shape, bronze armor"
CARACALA = "a round-white-head cartoon Roman emperor with a simple flat short curly dark beard shape, a frowning face and a purple cloak"
DIOC = "an old round-white-head cartoon retired Roman emperor with a simple flat short white beard shape, in a simple brown work tunic"
CONST = "a round-white-head cartoon Roman emperor, clean shaven with short dark hair, golden armor and a purple cloak"
ALARICO = "a round-white-head cartoon Gothic king with long blond hair, a simple flat blond beard shape, a fur cloak and an iron helmet"
ODOACRO = "a big round-white-head cartoon barbarian general with long brown hair, a simple flat brown mustache shape and a late Roman officer cloak"
MENINO = "a small round-white-head cartoon teenage boy emperor in an oversized purple cloak and a too-big golden diadem"
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes"

# ───────────────────────── HOOK (390 a.C.: a espada de Breno na balança) ─────────────────────────
cap("Hook")
b("[serious] Roma, trezentos e noventa antes de Cristo. A cidade está pegando fogo, e quem pôs fogo foram os gauleses.",
  f"rome_burning|The small ancient city of Rome in 390 BC burning, red tile roofs and temples on hills on fire, smoke in the sky, {GAUL} running through the streets" + SEMBAND,
  f"gauls_street|{GAUL} with torches walking through an empty ancient Roman street with columns and burning houses, night glow" + SEMBAND,
  "capitol_hill|The rocky Capitoline hill with a small temple on top, Roman defenders behind a wall looking down at smoke rising from the city below",
  f"gaul_camp|A camp of {GAUL} around fires below a rocky hill, tents and loot piled up, evening",
  card="390 a.C.")
b("Imagine que você é um senador romano, preso no alto de um morro, cercado e com fome. Os gauleses topam ir embora… por mil libras de ouro.",
  f"hungry_senators|Three hungry {SEN} sitting on rocks on top of a hill, empty bowls, looking worried, a campfire",
  "gold_pile|A big pile of shiny gold bars, gold cups, gold rings and coins on a cloth on the ground, Roman women giving their jewelry",
  f"breno_demand|{BRENO}, pointing with one finger and smiling greedily at a pile of gold, his warriors laughing behind him" + SEMBAND,
  "deal_handshake|A tense meeting on a hill between a Roman senator in a white toga and a huge Gaulish chieftain, both with arms crossed, warriors watching",
  "senator_view|A round-white-head cartoon Roman senator on top of a rocky hill looking down at the burning city below, hands on his head")
b("Na pesagem, os romanos reclamam que os pesos estão roubados. Aí o chefe gaulês, Breno, tira a espada, joga em cima da balança e diz: [slightly dramatic] ai dos vencidos.",
  "scale_weigh|A big ancient bronze balance scale on a wooden table, gold on one pan and dark stone weights on the other, a Roman official frowning at it",
  f"romans_protest|Angry {SEN} pointing at the weights of a big balance scale and shouting in protest",
  f"breno_sword|{BRENO}, throwing his long iron sword onto the weights pan of a big bronze balance scale with a dramatic gesture, gold on the other pan" + SEMBAND + "@@BRENO",
  "sword_on_scale|Close view of a long iron sword lying across the pan of a bronze balance scale, the scale tipping down, gold coins flying, dramatic light",
  f"breno_laugh|{BRENO}, laughing loudly with his hands on his hips, Roman senators in shock around him" + SEMBAND)
b("[curious] Pelo menos, é assim que conta o historiador Tito Lívio, mais de três séculos depois. Detalhe: ele era romano. E nas histórias romanas o gaulês é sempre o vilão.",
  "livy_writing|A round-white-head cartoon Roman historian in a toga writing on a long scroll at a desk with oil lamps and piles of scrolls, smiling slyly" + SEMTXT + "@@TITO LÍVIO",
  "scroll_gaul|An unrolled ancient papyrus scroll on a desk with a small drawing of a big angry Gaulish warrior on it, a quill and an ink pot" + SEMTXT,
  "livy_wink|A round-white-head cartoon Roman historian winking while holding up a scroll, comic",
  "gaul_villain|A comic ancient theater stage where an actor dressed as a huge Gaulish warrior plays the villain with an evil laugh while Roman actors play the heroes",
  "livy_reading|A round-white-head cartoon Roman historian reading a scroll aloud to a group of Romans in a sunny garden with columns")
b("§ [serious] E aqui fica a pergunta: como uma cidade que pagou resgate aos bárbaros virou a dona do mundo e, oitocentos anos depois, virou a vencida?",
  "map_empire_hook|Map of the Mediterranean Sea and Europe with the huge territory of the Roman Empire around the sea painted deep red, the lands outside pale, the sea blue, " + MAPA,
  "colosseum_glory|The Colosseum and the Roman Forum in their full glory under a bright blue sky, crowds of round-white-head cartoon Romans in togas",
  f"legion_march|A huge Roman legion marching in perfect lines on a stone road, {LEG}, golden eagle standards" + SEMBAND,
  f"goths_rome|{ALARICO.replace('a round', 'A round')} and his Gothic warriors riding into the ruined city of Rome through a broken gate, smoke behind" + SEMBAND,
  "scale_flip|A giant bronze balance scale tipping over, a small Roman village on one side becoming a marble city, symbolic, dramatic sky")
b("Essa é a história inteira de Roma. Guarde essa espada na balança: ela volta. E tudo começa num lugar em que ninguém apostaria. Um brejo.",
  "seven_hills|Aerial view of seven green hills around a marshy valley and a winding river, a few huts on the hills, early Iron Age Italy, no city yet",
  "sword_kept|A long iron sword lying across an empty bronze balance scale in the shadow, a single beam of light, mysterious, symbolic",
  "marsh_frogs|A muddy marsh between hills with reeds, frogs and mosquitoes, a comic surprised frog in front, early morning mist",
  "marsh_valley|Wide view of a misty marshy valley between green hills with tall reeds and a river, birds flying, no buildings, dawn")

# ───────────────────────── 1. O BREJO E OS REIS ─────────────────────────
cap("1. Uma aldeia no meio do brejo")
b("Olhe para a Itália oitocentos anos antes de Cristo. Um rio, o Tibre, e sete morros em volta de um vale alagado. No alto, cabanas de palha. Lá embaixo, sapo e mosquito.",
  "heron_marsh|A white heron standing in a marsh among tall reeds, small green hills far behind, peaceful morning",
  "palatine_huts|Round huts with thatched straw roofs on top of a green hill in early Iron Age Italy, families of round-white-head cartoon villagers with goats, smoke from a fire",
  "tiber_river|The Tiber river winding between green hills under a blue sky, reeds and a small wooden boat, no city",
  "map_italy_tiber|Map of the Italian peninsula with a small red dot in the middle of the west coast on a river, the sea around blue, " + MAPA,
  "villager_mosquito|A round-white-head cartoon villager in a simple wool tunic slapping a mosquito on his arm next to a muddy marsh, comic",
  "iron_family|A round-white-head cartoon Iron Age family in simple wool clothes sitting by a fire in front of their straw hut on a hill, goats and a dog",
  "hut_inside|Inside a simple round straw hut in early Iron Age Italy, a clay oven, pots and a loom, warm firelight",
  card="c. 800 a.C.")
b("Os romanos depois inventaram uma origem mais bonita: os gêmeos Rômulo e Remo, jogados no rio e criados por uma loba. Rômulo mata o irmão e dá o nome à cidade.",
  "wolf_twins|A gentle she-wolf in a cave by a river with two cartoon baby twins with round white heads, warm light, legend style",
  "twins_river|A basket with two cartoon baby twins floating on a river among reeds, legend style",
  "brothers_fight|Two young round-white-head cartoon brothers in simple tunics arguing furiously over a line plowed in the ground on a hill, legend style",
  "romulus_wall|A young round-white-head cartoon founder plowing a furrow around a hill with two white oxen, legend style, dawn",
  "wolf_statue|An ancient bronze statue of a she-wolf feeding two small babies, displayed in a museum, soft light")
b("[curious] É lenda. Mas diz muito sobre Roma: ela começa com briga de família. O fato é mais prosaico: a aldeia tinha um vau no rio, sal perto do mar e uma rota de comércio passando na porta.",
  "salt_traders|Round-white-head cartoon traders carrying sacks of salt on mules across a shallow ford of a river, hills behind",
  "ford_crossing|A shallow river ford with merchants, sheep and carts crossing, a small village on the hill above, sunny",
  "salt_pans|White salt pans at the mouth of a river by the sea, workers raking salt, ancient Italy",
  "legend_fact|Split view: on the left a legendary she-wolf with twins in golden light, on the right archaeologists digging the postholes of ancient huts on a hill, symbolic",
  "cattle_market|Round-white-head cartoon herders trading cattle and salt at a riverside market next to a shallow ford, early Iron Age Italy",
  "river_boats|Small merchant boats on the Tiber river unloading clay jars and sacks of salt at a riverside village, sunny")
b("§ Pense numa vila à beira de uma rodovia: todo mundo para ali. Só que lugar bom atrai dono. Os últimos reis de Roma vieram dos etruscos, os vizinhos ricos do norte.",
  "etruscan_city|A rich Etruscan city on a hilltop with painted temples and walls, nobles in colorful robes, ancient Italy",
  f"etruscan_king|{TARQ}, sitting on an ivory throne in a painted Etruscan hall, servants around him",
  "forum_drain|Round-white-head cartoon workers digging a big stone drain channel in a muddy valley, turning the marsh into a dry square, ancient Rome",
  "highway_stop|A comic modern analogy: a busy roadside diner and gas station on a highway where every car and truck stops, round-white-head cartoon travelers" + SEMTXT,
  "etruscan_banquet|Etruscan nobles in colorful robes lying on couches at a banquet in a hall with painted walls, musicians playing double flutes")
b("Foram eles que drenaram o brejo e fizeram dele uma praça, o Fórum. O último rei, Tarquínio, o Soberbo, era tão odiado que o apelido já diz tudo.",
  "early_forum|The early Roman Forum: a simple paved square with a few temples and market stalls between hills, ancient Rome",
  f"tarquin_arrogant|{TARQ}, with his nose in the air, walking past bowing Roman citizens who glare at him behind his back",
  f"tarquin_out|{TARQ}, being chased out of the city gates by an angry crowd of round-white-head cartoon Romans, comic",
  "tarquin_feast|An arrogant round-white-head cartoon Etruscan king eating grapes on a throne while tired Roman workers carry heavy stones outside the window",
  card="509 a.C.")
b("Em quinhentos e nove antes de Cristo, os romanos expulsam o rei e juram nunca mais ter outro. O problema: e agora, quem manda?",
  "oath_no_king|Round-white-head cartoon Romans raising their right hands in an oath in front of a temple, an empty throne in front of them",
  "empty_throne|An empty ivory throne with a golden wreath on it in an empty hall, dramatic light, symbolic",
  "who_rules|Confused round-white-head cartoon Roman citizens looking at each other in a square, scratching their heads, comic",
  "romans_cheer|A crowd of round-white-head cartoon Romans cheering and celebrating in the square after expelling the king, throwing flowers")

# ───────────────────────── 2. A REPÚBLICA ─────────────────────────
cap("2. Uma cidade sem rei")
b("A resposta foi dividir o poder. Em vez de um rei, dois cônsules, eleitos por um ano só, e cada um podia vetar o outro. E um Senado de velhos ricos que só dava conselho. Conselho que ninguém ousava ignorar.",
  f"two_consuls|Two round-white-head cartoon Roman consuls in togas with purple borders sitting side by side on folding ivory chairs, each raising a hand to stop the other, comic",
  f"senate_old|Many old {SEN} sitting on benches in a stone hall, frowning, one standing and speaking",
  "lictors|Round-white-head cartoon Roman guards carrying bundles of rods with axes walking in front of a consul through a street",
  "voting|Round-white-head cartoon Roman citizens in a line dropping small wooden tablets into a big basket to vote, an official watching",
  "consuls_argue|Two round-white-head cartoon Roman consuls in togas with purple borders standing back to back with crossed arms, sulking, comic",
  "senate_house|The Roman Senate house, a tall simple brick building with bronze doors, senators in togas walking up the steps")
b("Mas quem lutava as guerras era a plebe, o povo comum, que não mandava em nada. Então, em quatrocentos e noventa e quatro, ela faz uma coisa genial: vai embora e acampa num morro.",
  "plebs_work|Round-white-head cartoon Roman common people working: a baker, a blacksmith, a farmer and a soldier, simple tunics, busy street",
  "plebs_leave|A long line of round-white-head cartoon Roman common people with bundles leaving the city gates, walking toward a hill",
  "plebs_hill|A camp of common Roman people on a green hill outside the city, tents and fires, arms crossed, determined",
  card="494 a.C.")
b("Imagine uma greve geral: a cidade sem soldado, sem padeiro, sem pedreiro. O Senado cede, e a plebe ganha os seus tribunos e, depois, leis escritas na praça, para todo mundo ler.",
  "empty_city|An empty ancient Roman street with closed shops, an abandoned bakery oven and a lonely senator looking around, comic",
  f"senate_gives|Nervous {SEN} walking up to the camp of the common people on a hill, offering a handshake",
  "twelve_tables|Twelve big bronze tablets fixed on a wall in the Roman Forum, citizens reading them, the tablets covered with tiny unreadable marks" + SEMTXT)
b("§ Roma estava aprendendo a resolver as brigas por dentro. Mas o perigo veio de fora. Em trezentos e noventa, os gauleses descem do norte, esmagam o exército romano e entram na cidade. É a cena da balança.",
  f"gauls_alps|A huge horde of {GAUL} coming down from snowy mountains toward the green plains of Italy" + SEMBAND,
  f"allia_battle|A chaotic battle by a small river: {GAUL} charging and Roman soldiers running away in panic" + SEMBAND,
  "breno_sword#detalhe-centro",
  card="390 a.C.")
b("Conta a lenda que o general Camilo chega na hora e diz que Roma se resgata com ferro, não com ouro. Bonito, mas provavelmente inventado. O certo é que Roma pagou. E aprendeu a lição de Breno: [serious] nunca mais ser a vencida.",
  f"camillus|{CAMILO}, arriving at the weighing scene and pushing away the gold with his sword, legend style",
  "servian_wall|Round-white-head cartoon Roman workers building a tall stone city wall with big square blocks around the hills of Rome",
  "never_again|A Roman boy and an old Roman man watching from a new stone wall at sunset, determined, the city behind them")

# ───────────────────────── 3. VENCIDOS QUE VIRAM ROMANOS ─────────────────────────
cap("3. Fazer do inimigo um romano")
b("Então Roma ergue uma muralha de pedra e sai para conquistar a Itália. Mas repare no truque. Quando vencia uma cidade, Roma não cobrava ouro, como Breno. Cobrava soldados.",
  f"conquer_italy|{LEG} marching out of the gates of Rome toward green Italian hills with small walled towns" + SEMBAND,
  "map_italy_conquest|Map of the Italian peninsula with the center painted red and the red area spreading south, the sea blue, " + MAPA,
  "trick_soldiers|A Roman officer at a table recruiting young men from a conquered Italian town, they line up with spears and shields, sunny",
  card="338 a.C.")
b("A cidade vencida virava aliada. Ficava com as suas leis e os seus deuses, mandava homens para o exército e dividia o saque da guerra seguinte. Algumas ganhavam até a cidadania. [warm] O vencido de ontem era o legionário de amanhã.",
  "allies_feast|A Roman officer and the leaders of a conquered Italian town sharing bread and wine at a long table, friendly, both groups in different clothes",
  "citizen_toga|A happy round-white-head cartoon man from a conquered Italian town putting on a white Roman toga for the first time, family cheering",
  "mixed_legion|A Roman army column with soldiers of many Italian peoples in slightly different armors marching together" + SEMBAND)
b("§ E, para ligar tudo, estradas. Em trezentos e doze começa a Via Ápia: de pedra, reta, feita para o exército andar rápido. Trechos dela estão lá até hoje. Tente dizer o mesmo do asfalto da sua rua.",
  "appian_build|Round-white-head cartoon Roman workers laying big flat paving stones of a straight road in layers of gravel and sand, a surveyor with a measuring tool",
  "appian_today|The ancient Appian Way today: big old paving stones between tall umbrella pine trees and cypress trees, a tourist walking",
  "pothole_street|A modern city street full of potholes with a car splashing water and an annoyed round-white-head cartoon pedestrian, comic",
  card="312 a.C.")
b("[curious] E aqui está a primeira peça da resposta. Roma não cresceu porque esmagava os vencidos. Cresceu porque fazia deles romanos. Cada guerra ganha deixava o exército maior para a próxima.",
  "piece_one|A big golden puzzle piece being placed into a puzzle that shows a small map of Italy, a round-white-head cartoon Roman holding it, symbolic" + SEMTXT,
  "army_grows|A small group of Roman soldiers that grows into a bigger and bigger army column marching across hills, symbolic sequence")
b("§ Em pouco mais de dois séculos, Roma manda na Itália inteira. Só que a Itália acaba no mar. E do outro lado, na costa da África, tem uma cidade mais rica, com a maior frota do Mediterrâneo. Cartago.",
  "italy_sea|A Roman soldier standing on a cliff at the southern tip of Italy looking at the sea, hands on hips, frustrated",
  "carthage_port|The rich city of Carthage on the coast of Africa with its famous round military harbor full of warships, palm trees, sunny",
  "map_carthage|Map of the western Mediterranean with the Italian peninsula painted red and the coast of North Africa, Sardinia and western Sicily painted purple, " + MAPA)

# ───────────────────────── 4. CARTAGO ─────────────────────────
cap("4. Cartago deve ser destruída")
b("Uma praia da Itália. Centenas de carpinteiros desmontam um navio de Cartago que encalhou. Roma não sabe fazer navio de guerra. Então copia, peça por peça.",
  "wreck_copy|Round-white-head cartoon Roman carpenters taking apart a stranded Carthaginian warship on a beach and measuring every plank, comic",
  "shipyard|A busy Roman shipyard with many warships being built at the same time, hammers, timber, sawdust",
  "rowers_sand|Round-white-head cartoon Roman rowers sitting on benches on a beach, rowing in the air with oars, an officer shouting the rhythm, comic",
  card="260 a.C.")
b("Os remadores treinam na areia, remando no seco. E, como Roma não sabe lutar no mar, põe na proa uma ponte com gancho: prende o navio inimigo e luta como se estivesse em terra.",
  "corvus|A Roman warship lowering a wooden boarding bridge with a big iron spike onto an enemy ship, Roman soldiers running across",
  "sea_battle|A sea battle between Roman and Carthaginian warships with oars, boarding bridges and soldiers fighting on decks" + SEMBAND)
b("§ Funciona, e Roma ganha a primeira guerra. Cartago quer revanche e manda o seu melhor general, Aníbal. Ele faz o impensável: atravessa os Alpes com um exército e dezenas de elefantes. [amazed] Elefantes. Na neve.",
  f"hannibal|{ANIBAL}, standing on a rocky mountain pass pointing toward Italy, his army behind him@@ANÍBAL",
  "elephants_snow|War elephants with soldiers walking through deep snow on a narrow mountain pass in the Alps, a cold surprised elephant in front, comic",
  "map_hannibal|Map of Spain, southern France and Italy with a dotted red route going from Spain over the Alps into Italy, " + MAPA,
  card="218 a.C.")
b("Em Canas, numa tarde de duzentos e dezesseis, Aníbal cerca o exército romano e mata cerca de cinquenta mil homens. Imagine um estádio lotado sumindo numa só tarde.",
  "cannae|Aerial view of a huge battle on a dry plain where a Carthaginian army surrounds a packed Roman army from all sides, dust" + SEMBAND,
  "stadium_empty|A huge modern football stadium full of cartoon fans on one side and completely empty on the other side, symbolic",
  card="216 a.C.")
b("Qualquer cidade teria se rendido. Roma, não. E sabe por quê? A maioria dos aliados do centro da Itália não trocou de lado. [warm] O truque dos vencidos que viram romanos segurou Roma de pé.",
  "allies_loyal|Leaders of Italian towns in different clothes standing firm next to Roman senators, arms crossed, refusing a Carthaginian messenger",
  f"scipio|{CIPIAO}, raising his sword in front of his army on an African plain, war elephants in the distance",
  card="202 a.C.")
b("§ Cinquenta anos depois, o velho senador Catão mostra no Senado figos fresquinhos, colhidos em Cartago três dias antes. O recado: ela está perto demais. E todo discurso dele termina igual: Cartago deve ser destruída.",
  f"cato_figs|{CATAO}, holding up big fresh purple figs in front of the Roman Senate with a meaningful look, senators staring@@CATÃO",
  "figs_close|Close view of a few big fresh purple figs in an old man's open hand, very fresh with drops of water",
  f"cato_speech|{CATAO}, banging his fist on a stone lectern at the end of a speech, other senators rolling their eyes, comic")
b("Em cento e quarenta e seis, Roma arrasa Cartago e vende quem sobrou como escravo. E não, ninguém jogou sal na terra: isso foi inventado muito depois. Agora a espada na balança era de Roma. O problema é o que vem junto com ganhar tudo.",
  "carthage_burns|The city of Carthage burning at night, Roman soldiers on the walls, flames reflected in the harbor" + SEMBAND,
  "roman_scale|A Roman general throwing his sword onto a big bronze balance scale, piles of captured gold on the other pan, symbolic",
  card="146 a.C.")

# ───────────────────────── 5. O PREÇO DA VITÓRIA ─────────────────────────
cap("5. O preço de ganhar tudo")
b("Imagine que você é um soldado romano voltando para casa depois de anos de guerra. Você chega no seu sítio… e ele não existe mais. Um senador comprou tudo, e quem planta agora são escravos das guerras.",
  "soldier_home|A tired round-white-head cartoon Roman soldier with a backpack arriving at a small farm on a hill at sunset",
  "farm_gone|The same small farm now replaced by a huge estate with a big villa and dozens of enslaved workers in the fields, the soldier shocked at the fence",
  "rich_villa|A rich Roman senator relaxing in a luxurious villa with marble columns, grapes and servants, comic")
b("Ouro e escravos entram aos montes, os ricos compram as terras, e o soldado-agricultor, a base do exército, vira pobre em Roma. Então, em cento e trinta e três, o tribuno Tibério Graco propõe dividir as terras públicas.",
  "poor_rome|Poor round-white-head cartoon families in a crowded dirty street of ancient Rome, tall wooden apartment buildings",
  f"tiberius|{TIBERIO}, speaking passionately to a big crowd of poor Romans in the Forum, pointing to the fields@@TIBÉRIO GRACO",
  card="133 a.C.")
b("Os senadores respondem com pedaços de banco. Você ouviu certo: arrancam as pernas dos bancos e matam Tibério e centenas de seguidores na rua. Pela primeira vez, a política de Roma se resolve no porrete.",
  f"bench_legs|Angry {SEN} tearing the legs off wooden benches to use as clubs, comic but tense",
  "forum_riot|A riot in the Roman Forum with senators with clubs chasing a crowd, dust and fallen chairs, no blood")
b("§ Aí vem o general Mário, com uma solução prática: se o pobre não tem terra, que vire soldado profissional, com salário e terra prometida no fim. Só que agora o soldado deve tudo ao general, não a Roma.",
  f"marius|{MARIO}, recruiting poor young men in tattered clothes who line up eagerly to get armor and a bag of coins@@MÁRIO",
  "loyal_general|Roman soldiers cheering and raising their swords to their general on a platform, ignoring a small senator behind them",
  card="107 a.C.")
b("E os aliados italianos, aqueles que seguraram Roma contra Aníbal? Pediram a cidadania e ouviram um não. Fizeram guerra e arrancaram a cidadania. [serious] Lembra da nossa pergunta? Ela acaba de ficar mais difícil: Roma estava parando de dividir.",
  "allies_refused|Italian leaders asking for citizenship in front of Roman senators, a senator showing them the door, comic",
  "social_war|Two armies dressed almost the same, Roman and Italian, facing each other on a field" + SEMBAND,
  "door_closing|A big wooden door with bronze studs closing in front of a crowd, symbolic")
b("Em oitenta e oito, o general Sila faz o que nenhum romano tinha feito: marcha com o exército contra a própria Roma. O problema estava posto: quem tem o maior exército manda. E o próximo da fila tinha um exército enorme.",
  f"sulla_march|{SILA}, riding at the head of his legions toward the walls of Rome, citizens on the walls in panic" + SEMBAND,
  "army_gates|A Roman army entering the gates of Rome itself, frightened citizens hiding behind columns" + SEMBAND,
  card="88 a.C.")

# ───────────────────────── 6. CÉSAR ─────────────────────────
cap("6. O homem que cruzou o rio")
b("Um jovem nobre romano é sequestrado por piratas. Eles pedem vinte talentos de resgate. Ele ri e diz que vale pelo menos cinquenta. Promete voltar e crucificar todos. [curious] Eles acham graça. Ele volta. E crucifica.",
  f"pirates_caesar|{CESAR_JOVEM}, sitting relaxed on a pirate ship laughing while rough pirates look confused, Mediterranean sea",
  "pirates_ransom|Pirates counting sacks of silver on the deck of a ship, the young Roman nobleman pointing at the sacks saying more, comic",
  f"caesar_returns|{CESAR_JOVEM}, arriving with warships at a pirate island, pirates panicking on the beach" + SEMBAND)
b("O nome dele é Júlio César. Em oito anos, ele conquista a Gália inteira, a terra dos netos de Breno: pelas contas de Plutarco, um milhão de mortos. O chefe gaulês, Vercingetórix, se rende e joga as armas aos pés dele.",
  f"caesar_gaul|{CESAR}, on a horse in front of his legions in a green Gaulish forest landscape" + SEMBAND + "@@JÚLIO CÉSAR",
  "map_gaul|Map of western Europe with Italy painted red and Gaul, the land of today's France, painted orange with red arrows going into it, " + MAPA,
  f"vercingetorix|{VERC}, throwing his sword and helmet at the feet of {CESAR} sitting on a chair, Roman soldiers around, the scale reversed@@VERCINGETÓRIX",
  card="52 a.C.")
b("§ O Senado manda César largar o exército. Só que, em janeiro de quarenta e nove, ele chega a um riozinho, o Rubicão, a fronteira que general armado não podia cruzar. Para, pensa… e diz: a sorte está lançada. E cruza.",
  f"rubicon|{CESAR}, on horseback at the bank of a tiny shallow river at night, thinking, his soldiers waiting behind",
  "rubicon_cross|Roman legionaries wading across a tiny shallow river at dawn with their general in front" + SEMBAND,
  "dice|Two ancient bone dice rolling on a wooden table, dramatic light, symbolic",
  card="49 a.C.")
b("Ganha a guerra civil, vira ditador e mexe até no calendário: o ano de trezentos e sessenta e cinco dias, com bissexto, é dele. Toda vez que você marca alguma coisa em julho, está homenageando César.",
  f"caesar_dictator|{CESAR}, sitting on a golden chair in the Senate while senators bow nervously",
  "calendar_july|A modern wall calendar on the page of July hanging in a kitchen, with a small laurel wreath drawn on it, a cat looking at it" + SEMTXT)
b("Mas um homem com tanto poder parecia rei, e Roma tinha jurado não ter reis. Nos idos de março de quarenta e quatro, senadores o matam com vinte e três facadas. E não, ele não disse até tu, Brutus: isso é Shakespeare.",
  "ides_march|A group of round-white-head cartoon senators in togas surrounding a man in a laurel wreath in a stone hall, daggers raised, dramatic shadows, no blood",
  "caesar_fallen|A fallen laurel wreath and a red cloak on a marble floor at the foot of a statue, dramatic, symbolic, no blood",
  "shakespeare|A round-white-head cartoon Elizabethan playwright with a ruff collar writing with a quill and smiling, a theater stage behind, comic" + SEMTXT,
  card="44 a.C.")
b("O problema é que matar César não trouxe a república de volta. Só trouxe mais guerra.",
  "civil_war_again|Two Roman armies clashing on a field under a stormy sky" + SEMBAND)

# ───────────────────────── 7. AUGUSTO ─────────────────────────
cap("7. Um rei que não se chamava rei")
b("Alexandria, trinta antes de Cristo. Cleópatra, a última rainha do Egito, se mata para não desfilar acorrentada em Roma. Quem a venceu foi Otaviano, o herdeiro de César.",
  f"cleopatra|{CLEO}, sitting sadly on a golden throne in a palace in Alexandria, a basket with a snake nearby, dramatic light",
  f"octavian_alex|{OTAV}, walking into a palace in Alexandria with Roman soldiers, Egyptian servants bowing@@OTAVIANO",
  card="30 a.C.")
b("O Egito vira a despensa de Roma. Se você viu o nosso vídeo do Egito, já conhece o fim dessa história.",
  "grain_ships|Big Roman grain ships loaded with sacks sailing from Egypt with pyramids far behind",
  "bread_rome|Round-white-head cartoon Romans receiving free bread and grain at a distribution point in Rome")
b("§ Aí Otaviano faz a jogada mais esperta da história de Roma. Ele não se diz rei. Devolve o poder ao Senado… e fica com o exército, o dinheiro e as províncias. O Senado, agradecido, dá a ele um título novo: Augusto.",
  f"octavian_senate|{OTAV}, humbly handing a scroll to the Senate while hiding a big bag of coins and an army behind his back, comic",
  f"augustus_title|{OTAV}, being honored by {SEN} who place a golden laurel crown on his head",
  card="27 a.C.")
b("[curious] Ele inventou o cargo de imperador sem nunca usar a palavra rei. Ainda ganhou um mês, agosto. E se gabava de ter recebido uma Roma de tijolo e deixado uma de mármore.",
  "brick_marble|A split view of Rome: on the left an old city of brown brick, on the right the same city in shining white marble, symbolic",
  "marble_rome|The Roman Forum and temples in shining white marble under a blue sky, round-white-head cartoon Romans walking")
b("§ Começa a Paz Romana, uns duzentos anos sem guerra grande dentro do império. Mas a fronteira sangra. No ano nove, três legiões inteiras são massacradas numa floresta da Germânia. E Augusto, já velho, bate a cabeça na porta e grita: Varo, devolva as minhas legiões!",
  "germania|Roman legionaries trapped in a dark dense forest with heavy rain and Germanic warriors attacking from the trees" + SEMBAND,
  f"augustus_wall|{AUG_VELHO}, banging his head against a palace door in despair, servants watching, comic",
  card="9 d.C.")
b("O problema é que tudo dependia de um homem só, e não havia regra para escolher o próximo. Às vezes vinha um bom. Às vezes vinha Calígula. Ou Nero.",
  "throne_lottery|A Roman throne with a big question mark shaped cloud above it and many different Romans pushing to sit on it, comic" + SEMTXT,
  "nero_lyre|A round-white-head cartoon Roman emperor with a simple flat neck beard shape playing a lyre on a balcony, a city glowing behind him, comic")

# ───────────────────────── 8. GRANDE DEMAIS ─────────────────────────
cap("8. Grande demais")
b("Ano cento e dezessete. Imagine que você é um legionário no frio da Britânia, e o seu primo serve no deserto da Síria. Mesmo exército, mesma moeda, mesma lei. Roma vai do Atlântico à Mesopotâmia, com uns sessenta milhões de pessoas.",
  "britannia_cold|A round-white-head cartoon Roman legionary shivering in the rain and wind on a grey northern hill, wrapped in a cloak",
  "syria_desert|A round-white-head cartoon Roman legionary sweating in a hot desert next to a palm tree and a camel, in a fortress gate",
  "map_empire_117|Map of Europe, North Africa and the Middle East with the Roman Empire at its largest painted red around the whole Mediterranean, " + MAPA,
  card="117 d.C.")
b("Em duzentos e doze, o imperador Caracala dá a cidadania a quase todos os homens livres do império. O vencido virou romano de vez. [curious] Generosidade? Nem tanto, porque cidadão pagava imposto de herança.",
  f"caracalla|{CARACALA}, announcing something from a balcony to a huge crowd of people of many lands@@CARACALA",
  "tax_collector|A round-white-head cartoon Roman tax collector with an abacus and a big money bag knocking at a door, a family hiding, comic",
  card="212 d.C.")
b("§ E aqui está a segunda peça da resposta: o império que crescia engolindo vizinhos agora era grande demais para ser defendido de um lugar só. Quando o inimigo atacava num canto, o imperador estava a meses de distância.",
  "piece_two|A second golden puzzle piece being placed next to the first, showing a huge red empire map, symbolic" + SEMTXT,
  "messenger_far|A tired Roman messenger on a horse riding on an endless road through mountains, days and nights passing, symbolic")
b("Então os exércitos da fronteira começam a fazer o próprio imperador. Em cinquenta anos, uns vinte e seis imperadores, quase todos assassinados. Um deles, Valeriano, acaba prisioneiro dos persas.",
  "soldiers_crown|Roman soldiers lifting their general on a shield and crowning him emperor in a camp" + SEMBAND,
  "emperor_carousel|A comic row of many different Roman emperors in purple pushing each other off a throne one after another",
  "valerian_persia|A round-white-head cartoon Persian king on a horse in front of a kneeling Roman emperor in purple, Persian soldiers around",
  card="235–284")
b("Só que, para pagar tanto soldado, o governo derrete a moeda: a moeda de prata termina com menos de cinco por cento de prata. Pense no dinheiro do seu bolso valendo menos a cada mês. [serious] Roma precisava de alguém que segurasse o império antes que ele rachasse.",
  "coins_melt|A Roman mint worker pouring cheap metal into a melting pot of silver coins, coins turning grey",
  "coins_compare|Close view of a shiny silver Roman coin next to a dull grey copper coin of the same size, symbolic" + SEMTXT,
  "empire_crack|A big red map-like marble disk with deep cracks running across it, symbolic" + SEMTXT)

# ───────────────────────── 9. DIVIDIR ─────────────────────────
cap("9. Dividir para não cair")
b("Uma horta na costa da Croácia, ano trezentos e oito. Um velho imperador aposentado cuida dos repolhos. Vêm pedir que ele volte ao poder, e ele responde: se vocês vissem os repolhos que eu planto, não pediriam isso.",
  f"diocletian_garden|{DIOC}, proudly holding a huge cabbage in a vegetable garden by a big palace on the sea coast",
  "envoys_garden|Two round-white-head cartoon Roman officials in rich clothes standing awkwardly in a vegetable garden, an old man showing them cabbages, comic",
  card="308 d.C.")
b("O jardineiro é Diocleciano. No poder, ele tinha dividido o império entre quatro governantes, cada um perto de uma fronteira. E tabelou o preço de mais de mil produtos, do sapato ao frango.",
  "tetrarchs|Four round-white-head cartoon Roman emperors in purple embracing each other in a group hug, a famous statue pose, comic",
  "price_list|A huge stone tablet with long columns of tiny marks in a market, merchants staring at it in shock, sandals and chickens on the stalls" + SEMTXT)
b("Não funcionou, porque os produtos sumiram do mercado. Se você ou os seus pais viveram os anos oitenta no Brasil, já viram esse filme.",
  "empty_market|An ancient Roman market with empty stalls and a confused round-white-head cartoon customer with a basket",
  "eighties_market|A 1980s Brazilian supermarket with empty shelves and a price tag man, round-white-head cartoon shoppers, comic" + SEMTXT)
b("§ Depois dele, os quatro brigam, e Constantino ganha. Na véspera da batalha decisiva, em trezentos e doze, ele diz ter visto um sinal no céu e manda pintar o símbolo de Cristo nos escudos. Vence. E o império que perseguia cristãos passa a protegê-los.",
  f"constantine_sign|{CONST}, looking up at a glowing cross of light in the sky above his army camp at sunset@@CONSTANTINO",
  "shields_paint|Roman soldiers painting a simple Chi-Rho Christian symbol on their round shields in a camp",
  "milvian|A battle at a stone bridge over a river with soldiers falling into the water" + SEMBAND,
  card="312 d.C.")
b("E muda o centro do império para o leste, numa cidade nova com o nome dele: Constantinopla. Faz sentido, porque o dinheiro estava no Oriente. Só que isso deixa o Ocidente mais pobre, mais exposto… e cada vez mais dependente de soldados bárbaros.",
  "constantinople|The new city of Constantinople on the Bosphorus strait with domes, walls and ships, golden sunlight",
  "map_split|Map of the Roman Empire around the Mediterranean, the western half painted pale orange and the eastern half painted deep red, " + MAPA,
  "barbarian_soldiers|Germanic warriors with long hair and fur cloaks putting on Roman helmets and receiving pay from a Roman officer" + SEMBAND,
  card="330 d.C.")

# ───────────────────────── 10. A BALANÇA VIRA ─────────────────────────
cap("10. A balança vira")
b("Margem do rio Danúbio, trezentos e setenta e seis. Milhares de godos, fugindo dos hunos, imploram para entrar no império. Roma deixa… e depois explora tanto os refugiados que eles se revoltam. Em dois anos, matam o próprio imperador em batalha.",
  "danube_goths|Thousands of Gothic families with carts and children waiting on the bank of a wide river, Roman soldiers on the other side, cold grey sky",
  "goths_cross|Gothic families crossing a wide river on boats and rafts, crowded and desperate",
  "adrianople|A battle on a hot plain where Gothic cavalry overwhelms a Roman army" + SEMBAND,
  card="376 d.C.")
b("Quatrocentos e oito. Imagine Roma cercada pelo rei godo Alarico. Então Roma faz o que tinha feito com Breno: paga resgate. Cinco mil libras de ouro, cinco vezes o de Breno… e três mil libras de pimenta.",
  f"alaric_walls|{ALARICO}, on horseback in front of the high walls of Rome with his army camped around" + SEMBAND + "@@ALARICO",
  "ransom_again|Roman senators carrying chests of gold out of the gates of Rome to a waiting Gothic army, the bronze balance scale again",
  "pepper_sacks|A huge pile of sacks overflowing with black pepper next to gold chests, a Gothic warrior sneezing, comic",
  card="408 d.C.")
b("Não adianta. Em vinte e quatro de agosto de quatrocentos e dez, os godos entram e saqueiam a cidade por três dias. É a primeira vez em oitocentos anos. Lá em Belém, São Jerônimo escreve: [serious] foi tomada a cidade que tinha tomado o mundo inteiro.",
  "sack_410|Gothic warriors pouring into the city of Rome through a gate at night, temples and statues behind" + SEMBAND,
  "jerome|An old round-white-head cartoon monk with a simple flat long white beard shape writing by candlelight in a cave study, a lion sleeping beside him, sad",
  card="410 d.C.")
b("§ Lembra da pergunta do começo? Aqui está a terceira peça. Roma fazia dos vencidos romanos. Os godos entraram como um povo à parte, com rei próprio, pagos para lutar. [serious] E a cidade do ai dos vencidos agora era a vencida.",
  "piece_three|A third golden puzzle piece fitting into a puzzle of a burning Rome, symbolic" + SEMTXT,
  "goths_apart|A Gothic king and his warriors in their own camp next to a Roman city, separate, under their own banners, paid with chests of coins" + SEMBAND)
b("O fim chega quase sem barulho. Em quatrocentos e setenta e seis, o general bárbaro Odoacro tira do trono um menino, Rômulo Augústulo, com o nome do fundador e do primeiro imperador. Mas será que Roma acabou ali?",
  f"odoacer_boy|{ODOACRO}, gently taking the golden diadem off the head of {MENINO} on a throne in a palace in Ravenna@@ODOACRO",
  "insignia_box|Imperial purple robes and a golden diadem being packed into a wooden chest to be sent away by ship, symbolic",
  card="476 d.C.")

# ───────────────────────── FECHO (≤ 45 s) ─────────────────────────
cap("Fecho")
b("§ A metade oriental seguiu se chamando romana até mil quatrocentos e cinquenta e três. E a resposta da nossa pergunta: Roma virou dona do mundo fazendo dos vencidos romanos, e caiu quando não conseguiu mais.",
  "byzantium|The great golden-domed city of Constantinople with high walls by the sea, sunset, centuries later",
  "piece_final|A finished golden puzzle showing the whole story of Rome from a small village to a great empire, symbolic" + SEMTXT,
  card="1453")
b("Só que repare. A terra dos gauleses de Breno hoje fala francês, filho do latim. E você, que ouve isto em português, fala um latim que mudou. [warm] Ai dos vencidos? Os vencidos ficaram com Roma.",
  "gauls_today|A modern Paris street cafe with round-white-head cartoon French people chatting, a small Gaulish helmet on a shelf, sunny",
  "latin_words|A round-white-head cartoon Brazilian family at a breakfast table talking, small floating speech bubbles with laurel leaves, warm and funny" + SEMTXT,
  "sword_rest|The long iron sword resting on the bronze balance scale, now covered with flowers and vines, peaceful light, symbolic")
b("E para você: Roma acabou em quatrocentos e setenta e seis, em mil quatrocentos e cinquenta e três… ou ainda não acabou? Conta aí nos comentários.",
  f"guide_comment|{GUIA} sitting on a fallen Roman column in front of the Colosseum, holding a small balance scale, thinking",
  "colosseum_sunset|The Colosseum at sunset today with tourists and a scooter passing, warm light")

# Grafia para a VOZ (o Fish lê como português; nomes latinos em forma portuguesa quase não precisam). Conferir no teste de nomes (qa/pronuncia/).
# blocos.json leva "texto" (falado, vai ao Fish) e "tela" (grafia correta: legendas e SCRIPT).
FALA = [("Vercingetórix", "Vercinguetórix"), ("Áccio", "Ácio"), ("Augústulo", "Augústulo"), ("Caracala", "Caracala"),
        ("Rubicão", "Rubicão"), ("Tibre", "Tibre"), ("Odoacro", "Odoacro")]
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
