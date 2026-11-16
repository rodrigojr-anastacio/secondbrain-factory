# Roteiro do longo 04 (Em Relevo, 1983: o El Niño que partiu o Brasil ao meio). Fonte única do texto -> shared/blocos.json.
# Base: serie-g1-el-nino/RELATORIO.md (ângulo A) + pesquisa/FATOS.md e CHECAGEM.md (13/11/2026).
# Mesmo formato do longo-02/03: id, cap (aba), marcha (1 = hook mais rápido), fala (limpa), fala_tts (tags v3, números por extenso),
# tela (algarismos; "|" separa os cartões da legenda). "fonte" = item de pesquisa/FATOS.md que sustenta o bloco.
import json, re
from pathlib import Path

B = []
TAG = re.compile(r"\[[a-z ]+\]\s*")
def b(cap, fala, tela, fonte=""):
    fala = fala.strip()
    B.append({"id": f"b{len(B)+1:02d}", "cap": cap, "marcha": 1 if len(B) < 6 else 2, "fala": TAG.sub("", fala), "fala_tts": fala,
              "tela": tela.strip(), "fonte": fonte})

C1 = "PERGUNTA 1/4 · O QUE ACONTECEU NO SUL"
C2 = "PERGUNTA 2/4 · O QUE ACONTECEU NO SERTÃO"
C3 = "PERGUNTA 3/4 · POR QUE OS DOIS AO MESMO TEMPO"
C4 = "PERGUNTA 4/4 · E EM 2026?"

# ---------------- HOOK ----------------
b("UNIÃO DA VITÓRIA (PR) · JULHO DE 1983",
  "[serious] União da Vitória, no Paraná. Julho de mil novecentos e oitenta e três.\nNormalmente, o rio Iguaçu passa ali com uns dois metros e meio.\nNo dia dezoito, ele chegou a dez metros e quarenta e dois centímetros.\nA água cobriu a cidade. Dezoito pessoas morreram.",
  "União da Vitória, no Paraná. Julho de 1983. | Normalmente, o rio Iguaçu passa ali com uns 2,5 metros. | No dia 18, ele chegou a 10,42 metros. | A água cobriu a cidade. Dezoito pessoas morreram.",
  "F1, F2")
b("BLUMENAU (SC) · JULHO DE 1983",
  "Uns duzentos quilômetros a leste, em Blumenau, o Itajaí-Açu passou dos quinze metros.\nEra a terceira cheia do rio naquele ano.\nE ainda viria uma quarta.",
  "Uns 200 quilômetros a leste, em Blumenau, | o Itajaí-Açu passou dos 15 metros. | Era a terceira cheia do rio naquele ano. | E ainda viria uma quarta.",
  "F3, F17")
b("MOMBAÇA (CE) · 1983",
  "[serious] Agora, suba dois mil e quinhentos quilômetros no mapa.\nSertão do Ceará, no mesmo ano.\nEm Mombaça, o pluviômetro marcou menos da metade da chuva normal.\nEra o quinto ano de uma seca que tinha começado em mil novecentos e setenta e nove.",
  "Agora, suba 2.500 quilômetros no mapa. | Sertão do Ceará, no mesmo ano. | Em Mombaça, o pluviômetro marcou menos da metade da chuva normal. | Era o quinto ano de uma seca que tinha começado em 1979.",
  "F5, F10, F17")
b("CANINDÉ (CE) · AGOSTO DE 1983",
  "Em agosto, segundo o Memorial da Democracia, cinco mil flagelados invadiram um armazém de comida do governo em Canindé, no Ceará.\nNo Nordeste, já eram dez milhões de flagelados.",
  "Em agosto, segundo o Memorial da Democracia, | 5 mil flagelados invadiram um armazém de comida do governo | em Canindé, no Ceará. | No Nordeste, já eram 10 milhões de flagelados.",
  "F8, F9")
b("A PERGUNTA",
  "[curious] O mesmo país. O mesmo ano.\nUma parte com água demais. A outra sem água nenhuma.\n[intrigued] E agora, com o El Niño de dois mil e vinte e seis, muita gente pergunta: isso pode acontecer de novo?",
  "O mesmo país. O mesmo ano. | Uma parte com água demais. A outra sem água nenhuma. | E agora, com o El Niño de 2026, muita gente pergunta: | isso pode acontecer de novo?")
