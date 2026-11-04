#!/usr/bin/env python3
"""Fonte única do 002-india: roteiro + planos.

Remodelagem para pt-BR de "The ENTIRE History of India in 16 Minutes" (History in Minutes, p9IIGdg91fE):
mesma ordem, mesmos beats, mesmo hook e mesmo fecho; texto reescrito como narração brasileira natural.

Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (o id I### é dado na ordem de aparição)
  "chave"          reuso; o enquadramento é escolhido sozinho
  "chave#enq"      reuso com enquadramento fixo
Se um bloco tiver poucos planos para a duração (> MAX_PLANO s cada), depois
dos 3 primeiros minutos o gerador completa com reenquadramentos das imagens
do próprio bloco.
"""
import json, math, re
from pathlib import Path

WPS = 2.5            # palavras por segundo (~150 ppm)
BREAK, LONG = 0.35, 0.8
MAX_PLANO = 4.25     # s estimados (o áudio real varia ±10%; o render reescala por bloco)
INEDITO_ATE = 180.0  # s: só imagens novas até aqui
JANELA = 60.0        # s: mesmo enquadramento da mesma imagem só depois disso
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}


B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None): B.append({"t": t, "s": list(s), "card": card})

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("[serious] Olhe para a Índia do espaço em maio, e você não vai ver um país verde. Vai ver um país marrom: campos torrados, represas quase vazias.",
  "space_may|Satellite view of the Indian subcontinent from space in the dry season, the whole land brown and dusty, the blue Arabian Sea on the left and the Bay of Bengal on the right, a few white clouds",
  "dry_fields|Parched brown farmland in India in May, cracked earth, a lonely dry tree, a farmer in a white dhoti shading his eyes from the harsh sun",
  "reservoir_low|A nearly empty reservoir in India with a big dam wall, the water a tiny puddle at the bottom, boats stranded on cracked mud")
b("Nos piores anos, passa dos quarenta e nove graus. [break] [curious] Agora olhe em setembro. É outro país.",
  "heat_town|A dusty north Indian town street at noon in extreme heat, a huge street thermometer at the red top, people hiding under umbrellas, heat shimmer",
  "space_september|Satellite view of the Indian subcontinent from space after the monsoon, the whole land bright green, swirling white monsoon clouds, the blue Arabian Sea and the Bay of Bengal")
b("Verde do Mar Arábico à Baía de Bengala. [break] Nenhum rei mandou, nenhum império construiu. [break] No meio do caminho, chegou um vento.",
  "green_paddies|Endless bright green rice paddies in India after the rain, coconut palms, a village and water mirrors reflecting the sky",
  "king_shrug|An ancient Indian king on a golden throne shrugging with empty open hands, looking up at the sky with a confused face",
  "monsoon_wall|A huge dark wall of monsoon clouds rolling in from the sea over an Indian coastline with palm trees bending in the wind")
b("[amazed] Ele traz uns setenta por cento da chuva do ano em quatro meses, e quase um bilhão e meio de pessoas dependem dele. [serious] Quando falhou, milhões morreram de fome.",
  "monsoon_village|Heavy monsoon rain pouring on an Indian village, children dancing in the rain, women holding up their saris, mud streets turning to streams",
  "india_crowd|A huge colorful crowd of modern Indian people filling a wide street from edge to edge, seen from above",
  "farmers_rain|Indian farmers in a flooded field joyfully planting rice seedlings under light rain",
  "famine_old|A sad old engraving-style scene of a 19th century Indian village during a drought famine, thin people sitting by an empty well, dry fields")
b("A Índia não é um país que tem uma monção. [long-break] [emphasis] A Índia é uma monção que fez crescer um país.",
  "map_monsoon|Illustrated map of South Asia and the Indian Ocean with big curved blue arrows of the summer monsoon wind blowing from the ocean onto the land, rain clouds over India, no labels, no text",
  "wind_village|Strong monsoon wind blowing through an Indian village, palm trees bending, women holding their saris, kids running toward the first rain",
  "farmer_sky|An Indian farmer standing in his field with arms wide open looking up at dark rain clouds, the first drops falling on his face")
b("E esse vento está escrito no próprio planeta: a idade geológica em que você vive se chama Meghalaiano, [break] por causa de um canto da Índia.",
  "earth_layers|A cutaway cliff showing many colorful rock layers of the Earth, a tiny geologist with a hammer pointing at the thin top layer",
  "geologists|A group of geologists in a meeting room around a big chart of Earth's ages, one of them pinning a small map of northeast India at the very top",
  "meghalaya_hills|Misty green hills of Meghalaya in northeast India, waterfalls pouring off cliffs, living root bridges, heavy clouds")
b("Numa caverna de lá, uma estalagmite registrou quando, há quatro mil e duzentos anos, esse vento falhou e a seca atingiu do Egito à China.",
  "cave_stalagmite|Inside a dark limestone cave in Meghalaya, a tall stalagmite lit by a scientist's headlamp, water dripping",
  "stalagmite_cut|Scientists in a lab looking at a stalagmite cut in half lengthwise, showing many thin growth rings like tree rings",
  "drought_world|Ancient world in drought: an Egyptian farmer by a low Nile on the left and an ancient Chinese farmer by a dry field on the right, both looking at a cloudless sky")
b("[serious] Neste ano, ele enfraqueceu de novo.",
  "dry_sky_2026|A modern Indian farmer in 2026 with a smartphone in his hand standing in a dry field, looking up at a clear sky with only thin clouds")
b("[slightly dramatic] E aqui vem o impossível. [break] Alexandre, os Máurias, os mogóis, os portugueses, a Companhia das Índias e o Raj britânico: todos se foram.",
  "alexander_ruins|A broken marble statue of Alexander the Great lying in the dust among ruined Greek columns",
  "empires_fade|Ghostly faded figures of conquerors from different eras of India walking away into the mist: a Greek soldier, a Mauryan king, a Mughal emperor, a Portuguese captain, a British officer",
  "goa_ruin|An old abandoned Portuguese colonial church in Goa, India, with vines growing on the white walls",
  "union_jack_down|A British Union Jack flag being lowered at sunset over an Indian colonial building, Indian people watching")
