# Roteiro do longo 05 (Em Relevo, enchente de maio/2024: por que a chuva da serra alagou Porto Alegre). Fonte única do texto -> shared/blocos.json.
# Base: EMBALAGEM.md + CRIVO.md (aprovado r2, 15/11/2026) e pesquisa/FATOS.md (F1..F53). Mesmo formato do longo-02/03/04:
# id, cap (aba), marcha (1 = hook mais rápido), fala (limpa), fala_tts (tags v3, números por extenso),
# tela (algarismos; "|" separa os cartões da legenda). "fonte" = item de pesquisa/FATOS.md que sustenta o bloco.
# Promessa (EMBALAGEM): ver no mapa por que a chuva da serra pôs Porto Alegre debaixo d'água. Frase-âncora no b02 (< 0:30).
# Fio condutor: seguir o caminho da água, da serra até o centro de Porto Alegre (chuva -> lago/funil -> saída -> cidade).
# Sem a moldura "Isso nos leva às seguintes perguntas" (gap 5); sem anunciar próximo vídeo; "quase um terço"/"30%" (crivo r2).
import json, re
from pathlib import Path

B = []
TAG = re.compile(r"\[[a-z ]+\]\s*")
def b(cap, fala, tela, fonte=""):
    fala = fala.strip()
    B.append({"id": f"b{len(B)+1:02d}", "cap": cap, "marcha": 1 if len(B) < 6 else 2, "fala": TAG.sub("", fala), "fala_tts": fala,
              "tela": tela.strip(), "fonte": fonte})

C1 = "1 · A CHUVA DA SERRA"
C2 = "2 · O LAGO QUE RECEBE TUDO"
C3 = "3 · A SAÍDA"
C4 = "4 · O QUE CEDEU"

# ---------------- HOOK (paga a promessa até ~0:30) ----------------
b("CAXIAS DO SUL (RS) · 2 DE MAIO DE 2024",
  "[serious] Caxias do Sul, na serra gaúcha. Dois de maio de dois mil e vinte e quatro.\nEm um só dia, caíram ali duzentos e sessenta e seis milímetros de chuva.\nQuase três vezes o recorde anterior.",
  "Caxias do Sul, na serra gaúcha. 2 de maio de 2024. | Em um só dia, caíram ali 266 milímetros de chuva. | Quase 3 vezes o recorde anterior.",
  "F24")
b("PORTO ALEGRE (RS) · 5 DE MAIO DE 2024",
  "Três dias depois, a cem quilômetros dali, o Guaíba chegou a cinco metros e trinta e cinco centímetros em Porto Alegre.\nMais alto que na cheia de mil novecentos e quarenta e um.\n[serious] A chuva mais pesada caiu na serra. Quem afundou foi Porto Alegre.",
  "Três dias depois, a 100 quilômetros dali, | o Guaíba chegou a 5,35 metros em Porto Alegre. | Mais alto que na cheia de 1941. | A chuva mais pesada caiu na serra. | Quem afundou foi Porto Alegre.",
  "F1, F7, F22, F31")
b("PORTO ALEGRE (RS) · MAIO DE 2024",
  "Cerca de cento e sessenta mil pessoas foram atingidas só na capital, segundo a prefeitura.\nA rodoviária e o aeroporto ficaram debaixo d'água.\nNo estado inteiro, a Defesa Civil contou cento e oitenta e quatro mortos.",
  "Cerca de 160 mil pessoas atingidas só na capital, segundo a prefeitura. | A rodoviária e o aeroporto ficaram debaixo d'água. | No estado inteiro, a Defesa Civil contou 184 mortos.",
  "F44, F47, F49, F50 (números de 41 e 171 dias ficam para a legenda/descrição)")
b("O MAPA",
  "[curious] A capital também teve chuva recorde naquele mês.\nMas ela é pouca perto da água que desceu até a cidade.\nEntão, como a chuva da serra foi parar dentro de Porto Alegre?\nA resposta está no mapa.",
  "A capital também teve chuva recorde naquele mês. | Mas ela é pouca perto da água que desceu até a cidade. | Então, como a chuva da serra foi parar dentro de Porto Alegre? | A resposta está no mapa.",
  "F25, F19")
