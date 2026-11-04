# LEVANTAMENTO: nicho "Archive in Minutes" (história inteira de organizações em N minutos)

Data: 2026-11-04 · Brief: `~/workspace/referencias/BRIEF-canal-archive.md` · Dados brutos: `pesquisa/archive-in-minutes/dados.json` · Thumbs: `pesquisa/archive-in-minutes/thumbs/` (fora do git) · Vídeos assistidos: `pesquisa/tendencias/assets/2026-11-04/<id>/` e `youtube.assistidos`.
Legenda: **[O]** = observado (API, frames, transcrição) · **[I]** = inferido/estimativa.

---

## Resumo executivo

> **Atualização 2026-11-04 (noite):** a recomendação de idioma abaixo (pt-BR) foi **substituída** por `IDIOMA.md`. O canal sai em **espanhol** (`canais/dossie-es/`), com o francês em 2º; o pt-BR ficou em 3º. Pastas citadas como `canais/dossie-ptbr/…` agora estão em `canais/dossie-es/arquivo-ptbr/`.

**Recomendação: TESTAR, em pt-BR, num canal novo** (slug `dossie-ptbr`, nome sugerido **Dossiê em Minutos**). Fórmula: "A história INTEIRA da <organização> em N minutos", com 10 a 16 min, ilustração em quadrinho e hook por anedota datada. O piloto é **a KGB**. Depois, fazer 3 vídeos em 2–3 semanas e decidir com número (critério abaixo).

**Por que TESTAR, e não INVESTIR:**
- A demanda está provada: Archive in Minutes fez 1,95 mi de views em 21 dias, cerca de 2,8 mi por mês [O/I].
- O inglês já saturou: 14 clones surgiram em 3 semanas e quase todos ficam abaixo de 2 mil views por vídeo [O].
- Em pt-BR não existe canal com a fórmula aplicada a organizações [O]. Mas o mercado é menor, o RPM vale ~0,3× o do inglês e o nosso `historia-ptbr` ainda tem 6–17 views por vídeo, então a demanda em pt-BR **para nós** não está provada.

**Números-chave**
| | |
|---|---|
| Canais mapeados | **56** (15 buscas `search.list`, ~1.700 unidades de cota) [O] |
| Vídeos assistidos | **10** de **7 canais** (watch.py, via WARP) [O] |
| Archive in Minutes | 1º vídeo em 14/10; 19 vídeos (1/dia); 1,95 mi de views; 13,2 mil inscritos; mediana de 86 mil views/vídeo; duração média de 13 min [O] |
| Tema pesa mais que tudo | Organizações famosas (Gestapo, SS, KGB, Mossad, CIA, Stasi, MI6): **mediana de 146 mil**. Eventos/estados (Titanic, Romanovs, Barbarossa, Muro, Afeganistão): **mediana de 38 mil** [O] |
| Clones em inglês | 14 canais copiando o template desde 10/2026. Melhor vídeo: 9,8–25 mil; mediana < 1 mil [O] |
| Concorrência pt-BR | 0 canais com a fórmula para organizações. Há demanda por nazismo/espionagem em pt: Fragmentos da História teve 212 mil views com "Hiena da Gestapo" [O] |
| Receita pt-BR (estimativa) | US$ 0–300/mês nos 3 primeiros meses. Se pegar (10–20% das views do Archive): **US$ 280–1.560/mês** [I] |
| Custo por vídeo (nossa pipeline) | ~US$ 7–9 direto (Fish ~US$ 0,25 + ~170 imagens `medium` ~US$ 7 + thumb). O visual do Archive é quase o mesmo da nossa pipeline [I, base em `conhecimento/anti-padroes.md`] |

**Critério para passar a INVESTIR** (após 3 vídeos e 14 dias do 1º): média ≥ 3 mil views/vídeo **ou** 1 vídeo ≥ 15 mil, com % assistido ≥ 35%. Abaixo de 500 views/vídeo em média: DESCARTAR ou trocar o idioma para es [I, proposta].

**Próximos passos (decisão do Rodrigo)**
1. Aprovar o nome e criar o canal no YouTube. Os handles `@dossieemminutos`, `@dossieinteiro` e `@arquivomortohistoria` estavam livres em 04/11 (channels.list forHandle).
2. Escolher a voz: sugestão de uma voz pt-BR **diferente** da do `historia-ptbr`, grave e sóbria.
3. Dar o OK para produzir o piloto (roteiro pronto em `canais/dossie-ptbr/videos/001-kgb/SCRIPT.md`; teto de US$ 10).

