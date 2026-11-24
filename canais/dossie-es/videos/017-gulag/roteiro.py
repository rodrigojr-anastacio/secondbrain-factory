#!/usr/bin/env python3
"""Fonte única do dossie-es 017 (El Gulag): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py (na pasta do vídeo). Geração copiada do 015-gru.

Embalagem aprovada no crivo r3 (23/11/2026, EMBALAGEM.md/CRIVO.md):
  A/T1 "GULAG: la empresa de Stalin que necesitaba presos" + lingote em trapézio com estrela dentro de marmita de lata vazia, GULAG + sello ¿RENTABLE? (objeto-simbolo, controle)
  B/T2 "Cómo funcionaba el Gulag por dentro: plan, oro y mano de obra presa" + tabela de normas com 3 pães decrescentes e carimbo de estrela, NORMA (documento-evidencia)
  C/T3 "Republicanos y Franquistas, Presos en el Mismo Gulag | Expedientes de Stalin" + homem de telogreika e ushanka desce do navio em Barcelona, BARCELONA (cena-acao)
Ângulo (ANGULO.md): el Gulag como empresa (papeles: decreto, libro, oro, norma, memorándum, orden) y los hispanohablantes que se tragó
(marineros, pilotos, divisionarios, el mexicano Vadillo) hasta el Semíramis (1954) y Solzhenitsyn en TVE (1976).

Sintaxe dos planos (campo s): "chave|prompt" nova · "chave" reuso · "chave#enq" reuso com enquadramento · + "@@TEXTO" rótulo.
"""
import json, math, re
from pathlib import Path

WPS = 2.38           # palavras/s medidas no 001–015 (erro de 1–3%)
BREAK, LONG = 0.35, 0.8
MAX_PLANO_INICIO = 3.0   # s por plano nos primeiros INICIO s (~20 cortes/min)
INICIO = 60.0
MAX_PLANO = 3.6      # s por plano depois (~17 cortes/min)
INEDITO_ATE = 180.0  # s: só imagens novas até aqui
JANELA = 60.0        # s: mesmo enquadramento da mesma imagem só depois disso
HOOK_MAX = 40.0      # s: bíblia 25–35 s + frase-ponte pedida pela EMBALAGEM
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "GULAG: la empresa de Stalin que necesitaba presos"
TITULOS = ("T1 GULAG: la empresa de Stalin que necesitaba presos / "
           "T2 Cómo funcionaba el Gulag por dentro: plan, oro y mano de obra presa / "
           "T3 Republicanos y Franquistas, Presos en el Mismo Gulag | Expedientes de Stalin")
PROMESSA = ("El Gulag por dentro como una empresa del Estado soviético que funcionaba con presos (decreto para colonizar y explotar, "
            "oro en toneladas, la norma, los informes inflados, hasta su cierre 'por ineficiencia'), y los españoles de los dos bandos "
            "de la guerra civil que acabaron en sus campos, hasta el barco que los trajo a Barcelona en 1954.")

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Barcelona, dos de abril de mil novecientos cincuenta y cuatro. Un barco griego entra en el puerto.", card="BARCELONA, 1954")
b("A bordo vienen doscientos ochenta y seis españoles. No vuelven de una guerra. Vuelven de los campos de trabajo soviéticos.")
b("Unos habían luchado por Franco. Otros, contra él. Y durante años compartieron los mismos campos.")
b("Esta es TODA la historia del Gulag: la empresa de Stalin que necesitaba presos. Y la de los españoles que acabaron trabajando para ella. Para entender cómo llegaron ahí, hay que abrir sus papeles.", ideia=True)

# ───────────────────────── 1. EL DECRETO ─────────────────────────
cap("1. El Decreto")
b("El Decreto. Moscú, once de julio de mil novecientos veintinueve. Un decreto secreto del gobierno soviético fija una tarea para los presos con penas largas.", card="MOSCÚ, 1929")
b("No basta con encerrarlos. Irán a regiones remotas, casi vacías, para colonizarlas y explotar sus recursos naturales: madera, carbón, metales.")
b("El plan es modesto. Campos pequeños, cincuenta mil plazas para todo el país. Es la primera cifra de la empresa. Y se queda corta desde el primer invierno.")
b("Al año siguiente, la administración que dirige esos campos recibe su nombre definitivo. Por sus siglas en ruso: Gulag, Dirección General de Campos.")
b("Los historiadores discuten si se arrestaba para llenar los campos. Lo que dicen los papeles es que el plan contaba a los presos como mano de obra. Y su primera gran obra tuvo hasta un libro.", ideia=True)