b("A PERGUNTA",
  "[serious] Isso nos leva às seguintes perguntas.\n[curious] O que aconteceu no Sul?\n[curious] O que aconteceu no sertão?\n[curious] Por que os dois ao mesmo tempo?\n[intrigued] E o que isso diz sobre dois mil e vinte e seis?",
  "Isso nos leva às seguintes perguntas. | O que aconteceu no Sul? | O que aconteceu no sertão? | Por que os dois ao mesmo tempo? | E o que isso diz sobre 2026?")
b("A PERGUNTA",
  "[serious] Mas antes, olhe o mapa.\nO Sul recebe chuva o ano inteiro, trazida pelas frentes frias.\nO sertão depende de poucos meses de chuva, de fevereiro a maio.\nEm mil novecentos e oitenta e três, os dois foram empurrados para extremos opostos.",
  "Mas antes, olhe o mapa. | O Sul recebe chuva o ano inteiro, trazida pelas frentes frias. | O sertão depende de poucos meses de chuva, de fevereiro a maio. | Em 1983, os dois foram empurrados para extremos opostos.",
  "F16 (longo-02 b24, longo-03 b07)")

# ---------------- 1. O QUE ACONTECEU NO SUL ----------------
b(C1,
  "Comece pelo Iguaçu.\nEle nasce perto de Curitiba e corre para o oeste, até as Cataratas.\nEm União da Vitória, ele faz curvas largas numa várzea plana.\nE a cidade cresceu dentro dessas curvas.",
  "Comece pelo Iguaçu. | Ele nasce perto de Curitiba e corre para o oeste, até as Cataratas. | Em União da Vitória, ele faz curvas largas numa várzea plana. | E a cidade cresceu dentro dessas curvas.",
  "geografia (relevo ETOPO/Landsat)")
b(C1,
  "A chuva começou cedo.\nEm novembro de mil novecentos e oitenta e dois, o rio já tinha passado dos seis metros.\nEm maio de oitenta e três, de novo.\nNo começo de julho, ele estava em quase cinco metros. Cheio, mas sob controle.",
  "A chuva começou cedo. | Em novembro de 1982, o rio já tinha passado dos 6 metros. | Em maio de 83, de novo. | No começo de julho, ele estava em quase 5 metros. | Cheio, mas sob controle.",
  "F2")
b(C1,
  "[serious] Aí veio uma semana inteira de chuva.\nSegundo a Defesa Civil do Paraná, choveram uns oitocentos milímetros.\nA média de junho e julho, somados, é de cento e trinta e oito.\nQuase seis vezes mais, em uma semana.",
  "Aí veio uma semana inteira de chuva. | Segundo a Defesa Civil do Paraná, choveram uns 800 milímetros. | A média de junho e julho, somados, é de 138. | Quase 6 vezes mais, em uma semana.",
  "F1")
b(C1,
  "O rio respondeu.\nEm quinze dias, subiu mais de cinco metros e meio, até os dez metros e quarenta e dois, no dia dezoito de julho.\nE ficou acima dos seis metros por mais de um mês.",
  "O rio respondeu. | Em 15 dias, subiu mais de 5,5 metros, | até os 10,42 metros, no dia 18 de julho. | E ficou acima dos 6 metros por mais de um mês.",
  "F2")
b(C1,
  "A cidade ficou sem luz, sem água potável e sem comida chegando.\nMais de duas mil e quatrocentas famílias ficaram desamparadas.\nMuitas foram para a casa de parentes. A maioria, para abrigos.",
  "A cidade ficou sem luz, sem água potável e sem comida chegando. | Mais de 2.400 famílias ficaram desamparadas. | Muitas foram para a casa de parentes. | A maioria, para abrigos.",
  "F1")
b(C1,
  "Do espaço, dá para ver o tamanho disso.\nEste é o satélite Landsat 4 sobre União da Vitória no dia três de julho, antes da cheia grande.\nE este é o mesmo lugar no dia quatro de agosto, mais de duas semanas depois do pico, com o rio ainda acima dos sete metros.\nA várzea virou um lago.",
  "Do espaço, dá para ver o tamanho disso. | Este é o satélite Landsat 4 sobre União da Vitória | no dia 3 de julho, antes da cheia grande. | E este é o mesmo lugar no dia 4 de agosto, | mais de duas semanas depois do pico, | com o rio ainda acima dos 7 metros. | A várzea virou um lago.",
  "F2 (7,42 m em 04/08), cenas Landsat em FATOS §imagem")
