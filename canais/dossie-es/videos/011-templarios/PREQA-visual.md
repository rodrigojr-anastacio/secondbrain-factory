# Pré-QA visual automático

- Alvo: `canais/dossie-es/videos/011-templarios/preqa` · 120 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.283 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 11 · médio 29 · baixo 31
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:37 | Q07 `1117.png` | medio | texto_encavalado | O carimbo 'CLASIFICADO' se sobrepõe à aba 'EXPEDIENTE 1' e ao canto da placa, e fica parcialmente atrás da borda dourada. Parece composição intencional de placa de capítulo, mas o texto do carimbo ainda é legível. Em dúvida entre estilo e defeito. |
| 0:37 | Q07 `1117.png` | medio | anacronismo | O fundo mostra Jerusalém com a Cúpula da Rocha e minaretes. No contexto dos templários, o cenário em torno de 1119 pode ser aceitável, mas os minaretes são anacrônicos para essa época. Em dúvida. |
| 0:38 | Q08 `1139.png` | medio | texto_encavalado | O carimbo 'CLASIFICADO' se sobrepõe à aba 'EXPEDIENTE 1' e ao canto da placa. Mesma dúvida do Q07 quanto à composição, embora legível. |
| 0:38 | Q08 `1139.png` | medio | anacronismo | Minaretes junto à Cúpula da Rocha no fundo de Jerusalém, possivelmente anacrônicos para o período. Em dúvida. |
| 1:10 | Q13 `2115.png` | alto | texto_inventado | O livro aberto no atril tem texto ilegível inventado pela IA, com garranchos que imitam escrita, bem visível nas duas páginas. Seria melhor trocar a imagem ou deixar as páginas sem escrita legível. |
| 1:20 | Q14 `2415.png` | medio | fundo/faixa | Há uma faixa uniforme na borda esquerda do mapa (~7%, RGB 79,91,95), com o mar liso. Também aparece uma linha horizontal de dobra no meio do mar. Pode ser textura intencional de papel ou o oceano plano do mapa. Na dúvida, conferir se há emenda. |
| 1:22 | Q15 `2473.png` | medio | fundo/faixa | A faixa uniforme na borda esquerda (~14%, RGB 78,90,95) ocupa mais área do que em Q14. Parece mar liso do mapa, mas pode ser emenda ou fundo chapado sem relevo. Há também a linha horizontal de dobra no mar. Conferir. |
| 1:25 | Q16 `2564.png` | medio | elemento_fora | A placa de título 'EL HÁBITO' cobre quase todo o personagem deitado na cama, deixando só as mãos visíveis. Se for um cartão de capítulo intencional, é aceitável. O carimbo 'CLASIFICADO' invade a borda da placa e passa por cima da cena. Conferir se a sobreposição é a pretendida. |
| 1:30 | Q18 `2715.png` | medio | fundo/faixa | O sinal automático acusa faixa uniforme de 6% na borda inferior (RGB 44,54,61). Visualmente o piso de pedra escuro parece continuar até a base, então pode ser só sombra da cena. Conferir se não há faixa chapada. |
| 2:10 | Q24 `3915.png` | alto | anacronismo | Alfonso I el Batallador aparece com túnica templária com cruz vermelha e bandeiras templárias com cruz na tenda, em 1131. Há dúvida sobre o enquadramento, mas a cruz vermelha em um rei de Aragão é inconsistente com o contexto. A lamparina a óleo de vidro também parece tardia para a época. |
| 2:12 | Q25 `3959.png` | medio | anacronismo | Na mesa há uma lamparina a óleo de vidro com chaminé (estilo séc. XIX), anacrônica para 1131. Há também um jarro metálico no canto direito que parece moderno. Fica a dúvida se é estilo ou defeito. |
| 2:20 | Q26 `4215.png` | medio | anacronismo | O hospitalário do centro usa cruz branca de oito pontas sobre túnica preta, que é mais tardia, e o da direita tem cruz vermelha alongada de duas barras no manto. As cruzes não são claras nem coerentes com a época, mas pode ser licença de estilo. |
| 3:20 | Q35 `6015.png` | alto | anacronismo | Os dois guardas ao lado do trono usam armadura de placas completa, com elmo fechado, de estilo claramente tardo-medieval (séc. XV). O vídeo é de 1147, época de cota de malha. Os brasões com leões rampantes nas laterais também são duvidosos para a época e o lugar. |
| 4:00 | Q42 `7215.png` | alto | texto_inventado | A legenda do rótulo está escrita "SIMÓN DE MONTFOR", com o T final faltando. Em Q43 aparece "MONTFORT". Ou é erro de grafia ou a placa foi cortada; precisa ser corrigida. |
| 4:19 | Q45 `7763.png` | medio | anacronismo | A inscrição "1214" está gravada na muralha. Numeração arábica num castelo medieval do século XIII é um anacronismo discreto, e é texto escrito pela IA dentro da cena. |
| 4:30 | Q47 `8115.png` | medio | moldura | Faixa preta na borda esquerda (~7%, sinal automático). Parte dela coincide com a sombra escura do canto, que pode ser intencional, mas o bloco chapado preto no alto à esquerda parece margem de IA. Conferir e recortar se for o caso. |
| 4:50 | Q51 `8715.png` | alto | anacronismo | Jaime I desembarca em Mallorca (1229) num barco com proa de dragão, tipo drakkar viking, que não é a embarcação da frota aragonesa do século XIII. O castelo ao fundo também é genérico. |
| 4:51 | Q52 `8718.png` | alto | anacronismo | Mesmo problema do Q51: barco com cabeça de dragão estilo viking no desembarque de Jaime I em Mallorca, em 1229. |
| 5:20 | Q55 `9615.png` | medio | anacronismo | Uma cruz vermelha templária aparece também em figuras de verde e azul ao fundo, e a figura de manto vermelho (o rei) usa cruz templária no peito. Fica estranho para Jaime I e pode ser erro de iconografia; na dúvida entre estilo e erro, registrar. |
| 5:39 | Q57 `10172.png` | medio | elemento_fora | A placa de capítulo 'LA ORDEN' cobre quase todo o personagem sentado, incluindo o rosto e o tronco. Se for a placa de capítulo intencional, é só enquadramento; o personagem principal fica totalmente escondido, e a dúvida é se a imagem de fundo foi pensada para isso. |
| 5:40 | Q58 `10194.png` | medio | elemento_fora | A placa 'LA ORDEN' tapa a cabeça e o tronco do personagem sentado à mesa, e só as mãos aparecem. Mesma dúvida de enquadramento do Q57. |
| 5:40 | Q59 `10215.png` | medio | elemento_fora | A placa 'LA ORDEN' esconde o rosto do personagem sentado, e só as mãos e o papel aparecem. Mesma dúvida de enquadramento do Q57. |
| 6:03 | Q62 `10894.png` | medio | anacronismo | A cena de 'PARÍS, 1307' mostra um castelo com torres de telhado cônico verde e bandeirolas brancas com cruz vermelha, parecidas com a bandeira de São Jorge/inglesa. Há dúvida se é anacronismo ou se lembra os Templários. A cidade coberta por nuvens baixas e fogo nos telhados também foge do estilo. |
| 6:30 | Q65 `11715.png` | medio | valor_errado | O ponto de ACRE fica sobre o mar, ao lado da costa do Levante, com o rótulo em cima de Chipre. Jerusalém também está muito perto da costa. Na escala do mapa a diferença é pequena, mas a posição de Acre parece imprecisa. |
| 6:31 | Q66 `11719.png` | medio | valor_errado | Mesma imprecisão do Q65: o marcador de ACRE está sobre a água, perto do litoral, e o rótulo se sobrepõe visualmente a Chipre. |
| 7:58 | Q80 `14342.png` | alto | texto_inventado | O pergaminho na mesa, embaixo, traz linhas de texto falso e ilegível escritas pela IA, com letras inventadas. Fica bem visível em primeiro plano. O rótulo "BARBARA FRALE" vem do código e está correto. |
| 8:20 | Q83 `15015.png` | alto | texto_inventado | O pergaminho sobre a mesa do bispo traz letras inventadas pela IA, em caixa alta e parcialmente invertidas (algo como 'PARTHENTIS...'), com um selo vermelho. O texto é visível e ilegível. |
| 8:30 | Q84 `15315.png` | medio | moldura | A imagem parece ter resolução e nitidez diferentes das demais, com aspecto mais suave. Há uma margem estreita no lado direito, mas não dá para confirmar se é moldura. Vale conferir com o detector de bordas. |
| 8:50 | Q87 `15915.png` | alto | anacronismo | Notre-Dame de Paris aparece com fumaça de incêndio e andaime na torre, o que é uma cena de 2019. O contexto parece ser a dissolução dos Templários, em 1312, e o quadro destoa dele. Também há uma assinatura ilegível no canto inferior direito. |
| 9:29 | Q92 `17084.png` | medio | fundo/faixa | Mapa 2D com faixa uniforme de mar (14% da borda esquerda) e linha horizontal fina de emenda visível no mar à esquerda (~y=277). O mar liso pode ser parte do estilo do mapa, mas a emenda é discreta e merece conferência. |
| 9:30 | Q93 `17115.png` | medio | elemento_fora | Crossfade entre o mapa e o retrato do cardeal, mas o rótulo 'MONZON' e o mapa ficam muito visíveis sobre o personagem. Se não for só transição, a sobreposição atrapalha a leitura. |
| 10:20 | Q101 `18615.png` | medio | anacronismo | Guindaste/torno de madeira e muralha com merlões de aparência quase moderna; no topo, bandeira cortada pela borda superior e templários com cruz vermelha. Possível anacronismo discreto na construção, dúvida entre estilo e defeito. |
| 10:40 | Q103 `19215.png` | alto | anacronismo | Caravela com velas brancas e cruz vermelha templária, tripulação com chapéus e roupas renascentistas, tudo bem posterior à extinção da Ordem (1312). Se a cena é a narrativa do mito dos Templários em Portugal/Ordem de Cristo, é aceitável, mas a embarcação parece do século XV e o contexto é duvidoso. |
| 10:46 | Q105 `19369.png` | medio | elemento_fora | A placa de capítulo (EXPEDIENTE 12 / LA BANDERA) cobre a faixa central do quadro. O carimbo CLASIFICADO passa por cima da borda superior direita da placa e invade a folhagem. Parece estilo intencional do canal, mas a placa esconde parte da caravela e da praia. |
| 10:55 | Q106 `19639.png` | medio | anacronismo | A bandeira com cruz templária cinza-escura na praia, com Cabral, não tem cor definida. A legenda 'PEDRO ÁLVARES CABRAL' está em português, num canal de dossiê em espanhol. Confirmar o idioma. |
| 11:00 | Q108 `19815.png` | medio | anacronismo | A bandeira branca com cruz vermelha simples lembra a cruz templária ou da Ordem de Cristo, mas o desenho é de uma cruz grega reta. Pode ser dúvida histórica; a cruz da Ordem de Cristo tem pontas alargadas. |
| 11:28 | Q111 `20645.png` | medio | valor_errado | O mapa mostra uma mancha preta pequena no Egito/Mar Vermelho, perto do Sinai, parecendo artefato. A rota Lisboa–Brasil é uma curva reta bem simples, e o rótulo LISBOA está na costa do Mediterrâneo e não de Portugal. Conferir a posição do ponto. |
| 11:48 | Q114 `21230.png` | medio | anacronismo | Fundo do castelo/vila tem estilo diferente do canal (mais digital/ilustração limpa, menos tinta grossa) e castelo com bandeirolas vermelhas; dúvida se é estilo intencional. Faixa superior é só céu escuro liso, não defeito. |
| 11:50 | Q116 `21315.png` | medio | anacronismo | Bandeira preta com cruz branca flutuando na torre em 'Monzón, hoje': cruz de estilo hospitalário/maltês, não templária; dúvida sobre correção histórica. Soldado com armadura na torre sugere cena medieval, em conflito com 'hoje'. |
| 12:30 | Q120 `22515.png` | alto | anacronismo | Escritório com máquina de escrever, abajur de mesa e papel de parede de época moderna (séc. XX) com cruz templária na lareira; pode ser intencional (dossiê moderno), mas a cruz vermelha na lareira parece elemento solto/estranho. |

