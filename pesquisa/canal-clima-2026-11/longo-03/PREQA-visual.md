# Pré-QA visual automático

- Alvo: `pesquisa/canal-clima-2026-11/longo-03/preqa` · 120 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.335 · `tools/preqa_visual.py`
- Resultado: **REPROVADO (há bloqueante)** · bloqueante 18 · alto 27 · médio 44 · baixo 24
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:00 | Q01 `0.png` | medio | texto_encavalado | No rodapé, a linha de fontes ('FONTES: THEOPHILO · CENSO DE 1872…') fica colada sobre o terreno e quase ilegível. A linha de créditos do mapa ('MAPA: NASA BLUE MARBLE…') está logo abaixo, também pouco legível. O rótulo 'FORTALEZA · 1878' no topo esquerdo tem contraste fraco sobre o mar escuro. |
| 0:04 | Q02 `112.png` | medio | texto_encavalado | A legenda 'Uma cidade de uns 25' fica logo abaixo da moldura da planta, quase encostada na borda inferior. A faixa de fontes no rodapé também fica colada à legenda, deixando o rodapé apertado. |
| 0:12 | Q04 `346.png` | medio | anacronismo | A foto 'THEOPHILO VACINA · 1907' é de 1907, mas o quadro está no contexto de Fortalezas 1878 (selo 'FORTALEZA · 1878' no canto). É anacronismo de contexto, embora a legenda da imagem declare a data. Dúvida: pode ser intencional como ilustração de apoio. |
| 0:20 | Q06 `600.png` | medio | texto_encavalado | A legenda 'E num único dia,' fica colada embaixo do rótulo 'MORTOS DE VARÍOLA EM 1 DIA', quase encostando, e a caixa da legenda ainda está em animação. Apertado, mas legível. |
| 0:20 | Q07 `609.png` | alto | valor_errado | O contador animado mostra 876 aos 0:20, depois de mostrar 655 no quadro anterior no mesmo segundo. O valor final deveria ser 1.004 ou similar (o texto da narração fala '10 de…'); a contagem passa por valores intermediários, confirmar se o número final chega ao correto. Também há risco de o contador estar errado em relação ao rótulo 'MORTOS DE VARÍOLA EM 1 DIA'. |
| 0:30 | Q08 `900.png` | alto | texto_encavalado | Duas legendas/textos de digitação simultâneos: a faixa grande '5% D▌' (cartão branco inclinado) e a legenda menor 'Pelas contas▌' logo abaixo, mais o rótulo 'PELAS CONTAS MAIS ALTAS'. Três camadas de texto repetido disputando a atenção no terço inferior, com duplicação de conteúdo. |
| 0:30 | Q08 `900.png` | medio | elemento_fora | A faixa uniforme na borda esquerda (RGB 27,33,41) parece ser só o oceano escuro do mapa; mas o rótulo 'O IMPÉRIO · 1877' flutua sobre o mapa sem fundo, com legibilidade baixa sobre o relevo claro. |
| 0:37 | Q09 `1104.png` | medio | elemento_fora | A caixa de texto grande (barra branca com 'E' e cursor) está quase vazia e sobrepõe o mapa e a faixa 'QUASE NINGUÉM FALA DELA'. Provavelmente é animação de digitação, mas a legenda 'Mesmo as' aparece ao mesmo tempo, o que cria duplicidade confusa de texto na tela. |
| 1:06 | Q13 `1985.png` | alto | fundo/faixa | O quadro inteiro é um fundo bege/branco liso, sem mapa nem conteúdo, apesar do rótulo 'PERGUNTA 1/4'. Só há legenda e rodapé. Pode ser uma transição entre cenas, mas parece um mapa que não carregou ou uma cena vazia. Há também uma faixa clara na borda direita. |
| 1:17 | Q16 `2324.png` | medio | outro | A foto 'SANTA QUITÉRIA (CE) · AÇUDE SECO · 2018' ocupa quase todo o quadro e cobre o mapa. A faixa vermelha da legenda da foto fica colada na borda inferior. Dúvida entre estilo e defeito: a foto parece real, mas a vegetação verde destoa de um 'açude seco'. |
| 1:20 | Q17 `2387.png` | bloqueante | fundo/faixa | Listras verticais regulares cobrem quase todo o quadro, a partir de x≈130 até a borda direita, sobre o mapa desfocado. Parece artefato de render ou z-fighting, não transição intencional. |
| 1:30 | Q19 `2700.png` | medio | elemento_fora | O rótulo 'MÉDIA 1.450 MM' fica sobreposto às barras do gráfico, o que dificulta a leitura. Além disso, o '1850' do eixo está cortado na borda esquerda ('850'). |
| 1:40 | Q20 `3000.png` | bloqueante | fundo/faixa | Listras verticais claras sobre todo o fundo do mapa, atrás e ao redor do cartão do gráfico. |
| 1:40 | Q20 `3000.png` | alto | texto_encavalado | O rótulo vermelho '1877 · 468 MM' fica por cima das barras do gráfico e é cortado pela barra vertical vermelha. O '468' fica ilegível e o texto está distorcido/espremido. |
| 1:41 | Q21 `3027.png` | bloqueante | fundo/faixa | Listras verticais fortes sobre todo o fundo do mapa (x≈130 em diante). A cena está em transição, mas o padrão de listras é artefato. |
| 1:52 | Q24 `3369.png` | medio | anacronismo | A legenda diz 'Em 1872,' mas a placa do mapa diz 'REBOUÇAS · 1877'. Pode haver incoerência de datas; vale conferir. Há também texto histórico da imagem do mapa, que é documento real e talvez aceitável. |
| 2:14 | Q28 `4008.png` | medio | legenda | A legenda mostra só 'Forta' (palavra cortada). Provavelmente é animação de digitação, então não é defeito. Mas há um pequeno traço vermelho solto no meio do mapa (~x 217, y 348) que parece um elemento perdido. |
| 2:30 | Q30 `4485.png` | medio | texto_inventado | O mapa histórico (1878) no cartão tem texto em letra pequena e antiga (PARAHYBA, PERNAMBUCO, ALAGOAS etc.). É um mapa de arquivo e pode ser intencional, mas se tiver sido gerado por IA há risco de rótulos falsos. Confirmar a origem. O 'PERNAMBUCO' fica parcialmente coberto pelo relevo. |
| 2:36 | Q32 `4691.png` | alto | outro | O quadro inteiro é um fundo de pergaminho bege vazio, sem conteúdo. Só há um texto minúsculo e ilegível no centro (~y 335), a legenda 'E a' e os selos de fonte. Parece uma cena que não carregou (placeholder) ou uma imagem faltando. Se for transição de cena, confirmar. |
| 2:36 | Q32 `4691.png` | medio | texto_inventado | O texto minúsculo e ilegível no centro do pergaminho (~x 480, y 335) parece um título que não renderizou direito ou escrita falsa. Não dá para ler. |
| 2:37 | Q33 `4722.png` | medio | fundo/faixa | Fundo bege de papel com listras horizontais finas visíveis em todo o quadro; o sinal automático acusa faixa uniforme de 3% no topo (RGB 199,176,130). Pode ser textura de papel intencional, mas conferir se não é faixa/z-fighting. |
| 2:40 | Q34 `4800.png` | medio | fundo/faixa | Mesmo fundo bege com listras horizontais; sinal de faixa no topo. Conferir se é textura intencional. |
| 2:40 | Q34 `4800.png` | medio | elemento_fora | O título 'FORTALEZA · 1878 · MORTES POR MÊS' fica sozinho no meio do quadro, sem gráfico nem dado, e deixa uma tela quase vazia. Parece elemento ainda não carregado. |
| 2:44 | Q35 `4921.png` | medio | fundo/faixa | Fundo com listras horizontais e sinal de faixa no topo (RGB 199,176,130). |
| 2:44 | Q35 `4921.png` | medio | elemento_fora | Título no meio do quadro sem gráfico ou dado visível; o quadro fica vazio. |
| 2:45 | Q36 `4937.png` | medio | elemento_fora | Toda a área à direita da foto está vazia, com a composição desequilibrada. Parece que falta o gráfico de mortes por mês. |
| 2:54 | Q37 `5217.png` | medio | valor_errado | O contador mostra 980 enquanto a legenda ainda diz 'No dia 10 de dezembro,'. Pode ser animação em curso, mas o valor é anterior ao dado final. |
| 3:20 | Q41 `6000.png` | medio | valor_errado | A caixa mostra "1880" enquanto a legenda ainda diz "A chuva só voltou de verdade em" (digitação em andamento), e o termômetro de mortos já está preenchido de 150 a 500 mil. Pode ser animação, mas o valor já aparece antes da narração chegar nele. |
| 3:22 | Q42 `6075.png` | alto | elemento_fora | O círculo vermelho no centro não destaca nada (o mapa/fundo atrás sumiu), e a legenda "No Rio" fica colada na borda inferior do círculo. |
| 3:22 | Q42 `6075.png` | medio | fundo/faixa | Fundo de papel bege com linhas horizontais; o sinal automático acusa faixa uniforme no topo (RGB 199,176,130). Provavelmente é a textura intencional de pergaminho, mas fica a dúvida. O mapa sumiu, com um círculo vermelho vazio no centro. |
| 3:24 | Q43 `6106.png` | alto | elemento_fora | Quadro quase vazio: só fundo bege com linhas e a legenda "No Rio de Janeiro, a capital". Falta o conteúdo visual (mapa ou imagem), parece cena que não carregou. |
| 3:28 | Q44 `6238.png` | medio | elemento_fora | O título "RIO DE JANEIRO · 1878 · O BESOURO" está no meio do quadro sobre fundo bege vazio, sem imagem, em vez de no topo como em Q45. Sensação de cena vazia. |
| 3:28 | Q45 `6254.png` | alto | texto_inventado | A foto da esquerda (Ceará · retirante) tem moldura preta e dourada irregular e texto ilegível invertido/inventado nas laterais da imagem de IA. A legenda da polaroide está quase invisível, em bege claro sobre branco. |
| 3:29 | Q46 `6256.png` | medio | elemento_fora | Alterna com Q45: o título está no centro e as fotos sumiram, o que dá a impressão de piscada/falha de composição entre dois layouts. Fundo bege vazio. |
| 3:29 | Q47 `6272.png` | alto | texto_inventado | A foto da esquerda mantém moldura preta/dourada e texto falso e ilegível escrito pela IA nas laterais da imagem. |
| 3:30 | Q48 `6300.png` | medio | elemento_fora | O título no centro com fundo bege vazio, sem imagem, repete a alternância de layouts. A legenda está em digitação (aceitável). |
| 3:40 | Q49 `6600.png` | medio | fundo/faixa | Fundo bege com listras horizontais finas e manchas ovais. A faixa de topo RGB(207,190,158) sinalizada é só o fundo de papel, provavelmente estilo intencional. Pergunta 1/4 combina com 'O QUE ACONTECEU'. |
| 3:40 | Q49 `6600.png` | medio | texto_encavalado | O carimbo rosa 'PRIMEIRO FOTOJORNALISMO DO BRASIL?' sobrepõe a palavra 'BESOURO' da linha 'RIO DE JANEIRO · 1878 · O BESOURO', cortando a leitura. A legenda mostra 'Br' em animação de digitação (não é defeito). |
| 3:42 | Q51 `6671.png` | bloqueante | fundo/faixa | Atrás do globo 3D há uma faixa chapada azul-marinho no topo (cerca de 30% da altura) com corte reto contra o fundo cinza-escuro, formando uma emenda horizontal visível atrás do globo. |
| 3:50 | Q52 `6900.png` | alto | elemento_fora | O mapa de anomalia de temperatura do Pacífico aparece como uma placa 3D recortada, com bordas serrilhadas à esquerda e blocos de relevo saltando no canto superior direito, que cobrem a lista de perguntas. As bordas expostas e a emenda ficam visíveis sobre a base de satélite. |
| 4:00 | Q53 `7200.png` | alto | elemento_fora | No canto superior direito, bloco 3D vermelho serrilhado ('caixote') saindo da borda da placa de dados, junto à costa da América do Norte. É um artefato de geometria. As bordas da placa ficam expostas no topo. |
| 4:06 | Q54 `7383.png` | bloqueante | fundo/faixa | Listras verticais claras sobre todo o quadro, da esquerda para a direita, cobrindo mapa e barras. Parece defeito de render ou z-fighting, e não transição. Também há faixa azul chapada no topo, acima de ~y=85. |
| 4:06 | Q54 `7383.png` | medio | valor_errado | Os rótulos dos valores (2,53; 2,33; 2,40; 2,71) estão borrados atrás das listras, e uma caixa branca com 'N' aparece sobre a terceira barra. Parece legenda ou placeholder truncado. Pode ser animação em andamento. |
| 4:10 | Q55 `7500.png` | bloqueante | fundo/faixa | Faixa azul chapada no topo (até ~y=75) com corte reto contra o fundo cinza-escuro atrás do mapa 3D inclinado, uma emenda de fundo visível. |
| 4:10 | Q55 `7500.png` | medio | texto_encavalado | Rótulo 'O NOSSO VÍDEO ANTERIOR' no canto superior esquerdo está minúsculo e quase ilegível, com a linha de cima em vermelho ilegível. Está solto e desproporcional ao resto do layout. |
| 4:20 | Q56 `7800.png` | bloqueante | fundo/faixa | Faixa azul chapada no topo (até ~y=50) com corte reto e emenda contra o fundo escuro atrás do mapa 3D. |
| 4:21 | Q57 `7837.png` | bloqueante | fundo/faixa | Listras verticais regulares cobrem quase todo o quadro, da esquerda até a direita, sobre o mapa desfocado. Parece z-fighting ou artefato de render, e o mapa fica ilegível. |
| 4:40 | Q59 `8400.png` | alto | elemento_fora | A linha da faixa de nuvens (ZCIT) está colada no topo do quadro e passa por trás do rótulo 'PERGUNTA 2/4'. Fica deslocada em relação ao mapa e ao rótulo 'FAIXA DE NUVENS' que aparecia no Q58. Há também manchas circulares translúcidas e uma faixa cinza no topo. |
| 4:41 | Q60 `8439.png` | bloqueante | fundo/faixa | O quadro inteiro é um fundo branco/bege quase chapado, sem mapa, globo ou conteúdo. Só aparecem o rótulo e as fontes. Fora de uma transição clara, parece tela vazia com o mapa sumido. Sinal de faixa à direita (RGB 222,220,217). |
| 4:50 | Q61 `8700.png` | bloqueante | fundo/faixa | Atrás do globo há um fundo dividido em dois blocos chapados: azul royal no topo e azul quase preto embaixo, com uma linha horizontal dura em y≈145. Parece emenda de fundo, e uma sombra escura enorme aparece no canto inferior direito. |
| 4:50 | Q61 `8700.png` | alto | valor_errado | O título '9-13 MI · NORTE DA CHINA · MORTOS ESTIMADOS' fica sobre um globo centrado na África e no Oceano Índico, sem a China visível. A legenda fala da Índia (5,5 a 10 milhões). Dado e mapa não batem. O título grande também encosta no topo do quadro. |
| 5:00 | Q62 `9000.png` | bloqueante | fundo/faixa | Mesma emenda de fundo atrás do globo: bloco azul no topo, bloco azul-escuro chapado embaixo e linha horizontal dura em y≈135. Há também sombra escura no canto inferior direito. |
| 5:06 | Q63 `9173.png` | medio | outro | O mapa está muito desfocado e com grade de pixels/quadriculado visível, provavelmente textura de baixa resolução. Pode ser desfoque de transição intencional, mas a grade fica aparente. Sinal de faixa no topo. |
| 5:20 | Q65 `9600.png` | medio | texto_inventado | O rótulo vermelho sobre o mapa diz "O GRANDES AÇUDES", com um "O" sobrando ou erro de texto no início. A pergunta 2/4 não parece ter bug de dados, mas o rótulo deve ser revisado. |
| 5:25 | Q66 `9750.png` | medio | fundo/faixa | Fundo bege liso com listras horizontais finas (textura de papel) e sem mapa, por trás só da legenda "No go". O sinal automático de faixa no topo é só a textura/vinheta do papel, sendo provável que seja um cartão intencional. Se o papel não for estilo intencional, vale a dúvida: parece cena vazia. |
| 5:26 | Q67 `9782.png` | medio | fundo/faixa | Mesmo fundo bege com listras horizontais e nenhum elemento além da legenda, que está em digitação ("a resposta fo"). Provável cartão de papel intencional, mas a cena está vazia e vale confirmar. |
| 5:30 | Q68 `9900.png` | medio | fundo/faixa | Fundo bege listrado, vazio, só com a legenda "O chefe do governo, o senador Sinimbu, chegou a dizer:". Confirmar se o cartão de papel liso é intencional (cena de citação) e não uma imagem que falhou ao carregar. |
| 6:04 | Q75 `10924.png` | alto | fundo/faixa | Listras verticais claras sobre todo o mapa, com bordas desfocadas. Pode ser efeito de transição, mas parece z-fighting ou grade de faixas. Se não for intencional, é defeito de render. O mesmo padrão aparece em Q78. |
| 6:13 | Q78 `11187.png` | alto | fundo/faixa | Listras verticais regulares sobre o mapa desfocado, como em Q75. Se não forem uma transição intencional, é artefato de render. |
| 6:20 | Q79 `11400.png` | medio | elemento_fora | O rótulo 'AÇUDE DO CEDRO' tem um '1' cortado ou sobrando à direita da caixa, parecendo texto truncado. Além disso, o marcador vermelho está sobreposto ao disco azul e à haste, o que deixa a leitura confusa. |
| 6:26 | Q81 `11584.png` | medio | elemento_fora | Atrás das fotos, o marcador vermelho 3D do mapa e a placa 'AÇUDE DO CEDRO 1884 → 1906' aparecem parcialmente cobertos pelas fotos. Um '91' vaza ao lado da placa, no topo, e o marcador vermelho aparece cortado entre as duas fotos. |
| 6:30 | Q82 `11700.png` | alto | texto_encavalado | O número grande '22 ANOS' está por cima da placa 'AÇUDE DO CEDRO' no topo. Resta apenas o fragmento '91' ao lado, e o texto da placa fica ilegível, encavalado com o título. |
| 6:30 | Q82 `11700.png` | medio | elemento_fora | O marcador vermelho 3D está cortado pela borda superior. O diorama circular (disco azul) tem aspecto de placeholder, com um fio ou rio sobre ele, e a hastes pretas parecem soltas. |
| 6:34 | Q83 `11809.png` | alto | fundo/faixa | Fundo bege de pergaminho com listras horizontais finas (linhas de varredura) em todo o quadro, e uma faixa mais escura no topo (RGB 199,176,130). O quadro está praticamente vazio. |
| 6:34 | Q83 `11809.png` | alto | texto_cortado | A legenda 'E aqu' está incompleta e há um texto minúsculo ilegível no centro do quadro (~y=335). Se não for animação de digitação, é texto quebrado. |
| 6:35 | Q84 `11840.png` | medio | fundo/faixa | Fundo bege com listras horizontais visíveis e faixa uniforme na borda superior, sem imagem ou mapa. O título 'FRASE ATRIBUÍDA A DOM PEDRO II' fica sobre fundo liso, e a frase em si não aparece. |
| 6:48 | Q85 `12242.png` | medio | fundo/faixa | Quadro quase todo branco/creme, sem conteúdo além da legenda 'Mas a' (provavelmente em digitação). É um quadro vazio fora de transição, com faixas claras nas bordas. |
| 6:59 | Q87 `12569.png` | alto | outro | A foto histórica 'RIO ACRE · SERINGAL' está rotacionada 90° (de lado), então a cena fica irreconhecível. Além disso, a legenda diz c. 1910, em um contexto de 1877. |
| 7:00 | Q88 `12600.png` | alto | outro | A foto do seringal continua girada 90° (de lado). O contador '4.764' já aparece completo enquanto a legenda ainda diz 'quase 5', então valor e fala ficam descasados. |
| 7:30 | Q92 `13500.png` | medio | texto_encavalado | Os rótulos 'ACRE · BRASIL · 1903' e 'ACRE' se sobrepõem na região do Acre. A linha vermelha e a sombra cruzam o texto do rótulo, o que prejudica a leitura. |
| 7:50 | Q95 `14100.png` | bloqueante | texto_encavalado | O título '7 CAMPOS · +70 MIL' no topo está cortado pela borda superior e fica atrás/encavalado com a placa 'PERGUNTA 3/4'. O rótulo 'ALAGADIÇO · 1915' está coberto pela faixa '1932 · CERCADOS PARA NÃO CHEGAR A FORTALEZA' e pelos pinos, então fica ilegível. |
| 7:52 | Q96 `14170.png` | alto | texto_encavalado | Há uma caixa de legenda grande e vazia, com só um 'V' e o cursor, logo abaixo da faixa '1909 · INSPETORIA DE OBRAS CONTRA AS SECAS'. Ao mesmo tempo aparece outra legenda pequena 'Só e', fora de posição. São duas caixas de legenda simultâneas e uma está quase vazia. Se não for animação de digitação intencional, é defeito. |
| 8:19 | Q98 `14964.png` | alto | texto_encavalado | O cartão da checklist 'Por que quase ninguém fala' cobre a parte esquerda do cartão da linha do tempo (título 'ROTEIRO' e primeiros anos cortados, só '2', 1958, 1983, 2012 visíveis). Dois elementos de tela se sobrepõem e a leitura do roteiro fica prejudicada. |
| 8:20 | Q99 `15000.png` | bloqueante | tela_preta | O quadro inteiro é um fundo branco/bege chapado, sem mapa nem conteúdo. Só aparecem o rótulo, a legenda e as fontes. O mapa sumiu, o que parece falha de render ou fundo vazio fora de transição. Os sinais automáticos de faixas uniformes no topo e na direita confirmam. |
| 8:20 | Q100 `15011.png` | bloqueante | tela_preta | O fundo é bege/branco chapado, sem mapa nem imagem. Só aparecem o rótulo 'PERGUNTA 4/4', a legenda e as fontes. Faixas uniformes no topo e na direita. A legenda 'até o país se acostumar com ela.' ficou repetida do quadro anterior, mas o rótulo já mudou para a pergunta 4/4, então o fundo vazio persiste na troca de cena. |
| 8:21 | Q101 `15040.png` | bloqueante | fundo/faixa | Atrás do globo 3D há uma faixa azul-marinho chapada no topo (~30% do quadro) e um bloco cinza-escuro embaixo, com uma divisão horizontal dura em y≈165. O fundo tem duas cores e parece um chão/horizonte estranho. O globo flutua sobre essa emenda, e há uma sombra elíptica escura no canto inferior direito. |
| 8:30 | Q102 `15300.png` | bloqueante | fundo/faixa | A camada de anomalia de temperatura do Pacífico é um retângulo plano com bordas retas e emendas visíveis, que cobre o mapa. Há blocos 3D deformados e brancos no canto direito (costa oeste da América do Norte) e na esquerda (Austrália/Nova Guiné), com artefatos de extrusão e z-fighting. O relevo está quebrado e a faixa não se integra ao mapa. |
| 8:40 | Q103 `15600.png` | bloqueante | fundo/faixa | O mapa ocupa só a faixa superior e termina numa borda reta e inclinada. Abaixo há um bloco chapado azul-escuro vazio (mais da metade do quadro) onde estão as pirâmides 3D de dados. O mapa e a textura sumiram atrás das barras. |
| 8:40 | Q103 `15600.png` | medio | valor_errado | Os valores '2,53' e '3,06' sobre as pirâmides têm contorno escuro e baixo contraste sobre o fundo escuro, o que dificulta a leitura. As pirâmides estão cortadas pela borda inferior e não há rótulo dizendo o que cada uma representa. |
| 8:46 | Q104 `15776.png` | bloqueante | fundo/faixa | Listras verticais claras regulares cobrem o quadro inteiro, da borda esquerda à direita, sobre o mapa do Nordeste. Parece defeito de render, z-fighting ou grade de textura, e não uma transição intencional. |
| 9:30 | Q110 `17100.png` | alto | moldura | A imagem de satélite de Jati (CE) tem um bloco preto chapado no canto superior esquerdo, dentro da moldura (cunha de dados ausentes da cena). Parece borda sem imagem, não conteúdo. |
| 9:37 | Q111 `17305.png` | alto | elemento_fora | O cartão da linha do tempo 'SECAS DO NORDESTE' cobre o centro do mapa e esconde os pontos vermelhos das cisternas, deixando só a parte inferior visível. O rótulo 'TRANSPOSIÇÃO · 2020' fica colado na base do cartão e parece solto. |
| 9:37 | Q111 `17305.png` | medio | valor_errado | A linha do tempo mostra os marcos 1915, 1932 e 2012-17 sem destaque nem animação, e o espaçamento não é proporcional aos anos. Pode ser estado inicial da animação ou estilo; vale conferir. |
| 9:40 | Q112 `17400.png` | alto | elemento_fora | Mesmo problema de Q111: o cartão da linha do tempo cobre os pontos do mapa, e 'TRANSPOSIÇÃO · 2020' parece solto, colado na borda do cartão. |
| 9:43 | Q113 `17497.png` | alto | texto_encavalado | O cartão bege da linha do tempo 'SECAS DO NORDESTE' fica por cima da foto do carro-pipa e cobre boa parte do caminhão (cabine e rodas dianteiras). Os dois elementos competem e o enquadramento fica poluído. Pode ser composição intencional, então registro com dúvida. |
| 9:43 | Q113 `17497.png` | medio | valor_errado | Na linha do tempo, só 1877 está destacado; 1915, 1932 e 2012-17 aparecem sem marcação clara, e o título diz 'SÓ EM 1877 MORTES EM MASSA'. Pode ser animação em andamento, mas o ponto vermelho de 1877 fica deslocado do número. |
| 10:00 | Q115 `18000.png` | medio | fundo/faixa | O fundo é bege/branco liso, sem mapa, em um quadro de transição para 'A RESPOSTA'. O canto inferior direito escurece (RGB 216,214,210) e a faixa clara no topo é uniforme. Parece fundo intencional, mas o quadro está vazio e destoa do mapa 3D escuro dos demais. |
| 10:00 | Q116 `18006.png` | medio | fundo/faixa | Fundo bege liso e quase vazio, só com a legenda em digitação ('En'). O sinal automático de faixa uniforme na borda direita e no topo provavelmente vem do degradê do fundo. Dúvida entre estilo e defeito. |
| 10:30 | Q120 `18900.png` | alto | texto_encavalado | A caixa grande 'É O' (título 'O QUE TRANSFORMA SECA EM TRAGÉDIA') cobre o rótulo 'ACRE', que fica parcialmente escondido sob a caixa. A legenda 'Ma' aparece ao mesmo tempo, em outra posição, o que gera elementos de texto duplicados. |

