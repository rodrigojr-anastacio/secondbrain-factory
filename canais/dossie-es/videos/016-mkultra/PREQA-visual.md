# Pré-QA visual automático

- Alvo: `canais/dossie-es/videos/016-mkultra/preqa` · 120 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.279 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 5 · médio 25 · baixo 36
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:28 | Q06 `825.png` | alto | valor_errado | No mapa, o marcador de Huautla fica sobre o litoral do Golfo/Istmo, longe da Sierra Mazateca (Oaxaca), e quase colado à Cidade do México. O rótulo 'HUAUTLA' encosta no rótulo 'CIUDAD DE MÉXICO' e o ponto de Tegucigalpa parece deslocado. |
| 0:42 | Q08 `1260.png` | medio | texto_encavalado | O carimbo 'CLASIFICADO' sobrepõe a borda superior direita da placa de título e fica inclinado. O 'Nº 016' do dossiê pode estar errado para o primeiro episódio. Parece ser estilo intencional de placa de capítulo, mas a sobreposição merece conferência. |
| 0:42 | Q09 `1267.png` | medio | sobreposicao | A placa 'EXPEDIENTE 1' e o carimbo 'CLASIFICADO' ficam muito perto e encostam na placa principal; o carimbo vermelho cobre parte da borda superior direita. Dá para ler tudo, então é só estética. Pode ser o estilo intencional de placa de capítulo. |
| 0:45 | Q10 `1350.png` | alto | elemento_fora | O texto 'WASHINGTON, 1952' aparece duas vezes, na placa superior esquerda e na inferior esquerda (HUD duplicado). Além disso, os rótulos estão em inglês num canal em espanhol ('WASHINGTON' é a grafia em inglês, em espanhol seria 'Washington' igual, mas o rótulo inferior repete a informação). |
| 0:55 | Q11 `1650.png` | medio | anacronismo | A bandeira dos EUA à direita mostra estrelas em fileiras irregulares e muitas listras; em 1952 eram 48 estrelas. Não dá para contar, mas parece haver mais fileiras de estrelas do que o correto. Dúvida de anacronismo. |
| 1:15 | Q13 `2250.png` | medio | texto_inventado | O documento tem texto borrado ilegível, um selo vermelho com símbolo de águia e letras falsas. Está desfocado, mas o selo redondo no canto superior direito tem letras inventadas ainda visíveis. |
| 1:19 | Q14 `2360.png` | alto | elemento_fora | Placa duplicada: 'MÉXICO, 1953' no topo esquerdo e 'CIUDAD DE MÉXICO' embaixo à esquerda, repetindo a informação de lugar (HUD duplicado). A placa inferior cobre parte dos pedestres e da calçada. |
| 1:46 | Q18 `3190.png` | medio | elemento_fora | A placa de capítulo ('EXPEDIENTE 2 / DOSSIER · MKULTRA · Nº 016 / LA GRANJA') cobre boa parte do centro da cena e o carimbo 'CLASIFICADO' ultrapassa a borda superior direita da placa. Provavelmente é design intencional do canal, mas vale confirmar a sobreposição do carimbo e se o número 'Nº 016' está correto. |
| 2:45 | Q27 `4950.png` | medio | elemento_fora | A placa de capítulo 'LA VELADA' cobre o rosto e a cabeça da personagem durante o movimento de câmera; só ficam visíveis o cesto, o xale e a blusa. Se for só uma fase da animação, é aceitável; o ideal é conferir se o rosto não fica escondido por muito tempo. |
| 3:29 | Q32 `6267.png` | medio | elemento_fora | A placa 'LA BOLSA' cobre a cabeça da personagem de casaco no centro-esquerda (só aparecem o corpo e o livro). A cabeça cortada pela placa parece um defeito de enquadramento. |
| 3:45 | Q35 `6750.png` | medio | texto_inventado | O cheque no centro tem linhas de texto borradas e ilegíveis (borrões no lugar de escrita) e um selo com fachada de templo. Parece intencional como texto desfocado, mas o borrão parece 'texto falso' da IA e pode ser lido como defeito; confirmar se foi proposital. |
| 4:31 | Q41 `8122.png` | medio | texto_encavalado | A placa de capítulo cobre o rosto da mulher e o corpo dos pedestres no centro da cena. O carimbo 'CLASIFICADO' invade a borda superior da placa. Pode ser estilo intencional de placa de capítulo, mas a sobreposição é pesada. |
| 5:31 | Q48 `9944.png` | medio | fundo/faixa | O fundo é quase preto, com vinheta marrom-escura, e as capas ocupam só a parte inferior. A capa #1 está cortada pela borda inferior e há grande espaço vazio no topo. O contexto sugere cena final de série com vinheta intencional, mas a composição desequilibrada e os sinais automáticos de faixa escura nas bordas deixam dúvida entre estilo e defeito. |
| 5:33 | Q49 `9994.png` | medio | texto_inventado | Nas capas de revista, o subtítulo 'HISTORIAS REALES DE ESPIONAJE QUE NO ESTÁN EN EL CANAL' está parcialmente coberto/ilegível nas capas #2 e #3, e os textos pequenos das capas (caixas de legenda, 'EXPEDIENTE') são letra miúda de IA. Pode ser estilo de mockup; dúvida entre estilo e defeito. |
| 5:39 | Q51 `10184.png` | medio | fundo/faixa | Faixa marrom chapada na base (~14%) simulando mesa e área grande e vazia à direita do fundo azul listrado; o pôster está só à esquerda, deixando a composição desbalanceada. Provavelmente é o início de uma animação, mas vale confirmar. |
| 5:45 | Q52 `10350.png` | medio | texto_encavalado | A placa 'ENLACE EN LA DESCRIPCIÓN · COMENTARIO FIJADO' cobre boa parte do segundo pôster e parte do laptop, e as setas vermelhas descem sobre o laptop. A leitura da placa está OK, mas o elemento atrás fica muito tapado. |
| 6:48 | Q63 `12241.png` | medio | texto_encavalado | A placa de capítulo 'LOS PUROS' cobre as mãos e a caixa de charutos, que são o foco da cena, e o carimbo 'CLASIFICADO' cobre o rosto/óculos do homem à direita. É placa de título intencional, mas tapa bastante a ilustração. |
| 6:48 | Q64 `12249.png` | medio | texto_encavalado | Mesma placa 'LOS PUROS' do Q63, ainda na animação: tapa a caixa e as mãos, e o carimbo 'CLASIFICADO' cobre o rosto do homem à direita. Se for a mesma tela em duas fases da entrada, só registrar a dúvida de composição. |
| 7:35 | Q69 `13650.png` | medio | anacronismo | O orador é um homem barbudo de farda verde-oliva e quepe, claramente um líder revolucionário cubano. É um personagem real e reconhecível, e o contexto do vídeo (MKUltra) pode exigir cuidado. Também há dúvida se o prédio colonial e a multidão correspondem ao cenário esperado. |
| 7:42 | Q70 `13845.png` | medio | anacronismo | O carro verde em primeiro plano parece um Chevrolet Impala de 1964-65. Para uma cena de 1963 isso é levemente adiantado, mas aceitável. Dúvida de época. |
| 9:25 | Q84 `16950.png` | medio | anacronismo | Bandeira dos EUA na esquerda e mapa dos EUA na parede. A bandeira parece ter faixas e estrelas plausíveis, mas é pequena e as estrelas estão aglomeradas. Verificar se o número de estrelas e o mapa dos EUA (com Alasca) combinam com a época do vídeo (anos 50, possivelmente antes de 1959). |
| 10:25 | Q92 `18750.png` | alto | anacronismo | O especialista (Alfred McCoy) usa um laptop moderno na mesa. A cena remete à década de 1970, então o laptop é anacrônico. |
| 10:52 | Q97 `19575.png` | medio | texto_encavalado | A placa de capítulo 'EL CURSO' cobre quase todo o torso da personagem e o carimbo 'CLASIFICADO' invade a janela/parede. Provavelmente é o layout intencional da placa de capítulo, mas a composição fica pesada. Dúvida entre estilo e defeito. |
| 10:55 | Q99 `19650.png` | alto | texto_cortado | A etiqueta 'LUGAR Y FECHA / HONDURAS, 19' está truncada: o ano termina em '19' sem os dois últimos dígitos. Pode ser animação de digitação em andamento, mas aos 10:55 parece texto incompleto. |
| 11:05 | Q100 `19950.png` | medio | texto_cortado | A etiqueta de nome mostra só 'RICH', parecendo nome incompleto (por exemplo, sobrenome cortado). Pode ser animação de entrada, mas há dúvida. |
| 11:15 | Q101 `20250.png` | medio | texto_inventado | As páginas têm linhas de texto borradas, que simulam escrita ilegível. Estão desfocadas de propósito e não leem como texto falso, mas dá para notar que são pseudotexto. |
| 11:55 | Q107 `21450.png` | medio | texto_inventado | A etiqueta no canto superior esquerdo ('LUGAR Y FECHA / MANUAL DE 1983') tem o rótulo pequeno 'LUGAR Y FECHA' encostado/encavalado no topo da linha 'MANUAL DE 1983', com leitura apertada. O texto borrado do documento é intencional (tarja/censura), mas a etiqueta parece apertada. |
| 12:45 | Q112 `22950.png` | medio | anacronismo | Na estante, à direita, há uma bandeira azul e branca com duas estrelas, parecida com a de Honduras. Pode ser bandeira real não pedida ou lugar errado. Confirmar se o contexto do roteiro exige isso. A paisagem pela janela também sugere um lugar específico. |
| 12:53 | Q113 `23191.png` | medio | elemento_fora | A placa de título cobre o rosto do personagem à esquerda e as figuras do meio. Pode ser a composição intencional de uma abertura de capítulo; fica a dúvida. Q114 repete o mesmo quadro no mesmo tempo, sem mudança. |
| 13:45 | Q120 `24750.png` | medio | valor_errado | O mapa da América Central e do Caribe não tem nenhum rótulo, o que pode ser intencional. A Colômbia e a Venezuela estão cortadas pela borda inferior e direita. O Yucatán e as divisões de Belize/Guatemala parecem simplificados. |