31 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q01 (0:00): faixa uniforme na borda topo: 14% do quadro, cor RGB(60,74,82)
- Q02 (0:01): faixa uniforme na borda topo: 14% do quadro, cor RGB(60,74,82)
- Q03 (0:01): faixa uniforme na borda topo: 14% do quadro, cor RGB(60,74,82)
- Q06 (0:30): faixa uniforme na borda topo: 18% do quadro, cor RGB(79,90,95)
- Q07 (0:37): faixa uniforme na borda topo: 14% do quadro, cor RGB(42,50,50)
- Q08 (0:38): faixa uniforme na borda topo: 15% do quadro, cor RGB(42,50,50)
- Q14 (1:20): faixa uniforme na borda esquerda: 7% do quadro, cor RGB(79,91,95)
- Q15 (1:22): faixa uniforme na borda esquerda: 14% do quadro, cor RGB(78,90,95)
- Q18 (1:30): faixa uniforme na borda base: 6% do quadro, cor RGB(44,54,61)
- Q28 (2:36): faixa uniforme na borda topo: 6% do quadro, cor RGB(83,95,100)
- Q31 (2:58): faixa uniforme na borda topo: 7% do quadro, cor RGB(42,49,48)
- Q32 (2:58): faixa uniforme na borda topo: 6% do quadro, cor RGB(42,49,48)
- Q34 (3:10): faixa uniforme na borda topo: 8% do quadro, cor RGB(62,75,83)
- Q39 (3:45): faixa uniforme na borda topo: 16% do quadro, cor RGB(45,57,62)
- Q40 (3:46): faixa uniforme na borda topo: 16% do quadro, cor RGB(45,57,62)
- Q47 (4:30): faixa preta na borda esquerda: 7% do quadro
- Q74 (7:20): faixa uniforme na borda topo: 11% do quadro, cor RGB(73,89,96)
- Q76 (7:40): faixa uniforme na borda topo: 14% do quadro, cor RGB(44,51,55)
- Q77 (7:40): faixa uniforme na borda topo: 15% do quadro, cor RGB(45,52,56)
- Q85 (8:33): faixa uniforme na borda topo: 5% do quadro, cor RGB(79,90,95)
- Q89 (9:07): faixa uniforme na borda topo: 6% do quadro, cor RGB(35,45,51)
- Q90 (9:07): faixa uniforme na borda topo: 6% do quadro, cor RGB(35,45,51)
- Q92 (9:29): faixa uniforme na borda esquerda: 14% do quadro, cor RGB(78,90,95)
- Q94 (9:40): faixa uniforme na borda topo: 11% do quadro, cor RGB(80,95,101)
- Q95 (9:50): faixa uniforme na borda topo: 11% do quadro, cor RGB(32,49,62)
- Q113 (11:40): faixa uniforme na borda topo: 13% do quadro, cor RGB(59,77,92)
- Q114 (11:48): faixa uniforme na borda topo: 7% do quadro, cor RGB(38,51,56)
- Q115 (11:48): faixa uniforme na borda topo: 7% do quadro, cor RGB(38,51,56)

