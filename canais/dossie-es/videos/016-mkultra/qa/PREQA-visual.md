# Pré-QA visual automático

- Alvo: `canais/dossie-es/videos/016-mkultra/out/video.mp4` · 83 quadros (1 a cada 10 s) · modelo `claude-sonnet-5-5` · custo US$ 0.267 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 4 · médio 13 · baixo 19
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:45 | Q05 `f0005.jpg` | medio | anacronismo | Barracões de madeira (estilo temporário de guerra) ao lado do Reflecting Pool, com o Monumento a Washington ao fundo: o lugar é plausível para 1952 (os 'tempos' ficaram até os anos 60), mas o monumento parece sem o Lincoln Memorial/enquadramento exato; vale conferir se o lugar bate com o roteiro. |
| 0:55 | Q06 `f0006.jpg` | medio | anacronismo | Bandeira americana à direita tem estrelas espalhadas em um campo só no canto e listras inclinadas; contagem de estrelas e detalhes imprecisos (possível erro de bandeira de 1952, com 48 estrelas). Dúvida entre estilo e defeito. |
| 1:05 | Q07 `f0007.jpg` | medio | texto_inventado | Caderno com manuscrito borrado e ilegível, escrito pela IA; está desfocado de propósito e dá aspecto de letra falsa, mas não é legível, então o risco é baixo. |
| 1:15 | Q08 `f0008.jpg` | alto | texto_inventado | Documento com texto borrado/ilegível inventado pela IA e um selo circular vermelho com uma águia e letras falsas no canto superior direito. O desfoque disfarça, mas o selo é bem visível e o emblema pode sugerir um país específico. |
| 2:45 | Q17 `f0017.jpg` | medio | elemento_fora | A placa de capítulo 'LA VELADA' cobre o rosto da mulher em primeiro plano, que fica sem cabeça visível. Pode ser enquadramento intencional da placa, mas o corte do personagem chama atenção. |
| 4:35 | Q28 `f0028.jpg` | medio | fundo/faixa | No canto superior direito aparece um bloco/placa lisa bege cortada pela borda (parece um letreiro vazio). Pode ser elemento de cena, mas parece uma faixa chapada estranha. |
| 5:35 | Q34 `f0034.jpg` | medio | texto_inventado | As capas 'Expedientes Secretos' têm microtexto pequeno (legendas e caixas, ex.: 'LA COSA · MOSCÚ, 1945'). As capas laterais #2 e #3 estão com texto borrado e ilegível. É um mockup de capas, então talvez seja intencional, mas o texto dentro da arte foi gerado pela IA. |
| 5:45 | Q35 `f0035.jpg` | alto | texto_encavalado | A placa central 'ENLACE EN LA DESCRIPCIÓN · COMENTARIO FIJADO' cobre o pôster do meio e parte do laptop. O cartaz do meio fica quase ilegível, e a legenda 'DOSSIER EN MINUTOS' dentro da tela do laptop fica cortada na borda inferior direita. Pode ser composição intencional de CTA, mas a sobreposição atrapalha. |
| 5:45 | Q35 `f0035.jpg` | medio | fundo/faixa | Faixa marrom chapada na base (~15% do quadro) abaixo do laptop e do celular, parecendo uma mesa. Pode ser intencional, mas o corte é duro e destoa do fundo azul-escuro. |
| 7:45 | Q47 `f0047.jpg` | medio | anacronismo | A cena é a Cidade do México em 1963, mas os carros parecem mais modernos (frente do carro verde com linhas dos anos 60 tardios) e o prédio de vidro alto parece moderno. O monumento lembra o Anjo da Independência, mas a escultura no topo está distorcida. Na dúvida, registrado como possível imprecisão de lugar/época. |
| 8:35 | Q52 `f0052.jpg` | medio | texto_inventado | A folha na mão do homem tem linhas de texto borrado/pseudo-letras e o calendário na parede tem uma grade sem números. O texto está desfocado e ilegível, então só incomoda se o espectador olhar de perto. Dúvida entre estilo e defeito. |
| 10:45 | Q65 `f0065.jpg` | medio | fundo/faixa | O sinal automático acusou faixa uniforme de 6% na borda direita (RGB 52,75,86). Visualmente é o mar azul-ardósia liso do mapa, que parece fazer parte da cena, sem emenda aparente. Conferir se não é faixa de preenchimento e se o mapa cobre o quadro inteiro. O rótulo TEGUCIGALPA e o ponto vermelho estão certos e legíveis. |
| 11:05 | Q67 `f0067.jpg` | alto | texto_cortado | A plaquinha de nome no canto inferior esquerdo mostra só 'RIC', parece truncada ou incompleta. Se não estiver em animação de digitação, o nome está cortado. Fica também em parte sobre o copo d'água. |
| 12:15 | Q74 `f0074.jpg` | medio | texto_inventado | A linha riscada em vermelho no papel tem texto borrado e pseudo-letras ('RENIL RUDAE ZEEL IE'). Está desfocado e riscado, então provavelmente intencional. Dúvida entre estilo e texto inventado pela IA. |
| 12:35 | Q76 `f0076.jpg` | medio | anacronismo | Redação do Baltimore Sun em 1997 com monitores CRT bege, o que é plausível. Porém a cúpula na janela e a cidade são genéricas e não parecem Baltimore. O cenário também é bem limpo para a época. A legenda 'BALTIMORE SUN, 1997' é rótulo de código e está legível, no canto inferior esquerdo. |
| 12:45 | Q77 `f0077.jpg` | alto | anacronismo | Bandeira azul e branca com duas estrelas visíveis na prateleira à direita, parecida com a de Honduras e com estrelas demais. É bandeira desenhada pela IA, possivelmente errada ou não pedida, num escritório de gabinete. Precisa conferir se o país bate com o roteiro. |
| 12:55 | Q78 `f0078.jpg` | medio | texto_encavalado | Placa de título 'LOS NIÑOS SANTOS' semitransparente, com os personagens e o povoado visíveis através dela. Pode ser transição de entrada (fade) e então não é defeito. Se for estática, a legibilidade do subtítulo 'DOSSIER · MKULTRA · Nº 016' e do carimbo 'CLASIFICADO' fica prejudicada pelo fundo. |