# ───────────────────────── 2. EL LIBRO ─────────────────────────
cap("2. El Libro")
b("El Libro. Moscú, primavera de mil novecientos treinta y siete. Semión Firin, antiguo subjefe del Gulag, es arrestado. En agosto lo fusilan.", card="MOSCÚ, 1937")
b("Firin había editado, junto a Máximo Gorki y Leopold Averbaj, la historia oficial del canal del mar Blanco, escrita por treinta y seis autores soviéticos. Según el diario ruso Nóvaya Gazeta, tras su caída se retira la tirada.")
b("El canal une el mar Blanco con el Báltico: doscientos veintisiete kilómetros, abiertos en unos veinte meses por más de cien mil presos. Se inaugura el dos de agosto de mil novecientos treinta y tres.")
b("Los registros del propio Gulag anotan unos doce mil fallecidos. Algunas estimaciones de historiadores duplican esa cifra. Ese mismo mes, una brigada de unos ciento veinte escritores recorre la obra para celebrarla.")
b("La empresa había aprendido algo: las obras también se enseñan. Once años después, invitaría a otro visitante a ver sus minas. Esta vez, desde Washington.", ideia=True)

# ───────────────────────── 3. EL ORO ─────────────────────────
cap("3. El Oro")
b("El Oro. Magadán, mayo de mil novecientos cuarenta y cuatro. Henry Wallace, vicepresidente de Estados Unidos, aterriza en Kolimá, en el extremo noreste soviético.", card="MAGADÁN, 1944")
b("Lo recibe Iván Nikíshov, jefe de Dalstrói, la empresa del Gulag que saca oro de la región. Le enseña escuelas, granjas y minas.")
b("Según presos que lo vivieron, las torres de vigilancia desaparecen esos días y los reclusos quedan encerrados. Años después, Wallace admitió que lo había impresionado demasiado el espectáculo.")
b("Detrás del espectáculo estaban las cifras. Entre mil novecientos veintiocho y mil novecientos treinta y tres, la región había dado menos de dos toneladas de oro. En mil novecientos treinta y siete, Dalstrói entrega cincuenta y una toneladas y media. A comienzos de mil novecientos cuarenta trabajan allí más de ciento noventa mil presos.")
b("En Moscú, los informes se medían en toneladas. Pero había una pregunta que ningún informe respondía: ¿era rentable? Dentro de los campos, la respuesta empezaba en una tabla.", ideia=True)

# ───────────────────────── 4. LA NORMA ─────────────────────────
cap("4. La Norma")
b("La Norma. Moscú, trece de marzo de mil novecientos cincuenta. El gobierno soviético decide pagar un salario a los presos de los campos.", card="MOSCÚ, 1950")
b("Hasta entonces, la paga era la comida. Según Applebaum, en trabajo pesado, quien cumplía la norma podía recibir ochocientos gramos de pan. A los presos clasificados como inválidos les tocaba la mitad.")
b("Había existido otro incentivo: días de condena descontados por buen trabajo. Según el historiador Oleg Jlevniuk, Beria los suprimió en mil novecientos treinta y nueve.")
b("A comienzos de los años cincuenta, más de la cuarta parte de los presos que trabajaban a destajo no alcanzaba la norma. Los propios dirigentes ya preferían trabajadores libres, que rendían más y no necesitaban guardias. El salario fue un último intento.")
b("En total, según el directorio de la organización rusa Memorial que cita Applebaum, hubo al menos cuatrocientos setenta y seis complejos de campos. En algunos acabaron españoles que habían llegado como aliados.", ideia=True)

