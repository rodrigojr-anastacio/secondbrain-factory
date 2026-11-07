#!/usr/bin/env python3
"""Fonte única do 005-brasil (07/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

Molde History in Minutes (canais/historia-ptbr/biblia/roteiro.md; referência de código: videos/004-china e 003-ira v2):
  hook (anedota da nau Bretoa, 1511: a lista de carga em que o nome Brasil aparece: madeira, bichos e gente)
  → "Essa é a história inteira do Brasil" → pergunta central (a terra que nasceu como carga de navio virou país: como?)
  → promessa em lista → "o que vai no navio e o que fica aqui; guarde essa lista de carga"
  → 10 eras ligadas por "mas… então…" (título-frase só na placa, nunca falado)
  → fecho que paga a lista de carga e a palavra "brasileiro".
Fio condutor: O QUE VAI NO NAVIO E O QUE FICA: cada riqueza (pau-brasil, açúcar, ouro, café, borracha, petróleo, soja) sai e deixa um país diferente.
Loops: lista de carga (hook → era 2 → fecho); linha de Tordesilhas (era 1 → era 4); quase 5 milhões (era 3 → era 7 → fecho);
       conselho de Dom João (era 5 → era 6); o navio no sentido contrário (era 5); "o petróleo é nosso" (era 9).

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1500") · texto que começa com "§ " abre ideia nova (~0,9 s antes) · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco (técnica B2 do 003), gaps 0,35/0,9/1,5 s no build.py, tags de tom só onde a emoção muda.
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (004: 2.093 palavras em 16:14; a estimativa erra ~3% para cima)
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
TITULO = "A história INTEIRA do Brasil"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None):
    ideia = t.startswith("§")
    B.append({"t": t.lstrip("§ ").strip(), "s": list(s), "card": card, "ideia": ideia})

# Mapas sem texto (rótulos no código, src/labels.jsx) e regra de "sem escrita" em objetos com inscrição
MAPA = ("painted like a blank parchment terrain map seen from directly above, only coastlines, rivers, mountains and flat colored areas, "
        "completely blank with no writing anywhere, no letters, no words, no labels, no symbols, no compass, no border, no frame")
SEMTXT = ", no readable writing, no letters anywhere, no signs, no boards"
SEMBAND = ", no flags"
# Respeito (brief): indígenas e africanos escravizados com dignidade, sem caricatura, sem cocar de filme, sem exagero de traços.
INDIG = "Indigenous Tupi people drawn with dignity as round-white-head cartoon people with straight black bowl-cut hair, simple red and black body paint and small bead necklaces, no feather headbands, no caricature"
AFRO = "enslaved African men and women drawn with dignity as round-white-head cartoon people with short curly black hair and simple plain clothes, no caricature"
# Personagens (regra da bíblia: nada de rosto descrito; "round-white-head cartoon …"; figuras modernas sem nome no prompt)
CABRAL = "a round-white-head cartoon Portuguese captain with a simple flat dark beard shape, a black velvet cap and a dark 1500s doublet"
CAMINHA = "a round-white-head cartoon Portuguese scribe with a simple flat grey beard shape, a dark cap and a quill pen"
NASSAU = "a round-white-head cartoon Dutch count with long curly hair, a small simple mustache shape, a black 1600s outfit with a wide white lace collar"
ZUMBI = "a strong round-white-head cartoon Afro-Brazilian quilombo leader with short curly black hair, simple cloth clothes and a spear, standing proud"
BANDEIRANTE = "a round-white-head cartoon Portuguese colonial explorer with a simple flat beard shape, a wide floppy hat, a padded leather jerkin and a musket"
TIRADENTES = "a round-white-head cartoon colonial militia officer with a simple flat long brown beard shape and long brown hair, a plain white shirt"
JOAO = "a chubby round-white-head cartoon Portuguese prince regent with a white tied-back wig, a dark blue coat with gold epaulettes and a red sash"
MARIA = "an old round-white-head cartoon queen with messy grey hair, a small crown and a black dress, looking confused"
PEDRO1 = "a young round-white-head cartoon prince with simple flat dark sideburn shapes and curly dark hair, a dark green and gold military uniform"
PEDRO2 = "an old round-white-head cartoon emperor with a simple flat long white beard shape and a plain black frock coat"
PEDRO2_KID = "a five-year-old round-white-head cartoon boy emperor in a tiny green and gold uniform, sitting on a very big throne"
ISABEL = "a round-white-head cartoon princess with dark hair in a bun and an elegant light 1880s dress"
GETULIO = "a short round-white-head cartoon politician with slicked-back dark hair, a cigar and a light 1930s suit"
JK = "a smiling round-white-head cartoon politician with combed dark hair and a grey 1950s suit"
GENERAL = "a round-white-head cartoon general with dark sunglasses, a military cap and an olive green uniform with medals"
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes"

# ───────────────────────── HOOK (a lista de carga da nau Bretoa, 1511) ─────────────────────────
cap("Hook")
b("[serious] Portugal, mil quinhentos e onze. Um navio chamado Bretoa volta de uma terra nova, do outro lado do Atlântico. E alguém anota tudo o que vem no porão.",
  "bretoa_arrive|A Portuguese carrack ship with white sails with red crosses arriving at the port of Lisbon in 1511, old houses and towers on the hills, seagulls, morning light",
  "clerk_list|A round-white-head cartoon Portuguese clerk with a quill pen writing a long list on a long scroll at a wooden desk on a busy dock, crates around him" + SEMTXT,
  "hold_dark|Inside the dark wooden hold of an old ship, lantern light, piles of red logs and cages",
  "lisbon_dock_crowd|A crowd of curious Lisbon merchants, ladies and children gathering on the dock around a newly arrived ship in 1511, pointing at the cargo",
  "atlantic_cross|An old Portuguese carrack ship sailing alone across a vast blue Atlantic ocean, big waves, wide view", card="1511")
b("[curious] O que tem lá dentro? Cinco mil toras de uma madeira vermelha, com papagaios, saguis e macacos espremidos no meio.",
  "red_logs|Thousands of heavy logs of red brazilwood stacked on a dock, the cut ends glowing deep red like embers",
  "parrots_cage|Colorful green and red parrots in wooden cages on a ship deck, sailors pointing at them, comic",
  "marmosets|Tiny cute marmoset monkeys peeking out of a wooden crate on a dock, surprised Portuguese sailors")
b("[serious] E tem gente também: dezenas de indígenas escravizados, a maioria mulheres.",
  f"captives_ship|{INDIG.replace('people', 'women and a few men')}, sitting sad and chained on the deck of a Portuguese ship at sea, the coast of their land far behind, sorrowful and respectful",
  "coast_behind|View from the stern of an old ship of a green tropical coast with palm trees and mountains slowly disappearing on the horizon, melancholic")
b("Essa é uma das primeiras vezes que o nome Brasil aparece num documento. E sabe onde ele aparece? [amazed] Numa lista de carga.",
  "old_document|An old yellowed sixteenth-century document with lines of handwriting-like squiggles on a wooden table under candlelight, a quill beside it" + SEMTXT,
  "name_brasil|Close view of a medieval-looking ship logbook page with a small drawing of a red log at the margin, warm candlelight" + SEMTXT,
  "scroll_cargo|A long paper scroll unrolling across a ship deck, with small drawings of logs, parrots, monkeys and tiny people on it like an inventory, symbolic" + SEMTXT,
  "map_coast_1511|Map of the Atlantic Ocean with the coast of Portugal in the upper right and the green coast of South America on the left, a dotted ship route between them, " + MAPA)
b("§ Depois da madeira, vieram o açúcar, o ouro, o café e a borracha, e cada riqueza que saía num navio deixava para trás um país diferente.",
  "sugar_cane|A field of tall green sugar cane under a tropical sun with a white colonial mill house in the background",
  "gold_pan|A colonial miner washing a wooden pan in a mountain river, gold flakes shining in the pan",
  "coffee_beans|Red coffee cherries on green coffee plants on rolling hills, sacks of coffee in front",
  "rubber_tree|A rubber tree in the Amazon rainforest with white latex dripping into a small cup, misty jungle",
  "ships_parade|A line of ships of different ages sailing away from a tropical coast: a carrack, a galleon, a steamship and a modern cargo ship, symbolic")
b("§ [serious] Essa é a história inteira do Brasil: como a terra que nasceu numa lista de carga virou um país de mais de duzentos milhões de pessoas.",
  "brazil_today|Aerial view of Rio de Janeiro today with Sugarloaf Mountain, beaches and the city between green mountains, sunny day",
  "crowd_today|A huge happy diverse crowd of Brazilian people of every color in a sunny street today, families, kids, elders, all as round-white-head cartoon people",
  "map_brazil_big|Map of South America with the huge territory of Brazil painted in green and gold, the neighboring countries pale, the ocean blue, " + MAPA,
  "sao_paulo_today|Aerial view of the huge city of São Paulo today with endless skyscrapers to the horizon, dusk",
  "amazon_wide|A wide view of the Amazon river winding through endless green rainforest at sunrise, mist rising")
b("No caminho: um rei fugindo de Napoleão, um imperador enterrado com terra do Brasil… e uma capital erguida do zero em menos de quatro anos.",
  f"king_flee|{JOAO}, hurrying up a gangplank onto a ship with treasure chests, French soldiers tiny on the hills behind, comic panic",
  f"pedro_soil|{PEDRO2}, holding a small cloth pillow filled with red Brazilian earth close to his chest, sad and tender",
  "brasilia_build|Workers and cranes building modern white concrete buildings in an empty red-dirt savanna in 1958, a big blue sky",
  "brasilia_plane|Aerial view of Brasília shaped like an airplane, modern white buildings and a long green esplanade, red earth around",
  "pedro2_ship_dawn|A small ship leaving a tropical bay at dawn with an old bearded man on the deck looking back, sad")
b("§ E, em cada capítulo, a pergunta vai ser a mesma: o que vai no navio… e o que fica aqui? Guarde essa lista de carga, porque ela volta no final.",
  "ship_vs_land|Split view: on the left a ship sailing away full of cargo, on the right a village of people on the beach watching it go, symbolic",
  "scale_ship|A big golden balance scale with a ship on one side and a small village with people on the other side, symbolic",
  "keep_list|A rolled old paper scroll tied with a red ribbon placed in a wooden chest on a ship, a hand closing the lid, symbolic" + SEMTXT,
  "horizon_ship|A single old sailing ship on the horizon at sunset seen from a tropical beach with palm trees, calm and mysterious")

# ───────────────────────── 1. ANTES DO NOME ─────────────────────────
cap("1. Uma terra que já tinha dono")
b("Mas, muito antes de qualquer navio, essa terra já tinha gente. Milhões de pessoas, de centenas de povos diferentes.",
  "forest_village|A large Indigenous village in a clearing of the Amazon forest seen from above, round houses with palm-thatched roofs around a central plaza, smoke rising",
  "many_peoples|Many different Indigenous peoples of the Brazilian lands, from the forest, the coast and the savanna, standing together, drawn with dignity as round-white-head cartoon people with different simple body paints and adornments, no caricature",
  "river_canoes|Indigenous people paddling long wooden canoes on a wide calm Amazon river at sunset, drawn with dignity, no caricature",
  "aerial_forest|Aerial view of endless green Atlantic forest meeting a white beach and the ocean, no people, pristine, 1400s", card="c. 1000")
b("Na ilha de Marajó, um povo ergueu morros de terra para escapar das cheias e fez uma das cerâmicas mais sofisticadas das Américas.",
  "marajo_mounds|Artificial earth mounds rising above a flooded plain on Marajó island, with villages of thatched houses on top, ancient Amazon",
  "marajo_pottery|Close view of a big ancient Marajoara ceramic funeral urn with intricate red, white and black geometric patterns and a stylized face shape, museum light" + SEMTXT,
  "potter|An ancient Indigenous potter woman painting fine geometric lines on a big clay vase, drawn with dignity, warm light@@MARAJOARA",
  "marajo_flood|The flooded plains of Marajó island in the rainy season with houses on top of earth mounds and canoes between them", card="400–1400")
b("§ E a floresta? Parte dela foi cultivada. Arqueólogos acham na Amazônia uma terra preta, feita por gente, e aldeias ligadas por estradas.",
  "terra_preta|Archaeologists kneeling in a dig in the Amazon rainforest holding a handful of rich black soil, broken pottery pieces in the dirt, amazed",
  "ancient_roads|Aerial view of ancient Amazon villages connected by straight raised roads through the forest, imagined reconstruction",
  "forest_garden|Indigenous people tending fruit trees and palms in the middle of the rainforest, a garden forest, drawn with dignity",
  "black_soil_hands|Close view of hands holding rich dark black soil next to pale yellow ordinary soil, comparison, symbolic")
b("No litoral viviam os povos tupis, com roças de mandioca, canoas e guerras entre vizinhos.",
  f"tupi_village|A Tupi village on the Brazilian coast with long palm-thatched houses inside a wooden palisade, the sea and palm trees behind, {INDIG}",
  "manioc|Indigenous women harvesting manioc roots in a garden and grating them, drawn with dignity, no caricature",
  "tupi_war|Two groups of Tupi warriors with bows and wooden clubs facing each other on a beach, drawn with dignity, no caricature")
b("Muita palavra que você fala vem deles: mandioca, jacaré, pipoca… até Ipanema.",
  "popcorn|A clay pot full of popping popcorn over a fire in an Indigenous village, kids laughing, comic",
  "caiman|A big friendly cartoon caiman lying on a river bank with its mouth open, birds on its back",
  "ipanema|Ipanema beach in Rio de Janeiro today with the twin peaks of Dois Irmãos mountain, people on the sand")
b("§ Do outro lado do mar, em mil quatrocentos e noventa e quatro, Portugal e Espanha riscaram uma linha no mapa e dividiram o mundo. Ninguém perguntou a quem morava aqui. Guarde essa linha.",
  "tordesilhas_table|A round-white-head cartoon Portuguese king and a Spanish king leaning over a big blank globe on a table, drawing a line down the middle with a ruler, comic" + SEMTXT,
  "pope_globe|A round-white-head cartoon pope in white robes blessing a big globe while two ambassadors argue next to it, comic" + SEMTXT,
  "map_tordesilhas|Map of the Atlantic with South America on the left, a straight vertical red line cutting through the eastern bulge of South America from north to south, " + MAPA,
  "line_village|A Tupi village on the beach going about daily life, totally unaware of a giant red dotted line drawn across the sky above it, comic and symbolic", card="1494")

# ───────────────────────── 2. UMA TERRA COM NOME DE ÁRVORE ─────────────────────────
cap("2. Uma terra com nome de árvore")
b("Em abril de mil e quinhentos, a frota de Pedro Álvares Cabral, a caminho da Índia, avistou um monte no sul da Bahia.",
  "cabral_fleet|A fleet of thirteen Portuguese ships with white sails and red crosses on a blue ocean, a green mountain on the horizon",
  f"cabral|{CABRAL}, looking through a spyglass on the deck of a ship, pointing at land@@PEDRO ÁLVARES CABRAL",
  "sailors_land|Portuguese sailors climbing the masts and shouting with joy at the sight of land, birds flying around the ship",
  "monte_pascoal|A round green mountain rising behind a tropical beach with palm trees, seen from the sea", card="1500")
b("O escrivão Pero Vaz de Caminha escreveu ao rei sobre a gente e a terra. Aquela frase, em se plantando, tudo dá? Ele nunca escreveu desse jeito.",
  f"caminha|{CAMINHA}, writing a long letter on the deck of a ship by lamplight" + SEMTXT + "@@PERO VAZ DE CAMINHA",
  "plant_myth|A cartoon seed falling into fertile earth and instantly growing into a huge tree full of every kind of fruit, ironic, comic, dreamlike",
  f"first_meet|Portuguese sailors in a rowing boat meeting {INDIG} on a beach, curious on both sides, exchanging a hat and a feather headdress, peaceful",
  "letter_king|A round-white-head cartoon Portuguese king in Lisbon reading a long letter with wide eyes at his throne" + SEMTXT)
b("§ Ouro, ninguém achou. Mas havia uma árvore de madeira vermelha cor de brasa, que dava tinta: o pau-brasil. E a terra ficou com o nome da madeira.",
  "brazilwood_tree|A tall brazilwood tree with yellow flowers in the Atlantic forest, its cut trunk showing deep red wood",
  "red_dye|European dyers dipping cloth into a big vat of deep red dye in a workshop, the cloth coming out bright red",
  "name_glow|A log of red brazilwood glowing like an ember on a beach, symbolic, warm light",
  "cut_trunk|Close view of a freshly cut brazilwood trunk showing its bright red-orange heartwood, wood chips on the ground")
b("Os tupis cortavam e levavam as toras até os navios, em troca de machados, facas e espelhos.",
  f"barter|{INDIG}, carrying heavy red logs to the beach while Portuguese sailors hand them metal axes and small mirrors",
  "axes_mirrors|Metal axes, knives and small round mirrors spread on a cloth on the sand, trade goods",
  "logs_beach|Long rows of red logs piled on a tropical beach waiting for a ship anchored offshore, Tupi carriers and Portuguese sailors around")
b("Quem vivia desse comércio, diz a explicação mais aceita, era chamado de brasileiro: nome de ofício, como ferreiro ou marinheiro.",
  "brasileiro_job|A round-white-head cartoon Portuguese trader with a hat counting red logs with a notebook next to a blacksmith at his anvil and a sailor with a rope, three workers side by side, comic",
  "bretoa_arrive#detalhe-centro", card="1511")
b("§ Para segurar a terra, a Coroa a fatiou em capitanias e, em mil quinhentos e quarenta e nove, mandou um governador-geral, que fundou Salvador.",
  "map_capitanias|Map of the Brazilian coast cut into many horizontal stripes of different pastel colors from the coast to the interior, " + MAPA,
  "salvador_1549|The founding of the colonial town of Salvador in 1549 on a hill above a big bay, Portuguese soldiers and Jesuit priests building walls and a church", card="1549")
b("Os franceses também queriam pau-brasil e chegaram a fundar uma colônia na baía de Guanabara.",
  "french_ships|French 1550s sailing ships with plain white sails anchored in a big bay surrounded by green mountains and a sugarloaf rock, French soldiers in 1550s armor on the beach, no flags",
  "guanabara_fort|A small 1550s wooden and stone fort on an island in a tropical bay, cannons pointing at the sea, no flags, no banners", card="1555")
b("Os portugueses responderam com uma vila-fortaleza, em mil quinhentos e sessenta e cinco, e expulsaram os franceses. A vila era o Rio de Janeiro.",
  "rio_founding|Portuguese soldiers building a wooden fortress village at the foot of the Sugarloaf mountain in 1565, ships in the bay@@RIO DE JANEIRO",
  "french_out|1560s sailing ships with plain sails leaving a tropical bay while Portuguese soldiers in helmets cheer on the beach, comic, no flags, no banners", card="1565")
b("§ Mas madeira dava pouco. Para encher os navios de verdade, Portugal precisava de outra coisa. E achou uma bem doce.",
  "empty_ship|An almost empty ship hold with just a few red logs, a Portuguese merchant scratching his head, comic",
  "sugar_cube|A big shiny cube of white sugar glowing on a dark table like a treasure, symbolic")

# ───────────────────────── 3. O AÇÚCAR E AS CORRENTES ─────────────────────────
cap("3. O doce que custou caro")
b("No litoral de Pernambuco e da Bahia nasceram os engenhos. No fim do século dezesseis, o Brasil era o maior produtor de açúcar do mundo.",
  "engenho|A colonial sugar mill in northeastern Brazil: a big white master house, a chapel, a water wheel mill and green cane fields to the horizon@@ENGENHO",
  "sugar_loaves|Cone-shaped sugar loaves stacked in wooden crates on a dock, ready to be shipped to Europe", card="1580")
b("Só que um engenho engolia gente: cortar a cana, moer, ferver o caldo noite adentro.",
  f"cane_cut|{AFRO}, cutting tall sugar cane under a burning sun, a Portuguese overseer on a horse watching, heavy and sad",
  "boiling_house|Inside a hot colonial sugar boiling house at night, big copper kettles steaming, exhausted workers stirring with long paddles, firelight")
b("Primeiro, escravizaram indígenas. Epidemias, guerras e trabalho forçado mataram boa parte dos povos do litoral.",
  "epidemic|A sad empty Tupi village with abandoned houses, a few sick people lying in hammocks, grey sky, respectful",
  "jesuit_village|Jesuit priests in black robes teaching Indigenous people in front of a small colonial church in a mission village")
b("§ Então Portugal se voltou para a África. E aqui vale parar num número.",
  "map_atlantic_slave|Map of the South Atlantic with the coast of West and Central Africa on the right and the coast of Brazil on the left, many thin dark arrows crossing from Africa to Brazil, " + MAPA,
  "slave_ship|A dark sailing ship crossing the ocean under a stormy sky, heavy and ominous")
b("[serious] Quase cinco milhões de africanos escravizados chegaram vivos ao Brasil. Quase metade de todos os que desembarcaram nas Américas. Nenhum lugar recebeu mais.",
  f"arrival_port|{AFRO}, arriving on a colonial dock in Salvador after the crossing, exhausted, families holding each other, respectful and sad",
  "five_million|A huge crowd of tiny people drawn as small dots and figures filling a whole map of the Atlantic, symbolic, sombre colors@@QUASE 5 MILHÕES")
b("Para comparar: os Estados Unidos receberam menos de meio milhão. E centenas de milhares morreram na travessia. Guarde esse número.",
  "compare_bars|Two piles of sand side by side on a wooden table, one enormous and one very small, symbolic, sombre light" + SEMTXT,
  "sea_memorial|White flowers floating on dark ocean waves at dusk, a memorial, quiet and respectful")
b("§ Todo esse açúcar atraiu os holandeses. Em mil seiscentos e trinta, eles tomaram Pernambuco e ficaram quase vinte e cinco anos.",
  "dutch_attack|Dutch warships with orange, white and blue striped flags attacking a colonial Brazilian port town, cannon smoke",
  "map_dutch|Map of the northeastern bulge of Brazil with the coastal area painted orange, the rest of the land pale green, " + MAPA, card="1630")
b("Com Maurício de Nassau, Recife ganhou pontes, um observatório e a primeira sinagoga das Américas.",
  f"nassau|{NASSAU}, proudly showing a new wooden bridge over a river in colonial Recife with Dutch-style houses@@MAURÍCIO DE NASSAU",
  "synagogue|A small 1600s synagogue building in colonial Recife with people entering on a sunny street" + SEMTXT,
  "observatory|A small rooftop astronomical observatory on a Dutch colonial house in Recife at night, a man with a telescope looking at the stars")
b("Até que senhores de engenho, indígenas e soldados negros lutaram juntos e expulsaram os holandeses, em mil seiscentos e cinquenta e quatro.",
  "guararapes|A battle on green hills: Portuguese-Brazilian planters, Indigenous warriors and Black soldiers fighting side by side against Dutch soldiers, dynamic" + SEMBAND,
  "dutch_leave|Dutch ships leaving the harbor of Recife while people celebrate on the docks", card="1654")
b("Só que os holandeses levaram o segredo do açúcar para o Caribe. O preço despencou, e Portugal precisou de outra riqueza.",
  "caribbean_sugar|Dutch merchants setting up new sugar mills on a Caribbean island with turquoise sea and palm trees",
  "price_drop|A Portuguese merchant fainting next to a pile of unsold sugar loaves on a dock, comic")

# ───────────────────────── 4. A FEBRE DO OURO ─────────────────────────
cap("4. A febre do ouro")
b("Enquanto isso, nas serras de Alagoas, escravizados fugidos tinham erguido Palmares, um quilombo que resistiu por quase um século.",
  "palmares|A large free quilombo village of thatched houses on green hills behind a wooden palisade, people farming and children playing, peaceful, drawn with dignity@@PALMARES",
  "quilombo_defend|Quilombo defenders with spears and bows on a palisade watching a colonial army approach in the valley, determined, drawn with dignity")
b("Seu último grande líder, Zumbi, foi morto em vinte de novembro de mil seiscentos e noventa e cinco. Hoje, esse dia é feriado nacional: o Dia da Consciência Negra.",
  f"zumbi|{ZUMBI} on a hill above Palmares at sunset@@ZUMBI DOS PALMARES",
  "consciencia_today|A modern street celebration in Brazil on Black Awareness Day, people of African descent dancing and drumming, joyful, drawn with dignity" + SEMTXT, card="1695")
b("§ E, quase nos mesmos anos, bandeirantes paulistas, que entravam no sertão caçando indígenas e riquezas, acharam ouro em Minas Gerais.",
  f"bandeirantes|{BANDEIRANTE}, leading a column of men with muskets through a dense forest and a river@@BANDEIRANTES",
  "gold_found|A colonial explorer kneeling in a mountain stream holding up a shining gold nugget, his men running toward him, amazed",
  "minas_hills|Green rolling mountains of Minas Gerais with a river and miners working in the water, misty morning", card="c. 1695")
b("Lembra da linha de Tordesilhas? Os bandeirantes passaram por cima dela. Em mil setecentos e cinquenta, a Espanha aceitou: o Brasil já tinha quase o formato de hoje.",
  "map_tordesilhas#detalhe-centro",
  "map_brazil_1750|Map of South America with the large territory of Brazil painted in green almost in its modern shape, a faint old vertical line far to the east, " + MAPA, card="1750")
b("Tanta gente correu para as minas que a Coroa tentou limitar a saída de Portugal.",
  "gold_rush|Crowds of people with mules, sacks and pans walking up a mountain trail toward gold mines, chaotic and busy",
  "lisbon_empty|A Portuguese official in Lisbon looking at a nearly empty village street with a few old people, comic")
b("Vila Rica, hoje Ouro Preto, se encheu de igrejas forradas de ouro, muitas com esculturas do Aleijadinho.",
  "ouro_preto|The colonial town of Ouro Preto with baroque churches with white walls and twin towers on green hills, cobbled streets@@OURO PRETO",
  "gold_church|Inside a baroque church covered in golden carved wood, light coming through the windows, sparkling")
b("§ Mas o ouro também ia embora. A Coroa ficava com um quinto de tudo, e muito desse ouro seguia de Lisboa para a Inglaterra, para pagar tecidos.",
  "quinto|A Portuguese tax collector weighing gold on a scale and taking one fifth into a chest with the royal coat of arms, miners watching unhappy" + SEMTXT,
  "gold_to_england|Chests of gold being loaded from a Lisbon dock onto an English ship, English merchants with bolts of wool cloth, comic")
b("§ Quando o ouro foi minguando, a Coroa ameaçou cobrar os impostos atrasados à força. E, em Minas, um grupo começou a sonhar com uma república.",
  "conspiracy|Colonial men in tricorn hats whispering around a candle in a dark room in Vila Rica, plotting, a map on the table" + SEMTXT, card="1789")
b("Foram traídos. Só um foi enforcado: um alferes que também arrancava dentes, o Tiradentes. Hoje, o dia dele também é feriado.",
  f"tiradentes|{TIRADENTES}, pulling a tooth from a grimacing patient with pliers, comic@@TIRADENTES",
  "tiradentes_end|An empty wooden gallows on a colonial square in Rio de Janeiro at dawn, a crowd leaving, quiet and sad", card="1792")

# ───────────────────────── 5. O REI QUE CHEGOU FUGINDO ─────────────────────────
cap("5. O rei que chegou fugindo")
b("Em novembro de mil oitocentos e sete, o exército de Napoleão marchava sobre Lisboa. E a família real portuguesa fez o que nenhuma outra tinha feito.",
  "napoleon_march|French soldiers of Napoleon in blue uniforms and tall hats marching on a country road, cannons, dust" + SEMTXT + SEMBAND,
  f"joao_worried|{JOAO}, biting his nails in a palace window while a messenger brings bad news", card="1807")
b("Fugiu. Entre dez e quinze mil pessoas embarcaram com o tesouro, os arquivos e a biblioteca real.",
  "lisbon_embark|Chaotic Lisbon dock with nobles, servants, chests, paintings and books being loaded onto many ships in the rain, comic panic",
  "books_crates|Crates full of old books and rolled documents being carried onto a ship by sweating servants, comic")
b("Conta-se que a velha rainha, Maria, a Louca, gritava pelo caminho: não corram tanto, vão pensar que estamos fugindo.",
  f"maria_carriage|{MARIA}, leaning out of a rushing horse carriage and shouting at the driver, comic@@D. MARIA I")
b("§ Em mil oitocentos e oito, o Rio de Janeiro virou a capital de um império europeu. É o único caso conhecido de uma metrópole governada de dentro da sua colônia.",
  "rio_1808|The colonial port of Rio de Janeiro in 1808 with ships arriving, crowds on the docks and green mountains behind",
  f"joao_arrives|{JOAO}, stepping off a boat onto a Rio dock under palm trees, sweating in the heat, a crowd bowing", card="1808")
b("Para abrigar a corte, casas eram marcadas com duas letras: PR, de Príncipe Regente. O povo lia: ponha-se na rua.",
  "pr_door|A colonial house door in Rio being marked with two big white painted letters P R by an official, the owner family shocked behind",
  "kicked_out|A Brazilian family carrying their furniture out into the street while Portuguese nobles move into their house, comic")
b("§ E repare: pela primeira vez, o navio veio no sentido contrário. Em vez de levar a riqueza, trouxe o governo.",
  "ship_reverse|An old Portuguese ship arriving at a tropical port carrying a throne, a crown and royal chests instead of taking cargo away, symbolic, comic",
  "map_reverse|Map of the Atlantic Ocean with a big golden arrow going from Portugal in the upper right to Rio de Janeiro on the coast of Brazil, " + MAPA)
b("Em poucos meses, a colônia ganhou portos abertos ao mundo, um banco, uma imprensa e um jardim botânico.",
  "open_ports|British and American merchant ships crowding the port of Rio, merchants unloading goods",
  "botanical_rio|The Rio de Janeiro botanical garden with a long avenue of tall royal palm trees, visitors walking")
b("Dom João gostou tanto que ficou treze anos, muito depois da queda de Napoleão.",
  f"joao_happy|{JOAO}, lying in a hammock under a palm tree eating a chicken leg, very happy, comic")
b("§ Em mil oitocentos e vinte e um, ele voltou para Lisboa e deixou aqui o filho, Pedro. Diz a tradição que o conselho foi: se o Brasil se separar, que seja com você, antes que algum aventureiro fique com ele. Guarde esse conselho.",
  f"joao_leaves|{JOAO}, crying while hugging {PEDRO1} on a dock before boarding a ship",
  f"advice|{JOAO}, whispering into the ear of {PEDRO1}, pointing at a crown on a cushion, secretive", card="1821")

# ───────────────────────── 6. UM IMPÉRIO EM FAMÍLIA ─────────────────────────
cap("6. Um império em família")
b("Em Lisboa, as Cortes quiseram fazer o Brasil voltar a ser colônia e mandaram Pedro voltar para casa.",
  "cortes_lisbon|Angry Portuguese deputies in 1820s coats shouting in a parliament hall in Lisbon, waving papers",
  f"pedro_letter|{PEDRO1}, reading an official letter with a frown, getting angry")
b("Em sete de setembro de mil oitocentos e vinte e dois, perto do riacho do Ipiranga, ele leu as cartas e rompeu com Portugal: Independência ou morte.",
  f"ipiranga_painting|{PEDRO1}, on a horse on a hill raising a sword in the air, guards cheering, heroic painting style, by a small stream@@IPIRANGA",
  "ipiranga_stream|A small stream with grass and trees on a hill near São Paulo in 1822, a road with a few riders", card="1822")
b("Esse é o quadro. Pelos relatos, ele estava numa mula, e com uma dor de barriga daquelas.",
  f"pedro_mule|{PEDRO1}, riding a small grumpy mule and holding his belly with a pained face, comic",
  "mule_close|A grumpy small mule chewing grass on a dusty road, comic")
b("§ Lembra do conselho do pai? Pedro seguiu à risca: o Brasil ficou independente… com o herdeiro do rei de Portugal como imperador.",
  f"pedro_crowned|{PEDRO1}, being crowned emperor in a church, wearing a big green and gold cape, proud",
  f"joao_far|{JOAO}, in Lisbon reading a letter and smiling slyly, comic")
b("E, enquanto a América espanhola se partia em várias repúblicas, o Brasil continuou um só. Ou quase: no sul, perdeu uma guerra, e a Cisplatina virou o Uruguai.",
  "map_south_america|Map of South America divided into many colored countries with the huge Brazil in one single green color, " + MAPA,
  "map_uruguay|Map of southern Brazil and the Río de la Plata with a small area south of Brazil highlighted in light blue, " + MAPA, card="1828")
b("§ Pedro durou pouco. Em mil oitocentos e trinta e um, abdicou e foi lutar pelo trono da filha em Portugal. Deixou aqui o herdeiro… de cinco anos.",
  f"pedro_leaves|{PEDRO1}, waving goodbye from a ship leaving Rio",
  f"boy_emperor|{PEDRO2_KID}, looking around lost while adults bow@@D. PEDRO II", card="1831")
b("Depois de anos de revoltas, do Pará ao Rio Grande do Sul, os políticos declararam o menino maior de idade, aos catorze anos.",
  "revolts|Rebels on horseback in the southern Brazilian plains with gaucho hats and ponchos charging, dust" + SEMBAND,
  "boy_adult|A fourteen-year-old round-white-head cartoon boy emperor being handed a crown by old politicians who are measuring his height with a ruler, comic", card="1840")
b("E o Brasil teve, por quase cinquenta anos, um imperador que preferia os livros.",
  f"pedro_books|{PEDRO2.replace('old ', 'middle-aged ').replace('long white', 'dark brown')}, sitting in a huge library surrounded by stacks of books and a telescope" + SEMTXT)

# ───────────────────────── 7. O CAFÉ, A GUERRA E A LEI ÁUREA ─────────────────────────
cap("7. Café, guerra e liberdade")
b("Mas o império rodava sobre outra riqueza: o café. Primeiro no vale do Paraíba, depois em São Paulo, o grão encheu os navios.",
  "coffee_farm|A big coffee plantation in the Paraíba valley in the 1850s with a white manor house, endless rows of coffee bushes on the hills",
  "coffee_ships|Sacks of coffee being loaded onto steamships at the port of Santos, busy dock workers", card="1850")
b("E o café, como o açúcar, era colhido por gente escravizada. Em mil oitocentos e cinquenta, sob pressão inglesa, o Brasil proibiu o tráfico. A escravidão, não.",
  f"coffee_slaves|{AFRO}, harvesting red coffee cherries into baskets on a hillside plantation, an overseer watching, heavy and respectful",
  "british_ship|A British navy warship stopping a slave ship at sea, sailors with telescopes")
b("§ Então veio a guerra mais sangrenta da América do Sul: Brasil, Argentina e Uruguai contra o Paraguai, por mais de cinco anos.",
  "paraguay_war|A big 1860s battle in a swampy plain with soldiers in uniforms, cannons and smoke, rivers and palm trees" + SEMBAND,
  "map_paraguay|Map of the center of South America with Paraguay highlighted in red between Brazil, Argentina and Bolivia, rivers in blue, " + MAPA, card="1864")
b("O Paraguai perdeu boa parte da sua gente. E o Brasil voltou com um exército grande, orgulhoso… e com opinião política.",
  "army_return|Brazilian army officers in 1870 uniforms parading proudly through Rio, mustaches, medals" + SEMBAND,
  "officers_talk|Army officers in 1880s uniforms arguing about politics in a smoky café, newspapers on the table" + SEMTXT)
b("Na Filadélfia, o imperador pegou o telefone novo de Graham Bell e, conta-se, exclamou: meu Deus, isto fala!",
  f"telephone|{PEDRO2}, holding an early 1876 telephone to his ear with a shocked happy face at a fair, an inventor beside him, comic", card="1876")
b("§ Lembra daquele número, quase cinco milhões? Nos anos de mil oitocentos e oitenta, o Brasil era o último país das Américas com escravidão.",
  "map_americas_last|Map of North and South America with all countries pale grey except Brazil painted dark, " + MAPA,
  "abolition_rally|A big crowd of abolitionists, Black and white, gathering in a Rio street in the 1880s, hopeful" + SEMTXT)
b("Em treze de maio de mil oitocentos e oitenta e oito, a princesa Isabel assinou a Lei Áurea. Dois artigos: a escravidão estava extinta.",
  f"isabel_signs|{ISABEL}, signing a short document with a golden pen at a desk in a palace, people watching" + SEMTXT + "@@LEI ÁUREA",
  "freedom_party|People celebrating freedom in the streets of Rio on May 13 1888, hats in the air, flowers, drawn with dignity" + SEMBAND + SEMTXT, card="1888")
b("[serious] E só. Nenhuma terra, nenhuma escola, nenhuma ajuda para quem foi libertado.",
  "freed_road|A freed family walking alone on a long dusty road with a small bundle, no house in sight, sunset, quiet and respectful",
  "empty_hands|Close view of open empty hands of a Black worker, symbolic, quiet light")
b("§ Os fazendeiros ficaram furiosos com a monarquia. O exército também. Um ano e meio depois, militares derrubaram o imperador, quase sem um tiro.",
  "farmers_angry|Angry coffee farmers in top hats shouting in a meeting room, comic",
  "republic_coup|Army officers on horseback in a square in Rio in 1889 announcing a new government, soldiers lined up, calm, almost no fighting" + SEMBAND, card="1889")
b("A família imperial foi posta num navio de madrugada. Dom Pedro morreu em Paris, dois anos depois, com um travesseiro de terra do Brasil no caixão.",
  "night_ship|A small ship leaving the bay of Rio de Janeiro at dawn with a family on deck looking back, sad",
  "pedro_soil", card="1891")

# ───────────────────────── 8. A REPÚBLICA DO CAFÉ COM LEITE ─────────────────────────
cap("8. A república do café com leite")
b("A república nova era, na prática, do café. Por volta de mil e novecentos, o Brasil produzia mais da metade do café do mundo.",
  "coffee_world|A giant pile of coffee sacks dwarfing tiny ships around it in the port of Santos, symbolic, comic",
  "barons|Rich coffee barons in white suits and hats counting money on a veranda of a mansion in São Paulo", card="1900")
b("São Paulo, do café, e Minas, do leite, se revezavam na presidência. O povo chamou de política do café com leite.",
  "cafe_com_leite|A coffee cup and a milk jug cartoon characters taking turns sitting on a presidential chair, comic" + SEMTXT,
  "election_old|Men in 1900s hats voting out loud in front of a local boss with a big mustache, comic" + SEMTXT)
b("§ No sertão da Bahia, o exército arrasou Canudos, um arraial de sertanejos pobres, depois de três expedições derrotadas.",
  "canudos|A large village of mud houses in the dry backlands of Bahia with a church in the middle, poor sertanejos, cacti@@CANUDOS",
  "canudos_war|Soldiers with rifles and cannons on dry hills in front of a burning backlands village, sad", card="1897")
b("Para colher o café sem escravidão, vieram milhões de imigrantes: italianos, portugueses, espanhóis e, a partir de mil novecentos e oito, japoneses.",
  "immigrant_ship|A steamship full of European immigrants with suitcases arriving at the port of Santos, hopeful faces",
  "japanese_arrive|Japanese immigrant families in 1908 clothes stepping off a ship in Santos, carrying bundles, curious", card="1908")
b("Hoje, o Brasil tem a maior comunidade japonesa fora do Japão.",
  "liberdade|A street in São Paulo today decorated with round red Japanese paper lanterns hanging overhead, shop fronts with plain colored awnings, people walking, festive, no signs, no writing, no letters, no characters anywhere")
b("§ Na Amazônia, a borracha deixou Manaus tão rica que ela ergueu um teatro de ópera no meio da floresta.",
  "manaus_opera|The Manaus opera house with its colorful dome in the middle of the Amazon city, jungle around@@TEATRO AMAZONAS",
  "rubber_tapper|A rubber tapper cutting the bark of a tree in the dark rainforest, white latex dripping")
b("E Henry Ford quis plantar borracha e construiu uma cidadezinha americana na selva: Fordlândia. Quase não saiu borracha.",
  "fordlandia|An American-style small town with white wooden houses, a water tower and a golf course in the middle of the Amazon rainforest, absurd and comic@@FORDLÂNDIA",
  "dead_trees|Rows of sick dying rubber trees with yellow leaves in a plantation, an American manager scratching his head, comic", card="1928")
b("§ Então, em mil novecentos e vinte e nove, a bolsa de Nova York quebrou, e o mundo parou de comprar café.",
  "crash_1929|Panicked stock brokers in 1929 suits and hats running in a New York street, papers flying" + SEMTXT,
  "coffee_burn|Huge piles of coffee sacks burning in an open field in Brazil, black smoke, workers watching", card="1929")
b("O governo chegou a queimar dezenas de milhões de sacas para segurar o preço. E o café com leite azedou.",
  "coffee_sea|Workers dumping coffee beans from a ship into the sea, comic and sad",
  "sour_milk|A coffee cup with sour milk curdling and a sad face drawn on the cup, comic")

# ───────────────────────── 9. DE VARGAS A BRASÍLIA ─────────────────────────
cap("9. O petróleo é nosso")
b("Em mil novecentos e trinta, um gaúcho baixinho, de charuto, chegou ao poder por uma revolução: Getúlio Vargas.",
  f"vargas|{GETULIO}, arriving in Rio on a train with soldiers in gaucho hats cheering@@GETÚLIO VARGAS",
  "horses_obelisk|Gaucho soldiers tying their horses to an obelisk on a big avenue in Rio in 1930, comic" + SEMBAND, card="1930")
b("Deu aos trabalhadores salário mínimo, férias e carteira assinada. E deu ao país censura e polícia política. Em mil novecentos e trinta e sete, virou ditador.",
  "workers_card|Happy factory workers in 1940s clothes holding small blue work booklets, a factory behind them" + SEMTXT,
  "censor|A 1930s censor in a suit cutting pieces out of a newspaper with big scissors, comic" + SEMTXT, card="1937")
b("§ Na Segunda Guerra, esse ditador mandou soldados lutar contra o fascismo na Itália. Diziam que era mais fácil uma cobra fumar… e a tropa pôs no braço uma cobra fumando.",
  "feb_italy|Brazilian soldiers in 1944 green uniforms and helmets marching in the snowy mountains of Italy" + SEMBAND,
  "smoking_snake|A cartoon green snake smoking a pipe on a round shoulder patch, comic badge" + SEMTXT, card="1944")
b("Deposto em quarenta e cinco, voltou eleito e criou a Petrobras, com um lema que resume este vídeo inteiro: o petróleo é nosso.",
  "oil_rally|A big crowd in 1950s Rio marching with banners and oil barrels, cheering" + SEMTXT,
  "oil_drop|A big black drop of oil glowing with green and yellow light, symbolic", card="1953")
b("§ [serious] Em mil novecentos e cinquenta e quatro, pressionado pelos militares, Vargas se matou no palácio do Catete. Deixou uma carta: saio da vida para entrar na história.",
  "catete|A grand old palace in Rio at night with one lit window, quiet and sad, empty street",
  "letter_desk|A folded letter on a dark desk next to a pair of round glasses, quiet light" + SEMTXT, card="1954")
b("§ Dois anos depois, Juscelino Kubitschek prometeu cinquenta anos de progresso em cinco.",
  f"jk|{JK}, waving from an open car to a cheering crowd@@JUSCELINO KUBITSCHEK",
  "car_factory|A new 1950s car factory in São Paulo with shiny cars on the line", card="1956")
b("E construiu uma capital nova, no meio do cerrado, em menos de quatro anos. Brasília foi inaugurada em abril de mil novecentos e sessenta, com forma de avião.",
  "brasilia_build",
  "brasilia_plane@@BRASÍLIA",
  "congress|The modern Brazilian National Congress building with two tall towers and two white bowls, blue sky", card="1960")
b("Era o futuro, feito de concreto… e pago com uma montanha de dívida. Quatro anos depois, os tanques saíram às ruas.",
  "debt_mountain|A huge mountain of paper bills and coins towering over a small modern white city, a banker on top, comic" + SEMTXT,
  "tanks_street|Military tanks rolling down a wide avenue in Rio in 1964, people watching from the sidewalks" + SEMBAND)

# ───────────────────────── 10. TANQUES, INFLAÇÃO E O REAL ─────────────────────────
cap("10. Da ditadura ao real")
b("Em mil novecentos e sessenta e quatro, os militares derrubaram o presidente João Goulart e ficaram vinte e um anos no poder.",
  f"generals|Three round-white-head cartoon generals with dark sunglasses, military caps and medals sitting at a long table, serious",
  f"general|{GENERAL}, standing in front of a plain red curtain giving a speech, no flags", card="1964")
b("O crescimento rápido ganhou nome de milagre econômico. Em setenta, o Brasil foi tricampeão, e o governo fez questão de faturar.",
  "highway|A giant highway being cut through the Amazon rainforest by bulldozers, red dirt and fallen trees",
  "worldcup_1970|Brazilian football fans in yellow shirts celebrating a World Cup win in the streets in 1970, confetti", card="1970")
b("O lema era: Brasil, ame-o ou deixe-o. E houve censura, prisões e tortura de opositores.",
  "prison_dark|A dark prison corridor with closed metal doors, a single light bulb, sombre and quiet",
  "newspaper_censor|A newspaper printing room in the 1970s with a censor in a suit standing over the editors, tense" + SEMTXT)
b("Quando a censura cortava uma notícia, um grande jornal publicava no lugar versos de Camões. Outro, receitas de bolo.",
  "cake_page|A newspaper page with a big drawing of a cake in the middle of the columns, a reader laughing, comic" + SEMTXT,
  "poem_page|An old newspaper with a small drawing of a poet with a laurel crown in the middle of the columns, comic" + SEMTXT)
b("§ Em mil novecentos e oitenta e cinco, a democracia voltou. Mas o presidente eleito, Tancredo Neves, morreu antes de tomar posse. Três anos depois, veio a Constituição que vale até hoje.",
  "diretas_ja|A huge crowd in yellow shirts in a city square in 1984 demanding direct elections, balloons, joyful" + SEMTXT,
  "hospital_vigil|A crowd holding candles at night in front of a hospital, praying, sad", card="1985")
b("§ Aí veio o pesadelo do dinheiro. Em mil novecentos e noventa, um presidente recém-eleito congelou o dinheiro das contas e da poupança por dezoito meses.",
  "frozen_money|A bank vault with piles of money frozen inside a big block of ice, people outside shocked, comic",
  "bank_line|An angry long line of people in front of a closed bank building with closed doors in 1990, comic" + SEMTXT, card="1990")
b("Em noventa e três, os preços subiram mais de dois mil por cento num ano só. No mercado, a maquininha de etiquetas remarcava tudo, todo dia.",
  "price_gun|A supermarket worker with a price label gun relabeling cans on a shelf while a customer cries, comic" + SEMTXT,
  "money_pile|A woman in 1990s clothes carrying a huge stack of banknotes to the counter of a modern 1990s Brazilian bakery with glass display cases to buy one small bread roll, comic" + SEMTXT, card="1993")
b("Em oito anos, o Brasil trocou de moeda cinco vezes. A quinta, o real, deu certo, e está aí até hoje.",
  "five_coins|Five different old Brazilian banknotes in a row, each one fading away except the last green one shining" + SEMTXT,
  "real_coin|Close view of one shiny bimetallic coin, golden center and silver ring, glowing alone on a dark wooden table, no people, symbolic" + SEMTXT, card="1994")
b("§ Desde então, o país teve presidentes de esquerda, de centro e de direita, e dois impeachments. E a democracia seguiu de pé.",
  "voting_booth|Brazilian people of all ages in line to vote with an electronic voting machine in a school, calm and orderly" + SEMTXT,
  "planalto|The modern Brazilian presidential palace with white columns in Brasília at sunset, calm" + SEMBAND)
b("E os navios? O Brasil é hoje o maior exportador do mundo de soja, café, suco de laranja, carne… e de açúcar, de novo.",
  "soy_fields|Endless soybean fields with combine harvesters at sunset in the center of Brazil",
  "cargo_port|A huge modern Brazilian port with giant cargo ships and grain terminals, trucks lined up",
  "orange_juice|Mountains of oranges and big plain orange steel tanks at a modern juice factory, comic" + SEMTXT, card="2025")

# ───────────────────────── FECHO (paga a lista de carga e a palavra "brasileiro") ─────────────────────────
cap("Fecho")
b("§ [warm] Lembra da lista de carga da nau Bretoa? Madeira, bichos… e gente.",
  "old_document",
  "red_logs",
  "scroll_cargo")
b("Quinhentos anos depois, os navios saem cheios de soja, minério e petróleo. E a pergunta continua a mesma: o que vai no navio… e o que fica aqui?",
  "cargo_port",
  "ship_vs_land")
b("Mas uma coisa mudou. Brasileiro já não é o nome de quem carrega a madeira dos outros. É o nome de duzentos e treze milhões de pessoas.",
  "crowd_today",
  "brasileiro_job")
b("Netos de indígenas, de africanos, de portugueses, de imigrantes. Foi isso que ficou.",
  "family_today|A big Brazilian family of mixed ancestry having a Sunday lunch together at a long table in a backyard, laughing, warm light",
  "brazil_today")
b("E você? Qual desses ciclos deixou mais marcas na sua cidade: o açúcar, o ouro, o café, a borracha? Conta aqui nos comentários.",
  f"guide_comment|{GUIA} standing on a beach next to a stack of red brazilwood logs, a sugar loaf, a gold nugget, a coffee sack and a rubber ball, scratching its head, thinking",
  "ships_parade")


# Grafia para a VOZ (o Fish lê como português; aqui quase tudo já é português). Conferir no teste de nomes (qa/pronuncia/).
# blocos.json leva "texto" (falado, vai ao Fish) e "tela" (grafia correta: legendas e SCRIPT).
FALA = [("Kubitschek", "Kubitchéque"), ("Nassau", "Nassáu"), ("Bretoa", "Bretôa"),
        ("Napoleão", "Napoleão"), ("Ipiranga", "Ipiranga"), ("Fordlândia", "Fórdlândia"), 
        ("PR", "pê érre"), ("Camões", "Camões")]
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
