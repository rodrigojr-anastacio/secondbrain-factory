# Pré-QA visual automático

- Alvo: `canais/dossie-es/videos/014-yakuza/preqa` · 95 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.238 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 10 · médio 28 · baixo 39
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:10 | Q03 `315.png` | medio | texto_inventado | O roteiro/caderno nas mãos do diretor tem rabiscos pseudo-japoneses e números ilegíveis escritos pela IA. É pequeno e fica meio desfocado, mas está visível no centro-direita do quadro. |
| 0:20 | Q04 `615.png` | medio | texto_inventado | O medalhão central tem um padrão de glifos/labirinto que lembra uma escrita falsa. Pode ser só ornamento decorativo; na dúvida registro como estilo discutível. |
| 1:10 | Q10 `2115.png` | alto | anacronismo | Cena de fosso e muralhas de castelo japonês (estilo Edo), mas ao fundo aparece um skyline de arranha-céus modernos. Se o contexto for período Edo, é anacronismo claro. |
| 1:20 | Q11 `2415.png` | medio | anacronismo | Faixas e cartazes dos manifestantes estão em branco, o que é correto. Há bandeiras vermelhas e braçadeiras vermelhas, e se o contexto for o Japão, o cenário parece uma fábrica ocidental de tijolos. Pode ser lugar errado, então vale conferir a intenção. |
| 1:38 | Q13 `2940.png` | medio | elemento_fora | A placa de título 'LA CELDA' cobre a maior parte do quadro e esconde os rostos e o alto dos homens de casaco. Provavelmente é intencional, como placa de capítulo, mas vale checar. Os textos em espanhol estão legíveis e nada está cortado. |
| 1:40 | Q14 `3015.png` | medio | anacronismo | Soldado de capacete e uniforme azul-acinzentado, de costas, diante de uma prisão com arame farpado. Em 'Tokio, 1948' o uniforme não parece nitidamente de ocupação americana ou japonesa. Dúvida entre estilo e defeito. |
| 1:50 | Q15 `3315.png` | medio | anacronismo | Bandeira vermelha no mastro, no canto superior direito, sem identificação. Soldados ao fundo com uniformes verde-oliva e detalhes vermelhos. Pode ser anacronismo ou lugar errado para Tóquio 1948. Dúvida entre estilo e defeito. |
| 2:00 | Q16 `3615.png` | medio | anacronismo | Guardas com casacos verdes e braçadeiras ou detalhes vermelhos, e emblemas nos pilares do portão com marcas ilegíveis. Os uniformes podem não corresponder a Tóquio 1948. Dúvida entre estilo e defeito. |
| 2:35 | Q20 `4637.png` | medio | fundo/faixa | O sinal automático apontou faixa uniforme no topo (cor RGB 91,89,76, ~18% do quadro). É um céu liso e acinzentado atrás da cena, então provavelmente faz parte do estilo e não é defeito. Fica registrado por dúvida: a transição para os prédios é abrupta, parece um bloco chapado. |
| 3:30 | Q26 `6315.png` | medio | texto_inventado | Lanternas vermelhas penduradas no alto (canto superior esquerdo e direito) trazem símbolos/letras tipo caractere japonês inventado pela IA; pequenos, mas visíveis. Placas pequenas nas paredes laterais também com marcas ilegíveis. |
| 3:50 | Q29 `6915.png` | alto | fundo/faixa | Faixa preta chapada na borda esquerda (~8% do quadro) que se funde ao fundo escuro e corta o cone de luz; sinal automático confirma. Possível moldura/letterbox lateral da imagem de IA. Pode ser escuridão de palco intencional, mas a borda é suspeita. |
| 4:00 | Q30 `7215.png` | medio | moldura | Laterais esquerda e direita do palco com blocos pretos grandes e cantos superiores pretos; pode ser cortina/enquadramento de cena, mas parece faixa preta nas bordas. Dúvida entre estilo e defeito. |
| 4:20 | Q32 `7815.png` | medio | anacronismo | Aviões-modelo na prateleira com logotipo vermelho em forma de 'X'/estrela na cauda: marca/insígnia inventada. O texto 'JAL' é falso/ilegível. Teto com luminárias fluorescentes modernas e cadeira de escritório com rodinhas, possivelmente moderno demais para a época. |
| 4:50 | Q36 `8715.png` | medio | texto_inventado | Os papéis na mesa têm linhas de escrita ilegível/falsa gerada pela IA e carimbos vermelhos com símbolos inventados. Está pequeno e borrado, sem leitura possível, então fica como dúvida entre estilo e defeito. |
| 5:40 | Q42 `10215.png` | medio | anacronismo | Casa em estilo enxaimel (meia-madeira) europeu, com bandeira vermelha rasgada e carro antigo, no lugar de um cenário japonês. Lugar aparentemente errado para um tema de kamikaze/Japão; confirmar se a cena é intencional. |
| 6:00 | Q44 `10815.png` | medio | texto_inventado | Caligrafia japonesa falsa no quadro pendurado à esquerda e nos papéis da parede. Está discreta e em estilo de tinta, mas é texto inventado pela IA. |
| 6:10 | Q45 `11115.png` | alto | texto_inventado | Jornais e revistas do quiosque têm manchetes com caracteres pseudo-japoneses ilegíveis e números sem sentido (ex.: "8I8-81"). Também há letreiros inventados nos prédios ao fundo. Texto falso bem visível. |
| 6:30 | Q48 `11715.png` | alto | texto_inventado | Calendário com cabeçalho em caracteres falsos, e escrita inventada "1992" na mesa com caracteres pseudo-japoneses. Os números do calendário são incoerentes (sequência truncada). |
| 6:30 | Q48 `11715.png` | medio | outro | Sobreposição de várias camadas translúcidas e retângulos com contornos fantasma por toda a cena. Pode ser um crossfade entre duas cenas, o que não seria defeito. Se for um frame parado, é defeito. |
| 6:50 | Q50 `12315.png` | medio | texto_inventado | Livro aberto com tabelas e caracteres pseudo-japoneses ilegíveis nas páginas, pergaminho na parede e carimbo vermelho no canto inferior esquerdo. Texto falso escrito pela IA, mas ilegível e em segundo plano, como textura do livro. |
| 7:30 | Q54 `13515.png` | medio | anacronismo | Monitores CRT nas mesas laterais da sala de tribunal. Confirmar se a época da cena (julgamento) condiz. As plaquetas de nome nas mesas têm rabiscos ilegíveis, pequenos. |
| 7:50 | Q56 `14100.png` | alto | texto_encavalado | A placa de capítulo 'LA ASAMBLEA' cobre parte da cena, e o carimbo 'CLASIFICADO' invade o canto superior direito da placa, sobrepondo-se à fileira de homens sentados. Há também um pequeno bloco vermelho pixelado no topo esquerdo, atrás da placa, que parece artefato. |
| 7:50 | Q57 `14115.png` | medio | texto_inventado | As plaquinhas de nome na mesa da diretoria (fileira do fundo) têm rabiscos ilegíveis escritos pela IA, e há pixels vermelhos soltos no canto superior esquerdo. Ficam pequenos e discretos atrás da placa de capítulo. |
| 8:10 | Q59 `14715.png` | alto | texto_inventado | O documento ornamentado em primeiro plano tem texto borrado e ilegível no centro, e os cartazes na parede e na janela mostram manchas parecidas com texto. Parece letra inventada pela IA. |
| 8:20 | Q60 `15015.png` | alto | texto_inventado | A placa acima da porta do prédio ao fundo mostra letras falsas e ilegíveis (algo como 'LEAS T B IZ&'). Os ícones das caixas de papelão também são rabiscos. Falta ainda o rótulo do código no lugar da placa. |
| 8:30 | Q61 `15315.png` | medio | anacronismo | A cena parece do século XIX (vestido vitoriano, pena, rolos lacrados), mas o tema é Yakuza moderno. Há dúvida se é estilo ou erro de época. O livro aberto e os rolos têm texto falso em linhas ilegíveis. |
| 8:50 | Q63 `15888.png` | medio | anacronismo | O cenário é um hospital com palmeiras, estilo Califórnia/UCLA, que aparentemente corresponde ao transplante de fígado. Há dúvida se é intencional. A placa à direita, em branco, está ok. |
| 9:10 | Q66 `16515.png` | medio | texto_inventado | No livro/passaporte aberto há a palavra "VISA" escrita pela IA e texto borrado ilegível nas páginas e no carimbo. É pequeno e desfocado, mas é texto gerado pela IA. Em espanhol seria "VISADO". O rótulo deveria vir do código. |
| 9:30 | Q68 `17115.png` | medio | texto_inventado | A carta sobre a mesa tem caracteres borrados ilegíveis simulando escrita. Está desfocada e discreta, mas é texto falso gerado pela IA. |
| 9:40 | Q69 `17415.png` | alto | anacronismo | O avião a jato de quatro motores (estilo DC-8/Boeing 707) está ao lado de aviões de hélice e uniformes de aparência antiga. A mistura de época fica estranha, e a legenda do contexto sugere cenário atual ou outro período. A fumaça sai de trás das asas, como num lançamento, e não de motores a jato. |
| 10:00 | Q72 `18015.png` | medio | moldura | Faixa preta larga na borda esquerda (~6%), que parece uma parede de tijolos muito escura. Pode ser enquadramento intencional da cela, mas está chapada e lembra a faixa preta de letterbox da IA. Dúvida entre estilo e defeito; vale recortar ou conferir. |
| 10:10 | Q73 `18315.png` | medio | outro | Dupla exposição: avião e montanhas translúcidos sobrepostos à sala do tribunal, e uma faixa de texto minúsculo ilegível na frente da bancada. Pode ser crossfade entre cenas; se for imagem única, a cena fica confusa. |
| 10:30 | Q75 `18915.png` | alto | texto_inventado | Placa do carro de polícia traz 'CUB' (letras inventadas pela IA) e há cartazes com rabiscos de texto falso na parede à esquerda e um jornal no banco. Os letreiros em branco nas paredes são aceitáveis. |
| 11:28 | Q82 `20644.png` | medio | outro | A placa de capítulo 'LA SENTENCIA' cobre quase toda a parte central da sala de tribunal e as figuras sentadas atrás dela. É provável que seja um estilo intencional, mas a cena fica bem tapada. |
| 12:20 | Q88 `22215.png` | alto | outro | A imagem inteira tem sobreposição de linhas e grades, com duplicação de elementos como câmeras, janelas e pessoas, como se fosse uma dupla exposição. Pode ser crossfade entre duas cenas, mas parece um artefato de IA. Se for um quadro parado, é defeito. Confirmar se é transição. |
| 12:22 | Q89 `22254.png` | medio | elemento_fora | A placa de capítulo 'LA PUERTA' cobre o centro da cena (a mesa de assinatura e os rostos). O carimbo vermelho 'CLASIFICADO' invade a borda superior direita da placa e sobrepõe a aba 'EXPEDIENTE CERRADO'. É provável que seja design intencional de placa de capítulo; registrado por dúvida de sobreposição. |
| 12:40 | Q91 `22815.png` | medio | texto_inventado | No livro aberto, o gráfico de barras tem rótulos borrados e ilegíveis no eixo, e há cartazes com caracteres falsos na parede de fundo. Estão discretos e escuros, mas são texto pseudo-legível da IA. O uniforme do oficial também tem um distintivo ilegível. |
| 13:00 | Q93 `23415.png` | medio | texto_inventado | Os recortes de jornal na parede, as lombadas dos livros e a folha de escrita têm texto/rabisco falso da IA. O texto é pequeno e fica em segundo plano, mas é legível como pseudoletra. |

