# Benchmark das referências, últimos 28 dias (14/11/2026)

Brief: `~/workspace/referencias/BRIEF-benchmark-referencias-28d.md`. Só leitura: nada mudou em bíblia, backlog ou banco.
Coleta: YouTube Data API em 14/11 ~10h (**148 unidades**: `channels` + `playlistItems` + `videos`; sem `search`), 35 canais de referência + os 4 nossos. Custo: US$ 0.
Janela: **28 d = 17/10 a 14/11**. Longo = mais de 3 min; Short = até 3 min. Horários em BRT. "v/i" = views ÷ inscritos atuais do canal.
**[O]** = observado · **[I]** = inferido · **Hipótese** = sem dado direto.
Dados: `dados/canais-2026-11-14.json` (todos os vídeos), `dados/videos-90d.csv`, `dados/resumo.json`, `dados/nossos-*.json`. Grades de thumbs (3 melhores + 3 piores): `thumbs/grade-*.jpg`. Scripts: `scripts/`.

## Resposta curta
| Nosso canal | Ritmo deles (28 d) | Nosso ritmo | O que mais funcionou neles | 1 recomendação (Hipótese) |
|---|---|---|---|---|
| História em minutos | HiM 0,75/sem · Genius 1,5 · clones pt 2–4,25 | ~4,5/sem (7 em 11 d) | **Rússia 254 mil, França 188 mil** (clone pt), **1ª Guerra 237 mil** (History Easy Guide), Alemanha 271 mil (Genius) | Escolher o tema pelo que um vídeo pt **está rodando agora** (é de onde vêm nossos sugeridos); testar 1 guerra mundial, com OK do Rodrigo (fora da bíblia) |
| Dossier en Minutos | Archive 6,5/sem · Atlas 7,75 | ~4/sem (6 em 10 d) | **Nazistas** (Archive SS 684 mil, Gestapo 452 mil) e **CIA vs KGB** (Atlas 100 mil, o melhor dele) | **Gestapo** já (backlog 008) e horário fixo 18–19h |
| Em Relevo | Mundo Entrópico 2,25/sem · Chão do Sul 2/sem | 2 no ar + 3 agendados em 6 d | **Sul do Brasil**: Chão do Sul 736 mil (o 1º vídeo do canal), Mundo Entrópico SC 447 mil | Fazer do Sul a série-âncora, com thumb de mapa do estado aceso + pergunta de 2–3 palavras |
| Clearance Required | WTS 2,5/sem · CWFP 0,75 | 1 no ar + 2 agendados | **Ilhas fechadas do Pacífico**: "Why Is Wake Island Still Closed to Americans?" **529 mil** (canal de 15 dias) | Série "ilhas/bases fechadas do Pacífico" logo depois de Midway e Bikini |

**Leitura geral [O]:** em todos os nichos o padrão é o mesmo: **1 ou 2 vídeos fazem 80–95% das views** do canal, e o hit vem de um **tema já provado por outro canal** (Rússia e França no pt, SS no es, Wake depois de Iwo Jima, Sul depois de Mundo Entrópico). Postar mais não substitui tema: o Spies in Minutes publicou **50 vídeos em 13 dias** e tem mediana de **29 views**.

---