b("A Índia continua aqui. Os mesmos rios, a mesma chuva, e mais gente do que qualquer país da história.",
  "ganges_today|The Ganges river at Varanasi today with ghats, temples, boats and pilgrims at sunrise",
  "rain_city|Monsoon rain falling on a busy modern Indian city street with colorful auto rickshaws and umbrellas")
b("[curious] Então como uma terra que todo império queria sobrevive a todos os impérios que a tomaram?",
  "conquerors_line|A long line of foreign armies from different eras marching into India through a mountain pass: Greek phalanx, Turkish horsemen, Mughal elephants, British redcoats",
  "farmer_calm_india|An Indian farmer calmly plowing his green field with two oxen while ghostly armies march past in the background")
b("Por que milhões morreram de fome em 1943, se a chuva não falhou? [break] E por que, agora, a Índia briga pelo rio que lhe deu o nome?",
  "bengal_1943_market|A 1940s Bengal market with empty rice baskets and very high price signs, worried people in dhotis and saris",
  "rain_no_food|1940s Bengal: rain falling over green rice fields while hungry people wait in a long line in front of a closed rice shop",
  "indus_wide|The wide Indus river flowing between dry brown mountains, seen from high above, a long old bridge crossing it",
  "indus_dispute|An Indian official and a Pakistani official in suits standing on opposite banks of a wide mountain river, glaring at each other")
b("[warm] Esta é a história dos primeiros dentistas do mundo, de uma cidade que virou ferrovia e de um imperador que ninguém conseguiu ler por séculos.",
  "dentist_ancient|A prehistoric healer in a mud-brick village carefully drilling a patient's tooth with a small bow drill, the patient wincing",
  "bricks_railway|A 19th century steam train running on a railway track laid over ancient red bricks",
  "ashoka_pillar|A tall polished stone pillar with four lions on top standing in an ancient Indian landscape, carved letters on it",
  "battle_storm|An 18th century battlefield in Bengal under a sudden heavy monsoon downpour, cannons and soldiers in the rain")
b("De uma batalha decidida por uma tempestade, de uma empresa com exército próprio, de um nariz que mudou a cirurgia e de uma mágica inventada por um jornal.",
  "company_army|A huge army of Indian sepoys in red coats marching under a striped East India Company flag, a merchant in a top hat watching with a ledger",
  "nose_man|An 18th century Indian ox cart driver with a bandage on his nose, looking at his reflection in a hand mirror, amazed",
  "rope_trick|A street magician in old India playing a flute while a rope rises straight into the air and a boy climbs it, a crowd gasping")
b("De uma fronteira traçada por quem nunca tinha visto o país. [break] De pimenta, sal e diamantes, e de um vento que decidia quem governava.",
  "lawyer_map|A 1940s British lawyer in a suit and round glasses drawing a line with a pencil across a big map at a desk, sweating",
  "spice_salt_diamond|A still life on a wooden table: a pile of black pepper, a heap of white salt and a huge sparkling diamond",
  "wind_throne|A royal throne in an Indian palace hall with monsoon wind blowing through, curtains flying, a crown rolling off the seat")
b("Para entender, temos que voltar para antes dos mogóis e de Buda, até um rio perto de Chennai e um machado de pedra mais velho que a nossa espécie.",
  "time_tunnel|A swirling tunnel of history going back in time: a Mughal palace, a Buddhist stupa, then a wild prehistoric landscape at the end",
  "riverbank_chennai|A prehistoric riverbank in south India with red earth, scrub trees and a calm river, no people",
  "stone_axe|A big teardrop-shaped prehistoric stone hand axe lying on red earth by a river")

# ───────────────────────── 1. ANTES DAS CIDADES ─────────────────────────
cap("1. Antes das cidades")
b("[amazed] Em 2011, cientistas dataram os machados de Attirampakkam com átomos de raios cósmicos. [break] Um milhão e meio de anos.",
  "axe_lab|Scientists in a modern lab measuring a prehistoric stone hand axe with a machine, screens with graphs",
  "cosmic_rays|Cosmic rays shown as glowing streaks falling from space onto a prehistoric riverbank and stones",
  "erectus_axe|An early human ancestor of the Homo erectus kind, hairy and muscular, knapping a stone hand axe by a river in prehistoric south India", card="1,5 milhão de anos")
b("A nossa espécie chegou bem depois, e encontrou parentes pelo caminho.",
  "sapiens_arrive|A small group of early modern humans with spears and skins walking into a green Indian valley",
  "meet_neanderthal|An early modern human and a stocky Neanderthal man meeting by a campfire, curious and cautious")
b("[curious] Os indianos carregam tantos pedaços de DNA neandertal que, em 2025, cientistas remontaram metade do genoma neandertal só com genomas indianos.",
  "neanderthal_family|A Neanderthal family sitting by a fire at the entrance of a cave, simple and peaceful",
  "dna_lab|Geneticists in a lab in India looking at screens full of DNA sequences, a Neanderthal skull model on the desk",
  "dna_puzzle|A giant glowing DNA double helix being assembled like a jigsaw puzzle from many small colorful pieces held by modern Indian people")
b("O passado da Índia engana até cientista. Em Bhimbetka, gente pintou cenas de caça na rocha há pelo menos dez mil anos.",
  "rock_shelter_inside|Inside a sandstone rock shelter in central India with red prehistoric paintings of hunters, dancers and animals on the walls",
  "bhimbetka|The huge sandstone rock shelters of Bhimbetka in central India surrounded by green forest",
  "cave_hunt|Prehistoric people painting red hunting scenes of deer and bison on a rock shelter wall by firelight")
b("Em 2021, pesquisadores anunciaram no teto de um abrigo o fóssil de um dos primeiros animais da Terra, de quinhentos e cinquenta milhões de anos.",
  "ceiling_fossil|Researchers with flashlights pointing excitedly at a leaf-shaped oval mark on the low rock ceiling of a shelter")
