#!/usr/bin/env python3
"""Fonte única do dossie-es 011 (Los Templarios): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (na pasta do vídeo). Conteúdo no topo; geração no fim (copiada do 010-cartel-medellin).

Embalagem aprovada no crivo r3 (17/11/2026, EMBALAGEM.md/CRIVO.md):
  A/T1 "Cómo los templarios criaron a un rey… y su nieto los asedió" + coroa de menino sobre o manto, sigla TEMPLARIOS + sello HUÉRFANO
  B/T2 "TEMPLARIOS: declarados inocentes cuando la orden ya no existía" + sentença com 6 selos pendentes, "TARRAGONA"
  C/T3 "Monzón, 1309: los últimos templarios en armas" + trabuco contra a lua diante do castelo, "¿HEREJES?"
  Frase-âncora do hook: "Esta es TODA la historia de los Templarios. Y de cómo terminó en Aragón."
Ângulo (ANGULO.md): a ordem contada pela Coroa de Aragão; fio = o castelo de Monzón (1143 → 1214 → 1309 → Hospitalários).
Fora da manada: El Hábito, La Plaza (Calatrava), El Niño, La Isla, La Orden (a de Jaime II, 1/12/1307), La Bandera (Caminha).
Fatos obrigatórios da manada (fundação, Troyes, banco, Acre, Paris 1307, Chinon, Vienne, Molay) só como contexto curto.

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (id I### na ordem de aparição) · "chave" reuso · "chave#enq" reuso com enquadramento
  + "@@TEXTO"      rótulo na tela (máquina de escrever; CAIXA ALTA, até ~28 caracteres)
Bloco: b(texto, *planos, card="MONZÓN, 1309", ideia=True) · capítulo: cap("5. La Encomienda")
Mapas (chave map_*): base sem texto nem pinos; pinos, setas e nomes no código (src/labels.jsx).
"""
import json, math, re
from pathlib import Path

WPS = 2.38           # palavras/s medidas no 001–008 (erro de 1–3%)
BREAK, LONG = 0.35, 0.8
MAX_PLANO_INICIO = 3.0   # s por plano nos primeiros INICIO s (~20 cortes/min)
INICIO = 60.0
MAX_PLANO = 3.6      # s por plano depois (~17 cortes/min)
INEDITO_ATE = 180.0  # s: só imagens novas até aqui
JANELA = 60.0        # s: mesmo enquadramento da mesma imagem só depois disso
HOOK_MAX = 36.0      # s: a bíblia pede hook de 25–35 s (EMBALAGEM: teto 0:35)
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "Cómo los templarios criaron a un rey… y su nieto los asedió"
PROMESSA = ("TODA la historia de los Templarios contada desde la Corona de Aragón: la orden que crió a un rey niño acaba sitiada "
            "por el nieto de ese rey en el mismo castillo, como los últimos templarios en armas del reino, y es declarada inocente "
            "en Tarragona cuando ya no existía.")

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Monzón, reino de Aragón, mayo de mil trescientos nueve.", card="MONZÓN, 1309")
b("Las tropas del rey Jaime Segundo llevan meses asediando este castillo. Dentro resisten, en armas, los últimos templarios del reino.")
b("Noventa y cinco años antes, aquí mismo, la orden crió a un niño huérfano: el abuelo de este rey.")
b("Se rinden. Tres años y medio después, un concilio en Tarragona los declara inocentes. Ya no queda orden que salvar.")
b("Esta es TODA la historia de los Templarios. Y de cómo terminó en Aragón.", ideia=True)

# ───────────────────────── 1. EL VOTO ─────────────────────────
cap("1. El Voto")
b("El Voto. Jerusalén, hacia mil ciento veinte. Un caballero de Champaña, Hugo de Payns, y unos pocos compañeros hacen sus votos de pobreza, castidad y obediencia ante el patriarca de Jerusalén. Son monjes, pero conservan la espada.", card="JERUSALÉN, 1120")
b("Su misión es proteger a los peregrinos en los caminos de Tierra Santa. El rey de Jerusalén les cede parte de su palacio, en el monte del Templo. De ahí el nombre: templarios.")
b("En mil ciento veintinueve, un concilio en Troyes, en Francia, les da una regla. Desde entonces, reyes y nobles de toda Europa les regalan tierras y dinero.")
b("Pero uno de los primeros grandes regalos no llega de Francia. Llega de Barcelona.", ideia=True)

# ───────────────────────── 2. EL HÁBITO ─────────────────────────
cap("2. El Hábito")
b("El Hábito. Barcelona, julio de mil ciento treinta y uno. El conde Ramón Berenguer Tercero, señor de Barcelona y de media Cataluña, está enfermo.", card="BARCELONA, 1131")
b("Ya había entregado a los templarios el castillo de Grañena, en tierras recién ganadas a los musulmanes. Ahora hace algo más: pocos días antes de morir, ingresa en la orden.")
b("No es un caso raro. En ese siglo, muchos nobles piden entrar en una orden en su lecho de muerte, para morir como hermanos y ser enterrados con ella.")
b("Uno de los hombres más poderosos de la Península muere como hermano del Temple. Y ese mismo año, otro rey va todavía más lejos.", ideia=True)

# ───────────────────────── 3. EL TESTAMENTO ─────────────────────────
cap("3. El Testamento")
b("El Testamento. Bayona, octubre de mil ciento treinta y uno. Alfonso Primero de Aragón, el Batallador, no tiene hijos. Mientras asedia la ciudad, dicta su testamento.", card="BAYONA, 1131")
b("Deja sus reinos, Aragón y Pamplona, a tres órdenes religiosas: el Santo Sepulcro, los hospitalarios y los templarios. Muere en mil ciento treinta y cuatro, y los nobles no cumplen su voluntad.")
b("Nueve años después, en Gerona, el Temple renuncia a su parte del reino. A cambio recibe castillos, entre ellos Monzón, sobre una roca junto al río Cinca. Ese castillo va a volver una y otra vez a esta historia.", card="GERONA, 1143")
b("Cuatro años después, el Temple recibe otra fortaleza. Esta vez, en Castilla.", ideia=True)

# ───────────────────────── 4. LA PLAZA ─────────────────────────
cap("4. La Plaza")
b("La Plaza. Calatrava, mil ciento cuarenta y siete. El rey Alfonso Séptimo conquista esta fortaleza junto al río Guadiana y la entrega a los templarios.", card="CALATRAVA, 1147")
b("Es la llave del camino hacia Toledo. Diez años después, los almohades avanzan desde el sur. A fines de mil ciento cincuenta y siete, los templarios abandonan la plaza.")
b("En enero de mil ciento cincuenta y ocho, el rey Sancho Tercero se la ofrece a quien quiera defenderla. La acepta un abad cisterciense, Raimundo de Fitero. De ahí nace otra orden: la de Calatrava.")
b("En Castilla, el Temple perdió una plaza. En Aragón, Monzón sigue en pie. Y allí le van a confiar algo más valioso que un castillo.", ideia=True)

