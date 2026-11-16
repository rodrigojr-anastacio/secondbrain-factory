# ROTEIRO: longo 01 do canal de clima (pt-BR) — "7 tornados em 6 dias"

Brief: `~/workspace/referencias/BRIEF-clima-longo-01.md` (estrutura aprovada pelo Rodrigo, 08/11/2026). Fonte única do texto: `shared/roteiro.py` → `shared/blocos.json` (fala com números por extenso; legenda da tela com algarismos). Fatos e fontes: `SOURCES.md` e `pesquisa/FATOS.md`.

- **v2 (08/11/2026, brief `BRIEF-clima-longo-01-v2.md`):** voz ElevenLabs v3 e texto sem "caixinhas". A v1 (Kokoro, 11:19) está no histórico do git.
- **Duração:** 10:23 (fala termina em 10:20). 51 blocos, 1.762 palavras faladas.
- **Hook:** o do piloto, com a pergunta reescrita: fatos → "Então... o que está acontecendo no Sul do Brasil? Por que tantos eventos dessa magnitude, como nunca antes?" → "Isso nos leva às seguintes perguntas." → as 3 perguntas → "Mas antes, é preciso entender o que aconteceu de verdade nesses 6 dias…".
- **Sem "caixinha":** b25 "Então, por que isso acontece justamente aqui?"; b37 "E a pergunta que todo mundo no Sul está fazendo: isso vai voltar a acontecer?"; b42 "Agora, a pergunta mais difícil: até onde isso pode chegar?". Na tela, as abas viram "PERGUNTA 1/3 · POR QUÊ", "PERGUNTA 2/3 · RISCO", "PERGUNTA 3/3 · ATÉ ONDE".
- **Voz:** ElevenLabs `eleven_v3`, voz "Fernanda" (`7iqXtOF3wl3pomwXFY7G`), `stability 0.0`, `similarity_boost 0.8`, um request por bloco (`shared/gera_voz_eleven.py`; o texto com tags fica em `fala_tts` no `blocos.json`). Tags de emoção: `[serious]` no início dos fatos, `[curious]`/`[intrigued]` antes das perguntas. Velocidade por atempo no ffmpeg (`shared/monta_audio_v2.py`):

| Trecho | Blocos | Atempo | Palavras/min (fala + pausas entre blocos) |
|---|---|---|---|
| Hook | b01–b06 (0:00–0:46) | 1,3 | **144** |
| Passagem | b07 (0:46–0:52) | 1,25 | 201* |
| Resto | b08–b51 (0:53–fim) | 1,2 | **173** |

\* b07 é um bloco só, sem pergunta, e soa corrido; o hook tem 6 perguntas com pausa dramática e as tags `[serious]`, por isso conta menos palavras por minuto mesmo a 1,3×.
- **Pronúncia na fala:** "Inméti" (Inmet), "Méti Sul" (MetSul), "éfe dois" (F2), "cép", "quatro, zero, um, nove, nove"; números por extenso.