## 1. Tabela resumo por referência (28 d, só longos)
| Canal | Papel | Inscritos | Idade (1º vídeo no ar) | Longos/sem | Duração média | Mediana views | Melhor vídeo (28 d) |
|---|---|---|---|---|---|---|---|
| **historia-ptbr** | | | | | | | |
| History in Minutes (en) | principal | 20,5 mil | 63 d | 0,75 | 17 min | 2,3 mil | Christianity 2,6 mil (1 d) |
| Genius History (en) | principal | 41,9 mil | 152 d | 1,5 | 21 min | 34,5 mil | Germany 271 mil |
| História em minutos (clone pt de 08/2026) | clone | 5,6 mil | 35 d | 2,25 | 30 min | 2,3 mil | Rússia 254 mil |
| History Easy Guide (pt) | clone | 3,0 mil | 17 d* | 4,25 (+14 Shorts) | 14 min | 5,5 mil | 1ª Guerra Mundial 237 mil |
| História Inteira (pt) | clone | 42 | 14 d | 0,5 (+8 Shorts) | 15 min | 549 | Brasil 896 |
| **dossie-es** | | | | | | | |
| Archive in Minutes (en) | principal | 21,5 mil | 30 d* | 6,5 | 15 min | 59,9 mil | The SS 684 mil |
| Atlas del Tiempo (es) | principal | 1,8 mil | 36 d* | 7,75 | 20 min | 1,2 mil | CIA vs KGB 100 mil |
| Te lo Pinto (es) | similar | 603 mil | 2,5 anos | 6,25 | 34 min | 160 mil | Corea del Norte 333 mil |
| Archivo Desclasificado (es) | similar | 7,6 mil | 25 d* | 5 | 48 min | 32,9 mil | Crisis de los misiles 268 mil |
| Archivo en Minutos (clone es) | clone | 16 | 15 d | 1,75 | 16 min | 355 | Gestapo 1,8 mil |
| **Em Relevo** | | | | | | | |
| Mundo Entrópico (pt) | principal | 66 mil | 1,8 ano | 2,25 | 16 min | 60 mil | O que está ACONTECENDO com SANTA CATARINA?! 447 mil |
| Chão do Sul (pt) | principal | 6,6 mil | 20 d* | 2 | 20 min | 47,8 mil | Por que a Região Sul é o OPOSTO… 736 mil |
| Um Documentário (pt) | similar | 130 mil | 7 meses | 0,75 | 68 min | 289 mil | Era do Gelo 460 mil |
| The Last Day (en) | similar | 36,5 mil | 4 meses | 0,75 | 19 min | 148 mil | Chovesse 1 ano 444 mil |
| **Clearance Required** | | | | | | | |
| Where They Stood (en) | principal | 3,8 mil | 41 d | 2,5 | 22 min | 33,8 mil | Omaha Beach 348 mil |
| Civil War Fine Print (en) | principal | 4,1 mil | 6 d | 0,75 (+5 Shorts) | 15 min | 7,7 mil | Lincoln's Death 1,09 mi |
| Long After The Guns (en) | clone | 1,2 mil | 15 d | 1,75 | 16 min | 2,1 mil | Wake Island 529 mil |
| Ship Tales (en) | clone | 1,1 mil | 49 d | 4,75 | 16 min | 890 | USS Massachusetts 92 mil |
| Forgotten Fleet (en) | similar | 15,2 mil | 8 meses | 3,5 | 16 min | 12,9 mil | Pink Submarine 447 mil |

\* Canal antigo que apagou ou escondeu os vídeos velhos: a idade é a do 1º vídeo **que está no ar**. Os outros 15 canais (clones minúsculos, Spies in Minutes, Astrum, Geoff etc.) estão em `dados/resumo.json`.

---

## 2. Por canal nosso

### 2.1 História em minutos (historia-ptbr)
**Temas nos 28 d [O]:** Genius: Alemanha, Austrália, Suíça, Itália, Dinamarca, Rússia. HiM: Cristianismo, Japão, Coreia. Clone pt de 08/2026: Rússia, França, Austrália, Japão + Brasil atual (governos, crises, Maduro, furacão). History Easy Guide: 1ª e 2ª Guerra, Roma, Brasil, impérios, Guerra Fria, Esparta, Egito, Napoleão, Revolução Francesa (14/11) + atualidades (Trump/Irã, Banco Master).

**Funcionou × flopou [O]:**
| Funcionou | Views (v/i) | Flopou | Views |
|---|---|---|---|
| Genius: Alemanha | 271 mil (6,5) | HiM: Japão, Coreia, Cristianismo | 1,4–2,6 mil |
| Clone pt: Rússia (37 min) | 254 mil (46) | Clone pt: Japão, Austrália | 2,3–2,4 mil |
| HEG: 1ª Guerra Mundial | 237 mil (80) | HEG: Chernobyl, Banco Master, Cidades perdidas | ~1 mil |
| Clone pt: França (38 min) | 188 mil (34) | Clones 10/2026 (Portugal, Incas, Argentina, KGB) | 2–9 |
| Genius: Austrália | 109 mil (2,6) | Genius: Dinamarca, Itália, Suíça | 30–38 mil (o "piso" dele) |
| HEG: 2ª Guerra Mundial | 107 mil (36) | | |
| HEG: Roma (12 min) | 73 mil (25) | | |

