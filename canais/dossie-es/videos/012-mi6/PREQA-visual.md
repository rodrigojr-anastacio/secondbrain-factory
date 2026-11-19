# Pré-QA visual automático

- Alvo: `canais/dossie-es/videos/012-mi6/preqa` · 120 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.293 · `tools/preqa_visual.py`
- Resultado: **REPROVADO (há bloqueante)** · bloqueante 1 · alto 10 · médio 34 · baixo 31
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:10 | Q04 `315.png` | alto | valor_errado | Mapa da América Latina com geografia incoerente: o Brasil aparece duplicado (um à esquerda em tons marrons e outro recortado à direita em azul/amarelo), a América do Sul está desfigurada e o mapa parece ter uma segunda cópia da região no lado direito. Há pontos vermelhos soltos sem rótulo. |
| 0:10 | Q04 `315.png` | medio | fundo/faixa | Vincos do papel e cores chapadas por região (amarelo, azul, verde) sem lógica geográfica dão aspecto de emenda; na borda esquerda aparece a mesa de madeira e um objeto cortado no canto superior esquerdo. |
| 0:12 | Q05 `351.png` | medio | valor_errado | Rótulo 'PANAMA' sem acento (Panamá em espanhol) e o ponto vermelho está sobre a costa da Colômbia/Panamá, ligeiramente deslocado para o mar; o rótulo fica colado à borda do pino. Dúvida: pode ser o rótulo fijo intencional. |
| 0:20 | Q06 `615.png` | medio | elemento_fora | Mapa de fantasia (castelos, florestas) em vez de mapa real, com um contorno preto grosso desenhado de forma irregular e borrões de tinta; a mão com caneta tem anatomia estranha. Pode não corresponder ao tema da narração (América Latina). |
| 0:37 | Q07 `1103.png` | medio | anacronismo | Cena de Londres com carros tipo Ford T e cavalos e a placa 'EL MI6 · Nº 012'; o relógio do Big Ben e a arquitetura são plausíveis para a época, mas o título 'EL DIARIO' com 'Dossier · El MI6' em um vídeo cuja sequência anterior fala de Panamá/América Latina sugere troca de tema; confirme se é intencional. |
| 0:40 | Q09 `1187.png` | medio | outro | A imagem está muito ampliada e pixelada/borrada, parecendo um recorte de quadrinho. Enquadramento confuso: massa preta ocupa quase todo o centro e não dá para entender a cena. Há faixa preta fina atravessando a madeira no topo, perto da etiqueta 'LUGAR Y FECHA'. Pode ser estilo, mas parece defeito de recorte. |
| 0:40 | Q10 `1215.png` | medio | outro | Mesma imagem ampliada e pixelada de Q09, com enquadramento ilegível (massa preta central) e baixa resolução. Parece quase duplicado de Q09 no mesmo tempo (0:40), com só um leve zoom. Na dúvida entre estilo e defeito. |
| 1:27 | Q16 `2610.png` | alto | valor_errado | A legenda diz 'MÉXICO, 1917', mas a cena é um escritório europeu, com mapa da Europa na parede, e mostra Zimmermann (diplomata alemão) em Berlim. O lugar parece errado para o telegrama Zimmermann. Também há uma máquina de escrever e um telefone de época plausível, sem problema. |
| 1:50 | Q20 `3315.png` | medio | outro | A imagem parece ter dupla exposição: linhas fantasma de outro desenho (arco grande e curvas à direita, contornos sobrepostos sobre o salão e as pessoas) cruzam o quadro, com aspecto de crossfade mal resolvido ou camada duplicada. Pode ser transição, mas está bem visível em um quadro estático. |
| 2:10 | Q22 `3915.png` | medio | anacronismo | Cena de 1918: o skyline de Nova York tem arranha-céus com ar de Art Déco (espiral estilo Chrysler/Empire State, ~1930) e a Estátua da Liberdade em um pedestal estranho, o que é anacrônico. A bandeira vermelha com estrela no mastro do navio não corresponde a uma bandeira dos EUA. A faixa do topo apontada pelo sinal automático é só céu liso, falso positivo. |
| 3:20 | Q31 `6015.png` | bloqueante | moldura | Faixa preta chapada no topo (~7% do quadro) e, logo abaixo, uma linha de borda de papel/bege antes da ilustração começar. É moldura/letterbox de imagem de IA e precisa ser recortada. |
| 3:26 | Q32 `6172.png` | medio | anacronismo | A cena de fundo mostra um transatlântico em frente a arranha-céus tipo Chrysler/Empire State (Nova York, anos 30), enquanto o contexto do dossiê MI6 é a década de 1920 (Zinóviev). Em dúvida entre época e estilo; conferir se o ano da cena bate com a narrativa. |
| 3:26 | Q32 `6172.png` | medio | elemento_fora | A placa de capítulo cobre a chaminé e boa parte do navio, e o carimbo 'CLASIFICADO' invade a borda da placa. Pode ser a composição intencional da placa, mas o conjunto fica apertado sobre a ilustração. |
| 3:26 | Q33 `6179.png` | medio | anacronismo | Navio em Nova York com bandeiras vermelhas no mastro e na proa e um rebocador com bandeira vermelha/azul. As bandeiras são pequenas e indefinidas, e podem ser anacrônicas ou inadequadas para 1940. Dúvida entre estilo e defeito. |
| 3:40 | Q35 `6615.png` | medio | anacronismo | A bandeira atrás da mulher é desbotada e indefinida, com um emblema vermelho/branco ambíguo. Não dá para saber qual país é, o que pode ser bandeira inventada. Confirmar se faz sentido para a cena. |
| 4:22 | Q40 `7863.png` | medio | valor_errado | Mapa: Bermudas fica no Atlântico, perto da costa leste dos EUA, mas aparece mais ao centro. A rota Nova York–Bermudas–Londres parece plausível, mas a ilha desenhada é grande e irregular. Há também uma emenda/vinco vertical e horizontal no centro do mapa, de textura de papel dobrado, que pode ser estilo intencional. |
| 5:10 | Q49 `9315.png` | medio | texto_inventado | O documento segurado em primeiro plano tem texto borrado/ilegível com assinatura e carimbo vermelho. É texto falso da IA, mas desfocado e de pouco destaque, parecendo intencional. |
| 5:30 | Q53 `9915.png` | alto | fundo/faixa | Faixas laterais chapadas e escurecidas nas bordas esquerda e direita (a direita ocupa cerca de 15% do quadro), com aspecto de margem/moldura. A cena parece uma imagem recortada e centralizada, com vinheta lateral que não é do estilo. |
| 5:30 | Q53 `9915.png` | alto | valor_errado | A legenda do personagem diz 'ELÍAS BELMO', enquanto o Q54 mostra 'ELÍAS BELMONTE'. O nome está cortado ou errado. |
| 5:31 | Q54 `9934.png` | alto | fundo/faixa | Faixas laterais chapadas e escuras nas bordas esquerda e direita (a direita ocupa cerca de 16% do quadro), indicando moldura/margem de imagem de IA em volta da cena. |
| 5:50 | Q56 `10515.png` | medio | texto_inventado | A placa da estação ('VIDEPIAN...') e o letreiro na lateral da locomotiva ('DEUTSCHE REICHSBAHN...') têm letras falsas ou ilegíveis escritas pela IA. A locomotiva é identificada como alemã, o que pode ser anacrônico ou fora de lugar. |
| 6:20 | Q60 `11415.png` | medio | texto_encavalado | O carimbo "CLASIFICADO" avança sobre a borda superior direita da placa "EL MAPA" e sobrepõe a aba. Parece ser o estilo da placa de capítulo, mas o carimbo encosta na etiqueta e no rosto do personagem. Se a sobreposição não for intencional, é preciso ajustar. |
| 6:21 | Q61 `11426.png` | medio | texto_encavalado | Mesma placa de capítulo do Q60, com o carimbo "CLASIFICADO" sobre a borda da placa e perto do rosto. Vale conferir se a sobreposição é intencional. |
| 6:21 | Q62 `11433.png` | medio | texto_encavalado | Mesma placa de capítulo do Q60, com o carimbo "CLASIFICADO" sobre a borda da placa e perto do rosto. Vale conferir se a sobreposição é intencional. |
| 7:36 | Q71 `13689.png` | medio | elemento_fora | A placa de capítulo ('EXPEDIENTE 8', 'DOSSIER · EL MI6 · Nº 012', carimbo 'CLASIFICADO') mostra 'EL MI6' enquanto o contexto do canal é dossie-es sobre CIA/FBI/Mossad. Pode ser o tema deste vídeo, mas vale conferir se o nome e o número do dossiê estão corretos. O carimbo 'CLASIFICADO' sobrepõe a borda da placa, o que parece intencional. |
| 7:40 | Q72 `13815.png` | medio | texto_inventado | A fuselagem do avião tem uma marca circular ilegível no lado direito (insígnia inventada pela IA, parecida com 'HH'). Pequena, mas é uma marca nacional inventada e anacrônica. Em 1941 o Brasil usaria outro tipo de marca, ou nenhuma. |
| 7:50 | Q73 `14115.png` | medio | anacronismo | A insígnia oval na asa direita traz símbolos inventados ('HHH'), que parecem uma marca falsa. O avião também não identifica um país claro. Vale pedir uma asa sem marcação. |
| 8:00 | Q75 `14415.png` | alto | texto_inventado | A carta sobre a mesa tem linhas de texto manuscrito ilegível e uma assinatura em garranchos, inventados pela IA. Estão bem visíveis em primeiro plano. O rótulo ou o texto precisa ser coberto ou removido. |
| 8:10 | Q76 `14715.png` | medio | fundo/faixa | O sinal automático acusa faixa uniforme no topo, de 8% do quadro, em RGB(131,145,150). Visualmente parece céu liso e degradê da cena, sem emenda clara. Há dúvida entre estilo e defeito, então vale conferir a borda superior. |
| 8:20 | Q77 `15015.png` | alto | texto_inventado | A carta em primeiro plano tem texto falso ilegível, em linhas de garranchos. É o mesmo problema de Q75, só que com enquadramento mais fechado e o texto ainda mais evidente. |
| 9:10 | Q84 `16515.png` | medio | texto_inventado | A folha em primeiro plano tem texto borrado e falso. A placa do mapa à esquerda também tem letras ilegíveis. Os mapas-múndi na parede trazem continentes pouco precisos, mas sem rótulos legíveis. |
| 9:42 | Q88 `17473.png` | medio | fundo/faixa | O sinal automático indica faixa uniforme no topo (17%, RGB 49,57,59). Visualmente é o céu cinza-escuro liso atrás do navio, que parece fazer parte da cena. Conferir se não é um bloco chapado sem gradiente ou textura. |
| 9:46 | Q89 `17572.png` | alto | anacronismo | Cena de Portsmouth 1956 com o encouraçado ao fundo e bandeirinhas de sinalização inventadas (vermelha/branca, dinamarquesa-like). Dois homens acenando, o da direita barbudo, não parece Khrushchev nem Bulganin. A legenda 'NIKITA JRUSCHOV' pode estar associada à pessoa errada. Verificar a identidade dos personagens. |
| 9:50 | Q90 `17715.png` | medio | anacronismo | Navio de guerra com bandeirinhas vermelhas e um veleiro antigo ao fundo (galeão), mistura de épocas no porto de 1956. Marinheiros cortados na borda inferior, enquadramento normal. |
| 10:20 | Q94 `18615.png` | medio | anacronismo | Ônibus de dois andares preto à direita, com formato pouco britânico dos anos 50 (Routemaster é de 1956, mas o preto destoa). O prédio é inventado, sem identificação do Almirantado. Dúvida entre estilo e erro. Faixa superior uniforme é só céu liso. |
| 10:50 | Q99 `19515.png` | medio | texto_inventado | A folha de papel tem texto borrado ilegível e uma faixa vermelha no topo, gerados pela IA. Está desfocado de propósito e dá para ler como documento, mas pode ser lido como texto falso. Também há mapas antigos com linhas falsas nos cantos inferiores. Dúvida entre estilo e defeito. |
| 11:20 | Q104 `20415.png` | medio | anacronismo | O caça no pátio tem marcas triangulares vermelhas na fuselagem e na entrada de ar que parecem insígnias inventadas. Podem ser lidas como marcação da Argentina ou como marcação falsa, sem bandeira definida. Se for a Fuerza Aérea Argentina (Mirage/Dagger), confirmar a insígnia. |
| 11:34 | Q105 `20835.png` | medio | anacronismo | Escritório de Lawrence Freedman traz monitor CRT e impressora de escritório modernos; pode ser coerente com a época do personagem, mas vale confirmar o período da cena. Mapa sobre a mesa tem rabiscos ilegíveis (não são texto legível, detalhe pequeno). |
| 11:40 | Q106 `21015.png` | medio | anacronismo | Soldado de uniforme verde-oliva e homem com braçadeira vermelha no armazém: uniforme e braçadeira ambíguos, podem sugerir facção/época errada. Dúvida entre estilo e defeito. |
| 12:04 | Q109 `21710.png` | medio | elemento_fora | Placa de título 'EL INFORME' cobre completamente o rosto/olhos do personagem de fundo (cobre boca e nariz, só olhos visíveis) e o selo 'CLASIFICADO' sobrepõe a testa; sobreposição de elementos incômoda, mas pode ser intencional do cartão de capítulo. |
| 12:20 | Q112 `22215.png` | alto | texto_inventado | Placas na parede do bunker (esquerda, com texto miúdo ilegível, e direita com mancha vermelha/escorrida) trazem letras inventadas pela IA; pequenas mas visíveis. |
| 12:40 | Q114 `22815.png` | alto | valor_errado | Mapa das Américas com colorização incoerente: a região esquerda/México em azul e a faixa verde-oliva no Caribe e no Atlântico norte cortam o continente em blocos retangulares (por causa das dobras). A América do Sul está parcialmente em marrom e o Brasil/Amazônia em amarelo, de modo que a geografia política parece errada. Há também pontos vermelhos soltos no oceano e na terra, sem sentido. |
| 12:50 | Q115 `23112.png` | medio | fundo/faixa | Faixa uniforme cinza escuro na base (cerca de 8% do quadro, RGB 50,51,52), abaixo do laptop. Pode ser só a mesa desfocada do cenário, mas confirme que não é uma faixa chapada. O texto na tela cobre a imagem do laptop de forma intencional. |
| 12:51 | Q116 `23119.png` | medio | fundo/faixa | Mesma faixa uniforme cinza escuro na base (cerca de 7%, RGB 50,51,51) abaixo do laptop; provavelmente é a mesa, mas confira se não é faixa chapada. |
| 13:00 | Q117 `23415.png` | medio | moldura | Faixa escura/preta na borda inferior (cerca de 3-4% da altura), com padrão de balaustrada. Pode ser a grade da galeria da cena, mas parece moldura ou letterbox de imagem de IA. Confirme com o detector de bordas. |

