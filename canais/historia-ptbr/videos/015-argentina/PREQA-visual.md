# Pré-QA visual automático

- Alvo: `canais/historia-ptbr/videos/015-argentina/preqa` · 103 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.231 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 2 · médio 14 · baixo 32
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:00 | Q01 `15.png` | medio | outro | O rótulo '1992' no canto superior esquerdo fica semitransparente sobre a planta e a estante, com legibilidade fraca. Pode ser um título intencional, mas o contraste está baixo e a caixa se mistura ao fundo. |
| 0:30 | Q04 `915.png` | medio | anacronismo | Cena de época com bonde, carruagem e um automóvel antigo ao fundo. Misturar carruagem e carro antigo na mesma rua pode ser aceitável, mas vale checar a coerência da época. |
| 1:20 | Q09 `2415.png` | medio | elemento_fora | Rótulo 'POTOSÍ → BUENOS AIRES' está no canto inferior esquerdo, sobre a costa e a cordilheira, tapando parte do mapa. A seta '→' é pequena e fraca. Potosí fica na Bolívia, mas a linha pontilhada parte de um ponto sobre os Andes, sem marcador de origem. O trajeto parece aproximado. |
| 2:30 | Q16 `4515.png` | medio | elemento_fora | A placa de capítulo 'CAPÍTULO 2 / A primeira conta' cobre o rosto e o corpo do terceiro bonequinho da esquerda, em primeiro plano. A placa '1824' no canto superior esquerdo também cobre parte do poste de luz. A sobreposição é aceitável, mas esconde personagens. |
| 3:30 | Q22 `6315.png` | alto | outro | Quadro com várias camadas semitransparentes sobrepostas (duplo/triplo): praça, multidão com cartolas e grade/carruagem se misturam. Pode ser crossfade entre cenas, que não é defeito, mas está em t=3:30 sem transição evidente e ilegível como imagem estática. Confirmar se é só a transição; se for imagem fixa, é emenda quebrada. |
| 5:10 | Q32 `9315.png` | medio | outro | A cena parece mesclar duas imagens: à esquerda uma rua externa com carruagem, à direita um salão interno com lustres, sem divisão arquitetônica coerente. Na dúvida entre estilo e emenda, fica como risco de composição estranha. Também há um bilhete com rabiscos no canto inferior direito sobre uma travessa, elemento solto. |
| 6:30 | Q40 `11715.png` | medio | outro | O estilo é diferente dos outros quadros: traço mais limpo e de alto contraste, sem o cenário detalhado. Os bonecos estão muito ampliados e cortados pelas bordas, e o pergaminho vazio ocupa o centro. Pode ser enquadramento intencional, mas vale conferir se combina com a sequência. |
| 6:40 | Q41 `12015.png` | medio | elemento_fora | A placa de capítulo "CAPÍTULO 5 / A algema de ouro" cobre a parte inferior central da cena e esconde parte dos deputados e da mesa. É sobreposição de overlay com a ilustração, mas parece intencional como cartela de capítulo; o selo "1899" no canto superior esquerdo está ok. |
| 7:10 | Q44 `12915.png` | medio | anacronismo | A cena mostra uma rua com bondes e um automóvel preto, fiacre puxado a cavalo e prédios haussmannianos em estilo parisiense, mas o contexto é a Argentina de 1899-1900. O carro parece um Ford T, que é posterior a 1900. Há dúvida se é Buenos Aires: a arquitetura lembra Paris, e o veículo é possivelmente anacrônico. |
| 8:30 | Q52 `15315.png` | medio | texto_inventado | A carta tem rabiscos ilegíveis que imitam escrita, e a assinatura embaixo também é falsa. Como não dá para ler como texto real, passa como garrancho de estilo. Registrado como dúvida entre estilo e defeito. |
| 9:40 | Q59 `17415.png` | medio | anacronismo | O obelisco de Buenos Aires aparece ao fundo (já existe em 1946, então é plausível). Ainda assim, o balcão rosa lembra a Casa Rosada. O rótulo 'JUAN PERÓN' no canto inferior esquerdo está sobre a multidão e cobre parte dos personagens. Isso é texto de código e provavelmente intencional, mas a caixa tapa rostos da multidão. |
| 11:20 | Q69 `20415.png` | medio | fundo/faixa | Fundo bege chapado ocupa quase todo o quadro acima da maquete, com faixa uniforme na borda esquerda. Pode ser fundo intencional de ilustração conceitual, mas parece vazio e sem textura. Na dúvida entre estilo e defeito, fica como médio. |
| 12:20 | Q75 `22215.png` | medio | texto_inventado | Rótulo 'PESO ARGENTINO · -4 ZEROS' está em inglês/misto num vídeo em português (deveria ser 'ZEROS'→'zeros' em PT) e cobre parte da cédula na mesa. A cédula tem círculo vazio sem texto legível. Placa '1983' ok. |
| 12:40 | Q77 `22815.png` | alto | texto_encavalado | Placa de capítulo 'CAPÍTULO 9 / O décimo terceiro zero' está semitransparente e sobreposta ao personagem e à mesa, com baixo contraste; a leitura fica difícil. O rótulo '1985' no canto superior esquerdo está quase invisível sobre as estantes. Pode ser transição de entrada (fade), por isso não é bloqueante. |
| 13:20 | Q81 `24015.png` | medio | fundo/faixa | Fundo bege liso ocupa ~19% do topo e uma faixa fina na esquerda. Parece parte da cena (parede/fundo de cartum, mesa em perspectiva), não um defeito de borda. Registrado por dúvida entre estilo e defeito. A cesta da direita e o maço de notas cortados na borda são enquadramento normal. |
| 15:20 | Q93 `27615.png` | medio | fundo/faixa | O fundo bege liso ocupa o topo e a lateral esquerda (RGB ~246,238,210), como um fundo vazio atrás da máquina de dinheiro. Não há mapa nem 3D, então provavelmente é cenário liso intencional, mas a composição fica vazia e parece uma faixa chapada. Dúvida entre estilo e defeito. |

