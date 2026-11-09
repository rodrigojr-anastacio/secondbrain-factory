# Roteiro do longo 01 (fonte única do texto). Gera shared/blocos.json.
# Cada bloco: id, cap (aba de capítulo), marcha (1 = rápida como o piloto; 2 = mais calma; 1.5 = transição),
# fala (o que a Kokoro lê: números por extenso, uma frase por linha) e tela (legenda: números em algarismos; "|" separa os cartões).
import json, re
from pathlib import Path

B = []
TAG = re.compile(r"\[[a-z ]+\]\s*")
def b(cap, marcha, fala, tela):
    # v2 (ElevenLabs v3): "fala_tts" leva as tags de emoção; "fala" é o texto limpo (Whisper, contagem de palavras)
    fala = fala.strip()
    B.append({"id": f"b{len(B)+1:02d}", "cap": cap, "marcha": marcha, "fala": TAG.sub("", fala), "fala_tts": fala, "tela": tela.strip()})

# ---------------- HOOK (o do piloto, aprovado) ----------------
b("MARINGÁ", 1,
  "[serious] Maringá, Paraná, dois de novembro.\nUm tornado éfe dois, com ventos de até duzentos e cinquenta quilômetros por hora, atinge quarenta por cento da cidade.",
  "Maringá, Paraná, 2 de novembro. | Um tornado F2, com ventos de até 250 km/h, | atinge 40% da cidade.")
b("CHAPECÓ", 1,
  "[serious] Dois dias depois, Chapecó, Santa Catarina.\nDezesseis quilômetros de destruição.\nPara a Defesa Civil, o maior evento climático em cinquenta anos.",
  "Dois dias depois, Chapecó, Santa Catarina. | 16 km de destruição. | Para a Defesa Civil, | o maior evento climático em 50 anos.")
b("SANTO AUGUSTO", 1,
  "[serious] No dia sete, Santo Augusto, no Rio Grande do Sul.\nCinquenta casas destelhadas de madrugada.",
  "No dia 7, Santo Augusto, no Rio Grande do Sul. | 50 casas destelhadas de madrugada.")
b("7 EM 6 DIAS", 1,
  "[serious] Sete tornados confirmados em seis dias.",
  "7 tornados confirmados em 6 dias.")
b("A PERGUNTA", 1,
  "[curious] Então... o que está acontecendo no Sul do Brasil?\n[intrigued] Por que tantos eventos dessa magnitude, como nunca antes?",
  "Então... o que está acontecendo no Sul do Brasil? | Por que tantos eventos dessa magnitude, | como nunca antes?")
b("A PERGUNTA", 1,
  "[serious] Isso nos leva às seguintes perguntas.\n[curious] Por que isso está acontecendo?\n[curious] Qual o risco de voltar a acontecer?\n[intrigued] E até que proporção isso pode chegar?",
  "Isso nos leva às seguintes perguntas. | Por que isso está acontecendo? | Qual o risco de voltar a acontecer? | E até que proporção isso pode chegar?")
b("A PERGUNTA", 1,
  "[serious] Mas antes, é preciso entender o que aconteceu de verdade nesses seis dias.\nPorque não foi um evento só.",
  "Mas antes, é preciso entender o que aconteceu de verdade nesses 6 dias. | Porque não foi um evento só.")

# ---------------- 7 TORNADOS EM 6 DIAS ----------------
b("DIA 1 · 2/11", 1.5,
  "[serious] Domingo à noite, primeiro de novembro.\nUm ciclone se forma na costa do Rio Grande do Sul e organiza uma frente fria, que avança pelo Paraná.\nPor volta das três da manhã, uma supercélula chega a Maringá.",
  "Domingo à noite, 1º de novembro. | Um ciclone se forma na costa do Rio Grande do Sul | e organiza uma frente fria, que avança pelo Paraná. | Por volta das 3 da manhã, | uma supercélula chega a Maringá.")
