# Pré-QA visual automático

- Alvo: `canais/dossie-es/videos/015-gru/preqa` · 120 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.286 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 9 · médio 29 · baixo 42
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:01 | Q01 `20.png` | medio | texto_inventado | Letreiro de destino na frente do bonde (centro) traz texto ilegível/inventado pela IA ('FIJID MER' ou similar); pequeno, mas visível. Além disso, óculos escuros em vários homens em primeiro plano parecem estranhos para a época. |
| 0:01 | Q02 `40.png` | medio | texto_inventado | Mesmo quadro de Q01: letreiro do bonde com texto inventado/ilegível no centro da imagem. |
| 0:02 | Q03 `48.png` | medio | texto_inventado | Letreiro do bonde com texto falso ilegível ('LING MER' ou similar) no centro. |
| 0:02 | Q04 `60.png` | medio | texto_inventado | Letreiro do bonde com texto inventado ilegível no centro da imagem. |
| 0:21 | Q06 `620.png` | alto | texto_inventado | Passaporte com 'PASSPORT' em inglês e carimbo circular com letras falsas/ilegíveis; texto manuscrito inventado no papel e na etiqueta no canto inferior esquerdo. Rosto da foto borrado. |
| 0:33 | Q08 `976.png` | alto | valor_errado | No mapa, 'BRUSELAS' está sem acento correto (grafia correta 'BRUSELAS' é aceita, mas o ponto de Bruselas e La Haya fica muito próximo e as caixas quase se encostam). O ponto de 'NÁPOLES' está no leste do Mediterrâneo, na região da Grécia/Turquia, e não na Itália; localização geográfica errada. Também 'MONTEVIDEO' fica no oceano, deslocado da costa. |
| 0:49 | Q10 `1464.png` | medio | elemento_fora | A placa de título "EL MARINERO" cobre a parte de cima do carro e os pedestres do centro. Provavelmente é intencional (placa de capítulo), mas o carro ficou cortado pela placa; confirmar o enquadramento. |
| 1:03 | Q14 `1882.png` | medio | anacronismo | Soldados com sobretudos e chapéus de pele em marcha com bandeiras brancas lisas, em São Petersburgo em novembro de 1918. As bandeiras sem símbolo são aceitáveis, mas o uniforme cinza-verde com gola vermelha parece mais soviético tardio do que de 1918. Dúvida entre estilo e defeito. |
| 1:59 | Q23 `3581.png` | alto | valor_errado | No mapa, o ponto e o rótulo 'PARÍS' estão no oeste da França, perto da costa da Bretanha/Normandia, e não na posição real de Paris (norte-central, logo abaixo de Bruxelas). A rota Bruxelas–Paris também fica estranha. |
| 1:59 | Q23 `3581.png` | medio | texto_encavalado | Os rótulos 'ÁMSTERDAM' e 'BRUSELAS' e as linhas da rota se amontoam e se sobrepõem na região do Benelux. Os pontos quase se tocam, o que prejudica a leitura. |
| 1:59 | Q23 `3581.png` | medio | fundo/faixa | Dobras de papel visíveis e um bloco chapado bege/branco ocupam o lado esquerdo e o oceano. Pode ser intencional (mapa em papel), mas há dúvida se o fundo liso e as faixas retas ficaram como defeito. |
| 2:31 | Q28 `4520.png` | alto | texto_inventado | A fachada à direita tem letreiro com texto falso da IA, "OFL·MER CARS", legível e sem sentido. A placa grande pendurada acima do homem na escada está em branco, o que é correto. |
| 2:57 | Q32 `5308.png` | alto | texto_inventado | Os letreiros das lojas nos dois lados da rua têm letras inventadas e ilegíveis: "XRNDIE SPUNFL", "DULPEINUE", "ZOBRIDE III", "DALBALCIE". Também há cartazes com rabiscos falsos na parede à esquerda. |
| 3:11 | Q34 `5720.png` | medio | anacronismo | Há uma bandeira vermelha lisa no canto superior direito e guardas com braçadeira vermelha. Pode ser coerente com a URSS dos anos 40, mas a bandeira está sem emblema. Na dúvida entre estilo e defeito, registro como médio. As placas e o quadro da porta ficaram em branco, o que é correto. |
| 3:15 | Q35 `5854.png` | medio | texto_inventado | No casco do barco do primeiro plano, à esquerda, há um registro ilegível em letras falsas. Há também bandeirinhas minúsculas nos mastros. O rótulo 'MARSELLA, 1942' é do código e está legível. A faixa de 6% no topo é só céu nublado liso, sem defeito. |
| 4:01 | Q41 `7220.png` | medio | anacronismo | Legenda 'SAN PETERSBURGO, 2009' sobre cena de canal. Não há defeito claro, mas é cena de época atual em estilo graphic novel; sem letreiros inventados visíveis. Dúvida menor: placa vertical à direita (perto da porta, x~935) com marcações ilegíveis. |
| 4:31 | Q47 `8120.png` | medio | outro | Os dois homens têm ternos, gravatas e posturas quase idênticos e rostos parecidos com figuras reais; dúvida entre estilo e defeito de coerência (parecem duplicados). Cúpula do Capitólio ao fundo ok. |
| 5:26 | Q56 `9769.png` | medio | valor_errado | Mapa do Caribe: o rótulo LOURDES e o ponto vermelho ficam no oeste de Cuba, perto de Havana/Pinar del Río. A base de Lourdes fica nos arredores de Havana, então a posição parece aceitável, mas a linha liga ao 'Cayos de Florida' em arco, e vale conferir a geografia. Dúvida: pode ser estilo intencional. |
| 5:51 | Q59 `10520.png` | medio | elemento_fora | Placa dourada grande e em branco flutua no meio do corredor, pendurada sem suporte visível, tapando a perspectiva. Pode ser um espaço reservado para rótulo do código; se o rótulo não for sobreposto, fica uma placa vazia estranha. Placas menores nas portas também estão vazias. |
| 6:01 | Q60 `10820.png` | medio | anacronismo | Figura real (Putin) reconhecível, com legenda 'VLADIMIR PUTIN' no canto inferior esquerdo. A etiqueta fica colada na borda esquerda e na base, perto do limite do quadro. Dois painéis em branco na parede atrás dele parecem espaços vazios. |
| 6:30 | Q64 `11698.png` | alto | texto_inventado | Letreiros das lojas com texto falso ou ilegível: placa no alto à direita ('...KEROS TRASATLÁN...' ilegível), placa 'SUNCA BANC' à esquerda e letras no toldo verde esquerdo. Tipografia inventada pela IA, visível em fachadas. |
| 6:31 | Q65 `11720.png` | alto | texto_inventado | As placas das lojas ao fundo têm letras falsas e ilegíveis: placa redonda à esquerda, placa retangular no alto à direita com rabiscos e toldos verdes com marcas tipo 'HR'. A IA inventou o texto. |
| 6:31 | Q65 `11720.png` | medio | anacronismo | Serguéi Skripal aparece como um homem jovem, de terno azul e cabelo penteado, em uma rua de cidade espanhola. Não bate com a figura real, e a dúvida é se isso é estilo ou erro de lugar/personagem. |
| 6:41 | Q66 `12020.png` | medio | outro | Os dois homens são quase idênticos (mesmo rosto, terno e pose espelhada). Pode ser intencional (dupla/disfarce), mas parece clone de IA. A garrafa tem rótulo branco em branco, aceitável. |
| 7:15 | Q70 `13056.png` | medio | elemento_fora | A placa de capítulo 'EL BAILE' cobre boa parte da cena. O letreiro 'HOTEL' no prédio à esquerda é texto da IA e aparece cortado e inclinado. A placa 'EXPEDIENTE 8' / 'CLASIFICADO' está legível e não é defeito. |
| 7:19 | Q71 `13157.png` | medio | texto_encavalado | Dois rótulos ao mesmo tempo: 'LUGAR Y FECHA / NÁPOLES, 2015' no canto superior esquerdo e 'MARÍA ADELA KUHFELDT RIVERA' embaixo. Estão separados e legíveis, mas o rótulo de cima sobrepõe o lustre. Vale checar se são dois elementos duplicados. |
| 7:21 | Q72 `13220.png` | medio | anacronismo | A cliente usa vestido e penteado do século XIX, enquanto o vendedor veste traje de época. A cena parece não bater com o contexto moderno do vídeo (Nápoles, 2015). Dúvida entre estilo e erro de época. |
| 7:51 | Q74 `14120.png` | medio | anacronismo | Lima, Perú: palmeiras e ruas de pedra com capa verde e faixa vermelha são plausíveis, mas a vestimenta dos figurantes é ambígua quanto à época (colonial/republicana). Confira se bate com o período do roteiro. Na dúvida entre estilo e defeito. |
| 8:51 | Q83 `15920.png` | medio | texto_inventado | O calendário na parede (alto, à direita) mostra uma grade de números e uma figura impressa, com texto/numeração gerado pela IA, não legível. Também há um quadro pequeno na parede à esquerda com imagem indefinida. Discreto, mas é texto inventado em calendário. |
| 9:13 | Q86 `16576.png` | medio | fundo/faixa | O sinal automático acusa faixa uniforme no topo (7%, RGB 41,49,54). No quadro, o topo parece céu escuro de tempestade, que combina com a cena, mas a faixa pode ser uma borda chapada da imagem de IA. Conferir o recorte; na dúvida entre estilo e defeito, registrado como médio. |
| 9:31 | Q88 `17120.png` | alto | anacronismo | O laptop no centro tem a logo vermelha da maçã (marca Apple) visível. É marca real em objeto moderno, a cor destoa da paleta e pode ser anacrônica para o tema GRU/Guerra Fria. Se a cena não for contemporânea, trocar a imagem ou pedir 'laptop sem logotipo'. |
| 9:39 | Q89 `17382.png` | medio | valor_errado | Rótulo 'MOSCÚ' (com acento espanhol) está cortado no fim: aparece como 'MOSCÚ' sem o resto da caixa folgada, e 'KIEV' está escrito 'KIEV' mas o mapa do canal é em espanhol; Kiev fica deslocada para o oeste do Dnieper e Moscou está posicionada bem ao norte/leste do real (curva ligando pontos geograficamente imprecisos). Dúvida: pode ser estilo, mas a posição dos pontos não bate com a geografia. |
| 9:41 | Q90 `17420.png` | medio | texto_inventado | Tabuleiro de xadrez tem letras e números inventados pela IA nas bordas ('H B C C F F B', '3', '9', '2', '1') fora de ordem; legíveis mas sem sentido. Também há uma faixa escura fina no topo (4%) que parece parte da cena escura, provavelmente vinheta. |
| 10:21 | Q94 `18643.png` | medio | texto_encavalado | Placa de capítulo 'LA PISTA' cobre boa parte do fundo, incluindo a ponte e o topo do carro; faixa uniforme cinza-azulada no topo (7%) é céu liso da cena, provável estilo. Placas de estrada à direita em branco/escuras sem texto. Carro e viatura em estilo moderno (Volvo/viatura) podem destoar de época, mas sem evidência clara. |
| 10:51 | Q99 `19520.png` | medio | texto_inventado | Na tela do monitor há um post-it com rabiscos que imitam escrita, e a tela de login traz campos com 'LOGIN' e fileiras de círculos. É texto/UI desenhado pela IA. A palavra LOGIN está legível e o resto é só garatuja, então é discreto e pode ser intencional. |
| 11:57 | Q109 `21504.png` | alto | valor_errado | Mapa de México/Caribe: o rótulo 'CIUDAD DE MÉXICO' e o ponto vermelho estão sobre o Golfo/lado do Golfo de México, perto da costa de Veracruz, não no altiplano central onde fica a capital. Há também uma linha vermelha solta e pontos vermelhos aleatórios sem explicação. Confira o posicionamento do marcador. |
| 12:51 | Q115 `23120.png` | medio | texto_inventado | Janelas, porta e escada do avião têm retângulos brancos chapados. Os faróis da van e o motor também. Parecem placeholders ou janelas sem textura. A placa lateral do avião está em branco, o que é correto. Também há dúvida de estilo: o Putin reconhecível em primeiro plano é uma figura real. |
| 13:11 | Q118 `23720.png` | medio | texto_inventado | O documento em primeiro plano tem linhas simuladas de texto e um selo ilegível no canto inferior direito com letras falsas. Em geral lê-se como estilo, mas o selo tem escrita inventada. |

