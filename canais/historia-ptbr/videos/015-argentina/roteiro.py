#!/usr/bin/env python3
"""Fonte única do 015-argentina (23/11/2026): roteiro (+ planos, quando o storyboard for escrito).
Gera SCRIPT.md e blocos.json; com o storyboard escrito (PENDENTE = False), também cenas.json, STORYBOARD.md e storyboard.json.
Uso: python3 roteiro.py   (rode na pasta do vídeo)

Vídeo da BÍBLIA DE ROTEIRO v2 (canais/historia-ptbr/biblia/roteiro.md; checklist em canais/historia-ptbr/tools/checklist_roteiro_v2.py).
ÂNGULO próprio (ANGULO.md): "os 13 zeros: a conta que ninguém quer pagar" — desde o porto colonial, a Argentina briga por quem paga
a conta do Estado (Buenos Aires × províncias pela alfândega; campo × cidade; governo × credores). O dinheiro do pampa (couro, charque,
trigo, carne, soja) está no meio de cada briga: quem fica com ele, manda. Quando ninguém aceita pagar, a conta vai para quem não pode
recusar: quem tem o peso no bolso. Cada zero cortado é o recibo de uma briga não resolvida.
EMBALAGEM.md aprovada no crivo r5 (3/3):
  A/T1 "A Argentina já foi RICA. Por que apagou 13 zeros da moeda?" + thumb rosto-emocao (rapaz de 1992 com o maço de 1969, "VALE NADA")
  B/T2 "Argentina: como a CARNE e o TRIGO decidiram quem manda" + thumb conflito-xvy (produtor do pampa × tangueiro, "QUEM PAGA?" + "1946")
  C/T3 "Por que a Argentina trocou de dinheiro 4 vezes em 22 anos?" + thumb numero-estatistica ("13 ZEROS", tesoura na cédula)
Hook: a gaveta do avô em 1/1/1992 — maço de 1969 com cinta de 1 milhão, dinheiro de uma tropa vendida no pampa (≤ 0:25)
  → frase-âncora "em vinte e dois anos… quatro vezes… treze zeros" (≤ 0:30) → "entre os mais ricos do mundo" (passagem)
  → PERGUNTA CENTRAL (≤ 0:50) → "essa é a história inteira" + "quem paga a conta… o couro, a carne, o trigo… quem fica com esse dinheiro, manda" (≤ 1:00).
Peças da resposta: 1 (cap. 4, 1890) quem manda e não quer cobrar de quem tem imprime ou pede emprestado; 2 (cap. 7, 1952) a conta muda de
  lado, mas não some; 3 (cap. 9, 1989) quando ninguém aceita pagar, a conta para no bolso de quem segura o dinheiro. Fecho responde e reenquadra.
"Guarde" único: o maço do avô → volta no cap. 8 (1970: vira dez mil; 1983: vira um peso), no cap. 9 (1992: o 13º zero) e no fecho.
As 4 trocas com motivo: 1970 e 1983 (cap. 8), 1985 e 1992 (cap. 9).
Neutralidade: Rosas, Roca, Perón, golpes, ditadura 1976–83 (com seriedade, números com a fonte), Malvinas, Menem, Kirchner/Cobos, Milei (1 frase).

Sintaxe dos planos (campo s), igual ao 016/017:
  "chave|prompt"            imagem nova (o id I### é dado na ordem de aparição)
  "chave"                   reuso; o enquadramento é escolhido sozinho
  "chave#enq"               reuso com enquadramento fixo
  qualquer um + "@@TEXTO"   rótulo na tela nesse plano (com moderação)
Bloco: b(texto, *planos, card="1992") · texto que começa com "§ " abre ideia nova · capítulo: cap("3. Título-frase")
Storyboard: escreva os planos em P[n] (n = número do bloco) acima de "# __PLANOS__" e ponha PENDENTE = False.
Voz: Fish drama-3, 1 chamada por bloco, tags de tom só onde a emoção muda. Gaps do build.py: 0,25/0,6/1,2 s (006–017).
Imagens: Codex (canal.yaml visual.gerador: codex; fallback gemini). Prompts só de conteúdo; o estilo vem do canal.yaml.
"""
import json, math, re
from pathlib import Path