24 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q01 (0:00): faixa uniforme na borda topo: 5% do quadro, cor RGB(17,26,38)
- Q05 (0:19): faixa uniforme na borda topo: 4% do quadro, cor RGB(199,176,130)
- Q06 (0:20): faixa uniforme na borda topo: 4% do quadro, cor RGB(199,176,130)
- Q07 (0:20): faixa uniforme na borda topo: 4% do quadro, cor RGB(199,176,130)
- Q08 (0:30): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(27,33,41)
- Q09 (0:37): faixa uniforme na borda topo: 5% do quadro, cor RGB(33,38,48)
- Q10 (0:40): faixa uniforme na borda topo: 4% do quadro, cor RGB(34,42,49)
- Q13 (1:06): faixa uniforme na borda topo: 4% do quadro, cor RGB(246,245,243)
- Q13 (1:06): faixa uniforme na borda direita: 12% do quadro, cor RGB(222,220,216)
- Q14 (1:07): faixa uniforme na borda topo: 5% do quadro, cor RGB(14,21,31)
- Q15 (1:10): faixa uniforme na borda topo: 4% do quadro, cor RGB(15,22,32)
- Q16 (1:17): faixa uniforme na borda topo: 5% do quadro, cor RGB(14,19,28)
- Q18 (1:20): faixa uniforme na borda topo: 4% do quadro, cor RGB(25,31,40)
- Q19 (1:30): faixa uniforme na borda topo: 4% do quadro, cor RGB(31,37,44)
- Q22 (1:45): faixa uniforme na borda topo: 5% do quadro, cor RGB(13,18,27)
- Q24 (1:52): faixa uniforme na borda topo: 5% do quadro, cor RGB(22,26,34)
- Q24 (1:52): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(46,40,35)
- Q28 (2:14): faixa uniforme na borda topo: 5% do quadro, cor RGB(29,39,56)
- Q30 (2:30): faixa uniforme na borda topo: 5% do quadro, cor RGB(13,19,28)
- Q31 (2:30): faixa uniforme na borda topo: 5% do quadro, cor RGB(15,23,33)
- Q32 (2:36): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q33 (2:37): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q34 (2:40): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q35 (2:44): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q36 (2:45): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q37 (2:54): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q38 (3:00): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q42 (3:22): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q43 (3:24): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q44 (3:28): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q45 (3:28): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q46 (3:29): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q47 (3:29): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q48 (3:30): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q49 (3:40): faixa uniforme na borda topo: 4% do quadro, cor RGB(207,190,158)
- Q50 (3:41): faixa uniforme na borda topo: 4% do quadro, cor RGB(246,245,244)
- Q50 (3:41): faixa uniforme na borda direita: 12% do quadro, cor RGB(222,220,216)
- Q51 (3:42): faixa uniforme na borda topo: 5% do quadro, cor RGB(17,39,71)
- Q51 (3:42): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(26,33,47)
- Q54 (4:06): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(21,35,56)
- Q55 (4:10): faixa uniforme na borda topo: 5% do quadro, cor RGB(17,39,71)
- Q56 (4:20): faixa uniforme na borda topo: 5% do quadro, cor RGB(17,39,71)
- Q59 (4:40): faixa uniforme na borda topo: 3% do quadro, cor RGB(123,125,128)
- Q60 (4:41): faixa uniforme na borda topo: 3% do quadro, cor RGB(246,245,244)
- Q60 (4:41): faixa uniforme na borda direita: 12% do quadro, cor RGB(222,220,217)
- Q61 (4:50): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(26,33,46)
- Q62 (5:00): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(26,32,45)
- Q63 (5:06): faixa uniforme na borda topo: 5% do quadro, cor RGB(34,43,58)
- Q66 (5:25): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q67 (5:26): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q68 (5:30): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q69 (5:40): faixa uniforme na borda topo: 5% do quadro, cor RGB(15,23,33)
- Q70 (5:41): faixa uniforme na borda topo: 5% do quadro, cor RGB(20,31,41)
- Q71 (5:41): faixa uniforme na borda topo: 5% do quadro, cor RGB(20,31,41)
- Q72 (5:50): faixa uniforme na borda topo: 4% do quadro, cor RGB(34,43,52)
- Q73 (6:00): faixa uniforme na borda topo: 5% do quadro, cor RGB(23,28,36)
- Q73 (6:00): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(50,45,39)
- Q74 (6:00): faixa uniforme na borda topo: 5% do quadro, cor RGB(23,28,36)
- Q76 (6:07): faixa uniforme na borda topo: 5% do quadro, cor RGB(25,30,38)
- Q76 (6:07): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(49,44,38)
- Q77 (6:10): faixa uniforme na borda topo: 5% do quadro, cor RGB(27,32,39)
- Q77 (6:10): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(49,44,38)
- Q79 (6:20): faixa uniforme na borda topo: 4% do quadro, cor RGB(17,27,38)
- Q80 (6:25): faixa uniforme na borda topo: 5% do quadro, cor RGB(14,20,30)
- Q83 (6:34): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q84 (6:35): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q85 (6:48): faixa uniforme na borda topo: 3% do quadro, cor RGB(246,245,243)
- Q85 (6:48): faixa uniforme na borda direita: 11% do quadro, cor RGB(222,220,215)
- Q89 (7:06): faixa uniforme na borda topo: 5% do quadro, cor RGB(50,45,38)
- Q99 (8:20): faixa uniforme na borda topo: 3% do quadro, cor RGB(242,241,239)
- Q99 (8:20): faixa uniforme na borda direita: 11% do quadro, cor RGB(212,210,206)
- Q100 (8:20): faixa uniforme na borda topo: 4% do quadro, cor RGB(246,245,244)
- Q100 (8:20): faixa uniforme na borda direita: 12% do quadro, cor RGB(222,220,216)
- Q101 (8:21): faixa uniforme na borda topo: 5% do quadro, cor RGB(17,39,71)
- Q101 (8:21): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(28,36,51)
- Q105 (8:50): faixa uniforme na borda topo: 4% do quadro, cor RGB(37,46,55)
- Q107 (9:10): faixa uniforme na borda topo: 5% do quadro, cor RGB(19,29,41)
- Q110 (9:30): faixa uniforme na borda topo: 5% do quadro, cor RGB(16,21,30)
- Q113 (9:43): faixa uniforme na borda topo: 5% do quadro, cor RGB(25,30,38)
- Q114 (9:50): faixa uniforme na borda topo: 5% do quadro, cor RGB(17,25,37)
- Q115 (10:00): faixa uniforme na borda topo: 4% do quadro, cor RGB(244,243,241)
- Q115 (10:00): faixa uniforme na borda direita: 11% do quadro, cor RGB(216,214,210)
- Q116 (10:00): faixa uniforme na borda topo: 4% do quadro, cor RGB(246,245,243)
- Q116 (10:00): faixa uniforme na borda direita: 11% do quadro, cor RGB(221,219,215)
- Q117 (10:10): faixa uniforme na borda topo: 5% do quadro, cor RGB(17,23,33)
- Q118 (10:10): faixa uniforme na borda topo: 5% do quadro, cor RGB(17,23,33)

