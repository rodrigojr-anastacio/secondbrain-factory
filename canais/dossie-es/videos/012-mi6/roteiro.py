#!/usr/bin/env python3
"""Fonte única do dossie-es 012 (El MI6): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (na pasta do vídeo). Conteúdo no topo; geração no fim (copiada do 011-templarios).

Embalagem aprovada no crivo r3 (18/11/2026, EMBALAGEM.md/CRIVO.md):
  A/T1 "MI6: el plan nazi para Sudamérica que nadie escribió en Berlín" + máquina de escrever no escuro, sello NUEVA YORK (objeto-simbolo, controle)
  B/T2 "Cómo el MI6 engañó a un presidente, a un país y a sí mismo" + rosto de Roosevelt aos microfones, folha riscada, ¿SABÍA? (rosto-emocao, TESTE personagem)
  C/T3 "El Complot Nazi que Nunca Existió | Expedientes Secretos del MI6" + o mapa em 5 blocos sendo traçado, 14 → 5 (mapa-lugar)
  Frase-âncora do hook: "Esta es TODA la historia del MI6. Y de los papeles con que movió el mundo."
Ângulo (ANGULO.md): a história inteira contada pelos papéis que o MI6 fabricou, vazou ou fez sumir; miolo nas Américas (BSC 1940–41).
Fora da manada: El Diario, El Telegrama, La Carta (Zinoviev), El Pasaporte, La Isla, La Firma, El Mapa, La Aerolínea, El Registro, El Misil.
Fatos obrigatórios da manada (1909, Philby, Iraque/Chilcot, 1992) só como contexto curto, nunca como cena principal na ordem deles.

Sintaxe dos planos (campo s):
  "chave|prompt"   imagem nova (id I### na ordem de aparição) · "chave" reuso · "chave#enq" reuso com enquadramento
  + "@@TEXTO"      rótulo na tela (máquina de escrever; CAIXA ALTA, até ~28 caracteres)
Bloco: b(texto, *planos, card="WASHINGTON, 1941", ideia=True) · capítulo: cap("5. La Isla")
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
HOOK_MAX = 36.0      # s: a bíblia pede hook de 25–35 s (EMBALAGEM: frase-âncora até 0:35)
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "MI6: el plan nazi para Sudamérica que nadie escribió en Berlín"
TITULOS = ("T1 MI6: el plan nazi para Sudamérica que nadie escribió en Berlín / "
           "T2 Cómo el MI6 engañó a un presidente, a un país y a sí mismo / "
           "T3 El Complot Nazi que Nunca Existió | Expedientes Secretos del MI6")
PROMESSA = ("Toda la historia del MI6 contada por los papeles que fabricó, filtró o hizo desaparecer, empezando por el plan "
            "nazi para Sudamérica que Roosevelt anunció por radio en 1941 y que, según los historiadores, salió de una "
            "oficina británica en Nueva York.")

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Washington, veintisiete de octubre de mil novecientos cuarenta y uno. El presidente Roosevelt habla por radio al país.", card="WASHINGTON, 1941")
b("Dice tener un mapa secreto, hecho en Alemania por el gobierno de Hitler. Catorce países de Sudamérica y Centroamérica se reducen a cinco estados vasallos. Uno incluye el canal de Panamá.")
b("Berlín lo llama falsificación. Según los historiadores, lo era: el mapa salió de una oficina británica en Nueva York.")
b("Esta es TODA la historia del MI6. Y de los papeles con que movió el mundo.", ideia=True)

# ───────────────────────── 1. EL DIARIO ─────────────────────────
cap("1. El Diario")
b("El Diario. Londres, siete de octubre de mil novecientos nueve. Un oficial de la Armada, Mansfield Cumming, anota en su diario su primer día completo de trabajo.", card="LONDRES, 1909")
b("Fue a la oficina, se quedó todo el día, no vio a nadie y no había nada que hacer.")
b("Cumming dirige la sección exterior de una nueva Oficina del Servicio Secreto, creada por un gobierno preocupado por los espías alemanes. La sección interior será el MI5. La suya, el MI6. Casi no tiene personal ni presupuesto.")
b("El servicio secreto más famoso del mundo nace casi con una página en blanco. Siete años después, un papel cambia una guerra. Y no es obra del MI6.", ideia=True)

# ───────────────────────── 2. EL TELEGRAMA ─────────────────────────
cap("2. El Telegrama")
b("El Telegrama. Enero de mil novecientos diecisiete. Berlín envía un mensaje cifrado a su representante en México, a través de su embajada en Washington. Propone a México una alianza si Estados Unidos entra en la guerra.", card="MÉXICO, 1917")
b("A cambio, dinero y ayuda para recuperar Texas, Nuevo México y Arizona. Lo descifran en Londres, en la Sala Cuarenta de la Armada británica, no en la oficina de Cumming.")
b("Para ocultar que leen los telegramas alemanes, consiguen una copia en Ciudad de México. El primero de marzo, el telegrama sale en la prensa estadounidense.")
b("Dos días después, el jefe de la diplomacia alemana, Arthur Zimmermann, admite que es auténtico. En abril, Estados Unidos entra en la guerra. No fue la única razón, pero pesó.")
b("En Londres queda la lección: un papel bien colocado puede mover a Washington. Antes de aplicarla, otro papel les estalla en las manos.", ideia=True)

# ───────────────────────── 3. LA CARTA ─────────────────────────
cap("3. La Carta")
b("La Carta. Riga, otoño de mil novecientos veinticuatro. La delegación del MI6 en Letonia envía a Londres la copia de una carta atribuida a Grigori Zinóviev, jefe de la Internacional Comunista.", card="RIGA, 1924")
b("La carta pide a los comunistas británicos preparar la revolución. Llega en plena campaña electoral, con un gobierno laborista que acaba de firmar tratados con Moscú.")
b("El veinticinco de octubre, el diario Daily Mail la publica en portada. Moscú dice que es falsa. Cuatro días después, los laboristas pierden las elecciones.")
b("En mil novecientos noventa y nueve, la historiadora del Foreign Office Gill Bennett concluyó que es imposible saber quién la escribió. Lo más probable, según ella, es que la encargaran exiliados rusos.")
b("Y que oficiales de los servicios secretos británicos la filtraran a los conservadores y a la prensa. Un país votó con un papel falso sobre la mesa.", ideia=True)

# ───────────────────────── 4. EL PASAPORTE ─────────────────────────
cap("4. El Pasaporte")
b("El Pasaporte. Nueva York, junio de mil novecientos cuarenta. Llega un millonario canadiense, William Stephenson, piloto en la Primera Guerra Mundial. Su cargo es modesto: oficial de control de pasaportes.", card="NUEVA YORK, 1940")
b("Es la cobertura clásica del MI6 en el extranjero. Meses antes, esa oficina tenía nueve personas. Stephenson la convierte en la Coordinación de Seguridad Británica, la BSC.")
b("Cientos de personas trabajan para ella desde la oficina tres mil seiscientos tres del Rockefeller Center. Gran Bretaña está sola frente a Hitler. Estados Unidos es neutral.")
b("Según su propia historia interna, la BSC tiene dos misiones: localizar agentes nazis en el continente y lograr que Washington entre en la guerra.")
b("Para cumplir las dos misiones necesita papeles. Y muchos de los que cruzan el Atlántico pasan por una isla.", ideia=True)

# ───────────────────────── 5. LA ISLA ─────────────────────────
cap("5. La Isla")
b("La Isla. Bermudas, mil novecientos cuarenta y uno. En el hotel Princess de Hamilton, cerca de mil censores británicos abren las cartas que viajan entre América y Europa.", card="BERMUDAS, 1941")
b("Cada bolsa de correo que hace escala en la isla se abre, se lee y se vuelve a cerrar. Algunas cartas pasan por pruebas químicas.")
b("Según el oficial de la BSC Montgomery Hyde, una censora, Nadya Gardner, sospecha de unas cartas firmadas por un tal Joe K. Propone probarlas con yodo. Aparece una escritura oculta sobre barcos y aviones.")
b("Las cartas pasan al FBI. En agosto cae en Estados Unidos la red de espías de Kurt Ludwig.")
b("La censura no solo caza espías. También guarda copias de cartas auténticas. Según el propio Hyde, una de ellas, la de un militar boliviano, servirá de modelo.", ideia=True)

# ───────────────────────── 6. LA FIRMA ─────────────────────────
cap("6. La Firma")
b("La Firma. La Paz, julio de mil novecientos cuarenta y uno. El gobierno del general Peñaranda recibe una carta por medio del representante de Estados Unidos.", card="LA PAZ, 1941")
b("Aparece firmada por el mayor Elías Belmonte, agregado aéreo de Bolivia en Berlín, y dirigida al representante alemán en La Paz, Ernst Wendler. Según la carta, se acerca el momento de dar un golpe de Estado.")
b("El gobierno boliviano declara el estado de sitio, cierra periódicos, detiene a dirigentes políticos y expulsa al diplomático alemán.")
b("En mil novecientos sesenta y dos, Hyde contó su versión: la carta era falsa, obra de los británicos. Relatos posteriores añaden un laboratorio en Toronto y una máquina de escribir hecha para imitar la de Belmonte.")
b("En dos mil veinticuatro, un estudio académico la puso en duda: no encontró pruebas en los archivos. Tres meses después, otro papel sale de Toronto.", ideia=True)

# ───────────────────────── 7. EL MAPA ─────────────────────────
cap("7. El Mapa")
b("El Mapa. Toronto, otoño de mil novecientos cuarenta y uno. Según el museo de la inteligencia militar británica, allí funciona un laboratorio secreto, la Estación M, dirigido por un autor de canciones, Eric Maschwitz.", card="TORONTO, 1941")
b("Según la misma fuente, la idea fue de un agente de la BSC, Ivar Bryce. El mapa se fabrica en dos días, envejecido y manchado como si hubiera viajado, y llega a Roosevelt a través del director del FBI.")
b("¿Lo sabía Roosevelt? Según el historiador Nicholas Cull, en un borrador del discurso tachó la frase que decía: un mapa de autenticidad indudable. Por radio dijo únicamente: un mapa secreto. Nadie sabe si fue engañado o si solo dudaba.")
b("Berlín lo niega. Después de la guerra, en los archivos alemanes capturados no aparece ningún mapa así. No hay rastro de ese complot nazi para Sudamérica: según los historiadores, nunca existió.")
b("Cuarenta y un días después del discurso, Japón ataca Pearl Harbor.", ideia=True)
b("Si te está gustando este expediente, suscríbete. Porque ese mismo año, la BSC dirige otro papel contra Brasil.")

# ───────────────────────── 8. LA AEROLÍNEA ─────────────────────────
cap("8. La Aerolínea")
b("La Aerolínea. Río de Janeiro, finales de mil novecientos cuarenta y uno. La aerolínea italiana LATI une Roma con Brasil. Según Londres y Washington, transporta agentes, valijas diplomáticas y mercancías del Eje.", card="RÍO DE JANEIRO, 1941")
b("La compañía tiene aliados en el gobierno de Getúlio Vargas, así que las quejas oficiales no funcionan. Según la propia BSC, sus agentes fabrican una carta de la dirección de LATI que insulta al presidente Vargas. Y logran que le llegue.")
b("En diciembre, tras Pearl Harbor y con la presión de Estados Unidos, Vargas ordena expropiar LATI y la compañía alemana Cóndor. La carta no fue la única razón. Pero la BSC se atribuyó el mérito.")
b("Estados Unidos ya está en guerra, pero por Pearl Harbor, no por los papeles de la BSC. Y mientras el MI6 fabrica papeles para engañar a otros, una traición crece dentro de su propia casa.", ideia=True)

# ───────────────────────── 9. EL COMUNICADO ─────────────────────────
cap("9. El Comunicado")
b("El Comunicado. Londres, siete de noviembre de mil novecientos cincuenta y cinco. En la Cámara de los Comunes, el jefe de la diplomacia británica, Harold Macmillan, habla de un antiguo oficial del MI6.", card="LONDRES, 1955")
b("No tengo razones, dice, para concluir que el señor Philby haya traicionado nunca los intereses de este país.")
b("El señor Philby es Kim Philby. La inteligencia soviética lo reclutó en mil novecientos treinta y cuatro. Desde mil novecientos cuarenta y cuatro dirigió la sección del MI6 que debía combatir a los soviéticos.")
b("En mil novecientos cincuenta y uno, dos diplomáticos amigos suyos huyen a Moscú y las sospechas caen sobre él. El papel de Macmillan lo exculpa en público. En enero de mil novecientos sesenta y tres, desde Beirut, Philby huye a la Unión Soviética.")
b("El servicio que engañaba a otros con papeles estaba engañado por dentro. Y al año siguiente del comunicado, otro papel desaparece para proteger al servicio.", ideia=True)

# ───────────────────────── 10. EL REGISTRO ─────────────────────────
cap("10. El Registro")
b("El Registro. Portsmouth, abril de mil novecientos cincuenta y seis. El crucero soviético Ordzhonikidze llega con Nikita Jruschov y Nikolái Bulganin, en visita oficial a Gran Bretaña. El gobierno de Anthony Eden quiere que nada la arruine.", card="PORTSMOUTH, 1956")
b("El diecinueve de abril, un buzo veterano, el comandante Lionel Crabb, se sumerge en el puerto para examinar el casco del crucero, en una misión del MI6. No vuelve a la superficie.")
b("Del libro de registro de su hotel desaparecen las páginas con su nombre y el del hombre que lo acompañaba. El Almirantado anuncia que no regresó de unas pruebas de equipo submarino.")
b("Moscú protesta. Eden dice en privado que la operación se hizo sin su autorización. Los primeros documentos del caso no se hicieron públicos hasta dos mil seis.")
b("Ahora, para proteger al servicio, alguien arranca páginas. Veinticinco años después, el papel que fracasa es una advertencia.", ideia=True)

# ───────────────────────── 11. EL MISIL ─────────────────────────
cap("11. El Misil")
b("El Misil. Londres, julio de mil novecientos ochenta y uno. El Comité Conjunto de Inteligencia, que reúne lo que saben el MI6 y los demás servicios, escribe que no se puede descartar un intento argentino de tomar las Malvinas por la fuerza.", card="LONDRES, 1981")
b("El dos de abril de mil novecientos ochenta y dos, tropas argentinas desembarcan en las islas. Un año después, el informe oficial Franks no culpa al gobierno de Margaret Thatcher por la decisión argentina.", card="MALVINAS, 1982")
b("En la guerra, lo que más preocupa a Londres es el misil francés Exocet. Argentina tiene pocos y busca más. Según el historiador Lawrence Freedman, que escribió por encargo del gobierno británico, agentes británicos se hacen pasar por compradores en el mercado de armas, para que Argentina no consiga más.")
b("Según Londres, no los consiguió. En setenta y cuatro días, el conflicto dejó más de novecientos muertos entre argentinos, británicos y habitantes de las islas.")
b("Esta vez el engaño no fue de documentos, sino de identidades falsas. Veinte años después, un dossier del gobierno británico, apoyado en informes del MI6, ayuda a llevar a su país a otra guerra.", ideia=True)

# ───────────────────────── 12. EL INFORME ─────────────────────────
cap("12. El Informe")
b("El Informe. Londres, seis de julio de dos mil dieciséis. Tras siete años de investigación, John Chilcot presenta su informe sobre la participación británica en la guerra de Irak, que empezó en dos mil tres.", card="LONDRES, 2016")
b("Concluye que lo que se afirmaba sobre las armas de destrucción masiva de Sadam Husein se presentó con una certeza injustificada. Parte de los informes del MI6 venía de fuentes poco comprobadas. Algunos se retiraron después.")
b("Las armas nunca aparecieron.")
b("Como en mil novecientos diecisiete y en mil novecientos cuarenta y uno, un papel pesó en una decisión de guerra. Pero esta vez, el país convencido con certezas injustificadas era el propio.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. El Mapa")
b("El Mapa. Hoy el MI6 tiene página web y publica ofertas de empleo. Su existencia no se reconoció oficialmente hasta mil novecientos noventa y dos. En dos mil veinticinco, por primera vez, lo dirige una mujer.", card="LONDRES, HOY")
b("Del mapa de Roosevelt no hay rastro en los archivos alemanes. Según los historiadores, salió de la inteligencia británica en Nueva York. Según el museo militar británico, de un laboratorio en Toronto.")
b("En más de un siglo, el MI6 robó secretos, como cualquier servicio. Pero muchas de sus historias más conocidas giran en torno a papeles: los que escribió, los que filtró y los que hizo desaparecer.")
b("Un espía roba documentos. En estos expedientes, el MI6 aprendió algo más útil: a escribirlos.", ideia=True)
b("Y tú, ¿crees que hoy un documento falso todavía podría cambiar una guerra? Déjalo en los comentarios.")

# ───────────────────────── STORYBOARD (planos por bloco, na ordem dos blocos) ─────────────────────────
SB = []
_textos = [x for x in B if "t" in x]
if SB:
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