- **Japão é a prova mais limpa de tema fraco [O]:** flopou nos 3 canais que o publicaram em 28 d (HiM 2,3 mil, clone pt 2,3 mil; Genius tem um de 993 mil, mas de 14/10). **Austrália** foi bem em en (109 mil) e mal em pt (2,4 mil).
- **HiM está em queda [O]:** dos 641 mil (Índia, 30/09) para 1,4–2,6 mil nos 3 vídeos de novembro, com 0,75 vídeo/semana. O molde segue vivo (Genius, clones pt); o canal-modelo é que esfriou.
- **Título [O]:** os hits em pt usam "Toda a história de X em N minutos" (clone) e "A HISTÓRIA INTEIRA de X" (HEG); os de en, "The ENTIRE History of X in N Minutes". HiM trocou para título-frase ("Korea Survived Every Empire…") e caiu ainda mais (1,4 mil). Duração não decide: hits com 12, 17, 21 e 38 min.
- **Thumb [O]** (`thumbs/grade-genius-history.jpg`, `grade-history-easy-guide.jpg`, `grade-história-em-minutos--clone-08-2026-.jpg`):
  - Genius: nome do país em serifa gigante + "ANO – 2026" + figura histórica grande + panorama. Os hits e os flops têm a **mesma** thumb, então quem decide é o tema.
  - Clone pt: o mesmo molde, mas com o **líder atual** na figura (Putin, Macron) e prédios pegando fogo nos 2 hits.
  - **HEG usa bonequinho de cabeça redonda, igual ao nosso**, com 3–4 palavras de impacto ("1 TIRO E O MUNDO EXPLODIU", "6 ANOS QUE MUDARAM TUDO") + etiqueta vermelha com o tema. Os flops do HEG usam o mesmo estilo em tema fraco.
- **Frequência e horário [O]:** Genius publica sempre às **09:30** (6 de 6); HiM ~16h; o clone entre 18h e 22h; HEG em qualquer hora (9h–21h). Dias variados em todos.

### 2.2 Dossier en Minutos (dossie-es)
**Temas nos 28 d [O]:** Archive (26 vídeos): SS, Gestapo, MI6, Mossad, KGB, União Soviética, CIA, Beria, Stasi, Terceiro Reich, Afeganistão, Abwehr, Romanov, Cuba 62, Barbarossa, Heydrich, Valquíria, Nuremberg, GRU, Kempeitai, OSS, NKVD, FBI, FSB, Guarda Revolucionária, MSS. Atlas (31): agências (CIA vs KGB, Mossad, KGB, Gestapo, Stasi, SS, os "vs") e muitos países. Te lo Pinto: 2ª Guerra, KGB, SS, FBI vs CIA, polícia nazista.

**Funcionou × flopou [O]:**
| Funcionou | Views | Flopou | Views |
|---|---|---|---|
| Archive: SS / Gestapo | 684 / 452 mil | Archive: Guarda Revolucionária, FSB, MSS (novos) | 3–14 mil |
| Archive: MI6 / Mossad / KGB | 275 / 272 / 247 mil | Atlas: países (China, Brasil, Japão, Austrália, Canadá, Yemen) | 0,2–0,9 mil |
| Atlas: **CIA vs KGB** | 100 mil (57 v/i) | Atlas: "vs" menos famosos (Mossad vs KGB, CIA vs Mossad, MI6 vs KGB, FBI vs KGB) | 1,7–6 mil |
| Atlas: Mossad / KGB | 86 / 45 mil | Atlas: Las Vegas | 474 |
| Te lo Pinto: KGB / polícia nazista / FBI vs CIA | 246 / 200 / 182 mil | | |
| Archivo Desclasificado: Cuba 62 / Rosenberg / Sorge (48 min) | 268 / 166 / 129 mil | | |

