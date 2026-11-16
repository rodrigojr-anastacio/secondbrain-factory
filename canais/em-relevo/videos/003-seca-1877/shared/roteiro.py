# Roteiro do longo 03 (Em Relevo, A Grande Seca de 1877). Fonte única do texto -> shared/blocos.json.
# Base: pauta 13/11 (pesquisa/pauta-2026-11-15/RELATORIO.md §3) + pesquisa/FATOS.md, DADOS.md e CHECAGEM.md (13/11/2026).
# Mesmo formato do longo-02: id, cap (aba), marcha (1 = hook mais rápido), fala (limpa), fala_tts (tags v3, números por extenso),
# tela (algarismos; "|" separa os cartões da legenda). "fonte" = item da CHECAGEM que sustenta o bloco.
import json, re
from pathlib import Path

B = []
TAG = re.compile(r"\[[a-z ]+\]\s*")
def b(cap, fala, tela, fonte=""):
    fala = fala.strip()
    B.append({"id": f"b{len(B)+1:02d}", "cap": cap, "marcha": 1 if len(B) < 7 else 2, "fala": TAG.sub("", fala), "fala_tts": fala,
              "tela": tela.strip(), "fonte": fonte})

C1 = "PERGUNTA 1/4 · O QUE ACONTECEU"
C2 = "PERGUNTA 2/4 · POR QUE NÃO CHOVEU"
C3 = "PERGUNTA 3/4 · O QUE MUDOU NO MAPA"
C4 = "PERGUNTA 4/4 · E EM 2026?"

# ---------------- HOOK ----------------
b("FORTALEZA · 1878",
  "[serious] Fortaleza, mil oitocentos e setenta e oito.\nUma cidade de uns vinte e cinco mil habitantes.\nEm poucos meses, chegam mais de cem mil pessoas.\nA pé. Vindas do sertão.",
  "Fortaleza, 1878. | Uma cidade de uns 25 mil habitantes. | Em poucos meses, chegam mais de 100 mil pessoas. | A pé. Vindas do sertão.",
  "C3")
b("FORTALEZA · 1878",
  "[serious] No fim daquele ano, segundo o farmacêutico Rodolpho Theophilo, que viveu tudo aquilo, a cidade tinha cento e sessenta mil pessoas.\nMais de seis vezes o tamanho de antes.",
  "No fim daquele ano, segundo o farmacêutico Rodolpho Theophilo, | que viveu tudo aquilo, | a cidade tinha 160 mil pessoas. | Mais de 6 vezes o tamanho de antes.",
  "C3")
b("FORTALEZA · 1878",
  "[serious] E num único dia, dez de dezembro, a varíola matou mil e quatro pessoas.",
  "E num único dia, 10 de dezembro, | a varíola matou 1.004 pessoas.",
  "C4")
b("A PERGUNTA",
  "Essa é a Grande Seca de mil oitocentos e setenta e sete.\nAs estimativas chegam a quinhentos mil mortos.\nPelas contas mais altas, cinco por cento de toda a população do Império.\nProporcionalmente, a maior catástrofe da história do Brasil.",
  "Essa é a Grande Seca de 1877. | As estimativas chegam a 500 mil mortos. | Pelas contas mais altas, 5% de toda a população do Império. | Proporcionalmente, a maior catástrofe da história do Brasil.",
  "C2 (Agência Senado)")
b("A PERGUNTA",
  "[curious] Mesmo assim, quase ninguém fala dela.\n[intrigued] E agora, com o El Niño de dois mil e vinte e seis, uma pergunta voltou: aquilo pode se repetir?",
  "Mesmo assim, quase ninguém fala dela. | E agora, com o El Niño de 2026, uma pergunta voltou: | aquilo pode se repetir?",
  "C11")
b("A PERGUNTA",
  "[serious] Isso nos leva às seguintes perguntas.\n[curious] O que aconteceu, afinal?\n[curious] Por que não choveu?\n[curious] O que essa seca mudou no mapa do Brasil?\n[intrigued] E ela pode se repetir em dois mil e vinte e seis?",
  "Isso nos leva às seguintes perguntas. | O que aconteceu, afinal? | Por que não choveu? | O que essa seca mudou no mapa do Brasil? | E ela pode se repetir em 2026?")
