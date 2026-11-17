# Pré-QA visual automático

- Alvo: `canais/dossie-es/videos/010-cartel-medellin/preqa` · 113 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.265 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 10 · médio 23 · baixo 32
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:36 | Q07 `1088.png` | medio | fundo/faixa | O sinal automático acusa faixa uniforme no topo (17%, RGB 41,49,52). Na imagem é o céu escuro e liso da cena, com nuvens, o que provavelmente é intencional e não tem emenda visível. Fica registrado só pela dúvida: confirme que não há faixa chapada de verdade. |
| 0:36 | Q08 `1094.png` | medio | fundo/faixa | O sinal automático acusa faixa uniforme no topo (17%, RGB 41,49,52). Parece ser o céu escuro e liso da cena, sem emenda visível. Fica registrado pela dúvida: confirme que o céu não é um bloco chapado. |
| 0:40 | Q09 `1215.png` | medio | anacronismo | As duas bandeirinhas de mesa sobre a mesa (cores azul-acinzentado/oliva) não correspondem a nenhuma bandeira reconhecível. Ficam como bandeira inventada/genérica para uma cena de Washington 1979. Dúvida entre estilo e defeito. |
| 0:50 | Q10 `1515.png` | alto | anacronismo | Guardas com uniforme napoleônico/de gala e quepe alto de pelo, diante de um palácio neoclássico europeu, não combinam com o contexto (Colômbia/Washington, 1979). Lugar e época parecem errados. Os carros são mais antigos que o final dos anos 70. |
| 2:00 | Q19 `3615.png` | medio | texto_inventado | As bandeiras/tapeçarias nas paredes (direita e esquerda) e os quadros ao fundo têm padrões que parecem glifos ou letras falsas. Ficam discretos e sem legibilidade, então o risco é baixo. |
| 2:50 | Q26 `5115.png` | medio | anacronismo | A bandeira ao fundo tem faixas amarela, azul e vermelha dispostas de forma diagonal e estranha, e não horizontal como a colombiana. Pode ser uma distorção da IA. Vale conferir. |
| 3:00 | Q27 `5415.png` | medio | anacronismo | As duas bandeiras ao lado do quadro são só amarelo e vermelho, sem o azul da bandeira colombiana (amarelo-azul-vermelho). Pode ser uma bandeira inventada ou espanhola, o que destoa em um plenário de Bogotá. Vale conferir. |
| 3:30 | Q30 `6315.png` | medio | texto_inventado | O documento na mesa tem texto ilegível inventado pela IA, com linhas de letra falsa e um selo. Fica pequeno e em segundo plano, mas é visível. |
| 4:00 | Q35 `7215.png` | medio | texto_inventado | O papel na mesa, embaixo à direita, tem rabiscos que imitam texto e parecem letra falsa da IA. Está pequeno e semiescondido na borda, por isso a severidade é média. |
| 4:20 | Q37 `7815.png` | medio | anacronismo | A calculadora eletrônica com visor laranja na bancada parece moderna para um banco do Panamá em 1984. É duvidoso: calculadoras de mesa já existiam nessa época. Também há um objeto cortado na borda direita, mas isso é enquadramento normal. |
| 5:00 | Q43 `9015.png` | alto | moldura | Faixa preta chapada na borda direita (~14% do quadro) e uma faixa escura na esquerda, formando letterbox lateral. Parte pode ser o batente da porta em penumbra, mas a faixa direita é totalmente preta e sem detalhe. Precisa de recorte ou checagem. |
| 5:10 | Q44 `9315.png` | medio | anacronismo | Bogotá no Palácio de Justiça: blindados e uniformes parecem genéricos/europeus, com um possível risco de época. Há bandeiras vermelhas minúsculas nas bordas direita e esquerda, sem identificação clara. Fachada neoclássica genérica, sem relação clara com o edifício real. Ficção intencional, mas vale conferir. |
| 5:50 | Q50 `10515.png` | medio | anacronismo | Bandeira amarelo-azul-vermelha atrás dos homens (parece a da Colômbia, mas as faixas estão na vertical, o que não bate com a bandeira real). Fica em dúvida entre estilo e erro de bandeira inventada. |
| 6:10 | Q52 `11115.png` | medio | elemento_fora | Casa de estilo enxaimel alpino e pinheiros de clima temperado não combinam com uma fazenda colombiana. As viaturas têm emblemas pequenos ilegíveis nas portas, que podem ser texto inventado. |
| 7:10 | Q60 `12915.png` | alto | texto_inventado | Medalhão no topo do arco com monograma/letra escrita pela IA (tipo "M" rabiscado) e letreiros ilegíveis nas lojas ao fundo, à direita e à esquerda. |
| 7:20 | Q61 `13215.png` | alto | texto_inventado | Placa acima da porta com "POLICA STATION" (erro de grafia, e em inglês), mais um letreiro ilegível na construção da esquerda e uma plaqueta com texto falso ao lado da porta. Rótulo deveria vir do código. |
| 7:30 | Q62 `13515.png` | medio | anacronismo | Tribunal com monitores/impressoras de computador e fones de ouvido; se o caso é anterior aos anos 90, é anacrônico. Dúvida entre estilo e erro de época. |
| 7:54 | Q65 `14219.png` | medio | elemento_fora | A placa de capítulo 'LOS REHENES' cobre o rosto da apresentadora do nariz para baixo (só olhos e cabelo aparecem). Pode ser intencional como placa de capítulo, mas o enquadramento esconde o personagem. 'CLASIFICADO' também encosta no cabelo dela. O 'ON AIR' do estúdio é texto legítimo da cena. |
| 7:54 | Q66 `14225.png` | medio | elemento_fora | Mesma placa 'LOS REHENES' tapando a boca e o nariz da apresentadora, em tela com zoom ligeiramente diferente do Q65. Se houver dúvida entre estilo e defeito: o quadro repete a placa por ~0s no mesmo tempo (7:54), o que sugere duplicação de quadro ou crossfade. |
| 8:20 | Q69 `15015.png` | alto | texto_inventado | Manchete do jornal na mesa, embaixo à direita, com letras falsas ('Emots Mions Use'), e cartazes na parede à esquerda com texto ilegível. A etiqueta 'FRANCISCO SANTOS' no canto inferior esquerdo está sobre a máquina de escrever, com baixo contraste e legibilidade fraca, parecendo semitransparente. |
| 9:00 | Q73 `16215.png` | medio | anacronismo | A bandeira à direita parece ter as cores da Colômbia (amarelo, azul, vermelho) e o presidente César Gaviria usa um pin vermelho na lapela. A faixa presidencial aparece só como um pedaço azul/vermelho no peito. Confira se é coerente. A bandeira à esquerda está quase toda cortada e atrás da câmera. |
| 9:20 | Q77 `16815.png` | alto | moldura | Faixa clara estreita na borda esquerda do quadro, e a borda inferior parece ter margem. Indica moldura/margem de papel da IA, e o recorte não foi aplicado. |
| 9:50 | Q80 `17715.png` | medio | texto_inventado | Placas pequenas sobre as portas e um quadro vermelho na parede do fundo mostram marcas parecidas com texto, ilegíveis, inventadas pela IA. Estão discretas. |
| 10:20 | Q85 `18615.png` | alto | texto_inventado | Os cartazes de mapa na parede esquerda trazem letras falsas ilegíveis (ex.: "GRGANCAD"). O jornal à direita e o papel sobre a mesa têm manchetes e texto inventados pela IA, além de um fragmento de texto "PEE GRGANCAD" no canto inferior direito. |
| 10:30 | Q86 `18915.png` | alto | texto_inventado | O quadro emoldurado na parede direita tem texto inventado e ilegível ("ERO CIE DIE ANUSO" ou similar), com diagrama falso. |
| 10:50 | Q88 `19515.png` | medio | texto_inventado | Os mapas e cartazes na parede, além do jornal sobre a mesa, têm rótulos e manchetes inventados e ilegíveis, discretos e parcialmente cortados pela borda. O texto "PLAAK EAGEHCAD" no cartaz do canto superior esquerdo é falso. |
| 11:30 | Q94 `20715.png` | medio | texto_inventado | Helicóptero com marcações inventadas: "1991" no casco e uma plaqueta vermelha com letras ilegíveis no nariz. A IA escreveu texto que não deveria estar na imagem. |
| 11:40 | Q95 `21015.png` | alto | texto_inventado | Jornal empilhado à esquerda com manchetes em letras falsas/ilegíveis e espelhadas ("Eloigh ien Es exnot"), escrito pela IA. Também há um cartaz com "1991" no canto superior esquerdo e a capa do livro diz "NATIONAL CONSTITUTION" em inglês, fora do idioma do canal (espanhol). |
| 12:00 | Q99 `21615.png` | alto | anacronismo | Soldados com capacetes e uniformes de estilo alemão da Segunda Guerra marchando na montanha, em um dossiê sobre o Cartel de Medellín (Colômbia, anos 80-90). Época e lugar incompatíveis com o tema do vídeo. |
| 12:50 | Q104 `23115.png` | medio | elemento_fora | Folha de papel com uma tarja preta grossa no meio. Pode ser intencional (documento censurado), mas lembra faixa preta de erro; confirmar se é intencional. Mesa com pena de escrever e selo de cera ao lado de máquina de escrever mistura épocas. |
| 13:10 | Q108 `23715.png` | medio | anacronismo | Policiais com jaqueta escrita 'POLICE' em inglês numa cena do cartel de Medellín (Colômbia); o uniforme e o idioma destoam do lugar, e o texto foi gerado pela IA. Pode ser lugar errado (EUA), então confira o contexto da cena. |
| 13:20 | Q109 `24015.png` | medio | texto_inventado | Pilhas de livros/caixas à direita têm letras ilegíveis inventadas pela IA, e há um emblema com estrela vermelha no canto superior direito. A cena está em dupla exposição, então pode ser crossfade, mas o detalhe fica estranho. |
| 14:00 | Q113 `25215.png` | medio | texto_inventado | No papel sobre a mesa, à direita da mancha vermelha, há rabiscos que parecem escrita ilegível inventada pela IA (algo como 'Hypothetical'). São pequenos e parcialmente cobertos pela tinta. O mapa-múndi ao fundo não mostra texto legível. |

