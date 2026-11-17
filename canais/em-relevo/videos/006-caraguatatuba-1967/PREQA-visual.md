# Pré-QA visual automático

- Alvo: `canais/em-relevo/videos/006-caraguatatuba-1967/preqa` · 97 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.235 · `tools/preqa_visual.py`
- Resultado: **REPROVADO (há bloqueante)** · bloqueante 1 · alto 17 · médio 31 · baixo 13
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:03 | Q01 `90.png` | alto | valor_errado | A barra/rótulo no mapa mostra 530 MM, mas a legenda diz 'Em Bertioga, 683'. O valor da legenda não bate com o número animado (pode ser a barra ainda crescendo, mas parece divergente). |
| 0:09 | Q02 `270.png` | medio | valor_errado | Rótulo da barra mostra 216 MM, mas a legenda fala 234 mm para Caraguatatuba. O contador ainda não chegou ao valor, ou o dado está errado. Conferir. |
| 0:15 | Q03 `450.png` | medio | elemento_fora | O rótulo '234 MM' do quadro anterior aparece cortado e esmaecido atrás da borda superior da foto Landsat, no alto, à direita. É resíduo de HUD que vaza para outro elemento. |
| 0:21 | Q04 `630.png` | medio | valor_errado | A altura marcada nos cortes (685 M e 700 M) não bate com o 699 M do Q08 para o mesmo corte de Caraguatatuba. A legenda 'onde' está no meio da digitação, então isso não é defeito. |
| 0:45 | Q08 `1350.png` | alto | valor_errado | A medida no corte 3D mostra 699 M, mas o cartão 'PAREDE 700 M' e a legenda dizem 700 m. O valor animado está inconsistente ou ainda não terminou. |
| 0:57 | Q10 `1710.png` | alto | texto_encavalado | A legenda 'Depois de 19' (em digitação) fica por cima da faixa vermelha 'CARTA DE DECLI... · 1975' e esconde parte do título. A faixa é um rótulo do próprio mapa, então o texto fica cortado/encavalado. A legenda em si é animação de digitação e não conta como defeito. |
| 0:57 | Q10 `1710.png` | medio | elemento_fora | Os três cards de dados (700 M, 400 MM, 1 A 2,5 M) aparecem apagados sobre o fundo bege, com baixo contraste e o rótulo quase ilegível. Pode ser fade intencional da transição, mas fica fraco. Na dúvida, registro como estilo. |
| 1:03 | Q11 `1890.png` | medio | elemento_fora | A legenda cobre a parte inferior da carta de declividades, que está cortada na borda. A faixa vermelha com o título da carta aparece só como uma tira atrás da legenda, então o rótulo fica escondido. Dúvida entre estilo e defeito. |
| 1:21 | Q14 `2430.png` | alto | texto_cortado | A legenda diz 'Suba a câmera pelo vale do Rio Sa', com o nome cortado (deveria ser Rio Sahy ou similar). Pode ser digitação em andamento, mas não há cursor visível, o que sugere texto truncado. |
| 1:21 | Q14 `2430.png` | medio | valor_errado | O medidor mostra '349 M' com a marca em 3,5 km, enquanto no Q15 sobe a 750 M com 7,5 km. A animação parece coerente, mas o medidor está colado na borda direita e o 750 M do Q15 fica encostado no topo do painel. |
| 1:45 | Q18 `3150.png` | medio | elemento_fora | A linha vermelha do escoamento começa sobre o rótulo 'BACIA DO SANTO ANTÔNIO' e o atravessa. Além disso, o rótulo 'MINUTOS, NÃO DIAS' fica colado no canto inferior esquerdo, ao lado da legenda. Pode ser intencional, mas a leitura fica apertada. |
| 2:03 | Q21 `3690.png` | medio | elemento_fora | A linha tracejada amarela passa por cima do relevo sem ligação clara com os pontos citados no rótulo 'CARAGUATATUBA ↔ BARRA DO SAHY'. Ela termina no meio do mapa, e a ponta do lado de Caraguatatuba parece não coincidir com o litoral. Há dúvida se é um defeito de posicionamento. |
| 2:09 | Q22 `3870.png` | medio | fundo/faixa | O fundo é navy escuro com relevo quase invisível, e o bloco 3D fica pequeno e deslocado para a esquerda, deixando grande área vazia à direita. O detector acusou faixas uniformes nas bordas. Provavelmente é fundo intencional e não uma faixa de cor errada, mas o fundo difere do mapa das cenas vizinhas. |
| 2:45 | Q28 `4950.png` | medio | texto_cortado | O rótulo 'FAIXA DE POUCOS KM' está cortado pela borda esquerda ('IXA DE POUCOS KM'). Pode ser movimento de câmera, mas ele fica ilegível no quadro. |
| 2:51 | Q29 `5130.png` | medio | texto_cortado | A etiqueta 'PLUVIÔMETRO · BERTIOGA' está cortada pela borda esquerda ('LUVIÔMETRO'). Pode ser movimento de câmera, mas ela fica ilegível no quadro. |
| 3:03 | Q31 `5490.png` | medio | texto_encavalado | A caixa de legenda cobre a base do rótulo/seta 'CICLONE PEQUENO' e o ponto do ciclone, que fica parcialmente escondido atrás dela. |
| 3:09 | Q32 `5670.png` | alto | texto_encavalado | A legenda 'O oceano estava mais quente que o normal, e o vento,' cobre a parte de cima da etiqueta laranja 'OCEANO MAIS QUENTE (+~1 °C)'. A etiqueta fica cortada e difícil de ler. |
| 3:21 | Q34 `6030.png` | medio | texto_encavalado | O rótulo amarelo 'MÉDIA DE FEVEREIRO · 225 MM' está quebrado em duas linhas, e a linha tracejada da média passa por cima do texto, cortando 'FEVEREIRO'. A leitura fica prejudicada. |
| 3:27 | Q35 `6210.png` | medio | texto_encavalado | O rótulo 'MÉDIA DE FEVEREIRO · 225 MM' fica sobre o relevo claro, com a linha tracejada passando pelo texto, e perde legibilidade. Pode ser parte da transição, mas o texto continua difícil de ler. |
| 3:39 | Q37 `6570.png` | alto | texto_encavalado | Na coluna esquerda, o rótulo '115 MM' quebra em duas linhas e a segunda linha ('MM') cobre a data '17 / 03', que fica cortada atrás da legenda. Há sobreposição de elementos. |
| 3:51 | Q39 `6930.png` | bloqueante | texto_encavalado | O texto de tela 'NA SERRA, A CHUVA MUDA DE VALE PARA VALE' fica por cima dos rótulos 'TRANSBORDOU' e 'MENOS DA METADE', que aparecem cortados e sobrepostos. Isso atrapalha a leitura. |
| 3:57 | Q40 `7110.png` | alto | texto_encavalado | Ainda aparece o texto 'NA SERRA, A CHUVA MUDA DE VALE PARA VALE' sobreposto aos rótulos 'POSTO A POUCOS KM' e 'MENOS DA METADE'. O cartão 'CASCA 1 A 2,5 M' entra por cima na mesma cena. Provavelmente é crossfade, mas há elementos duplicados e confusos. Vale conferir. |
| 4:03 | Q41 `7290.png` | alto | texto_encavalado | O painel 'Corte da encosta' cobre o título 'MORRO DO CRUZEIRO · CARAGUATATUBA' (parte inferior das letras cortada) e o número '5,7 KM' fica parcialmente escondido atrás do painel. Na régua, o '0' do topo está cortado e '2' e '2,5' ficam quase colados. |
| 4:09 | Q42 `7470.png` | alto | texto_encavalado | O painel cobre o título 'MORRO DO CRUZEIRO · CARAGUATATUBA' e esconde parte do '5,7 KM'. O '0' da régua está cortado no topo e os rótulos '2' e '2,5' se apertam. |
| 4:15 | Q43 `7650.png` | alto | texto_encavalado | No cartão 'SERRA × CASCA', o '700 M' encavala com o título 'SERRA × CASCA' e encosta no topo da barra. Há também um '700 M' duplicado no gráfico do mapa. |
| 4:21 | Q44 `7830.png` | alto | texto_encavalado | No cartão 'SERRA × CASCA', o '700 M' encavala com o título do cartão e quase encosta nele. |
| 4:27 | Q45 `8010.png` | medio | outro | A cena do esquema é um bloco chapado com árvores cortadas no topo (as copas de cima ficam cortadas pela borda superior da área do desenho). O fundo está vazio e a composição é pouco atraente. Há dúvida se é estilo ou defeito. |
| 4:39 | Q47 `8370.png` | alto | texto_encavalado | O rótulo vermelho 'A RUPTURA DESCE ATÉ A ROCHA SÃ' fica atrás da legenda e é cortado pela caixa, com a metade inferior das letras escondida. Uma árvore também é cortada na borda direita do desenho. |
| 4:45 | Q48 `8550.png` | medio | fundo/faixa | O mapa de declividade escaneado aparece em preto e branco sobre fundo bege liso, com uma borda branca de papel e uma legenda com texto minúsculo ilegível do documento original. Há uma faixa branca sem conteúdo no topo do mapa. A legenda cobre a parte inferior do mapa. Há dúvida se é estilo. |
| 4:51 | Q49 `8730.png` | alto | texto_encavalado | A legenda no rodapé cobre a parte de baixo da imagem do mapa em preto e branco e a sombra/faixa vermelha embaixo dela, que fica meio visível sob a legenda. A imagem também parece cortada na base atrás da legenda. |
| 4:51 | Q49 `8730.png` | medio | fundo/faixa | O fundo bege chapado com o mapa escaneado em P&B (cartão branco com sombra) destoa do estilo de relevo 3D do canal. Pode ser intencional, como documento histórico, mas cabe conferir. O mapa escaneado tem texto minúsculo ilegível no quadro do canto superior direito. |
| 5:03 | Q51 `9090.png` | medio | texto_encavalado | A legenda ainda está sendo digitada ('A re'), o que não é defeito. Porém o rótulo 'GRANITO DE CARAGUATATUBA' fica em cima das manchas de pontos do mapa e perde legibilidade. O título '8 EM CADA 10' encosta no topo do quadro. |
| 5:39 | Q57 `10170.png` | alto | valor_errado | O contador grande no topo mostra "629 CICATRIZES", mas a legenda diz "640 cicatrizes" (palavra 640 sublinhada). Os valores divergem entre tela e narração. |
| 5:57 | Q60 `10710.png` | medio | texto_encavalado | O rótulo "AVALANCHE DE DETRITOS (OLGA CRUZ)" aparece esmaecido, com baixo contraste sobre a floresta verde, e fica sobre a linha de detritos. É provável que esteja em fade-in, mas a legibilidade é fraca. |
| 6:09 | Q62 `11070.png` | medio | tela_preta | Fundo quase todo navy escuro e sem conteúdo, com o relevo quase invisível. Só há o título e a legenda. Os sinais automáticos de faixa na borda base e na direita correspondem ao mar escuro do mapa. Pode ser transição intencional, mas a cena está vazia. |
| 6:21 | Q64 `11430.png` | alto | texto_encavalado | Crossfade entre o mapa escuro e o mapa satélite com cartões 1–4 e textos duplicados e fantasmas, como "RIO SANTO ANTÔNIO · LARGURA (ESQUEMA)" e "10-20 M". Se for transição, é aceitável, mas se o quadro ficar parado haverá sobreposição ilegível. |
| 6:27 | Q65 `11610.png` | alto | valor_errado | Painel direito mostra "ATÉ 0 CM" (contador animado começando em zero) sobreposto ao prédio, enquanto a lama ainda não subiu; valor inicial errado/estranho. O rótulo amarelo também invade o prédio bege com leitura ruim. |
| 6:33 | Q66 `11790.png` | medio | texto_cortado | Legenda termina em "mais de 1 me" e fica cortada, mas pode ser animação de digitação; confirmar que a frase completa aparece depois. |
| 6:33 | Q66 `11790.png` | medio | texto_encavalado | Rótulo "ATÉ 80 CM" fica sobre o prédio bege e a lama translúcida, com contraste fraco. A linha amarela vertical na borda direita do painel parece solta. |
| 6:39 | Q67 `11970.png` | medio | elemento_fora | Composição desequilibrada: o número "120" e os rótulos ficam deslocados para a esquerda, e o título "VÍTIMAS DE 1967" está desalinhado em relação ao bloco do número. Há um grande vazio à direita, e o fundo é muito escuro, quase sem relevo visível. |
| 7:09 | Q72 `12870.png` | medio | outro | A etiqueta de capítulo mudou para "5 · 2023: A MESMA RECEITA", mas a legenda ainda é a frase do capítulo 4 sobre a planície (1967/fazenda), e o mapa está igual ao anterior. Possível dessincronia entre capítulo e fala; confirmar. |
| 7:33 | Q76 `13590.png` | medio | valor_errado | A régua mostra 584 M e 5,0 KM e depois vira 685 M e 5,4 KM em Q77. Se isso for contador animado, tudo bem; se não, o valor inicial está errado. Há dúvida entre animação e erro. |
| 7:39 | Q77 `13770.png` | alto | valor_errado | O painel e o mapa mostram 685 M e 5,4 KM (parede), enquanto o quadro anterior Q76 mostrava 584 M e 5,0 KM para o mesmo corte. A altura do diorama parece quase igual nos dois quadros. Pode ser animação de valor que ainda não terminou, ou os valores divergem; conferir qual é o correto. |
| 8:09 | Q82 `14670.png` | medio | texto_encavalado | O título 'A RECEITA DA SERRA DO MAR' aparece semitransparente sobre o relevo claro e fica quase ilegível. Pode ser entrada ou crossfade do título; se for estado estático, falta contraste. |
| 8:45 | Q88 `15750.png` | medio | valor_errado | Os valores animados dos dois blocos (685 M / 5,4 KM e 700 M / 5,7 KM) vêm da animação que antes mostrava 360/368 M e 3,2/3,4 KM, e as barras de escala ainda estão em transição. A legenda diz 'o degrau medido é o mesmo', mas 685 e 700 não são idênticos. Confirmar o estado final do cálculo. |
| 9:09 | Q92 `16470.png` | medio | fundo/faixa | O mapa inteiro está lavado em tom marrom/âmbar chapado, com mar e terra quase sem contraste e relevo apagado. Pode ser uma transição intencional (fade para o fundo da placa 'O QUE FAZER'), mas a faixa uniforme de 10% na borda direita indica fundo sem textura. Confirmar que é crossfade e não perda de textura. |
| 9:15 | Q93 `16650.png` | medio | fundo/faixa | O fundo marrom liso, sem mapa, ocupa o quadro todo, com faixas uniformes nas bordas (topo, base, direita). Parece fundo de cena intencional atrás dos cartões. Há dúvida se a perda do mapa 3D é estilo ou defeito. A metade direita fica vazia. |
| 9:27 | Q95 `17010.png` | medio | tela_preta | O mapa fica quase preto (azul-marinho muito escuro, RGB ~11,18,36), com relevo quase invisível atrás do cartão 'VÍDEO NO CANAL'. Pode ser vinheta intencional de encerramento, mas o fundo está bem escuro e sem informação. Confirmar. |
| 9:33 | Q96 `17190.png` | medio | tela_preta | Mesmo fundo quase preto do Q95, com o mapa praticamente invisível durante todo o cartão. Se for intencional, ok. O trecho já dura mais de 6 s sem a câmera mostrar nada. |

