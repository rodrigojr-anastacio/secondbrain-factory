# Pré-QA visual automático

- Alvo: `pesquisa/canal-clima-2026-11/longo-04/preqa` · 120 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.311 · `tools/preqa_visual.py`
- Resultado: **REPROVADO (há bloqueante)** · bloqueante 6 · alto 30 · médio 34 · baixo 21
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:12 | Q03 `370.png` | medio | texto_encavalado | A etiqueta 'UNIÃO DA VITÓRIA (PR)' sobrepõe o topo do cilindro/anel vermelho do pluviômetro atrás dela, com o elemento aparecendo parcialmente escondido. A leitura continua possível, mas a composição fica confusa. |
| 0:19 | Q05 `556.png` | alto | elemento_fora | A foto do centro de Blumenau (rótulo 'CENTRO E RIO ITAJAÍ-AÇU · 2010') cobre quase todo o quadro e tapa o mapa 3D. Além disso, o valor '15,26 M' aparece sobreposto ao topo de um cilindro, e o cilindro parece cortado atrás do número. A data da foto (2010) é posterior a 1983, mas está rotulada como imagem atual, o que é aceitável. |
| 0:21 | Q06 `635.png` | medio | elemento_fora | O cilindro 3D passa para fora do quadro pelo topo e a etiqueta 'BLUMENAU (SC)' fica por cima do anel vermelho. Há também um bloco azul chapado (polígono de água) cortado na borda esquerda, que pode ser resquício da cena anterior. |
| 0:24 | Q07 `726.png` | alto | valor_errado | O rótulo no canto superior diz 'MOMBAÇA (CE) · 1983', mas o mapa mostra o Brasil inteiro sem nenhum marcador em Mombaça. A legenda ('Agora, suba 2.') fica sobre a parte inferior do mapa, perto do rodapé de fontes. Pode ser só um enquadramento de transição. |
| 0:36 | Q09 `1072.png` | medio | fundo/faixa | O fundo do mapa é muito escuro, quase preto, em toda a parte de cima e nas laterais (faixa RGB 14,19,27 no topo). Parece vinheta, mas o mapa quase não aparece e o contorno do litoral some. Pode ser estilo; registro por dúvida. |
| 0:36 | Q09 `1072.png` | medio | elemento_fora | A foto do açude seco (Santa Quitéria, 2018) está sobre a legenda 'MOMBAÇA (CE) · 1983'. A foto é de 2018 e o rótulo do mapa é de 1983, o que pode confundir. O selo vermelho da foto também fica colado na borda inferior da moldura. |
| 1:03 | Q17 `1902.png` | alto | texto_inventado | Na caixa branca sobre o Rio Grande do Sul aparece só um 'P' com uma barra vermelha: parece placeholder ou texto incompleto, sem sentido. |
| 1:03 | Q17 `1902.png` | medio | elemento_fora | Os cartões 1 e 2 estão em cima do mapa da América do Sul, e o cartão 2 já cobre parte do Brasil, enquanto os cartões 3 e 4 ainda não entraram. Pode ser entrada intencional da animação, então registro por dúvida. |
| 1:07 | Q18 `1997.png` | medio | texto_encavalado | A legenda 'E o que isso diz sobre 2026?' fica sobre o rótulo azul 'ÁGUA DEMAIS' e a área azul do Sul, bem perto. A leitura não é prejudicada, mas fica apertado. |
| 1:09 | Q19 `2061.png` | medio | valor_errado | O gráfico circular aparece todo em bege, sem cor para Sul e Sertão, embora o texto central já cite os dois. Pode ser o início da animação, então registro por dúvida. |
| 1:16 | Q20 `2268.png` | alto | texto_encavalado | Na parte de baixo do painel 'QUANDO CHOVE', a legenda azul 'SUL: CHUVA O ANO INTEIRO (FRENTES FRIAS)' fica atrás da legenda falada ('O sertão depende de poucos meses de'). Isso cobre o começo do texto e a linha de fonte do painel. |
| 1:16 | Q20 `2268.png` | medio | elemento_fora | A legenda de fala invade a área do painel do gráfico e cobre parte da sua legenda. |
| 1:44 | Q25 `3132.png` | medio | texto_encavalado | O rótulo 'MAI-JUN/83 · 6,65 M' está sobre a linha tracejada de 6 M e sobre a curva do gráfico, e o rótulo do eixo Y ('2.5' aparece como '.5', cortado pela borda esquerda do cartão); legibilidade fraca. |
| 1:50 | Q26 `3311.png` | alto | texto_encavalado | A placa de título 'CHEIO, MAS SOB CONTROLE' e a etiqueta '3 DE JULHO' cobrem a parte inferior do gráfico: o eixo X (JAN/83) fica parcialmente tapado e a fonte 'FONTE:' fica cortada. Além disso há dois textos redundantes ('CHEIO, MAS SOB CONTROLE' grande e a legenda 'Cheio, mas sob con') empilhados. |
| 2:12 | Q31 `3966.png` | medio | texto_encavalado | No gráfico, o rótulo '18 JUL · 10,42 M' encosta no marcador e no texto 'MÊS ACIMA DE 6 M', que fica espremido junto à borda direita do cartão e quase colide com a linha tracejada de 6 M; leitura apertada. |
| 2:17 | Q32 `4112.png` | alto | texto_encavalado | A etiqueta 'ACIMA DE 6 METROS' e a placa 'POR MAIS DE UM MÊS' cobrem o rodapé do gráfico: tapam o eixo X (JAN/83, ABR parcial) e o texto 'FONTE:' do gráfico, deixando-o cortado. |
| 2:17 | Q32 `4112.png` | medio | texto_encavalado | O rótulo '18 JUL · 10,42 M' e 'MÊS ACIMA DE 6 M' estão apertados e sobrepostos ao marcador e à faixa rosa; o texto 'MÊS ACIMA DE 6 M' encosta na borda direita do cartão. |
| 2:29 | Q35 `4481.png` | medio | tela_preta | O mapa de fundo está quase preto durante a exibição da foto da ponte. Pode ser escurecimento intencional para destacar a foto. Se não for, o fundo ficou apagado fora de uma transição. |
| 2:47 | Q38 `5017.png` | bloqueante | texto_encavalado | A placa de capítulo "A VÁRZEA VIROU UM LAGO" fica por cima do rótulo "LANDSAT 4 · MESMA JANELA · ~52 × 29 KM" à esquerda. O texto dos dois se mistura e atrapalha a leitura. A placa também repete a legenda logo abaixo ("A várzea virou um"). |
| 2:53 | Q40 `5198.png` | alto | elemento_fora | O rótulo vermelho "VALE ES…" está cortado e escondido atrás da moldura da foto de Blumenau, com o texto incompleto. O rótulo do mapa fica sobreposto à foto. |
| 2:53 | Q40 `5198.png` | medio | tela_preta | O fundo do mapa está muito escuro (quase preto) atrás da foto. Pode ser escurecimento intencional, mas o mapa quase não aparece. |
| 2:59 | Q41 `5365.png` | alto | valor_errado | O termômetro de Blumenau mostra 10,60 m, mas o rótulo da linha tracejada de referência (~10 m, à direita da coluna) está minúsculo, sobreposto à coluna e ilegível. A escala do eixo 10 também colide com o tracejado. |
| 3:05 | Q42 `5540.png` | alto | valor_errado | O número grande mostra 15,26 m (20/05), mas a lista abaixo diz 20/05 · 12,52 m. O valor do grande está inconsistente com a linha da data (o valor da cheia de 09/07 aparece no lugar). O rótulo da linha tracejada em 10 m também é ilegível. |
| 3:10 | Q43 `5700.png` | medio | valor_errado | A legenda diz 'em setembro, o rio encheu' enquanto o painel mostra 24/09 · 11,75 m, bem abaixo do pico de julho. O rótulo da linha de 10 m segue ilegível, minúsculo e sobreposto à coluna. |
| 3:12 | Q44 `5772.png` | alto | anacronismo | A foto legendada 'Blumenau · Enchente de 2008' aparece num trecho sobre 1983/Santa Catarina; é uma foto de outro evento, com blindado M113 e placa 'VIGIFO...' parcialmente cortada. Está fora do contexto temporal e fica sobre o mapa escuro. |
| 3:20 | Q45 `5989.png` | alto | valor_errado | O número animado mostra 75 (municípios em calamidade) enquanto a legenda fala em '78 municípios'. O valor animado está divergente da narração. |
| 3:29 | Q47 `6283.png` | medio | elemento_fora | O rótulo do topo diz 'PERGUNTA 2/4' mas o card ativo ('AGORA') ainda é o 1 (O que aconteceu no Sul?), em vez do 2. O 2 não está marcado. O mapa mostra o Nordeste, mas o destaque está desconectado. |
| 3:38 | Q50 `6553.png` | medio | valor_errado | O gráfico mostra só uma barra no início. Pode ser a animação de crescimento, mas a barra de 1920 está bem abaixo da média. Confirmar que o valor animado não começa errado. |
| 3:58 | Q52 `7127.png` | alto | texto_encavalado | A placa de capítulo '1983 EM MOMBAÇA' e a caixa de texto grande com '4▌' ficam por cima da parte inferior do gráfico e cobrem a linha de fonte e os rótulos do eixo. Parte do cartão do gráfico fica escondida. O texto ainda está em animação de digitação, então o defeito está na sobreposição e não no texto incompleto. |
| 4:11 | Q55 `7524.png` | medio | elemento_fora | A placa 'AÇUDES SECAM · O GADO MORRE' cobre a borda esquerda da foto do Açude de Coremas. A foto também invade a margem do mapa. Provavelmente é estilo intencional, mas a sobreposição está apertada e fica na dúvida. |
| 4:21 | Q57 `7831.png` | alto | elemento_fora | O cartão 'ALISTADOS NAS FRENTES DE EMERGÊNCIA' aparece vazio, sem gráfico nem valores, só o título e a fonte. Pode ser animação de entrada, mas vale confirmar que o gráfico entra a tempo. |
| 4:28 | Q58 `8051.png` | medio | texto_encavalado | No gráfico, o rótulo '3,13 MILHÕES' encosta no título do cartão 'ALISTADOS NAS FRENTES DE EMERGÊNCIA'; o '3,13' fica quase em cima do título. O rótulo '~460 MIL' também é discreto sobre a barra azul. |
| 4:28 | Q58 `8051.png` | medio | valor_errado | A legenda diz 'menos de 500' (mil), mas o gráfico mostra '~460 MIL' e a fala omite a unidade. Pode confundir; confirmar se é consistente. |
| 5:13 | Q68 `9381.png` | bloqueante | fundo/faixa | Quadro quase todo escuro e vazio: um bloco azul-marinho chapado com divisão diagonal cobre a maior parte da tela, com só um canto de oceano visível no alto à direita. Parece mapa/globo que ainda não carregou (textura ausente), com faixas uniformes no topo e à esquerda. |
| 5:16 | Q69 `9467.png` | alto | fundo/faixa | O mapa do Pacífico é um plano inclinado e flutuante. Faixas chapadas azul-marinho aparecem no topo e à esquerda, e as bordas do plano ficam visíveis (canto superior esquerdo e borda inferior), sem cobrir o quadro. |
| 5:18 | Q70 `9539.png` | alto | fundo/faixa | O plano do mapa do Pacífico fica solto sobre o fundo azul-escuro. A camada de anomalia de temperatura tem bordas retas e serrilhadas (esquerda, perto da Austrália), e há emenda visível entre ela e o mapa base. |
| 5:26 | Q71 `9779.png` | bloqueante | fundo/faixa | O mapa foi achatado numa faixa fina no meio do quadro, cercado por grandes áreas azul-marinho chapadas. Há uma faixa azul mais clara no topo (RGB 17,39,71), com corte reto atrás do título. |
| 5:26 | Q71 `9779.png` | alto | valor_errado | Os valores animados dos marcadores aparecem como 0,26, 0,00, 0,00 e 0,00 enquanto os rótulos dizem +2,4, +2,3, +2,2 e +2,0. Os contadores começam em zero e as formas ainda são polígonos achatados. |
| 5:33 | Q72 `10003.png` | alto | fundo/faixa | O mapa continua reduzido a uma faixa fina e deformada sobre fundo azul-escuro chapado, com a faixa azul no topo (RGB 17,39,71) atrás do título e do '+2,4 °C'. |
| 5:33 | Q72 `10003.png` | medio | valor_errado | Os valores acima das pirâmides (2,40, 2,28, 2,25, 1,97) divergem dos rótulos (+2,4, +2,3, +2,2, +2,0) por arredondamento. O número 2,40 também toca o '+2,4 °C' do topo e o título, e a legibilidade dos números é fraca. |
| 5:36 | Q73 `10075.png` | alto | fundo/faixa | Faixa azul chapada (RGB 17,39,71) no topo, atrás do mapa 3D, com corte nítido em relação ao fundo escuro; o mapa flutua num fundo de cor diferente. Também há o mesmo bloco azul no topo em Q74 e Q75. |
| 5:42 | Q74 `10249.png` | alto | fundo/faixa | Faixa azul chapada no topo (~12% do quadro) com borda nítida contra o fundo escuro atrás do mapa 3D; fundo inconsistente. A seta azul de descida está cortada/pequena, sem rótulo ainda. |
| 5:47 | Q75 `10407.png` | alto | fundo/faixa | Faixa azul chapada no topo atrás do mapa 3D, com limite horizontal visível contra o fundo escuro. |
| 5:55 | Q77 `10638.png` | alto | texto_encavalado | A legenda 'Bem na entrada da época de chuva do ser' cobre o texto do cartão do calendário ('...NIÑO: DEZEMBRO E JANEIRO') e a linha de fonte, que ficam parcialmente escondidos. |
| 5:59 | Q78 `10781.png` | alto | texto_encavalado | A legenda 'O inverno do sertanejo veio fraco...' cobre a legenda do calendário ('...E JANEIRO', '...A MAIO'), deixando o texto cortado e ilegível dentro do cartão. |
| 6:02 | Q79 `10853.png` | medio | texto_inventado | A imagem da NOAA em transparência sobre o mapa tem o título 'Warm Episode Relationships' cortado pela borda superior e em inglês, e a sobreposição com o mapa de fundo deixa o texto confuso. Pode ser crossfade; fica a dúvida. |
| 6:20 | Q81 `11394.png` | medio | valor_errado | No eixo Y aparece '2.5' parcialmente cortado na borda esquerda do cartão ('.5'), e os rótulos 'OUT/82' e 'SET' tocam as bordas do gráfico. Há ainda a curva tracejada vermelha do Pacífico interrompida, o que pode ser animação em andamento. |
| 6:26 | Q82 `11569.png` | medio | texto_encavalado | No marcador do pico, o rótulo '18 JUL 1983' fica colado ao ponto e à linha vertical, e o título '18 JUL · 10,42 M' fica logo acima, quase encostando. Os dois textos ficam apertados e com leitura fraca. |
| 6:31 | Q83 `11730.png` | medio | texto_encavalado | Os rótulos 'RIO NO PICO ↗' e 'PACÍFICO ESFRIANDO ↘' ficam por cima da área azul e da linha tracejada do gráfico, com contraste fraco. O 'RIO NO PICO' em azul sobre o preenchimento azul fica pouco legível. |
| 6:43 | Q85 `12079.png` | alto | legenda | A legenda no centro inferior mostra só 'F▌' numa caixinha, uma palavra incompleta. Pode ser início de animação de digitação, mas ficou isolada num quadro longe do início da fala. Vale confirmar. |
| 6:43 | Q85 `12079.png` | medio | elemento_fora | No cartão do gráfico circular, as duas legendas azuis (primavera e outono-inverno) usam a mesma cor. O gráfico mostra azul só na primavera/ano 1 e em parte do ano 2, e a legenda 'Outono-inverno' não é distinguível. Há dúvida se é erro de dado ou animação em andamento. |
| 6:51 | Q86 `12342.png` | bloqueante | texto_encavalado | A placa de capítulo 'VAI IMPORTAR EM 2026' (com carimbo 'GUARDE...' atrás) se sobrepõe à legenda 'Guarde isso. Vai importar em 2026.', que repete o mesmo texto e cobre o carimbo. A legenda também cobre a legenda do gráfico, cortando o início das linhas 'PRIMAVERA DO ANO 1…' e 'OUTONO-INVERNO…'. O resultado atrapalha a leitura. |
| 7:23 | Q93 `13277.png` | alto | fundo/faixa | O mapa (satélite + camada de temperatura do mar) aparece como um retângulo inclinado sobre fundo azul-escuro chapado. Há grandes áreas vazias no topo e à direita, e a borda do mapa fica visível e cortada. Os sinais automáticos de faixa uniforme no topo e na direita confirmam. A camada de anomalia térmica tem recortes serrilhados e sai do quadro à esquerda. |
| 7:23 | Q93 `13277.png` | alto | elemento_fora | O rótulo vermelho '2026' está cortado pela borda esquerda do quadro e aparece só como '2026' parcial, sem o texto completo. Ele fica sobreposto ao cartão '1 O QUE ACONTECEU NO SUL?' e à camada do mapa. |
| 7:23 | Q93 `13277.png` | medio | texto_encavalado | Os cartões das perguntas 1 a 4 ficam em cima do mapa vermelho. Os cartões 1 e 2 estão semitransparentes e o texto fica com contraste fraco sobre o fundo avermelhado. |
| 7:25 | Q94 `13347.png` | alto | fundo/faixa | O mapa aparece como um bloco inclinado, com a borda esquerda e a inferior visíveis, sobre fundo azul-escuro chapado. Há grande área vazia à esquerda e abaixo, e o sinal automático acusa faixa uniforme na borda esquerda. A camada de temperatura tem bordas serrilhadas, em degraus, sobre a Austrália e a Ásia. |
| 7:27 | Q95 `13402.png` | medio | fundo/faixa | Faixa escura chapada no topo e na base atrás do mapa inclinado, com bordas retas do plano visíveis. A camada de temperatura tem bordas serrilhadas em degraus ao redor da Austrália, da Indonésia e da costa oeste da América. |
| 7:38 | Q97 `13754.png` | bloqueante | fundo/faixa | O mapa do Pacífico aparece como uma faixa retangular chapada (anomalia de temperatura) com bordas retas no topo (~y=125) e embaixo (~y=455), em contraste com a Terra escura ao redor. Parece uma faixa/emenda atrás do mapa, não uma projeção natural. |
| 7:38 | Q97 `13754.png` | alto | valor_errado | O mostrador 'Chance de El Niño histórico' marca ~3% com a agulha quase em 0%. Já o título '+2,5 °C' e a legenda ('E calculou cerca de') indicam que o valor ainda está sendo animado e começa errado. Uma agulha em ~3% sobre o arco cinza sem preenchimento é ruim se o quadro ficar visível. |
| 7:47 | Q98 `14019.png` | bloqueante | fundo/faixa | A mesma faixa retangular de anomalia do Pacífico com bordas retas horizontais (topo ~y=135, base ~y=455), contrastando com o mapa escuro em volta, parece emenda/faixa de cor chapada atrás do mapa. |
| 7:47 | Q98 `14019.png` | medio | texto_cortado | A legenda termina em 'Mas não é cer' (palavra cortada). Provavelmente está no meio da animação de digitação, então o defeito não é certo. |
| 7:47 | Q98 `14019.png` | medio | valor_errado | O selo 'PROVÁVEL = CERTO' no mostrador contradiz a legenda ('mais provável que sim. Mas não é cer[teza]') e o próprio ~60%. Isso é falha de conteúdo, não só estética; vale revisar. |
| 8:18 | Q102 `14926.png` | alto | texto_encavalado | A legenda 'A NOAA prevê que o de agora comece a enfraquecer no início de 2027.' invade a parte inferior do cartão do calendário e cobre a legenda do cartão (só aparece 'FONTE: NOAA/CPC (BOLETIM DE 12/11/2026)' parcialmente coberta). Isso encobre a legenda 'PRIMAVERA DE 2026: JÁ ACONTECEU'. |
| 8:26 | Q103 `15173.png` | medio | texto_encavalado | A placa 'É ATENÇÃO' e a tarja 'ISSO NÃO É PREVISÃO DE ENCHENTE' ficam coladas, e a legenda 'também merecem atenção' se aproxima da legenda do gráfico (OUTONO E INVERNO...). O texto da legenda quase toca a caixa do calendário, e a fonte 'FONTE: NOAA/CPC' fica logo atrás da legenda de rodapé. Aperto de layout, mas legível. |
| 9:03 | Q109 `16296.png` | medio | fundo/faixa | O sinal automático acusou faixa uniforme escura (RGB 14,20,29) na borda do topo. O fundo do mapa está muito escurecido atrás da foto, e o topo parece quase preto. Provavelmente é vinheta/dimming intencional para destacar a foto, mas convém confirmar que não é faixa chapada. |
| 9:38 | Q115 `17338.png` | alto | texto_encavalado | A legenda 'Foi o mesmo El Niño, puxando o Brasil para os dois lad' se sobrepõe à parte de baixo da placa 'PUXANDO O BRASIL PARA OS DOIS LADOS', e o texto da placa repete o da legenda. Se a legenda estiver só em animação de digitação, o encavalamento ainda assim atrapalha a leitura. |
| 9:40 | Q116 `17410.png` | medio | fundo/faixa | O plano do mapa 3D está inclinado e deixa cantos e faixas de fundo azul-escuro chapado no topo e na base. Isso pode ser movimento de câmera, mas as bordas do plano ficam visíveis. |
| 9:46 | Q117 `17582.png` | alto | fundo/faixa | Faixa chapada azul-escura (RGB 23,30,43) com cerca de 5% de altura no topo atrás do mapa 3D do Pacífico, e uma faixa semelhante na base. O mapa não preenche o quadro. Pode ser a borda do plano 3D durante a câmera em movimento, então vale conferir. |
| 9:51 | Q118 `17739.png` | medio | fundo/faixa | O plano do mapa está inclinado e deixa triângulos de fundo azul-escuro chapado no topo e na base. Pode ser transição de câmera, mas as bordas do plano aparecem. |
| 9:54 | Q119 `17811.png` | medio | elemento_fora | A placa grande 'MANDA PRA QUEM TEM FAMÍLIA NO SUL OU NO SERTÃO' cobre boa parte do Nordeste vermelho e do mapa. Ela repete o conteúdo da legenda, que está em digitação ('Se você quer entender co'). Pode ser intencional, mas fica pesado visualmente. |

