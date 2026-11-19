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
b("Washington, veintisiete de octubre de mil novecientos cuarenta y uno. Roosevelt habla por radio a todo el país.", card="WASHINGTON, 1941")
b("Dice tener un mapa secreto, hecho en Alemania por el gobierno de Hitler. Catorce países de Sudamérica y Centroamérica quedan en cinco estados vasallos. Uno, con el canal de Panamá.")
b("Berlín lo llama falsificación. Según los historiadores, tenía razón: el mapa salió de una oficina británica en Nueva York.")
b("Esta es TODA la historia del MI6. Y de los papeles con que movió el mundo.", ideia=True)

# ───────────────────────── 1. EL DIARIO ─────────────────────────
cap("1. El Diario")
b("El Diario. Londres, octubre de mil novecientos nueve. El gobierno británico, preocupado por los espías alemanes, crea una pequeña Oficina del Servicio Secreto. La sección que vigila dentro del país será el MI5. La que espía fuera, el MI6.", card="LONDRES, 1909")
b("La sección exterior la recibe un capitán de la Marina, Mansfield Cumming. No tiene agentes, ni dinero, ni instrucciones.")
b("El siete de octubre anota en su diario su primer día de trabajo: fue a la oficina, se quedó todo el día, no vio a nadie y no había nada que hacer.")
b("El primer papel del servicio secreto más famoso del mundo es una página vacía. Ocho años después, otro papel cambia una guerra. Y no lo consigue el MI6.", ideia=True)

# ───────────────────────── 2. EL TELEGRAMA ─────────────────────────
cap("2. El Telegrama")
b("El Telegrama. Enero de mil novecientos diecisiete. Berlín envía un mensaje cifrado a su embajador en México. Si Estados Unidos entra en la guerra, Alemania ofrece a México una alianza, dinero y recuperar Texas, Nuevo México y Arizona.", card="MÉXICO, 1917")
b("Lo descifran en Londres, en la Sala Cuarenta de la Marina británica, no en la oficina de Cumming. Para no revelar que leen los cables alemanes, consiguen una copia en la oficina de telégrafos de Ciudad de México.")
b("El primero de marzo, el telegrama sale en la prensa estadounidense. Dos días después, el ministro alemán Arthur Zimmermann admite que es auténtico. En abril, Estados Unidos entra en la guerra. No fue la única razón, pero pesó.")
b("Los espías británicos aprenden la lección: un papel llegado desde México puede mover a Washington. Antes de usarla, otro papel les estalla en casa.", ideia=True)

# ───────────────────────── 3. LA CARTA ─────────────────────────
cap("3. La Carta")
b("La Carta. Riga, otoño de mil novecientos veinticuatro. La estación del MI6 en Letonia envía a Londres la copia de una carta firmada por Grigori Zinóviev, jefe de la Internacional Comunista.", card="RIGA, 1924")
b("La carta pide a los comunistas británicos preparar la revolución. Llega en plena campaña electoral, con un gobierno laborista que acaba de firmar tratados con Moscú.")
b("El veinticinco de octubre, el Daily Mail la publica en portada. Moscú dice que es falsa. Cuatro días después, los laboristas pierden las elecciones.")
b("En mil novecientos noventa y nueve, un informe del Ministerio de Exteriores concluyó que la carta era, muy probablemente, obra de exiliados rusos. Y que es probable que oficiales de los servicios secretos la filtraran a la oposición y a la prensa.")
b("Un país votó con un papel falso sobre la mesa. Dieciséis años después, el MI6 ya no espera a que otros lo fabriquen.", ideia=True)

# ───────────────────────── 4. EL PASAPORTE ─────────────────────────
cap("4. El Pasaporte")
b("El Pasaporte. Nueva York, junio de mil novecientos cuarenta. Llega un millonario canadiense, William Stephenson, antiguo piloto de la Primera Guerra Mundial. Su cargo es modesto: oficial de control de pasaportes.", card="NUEVA YORK, 1940")
b("Es la tapadera clásica del MI6 en el extranjero. Un año antes, su oficina en Nueva York tenía nueve empleados. Stephenson la convierte en la Coordinación de Seguridad Británica, la BSC, con cientos de personas en la sala tres mil seiscientos tres del Rockefeller Center.")
b("Gran Bretaña está sola frente a Hitler. Estados Unidos es neutral y la mayoría de sus ciudadanos no quiere la guerra. La BSC tiene dos misiones: cazar agentes nazis en América y empujar a Washington hacia la guerra.")
b("Para las dos necesita papeles. Y muchos de los papeles del continente pasan por una isla.", ideia=True)

