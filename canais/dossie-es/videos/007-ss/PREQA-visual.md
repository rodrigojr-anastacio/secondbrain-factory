# Pré-QA visual automático

- Alvo: `canais/dossie-es/videos/007-ss/preqa` · 99 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.227 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 3 · médio 18 · baixo 31
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:15 | Q03 `450.png` | medio | anacronismo | Policiais/guardas de uniforme azul com quepe e cinto vermelho cavando a sepultura; uniformes ambíguos para o contexto (Bertioga, 1979). Há também pequenas manchas e emblemas vermelhos nas golas/braços que podem ser insígnias. Conferir se não lembram insígnias SS. |
| 0:45 | Q08 `1350.png` | medio | anacronismo | Sete homens idênticos de uniforme cinza-azulado com colarinho preto, boné e pequena medalha vermelha no peito, lembrando uniforme paramilitar. Há pequenos distintivos vermelhos no peito, o que pode contrariar a regra de uniformes sem insígnias. Os rostos e poses são quase clonados. |
| 1:35 | Q15 `2850.png` | medio | texto_inventado | A pasta à direita tem etiqueta com rabisco que parece palavra ("Bericht"), e o livro aberto tem tabelas com escrita falsa. Está pequeno e discreto, mas é texto inventado pela IA. Há também dupla exposição fantasma (figuras translúcidas nos cantos), que pode ser crossfade. |
| 2:12 | Q19 `3956.png` | medio | elemento_fora | A placa 'LOS CUCHILLOS' e a aba 'EXPEDIENTE 3' cobrem o rosto do personagem (testa/olhos/nariz). Parece intencional como cartão de capítulo, mas esconde o rosto inteiro; o selo 'CLASIFICADO' encosta na aba. A faixa uniforme no topo (7%, RGB 44,45,41) detectada pelo sinal automático parece ser só o fundo escuro da cena, provável vinheta. |
| 4:35 | Q34 `8250.png` | alto | moldura | Faixa preta vertical na borda esquerda (~5% do quadro, confirmada pelo sinal automático); parece resíduo de letterbox/moldura da imagem de IA e precisa de recorte. |
| 5:05 | Q37 `9150.png` | medio | fundo/faixa | Faixa uniforme no topo (13%, RGB 35,45,50). Parece céu liso escuro da cena, não defeito claro. Registrado por dúvida entre estilo e defeito; conferir se não há emenda visível. |
| 6:05 | Q43 `10950.png` | medio | moldura | Faixa preta fina no topo do quadro (letterbox leve, cerca de 2-3% da altura) acima da sala de aula. Parece resquício de moldura de IA e deve ser recortada. |
| 7:15 | Q50 `13050.png` | medio | texto_inventado | As folhas de papel sobre a mesa têm escrita manuscrita falsa. Ela é ilegível e sem números ou palavras legíveis, então é tolerada pelo contexto. Fica registrada só pela dúvida. |
| 7:25 | Q51 `13350.png` | medio | moldura | O sinal automático indica faixa preta na borda esquerda (6%). Visualmente ela se confunde com a cortina escura da cena. Há dúvida entre estilo e defeito; vale conferir e recortar se for faixa de IA. |
| 7:45 | Q53 `13950.png` | medio | fundo/faixa | O sinal automático acusa faixa uniforme no topo (12%, RGB 51,61,67). Visualmente é céu nublado liso que faz parte da cena, sem emenda evidente. Há dúvida, então fica registrado como médio. |
| 8:55 | Q60 `16050.png` | medio | anacronismo | No soldado da frente há um pequeno emblema vermelho no peito/gola e marcas no capacete. Pode contar como insígnia, contra a regra de uniformes sem insígnias. Verificar. |
| 9:05 | Q61 `16350.png` | medio | anacronismo | Os tanques têm números/marcas brancas no casco e na torre, e um tripulante usa lenço vermelho. Há dúvida se a marcação é insígnia ou detalhe de estilo. A bíblia pede uniformes sem insígnias; conferir. |
| 9:45 | Q65 `17550.png` | medio | elemento_fora | A placa 'EXPEDIENTE 11 / EL PARCHE' cobre o rosto e parte do tronco do homem sentado à esquerda. Pode ser composição intencional de placa de capítulo, mas esconde o personagem. O carimbo 'CLASIFICADO' encosta na borda da placa. |
| 10:15 | Q68 `18450.png` | medio | anacronismo | Os capacetes dos soldados lembram o modelo britânico da Primeira Guerra (tipo Brodie), e as perneiras são de estilo antigo, o que destoa de 1945. A bandeira britânica combina com o contexto. O cartão 'LUGAR Y FECHA' está completo e legível. O emblema vermelho no caminhão é uma insígnia pouco clara. |
| 11:43 | Q77 `21078.png` | medio | valor_errado | Rótulo escreve 'GENOVA' (sem acento) enquanto Q78/Q79 mostram 'GÉNOVA' com acento; marcador sobre a Itália/Mediterrâneo fica ligeiramente deslocado. Inconsistência de grafia entre quadros do mesmo mapa. |
| 11:46 | Q80 `21168.png` | medio | valor_errado | Rótulo 'GENOVA' sem acento, inconsistente com 'GÉNOVA' de Q78/Q79; o mapa volta ao estado inicial sem rota depois de Q79 (t=11:46), possível reinício de animação fora de ordem. |
| 12:25 | Q85 `22350.png` | alto | anacronismo | A cena é de 1983, mas o avião e o carro azul à direita parecem de época indefinida. Os policiais têm uniformes azuis com distintivo vermelho no braço, em estilo genérico moderno. O número '1983' na escada do avião é texto escrito pela IA e não vem do código. |
| 12:45 | Q89 `22950.png` | medio | texto_inventado | O microfone do repórter à direita traz uma bandeirinha com letras ilegíveis e inventadas pela IA. É pequeno, mas dá para notar. |
| 12:55 | Q90 `23250.png` | medio | anacronismo | Soldados de uniforme cinza-azulado em rua de estilo italiano, com um lenço vermelho no pescoço e fogo ao fundo. O contexto é duvidoso: o uniforme pode não corresponder à época ou ao grupo da narração. Sem insígnias legíveis, e o lenço vermelho é pontual e talvez intencional. |
| 13:05 | Q91 `23550.png` | alto | texto_inventado | A placa pendurada no poste à direita, na rua da vila, traz rabiscos que parecem texto inventado e ilegível. As janelas e placas de madeira nas casas ao fundo estão em branco, o que é correto. |
| 14:15 | Q98 `25650.png` | medio | elemento_fora | O círculo vermelho com um traço sobre a capa do livro parece um símbolo inventado, sem relação clara com a cena. Pode ser lido como marca ou emblema. Na dúvida entre estilo e defeito, registro como médio. |

