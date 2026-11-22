#!/usr/bin/env python3
"""Fonte única do dossie-es 014 (La Yakuza): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py (na pasta do vídeo). Geração copiada do 013-nuremberg.

Embalagem aprovada no crivo r3 (21/11/2026, EMBALAGEM.md/CRIVO.md):
  A/T1 "YAKUZA: la mafia que tenía su nombre en la puerta" + letreiro arrancado, YAKUZA + sello ¿LEGAL? (objeto-simbolo, controle)
  B/T2 "Cómo la Yakuza pasó de trabajar para Japón a ser su enemiga" + 184.000 riscado sobre salão de tatame vazio, HOY 17.600 (numero-estatistica)
  C/T3 "Japón, 1992: la Yakuza tuvo que esconder su nombre" + homem em contraluz rasgando o cartão com o emblema, rótulo YAKUZA (cena-acao)
Ângulo (ANGULO.md): la mafia que no se escondía (ser yakuza nunca foi crime; o Estado a usou à vista e depois a apagou com papéis).

Sintaxe dos planos (campo s): "chave|prompt" nova · "chave" reuso · "chave#enq" reuso com enquadramento · + "@@TEXTO" rótulo.
"""
import json, math, re
from pathlib import Path

WPS = 2.38           # palavras/s medidas no 001–013 (erro de 1–3%)
BREAK, LONG = 0.35, 0.8
MAX_PLANO_INICIO = 3.0   # s por plano nos primeiros INICIO s (~20 cortes/min)
INICIO = 60.0
MAX_PLANO = 3.6      # s por plano depois (~17 cortes/min)
INEDITO_ATE = 180.0  # s: só imagens novas até aqui
JANELA = 60.0        # s: mesmo enquadramento da mesma imagem só depois disso
HOOK_MAX = 40.0      # s: EMBALAGEM: frase-âncora até 0:40
ENQ = ["médio-esq", "médio-dir", "detalhe-centro", "detalhe-alto", "detalhe-baixo", "aberto"]
MOV_NOVO = ["zoom-in lento", "pan esq→dir", "zoom-out lento", "pan dir→esq", "push-in leve", "tilt ↓ lento"]
MOV_ENQ = {"aberto": "zoom-out lento", "médio-esq": "pan esq→dir", "médio-dir": "pan dir→esq",
           "detalhe-centro": "push-in leve", "detalhe-alto": "tilt ↓ lento", "detalhe-baixo": "tilt ↑ lento"}
TITULO = "YAKUZA: la mafia que tenía su nombre en la puerta"
TITULOS = ("T1 YAKUZA: la mafia que tenía su nombre en la puerta / "
           "T2 Cómo la Yakuza pasó de trabajar para Japón a ser su enemiga / "
           "T3 Japón, 1992: la Yakuza tuvo que esconder su nombre")