b("A PERGUNTA",
  "[serious] Mas antes, é preciso entender uma coisa.\nNo sertão do Ceará, quase toda a chuva do ano cai em poucos meses, de fevereiro a maio.\nO sertanejo chama essa época de inverno.\nSe esses meses falham, o ano inteiro falha.",
  "Mas antes, é preciso entender uma coisa. | No sertão do Ceará, quase toda a chuva do ano cai em poucos meses, | de fevereiro a maio. | O sertanejo chama essa época de inverno. | Se esses meses falham, o ano inteiro falha.",
  "C8b")

# ---------------- 1. O QUE ACONTECEU ----------------
b(C1,
  "Março de mil oitocentos e setenta e sete.\nNo sertão, a tradição diz que, se chover até o dia de São José, dezenove de março, o inverno vai ser bom.\nNaquele ano, a chuva não veio.",
  "Março de 1877. | No sertão, a tradição diz que, se chover até o dia de São José, | 19 de março, o inverno vai ser bom. | Naquele ano, a chuva não veio.",
  "C1")
b(C1,
  "Fortaleza tem uma das séries de chuva mais longas do Brasil, medida desde mil oitocentos e quarenta e nove.\nNa média, chove mais de mil e quatrocentos milímetros por ano.\nEm mil oitocentos e setenta e sete, choveram quatrocentos e sessenta e oito.\nUm terço do normal.\nO ano mais seco de todo o registro.\n[serious] E mil oitocentos e setenta e oito foi o segundo.",
  "Fortaleza tem uma das séries de chuva mais longas do Brasil, | medida desde 1849. | Na média, chove mais de 1.400 milímetros por ano. | Em 1877, choveram 468. | Um terço do normal. | O ano mais seco de todo o registro. | E 1878 foi o segundo.",
  "C8")
b(C1,
  "E isso é no litoral. No sertão, onde já chove bem menos, o pasto secou, o gado morreu e as roças de milho, feijão e mandioca não vingaram.",
  "E isso é no litoral. | No sertão, onde já chove bem menos, o pasto secou, | o gado morreu | e as roças de milho, feijão e mandioca não vingaram.",
  "C1")
b(C1,
  "Em mil oitocentos e setenta e dois, o Ceará tinha pouco mais de setecentas mil pessoas.\nE uma multidão fez a mesma coisa: pegou o que tinha e andou.\nPara o litoral, onde havia porto, comida chegando de navio e o governo.",
  "Em 1872, o Ceará tinha pouco mais de 700 mil pessoas. | E uma multidão fez a mesma coisa: | pegou o que tinha e andou. | Para o litoral, onde havia porto, comida chegando de navio e o governo.",
  "C2b")
b(C1,
  "No mapa, é como se o sertão inteiro escorresse para a costa.\nEssas pessoas ficaram conhecidas por um nome: retirantes.",
  "No mapa, é como se o sertão inteiro escorresse para a costa. | Essas pessoas ficaram conhecidas por um nome: | retirantes.")
b(C1,
  "Fortaleza não estava preparada.\nO governo montou abarracamentos, campos de barracas nos arredores da cidade.\nEm agosto de mil oitocentos e setenta e oito, eram quase cento e catorze mil pessoas abarracadas.",
  "Fortaleza não estava preparada. | O governo montou abarracamentos, | campos de barracas nos arredores da cidade. | Em agosto de 1878, | eram quase 114 mil pessoas abarracadas.",
  "C3b")
b(C1,
  "A comida vinha por mar, mas não dava.\nE o que chegava nem sempre servia: houve denúncias de carne estragada e de farinha misturada com cal.",
  "A comida vinha por mar, mas não dava. | E o que chegava nem sempre servia: | houve denúncias de carne estragada | e de farinha misturada com cal.",
  "C5")
b(C1,
  "[serious] E aí veio a varíola.\nEm gente fraca de fome, amontoada em barracas, o vírus se espalhou depressa.\nEm novembro de mil oitocentos e setenta e oito, quase dez mil mortes em Fortaleza.\nEm dezembro, mais de quinze mil, quase todas de varíola.",
  "E aí veio a varíola. | Em gente fraca de fome, amontoada em barracas, | o vírus se espalhou depressa. | Em novembro de 1878, quase 10 mil mortes em Fortaleza. | Em dezembro, mais de 15 mil, quase todas de varíola.",
  "C4b")
