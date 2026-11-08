# ROTEIRO: longo 01 do canal de clima (pt-BR) — "7 tornados em 6 dias"

Brief: `~/workspace/referencias/BRIEF-clima-longo-01.md` (estrutura aprovada pelo Rodrigo, 08/11/2026). Fonte única do texto: `shared/roteiro.py` → `shared/blocos.json` (fala com números por extenso; legenda da tela com algarismos). Fatos e fontes: `SOURCES.md` e `pesquisa/FATOS.md`.

- **Duração:** 11:19 (fala termina em 11:17). 51 blocos, 1.756 palavras faladas.
- **Hook:** o do piloto, sem mudança ("Maringá, Paraná, 2 de novembro…" → Chapecó → Santo Augusto → 7 em 6 dias → a pergunta → 3 caixinhas).
- **Voz:** Kokoro `pf_dora`, custo zero, em 2 marchas (pedido do Rodrigo):

| Marcha | Blocos | Ajuste | Palavras/min (fala + pausas internas) |
|---|---|---|---|
| 1 (igual ao piloto) | b01–b07 (0:00–0:49) | velocidade 1,1 + atempo 1,05; pausa entre frases 0,20 s | **183** |
| 1,5 (transição) | b08–b09 (0:50–1:21) | velocidade 1,02 + atempo 1,02; pausa 0,32 s | 187* |
| 2 (mais calma) | b10–b51 (1:21–fim) | velocidade 0,88, sem atempo; pausa entre frases 0,50 s e entre blocos 0,75 s | **165** |

\* Os blocos de transição têm muitos números por extenso ("cento e oitenta e duzentos e cinquenta e três quilômetros por hora"), que inflam a contagem de palavras; a velocidade efetiva cai em degraus (1,155 → 1,04 → 0,88), sem salto num bloco só.
- **Perguntas:** a Kokoro lê pergunta sem entonação. Cada frase com "?" é gerada separada e ganha uma rampa de pitch nos últimos ~0,5 s (rubberband do ffmpeg, +7% nas abertas e +10% nas de sim/não, com formantes preservados), mais 0,12 s de pausa depois. No Whisper do vídeo final, 6 das 10 perguntas saíram transcritas com "?" (0:33, 0:35, 0:37, 0:40, 7:58 e 10:53).
- **Pronúncia corrigida na fala:** "Inméti" (Inmet), "Méti Sul" (MetSul), "éfe dois" (F2), "cép", "quatro, zero, um, nove, nove".