31 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q11 (1:05): faixa uniforme na borda topo: 8% do quadro, cor RGB(79,96,103)
- Q19 (2:12): faixa uniforme na borda topo: 7% do quadro, cor RGB(44,45,41)
- Q26 (3:15): faixa uniforme na borda topo: 5% do quadro, cor RGB(81,89,91)
- Q28 (3:35): faixa uniforme na borda topo: 16% do quadro, cor RGB(68,84,90)
- Q34 (4:35): faixa preta na borda esquerda: 5% do quadro
- Q37 (5:05): faixa uniforme na borda topo: 13% do quadro, cor RGB(35,45,50)
- Q44 (6:15): faixa uniforme na borda topo: 6% do quadro, cor RGB(87,107,114)
- Q45 (6:25): faixa uniforme na borda topo: 5% do quadro, cor RGB(94,102,103)
- Q51 (7:25): faixa preta na borda esquerda: 6% do quadro
- Q53 (7:45): faixa uniforme na borda topo: 12% do quadro, cor RGB(51,61,67)
- Q54 (7:55): faixa uniforme na borda topo: 22% do quadro, cor RGB(44,51,55)
- Q58 (8:35): faixa uniforme na borda topo: 5% do quadro, cor RGB(75,89,96)
- Q61 (9:05): faixa uniforme na borda topo: 8% do quadro, cor RGB(81,99,112)
- Q82 (11:55): faixa uniforme na borda topo: 8% do quadro, cor RGB(68,87,90)
- Q88 (12:35): faixa uniforme na borda topo: 11% do quadro, cor RGB(57,68,75)

## Quadros

Q01=0:02, Q02=0:05, Q03=0:15, Q04=0:25, Q05=0:33, Q06=0:34, Q07=0:35, Q08=0:45, Q09=0:54, Q10=0:55, Q11=1:05, Q12=1:15, Q13=1:24, Q14=1:25, Q15=1:35, Q16=1:45, Q17=1:55, Q18=2:05, Q19=2:12, Q20=2:15, Q21=2:25, Q22=2:35, Q23=2:45, Q24=2:55, Q25=3:05, Q26=3:15, Q27=3:25, Q28=3:35, Q29=3:45, Q30=3:55, Q31=4:05, Q32=4:15, Q33=4:25, Q34=4:35, Q35=4:45, Q36=4:55, Q37=5:05, Q38=5:15, Q39=5:25, Q40=5:35, Q41=5:45, Q42=5:55, Q43=6:05, Q44=6:15, Q45=6:25, Q46=6:35, Q47=6:45, Q48=6:55, Q49=7:05, Q50=7:15, Q51=7:25, Q52=7:35, Q53=7:45, Q54=7:55, Q55=8:05, Q56=8:15, Q57=8:25, Q58=8:35, Q59=8:45, Q60=8:55, Q61=9:05, Q62=9:15, Q63=9:25, Q64=9:35, Q65=9:45, Q66=9:55, Q67=10:05, Q68=10:15, Q69=10:25, Q70=10:35, Q71=10:45, Q72=10:55, Q73=11:05, Q74=11:15, Q75=11:25, Q76=11:35, Q77=11:43, Q78=11:45, Q79=11:45, Q80=11:46, Q81=11:48, Q82=11:55, Q83=12:05, Q84=12:15, Q85=12:25, Q86=12:27, Q87=12:30, Q88=12:35, Q89=12:45, Q90=12:55, Q91=13:05, Q92=13:15, Q93=13:25, Q94=13:35, Q95=13:45, Q96=13:55, Q97=14:05, Q98=14:15, Q99=14:25
