#!/usr/bin/env python3
"""Fonte única do dossie-es 016 (MKUltra): roteiro + planos. Gera SCRIPT.md, blocos.json e, quando o storyboard
estiver preenchido (SB/THUMBS), cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py (na pasta do vídeo). Maquinaria de geração copiada do 015-gru (que veio do 014-yakuza).

Embalagem aprovada no crivo r5 (24/11/2026, EMBALAGEM.md/CRIVO.md):
  A/T1 "TODA la historia de MKUltra en 13 minutos | Del laboratorio de la CIA a América Latina" + cogumelos e vela + MKULTRA (objeto-simbolo, controle)
  B/T2 "Cómo la CIA buscó en América Latina la droga del control mental" + cientista com saco de piule + "10 LIBRAS" (cena-acao)
  C/T3 "MKULTRA: lo que la CIA vino a buscar a México… y lo que dejó" + "stress" riscado/"deplore" sobre bandeira de Honduras (documento-evidencia)
Ângulo (ANGULO.md): lo que la CIA vino a buscar a América Latina (semillas 1952, hongos 1955–56, selva 1966) y lo que dejó (químicos contra Castro 1960–61, curso y manual de Honduras 1983–97).

Sintaxe dos planos (campo s): "chave|prompt" nova · "chave" reuso · "chave#enq" reuso com enquadramento · + "@@TEXTO" rótulo.
ROTEIRO v1 (24/11/2026): planos ainda NÃO feitos (SB = [] e THUMBS = []): a etapa storyboard preenche.
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
HOOK_MAX = 50.0      # s: EMBALAGEM: frase-âncora ≤ 0:35 e linha de promessa (último bloco do hook) ≤ 0:50
ANCORA_MAX = 35.0    # s: fim do bloco da frase-âncora
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "TODA la historia de MKUltra en 13 minutos | Del laboratorio de la CIA a América Latina"
TITULOS = ("T1 TODA la historia de MKUltra en 13 minutos | Del laboratorio de la CIA a América Latina / "
           "T2 Cómo la CIA buscó en América Latina la droga del control mental / "
           "T3 MKULTRA: lo que la CIA vino a buscar a México… y lo que dejó")
PROMESSA = ("La historia entera de MKUltra contada por lo que la CIA vino a buscar a América Latina (las semillas de México, "
            "los hongos de Huautla, las plantas de la Amazonía, los químicos que preparó para Fidel Castro) y por lo que dejó "
            "(un método de interrogatorio en un manual usado en Honduras, corregido a mano).")

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Huautla de Jiménez, Oaxaca, verano de mil novecientos cincuenta y seis. Es de noche. María Sabina canta en mazateco.", card="HUAUTLA, 1956")
b("Los hongos pasan de mano en mano. Un químico de Delaware los mastica. No siente éxtasis. Dirá después que se sintió desorientado.")
b("Se llama James Moore. Y desde hace tres años trabaja bajo contrato para la CIA.")
b("Esta es TODA la historia de MKUltra. De lo que la CIA vino a buscar a América Latina… y de lo que dejó.", ideia=True)
b("Las semillas de México, los hongos de Huautla, los químicos que preparó para Fidel Castro y un manual en Honduras.")

# ───────────────────────── 1. LAS SEMILLAS ─────────────────────────
cap("1. Las Semillas")
b("Las Semillas. Washington, octubre de mil novecientos cincuenta y dos. A la CIA le aterra una idea que llega de la guerra de Corea: el lavado de cerebro.", card="WASHINGTON, 1952", ideia=True)
b("Para defenderse, y tener su propia arma, crea el proyecto Bluebird, luego llamado Artichoke. Su jefe, Morse Allen, oye en una reunión el nombre de un arbusto mexicano: el piule.")
b("Pueblos indígenas usan sus semillas en ceremonias religiosas. Allen envía a México a un joven científico de la agencia, cuyo nombre no aparece en los papeles publicados.")
b("Llega entre diciembre de mil novecientos cincuenta y dos y comienzos del cincuenta y tres. Se hace pasar por investigador de plantas anestésicas. Prueba muestras en la sierra, al sur de la capital.", card="MÉXICO, 1953")
b("En febrero ya tiene sacos llenos. Según el periodista John Marks, entre ellos, diez libras de piule.")
b("Antes de irse, oye hablar de unos hongos especiales que solo salen con las lluvias del verano.", ideia=True)

# ───────────────────────── 2. LA GRANJA ─────────────────────────
cap("2. La Granja")
b("La Granja. Pensilvania, veinticuatro de junio de mil novecientos cincuenta y tres. Morse Allen visita Toughkenamon, la mayor zona productora de champiñones del mundo.", card="PENSILVANIA, 1953", ideia=True)
b("En abril, el director Allen Dulles había aprobado un programa nuevo, con dinero fuera de la contabilidad normal: MKUltra.")
b("A los productores no les gusta cultivar hongos tóxicos: perderían clientes. Pero, según Marks, el patriotismo gana. Cultivarán el hongo que pida el gobierno.")
b("Dos días después, Allen firma un memorando: Hongos, variedades narcóticas y venenosas. Ya hay presupuesto y granja. Falta el hongo.")
b("En noviembre, la CIA pone LSD, sin avisarle, en la copa de licor de Frank Olson, científico del Ejército. Nueve días después, Olson cae desde el décimo piso de un hotel de Nueva York.", ideia=True)

# ───────────────────────── 3. LA VELADA ─────────────────────────
cap("3. La Velada")
b("La Velada. Huautla, veintinueve de junio de mil novecientos cincuenta y cinco. Un banquero de Nueva York entra de noche en una casa de adobe.", card="HUAUTLA, 1955", ideia=True)
b("Es Robert Gordon Wasson, vicepresidente de J. P. Morgan y aficionado a los hongos. Con él, un fotógrafo y una veintena de mazatecos. María Sabina dirige la ceremonia.")
b("Wasson se describirá como uno de los primeros hombres blancos en comer los hongos sagrados. Ella los llama los niños santos.")
b("Wasson viaja por su cuenta. Pero un botánico de la Ciudad de México envía un informe del viaje. Según Marks, llega a la sede de la CIA… y a un químico que cobra de la agencia.", ideia=True)

# ───────────────────────── 4. LA BOLSA ─────────────────────────
cap("4. La Bolsa")
b("La Bolsa. Delaware, mil novecientos cincuenta y seis. James Moore le escribe a Wasson una carta que, según el banquero, llega de la nada.", card="DELAWARE, 1956", ideia=True)
b("Quiere estudiar los hongos mexicanos. Y conoce, dice, una fundación que podría ayudar. El Fondo Geschickter aporta dos mil dólares.")
b("Según Marks, ese fondo era un canal de la CIA, y la búsqueda del hongo se vuelve el subproyecto cincuenta y ocho de MKUltra. Marks no dice que Wasson supiera de dónde salía el dinero.")
b("En Huautla duermen en el suelo de tierra. Todos disfrutan, menos Moore: tiene un resfriado terrible, pasan hambre, le pica todo el cuerpo.")
b("En la velada de María Sabina, los demás ven maravillas. Él no. Wasson dirá que parecía un marinero de agua dulce en alta mar.")
b("Poco después, Moore vuelve a Delaware con una bolsa de hongos. Y se encierra en su laboratorio a buscar el principio activo.", ideia=True)

# ───────────────────────── 5. LA REVISTA ─────────────────────────
cap("5. La Revista")
b("La Revista. Nueva York, trece de mayo de mil novecientos cincuenta y siete. La revista Life publica diecisiete páginas de Wasson con fotos a color.", card="NUEVA YORK, 1957", ideia=True)
b("Un editor le pone al artículo un título que Wasson no quería: En busca del hongo mágico.")
b("Mientras tanto, el micólogo francés Roger Heim cultiva los hongos en París y manda muestras a Albert Hofmann, el químico suizo que descubrió el LSD.")
b("En marzo de mil novecientos cincuenta y ocho, Hofmann publica el resultado: psilocibina. La CIA pagó parte de la expedición. La molécula la presenta un laboratorio suizo.")
b("Y el artículo atrae a México oleadas de visitantes. Uno de ellos, de vacaciones, es un psicólogo de Harvard: Timothy Leary.", ideia=True)
b("Si te interesan estos expedientes, suscríbete. Porque mientras la CIA buscaba en la sierra mexicana, su laboratorio ya preparaba químicos para un solo hombre: Fidel Castro.")

# ───────────────────────── 6. EL ESTUDIO ─────────────────────────
cap("6. El Estudio")
b("El Estudio. Washington, mil novecientos sesenta. Fidel Castro gobierna Cuba con discursos de horas por radio y televisión.", card="WASHINGTON, 1960", ideia=True)
b("Según el Comité Church del Senado, que cita un informe interno de la CIA, entre marzo y agosto la agencia estudia cómo sabotearlos. Los planes salen de la División de Servicios Técnicos: el laboratorio de la CIA, la misma división que administraba MKUltra.")
b("Un funcionario recuerda haber discutido rociar el estudio desde donde transmite Castro con una sustancia de efectos parecidos al LSD. Se descarta: no es fiable.")
b("Otro plan: poner sales de talio en sus zapatos durante un viaje, para que se le caiga la barba. Lo prueban en animales. Castro cancela el viaje.")
b("Y el laboratorio impregna una caja de puros con un químico que desorienta, para que Castro fume uno antes de un discurso.", ideia=True)

# ───────────────────────── 7. LOS PUROS ─────────────────────────
cap("7. Los Puros")
b("Los Puros. Dieciséis de agosto de mil novecientos sesenta. Un funcionario de la CIA recibe una caja de los puros favoritos de Castro.", card="AGOSTO DE 1960", ideia=True)
b("La orden ya no es humillarlo. Es tratarlos con una toxina botulínica tan potente, según el Comité Church, que bastaba con llevarse un puro a la boca.")
b("El siete de octubre están listos. El trece de febrero de mil novecientos sesenta y uno, se entregan a una persona no identificada. Y el registro, dice el comité, no revela si se intentó hacerlos llegar a Castro.")
b("El comité halló pruebas de al menos ocho complots de la CIA contra la vida de Castro entre mil novecientos sesenta y sesenta y cinco. Castro murió en dos mil dieciséis, a los noventa años.", ideia=True)

# ───────────────────────── 8. LA SILLA ─────────────────────────
cap("8. La Silla")
b("La Silla. Ciudad de México, julio de mil novecientos sesenta y tres. Washington pide a la estación de la CIA un candidato para un experimento de hipnosis rápida.", card="CIUDAD DE MÉXICO, 1963", ideia=True)
b("Eligen a un agente de poca monta que, al parecer, los soviéticos habían convertido en agente doble. Lo citan con una excusa: los jefes quieren darle más dinero.")
b("El plan: tumbar su silla hacia atrás, de golpe, y que en ese instante entre un hipnotizador traído de California.")
b("Los oficiales tumban la silla. El hipnotizador se queda paralizado. No pasa nada. Le dicen al agente que oyeron un ruido y quisieron protegerlo. Él se lo cree.")
b("Así se lo contó a Marks uno de los participantes. Ese mismo mes, un informe del inspector general de la CIA concluye que las drogas de MKUltra casi no se usan en operaciones.", ideia=True)

# ───────────────────────── 9. LA SELVA ─────────────────────────
cap("9. La Selva")
b("La Selva. Iquitos, Perú, mil novecientos sesenta y seis. MKUltra ya se llama MKSearch. Y la búsqueda de plantas sigue.", card="IQUITOS, 1966", ideia=True)
b("J. C. King, exjefe de la división de la CIA para el hemisferio occidental, funda con apoyo de la agencia una empresa en apariencia privada: la Amazon Natural Drug Company.")
b("Según Marks, King recorre los ríos en su casa flotante, con un vaso de whisky. En sus oficinas de Iquitos trabajan al menos dos paramilitares de la CIA.")
b("Envían a Estados Unidos una liana paralizante, base del curare, y cultivan yagé, la ayahuasca. Un botánico de Harvard trabaja con ellos sin saber nada de la CIA.")
b("En mil novecientos setenta y dos, la CIA cierra MKSearch. En enero de mil novecientos setenta y tres, por orden verbal del director Richard Helms, se destruyen los archivos de MKUltra.", ideia=True)

# ───────────────────────── 10. EL TESTIGO ─────────────────────────
cap("10. El Testigo")
b("El Testigo. Washington, tres de agosto de mil novecientos setenta y siete. Ante el Senado, la CIA responde por fin qué consiguió.", card="WASHINGTON, 1977", ideia=True)
b("Ese año se habían encontrado papeles financieros que escaparon a la destrucción: ciento cuarenta y nueve subproyectos, cuarenta y cuatro universidades. Y el nombre del psiquiatra Ewen Cameron, en Montreal: sus pacientes demandarían a la CIA, que había financiado parte de su trabajo.")
b("Un funcionario, Frank Laubinger, dice que no conoce ninguna droga del programa que haya llegado a uso operativo.")
b("Y John Gittinger, psicólogo de la agencia durante veintiséis años, explica qué cambiaba de verdad a una persona: aislarla, cortarle todo contacto y someterla a un estrés largo en el interrogatorio.")
b("Más de veinte años buscando la droga del control mental en semillas, hongos y lianas. Y la respuesta era una habitación cerrada.", ideia=True)

# ───────────────────────── 11. EL CURSO ─────────────────────────
cap("11. El Curso")
b("El Curso. Honduras, mil novecientos ochenta y tres. La CIA da un curso de interrogatorio a militares hondureños.", card="HONDURAS, 1983", ideia=True)
b("Según el historiador Alfred McCoy, la agencia ya había resumido en mil novecientos sesenta y tres, en un manual secreto llamado KUBARK, una década de investigación sobre la mente. Lo central ya no eran las drogas: eran el aislamiento y el estrés.")
b("Lo que quedó en Honduras no fue una droga. Fue el método, según el historiador Alfred McCoy.")
b("En mil novecientos ochenta y ocho, Richard Stolz, subdirector de operaciones de la CIA, lo describe ante el Senado: tres semanas de clase y dos de práctica, con presos reales. Asegura que el maltrato físico se rechazó.")
b("En esos años actúa el Batallón tres dieciséis, una unidad secreta del ejército hondureño. El Comisionado Nacional de Derechos Humanos documentó ciento ochenta y cuatro casos de desaparición.")
b("Stolz admitió algo más: un oficial de la CIA visitó en su celda a Inés Murillo, una abogada detenida ilegalmente casi ochenta días en mil novecientos ochenta y tres.", ideia=True)

# ───────────────────────── 12. LA TACHADURA ─────────────────────────
cap("12. La Tachadura")
b("La Tachadura. Baltimore, veintisiete de enero de mil novecientos noventa y siete. El Baltimore Sun publica un manual de la CIA… de mil novecientos ochenta y tres.", card="BALTIMORE, 1997", ideia=True)
b("Según un informe del Senado, nació de las notas del curso de Honduras. Habla de celdas sin ventanas y de arrestos de madrugada, para causar el máximo malestar mental.")
b("En la segunda página dice, en inglés: «we do not stress», no ponemos énfasis en las técnicas coercitivas, pero queremos que sepas usarlas bien.")
b("Entre mil novecientos ochenta y cuatro y ochenta y cinco, alguien la corrige a mano. Tacha «do not stress» y escribe «deplore»: deploramos esas técnicas, y queremos que las conozcas para que las evites. Debajo, la frase original se sigue leyendo.")
b("La CIA entregó el manual cuando el Sun amenazó con demandarla. En Honduras, el juez Roy Medina dijo que confirmaba una verdad que su país conocía desde hacía mucho.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. Los Niños Santos")
b("Los Niños Santos. Huautla, otoño de mil novecientos sesenta y dos. Albert Hofmann sube a la sierra con Wasson. Trae pastillas de psilocibina.", card="HUAUTLA, 1962", ideia=True)
b("María Sabina las prueba de noche. Al amanecer, dice que tienen el mismo poder que los hongos. La casa de la velada de mil novecientos cincuenta y cinco ya no existe: según Hofmann, la quemaron, probablemente vecinos molestos porque reveló el secreto a extraños.")
b("Años después, en el testimonio que recogió Álvaro Estrada, ella contó que desde que llegaron los extranjeros, los niños santos perdieron su pureza.")
b("La CIA vino a América Latina a buscar una droga para abrir la mente. Lo que dejó fue un manual para quebrarla.", ideia=True)
b("Y tú, ¿qué pesa más en esta historia: lo que la CIA vino a buscar, o lo que dejó? Déjalo en los comentarios.")

# ───────────────────────── STORYBOARD (planos por bloco, na ordem dos blocos) ─────────────────────────
# Preenchido na etapa storyboard (skill storyboard): uma lista de planos por bloco de texto, na ordem.
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
    if not SB:   # roteiro antes do storyboard: só SCRIPT.md + blocos.json (+ mapa de tempos para conferir a EMBALAGEM)
        tt, linhas_t, capa = 0.0, [], None
        for blk in B:
            if "cap" in blk: capa = blk["cap"]; linhas_t.append(f"{fmt(tt)}  {capa}"); continue
            d_ = dur(blk["t"]); linhas_t.append(f"   {fmt(tt)}–{fmt(tt + d_)}  {limpo(blk['t'])[:70]}"); tt += d_
        (out / "SCRIPT.md").write_text(
            f"# {TITULO}: roteiro\n\nPromessa: {PROMESSA}\n\nTítulos: {TITULOS}\n\n"
            f"Gerado por `roteiro.py` (fonte única; edite lá). {words} palavras, ~{fmt(total)} estimados a {WPS*60:.0f} ppm (com as pausas entre frases).\n"
            "Os blocos [Nxxx] são os mesmos de `blocos.json` (lá com as tags do Fish). Storyboard ainda não feito.\n" + "\n".join(script))
        print("\n".join(linhas_t)); print(json.dumps({"palavras": words, "duracao": fmt(total), "blocos": len(blocos)}, ensure_ascii=False))
        return
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