# ───────────────────────── 5. LA ISLA ─────────────────────────
cap("5. La Isla")
b("La Isla. Bermudas, mil novecientos cuarenta y uno. En el hotel Princess de Hamilton, cerca de mil censores británicos abren las cartas que viajan entre América y Europa.", card="BERMUDAS, 1941")
b("Hidroaviones y barcos hacen escala en la isla. Cada saca de correo se abre, se lee y se vuelve a cerrar; algunas cartas pasan por pruebas químicas, en busca de tinta invisible.")
b("Una censora, Nadya Gardner, sospecha de unas cartas firmadas por un tal Joe K, enviadas desde Nueva York, y propone probarlas con yodo. Aparece una escritura oculta sobre barcos y aviones. La pista lleva al FBI hasta la red de Kurt Ludwig, detenido en agosto.")
b("La censura de Bermudas no solo caza espías. También guarda copias de cartas auténticas. Según la propia BSC, una de ellas, la de un militar boliviano, servirá de modelo.", ideia=True)

# ───────────────────────── 6. LA FIRMA ─────────────────────────
cap("6. La Firma")
b("La Firma. La Paz, julio de mil novecientos cuarenta y uno. El gobierno del general Peñaranda recibe, a través del embajador de Estados Unidos, una carta.", card="LA PAZ, 1941")
b("La firma el mayor Elías Belmonte, agregado aéreo de Bolivia en Berlín, y va dirigida al ministro alemán en La Paz, Ernst Wendler. Dice que se acerca el momento de dar el golpe.")
b("Bolivia declara el estado de sitio, cierra periódicos, detiene a políticos y expulsa al ministro alemán.")
b("Veinte años después, un antiguo oficial de la BSC, Montgomery Hyde, contó su versión: la carta era falsa, fabricada en un laboratorio británico de Toronto con una máquina de escribir construida para imitar la de Belmonte.")
b("En dos mil veinticuatro, un estudio académico puso en duda esa versión: no halló pruebas en los archivos. Lo que nadie discute es lo que pasó en La Paz. Tres meses después, Toronto entrega otro papel.", ideia=True)

# ───────────────────────── 7. EL MAPA ─────────────────────────
cap("7. El Mapa")
b("El Mapa. Toronto, otoño de mil novecientos cuarenta y uno. El laboratorio se llama Estación M y lo dirige un letrista de canciones, Eric Maschwitz.", card="TORONTO, 1941")
b("Según el museo de la inteligencia militar británica, la idea fue de un agente de la BSC, Ivar Bryce. El mapa se fabrica en dos días: envejecido, manchado como si hubiera viajado, con tintas como las alemanas. Llega a Roosevelt por medio del director del FBI.")
b("¿Lo sabía Roosevelt? Según el historiador Nicholas Cull, en un borrador del discurso tachó una frase: un mapa de autenticidad indudable. En la radio dijo solo: un mapa secreto. Nadie sabe si fue engañado o si solo dudaba.")
b("Berlín lo negó. Después de la guerra, en los archivos alemanes capturados no apareció ningún mapa así. El complot nazi para Sudamérica no existía.")
b("Cuarenta y un días después, Japón ataca Pearl Harbor.", ideia=True)
b("Si este expediente te está gustando, suscríbete. Porque ese mismo otoño, la BSC apunta su siguiente papel contra Brasil.")

# ───────────────────────── 8. LA AEROLÍNEA ─────────────────────────
cap("8. La Aerolínea")
b("La Aerolínea. Río de Janeiro, fines de mil novecientos cuarenta y uno. La aerolínea italiana LATI une Roma con Brasil. Para Londres y Washington, transporta agentes, valijas diplomáticas y mercancías del Eje.", card="RÍO DE JANEIRO, 1941")
b("La compañía tiene amigos en el gobierno de Getúlio Vargas, así que las quejas oficiales no sirven. Según la propia BSC, sus agentes fabrican una carta de la dirección de LATI que insulta al presidente Vargas, y hacen que llegue a sus manos.")
b("En diciembre, tras Pearl Harbor y con la presión de Estados Unidos, Vargas ordena expropiar LATI y la alemana Cóndor. La carta no fue la única razón. Pero la BSC se la apuntó.")
b("Estados Unidos ya está en guerra: lo llevó Pearl Harbor, no los papeles de la BSC. Y mientras el MI6 fabrica papeles para engañar a otros, el engaño ya está dentro de su propia casa.", ideia=True)