WPS = 2.1            # palavras por segundo no drama-3 (006–017: ~128–131 ppm com pausas)
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
TITULO = "A história INTEIRA da Argentina"
PERGUNTA = "Como um país que já esteve entre os mais ricos do mundo precisou apagar treze zeros do próprio dinheiro?"
PROMESSA = ("Como a Argentina, que já esteve entre os países mais ricos do mundo, trocou de dinheiro 4 vezes em 22 anos e apagou 13 zeros "
            "da moeda: 200 anos de uma briga por quem paga a conta, com o dinheiro do pampa (couro, carne, trigo) no meio de cada briga "
            "(EMBALAGEM.md r5).")
TITULOS = ('T1 "A Argentina já foi RICA. Por que apagou 13 zeros da moeda?" / T2 "Argentina: como a CARNE e o TRIGO decidiram quem manda" / '
           'T3 "Por que a Argentina trocou de dinheiro 4 vezes em 22 anos?"')

B = []
def cap(titulo): B.append({"cap": titulo})
def b(t, *s, card=None):
    ideia = t.startswith("§")
    n = sum(1 for x in B if "t" in x) + 1
    if not s: s = tuple(P.get(n, ()))
    if not s and PENDENTE: s = (f"tmp{n:03d}|placeholder",)
    assert s, f"N{n:03d} sem planos"
    B.append({"t": t.lstrip("§ ").strip(), "s": list(s), "card": card, "ideia": ideia})

PENDENTE = True   # storyboard ainda não escrito (skill storyboard: preencher P e pôr False)
P = {}
# __PLANOS__


# ───────────────────────── HOOK (a gaveta do avô, 1/1/1992) ─────────────────────────
cap("Hook")
b("[curious] Buenos Aires, primeiro de janeiro de noventa e dois. Você abre a gaveta do avô: um maço de cédulas com cinta, um milhão de pesos.", card="1992")
b("É o preço de uma tropa vendida no pampa em sessenta e nove. Hoje, você junta um centavo com cem mil maços desses.")
b("Porque, em vinte e dois anos, a Argentina trocou de dinheiro quatro vezes e apagou treze zeros.")
b("[serious] Então fica a pergunta: como um país que já esteve entre os mais ricos do mundo precisou apagar treze zeros do próprio dinheiro?")
b("§ Essa é a história inteira da Argentina. A resposta mora numa briga de duzentos anos: quem paga a conta. E quem paga quase sempre foi o pampa: o couro, a carne, o trigo. Quem fica com esse dinheiro, manda.")
b("Guarde esse maço: ele volta. E tudo começa num porto que nem podia ser porto.")

# ───────────────────────── 1. O PORTO QUE NÃO PODIA SER PORTO ─────────────────────────
cap("1. O porto que não podia ser porto")
b("§ Rio da Prata, por volta de mil seiscentos e cinquenta. É noite, e um navio holandês ancora longe da margem. Botes vão e voltam: descem tecidos e ferro, sobem couro de boi e, escondida no meio, prata de Potosí.", card="c. 1650")
b("Tudo proibido. A lei manda a mercadoria pelo caminho oficial: Panamá, Lima e meses em lombo de mula. Imagine mandar uma carta de São Paulo para o Rio passando por Lisboa.")
b("Então Buenos Aires vive de contrabando. E o pampa ajuda: o gado dos primeiros espanhóis virou rebanhos soltos. Ninguém criava esses bois, caçava. Mas só o couro tinha preço.")
b("§ Em mil setecentos e setenta e seis, a Espanha desiste de brigar com o mapa: cria o vice-reino do Rio da Prata e abre o porto. Nasce a alfândega, a caixa registradora de Buenos Aires.", card="1776")
b("Repare: o couro de meio continente agora paga imposto numa porta só. Quem tem a chave tem o dinheiro. Então, em maio de mil oitocentos e dez, Buenos Aires se livra do vice-rei. E a pergunta vira outra: de quem é a chave?", card="1810")