21 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q08 (0:30): faixa uniforme na borda topo: 5% do quadro, cor RGB(18,26,34)
- Q09 (0:36): faixa uniforme na borda topo: 5% do quadro, cor RGB(14,19,27)
- Q10 (0:39): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q11 (0:42): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q12 (0:46): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q14 (0:53): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(28,32,38)
- Q15 (0:58): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(28,31,38)
- Q16 (1:00): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(28,31,38)
- Q18 (1:07): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(29,32,38)
- Q40 (2:53): faixa uniforme na borda topo: 5% do quadro, cor RGB(30,25,21)
- Q48 (3:33): faixa uniforme na borda topo: 3% do quadro, cor RGB(19,26,32)
- Q49 (3:36): faixa uniforme na borda topo: 5% do quadro, cor RGB(16,23,32)
- Q53 (4:00): faixa uniforme na borda topo: 4% do quadro, cor RGB(36,40,45)
- Q55 (4:11): faixa uniforme na borda topo: 4% do quadro, cor RGB(24,26,32)
- Q55 (4:11): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(47,39,33)
- Q56 (4:13): faixa uniforme na borda topo: 4% do quadro, cor RGB(27,29,34)
- Q56 (4:13): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(45,38,33)
- Q57 (4:21): faixa uniforme na borda topo: 4% do quadro, cor RGB(26,28,34)
- Q57 (4:21): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(46,38,33)
- Q59 (4:31): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q60 (4:38): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q61 (4:47): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q62 (4:53): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q63 (4:59): faixa uniforme na borda topo: 3% do quadro, cor RGB(199,176,130)
- Q68 (5:13): faixa uniforme na borda topo: 4% do quadro, cor RGB(19,27,40)
- Q68 (5:13): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(24,29,40)
- Q69 (5:16): faixa uniforme na borda topo: 4% do quadro, cor RGB(23,30,43)
- Q69 (5:16): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(22,29,40)
- Q71 (5:26): faixa uniforme na borda topo: 5% do quadro, cor RGB(17,39,71)
- Q72 (5:33): faixa uniforme na borda topo: 4% do quadro, cor RGB(17,39,71)
- Q73 (5:36): faixa uniforme na borda topo: 5% do quadro, cor RGB(17,39,71)
- Q74 (5:42): faixa uniforme na borda topo: 5% do quadro, cor RGB(17,39,71)
- Q75 (5:47): faixa uniforme na borda topo: 5% do quadro, cor RGB(17,39,71)
- Q76 (5:49): faixa uniforme na borda topo: 4% do quadro, cor RGB(35,42,50)
- Q93 (7:23): faixa uniforme na borda topo: 5% do quadro, cor RGB(23,30,43)
- Q93 (7:23): faixa uniforme na borda direita: 5% do quadro, cor RGB(24,29,40)
- Q94 (7:25): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(23,29,40)
- Q109 (9:03): faixa uniforme na borda topo: 5% do quadro, cor RGB(14,20,29)
- Q117 (9:46): faixa uniforme na borda topo: 5% do quadro, cor RGB(23,30,43)