# ───────────────────────── 5. EL NIÑO ─────────────────────────
cap("5. El Niño")
b("El Niño. Muret, Francia, doce de septiembre de mil doscientos trece. El rey Pedro Segundo de Aragón muere en batalla. Su esposa había muerto en Roma ese mismo año.", card="MURET, 1213")
b("Su único hijo, Jaime, tiene cinco años y está en manos del enemigo de su padre, Simón de Montfort. El papa Inocencio Tercero ordena que lo devuelvan.")
b("Montfort lo tenía desde mil doscientos once, prometido a una de sus hijas. Ahora obedece al papa y entrega al niño a un enviado de Roma.")
b("En mil doscientos catorce, el niño rey llega a Monzón. Lo custodia el maestre del Temple en Aragón y Cataluña, Guillem de Montredón.", card="MONZÓN, 1214")
b("Años después, el propio Jaime lo cuenta en su crónica: el maestre lo llevó a Monzón y allí estuvo dos años y medio. Sale en mil doscientos diecisiete, con nueve años.")
b("La orden ha criado a un rey. Y ese rey va a necesitarla en el mar.", ideia=True)

# ───────────────────────── 6. LA ISLA ─────────────────────────
cap("6. La Isla")
b("La Isla. Santa Ponsa, Mallorca, septiembre de mil doscientos veintinueve. Jaime ya tiene veintiún años y desembarca para conquistar la isla.", card="MALLORCA, 1229")

b("Entre sus tropas van los templarios. El treinta y uno de diciembre cae la ciudad de Mallorca, la actual Palma. La orden recibe tierras en la isla por su ayuda.")
b("En su crónica, Jaime recuerda esa campaña con detalle: la tormenta en la travesía, el desembarco y los meses de asedio frente a la ciudad.")
b("Nueve años después, en mil doscientos treinta y ocho, Jaime entra en Valencia. Otra vez el Temple está a su lado. Ese rey pasará a la historia como Jaime el Conquistador.")
b("Para entonces, los templarios de Aragón son una pieza del reino. Hasta que un nieto de Jaime recibe noticias de París.", ideia=True)

# ───────────────────────── 7. LA ORDEN ─────────────────────────
cap("7. La Orden")
b("La Orden. Corona de Aragón, uno de diciembre de mil trescientos siete. Jaime Segundo, nieto del niño de Monzón, firma una orden: detener a los templarios de sus reinos y tomar sus bienes.", card="ARAGÓN, 1307")
b("Encarga el proceso al inquisidor y a los obispos de Valencia y de Zaragoza. Sus oficiales salen hacia las casas de la orden, una por una.")
b("La idea no es suya. Siete semanas antes, el rey de Francia había hecho arrestar a todos los templarios de su reino. La orden de arresto los acusaba de herejía: de renegar de Cristo y escupir sobre la cruz.", card="PARÍS, 1307")
b("El papa Clemente Quinto protestó. Pero el veintidós de noviembre cedió, y ordenó arrestarlos en toda la cristiandad. La orden ya no tenía Tierra Santa que defender: la había perdido en Acre, en mil doscientos noventa y uno.")
b("Los templarios de Aragón no esperan a los oficiales del rey. Hacen lo que casi nadie hizo en Francia: se encierran en sus castillos.", ideia=True)
b("Si este expediente te está gustando, suscríbete: así no te pierdes el próximo. Y ahora, volvemos a Monzón.")

# ───────────────────────── 8. EL ASEDIO ─────────────────────────
cap("8. El Asedio")
b("El Asedio. Monzón, fines de mil trescientos ocho. Las tropas de Jaime Segundo rodean la roca sobre el Cinca. Arriba, en el castillo donde la orden custodió a su abuelo, resisten los templarios.", card="MONZÓN, 1308")
b("No son los únicos. En Miravet, sobre el río Ebro, veintidós hombres aguantan unos diez meses. Se rinden el doce de diciembre. Seis de ellos se niegan hasta el final a entregarse por su voluntad.", card="MIRAVET, 1308")
b("En Monzón pasa el invierno. Nadie viene a ayudarlos. En mayo de mil trescientos nueve, Monzón y Chalamera, entre los últimos, se rinden.")
b("Los últimos templarios en armas del reino salen como prisioneros. Su destino ya no lo decide el rey de Aragón: lo decide la Iglesia.", ideia=True)

# ───────────────────────── 9. EL CONCILIO ─────────────────────────
cap("9. El Concilio")
b("El Concilio. Meses antes de la rendición de Monzón, en agosto de mil trescientos ocho, en el castillo de Chinon, tres cardenales del papa interrogan al gran maestre, Jacques de Molay, y a otros jefes de la orden.", card="CHINON, 1308")
b("Según la historiadora Barbara Frale, que redescubrió el pergamino en el Archivo Apostólico Vaticano en dos mil uno, los cardenales los absuelven si piden perdón. No es una absolución de la orden. Y el papa no la hace pública.")
b("En Castilla, el concilio de Salamanca de mil trescientos diez declara inocentes a los templarios del reino. En Portugal, el rey Dionisio toma sus bienes, pero no los encarcela.")
b("El veintidós de marzo de mil trescientos doce, el papa firma la bula que disuelve la orden y la anuncia en el concilio de Vienne. No dice que sea culpable: dice que ya no puede seguir.")

b("Siete meses después, el cuatro de noviembre de mil trescientos doce, el concilio de Tarragona juzga a los templarios de la Corona de Aragón. Los declara inocentes. Según los historiadores, reciben una pensión y viven el resto de su vida en antiguas casas de la orden.", card="TARRAGONA, 1312")
b("En París, en marzo de mil trescientos catorce, Jacques de Molay, que se había retractado de su confesión, va a la hoguera.")
b("La orden ya no existe. Quedan sus castillos. Y dos reyes de la Península no quieren perderlos.", ideia=True)

