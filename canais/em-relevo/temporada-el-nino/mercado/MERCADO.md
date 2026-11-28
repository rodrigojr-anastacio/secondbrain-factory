# Mercado: Super El Niño no Brasil (temporada do Em Relevo), 28/11/2026

Parte do diagnóstico de `relatorios/portfolio/2026-11-28-dados/em-relevo.md` (não refeito aqui). Custo pago: US$ 0 (yt-dlp via WARP + Data API só leitura `videos/channels/playlistItems.list`, sem `search.list`). Arquivos: `refs.csv` (542 vídeos), `thumbs/` (83 miniaturas), `mosaico-outliers.jpg`, `lado-a-lado-cosmos-x-nos.jpg`.

**Método.** 157 buscas yt-dlp (relevância, "este ano por views" e, nas 39 primeiras, "mais recentes"): 52 consultas pt (as do pedido + estados, 1877/1982/1997/2015, La Niña, apagão, safra, dengue, aviação, Pantanal etc.) e 7 en/es. 1.385 vídeos únicos; 693 com "niño/niña" no título e data ≥ 2025; 542 no CSV (≥ 1.000 views, > 60 s). Inscritos de 444 canais; **mediana do canal** = mediana de views dos vídeos > 3 min entre os últimos 50 uploads (exclui o próprio vídeo). **Marca ⚠ = base frágil** (< 8 vídeos ou mediana < 500: o múltiplo infla). **(S)** = vídeo com a cara/voz de Sérgio Sacani (corte, entrevista ou reação; observado nas thumbs e títulos). **Outlier** = pt, 2026, > 3 min, canal < 50 mil inscritos, ≥ 5× a mediana, ≥ 5 mil views (+ CanalSingularidade, sem base: só 2 vídeos longos). Classificação de título por regex; classificação de thumb **à mão** (olhei as 83). Views de 28/11/2026.

## Achados (5 linhas)
1. **Metade do "outlier pequeno" em pt é Sacani, não formato.** 10 dos 29 outliers e 8 das 20 maiores (FrameCast 2,4 mi, Refúgio Cortes 1,6 mi, Cosmos Oculto 1,5 mi + 318 mil, Khonshu 356 mil…) são cortes/entrevistas do mesmo cientista; a cara dele aparece em 8 das 20 thumbs. **Não é replicável** (direitos, pessoa). Sem eles sobram 19 outliers "originais".
2. **O padrão replicável é "Brasil + consequência vaga + data", não o mapa.** Nos 20 maiores: "Brasil/estado" como sujeito 13/20 (65%), "(Super) El Niño" + marcador de tempo 9/20, "o que vai/pode acontecer" 6/20, caixa alta em ≥ 2 palavras 14/20. Palavras específicas (seca, chuva, calor, dezembro, "visto do espaço", "partindo") aparecem em **no máximo 2 de 20 títulos**: o tema (Super El Niño no Brasil) pesa mais que a palavra.
3. **Os 3 outliers originais de hoje são lotérica de canal minúsculo**: Cosmos Brutal (844 insc., 1 hit em 14 vídeos; os outros 25–11 mil), Radar do Planeta (716 insc.: 151 mil em 3 dias; os 3 vídeos seguintes: 13,8 mil, 836, 48), CanalSingularidade (12,5 mil insc., 2,2 mi em 4 dias). O algoritmo está **testando** canais novos no tema; o 002 só recebeu 595 impressões.
4. **Nossa thumb está na mesma família do Cosmos** (escuro, faixa quente do Pacífico, 2–3 palavras, amarelo/branco). A diferença é globo fotorrealista saturado + **data** ("DEZEMBRO CRÍTICO") contra mapa plano + dúvida ("SÓ 2 °C?"). O CTR do 002 (3,2% geral; 4,2% em 21–26/11) não é o gargalo principal; **impressões** são.
5. **Tema "NÃO é o que você pensa" tem 3 vídeos ≥ 1,1 mi** (Miranda Verso 1,73 mi, Investidor Sardinha 1,2 mi, Sou curioso?! 1,1 mi) e é exatamente o conteúdo do nosso 002 (termômetro novo, "super" não é oficial), embalado como pergunta sim/não.