b("O MAPA",
  "Olhe de cima.\nDa serra, do planalto e do centro do estado vêm os rios: o Jacuí, o Taquari, o Caí, o Sinos e, perto da capital, o Gravataí.\nTodos terminam no mesmo lugar: no Guaíba, bem na frente de Porto Alegre.",
  "Olhe de cima. | Da serra, do planalto e do centro do estado vêm os rios: | o Jacuí, o Taquari, o Caí, o Sinos e, perto da capital, o Gravataí. | Todos terminam no mesmo lugar: | no Guaíba, bem na frente de Porto Alegre.",
  "F16")
b("O MAPA",
  "Oficialmente, o Guaíba é um lago. Muita gente ainda diz rio, e a ciência admite que ele tem um pouco dos dois.\n[intrigued] Esse lago recebe a água de quase um terço do Rio Grande do Sul. E só tem uma saída.\n[serious] Para entender maio de dois mil e vinte e quatro, vamos seguir o caminho dessa água, da serra até o centro da cidade.",
  "Oficialmente, o Guaíba é um lago. | Muita gente ainda diz rio, e a ciência admite que ele tem um pouco dos dois. | Esse lago recebe a água de quase 1/3 do Rio Grande do Sul. | E só tem uma saída. | Para entender maio de 2024, vamos seguir o caminho dessa água, | da serra até o centro da cidade.",
  "F18, F15")

# ---------------- 1. A CHUVA DA SERRA ----------------
b(C1,
  "Comece pelo céu.\nNo fim de abril, uma frente fria parou sobre o Rio Grande do Sul e não seguiu viagem.\nSegundo os meteorologistas, um bloqueio de ar quente ao norte segurou o sistema no lugar, enquanto a umidade vinda do norte alimentava as nuvens.",
  "Comece pelo céu. | No fim de abril, uma frente fria parou sobre o Rio Grande do Sul | e não seguiu viagem. | Segundo os meteorologistas, um bloqueio de ar quente ao norte | segurou o sistema no lugar, | enquanto a umidade vinda do norte alimentava as nuvens.",
  "F53 (descrição geral, sem número)")
b(C1,
  "Entre vinte e quatro de abril e quatro de maio, choveu em média mais de quatrocentos e vinte milímetros no estado.\nO número é do World Weather Attribution, um grupo de cientistas que estuda eventos extremos.\nÉ como se uns três meses de chuva caíssem em onze dias.",
  "Entre 24 de abril e 4 de maio, | choveu em média mais de 420 milímetros no estado. | O número é do World Weather Attribution, | um grupo de cientistas que estuda eventos extremos. | É como se uns 3 meses de chuva caíssem em 11 dias.",
  "F23")
b(C1,
  "E a chuva foi mais forte justamente onde nascem os rios: na serra e no planalto.\nCaxias do Sul somou setecentos e sete milímetros em treze dias.\nSanta Maria, no centro do estado, teve, num único dia, a maior chuva já registrada ali em cento e doze anos.",
  "E a chuva foi mais forte justamente onde nascem os rios: | na serra e no planalto. | Caxias do Sul somou 707 milímetros em 13 dias. | Santa Maria, no centro do estado, | teve, num único dia, a maior chuva já registrada ali em 112 anos.",
  "F24")
b(C1,
  "E não era a primeira cheia grande.\nEm setembro de dois mil e vinte e três, o Taquari já tinha passado do recorde de mil novecentos e quarenta e um.\nEm novembro, o Guaíba passou dos três metros de novo.\n[serious] Maio de dois mil e vinte e quatro foi a terceira grande cheia em oito meses.",
  "E não era a primeira cheia grande. | Em setembro de 2023, o Taquari já tinha passado do recorde de 1941. | Em novembro, o Guaíba passou dos 3 metros de novo. | Maio de 2024 foi a terceira grande cheia em 8 meses.",
  "F11, F12, F13, F14")
b(C1,
  "Agora, olhe o relevo.\nA serra gaúcha, onde fica Caxias do Sul, está a uns oitocentos metros de altitude. Porto Alegre, quase no nível do mar.\nToda a chuva que cai lá em cima tem de descer. E desce por vales estreitos e fundos.",
  "Agora, olhe o relevo. | A serra gaúcha, onde fica Caxias do Sul, está a uns 800 metros de altitude. | Porto Alegre, quase no nível do mar. | Toda a chuva que cai lá em cima tem de descer. | E desce por vales estreitos e fundos.",
  "geografia (relevo ETOPO/SRTM; Caxias ~760–800 m)")