# ───────────────────────── 9. EL COMUNICADO ─────────────────────────
cap("9. El Comunicado")
b("El Comunicado. Londres, siete de noviembre de mil novecientos cincuenta y cinco. En la Cámara de los Comunes, el ministro de Exteriores, Harold Macmillan, lee una declaración sobre un antiguo oficial del MI6.", card="LONDRES, 1955")
b("No tengo razones, dice, para concluir que el señor Philby haya traicionado nunca los intereses de este país.")
b("El señor Philby es Kim Philby. La inteligencia soviética lo reclutó en mil novecientos treinta y cuatro. Desde mil novecientos cuarenta y cuatro dirigió la sección del MI6 que debía combatir a los soviéticos.")
b("En mil novecientos cincuenta y uno, dos diplomáticos amigos suyos huyeron a Moscú y las sospechas cayeron sobre él. El papel de Macmillan lo limpia en público. En enero de mil novecientos sesenta y tres, desde Beirut, Philby huye a la Unión Soviética.")
b("El servicio que engañaba a otros con papeles estaba engañado por dentro. Y antes de la fuga de Philby, el MI6 ya había tenido que hacer desaparecer otro papel.", ideia=True)

# ───────────────────────── 10. EL REGISTRO ─────────────────────────
cap("10. El Registro")
b("El Registro. Portsmouth, abril de mil novecientos cincuenta y seis. El crucero soviético Ordzhonikidze trae a Nikita Jrushchov de visita oficial a Gran Bretaña. El gobierno de Anthony Eden quiere que nada la estropee.", card="PORTSMOUTH, 1956")
b("El diecinueve de abril, un buzo veterano, el comandante Lionel Crabb, se sumerge en el puerto para examinar el casco del crucero en una misión del MI6. No vuelve a salir.")
b("Del libro de registro de su hotel desaparecen las páginas con su nombre y el de su acompañante. El Almirantado anuncia que se perdió durante unas pruebas de equipo submarino.")
b("Moscú protesta. Eden dice en privado que la operación se hizo contra sus órdenes, y poco después el jefe del MI6 es reemplazado. Los documentos del caso no se abrieron hasta dos mil seis.")
b("Ahora el MI6 arranca páginas para protegerse. Veintiséis años después, el papel que falla es un aviso.", ideia=True)

# ───────────────────────── 11. EL MISIL ─────────────────────────
cap("11. El Misil")
b("El Misil. Londres, julio de mil novecientos ochenta y uno. El Comité Conjunto de Inteligencia, que reúne lo que saben el MI6 y los demás servicios, escribe que no se puede descartar una invasión argentina de las Malvinas.", card="LONDRES, 1981")
b("El dos de abril de mil novecientos ochenta y dos, tropas argentinas desembarcan en las islas. Al año siguiente, un informe oficial, el informe Franks, concluye que no se puede culpar al gobierno de Margaret Thatcher por no haberlo previsto.", card="MALVINAS, 1982")
b("En la guerra, lo que más preocupa a Londres es el misil francés Exocet. Argentina tiene pocos y busca más. Según la historia oficial de Lawrence Freedman, agentes británicos se hacen pasar por compradores en el mercado de armas para quedarse con los misiles antes que Argentina.")
b("Según Londres, Argentina no consiguió más Exocet durante la guerra. En setenta y cuatro días, el conflicto dejó más de novecientos caídos entre argentinos, británicos e isleños.")
b("Esta vez el engaño fueron identidades falsas, no documentos. Veinte años después, un papel de los servicios británicos ayuda a llevar a su país a otra guerra.", ideia=True)

# ───────────────────────── 12. EL INFORME ─────────────────────────
cap("12. El Informe")
b("El Informe. Londres, seis de julio de dos mil dieciséis. Tras siete años de investigación, John Chilcot presenta su informe sobre la participación británica en la guerra de Irak de dos mil tres.", card="LONDRES, 2016")
b("Concluye que las afirmaciones sobre las armas de destrucción masiva de Sadam Husein se presentaron con una certeza que no estaba justificada. Parte de los informes del MI6 venía de fuentes poco comprobadas, y algunos se retiraron después.")
b("Las armas nunca aparecieron.")
b("Como en mil novecientos diecisiete y en mil novecientos cuarenta y uno, un papel ayudó a empujar a un país a la guerra. Pero esta vez, el país engañado era el suyo.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. El Mapa")
b("El Mapa. Hoy el MI6 tiene página web y publica ofertas de empleo. Su existencia no se reconoció oficialmente hasta mil novecientos noventa y dos. En dos mil veinticinco, por primera vez, lo dirige una mujer.", card="LONDRES, HOY")
b("El mapa de Roosevelt apareció décadas después entre sus papeles privados. Alemania nunca lo dibujó. Según los historiadores, salió de una oficina de pasaportes en Nueva York y de un laboratorio en Toronto.")
b("En más de un siglo, el MI6 robó secretos, como cualquier servicio. Pero muchos de sus golpes más famosos fueron papeles: los que escribió, los que filtró y los que hizo desaparecer.")
b("Un espía roba documentos. El MI6 aprendió algo más útil: a escribirlos.", ideia=True)
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