## Texto com tempos (tempos do `out/video.mp4`)
| Bloco | Tempo | Aba | Marcha | Texto (tela) |
|---|---|---|---|---|
| b01 | 0:00.1–0:08.3 | MARINGÁ | 1 | Maringá, Paraná, 2 de novembro. / Um tornado F2, com ventos de até 250 km/h, / atinge 40% da cidade. |
| b02 | 0:09.6–0:17.5 | CHAPECÓ | 1 | Dois dias depois, Chapecó, Santa Catarina. / 16 km de destruição. / Para a Defesa Civil, / o maior evento climático em 50 anos. |
| b03 | 0:18.8–0:23.9 | SANTO AUGUSTO | 1 | No dia 7, Santo Augusto, no Rio Grande do Sul. / 50 casas destelhadas de madrugada. |
| b04 | 0:25.2–0:27.5 | 7 EM 6 DIAS | 1 | 7 tornados confirmados em 6 dias. |
| b05 | 0:28.9–0:33.9 | A PERGUNTA | 1 | O que está acontecendo no Sul do Brasil / para ter tantos eventos dessa magnitude, / como nunca antes? |
| b06 | 0:34.3–0:40.4 | A PERGUNTA | 1 | Por que isso está acontecendo? / Qual o risco de voltar a acontecer? / E até que proporção isso pode chegar? |
| b07 | 0:40.8–0:49.4 | A PERGUNTA | 1 | 3 perguntas, 3 caixinhas. / Vamos abrir uma por uma. / Mas antes, é preciso entender o que aconteceu de verdade nesses 6 dias. / Porque não foi um evento só. |
| b08 | 0:50.7–1:02.2 | DIA 1 · 2/11 | 1.5 | Domingo à noite, 1º de novembro. / Um ciclone se forma na costa do Rio Grande do Sul / e organiza uma frente fria, que avança pelo Paraná. / Por volta das 3 da manhã, / uma supercélula chega a Maringá. |
| b09 | 1:02.8–1:20.9 | DIA 1 · 2/11 | 1.5 | O aeroporto mede rajadas de quase 100 km/h. / Mas o vento mais forte não passou pela estação. / O Simepar foi a campo, mediu o estrago / e classificou o tornado como F2: / ventos estimados entre 180 e 253 km/h, / num rastro de uns 15 km. |
| b10 | 1:21.5–1:32.9 | DIA 1 · 2/11 | 2 | Ninguém morreu. / Mas, 2 dias depois, a cidade ainda contava / quase 900 árvores no chão, / 219 postes quebrados / e 35 mil imóveis sem luz. |
| b11 | 1:34.2–1:46.4 | DIA 3 · 4/11 | 2 | 2 dias de trégua. / E então vem a quarta-feira, 4 de novembro, / o dia mais violento da semana. / Uma linha de tempestades atravessa / o oeste de Santa Catarina e o norte gaúcho. |
| b12 | 1:47.2–2:05.1 | DIA 3 · 4/11 | 2 | 10h30 da manhã, Chapecó. / O radar mostra o vento girando dentro da tempestade. / Uma estação do Inmet mede 126 km/h. / No aeroporto, um avião da Azul está parado na pista, / e a tripulação descreve: / "o avião está chacoalhando muito". |
| b13 | 2:05.9–2:18.0 | DIA 3 · 4/11 | 2 | Hangares destruídos, peças de metal arrancadas, / cerca de 2.400 casas e indústrias destelhadas. / A Defesa Civil tinha emitido o aviso de temporal / 15 minutos antes. |
| b14 | 2:18.7–2:28.8 | DIA 3 · 4/11 | 2 | 18 minutos depois, a mesma linha de tempestades / gera outro tornado, em Xanxerê, / a uns 40 km dali. / Caminhões e ônibus tombam na rodovia. |
| b15 | 2:29.6–2:45.6 | DIA 3 · 4/11 | 2 | Na mesma manhã, do outro lado do rio Uruguai, / um tornado arrasa um eucaliptal inteiro em Erval Grande / e derruba uma torre de alta tensão em Barra do Rio Azul. / E à 1h30 da tarde, já no Planalto Norte, / é a vez de Rio Negrinho: / 82 casas atingidas. |
| b16 | 2:46.4–2:53.8 | DIA 3 · 4/11 | 2 | 4 tornados num único dia. / Nos temporais daquela quarta-feira, / 2 pessoas morreram em Santa Catarina. |
| b17 | 2:55.1–3:12.6 | DIA 6 · 7/11 | 2 | Sábado, 7 de novembro, de madrugada. / Uma única supercélula cruza o noroeste gaúcho. / À 1h18, Santo Augusto: / cerca de 50 casas destelhadas. / 36 minutos depois, a mesma tempestade / gera outro tornado, em Palmeira das Missões. |
| b18 | 3:13.9–3:24.6 | 7 EM 6 DIAS | 2 | 7 tornados confirmados pelas Defesas Civis, em 6 dias. / 3 no Rio Grande do Sul, 3 em Santa Catarina, 1 no Paraná. / 9 municípios atingidos. |
| b19 | 3:25.9–3:32.6 | É INÉDITO? | 2 | Agora, a pergunta que todo mundo fez. / Isso é inédito? / A resposta curta é: não. |
| b20 | 3:33.3–3:47.2 | É INÉDITO? | 2 | Em abril de 2015, um tornado atravessou Xanxerê, / a mesma cidade de agora, / e atingiu mais de 2 mil casas. / Em 2009, Guaraciaba, no extremo oeste catarinense, / teve um tornado F3, com 4 mortos. |
| b21 | 3:48.0–4:05.7 | É INÉDITO? | 2 | E há exatamente 1 ano, em 7 de novembro de 2025, / Rio Bonito do Iguaçu, no Paraná, / foi atingida por um F4. / Um rastro de 75 km, com até 3 km de largura. / 90% da área urbana atingida. / 7 mortes no estado. |
| b22 | 4:06.5–4:16.9 | É INÉDITO? | 2 | Os números também sobem. / Em 2025, o Brasil registrou 92 tornados, um recorde. / Até julho deste ano, já eram 81. |
| b23 | 4:17.7–4:41.9 | É INÉDITO? | 2 | Mas atenção: mais registros não significam, / necessariamente, mais tornados. / Hoje todo mundo tem uma câmera no bolso, / e desde 2018 uma plataforma reúne cada relato. / Um estudo de 2011 mostrou que os relatos de tornado no Brasil / se multiplicaram por 10 em 30 anos, / e boa parte disso é a gente vendo mais. / Entre os especialistas, não há consenso. |
| b24 | 4:42.7–5:02.7 | É INÉDITO? | 2 | O que não muda é o mapa. / A faixa entre o norte da Argentina, o Paraguai, o Uruguai e o Sul do Brasil / é considerada por pesquisadores / a 2ª região mais propícia a tornados do mundo, / depois dos Estados Unidos. / E satélites da NASA mostraram que as tempestades daqui / estão entre as mais intensas da Terra. |
| b25 | 5:04.0–5:07.7 | CAIXA 1 · POR QUÊ | 2 | Primeira caixinha. / Por que isso acontece aqui? |
| b26 | 5:08.5–5:21.8 | CAIXA 1 · POR QUÊ | 2 | Comece pela Amazônia. / A floresta joga uma quantidade enorme de umidade no ar. / A uns 1.500 m de altitude, um vento forte, / o jato de baixos níveis, / carrega esse ar quente e úmido para o sul. |
| b27 | 5:22.5–5:36.0 | CAIXA 1 · POR QUÊ | 2 | No caminho, existe uma parede: / a Cordilheira dos Andes. / Ela barra o ar e o canaliza, colado à encosta, / direto para o Paraguai, o norte da Argentina e o Sul do Brasil. / É como um rio invisível de umidade. |
| b28 | 5:36.7–5:47.1 | CAIXA 1 · POR QUÊ | 2 | Do outro lado, chegam as frentes frias, / vindas da Argentina. / Quando o ar frio encontra esse ar quente e úmido, / o ar quente é empurrado para cima. / É o gatilho. |
| b29 | 5:47.9–6:04.9 | CAIXA 1 · POR QUÊ | 2 | Uma tempestade comum sobe e chove. / Mas aqui tem um ingrediente a mais: / o vento muda de direção e de força com a altura. / Perto do chão, sopra de um lado. / Lá em cima, mais forte, de outro. / E o ar entre as camadas começa a rolar, / deitado, como um rolo de massa. |
| b30 | 6:05.6–6:19.1 | CAIXA 1 · POR QUÊ | 2 | A corrente que sobe dentro da nuvem / levanta esse rolo e o põe em pé. / Agora, a tempestade inteira gira. / É a supercélula. / Esse giro, com alguns km de largura, / se chama mesociclone, e aparece no radar. |
| b31 | 6:19.8–6:29.4 | CAIXA 1 · POR QUÊ | 2 | Na traseira, uma descida de ar frio / se enrola em volta do giro. / Em parte dos casos, ele se estreita, / acelera e toca o chão. / É o tornado. |
| b32 | 6:30.2–6:45.0 | CAIXA 1 · POR QUÊ | 2 | E aqui vai uma coisa que pouca gente sabe: / a maioria das supercélulas não gera tornado. / E por que algumas geram e outras não, / o próprio laboratório de tempestades do governo americano admite: / a ciência ainda não entende totalmente. |
| b33 | 6:45.8–6:56.0 | CAIXA 1 · POR QUÊ | 2 | Umidade da Amazônia, a parede dos Andes, / frentes frias e vento que muda com a altura. / Poucos lugares do planeta juntam esses 4 ingredientes / como o Sul do Brasil. |
| b34 | 6:57.4–7:18.3 | EL NIÑO | 2 | E este ano tem um agravante. / O Pacífico equatorial está mais de 2 °C acima do normal. / É um El Niño muito forte, e ainda se fortalecendo. / A NOAA dá 83% de chance de ele se tornar / o mais forte desde 1950, / quando as medições começaram. |
| b35 | 7:19.1–7:28.5 | EL NIÑO | 2 | O El Niño deixa o jato de baixos níveis / mais frequente e mais forte. / Mais umidade chegando ao Sul. / Mais chuva. / Mais dias com os ingredientes juntos. |
| b36 | 7:29.2–7:53.7 | EL NIÑO | 2 | Mas cuidado com o que a ciência não diz. / O El Niño não causa cada tornado, / e não há estudo que ligue o El Niño, sozinho, ao número de tornados. / Ele aumenta as chances. / E o aquecimento global? / Ele deixa a atmosfera mais quente e úmida, / o que alimenta tempestades. / Mas, para tornados, o IPCC diz que os registros / ainda são curtos demais para afirmar uma tendência. |
| b37 | 7:55.0–8:01.3 | CAIXA 2 · RISCO | 2 | Segunda caixinha. / Qual o risco de voltar a acontecer? / Alto. / E não é exagero. |
| b38 | 8:02.1–8:16.9 | CAIXA 2 · RISCO | 2 | O pico do El Niño está previsto para a virada do ano, / entre dezembro e janeiro. / A previsão para novembro, dezembro e janeiro / é de chuva acima da média no Sul, / com destaque para o oeste catarinense. / E os solos já estão encharcados. |
| b39 | 8:17.7–8:27.8 | CAIXA 2 · RISCO | 2 | A temporada mais ativa de tornados / vai do fim do inverno à primavera. / Ou seja: estamos no meio dela. / E a MetSul alerta para eventos extremos / também no verão. |
| b40 | 8:28.6–8:43.6 | CAIXA 2 · RISCO | 2 | No mapa, as regiões mais expostas formam um arco: / o norte e o noroeste gaúcho, / o oeste de Santa Catarina / e o sudoeste do Paraná. / Mas este ano mostrou que o risco não para aí: / o norte do Paraná e os Campos Gerais também tiveram tornados. |
| b41 | 8:44.4–8:55.9 | CAIXA 2 · RISCO | 2 | Ninguém consegue prever onde cai o próximo tornado. / Mas dá para prever os dias de risco, / com 1 ou 2 dias de antecedência. / Já o alerta do tornado em si / chega com minutos. |
| b42 | 8:57.2–9:01.3 | CAIXA 3 · ATÉ ONDE | 2 | Terceira caixinha. / Até que proporção isso pode chegar? |
| b43 | 9:02.1–9:22.1 | CAIXA 3 · ATÉ ONDE | 2 | Tornados são classificados pelo estrago, / numa escala de 0 a 5. / O Brasil usa a escala Fujita original. / Maringá foi um F2: até 253 km/h. / Um F4, como o de Rio Bonito do Iguaçu, / passa dos 330. / Um F5, dos 420. |
| b44 | 9:22.9–9:36.8 | CAIXA 3 · ATÉ ONDE | 2 | O Brasil nunca teve um F5 confirmado. / Mas a região já teve: / San Justo, na Argentina, em 1973, / a uns 300 km da fronteira gaúcha. / 63 mortos. |
| b45 | 9:37.6–9:51.9 | CAIXA 3 · ATÉ ONDE | 2 | Nos Estados Unidos, são cerca de 1.200 tornados por ano. / O mais largo já medido, em El Reno, / tinha 4,2 km de largura. / O de Rio Bonito do Iguaçu chegou a 3,2 km. |
| b46 | 9:52.7–10:08.7 | CAIXA 3 · ATÉ ONDE | 2 | O pior cenário não é um tornado maior. / É um tornado forte sobre uma cidade grande. / Um F3, ou F4, cruzando uma Chapecó, uma Maringá. / A região tem os ingredientes para isso. / Por isso, o que mais importa / é saber o que fazer. |
| b47 | 10:10.1–10:23.4 | O QUE FAZER | 2 | Primeiro: receba os alertas no celular. / Mande o seu CEP por SMS para 40199. / É de graça. / E, no Sul, o Defesa Civil Alerta / aparece direto na tela do celular, / com som, sem cadastro. |
| b48 | 10:24.1–10:33.6 | O QUE FAZER | 2 | Segundo: conheça os sinais. / Uma nuvem baixa e escura girando. / Uma nuvem em forma de funil. / Granizo grande. / Um ronco contínuo, como um trem chegando. |
| b49 | 10:34.3–10:50.4 | O QUE FAZER | 2 | Terceiro: se o alerta tocar, / vá para um cômodo pequeno no andar mais baixo, / sem janelas, como um banheiro, / e proteja a cabeça. / Longe de vidro, de galpões e de árvores. / Ao ar livre, deite numa vala. / E nunca se abrigue embaixo de um viaduto. |
| b50 | 10:51.7–11:10.5 | A RESPOSTA | 2 | Então, o que está acontecendo no Sul? / Não é um mistério, nem um castigo. / É o encontro da Amazônia com os Andes e com o frio do sul, / num dos cantos mais tempestuosos do planeta, / turbinado este ano por um El Niño muito forte. / Os tornados sempre estiveram aqui. / Agora, estamos vendo cada um deles. |
| b51 | 11:11.3–11:16.9 | A RESPOSTA | 2 | Manda este vídeo para quem mora no Sul. / E se inscreve: a temporada ainda não acabou. |