13 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q03 (0:15): faixa uniforme na borda direita: 3% do quadro, cor RGB(12,31,57)
- Q08 (0:45): faixa uniforme na borda base: 6% do quadro, cor RGB(20,30,56)
- Q08 (0:45): faixa uniforme na borda direita: 9% do quadro, cor RGB(16,24,47)
- Q09 (0:51): faixa uniforme na borda base: 7% do quadro, cor RGB(20,30,56)
- Q10 (0:57): faixa uniforme na borda base: 5% do quadro, cor RGB(221,206,173)
- Q11 (1:03): faixa uniforme na borda base: 5% do quadro, cor RGB(221,206,173)
- Q11 (1:03): faixa uniforme na borda direita: 11% do quadro, cor RGB(220,204,169)
- Q22 (2:09): faixa uniforme na borda base: 7% do quadro, cor RGB(18,28,56)
- Q22 (2:09): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(17,24,46)
- Q22 (2:09): faixa uniforme na borda direita: 11% do quadro, cor RGB(15,23,46)
- Q23 (2:15): faixa uniforme na borda base: 6% do quadro, cor RGB(18,25,46)
- Q24 (2:21): faixa uniforme na borda base: 6% do quadro, cor RGB(22,30,52)
- Q25 (2:27): faixa uniforme na borda base: 3% do quadro, cor RGB(27,35,58)
- Q29 (2:51): faixa uniforme na borda base: 4% do quadro, cor RGB(58,64,150)
- Q33 (3:15): faixa uniforme na borda base: 7% do quadro, cor RGB(18,29,56)
- Q33 (3:15): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(20,27,48)
- Q33 (3:15): faixa uniforme na borda direita: 20% do quadro, cor RGB(15,23,46)
- Q34 (3:21): faixa uniforme na borda base: 7% do quadro, cor RGB(18,29,56)
- Q34 (3:21): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(20,27,48)
- Q34 (3:21): faixa uniforme na borda direita: 18% do quadro, cor RGB(15,23,46)
- Q35 (3:27): faixa uniforme na borda base: 6% do quadro, cor RGB(22,31,58)
- Q36 (3:33): faixa uniforme na borda topo: 4% do quadro, cor RGB(226,212,182)
- Q36 (3:33): faixa uniforme na borda base: 7% do quadro, cor RGB(220,203,168)
- Q36 (3:33): faixa uniforme na borda direita: 10% do quadro, cor RGB(217,200,163)
- Q37 (3:39): faixa uniforme na borda topo: 4% do quadro, cor RGB(226,212,182)
- Q37 (3:39): faixa uniforme na borda base: 6% do quadro, cor RGB(220,203,168)
- Q37 (3:39): faixa uniforme na borda direita: 10% do quadro, cor RGB(217,200,163)
- Q38 (3:45): faixa uniforme na borda base: 7% do quadro, cor RGB(18,29,56)
- Q38 (3:45): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(20,27,48)
- Q38 (3:45): faixa uniforme na borda direita: 25% do quadro, cor RGB(15,23,46)
- Q39 (3:51): faixa uniforme na borda base: 7% do quadro, cor RGB(18,29,56)
- Q39 (3:51): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(20,27,48)
- Q39 (3:51): faixa uniforme na borda direita: 25% do quadro, cor RGB(15,23,46)
- Q40 (3:57): faixa uniforme na borda base: 4% do quadro, cor RGB(24,33,59)
- Q41 (4:03): faixa uniforme na borda direita: 3% do quadro, cor RGB(15,23,46)
- Q42 (4:09): faixa uniforme na borda direita: 3% do quadro, cor RGB(15,23,46)
- Q43 (4:15): faixa uniforme na borda direita: 3% do quadro, cor RGB(15,23,46)
- Q44 (4:21): faixa uniforme na borda direita: 3% do quadro, cor RGB(15,23,46)
- Q45 (4:27): faixa uniforme na borda base: 7% do quadro, cor RGB(18,29,56)
- Q45 (4:27): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(19,27,48)
- Q45 (4:27): faixa uniforme na borda direita: 9% do quadro, cor RGB(15,23,46)
- Q46 (4:33): faixa uniforme na borda base: 7% do quadro, cor RGB(18,29,56)
- Q46 (4:33): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(19,26,48)
- Q46 (4:33): faixa uniforme na borda direita: 10% do quadro, cor RGB(15,23,46)
- Q47 (4:39): faixa uniforme na borda base: 7% do quadro, cor RGB(18,29,56)
- Q47 (4:39): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(19,26,47)
- Q47 (4:39): faixa uniforme na borda direita: 10% do quadro, cor RGB(15,23,46)
- Q48 (4:45): faixa uniforme na borda topo: 3% do quadro, cor RGB(227,213,184)
- Q48 (4:45): faixa uniforme na borda base: 5% do quadro, cor RGB(221,206,172)
- Q48 (4:45): faixa uniforme na borda direita: 15% do quadro, cor RGB(220,204,169)
- Q49 (4:51): faixa uniforme na borda topo: 3% do quadro, cor RGB(227,213,184)
- Q49 (4:51): faixa uniforme na borda base: 5% do quadro, cor RGB(221,206,172)
- Q49 (4:51): faixa uniforme na borda direita: 11% do quadro, cor RGB(220,204,169)
- Q62 (6:09): faixa uniforme na borda base: 7% do quadro, cor RGB(19,29,55)
- Q62 (6:09): faixa uniforme na borda direita: 24% do quadro, cor RGB(14,22,45)
- Q63 (6:15): faixa uniforme na borda base: 7% do quadro, cor RGB(19,29,55)
- Q63 (6:15): faixa uniforme na borda direita: 11% do quadro, cor RGB(14,22,45)
- Q65 (6:27): faixa uniforme na borda topo: 5% do quadro, cor RGB(11,19,35)
- Q65 (6:27): faixa uniforme na borda base: 7% do quadro, cor RGB(18,29,56)
- Q65 (6:27): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(15,24,45)
- Q65 (6:27): faixa uniforme na borda direita: 6% do quadro, cor RGB(14,23,46)
- Q66 (6:33): faixa uniforme na borda topo: 5% do quadro, cor RGB(11,19,35)
- Q66 (6:33): faixa uniforme na borda base: 7% do quadro, cor RGB(18,29,56)
- Q66 (6:33): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(15,24,45)
- Q66 (6:33): faixa uniforme na borda direita: 6% do quadro, cor RGB(14,23,46)
- Q67 (6:39): faixa uniforme na borda base: 7% do quadro, cor RGB(21,30,57)
- Q67 (6:39): faixa uniforme na borda direita: 33% do quadro, cor RGB(18,28,56)
- Q74 (7:21): faixa uniforme na borda topo: 5% do quadro, cor RGB(16,24,37)
- Q74 (7:21): faixa uniforme na borda base: 7% do quadro, cor RGB(10,20,40)
- Q74 (7:21): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(14,23,39)
- Q74 (7:21): faixa uniforme na borda direita: 11% do quadro, cor RGB(17,26,40)
- Q75 (7:27): faixa uniforme na borda topo: 5% do quadro, cor RGB(16,24,37)
- Q75 (7:27): faixa uniforme na borda base: 7% do quadro, cor RGB(10,20,40)
- Q75 (7:27): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(14,23,39)
- Q75 (7:27): faixa uniforme na borda direita: 11% do quadro, cor RGB(17,26,40)
- Q76 (7:33): faixa uniforme na borda base: 7% do quadro, cor RGB(18,28,56)
- Q76 (7:33): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(18,25,47)
- Q76 (7:33): faixa uniforme na borda direita: 9% do quadro, cor RGB(19,27,48)
- Q77 (7:39): faixa uniforme na borda base: 7% do quadro, cor RGB(18,28,56)
- Q77 (7:39): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(18,25,47)
- Q78 (7:45): faixa uniforme na borda base: 6% do quadro, cor RGB(17,25,43)
- Q79 (7:51): faixa uniforme na borda base: 6% do quadro, cor RGB(17,25,43)
- Q80 (7:57): faixa uniforme na borda base: 6% do quadro, cor RGB(17,25,42)
- Q81 (8:03): faixa uniforme na borda base: 7% do quadro, cor RGB(22,32,57)
- Q83 (8:15): faixa uniforme na borda base: 6% do quadro, cor RGB(13,20,40)
- Q83 (8:15): faixa uniforme na borda direita: 9% do quadro, cor RGB(13,20,40)
- Q84 (8:21): faixa uniforme na borda base: 7% do quadro, cor RGB(13,20,40)
- Q84 (8:21): faixa uniforme na borda direita: 11% do quadro, cor RGB(14,21,40)
- Q85 (8:27): faixa uniforme na borda base: 7% do quadro, cor RGB(13,20,40)
- Q85 (8:27): faixa uniforme na borda direita: 4% do quadro, cor RGB(15,21,40)
- Q87 (8:39): faixa uniforme na borda base: 6% do quadro, cor RGB(18,28,56)
- Q88 (8:45): faixa uniforme na borda base: 7% do quadro, cor RGB(18,28,56)
- Q92 (9:09): faixa uniforme na borda direita: 10% do quadro, cor RGB(131,101,71)
- Q93 (9:15): faixa uniforme na borda topo: 4% do quadro, cor RGB(157,118,76)
- Q93 (9:15): faixa uniforme na borda base: 7% do quadro, cor RGB(149,112,71)
- Q93 (9:15): faixa uniforme na borda direita: 20% do quadro, cor RGB(150,113,72)
- Q94 (9:21): faixa uniforme na borda topo: 4% do quadro, cor RGB(157,118,76)
- Q94 (9:21): faixa uniforme na borda base: 7% do quadro, cor RGB(149,112,71)
- Q94 (9:21): faixa uniforme na borda direita: 10% do quadro, cor RGB(150,113,72)
- Q95 (9:27): faixa uniforme na borda base: 7% do quadro, cor RGB(14,20,37)
- Q95 (9:27): faixa uniforme na borda direita: 11% do quadro, cor RGB(11,18,36)
- Q96 (9:33): faixa uniforme na borda base: 7% do quadro, cor RGB(14,20,37)
- Q96 (9:33): faixa uniforme na borda direita: 13% do quadro, cor RGB(11,18,36)
- Q97 (9:39): faixa uniforme na borda base: 22% do quadro, cor RGB(14,20,37)
- Q97 (9:39): faixa uniforme na borda direita: 9% do quadro, cor RGB(11,18,36)