b(C1,
  "O vale do Taquari é um desses.\nNa quinta-feira, dois de maio, o rio chegou a cerca de trinta e três metros e setenta em Lajeado.\nMais de três metros acima da marca de mil novecentos e quarenta e um.\nCidades inteiras do vale ficaram debaixo d'água.",
  "O vale do Taquari é um desses. | Na quinta-feira, 2 de maio, | o rio chegou a cerca de 33,7 metros em Lajeado. | Mais de 3 metros acima da marca de 1941. | Cidades inteiras do vale ficaram debaixo d'água.",
  "F27, F28")
b(C1,
  "Mas aquela água não ia parar ali.\nO Taquari deságua no Jacuí. E o Jacuí corre para o leste, direto para Porto Alegre.",
  "Mas aquela água não ia parar ali. | O Taquari deságua no Jacuí. | E o Jacuí corre para o leste, direto para Porto Alegre.",
  "F16, F19")

# ---------------- 2. O LAGO QUE RECEBE TUDO (paga o T2 até ~4:00) ----------------
b(C2,
  "Agora, suba a câmera e olhe o mapa inteiro.\nA chuva que cai em mais de duzentos e cinquenta municípios escorre para o mesmo lugar.\nUma bacia de cerca de oitenta e cinco mil quilômetros quadrados. Uns trinta por cento do estado.",
  "Agora, suba a câmera e olhe o mapa inteiro. | A chuva que cai em mais de 250 municípios escorre para o mesmo lugar. | Uma bacia de cerca de 85 mil km². | Uns 30% do estado.",
  "F15, F16")
b(C2,
  "Os rios do planalto e do centro formam o Jacuí.\nO Taquari desce da serra e se junta a ele.\nMais perto da capital, chegam o Caí, o Sinos e o Gravataí.\nE todos desembocam no mesmo lago: o Guaíba.",
  "Os rios do planalto e do centro formam o Jacuí. | O Taquari desce da serra e se junta a ele. | Mais perto da capital, chegam o Caí, o Sinos e o Gravataí. | E todos desembocam no mesmo lago: o Guaíba.",
  "F16")
b(C2,
  "[curious] E o Guaíba é diferente do que parece.\nTem uns quinhentos quilômetros quadrados, mas só uns poucos metros de fundura.\nÉ largo e raso. Quando entra muita água, ela não tem para onde descer. Ela sobe e se espalha.",
  "E o Guaíba é diferente do que parece. | Tem uns 500 km², | mas só uns poucos metros de fundura. | É largo e raso. | Quando entra muita água, ela não tem para onde descer. | Ela sobe e se espalha.",
  "F17")
b(C2,
  "Quase toda a água que chega a ele vem do Jacuí e do Taquari.\nEm média, o Guaíba despeja uns mil e duzentos metros cúbicos por segundo, segundo o DMAE, o departamento de água da capital.\nEm maio, segundo os pesquisadores, os rios passaram muito das maiores vazões já medidas.",
  "Quase toda a água que chega a ele vem do Jacuí e do Taquari. | Em média, o Guaíba despeja uns 1.200 m³ por segundo, | segundo o DMAE, o departamento de água da capital. | Em maio, segundo os pesquisadores, | os rios passaram muito das maiores vazões já medidas.",
  "F19, F20")
b(C2,
  "E o tempo da água importa.\nO Taquari e o Caí chegaram ao máximo na quinta. O Sinos, no sábado. O Jacuí, no domingo.\nAs cheias dos rios foram se somando em frente à cidade.\nE o Guaíba chegou ao pico no domingo, cinco de maio, de madrugada.",
  "E o tempo da água importa. | O Taquari e o Caí chegaram ao máximo na quinta. | O Sinos, no sábado. O Jacuí, no domingo. | As cheias dos rios foram se somando em frente à cidade. | E o Guaíba chegou ao pico no domingo, 5 de maio, de madrugada.",
  "F30, F31, F1")
b(C2,
  "Por isso, Porto Alegre não precisava da pior chuva em cima dela para afundar.\nBastava a chuva forte lá em cima, na serra e no centro do estado.\n[serious] O lago na frente da cidade recebe tudo.",
  "Por isso, Porto Alegre não precisava da pior chuva em cima dela para afundar. | Bastava a chuva forte lá em cima, na serra e no centro do estado. | O lago na frente da cidade recebe tudo.",
  "síntese de F15–F31")