# ───────────────────────── 2. A PRIMEIRA CONTA ─────────────────────────
cap("2. A primeira conta")
b("§ Londres, julho de mil oitocentos e vinte e quatro. O banco Baring lança os títulos do primeiro empréstimo de Buenos Aires: um milhão de libras, a seis por cento.", card="1824")
b("Era para um porto, povoados e água encanada. Só que, descontados juros adiantados e comissões, chegou pouco mais da metade. Tente pegar um empréstimo e receber metade na assinatura.")
b("§ E nem essa metade virou porto. No fim de vinte e cinco, começa a guerra com o Império do Brasil pela Banda Oriental, o atual Uruguai. Se você é brasileiro, a primeira conta da Argentina foi gasta numa guerra contra o seu país.", card="1825")
b("A esquadra brasileira bloqueia o Prata, e o couro para de sair. Sem couro, a alfândega seca. Então o governo faz o que ainda vai fazer muitas vezes: imprime papel que não se troca por metal.")
b("Em vinte e sete, Buenos Aires para de pagar os ingleses: primeiro calote. A conta fica com o credor de Londres e com quem tinha papel no bolso. Mas o interior pergunta: e a nossa parte da alfândega?", card="1827")

# ───────────────────────── 3. O DONO DA ALFÂNDEGA ─────────────────────────
cap("3. O dono da alfândega")
b("§ Um saladeiro no Prata, anos de mil oitocentos e vinte. Carne salgada secando ao sol: o charque. Boa parte embarca para Cuba e para o Brasil, para alimentar gente escravizada.")
b("Um dos sócios de saladeiro é Juan Manuel de Rosas, governador de Buenos Aires desde vinte e nove. Se você já comeu charque gaúcho, saiba: um concorrente dele mandou na Argentina por uns vinte anos.", card="1829")
b("Rosas governa com a alfândega na mão: cerca de oitenta por cento da receita da província. E não divide com ninguém. Quando França e Inglaterra bloqueiam o porto, ele paga imprimindo papel.")
b("§ Mas quem fica do lado de fora acaba arrombando. Em cinquenta e dois, o caudilho Urquiza derrota Rosas com ajuda do Brasil, de novo. Só que Buenos Aires não aceita dividir e passa quase dez anos à parte.", card="1852")
b("A briga só acaba em oitenta, com combates nas ruas e milhares de mortos: o governo nacional fica com a alfândega. E a campanha de Julio Roca contra os povos indígenas do sul entrega milhões de hectares a poucas famílias.", card="1880")
b("Agora o porto era do país, e o pampa tinha dono. O problema era quem ia pagar a festa que vinha.")

# ───────────────────────── 4. CADA BANCO COM SUA IMPRESSORA ─────────────────────────
cap("4. Cada banco com sua impressora")
b("§ Londres, quinze de novembro de mil oitocentos e noventa. No Banco da Inglaterra, banqueiros da City assinam uma garantia de dezessete milhões de libras. Tudo para salvar o Baring, aquele de vinte e quatro.", card="1890")
b("O banco tinha se enchido de títulos argentinos. Só que ninguém mais comprava. O último encalhado era de água e esgoto para Buenos Aires. A água encanada de vinte e quatro: se você está contando, sessenta e seis anos de espera.")
b("§ Como se chega ali? Em oitenta e sete, uma lei deixa os bancos das províncias emitirem dinheiro. Imagine cada estado do Brasil com a sua impressora de reais.", card="1887")
b("Então as províncias tomam ouro emprestado em Londres, imprimem papel e emprestam para quem compra terra no pampa. A terra sobe, o papel se multiplica, e o ouro some. Em noventa, vem a Revolução do Parque, e o presidente renuncia.")
b("Lembra da nossa pergunta? Aqui está a primeira peça da resposta: quando quem manda não quer cobrar de quem tem, imprime ou pede emprestado. E a conta chega depois, com juros. Então, como amarrar a mão de quem imprime?")