36 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q48 (5:31): faixa uniforme na borda topo: 29% do quadro, cor RGB(19,17,15)
- Q48 (5:31): faixa uniforme na borda esquerda: 19% do quadro, cor RGB(14,13,12)
- Q48 (5:31): faixa uniforme na borda direita: 21% do quadro, cor RGB(14,13,12)
- Q49 (5:33): faixa uniforme na borda topo: 21% do quadro, cor RGB(19,17,15)
- Q49 (5:33): faixa uniforme na borda base: 13% do quadro, cor RGB(14,13,12)
- Q49 (5:33): faixa uniforme na borda esquerda: 19% do quadro, cor RGB(14,13,12)
- Q49 (5:33): faixa uniforme na borda direita: 19% do quadro, cor RGB(14,13,12)
- Q50 (5:35): faixa uniforme na borda topo: 17% do quadro, cor RGB(19,17,15)
- Q50 (5:35): faixa uniforme na borda base: 13% do quadro, cor RGB(14,13,12)
- Q50 (5:35): faixa uniforme na borda esquerda: 4% do quadro, cor RGB(14,13,12)
- Q50 (5:35): faixa uniforme na borda direita: 4% do quadro, cor RGB(14,13,12)
- Q51 (5:39): faixa uniforme na borda base: 14% do quadro, cor RGB(44,33,23)
- Q51 (5:39): faixa uniforme na borda esquerda: 4% do quadro, cor RGB(27,31,37)
- Q51 (5:39): faixa uniforme na borda direita: 33% do quadro, cor RGB(27,31,37)
- Q52 (5:45): faixa uniforme na borda topo: 5% do quadro, cor RGB(16,19,26)
- Q52 (5:45): faixa uniforme na borda base: 15% do quadro, cor RGB(20,16,15)
- Q52 (5:45): faixa uniforme na borda esquerda: 4% do quadro, cor RGB(13,16,21)
- Q53 (5:46): faixa uniforme na borda topo: 5% do quadro, cor RGB(16,19,26)
- Q53 (5:46): faixa uniforme na borda base: 14% do quadro, cor RGB(20,16,15)
- Q53 (5:46): faixa uniforme na borda esquerda: 4% do quadro, cor RGB(13,16,21)
- Q54 (5:49): faixa uniforme na borda base: 12% do quadro, cor RGB(31,33,31)
- Q55 (5:49): faixa uniforme na borda base: 12% do quadro, cor RGB(31,33,31)
- Q56 (5:50): faixa uniforme na borda base: 4% do quadro, cor RGB(32,34,32)
- Q57 (5:55): faixa uniforme na borda topo: 7% do quadro, cor RGB(58,72,84)
- Q61 (6:35): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(58,72,80)
- Q78 (8:37): faixa uniforme na borda base: 11% do quadro, cor RGB(49,42,35)
- Q79 (8:38): faixa uniforme na borda base: 11% do quadro, cor RGB(45,39,32)
- Q94 (10:40): faixa uniforme na borda direita: 8% do quadro, cor RGB(53,74,87)
- Q95 (10:43): faixa uniforme na borda direita: 8% do quadro, cor RGB(53,74,87)
- Q96 (10:45): faixa uniforme na borda direita: 5% do quadro, cor RGB(53,74,87)