42 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q15 (1:16): faixa uniforme na borda topo: 10% do quadro, cor RGB(85,102,106)
- Q16 (1:21): faixa uniforme na borda topo: 4% do quadro, cor RGB(141,151,141)
- Q25 (2:11): faixa uniforme na borda topo: 4% do quadro, cor RGB(50,60,67)
- Q35 (3:15): faixa uniforme na borda topo: 6% do quadro, cor RGB(83,98,106)
- Q36 (3:31): faixa uniforme na borda esquerda: 4% do quadro, cor RGB(60,72,75)
- Q39 (3:47): faixa uniforme na borda topo: 12% do quadro, cor RGB(74,84,85)
- Q49 (4:51): faixa uniforme na borda topo: 11% do quadro, cor RGB(71,90,101)
- Q50 (4:51): faixa uniforme na borda topo: 10% do quadro, cor RGB(73,89,102)
- Q53 (5:18): faixa uniforme na borda topo: 11% do quadro, cor RGB(42,52,58)
- Q86 (9:13): faixa uniforme na borda topo: 7% do quadro, cor RGB(41,49,54)
- Q90 (9:41): faixa preta na borda topo: 4% do quadro
- Q94 (10:21): faixa uniforme na borda topo: 7% do quadro, cor RGB(55,62,67)
- Q95 (10:22): faixa uniforme na borda topo: 7% do quadro, cor RGB(55,62,67)
- Q96 (10:22): faixa uniforme na borda topo: 7% do quadro, cor RGB(55,62,67)
- Q101 (11:11): faixa uniforme na borda topo: 7% do quadro, cor RGB(80,99,106)
- Q104 (11:41): faixa uniforme na borda topo: 13% do quadro, cor RGB(49,64,79)
- Q114 (12:41): faixa uniforme na borda base: 6% do quadro, cor RGB(68,81,87)
- Q115 (12:51): faixa uniforme na borda topo: 6% do quadro, cor RGB(47,59,69)

