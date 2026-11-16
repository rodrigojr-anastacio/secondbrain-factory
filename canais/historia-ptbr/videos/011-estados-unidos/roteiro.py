#!/usr/bin/env python3
"""Fonte única do 011-estados-unidos (16/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

8º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
1º com ÂNGULO próprio (ANGULO.md, 16/11/2026): "a promessa cobrada". Forma modelada (History in Minutes/Genius), conteúdo nosso.
EMBALAGEM.md aprovada no crivo r3:
  A/T1 "Os EUA prometeram o que NÃO cumpriam. Como viraram potência?" + thumb rosto-emocao (Douglass fora da festa, "IGUAIS?")
  B/T2 "Como UMA FRASE construiu os Estados Unidos" + thumb objeto-simbolo (Sino da Liberdade rachado, "LIBERDADE")
  C/T3 "Como 13 colônias viraram potência? A resposta é uma PROMESSA" + thumb antes-depois (Independence Hall 1776 × 2026)
Hook: Douglass em Rochester, 5/7/1852 → PERGUNTA CENTRAL (≤ 0:50) → o sino rachado e mudo → "essa é a história inteira" → 1 "guarde"
  (a pergunta de Douglass, paga no fecho) → era 1.
Fio condutor: A FRASE DE 1776 COBRADA. Cada era = uma cobrança (cena) → o que ela mudou → o novo problema.
  Peça 1 (cap. 2): a frase era grande demais para quem a escreveu, mas estava escrita, para todos.
  Peça 2 (cap. 5): ninguém precisou inventar ideia nova; bastava ler a frase em voz alta (Seneca Falls).
  Peça 3 (cap. 10): virar potência deixou o país exposto; quem quer liderar o mundo livre precisa parecer livre.
  Lado "potência": cap. 7 (maior economia industrial, feita com imigrantes; Wong Kim Ark), cap. 9 (metade da produção mundial).
  Fecho: a frase construiu o país porque estava escrita e qualquer um podia cobrá-la (confirma o T2).
Seriedade: escravidão, remoção dos Cherokee, Guerra Civil e Segunda Guerra sem humor e sem imagem gráfica
  (sem correntes/chicote em close, sem ferida, sem corpo; objetos, silhuetas, campo vazio). Nada de capuz da Klan nem símbolo extremista.
  Fecho no presente com 1 frase neutra (250 anos), sem política atual.

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1776") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006–010).
Imagens: Codex (canal.yaml visual.gerador: codex; fallback nano-banana). Prompts só de conteúdo; o estilo vem do canal.yaml.
  O Codex põe marcos fora de época (anti-padroes §3d): cada cena de época diz o que NÃO pode aparecer.
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (006–010: ~128 ppm com pausas)
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
TITULO = "A história INTEIRA dos Estados Unidos"
PERGUNTA = "Como um país fundado numa frase que ele mesmo não cumpria virou a maior potência do mundo?"
PROMESSA = ("Como um país fundado numa frase que ele mesmo não cumpria (\"todos os homens são criados iguais\") virou a maior "
            "potência do mundo: cada vez que alguém foi cobrar essa frase, o país teve de deixar mais gente entrar, e cresceu com isso "
            "(EMBALAGEM.md r3).")
TITULOS = ('T1 "Os EUA prometeram o que NÃO cumpriam. Como viraram potência?" / T2 "Como UMA FRASE construiu os Estados Unidos" / '
           'T3 "Como 13 colônias viraram potência? A resposta é uma PROMESSA"')

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None):
    ideia = t.startswith("§")
    B.append({"t": t.lstrip("§ ").strip(), "s": list(s), "card": card, "ideia": ideia})

# ───────── regras de prompt (Codex/nano-banana) ─────────
MAPA = ("painted like a blank parchment terrain map seen from directly above, only coastlines, seas, rivers, mountains and flat colored areas, "
        "completely blank with no writing anywhere, no letters, no words, no labels, no symbols, no compass, no border, no frame")
SEMTXT = ", no readable writing, no letters anywhere, no signs, no boards"
SEMBAND = ", no flags, no banners, no stars and stripes"
COLONIAL = ", 18th century colonial America: brick and wooden buildings, dirt streets, horse carts, no skyscrapers, no cars, no Statue of Liberty, no modern objects"
SEC17 = ", early 17th century Virginia: small wooden houses with thatched roofs, a wooden palisade, forest, no brick towns, no modern objects"
SEC19 = ", 19th century America: no cars, no skyscrapers, no electric lights, no modern objects"
GUERRA = ", no blood, no wounds, no bodies, no violence shown"
ESCRAV = ", dignified and serious, no chains in close-up, no whips, no wounds, no blood, no suffering faces in close-up"
SEMSIMB = (", absolutely no symbols of any kind, no flags, no insignia, no emblems, no armbands, no hoods, "
           "no letters, no blood, no injuries, no violence shown")
# Personagens (regra da bíblia: nada de rosto descrito; "round-white-head cartoon …")
DOUGLASS = ("a round-white-head cartoon Frederick Douglass in 1852: a tall orator with a big voluminous dark wavy hair shape and a short dark beard shape, "
            "dark 19th century suit, vest and white collar")
PLATEIA52 = "round-white-head cartoon American audience of 1852, men in dark frock coats and top hats, women in long dresses and bonnets, seated in a wooden hall"
COLONOS17 = "round-white-head cartoon English colonists of 1619 with simple flat beard shapes, doublets, ruffled collars and tall hats"
AFRICANOS = "round-white-head cartoon African men and women of 1619 in simple cloth garments"
JEFFERSON = "a round-white-head cartoon young Thomas Jefferson of 1776 with a reddish tied-back hair shape, a brown coat and a white cravat"
DELEGADOS = "round-white-head cartoon American delegates of 1776-1787 in tricorn hats, knee breeches, long coats and white wigs or tied hair"
NOVAIORQUE = "round-white-head cartoon New York colonists and soldiers of 1776 in plain coats and tricorn hats"
CHEROKEE = ("round-white-head cartoon Cherokee people of 1828: men in long hunting shirts, sashes and wrapped cloth turbans, "
            "women in long cotton dresses and shawls")
SEQUOYAH = "a round-white-head cartoon Sequoyah, Cherokee scholar of 1821, with a cloth turban, a long pipe and a hunting shirt, writing symbols on a slate"
JACKSON = "a round-white-head cartoon President Andrew Jackson of 1832 with a tall stiff white hair shape, a dark coat and a high collar"
SOLDADOS30 = "round-white-head cartoon US Army soldiers of 1838 in plain dark blue uniforms and tall caps"
STANTON = "a round-white-head cartoon Elizabeth Cady Stanton of 1848, a woman with dark curls under a white cap, a dark dress with a white collar"
SENECA = "round-white-head cartoon men and women of 1848 in a small brick chapel, women in long dresses and bonnets, men in dark frock coats"
LINCOLN = "a round-white-head cartoon Abraham Lincoln with a simple flat chin beard shape without mustache, a tall black stovepipe hat and a long black frock coat"
SOLD_UNIAO = "round-white-head cartoon Union soldiers of 1863 in dark blue uniforms and kepi caps"
SOLD_CONF = "round-white-head cartoon Confederate soldiers of 1863 in grey uniforms and kepi caps"
LIBERTOS = "round-white-head cartoon formerly enslaved African American families of 1865 in simple work clothes, smiling with hope"
SUFRAG76 = "round-white-head cartoon American women suffragists of 1876 in long dark Victorian dresses with bustles and small hats"
ANTHONY = "a round-white-head cartoon Susan B. Anthony of 1876 with a dark hair bun shape, small round glasses, a dark dress and a red shawl"
OPERARIOS = "round-white-head cartoon immigrant factory workers of the 1890s in caps, vests and rolled sleeves"
IMIGRANTES = "round-white-head cartoon European immigrant families of 1900 with suitcases, bundles, shawls and caps"
CHINESES = "round-white-head cartoon Chinese immigrant workers of 1880 in plain blue jackets, a long black braided queue hairstyle and round hats"
WONG = "a round-white-head cartoon Wong Kim Ark, a young Chinese American cook of 1895, in a plain dark Western suit and a bowler hat, holding papers"
WILSON = "a round-white-head cartoon President Woodrow Wilson of 1917 with small round glasses, a long face shape and a dark suit"
SENTINELAS = "round-white-head cartoon American suffragists of 1917 in long coats and wide hats holding plain purple, white and gold sashes"
BURN = "a round-white-head cartoon young Harry Burn, 24-year-old Tennessee legislator of 1920, with slicked dark hair, a light suit and a red rose on the lapel"
RANDOLPH = "a round-white-head cartoon A. Philip Randolph of 1941, a tall dignified union leader with a thin mustache shape, in a three-piece suit"
FDR = "a round-white-head cartoon President Franklin D. Roosevelt of 1941 with small round glasses and a cigarette holder, in a grey suit"
OPERARIAS = "round-white-head cartoon American women factory workers of 1942 in blue work overalls and red bandanas"
SOLD42 = "round-white-head cartoon African American soldiers of 1942 in plain olive uniforms and garrison caps"
HO = "a round-white-head cartoon Ho Chi Minh of 1945 with a thin wispy goatee shape and a simple khaki tunic, speaking at a microphone"
KING = "a round-white-head cartoon Martin Luther King Jr. of 1963 with a short mustache shape and a dark suit and tie, speaking at a podium with microphones"
MARCHA = "round-white-head cartoon crowd of 1963, Black and white Americans in suits, dresses and hats, holding plain blank signs"
GUIA = "a cheerful little cartoon narrator character with a round white head and dot eyes"

# ───────────────────────── HOOK (Rochester, 5/7/1852) ─────────────────────────
cap("Hook")
b("[serious] Rochester, Nova York, cinco de julho de mil oitocentos e cinquenta e dois. Imagine você numa plateia ainda com cheiro dos fogos da véspera.",
  f"rochester_hall|The inside of a crowded 19th century wooden lecture hall in Rochester, New York, in 1852, {PLATEIA52}, gas lamps not lit, daylight through tall windows" + SEC19 + SEMBAND + SEMTXT,
  "fireworks_eve|A small 1852 American town street at night after a celebration, the last fireworks fading in the sky, red white and blue cloth bunting without stars on wooden houses" + SEC19 + SEMTXT,
  f"audience_close|Close view of {PLATEIA52}, waiting and whispering, looking toward a stage" + SEC19,
  "empty_stage|An empty wooden lecture stage with a simple lectern and a glass of water, 1852, seen from the audience" + SEC19 + SEMTXT,
  card="1852")
b("Sobe ao palco um homem que nasceu escravizado e fugiu aos vinte anos: Frederick Douglass. Pediram que ele falasse do Quatro de Julho. Ele escolheu o dia cinco.",
  f"douglass_stage|{DOUGLASS}, walking onto the wooden stage of the hall, serious and calm, audience in the foreground" + SEC19 + SEMTXT + "@@FREDERICK DOUGLASS",
  f"douglass_young_run|Symbolic memory scene: a young round-white-head cartoon Black man of 1838 in a sailor's shirt and cap walking fast along a harbor at dawn, looking back over his shoulder, ships behind" + SEC19,
  "douglass_letter|Close view of a 19th century invitation letter with a wax seal in a hand, only illegible flowing marks" + SEMTXT,
  "calendar_4_5|Symbolic comic scene: a 19th century wall calendar with two pages, the first page torn away and falling, only abstract shapes instead of numbers" + SEMTXT,
  f"douglass_profile|{DOUGLASS}, seen in profile at the lectern, arranging his papers, determined" + SEC19 + SEMTXT)
b("E pergunta: o que é, para o escravo, o seu Quatro de Julho? [break] Este Quatro de Julho é de vocês. Não meu.",
  f"douglass_point|{DOUGLASS} at the lectern pointing at the audience, indignant and powerful" + SEC19 + SEMTXT,
  f"audience_shock|{PLATEIA52}, some uncomfortable, some nodding, looking up at the speaker" + SEC19,
  "audience_whisper|Two round-white-head cartoon women of 1852 in bonnets whispering to each other in a wooden hall, surprised" + SEC19,
  "douglass_window|Symbolic scene: a dark street at night, a tall man in a dark suit with voluminous hair standing outside, seen from behind, looking through a bright window at a party of round-white-head cartoon people in top hats raising glasses under red white and blue bunting" + SEC19 + SEMBAND + SEMTXT)
b("Setenta e seis anos antes, esse país tinha escrito que todos os homens são criados iguais. Então, como um país fundado numa frase que ele mesmo não cumpria virou a maior potência do mundo?",
  "parchment_glow|Close view of an old 18th century parchment document with lines of illegible faded handwriting, one line glowing softly with golden light, candlelight" + SEMTXT,
  "map_13_colonies|Map of the east coast of North America in 1776 with a thin strip of thirteen colonies along the Atlantic painted in warm ochre and the rest of the continent uncolored, " + MAPA,
  "map_usa_today|Map of North America where the whole territory of the modern United States from the Atlantic to the Pacific is painted in warm ochre, " + MAPA,
  "power_symbols|Symbolic scene: a huge modern aircraft carrier, a city of glass skyscrapers and a cargo port full of containers under a bright blue sky, seen from far away" + SEMBAND + SEMTXT,
  "ocean_crossing|Symbolic scene: a tiny wooden sailing ship of 1776 and a huge modern cargo ship crossing the same blue ocean side by side, comic" + SEMBAND + SEMTXT,
  f"guide_question|{GUIA} standing between a small colonial brick building and a giant modern skyscraper, scratching his head, comic" + SEMTXT)
b("Até o Sino da Liberdade, em Filadélfia, já está rachado e mudo. Só que a frase continua escrita. E o que está escrito pode ser cobrado.",
  "bell_crack|The Liberty Bell alone hanging from a dark wooden yoke in a dim room, a long vertical crack in the bronze, plain smooth bronze with no letters, dramatic light" + SEMTXT,
  "bell_mute|The old bell tower of Philadelphia in 1852 at sunset with the bell hanging still, a pigeon sitting on the beam, silent" + SEC19 + SEMTXT,
  "bell_crack_close|Close view of the long dark crack in the bronze of an old bell, light grazing the metal, no letters",
  "parchment_finger|Close view of a round-white-head cartoon hand pointing at one line of an old parchment document with illegible handwriting, candlelight" + SEMTXT,
  f"line_people|A long line of round-white-head cartoon Americans from different centuries (a colonial woman, a freed man of 1865, a Chinese worker of 1880, a suffragist of 1917, a marcher of 1963) standing in a queue in front of an old brick building, each holding a rolled paper" + SEMBAND + SEMTXT)
b("Essa é a história inteira dos Estados Unidos. [break] Guarde a pergunta de Douglass: ela volta. E tudo começa num verão em que duas coisas chegam juntas.",
  "hall_1776|Independence Hall in Philadelphia in 1776, a red brick building with a white bell tower, dirt street with a horse cart and a few round-white-head cartoon colonists in tricorn hats, warm light" + COLONIAL + SEMBAND + SEMTXT,
  f"douglass_echo|{DOUGLASS}, seen from below at the lectern, finishing his sentence, dramatic light from a tall window" + SEC19 + SEMTXT,
  f"guide_summer|{GUIA} wiping sweat from his forehead under a hot summer sun on a riverbank in a forest, comic" + SEMTXT,
  "ship_arrival_hook|A small 17th century sailing ship arriving at a forested river bank at sunrise, seen from far away" + SEC17 + SEMBAND,
  "jamestown_river|A wide calm river in Virginia in 1619 at dawn, dense green forest on both banks, a small wooden ship with square sails anchored" + SEC17 + SEMBAND)

# ───────────────────────── 1. O VERÃO DE 1619 ─────────────────────────
cap("1. O verão de 1619")
b("§ Jamestown, Virgínia, julho de mil seiscentos e dezenove. Numa igrejinha de madeira, vinte e dois homens eleitos pelos colonos se sentam para fazer leis.",
  "jamestown_fort|The small triangular wooden fort of Jamestown, Virginia, in 1619, a palisade of logs, a few thatched houses and a small wooden church inside, river behind" + SEC17 + SEMBAND,
  f"church_assembly|Inside a small wooden church in Jamestown in 1619, {COLONOS17} sitting on benches in a circle, debating, one standing and talking, hot summer light" + SEC17 + SEMTXT,
  f"assembly_vote|{COLONOS17} raising their hands to vote inside a simple wooden church, a clerk writing on a large book" + SEC17 + SEMTXT,
  f"colonist_sweat|{COLONOS17} fanning themselves with their hats in the heat of the small church, comic" + SEC17,
  card="1619")
b("É a primeira assembleia eleita da América inglesa. Repare na data. Semanas depois, um navio chamado White Lion ancora ali perto e troca comida por vinte e poucos africanos escravizados.",
  "assembly_book|Close view of a large old handwritten record book open on a wooden table with a quill and an inkwell, illegible script, candlelight" + SEMTXT,
  "white_lion|A small 17th century English warship with square sails anchored at a river mouth in Virginia at sunset, a rowboat going to shore" + SEC17 + SEMBAND,
  f"point_comfort|{AFRICANOS} standing on a beach at Point Comfort, Virginia, in 1619, seen from a distance, English colonists and barrels of food on the sand, solemn atmosphere" + SEC17 + ESCRAV,
  "rolfe_letter|Close view of a 17th century handwritten letter on rough paper with a quill and ink, illegible script, candlelight" + SEMTXT,
  f"barrels_trade|Close view of barrels and sacks of food being exchanged on a beach, the legs of English colonists and the hem of simple cloth garments, solemn" + SEC17 + ESCRAV)
b("Mesmo verão, mesma colônia. O voto e a escravidão desembarcam juntos, e vão crescer juntos. [break] Se você perguntasse, ninguém ali chamaria isso de contradição.",
  "split_1619|Symbolic split scene: on the left a small wooden church with colonists voting, on the right a tobacco field with African workers, the same river behind both, serious" + SEC17 + ESCRAV + SEMTXT,
  "tobacco_field|A wide tobacco plantation in colonial Virginia with large green leaves, wooden drying barns and African workers in the distance, hazy summer light" + SEC17 + ESCRAV,
  "river_ships|Several small wooden ships on a Virginia river in the 1600s loading barrels of tobacco, forest behind" + SEC17 + SEMBAND,
  f"colonists_shrug|{COLONOS17} shrugging and looking away with indifferent faces, comic but serious" + SEC17)
b("§ Cento e cinquenta anos depois, já são treze colônias, ricas de tabaco, arroz e trabalho forçado. E acostumadas a votar as próprias leis.",
  "map_1765|Map of the east coast of North America in 1765 with thirteen small colonies painted in different soft colors along the Atlantic and French territory in pale blue to the west, " + MAPA,
  "colonial_port|A busy colonial American port of 1765 with brick warehouses, sailing ships and round-white-head cartoon merchants rolling barrels" + COLONIAL + SEMBAND + SEMTXT,
  "rice_carolina|A rice plantation in colonial South Carolina with flooded fields and African workers in the distance, a big white house far away" + COLONIAL + ESCRAV,
  f"town_meeting|A colonial New England town meeting in a white wooden meeting house in 1765, {DELEGADOS} arguing and raising hands" + COLONIAL + SEMTXT)
b("Só que a Grã-Bretanha sai endividada de uma guerra contra a França e manda a conta para a América: impostos. O problema é que os colonos não tinham voto em Londres.",
  "king_debt|A round-white-head cartoon King George III of 1765 with a white wig shape and a red royal robe, sitting on a throne and looking at a very long paper bill unrolling to the floor, worried, comic" + SEMTXT,
  "parliament_far|The British Parliament hall of 1765 full of round-white-head cartoon lords in wigs, seen from far away, no Americans inside" + SEMBAND + SEMTXT,
  "redcoats_ship|British redcoat soldiers of 1765 disembarking from a ship in a colonial harbor, round-white-head cartoon style, seen from far away" + COLONIAL + SEMBAND + SEMTXT,
  "tax_papers|Close view of a pile of colonial papers and a stack of coins on a wooden table with a hand stamping them, no readable letters" + SEMTXT,
  f"angry_colonists|{NOVAIORQUE} angrily waving papers in a colonial street, shouting" + COLONIAL + SEMBAND + SEMTXT)

# ───────────────────────── 2. UMA FRASE GRANDE DEMAIS ─────────────────────────
cap("2. Uma frase grande demais")
b("§ Filadélfia, junho de mil setecentos e setenta e seis. Num quarto alugado, um advogado da Virgínia de trinta e três anos escreve à luz de vela.",
  f"jefferson_room|{JEFFERSON}, writing at a small wooden desk with a quill by candlelight in a rented room in Philadelphia in 1776, papers everywhere, night" + COLONIAL + SEMTXT,
  "philadelphia_1776|A street in Philadelphia in June 1776 with red brick houses, cobblestones and round-white-head cartoon people in tricorn hats, summer evening" + COLONIAL + SEMBAND + SEMTXT,
  "quill_close|Close view of a feather quill writing on parchment by candlelight, only illegible flowing marks" + SEMTXT,
  f"jefferson_think|{JEFFERSON}, looking out of a window at night, thinking, holding the quill" + COLONIAL,
  card="1776")
b("Thomas Jefferson tem pouco tempo para explicar ao mundo por que treze colônias vão se separar do rei. E ele escreve: todos os homens são criados iguais.",
  f"jefferson_crumple|{JEFFERSON}, surrounded by crumpled paper balls on the floor, tired, comic" + COLONIAL + SEMTXT,
  "declaration_draft|Close view of a parchment with a freshly written first line in dark ink and the rest blank, a quill resting on it, candlelight" + SEMTXT,
  "declaration_light|Symbolic scene: an old parchment on a desk shining with golden light that spreads out of the open window over a colonial city at night" + COLONIAL + SEMTXT,
  f"jefferson_proud|{JEFFERSON}, holding up a sheet of parchment, satisfied" + COLONIAL + SEMTXT)
b("Repare: ele não escreveu todos os ingleses, nem todos os proprietários. Escreveu todos. Só que o próprio Jefferson escravizou mais de seiscentas pessoas ao longo da vida.",
  f"guide_all|{GUIA} pointing at a giant parchment with one glowing line, raising an eyebrow, comic" + SEMTXT,
  "monticello|The hilltop plantation house of Monticello in Virginia with its small dome, gardens and, far below, simple wooden cabins of enslaved workers, hazy light" + COLONIAL + ESCRAV,
  "cabins_row|A row of simple wooden cabins of enslaved people on a Virginia plantation at dusk, smoke from a chimney, a few people sitting outside, dignified" + COLONIAL + ESCRAV,
  f"jefferson_shadow|{JEFFERSON}, seen from behind at a window looking down at plantation fields, his long shadow on the floor, serious" + COLONIAL)
b("No rascunho, ele culpava o rei pelo tráfico de escravizados. O Congresso cortou o parágrafo inteiro. Mas, em quatro de julho, o resto é aprovado.",
  "draft_cut|Close view of a handwritten 18th century draft on parchment with one whole paragraph crossed out with thick ink lines, illegible script" + SEMTXT,
  f"congress_vote|Inside the Assembly Room of the Pennsylvania State House in 1776: {DELEGADOS} sitting at tables with green cloth, voting with raised hands, tall windows" + COLONIAL + SEMBAND + SEMTXT,
  f"delegates_shake|{DELEGADOS} shaking hands and signing a large parchment one after another, solemn" + COLONIAL + SEMTXT,
  "hall_1776#médio-esq")
b("§ Meses antes, Abigail Adams tinha escrito ao marido, John, que estava no Congresso: lembre-se das senhoras. John respondeu que não podia deixar de rir. [break] Spoiler: elas lembraram dele.",
  "abigail_write|A round-white-head cartoon Abigail Adams of 1776 in a white cap and a long dress writing a letter at a farmhouse table in Massachusetts with a quill, determined" + COLONIAL + SEMTXT,
  f"john_laugh|A round-white-head cartoon John Adams of 1776, bald on top, in a dark coat, reading a letter in Philadelphia and laughing, comic" + COLONIAL + SEMTXT,
  f"abigail_look|A round-white-head cartoon Abigail Adams of 1776 in a white cap, looking straight at the viewer with raised eyebrows, unimpressed, comic" + COLONIAL,
  f"letter_ship|A sealed 18th century letter traveling on horseback along a dirt road between farms, comic" + COLONIAL + SEMTXT)
b("Cinco dias depois, em Nova York, a Declaração é lida em voz alta. A multidão derruba a estátua de chumbo do rei George. E o chumbo vira balas, mais de quarenta mil.",
  f"ny_reading|{NOVAIORQUE} gathered on a green in New York in July 1776 listening to an officer reading a parchment aloud" + COLONIAL + SEMBAND + SEMTXT,
  f"statue_fall|{NOVAIORQUE} pulling ropes to topple a golden equestrian statue of a king on a stone pedestal in a small fenced park, cheering" + COLONIAL + SEMBAND + SEMTXT,
  "statue_pieces|The broken pieces of a golden lead statue of a king on horseback lying on the grass of a small park, a horse's head on the ground, comic" + COLONIAL + SEMTXT,
  "musket_balls|Close view of hundreds of small grey lead musket balls poured into a wooden box, a mold beside them" + SEMTXT)
b("A guerra dura até mil setecentos e oitenta e um. E aqui está a primeira peça da resposta: a frase era grande demais para quem a escreveu. Mas estava escrita, para todos.",
  f"war_march|Round-white-head cartoon American Continental soldiers of 1781 in blue coats marching along a dirt road with French soldiers in white coats, seen from far away" + COLONIAL + SEMBAND + GUERRA,
  "yorktown_field|An empty field at Yorktown in 1781 after the battle, cannons silent, smoke clearing, earthworks, autumn light" + COLONIAL + SEMBAND + GUERRA,
  "parchment_glow#médio-dir",
  f"guide_piece|{GUIA} placing a first big puzzle piece shaped like a parchment onto an empty puzzle board, comic" + SEMTXT)
b("O problema: agora era preciso fazer um país com ela. E fazer um país é fazer contas.",
  "puzzle_board|A big empty wooden puzzle board with only one piece placed in the corner, warm light" + SEMTXT,
  f"guide_tired|{GUIA} sitting on a pile of papers, holding his head, comic" + SEMTXT,
  "abacus_coins|Close view of colonial coins, an abacus and a ledger on a wooden table" + SEMTXT,
  "hall_1787_road|Round-white-head cartoon delegates of 1787 arriving by carriage at a red brick building with a white bell tower in Philadelphia" + COLONIAL + SEMBAND + SEMTXT)

# ───────────────────────── 3. AS CONTAS DA CONSTITUIÇÃO ─────────────────────────
cap("3. As contas da Constituição")
b("§ Mil setecentos e oitenta e sete, de novo em Filadélfia, no mesmo prédio de tijolos. Imagine você ali: portas fechadas, janelas fechadas, um calor de rachar. E uma pergunta prática: quem conta como gente?",
  f"convention_hot|Inside the Assembly Room of Independence Hall in summer 1787, windows shut, {DELEGADOS} sweating, fanning themselves, papers on tables with green cloth" + COLONIAL + SEMBAND + SEMTXT,
  "closed_windows|The red brick facade of Independence Hall in summer 1787 with all windows shut and curtains drawn, a guard at the door" + COLONIAL + SEMBAND + SEMTXT,
  f"washington_chair|A round-white-head cartoon George Washington of 1787 with a white tied hair shape, in a dark coat, sitting in a high-backed chair at the front of the room, presiding, serious" + COLONIAL + SEMTXT,
  f"fly_delegate|{DELEGADOS}: one delegate swatting a fly with a folded paper, the others sweating, comic" + COLONIAL + SEMTXT,
  card="1787")
b("Os estados do Sul querem contar os escravizados, para ter mais deputados. Mas sem dar a eles voto nenhum. A saída é uma conta: cada pessoa escravizada vale três quintos de uma pessoa.",
  f"south_delegates|{DELEGADOS} from the southern states standing and arguing, pointing at a chart of abstract figures" + COLONIAL + SEMTXT,
  "fraction_symbol|Symbolic scene: a balance scale on a desk, on one side five small identical wooden human figures and on the other side only three, serious" + SEMTXT,
  "chairs_count|Symbolic scene: rows of empty chairs in an assembly hall, more chairs being added on one side, serious" + COLONIAL + SEMTXT,
  "census_book|Close view of a 1790 census ledger with columns of tally marks and a quill, illegible script" + SEMTXT)
b("Tente explicar essa matemática para uma criança. A Constituição ainda dá vinte anos de prazo para o tráfico de escravizados. A frase dizia todos; as contas diziam três quintos.",
  f"guide_child|{GUIA} trying to explain a fraction written as abstract shapes on a small blackboard to a confused round-white-head cartoon child, comic" + SEMTXT,
  "slave_ship_far|A sailing ship of the 1790s on the open Atlantic seen from very far away under a grey sky, ominous, no people visible" + SEMBAND,
  "parchment_vs_ledger|Symbolic scene: a glowing old parchment and a dark accounting ledger side by side on a desk, the ledger casting a shadow over the parchment" + SEMTXT,
  f"signing_1787|{DELEGADOS} signing a large parchment one by one at a table, solemn" + COLONIAL + SEMTXT)
b("§ E o país cresce rápido. Em mil oitocentos e três, Jefferson, agora presidente, compra da França um território que dobra o tamanho do país.",
  "map_louisiana|Map of North America in 1803 with the young United States in ochre along the east and a huge territory west of the Mississippi river highlighted in gold, " + MAPA,
  f"jefferson_president|A round-white-head cartoon Thomas Jefferson of 1803, older, with grey-red hair shape, in a plain coat, holding a rolled map, pleased" + SEC19 + SEMTXT,
  "wagons_west|Covered wagons crossing a wide prairie toward distant mountains at sunset, round-white-head cartoon pioneer families walking beside them" + SEC19 + SEMBAND,
  "map_usa_today#médio-esq")
b("Mas cada pedaço de terra novo traz a mesma pergunta: de quem é essa terra? E quem já vive nela?",
  "forest_village|A Cherokee town of the 1820s in the green hills of Georgia with log cabins, farms, orchards and a council house, peaceful morning" + SEC19 + SEMBAND,
  "surveyors|Round-white-head cartoon American land surveyors of the 1820s with a tripod and chains measuring land at the edge of a forest, Cherokee farmers watching from their field" + SEC19,
  "map_georgia|Map of the southeastern United States in 1828 with the hills of northern Georgia highlighted in green, " + MAPA)

# ───────────────────────── 4. OS CHEROKEE FORAM AO TRIBUNAL ─────────────────────────
cap("4. Os Cherokee foram ao tribunal")
b("§ Geórgia, mil oitocentos e vinte e oito. Numa gráfica de madeira, sai um jornal impresso em duas línguas, inglês e cherokee. Imagine o trabalho: a escrita cherokee tinha sido inventada poucos anos antes por um homem só, Sequoyah.",
  f"printing_press|Inside a small log printing house in New Echota, Georgia, in 1828, {CHEROKEE} operating a wooden printing press, freshly printed sheets hanging to dry with only abstract marks" + SEC19 + SEMTXT,
  "newspaper_close|Close view of a freshly printed 19th century newspaper page with two columns of abstract illegible marks, ink roller beside it" + SEMTXT,
  f"sequoyah|{SEQUOYAH}, sitting outside a log cabin with a slate full of abstract symbols, proud" + SEC19 + SEMTXT,
  f"cherokee_read|{CHEROKEE} reading printed sheets together in front of a log house, a child pointing" + SEC19 + SEMTXT,
  card="1828")
b("Os Cherokee fizeram o que o país dizia admirar. Escreveram uma constituição, criaram tribunais, abriram escolas. Então acharam ouro nas terras deles.",
  "council_house|A Cherokee council house of 1827 with round-white-head cartoon Cherokee leaders in turbans and coats seated around a table, one reading a long document" + SEC19 + SEMTXT,
  "cherokee_school|A small log schoolhouse in the Cherokee Nation in 1828 with round-white-head cartoon Cherokee children at wooden benches" + SEC19 + SEMTXT,
  "gold_pan|Close view of a gold pan in a mountain stream with shiny gold flakes, the hands of a prospector" + SEC19,
  "gold_rush_ga|Round-white-head cartoon gold prospectors of 1829 rushing with picks and pans into green hills of Georgia" + SEC19 + SEMBAND)
b("Aí a Geórgia quis as terras. E os Cherokee fizeram uma coisa muito americana: processaram. Em mil oitocentos e trinta e dois, a Suprema Corte deu razão a eles.",
  "georgia_men|Round-white-head cartoon Georgia officials of 1830 in top hats pointing at a map of Cherokee land, greedy, comic" + SEC19 + SEMTXT,
  "lawyer_cherokee|Round-white-head cartoon Cherokee leaders in coats and turbans with an American lawyer carrying a stack of law books up the steps of a 19th century courthouse" + SEC19 + SEMTXT,
  "supreme_court_1832|A small 1830s courtroom with round-white-head cartoon judges in black robes at a long bench, the chief judge reading a decision" + SEC19 + SEMBAND + SEMTXT,
  "gavel|Close view of a wooden judge's gavel striking a block on a desk" + SEMTXT)
b("Só que o presidente Andrew Jackson não fez cumprir. Em mil oitocentos e trinta e oito, o exército tira cerca de dezesseis mil Cherokee de casa e os leva a pé para o oeste. Pelas estimativas, uns quatro mil morrem no caminho.",
  f"jackson_desk|{JACKSON}, sitting at his desk and pushing a paper aside, stern" + SEC19 + SEMTXT,
  f"removal_soldiers|{SOLDADOS30} escorting {CHEROKEE} away from their log houses, families carrying bundles, sad and dignified, seen from a distance" + SEC19 + SEMBAND + GUERRA,
  "trail_winter|A long line of round-white-head cartoon Cherokee families walking along a muddy road through a bare winter forest with wagons, seen from very far away, grey sky" + SEC19 + SEMBAND + GUERRA,
  "empty_cabin|An empty Cherokee log cabin with an open door and a cold fireplace, autumn leaves blowing in, nobody inside" + SEC19)
b("Cobrar pela lei nem sempre bastava. O problema estava ficando grande demais para caber num país só.",
  "map_trail|Map of the southeastern United States with a long dotted path running west from Georgia to the plains beyond the Mississippi river, " + MAPA,
  "court_empty|An empty 1830s courtroom with the bench and chairs, a decision paper left on the desk, dusty light" + SEC19 + SEMTXT,
  "bell_crack#detalhe-centro")

# ───────────────────────── 5. O SINO E A FRASE REESCRITA ─────────────────────────
cap("5. O sino e a frase reescrita")
b("§ Na mesma época, em Filadélfia, um sino velho ganha apelido novo. Os abolicionistas leem a inscrição dele, proclamai liberdade em toda a terra, e em mil oitocentos e trinta e cinco o chamam de Sino da Liberdade.",
  "bell_tower|The white bell tower of the old Pennsylvania State House in Philadelphia in the 1830s, red brick, pigeons, quiet street" + SEC19 + SEMBAND + SEMTXT,
  "abolitionists_print|Round-white-head cartoon abolitionists of 1835, Black and white men and women in dark clothes, around a small printing press, holding a pamphlet with a drawing of a bell" + SEC19 + SEMTXT,
  "bell_inscription|Close view of the upper band of an old bronze bell with a raised decorative strip and illegible worn marks" + SEMTXT,
  "bell_pamphlet|Close view of an 1830s pamphlet cover with a woodcut drawing of a bell and only abstract illegible marks" + SEMTXT,
  card="1835")
b("Os abolicionistas deram ao sino o nome de liberdade. Poucos anos depois, ele rachou. E em mil oitocentos e quarenta e seis, calou para sempre. Se você for a Filadélfia hoje, a rachadura continua lá.",
  "bell_crack#aberto",
  "bell_ring|Round-white-head cartoon bell ringers of 1846 pulling a rope to ring a big old bell, a crack spreading up the bronze, surprised faces, comic" + SEC19 + SEMTXT,
  "bell_silent|The cracked Liberty Bell hanging silent in a dim room, dust floating in a ray of light" + SEMTXT,
  f"bell_tourists|Round-white-head cartoon modern tourists with phones looking at the cracked Liberty Bell in a bright modern glass pavilion" + SEMBAND + SEMTXT)
b("§ Seneca Falls, Nova York, julho de mil oitocentos e quarenta e oito. Numa capela, umas trezentas pessoas ouvem Elizabeth Cady Stanton ler um texto que parece familiar.",
  "chapel_seneca|A small red brick Wesleyan chapel in Seneca Falls, New York, in July 1848, horses and buggies parked outside, summer" + SEC19 + SEMBAND + SEMTXT,
  f"stanton_read|{STANTON}, standing at a pulpit reading aloud from a sheet of paper, confident" + SEC19 + SEMTXT,
  f"seneca_crowd|{SENECA}, listening attentively, some surprised" + SEC19,
  "two_parchments|Close view of two documents side by side on a table, an old parchment and a newer paper, with almost identical illegible handwriting" + SEMTXT,
  card="1848")
b("É a Declaração de Independência, com duas palavras a mais: todos os homens e mulheres são criados iguais. Cem pessoas assinam. Uma delas é aquele homem do Quatro de Julho, Douglass.",
  "parchment_insert|Close view of a handwritten line on paper with a small caret mark and two words inserted above it in fresh ink, only illegible flowing marks" + SEMTXT,
  f"seneca_sign|{SENECA}: men and women lining up to sign a long paper on a table" + SEC19 + SEMTXT,
  f"douglass_sign|{DOUGLASS.replace('in 1852', 'in 1848')}, signing a long paper with a quill among women in bonnets, smiling" + SEC19 + SEMTXT,
  f"guide_two_words|{GUIA} holding a magnifying glass over a line of handwriting, delighted, comic" + SEMTXT)
b("E aqui está a segunda peça da resposta: ninguém precisou inventar uma ideia nova. Bastava pegar a frase de mil setecentos e setenta e seis e ler em voz alta, querendo dizer todos.",
  f"guide_piece2|{GUIA} placing a second puzzle piece next to the first one on the puzzle board, comic" + SEMTXT,
  "parchment_glow#detalhe-alto",
  f"read_aloud|Round-white-head cartoon people of different backgrounds in 19th century clothes reading the same paper aloud in a town square" + SEC19 + SEMBAND + SEMTXT,
  "douglass_point#médio-dir")
b("Só que o Sul tinha construído a riqueza em cima de quatro milhões de escravizados. E quando Abraham Lincoln é eleito, em mil oitocentos e sessenta, onze estados saem do país. Aí a cobrança vira guerra.",
  "cotton_field|A vast cotton field in the American South of 1860 with white cotton bolls, African American workers in the distance, a big white plantation house far away, hazy" + SEC19 + ESCRAV,
  f"lincoln_elected|{LINCOLN} standing in front of a crowd of 1860 in top hats, newly elected, serious" + SEC19 + SEMBAND + SEMTXT,
  "map_split|Map of the United States in 1861 with the southern states painted in grey and the northern states in blue, a jagged line between them, " + MAPA,
  "fort_cannon|A brick sea fort in a harbor at dawn in April 1861 with a cannon smoking in the foreground, seen from far away" + SEC19 + SEMBAND + GUERRA)

# ───────────────────────── 6. OITENTA E SETE ANOS ATRÁS ─────────────────────────
cap("6. Oitenta e sete anos atrás")
b("§ Gettysburg, Pensilvânia, novembro de mil oitocentos e sessenta e três. Num cemitério ainda sendo aberto, onde quatro meses antes aconteceu a maior batalha da guerra.",
  "gettysburg_field|Rolling green fields and low stone walls of Gettysburg, Pennsylvania, in November 1863, bare trees, rows of simple white wooden markers on a hill, grey sky, nobody lying on the ground" + SEC19 + SEMBAND + GUERRA + SEMTXT,
  "cemetery_rows|Rows of simple new white wooden grave markers on a grassy hill, autumn, solemn, no names" + SEC19 + SEMTXT,
  f"crowd_1863|A large crowd of round-white-head cartoon people of 1863 in coats and top hats gathered around a wooden platform in a field, {SOLD_UNIAO} standing guard" + SEC19 + SEMBAND,
  "stone_wall|A low stone wall in an empty field with a single forgotten kepi cap on top, autumn leaves" + SEC19 + GUERRA,
  card="1863")
b("O orador principal fala duas horas. Ninguém lembra do discurso dele. Depois, Lincoln fala por uns dois minutos. Duzentas e setenta e duas palavras: cabe na tela do seu celular.",
  "orator_long|A round-white-head cartoon elderly orator of 1863 with white hair, speaking with grand gestures on a wooden platform, a sundial-like pocket watch showing the time passing, audience yawning, comic" + SEC19 + SEMBAND + SEMTXT,
  "pocket_watch|Close view of an open 19th century pocket watch in a hand, comic" + SEMTXT,
  f"lincoln_podium|{LINCOLN}, standing on a wooden platform holding a small sheet of paper, speaking calmly to a crowd" + SEC19 + SEMBAND + SEMTXT,
  "small_paper|Close view of a small folded sheet of paper with a few lines of illegible handwriting in a hand" + SEMTXT)
b("E a primeira frase é uma conta: oitenta e sete anos atrás. Repare: oitenta e sete anos antes não é a Constituição. É mil setecentos e setenta e seis. Lincoln diz que o país nasceu daquela frase.",
  f"lincoln_close|{LINCOLN}, seen from below, speaking, solemn, grey sky behind" + SEC19 + SEMBAND,
  f"guide_count|{GUIA} counting on his fingers in front of a big calendar with abstract pages flying back in time, comic" + SEMTXT,
  "hall_1776#detalhe-centro",
  "parchment_glow#aberto")
b("A guerra termina em mil oitocentos e sessenta e cinco, com algo entre seiscentos e vinte e setecentos e cinquenta mil mortos. Aí vêm três emendas: acaba a escravidão, quem nasce no país é cidadão, e homem negro pode votar.",
  "battlefield_after|An empty battlefield in 1865 at dawn after the war, broken fences, a quiet field of grass, mist, a few abandoned caps and a drum on the ground, nobody lying on the ground" + SEC19 + SEMBAND + GUERRA,
  f"freed_families|{LIBERTOS}, walking together along a country road at sunrise carrying bundles, hopeful" + SEC19,
  "capitol_1868|The United States Capitol building in Washington in 1868 with its new white dome, horse carriages in front" + SEC19 + SEMBAND + SEMTXT,
  "first_vote|A round-white-head cartoon African American man of 1870 in a dark suit dropping a paper ballot into a wooden ballot box, proud, other men in line behind him" + SEC19 + SEMBAND + SEMTXT)
b("Então, pela primeira vez, a frase entra na lei. Só que no Sul, em poucos anos, novas leis tiram o voto de volta e separam escolas, trens e bebedouros. A conta foi paga, e logo depois, estornada.",
  "law_book|Close view of a heavy law book opening with golden light coming out of the pages, illegible script" + SEMTXT,
  "segregated_train|A 19th century train car with a wooden partition dividing it into two sections, empty seats, serious" + SEC19 + SEMTXT,
  "two_fountains|Two plain water fountains side by side on a brick wall, one shiny and one rusty, serious, no signs" + SEMTXT,
  "torn_receipt|Symbolic scene: a paper receipt torn in two pieces falling onto a wooden desk" + SEMTXT)

# ───────────────────────── 7. A ESTÁTUA E A PORTA FECHADA ─────────────────────────
cap("7. A estátua e a porta fechada")
b("§ Filadélfia, quatro de julho de mil oitocentos e setenta e seis, cem anos da Declaração. No meio da festa oficial, cinco mulheres sobem até a tribuna com um papel que ninguém pediu.",
  "centennial|A grand outdoor centennial celebration in front of Independence Hall in Philadelphia in 1876, crowds in Victorian clothes, red white and blue bunting without stars, officials on a platform" + SEC19 + SEMBAND + SEMTXT,
  f"women_march|{SUFRAG76}, five women walking firmly through the crowd toward the official platform holding a rolled paper" + SEC19 + SEMTXT,
  "official_platform|Round-white-head cartoon officials of 1876 in top hats on a decorated wooden platform, one of them looking surprised at a rolled paper being handed to him, comic" + SEC19 + SEMBAND + SEMTXT,
  "centennial_fireworks|Fireworks over Philadelphia at night in 1876, the bell tower of Independence Hall in silhouette" + SEC19,
  card="1876")
b("É a Declaração dos Direitos das Mulheres. Lá fora, Susan B. Anthony lê o texto para a multidão. Imagine a cara das autoridades: era o aniversário da liberdade, e a liberdade veio cobrar.",
  f"anthony_read|{ANTHONY}, standing on a small platform outside a brick hall reading a document aloud to a crowd, determined" + SEC19 + SEMTXT,
  "officials_faces|Round-white-head cartoon officials of 1876 in top hats with shocked and embarrassed faces, comic" + SEC19,
  f"crowd_listen|Round-white-head cartoon crowd of 1876 in Victorian clothes listening, some women clapping" + SEC19 + SEMBAND,
  "bill_paper|Symbolic comic scene: a long paper bill being handed to a birthday cake shaped like a brick building with one hundred candles" + SEMTXT)
b("§ Nas décadas seguintes, os Estados Unidos viram a maior economia industrial do mundo. Aço, trilhos, petróleo. Agora olhe para quem acende os fornos: milhões de imigrantes.",
  "steel_mill|A huge steel mill of the 1890s in Pittsburgh with tall smoking chimneys, glowing furnaces and rivers of molten metal" + SEC19.replace("no electric lights, ", "") + SEMTXT,
  f"workers_furnace|{OPERARIOS} working at a glowing furnace, sweaty and strong" + SEC19.replace("no electric lights, ", "") + SEMTXT,
  "railroad_1890|A steam train crossing a huge iron bridge over a river in the 1890s, smoke trailing" + SEC19 + SEMBAND + SEMTXT,
  "oil_derricks|A field of wooden oil derricks in Pennsylvania in the 1880s, barrels and workers" + SEC19 + SEMTXT)
b("Aqui está a outra metade da nossa pergunta, a potência. Ela foi feita com gente que chegava. Em mil oitocentos e oitenta e seis, a França dá de presente uma estátua: a Liberdade.",
  f"ellis_boat|{IMIGRANTES} crowded on the deck of a steamship arriving in New York harbor, looking up in awe" + SEMBAND + SEMTXT,
  "statue_1886|The Statue of Liberty newly built on its island in New York harbor in 1886, steamships and sailboats around it, a small crowd celebrating" + SEMBAND + SEMTXT,
  "ellis_hall|The great registry hall of Ellis Island around 1900 full of round-white-head cartoon immigrants with bags waiting in lines" + SEMBAND + SEMTXT,
  f"guide_statue|{GUIA} looking up at the giant Statue of Liberty, mouth open, comic" + SEMBAND + SEMTXT)
b("Só que, quatro anos antes, uma lei tinha proibido a entrada de trabalhadores chineses. A porta abria e fechava ao mesmo tempo.",
  f"chinese_rail|{CHINESES} building a railroad through the mountains of the American West in the 1860s with picks and wheelbarrows" + SEC19 + SEMTXT,
  "door_half|Symbolic scene: a huge wooden door in a harbor, half open with sunlight on one side and closed with a lock on the other, serious" + SEMTXT,
  "sf_port|The port of San Francisco in the 1880s with wooden piers, steamships and round-white-head cartoon Chinese passengers being stopped by officials at a gate" + SEC19 + SEMBAND + SEMTXT)
b("Aí um cozinheiro de São Francisco, filho de chineses, volta de viagem e é barrado no porto. Wong Kim Ark cobra a frase pela emenda de mil oitocentos e sessenta e oito: eu nasci aqui.",
  f"wong_port|{WONG}, standing at a ship's gangway in San Francisco in 1895, stopped by a round-white-head cartoon customs officer in uniform holding up his hand" + SEC19 + SEMBAND + SEMTXT,
  f"wong_cell|{WONG}, waiting on a wooden bench in a plain harbor detention room, looking out of a small window at the city" + SEC19 + SEMTXT,
  f"wong_papers|{WONG}, holding out a birth paper with confidence, close view" + SEC19 + SEMTXT,
  "sf_chinatown|A street in San Francisco's Chinatown in the 1890s with wooden balconies, red lanterns and round-white-head cartoon people" + SEC19 + SEMTXT)
b("Em mil oitocentos e noventa e oito, a Suprema Corte concorda: quem nasce no país é cidadão, mesmo filho de estrangeiros. É isso que transforma imigrante em americano em uma geração. O problema: e as americanas, que ainda não votavam?",
  "court_1898|The Supreme Court chamber of 1898 with round-white-head cartoon judges in black robes at a long bench, one reading a decision" + SEC19 + SEMBAND + SEMTXT,
  "baby_family|A round-white-head cartoon immigrant family of 1900 holding a newborn baby in a small apartment, proud and happy" + SEMTXT,
  "generations|Symbolic scene: a round-white-head cartoon immigrant grandfather with a suitcase, his son in a worker's cap and his granddaughter in a 1920s school uniform standing side by side" + SEMTXT,
  "women_window|Round-white-head cartoon American women of 1900 looking through a window at men lining up to vote, crossed arms" + SEMBAND + SEMTXT)

# ───────────────────────── 8. UM BILHETE DE MÃE ─────────────────────────
cap("8. Um bilhete de mãe")
b("§ Washington, mil novecentos e dezessete. O presidente Woodrow Wilson leva o país à Primeira Guerra Mundial para que o mundo fique seguro para a democracia. Na calçada da Casa Branca, mulheres com faixas perguntam: e aqui?",
  f"wilson_speech|{WILSON}, speaking at a podium in Congress in April 1917, raising a finger" + SEMBAND + SEMTXT,
  f"sentinels|{SENTINELAS}, standing in a silent line on the sidewalk in front of the iron fence of the White House in winter, holding blank banners" + SEMBAND + SEMTXT,
  "white_house_1917|The White House in Washington in 1917 seen through its iron fence, a few early automobiles on the street, winter" + SEMBAND + SEMTXT,
  f"wilson_window|{WILSON}, peeking through a White House curtain at the women outside, annoyed, comic" + SEMTXT,
  card="1917")
b("Algumas vão presas por isso. Mas a guerra acaba, e a pressão não. Em agosto de mil novecentos e vinte, falta um estado para a emenda do voto feminino valer. O Tennessee.",
  "arrest_1917|Round-white-head cartoon police officers of 1917 leading calm suffragists in long coats into a police wagon, seen from a distance, no violence" + SEMBAND + SEMTXT,
  "map_states_1920|Map of the United States where most states are painted in gold and one state in the south, Tennessee, is left blank in the middle, " + MAPA,
  "nashville_capitol|The Tennessee State Capitol in Nashville in August 1920, a classical building on a hill, round-white-head cartoon people with yellow and red roses arriving" + SEMBAND + SEMTXT,
  "roses|Close view of yellow roses and red roses pinned on the lapels of men in suits" + SEMTXT,
  card="1920")
b("Aí um deputado de vinte e quatro anos, Harry Burn, que vinha votando contra, tem no bolso uma carta da mãe dele. Ela escreveu: seja um bom menino. Ele vota sim.",
  f"burn_desk|{BURN}, sitting at his desk in the crowded Tennessee House chamber, nervous" + SEMBAND + SEMTXT,
  f"burn_letter|{BURN}, reading a small handwritten letter from his pocket, eyes wide" + SEMTXT,
  "mother_letter|A round-white-head cartoon elderly farm woman of 1920 in a simple dress writing a letter at a kitchen table in rural Tennessee" + SEMTXT,
  f"burn_vote|{BURN}, standing and saying yes in the chamber, other legislators turning their heads in shock, comic" + SEMBAND + SEMTXT)
b("Pense nisso da próxima vez que você ignorar uma mensagem da sua mãe. Mais de vinte e cinco milhões de mulheres ganham o voto.",
  f"guide_phone|{GUIA} looking at a modern phone with a message notification and quickly answering it, guilty, comic" + SEMTXT,
  "women_vote_1920|Round-white-head cartoon American women of 1920 in cloche hats lining up and casting paper ballots into a wooden box, joyful" + SEMBAND + SEMTXT,
  "celebration_1920|Round-white-head cartoon women of 1920 celebrating in a street with yellow sashes, throwing hats in the air" + SEMBAND + SEMTXT)
b("§ Depois vem a quebra da bolsa de mil novecentos e vinte e nove, e o governo passa a garantir o que nunca garantiu: aposentadoria e salário mínimo. Só que, lá fora, o mundo estava de novo pegando fogo.",
  "crash_1929|Round-white-head cartoon men of 1929 in suits and hats crowding a street in front of a closed bank, worried" + SEMBAND + SEMTXT,
  "breadline|A long line of round-white-head cartoon unemployed men of 1931 in coats and caps waiting for bread on a city sidewalk, grey" + SEMBAND + SEMTXT,
  "radio_family|A round-white-head cartoon American family of 1935 listening to a big wooden radio in their living room, hopeful" + SEMTXT,
  "globe_fire|Symbolic scene: an old desk globe with small flames rising from Europe and Asia, dark room" + SEMTXT)

# ───────────────────────── 9. O ARSENAL E O DUPLO V ─────────────────────────
cap("9. O arsenal e o Duplo V")
b("§ Junho de mil novecentos e quarenta e um. As fábricas americanas já fazem armas para a guerra na Europa, mas quase não contratam negros. Então um sindicalista, A. Philip Randolph, promete levar cem mil pessoas a Washington.",
  "factory_gate_1941|The gate of a big American arms factory in 1941 with a long line of round-white-head cartoon job seekers, Black workers being turned away by a guard, serious" + SEMSIMB,
  f"randolph|{RANDOLPH}, speaking to a meeting of railroad porters in a union hall, raising his hand, determined" + SEMSIMB,
  "march_flyer|Close view of a stack of 1941 leaflets on a table with a drawing of the Capitol dome and only abstract illegible marks" + SEMSIMB,
  "porters_organize|Round-white-head cartoon African American sleeping car porters of 1941 in uniforms and caps handing out leaflets on a train platform" + SEMSIMB,
  card="1941")
b("Uma semana antes da data, o presidente Roosevelt assina uma ordem proibindo a discriminação nas fábricas de guerra. Imagine conseguir isso só com a ameaça de uma passeata.",
  f"fdr_sign|{FDR}, sitting at his desk in the Oval Office signing a paper, aides around him" + SEMSIMB,
  f"guide_march|{GUIA} holding a blank sign and looking amazed at a signed paper flying out of a window of the White House, comic" + SEMSIMB,
  "workers_hired|Round-white-head cartoon Black and white workers of 1942 side by side on an aircraft assembly line, riveting" + SEMSIMB,
  f"randolph_smile|{RANDOLPH}, reading a newspaper and smiling slightly" + SEMSIMB)
b("Aí vem Pearl Harbor, e o país inteiro vira fábrica. Só que mais de um milhão de soldados negros servem em tropas separadas. Em mil novecentos e quarenta e dois, um jornal negro de Pittsburgh lança uma campanha: Duplo V. Vitória lá fora, e vitória aqui dentro.",
  "pearl_smoke|A naval harbor in Hawaii in December 1941 seen from far away, columns of dark smoke rising over grey ships, palm trees, nobody visible" + SEMSIMB,
  "factory_tanks|A huge American car factory of 1942 converted to build tanks, long assembly lines of olive green tanks, sparks" + SEMSIMB,
  f"segregated_units|{SOLD42}, standing in formation at a separate camp, white soldiers in another camp in the distance, serious" + SEMSIMB,
  "courier_press|Inside a newspaper office in Pittsburgh in 1942, round-white-head cartoon African American journalists in shirtsleeves and vests at typewriters and a big printing press" + SEMSIMB,
  "double_v|Symbolic scene: two big golden V shapes, one overlapping the other, glowing on a dark blue background, no letters, no other symbols",
  f"soldier_letter|{SOLD42}: one soldier writing a letter on a wooden crate, determined" + SEMSIMB)
b("Em mil novecentos e quarenta e cinco, a guerra acaba. Então os Estados Unidos saem dela com cerca de metade da produção industrial do mundo. Repare: é a maior potência da Terra.",
  "ruins_vs_factories|Symbolic split scene: on the left a ruined European city in 1945 with broken buildings, on the right a busy American industrial city with working factories and ships, no people in danger" + SEMSIMB,
  "port_1945|A huge busy American port in 1945 full of cargo ships, cranes and trains" + SEMSIMB,
  "map_usa_today#aberto",
  "planes_rows|Rows of hundreds of new military airplanes parked on an airfield in 1944 seen from above" + SEMSIMB)
b("E aí vem a parte estranha. Em setembro, em Hanói, um líder que meses antes trabalhava com agentes americanos declara a independência do Vietnã. A primeira frase ele pega emprestada: todos os homens são criados iguais.",
  "hanoi_square|A large square in Hanoi in September 1945 full of round-white-head cartoon Vietnamese people in white shirts and conical hats, facing a simple wooden stage, trees around" + SEMSIMB,
  f"ho_speech|{HO}, reading from a sheet of paper on a simple wooden stage, calm" + SEMSIMB,
  "parchment_glow#médio-esq",
  f"guide_surprise|{GUIA} reading a letter and dropping his hat in surprise, comic" + SEMTXT)
b("A frase tinha virado produto de exportação. E isso criou um problema.",
  "export_crate|Symbolic comic scene: a wooden export crate on a cargo ship with a glowing old parchment inside, about to be shipped" + SEMSIMB,
  "globe_light|Symbolic scene: an old desk globe with small points of golden light appearing on different continents" + SEMTXT,
  "cold_war_chess|Symbolic scene: a giant chessboard over a map of the world, one side of pieces in blue and the other in red, tense" + SEMSIMB)

# ───────────────────────── 10. O CHEQUE SEM FUNDOS ─────────────────────────
cap("10. O cheque sem fundos")
b("§ Mil novecentos e cinquenta e dois. Na Guerra Fria, a União Soviética usa fotos da segregação americana como propaganda. Então o próprio governo dos Estados Unidos escreve à Suprema Corte: a discriminação racial dá munição aos comunistas.",
  "propaganda_wall|Symbolic scene: a wall in a cold grey city covered with blank posters and photographs turned away from the viewer, people in heavy coats looking at them" + SEMSIMB,
  "washington_office|A government office in Washington in 1952 with a round-white-head cartoon official in a grey suit dictating a letter to a typist, serious" + SEMSIMB,
  "segregated_school|Two school buildings of 1952 side by side, one new and bright, one old and shabby, round-white-head cartoon children walking to each, serious" + SEMSIMB,
  "court_1954|The marble Supreme Court building in Washington in 1954 with round-white-head cartoon people on the steps" + SEMSIMB,
  card="1952")
b("Repare na terceira peça da resposta: virar potência deixou o país exposto. Pense bem: quem quer liderar o mundo livre precisa parecer livre. Em mil novecentos e cinquenta e quatro, a Corte declara inconstitucional a escola separada.",
  f"guide_piece3|{GUIA} placing a third puzzle piece on the puzzle board next to the other two, comic" + SEMTXT,
  "spotlight_map|Symbolic scene: a giant spotlight from the sky shining on a map of the United States while the rest of the world watches in the dark" + SEMSIMB,
  "school_door|Round-white-head cartoon Black and white children of 1954 walking together through the open door of a school, hopeful" + SEMSIMB,
  "newspaper_1954|Close view of a 1954 newspaper being read on a porch, only abstract illegible columns" + SEMTXT)
b("§ Washington, agosto de mil novecentos e sessenta e três. Duzentas e cinquenta mil pessoas diante do memorial de Lincoln. Martin Luther King diz que os fundadores assinaram uma nota promissória.",
  f"march_1963|A huge crowd of {MARCHA} filling the long reflecting pool area in front of the Lincoln Memorial in Washington in August 1963, seen from above" + SEMSIMB,
  f"king_podium|{KING}, speaking passionately at the podium on the steps of the Lincoln Memorial, crowd below" + SEMSIMB + "@@MARTIN LUTHER KING",
  "lincoln_memorial|The white marble Lincoln Memorial with its columns and the seated statue inside, summer light, crowd on the steps" + SEMSIMB,
  f"march_faces|Close view of {MARCHA}, listening with emotion" + SEMSIMB,
  card="1963")
b("E que a América deu a uma parte dos seus cidadãos um cheque sem fundos. Mas, diz King: nós nos recusamos a acreditar que o banco da justiça está falido.",
  "bad_check|Close view of an old bank check on a wooden desk with a big red ink rejection stripe across it, only abstract illegible marks, no readable words" + SEMTXT,
  "bank_vault|Symbolic scene: a huge round bank vault door swinging open with golden light coming out, hopeful" + SEMTXT,
  "king_podium#detalhe-centro",
  f"crowd_cheer|{MARCHA} raising their hands and cheering, hopeful" + SEMSIMB)
b("Em dois anos vêm as leis dos direitos civis, do voto, e de uma imigração sem cota por país de origem. Em mil novecentos e noventa e um, a União Soviética acaba, e sobra uma superpotência só. Então, lembra da nossa pergunta?",
  "signing_1964|A round-white-head cartoon American president of 1964 in a dark suit signing a law at a desk surrounded by people, pens on the desk" + SEMSIMB,
  "voters_1965|Round-white-head cartoon African American voters of 1965 lining up at a polling place in the South, proud" + SEMSIMB,
  "airport_1966|A busy American airport arrival hall of the late 1960s with round-white-head cartoon immigrants from many countries carrying suitcases" + SEMSIMB,
  "wall_1991|Symbolic scene: a red star made of stone on a pedestal cracking and crumbling in a grey square, 1991, people watching from far away" + SEMBAND,
  f"guide_back|{GUIA} turning around and pointing back toward a tiny old lecture hall far behind him in the distance, comic" + SEMTXT)

# ───────────────────────── FECHO (≤ 45 s) ─────────────────────────
cap("Fecho")
b("§ A frase não fez dos Estados Unidos uma potência sozinha. Construiu o país porque estava escrita, para todos, e qualquer um podia cobrar. Cada cobrança paga abriu a porta para mais gente: no voto, na fábrica, no exército.",
  "parchment_glow#detalhe-baixo",
  "line_people#aberto",
  "door_open_final|Symbolic scene: a huge old wooden door wide open with warm golden light pouring out onto a long line of round-white-head cartoon people of all eras walking in" + SEMBAND + SEMTXT)
b("Douglass perguntou de quem era aquele Quatro de Julho. Em dois mil e vinte e seis, o país fez duzentos e cinquenta anos, e a resposta continua mudando a cada cobrança.",
  "douglass_window#aberto",
  "bell_tourists#médio-esq",
  "hall_today|Independence Hall in Philadelphia today, the same red brick building with the white bell tower, small between tall glass skyscrapers, round-white-head cartoon tourists, bright blue sky" + SEMBAND + SEMTXT,
  card="2026")
b("[warm] Talvez a pergunta nunca tenha sido como eles viraram potência apesar da frase. E sim por causa dela. Qual dessas cobranças te surpreendeu mais? Conta nos comentários.",
  f"guide_end|{GUIA} sitting on the steps of an old red brick building with a white bell tower, holding a rolled parchment and smiling at the viewer" + SEMBAND + SEMTXT,
  "map_usa_today#detalhe-centro")

# Grafia para a VOZ (o Fish lê como português). Conferir no teste de nomes (qa/pronuncia/).
# blocos.json leva "texto" (falado, vai ao Fish) e "tela" (grafia correta: legendas e SCRIPT).
FALA = [("Rochester", "Rótchester"), ("Frederick Douglass", "Frédérik Dâglas"), ("Douglass", "Dâglas"),
        ("Jamestown", "Djêimstáun"), ("White Lion", "Uáit Láion"), ("Thomas Jefferson", "Tômas Djéferson"), ("Jefferson", "Djéferson"),
        ("Abigail Adams", "Ábigueil Édams"), ("John", "Djón"), ("George", "Djórdj"), ("Sequoyah", "Sicóia"),
        ("Andrew Jackson", "Éndru Djéquisson"), ("Seneca Falls", "Sêneca Fóls"), ("Elizabeth Cady Stanton", "Elízabeth Quêidi Stânton"),
        ("Abraham Lincoln", "Abraão Líncoln"), ("Lincoln", "Líncoln"), ("Gettysburg", "Guétisburg"), ("Pensilvânia", "Pensilvânia"),
        ("Susan B. Anthony", "Súzan Bí Éntoni"), ("Wong Kim Ark", "Uóng Quim Árk"), ("São Francisco", "São Francisco"),
        ("Woodrow Wilson", "Uúdrou Uílson"), ("Tennessee", "Ténessi"), ("Harry Burn", "Rári Bârn"), ("Pearl Harbor", "Pérl Rárbor"),
        ("Pittsburgh", "Pítsburg"), ("A. Philip Randolph", "Ei Fílip Rêndolf"), ("Roosevelt", "Rôusvelt"), ("Hanói", "Hanói"), ("Martin Luther King", "Mártin Lúter King"), ("King", "King"),
        ("Virgínia", "Virgínia"), ("Cherokee", "Tcherokí"), ("cherokee", "tcherokí")]
def fala(t):
    for a, z in FALA: t = re.sub(r"(?<![\wÀ-ú])" + re.escape(a) + r"(?![\wÀ-ú])", z, t)
    return t

IDEIA = set()
THUMB = None   # thumbs nascem dos 3 conceitos aprovados no crivo (EMBALAGEM.md r3): arte na etapa 2 (skill thumbnail)

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