## Quadros

Q01=0:01, Q02=0:01, Q03=0:05, Q04=0:15, Q05=0:25, Q06=0:28, Q07=0:35, Q08=0:42, Q09=0:42, Q10=0:45, Q11=0:55, Q12=1:05, Q13=1:15, Q14=1:19, Q15=1:25, Q16=1:35, Q17=1:45, Q18=1:46, Q19=1:47, Q20=1:55, Q21=2:05, Q22=2:15, Q23=2:25, Q24=2:35, Q25=2:44, Q26=2:45, Q27=2:45, Q28=2:55, Q29=3:05, Q30=3:15, Q31=3:25, Q32=3:29, Q33=3:29, Q34=3:35, Q35=3:45, Q36=3:55, Q37=4:05, Q38=4:15, Q39=4:25, Q40=4:30, Q41=4:31, Q42=4:35, Q43=4:45, Q44=4:55, Q45=5:05, Q46=5:15, Q47=5:25, Q48=5:31, Q49=5:33, Q50=5:35, Q51=5:39, Q52=5:45, Q53=5:46, Q54=5:49, Q55=5:49, Q56=5:50, Q57=5:55, Q58=6:05, Q59=6:15, Q60=6:25, Q61=6:35, Q62=6:45, Q63=6:48, Q64=6:48, Q65=6:55, Q66=7:05, Q67=7:15, Q68=7:25, Q69=7:35, Q70=7:42, Q71=7:42, Q72=7:45, Q73=7:55, Q74=8:05, Q75=8:15, Q76=8:25, Q77=8:35, Q78=8:37, Q79=8:38, Q80=8:45, Q81=8:55, Q82=9:05, Q83=9:15, Q84=9:25, Q85=9:35, Q86=9:36, Q87=9:36, Q88=9:45, Q89=9:55, Q90=10:05, Q91=10:15, Q92=10:25, Q93=10:35, Q94=10:40, Q95=10:43, Q96=10:45, Q97=10:52, Q98=10:53, Q99=10:55, Q100=11:05, Q101=11:15, Q102=11:25, Q103=11:35, Q104=11:45, Q105=11:51, Q106=11:52, Q107=11:55, Q108=12:05, Q109=12:15, Q110=12:25, Q111=12:35, Q112=12:45, Q113=12:53, Q114=12:53, Q115=12:55, Q116=13:05, Q117=13:15, Q118=13:25, Q119=13:35, Q120=13:45