b(C1,
  "[serious] No dia dez de dezembro, foram mil e quatro mortos.\nOs coveiros não deram conta, e mais de duzentos corpos ficaram para o dia seguinte.\nFortaleza chama essa data, até hoje, de o Dia dos Mil Mortos.",
  "No dia 10 de dezembro, foram 1.004 mortos. | Os coveiros não deram conta, | e mais de 200 corpos ficaram para o dia seguinte. | Fortaleza chama essa data, até hoje, | de o Dia dos Mil Mortos.",
  "C4")
b(C1,
  "Quantas pessoas a seca matou, no total?\nNinguém contou direito.\nAs estimativas vão de cento e cinquenta mil a quinhentos mil, no Ceará e nas províncias vizinhas.\nE a chuva só voltou de verdade em mil oitocentos e oitenta.",
  "Quantas pessoas a seca matou, no total? | Ninguém contou direito. | As estimativas vão de 150 mil a 500 mil, | no Ceará e nas províncias vizinhas. | E a chuva só voltou de verdade em 1880.",
  "C2, C1")
b(C1,
  "No Rio de Janeiro, a capital do Império, a seca era notícia distante.\nAté que, em mil oitocentos e setenta e oito, um jornal ilustrado da corte, O Besouro, publicou fotografias de retirantes feitas em Fortaleza.\nPara os historiadores, é possivelmente a primeira experiência de fotojornalismo do Brasil.",
  "No Rio de Janeiro, a capital do Império, a seca era notícia distante. | Até que, em 1878, um jornal ilustrado da corte, O Besouro, | publicou fotografias de retirantes feitas em Fortaleza. | Para os historiadores, é possivelmente | a primeira experiência de fotojornalismo do Brasil.",
  "C9")

# ---------------- 2. POR QUE NÃO CHOVEU ----------------
b(C2,
  "[curious] Agora, por que não choveu?\nA resposta não está no Ceará.\nEstá do outro lado do planeta.",
  "Agora, por que não choveu? | A resposta não está no Ceará. | Está do outro lado do planeta.")
b(C2,
  "Entre mil oitocentos e setenta e sete e setenta e oito, o Pacífico tropical esquentou como poucas vezes na história.\nFoi um El Niño.\nE, pelas reconstruções da temperatura do mar, um dos mais fortes já registrados.\nNo mesmo nível dos de oitenta e dois, noventa e sete e dois mil e quinze.",
  "Entre 1877 e 78, o Pacífico tropical esquentou | como poucas vezes na história. | Foi um El Niño. | E, pelas reconstruções da temperatura do mar, | um dos mais fortes já registrados. | No mesmo nível dos de 82, 97 e 2015.",
  "C7, D2")
b(C2,
  "No nosso vídeo sobre o El Niño, a gente mostrou como isso funciona.\nQuando o Pacífico esquenta, o ar sobe lá, em cima da água quente.\nE desce em outros lugares.\nUm deles é o norte do Nordeste.\nE ar que desce não forma nuvem.",
  "No nosso vídeo sobre o El Niño, a gente mostrou como isso funciona. | Quando o Pacífico esquenta, o ar sobe lá, em cima da água quente. | E desce em outros lugares. | Um deles é o norte do Nordeste. | E ar que desce não forma nuvem.",
  "longo-02 b24")
b(C2,
  "Mas, no Ceará, o Atlântico também manda.\nA chuva de fevereiro a maio vem de uma faixa de nuvens que acompanha a linha do equador.\nQuando o Atlântico Norte fica mais quente que o do Sul, essa faixa sobe, e não chega até o Ceará.\n[serious] E, em mil oitocentos e setenta e oito, o Atlântico Norte esteve quente como nunca no registro.",
  "Mas, no Ceará, o Atlântico também manda. | A chuva de fevereiro a maio vem de uma faixa de nuvens | que acompanha a linha do equador. | Quando o Atlântico Norte fica mais quente que o do Sul, | essa faixa sobe, e não chega até o Ceará. | E, em 1878, o Atlântico Norte esteve quente como nunca no registro.",
  "C7, C8b")
b(C2,
  "E o Brasil não estava sozinho.\nO mesmo clima secou a Índia e o norte da China.\nNa Índia, de cinco milhões e meio a quase dez milhões de mortos.\nNa China, de nove a treze milhões.",
  "E o Brasil não estava sozinho. | O mesmo clima secou a Índia e o norte da China. | Na Índia, de 5,5 milhões a quase 10 milhões de mortos. | Na China, de 9 a 13 milhões.",
  "C7b, C7c")
