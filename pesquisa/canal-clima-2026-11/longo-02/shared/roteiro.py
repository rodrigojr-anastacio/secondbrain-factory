# Roteiro do longo 02 (Em Relevo, Super El Niño 2026 e o Brasil). Fonte única do texto -> shared/blocos.json.
# Base: ../longo-02-proposta/ROTEIRO-rascunho.md (aprovado 09/11) + correções de pesquisa/CHECAGEM.md (09/11).
# Cada bloco: id, cap (aba), fala_tts (com tags v3), fala (limpa), tela (algarismos; "|" separa cartões da legenda).
# "atualizar": True = depende do boletim NOAA de 12/11 (slot fixo na timeline; ver ATUALIZAR-12-11.md).
import json, re
from pathlib import Path

B = []
TAG = re.compile(r"\[[a-z ]+\]\s*")
def b(cap, fala, tela, atualizar=False):
    fala = fala.strip()
    B.append({"id": f"b{len(B)+1:02d}", "cap": cap, "marcha": 1 if len(B) < 7 else 2, "fala": TAG.sub("", fala), "fala_tts": fala,
              "tela": tela.strip(), "atualizar": atualizar})

# ---------------- HOOK ----------------
b("MANAUS",
  "[serious] Manaus, nove de outubro.\nA fumaça das queimadas fecha escolas e universidades.\nDe manhã, os sensores da cidade marcam quase duzentos microgramas de fumaça fina por metro cúbico de ar.\nA OMS recomenda no máximo quinze.",
  "Manaus, 9 de outubro. | A fumaça das queimadas fecha escolas e universidades. | De manhã, os sensores da cidade marcam | quase 200 microgramas de fumaça fina por metro cúbico de ar. | A OMS recomenda no máximo 15.")
b("SANTA CATARINA",
  "[serious] No mesmo mês, em Dionísio Cerqueira, Santa Catarina, chovem quinhentos e oitenta e um milímetros.\nMais de meio metro de água em um mês.",
  "No mesmo mês, em Dionísio Cerqueira, Santa Catarina, | chovem 581 milímetros. | Mais de meio metro de água em um mês.")
b("PACÍFICO",
  "[serious] E do outro lado dos Andes, na costa do Peru, o mar está cinco graus e meio acima do normal.",
  "E do outro lado dos Andes, na costa do Peru, | o mar está 5 graus e meio acima do normal.")
b("A PERGUNTA",
  "Fumaça no Norte. Água demais no Sul. Mar quente no Pacífico.\nParecem três notícias diferentes.\nMas têm o mesmo nome.",
  "Fumaça no Norte. Água demais no Sul. Mar quente no Pacífico. | Parecem 3 notícias diferentes. | Mas têm o mesmo nome.")
b("A PERGUNTA",
  "[curious] Então... esse é mesmo o tal Super El Niño?\n[intrigued] E o que ele vai fazer com o Brasil neste verão?",
  "Então... esse é mesmo o tal Super El Niño? | E o que ele vai fazer com o Brasil neste verão?")
b("A PERGUNTA",
  "[serious] Isso nos leva às seguintes perguntas.\n[curious] O que é, afinal, o El Niño?\n[curious] Por que este é diferente?\n[curious] O que muda na minha região?\n[intrigued] E até quando isso vai durar?",
  "Isso nos leva às seguintes perguntas. | O que é, afinal, o El Niño? | Por que este é diferente? | O que muda na minha região? | E até quando isso vai durar?")
b("A PERGUNTA",
  "[serious] Mas antes, é preciso entender uma coisa.\nO El Niño não começa no Brasil.\nComeça a mais de dez mil quilômetros daqui, no meio do oceano.",
  "Mas antes, é preciso entender uma coisa. | O El Niño não começa no Brasil. | Começa a mais de 10 mil quilômetros daqui, no meio do oceano.")