b("[warm] Dois anos depois, outra equipe olhou mais de perto. [long-break] Era a marca de uma colmeia que tinha caído.",
  "second_team|A second team of scientists on a ladder examining the rock ceiling mark with a magnifying glass, one of them raising an eyebrow",
  "beehive_mark|A wild honeybee hive hanging from a rock ceiling, and next to it the oval print left where an old hive fell off")
b("Depois vieram os agricultores. [break] Em Mehrgarh, no atual Paquistão, há nove mil anos, gente furava os molares de pacientes vivos, provavelmente com brocas de ponta de pedra.",
  "mehrgarh|The early farming village of Mehrgarh nine thousand years ago: mud-brick houses, wheat fields, goats, at the foot of dry mountains",
  "bow_drill|Close view of a prehistoric healer's hands working a small bow drill with a flint tip", card="7000 a.C.")
b("[amazed] É a odontologia mais antiga conhecida, e durou mil e quinhentos anos. Esses agricultores também estavam entre os primeiros a plantar algodão. [break] Guarde esse algodão.",
  "skull_teeth|An archaeologist holding an ancient human jaw and pointing at a tiny perfect drilled hole in a molar",
  "cotton_field|Prehistoric farmers in a field of fluffy white cotton plants, picking the bolls")

# ───────────────────────── 2. AS CIDADES DO INDO ─────────────────────────
cap("2. As cidades do Indo")
b("Por volta de 3300 antes de Cristo, os descendentes deles ergueram vilas no rio Indo, que viraram as primeiras grandes cidades do sul da Ásia.",
  "map_indus|Illustrated map of South Asia showing the Indus river and its tributaries in the northwest and the Ganges river in the east, the Himalaya mountains at the top, the Arabian Sea, no labels, no text", card="3300 a.C.")
b("Ruas em grade, esgoto coberto, tijolos e pesos no mesmo padrão por centenas de quilômetros.",
  "grid_streets|Bird's-eye view of an ancient Indus city with perfectly straight streets in a grid, brick houses and people walking")
b("[curious] O rio se chamava Sindhu. Esse nome passou pelo persa e pelo grego, e virou a palavra Índia.",
  "indus_ancient|The wide ancient Indus river at sunset with reed boats and a brick city on the bank")
b("[serious] Depois, as cidades foram abandonadas e esquecidas, até que o mundo moderno as usou como pedreira.",
  "abandoned_city|An abandoned ancient brick city half buried by dust and dry grass, empty streets, no people")
b("Nos anos 1850, engenheiros britânicos que faziam uma ferrovia no Punjab precisavam de lastro, e acharam um morro de tijolos antigos perfeitos.",
  "rail_engineers|1850s British railway engineers in pith helmets with plans and surveying tools in the dry Punjab plain, Indian workers behind")
b("Usaram tijolo para uns cento e sessenta quilômetros de trilho. Uma das cidades mais antigas da Ásia foi parar debaixo dos trens. [long-break] Era Harappa. Guarde esse nome.",
  "workers_bricks|Long line of 19th century Indian workers carrying baskets of ancient bricks to a railway under construction",
  "harappa_today|The excavated ruins of Harappa today, low brick walls and foundations under a blue sky, a few visitors")
b("Ninguém consegue ler o que aquele povo escrevia. Em 2025, o estado de Tâmil Nadu ofereceu um milhão de dólares a quem decifrar a escrita.",
  "indus_seals|Small square ancient Indus stone seals with a carved unicorn-like bull and rows of mysterious signs, in a museum case",
  "tamil_prize|A modern Indian politician on a stage announcing a prize, a giant symbolic check, a big image of an Indus seal on a screen behind")
b("Na China, um museu paga por cada sinal decifrado dos ossos oraculares. Aqui, o prêmio é pela escrita inteira.",
  "oracle_bones|Ancient Chinese oracle bones with carved signs displayed in a museum, a scholar with a magnifying glass")
b("[curious] Talvez você tenha ouvido que invasores destruíram essas cidades. [break] Não há sinal de massacre.",
  "invaders_myth|Imaginary warriors with chariots charging at an ancient brick city drawn like an old storybook illustration, with a big question mark style of faded colors")
b("Há quatro mil e duzentos anos, a seca registrada naquela caverna chegou até elas. A mesma que, como mostramos no vídeo do Egito, derrubou os construtores de pirâmides.",
  "indus_drought|An ancient Indus city by a shrinking river with cracked mud banks, worried people carrying empty pots")
b("[serious] E não foi a última. Em 2025, climatologistas acharam quatro secas em mil anos, cada uma com mais de oitenta e cinco anos.",
  "climate_lab|Climate scientists at a computer showing a long timeline chart with four deep dips, pointing at them")
b("Os rios encolheram, o povo migrou rumo ao Ganges, e as cidades se esvaziaram devagar.",
  "empty_streets|A quiet ancient brick city street with closed doors and dust blowing, the last family leaving")
b("Enquanto isso, chegavam do noroeste povos que falavam uma forma antiga de sânscrito.",
  "mountain_pass|Ancient herders with horses and cattle coming down a rocky mountain pass in the northwest of India")
b("[curious] Eram primos dos antigos iranianos, de uma família de línguas que provavelmente nasceu perto do rio Volga. [break] A mesma família do português.",
  "steppe|Wide grassy steppe near the Volga river with ancient horse herders and wagons",
  "language_tree|A big illustrated tree with branches spreading out, small figures on different branches: an ancient Indian priest, a Persian, a Greek, a Roman and a Portuguese sailor")
b("Na Índia, essa chegada ainda gera briga. A genética mostra uma migração lenta, há uns quatro mil anos. [break] Não uma invasão. Uma mistura.",
  "debate|Modern Indian professors debating passionately around a table full of books and maps")

# ───────────────────────── 3. ASHOKA ─────────────────────────
cap("3. O imperador arrependido")
b("Por volta de 260 antes de Cristo, um imperador Máuria conquistou o reino de Kalinga. [serious] As próprias inscrições dele admitem: cem mil mortos.",
  "mauryan_army|A huge ancient Mauryan army with war elephants, chariots and archers marching across a plain", card="260 a.C.")