b(C2,
  "Um estudo de dois mil e dezoito ligou essas fomes ao mesmo El Niño, junto com o oceano Índico e o Atlântico.\nE as estimativas de mortos, no mundo, passam de cinquenta milhões.",
  "Um estudo de 2018 ligou essas fomes ao mesmo El Niño, | junto com o oceano Índico e o Atlântico. | E as estimativas de mortos, no mundo, | passam de 50 milhões.",
  "C7")
b(C2,
  "[serious] Mas o clima explica a falta de chuva.\nNão explica, sozinho, tantas mortes.\nNo Ceará de mil oitocentos e setenta e sete, não havia nenhum grande açude, e nenhuma ferrovia chegava ao sertão.\nO socorro chegava de navio, e daí para dentro era a pé ou no lombo de animal.",
  "Mas o clima explica a falta de chuva. | Não explica, sozinho, tantas mortes. | No Ceará de 1877, não havia nenhum grande açude, | e nenhuma ferrovia chegava ao sertão. | O socorro chegava de navio, | e daí para dentro era a pé ou no lombo de animal.",
  "C5c, C5d, D5")
b(C2,
  "No governo, a resposta foi lenta.\nO chefe do governo, o senador Sinimbu, chegou a dizer: a solução depende da Divina Providência, e não de nós.\nE, no Senado, um pedido de investigação sobre o dinheiro do socorro não foi aprovado.",
  "No governo, a resposta foi lenta. | O chefe do governo, o senador Sinimbu, chegou a dizer: | a solução depende da Divina Providência, e não de nós. | E, no Senado, um pedido de investigação | sobre o dinheiro do socorro não foi aprovado.",
  "C5")

# ---------------- 3. O QUE MUDOU NO MAPA ----------------
b(C3,
  "[curious] Então, o que essa seca mudou no mapa do Brasil?\nMais do que parece.",
  "Então, o que essa seca mudou no mapa do Brasil? | Mais do que parece.")
b(C3,
  "Primeiro, os trilhos.\nEm mil oitocentos e setenta e oito, o governo assumiu a Estrada de Ferro de Baturité e pôs os retirantes para trabalhar nela, como obra de socorro.\nOs trilhos chegaram a Baturité em mil oitocentos e oitenta e dois.\nE a Quixadá, no coração do sertão, em mil oitocentos e noventa e um.",
  "Primeiro, os trilhos. | Em 1878, o governo assumiu a Estrada de Ferro de Baturité | e pôs os retirantes para trabalhar nela, como obra de socorro. | Os trilhos chegaram a Baturité em 1882. | E a Quixadá, no coração do sertão, em 1891.",
  "C5c, D5")
b(C3,
  "No norte da província, a mesma coisa.\nA ferrovia que saía do porto de Camocim chegou a Sobral no último dia de mil oitocentos e oitenta e dois.",
  "No norte da província, a mesma coisa. | A ferrovia que saía do porto de Camocim | chegou a Sobral no último dia de 1882.",
  "D5")
b(C3,
  "Depois, a água.\nA seca convenceu o governo a represar o sertão.\nEm Quixadá, começou em mil oitocentos e oitenta e quatro a obra do Açude do Cedro, ao pé de uma pedra famosa, a Galinha Choca.\nFoi o primeiro grande açude público do país.\nLevou vinte e dois anos e só ficou pronto em mil novecentos e seis, já na República.",
  "Depois, a água. | A seca convenceu o governo a represar o sertão. | Em Quixadá, começou em 1884 a obra do Açude do Cedro, | ao pé de uma pedra famosa, a Galinha Choca. | Foi o primeiro grande açude público do país. | Levou 22 anos e só ficou pronto em 1906, já na República.",
  "C5d")
b(C3,
  "[curious] E aqui entra uma lenda.\nDiz a tradição que Dom Pedro Segundo prometeu vender até a última joia da Coroa para que nenhum cearense morresse de fome.\nNão há documento que prove essa frase.\nE as joias não foram vendidas.",
  "E aqui entra uma lenda. | Diz a tradição que Dom Pedro II prometeu vender até a última joia da Coroa | para que nenhum cearense morresse de fome. | Não há documento que prove essa frase. | E as joias não foram vendidas.",
  "C5b")