# ---------------- 1/4 O QUE É ----------------
C1 = "PERGUNTA 1/4 · O QUE É"
b(C1,
  "Imagine o Pacífico equatorial como uma piscina que ocupa quase metade da volta do planeta.\nNormalmente, ventos constantes, os alísios, sopram de leste para oeste.\nDa América do Sul em direção à Indonésia.",
  "Imagine o Pacífico equatorial como uma piscina | que ocupa quase metade da volta do planeta. | Normalmente, ventos constantes, os alísios, | sopram de leste para oeste. | Da América do Sul em direção à Indonésia.")
b(C1,
  "Esses ventos empurram a água quente da superfície para o oeste.\nEla se acumula lá, do lado da Indonésia.\nO mar chega a ficar meio metro mais alto do que na costa do Equador.\nE, no lugar da água quente que foi embora, sobe água fria do fundo, perto da América do Sul.",
  "Esses ventos empurram a água quente da superfície para o oeste. | Ela se acumula lá, do lado da Indonésia. | O mar chega a ficar meio metro mais alto | do que na costa do Equador. | E, no lugar da água quente que foi embora, | sobe água fria do fundo, perto da América do Sul.")
b(C1,
  "Onde a água é quente, o ar sobe, forma nuvens e chove.\nÉ por isso que chove tanto na Indonésia.\nDo lado de cá, sobre a água fria, o ar desce.\nE ar que desce é ar seco.",
  "Onde a água é quente, o ar sobe, forma nuvens e chove. | É por isso que chove tanto na Indonésia. | Do lado de cá, sobre a água fria, o ar desce. | E ar que desce é ar seco.")
b(C1,
  "Agora, o El Niño.\nA cada dois a sete anos, esses ventos enfraquecem.\nE a água quente, que estava represada a oeste, escorre de volta para o leste.\nComo numa gangorra.\nUma faixa de mar quente se espalha pelo meio do Pacífico, até a costa da América do Sul.",
  "Agora, o El Niño. | A cada 2 a 7 anos, esses ventos enfraquecem. | E a água quente, que estava represada a oeste, | escorre de volta para o leste. | Como numa gangorra. | Uma faixa de mar quente se espalha pelo meio do Pacífico, | até a costa da América do Sul.")
b(C1,
  "E a chuva vai junto com a água quente.\nO lugar onde o ar sobe se desloca milhares de quilômetros.\nE isso reorganiza a circulação do ar de meio planeta.\nInclusive em cima do Brasil.",
  "E a chuva vai junto com a água quente. | O lugar onde o ar sobe se desloca milhares de quilômetros. | E isso reorganiza a circulação do ar de meio planeta. | Inclusive em cima do Brasil.")
b(C1,
  "O nome veio dos pescadores do Peru, no século dezenove.\nDe alguns em alguns anos, eles percebiam a água esquentar perto do Natal.\nE chamaram aquela corrente de El Niño.\nO Menino.\nUma referência ao menino Jesus.",
  "O nome veio dos pescadores do Peru, no século 19. | De alguns em alguns anos, | eles percebiam a água esquentar perto do Natal. | E chamaram aquela corrente de El Niño. | O Menino. | Uma referência ao menino Jesus.")
b(C1,
  "Para medir o El Niño, os cientistas olham um retângulo específico no meio do Pacífico, chamado Niño três ponto quatro.\nSe a água fica meio grau acima do normal, por alguns meses, é El Niño.\nAcima de um grau e meio, é forte.\nAcima de dois, muito forte.\nE é aqui que aparece a palavra que você tem ouvido: super.",
  "Para medir o El Niño, os cientistas olham um retângulo | no meio do Pacífico, chamado Niño 3.4. | Se a água fica meio grau acima do normal, por alguns meses, é El Niño. | Acima de 1 grau e meio, é forte. | Acima de 2, muito forte. | E é aqui que aparece a palavra que você tem ouvido: super.")

# ---------------- 2/4 É SUPER? ----------------
C2 = "PERGUNTA 2/4 · É SUPER?"
b(C2,
  "[curious] Então, por que este é diferente?\n[curious] Ele é mesmo um super El Niño?",
  "Então, por que este é diferente? | Ele é mesmo um super El Niño?")
