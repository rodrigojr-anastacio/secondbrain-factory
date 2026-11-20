#!/usr/bin/env python3
"""Fonte única do dossie-es 013 (Juicios de Núremberg): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py (na pasta do vídeo). Geração copiada do 012-mi6.

Embalagem aprovada no crivo r3 (20/11/2026, EMBALAGEM.md/CRIVO.md):
  A/T1 fórmula + fones sobre creme, NÚREMBERG + sello SIN NOMBRE (objeto-simbolo, controle)
  B/T2 "Cómo Núremberg le puso nombre al crimen que no tenía nombre" + fiscal lendo a acusação sob refletor, sem texto (cena-acao)
  C/T3 "Núremberg: de la sala 600 a los tribunales de América Latina" + mapa atlântico, fio vermelho, HASTA AQUÍ (mapa-lugar)
Ângulo (ANGULO.md): las palabras de Núremberg (o tribunal que inventou o que ia julgar) e o destino delas na América Latina.

Sintaxe dos planos (campo s): "chave|prompt" nova · "chave" reuso · "chave#enq" reuso com enquadramento · + "@@TEXTO" rótulo.
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
HOOK_MAX = 36.0      # s: a bíblia pede hook de 25–35 s (EMBALAGEM: frase-âncora até 0:35)
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "TODA la historia de los Juicios de Núremberg en 14 minutos"
TITULOS = ("T1 TODA la historia de los Juicios de Núremberg en 14 minutos / "
           "T2 Cómo Núremberg le puso nombre al crimen que no tenía nombre / "
           "T3 Núremberg: de la sala 600 a los tribunales de América Latina")
PROMESSA = ("Núremberg tuvo que inventar lo que iba a juzgar (las palabras genocidio y crímenes contra la humanidad, "
            "la regla contra 'cumplía órdenes', hasta la sala y la traducción; genocidio, de Lemkin, entró en la acusación pero no en la sentencia) y esas reglas acabaron alcanzando a "
            "criminales y dictadores en América Latina.")

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Núremberg, octubre de mil novecientos cuarenta y seis. En un hotel, un fiscal estadounidense ve a un abogado polaco muy afectado.", card="NÚREMBERG, 1946")
b("Es Raphael Lemkin. La guerra le quitó a cuarenta y nueve familiares. Para ese crimen, inventó una palabra.")
b("Se leyó en voz alta el primer día del juicio. En la sentencia, ni una vez. La palabra es genocidio.")
b("Esta es TODA la historia de los juicios de Núremberg. Y de las palabras que viajaron desde allí hasta América Latina.", ideia=True)

# ───────────────────────── 1. LA PALABRA ─────────────────────────
cap("1. La Palabra")
b("La Palabra. Washington, mil novecientos cuarenta y cuatro. Lemkin es un jurista judío polaco. Huyó de la invasión alemana en mil novecientos treinta y nueve.", card="WASHINGTON, 1944")
b("En un libro sobre la ocupación nazi de Europa, propone un término nuevo. Une la raíz griega genos, pueblo o raza, con la terminación latina cidio, matar.")
b("Para Lemkin, genocidio es la destrucción de una nación o de un grupo étnico. No solo matar personas. Borrar a un pueblo entero.")
b("Tres años antes, Churchill había dicho por radio que el mundo estaba ante un crimen sin nombre. Ahora el nombre existe.")
b("Falta que un tribunal se atreva a usarlo. Y otro jurista busca otra palabra. Estudió Derecho en la misma universidad que Lemkin.", ideia=True)

# ───────────────────────── 2. EL JARDÍN ─────────────────────────
cap("2. El Jardín")
b("El Jardín. Cambridge, veintinueve de julio de mil novecientos cuarenta y cinco. Robert Jackson, el fiscal jefe estadounidense, almuerza en casa del profesor Hersch Lauterpacht. Después, hablan en el jardín.", card="CAMBRIDGE, 1945")
b("Según el jurista y escritor Philippe Sands, en el jardín Jackson le pide ayuda con una pregunta: cómo llamar lo que los nazis hicieron con millones de civiles.")
b("Lauterpacht le propone un nombre: crímenes contra la humanidad.")
b("Lauterpacht estudió en Leópolis, la ciudad que los alemanes llamaban Lemberg. Lemkin también. Según Sands, casi toda la familia de Lauterpacht fue asesinada allí.")
b("Y uno de los futuros acusados gobernó la Polonia ocupada, Leópolis incluida: Hans Frank.")
b("Diez días después del almuerzo, esa expresión entra en un documento firmado por cuatro potencias.", ideia=True)

# ───────────────────────── 3. LA CARTA ─────────────────────────
cap("3. La Carta")
b("La Carta. Londres, agosto de mil novecientos cuarenta y cinco. Su artículo ocho cabe en una frase. Haber actuado por orden de un gobierno o de un superior no libra a nadie de responsabilidad.", card="LONDRES, 1945")
b("Como máximo, podrá reducir la pena. Las cuatro potencias aliadas firman esa Carta el ocho de agosto. Define tres crímenes: contra la paz, de guerra y contra la humanidad.")
b("En los meses siguientes, diecinueve países se adhieren al acuerdo. Entre ellos, Venezuela, Uruguay, Paraguay, Panamá, Honduras y Haití.")
b("Guarda esa regla de las órdenes. Cuarenta y dos años después, en Buenos Aires, alguien la escribirá al revés. Pero antes, la regla necesita una sala.", ideia=True)

# ───────────────────────── 4. LA SALA ─────────────────────────
cap("4. La Sala")
b("La Sala. Núremberg, verano de mil novecientos cuarenta y cinco. Un capitán estadounidense de treinta y tres años, Dan Kiley, recibe un encargo: preparar la sala seiscientos del Palacio de Justicia.", card="NÚREMBERG, 1945")
b("Kiley es arquitecto y sirve en el servicio de inteligencia de su país. La sala es demasiado pequeña para lo que viene.")
b("Kiley derriba una pared y eleva el techo. La sala duplica su tamaño. Instala cabinas de vidrio para intérpretes y camarógrafos. Y una galería para doscientos cincuenta periodistas.")
b("Según contó Kiley, en la obra trabajaron presos que habían sido miembros de las SS, junto a civiles alemanes. Las butacas de terciopelo rojo salieron de un cine cercano.")
b("Para Kiley no era un juicio cualquiera: lo iba a mirar el mundo entero. Y en esa sala, la primera palabra importante se iba a decir en francés.", ideia=True)

# ───────────────────────── 5. EL MICRÓFONO ─────────────────────────
cap("5. El Micrófono")
b("El Micrófono. Núremberg, veinte de noviembre de mil novecientos cuarenta y cinco, primer día del juicio. Un fiscal francés, Pierre Mounier, lee ante el micrófono el cargo de crímenes de guerra.", card="NÚREMBERG, 1945")
b("Ahí está la palabra de Lemkin: genocidio. La acusación habla del exterminio de grupos raciales y nacionales. Sobre todo, de judíos, polacos y gitanos.")
b("En ese mismo instante, la palabra suena en otras tres lenguas. Detrás de un vidrio, los intérpretes de Léon Dostert traducen mientras Mounier habla.")
b("Dostert, antiguo intérprete del general Eisenhower, probó a unos setecientos candidatos. Solo sirvió uno de cada veinte. Después, la ONU copiará el sistema.")
b("Pero una acusación también puede volverse contra quien acusa. Unos meses después, un abogado alemán lo demuestra con un cuestionario.", ideia=True)

# ───────────────────────── 6. EL CUESTIONARIO ─────────────────────────
cap("6. El Cuestionario")
b("El Cuestionario. Once de mayo de mil novecientos cuarenta y seis. Un oficial de la Marina estadounidense le hace preguntas por escrito al almirante Chester Nimitz, que había comandado la flota del Pacífico.", card="ESTADOS UNIDOS, 1946")
b("Las preguntas las pidió Otto Kranzbühler, abogado del almirante Karl Dönitz, el sucesor de Hitler. A Dönitz se lo acusa, entre otros cargos, de hundir barcos sin aviso.")
b("Nimitz responde bajo juramento: el siete de diciembre de mil novecientos cuarenta y uno, el jefe de operaciones navales ordenó la guerra submarina sin restricciones contra Japón.")
b("La sentencia cita esa respuesta y una orden británica de mil novecientos cuarenta. Y escribe que la pena de Dönitz no se fija por esas violaciones. Recibe diez años por otros cargos.")
b("El tribunal solo juzga a los vencidos: será una de sus críticas más repetidas. Pero no finge que los vencedores no tengan expedientes. Y en octubre, un hombre espera de la sentencia otra cosa: su palabra.", ideia=True)

# ───────────────────────── 7. EL HOTEL ─────────────────────────
cap("7. El Hotel")
b("El Hotel. Núremberg, primeros días de octubre de mil novecientos cuarenta y seis. Volvemos al hotel del principio, el Grand Hotel. El fiscal Henry King contó que allí vio a Lemkin muy afectado.", card="NÚREMBERG, 1946")
b("Los jueces acaban de leer la sentencia, tras doscientos dieciocho días de audiencias. Condenan a muerte a doce acusados, Bormann entre ellos, en ausencia, y absuelven a tres. Los demás van a prisión.")
b("Diez de esas condenas se ejecutan el dieciséis de octubre. Hermann Göring se había quitado la vida la noche anterior, en su celda.")
b("La sentencia condena crímenes contra la humanidad, pero solo los ligados a la guerra. Lo que el régimen hizo antes contra judíos y otros grupos queda fuera. Y la palabra genocidio no aparece ni una vez.")
b("Según el jurista William Schabas, Lemkin llamó a ese veredicto el día más negro de su vida. Su palabra había entrado en la sala, pero no en la sentencia.", ideia=True)
b("Si te interesan estos expedientes, suscríbete. Porque lo que viene ahora se cuenta mucho menos: Núremberg no terminó en esa sala.")

# ───────────────────────── 8. EL CÓDIGO ─────────────────────────
cap("8. El Código")
b("El Código. Núremberg, nueve de diciembre de mil novecientos cuarenta y seis. Empieza la serie de juicios que siguen al principal, ahora ante tribunales militares estadounidenses.", card="NÚREMBERG, 1946")
b("El primero sienta en el banquillo a veintitrés acusados, casi todos médicos. Se los acusa de experimentos con prisioneros de los campos, sin su consentimiento. Muchos de ellos murieron o quedaron mutilados.")
b("En agosto de mil novecientos cuarenta y siete, dieciséis son culpables y siete condenados a muerte. Con la sentencia nace un texto de diez puntos: el Código de Núremberg.")
b("Su primera frase dice: el consentimiento voluntario del sujeto humano es absolutamente esencial. La ética médica todavía empieza ahí, con las víctimas de aquellos experimentos.")
b("Otra regla inventada en Núremberg. Mientras tanto, Lemkin recorre pasillos, delegado por delegado, con su palabra.", ideia=True)

# ───────────────────────── 9. LA CONVENCIÓN ─────────────────────────
cap("9. La Convención")
b("La Convención. París, nueve de diciembre de mil novecientos cuarenta y ocho. La ONU aprueba la Convención para la Prevención y la Sanción del Delito de Genocidio.", card="PARÍS, 1948")
b("Define el genocidio como los actos cometidos para destruir, total o parcialmente, a un grupo nacional, étnico, racial o religioso.")
b("La palabra que el tribunal no escribió ahora es un delito internacional. Entra en vigor en enero de mil novecientos cincuenta y uno.")
b("Pero una ley solo sirve si alguien la aplica. Y varios de los responsables de esos crímenes cruzaron el océano.", ideia=True)

# ───────────────────────── 10. LA FÁBRICA ─────────────────────────
cap("10. La Fábrica")
b("La Fábrica. São Bernardo do Campo, Brasil, años sesenta. En la planta de Volkswagen trabaja un austríaco llamado Franz Stangl. Usa su propio nombre.", card="SÃO PAULO, 1967")
b("Stangl había sido comandante de Sobibor y después de Treblinka, dos campos de exterminio donde fueron asesinados cientos de miles de judíos. Huyó por Italia y Siria y llegó a Brasil en mil novecientos cincuenta y uno.")
b("El veintiocho de febrero de mil novecientos sesenta y siete, la policía brasileña lo detiene en São Paulo, tras una pista de Simon Wiesenthal. En junio, Brasil lo extradita a Alemania Occidental.")
b("En diciembre de mil novecientos setenta, un tribunal de Düsseldorf lo condena a cadena perpetua. Según esa sentencia, en Treblinka fueron asesinadas al menos cuatrocientas mil personas.")
b("Stangl murió en prisión en mil novecientos setenta y uno. Brasil lo entregó. En Chile, la respuesta fue otra.", ideia=True)

# ───────────────────────── 11. EL PLAZO ─────────────────────────
cap("11. El Plazo")
b("El Plazo. Santiago de Chile, mil novecientos sesenta y tres. Alemania Occidental pide la extradición de Walter Rauff, antiguo oficial de las SS.", card="SANTIAGO, 1963")
b("Según la fiscalía alemana, Rauff dirigió el uso de camiones en los que se asfixiaba a las víctimas con gas. Así fueron asesinadas unas noventa y siete mil personas.")
b("La Corte Suprema de Chile rechaza la extradición. Según la ley chilena, el delito ya había prescrito: el plazo era de quince años.")
b("En mil novecientos sesenta y ocho, la ONU aprueba otra convención: los crímenes de guerra y contra la humanidad no prescriben. Para el caso Rauff, llegó tarde.")
b("Rauff murió libre en Santiago, en mil novecientos ochenta y cuatro. En Argentina, el obstáculo no fue un plazo. Fue una ley.", ideia=True)

# ───────────────────────── 12. LA LEY ─────────────────────────
cap("12. La Ley")
b("La Ley. Buenos Aires, mil novecientos ochenta y cinco. Nueve excomandantes de la dictadura militar se sientan en el banquillo, acusados de secuestros, torturas y asesinatos. La prensa habla del Núremberg argentino.", card="BUENOS AIRES, 1985")
b("El fiscal Julio César Strassera cierra su alegato con una frase: señores jueces, nunca más. En diciembre, cinco de los nueve son condenados.")
b("Quedan cientos de oficiales por juzgar. En mil novecientos ochenta y seis, una ley pone plazo a las denuncias. Al año siguiente, tras un levantamiento militar, llega la Ley de Obediencia Debida.")
b("Presume que casi todos los oficiales de menor rango actuaron cumpliendo órdenes y, por eso, no pueden ser castigados. Es la defensa que el artículo ocho de Núremberg había rechazado en mil novecientos cuarenta y cinco.")
b("En dos mil tres, el Congreso la anula. En dos mil cinco, la Corte Suprema la declara inconstitucional y los juicios se reabren. En otro país, la palabra de Lemkin llega a un tribunal nacional, contra un exdictador.", ideia=True)

# ───────────────────────── 13. LA JUEZA ─────────────────────────
cap("13. La Jueza")
b("La Jueza. Ciudad de Guatemala, diez de mayo de dos mil trece. La jueza Yassmín Barrios lee la sentencia contra el exdictador Efraín Ríos Montt.", card="GUATEMALA, 2013")
b("El tribunal lo declara culpable de genocidio contra el pueblo maya ixil, por mil setecientas setenta y una víctimas documentadas, y de delitos contra los deberes de humanidad. Ochenta años de prisión.")
b("Según la radio pública estadounidense NPR, era la primera vez que un país condenaba por genocidio a uno de sus propios exjefes de Estado.")
b("Diez días después, la Corte de Constitucionalidad anula la sentencia por defectos de procedimiento, no por inocencia. El juicio vuelve a empezar y Ríos Montt muere en dos mil dieciocho sin un nuevo veredicto.")
b("Pero la palabra ya se había escrito en una sentencia de su propio país. Sesenta y siete años después de faltar en la de Núremberg.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. La Palabra")
b("La Palabra. Nueva York, agosto de mil novecientos cincuenta y nueve. Raphael Lemkin muere de un ataque al corazón, a los cincuenta y nueve años, sin dinero.", card="NUEVA YORK, 1959")
b("Según el periodista A. M. Rosenthal, del New York Times, a su entierro fueron siete personas.")
b("Núremberg no inventó el crimen. Le puso nombre ante un tribunal: crímenes contra la humanidad en la sentencia, genocidio en la acusación. Y sus reglas terminaron en salas de Buenos Aires y de Guatemala.")
b("El crimen era viejo. Lo nuevo fue tener una palabra para él.", ideia=True)
b("Y tú, ¿crees que ponerle nombre a un crimen ayuda a que no se repita? Déjalo en los comentarios.")

# ───────────────────────── STORYBOARD ─────────────────────────
SB = None
_textos = [x for x in B if "t" in x]
if SB is not None:
    assert len(SB) == len(_textos), f"SB {len(SB)} x blocos {len(_textos)}"
    for _blk, _s in zip(_textos, SB): _blk["s"] = _s
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
        f"# {TITULO}: roteiro\n\nPromessa: {PROMESSA}\n\nTítulos: {TITULOS}\n\n"
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