b(C3,
  "Mas a mudança maior foi de gente.\nCom passagem paga pelo governo, milhares de cearenses embarcaram para a Amazônia, onde a borracha começava a valer muito dinheiro.\nSó para o Amazonas, foram quase cinco mil em pouco mais de um ano.",
  "Mas a mudança maior foi de gente. | Com passagem paga pelo governo, milhares de cearenses embarcaram para a Amazônia, | onde a borracha começava a valer muito dinheiro. | Só para o Amazonas, foram quase 5 mil em pouco mais de um ano.",
  "C5, C6")
b(C3,
  "Foi o começo de uma onda que não parou mais.\nNas décadas seguintes, seringueiros nordestinos subiram os rios até um território que era da Bolívia: o Acre.\nE, em mil novecentos e três, depois de uma revolta desses seringueiros, o Brasil ficou com o Acre, pelo Tratado de Petrópolis.",
  "Foi o começo de uma onda que não parou mais. | Nas décadas seguintes, seringueiros nordestinos subiram os rios | até um território que era da Bolívia: o Acre. | E, em 1903, depois de uma revolta desses seringueiros, | o Brasil ficou com o Acre, pelo Tratado de Petrópolis.",
  "C6b, C6c")
b(C3,
  "Ou seja, a seca de mil oitocentos e setenta e sete ajudou a desenhar a fronteira oeste do Brasil.\nNão sozinha.\nMas os historiadores apontam essa seca como o começo desse caminho.",
  "Ou seja, a seca de 1877 ajudou a desenhar a fronteira oeste do Brasil. | Não sozinha. | Mas os historiadores apontam essa seca como o começo desse caminho.",
  "C6b")
b(C3,
  "[serious] E tem uma coisa que demorou muito a mudar.\nNas secas de mil novecentos e quinze e de mil novecentos e trinta e dois, o governo do Ceará cercou retirantes em campos, para que não chegassem a Fortaleza.\nO povo chamava de currais do governo.\nEm trinta e dois, foram sete campos, com mais de setenta mil pessoas.",
  "E tem uma coisa que demorou muito a mudar. | Nas secas de 1915 e de 1932, o governo do Ceará cercou retirantes em campos, | para que não chegassem a Fortaleza. | O povo chamava de currais do governo. | Em 32, foram 7 campos, com mais de 70 mil pessoas.",
  "C10, C10b")
b(C3,
  "Só em mil novecentos e nove o país criou um órgão permanente contra as secas.\nA inspetoria que, mais tarde, virou o Dnócs.",
  "Só em 1909 o país criou um órgão permanente contra as secas. | A inspetoria que, mais tarde, virou o DNOCS.",
  "C10c")
b(C3,
  "[curious] E por que quase ninguém fala da seca de mil oitocentos e setenta e sete?\nParte da resposta está aqui.\nOs mortos eram pobres, do sertão, longe da capital.\nNinguém contou os corpos direito.\nA investigação foi barrada.\nE as secas seguintes repetiram a história, até o país se acostumar com ela.",
  "E por que quase ninguém fala da seca de 1877? | Parte da resposta está aqui. | Os mortos eram pobres, do sertão, longe da capital. | Ninguém contou os corpos direito. | A investigação foi barrada. | E as secas seguintes repetiram a história, | até o país se acostumar com ela.",
  "C2, C5")

# ---------------- 4. E EM 2026? ----------------
b(C4,
  "[curious] E a última pergunta.\nCom o El Niño de dois mil e vinte e seis, aquilo pode se repetir?",
  "E a última pergunta. | Com o El Niño de 2026, aquilo pode se repetir?")
b(C4,
  "O El Niño deste ano já é muito forte.\nPela mesma reconstrução da temperatura do mar, ele já está no nível do de mil oitocentos e setenta e sete, ou acima.\nE a previsão oficial para novembro, dezembro e janeiro é de chuva abaixo da média em áreas do Nordeste, principalmente no norte da região.",
  "O El Niño deste ano já é muito forte. | Pela mesma reconstrução da temperatura do mar, | ele já está no nível do de 1877, ou acima. | E a previsão oficial para novembro, dezembro e janeiro | é de chuva abaixo da média em áreas do Nordeste, | principalmente no norte da região.",
  "C11, D2")
b(C4,
  "Mas, para o sertão do Ceará, o que decide é o inverno de fevereiro a maio de dois mil e vinte e sete.\nE aí o Atlântico também pesa.\nA Funceme, o órgão de meteorologia do Ceará, diz que ainda é cedo para prever.",
  "Mas, para o sertão do Ceará, o que decide | é o inverno de fevereiro a maio de 2027. | E aí o Atlântico também pesa. | A Funceme, o órgão de meteorologia do Ceará, | diz que ainda é cedo para prever.",
  "C11, D7")