# ───────────────────────── 10. LA BULA ─────────────────────────
cap("10. La Bula")
b("La Bula. Aviñón, diez de junio de mil trescientos diecisiete. A petición de Jaime Segundo, el papa Juan Veintidós crea una orden nueva en el reino de Valencia: la de Montesa.", card="AVIÑÓN, 1317")
b("Montesa recibe los bienes del Temple y del Hospital en Valencia. En Aragón y Cataluña, los bienes templarios pasan a los hospitalarios, sus viejos rivales. Monzón también.")
b("Montesa tiene su propio maestre durante casi tres siglos. A fines del siglo dieciséis, Felipe Segundo incorpora ese cargo a la Corona.")
b("Uno de los castillos que recibe Montesa lo habían terminado los templarios justo antes de su caída. Un siglo después, tendrá un huésped que tampoco quiso rendirse.", ideia=True)

# ───────────────────────── 11. LA ROCA ─────────────────────────
cap("11. La Roca")
b("La Roca. Peñíscola, mil cuatrocientos diecisiete. Desde Constanza llega la noticia: un concilio ha depuesto al papa Benedicto Trece. El papa depuesto está aquí, en este castillo.", card="PEÑÍSCOLA, 1417")
b("Se llama Pedro de Luna y es aragonés. En plena división de la Iglesia, con varios papas a la vez, no acepta la sentencia. Se queda en Peñíscola y sigue llamándose papa hasta su muerte, en mil cuatrocientos veintitrés.")
b("El castillo donde resiste lo construyeron los templarios entre mil doscientos noventa y cuatro y mil trescientos siete. Fue de las últimas obras de la orden. Después pasó a Montesa.")
b("Un siglo después de los templarios, otro aragonés resiste en uno de sus castillos. Mientras tanto, en Portugal, otra heredera del Temple prepara barcos.", ideia=True)

# ───────────────────────── 12. LA BANDERA ─────────────────────────
cap("12. La Bandera")
b("La Bandera. Costa de lo que hoy es Brasil, veintiséis de abril de mil quinientos. La flota de Pedro Álvares Cabral celebra su primera misa en tierra brasileña.", card="BRASIL, 1500")
b("El cronista de la flota, Pero Vaz de Caminha, lo cuenta en su carta al rey Manuel: junto al capitán estaba la bandera de Cristo, con la que había salido de Belén, en Lisboa.")
b("Para los historiadores, es la bandera de la Orden de Cristo, la heredera portuguesa del Temple. El rey Dionisio la había creado en mil trescientos diecinueve con los bienes de los templarios de su reino.")
b("Cabral es caballero de esa orden, y la orden había pagado durante décadas las navegaciones portuguesas. Su emblema es una cruz roja con otra blanca en el centro, heredera de la templaria.")
b("Ciento ochenta y ocho años después del fin del Temple, una cruz heredera de los templarios llega a América. Mientras tanto, Monzón, el castillo del niño rey, lleva casi dos siglos en otras manos.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. El Castillo")
b("El Castillo. Monzón había pasado a los hospitalarios, la orden con la que el Temple compartió, en mil ciento treinta y uno, la herencia de un reino.", card="MONZÓN, HOY")
b("En sus muros, la orden protegió a un rey huérfano. Desde fuera, el nieto de ese rey los obligó a rendirse. Y un concilio los declaró inocentes cuando ya no quedaba orden que salvar.")
b("En Francia, el final de los templarios fue una hoguera. En Aragón fue más lento y más frío: un asedio, un juicio y un reparto de castillos.")
b("A los templarios de Aragón no los venció ningún ejército musulmán. Los desarmaron los reyes a quienes habían servido.", ideia=True)
b("Y tú, ¿qué te parece más injusto: la hoguera de París o el asedio de Monzón? Déjalo en los comentarios.")


# ───────────────────────── STORYBOARD (planos por bloco, na ordem dos blocos) ─────────────────────────
SEM = ", no lettering anywhere"      # papéis, placas, capas: o nano-banana inventa texto
VIOL = ", seen from far away, no bodies, no blood"
NOARM = ", no weapons pointed at anyone"
PAPER = "completely blank parchment with no writing, no marks, no letters"
ILEG = "the writing only as faint completely illegible blurred lines, no readable letters"
MAPA = "flat scan of an old printed paper map seen from directly above, muted colors, only coastlines, rivers and terrain shading, completely blank: no labels, no text, no letters, no pins, no markers, no arrows, no table, no frame, no ocean names"
# Personagens (descrição visual fixa; "resembling", nunca foto; sem insígnias inventadas)
TEMPLAR = "a medieval Templar knight-monk with a full dark beard and short hair, bareheaded, wearing a white wool mantle with a red cross pattée on the shoulder over chain mail"
TEMPLARS = "medieval Templar knight-monks with full beards and short hair, bareheaded, in white wool mantles with a red cross pattée over chain mail"
MONZON = "the medieval stone castle of Monzón on top of an isolated rocky hill above the flat plain of the river Cinca in Aragon, a square stone keep and long walls following the rock"
J2 = "a medieval Aragonese king in his forties with a short dark beard, a simple gold circlet and a dark crimson robe, 1308, resembling James II of Aragon"
J1N = "a six-year-old medieval boy with fair reddish hair, a small plain gold circlet and a plain blue wool tunic, 1214"
J1 = "a very tall young medieval king of twenty-one with reddish-blond hair and a short beard, chain mail and a plain dark red surcoat, a simple gold circlet, 1229, resembling James I of Aragon"
MASTER = "an elderly Templar master with a long grey beard, bareheaded, in a white mantle with a red cross pattée, 1214"
RB3 = "a frail elderly medieval count with a grey beard, 1131, resembling Ramon Berenguer III of Barcelona"
ALF = "a battle-hardened medieval king of about sixty with a grey beard, chain mail and a simple iron crown, 1131, resembling Alfonso I of Aragon"
MOLAY = "a gaunt old bearded man of about sixty-five in a worn plain white mantle, 1308, resembling Jacques de Molay"
FRALE = "an Italian woman historian in her thirties with dark hair and glasses, modern clothes, 2001"
LUNA = "a very old thin pope of about ninety with a white beard, white robes and a red cape, 1417, resembling Pope Benedict XIII Pedro de Luna"
CABRAL = "a Portuguese nobleman captain of about thirty-two with a dark beard, a dark velvet doublet and a cape, 1500, resembling Pedro Álvares Cabral"
FELIPE = "a handsome cold medieval French king of about forty with long fair hair, a gold crown and a plain blue robe, 1307, resembling Philip IV of France"
CLEMENT = "an elderly medieval pope with a grey beard in white robes and a papal tiara, 1307, resembling Pope Clement V"
TREB = "a large medieval wooden counterweight trebuchet with a square counterweight box, an A-frame on wooden wheels and a long throwing arm, nothing hanging loose"