---

## 1. Mapa de concorrência

Método [O]: 15 buscas (en: Gestapo, KGB, CIA, Mossad, Stasi, SS, Legião Estrangeira, máfia; pt: KGB, Gestapo, "a história INTEIRA em minutos"; es: KGB, Gestapo; fr: KGB; de: Stasi). Para cada canal candidato: channels + playlistItems + videos (lista completa até 50 vídeos).
Views/mês [I]: para canal com < 1 ano, views ÷ idade × 30. Para canal antigo, a soma dos vídeos longos dos últimos 90 dias ÷ 3. "Licensed" = `contentDetails.licensedContent`, indício (não prova) de canal com parceiro/YPP.

### 1a. Fórmula exata ("ENTIRE/COMPLETA/TODA la historia de <X> em N minutos"), canais novos
| Canal | Idioma | 1º vídeo (idade) | Vídeos | Views | Inscritos | Views/mês [I] | Ritmo | Melhor vídeo | Mediana | Monetização [I] |
|---|---|---|---|---|---|---|---|---|---|---|
| [Archive in Minutes](https://www.youtube.com/channel/UCFp0Rk-ad8JD78Qw9nEJ29w) | en | 14/10 (21 d) | 19 | 1.949.073 | 13.200 | **~2,8 mi** | 1/dia | Gestapo 349 mil | 86 mil | elegível; licensed=true em todos; anúncios na página → **provavelmente monetizado** |
| [CountryCorns](https://www.youtube.com/channel/UCKWRnsyYbPFgWclCF0_yOTw) | en | 27/09 (38 d) | 5 | 1.390.407 | 7.500 | ~1,1 mi (82% de 1 vídeo) | irregular | Israel 1,14 mi | 131 mil | elegível, não confirmado |
| [History in Minutes](https://www.youtube.com/channel/UCYjRQ6T2BxBnJtPytI9OnNg) | en | 11/09 (54 d) | 8 | 1.444.864 | 16.500 | ~0,8 mi | ~1/semana | Índia 614 mil | 90 mil | elegível, não confirmado |
| [Genius History](https://www.youtube.com/channel/UC-q0RDBWjYlYA2KkPzq0WSQ) | en | 15/06 (142 d) | 16 | 3.507.126 | 34.200 | ~0,74 mi | ~1/semana | Irã 927 mil | 98 mil | provavelmente monetizado |
| [Ziro History](https://www.youtube.com/channel/UC0D2w4MJDTzx8ceT1YSbiTw) | en | 06/10 (29 d) | 33 | 2.327.508 | 21.300 | ~2,4 mi | >1/dia | Rússia (45 min) 333 mil | 42 mil | elegível; variante longa (35–50 min) |
| [Prima Historian](https://www.youtube.com/channel/UCWh76g3H7IYBqcnvdgDog9w) | en | 25/10 (10 d) | 3 | 358.559 | 4.320 | não confiável | — | Israel 375 mil | 1 mil | ainda não elegível |
| [Atlas del Tiempo](https://www.youtube.com/channel/UCku9KB11TReyHHC1kK9CCEw) | es | 08/10 (27 d) | 27 | 81.434 | 729 | ~90 mil | 1/dia | Mossad 32,5 mil | 747 | ainda não elegível |
| [Historia Total](https://www.youtube.com/channel/UC6ZUELsUCkrHF5ZO4m4hpMQ) | es | 02/10 (33 d) | 13 | 743.120 | 1.590 | ~0,68 mi (1 hit) | ~3/semana | Israel 736 mil | 639 | elegível, não confirmado |
| [Abre la Historia](https://www.youtube.com/@abrehistoria) | es | 20/10 (15 d) | 7 | 51.548 | 281 | ~100 mil (1 hit) | ~3/semana | Israel 49 mil | 591 | não elegível |
| [Cronopaís](https://www.youtube.com/@cronopais9) | es | 17/10 (18 d) | 9 | 34.084 | 154 | ~57 mil | ~3/semana | Alemanha 19,8 mil | 1 mil | não elegível |
| [Siglos y Fronteras](https://www.youtube.com/@siglosyfronteras) | es | 21/10 (14 d) | 12 | 18.806 | 254 | ~40 mil | ~1/dia | Haiti 17,5 mil | 128 | não elegível |
| [Historia Ágil](https://www.youtube.com/@남이경진-z7g) | es | 11/10 (24 d) | 13 | 21.703 | 109 | ~27 mil | ~4/semana | Roma 17,8 mil | 511 | não elegível |
| [Historia con Monóculo](https://www.youtube.com/@historiaconmonoculo) | es | 29/10 (6 d) | 7 | 3.850 | 31 | — | 1/dia | Irã 4,4 mil | 357 | não elegível |
| [Traço Curioso](https://www.youtube.com/@traco-curioso) | pt | 15/06 (142 d) | 64 | 742.989 | 7.280 | ~157 mil (1 hit) | ~3/semana | História do Mundo 610 mil | 541 | elegível, não confirmado |
| [History Easy Guide](https://www.youtube.com/@historyeasyguide) | pt | 27/10 (8 d) | 13 | 33.458 | 369 | — | >1/dia | 1ª Guerra (17 min) 24 mil | 1,4 mil | não elegível |
| [Depois do Poder](https://www.youtube.com/@depoisdopoder) | pt | 24/09 (41 d) | 2 | 11.845 | 132 | — | — | França 11,5 mil | — | não elegível |
| [Canal Outro Ponto](https://www.youtube.com/@canaloutroponto) | pt | 27/07 (100 d) | 11 | 18.243 | 115 | — | — | Roma 8,7 mil | 637 | não elegível |

### 1b. Clones do template do Archive em inglês (todos de 09–10/2026) [O]
| Canal | Vídeos | Views | Melhor | Mediana |
|---|---|---|---|---|
| [The Org Files](https://www.youtube.com/@theorgfiles) | 13 | 28.313 | Mossad 24 mil | 255 |
| [Last Empire](https://www.youtube.com/@lastempire02) | 36 | 37.928 | Nazi Germany 24,8 mil | 309 |
| [Fuse Room](https://www.youtube.com/@fuse-room) | 10 | 15.746 | KGB 9,8 mil | 856 |
| [Agent Curious](https://www.youtube.com/@agentcurious-am) | 35 | 12.923 | CIA 9,4 mil | 65 |
| [Mr. Zombi](https://www.youtube.com/@mr.zombitv) | 28 | 12.219 | YouTube 8,6 mil | 179 |
| [Rewind the World](https://www.youtube.com/@rewindtheworld-j2p) | 14 | 7.473 | Kim Jong Un 2 mil | 323 |
| [Echoes of Empire HQ](https://www.youtube.com/@echoesofempireofficial-g8l) | 28 | 11.945 | Mossad 3,2 mil | 211 |
| [Before Lore](https://www.youtube.com/@beforeloreyt) | 11 | 4.411 | CIA 1,9 mil | 277 |
| [History Behind the Story](https://www.youtube.com/@historybehindthestory) | 14 | 3.394 | KGB 1,4 mil | 114 |
| [Empire Uncovered](https://www.youtube.com/@empireuncovered-c5w) | 21 | 1.018 | CIA 322 | 7 |
| [Past in Chapters](https://www.youtube.com/@survivethepast-z2y) | 7 | 738 | CIA 535 | 101 |
| [Spies in Minutes](https://www.youtube.com/@spiesinminutes) | **23 em 4 dias** | 574 | Cheka 171 | 23 |
| [The Vault in Minutes](https://www.youtube.com/@historyvaultshow) | 4 | 246 | MI6 168 | 125 |
| [The Past In Minutes](https://www.youtube.com/@thepastminutes) | 8 | 35 | Mossad 36 | 0 |
| [Cold Cabinets](https://www.youtube.com/@thecoldcabinets) | 4 | 456 | KGB 287 | 178 |

**Leitura [I]:** o algoritmo recompensou o 1º canal a acertar a combinação "organização sombria + quadrinho + 1/dia". Os clones que entraram depois com os mesmos temas (KGB, CIA, Mossad) não pegaram. Entrar em inglês hoje seria ser o 16º clone.

### 1c. Mesmo nicho (serviços secretos, nazismo, Guerra Fria), formatos diferentes [O]
| Canal | Idioma | Vídeos | Inscritos | Views/mês [I] | Observação |
|---|---|---|---|---|---|
| [Into the Shadows](https://www.youtube.com/@intotheshadows) | en | 585 | 1,3 mi | ~6,2 mi | "How the Gestapo Actually Worked" (1,04 mi); 25–40 min; prova do teto do nicho |
| [Simplicissimus](https://www.youtube.com/@simplicissimus) | de | 524 | 2,6 mi | ~13,7 mi | "Die Wahrheit über die Stasi"; gigante; nenhum clone da fórmula em alemão |
| [Te lo Pinto](https://www.youtube.com/@telopintofacil) (aparece como "Mr Sticky") | es | 310 | 594 mil | ~6,1 mi | "La HISTORIA COMPLETA de la KGB" (36 min): 138 mil em 5 dias, remodelando os beats do Archive |
| [Historia Incomprendida](https://www.youtube.com/@historiaincomprendida) | es | 1.766 | 4,46 mi | ~3,3 mi | biografias e crimes, 28 min |
| [The War Economy](https://www.youtube.com/@thewareconomyyt) | en | 21 | 1.310 | ~0,2 mi | "The Mossad Explained" 160 mil (1 hit) |
| [Fragmentos da História](https://www.youtube.com/@fragmentosdahistoriaoficial) | **pt** | 196 | 24.100 | ~46 mil | Hiena da Gestapo 212 mil; nazistas/SS em 25–70 min, foto real |
| [Histórias Romanas](https://www.youtube.com/@historiasromanas) | **pt** | 1.006 | 295 mil | ~0,66 mi | prova que história militar em pt-BR escala |
| [Total History](https://www.youtube.com/@_totalhistory) | **pt** | 67 | 72.500 | ~0,1 mi | "Por que ninguém atacou Portugal na 2ª Guerra?" 2,2 mi |
| [Classé Secret Défense](https://www.youtube.com/@classesecretdefense) | fr | 99 | 5.170 | ~80 mil | DGSE/CIA/Mossad em entrevista; demanda em fr |
| [Archives Soviétiques](https://www.youtube.com/@archivessovietiques) | fr | 52 | 3.300 | ~65 mil | KGB narrado, 52 min; 62,7 mil no melhor vídeo |
| [Historias Reales de Espías](https://www.youtube.com/@spyhistory_es) / [Histoires Vraies d'Espions](https://www.youtube.com/@spyhistory_fr) | es/fr | 73 | 8.080 / 4.700 | 14 mil / 5 mil | mesmo dono, dublado; narrativa longa |
| [Klaus](https://www.youtube.com/@klausanimationyt) | en | 128 | 28.400 | ~0,49 mi | "Explained like you're 5" |
| [Der Panzer](https://www.youtube.com/@derpanzerdocumentaries), [The Soldier's Diary](https://www.youtube.com/@thesoldierdiaryeng), [Nazi Tales](https://www.youtube.com/@nazitales8998) | en | 60–154 | 12–27 mil | — | documentário colorizado longo (40–60 min) |

Lista completa (56 canais, com `calc` por canal): `dados.json` → `canais`.

---

## 2. Anatomia do formato

Vídeos assistidos [O] (`youtube.assistidos`, 2026-11-04):
| ID | Canal | Título | Duração | Views | Cortes/min no início |
|---|---|---|---|---|---|
| pbIzG1QvoWs | Archive in Minutes | The ENTIRE History of the Gestapo in 12 Minutes | 12:26 | 348 mil | 20 |
| PmpWyltn08s | Archive in Minutes | The ENTIRE History of the SS in 16 Minutes | 16:18 | 317 mil | 19 |
| VNJhu4rh6OY | Archive in Minutes | The ENTIRE History of the KGB in 13 Minutes | 13:51 | 236 mil | 18 |
| T9ruitgpvJQ | Archive in Minutes | The ENTIRE History of the Abwehr in 16 Minutes (flop) | 16:31 | 33 mil | 22 |
| ihGK1iyUN1E | CountryCorns | The ENTIRE History of Israel in 10 Minutes | 8:46 | 1,14 mi | 12 |
| by7uTDjSx7Y | Te lo Pinto / Mr Sticky (es) | La HISTORIA COMPLETA de la KGB | 36:04 | 138 mil | 11 |
| 9LyvAHVecwY | Atlas del Tiempo (es) | TODA la Historia del Mossad en 17 Minutos | 17:28 | 32,5 mil | 6 |
| uBRJbDwWc9Q | Fuse Room (clone en) | The ENTIRE History of the KGB in 15 Minutes | 15:00 | 9,8 mil | 14 |
| IE3zeXlWQlg | The War Economy | The Mossad Explained | 22:02 | 160 mil | 3 |
| cai8w5aap68 | The Org Files (clone en) | The ENTIRE History of Mossad in 25 Minutes | 25 min | 24 mil | — (só hook) |

### 2a. Títulos
- **[O]** Archive usa sempre o mesmo molde: "The ENTIRE History of [the] <X> in N Minutes", com ENTIRE em caixa alta e N igual à duração arredondada (9–20). X tem **1 a 3 palavras** (sigla ou nome próprio: KGB, SS, MI6, Beria).
- **[O]** Performa: organizações de **repressão/espionagem com nome famoso**. Gestapo 349 mil, SS 317 mil, KGB 236 mil, Mossad 146 mil, CIA 141 mil, Soviet Union 126 mil, Cold War 117 mil, Stasi 114 mil, MI6 109 mil, Beria 86 mil.
- **[O]** Flopa: organizações que o público não conhece (NKVD 22 mil, Abwehr 33 mil), eventos pontuais ou temas fora do eixo (Titanic 11 mil, Romanovs 36 mil, Barbarossa 34 mil, Berlin Wall 40 mil, Soviet-Afghan War 24 mil). FSB (20 min) tinha 4,5 mil com 1 dia.
- **[I]** O gatilho é "instituição temida + promessa de completude curta". Sigla curta e famosa é o melhor X. Vídeos acima de ~17 min não ajudam: os de 16–20 min do Archive estão espalhados entre hits e flops, e os de 31–36 min da Prima Historian ficaram em ~1 mil.
- **[O]** Em espanhol, o molde vira "TODA la Historia de X en N Minutos" ou "La HISTORIA COMPLETA de X", às vezes com subtítulo ("| El Servicio Secreto Más Temido del Mundo"). Em português (Traço Curioso, Depois do Poder, History Easy Guide): "A História do X em N Minutos" / "Toda a História da França em 11 Minutos".

### 2b. Thumbnails ([O], mosaico em `thumbs/_mosaico-archive-por-views-dia.jpg`)
- **Composição fixa no Archive (19 de 19):** personagem-ícone da organização em meio corpo à **esquerda** (chefe ou agente arquetípico: Himmler, Putin, Dulles, agente de fedora), cenário reconhecível ao fundo (Lubyanka, prédio da Gestapo, castelo de Wewelsburg), **nome em caixa alta gigante, preto, serifado/slab** no canto superior direito, período "AAAA – AAAA" logo abaixo e um **ícone-selo redondo** ao lado do nome (anel, envelope, emblema, bandeira).
- **Cores:** céu azul-claro chapado, paleta realista dessaturada, contorno preto grosso de quadrinho. Nenhuma suástica visível; os uniformes são estilizados.
- **Objeto na mão** do personagem conta o tema: anel de caveira (SS), carta (Gestapo), pasta com estrela (KGB), cachimbo e documentos (CIA).
- **Atlas del Tiempo (es)** copia o template, com fundo pergaminho sépia e nome do canal no topo. **Te lo Pinto (es)**: o mesmo layout (Putin + Lubyanka + "KGB 1917–1991"). **CountryCorns**: líder em cartoon apontando, palavra amarela e datas em pílula vermelha.
- **[I]** A thumb é um "pôster de filme" com 1 rosto, 1 palavra e 1 data. É reconhecível na grade e legível no celular.

### 2c. Hook (primeiros ~20 s, transcrição real) [O]
- **Gestapo:** "In 1943, a war widow tells a colleague at her munitions factory a joke. Hitler wants to cheer up Berlin, and Göring tells him to jump off the radio tower. The colleague reports her. She is put to death. This is the entire history of the Gestapo, and how a small police force watched 80 million people."
- **SS:** "In the spring of 1945, on Heinrich Himmler's orders, thousands of silver rings with a skull on them are hidden inside a hillside near a castle in Western Germany. Then, the story goes, the entrance is blown shut. Each ring belonged to a dead SS man. They have never been found. This is the entire history of the SS."
- **KGB:** "December 1989, Dresden. A KGB officer burns files so fast the furnace bursts. A crowd is at the gate. He calls for help, and the answer is: Moscow is silent. His name is Vladimir Putin. This is the entire history of the KGB, from 40 men to an empire of secrets, and why it never died."
- **Abwehr (flop):** "In July 1944, Hitler approves an iron cross for Germany's best spy in Britain… None of those agents exist, and the spy works for the British. This is the entire history of the Abwehr." É o mesmo molde de hook, com 10% das views: **o tema decide, não o hook** [I].
- **Atlas del Tiempo (es) e The Org Files (en), Mossad:** os dois abrem com a captura de Eichmann ("Buenos Aires, 11 de mayo de 1960…"). Os clones copiam a mesma anedota.
- **Fuse Room (clone):** "Moscow, 1971. A man steps out of his apartment building…". É uma cena genérica sem nome nem fato verificável, e teve 9,8 mil views [I: perde força].
- **Técnica [I]:** (1) data + lugar; (2) cena humana concreta em 2–4 frases curtas no presente; (3) **desfecho seco ou reviravolta** ("She is put to death." / "His name is Vladimir Putin." / "They have never been found."); (4) a frase do título ("This is the entire history of X"); (5) uma promessa ou pergunta em 1 linha. **Tudo em 15–22 s**, bem mais curto que o nosso hook do `historia-ptbr` (45 s). Às vezes o vídeo volta a essa cena no fim.

### 2d. Roteiro e estrutura [O]
- **Capítulos-objeto:** 13–17 capítulos de 40–70 s, com títulos de 1–2 palavras e artigo ("The joke", "The stamp", "The card index", "The cellar", "The rings"). Cada capítulo é **uma cena ou objeto concreto** com data. O KGB usa "lugar, ano" ("Dresden, 1989", "The Cheka, 1917") e tem 8 capítulos.
- **Cronologia estrita** depois do hook (fundação → auge → crimes → queda → herança). O **fechamento volta ao objeto do hook** (SS: "The skull rings" → "The rings"; Gestapo: "The joke" → "The cellar") [O pelos capítulos; I pelo payoff].
- **Narração no presente histórico**, frases curtas e factuais, números exatos ("about 40 officials, working from the fourth floor… Gorokhovaya Street, number two"). Quase sem adjetivo; o horror vem do fato.
- **Ritmo da fala [I]:** ~160–170 palavras/min. Um vídeo de 13 min ≈ 2.100 palavras na fala deles. No nosso ritmo com pausas (~135 palavras/min), 13 min ≈ **1.750 palavras**.
- Sem CTA no meio, sem "inscreva-se" no hook e sem patrocínio [O, transcrições].

### 2e. Edição [O, hook_sheet e video_sheet]
- **Visual:** ilustração de IA em quadrinho/graphic novel, contorno preto grosso, cores realistas dessaturadas, iluminação de cena (lareira, neve, luz de luminária). Personagens adultos com rosto reconhecível (Putin, Lenin, Dzerzhinsky): **não** é o bonequinho do `historia-ptbr`.
- **Cortes:** 18–22 por minuto no 1º minuto (Archive), contra 6–14 nos concorrentes que flopam. Ken Burns leve.
- **Texto na tela:** rótulo em letra de mão maiúscula, escura e com **sublinhado vermelho** ("DRESDEN, 1989", "PERMISSION TO MARRY", "THE SKULL RING", "30,000+ ALIVE") em ~1/3 dos planos. Cartão de capítulo com a mesma tipografia.
- **Mapas:** mapa bege simples, sem rótulos de fundo, com pino vermelho e seta animada ("PETROGRAD" → "MOSCOW").
- **Voz:** narrador masculino em inglês, neutro, grave e constante. É provavelmente TTS de alta qualidade ou clone [I: sem respiração audível, ritmo regular]. Música de fundo discreta [I: não medida].
- **Legenda queimada:** não no Archive. O Atlas del Tiempo usa, e o ritmo dele (6 cortes/min) é bem mais lento.

### 2f. Cadência e crescimento [O/I]
- Archive: **1 vídeo por dia** desde 14/10 (19 em 21 dias), sempre ~13 min. O canal foi criado em 30/09 e a descrição promete "every one of these stories… you can see all of it in photographs" [O].
- Explicação do crescimento [I]: (1) volume diário para testar temas e deixar o algoritmo achar os hits (KGB no dia 5, Gestapo no dia 13); (2) template de thumb idêntico, que gera reconhecimento na barra lateral; (3) temas com busca perene e curiosidade "sombria"; (4) sessão longa, porque um vídeo puxa o outro (SS → Gestapo → KGB → Stasi); (5) provável mesma operação do History in Minutes/Genius History (mesmo molde de título e país US) [I, não confirmado].

---

## 3. Oportunidade

### 3a. Idioma
| Mercado | Saturação [O] | RPM história [I] | Leitura |
|---|---|---|---|
| **en** | **Alta**: Archive domina e 14 clones fracassam | US$ 4–8 (nazismo/violência: provável corte por anúncio limitado) | Não entrar com a mesma fórmula |
| **es** | Média-alta: 8 canais novos com a fórmula desde 10/2026 (quase todos < 1 mil de mediana); Te lo Pinto já fez KGB | 0,25–0,4× → US$ 1–3,2 | Segunda opção, se o pt-BR funcionar |
| **pt-BR** | **Baixa**: nenhum canal com organizações; só países/mundo (Traço Curioso, Depois do Poder, History Easy Guide, nosso `historia-ptbr`) | 0,25–0,35× → US$ 1–2,8 | **Entrar agora** (janela de primeiro a chegar) |
| fr | Baixa na fórmula; demanda existe (Classé Secret Défense, Archives Soviétiques) | 0,5–0,7× → US$ 2–5,6 | Opção futura; não temos voz fr paga |
| de | Nenhum clone; Simplicissimus domina o tema | ~0,8–1× [I] | Fora do nosso alcance de idioma/revisão |

**Recomendação:** pt-BR. É o único mercado grande sem a fórmula, nossa pipeline e revisão já são em pt, e o `historia-ptbr` serve de laboratório para as mesmas skills.

### 3b. Projeção (estimativa, em faixa) [I]
- Archive: 2,8 mi views/mês × US$ 4–8 → ~US$ 11–22 mil/mês (se monetizado e sem limitação de anúncios).
- **Nossa versão pt-BR:** cenário conservador de 10–20% das views do Archive (280–560 mil/mês) × RPM US$ 1–2,8 → **US$ 280–1.560/mês** depois do YPP (1.000 inscritos + 4.000 h). Para 4.000 h com vídeos de 13 min a 40% de retenção, são precisas ~46 mil views [I].
- Cenário realista dos 2 primeiros meses: 0–50 mil views, **sem receita**. O custo direto é de ~US$ 8/vídeo.

### 3c. Diferenciação possível [I]
1. **Ângulo Brasil/lusófono** quando houver fato real: DOPS e a ditadura, Operação Condor, a Gestapo e o Brasil (espiões nazistas no Rio, Filinto Müller e Olga Benário), a KGB e o Brasil, o Mossad e Eichmann na Argentina. Ninguém faz isso em inglês.
2. **Identidade "dossiê":** pasta parda, carimbo vermelho "CONFIDENCIAL" com o período e capítulos como "fichas" ("FICHA 1: A PIADA"). É a assinatura visual, sem copiar o template do Archive.
3. **Fontes na descrição** (livros e arquivos), para credibilidade e contra a acusação de "conteúdo produzido em massa".
4. Cadência sustentável (2–3/semana com revisão humana), não 1/dia de template.

### 3d. Riscos
| Risco | Política/fonte | Mitigação |
|---|---|---|
| **Conteúdo sobre nazismo, extremismo e violência** | Diretrizes do YouTube sobre discurso de ódio e organizações violentas permitem conteúdo **educacional/documental (EDSA)** com contexto; glorificação é removida. Imagens de suásticas/símbolos sem contexto e violência gráfica levam a **anúncio limitado** (diretrizes de adequação para anunciantes: "eventos sensíveis", "violência") [I: conhecimento das políticas, não reconsultado hoje] | Tom factual e condenatório; **nada de suástica nem runas SS na thumb**; sem cadáveres/sangue nas imagens; contexto de vítimas; começar por KGB/CIA/Mossad/Stasi, que têm menos risco que SS/Gestapo |
| **Conteúdo inautêntico** (antigo "repetitivo"; política do YPP atualizada em 07/2025: produção em massa e template com pouca variação) | Clones como Spies in Minutes (23 vídeos em 4 dias) são o exemplo do risco [O] | Roteiro original pesquisado com fontes; capítulos e anedotas próprias; cadência humana; voz clonada com revisão; não reaproveitar o texto do concorrente |
| **Conteúdo sintético/IA** | Rótulo "conteúdo alterado ou sintético" exigido para conteúdo **realista**. Quadrinho não é realista; voz clonada narrando fatos não exige rótulo [I] | Marcar o rótulo se houver dúvida; nota de "narração com voz sintética" na descrição (já é padrão no `pacote-youtube`) |
| **Temas geopolíticos atuais** (Mossad, FSB, Israel) | Limitação de anúncio e ataques nos comentários | Recortes históricos; dados com fonte; evitar o presente imediato na thumb |
| **Direitos** | Fotos de arquivo e trechos de filme geram Content ID (`anti-padroes.md` #6) | Só ilustração própria, mapas próprios, trilha sintetizada no código |
| **Pessoas reais desenhadas** (Putin, Himmler) | Comentário histórico com ilustração é aceito [I] | Sem difamação; legendas factuais |
| **Canibalizar o `historia-ptbr`** | Mesmo público pt-BR de história | Voz, nome e visual diferentes; temas distintos (organizações × países) |
| **Clones em pt** | Se pegar, vai ser copiado como foi em en | Velocidade nos 20 temas fortes + identidade "dossiê" + ângulo Brasil |

### 3e. Decisão: **TESTAR (pt-BR)**, com temas ranqueados por evidência
| # | Tema | Evidência [O] |
|---|---|---|
| 1 | KGB | Archive 236 mil; Te lo Pinto (es) 138 mil em 5 dias; Archives Soviétiques (fr) 62,7 mil; busca em 4 idiomas |
| 2 | Gestapo | Archive 349 mil; Into the Shadows 1,04 mi; Fragmentos da História (pt) "Hiena da Gestapo" 212 mil |
| 3 | CIA | Archive 141 mil; Classé Secret Défense (fr) 56 mil; 4 clones (sinal de demanda) |
| 4 | Mossad | Archive 146 mil; The War Economy 160 mil; Atlas del Tiempo (es) 32,5 mil |
| 5 | SS | Archive 317 mil (risco de política maior) |
| 6 | Stasi | Archive 114 mil; Simplicissimus (de) |
| 7 | MI6 | Archive 109 mil |
| 8 | União Soviética | Archive 126 mil |
| 9 | Guerra Fria | Archive 117 mil |
| 10 | Beria (pessoa-instituição) | Archive 86 mil |
| 11 | DOPS / ditadura (ângulo Brasil) | sem concorrente; Total History (pt) 2,2 mi com "Portugal na 2ª Guerra" mostra apetite por ângulo lusófono [I] |
| 12 | Máfia (Cosa Nostra) | busca en "history of the mafia explained" traz HISTORY e Hypothetically, mas nenhum vídeo no molde "história inteira" [O]; views não coletadas → **Hipótese** |
| 13 | Legião Estrangeira Francesa | busca en traz DW Documentary e canais militares, nenhum no molde [O]; views não coletadas → **Hipótese** |
| 14 | Gulag | o Archive tem thumb pronta no mosaico, mas o vídeo não está na lista pública de uploads em 04/11 (agendado ou removido?) [O]; tema irmão do NKVD → **Hipótese** |
| 15 | Crise dos Mísseis | Archive 49 mil |
| 16 | Muro de Berlim | Archive 40 mil |
| 17 | NKVD | Archive 22 mil (fraco) |
| 18 | Abwehr | Archive 33 mil (fraco) |
| 19 | Romanov | Archive 36 mil (fraco) |
| 20 | Titanic | Archive 11 mil (fora do eixo) |
O backlog final do canal está em `canais/dossie-ptbr/backlog.md` (reordenado com o ângulo Brasil e o risco de política).

---

## Limitações
- Views coletadas em 2026-11-04. Views/mês são extrapolação de 3–8 semanas e mudam rápido [I].
- RPM vem da tabela de referência do playbook, sem dado nosso.
- Monetização: `licensedContent` e anúncios na página são indícios, não prova.
- 15 buscas cobrem as palavras óbvias; podem existir canais pt/es com títulos diferentes não captados.
- Voz e música do Archive não foram medidas (watch.py não mede loudness nem a trilha).
- Os vídeos das pastas `pesquisa/countrycorns/` e `pesquisa/formato-in-minutes-subnichos/` são de outro job e não entraram aqui.

## Sugestões para `conhecimento/` (não editei; outro job está nesses arquivos)
- **hooks.md:** "Molde Archive" = data + lugar → cena humana em 2–4 frases → desfecho seco → "Esta é a história INTEIRA de X" → promessa em 1 linha; **15–22 s**. Fonte: hook.txt de pbIzG1QvoWs, PmpWyltn08s e VNJhu4rh6OY (2026-11-04). Mesmo molde no Abwehr com 33 mil: **o tema decide** (Hipótese reforçada com 19 vídeos do mesmo canal).
- **titulos.md:** em "história INTEIRA de X", X curto e famoso (sigla) performa: mediana de 146 mil (7 organizações famosas) × 38 mil (8 eventos/estados) no Archive (dados.json, 2026-11-04).
- **roteiros.md:** "capítulos-objeto" (13–17 capítulos de 1–2 palavras, cada um uma cena ou objeto datado) e fechamento que volta ao objeto do hook. Fonte: capítulos de PmpWyltn08s e pbIzG1QvoWs.
- **thumbnails/README.md:** template Archive = personagem à esquerda + cenário + NOME gigante preto + datas + selo redondo; nenhuma suástica nas 19 thumbs. Fonte: mosaico 2026-11-04.
- **anti-padroes.md:** "ser o 16º clone": 14 canais copiaram o template do Archive em inglês em 3 semanas, com mediana < 1 mil views (dados.json, 2026-11-04). Antes de entrar num formato, conte os clones.