b("Abalado, ele virou budista e gravou mensagens de compaixão em rochas e em colunas com leões pelo império todo.",
  "emperor_monks|The ancient emperor kneeling before Buddhist monks in orange robes, receiving a blessing")
b("[slightly dramatic] Depois, a escrita dele caiu em desuso, e por séculos ninguém leu uma palavra.",
  "pillar_forgotten|An ancient stone pillar with carved letters overgrown by jungle vines, a monkey sitting on it")
b("Em 1837, James Prinsep, da Companhia das Índias Orientais, decifrou as letras. Mas o rei só usava títulos, como Amado dos Deuses.",
  "prinsep|A 19th century British scholar in a coat at a candle-lit desk covered in copies of ancient inscriptions, a eureka expression")
b("Só em 1915, quando um engenheiro de mina de ouro achou uma rocha com o nome dele, houve certeza. [break] [warm] Ashoka. Guarde os leões dele.",
  "ashoka|The ancient Indian emperor Ashoka in royal robes standing peacefully in front of a lion pillar and a stupa",
  "lion_capital|Close view of the stone capital with four lions back to back on top of an ancient pillar, against a blue sky")

# ───────────────────────── 4. O VENTO DOS MERCADORES ─────────────────────────
cap("4. O vento dos mercadores")
b("[warm] Enquanto isso, o vento enriquecia a Índia. Os marinheiros aprenderam a cruzar o Mar Arábico com a monção: ida no verão, volta no inverno.",
  "map_trade|Illustrated map of the Arabian Sea and Red Sea with a dotted ship route curving between the Red Sea coast of Egypt and the west coast of India, small ships, wind arrows, no labels, no text")
b("Mercadores romanos descarregavam pimenta indiana em Berenice, no Egito. E lá, em 2023, arqueólogos anunciaram um Buda de mármore.",
  "berenike|An ancient Red Sea port with Roman merchants in togas unloading sacks and jars from a ship, desert hills behind",
  "marble_buddha|Archaeologists brushing sand off a white marble statue of the Buddha in a desert excavation")
b("[amazed] Em 408, os godos cercaram Roma. E parte do resgate que exigiram foi pimenta: [break] quase uma tonelada.",
  "goths_siege|Gothic warriors with round shields and helmets camped outside the walls of ancient Rome",
  "pepper_ransom|Romans in togas carrying huge sacks of black pepper out of the city gate to a Gothic king, who grins", card="408")
b("[curious] Até a palavra monção vem desse comércio: é portuguesa, do árabe mawsim, a estação.",
  "arab_sailor|An Arab sailor in a turban on a dhow explaining the seasonal wind to a curious Portuguese sailor")
b("A Índia exportava ideias também. Em 628, o astrônomo Brahmagupta já tinha escrito regras para fazer contas com o zero.",
  "brahmagupta|An ancient Indian astronomer in a white dhoti sitting under a pavilion writing on palm leaves, stars and planets drawn around him", card="628")
b("Outros povos tinham um sinal para um lugar vazio. [amazed] A Índia fez do nada um número.",
  "empty_place|An ancient Babylonian scribe pressing marks into a clay tablet, leaving a small gap")
b("Os algarismos indianos foram para o oeste num livro do persa Al-Khwarizmi, que deu nome ao algoritmo.",
  "khwarizmi|The medieval Persian scholar Al-Khwarizmi in a turban writing a book in a library of Baghdad, numbers floating around")
b("E o xadrez, o jogo do xeque-mate, quase certamente nasceu aqui, como chaturanga.",
  "chaturanga|Two ancient Indian nobles playing chaturanga, an early chess game, on a cloth board with carved elephants, horses and chariots")
b("E não só ideias. [break] Em 1025, o imperador Rajendra Chola mandou uma frota cruzar a Baía de Bengala para atacar Srivijaya, na atual Indonésia.",
  "chola_emperor|The south Indian emperor Rajendra Chola wearing gold jewelry and a tall crown, pointing to the sea from a temple terrace",
  "map_chola|Illustrated map of the Bay of Bengal from south India to the Malay peninsula and Sumatra, with a fleet of small ships and a dotted arrow crossing the sea, no labels, no text", card="1025")
b("As mesmas rotas levaram deuses indianos para o leste. [amazed] Angkor Wat, no Camboja, o maior monumento religioso do planeta, nasceu hindu.",
  "gods_ship|Merchants on a ship carrying carved statues of Hindu gods across the sea toward a tropical coast",
  "angkor|Angkor Wat temple in Cambodia at sunrise, its five lotus towers reflected in a pond")

# ───────────────────────── 5. SULTÕES E MOGÓIS ─────────────────────────
cap("5. Sultões e mogóis")
b("O islã chegou duas vezes. Primeiro pelo mar, com mercadores árabes na monção. [break] Depois pelas montanhas, com exércitos.",
  "arab_merchants|Medieval Arab merchants arriving by dhow at a palm-lined port in Kerala, trading with local Indian merchants")
b("Em 1206, um general turco que tinha sido vendido como escravo fundou o Sultanato de Délhi.",
  "slave_general|A medieval Turkish general in armor and turban on a throne in Delhi, an old chain lying broken at his feet", card="1206")
b("[curious] E, como os mamelucos do nosso vídeo do Egito, os sucessores dele fizeram o que quase ninguém conseguiu: [break] seguraram os mongóis.",
  "sultan_vs_mongols|Delhi Sultanate soldiers with war elephants blocking a charge of Mongol horse archers on a dusty plain")
b("Em 1498, Vasco da Gama chegou a Calicute na monção. Perguntado o que queria, um dos homens respondeu: [break] Vimos buscar cristãos e especiarias.",
  "gama_ships|Vasco da Gama's three Portuguese caravels with red crosses on white sails arriving at the palm-lined coast of Calicut",
  "calicut_meeting|Portuguese sailors in 1498 clothes meeting a merchant in a turban on a busy Indian market street", card="1498")
b("[warm] Dois anos depois, a frota seguinte, de Cabral, saiu rumo à Índia e, no caminho, chegou ao Brasil.",
  "cabral_brazil|Portuguese caravels with red crosses on white sails arriving at a tropical Brazilian beach in 1500, green forest, a sailor looking at a map of India and scratching his head")
