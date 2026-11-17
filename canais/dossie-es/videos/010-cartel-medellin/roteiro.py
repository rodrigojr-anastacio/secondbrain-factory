#!/usr/bin/env python3
"""Fonte única do dossie-es 010 (El Cártel de Medellín): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (na pasta do vídeo). Conteúdo no topo; geração no fim (copiada do 009-gestapo).

Embalagem aprovada no crivo r3 (16/11/2026, EMBALAGEM.md/CRIVO.md):
  A/T1 "TODA la Historia del Cártel de Medellín en 14 Minutos | Su Guerra contra la Extradición" + algemas abertas, sello INTOCABLES
  B/T2 "CÁRTEL DE MEDELLÍN: La guerra por una sola palabra" + página datilografada com uma palavra tarjada, "ART. 35"
  C/T3 "Cómo el Cártel de Medellín tomó de rehén a todo un país" + helicópteros sobre a fazenda (de dia), "¿RESCATE?"
  Frase-âncora do hook: "Esta es TODA la historia del Cártel de Medellín. Y de la guerra que le hizo a un país entero por una sola palabra: extradición."
Ângulo (ANGULO.md): o cartel pelo lado do Estado e dos reféns; fio = a palavra "extradición" (tratado 1979 → sentença 1986 →
decreto 1989 → art. 35 de 1991 → Acto Legislativo 1997). Hook = Diana Turbay, 25/01/1991, pago no exp. 9 e no cierre.
Fora da manada (nenhuma transcrição em ref/): Tratado/Zea, Los Cinco (1985), El Juez, La Sentencia, Los Rehenes, La Operación,
El Sacerdote, o placar 51–13–5, o Acto Legislativo. Fatos obrigatórios da manada (Lara, Cano, Galán, Avianca, fuga, morte) só
como frase de contexto, nunca como cena principal.

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (id I### na ordem de aparição) · "chave" reuso · "chave#enq" reuso com enquadramento
  + "@@TEXTO"      rótulo na tela (máquina de escrever; CAIXA ALTA, até ~28 caracteres)
Bloco: b(texto, *planos, card="BOGOTÁ, 1986", ideia=True) · capítulo: cap("5. El Juez")
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
HOOK_MAX = 35.0      # s: a bíblia pede hook de 25–35 s
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "TODA la Historia del Cártel de Medellín | Su Guerra contra la Extradición"

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Copacabana, Antioquia. Enero de mil novecientos noventa y uno.", card="COPACABANA, 1991")
b("Helicópteros de la Policía sobre una finca. Los captores sacan corriendo a una secuestrada.")
b("Hay disparos. Ella muere esa misma tarde.")
b("Se llama Diana Turbay. Periodista. Hija de un expresidente de Colombia.")
b("En el gobierno de su padre se firmó el tratado que sus captores querían destruir.")
b("Esta es TODA la historia del Cártel de Medellín. Y de la guerra que le hizo a un país entero por una sola palabra: extradición.", ideia=True)

# ───────────────────────── 1. EL TRATADO ─────────────────────────
cap("1. El Tratado")
b("El Tratado. Washington, catorce de septiembre de mil novecientos setenta y nueve. Colombia y Estados Unidos firman un tratado de extradición.", card="WASHINGTON, 1979")
b("En Bogotá gobierna Julio César Turbay. Resumido, el texto dice esto. Un colombiano acusado en Estados Unidos puede ser enviado allá para ser juzgado.")
b("El narcotráfico figura entre los delitos del tratado. Para los traficantes que empiezan a llenar avionetas de cocaína rumbo a Florida, es una amenaza nueva: un juicio a miles de kilómetros de casa.")
b("En mil novecientos ochenta, el Congreso aprueba el tratado con la Ley veintisiete. Pero esa ley no la firma el presidente, que está de viaje. Quien la firma, en su lugar, es un ministro delegatario: Germán Zea.")
b("Nadie lo advierte entonces. No es la firma del presidente.", ideia=True)

# ───────────────────────── 2. EL PANFLETO ─────────────────────────
cap("2. El Panfleto")
b("El Panfleto. Cali, dos de diciembre de mil novecientos ochenta y uno. En pleno partido, una avioneta lanza miles de papeles sobre las tribunas del estadio Pascual Guerrero.", card="CALI, 1981")
b("Anuncian un grupo nuevo: Muerte a Secuestradores, el MAS. Semanas antes, la guerrilla del eme diecinueve había secuestrado a Martha Nieves Ochoa. Es hermana de tres traficantes de Medellín.")
b("Según la revista Semana, el comunicado afirma que lo respaldan doscientos veintitrés jefes del narcotráfico. Dice que pondrán dinero y hombres para perseguir a los secuestradores.")
b("En febrero de mil novecientos ochenta y dos, Martha Nieves vuelve a casa. Según varios historiadores, los grandes traficantes aprenden de ese episodio que, unidos, pueden presionar a cualquiera.")
b("Los hermanos Ochoa. Gonzalo Rodríguez Gacha. Carlos Lehder. Y un contrabandista criado en Envigado, Pablo Escobar. Ese grupo ya tiene dinero y armas. Le falta una cosa: que el tratado nunca los alcance.", ideia=True)

# ───────────────────────── 3. EL CHEQUE ─────────────────────────
cap("3. El Cheque")
b("El Cheque. Bogotá, mil novecientos ochenta y tres. En la Cámara de Representantes, un congresista muestra la copia de un cheque de un millón de pesos.", card="BOGOTÁ, 1983")
b("Lo giró Evaristo Porras, un traficante de Leticia. Según el congresista, el dinero llegó al nuevo ministro de Justicia, Rodrigo Lara Bonilla. Lara explica que entró a una sociedad familiar como pago de un negocio.")
b("El congresista es Jairo Ortega. Su suplente en la Cámara se llama Pablo Escobar.")
b("Lara contraataca: denuncia el dinero de la droga en la política. Y señala a Escobar. En octubre, Escobar pierde la inmunidad. Poco después se retira de la política.")
b("El treinta de abril de mil novecientos ochenta y cuatro, asesinan a Lara Bonilla en Bogotá. Belisario Betancur, que hasta entonces había negado las solicitudes de Estados Unidos, empieza a firmar extradiciones.", ideia=True)

# ───────────────────────── 4. LOS PRIMEROS ─────────────────────────
cap("4. Los Primeros")
b("Los Primeros. Ciudad de Panamá, mayo de mil novecientos ochenta y cuatro. Escobar y Jorge Luis Ochoa, que han salido de Colombia, se reúnen con el expresidente Alfonso López Michelsen.", card="PANAMÁ, 1984")
b("Según López Michelsen, le ofrecen un trato: desmontar el negocio y repatriar su dinero, a cambio de que no haya extradición.")
b("El gobierno no acepta. Y el cinco de enero de mil novecientos ochenta y cinco, por primera vez, Colombia entrega a cinco de sus ciudadanos a la justicia de Estados Unidos.")
b("Uno de ellos es Hernán Botero Moreno, que había presidido el Atlético Nacional, el club de fútbol de Medellín. Lo acusan de lavar más de cincuenta millones de dólares del narcotráfico. Pasará diecisiete años en prisión.")
b("La palabra ya no es un papel en Washington. Es un vuelo que sale de Bogotá. Y los capos empiezan a llamarse a sí mismos los Extraditables. Su blanco siguiente serán los jueces.", ideia=True)

# ───────────────────────── 5. EL JUEZ ─────────────────────────
cap("5. El Juez")
b("El Juez. Bogotá, veintitrés de julio de mil novecientos ochenta y cinco. Asesinan al juez Tulio Manuel Castro Gil.", card="BOGOTÁ, 1985")
b("Nueve meses antes, él había llamado a juicio a Pablo Escobar por el asesinato de Lara Bonilla.")
b("No es el único. Muchos jueces que llevan procesos contra el cártel denuncian amenazas en casa, por teléfono y por correo. A sus familias también.")
b("En noviembre, la guerrilla del eme diecinueve toma el Palacio de Justicia. En la toma y en la operación militar para recuperarlo mueren once magistrados de la Corte Suprema. Si el cártel tuvo algo que ver, todavía se discute.")
b("La Corte que debe decidir sobre el tratado queda diezmada. Un año después, la nueva Corte decide.", ideia=True)

# ───────────────────────── 6. LA SENTENCIA ─────────────────────────
cap("6. La Sentencia")
b("La Sentencia. Bogotá, doce de diciembre de mil novecientos ochenta y seis. La Corte Suprema declara inconstitucional la ley que aprobó el tratado.", card="BOGOTÁ, 1986")
b("La Corte encuentra un defecto de forma. El problema no es lo que dice el tratado. Es quién firmó la ley: aquel ministro delegatario, en mil novecientos ochenta.")
b("Dos días después, el presidente Virgilio Barco vuelve a firmar la ley. Esta vez, él mismo.")
b("Tres días más tarde asesinan en Bogotá a Guillermo Cano, director de El Espectador, el diario que llevaba años denunciando al cártel.")
b("Con la ley firmada de nuevo, el cuatro de febrero de mil novecientos ochenta y siete, la Policía captura a Carlos Lehder en una finca cerca de Guarne, en Antioquia. En menos de veinticuatro horas viaja en un avión rumbo a Estados Unidos.")
b("Pero en junio de mil novecientos ochenta y siete, la Corte anula también la nueva ley, por un vicio de trámite. La extradición queda otra vez en el aire. Y la violencia se intensifica.", ideia=True)

# ───────────────────────── 7. EL ESTADO DE SITIO ─────────────────────────
cap("7. El Estado de Sitio")
b("El Estado de Sitio. Bogotá, dieciocho de agosto de mil novecientos ochenta y nueve. El presidente Virgilio Barco firma, bajo estado de sitio, el decreto mil ochocientos sesenta.", card="BOGOTÁ, 1989")
b("La extradición ya no necesita una ley aprobada por el Congreso. Basta una decisión del gobierno.")
b("Ese mismo día, en Soacha, asesinan a Luis Carlos Galán, el candidato favorito a la presidencia. Cinco días después, los Extraditables declaran la guerra total al Estado.")
b("Siguen meses de atentados: un avión de Avianca derribado en pleno vuelo, con ciento diez muertos, la sede del DAS en Bogotá, bancos, centros comerciales. La justicia los atribuyó al cártel. En Medellín asesinan a cientos de policías.")
b("El Estado responde en los tribunales. Desde noviembre de mil novecientos noventa, en los procesos de narcotráfico hay jueces sin rostro: su identidad queda en reserva, para que nadie pueda amenazarlos.")
b("Pero el cártel recurre a otra forma de presión, más cruel que una bomba: el secuestro.", ideia=True)
b("Si este expediente te muestra una Colombia que no conocías, suscríbete. Cada semana abrimos uno nuevo. Ahora, volvemos a Diana Turbay.")

# ───────────────────────── 8. LOS REHENES ─────────────────────────
cap("8. Los Rehenes")
b("Los Rehenes. Bogotá, treinta de agosto de mil novecientos noventa. Diana Turbay dirige la revista Hoy por Hoy y el noticiero Criptón. Sale de viaje con cinco personas de su equipo.", card="BOGOTÁ, 1990")
b("Le han prometido una entrevista con el cura Manuel Pérez, jefe de la guerrilla del ELN. Es una trampa. Según reconstruyó García Márquez, los esperan hombres de los Extraditables.")
b("El diecinueve de septiembre secuestran a Francisco Santos, jefe de redacción de El Tiempo. Y a Marina Montoya, hermana del secretario general de la Presidencia del gobierno anterior.")
b("En noviembre secuestran a Maruja Pachón, directora de Focine y cuñada de Luis Carlos Galán. Y a Beatriz Villamizar, cuñada de Maruja.")
b("No los eligen al azar. Todos tienen vínculos con el poder. García Márquez lo cuenta en Noticia de un secuestro: los rehenes eran su forma de presionar al gobierno.")
b("Desde septiembre, el nuevo presidente, César Gaviria, ofrece una salida. Quien se entregue y confiese un delito tendrá rebaja de pena y no será extraditado. Al cártel no le basta. Quiere que nadie, nunca, pueda ser extraditado.", ideia=True)

# ───────────────────────── 9. LA OPERACIÓN ─────────────────────────
cap("9. La Operación")
b("La Operación. Copacabana, veinticinco de enero de mil novecientos noventa y uno. Volvemos a la finca de la montaña.", card="COPACABANA, 1991")
b("La familia no sabía nada de la operación. Diana había pedido a los suyos que evitaran cualquier intento de rescatarla por la fuerza.")
b("Ese día llega un grupo de élite de la Policía con helicópteros. El gobierno dirá que no buscaban a Diana, sino a hombres del cártel.")
b("Los captores la sacan corriendo. Recibe un disparo en la espalda. La versión oficial culpa a los secuestradores. Otras versiones no descartan que el disparo viniera de la propia operación.")
b("La llevan en helicóptero a Medellín. Muere en el Hospital General, al final de la tarde.")
b("Días después, los Extraditables anuncian que han ejecutado a Marina Montoya. Y el país entiende que la guerra por una palabra ya alcanza a cualquiera.", ideia=True)

# ───────────────────────── 10. EL SACERDOTE ─────────────────────────
cap("10. El Sacerdote")
b("El Sacerdote. Bogotá, mayo de mil novecientos noventa y uno. Rafael García Herreros tiene ochenta y dos años y un programa de televisión de pocos minutos: El Minuto de Dios.", card="BOGOTÁ, 1991")
b("Desde la pantalla le habla a Pablo Escobar. Le pide que se entregue.")
b("Alberto Villamizar, el esposo de Maruja Pachón, lleva meses negociando por su cuenta para salvarla. Y busca al sacerdote.")
b("Según el relato de García Márquez, Escobar acepta que el sacerdote sea el testigo de su entrega.")
b("El veinte de mayo, tras seis meses de cautiverio, los captores liberan a Maruja Pachón. Ese mismo día, también a Francisco Santos.")
b("Pero Escobar todavía no se entrega. Espera una sola cosa. Una frase escrita en otra parte de Bogotá.", ideia=True)

# ───────────────────────── 11. EL ARTÍCULO ─────────────────────────
cap("11. El Artículo")
b("El Artículo. Bogotá, diecinueve de junio de mil novecientos noventa y uno. La Asamblea Nacional Constituyente escribe una Constitución nueva para Colombia.", card="BOGOTÁ, 1991")
b("Ese día vota un artículo cuya frase central dice: «Se prohíbe la extradición de colombianos por nacimiento».")
b("Cincuenta y uno a favor. Trece en contra. Cinco abstenciones.")
b("Horas después, un helicóptero aterriza en una cárcel nueva en las montañas de Envigado, sobre Medellín. De él baja Pablo Escobar. Se entrega junto al sacerdote García Herreros y a Alberto Villamizar.")
b("Según investigaciones posteriores, el lugar lo había escogido él. La llamaban La Catedral.")
b("La extradición, la palabra por la que el cártel hizo la guerra, quedaba prohibida en la nueva Constitución. Por un tiempo, parecieron intocables.", ideia=True)

# ───────────────────────── 12. LA FUGA ─────────────────────────
cap("12. La Fuga")
b("La Fuga. Envigado, julio de mil novecientos noventa y dos. Tras las denuncias de que Escobar ordenaba asesinatos desde La Catedral, el gobierno decide trasladarlo.", card="ENVIGADO, 1992")
b("En la noche del veintiuno al veintidós de julio, Escobar escapa con varios de sus hombres, aunque la cárcel está rodeada por el Ejército. Es un duro golpe para el Estado.")
b("Empieza la persecución. La Policía refuerza su Bloque de Búsqueda. Y aparece otro grupo ilegal, Los Pepes, formado por antiguos socios y rivales de Escobar, que asesinan a sus allegados.")
b("El dos de diciembre de mil novecientos noventa y tres, Escobar muere en Medellín durante un operativo de la Policía. Acababa de cumplir cuarenta y cuatro años.")
b("Para entonces, Rodríguez Gacha había muerto en un operativo policial, en mil novecientos ochenta y nueve. Y Lehder seguía preso en Estados Unidos.")
b("El Cártel de Medellín se desmorona. Pero la extradición sigue prohibida en la Constitución.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. La Palabra")
b("La Palabra. Bogotá, dieciséis de diciembre de mil novecientos noventa y siete. El Congreso aprueba el Acto Legislativo número uno. La extradición de colombianos vuelve a la Constitución.", card="BOGOTÁ, 1997")
b("No es retroactiva. Pero en mil novecientos noventa y nueve capturan a Fabio Ochoa, hermano de Martha Nieves, acusado de seguir traficando después de esa fecha. En septiembre de dos mil uno lo extraditan a Estados Unidos.")
b("Desde entonces, Colombia ha extraditado a miles de personas. Según El Tiempo, solo entre dos mil diez y dos mil veinte fueron cerca de mil novecientas.")
b("Diana Turbay no alcanzó a verlo. Murió casi siete años antes, secuestrada, en la guerra contra un tratado firmado durante el gobierno de su padre.")
b("Durante más de seis años, la Constitución prohibió la extradición. La violencia de esa guerra costó la vida a cientos de policías, jueces, periodistas y civiles. Y al final, la palabra volvió.", ideia=True)
b("Y tú, ¿qué crees que aprendió Colombia de esta guerra? ¿Qué parte de esta historia no conocías? Déjalo en los comentarios.")

THUMBS = []
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