39 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q05 (0:30): faixa uniforme na borda topo: 4% do quadro, cor RGB(77,87,79)
- Q20 (2:35): faixa uniforme na borda topo: 18% do quadro, cor RGB(91,89,76)
- Q23 (3:00): faixa uniforme na borda base: 7% do quadro, cor RGB(53,66,71)
- Q29 (3:50): faixa preta na borda esquerda: 8% do quadro
- Q37 (5:00): faixa uniforme na borda topo: 11% do quadro, cor RGB(74,90,100)
- Q37 (5:00): faixa uniforme na borda base: 7% do quadro, cor RGB(56,64,57)
- Q39 (5:17): faixa uniforme na borda topo: 21% do quadro, cor RGB(45,58,62)
- Q40 (5:20): faixa uniforme na borda topo: 6% do quadro, cor RGB(87,108,116)
- Q43 (5:50): faixa uniforme na borda topo: 6% do quadro, cor RGB(30,34,39)
- Q52 (7:10): faixa uniforme na borda topo: 14% do quadro, cor RGB(83,99,106)
- Q69 (9:40): faixa uniforme na borda topo: 19% do quadro, cor RGB(31,41,50)
- Q70 (9:46): faixa uniforme na borda base: 6% do quadro, cor RGB(45,49,48)
- Q72 (10:00): faixa preta na borda esquerda: 6% do quadro