31 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q07 (0:37): faixa uniforme na borda topo: 4% do quadro, cor RGB(59,63,64)
- Q18 (1:40): faixa uniforme na borda topo: 12% do quadro, cor RGB(85,100,100)
- Q22 (2:10): faixa uniforme na borda topo: 6% do quadro, cor RGB(148,149,145)
- Q31 (3:20): faixa preta na borda topo: 7% do quadro
- Q41 (4:25): faixa uniforme na borda topo: 3% do quadro, cor RGB(34,44,49)
- Q50 (5:20): faixa uniforme na borda topo: 4% do quadro, cor RGB(65,71,66)
- Q53 (5:30): faixa uniforme na borda esquerda: 4% do quadro, cor RGB(73,67,59)
- Q53 (5:30): faixa uniforme na borda direita: 15% do quadro, cor RGB(73,66,59)
- Q54 (5:31): faixa uniforme na borda esquerda: 4% do quadro, cor RGB(73,67,59)
- Q54 (5:31): faixa uniforme na borda direita: 16% do quadro, cor RGB(73,66,59)
- Q70 (7:30): faixa uniforme na borda topo: 8% do quadro, cor RGB(72,85,92)
- Q72 (7:40): faixa uniforme na borda topo: 5% do quadro, cor RGB(53,65,70)
- Q76 (8:10): faixa uniforme na borda topo: 8% do quadro, cor RGB(131,145,150)
- Q88 (9:42): faixa uniforme na borda topo: 17% do quadro, cor RGB(49,57,59)
- Q89 (9:46): faixa uniforme na borda topo: 4% do quadro, cor RGB(93,102,99)
- Q94 (10:20): faixa uniforme na borda topo: 7% do quadro, cor RGB(116,124,126)
- Q95 (10:30): faixa uniforme na borda base: 3% do quadro, cor RGB(86,98,101)
- Q103 (11:10): faixa uniforme na borda topo: 4% do quadro, cor RGB(34,43,49)
- Q104 (11:20): faixa uniforme na borda topo: 6% do quadro, cor RGB(70,83,90)
- Q115 (12:50): faixa uniforme na borda base: 8% do quadro, cor RGB(50,51,52)
- Q116 (12:51): faixa uniforme na borda base: 7% do quadro, cor RGB(50,51,51)