b("Em 1526, Babur, descendente de Gengis Khan, venceu em Panipat com canhões e fundou o Império Mogol.",
  "babur|Babur, the first Mughal emperor, a bearded Central Asian warrior king in a turban and armor, on horseback", card="1526")
b("O tataraneto dele, Shah Jahan, ergueu o Taj Mahal para a esposa, morta no parto do décimo quarto filho.",
  "shahjahan_mumtaz|The Mughal emperor Shah Jahan with a long beard and his wife Mumtaz Mahal in rich Mughal clothes in a palace garden",
  "taj|The finished white marble Taj Mahal at golden hour reflected in the long garden pool")
b("[slightly sad] Depois, o próprio filho o prendeu no forte de Agra. De lá, diz a história, ele via o túmulo dela.",
  "agra_prisoner|An old Mughal emperor with a white beard locked in a red sandstone fort room, guards at the door",
  "taj_window|View from an arched window of a red sandstone fort across a river to the white Taj Mahal far away, an old man's silhouette looking out")
b("[curious] Dizem que a Índia mogol era o país mais rico do mundo. Por uma estimativa famosa, fazia um quarto da produção mundial em 1700.",
  "mughal_court|A splendid Mughal court with an emperor on a jeweled throne, nobles in silk, gold and jewels everywhere", card="1700")
b("Mas também tinha mais de um quarto da população do mundo. [break] Grande não é o mesmo que rico.",
  "mughal_peasants|A huge crowd of poor Mughal-era peasants in simple clothes working in fields, stretching to the horizon")
b("O império se esgotou em guerras contra os maratas. Em 1739, o persa Nader Shah saqueou Délhi e levou o Trono do Pavão e o diamante Koh-i-Noor. [break] Guarde esse diamante.",
  "maratha_war|Maratha light cavalry riding through rocky Deccan hills, attacking a slow Mughal army column",
  "nader_delhi|The Persian conqueror Nader Shah in armor and a red Persian hat riding into Delhi with his army, carts loaded with treasure",
  "kohinoor|A huge sparkling diamond held up to the light in a man's hand", card="1739")

# ───────────────────────── 6. O SEGREDO DA ÍNDIA ─────────────────────────
cap("6. O segredo da Índia")
b("[serious] E esse é o segredo da Índia. O Egito, como vimos, é um rio com um país em volta. [break] A Índia foi construída em volta de um vento.",
  "nile_callback|Aerial view of the Nile as a narrow green ribbon through the desert, an Egyptian village on the bank",
  "india_wind|Wide view of the Indian subcontinent from high above with huge swirling monsoon clouds pouring onto the green land")
b("Todo verão, ele joga o Oceano Índico sobre a terra e alimenta um dos lugares mais populosos do planeta.",
  "rain_coast|Monsoon rain sweeping in from the ocean over the Kerala coast, fishermen pulling boats up the beach")
b("Conquistadores vinham pelas montanhas, mercadores no vento. Todos queriam o que a chuva dava: grãos, algodão, pimenta e gente para taxar.",
  "khyber|Invading horsemen of different eras riding through the narrow Khyber Pass with steep brown cliffs")
b("[slightly dramatic] Nenhum deles mandava nela. Monção boa enchia o tesouro. Monção ruim esvaziava.",
  "king_cloud|An old Indian king on a palace balcony pointing his scepter angrily at a rain cloud that ignores him")
b("Reis vinham e iam. [warm] O povo que plantava com a chuva durou mais que todos eles.",
  "kings_parade|A parade of Indian kings of different eras walking one after another and fading into mist")
b("Os conquistadores seguintes chegaram nesse vento, e nem eram um país. [long-break] Eram uma empresa.",
  "eic_ships|Big 18th century East India Company merchant ships with striped red and white flags anchored off the Indian coast")

b("Em junho de 1757, em Plassey, o pequeno exército de Robert Clive enfrentou o nababo de Bengala, com dez vezes mais homens.",
  "clive|Robert Clive, an 18th century British officer in a red coat and tricorn hat, standing in front of a small army",
  "nawab_army|A huge 18th century Bengal army with war elephants, cavalry and cannons stretching across a plain, the Nawab on an elephant", card="1757")
b("[slightly dramatic] No meio da batalha, caiu uma tempestade de monção. Os britânicos cobriram a pólvora com lonas. [break] Os artilheiros do nababo, não.",
  "storm_battle|A sudden heavy monsoon storm breaking over an 18th century battlefield, dark clouds and sheets of rain",
  "tarpaulins|British soldiers in red coats rushing to throw canvas tarpaulins over barrels of gunpowder in the rain")
b("A cavalaria dele atacou contando com canhões mudos, e foi repelida. E um aliado a quem Clive prometera o trono nem se mexeu.",
  "cavalry_charge|Bengal cavalry charging in the rain toward British lines, surprised by cannon smoke")
b("[amazed] Os britânicos perderam vinte e dois homens. Uma empresa tinha acabado de tomar Bengala. [serious] Guarde essa chuva.",
  "clive_victory|Robert Clive in a red coat raising his sword in victory after the rain, the sun breaking through")
b("Em 1803, a Companhia, dirigida de um escritório de cinco janelas em Londres, tinha um exército de duzentos mil homens: o dobro do britânico.",
  "london_office|A narrow 18th century London office building only five windows wide on a busy street, merchants entering",
  "sepoy_army|A massive army of Indian sepoys in red coats on parade, stretching to the horizon, a few British officers on horses", card="1803")
b("[curious] E deu ao inglês uma palavra do hindustâni: loot, saque.",
  "loot|British soldiers carrying chests of treasure and jewels out of an Indian palace onto carts")
b("Nem todo mundo se dobrou. No sul, Tipu Sultan, de Mysore, atacou a Companhia com foguetes de ferro.",
  "tipu|Tipu Sultan, ruler of Mysore, in a tiger-striped tunic and turban, standing proudly in front of his army",
  "mysore_rockets|Mysore soldiers launching iron-tube war rockets with long bamboo sticks, fiery trails toward British lines")