# ───────────────────────── 5. A ALGEMA DE OURO ─────────────────────────
cap("5. A algema de ouro")
b("§ Buenos Aires, outubro de mil oitocentos e noventa e nove. Uma lei cria a Caixa de Conversão: o peso de papel fica preso ao ouro, e só se imprime papel novo quando entra ouro novo.", card="1899")
b("É uma algema na impressora. E funciona, porque o ouro está entrando: carne e trigo para a Europa. Se você fosse dono de terra no pampa, esses eram os seus anos: a Argentina fica entre os países mais ricos do mundo.")
b("§ Mas de quem é esse dinheiro? Junho de mil novecentos e doze, Alcorta, em Santa Fé. Mais de dois mil colonos lotam um salão: quase todos imigrantes italianos e espanhóis, quase nenhum dono da terra que planta.", card="1912")
b("O aluguel da terra come a colheita. Então eles decidem não plantar até o aluguel baixar: é o Grito de Alcorta. Imagine plantar o trigo que alimenta a Europa e não conseguir pagar o aluguel do chão.")
b("Só que a algema de ouro só segura quando o ouro chega. A Caixa fecha na guerra de catorze e, de novo, em vinte e nove. E, em setembro de trinta, os militares derrubam um presidente eleito. Quem ia comprar a carne agora?", card="1930")

# ───────────────────────── 6. A CARNE COM LETRA MIÚDA ─────────────────────────
cap("6. A carne com letra miúda")
b("§ Londres, primeiro de maio de mil novecentos e trinta e três. O vice-presidente Julio Roca, filho do general de oitenta, fecha um acordo com o ministro inglês Walter Runciman: a Inglaterra continua comprando carne argentina.", card="1933")
b("Mas com cota. E repare na letra miúda: no máximo quinze por cento dessa carne passa por frigoríficos argentinos. O resto fica com os estrangeiros. A Roca é atribuída a frase: a Argentina seria parte integrante do Império Britânico.")
b("§ Só que, aqui dentro, quem perde é o criador que vende o boi barato ao frigorífico. Em trinta e cinco, o senador Lisandro de la Torre denuncia o negócio. No último dia do debate, um policial atira contra ele e mata o colega que o protegia, Enzo Bordabehere.", card="1935")
b("Pense nisso: a briga pela carne chegou a tiros dentro do Congresso.")
b("Na Segunda Guerra, a Inglaterra segue comprando, mas paga em libras presas em Londres: a carne vai, e o dinheiro fica lá. Em quarenta e três, outro golpe. E dele sai um coronel com outra resposta para a pergunta de sempre: quem fica com o dinheiro do pampa?")

# ───────────────────────── 7. O CAMPO PAGA A CIDADE ─────────────────────────
cap("7. O campo paga a cidade")
b("§ Pergamino, no pampa, fim de mil novecentos e quarenta e seis. Imagine que você plantou trigo. Na estação, só existe um comprador: o IAPI, o instituto criado em maio pelo governo de Juan Perón.", card="1946")
b("O preço é o que o instituto marca, e é baixo. No porto, o mesmo trigo segue para uma Europa com fome, por muito mais. Você nunca vê essa diferença. Quem vê é o governo.")
b("Do outro lado da conta, nas fábricas de Buenos Aires, o operário ganha aumento, décimo terceiro e férias pagas. Quem paga? O campo. E Perón nacionaliza o Banco Central: agora quem manda também decide quanto dinheiro existe.")
b("§ Só que o campo não é bobo: com preço baixo, planta menos. Aí vêm as secas, e o trigo some. Em fevereiro de cinquenta e dois, o governo anuncia no rádio um plano de emergência: carne e farinha branca para fora, e pão escuro na cidade.", card="1952")
b("E aqui está a segunda peça da resposta: a conta muda de lado, mas não some. Em cinquenta e cinco, os militares derrubam Perón. E começa um pêndulo: cada governo empurra a conta para quem não está no poder.")

