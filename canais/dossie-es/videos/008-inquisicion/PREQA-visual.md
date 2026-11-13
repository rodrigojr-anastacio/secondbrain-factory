# Pré-QA visual automático

- Alvo: `canais/dossie-es/videos/008-inquisicion/preqa` · 120 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.266 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 1 · médio 27 · baixo 29
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:32 | Q07 `975.png` | medio | elemento_fora | O carimbo 'CLASIFICADO' fica sobre a borda superior direita da placa e cobre parte da torre e da bandeira. Pode ser estilo intencional, mas o carimbo ultrapassa a placa e a leitura fica um pouco apertada. |
| 0:39 | Q08 `1171.png` | medio | texto_inventado | A página do livro aberto, à direita, traz escrita e desenhos ilegíveis inventados pela IA. É pequena e discreta, mas visível. O nome 'BERNARDO GUI' é rótulo do código e está correto. |
| 0:55 | Q11 `1646.png` | medio | elemento_fora | No mapa, o rótulo TOULOUSE fica colado na borda esquerda e o ponto de Toulouse está quase no canto. O enquadramento deixa a França quase toda fora do quadro. Além disso, há pequenas manchas vermelhas soltas (Albânia, Líbia, Egito, canto direito) que parecem artefatos do mapa. |
| 1:21 | Q16 `2430.png` | medio | anacronismo | Roma 1478 mostra uma cúpula e fachadas de estilo barroco (igreja com cúpula ao centro), posteriores a 1478. A cena é de IA e pode passar, mas há dúvida de época. A faixa de cor sinalizada pelo detector no topo é só o céu liso do pôr do sol, o que é aceitável. |
| 2:01 | Q19 `3630.png` | medio | fundo/faixa | Faixa cinza-esverdeada lisa (RGB 55,60,58) no topo, cerca de 4% do quadro, acima das torres. Parece céu liso ou vinheta da cena, mas pode ser uma faixa chapada. Na dúvida entre estilo e defeito, registro como médio. |
| 2:02 | Q20 `3649.png` | medio | fundo/faixa | Faixa lisa cinza-esverdeada no topo, a mesma do Q19. Parece céu intencional, mas há dúvida se é uma faixa chapada. |
| 2:02 | Q21 `3662.png` | medio | fundo/faixa | Faixa lisa cinza-esverdeada no topo, a mesma dos quadros anteriores. Parece céu liso, com dúvida entre estilo e defeito. |
| 3:41 | Q31 `6630.png` | medio | anacronismo | Galeria de museu com vitrines de vidro e figurantes em trajes do séc. XIX. O contexto diz que é intencional, mas o conteúdo das vitrines (aparelhos de laboratório e máquinas) é genérico e não deixa claro que se trata de objetos da Inquisição. Dúvida entre estilo e defeito. |
| 4:23 | Q36 `7890.png` | medio | anacronismo | Granada/Alhambra com bandeirinhas vermelhas nas torres. Não dá para ver emblema legível. Na dúvida entre estilo e defeito, conferir se não lembram bandeira anacrônica. |
| 4:44 | Q40 `8519.png` | medio | valor_errado | Mapa com fronteiras modernas (Norte da África com linhas retas de países atuais) numa narrativa de 1492. Dúvida entre estilo e erro. O rótulo 'Imperio Otomano' está sobre a Anatólia, aceitável. Há pontinhos vermelhos soltos (Irã, Arábia, Egito) que parecem ruído de textura. |
| 5:21 | Q47 `9630.png` | medio | texto_inventado | O pergaminho segurado pelo terceiro homem da esquerda traz glifos/escrita pseudo-asteca ilegíveis. Pode ser aceitável como códice, mas é texto inventado pela IA e bem visível. |
| 5:31 | Q48 `9930.png` | medio | anacronismo | Um cocar de penas vermelho aparece no meio da multidão ajoelhada, à esquerda do centro. Em cena de missa cristã com indígenas convertidos, o cocar pode ser anacrônico ou estereotipado. Na dúvida entre estilo e defeito, registro como médio. |
| 6:18 | Q54 `11353.png` | medio | texto_inventado | Na parede ao fundo há uma placa/brasão com símbolos pseudo-escritos e o número '1572'. A IA gerou esse texto, que pode ser falso. A legenda 'FRAY LUIS DE LEÓN' é do código e está legível, mas fica perto da borda inferior esquerda e sobre as cabeças dos frades. |
| 6:36 | Q57 `11876.png` | medio | valor_errado | O rótulo MEXICO está sem acento (no Q59 aparece MÉXICO) e o pino cai no litoral do Golfo (Tamaulipas/Veracruz), não na cidade do México. Pode ser intencional, mas é inconsistente com os quadros seguintes. |
| 6:38 | Q58 `11945.png` | medio | valor_errado | Mesmo problema do Q57: rótulo MEXICO sem acento, inconsistente com MÉXICO no Q59, e pino no litoral do Golfo. |
| 7:01 | Q65 `12630.png` | medio | anacronismo | Os soldados no forte usam casacas azuis e chapéus de aba tipo século XVIII, e as bandeiras vermelhas lisas nos navios e no forte são genéricas. Dúvida sobre a época (colônia hispânica), sem erro claro. |
| 7:39 | Q69 `13764.png` | medio | elemento_fora | A placa de capítulo mostra 'EXPEDIENTE 10' e 'Nº 008', e o carimbo 'CLASIFICADO' encosta na aba da placa e invade a imagem. Pode haver numeração inconsistente entre os dois campos. Também há dúvida sobre estilo ou defeito: o carimbo se sobrepõe à aba 'EXPEDIENTE 10'. |
| 8:11 | Q74 `14730.png` | medio | texto_inventado | Na página do manuscrito aberto há linhas de escrita cursiva ilegível, inventada pela IA. É discreta e funciona como textura de manuscrito, mas é letra falsa visível. |
| 9:11 | Q81 `16530.png` | medio | elemento_fora | Praça com colunata tipo São Pedro e fogueira com grande coluna de fumaça no centro; a multidão ao redor das chamas é pequena e discreta, mas há risco de a fogueira parecer figura/cena de queima gráfica. Também há uma faixa vermelha cortada na borda esquerda (bandeira/pano) e uma fatia de prédio cortada na borda direita; é só enquadramento, mas confira se são bandeiras anacrônicas. |
| 10:01 | Q87 `18030.png` | medio | texto_inventado | Os dois livros abertos têm linhas de escrita falsa/ornamentos ilegíveis nas páginas. Pequeno e em estilo de manuscrito decorativo, mas é texto inventado pela IA. |
| 11:10 | Q95 `20113.png` | medio | anacronismo | Multidão de roupas do séc. XIX (coletes, faixas vermelhas na cintura) ao fundo da placa 'El Maestro'; provavelmente intencional (cena de 1817 e posteriores), mas há dúvida se combina com o restante do capítulo. |
| 11:17 | Q98 `20309.png` | medio | texto_inventado | O quadro-negro ao fundo tem rabiscos de giz pseudo-letras ilegíveis (símbolos tipo 'A', 'FA'). São garranchos que parecem texto falso da IA, mas pouco legíveis e discretos. |
| 11:47 | Q101 `21213.png` | medio | anacronismo | A bandeira à esquerda e a do canto direito mostram emblemas indefinidos. Têm aspecto de estandarte inventado, e o enquadramento mostra dois estandartes sem identificação clara (dúvida entre estilo e defeito). |
| 12:51 | Q110 `23130.png` | medio | outro | Os dois monges no canto inferior direito estão cortados pela borda e parecem ligeiramente deformados. O frade da direita segura um objeto indefinido. Pode ser só enquadramento normal; registrado por dúvida. |
| 13:01 | Q111 `23430.png` | medio | texto_inventado | As páginas do livro aberto trazem tabela com manuscrito falso e ilegível, escrito pela IA. É pequeno e decorativo, e o texto é ilegível de propósito, mas é texto inventado visível. Registrado por dúvida. |
| 13:03 | Q112 `23491.png` | alto | valor_errado | No mapa da América do Sul, o rótulo "CHILE" está no litoral do Pacífico na altura do norte do Chile, fora da posição correta, e o rótulo "RÍO DE LA PLATA" aponta para a costa atlântica da Argentina/Uruguai. "Cartagena" e "Quito" estão aproximadamente certos. O ponto de Lima parece certo. O pin de Chile fica mal posicionado. |
| 13:06 | Q113 `23578.png` | medio | valor_errado | Rótulo "CHILE" marca um país/região inteira, enquanto os demais rótulos são cidades. Além disso, o ponto está na costa e a geografia do mapa parece levemente distorcida (Cartagena no topo ok). Possível inconsistência de rótulos; confirmar se é o desejado pelo roteiro. |
| 13:41 | Q118 `24630.png` | medio | texto_inventado | Os livros pendurados no pescoço do homem têm páginas com escrita falsa/ilegível gerada pela IA. É texto manuscrito pequeno, em tom de rabisco, bem visível em primeiro plano. Dúvida entre estilo e defeito. |