b("DIA 1 · 2/11", 1.5,
  "O aeroporto mede rajadas de quase cem quilômetros por hora.\nMas o vento mais forte não passou pela estação.\nO Simepar foi a campo, mediu o estrago e classificou o tornado como éfe dois: ventos estimados entre cento e oitenta e duzentos e cinquenta e três quilômetros por hora, num rastro de uns quinze quilômetros.",
  "O aeroporto mede rajadas de quase 100 km/h. | Mas o vento mais forte não passou pela estação. | O Simepar foi a campo, mediu o estrago | e classificou o tornado como F2: | ventos estimados entre 180 e 253 km/h, | num rastro de uns 15 km.")
b("DIA 1 · 2/11", 2,
  "Ninguém morreu.\nMas, dois dias depois, a cidade ainda contava quase novecentas árvores no chão, duzentos e dezenove postes quebrados e trinta e cinco mil imóveis sem luz.",
  "Ninguém morreu. | Mas, 2 dias depois, a cidade ainda contava | quase 900 árvores no chão, | 219 postes quebrados | e 35 mil imóveis sem luz.")
b("DIA 3 · 4/11", 2,
  "Dois dias de trégua.\nE então vem a quarta-feira, quatro de novembro, o dia mais violento da semana.\nUma linha de tempestades atravessa o oeste de Santa Catarina e o norte gaúcho.",
  "2 dias de trégua. | E então vem a quarta-feira, 4 de novembro, | o dia mais violento da semana. | Uma linha de tempestades atravessa | o oeste de Santa Catarina e o norte gaúcho.")
b("DIA 3 · 4/11", 2,
  "[serious] Dez e meia da manhã, Chapecó.\nO radar mostra o vento girando dentro da tempestade.\nUma estação do Inméti mede cento e vinte e seis quilômetros por hora.\nNo aeroporto, um avião da Azul está parado na pista, e a tripulação descreve: o avião está chacoalhando muito.",
  "10h30 da manhã, Chapecó. | O radar mostra o vento girando dentro da tempestade. | Uma estação do Inmet mede 126 km/h. | No aeroporto, um avião da Azul está parado na pista, | e a tripulação descreve: | \"o avião está chacoalhando muito\".")
b("DIA 3 · 4/11", 2,
  "Hangares destruídos, peças de metal arrancadas, cerca de duas mil e quatrocentas casas e indústrias destelhadas.\nA Defesa Civil tinha emitido o aviso de temporal quinze minutos antes.",
  "Hangares destruídos, peças de metal arrancadas, | cerca de 2.400 casas e indústrias destelhadas. | A Defesa Civil tinha emitido o aviso de temporal | 15 minutos antes.")
b("DIA 3 · 4/11", 2,
  "Dezoito minutos depois, a mesma linha de tempestades gera outro tornado, em Xanxerê, a uns quarenta quilômetros dali.\nCaminhões e ônibus tombam na rodovia.",
  "18 minutos depois, a mesma linha de tempestades | gera outro tornado, em Xanxerê, | a uns 40 km dali. | Caminhões e ônibus tombam na rodovia.")
b("DIA 3 · 4/11", 2,
  "Na mesma manhã, do outro lado do rio Uruguai, um tornado arrasa um eucaliptal inteiro em Erval Grande e derruba uma torre de alta tensão em Barra do Rio Azul.\nE à uma e meia da tarde, já no Planalto Norte, é a vez de Rio Negrinho: oitenta e duas casas atingidas.",
  "Na mesma manhã, do outro lado do rio Uruguai, | um tornado arrasa um eucaliptal inteiro em Erval Grande | e derruba uma torre de alta tensão em Barra do Rio Azul. | E à 1h30 da tarde, já no Planalto Norte, | é a vez de Rio Negrinho: | 82 casas atingidas.")