# ---------------- 3. A SAÍDA ----------------
b(C3,
  "[curious] Se entra tanta água, por que ela não vai logo embora?\nO Guaíba só tem uma saída.\nAo sul, ele deságua na Lagoa dos Patos.",
  "Se entra tanta água, por que ela não vai logo embora? | O Guaíba só tem uma saída. | Ao sul, ele deságua na Lagoa dos Patos.",
  "F21")
b(C3,
  "Que, na verdade, é uma laguna: uns duzentos e cinquenta quilômetros de comprimento, ligada ao mar.\nE a ligação com o oceano fica lá no fim, em Rio Grande.\nUma passagem estreita, entre dois molhes de pedra.",
  "Que, na verdade, é uma laguna: | uns 250 quilômetros de comprimento, ligada ao mar. | E a ligação com o oceano fica lá no fim, em Rio Grande. | Uma passagem estreita, entre dois molhes de pedra.",
  "F21")
b(C3,
  "Ou seja: a água de quase um terço do estado precisa atravessar um lago raso,\ndescer duzentos e cinquenta quilômetros de laguna\ne passar por um gargalo para chegar ao mar.",
  "Ou seja: a água de quase 1/3 do estado | precisa atravessar um lago raso, | descer 250 quilômetros de laguna | e passar por um gargalo para chegar ao mar.",
  "F15, F21")
b(C3,
  "E ainda tem o vento.\nQuando ele sopra do sul, empurra a água da laguna de volta e segura o Guaíba.\nSegundo pesquisadores do Instituto de Pesquisas Hidráulicas da UFRGS, isso pode somar até uns cinquenta centímetros ao nível.",
  "E ainda tem o vento. | Quando ele sopra do sul, empurra a água da laguna de volta | e segura o Guaíba. | Segundo pesquisadores do Instituto de Pesquisas Hidráulicas da UFRGS, | isso pode somar até uns 50 centímetros ao nível.",
  "F32 (não afirmar que o vento causou o pico: F33)")
b(C3,
  "Em maio, a água desceu devagar.\nA Lagoa dos Patos só chegou ao pico em meados de maio, e causou alagamentos em Pelotas, São Lourenço do Sul e Rio Grande.\nEm Porto Alegre, o Guaíba ficou cerca de um mês acima da cota de inundação.",
  "Em maio, a água desceu devagar. | A Lagoa dos Patos só chegou ao pico em meados de maio, | e causou alagamentos em Pelotas, São Lourenço do Sul e Rio Grande. | Em Porto Alegre, o Guaíba ficou cerca de um mês | acima da cota de inundação.",
  "F35, F6")

# ---------------- 4. O QUE CEDEU ----------------
b(C4,
  "Agora, a última parte do caminho: a cidade.\nPorto Alegre sabia que isso podia acontecer.\nEm mil novecentos e quarenta e um, o Guaíba chegou a uns quatro metros e setenta e levou mais de um mês para voltar aos três metros.",
  "Agora, a última parte do caminho: a cidade. | Porto Alegre sabia que isso podia acontecer. | Em 1941, o Guaíba chegou a uns 4,7 metros | e levou mais de um mês para voltar aos 3 metros.",
  "F7, 1941 (FATOS §11)")
b(C4,
  "Depois disso, a cidade planejou uma defesa.\nO projeto é de mil novecentos e quarenta e três. As obras principais saíram nos anos setenta.\nO muro da Mauá, no centro. Sessenta e oito quilômetros de diques. Quatorze comportas. E vinte e três casas de bombas.",
  "Depois disso, a cidade planejou uma defesa. | O projeto é de 1943. As obras principais saíram nos anos 70. | O muro da Mauá, no centro. 68 km de diques. | 14 comportas. E 23 casas de bombas.",
  "F37, F38")
b(C4,
  "Funciona assim.\nO muro e os diques deixam o Guaíba do lado de fora.\nAs comportas são portões de aço nas passagens do muro, fechados na cheia.\nE as casas de bombas jogam para fora a chuva que cai do lado de dentro.\n[serious] Se uma peça falha, a água acha o caminho.",
  "Funciona assim. | O muro e os diques deixam o Guaíba do lado de fora. | As comportas são portões de aço nas passagens do muro, fechados na cheia. | E as casas de bombas jogam para fora a chuva que cai do lado de dentro. | Se uma peça falha, a água acha o caminho.",
  "F37 (descrição do sistema, DMAE)")
