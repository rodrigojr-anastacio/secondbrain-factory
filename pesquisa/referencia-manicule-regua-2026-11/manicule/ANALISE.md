# Manicule (@maniculetv): anatomia do formato

16/11/2026. Fonte: os 2 vídeos baixados (720p), folhas de 2 s (todas as 18 lidas), transcrições Whisper inteiras, descrições, medições de áudio próprias (scripts em `~/cache/ref-mr/scripts/`: `audio_bed.py`, `sfx_peaks.py`, `gaps_stats.py`, `f0.py`, `frames_contact.py`).
**A** = "The Shortcut Over Antarctica No Airline Takes" (3axv-sGQ1Lw, 8:15, 1,23 mi views, 30/10). **T** = "The Shortcut Over Tibet Most Airlines Skip" (bUh0Nd5tpUQ, 8:41, 73 mil, 05/11).
Frames-exemplo em `frames/` (`tipo_A|T_mmss.jpg`), visão geral em `contact.jpg`. O que não é medido ou visto está marcado como **Hipótese**.

## 0. Números-chave
| | A (1,23 mi) | T (73 mil) |
|---|---|---|
| Duração / fala útil | 8:15 / 7:59 (end screen mudo de 15 s) | 8:41 / 8:24 (end screen de 16 s) |
| Palavras/min | 160 | 167 |
| Palavras por frase (média) | 10,5 | 12,1 |
| Pausa após ponto (mediana, p10–p90) | 0,72 s (0,40–1,00) | 0,74 s (0,38–1,21) |
| Pausas > 0,6 s | 86 | 78 |
| Cortes secos (detector) / após juntar rajadas a < 1,5 s | 38 / 18 | 24 / 22 |
| Trocas de cena (cortes + histograma, juntadas) | 26 → 1 a cada ~18 s | 33 → 1 a cada ~15 s |
| Composições distintas (contagem manual nas folhas) | ~56 → ~9 s cada | ~70 → ~7,5 s cada |
| Quadros quase parados | 84% | 76% |
| Loudness | −14,2 LUFS | −14,7 LUFS |
| Capítulos na descrição | 8 | 7 |
| Áudio | inglês (en-US original) + 10 faixas dubladas (ar, de, es, fr, hi, id, ja, pl, pt, uk) | idem |
| Material real (foto/vídeo de arquivo) | **0%** | **0%** |

## 1. Roteiro

### 1.1 Hook 0–30 s (transcrito)
**A (Antártica)**
> [0:00] Everyday, airliners fly over the top of the world. [0:03] Between North America and Asia, they cut straight across the Arctic. [0:07] Now look at the bottom of the world. [0:09] Almost nothing. [0:11] So why do planes avoid Antarctica? [0:15] Here's the strangest part. [0:16] Take a globe and stretch a string from Perth in Australia to Buenos Aires in Argentina. [0:22] Pull it tight. [0:24] The shortest path doesn't cross the ocean the way a flat map suggests. [0:27] It dives south over the ice, past the South Pole, with less than 500 km to spare.

Continua: [0:36] "No airline flies that line, not one." [0:38] "And no, it's not forbidden." (Tratado da Antártida, art. VII) → [0:54] "There are five reasons why. The first one has nothing to do with ice, and the last one costs 257 lives." Fim do cold open em 1:02.

**T (Tibet)**
> [0:00] The airliners cruise about 11 km up. [0:03] Mount Everest is less than 9. [0:05] So in theory, a jet can fly over anything on Earth. [0:09] And yet, across Asia, most long-haul flights go around one place. [0:14] So why do planes avoid flying over Tibet? [0:18] This is the Tibetan Plateau. [0:20] A plateau is a huge block of high ground, and this one is bigger than Greenland. [0:25] Most of it sits more than 4 km above the sea. [0:28] And it isn't closed.

Continua: [0:36] permissão especial, oxigênio extra, plano de fuga → "Most never bother." [0:46] "There are five reasons why, and strangely the flying itself is the easy part. Every one of them comes down to what happens if something goes wrong." [0:54] "At the end, we'll meet the cargo airline that crosses anyway." Fim do cold open em 0:59.