## Quadros

Q01=0:00, Q02=0:01, Q03=0:01, Q04=0:10, Q05=0:12, Q06=0:20, Q07=0:37, Q08=0:37, Q09=0:40, Q10=0:40, Q11=0:50, Q12=1:10, Q13=1:20, Q14=1:24, Q15=1:24, Q16=1:27, Q17=1:30, Q18=1:40, Q19=1:46, Q20=1:50, Q21=2:00, Q22=2:10, Q23=2:25, Q24=2:25, Q25=2:30, Q26=2:32, Q27=2:40, Q28=2:50, Q29=3:02, Q30=3:10, Q31=3:20, Q32=3:26, Q33=3:26, Q34=3:30, Q35=3:40, Q36=3:50, Q37=3:57, Q38=4:00, Q39=4:10, Q40=4:22, Q41=4:25, Q42=4:25, Q43=4:28, Q44=4:30, Q45=4:46, Q46=4:50, Q47=4:50, Q48=5:00, Q49=5:10, Q50=5:20, Q51=5:20, Q52=5:22, Q53=5:30, Q54=5:31, Q55=5:37, Q56=5:50, Q57=5:57, Q58=6:00, Q59=6:10, Q60=6:20, Q61=6:21, Q62=6:21, Q63=6:30, Q64=6:37, Q65=6:40, Q66=6:46, Q67=7:00, Q68=7:10, Q69=7:20, Q70=7:30, Q71=7:36, Q72=7:40, Q73=7:50, Q74=7:53, Q75=8:00, Q76=8:10, Q77=8:20, Q78=8:37, Q79=8:37, Q80=8:40, Q81=8:41, Q82=8:50, Q83=9:00, Q84=9:10, Q85=9:20, Q86=9:30, Q87=9:40, Q88=9:42, Q89=9:46, Q90=9:50, Q91=9:53, Q92=10:00, Q93=10:00, Q94=10:20, Q95=10:30, Q96=10:40, Q97=10:46, Q98=10:46, Q99=10:50, Q100=11:00, Q101=11:00, Q102=11:03, Q103=11:10, Q104=11:20, Q105=11:34, Q106=11:40, Q107=11:50, Q108=12:00, Q109=12:04, Q110=12:04, Q111=12:10, Q112=12:20, Q113=12:30, Q114=12:40, Q115=12:50, Q116=12:51, Q117=13:00, Q118=13:10, Q119=13:20, Q120=13:30