b(C2,
  "Primeiro, os fatos.\nEm junho, o Pacífico ainda estava morno.\nEm setembro, já era outra coisa.\nE em outubro, segundo o Inméti, aquela região teve a maior anomalia para o mês desde que existe registro.\nMaior até que a de mil novecentos e oitenta e dois.\nNa costa do Peru, o mar passa dos cinco graus acima do normal.",
  "Primeiro, os fatos. | Em junho, o Pacífico ainda estava morno. | Em setembro, já era outra coisa. | E em outubro, segundo o Inmet, aquela região teve | a maior anomalia para o mês desde que existe registro. | Maior até que a de 1982. | Na costa do Peru, o mar passa dos 5 graus acima do normal.")
b(C2,
  "Agora, compare com os grandes El Niños da história.\nMil novecentos e oitenta e dois e oitenta e três. Noventa e sete e noventa e oito. Dois mil e quinze e dezesseis. E o mais recente, de dois mil e vinte e três e vinte e quatro.\nPelo termômetro tradicional, o El Niño de dois mil e vinte e seis já passou o de oitenta e dois e o de noventa e sete.\nE está a pouco mais de um décimo de grau do recorde de dois mil e quinze.\nIsso em outubro. Dois ou três meses antes do pico.",
  "Agora, compare com os grandes El Niños da história. | 1982 e 83. 97 e 98. 2015 e 16. | E o mais recente, de 2023 e 24. | Pelo termômetro tradicional, o El Niño de 2026 | já passou o de 82 e o de 97. | E está a pouco mais de 1 décimo de grau do recorde de 2015. | Isso em outubro. Dois ou três meses antes do pico.")
b(C2,
  "[intrigued] Mas tem um detalhe que quase ninguém conta.\nO planeta inteiro está mais quente.\nE o oceano tropical todo esquentou junto.\nPor isso, este ano, a NOAA, a agência americana que é a referência mundial no assunto, passou a usar um termômetro novo.\nEle desconta esse aquecimento geral e mede só o quanto o Pacífico está mais quente que o resto dos trópicos.\nPorque é essa diferença que mexe com o clima.",
  "Mas tem um detalhe que quase ninguém conta. | O planeta inteiro está mais quente. | E o oceano tropical todo esquentou junto. | Por isso, este ano, a NOAA, a agência americana | que é a referência mundial no assunto, | passou a usar um termômetro novo. | Ele desconta esse aquecimento geral | e mede só o quanto o Pacífico está mais quente que o resto dos trópicos. | Porque é essa diferença que mexe com o clima.")
# --- slot [ATUALIZAR 12/11]: b19–b21 (cenário de hoje = boletim de 08/10; variantes em ATUALIZAR-12-11.md) ---
b(C2,
  "E, com esse termômetro, a história muda.\nO recorde passa a ser o de mil novecentos e oitenta e dois e oitenta e três, com dois graus e quatro décimos.\nO de dois mil e vinte e seis está, hoje, em dois graus.\nJá é muito forte. Já passou o de dois mil e vinte e três.\nMas ainda não é o maior da história.",
  "E, com esse termômetro, a história muda. | O recorde passa a ser o de 1982 e 83, com 2 graus e 4 décimos. | O de 2026 está, hoje, em 2 graus. | Já é muito forte. Já passou o de 2023. | Mas ainda não é o maior da história.", atualizar=True)
b(C2,
  "[curious] Pode virar?\nPode.\nNo último boletim, a própria NOAA calculou entre setenta e oitenta e três por cento de chance de ele se tornar o mais forte desde mil novecentos e cinquenta, quando as medições começaram.\nE os vinte e sete modelos de previsão acompanhados pela Universidade Columbia apontam para um El Niño muito forte até fevereiro.",
  "Pode virar? | Pode. | No último boletim, a própria NOAA calculou entre 70 e 83% de chance | de ele se tornar o mais forte desde 1950, quando as medições começaram. | E os 27 modelos de previsão acompanhados pela Universidade Columbia | apontam para um El Niño muito forte até fevereiro.", atualizar=True)