**Molde comum do hook:** contraste visual em 3 frases (norte cheio × sul vazio; 11 km × 9 km) → pergunta-título falada **e** escrita na tela (A 0:12 `texto` sobre o globo; T 0:14) → demonstração física e concreta (barbante no globo; Groenlândia sobreposta ao planalto, `mapa` T 0:24) → derruba a resposta óbvia ("not forbidden" / "isn't closed") → promessa numerada "five reasons" + **dois ganchos com prazo** (o 1º e o último motivo; ou "at the end, we'll meet…"). Na tela, a promessa vira um índice I–V com o V em vermelho ("257 LIVES", A 0:58; T 0:58 "AT THE END: THE CARGO AIRLINE THAT CROSSES ANYWAY").

### 1.2 Estrutura em blocos
**A**
| Min | Bloco | Mecanismo + anedota datada |
|---|---|---|
| 0:00 | Cold open "The line no airline flies" | barbante Perth–Buenos Aires, mapa plano × globo, Tratado de 1959 + carimbo NOT BANNED |
| 1:02 | I Nobody to fly to (*People*) | 9 em 10 pessoas no norte (pictograma); SAS 1954 Copenhague–LA (snowsuits), Polar 1–4 de 1998; "no ring of cities" |
| 2:19 | II Nowhere to land (*Runways*) | ETOPS (avião desenhado, motor falha), barras 60/330/370 min, círculos de alcance, checklist "in practice", South Polar Area 60°S + SPECIAL APPROVAL |
| 3:49 | III Nowhere to go down (*Altitude*) | perfil de altitude: cruzeiro 11 km, seguro 3 km, gelo 4.093 m acima da linha segura; barra de oxigênio esvaziando |
| 4:32 | CTA no meio | "If you like seeing the world through maps like this, subscribe. There's a new deep dive every week." |
| 4:37 | IV The cold (*Cold*) | termômetro + duto de combustível com cristais de cera (−47 °C), Qantas 2021 a −75 °C, Vostok −89,2 °C |
| 5:30 | V Can't trust your eyes (*Whiteout*) | Air New Zealand 901 (28/11/1979): rota no mapa, esquema do Erebus, efeito whiteout que apaga a tela, 12:49 PM / **257** |
| 6:46 | "And yet, planes go there" | QF14 2021 (17 h 25), QF28 2023 a 74°S, voos panorâmicos, A350 370 min "direct southern routes" |
| 7:36 | "Five reasons, one string" | recapitulação em 5 caixas que entram uma a uma; volta ao barbante + carimbo NOT BANNED |
| 8:00 | End screen (mudo) | "TELL US IN THE COMMENTS · Would you fly *over the ice?*" + botão SUBSCRIBE que vira SUBSCRIBED |

**T**
| Min | Bloco | Mecanismo + anedota datada |
|---|---|---|
| 0:00 | Cold open | maciço do Everest em 3D "TRUE SCALE" com a linha de cruzeiro; globo com rota curta × desvio; Groenlândia sobreposta; airways L888 |
| 0:59 | I The ground | barras Antártica × Tibet (**ponte para o vídeo A**), bloco 3D com cordilheiras, grade de MSA quadrado a quadrado (`mapa_T_0134`), "The Hump" 1942–45 (594 aviões) |
| 2:14 | II Nowhere to go down (*Pressure*) | relógio da consciência útil (17 s, 26 s, 43 s), perfil de descida mar × planalto, máscara química de 12–22 min, Sichuan 3U8633 (2018): cockpit visto de cima, perfil do voo |
| 4:02 | CTA no meio | mesma fala exata do A |
| 4:09 | III One engine (*Engines*) | avião de cima com motor falhando, drift-down mar × planalto, regra de 2.000 ft, plano de fuga por ponto da rota |
| 5:00 | (gancho dentro do III) | Boeing 2002: "When the numbers don't work", 3 cartões |
| 5:11 | IV Airports in thin air (*Airports*) | aeroportos no planalto, densidade do ar (100/70/64%), corrida de decolagem, Lhasa em 3D com rota de fuga monomotor, Boeing 737 2000, regra da CAAC de 2.438 m, alternados a mais de 1.000 km |
| 6:49 | V Who it pays for (*Cost*) | checklist "Add it all up", passageiros × carga vistos de cima, DHL A330 2024 por L888/Y1 (1 ano de permissão, NO OXYGEN NO PERMISSION), relógio de 20 min economizados |
| 8:02 | Recapitulação | 5 caixas com uma frase cada; fecho em 3D "Over Tibet, the hard part is *coming down*." |
| 8:25 | End screen (mudo) | "Would you take *the shortcut over Tibet?*" + SUBSCRIBE |