b("Os britânicos capturaram alguns e copiaram. Em 1814, as cópias atacaram um forte americano e foram parar no hino dos Estados Unidos.",
  "rockets_captured|British soldiers loading captured iron rockets into crates on a ship",
  "fort_mchenry|A star-shaped American fort at night in 1814 with red rocket trails across the sky and the American flag flying")
b("Em 1792, soldados de Tipu cortaram o nariz de Cowasjee, um condutor de bois que servia os britânicos.",
  "cowasjee|An 18th century Indian ox cart driver with a bullock cart full of supplies for the British army, stopped by Mysore soldiers",
  "nose_bandage|The same ox cart driver sitting sadly with a big bandage over his nose")
b("Um cirurgião perto de Pune refez o nariz com pele da testa dele, um método indiano de séculos.",
  "pune_surgeon|An 18th century Indian surgeon carefully working on a patient's face in a simple room near Pune, British officers watching amazed")
b("Uma revista de Londres publicou o caso. [amazed] Vinte anos depois, um cirurgião britânico copiou o método, e nasceu a cirurgia plástica moderna.",
  "london_magazine|Gentlemen in a London coffee house in the 1790s reading a magazine with an illustration of an Indian man's face, surprised")
b("[curious] E o diamante? Em 1849, a Companhia fez um marajá de dez anos, Duleep Singh, entregá-lo. [break] Hoje ele está numa coroa britânica, na Torre de Londres.",
  "duleep|A 10-year-old Sikh maharaja in a turban with jewels sitting on a big throne, British officials handing him a document to sign",
  "tower_crown|A royal crown with a huge diamond displayed in a glass case in the Tower of London, tourists looking", card="1849")

# ───────────────────────── 7. O RAJ BRITÂNICO ─────────────────────────
cap("7. O Raj britânico")
b("A monção continuava mandando. [serious] Em 1876, ela falhou no sul, e milhões morreram.",
  "famine_1876|A dry south Indian landscape in 1876 with dead crops, a dry well and a family sitting in despair, no rain", card="1876")
b("Naquele inverno, o vice-rei deu uma festa de uma semana em Délhi para proclamar Vitória imperatriz da Índia. No meio da fome.",
  "durbar|The grand 1877 Delhi Durbar: a huge ceremonial camp with tents, elephants in decorations, British officials and Indian princes, a big banner with a crown")
b("[slightly sad] O mesmo El Niño castigou o Ceará: a Grande Seca de 1877 matou centenas de milhares de brasileiros.",
  "ceara_seca|The dry sertão of Ceará in Brazil in 1877: cracked earth, cactus, a dead cow, and a family of retirantes walking with bundles under a scorching sun")
b("Para taxar o sal, os britânicos plantaram uma cerca de espinhos de quase quatro metros de altura e mil e oitocentos quilômetros, vigiada por doze mil homens.",
  "salt_hedge|A gigantic thorny hedge, taller than a man, stretching endlessly across the Indian plain to the horizon")
b("Um funcionário a comparou à Muralha da China. Ela foi abandonada em 1879, e esquecida.",
  "hedge_wall|A British official in a pith helmet looking at the endless hedge, and in a thought bubble the Great Wall of China")
b("Um dos chefes dela, Allan Octavian Hume, fundou depois o Congresso Nacional Indiano. [break] Guarde esse nome.",
  "hume|Allan Octavian Hume, a Victorian British official with a big white beard, standing with a group of Indian men in coats and turbans", card="1885")
b("Nessa época, o Ocidente se apaixonou pela mágica indiana. [curious] Mas o famoso truque da corda, em que um menino sobe no ar e some, [long-break] nunca existiu.",
  "western_magic|A Victorian theater audience in London watching an Indian magician on stage, amazed")
b("Foi inventado em 1890 por um repórter do Chicago Tribune. O jornal confessou a farsa quatro meses depois, e quase ninguém notou.",
  "tribune_reporter|An 1890 American newspaper reporter with a mustache typing a story with a sly smile in a busy newsroom")
b("[amazed] O repórter depois chefiou o Serviço Secreto dos Estados Unidos.",
  "secret_service|The same reporter, older, sitting at a big desk with an official badge and a small American flag, agents in dark suits behind him")
b("Em 1930, Gandhi, líder do partido de Hume, andou quase quatrocentos quilômetros até o mar para fazer sal contra a lei.",
  "salt_march|Mahatma Gandhi, a thin bald man in a white dhoti with round glasses and a walking stick, leading a long march of followers along a dusty road",
  "gandhi_salt|Gandhi on the seashore bending down to pick up a handful of natural salt from the mud, crowds watching", card="1930")
b("[curious] Lembra do algodão? A Grã-Bretanha proibiu o tecido indiano para proteger seus tecelões, e depois inundou a Índia com pano de fábrica.",
  "calico_ban|18th century English weavers protesting against colorful Indian cotton cloth, a British official nailing a ban notice")
b("Gandhi respondeu com uma roca de fiar, e pôs a roca na bandeira do partido.",
  "congress_flag|Indian people in white homespun clothes raising a saffron, white and green flag with a spinning wheel in the center")
b("[serious] Então veio uma fome que quebrou o padrão. Em 1943, até três milhões de pessoas morreram em Bengala.",
  "bengal_1943|Calcutta street in 1943 with long queues of thin people waiting for food at a relief kitchen, sad faces", card="1943")
b("Em 2019, cientistas reconstruíram a umidade do solo indiano desde 1870. Cinco grandes fomes batiam com secas. [break] 1943, não.",
  "soil_scientists|Modern Indian scientists at a computer screen showing a long soil moisture chart from 1870 to today")
b("[slightly dramatic] Lembra da chuva de Plassey? Desta vez, ela veio acima do normal.",
  "rain_1943|Heavy rain falling over green rice fields in 1940s Bengal, a farmer under a palm-leaf umbrella looking confused")
b("Um ciclone estragou a colheita, e o Japão cortou o arroz da Birmânia. Mas os pesquisadores falam em falha de política.",
  "cyclone|A 1942 cyclone hitting the Bengal coast, flattened rice fields and broken huts")
