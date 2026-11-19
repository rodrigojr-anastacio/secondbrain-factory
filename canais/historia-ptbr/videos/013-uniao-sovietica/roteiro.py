#!/usr/bin/env python3
"""Fonte única do 013-uniao-sovietica (18/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

10º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
3º com ÂNGULO próprio (ANGULO.md): "a prateleira e o Plano" — cada plano resolve a urgência da vez e deixa a falta que o próximo promete resolver.
EMBALAGEM.md aprovada no crivo r3:
  A/T1 "A URSS chegou ao ESPAÇO. Por que faltava comida?" + thumb rosto-emocao (Iéltsin pasmo diante da fartura, “NEM O POLITBURO”)
  B/T2 "Como o PÃO explica a União Soviética inteira" + thumb objeto-simbolo (avoska vazia diante de prateleiras vazias, "VAI QUE…")
  C/T3 "URSS: o país que pôs o 1º homem no espaço e COMPRAVA trigo" + thumb numero-estatistica ("30 MIL / NA FILA")
Hook: Houston 1989 (controle de missão de manhã, supermercado à tarde, "nem o Politburo tem essa escolha") → 30 mil na fila da lanchonete
  americana (31/01/1990) → trigo de fora desde 1963 → PERGUNTA CENTRAL (≤ 0:45) → "essa é a história inteira… começa com uma promessa de pão".
Fio condutor: A PRATELEIRA. Cada era = uma urgência → o plano que a resolve → a falta que sobra.
  Peça 1 (cap. 3): o plano faz uma coisa enorme de cada vez (aço sim, prateleira depois).
  Peça 2 (cap. 5): foguete é uma ordem; vaca são mil decisões (Riazan).
  Peça 3 (cap. 7): a prateleira enche com dinheiro do petróleo (emprestada).
  Fecho: o foguete é uma ordem só; a prateleira são milhões de escolhas por dia.
"Guarde" único: os americanos da sopa de 1921 (ARA) → pago no cap. 9 (comida de fora de novo: lanchonete americana e reserva de Berlim).
Neutralidade: fomes (1921, 1932–33, 1946–47) e Novocherkassk com números como estimativa, sem humor sobre vítimas, sem imagem gráfica.
KGB/serviço secreto: fora (tema do dossie-es). Golpe e 25/12 em 1 frase cada (consenso da manada).

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1921") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006–012).
Imagens: Codex (canal.yaml visual.gerador: codex; fallback nano-banana). Prompts só de conteúdo; o estilo vem do canal.yaml.
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (006–012: ~128 ppm com pausas)
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
TITULO = "A história INTEIRA da União Soviética"
PERGUNTA = "Como o país que chegou primeiro ao espaço não conseguia encher uma prateleira?"
PROMESSA = ("Por que o país que chegou primeiro ao espaço passou setenta anos sem conseguir encher a prateleira, contado da promessa de pão "
            "de 1917 à fila de 1990, plano por plano (EMBALAGEM.md r3).")
TITULOS = ('T1 "A URSS chegou ao ESPAÇO. Por que faltava comida?" / T2 "Como o PÃO explica a União Soviética inteira" / '
           'T3 "URSS: o país que pôs o 1º homem no espaço e COMPRAVA trigo"')

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None):
    ideia = t.startswith("§")
    if not s: s = (f"ph{len(B):03d}|placeholder",)
    B.append({"t": t.lstrip("§ ").strip(), "s": list(s), "card": card, "ideia": ideia})

# ───────────────────────── HOOK (Houston, 1989) ─────────────────────────
cap("Hook")
b("[curious] Houston, setembro de mil novecentos e oitenta e nove. Imagine que você é Boris Iéltsin, deputado soviético, visitando os Estados Unidos.")
b("De manhã, o controle de missão da NASA. Nada de novo: o seu país pôs o primeiro homem no espaço. À tarde, um supermercado. E ele diz: nem o Politburo tem essa escolha.")
b("Quatro meses depois, em Moscou, cerca de trinta mil pessoas enfrentam a fila de uma lanchonete americana. Num só dia. E o país do Sputnik comprava trigo do exterior desde sessenta e três.")
b("[serious] Então fica a pergunta: como o país que chegou primeiro ao espaço não conseguia encher uma prateleira?")
b("Essa é a história inteira da União Soviética. E ela começa com uma promessa de pão.")

# ───────────────────────── 1. PAZ, TERRA E PÃO ─────────────────────────
cap("1. A promessa do pão")
b("§ Uma aldeia na beira do rio Volga, mil novecentos e dezenove. Homens armados batem na porta. Levam o trigo do celeiro. E levam também a semente da próxima safra.", card="1919")
b("Tente explicar a eles que aquilo era o plantio do ano que vem. Não adianta: a cidade tem fome, e o exército também.")
b("Dois anos antes, os bolcheviques tinham tomado o poder com um lema que cabia num cartaz: paz, terra e pão. Só que a paz virou guerra civil. E o pão virou requisição.")
b("§ Então veio a conta. Em mil novecentos e vinte e um, a fome cobre o Volga. Morrem milhões de pessoas; a estimativa mais citada fala em cerca de cinco milhões.")
b("E quem aparece com comida? Pense na ironia: Herbert Hoover, um americano que detestava os bolcheviques. Só que detestava mais ainda ver criança com fome.", card="1921")
b("No auge, as cozinhas americanas alimentam mais de dez milhões de pessoas por dia. Guarde esses americanos com comida.")
b("O problema é óbvio: um governo que prometeu pão não pode viver da sopa do país que ele chama de inimigo.")

# ───────────────────────── 2. O RECUO ─────────────────────────
cap("2. Um passo atrás")
b("§ Moscou, mil novecentos e vinte e dois. Num mercado de rua, você encontra pão branco, botas, salsicha. Um ano antes, vender isso na rua era crime.", card="1922")
b("Então Lênin recuou. A requisição virou imposto, e o camponês podia vender o que sobrava. A prateleira, por um momento, enche.")
b("No mesmo ano do recuo, nasce um escritório discreto para fazer contas: a Comissão Estatal de Planejamento, o Gosplan. Repare nesse nome: daqui a pouco, ele vai mandar em tudo.")
b("§ Mas aí aparece a tesoura. Os produtos da cidade ficam caros, o trigo fica barato. O que sai da fábrica custa quase três vezes o que custava antes da guerra.")
b("E o camponês responde como você responderia: segura o trigo no celeiro e espera um preço melhor.")
b("Em mil novecentos e vinte e oito, mesmo depois de safras boas, o Estado não consegue comprar grão. As cidades voltam a ter fila. E o homem que agora manda em Moscou, Stálin, tem outra ideia. O problema é que ela não cabe num mercado de rua.")

# ───────────────────────── 3. DOIS MAIS DOIS, CINCO ─────────────────────────
cap("3. Dois mais dois, cinco")
b("§ Olhe para este cartaz de mil novecentos e trinta e um. Em letras vermelhas enormes: dois mais dois igual a cinco.", card="1931")
b("A ideia é que o entusiasmo dos operários faz o plano de cinco anos sair em quatro. Matemática soviética: o resultado vem antes da conta.")
b("O Gosplan agora escreve o país inteiro em metas. Aço, carvão, represas, tratores. Primeiro a indústria pesada. A prateleira? Fica para o próximo plano.")
b("§ E a crise de vinte e oito ganha uma resposta de ferro: se o camponês segura o trigo, o Estado fica com a terra. As fazendas de família viram fazendas coletivas, e o grão passa a ser entregue, não vendido.")
b("[serious] Em agosto de trinta e dois, uma lei transforma em crime grave pegar espigas no campo coletivo, mesmo as que sobraram no chão. Imagine ser preso por catar trigo. Naquele ano e no seguinte, a fome deixa milhões de vítimas, sobretudo na Ucrânia e no Cazaquistão.", card="1932")
b("§ Se você morasse numa cidade, o pão vinha com cartão de racionamento. E o povo aprende a andar com uma sacola de rede no bolso: a avoska. O nome vem de avos, algo como vai que. Vai que aparece alguma coisa.")
b("Em mil novecentos e trinta e cinco, o cartão do pão acaba. E Stálin anuncia: a vida ficou melhor, camaradas. A vida ficou mais alegre. Repare que a sacola continua no bolso.", card="1935")
b("Aqui está a primeira peça da resposta: a prateleira é sempre o próximo plano. O de agora tem uma urgência maior. O problema é quando a urgência maior bate na porta.")

# ───────────────────────── 4. O PLANO VAI À GUERRA ─────────────────────────
cap("4. A fábrica no trem")
b("§ Verão de mil novecentos e quarenta e um. Imagine desmontar a sua fábrica parafuso por parafuso, pôr tudo num trem e remontar do outro lado dos Urais. No inverno.", card="1941")
b("Foi o que aconteceu quando a Alemanha invadiu. Em um ano e pouco, mais de mil e quinhentas grandes fábricas de armamento viajaram para o leste.")
b("Os tanques saem dessas fábricas remontadas no frio. E a prateleira, mais uma vez, fica para o próximo plano.")
b("§ Só que a prateleira paga a conta de novo. Olhe a fila do pão: voltou, e com cartão. E, depois da vitória, uma seca traz outra fome, em mil novecentos e quarenta e seis e quarenta e sete.")
b("Então, em dezembro de quarenta e sete, o racionamento acaba, junto com uma troca de moeda: dez rublos velhos por um novo. Quem escondia dinheiro no colchão descobriu que o colchão tinha encolhido.", card="1947")
b("O plano provou que vence uma guerra. Mas o que ele faz quando não tem guerra para vencer?")

# ───────────────────────── 5. ALCANÇAR A AMÉRICA ─────────────────────────
cap("5. Alcançar a América")
b("§ Leningrado, maio de mil novecentos e cinquenta e sete. Numa reunião sobre agricultura, Nikita Khruschov sobe ao palco e diz: vamos alcançar e ultrapassar a América.", card="1957")
b("Repare: não em foguetes. Em carne, leite e manteiga por habitante. Em poucos anos.")
b("Cinco meses depois, o Sputnik está em órbita. No céu, a América já foi alcançada. No açougue, ainda não.")
b("§ Riazan, mil novecentos e cinquenta e nove. O chefe local do partido, Alexei Larionov, promete triplicar a entrega de carne em um ano. E entrega.", card="1959")
b("Como? Você não vai gostar: comprando carne das regiões vizinhas e abatendo o rebanho às pressas, inclusive vacas leiteiras e de cria. Ganha medalha de herói.")
b("Mas, no ano seguinte, o rebanho da região cai quase dois terços. A carne some. Larionov cai em desgraça e morre poucos meses depois; a versão oficial fala em doença.")
b("§ Khruschov, enquanto isso, visita uma fazenda de milho em Iowa e volta encantado. Agora o país inteiro vai plantar milho. Só que o milho não nasce onde o plano manda; nasce onde o clima deixa.")
b("Segunda peça da resposta: quando a prateleira finalmente vira urgência, a pressa come a semente. Em dezenove, o trigo do plantio. Em cinquenta e nove, as vacas de cria. Só que semente comida não volta no ano seguinte.")

# ───────────────────────── 6. COMUNISMO EM 1980 ─────────────────────────
cap("6. Comunismo com data marcada")
b("§ Moscou, outubro de mil novecentos e sessenta e um. No congresso do partido, o novo programa promete: a base do comunismo estará pronta em mil novecentos e oitenta. Você pode marcar na agenda.", card="1961")
b("Naquele mesmo ano, Gagarin tinha dado a volta na Terra. Parecia que nada era impossível.")
b("§ Mas em maio de sessenta e dois, o governo aumenta o preço da carne em trinta por cento e o da manteiga em vinte e cinco.", card="1962")
b("[serious] Em Novocherkassk, operários de uma fábrica de locomotivas entram em greve. O exército atira. Morrem vinte e seis pessoas, e o país só fica sabendo mais de vinte e cinco anos depois.")
b("§ Aí, em sessenta e três, a colheita falha. E o país que pôs o primeiro homem em órbita faz a primeira grande compra de trigo no exterior: uns seis milhões e meio de toneladas do Canadá.", card="1963")
b("Pense nisso: dois anos depois de Gagarin, o pão de muita mesa soviética atravessava o oceano. E a fábrica soviética continuava ganhando prêmio pela tonelada produzida, não pelo que o povo queria comprar. Quem ia mudar esse placar?")

# ───────────────────────── 7. A PRATELEIRA EMPRESTADA ─────────────────────────
cap("7. A prateleira emprestada")
b("§ Uma resposta tinha saído no jornal. Kharkov, setembro de mil novecentos e sessenta e dois: um professor de economia, Evsei Liberman, publica no Pravda um artigo de título ousado. Plano, lucro, prêmio.", card="1962")
b("A ideia: a fábrica que vende o que o povo quer ganha prêmio. Parece óbvio para você. Em sessenta e cinco, o primeiro-ministro, Alexei Kossyguin, tenta aplicar. A partir de sessenta e oito, a reforma vai sendo esvaziada, sem barulho.", card="1965")
b("§ Então, em mil novecentos e setenta e dois, a União Soviética compra uns dezoito milhões de toneladas de grãos dos Estados Unidos. Os americanos com comida, de novo.", card="1972")
b("E aí você pergunta: foi só uma emergência? Não. Em setenta e cinco, Moscou assina com Washington um acordo de cinco anos: comprar, todo ano, no mínimo seis milhões de toneladas de trigo e milho americanos. A compra de emergência vira contrato.", card="1975")
b("§ A prateleira melhora. Só que a avoska continua no bolso. E a piada da época diz: prometeram o comunismo para oitenta; em oitenta, veio a Olimpíada.", card="1980")
b("Então, em oitenta e dois, o governo lança mais um plano, só para a comida: o Programa Alimentar. Mais um plano para consertar o que o plano anterior não fez.")
b("Terceira peça da resposta: quando a falta aperta de verdade, quem enche a prateleira é alguém de fora. Hoover em vinte e um, o Canadá em sessenta e três, os americanos em setenta e dois. Mas todo socorro tem dono.")

# ───────────────────────── 8. O AÇÚCAR SUMIU ─────────────────────────
cap("8. O açúcar sumiu")
b("§ Maio de mil novecentos e oitenta e cinco. O novo líder, Mikhail Gorbatchov, declara guerra à bebida. As lojas de vodca abrem mais tarde e vendem menos.", card="1985")
b("Mas o povo responde com o que tem em casa: destila a própria bebida. E para isso precisa de açúcar. Resultado: some o açúcar das lojas, e várias cidades passam a racioná-lo.")
b("Você já viu um governo perder dinheiro por vender menos vodca? Esse perdeu uns vinte bilhões de rublos em impostos.")
b("§ E o caixa, que já estava curto, leva mais dois golpes em mil novecentos e oitenta e seis: o preço do petróleo despenca, e explode um reator em Chernobyl.", card="1986")
b("Repare na volta que a história deu: o país que ia alcançar a América em manteiga agora não consegue pôr açúcar na loja. O problema é que, desta vez, todo mundo está vendo.")

# ───────────────────────── 9. DE VOLTA DE HOUSTON ─────────────────────────
cap("9. A volta de Houston")
b("§ Lembra do supermercado do Texas? Iéltsin volta para Moscou. Segundo um assessor, foi ali, entre as gôndolas, que desabou a última coisa que ele ainda acreditava no sistema.", card="1989")
b("E o que você encontraria em casa? Em Leningrado, chá e sabão passam a ser vendidos com talão. E aí entram na lista o açúcar, a vodca e o cigarro.")
b("§ Trinta e um de janeiro de mil novecentos e noventa. Na Praça Púchkin, em Moscou, abre a lanchonete americana do começo do vídeo. Cerca de trinta mil pessoas passam pelo balcão no primeiro dia.", card="1990")
b("Um sanduíche custa uns quatro rublos. Pense: mais de meio dia de salário. Mas mesmo assim a fila dá voltas na praça, no frio.")
b("§ Em dezembro de noventa, a Alemanha começa a mandar comida para Moscou. Parte vem da reserva de Berlim, um estoque criado por causa do bloqueio soviético de quarenta e oito.")
b("Lembra dos americanos com comida no Volga? Setenta anos depois, a comida de fora voltou. Só que agora vinha do estoque que existia por causa de Moscou.")
b("E um Estado que não consegue alimentar as próprias cidades fica sem resposta quando as repúblicas perguntam: por que ficar?")

# ───────────────────────── 10. O ÚLTIMO PLANO ─────────────────────────
cap("10. O último preço")
b("§ Dois de abril de mil novecentos e noventa e um. De um dia para o outro, o governo dobra os preços. Alguns triplicam. Imagine acordar e o seu pão custar o triplo.", card="1991")
b("Mesmo assim, as prateleiras continuam vazias. E a avoska, depois de sessenta anos no bolso, continua voltando para casa leve.")
b("§ Em agosto, uma tentativa de golpe fracassa em três dias. Em vinte e cinco de dezembro, a União Soviética deixa de existir.")
b("Aí, em janeiro de noventa e dois, a Rússia solta os preços. Em semanas, a prateleira enche. Cara, quase impossível de pagar. Mas enche.", card="1992")

# ───────────────────────── FECHO (≤ 45 s) ─────────────────────────
cap("Fecho")
b("§ Então, como o país que chegou primeiro ao espaço não conseguia encher uma prateleira? Porque a prateleira era sempre o próximo plano. E quando ela virava urgência, ou a pressa comia a semente, ou alguém de fora enchia.")
b("Talvez a pergunta certa nunca tenha sido por que faltava comida. Era quem decide o que vai na sua sacola. [break] Em dois mil e vinte e dois, a lanchonete da Praça Púchkin reabriu com outro nome.", card="2022")
b("[warm] Na sua casa, alguém tinha uma sacola do vai que? Conta nos comentários.")

# Grafia para a VOZ (o Fish lê como português). Conferir no teste de nomes (qa/pronuncia/).
# blocos.json leva "texto" (falado, vai ao Fish) e "tela" (grafia correta: legendas e SCRIPT).
FALA = [("Iéltsin", "Iéltsin"), ("Khruschov", "Khruchóv"), ("Kossyguin", "Kossíguin"), ("Gorbatchov", "Gorbatchóv"),
        ("Novocherkassk", "Novotcherkásk"), ("Riazan", "Riazã"), ("Larionov", "Larionóv"), ("Gosplan", "Gósplan"),
        ("avoska", "avóska"), ("avos", "ávos"), ("Púchkin", "Púchkin"), ("Herbert Hoover", "Hérbert Húver")]
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
