#!/usr/bin/env python3
"""Fonte única do 010-japao (14/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

7º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
1º vídeo com EMBALAGEM antes do roteiro (EMBALAGEM.md + CRIVO.md, aprovado na r2):
  T1 "O Japão COPIAVA todo mundo. Por que ninguém o conquistava?" · T2 "Como o MAR protegeu o Japão (até o dia em que parou)"
  thumb: bonequinho com tocha no muro de pedra + tufão + "SÓ SORTE?" + "1281".
Molde History in Minutes (narrativa contínua). Referência de código: videos/006-roma … 009-alemanha.
  hook: agosto de 1281, "você" no muro de pedra diante da frota de Kublai Khan → tufão → kamikaze → "Foi só sorte?"
  → "esse país vivia copiando os vizinhos" (< 1:00) → PERGUNTA CENTRAL (≤ 0:50) → "o mar era o muro… um dia vai falhar"
  → "Essa é a história inteira do Japão" → 1 "guarde" (o vento, pago em 1944) → era 1.
Fio condutor: A PORTA E O MAR. O mar dá tempo; o Japão escolhe o que entra (ideias sim, quem quer mandar não).
  Peça 1 (era 2): copiava, mas não se ajoelhava (carta de 607). Peça 2 (era 4): o mar dava tempo e o Japão usava esse tempo
  (o muro de 1276; Takashima: navios de rio) = resposta ao "só sorte?". Peça 3 (era 6): deixava entrar ideias e fechava a porta
  quando quem entrava queria mandar (sakoku). Virada (era 7): 1853, "nesse dia, o mar parou de proteger o Japão".
  Era 9: o invasor; 1944 o vento volta no nome dos pilotos; 1945 os americanos chegam pelo mar, 1ª ocupação estrangeira.
  Fecho: "O mar dava tempo. O vento ajudou uma noite. O resto foi escolha… Sorte foi uma noite. O resto foi escolha."
Seriedade: era 9 (1931–45) sem humor, sem imagem gráfica, sem bandeira/sol nascente/insígnia em imagem nenhuma
  (objetos, silhuetas, cidade de longe, relógio parado). Fecha no Japão de hoje com 1 frase neutra (população).

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1281") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006–009).
Imagens: Codex (canal.yaml visual.gerador: codex; fallback nano-banana). Prompts só de conteúdo; o estilo vem do canal.yaml.
  O Codex põe marcos fora de época (anti-padroes §3d): cada cena de época diz o que NÃO pode aparecer.
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (006–009: ~128 ppm com pausas)
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
TITULO = "A história INTEIRA do Japão"
PERGUNTA = "Como um país que copiava todo mundo passou quase setecentos anos sem que ninguém o conquistasse?"
PROMESSA = ("Como um país que copiava tudo de fora passou quase setecentos anos sem que nenhum invasor o conquistasse, "
            "e o que aconteceu quando a porta cedeu (EMBALAGEM.md r2).")
TITULOS = 'T1 "O Japão COPIAVA todo mundo. Por que ninguém o conquistava?" / T2 "Como o MAR protegeu o Japão (até o dia em que parou)"'

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None):
    ideia = t.startswith("§")
    B.append({"t": t.lstrip("§ ").strip(), "s": list(s), "card": card, "ideia": ideia})

# ───────── regras de prompt (Codex/nano-banana) ─────────
MAPA = ("painted like a blank parchment terrain map seen from directly above, only coastlines, seas, rivers, mountains and flat colored areas, "
        "completely blank with no writing anywhere, no letters, no words, no labels, no symbols, no compass, no border, no frame")
SEMTXT = ", no readable writing, no letters anywhere, no signs, no boards"
SEMBAND = ", no flags, no banners with symbols, no letters on sails, shields or banners"
SEMSOL = ", no rising sun flag, no red sun disc anywhere"
ANTIGO = ", prehistoric setting: no castles, no pagodas, no temples, no metal tools, no modern objects"
MEDIEVAL = (", medieval Japan: low wooden buildings with thatched or simple tiled roofs, no stone castles, no tall white castle towers, "
            "no pagodas unless described, no modern objects")
EDOJP = ", Edo period Japan: wooden houses with tiled roofs, no modern objects, no Western buildings"
SANG = ", no blood, no gore"
# 1931–45 e política de anúncios: nenhum símbolo em imagem nenhuma
SEMSIMB = (", absolutely no symbols of any kind, no flags, no rising sun, no red sun discs, no insignia, no emblems, no armbands, "
           "no letters, no blood, no injuries, no violence shown")
# Personagens (regra da bíblia: nada de rosto descrito; "round-white-head cartoon …")
JOMON = "round-white-head cartoon prehistoric Japanese villagers in simple hemp and fur clothes, long black hair tied back"
YAYOI = "round-white-head cartoon ancient Japanese rice farmers of 300 BC in plain hemp tunics, black hair tied in simple knots"
YAMATO = "a round-white-head cartoon ancient Japanese chief of the 5th century in white robes with a bead necklace and a bronze mirror"
COREANO = "round-white-head cartoon Korean monks of the 6th century in grey robes with shaved heads"
SHOTOKU = "a round-white-head cartoon Japanese prince of the 7th century with a simple flat thin mustache shape, a black cap, a long pale robe and a flat wooden scepter"
ENVIADO = "a round-white-head cartoon Japanese envoy of the 7th century in a pale court robe and a black cap, bowing and holding a scroll"
YANG = "a round-white-head cartoon Chinese emperor of the 7th century with a simple flat beard shape, a flat black board crown with hanging bead strings and a yellow dragon robe"
CORTE = ("round-white-head cartoon Japanese court nobles of the Heian period: ladies in many layered colorful silk robes with very long straight black hair, "
         "gentlemen in tall black lacquered caps and wide-sleeved robes")
DAMA = "a round-white-head cartoon Heian court lady with very long straight black hair and twelve layered colorful silk robes"
SAM12 = ("round-white-head cartoon Japanese samurai of the 12th–13th century in simple boxy lamellar armor laced with colored cords, "
         "plain iron helmets without horns or crests, longbows and curved swords")
XOGUM = "a round-white-head cartoon Japanese military ruler of 1192 in a dark court robe and a tall black cap, sitting on a mat with a fan"
IMPERADOR = "a round-white-head cartoon young Japanese emperor of the 12th century in white and orange court robes with a tall black cap"
KUBLAI = "a round-white-head cartoon Mongol emperor with a simple flat thin mustache shape, a round fur-trimmed hat and a golden silk robe"
MONGOIS = "round-white-head cartoon Mongol and Chinese soldiers of the 13th century in padded leather armor and fur-trimmed helmets, with bows and round shields"
PORT = "round-white-head cartoon Portuguese sailors and merchants of 1543 with simple flat beard shapes, puffy breeches, doublets and wide-brimmed hats"
JESUITA = "a round-white-head cartoon Jesuit priest of 1549 with a simple flat dark beard shape, in a plain black cassock, holding a small wooden cross"
NOBUNAGA = "a round-white-head cartoon Japanese warlord of 1575 with a simple flat thin mustache shape, shaved top of the head with a small topknot, dark armor and a black cloak"
ASHIGARU = "round-white-head cartoon Japanese foot soldiers of 1575 with conical iron hats and simple armor, holding matchlock arquebuses"
IEYASU = "a round-white-head cartoon chubby Japanese warlord of 1600, shaved top of the head with a small topknot, dark brown armor and a folding fan"
HOLANDESES = "round-white-head cartoon Dutch merchants of the 17th century with wide-brimmed black hats, white collars and dark coats"
EDOPOVO = "round-white-head cartoon townspeople of 18th century Edo in simple cotton kimonos, men with the shaved top and topknot, women with tied-up black hair"
SAM19 = "round-white-head cartoon Japanese samurai officials of 1853 in kimono and wide hakama trousers with two swords at the belt, shaved top of the head with a topknot"
PERRY = "a round-white-head cartoon stern American naval commodore of 1853 with simple flat grey side whiskers, a dark blue naval coat with gold epaulettes and a bicorne hat"
MEIJI = "a round-white-head cartoon young Japanese emperor of 1872 with a simple flat thin mustache shape, in a dark Western military uniform with gold braids"
IWAKURA = "round-white-head cartoon Japanese officials of 1871, some in kimono with topknots and swords, some in Western frock coats and top hats"
SOLD05 = "round-white-head cartoon Japanese soldiers of 1905 in dark blue uniforms with flat peaked caps"
IMIGR = "round-white-head cartoon Japanese immigrant families of 1908, men in simple Western suits and hats, women in kimonos, children, with suitcases and cloth bundles"
SOLD40 = "round-white-head cartoon Japanese soldiers of the 1940s in plain khaki uniforms and plain field caps"
CIV45 = "round-white-head cartoon Japanese civilians of 1945 in simple worn clothes"
US45 = "round-white-head cartoon American soldiers of 1945 in plain olive uniforms and helmets"
POVO64 = "round-white-head cartoon Japanese people of 1964 in 1960s clothes, men in suits and narrow ties, women in simple dresses"
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes"

# ───────────────────────── HOOK (agosto de 1281) ─────────────────────────
cap("Hook")
b("[serious] Japão, agosto de mil duzentos e oitenta e um. Imagine você em cima de um muro de pedra, numa praia, olhando para o mar.",
  f"wall_dusk|A long low wall of piled grey stones running along a sandy beach in southern Japan at dusk in 1281, a few {SAM12} standing on top looking at the sea" + MEDIEVAL + SEMSOL,
  f"pov_wall|View from behind a round-white-head cartoon young samurai of 1281 in simple lamellar armor standing on a stone wall, looking at a calm grey sea at dusk" + SEMSOL,
  "sea_horizon|A wide calm grey sea at dusk seen from a Japanese beach, dozens of small dark sails appearing on the horizon, ominous clouds",
  "stones_close|Close view of a rough stone wall on a beach with waves breaking below it, a samurai's straw sandals and the end of a longbow resting on top, dusk light",
  card="1281")
b("Na sua frente, segundo as crônicas, a maior frota de invasão que o mundo já tinha visto: milhares de navios de Kublai Khan, neto de Gêngis e dono da China.",
  "fleet_huge|A huge fleet of hundreds of 13th century Chinese wooden junks with ribbed brown sails filling the sea up to the horizon, seen from a Japanese beach" + SEMBAND,
  f"kublai_throne|{KUBLAI}, sitting on a golden throne in a Chinese palace hall, pointing forward with a determined face, courtiers bowing" + SEMBAND + "@@KUBLAI KHAN",
  "map_mongol|Map of Asia in 1280 where a huge empire stretching from Korea and China to Persia and Russia is painted in one solid ochre color, the islands of Japan uncolored in the east, " + MAPA,
  f"junk_deck|On the deck of a 13th century Chinese war junk, {MONGOIS} crowded together, looking toward a distant green coast" + SEMBAND,
  "junks_close|Close view of three big wooden war junks with ribbed sails and wooden castles at the stern sailing side by side on a grey sea" + SEMBAND)
b("Aí, numa noite, vem um tufão. De manhã, quase não sobra frota. Os japoneses chamam aquele vento de kamikaze: o vento divino.",
  "typhoon_night|A violent typhoon at night: gigantic dark waves, black sky with a lightning bolt, many wooden junks tipping over and breaking apart" + SEMBAND,
  "typhoon_close|Close view of a broken wooden junk mast and torn ribbed sail falling into huge waves under a lightning-lit sky, no people visible",
  "morning_debris|A calm Japanese bay at sunrise after a storm, broken planks and pieces of masts floating on the water, a stone wall on the beach, no people in the water" + SANG,
  f"shrine_prayer|Round-white-head cartoon Shinto priests of the 13th century in white robes and tall black caps praying at a small wooden shrine by the sea, wind blowing their sleeves" + MEDIEVAL,
  "wind_symbol|Symbolic scene: a giant swirl of wind and clouds sweeping over a dark sea from a small green island, dramatic and mystical, no people")
b("§ Foi só sorte? [break] Os japoneses juravam que não. E tem uma coisa mais estranha: esse país vivia copiando os vizinhos.",
  f"samurai_sky|{SAM12} on a beach looking up at a clearing sky with relieved and amazed faces, arms raised" + MEDIEVAL + SEMSOL,
  "copy_brush|Close view of a round-white-head cartoon Japanese scholar's hand copying brush strokes from an old scroll onto a blank sheet, only abstract black brush marks" + SEMTXT,
  "copy_gun|A round-white-head cartoon Japanese blacksmith of 1543 in his forge carefully copying a European matchlock arquebus placed on a cloth next to his own copy",
  "copy_train|A round-white-head cartoon Japanese engineer of 1872 in a frock coat studying a small British steam locomotive with a notebook full of drawings" + SEMTXT)
b("Então, a pergunta: como um país que copiava todo mundo passou quase setecentos anos sem que ninguém o conquistasse?",
  "door_sea|Symbolic scene: a huge old wooden Japanese gate standing alone in the middle of the sea, closed, waves around it, dramatic sky",
  "map_japan_sea|The islands of Japan alone in a vast blue sea, the coast of Korea and China far to the west, " + MAPA,
  "hands_islands|Symbolic scene: giant hands of a Mongol general, a European sailor and an American admiral reaching from the sea toward a small green Japanese island, comic" + SEMBAND,
  "ships_around|Many ships of different centuries (Mongol junks, Portuguese carracks, steamships) circling a small green island at a distance, symbolic" + SEMBAND)
b("O mar era o muro do Japão, sim. Mas um dia esse muro vai falhar. Essa é a história inteira do Japão. [break] Guarde esse vento: ele volta.",
  "sea_wall_waves|Huge waves crashing around the rocky coast of a green Japanese island, like a natural wall, sunny sky with fast clouds",
  "black_ship_shadow|A dark silhouette of a 19th century steamship with smoking chimney appearing in the fog on a grey sea, ominous" + SEMBAND,
  f"guide_wind|{GUIA} on a Japanese beach holding his hat against a strong wind, looking at the sea with curiosity" + SEMSOL,
  "wind_cloud_hook|A swirling wind cloud shaped like a spiral over the sea at dawn, mysterious, no people",
  f"samurai_gaze|A round-white-head cartoon samurai of 1281 seen from the side, standing on a stone wall at sunrise, looking at the empty sea, thoughtful" + MEDIEVAL + SEMSOL)

# ───────────────────────── 1. GENTE QUE CHEGOU PELO MAR ─────────────────────────
cap("1. Gente que chegou pelo mar")
b("§ Só que, antes de ser muro, o mar foi estrada. Imagine uma aldeia de casas meio enterradas no chão, há uns cinco mil anos. Gente que caça, pesca e cozinha em potes enfeitados com marcas de corda.",
  f"jomon_village|A prehistoric Japanese village of pit houses with conical thatched roofs half sunk into the ground in a forest clearing, {JOMON} cooking around a fire" + ANTIGO,
  f"jomon_fishing|{JOMON} fishing with nets from a simple dugout canoe near a rocky green coast" + ANTIGO,
  f"jomon_hunt|{JOMON} returning from the forest carrying a wild boar on a pole, autumn trees" + ANTIGO,
  "jomon_pot|Close view of an ancient Jomon clay pot with a flame-like rim and rope-pattern decoration, standing on the earth floor of a hut by firelight, no writing",
  f"jomon_potter|{JOMON}: a woman pressing a twisted cord onto a wet clay pot to make patterns, children watching" + ANTIGO,
  "jomon_kids|Round-white-head cartoon prehistoric Japanese children playing on a beach with shells and a small clay pot, green forested hills behind" + ANTIGO,
  card="3000 a.C.")
b("São os jomon, e esses potes estão entre as cerâmicas mais antigas do mundo. Então, por volta de trezentos antes de Cristo, chegam barcos do continente, trazendo arroz e metal.",
  "jomon_pots_row|A row of different ancient Jomon clay pots with rope patterns displayed on a wooden shelf, warm light, no labels" + SEMTXT,
  f"boats_arrive|Simple wooden boats arriving on a Japanese beach from the sea, {YAYOI} unloading baskets of rice seedlings and bronze tools" + ANTIGO.replace("no metal tools, ", ""),
  "map_crossing|Map of the sea between the Korean peninsula and the Japanese islands with a few small boats crossing, " + MAPA,
  f"bronze_tools|Close view of ancient bronze bells, a bronze sword and an iron sickle on a straw mat, held by {YAYOI}" + SEMTXT,
  f"rice_seedlings|{YAYOI} planting the first rice seedlings in a muddy field by the sea, curious Jomon hunters watching from the forest edge" + ANTIGO.replace("no metal tools, ", ""))
b("E arroz muda tudo, porque arrozal pede canal, vizinho e chefe. Os chefes brigam, e os vencedores ganham túmulos em forma de fechadura, os kofun. O maior tem mais área que a base da Grande Pirâmide.",
  f"rice_paddies|{YAYOI} working together in flooded rice paddies, digging a small irrigation canal, wooden watchtower in the background, green hills" + ANTIGO.replace("no metal tools, ", ""),
  f"chiefs_fight|Two groups of {YAYOI} with wooden shields and bronze spears facing each other angrily across a rice field, no blood" + SEMBAND,
  "kofun_aerial|Aerial view of a gigantic keyhole-shaped burial mound covered with trees, surrounded by a moat of still water, green Japanese countryside, no modern buildings",
  "kofun_pyramid|Symbolic comparison: a keyhole-shaped wooded burial mound next to an Egyptian pyramid at the same scale on a flat plain, the mound clearly wider, comic" + SEMTXT,
  "haniwa|Close view of simple ancient clay haniwa figures of horses and warriors standing in a row on the slope of a burial mound" + SEMTXT,
  f"mound_builders|Hundreds of {YAYOI} carrying baskets of earth up a huge half-built burial mound, a chief watching from a litter" + ANTIGO.replace("no metal tools, ", ""))
b("§ Um clã sai na frente, os Yamato, e anuncia que descende da deusa do sol, Amaterasu. Spoiler: a família continua no trono até hoje. É a monarquia hereditária mais antiga do mundo.",
  f"yamato_chief|{YAMATO}, standing proudly before kneeling villagers on a hill, holding up a shining bronze mirror" + ANTIGO.replace("no metal tools, ", "") + "@@CLÃ YAMATO",
  "amaterasu|A cartoon sun goddess with a round white head, long black hair and white and red robes stepping out of a cave and spreading golden light over the mountains, mythical, no sun disc symbol",
  "family_tree|Symbolic scene: a giant ancient tree whose branches go from a simple ancient chief at the roots up to a modern man in a suit at the top, all round-white-head cartoon figures" + SEMTXT,
  "mirror_sword_jewel|Close view of a bronze mirror, a straight ancient sword and a curved green jade jewel on a silk cloth, sacred atmosphere" + SEMTXT,
  "spoiler_throne|Symbolic comic scene: a long line of round-white-head cartoon emperors from ancient robes to a modern suit, all standing one behind the other in front of the same simple throne" + SEMTXT,
  "ise_shrine|A simple ancient wooden Shinto shrine with a thatched roof and crossed roof beams in a cedar forest, morning mist" + ANTIGO.replace("no temples, ", ""))
b("Se você acha comprida a árvore da sua família, pense nessa. Mas um clã com deusa na família tinha um problema: do outro lado do mar havia um império mais rico, que se achava o centro do mundo.",
  f"guide_tree|{GUIA} looking up at an enormously tall family tree drawn as a real tree disappearing into the clouds, impressed, comic" + SEMTXT,
  "chang_an_far|A huge walled Chinese city of the 7th century seen across the sea from a Japanese hill, golden palaces and wide straight avenues, impressive" + SEMBAND,
  "map_china_japan|Map of East Asia with a huge China painted in gold and the small islands of Japan in green across the sea, " + MAPA,
  f"yamato_worried|{YAMATO} on a cliff looking worried across the sea toward a distant golden glow on the horizon",
  "chinese_emperor_far|A Chinese emperor of the 6th century on a huge golden throne looking down at a tiny map of the world with China in the center, comic" + SEMTXT,
  "tribute_line|A long line of foreign envoys carrying gifts up the steps of a golden Chinese palace, seen from far away" + SEMBAND)

# ───────────────────────── 2. UMA CARTA PARA O FILHO DO CÉU ─────────────────────────
cap("2. Uma carta para o Filho do Céu")
b("§ Esse império era a China. E o que vinha de lá chegava pelo mar, quase sempre passando pela Coreia: a escrita, as ideias, e, no século seis, uma estátua dourada do Buda.",
  f"korea_boat|{COREANO} arriving on a Japanese beach in a wooden boat carrying a small golden Buddha statue and bundles of scrolls" + ANTIGO.replace("no temples, ", "").replace("no metal tools, ", ""),
  "golden_buddha|Close view of a small golden seated Buddha statue unwrapped from a silk cloth on a wooden table, Japanese court nobles of the 6th century looking amazed",
  "chinese_scrolls|Bundles of ancient Chinese scrolls and brushes unpacked from wooden chests, only abstract brush marks" + SEMTXT,
  "map_korea_route|Map of East Asia showing a dotted route from China through the Korean peninsula to the Japanese islands, " + MAPA,
  "buddha_debate|Round-white-head cartoon Japanese court nobles of the 6th century arguing in two groups around the small golden Buddha statue, comic" + ANTIGO.replace("no temples, ", "").replace("no metal tools, ", ""))
b("Imagine agora a corte da China, no ano seiscentos e sete. Um enviado japonês entrega uma carta ao imperador. A carta diz: do Filho do Céu da terra onde o sol nasce, ao Filho do Céu da terra onde o sol se põe.",
  f"sui_court|A grand Chinese imperial hall of the 7th century with red pillars, {ENVIADO} kneeling before the throne, Chinese officials in long robes watching" + SEMBAND,
  f"envoy_letter|{ENVIADO} holding out a sealed scroll with both hands, nervous smile" + SEMTXT,
  f"emperor_reads|{YANG} unrolling a scroll on his throne, eyebrows rising" + SEMTXT + "@@IMPERADOR YANG",
  "sunrise_sunset|Symbolic split scene: on the left a sun rising over green Japanese islands, on the right a sun setting over a golden Chinese palace, no symbols" + SEMTXT,
  "letter_seal|Close view of a rolled silk scroll tied with a red cord and a small round wax seal resting on a lacquer tray, the scroll closed" + SEMTXT,
  "shotoku_writes|" + SHOTOKU + ", writing with a brush at a low desk in a simple wooden palace, a cheeky smile" + SEMTXT + "@@PRÍNCIPE SHŌTOKU",
  card="607")
b("O imperador Yang não gosta nem um pouco. Na China só cabia um Filho do Céu, e ele não estava se pondo. Quando você chama o Japão de terra do sol nascente, está ecoando essa carta.",
  f"emperor_angry|{YANG} standing up from his throne, furious, throwing the scroll on the floor, courtiers hiding behind pillars, comic",
  "officials_shocked|Round-white-head cartoon Chinese court officials of the 7th century in long robes and black caps, looking at each other in shock, comic" + SEMTXT,
  f"guide_sunrise|{GUIA} on a beach watching a beautiful sunrise over the sea, arms open, peaceful" + SEMSOL,
  "sunrise_islands|A golden sunrise over the sea and the green mountains of Japan, birds flying, peaceful, no flags")
b("§ E aqui está a primeira peça da resposta: o Japão copiava, mas não se ajoelhava. A capital, Nara, é uma miniatura da capital chinesa. Alguns chefes até aceitaram títulos da China, quando isso dava comércio. Só que nenhum imperador chinês mandou no Japão.",
  "nara_city|The ancient Japanese capital Nara in 710 seen from above: a grid of straight wide avenues, wooden palaces with red pillars and grey tiled roofs, a tall wooden pagoda, mountains around" + SEMBAND + "@@NARA",
  "grid_compare|Symbolic scene: a big Chinese city plan and a small copy of the same grid plan side by side on a table, drawn as simple lines, a round-white-head cartoon architect measuring" + SEMTXT,
  "nara_buddha_hall|A huge wooden Buddhist temple hall in 8th century Nara with a giant bronze Buddha inside, round-white-head cartoon monks and nobles bowing",
  "trade_title|Round-white-head cartoon Japanese envoys receiving a golden seal from Chinese officials while porters carry chests of silk to a ship, symbolic of trade" + SEMBAND,
  "no_soldier|Symbolic scene: an empty Japanese beach with an untouched sand shore, a Chinese war junk turning back on the horizon, calm" + SEMBAND)
b("O problema de copiar um gigante é que, um dia, o gigante tropeça. E quando a China entrou em crise, o Japão parou de mandar embaixadas e olhou para dentro.",
  "giant_trips|Symbolic comic scene: a giant golden Chinese dragon-shaped statue tripping over a stone, a tiny Japanese cartoon figure stepping back surprised" + SEMTXT,
  "embassy_ship_dock|An empty Japanese embassy ship tied up at a wooden dock, sails folded, round-white-head cartoon officials shaking their heads" + SEMBAND + MEDIEVAL,
  "court_inward|Round-white-head cartoon Heian nobles closing a sliding paper door and turning toward a beautiful inner garden with a pond" + MEDIEVAL)

# ───────────────────────── 3. POETAS NA CORTE, ESPADAS NO CAMPO ─────────────────────────
cap("3. Poetas na corte, espadas no campo")
b("§ Quioto, por volta do ano mil. Imagine uma dama da corte escrevendo à luz de lamparina, com doze camadas de seda no corpo. Na corte, uma cor errada na manga podia arruinar uma reputação.",
  f"lady_writing|{DAMA} writing with a brush at a low lacquer desk by the light of an oil lamp, behind a bamboo blind, at night" + SEMTXT + MEDIEVAL,
  "silk_layers|Close view of the sleeves of a Heian court robe showing many layers of silk in graded colors, red, green, purple and yellow",
  f"court_judging|{CORTE} looking with horror at one lady whose sleeve colors do not match, comic" + MEDIEVAL,
  "kyoto_palace|The Heian palace in Kyoto around the year 1000: low elegant wooden halls with orange pillars and cypress-bark roofs around a white gravel courtyard" + MEDIEVAL + "@@QUIOTO",
  card="ano 1000")
b("Ela se chama Murasaki Shikibu e escreve o Genji, um dos primeiros romances do mundo. Repare no alfabeto: é o kana, criado no Japão, porque a escrita chinesa não servia bem para a língua japonesa.",
  f"murasaki|{DAMA} smiling proudly with a stack of handwritten pages, ladies reading over her shoulder" + SEMTXT + "@@MURASAKI SHIKIBU",
  "kana_brush|Close view of a brush painting flowing cursive strokes on a sheet of paper, only abstract graceful lines, no real characters" + SEMTXT,
  "genji_scroll|A painted Japanese picture scroll unrolled on the floor showing tiny court scenes seen from above with the roofs removed, no writing" + SEMTXT,
  f"guide_phone|{GUIA} reading a long book on a smartphone next to a Heian lady reading a scroll, both crying with emotion, comic" + SEMTXT)
b("§ Só que, enquanto a corte fazia poesia, quem cuidava das terras lá fora eram famílias armadas: os samurais. E aí, em mil cento e oitenta e cinco, uma dessas famílias vence a guerra, e o chefe dela vira xogum.",
  f"provinces|{SAM12} on horseback riding through rice fields in the provinces while peasants bow" + MEDIEVAL + SEMSOL,
  f"poets_vs_warriors|Symbolic split scene: on the left Heian nobles writing poems in a garden, on the right {SAM12} sharpening swords in a farmyard" + MEDIEVAL,
  "dannoura|A sea battle of 1185 between many small Japanese wooden boats with archers, waves and arrows in the air, no blood, no flags with symbols" + SEMBAND,
  f"shogun_named|{XOGUM}, receiving a scroll of appointment from a court official, kneeling samurai around" + SEMTXT + MEDIEVAL + "@@XOGUM",
  card="1185")
b("O imperador continua no trono, mas quem manda é o general. Pense num prédio onde o dono só assina o que o síndico decide. E esse arranjo vai durar quase setecentos anos.",
  f"emperor_signs|{IMPERADOR} sitting on a raised mat signing a paper with a bored face while a samurai general stands beside him pointing at where to sign, comic" + SEMTXT,
  f"guide_building|{GUIA} in front of a small apartment building watching a tiny king in a window sign papers handed by a stern doorman, comic" + SEMTXT)
b("Então o Japão tinha dois donos. E, do outro lado do mar, alguém queria ser o dono de todos: aquele neto de Gêngis.",
  "two_masters|Symbolic scene: a Japanese emperor on the left and a samurai general on the right pulling the same rope tied to a small model of Japan, comic" + SEMTXT,
  f"kublai_letter|{KUBLAI} dictating a letter to a scribe in a golden palace, a map of Japan on a table" + SEMTXT)

# ───────────────────────── 4. O VENTO DIVINO ─────────────────────────
cap("4. O vento divino")
b("§ Kublai Khan manda cartas exigindo que o Japão se submeta. O governo dos samurais nem responde. Então, em mil duzentos e setenta e quatro, a primeira frota desembarca na baía de Hakata.",
  "letters_ignored|Round-white-head cartoon samurai officials of 1270 in a wooden hall reading a Mongol letter and putting it aside with crossed arms" + SEMTXT + MEDIEVAL,
  f"landing_1274|{MONGOIS} landing from boats on a wide sandy beach, horses and drums, Japanese pine trees behind" + SEMBAND + MEDIEVAL + "@@BAÍA DE HAKATA",
  "map_hakata|Map of the strait between Korea and the southern Japanese island of Kyushu, a bay on the northern coast of Kyushu, " + MAPA,
  card="1274")
b("Imagine você samurai: você grita o seu nome e a sua linhagem, como manda a tradição, conta uma crônica, e espera um adversário. Do outro lado vêm nuvens de flechas e bombas de ferro que explodem.",
  f"samurai_shout|A round-white-head cartoon samurai of 1274 on horseback in simple lamellar armor, shouting proudly with one arm raised in front of a line of enemies" + MEDIEVAL + SEMSOL,
  "arrow_cloud|A cloud of arrows rising from a line of Mongol archers behind round shields on a beach, seen from the Japanese side, no blood" + SEMBAND,
  "iron_bomb|Close view of a round ceramic and iron bomb with a burning fuse rolling on the sand, startled horses in the background, no blood",
  f"samurai_surprised|{SAM12} ducking behind their shields, eyes wide with surprise at small explosions on the beach, comic, no blood" + SEMSOL)
b("Os invasores voltam para os navios, e uma tempestade faz o resto. Aí os japoneses fazem o que ninguém faz com sorte: se preparam. Constroem um muro de pedra de uns vinte quilômetros na praia.",
  "storm_1274|Mongol junks being tossed by a storm off a Japanese coast at night" + SEMBAND,
  f"wall_building|Round-white-head cartoon Japanese farmers and {SAM12} carrying and piling big stones to build a long wall along a beach, busy and organized" + MEDIEVAL,
  "wall_long|A long stone defensive wall about two meters high curving along the whole length of a sandy bay, seen from a hill, pine trees" + MEDIEVAL,
  card="1276")
b("§ Por isso, em mil duzentos e oitenta e um, a frota gigante quase não consegue desembarcar. Fica semanas no mar, atacada de noite por barquinhos de samurais. Até que chega aquele tufão.",
  "fleet_blocked|The huge Mongol fleet anchored off a beach blocked by a long stone wall lined with samurai, seen from above" + SEMBAND,
  "night_raid|Small Japanese rowing boats with samurai approaching a giant Chinese junk at night, torches, quiet sea, no blood" + SEMBAND,
  "typhoon_wide|A typhoon approaching a bay full of anchored junks: a black wall of clouds, rising waves, bending pine trees on the shore" + SEMBAND,
  card="1281")
b("E lembra da nossa pergunta: foi só sorte? No fundo do mar, perto da ilha de Takashima, arqueólogos acharam os navios. Muitos eram de fundo chato: barcos de rio no oceano.",
  f"divers|Round-white-head cartoon archaeologist divers in modern diving suits exploring the remains of an old wooden ship on the sea floor near rocks, fish around" + SEMTXT,
  "wreck_wood|Close view of old blackened wooden planks of a shipwreck half buried in sand under the sea, a diver measuring with a tape",
  "flat_hull|Symbolic cross-section drawing of two wooden ships: one with a deep keel for the open ocean, one flat-bottomed river boat wobbling on a big wave, comic" + SEMTXT,
  "hasty_shipyard|A crowded 13th century Chinese shipyard where round-white-head cartoon carpenters build many wooden boats in a hurry, a foreman shouting" + SEMBAND)
b("Tente atravessar um mar de tufões num barco de rio. Segunda peça da resposta: o mar dava tempo, e o Japão usava esse tempo. O problema: vitória contra invasor não rende terra para dividir, e os samurais queriam pagamento.",
  f"guide_riverboat|{GUIA} in a tiny flat river boat on a huge ocean wave, holding on desperately, comic",
  f"samurai_pay|{SAM12} standing in line in front of a samurai official with an empty chest, holding out their hands, annoyed faces, comic" + MEDIEVAL,
  "empty_chest|Close view of an open empty wooden treasure chest on a tatami floor, a single coin at the bottom" + SEMTXT)

# ───────────────────────── 5. OS BÁRBAROS DO SUL ─────────────────────────
cap("5. Os bárbaros do sul")
b("§ Sem pagamento, os samurais se viram contra o xogum, e o Japão se parte em dezenas de senhores em guerra. Até que, em mil quinhentos e quarenta e três, um barco perdido encosta numa ilhazinha do sul, Tanegashima.",
  "warring_map|Map of the Japanese islands divided into dozens of small territories in many colors, " + MAPA,
  f"warlords_war|Round-white-head cartoon Japanese samurai armies of the 15th century in lamellar armor clashing on a field near a burning wooden village, no blood" + SEMBAND + MEDIEVAL,
  "junk_lost|A battered Chinese junk drifting toward a small green subtropical island with palm-like cycad trees and a sandy beach, calm sea" + SEMBAND + "@@TANEGASHIMA",
  card="1543")
b("Dentro, três portugueses, com uma coisa que o Japão nunca tinha visto: o arcabuz. O senhor da ilha compra dois e manda o ferreiro copiar. Em poucas décadas, o Japão tem milhares deles.",
  f"portuguese_land|{PORT} stepping onto a Japanese beach from a small boat, curious Japanese villagers and a samurai lord watching" + SEMBAND,
  f"gun_demo|A Portuguese sailor of 1543 firing a matchlock arquebus at a target, smoke, a round-white-head cartoon Japanese lord in kimono jumping with surprise, comic",
  "blacksmith_copy|A round-white-head cartoon Japanese blacksmith of the 16th century in his forge hammering a gun barrel, a European arquebus beside him as a model",
  f"many_guns|Rows of matchlock arquebuses stacked in a Japanese armory of the 1570s, {ASHIGARU} checking them" + SEMBAND)
b("§ E você tem parente nessa história. Os portugueses trazem padres, tecidos e palavras: o nosso pão virou pan, em japonês. Arigatô vem de obrigado? Isso é mito. Mas o pão é verdade.",
  f"xavier|{JESUITA} preaching to curious Japanese townspeople in front of a wooden house" + MEDIEVAL + "@@FRANCISCO XAVIER",
  "portuguese_ship_japan|A big Portuguese carrack with round-white-head cartoon sailors unloading bales of cloth at a Japanese port, Japanese merchants bargaining" + SEMBAND + MEDIEVAL,
  "bread_pan|A round-white-head cartoon Japanese baker of the 16th century proudly holding a round loaf of bread next to a Portuguese sailor, comic" + SEMTXT,
  f"guide_bread|{GUIA} holding a loaf of bread in one hand and wagging a finger with the other, comic" + SEMTXT)
b("Com essas armas, um senhor chamado Oda Nobunaga põe milhares de atiradores atrás de cercas de madeira e vence a cavalaria mais temida do Japão. O sucessor dele termina de unificar o país, e até tenta invadir a Coreia. Não dá certo.",
  f"nobunaga|{NOBUNAGA} standing on a hill pointing with a fan, his army behind him" + SEMBAND + "@@ODA NOBUNAGA",
  f"nagashino|{ASHIGARU} in three rows behind a wooden palisade firing arquebuses at charging samurai horsemen, a lot of smoke, no blood" + SEMBAND,
  "unified_map|Map of the Japanese islands now painted in a single color, " + MAPA,
  "korea_ships|Japanese wooden warships of 1592 crossing the strait toward the Korean coast, waves, grey sky" + SEMBAND,
  card="1575")
b("Só que, junto com as armas, os portugueses trouxeram outra coisa: uma fé com chefe em Roma. E, por volta de mil e seiscentos, já eram, estima-se, uns trezentos mil cristãos japoneses.",
  "christians|Round-white-head cartoon Japanese Christians of 1600 in kimonos kneeling in a simple wooden church with a wooden cross, candles" + SEMTXT,
  "rome_shadow|Symbolic scene: the long shadow of a Pope's tall hat falling over a Japanese town across the sea, ominous, comic" + SEMTXT)

# ───────────────────────── 6. A PORTA TRANCADA ─────────────────────────
cap("6. A porta trancada")
b("§ Imagine uma ilha artificial em forma de leque, pouco maior que um campo de futebol, no porto de Nagasaki. Uma ponte, vigias na ponte, e lá dentro uns poucos holandeses. Durante mais de duzentos anos, essa é a janela do Japão para a Europa.",
  "dejima_aerial|A small fan-shaped artificial island in Nagasaki harbor in the 1700s with a few wooden warehouses and a single stone bridge to the city, a Dutch ship anchored nearby, no flags" + EDOJP.replace("no Western buildings", "a few Western-style warehouses only on the island") + "@@DEJIMA",
  f"bridge_guard|A round-white-head cartoon Japanese guard of the 1700s with two swords standing at the gate of a small bridge, frowning at a {HOLANDESES.replace('merchants', 'merchant')} on the other side" + EDOJP,
  f"dutch_bored|{HOLANDESES} sitting in a small courtyard on a tiny island, bored, smoking long clay pipes, looking at the city beyond the water, comic" + SEMTXT,
  "window_europe|Symbolic scene: a single small window open in a huge wooden wall around Japan, a Dutch merchant's face peeking in, comic" + SEMTXT,
  card="1641")
b("Como se chega nisso? Os Tokugawa vencem a guerra em mil e seiscentos e trazem paz. Mas desconfiam dos cristãos, que obedecem a um chefe em Roma. Então proíbem a fé, expulsam os portugueses e trancam a porta.",
  f"sekigahara|A big battle of 1600 on a misty plain between two samurai armies with tall plain banners, no symbols on banners" + SEMBAND + MEDIEVAL.replace("no stone castles, no tall white castle towers, ", "") + "@@SEKIGAHARA",
  f"ieyasu|{IEYASU} sitting calmly on a camp stool, fanning himself, generals kneeling" + SEMBAND + "@@TOKUGAWA IEYASU",
  "edict_board|A wooden notice board in a Japanese town with a blank paper edict nailed on it, townspeople looking worried, the paper completely blank" + SEMTXT,
  "ship_leaving|A Portuguese carrack sailing away from a Japanese harbor while samurai officials watch from the pier with arms crossed" + SEMBAND + EDOJP,
  "door_closing|Symbolic scene: a huge wooden Japanese gate on a beach being closed by samurai guards, a European ship outside on the sea" + SEMTXT)
b("Japonês que saísse do país e voltasse podia ser executado. Os holandeses ganham a vaga porque prometem falar de comércio, não de Deus. Negócio é negócio.",
  "boats_burned|Japanese ocean-going ships pulled onto a beach and left to rot, only small coastal boats in the water" + EDOJP,
  f"dutch_deal|{HOLANDESES} bowing deeply before a samurai official and showing a chest of goods, a priest walking away in the background, comic" + SEMTXT)
b("§ E aqui a pergunta do começo fica clara. Terceira peça da resposta: o Japão deixava entrar ideias e fechava a porta quando quem entrava queria mandar. E a distância do mar deixava fazer isso sem castigo.",
  "dutch_books|A round-white-head cartoon Japanese scholar of the 1700s studying Dutch anatomy books and a microscope by candlelight" + SEMTXT,
  "map_far|Map of the world in 1700 with Europe at the far left edge and Japan alone at the far right edge, a long dotted sea route between them, " + MAPA,
  "gate_ideas|Symbolic scene: a half-open Japanese gate letting books and seeds float in while a soldier with a spear is pushed out, comic" + SEMTXT)
b("Lá dentro, duzentos anos de paz. Edo, a futura Tóquio, passa de um milhão de pessoas. Se você lê mangá, a palavra vem dessa época.",
  f"edo_street|A busy street of Edo in the 1700s full of {EDOPOVO}, shops with cloth curtains, a wooden bridge over a canal, Mount Fuji far in the background" + SEMTXT + EDOJP + "@@EDO",
  "woodblock|A round-white-head cartoon Japanese printmaker of the 1800s carving a woodblock and printing a colorful picture of a big wave, no writing" + SEMTXT,
  f"edo_theater|{EDOPOVO} laughing in a crowded wooden theater watching actors in colorful costumes" + EDOJP)
b("O problema é que, do outro lado do mundo, alguém inventava um navio que não precisava de vento.",
  "steam_factory|A 19th century British shipyard with a big black steamship being built, tall chimneys and smoke" + SEMBAND,
  "steam_engine|Close view of the pistons and gears of a 19th century steam engine glowing with heat" + SEMTXT)

# ───────────────────────── 7. OS NAVIOS NEGROS ─────────────────────────
cap("7. Os navios negros")
b("§ Baía de Edo, julho de mil oitocentos e cinquenta e três. Imagine você pescando, e no horizonte aparecem quatro navios pretos, soltando fumaça, andando contra o vento.",
  "fishermen_1853|Round-white-head cartoon Japanese fishermen of 1853 in a small wooden boat in a calm bay, one pointing in shock at the horizon" + EDOJP,
  "black_ships|Four black 19th century American warships, two of them steam frigates with paddle wheels and smoking chimneys, entering a Japanese bay against the wind" + SEMBAND,
  "smoke_close|Close view of a tall black chimney of a paddle steamer pouring thick black smoke into a blue sky" + SEMTXT,
  card="1853")
b("É o comodoro americano Matthew Perry, com uma carta e com canhões. O recado: abram os portos. Nesse dia, o mar parou de proteger o Japão.",
  f"perry|{PERRY} standing on the deck of a black steamship, holding a sealed letter, cannons behind him" + SEMBAND + "@@MATTHEW PERRY",
  "cannons_shore|A row of big black cannons on a steamship deck pointing at a Japanese coast with wooden houses" + SEMBAND,
  "sea_not_wall|Symbolic scene: a stone wall on a Japanese beach while a black steamship simply sails past it, waves irrelevant" + SEMBAND)
b("Um poema da época faz piada: um chá caro acordou o país do sono da paz, e com só quatro xícaras ninguém dorme à noite. Em japonês, o nome do chá soava igual a navio a vapor.",
  f"tea_cups|{EDOPOVO} sitting awake at night with four teacups in front of them, wide-open eyes, comic" + EDOJP,
  "tea_steam|Symbolic comic scene: four Japanese teacups on a tray, and the steam rising from each cup takes the shape of a small black steamship" + SEMTXT)
b("§ E o Japão tinha visto o que aconteceu com a China, que perdeu a Guerra do Ópio para os britânicos pouco mais de dez anos antes. Então ele assina tratados desiguais, porque não tem como dizer não.",
  "opium_war|British steam warships firing at Chinese wooden junks near a river fort in 1840, smoke, no blood" + SEMBAND,
  f"treaty_sign|{SAM19} signing a document at a table with American officers in dark blue uniforms, tense faces, the paper blank" + SEMTXT,
  f"officials_worry|{SAM19} talking nervously in a wooden hall, one holding a small model of a steamship" + EDOJP)
b("Os samurais se revoltam contra o xogum que abriu a porta. Mas o que fazer? Expulsar os estrangeiros, sem canhão? Ou o impensável: copiar o invasor para não ser invadido.",
  f"samurai_rebels|{SAM19} with drawn swords shouting angrily in a courtyard at night, torches" + EDOJP,
  "sword_vs_cannon|Symbolic comic scene: a samurai with a sword facing a giant black cannon that is much bigger than him, sweating" + SEMTXT,
  "mirror_ship|Symbolic scene: a samurai looking at his reflection in a big mirror, and the reflection is a man in a Western uniform beside a steamship" + SEMTXT)

# ───────────────────────── 8. COPIAR O OCIDENTE, DEPRESSA ─────────────────────────
cap("8. Copiar o Ocidente, depressa")
b("§ Os rebeldes vencem, derrubam o xogum e põem na frente um imperador de quinze anos. É a Restauração Meiji, em mil oitocentos e sessenta e oito.",
  f"meiji_young|{MEIJI.replace('young Japanese emperor of 1872 with a simple flat thin mustache shape, in a dark Western military uniform with gold braids', 'teenage Japanese emperor of 1868 in white and red court robes with a tall black cap')}, sitting on a throne while samurai leaders kneel" + EDOJP + "@@IMPERADOR MEIJI",
  "castle_surrender|Samurai of 1868 handing over the keys of a big white Japanese castle to soldiers in mixed Western and Japanese uniforms" + SEMBAND,
  card="1868")
b("Agora imagine um navio saindo de Yokohama com boa parte do governo a bordo. Eles vão passar quase dois anos visitando fábricas, escolas e quartéis nos Estados Unidos e na Europa.",
  f"iwakura_ship|{IWAKURA} waving goodbye from the deck of a big steamship leaving a Japanese port" + SEMBAND,
  f"iwakura_factory|{IWAKURA} visiting a noisy British textile factory with machines, taking notes with wide eyes" + SEMTXT,
  f"iwakura_school|{IWAKURA} looking into a European classroom with children at desks" + SEMTXT,
  card="1871")
b("Imagine boa parte dos ministros do Brasil viajando dois anos para copiar o mundo. Eles voltam e copiam tudo: a ferrovia inglesa, a constituição alemã, o exército, a escola. Os samurais perdem até o direito de andar de espada.",
  f"guide_suitcases|{GUIA} watching a long line of tiny ministers in suits carrying suitcases onto a ship, comic" + SEMTXT,
  "first_train|The first Japanese train of 1872: a small British-style steam locomotive leaving a station among round-white-head cartoon Japanese people in kimonos and Western clothes, amazed" + SEMTXT,
  "meiji_school|A Meiji-era Japanese classroom with round-white-head cartoon children in kimonos at Western desks and a teacher in a suit with a blackboard covered only in simple drawings" + SEMTXT,
  "swords_down|A round-white-head cartoon old samurai sadly placing his two swords on a table in front of a policeman in a Western uniform" + SEMTXT)
b("§ E funciona depressa. Em mil oitocentos e noventa e cinco, o Japão vence a China. Em mil novecentos e cinco, vence a Rússia: pela primeira vez nos tempos modernos, um país asiático derrota uma potência europeia.",
  "war_1895|Japanese steel warships of 1894 firing at Chinese warships at sea, smoke, no blood" + SEMBAND,
  "tsushima|The naval battle of Tsushima in 1905: grey battleships firing at each other on a rough sea, smoke and splashes, no blood" + SEMBAND,
  f"soldiers_1905|{SOLD05} cheering on a hill with rifles raised, no flags" + SEMBAND,
  "map_1905|Map of East Asia where Japan, Taiwan and the southern tip of Manchuria are painted in the same red-brown color, " + MAPA,
  card="1905")
b("Três anos depois, o navio Kasato Maru chega a Santos com setecentos e oitenta e um japoneses. Se você conhece um descendente de japonês no Brasil, a história dele começa aqui.",
  f"kasato|A steamship arriving at the port of Santos in Brazil in 1908, {IMIGR} crowded at the rail looking at the green hills of the coast" + SEMBAND + "@@KASATO MARU",
  f"immigrants_port|{IMIGR} walking down a gangway onto a Brazilian dock with palm trees and warehouses" + SEMTXT,
  "coffee_farm|Round-white-head cartoon Japanese immigrants of 1908 working on a Brazilian coffee plantation, rows of coffee trees, red earth, blue sky",
  card="1908")
b("Só que o Japão não copiou só fábricas. Copiou também o que as potências faziam com elas: colônias.",
  "empire_copy|Symbolic scene: a round-white-head cartoon Japanese official of 1900 in a frock coat copying a European colonial map onto a blank map with a brush, serious" + SEMTXT,
  "map_colonies|Map of the world in 1900 with large colonial territories in Africa and Asia painted in different flat colors, " + MAPA)

# ───────────────────────── 9. O INVASOR (1931–45; sem humor) ─────────────────────────
cap("9. O país que ninguém conquistava")
b("§ [serious] Primeiro, Taiwan. Depois, a Coreia, anexada em mil novecentos e dez. Em mil novecentos e trinta e um, a Manchúria. O país que ninguém conquistava agora conquistava os vizinhos.",
  "map_expansion|Map of East Asia in 1932 with Japan, Korea, Taiwan and Manchuria painted in the same dark red color, " + MAPA,
  f"soldiers_march|{SOLD40} marching on a dusty road through a Manchurian plain, seen from far away" + SEMSIMB,
  "korea_occupied|A Korean city street of 1910 with traditional tiled roofs and Japanese soldiers standing guard, Korean townspeople walking past with heads down" + SEMSIMB,
  card="1910")
b("Em mil novecentos e trinta e sete, vem a guerra com a China. Em Nanquim, soldados japoneses matam dezenas de milhares de civis; algumas estimativas passam de duzentos mil.",
  "nanjing_wall|The old grey city wall of Nanjing with a large gate under a dark smoky sky, empty road, no people" + SEMSIMB,
  "empty_shoes|A pair of small worn shoes and a broken umbrella on an empty street of an old Chinese city, ash in the air, no people" + SEMSIMB,
  "candles_memorial|Many small candles burning in the dark in front of a stone memorial wall, quiet and solemn" + SEMSIMB,
  card="1937")
b("§ Em dezembro de mil novecentos e quarenta e um, o Japão ataca Pearl Harbor e entra em guerra com os Estados Unidos. E, quando a guerra vira, ele procura de novo aquele vento: os pilotos suicidas ganham o nome de kamikaze.",
  "pearl_harbor|American battleships at anchor in a harbor in Hawaii under a smoky sky, small planes far away, seen from a distance, no fire on people" + SEMSIMB,
  "pacific_map|Map of the Pacific Ocean in 1942 with islands and coastlines, a large area around Japan shaded in dark red, " + MAPA,
  "lone_plane|A single small propeller plane flying toward the clouds over a grey ocean at dawn, seen from far away, lonely" + SEMSIMB,
  "wind_returns|The same swirling wind cloud over the sea as in 1281, now with a small plane flying into it, symbolic, solemn" + SEMSIMB,
  card="1941")
b("Em agosto de mil novecentos e quarenta e cinco, duas bombas atômicas destroem Hiroshima e Nagasaki. Mais de cem mil pessoas morrem até o fim daquele ano.",
  "stopped_watch|Close view of an old pocket watch stopped at a quarter past eight, lying on grey ash, solemn" + SEMSIMB,
  "hiroshima_dome|A ruined domed building standing alone among flattened grey ruins of a city under a pale sky, seen from far away, no people" + SEMSIMB,
  "paper_cranes|Thousands of colorful paper cranes on strings hanging at a quiet memorial, soft light" + SEMSIMB,
  card="1945")
b("Dias depois, imagine ouvir no rádio, pela primeira vez, a voz do imperador. Ele pede ao povo que suporte o insuportável. É a rendição.",
  f"radio_listen|{CIV45} kneeling around an old wooden radio in a simple room, heads bowed, silent" + SEMSIMB,
  "radio_close|Close view of an old 1940s wooden radio with a round speaker cloth on a low table, morning light" + SEMSIMB)
b("§ E a nossa pergunta ganha um fim amargo. Os americanos chegam pelo mar e, pela primeira vez na história, um exército estrangeiro manda no Japão. Mas a ocupação dura menos de sete anos. O que o Japão faria com a porta escancarada?",
  "fleet_tokyo_bay|A large fleet of grey American warships anchored in Tokyo Bay under a calm sky, Mount Fuji far away" + SEMSIMB,
  f"us_soldiers_tokyo|{US45} walking along a ruined Tokyo street among Japanese civilians, everyone quiet" + SEMSIMB,
  "door_open_wide|Symbolic scene: the huge old wooden Japanese gate in the sea now wide open, broken hinges, grey dawn" + SEMTXT,
  card="1945")

# ───────────────────────── 10. A PORTA ABERTA PARA VENDER ─────────────────────────
cap("10. A porta aberta para vender")
b("§ Tóquio, outubro de mil novecentos e sessenta e quatro. Imagine você na plataforma: um trem branco de nariz comprido sai a mais de duzentos quilômetros por hora. É o trem-bala, inaugurado dias antes da Olimpíada.",
  f"shinkansen_platform|{POVO64} on a station platform in 1964 watching a white and blue bullet train with a long rounded nose depart, amazed" + SEMTXT,
  "shinkansen_fuji|A white and blue 1964 bullet train speeding past green tea fields with Mount Fuji in the background, blue sky" + SEMTXT,
  "olympic_stadium|A big modern stadium in Tokyo in 1964 full of people, fireworks, no flags, no rings, no logos" + SEMTXT,
  card="1964")
b("Dezenove anos depois das bombas, o Japão recebe o mundo. Como? Primeiro, porque os americanos escrevem uma constituição que renuncia à guerra, e o país troca o quartel pela fábrica.",
  "constitution|Round-white-head cartoon Japanese and American officials of 1946 around a table with a thick blank document, serious but calm" + SEMTXT,
  "soldier_to_worker|Symbolic split scene: on the left a pile of old plain helmets, on the right round-white-head cartoon workers of the 1950s in a busy factory" + SEMSIMB)
b("E aí ele faz o que sempre fez: copia e melhora. Rádio, carro, televisão. Em mil novecentos e sessenta e oito, já é a segunda maior economia do mundo.",
  "factory_radios|A 1960s Japanese factory line with round-white-head cartoon workers in white caps assembling small transistor radios" + SEMTXT,
  "cars_port|Hundreds of small 1960s cars lined up at a Japanese port waiting to be loaded onto a cargo ship" + SEMTXT,
  "tv_family|A 1960s family of round-white-head cartoon people gathered around a new television set in a small living room" + SEMTXT)
b("Tente contar quantas coisas japonesas existem na sua casa agora. O país que trancou a porta por dois séculos agora queria entrar na sua sala, de preferência dentro de uma televisão.",
  f"guide_living_room|{GUIA} in a modern living room surrounded by a game console, a camera, a car key and a television, counting on his fingers, comic" + SEMTXT,
  "tv_door|Symbolic comic scene: a tiny samurai stepping out of an old television screen into a modern living room, waving" + SEMTXT)
b("§ Depois vem a crise dos anos noventa, e hoje o desafio vem de dentro: quase três em cada dez japoneses têm mais de sessenta e cinco anos. Então, e a pergunta do começo?",
  "tokyo_today|Modern Tokyo at dusk with skyscrapers and busy streets, neon lights as plain colored shapes, no readable signs" + SEMTXT,
  "elderly_park|Round-white-head cartoon elderly Japanese people doing morning exercises together in a park with cherry trees in bloom" + SEMTXT,
  "old_young|A round-white-head cartoon Japanese grandmother and her grandchild walking together on a quiet street, warm light" + SEMTXT)

# ───────────────────────── FECHO (≤ 45 s) ─────────────────────────
cap("Fecho")
b("§ O mar dava tempo. O vento ajudou uma noite. O resto foi escolha: o Japão deixava entrar ideias e fechava a porta quando quem entrava queria mandar.",
  "wall_dawn_final|The old stone wall on the Japanese beach at dawn, calm sea, a single pine tree, peaceful",
  "gate_half_open|The huge old wooden Japanese gate in the calm sea, half open, warm golden light coming through",
  "wind_cloud_hook")
b("Quando o mar virou estrada, copiou o invasor para não ser invadido, e virou o invasor, até mil novecentos e quarenta e cinco. Sorte foi uma noite. O resto foi escolha.",
  "sea_road|Symbolic scene: the sea between Japan and the world turning into a wide road full of ships of all eras, seen from above" + SEMBAND,
  "black_ships", "wall_dusk")
b("[warm] Talvez a pergunta nunca tenha sido quem conseguia entrar. E sim quem decidia abrir a porta. E você: qual virada do Japão mais te surpreendeu? Conta aí nos comentários.",
  f"guide_gate|{GUIA} standing in front of the old wooden Japanese gate on the beach, holding the handle and smiling at the viewer" + SEMSOL,
  "sunrise_islands#aberto")

# Grafia para a VOZ (o Fish lê como português). Conferir no teste de nomes (qa/pronuncia/).
# blocos.json leva "texto" (falado, vai ao Fish) e "tela" (grafia correta: legendas e SCRIPT).
FALA = [("Kublai Khan", "Cublai Cã"), ("Gêngis", "Gêngis"), ("kamikaze", "camicáze"), ("jomon", "djômon"),
        ("kofun", "kôfun"), ("Yamato", "Iamáto"), ("Amaterasu", "Amaterássu"), ("Yang", "Iáng"), ("Nara", "Nára"),
        ("Quioto", "Quióto"), ("Murasaki Shikibu", "Murassáki Xikíbu"), ("Genji", "Guêndji"), ("kana", "kána"),
        ("Hakata", "Rakáta"), ("Takashima", "Takaxíma"), ("Tanegashima", "Taneguaxíma"), ("Arigatô", "Arigatô"),
        ("pan", "pân"), ("Oda Nobunaga", "Ôda Nobunága"), ("Nagasaki", "Nagassáki"), ("Tokugawa", "Tokugáua"),
        ("Edo", "Êdo"), ("mangá", "mangá"), ("Matthew Perry", "Méthiu Péri"), ("Meiji", "Mêidji"),
        ("Yokohama", "Iokorráma"), ("Kasato Maru", "Kassáto Máru"), ("Manchúria", "Manchúria"),
        ("Nanquim", "Nanquim"), ("Pearl Harbor", "Pérl Rárbor"), ("Hiroshima", "Iroxíma")]
def fala(t):
    for a, z in FALA: t = re.sub(r"(?<![\wÀ-ú])" + re.escape(a) + r"(?![\wÀ-ú])", z, t)
    return t

IDEIA = set()
THUMB = None   # thumb nasce do conceito aprovado no crivo (EMBALAGEM.md): arte na etapa 2 (skill thumbnail)

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
    (out / "STORYBOARD.md").write_text("\n".join(linhas) + "\n")
    print(json.dumps(stats, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