b(C2,
  "[curious] Então, ele é super?\nSuper é um apelido da imprensa.\nNenhuma agência oficial usa essa palavra.\nO termo técnico é muito forte.\nE isso ele já é.\nSe vai virar recorde, a resposta vem nas próximas semanas.",
  "Então, ele é super? | Super é um apelido da imprensa. | Nenhuma agência oficial usa essa palavra. | O termo técnico é muito forte. | E isso ele já é. | Se vai virar recorde, a resposta vem nas próximas semanas.", atualizar=True)
b(C2,
  "E, antes de ir para o Brasil, uma coisa importante.\nO El Niño não é causado pelo aquecimento global.\nEle existe há milhares de anos.\nMas agora ele acontece por cima de um planeta mais quente.\nÉ como uma onda de calor que chega num dia que já estava quente.",
  "E, antes de ir para o Brasil, uma coisa importante. | O El Niño não é causado pelo aquecimento global. | Ele existe há milhares de anos. | Mas agora ele acontece por cima de um planeta mais quente. | É como uma onda de calor que chega num dia que já estava quente.")

# ---------------- 3/4 MINHA REGIÃO ----------------
C3 = "PERGUNTA 3/4 · MINHA REGIÃO"
b(C3,
  "[curious] Agora, a pergunta que mais importa para quem está aqui.\n[curious] O que muda na minha região?",
  "Agora, a pergunta que mais importa para quem está aqui. | O que muda na minha região?")
b(C3,
  "Lembra do ar que sobe sobre a água quente e desce sobre a água fria?\nCom o El Niño, esse ar passa a descer em cima da Amazônia e do norte do Nordeste.\nAr que desce não forma nuvem. Menos chuva.\nNo Sul acontece o contrário.\nA corrente de vento lá do alto, o jato subtropical, fica mais forte e segura as frentes frias e as tempestades em cima da região.\nMais chuva.",
  "Lembra do ar que sobe sobre a água quente e desce sobre a água fria? | Com o El Niño, esse ar passa a descer | em cima da Amazônia e do norte do Nordeste. | Ar que desce não forma nuvem. Menos chuva. | No Sul acontece o contrário. | A corrente de vento lá do alto, o jato subtropical, fica mais forte | e segura as frentes frias e as tempestades em cima da região. | Mais chuva.")
b(C3,
  "É esse o desenho que a previsão oficial mostra para novembro, dezembro e janeiro.\nO governo federal montou um painel só para o El Niño, com sete órgãos.\nE o resumo é este.\nChuva acima da média no Sul.\nAbaixo da média em boa parte do Norte e do Nordeste.\nE calor acima do normal em quase todo o país.",
  "É esse o desenho que a previsão oficial mostra | para novembro, dezembro e janeiro. | O governo federal montou um painel só para o El Niño, com 7 órgãos. | E o resumo é este. | Chuva acima da média no Sul. | Abaixo da média em boa parte do Norte e do Nordeste. | E calor acima do normal em quase todo o país.")
b("NORTE",
  "Comece pelo Norte.\nEm Roraima, no início de setembro, o rio Branco, em Boa Vista, ficou abaixo de todos os mínimos já registrados para aquela época do ano, segundo o Serviço Geológico do Brasil.",
  "Comece pelo Norte. | Em Roraima, no início de setembro, o rio Branco, em Boa Vista, | ficou abaixo de todos os mínimos já registrados para aquela época do ano, | segundo o Serviço Geológico do Brasil.")
b("NORTE",
  "No Amazonas, os focos de queimada em setembro foram quase quatro vezes os do ano passado.\nTrês mil setecentos e vinte e seis contra novecentos e quarenta e dois.\nE foi essa fumaça que fechou as escolas de Manaus.",
  "No Amazonas, os focos de queimada em setembro | foram quase 4 vezes os do ano passado. | 3.726 contra 942. | E foi essa fumaça que fechou as escolas de Manaus.")
