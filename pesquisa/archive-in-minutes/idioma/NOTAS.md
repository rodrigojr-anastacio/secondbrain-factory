# Nicho "Dossiê" (história INTEIRA de organizações em N minutos): demanda e concorrência por idioma

Data: 2026-11-04 · Autor: Tendências (Claude Code) · Complementa `pesquisa/archive-in-minutes/LEVANTAMENTO.md` (não refaz; atualiza os números dos canais es/pt/fr).
Legenda: **[O]** observado (busca do YouTube via WARP, YouTube Data API) · **[I]** inferido/estimativa.

## Resumo
- **en: sem vaga.** 101 canais no molde exato, 91 criados desde 09/2026, mediana dos clones de 25 views; só Archive in Minutes (146 mil de mediana) e Ziro (16,6 mil) passam de 5 mil [O].
- **es: vaga parcial e a melhor prova de demanda.** 13 canais no molde, todos de 06/10 a 03/11; 12 sem tração (mediana de 17 views). O único acima de 5 mil, **Atlas del Tiempo** (735 inscritos), saiu de 96–3,4 mil views com países para **KGB 30,6 mil e Mossad 33,1 mil** quando trocou para organizações [O]. Demanda: 41 vídeos C4 de 2026 > 100 mil [O].
- **pt: vaga total, demanda média.** 3 clones com 0–15 inscritos e melhor vídeo de 54 views; um se chama **"Dossiê Completo"**. Demanda de 229 mil (mediana top-10 C4), cerca de 57% da do es; Stasi e MI6 quase não têm busca em pt [O].
- **fr: vaga total, demanda alta mas de TV.** 1 clone (melhor vídeo de 360 views). Mediana top-10 C4 de 623 mil, mas concentrada em Investigation/LCI; só 16 vídeos C4 de 2026 > 100 mil [O]. RPM provavelmente o melhor fora do en [I].
- **de / it:** vaga, mas demanda fraca (exceto Stasi em de e máfia em it) [O].
- **Surpresa:** russo tem a maior demanda fora do en (mediana top-10 C4 de 1,48 mi; 68 vídeos de 2026 > 100 mil com só 5 buscas) e quase nenhum clone, mas não monetiza o público da Rússia desde 2022 [I]. Hindi e árabe têm demanda alta (Mossad/CIA) com RPM baixo [I].
- **Surpresa 2:** a manada já chegou a todos os idiomas. Clones do molde criados nas últimas 3 semanas: es 13, de 6, pl 3, pt 3, it 2, hi 2, fr 1, ru 1, e alguns copiam até o subtítulo do Archive ("from 40 men to Putin") [O]. A janela fecha em dias, não em meses [I].

## Método [O]
- **Buscas sem cota** (`scripts/buscar.py`, `scripts/clones.py`): yt-dlp `--flat-playlist` via WARP (`socks5://127.0.0.1:40000`), com `youtube:lang=<idioma>`. Em en/es/pt/fr/de/it: 12 temas escritos nativamente ("historia de la KGB", "Geschichte der Stasi", "storia dei templari"…) + 4 consultas da fórmula traduzida ("TODA la historia de", "die ganze Geschichte", "a história inteira"…). Em ru/tr/hi/ja/pl/ar: 4–5 consultas (KGB, CIA, Mossad, Gestapo e a fórmula). Cada consulta em 2 ordens: relevância (30 resultados) e "este ano por views" (`sp=CAMSAggF`). Para concorrência: fórmula + organização em cada idioma, por **data de envio** (`sp=CAI%3D`) e por relevância (40 resultados). Ao todo, 248 + 112 consultas e 0 erros.
- **Enriquecimento pela API** (`scripts/enriquecer.py`, `canais.py`, `resumo.py`): `videos.list` dos 4.485 vídeos achados (título original, data, idioma do áudio, views); `channels.list` + `playlistItems` (até 100 uploads) de 430 canais candidatos; país de 1.000+ canais de demanda. Cota gasta: **~1.230 unidades e 0 `search.list`**.
- **Regras de contagem** (`scripts/comum.py`, `demanda.py`): o vídeo conta para o idioma pelo `defaultAudioLanguage` (ou, sem ele, pelo script/palavras do título original). Precisa ter ≥ 4 min, título original citando o tema e não ser ficção, música ou jogo (filtro por palavras). O universo é a **amostra das buscas**, não todo o YouTube: os números servem para comparar idiomas entre si.
- Autocomplete (`scripts/sugestoes.py`): `suggestqueries.google.com` (client=youtube, ds=yt, hl/gl do idioma) via WARP. A org sozinha ("kgb") sempre devolve 14 sugestões (o máximo), então só a frase "história da <org>" discrimina, e mesmo assim fracamente.

## 1. Comparativo geral [O]

| Idioma | C4 mediana do top-1 | C4 mediana da mediana top-10 | C4 soma top-10 | C4 vídeos 2026 > 100 mil | C4 > 1 mi | Núcleo-7 mediana top-10 | Núcleo-7 2026 > 100 mil | 12 temas 2026 > 100 mil | > 1 mi | Autocomplete "história da X" (soma 8 orgs) | Canais do molde exato | Clones desde 09/2026 | Mediana dos clones | Molde com mediana > 5 mil |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| en | 7,46 mi | 1,78 mi | 160,26 mi | 112 | 30 | 717,0 mil | 155 | 298 | 71 | 42 | 101 | 91 | 25 | 2 |
| es | 2,77 mi | 400,7 mil | 31,09 mi | 41 | 5 | 371,7 mil | 47 | 102 | 26 | 32 | 13 | 13 | 17 | 1 |
| pt | 851,2 mil | 228,7 mil | 13,90 mi | 21 | 1 | 122,0 mil | 22 | 32 | 1 | 27 | 3 | 3 | 10 | 0 |
| fr | 4,43 mi | 622,7 mil | 43,01 mi | 16 | 3 | 184,0 mil | 17 | 51 | 7 | 25 | 1 | 1 | 8 | 0 |
| de | 598,5 mil | 44,7 mil | 8,45 mi | 4 | 0 | 47,1 mil | 8 | 17 | 2 | 24 | 6 | 6 | 4 | 0 |
| it | 506,3 mil | 33,1 mil | 8,36 mi | 4 | 0 | 37,3 mil | 7 | 18 | 2 | 23 | 2 | 2 | 134 | 0 |
| ru | 3,95 mi | 1,48 mi | 70,76 mi | 68 | 6 | — | — | — | — | 36 | 1 | 1 | 0 | 0 |
| tr | 628,0 mil | 42,1 mil | 6,69 mi | 4 | 1 | — | — | — | — | 28 | 0 | 0 | 0 | 0 |
| hi | 1,91 mi | 625,6 mil | 42,75 mi | 27 | 6 | — | — | — | — | 16 | 2 | 2 | 10 | 0 |
| ja | 235,5 mil | 66,0 mil | 2,71 mi | 6 | 0 | — | — | — | — | 25 | 0 | 0 | 0 | 0 |
| pl | 790,8 mil | 170,8 mil | 10,01 mi | 14 | 0 | — | — | — | — | 61 | 3 | 3 | 0 | 0 |
| ar | 3,11 mi | 221,4 mil | 36,76 mi | 10 | 0 | — | — | — | — | 27 | 0 | 0 | 0 | 0 |

Colunas: **C4** = KGB, CIA, Mossad e Gestapo (os 4 temas buscados em TODOS os 12 idiomas; é a coluna comparável). **Núcleo-7** = C4 + Stasi, SS e MI6 (só nos 6 idiomas obrigatórios). "Mediana da mediana top-10" = mediana, entre os temas, da mediana de views dos 10 vídeos mais vistos de cada tema. "2026 > 100 mil" = vídeos únicos publicados em 2026 com mais de 100 mil views. Autocomplete = nº de sugestões do YouTube para a frase "história da <org>" no idioma (máximo 14 por org; proxy fraco). "Molde exato" = canal com ≥ 1 título "história INTEIRA/COMPLETA de <organização> em N minutos" e ≥ 40% dos vídeos na fórmula. "Clones" = desses, os que começaram a postar a partir de 01/09/2026. "Mediana dos clones" = mediana das medianas de views dos vídeos fórmula+organização de cada clone.

## 2. Inglês (en)

**Veredito: NÃO há vaga.** Demanda máxima [O]: C4 com mediana top-10 de 1,78 mi e 112 vídeos de 2026 acima de 100 mil. Mas o molde já tem **101 canais**, **91 criados desde 09/2026** (eram 14 no levantamento da manhã; a busca por data de envio achou muito mais), com mediana dos clones de **25 views**. Só 2 canais passam de 5 mil de mediana: Archive in Minutes (146 mil) e Ziro History (16,6 mil). [I] Entrar seria ser o 92º clone.

Demanda por tema [O] (vídeos ≥ 4 min no idioma, título original cita o tema; amostra das buscas, não o universo)

| Tema | Vídeos | Top-1 all-time | Mediana top-10 | Top-1 de 2026 | 2026 > 100 mil | 2026 > 1 mi | Top de 2026 (canal) |
|---|---|---|---|---|---|---|---|
| KGB | 130 | 2,78 mi | 644,5 mil | 470,0 mil | 9 | 0 | HOW DID ANDROPOV PUNISH HIS DAUGHTER'S RAPISTS? TH (USSR Uncovered) |
| CIA | 188 | 19,42 mi | 6,53 mi | 18,11 mi | 66 | 28 | CIA Whistleblower John Kiriakou: They Can See All  (The Diary Of A CEO) |
| Mossad | 96 | 8,67 mi | 2,84 mi | 1,15 mi | 28 | 2 | John Kiriakou: "He Sold Us Secrets!" How Jefferey  (Jack Neel) |
| Stasi | 41 | 2,48 mi | 133,7 mil | 225,1 mil | 4 | 0 | Stasi Files: Inside East Germany’s Secret Police / (SLICE Full Doc) |
| Gestapo | 58 | 6,25 mi | 717,0 mil | 1,04 mi | 11 | 1 | How the Gestapo Actually Worked (Into the Shadows) |
| SS | 64 | 8,33 mi | 1,99 mi | 2,24 mi | 36 | 4 | SS Division in France, Das Reich (Investigation) |
| MI6 | 89 | 5,69 mi | 248,1 mil | 2,08 mi | 5 | 2 | Why is the MI6 building so damn obvious? (Luke O’Sullivan) |
| FBI | 103 | 15,68 mi | 4,56 mi | 7,70 mi | 50 | 11 | The FBI's Most Valuable Agent (fern) |
| Máfia | 85 | 12,63 mi | 4,90 mi | 9,48 mi | 37 | 14 | 1 Ex-Mafia Boss vs 20 Cops (ft. Michael Franzese)  (Jubilee) |
| Templários | 57 | 9,77 mi | 1,58 mi | 2,46 mi | 31 | 3 | The Basement: Tim Hogan / Templar Knights, Atlanti (The Why Files) |
| Legião Estrangeira | 61 | 4,46 mi | 1,56 mi | 781,9 mil | 7 | 0 | What It ACTUALLY Takes to Join the French Foreign  (Mike Ritland) |
| Cartel | 40 | 7,29 mi | 2,63 mi | 7,29 mi | 21 | 9 | Your Life as Every Mexican Cartel Rank (The Life Outline) |