- **O Archive está desacelerando [O]:** vídeos de 17/10–31/10 têm mediana de ~220 mil; os de 01/11–13/11, ~27 mil (ritmo de 1,3–13 mil views/dia contra 8–44 mil). No mesmo período a duração subiu de 9–16 para 15–21 min e os temas ficaram menos famosos. [I] Pode ser cansaço do tema, duração maior ou só tema pior; não dá para separar.
- **Em es, o molde funciona só com agência famosa [O]:** o Atlas faz 45–100 mil com CIA/KGB/Mossad e menos de 1 mil com país. Nosso Mossad (412) e nossa CIA (178) estão no mesmo tema que deu 86 e 100 mil ao Atlas.
- **Título [O]:** Archive "The ENTIRE History of X in N Minutes" (o aposto "Japan's Gestapo"/"the Spies Before the CIA" aparece nos novos e não salvou). Atlas "TODA la Historia de X en N Minutos | subtítulo"; Te lo Pinto "La HISTORIA COMPLETA de X".
- **Thumb [O]** (`grade-archive-in-minutes.jpg`, `grade-atlas-del-tiempo.jpg`): Archive com HQ em tinta, 1 personagem com objeto-símbolo (anel da SS, carta, envelope), sigla gigante + "ANO – ANO" e selo redondo. Atlas no papel sépia: sigla gigante + datas + agente de chapéu/óculos ou líder (Putin no KGB). O **"vs" com 2 rostos** (agente CIA × Putin) foi o melhor do Atlas. Hits e flops do Archive têm a mesma thumb: de novo, quem decide é o tema.
- **Frequência e horário [O]:** Archive publica **todo dia às 18:00–19:00**; Atlas, 17:00–19:00 (com alguns às 9h); Archivo Desclasificado, 17:00 cravado. Todos têm horário fixo.

### 2.3 Em Relevo
**Temas nos 28 d [O]:** Mundo Entrópico: SC, RS encolhendo, ES, litoral do PR, ranking de estados, Roraima, Alagoas, Piauí, MG. Chão do Sul: só a Região Sul (oposto do Brasil, lugares proibidos, Aquífero Guarani, quem ama/odeia o Sul, pinhão). Um Documentário: Terra pré-histórica (os hits de agosto–setembro eram tragédias: Miyako 6,9 mi, Yungay 5,3 mi). The Last Day: "What would happen if…".

**Funcionou × flopou [O]:**
| Funcionou | Views | Flopou | Views |
|---|---|---|---|
| Chão do Sul: Região Sul é o OPOSTO | 736 mil (111 v/i) | Chão do Sul: pinhão | 1,1 mil |
| ME: O que está ACONTECENDO com SANTA CATARINA?! | 447 mil | ME: litoral do Piauí | 6 mil |
| ME: Por que o RS vai começar a ENCOLHER? | 259 mil | ME: Alagoas encolher, Roraima | 23–25 mil |
| ME: Espírito Santo / litoral do PR | 213 / 202 mil | | |
| Chão do Sul: Lugares proibidos do Sul | 158 mil | | |

- **O Sul é o veio [O]:** 6 dos 8 maiores vídeos de mapa-Brasil dos 28 d são sobre o Sul (SC, RS, PR, região). A mesma fórmula com estado do Norte/Nordeste fez 6–25 mil.
- **Título [O]:** "O que está ACONTECENDO com X?!", "Por que X vai começar a ENCOLHER?", "Por que NENHUM outro estado é como X?", "Por que a Região Sul é o OPOSTO…". Pergunta + 1 palavra em caixa alta.
- **Thumb [O]** (`grade-mundo-entrópico.jpg`, `grade-chão-do-sul.jpg`): ME com mapa de satélite escuro, estado em vermelho entre vizinhos verdes, seta e 2–3 palavras ("UM COLAPSO INEVITÁVEL?"); 100% padrão. Chão do Sul com **relevo 3D recortado** (geodo de ametista, aquífero azul) + 3–4 palavras ("O SUL É OUTRO PAÍS"). É a nossa identidade visual, e ela já provou que funciona.
- **Frequência e horário [O]:** ME publica ter/sex às **18:00** (8 de 9); Chão do Sul, 2/sem de manhã ou à tarde.

