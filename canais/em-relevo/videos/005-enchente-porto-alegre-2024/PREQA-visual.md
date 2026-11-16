# Pré-QA visual automático

- Alvo: `pesquisa/canal-clima-2026-11/longo-05/preqa` · 104 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.232 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 6 · médio 29 · baixo 18
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:23 | Q05 `690.png` | medio | texto_encavalado | A faixa de título 'A CHUVA MAIS PESADA CAIU NA SERRA. QUEM AFUNDOU FOI' fica acima da legenda 'Quem afundo' e repete o mesmo trecho. Há dúvida se é intencional: o texto parece em animação, mas os dois textos se duplicam e pesam na leitura. |
| 0:26 | Q06 `771.png` | medio | elemento_fora | Atrás da foto, o rótulo 'PORTO ALEGRE (RS)' do mapa aparece escurecido e vaza por trás da faixa navy 'PESSOAS ATINGIDAS'. O cilindro do mapa também aparece no canto superior esquerdo, perto do rótulo 'PORTO ALEGRE (RS) · MAIO DE 2024'. É resíduo da cena anterior durante o crossfade e pode estar sujando a composição. |
| 0:32 | Q07 `960.png` | medio | elemento_fora | Crossfade da foto do aeroporto com o mapa: o pino vermelho, o cilindro e o rótulo ficam sobrepostos à foto, e a legenda coral 'AEROPORTO SALGADO FILHO · 5 MAI 2024' fica pouco legível. Provavelmente é transição, mas o quadro está confuso. |
| 0:41 | Q09 `1230.png` | medio | elemento_fora | Um dos cilindros (Porto Alegre) tem uma faixa translúcida clara acima dele, como um fantasma ou resíduo de animação. Pode ser a animação de crescimento do cilindro, mas parece estranho. Além disso, a base do cilindro de Caxias do Sul está desalinhada com o topo. |
| 1:26 | Q16 `2580.png` | medio | elemento_fora | A nuvem 3D enorme cobre os rótulos 'UMIDADE DO NORTE' e 'BLOQUEIO DE AR QUENTE' e a faixa tracejada no topo. Os rótulos ficam amontoados e quase encavalados sobre as esferas, o que prejudica a leitura. Pode ser intencional como esquema. |
| 1:44 | Q19 `3120.png` | medio | valor_errado | No painel 'O TAMANHO DA CHUVA', o bloco azul de '3 MESES DE CHUVA' aparece sem valor ou rótulo numérico. O espaço à direita de '11 DIAS' está vazio. Pode ser animação ainda em andamento. Também há dúvida se a ausência de barra para '11 DIAS' é intencional. |
| 1:48 | Q20 `3253.png` | medio | texto_encavalado | A etiqueta coral 'ONDE NASCEM OS RIOS' encosta no pino vermelho e quase encosta na placa navy 'CAXIAS DO SUL'. As barras azuis da chuva passam por trás das etiquetas. Ainda dá para ler, mas fica apertado. |
| 1:53 | Q21 `3390.png` | alto | texto_encavalado | A placa navy 'CAXIAS DO SUL' cobre o fim da etiqueta coral 'ONDE NASCEM OS RIOS', e o texto fica cortado em 'ONDE NASCEM OS'. O pino vermelho também fica por cima da etiqueta. |
| 2:47 | Q30 `5010.png` | medio | texto_encavalado | A placa coral '+3 M ACIMA DE 1941' fica por cima do topo do cilindro 3D (régua) e cobre parte dele. O cilindro também parece cortado/deslocado atrás da placa. Pode ser estilo, mas atrapalha a leitura do mostrador. |
| 3:14 | Q35 `5820.png` | medio | valor_errado | A legenda diz 'Uma bacia de cerca de 85 mil km' e termina em 'km' com o cursor, sem o ²; o título grande mostra '~85 MIL km²'. Pode ser só a digitação em andamento, mas vale conferir. Os pontos brancos sobre os rios também parecem excessivos e poluem o mapa, o que pode ser estilo. |
| 3:47 | Q41 `6815.png` | alto | texto_encavalado | No medidor, o valor "~1.200 M³/S" se sobrepõe ao rótulo "MAIORES JÁ MEDIDAS" e ao ponto/ponteiro da agulha. O texto fica apertado e atrapalha a leitura. |
| 3:50 | Q42 `6900.png` | alto | texto_encavalado | O valor "~1.200 M³/S" encosta no rótulo "MAIORES JÁ MEDIDAS" e no pino da agulha, no medidor à direita. |
| 3:50 | Q42 `6900.png` | medio | texto_cortado | A linha "CAÍ, SINOS, GRAVATAÍ" termina cortada no fim, com o "Í" final incompleto. Pode ser um corte de máscara ou de animação. |
| 3:59 | Q43 `7170.png` | alto | texto_encavalado | A palavra "ACIMA" em coral fica em cima do pino da agulha e da linha vermelha do ponteiro. O rótulo "MAIO DE 2024" também está colado. Fica mal legível e visualmente confuso. |
| 3:59 | Q43 `7170.png` | medio | texto_cortado | A linha "CAÍ, SINOS, GRAVATAÍ" continua cortada no fim, com o "Í" incompleto. |
| 3:59 | Q43 `7170.png` | medio | valor_errado | O medidor mostra "ACIMA" com a agulha apontando para baixo/fora do arco, e não sobre a escala. Pode ser uma animação intencional, mas parece estranho. |
| 5:07 | Q56 `9202.png` | medio | fundo/faixa | O sinal automático acusou faixa uniforme na borda direita (RGB 19,30,41, ~6% do quadro). Visualmente é o oceano escuro do mapa, que parece escurecimento natural do fundo, sem emenda nítida. Na dúvida entre estilo e defeito, convém conferir se há faixa chapada ou corte de textura na borda direita. |
| 5:29 | Q60 `9870.png` | medio | elemento_fora | O painel bege do gráfico cobre boa parte da foto de Pelotas e esconde o canto esquerdo dela. A legenda 'e causou alagamentos em Pelotas...' parece vir da digitação, então é só o conjunto que fica carregado. Não há faixa de cor errada: a faixa escura na borda esquerda é o fundo do mapa. |
| 5:47 | Q63 `10410.png` | alto | texto_cortado | A faixa 'MAIS DE UM MÊS PARA VOLTAR AOS 3 M...' é cortada pela foto do Mercado Público, que fica sobreposta ao texto. A frase termina em 'AOS 3 M' e perde o resto. O título 'GUAÍBA: 4,7 METROS' também encosta na foto. |
| 5:50 | Q64 `10497.png` | medio | outro | O esquema 'O SISTEMA DE PROTEÇÃO CONTRA CHEIAS' mostra só 'LAGO GUAÍBA' e 'CIDADE', sem nenhum elemento de proteção (diques, comportas) e com grande área vazia. Pode ser o início da animação, mas se não for, o esquema fica sem conteúdo. |
| 6:32 | Q71 `11760.png` | medio | texto_encavalado | No esquema, o rótulo coral 'COMPORTA · AV. SERTÓRIO · 3 MAI' fica sobre a linha ciano do rio e perto do círculo ciano; 'NAVEGANTES' fica logo abaixo. Os textos ficam apertados e a leitura é um pouco prejudicada. Também não há legenda no quadro, o que pode ser transição. |
| 6:33 | Q72 `11789.png` | medio | texto_encavalado | O rótulo coral 'COMPORTA · AV. SERTÓRIO · 3 MAI' cruza a linha ciano do rio, e 'NAVEGANTES' fica colado a ele. A leitura fica prejudicada. |
| 6:41 | Q73 `12030.png` | medio | texto_encavalado | No esquema, o rótulo "SEM ENERGIA · INUNDADAS" encosta/sobrepõe o rótulo "CIDADE" no canto inferior direito do painel, e a leitura fica prejudicada. |
| 6:50 | Q74 `12300.png` | medio | texto_encavalado | Mesma sobreposição no painel: "INUNDADAS" colide com "CIDADE". |
| 6:51 | Q75 `12332.png` | medio | texto_encavalado | "INUNDADAS" colide com "CIDADE" no painel. Além disso, "SARANDI" e "NAVEGANTES" ficam muito próximos, quase encostando. |
| 6:59 | Q76 `12570.png` | medio | texto_encavalado | "INUNDADAS" sobrepõe "CIDADE" no painel. Rótulos "SARANDI", "COMPORTA", "NAVEGANTES" e "CASA DE BOMBAS Nº 10" ficam apertados na região esquerda. |
| 7:03 | Q77 `12681.png` | medio | texto_encavalado | "INUNDADAS" colide com "CIDADE" no painel. |
| 7:08 | Q78 `12840.png` | medio | texto_encavalado | "INUNDADAS" colide com "CIDADE" no painel. |
| 7:17 | Q79 `13110.png` | alto | texto_encavalado | A etiqueta coral "WORLD WEATHER ATTRIBUTION" fica por cima da legenda do painel ("ESQUEMA FORA DE ESCALA · POSIÇÕES ILUSTRATIVAS"), cortando-a. A caixa "FALHA DESDE ~4,5 M" cobre a borda inferior do painel. "INUNDADAS" colide com "CIDADE". |
| 7:22 | Q80 `13260.png` | medio | fundo/faixa | Sem mapa e com fundo bege liso com listras horizontais; só o título ocupa a tela, deixando uma grande área vazia. Pode ser o painel de papel intencional, mas o sinal de faixa na borda superior (RGB 199,176,130) tem de ser conferido. Na dúvida entre estilo e defeito. |
| 8:41 | Q94 `15631.png` | medio | elemento_fora | O painel de papel bege 'E O CLIMA? · WORLD WEATHER ATTRIBUTION · 03/06/2024' está vazio no centro, só com título e rodapé. Pode ser o 1º quadro do bloco, quando a animação começa em branco, então é provavelmente intencional. Se o quadro aparecer com tempo suficiente, vale confirmar. |
| 9:11 | Q99 `16521.png` | medio | elemento_fora | No painel ilustrativo, o rótulo "DIQUES · 68 KM" fica sobre a linha tracejada e o primeiro marcador amarelo, o que prejudica a leitura. O "MURO DA MAUÁ" também encosta na linha de diques. |
| 9:14 | Q100 `16620.png` | medio | texto_encavalado | No painel, "DIQUES · 68 KM" está sobreposto à linha tracejada e ao marcador amarelo, com leitura fraca. "MURO DA MAUÁ" também toca os marcadores. |
| 9:32 | Q102 `17160.png` | medio | texto_encavalado | A caixa de título "POR Q" cobre a parte superior dos rios ciano e do mapa. Pode ser só a animação de digitação, mas na versão final cobriria parte do dado. Há também um pequeno traço preto solto à esquerda, perto de x=240, y=387, sem função aparente. |
| 9:32 | Q103 `17168.png` | medio | texto_encavalado | A caixa "POR QUE O" cobre a ponta superior da rede de rios. Há um pequeno traço preto solto no mapa, perto de x=240, y=387. |

