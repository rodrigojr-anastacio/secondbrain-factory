#!/usr/bin/env python3
"""Fonte única do 017-cuba (22/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

14º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
7º com ÂNGULO próprio (ANGULO.md): "quem compra, manda" — uma ilha de um produto só precisa de preço garantido; cada comprador
(a Coroa em 1717, os EUA em 1891/1902/1934, a URSS em 1960/1964/1972, a Venezuela em 2000) garantiu o preço cobrando uma cláusula,
e cada cláusula empurrou Cuba para o próximo comprador. Resposta NÃO é a "mesada" do Riqueza e Ruína nem o fecho com Martí do HistoDarias.
EMBALAGEM.md aprovada no crivo r3:
  A/T1 "Cuba adoçava o MUNDO. Por que dependia de um país só?" + thumb rosto-emocao (guajiro em pânico sobre sacos, "SEM COMPRADOR")
  B/T2 "Por que Cuba só trocava de COMPRADOR? E o que cobravam?" + thumb numero-estatistica ("5× O PREÇO")
  C/T3 "Cuba: como o AÇÚCAR decidiu quem mandava na ilha" + thumb mapa-lugar (ilha amarrada por corda, sem texto)
Hook: julho de 1960, 700 mil t sem comprador (≤ 0:20) → Moscou compra as mesmas 3 dias depois (≤ 0:30) → "quase cinco vezes o preço"
  + "cada um cobrou outra coisa" + Espanha/EUA/URSS/Venezuela (≤ 0:45) → PERGUNTA CENTRAL (≤ 0:50) → "essa é a história inteira".
Peças da resposta: 1 (cap. 8) o comprador que paga bem pede que você continue vendendo o mesmo; 2 (cap. 9) quanto melhor o preço,
  mais caro sair. Fecho: só um gigante garante preço; cada garantia veio com uma cláusula; Cuba escolhia de quem depender.
"Guarde" único: as 700 mil toneladas → pagas no cap. 7 (trocam de mão em 72 h) e no fecho (mudaram de cláusula).
Neutralidade: Fidel, Batista, Baía dos Porcos, mísseis, embargo, 2026 em fatos dos dois lados, sem adjetivo.

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1960") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006–016).
Imagens: Codex (canal.yaml visual.gerador: codex; fallback nano-banana). Prompts só de conteúdo; o estilo vem do canal.yaml.
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (006–016: ~128–130 ppm com pausas)
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
TITULO = "A história INTEIRA de Cuba"
PERGUNTA = "Por que Cuba sempre dependeu de um país só para comprar o que ela produz?"
PROMESSA = ("Por que Cuba sempre dependeu de um país só para comprar o que ela produz, e o que cada comprador cobrou por isso: "
            "as 700 mil toneladas de 1960 que trocam de mão em 3 dias, o preço de quase cinco vezes o mercado, a Coroa, os EUA, "
            "a URSS e a Venezuela (EMBALAGEM.md r3).")
TITULOS = ('T1 "Cuba adoçava o MUNDO. Por que dependia de um país só?" / T2 "Por que Cuba só trocava de COMPRADOR? E o que cobravam?" / '
           'T3 "Cuba: como o AÇÚCAR decidiu quem mandava na ilha"')

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None):
    ideia = t.startswith("§")
    n = sum(1 for x in B if "t" in x) + 1
    if not s: s = tuple(P.get(n, ()))
    if not s and PENDENTE: s = (f"tmp{n:03d}|placeholder",)
    assert s, f"N{n:03d} sem planos"
    B.append({"t": t.lstrip("§ ").strip(), "s": list(s), "card": card, "ideia": ideia})

PENDENTE = True   # storyboard ainda não escrito
P = {}
# __PLANOS__


# ───────────────────────── HOOK (as 700 mil toneladas, 1960) ─────────────────────────
cap("Hook")
b("[curious] Havana, julho de mil novecentos e sessenta. Imagine que você tem um armazém no porto, cheio de sacos de açúcar até o teto. Esse açúcar já tem comprador: os Estados Unidos.", card="1960")
b("Aí, no dia seis, Washington corta a cota de Cuba: setecentas mil toneladas ficam sem comprador. Três dias depois, chega um recado de Moscou. A União Soviética compra exatamente essas setecentas mil.")
b("E um dia ia pagar quase cinco vezes o preço do mercado. Só que nenhum comprador de Cuba cobrou só em dinheiro. Nem a Espanha, nem os Estados Unidos, nem os soviéticos, nem a Venezuela.")
b("[serious] Então fica a pergunta: por que Cuba sempre dependeu de um país só para comprar o que ela produz?")
b("Essa é a história inteira de Cuba. Guarde essas setecentas mil toneladas: elas voltam. E tudo começa com uma ilha que, para azar de quem chegou, quase não tinha ouro.")

# ───────────────────────── 1. A ILHA QUE FICOU SEM OURO ─────────────────────────
cap("1. A ilha que ficou sem ouro")
b("§ Bayamo, leste de Cuba, mil seiscentos e quatro. Um pirata francês, Gilberto Girón, sequestra o bispo da ilha numa fazenda perto da cidade. E pede resgate.", card="1604")
b("Repare que ninguém em Bayamo estranha um navio francês por ali. A cidade vivia de vender couro a navios estrangeiros. E isso era crime.")
b("Porque a lei espanhola dizia: Cuba só vende para a Espanha, nos navios da Espanha. Só que esses navios quase não passavam pelo leste, e couro não espera. Então o povo vendia para quem aparecesse.")
b("Os moradores pagam o resgate e depois emboscam o pirata. Um escrivão escreve um poema sobre o caso, que hoje é tido como a primeira obra da literatura cubana. Tente ganhar fama literária com um sequestro.")
b("§ Era o jeito de uma ilha que tinha ficado sem ouro. O pouco que havia acabou em poucas décadas, junto com a maior parte dos taínos, levados por guerra, trabalho forçado e epidemias. Sobrou Havana, o porto onde as frotas da prata paravam na volta.")
b("O problema é que a Espanha não queria só proibir. Queria comprar. E, um século depois, ela acha o produto certo.")

# ───────────────────────── 2. O COMPRADOR POR DECRETO ─────────────────────────
cap("2. O comprador por decreto")
b("§ Arredores de Havana, julho de mil setecentos e dezessete. Plantadores de tabaco, os vegueros, se juntam no povoado de Jesús del Monte. Estão furiosos com uma lei que chegou de Madri.", card="1717")
b("A lei, de abril, cria o estanco do tabaco: daqui em diante, todo o fumo de Cuba só pode ser vendido a um comprador, o rei. Pelo preço que o rei marcar.")
b("Imagine que você planta, colhe, seca as folhas, e só existe uma porta para bater. Os vegueros se levantam em dezessete, de novo em vinte e outra vez em vinte e três. Mas o estanco fica.")
b("§ Então Madri vai além. Em mil setecentos e quarenta, uma companhia de Havana ganha o monopólio do comércio com a Espanha: um único balcão compra e vende quase tudo o que a ilha produz.", card="1740")
b("Mas comprador único só funciona enquanto ninguém mostra outro. Em mil setecentos e sessenta e dois, os ingleses tomam Havana por onze meses, e navios de outros portos lotam o cais. Cuba descobre que tinha clientes fora da Espanha.")
b("O problema era convencer Madri a deixar.")

# ───────────────────────── 3. O VIZINHO EM CHAMAS ─────────────────────────
cap("3. O vizinho em chamas")
b("§ Madri, mil setecentos e noventa e dois. Um advogado de Havana de vinte e poucos anos, Francisco de Arango, entrega à Coroa um discurso comprido. A tese cabe numa frase: a ilha vizinha está pegando fogo, e Cuba pode ficar com o lugar dela.", card="1792")
b("A vizinha era a colônia francesa de São Domingos, a maior produtora de açúcar do mundo, onde os escravizados tinham se rebelado no ano anterior. O açúcar do mundo ficou, de repente, sem fornecedor.")
b("Arango pede duas coisas: comércio mais livre e mais africanos escravizados. E consegue. Em poucas décadas, Cuba vira a maior produtora de açúcar do planeta, erguida sobre centenas de milhares de pessoas trazidas à força.")
b("Pense no açúcar do seu café. Por boa parte do século dezenove, uma fatia enorme dele saía de uma ilha só.")
b("§ Só que tem um detalhe. A bandeira em Havana continua espanhola, mas quem compra cada vez mais é outro país, logo ali, a uns cento e cinquenta quilômetros. No fim do século, a maior parte do açúcar cubano já ia para os Estados Unidos.")
b("E aí aparece o problema de sempre: e se esse comprador mudasse de ideia?")

# ───────────────────────── 4. A BANDEIRA DE UM, O COMPRADOR DE OUTRO ─────────────────────────
cap("4. A bandeira de um, o comprador de outro")
b("§ Washington, mil oitocentos e noventa e um. Num congresso de países da América, um delegado do Uruguai toma notas. Ele é cubano, vive exilado em Nova York e se chama José Martí.", card="1891")
b("Em maio, ele escreveu numa revista: [break] o povo que compra, manda. O povo que vende, serve. E o povo que quer morrer vende a um povo só.")
b("Martí sabia do que falava. Cuba tinha feito uma guerra de dez anos pela independência, de sessenta e oito a setenta e oito, e perdido. E agora o açúcar dela dependia de uma lei americana.")
b("§ Porque, naquele ano, um acordo entre Washington e Madri deixa o açúcar cubano entrar nos Estados Unidos quase sem imposto. A ilha bate recorde de produção. Aí, em noventa e quatro, o Congresso americano muda a lei e volta a cobrar quarenta por cento.", card="1894")
b("Em dois anos, as vendas para os Estados Unidos caem pela metade. Usina parada é gente sem trabalho no campo. Imagine depender de uma lei votada num país onde você nem vota.")
b("Em fevereiro de noventa e cinco, a guerra recomeça, organizada justamente por Martí, que cai em combate três meses depois. A luta segue, e em noventa e oito os Estados Unidos entram nela. A Espanha sai de Cuba. Só que quem fica com a caneta é o comprador.", card="1895")

# ───────────────────────── 5. VINTE POR CENTO ─────────────────────────
cap("5. Vinte por cento")
b("§ Havana, dezembro de mil novecentos e dois. Cuba, independente havia sete meses, assina com os Estados Unidos um tratado de reciprocidade. O açúcar cubano ganha vinte por cento de desconto na tarifa americana.", card="1902")
b("Parece presente. Só que vem junto com outro papel, a Emenda Platt, posta na Constituição cubana: ela dá a Washington o direito de intervir na ilha e uma base em Guantánamo.")
b("Ou seja, o desconto entra pela porta da frente, e a cláusula, pela dos fundos. Repare que ninguém precisou de exército para isso: bastou o preço.")
b("§ Então o desconto atrai dinheiro. Empresas americanas compram usinas, terras e ferrovias. Antes da Primeira Guerra, tinham pouco mais de um terço da capacidade das usinas. Em mil novecentos e vinte e quatro, quase dois terços.", card="1924")
b("No meio do caminho, em vinte, o preço do açúcar sobe às nuvens e despenca em poucos meses. Bancos cubanos quebram, e credores americanos ficam com mais usinas. Cuba produzia. Mas a decisão morava em outro lugar.")

# ───────────────────────── 6. O MESMO MÊS ─────────────────────────
cap("6. O mesmo mês")
b("§ Washington, maio de mil novecentos e trinta e quatro. No dia nove, Roosevelt assina uma lei de cotas: o governo americano passa a decidir quanto açúcar cada fornecedor pode vender aos Estados Unidos.", card="1934")
b("Vinte dias depois, os dois países assinam um tratado que acaba com a Emenda Platt. Guantánamo fica. E a cláusula sai da Constituição para morar num número: a cota.")
b("Pense na cena: num mesmo mês, Cuba ganha o direito de não ser invadida e perde o direito de decidir quanto vende. Tente explicar essa vitória a um usineiro de Camagüey.")
b("§ Então, por vinte e cinco anos, a ilha vive em torno de um número escrito em Washington. Cota alta, emprego no campo. Cota baixa, o tempo morto entre uma safra e outra fica mais comprido.")
b("Governos caem e sobem nesse meio-tempo. Em cinquenta e dois, Fulgencio Batista dá um golpe. Mas o número continua lá. E, em cinquenta e nove, chega ao poder alguém que promete rasgá-lo.")

# ───────────────────────── 7. SETECENTAS MIL TONELADAS ─────────────────────────
cap("7. Setecentas mil toneladas")
b("§ Havana, fevereiro de mil novecentos e sessenta. Anastas Mikoyan, vice de Khrushchev, inaugura uma exposição soviética: máquinas, tratores e muita gente curiosa.", card="1960")
b("Numa visita a uma cooperativa, a multidão gritou para ele: e armas e aviões também! Mikoyan repete a frase. Dias depois, assina um acordo: a União Soviética vai comprar um milhão de toneladas de açúcar por ano.")
b("Lembra da nossa pergunta? Aqui ela fica mais difícil. Porque, nesses meses, o governo de Fidel Castro desapropria terras, e as refinarias americanas, que se recusam a processar petróleo soviético, são tomadas.")
b("§ Aí vem o dia seis de julho: Eisenhower corta as setecentas mil toneladas que faltavam. Três dias depois, Khrushchev oferece comprar exatamente as mesmas. Se você é o dono daquele armazém do começo, o seu açúcar troca de mão em setenta e duas horas.")
b("Em sessenta e um, exilados treinados pelos Estados Unidos desembarcam na Baía dos Porcos e são derrotados. Em sessenta e dois, mísseis soviéticos na ilha quase começam uma guerra nuclear, e o embargo americano fica total. O comprador novo tinha chegado. Só que ele também ia cobrar.", card="1962")

# ───────────────────────── 8. SEIS CENTAVOS ─────────────────────────
cap("8. Seis centavos")
b("§ Moscou, janeiro de mil novecentos e sessenta e quatro. Fidel Castro vai à União Soviética e volta com um contrato: Moscou compra açúcar cubano por anos, a seis centavos de dólar a libra. Preço fixo, num mercado que sobe e desce.", card="1964")
b("Preço fixo é o sonho de qualquer produtor. Imagine saber hoje quanto você vai receber por cada saco daqui a seis anos. E as quantidades sobem ano a ano, até cinco milhões de toneladas em setenta.")
b("Só que preço fixo pede promessa fixa. Cuba, que tinha prometido sair do açúcar, faz o contrário: aposta numa colheita de dez milhões de toneladas para mil novecentos e setenta. O país inteiro vai para o canavial.")
b("§ A safra dá cerca de oito milhões e meio, a maior da história de Cuba, e mesmo assim é um fracasso. Em vinte e seis de julho, Fidel assume em público a responsabilidade. Cuba nunca tinha produzido tanto açúcar. E nunca tinha dependido tanto de quem o comprava.", card="1970")
b("E aqui está a primeira peça da resposta: o comprador que paga bem não pede pouco. Pede que você continue vendendo a mesma coisa, para ele. Só que o preço dele ainda ia subir muito.")

# ───────────────────────── 9. QUASE CINCO VEZES O PREÇO ─────────────────────────
cap("9. Quase cinco vezes o preço")
b("§ Moscou, julho de mil novecentos e setenta e dois. Cuba entra no Comecon, o mercado comum do bloco soviético. A partir daí, o açúcar vira moeda: vai para o leste e volta como petróleo, trigo, máquinas e adubo.", card="1972")
b("E o preço? No começo dos anos oitenta, segundo a CIA, Moscou pagava cerca de quarenta e dois centavos por libra, quase cinco vezes o preço do mercado mundial. Em oitenta e sete, uma tonelada de açúcar valia cerca de quatro toneladas e meia de petróleo soviético.")
b("Pense num cliente que paga cinco vezes o preço do seu pão. Você não abre outra padaria: você faz mais pão. Em oitenta e nove, mais de oitenta por cento das exportações cubanas iam para o bloco socialista.")
b("Lembra da pergunta? A segunda peça está aqui: quanto melhor o preço, mais caro sair. O preço alto era a corda.")
b("§ Então, em mil novecentos e noventa e um, o comprador simplesmente deixa de existir. A União Soviética acaba, e com ela o preço, o petróleo e o trigo. Cuba entra no que o governo chamou de Período Especial: apagões, comida racionada, ônibus parados.", card="1991")
b("Sem o preço de Moscou, a safra cai quase à metade em dois anos. E pela primeira vez desde o rei de mil setecentos e dezessete, a ilha não tinha um grande comprador. O problema era achar outro.")

# ───────────────────────── 10. PETRÓLEO POR JALECO ─────────────────────────
cap("10. Petróleo por jaleco")
b("§ Caracas, trinta de outubro de dois mil. Fidel Castro e Hugo Chávez assinam um convênio: a Venezuela manda cinquenta e três mil barris de petróleo por dia, em condições especiais. E Cuba paga com gente: médicos, professores, técnicos.", card="2000")
b("Repare na mudança: o comprador novo não queria açúcar. Queria serviço. Nos anos seguintes, o petróleo chega a uns cem mil barris por dia, e perto de trinta mil profissionais cubanos trabalham na Venezuela, a maioria na saúde.")
b("E o açúcar? Em dois mil e dois, sem o preço antigo, o governo fecha quase metade das usinas. Tente achar outro país que já foi o maior exportador de açúcar do mundo e hoje compra açúcar de fora.")
b("§ Mas um comprador que paga com petróleo depende do próprio petróleo. A Venezuela entra em crise, e os barris diminuem. Em janeiro de dois mil e vinte e seis, depois que forças americanas capturam Nicolás Maduro, o petróleo venezuelano para de chegar.", card="2026")
b("Em dois mil e vinte e cinco, a ilha que já colheu oito milhões e meio de toneladas colheu menos de cento e cinquenta mil. O problema de sempre voltou, agora sem ninguém do outro lado do balcão.")

# ───────────────────────── FECHO ─────────────────────────
cap("Fecho")
b("§ [warm] Então, por que Cuba sempre dependeu de um país só? Porque quem vive de um produto precisa de preço garantido, e só um gigante garante preço. E cada garantia veio com uma cláusula: o estanco, a cota, o alinhamento, os médicos.")
b("As setecentas mil toneladas de mil novecentos e sessenta não mudaram de dono. Mudaram de cláusula.")
b("Talvez Cuba nunca tenha escolhido entre depender ou não. Escolhia de quem. E você, o que acha? Conta nos comentários.")

FALA = [("Bayamo", "Baiámo"), ("Gilberto Girón", "Rilbérto Rirón"), ("Girón", "Rirón"), ("Jesús del Monte", "Rerús del Mônte"),
        ("vegueros", "veguêros"), ("Arango", "Arángo"), ("Camagüey", "Camaguêi"), ("Mikoyan", "Mikoián"), ("Khrushchev", "Krushóv"),
        ("Comecon", "Cômecon"), ("Hugo Chávez", "Úgo Tcháves"), ("Fulgencio Batista", "Fulrrêncio Batísta"), ("Eisenhower", "Áisen-rauer"),
        ("Roosevelt", "Rúsvelt"), ("Guantánamo", "Guantánamo"), ("Nicolás Maduro", "Nicolás Madúro"), ("taínos", "taínos")]
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