PROMESSA = ("En Japón, ser yakuza nunca fue delito: durante un siglo la mafia tuvo oficinas con su nombre en la puerta y trabajó a la vista "
            "para ministros, gobiernos y empresas, hasta que Japón inventó leyes y contratos para borrarla de la vista; de 184.000 miembros a 17.600.")

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None, ideia=False): B.append({"t": t, "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK ─────────────────────────
cap("Hook")
b("Tokio, mayo de mil novecientos noventa y dos. Frente a su casa, cinco hombres atacan con cuchillos al cineasta Juzo Itami.", card="TOKIO, 1992")
b("Días antes, Itami había estrenado una película que enseña a no pagarle a la yakuza.")
b("Los grupos de la yakuza tenían oficinas, emblema y tarjetas con su nombre. Pertenecer a la yakuza no era delito. Hoy tampoco.")
b("Esta es TODA la historia de la Yakuza: la mafia que no se escondía, porque trabajaba para el poder. De ciento ochenta y cuatro mil miembros y asociados… a diecisiete mil seiscientos.", ideia=True)

# ───────────────────────── 1. EL MINISTRO ─────────────────────────
cap("1. El Ministro")
b("El Ministro. Tokio, cuatro de octubre de mil novecientos diecinueve. El ministro del Interior, Takejiro Tokonami, reúne a treinta y seis grandes jefes de apuestas.", card="TOKIO, 1919")
b("Vienen de un mundo viejo de tahúres y vendedores ambulantes. Según la explicación más aceptada, su nombre sale de una de las peores manos de un juego de cartas: ocho, nueve y tres. Ya, ku, za.")
b("Un mes después nace la Gran Sociedad de la Esencia Nacional de Japón. Promete defender al emperador y combatir a los rojos. Dice tener seiscientos mil miembros. La cifra la da ella misma.")
b("Según el politólogo Masao Maruyama, sus hombres actúan como rompehuelgas y atacan a sindicatos y a campesinos.")
b("No la organiza un jefe criminal. La organiza un ministro. La próxima vez que el Estado los necesite, el intermediario saldrá de una cárcel.", ideia=True)

# ───────────────────────── 2. LA CELDA ─────────────────────────
cap("2. La Celda")
b("La Celda. Tokio, veinticuatro de diciembre de mil novecientos cuarenta y ocho. De la prisión de Sugamo salen, sin juicio, varios sospechosos de crímenes de guerra.", card="TOKIO, 1948")
b("Uno es Yoshio Kodama, ultranacionalista. Durante la guerra compró materiales en China para la Marina Imperial. Otro, ese mismo día, es Nobusuke Kishi, exministro del gobierno de guerra.")
b("Según los periodistas David Kaplan y Alec Dubro, Kodama sale con un compromiso: ayudar a la ocupación estadounidense contra los comunistas.")
b("Afuera, los mercados negros de la posguerra están en manos de bandas. En Kobe, el joven jefe Kazuo Taoka convierte al Yamaguchi-gumi en el que reparte el trabajo en el puerto.")
b("Ocho años después, Kishi es primer ministro. Y en mil novecientos sesenta, según un historiador, recurre a Kodama.", ideia=True)

# ───────────────────────── 3. LA VISITA ─────────────────────────
cap("3. La Visita")
b("La Visita. Tokio, junio de mil novecientos sesenta. El presidente Eisenhower debe llegar el diecinueve. Las calles están llenas de protestas contra el tratado de seguridad con Estados Unidos.", card="TOKIO, 1960")
b("Según el historiador Nick Kapur, el gobierno de Kishi le pide a Kodama una fuerza privada para proteger la visita.")
b("Según Kapur, el plan de movilización prevé ciento cuarenta y seis mil ochocientos setenta y nueve hombres. Son derechistas y yakuza. La policía calcula que, como mucho, podrían reunirse unos ciento veinte mil.")
b("El dieciséis de junio, el gobierno pide aplazar la visita, y la visita se cancela. Aun así, la yakuza nunca fue tan grande. En mil novecientos sesenta y tres, según cifras policiales citadas por la prensa, suma ciento ochenta y cuatro mil miembros y asociados.")
b("Ya no son tahúres de feria. Ahora están también sobre los escenarios.", ideia=True)

# ───────────────────────── 4. LA CANTANTE ─────────────────────────
cap("4. La Cantante")
b("La Cantante. Tokio, treinta y uno de diciembre de mil novecientos setenta y tres. La televisión pública NHK emite su gran concurso musical de fin de año, el Kohaku.", card="TOKIO, 1973")
b("Por primera vez en dieciocho años, no aparece Hibari Misora, la cantante más famosa del país. Ese año, su hermano había sido procesado por actividades ligadas a una organización criminal.")
b("Hibari nunca fue acusada de nada. Pero, según los periodistas Kaplan y Dubro, durante años el Yamaguchi-gumi de Kazuo Taoka se encargó de la seguridad de sus conciertos.")
b("La yakuza estaba en el escenario, a la vista de todos. Y Kodama, el hombre de la celda, ya cobraba de una empresa estadounidense que fabrica aviones.", ideia=True)

# ───────────────────────── 5. LOS RECIBOS ─────────────────────────
cap("5. Los Recibos")
b("Los Recibos. Washington, febrero de mil novecientos setenta y seis. Un subcomité del Senado de Estados Unidos investiga los pagos de la empresa Lockheed en el extranjero.", card="WASHINGTON, 1976")
b("Aparece un nombre japonés: Yoshio Kodama, su asesor secreto en Japón. Según la revista Time, recibió más de siete millones de dólares desde mil novecientos sesenta.")
b("Entre los papeles hay recibos por unos dos millones de dólares, de noviembre de mil novecientos setenta y dos. Ese mismo mes, la aerolínea japonesa ANA acepta comprar aviones TriStar de Lockheed por ciento treinta millones.")
b("El escándalo alcanzará al ex primer ministro Kakuei Tanaka, detenido en julio. Kodama, convaleciente de un derrame cerebral, se queda en su casa de Tokio. Hasta allí va a buscarlo un avión.", ideia=True)

# ───────────────────────── 6. EL AVIÓN ─────────────────────────
cap("6. El Avión")
b("El Avión. Tokio, veintitrés de marzo de mil novecientos setenta y seis. Mitsuyasu Maeno, actor de veintinueve años, alquila una avioneta Piper en el aeródromo de Chofu.", card="TOKIO, 1976")
b("Va vestido de piloto kamikaze, con la cinta del sol naciente en la frente. Sobrevuela el barrio de Setagaya y da dos vueltas sobre la casa de Kodama.")
b("Después se lanza contra ella, gritando vivas al emperador. El avión choca contra el segundo piso. Maeno muere. Kodama, en otra habitación, sale ileso.")
b("Maeno también era ultranacionalista. Según la prensa de la época, se sentía traicionado: su ídolo cobraba de una empresa extranjera.")
b("El padrino de los nacionalistas, el amigo de los ministros, queda a la vista de todo el país. En los años ochenta, una guerra por la sucesión del Yamaguchi-gumi deja al menos treinta y seis muertos, según el periodista David Kaplan. Y Japón decide mirar a la yakuza de otra manera.", ideia=True)

# ───────────────────────── 7. EL LETRERO ─────────────────────────
cap("7. El Letrero")
b("El Letrero. Japón, primero de marzo de mil novecientos noventa y dos. Entra en vigor la ley contra los grupos violentos. No prohíbe ser yakuza.", card="JAPÓN, 1992")
b("Las comisiones de seguridad pública de cada prefectura pueden designar a un grupo como violento. Sus miembros no pueden, por ejemplo, exigir dinero en nombre del grupo.")
b("Hasta entonces, el nombre del grupo estaba en la puerta y en las tarjetas de visita. Según el Libro Blanco de la Policía de ese año, de ciento ocho oficinas del Yamaguchi-gumi revisadas, cuarenta y una quitan el letrero y el emblema. Y hay jefes que borran el nombre del grupo de sus tarjetas.")
b("En mayo, Juzo Itami estrena su película. Días después llegan los cinco hombres. En noviembre, el Yamaguchi-gumi, ya el mayor del país, demanda a la comisión de Hyogo para anular su designación. Después retira la demanda.")
b("Itami tarda tres meses en recuperarse y vuelve a filmar. Dos de sus atacantes reciben penas de seis y cinco años. En mil novecientos noventa y siete, Itami muere al caer de un edificio. La policía concluye que fue un suicidio. El periodista Jake Adelstein sostiene otra versión, que nunca se ha probado.", ideia=True)
b("Si te interesan estos expedientes, suscríbete. Porque la ley tenía un límite: las grandes empresas seguían pagando.")

# ───────────────────────── 8. LA ASAMBLEA ─────────────────────────
cap("8. La Asamblea")
b("La Asamblea. Japón, veintisiete de junio de mil novecientos noventa y siete. Dos mil trescientas cincuenta y cinco empresas celebran su junta de accionistas el mismo día.", card="JAPÓN, 1997")
b("No es casualidad. Así se defienden de los sokaiya: extorsionistas que compran unas pocas acciones y amenazan con reventar la junta con escándalos si no se les paga. Según la policía, muchos trabajan con la yakuza.")
b("Con todas las juntas a la vez, los sokaiya no pueden estar en todas. Ese mismo mes, la fiscalía investiga al banco Dai-Ichi Kangyo, uno de los mayores del país, por préstamos a un sokaiya, Ryuichi Koike.")
b("Su expresidente del consejo, Tadashi Okuda, será condenado, con pena suspendida, por un préstamo ilegal de once mil ochocientos millones de yenes. Los bancos también pagaban. Y en Estados Unidos, el FBI hará su propio trato.", ideia=True)

# ───────────────────────── 9. EL HÍGADO ─────────────────────────
cap("9. El Hígado")
b("El Hígado. Los Ángeles, julio de dos mil uno. En el hospital de la Universidad de California, un paciente japonés recibe un trasplante de hígado.", card="LOS ÁNGELES, 2001")
b("Es Tadamasa Goto, jefe del Goto-gumi, el grupo de los hombres que atacaron a Itami.")
b("Según el diario Los Angeles Times, Goto entró en Estados Unidos con una visa obtenida con ayuda del FBI, a cambio de información sobre la yakuza. Él y otro yakuza donaron cien mil dólares al hospital.")
b("Un exjefe de la unidad asiática del FBI dijo después que el FBI no le consiguió la operación y que Goto no entregó nada importante. En dos mil ocho, el Yamaguchi-gumi lo expulsa. En dos mil nueve, Goto se ordena sacerdote budista.")
b("En casa, el poder ya no los protege. Algunos buscan negocio mucho más lejos. Hasta Sudamérica.", ideia=True)

# ───────────────────────── 10. EL AEROPUERTO ─────────────────────────
cap("10. El Aeropuerto")
b("El Aeropuerto. Buenos Aires, veintisiete de marzo de dos mil diez. En Ezeiza, la policía detiene a un japonés que embarca hacia su país con tres kilos de cocaína.", card="BUENOS AIRES, 2010")
b("Se llama Hirasawa. Según contó después a la revista InSight Crime, pasó unos treinta años en la yakuza, casi todos en el Yamaguchi-gumi. Había venido a Sudamérica a comprar droga para venderla en Japón.")
b("Lo condenan a cuatro años y nueve meses. Año y medio después, la sentencia se anula y lo deportan.")
b("En dos mil veinticuatro, la policía japonesa detiene a un alto miembro del Sumiyoshi-kai, de setenta y seis años, por unos quince kilos de droga estimulante enviados desde México. Se investiga un vínculo con un cártel. No está probado.")
b("En Japón, el cerco ya no lo pone solo la policía. Lo ponen los contratos.", ideia=True)

# ───────────────────────── 11. EL CONTRATO ─────────────────────────
cap("11. El Contrato")
b("El Contrato. Tokio, veintitrés de agosto de dos mil once. Shinsuke Shimada, uno de los presentadores más famosos de la televisión japonesa, anuncia que se retira. Admite su relación con un yakuza.", card="TOKIO, 2011")
b("Poco más de un mes después, el primero de octubre, Tokio y Okinawa completan la lista: las cuarenta y siete prefecturas ya tienen ordenanzas contra la yakuza.")
b("Las empresas no pueden pagarles ni ayudarlos a sabiendas. En los contratos aparece una cláusula: quien firma declara no pertenecer a un grupo violento.")
b("El Estado que la había usado ya no necesita prohibirla. Le basta con que nadie firme con ella. Diez años después, un tribunal va más lejos.", ideia=True)

# ───────────────────────── 12. LA SENTENCIA ─────────────────────────
cap("12. La Sentencia")
b("La Sentencia. Fukuoka, veinticuatro de agosto de dos mil veintiuno. Un tribunal condena a muerte a Satoru Nomura, jefe del Kudo-kai, el único grupo de Japón designado como especialmente peligroso.", card="FUKUOKA, 2021")
b("Lo declara responsable de ordenar cuatro ataques contra ciudadanos. Entre ellos, el asesinato en mil novecientos noventa y ocho del exjefe de una cooperativa de pescadores. Es la primera pena de muerte para un jefe de la yakuza.")
b("Según la prensa, Nomura le advierte al juez que se arrepentirá de esto toda su vida. En dos mil veinticuatro, un tribunal superior lo absuelve de ese asesinato y cambia la pena por cadena perpetua. El caso sigue en el Supremo.")
b("Nomura había gobernado su grupo desde una sede con su emblema, en Kitakyushu. Esa puerta ya no existe.", ideia=True)

# ───────────────────────── CIERRE ─────────────────────────
cap("Cierre. La Puerta")
b("La Puerta. Kitakyushu, noviembre de dos mil diecinueve. La ciudad, un centro contra la yakuza, el dueño del edificio y el propio Kudo-kai firman un acuerdo: la sede se derribará. El terreno termina en manos de una organización que ayuda a personas sin hogar.", card="KITAKYUSHU, 2019")
b("A finales de dos mil veinticinco, según la Agencia Nacional de Policía, la yakuza suma diecisiete mil seiscientos miembros y asociados. En mil novecientos sesenta y tres eran ciento ochenta y cuatro mil.")
b("Juzo Itami enseñó en una película a cerrarle la puerta a la yakuza. Mucho antes, se la habían abierto un ministro en mil novecientos diecinueve, un primer ministro en mil novecientos sesenta y las grandes empresas.")
b("La yakuza nunca se escondió del poder. Se escondió cuando el poder dejó de necesitarla.", ideia=True)
b("Y tú, ¿quién crees que necesitaba más al otro: la yakuza al Estado, o el Estado a la yakuza? Déjalo en los comentarios.")

# ───────────────────────── STORYBOARD (planos por bloco, na ordem dos blocos) ─────────────────────────
SB = [[] for x in B if "t" in x]   # storyboard: depois do crivo de ângulo
THUMBS = []
_textos = [x for x in B if "t" in x]
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