b("A comida foi para a guerra, os preços dispararam, e o governo nem declarou fome.",
  "war_food|1940s army trucks loaded with rice sacks driving away from a Bengal village while villagers watch")

# ───────────────────────── 8. LIBERDADE E PARTILHA ─────────────────────────
cap("8. Liberdade e partilha")
b("Quatro anos depois, a Índia estava livre, e partida em dois. Quem traçou a linha foi Cyril Radcliffe, um advogado de Londres que nunca tinha pisado lá.",
  "independence|Huge joyful crowds in Delhi in August 1947 waving the Indian tricolor flag with the blue wheel",
  "radcliffe|Cyril Radcliffe, a British lawyer in a grey suit and round glasses, stepping off a plane in India, looking lost in the heat", card="1947")
b("Ele teve umas cinco semanas. A fronteira saiu dois dias depois da independência.",
  "radcliffe_desk|Cyril Radcliffe alone in a hot office at night with a ceiling fan, drawing a line on a huge map of India, piles of papers")
b("[serious] De doze a quinze milhões de pessoas fugiram, e de duzentas mil a dois milhões morreram. [break] Radcliffe queimou os papéis e recusou o pagamento.",
  "partition_train|An overcrowded 1947 train with refugees packed inside and sitting on the roof, leaving a station")
b("[curious] Lembra da cidade debaixo da ferrovia? Harappa ficou no Paquistão, com a maior parte do rio que deu nome à Índia.",
  "map_partition|Illustrated map of the Indian subcontinent in 1947 with India in one color and West and East Pakistan in another color, the Indus river highlighted in blue, no labels, no text")
b("[slightly sad] Cinco meses depois, Gandhi foi morto a tiros por um nacionalista hindu.",
  "gandhi_mourning|Huge grieving crowds in Delhi in January 1948 around a flower-covered funeral carriage, people crying", card="1948")
b("Em 1950, a república escolheu seu emblema: [warm] os leões de Ashoka, das colunas que ninguém lia.",
  "emblem|An official 1950 Indian government document with a seal showing four lions back to back, held up by a smiling official",
  "lion_capital")
b("A primeira eleição foi a maior já vista: cento e setenta e três milhões de eleitores, e uns oitenta e cinco por cento não sabiam ler.",
  "election_1951|A long line of Indian villagers in 1951 waiting to vote outside a village school, women in saris and men in turbans")
b("Por isso, cada partido ganhou um símbolo, de uma junta de bois a uma lamparina.",
  "ballot_symbols|A row of 1951 ballot boxes each painted with a simple picture symbol: a pair of bullocks, an oil lamp, a tree, a hut, villagers choosing")
b("O resto passa rápido. 1962, guerra com a China. 1971, guerra com o Paquistão, e nasce Bangladesh. 1974, um teste nuclear chamado Buda Sorridente.",
  "war_1962|Indian soldiers in winter coats in the snowy Himalaya mountains in 1962",
  "bangladesh|Crowds in Dhaka in 1971 waving the green flag of Bangladesh with a red circle, celebrating",
  "nuclear_test|A desert in Rajasthan in 1974 with a huge dust cloud rising from the ground, scientists watching from far away", card="1962")
b("1984, uma primeira-ministra assassinada e o vazamento de gás de Bhopal. 1991, quase falência, e a economia se abre.",
  "indira|Mourning crowds in Delhi in 1984 with flowers around a portrait of a woman prime minister with a white streak in her hair",
  "bhopal|A chemical factory in Bhopal at night in 1984 with a yellowish gas cloud spreading over a sleeping town")
b("2014: Narendra Modi chega ao poder. [break] 2023: a Índia vira o país mais populoso da Terra, e pousa uma sonda perto do polo sul da Lua.",
  "modi|Narendra Modi, an Indian politician with a white beard and glasses, waving to a huge crowd with orange flags",
  "chandrayaan|An Indian lunar lander with a small rover standing on the grey surface of the Moon near the south pole, the Earth in the black sky")
b("2025, um atentado na Caxemira, ataques ao Paquistão e tarifas americanas de cinquenta por cento. [break] O que nos traz até agora.",
  "kashmir|The green valley of Pahalgam in Kashmir with pine trees and snowy mountains, candles and flowers of mourning in the foreground",
  "tariffs|Shipping containers piled at an Indian port with a big red 50% stamp on them, worried exporters", card="2025")

# ───────────────────────── 9. A ÍNDIA DE HOJE ─────────────────────────
cap("9. A Índia de hoje")
b("A Índia tem quase um bilhão e meio de pessoas, mais que qualquer país na história. E a mulher indiana já tem, em média, menos de dois filhos.",
  "india_today|A huge busy modern Indian city with metro trains, flyovers, skyscrapers and crowds", card="2026")
b("Pelo governo, é a quarta maior economia do mundo. [serious] Mas, por pessoa, produz umas doze vezes menos que o Japão.",
  "mumbai|Mumbai skyline with modern glass towers by the sea, the Gateway of India in the foreground")
b("Em setembro, a Índia terminou de contar as casas do seu primeiro censo digital. Em fevereiro, conta as pessoas e, pela primeira vez desde 1931, as castas.",
  "census_door|An Indian census worker with a tablet at the door of a village house, a family greeting her")
b("A última contagem completa de castas foi feita pelos britânicos.",
  "census_1931|A 1931 British census officer with a big ledger interviewing an Indian villager, clerks writing")
b("[serious] E, neste ano, o vento chegou atrasado e fraco. No fim de setembro, a chuva estava mais de dez por cento abaixo do normal.",
  "late_monsoon|Indian farmers in 2026 sitting on a dry field edge looking at a clear sky with a few weak clouds")
b("[curious] E por que isso importa? [break] Porque o problema mais antigo da Índia voltou. [long-break] Não são invasores. É a água.",
  "water_pots|Indian women carrying steel water pots on their heads walking across a dry field to a distant well")
b("O El Niño deve seguir no ano que vem, e monção fraca é comida mais cara. [break] E a briga saiu do céu para os rios.",
  "market_prices|A modern Indian vegetable market with price boards and worried shoppers looking at onions and tomatoes")