## a) Vídeos de 2026
### Outliers pt (29; canal < 50 mil inscritos e ≥ 5× a mediana; ordenados por views)
| título | canal | inscritos | views | data (2026) | min | mediana do canal | múltiplo |
|---|---|---|---|---|---|---|---|
| [🔴ALERTA: SÉRGIO SACANI EXPLICA O SUPER EL NIÑO E AS CHUVAS DE SETEMBRO](https://youtu.be/y55u6AnLkK8) | FrameCast BR (S) | 22,1 mil | 2.404.611 | 10/09 | 15 | 3.410 | 705× |
| [O Pacífico está PARTINDO o BRASIL em DOIS](https://youtu.be/GIlODBvMMKE) | CanalSingularidade | 12,5 mil | 2.200.636 | 24/11 | 10 | — | s/ base ⚠ |
| [“O BRASIL INTEIRO VAI SENTIR”: OS EFEITOS DO SUPER EL NIÑO / SÉRGIO SACANI](https://youtu.be/C82XkHQNL4g) | Refúgio Cortes (S) | 45,8 mil | 1.568.000 | 19/10 | 20 | 64.955 | 24× |
| [EL NIÑO: O FENÔMENO QUE PODE MUDAR O BRASIL! 🌎 #ElNino #Clima #cosmos](https://youtu.be/ypzxfNnCVio) | Cosmos Oculto (S) | 26,4 mil | 1.507.711 | 07/11 | 11 | 959 | 1572× |
| [O El Niño de 2026 NÃO é o Que Você Pensa](https://youtu.be/gkkqmtbOwmE) | Sou curioso?! | 11,7 mil | 1.102.906 | 06/10 | 25 | 214.400 | 5,1× ⚠ |
| [SACANI ALERTA: O EL NIÑO PODE CAUSAR UM ESTRAGO SEM PRECEDENTES](https://youtu.be/-c9PYfPA4JA) | Cortes do Khonshu (S) | 6,3 mil | 355.933 | 24/08 | 18 | 21.722 | 16× |
| [EL NIÑO VAI CASTIGAR O BRASIL? O ALERTA DE SACANI! 🌎 #ElNino #SergioSacani #Co](https://youtu.be/753EunXU8LM) | Cosmos Oculto (S) | 26,4 mil | 317.668 | 25/10 | 18 | 959 | 331× |
| [O Que Destruiu Tupanciretã Pode Voltar — e o Super El Niño Explica Por Quê](https://youtu.be/LXQmVHzwhSU) | Radar Do Planeta | 716 | 151.367 | 25/11 | 12 | 554 | 273× |
| [SUPER EL NIÑO DE 2026 / A Crise Oceânica Que Pode Mudar o Futuro da Terra - Vo](https://youtu.be/mDswg5vaN8A) | Santuário Marinho Docu | 35,3 mil | 120.502 | 15/06 | 48 | 19.360 | 6,2× |
| [O SUPER El Niño Visto do Espaço: o Que Vai Acontecer com o Brasil](https://youtu.be/A_DD4hC8UoQ) | Cosmos Brutal | 844 | 100.323 | 11/11 | 19 | 929 | 108× ⚠ |
| [SUPER EL NIÑO: O QUE PODE ACONTECER NO BRASIL NOS PRÓXIMOS MESES](https://youtu.be/41ytCppw6KE) | Cortes Singularidade (S) | 9,4 mil | 89.456 | 25/09 | 38 | 11.339 | 7,9× |
| [EL NIÑO vai acabar com o BRASIL?](https://youtu.be/DtODLz7niM0) | Radar Geopolítico  | 10,5 mil | 77.589 | 17/07 | 14 | 3.469 | 22× |
| [EL NIÑO NO BRASIL: O PIOR AINDA ESTÁ POR VIR?](https://youtu.be/Gw7-5kE51pI) | Cortes do Faccina (S) | 1,8 mil | 56.116 | 10/11 | 26 | 378 | 148× ⚠ |
| [EL NIÑO 2026 COMEÇOU: OS RISCOS PARA O BRASIL ATÉ 2027 / El NINÕ 2026–2027 (Ep](https://youtu.be/UhXlER48SHU) | Florestal Brasil | 33,8 mil | 41.971 | 15/07 | 31 | 528 | 80× |
| [SUPER EL NIÑO 2026: CALOR PODE AUMENTAR E PREOCUPA A POPULAÇÃO DA PARAÍBA / MR](https://youtu.be/CcJudGTlQdc) | MRTV - A TV do Blog do | 45,8 mil | 39.384 | 09/11 | 8 | 381 | 103× ⚠ |
| [5 Cidades Brasileiras que Podem Sentir o Novo El Niño #elnino  #clima  #brasil](https://youtu.be/Bs7fNvRW3BU) | Agora você Sabe | 158 | 24.439 | 31/08 | 4 | 274 | 89× ⚠ |
| [SERJÃO EXPLICA O SUPER EL NIÑO QUE VAI ATINGIR O BRASIL EM 2026? #elnino #clim](https://youtu.be/hQI8N754HVw) | The_Universe_4 (S) | 43,6 mil | 23.275 | 18/06 | 8 | 291 | 80× ⚠ |
| [El Niño 2026: o que vai acontecer?](https://youtu.be/9Ee0ntOkxR8) | Bianca Witzel | 42,8 mil | 18.046 | 19/06 | 5 | 2.225 | 8,1× ⚠ |
| [EL NIÑO 2026: O QUE PODE ACONTECER COM O CLIMA DO BRASIL?](https://youtu.be/1ZzVLX-6CF0) | Curiosomente | 34,8 mil | 13.366 | 06/11 | 17 | 134 | 100× ⚠ |
| [El Niño: o mais forte da história? O que os satélites revelam](https://youtu.be/5C64aH3vZ-k) | Vista Orbital | 111 | 12.473 | 26/10 | 14 | 158 | 79× ⚠ |
| [EL NIÑO 2026: Os 120 Dias Que Podem DEVASTAR o Brasil!](https://youtu.be/OFkyPhcZ7YU) | Planeta em Alerta | 218 | 10.668 | 22/11 | 10 | 300 | 36× ⚠ |
| [El Niño 2026 Explicado de Um Jeito Que Até Uma Criança Entende](https://youtu.be/6jHOtIq7ihs) | O Mais... do Mundo! | 419 | 10.021 | 31/05 | 8 | 267 | 38× ⚠ |
| [El Niño 2026: 83% de Chance de Impacto na Safra — O Que os Dados Dizem e Como ](https://youtu.be/3_pVh6RQWn0) | Dataagro | 78 | 9.921 | 03/04 | 6 | 133 | 75× ⚠ |
| [SÉRGIO SACANI FAZ UM GRAVE ALERTA SOBRE OS IMPACTOS DO EL NIÑO/ O QUE É O SUP](https://youtu.be/5l-mGCgQXRQ) | Fronteira Econômica (S) | 5,2 mil | 9.703 | 21/11 | 10 | 1.629 | 6,0× |
| [O que o "SUPER" El Niño faz com a SUA região do Brasil? (medimos 44 anos de ch](https://youtu.be/yiuO0D57Zng) | E Se Fosse Aqui? | 47 | 8.532 | 26/11 | 12 | 150 | 57× ⚠ |
| [EL NIÑO: O FENÔMENO QUE PODE CAUSAR SECA OU ENCHENTE NO BRASIL](https://youtu.be/YbXxuAEnpuQ) | Cosmos Oculto (S) | 26,4 mil | 6.185 | 01/09 | 14 | 1.051 | 5,9× |
| [A TRAGÉDIA DO EL NIÑO 1877 / A Seca que Matou Milhões de Pessoas / Documentári](https://youtu.be/w9w_K-Ih6xw) | Arquivo Brasil | 269 | 6.183 | 22/09 | 51 | 656 | 9,4× |
| [COMO O EL NINO VAI AFETAR CADA REGIÃO DO BRASIL EM 2026](https://youtu.be/lm8Jag3tiCs) | Planeta de Duvida | 26 | 6.016 | 19/08 | 6 | 57 | 105× ⚠ |
| [EL NIÑO 2026–2027: O QUE PODE ACONTECER NO BRASIL?](https://youtu.be/YA-x6Nnjnv8) | PLANETA IMPLACÁVEL | 1,1 mil | 5.069 | 06/09 | 4 | 126 | 40× ⚠ |

### Referência: grandes canais pt (≥ 500 mil views; não são outliers de canal pequeno)
| título | canal | inscritos | views | data (2026) | min | mediana do canal | múltiplo |
|---|---|---|---|---|---|---|---|
| [Super EL NIÑO NO BRASIL: o que esperar?](https://youtu.be/BAf4EYZ1AGk) | Paulo Jubilut | 3,9 mi | 5.937.439 | 27/08 | 19 | 170.213 | 35× |
| [O QUE É esse TAL de EL NIÑO? ENTENDA TUDO sobre o FENÔMENO!](https://youtu.be/tWhcTTC-pyw) | Manual do Mundo | 20,6 mi | 3.657.936 | 08/08 | 14 | 923.949 | 4,0× |
| [EL NIÑO na aviação! O que esperar? Feat. @SpaceToday  / EP. 1444](https://youtu.be/Qg8QwqACmMg) | Aviões e Músicas | 4,3 mi | 1.770.178 | 23/08 | 27 | 84.229 | 21× |
| [O El Niño NÃO é o Que Pensávamos Que Fosse](https://youtu.be/oGWX6AVkKZo) | Miranda Verso | 62,5 mil | 1.726.487 | 27/09 | 21 | 23.541 | 73× |
| [El Niño: como a passagem do fenômeno se tornou um desastre global](https://youtu.be/1iAw3SROEnA) | BBC News Brasil | 5,1 mi | 1.470.506 | 01/11 | 9 | 176.494 | 8,3× |
| ["CATASTRÓFICO": OS EFEITOS do SUPER EL NIÑO vão ABALAR 100% do BRASIL [com SÉR](https://youtu.be/b677ad-gqrI) | Ambiente de Conhecimen (S) | 341,0 mil | 1.415.242 | 09/08 | 20 | 63.020 | 22× |
| [O SUPER EL NIÑO ESTÁ CHEGANDO / Toda vez que aconteceu, o Brasil quebrou (se p](https://youtu.be/YHODkOqUwNc) | O Primo Rico | 7,9 mi | 1.331.027 | 18/07 | 31 | 452.930 | 2,9× |
| [Super El Niño pode estar entre os mais intensos já registrados; veja o que esp](https://youtu.be/iIbtVj_RZrQ) | g1 | 2,8 mi | 1.330.928 | 17/08 | 7 | 8.974 | 148× |
| [Super El Niño 2026: O Colapso Climático que vai Mudar o Brasil](https://youtu.be/dFQOVj6h2So) | Canal Top10 | 10,0 mi | 1.158.249 | 21/06 | 16 | 55.876 | 21× |
| [El NINO pode acabar com o BRASIL...](https://youtu.be/QJR4bu6BYHY) | Fatos Desconhecidos | 23,0 mi | 1.148.976 | 25/06 | 10 | 173.195 | 6,6× |
| [SUPER EL NIÑO SERÁ PIOR DO QUE O ESPERADO / O que pode acontecer com a economi](https://youtu.be/F0ZQH22Jzpg) | Bruno Perini - Você MA | 2,1 mi | 1.099.492 | 27/08 | 24 | 213.396 | 5,2× ⚠ |
| [URGENTE! ESPECIALISTA ROMPE O SILÊNCIO E REVELA TUDO SOBRE SOBRE O EL NIÑO NO ](https://youtu.be/SLcLulUFsc0) | Pânico Retrô | 3,0 mi | 1.046.571 | 23/06 | 13 | 73.964 | 14× |
| [É assim que o Super EL NIÑO vai Atingir cada estado do Brasil](https://youtu.be/p59XASLA-2A) | Capital Financeiro | 510,0 mil | 972.222 | 07/09 | 31 | 309.264 | 3,1× |
| [JH: Série especial explica o fenômeno climático El Niño](https://youtu.be/a1l5JoxJOTc) | g1 | 2,8 mi | 941.204 | 09/11 | 6 | 8.974 | 105× |

### es (≥ 300 mil views; formato de referência)
| título | canal | inscritos | views | data (2026) | min | mediana do canal | múltiplo |
|---|---|---|---|---|---|---|---|
| [El Niño se Acerca: Prepara esta Luz de Emergencia Casera](https://youtu.be/4NcB71jyCgY) | EL ANGELITO | 1,9 mi | 2.960.292 | 11/09 | 11 | 66.214 | 45× |
| [Se Viene un Súper El Niño: ¿Qué lo Hace Diferente Esta Vez?](https://youtu.be/oO0crrQ47-M) | El Robot de Platón | 3,1 mi | 2.891.865 | 16/07 | 23 | 631.540 | 4,6× |
| [¿Por Qué Este Súper Niño Es El Más Peligroso De La Historia?](https://youtu.be/_WbhI7U6ETA) | El Mecanismo | 51,9 mil | 2.271.513 | 03/10 | 11 | 41.061 | 55× |
| [Super El Niño Warning / Rising Heat Could Cause Severe Heatwaves in India / By](https://youtu.be/RyAZYKg_SgI) | Ankit Inspires India | 6,0 mi | 1.926.642 | 22/04 | 27 | 1.502.060 | 1,3× |
| [Lo que viene después de El Niño es peor que El Niño](https://youtu.be/4Qm4nd4JMpM) | Astrovía | 110,0 mil | 1.813.601 | 29/09 | 19 | 156.689 | 12× |
| [O VERDADEIRO IMPACTO DO SUPER EL NIÑO NA SUA VIDA](https://youtu.be/IGgMxhMxHao) | Olá, Ciência! | 2,6 mi | 1.493.218 | 27/07 | 15 | 385.099 | 3,9× |
| [India’s NEXT Economic Crisis: Super El Niño 2026 / Case Study](https://youtu.be/fNNz9a2OIn4) | Think School | 6,6 mi | 1.337.459 | 22/05 | 19 | 1.150.931 | 1,2× |
| [Te MENTIRAM sobre o El Niño](https://youtu.be/0VYUw2UIUow) | Investidor Sardinha l  | 2,0 mi | 1.202.497 | 13/11 | 19 | 706.806 | 1,7× |
| [#NADIEDICENADA / FENÓMENO DE EL NIÑO: ANDRÉS RIEZNIK EXPLICA TODO + ANGELITA Y](https://youtu.be/ZxYoh5Nzf98) | LUZU TV | 3,4 mi | 1.095.971 | 19/10 | 134 | 179.599 | 6,1× |

### en (≥ 300 mil views)
| título | canal | inscritos | views | data (2026) | min | mediana do canal | múltiplo |
|---|---|---|---|---|---|---|---|
| [2026 will be India's Hottest Year / SUPER El Niño is Coming / Dhruv Rathee](https://youtu.be/UQr0wGqvfe4) | Dhruv Rathee | 33,4 mi | 14.505.428 | 25/04 | 19 | 13.190.369 | 1,1× |
| [Nobody has EVER seen an El Niño like this](https://youtu.be/cfT46UVhTfo) | AsapSCIENCE | 10,8 mi | 8.674.428 | 24/09 | 4 | 425.787 | 20× |
| [The Biggest El Niño in Recorded History](https://youtu.be/mgPN8B-B7tg) | StarTalk | 6,0 mi | 5.545.327 | 09/10 | 19 | 966.442 | 5,7× |
| [I’ve tracked El Niño for years. I’ve never seen this before](https://youtu.be/9OixPlkyrhc) | CBC News | 4,8 mi | 3.024.451 | 11/09 | 3 | 19.078 | 158× |
| [We've Never Seen This Kind Of El Nino](https://youtu.be/EgIYVk3ygbc) | Ryan Hall, Y'all | 3,6 mi | 2.836.569 | 30/08 | 11 | 1.905.822 | 1,5× |
| [We Were Wrong About Super El Niño](https://youtu.be/f8-FG_T-I24) | GetsetflySCIENCE by Ga | 9,9 mi | 2.535.555 | 22/08 | 23 | 1.915.551 | 1,3× |
| [This Super El Niño Just Changed My Winter Forecast...](https://youtu.be/jFPZYVcBDvQ) | Max Velocity - Severe  | 2,2 mi | 2.530.435 | 15/11 | 10 | 664.934 | 3,8× |
| [Nobody Realizes What El Niño Is About To Do To Our Planet](https://youtu.be/G27YUk3pVw8) | The Secrets of the Uni | 1,8 mi | 2.455.775 | 24/10 | 22 | 93.369 | 26× |
| [This Super El Niño Will Be the Strongest In Living Memory](https://youtu.be/_b_sGbjSVZQ) | Astrum Earth | 516,0 mil | 2.447.880 | 08/06 | 22 | 1.332.300 | 1,8× |

Leitura es/en: **El Mecanismo** (es, 51,9 mil insc.; é o modelo mais próximo do Em Relevo) fez 2,27 mi com "¿Por qué este Súper Niño es el más peligroso de la historia?" e 575 mil com "Este Súper Niño está provocando cosas que no deberían pasar"; **Astrovía** 1,81 mi e **Coordenada Crítica** 905 mil com "Lo que viene después de El Niño es peor" (La Niña, §e). Em en, o padrão é "Nobody has EVER seen…" / "We were wrong about…" / "Strongest in living memory". Nosso 002 (**3 insc., 163 views**, 12/11) fica no CSV com ⚠ (sem base).

## b) Padrões de título
**Frequência** (regex; top 20 outliers = os 20 de maior view; "todos" = 29; "≥ 100 mil" = 73 vídeos pt de 2026 > 3 min, sem g1/MetSul):

| marcador no título | top 20 | todos (29) | ≥ 100 mil (73) |
|---|---|---|---|
| contém "Brasil" | 12 | 17 | 39 |
| "Brasil"/estado/região/cidade como sujeito (qualquer) | **13** | 18 | 43 |
| "(Super) El Niño" no início | 11 | — | — |
| "Super/Súper" | 8 | 10 | 37 |
| marcador de tempo (2026, 2027, próximos meses, 120 dias, ano) | 9 | 14 | 19 |
| "o que vai/pode acontecer/esperar" | 6 | 8 | 11 |
| urgência/alarme (alerta, pior, devastar, castigar, urgente) | 5 | 6 | 26 |
| pergunta (termina em "?") | 5 | 7 | 11 |
| afirmação | 9 | 12 | 42 |
| afirmação + tempo/urgência | 5 | 9 | 17 |
| mito/contraste ("NÃO é o que…", "mentiram") | 1 | 2 | 6 |
| chuva/enchente · seca · calor | 1 · 0 · 1 | 3 · 2 · 1 | 7 · 3 · 1 |
| "dezembro/verão" | 1 | 2 | 2 |
| "visto do espaço" · "partindo/rachou" | 2 · 1 | 2 · 1 | 1 · 2 |
| caixa alta em ≥ 2 palavras | **14** | 21 | — |
| comprimento (mediana; mín–máx) | 67 (32–96) | 65 | — |

**3 padrões de título que mais aparecem (top 20):**
1. **Brasil/lugar como sujeito + consequência vaga** (13/20, 65%): "…o Que Vai Acontecer com o Brasil", "vai acabar com o BRASIL?", "O BRASIL INTEIRO VAI SENTIR", "O Pacífico está PARTINDO o BRASIL em DOIS".
2. **"(Super) El Niño" + marcador de tempo** (9/20, 45%): "…2026", "…ATÉ 2027", "…PRÓXIMOS MESES", "Os 120 Dias…". Pergunta fica em 5/20; afirmação domina (9 + 5 com tempo).
3. **Alarme/"o que vai acontecer"** (urgência 5/20 + "o que vai/pode acontecer" 6/20; sobrepõem-se): "O PIOR AINDA ESTÁ POR VIR?", "VAI CASTIGAR O BRASIL?". O **contra-intuitivo "NÃO é o que você pensa"** é raro (1/20), mas é o de maior views entre os originais (1,1 mi) e o do Miranda Verso (1,73 mi, fora dos 20 por outlier de canal 62,5 mil).

**Contra a hipótese do pedido:** a palavra "dezembro" só está em thumb (Cosmos Brutal), não em título. **O nosso título ("El Niño 2026 vai ser o mais forte da história?")** tem 3 dos marcadores (El Niño no início, tempo, pergunta) mas **não tem "Brasil"**, o marcador mais frequente (65%).

### Autocomplete do YouTube (via WARP, 28/11/2026; ordem = ranking da sugestão; sem volume)
| semente | sugestões (pt-BR salvo indicação) |
|---|---|
| "super el niño" | super el niño 2026 · **no brasil** · icl · e a catástrofe climática · fantástico · e a resiliência do setor elétrico brasileiro · **1877** · 2026 brasil · edit |
| "super el nino" | 2026 · **1877** · 2026 no brasil · 2027 · 2026 sergio sacani · fantástico · brasil · **no brasil o que esperar** · icl |
| "super el niño brasil" | super el nino no brasil o que esperar · **2026 o brasil precisa se preparar** · 2026 brasil · efeitos do super el nino no brasil · 2016 · 2023 |
| "el niño" | 2026 · de oro · y la niña · brasil · fenomeno climatico · manual do mundo · **em niño 1877** |
| "el niño 2026" | brasil · no brasil · 2026 2027 · peru · argentina · explained · noticias |
| "el niño brasil" | brasileño (música; ruído) · 2026 · **paralelo** · escola · **nordeste** |
| "el niño nordeste" | nordeste brasil · 2026 · super el nino nordeste · no nordeste brasileiro · fenômeno no nordeste |
| "el niño sul" | sul do brasil · 2026 sul do brasil · america do sul · **rio grande do sul** · mato grosso do sul |
| "el niño calor" | calor extremo · 2026 calor · onda de calor |
| "el niño seca" | 2026 seca (resto é música/"sicario") |
| "el niño dezembro" / "chuva" / "verão" | **1 sugestão cada** ("el nino dezembro", "el nino chuva") / "verão": **nenhuma** |
| [es] "super el niño" | 2026 · no brasil · explicado · argentina · 1877 · españa |
| [en] "super el nino" | 2026 · brasil · 2026 sergio sacani · no brasil o que esperar |
| expansões a–z ("super el nino X") | **como se preparar · o que fazer · confirmado · chegando · ficou mais forte · vai acontecer · pode estar · novembro 2026 · efeitos no brasil · aviação ("el nino na aviação") · tornado · terremoto · temperatura · onda de calor · minas gerais · rio grande do sul · rs · paraná · sudeste · ribeirão preto · setor elétrico · jornal nacional · globo · fantástico · 1877 · 2016 · 2023 · geografia · documentário** |
| pessoas na sugestão | **sacani/sergio sacani · serjão · molion · jubilut · primo rico · castanhari · manual do mundo · carlos nobre · leandro ribeiro · ricardo felício · ricardo marcílio · space today · sobrevivencialismo · jeangrafia** |

Leitura: a demanda de busca é **por pessoa e por "Brasil/o que esperar/como se preparar"**; "seca", "chuva", "verão" e "dezembro" praticamente não aparecem como termo de busca (mas "rio grande do sul", "nordeste", "sudeste", "minas gerais", "paraná" aparecem com "super el nino"). **1877** é sugestão em 3 variantes: demanda ligada ao nosso 003 (Seca 1877), mas ver §e.

## c) Padrões de thumb (olhadas à mão; 83 thumbs em `thumbs/<id>.jpg`, 640×360)
Legenda: fundo E = escuro, M = misto/saturado, C = claro; "globo" = globo/satélite/mapa de anomalia do Pacífico; "mapa BR" = Brasil com dado; "cena" = foto de enchente/seca/tempestade.

| atributo | top 20 outliers | 19 sem Sacani | todos (29) |
|---|---|---|---|
| fundo escuro (E) / misto (M) / claro (C) | 14 / 5 / 1 | 15 / 3 / 1 | 18 / 10 / 1 |
| herói = globo/satélite/anomalia do Pacífico | 10 | 7 | 13 |
| herói = mapa do Brasil com dado | 3 | 7 | 7 |
| herói = foto-cena (enchente, seca, tempestade) | 5 | 4 | 7 |
| rosto | 11 (8 = Sacani) | 3 | 13 |
| texto ≤ 4 palavras (mediana de palavras) | 9 (5) | 13 (3) | 15 (4) |
| texto ≥ 9 palavras | 4 | 1 | 4 |
| cor do texto: branco + amarelo/vermelho | 16 | 13 | 22 |

Para a mesma leitura nos **27 vídeos pt ≥ 500 mil de qualquer canal**: escuro 15, globo 15, rosto 17, cena 8, mapa BR 3.

**3 padrões de thumb que mais aparecem:**
1. **Fundo escuro + 1 herói de satélite/globo/mapa "em brasa"** (laranja-vermelho saturado): 13/20 com globo ou mapa BR (65%); 14/19 (74%) sem Sacani.
2. **Texto de 2–4 palavras em branco com vermelho ou amarelo**, caixa alta, contorno grosso: 9/20 (45%) top 20; 13/19 (68%) sem Sacani; as exceções são cortes com frase de 9–20 palavras.
3. **Rosto** (11/20; **8 são Sacani**, não replicável) ou **foto-cena de enchente/tempestade** (5/20; replicável com licença). Sem rosto: 84% dos originais.
Nenhum outlier tem "bege/polaroid"; o único de fundo claro entre os 20 maiores é a Bianca Witzel (apresentadora, 18 mil). O mapa **plano** de anomalia como herói aparece em 2 casos (Sou curioso?!, **1,1 mi**, "NEM A CIÊNCIA ESPERAVA" com o mapa numa moldura; MRTV, 39 mil) contra globo/satélite fotorrealista em 10: **o mapa plano não está proibido pelo mercado**, o que o Sou curioso?! tem é título contra-intuitivo. **Hipótese**: a regra da bíblia "no máximo 1 mapa escuro por vídeo" vale para o nosso 3×mesmo-conceito (seca 1877), mas **neste tema o escuro é o padrão do nicho** (Cosmos, Singularidade, Radar do Planeta); o que muda é o herói (globo/continente em brasa) e o texto.

## d) Por que o Cosmos Brutal fez ~100 mil e nós 163
Imagem: `lado-a-lado-cosmos-x-nos.jpg`. Fontes: Data API, transcrição Whisper dos primeiros 3 min do vídeo deles (`tools`/yt-dlp via WARP), `ROTEIRO.md` do 002, `youtube.alcance_diario` e `analytics_trafego_detalhe` (até 26–28/11).

| | **Cosmos Brutal** (`A_DD4hC8UoQ`) | **Em Relevo 002** (`FeSLzHvlkbo`) |
|---|---|---|
| título | O SUPER El Niño Visto do Espaço: o Que Vai Acontecer com o Brasil | El Niño 2026 vai ser o mais forte da história? |
| thumb (no ar) | globo fotorrealista, faixa do Pacífico em brasa, **"DEZEMBRO CRÍTICO"** (2 palavras, branco/vermelho) | mapa vetorial plano navy, termômetro, seta amarela até o Brasil, **"SÓ 2 °C?"** |
| duração | 19:33 | 12:10 |
| canal | 844 insc., criado 04/11, 14 vídeos (mediana 929) | 3 insc., 5 vídeos no ar |
| publicação | **10/11 22:42 (BRT)**, 3ª-feira à noite | 12/11 18:15 (BRT), 5ª-feira |
| resultado | 100.323 views em 18 dias; o vídeo seguinte do mesmo tema: 11 mil (24/11) | 163 views em 16 dias; 595 impressões (Reporting API) |
| tráfego | não público | 120 de 135 views (Analytics até 25/11) vêm de "vídeos relacionados": O POVO 29, BBC Brasil 27, **Cosmos Brutal 10**, Ruptura do Povo 8, Ruma News 5 (`RELATED_VIDEO`); inscritos 9; busca 3 |

**Hook, primeiros 30 s.**
- **Cosmos (transcrição):** "Neste exato momento, uma faixa do Oceano Pacífico, quase duas vezes maior que o Brasil, está mais quente do que deveria. E ela nunca esteve tão quente. Em outubro, os satélites mediram a água dessa região 2,47 graus acima do normal. Foi o maior valor já registrado para um mês de outubro. O recorde anterior era de 1982. E o ano de 1982 terminou em tragédia." A promessa vem aos 0:35 ("o mais forte desde que começamos a medir"), o prazo aos 0:46 ("pico em dezembro, daqui a poucas semanas"), o formato aos 1:11 ("você vai ver tudo isso de cima, do espaço") e a lista de perguntas (regiões, risco de apagão) aos 1:17. **Abre com um número, um recorde e uma ameaça no ar agora.**
- **Nosso:** "Manaus, 9 de outubro. A fumaça das queimadas fecha escolas… (~200 µg/m³; OMS 15). No mesmo mês, em Dionísio Cerqueira, chovem 581 mm… E, do outro lado dos Andes, o mar está 5 graus e meio acima do normal." A pergunta do vídeo só aparece aos **0:36** ("então… esse é mesmo o tal Super El Niño?"). **Abre com 3 cenas locais e só depois formula a pergunta**; sem o recorde nem o prazo.

**O que o nosso dado diz:** CTR do 002 = **3,19%** (595 impressões; sugerido 3,17% em 537), já ao nível da média do Dossier (3,69% em 269 mil impressões). Por janela (Reporting API, "todas as origens"): **12–15/11: 1,60% (250 imp.)**; 16–20/11: 7,7% (13 imp.); **21–26/11: 4,22% (332 imp.)**. A thumb "SÓ 2 °C?" substituiu a bege em data que não consegui confirmar (a do ar não é a `thumb-nova.jpg` do repo, que é a versão de relevo claro): **Hipótese** de que a troca explique 1,6% → 4,2% (amostra pequena, mistura de fontes, origem mudou para sugerido).

**Conclusão em 5 bullets**
1. **Distribuição, não clique, separa os dois.** 100 mil views com CTR de 3–6% pedem **~1,7–3,3 mi de impressões** (**Hipótese**, conta de padeiro); nós tivemos 595. O YouTube testou o Cosmos em escala e não nos testou.
2. **Foi loteria de canal minúsculo**: 1 acerto em 14 vídeos (mediana 929); o Radar do Planeta (716 insc.) e o CanalSingularidade seguem o mesmo desenho (um pico em 3–4 dias). Ninguém garante repetir; só dá para **subir a chance** (e depois do acerto, o seguinte rendeu 11–14 mil: o tema com cadência reforça).
3. **Embalagem do Cosmos tem urgência com prazo ("DEZEMBRO CRÍTICO", "pico em dezembro") e "Brasil" no título**; a nossa tem dúvida ("SÓ 2 °C?", "o mais forte da história?") e **não tem Brasil nem data**. Pergunta sim/não "esgota a curiosidade" (bíblia) e o título do 002 ficou longe do padrão dos 20 (Brasil 65%).
4. **Hook**: eles abrem com número + recorde + tragédia de 1982 + prazo em 46 s; nós abrimos com 3 cenas e a pergunta aos 36 s. O nosso é bom para segurar (retenção 59% em 12 min, relativa 0,5–0,66), **mas o hook não explica as impressões**: quem decide o clique é título+thumb e quem decide a distribuição é o histórico do canal no tema (0 vs. uma semana de vizinhança).
5. **Nosso ativo comprovado é o conteúdo** (59%, 4,2% de CTR na janela boa, views vindas do sugerido de O POVO/BBC/Cosmos): o 002 está no grafo certo. A ação de menor custo é **reembalar** (título com Brasil + data + "NÃO é o que você pensa", thumb com globo/continente em brasa) e **entrar em cadência** no tema antes do pico (dezembro–fevereiro).

## e) Lacunas e saturação (alimenta a escolha dos 6 vídeos)
Busca com 52 consultas pt (28/11); "n" = vídeos pt de 2026 > 3 min com o termo no título (regex; ruído pequeno). **Saturado** = ≥ 3 vídeos ≥ 500 mil ou ≥ 5 outliers.

**Saturado em pt:** "o que esperar/o que é El Niño" (Jubilut 5,9 mi, Manual do Mundo 3,7 mi, BBC 1,5 mi, g1, Olá Ciência 1,5 mi); "estado por estado/sua região" (Capital Financeiro 972 mil, JeanGrafia, Explica no Mapa 78 mil, E Se Fosse Aqui 8,5 mil, Planeta de Dúvida 6 mil); "Pacífico partindo/rachando o Brasil" (CanalSingularidade 2,2 mi, JeanGrafia 143 mil); "preço/safra/economia" (Primo Rico 1,3 mi, Perini 1,1 mi, Climatempo 200 mil); tudo com Sacani.

| # | tema/ângulo candidato | evidência de demanda (vídeo de referência, views) | oferta pt / colisão | notas |
|---|---|---|---|---|
| 1 | **"NÃO é o que você pensa" / termômetro novo, "super" não é oficial, ainda não é o maior** (reembalagem do 002 ou 2º vídeo) | Miranda Verso 1,73 mi (62 mil insc., 27/09); Investidor Sardinha "Te MENTIRAM…" 1,2 mi (13/11); Sou curioso?! 1,1 mi (06/10); GetsetflySCIENCE "We Were Wrong About Super El Niño" 2,5 mi | **média**: 3 grandes, nenhum com o dado RONI/ONI | já temos o conteúdo (b19–b21); pede mapa/gráfico da NOAA |
| 2 | **Roraima/Amazônia: seca e fogo de dez–abr** (rio Branco abaixo do mínimo; rio Negro 4 m acima de 2024) | Tempo&Dinheiro "El Niño virou fumaça?" 373 mil; g1 JH "incêndios florestais" 182 mil; Professor Ricardo 149 mil; Radar do Planeta "Enquanto o Sul afoga, a Amazônia seca e pega fogo" 27/11 (853 views, 716 insc.) | **média**: 30 vídeos, maioria TV; Radar do Planeta acabou de entrar | dado próprio do roteiro 002 (b26–b28); ângulo "norte da Amazônia, não Manaus" é lacuna |
| 3 | **Nordeste: o sertão e o El Niño** | Chão do Nordeste "Ninguém imagina o que o El Niño pode fazer com o Nordeste" **217 mil** (11,5 mil insc., 12/11); Agro em Debate 292 mil (Molion); Agreste Selvagem 76 mil | **média-baixa**: 44 vídeos, 2 ≥ 100 mil; autocomplete "el niño nordeste" ×5 | clone de Chão do Sul tem 217 mil: demanda provada |
| 4 | **Vai faltar luz? Apagão, reservatórios e conta de luz** | Ernesto Reis "Apagão mundial, guerra, El Niño, kit 72 h" **131 mil**; talvezverso 53 mil; Jovem Pan "Copom/conta de luz" 34 mil; autocomplete "super el niño e a resiliência do setor elétrico" e "apagão" no hook do Cosmos | **baixa**: 10 vídeos, só de notícia ou sobrevivencialismo | reservatórios a 65,9% (b31) é dado próprio e contra-narrativa; mapa de bacias/hidrelétricas é lacuna |
| 5 | **Sul: o vale do Taquari/Muçum "pode voltar"** (por que o vale inunda de novo) | Radar do Planeta "O que destruiu Tupanciretã pode voltar" **151 mil** em 3 dias; g1 "chuvas no Sul" 179 mil; MetSul 275–335 mil; Carol Capel 170 mil | **alta** (MetSul, TV, Carol Capel); mas ninguém faz o mapa de bacia | nosso 005 (Porto Alegre) está no ar com 130 views; evitar "notícia/flagrante" |
| 6 | **La Niña em 2027: o que vem depois do El Niño** | **es:** Astrovía 1,81 mi (110 mil insc., 29/09), Coordenada Crítica 905 mil (21 mil insc., 23/10); **pt:** Tempo no Nordeste 10–19 mil (3 vídeos), Será Que Chove? 9,9 mil | **baixa em pt**; demanda **provada só em es** | **Hipótese** de transferência; tempo certo é o fim do pico (jan–fev) |
| 7 | **1982-83 e 1997-98 comparados a 2026 no mapa** (Blumenau 1983, Roraima 1998; o "último super" no Brasil) | DW News "A historic El Niño…" 2,07 mi (en); KTLA 1982-83 280 mil (en); BBC Brasil 1877 1,47 mi; autocomplete "super el nino 1877" (3×) e "el niño de 1877" | **baixa em pt** para 1983/1998 (Arquivo Brasil 1877 doc: 6 mil; Planeta Severo 1997: 110) | **colisão com os nossos 003/004** (24–31 views); funciona só **ligado a 2026**; sem "matou" no título |
| 8 | **Safra e preço do alimento, em mapa** (soja, milho, café, arroz) | Primo Rico 1,33 mi; Perini 1,10 mi; Climatempo 200 mil/181 mil | **alta** em finanças; **baixa em mapa** | RPM maior; arriscado "parecer economia"; 75 vídeos no tema |
| 9 | **Aviação e El Niño** (jato subtropical, turbulência) | Aviões e Músicas **1,77 mi** (4,3 mi insc.); Minuto Aéreo 372 mil (Sacani); autocomplete "el nino na aviação" | **baixa** de mapa (12 vídeos, 2 ≥ 100 mil) | plausível com o jato em 3D; fora do núcleo; **Hipótese** |
| 10 | **Verão 2026/27 por região (previsão oficial, mapa 3D)** | CNN Brasil onda de calor 224 mil; SBT News 178 mil; MetSul 71 mil (25/11); autocomplete "o que muda no seu verão", "super el nino sudeste/minas gerais/paraná/rs" | **alta** (notícia); mapa 3D de chuva+calor é lacuna | encaixa com o pico dez–fev; risco "parecer notícia" |
| 11 | **Calor e saúde (dengue, mortes por calor)** | globonews "13,3 mil mortes por calor" 59 mil; TV Aparecida dengue 15 mil; (es: Panorama Peru 21 mil) | **muito baixa**: 9 vídeos, máx. 59 mil | demanda fraca; **título sem "mortes"** (política) |
| 12 | **Por estado: um vídeo por UF (RS, SC, PR, MG, SP, AM, BA)** | Capital Financeiro "cada estado" 972 mil; Explica no Mapa "SEU estado" 78 mil; MRTV Paraíba 39 mil; autocomplete "rio grande do sul", "minas gerais", "paraná", "rs", "ribeirão preto" | **alta** no genérico; **baixa** no específico (um estado, mapa) | série encaixa em cadência; long tail sem prova de volume |

Fora da lista por baixa evidência ou aderência: Pantanal e hidrovias (1–2 vídeos, sem demanda medida); "como se preparar/kit" (EL ANGELITO 2,96 mi em es; em pt é sobrevivencialismo); litoral/ressaca/pesca (16 vídeos, 1 ≥ 100 mil).

## f) CTR de referência (honesto: CTR de terceiro não é público)
**Nossos dados** (`youtube.alcance_diario`, Reporting API; "todas as origens"; atraso 1–2 dias):

| canal | impressões | CTR ponderado |
|---|---|---|
| dossie-es | 269.361 | 3,69% |
| historia-ptbr | 18.473 | 3,42% |
| em-relevo | 4.213 | 2,18% |
| lugares-guerra-en | 4.622 | 1,64% |

- **Dossier e História, vencedores no sugerido (origem 7)** com ≥ 1,5 mil impressões: Masones 6,48% (1.758), Egito 5,55% (2.648; História), Inquisición 4,64% (2.326), FBI 4,37% (1.692), Índia 4,08% (2.107; História). Com amostra grande, a faixa estabiliza em **3,4–4,0%** (SS 3,97% em 31 mil imp., Cosa Nostra 3,44% em 66 mil). **Leia "4–7%" como amostra pequena de vencedor, não como média.**
- **Em Relevo 002**: 3,19% (595 imp.; sugerido 3,17% em 537; busca 4,0% em 25); 1,60% em 12–15/11 e 4,22% em 21–26/11 (§d). 001: 5,3% (262 imp.); 003: 1,04% (1.832); 004: 2,67% (487); 005: 2,60% (1.037).
- **Aviso de método:** o 002 teve 163 views mas só ~19 cliques estimados (595 × 3,2%). A diferença vem de visualizações sem impressão (autoplay "a seguir" e vídeo sugerido de O POVO/BBC: 120 views de `RELATED_VIDEO`). **Hipótese:** o CTR da Reporting API subestima o alcance real de vídeos que vivem de "a seguir".

**O que dá para inferir dos outliers (todas Hipóteses):**
- **Views por inscrito** (Cosmos Brutal 119; Radar do Planeta 211; CanalSingularidade 176; Cosmos Oculto 57): quase tudo é audiência fora do canal, ou seja, recomendação/home; a embalagem foi aprovada pelo algoritmo no teste inicial.
- **Impressões implícitas:** views ÷ CTR. Com CTR de 3–6% (faixa dos nossos canais maduros e do nicho): Cosmos Brutal ≈ 1,7–3,3 mi; CanalSingularidade ≈ 37–73 mi (improvável; o CTR dele deve ser maior, ou parte vem de Shorts/telas finais; **sem base**).
- **Velocidade:** CanalSingularidade 2,2 mi em 4 dias (≈ 550 mil/dia); Radar do Planeta 151 mil em 3 dias depois de 5 vídeos de 58–3.800 views; Cosmos Brutal 100 mil em ~18 dias. Padrão de **pico curto** → o teste do algoritmo acontece nas primeiras 24–72 h, e um CTR < 2% (como o do 003: 1,0%) encerra.
- **Régua prática (bíblia/diagnóstico):** CTR ≥ 3,5% nas primeiras ~1.000 impressões do sugerido; < 2% com ≥ 1.000 impressões → trocar a embalagem. Não existe CTR de terceiro público; qualquer número acima é conta, não medição.

## Limitações
Mediana de canal com poucos vídeos infla o múltiplo (⚠); classificação de título por regex e de thumb manual (n = 83); views de um dia (28/11); "outlier de canal pequeno" mistura canais de 100 a 46 mil inscritos; Sacani identificado por thumb/título (alguns canais podem ser entrevistas autorizadas); a thumb do 002 no ar foi baixada de `i.ytimg.com` em 28/11 e pode ter mudado depois do lançamento.