## Quadros

Q01=0:00, Q02=0:04, Q03=0:10, Q04=0:12, Q05=0:19, Q06=0:20, Q07=0:20, Q08=0:30, Q09=0:37, Q10=0:40, Q11=0:46, Q12=0:50, Q13=1:06, Q14=1:07, Q15=1:10, Q16=1:17, Q17=1:20, Q18=1:20, Q19=1:30, Q20=1:40, Q21=1:41, Q22=1:45, Q23=1:50, Q24=1:52, Q25=2:10, Q26=2:13, Q27=2:13, Q28=2:14, Q29=2:20, Q30=2:30, Q31=2:30, Q32=2:36, Q33=2:37, Q34=2:40, Q35=2:44, Q36=2:45, Q37=2:54, Q38=3:00, Q39=3:08, Q40=3:10, Q41=3:20, Q42=3:22, Q43=3:24, Q44=3:28, Q45=3:28, Q46=3:29, Q47=3:29, Q48=3:30, Q49=3:40, Q50=3:41, Q51=3:42, Q52=3:50, Q53=4:00, Q54=4:06, Q55=4:10, Q56=4:20, Q57=4:21, Q58=4:30, Q59=4:40, Q60=4:41, Q61=4:50, Q62=5:00, Q63=5:06, Q64=5:10, Q65=5:20, Q66=5:25, Q67=5:26, Q68=5:30, Q69=5:40, Q70=5:41, Q71=5:41, Q72=5:50, Q73=6:00, Q74=6:00, Q75=6:04, Q76=6:07, Q77=6:10, Q78=6:13, Q79=6:20, Q80=6:25, Q81=6:26, Q82=6:30, Q83=6:34, Q84=6:35, Q85=6:48, Q86=6:50, Q87=6:59, Q88=7:00, Q89=7:06, Q90=7:10, Q91=7:20, Q92=7:30, Q93=7:33, Q94=7:40, Q95=7:50, Q96=7:52, Q97=8:10, Q98=8:19, Q99=8:20, Q100=8:20, Q101=8:21, Q102=8:30, Q103=8:40, Q104=8:46, Q105=8:50, Q106=9:00, Q107=9:10, Q108=9:20, Q109=9:25, Q110=9:30, Q111=9:37, Q112=9:40, Q113=9:43, Q114=9:50, Q115=10:00, Q116=10:00, Q117=10:10, Q118=10:10, Q119=10:20, Q120=10:30