## Quadros

Q01=0:01, Q02=0:01, Q03=0:02, Q04=0:02, Q05=0:11, Q06=0:21, Q07=0:24, Q08=0:33, Q09=0:41, Q10=0:49, Q11=0:50, Q12=0:53, Q13=1:01, Q14=1:03, Q15=1:16, Q16=1:21, Q17=1:25, Q18=1:31, Q19=1:41, Q20=1:41, Q21=1:44, Q22=1:54, Q23=1:59, Q24=2:01, Q25=2:11, Q26=2:16, Q27=2:21, Q28=2:31, Q29=2:40, Q30=2:40, Q31=2:41, Q32=2:57, Q33=3:01, Q34=3:11, Q35=3:15, Q36=3:31, Q37=3:36, Q38=3:37, Q39=3:47, Q40=3:51, Q41=4:01, Q42=4:01, Q43=4:15, Q44=4:16, Q45=4:21, Q46=4:27, Q47=4:31, Q48=4:38, Q49=4:51, Q50=4:51, Q51=4:58, Q52=5:01, Q53=5:18, Q54=5:19, Q55=5:19, Q56=5:26, Q57=5:31, Q58=5:41, Q59=5:51, Q60=6:01, Q61=6:11, Q62=6:21, Q63=6:21, Q64=6:30, Q65=6:31, Q66=6:41, Q67=7:00, Q68=7:01, Q69=7:11, Q70=7:15, Q71=7:19, Q72=7:21, Q73=7:41, Q74=7:51, Q75=7:51, Q76=8:01, Q77=8:21, Q78=8:25, Q79=8:26, Q80=8:33, Q81=8:41, Q82=8:43, Q83=8:51, Q84=9:10, Q85=9:11, Q86=9:13, Q87=9:21, Q88=9:31, Q89=9:39, Q90=9:41, Q91=9:51, Q92=10:01, Q93=10:11, Q94=10:21, Q95=10:22, Q96=10:22, Q97=10:31, Q98=10:41, Q99=10:51, Q100=10:57, Q101=11:11, Q102=11:15, Q103=11:21, Q104=11:41, Q105=11:44, Q106=11:44, Q107=11:44, Q108=11:51, Q109=11:57, Q110=12:00, Q111=12:11, Q112=12:21, Q113=12:31, Q114=12:41, Q115=12:51, Q116=12:55, Q117=12:56, Q118=13:11, Q119=13:21, Q120=13:31