SB = [
 # N001 Monzón, mayo de 1309
 [f"monzon_dawn|Wide shot of {MONZON} at dawn in May, mist over the plain, 1309", f"treb_moon|Night scene, {TREB} in black silhouette in the foreground, behind it a huge bright full moon with a pale halo, on the right {MONZON} with one lit window, small campfires between them"],
 # N002 tropas de Jaime II… dentro resisten
 [f"siege_camp|A royal Aragonese siege camp of tents and wooden palisades at the foot of {MONZON}, soldiers around campfires, 1309, seen from far away" + VIOL, f"j2_tent|{J2} standing in a command tent looking up at a castle through the open flap, 1309", f"templar_wall|{TEMPLAR} on the battlements of a stone castle at dusk, looking down at enemy campfires below, 1309"],
 # N003 crió a un niño huérfano
 ["crown_mantle|A small child-size medieval golden crown with four fleurons resting on a neatly folded white wool mantle with part of a red cross pattée visible, on a stone window ledge, warm side light, dark slate background", f"boy_window|{J1N} looking out of a narrow castle window at a wide river plain, seen from behind, 1214", f"boy_templars|{J1N} walking in a castle courtyard between two tall {TEMPLARS}, 1214"],
 # N004 se rinden… Tarragona inocentes… ya no queda orden
 [f"surrender_gate|The gate of a stone castle opening, a few {TEMPLARS} walking out unarmed with their heads bowed toward waiting royal soldiers, 1309, seen from far away" + VIOL, f"charter_seals|A wide medieval parchment charter on a dark wooden table, six large wax seals in ochre and brown hanging from cords along its bottom edge, {ILEG}, candle light", "tarragona_cathedral|The Romanesque-Gothic cathedral of Tarragona on its hill above the Mediterranean at sunset, 1312, no people"],
 # N005 Esta es TODA la historia
 ["case_file|A brown cardboard case folder on a dark desk, a white Templar mantle with a red cross folded on top, a red rubber stamp and an oil lamp" + SEM, "red_stamp|A hand slamming a red rubber stamp onto a brown paper case file, ink splash, dramatic close-up" + SEM],
 # N006 El Voto. Jerusalén 1120, votos ante el patriarca
 ["jerusalem_1120|The walled city of Jerusalem in about 1120 seen from the Mount of Olives at dawn, domes and towers, pilgrims on the road", f"vows_church|A small group of {TEMPLARS} kneeling before a bearded patriarch in rich robes inside a dim stone church lit by candles, 1120", "hugo_payns|A French knight of about fifty with a grey-streaked beard, plain mantle, kneeling with joined hands, 1120, resembling Hugues de Payns@@HUGO DE PAYNS", "vow_hands|Close-up of a knight's rough hands joined between the hands of a bishop, candle light, 1120", "sword_altar|A plain sword laid on a stone altar beside a cross and a candle, 1120", "monk_knight|A bearded knight in chain mail putting on a plain white wool mantle in a stone cell, 1120"],
 # N007 peregrinos, palacio, monte del Templo, templarios
 ["pilgrims_road|Medieval pilgrims with staffs walking on a dusty road through rocky hills of the Holy Land, 1120", f"escort_road|Two mounted {TEMPLARS} escorting a line of pilgrims through a rocky valley, seen from far away, 1120", "king_jerusalem|A medieval king of Jerusalem in a crown and robe gesturing toward a large domed building, 1120, resembling Baldwin II of Jerusalem", "temple_mount|The Temple Mount esplanade in Jerusalem with a large domed mosque building and arcades, 1120, no people", f"stables_vaults|Vast stone vaults under a building with horses and {TEMPLARS} tending them, torchlight, 1120"],
 # N008 Troyes 1129, regla, donaciones
 ["troyes_council|A medieval church council in the cathedral of Troyes, bishops and abbots seated in a semicircle, a knight standing in the center, 1129", "rule_book|A thick closed medieval book with a leather cover and brass clasps lying on a wooden lectern, only the cover and spine visible, no pages visible, no writing", "donation_charter|A medieval nobleman handing a sealed parchment to a kneeling Templar in a castle hall, 1130", "fields_mill|Green fields, a water mill and a small stone farmhouse with a cross over the door, medieval Europe, 1130"],
 # N009 no llega de Francia: llega de Barcelona
 ["barcelona_1131|The walled medieval city of Barcelona by the sea in 1131 seen from a hill, towers, small ships in the harbor", "map_iberia|" + MAPA + ", showing the Iberian Peninsula and southern France"],
 # N010 El Hábito. Barcelona 1131, conde enfermo
 [f"count_bed|{RB3} lying ill in a large bed in a stone chamber, candles, a physician beside him, 1131@@RAMÓN BERENGUER III", "count_palace|A Romanesque stone palace hall in Barcelona with a fireplace and tapestries without any images, 1131, empty", "count_hand|Close-up of an old man's hand with a signet ring resting on a bed blanket, candle light, 1131"],
 # N011 Grañena, ingresa en la orden
 ["granyena_castle|A small medieval stone castle on a bare hill in the dry Segarra countryside of Catalonia, 1131", "frontier_land|Dry rolling fields and a watchtower on a ridge in Catalonia, recently conquered land, 1131", f"habit_bed|{RB3} in bed receiving a folded white mantle with a red cross from {TEMPLAR}, candle light, 1131", "habit_close|Close-up of a folded white wool mantle with a red cross pattée laid on a dark bed blanket, 1131"],
 # N012 no es un caso raro… lecho de muerte
 ["deathbed_noble|A medieval nobleman on his deathbed, a monk with a book at his side, family members in the shadows, 12th century", "monks_procession|A procession of monks in habits carrying candles through a cloister at night, 12th century", "tomb_slab|A plain carved stone tomb slab in the floor of a Romanesque monastery church, a small cross carved on it, no inscription", "ripoll_cloister|The Romanesque cloister of the monastery of Ripoll in Catalonia, columns and arches, soft light, no people"],
 # N013 muere como hermano… otro rey más lejos
 ["count_funeral|Monks and knights around a bier covered with a white cloth with a red cross in a dim Romanesque church, candles, seen from far away, no body visible", "candle_out|A single candle flame going out in a dark stone chamber, smoke rising", f"alf_ride|{ALF} riding at the head of an army through a mountain pass, banners without symbols, 1131"],
 # N014 El Testamento. Bayona 1131, sin hijos, asedia, dicta
 ["bayonne_siege|A medieval army besieging the walled town of Bayonne by a river in autumn 1131, tents and smoke, seen from far away" + VIOL, f"alf_tent|{ALF} seated in a campaign tent dictating to a scribe by lamplight, plain tunic with no cross and no emblems, plain tent without banners, the picture fills the whole frame with no black bars, 1131@@ALFONSO I EL BATALLADOR", "scribe_testament|A medieval scribe writing on a long parchment with a quill by lamplight in a tent, " + ILEG, "seal_testament|Close-up of a wax seal being pressed onto a parchment, 1131" + SEM],
 # N015 tres órdenes… muere 1134… nobles no cumplen
 ["three_orders|Three medieval monks standing side by side in a hall: a Templar in a white mantle with a red cross, a Hospitaller in a black mantle with a white cross, and a canon of the Holy Sepulchre in a white habit with a red double cross, 1131", "testament_close|A long medieval parchment testament with a hanging wax seal on a table, " + ILEG, "fraga_field|An empty battlefield on a dry plain near Fraga at sunset in July 1134, broken lances and abandoned shields, seen from far away" + VIOL, "nobles_assembly|Medieval Aragonese nobles arguing in a stone hall in Jaca, one tearing a parchment, 1134"],
 # N016 Gerona 1143… Monzón sobre una roca… volverá
 ["girona_walls|The walled medieval city of Girona above the river Onyar in November 1143, grey sky", "pact_table|Medieval noblemen and Templars seated at a long table signing a parchment agreement in a vaulted hall, 1143" + SEM, "rb4_portrait|A medieval prince of about thirty with a short beard and a plain circlet, 1143, resembling Ramon Berenguer IV of Barcelona@@RAMÓN BERENGUER IV", f"monzon_day|Wide daytime shot of {MONZON}, the river Cinca shining below, 1143", "keys_handover|A medieval steward handing a large iron ring of castle keys to a Templar at a castle gate, 1143"],
 # N017 Cuatro años después… Castilla
 ["castile_plain|The vast dry plain of La Mancha in Castile with a distant fortress, 1147", "castile_riders|Mounted knights riding south across a dry Castilian plain under a big sky, 1147, seen from far away"],
 # N018 La Plaza. Calatrava 1147
 ["calatrava_fortress|The Muslim fortress of Calatrava la Vieja beside the river Guadiana, towers and walls of reddish earth, 1147", "alfonso7|A medieval king of Castile of about forty with a dark beard and crown, chain mail, 1147, resembling Alfonso VII", f"calatrava_templars|{TEMPLARS} riding into the gate of a reddish-walled fortress by a river, 1147"],
 # N019 llave hacia Toledo, almohades, abandonan
 ["toledo_road|A dusty road winding north across the Castilian plain toward distant hills, 1150s", "almohad_army|A large Almohad army with tents and horsemen on a southern plain, seen from far away, 1157" + VIOL, "templars_leave|A column of mounted Templars in white mantles leaving a fortress at dusk, seen from behind, 1157", "empty_fortress|The empty courtyard of a reddish-walled fortress, gate open, wind blowing dust, 1157"],
 # N020 Sancho III 1158, Raimundo de Fitero, Orden de Calatrava
 ["sancho3|A young medieval king of Castile of about twenty-four with a light beard and crown on a throne, 1158, resembling Sancho III, two guards in simple chain mail coifs and plain open helmets beside the throne, no plate armor, no heraldic beasts", "fitero_abbot|A Cistercian abbot of about fifty in a white habit, tonsured, kneeling before a young king in a hall, 1158, resembling Raymond of Fitero@@RAIMUNDO DE FITERO", "cistercian_monks|Cistercian monks in white habits putting on chain mail in a monastery courtyard, 1158", "calatrava_order|Knights in white habits with a plain cross riding out of a reddish fortress by a river, 1158", "almazan|The walled medieval town of Almazán in Castile on a winter day, 1158"],
 # N021 En Castilla perdió… Monzón sigue en pie
 ["monzon_dusk|Wide shot of {MONZON} at dusk with lit windows, 1160".replace("{MONZON}", MONZON), "calatrava_fortress#médio-dir", "crown_mantle#detalhe-centro"],
 # N022 El Niño. Muret 1213
 ["muret_field|An empty medieval battlefield near Muret in southern France in September 1213, broken banners without symbols in the grass, morning fog, seen from far away" + VIOL, "pedro2|A medieval king of Aragon of about thirty-five with a dark beard and crown in chain mail, 1213, resembling Peter II of Aragon", "rome_1213|Rome in 1213, ancient ruins and medieval church towers along the Tiber at dusk", "black_veil|A black mourning veil laid on a carved wooden chest in a dim chamber, 1213"],
 # N023 Jaime 5 años, Montfort, Inocencio III
 [f"boy_alone|{J1N} sitting alone on a bench in a large stone hall, guards at the door, 1213", "montfort|A grim medieval French lord of about fifty with a grey beard in chain mail and a dark surcoat, 1213, resembling Simon de Montfort@@SIMÓN DE MONTFORT", "innocent3|A medieval pope of about fifty in white robes and a tiara writing at a desk in the Lateran palace, 1214, resembling Pope Innocent III", "papal_letter|A papal letter with a hanging lead seal on a cord, " + ILEG],
 # N024 Montfort lo tenía desde 1211… entrega a un enviado
 ["carcassonne|The walled medieval city of Carcassonne on its hill, 1214", f"boy_handover|{J1N} holding the hand of a cardinal legate in red robes, walking away from a castle gate, French soldiers watching, 1214", "legate_road|A small mounted escort with a cardinal in red and a child on a horse riding across the Pyrenees foothills, 1214"],
 # N025 1214 llega a Monzón, Guillem de Montredón
 [f"boy_arrives|{J1N} on horseback arriving at the gate of {MONZON}, {TEMPLARS} waiting, 1214", f"master_boy|{MASTER} kneeling to greet {J1N} in a castle courtyard, 1214@@GUILLEM DE MONTREDÓN", "monzon_courtyard|The inner courtyard of a Romanesque Templar castle with a chapel and a well, 1214"],
 # N026 crónica, dos años y medio, sale 1217 con nueve años
 ["chronicle_book|A medieval chronicle manuscript open on a lectern with a small illuminated picture of a castle on the page, " + ILEG, f"boy_lessons|{J1N} learning to read with {MASTER} at a table in a castle room, candle light, 1215", f"boy_sword|{J1N} practicing with a small wooden sword in a castle courtyard while {TEMPLAR} watches, 1216", f"boy_leaves|A nine-year-old boy with reddish hair on horseback leaving {MONZON} with an escort, 1217"],
 # N027 ha criado a un rey… en el mar
 ["crown_mantle#médio-esq", "mediterranean_sea|The Mediterranean Sea at dawn with a fleet of medieval sailing ships, 1229"],
 # N028 La Isla. Santa Ponsa 1229
 ["fleet_storm|A medieval fleet of galleys and sailing ships in a stormy sea, 1229", f"j1_landing|{J1} wading ashore from a round-hulled medieval wooden ship with a triangular lateen sail and a flat rounded bow, no raised carved prow, no dragon head, onto a rocky beach of Mallorca with soldiers, no numbers or digits anywhere@@JAIME I", "santa_ponsa|A rocky cove with pine trees on the coast of Mallorca, ships anchored, 1229"],
 # N029 templarios con él, cae Mallorca 31/12, tierras
 [f"templars_landing|{TEMPLARS} landing horses from a ship onto a beach, 1229", "palma_siege|The walled Muslim city of Madina Mayurqa (Palma) under siege, siege towers and tents, seen from far away, December 1229" + VIOL, "palma_gate|Christian knights entering through a breached city gate at dawn, seen from far away, 31 December 1229" + VIOL, "mallorca_fields|Olive groves and stone farmhouses in the countryside of Mallorca, 1230"],
 # N030 crónica: tormenta, desembarco, meses de asedio
 ["chronicle_book#detalhe-alto", "fleet_storm#médio-dir", "siege_winter|A medieval siege camp in winter rain before city walls, soldiers huddled by fires, 1229" + VIOL],
 # N031 Valencia 1238, Jaime el Conquistador
 ["valencia_1238|The walled city of Valencia with its minarets and the river Turia, a Christian army outside, 1238, seen from far away", f"j1_entry|{J1} riding into a city through a gate followed by knights and {TEMPLARS}, 1238", "j1_older|A tall medieval king of about thirty with reddish-blond hair and beard, crown and plain red surcoat, standing on a wall overlooking the sea, 1238, resembling James I of Aragon", "valencia_huerta|The green irrigated huerta of Valencia with orange trees and water channels, 1240"],
 # N032 pieza del reino… noticias de París
 ["aragon_castles|A line of Templar castles on hilltops across the dry landscape of Aragon, seen from far away, 1300", "messenger|A royal messenger on a lathered horse galloping toward a castle at dusk, 1307"],
 # N033 La Orden. 1/12/1307, Jaime II firma
 [f"j2_sign|{J2} signing a parchment order at a desk in a palace room, an official waiting, 1307" + SEM, "royal_order|A royal parchment order with a hanging wax seal on a desk, " + ILEG, f"j2_portrait|{J2} in portrait, serious face, in a stone palace hall, 1307@@JAIME II", "zaragoza_palace|The Aljafería palace of Zaragoza with its towers in winter, 1307"],
 # N034 inquisidor y obispos; oficiales salen
 ["inquisitor|A Dominican friar in a black and white habit reading a document by candlelight, 1307" + SEM, "bishops|Two medieval bishops in mitres conferring in a cloister, 1307", "officials_ride|Royal officials on horseback leaving a city gate on a winter road, 1307", "commandery_door|Royal officials knocking at the door of a small rural Templar house with a cross over the door, 1307"],
 # N035 Francia arresta… acusados de herejía
 ["paris_1307|Paris in October 1307 at dawn, the towers of the Templar fortress in the Marais, mist", f"felipe|{FELIPE} on a throne, cold expression, 1307", f"arrest_dawn|Royal French soldiers leading {TEMPLARS} out of a building at dawn, seen from far away, 1307" + VIOL + NOARM, "accusation|A royal French document with a seal on a table beside a crucifix, " + ILEG, "cell_templar|A Templar in a torn white mantle sitting in a dark prison cell, head down, 1307"],
 # N036 Clemente V protestó, 22/11 cedió; Acre 1291
 [f"clement|{CLEMENT} reading a letter with an angry face in a palace room, 1307", "papal_bull|A papal bull with a hanging lead seal being handed to a messenger, 1307, " + ILEG, "acre_1291|The coastal city of Acre with smoke rising from its walls by the sea, May 1291, seen from far away" + VIOL, "acre_ships|Ships leaving a burning coastal city at dusk, refugees on board, 1291, seen from far away" + VIOL, "map_holyland|" + MAPA + ", showing the eastern Mediterranean coast"],
 # N037 se encierran en sus castillos
 [f"gates_close|{TEMPLARS} closing the heavy wooden gates of a castle, 1307", f"templars_walls|{TEMPLARS} carrying supplies up stone stairs onto castle walls, 1307", "miravet_castle|The medieval castle of Miravet on a rocky hill above the river Ebro in Catalonia, 1307"],
 # N038 CTA + volvemos a Monzón
 ["case_file#médio-dir", "monzon_dawn#detalhe-centro", "treb_moon#médio-esq"],
 # N039 El Asedio. Monzón fines 1308
 ["siege_lines|Royal Aragonese troops digging siege lines and setting up tents around a rocky hill crowned by a castle, late autumn 1308, seen from far away", "siege_camp#médio-dir", f"templar_watch|{TEMPLAR} keeping watch on a castle tower at night, a brazier beside him, 1308", "crown_mantle#detalhe-baixo"],
 # N040 Miravet 22 hombres, 10 meses, 12/12, seis
 ["miravet_castle#médio-dir", "miravet_siege|Royal troops camped by the river Ebro below the castle of Miravet, boats on the river, seen from far away, 1308", "saguardia|A Catalan Templar commander of about fifty with a grey beard in a white mantle, standing firm in a castle hall, 1308", "six_templars|Six Templars in white mantles standing together in a castle hall facing royal envoys, 1308", "miravet_surrender|Royal officials receiving keys at the gate of a castle above a river in winter, 1308"],
 # N041 pasa el invierno… mayo 1309 se rinden
 ["monzon_snow|{MONZON} in winter with snow on the plain and smoke from siege fires, 1309".replace("{MONZON}", MONZON), "treb_moon#detalhe-alto", "surrender_gate#médio-dir"],
 # N042 salen prisioneros… decide la Iglesia
 [f"prisoners_road|{TEMPLARS} walking in a line on a road escorted by royal soldiers, unchained, spring 1309, seen from far away", "bishop_court|A medieval ecclesiastical court with bishops seated at a long table, 1309", "case_file#detalhe-centro"],
 # N043 Chinon 1308, cardenales, Molay
 ["chinon_castle|The royal castle of Chinon on its ridge above the river Vienne in August 1308", "three_cardinals|Three cardinals in red robes seated at a table in a stone tower room, a notary writing, 1308", f"molay_cell|{MOLAY} standing before three cardinals in a stone room, 1308@@JACQUES DE MOLAY", "notary|A medieval notary writing on a long parchment roll, " + ILEG, f"molay_face|Close-up of {MOLAY}, tired eyes, 1308"],
 # N044 Frale 2001, absuelven si piden perdón, no la hace pública
 ["vatican_archive|Endless shelves of old bound volumes and parchment boxes in the Vatican Apostolic Archive, warm light, no people", f"frale|{FRALE} seen from behind examining an old document with gloved hands at an archive table, the document edge-on and blank, no writing visible, 2001@@BARBARA FRALE", "chinon_parchment|A long medieval parchment roll unrolled on a table with a small hanging seal, " + ILEG, "pope_secret|A medieval pope placing a parchment into a wooden chest, 1308", "archive_box|A wooden archive chest being closed in a dim archive room, 1308"],
 # N045 Salamanca 1310; Portugal no los encarcela
 ["salamanca|The Romanesque old cathedral of Salamanca in October 1310", "salamanca_council|Medieval bishops in a council hall voting by raising their hands, 1310", "dinis|A medieval king of Portugal of about fifty with a grey beard and a crown, 1310, resembling King Denis of Portugal", "tomar_castle|The Templar castle of Tomar on its hill in Portugal, 1310"],
 # N046 22/03/1312 bula, Vienne, no dice culpable
 [f"clement_sign|{CLEMENT} signing a document at a desk, seen from the side, the page hidden by his hand and blank, no writing visible, 1312", "vienne_council|The council of Vienne in a great cathedral, hundreds of bishops in mitres seated in rows, 1312", "vienne_cathedral|The Gothic cathedral of Vienne by the river Rhône in spring 1312", "papal_bull#detalhe-centro"],
 # N047 Tarragona 4/11/1312 inocentes, pensión
 ["tarragona_cathedral#médio-dir", "tarragona_council|Bishops in mitres seated in the chapter house of Tarragona cathedral hearing Templars standing before them, 1312", "charter_seals#médio-esq", "old_templar|An old former Templar in a plain brown robe sitting in the sun in a monastery courtyard, 1320", "templar_house|A small Templar house with a garden and a chapel in the Catalan countryside, 1320"],
 # N048 Molay hoguera 1314
 ["notre_dame|The Île de la Cité in Paris at dusk in March 1314, the twin towers of a medieval cathedral complete with no scaffolding, a thin column of smoke rising from the island, seen from far across the river, no people visible, no signature", "smoke_seine|A column of grey smoke rising above the river Seine at dusk, seen from far away, no figures", f"molay_face#médio-dir"],
 # N049 la orden ya no existe; castillos
 ["aragon_castles#médio-esq", "empty_hall|An empty Templar castle hall with a cold fireplace and a white mantle hanging on a peg, dusty light, 1312", f"j2_portrait#detalhe-centro"],
 # N050 La Bula. Aviñón 1317, Juan XXII, Montesa
 ["avignon|The papal palace of Avignon above the river Rhône, 1317", "john22|A small elderly pope of about seventy in white robes at a desk in Avignon, 1317, resembling Pope John XXII", "montesa_castle|The medieval castle of Montesa on a rocky hill in Valencia, 1317", "montesa_knights|Knights in white habits with a plain red cross receiving a parchment from a bishop, 1319"],
 # N051 bienes Temple y Hospital; hospitalarios; Monzón también
 ["hospitallers|Medieval Hospitaller knights in black mantles with a white cross taking possession of a castle gate, 1317", "monzon_day#médio-dir", "keys_handover#detalhe-centro", "map_iberia#médio-esq"],
 # N052 casi tres siglos; Felipe II incorpora
 ["felipe2|An austere Spanish king of about sixty with a grey beard in black clothes, 1587, resembling Philip II of Spain", "escorial|The monastery-palace of El Escorial with mountains behind, 1587", "montesa_castle#detalhe-alto"],
 # N053 castillo terminado antes de su caída; huésped
 ["peniscola|The castle of Peñíscola on a rocky peninsula almost surrounded by the sea, 1310", "peniscola_build|Medieval masons and Templars building thick stone walls of a castle by the sea, 1300", "peniscola_night|The castle of Peñíscola at night with one lit window, waves below"],
 # N054 La Roca. Peñíscola 1417, Constanza depone a Benedicto XIII
 ["constance|The council of Constance in a great hall, bishops and cardinals seated in rows, 1417", "messenger_sea|A messenger with a sealed letter climbing steps toward a castle on a rock by the sea, 1417", f"luna_window|{LUNA} standing at a castle window looking at the sea, 1417", "letter_seal|A sealed letter with a broken wax seal on a table by a window, " + ILEG],
 # N055 Pedro de Luna, aragonés, varios papas, no acepta, 1423
 [f"luna_portrait|{LUNA} in portrait, stubborn face, 1417@@BENEDICTO XIII", "three_popes|Three empty papal thrones in a dim hall, symbolizing a divided Church, 1410", f"luna_desk|{LUNA} writing at a desk in a castle room, 1420", "peniscola_storm|The castle of Peñíscola under a stormy sky, waves crashing, 1423", "luna_chapel|A small castle chapel with a single candle and an empty papal chair, 1423"],
 # N056 construido por templarios 1294–1307; Montesa
 ["peniscola_build#médio-dir", "peniscola_sea|The castle of Peñíscola seen from a boat at sea, walls rising from the rock, calm water, morning light", "templar_mason|A Templar in a white mantle overseeing masons on scaffolding, 1300", "montesa_knights#detalhe-centro"],
 # N057 otro aragonés resiste… Portugal prepara barcos
 ["peniscola_night#detalhe-alto", "lisbon_shipyard|A Portuguese shipyard on the Tagus with caravels being built, 15th century", "caravel_sail|A caravel with a large white sail bearing a red cross with a white inner cross, at sea, 1500"],
 # N058 La Bandera. Brasil 26/04/1500, primera misa
 ["brazil_coast|The tropical coast of Brazil with a long beach, palm trees and green hills, a fleet of caravels anchored offshore, April 1500", "first_mass|Portuguese sailors and a friar celebrating Mass at a wooden altar on a tropical beach, indigenous people watching from the trees, 1500", "cross_beach|A large wooden cross planted on a tropical beach at sunset, 1500", f"cabral|{CABRAL} standing on the beach beside a banner, 1500@@PEDRO ÁLVARES CABRAL"],
 # N059 Caminha, carta al rey Manuel, bandera de Cristo, Belén
 [f"caminha|A middle-aged Portuguese scribe writing a long letter with a quill at a table in a ship's cabin, 1500, " + ILEG + "@@PERO VAZ DE CAMINHA", "banner_beach|A white banner with a red cross bearing a white inner cross held on a pole on a tropical beach, 1500", "belem_tower|The Tagus riverside at Belém, Lisbon, with ships departing, 1500", "manuel1|A Portuguese king of about thirty with a dark beard reading a letter on a throne, 1500, resembling King Manuel I"],
 # N060 Orden de Cristo, Dionisio 1319
 ["dinis#médio-dir", "tomar_convent|The round church of the Convent of Christ in Tomar, Portugal", "christ_knights|Portuguese knights in white mantles with a red cross with a white inner cross kneeling in a round church, 1320", "caravel_sail#detalhe-centro", "tomar_castle#médio-esq"],
 # N061 Cabral caballero; pagó navegaciones; cruz roja con blanca
 ["cabral#detalhe-centro", "navigators|Portuguese navigators studying a large map on a table with astrolabes, 15th century" + SEM, "map_atlantic|" + MAPA + ", showing the Atlantic Ocean between Portugal, Africa and Brazil", "cross_detail|Close-up of a red cross pattée with a white inner cross painted on a weathered wooden ship's sail, 1500"],
 # N062 188 años; Monzón dos siglos en otras manos
 ["caravel_sail#médio-esq", "brazil_coast#detalhe-centro", "monzon_dusk#médio-esq", "hospitallers#detalhe-centro"],
 # N063 El Castillo. Monzón hospitalarios
 ["monzon_today|The castle of Monzón on its rock above the town today at sunset, quiet streets below", "hospitaller_banner|A black banner with a white cross flying over a stone castle tower, 1320", "three_orders#detalhe-centro", "testament_close#detalhe-baixo"],
 # N064 rey huérfano; nieto; concilio
 ["crown_mantle#aberto", "j2_tent#médio-dir", "charter_seals#detalhe-centro", "boy_window#detalhe-centro"],
 # N065 Francia hoguera; Aragón asedio, juicio, reparto
 ["smoke_seine#médio-dir", "treb_moon#aberto", "tarragona_council#detalhe-centro", "keys_handover#médio-esq"],
 # N066 no los venció ningún ejército musulmán
 ["empty_hall#detalhe-centro", "monzon_today#detalhe-alto", "habit_close#médio-dir"],
 # N067 Y tú, ¿qué te parece más injusto?
 ["typewriter_end|A typewriter with a blank sheet on a dark desk beside a white mantle with a red cross, a lamp switching off" + SEM, "folder_close|A hand closing a thick brown case file with a red circular stamp on a dark desk, lamp light" + SEM, "monzon_dawn#aberto"],
]
_textos = [x for x in B if "t" in x]
assert len(SB) == len(_textos), f"SB {len(SB)} x blocos {len(_textos)}"
for _blk, _s in zip(_textos, SB): _blk["s"] = _s

