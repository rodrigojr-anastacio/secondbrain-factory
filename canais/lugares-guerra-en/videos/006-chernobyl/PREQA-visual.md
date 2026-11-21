# Pré-QA visual automático

- Alvo: `canais/lugares-guerra-en/videos/006-chernobyl/preqa/stills` · 275 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.626 · `tools/preqa_visual.py`
- Resultado: **REPROVADO (há bloqueante)** · bloqueante 2 · alto 11 · médio 68 · baixo 51
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:16 | Q06 `469.png` | medio | outro | A foto da sala de controle mostra uma pessoa de máscara com o rosto cortado no topo, atrás da régua de horas. A legenda 'TODAY · UNIT 4 CONTROL ROOM' está correta, mas o contador mostra '+00:00:00' sobre foto de hoje. Dúvida entre estilo e defeito, já que o contador faz parte do estilo do canal. |
| 0:41 | Q13 `1232.png` | medio | texto_encavalado | A legenda "Chernobyl nuclear power plant" fica no meio do quadro sobre a imagem de satélite, com contraste fraco sobre o verde claro. Dá para ler, mas o texto está sobreposto à imagem e à ficha. Pode ser um rótulo intencional do mapa; fica o registro pela dúvida. |
| 0:58 | Q19 `1742.png` | medio | valor_errado | O contador mostra +62:02:23 / MON 28 APR 15:26:03, mas a régua está em Forsmark. O valor pula depois para +67:36:20 em Q20. Possível inconsistência, mas pode ser intencional. |
| 1:00 | Q20 `1810.png` | medio | valor_errado | Contador e régua de horas mostram +67:36:20 / MON 28 APR 21:00 sobre uma foto de 2016 em Pripyat; o contador parece estar parado em relação a Q22–Q23. Conferir se o valor deveria mudar. O contador também cobre o guarda-chuva grafitado, o que é aceitável. |
| 1:21 | Q26 `2430.png` | bloqueante | texto_encavalado | Rótulo 'PRIPYAT' sobreposto ao rótulo 'CHERNOBYL NPP': o início de 'CHERNOBYL' fica ilegível (aparece 'OBYL NPP') por baixo de 'PRIPYAT', no topo do círculo. |
| 1:21 | Q26 `2430.png` | medio | fundo/faixa | Mapa esquemático quase todo em cinza-azulado chapado, com a costa/terra pouco legível e sem a paleta definida (terra areia/mar escuro). A faixa mais escura no topo pode ser a terra ou um defeito. Na dúvida entre estilo e defeito, registro como médio. |
| 2:03 | Q39 `3699.png` | alto | valor_errado | O cartão mostra "FRI 25 APR 1986 · 01:06 · ONE DAY EARLY" e a régua do topo marca o cursor em SAT 26 APR. O contador "-24:17:40" do Q40 não bate com a data/hora do cartão, o que sugere valor animado ou data inconsistente. Vale conferir contra a narração. |
| 2:08 | Q40 `3837.png` | medio | valor_errado | O contador "BEFORE THE BUTTON -24:17:40" com "FRI 25 APR · 01:06" parece inconsistente com a contagem regressiva até 26/04 01:23. A diferença seria de cerca de 24h17min, então a conta parece bater. Mas a foto é "BEFORE 1986" com ficha de data da usina, e o rótulo da ficha e o HUD competem no quadro. Dúvida de estilo, só registrar. |
| 2:19 | Q43 `4160.png` | medio | fundo/faixa | Faixa escura uniforme (RGB 18,17,16) na borda direita, cerca de 8% do quadro, e faixa escura semelhante à esquerda. Provavelmente é o 4:3 de época com laterais desfocadas do próprio filme, estilo intencional. Mas as laterais parecem quase pretas e chapadas em vez de desfocadas, e há uma linha vertical nítida na borda esquerda da imagem. Na dúvida entre estilo e defeito, registro como médio. |
| 2:21 | Q44 `4233.png` | medio | texto_encavalado | A palavra 'Event' do documento fica colada atrás do contador 'BEFORE THE BUTTON' no canto superior esquerdo. A régua de horas no topo também corta a primeira linha do documento. É um recorte de zoom no documento, e o HUD cobre parte do texto sem atrapalhar a linha grifada. |
| 2:30 | Q47 `4497.png` | medio | texto_encavalado | No topo, a régua de horas se sobrepõe às linhas do documento ('vibration characteristics of turbogenerator No. 7...') e o HUD do contador cobre o início das linhas. O texto atrás fica cortado e ilegível, mas é contexto secundário. A linha grifada, que é a principal, está legível. |
| 2:32 | Q48 `4557.png` | medio | texto_encavalado | A régua de horas no topo passa por cima do texto do documento ('until 12:..., vibration characteristics...'), e o contador cobre o início das linhas. Fica uma sobreposição de texto no topo. A linha grifada continua legível. |
| 2:34 | Q49 `4622.png` | medio | texto_encavalado | O contador 'BEFORE THE BUTTON' no canto superior esquerdo cobre o início das linhas do documento ('07:10', '14:00') e a régua de horas corta o topo da primeira linha. Parte do documento fica ilegível, mas o contador e a régua fazem parte do estilo intencional. Registrado por dúvida. |
| 2:35 | Q50 `4645.png` | medio | texto_encavalado | Mesma situação do Q49: o contador cobre o início das linhas de horário e a régua corta a primeira linha do documento. Na parte inferior, o texto 'printout of DREG)' fica cortado pela borda e pela fonte mono. Provavelmente é estilo, mas a legibilidade é fraca. |
| 2:52 | Q55 `5165.png` | medio | texto_encavalado | O contador no canto superior esquerdo se sobrepõe às primeiras linhas do documento ('03:47', '07:10'). Os horários ficam ilegíveis e as linhas, parcialmente cobertas. A primeira linha, 'graphite stack with nitrogen commences', é cortada pela régua. Pode ser estilo, mas atrapalha a leitura. |
| 2:53 | Q56 `5195.png` | medio | texto_encavalado | O contador cobre os horários '03:47' e '07:10' no canto superior esquerdo, e a régua corta a primeira linha do documento. O resultado é o mesmo do Q55, com leitura prejudicada na área do contador. |
| 3:01 | Q59 `5431.png` | medio | valor_errado | Esta tela de transição ("SAT 26 APR 1986 · 00:00 · NEW SHIFT") não mostra o contador "SINCE THE SHUTDOWN BUTTON" que aparece nos quadros vizinhos. Pode ser intencional, por ser um cartão de título. O fundo escuro liso com vinheta parece fazer parte do estilo, e as faixas laterais apontadas pelo sinal automático não são defeito. |
| 3:13 | Q62 `5797.png` | alto | texto_encavalado | O contador "+01:23:40" e a caixa SINCE THE SHUTDOWN BUTTON ficam por cima do texto do documento no canto superior esquerdo, e a régua de horas cobre as primeiras linhas. O crédito "Source: IAEA, INSAG-7 (1992)" no canto inferior esquerdo também se sobrepõe ao texto da página e fica difícil de ler. Já a página do documento está em tela cheia, sem margem. |
| 3:14 | Q63 `5822.png` | alto | texto_encavalado | Mesmo problema do Q62: o contador e a caixa "SINCE THE SHUTDOWN BUTTON" cobrem o texto do documento no canto superior esquerdo, a régua de horas cobre a primeira linha, e o crédito "Source: IAEA, INSAG-7 (1992)" se mistura com o texto da página no canto inferior. |
| 3:25 | Q65 `6158.png` | medio | elemento_fora | O texto do documento passa por trás do contador no canto superior esquerdo e da régua de horas. Fica uma palavra parcialmente tapada ('...ctor thermal power') e há texto cortado no topo. O texto 'neutron powe' é cortado pela borda direita. Pode ser enquadramento normal do zoom, mas atrapalha um pouco a leitura. |
| 3:27 | Q66 `6220.png` | medio | elemento_fora | O contador sobre o documento tapa o início da primeira linha ('...ctor thermal power'). O texto do documento é cortado pela borda direita em 'neutron powe'. Pode ser enquadramento do zoom. |
| 3:32 | Q68 `6360.png` | medio | elemento_fora | O contador cobre o início da linha 'reactor thermal power'. A borda direita corta 'neutron power'. Pode ser enquadramento do zoom. |
| 3:33 | Q69 `6391.png` | medio | elemento_fora | O contador tapa o início da primeira linha do documento e a borda direita corta 'neutron powe'. Pode ser enquadramento do zoom. |
| 3:36 | Q70 `6472.png` | alto | texto_encavalado | A régua de horas no topo e o contador à esquerda ficam por cima do texto do documento (ex.: 'tory limitations', 'should have applied'), que fica misturado e ilegível nessas áreas. O crédito 'Source: IAEA, INSAG-7 (1992)' no canto inferior esquerdo se sobrepõe à linha do documento 'at 01:23:04 as stated...'. |
| 3:37 | Q71 `6502.png` | alto | texto_encavalado | A régua e o contador ficam sobre as linhas do topo do documento, que ficam ilegíveis ('should have applied' atrás do contador). O crédito 'Source: IAEA...' se sobrepõe ao texto do documento embaixo. |
| 3:40 | Q72 `6603.png` | alto | texto_encavalado | O contador '+00:20:40' está sobre o texto do documento ('...ol power control'), que aparece atrás dele e polui a leitura. O crédito inferior se sobrepõe a 'al blocked (01:23:04...'. O texto do documento é cortado nas bordas por causa do zoom. |
| 3:41 | Q73 `6641.png` | alto | valor_errado | O contador no canto superior esquerdo mostra +00:20:40 / SAT 26 APR 01:03, mas o documento em tela trata de 00:28:00 e da queda de potência. O mesmo valor continua no Q74 e no Q75, e no Q76 muda para +00:01:10 / 01:22:30. O contador parece estar congelado ou fora de sincronia com a cena. |
| 3:57 | Q78 `7123.png` | medio | texto_encavalado | A régua de horas e o contador do canto superior esquerdo ficam sobre o texto do documento, que está com zoom e rolado até o topo. O texto atrás do contador fica ilegível, e o crédito 'Source: IAEA' no canto inferior esquerdo se sobrepõe a 'button was pressed'. Pode ser o estilo intencional do HUD, mas atrapalha a leitura do documento. |
| 3:58 | Q79 `7155.png` | medio | texto_encavalado | Mesma sobreposição do Q78: a régua e o contador cobrem as primeiras linhas do documento, e o crédito inferior esquerdo se sobrepõe ao texto 'button was pressed'. Há dúvida se é estilo ou defeito. |
| 4:27 | Q86 `7996.png` | medio | texto_encavalado | A legenda de crédito 'Source: IAEA, INSAG-7 (1992)' no canto inferior esquerdo se sobrepõe ao horário '01:23:46' do documento, e o contador no canto superior esquerdo cobre '01:23:10' e '01:23:30'. O estilo prevê esses elementos sobre documentos, mas a sobreposição prejudica a leitura de alguns horários. |
| 4:27 | Q87 `8023.png` | medio | texto_encavalado | A legenda de crédito 'Source: IAEA...' se sobrepõe ao horário '01:23:46' no canto inferior esquerdo, e o contador cobre parte de '01:23:10' e '01:23:30'. A legibilidade dos horários cai. |
| 4:36 | Q90 `8292.png` | medio | elemento_fora | A foto da sala de controle mostra um jaleco branco sem cabeça, cortado no topo pela régua de horas. O rosto/máscara fica escondido atrás da régua. Pode ser enquadramento normal; registro por dúvida. |
| 4:42 | Q91 `8462.png` | medio | texto_encavalado | A legenda de crédito 'Source: IAEA, INSAG-7 (1992)' no canto inferior esquerdo se sobrepõe ao texto do documento ('demonstrated that...'), o que prejudica a leitura. O texto no topo do documento também é cortado pela régua. |
| 4:44 | Q92 `8513.png` | medio | texto_encavalado | O crédito 'Source: IAEA, INSAG-7 (1992)' fica por cima da linha 'demonstrated that there was also...' do documento e dificulta a leitura dessa linha. |
| 4:58 | Q96 `8947.png` | alto | valor_errado | O cartão de impressão mostra 'NO VOLTAGE = 48 V', que é contraditório (sem tensão não pode ser 48 V). Pode ser erro de transcrição da tabela INSAG-7. O contador está em +00:00:09, coerente com 01:23:49. Verificar o texto-fonte. |
| 5:04 | Q97 `9113.png` | medio | texto_encavalado | A régua de horas e a caixa do contador cobrem parte do texto do documento ('Emergency protection signal'). O 'E' inicial e o ':23' ficam cortados ao lado da caixa. Provavelmente é uma sobreposição do estilo, mas atrapalha um pouco a leitura. |
| 5:05 | Q98 `9145.png` | medio | texto_encavalado | A caixa do contador cobre o início da linha 'Emergency protection signal'. Sobra um ':23' solto na borda esquerda. |
| 5:24 | Q105 `9722.png` | medio | fundo/faixa | Faixa escura na borda direita (RGB 31,28,25) e barra preta na borda esquerda ao lado do filme 4:3. Parece o pillarbox intencional do filme de época, mas as laterais estão escuras e lisas, sem o desfoque descrito no estilo do canal. Possível dúvida entre estilo e defeito. |
| 5:28 | Q106 `9848.png` | medio | valor_errado | A tela de título mostra "01:28" em amarelo escurecido, provavelmente em fade de entrada. Se não for transição, o contraste do número está fraco. |
| 5:46 | Q112 `10384.png` | alto | texto_encavalado | Os rótulos "PRIPYAT" e "CHERNOBYL NPP" estão sobrepostos no topo do mapa; "CHERNOBYL NPP" fica quase ilegível atrás de "PRIPYAT" e do círculo amarelo. |
| 6:22 | Q117 `11459.png` | alto | valor_errado | Cartão '250 FIREMEN ON SITE · 04:00' aparece com o relógio da cena em 06:00 (+04:36:20). O rótulo mostra 04:00 enquanto o contador marca 06:00. Parece inconsistência de dados. |
| 6:37 | Q120 `11910.png` | medio | texto_cortado | Cartão '28 WITHIN FOUR MONTHS · UNSCEAR' no canto superior direito passa por cima do helicóptero e cobre a ponta do rotor. A caixa também fica colada na borda direita. |
| 6:37 | Q120 `11910.png` | medio | valor_errado | A foto tem legenda '13 JUN 1986', mas o contador marca 'SAT 26 APR · ~10:00' (+08:36:20). A data da imagem destoa da linha do tempo. Pode ser intencional como ilustração; vale conferir. |
| 6:48 | Q122 `12227.png` | medio | fundo/faixa | O documento escaneado fica estreito no meio de um fundo escuro liso, com faixas pretas largas nas laterais (~8% à direita). Pode ser estilo intencional de documento em página inteira (0,5 s) antes do zoom. Se esse enquadramento durar mais que a abertura, fica parecendo vazio. |
| 6:56 | Q125 `12465.png` | medio | valor_errado | O número '1 · 1 · 34' com 'DEAD · MISSING · UNDER OBSERVATION' parece o estado final do contador. A leitura dos números separados por pontos é pouco clara. Os valores batem com o documento (1 morto, 1 desaparecido, 34 em observação). A faixa escura de 33% na base é só fundo liso do cartão de número, sem defeito. |
| 7:06 | Q129 `12793.png` | medio | elemento_fora | Quadrado cinza chapado (~40x35 px) solto sobre o documento, logo abaixo do trecho grifado à esquerda, parecendo placeholder ou elemento de UI quebrado. Não faz parte do documento. |
| 7:08 | Q130 `12836.png` | medio | elemento_fora | O mesmo quadrado cinza chapado aparece abaixo do grifo amarelo, à esquerda, e persiste no quadro seguinte da animação. Parece placeholder ou elemento de UI quebrado. |
| 7:26 | Q136 `13378.png` | medio | texto_cortado | O texto do documento é cortado na borda inferior. O crédito 'Order of the Ministry of Motor Transport · Wilson Center…' fica sobreposto à linha do documento ("к эвакуации населения…"), prejudicando a leitura dessa linha. |
| 7:27 | Q137 `13407.png` | medio | elemento_fora | O crédito no canto inferior esquerdo ('Order of the Ministry of Motor Transport · Wilson Center...') fica por cima da última linha do documento e atrapalha a leitura dela. Pode ser estilo intencional do crédito, mas a bíblia diz que não há crédito em tela, então vale conferir. |
| 7:39 | Q142 `13782.png` | medio | fundo/faixa | Filme 4:3 com laterais desfocadas escuras e uma faixa vertical escura bem marcada na borda direita (cerca de 8%). É o formato 4:3 intencional descrito no contexto do canal, mas a borda esquerda do filme parece ter linha preta dura. Conferir. |
| 7:48 | Q146 `14036.png` | medio | fundo/faixa | O sinal automático acusou faixa escura uniforme na base (31%) e na borda direita (8%). Visualmente é o fundo escuro com vinheta de um cartão de número, e o estilo parece intencional. Registro por dúvida entre estilo e defeito, sem bloqueio. |
| 8:22 | Q157 `15065.png` | medio | valor_errado | Contador mostra +33:36:20, igual ao de Q158-Q160, e a régua está em ~11:00. Os quadros anteriores mostravam +26:36:20 às 04:00. A diferença de 7 h bate com a de 04:00 para ~11:00, então o valor provavelmente está certo. Fica a dúvida porque o contador não tem nenhum segundo de variação entre quadros, o que pode indicar que está parado. |
| 9:48 | Q171 `17625.png` | medio | texto_encavalado | A caixa amarela '45,000 → 5,000' (canto superior direito) e o contador '+55:36:20' (esquerda) cobrem trechos do documento, e a legenda mono inferior sobrepõe a última linha ('crater of the reactor'). O documento está em zoom intencional e a linha grifada continua legível, então pode ser estilo; fica como dúvida. |
| 9:48 | Q172 `17643.png` | medio | texto_encavalado | Mesma situação do Q171: a caixa '45,000 → 5,000' e o contador cobrem texto do documento, e o crédito inferior sobrepõe a última linha. A leitura da linha grifada não é afetada, então a dúvida é entre estilo e defeito. |
| 10:38 | Q184 `19140.png` | medio | valor_errado | A foto é de 1 de maio de 1986 (RIVM, Holanda), mas a régua de horas e o contador continuam em MON 28 APR, +55:36:20, com o marcador em FORSMARK. Pode ser intencional (flashback), mas a data da ficha não bate com o HUD. |
| 10:53 | Q188 `19585.png` | medio | texto_encavalado | A régua de horas e o contador (canto superior esquerdo) ficam sobre o texto do jornal. A primeira linha do artigo fica atrás da régua e o contador sobrepõe parte do texto. O crédito 'UPI Archives' sobrepõe a última linha. O documento é lido na linha grifada, então a legibilidade só cai um pouco. |
| 10:57 | Q190 `19721.png` | medio | fundo/faixa | Há faixa lateral chapada e escura na borda direita (~8%, RGB 36,33,23). Pelo contexto, é o vídeo de época em 4:3 com laterais desfocadas, que é estilo intencional. Mas aqui a faixa direita parece lisa e chapada, não desfocada, e o lado esquerdo tem um degradê escuro diferente. Vale confirmar. |
| 11:00 | Q191 `19797.png` | medio | fundo/faixa | Faixa cinza chapada na borda direita (~8%, RGB 32,32,32), com cara de bloco sólido e não de lateral desfocada. O lado esquerdo tem um degradê diferente. Pode ser o 4:3 de época; confirmar. |
| 11:05 | Q192 `19949.png` | medio | valor_errado | O contador no canto superior esquerdo continua em +55:36:20 como nos quadros anteriores, e a régua marca Forsmark, mas a cena já é a do mapa com Chernobyl. Parece um contador congelado, não animado. Se for intencional, pode ficar assim. |
| 11:30 | Q198 `20713.png` | medio | texto_encavalado | Zoom do documento: o início da linha ('Dolgikh V. I.') e o texto no topo ('...Working copy') ficam cortados pela borda e o contador no canto sobrepõe o texto 'for...about the accident' e 'Nuclear Power Station]', atrapalhando a leitura. A legenda de crédito no rodapé também se sobrepõe ao texto do documento. |
| 11:33 | Q199 `20782.png` | medio | texto_encavalado | Mesmo caso do Q198: o contador no canto superior esquerdo cobre parte do texto do documento ('Nuclear Power Station]'), e a barra de crédito inferior se sobrepõe às linhas finais do documento ('Out of the 45,000 residents...'). |
| 11:41 | Q200 `21023.png` | alto | texto_cortado | No primeiro cartão, o texto '01:23:40' é mais largo que a caixa e encosta/ultrapassa as bordas esquerda e direita do cartão, ficando apertado e quase vazando. |
| 11:54 | Q202 `21419.png` | medio | texto_encavalado | No topo, o texto do documento passa por trás da régua de horas e do contador ("population.", "Gorbachev M.S." parcialmente cobertos pelo contador). Pode ser rolagem do documento em zoom, mas o texto cortado fica ilegível sob o HUD. |
| 11:55 | Q203 `21456.png` | medio | texto_encavalado | O contador cobre o início de "Gorbachev M.S." e o texto do topo corta sob a régua. O marca-texto da segunda linha ("delay.") invade a margem esquerda e fica parcialmente atrás do contador. |
| 12:00 | Q204 `21602.png` | medio | texto_encavalado | A linha de cima do documento ("...achev E.K. People were relocated...") passa por baixo da régua, e o nome "Yakovlev A.N." fica coberto pelo contador. O texto fica cortado e ilegível no topo. |
| 12:02 | Q205 `21660.png` | medio | texto_encavalado | O contador cobre o início de "Yakovlev A.N." e as linhas do topo sobem por trás da régua, sem leitura possível. |
| 12:08 | Q207 `21851.png` | medio | texto_encavalado | As linhas do topo do documento ("Ligachev E.K....", "Yakovlev A.N.") ficam sob a régua e o contador, com texto cortado e sobreposto. |
| 12:10 | Q208 `21894.png` | medio | texto_encavalado | O contador cobre "Yakovlev A.N." e as primeiras linhas do documento se sobrepõem à régua de horas. A leitura fica prejudicada. |
| 12:47 | Q215 `22998.png` | medio | texto_cortado | Documento (UPI) em zoom: texto cortado pelas bordas direita, superior e inferior, e a primeira linha fica atrás da régua de horas no topo ("White House spokesman Larry Speakes..."). Provavelmente é o enquadramento intencional do DocGrifo, mas a linha sobreposta à régua prejudica a leitura. Em dúvida entre estilo e defeito. |
| 12:47 | Q216 `23018.png` | medio | texto_cortado | Mesmo documento UPI: a primeira linha passa por trás da régua de horas e o texto é cortado nas bordas direita e inferior. Provável enquadramento do zoom, mas a linha sob a régua atrapalha. Em dúvida entre estilo e defeito. |
| 13:01 | Q220 `23418.png` | medio | texto_encavalado | No canto superior esquerdo, o contador 'SINCE THE SHUTDOWN BUTTON' cobre a bandeira e parte do cabeçalho 'Office of the Historian' e o início da linha 'FOREIGN RELATIONS OF THE UNITED STATES'. O texto do documento fica parcialmente tapado. O texto do documento também sai pela borda direita, mas isso é zoom intencional. |
| 13:02 | Q221 `23452.png` | medio | texto_encavalado | O contador cobre a bandeira e o início do cabeçalho do documento ('Office of the Historian', 'FOREIGN RELATIONS...'). Há sobreposição de texto no canto superior esquerdo, com leitura prejudicada. |
| 13:53 | Q232 `24989.png` | bloqueante | texto_encavalado | Os rótulos "PRIPYAT" e "CHERNOBYL NPP" estão sobrepostos perto do círculo da zona de 30 km. "CHERNOBYL NPP" fica ilegível, só aparece "...OBYL NPP" atrás de "PRIPYAT". |
| 13:53 | Q232 `24989.png` | medio | fundo/faixa | O mapa quase não tem terra visível: só um recorte pequeno de costa no topo, e o resto é um fundo cinza-azulado chapado. Há dúvida se é estilo do Mapa2D ou se faltou terra/mar. A cor também não segue o estilo descrito (areia #D9CBA8 e mar #0E2A3B). |
| 14:19 | Q238 `25773.png` | medio | texto_encavalado | A etiqueta de crédito 'Law of Ukraine No. 791a-XII, 27 Feb 1991' no canto inferior esquerdo se sobrepõe ao texto do documento '(обов'язкового)'. A leitura da linha do documento fica prejudicada. O crédito mono no canto é estilo do canal, então o defeito é só a colisão com o texto. |
| 14:20 | Q239 `25791.png` | medio | texto_encavalado | A etiqueta de crédito 'Law of Ukraine...' no canto inferior esquerdo se sobrepõe a '(обов'язкового)' do documento, dificultando a leitura dessa linha. |
| 14:32 | Q243 `26145.png` | medio | texto_cortado | O texto do documento ucraniano está cortado nas bordas esquerda e direita ("одер…", "…дукції", "…ань"), e a linha inferior "чорнобильської катастрофи" também está cortada pela borda de baixo. A chapa Law of Ukraine cobre parte do texto do rodapé. Pode ser zoom intencional do DocGrifo, por isso a gravidade é média. |
| 14:33 | Q244 `26184.png` | medio | texto_cortado | É o mesmo zoom do documento do Q243, com texto cortado nas laterais e embaixo. A legenda da fonte cobre a linha inferior. Provavelmente é movimento do DocGrifo, mas a leitura fica prejudicada. |
| 15:38 | Q259 `28128.png` | medio | texto_encavalado | A ficha '1986 · CHERNOBYL NPP UNIT 4' fica colada logo abaixo do rótulo '26 APR 1986 · ~01:24' e quase encosta nele. As linhas de crédito 'Film: Ukrkinokhronika...' e 'Photo: hnapel (CC0)' ficam apertadas embaixo. Isso lota o rodapé. Além disso, há créditos em tela, que a bíblia manda deixar só na descrição. |
| 15:44 | Q260 `28321.png` | medio | elemento_fora | A marca d'água/logo 'VOA' fica bem visível no canto inferior direito. É material de TV de terceiros (VOA News), contra a política de material da bíblia. Também há o crédito 'VOA News' em tela. |
| 15:58 | Q265 `28730.png` | medio | outro | Faixa preta na borda esquerda (~7%) e área escura grande à direita, quase preta. Pode ser o 4:3 de época sem as laterais desfocadas, que a bíblia descreve como estilo. Aqui as laterais estão pretas e não desfocadas, então fica a dúvida. A cena também está muito escura. |

