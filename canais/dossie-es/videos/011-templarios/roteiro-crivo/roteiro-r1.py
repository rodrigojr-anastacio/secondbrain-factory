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
b("El Voto. Jerusalén, hacia mil ciento veinte. Un caballero de Champaña, Hugo de Payns, y unos pocos compañeros juran algo nuevo: vivir como monjes y pelear como soldados.", card="JERUSALÉN, 1120")
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
b("Deja sus reinos, Aragón y Pamplona, a tres órdenes religiosas: el Santo Sepulcro, los hospitalarios y los templarios. Unos monjes soldados, herederos de un reino.")
b("Por qué lo hizo, nadie lo sabe con certeza. Según los historiadores, quizá quería que su guerra contra los musulmanes siguiera. O tal vez sabía que los nobles nunca lo aceptarían.")
b("En mil ciento treinta y cuatro, Alfonso es derrotado en Fraga y muere semanas después. Los nobles no cumplen el testamento. En Aragón eligen rey a su hermano Ramiro, que era monje.")
b("Las órdenes se quedan sin reino. Pero el Temple no renuncia a cambio de nada.", ideia=True)

# ───────────────────────── 4. LA ENCOMIENDA ─────────────────────────
cap("4. La Encomienda")
b("La Encomienda. Gerona, noviembre de mil ciento cuarenta y tres. Para cerrar el asunto del testamento, Ramón Berenguer Cuarto, que ahora gobierna Aragón, pacta con el Temple.", card="GERONA, 1143")
b("La orden renuncia a su parte del reino. A cambio recibe castillos, entre ellos Monzón, sobre una roca junto al río Cinca, y la quinta parte de lo que se conquiste a los musulmanes.")
b("Monzón se convierte en una de sus casas más ricas, lo que la orden llama una encomienda. Desde allí, los hermanos del Temple administran aldeas, molinos y rentas de toda la comarca.")
b("Con el tiempo, la orden funcionará también como un banco: guardará dinero, prestará a reyes y dará cartas de crédito a los peregrinos. El rey de Francia llegará a guardar su tesoro en la casa del Temple en París.")
b("Cuatro años después del pacto de Gerona, el Temple recibe otra fortaleza. Esta vez, en Castilla.", ideia=True)

# ───────────────────────── 5. LA PLAZA ─────────────────────────
cap("5. La Plaza")
b("La Plaza. Calatrava, mil ciento cuarenta y siete. El rey Alfonso Séptimo conquista esta fortaleza junto al río Guadiana y la entrega a los templarios.", card="CALATRAVA, 1147")
b("Es la llave del camino hacia Toledo. Diez años después, los almohades avanzan desde el sur. A fines de mil ciento cincuenta y siete, los templarios abandonan la plaza.")
b("En enero de mil ciento cincuenta y ocho, el rey Sancho Tercero se la ofrece a quien quiera defenderla. La acepta un abad cisterciense, Raimundo de Fitero. De ahí nace otra orden: la de Calatrava.")
b("En Castilla, el Temple perdió una plaza. En Aragón, Monzón sigue en pie. Y allí le van a confiar algo más valioso que un castillo.", ideia=True)

# ───────────────────────── 6. EL NIÑO ─────────────────────────
cap("6. El Niño")
b("El Niño. Muret, Francia, doce de septiembre de mil doscientos trece. El rey Pedro Segundo de Aragón muere en batalla. Su esposa había muerto en Roma ese mismo año.", card="MURET, 1213")
b("Su único hijo, Jaime, tiene cinco años y está en manos del enemigo de su padre, Simón de Montfort. El papa Inocencio Tercero ordena que lo devuelvan.")
b("Montfort lo tenía desde mil doscientos once, prometido a una de sus hijas. Ahora obedece al papa y entrega al niño a un enviado de Roma.")
b("En mil doscientos catorce, el niño rey llega a Monzón. Lo custodia el maestre del Temple en Aragón y Cataluña, Guillem de Montredón.", card="MONZÓN, 1214")
b("Años después, el propio Jaime lo cuenta en su crónica: el maestre lo llevó a Monzón y allí estuvo dos años y medio. Sale en mil doscientos diecisiete, con nueve años.")
b("La orden ha criado a un rey. Y ese rey va a necesitarla en el mar.", ideia=True)

# ───────────────────────── 7. LA ISLA ─────────────────────────
cap("7. La Isla")
b("La Isla. Santa Ponsa, Mallorca, septiembre de mil doscientos veintinueve. Jaime ya tiene veintiún años y desembarca para conquistar la isla.", card="MALLORCA, 1229")