# ───────────────────────── 8. O PÊNDULO ─────────────────────────
cap("8. O pêndulo")
b("§ Buenos Aires, primeiro de janeiro de mil novecentos e setenta. Chega o peso lei, com dois zeros a menos. Lembra do maço do avô? Nesse dia, o milhão vira dez mil.", card="1970")
b("O motivo: quinze anos de pêndulo e de inflação encheram as cédulas de zeros. Repare: nenhum zero cai por capricho. Cada corte chega depois de anos imprimindo para tapar o buraco do governo.")
b("§ Em junho de setenta e cinco, a briga explode. Um pacote do ministro Celestino Rodrigo dobra o dólar e quase triplica a gasolina. Os sindicatos param o país, e o plano cai: é o rodrigazo.", card="1975")
b("[serious] Em março de setenta e seis, os militares tomam o poder outra vez. A ditadura faz desaparecer milhares de pessoas: cerca de trinta mil, segundo organismos de direitos humanos; quase nove mil casos registrados pela comissão oficial de oitenta e quatro.", card="1976")
b("§ E a dívida externa salta de uns oito para uns quarenta e cinco bilhões de dólares. Em oitenta e dois, ano da derrota nas Malvinas, o Banco Central passa a bancar boa parte da dívida das empresas. Se você nunca pegou um dólar emprestado, parabéns: passou a dever mesmo assim.", card="1982")
b("Então a inflação passa de cem por cento, e em junho de oitenta e três a segunda troca corta mais quatro zeros: o peso argentino. O milhão do avô vira um peso. Só que o dinheiro novo nasce com a pergunta velha: quem paga?", card="1983")

# ───────────────────────── 9. O DÉCIMO TERCEIRO ZERO ─────────────────────────
cap("9. O décimo terceiro zero")
b("§ Noite de catorze de junho de oitenta e cinco. Raúl Alfonsín, eleito na volta da democracia, assina o Plano Austral: preços e salários congelados de um dia para o outro. É a terceira troca: o austral, três zeros a menos e a promessa de não imprimir para pagar o governo.", card="1985")
b("Funciona por um tempo. Mas ninguém aceita a conta: o campo reclama do câmbio, os sindicatos fazem greve atrás de greve. Então a impressora volta.")
b("§ Em julho de oitenta e nove, os preços sobem quase duzentos por cento num mês. Pelos números do INDEC, se você gastava cem no mercado no começo do mês, no fim precisava de quase trezentos. Alfonsín entrega o governo cinco meses antes do prazo.", card="1989")
b("Lembra da nossa pergunta? Aqui entra a terceira peça: quando ninguém aceita pagar, a conta para no bolso de quem segura o dinheiro. Então o governo de Carlos Menem amarra o peso ao dólar por lei: um peso, um dólar.")
b("E, no primeiro de janeiro de noventa e dois, a quarta troca corta os últimos quatro zeros: nasce o peso conversível. Repare na gaveta do começo: o milhão do avô agora vale um décimo de milionésimo de peso. Treze zeros em vinte e dois anos.", card="1992")
b("Só que, para cada peso, precisava existir um dólar. E, quando os dólares não chegam, a Argentina pega emprestado. O problema é que empréstimo vence.")