29 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q06 (0:31): faixa uniforme na borda topo: 8% do quadro, cor RGB(41,50,52)
- Q07 (0:32): faixa uniforme na borda topo: 8% do quadro, cor RGB(40,50,52)
- Q16 (1:21): faixa uniforme na borda topo: 5% do quadro, cor RGB(155,130,90)
- Q19 (2:01): faixa uniforme na borda topo: 4% do quadro, cor RGB(55,60,58)
- Q20 (2:02): faixa uniforme na borda topo: 4% do quadro, cor RGB(55,60,58)
- Q21 (2:02): faixa uniforme na borda topo: 4% do quadro, cor RGB(55,60,58)
- Q25 (2:41): faixa uniforme na borda topo: 3% do quadro, cor RGB(77,100,103)
- Q36 (4:23): faixa uniforme na borda topo: 5% do quadro, cor RGB(49,54,53)
- Q37 (4:23): faixa uniforme na borda topo: 5% do quadro, cor RGB(49,55,54)
- Q42 (5:01): faixa uniforme na borda topo: 4% do quadro, cor RGB(47,58,64)
- Q43 (5:02): faixa uniforme na borda topo: 6% do quadro, cor RGB(44,54,59)
- Q44 (5:03): faixa uniforme na borda topo: 7% do quadro, cor RGB(44,54,59)
- Q51 (5:57): faixa uniforme na borda topo: 21% do quadro, cor RGB(55,64,67)
- Q52 (5:57): faixa uniforme na borda topo: 21% do quadro, cor RGB(55,63,67)
- Q77 (8:44): faixa uniforme na borda topo: 17% do quadro, cor RGB(43,52,56)
- Q78 (8:44): faixa uniforme na borda topo: 17% do quadro, cor RGB(43,52,56)
- Q85 (9:44): faixa uniforme na borda topo: 13% do quadro, cor RGB(38,47,51)
- Q105 (12:21): faixa uniforme na borda topo: 17% do quadro, cor RGB(46,53,56)
- Q106 (12:22): faixa uniforme na borda topo: 17% do quadro, cor RGB(46,53,56)
- Q107 (12:22): faixa uniforme na borda topo: 13% do quadro, cor RGB(47,55,58)

