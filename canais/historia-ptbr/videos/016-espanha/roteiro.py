#!/usr/bin/env python3
"""Fonte única do 016-espanha (21/11/2026): roteiro + planos. Gera SCRIPT.md, blocos.json, cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

13º vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
6º com ÂNGULO próprio (ANGULO.md): "a costura" — o casamento de 1469 junta coroas, não países; o Novo Mundo é de Castela e o império
adia a costura; quando o dinheiro aperta, Madri costura à força (1624–1640, 1707–1717) e cada costura deixa alguém de fora
(foros bascos e navarros, a América de Cádis, os nacionalismos acelerados por 1898) até a costura assinada de 1978.
EMBALAGEM.md aprovada no crivo r3:
  A/T1 "A Espanha juntou meio mundo. Por que não juntava a si mesma?" + thumb rosto-emocao (rei com pilha de coroas, "REI DAS ESPANHAS")
  B/T2 "Por que a Espanha cobrava ALFÂNDEGA de si mesma até 1841?" + thumb conflito-xvy (fiscal castelhano × mercador navarro, "CASTELA × NAVARRA")
  C/T3 "Espanha: o império que ainda não era um país" + thumb objeto-simbolo (coroa partida e costurada, "1469")
Hook: Fernando disfarçado + licença falsa (1469) → "junta duas coroas… não dois países: lei, alfândega, moeda" (≤ 0:35) → PERGUNTA CENTRAL (≤ 0:50)
  → "rei das Espanhas, no plural, uma pilha de coroas" + "última alfândega de dentro só caiu em 1841" (≤ 1:05) → "essa é a história inteira".
Peças da resposta: 1 (cap. 4) nasceu de casamento, herança e acaso; 2 (cap. 6) quando o dinheiro apertou, costura à força arrebenta;
  3 (cap. 8) cada costura decide antes quem conta. Fecho: o mundo veio primeiro e pagou a conta.
"Guarde" único: o plural "Espanhas" → pago no cap. 5 (HISPANIARVM REX) e no fecho/cap. 10 (rei da Espanha, art. 56).
Neutralidade: Corpus de Sang, guerras carlistas, Guerra Civil, Franco, 2017 com contexto e sem lado. Mitos evitados: "Tanto monta" como lema
  dos dois, "catalães proibidos por lei de ir à América", "1898 criou os nacionalismos", "Bórgia trouxe a bula", "sol nunca se põe" como citação.

Sintaxe dos planos (campo s):
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1066") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006–014).
Imagens: Codex (canal.yaml visual.gerador: codex; fallback nano-banana). Prompts só de conteúdo; o estilo vem do canal.yaml.
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (006–014: ~128–130 ppm com pausas)
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
TITULO = "A história INTEIRA da Espanha"
PERGUNTA = "Por que a Espanha juntou meio mundo antes de conseguir juntar a si mesma?"
PROMESSA = ("Por que a Espanha juntou meio mundo antes de conseguir juntar a si mesma: o casamento de coroas, as alfândegas e moedas "
            "de dentro até 1717 e 1841, o rei das Espanhas no plural e cada costura que deixou alguém de fora (EMBALAGEM.md r3).")
TITULOS = ('T1 "A Espanha juntou meio mundo. Por que não juntava a si mesma?" / T2 "Por que a Espanha cobrava ALFÂNDEGA de si mesma até 1841?" / '
           'T3 "Espanha: o império que ainda não era um país"')

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


# ───────────────────────── HOOK (o noivo disfarçado, 1469) ─────────────────────────
cap("Hook")
b("[curious] Castela, outubro de mil quatrocentos e sessenta e nove. Imagine que você é um príncipe de dezessete anos, viajando à noite disfarçado de criado.", card="1469")
b("Você é Fernando, herdeiro de Aragão, e vai casar escondido com Isabel, herdeira de Castela. Com uma licença do papa falsa, assinada por um papa morto havia cinco anos.")
b("O casamento junta duas coroas. Mas não junta dois países: cada lado fica com a sua lei, a sua alfândega, a sua moeda. E esse país pela metade logo ganha um mundo inteiro.")
b("[serious] Então fica a pergunta: por que a Espanha juntou meio mundo antes de conseguir juntar a si mesma?")
b("Porque, por séculos, o rei foi rei das Espanhas, no plural: uma pilha de coroas numa cabeça só. E a última alfândega de dentro só caiu em mil oitocentos e quarenta e um.")
b("Essa é a história inteira da Espanha. Guarde esse plural. E tudo começa numa península que nunca teve um dono só.")

# ───────────────────────── 1. A COSTURA POR CIMA ─────────────────────────
cap("1. A costura por cima")
b("§ Toledo, ano quinhentos e oitenta e nove. Recaredo, rei dos visigodos, reúne os bispos e diz: daqui em diante, uma fé só. Ele troca a sua pela dos súditos.", card="589")
b("Faz sentido, porque os visigodos eram poucos: uma minoria mandando em milhões de hispano-romanos, que falavam latim desde Roma. Rezar igual era o jeito de virar um povo.")
b("Só que toda costura por cima deixa alguém de fora. Nas décadas seguintes, reis de Toledo forçam judeus ao batismo. Imagine viver num reino que quer você igual, ou fora.")
b("§ Mas essa costura não aguenta o primeiro puxão. Em setecentos e onze, um exército do norte da África atravessa o estreito, e o reino visigodo cai em poucos anos.", card="711")
b("Quase toda a península vira al-Andalus. Se você olhar o mapa, aos cristãos sobra uma faixa de montanhas no norte.")
b("O problema é que, nessa faixa, ninguém vai ser dono de tudo. Vão ser vários donos. E cada um com filhos.")

# ───────────────────────── 2. A HERANÇA QUE SE PARTE ─────────────────────────
cap("2. A herança que se parte")
b("§ Leão, dezembro de mil e sessenta e cinco. Fernando Primeiro, o rei mais poderoso do norte cristão, está no fim da vida. Então faz o que todo pai rico fazia: divide a herança.", card="1065")
b("Castela para um filho, Leão para outro, a Galícia para o terceiro. Em poucos anos, os irmãos estão em guerra.")
b("Pense numa família que herda um terreno e, em vez de uma casa, levanta três muros. Era assim, porque o reino era patrimônio, e patrimônio se repartia.")
b("§ Aí cada geração junta e reparte de novo. Leão e Castela se separam em mil cento e cinquenta e sete e só voltam a se unir em mil duzentos e trinta. Portugal, nesse meio-tempo, vai embora de vez.", card="1157")
b("Enquanto a guerra contra al-Andalus desce para o sul, sobram quatro coroas cristãs, Portugal, Castela, Aragão e Navarra, e Granada, muçulmana. Mas sobra também o hábito: tudo o que se junta pode se partir no próximo enterro.")

# ───────────────────────── 3. DOIS NOIVOS, DOIS PAÍSES ─────────────────────────
cap("3. Dois noivos, dois países")
b("§ Estrada de Castela para Saragoça, mil quatrocentos e oitenta. Imagine que você é um mercador de lã. Na fronteira, uma alfândega: você para, abre os fardos e paga.", card="1480")
b("Até aí, normal. Só que, desde mil quatrocentos e setenta e nove, os dois lados têm os mesmos reis: Isabel e Fernando, o casal do casamento escondido. E mesmo assim você paga para passar de um reino deles para o outro.")
b("E, depois da cancela, muda o dinheiro. Em Castela se conta em maravedis; em Barcelona, em libras e soldos. Cem mil maravedis valiam seis mil e quatrocentos soldos. Tente pagar um pastel assim.")
b("§ Acontece que o casamento uniu pessoas, não leis. Cada reino ficou com as suas Cortes, os seus tribunais, os seus impostos. Em Castela, a dona da coroa era Isabel. Em Aragão, era Fernando.")
b("Os historiadores chamam isso de monarquia composta: vários países, cada um com o seu contrato. Funcionava, mas só enquanto ninguém pedisse demais.")
b("Então, em mil quatrocentos e noventa e dois, esse arranjo ganha um pedaço novo, do outro lado do Atlântico. O problema: de quem ele é?")

# ───────────────────────── 4. O MUNDO É DE CASTELA ─────────────────────────
cap("4. O mundo é de Castela")
b("§ Sevilha, janeiro de mil quinhentos e três. Os reis criam a Casa de Contratação: todo navio para as Índias sai dali e volta para ali, registrado, pesado e taxado.", card="1503")
b("Se você já mandou uma encomenda para fora, sabe que tudo passa por um balcão. A América inteira passava por um só, em Castela.")
b("Porque as terras que Colombo achou foram incorporadas à coroa de Castela, não à de Aragão. Para quem era de Barcelona, chegar à América era, na prática, bem mais difícil.")
b("Repare no calendário: no ano de Colombo, Castela também toma Granada, o último reino muçulmano da península. Um ano, dois troféus, e nenhum é da Espanha.")
b("§ Mas, em mil quinhentos e quatro, Isabel morre, e Castela vai para a filha, Joana. Fernando, viúvo, casa de novo, com uma princesa francesa, Germana de Foix.", card="1509")
b("Em três de maio de mil quinhentos e nove, nasce um menino. Se ele vivesse, herdaria Aragão, e as duas coroas provavelmente se separariam de novo. O bebê vive poucas horas.")
b("Aqui está a primeira peça da resposta: a Espanha não nasceu de um plano. Nasceu de um casamento, de uma herança e de um acaso. Só que o acaso entregou tudo a um rapaz que mal falava castelhano.")

# ───────────────────────── 5. O REI DE UMA LISTA ─────────────────────────
cap("5. O rei de uma lista")
b("§ Astúrias, setembro de mil quinhentos e dezessete. Uma frota desviada pela tempestade despeja, numa vila de pescadores, um rapaz criado em Flandres. Conta-se que os moradores, assustados com tanta vela, acharam que era um ataque.", card="1517")
b("É Carlos, neto de Isabel e Fernando, o novo rei. Ou melhor, os novos reis: de Castela, de Aragão, de Navarra, de Nápoles, das Índias.")
b("Imagine assinar o seu nome e precisar de uma linha inteira só para os títulos. As moedas do filho dele, Filipe Segundo, resumem em latim: rei das Espanhas.")
b("§ E quem pagava tudo isso? Castela. A prata da América entrava por Sevilha, os impostos castelhanos subiam, e as guerras na Europa engoliam os dois. Os outros reinos davam pouco.")
b("Era o império que ainda não era um país: o rei mandava do México às Filipinas, mas, para cobrar imposto em Saragoça, você imagina: precisava negociar.")
b("§ Em mil quinhentos e noventa e um, Filipe testa o limite. O ex-secretário Antonio Pérez foge para Aragão e se protege atrás do foro aragonês. Aí o rei manda um exército, e o Justiça de Aragão, o juiz que defendia os foros, é executado.", card="1591")
b("Mas Filipe não apaga os foros, só os aperta. O problema fica para o neto, e o neto tinha um ministro com um plano.")

# ───────────────────────── 6. A CONTA ─────────────────────────
cap("6. A conta")
b("§ Madri, Natal de mil seiscentos e vinte e quatro. Enquanto a corte festeja, o conde-duque de Olivares, ministro de Filipe Quarto, entrega um memorial secreto.", card="1624")
b("Olivares escreveu ao rei, sem rodeio: o negócio mais importante da sua monarquia é fazer-se rei da Espanha. Ou seja, reduzir os outros reinos ao estilo e às leis de Castela.")
b("Faz sentido para quem paga a conta, porque Castela estava exausta. Então, em mil seiscentos e vinte e seis, vem a União de Armas: cada reino manda soldados. Castela, quarenta e quatro mil. Catalunha e Portugal, que tinha o mesmo rei desde mil quinhentos e oitenta, dezesseis mil cada.")
b("Pense no seu condomínio, com o síndico decidindo sozinho a cota de cada apartamento. A Catalunha recusa.")
b("§ Em junho de mil seiscentos e quarenta, com soldados aquartelados nas casas, os ceifeiros que chegam a Barcelona se revoltam, e o vice-rei não sai vivo da fuga. Em dezembro, Portugal aclama um rei próprio.", card="1640")
b("Em janeiro seguinte, a Catalunha se põe sob o rei da França. Madri leva doze anos para retomar Barcelona e, em mil seiscentos e cinquenta e nove, entrega o Rossilhão aos franceses. Portugal não volta.")
b("Aqui está a segunda peça da resposta: quando o dinheiro apertou, Madri tentou costurar à força, e a costura arrebentou dos dois lados. Lembra da nossa pergunta? Ela acabou de ficar mais difícil.")
b("Só que a costura à força ia voltar. Desta vez, com uma guerra europeia inteira por trás.")

# ───────────────────────── 7. DIREITO DE CONQUISTA ─────────────────────────
cap("7. Direito de conquista")
b("§ Madri, vinte e nove de junho de mil setecentos e sete. Filipe Quinto, o primeiro rei Bourbon, assina um decreto que acaba com as leis de Aragão e de Valência. E o motivo vem escrito: o justo direito de conquista.", card="1707")
b("Como se chega aí? O último Habsburgo morreu sem filhos. Castela apoiou o neto do rei da França; boa parte de Aragão, um arquiduque austríaco. Aragão perdeu a guerra, então pagou com as leis.")
b("§ Barcelona resiste até onze de setembro de mil setecentos e catorze, data lembrada até hoje. Em mil setecentos e dezesseis, acabam as instituições catalãs, e o castelhano entra no tribunal.", card="1714")
b("E, em mil setecentos e dezessete, as alfândegas entre Castela e Aragão vão para a costa. Se você fosse aquele mercador de lã, agora passaria sem parar. Só levou duzentos e trinta e oito anos de fila.")
b("Mas repare em quem ficou fora da conquista: o País Basco e Navarra. Tinham apoiado Filipe, então não havia o que conquistar, e mantiveram foros, alfândegas e impostos próprios. O problema: a costura à força deixou, de propósito, dois botões soltos.")

# ───────────────────────── 8. OS ESPANHÓIS DOS DOIS HEMISFÉRIOS ─────────────────────────
cap("8. Os espanhóis dos dois hemisférios")
b("§ Cádis, março de mil oitocentos e doze. Napoleão pôs o irmão no trono em Madri, e a cidade está cercada. Lá dentro, deputados escrevem uma constituição.", card="1812")
b("O artigo primeiro é a costura mais ambiciosa de todas: a nação espanhola é a reunião de todos os espanhóis de ambos os hemisférios. Imagine: Madri, Lima, México e Manila, um país só.")
b("Só que a conta tinha um truque. O número de deputados vinha da população, mas quem tinha origem africana ficava fora da conta. Na América, era muita gente, então os americanos ficavam em minoria no país que dizia ser deles também.")
b("Imagine ser chamado de cidadão por uma lei que não conta os seus vizinhos.")
b("§ E a costura não pega. Fernando Sétimo volta ao trono, em mil oitocentos e catorze, e anula a constituição. Do outro lado do mar, as guerras de independência já corriam. Em mil oitocentos e vinte e quatro, em Ayacucho, cai o último grande exército espanhol da América do Sul.", card="1824")
b("Aqui está a terceira peça da resposta: toda vez que tentava costurar, a Espanha decidia antes quem contava. E quem não contava ia embora. O problema é que, dentro de casa, ainda havia dois botões soltos.")

# ───────────────────────── 9. O IMPOSTO QUE FICA EM BILBAO ─────────────────────────
cap("9. O imposto que fica em Bilbao")
b("§ Rio Ebro, mil oitocentos e quarenta. Entre Castela e Navarra, um fiscal ainda abre carroças e cobra. É a última alfândega da Espanha contra a própria Espanha.", card="1840")
b("Ela só cai em mil oitocentos e quarenta e um, depois de uma guerra civil em que muita gente de Navarra e do País Basco lutou por um pretendente que prometia os foros. Aí a alfândega vai para os Pireneus e para a costa.")
b("Mas o principal fica. Depois de outra guerra carlista, uma lei de mil oitocentos e setenta e seis acaba com as isenções bascas. Aí, dois anos depois, Madri faz um acordo: as províncias bascas recolhem os próprios impostos e repassam uma cota ao Estado.", card="1876")
b("Esse acordo existe até hoje. Se você mora em Bilbao, o seu imposto de renda não vai para Madri: vai para a sua província, que depois paga a cota. Navarra tem um igual.")
b("§ Então, em mil oitocentos e noventa e oito, a Espanha perde Cuba, Porto Rico e as Filipinas para os Estados Unidos. O que sobrava do mundo inteiro vai embora num ano.", card="1898")
b("O choque acelera o que já vinha: três anos antes, Sabino Arana tinha fundado um partido nacionalista basco, e na Catalunha o catalanismo vira força eleitoral. Se o império já não junta, por que continuar costurado? O problema agora era político, e ia dividir o país ao meio.")

# ───────────────────────── 10. UMA À FORÇA, UMA ASSINADA ─────────────────────────
cap("10. Uma à força, uma assinada")
b("§ Barcelona, catorze de abril de mil novecentos e trinta e um. Da sacada da prefeitura, Francesc Macià proclama a República Catalã. Ela dura três dias: depois de negociar com Madri, vira um governo autônomo, e o País Basco ganha o seu em plena guerra civil.", card="1931")
b("Mas a guerra termina em trinta e nove com Francisco Franco no poder, e a costura volta a ser à força: o lema é uma, grande e livre; os estatutos acabam, e as outras línguas saem da vida pública. São quase quarenta anos.", card="1939")
b("§ Então, quando Franco sai de cena, em setenta e cinco, a Espanha tenta outra coisa: uma costura assinada. A Constituição de setenta e oito fala, na mesma frase, da indissolúvel unidade da nação espanhola e da autonomia das nacionalidades e regiões.", card="1978")
b("Oitenta e sete por cento dos votantes disseram sim. E o título do rei, no artigo cinquenta e seis, fica no singular: rei da Espanha.")
b("Hoje são dezessete comunidades autônomas. Se você já viu bandeiras diferentes na mesma arquibancada na Espanha, viu essa história. E a costura segue sendo testada: em dois mil e dezessete, um referendo na Catalunha, suspenso pela Justiça, terminou com Madri assumindo o governo catalão por alguns meses. O problema mudou de forma, mas não de lugar.")

# ───────────────────────── FECHO ─────────────────────────
cap("Fecho")
b("§ [warm] Então, por que a Espanha juntou meio mundo antes de juntar a si mesma? Porque o mundo veio primeiro e pagou a conta: o rei não precisava costurar a casa. Quando faltou dinheiro, costurou à força, e cada ponto deixou alguém de fora.")
b("Começou com uma licença falsa e chegou a um papel votado por milhões: do rei das Espanhas ao rei da Espanha.")
b("Talvez a pergunta não seja por que ela rasga, mas por que nunca parou de negociar a costura. E você, o que acha? Conta nos comentários.")

FALA = [("Valladolid", "Valhadolíd"), ("Germana de Foix", "Germana de Fuá"), ("Recaredo", "Recarêdo"), ("Saragoça", "Saragóça"),
        ("Antonio Pérez", "Antônio Pérez"), ("Olivares", "Olivares"), ("Rossilhão", "Rossilhão"), ("Ayacucho", "Aiacútcho"),
        ("Bilbao", "Bilbáo"), ("Sabino Arana", "Sabíno Arâna"), ("Francesc Macià", "Francésc Maciá"), ("Bourbon", "Burbôn"),
        ("Habsburgo", "Rábsburgo"), ("al-Andalus", "al-Ândalus"), ("Flandres", "Flândres"), ("Ebro", "Ébro"), ("Cádis", "Cádis")]
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