b("NORTE",
  "[serious] Mas atenção.\nNão é a seca de dois mil e vinte e três e vinte e quatro se repetindo igual.\nO rio Negro, em Manaus, está uns quatro metros acima do que estava nesta mesma data em dois mil e vinte e quatro.\nO ponto crítico agora é o norte da Amazônia.\nRoraima, o alto rio Negro e o Amapá.\nE, em Roraima, o pior período de fogo costuma ir de dezembro a abril.",
  "Mas atenção. | Não é a seca de 2023 e 2024 se repetindo igual. | O rio Negro, em Manaus, está uns 4 metros acima | do que estava nesta mesma data em 2024. | O ponto crítico agora é o norte da Amazônia. | Roraima, o alto rio Negro e o Amapá. | E, em Roraima, o pior período de fogo costuma ir de dezembro a abril.")
b("NORDESTE",
  "No Nordeste, a seca já avança.\nA área em seca grave passou de dezesseis para vinte e oito por cento da região entre agosto e setembro.\nNo país, os municípios em seca extrema foram de quatro para sessenta e oito em dois meses, a maioria no Nordeste: Alagoas, Bahia, Sergipe e Pernambuco.\nPara o verão, a previsão é de menos chuva e mais calor no semiárido.",
  "No Nordeste, a seca já avança. | A área em seca grave passou de 16 para 28% da região | entre agosto e setembro. | No país, os municípios em seca extrema foram de 4 para 68 em 2 meses, | a maioria no Nordeste: Alagoas, Bahia, Sergipe e Pernambuco. | Para o verão, a previsão é de menos chuva e mais calor no semiárido.")
b("CENTRO-OESTE E SUDESTE",
  "No Centro-Oeste e no Sudeste, o sinal mais claro é o calor.\nTemperaturas acima do normal no verão.\nA chuva fica irregular.\nAcima da média em São Paulo, no Triângulo Mineiro e no Mato Grosso do Sul.\nAbaixo no norte de Minas e do Espírito Santo.\nE, em janeiro, cresce o risco de cheia nos rios Doce e Paraíba do Sul.",
  "No Centro-Oeste e no Sudeste, o sinal mais claro é o calor. | Temperaturas acima do normal no verão. | A chuva fica irregular. | Acima da média em São Paulo, no Triângulo Mineiro e no Mato Grosso do Sul. | Abaixo no norte de Minas e do Espírito Santo. | E, em janeiro, cresce o risco de cheia nos rios Doce e Paraíba do Sul.")
b("CENTRO-OESTE E SUDESTE",
  "[curious] E a pergunta que sempre aparece: vai faltar luz?\nOs números de agora não apontam para isso.\nEm outubro, os reservatórios das hidrelétricas estavam com sessenta e cinco vírgula nove por cento.\nO segundo maior nível para a data desde dois mil e quinze.",
  "E a pergunta que sempre aparece: vai faltar luz? | Os números de agora não apontam para isso. | Em outubro, os reservatórios das hidrelétricas estavam com 65,9%. | O 2º maior nível para a data desde 2015.")
b("SUL",
  "E chegamos ao Sul, onde o El Niño mais pesa.\nEm setembro, o rio Taquari voltou a inundar cidades como Muçum, Encantado, Estrela e Lajeado.\nEm outubro, o Inméti registrou chuva recorde no Sul.\nE, só na primeira semana de novembro, foram sete tornados confirmados na região, segundo o levantamento da Climatempo.",
  "E chegamos ao Sul, onde o El Niño mais pesa. | Em setembro, o rio Taquari voltou a inundar cidades | como Muçum, Encantado, Estrela e Lajeado. | Em outubro, o Inmet registrou chuva recorde no Sul. | E, só na primeira semana de novembro, foram 7 tornados confirmados na região, | segundo o levantamento da Climatempo.")
b("SUL",
  "Na primeira semana de novembro, os temporais atingiram mais de duzentos e sessenta municípios no Rio Grande do Sul e em Santa Catarina.",
  "Na primeira semana de novembro, os temporais atingiram | mais de 260 municípios no Rio Grande do Sul e em Santa Catarina.")