# ───────────────────────── 5. LOS MARINEROS ─────────────────────────
cap("5. Los Marineros")
b("Los Marineros. Odesa, primavera de mil novecientos treinta y nueve. La guerra civil española acaba de terminar. En la Unión Soviética siguen las tripulaciones de tres mercantes de la República. Se llaman Cabo San Agustín, Juan Sebastián Elcano e Inocencio Figaredo. Años después, algunos compartirán campo con sus enemigos de la guerra.", card="ODESA, 1939")
b("Habían traído suministros para la República. Son doscientos cincuenta hombres sin un país al que volver. Ese verano, unos ciento treinta marineros de los barcos retenidos salen por Estambul. Los demás se quedan.")
b("Piden irse a México, a Francia, adonde sea. Según la historiadora Luiza Iordache, para Moscú un extranjero que quería marcharse era un sospechoso.")
b("A finales de junio de mil novecientos cuarenta y uno, días después de la invasión alemana, Lavrenti Beria ordena internar en Norilsk a los marineros y pilotos españoles que pedían salir. Ninguno fue juzgado.")
b("Norilsk, por encima del círculo polar, era una mina de níquel del Gulag. Allí la empresa los pone a trabajar. Según Iordache, más de veinte republicanos españoles fallecen en los campos antes de mil novecientos cincuenta y cuatro.", ideia=True)
b("Si te interesan estos expedientes, suscríbete. Porque con los marineros cayeron también los alumnos de una escuela de pilotos.")

# ───────────────────────── 6. LOS PILOTOS ─────────────────────────
cap("6. Los Pilotos")
b("Los Pilotos. Kirovabad, Azerbaiyán soviético, enero de mil novecientos treinta y nueve. Llega la última expedición de jóvenes españoles a una escuela de aviación militar.", card="KIROVABAD, 1939")
b("Entre todas las promociones son unos ciento cincuenta o doscientos alumnos. Vinieron a aprender a volar para la República. Cuando terminan, la República ya no existe.")
b("Los intentos de enviarlos a México fracasan. Moscú les ofrece trabajo en fábricas. Unos aceptan; otros piden marcharse.")
b("En enero de mil novecientos cuarenta detienen a ocho: ocho años por actividades antisoviéticas. Según Iordache, solo cuatro sobrevivieron. En junio de mil novecientos cuarenta y uno, al capitán Federico Gonzalo lo condenan a quince años por negarse a suscribir el empréstito del Estado.")
b("Mientras tanto, la guerra vaciaba los campos. En mil novecientos cuarenta y dos, según los certificados del propio Gulag, fallecen más de trescientos cincuenta mil presos. Y en mil novecientos cuarenta y tres llegaron españoles del otro bando.", ideia=True)

# ───────────────────────── 7. EL NÚMERO ─────────────────────────
cap("7. El Número")
b("El Número. Krasni Bor, cerca de Leningrado, diez de febrero de mil novecientos cuarenta y tres. La División Azul, los voluntarios que Franco envió a luchar junto a Alemania, recibe una gran ofensiva soviética. A sus soldados los llaman divisionarios.", card="KRASNI BOR, 1943")
b("Entre los capturados está Constante Vicente Giráldez. Según su hija, pierde la vista de un ojo. En sus papeles militares figura un número: doce mil ciento veintitrés.")
b("Según los historiadores, los divisionarios capturados van de unos trescientos setenta a casi quinientos. Llegan como prisioneros de guerra. A muchos los condenan y los envían a campos de trabajo.")
b("Según Iordache, a finales de los años cuarenta, republicanos y divisionarios conviven en los mismos campos. Uno de ellos fue Karagandá, en Kazajistán. Allí, según su hija, Constante Vicente acaba haciendo pan para los oficiales del campo.")
b("Hombres de los dos bandos de la guerra civil comparten ahora campo. Pero no todos los presos que hablaban español eran españoles. Uno era mexicano.", ideia=True)

# ───────────────────────── 8. LA EMBAJADA ─────────────────────────
cap("8. La Embajada")
b("La Embajada. Moscú, diecinueve de junio de mil novecientos cuarenta y siete. Un hombre vestido de campesino se presenta en la embajada de México y pide asilo.", card="MOSCÚ, 1947")
b("Es Evelio Vadillo, comunista de Ciudad del Carmen, en Campeche. Su partido lo había enviado a Moscú en mil novecientos treinta y cinco. Un año después lo detienen: cinco años de campo y cinco de destierro en Kazajistán.")
b("El embajador Luciano Joublanc Rivas lo recibe. Pero Moscú no deja salir a Vadillo. En mil novecientos cincuenta vuelve a prisión: veinte años, acusado de espiar para México.")
b("Lo liberan en mil novecientos cincuenta y cinco. El dieciséis de octubre, por fin, vuelve a México. Un libro reciente cuenta su caso con un título exacto: Veinte años en el Gulag.")
b("Vadillo sale dos años después de un cambio que lo movió todo en Moscú: la muerte de Stalin.", ideia=True)