### 2.4 Clearance Required (lugares-guerra-en)
**Temas nos 28 d [O]:** WTS: Omaha, Normandia, Hacksaw Ridge, B-52 em Hanói, montanha de foguetes de Hitler, submarino japonês no Alasca, Alemanha, Tiger na Bélgica, Cheyenne Mountain, Laos. CWFP: Lincoln, Appomattox, sobrinho de Lee. Long After The Guns: Wake, Tinian, minissubmarinos de Pearl Harbor, Pointe du Hoc, Okinawa, ponte do rio Kwai, Mulberry.

**Funcionou × flopou [O]:**
| Funcionou | Views | Flopou | Views |
|---|---|---|---|
| CWFP: Pictures of Lincoln's Death | 1,09 mi (270 v/i) | CWFP: Appomattox, sobrinho de Lee | 3,7–7,7 mil |
| LATG: **Wake Island Still Closed to Americans** | 529 mil (445 v/i) | LATG: Mulberry, rio Kwai | 0,5–1 mil |
| WTS: Under the Water at Omaha Beach | 348 mil | WTS: Laos, Cheyenne Mountain | 1,6–5 mil |
| Forgotten Fleet: Pink Submarine | 447 mil | Ship Tales: navios de 2ª linha | 0,1–0,9 mil |
| WTS: Still Digging Up Normandy | 136 mil | | |
| WTS: B-52 in a Lake in Hanoi | 54 mil em 4 d (o ritmo mais rápido do canal agora) | | |

- **O tema do nosso Midway/Bikini está provado [O]:** a ilha fechada do Pacífico (Wake) fez 529 mil em 16 dias num canal de 15 dias. Cheyenne Mountain (lugar fechado nos EUA, sem guerra visível) flopou no WTS (5 mil).
- **Título [O]:** "Why Is X Still…?", "What's Still Under…?", "Why Can't You Visit…?", "What Happened To The Real…?". O CWFP usa "…You Weren't Supposed to See" (é o nosso Gettysburg de 16/11).
- **Thumb [O]** (`grade-where-they-stood.jpg`, `grade-long-after-the-guns.jpg`, `grade-civil-war-fine-print.jpg`):
  - WTS: corte hiper-realista (objeto enterrado ou submerso sob a paisagem de hoje) + 2–3 palavras amarelas ("AIMING SINCE 1944").
  - LATG: tela dividida "1941. / TODAY." (P&B × cor), ou foto aérea + "98 NEVER LEFT".
  - CWFP: retrato de arquivo puro, sem texto, e foi 1,09 mi.
- **Frequência e horário [O]:** WTS 2,5/sem (13h–21h); LATG 1/dia na 1ª semana, às 19h.

---

## 3. Clones novos: como cresceram [O]
| Clone | Molde | 1º vídeo | Primeiras semanas (views por vídeo, na ordem) | 1º hit |
|---|---|---|---|---|
| História em minutos | historia-ptbr | 09/10 | 4,1 mil · **25 mil** · 2,7 mil · 711 · **254 mil** · 2,3 mil · **188 mil** · 2,4 mil… (3–4/sem, 30–38 min) | 5º vídeo, dia 10 (Rússia) |
| History Easy Guide | historia-ptbr | 27/10* | 22 mil · 73 mil · **237 mil** · 928 · 107 mil… (3 vídeos em 2 dias; 4/sem + Shorts) | 3º vídeo, dia 1 (1ª Guerra) |
| 4 clones "História em Minutos" de 10/2026 | historia-ptbr | 08–15/10 | 2–1,7 mil no melhor; maioria < 100 (1–2/sem; Portugal, Incas, Inglaterra, KGB) | nenhum |
| Historia Total (es) | dossie/história | 02/10 | 1,7 mil · 13 mil · 4 mil · 644 · **852 mil** (Israel) · 3,7 mil… | 5º vídeo, dia 10 |
| Archivo Desclasificado (es) | dossie (48 min) | 19/10* | 12 mil · **166 mil** · 16 mil · 51 mil · 24 mil · 77 mil · 129 mil · 68 mil · **268 mil** (1/dia, 17h) | 2º vídeo, dia 1 |
| Archivo en Minutos (es) | dossie-es | 29/10 | 355 · 1,8 mil · 1,5 mil · 145 · 544 · 50 · 9 | nenhum (igual a nós) |
| Spies in Minutes (en) | dossie | 31/10 | 50 vídeos em 13 d, mediana 29 | nenhum |
| Chão do Sul | Em Relevo | 24/10* | **736 mil** · 87 mil · 76 mil · 158 mil · 20 mil · 14 mil… | 1º vídeo |
| The Last Day (en) | Em Relevo | 10/07 | 283 mil · 154 mil · 23 mil · **1,58 mi**… | 1º vídeo; o maior no 4º |
| Long After The Guns | Clearance | 29/10 | **529 mil** · 521 · 7 mil · 986 · 21 mil · 1,8 mil · 2,1 mil | 1º vídeo (Wake) |
| Ship Tales | Clearance | 25/09 | 461 · 1,8 mil · 2 mil · 3,3 mil · **395 mil** · **945 mil**… (4–5/sem) | 5º vídeo, dia 14 |
| Civil War Fine Print | Clearance | 07/11 | **1,09 mi** · 7,7 mil · 3,7 mil (+5 Shorts) | 1º vídeo |