51 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q01 (0:06): faixa uniforme na borda topo: 24% do quadro, cor RGB(13,14,16)
- Q01 (0:06): faixa uniforme na borda direita: 19% do quadro, cor RGB(13,14,16)
- Q07 (0:20): faixa uniforme na borda base: 22% do quadro, cor RGB(12,15,18)
- Q07 (0:20): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(12,14,17)
- Q07 (0:20): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q08 (0:23): faixa uniforme na borda direita: 7% do quadro, cor RGB(30,26,25)
- Q09 (0:28): faixa uniforme na borda base: 27% do quadro, cor RGB(46,48,51)
- Q09 (0:28): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(44,46,48)
- Q09 (0:28): faixa uniforme na borda direita: 8% do quadro, cor RGB(44,46,49)
- Q11 (0:34): faixa uniforme na borda direita: 8% do quadro, cor RGB(16,9,12)
- Q12 (0:36): faixa uniforme na borda direita: 8% do quadro, cor RGB(34,30,30)
- Q16 (0:48): faixa uniforme na borda direita: 7% do quadro, cor RGB(30,28,23)
- Q17 (0:51): faixa uniforme na borda direita: 7% do quadro, cor RGB(31,36,32)
- Q19 (0:58): faixa uniforme na borda base: 23% do quadro, cor RGB(12,15,18)
- Q19 (0:58): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q22 (1:05): faixa uniforme na borda direita: 7% do quadro, cor RGB(15,15,12)
- Q23 (1:08): faixa uniforme na borda direita: 8% do quadro, cor RGB(17,17,22)
- Q24 (1:12): faixa uniforme na borda direita: 9% do quadro, cor RGB(27,27,25)
- Q25 (1:16): faixa uniforme na borda direita: 7% do quadro, cor RGB(25,20,17)
- Q26 (1:21): faixa uniforme na borda topo: 8% do quadro, cor RGB(39,46,54)
- Q26 (1:21): faixa uniforme na borda direita: 3% do quadro, cor RGB(45,52,61)
- Q29 (1:33): faixa uniforme na borda topo: 33% do quadro, cor RGB(12,14,18)
- Q29 (1:33): faixa uniforme na borda base: 31% do quadro, cor RGB(12,15,18)
- Q29 (1:33): faixa uniforme na borda esquerda: 26% do quadro, cor RGB(12,14,18)
- Q29 (1:33): faixa uniforme na borda direita: 26% do quadro, cor RGB(12,15,18)
- Q30 (1:36): faixa uniforme na borda direita: 7% do quadro, cor RGB(30,33,29)
- Q34 (1:46): faixa uniforme na borda direita: 29% do quadro, cor RGB(12,15,18)
- Q35 (1:50): faixa uniforme na borda direita: 29% do quadro, cor RGB(12,15,18)
- Q36 (1:52): faixa uniforme na borda direita: 7% do quadro, cor RGB(16,16,14)
- Q37 (1:56): faixa uniforme na borda direita: 30% do quadro, cor RGB(12,15,18)
- Q38 (1:59): faixa preta na borda direita: 22% do quadro
- Q39 (2:03): faixa uniforme na borda base: 22% do quadro, cor RGB(12,15,18)
- Q39 (2:03): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(12,14,17)
- Q39 (2:03): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q43 (2:19): faixa uniforme na borda direita: 8% do quadro, cor RGB(18,17,16)
- Q54 (2:48): faixa uniforme na borda base: 22% do quadro, cor RGB(12,15,18)
- Q54 (2:48): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(12,14,17)
- Q54 (2:48): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q57 (2:55): faixa uniforme na borda direita: 8% do quadro, cor RGB(21,20,22)
- Q59 (3:01): faixa uniforme na borda base: 22% do quadro, cor RGB(12,15,18)
- Q59 (3:01): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(12,14,17)
- Q59 (3:01): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q60 (3:07): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q61 (3:10): faixa uniforme na borda direita: 8% do quadro, cor RGB(35,32,29)
- Q67 (3:29): faixa uniforme na borda base: 31% do quadro, cor RGB(12,15,18)
- Q67 (3:29): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q74 (3:44): faixa uniforme na borda direita: 5% do quadro, cor RGB(33,29,33)
- Q75 (3:50): faixa uniforme na borda base: 31% do quadro, cor RGB(12,15,18)
- Q75 (3:50): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q80 (4:03): faixa uniforme na borda base: 31% do quadro, cor RGB(12,15,18)
- Q80 (4:03): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q83 (4:14): faixa uniforme na borda base: 22% do quadro, cor RGB(12,15,18)
- Q83 (4:14): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(12,14,17)
- Q83 (4:14): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q84 (4:18): faixa uniforme na borda direita: 8% do quadro, cor RGB(16,16,14)
- Q85 (4:23): faixa uniforme na borda base: 26% do quadro, cor RGB(12,15,18)
- Q85 (4:23): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(12,14,17)
- Q85 (4:23): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q95 (4:50): faixa uniforme na borda base: 31% do quadro, cor RGB(12,15,18)
- Q95 (4:50): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q96 (4:58): faixa uniforme na borda base: 21% do quadro, cor RGB(12,15,18)
- Q96 (4:58): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q103 (5:16): faixa uniforme na borda direita: 8% do quadro, cor RGB(17,19,20)
- Q105 (5:24): faixa uniforme na borda direita: 8% do quadro, cor RGB(31,28,25)
- Q106 (5:28): faixa uniforme na borda base: 26% do quadro, cor RGB(12,15,18)
- Q106 (5:28): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(12,14,17)
- Q106 (5:28): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q107 (5:32): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q109 (5:38): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q114 (6:08): faixa uniforme na borda direita: 7% do quadro, cor RGB(43,43,43)
- Q115 (6:12): faixa uniforme na borda direita: 8% do quadro, cor RGB(62,62,58)
- Q116 (6:17): faixa uniforme na borda base: 22% do quadro, cor RGB(12,15,18)
- Q116 (6:17): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(12,14,17)
- Q116 (6:17): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q118 (6:26): faixa uniforme na borda direita: 8% do quadro, cor RGB(32,27,25)
- Q119 (6:31): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q122 (6:48): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q125 (6:56): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q125 (6:56): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q142 (7:39): faixa uniforme na borda direita: 8% do quadro, cor RGB(37,35,31)
- Q143 (7:42): faixa uniforme na borda base: 22% do quadro, cor RGB(12,15,18)
- Q143 (7:42): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(12,14,17)
- Q143 (7:42): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q146 (7:48): faixa uniforme na borda base: 31% do quadro, cor RGB(12,15,18)
- Q146 (7:48): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q153 (8:12): faixa uniforme na borda direita: 7% do quadro, cor RGB(36,38,34)
- Q154 (8:14): faixa uniforme na borda direita: 8% do quadro, cor RGB(26,26,23)
- Q159 (8:30): faixa uniforme na borda direita: 7% do quadro, cor RGB(27,22,21)
- Q161 (9:12): faixa uniforme na borda direita: 8% do quadro, cor RGB(28,27,28)
- Q162 (9:16): faixa uniforme na borda direita: 7% do quadro, cor RGB(16,13,14)
- Q163 (9:20): faixa uniforme na borda base: 23% do quadro, cor RGB(12,15,18)
- Q163 (9:20): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q164 (9:23): faixa uniforme na borda direita: 7% do quadro, cor RGB(30,41,53)
- Q165 (9:28): faixa uniforme na borda base: 23% do quadro, cor RGB(12,15,18)
- Q165 (9:28): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q166 (9:32): faixa preta na borda direita: 7% do quadro
- Q169 (9:40): faixa uniforme na borda base: 22% do quadro, cor RGB(12,15,18)
- Q169 (9:40): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(12,14,17)
- Q169 (9:40): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q170 (9:44): faixa uniforme na borda direita: 8% do quadro, cor RGB(41,34,33)
- Q173 (9:50): faixa uniforme na borda base: 22% do quadro, cor RGB(12,15,18)
- Q173 (9:50): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(12,14,17)
- Q173 (9:50): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q174 (9:56): faixa uniforme na borda direita: 7% do quadro, cor RGB(31,4,4)
- Q179 (10:14): faixa uniforme na borda direita: 7% do quadro, cor RGB(15,15,12)
- Q181 (10:20): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q182 (10:24): faixa uniforme na borda direita: 7% do quadro, cor RGB(23,23,21)
- Q183 (10:33): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q185 (10:41): faixa uniforme na borda direita: 7% do quadro, cor RGB(18,18,17)
- Q186 (10:45): faixa preta na borda direita: 8% do quadro
- Q190 (10:57): faixa uniforme na borda direita: 8% do quadro, cor RGB(36,33,23)
- Q191 (11:00): faixa uniforme na borda direita: 8% do quadro, cor RGB(32,32,32)
- Q193 (11:10): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q194 (11:13): faixa uniforme na borda direita: 8% do quadro, cor RGB(17,16,15)
- Q195 (11:17): faixa uniforme na borda direita: 8% do quadro, cor RGB(40,36,33)
- Q196 (11:22): faixa uniforme na borda direita: 8% do quadro, cor RGB(24,22,20)
- Q197 (11:24): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q200 (11:41): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q200 (11:41): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(12,14,17)
- Q200 (11:41): faixa uniforme na borda direita: 7% do quadro, cor RGB(12,15,18)
- Q201 (11:49): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q206 (12:04): faixa uniforme na borda direita: 8% do quadro, cor RGB(18,16,16)
- Q209 (12:13): faixa uniforme na borda base: 22% do quadro, cor RGB(12,15,18)
- Q209 (12:13): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(12,14,17)
- Q209 (12:13): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q210 (12:17): faixa uniforme na borda direita: 7% do quadro, cor RGB(11,14,19)
- Q211 (12:21): faixa uniforme na borda base: 21% do quadro, cor RGB(12,15,18)
- Q211 (12:21): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q212 (12:24): faixa uniforme na borda direita: 8% do quadro, cor RGB(10,39,27)
- Q213 (12:34): faixa uniforme na borda direita: 4% do quadro, cor RGB(6,44,26)
- Q214 (12:43): faixa uniforme na borda base: 27% do quadro, cor RGB(46,48,51)
- Q214 (12:43): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(44,46,48)
- Q214 (12:43): faixa uniforme na borda direita: 8% do quadro, cor RGB(44,46,49)
- Q217 (12:49): faixa uniforme na borda direita: 8% do quadro, cor RGB(16,10,9)
- Q218 (12:52): faixa uniforme na borda direita: 8% do quadro, cor RGB(21,21,6)
- Q219 (12:56): faixa uniforme na borda direita: 7% do quadro, cor RGB(30,30,28)
- Q224 (13:13): faixa uniforme na borda base: 22% do quadro, cor RGB(12,15,18)
- Q224 (13:13): faixa uniforme na borda esquerda: 8% do quadro, cor RGB(12,14,17)
- Q224 (13:13): faixa uniforme na borda direita: 8% do quadro, cor RGB(12,15,18)
- Q225 (13:20): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q228 (13:39): faixa uniforme na borda direita: 7% do quadro, cor RGB(32,32,26)
- Q230 (13:46): faixa uniforme na borda direita: 7% do quadro, cor RGB(25,28,24)
- Q231 (13:49): faixa uniforme na borda direita: 7% do quadro, cor RGB(42,40,38)
- Q232 (13:53): faixa uniforme na borda topo: 8% do quadro, cor RGB(39,46,54)
- Q232 (13:53): faixa uniforme na borda direita: 3% do quadro, cor RGB(45,52,61)
- Q233 (13:58): faixa uniforme na borda direita: 11% do quadro, cor RGB(52,48,46)
- Q235 (14:06): faixa uniforme na borda direita: 11% do quadro, cor RGB(29,28,29)
- Q237 (14:15): faixa uniforme na borda direita: 11% do quadro, cor RGB(62,58,56)
- Q238 (14:19): faixa uniforme na borda topo: 4% do quadro, cor RGB(255,255,255)
- Q239 (14:20): faixa uniforme na borda topo: 3% do quadro, cor RGB(255,255,255)
- Q241 (14:22): faixa uniforme na borda direita: 4% do quadro, cor RGB(254,254,254)
- Q242 (14:26): faixa uniforme na borda direita: 7% do quadro, cor RGB(22,16,11)
- Q243 (14:32): faixa uniforme na borda topo: 27% do quadro, cor RGB(255,255,255)
- Q244 (14:33): faixa uniforme na borda topo: 27% do quadro, cor RGB(255,255,255)
- Q247 (14:41): faixa uniforme na borda topo: 33% do quadro, cor RGB(12,14,18)
- Q247 (14:41): faixa uniforme na borda base: 31% do quadro, cor RGB(12,15,18)
- Q247 (14:41): faixa uniforme na borda esquerda: 27% do quadro, cor RGB(12,14,18)
- Q247 (14:41): faixa uniforme na borda direita: 27% do quadro, cor RGB(12,15,18)
- Q249 (14:53): faixa uniforme na borda topo: 9% do quadro, cor RGB(34,40,48)
- Q250 (14:57): faixa uniforme na borda topo: 9% do quadro, cor RGB(12,14,18)
- Q250 (14:57): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q250 (14:57): faixa uniforme na borda esquerda: 27% do quadro, cor RGB(12,14,18)
- Q253 (15:09): faixa uniforme na borda topo: 23% do quadro, cor RGB(12,14,18)
- Q253 (15:09): faixa uniforme na borda base: 22% do quadro, cor RGB(12,15,18)
- Q253 (15:09): faixa uniforme na borda esquerda: 33% do quadro, cor RGB(12,14,18)
- Q253 (15:09): faixa uniforme na borda direita: 33% do quadro, cor RGB(12,15,18)
- Q254 (15:13): faixa uniforme na borda topo: 4% do quadro, cor RGB(128,155,180)
- Q255 (15:16): faixa uniforme na borda topo: 9% do quadro, cor RGB(12,14,18)
- Q255 (15:16): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q255 (15:16): faixa uniforme na borda esquerda: 13% do quadro, cor RGB(12,14,18)
- Q256 (15:20): faixa uniforme na borda topo: 6% do quadro, cor RGB(182,188,188)
- Q257 (15:28): faixa uniforme na borda topo: 9% do quadro, cor RGB(12,14,18)
- Q257 (15:28): faixa uniforme na borda base: 33% do quadro, cor RGB(12,15,18)
- Q257 (15:28): faixa uniforme na borda esquerda: 11% do quadro, cor RGB(12,14,18)
- Q259 (15:38): faixa uniforme na borda topo: 8% do quadro, cor RGB(12,14,18)
- Q264 (15:55): faixa uniforme na borda direita: 7% do quadro, cor RGB(17,13,14)
- Q265 (15:58): faixa preta na borda direita: 28% do quadro
- Q268 (16:07): faixa uniforme na borda direita: 4% do quadro, cor RGB(254,254,254)
- Q269 (16:13): faixa uniforme na borda base: 7% do quadro, cor RGB(34,26,25)
- Q269 (16:13): faixa uniforme na borda esquerda: 4% do quadro, cor RGB(34,26,25)
- Q269 (16:13): faixa uniforme na borda direita: 4% do quadro, cor RGB(17,20,24)
- Q270 (16:17): faixa uniforme na borda topo: 24% do quadro, cor RGB(13,14,16)
- Q270 (16:17): faixa uniforme na borda direita: 19% do quadro, cor RGB(13,14,16)
- Q271 (16:23): faixa uniforme na borda topo: 33% do quadro, cor RGB(46,48,51)
- Q271 (16:23): faixa uniforme na borda base: 27% do quadro, cor RGB(46,48,51)
- Q271 (16:23): faixa uniforme na borda esquerda: 22% do quadro, cor RGB(46,48,51)
- Q271 (16:23): faixa uniforme na borda direita: 22% do quadro, cor RGB(46,48,51)
- Q274 (16:33): faixa uniforme na borda topo: 27% do quadro, cor RGB(13,15,19)
- Q274 (16:33): faixa uniforme na borda base: 28% do quadro, cor RGB(13,16,19)
- Q274 (16:33): faixa uniforme na borda esquerda: 14% do quadro, cor RGB(13,15,19)
- Q274 (16:33): faixa uniforme na borda direita: 14% do quadro, cor RGB(13,16,19)
- Q275 (16:38): faixa uniforme na borda topo: 27% do quadro, cor RGB(12,14,18)
- Q275 (16:38): faixa uniforme na borda base: 26% do quadro, cor RGB(12,15,18)
- Q275 (16:38): faixa uniforme na borda esquerda: 14% do quadro, cor RGB(12,14,18)
- Q275 (16:38): faixa uniforme na borda direita: 14% do quadro, cor RGB(12,15,18)