b("SUL",
  "O El Niño não causa cada tempestade.\nEle aumenta as chances.\nÉ o padrão que ele favorece no Sul: mais chuva, mais dias de temporal, solo encharcado e rios cheios.\nSe você quer entender por que o Sul virou corredor de tornados, a gente fez um vídeo inteiro só sobre isso.",
  "O El Niño não causa cada tempestade. | Ele aumenta as chances. | É o padrão que ele favorece no Sul: mais chuva, mais dias de temporal, | solo encharcado e rios cheios. | Se você quer entender por que o Sul virou corredor de tornados, | a gente fez um vídeo inteiro só sobre isso.")
b("SUL",
  "[intrigued] E um detalhe que vai contra a intuição.\nNo Rio Grande do Sul, a previsão é de temperatura abaixo do normal.\nCom mais nuvem e mais chuva, o calor fica contido.",
  "E um detalhe que vai contra a intuição. | No Rio Grande do Sul, a previsão é de temperatura abaixo do normal. | Com mais nuvem e mais chuva, o calor fica contido.")
b("SUL",
  "E o Sul conhece bem esse filme.\nEm mil novecentos e oitenta e três, durante um dos El Niños mais fortes da história, o rio Iguaçu, em União da Vitória, no Paraná, saiu de dois metros e meio para mais de dez metros.\nDezoito pessoas morreram.\nEm Blumenau, o Itajaí-Açu passou dos quinze metros.",
  "E o Sul conhece bem esse filme. | Em 1983, durante um dos El Niños mais fortes da história, | o rio Iguaçu, em União da Vitória, no Paraná, | saiu de 2 metros e meio para mais de 10 metros. | 18 pessoas morreram. | Em Blumenau, o Itajaí-Açu passou dos 15 metros.")
b("SUL",
  "[curious] E a grande enchente de dois mil e vinte e quatro, no Rio Grande do Sul?\nOs cientistas que estudaram o caso apontam o El Niño como um dos fatores, junto com o aquecimento global.\nE ela veio quando ele já estava perdendo força.\nOu seja, o perigo não termina junto com o pico.",
  "E a grande enchente de 2024, no Rio Grande do Sul? | Os cientistas que estudaram o caso apontam o El Niño como um dos fatores, | junto com o aquecimento global. | E ela veio quando ele já estava perdendo força. | Ou seja, o perigo não termina junto com o pico.")
b("O MUNDO",
  "E o efeito vai muito além do Brasil.\nO planeta sente o El Niño com uns três meses de atraso.\nOutubro de dois mil e vinte e seis já foi o outubro mais quente da história, segundo o Copernicus, o serviço europeu de clima.\nE uma análise do site Carbon Brief dá noventa e seis por cento de chance de dois mil e vinte e sete ser o ano mais quente já registrado.",
  "E o efeito vai muito além do Brasil. | O planeta sente o El Niño com uns 3 meses de atraso. | Outubro de 2026 já foi o outubro mais quente da história, | segundo o Copernicus, o serviço europeu de clima. | E uma análise do site Carbon Brief dá 96% de chance | de 2027 ser o ano mais quente já registrado.")

# ---------------- 4/4 ATÉ QUANDO ----------------
C4 = "PERGUNTA 4/4 · ATÉ QUANDO"
b(C4,
  "[curious] E a última pergunta.\nA mais buscada de todas: até quando isso vai durar?",
  "E a última pergunta. | A mais buscada de todas: até quando isso vai durar?")
b(C4,
  "O pico deve chegar até dezembro, no máximo em janeiro.\nBem no meio do nosso verão.\nA agência de meteorologia da Austrália e a maioria dos modelos apontam para o auge em novembro ou dezembro.",
  "O pico deve chegar até dezembro, no máximo em janeiro. | Bem no meio do nosso verão. | A agência de meteorologia da Austrália e a maioria dos modelos | apontam para o auge em novembro ou dezembro.")
b(C4,
  "Depois, ele perde força devagar.\nA NOAA espera El Niño até o outono, entre março e maio de dois mil e vinte e sete.\nE, a partir de abril, o mais provável é que o Pacífico volte ao normal.",
  "Depois, ele perde força devagar. | A NOAA espera El Niño até o outono, entre março e maio de 2027. | E, a partir de abril, o mais provável é que o Pacífico volte ao normal.")