- **O 1º hit veio entre o 1º e o 5º longo, até o dia 14**, sempre num tema que já tinha hit em outro canal [O]. Quem não acertou o tema até o 5º vídeo (clones de 10/2026, Archivo en Minutos, Spies in Minutes) continua em 0–2 mil.
- **De onde vem o tráfego [I]:** o hit sai muito acima dos inscritos (v/i de 34 a 445), ou seja, de sugeridos e da página inicial, colado num vídeo grande do mesmo tema (Wake ao lado de Iwo Jima/Midway, Rússia e França em pt ao lado de Genius/HiM, Sul ao lado de Mundo Entrópico). É o mesmo mecanismo que já vemos em nós: o 2º maior tráfego do historia-ptbr é de sugeridos de um vídeo do History Easy Guide sobre o mesmo tema (Brasil, 252 views).
- **Depois do hit, o resto cai 10–100× [O]** (Long After The Guns 529 mil → 0,5–21 mil; clone pt 254 mil → 0,6–2,5 mil). Chão do Sul é a exceção (piso de 14–158 mil), porque ficou no mesmo veio (Sul).
- \* Canal antigo renomeado ou relançado.

---

## 4. Cruzamento com nossas métricas
Fontes: `relatorios/metricas/2026-11-14.md`, `youtube.studio_video` (export de 09/11), `youtube.alcance_diario` (Reporting API, só 10/11), `youtube.analytics_video_dia`.

| | historia-ptbr | dossie-es | Em Relevo | Clearance |
|---|---|---|---|---|
| Longos no ar / dias de canal [O] | 7 / 11 d (+França 15/11, Alemanha 16/11) | 6 / 10 d (+SS, Inquisición) | 2 / 3 d (+3 agendados) | 1 / 1 d (+Bikini, Gettysburg) |
| Ritmo [O] | ~4,5/sem | ~4/sem | ~5/sem planejado | ~3 em 4 d |
| Ritmo da referência [O] | Genius 1,5 · clone pt 2,25 · HEG 4,25 | Archive 6,5 · Atlas 7,75 | 2–2,25 | WTS 2,5 |
| Melhor vídeo nosso [O] | Egito 380 | Mossad 412 | Sul 15 | Midway 12 |
| Mesmo tema na referência [O] | Egito: HiM 571 mil (09/2026); clone pt 2,7 mil | Mossad: Archive 272 mil, Atlas 86 mil | Sul: Chão do Sul 736 mil, ME SC 447 mil | Ilha do Pacífico: Wake 529 mil |
| Impressões [O] | Egito 920 + Índia 1.273 (Studio até 08/11); canal 1.124 (Reporting, 10/11) | Mossad 5.521 (Studio); 204 (10/11) | sem dado ainda | sem dado ainda |
| CTR [O] | 3,7–4,0% (Studio); 6,3% no dia 10/11 | 2,3% (Studio); 5,9% no dia 10/11 | — | — |
| Retenção [O] | 42% (7,5 min/view) | 56% (7,4 min/view) | — | — |
| Tráfego [O] | 47% página inicial/feed (SUBSCRIBER na API), 44% sugeridos, 4% busca | 65% sugeridos, 20% página inicial, 9% busca ("mossad") | — | — |