## Quadros

Q01=0:06, Q02=0:10, Q03=0:11, Q04=0:13, Q05=0:13, Q06=0:16, Q07=0:20, Q08=0:23, Q09=0:28, Q10=0:32, Q11=0:34, Q12=0:36, Q13=0:41, Q14=0:44, Q15=0:45, Q16=0:48, Q17=0:51, Q18=0:54, Q19=0:58, Q20=1:00, Q21=1:02, Q22=1:05, Q23=1:08, Q24=1:12, Q25=1:16, Q26=1:21, Q27=1:25, Q28=1:29, Q29=1:33, Q30=1:36, Q31=1:40, Q32=1:43, Q33=1:44, Q34=1:46, Q35=1:50, Q36=1:52, Q37=1:56, Q38=1:59, Q39=2:03, Q40=2:08, Q41=2:13, Q42=2:16, Q43=2:19, Q44=2:21, Q45=2:22, Q46=2:24, Q47=2:30, Q48=2:32, Q49=2:34, Q50=2:35, Q51=2:36, Q52=2:39, Q53=2:42, Q54=2:48, Q55=2:52, Q56=2:53, Q57=2:55, Q58=2:58, Q59=3:01, Q60=3:07, Q61=3:10, Q62=3:13, Q63=3:14, Q64=3:18, Q65=3:25, Q66=3:27, Q67=3:29, Q68=3:32, Q69=3:33, Q70=3:36, Q71=3:37, Q72=3:40, Q73=3:41, Q74=3:44, Q75=3:50, Q76=3:54, Q77=3:54, Q78=3:57, Q79=3:58, Q80=4:03, Q81=4:08, Q82=4:10, Q83=4:14, Q84=4:18, Q85=4:23, Q86=4:27, Q87=4:27, Q88=4:31, Q89=4:33, Q90=4:36, Q91=4:42, Q92=4:44, Q93=4:46, Q94=4:47, Q95=4:50, Q96=4:58, Q97=5:04, Q98=5:05, Q99=5:09, Q100=5:11, Q101=5:14, Q102=5:14, Q103=5:16, Q104=5:19, Q105=5:24, Q106=5:28, Q107=5:32, Q108=5:35, Q109=5:38, Q110=5:42, Q111=5:43, Q112=5:46, Q113=5:59, Q114=6:08, Q115=6:12, Q116=6:17, Q117=6:22, Q118=6:26, Q119=6:31, Q120=6:37, Q121=6:42, Q122=6:48, Q123=6:51, Q124=6:52, Q125=6:56, Q126=6:59, Q127=6:59, Q128=7:02, Q129=7:06, Q130=7:08, Q131=7:10, Q132=7:13, Q133=7:16, Q134=7:19, Q135=7:22, Q136=7:26, Q137=7:27, Q138=7:29, Q139=7:29, Q140=7:34, Q141=7:36, Q142=7:39, Q143=7:42, Q144=7:45, Q145=7:46, Q146=7:48, Q147=7:51, Q148=7:52, Q149=7:57, Q150=8:04, Q151=8:06, Q152=8:08, Q153=8:12, Q154=8:14, Q155=8:18, Q156=8:20, Q157=8:22, Q158=8:26, Q159=8:30, Q160=8:59, Q161=9:12, Q162=9:16, Q163=9:20, Q164=9:23, Q165=9:28, Q166=9:32, Q167=9:36, Q168=9:37, Q169=9:40, Q170=9:44, Q171=9:48, Q172=9:48, Q173=9:50, Q174=9:56, Q175=10:02, Q176=10:03, Q177=10:09, Q178=10:11, Q179=10:14, Q180=10:16, Q181=10:20, Q182=10:24, Q183=10:33, Q184=10:38, Q185=10:41, Q186=10:45, Q187=10:48, Q188=10:53, Q189=10:55, Q190=10:57, Q191=11:00, Q192=11:05, Q193=11:10, Q194=11:13, Q195=11:17, Q196=11:22, Q197=11:24, Q198=11:30, Q199=11:33, Q200=11:41, Q201=11:49, Q202=11:54, Q203=11:55, Q204=12:00, Q205=12:02, Q206=12:04, Q207=12:08, Q208=12:10, Q209=12:13, Q210=12:17, Q211=12:21, Q212=12:24, Q213=12:34, Q214=12:43, Q215=12:47, Q216=12:47, Q217=12:49, Q218=12:52, Q219=12:56, Q220=13:01, Q221=13:02, Q222=13:07, Q223=13:09, Q224=13:13, Q225=13:20, Q226=13:28, Q227=13:34, Q228=13:39, Q229=13:42, Q230=13:46, Q231=13:49, Q232=13:53, Q233=13:58, Q234=14:03, Q235=14:06, Q236=14:09, Q237=14:15, Q238=14:19, Q239=14:20, Q240=14:22, Q241=14:22, Q242=14:26, Q243=14:32, Q244=14:33, Q245=14:35, Q246=14:38, Q247=14:41, Q248=14:46, Q249=14:53, Q250=14:57, Q251=15:00, Q252=15:04, Q253=15:09, Q254=15:13, Q255=15:16, Q256=15:20, Q257=15:28, Q258=15:32, Q259=15:38, Q260=15:44, Q261=15:49, Q262=15:52, Q263=15:53, Q264=15:55, Q265=15:58, Q266=16:02, Q267=16:06, Q268=16:07, Q269=16:13, Q270=16:17, Q271=16:23, Q272=16:29, Q273=16:31, Q274=16:33, Q275=16:38