**Ritmo:** 5 motivos de ~1:00–1:30 cada. Todo motivo tem o mesmo formato: cartão do capítulo (2–4 s) → mecanismo explicado com 1 diagrama simples → 1 caso real datado num cartão-ficha → frase-ponte para o próximo.

### 1.3 Loops/promessas e onde são pagos
| Promessa | Onde | Pago em |
|---|---|---|
| A: "the last one costs 257 lives" | 0:56 (+ caixa V vermelha "257 LIVES") | 5:30–6:36 (Erebus; "257" grande em 6:24) |
| A: "the first one has nothing to do with ice" | 0:56 | 1:03 (pessoas/demanda) |
| A: barbante Perth–Buenos Aires | 0:16 | 2:08 ("doesn't even have a direct flight") e 7:48 (fecho) |
| A: "it's not forbidden" | 0:38 | 7:20–7:53 ("isn't banned", carimbo volta em 7:54) |
| A (gancho interno): "So far, every reason is about what might happen. The last one actually did." | 5:25 | 5:35 |
| T: "At the end, we'll meet the cargo airline that crosses anyway" | 0:54 (+ texto na tela 0:56) | 7:23 (DHL) |
| T: "the flying itself is the easy part / what happens if something goes wrong" | 0:46 | 8:19 "Over Tibet, the hard part is coming down." |
| T: 11 km × 9 km, "a jet can fly over anything" | 0:00 | 8:19 (mesma frase repetida no fecho) |
| T: "that was only the edge of the plateau" | 3:55 | 6:33 (alternados a mais de 1.000 km do meio) |

### 1.4 Transições (frases-ponte reais)
- A 2:13 "But even if a million people wanted that flight tomorrow, an airline would hit the second problem."
- A 3:18 "And yes, Antarctica has runways. … But an airliner in trouble needs more than a strip of ice."
- A 5:25 "So far, every reason is about what might happen. The last one actually did."
- A 6:46 "And yet, sometimes, a plane does go there."
- T 2:07 "Today's jets fly far above anything those crews could reach, as long as nothing goes wrong."
- T 3:55 "And that was only the edge of the plateau."
- T 7:18 "But one kind of airline has far fewer people on board."
Padrão: a última frase do capítulo abre a pergunta que o próximo responde ("mas…", "e se…", "e ainda assim…").

### 1.5 Fecho e CTA
- **Fecho:** "So why do planes avoid X?" repetido → recapitulação em uma linha por motivo (A 7:39 "Almost nobody to fly to, nowhere to land, nowhere to go down, a cold that can freeze fuel, and light that can hide a mountain.") → imagem do começo → frase final com virada (A 7:53 "It isn't banned, it's just that no airline has found a good enough reason to fly it."; T 8:19 "A jet can fly over anything on Earth. Over Tibet, the hard part is coming down.").
- **CTA falado:** 1 só, no meio, igual nos dois: A **4:32** / T **4:02**: "If you like seeing the world through maps like this, subscribe. There's a new deep dive every week." Na tela: cartão "The world, through *maps*" + botão vermelho com a mão-índice (☞) que vira SUBSCRIBED + "A NEW DEEP DIVE EVERY WEEK".
- **CTA no fim:** sem fala; pergunta para os comentários ligada ao tema + botão SUBSCRIBE (A 8:00, T 8:25), com a trilha por baixo.
- **Sem** sponsor, Patreon, produto, merch ou link externo em nenhum dos dois (fala, tela e descrição).

