#!/usr/bin/env python3
"""Fonte única do 012-portugal (17/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

9º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
2º com ÂNGULO próprio (ANGULO.md, 17/11/2026): "a linha" (a fronteira luso-espanhola como personagem; Olivença abre e fecha).
EMBALAGEM.md aprovada no crivo r2:
  A/T1 "A fronteira de Portugal é QUASE a mesma desde 1297. Como?" + thumb rosto-emocao (fiscal espantado diante do marco que falta, "CADÊ?")
  B/T2 "Como uma LINHA protegeu Portugal (até o dia em que cedeu)" + thumb objeto-simbolo (marco de granito P|E sobre a linha, "700 ANOS")
  C/T3 "Por que Portugal ainda existe? A resposta tem 1.200 KM" + thumb mapa-lugar (escala Pernambuco × Portugal × Espanha, "PERNAMBUCO É MAIOR")
Hook: os marcos numerados (frase dos 1.200 km ≤ 0:30) → o salto de ~cem números diante de Olivença (1801) → PERGUNTA CENTRAL (≤ 0:50,
  com o mapa de escala na tela) → "e por que aqui ela cedeu?" → "essa é a história inteira" → 1 "guarde" (os marcos que faltam) → era 1.
Fio condutor: A LINHA. Cada era = um perigo para a linha → quem/que a segurou → o novo perigo.
  Peça 1 (cap. 3): assinada cedo, quando o vizinho era um menino (1297).   Peça 2 (cap. 4): quando Castela veio pela coroa, foi gente que segurou (1383).
  Peça 3 (cap. 5): sem espaço em terra, a disputa foi para o mar (1494).   "A pergunta fica mais difícil" (cap. 6): a coroa atravessa, a linha fica.
  Peça 4 (cap. 7): pedra, pólvora e gente teimosa (Elvas).   Onde cedeu (cap. 8): 1801, quando ninguém olhava.   Fecho: a linha + quem a segurou.
Crivo r2 (acréscimo): a LINHA é de 1297; os MARCOS numerados vêm de 1864–1926. Nunca dizer nem mostrar que as pedras têm 700 anos.
Neutralidade: Olivença com a posição de cada governo (sem defender devolução); guerras, 1383, Salazar/Franco e a guerra colonial sem humor
  sobre vítimas e sem imagem gráfica. Fecho no presente com 1 frase neutra.

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1297") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006–011).
Imagens: Codex (canal.yaml visual.gerador: codex; fallback nano-banana). Prompts só de conteúdo; o estilo vem do canal.yaml.
  O Codex põe marcos fora de época e vaza as refs do Egito (visual.md 010/011): cada cena diz o que NÃO pode aparecer (IBER).
  Planos COMPOSTOS NO CÓDIGO na etapa 2 (o prompt é só fallback): `escala_pe_pt_es` (silhuetas reais na mesma escala, Natural Earth + IBGE,
  o mesmo asset da Thumb C) e os rótulos de mapa (labels.jsx).
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (006–011: ~128 ppm com pausas)
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
TITULO = "A história INTEIRA de Portugal"
PERGUNTA = "Como um país menor que Pernambuco segurou a mesma fronteira com a Espanha por setecentos anos?"
PROMESSA = ("Como um país menor que Pernambuco segurou quase a mesma fronteira com a Espanha por setecentos anos, e onde, e por que, "
            "ela cedeu uma única vez (Olivença, 1801) (EMBALAGEM.md r2).")
TITULOS = ('T1 "A fronteira de Portugal é QUASE a mesma desde 1297. Como?" / T2 "Como uma LINHA protegeu Portugal (até o dia em que cedeu)" / '
           'T3 "Por que Portugal ainda existe? A resposta tem 1.200 KM"')

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None):
    ideia = t.startswith("§")
    B.append({"t": t.lstrip("§ ").strip(), "s": list(s), "card": card, "ideia": ideia})

# ───────── regras de prompt (Codex/nano-banana) ─────────
MAPA = ("painted like a blank parchment terrain map seen from directly above, only coastlines, seas, rivers, mountains and flat colored areas, "
        "completely blank with no writing anywhere, no letters, no words, no labels, no symbols, no compass, no border, no frame")
SEMTXT = ", no readable writing, no letters anywhere, no numbers, no signs, no boards"
SEMBAND = ", no flags, no banners, no coats of arms, no heraldic shields"
GUERRA = ", no blood, no wounds, no bodies, no violence shown"
IBER = (", strictly Portugal and Spain: Iberian landscape with granite hills, cork oaks, olive trees and whitewashed villages, "
        "NO pyramids, NO palm trees, NO pharaoh headdress, NO desert dunes, NO Roman or Greek ruins")
MED = ", medieval Iberia: stone castles and walled towns, no modern objects, no cars, no electric lines, no glass windows"
SEC15 = ", late 15th century: wooden sailing ships, no modern objects, no steamships"
SEC17 = ", 17th century: no modern objects, no cars, no electric lines"
MODERNO60 = ", 1960s Portugal: no smartphones, no modern cars, no modern logos"
# Personagens (regra da bíblia: nada de rosto descrito; "round-white-head cartoon …"; nomes reais só no rótulo do código)
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes, wearing an ordinary brown felt hat and a plain brown jacket"
AFONSO = ("a round-white-head cartoon young knight of 1128, under twenty, Afonso Henriques, with a simple flat short dark beard shape, "
          "chainmail and a plain white surcoat")
TERESA = "a round-white-head cartoon noblewoman of 1128, Countess Teresa, stern, with a white veil, a thin gold circlet and a long red dress"
DINIS = "a round-white-head cartoon King Dinis of Portugal of 1297, about thirty-five, with a simple flat brown beard shape, a simple gold crown and a blue cloak"
FERNANDO4 = "a round-white-head cartoon boy king of eleven, Fernando IV of Castile, with a small gold crown slightly too big for his head and a red cloak"
MOLINA = "a round-white-head cartoon Queen María de Molina of 1297, a serious noblewoman with a white veil and wimple and a dark purple dress"
MESTRE = "a round-white-head cartoon João, Master of Avis, of 1383, a young man with a simple flat dark beard shape, in a dark tunic with a plain green cross"
ALVARO = "a round-white-head cartoon old Lisbon citizen of 1383, Álvaro Pais, with a white flat beard shape and a brown cloak, riding a brown horse"
POVO14 = "round-white-head cartoon Lisbon townspeople of 1383 (craftsmen, fishwives, porters) in simple medieval clothes"
FERNAO = "a round-white-head cartoon medieval chronicler of the 1430s in a dark robe, writing in a big book with a quill by a window"
CASTELA = "round-white-head cartoon Castilian knights of the 14th century in chainmail and red surcoats without symbols"
JOAO2 = "a round-white-head cartoon King João II of Portugal of 1494 with a simple flat dark beard shape, a black hat and a dark velvet cloak"
GAMA = "a round-white-head cartoon Vasco da Gama of 1498 with a long flat dark beard shape, a black cap and a dark doublet"
NAU = "Portuguese sailing ships of the 1490s (caravels and naus) with white square sails marked only with plain red crosses"
SEBASTIAO = "a round-white-head cartoon young King Sebastião of 1578, twenty-four, with a light blond hair shape, in shiny plate armor"
FILIPE2 = "a round-white-head cartoon King Philip II of Spain of 1580, dressed all in black with a white ruff collar and a short pointed grey beard shape"
NOBRES16 = "round-white-head cartoon Portuguese noblemen of 1581 in dark doublets, ruff collars and capes"
JOAO4 = "a round-white-head cartoon King João IV of Portugal of 1640 with a moustache and short beard shape, long dark hair shape and a lace collar"
SOLD17 = "round-white-head cartoon soldiers of the 1650s with simple morion helmets, buff leather coats and muskets"
ELVENSES = "round-white-head cartoon townspeople of Elvas of 1658, thin and tired, in simple 17th century clothes"
GODOY = "a round-white-head cartoon Manuel Godoy of 1801, a plump smiling Spanish minister with a powdered white hair shape and a blue coat with gold braid"
RAINHA_ES = "a round-white-head cartoon Queen María Luisa of Spain of 1801 with a tall powdered hair shape, a pale silk dress and a fan"
DIPLOM19 = "round-white-head cartoon European diplomats of 1815 in dark tailcoats, white cravats and powdered or short hair"
CONTRAB = "round-white-head cartoon Portuguese villagers of the 1950s in dark caps, berets and black shawls carrying heavy sacks on their backs"
EMIGR = "round-white-head cartoon young Portuguese men and women of the 1960s in simple worn clothes and caps, carrying small cardboard suitcases and bundles"
PASSADOR = "a round-white-head cartoon smuggler-guide of the 1960s in a dark beret and a heavy coat, holding a small lantern"
MILIT74 = "round-white-head cartoon young Portuguese soldiers of 1974 in olive-green uniforms with red carnations in the barrels of their rifles, smiling"
POVO74 = "a joyful round-white-head cartoon crowd of Lisbon in 1974 holding red carnations, men in shirts and women in dresses"

# ───────────────────────── HOOK (os marcos que faltam) ─────────────────────────
cap("Hook")
b("[serious] Portugal e Espanha. São mil e duzentos quilômetros de fronteira, marcados com pedras numeradas. Imagine você seguindo os números, um por um, pela beira de um rio.",
  "markers_row|A long row of low identical light-grey granite border marker stones with square bases and low pyramid tops, running along a quiet riverbank across the countryside, morning light" + IBER + SEMTXT + SEMBAND,
  "border_aerial|A wide aerial view of the countryside where Portugal meets Spain: rolling hills, cork oaks, a winding river, and a thin line of small white stones running along it to the horizon" + IBER + SEMTXT,
  "marker_close|Close view of one light-grey granite border marker stone with a square base and a pyramid top in dry grass, plain smooth faces" + IBER + SEMTXT,
  "markers_walk|Back view of a small round-white-head cartoon walker with a backpack following a path of small stone markers along a river, comic and curious" + IBER + SEMTXT,
  "river_border|A calm river between two banks of Iberian countryside, one bank greener and one golden, morning mist" + IBER + SEMTXT)
b("Oitocentos. Oitocentos e um. [break] E aí as pedras somem. São uns cem marcos que nunca foram postos.",
  "marker_801|A single granite border marker stone on a riverbank seen from the side, the path ahead along the river completely empty, late afternoon light" + IBER + SEMTXT + "@@MARCO 801",
  "markers_gap|A riverbank path where a row of small stone markers suddenly stops and the grass continues empty for a long way, dramatic" + IBER + SEMTXT,
  f"guide_gap|{GUIA} standing at the last stone marker of a row, looking at the empty riverbank ahead, scratching his head, comic" + IBER + SEMTXT,
  "empty_hole|Close view of an empty hole in the earth on a riverbank where a stone marker should be, grass around it" + IBER + SEMTXT)
b("Só que, do outro lado do rio, fica Olivença: calçada portuguesa, igreja portuguesa, placas em espanhol.",
  "olivenca_view|A small whitewashed Iberian town on a low hill across a river, a castle tower and a church tower, seen from the opposite bank" + IBER + SEMTXT + SEMBAND + "@@OLIVENÇA",
  "olivenca_pavement|Close view of a cobbled square paved with black and white stone mosaic patterns in waves, typical Portuguese pavement, whitewashed houses" + IBER + SEMTXT,
  "olivenca_church|A white church with an ornate carved stone doorway with twisted rope-like columns in a small Iberian town square, sunny" + IBER + SEMTXT + SEMBAND,)
b("A Espanha governa Olivença desde mil oitocentos e um. Mas Portugal nunca reconheceu isso formalmente. No resto do caminho, a linha é quase a mesma desde mil duzentos e noventa e sete.",
  "olivenca_castle|The old castle keep of a small whitewashed Iberian border town at sunset, seen from below" + IBER + SEMTXT + SEMBAND,
  "olivenca_street|A narrow whitewashed street of a small Iberian border town with flower pots, iron balconies and an old man on a bench, afternoon light" + IBER + SEMTXT + SEMBAND,
  "two_ministries|Symbolic scene: two round-white-head cartoon officials in dark suits sitting at two separate desks back to back, each holding an old map and refusing to look at the other, comic" + SEMTXT + SEMBAND,
  "map_iberia_line|Map of the Iberian Peninsula with the land border between Portugal and Spain drawn as a thin bright golden line from north to south, " + MAPA,
  "border_map_old|An old 18th century hand-drawn map of a river border lying on a desk with a magnifying glass, only illegible decorative marks" + SEMTXT,
  "line_old_new|Symbolic scene: an old medieval parchment and a modern paper map lying side by side on a table, the same thin line drawn on both" + SEMTXT,
  card="1801")
b("Então fica a pergunta: como um país menor que Pernambuco segurou a mesma fronteira com a Espanha por setecentos anos? [break] E por que, justamente aqui, ela cedeu?",
  "escala_pe_pt_es|Flat comparison graphic on plain light parchment: three flat land silhouettes with thick black outlines at the same scale, a long thin green state shape on the left, a small golden country shape in the middle, and a huge dark grey country shape attached to the right of the golden one, a tiny round-white-head cartoon man standing with crossed arms on the golden shape" + SEMTXT + SEMBAND,
  "giant_neighbor|Symbolic comic scene: a tiny round-white-head cartoon man standing with crossed arms next to a giant round-white-head cartoon man who leans over him, on a line drawn on the ground" + SEMTXT + SEMBAND,
  "olivenca_dusk|A small whitewashed hilltop town across a river at dusk, the first lights in the windows, a single stone marker in the foreground" + IBER + SEMTXT + SEMBAND,
  "pernambuco_coast|The coast of Pernambuco, Brazil, with a long beach, coconut palms, reefs and turquoise water, seen from above, no people" + SEMTXT + SEMBAND,
  f"guide_question|{GUIA} sitting on a granite border stone, chin on hand, thinking hard, comic" + IBER + SEMTXT)
b("Essa é a história inteira de Portugal. Guarde esses marcos que faltam: eles voltam. E tudo começa com uma briga de família, na beira de outro rio.",
  "river_dawn_hook|A quiet river at dawn between two banks of granite hills, one small stone marker standing alone on the bank" + IBER + SEMTXT,
  "minho_river|The wide green Minho river between forested hills in northern Iberia at dawn, mist, stone villages on both banks" + IBER + MED + SEMTXT,
  "minho_bridge_old|An old medieval stone bridge over a green river in northern Portugal, misty morning" + MED + IBER + SEMTXT,
  "family_fight_hint|Symbolic comic scene: a medieval mother and her grown son glaring at each other across a long wooden table, a goblet knocked over" + MED + SEMTXT + SEMBAND,
  "guimaraes_castle|A small medieval stone castle on a rocky green hill in northern Portugal in the 12th century, a keep and battlements" + MED + IBER + SEMTXT + SEMBAND)

# ───────────────────────── 1. UMA LINHA NO RIO ─────────────────────────
cap("1. Uma linha no rio")
b("§ Valença, na margem do rio Minho. Do outro lado da água, a um grito de distância, fica Tui, na Galiza. Imagine dois pescadores do século doze, um em cada margem: mesma língua, mesmo peixe, mesma reza.",
  "valenca_tui|Two small medieval walled towns facing each other across the wide green Minho river, each on its own hill with a stone church, 12th century, misty morning" + MED + IBER + SEMTXT + SEMBAND,
  "fishermen_banks|Two round-white-head cartoon medieval fishermen in small wooden boats on a green river, one near each bank, waving and talking to each other" + MED + IBER + SEMTXT,
  "fish_same|Close view of two baskets of the same silver river fish on two wooden piers facing each other across water" + MED + IBER + SEMTXT,
  "two_chapels|Two small Romanesque stone chapels on opposite banks of a river, bells ringing at the same time, birds flying" + MED + IBER + SEMTXT + SEMBAND,
  "minho_villages|Two small stone villages facing each other across the Minho river, vineyards on the slopes, church bells" + MED + IBER + SEMTXT + SEMBAND,
  "market_two_banks|A medieval riverside market with round-white-head cartoon peasants trading fish and bread from boats between the two banks" + MED + IBER + SEMTXT)
b("Até que, em mil cento e vinte e oito, um rapaz de menos de vinte anos, Afonso Henriques, vence as tropas da própria mãe e fica com o condado de Portugal, um pedaço do reino de Leão. Pois é: o primeiro inimigo de Portugal era da família.",
  f"afonso_horse|{AFONSO}, on a horse at the front of his small army, determined" + MED + IBER + SEMBAND + "@@AFONSO HENRIQUES",
  "map_condado|Map of the northwest of the Iberian Peninsula in the 12th century with a small county between the Minho and the Douro rivers painted in soft green and a larger kingdom around it in pale ochre, " + MAPA,
  "sao_mamede_field|Two small medieval armies of round-white-head cartoon knights facing each other across a green field near a castle in northern Portugal, summer of 1128" + MED + IBER + SEMBAND + GUERRA,
  f"teresa_tent|{TERESA}, standing in front of her tent with Galician noblemen, arms crossed" + MED + SEMBAND + "@@D. TERESA",
  "guimaraes_1128|Close view of a medieval stone keep of a small castle on a rocky hill with a group of horsemen riding out of the gate, 1128" + MED + IBER + SEMTXT + SEMBAND,
  "leon_court|The court of the medieval kingdom of León in 1128, a stone throne room with round-white-head cartoon nobles, seen from far away" + MED + SEMTXT + SEMBAND,
  f"afonso_wins|{AFONSO}, raising his sword after a battle on a green field, his soldiers cheering" + MED + IBER + SEMBAND + GUERRA,
  f"mother_son_comic|Symbolic comic scene: {TERESA} leaving on horseback with her nose in the air while {AFONSO} waves goodbye awkwardly" + MED + IBER + SEMBAND,
  card="1128")
b("Então Afonso passa a se chamar rei. Em mil cento e quarenta e três, em Zamora, o primo dele, rei de Leão, aceita. Agora repare no mapa: ao norte, a linha é exatamente aquele rio entre os dois pescadores.",
  f"afonso_king|{AFONSO}, a few years older, now wearing a simple gold crown, sitting on a wooden throne" + MED + SEMBAND,
  "afonso_letter|Close view of a medieval royal letter with a heavy wax seal on a wooden table, a crown beside it" + MED + SEMTXT,
  "zamora_town|A medieval walled Castilian town on a rocky hill above a wide river with a Romanesque cathedral dome, 1143" + MED + IBER + SEMTXT + SEMBAND,
  "zamora_meeting|Two round-white-head cartoon medieval kings, cousins, shaking hands inside a stone hall in 1143, monks and knights around" + MED + SEMTXT + SEMBAND,
  "teresa_leaves|A small medieval procession of a noblewoman on horseback leaving a castle under grey skies, servants carrying chests" + MED + IBER + SEMTXT + SEMBAND,
  "map_minho|Map of the northwest of the Iberian Peninsula with the Minho river highlighted as a bright blue line between two lands, " + MAPA,
  "minho_boats|Small wooden boats crossing the Minho river between two stone villages in the 12th century, fishermen waving to each other" + MED + IBER + SEMTXT,
  card="1143")
b("Dos dois lados do Minho se fala a mesma língua, o galego-português. A linha vai separando essa língua aos poucos, em séculos. Se você já ouviu um galego falar, sabe: dá para entender quase tudo.",
  "two_villagers|Two round-white-head cartoon medieval peasants on opposite banks of a narrow river chatting happily across the water" + MED + IBER + SEMTXT,
  "manuscript_songs|Close view of an illuminated medieval songbook page with a drawing of a troubadour with a lute, the text area only as illegible decorative marks" + SEMTXT,
  f"guide_galician|{GUIA} talking with a round-white-head cartoon modern Galician fisherman on a pier, both laughing, understanding each other, comic" + IBER + SEMTXT,
  "galician_today|A modern Galician fishing village with granite houses, small colorful boats and a green river mouth, sunny" + IBER + SEMTXT + SEMBAND,
  "river_split_time|Symbolic scene: the same river seen in three moments from left to right, medieval boats, 18th century boats and modern small boats, both banks always talking" + IBER + SEMTXT)
b("Só que uma linha no norte não basta. Ao sul, não existe linha nenhuma. Lá embaixo ainda mandam os muçulmanos, e Lisboa é deles.",
  "map_south_open|Map of the Iberian Peninsula in 1140 with a small Christian kingdom in the north painted green and the whole south painted in soft ochre with no line between them, " + MAPA,
  "lisbon_moorish|Medieval Muslim Lisbon in 1140 seen from the Tagus river: a walled hill with a castle on top, white houses and a mosque with a minaret, boats on the river" + MED + IBER + SEMTXT + SEMBAND,
  "tagus_boats|Small medieval boats with triangular sails on the wide Tagus river in front of a walled hill city at sunset" + MED + IBER + SEMTXT + SEMBAND,
  "moorish_walls|Close view of the strong stone walls and gate of a medieval Muslim city on a hill, guards on top" + MED + SEMBAND + GUERRA,
  f"afonso_looks_south|{AFONSO}, wearing his simple crown, standing on a hill and looking south toward a distant walled city, worried" + MED + IBER + SEMBAND)

# ───────────────────────── 2. A LINHA DESCE ATÉ O MAR ─────────────────────────
cap("2. A linha desce até o mar")
b("§ Porto, verão de mil cento e quarenta e sete. Uma frota de cruzados ingleses, flamengos e alemães, a caminho de Jerusalém, para na cidade para se abastecer. O bispo da cidade sobe num púlpito improvisado e faz um pedido.",
  "crusader_fleet|A big medieval fleet of round wooden cog ships with white sails arriving at the mouth of the Douro river at Porto in 1147, a small stone town on the hill" + MED + IBER + SEMBAND + SEMTXT,
  "porto_1147|The small medieval town of Porto in 1147 on a steep hill above the Douro river, a stone cathedral on top, ships below" + MED + IBER + SEMTXT + SEMBAND,
  "porto_quay|A busy medieval quay on the Douro river at Porto with crusader ships tied up and round-white-head cartoon townspeople selling bread and wine to sailors" + MED + IBER + SEMTXT + SEMBAND,
  "bishop_sermon|A round-white-head cartoon medieval bishop with a mitre speaking from a simple wooden platform to a crowd of round-white-head cartoon crusaders on a riverbank" + MED + SEMTXT + SEMBAND,
  "crusader_knights|Round-white-head cartoon English and Flemish crusaders of 1147 in chainmail stepping off their ships onto a stone quay, curious" + MED + SEMBAND,
  "crusaders_listen|Round-white-head cartoon crusaders of 1147 in chainmail and plain cloaks listening with arms crossed, skeptical, comic" + MED + SEMBAND,
  card="1147")
b("Por que ir até Jerusalém, se tem infiel aqui do lado? E ainda com direito ao saque. Os cruzados topam. Em outubro, depois de quatro meses de cerco, Lisboa se rende.",
  "crusaders_cheer|Round-white-head cartoon crusaders raising their fists and cheering on a riverbank, a bishop smiling, comic" + MED + SEMBAND,
  "lisbon_siege|The siege of medieval Lisbon in 1147 seen from far away: ships on the Tagus river, a wooden siege tower against the walls of a hill city, camps around" + MED + IBER + SEMBAND + GUERRA,
  "siege_camp|A medieval crusader camp of tents in front of the walls of a hill city by a wide river, cooking fires, 1147" + MED + IBER + SEMBAND + SEMTXT,
  "siege_tower|A tall wooden siege tower on wheels being pushed toward stone city walls by round-white-head cartoon soldiers" + MED + SEMBAND + GUERRA,
  "lisbon_gate_open|The gates of a medieval walled hill city opening, round-white-head cartoon people walking out with bundles, knights waiting, serious" + MED + IBER + SEMBAND + GUERRA)
b("§ Aí a linha começa a descer. Se você olhar o mapa, ela desce cidade por cidade, castelo por castelo, por cem anos. Até que, em mil duzentos e quarenta e nove, Afonso Terceiro toma Faro, lá no Algarve.",
  "map_line_south|Map of the Iberian Peninsula showing a green Christian kingdom in the west growing southward in three soft shades, a thin golden line moving down toward the southern coast, " + MAPA,
  "castles_chain|A chain of small medieval stone castles on hills one after another toward the south, across a dry golden plain" + MED + IBER + SEMTXT + SEMBAND,
  "faro_1249|The small walled medieval town of Faro in 1249 by a calm lagoon and the sea, round-white-head cartoon Portuguese knights at the gate" + MED + IBER + SEMTXT + SEMBAND + GUERRA,
  "afonso3|A round-white-head cartoon King Afonso III of Portugal of 1249 with a simple flat beard shape and a gold crown, on horseback at a seaside town gate" + MED + IBER + SEMBAND + "@@AFONSO III",
  card="1249")
b("E olhe o que acontece: a linha bate no mar. Ao sul, água. A oeste, água. Portugal acabou de crescer. [break] Literalmente: não tem mais para onde ir.",
  "algarve_coast|The golden cliffs and beaches of the Algarve coast with the open blue ocean, a small medieval watchtower on a cliff" + MED + IBER + SEMTXT,
  "map_portugal_1249|Map of the Iberian Peninsula in 1249 with Portugal complete in green along the Atlantic coast, from the Minho to the Algarve, and the rest in pale ochre, " + MAPA,
  f"guide_coast|{GUIA} standing at the edge of a cliff above the ocean, looking down at the water, then shrugging, comic" + IBER + SEMTXT,
  "knight_beach|A round-white-head cartoon medieval knight standing on a beach with the waves at his feet, looking at the endless ocean, puzzled, comic" + MED + IBER + SEMBAND)
b("O problema é o leste. Do outro lado está Castela, quatro, cinco vezes maior. E Castela não tem pressa nenhuma de dizer onde termina Portugal.",
  "map_castile_big|Map of the Iberian Peninsula in the late 13th century with a narrow green kingdom in the west and a huge kingdom painted in deep red covering most of the center, " + MAPA,
  f"castile_army|{CASTELA}, a big army camped on a dry plain under a hot sky, tents and horses" + MED + IBER + SEMBAND,
  "border_castles|Two medieval stone castles on two hills facing each other across a valley, one smaller than the other" + MED + IBER + SEMTXT + SEMBAND,
  "shepherd_confused|A round-white-head cartoon medieval shepherd with his sheep in a valley between two castles, not sure which side he is on, comic" + MED + IBER + SEMTXT)

# ───────────────────────── 3. UM TRATADO COM UM MENINO ─────────────────────────
cap("3. Um tratado com um menino")
b("§ Alcanizes, setembro de mil duzentos e noventa e sete. Numa vila de Castela, perto da raia, dois reis vão assinar um papel. De um lado, Dom Dinis, rei de Portugal, trinta e cinco anos.",
  "alcanices_town|A small medieval walled town on a dry plateau in Castile in 1297, a stone church and a castle, autumn light" + MED + IBER + SEMTXT + SEMBAND,
  "treaty_hall|A medieval stone hall with a long wooden table, a parchment, a quill and wax seals, nobles and clerics standing around" + MED + SEMTXT + SEMBAND,
  f"dinis_arrives|{DINIS}, arriving at the hall with his councilors, confident" + MED + SEMBAND + "@@D. DINIS",
  "parchment_seals|Close view of a medieval parchment treaty with two red wax seals hanging from cords, only illegible decorative marks" + SEMTXT,
  card="1297")
b("Do outro lado, Fernando Quarto de Castela. Onze anos. Quem governa por ele é a mãe, Maria de Molina, apertada por guerras e por nobres rebeldes. Imagine negociar a fronteira do seu país com uma criança, e com a mãe dela com pressa.",
  f"fernando_boy|{FERNANDO4}, sitting on a big chair with his feet not touching the floor" + MED + SEMBAND + "@@FERNANDO IV",
  f"molina|{MOLINA}, standing behind her son's chair, tired and worried, reading letters" + MED + SEMTXT + SEMBAND + "@@MARIA DE MOLINA",
  "rebel_nobles|Round-white-head cartoon Castilian noblemen of 1297 arguing and pointing fingers in a castle courtyard, rebellious" + MED + SEMBAND,
  f"dinis_smiles|{DINIS}, smiling across the table at a little boy king, comic" + MED + SEMBAND,
  "boy_quill|Close view of a small child's hand holding a big quill above a parchment, a woman's hand guiding it" + MED + SEMTXT)
b("Então Dinis aproveita: leva as terras de Riba-Côa e fecha o desenho da linha. Setecentos anos depois, quase toda a linha continua onde aquele menino a assinou.",
  "map_ribacoa|Map of the Portugal–Castile border in 1297 with a small region east of the Côa river highlighted in bright green joining Portugal, " + MAPA,
  "ribacoa_land|Granite hills and small fortified villages above a deep river valley in the Côa region, dry grass and almond trees" + MED + IBER + SEMTXT + SEMBAND,
  "map_line_today|Map of the Iberian Peninsula with the modern Portugal–Spain land border drawn as a thin golden line, almost the same shape as an older faded line beneath it, " + MAPA,
  "markers_row#detalhe-centro")
b("Essa é a primeira peça da resposta: Portugal pôs a linha no papel quando teve a chance, com data, selo e testemunha. E linha assinada é linha que dá para cobrar de qualquer rei que vier depois.",
  f"dinis_parchment|{DINIS}, holding up a sealed parchment with satisfaction" + MED + SEMTXT + SEMBAND,
  "parchment_seals#detalhe-alto",
  "puzzle_piece|Symbolic scene: a big golden puzzle piece being placed into an old parchment map, only one piece filled" + SEMTXT,
  "map_line_today#detalhe-alto")
b("Só que um papel segura terra. Não segura coroa. E os reis de Portugal e de Castela vivem casando entre si. [break] Um dia, um casamento vai fazer o que exército nenhum fez.",
  "royal_wedding|A medieval royal wedding in a stone cathedral, a round-white-head cartoon young king and princess holding hands in front of a bishop" + MED + SEMTXT + SEMBAND,
  "crown_parchment|Symbolic scene: a gold crown resting on top of an old parchment map, its shadow falling across the drawn line" + SEMTXT,
  "family_tree|Symbolic comic scene: a big tree whose branches end in small crowns from two kingdoms, tangled together" + SEMTXT + SEMBAND)

# ───────────────────────── 4. O GRITO EM LISBOA ─────────────────────────
cap("4. O grito em Lisboa")
b("§ Lisboa, outubro de mil trezentos e oitenta e três. No paço, morre o rei Fernando. A única filha, Dona Beatriz, é casada com o rei de Castela. E o problema é o contrato: Portugal vai junto, de herança.",
  "funeral_1383|A quiet medieval Portuguese royal chamber in 1383 with an empty bed, candles and a simple gold crown on a cushion, mourning nobles at the door" + MED + SEMTXT + SEMBAND,
  "beatriz_juan|A round-white-head cartoon young princess Beatriz and an older round-white-head cartoon King of Castile sitting together on thrones, a red-cloaked court around" + MED + SEMBAND,
  "crown_cart|Symbolic comic scene: a gold crown being loaded onto a cart that is about to leave toward the east" + MED + IBER + SEMTXT,
  "map_inherit|Map of the Iberian Peninsula where the red color of Castile is spreading over the narrow green kingdom in the west like spilled ink, " + MAPA,
  card="1383")
b("Castela não precisa atravessar a linha, porque basta esperar. [break] Em dezembro, em Lisboa, o Mestre de Avis entra no paço e mata ali mesmo o conde Andeiro, o homem forte da corte.",
  f"castile_waits|{CASTELA}, sitting relaxed by the border river, playing dice and waiting, comic" + MED + IBER + SEMBAND,
  f"mestre|{MESTRE}, walking fast through a dark stone corridor of a palace in Lisbon, determined" + MED + SEMBAND + "@@MESTRE DE AVIS",
  "palace_door|A heavy wooden palace door in medieval Lisbon slightly open, torchlight inside, a shadow on the floor, tense" + MED + SEMTXT + GUERRA,
  "palace_window|The window of a medieval palace in Lisbon at night with candlelight, people looking up from the street" + MED + SEMTXT + GUERRA)
b("Aí um homem, Álvaro Pais, sai a cavalo pelas ruas e grita: “Matam o Mestre! Acudam ao Mestre!” [break] O Mestre estava ótimo. Mas o grito funcionou: o povo sai de casa.",
  f"alvaro_ride|{ALVARO}, galloping through a narrow medieval street of Lisbon, shouting with his arm raised" + MED + SEMTXT + SEMBAND + "@@ÁLVARO PAIS",
  f"windows_open|{POVO14} opening windows and doors in a narrow medieval street at night, alarmed" + MED + SEMTXT,
  f"crowd_run|{POVO14} running up a steep street toward a palace with torches and tools, determined" + MED + SEMTXT + SEMBAND + GUERRA,
  f"mestre_balcony|{MESTRE}, appearing at a palace window alive and well, waving to the crowd below, slightly surprised, comic" + MED + SEMBAND)
b("Se você já viu um boato no grupo da família tirar todo mundo do sofá, entendeu mil trezentos e oitenta e três. Quem conta essa cena é o cronista Fernão Lopes, e ele chama aquela gente de arraia-miúda.",
  f"guide_phone|{GUIA} looking at a smartphone in a modern living room while his whole cartoon family jumps off the sofa, comic" + SEMTXT,
  f"fernao|{FERNAO}" + MED + SEMTXT + "@@FERNÃO LOPES",
  f"arraia|{POVO14}, a crowd of fishwives, carpenters and porters filling a square, cheering" + MED + SEMTXT + SEMBAND,
  "chronicle_book|Close view of a big medieval chronicle book open on a desk with a candle, a small drawing of a crowd on the page, the text only as illegible marks" + SEMTXT)
b("Foi ela que escolheu o rei. Dois anos depois, em Aljubarrota, com uns arqueiros ingleses ajudando, Castela perde a batalha e a vontade.",
  f"mestre_crowd|{MESTRE}, lifted on the shoulders of a cheering crowd of medieval townspeople" + MED + SEMBAND,
  "aljubarrota|The battle of Aljubarrota in 1385 seen from far away on a hilltop: a small army in a tight square with archers on the sides facing a much bigger army of knights, dust" + MED + IBER + SEMBAND + GUERRA,
  "archers|Round-white-head cartoon English longbow archers of 1385 in simple tunics, drawing their bows behind wooden stakes" + MED + SEMBAND + GUERRA,
  f"castile_retreat|{CASTELA}, riding away from a hilltop in disorder, dropping their lances, seen from behind" + MED + IBER + SEMBAND + GUERRA,
  card="1385")
b("Segunda peça da resposta: quando Castela veio pela coroa, quem segurou a linha não foi muralha. Foi gente. [break] Só que, com a linha segura, aparece outro problema: um reino pequeno, entre Castela e o mar, cresce para onde?",
  "arraia#médio-dir",
  "border_castles#detalhe-centro",
  "map_portugal_1249#detalhe-baixo",
  f"guide_squeezed|{GUIA} squeezed between a giant wall on one side and the sea on the other, arms out, comic" + IBER + SEMTXT)

# ───────────────────────── 5. A LINHA VAI PARA A ÁGUA ─────────────────────────
cap("5. A linha vai para a água")
b("§ Se por terra não dá, vai por água. Em mil quatrocentos e quinze, os portugueses atravessam o estreito e tomam Ceuta, na África. E aí, ano após ano, descem a costa, um cabo de cada vez.",
  "ceuta_fleet|A fleet of medieval Portuguese ships crossing the Strait of Gibraltar in 1415 toward a white walled city on the African coast" + MED + SEMBAND + SEMTXT,
  f"caravels_coast|{NAU} sailing along a dry African coastline with cliffs, one ship after another" + SEC15 + SEMBAND + SEMTXT,
  "map_capes|Map of the west coast of Africa with a dotted line going south along the coast, cape after cape, " + MAPA,
  "sailors_look|Round-white-head cartoon Portuguese sailors of the 15th century on deck looking at an unknown coast with curiosity and fear" + SEC15 + SEMBAND,
  card="1415")
b("E aí Castela também vai para o mar. Colombo volta em mil quatrocentos e noventa e três dizendo que achou as Índias, e o papa traça uma linha no oceano: cem léguas a oeste de Cabo Verde. Tudo depois dela, para Castela.",
  "columbus_back|A round-white-head cartoon Christopher Columbus of 1493 in a dark cloak presenting parrots and gold objects to the Castilian court, the court amazed" + SEC15 + SEMBAND + SEMTXT,
  "pope_line|A round-white-head cartoon Pope of 1493 in white robes and a tall papal tiara drawing a straight line with a long ruler on a huge parchment map of the Atlantic, comic" + SEC15 + SEMTXT,
  "map_100|Map of the Atlantic Ocean with a thin red vertical line close to the west coast of Africa, Africa on the right, an empty ocean on the left, " + MAPA,
  "castile_happy|Round-white-head cartoon Castilian courtiers of 1493 celebrating around a map, comic" + SEC15 + SEMBAND)
b("Dom João Segundo faz o que Portugal sabe fazer melhor: discute a linha. [break] Em Tordesilhas, em mil quatrocentos e noventa e quatro, ela vai para trezentas e setenta léguas.",
  f"joao2|{JOAO2}, leaning over a map with a pointing finger, stubborn" + SEC15 + SEMTXT + SEMBAND + "@@D. JOÃO II",
  "tordesillas_table|Portuguese and Castilian ambassadors of 1494 arguing around a long table with a big map in a Castilian town hall, pushing a ruler back and forth, comic" + SEC15 + SEMTXT + SEMBAND,
  "map_370|Map of the Atlantic Ocean with a thin red vertical line moved far to the west, now crossing the eastern bulge of South America, " + MAPA,
  "seal_1494|Close view of two hands pressing a wax seal onto a parchment treaty on a table" + SEC15 + SEMTXT,
  card="1494")
b("Duzentas e setenta léguas de diferença. Repare onde elas caem: num pedaço de terra que nenhum europeu tinha pisado ainda. [break] É por causa dessa briga de fronteira no meio do mar que você está ouvindo este vídeo em português.",
  "map_370#detalhe-centro",
  "brazil_coast_1494|An untouched tropical coastline of South America in 1494 with a white beach and dense green forest, no ships, no people" + SEC15 + SEMTXT,
  f"guide_brazil|{GUIA} sitting on a modern Brazilian beach with a coconut, pointing at a thin red line drawn on the sand, comic" + SEMTXT + SEMBAND,
  "brazil_today|A modern Brazilian city street with people talking, a street market and colorful houses, bright daylight" + SEMTXT + SEMBAND)
b("Quatro anos depois, Vasco da Gama chega a Calecute, na Índia. Segundo o diário da viagem, dois mercadores de Túnis, que falavam castelhano, perguntam ao primeiro português que desce: o diabo te leve, quem te trouxe aqui?",
  f"gama_ships|{NAU}, three ships anchored off the green coast of Calicut, India, in 1498, palm trees on the Indian shore, local boats" + SEC15 + SEMBAND + SEMTXT,
  f"gama|{GAMA}, standing on deck looking at the Indian coast" + SEC15 + SEMBAND + "@@VASCO DA GAMA",
  "tunis_merchants|Two round-white-head cartoon North African merchants of 1498 in long robes and turbans in an Indian port market, shocked to see a European sailor, one pointing, comic" + SEC15 + SEMTXT + SEMBAND,
  "sailor_shore|A round-white-head cartoon Portuguese sailor of 1498 in a simple shirt stepping onto a busy Indian quay, nervous" + SEC15 + SEMTXT + SEMBAND,
  card="1498")
b("E o português responde: “Viemos buscar cristãos e especiaria.” [break] Terceira peça da resposta: sem espaço em terra, Portugal levou a disputa com Castela para a água. O problema: cerca de um milhão de pessoas para segurar um império do Brasil à Índia.",
  "spices_market|Sacks of pepper, cinnamon and cloves piled high in a colorful Indian market of 1498" + SEC15 + SEMTXT,
  "map_empire|Map of the world with small green dots along the coasts of Brazil, Africa and India connected by thin sea routes from a tiny Portugal, " + MAPA,
  "tiny_crew|Symbolic comic scene: a handful of round-white-head cartoon Portuguese sailors trying to hold the ropes of a gigantic sail as big as a mountain" + SEC15 + SEMTXT + SEMBAND,
  "lisbon_port_1500|The busy port of Lisbon around 1500 on the Tagus river with many sailing ships, warehouses and crowds" + SEC15 + IBER + SEMTXT + SEMBAND)

# ───────────────────────── 6. A COROA ATRAVESSA, A LINHA FICA ─────────────────────────
cap("6. A coroa atravessa, a linha fica")
b("§ Tomar, abril de mil quinhentos e oitenta e um. No convento dos antigos templários, um rei vestido de preto jura diante dos nobres portugueses. É Filipe Segundo, rei da Espanha, e agora também de Portugal.",
  "tomar_convent|A grand Renaissance convent with a round templar church on a green hill above a small Portuguese town in 1581" + IBER + SEMTXT + SEMBAND + "@@TOMAR",
  f"tomar_cortes|{FILIPE2}, standing in a great hall of a convent with tall windows, swearing an oath with his hand on a book, {NOBRES16} watching" + SEMTXT + SEMBAND,
  f"filipe2|{FILIPE2}, sitting on a dark throne in a gloomy palace, holding a crown in his lap, slightly smiling" + SEMBAND + "@@FILIPE II",
  card="1581")
b("Como ele chegou aqui? Três anos antes, o jovem rei Dom Sebastião sumiu numa batalha no Marrocos, sem deixar filho, e a coroa caiu no colo do tio. Castela consegue o que queria em mil trezentos e oitenta e três. E a nossa pergunta fica mais difícil.",
  f"sebastiao|{SEBASTIAO}, on a white horse in front of his army in a dry Moroccan plain, proud" + SEMBAND + GUERRA + "@@D. SEBASTIÃO",
  "alcacer_dust|A battlefield in a dry Moroccan plain in 1578 covered in a cloud of dust, seen from far away, abandoned lances and a riderless white horse" + SEMBAND + GUERRA + SEMTXT,
  "crown_lap|Symbolic comic scene: a gold crown falling from the sky into the lap of a king dressed in black" + SEMTXT + SEMBAND,
  "map_union|Map of the Iberian Peninsula in 1580 entirely painted in one deep red color, with a thin golden line still faintly visible on the western side, " + MAPA,
  card="1580")
b("Porque Filipe jura que Portugal continua um reino à parte, com leis, moeda e cargos portugueses. Segundo historiadores, até a alfândega da raia é abolida em mil quinhentos e oitenta e dois. Só que, em mil quinhentos e noventa e um, ela volta. A coroa atravessou a linha. A linha ficou.",
  "two_coins|Close view of two different old silver coins side by side on a wooden table, plain designs without letters" + SEMTXT,
  "customs_house|A small 16th century stone customs house on a dusty road by a river at the border, a wooden barrier and a clerk with a ledger, mule carts waiting" + IBER + SEMTXT + SEMBAND,
  "customs_closed_open|Symbolic scene: the same small stone customs house shown with its door shut and weeds, and beside it the same door open again with a clerk counting coins" + IBER + SEMTXT + SEMBAND)
b("Só que um rei da Espanha traz junto os inimigos da Espanha. Os holandeses, em guerra com Madri, vão atrás do açúcar onde ele estava: em Pernambuco. Se você já andou pelo Recife antigo, pisou numa cidade que foi holandesa por causa disso.",
  "dutch_fleet|A Dutch fleet of the 1630s with orange-white-blue striped sails arriving at a tropical harbor with a sandy reef" + SEC17 + SEMTXT,
  "sugar_mill|A 17th century sugar mill in Pernambuco with a big wooden water wheel and sugarcane fields, workers in the distance" + SEC17 + SEMTXT + SEMBAND,
  f"guide_recife|{GUIA} walking on a colorful cobbled street of old Recife with old houses and a river, looking at the facades, smiling" + SEMTXT + SEMBAND,
  card="1630")
b("Sessenta anos pagando guerras que não eram suas. Até que um grupo de nobres decide que chega. [break] O problema é que expulsar um rei é fácil. Difícil é aguentar o exército dele na porta.",
  f"nobles_plot|{NOBRES16}, plotting by candlelight around a table in a dark Lisbon house" + SEC17 + SEMTXT + SEMBAND,
  "tax_pile|Symbolic scene: a pile of coin bags being carried away from Lisbon on carts toward the east" + SEC17 + IBER + SEMTXT,
  "army_gate|A big army of the 17th century camped outside a city gate at dawn, tents and cannons, seen from the walls" + SEC17 + IBER + SEMBAND + GUERRA)

# ───────────────────────── 7. VINTE E OITO ANOS NA RAIA ─────────────────────────
cap("7. Vinte e oito anos na raia")
b("§ Lisboa, primeiro de dezembro de mil seiscentos e quarenta: um golpe no paço, e o duque de Bragança vira Dom João Quarto. Aí começa a parte difícil: vinte e oito anos de guerra, quase toda em cima da linha.",
  f"joao4|{JOAO4}, being acclaimed on a palace balcony above a square in Lisbon, a crowd cheering" + SEC17 + SEMBAND + "@@D. JOÃO IV",
  "lisbon_1640|The riverside palace square of Lisbon in 1640 full of round-white-head cartoon people throwing hats in the air" + SEC17 + IBER + SEMTXT + SEMBAND,
  "border_war|A dry border valley of the 1640s with small forts on both sides, soldiers patrolling, smoke from far away" + SEC17 + IBER + SEMBAND + GUERRA,
  card="1640")
b("§ Elvas, inverno de mil seiscentos e cinquenta e oito. Imagine uma cidade fechada dentro de muralhas em forma de estrela, a poucos quilômetros de Badajoz. Lá fora, o exército espanhol. Lá dentro, fome e peste.",
  "elvas_star|A Portuguese town on a hill surrounded by huge star-shaped fortress walls with pointed bastions and a deep dry moat, seen from above in winter" + SEC17 + IBER + SEMTXT + SEMBAND + "@@ELVAS",
  f"elvas_siege|{SOLD17}, a besieging army camped in trenches around star-shaped walls, cannons pointing at the town, grey winter sky" + SEC17 + IBER + SEMBAND + GUERRA,
  f"elvas_inside|{ELVENSES}, sharing small pieces of bread in a cold stone street inside the walls, serious and dignified" + SEC17 + IBER + SEMTXT + SEMBAND,
  card="1658")
b("Os sitiados aguentam três meses. Em catorze de janeiro de mil seiscentos e cinquenta e nove, chega um exército de socorro e rompe as linhas espanholas. Elvas fica portuguesa.",
  f"relief_army|{SOLD17}, a relief army marching through a frosty dawn toward a fortified town, determined" + SEC17 + IBER + SEMBAND + GUERRA,
  "lines_broken|A line of wooden siege fences and trenches broken open in the snow-dusted fields outside star-shaped walls, abandoned tents" + SEC17 + IBER + SEMBAND + GUERRA + SEMTXT,
  f"elvas_cheer|{ELVENSES}, cheering on top of the bastion walls at sunrise, waving hats" + SEC17 + IBER + SEMTXT + SEMBAND,
  card="1659")
b("As muralhas estão lá até hoje e viraram Patrimônio Mundial. Em mil seiscentos e sessenta e oito, a Espanha assina a paz e reconhece Portugal.",
  "elvas_today|The star-shaped fortress walls of Elvas today, green grass on the bastions, round-white-head cartoon tourists walking on top, bright blue sky" + IBER + SEMTXT + SEMBAND,
  f"guide_wall|{GUIA} standing on top of an old star-shaped fortress wall, shading his eyes and looking at a plain on the horizon" + IBER + SEMTXT + SEMBAND,
  "peace_1668|Portuguese and Spanish ambassadors of 1668 in wigs and lace collars signing a treaty at a table, relieved" + SEC17 + SEMTXT + SEMBAND,
  card="1668")
b("Quarta peça da resposta: a linha não se segurou sozinha. Foi pedra, pólvora e gente que não arredou pé, cidade por cidade. [break] E aí vem o perigo mais traiçoeiro de todos: a paz.",
  "elvas_star#detalhe-centro",
  "stubborn_people|Round-white-head cartoon Portuguese villagers of the 17th century standing with crossed arms on a wall, stubborn, comic" + SEC17 + IBER + SEMTXT + SEMBAND,
  "markers_row#médio-dir")
b("Com o ouro do Brasil chegando, Portugal passa um século de costas para a raia. Muralha precisa de soldado, e soldado custa caro. [break] O problema: quem para de olhar para a linha, um dia leva um susto nela.",
  "gold_ship|A big 18th century sailing ship unloading chests of gold at the port of Lisbon, officials counting" + IBER + SEMTXT + SEMBAND,
  "baroque_palace|A lavish 18th century baroque palace interior in Portugal with golden carved wood and round-white-head cartoon courtiers dancing" + SEMTXT + SEMBAND,
  "empty_bastion|An empty, overgrown star-shaped bastion with a rusty cannon and goats grazing, no soldiers" + IBER + SEMTXT + SEMBAND)

# ───────────────────────── 8. ONDE A LINHA CEDEU ─────────────────────────
cap("8. Onde a linha cedeu")
b("§ Alentejo, maio de mil oitocentos e um. A Espanha, aliada da França de Napoleão, invade o Alentejo. Mas a guerra dura só umas três semanas. Tão curta que ganhou nome de fruta.",
  "invasion_1801|Spanish soldiers of 1801 in white and blue uniforms with bicorne hats marching across a dry Alentejo plain with cork oaks" + IBER + SEMBAND + GUERRA + SEMTXT,
  "alentejo_villagers|Round-white-head cartoon Alentejo villagers of 1801 watching soldiers pass from behind a whitewashed wall, worried" + IBER + SEMTXT + SEMBAND,
  "orange_tree|A single orange tree full of bright oranges in a whitewashed courtyard in southern Portugal" + IBER + SEMTXT,
  card="1801")
b("Diz a tradição que Manuel Godoy, o homem forte de Madri, colheu ramos de laranjeira perto de Elvas e mandou para a rainha da Espanha. Daí, Guerra das Laranjas. Para Portugal, a fruta saiu cara.",
  f"godoy|{GODOY}, picking an orange branch from a tree in front of star-shaped fortress walls, very pleased with himself, comic" + IBER + SEMBAND + "@@MANUEL GODOY",
  f"queen_oranges|{RAINHA_ES}, receiving a basket of orange branches from a messenger in a palace, delighted" + SEMTXT + SEMBAND,
  "orange_receipt|Symbolic comic scene: a single orange on a silver plate next to a very long unrolled bill" + SEMTXT)
b("Então, no tratado de paz, assinado em Badajoz, Portugal entrega Olivença. Em mil oitocentos e quinze, o Congresso de Viena pede que a Espanha devolva. A Espanha não devolve, e diz que vale o tratado de Badajoz.",
  "badajoz_treaty|Diplomats of 1801 in powdered wigs and tailcoats signing a treaty at a table in a Spanish border town, one looking sad" + SEMTXT + SEMBAND,
  f"vienna_congress|{DIPLOM19}, sitting around a big round table covered with maps in a grand palace hall in Vienna, 1815" + SEMTXT + SEMBAND,
  "olivenca_view#médio-dir",
  card="1815")
b("Lembra dos marcos que faltam? Olhe de novo: é aqui. A linha cedeu justamente no tempo em que Portugal tinha parado de olhar para ela. [break] E esse buraco nunca foi fechado.",
  "markers_gap#detalhe-centro",
  "empty_hole#aberto",
  "map_olivenca|Map of the middle section of the Portugal–Spain border with a small area around a town on the east bank of a river highlighted in pale stripes, the border line missing there, " + MAPA)
b("Seis anos depois, é Napoleão que atravessa a raia, e a corte foge para o Brasil. Em mil oitocentos e vinte e dois, o Brasil vai embora. [break] Então Portugal fica de novo só com a linha e o mar. O problema é que o mundo lá fora mudou.",
  "french_cross|French soldiers of 1807 in blue coats and bicorne hats crossing a stone bridge over a river into Portugal, rain" + IBER + SEMBAND + GUERRA + SEMTXT,
  "court_ships|A fleet of sailing ships leaving the Tagus river at Lisbon in 1807 under grey skies, crowds on the quay" + IBER + SEMTXT + SEMBAND,
  "lonely_coast|A lonely Portuguese coast at sunset with the open ocean on one side and dry hills on the other, a single stone marker on a hill" + IBER + SEMTXT,
  card="1822")

# ───────────────────────── 9. MURO E PORTA ─────────────────────────
cap("9. Muro e porta")
b("§ Então o século vinte chega com Portugal humilhado pelos ingleses na África, sem rei a partir de mil novecentos e dez e, depois, com a ditadura de Salazar. Na Espanha, guerra civil e, depois, Franco.",
  "lisbon_1910|A Lisbon street of 1910 with trams and round-white-head cartoon people in hats reading newspapers, excited" + SEMTXT + SEMBAND,
  "dictator_office|A dark 1930s government office with a bare desk, a desk lamp and a single chair, rain on the window, no portraits" + SEMTXT + SEMBAND,
  "spain_1936|A dusty Spanish village of 1936 with empty streets and smoke on the horizon, serious" + IBER + SEMTXT + SEMBAND + GUERRA)
b("§ Lisboa, março de mil novecentos e trinta e nove. Os dois regimes assinam um pacto de amizade e não agressão. A linha vira um muro combinado: ninguém atravessa para mandar, e as duas ditaduras se protegem.",
  "pact_1939|Two round-white-head cartoon diplomats of 1939 in dark suits signing a document at a long table in a formal Lisbon room, stiff and serious" + SEMTXT + SEMBAND,
  "wall_line|Symbolic scene: a tall grey wall built exactly along a thin line on a green landscape, two watchtowers facing each other politely" + IBER + SEMTXT + SEMBAND,
  "border_post_50s|A small border post of the 1950s on a country road in Portugal: a striped barrier, a white guardhouse and a uniformed officer with a cap, no flags" + IBER + SEMTXT + SEMBAND,
  card="1939")
b("Só que muro, para quem mora na raia, é porta. Imagine: de noite, sacos de café atravessam a linha nas costas, do lado português para o espanhol. Em vilas como Marvão, o contrabando sustentou famílias inteiras.",
  f"smugglers_night|{CONTRAB}, walking in a line along a dark mountain path at night under the moon, quiet" + IBER + SEMTXT + SEMBAND,
  "coffee_sacks|Close view of rough sacks full of coffee beans hidden among rocks and bushes at night" + IBER + SEMTXT,
  "marvao|A white walled hilltop village on a granite crag above a wide valley at dusk, castle on top" + IBER + SEMTXT + SEMBAND + "@@MARVÃO")
b("E nos anos sessenta, gente também atravessa. Imagine pagar um passador para cruzar a pé a fronteira de noite, rumo à França, levando metade de uma fotografia rasgada. A outra metade fica com ele.",
  f"emigrants_path|{EMIGR}, following a guide on a dark mountain path at night with small suitcases, scared" + MODERNO60 + IBER + SEMTXT + SEMBAND,
  f"passador|{PASSADOR}, waiting at a crossroads at night, holding out his hand" + MODERNO60 + IBER + SEMTXT,
  "torn_photo|Close view of two hands holding the two halves of an old black-and-white family photograph torn in the middle, faces as simple cartoon shapes" + MODERNO60 + SEMTXT,
  card="1965")
b("Quando você chega, manda a sua metade para casa: é o recibo de que deu certo. Em quinze anos, cerca de um milhão e meio de portugueses saem do país, muitos assim, a salto.",
  "photo_letter|A round-white-head cartoon old mother in a black shawl in a Portuguese village kitchen opening an envelope and finding half of a photograph, tears of joy" + MODERNO60 + IBER + SEMTXT,
  "paris_bidonville|Round-white-head cartoon Portuguese immigrant workers of the 1960s on a construction site near Paris, carrying bricks, tired but smiling" + MODERNO60 + SEMTXT + SEMBAND,
  "village_empty|A small Portuguese mountain village of the 1960s with closed shutters, only old people sitting on doorsteps" + MODERNO60 + IBER + SEMTXT)
b("Enquanto isso, o regime luta para manter as colônias na África. O problema: um país não aguenta por muito tempo uma guerra longe de casa e uma porta fechada dentro dela.",
  "colonial_war|Round-white-head cartoon young Portuguese soldiers of the 1960s in green uniforms boarding a big grey ship at the port of Lisbon, families waving goodbye" + MODERNO60 + SEMTXT + SEMBAND,
  "letters_home|A pile of airmail letters with blank envelopes and a small radio on a kitchen table in a Portuguese house of the 1970s" + SEMTXT,
  "wall_line#detalhe-centro")

# ───────────────────────── 10. A CANCELA SOBE ─────────────────────────
cap("10. A cancela sobe")
b("§ Lisboa, vinte e cinco de abril de mil novecentos e setenta e quatro. Depois da meia-noite, uma canção toca no rádio: é a senha. Então os militares derrubam o regime quase sem tiros, e no ano seguinte as colônias na África ficam independentes.",
  "radio_night|An old 1970s radio glowing on a table in a dark room at midnight, a hand turning the dial" + SEMTXT,
  f"carnations|{MILIT74}, standing on a tank in a Lisbon square surrounded by people" + SEMTXT + SEMBAND,
  f"crowd_1974|{POVO74}, filling a wide Lisbon avenue in the morning sun" + SEMTXT + SEMBAND,
  card="1974")
b("§ Mosteiro dos Jerónimos, junho de mil novecentos e oitenta e cinco. Portugal assina a entrada na Comunidade Europeia. Repare: a Espanha assina a dela no mesmo dia. Em oitenta e seis, entram juntos.",
  "jeronimos|The white stone cloister of a Manueline monastery in Lisbon with intricately carved arches, sunny day" + IBER + SEMTXT + SEMBAND + "@@JERÓNIMOS",
  "signing_1985|A round-white-head cartoon Portuguese prime minister of 1985 in a dark suit and glasses signing a big document at a long table in a stone cloister, officials applauding" + SEMTXT + SEMBAND,
  "two_doors|Symbolic comic scene: two round-white-head cartoon men, one small and one big, walking through the same big open door at the same time, side by side" + SEMTXT + SEMBAND,
  card="1985")
b("§ Na raia, vinte e seis de março de mil novecentos e noventa e cinco. Nos postos, de Valença a Vila Real de Santo António, acaba o controle de passaporte. As cancelas sobem, e ficam lá em cima.",
  "barrier_up|A border post on a road between Portugal and Spain in 1995 with the striped barrier raised up, an officer waving cars through, sunny" + IBER + SEMTXT + SEMBAND,
  "empty_booth|An empty border control booth on a road with its door open and nobody inside, grass growing around it" + IBER + SEMTXT + SEMBAND,
  "bridge_river|A long modern road bridge over a wide river between two countries, cars crossing freely, blue sky" + IBER + SEMTXT + SEMBAND,
  card="1995")
b("Hoje, se você atravessa a ponte entre Elvas e Badajoz, o único aviso de que mudou de país é o seu celular: o relógio pula uma hora. [break] Então, setecentos anos de linha, e quem percebe é o telefone.",
  f"guide_clock|{GUIA} driving a small car across a bridge and staring at a phone on the dashboard showing a clock jumping forward, surprised, comic" + SEMTXT + SEMBAND,
  "phone_clock|Close view of a smartphone in a hand showing a simple clock icon with two clock hands moving, no numbers, a bridge outside the car window" + SEMTXT,
  "elvas_today#detalhe-alto")
b("Mas aí vem a última dúvida: uma linha que ninguém mais vigia ainda é uma fronteira?",
  "markers_row#aberto",
  "border_aerial#detalhe-baixo")

# ───────────────────────── FECHO (≤ 45 s) ─────────────────────────
cap("Fecho")
b("§ Então, como um país menor que Pernambuco segurou a mesma fronteira por setecentos anos? A resposta tem mil e duzentos quilômetros, e gente em cima deles: um rei que assinou cedo, o povo de Lisboa, os sitiados de Elvas.",
  "escala_pe_pt_es#aberto",
  "arraia#médio-esq",
  "elvas_cheer#aberto")
b("Talvez a pergunta certa nunca tenha sido como a linha aguentou os ataques. Porque ela abriu quando ninguém mais quis atravessar para mandar. [break] Em dois mil e vinte e seis, os cem marcos de Olivença continuam sem existir.",
  "barrier_up#detalhe-centro",
  "olivenca_dusk#aberto",
  "empty_hole#detalhe-baixo",
  card="2026")
b("[warm] Você sabia que a fronteira tinha esse buraco? Conta nos comentários.",
  f"guide_end|{GUIA} sitting on a granite border marker on a riverbank at sunset, waving at the viewer, a small whitewashed town across the river" + IBER + SEMTXT + SEMBAND)

# Grafia para a VOZ (o Fish lê como português). Conferir no teste de nomes (qa/pronuncia/).
# blocos.json leva "texto" (falado, vai ao Fish) e "tela" (grafia correta: legendas e SCRIPT).
FALA = [("Alcácer-Quibir", "Alcácer Quibir"), ("Riba-Côa", "Riba Côa"), ("Fernando Quarto", "Fernando Quarto"),
        ("Godoy", "Godói"), ("Jerónimos", "Jerônimos"), ("Calecute", "Calecute"), ("Túnis", "Túnis"),
        ("galego-português", "galego português"), ("arraia-miúda", "arraia miúda"), ("Andeiro", "Andêiro")]
def fala(t):
    for a, z in FALA: t = re.sub(r"(?<![\wÀ-ú])" + re.escape(a) + r"(?![\wÀ-ú])", z, t)
    return t

IDEIA = set()
THUMB = None   # thumbs nascem dos 3 conceitos aprovados no crivo (EMBALAGEM.md r2): arte na etapa 2 (skill thumbnail)

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