b(C1,
  "No vale do Itajaí, em Santa Catarina, o problema é outro.\nO rio corre apertado entre morros.\nQuando enche, não tem para onde se espalhar. Sobe.",
  "No vale do Itajaí, em Santa Catarina, o problema é outro. | O rio corre apertado entre morros. | Quando enche, não tem para onde se espalhar. | Sobe.",
  "geografia (relevo)")
b(C1,
  "Em Blumenau, a régua do Itajaí-Açu passou dos dez metros em março.\nDos doze, em maio.\nNo dia nove de julho, chegou a quinze metros e trinta e quatro centímetros.\nE, em setembro, o rio encheu de novo.",
  "Em Blumenau, a régua do Itajaí-Açu passou dos 10 metros em março. | Dos 12, em maio. | No dia 9 de julho, chegou a 15,34 metros. | E, em setembro, o rio encheu de novo.",
  "F3")
b(C1,
  "[serious] Santa Catarina inteira foi atingida.\nSegundo um levantamento da geógrafa Maria Lúcia Herrmann, da Universidade Federal de Santa Catarina, setenta e oito municípios decretaram calamidade pública em julho.\nForam quarenta e nove mortos e quase duzentos mil desabrigados.",
  "Santa Catarina inteira foi atingida. | Segundo um levantamento da geógrafa Maria Lúcia Herrmann, da UFSC, | 78 municípios decretaram calamidade pública em julho. | Foram 49 mortos e quase 200 mil desabrigados.",
  "F4")

# ---------------- 2. O QUE ACONTECEU NO SERTÃO ----------------
b(C2,
  "[curious] Agora, o sertão.\nLá, a seca não tinha começado em oitenta e três.\nEla vinha desde mil novecentos e setenta e nove.",
  "Agora, o sertão. | Lá, a seca não tinha começado em 83. | Ela vinha desde 1979.",
  "F10")
b(C2,
  "Mombaça, no centro do Ceará, tem um pluviômetro do Dnócs que mede a chuva desde mil novecentos e dez.\nNa média, chove ali uns setecentos e oitenta milímetros por ano.\nEm oitenta e um, choveram quatrocentos e setenta e dois.\nEm oitenta e dois, quatrocentos e sete.\n[serious] E em oitenta e três, trezentos e sessenta e seis. Menos da metade.",
  "Mombaça, no centro do Ceará, tem um pluviômetro do DNOCS | que mede a chuva desde 1910. | Na média, chove ali uns 780 milímetros por ano. | Em 81, choveram 472. | Em 82, 407. | E em 83, 366. Menos da metade.",
  "F5")
b(C2,
  "No sertão, um ano ruim se aguenta.\nTrês seguidos, não.\nNo primeiro, a roça falha. No segundo, acaba o que estava guardado.\nNo terceiro, secam os açudes pequenos e o gado começa a morrer.",
  "No sertão, um ano ruim se aguenta. | Três seguidos, não. | No primeiro, a roça falha. | No segundo, acaba o que estava guardado. | No terceiro, secam os açudes pequenos e o gado começa a morrer.",
  "didático (Hipótese de narração, sem número)")
b(C2,
  "Sem colheita, o que sobrava era o trabalho que o governo oferecia nas frentes de emergência: obras de açude, de estrada e de poço.\nPelos números da Sudene, em mil novecentos e oitenta e três, mais de três milhões de pessoas se alistaram nelas.\nEm setenta e nove, tinham sido menos de quinhentas mil.",
  "Sem colheita, o que sobrava era o trabalho que o governo oferecia | nas frentes de emergência: | obras de açude, de estrada e de poço. | Pelos números da Sudene, em 1983, | mais de 3 milhões de pessoas se alistaram nelas. | Em 79, tinham sido menos de 500 mil.",
  "F7")
b(C2,
  "[serious] Em agosto, a fome virou revolta.\nFlagelados ocuparam a sede do governo do Ceará, em Fortaleza, pedindo comida.\nDois dias depois, em Canindé, a multidão invadiu o armazém da Cobal, a companhia de abastecimento do governo, e levou os alimentos.",
  "Em agosto, a fome virou revolta. | Flagelados ocuparam a sede do governo do Ceará, em Fortaleza, | pedindo comida. | Dois dias depois, em Canindé, a multidão invadiu o armazém da Cobal, | a companhia de abastecimento do governo, | e levou os alimentos.",
  "F8")