b("DIA 3 · 4/11", 2,
  "Quatro tornados num único dia.\nNos temporais daquela quarta-feira, duas pessoas morreram em Santa Catarina.",
  "4 tornados num único dia. | Nos temporais daquela quarta-feira, | 2 pessoas morreram em Santa Catarina.")
b("DIA 6 · 7/11", 2,
  "[serious] Sábado, sete de novembro, de madrugada.\nUma única supercélula cruza o noroeste gaúcho.\nÀ uma e dezoito, Santo Augusto: cerca de cinquenta casas destelhadas.\nTrinta e seis minutos depois, a mesma tempestade gera outro tornado, em Palmeira das Missões.",
  "Sábado, 7 de novembro, de madrugada. | Uma única supercélula cruza o noroeste gaúcho. | À 1h18, Santo Augusto: | cerca de 50 casas destelhadas. | 36 minutos depois, a mesma tempestade | gera outro tornado, em Palmeira das Missões.")
b("7 EM 6 DIAS", 2,
  "Sete tornados confirmados pelas Defesas Civis, em seis dias.\nTrês no Rio Grande do Sul, três em Santa Catarina, um no Paraná.\nNove municípios atingidos.",
  "7 tornados confirmados pelas Defesas Civis, em 6 dias. | 3 no Rio Grande do Sul, 3 em Santa Catarina, 1 no Paraná. | 9 municípios atingidos.")

# ---------------- É INÉDITO? ----------------
b("É INÉDITO?", 2,
  "Agora, a pergunta que todo mundo fez.\n[curious] Isso é inédito?\n[serious] A resposta curta é: não.",
  "Agora, a pergunta que todo mundo fez. | Isso é inédito? | A resposta curta é: não.")
b("É INÉDITO?", 2,
  "Em abril de dois mil e quinze, um tornado atravessou Xanxerê, a mesma cidade de agora, e atingiu mais de duas mil casas.\nEm dois mil e nove, Guaraciaba, no extremo oeste catarinense, teve um tornado éfe três, com quatro mortos.",
  "Em abril de 2015, um tornado atravessou Xanxerê, | a mesma cidade de agora, | e atingiu mais de 2 mil casas. | Em 2009, Guaraciaba, no extremo oeste catarinense, | teve um tornado F3, com 4 mortos.")
b("É INÉDITO?", 2,
  "E há exatamente um ano, em sete de novembro de dois mil e vinte e cinco, Rio Bonito do Iguaçu, no Paraná, foi atingida por um éfe quatro.\nUm rastro de setenta e cinco quilômetros, com até três quilômetros de largura.\nNoventa por cento da área urbana atingida. Sete mortes no estado.",
  "E há exatamente 1 ano, em 7 de novembro de 2025, | Rio Bonito do Iguaçu, no Paraná, | foi atingida por um F4. | Um rastro de 75 km, com até 3 km de largura. | 90% da área urbana atingida. | 7 mortes no estado.")
b("É INÉDITO?", 2,
  "Os números também sobem.\nEm dois mil e vinte e cinco, o Brasil registrou noventa e dois tornados, um recorde.\nAté julho deste ano, já eram oitenta e um.",
  "Os números também sobem. | Em 2025, o Brasil registrou 92 tornados, um recorde. | Até julho deste ano, já eram 81.")
b("É INÉDITO?", 2,
  "Mas atenção: mais registros não significam, necessariamente, mais tornados.\nHoje todo mundo tem uma câmera no bolso, e desde dois mil e dezoito uma plataforma reúne cada relato.\nUm estudo de dois mil e onze mostrou que os relatos de tornado no Brasil se multiplicaram por dez em trinta anos, e boa parte disso é a gente vendo mais.\nEntre os especialistas, não há consenso.",
  "Mas atenção: mais registros não significam, | necessariamente, mais tornados. | Hoje todo mundo tem uma câmera no bolso, | e desde 2018 uma plataforma reúne cada relato. | Um estudo de 2011 mostrou que os relatos de tornado no Brasil | se multiplicaram por 10 em 30 anos, | e boa parte disso é a gente vendo mais. | Entre os especialistas, não há consenso.")