# Thumbs (EMBALAGEM.md aprovado no crivo r3): texto (sigla, sellos, TARRAGONA, ¿HEREJES?, aba) no Thumbnail.jsx.
THUMBS = [
    {"id": "thumb-A", "prompt": "Ink graphic novel illustration: a small child-size medieval golden crown, simple narrow band with four fleurons, resting on a neatly folded white wool mantle with part of a red cross pattée visible beneath it, the mantle partly in shadow, on a stone window ledge, warm side light from a castle window, the crown and mantle occupy the LEFT 55 percent of the frame, plain dark slate-blue background, RIGHT half empty dark background, no people, no knight, no helmet, no sword, no lettering, no hex codes"},
    {"id": "thumb-B", "prompt": "Ink graphic novel illustration: a wide medieval parchment charter lying on a dark wooden table that fills at least a third of the frame, slightly in perspective, six large round wax seals in ochre and brown hanging in a row from cords along its bottom edge, the writing on the parchment only as faint completely illegible blurred lines, warm candle light from the left, no red color, no readable letters, no people, no hex codes"},
    {"id": "thumb-C", "prompt": "Ink graphic novel illustration: night scene, a large medieval wooden counterweight trebuchet in black silhouette in the left foreground, clearly showing its square counterweight box, A-frame on wooden wheels and the long throwing arm lowered and pointing up to the right at an angle with absolutely nothing hanging from it, no rope, no sling, no cords, no chains, directly behind it a huge bright full moon with a wide pale halo making the sky behind the machine the brightest area of the image, behind on the right a stone castle with a keep on an isolated rocky hill with one lit yellow window, a low line of small campfires between them, slate-blue night sky darkening toward the edges, no orange, no people, no noose, no flags, no symbols, no lettering, no hex codes, lower right ground dark and empty"},
]
# a 1ª prova do 001 (04/11) saiu com moldura de papel: todo prompt leva sangria explícita
SANGRIA = ", full-bleed illustration filling the entire frame edge to edge, no border, no margin, no white frame, no panel outline"
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
        blocos.append({"id": bid, "texto": blk["t"], "ideia": blk["ideia"]})
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
        if not specs:   # roteiro antes do storyboard: bloco ainda sem planos
            avisos.append(f"{bid}: sem planos"); prompts.setdefault("_tbd", "TBD"); specs = [("_tbd", None, None)]
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
                cenas.append({"id": ids[k], "prompt": prompts[k] + SANGRIA})
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
        if cap_atual == "Hook" and t + d > HOOK_MAX: avisos.append(f"{bid}: hook passa de {HOOK_MAX:.0f}s ({fmt(t + d)})")
        t += d

    total = t
    cenas.extend({"id": t["id"], "prompt": t["prompt"] + SANGRIA} for t in THUMBS)
    reuso = [p for p in planos if not p["nova"]]
    apos = [p for p in planos if p["ini"] >= INEDITO_ATE]
    reuso_apos = [p for p in apos if not p["nova"]]
    words = sum(len(limpo(b_["texto"]).split()) for b_ in blocos)
    stats = {"palavras": words, "duracao_s": round(total), "planos": len(planos),
             "imagens_video": len(ids), "imagens_total": len(cenas),
             "reuso_pct": round(100 * len(reuso) / len(planos), 1),
             "reuso_pct_apos_3min": round(100 * len(reuso_apos) / max(1, len(apos)), 1),
             "plano_medio_s": round(total / len(planos), 2),
             "cortes_1o_min": sum(1 for p in planos if p["ini"] < 60), "rotulos": sum(1 for p in planos if p["rot"]),
             "capitulos": sum(1 for x in B if "cap" in x and x["cap"][0].isdigit()), "avisos": avisos}

    (out / "blocos.json").write_text(json.dumps(blocos, ensure_ascii=False, indent=1) + "\n")
    (out / "cenas.json").write_text(json.dumps(cenas, ensure_ascii=False, indent=1) + "\n")
    (out / "storyboard.json").write_text(json.dumps({"stats": stats, "planos": planos}, ensure_ascii=False, indent=1) + "\n")
    (out / "SCRIPT.md").write_text(
        f"# {TITULO} en {round(total / 60)} minutos: roteiro\n\n"
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