32 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q11 (1:40): faixa uniforme na borda topo: 3% do quadro, cor RGB(34,171,252)
- Q29 (4:40): faixa uniforme na borda topo: 6% do quadro, cor RGB(110,200,248)
- Q31 (5:00): faixa uniforme na borda topo: 12% do quadro, cor RGB(127,153,170)
- Q43 (7:00): faixa uniforme na borda topo: 7% do quadro, cor RGB(117,201,250)
- Q48 (7:50): faixa uniforme na borda topo: 7% do quadro, cor RGB(249,235,199)
- Q53 (8:40): faixa uniforme na borda topo: 6% do quadro, cor RGB(113,200,246)
- Q58 (9:30): faixa uniforme na borda topo: 4% do quadro, cor RGB(96,190,241)
- Q63 (10:20): faixa uniforme na borda topo: 11% do quadro, cor RGB(80,189,250)
- Q65 (10:40): faixa uniforme na borda topo: 8% do quadro, cor RGB(96,191,251)
- Q69 (11:20): faixa uniforme na borda esquerda: 4% do quadro, cor RGB(245,237,202)
- Q76 (12:30): faixa uniforme na borda esquerda: 5% do quadro, cor RGB(54,50,41)
- Q79 (13:00): faixa uniforme na borda topo: 9% do quadro, cor RGB(59,181,252)
- Q81 (13:20): faixa uniforme na borda topo: 19% do quadro, cor RGB(248,240,217)
- Q81 (13:20): faixa uniforme na borda esquerda: 4% do quadro, cor RGB(249,241,217)
- Q84 (13:50): faixa uniforme na borda topo: 13% do quadro, cor RGB(250,242,216)
- Q84 (13:50): faixa uniforme na borda base: 7% do quadro, cor RGB(216,156,89)
- Q85 (14:00): faixa uniforme na borda topo: 16% do quadro, cor RGB(248,237,207)
- Q93 (15:20): faixa uniforme na borda topo: 19% do quadro, cor RGB(246,238,210)
- Q93 (15:20): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(247,238,210)
- Q96 (15:50): faixa uniforme na borda topo: 9% do quadro, cor RGB(97,194,249)
- Q97 (16:00): faixa uniforme na borda esquerda: 9% do quadro, cor RGB(248,242,218)
- Q100 (16:30): faixa uniforme na borda topo: 8% do quadro, cor RGB(247,234,202)

## Quadros

Q01=0:00, Q02=0:10, Q03=0:20, Q04=0:30, Q05=0:40, Q06=0:50, Q07=1:00, Q08=1:10, Q09=1:20, Q10=1:30, Q11=1:40, Q12=1:50, Q13=2:00, Q14=2:10, Q15=2:20, Q16=2:30, Q17=2:40, Q18=2:50, Q19=3:00, Q20=3:10, Q21=3:20, Q22=3:30, Q23=3:40, Q24=3:50, Q25=4:00, Q26=4:10, Q27=4:20, Q28=4:30, Q29=4:40, Q30=4:50, Q31=5:00, Q32=5:10, Q33=5:20, Q34=5:30, Q35=5:40, Q36=5:50, Q37=6:00, Q38=6:10, Q39=6:20, Q40=6:30, Q41=6:40, Q42=6:50, Q43=7:00, Q44=7:10, Q45=7:20, Q46=7:30, Q47=7:40, Q48=7:50, Q49=8:00, Q50=8:10, Q51=8:20, Q52=8:30, Q53=8:40, Q54=8:50, Q55=9:00, Q56=9:10, Q57=9:20, Q58=9:30, Q59=9:40, Q60=9:50, Q61=10:00, Q62=10:10, Q63=10:20, Q64=10:30, Q65=10:40, Q66=10:50, Q67=11:00, Q68=11:10, Q69=11:20, Q70=11:30, Q71=11:40, Q72=11:50, Q73=12:00, Q74=12:10, Q75=12:20, Q76=12:30, Q77=12:40, Q78=12:50, Q79=13:00, Q80=13:10, Q81=13:20, Q82=13:30, Q83=13:40, Q84=13:50, Q85=14:00, Q86=14:10, Q87=14:20, Q88=14:30, Q89=14:40, Q90=14:50, Q91=15:00, Q92=15:10, Q93=15:20, Q94=15:30, Q95=15:40, Q96=15:50, Q97=16:00, Q98=16:10, Q99=16:20, Q100=16:30, Q101=16:40, Q102=16:50, Q103=17:00