b("É INÉDITO?", 2,
  "O que não muda é o mapa.\nA faixa entre o norte da Argentina, o Paraguai, o Uruguai e o Sul do Brasil é considerada por pesquisadores a segunda região mais propícia a tornados do mundo, depois dos Estados Unidos.\nE satélites da NASA mostraram que as tempestades daqui estão entre as mais intensas da Terra.",
  "O que não muda é o mapa. | A faixa entre o norte da Argentina, o Paraguai, o Uruguai e o Sul do Brasil | é considerada por pesquisadores | a 2ª região mais propícia a tornados do mundo, | depois dos Estados Unidos. | E satélites da NASA mostraram que as tempestades daqui | estão entre as mais intensas da Terra.")

# ---------------- PERGUNTA 1: POR QUE ----------------
b("PERGUNTA 1/3 · POR QUÊ", 2,
  "[curious] Então, por que isso acontece justamente aqui?",
  "Então, por que isso acontece justamente aqui?")
b("PERGUNTA 1/3 · POR QUÊ", 2,
  "Comece pela Amazônia.\nA floresta joga uma quantidade enorme de umidade no ar.\nA uns mil e quinhentos metros de altitude, um vento forte, o jato de baixos níveis, carrega esse ar quente e úmido para o sul.",
  "Comece pela Amazônia. | A floresta joga uma quantidade enorme de umidade no ar. | A uns 1.500 m de altitude, um vento forte, | o jato de baixos níveis, | carrega esse ar quente e úmido para o sul.")
b("PERGUNTA 1/3 · POR QUÊ", 2,
  "No caminho, existe uma parede: a Cordilheira dos Andes.\nEla barra o ar e o canaliza, colado à encosta, direto para o Paraguai, o norte da Argentina e o Sul do Brasil.\nÉ como um rio invisível de umidade.",
  "No caminho, existe uma parede: | a Cordilheira dos Andes. | Ela barra o ar e o canaliza, colado à encosta, | direto para o Paraguai, o norte da Argentina e o Sul do Brasil. | É como um rio invisível de umidade.")
b("PERGUNTA 1/3 · POR QUÊ", 2,
  "Do outro lado, chegam as frentes frias, vindas da Argentina.\nQuando o ar frio encontra esse ar quente e úmido, o ar quente é empurrado para cima.\nÉ o gatilho.",
  "Do outro lado, chegam as frentes frias, | vindas da Argentina. | Quando o ar frio encontra esse ar quente e úmido, | o ar quente é empurrado para cima. | É o gatilho.")
b("PERGUNTA 1/3 · POR QUÊ", 2,
  "Uma tempestade comum sobe e chove.\nMas aqui tem um ingrediente a mais: o vento muda de direção e de força com a altura.\nPerto do chão, sopra de um lado. Lá em cima, mais forte, de outro.\nE o ar entre as camadas começa a rolar, deitado, como um rolo de massa.",
  "Uma tempestade comum sobe e chove. | Mas aqui tem um ingrediente a mais: | o vento muda de direção e de força com a altura. | Perto do chão, sopra de um lado. | Lá em cima, mais forte, de outro. | E o ar entre as camadas começa a rolar, | deitado, como um rolo de massa.")
b("PERGUNTA 1/3 · POR QUÊ", 2,
  "A corrente que sobe dentro da nuvem levanta esse rolo e o põe em pé.\nAgora, a tempestade inteira gira. É a supercélula.\nEsse giro, com alguns quilômetros de largura, se chama mesociclone, e aparece no radar.",
  "A corrente que sobe dentro da nuvem | levanta esse rolo e o põe em pé. | Agora, a tempestade inteira gira. | É a supercélula. | Esse giro, com alguns km de largura, | se chama mesociclone, e aparece no radar.")