- **Ritmo [O]:** já postamos tanto quanto os clones que deram certo, e mais que os canais-modelo de pt/en. Ritmo não é o gargalo. O Archive (6,5/sem) e o Atlas (7,75/sem) postam mais, mas o Atlas, com 7,75/sem, tem mediana de 1,2 mil: frequência sozinha não leva a lugar nenhum.
- **Temas [O]:** acertamos temas que funcionaram (Egito, Índia, Rússia, França, Alemanha no pt; CIA, Mossad, KGB, SS no es; Sul e ilha fechada nos outros dois). Diferença de alcance: o hit deles tem de 100 mil a 700 mil views, o nosso de 400. [I] Com CTR de 4–8%, um hit de 250 mil precisa de ~3–6 milhões de impressões; nós tivemos ~1–5 mil por vídeo. **O gap é de ~1.000× em impressões, não em CTR.**
- **CTR e retenção (nossos vs deles) [I]:** o CTR e a retenção deles não são públicos. O que dá para inferir: os hits deles saem na 1ª semana (vídeos com 3–7 dias já em 50–500 mil), então o YouTube testou o vídeo com um público grande cedo. Nossos 42–56% de retenção e 4–7% de CTR estão na faixa de canal saudável (**Hipótese**: 35–50% de retenção e 4–8% de CTR, faixa comum de documentário). O nosso problema é o **tamanho do teste** que o YouTube faz em canal com 3–14 inscritos, não a nota do vídeo.
- **O que já se repete em nós [O]:** 1 vídeo puxa o canal (Egito 44% das views do historia-ptbr; Mossad 53% do dossie-es), e o sugerido vem de um vídeo do mesmo tema num canal vizinho (History Easy Guide → nosso Brasil e Roma; Atlas/Archive → Mossad). Encaixa com a regra que a pauta de 13/11 já seguiu ("escolher o tema que os vizinhos estão rodando agora").
- **Horário [O]:** os nossos saem em horários soltos (historia-ptbr de 09:00 a 20:42; dossie-es de 09:00 a 20:10). Todas as referências fortes têm horário fixo (Genius 09:30; Archive 18–19h; Mundo Entrópico 18h; Archivo Desclasificado 17h). [I] O efeito do horário em canal novo é pequeno; o custo de fixar é zero.

---

## 5. Recomendações (todas **Hipótese**; o número que justifica vai junto)

### historia-ptbr
1. **Tema pelo que um vídeo pt está rodando agora**, não só pela busca: Rússia (254 mil) e França (188 mil) no clone, e os nossos sugeridos vêm de vizinhos com o mesmo tema. Antes de cada pauta, olhar os 28 d do clone de 08/2026, do HEG e do Genius (`scripts/coletar.py`, ~15 unidades por canal).
2. **Próximos países com sinal [O]:** **Estados Unidos** (Genius 541 mil, 10/2026) e **Ucrânia** (clone pt 25 mil, HiM 180 mil; risco da guerra atual: fechar em 1991 + 1 frase neutra). **Evitar Japão** (flop em 3 canais nos 28 d) e Austrália em pt (2,4 mil).
3. **Testar 1 guerra mundial** ("A história INTEIRA da Primeira Guerra Mundial em N minutos"): HEG 237 mil e 107 mil em pt, com bonequinho igual ao nosso. **Fora do nicho da bíblia (países/impérios): só com OK do Rodrigo.**
4. **Thumb:** no estilo "Bonecos", copiar a gramática do HEG: frase de 3–4 palavras com verbo ("1 TIRO E O MUNDO EXPLODIU") + etiqueta com o tema. No estilo HiM, testar o **líder atual** como figura (os 2 hits do clone: Putin e Macron). Medir no "Testar e comparar".
5. **Ritmo 3–4/sem num horário fixo** (sugestão: 09:30, como o Genius, ou 18:00): já postamos mais que o Genius (1,5/sem) e o clone (2,25/sem).

