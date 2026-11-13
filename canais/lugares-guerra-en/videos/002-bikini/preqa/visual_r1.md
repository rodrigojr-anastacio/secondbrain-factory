# Pré-QA visual automático

- Alvo: `canais/lugares-guerra-en/videos/002-bikini/preqa/stills` · 209 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.438 · `tools/preqa_visual.py`
- Resultado: **REPROVADO (há bloqueante)** · bloqueante 1 · alto 12 · médio 20 · baixo 40
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 1:35 | Q22 `2846.png` | medio | anacronismo | A legenda 'BIKINI ATOLL' não traz data, ao contrário das outras fichas (DATA · LUGAR). A foto é colorida, parece das décadas de 1970-80, e a ficha deveria dizer o ano. Quebra o padrão da Ficha. |
| 1:44 | Q24 `3119.png` | alto | valor_errado | O Número diz '1958 · LAST TEST' sobre um quadro legendado 'MARCH 1, 1954 · CASTLE BRAVO'. Se o ano 1958 for o último teste em Bikini, o dado está certo, mas o contraste com a ficha de 1954 pode confundir. Conferir se o número bate com a narração. |
| 2:33 | Q39 `4604.png` | medio | elemento_fora | A Ficha 'FEBRUARY 1946 · PEARL HARBOR' fica sobre o navio no canto inferior esquerdo e cobre parte do casco e da superestrutura. Dúvida entre estilo e defeito, pois a ficha é padrão do canal. A legibilidade está ok. |
| 3:02 | Q46 `5467.png` | alto | texto_encavalado | Dois rótulos conflitantes ao mesmo tempo: o número amarelo 'FEB 10 1946' no canto superior direito e a Ficha 'MARCH 1946 · BIKINI ISLAND' embaixo à esquerda. As datas divergem (10 de fevereiro x março de 1946), então um dos dois está errado ou o outro está defasado. O número também cobre parte da bandeira ao fundo. |
| 3:02 | Q46 `5467.png` | medio | valor_errado | Possível inconsistência de data entre a Ficha ('MARCH 1946') e o selo de data 'FEB 10 1946', que aparecem juntos no mesmo plano. Vale conferir qual está certa para o trecho. |
| 3:45 | Q55 `6741.png` | medio | moldura | Faixa preta estreita na borda esquerda do quadro (cerca de 15 px), vinda da película/escaneamento do filme de arquivo. Pode ser característica do material, mas aparece como margem preta. Na dúvida entre estilo e defeito, convém recortar ou dar zoom. |
| 3:53 | Q57 `7004.png` | medio | fundo/faixa | Mapa2D quase todo vazio: mar azul-escuro liso com apenas Bikini, Rongerik e a linha de 140 MI no centro. Terra mal visível (só pontinhos de ilhas no canto inferior). A cor RGB(14,42,59) é o mar #0E2A3B do canal, então a faixa é estilo e não bug, mas o mapa parece vazio. Dúvida entre estilo e defeito. |
| 4:54 | Q69 `8823.png` | alto | texto_encavalado | O rótulo amarelo '400+ mi' fica em cima da linha do mapa e colide com o ponto e o rótulo 'KWAJALEIN'. O 'mi' fica cortado e ilegível. |
| 4:54 | Q69 `8823.png` | medio | valor_errado | O ponto de Kwajalein fica quase em cima da linha Bikini–Kili, mas não está nela. O trajeto sugere passar por Kwajalein, e o mapa quase vazio com ilhas mínimas é fraco. Pode ser estilo (Mapa2D), mas confira. |
| 5:07 | Q72 `9214.png` | alto | fundo/faixa | Faixa preta/escura vertical de cerca de 30 px na borda direita, ao lado da foto aérea. A foto não preenche o quadro (3%, RGB 13,15,18). |
| 5:14 | Q73 `9416.png` | medio | fundo/faixa | Na borda direita do quadro há uma faixa vertical cinza-clara estreita (cerca de 15 px) que não faz parte da foto, e a foto não preenche a tela até a borda. O sinal automático de faixa no topo corresponde ao céu cinza liso da foto, que é normal. |
| 5:22 | Q74 `9646.png` | medio | fundo/faixa | Há uma faixa vertical clara e fina na borda direita, como se a imagem não cobrisse todo o quadro. Pode ser borda do filme de arquivo ou do render, e convém conferir. A faixa escura na base é parte da imagem do filme. |
| 5:48 | Q80 `10429.png` | medio | fundo/faixa | Fina faixa vertical clara na borda direita, a mesma do filme de arquivo de Q74, indicando que a imagem não preenche toda a largura. Convém conferir se é artefato de render ou do material de origem. |
| 5:59 | Q82 `10777.png` | alto | valor_errado | O cartão de data no canto superior direito diz 'JULY 5, 1946 · PARIS' (biquíni, Paris), mas a ficha inferior e o filme mostram o Test Able em Bikini de 1 de julho de 1946. Data e lugar não batem com a imagem; pode ser uma menção intencional ao lançamento do biquíni em Paris, mas parece um erro de dados. |
| 5:59 | Q82 `10777.png` | medio | elemento_fora | Duas caixas de data/lugar ao mesmo tempo (grande no topo direito e ficha pequena embaixo à esquerda) com informações conflitantes (5 de julho × 1 de julho); HUD duplicado. |
| 6:29 | Q88 `11671.png` | medio | moldura | Faixa escura chapada na base (~5%, RGB 21,20,19) abaixo da nuvem, logo abaixo da ficha. Pode ser a borda do filme de arquivo, mas parece uma moldura/faixa preta na parte inferior do quadro. Conferir se faz parte do original. |
| 7:56 | Q107 `14282.png` | medio | anacronismo | A ficha diz '1954 · BIKINI LAGOON', mas a cena parece filme colorido de barcaças e navios, e o contexto do trecho é 1946. Possível data errada; conferir a legenda. |
| 8:15 | Q111 `14843.png` | alto | texto_cortado | A ficha inferior mostra texto vazado: 'MARCH 1, 1954 · CASTLE BRAVO Faixa clara de vazamen…' cortado com reticências. É texto de nota/prompt interno que vazou para a ficha, que deveria ter só 'DATA · LUGAR' em 1 linha. |
| 8:15 | Q111 `14843.png` | alto | valor_errado | O número no canto superior direito mostra '78 MEGATONS' para Castle Bravo, que teve cerca de 15 megatons. Valor animado provavelmente errado ou parado em um valor intermediário errado. |
| 8:49 | Q118 `15858.png` | medio | moldura | Faixa preta vertical estreita na borda esquerda do quadro, de cerca de 3% da largura. Pode ser a perfuração/borda do filme, mas se parece com moldura preta da imagem. |
| 8:56 | Q119 `16071.png` | bloqueante | texto_encavalado | Mapa 2D com todos os pontos amontoados no centro: o rótulo 'FALLOUT · MARCH 1954' está coberto por 'BIKINI' e 'RONGERIK', e 'RONGELAP' está parcialmente coberto por 'RONGERIK' e pelas linhas amarelas. Os textos ficam ilegíveis. |
| 8:56 | Q119 `16071.png` | alto | fundo/faixa | O mapa quase não mostra terra (só uns fiapos de areia na base) e o quadro é um mar azul chapado e vazio. A escala está muito aberta e os atóis, minúsculos, ficam sem contexto geográfico legível. |
| 9:24 | Q125 `16920.png` | alto | texto_cortado | A Ficha no canto inferior esquerdo mostra só a letra "c" em vez da linha DATA · LUGAR (ou quem aparece). O texto está truncado ou incompleto, sem informação útil. |
| 9:33 | Q128 `17184.png` | alto | texto_cortado | A Ficha no canto inferior esquerdo mostra só a letra "c" em vez de DATA · LUGAR. O texto está truncado e a foto aérea do atol fica sem identificação. |
| 9:54 | Q135 `17826.png` | medio | texto_inventado | A ficha no canto inferior esquerdo mostra só a letra "c" no lugar da linha DATA · LUGAR. Parece texto truncado ou em animação de entrada. Se for um frame estático, a ficha está errada ou incompleta. |
| 11:07 | Q150 `20015.png` | medio | texto_cortado | A Ficha no canto inferior esquerdo mostra só a letra "c" em vez de uma linha DATA · LUGAR ou nome. Parece texto truncado ou ainda em animação de digitação. Se não for digitação, é bloqueante, porque a ficha fica sem informação. |
| 11:26 | Q154 `20586.png` | medio | elemento_fora | A caixa do número '0.4% OF THE AWARD PAID' cobre parte do texto do documento no canto superior direito, escondendo palavras da primeira linha ('the Plaintiffs–Appellants, the p…'). O texto fica cortado, mas isso é o esperado em número sobreposto, então é só dúvida de legibilidade. |
| 11:30 | Q156 `20707.png` | medio | legenda | A Ficha no canto inferior esquerdo mostra só a letra 'c' numa caixa pequena. Parece uma ficha truncada ou em animação de entrada. Se aparecer assim no render final, a ficha está incompleta, sem data nem lugar. |
| 12:07 | Q163 `21810.png` | medio | valor_errado | O número "190 MILLIREM A YEAR (2019)" aparece sobre filme de 1954. A dúvida é se o valor está correto, já que o contexto é ambíguo e o dado pode não bater com a narração. Conferir com o roteiro. |
| 12:21 | Q166 `22232.png` | alto | texto_cortado | A Ficha no canto inferior esquerdo mostra só a letra "c" em vez da linha completa (DATA · LUGAR). Texto truncado ou incompleto. Se não for animação de entrada, precisa corrigir. |
| 12:26 | Q167 `22369.png` | alto | texto_cortado | A Ficha no canto inferior esquerdo mostra só a letra "c", sem data nem lugar. Texto truncado ou campo vazio. |
| 14:28 | Q191 `26048.png` | medio | outro | No Mapa2D quase não aparece terra (só alguns pontinhos minúsculos de areia), então o mapa fica praticamente vazio e os rótulos BIKINI, KILI e MAJURO ficam soltos sobre o mar liso. O estilo é intencional (mar #0E2A3B), mas fica a dúvida se o shapefile carregou direito. |
| 15:08 | Q198 `27228.png` | medio | moldura | Faixa escura (~4%) na borda inferior, abaixo da linha clara do quadro de filme, e uma leve borda escura nas laterais. Parece ser a moldura/perfuração do filme de arquivo e não uma moldura de IA. Se for estilo do arquivo, é aceitável; senão, vale cortar com zoom leve. Em dúvida entre estilo e defeito. |

40 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q12 (0:45): faixa uniforme na borda topo: 33% do quadro, cor RGB(12,14,18)
- Q12 (0:45): faixa uniforme na borda base: 32% do quadro, cor RGB(12,15,18)
- Q12 (0:45): faixa uniforme na borda esquerda: 28% do quadro, cor RGB(12,14,18)
- Q12 (0:45): faixa uniforme na borda direita: 28% do quadro, cor RGB(12,15,18)
- Q13 (0:52): faixa uniforme na borda topo: 32% do quadro, cor RGB(14,42,59)
- Q13 (0:52): faixa uniforme na borda base: 33% do quadro, cor RGB(14,42,59)
- Q13 (0:52): faixa uniforme na borda esquerda: 17% do quadro, cor RGB(14,42,59)
- Q13 (0:52): faixa uniforme na borda direita: 12% do quadro, cor RGB(14,42,59)
- Q17 (1:08): faixa uniforme na borda base: 5% do quadro, cor RGB(11,14,28)
- Q17 (1:08): faixa uniforme na borda direita: 9% do quadro, cor RGB(11,14,29)
- Q18 (1:12): faixa preta na borda topo: 5% do quadro
- Q19 (1:17): faixa uniforme na borda topo: 4% do quadro, cor RGB(10,13,29)
- Q27 (1:51): faixa uniforme na borda esquerda: 10% do quadro, cor RGB(255,255,255)
- Q27 (1:51): faixa uniforme na borda direita: 4% do quadro, cor RGB(255,255,255)
- Q28 (1:52): faixa uniforme na borda esquerda: 9% do quadro, cor RGB(255,255,255)
- Q28 (1:52): faixa uniforme na borda direita: 4% do quadro, cor RGB(255,255,255)
- Q31 (2:05): faixa uniforme na borda base: 4% do quadro, cor RGB(34,62,56)
- Q33 (2:15): faixa uniforme na borda base: 3% do quadro, cor RGB(39,69,65)
- Q41 (2:41): faixa preta na borda direita: 5% do quadro
- Q43 (2:48): faixa preta na borda direita: 12% do quadro
- Q44 (2:51): faixa uniforme na borda topo: 8% do quadro, cor RGB(80,88,76)
- Q45 (2:57): faixa uniforme na borda base: 4% do quadro, cor RGB(37,45,36)
- Q46 (3:02): faixa uniforme na borda base: 3% do quadro, cor RGB(21,21,21)
- Q50 (3:21): faixa uniforme na borda topo: 4% do quadro, cor RGB(12,14,18)
- Q50 (3:21): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q50 (3:21): faixa uniforme na borda esquerda: 14% do quadro, cor RGB(12,14,18)
- Q53 (3:36): faixa uniforme na borda topo: 4% do quadro, cor RGB(12,14,18)
- Q53 (3:36): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q53 (3:36): faixa uniforme na borda esquerda: 13% do quadro, cor RGB(12,14,18)
- Q57 (3:53): faixa uniforme na borda topo: 33% do quadro, cor RGB(14,42,59)
- Q57 (3:53): faixa uniforme na borda base: 6% do quadro, cor RGB(14,42,59)
- Q57 (3:53): faixa uniforme na borda esquerda: 5% do quadro, cor RGB(14,42,59)
- Q57 (3:53): faixa uniforme na borda direita: 33% do quadro, cor RGB(14,42,59)
- Q61 (4:12): faixa uniforme na borda esquerda: 9% do quadro, cor RGB(255,255,255)
- Q62 (4:14): faixa uniforme na borda esquerda: 9% do quadro, cor RGB(255,255,255)
- Q66 (4:35): faixa uniforme na borda topo: 33% do quadro, cor RGB(12,14,18)
- Q66 (4:35): faixa uniforme na borda base: 32% do quadro, cor RGB(12,15,18)
- Q66 (4:35): faixa uniforme na borda esquerda: 24% do quadro, cor RGB(12,14,18)
- Q66 (4:35): faixa uniforme na borda direita: 25% do quadro, cor RGB(12,15,18)
- Q69 (4:54): faixa uniforme na borda topo: 19% do quadro, cor RGB(14,42,59)
- Q69 (4:54): faixa uniforme na borda base: 20% do quadro, cor RGB(14,42,59)
- Q69 (4:54): faixa uniforme na borda direita: 33% do quadro, cor RGB(14,42,59)
- Q72 (5:07): faixa uniforme na borda direita: 3% do quadro, cor RGB(13,15,18)
- Q73 (5:14): faixa uniforme na borda topo: 7% do quadro, cor RGB(166,166,166)
- Q74 (5:22): faixa uniforme na borda base: 3% do quadro, cor RGB(31,56,53)
- Q75 (5:29): faixa preta na borda topo: 5% do quadro
- Q75 (5:29): faixa preta na borda base: 5% do quadro
- Q76 (5:35): faixa uniforme na borda base: 20% do quadro, cor RGB(255,255,255)
- Q76 (5:35): faixa uniforme na borda esquerda: 11% do quadro, cor RGB(255,255,255)
- Q76 (5:35): faixa uniforme na borda direita: 9% do quadro, cor RGB(255,255,255)
- Q77 (5:36): faixa uniforme na borda base: 19% do quadro, cor RGB(255,255,255)
- Q77 (5:36): faixa uniforme na borda esquerda: 11% do quadro, cor RGB(255,255,255)
- Q77 (5:36): faixa uniforme na borda direita: 9% do quadro, cor RGB(255,255,255)
- Q78 (5:38): faixa uniforme na borda topo: 4% do quadro, cor RGB(157,157,157)
- Q79 (5:44): faixa uniforme na borda topo: 9% do quadro, cor RGB(181,181,181)
- Q81 (5:53): faixa uniforme na borda topo: 6% do quadro, cor RGB(181,182,178)
- Q88 (6:29): faixa uniforme na borda base: 5% do quadro, cor RGB(21,20,19)
- Q90 (6:42): faixa uniforme na borda base: 11% do quadro, cor RGB(254,254,254)
- Q90 (6:42): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(255,255,255)
- Q90 (6:42): faixa uniforme na borda direita: 9% do quadro, cor RGB(255,255,255)
- Q91 (6:43): faixa uniforme na borda base: 10% do quadro, cor RGB(255,255,255)
- Q91 (6:43): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(255,255,255)
- Q91 (6:43): faixa uniforme na borda direita: 8% do quadro, cor RGB(255,255,255)
- Q96 (7:11): faixa uniforme na borda esquerda: 9% do quadro, cor RGB(255,255,255)
- Q97 (7:13): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(255,255,255)
- Q104 (7:42): faixa uniforme na borda topo: 4% do quadro, cor RGB(12,14,18)
- Q104 (7:42): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q104 (7:42): faixa uniforme na borda esquerda: 15% do quadro, cor RGB(12,14,18)
- Q108 (7:59): faixa uniforme na borda esquerda: 3% do quadro, cor RGB(255,255,255)
- Q109 (8:00): faixa uniforme na borda topo: 9% do quadro, cor RGB(254,254,254)
- Q110 (8:09): faixa uniforme na borda topo: 33% do quadro, cor RGB(12,14,18)
- Q110 (8:09): faixa uniforme na borda base: 32% do quadro, cor RGB(12,15,18)
- Q110 (8:09): faixa uniforme na borda esquerda: 30% do quadro, cor RGB(12,14,18)
- Q110 (8:09): faixa uniforme na borda direita: 30% do quadro, cor RGB(12,15,18)
- Q114 (8:34): faixa uniforme na borda esquerda: 10% do quadro, cor RGB(255,255,255)
- Q114 (8:34): faixa uniforme na borda direita: 9% do quadro, cor RGB(255,255,255)
- Q115 (8:37): faixa uniforme na borda esquerda: 9% do quadro, cor RGB(255,255,255)
- Q115 (8:37): faixa uniforme na borda direita: 9% do quadro, cor RGB(255,255,255)
- Q117 (8:46): faixa uniforme na borda topo: 24% do quadro, cor RGB(9,13,29)
- Q119 (8:56): faixa uniforme na borda topo: 33% do quadro, cor RGB(14,42,59)
- Q119 (8:56): faixa uniforme na borda base: 33% do quadro, cor RGB(14,42,59)
- Q119 (8:56): faixa uniforme na borda esquerda: 33% do quadro, cor RGB(14,42,59)
- Q119 (8:56): faixa uniforme na borda direita: 29% do quadro, cor RGB(14,42,59)
- Q123 (9:18): faixa uniforme na borda topo: 20% do quadro, cor RGB(255,255,255)
- Q123 (9:18): faixa uniforme na borda esquerda: 10% do quadro, cor RGB(255,255,255)
- Q123 (9:18): faixa uniforme na borda direita: 10% do quadro, cor RGB(255,255,255)
- Q124 (9:21): faixa uniforme na borda topo: 19% do quadro, cor RGB(255,255,255)
- Q124 (9:21): faixa uniforme na borda esquerda: 9% do quadro, cor RGB(255,255,255)
- Q124 (9:21): faixa uniforme na borda direita: 9% do quadro, cor RGB(255,255,255)
- Q126 (9:29): faixa uniforme na borda base: 4% do quadro, cor RGB(255,255,255)
- Q126 (9:29): faixa uniforme na borda direita: 10% do quadro, cor RGB(255,255,255)
- Q127 (9:30): faixa uniforme na borda base: 3% do quadro, cor RGB(255,255,255)
- Q127 (9:30): faixa uniforme na borda direita: 9% do quadro, cor RGB(255,255,255)
- Q129 (9:37): faixa uniforme na borda esquerda: 10% do quadro, cor RGB(255,255,255)
- Q129 (9:37): faixa uniforme na borda direita: 4% do quadro, cor RGB(255,255,255)
- Q130 (9:38): faixa uniforme na borda esquerda: 9% do quadro, cor RGB(255,255,255)
- Q130 (9:38): faixa uniforme na borda direita: 4% do quadro, cor RGB(255,255,255)
- Q131 (9:42): faixa uniforme na borda topo: 3% do quadro, cor RGB(255,255,255)
- Q131 (9:42): faixa uniforme na borda esquerda: 10% do quadro, cor RGB(255,255,255)
- Q131 (9:42): faixa uniforme na borda direita: 9% do quadro, cor RGB(255,255,255)
- Q132 (9:43): faixa uniforme na borda esquerda: 10% do quadro, cor RGB(255,255,255)
- Q132 (9:43): faixa uniforme na borda direita: 8% do quadro, cor RGB(255,255,255)
- Q134 (9:51): faixa uniforme na borda direita: 7% do quadro, cor RGB(164,167,158)
- Q135 (9:54): faixa uniforme na borda base: 4% do quadro, cor RGB(152,152,152)
- Q136 (9:59): faixa uniforme na borda base: 5% do quadro, cor RGB(19,11,16)
- Q138 (10:14): faixa uniforme na borda topo: 9% do quadro, cor RGB(7,18,13)
- Q138 (10:14): faixa preta na borda direita: 5% do quadro
- Q143 (10:33): faixa uniforme na borda topo: 4% do quadro, cor RGB(88,101,121)
- Q144 (10:40): faixa uniforme na borda direita: 5% do quadro, cor RGB(255,255,255)
- Q145 (10:42): faixa uniforme na borda direita: 4% do quadro, cor RGB(255,255,255)
- Q146 (10:46): faixa uniforme na borda base: 4% do quadro, cor RGB(159,159,159)
- Q151 (11:14): faixa uniforme na borda esquerda: 10% do quadro, cor RGB(255,255,255)
- Q151 (11:14): faixa uniforme na borda direita: 10% do quadro, cor RGB(255,255,255)
- Q152 (11:16): faixa uniforme na borda esquerda: 9% do quadro, cor RGB(255,255,255)
- Q152 (11:16): faixa uniforme na borda direita: 9% do quadro, cor RGB(255,255,255)
- Q154 (11:26): faixa uniforme na borda topo: 4% do quadro, cor RGB(255,255,255)
- Q155 (11:27): faixa uniforme na borda topo: 4% do quadro, cor RGB(255,255,255)
- Q157 (11:37): faixa uniforme na borda base: 19% do quadro, cor RGB(255,255,255)
- Q157 (11:37): faixa uniforme na borda esquerda: 10% do quadro, cor RGB(255,255,255)
- Q157 (11:37): faixa uniforme na borda direita: 10% do quadro, cor RGB(255,255,255)
- Q158 (11:40): faixa uniforme na borda base: 19% do quadro, cor RGB(255,255,255)
- Q158 (11:40): faixa uniforme na borda esquerda: 9% do quadro, cor RGB(255,255,255)
- Q158 (11:40): faixa uniforme na borda direita: 9% do quadro, cor RGB(255,255,255)
- Q159 (11:41): faixa uniforme na borda base: 4% do quadro, cor RGB(38,46,37)
- Q160 (11:49): faixa uniforme na borda direita: 14% do quadro, cor RGB(12,15,18)
- Q171 (12:39): faixa uniforme na borda topo: 33% do quadro, cor RGB(12,14,18)
- Q171 (12:39): faixa uniforme na borda base: 32% do quadro, cor RGB(12,15,18)
- Q171 (12:39): faixa uniforme na borda esquerda: 18% do quadro, cor RGB(12,14,18)
- Q171 (12:39): faixa uniforme na borda direita: 18% do quadro, cor RGB(12,15,18)
- Q172 (12:45): faixa uniforme na borda topo: 4% do quadro, cor RGB(90,103,124)
- Q173 (12:50): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q175 (12:59): faixa uniforme na borda topo: 14% do quadro, cor RGB(10,13,28)
- Q176 (13:05): faixa uniforme na borda topo: 5% do quadro, cor RGB(9,13,28)
- Q177 (13:11): faixa uniforme na borda topo: 26% do quadro, cor RGB(9,13,29)
- Q178 (13:16): faixa uniforme na borda topo: 4% do quadro, cor RGB(60,72,91)
- Q178 (13:16): faixa uniforme na borda base: 4% do quadro, cor RGB(47,68,91)
- Q180 (13:27): faixa uniforme na borda topo: 6% do quadro, cor RGB(99,101,96)
- Q182 (13:42): faixa uniforme na borda topo: 5% do quadro, cor RGB(178,178,178)
- Q183 (13:48): faixa uniforme na borda topo: 8% do quadro, cor RGB(190,190,190)
- Q183 (13:48): faixa uniforme na borda direita: 8% do quadro, cor RGB(193,193,193)
- Q184 (13:52): faixa uniforme na borda base: 5% do quadro, cor RGB(10,22,20)
- Q187 (14:08): faixa uniforme na borda topo: 33% do quadro, cor RGB(12,14,18)
- Q187 (14:08): faixa uniforme na borda base: 32% do quadro, cor RGB(12,15,18)
- Q187 (14:08): faixa uniforme na borda esquerda: 16% do quadro, cor RGB(12,14,18)
- Q187 (14:08): faixa uniforme na borda direita: 16% do quadro, cor RGB(12,15,18)
- Q188 (14:12): faixa uniforme na borda topo: 13% do quadro, cor RGB(96,92,83)
- Q191 (14:28): faixa uniforme na borda topo: 19% do quadro, cor RGB(14,42,59)
- Q191 (14:28): faixa uniforme na borda base: 20% do quadro, cor RGB(14,42,59)
- Q191 (14:28): faixa uniforme na borda esquerda: 33% do quadro, cor RGB(14,42,59)
- Q191 (14:28): faixa uniforme na borda direita: 26% do quadro, cor RGB(14,42,59)
- Q198 (15:08): faixa uniforme na borda base: 4% do quadro, cor RGB(14,14,13)
- Q200 (15:18): faixa uniforme na borda esquerda: 10% do quadro, cor RGB(255,255,255)
- Q200 (15:18): faixa uniforme na borda direita: 4% do quadro, cor RGB(255,255,255)
- Q201 (15:18): faixa uniforme na borda esquerda: 9% do quadro, cor RGB(255,255,255)
- Q201 (15:18): faixa uniforme na borda direita: 4% do quadro, cor RGB(255,255,255)
- Q206 (15:43): faixa uniforme na borda topo: 33% do quadro, cor RGB(12,14,18)
- Q206 (15:43): faixa uniforme na borda base: 32% do quadro, cor RGB(12,15,18)
- Q206 (15:43): faixa uniforme na borda esquerda: 16% do quadro, cor RGB(12,14,18)
- Q206 (15:43): faixa uniforme na borda direita: 16% do quadro, cor RGB(12,15,18)
- Q208 (15:53): faixa uniforme na borda topo: 4% do quadro, cor RGB(161,161,161)
- Q209 (16:02): faixa uniforme na borda topo: 27% do quadro, cor RGB(12,14,18)
- Q209 (16:02): faixa uniforme na borda base: 26% do quadro, cor RGB(12,15,18)
- Q209 (16:02): faixa uniforme na borda esquerda: 14% do quadro, cor RGB(12,14,18)
- Q209 (16:02): faixa uniforme na borda direita: 14% do quadro, cor RGB(12,15,18)

## Quadros

Q01=0:02, Q02=0:05, Q03=0:09, Q04=0:14, Q05=0:17, Q06=0:20, Q07=0:24, Q08=0:28, Q09=0:33, Q10=0:37, Q11=0:38, Q12=0:45, Q13=0:52, Q14=0:56, Q15=0:59, Q16=1:04, Q17=1:08, Q18=1:12, Q19=1:17, Q20=1:23, Q21=1:30, Q22=1:35, Q23=1:39, Q24=1:44, Q25=1:46, Q26=1:48, Q27=1:51, Q28=1:52, Q29=1:57, Q30=2:02, Q31=2:05, Q32=2:08, Q33=2:15, Q34=2:19, Q35=2:25, Q36=2:29, Q37=2:31, Q38=2:31, Q39=2:33, Q40=2:38, Q41=2:41, Q42=2:45, Q43=2:48, Q44=2:51, Q45=2:57, Q46=3:02, Q47=3:07, Q48=3:09, Q49=3:15, Q50=3:21, Q51=3:27, Q52=3:31, Q53=3:36, Q54=3:41, Q55=3:45, Q56=3:50, Q57=3:53, Q58=3:56, Q59=4:00, Q60=4:04, Q61=4:12, Q62=4:14, Q63=4:18, Q64=4:25, Q65=4:31, Q66=4:35, Q67=4:42, Q68=4:47, Q69=4:54, Q70=5:00, Q71=5:04, Q72=5:07, Q73=5:14, Q74=5:22, Q75=5:29, Q76=5:35, Q77=5:36, Q78=5:38, Q79=5:44, Q80=5:48, Q81=5:53, Q82=5:59, Q83=6:04, Q84=6:08, Q85=6:13, Q86=6:19, Q87=6:25, Q88=6:29, Q89=6:36, Q90=6:42, Q91=6:43, Q92=6:49, Q93=6:56, Q94=7:02, Q95=7:05, Q96=7:11, Q97=7:13, Q98=7:17, Q99=7:21, Q100=7:26, Q101=7:31, Q102=7:34, Q103=7:37, Q104=7:42, Q105=7:46, Q106=7:52, Q107=7:56, Q108=7:59, Q109=8:00, Q110=8:09, Q111=8:15, Q112=8:19, Q113=8:26, Q114=8:34, Q115=8:37, Q116=8:41, Q117=8:46, Q118=8:49, Q119=8:56, Q120=9:01, Q121=9:05, Q122=9:10, Q123=9:18, Q124=9:21, Q125=9:24, Q126=9:29, Q127=9:30, Q128=9:33, Q129=9:37, Q130=9:38, Q131=9:42, Q132=9:43, Q133=9:48, Q134=9:51, Q135=9:54, Q136=9:59, Q137=10:07, Q138=10:14, Q139=10:18, Q140=10:24, Q141=10:26, Q142=10:29, Q143=10:33, Q144=10:40, Q145=10:42, Q146=10:46, Q147=10:50, Q148=10:52, Q149=11:01, Q150=11:07, Q151=11:14, Q152=11:16, Q153=11:22, Q154=11:26, Q155=11:27, Q156=11:30, Q157=11:37, Q158=11:40, Q159=11:41, Q160=11:49, Q161=11:55, Q162=12:00, Q163=12:07, Q164=12:12, Q165=12:16, Q166=12:21, Q167=12:26, Q168=12:29, Q169=12:31, Q170=12:34, Q171=12:39, Q172=12:45, Q173=12:50, Q174=12:55, Q175=12:59, Q176=13:05, Q177=13:11, Q178=13:16, Q179=13:22, Q180=13:27, Q181=13:33, Q182=13:42, Q183=13:48, Q184=13:52, Q185=13:57, Q186=14:02, Q187=14:08, Q188=14:12, Q189=14:16, Q190=14:22, Q191=14:28, Q192=14:31, Q193=14:35, Q194=14:42, Q195=14:50, Q196=14:58, Q197=15:03, Q198=15:08, Q199=15:13, Q200=15:18, Q201=15:18, Q202=15:23, Q203=15:28, Q204=15:34, Q205=15:39, Q206=15:43, Q207=15:46, Q208=15:53, Q209=16:02