b("PERGUNTA 1/3 · POR QUÊ", 2,
  "Na traseira, uma descida de ar frio se enrola em volta do giro.\nEm parte dos casos, ele se estreita, acelera e toca o chão.\nÉ o tornado.",
  "Na traseira, uma descida de ar frio | se enrola em volta do giro. | Em parte dos casos, ele se estreita, | acelera e toca o chão. | É o tornado.")
b("PERGUNTA 1/3 · POR QUÊ", 2,
  "[intrigued] E aqui vai uma coisa que pouca gente sabe: a maioria das supercélulas não gera tornado.\nE por que algumas geram e outras não, o próprio laboratório de tempestades do governo americano admite: a ciência ainda não entende totalmente.",
  "E aqui vai uma coisa que pouca gente sabe: | a maioria das supercélulas não gera tornado. | E por que algumas geram e outras não, | o próprio laboratório de tempestades do governo americano admite: | a ciência ainda não entende totalmente.")
b("PERGUNTA 1/3 · POR QUÊ", 2,
  "Umidade da Amazônia, a parede dos Andes, frentes frias e vento que muda com a altura.\nPoucos lugares do planeta juntam esses quatro ingredientes como o Sul do Brasil.",
  "Umidade da Amazônia, a parede dos Andes, | frentes frias e vento que muda com a altura. | Poucos lugares do planeta juntam esses 4 ingredientes | como o Sul do Brasil.")

# ---------------- EL NIÑO ----------------
b("EL NIÑO", 2,
  "[serious] E este ano tem um agravante.\nO Pacífico equatorial está mais de dois graus acima do normal.\nÉ um El Niño muito forte, e ainda se fortalecendo.\nA agência americana de oceanos e atmosfera dá oitenta e três por cento de chance de ele se tornar o mais forte desde mil novecentos e cinquenta, quando as medições começaram.",
  "E este ano tem um agravante. | O Pacífico equatorial está mais de 2 °C acima do normal. | É um El Niño muito forte, e ainda se fortalecendo. | A NOAA dá 83% de chance de ele se tornar | o mais forte desde 1950, | quando as medições começaram.")
b("EL NIÑO", 2,
  "O El Niño deixa o jato de baixos níveis mais frequente e mais forte.\nMais umidade chegando ao Sul. Mais chuva. Mais dias com os ingredientes juntos.",
  "O El Niño deixa o jato de baixos níveis | mais frequente e mais forte. | Mais umidade chegando ao Sul. | Mais chuva. | Mais dias com os ingredientes juntos.")
b("EL NIÑO", 2,
  "[serious] Mas cuidado com o que a ciência não diz.\nO El Niño não causa cada tornado, e não há estudo que ligue o El Niño, sozinho, ao número de tornados. Ele aumenta as chances.\n[curious] E o aquecimento global?\n[serious] Ele deixa a atmosfera mais quente e úmida, o que alimenta tempestades. Mas, para tornados, o painel do clima da ONU diz que os registros ainda são curtos demais para afirmar uma tendência.",
  "Mas cuidado com o que a ciência não diz. | O El Niño não causa cada tornado, | e não há estudo que ligue o El Niño, sozinho, ao número de tornados. | Ele aumenta as chances. | E o aquecimento global? | Ele deixa a atmosfera mais quente e úmida, | o que alimenta tempestades. | Mas, para tornados, o IPCC diz que os registros | ainda são curtos demais para afirmar uma tendência.")

# ---------------- PERGUNTA 2: RISCO ----------------
b("PERGUNTA 2/3 · RISCO", 2,
  "[curious] E a pergunta que todo mundo no Sul está fazendo: isso vai voltar a acontecer?\n[serious] Alto. E não é exagero.",
  "E a pergunta que todo mundo no Sul está fazendo: | isso vai voltar a acontecer? | Alto. | E não é exagero.")