b(C4,
  "E o Nordeste já está seco agora.\nEm setembro, segundo o Monitor de Secas, havia seca em noventa e seis por cento do território da região.",
  "E o Nordeste já está seco agora. | Em setembro, segundo o Monitor de Secas, | havia seca em 96% do território da região.",
  "D7")
b(C4,
  "Então, pode faltar chuva de novo?\nPode.\nMas o sertão de dois mil e vinte e seis não é o de mil oitocentos e setenta e sete.\nHoje há mais de um milhão e duzentas mil cisternas guardando a água da chuva ao lado das casas.\nAçudes como o Castanhão.\nE a água do rio São Francisco chegando ao Ceará pela transposição, desde dois mil e vinte.",
  "Então, pode faltar chuva de novo? | Pode. | Mas o sertão de 2026 não é o de 1877. | Hoje há mais de 1,2 milhão de cisternas | guardando a água da chuva ao lado das casas. | Açudes como o Castanhão. | E a água do rio São Francisco chegando ao Ceará | pela transposição, desde 2020.",
  "C11b, C11c")
b(C4,
  "E, principalmente, a seca deixou de matar de fome em massa.\nDe dois mil e doze a dois mil e dezessete, o semiárido viveu uma das piores secas em décadas.\nCentenas de cidades em emergência, carro-pipa, perda de safra e de gado.\nMas sem as mortes em massa de mil oitocentos e setenta e sete.",
  "E, principalmente, a seca deixou de matar de fome em massa. | De 2012 a 2017, o semiárido viveu uma das piores secas em décadas. | Centenas de cidades em emergência, carro-pipa, | perda de safra e de gado. | Mas sem as mortes em massa de 1877.",
  "C11")
b(C4,
  "O risco de hoje é outro.\nÁgua racionada, colheita perdida, gado vendido às pressas e calor.\nE ele pesa mais para quem vive longe da rede de água.",
  "O risco de hoje é outro. | Água racionada, colheita perdida, | gado vendido às pressas e calor. | E ele pesa mais para quem vive longe da rede de água.",
  "Hipótese de fecho (sem número)")

# ---------------- A RESPOSTA ----------------
b("A RESPOSTA",
  "[serious] Então, voltando a Fortaleza, mil oitocentos e setenta e oito.\nUma cidade de vinte e cinco mil pessoas, que recebeu mais de cem mil.\nNão foi só a falta de chuva.\nFoi um dos El Niños mais fortes da história, um Atlântico que segurou as nuvens longe do Ceará e um país que demorou a agir.",
  "Então, voltando a Fortaleza, 1878. | Uma cidade de 25 mil pessoas, que recebeu mais de 100 mil. | Não foi só a falta de chuva. | Foi um dos El Niños mais fortes da história, | um Atlântico que segurou as nuvens longe do Ceará | e um país que demorou a agir.")
b("A RESPOSTA",
  "Aquela seca levou trilhos para o sertão, fez nascer o primeiro grande açude e empurrou nordestinos até o Acre.\nO El Niño de dois mil e vinte e seis pode trazer outra seca.\n[serious] Mas o que transforma seca em tragédia não é só o clima.\nÉ o que se faz antes dela.",
  "Aquela seca levou trilhos para o sertão, | fez nascer o primeiro grande açude | e empurrou nordestinos até o Acre. | O El Niño de 2026 pode trazer outra seca. | Mas o que transforma seca em tragédia não é só o clima. | É o que se faz antes dela.")
b("A RESPOSTA",
  "Se você tem família no sertão, manda este vídeo para ela.\nE se inscreve no canal, para entender o clima do Brasil.",
  "Se você tem família no sertão, manda este vídeo para ela. | E se inscreve no canal, para entender o clima do Brasil.")

if __name__ == "__main__":
    json.dump(B, open(Path(__file__).parent / "blocos.json", "w"), ensure_ascii=False, indent=1)
    n = sum(len(re.findall(r"\w+", x["fala"])) for x in B)
    ch = sum(len(" ".join(l.strip() for l in x["fala_tts"].split("\n"))) for x in B)
    print(len(B), "blocos;", n, "palavras faladas;", ch, "caracteres para o TTS")