18 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q56 (5:07): faixa uniforme na borda direita: 6% do quadro, cor RGB(19,30,41)
- Q60 (5:29): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(51,45,39)
- Q61 (5:36): faixa uniforme na borda topo: 4% do quadro, cor RGB(199,176,130)
- Q62 (5:38): faixa uniforme na borda topo: 4% do quadro, cor RGB(199,176,130)
- Q63 (5:47): faixa uniforme na borda topo: 4% do quadro, cor RGB(199,176,130)
- Q80 (7:22): faixa uniforme na borda topo: 4% do quadro, cor RGB(199,176,130)
- Q81 (7:26): faixa uniforme na borda topo: 4% do quadro, cor RGB(199,176,130)
- Q82 (7:35): faixa uniforme na borda topo: 4% do quadro, cor RGB(199,176,130)
- Q84 (7:44): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(25,25,17)

## Quadros

Q01=0:01, Q02=0:05, Q03=0:13, Q04=0:14, Q05=0:23, Q06=0:26, Q07=0:32, Q08=0:37, Q09=0:41, Q10=0:47, Q11=0:50, Q12=0:59, Q13=1:00, Q14=1:08, Q15=1:17, Q16=1:26, Q17=1:33, Q18=1:35, Q19=1:44, Q20=1:48, Q21=1:53, Q22=2:02, Q23=2:05, Q24=2:11, Q25=2:20, Q26=2:22, Q27=2:29, Q28=2:37, Q29=2:38, Q30=2:47, Q31=2:54, Q32=2:56, Q33=3:04, Q34=3:05, Q35=3:14, Q36=3:18, Q37=3:23, Q38=3:32, Q39=3:32, Q40=3:41, Q41=3:47, Q42=3:50, Q43=3:59, Q44=4:05, Q45=4:08, Q46=4:17, Q47=4:22, Q48=4:26, Q49=4:34, Q50=4:35, Q51=4:43, Q52=4:44, Q53=4:53, Q54=4:56, Q55=5:02, Q56=5:07, Q57=5:11, Q58=5:20, Q59=5:21, Q60=5:29, Q61=5:36, Q62=5:38, Q63=5:47, Q64=5:50, Q65=5:56, Q66=6:05, Q67=6:07, Q68=6:14, Q69=6:23, Q70=6:23, Q71=6:32, Q72=6:33, Q73=6:41, Q74=6:50, Q75=6:51, Q76=6:59, Q77=7:03, Q78=7:08, Q79=7:17, Q80=7:22, Q81=7:26, Q82=7:35, Q83=7:42, Q84=7:44, Q85=7:53, Q86=7:56, Q87=8:02, Q88=8:02, Q89=8:11, Q90=8:20, Q91=8:23, Q92=8:29, Q93=8:38, Q94=8:41, Q95=8:47, Q96=8:56, Q97=8:56, Q98=9:05, Q99=9:11, Q100=9:14, Q101=9:23, Q102=9:32, Q103=9:32, Q104=9:41