b(C2,
  "Quantas pessoas morreram?\nNinguém contou.\nNão existe um número oficial confiável, e as estimativas que circulam variam demais.\n[serious] Mas os relatos da época falam de muitas crianças mortas de fome e de doenças da desnutrição.",
  "Quantas pessoas morreram? | Ninguém contou. | Não existe um número oficial confiável, | e as estimativas que circulam variam demais. | Mas os relatos da época falam de muitas crianças mortas | de fome e de doenças da desnutrição.",
  "F9b (número fora), Memorial")
b(C2,
  "Foi uma das maiores secas do século vinte no Brasil.\nSó em mil novecentos e oitenta e quatro a chuva voltou ao normal.",
  "Foi uma das maiores secas do século 20 no Brasil. | Só em 1984 a chuva voltou ao normal.",
  "F10, F5 (1984 = 101% da média em Mombaça)")

# ---------------- 3. POR QUE OS DOIS AO MESMO TEMPO ----------------
b(C3,
  "[curious] Então, por que o Brasil teve as duas coisas no mesmo ano?\nA resposta não está no Brasil.\nEstá no meio do oceano Pacífico.",
  "Então, por que o Brasil teve as duas coisas no mesmo ano? | A resposta não está no Brasil. | Está no meio do oceano Pacífico.")
b(C3,
  "Entre oitenta e dois e oitenta e três, o Pacífico tropical esquentou como nunca, desde que as medições modernas começaram, em mil novecentos e cinquenta.\nPelo índice que a NOAA usa hoje para comparar El Niños, aquele chegou a dois graus e quatro décimos acima do normal.\n[serious] Até hoje, é o recorde.",
  "Entre 82 e 83, o Pacífico tropical esquentou como nunca, | desde que as medições modernas começaram, em 1950. | Pelo índice que a NOAA usa hoje para comparar El Niños, | aquele chegou a 2,4 graus acima do normal. | Até hoje, é o recorde.",
  "F11")
b(C3,
  "No nosso vídeo sobre o El Niño, a gente mostrou como isso funciona.\nO ar sobe em cima da água quente do Pacífico.\nE desce em outros lugares. Um deles é o norte do Nordeste.\nE ar que desce não forma nuvem.",
  "No nosso vídeo sobre o El Niño, a gente mostrou como isso funciona. | O ar sobe em cima da água quente do Pacífico. | E desce em outros lugares. Um deles é o norte do Nordeste. | E ar que desce não forma nuvem.",
  "F16")
b(C3,
  "E o calendário piorou tudo.\nO pico do El Niño foi em dezembro e janeiro.\nBem na entrada da época de chuva do sertão, de fevereiro a maio.\nO inverno do sertanejo veio fraco, pelo terceiro ano seguido.",
  "E o calendário piorou tudo. | O pico do El Niño foi em dezembro e janeiro. | Bem na entrada da época de chuva do sertão, de fevereiro a maio. | O inverno do sertanejo veio fraco, pelo terceiro ano seguido.",
  "F11 (DJF 1983 +2,40; MAM +1,30), F5")
b(C3,
  "No Sul, acontece o contrário.\nO El Niño reforça uma corrente de vento lá no alto, o jato subtropical.\nEle segura as frentes frias e as tempestades em cima da região.\nE, em oitenta e três, um estudo do Inpe também encontrou bloqueios: o tempo travado no mesmo lugar, chovendo por dias.",
  "No Sul, acontece o contrário. | O El Niño reforça uma corrente de vento lá no alto, o jato subtropical. | Ele segura as frentes frias e as tempestades em cima da região. | E, em 83, um estudo do Inpe também encontrou bloqueios: | o tempo travado no mesmo lugar, chovendo por dias.",
  "F14")
b(C3,
  "[intrigued] E aqui tem um detalhe que quase ninguém percebe.\nEm julho de oitenta e três, quando o Iguaçu bateu os dez metros, o Pacífico já estava esfriando.\nO El Niño estava acabando.\n[serious] E mesmo assim, a pior enchente veio ali.",
  "E aqui tem um detalhe que quase ninguém percebe. | Em julho de 83, quando o Iguaçu bateu os 10 metros, | o Pacífico já estava esfriando. | O El Niño estava acabando. | E mesmo assim, a pior enchente veio ali.",
  "F11 (MJJ 1983 +0,47), F2")