b("Entre sus tropas van los templarios. El treinta y uno de diciembre cae la ciudad de Mallorca, la actual Palma. La orden recibe tierras en la isla por su ayuda.")
b("En su crónica, Jaime recuerda esa campaña con detalle: la tormenta en la travesía, el desembarco y los meses de asedio frente a la ciudad.")
b("Nueve años después, en mil doscientos treinta y ocho, Jaime entra en Valencia. Otra vez el Temple está a su lado. Ese rey pasará a la historia como Jaime el Conquistador.")
b("Para entonces, los templarios de Aragón son una pieza del reino. Pero la orden nació para otra guerra. Y esa guerra está a punto de perderse.", ideia=True)

# ───────────────────────── 8. LA ORDEN ─────────────────────────
cap("8. La Orden")
b("La Orden. Acre, mayo de mil doscientos noventa y uno. Cae la última gran ciudad cristiana de Tierra Santa. La orden se queda sin la misión que le dio origen.", card="ACRE, 1291")
b("Dieciséis años después, el trece de octubre de mil trescientos siete, el rey Felipe Cuarto de Francia hace arrestar a los templarios de su reino.", card="PARÍS, 1307")
b("La orden de arresto los acusa de herejía: de renegar de Cristo y escupir sobre la cruz. Muchos confiesan bajo tortura. El papa Clemente Quinto no había autorizado nada de esto.")
b("Al principio protesta. Pero el veintidós de noviembre cede: con una bula, ordena arrestar a los templarios en toda la cristiandad.")
b("En Aragón gobierna Jaime Segundo, nieto del niño de Monzón. Han pasado siete semanas desde los arrestos de París. El uno de diciembre de mil trescientos siete firma su propia orden: detener a los templarios de sus reinos.", card="ARAGÓN, 1307")
b("Los templarios aragoneses hacen algo que casi nadie hizo en Francia. Se encierran en sus castillos.", ideia=True)
b("Si este expediente te está gustando, suscríbete: así no te pierdes el próximo. Y ahora, al asedio.")

# ───────────────────────── 9. EL ASEDIO ─────────────────────────
cap("9. El Asedio")
b("El Asedio. Miravet, sobre el río Ebro. La defensa la dirige Ramón de Saguardia, lugarteniente del maestre en Cataluña, con veintidós hombres. Resisten unos diez meses. Se rinden el doce de diciembre de mil trescientos ocho.", card="MIRAVET, 1308")
b("Según los documentos de la época, seis de ellos, con el propio Saguardia, se niegan hasta el final a entregarse por su voluntad.")
b("Entre los últimos, Monzón y Chalamera. Monzón es la fortaleza donde la orden custodió a Jaime el Conquistador. Ahora la cercan las tropas de su nieto.", card="MONZÓN, 1309")
b("Los templarios aguantan todo el invierno. Nadie viene a ayudarlos. En mayo de mil trescientos nueve, Monzón y Chalamera se rinden.")
b("Los últimos templarios en armas del reino salen como prisioneros. Su destino ya no lo decide el rey de Aragón: lo decide la Iglesia.", ideia=True)

# ───────────────────────── 10. EL CONCILIO ─────────────────────────
cap("10. El Concilio")
b("El Concilio. Mientras tanto, en agosto de mil trescientos ocho, en el castillo de Chinon, tres cardenales del papa interrogan al gran maestre, Jacques de Molay, y a otros jefes de la orden.", card="CHINON, 1308")
b("Según la historiadora Barbara Frale, que redescubrió el pergamino en el Archivo Apostólico Vaticano en dos mil uno, los cardenales los absuelven si piden perdón. No es una absolución de la orden. Y el papa no la hace pública.")
b("En Castilla, el concilio de Salamanca de mil trescientos diez declara inocentes a los templarios del reino. En Portugal, el rey Dionisio toma sus bienes, pero no los encarcela.")
b("El veintidós de marzo de mil trescientos doce, el papa firma la bula que disuelve la orden y la anuncia en el concilio de Vienne. No dice que sea culpable: dice que ya no puede seguir.")

b("Siete meses después, el cuatro de noviembre de mil trescientos doce, el concilio de Tarragona juzga a los templarios de la Corona de Aragón. Los declara inocentes. Según los historiadores, reciben una pensión y viven el resto de su vida en antiguas casas de la orden.", card="TARRAGONA, 1312")
b("En París, en marzo de mil trescientos catorce, Jacques de Molay, que se había retractado de su confesión, va a la hoguera. Lo de la maldición contra el rey y el papa es leyenda.")
b("La orden ya no existe. Quedan sus castillos. Y dos reyes de la Península no quieren perderlos.", ideia=True)