# ───────────────────────── 10. O PORTO DE HOJE ─────────────────────────
cap("10. O porto de hoje")
b("§ La Plata, agosto de dois mil e um. Um funcionário da província recebe parte do salário num papel colorido: o patacão, um bônus da província. Não é peso, mas a padaria aceita.", card="2001")
b("Logo há mais de uma dúzia de quase-moedas, perto de metade do dinheiro em papel do país. Se você já pagou o almoço com vale, entende: é a conta voltando para o bolso, em outra cor.")
b("§ Em dezembro, o país suspende a dívida e tem cinco presidentes em onze dias. Aí vem a pesificação: o depósito em dólar vira um peso e quarenta por dólar, e o dólar de verdade passa de três. A diferença fica, de novo, com quem segurava o dinheiro.")
b("Então o governo volta ao porto e recria o imposto sobre a exportação de grãos, as retenções. A soja do pampa vira o caixa do Estado, como você viu o couro fazer na velha alfândega.", card="2002")
b("§ Senado, madrugada de dezessete de julho de dois mil e oito. Depois de meses de estradas bloqueadas pelo campo contra retenções maiores, a votação empata: trinta e seis a trinta e seis. Desempata o vice-presidente Julio Cobos, do próprio governo. E ele diz: meu voto não é positivo.", card="2008")
b("O aumento cai: o campo, mais uma vez, decidiu quem manda. Em dois mil e vinte e seis, com Javier Milei, a inflação caiu para perto de dois por cento ao mês. Só que a pergunta continua na mesa: quem paga o ajuste?", card="2026")

# ───────────────────────── FECHO ─────────────────────────
cap("Fecho")
b("§ [warm] Então, como um país que já esteve entre os mais ricos do mundo apagou treze zeros? Porque, por duzentos anos, a Argentina brigou por quem paga a conta: o porto contra as províncias, o campo contra a cidade, o governo contra os credores.")
b("E, quando ninguém aceita pagar, a conta vai para quem não pode recusar: quem tem o peso no bolso. Como o avô da gaveta.")
b("Talvez a pergunta nunca tenha sido quanto vale o peso, e sim quem fica segurando ele. E você, o que acha? Conta nos comentários.")

# Grafias de voz (texto → Fish); a tela/legenda usa a grafia correta. Conferir no Whisper (voz.md).
FALA = [("Juan Manuel de Rosas", "Ruan Manuel de Rôssas"), ("Rosas", "Rôssas"), ("Potosí", "Potossí"), ("Baring", "Bêring"),
        ("Justo José de Urquiza", "Rústo Rossé de Urkíssa"), ("Entre Ríos", "Êntre Ríos"), ("Caseros", "Casêros"),
        ("Julio Roca", "Rúlio Rôca"), ("Roca", "Rôca"), ("Juárez Celman", "Ruárez Célman"), ("Alcorta", "Alcórta"),
        ("Walter Runciman", "Uólter Rânsiman"), ("Lisandro de la Torre", "Lissândro de la Tôrre"), ("Enzo Bordabehere", "Ênzo Bordabeêre"),
        ("Otto Niemeyer", "Óto Nímaier"), ("Pergamino", "Pergamíno"), ("IAPI", "iápi"), ("Juan Perón", "Ruan Perón"),
        ("Avellaneda", "Avechanêda"), ("Celestino Rodrigo", "Celestíno Rodrígo"), ("rodrigazo", "rodrigásso"),
        ("Carlos Menem", "Cárlos Mênem"), ("Julio Cobos", "Rúlio Côbos"), ("Javier Milei", "Raviér Miléi"),
        ("saladeiro", "saladêiro")]

def fala(t):
    for a, z in FALA: t = re.sub(r"(?<![\wÀ-ú])" + re.escape(a) + r"(?![\wÀ-ú])", z, t)
    return t

IDEIA = set()
THUMB = None   # thumbs nascem dos 3 conceitos aprovados no crivo (EMBALAGEM.md r5): arte na etapa 2 (skill thumbnail)

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
    if not PENDENTE:   # sem storyboard, não grava cenas/planos de placeholder
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
    if not PENDENTE: (out / "STORYBOARD.md").write_text("\n".join(linhas) + "\n")
    if PENDENTE:   # só o roteiro: as estatísticas de planos não valem
        stats = {k: stats[k] for k in ("palavras", "duracao_s", "capitulos")} | {"storyboard": "pendente"}
    print(json.dumps(stats, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