b(C3,
  "Isso tem explicação.\nNo Sul do Brasil, o El Niño costuma trazer chuva a mais em duas épocas: na primavera em que ele começa, e no outono e no inverno do ano seguinte.\nFoi o que aconteceu: cheia em novembro de oitenta e dois, cheias em maio e julho de oitenta e três.\n[serious] Guarde isso. Vai importar em dois mil e vinte e seis.",
  "Isso tem explicação. | No Sul do Brasil, o El Niño costuma trazer chuva a mais em duas épocas: | na primavera em que ele começa, | e no outono e no inverno do ano seguinte. | Foi o que aconteceu: cheia em novembro de 82, | cheias em maio e julho de 83. | Guarde isso. Vai importar em 2026.",
  "F15, F2")
b(C3,
  "Ou seja, o mesmo aquecimento do Pacífico desligou a chuva no sertão e ligou a chuva no Sul.\nDuas pontas do mesmo fenômeno, a dois mil e quinhentos quilômetros uma da outra.",
  "Ou seja, o mesmo aquecimento do Pacífico | desligou a chuva no sertão e ligou a chuva no Sul. | Duas pontas do mesmo fenômeno, | a 2.500 quilômetros uma da outra.",
  "F16, F17")
b(C3,
  "Mas o clima não explica tudo.\nNo sertão, sofreu mais quem não tinha água guardada nem outra renda.\nNo Sul, quem morava na várzea, colado no rio.\n[serious] O El Niño escolheu os lugares. A forma como a gente ocupa esses lugares escolheu quem ia sofrer mais.",
  "Mas o clima não explica tudo. | No sertão, sofreu mais quem não tinha água guardada nem outra renda. | No Sul, quem morava na várzea, colado no rio. | O El Niño escolheu os lugares. | A forma como a gente ocupa esses lugares escolheu quem ia sofrer mais.",
  "fecho editorial (sem número)")

# ---------------- 4. E EM 2026? ----------------
b(C4,
  "[curious] E a última pergunta.\nO que mil novecentos e oitenta e três diz sobre dois mil e vinte e seis?",
  "E a última pergunta. | O que 1983 diz sobre 2026?")
b(C4,
  "O El Niño deste ano já é muito forte.\nNo boletim de doze de novembro, a NOAA mediu a região que define o El Niño dois graus e meio acima do normal.\nE calculou cerca de sessenta por cento de chance de ele virar o mais forte desde mil novecentos e cinquenta.\nOu seja: é mais provável que sim. Mas não é certeza.",
  "O El Niño deste ano já é muito forte. | No boletim de 12 de novembro, a NOAA mediu a região que define o El Niño | 2,5 graus acima do normal. | E calculou cerca de 60% de chance | de ele virar o mais forte desde 1950. | Ou seja: é mais provável que sim. Mas não é certeza.",
  "F13")
b(C4,
  "E o Sul já sentiu.\nEm outubro, o Inmet registrou chuva recorde na região, com quase seiscentos milímetros no mês em Laranjeiras do Sul, no Paraná, e em Dionísio Cerqueira, em Santa Catarina.\nE, no começo de novembro, temporais causaram estragos em cinquenta e quatro cidades catarinenses.",
  "E o Sul já sentiu. | Em outubro, o Inmet registrou chuva recorde na região, | com quase 600 milímetros no mês | em Laranjeiras do Sul (PR) e em Dionísio Cerqueira (SC). | E, no começo de novembro, | temporais causaram estragos em 54 cidades catarinenses.",
  "F18, F19")
b(C4,
  "Agora, lembra do detalhe de oitenta e três?\nA pior enchente veio quando o El Niño já estava acabando.\nA NOAA prevê que o de agora comece a enfraquecer no início de dois mil e vinte e sete.\n[serious] Isso não é previsão de enchente. Mas, pelo que oitenta e três mostrou, o outono e o inverno do ano que vem também merecem atenção no Sul.",
  "Agora, lembra do detalhe de 83? | A pior enchente veio quando o El Niño já estava acabando. | A NOAA prevê que o de agora comece a enfraquecer no início de 2027. | Isso não é previsão de enchente. | Mas, pelo que 83 mostrou, o outono e o inverno do ano que vem | também merecem atenção no Sul.",
  "F13, F15")