## Quadros

Q01=0:01, Q02=0:02, Q03=0:02, Q04=0:11, Q05=0:21, Q06=0:31, Q07=0:32, Q08=0:39, Q09=0:41, Q10=0:51, Q11=0:55, Q12=1:01, Q13=1:15, Q14=1:18, Q15=1:19, Q16=1:21, Q17=1:31, Q18=1:41, Q19=2:01, Q20=2:02, Q21=2:02, Q22=2:11, Q23=2:21, Q24=2:31, Q25=2:41, Q26=2:50, Q27=2:51, Q28=3:01, Q29=3:11, Q30=3:31, Q31=3:41, Q32=3:43, Q33=3:51, Q34=4:01, Q35=4:11, Q36=4:23, Q37=4:23, Q38=4:31, Q39=4:41, Q40=4:44, Q41=4:59, Q42=5:01, Q43=5:02, Q44=5:03, Q45=5:06, Q46=5:11, Q47=5:21, Q48=5:31, Q49=5:41, Q50=5:51, Q51=5:57, Q52=5:57, Q53=6:11, Q54=6:18, Q55=6:21, Q56=6:31, Q57=6:36, Q58=6:38, Q59=6:41, Q60=6:43, Q61=6:43, Q62=6:51, Q63=6:54, Q64=6:58, Q65=7:01, Q66=7:11, Q67=7:21, Q68=7:31, Q69=7:39, Q70=7:41, Q71=7:51, Q72=7:59, Q73=8:01, Q74=8:11, Q75=8:21, Q76=8:41, Q77=8:44, Q78=8:44, Q79=8:51, Q80=8:51, Q81=9:11, Q82=9:21, Q83=9:31, Q84=9:41, Q85=9:44, Q86=9:51, Q87=10:01, Q88=10:05, Q89=10:11, Q90=10:21, Q91=10:31, Q92=10:41, Q93=10:51, Q94=11:01, Q95=11:10, Q96=11:11, Q97=11:11, Q98=11:17, Q99=11:31, Q100=11:41, Q101=11:47, Q102=11:51, Q103=11:58, Q104=12:11, Q105=12:21, Q106=12:22, Q107=12:22, Q108=12:28, Q109=12:31, Q110=12:51, Q111=13:01, Q112=13:03, Q113=13:06, Q114=13:11, Q115=13:21, Q116=13:34, Q117=13:34, Q118=13:41, Q119=13:51, Q120=14:01