b(C4,
  "Em maio, várias falharam.\nNo dia três, uma comporta perto da avenida Sertório rompeu.\nA água entrou pela zona norte, em bairros como Navegantes.",
  "Em maio, várias falharam. | No dia 3, uma comporta perto da avenida Sertório rompeu. | A água entrou pela zona norte, em bairros como Navegantes.",
  "F40")
b(C4,
  "As casas de bombas dependem de energia. Com a cidade alagada, muitas ficaram sem luz ou foram inundadas.\nNo dia seguinte ao pico, dezenove das vinte e três estavam paradas, segundo dados da prefeitura.\nA chuva que devia ser bombeada para fora ficou dentro. E, por algumas delas, o próprio Guaíba entrou.",
  "As casas de bombas dependem de energia. | Com a cidade alagada, muitas ficaram sem luz ou foram inundadas. | No dia seguinte ao pico, 19 das 23 estavam paradas, segundo dados da prefeitura. | A chuva que devia ser bombeada para fora ficou dentro. | E, por algumas delas, o próprio Guaíba entrou.",
  "F41, F43")
b(C4,
  "No Sarandi, na zona norte, o dique rompeu, e a casa de bombas número dez foi inundada.\nO Sarandi foi o bairro com mais gente atingida: cerca de vinte e seis mil pessoas, segundo a prefeitura.",
  "No Sarandi, na zona norte, o dique rompeu, | e a casa de bombas número 10 foi inundada. | O Sarandi foi o bairro com mais gente atingida: | cerca de 26 mil pessoas, segundo a prefeitura.",
  "F42, F45")
b(C4,
  "E um detalhe importante: pelo que apontam os relatos técnicos, a água não passou por cima do muro da Mauá.\nEla entrou pelos pontos fracos do sistema.\nSegundo o estudo do World Weather Attribution, a defesa teria começado a falhar perto dos quatro metros e meio, apesar de ser apresentada como capaz de segurar seis.",
  "E um detalhe importante: pelo que apontam os relatos técnicos, a água não passou por cima do muro da Mauá. | Ela entrou pelos pontos fracos do sistema. | Segundo o estudo do World Weather Attribution, | a defesa teria começado a falhar perto dos 4,5 metros, | apesar de ser apresentada como capaz de segurar 6.",
  "F39, F43")
b(C4,
  "Por que falhou, ainda se discute.\nEx-diretores do DMAE apontam falta de manutenção. A prefeitura fala em problemas na concepção do sistema. Pesquisadores falam em falta de gestão.\nO fato é que a defesa feita depois de mil novecentos e quarenta e um não segurou essa cheia, que passou dos cinco metros.",
  "Por que falhou, ainda se discute. | Ex-diretores do DMAE apontam falta de manutenção. | A prefeitura fala em problemas na concepção do sistema. | Pesquisadores falam em falta de gestão. | O fato é que a defesa feita depois de 1941 | não segurou essa cheia, que passou dos 5 metros.",
  "F43")
b(C4,
  "E a água tomou a cidade.\nNo Mercado Público, chegou a um metro e meio.\nMenino Deus, Farrapos, Humaitá, as ilhas.\nSegundo a prefeitura, cerca de trinta por cento do território da capital ficou debaixo d'água.",
  "E a água tomou a cidade. | No Mercado Público, chegou a 1,5 metro. | Menino Deus, Farrapos, Humaitá, as ilhas. | Segundo a prefeitura, cerca de 30% do território da capital | ficou debaixo d'água.",
  "F48, F45, F44")

# ---------------- A RESPOSTA ----------------
b("A RESPOSTA",
  "[serious] Então, voltando à serra.\nPor que a chuva que caiu lá em cima alagou Porto Alegre?",
  "Então, voltando à serra. | Por que a chuva que caiu lá em cima alagou Porto Alegre?")
b("A RESPOSTA",
  "Porque, em onze dias, caiu uns três meses de chuva, e mais forte justamente onde nascem os rios.\nPorque a região já tinha passado por duas grandes cheias em oito meses.\nPorque a água de quase um terço do estado desce para o mesmo lago raso, em frente à capital, e as cheias chegaram quase juntas.",
  "Porque, em 11 dias, caiu uns 3 meses de chuva, | e mais forte justamente onde nascem os rios. | Porque a região já tinha passado por duas grandes cheias em 8 meses. | Porque a água de quase 1/3 do estado desce para o mesmo lago raso, | em frente à capital, e as cheias chegaram quase juntas.",
  "F23, F24, F11–F13, F15, F30")