32 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q07 (0:36): faixa uniforme na borda topo: 17% do quadro, cor RGB(41,49,52)
- Q08 (0:36): faixa uniforme na borda topo: 17% do quadro, cor RGB(41,49,52)
- Q14 (1:30): faixa uniforme na borda topo: 21% do quadro, cor RGB(15,19,23)
- Q15 (1:31): faixa uniforme na borda topo: 21% do quadro, cor RGB(17,20,24)
- Q16 (1:31): faixa uniforme na borda topo: 21% do quadro, cor RGB(17,20,24)
- Q17 (1:40): faixa uniforme na borda topo: 10% do quadro, cor RGB(51,65,74)
- Q20 (2:10): faixa uniforme na borda topo: 4% do quadro, cor RGB(55,64,73)
- Q43 (5:00): faixa preta na borda direita: 14% do quadro
- Q53 (6:20): faixa preta na borda esquerda: 3% do quadro
- Q54 (6:30): faixa uniforme na borda topo: 8% do quadro, cor RGB(54,68,77)
- Q72 (8:50): faixa uniforme na borda topo: 11% do quadro, cor RGB(47,58,67)
- Q82 (10:06): faixa uniforme na borda topo: 4% do quadro, cor RGB(23,32,35)
- Q83 (10:06): faixa uniforme na borda topo: 5% do quadro, cor RGB(23,32,34)
- Q93 (11:20): faixa uniforme na borda topo: 8% do quadro, cor RGB(76,99,108)
- Q96 (11:50): faixa uniforme na borda topo: 12% do quadro, cor RGB(19,25,30)
- Q97 (11:51): faixa uniforme na borda topo: 12% do quadro, cor RGB(19,26,30)
- Q98 (11:51): faixa uniforme na borda topo: 11% do quadro, cor RGB(19,26,30)
- Q99 (12:00): faixa uniforme na borda topo: 5% do quadro, cor RGB(55,71,81)
- Q109 (13:20): faixa uniforme na borda topo: 6% do quadro, cor RGB(79,88,88)
- Q109 (13:20): faixa uniforme na borda base: 4% do quadro, cor RGB(43,49,52)