### dossie-es
1. **Gestapo como próximo vídeo** (backlog 008): Archive 452 mil; Te lo Pinto "policía nazi" 200 mil; Archivo en Minutos 1,8 mil (o melhor dele). Cluster nazista é o mais quente nos 3 canais.
2. **1 episódio "CIA vs KGB"** (o melhor do Atlas, 100 mil; Te lo Pinto FBI vs CIA 182 mil) com thumb de 2 rostos. Só o par mais famoso: os outros "vs" do Atlas fizeram 1,7–6 mil. Formato novo: precisa do OK do Rodrigo.
3. **Ficar em agência ou organização famosa; nunca país** (Atlas: país < 1 mil, agência 45–100 mil). Cartéis seguem com o risco já anotado no backlog.
4. **Horário fixo 18:00–19:00 BRT** (Archive e Atlas; público MX/AR/ES às 15–23h locais).
5. **Não acelerar além de 3–4/sem**: Spies in Minutes (12,5/sem, mediana 29) e o Archive caindo de ~220 mil para ~27 mil de mediana em novembro mostram que o volume e a saturação do molde cobram.

### Em Relevo
1. **Série-âncora do Sul** (SC, RS, PR, Aquífero Guarani, "o Sul é outro país", temporais): Chão do Sul 736 mil e 158 mil; ME SC 447 mil, RS 259 mil, PR 202 mil. A fórmula com o Norte/Nordeste fez 6–25 mil.
2. **Título no padrão que funcionou:** "O que está ACONTECENDO com X?!" e "Por que X vai começar a ENCOLHER?" (447 e 259 mil); nosso "O que está acontecendo com o clima no Sul do Brasil?" já está perto, falta a palavra em caixa alta.
3. **Thumb:** o estado aceso em vermelho entre vizinhos verdes, ou o recorte 3D (geodo, aquífero), + 2–4 palavras em pergunta (ME e Chão do Sul: 100% dos hits).
4. **Desastre reconstruído como formato longo:** Um Documentário fez 2,6–6,9 mi por tragédia (ago–set). Nossa Grande Seca de 1877 é esse formato: medir contra o Sul.
5. **2–3 por semana com horário fixo** (ME ter/sex 18h) bastam: temos 5 em ~6 dias. O canal não tem bíblia em `canais/` (vive em `pesquisa/canal-clima-2026-11/`): o título e a thumb acima entram lá quando o Rodrigo aprovar.

### Clearance Required
1. **Série das ilhas e bases fechadas do Pacífico** depois de Midway e Bikini: Wake 529 mil em 16 dias (canal de 15 dias). Wake já tem dono; candidatos do mesmo tipo: Johnston Atoll, Kwajalein, Tinian (LATG 21 mil). Fatos e acesso a conferir no roteiro.
2. **Objeto da guerra que ainda está lá** (WTS: Omaha 348 mil, Normandia 136 mil, B-52 em Hanói 54 mil em 4 dias; Forgotten Fleet: Pink Submarine 447 mil) é a 2ª linha. Lugar fechado sem guerra visível (Cheyenne 5 mil) flopou.
3. **Thumb:** testar "1944. / TODAY." em tela dividida (LATG) ou o corte com o objeto enterrado/submerso + 2–3 palavras amarelas (WTS). Para Gettysburg, o retrato de arquivo sem texto do CWFP (1,09 mi) é o controle do teste.
4. **2–2,5 longos/sem** (WTS 2,5; LATG 1,75), num horário fixo à tarde nos EUA (13–19h BRT).
5. **Se o 1º hit não vier até o 5º longo, trocar o tema, não o ritmo** (Ship Tales: hit no 5º e no 6º; os clones literais do Iwo Jima continuam com mediana de 28 views).

---

## Limitações
- Views do dia 14/11; vídeos com menos de 3 dias ainda vão subir (por isso os "piores" só contam vídeos com 3 dias ou mais).
- Shorts = até 3 min pela duração (a API não marca Short).
- Canal antigo que apagou vídeos aparece mais novo do que é (\* nas tabelas).
- Nossas impressões: só o export do Studio até 08/11 e 1 dia de Reporting API (10/11). CTR e retenção das referências não são públicos: tudo o que diz respeito a eles no §4 é inferido.
- O vínculo hit ↔ sugerido do vizinho é inferência pelo v/i e pelo nosso próprio tráfego; não temos o tráfego deles.