b("A RESPOSTA",
  "Porque esse lago só se esvazia devagar, por uma laguna de duzentos e cinquenta quilômetros e uma saída estreita para o mar.\nE porque, segundo o estudo do World Weather Attribution, a defesa da cidade teria cedido nos pontos fracos antes do limite para o qual foi feita.",
  "Porque esse lago só se esvazia devagar, | por uma laguna de 250 quilômetros e uma saída estreita para o mar. | E porque, segundo o estudo do World Weather Attribution, | a defesa da cidade teria cedido nos pontos fracos | antes do limite para o qual foi feita.",
  "F21, F39, F43")
b("A RESPOSTA",
  "E o clima?\nO mesmo estudo do World Weather Attribution calculou que o aquecimento global mais que dobrou a chance de uma chuva assim, e a deixou de seis a nove por cento mais intensa.\nE que o El Niño daquele ano, sozinho, teve um peso parecido.",
  "E o clima? | O mesmo estudo do World Weather Attribution calculou | que o aquecimento global mais que dobrou a chance de uma chuva assim, | e a deixou de 6 a 9% mais intensa. | E que o El Niño daquele ano, sozinho, teve um peso parecido.",
  "F51, F52")
b("A RESPOSTA",
  "[serious] Isso não quer dizer que uma enchente igual vai voltar em data marcada. Ninguém consegue prever isso.\nMas a geografia não muda.\nA chuva da serra vai continuar descendo para o Guaíba. O que pode mudar é a defesa, e o aviso.",
  "Isso não quer dizer que uma enchente igual vai voltar em data marcada. | Ninguém consegue prever isso. | Mas a geografia não muda. | A chuva da serra vai continuar descendo para o Guaíba. | O que pode mudar é a defesa, e o aviso.",
  "fecho editorial (sem previsão)")
b("A RESPOSTA",
  "Depois de dois mil e vinte e quatro, a prefeitura fechou para sempre oito das catorze comportas do muro, trocadas por concreto, reformou as outras e reforçou o dique do Sarandi.\nE o aviso chega pelo celular: a Defesa Civil manda alerta por SMS.\nPara se cadastrar, basta mandar o seu CEP para o número quarenta mil cento e noventa e nove.",
  "Depois de 2024, a prefeitura fechou para sempre oito das 14 comportas do muro, trocadas por concreto, | reformou as outras e reforçou o dique do Sarandi. | E o aviso chega pelo celular: a Defesa Civil manda alerta por SMS. | Para se cadastrar, basta mandar o seu CEP para o número 40199.",
  "FATOS-bruto §2 (comportas concretadas, SBT/Observador do Tempo); SMS 40199 (Defesa Civil)")
b("A RESPOSTA",
  "Se você quer entender por que o Sul tem um clima tão diferente do resto do Brasil, o nosso vídeo sobre isso está aqui no canal.\nSe você tem família no Rio Grande do Sul, manda este vídeo para ela.\nE se inscreve no Em Relevo, para entender o clima do Brasil no mapa.",
  "Se você quer entender por que o Sul tem um clima tão diferente do resto do Brasil, | o nosso vídeo sobre isso está aqui no canal. | Se você tem família no Rio Grande do Sul, manda este vídeo para ela. | E se inscreve no Em Relevo, para entender o clima do Brasil no mapa.",
  "CTA: puxa sessão para bG6-E4qjXYc (clima do Sul, publicado); sem gancho de próximo vídeo")

if __name__ == "__main__":
    json.dump(B, open(Path(__file__).parent / "blocos.json", "w"), ensure_ascii=False, indent=1)
    n = sum(len(re.findall(r"\w+", x["fala"])) for x in B)
    ch = sum(len(" ".join(l.strip() for l in x["fala_tts"].split("\n"))) for x in B)
    print(len(B), "blocos;", n, "palavras faladas;", ch, "caracteres para o TTS")
    t = 0.4
    for x in B:
        w = len(re.findall(r"\w+", x["fala"]))
        print(f'{x["id"]} {int(t//60)}:{t%60:04.1f} {w:3d}p {x["cap"]}')
        t += w / 2.9 + 0.6
    print(f"total estimado {int(t//60)}:{t%60:04.1f}")