País dos canais (% das views do top-20 de cada tema) [O]: US 49%, GB 20%, ?? 10%, NL 7%, FR 5%, DE 3%, CA 2%, AU 1%

Teto (maiores canais no núcleo-7, outro formato) [O]: LADbible Stories (GB, 4,12 mi inscritos); The Diary Of A CEO (GB, 21,50 mi inscritos); criminals and crime fighters (?, 826,0 mil inscritos); The Infographics Show (US, 15,50 mi inscritos); Insider (US, 9,62 mi inscritos)

Concorrência: molde exato ("história INTEIRA/COMPLETA de <organização> em N minutos", ≥ 40% dos vídeos na fórmula) [O]

| Canal | País | 1º vídeo | Vídeos | Inscritos | Mediana (fórmula+org) | Mediana longos ≥ 7 d | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| [Archive in Minutes](https://www.youtube.com/channel/UCFp0Rk-ad8JD78Qw9nEJ29w) | US | 2026-10-14 | 19 | 13,2 mil | 146,4 mil | 114,7 mil | 349,9 mil: The ENTIRE History of the Gestapo in 12 Minutes |
| [The Org Files](https://www.youtube.com/channel/UC6oxeyXhNOwavYWv6ENx_oA) | US | 2026-09-23 | 13 | 104 | 140 | 267 | 24,1 mil: The ENTIRE History of Mossad in 25 Minutes |
| [Ziro History](https://www.youtube.com/channel/UC0D2w4MJDTzx8ceT1YSbiTw) | ? | 2026-10-06 | 34 | 21,3 mil | 16,6 mil | 57,6 mil | 16,6 mil: The Entire History of the KGB in 37 Minutes |
| [Fuse Room](https://www.youtube.com/channel/UCzB0_K3Qso0Xs2OIWPo22Ag) | US | 2026-10-17 | 10 | 110 | 2,2 mil | 1,2 mil | 9,9 mil: The ENTIRE History of the KGB in 15 Minutes |
| [Yankee Explainer](https://www.youtube.com/channel/UC6BpWWWuXgDickgd8fIuSxg) | CA | 2026-10-22 | 19 | 379 | 2,4 mil | 721 | 4,2 mil: The Entire History of Mossad in 20 Minutes |
| [Echoes of Empire HQ](https://www.youtube.com/channel/UCFnvdk8IWOZVgh0SdBdBy8Q) | US | 2026-10-02 | 28 | 4 | 1,4 mil | 16 | 3,2 mil: Mossad Complete History In Just 32 Minutes  |
| [Before Lore](https://www.youtube.com/channel/UCytHCAquU0PgmJDOD4CyO_w) | US | 2026-10-10 | 11 | 135 | 447 | 277 | 1,9 mil: The ENTIRE History of the CIA in 11 Minutes |
| [History Behind the Story](https://www.youtube.com/channel/UC1jznFrbFiIt0NVqYbr37ow) | ? | 2026-10-10 | 14 | 13 | 72 | 116 | 1,4 mil: The ENTIRE History of the KGB in 11 Minutes |
| [Crayon Historic](https://www.youtube.com/channel/UChqfBoHomKBkiI6oexRXV3g) | US | 2025-07-12 | 13 | 4,5 mil | 136 | 550 | 927: The ENTIRE History of The KGB (and its successors) |
| [The Whole Story](https://www.youtube.com/channel/UCfTGdun1ZqVGswy6eI0pA3w) | ? | 2026-10-23 | 12 | 13 | 51 | 231 | 855: The Entire History of the KGB in 14 Minutes |
| [Epochs Untold](https://www.youtube.com/channel/UCe2GXDIkvc_RtgnXIcLXPqQ) | ? | 2026-10-31 | 2 | 3 | 822 | 0 | 822: The ENTIRE History of the KGB in 12 Minutes |
| [Rewind the World](https://www.youtube.com/channel/UC9I098wswtTqWvjwfPlVPKA) | US | 2026-10-18 | 14 | 65 | 649 | 274 | 649: The ENTIRE History of the CIA in 10 Minutes |
| [Sounds MadeUp History](https://www.youtube.com/channel/UChCFOsHH46s-CuHqiHTli9g) | ES | 2026-10-12 | 11 | 287 | 637 | 474 | 637: The ENTIRE History of the KGB in 8 Minutes |
| [Hourglass History](https://www.youtube.com/channel/UClWTSCQ8ZOFCOVY86RxHOrg) | US | 2026-10-07 | 14 | 3 | 20 | 20 | 622: The Entire History of the KGB in 14 Minutes |
| [Past Unpacked](https://www.youtube.com/channel/UCXyLuHudy7m8vNWxK1K1vXA) | US | 2009-08-29 | 29 | 30 | 272 | 142 | 621: The ENTIRE History of the Mossad in 10 Minutes |
| … mais 86 canais (ver JSON) | | | | | | | |

Fórmula com organização, outro molde (sem "N minutos", para dormir, longo ou só 1 vídeo) [O]: FINAiUS (US, 804,0 mil insc.; 2,01 mi em "Black Budget - The ENTIRE History of CIA / Do"); Joshua Roberts (US, 86,3 mil insc.; 235,6 mil em "MEXICAN DRUG CARTELS / The COMPLETE History o"); The Culture Mafia (AU, 318,0 mil insc.; 153,7 mil em "The Complete History of the Sicilian Mafia"); Spy Operations (US, 15,3 mil insc.; 64,1 mil em "The Complete History of MI6 in 45 Minutes"); Historic Feed (US, 5,6 mil insc.; 33,2 mil em "ENTIRE History of The Waffen SS / Nazi / WW2 "); Ancient Whispers (ES, 646 insc.; 6,5 mil em "The Complete History of the Italian Mafia to ")

Fórmula com outros temas (países, cidades, desenhos) [O]: Majestic Studios (2025-03-20, mediana 432,8 mil, melhor 3,27 mi); CountryCorns (2026-09-27, mediana 123,5 mil, melhor 1,14 mi); Genius History (2026-06-15, mediana 88,2 mil, melhor 927,3 mil); History in Minutes (2026-09-11, mediana 72,7 mil, melhor 613,7 mil); Ethos (2026-10-21, mediana 19,7 mil, melhor 155,0 mil)

## 3. Espanhol (es)

**Veredito: vaga PARCIAL (1 ocupante pequeno; 12 clones sem tração).** Demanda [O]: a 2ª maior entre os obrigatórios no que importa para o canal novo: 41 vídeos C4 de 2026 acima de 100 mil (fr tem 16, pt 21) e 102 nos 12 temas; cartel, CIA, FBI e máfia são os temas mais fortes; Stasi e MI6 são fracos (mediana top-10 de 18 mil e 16 mil). Concorrência [O]: 13 canais no molde exato, **todos de 06/10 a 03/11/2026**, mediana dos clones de 17 views. Só **Atlas del Tiempo** passa de 5 mil: 735 inscritos e 28 vídeos; os 22 vídeos anteriores (países, cidades, guerras) tiveram 96–3,4 mil views, e ao trocar para organizações saltou para KGB 30,6 mil, Mossad 33,1 mil, CIA vs KGB 15,2 mil, Gestapo 7,2 mil e SS 2,0 mil (de 28/10 a 03/11). É a prova direta de que **organização rende 10–40× mais que país** no mesmo canal em es [O]. Fora do molde, Te lo Pinto (ES, 595 mil inscritos) fez "La HISTORIA COMPLETA de la KGB" (36 min, 139 mil) e pode ocupar o espaço [I]. Países dos canais de demanda [O]: MX 22%, ES 22%, US 9%, AR 6% (18% sem país), ou seja, público latino-americano grande e RPM no fator 0,25–0,4× [I, tabela do playbook].

Demanda por tema [O] (vídeos ≥ 4 min no idioma, título original cita o tema; amostra das buscas, não o universo)

| Tema | Vídeos | Top-1 all-time | Mediana top-10 | Top-1 de 2026 | 2026 > 100 mil | 2026 > 1 mi | Top de 2026 (canal) |
|---|---|---|---|---|---|---|---|
| KGB | 42 | 1,83 mi | 371,7 mil | 272,1 mil | 3 | 0 | CÓMO ANDRÓPOV VENGÓ A SU HIJA: LA OPERACIÓN SECRET (La Cara Oculta de Moscú) |
| CIA | 48 | 3,70 mi | 1,10 mi | 1,85 mi | 18 | 4 | ¿Qué sabe Putin de la CIA? Lección que México debe (Noticias El Debate) |
| Mossad | 54 | 3,70 mi | 429,8 mil | 1,19 mi | 19 | 1 | Experto en Espionaje: "el Mossad tiene espías en c (Tiene Sentido Pódcast) |
| Stasi | 24 | 1,33 mi | 18,0 mil | 59,0 mil | 0 | 0 | La HISTORIA REAL de la STASI: el espionaje que des (AndyGM en Berlín) |
| Gestapo | 23 | 1,56 mi | 198,3 mil | 105,4 mil | 1 | 0 | ¿Cómo Funcionaba REALMENTE la Gestapo? / La ORDEN  (Der Kommandant Español) |
| SS | 26 | 2,88 mi | 814,0 mil | 965,3 mil | 6 | 0 | "Lo que hizo Patton cuando un oficial de las SS ca (Armas de Guerra Alemanas) |
| MI6 | 21 | 752,1 mil | 15,7 mil | 74,1 mil | 0 | 0 | Los Cinco de Cambridge: Kim Philby y los topos sov (Archivo Desclasificado) |
| FBI | 34 | 3,59 mi | 1,21 mi | 3,59 mi | 10 | 2 | Cuando Un Agente Del FBI Humilla A Policías Corrup (Ex Agente) |
| Máfia | 30 | 5,50 mi | 1,63 mi | 2,64 mi | 10 | 6 | La vendieron a un viudo de la mafia, pero terminó  (venganza y amor) |
| Templários | 31 | 2,48 mi | 582,7 mil | 2,16 mi | 6 | 1 | Tu vida en Cada Rango de Caballero Templario (Te lo Pinto) |
| Legião Estrangeira | 26 | 979,4 mil | 70,1 mil | 42,8 mil | 0 | 0 | #164 - Correr 90KM con los Pies Sangrando; Dormir  (GÉNESIS 2:24) |
| Cartel | 70 | 11,97 mi | 2,99 mi | 5,49 mi | 32 | 12 | Me uní al cártel por 15 mil a la quincena: me ense (Penitencia) |

País dos canais (% das views do top-20 de cada tema) [O]: MX 22%, ES 22%, ?? 18%, FR 13%, US 9%, AR 6%, CZ 3%, DE 2%

Teto (maiores canais no núcleo-7, outro formato) [O]: SLICE Historia (FR, 222,0 mil inscritos); Armapedia (MX, 4,68 mi inscritos); Solo Fonseca (CZ, 1,37 mi inscritos); Der Kommandant Español (ES, 259,0 mil inscritos); La Armería (MX, 2,74 mi inscritos)

Concorrência: molde exato ("história INTEIRA/COMPLETA de <organização> em N minutos", ≥ 40% dos vídeos na fórmula) [O]

| Canal | País | 1º vídeo | Vídeos | Inscritos | Mediana (fórmula+org) | Mediana longos ≥ 7 d | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| [Atlas del Tiempo](https://www.youtube.com/channel/UCku9KB11TReyHHC1kK9CCEw) | ? | 2026-10-08 | 28 | 735 | 11,2 mil | 682 | 33,1 mil: TODA la Historia del Mossad en 17 Minutos / El Ser |
| [Archivo en Minutos](https://www.youtube.com/channel/UC8ItUk7b3hyc7UpIeXlNjdg) | ES | 2026-10-30 | 5 | 2 | 172 | 0 | 573: La historia COMPLETA del MI6 en 24 minutos |
| [Pestaña de Crónicas](https://www.youtube.com/channel/UCenofz9Br28MWn30HKpCMuw) | ? | 2026-10-24 | 11 | 10 | 201 | 132 | 525: La HISTORIA Completa de la GESTAPO en 15 minutos |
| [Archivo Minuto](https://www.youtube.com/channel/UCRlD1Xn5Smy0iCtFPAeRkzA) | MX | 2026-11-02 | 1 | 1 | 80 | 0 | 80: LA HISTORIA COMPLETA DEL MI6 EN 14 MINUTOS |
| [Civilizations & Lost History](https://www.youtube.com/channel/UCLousolrDy3iYqwZ0MM-f8A) | ? | 2026-10-30 | 20 | 1 | 17 | 0 | 64: La historia COMPLETA del Mossad en 10 minutos |
| [Dark History Vault](https://www.youtube.com/channel/UC0zYrsP0O8EeVlQ9AaUkCjQ) | ? | 2026-10-06 | 22 | 2 | 25 | 14 | 32: The Entire History of the KGB Explained in 13 Minu |
| [Construido sobre ti](https://www.youtube.com/channel/UC4bmU06dXEZ7Ec4_wi4tLlQ) | ? | 2026-10-17 | 20 | 13 | 32 | 126 | 32: Toda la historia de la CIA en 15 minutos |
| [Historia en Minutos](https://www.youtube.com/channel/UCeWmQcsXZ4W55mnl5-IjCxQ) | ? | 2026-10-15 | 7 | 0 | 6 | 2 | 6: La historia COMPLETA de la KGB en 17 minutos / Sob |
| [Archivo de Historias](https://www.youtube.com/channel/UCJ0oNE6D4muevkIwxi1u_qQ) | ? | 2026-10-31 | 4 | 0 | 2 | 0 | 5: Historia completa de la KGB en 18 minutos |
| [Plomo y Pergamino](https://www.youtube.com/channel/UCFQh5evTcCLA8cpFxIU1Jqg) | ? | 2026-11-03 | 2 | 0 | 1 | 0 | 2: TODA la historia de la Gestapo en 13 minutos |
| [Cronofolio](https://www.youtube.com/channel/UCO7P9-IALQ5CzAko9Ml8Pgg) | ? | 2026-11-03 | 2 | 0 | 0 | 0 | 0: TODA la historia del KGB en 16 minutos… y por qué  |
| [Caja B](https://www.youtube.com/channel/UCWjbf7Fcj9sEdrE3mIEz0FA) | ES | 2026-11-03 | 1 | 0 | 0 | 0 | 0: La Historia COMPLETA de la Gestapo en 11 Minutos |
| [Archivos en Minutos](https://www.youtube.com/channel/UCbsAjBx3waufmBhdZSwFMGQ) | ? | 2026-11-03 | 2 | 0 | 0 | 0 | 0: La historia COMPLETA de la Stasi en 13 Minutos |

Fórmula com organização, outro molde (sem "N minutos", para dormir, longo ou só 1 vídeo) [O]: Te lo Pinto (ES, 595,0 mil insc.; 139,1 mil em "La HISTORIA COMPLETA de la KGB"); Tras las Huellas de la Histo (?, 8,8 mil insc.; 121,2 mil em "DUÉRMETE con la historia COMPLETA de los Temp"); Espía Real (?, 36,4 mil insc.; 66,2 mil em "¿Cómo Entró Shaldag en Irán? El Mossad Pasó A"); Descanso Histórico (AR, 14,4 mil insc.; 31,6 mil em "Toda La Historia De La Mafia Italiana Para Do"); Inframundo Criminal (CO, 38,7 mil insc.; 25,7 mil em "El cartel de Los Zetas: La historia completa "); Pergaminos Olvidados (ES, 47,9 mil insc.; 21,1 mil em "DUERME ESCUCHANDO LA HISTORIA COMPLETA DE LOS")

Fórmula com outros temas (países, cidades, desenhos) [O]: GodOfCoffee (2007-05-09, mediana 85,5 mil, melhor 346,8 mil); Chronopolis (2026-10-16, mediana 65,2 mil, melhor 71,3 mil); Menuda Historia (2026-10-19, mediana 12,3 mil, melhor 21,0 mil); Cronopaís (2026-10-17, mediana 1,0 mil, melhor 20,0 mil); HISTORIA EN RELIEVE (2026-10-16, mediana 957, melhor 169,1 mil)

## 4. Português (pt)

**Veredito: SIM, há vaga.** Demanda [O]: C4 com mediana top-10 de 229 mil (57% do es, 37% do fr) e 21 vídeos C4 de 2026 acima de 100 mil; Mossad é o tema mais forte (16 vídeos de 2026 > 100 mil, top 1,29 mi), CIA e SS vêm em seguida; **Stasi (mediana top-10 de 1,2 mil) e MI6 (2,2 mil) praticamente não têm demanda em pt** e máfia teve só 6 vídeos no idioma. Concorrência [O]: 3 clones no molde exato (15/10, 26/10, 27/10), 0–15 inscritos, mediana ≤ 41 e melhor vídeo de 54 views. **Um deles se chama "Dossiê Completo"** (https://www.youtube.com/channel/UCPDSNGNogjF5morFKNuNuwg), o que colide com o nome sugerido "Dossiê em Minutos". Há canais da fórmula com países que podem pivotar: História em minutos (4,3 mil inscritos; Rússia 206 mil), Ruínas Vivas, Depois do Poder. Teto [O]: Fatos Desconhecidos (23 mi), Historiou (416 mil), Ótica Militar (136 mil). 87% das views do top-20 vêm de canais BR [O].

Demanda por tema [O] (vídeos ≥ 4 min no idioma, título original cita o tema; amostra das buscas, não o universo)

| Tema | Vídeos | Top-1 all-time | Mediana top-10 | Top-1 de 2026 | 2026 > 100 mil | 2026 > 1 mi | Top de 2026 (canal) |
|---|---|---|---|---|---|---|---|
| KGB | 33 | 427,1 mil | 122,0 mil | 87,6 mil | 0 | 0 | TERESHKOVA ESCONDEU ISSO AO POUSAR / KGB PROCUROU  (Pistas da Era Soviética) |
| CIA | 37 | 996,5 mil | 335,3 mil | 996,5 mil | 4 | 0 | Como CIA e Mossad Mataram o Líder Supremo do Irã (Relatividade) |
| Mossad | 47 | 1,29 mi | 404,5 mil | 1,29 mi | 16 | 1 | Câmeras Gravaram 29 Agentes Do MOSSAD ELIMINANDO L (Ótica Militar) |
| Stasi | 11 | 62,3 mil | 1,2 mil | 13,9 mil | 0 | 0 | O Oficial da Stasi que Fugiu Para o Ocidente — Lev (Coronel Rubro) |
| Gestapo | 21 | 706,0 mil | 89,5 mil | 706,0 mil | 2 | 0 | Assim Foi EXECUTADA a HIENA da GESTAPO *Aviso: IMA (Curiosidades Incríveis) |
| SS | 25 | 1,03 mi | 271,4 mil | 281,7 mil | 1 | 0 | A Unidade Mais Temida da Waffen-SS: Das Reich / 4K (Historiou) |
| MI6 | 10 | 15,8 mil | 2,2 mil | 1,6 mil | 0 | 0 | O ESPIÃO DENTRO DO MI6: Como Kim Philby trabalhou  (Dossiê Oculto) |
| FBI | 23 | 3,28 mi | 251,6 mil | 731,7 mil | 5 | 0 | Jack, o Estripador / História Completa + Análise d (Ossos Perdidos) |
| Máfia | 6 | 1,05 mi | 46,5 mil | 0 | 0 | 0 |  () |
| Templários | 29 | 1,09 mi | 279,1 mil | 330,5 mil | 4 | 0 | Estrutura foi construída pelos Cavaleiros Templári (Canal History Brasil) |
| Legião Estrangeira | 34 | 513,5 mil | 166,4 mil | 28,4 mil | 0 | 0 | O Que a Legião Estrangeira Diz Sobre Treinar com o (Ecos do Chumbo) |
| Cartel | 15 | 467,4 mil | 82,9 mil | 467,4 mil | 2 | 0 | As Piores Torturas do Cartel da História (Dor Pintada) |

País dos canais (% das views do top-20 de cada tema) [O]: BR 87%, ?? 5%, GB 3%, PT 2%, PE 1%, DE 1%, BE 1%, US 0%

Teto (maiores canais no núcleo-7, outro formato) [O]: Fatos Desconhecidos (BR, 23,00 mi inscritos); Relatividade (BR, 25,4 mil inscritos); Ótica Militar (GB, 136,0 mil inscritos); Historiou (BR, 416,0 mil inscritos); Mossad: Arquivos Sombrios (?, 13,7 mil inscritos)

Concorrência: molde exato ("história INTEIRA/COMPLETA de <organização> em N minutos", ≥ 40% dos vídeos na fórmula) [O]

| Canal | País | 1º vídeo | Vídeos | Inscritos | Mediana (fórmula+org) | Mediana longos ≥ 7 d | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| [Historia em Minutos](https://www.youtube.com/channel/UC5eTe96eJuE4gkyJ5IQ5Fww) | BR | 2026-10-26 | 7 | 15 | 41 | 29 | 54: Toda a história da CIA em 12 minutos |
| [Dossiê Completo](https://www.youtube.com/channel/UCPDSNGNogjF5morFKNuNuwg) | ? | 2026-10-27 | 7 | 0 | 10 | 14 | 23: A História INTEIRA da KGB em 13 Minutos |
| [História em Minutos](https://www.youtube.com/channel/UCyOrXqAEQpKKHreTYqOqdEw) | ? | 2026-10-15 | 6 | 0 | 2 | 6 | 2: A história COMPLETA da KGB em 17 minutos / Sobrevi |

Fórmula com organização, outro molde (sem "N minutos", para dormir, longo ou só 1 vídeo) [O]: Ossos Perdidos (BR, 1,54 mi insc.; 731,8 mil em "Jack, o Estripador / História Completa + Anál"); Contos não Contados (?, 1,2 mil insc.; 37,7 mil em "MOSSAD  - História completa da agência de int"); HistóriaEmGuerra (BR, 492 insc.; 2,2 mil em "SS finlandesa: o que realmente aconteceu? (Hi"); Análise Militar (BR, 6,0 mil insc.; 106 em "A História Completa da CIA: Como Nasceu a Agê")

Fórmula com outros temas (países, cidades, desenhos) [O]: Depois do Poder (2026-09-24, mediana 6,2 mil, melhor 11,6 mil); História em minutos (2026-10-09, mediana 2,0 mil, melhor 205,9 mil); Ruínas Vivas (2026-08-28, mediana 1,1 mil, melhor 166,6 mil); History Easy Guide (2026-10-27, mediana 603, melhor 25,3 mil); História Inteira (2026-10-31, mediana 158, melhor 158)

## 5. Francês (fr)

**Veredito: SIM, há vaga.** Demanda [O]: C4 com mediana top-10 de **623 mil (a maior entre os obrigatórios depois do en)**, Mossad 5,04 mi (Investigation, 2026), Légion étrangère 12,8 mi, máfia e cartel acima de 1 mi; mas a demanda é concentrada em TV e grandes canais (Investigation 5,4 mi de inscritos, LCI, HugoDécrypte, Micode, Trash), e só 16 vídeos C4 de 2026 passam de 100 mil. Stasi (3,9 mil), MI6 (7,0 mil) e Gestapo (68 mil) são fracos. Concorrência [O]: 1 clone no molde (Récits d'Archives, desde 27/10, 620 inscritos, melhor vídeo 360) e Chroniques Éternelles (Mossad, 221 views). 90% FR [O]; RPM no fator 0,5–0,7× [I], o melhor entre os não-en. Exige voz e revisão em francês [I].

Demanda por tema [O] (vídeos ≥ 4 min no idioma, título original cita o tema; amostra das buscas, não o universo)

| Tema | Vídeos | Top-1 all-time | Mediana top-10 | Top-1 de 2026 | 2026 > 100 mil | 2026 > 1 mi | Top de 2026 (canal) |
|---|---|---|---|---|---|---|---|
| KGB | 41 | 4,43 mi | 486,3 mil | 118,3 mil | 1 | 0 | Ta vie à chaque grade du KGB soviétique (Galon Zéro) |
| CIA | 35 | 4,43 mi | 777,0 mil | 795,8 mil | 4 | 0 | Comment le Mossad et la CIA ont espionné Ali Khame (L'Orient-Le Jour) |
| Mossad | 47 | 5,04 mi | 759,1 mil | 5,04 mi | 12 | 3 | Mossad, l'histoire secrète d'Israël (Investigation) |
| Stasi | 11 | 92,1 mil | 3,9 mil | 8,6 mil | 0 | 0 | Quand le chancelier Willy Brandt était surveillé p (Karambolage en français -) |
| Gestapo | 23 | 1,71 mi | 67,6 mil | 55,7 mil | 0 | 0 | JEAN MOULIN : quelqu'un l'a livré à la Gestapo — 8 (Dossiers Interdits) |
| SS | 20 | 1,64 mi | 184,0 mil | 310,2 mil | 1 | 0 | MEGA EPISODE : Dans la tête des SS, les fanatiques (SLICE Histoire) |
| MI6 | 9 | 66,6 mil | 7,0 mil | 30,6 mil | 0 | 0 | Les secrets les plus troublants que le MI6 voulait (Hakken) |
| FBI | 20 | 1,61 mi | 424,2 mil | 464,1 mil | 4 | 0 | Le génie qui a défié le FBI pendant 17 ans (Hardisk) |
| Máfia | 41 | 3,06 mi | 1,70 mi | 1,51 mi | 11 | 3 | La mafia qui a conquis Marseille (en à peine 3 ans (AVRE (Explore Media)) |
| Templários | 47 | 3,62 mi | 793,3 mil | 179,8 mil | 1 | 0 | Affaire de Gisors, la véritable enquête. (Révélati (Vendredi 13 Doc's) |
| Legião Estrangeira | 30 | 12,83 mi | 1,87 mi | 228,1 mil | 6 | 0 | Pourquoi la Légion étrangère est devenue aussi pui (Twaylo) |
| Cartel | 36 | 5,03 mi | 1,14 mi | 1,11 mi | 14 | 1 | Sinaloa : Dans les coulisses du cartel le plus pui (Notre Monde) |

País dos canais (% das views do top-20 de cada tema) [O]: FR 93%, ?? 2%, GB 1%, DE 1%, LB 1%, HK 0%, BE 0%, AU 0%

Teto (maiores canais no núcleo-7, outro formato) [O]: Investigation (FR, 5,38 mi inscritos); HugoDécrypte - Grands formats (FR, 2,03 mi inscritos); Trash (FR, 3,16 mi inscritos); Micode (FR, 2,01 mi inscritos); LCI (FR, 2,24 mi inscritos)

Concorrência: molde exato ("história INTEIRA/COMPLETA de <organização> em N minutos", ≥ 40% dos vídeos na fórmula) [O]

| Canal | País | 1º vídeo | Vídeos | Inscritos | Mediana (fórmula+org) | Mediana longos ≥ 7 d | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| [Récits d’Archives](https://www.youtube.com/channel/UCuL3Oab-izlAMszp0UXI63g) | FR | 2026-10-27 | 7 | 620 | 8 | 293 | 360: L'histoire COMPLÈTE du KGB en 13 minutes |

Fórmula com organização, outro molde (sem "N minutos", para dormir, longo ou só 1 vídeo) [O]: How It Happened (AU, 8,2 mil insc.; 413,4 mil em "The Complete History of Israel's Intelligence"); L'histoire Complete de la Ma (?, 4,8 mil insc.; 263,8 mil em "(14) L'histoire Complete de la Mafia - Le Der"); Murmures Anciens (ES, 628 insc.; 5,1 mil em "Toute l’Histoire de la Mafia Italienne pour D"); Der Legionär Français (FR, 7,8 mil insc.; 2,3 mil em "Les SS : La Garde d'Élite d'Hitler qui a Semé"); Chroniques Éternelles (FR, 680 insc.; 221 em "TOUTE l’histoire du Mossad en 10 minutes")

Fórmula com outros temas (países, cidades, desenhos) [O]: Turtoon (2023-11-08, mediana 260,0 mil, melhor 1,17 mi); Alexcalibur01 (2013-05-12, mediana 138,4 mil, melhor 1,03 mi); LucasDW (2024-11-04, mediana 109,9 mil, melhor 557,5 mil); Kiyu (2024-07-09, mediana 82,5 mil, melhor 534,3 mil); Shidyl (2025-09-21, mediana 76,3 mil, melhor 325,7 mil)

## 6. Alemão (de)

**Veredito: sim, mas com demanda fraca.** Demanda [O]: C4 com mediana top-10 de 44,7 mil e só 4 vídeos C4 de 2026 > 100 mil; a exceção é a **Stasi** (mediana top-10 de 409 mil; Simplicissimus 1,91 mi em 2026), e SS, máfia e cartel também têm demanda. Concorrência [O]: 6 clones no molde, de 28/10 a 04/11, melhor vídeo 553 (SS). Teto: Simplicissimus (2,6 mi), Terra X History, DER SPIEGEL. [I] Fora do nosso alcance de idioma e revisão; só faria sentido para Stasi/SS.

Demanda por tema [O] (vídeos ≥ 4 min no idioma, título original cita o tema; amostra das buscas, não o universo)

| Tema | Vídeos | Top-1 all-time | Mediana top-10 | Top-1 de 2026 | 2026 > 100 mil | 2026 > 1 mi | Top de 2026 (canal) |
|---|---|---|---|---|---|---|---|
| KGB | 43 | 283,6 mil | 35,0 mil | 98,0 mil | 0 | 0 | CIA gegen KGB – mitten in Europa beginnt eine gnad (Deutsch Knallhart) |
| CIA | 52 | 2,46 mi | 219,0 mil | 285,3 mil | 2 | 0 | So arbeitet die CIA (ZIB erklärt) |
| Mossad | 28 | 910,7 mil | 42,2 mil | 144,4 mil | 1 | 0 | Vom SS-Kommandeur zum Mossad-Agenten / Otto Skorze (Alexander Weiss) |
| Stasi | 59 | 1,91 mi | 409,3 mil | 1,91 mi | 3 | 1 | Die Wahrheit über die Stasi (Simplicissimus) |
| Gestapo | 28 | 286,2 mil | 47,1 mil | 286,2 mil | 1 | 0 | Gestapo-Müller: Der Nazi, der nach Hitlers Tod spu (World History DE) |
| SS | 28 | 2,50 mi | 364,9 mil | 144,4 mil | 2 | 0 | Vom SS-Kommandeur zum Mossad-Agenten / Otto Skorze (Alexander Weiss) |
| MI6 | 3 | 5,1 mil | 5,0 mil | 5,0 mil | 0 | 0 | Heinz Felfe: SS, MI6, KGB — diente er sieben Gehei (Verlorene Zeit) |
| FBI | 15 | 3,44 mi | 113,0 mil | 90,5 mil | 0 | 0 | Jack the Ripper / Die ganze Geschichte + FBI-Analy (Verlorene Knochen) |
| Máfia | 29 | 3,15 mi | 872,6 mil | 2,79 mi | 2 | 1 | Das geheime Schlachthaus der serbischen Mafia (Simplicissimus) |
| Templários | 16 | 187,0 mil | 61,0 mil | 23,1 mil | 0 | 0 | Die blutigsten Schlachten der Templer - von denen  (MDVAL) |
| Legião Estrangeira | 38 | 1,16 mi | 314,7 mil | 352,2 mil | 2 | 0 | Spezialauftrag für Fremdenlegion: Häuserkampf und  (ZDFinfo Dokus & Reportage) |
| Cartel | 21 | 4,68 mi | 494,5 mil | 569,4 mil | 5 | 0 | Kokain-Flut – Die Schweiz im Griff des globalen Ka (SRF Dokus & Reportagen) |

País dos canais (% das views do top-20 de cada tema) [O]: DE 77%, ?? 14%, FR 5%, CH 2%, BE 2%, AT 1%, GE 0%, TR 0%

Teto (maiores canais no núcleo-7, outro formato) [O]: Simplicissimus (DE, 2,60 mi inscritos); Terra X History (DE, 1,43 mi inscritos); Slice Doku (FR, 30,5 mil inscritos); DER SPIEGEL (DE, 2,35 mi inscritos); Galileo (DE, 3,33 mi inscritos)

Concorrência: molde exato ("história INTEIRA/COMPLETA de <organização> em N minutos", ≥ 40% dos vídeos na fórmula) [O]

| Canal | País | 1º vídeo | Vídeos | Inscritos | Mediana (fórmula+org) | Mediana longos ≥ 7 d | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| [Destiny Griffin](https://www.youtube.com/channel/UCNWrWW3xhBiUwCoNpsEyPng) | ? | 2026-10-29 | 7 | 2 | 177 | 0 | 553: Die GANZE Geschichte der SS in 16 Minuten |
| [ZeitBlitz](https://www.youtube.com/channel/UCreJ47iJQMOEPfWtic7tIjQ) | ? | 2026-11-03 | 1 | 1 | 27 | 0 | 27: Die ganze Geschichte der CIA in 14 Minuten |
| [The Unknown Scriptures](https://www.youtube.com/channel/UCAjPw-YHD_e08l7iJdKTMsw) | US | 2026-10-28 | 3 | 1 | 4 | 4 | 4: Die Gesamte Geschichte der Gestapo in 24 Minuten |
| [Akte Geheim](https://www.youtube.com/channel/UCPqTAQWbdN0eGxuIbKbFZcw) | AT | 2026-10-31 | 3 | 0 | 4 | 0 | 4: Die GESAMTE Geschichte der Stasi in 13 Minuten |
| [Geschichte in Minuten](https://www.youtube.com/channel/UCYrCe1X6qIf--UN9PY_hHzA) | ? | 2026-11-04 | 1 | 1,2 mil | 1 | 0 | 1: Die gesamte Geschichte der CIA in 13 Minuten |
| [조순자조순자](https://www.youtube.com/channel/UCv_PZJ83WWUdnbna8ZmMdDQ) | ? | 2026-11-04 | 1 | 0 | 0 | 0 | 0: Die GANZE Geschichte der GESTAPO in 21 Minuten |

Fórmula com organização, outro molde (sem "N minutos", para dormir, longo ou só 1 vídeo) [O]: Verlorene Knochen (DE, 5,8 mil insc.; 90,5 mil em "Jack the Ripper / Die ganze Geschichte + FBI-"); MauerNarben (?, 4,8 mil insc.; 22,0 mil em "War der Kommandeur von Irans Gefährlichster M"); GeschichteImKrieg (DE, 774 insc.; 23,8 mil em "Die Waffen-SS-Veteranen in Afrika: Der geheim"); Geschichte ohne Mythen / Der (DE, 7,5 mil insc.; 7,2 mil em "Die Totenkopf-Division: Im Zentrum der Hölle "); Der Kommandant (DE, 32,3 mil insc.; 1,5 mil em "Die Gesamte Geschichte der GESTAPO aus DEUTSC"); Vergessene Front (DE, 39 insc.; 342 em "Die Totenkopf-Division – Im Zentrum der Hölle")

Fórmula com outros temas (países, cidades, desenhos) [O]: Geschichte. Lebt. (2026-02-24, mediana 57,4 mil, melhor 492,8 mil); Geschichte Ewig (2026-09-08, mediana 7,3 mil, melhor 115,9 mil); Jäger (2024-12-24, mediana 1,8 mil, melhor 31,5 mil); GeschichteEwig (2026-09-08, mediana 1,5 mil, melhor 6,2 mil); Zeitspiegel (2026-10-09, mediana 1,4 mil, melhor 68,2 mil)

## 7. Italiano (it)

**Veredito: sim, mas com demanda fraca.** Demanda [O]: C4 com mediana top-10 de 33,1 mil, a menor dos obrigatórios; só **máfia** é forte (mediana top-10 de 1,01 mi; Nova Lectio). O tema Stasi está contaminado pelo caso Garlasco (Alberto Stasi) e não vale como sinal. Concorrência [O]: 2 clones (Archivio Storico desde 31/10, melhor 571; Dossier in Minuti de 04/11).

Demanda por tema [O] (vídeos ≥ 4 min no idioma, título original cita o tema; amostra das buscas, não o universo)

| Tema | Vídeos | Top-1 all-time | Mediana top-10 | Top-1 de 2026 | 2026 > 100 mil | 2026 > 1 mi | Top de 2026 (canal) |
|---|---|---|---|---|---|---|---|
| KGB | 21 | 141,9 mil | 13,6 mil | 45,1 mil | 0 | 0 | Oleg Gordievsky: La Grande Fuga dal KGB (Dentro La Storia) |
| CIA | 48 | 4,13 mi | 186,1 mil | 135,1 mil | 2 | 0 | 29 messaggi alieni tradotti dall'NSA?: la storia d (Omega Click ) |
| Mossad | 26 | 361,0 mil | 37,3 mil | 361,0 mil | 1 | 0 | NETANYAHU e il MOSSAD potevano evitare il 7 ottobr (Will Media) |
| Stasi | 17 | 214,0 mil | 45,6 mil | 214,0 mil | 1 | 0 | DNA sui pedali di Stasi: parla il genetista che sc (Rai) |
| Gestapo | 25 | 651,7 mil | 28,9 mil | 651,7 mil | 1 | 0 | Perché l’ICE (non) è la Gestapo (Nova Lectio) |
| SS | 25 | 1,40 mi | 131,4 mil | 146,4 mil | 2 | 0 | Ernst Kaltenbrunner / La bestia delle SS che terro (WW2 Legends IT) |
| MI6 | 5 | 12,7 mil | 151 | 151 | 0 | 0 | "MI6: LA VERITÀ CHE NESSUN FILM RACCONTA" - Storia (Storia Express) |
| FBI | 22 | 1,76 mi | 54,0 mil | 60,9 mil | 0 | 0 | L'FBI Ha Speso Milioni Per Incastrare Carlo Gambin (Sospeter tv) |
| Máfia | 34 | 4,13 mi | 1,01 mi | 1,87 mi | 6 | 1 | Come la ’Ndrangheta è diventata la mafia più poten (Nova Lectio) |
| Templários | 42 | 208,7 mil | 61,6 mil | 55,6 mil | 0 | 0 | I TEMPLARI: dai nove cavalieri di Gerusalemme ai b (Storie per Dormire Bene) |
| Legião Estrangeira | 18 | 3,86 mi | 113,6 mil | 3,86 mi | 1 | 1 | DENTRO LA LEGIONE STRANIERA: i soldati più duri al (Progetto Happiness) |
| Cartel | 33 | 1,40 mi | 245,8 mil | 402,0 mil | 4 | 0 | Perché Trump ha catturato Maduro in Venezuela ma h (Roberto Saviano Official) |

País dos canais (% das views do top-20 de cada tema) [O]: IT 94%, ?? 4%, SE 1%, BE 1%, ES 0%, US 0%, BR 0%, PL 0%

Teto (maiores canais no núcleo-7, outro formato) [O]: Nova Lectio (IT, 1,62 mi inscritos); Stefano Ticci (IT, 61,1 mil inscritos); Dentro La Storia (IT, 144,0 mil inscritos); Geopop (IT, 3,03 mi inscritos); Roberto Solari (?, 1,8 mil inscritos)

Concorrência: molde exato ("história INTEIRA/COMPLETA de <organização> em N minutos", ≥ 40% dos vídeos na fórmula) [O]

| Canal | País | 1º vídeo | Vídeos | Inscritos | Mediana (fórmula+org) | Mediana longos ≥ 7 d | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| [Archivio Storico](https://www.youtube.com/channel/UCu-v7V_5stsXg_UF4W25adA) | ? | 2026-10-31 | 3 | 1 | 268 | 0 | 571: L'INTERA Storia del KGB in 18 Minuti |
| [Dossier in Minuti](https://www.youtube.com/channel/UCGdWLjUdB5YxYvf0yHvw0xQ) | IT | 2026-11-04 | 1 | 4 | 1 | 0 | 1: L'INTERA storia della Gestapo in 16 minuti |

Fórmula com organização, outro molde (sem "N minutos", para dormir, longo ou só 1 vídeo) [O]: Ossa Perdute (IT, 12,9 mil insc.; 37,3 mil em "Jack lo Squartatore / Storia completa + Anali"); ARTIFACTA (IT, 69,5 mil insc.; 16,2 mil em "TEMPLARI - La Storia COMPLETA"); Il Diario di Tutankhamon (IT, 1,4 mil insc.; 5,7 mil em "La Storia Completa Dei Cavalieri Templari / D")

Fórmula com outros temas (países, cidades, desenhos) [O]: Capitano Toon (2023-09-11, mediana 69,2 mil, melhor 635,6 mil); Rovine viventi (2026-07-06, mediana 28,0 mil, melhor 182,9 mil); Glae (2024-12-14, mediana 19,1 mil, melhor 72,9 mil); Il Segreto dei Popoli (2026-10-05, mediana 12,7 mil, melhor 237,0 mil); Atlante Vivo (2026-10-17, mediana 93, melhor 718)

## 8. Russo (ru), exploratório

**Veredito: vaga sim, mas mercado sem receita.** Demanda [O]: a maior fora do en, com apenas 5 buscas: C4 com mediana top-10 de **1,48 mi** e **68 vídeos C4 de 2026 acima de 100 mil** (KGB sozinho: 32). Concorrência [O]: 1 clone ("ВСЯ ИСТОРИЯ КГБ за 17 минут", 0 views); "Сонный Архив" faz "полная история" para dormir (82,8 mil inscritos). Monetização [I, conhecimento de política, não reconsultado hoje]: o YouTube suspendeu anúncios para usuários na Rússia em 03/2022 e o serviço é desacelerado no país desde 2024; os maiores canais estão registrados em AE (34% das views), US e ES. Receita por view muito baixa: **não recomendo**.

Demanda por tema [O] (vídeos ≥ 4 min no idioma, título original cita o tema; amostra das buscas, não o universo)

| Tema | Vídeos | Top-1 all-time | Mediana top-10 | Top-1 de 2026 | 2026 > 100 mil | 2026 > 1 mi | Top de 2026 (canal) |
|---|---|---|---|---|---|---|---|
| KGB | 69 | 6,07 mi | 2,72 mi | 6,07 mi | 32 | 1 | Фейковые мощи, чудеса, КГБ и РПЦ – разговор со свя (вДудь) |
| CIA | 42 | 4,65 mi | 2,62 mi | 2,76 mi | 16 | 4 | Как ЦРУ ликвидировали Усаму бен Ладена / Уроки ист (МИНАЕВ LIVE) |
| Mossad | 51 | 1,86 mi | 349,4 mil | 1,13 mi | 13 | 1 | МОССАД: Разведка, которой разрешено ВСЁ !? (Виталий Шевченко) |
| Stasi | 1 | 142 | 142 | 142 | 0 | 0 | Dissident tötet Stasi-Spitzel nach Gefängnis / Wah (Akte Nebenan) |
| Gestapo | 42 | 3,26 mi | 324,2 mil | 364,6 mil | 9 | 0 | СОВЕТСКИЙ МАЛЬЧИК, который ОБМАНУЛ ГЕСТАПО 67 раз (МОНОЛИТ) |
| SS | 5 | 804,6 mil | 241,8 mil | 804,6 mil | 3 | 0 | ЛУЧШИЙ ПРОКУРОР СССР… оказалась карателем СС! КГБ  (В пламени историй) |
| MI6 | 2 | 45,9 mil | 31,4 mil | 45,9 mil | 0 | 0 | MI6 vs Джеймс Бонд: как на самом деле работает бри (AleX BROK) |
| FBI | 1 | 509,3 mil | 509,3 mil | 0 | 0 | 0 |  () |

País dos canais (% das views do top-20 de cada tema) [O]: AE 34%, RU 23%, US 13%, ES 8%, KZ 7%, ?? 4%, DE 3%, PL 2%

Teto (maiores canais no núcleo-7, outro formato) [O]: Центральное Телевидение (AE, 5,01 mi inscritos); Владимир Логинов (US, 953,0 mil inscritos); МИНАЕВ LIVE (RU, 4,40 mi inscritos); Россия 90х (AE, 1,12 mi inscritos); вДудь (ES, 10,30 mi inscritos)

Concorrência: molde exato ("história INTEIRA/COMPLETA de <organização> em N minutos", ≥ 40% dos vídeos na fórmula) [O]

| Canal | País | 1º vídeo | Vídeos | Inscritos | Mediana (fórmula+org) | Mediana longos ≥ 7 d | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| [Шкала Жизни](https://www.youtube.com/channel/UC_zaesccVYcrZ50Du0QiRuQ) | US | 2026-10-18 | 2 | 0 | 0 | 18 | 0: ВСЯ ИСТОРИЯ КГБ за 17 минут |

Fórmula com organização, outro molde (sem "N minutos", para dormir, longo ou só 1 vídeo) [O]: Забытые Лица (PL, 4,5 mil insc.; 322,7 mil em "Гестапо глазами немцев: полная история 1933–1"); Сонный Архив (?, 82,8 mil insc.; 32,4 mil em "Полная история КАРТЕЛЕЙ: теневое государство."); Тайное Досье (US, 136,0 mil insc.; 3,9 mil em "Милиционеры убили майора КГБ — и обрушили все"); Рожденные в СССР (?, 891 insc.; 5 em "Вот как работает КГБ изнутри (полная история)")

Fórmula com outros temas (países, cidades, desenhos) [O]: Total Arsenal (2026-07-02, mediana 140, melhor 285)

## 9. Turco (tr), exploratório

**Veredito: sem demanda relevante.** Demanda [O]: C4 com mediana top-10 de 42 mil; só Mossad tem tração (GZT, 1,61 mi). 0 canais no molde.

Demanda por tema [O] (vídeos ≥ 4 min no idioma, título original cita o tema; amostra das buscas, não o universo)

| Tema | Vídeos | Top-1 all-time | Mediana top-10 | Top-1 de 2026 | 2026 > 100 mil | 2026 > 1 mi | Top de 2026 (canal) |
|---|---|---|---|---|---|---|---|
| KGB | 41 | 875,9 mil | 66,2 mil | 40,6 mil | 0 | 0 | Şçolokov ölmeden önce ne dedi? KGB dosyasındaki sı (Osmanlı’nın Gölgesi) |
| CIA | 25 | 380,2 mil | 2,2 mil | 3,5 mil | 0 | 0 | CIA’nın Eski Patronu Stansfield Turner 32. Gün’de  (32.Gün) |
| Mossad | 20 | 1,61 mi | 246,1 mil | 1,61 mi | 4 | 1 | MİT'in en derin operasyonu: MOSSAD'ın Türkiye'deki (GZT) |
| Gestapo | 5 | 73,9 mil | 18,0 mil | 18,0 mil | 0 | 0 | Gestapo: En SAF Haliyle Nazi Terörü / RENKLİ Tarih (Der Panzer Türkçe) |
| SS | 1 | 22,3 mil | 22,3 mil | 0 | 0 | 0 |  () |
| MI6 | 2 | 3,4 mil | 3,3 mil | 3,4 mil | 0 | 0 | KGB'yi BİTİREN ARŞİV MEMURU: Sovyetler Birliğini Y (Mahir Esen) |
| FBI | 1 | 941,7 mil | 941,7 mil | 941,7 mil | 1 | 0 | FBI’A EĞİTİM VEREN SERİ KATİL - EDMUND KEMPER (Onur Can Yenilmez) |

País dos canais (% das views do top-20 de cada tema) [O]: TR 97%, US 2%, DE 1%, ?? 1%, KZ 0%

Teto (maiores canais no núcleo-7, outro formato) [O]: GZT (TR, 2,63 mi inscritos); Kaan Ünsal Alphan (TR, 507,0 mil inscritos); GAİN (TR, 534,0 mil inscritos); 32.Gün (TR, 1,05 mi inscritos); DFT Tarih (TR, 1,07 mi inscritos)

Concorrência: molde exato ("história INTEIRA/COMPLETA de <organização> em N minutos", ≥ 40% dos vídeos na fórmula) [O]

Nenhum.

## 10. Hindi (hi), exploratório

**Veredito: vaga sim, demanda alta, RPM baixo.** Demanda [O]: C4 com mediana top-10 de 626 mil e 27 vídeos C4 de 2026 > 100 mil, puxada por CIA/Mossad em pauta atual (Irã, Khamenei); Gestapo não existe como tema. O espaço é de mídia grande (The Lallantop 35 mi, Crime Tak 13,6 mi, Lucky Bisht 1,1 mi). Concorrência [O]: 2 canais com título em inglês + "Hindi" (melhores vídeos de 3 e 17 views). RPM [I]: o mais baixo da lista. Há ruído de classificação de idioma em máfia/cartel.

Demanda por tema [O] (vídeos ≥ 4 min no idioma, título original cita o tema; amostra das buscas, não o universo)

| Tema | Vídeos | Top-1 all-time | Mediana top-10 | Top-1 de 2026 | 2026 > 100 mil | 2026 > 1 mi | Top de 2026 (canal) |
|---|---|---|---|---|---|---|---|
| KGB | 24 | 1,77 mi | 227,6 mil | 262,4 mil | 6 | 0 | अकेले इस KGB Spy ने पूरा SOVIET UNION खत्म कर दिया (Lucky Bisht ) |
| CIA | 24 | 2,05 mi | 1,02 mi | 2,05 mi | 13 | 4 | How Mossad & CIA Got Ayatollah Khamenei / Israel & (The Deshbhakt) |
| Mossad | 32 | 9,08 mi | 1,83 mi | 2,05 mi | 15 | 4 | How Mossad & CIA Got Ayatollah Khamenei / Israel & (The Deshbhakt) |
| Gestapo | 1 | 1,4 mil | 1,4 mil | 0 | 0 | 0 |  () |
| SS | 3 | 898,2 mil | 748,9 mil | 898,2 mil | 3 | 0 | SS Baychimo Wo Jahaaz Jo 38 Saal Tak Marne Se Inka (Deep Sea Rahasya) |
| MI6 | 2 | 446,8 mil | 385,3 mil | 446,8 mil | 2 | 0 | OPERATION GOLD सबसे बड़ा धोखा, CIA-MI6 जमीन के नीच (Lucky Bisht ) |
| FBI | 2 | 1,23 mi | 1,13 mi | 1,23 mi | 1 | 1 | 1 महिला जासूस जिसने 2 FBI Agent और पूरे अमेरिका को (Lucky Bisht ) |
| Máfia | 6 | 5,14 mi | 1,56 mi | 5,14 mi | 6 | 5 | La Rosa de Guadalupe / Buchonas, chicas de la mafi (90'S HiTs) |
| Cartel | 2 | 7,69 mi | 4,16 mi | 7,69 mi | 1 | 1 | Inside the Most Dangerous Cartel You’ve Never Seen (Dhruv Rathee) |

País dos canais (% das views do top-20 de cada tema) [O]: IN 77%, US 10%, DE 10%, ?? 2%, AE 1%, PK 0%

Teto (maiores canais no núcleo-7, outro formato) [O]: The Lallantop (IN, 35,10 mi inscritos); Crime Tak (IN, 13,60 mi inscritos); Lucky Bisht  (IN, 1,11 mi inscritos); Shubhankar Mishra  (IN, 9,21 mi inscritos); The Deshbhakt (IN, 6,92 mi inscritos)

Concorrência: molde exato ("história INTEIRA/COMPLETA de <organização> em N minutos", ≥ 40% dos vídeos na fórmula) [O]

| Canal | País | 1º vídeo | Vídeos | Inscritos | Mediana (fórmula+org) | Mediana longos ≥ 7 d | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| [History Through Time](https://www.youtube.com/channel/UC-bBq3pgNLBF3r3EZmIi4hA) | IN | 2026-10-18 | 7 | 17 | 17 | 464 | 17: The ENTIRE History of the Mossad in 10 Minutes |
| [Itihaas Originals](https://www.youtube.com/channel/UCDx1ukhYxBrnL4zaUkTzLEw) | US | 2026-10-02 | 10 | 25 | 3 | 351 | 3: The ENTIRE History of the CIA in 13 Minutes / Hind |

Fórmula com organização, outro molde (sem "N minutos", para dormir, longo ou só 1 vídeo) [O]: ExBanker Lens (IN, 168 insc.; 676 em "Black Budget :  The ENTIRE History of CIA / H"); AN fininfo (IN, 4 insc.; 22 em "CIA दुनिया की सबसे रहस्यमयी एजेंसी का पूरा सच")

## 11. Japonês (ja), exploratório

**Veredito: sem demanda relevante.** Demanda [O]: C4 com mediana top-10 de 66 mil; Gestapo 4,1 mil. 0 canais no molde.

Demanda por tema [O] (vídeos ≥ 4 min no idioma, título original cita o tema; amostra das buscas, não o universo)

| Tema | Vídeos | Top-1 all-time | Mediana top-10 | Top-1 de 2026 | 2026 > 100 mil | 2026 > 1 mi | Top de 2026 (canal) |
|---|---|---|---|---|---|---|---|
| KGB | 9 | 214,7 mil | 24,4 mil | 24,4 mil | 0 | 0 | 【渋谷チーマー裏面史】本職ヤクザも恐れた最強ギャング「KGB」の実態。3代リーダー・矢尻哲朗という怪 (アングラファイル) |
| CIA | 4 | 256,3 mil | 121,5 mil | 256,3 mil | 2 | 0 | 【暗殺や潜入はある？】CIA・MI6と話してわかった世界で最も有名な諜報機関の実態。【公安】【スパイ (元公安捜査官【勝丸円覚】) |
| Mossad | 29 | 427,6 mil | 107,7 mil | 293,2 mil | 4 | 0 | 【イラン攻撃】世界屈指のイスラエル情報機関「モサド」の完璧作戦と、スパイの内通・情報戦の裏側を解説／ (楽待 RAKUMACHI) |
| Gestapo | 14 | 9,1 mil | 4,1 mil | 1,6 mil | 0 | 0 | ゲシュタポの拷問室――史上最も恐ろしい密室の真実 (帝国の日記) |
| MI6 | 2 | 28,0 mil | 14,4 mil | 0 | 0 | 0 |  () |
| Máfia | 1 | 2,08 mi | 2,08 mi | 0 | 0 | 0 |  () |

País dos canais (% das views do top-20 de cada tema) [O]: JP 88%, ?? 7%, KR 5%, VN 0%

Teto (maiores canais no núcleo-7, outro formato) [O]: 僕らの知らない物語 (JP, 352,0 mil inscritos); 元公安捜査官【勝丸円覚】 (JP, 38,9 mil inscritos); 楽待 RAKUMACHI (JP, 1,75 mi inscritos); 想像以上にヤバすぎた… (JP, 11,7 mil inscritos); 歴史狙撃 - History Sniper (KR, 2,5 mil inscritos)

Concorrência: molde exato ("história INTEIRA/COMPLETA de <organização> em N minutos", ≥ 40% dos vídeos na fórmula) [O]

Nenhum.

Fórmula com organização, outro molde (sem "N minutos", para dormir, longo ou só 1 vídeo) [O]: 歴史を旅するチャンネル (?, 457 insc.; 40 em "【衝撃】石油が世界を支配した本当の理由｜戦争・CIA・独占の全歴史【雑学/面白動画】")

## 12. Polonês (pl), exploratório

**Veredito: vaga sim, demanda média.** Demanda [O]: C4 com mediana top-10 de 171 mil e 14 vídeos C4 de 2026 > 100 mil; Gestapo e KGB são temas fortes (ocupação, PRL). Autocomplete com o maior número de sugestões (61), mas "historia" é genérico em polonês [I]. Concorrência [O]: 3 clones de 03–04/11 (melhor vídeo 91); um copia até o subtítulo do Archive: "CAŁA historia KGB w 17 minut — od 40 ludzi do Putina".

Demanda por tema [O] (vídeos ≥ 4 min no idioma, título original cita o tema; amostra das buscas, não o universo)

| Tema | Vídeos | Top-1 all-time | Mediana top-10 | Top-1 de 2026 | 2026 > 100 mil | 2026 > 1 mi | Top de 2026 (canal) |
|---|---|---|---|---|---|---|---|
| KGB | 33 | 1,05 mi | 321,7 mil | 655,0 mil | 6 | 0 | Przepowiedziała PRZYSZŁOŚĆ DO 5079 roku ! Baba Wan (Prawdziwe Historie) |
| CIA | 11 | 1,80 mi | 162,9 mil | 228,7 mil | 3 | 0 | Szef CIA w Moskwie! Nowe info! Wiceszef MON: Polsk (HISTORIA REALNA) |
| Mossad | 10 | 332,1 mil | 19,4 mil | 251,8 mil | 2 | 0 | Porwania, bomby i sabotaż – kulisy działań Mosadu  (Historia jakiej nie znaci) |
| Stasi | 6 | 287,0 mil | 23,6 mil | 24,5 mil | 0 | 0 | SB KONTRA KGB I STASI. Nikt nie miał dowiedzieć si (Ślady historii) |
| Gestapo | 21 | 530,0 mil | 178,6 mil | 530,0 mil | 4 | 0 | Czerwone Gestapo – kaci z Urzędu Bezpieczeństwa. H (Historia bez cenzury) |
| SS | 1 | 215,1 mil | 215,1 mil | 0 | 0 | 0 |  () |
| MI6 | 2 | 12,1 mil | 6,2 mil | 12,1 mil | 0 | 0 | Jak CIA i MI6 obalały demokratyczny rząd w Iranie  (RMF FM) |
| FBI | 1 | 397 | 397 | 397 | 0 | 0 | FBI i KGB chciały go zniszczyć - jednocześnie. Z p (Historie szpiegowskie) |

País dos canais (% das views do top-20 de cada tema) [O]: PL 90%, ?? 9%, US 1%, CH 0%, VN 0%

Teto (maiores canais no núcleo-7, outro formato) [O]: National Geographic Polska (PL, 920,0 mil inscritos); HISTORIA REALNA (PL, 776,0 mil inscritos); Historia bez cenzury (PL, 1,88 mi inscritos); Powojnie (PL, 361,0 mil inscritos); Prawdziwe Historie (PL, 156,0 mil inscritos)

Concorrência: molde exato ("história INTEIRA/COMPLETA de <organização> em N minutos", ≥ 40% dos vídeos na fórmula) [O]

| Canal | País | 1º vídeo | Vídeos | Inscritos | Mediana (fórmula+org) | Mediana longos ≥ 7 d | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| [Dziejoryt](https://www.youtube.com/channel/UCMLR5Gh0WBpb0V04ibdKRRg) | ? | 2026-11-03 | 2 | 2 | 46 | 0 | 91: CAŁA historia Gestapo w 20 minut |
| [Kronokadr](https://www.youtube.com/channel/UC8LiSsyArbW8KVX216BAa3g) | ? | 2026-11-03 | 2 | 0 | 0 | 0 | 1: CAŁA historia KGB w 17 minut — od 40 ludzi do Puti |
| [Czas Przeszły](https://www.youtube.com/channel/UCMMMnzWvhgry8r5r094dd7A) | PL | 2026-11-04 | 1 | 0 | 0 | 0 | 0: CAŁA historia SS w 16 minut |

Fórmula com organização, outro molde (sem "N minutos", para dormir, longo ou só 1 vídeo) [O]: Der Kommandant POL (PL, 4,5 mil insc.; 12,3 mil em "Cała Historia GESTAPO z NIEMIECKIEJ Perspekty")

## 13. Árabe (ar), exploratório

**Veredito: vaga sim, com risco político.** Demanda [O]: C4 com mediana top-10 de 221 mil; **Mossad** forte (mediana top-10 de 1,98 mi) e CIA também; KGB e Gestapo fracos. 0 canais no molde. Teto: Haitham Soliman (1,8 mi), Abulsadiq (6,6 mi), Al Jazeera. [I] Tema Mossad muito politizado; RPM baixo-médio.

Demanda por tema [O] (vídeos ≥ 4 min no idioma, título original cita o tema; amostra das buscas, não o universo)

| Tema | Vídeos | Top-1 all-time | Mediana top-10 | Top-1 de 2026 | 2026 > 100 mil | 2026 > 1 mi | Top de 2026 (canal) |
|---|---|---|---|---|---|---|---|
| KGB | 14 | 885,5 mil | 16,3 mil | 120,7 mil | 1 | 0 | بلا تحفظ / جاسوس سوفيتي يروي قصته ويكشف أسرار مهمت (العربية برامج) |
| CIA | 7 | 5,67 mi | 426,0 mil | 784,7 mil | 2 | 0 | أقذر خائن في تاريخ الـ CIA - باع بلده ثم باع ابنه  (Haitham Soliman - هيثم سل) |
| Mossad | 24 | 4,89 mi | 1,98 mi | 632,6 mil | 7 | 0 | القصة الحقيقية لعملية ميونيخ 1972 / كيف خدعت المقا (Haitham Soliman - هيثم سل) |
| Gestapo | 6 | 1,33 mi | 16,7 mil | 43 | 0 | 0 | الجستابو: عيون هتلر وآذانه / فيلم وثائقي (Der Soldat العربية) |
| SS | 1 | 124,5 mil | 124,5 mil | 124,5 mil | 1 | 0 | Полная История Нацистской СС: Неизвестные Подробно (Война без лжи) |
| MI6 | 1 | 597,9 mil | 597,9 mil | 597,9 mil | 1 | 0 | وثائقي - MI6 المخابرات البريطانية إسقاط دول وتشكيل (Step News Agency - وكالة ) |

País dos canais (% das views do top-20 de cada tema) [O]: EG 44%, JO 22%, CA 17%, QA 11%, SA 5%, ?? 1%, KZ 0%, MA 0%

Teto (maiores canais no núcleo-7, outro formato) [O]: Haitham Soliman - هيثم سليمان (EG, 1,81 mi inscritos); Abulsadiq - ابو الصادق (JO, 6,58 mi inscritos); Step News Agency - وكالة ستيب نيوز (CA, 6,05 mi inscritos); AlJazeera Arabic  قناة الجزيرة (QA, 23,80 mi inscritos); Nest Productions (EG, 1,01 mi inscritos)

Concorrência: molde exato ("história INTEIRA/COMPLETA de <organização> em N minutos", ≥ 40% dos vídeos na fórmula) [O]

Nenhum.

## 14. Canais do levantamento anterior, atualizados [O] (04/11, à tarde)
| Canal | Idioma | País | Views (manhã → tarde) | Inscritos | Vídeos | Mediana longos | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| Atlas del Tiempo | es | ? | 81.434 → (cache) | 729 → 735 | 27 → 28 | 743 | Mossad 33,1 mil (mediana fórmula+org 11,2 mil) |
| Te lo Pinto | es | ES | 121,29 mi → 121,53 mi | 594 → 595 mil | 310 | 180 mil | KGB 139 mil (fórmula); canal: 2,78 mi |
| Historia Total | es | US | 743.120 → 752.752 | 1.590 → 1.600 | 13 | 639 | Israel 737 mil |
| Abre la Historia | es | ES | 51.548 → 51.918 | 281 | 7 | 591 | Israel 49 mil |
| Cronopaís | es | ? | 34.084 | 154 → 159 | 9 | 1,0 mil | Alemanha 20 mil |
| Siglos y Fronteras | es | US | 18.806 | 254 | 12 | 121 | Haiti 17,5 mil |
| Historia Ágil | es | ? | 21.703 | 109 → 110 | 13 | 512 | Roma 17,9 mil |
| Historia con Monóculo | es | ? | 3.850 → 4.957 | 31 → 34 | 7 | 357 | Irã 4,6 mil |
| Historias Reales de Espías | es | MX | 914.969 | 8.080 | 73 | 5,7 mil | 145 mil |
| Historia Incomprendida | es | US | 989,8 mi → 989,9 mi | 4,46 mi | 1.766 | 103 mil | 685 mil |
| Traço Curioso | pt | BR | 742.989 | 7.280 | 64 | 537 | Mundo 610 mil |
| History Easy Guide | pt | ? | 33.458 | 369 → 378 | 13 → 14 | 603 | 1ª Guerra 25 mil |
| Depois do Poder | pt | BR | 11.845 | 132 → 133 | 2 | 6,2 mil | França 11,6 mil |
| Canal Outro Ponto | pt | ? | 18.243 | 115 | 11 | 637 | Roma 8,7 mil |
| Fragmentos da História | pt | BR | 2,28 mi | 24.100 | 196 | 13,8 mil | 121 mil |
| Total History | pt | BR | 7,48 mi | 72.500 | 67 | 33,9 mil | Portugal 2,24 mi |
| Classé Secret Défense | fr | FR | 384.863 → 385.403 | 5.170 | 99 | 27,2 mil | 94 mil |
| Archives Soviétiques | fr | ? | 255.251 | 3.300 | 52 | 1,1 mil | KGB 62,7 mil |
| Histoires Vraies d'Espions | fr | FR | 511.632 | 4.700 | 73 | 3,6 mil | 53,6 mil |
| Simplicissimus | de | DE | 673,9 mi | 2,6 mi | 524 | 2,04 mi | 5,81 mi |

Nota: o `viewCount` do canal na API é atualizado com atraso, então a maioria não mudou em 6 h; as views dos vídeos (usadas nas medianas) são as do momento.

## 15. Leitura para a decisão do idioma [I]
| Idioma | Demanda C4 (mediana top-10) [O] | Vídeos C4 2026 > 100 mil [O] | Concorrência no molde [O] | RPM relativo [I] | Revisão nativa nossa | Leitura |
|---|---|---|---|---|---|---|
| es | 401 mil | 41 | 1 ocupante pequeno (Atlas, 735 insc.) + 12 clones mortos | 0,25–0,4× | não | **melhor relação demanda × concorrência, com prova direta** (Atlas) |
| fr | 623 mil | 16 | 1 clone morto | 0,5–0,7× | não | maior RPM, vaga total; demanda dominada por TV |
| pt | 229 mil | 21 | 3 clones mortos (um "Dossiê Completo") | 0,25–0,35× | **sim** | vaga total, demanda menor; é o único idioma que revisamos |
| en | 1,78 mi | 112 | 101 canais, 91 clones | 1× | parcial | não entrar |
| de | 44,7 mil | 4 | 6 clones mortos | ~0,8–1× | não | só Stasi/SS |
| it | 33,1 mil | 4 | 2 clones | ~0,4–0,6× | não | só máfia |

Sugestão para o Rodrigo decidir [I]:
1. **Se a régua for "maior chance de pegar":** es. O Atlas del Tiempo mostrou em 7 dias que um canal com 735 inscritos tira 15–33 mil views por vídeo de organização em es. O ocupante é pequeno e começou há 1 semana.
2. **Se a régua for "receita por view":** fr, com o custo de voz e revisão em francês.
3. **Se a régua for "operar com qualidade sem revisor externo":** pt, com o teto de demanda mais baixo (≈ 57% do es) e a necessidade de trocar o nome (já existe "Dossiê Completo").
4. Em qualquer idioma: começar pelos temas com demanda **no idioma** (pt: Mossad, CIA, SS, Gestapo, KGB; evitar Stasi e MI6. es: CIA, Mossad, KGB, SS, cartel, máfia), porque a ordem do Archive (en) não se transfere 1:1.
5. Janela: 13 clones es e 3 pt surgiram em ~3 semanas. Quem entrar deve publicar os 5–6 temas fortes nos primeiros 10 dias [I].

### Nome e handle (o canal já existe) [O]
- O Rodrigo criou o canal **"Dossiê em Minutos"** (`UCVCYqeuCwTWC7Lqez_qeWRA`, handle `@dossieminutos`, 0 vídeos em 04/11; ver `pesquisa/archive-in-minutes/AVISO-CANAL-CRIADO.md`). Nome e handle podem ser trocados no YouTube, então o idioma continua em aberto.
- Em pt já existem "Dossiê Completo" (clone do molde, 7 vídeos) e "Dossiê Oculto" (fez MI6/Kim Philby). O nome é parecido, mas os dois canais são minúsculos [O].
- Se ganhar **es**: "Dossier en Minutos". Os handles `@dossierenminutos`, `@eldossierenminutos`, `@dossiersenminutos` e `@expedienteenminutos` estavam livres em 04/11 (`channels.list forHandle`). Evite "Archivo/Archivos en Minutos", "Archivo Minuto" e "Historia en Minutos": todos já são clones [O].
- Se ganhar **fr**: "Dossier en Minutes" (`@dossierenminutes` livre em 04/11) [O].

## Limitações
- Amostra: até 30–40 resultados por consulta; somas e medianas comparam idiomas, mas não medem o mercado inteiro.
- Idioma do vídeo pelo `defaultAudioLanguage`, que às vezes vem errado (há ruído em hi/ar/ja: vídeos em espanhol ou russo caíram nesses idiomas; ver `dados/demanda.json`).
- Temas com nomes ambíguos: "KGB" (gangue em ja), "SS" (navio em hi), "Stasi" (caso Garlasco em it) e ficção em máfia/cartel/FBI. O núcleo C4 é o mais limpo.
- Clones com 0–3 dias têm views quase nulas por idade; a "mediana dos clones" mistura canais de 1 dia e de 4 semanas. Mesmo os de 3–4 semanas (es: Pestaña de Crónicas, Construido sobre ti; en: dezenas) estão abaixo de 300 [O].
- RPM: fatores da tabela do `playbooks/garimpo-tendencias.md` (en, es, pt, fr); de, it, ru, hi e ar são estimativas sem fonte própria [I].
- Monetização na Rússia: conhecimento de política, não reconsultado hoje [I].

## Arquivos
- Scripts: `pesquisa/archive-in-minutes/idioma/scripts/` (`buscar.py`, `clones.py`, `sugestoes.py`, `enriquecer.py`, `canais.py`, `demanda.py`, `analise_canais.py`, `resumo.py`, `tabelas.py`, `comum.py`). Rode-os de `tools/` com `tools/.venv/bin/python`; os que só leem dados com `python3 -I`.
- Dados: `pesquisa/archive-in-minutes/idioma/dados/`. O resumo é `resumo_idiomas.json`; os outros são `demanda.json`, `concorrencia.json`, `sugestoes.json`, `candidatos_formula.json` e `paises_canais.json`. Os brutos (`busca.jsonl`, `busca_clones.jsonl`, `videos_api.json`, `canais_api.json`) estão em `.gz`; descompacte (`gunzip -k`) antes de rodar os scripts de novo.