## Quadros

Q01=0:00, Q02=0:01, Q03=0:02, Q04=0:10, Q05=0:20, Q06=0:30, Q07=0:36, Q08=0:36, Q09=0:40, Q10=0:50, Q11=1:00, Q12=1:10, Q13=1:20, Q14=1:30, Q15=1:31, Q16=1:31, Q17=1:40, Q18=1:50, Q19=2:00, Q20=2:10, Q21=2:20, Q22=2:30, Q23=2:38, Q24=2:38, Q25=2:40, Q26=2:50, Q27=3:00, Q28=3:10, Q29=3:20, Q30=3:30, Q31=3:37, Q32=3:37, Q33=3:40, Q34=3:50, Q35=4:00, Q36=4:10, Q37=4:20, Q38=4:30, Q39=4:38, Q40=4:38, Q41=4:40, Q42=4:50, Q43=5:00, Q44=5:10, Q45=5:20, Q46=5:27, Q47=5:27, Q48=5:30, Q49=5:40, Q50=5:50, Q51=6:00, Q52=6:10, Q53=6:20, Q54=6:30, Q55=6:33, Q56=6:33, Q57=6:40, Q58=6:50, Q59=7:00, Q60=7:10, Q61=7:20, Q62=7:30, Q63=7:40, Q64=7:50, Q65=7:54, Q66=7:54, Q67=8:00, Q68=8:10, Q69=8:20, Q70=8:30, Q71=8:40, Q72=8:50, Q73=9:00, Q74=9:10, Q75=9:11, Q76=9:11, Q77=9:20, Q78=9:30, Q79=9:40, Q80=9:50, Q81=10:00, Q82=10:06, Q83=10:06, Q84=10:10, Q85=10:20, Q86=10:30, Q87=10:40, Q88=10:50, Q89=10:56, Q90=10:57, Q91=11:00, Q92=11:10, Q93=11:20, Q94=11:30, Q95=11:40, Q96=11:50, Q97=11:51, Q98=11:51, Q99=12:00, Q100=12:10, Q101=12:20, Q102=12:30, Q103=12:40, Q104=12:50, Q105=12:54, Q106=12:54, Q107=13:00, Q108=13:10, Q109=13:20, Q110=13:30, Q111=13:40, Q112=13:50, Q113=14:00
