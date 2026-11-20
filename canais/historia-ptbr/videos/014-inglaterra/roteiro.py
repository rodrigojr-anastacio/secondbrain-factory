#!/usr/bin/env python3
"""Fonte única do 014-inglaterra (20/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

11º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
4º com ÂNGULO próprio (ANGULO.md): "a coroa que vem de fora" — seis coroas para gente de fora; cada rei de fora paga com um pedaço de poder no papel;
o papel vira Parlamento, crédito, frota e império.
EMBALAGEM.md aprovada no crivo r3:
  A/T1 "A Inglaterra IMPORTAVA reis. Como mandou em 1/4 do mundo?" + thumb rosto-emocao (Jaime VI de manta xadrez se coroando, "MINHA!")
  B/T2 "Como reis de FORA deixaram a Inglaterra mais forte" + thumb cena-acao (coroação de Natal de 1066 com fogo lá fora, "NATAL DE 1066")
  C/T3 "Inglaterra, o país que dava a COROA a estrangeiros" + thumb documento-evidencia (Declaração de Direitos circulada, "O PREÇO")
Hook: Carey galopa 60 h (1603) → "o rei da Inglaterra agora é um escocês" (≤ 0:30) → PERGUNTA CENTRAL (≤ 0:50) → tomaram × receberam,
  Natal com fogo → o preço concreto (imposto só com licença) (≤ 1:00) → "essa é a história inteira… numa ilha que todo mundo atravessa".
Peças da resposta: 1 (cap. 3) rei que precisa de dinheiro precisa pedir, e quem é pedido aprende a cobrar; 2 (cap. 7) o papel que amarra
  o rei de fora deixa o país confiável para pedir emprestado; 3 (cap. 9) a coroa vem de fora, o poder fica dentro, no papel, e o papel paga a frota.
"Guarde" único: a promessa no estandarte de 1688 → paga no cap. 10 (juramento de Carlos III, 2023).
Neutralidade: execução de 1649, colonialismo e fome irlandesa com contexto, sem imagem gráfica. Mitos evitados: Jorge I "sem inglês",
  "saiu do gabinete pela língua", Walpole "primeiro-ministro" sem ressalva, ondas de Canuto (contada como lenda e no sentido original).

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1066") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006–013).
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
TITULO = "A história INTEIRA da Inglaterra"
PERGUNTA = "Como um país que vivia buscando rei lá fora acabou mandando em um quarto do mundo?"
PROMESSA = ("Como a Inglaterra entregou a coroa a gente de fora seis vezes, e como o preço cobrado de cada rei estrangeiro virou a força "
            "que mandou em um quarto do mundo (EMBALAGEM.md r3).")
TITULOS = ('T1 "A Inglaterra IMPORTAVA reis. Como mandou em 1/4 do mundo?" / T2 "Como reis de FORA deixaram a Inglaterra mais forte" / '
           'T3 "Inglaterra, o país que dava a COROA a estrangeiros"')

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

# ───────────────────────── HOOK (Carey, 1603) ─────────────────────────
cap("Hook")
b("[curious] Palácio de Richmond, março de mil seiscentos e três. Imagine que você é Robert Carey, um nobre inglês. A rainha Elizabeth acabou de morrer, sem filhos.", card="1603")
b("Você monta e galopa para o norte. Sessenta horas, até Edimburgo, para dar a notícia: o rei da Inglaterra agora é um escocês. O vizinho da guerra de sempre.")
b("[serious] E aí fica a pergunta: como um país que vivia buscando rei lá fora acabou mandando em um quarto do mundo?")
b("Porque não foi a primeira vez. Um dinamarquês e um normando tomaram a coroa à força; o normando, coroado num Natal em que a vizinhança pegava fogo. Um francês, um holandês e um alemão a receberam.")
b("E cada um pagou um preço. Um deles teve de aceitar, por escrito, que não cobraria um centavo de imposto sem pedir licença.")
b("Essa é a história inteira da Inglaterra. E começa numa ilha que todo mundo atravessa.")

# ───────────────────────── 1. A ILHA QUE TODO MUNDO ATRAVESSA ─────────────────────────
cap("1. A ilha que todo mundo atravessa")
b("§ Mil e dezesseis. Um dinamarquês, Canuto, senta no trono da Inglaterra. Ele também manda na Dinamarca e na Noruega: a ilha vira província de um império do mar do Norte.", card="1016")
b("Não era novidade. Antes dele, atravessaram o mar os romanos, depois os anglos e os saxões, depois os vikings. Alfredo, o Grande, segurou os vikings no sul. Mas a ilha seguia sendo onde todo mundo desembarcava.")
b("Só que deixava marca. Se você já disse sky, egg ou knife, falou palavras dos vikings.")
b("§ Conta uma lenda, escrita uns cem anos depois, que Canuto mandou o mar recuar. A versão que você conhece é a do rei arrogante. Só que a lenda original diz o contrário: ele molha os pés de propósito, para mostrar aos bajuladores que rei nenhum manda nas ondas.")
b("Repare no recado: rei de fora, para ser aceito, tinha de parecer menor.")
b("Canuto morre em mil e trinta e cinco, os filhos brigam e a coroa volta para um inglês. O problema é que, do outro lado do canal, um parente normando achava que ela era dele.")

# ───────────────────────── 2. GRITOS EM DUAS LÍNGUAS ─────────────────────────
cap("2. Gritos em duas línguas")
b("§ Abadia de Westminster, Natal de mil e sessenta e seis. Guilherme da Normandia, que venceu em Hastings dois meses antes, vai ser coroado.", card="1066")
b("Lá dentro, um bispo pergunta em francês se aceitam o novo rei, e um arcebispo repete em inglês. A igreja inteira grita que sim.")
b("Só que, do lado de fora, os guardas normandos não entendem os gritos. Acham que é revolta e põem fogo nas casas vizinhas. A igreja esvazia, e um cronista conta que Guilherme terminou a cerimônia tremendo.")
b("Já aplaudiu um discurso numa língua que você não entende? Aqueles guardas fizeram o contrário: ouviram aplauso e entenderam ataque.")
b("§ Então o normando faz o que conquistador faz: castelo de pedra e terra para os seus. Vinte anos depois, manda contar o reino inteiro, até os porcos, num livro de impostos. Imagine o fiscal contando as suas galinhas.")
b("E a corte fala francês por uns três séculos. O problema: o rei da Inglaterra agora também era senhor na França, e o dinheiro atravessava o canal na direção errada.")

# ───────────────────────── 3. O REI PRESO NA ILHA ─────────────────────────
cap("3. O rei preso na ilha")
b("§ Ruão, junho de mil duzentos e quatro. A capital da Normandia se rende ao rei da França. O rei João perde a terra de onde a família tinha vindo.", card="1204")
b("João era filho de Henrique Segundo, um francês nascido em Le Mans, que herdou a Inglaterra por acordo e chegou a mandar em metade da França.")
b("Agora imagine o problema dele: preso na ilha, querendo a Normandia de volta e sem dinheiro. A solução de sempre? Imposto. E mais imposto.")
b("§ Então os barões se cansam. Em mil duzentos e quinze, obrigam João a aceitar a Magna Carta: imposto extraordinário, só com o conselho do reino. O papa anula em semanas, mas o papel volta, reeditado, várias vezes.", card="1215")
b("Mas quem dá o passo seguinte é outro estrangeiro. Simon de Montfort, nobre nascido na França e cunhado do rei, lidera uma revolta. Em mil duzentos e sessenta e cinco, chama para o parlamento não só barões, mas gente das cidades.", card="1265")
b("Aqui está a primeira peça da resposta: rei que precisa de dinheiro precisa pedir. E quem é pedido aprende a cobrar. Você mesmo: quando alguém te pede um favor grande, não pede nada em troca?")
b("O problema é que esse país que cobrava o rei ainda fazia isso em francês.")

# ───────────────────────── 4. A LÍNGUA VOLTA ─────────────────────────
cap("4. A língua volta")
b("§ Westminster, mil trezentos e sessenta e dois. O Parlamento aprova uma lei: nos tribunais, a partir de agora, se fala inglês. O detalhe é ótimo: a lei foi escrita em francês.", card="1362")
b("Imagine ser julgado numa língua que você não entende: era a vida do camponês inglês. E havia um motivo a mais, porque a Inglaterra estava em guerra com a França, a Guerra dos Cem Anos.")
b("§ Em mil trezentos e noventa e nove, Henrique Quarto reivindica o trono diante do Parlamento. Em inglês. Só que a guerra termina, em mil quatrocentos e cinquenta e três, com quase tudo perdido na França.", card="1399")
b("Então a briga vira caseira: Lancaster contra York, trinta anos de Guerra das Rosas.")
b("E quem ganha? Mais um que vinha de fora. Henrique Tudor, criado no exílio, desembarca em Gales em mil quatrocentos e oitenta e cinco, com mercenários franceses, e vence.", card="1485")
b("O novo rei chega com uma meta: nunca mais depender de barão. O problema é que, para isso, a família dele também ia precisar do Parlamento.")

# ───────────────────────── 5. O REI FORTE QUE PRECISOU DO PAPEL ─────────────────────────
cap("5. O rei forte que precisou do papel")
b("§ Londres, mil quinhentos e vinte e nove. Henrique Oitavo, filho do Tudor, quer anular o casamento, e o papa diz não. Imagine o rei mais poderoso da Inglaterra esperando licença de Roma.", card="1529")
b("Então ele faz uma coisa nova: em vez de brigar sozinho, chama o Parlamento. Por sete anos, lei após lei, o Parlamento corta os laços com Roma. Em mil quinhentos e trinta e quatro, faz do rei o chefe da Igreja da Inglaterra.", card="1534")
b("Só que repare: se uma lei do Parlamento muda até a religião do país, o que ela não pode mudar? E as terras dos mosteiros, vendidas, vão parar com gente que senta no Parlamento.")
b("Pense em emprestar a chave da sua casa para alguém regar as plantas. Depois, vai ser difícil pedir de volta.")
b("§ A filha de Henrique, Elizabeth, reina quase quarenta e cinco anos, enfrenta a Armada espanhola e nunca se casa. E voltamos ao galope do começo: sem herdeiro, a coroa vai para o vizinho do norte.", card="1588")
b("O problema: o escocês que chegava acreditava que rei só presta contas a Deus.")

# ───────────────────────── 6. O NOME RECUSADO ─────────────────────────
cap("6. O nome recusado")
b("§ Londres, abril de mil seiscentos e quatro. O novo rei, Jaime, pede à Câmara dos Comuns um título novo: rei da Grã-Bretanha. E os Comuns dizem não.", card="1604")
b("Lembra do escocês do começo? Ele esperava esse trono havia anos, e trocava até cartas secretas com o ministro da rainha. Só não esperava o não. Assume o título por proclamação, mas o recado estava dado.")
b("§ Buckinghamshire, mil seiscentos e trinta e sete. O fidalgo John Hampden se recusa a pagar vinte xelins da taxa dos navios, que o filho de Jaime, Carlos Primeiro, cobra sem Parlamento. Perde no tribunal por sete votos a cinco. E vira herói.", card="1637")
b("Carlos governa onze anos sem Parlamento. Imagine o síndico cobrando taxa extra sem assembleia por onze anos. Até que, em mil seiscentos e quarenta, falta dinheiro para guerrear com os escoceses, e a assembleia volta. Agora ponha exércitos nessa reunião.", card="1640")
b("[serious] O resultado é uma guerra civil. Em mil seiscentos e quarenta e nove, o rei é julgado e executado em Londres. E por onze anos a Inglaterra fica sem rei.", card="1649")
b("Lembra da nossa pergunta? Ela acabou de ficar mais estranha: o país que vai mandar no mundo está sem rei nenhum. Em mil seiscentos e sessenta, a monarquia volta. O problema é que, quando o rei seguinte vira católico, a ilha protestante vai procurar outro. Lá fora.", card="1660")

# ───────────────────────── 7. A INVASÃO POR CONVITE ─────────────────────────
cap("7. A invasão por convite")
b("§ Novembro de mil seiscentos e oitenta e oito. Na costa sul da Inglaterra, desembarca um exército holandês. Nos estandartes, segundo os relatos, em vez de ameaça, uma promessa: as liberdades da Inglaterra e a religião protestante.", card="1688")
b("Quem chegava era Guilherme de Orange, holandês e genro do rei. Convidado: sete ingleses poderosos tinham escrito pedindo que viesse. O rei católico, Jaime Segundo, foge para a França. Guarde essa promessa no estandarte.")
b("§ Então, em fevereiro de mil seiscentos e oitenta e nove, Guilherme e a mulher, Maria, ouvem a leitura de uma declaração: sem o Parlamento, o rei não cobra imposto nem mantém exército em tempo de paz. E aceitam a coroa.", card="1689")
b("E aqui muda tudo. Guilherme queria guerra contra a França, e guerra custa caro. Em mil seiscentos e noventa e quatro, um grupo de comerciantes funda o Banco da Inglaterra e empresta ao governo um milhão e duzentas mil libras, a oito por cento.", card="1694")
b("Por que emprestar? Porque um rei sozinho podia dar calote. Um Parlamento de proprietários e comerciantes, os próprios credores, pagava. É como o seu crédito no banco: se você paga em dia, o juro cai.")
b("Segunda peça da resposta: o papel que amarrava o rei de fora deixou o país confiável para pedir emprestado. O problema é que a rainha Ana morre sem filhos vivos, e a lei manda buscar o próximo protestante na Alemanha.")

# ───────────────────────── 8. O REI QUE PRECISA DE LICENÇA ─────────────────────────
cap("8. O rei que precisa de licença")
b("§ Mil setecentos e um. O Parlamento escreve as regras para um rei que ainda nem chegou. Protestante. Nada de guerra pelas terras dele lá fora sem o Parlamento. E nem sair da ilha sem licença.", card="1701")
b("Imagine o seu chefe novo chegando com a lista do que ele não pode fazer. Assim chega, em mil setecentos e catorze, Jorge de Hanôver. Fala pouco inglês e prefere o francês. Dois anos depois, pede para visitar a terra dele, e o Parlamento revoga a cláusula.", card="1714")
b("§ Com o tempo, Jorge deixa de ir às reuniões com os ministros. Aí quem senta na cabeceira é Robert Walpole, chefe do Tesouro por vinte e um anos: o que hoje chamamos de primeiro-ministro. Ele mesmo recusava o título; soava como ofensa.", card="1721")
b("Então o crédito barato vira navio. A dívida do país se multiplica por mais de dez em menos de cem anos. Quase tudo vira frota.")
b("Em mil setecentos e sessenta e três, a Grã-Bretanha, já unida à Escócia, vence a França e fica com o Canadá e o caminho da Índia. Só que essa conta também precisava de alguém para pagar.", card="1763")

# ───────────────────────── 9. A MEDALHA QUE FICOU NA FRANÇA ─────────────────────────
cap("9. A medalha que ficou na França")
b("§ Agora olhe para esta medalha francesa de mil oitocentos e quatro. A inscrição diz: descida na Inglaterra, cunhada em Londres. Foi feita antes da invasão. A invasão nunca veio.", card="1804")
b("É como você mandar bordar a faixa de campeão antes da final. Napoleão tinha um exército enorme em Boulogne. Mas a frota paga com a dívida venceu em Trafalgar, em mil oitocentos e cinco, e a medalha ficou na França.", card="1805")
b("Vinte anos antes, a mesma conta tinha custado a América. Londres taxou as colônias, e os colonos responderam com o velho argumento inglês: sem representação, sem imposto. Em mil setecentos e oitenta e três, eles se foram.")
b("§ Então o crédito, a frota e o carvão das fábricas fazem o resto. No começo do século vinte, o império britânico ocupa perto de um quarto das terras do mundo, com uns quatrocentos e cinquenta milhões de pessoas.", card="1922")
b("[serious] Muita gente pagou caro por esse império, da Índia à Irlanda: fomes, guerras e governos que ninguém escolheu.")
b("E no trono, no auge? A rainha Vitória, neta de um rei de Hanôver, casada com o príncipe alemão Alberto. Em casa, os dois falavam alemão.")
b("Terceira peça da resposta: a coroa vinha de fora, mas o poder ficava do lado de dentro, no papel. E foi o papel que pagou a frota. O problema é que, em mil novecentos e catorze, o inimigo passa a ser justamente a Alemanha.", card="1914")

# ───────────────────────── 10. A CONTA ─────────────────────────
cap("10. A conta chega")
b("§ Washington, mil novecentos e quarenta e cinco. A guerra acabou, e o país que emprestou ao mundo por dois séculos agora pede: quase quatro bilhões de dólares aos americanos.", card="1945")
b("No meio do caminho, em mil novecentos e dezessete, o rei Jorge Quinto tinha trocado o nome alemão da família por um bem inglês: Windsor. A coroa de fora agora queria parecer de dentro.", card="1917")
b("§ Então o império encolhe. A Índia fica independente em mil novecentos e quarenta e sete. Em setenta e três, o país entra no mercado comum europeu; em dois mil e dezesseis, vota para sair.", card="1947")
b("Só que a conta demorou: a última parcela foi paga em vinte e nove de dezembro de dois mil e seis. Imagine quitar em dois mil e seis uma conta de quarenta e cinco.", card="2006")
b("§ Seis de maio de dois mil e vinte e três. Carlos Terceiro, descendente direto daquele Jorge de Hanôver, é coroado em Westminster. Antes da coroa, faz um juramento: governar os seus povos segundo as leis e os costumes deles.", card="2023")
b("Lembra da promessa no estandarte de mil seiscentos e oitenta e oito? Você acabou de ouvi-la de novo. Quem promete é o rei; quem cobra é o Parlamento.")

# ───────────────────────── FECHO (≤ 45 s) ─────────────────────────
cap("Fecho")
b("§ Então, como um país que vivia buscando rei lá fora acabou mandando em um quarto do mundo? Porque cada rei de fora chegava precisando dos ingleses e pagava com um pedaço de poder escrito no papel. O papel virou crédito; o crédito, frota; a frota, império.")
b("Talvez a pergunta certa nunca tenha sido por que eles importavam reis. Era por que podiam: o rei já não era quem mandava. [break] Hoje, o Parlamento continua a poucos passos da abadia onde Guilherme tremeu.")
b("[warm] Qual desses reis de fora você não conhecia? Conta nos comentários.")

# Grafia para a VOZ (o Fish lê como português). Conferir no teste de nomes (qa/pronuncia/).
# blocos.json leva "texto" (falado, vai ao Fish) e "tela" (grafia correta: legendas e SCRIPT).
FALA = [("Robert Carey", "Róbert Kéri"), ("Richmond", "Rítchmond"), ("Canuto", "Canúto"), ("sky, egg ou knife", "scái, égue ou náife"),
        ("Westminster", "Uéstminster"), ("Hastings", "Hêistings"), ("Ruão", "Ruão"), ("Le Mans", "Le Mã"), ("Simon de Montfort", "Simón de Monfór"),
        ("Calais", "Calê"), ("Lancaster", "Lâncaster"), ("York", "Iórque"), ("Tudor", "Túdor"), ("Orange", "Orânge"),
        ("Hanôver", "Hanôver"), ("Walpole", "Uólpol"), ("Boulogne", "Bulônhe"), ("Trafalgar", "Trafalgár"), ("Windsor", "Uíndsor"),
        ("Washington", "Uóchinton"), ("John Hampden", "Djón Rêmpden"), ("Buckinghamshire", "Bâkinghamxer")]
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