## Quadros

Q01=0:00, Q02=0:01, Q03=0:01, Q04=0:10, Q05=0:20, Q06=0:30, Q07=0:37, Q08=0:38, Q09=0:40, Q10=0:44, Q11=0:50, Q12=1:00, Q13=1:10, Q14=1:20, Q15=1:22, Q16=1:25, Q17=1:26, Q18=1:30, Q19=1:40, Q20=1:50, Q21=2:00, Q22=2:08, Q23=2:08, Q24=2:10, Q25=2:12, Q26=2:20, Q27=2:30, Q28=2:36, Q29=2:40, Q30=2:42, Q31=2:58, Q32=2:58, Q33=3:00, Q34=3:10, Q35=3:20, Q36=3:24, Q37=3:30, Q38=3:40, Q39=3:45, Q40=3:46, Q41=3:50, Q42=4:00, Q43=4:02, Q44=4:10, Q45=4:19, Q46=4:23, Q47=4:30, Q48=4:40, Q49=4:46, Q50=4:47, Q51=4:50, Q52=4:51, Q53=5:00, Q54=5:10, Q55=5:20, Q56=5:30, Q57=5:39, Q58=5:40, Q59=5:40, Q60=5:47, Q61=6:00, Q62=6:03, Q63=6:10, Q64=6:20, Q65=6:30, Q66=6:31, Q67=6:40, Q68=6:50, Q69=6:50, Q70=6:51, Q71=7:00, Q72=7:05, Q73=7:10, Q74=7:20, Q75=7:30, Q76=7:40, Q77=7:40, Q78=7:46, Q79=7:50, Q80=7:58, Q81=8:00, Q82=8:10, Q83=8:20, Q84=8:30, Q85=8:33, Q86=8:40, Q87=8:50, Q88=9:00, Q89=9:07, Q90=9:07, Q91=9:20, Q92=9:29, Q93=9:30, Q94=9:40, Q95=9:50, Q96=9:52, Q97=9:53, Q98=10:00, Q99=10:07, Q100=10:10, Q101=10:20, Q102=10:30, Q103=10:40, Q104=10:45, Q105=10:46, Q106=10:55, Q107=10:58, Q108=11:00, Q109=11:10, Q110=11:20, Q111=11:28, Q112=11:30, Q113=11:40, Q114=11:48, Q115=11:48, Q116=11:50, Q117=12:00, Q118=12:10, Q119=12:20, Q120=12:30