## Texto com tempos (tempos do `out/video-v2.mp4`)
| Bloco | Tempo | Aba | Atempo | Texto (tela) |
|---|---|---|---|---|
| b01 | 0:00.1–0:08.2 | MARINGÁ | 1.3 | Maringá, Paraná, 2 de novembro. / Um tornado F2, com ventos de até 250 km/h, / atinge 40% da cidade. |
| b02 | 0:09.5–0:18.7 | CHAPECÓ | 1.3 | Dois dias depois, Chapecó, Santa Catarina. / 16 km de destruição. / Para a Defesa Civil, / o maior evento climático em 50 anos. |
| b03 | 0:20.1–0:24.8 | SANTO AUGUSTO | 1.3 | No dia 7, Santo Augusto, no Rio Grande do Sul. / 50 casas destelhadas de madrugada. |
| b04 | 0:26.1–0:28.5 | 7 EM 6 DIAS | 1.3 | 7 tornados confirmados em 6 dias. |
| b05 | 0:29.9–0:36.6 | A PERGUNTA | 1.3 | Então... o que está acontecendo no Sul do Brasil? / Por que tantos eventos dessa magnitude, / como nunca antes? |
| b06 | 0:37.0–0:46.0 | A PERGUNTA | 1.3 | Isso nos leva às seguintes perguntas. / Por que isso está acontecendo? / Qual o risco de voltar a acontecer? / E até que proporção isso pode chegar? |
| b07 | 0:46.4–0:52.1 | A PERGUNTA | 1.25 | Mas antes, é preciso entender o que aconteceu de verdade nesses 6 dias. / Porque não foi um evento só. |
| b08 | 0:53.4–1:04.3 | DIA 1 · 2/11 | 1.2 | Domingo à noite, 1º de novembro. / Um ciclone se forma na costa do Rio Grande do Sul / e organiza uma frente fria, que avança pelo Paraná. / Por volta das 3 da manhã, / uma supercélula chega a Maringá. |
| b09 | 1:04.9–1:22.3 | DIA 1 · 2/11 | 1.2 | O aeroporto mede rajadas de quase 100 km/h. / Mas o vento mais forte não passou pela estação. / O Simepar foi a campo, mediu o estrago / e classificou o tornado como F2: / ventos estimados entre 180 e 253 km/h, / num rastro de uns 15 km. |
| b10 | 1:22.9–1:32.7 | DIA 1 · 2/11 | 1.2 | Ninguém morreu. / Mas, 2 dias depois, a cidade ainda contava / quase 900 árvores no chão, / 219 postes quebrados / e 35 mil imóveis sem luz. |
| b11 | 1:34.1–1:44.0 | DIA 3 · 4/11 | 1.2 | 2 dias de trégua. / E então vem a quarta-feira, 4 de novembro, / o dia mais violento da semana. / Uma linha de tempestades atravessa / o oeste de Santa Catarina e o norte gaúcho. |
| b12 | 1:44.7–1:59.6 | DIA 3 · 4/11 | 1.2 | 10h30 da manhã, Chapecó. / O radar mostra o vento girando dentro da tempestade. / Uma estação do Inmet mede 126 km/h. / No aeroporto, um avião da Azul está parado na pista, / e a tripulação descreve: / "o avião está chacoalhando muito". |
| b13 | 2:00.3–2:10.3 | DIA 3 · 4/11 | 1.2 | Hangares destruídos, peças de metal arrancadas, / cerca de 2.400 casas e indústrias destelhadas. / A Defesa Civil tinha emitido o aviso de temporal / 15 minutos antes. |
| b14 | 2:11.0–2:20.1 | DIA 3 · 4/11 | 1.2 | 18 minutos depois, a mesma linha de tempestades / gera outro tornado, em Xanxerê, / a uns 40 km dali. / Caminhões e ônibus tombam na rodovia. |
| b15 | 2:20.8–2:35.4 | DIA 3 · 4/11 | 1.2 | Na mesma manhã, do outro lado do rio Uruguai, / um tornado arrasa um eucaliptal inteiro em Erval Grande / e derruba uma torre de alta tensão em Barra do Rio Azul. / E à 1h30 da tarde, já no Planalto Norte, / é a vez de Rio Negrinho: / 82 casas atingidas. |
| b16 | 2:36.1–2:41.7 | DIA 3 · 4/11 | 1.2 | 4 tornados num único dia. / Nos temporais daquela quarta-feira, / 2 pessoas morreram em Santa Catarina. |
| b17 | 2:43.0–2:58.8 | DIA 6 · 7/11 | 1.2 | Sábado, 7 de novembro, de madrugada. / Uma única supercélula cruza o noroeste gaúcho. / À 1h18, Santo Augusto: / cerca de 50 casas destelhadas. / 36 minutos depois, a mesma tempestade / gera outro tornado, em Palmeira das Missões. |
| b18 | 3:00.2–3:09.5 | 7 EM 6 DIAS | 1.2 | 7 tornados confirmados pelas Defesas Civis, em 6 dias. / 3 no Rio Grande do Sul, 3 em Santa Catarina, 1 no Paraná. / 9 municípios atingidos. |
| b19 | 3:10.8–3:17.2 | É INÉDITO? | 1.2 | Agora, a pergunta que todo mundo fez. / Isso é inédito? / A resposta curta é: não. |
| b20 | 3:17.9–3:30.1 | É INÉDITO? | 1.2 | Em abril de 2015, um tornado atravessou Xanxerê, / a mesma cidade de agora, / e atingiu mais de 2 mil casas. / Em 2009, Guaraciaba, no extremo oeste catarinense, / teve um tornado F3, com 4 mortos. |
| b21 | 3:30.8–3:47.1 | É INÉDITO? | 1.2 | E há exatamente 1 ano, em 7 de novembro de 2025, / Rio Bonito do Iguaçu, no Paraná, / foi atingida por um F4. / Um rastro de 75 km, com até 3 km de largura. / 90% da área urbana atingida. / 7 mortes no estado. |
| b22 | 3:47.8–3:55.8 | É INÉDITO? | 1.2 | Os números também sobem. / Em 2025, o Brasil registrou 92 tornados, um recorde. / Até julho deste ano, já eram 81. |
| b23 | 3:56.5–4:17.9 | É INÉDITO? | 1.2 | Mas atenção: mais registros não significam, / necessariamente, mais tornados. / Hoje todo mundo tem uma câmera no bolso, / e desde 2018 uma plataforma reúne cada relato. / Um estudo de 2011 mostrou que os relatos de tornado no Brasil / se multiplicaram por 10 em 30 anos, / e boa parte disso é a gente vendo mais. / Entre os especialistas, não há consenso. |
| b24 | 4:18.6–4:34.8 | É INÉDITO? | 1.2 | O que não muda é o mapa. / A faixa entre o norte da Argentina, o Paraguai, o Uruguai e o Sul do Brasil / é considerada por pesquisadores / a 2ª região mais propícia a tornados do mundo, / depois dos Estados Unidos. / E satélites da NASA mostraram que as tempestades daqui / estão entre as mais intensas da Terra. |
| b25 | 4:36.1–4:38.5 | PERGUNTA 1/3 · POR QUÊ | 1.2 | Então, por que isso acontece justamente aqui? |
| b26 | 4:39.2–4:50.9 | PERGUNTA 1/3 · POR QUÊ | 1.2 | Comece pela Amazônia. / A floresta joga uma quantidade enorme de umidade no ar. / A uns 1.500 m de altitude, um vento forte, / o jato de baixos níveis, / carrega esse ar quente e úmido para o sul. |
| b27 | 4:51.6–5:04.4 | PERGUNTA 1/3 · POR QUÊ | 1.2 | No caminho, existe uma parede: / a Cordilheira dos Andes. / Ela barra o ar e o canaliza, colado à encosta, / direto para o Paraguai, o norte da Argentina e o Sul do Brasil. / É como um rio invisível de umidade. |
| b28 | 5:05.1–5:14.3 | PERGUNTA 1/3 · POR QUÊ | 1.2 | Do outro lado, chegam as frentes frias, / vindas da Argentina. / Quando o ar frio encontra esse ar quente e úmido, / o ar quente é empurrado para cima. / É o gatilho. |
| b29 | 5:15.0–5:32.7 | PERGUNTA 1/3 · POR QUÊ | 1.2 | Uma tempestade comum sobe e chove. / Mas aqui tem um ingrediente a mais: / o vento muda de direção e de força com a altura. / Perto do chão, sopra de um lado. / Lá em cima, mais forte, de outro. / E o ar entre as camadas começa a rolar, / deitado, como um rolo de massa. |
| b30 | 5:33.4–5:46.9 | PERGUNTA 1/3 · POR QUÊ | 1.2 | A corrente que sobe dentro da nuvem / levanta esse rolo e o põe em pé. / Agora, a tempestade inteira gira. / É a supercélula. / Esse giro, com alguns km de largura, / se chama mesociclone, e aparece no radar. |
| b31 | 5:47.6–5:56.2 | PERGUNTA 1/3 · POR QUÊ | 1.2 | Na traseira, uma descida de ar frio / se enrola em volta do giro. / Em parte dos casos, ele se estreita, / acelera e toca o chão. / É o tornado. |
| b32 | 5:56.9–6:10.4 | PERGUNTA 1/3 · POR QUÊ | 1.2 | E aqui vai uma coisa que pouca gente sabe: / a maioria das supercélulas não gera tornado. / E por que algumas geram e outras não, / o próprio laboratório de tempestades do governo americano admite: / a ciência ainda não entende totalmente. |
| b33 | 6:11.1–6:20.7 | PERGUNTA 1/3 · POR QUÊ | 1.2 | Umidade da Amazônia, a parede dos Andes, / frentes frias e vento que muda com a altura. / Poucos lugares do planeta juntam esses 4 ingredientes / como o Sul do Brasil. |
| b34 | 6:22.1–6:40.1 | EL NIÑO | 1.2 | E este ano tem um agravante. / O Pacífico equatorial está mais de 2 °C acima do normal. / É um El Niño muito forte, e ainda se fortalecendo. / A NOAA dá 83% de chance de ele se tornar / o mais forte desde 1950, / quando as medições começaram. |
| b35 | 6:40.8–6:49.5 | EL NIÑO | 1.2 | O El Niño deixa o jato de baixos níveis / mais frequente e mais forte. / Mais umidade chegando ao Sul. / Mais chuva. / Mais dias com os ingredientes juntos. |
| b36 | 6:50.2–7:12.0 | EL NIÑO | 1.2 | Mas cuidado com o que a ciência não diz. / O El Niño não causa cada tornado, / e não há estudo que ligue o El Niño, sozinho, ao número de tornados. / Ele aumenta as chances. / E o aquecimento global? / Ele deixa a atmosfera mais quente e úmida, / o que alimenta tempestades. / Mas, para tornados, o IPCC diz que os registros / ainda são curtos demais para afirmar uma tendência. |
| b37 | 7:13.4–7:19.6 | PERGUNTA 2/3 · RISCO | 1.2 | E a pergunta que todo mundo no Sul está fazendo: / isso vai voltar a acontecer? / Alto. / E não é exagero. |
| b38 | 7:20.3–7:32.6 | PERGUNTA 2/3 · RISCO | 1.2 | O pico do El Niño está previsto para a virada do ano, / entre dezembro e janeiro. / A previsão para novembro, dezembro e janeiro / é de chuva acima da média no Sul, / com destaque para o oeste catarinense. / E os solos já estão encharcados. |
| b39 | 7:33.3–7:42.4 | PERGUNTA 2/3 · RISCO | 1.2 | A temporada mais ativa de tornados / vai do fim do inverno à primavera. / Ou seja: estamos no meio dela. / E a MetSul alerta para eventos extremos / também no verão. |
| b40 | 7:43.1–7:57.1 | PERGUNTA 2/3 · RISCO | 1.2 | No mapa, as regiões mais expostas formam um arco: / o norte e o noroeste gaúcho, / o oeste de Santa Catarina / e o sudoeste do Paraná. / Mas este ano mostrou que o risco não para aí: / o norte do Paraná e os Campos Gerais também tiveram tornados. |
| b41 | 7:57.8–8:08.3 | PERGUNTA 2/3 · RISCO | 1.2 | Ninguém consegue prever onde cai o próximo tornado. / Mas dá para prever os dias de risco, / com 1 ou 2 dias de antecedência. / Já o alerta do tornado em si / chega com minutos. |
| b42 | 8:09.7–8:13.0 | PERGUNTA 3/3 · ATÉ ONDE | 1.2 | Agora, a pergunta mais difícil: / até onde isso pode chegar? |
| b43 | 8:13.7–8:31.9 | PERGUNTA 3/3 · ATÉ ONDE | 1.2 | Tornados são classificados pelo estrago, / numa escala de 0 a 5. / O Brasil usa a escala Fujita original. / Maringá foi um F2: até 253 km/h. / Um F4, como o de Rio Bonito do Iguaçu, / passa dos 330. / Um F5, dos 420. |
| b44 | 8:32.6–8:44.3 | PERGUNTA 3/3 · ATÉ ONDE | 1.2 | O Brasil nunca teve um F5 confirmado. / Mas a região já teve: / San Justo, na Argentina, em 1973, / a uns 300 km da fronteira gaúcha. / 63 mortos. |
| b45 | 8:45.0–8:57.6 | PERGUNTA 3/3 · ATÉ ONDE | 1.2 | Nos Estados Unidos, são cerca de 1.200 tornados por ano. / O mais largo já medido, em El Reno, / tinha 4,2 km de largura. / O de Rio Bonito do Iguaçu chegou a 3,2 km. |
| b46 | 8:58.3–9:13.8 | PERGUNTA 3/3 · ATÉ ONDE | 1.2 | O pior cenário não é um tornado maior. / É um tornado forte sobre uma cidade grande. / Um F3, ou F4, cruzando uma Chapecó, uma Maringá. / A região tem os ingredientes para isso. / Por isso, o que mais importa / é saber o que fazer. |
| b47 | 9:15.2–9:28.0 | O QUE FAZER | 1.2 | Primeiro: receba os alertas no celular. / Mande o seu CEP por SMS para 40199. / É de graça. / E, no Sul, o Defesa Civil Alerta / aparece direto na tela do celular, / com som, sem cadastro. |
| b48 | 9:28.7–9:38.8 | O QUE FAZER | 1.2 | Segundo: conheça os sinais. / Uma nuvem baixa e escura girando. / Uma nuvem em forma de funil. / Granizo grande. / Um ronco contínuo, como um trem chegando. |
| b49 | 9:39.5–9:54.7 | O QUE FAZER | 1.2 | Terceiro: se o alerta tocar, / vá para um cômodo pequeno no andar mais baixo, / sem janelas, como um banheiro, / e proteja a cabeça. / Longe de vidro, de galpões e de árvores. / Ao ar livre, deite numa vala. / E nunca se abrigue embaixo de um viaduto. |
| b50 | 9:56.1–10:14.6 | A RESPOSTA | 1.2 | Então, o que está acontecendo no Sul? / Não é um mistério, nem um castigo. / É o encontro da Amazônia com os Andes e com o frio do sul, / num dos cantos mais tempestuosos do planeta, / turbinado este ano por um El Niño muito forte. / Os tornados sempre estiveram aqui. / Agora, estamos vendo cada um deles. |
| b51 | 10:15.3–10:19.8 | A RESPOSTA | 1.2 | Manda este vídeo para quem mora no Sul. / E se inscreve: a temporada ainda não acabou. |