b("PERGUNTA 2/3 · RISCO", 2,
  "O pico do El Niño está previsto para a virada do ano, entre dezembro e janeiro.\nA previsão para novembro, dezembro e janeiro é de chuva acima da média no Sul, com destaque para o oeste catarinense.\nE os solos já estão encharcados.",
  "O pico do El Niño está previsto para a virada do ano, | entre dezembro e janeiro. | A previsão para novembro, dezembro e janeiro | é de chuva acima da média no Sul, | com destaque para o oeste catarinense. | E os solos já estão encharcados.")
b("PERGUNTA 2/3 · RISCO", 2,
  "A temporada mais ativa de tornados vai do fim do inverno à primavera. Ou seja: estamos no meio dela.\nE a Méti Sul alerta para eventos extremos também no verão.",
  "A temporada mais ativa de tornados | vai do fim do inverno à primavera. | Ou seja: estamos no meio dela. | E a MetSul alerta para eventos extremos | também no verão.")
b("PERGUNTA 2/3 · RISCO", 2,
  "No mapa, as regiões mais expostas formam um arco: o norte e o noroeste gaúcho, o oeste de Santa Catarina e o sudoeste do Paraná.\nMas este ano mostrou que o risco não para aí: o norte do Paraná e os Campos Gerais também tiveram tornados.",
  "No mapa, as regiões mais expostas formam um arco: | o norte e o noroeste gaúcho, | o oeste de Santa Catarina | e o sudoeste do Paraná. | Mas este ano mostrou que o risco não para aí: | o norte do Paraná e os Campos Gerais também tiveram tornados.")
b("PERGUNTA 2/3 · RISCO", 2,
  "Ninguém consegue prever onde cai o próximo tornado.\nMas dá para prever os dias de risco, com um ou dois dias de antecedência.\nJá o alerta do tornado em si chega com minutos.",
  "Ninguém consegue prever onde cai o próximo tornado. | Mas dá para prever os dias de risco, | com 1 ou 2 dias de antecedência. | Já o alerta do tornado em si | chega com minutos.")

# ---------------- PERGUNTA 3: ATÉ ONDE ----------------
b("PERGUNTA 3/3 · ATÉ ONDE", 2,
  "[curious] Agora, a pergunta mais difícil: até onde isso pode chegar?",
  "Agora, a pergunta mais difícil: | até onde isso pode chegar?")
b("PERGUNTA 3/3 · ATÉ ONDE", 2,
  "Tornados são classificados pelo estrago, numa escala de zero a cinco.\nO Brasil usa a escala Fujita original.\nMaringá foi um éfe dois: até duzentos e cinquenta e três quilômetros por hora.\nUm éfe quatro, como o de Rio Bonito do Iguaçu, passa dos trezentos e trinta. Um éfe cinco, dos quatrocentos e vinte.",
  "Tornados são classificados pelo estrago, | numa escala de 0 a 5. | O Brasil usa a escala Fujita original. | Maringá foi um F2: até 253 km/h. | Um F4, como o de Rio Bonito do Iguaçu, | passa dos 330. | Um F5, dos 420.")
b("PERGUNTA 3/3 · ATÉ ONDE", 2,
  "[serious] O Brasil nunca teve um éfe cinco confirmado.\nMas a região já teve: San Justo, na Argentina, em mil novecentos e setenta e três, a uns trezentos quilômetros da fronteira gaúcha.\nSessenta e três mortos.",
  "O Brasil nunca teve um F5 confirmado. | Mas a região já teve: | San Justo, na Argentina, em 1973, | a uns 300 km da fronteira gaúcha. | 63 mortos.")