# ───────────────────────── 11. LA BULA ─────────────────────────
cap("11. La Bula")
b("La Bula. Aviñón, diez de junio de mil trescientos diecisiete. A petición de Jaime Segundo, el papa Juan Veintidós crea una orden nueva en el reino de Valencia: la de Montesa.", card="AVIÑÓN, 1317")
b("Montesa recibe los bienes del Temple y del Hospital en Valencia, con castillos como Peñíscola. En Aragón y Cataluña, los bienes templarios pasan a los hospitalarios, sus viejos rivales.")
b("Montesa tiene su propio maestre durante casi tres siglos. A fines del siglo dieciséis, Felipe Segundo incorpora ese cargo a la Corona.")
b("En Portugal, el rey Dionisio hace lo mismo. En mil trescientos diecinueve nace la Orden de Cristo, que hereda los bienes del Temple. Con los años, tendrá su sede en Tomar.")
b("Su emblema es una cruz roja con otra blanca en el centro, heredera de la templaria. Pronto esa cruz va a cruzar el océano.", ideia=True)

# ───────────────────────── 12. LA BANDERA ─────────────────────────
cap("12. La Bandera")
b("La Bandera. Costa de lo que hoy es Brasil, veintiséis de abril de mil quinientos. La flota de Pedro Álvares Cabral celebra su primera misa en tierra brasileña.", card="BRASIL, 1500")
b("El cronista de la flota, Pero Vaz de Caminha, lo cuenta en su carta al rey Manuel: junto al capitán estaba la bandera de Cristo, con la que había salido de Belén, en Lisboa.")
b("Para los historiadores, es la bandera de la Orden de Cristo. Cabral es caballero de esa orden, y la orden había pagado durante décadas las navegaciones portuguesas.")
b("Ciento ochenta y ocho años después del fin del Temple, una cruz heredera de los templarios llega a América. Mientras tanto, Monzón, el castillo del niño rey, lleva casi dos siglos en otras manos.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. El Castillo")
b("El Castillo. Monzón había pasado a los hospitalarios, la orden con la que el Temple compartió, en mil ciento treinta y uno, la herencia de un reino.", card="MONZÓN, HOY")
b("En sus muros, la orden protegió a un rey huérfano. Desde fuera, el nieto de ese rey los obligó a rendirse. Y un concilio los absolvió cuando ya no quedaba orden que salvar.")
b("En Francia, el final de los templarios fue una hoguera. En Aragón fue más lento y más frío: un asedio, un juicio y un reparto de castillos.")
b("A los templarios de Aragón no los venció ningún ejército musulmán. Los desarmaron los reyes a quienes habían servido.", ideia=True)
b("Y tú, ¿qué te parece más injusto: la hoguera de París o el asedio de Monzón? Déjalo en los comentarios.")

# Thumbs (EMBALAGEM.md aprovado no crivo r3): texto (sigla, sellos, TARRAGONA, ¿HEREJES?, aba) no Thumbnail.jsx.
THUMBS = [
    {"id": "thumb-A", "prompt": "Ink graphic novel illustration: a small child-size medieval golden crown, simple narrow band with four fleurons, resting on a neatly folded white wool mantle with part of a red cross pattée visible beneath it, the mantle partly in shadow, on a stone window ledge, warm side light from a castle window, the crown and mantle occupy the LEFT 55 percent of the frame, plain dark slate-blue background, RIGHT half empty dark background, no people, no knight, no helmet, no sword, no lettering, no hex codes"},
    {"id": "thumb-B", "prompt": "Ink graphic novel illustration: a wide medieval parchment charter lying on a dark wooden table that fills at least a third of the frame, slightly in perspective, six large round wax seals in ochre and brown hanging in a row from cords along its bottom edge, the writing on the parchment only as faint completely illegible blurred lines, warm candle light from the left, no red color, no readable letters, no people, no hex codes"},
    {"id": "thumb-C", "prompt": "Ink graphic novel illustration: night scene, a large medieval wooden counterweight trebuchet in black silhouette in the left foreground, clearly showing its square counterweight box, A-frame on wooden wheels and long throwing arm tilted back, the sling folded against the arm, nothing hanging loose, directly behind it a huge bright full moon with a wide pale halo making the sky behind the machine the brightest area of the image, behind on the right a stone castle with a keep on an isolated rocky hill with one lit yellow window, a low line of small campfires between them, slate-blue night sky darkening toward the edges, no orange, no people, no rope, no noose, no flags, no symbols, no lettering, no hex codes, lower right ground dark and empty"},
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
