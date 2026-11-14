#!/usr/bin/env python3
"""Fonte única do 009-alemanha (13/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

4º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
Molde History in Minutes (narrativa contínua). Referência de código: videos/006-roma, 007-russia e 008-franca.
  hook: Versalhes, 18/01/1871: a Alemanha nasce no Salão dos Espelhos, no palácio do inimigo, com Paris cercada
  → Goethe e Schiller, 1796 (Xenien): "Alemanha? Mas onde fica? Eu não sei encontrar esse país."
  → PERGUNTA CENTRAL (≤ 0:50) → "Essa é a história inteira da Alemanha" → 1 "guarde" (o Salão dos Espelhos) → Teutoburgo (era 1)
  → 10 eras, cada uma: problema herdado → cena no presente → ≤ 3 fatos → solução → novo problema
  → fecho ≤ 45 s: responde, reenquadra e pergunta para os comentários.
Fio condutor: A PERGUNTA DE GOETHE ("onde fica a Alemanha?") e O SALÃO DOS ESPELHOS (1871 nasce ali; 1919 a paz é assinada ali).
  A resposta montada em 3 peças: a língua une, o poder (e a fé) divide (peça 1, era 3); o país não nasceu de uma votação, nasceu de
  três guerras, por isso na casa do inimigo, e fronteira feita na guerra é fronteira provisória (peça 2, era 6); feito pela guerra,
  desfeito pela guerra: 40 anos em que "onde fica" dependia do lado do muro (peça 3, era 10). Fecho: 1990, sem um tiro e com uma assinatura,
  pela primeira vez fronteiras que nenhum vizinho contesta.
Pergunta volta: era 3 (1ª peça), era 6 (2ª peça), era 8 ("lembra da nossa pergunta?"), era 10 (3ª peça), fecho (resposta).
Seriedade: 1933–45 é UMA era (9), sem humor, sem imagem gráfica, sem símbolo nazista em imagem nenhuma (só silhuetas, multidões sem bandeira,
  trilhos, malas, velas). Fecha em 1990 + 1 frase neutra (memoriais/economia); nada de política atual.

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1871") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006–008).
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (006–008: ~128 ppm com pausas)
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
TITULO = "A história INTEIRA da Alemanha"
PERGUNTA = "Por que um povo com a mesma língua levou mil anos para virar um país, e por que, mesmo depois disso, ninguém sabia dizer onde a Alemanha começava e terminava?"

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
SEMMOD = ", no modern objects, no modern flags"          # 005/007: o nano-banana põe bandeira atual em cena de época
SANG = ", no blood, no gore"
# 1933–45 e política de anúncios: nenhum símbolo em imagem nenhuma
SEMSIMB = (", absolutely no symbols of any kind, no swastikas, no armbands, no insignia, no flags, no banners, no eagles, "
           "no emblems, no letters, no blood, no violence shown")
# Personagens (regra da bíblia: nada de rosto descrito; "round-white-head cartoon …")
GERM = "round-white-head cartoon Germanic tribal warriors of the 1st century with long hair, simple flat beard shapes, bare chests or simple fur cloaks, long spears and tall wooden shields"
LEG = "round-white-head cartoon Roman legionaries in red tunics, segmented iron armor, iron helmets and curved red rectangular shields"
ARMIN = "a round-white-head cartoon young Germanic chief with long blond hair, a simple flat short beard shape, a Roman-style bronze breastplate over a fur cloak and a long spear"
VARO = "a round-white-head cartoon middle-aged Roman governor, beardless, in a bronze cuirass with a red general's cloak and a plumed helmet"
AUGUSTO = "a round-white-head cartoon old Roman emperor, beardless, with short hair and a laurel wreath, in a white and purple toga"
CMAGNO = "a round-white-head cartoon old emperor with a simple flat long white beard shape, a heavy golden crown with a cross and a blue and gold robe"
OTAO = "a round-white-head cartoon medieval German king of the 10th century with a simple flat long red beard shape, an octagonal golden crown with a cross and a red cloak"
HENR4 = "a round-white-head cartoon young medieval emperor of the 11th century with a simple flat short dark beard shape, barefoot, wearing a plain grey wool penitent's robe, no crown"
PAPA = "a round-white-head cartoon medieval Pope with a simple flat white beard shape, a tall white papal hat and white and gold robes"
ELEITORES = "round-white-head cartoon medieval German prince-electors: three archbishops in red robes and mitres and four princes in red ermine-trimmed cloaks and fur caps"
GUTEN = "a round-white-head cartoon German craftsman of 1450 with a simple flat long brown beard shape, a fur-trimmed cap and a leather apron"
LUTERO = "a round-white-head cartoon German monk of 1517, beardless, chubby, with the round tonsure haircut and a black monk's habit"
TETZEL = "a round-white-head cartoon fat medieval preacher in a white and black Dominican habit standing next to a big iron money chest"
PRINCIPES = "round-white-head cartoon German princes of the 16th century in fur coats, feathered flat caps and gold chains"
MERC = "round-white-head cartoon mercenary soldiers of the 1630s with wide-brimmed feathered hats, breastplates, long pikes and muskets"
CAMP = "round-white-head cartoon German peasants of the 17th century in simple brown clothes, women with white headscarves"
FG1 = "a round-white-head cartoon grumpy stout Prussian king of 1730 with a short white wig, a plain blue military coat and a walking stick"
GIGANTES = "very tall round-white-head cartoon Prussian grenadiers of 1730 in blue coats with tall pointed brass-fronted mitre caps"
FRED = "a round-white-head cartoon thin Prussian king of the 1750s with a grey wig, a black tricorne hat, a plain blue military coat and a walking cane"
NAPO = "a round-white-head cartoon short French emperor of 1806 with straight dark hair, a black bicorne hat worn sideways and a grey overcoat over a green uniform"
GRIMM = "two round-white-head cartoon German brothers of 1810, scholars with dark curly hair, beardless, in dark frock coats and high white collars"
FW4 = "a round-white-head cartoon bald, chubby Prussian king of 1849, beardless, in a dark blue Prussian general's uniform with gold epaulettes"
DEPUT = "round-white-head cartoon German members of parliament of 1848, professors and lawyers with spectacles, frock coats and big sideburns"
BISM = "a round-white-head cartoon tall bald Prussian statesman of the 1860s with a simple flat bushy grey mustache shape, a dark blue uniform coat and a spiked helmet under his arm"
WILH1 = "a round-white-head cartoon old Prussian king with big simple flat white side whiskers and mustache shapes, a dark blue uniform, a red sash and medals"
PRUS = "round-white-head cartoon Prussian and German officers of 1871 in dark blue uniforms with plain spiked leather helmets with smooth fronts (no badge, no emblem, no eagle) and swords"
WILH2 = "a round-white-head cartoon young German emperor of 1890 with a simple flat upturned waxed mustache shape, a white uniform with a breastplate and a shiny spiked helmet with a plain top, no emblems"
TROPAS = "round-white-head cartoon German soldiers of 1916 in grey uniforms and round steel helmets"
WEIM = "round-white-head cartoon Berliners of the 1920s, men in flat caps and coats, women in cloche hats and short coats"
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes"

# ───────────────────────── HOOK (Versalhes, 18/01/1871) ─────────────────────────
cap("Hook")
b("[serious] Versalhes, dezoito de janeiro de mil oitocentos e setenta e um. Imagine você no palácio dos reis da França, no Salão dos Espelhos. Lá fora, Paris está cercada e com fome.",
  "versailles_winter|The palace of Versailles in winter 1871 under a grey sky, snow on the gardens, Prussian soldiers in dark blue coats and spiked helmets guarding the gates, smoke on the horizon" + SEMBAND,
  "hall_mirrors_empty|The Hall of Mirrors of Versailles: a very long golden gallery with huge chandeliers, tall arched mirrors and painted ceiling, cold winter light, empty",
  "paris_siege|Paris under siege in the winter of 1870, snowy streets, round-white-head cartoon Parisians in coats queuing in front of an empty butcher shop, cannons on the walls in the distance" + SEMTXT,
  "paris_hungry|Round-white-head cartoon hungry Parisian family of 1870 sharing a tiny piece of bread by a cold fireplace, worried faces, winter",
  "siege_cannon|Prussian siege cannons on a snowy hill aiming at the distant city of Paris in winter 1870, soldiers in dark coats warming their hands by a fire" + SEMBAND,
  card="1871")
b("Lá dentro, centenas de oficiais alemães erguem as espadas e gritam viva para um rei da Prússia, que acaba de virar imperador. [curious] De um país que nasce ali mesmo, na casa do inimigo.",
  f"proclamation|The Hall of Mirrors of Versailles packed with {PRUS} raising their swords and cheering toward a small stage where {WILH1} stands" + SEMBAND,
  "swords_raised|Close view of dozens of raised swords and spiked helmets in a golden hall full of mirrors and chandeliers, dramatic light" + SEMBAND,
  f"kaiser_stage|{WILH1}, standing on a small red stage in the Hall of Mirrors of Versailles while princes in uniforms bow" + SEMBAND + "@@GUILHERME I",
  "mirror_reflection|A tall golden mirror in Versailles reflecting a crowd of cheering officers in spiked helmets, symbolic" + SEMBAND,
  "french_rooms|A round-white-head cartoon old French palace servant peeking from behind a golden door at the cheering German officers with a horrified face, comic" + SEMBAND,
  "pickelhaube_close|Close view of a black leather spiked helmet with a shiny brass spike resting on a golden chair in a palace hall, symbolic" + SEMBAND)
b("Setenta e cinco anos antes, dois dos maiores poetas da língua alemã, Goethe e Schiller, tinham escrito: Alemanha? Mas onde fica? Eu não sei encontrar esse país.",
  "goethe_schiller|Two round-white-head cartoon German poets of 1796 in frock coats and powdered hair, one tall and thin, one older and stout, sitting at a desk with quills, looking puzzled at a big blank map" + SEMTXT + "@@GOETHE E SCHILLER",
  "poets_search|Two round-white-head cartoon poets of 1796 in frock coats searching with a magnifying glass over a blank map of central Europe, scratching their heads, comic" + SEMTXT,
  "map_patchwork_hook|Map of central Europe in 1790 covered by a dense patchwork of hundreds of tiny territories in many different colors, " + MAPA,
  "quill_paper|Close view of a quill pen and an inkwell on a wooden desk by candlelight, a sheet of paper with only a small drawing of a question mark" + SEMTXT,
  "weimar_town|A small German town of 1796 with a ducal palace, cobblestone streets and half-timbered houses, round-white-head cartoon people in 18th century clothes walking, autumn" + SEMTXT)
b("§ [serious] Então, a pergunta: por que um povo com a mesma língua levou mil anos para virar um país, e por que, mesmo depois disso, ninguém sabia dizer onde a Alemanha começava e terminava?",
  "map_borders_moving|Symbolic scene: a map of central Europe where the borders of one country are drawn several times in different colors, like lines that keep moving, " + MAPA,
  "hands_map|Several round-white-head cartoon hands of kings, generals and diplomats from different centuries pulling the same parchment map in different directions, comic" + SEMTXT,
  "forest_rhine|A dark ancient forest by a wide river at dawn, mist between the trees, symbolic",
  "berlin_wall_hook|A grey concrete wall with barbed wire crossing a city street in the 1960s, a watchtower, cold light, no people" + SEMTXT,
  "brandenburg_gate|The Brandenburg Gate in Berlin with its columns and the four-horse chariot on top, seen at dawn, peaceful, no people" + SEMTXT,
  "question_map|A round-white-head cartoon little narrator character with dot eyes standing on a big blank map of Europe and holding a huge question mark, comic" + SEMTXT)
b("Essa é a história inteira da Alemanha. Guarde esse salão de espelhos: ele volta. E tudo começa numa floresta onde Roma perdeu um exército inteiro.",
  "map_germany_hook|Map of today's Germany between the North Sea, the Baltic Sea, the Alps and the Rhine, painted soft green, the neighbors pale beige, " + MAPA,
  "mirror_hall_kept|A single tall golden mirror of Versailles with a beam of light on it in an empty hall, symbolic",
  "teutoburg_dark|A very dark and wet ancient forest with huge trees, mud and fallen trunks, heavy rain, a narrow path disappearing into the shadows",
  "rome_shocked|A round-white-head cartoon Roman senator in a toga dropping a scroll in shock in a marble hall, comic" + SEMTXT,
  "forest_edge|The edge of a huge dark forest seen from a sunny Roman field, legionaries looking at it nervously, the trees like a wall" + SEMBAND)

# ───────────────────────── 1. A FLORESTA ─────────────────────────
cap("1. A floresta que Roma não engoliu")
b("Ano nove. Olhe para essa floresta a leste do Reno: escura, encharcada, sem estrada. Três legiões romanas marcham por ela em fila comprida, debaixo de chuva. Imagine o barro até o joelho.",
  f"legions_forest|A long column of {LEG} marching through a dark muddy forest in heavy rain, wagons stuck in the mud" + SEMBAND,
  "map_rhine_9|Map of Western Europe in the year 9 with the Roman Empire painted red up to the Rhine river and the dark green forests of Germania east of the Rhine, " + MAPA,
  "mud_knees|Close view of Roman soldiers' legs and sandals sunk up to the knees in deep mud on a forest path, rain, comic but tense" + SEMBAND,
  f"varus_horse|{VARO} riding a horse in the rain in a forest, looking annoyed at the mud" + "@@VARO",
  "wagons_mud|Roman supply wagons and mules stuck in deep mud between huge trees, soldiers pushing and slipping, rain, comic" + SEMBAND,
  "rain_helmet|Close view of a Roman legionary with a dripping wet iron helmet looking up at the rain with a miserable face, comic" + SEMBAND,
  card="9 d.C.")
b("Quem guia é Armínio, um chefe germânico que cresceu entre os romanos e serviu no exército deles. Só que ele leva os romanos direto para uma armadilha. Em poucos dias, as três legiões somem.",
  f"arminius|{ARMIN} riding next to Roman officers in a forest, smiling politely while secretly signaling to someone hidden in the trees" + "@@ARMÍNIO",
  f"ambush|{GERM} jumping out of the trees and from behind earth walls to attack a stretched column of Roman soldiers in a rainy forest" + SEMBAND + SANG,
  "eagle_lost|A golden Roman legion eagle standard lying in the mud among fallen leaves in a dark forest, rain, symbolic" + SEMTXT,
  "germanic_hidden|Round-white-head cartoon Germanic warriors hiding behind huge trees and bushes in a dark forest, waiting silently with spears" + SEMBAND,
  "earth_wall|A long low wall of earth and turf hidden at the edge of a forest by a swampy path, warriors crouching behind it, rain" + SEMBAND,
  "legions_vanish|An empty muddy forest path after a battle with broken spears and abandoned Roman shields among the trees, mist, no bodies" + SEMBAND + SANG)
b("[curious] Conta-se que o imperador Augusto, em Roma, batia a cabeça na porta e gritava: Varo, devolva as minhas legiões!",
  f"augustus_door|{AUGUSTO} banging his head against a big wooden palace door in despair, servants looking worried, comic" + "@@AUGUSTO",
  f"augustus_shout|{AUGUSTO} shouting with raised arms in a marble palace hall, comic, dramatic",
  "rome_palace|The Palatine Hill in Rome with marble palaces and temples at dusk, a single lit window, symbolic",
  "messenger_rome|A round-white-head cartoon exhausted Roman messenger kneeling before an old emperor in a marble hall, delivering bad news, servants gasping, comic")
b("§ Roma desiste da floresta, e o Reno vira fronteira. Repare: Colônia, Mainz e Tréveris nasceram romanas, do lado de cá. [curious] Colônia vem de colônia romana. A água-de-colônia que você já passou é de lá.",
  "roman_frontier|A Roman stone fort with watchtowers on the bank of the wide Rhine river, legionaries on the walls looking at the dark forest on the other side" + SEMBAND,
  "roman_cologne|The Roman city of Cologne on the Rhine in the 2nd century with stone walls, a temple, a harbor and boats, sunny",
  "cologne_bottle|Close view of an elegant old glass bottle of eau de cologne with a plain label without writing on a marble table, a round-white-head cartoon hand spraying it, comic" + SEMTXT,
  "trier_gate|A big dark Roman stone city gate with two towers and arches, the Porta Nigra of Trier, in Roman times, people passing",
  "rhine_two_banks|The wide Rhine river seen from above: on the west bank a Roman town with red roofs and vineyards, on the east bank a dark wild forest, symbolic",
  "roman_wine|Round-white-head cartoon Romans and local people pressing grapes in a vineyard on the Rhine hills, sunny, cheerful")
b("Mas aqueles povos nunca foram um povo só: queruscos, suevos, saxões, francos, cada um com o seu chefe. Então, quando Roma enfraquece, no século cinco, eles atravessam o Reno e repartem o império.",
  f"tribes_argue|Several {GERM} chiefs from different tribes arguing around a fire in a forest clearing, pointing at each other, comic" + SEMBAND,
  "tribes_shields|Round-white-head cartoon Germanic warriors of several different tribes with differently painted shields standing in separate groups, eyeing each other suspiciously" + SEMBAND,
  "rhine_crossing|Columns of round-white-head cartoon Germanic warriors and families with wagons crossing a wide frozen river into a Roman province, an abandoned Roman fort on the bank" + SEMBAND,
  "goths_rome|Round-white-head cartoon Germanic warriors with long hair walking through the streets of a Roman city with temples, Roman citizens hiding, comic" + SEMBAND,
  "franks_rise|Round-white-head cartoon Frankish warriors with long hair raising small axes on a hill above a river valley, sunrise" + SEMBAND,
  card="séc. V")
b("Um rei franco, Carlos Magno, junta quase tudo de novo no ano oitocentos. Só que os netos dele repartem o império em três. E repare: a fatia do leste ia levar mil anos para virar um país.",
  f"charlemagne|{CMAGNO} sitting on a stone throne in a palace chapel with an octagonal dome, nobles around him" + "@@CARLOS MAGNO",
  "map_verdun|Map of Western Europe split into three long vertical bands: a blue band in the west, a yellow band in the middle and a green band in the east, " + MAPA,
  "three_grandsons|Three round-white-head cartoon young medieval kings sitting at a long table cutting a big parchment map into three pieces with scissors, eyeing each other, comic" + SEMTXT,
  "charlemagne_crown_rome|An old emperor with a simple flat long white beard shape kneeling before the Pope in an old basilica on Christmas night, being crowned, candles",
  "east_slice|Symbolic scene: a green slice of a parchment map with forests, rivers and small castles floating alone, a long road disappearing into the distance toward a far horizon" + SEMTXT,
  card="843")

# ───────────────────────── 2. O IMPÉRIO DE PEDAÇOS ─────────────────────────
cap("2. Um imperador descalço na neve")
b("Canossa, janeiro de mil e setenta e sete. Diante de um castelo nas montanhas, um homem espera na neve, descalço, com roupa de penitente. É o imperador, Henrique Quarto. E o papa, lá dentro, o faz esperar três dias.",
  "canossa_castle|A medieval stone castle on a rocky snowy mountain in northern Italy in January, a cold blue sky, a few footprints in the snow at the gate",
  f"henry_snow|{HENR4} standing in the snow in front of a closed castle gate, shivering, with folded hands, comic but sad" + "@@HENRIQUE IV",
  "bare_feet_snow|Close view of bare cold feet standing in deep snow in front of a heavy wooden castle gate, symbolic, comic",
  f"pope_window|{PAPA} looking out of a castle window with his arms crossed and a stern face, snowy mountains behind" + "@@PAPA GREGÓRIO VII",
  "canossa_monks|Round-white-head cartoon medieval monks peeking curiously over a snowy castle wall at a barefoot man waiting at the gate, comic",
  "canossa_wait|A barefoot round-white-head cartoon medieval emperor in a grey wool robe sitting on a stone in the snow at night under the stars, a closed gate behind him, sad and comic",
  card="1077")
b("Como um imperador chegou a isso? Desde Otão, o Grande, coroado em novecentos e sessenta e dois, os reis alemães também eram coroados imperadores. Só que brigavam com o papa, e o papa podia expulsar o imperador da Igreja. Aí os príncipes aproveitavam para se rebelar.",
  f"otto_crowned|{OTAO} kneeling before the Pope in an old basilica in Rome, being crowned emperor, candles and nobles" + "@@OTÃO, O GRANDE",
  "pope_emperor_tug|A round-white-head cartoon medieval Pope and a round-white-head cartoon medieval emperor pulling the same golden crown in opposite directions, comic" + SEMTXT,
  "princes_whisper|Round-white-head cartoon medieval German princes in fur cloaks whispering and smiling slyly behind a column while an emperor walks away, comic",
  card="962")
b("§ Pior: o imperador não herdava a coroa. Era eleito pelos grandes príncipes e, a partir de mil trezentos e cinquenta e seis, por sete eleitores. Imagine um chefe escolhido pelos próprios subordinados. Quem você acha que mandava?",
  f"electors|{ELEITORES} sitting in a semicircle in a medieval hall, voting by raising their hands, an emperor-candidate waiting nervously" + "@@OS SETE ELEITORES",
  "golden_bull|A big completely blank medieval parchment sheet (no writing at all) with a heavy golden seal hanging from it on a red velvet table, candles" + SEMTXT,
  card="1356")
b("[curious] Era o Sacro Império Romano-Germânico. Séculos depois, Voltaire debochou: não era nem sacro, nem romano, nem império. Eram mais de trezentos pedaços, cada um com o seu senhor.",
  "map_hre|Map of central Europe in the 16th century covered by a dense patchwork of more than three hundred small territories in many different colors, " + MAPA,
  "voltaire_laugh|A round-white-head cartoon thin French philosopher of the 1750s in a long grey wig laughing while writing at a desk, comic" + SEMTXT + "@@VOLTAIRE",
  "tiny_castles|Many tiny castles, walled towns and church towers on green hills close to each other, each with a different colored roof, like a crowded toy landscape" + SEMBAND,
  "little_lords|A comic line of round-white-head cartoon little German lords, bishops and city mayors, each standing proudly in front of his own tiny castle" + SEMBAND)
b("Um império com coroa, mas sem centro. O problema é que uma ideia ia correr por esses pedaços mais rápido que qualquer exército.",
  "crown_no_center|Symbolic scene: a golden imperial crown floating over a map broken into hundreds of small pieces, warm light" + SEMTXT,
  "sparks_press|Close view of a wooden printing press in a dark workshop with a beam of light, symbolic, no flags anywhere" + SEMTXT)

# ───────────────────────── 3. A PRENSA E O MONGE ─────────────────────────
cap("3. Uma língua para todos e uma fé partida")
b("Wittenberg, mil quinhentos e dezessete. Um monge, Martinho Lutero, está furioso: um pregador vende indulgências na região. Pague, e a alma do seu parente sai do purgatório mais cedo.",
  "wittenberg|A small German university town of 1517 with a castle church with a tall round tower, half-timbered houses and a market square, autumn, the church door is plain wood with no posters, no writing, no signs anywhere",
  f"luther_angry|{LUTERO}, sitting at a desk in a monastery cell, frowning and writing furiously by candlelight" + SEMTXT + "@@MARTINHO LUTERO",
  f"tetzel|{TETZEL} preaching in a town square to worried round-white-head cartoon peasants dropping coins into the chest, comic" + SEMTXT,
  "coins_chest|Close view of coins falling into a big iron money chest with a heavy lock, warm light" + SEMTXT,
  card="1517")
b("[curious] O slogan, segundo os críticos: quando a moeda cai no cofre, a alma sai do purgatório. Então Lutero escreve noventa e cinco teses contra isso e, diz a tradição, prega na porta de uma igreja.",
  "soul_jump|A comic symbolic scene: a tiny happy cartoon soul with wings jumping out of a cloud of smoke when a coin falls into a chest" + SEMTXT,
  f"luther_door|{LUTERO} nailing a big completely blank sheet of paper (no writing at all) to a heavy wooden church door with a hammer, townspeople watching curious" + SEMTXT,
  "door_paper|Close view of a big sheet of paper nailed to an old wooden church door, a hammer hanging next to it, only tiny unreadable lines on the paper" + SEMTXT)
b("Só que, setenta anos antes, em Mainz, Gutenberg tinha montado a prensa de tipos móveis. Então as teses correm o império em poucas semanas. Pense nisso como o primeiro texto que viralizou.",
  f"gutenberg|{GUTEN} pulling the big wooden lever of a printing press in a workshop full of paper sheets, proud" + SEMTXT + "@@GUTENBERG",
  "metal_type|Close view of small metal letter blocks arranged in a wooden frame, ink roller, on a workbench, no readable words" + SEMTXT,
  "pamphlets_fly|Hundreds of printed pamphlets flying over German towns, castles and rivers like a flock of birds, comic, symbolic" + SEMTXT,
  "phone_scroll|A round-white-head cartoon modern young man scrolling on a smartphone on a bus, and next to him a cartoon man of 1517 reading a pamphlet with the same face, comic" + SEMTXT,
  card="c. 1450")
b("§ Escondido num castelo, Lutero traduz o Novo Testamento para o alemão em umas onze semanas, com palavras que se entendiam do norte ao sul. Imagine o Brasil sem um português escrito comum. Era quase assim antes dele.",
  "wartburg|A medieval castle on top of a forested hill in central Germany, autumn colors, morning mist",
  "luther_translates|A round-white-head cartoon chubby German man of 1521 with short hair and a simple flat short dark beard shape, disguised as a knight in a plain brown doublet, translating a big book at a wooden desk in a castle room by a window" + SEMTXT,
  "german_bible|Close view of an open old printed book with a woodcut picture, the rest of the pages blank, on a wooden table next to a candle" + SEMTXT,
  "dialects|Round-white-head cartoon German peasants from the north and from the south talking and not understanding each other, then both reading the same book and smiling, comic" + SEMTXT,
  card="1522")
b("E aqui está a primeira peça da resposta. A Alemanha ganha uma língua escrita comum, mas a fé se parte ao meio: metade dos príncipes vira protestante, metade fica católica.",
  "piece_one|A big golden puzzle piece being placed into a puzzle that shows an open book in the middle of a map of central Europe, symbolic" + SEMTXT,
  f"princes_split|Two groups of {PRINCIPES} on opposite sides of a hall, one holding open books, the other holding rosaries, glaring at each other" + SEMTXT,
  "church_split|Symbolic scene: a medieval church split down the middle by a crack, one half with plain white walls and the other half with golden altars" + SEMTXT)
b("Em mil quinhentos e cinquenta e cinco, a regra vira: cada príncipe escolhe a religião do seu território. A língua une. Mas o poder, e agora a fé, dividem. E uma casa dividida assim só precisava de uma faísca.",
  "prince_decides|A round-white-head cartoon German prince of 1555 pointing at a church while his subjects line up behind him obediently, comic" + SEMTXT,
  "map_religion|Map of central Europe in 1555 with many small territories colored either light purple or orange in a confusing patchwork, " + MAPA,
  card="1555")

# ───────────────────────── 4. TRINTA ANOS ─────────────────────────
cap("4. Trinta anos de inferno")
b("Praga, maio de mil seiscentos e dezoito. Nobres protestantes invadem o castelo e jogam três funcionários do imperador católico pela janela. [curious] Os três sobrevivem. Os católicos dizem que foi um anjo. Os protestantes, que foi um monte de esterco.",
  "prague_castle|Prague Castle on its hill above the city with red roofs and the gothic cathedral towers, spring 1618",
  "defenestration|Angry round-white-head cartoon Bohemian nobles of 1618 in black clothes throwing three officials in fancy coats out of a tall castle window, comic" + SEMTXT,
  "dung_landing|A comic scene: three round-white-head cartoon officials in fancy 1618 coats sitting dazed in a big pile of hay and dung under a tall castle wall, alive",
  card="1618")
b("Começa a Guerra dos Trinta Anos. E o que era briga de religião vira briga de reis: Suécia, Dinamarca, Espanha, e até a França católica do lado dos protestantes. [curious] A religião, já dava para ver, era desculpa.",
  "kings_table|Round-white-head cartoon kings of Sweden, Spain, Denmark and France of the 1630s sitting around a big map of the German lands and placing small soldier figures on it, comic" + SEMTXT,
  f"swedish_army|{MERC} marching into a German valley with cannons, a burning village in the distance" + SEMBAND,
  "cardinal_sly|A round-white-head cartoon French cardinal of 1635 in red robes secretly handing a bag of gold coins to a Protestant king under the table, comic" + SEMTXT)
b("Imagine a sua cidade saqueada, ocupada e saqueada de novo, por exércitos que nem falam a sua língua. Em algumas regiões, mais da metade da população morre. No total, algo entre um quinto e um terço.",
  f"village_looted|{MERC} carrying chickens, barrels and furniture out of a German village while {CAMP} hide in the woods, smoke" + SEMBAND + SANG,
  "empty_village|An abandoned German village of the 1630s with broken roofs, empty fields full of weeds and a lonely church, grey sky, crows",
  f"refugees|{CAMP} walking on a muddy road with carts and children, leaving a burned village behind, sad" + SEMBAND,
  "plague_cart|A medieval German town street with closed doors, a doctor with a long beak mask walking alone, gloomy, no corpses" + SEMTXT)
b("§ Na Paz de Vestfália, em mil seiscentos e quarenta e oito, cada um dos cerca de trezentos príncipes ganha quase a independência. Repare: o império continua, mas só no papel.",
  "westphalia|Round-white-head cartoon diplomats of 1648 in black clothes and big lace collars signing a long treaty around a table in a wooden town hall, exhausted faces" + SEMTXT,
  "map_1648|Map of central Europe in 1648 broken into hundreds of tiny colored pieces like a shattered mosaic, " + MAPA,
  card="1648")
b("Só que território fraco no meio da Europa vira estrada para o exército dos outros. Alguém ia ter que virar muralha.",
  "map_crossroads|Map of Europe with arrows of many colors from all directions crossing a weak patchwork in the center, " + MAPA.replace("no symbols, ", ""),
  "sandy_plain|A flat sandy plain with pine forests and small lakes in northeastern Germany, grey sky, no mountains, a lonely watchtower")

# ───────────────────────── 5. A PRÚSSIA ─────────────────────────
cap("5. Um exército que tinha um país")
b("Potsdam, por volta de mil setecentos e trinta. Um rei rabugento passa em revista o seu regimento preferido: só gigantes, alguns com mais de dois metros, comprados ou sequestrados pela Europa.",
  f"giants_review|{FG1} inspecting a line of {GIGANTES} who are twice his size, in a palace courtyard, comic" + SEMBAND + "@@FREDERICO GUILHERME I",
  "giant_kidnap|A comic scene: Prussian recruiters of 1730 lifting a very tall surprised round-white-head cartoon farmer into a carriage at night",
  "potsdam_square|A parade ground in Potsdam in 1730 with neat lines of blue-coated soldiers drilling and a small palace behind, sunny" + SEMBAND,
  card="c. 1730")
b("[curious] Era o único luxo daquele rei pão-duro. A Prússia era areia, frio e nenhuma montanha para se esconder. Então virou quartel. Uma frase da época resume: a Prússia não é um país com um exército. É um exército com um país.",
  "stingy_king|A round-white-head cartoon grumpy Prussian king in a plain blue coat counting tiny coins at a bare table, a candle, comic" + SEMTXT,
  "map_prussia|Map of northern Europe in 1740 with a small scattered blue territory stretched across the flat north from the Rhine to the Baltic Sea, " + MAPA,
  "barracks_state|A comic symbolic scene: a whole small country drawn as a huge military barracks with a little town hidden inside its courtyard" + SEMTXT)
b("O filho dele, Frederico, o Grande, tocava flauta e enfrentava, sem perder o reino, vizinhos muito maiores. E mandou plantar batata por decreto. Da próxima vez que você comer salada de batata, agradeça a ele.",
  f"frederick_flute|{FRED}, playing the flute in an elegant rococo music room with candles, musicians around him" + SEMTXT + "@@FREDERICO, O GRANDE",
  f"frederick_battle|{FRED} on a horse on a hill commanding blue-coated Prussian soldiers in a big battle on a plain" + SEMBAND,
  "potato_order|Round-white-head cartoon Prussian peasants of the 1750s looking suspiciously at potatoes while an officer reads an order in a village, comic" + SEMTXT,
  "potato_salad|Close view of a bowl of German potato salad on a modern kitchen table, a round-white-head cartoon hand with a fork, comic" + SEMTXT,
  card="1756")
b("§ Então vem Napoleão. Em mil oitocentos e seis, sob a pressão dele, o Sacro Império acaba depois de oito séculos e meio. Meses depois, ele esmaga a Prússia em Jena e entra em Berlim.",
  f"napoleon_berlin|{NAPO} riding a white horse through the Brandenburg Gate in Berlin with French soldiers, round-white-head cartoon Berliners watching sadly" + SEMBAND + "@@NAPOLEÃO",
  "jena|A big battle on rolling hills in 1806 with French infantry in blue coats advancing through smoke and Prussian soldiers retreating" + SEMBAND,
  "crown_museum|A golden medieval imperial crown on a velvet cushion being put away into a dusty wooden box by a sad old servant, symbolic",
  card="1806")
b("Aí dois irmãos, os Grimm, saem recolhendo histórias do povo: Branca de Neve, Chapeuzinho Vermelho, João e Maria. Você cresceu com elas. Eles queriam provar que existia um povo alemão, mesmo sem país.",
  f"grimm_listen|{GRIMM} listening and taking notes while an old round-white-head cartoon village woman tells a story by the fireplace" + SEMTXT + "@@IRMÃOS GRIMM",
  "fairy_tales|A cartoon forest scene with a girl in a red hood, a wolf behind a tree, a gingerbread house and seven little dwarfs walking in a line, storybook style",
  "kid_book|A round-white-head cartoon modern child in pajamas reading a fairy tale book in bed with a flashlight, a red hood drawing on the cover" + SEMTXT)
b("Um povo, eles já tinham. Faltava fazer o país. E a dúvida era: de baixo para cima, com o povo, ou de cima para baixo, com um exército?",
  "two_roads|A road splitting into two paths in a German landscape: one leading to a parliament building, the other to a fortress with cannons, symbolic" + SEMTXT)

# ───────────────────────── 6. FERRO E SANGUE ─────────────────────────
cap("6. Ferro e sangue")
b("Frankfurt, mil oitocentos e quarenta e nove. Um parlamento eleito, cheio de professores, escreve a constituição de uma Alemanha unida e oferece a coroa ao rei da Prússia.",
  f"frankfurt_parliament|{DEPUT} debating in a big round church hall in Frankfurt, one of them giving a passionate speech" + SEMTXT,
  "paulskirche|A round red sandstone church in Frankfurt in 1848 with crowds of round-white-head cartoon citizens in top hats gathered outside, spring" + SEMBAND,
  f"crown_offer|A small delegation of {DEPUT} bowing and offering a paper crown on a cushion to {FW4} in a Berlin palace" + "@@FREDERICO GUILHERME IV",
  card="1849")
b("[curious] Ele recusa. Numa carta, chama aquilo de coroa vinda da sarjeta: rei de verdade só aceitava coroa de Deus e de outros príncipes. Repare na diferença: os professores tinham os votos. Mas quem tinha os canhões era a Prússia.",
  f"king_refuses|{FW4}, turning his head away with his nose up and pushing back a crown on a cushion, the professors shocked, comic",
  "gutter_crown|A comic symbolic scene: a small paper crown lying in a muddy street gutter, a royal shoe stepping over it" + SEMTXT,
  "votes_cannons|A comic symbolic scene: on a scale, a pile of paper ballots on one side and a heavy black cannon on the other side, the cannon side much lower" + SEMTXT)
b("§ Treze anos depois, o novo chefe do governo prussiano, Otto von Bismarck, diz aos deputados: as grandes questões não se decidem com discursos e votações, mas com ferro e sangue.",
  f"bismarck_speech|{BISM}, speaking firmly to a committee of round-white-head cartoon deputies at a long table, some of them shocked" + SEMTXT + "@@OTTO VON BISMARCK",
  "iron_blood|Close view of an iron cannonball and a sword on a dark wooden table under a lamp, dramatic, symbolic" + SEMTXT + SANG,
  card="1862")
b("E ele cumpre: três guerras curtas. Contra a Dinamarca, contra a Áustria e, em mil oitocentos e setenta, contra a França, que ele provoca editando um telegrama para soar como insulto.",
  "war_denmark|Prussian soldiers in dark blue and Austrian soldiers in white coats together storming earth fortifications in snow in 1864" + SEMBAND,
  "war_austria|Prussian infantry in dark blue coats and spiked helmets charging Austrian soldiers in white coats on a hill in summer 1866, smoke" + SEMBAND,
  f"telegram|{BISM}, sitting at a desk crossing out lines on a telegram with a pencil and smiling slyly, comic" + SEMTXT,
  card="1870")
b("Os estados do sul correm para o lado da Prússia, o imperador francês é capturado, e voltamos ao Salão dos Espelhos. [curious] O novo imperador estava emburrado: queria ser imperador da Alemanha, não imperador alemão. E desce do palanque sem apertar a mão de Bismarck.",
  "sedan_surrender|A round-white-head cartoon French emperor of 1870 with a long waxed mustache handing over his sword to Prussian officers in a field" + SEMBAND,
  "proclamation",
  f"grumpy_kaiser|{WILH1} with his arms crossed and a sulking face walking past {BISM} who holds out his hand, in the Hall of Mirrors, comic" + SEMBAND,
  card="1871")
b("E aqui está a segunda peça da resposta. A Alemanha não nasceu de uma votação. Nasceu de três guerras, e por isso nasceu na casa do inimigo. Só que país feito na guerra tem fronteira feita na guerra.",
  "piece_two|A second golden puzzle piece placed next to the first, showing a sword lying across a map of central Europe, symbolic" + SEMTXT,
  "map_1871|Map of Europe in 1871 with the new German Empire painted dark blue in the center and France, Austria and Russia in pale colors around it, absolutely no letters or country names written on the map, " + MAPA,
  "neighbors_watch|Round-white-head cartoon French, Russian and British gentlemen of 1871 peeking nervously over a fence at a big new factory and barracks, comic" + SEMBAND)

# ───────────────────────── 7. O GIGANTE ─────────────────────────
cap("7. O gigante no meio da Europa")
b("Vale do Ruhr, mil e novecentos. Imagine chaminés até o horizonte, fornos acesos dia e noite, trens de carvão. Em poucas décadas, a Alemanha produz mais aço que a Inglaterra.",
  "ruhr|An industrial valley in Germany in 1900 full of tall brick chimneys, blast furnaces glowing orange, coal trains and workers' houses, smoky sky",
  "steel_workers|Round-white-head cartoon German steel workers of 1900 in caps pouring glowing molten steel in a huge factory hall" + SEMTXT,
  card="1900")
b("Dali saem o carro a gasolina, de Benz, e a aspirina, da Bayer. [curious] Aquele comprimido na sua gaveta tem passaporte alemão.",
  "benz_car|A round-white-head cartoon man of 1886 with a beard driving a tiny three-wheeled early motor car on a cobblestone street, people staring amazed, comic" + SEMTXT,
  "aspirin|Close view of a modern white pill bottle without label and two white tablets on a bedside table, comic" + SEMTXT,
  "old_pension|A round-white-head cartoon old German worker of 1890 receiving a few coins at a post office counter and smiling, Bismarck watching from a portrait with a sly face, comic" + SEMTXT)
b("§ Só que, em mil oitocentos e oitenta e oito, sobe ao trono Guilherme Segundo, jovem e impaciente. Ele demite Bismarck, quer colônias e uma marinha para encarar a britânica. Então consegue juntar contra si França, Rússia e Inglaterra.",
  f"wilhelm2|{WILH2}, posing proudly with one hand on his sword on a big warship deck" + SEMBAND + "@@GUILHERME II",
  "bismarck_leaves|A round-white-head cartoon old bald statesman with a big grey mustache walking down the stairs of a ship with a suitcase, a young emperor waving from above, 1890 harbour with a modern steamship only, no galleon, no Roman soldiers, no crowns on bystanders, comic",
  "warships|A line of big grey battleships of 1905 with tall funnels sailing in the North Sea, smoke" + SEMBAND,
  "alliance|Round-white-head cartoon French, Russian and British leaders of 1907 shaking hands in a circle and looking sideways toward Germany, comic" + SEMBAND,
  card="1888")
b("Em mil novecentos e catorze vem a guerra em duas frentes que Bismarck temia. Pense: quatro anos de trincheira. Em mil novecentos e dezoito, com fome pelo bloqueio, a Alemanha se rende, e o imperador foge para a Holanda.",
  f"trench_1916|{TROPAS} in a muddy trench under a grey sky with shell craters and broken trees behind" + SEMBAND + SANG,
  "turnip_winter|Round-white-head cartoon hungry Berliners of 1917 queueing in the snow for turnips at a market stall, thin and tired" + SEMTXT,
  "kaiser_flees|A round-white-head cartoon emperor with a waxed mustache sitting sadly in a train compartment with suitcases, looking out at a Dutch windmill, 1918" + SEMBAND,
  card="1918")
b("Lembra do Salão dos Espelhos? Em mil novecentos e dezenove, os vencedores escolhem o mesmo salão para a Alemanha assinar a paz. Ela perde cerca de um oitavo do território e as colônias, e assume a culpa pela guerra. Só que quem herda essa conta é uma república recém-nascida.",
  "hall_mirrors_empty",
  "treaty_1919|Round-white-head cartoon diplomats in dark suits at a long table in the Hall of Mirrors of Versailles in 1919, two German delegates signing with grim faces, photographers, every man has a plain simple round white head with dot eyes and an optional simple big mustache shape, nobody has a toothbrush mustache or side-parted hair" + SEMTXT,
  "map_1919|Map of Germany in 1919 in dark blue with small areas on its edges in the west, north and east colored grey to show lost lands, " + MAPA,
  "bill_republic|A round-white-head cartoon young woman in 1919 clothes representing a new republic receiving an absurdly long unrolled bill from stern diplomats, comic" + SEMTXT,
  card="1919")

# ───────────────────────── 8. A REPÚBLICA FERIDA ─────────────────────────
cap("8. O pão de duzentos bilhões")
b("Berlim, novembro de mil novecentos e vinte e três. Uma mulher empurra um carrinho de mão cheio de notas até a padaria: um pão custa duzentos bilhões de marcos. [curious] Conta-se que um ladrão levou o carrinho e deixou o dinheiro na calçada.",
  f"wheelbarrow|A round-white-head cartoon Berlin woman of 1923 in a cloche hat pushing a wheelbarrow full of bundles of banknotes along a street toward a bakery" + SEMTXT,
  "bread_price|Close view of a single loaf of bread on a bakery counter next to huge stacks of banknote bundles, a shocked round-white-head cartoon baker, comic" + SEMTXT,
  "thief_wheelbarrow|A comic scene: a round-white-head cartoon thief in a flat cap running away with an empty wheelbarrow, leaving a pile of banknotes on the sidewalk" + SEMTXT,
  "kids_banknotes|Round-white-head cartoon children of 1923 playing with bundles of worthless banknotes like building blocks in a street, comic" + SEMTXT,
  card="1923")
b("Se os seus pais viveram a inflação do Brasil antes do Plano Real, eles conhecem esse filme. Agora imagine os preços dobrando a cada poucos dias. E quem leva a culpa é a república de Weimar, a primeira democracia alemã.",
  "brazil_market|A round-white-head cartoon Brazilian supermarket employee of 1990 putting new price stickers on top of old price stickers on cans with a price gun, comic, the price stickers are plain colored circles with no numbers and the can labels are plain colors, no dollar signs" + SEMTXT,
  "weimar_assembly|Round-white-head cartoon German politicians of 1919 in dark suits at a national assembly in a theater hall, serious faces" + SEMTXT + SEMBAND,
  "worthless_money|Round-white-head cartoon Berliners of 1923 using bundles of banknotes as fuel in a stove, comic" + SEMTXT)
b("§ Aí os inimigos da república espalham uma mentira: o exército não tinha perdido a guerra; tinha sido apunhalado pelas costas por políticos, comunistas e judeus. Era falso. Mas muita gente quis acreditar.",
  f"lie_whisper|{WEIM} whispering rumors to each other in a dark smoky beer hall, suspicious faces" + SEMTXT,
  "newspaper_lies|A stack of newspapers of 1920 with only big dark blocks instead of headlines on a street kiosk, round-white-head cartoon passersby frowning" + SEMTXT)
b("Então, no meio da festa dos anos vinte, a bolsa de Nova York quebra. É mil novecentos e vinte e nove. Os empréstimos americanos somem, e seis milhões de alemães ficam sem emprego.",
  "berlin_twenties|A lively Berlin street at night in 1927 with cabaret lights, trams, cars and round-white-head cartoon people dancing, cheerful, all neon signs and theatre marquees are plain glowing shapes with no letters, no words" + SEMTXT,
  "wall_street_crash|Round-white-head cartoon stockbrokers of 1929 panicking in front of a stock exchange building in New York, papers flying" + SEMTXT,
  f"unemployed|A long line of {WEIM} unemployed men waiting in front of a closed factory gate in winter 1931, sad" + SEMTXT,
  card="1929")
b("Lembra da nossa pergunta? Agora ela fica perigosa: um partido promete devolver tudo o que foi perdido, e mais. Em janeiro de mil novecentos e trinta e três, conservadores convencem o presidente a nomear Adolf Hitler chanceler, achando que iam controlá-lo. Estavam errados.",
  "crowd_rally|A huge crowd of round-white-head cartoon people of 1932 seen from behind listening to a distant speaker on a podium, grey sky" + SEMSIMB,
  "old_president|A round-white-head cartoon very old German president of 1933 with a simple flat big white mustache shape, a field marshal uniform, sitting at a desk being persuaded by men in suits" + SEMSIMB,
  "puppet_strings|Symbolic scene: elegant hands in white gloves holding the strings of a marionette, but the strings are already snapping, dark background" + SEMSIMB,
  card="1933")

# ───────────────────────── 9. O ABISMO (1933–45; sem humor) ─────────────────────────
cap("9. O abismo")
b("[serious] Berlim, dez de novembro de mil novecentos e trinta e oito. De manhã, as calçadas estão cobertas de vidro. Na noite anterior, sinagogas foram queimadas e lojas de judeus destruídas pelo país inteiro. É a Noite dos Cristais.",
  "broken_glass|Close view of a cobblestone sidewalk covered with broken glass in front of a shop with smashed windows and an empty display, morning light, no people" + SEMSIMB,
  "synagogue_smoke|A synagogue with a dome in a German city street at dawn with smoke rising from its roof, somber, no people" + SEMSIMB,
  "street_silence|An empty Berlin street of 1938 at dawn with broken shop windows, a few round-white-head cartoon neighbors watching silently from their windows, somber" + SEMSIMB,
  card="1938")
b("Repare como se chegou ali: passo a passo, com leis. Em mil novecentos e trinta e três, a democracia acaba, e os primeiros campos de concentração recebem opositores. Em mil novecentos e trinta e cinco, os judeus alemães perdem a cidadania.",
  "parliament_closed|The doors of a big German parliament building closed with a heavy chain and a padlock, grey sky, symbolic, no people" + SEMSIMB,
  "law_stamp|A heavy rubber stamp coming down on a stack of official papers on a dark desk, symbolic, no readable text" + SEMSIMB,
  "lost_passport|Close view of an old document with a photo of a round-white-head cartoon family being crossed out with a black line, symbolic" + SEMSIMB)
b("§ Em setembro de mil novecentos e trinta e nove, a Alemanha invade a Polônia, e começa a Segunda Guerra Mundial. Em dois anos, ela domina quase toda a Europa e invade a União Soviética.",
  "tanks_1939|A column of grey tanks of 1939 driving along a dusty country road past a field and a small farmhouse, seen from far away" + SEMSIMB,
  "map_1941|Map of Europe in 1941 with a huge dark grey area covering most of the continent and pale areas for Britain, Spain, Sweden and the eastern Soviet Union, " + MAPA,
  card="1939")
b("Atrás da frente de batalha, o regime nazista assassina seis milhões de judeus europeus, além de ciganos roma e sinti, pessoas com deficiência, prisioneiros soviéticos e opositores. É o Holocausto: um genocídio planejado e executado pela máquina de um Estado.",
  "rail_tracks|Empty railway tracks in winter leading to a dark distant gate under a grey sky, snow, no people, solemn" + SEMSIMB,
  "suitcases|A pile of old empty leather suitcases and worn shoes in a dim room, solemn, symbolic, no people" + SEMSIMB,
  "candles_memorial|Many small candles burning on dark stone in the night, solemn, symbolic" + SEMSIMB,
  "barbed_fence|A barbed wire fence with wooden posts in fog at dawn, birch trees behind, no people, solemn" + SEMSIMB,
  card="1941–1945")
b("Depois de Stalingrado, em mil novecentos e quarenta e três, a guerra vira. Em maio de quarenta e cinco, com Berlim em ruínas e Hitler morto, a Alemanha se rende sem condições. O problema: o país nascido pela guerra fica sem governo, com a fronteira desenhada pelos outros.",
  "stalingrad|A city in ruins covered in snow with broken buildings and chimneys, smoke rising, a frozen river, no people" + SEMSIMB,
  "berlin_ruins|Berlin in ruins in May 1945: rows of bombed buildings with empty windows, rubble in the streets and the damaged Brandenburg Gate in the distance, dusty light" + SEMSIMB,
  "white_flag|A white cloth hanging from a broken window of a ruined building, symbolic, no people" + SEMSIMB,
  "map_zones|Map of Germany in 1945 divided into four zones colored blue, red, green and yellow, with the city of Berlin also cut in four inside the red zone, " + MAPA,
  card="1945")

# ───────────────────────── 10. O MURO ─────────────────────────
cap("10. O muro que caiu por engano")
b("Berlim, verão de mil novecentos e quarenta e cinco. Mulheres passam tijolos de mão em mão, tirando o entulho das ruas. Os alemães chamam esse momento de hora zero.",
  "rubble_women|A long line of round-white-head cartoon German women in headscarves and aprons passing bricks from hand to hand over piles of rubble in a ruined street, summer 1945" + SEMTXT,
  "bricks_close|Close view of hands in worn gloves cleaning old bricks with a hammer and stacking them neatly, dusty sunlight",
  "zero_hour|A round-white-head cartoon family of 1945 standing in front of a destroyed house with a small cart of belongings, looking at a new morning sky, quiet hope",
  card="1945")
b("Mas a conta vem inteira: a Alemanha perde as terras a leste do rio Oder, e milhões de alemães são expulsos de lá. Em mil novecentos e quarenta e nove, viram dois países: a Ocidental, democrática, e a Oriental, comunista, sob Moscou.",
  "expellees|Long columns of round-white-head cartoon German refugees of 1945 with carts and horses walking on a snowy road in the east, sad" + SEMBAND,
  "map_two_germanys|Map of central Europe in 1949 with West Germany painted green and East Germany painted red, a small divided city inside the red area, " + MAPA,
  "two_leaders|Two round-white-head cartoon German politicians of 1949, one old in a dark suit on the left and one in a grey suit on the right, standing back to back, comic" + SEMBAND,
  card="1949")
b("E aqui está a terceira peça da resposta. Feita pela guerra, a Alemanha foi desfeita pela guerra. Por quarenta anos, onde fica a Alemanha dependia de que lado do muro você estava.",
  "piece_three|A third golden puzzle piece fitting into a puzzle that shows a map of Germany cut in two by a grey wall, symbolic" + SEMTXT,
  "berlin_wall|The Berlin Wall in the 1970s: a grey concrete wall with a death strip, watchtowers and lamps, houses on both sides, cold light" + SEMTXT,
  "family_wall|Two round-white-head cartoon families waving at each other over the Berlin Wall from windows on opposite sides, sad" + SEMTXT,
  card="1961")
b("No lado ocidental, vem o milagre econômico. O Fusca que você viu na garagem do seu avô saiu dessa Alemanha. No oriental, a polícia política espiona até vizinho e parente.",
  "beetle_garage|A round-white-head cartoon Brazilian grandfather proudly polishing a light blue Volkswagen Beetle in a garage of the 1970s, comic" + SEMTXT,
  "wirtschaftswunder|A busy West German city street of the 1950s with new buildings, shops, trams and small round cars, cheerful" + SEMTXT,
  "stasi_ears|A round-white-head cartoon man in a grey coat and hat pressing a glass against an apartment wall to listen to the neighbors, grey apartment block, comic but tense" + SEMTXT)
b("§ Nove de novembro de mil novecentos e oitenta e nove. Depois de semanas de protestos pacíficos, um porta-voz do governo oriental anuncia ao vivo que a fronteira vai abrir. Perguntado quando, ele olha os papéis e responde: imediatamente.",
  "candle_protest|A huge peaceful crowd of round-white-head cartoon East Germans of 1989 walking at night holding candles in a city street, calm" + SEMTXT + SEMBAND,
  "press_conference|A round-white-head cartoon bald East German official with glasses at a press conference table in 1989, confused, looking at his papers, microphones and journalists" + SEMTXT,
  card="1989")
b("Milhares correm para o muro, e os guardas, sem ordens, abrem a passagem. Em três de outubro de mil novecentos e noventa, a Alemanha se reunifica sem um tiro. E num tratado com os vencedores da guerra, aceita as fronteiras de hoje como definitivas.",
  "wall_party|Round-white-head cartoon Berliners of 1989 dancing and hugging on top of the Berlin Wall at night in front of the Brandenburg Gate, fireworks" + SEMTXT,
  "gate_open|Round-white-head cartoon East German border guards in grey uniforms lifting a barrier while a joyful crowd runs through, night, 1989" + SEMTXT + SEMBAND,
  "hammer_wall|Round-white-head cartoon people chipping pieces of the Berlin Wall with hammers and chisels, smiling" + SEMTXT,
  "treaty_1990|Round-white-head cartoon diplomats of 1990 in suits signing a treaty at a round table and shaking hands, calm, flowers on the table" + SEMTXT + SEMBAND,
  card="1990")
b("Hoje, é a maior economia da Europa, e lembra o próprio passado com memoriais no centro da capital. Então, dá para responder a Goethe?",
  "berlin_today|Modern Berlin seen from above on a sunny day with the Reichstag building with its glass dome, the river Spree and the Brandenburg Gate" + SEMTXT,
  "memorial_blocks|A memorial field of many grey concrete blocks of different heights in the center of a modern city, people walking quietly between them, soft light" + SEMTXT)

# ───────────────────────── FECHO (≤ 45 s) ─────────────────────────
cap("Fecho")
b("§ E a resposta da nossa pergunta: a língua uniu os alemães cedo, mas o poder ficou em pedaços por mil anos. Quando o país nasceu, nasceu pela guerra, e a fronteira mudava a cada guerra. Só em mil novecentos e noventa, com uma assinatura, ela parou.",
  "piece_final|A finished golden puzzle showing the whole story of Germany from a dark forest to the Brandenburg Gate, symbolic" + SEMTXT,
  "mirror_final|A single tall golden mirror of Versailles reflecting the Brandenburg Gate at sunset, symbolic, dreamlike",
  "pen_sword|Symbolic scene: an old fountain pen lying on top of a sword on a wooden table by a window, warm light" + SEMTXT)
b("[warm] Talvez a pergunta de Goethe nunca tenha sido onde fica a Alemanha. E sim quem desenha o mapa: o canhão ou a assinatura.",
  "goethe_smile|Two round-white-head cartoon poets of 1796 in frock coats smiling and looking at a modern map of Germany with clear borders" + SEMTXT,
  "rhine_sunset|The Rhine river at sunset with a castle on a hill, vineyards and a small boat, peaceful")
b("E para você: qual virada da história alemã mais te surpreendeu? Conta aí nos comentários.",
  f"guide_comment|{GUIA} sitting on a bench in front of the Brandenburg Gate, holding a small golden mirror and looking at it thoughtfully" + SEMTXT,
  "brandenburg_gate#aberto")

# Grafia para a VOZ (o Fish lê como português). Conferir no teste de nomes (qa/pronuncia/).
# blocos.json leva "texto" (falado, vai ao Fish) e "tela" (grafia correta: legendas e SCRIPT).
FALA = [("Versalhes", "Versálhes"), ("Goethe", "Guête"), ("Schiller", "Chíler"), ("Armínio", "Armínio"),
        ("Colônia", "Colônia"), ("Mainz", "Máintz"), ("Tréveris", "Tréveris"), ("queruscos", "querúscos"),
        ("suevos", "suêvos"), ("Canossa", "Canóssa"), ("Otão", "Otão"), ("Voltaire", "Voltér"),
        ("Wittenberg", "Vítenberg"), ("Gutenberg", "Gútenberg"), ("Lutero", "Lutéro"), ("Vestfália", "Vestfália"),
        ("Potsdam", "Pótsdam"), ("Jena", "Iêna"), ("Grimm", "Grím"), ("Frankfurt", "Frânkfurt"),
        ("Bismarck", "Bísmark"), ("Ruhr", "Rúr"), ("Benz", "Bénts"), ("Bayer", "Báier"), ("Weimar", "Váimar"),
        ("Hitler", "Rítler"), ("Stalingrado", "Stalingrádo"), ("Oder", "Óder"), ("Praga", "Prága")]
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