## Quadros

Q01=0:00, Q02=0:01, Q03=0:10, Q04=0:20, Q05=0:30, Q06=0:39, Q07=0:40, Q08=0:50, Q09=1:00, Q10=1:10, Q11=1:20, Q12=1:30, Q13=1:38, Q14=1:40, Q15=1:50, Q16=2:00, Q17=2:10, Q18=2:20, Q19=2:30, Q20=2:35, Q21=2:40, Q22=2:50, Q23=3:00, Q24=3:10, Q25=3:20, Q26=3:30, Q27=3:35, Q28=3:40, Q29=3:50, Q30=4:00, Q31=4:10, Q32=4:20, Q33=4:24, Q34=4:30, Q35=4:40, Q36=4:50, Q37=5:00, Q38=5:10, Q39=5:17, Q40=5:20, Q41=5:30, Q42=5:40, Q43=5:50, Q44=6:00, Q45=6:10, Q46=6:20, Q47=6:21, Q48=6:30, Q49=6:40, Q50=6:50, Q51=7:00, Q52=7:10, Q53=7:20, Q54=7:30, Q55=7:40, Q56=7:50, Q57=7:50, Q58=8:00, Q59=8:10, Q60=8:20, Q61=8:30, Q62=8:40, Q63=8:50, Q64=8:50, Q65=9:00, Q66=9:10, Q67=9:20, Q68=9:30, Q69=9:40, Q70=9:46, Q71=9:50, Q72=10:00, Q73=10:10, Q74=10:20, Q75=10:30, Q76=10:40, Q77=10:41, Q78=10:50, Q79=11:00, Q80=11:10, Q81=11:20, Q82=11:28, Q83=11:30, Q84=11:40, Q85=11:50, Q86=12:00, Q87=12:10, Q88=12:20, Q89=12:22, Q90=12:30, Q91=12:40, Q92=12:50, Q93=13:00, Q94=13:10, Q95=13:20