19 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q34 (5:35): faixa uniforme na borda topo: 18% do quadro, cor RGB(18,18,14)
- Q34 (5:35): faixa uniforme na borda base: 13% do quadro, cor RGB(13,14,11)
- Q34 (5:35): faixa uniforme na borda esquerda: 10% do quadro, cor RGB(13,14,11)
- Q34 (5:35): faixa uniforme na borda direita: 10% do quadro, cor RGB(13,14,11)
- Q35 (5:45): faixa uniforme na borda topo: 5% do quadro, cor RGB(14,20,25)
- Q35 (5:45): faixa uniforme na borda base: 15% do quadro, cor RGB(20,16,13)
- Q35 (5:45): faixa uniforme na borda esquerda: 4% do quadro, cor RGB(11,17,20)
- Q36 (5:55): faixa uniforme na borda topo: 8% do quadro, cor RGB(58,72,83)
- Q40 (6:35): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(58,73,79)
- Q40 (6:35): faixa uniforme na borda direita: 4% do quadro, cor RGB(58,72,78)
- Q65 (10:45): faixa uniforme na borda direita: 6% do quadro, cor RGB(52,75,86)

## Quadros

Q01=0:05, Q02=0:15, Q03=0:25, Q04=0:35, Q05=0:45, Q06=0:55, Q07=1:05, Q08=1:15, Q09=1:25, Q10=1:35, Q11=1:45, Q12=1:55, Q13=2:05, Q14=2:15, Q15=2:25, Q16=2:35, Q17=2:45, Q18=2:55, Q19=3:05, Q20=3:15, Q21=3:25, Q22=3:35, Q23=3:45, Q24=3:55, Q25=4:05, Q26=4:15, Q27=4:25, Q28=4:35, Q29=4:45, Q30=4:55, Q31=5:05, Q32=5:15, Q33=5:25, Q34=5:35, Q35=5:45, Q36=5:55, Q37=6:05, Q38=6:15, Q39=6:25, Q40=6:35, Q41=6:45, Q42=6:55, Q43=7:05, Q44=7:15, Q45=7:25, Q46=7:35, Q47=7:45, Q48=7:55, Q49=8:05, Q50=8:15, Q51=8:25, Q52=8:35, Q53=8:45, Q54=8:55, Q55=9:05, Q56=9:15, Q57=9:25, Q58=9:35, Q59=9:45, Q60=9:55, Q61=10:05, Q62=10:15, Q63=10:25, Q64=10:35, Q65=10:45, Q66=10:55, Q67=11:05, Q68=11:15, Q69=11:25, Q70=11:35, Q71=11:45, Q72=11:55, Q73=12:05, Q74=12:15, Q75=12:25, Q76=12:35, Q77=12:45, Q78=12:55, Q79=13:05, Q80=13:15, Q81=13:25, Q82=13:35, Q83=13:45