# ───────────────────────── 9. EL MEMORÁNDUM ─────────────────────────
cap("9. Las Obras")
b("Las Obras. Moscú, doce de marzo de mil novecientos cincuenta y tres. Una semana después de la muerte de Stalin, Lavrenti Beria cancela más de veinte grandes obras del Gulag.", card="MOSCÚ, 1953")
b("Canales, presas, un ferrocarril por la tundra ártica entre Salejard e Ígarka. Ese mes, Beria informa a la dirección del partido de cuántos presos hay: más de dos millones y medio.")
b("El veintisiete de marzo, una amnistía libera a cerca de un millón, casi todos por delitos comunes. En junio, según Applebaum, Beria dice querer liquidar el trabajo forzado por su ineficiencia económica.")
b("Esa fue la respuesta del propio régimen a la pregunta del oro: la empresa no era rentable. Pero los españoles seguían dentro. Un año después, un barco fue a buscarlos.", ideia=True)

# ───────────────────────── 10. EL BARCO ─────────────────────────
cap("10. El Barco")
b("El Barco. Odesa, comienzos de mil novecientos cincuenta y cuatro. España y la Unión Soviética no tienen relaciones. La Cruz Roja francesa fleta un barco griego: el Semíramis.", card="ODESA, 1954")
b("Suben doscientos ochenta y seis españoles: más de doscientos divisionarios y unos treinta marineros y pilotos republicanos. También cuatro antiguos niños de la guerra.")
b("Durante la travesía, sus llamadas por radio a las familias se oyen en toda España. El dos de abril, a las cinco y treinta y cinco de la tarde, atracan en Barcelona.")
b("Según la revista Time, una multitud sube a bordo y algunas mujeres se desmayan. Cada uno había pasado entre diez y dieciséis años en campos soviéticos.")
b("En el puerto los recibe el general Muñoz Grandes, antiguo jefe de la División Azul. Según Time, en los campos quedaban todavía unos doscientos españoles. Y el Gulag aún no tenía el libro que lo haría famoso.", ideia=True)

# ───────────────────────── 11. LA ENTREVISTA ─────────────────────────
cap("11. La Entrevista")
b("La Entrevista. Madrid, marzo de mil novecientos setenta y seis. Franco ha muerto hace cuatro meses. En el programa Directísimo, de Televisión Española, José María Íñigo entrevista a un escritor ruso expulsado de su país: Alexandr Solzhenitsyn.", card="MADRID, 1976")
b("Su Archipiélago Gulag había salido en París en mil novecientos setenta y tres, y en español al año siguiente. En México, Octavio Paz lo defendió en la revista Plural.")
b("Para entonces, el Gulag ya no existía con ese nombre: una orden de enero de mil novecientos sesenta lo había disuelto.")
b("En el estudio, Solzhenitsyn les dice a los españoles, textualmente: «Vosotros no sabéis qué es el comunismo». Parte de la prensa de izquierda lo ataca. El novelista Juan Marsé lo llama «chorizo de las letras»: ladrón de las letras.")
b("De los españoles que volvieron en mil novecientos cincuenta y cuatro quedaba otra prueba, más callada: unas fotos.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. Las Fotos")
b("Las Fotos. Barcelona, dos de abril de mil novecientos cincuenta y cuatro. En el muelle, entre la multitud, el fotógrafo Carlos Pérez de Rozas retrata a los que bajan del Semíramis.", card="BARCELONA, 1954")
b("Hoy esas fotos están en el Archivo Fotográfico de Barcelona. Muestran a los que volvieron, hombres de los dos bandos, bajando del mismo barco.")
b("Siete décadas después, en dos mil veinticinco, un libro reconstruye el destino de los marineros republicanos en los campos soviéticos.")
b("Los historiadores discuten si el Gulag buscaba culpables o brazos. Sus papeles contaban brazos. Y los encontró en todas partes: entre sus enemigos, entre sus aliados y entre los que solo querían volver a casa.", ideia=True)
b("Y tú, ¿sabías que hubo españoles en el Gulag? ¿Conoces alguna historia así en tu familia? Déjalo en los comentarios.")

# ───────────────────────── STORYBOARD (planos por bloco, na ordem dos blocos) ─────────────────────────
SB = []
THUMBS = []

_textos = [x for x in B if "t" in x]
if SB:
    assert len(SB) == len(_textos), f"SB {len(SB)} x blocos {len(_textos)}"
    for _blk, _s in zip(_textos, SB): _blk["s"] = _s

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