### 1.6 Descrições
- Estrutura: parágrafo-resumo que repete o hook e lista os 5 motivos + o caso âncora → **Chapters** → **Sources** (A: 17 links; T: 18) → assinatura "☞ Manicule: look closer. New animated deep dives every week. Subscribe so you don't miss the next one."
- Fontes: documentos primários e oficiais (Antarctic Treaty Secretariat, 14 CFR 121.161/121.7/121.191 em law.cornell.edu, FAA AC 61-107B, Boeing Flight Operations 2002, CAAC/The Paper, DHL, Guinness, NZHistory, Australian Antarctic Division, ExxonMobil), imprensa especializada (Aviation Today, Australian Aviation, Flightradar24 blog, OPSGROUP, One Mile at a Time, Seattle Times 1993, People's Daily 2024) e Wikipedia (lista de aeroportos, The Hump, 3U8633, Daocheng, MORA).
- Créditos de material: **A não tem**. **T tem** "Map data: © OpenStreetMap contributors (ODbL); Natural Earth. Terrain: AWS Terrain Tiles (SRTM, GMTED, ETOPO1)." **Nenhum crédito de música** em nenhum dos dois.
- Tags (A): Air New Zealand 901, Antarctica, ETOPS, Mount Erebus, Qantas, South Pole, aviation, flying over Antarctica, geography, great circle, maps, polar routes, whiteout, why planes avoid Antarctica. Categoria Education.

## 2. Visual plano a plano

### 2.1 Tipos de plano (contagem de quadros de 2 s; A = 247 quadros, T = 260)
| Tipo | A | T | Exemplos |
|---|---|---|---|
| Globo ortográfico ilustrado (relevo sombreado, batimetria) | **59%** (com mapas) | — | `globo_A_0006`, `globo_A_0044`, `globo_A_0134`, `globo_A_0306`, `globo_A_0347`, `globo_A_0548` |
| Mapa plano 2D (relevo de terreno, rotas, rótulos) / mapa esquemático | (dentro do 59%) | **42%** (com globo) | `mapa_A_0028`, `mapa_A_0606`, `mapa_T_0036`, `mapa_T_0134`, `mapa_T_0204`, `mapa_T_0348`, `mapa_T_0646` |
| Relevo 3D (bloco de terreno real extrudado, câmera oblíqua) | 0% | **8%** | `relevo3d_T_0004`, `relevo3d_T_0026`, `relevo3d_T_0120`, `relevo3d_T_0554`, `relevo3d_T_0558`, `relevo3d_T_0823` |
| Gráfico/diagrama de dados (barras, perfil de altitude, termômetro, relógio, linha do tempo, grade de densidade) | **24%** | **21%** | `grafico_A_0250`, `grafico_A_0429`, `grafico_A_0452`, `grafico_T_0110`, `grafico_T_0222`, `grafico_T_0245`, `grafico_T_0342` |
| Ilustração esquemática em traço (avião de cima, pictograma, passageiro com máscara, cockpit) | 2% | **9%** | `ilustracao_A_0110`, `ilustracao_A_0232`, `ilustracao_T_0256`, `ilustracao_T_0332`, `ilustracao_T_0420`, `ilustracao_T_0718` |
| Texto puro (cartão de capítulo, número grande, CTA, recapitulação, end screen) | 14% | 20% | `texto_A_0104`, `texto_A_0520`, `texto_A_0632`, `texto_A_0433`, `texto_A_0746`, `texto_A_0802`, `texto_T_0057` |
| Foto real / vídeo real / IA generativa | **0%** | **0%** | — |

Em A, separando: globo ~50% e mapas planos/esquemáticos ~9%. Em T o mapa plano de terreno domina (~38%) e o globo só aparece no cold open (~4%). **Nenhum** quadro de foto, vídeo de arquivo, rosto ou imagem gerada por IA: 100% gráfico vetorial + dados geográficos.

### 2.2 Duração dos planos
- Medido: 26 (A) e 33 (T) trocas de cena → 1 a cada 15–18 s. Contagem manual de composições distintas: ~56 (A, ~9 s) e ~70 (T, ~7,5 s).
- Dentro de cada composição entra **um elemento novo a cada 2–4 s** (rótulo, linha, cartão, barra, carimbo). Por isso 76–84% dos quadros são "quase parados" e mesmo assim a tela nunca fica igual por mais de ~4 s. Ex.: A 2:34–2:52, barras 60 → 330 → 370 min → "6 hours +" em 4 passos; T 1:26–1:40, grade preenchida quadrado a quadrado, depois o caminho "2,030 km · 2 h 24".
- Cortes secos de verdade são poucos (18–22 depois de juntar as rajadas), quase todos na entrada e na saída do cartão de capítulo. O resto é dissolve/morph sobre o mesmo fundo (globo que gira, mapa que dá zoom).

### 2.3 O que dá a sensação de movimento
1. **Linhas que se desenham**: rotas tracejadas laranja/vermelhas (barbante A 0:30), rotas pontilhadas com avião na ponta (A 1:28 1954; A 5:44 Air NZ 901; A 6:50 QF14), curvas de descida (T 2:28), linhas de fuga (T 3:04).
2. **Ícone de avião percorrendo a rota** (A 1:30, 5:40, 7:02; T 7:44).
3. **Globo que gira/vira** entre hemisférios (A 0:06→0:08 norte → sul; A 1:14 sul em escuro → 1:16 norte claro) e **zoom/pan lento** em mapas planos (T 0:18→0:20, 3:12→3:20).
4. **Câmera 3D oblíqua** sobre relevo real (T 0:00 "THE EVEREST MASSIF · TRUE SCALE"; T 1:12–1:20 bloco girando; T 5:50–5:58 voo por Lhasa).
5. **Dados que crescem**: barras, termômetro descendo, relógio girando (17 → 26 → 43 s), barra de oxigênio esvaziando (A 4:28), contadores (594 aviões, T 2:04: 197 → 594).
6. **Efeitos de cena pontuais**: whiteout que apaga a tela (A 6:14–6:20), tela escura com "12:49 PM" e o 257 entrando (A 6:22–6:28), carimbos batidos na diagonal.
7. **Troca de paleta como marca de clima**: navy escuro no cold open, no desastre e no fecho; bege-papel nos capítulos explicativos; azul-gelo no capítulo "The cold" (A 4:38–5:24).

### 2.4 Paleta e acabamento
Fundo bege-papel com vinheta escura nos cantos e leve textura; modo escuro azul-ardósia/navy. Globo em relevo sombreado (terra bege, oceano azul com batimetria; no escuro, terra cinza-azulada e gelo branco). Acentos: **vermelho-tijolo** (perigo, rota impossível, capítulo atual), **laranja/dourado** (rotas e itálico no escuro), **azul-petróleo** (itálico do capítulo no claro, barras), **verde** (seguro: "SAFE ~3 KM", "all survived", rotas de fuga). Marca d'água "☞ MANICULE" fixa no canto superior esquerdo; **rastreador de capítulos I–V** fixo no canto superior direito (o atual em vermelho e sublinhado, com o nome em itálico: *People, Runways, Altitude, Cold, Whiteout*; *Ground, Pressure, Engines, Airports, Cost*).

## 3. Tipografia e rótulos
| Uso | Fonte (palpite) | Tamanho/posição | Cor |
|---|---|---|---|
| Títulos, cartões de capítulo, perguntas na tela | **Serifa de alto contraste, bold, com uma palavra em itálico colorido** (**Hipótese:** Newsreader / Source Serif Display / família parecida) | grande, centralizado; no globo, no alto (A 0:12, 0:36) | preto no bege; branco no navy; itálico azul (claro), dourado (escuro) ou vermelho (negativo) |
| Legendas técnicas, eixos, escalas, carimbos, marca d'água | **Monoespaçada em caixa alta, espaçada** (**Hipótese:** IBM Plex Mono) | pequena, no alto ou no rodapé ("ANTARCTICA, COAST TO COAST · SIMPLIFIED PROFILE") | cinza-escuro, vermelho ou verde conforme o sentido |
| Cidades | serifa bold pequena + ponto branco/preto | junto ao ponto | preto (claro) / branco (escuro) |
| Regiões, oceanos | serifa em caixa alta bem espaçada ("G R E E N L A N D", "SICHUAN BASIN") | sobre a área | marrom/cinza suave |
| Números de destaque | serifa grande ("−89.2°" em vermelho, A 5:14; "257" branco, A 6:24; "594" vermelho, T 2:04; "128 *all survived*", T 3:46) | centro ou cartão | vermelho/branco/preto |
| Fichas de caso | cartão bege com fio duplo (cara de etiqueta de museu): linha mono "28 NOV 1979 · AIR NEW ZEALAND 901 · DC-10" + título serifa | canto superior esquerdo ou direito | — |
| Carimbos | mono bold num retângulo girado ~5° | canto inferior direito | dourado "NOT BANNED"; vermelho "SPECIAL APPROVAL", "MOST NEVER BOTHER", "AS IF ONE ENGINE HAD FAILED", "NO OXYGEN, NO PERMISSION" |

**Animação de entrada:** fade curto; listas e checklists entram item a item, sincronizadas com a fala (A 3:10–3:16 "airport open / good weather / after a long flight"; T 6:54–7:06); carimbos "batem" (escala + leve giro, **Hipótese** pelo quadro a quadro); barras e linhas crescem.

**Rótulos de honestidade** (muito frequentes e característicos): "SCHEMATIC · NOT TO SCALE" (A 5:52), "TRACKS ILLUSTRATIVE" (A 6:50–7:34), "LINES APPROX." (A 1:40), "TRUE SCALE" (T 0:00), "HEIGHTS ×3" / "×2" (T 0:26, 5:50), "PLANE NOT TO SCALE · ROUTES ILLUSTRATIVE" (T 5:58), "CALCULATED FROM TERRAIN DATA · 1° SQUARES" (T 1:34), "HEIGHTS FROM TERRAIN DATA" (T 2:08), "SIMPLIFIED PROFILE" (A 4:08).

**Crédito na tela: não há crédito de imagem/mapa** (nem OpenStreetMap/Natural Earth, que só aparecem na descrição do T). Há **atribuição de fonte embutida nas legendas** em vários quadros: "THE ANTARCTIC TREATY · 1959 · Article VII·4" (`globo_A_0044`), "US RULES (FAA) · NOT A BAN" (A 3:48), "FAA: 30–60 SECONDS AT 35,000 FT" (T 2:22), "CAUSE · CAAC REPORT, 2020" (T 3:50), "BOEING · OPERATIONS IN MOUNTAINOUS AREAS · 2002" (T 5:00), "CIVIL AVIATION ADMINISTRATION OF CHINA" (T 6:20), "THE SHORTCUT · PER FLIGHT · DHL SAYS" (T 7:56), "EXAMPLE (737): BOEING…" (T 4:30). Ou seja: o crédito vai para a **fonte do fato**, não para a imagem (a imagem é toda deles).

## 4. Fontes do material
- **Visual:** 100% próprio, gerado a partir de dados geográficos abertos. T declara OpenStreetMap (ODbL), Natural Earth e AWS Terrain Tiles (SRTM, GMTED, ETOPO1). O globo em relevo sombreado com batimetria do A tem cara de Natural Earth (shaded relief + bathymetry): **Hipótese** (não creditado). Grade de MSA e perfis de terreno feitos com dados de altitude ("CALCULATED FROM TERRAIN DATA"). **Hipótese** de ferramenta: pipeline programático (mapas e 3D renderizados por código, tipo D3/Blender-GIS/Three.js), pelo acabamento idêntico entre os vídeos e pelos números exatos tirados de dados.
- **Fatos:** os links da descrição (§1.6). Nenhum material de arquivo de terceiros, então não há licença de imagem para administrar.

## 5. Som
- **Voz:** uma só voz, a mesma nos dois vídeos; F0 mediana 136–139 Hz (p25–p75 ≈ 115–180 Hz) → **Hipótese:** masculina. 160–167 pal/min, frases curtas (10–12 palavras), sem hesitações nem repetições; pausa após ponto com mediana de 0,72 s e variação moderada (cv 0,43–0,49), pausas maiores (1,1–2,0 s) onde a imagem precisa respirar (A 5:47.8 de 2,0 s antes do "257 on board"; T 2:02.7 antes do "594"). Humana ou IA: **indeterminado**. **Hipótese:** TTS de alta qualidade ou locutor com edição de pausas, pelos indícios de canal-esteira (criado em 06/10/2026, vídeo semanal + 46 shorts, 10 dublagens). Os erros do Whisper ("breeze", "Fostock", "Planters", "Erebus won" no lugar de "Airbus won", "some are warm") indicam pronúncia limpa mas rápida, não provam nada.
- **Trilha:** cama contínua por baixo da voz o vídeo inteiro: nenhum trecho abaixo de −50 dBFS, nem com −40 dBFS / 0,4 s. Nas pausas da voz, o fundo fica com mediana de −38,6 (A) / −38,9 dBFS (T), ~20 dB abaixo da fala (−17,6 / −18,2 dBFS RMS). Segue sob o end screen a −33…−35 dBFS. Estilo: **Hipótese** ambiente/eletrônica calma (não identificada; sem crédito na descrição → provavelmente biblioteca royalty-free).
- **SFX:** A tem um **"tique" curto e consistente** (~11 ms, pico −3 dBFS, centroide ~850 Hz) em cada elemento que "pousa" na tela, medido só nas pausas da voz: 0:35.6 ("No airline flies it"), 0:56.3 (caixa V vermelha), 1:28.4 (ficha 1954), 2:10.9, 2:27.8 (ETOPS), 2:34.7 / 2:42.8 / 2:47.3 (barras), e **5 tiques em 7:38.9–7:45.6, um por caixa da recapitulação**. Mais ~10 efeitos maiores (60–430 ms: woosh/impacto/clique do subscribe em 4:34.6; 5:49.3 com 432 ms no "257 on board"). Total: 39 transientes > −12 dBFS fora da fala em A, contra **17 em T** (clique do subscribe em 4:05.9; 8:00.4). **Hipótese:** T usa menos SFX que A.
- **Loudness:** −14,2 / −14,7 LUFS (padrão do YouTube).

## 6. O que funciona aqui (por que 1,2 mi)
1. **Pergunta geográfica que qualquer um entende, com cara de mistério** ("por que nenhum avião passa por cima da Antártida?") e um gesto físico que dá para fazer em casa (barbante no globo). O título-lacuna "The Shortcut Over X No Airline Takes" casa com uma thumb de mapa e rota tracejada que se lê em 1 segundo.
2. **Promessa numerada com o pior no fim** ("five reasons… the last one costs 257 lives"), mostrada na tela como índice I–V com o V em vermelho; o rastreador fixo no canto mostra o tempo todo quanto falta. Retenção pelo "quero ver o V".
3. **Cada motivo tem um caso humano datado** (1954, 1979, 2018, 2021), e o mais dramático (Erebus, 257 mortos) fica no capítulo V, com tratamento de cena próprio (tela escura, whiteout, número grande).
4. **Uma ideia por tela, montada na hora da fala**: diagramas simples (barras, perfil, termômetro) que constroem o argumento passo a passo; o espectador "vê" o raciocínio. Densidade alta de fatos (160 pal/min) sem confundir.
5. **Acabamento editorial e confiável**: paleta e tipografia de revista (serifa + mono), rótulos de escala e honestidade, fontes primárias na descrição. Passa autoridade, e isso ajuda a recomendação para um público adulto e internacional.
6. **Alcance internacional**: inglês simples + 10 faixas dubladas (hi, id, pt, es, ja…) num tema universal.
7. **Cadeia de vídeos irmãos**: Atlantic at night (491 mil) → Sydney–Londres (1,16 mi) → Antártica (1,23 mi) → Tibet (que cita a Antártida em 1:03 e repete a fala de CTA). **Hipótese:** o pico do A veio da recomendação em sequência com o Sydney–Londres, 3 dias antes; o Tibet (73 mil) mostra que o mesmo molde não garante alcance. A diferença mais visível é o tema (Antártida = mistério global; Tibet = nicho de aviação), não a produção, que no T é até mais rica (3D, mais composições, mais ilustrações).

## 7. Diferença em relação a um canal de material real/NASA
| | Manicule | Canal de material real (NASA/arquivo) |
|---|---|---|
| Imagem | 100% gráfico vetorial próprio sobre dados abertos (OSM, Natural Earth, terreno SRTM) | foto de satélite, vídeo de arquivo, imagem científica |
| Crédito | quase nenhum crédito de imagem (só "Map data…" na descrição do T); crédito da **fonte do fato** embutido na legenda | crédito por imagem na tela (NASA/ESA/agência) é obrigação e ocupa espaço |
| O que prova o fato | o diagrama e o número calculado ("FROM TERRAIN DATA") + o link da fonte | a própria imagem real é a prova |
| Emoção | vem do roteiro (caso humano + número grande) e do efeito gráfico (whiteout, tela escura), não da imagem | vem do "isto é real" (o evento filmado) |
| Liberdade | total: escala exagerada declarada (HEIGHTS ×3), esquema "NOT TO SCALE", rotas ilustrativas | presa ao que existe filmado/fotografado |
| Custo/escala | alto no começo (molde de animação), barato por vídeo depois (os mesmos componentes: globo, perfil, barras, ficha, carimbo, rastreador) | busca e licença de material a cada vídeo |
| Risco | parecer "slide animado"; depende do roteiro segurar | material bonito com roteiro fraco ainda prende |

Resumo: Manicule troca **"ver a coisa real"** por **"entender o mecanismo"**. A imagem é um argumento desenhado, não uma prova filmada.