b("Em abril de 2025, após um atentado que matou vinte e seis pessoas na Caxemira, a Índia suspendeu o tratado que divide o Indo com o Paquistão.",
  "treaty|An old treaty document on a table with a red stamp saying on hold, an Indian official putting it in a drawer")
b("No fim de agosto, um tribunal em Haia disse que o tratado segue valendo. A Índia não o reconhece. O Paquistão diz que ninguém suspende um tratado sozinho.",
  "hague|The Peace Palace in The Hague, a red brick building with a clock tower")
b("[slightly dramatic] O rio que deu nome à Índia está no tribunal. [break] E, rio acima, a China ergue a maior hidrelétrica do mundo no rio que vira o Brahmaputra.",
  "river_court|A symbolic image of a river flowing right through the middle of a courtroom, judges looking at it",
  "china_dam|A gigantic hydropower construction site in a deep gorge on the Tibetan plateau, cranes and tunnels, snowy peaks")
b("Por quatro mil anos, a Índia esperou a água cair do céu. [break] Agora, ela briga pela água no chão.",
  "waiting_sky|Ancient Indian farmers and modern Indian farmers standing side by side looking up at the sky, waiting for rain")
b("[warm] Há quatro mil e duzentos anos, o vento falhou, e as primeiras cidades se esvaziaram. Uma caverna em Meghalaya guardou o registro.",
  "empty_streets", "cave_stalagmite")
b("Ashoka não mandava na chuva. Os mogóis também não. A Companhia também não.",
  "ashoka", "eic_ships")
b("[warm] Neste setembro, vista do espaço, a Índia ficou verde de novo. Não toda, e não o bastante. [break] Mas ficou verde, como fica desde antes de existirem reis.",
  "space_september")
b("Os imperadores se foram. [long-break] O vento continua fazendo crescer um país.",
  "empires_fade",
  "monsoon_final|Monsoon clouds rolling over endless green Indian fields and villages at golden hour, birds flying")
b("[warm] Obrigado por acompanhar essa viagem dos primeiros dentistas ao maior censo do mundo. Se curtiu, deixa o like e se inscreve.",
  "time_tunnel",
  "taj")
b("E conta nos comentários: qual invenção indiana você mais usa? O zero, o xadrez, o algodão ou o xampu? Até o próximo.",
  "inventions|A wooden table with a chess board, a cotton shirt, a shampoo bottle, a big wooden zero and buttons, an Indian grandmother smiling behind it")

# blocos que abrem uma ideia nova (o build.py põe ~0,9 s antes deles; antes de capítulo já são ~1,5 s)
IDEIA = {5, 6, 8, 9, 11, 12, 13, 16, 18, 20, 23, 24, 27, 28, 31, 33, 34, 37, 39, 42, 45, 47, 49, 53, 54, 57, 58, 59, 62, 63, 65, 70, 71, 75, 76, 78, 80, 83, 86, 89, 90, 93, 94, 96, 98, 101, 103, 105, 106, 107, 109, 114, 115, 117, 118, 120, 122, 123, 124, 126, 127, 128}

THUMB = {"id": "thumb-base", "qualidade": "high",
         "prompt": "Wide panoramic landscape of India placed in the left 55% of the frame: the white Taj Mahal, a tall ornate Hindu temple tower, the Ganges river with wooden boats and ghats with pilgrims, palm trees and green fields; the right 45% of the frame is open bright blue sky with a few small white clouds above flat green fields, completely empty to leave room for a title"}

# ───────────────────────── geração ─────────────────────────
TAG = re.compile(r"\[[a-z][a-z -]*\]\s*")   # [break], [long-break], [emphasis] e as tags de tom ([curious] etc.)
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
            if "|" in s:
                k, p = s.split("|", 1)
                assert k not in prompts, f"chave repetida {k}"
                prompts[k] = p; specs.append((k, None))
            else:
                k, _, e = s.partition("#"); assert k in prompts, f"{bid}: chave {k} sem prompt antes"
                specs.append((k, e or None))
        need = math.ceil(d / MAX_PLANO)
        if len(specs) < need:
            if t + d <= INEDITO_ATE + 5:
                avisos.append(f"{bid} ({fmt(t)}): faltam planos novos ({len(specs)}/{need})")
            else:
                proprias = [k for k, _ in specs] or [planos[-1]["chave"]]
                i = 0
                while len(specs) < need:
                    specs.insert(min(2 * i + 1, len(specs)), (proprias[i % len(proprias)], None)); i += 1
        palavras = limpo(blk["t"]).split()
        cada = d / len(specs)
        for j, (k, e) in enumerate(specs):
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
            if cada < 2.0 or cada > MAX_PLANO + 0.5: avisos.append(f"{bid}: plano de {cada:.1f}s")
            planos.append({"plano": len(planos) + 1, "ini": round(ini, 2), "fim": round(ini + cada, 2),
                           "bloco": bid, "trecho": " ".join(palavras[a:z]), "chave": k, "imagem": ids[k],
                           "nova": nova, "enq": enq, "mov": mov, "nota": "; ".join(nota)})
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
             "plano_medio_s": round(total / len(planos), 2), "avisos": avisos}

    (out / "blocos.json").write_text(json.dumps(blocos, ensure_ascii=False, indent=1) + "\n")
    (out / "cenas.json").write_text(json.dumps(cenas, ensure_ascii=False, indent=1) + "\n")
    (out / "storyboard.json").write_text(json.dumps({"stats": stats, "planos": planos}, ensure_ascii=False, indent=1) + "\n")
    (out / "SCRIPT.md").write_text(
        f"# A HISTÓRIA COMPLETA da Índia em {round(total / 60)} minutos: roteiro\n\n"
        f"Gerado por `roteiro.py` (fonte única; edite lá). {words} palavras, ~{fmt(total)} estimados a {WPS*60:.0f} ppm.\n"
        "Os blocos [Nxxx] são os mesmos de `blocos.json` (lá com as tags do Fish).\n" + "\n".join(script))
    linhas = ["# Storyboard: A HISTÓRIA COMPLETA da Índia",
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
