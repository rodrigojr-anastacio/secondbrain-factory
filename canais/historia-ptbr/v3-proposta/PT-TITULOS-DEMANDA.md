# historia-ptbr v3: estruturas de título e demanda em pt-BR no nicho "como era viver" (coleta 28/11/2026)

Só pesquisa: nada foi mudado no canal, na bíblia nem no banco. Custo pago: US$ 0.

**Fontes e método (28/11/2026):**
- Busca do YouTube pelo `yt-dlp` via WARP (`ytsearch25`/`ytsearch20`/`ytsearch15`, `--js-runtimes node`): 42 termos em pt ("como era viver", "assim era a vida", "você não sobreviveria", "um dia na vida de", "brasil colonial como era", "rio de janeiro 1808", "bandeirantes como era", "tropeiros história", "ciclo do ouro minas gerais", "seringueiros", "cangaço como era", "como era ser criança em", "escravidão brasil como era" etc.), mais 25 termos pt de 2ª rodada, 22 de checagem (FEB, megafauna, Luzia, tigres, peste…) e 18 em en.
- Uploads dos últimos 12 meses (`playlistItems.list`) de 29 canais pt do nicho: Reconstrução Histórica, Reconstrução do Passado, Mundos Reimaginados, Nostalgia BRASIL, Memória Desbloqueada, Era Esquecida do Brasil, Crônicas de Ferro, Durma no Passado, Era Viking, Mistérios Medievais, fatos simples, História em Reconstrução, História do Amanhã, Vida Brasileira TV, O Reconstrutor, Viagem Pelo Tempo, Histories of Humanity, Antes da Cidade, Ruas de Outros Tempos, AntigamenteBR, Protagonistas da História, Rabisco da História, Por Quê, Hein?, Já Se Perguntou?, A Grande Saga, Kairus, Mundo sem Limite, Confluxo, E se você vivesse no passado?. O "Revelando Brasil" não apareceu em nenhuma busca nem tinha ID nos brutos; o vídeo dele (807.574 views) está em `relatorios/portfolio/2026-11-28-dados/historia-ptbr.md` §2.3.
- Views, data, duração, idioma e inscritos pela YouTube Data API (`videos.list`/`channels.list`, token readonly do historia-ptbr; zero `search.list`, ~250 unidades no total). 3.370 vídeos e 1.179 canais.
- Autocomplete do YouTube (`suggestqueries`, hl=pt, gl=BR, via WARP), 37 sementes. Nada gravado no banco; o `keywords.py` não foi rodado.
- **Corpus do nicho** (base das contagens): pt, publicado de 28/11/2025 a 28/11/2026, ≥ 5 min, título com marcador do formato ("como era", "assim era", "sobreviv", "um dia na vida", "instantes antes", "ANO:", "o que os … faziam" etc.), sem canais fora do nicho (filmes de terror, vlogs, aulas). **846 vídeos.**
- A coluna "visual" é **inferida** pelo título ("Reconstrução com IA") e pelo mosaico de 28 thumbs (`~/cache/tmp/v3pesq/mosaico.jpg` e `mos2.jpg`, temporários). "(massa)" = canal de reconstrução realista com IA em massa (≥ 150 vídeos em < 12 meses ou upload diário).
- Brutos e scripts: `~/cache/tmp/v3pesq/` (`vids.json`, `corpus.json`, `autocomplete.json`, `formulas.py`, `temas.py`). Temporários: não estão no git.