b("PERGUNTA 3/3 · ATÉ ONDE", 2,
  "Nos Estados Unidos, são cerca de mil e duzentos tornados por ano.\nO mais largo já medido, em El Reno, tinha quatro quilômetros e duzentos metros de largura.\nO de Rio Bonito do Iguaçu chegou a três quilômetros e duzentos.",
  "Nos Estados Unidos, são cerca de 1.200 tornados por ano. | O mais largo já medido, em El Reno, | tinha 4,2 km de largura. | O de Rio Bonito do Iguaçu chegou a 3,2 km.")
b("PERGUNTA 3/3 · ATÉ ONDE", 2,
  "[serious] O pior cenário não é um tornado maior.\nÉ um tornado forte sobre uma cidade grande. Um éfe três, ou éfe quatro, cruzando uma Chapecó, uma Maringá.\nA região tem os ingredientes para isso.\nPor isso, o que mais importa é saber o que fazer.",
  "O pior cenário não é um tornado maior. | É um tornado forte sobre uma cidade grande. | Um F3, ou F4, cruzando uma Chapecó, uma Maringá. | A região tem os ingredientes para isso. | Por isso, o que mais importa | é saber o que fazer.")

# ---------------- O QUE FAZER ----------------
b("O QUE FAZER", 2,
  "Primeiro: receba os alertas no celular.\nMande o seu cép por SMS para quatro, zero, um, nove, nove. É de graça.\nE, no Sul, o Defesa Civil Alerta aparece direto na tela do celular, com som, sem cadastro.",
  "Primeiro: receba os alertas no celular. | Mande o seu CEP por SMS para 40199. | É de graça. | E, no Sul, o Defesa Civil Alerta | aparece direto na tela do celular, | com som, sem cadastro.")
b("O QUE FAZER", 2,
  "Segundo: conheça os sinais.\nUma nuvem baixa e escura girando. Uma nuvem em forma de funil. Granizo grande. Um ronco contínuo, como um trem chegando.",
  "Segundo: conheça os sinais. | Uma nuvem baixa e escura girando. | Uma nuvem em forma de funil. | Granizo grande. | Um ronco contínuo, como um trem chegando.")
b("O QUE FAZER", 2,
  "Terceiro: se o alerta tocar, vá para um cômodo pequeno no andar mais baixo, sem janelas, como um banheiro, e proteja a cabeça.\nLonge de vidro, de galpões e de árvores.\nAo ar livre, deite numa vala.\nE nunca se abrigue embaixo de um viaduto.",
  "Terceiro: se o alerta tocar, | vá para um cômodo pequeno no andar mais baixo, | sem janelas, como um banheiro, | e proteja a cabeça. | Longe de vidro, de galpões e de árvores. | Ao ar livre, deite numa vala. | E nunca se abrigue embaixo de um viaduto.")
b("A RESPOSTA", 2,
  "[curious] Então, o que está acontecendo no Sul?\n[serious] Não é um mistério, nem um castigo.\nÉ o encontro da Amazônia com os Andes e com o frio do sul, num dos cantos mais tempestuosos do planeta, turbinado este ano por um El Niño muito forte.\nOs tornados sempre estiveram aqui. Agora, estamos vendo cada um deles.",
  "Então, o que está acontecendo no Sul? | Não é um mistério, nem um castigo. | É o encontro da Amazônia com os Andes e com o frio do sul, | num dos cantos mais tempestuosos do planeta, | turbinado este ano por um El Niño muito forte. | Os tornados sempre estiveram aqui. | Agora, estamos vendo cada um deles.")
b("A RESPOSTA", 2,
  "Manda este vídeo para quem mora no Sul.\nE se inscreve: a temporada ainda não acabou.",
  "Manda este vídeo para quem mora no Sul. | E se inscreve: a temporada ainda não acabou.")

if __name__ == "__main__":
    json.dump(B, open(Path(__file__).parent / "blocos.json", "w"), ensure_ascii=False, indent=1)
    import re
    n = sum(len(re.findall(r"\w+", x["fala"])) for x in B)
    print(len(B), "blocos;", n, "palavras faladas")
