#!/usr/bin/env python3
"""Fonte única da Etapa 1: roteiro + planos.

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
b("O Egito não é um país que tem um rio. [break] É um [emphasis] rio com um país em volta.",
  "nile_space_night|Satellite view of Egypt at night from space: a thin glowing line of lights following the Nile valley across a vast black desert, fanning out into the delta at the top",
  "nile_ribbon|Aerial view of the Nile river as a narrow bright green strip of farmland squeezed between two endless yellow deserts, a sharp edge where green meets sand",
  "river_country|Low aerial view along the Nile with villages, fields and towns packed tightly on both banks, empty desert cliffs right behind them")
b("[serious] Mais de noventa por cento dele é deserto. Quase todo egípcio vive numa faixa verde de poucos quilômetros, colada na água.",
  "desert_empty|Endless empty Sahara desert dunes under a harsh sun, one tiny lonely figure in the distance, heat shimmer",
  "green_edge|A farmer standing exactly on the line where a green crop field ends and bare desert sand begins, one foot on each side",
  "crowd_strip|Dense crowd of modern Egyptian people packed along a narrow riverbank strip with palm trees, the Nile on one side and desert on the other")
b("[curious] E o tempo, aqui, quebra a cabeça. [break] [amazed] Cleópatra viveu mais perto do iPhone do que dos homens que ergueram a Grande Pirâmide.",
  "cleo_window|Queen Cleopatra in royal Egyptian dress at a palace window, looking at a very old weathered pyramid far on the horizon",
  "timeline_rope|A long horizontal rope stretched across the desert like a timeline: a tiny pyramid at the far left end, a queen in Egyptian crown standing near the right end, a smartphone on a small pedestal at the very right end",
  "cleo_phone|Cleopatra in royal Egyptian dress looking puzzled at a modern smartphone in her hand")
b("[slightly dramatic] Mas a parte mais louca é outra. [long-break] Sumérios, hititas, assírios: todos sumiram. [break] O Egito continua aqui.",
  "sumer_ruins|Crumbling abandoned mud-brick ziggurat of Ur in the empty Mesopotamian desert",
  "hittite_ruins|Ruined stone Lion Gate of Hattusa on a barren Anatolian hill, abandoned",
  "felucca_today|Felucca sailboats on the Nile at sunset with palm trees and the Giza pyramids far on the horizon")
b("[curious] Então como um país invadido por persas, gregos, romanos, árabes, turcos e britânicos continuou sendo o Egito?",
  "invaders_line|A long line of foreign soldiers from different eras marching toward the pyramids: Persian, Greek hoplite, Roman legionary, Arab horseman, Ottoman janissary, British redcoat",
  "farmer_calm|An ancient Egyptian farmer calmly plowing his field by the Nile with an ox while foreign armies march past in the background")
b("Em menos de vinte minutos, sete mil anos. [break] E, no fim, o medo que o Egito carrega desde o primeiro faraó.",
  "seven_thousand|A long winding road of history along the Nile seen from above: prehistoric huts, then pyramids, temples, mosques with minarets and finally modern skyscrapers",
  "pharaoh_worried|An ancient pharaoh wearing the double crown standing on a riverbank, anxiously watching the low level of the Nile water",
  "modern_worried|A modern Egyptian official in a suit standing on the same riverbank in the same pose, anxiously watching the low Nile water")

# ───────────────────────── 1. ORIGENS ─────────────────────────
cap("1. O rio que fez um país")
b("[warm] Nossa história começa com um homem que morreu há mais de cinco mil anos e foi enterrado direto na areia quente.",
  "predynastic_family|A prehistoric Egyptian family in simple clothes standing at the edge of the desert above the Nile valley, five thousand years ago",
  "gebelein_burial|Prehistoric family laying a man's body curled in a fetal position into a shallow pit in hot desert sand, clay pots around, sad faces",
  "sand_mummy|A naturally dried prehistoric body lying curled in the sand of a grave, seen from above, no bandages", card="3300 a.C.")
b("A areia secou o corpo tão rápido que ele virou múmia sozinho. Hoje ele está no Museu Britânico.",
  "sun_sand_dry|Blazing sun over a desert grave, heat waves drying the sand, a curled shape under the sand surface",
  "museum_case|Museum visitors looking at an ancient curled-up natural mummy inside a glass display case in a London museum gallery")
b("[amazed] Em 2018, com luz infravermelha, cientistas acharam no braço dele [long-break] tatuagens: um touro selvagem e um carneiro. Das mais antigas do mundo.",
  "infrared_scan|Scientists in lab coats scanning the arm of an ancient mummy with an infrared camera, a monitor glowing",
  "tattoo_reveal|A scientist gasping in surprise at a monitor that shows dark animal-shaped marks on an ancient arm",
  "tattoo_bull|Close-up of faint dark ancient tattoos on a mummified upper arm showing a wild bull and a barbary sheep with curved horns")
b("[curious] Mas o que aquele povo fazia ali, na beira do Nilo? [break] É que o Saara nem sempre foi deserto.",
  "nile_camp|Prehistoric reed huts on the bank of the Nile with people fishing among papyrus",
  "sahara_question|A prehistoric man standing on a sand dune looking back at the empty desert behind him",
  "rock_art|Prehistoric rock paintings of cattle, giraffes and swimming people on a cave wall in the middle of the Sahara desert")
b("Há uns dez mil anos, ele era uma savana, com lagos, girafas e até hipopótamos. [break] Depois o clima mudou, e a chuva foi embora.",
  "green_sahara|Green Sahara savanna ten thousand years ago with blue lakes, giraffes, hippos and hunters with spears",
  "hippo_lake|Hippos in a blue lake surrounded by tall grass where the Sahara is today, a prehistoric hunter hiding in the reeds",
  "sahara_drying|Dry cracked lakebed with dying acacia trees and animal bones, prehistoric hunters looking worried at the cloudless sky")
b("[serious] Os grupos espalhados pelo Saara fizeram a única coisa possível: marcharam para a água.",
  "migration|A long column of prehistoric families with cattle and baskets walking across the desert toward a distant green river valley",
  "arrival_valley|Prehistoric people arriving at a cliff edge overlooking the lush green Nile valley, amazed")
b("[warm] E o Nilo tinha um truque. [break] Todo verão, sem falhar, ele transbordava.",
  "nile_flood|The Nile overflowing its banks in summer, brown water spreading over the fields, villages on small mounds like islands",
  "flood_villagers|Ancient Egyptian villagers on a flat rooftop happily watching the flood water cover their fields")
b("A água cobria os campos por semanas e, quando baixava, deixava uma lama preta e fértil. Era só jogar a semente e esperar.",
  "flood_receding|Brown flood water slowly withdrawing from the fields, leaving shiny black mud and white egrets",
  "black_mud|Ancient Egyptian farmers walking barefoot on rich black mud after the flood recedes, scattering seeds by hand",
  "wheat_harvest|Ancient Egyptian farmers harvesting tall golden wheat with sickles, the Nile behind them")
b("Os egípcios chamavam a própria terra de Kemet, a Terra Negra, por causa dessa lama. [break] E o deserto em volta era Deshret, a Terra Vermelha.",
  "kemet|An ancient Egyptian man kneeling and lifting a handful of black fertile soil, green crops all around",
  "kemet_aerial|Aerial view of the sharp border between black fertile Nile soil with green crops and the red desert",
  "deshret|Red-orange desert cliffs and dunes right next to a green field, an ancient Egyptian man pointing at the red desert")
b("Um rio que irriga sozinho e um deserto que serve de muralha. [break] [slightly dramatic] Ali, entre o preto e o vermelho, nasceram as primeiras aldeias e as primeiras brigas por poder.",
  "desert_wall|Bird's-eye view of the green Nile valley protected by vast deserts on both sides, tiny raiders lost and exhausted among the dunes",
  "first_village|Early Egyptian mud-brick village with granaries, pottery kilns and people working, the Nile behind",
  "granaries|Villagers storing grain in round mud granaries in an early Egyptian village",
  "chiefs_rivalry|Two prehistoric Egyptian chieftains holding stone maces, glaring at each other across a river")

# ───────────────────────── 2. UNIFICAÇÃO ─────────────────────────
cap("2. Dois reinos, uma coroa")
b("Por volta de 3200 antes de Cristo, havia dois Egitos: o Alto, no vale estreito do sul, e o Baixo, no delta do norte.",
  "map_two|Illustrated map of Egypt along the Nile from the delta to the first cataract, the narrow southern valley tinted in one color and the wide northern delta tinted in another, no labels",
  "delta_marsh|The Nile delta marshes with papyrus thickets, birds and small reed boats",
  "south_valley|The narrow southern Nile valley between tall limestone cliffs, small villages along the water")
b("[warm] E sim, o Alto Egito fica embaixo no mapa. O nome segue o rio, que corre de sul para norte.",
  "flow_north|Illustrated view of the Nile seen from above flowing upward on the page toward the sea, boats drifting with the current, big curved arrows showing the flow",
  "map_south_up|Illustrated map of the Nile drawn with south at the top: the narrow valley above and the delta fan below, a compass rose, no labels",
  "sail_south|Ancient Egyptian sailboat with a big square sail traveling south against the current, pushed by the north wind")
b("Cada reino tinha a sua coroa: uma branca e alta, no sul, e uma vermelha e achatada, no norte.",
  "white_crown|An ancient southern Egyptian king wearing the tall white bowling-pin shaped crown, standing in the narrow valley",
  "red_crown|An ancient northern Egyptian king wearing the flat red crown with a curled wire spiral, standing in the delta marshes",
  "two_kings|A southern king in a tall white crown and a northern king in a flat red crown facing each other across the river")
b("[slightly dramatic] Até que um rei do sul, Narmer, resolveu acabar com a disputa.",
  "narmer_march|King Narmer wearing the tall white crown, leading an army of spearmen northward along the Nile",
  "narmer_victory|King Narmer standing victorious over defeated northern warriors in the delta")
b("Numa placa de pedra famosa, a Paleta de Narmer, ele aparece de um lado com a coroa branca e, do outro, com a vermelha.",
  "narmer_palette|The Narmer Palette, a carved grey stone shield-shaped slab with reliefs, displayed alone in a museum case",
  "palette_relief|Ancient stone relief of an Egyptian king in the tall white crown holding an enemy by the hair and raising a mace",
  "narmer_red|Ancient stone relief of King Narmer wearing the flat red crown, walking in a procession behind standard bearers")
b("Por volta de 3100 antes de Cristo, os dois reinos viraram um só. [break] E o faraó passou a usar as duas coroas, encaixadas uma na outra.",
  "unification|Grand ceremony with people from the delta and the valley bowing together before a pharaoh on a throne by the Nile",
  "double_crown|Egyptian priests placing the combined red and white double crown on the head of a pharaoh", card="3100 a.C.")
b("[curious] Na mesma época surgiu a escrita. Etiquetas achadas numa tumba em Abidos estão entre os textos mais antigos do planeta.",
  "abydos_labels|Tiny carved bone labels with early picture signs lying on the floor of an excavated mud-brick tomb at Abydos",
  "early_scribe|An early Egyptian scribe sitting cross-legged painting hieroglyphs on a papyrus scroll")
b("[slightly dramatic] Com rei, coroa e escrita, o Egito estava pronto para algo que ninguém tinha feito antes: [break] construir montanhas.",
  "quarry|Egyptian workers cutting huge limestone blocks in a quarry with copper chisels and wooden mallets",
  "first_cataract_mountain|An Egyptian pharaoh looking up at a mountain and imagining a gigantic pyramid in its place, thought bubble with a pyramid")

# ───────────────────────── 3. PIRÂMIDES ─────────────────────────
cap("3. A era das pirâmides")
b("Por volta de 2650 antes de Cristo, o arquiteto Imhotep teve uma ideia: empilhar seis túmulos retangulares, um em cima do outro.",
  "imhotep_plan|The Egyptian architect Imhotep showing a plan drawn on papyrus to pharaoh Djoser",
  "mastaba_stack|Six rectangular stone tomb platforms stacked one on top of another, getting smaller, forming a step pyramid under construction", card="2650 a.C.")
b("Nasceu a Pirâmide de Degraus de Djoser, o primeiro grande monumento de pedra da história. [break] Séculos depois, Imhotep seria adorado como um deus.",
  "step_pyramid|The finished Step Pyramid of Djoser at Saqqara, gleaming white, inside a long walled courtyard",
  "imhotep_god|A seated statue of Imhotep holding a papyrus scroll, with people bringing offerings to it")
b("[warm] Depois veio Snefru, um obcecado: ergueu pelo menos três pirâmides, e numa delas os engenheiros tiveram que corrigir o ângulo no meio da obra.",
  "bent_pyramid|Pharaoh Sneferu looking at the Bent Pyramid of Dahshur, its slope angle visibly changing halfway up, workers scratching their heads")
b("O recorde ficou com o filho dele, Quéops: a Grande Pirâmide de Gizé, por volta de 2560 antes de Cristo. [break] [amazed] Uns dois milhões e trezentos mil blocos de pedra. Cento e quarenta e seis metros de altura.",
  "gp_construction|The Great Pyramid of Giza under construction with ramps and thousands of workers hauling limestone blocks on wooden sledges",
  "gp_white|The finished Great Pyramid of Giza covered in smooth polished white limestone casing, gleaming in the sun", card="2560 a.C.")
b("Por uns três mil e oitocentos anos, foi a construção mais alta feita pelo ser humano.",
  "gp_compare|The Great Pyramid towering over a much smaller medieval cathedral and a castle placed beside it for comparison")
b("[serious] Esqueça a cena de filme com escravos chicoteados. [break] Arqueólogos acharam a vila dos trabalhadores: padarias, cervejarias e até ossos quebrados que foram tratados.",
  "workers_village|Ancient Egyptian workers' village next to the Giza pyramids with bakeries, bread ovens, beer jars and cattle pens",
  "healed_arm|An ancient Egyptian healer setting a worker's broken arm with a wooden splint")
b("[warm] Eram equipes pagas em pão e cerveja, com apelidos como 'os Bêbados de Miquerinos'.",
  "work_gang|A cheerful team of Egyptian pyramid workers toasting with clay beer jars after a day of work")
b("[curious] Em 2013, num antigo porto do Mar Vermelho, apareceu o diário de um inspetor chamado Merer: os papiros escritos mais antigos já encontrados.",
  "wadi_jarf|Archaeologists carefully unrolling ancient papyrus fragments found in a cave at an ancient Red Sea harbor",
  "wadi_jarf")
b("Ele anotou, dia após dia, como levava blocos de calcário de barco até Gizé. É o caderno de obra da Grande Pirâmide.",
  "merer_boat|A wooden Nile boat loaded with white limestone blocks sailing toward the Giza plateau, crew rowing",
  "gp_construction")
b("Depois vieram as pirâmides de Quéfren e de Miquerinos, e a Esfinge, com corpo de leão e, provavelmente, o rosto de Quéfren.",
  "sphinx_carve|Workers carving the Great Sphinx out of the bedrock, the pyramid of Khafre behind it",
  "giza_three|Panoramic view of the three pyramids of Giza and the Great Sphinx in front, green fields and the Nile in the foreground")
b("Mas montanhas de pedra custam caro, e o poder do faraó foi minguando. [break] [slightly dramatic] Aí veio o golpe final.",
  "rich_nobles|Wealthy Egyptian nobles and priests counting gold and grain in a big storeroom while a pharaoh watches them, worried")
b("Por volta de 2200 antes de Cristo, uma seca de décadas atingiu boa parte do mundo. E o Nilo parou de subir.",
  "drought_nile|The Nile very low with cracked dry mud banks, dead crops and stranded boats", card="2200 a.C.")
b("Sem enchente, não tem colheita. Sem colheita, não tem faraó. Textos da época falam de fome e saques.",
  "famine|Hungry Egyptian villagers waiting in line at an almost empty granary while looters run off with sacks in the background")
b("O Antigo Império desmoronou. [break] [serious] E o Egito aprendeu a lição que ia se repetir por milênios: quem controla a água controla tudo.",
  "empty_throne|An empty abandoned pharaoh's throne in a dusty dark hall with sand blowing in",
  "pharaoh_worried")

# ───────────────────────── 4. MÉDIO E NOVO IMPÉRIO ─────────────────────────
cap("4. Os faraós guerreiros")
b("Depois de mais de um século de confusão, um rei de Tebas, Mentuhotep II, reunificou o país, por volta de 2050 antes de Cristo.",
  "mentuhotep|Pharaoh Mentuhotep II marching on foot at the head of Theban soldiers with shields and spears, holding a mace",
  card="2050 a.C.")
b("Começa o Médio Império, com canais, literatura e faraós que, nas estátuas, aparecem com cara de cansados.",
  "faiyum_canal|Egyptian workers digging a big irrigation canal in the Faiyum oasis",
  "senusret|Stone statue of pharaoh Senusret III with a tired careworn face, heavy eyelids and big ears")
b("[slightly dramatic] Só que, nessa época, chegaram estrangeiros do leste, os hicsos, trazendo algo que os egípcios nunca tinham visto: [long-break] cavalos puxando carros de guerra.",
  "hyksos_chariot|Foreign Hyksos warriors from the east charging on horse-drawn war chariots in the Nile delta, Egyptian foot soldiers shocked")
b("Eles dominaram o norte por cerca de um século, até que Ahmose, um príncipe de Tebas, copiou as armas do inimigo e os expulsou, por volta de 1550 antes de Cristo.",
  "ahmose|Egyptian prince Ahmose driving his own war chariot with a composite bow, leading Egyptian chariots",
  "hyksos_flee|Hyksos fleeing a fortified delta city as the Egyptian army storms the walls", card="1550 a.C.")
b("[serious] E o Egito aprendeu: para não ser invadido de novo, era preciso invadir primeiro. [break] Começa o Novo Império, a era de ouro dos faraós.",
  "nk_army|A massive New Kingdom Egyptian army with chariots and archers marching out of a city gate",
  "map_empire|Illustrated map of the eastern Mediterranean and the Nile showing the Egyptian empire at its height shaded from Nubia in the south to Syria in the north, no labels")
b("Uma das grandes governantes foi uma mulher, Hatshepsut, que se declarou faraó e, nas estátuas, aparece até com a barba postiça real.",
  "hatshepsut|Queen Hatshepsut as pharaoh on a throne wearing the striped royal headdress and the false royal beard",
  "hatshepsut")
b("Ela mandou uma expedição à misteriosa Terra de Punt, que voltou com árvores de incenso vivas para o templo dela.",
  "punt_ships|Egyptian ships returning from the land of Punt loaded with live incense trees in baskets, baboons and exotic goods",
  "deir_el_bahari|The terraced temple of Hatshepsut at Deir el-Bahari against tall cliffs, small incense trees planted in front")
b("Depois dela, Tutmés III fez umas dezessete campanhas militares e esticou o império do Sudão até a Síria.",
  "thutmose|Pharaoh Thutmose III leading a chariot charge at the battle of Megiddo",
  "map_empire")
b("[curious] Então veio o faraó mais estranho de todos: [break] Aquenáton.",
  "akhenaten|Pharaoh Akhenaten with an elongated face and long chin raising his hands toward the sun disk whose rays end in little hands")
b("Ele trocou os deuses antigos por um só, Aton, o disco do sol. Fechou templos e ergueu uma capital nova no meio do nada.",
  "temples_closed|Egyptian workers chiseling names of the old gods off temple walls while priests protest",
  "amarna|The new city of Amarna built quickly in the desert with open-air sun temples")
b("[serious] Quando ele morreu, tudo foi desfeito. [break] O nome dele foi apagado, e o provável filho dele trocou de nome, de Tutancáton para Tutancâmon.",
  "temples_closed",
  "tut_young|Young boy pharaoh Tutankhamun on a golden throne with his young wife")
b("Tutancâmon morreu com uns dezenove anos e foi um faraó menor. [break] Justamente por isso, a tumba dele foi esquecida e chegou quase intacta até nós.",
  "tut_hidden|A small tomb entrance hidden under sand and stone debris in the Valley of the Kings, tomb robbers walking past without noticing",
  "tut_hidden")
b("Ela só seria aberta em 1922, com mais de cinco mil objetos lá dentro. [break] [slightly dramatic] Guarde esse ano. Ele vai voltar.",
  "carter|Archaeologist Howard Carter peering with a candle through a hole into a tomb room filled with golden treasures",
  "tut_mask|The golden funerary mask of Tutankhamun glowing in the dark", card="1922")
b("[amazed] E então, o maior de todos: Ramsés II. Sessenta e seis anos no trono e, segundo os registros, mais de cem filhos.",
  "ramesses_family|Pharaoh Ramesses II on a throne surrounded by dozens of his children of all ages",
  "abu_simbel|The colossal rock temple of Abu Simbel with four giant seated statues of Ramesses II facing the Nile")
b("Em 1274 antes de Cristo, ele enfrentou os hititas em Kadesh, numa das maiores batalhas de carros de guerra da história. [break] Ninguém venceu.",
  "kadesh|Battle of Kadesh: thousands of Egyptian and Hittite chariots clashing near a river and a fortress", card="1274 a.C.")
b("Mas os dois lados assinaram um dos tratados de paz mais antigos que se conhecem. [break] Uma cópia dele está hoje na sede da ONU, em Nova York.",
  "treaty|Egyptian and Hittite envoys exchanging a silver tablet treaty in a palace hall",
  "un_replica|A replica of an ancient clay tablet displayed on a wall in a modern United Nations building hallway")
b("[serious] Algumas décadas depois, o mundo da Idade do Bronze desabou. Cidades queimaram, e os misteriosos Povos do Mar atacaram a costa.",
  "sea_peoples|Ships of the Sea Peoples with bird-head prows battling Egyptian ships near the Nile delta, coastal cities burning behind")
b("O Egito resistiu. [break] Mas logo depois os artesãos das tumbas reais cruzaram os braços: o pagamento em grãos estava atrasado.",
  "strike|Ancient Egyptian tomb workers sitting down with arms crossed in protest outside a temple, refusing to work")
b("É a primeira greve registrada da história. [break] E um sinal: o Egito estava enfraquecendo, e o mundo lá fora estava de olho.",
  "strike",
  "foreign_eyes|Foreign kings and generals from distant lands looking hungrily over a map of Egypt in a dark tent")

# ───────────────────────── 5. DOMINAÇÕES ─────────────────────────
cap("5. Todo mundo quer o Egito")
b("Nos séculos seguintes, o trono do faraó virou troféu. Vieram faraós de origem líbia e, depois, reis núbios, que desceram do sul e tomaram o país.",
  "libyan_pharaoh|A pharaoh of Libyan origin with a feather in his hair sitting on an Egyptian throne",
  "nubian_king|Kushite Nubian king Piye wearing a crown with two cobras, leading an army from the south into Egypt")
b("[amazed] Os núbios gostavam tanto do Egito antigo que, na terra deles, construíram mais pirâmides do que os próprios egípcios.",
  "meroe|Many small steep pyramids of Meroe in Sudan standing in the desert",
  "nubian_king")
b("[serious] Em 663 antes de Cristo, os assírios saquearam Tebas. [break] E em 525 antes de Cristo, chegaram os persas.",
  "assyrian_sack|Assyrian soldiers in pointed helmets sacking the temples of Thebes, smoke rising",
  "persian_army|The Persian army of king Cambyses marching into Egypt with spears and banners", card="525 a.C.")
b("[curious] Conta uma lenda, provavelmente exagerada, que os persas puseram gatos na frente das tropas, e os egípcios, que veneravam os gatos, não tiveram coragem de atacar.",
  "cats_battle|Persian soldiers holding cats in front of their shields while Egyptian soldiers hesitate",
  "cats_battle")
b("Lenda ou não, o Egito virou província persa. [break] Até que, em 332 antes de Cristo, chegou Alexandre, o Grande.",
  "persian_army",
  "alexander|Young Alexander the Great on horseback entering Egypt, Egyptians welcoming him with flowers", card="332 a.C.")
b("Os egípcios odiavam os persas e o receberam como libertador. [break] Um oráculo no deserto o chamou de filho de deus, e ele fundou uma cidade com o próprio nome: Alexandria.",
  "siwa|Alexander the Great at the desert oasis temple of Siwa receiving the oracle from a priest",
  "alexandria_found|Alexander marking the plan of a new city on the ground with grain, on the Mediterranean coast")
b("Quando ele morreu, o general Ptolomeu ficou com o Egito e fundou uma dinastia grega que durou quase três séculos.",
  "ptolemy|Greek general Ptolemy being crowned as an Egyptian pharaoh, wearing a mix of Greek and Egyptian clothes")
b("[amazed] Alexandria virou a capital do saber, com o Farol, uma das Sete Maravilhas, e a Biblioteca, que tentava juntar todos os livros conhecidos.",
  "lighthouse|The Lighthouse of Alexandria towering over a harbor full of ships",
  "library|Scholars reading scrolls in the vast Library of Alexandria with shelves full of papyrus rolls")
b("[curious] Os ptolomeus eram gregos e falavam grego. Segundo Plutarco, a primeira da família a aprender egípcio foi [long-break] Cleópatra.",
  "ptolemy",
  "cleo_study|Young Cleopatra studying Egyptian hieroglyphs with an Egyptian priest as tutor")
b("Cleópatra se aliou a Júlio César e depois a Marco Antônio para manter Roma longe. [break] [serious] Não deu certo.",
  "cleo_caesar|Cleopatra meeting Julius Caesar in her palace",
  "cleo_antony|Cleopatra and Mark Antony together on a golden ship")
b("Em 30 antes de Cristo, Otaviano venceu, Cleópatra morreu, e o Egito virou propriedade pessoal do imperador romano.",
  "octavian|Roman general Octavian entering Alexandria with legionaries",
  "cleo_end|Cleopatra lying still on a couch in her tomb, a small snake near a basket, servants mourning", card="30 a.C.")
b("Senadores romanos nem podiam entrar no Egito sem permissão. [break] [curious] O motivo? Trigo: o Egito virou o celeiro que alimentava Roma.",
  "senator_blocked|A Roman senator stopped at a harbor gate by soldiers, not allowed to land",
  "grain_ships|Roman grain ships loaded with sacks of Egyptian wheat sailing from Alexandria toward Rome")
b("[warm] Com Roma veio o cristianismo, e no deserto egípcio surgiram os primeiros monges cristãos.",
  "desert_monk|A Christian hermit monk living alone in a desert cave in Egypt")
b("[serious] E aí veio uma perda silenciosa. [break] Em 394 depois de Cristo, alguém gravou hieróglifos numa parede do templo de Filae.",
  "philae|The temple of Philae on an island in the Nile",
  "last_glyph|A lone priest carving a hieroglyphic inscription on a temple wall by lamplight", card="394 d.C.")
b("É a última inscrição em hieróglifos que se conhece. [break] Depois disso, por mais de mil e quatrocentos anos, ninguém no mundo conseguiu ler aquela escrita.",
  "glyphs_confused|Travelers from later centuries staring confused at walls covered in hieroglyphs, scratching their heads",
  "last_glyph")

# ───────────────────────── 6. ÁRABES, MAMELUCOS, OTOMANOS ─────────────────────────
cap("6. O Egito árabe")
b("Em 639, um exército árabe chegou pelo Sinai. O Egito passou a ter governo muçulmano e, aos poucos, foi ficando árabe na língua.",
  "amr|Arab Muslim army on horses and camels led by general Amr ibn al-As crossing the Sinai desert",
  "fustat|The new city of Fustat with its first mosque near the Nile, tents and mud-brick buildings", card="639")
b("[warm] A língua egípcia, herdeira da dos faraós, sobreviveu como copta, que hoje vive quase só nas missas da Igreja Copta.",
  "coptic_mass|A Coptic priest in ornate robes reading from a book during a candlelit mass")
b("Em 969, uma dinastia vinda do oeste, os fatímidas, fundou uma cidade nova ao lado da antiga. [break] O nome: al-Qahira, a Vitoriosa. Ou seja, o Cairo.",
  "cairo_founding|Fatimid builders constructing the walls and gates of the new city of Cairo", card="969")
b("Lá eles abriram Al-Azhar, uma mesquita que virou universidade e funciona até hoje, uma das mais antigas do mundo.",
  "al_azhar|The courtyard of the Al-Azhar mosque in Cairo with students sitting in circles around teachers")
b("[serious] Depois de Saladino, os sultões montaram um exército de soldados escravizados, comprados ainda meninos.",
  "mamluk_training|Young boys being trained as mamluk soldiers in archery and horse riding in a courtyard")
b("Eram os mamelucos. [break] Em 1250, eles mataram o próprio sultão e tomaram o Egito.",
  "mamluk_coup|Mamluk soldiers bursting into a sultan's tent with swords drawn", card="1250")
b("[slightly dramatic] Dez anos depois, os mongóis, que tinham arrasado Bagdá, vieram atrás do Egito. E em Ain Jalut, os mamelucos fizeram o impensável: [long-break] derrotaram os mongóis em campo aberto.",
  "ain_jalut|Mamluk cavalry charging Mongol horse archers in a valley at the battle of Ain Jalut")
b("O Cairo virou a maior cidade do mundo islâmico. [break] [serious] Até que a peste negra chegou e matou uma parte enorme da população.",
  "cairo_medieval|Bustling medieval Cairo with minarets, markets and camel caravans",
  "plague|Empty plague-stricken streets of medieval Cairo with mourners")
b("Em 1517, os turcos otomanos venceram os mamelucos e enforcaram o último sultão deles num portão do Cairo.",
  "ottomans|The Ottoman Turkish army with cannons and janissaries entering Cairo",
  "bab_zuwayla|The great medieval gate of Bab Zuwayla in Cairo with a silent crowd gathered in front", card="1517")
b("O Egito virou uma província distante de Istambul por quase três séculos. [break] [slightly dramatic] Até que, em 1798, chegou um general francês ambicioso demais.",
  "ottoman_province|An Ottoman governor in Cairo receiving tax payments while the Nile flows calmly behind",
  "french_fleet|A French fleet of sailing warships arriving at Alexandria")

# ───────────────────────── 7. EUROPEUS E SUEZ ─────────────────────────
cap("7. Os europeus e o canal")
b("Napoleão Bonaparte. [break] Ele venceu os mamelucos perto das pirâmides e trouxe junto mais de cento e cinquenta cientistas e artistas.",
  "battle_pyramids|French infantry squares fighting charging Mamluk cavalry with the pyramids in the background",
  "savants|French scientists and artists measuring and sketching the Great Sphinx", card="1798")
b("[curious] Em 1799, soldados franceses acharam, num forte em Roseta, uma pedra com o mesmo texto em três escritas: hieróglifos, demótico e grego.",
  "rosetta_found|French soldiers discovering a dark inscribed stone slab while rebuilding an old fort wall",
  "rosetta|The Rosetta Stone, a dark granite slab with three bands of ancient inscriptions")
b("Os britânicos expulsaram os franceses e levaram a pedra para Londres. [break] Mas foi um francês, Champollion, quem a decifrou, em 1822. [amazed] Depois de mais de mil e quatrocentos anos, os faraós voltaram a falar.",
  "champollion|Jean-Francois Champollion at his desk surrounded by papers, jumping up in excitement",
  "rosetta")
b("Com a saída dos franceses, um oficial albanês do exército otomano tomou o poder: Muhammad Ali. [break] [serious] Para não ter rivais, ele convidou os chefes mamelucos para uma festa na Cidadela e mandou matar quase todos.",
  "muhammad_ali|Muhammad Ali Pasha in Ottoman dress with a turban and white beard, looking determined",
  "citadel_trap|Mamluk horsemen trapped in a narrow passage of the Cairo Citadel as the gates close behind them")
b("Ele modernizou o país na marra e abriu a porta para um velho sonho europeu: ligar o Mediterrâneo ao Mar Vermelho.",
  "cotton_mill|A 19th-century Egyptian cotton mill with workers and machines",
  "map_suez|Illustrated map of Egypt showing the narrow strip of land between the Mediterranean and the Red Sea, no labels")
b("O Canal de Suez abriu em 1869, cavado por dezenas de milhares de egípcios, muitos forçados, e encurtou em milhares de quilômetros a viagem da Europa à Ásia.",
  "suez_dig|Thousands of Egyptian laborers digging the Suez Canal with shovels and baskets",
  "suez_open|The grand opening ceremony of the Suez Canal with ships, flags and fireworks", card="1869")
b("Só que as dívidas do governante Ismail afundaram o Egito, e em 1875 ele vendeu a parte egípcia do canal para a Grã-Bretanha.",
  "ismail|Khedive Ismail in a lavish palace surrounded by piles of bills and worried bankers",
  "ismail")
b("Sete anos depois, em 1882, os britânicos invadiram para proteger o canal e ficaram mais de setenta anos.",
  "british_invade|British warships bombarding Alexandria and redcoat troops landing on the beach",
  "british_cairo|British officers in pith helmets riding through Cairo streets while Egyptians watch", card="1882")
b("Em 1922, depois de grandes protestos, o Egito ganhou uma independência quase só no papel. [break] [warm] E lembra daquele ano? Foi o mesmo em que a tumba de Tutancâmon foi aberta.",
  "protests_1919|Egyptian crowds protesting in the streets of Cairo with flags, men and women together",
  "tut_mask")

# ───────────────────────── 8. EGITO MODERNO ─────────────────────────
cap("8. O Egito de hoje")
b("Em 1952, um grupo de jovens oficiais derrubou o rei. [break] O líder deles, Gamal Abdel Nasser, virou o herói do mundo árabe.",
  "nasser|Gamal Abdel Nasser giving a speech to a huge cheering crowd, young army officers in 1950s uniforms standing behind him", card="1952")
b("Em 1956, Nasser estatizou o Canal de Suez. [break] Grã-Bretanha, França e Israel atacaram, mas, pressionados por americanos e soviéticos, recuaram.",
  "suez_flag|Egyptian flags raised over the Suez Canal offices with celebrating workers",
  "suez_crisis|Warships and paratroopers over the Suez Canal zone", card="1956")
b("[slightly dramatic] E Nasser foi atrás do sonho mais antigo do Egito: controlar o Nilo, com a Represa Alta de Assuã, concluída em 1970.",
  "aswan_dam|The completed Aswan High Dam with the huge reservoir lake behind it", card="1970")
b("[amazed] Pela primeira vez em milhares de anos, a enchente parou. [break] E o lago da represa cresceu tanto que a UNESCO cortou o templo de Abu Simbel em blocos e o remontou mais no alto.",
  "aswan_dam",
  "abu_simbel_move|Engineers cutting the colossal Abu Simbel statues into huge blocks and lifting them with cranes")
b("Vieram as guerras com Israel, em 1967 e 1973, e em 1979 Anwar Sadat assinou a paz. [break] [serious] Dois anos depois, foi assassinado num desfile militar.",
  "war_1973|Egyptian soldiers crossing the Suez Canal in small boats",
  "sadat_peace|Anwar Sadat shaking hands at a peace signing ceremony")
b("Hosni Mubarak governou por quase trinta anos, até 2011, quando multidões encheram a Praça Tahrir. [break] Em dezoito dias, ele caiu.",
  "mubarak|Hosni Mubarak in a suit at a podium",
  "tahrir|A huge crowd filling Tahrir Square in Cairo with Egyptian flags", card="2011")
b("Depois vieram uma eleição, a deposição do presidente eleito e, em 2014, o general Abdel Fattah al-Sisi, que governa até hoje.",
  "sisi|An Egyptian president in a suit at a podium with Egyptian flags behind him")
b("[warm] Hoje o Egito tem mais de cem milhões de pessoas, uma capital nova no deserto e, desde 2025, o Grande Museu Egípcio, ao lado das pirâmides.",
  "new_capital|Modern skyscrapers of Egypt's new administrative capital rising in the desert",
  "gem|The huge modern Grand Egyptian Museum building near the Giza pyramids with crowds of visitors")
b("[curious] Mas lembra da promessa do começo? [break] [serious] O maior medo do Egito hoje não é um exército.",
  "modern_worried")
b("[slightly dramatic] É uma represa. [long-break] Na Etiópia, onde nasce o Nilo Azul, que manda a maior parte da água do Egito, foi inaugurada em 2025 a Grande Represa do Renascimento.",
  "gerd|A massive concrete dam on the Blue Nile in the green Ethiopian highlands, water flowing through its spillway",
  "map_nile|Illustrated map of the whole Nile basin from the Ethiopian highlands and Lake Victoria to the Mediterranean, rivers highlighted in blue, no labels", card="2025")
b("A maior hidrelétrica da África. [break] E o Egito, que depende quase só do Nilo, agora vê a torneira nas mãos de outro país.",
  "dry_canal|An Egyptian farmer looking worriedly at a low irrigation canal",
  "gerd")
b("[warm] Cinco mil anos atrás, o faraó olhava o rio e rezava pela enchente. [break] [serious] Hoje, o presidente olha o mesmo rio e negocia cada gota.",
  "pharaoh_worried", "modern_worried")
b("[curious] Então, como o Egito sobreviveu a todos? [break] Talvez porque os invasores mudavam, e o rio, não.",
  "invaders_line", "felucca_today")
b("Persas, gregos, romanos, árabes, turcos e britânicos passaram. [break] [warm] O Nilo ficou. E o Egito ficou junto.",
  "nile_space_night")
b("[warm] E pra você: qual foi a fase mais impressionante do Egito? Pirâmides, Cleópatra, mamelucos ou o Egito de hoje? Escreve aí nos comentários.",
  "eras_lineup|A lineup of figures from different Egyptian eras standing side by side by the Nile: a pyramid builder, a pharaoh, Cleopatra, a Mamluk warrior and a modern Egyptian",
  "giza_three")

# ───────────── Etapa 2: +25 imagens liberadas pelo manager (reuso depois dos 3 min → ~40%) ─────────────
# bloco → [(posição na lista de planos do bloco, "chave|prompt")]
EXTRA = {
 27: [(1, "bent_angle|Ancient Egyptian engineers on wooden scaffolding arguing and pointing at a huge pyramid whose slope suddenly changes to a gentler angle halfway up")],
 32: [(2, "merer_papyrus|Archaeologists in a desert cave near the Red Sea carefully unrolling a fragile ancient papyrus scroll covered in faint ink marks")],
 36: [(0, "drought_world|Wide ancient landscape of cracked dry fields and withered crops, ancient Egyptian farmers staring at an empty cloudless sky")],
 39: [(1, "theban_army|Ancient Theban soldiers with shields and spears marching north along the Nile behind a king in a war chariot")],
 41: [(1, "egyptians_horse|Astonished ancient Egyptian soldiers seeing a horse for the first time, one of them hiding behind his shield")],
 44: [(1, "hatshepsut_beard|Ancient Egyptian sculptors carving a statue of a female pharaoh wearing the royal false beard while the queen inspects it proudly")],
 49: [(1, "name_erased|Ancient Egyptian workers chiseling a pharaoh's carved name and sun disc off a temple wall, stone chips flying")],
 50: [(1, "tomb_buried|Desert sand and workmen's stone huts covering the hidden entrance of a small royal tomb in the Valley of the Kings, forgotten")],
 53: [(1, "kadesh_standoff|Two exhausted armies, Egyptian and Hittite, facing each other across a river after a battle, broken chariots between them")],
 57: [(1, "workers_sitting|Ancient Egyptian tomb workers sitting with arms crossed outside a temple wall, empty grain baskets in front of them, an official looking upset")],
 61: [(1, "egyptians_hesitate|Ancient Egyptian soldiers lowering their bows in hesitation, staring at cats walking in front of the enemy army")],
 75: [(1, "cairo_gate|Medieval Fatimid Cairo: a massive new stone city gate with crowds entering and minarets under construction, green banners")],
 79: [(1, "mongols_flee|Mamluk horsemen in armor chasing Mongol horse archers who flee across an open dusty plain")],
 85: [(2, "champollion_eureka|A young French scholar in 1820s clothes jumping up from a desk covered in papers and hieroglyph drawings, shouting with joy")],
 86: [(1, "mamluk_feast|Mamluk chiefs in rich robes and turbans riding through the gate of the Cairo Citadel to a celebration, unaware, soldiers watching from the walls")],
 89: [(1, "ismail_debt|An Egyptian ruler in a red fez at a desk buried under piles of debt papers, European bankers in top hats looming over him")],
 91: [(1, "independence_1922|Crowds of Egyptians in 1920s clothes and fezzes celebrating in a Cairo street waving green flags with a white crescent and three white stars (the 1920s Kingdom of Egypt flag, NOT the modern red-white-black flag), British officers still standing guard in the background")],
 92: [(1, "nasser_crowd|Gamal Abdel Nasser in a suit waving to a huge cheering crowd from a balcony in 1950s Cairo, the crowd waving green flags with a white crescent and three white stars (the 1950s Egyptian flag, NOT the modern red-white-black flag)")],
 94: [(1, "aswan_build|Thousands of workers and heavy machinery building a huge rock dam across the Nile in the 1960s")],
 95: [(1, "lake_nasser|A huge blue lake flooding a desert valley, the tops of ancient ruins disappearing under the rising water")],
 98: [(0, "election_line|Long queue of Egyptian voters outside a polling station in Cairo, people showing ink-stained fingers")],
100: [(1, "tanks_idle|Modern Egyptian army tanks parked in the desert with soldiers relaxing, an empty horizon with no enemy")],
103: [(2, "nile_negotiation|A modern Egyptian president at a negotiating table with other African leaders, a glass of water and a map of the Nile on the table")],
104: [(1, "conquerors_fade|Ghostly faded figures of conquerors from different eras walking away into the desert while the Nile keeps flowing in the foreground")],
105: [(1, "nile_eternal|The Nile flowing calmly at golden hour with ancient temple ruins on one bank and a modern city skyline on the other")],
}
_blocos = [blk for blk in B if "t" in blk]
for _n, _ins in EXTRA.items():
    for _pos, _s in _ins:
        _blocos[_n - 1]["s"].insert(_pos, _s)

# v2: blocos que abrem uma ideia nova (o build.py põe ~0,9 s antes deles; antes de capítulo já são ~1,5 s)
IDEIA = {3, 4, 5, 6, 10, 13, 15, 16, 20, 23, 24, 27, 28, 30, 32, 34, 35, 38, 41, 43, 44, 46, 47, 50, 52, 55,
         60, 62, 64, 66, 68, 70, 71, 75, 77, 79, 81, 82, 84, 86, 88, 90, 91, 94, 96, 97, 99, 100, 103, 104, 106}

THUMB = {"id": "thumb-base", "qualidade": "high",
         "prompt": "Wide panoramic landscape of ancient Egypt placed in the left 55% of the frame: the three pyramids of Giza, the Great Sphinx, the Nile with felucca boats, palm trees and a small city with temples; the right 45% of the frame is open bright blue sky and plain flat sand, completely empty to leave room for a title"}

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
        f"# A HISTÓRIA COMPLETA do Egito em {round(total / 60)} minutos: roteiro\n\n"
        f"Gerado por `roteiro.py` (fonte única; edite lá). {words} palavras, ~{fmt(total)} estimados a {WPS*60:.0f} ppm.\n"
        "Os blocos [Nxxx] são os mesmos de `blocos.json` (lá com as tags do Fish).\n" + "\n".join(script))
    linhas = ["# Storyboard: A HISTÓRIA COMPLETA do Egito",
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
