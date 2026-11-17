# Em Relevo: 3 candidatos a próximo vídeo, com evidência (17/11/2026)

Brief: `~/workspace/referencias/BRIEF-em-relevo-proximos-3.md`. Escopo: planeta Terra ligado ao Brasil, sem espaço. Dados coletados em 17/11/2026 pelo yt-dlp via WARP, com Data API (`videos.list`/`channels.list`/`playlistItems`, ~1,1 mil unidades e sem `search.list`), autocomplete do YouTube e RSS do Google Notícias. Custo US$ 0.

## Resumo (10 linhas)
1. **Varredura:** 28 temas e 82 buscas (`temas.tsv`, `scan/`). Também li os últimos 50 envios de 13 canais pt-BR de "geografia no mapa" (`canais-mapa/canais.json`). Os 5 temas mais fortes viraram uma ficha cada (`candidatos/*/FICHA.md`).
2. **#1 Atafona: "não foi o mar que subiu" (nota 8,1).** É o tema de demanda mais repetida: 7 canais com menos de 35 mil inscritos passaram de 5× a mediana, e 9 vídeos têm ≥ 100 mil views em 90 dias. Tem ~50 notícias em 90 dias e o melhor material livre (Landsat 1985→2025).
3. **#2 "O Brasil treme": Caruaru e o mapa dos 1.815 tremores (nota 7,7).** A notícia está quente agora: 10 tremores em ~35 h entre 15 e 17/11, e nenhum canal de mapa cobriu. É perecível: só vale com publicação até ~24/11. Depois disso, vira o evergreen "1.815 tremores".
4. **#3 Poços de Caldas: a cidade dentro de um vulcão de 33 km (nota 7,7).** A caldeira aparece no SRTM (conferido). As terras raras estão no noticiário (58 notícias em 90 dias). Puxa demanda, mas há só 1 vídeo do tema acima de 100 mil em 90 dias.
5. **Eu faria primeiro Atafona.** Tem a evidência mais larga e repetida, o melhor material real e o ângulo que só o mapa 3D mostra: o rio desce da serra, passa pelas barragens e chega à foz que perde areia. Exceção: se for para produzir até ~24/11, Caruaru passa à frente pela janela.
6. **Descartado: "cidades engolidas por represas" (6,3).** A demanda é alta, mas há 30 vídeos em 90 dias (18 com menos de 1 mil views) e as repetições recentes já caem a 0,4–2×. Também não há ruína reaparecendo agora, e o SRTM não "esvazia" o lago.
7. **Descartado: "o que existe debaixo de [lugar]" genérico.** A onda passou do pico: 54 vídeos em 2 semanas, 30 com menos de 2 mil views. O próprio Além do Mapa caiu de 1.751 para 30–100 views/h. Só sobrevive amarrado a um evento (por isso virou o #2).
8. **Backlog atual:** devem sair Granizo (cancelado; a demanda é de vídeo de celular e de TV), Neve (fora da estação), Cânions (turismo, 0,4–1,5×; o ângulo geológico foi feito pelo Sob o Mapa com 685 mil) e Calor do Super El Niño (canais gigantes; já fizemos o 002). Ficam parados Litoral do RS (402 mil e 20× no Explica no Mapa em 01/11, recém-feito) e Geada negra (guardar para jun–jul).
9. **Padrão que vale para os 3:** todos os concorrentes usam desastre de IA e tarja "URGENTE/SEGREDO". Nossa thumb ganha contraste com **relevo/satélite real escuro + 1 marca vermelha + 2–3 palavras**, prometendo uma virada ("NÃO FOI O MAR", "JÁ TREMEU 1.815×", "DENTRO DELE").
10. **Material:** os 3 passam de 40% da tela em material real + mapa 3D (estimativas de 55–70%). O ponto fraco comum é não haver **vídeo** livre do evento. O nível (b), acervo com crédito, só reforça; nenhum dos 3 depende dele.

---

## Ranking
| # | Candidato | Demanda | Momento | Material | Encaixe | Nota (média geom.) | Risco principal |
|---|---|---|---|---|---|---|---|
| 1 | **Atafona: o mar engole, o rio é o culpado** | 9 | 7 | 8 | 9 | **8,1** | manada de clones "o mar engoliu X de R$ N mi"; a causa "barragem" precisa de 2 fontes revisadas por pares |
| 2 | **O Brasil treme: Caruaru + catálogo de 1.815 sismos** | 8 | 9 (perecível) | 7 | 8 | **7,7** | chegar tarde (a notícia esfria em 1–2 semanas); disputar com rosto + "ALERTA" |
| 3 | **Poços de Caldas: vulcão de 33 km com cidade dentro** | 7 | 7 | 8 | 9 | **7,7** | colisão com o Arquivo Mineiro (abr/2026, mesma promessa); só 1 vídeo do tema > 100 mil em 90 d |
| — | Cidades engolidas por represas (descartado) | 8 | 4 | 7 | 7 | 6,3 | saturação, repetições caindo, momento só em 2027 |
| — | "Debaixo de [lugar]" genérico (descartado) | 8 → caindo | 3 | 7 | 9 | ~6 | onda passou do pico em 2 semanas |

### 1. Atafona/RJ: "não foi o mar que subiu, foi o rio que parou de mandar areia"
Ficha: `candidatos/mar-engolindo/FICHA.md` · mosaico: `candidatos/mar-engolindo/mosaico.jpg`
- **Demanda (12 meses, ★ = 90 d):**
  - ★ [youtu.be/Or4kQ6-R4gQ](https://youtu.be/Or4kQ6-R4gQ): 509 mil, **337×** (Luxo em Ruínas, 4,3 mil insc., 09/10)
  - [youtu.be/NNotrt5Cl4g](https://youtu.be/NNotrt5Cl4g): 398 mil, **523×** (Vozes do Mundo, 8,2 mil, 23/08)
  - ★ [youtu.be/3VCVLBXe56w](https://youtu.be/3VCVLBXe56w): 485 mil, 17,9× (Vilas Caídas, Praia do Saco, 05/11)
  - Mais: Santos em Movimento 198 mil (36×), Zona de Risco 167 mil (11×), Morro de SP 125 mil (83×), Balneário Camboriú 119 mil (8,9×, 11/11) e TV Record Atafona 150 mil (162×).
  - **Critério ≥ 3 canais pequenos com ≥ 5×: passa (7 canais).**
- **Autocomplete:** "atafona antes e depois", "atafona hoje", "avanço do mar no brasil / em atafona / na praia do saco".
- **Momento (Google Notícias, 90 d):** cerca de 50–57 itens por termo. Manchetes:
  - G1, 07/10: estudo de R$ 5,6 mi para Atafona, que já perdeu 500 casas.
  - G1, 26/09: casa desaba na Praia do Saco.
  - Agência Brasil, 11/11: soluções naturais na proteção costeira.
  - Também pesam a COP31 e as ressacas da primavera.
- **Manada:** lista de lugares com cena de destruição, culpa da "ganância" e do aquecimento, número do MapBiomas (−15% de areia de 1985 a 2021). Barragem e sedimento aparecem só de passagem.
- **Ângulo nosso:** o mar global sobe milímetros por ano, e Atafona recua de 3 a 8 m por ano. O mapa 3D desce o Paraíba do Sul da serra até a foz, passando pelas barragens e pela elevatória de Santa Cecília (até ~180 m³/s para o Guandu, a água do Rio). Fecha com o Landsat de 1985 a 2025: Atafona perde e Grussaí, ao lado, ganha. O Cabeço/SE, no São Francisco depois de Xingó, entra como 2ª prova.
- **Títulos:**
  - (T1) "Atafona: o Mar Engoliu 500 Casas — Mas o Culpado Está a 300 km Daqui". Lugar + número + virada, no molde de Or4kQ6/Ftwbkf. Os 300 km são a conferir na etapa 1.
  - (T2) "Não É o Mar Subindo: Por Que as Praias do Brasil Estão Sumindo". Mito corrigido + "por que"; modela NNotrt5Cl4g e o padrão "por que" do OMTR.
- **Thumb:** satélite real da foz, linha vermelha tracejada "1985" dentro do mar, seta subindo o rio até a barragem e "NÃO FOI O MAR".
- **Material:**
  - (a) Landsat e Sentinel-2 (domínio público); Google Earth Timelapse (CC BY 4.0, crédito obrigatório); SRTM; ~5 fotos úteis no Commons; Agência Brasil (conferir o crédito foto a foto).
  - (b) Fotos de jornal e de teses.
  - (c) TV, drone de youtuber e o vídeo viral do desabamento.
  - **Estimativa: ~55% da tela real.**

### 2. "O Brasil treme": Caruaru agora + o mapa de 1.815 tremores
Fichas: `candidatos/terremotos/FICHA.md` e `candidatos/subsolo/FICHA.md` (as duas chegaram sozinhas a Caruaru) · mosaicos nas duas pastas.
- **Demanda:**
  - [youtu.be/tC8_Jdfq2dk](https://youtu.be/tC8_Jdfq2dk): 868 mil, 598× (Cosmos Oculto/Sacani, 26 mil insc., 13/08; é podcast de 1h31)
  - [youtu.be/9TYVJYxajyg](https://youtu.be/9TYVJYxajyg): 563 mil, **386×** (Rotas do Brasil Oculto, 3,4 mil, Serra do Mar "falha ativa", 29/08)
  - ★ [youtu.be/1WJv7DjUtuo](https://youtu.be/1WJv7DjUtuo): 557 mil, **192×** (Além do Mapa, 6,2 mil, Nordeste: tremores e a cicatriz da crosta, 04/11)
  - Mais: Rogerdautry "Terremotos no RJ" 331 mil (19,6×); Barretos/estrondos 89,6 mil em 3 dias (5,3×); Atlas das Curiosidades 14 mil (28×).
  - **Critério: passa (5 canais).**
- **Momento:**
  - Enxame de Caruaru-PE entre 15 e 17/11: 10 tremores em ~35 h, o maior M2,8 (G1, Diario de PE, Folha PE, conferido em 17/11).
  - "tremor de terra em caruaru" já é a 1ª sugestão do autocomplete para "tremor de terra".
  - Até agora só há TV no YouTube (67 mil e 44 mil) e um explicador de 7,7 mil.
- **Ângulo nosso:** os 1.815 sismos do catálogo da rede sismográfica brasileira (USP, desde 1720; a consulta foi testada e responde) acendendo sobre o relevo real, agrupados nas cicatrizes da crosta: lineamento Pernambuco, João Câmara 1986, Serra do Tombador-MT M6,3 em 1955, Itacarambi 2007 (a única morte). Ninguém da manada mostra o catálogo inteiro sobre o relevo.
- **Títulos:**
  - (T1) "Caruaru Tremeu 10 Vezes em 35 Horas: o Que Existe Debaixo de Pernambuco". Evento + "debaixo de"; modela 1WJv7DjUtuo e Barretos. Só vale até ~24/11.
  - (T2, evergreen) "O Brasil Já Tremeu 1.815 Vezes, e o Mapa Mostra Onde Vai Tremer de Novo". Número que contradiz a crença; modela o Atlas (28×).
- **Thumb:** bloco 3D real da Borborema cortado, rachadura vermelha sob o pino "CARUARU" e "10 TREMORES" (ou "JÁ TREMEU 1.815×").
- **Material:**
  - (a) Catálogo da USP e do USGS, relevo, falhas do SGB, 1 foto de João Câmara 1986 no Commons (domínio público), Agência Brasil (Maricá 2026, Caruaru 2020).
  - (b) Fotos de 2026 de prefeitura, governo de PE e UFRN.
  - (c) TV.
  - **Estimativa: ~60–70% da tela**, mas a parte de foto é fina (quase tudo é mapa).
- **Antes de decidir:** um teste de custo zero, plotar o catálogo num still para ver se as faixas aparecem nítidas sobre o relevo. Também falta confirmar que o enxame tem a ver com o lineamento Pernambuco; sem isso, o título vira "por que o Agreste treme".

### 3. Poços de Caldas: o vulcão de 33 km que tem uma cidade dentro
Ficha: `candidatos/vulcoes/FICHA.md` · mosaico e hillshade SRTM conferido (`srtm-pocos-de-caldas-hillshade.png`).
- **Demanda:**
  - [youtu.be/ECToWsT_cZc](https://youtu.be/ECToWsT_cZc): 424 mil, **474×** (Curioso em 5 Minutos, 685 insc., "O vulcão mais antigo do mundo fica no Brasil", 04/09)
  - [youtu.be/XHyerrpzfrE](https://youtu.be/XHyerrpzfrE): 43 mil, **82×** (Arquivo Mineiro, Poços de Caldas + terras raras, abr/2026)
  - ★ [youtu.be/SxHTP3CRvOU](https://youtu.be/SxHTP3CRvOU): 74,5 mil, 23× (Segredos do Mapa, Noronha, há 15 dias)
  - Mais: Mundo SC Corupá 45 mil (20×).
  - **Critério: passa (5 canais)**, mas só 1 vídeo > 100 mil em 90 d.
  - O genérico "por que o Brasil não tem vulcões" teve 6 vídeos em 2 semanas, com 4 a 3 mil views: não serve.
- **Momento:**
  - Lynas comprou um projeto de terras raras em MG por R$ 3,5 bi (01/10).
  - Agência Brasil: "segunda maior reserva do mundo" (04/11).
  - CNN: a "cratera de 35 km" (06/11).
  - Autocomplete: "vulcão em minas gerais", "vulcão poços de caldas".
- **Ângulo nosso:** os concorrentes vendem lava de IA. Nós mostramos o anel no relevo real: planalto de dentro a ~1.300 m, terreno de fora a 870–1.000 m, cristas a ~1.800 m (SRTM conferido). A erosão deixou o anel de pé, e 80 milhões de anos de chuva concentraram as terras raras na argila.
- **Títulos:**
  - (T1) "O Maior Vulcão do Brasil Dá Para Ver do Espaço (e Tem uma Cidade Dentro)". Superlativo + parêntese de virada, padrão do OMTR.
  - (T2) "Uma Cidade Inteira Dentro de um Vulcão de 33 km, e o Que Ele Deixou no Chão". Número concreto, no molde do XHyerrpzfrE.
  - Evitar "construída dentro de um vulcão" (1,8× no Atlas) e o "20% das terras raras do mundo" sem fonte.
- **Thumb:** relevo real do anel, escuro, só a borda acesa em laranja, pino "VOCÊ ESTÁ AQUI" e "DENTRO DELE" em amarelo.
- **Material:**
  - (a) SRTM, Landsat/Sentinel, 227 arquivos de Poços no Commons (mais 470 de Noronha e 109 de Trindade), Agência Brasil.
  - (b) Prefeitura e mineradoras.
  - **Estimativa: ~55–65% da tela.**

## Descartados (pareciam bons; os dados derrubaram)
- **Cidades engolidas por represas** (`candidatos/cidades-submersas/FICHA.md`, 6,3).
  - A favor: 304 mil (1.321×), Sobradinho 199 mil (65×), Canudos 120 mil (39×).
  - Contra:
    - 30 vídeos em 90 d, 18 deles com menos de 1 mil views.
    - Os mais recentes do Brasil de Outrora já caem (Itá 0,4×, Jaguaribara 2×).
    - Sobradinho está a ~60%, sem ruína aparecendo.
    - O SRTM vê o lago como superfície plana.
  - Guardar para a seca de 2027, se o nível baixar.
- **"O que existe debaixo de [lugar]" genérico** (`candidatos/subsolo/FICHA.md`).
  - A favor: Sob o Mapa 685 mil (Sul/deserto Botucatu), Além do Mapa 557/443/383 mil, tudo entre 20/10 e 07/11.
  - Contra:
    - Em 2 semanas, 54 vídeos de 27 canais, 30 com menos de 2 mil views.
    - As repetições do próprio Além do Mapa (Minas, Alter do Chão, São Paulo) fazem 30–100 views/h, contra 1.751 do hit.
    - Serra do Mar, Bahia e Campos do Jordão ficaram em 0,1–0,5×.
    - O autocomplete é fraco: a onda vive de recomendação, não de busca.
  - Só funciona com evento (vira o #2).
- **Também visto na varredura e não aprofundado:**
  - Maceió/Braskem: 1,04 mi no Vilas Caídas em 04/11 e 332 mil no Igor Pinheiro, com 4+ repetições em out–nov. Saturado agora.
  - "Secar o Atlântico / Brasil à África a pé": 573 mil e 248× no O Mapa Não Mente em 09/11. Recém-feito, alto risco de clone.
  - El Niño: demanda gigante (Jubilut 5,9 mi, Cosmos Oculto 1,5 mi em 07/11), mas é de canal grande e já temos o 002.

## Backlog atual do Em Relevo × estes 3 (`youtube.backlog`, agendados; números em `backlog-atual/*.log`)
| id | Tema | Evidência agora (17/11) | Recomendação |
|---|---|---|---|
| 28 | Granizo (cancelado) | A demanda é de vídeo de celular e nowcasting (Natureza em Fúria 633 mil, Adriel Tavares 543 mil), que não temos | **sair** |
| 29 | Calor do Super El Niño | Gigantes dominam (Jubilut 5,9 mi a 27×, Manual do Mundo 3,6 mi); já fizemos o 002 (El Niño) | **sair** (ou só como gancho de outro tema) |
| 30 | Litoral do RS, 600 km de praia reta | Explica no Mapa "620 km de praia do RS esquecido" 402 mil (20×, 01/11): demanda real, mas recém-feito | **parar**; pode virar continuação do #1 (o litoral que ganha × o que perde) |
| 31 | Neve no Sul | Demanda de notícia em jun–set (CNN 473 mil em 07/09); em novembro está fora da estação | **sair** até mai/2027 |
| 32 | Cânions do Sul | Turismo, 0,4–1,5× a mediana; o ângulo geológico (deserto sob lava) já foi feito pelo Sob o Mapa (685 mil) | **sair** |
| 33 | Geada negra de 1975 | AntigamenteBR 422 mil (16×), Vestígio 80 mil (7×, 04/11); tema de história e de inverno | **guardar** para jun–jul (aniversário em 18/07) |

Os 3 candidatos ganham do backlog porque combinam **demanda medida em canais pequenos** com momento datado e ângulo de mapa que a manada não tem. O backlog era só clima do Sul, e o Rodrigo abriu o escopo.

## Arquivos
- `RELATORIO.md` (este), `refs.csv` (416 vídeos com ≥ 20 mil views e coluna `candidato`), `temas.tsv` (28 temas e buscas), `score.py`, `canais_mapa.py`.
- `scan/<tema>/refs.csv` + `medianas.json` (varredura); `canais-mapa/canais.json` (13 canais de mapa).
- `candidatos/<slug>/`: `FICHA.md`, `refs.csv`, `mosaico.jpg` (+ `-320`), `manada/` (transcrições); subsolo também tem `autocomplete.txt` e `noticias.txt`; vulcões tem o hillshade SRTM.
- `backlog-atual/` (medição dos agendados). `thumbs/` e `busca/` ficam fora do git (regeneráveis; `.gitignore`).