b(C4,
  "E o sertão?\nA previsão oficial para novembro, dezembro e janeiro é de chuva abaixo da média em áreas do Nordeste, principalmente no norte da região.\nMas o que decide é a época de chuva de fevereiro a maio de dois mil e vinte e sete.\nE a Funceme, o órgão de meteorologia do Ceará, diz que ainda é cedo para prever.",
  "E o sertão? | A previsão oficial para novembro, dezembro e janeiro | é de chuva abaixo da média em áreas do Nordeste, | principalmente no norte da região. | Mas o que decide é a época de chuva de fevereiro a maio de 2027. | E a Funceme, o órgão de meteorologia do Ceará, | diz que ainda é cedo para prever.",
  "F20")
b(C4,
  "E o Brasil de hoje não é o de oitenta e três.\nNo semiárido, há mais de um milhão e duzentas mil cisternas guardando água da chuva ao lado das casas.\nA seca de dois mil e doze a dois mil e dezessete, uma das piores em décadas, não trouxe a fome em massa das secas do passado.",
  "E o Brasil de hoje não é o de 83. | No semiárido, há mais de 1,2 milhão de cisternas | guardando água da chuva ao lado das casas. | A seca de 2012 a 2017, uma das piores em décadas, | não trouxe a fome em massa das secas do passado.",
  "F21, longo-03 b43")
b(C4,
  "No Sul, os vales do Iguaçu e do Itajaí têm hoje sistemas de alerta de cheia, e a Defesa Civil manda aviso no celular.\nMas as várzeas continuam ocupadas.\n[serious] E um rio que já subiu dez metros pode subir de novo.",
  "No Sul, os vales do Iguaçu e do Itajaí têm hoje sistemas de alerta de cheia, | e a Defesa Civil manda aviso no celular. | Mas as várzeas continuam ocupadas. | E um rio que já subiu 10 metros pode subir de novo.",
  "F22 (genérico)")

# ---------------- A RESPOSTA ----------------
b("A RESPOSTA",
  "[serious] Então, voltando a julho de mil novecentos e oitenta e três.\nO Iguaçu a dez metros em União da Vitória.\nE, a dois mil e quinhentos quilômetros dali, o sertão no quinto ano de seca.\nNão foram duas tragédias sem ligação.\nFoi o mesmo El Niño, puxando o Brasil para os dois lados.",
  "Então, voltando a julho de 1983. | O Iguaçu a 10 metros em União da Vitória. | E, a 2.500 quilômetros dali, o sertão no quinto ano de seca. | Não foram duas tragédias sem ligação. | Foi o mesmo El Niño, puxando o Brasil para os dois lados.")
b("A RESPOSTA",
  "O de dois mil e vinte e seis pode repetir esse padrão. Ou não: nenhum El Niño é igual ao outro.\n[serious] Mas mil novecentos e oitenta e três deixou uma lição.\nO perigo não acaba quando o Pacífico começa a esfriar.",
  "O de 2026 pode repetir esse padrão. Ou não: | nenhum El Niño é igual ao outro. | Mas 1983 deixou uma lição. | O perigo não acaba quando o Pacífico começa a esfriar.")
b("A RESPOSTA",
  "Se você quer entender como o El Niño funciona, o nosso vídeo sobre ele está aqui no canal.\nSe você tem família no Sul ou no sertão, manda este vídeo para ela.\nE se inscreve no canal, para entender o clima do Brasil.",
  "Se você quer entender como o El Niño funciona, | o nosso vídeo sobre ele está aqui no canal. | Se você tem família no Sul ou no sertão, manda este vídeo para ela. | E se inscreve no canal, para entender o clima do Brasil.",
  "CTA: puxa sessão para FeSLzHvlkbo (publicado); sem gancho de próximo vídeo")

if __name__ == "__main__":
    json.dump(B, open(Path(__file__).parent / "blocos.json", "w"), ensure_ascii=False, indent=1)
    n = sum(len(re.findall(r"\w+", x["fala"])) for x in B)
    ch = sum(len(" ".join(l.strip() for l in x["fala_tts"].split("\n"))) for x in B)
    print(len(B), "blocos;", n, "palavras faladas;", ch, "caracteres para o TTS")