## Quadros

Q01=0:03, Q02=0:09, Q03=0:15, Q04=0:21, Q05=0:27, Q06=0:33, Q07=0:39, Q08=0:45, Q09=0:51, Q10=0:57, Q11=1:03, Q12=1:09, Q13=1:15, Q14=1:21, Q15=1:27, Q16=1:33, Q17=1:39, Q18=1:45, Q19=1:51, Q20=1:57, Q21=2:03, Q22=2:09, Q23=2:15, Q24=2:21, Q25=2:27, Q26=2:33, Q27=2:39, Q28=2:45, Q29=2:51, Q30=2:57, Q31=3:03, Q32=3:09, Q33=3:15, Q34=3:21, Q35=3:27, Q36=3:33, Q37=3:39, Q38=3:45, Q39=3:51, Q40=3:57, Q41=4:03, Q42=4:09, Q43=4:15, Q44=4:21, Q45=4:27, Q46=4:33, Q47=4:39, Q48=4:45, Q49=4:51, Q50=4:57, Q51=5:03, Q52=5:09, Q53=5:15, Q54=5:21, Q55=5:27, Q56=5:33, Q57=5:39, Q58=5:45, Q59=5:51, Q60=5:57, Q61=6:03, Q62=6:09, Q63=6:15, Q64=6:21, Q65=6:27, Q66=6:33, Q67=6:39, Q68=6:45, Q69=6:51, Q70=6:57, Q71=7:03, Q72=7:09, Q73=7:15, Q74=7:21, Q75=7:27, Q76=7:33, Q77=7:39, Q78=7:45, Q79=7:51, Q80=7:57, Q81=8:03, Q82=8:09, Q83=8:15, Q84=8:21, Q85=8:27, Q86=8:33, Q87=8:39, Q88=8:45, Q89=8:51, Q90=8:57, Q91=9:03, Q92=9:09, Q93=9:15, Q94=9:21, Q95=9:27, Q96=9:33, Q97=9:39