## 1. Top 42 do nicho em pt (12 meses, por views)
| # | título | canal (inscritos) | views | data | dur. | visual |
|---|---|---|---|---|---|---|
| 1 | [Como os Persas produziam gelo no deserto a 50°C sem eletricidade](https://youtu.be/1pPcmSTyZrU) | Rabisco da História (15,3 mil) | 2.514.766 | 2026-08 | 11 min | **cartoon** |
| 2 | [Assim era a Vida no Mundo ANTES DO DILÚVIO há 5.000 Anos / (DOCUMENTÁRIO)](https://youtu.be/P3dqkHxJ2go) | Histórias Épicas da Bíblia (292,0 mil) | 2.293.841 | 2025-12 | 24 min | IA realista |
| 3 | [Caraguatatuba Instantes Antes da Serra Engolir a Cidade (1967)](https://youtu.be/wsYvujpyi28) | AntigamenteBR (8,2 mil) | 2.105.573 | 2026-08 | 23 min | IA realista |
| 4 | [Como Era a Comida na Época da Bíblia — 2.000 Anos Atrás](https://youtu.be/C7W6Vc-K3Ig) | Vestígios Sagrados (50,8 mil) | 1.872.706 | 2026-02 | 62 min | IA realista |
| 5 | [Como Era Viver no Brasil Durante a Ditadura Militar (1964–1985) Rotina, Repressão e Segred](https://youtu.be/540WYF6EKJE) | Era Esquecida do Brasil (7,3 mil) | 1.274.877 | 2026-09 | 15 min | IA realista |
| 6 | [O Dia em que o Povo Venceu o Império (E o Preço Brutal que Pagou por Isso)](https://youtu.be/QTjecFwrzbs) | Mundos Reimaginados (109,0 mil) | 1.014.168 | 2026-04 | 17 min | IA realista |
| 7 | [Como Era a Vida no Brasil em 1975? Uma Viagem Nostálgica aos Anos 70](https://youtu.be/fpBXVH13P6k) | Memória Desbloqueada (24,3 mil) | 1.011.272 | 2026-10 | 26 min | IA realista |
| 8 | [Como Era a Vida em um Castelo Medieval no Ano de 1200 — Antes da Guerra Chegar aos Portões](https://youtu.be/2dqGsuQrxeM) | Reconstrução Histórica (massa) (71,2 mil) | 801.270 | 2026-04 | 23 min | IA realista |
| 9 | [1999: Como Era a Vida no Brasil Antes dos Anos 2000? / Nostalgia dos Anos 90](https://youtu.be/GYIbrSwlDT8) | Memória Desbloqueada (24,3 mil) | 797.094 | 2026-09 | 18 min | IA realista |
| 10 | [O Dia em que Portugal se Mudou para o Brasil](https://youtu.be/qWPL11MOzOg) | Mundos Reimaginados (109,0 mil) | 790.439 | 2026-03 | 16 min | IA realista |
| 11 | [O Que Maria COZINHAVA Para Jesus Todos Os Dias: Receitas Bíblicas Reveladas](https://youtu.be/TZmBBvx-zaw) | Reconstrução Histórica (massa) (71,2 mil) | 749.484 | 2026-03 | 21 min | IA realista |
| 12 | [22 de Abril de 1500 / O Dia em que o Brasil Mudou](https://youtu.be/2CIvklZRezE) | Mundos Reimaginados (109,0 mil) | 699.425 | 2026-02 | 9 min | IA realista |
| 13 | [Como Era Viver Dentro de uma Casa na Pompeia em 79 d.C. / Reconstrução com IA](https://youtu.be/n3RtYj3NgYM) | Reconstrução do Passado (massa) (70,2 mil) | 591.621 | 2026-03 | 19 min | IA realista |
| 14 | [Por Que Você Não Sobreviveria ao Banquete Real da Rainha Elizabeth I (1570)](https://youtu.be/fPgp14fkWpg) | Reconstrução Histórica (massa) (71,2 mil) | 590.720 | 2026-06 | 23 min | IA realista |
| 15 | [Como os Vikings Sobreviviam a -40°C no Subsolo (O Segredo das Casas de Turfa)](https://youtu.be/_xrAcsfZyE8) | Era Viking (6,2 mil) | 566.207 | 2026-04 | 12 min | IA realista |
| 16 | [Assim Era Sobreviver a Uma Noite numa Taverna Medieval / Por Que Você Imploraria por Comid](https://youtu.be/qQCi9Gmk0tg) | Reconstrução Histórica (massa) (71,2 mil) | 554.536 | 2026-06 | 26 min | IA realista |
| 17 | [Assim Era a Residência Oficial de JÚLIO CÉSAR Quando Governou Roma em 62 a.C / Reconstruçã](https://youtu.be/RgdVkCybFdw) | Reconstrução do Passado (massa) (70,2 mil) | 544.814 | 2026-03 | 18 min | IA realista |
| 18 | [Como Era a Vida no Brasil em 1989? O Último Ano dos Anos 80](https://youtu.be/i9cgGDmxXTo) | Memória do Brasil (15,5 mil) | 542.859 | 2026-06 | 21 min | IA realista |
| 19 | [1991: Como Era a Vida no Brasil no Começo de uma Nova Década?](https://youtu.be/ZmuBcmKtH38) | Memória Desbloqueada (24,3 mil) | 529.859 | 2026-10 | 32 min | IA realista |
| 20 | [Assim Era a Vida Dentro de uma Fazenda no Brasil Colonial em 1800 (Luxo, Poeira e Trabalho](https://youtu.be/V6Fa5Vr4VGs) | Reconstrução Histórica (massa) (71,2 mil) | 507.362 | 2026-05 | 22 min | IA realista |
| 21 | [Como os humanos antigos sobreviviam no calor extremo?](https://youtu.be/vAYnGJ5ohgc) | Por Quê, Hein? (23,7 mil) | 491.329 | 2026-11 | 31 min | **cartoon** |
| 22 | [Voltei ao ÊXODO e Descobri Como Era a HIGIENE no Deserto...](https://youtu.be/pDhB5EMcsqU) | Viagem Pelo Tempo (massa) (53,7 mil) | 488.370 | 2026-05 | 17 min | IA realista |
| 23 | [Londrina Instantes Antes da Geada Negra Devorar os Cafezais (1975)](https://youtu.be/NBR5XGW42Yk) | AntigamenteBR (8,2 mil) | 447.337 | 2026-09 | 25 min | IA realista |
| 24 | [Brasil em 1994: Como Era a Vida? Nostalgia dos Anos 90 Que Marcou Uma Geração](https://youtu.be/gH3UJCw33HE) | Memória Desbloqueada (24,3 mil) | 444.511 | 2026-08 | 13 min | IA realista |
| 25 | [Como Era Viver em São Paulo em 1900 - 1930? A História Que Ninguém Conta](https://youtu.be/jYPHuER926c) | Protagonistas da História (6,7 mil) | 438.497 | 2026-02 | 20 min | IA realista |
| 26 | [Como Era Viver em uma Casa Vitoriana na Inglaterra (1880)](https://youtu.be/y9HduOtAzz4) | Reconstrução Histórica (massa) (71,2 mil) | 437.200 | 2026-03 | 23 min | IA realista |
| 27 | [Assim foi o Surgimento da Primeira Favela do Brasil / Rio de Janeiro em 1897 (Reconstrução](https://youtu.be/I6E4QuAUAmM) | O Reconstrutor (12,5 mil) | 431.200 | 2026-05 | 13 min | IA realista |
| 28 | [Como Era Viver Dentro da Casa de Santos Dumont em Petrópolis em 1918 / Reconstrução com IA](https://youtu.be/5IvJ1vTAmRE) | Reconstrução do Passado (massa) (70,2 mil) | 410.348 | 2026-07 | 19 min | IA realista |
| 29 | [Assim foi a Vida de Dom Pedro II como Imperador do Brasil (1840–1889) / Reconstrução com I](https://youtu.be/CpkqjnaGOAc) | O Reconstrutor (12,5 mil) | 374.133 | 2026-05 | 20 min | IA realista |
| 30 | [Assim Era a Vida Dentro de uma Casa no Brasil Colonial em 1700 (Calor, Escravidão e Sobrev](https://youtu.be/47vEa_vsE4Y) | Reconstrução Histórica (massa) (71,2 mil) | 369.515 | 2026-05 | 26 min | IA realista |
| 31 | [A Verdade Oculta das 5 Tribos que Sobrevivem nas Florestas da Amazônia / Documentário Comp](https://youtu.be/EUcUThIjtRY) | CronaOrigem (37,6 mil) | 362.754 | 2026-03 | 37 min | ? |
| 32 | [Como os NEANDERTAIS Dormiam a -40°C Há 30.000 Anos SEM CONGELAR?](https://youtu.be/lomeAgzDZLg) | Reconstrução Histórica (massa) (71,2 mil) | 348.806 | 2026-06 | 19 min | IA realista |
| 33 | [O Método Mongol de Sobreviver à Estepe Congelada Sem Lenha — Explicado](https://youtu.be/QkLBFY8BIeY) | Era Viking (6,2 mil) | 338.104 | 2026-04 | 18 min | IA realista |
| 34 | [Como os humanos antigos sobreviveram sem água potável?](https://youtu.be/hpDKjjZ-xrI) | Rabisco da História (15,3 mil) | 335.393 | 2026-08 | 16 min | **cartoon** |
| 35 | [Como os Humanos Foram Parar no Brasil?](https://youtu.be/jQSmckO11C4) | Por Quê, Hein? (23,7 mil) | 335.209 | 2026-09 | 33 min | **cartoon** |
| 36 | [Assim Era a Vida Dentro de uma Caravela Rumo ao Brasil em 1500 / Mar, Tempestade e Medo](https://youtu.be/YKBqL9GUydg) | Reconstrução do Passado (massa) (70,2 mil) | 333.863 | 2026-06 | 17 min | IA realista |
| 37 | [COMO era SOBREVIVER ao INVERNO na IDADE MÉDIA (FRIO e MUITA DIFICULDADE) / Durma no Passad](https://youtu.be/pu4VOIeP6ys) | Durma no Passado (20,4 mil) | 333.416 | 2026-02 | 39 min | IA realista |
| 38 | [Óbidos Momentos Antes do Maior Naufrágio da História do Rio Amazonas (1981)](https://youtu.be/gaM7kTBzY1g) | Vida Brasileira TV (11,1 mil) | 327.571 | 2026-10 | 37 min | IA realista |
| 39 | [Instantes Antes do Incêndio do Edifício Joelma (1974)](https://youtu.be/Uokjnnsg3Vs) | AntigamenteBR (8,2 mil) | 326.708 | 2026-08 | 25 min | IA realista |
| 40 | [Alagoas Momentos Antes das Águas Destruírem Tudo (2010)](https://youtu.be/uRMTAJbXBgM) | Vida Brasileira TV (11,1 mil) | 323.222 | 2026-09 | 25 min | IA realista |
| 41 | [Como Era Realmente a Vida Dentro de um Castelo Medieval no Inverno Anos 1200](https://youtu.be/suV2TVrBOCg) | Avesso (1,6 mil) | 317.772 | 2026-11 | 34 min | IA realista |
| 42 | [Assim Era a Vida Dentro da Casa de Machado de Assis no Rio de Janeiro em 1890 / Reconstruç](https://youtu.be/uvf52_nbxPw) | Reconstrução do Passado (massa) (70,2 mil) | 303.783 | 2026-10 | 17 min | IA realista |

**Fora da janela, mas é a prova mais próxima do nosso formato:** [Sua vida como um soldado brasileiro na 2ª Guerra Mundial](https://youtu.be/Xt67z9COves), Confluxo (10,4 mil inscritos), **643.946** views, 08/2025, 8 min, **cartoon com seta "VOCÊ"** na thumb. Também: [O que os humanos faziam antigamente quando uma mulher engravidava?](https://youtu.be/f50q5FbqriE), Já Se Perguntou? (canal criado em 01/11/2026, 5,8 mil inscritos), 230.276 em 3 semanas, cartoon.

**Leitura do top 42:**
- 37 de 42 são **IA realista** (inferido) e 4 são cartoon (Rabisco da História, Por Quê, Hein?). Mas os cartoons estão no topo: o nº 1 do nicho no ano é um cartoon (Persas e o gelo, 2,5 mi, canal com 15 mil inscritos), e os canais cartoon têm a **maior mediana por vídeo** do levantamento (Já Se Perguntou? 134 mil; Por Quê, Hein? 69 mil; Rabisco 9,8 mil) contra 5–7 mil dos canais de IA em massa.
- Canais pequenos vencem: 8 dos 42 são de canais com < 10 mil inscritos (Era Viking, AntigamenteBR, Era Esquecida, Protagonistas, Avesso…). O algoritmo distribui por tema e embalagem, não por tamanho do canal.
- Três famílias dominam: **Brasil** (1500–1900 e nostalgia 1970–2000), **bíblico** e **medieval/antiguidade**. Bíblico está fora do nosso molde.
- Duração dos que bombam: mediana ~21 min. Os cartoons ficam em 11–33 min. 12–15 min está dentro do que funciona (Era Viking 12 min, 566 mil; fatos simples 6 min, 228 mil).

## 2. Fórmulas de título (corpus de 846 vídeos)
Mediana de views por fórmula; "sem massa" tira os 5 canais de IA em massa (Reconstrução do Passado, Reconstrução Histórica, Histories of Humanity, Viagem Pelo Tempo, Nostalgia BRASIL), que puxam a mediana para baixo com 150–190 uploads cada.

| fórmula | exemplo real (views) | n | mediana | mediana sem massa | % ≥ 100 mil |
|---|---|---|---|---|---|
| **F8 "CIDADE, ANO: cena concreta"** | "Porto Alegre, 1920: casas de porta e janela coladas nas fábricas" (143.991) | 17 | **24.423** | 24.423 | 11% |
| F10 "A Realidade Brutal / O Lado Nojento / A Verdade Sobre X" | "A Vida NOJENTA E MORTAL do Cowboy Real No Velho Oeste" (201.255) | 12 | 14.704 | 19.751 | 8% |
| **F5 "Como os X faziam Y (a −40 °C / sem Z)"** | "Como os Vikings Sobreviviam a −40°C no Subsolo" (566.207); "Como os Persas produziam gelo no deserto a 50°C sem eletricidade" (2,5 mi) | 32 | 12.630 | 9.190 | **21%** |
| F1 "Assim Era a Vida (Dentro) de X em ANO" | "Assim Era a Vida Dentro de uma Fazenda no Brasil Colonial em 1800" (507.362) | **205** | 7.877 | 8.050 | 15% |
| F3 "(Por Que) Você Não Sobreviveria a X" | "Por Que Você Não Sobreviveria ao Banquete Real da Rainha Elizabeth I (1570)" (590.720) | 43 | 7.175 | 9.635 | 9% |
| **F6 "Um Dia na Vida / O Último Dia / O Dia em que X"** | "O Dia em que Portugal se Mudou para o Brasil" (790.439); "O Último Dia de Serviço de um Soldado Romano" (227.769) | 24 | 7.164 | 8.955 | **20%** |
| **F9 "O Que os X (Realmente) Faziam/Comiam"** | "O Que os Índios no Brasil Antigo Realmente Faziam o Dia Todo?" (232.559) | 20 | 6.664 | 5.018 | **30%** |
| F7 "CIDADE Instantes Antes de DESASTRE (ANO)" | "Caraguatatuba Instantes Antes da Serra Engolir a Cidade (1967)" (2,1 mi) | 45 | 4.575 | 4.575 | 20% |
| F2 "Como Era (a Vida / Viver / Ser) X (em ANO)" | "Como Era Viver no Brasil Durante a Ditadura Militar (1964–1985)" (1,27 mi) | **319** | 3.150 | 1.406 | 12% |
| F4 "ANO: Sem X, Sem Y – Z" | "1315: Sem Água Potável, Sem Geladeira – Comer na Idade Média" (195.917) | 22 | 2.913 | 2.913 | 9% |
| 2ª pessoa direta ("Sua vida como…", "Você era…") | Confluxo 643.946 (cartoon); Vida Brasileira TV "Por que você não sobreviveria 1 mês como tropeiro no Brasil de 1820" 130.414 | ~6 | — | — | (poucos casos) |

**O que os números dizem:**
1. **"Como Era…" e "Assim Era…" são a manada**: 524 dos 846 títulos (62%). A mediana é baixa (3–8 mil) porque todo canal de IA usa isso. A fórmula sozinha não vende; o que vende é o tema e a cena.
2. **Rendem mais as fórmulas com um objeto físico, um número ou uma cena** (F5 com "−40 °C"/"50 °C sem eletricidade", F9 "o que faziam o dia todo", F6 "o dia em que…"): 20–30% passam de 100 mil, contra 12–15% de "Como Era/Assim Era". É a lição do Dossier: nome ou fato concreto e cena física.
3. **"Você Não Sobreviveria" em pt é, sobretudo, de filmes de terror** (Derrotando Filmes, 1,77 mi de inscritos, domina o autocomplete: "backrooms", "silent hill"). Em história, rende em temas de luxo/nojo (banquete da Elizabeth 590 mil, taverna 555 mil, farol 251 mil) e cai fácil (mediana 7 mil). Para nós: usar a 2ª pessoa de forma **afirmativa e concreta** ("Você Embarcou…", "Você Foi Alistado…"), não em pergunta nem como desafio genérico.
4. **"ANO: Sem X, Sem Y" (Mistérios Medievais) não decolou em pt** (mediana 2,9 mil).
5. **Pergunta no título funciona quando é prática e física** (F5/F9 dos canais cartoon: "Como os humanos antigos sobreviviam no calor extremo?" 491 mil). Isso é diferente da pergunta-paradoxo que derrubou o v2 ("Por que o Egito…?"). Regra proposta: pergunta só se a resposta for uma técnica ou uma cena ("como dormiam a −40 °C"), nunca um "por quê" abstrato.

## 3. Termos demandados (autocomplete, 28/11/2026)
- **como era viver** → como era viver na idade media; como era viver na ditadura militar no brasil; como era viver nos anos 2000; como era viver na união soviética; como era viver nos anos 80; como era viver nos anos 90; como era viver; como era viver na grecia antiga; como era viver em um castelo medieval; como era viver no velho oeste
- **como era a vida no brasil** → como era a vida no brasil em 1975; como era a vida no brasil em 1800; como era a vida no brasil colonial; como era a vida no brasil em 1989; como era a vida no brasil em 1900; como era a vida no brasil nos anos 60; como era a vida no brasil; como era a vida no brasil em 1971; como era a vida no brasil em 1980; como era a vida dos escravos no brasil
- **como era a vida de um** → como era a vida de um faraó; como era a vida de um cavaleiro medieval; como era a vida de um escravo; como era a vida de um samurai; como era a vida de um campones na idade media; como era a vida de um rei na idade media; como era a vida de um pirata; como era a vida de um gladiador; como era a vida de um pastor de ovelhas em israel; como era a vida de uma criança na revolução industrial
- **como era a vida dos** → como era a vida dos escravos; como era a vida dos dinossauros; como era a vida dos vikings; como era a vida dos escravos no brasil; como era a vida dos escravos na senzala; como era a vida dos piratas; como era a vida dos homens das cavernas; como era a vida dos primeiros seres humanos; como era a vida dos escravos antigamente; como era a vida dos faraós
- **como era ser** → como era ser criança nos anos 2000; como era ser gay em cada epoca; como era ser crianca ha 50 anos; como era ser criança nos anos 90; como era ser adolescente nos anos 2000; como era ser um pirata; como era ser criança nos anos 80; como era ser um viking; como era ser criança nos anos 90 no brasil; como era ser um soldado na segunda guerra mundial
- **assim era a vida** → assim era a vida no mundo antes do diluvio; assim era a vida; assim era a vida dentro de uma caravela; assim era a vida dentro de uma casa de imigrantes italianos no brasil em 1875; assim era a vida da princesa isabel; assim era a vida dentro de uma senzala no brasil colonial em 1760; assim era a vida de henrique viii; assim era a vida em um castelo medieval; assim era a vida dentro de uma fazenda; assim era a vida no templo de salomão
- **você não sobreviveria** → você não sobreviveria; você não sobreviveria um dia na idade média; você não sobreviveria filme; você não sobreviveria um dia em the walking dead; você não sobreviveria um dia; você não sobreviveria backrooms; porque você não sobreviveria; porque voce nao sobreviveria em guerra mundial z; porque você não sobreviveria derrotando filmes; porque você não sobreviveria na idade media
- **como era a higiene** → como era a higiene na idade média; como era a higiene na epoca de jesus; como era a higiene no egito antigo; como era a higiene antigamente; como era a higiene na era vitoriana; como era a vida e a higiene dos navegadores portugueses nas grandes navegações; voltei ao êxodo e descobri como era a higiene no deserto; como era la higiene en el antiguo egipto; como era la higiene en la edad media; como era la higiene en el viejo oeste
- **como era a comida** → como era a comida na idade media; como era a comida dos escravos; como era a comida no tempo de jesus; como era a comida; como eram as comidas de antigamente; como era la comida en la edad media; como era la comida en la segunda guerra mundial; como era la comida medieval
- **como era ser escravo** → como era ser escravo no brasil; como era ser escravo; como era ser escravo em roma; como era vida dos escravos; como viviam os escravos; como viviam os escravos no brasil
- **como funcionava** → como funcionava um engenho de açúcar; como funciona; como funcionavam os pombos correios; como funciona o desenrola brasil; como funcionavam os aquedutos romanos; como funcionava o feudalismo; como funcionava o telex; como funcionava a blitzkrieg; como funciona o consórcio; como funciona a starlink
- **piores trabalhos** → piores trabalhos do mundo; piores trabalhos; piores trabalhos no brasil; os piores trabalhos da idade media; fala serio piores trabalhos; top 3 piores trabalhos
- **como era a vida em 1** → como era a vida em 1970; como era a vida em 1800; como era a vida em 1900; como era a vida em 1980; como era a vida em 1700; como era a vida em 1500; como era a vida em 1990; como era a vida em 1920; como era a vida em 1994; como era a vida em 1950
- **Sem sugestão nenhuma** (demanda de busca baixa): "como era tomar banho", "como era o dentista", "como era o rio de janeiro". "bandeirantes", "tropeiros", "cangaço", "caravela" e "1808" devolvem rádio/TV, música, filme ou livro (Laurentino Gomes), não "como era": esses temas vivem de **sugerido/navegação**, não de busca.

Leitura: a busca pede **profissões/papéis** ("a vida de um faraó / cavaleiro / samurai / camponês / pirata / gladiador / soldado romano", "ser um viking", "soldado na segunda guerra" e, no Brasil, "soldado brasileiro na segunda guerra"), **anos redondos** ("em 1800", "em 1900", "em 1500", "em 1700") e **Brasil** ("brasil colonial", "brasil em 1800", "escravos no brasil", "ditadura militar no brasil", nostalgia 70–2000). Higiene e comida aparecem em todas as épocas.

## 4. Portas abertas × manada (contagem no corpus de 12 meses)
| tema | vídeos pt 12 m | mediana | melhor (views) | leitura |
|---|---|---|---|---|
| **Brasil colonial/império 1500–1900** (todas as cidades e ciclos) | 241 (68 canais) | 3.226 | Fazenda colonial 507 mil; Portugal se muda 790 mil | Muito vídeo de IA, mas espalhado: cada **recorte** tem poucos vídeos (abaixo) |
| Caravela / viagem de 1500 | 20 | 1.887 | Caravela rumo ao Brasil 333.863 | **PORTA**: 1 hit de IA; ninguém em 2ª pessoa; autocomplete "assim era a vida dentro de uma caravela", "higiene dos navegadores portugueses" |
| Rio 1808 / chegada da corte | 36 | 2.083 | Portugal se muda 790.439; Nostalgia 290 mil | **PORTA**: demanda provada; todos são tour de palácio com IA; ninguém conta pelo carioca despejado ("PR") |
| Tropeiros | 9 | 2.705 | "Você não sobreviveria 1 mês como tropeiro" 130.414 (canal de 11 mil) | **PORTA**: 1 hit, nenhum concorrente forte |
| Ouro de Minas 1700–1750 | 26 | 765 | Ouro Preto 77 mil | **PORTA de busca escolar** ("ciclo do ouro") sem vídeo bom de cotidiano |
| Seringueiros / borracha | 13 | 1.393 | Manaus 1910 87 mil | Porta média: Amazônia bomba (Kairus 3,1 mi), borracha ainda não |
| Cangaço / sertão | 5 | 1.691 | "O único registro de Lampião vivo" 1,28 mi (canal de 2,8 mil, 11/2026) | **PORTA + urgência**: interesse por Lampião em alta; o cotidiano do sertão ninguém fez bem |
| Imigrantes (italianos, alemães, japoneses) | 23 | 1.150 | Casa de imigrantes italianos 1875: 283.964 | Porta média: 1 canal de IA faz tudo |
| FEB / pracinha 1944 | (busca própria) | — | Confluxo 643.946 (cartoon 2ª pessoa); Monte Castelo 260 mil (11/2026); 423 mil (11/2025) | **PORTA**: o vídeo mais parecido com o nosso formato já provou; autocomplete pede |
| Pré-história do Brasil (megafauna, Luzia) | ~6 | — | "Como os Humanos Foram Parar no Brasil?" 335 mil (cartoon); Luzia 157 mil (11/2026) | **PORTA**: em en é o maior formato do ano (13,6 mi); em pt quase vazio |
| Piores empregos (história / Brasil) | ~5 | — | en 1,6 mi; Fala Sério Roma 260 mil; "Tigres" (Brasil) só 1 vídeo de 20 views | **PORTA** no recorte Brasil colonial |
| Escravidão (cotidiano) | 42 | 4.972 | depoimentos 1,1 mi / 607 mil; 1888 385 mil | Demanda alta, tema sensível: só com cuidado, nunca como humor |
| Nostalgia Brasil 1970–2000 | 95 | 7.583 | 1975: 1,01 mi; 1999: 797 mil | Demanda enorme, mas é outro público e outro molde (fotos/IA, sem história antiga) |
| **Castelo medieval / inverno medieval** | 108 (medieval) | 5.657 | 801 mil, 554 mil, 333 mil, 318 mil… | **MANADA**: 6+ versões quase iguais em 2026 ("Como Era a Vida em um Castelo Medieval no Ano de 1200" ×3 canais) |
| **Higiene medieval / banho** | ~15 | — | Crônicas de Ferro 209 mil | **MANADA** (e o autocomplete de "tomar banho" é vazio) |
| **Bíblico** (Jesus, dilúvio) | 17 | 12.899 | 2,3 mi; 1,9 mi | Demanda alta, fora do molde e da política do canal |
| **"Instantes antes" (desastres BR)** | 45 (2 canais) | 4.575 | Caraguatatuba 2,1 mi | Fórmula nova e forte, mas é tragédia (choca com a política "sem morte"); não é para nós |
| Vikings / frio extremo | 38 | 6.754 | Era Viking 566 mil | Semimanada: "como sobreviviam a −40 °C" já foi feito; a convivência e o dia a dia ainda não |
| Roma (soldado, cotidiano 117 d.C.) | 90 (antiguidade) | 5.202 | Pompeia 592 mil; soldado romano cartoon 228 mil | Semimanada: "117 d.C." de IA repetido; a 2ª pessoa com humor está livre |

**Três portas mais abertas:** (1) **Brasil colonial pelos olhos de gente comum, com recorte físico** (caravela de 1500, carioca despejado em 1808, tropeiro, ouro de Minas): demanda provada por 1–2 hits de IA, nenhum em 2ª pessoa com humor; (2) **Brasil no século XX em situação extrema** (pracinha na neve em 1944, sertão de Lampião em 1930): a prova mais próxima do nosso formato (Confluxo, 644 mil, cartoon "VOCÊ") está aqui; (3) **pré-história do Brasil** (megafauna, primeiros humanos): em en é o formato do ano; em pt só 1 cartoon (335 mil) e documentários.

## 5. Canais grandes de "reconstrução IA realista em massa"
| canal | inscritos | criado | uploads em 12 m | mediana/vídeo | observação |
|---|---|---|---|---|---|
| Reconstrução Histórica | 71,2 mil | 2021 (virou IA em 2026) | 166 | 6.935 | "Assim Era / Como Era / Por Que Você Não Sobreviveria" em tudo; Brasil colonial e medieval |
| Reconstrução do Passado | 70,2 mil | 03/2026 | 163 | 5.221 | "Assim era a Vida Dentro de X em ANO / Reconstrução com IA"; já fez caravela, engenho, imigrantes, Lampião, 1808 |
| Histories of Humanity | 14,3 mil | 03/2026 | 191 | 2.369 | navios e engenharia |
| Viagem Pelo Tempo | 53,7 mil | 02/2026 | 157 | 8.347 | "Voltei no tempo…" (vlog IA, bíblico) |
| Nostalgia BRASIL | 21,4 mil | 01/2026 | 114 | 2.456 | Brasil 1808–1926 "(Reconstrução com IA)" |
| Mundos Reimaginados | 109 mil | 01/2026 | 48 | **87.097** | IA cinematográfica, Brasil (1500, 1808, Farrapos, Tiradentes): o melhor do nicho; poucos vídeos, mais cuidado |
| Memória Desbloqueada / Memória do Brasil | 24,3 / 15,5 mil | 07/2026 / 2021 | 17 / — | 24.938 | nostalgia anos 70–2000 |
| E se você vivesse no passado? | 248 | 04/2026 | 88 | < 1 mil | 2ª pessoa no nome, mas IA realista; não decolou |

**Canais cartoon/rabisco (o nosso visual), todos pequenos e com mediana alta:** Por Quê, Hein? (23,7 mil inscritos, mediana 69 mil), Já Se Perguntou? (5,8 mil, 134 mil, canal de novembro), Rabisco da História (15,3 mil, 9,8 mil; hit de 2,5 mi), fatos simples (1,4 mil; 228 mil), Confluxo (10,4 mil; 644 mil). Fazem "humanos antigos" e sobrevivência; **nenhum faz Brasil colonial/império com bonequinho em 2ª pessoa**. É a nossa posição.

## 6. Consequências para o título do historia-ptbr v3
- Molde recomendado: **"Lugar, ANO: Você [verbo concreto] + objeto/número"** ou **"Você [virou/embarcou/foi alistado] … ANO: [número físico]"** (ex.: "Rio, 1808: Pintaram 'PR' na Sua Porta", "Você Embarcou na Caravela de Cabral: 44 Dias Até o Brasil"). Junta a F8 (melhor mediana), a 2ª pessoa (diferencial e prova do Confluxo) e o fato concreto (lição do Dossier).
- Evitar: "Como Era a Vida em…" puro (manada, mediana 3 mil), "Por que…?" abstrato, "Sem X, Sem Y", "Você Não Sobreviveria" genérico (é de filme de terror em pt). Sem morte/morreu/massacre/chocante (política do canal).
- Thumb: bonequinho + seta/rótulo "VOCÊ" ou situação física + 2–3 palavras (Confluxo, Rabisco, Já Se Perguntou?): quase todo o top em IA realista usa ANO grande + cena; o cartoon se destaca no meio deles.