## Quadros

Q01=0:01, Q02=0:07, Q03=0:12, Q04=0:15, Q05=0:19, Q06=0:21, Q07=0:24, Q08=0:30, Q09=0:36, Q10=0:39, Q11=0:42, Q12=0:46, Q13=0:49, Q14=0:53, Q15=0:58, Q16=1:00, Q17=1:03, Q18=1:07, Q19=1:09, Q20=1:16, Q21=1:25, Q22=1:31, Q23=1:36, Q24=1:38, Q25=1:44, Q26=1:50, Q27=1:53, Q28=1:59, Q29=2:04, Q30=2:07, Q31=2:12, Q32=2:17, Q33=2:19, Q34=2:25, Q35=2:29, Q36=2:32, Q37=2:40, Q38=2:47, Q39=2:50, Q40=2:53, Q41=2:59, Q42=3:05, Q43=3:10, Q44=3:12, Q45=3:20, Q46=3:26, Q47=3:29, Q48=3:33, Q49=3:36, Q50=3:38, Q51=3:48, Q52=3:58, Q53=4:00, Q54=4:06, Q55=4:11, Q56=4:13, Q57=4:21, Q58=4:28, Q59=4:31, Q60=4:38, Q61=4:47, Q62=4:53, Q63=4:59, Q64=5:01, Q65=5:04, Q66=5:06, Q67=5:09, Q68=5:13, Q69=5:16, Q70=5:18, Q71=5:26, Q72=5:33, Q73=5:36, Q74=5:42, Q75=5:47, Q76=5:49, Q77=5:55, Q78=5:59, Q79=6:02, Q80=6:10, Q81=6:20, Q82=6:26, Q83=6:31, Q84=6:33, Q85=6:43, Q86=6:51, Q87=6:54, Q88=6:59, Q89=7:03, Q90=7:06, Q91=7:13, Q92=7:20, Q93=7:23, Q94=7:25, Q95=7:27, Q96=7:29, Q97=7:38, Q98=7:47, Q99=7:50, Q100=7:58, Q101=8:09, Q102=8:18, Q103=8:26, Q104=8:28, Q105=8:37, Q106=8:46, Q107=8:48, Q108=8:56, Q109=9:03, Q110=9:06, Q111=9:12, Q112=9:18, Q113=9:21, Q114=9:30, Q115=9:38, Q116=9:40, Q117=9:46, Q118=9:51, Q119=9:54, Q120=9:59