b(C4,
  "[curious] E depois?\nDepois de oitenta e três, de noventa e oito e de dois mil e dezesseis, o Pacífico esfriou e virou para o lado oposto.\nÉ a La Niña, a irmã do El Niño, que costuma inverter o desenho no Brasil: seca no Sul, chuva no Norte.\nMas, para dois mil e vinte e sete, ninguém confirmou isso ainda.\nÉ comum. Não é garantido.",
  "E depois? | Depois de 83, de 98 e de 2016, o Pacífico esfriou | e virou para o lado oposto. | É a La Niña, a irmã do El Niño, que costuma inverter o desenho no Brasil: | seca no Sul, chuva no Norte. | Mas, para 2027, ninguém confirmou isso ainda. | É comum. Não é garantido.")
b(C4,
  "E lembre de dois mil e vinte e quatro.\nO próprio painel do governo avisa: o El Niño deve enfraquecer depois do primeiro trimestre, mas os efeitos dele na circulação do ar podem continuar.",
  "E lembre de 2024. | O próprio painel do governo avisa: | o El Niño deve enfraquecer depois do primeiro trimestre, | mas os efeitos dele na circulação do ar podem continuar.")

# ---------------- O QUE FAZER / RESPOSTA ----------------
b("O QUE FAZER",
  "[curious] Então, o que fazer?\nDepende de onde você mora.",
  "Então, o que fazer? | Depende de onde você mora.")
b("O QUE FAZER",
  "No Sul, receba os alertas da Defesa Civil.\nMande o seu cép por SMS para quatro, zero, um, nove, nove. É de graça.\nE, em temporal, fique longe de rios, de encostas e de árvores.",
  "No Sul, receba os alertas da Defesa Civil. | Mande o seu CEP por SMS para 40199. É de graça. | E, em temporal, fique longe de rios, de encostas e de árvores.")
b("O QUE FAZER",
  "No Norte, nos dias de fumaça, feche portas e janelas e, se precisar sair, use máscara do tipo PFF dois.\nE, onde o calor apertar, beba água mesmo sem sede, fuja do sol nas horas mais quentes e tenha atenção dobrada com idosos e crianças.",
  "No Norte, nos dias de fumaça, feche portas e janelas | e, se precisar sair, use máscara do tipo PFF2. | E, onde o calor apertar, beba água mesmo sem sede, | fuja do sol nas horas mais quentes | e tenha atenção dobrada com idosos e crianças.")
b("A RESPOSTA",
  "[serious] Então, voltando ao começo.\nA fumaça em Manaus, a chuva em Santa Catarina e o mar quente no Peru são a mesma história.\nUm vento que enfraqueceu no meio do Pacífico.\nO El Niño de dois mil e vinte e seis já é muito forte.\nPode virar o maior desde mil novecentos e cinquenta.\nE o pico chega agora, no nosso verão.",
  "Então, voltando ao começo. | A fumaça em Manaus, a chuva em Santa Catarina | e o mar quente no Peru são a mesma história. | Um vento que enfraqueceu no meio do Pacífico. | O El Niño de 2026 já é muito forte. | Pode virar o maior desde 1950. | E o pico chega agora, no nosso verão.")
b("A RESPOSTA",
  "Manda este vídeo para quem vai passar o verão no Sul, no Norte ou no Nordeste.\nE se inscreve: a gente volta aqui quando os números mudarem.",
  "Manda este vídeo para quem vai passar o verão no Sul, no Norte ou no Nordeste. | E se inscreve: a gente volta aqui quando os números mudarem.")

if __name__ == "__main__":
    json.dump(B, open(Path(__file__).parent / "blocos.json", "w"), ensure_ascii=False, indent=1)
    n = sum(len(re.findall(r"\w+", x["fala"])) for x in B)
    ch = sum(len(" ".join(l.strip() for l in x["fala_tts"].split("\n"))) for x in B)
    print(len(B), "blocos;", n, "palavras faladas;", ch, "caracteres para o TTS")
