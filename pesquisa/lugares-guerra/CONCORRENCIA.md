# CONCORRÊNCIA e DEMANDA: canal de "lugares / arquivos de guerra" (Where They Stood + Civil War Fine Print)

Data: 2026-11-12 · Agente: Tendências (etapa 1, 3b-concorrência e demanda en do `playbooks/novo-canal.md`) · Dados brutos: `pesquisa/lugares-guerra/dados.json` e `idioma/dados/` · Scripts: `idioma/scripts/`.
Legenda: **[O]** observado (YouTube Data API, busca do YouTube via yt-dlp + WARP) · **[I]** inferido ou estimativa. Idade do canal = 1º vídeo lido (ou criação, quando só li os 100 vídeos mais novos).

---

## Resumo executivo

1. **A fórmula do Where They Stood (WTS) tem dono e clones mortos [O].** Em 5 semanas surgiram **21 canais** copiando o título/tema do Iwo Jima (17 deles abertos depois de 27/09). Mediana das medianas: **28 views**; só **1** canal passa de 10 mil no melhor vídeo; **0** passam de 5 mil de mediana. Quase todos repetem **o mesmo lugar** (14 títulos da mesma pergunta sobre Iwo Jima).
2. **Mas a família "por que X ainda está lá / por que não pode visitar" já tem 3 canais de verdade com tração, e o WTS não foi o primeiro [O]:** Forgotten Fleet (7,27 mi de views em 254 dias, 15,2 mil inscritos, mediana 10,8 mil, hits de 1,16 mi, 777 mil, 583 mil, 15 posts em 30 d), Ship Tales (1,55 mi em 48 dias, 1,07 mil inscritos; "Why Did America Raise Pearl Harbor's Other Battleships" 943 mil) e Insight Ship (USS Utah 469 mil). Mais IT'S HISTORY (894 mil inscritos; "Why Cheyenne Mountain is Totally Forbidden" 313 mil em 2025). O formato vem funcionando desde 2024 com tema "lugar/navio dos EUA"; o WTS acertou o tema mais famoso.
3. **Teto do nicho (c) [O]:** Yarnhub 18,7 mi views/mês (3,42 mi inscritos), Mark Felton 4,2 mi/mês, Kings and Generals 4,8 mi/mês, Operations Room 1,1 mi/mês; canais novos de guerra com tração: Warlines (2,33 mi em 141 d), WW2 Vellob (2,0 mi), Frontline Echoes (1,46 mi em 110 d). Ou seja: o nicho paga e cabe canal pequeno novo, mas a mediana típica de canal novo bom é **~1–10 mil**, não 1 mi.
4. **Civil War Fine Print (CWFP) é cedo demais para julgar [O]:** 5 dias, 1 longo de 882 mil e o 2º longo com 5 mil; 1 Short de 209 mil. Só 2 clones diretos (o melhor com 62 views). O gênero "fotos que você não deveria ver" existe em compilação de 100+ fotos (canais Mystery in History, com 7,6 mi de views, e Past in Pictures, com 1,0 mi), que não é o molde do CWFP.
5. **Demanda en por tema (34 temas, §4) [O]:** o ranking bruto é dominado por documentário de batalha de TV. Tirando batalha/ataque/vlog ("só lugar"), os que importam são **Diego Garcia (836 mil de mediana, 12 vídeos ≥100 mil), Iwo Jima (785 mil; já tomado), Falklands (714 mil), Pearl Harbor (414 mil, 9 ≥100 mil no último ano), Omaha (383 mil; WTS), Bikini (207 mil)**. Midway e Wake "só lugar" são fracos (96 mil e 104 mil), mas têm vídeos-teto de 3,3 mi e 17 mi.
6. **Risco de hit único [O] (§5):** WTS = 87% das views em 1 vídeo (Iwo Jima; foi o **vídeo nº 2**, não o nº 1), mas a **mediana sem o hit é 29,4 mil** e 7 de 10 vídeos passam de 25 mil; CWFP = 79% das views totais (99% dos longos) em 1 vídeo. Compatível com o padrão do `entrega-youtube-2026-11/RELATORIO.md` (tema já provado + queda de 13–150× depois), com uma diferença: o WTS não caiu a zero.
7. **Cota gasta: 1.085 unidades, 0 `search.list`** (videos.list 132 + channels.list 87 + playlistItems/videos 866; 440 buscas via yt-dlp/WARP sem cota; WARP funcionou o tempo todo).

---

## 1. Método
- **Buscas [O]:** 440 consultas no yt-dlp (WARP, 0 cota), 25–30 resultados cada: 108 de concorrência (fórmula, clones WTS, clones CWFP, nicho), 170 de demanda (34 temas × 5 consultas: "why can't you visit <tema>" em relevância e "este ano por views", "<tema> today", "<tema> documentary" em 2 ordens) e 162 de idioma. 6.381 vídeos únicos lidos com `videos.list`; 4.296 canais com `channels.list`; **301 canais** com os 100 vídeos mais novos lidos (`playlistItems` + `videos.list`) para views/mês e mediana. As tabelas abaixo trazem **81 canais** (os demais 220 ficam em `dados.json`).
- **Views/mês [I]:** canal < 1 ano = views ÷ idade × 30 (superestima canal com 1 hit: ver §5); canal antigo = views dos longos dos últimos 90 dias ÷ 3, só dentro dos 100 vídeos mais novos (**piso**). **Mediana** = só vídeos ≥ 4 min. Idade pelo 1º vídeo lido; "+" nos vídeos = só os 100 mais novos.
- **Classificação [I]:** por regex no título (fórmula: "can't visit / off limits / what's still under-at / why is X still there / sealed since…") + lugar de guerra; a classificação é minha e há zonas cinzentas (ex.: Dann e Frames of the Past entram como clone por 1 título).
- **Limites:** busca do YouTube devolve amostra (top ~30 por consulta), não o universo; canais sem nenhum título na amostra ficam de fora.

## 2. Mapa de concorrência

### Referências
| Canal | 1º vídeo (idade) | Vídeos (longos+shorts; + = só os 100 mais novos lidos) | Views | Inscritos | Views/mês | Mediana (longos) | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| [Where They Stood](https://www.youtube.com/channel/UCUt7wPSxHRObHObdAW-26JQ) | 2026-10-03 (40 d) | 11+0 | 5.184.153 | 3.670 | 3.888.114 | 29.735 | 4.535.929: Why Can't You Visit Iwo Jima? |
| [Civil War Fine Print](https://www.youtube.com/channel/UCE1gBqF9TF6JswS0zsxdGTg) | 2026-11-07 (5 d) | 2+4 | 919.508 | 3.100 | 5.517.048 | 443.896 | 882.770: The Pictures of Lincoln's Death You Weren't Supp |

### (a) Fórmula exata ("Why can't you visit / What's still under-at / Why is X still there"), canais com < 1 ano
| Canal | 1º vídeo (idade) | Vídeos (longos+shorts; + = só os 100 mais novos lidos) | Views | Inscritos | Views/mês | Mediana (longos) | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| [Forgotten Fleet](https://www.youtube.com/channel/UCyL5J-lo3XuYPPOiXvzbAWw) | 2026-03-03 (254 d) | 92+0 | 7.274.047 | 15.200 | 859.139 | 10.838 | 1.160.025: Why The Uss Arizona Can Never Be Raised |
| [Park Vibes](https://www.youtube.com/channel/UCYclu9eyo5EwGF-zSDDWNtw) | 2025-09-22 (1.1 a) | 24+0 | 5.300.357 | 33.700 | 151.526 | 42.406 | 1.300.976: What's Hidden on Hawaii's Forbidden Island? |
| [Ship Tales](https://www.youtube.com/channel/UCBPScyNOC9MUXSvRIg6Rs1Q) | 2026-09-25 (48 d) | 28+0 | 1.545.625 | 1.070 | 966.015 | 1.737 | 942.605: Why Did America Raise Pearl Harbor's Other Battl |
| [Curious Britain](https://www.youtube.com/channel/UCV2OhUlOMRRS5LHzD0XjM2A) | 2026-02-27 (258 d) | 68+4 | 1.151.200 | 6.910 | 133.860 | 3.000 | 219.342: 10 Creepy Ghost Towns Hidden Across the UK - Wha |
| [Earthyphus](https://www.youtube.com/channel/UCnJmHXWRscSezcZKSsSeXsA) | 2026-05-09 (187 d) | 8+0 | 1.123.587 | 1.530 | 180.254 | 25.777 | 921.933: Every Forbidden Island You're Not Allowed to Vis |
| [Ivan Old Army](https://www.youtube.com/channel/UCFM-Eh0E-9UsBrzVB1QDbyw) | 2026-07-15 (120 d) | 48+0 | 765.813 | 1.560 | 191.453 | 887 | 159.476: Why the P-51 Had a Scoop Under Its Belly — And t |
| [Insight Ship](https://www.youtube.com/channel/UC85c3UiXENXF8KvSh61jk4A) | 2026-04-16 (210 d) | 19+0 | 513.709 | 824 | 73.387 | 813 | 469.480: Why is the USS Utah Still at Pearl Harbor |
| [History Unfolded Films](https://www.youtube.com/channel/UCGCKfyQCYiYhAM5o7yzcD_A) | 2026-10-25 (18 d) | 10+24 | 144.326 | 157 | 240.543 | 163 | 2.493: The Forbidden American Island in the Middle of t |
| [Hollow Cairn](https://www.youtube.com/channel/UCD_DrxLSWHZeuleLw2RnGMg) | 2026-10-11 (32 d) | 11+0 | 136.578 | 380 | 128.041 | 872 | 68.620: Gettysburg Archaeology Who Is Still Buried Benea |
| [Sterling Map Mysteries](https://www.youtube.com/channel/UCVxRbbOdELNvj-OGeNWsDCg) | 2026-07-21 (114 d) | 8+0 | 117.966 | 257 | 31.043 | 674 | 111.692: They Were Forced to Leave Forever | Diego Garcia |
| [Explain By Atish](https://www.youtube.com/channel/UCf3Tahksap1DDjyKT2qL7ng) | 2026-08-16 (88 d) | 15+5 | 110.965 | 222 | 37.828 | 2.953 | 38.209: 10 Most Horrifying Places Hidden in the Ocean |
| [Verboten](https://www.youtube.com/channel/UCoty8Ah09w-LbSI40PO03Hw) | 2026-10-13 (30 d) | 13+36 | 31.268 | 37 | 31.268 | 27 | 597: Why Nobody Is Allowed Inside Area 51 |
| [MJ MYSTERY GLOBE](https://www.youtube.com/channel/UCQhZkAqNbU1qKDD5OLuuEHQ) | 2026-05-06 (190 d) | 41+55 | 23.592 | 203 | 3.725 | 5 | 559: World’s Deadliest Island Why the Navy Guards Sna |
| [TheHiddenBases](https://www.youtube.com/channel/UCO7sXwtwE8CrXvDEKCVDlkQ) | 2026-07-24 (111 d) | 29+0 | 19.022 | 130 | 5.141 | 144 | 11.027: The real reason Area 51 was secret - It wasn't a |
| [Strange World Vault](https://www.youtube.com/channel/UC1wHBq-ZOVqr9ZiIeFWDK9w) | 2026-07-03 (132 d) | 18+19 | 7.298 | 35 | 1.658 | 126 | 636: Drilled 12 Kilometers Down InTo The Earth —Then  |
| [Unreal Destinations](https://www.youtube.com/channel/UCZVC5u57-Rr5Cp3dyqr-Sng) | 2026-08-30 (74 d) | 33+24 | 7.055 | 24 | 2.860 | 26 | 251: Clipperton: The Poisoned Island Nobody Will Clai |
| [Unreachable Places](https://www.youtube.com/channel/UC5OenJkc7ToDgTVJSfVGZBA) | 2026-11-05 (7 d) | 5+15 | 5.447 | 7 | 23.344 | 50 | 334: Snake Island Brazil: The Island Whose Guards Are |

### (b1) Clones do Where They Stood (título/ideia do Iwo Jima copiados; 1º vídeo ≥ 09/2026 na maioria)
| Canal | 1º vídeo (idade) | Vídeos | Views | Inscritos | Mediana (longos) | Título-clone (views) | Melhor vídeo do canal |
|---|---|---|---|---|---|---|---|
| [Frames of the Past](https://www.youtube.com/channel/UCsy-u115ttcBBf6rA7J19TA) | 2026-10-22 (21 d) | 21+0 | 61.239 | 227 | 140 | Why Can’t You Visit Iwo Jima? (The 80-Year Secret) (635) | 67.626 |
| [Fallow Empire](https://www.youtube.com/channel/UCwpwyzGn3szBcSyWkbTgdmA) | 2026-06-17 (148 d) | 35+0 | 34.173 | 110 | 127 | 80 Years Later, Iwo Jima Is Still Off Limits (0) | 12.719 |
| [WW2 Time Capsule](https://www.youtube.com/channel/UC0fQ1FHHNmCR_dYJTRFCLOg) | 2025-11-26 (351 d) | 100+0+ | 28.476 | 133 | 35 | What's Still Inside the USS Arizona? (192) | 10.424 |
| [Hidden War Stories](https://www.youtube.com/channel/UCUd17ZYtW-61E57coBRD34Q) | 2026-07-27 (108 d) | 44+56+ | 26.739 | 15 | 2 | Famous for the flag raising, Iwo Jima is strictly off-limits as a military  (0) | 463 |
| [Aquila Strike](https://www.youtube.com/channel/UCU3wuvjhntTBcumRrJlxFQQ) | 2026-04-15 (211 d) | 11+15 | 23.151 | 31 | 38 | Why You’re Not Allowed on Iwo Jima (The Real Reason) (58) | 394 |
| [walter](https://www.youtube.com/channel/UCkGUpqkLZV2TiZR538d9cZQ) | 2026-10-03 (40 d) | 33+1 | 22.183 | 1.040 | 48 | Why Can't You Visit Wake Island ? (36) | 4.344 |
| [Dann](https://www.youtube.com/channel/UCr08HJDvi-vP-7t13BM5l1g) | 2026-10-08 (35 d) | 7+0 | 11.003 | 31 | 570 | Sealed Since D-Day: What We Found Inside This Nazi Battery (214) | 6.478 |
| [WW2 Sitrep](https://www.youtube.com/channel/UCCXco7fAxDgqZ8G8jqPKJsw) | 2026-10-29 (14 d) | 9+0 | 10.719 | 13 | 640 | Why Can't You Visit Iwo Jima? (910) | 7.015 |
| [Once Upon a Fact](https://www.youtube.com/channel/UClpdPABVZpEQuTLbeqHuYpw) | 2026-10-16 (27 d) | 15+19 | 6.220 | 21 | 8 | What's Still Under the Water at Omaha Beach? — The Sunken Tanks of D-Day (49) | 312 |
| [Long After The Guns](https://www.youtube.com/channel/UCXIMjn_vXy3W2_hb2c25HJw) | 2026-10-29 (14 d) | 7+0 | 3.876 | 24 | 297 | Why Is America Rebuilding Tinian Island, Where the Atomic Bombs Took Off? (89) | 6.247 |
| [War As It Was](https://www.youtube.com/channel/UCB4mJQ6fwkvhM17eBi1sg3A) | 2026-10-09 (34 d) | 7+0 | 1.155 | 3 | 31 | February 19, 1945 — Why Can't You Visit Iwo Jima? (58) | 599 |
| [HISTORY MCM STUDIO](https://www.youtube.com/channel/UCZcwfe7hHNFwi532nhQFF9g) | 2026-10-20 (23 d) | 11+1 | 577 | 0 | 28 | Why You’re Not Allowed to Visit Iwo Jima | Full Documentary (28) | 221 |
| [What remains](https://www.youtube.com/channel/UC2oY5U8ZeNaUUB1r3TCBeGw) | 2026-11-01 (11 d) | 5+0 | 249 | 1 | 28 | Why Can't You Go Inside the Tunnels of Iwo Jima? (103) | 103 |
| [Relic Ground](https://www.youtube.com/channel/UCagqlKD7Fb5wo1yeshlSbRA) | 2026-11-10 (2 d) | 3+0 | 188 | 3 | 88 | What's Still Left on Peleliu After 82 Years? (88) | 103 |
| [Forgotten Grounds](https://www.youtube.com/channel/UCgETYKxSkLjtX65qSMYAmKA) | 2026-10-27 (16 d) | 12+0 | 178 | 0 | 10 | Why Can't You Visit Iwo Jima? The Forbidden Island of Sulfur and Silence (40) | 56 |
| [Off Limits for us](https://www.youtube.com/channel/UCDSJj0Y-9jwdaRbX9ouZbCw) | 2026-11-08 (4 d) | 4+0 | 63 | 0 | 9 | Why You Still Can't Visit Iwo Jima (44) | 44 |
| [Harkaran History](https://www.youtube.com/channel/UC88163nhfcF1jyvR5fw-Zmw) | 2026-11-02 (10 d) | 11+0 | 18 | 0 | 1 | Why You Still Can’t Visit Iwo Jima (The 80-Year Secret) (1) | 6 |
| [Restricted Ground](https://www.youtube.com/channel/UCG3n2xnt7rGorYa4VJrsr7w) | 2026-11-01 (11 d) | 5+0 | 16 | 0 | 4 | Midway Today: The Battlefield Nobody Is Allowed to Visit (4) | 6 |
| [TheForbiddenPlace](https://www.youtube.com/channel/UCJ2se9NYKz8hrlcLqjgYN3Q) | 2026-11-06 (6 d) | 3+0 | 11 | 0 | 4 | Why Can't You Visit Iwo Jima? (8) | 8 |
| [OffLimitsHistory](https://www.youtube.com/channel/UCuCW8UVE94fGEokIAfKePYQ) | 2026-11-10 (2 d) | 1+0 | 1 | 0 | 1 | Why Can't You Visit Iwo Jima? (1) | 1 |
| [The War Stayed Here](https://www.youtube.com/channel/UC1ePZY84U-yn3UwUSBiIsNg) | 2026-11-05 (7 d) | 1+0 | 0 | 0 | 0 | Why Can't You Visit Bikini Atoll? (0) | 0 |

### (b2) Clones e parentes do Civil War Fine Print (ângulo "documentos / fotos que você não deveria ver")
| Canal | 1º vídeo (idade) | Vídeos (longos+shorts; + = só os 100 mais novos lidos) | Views | Inscritos | Views/mês | Mediana (longos) | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| [Markets of the Past](https://www.youtube.com/channel/UCPDCiU00ugujWP8H2HMbiFA) | 2026-04-10 (216 d) | 100+0+ | 15.173.088 | 114.000 | 2.107.373 | 46.851 | 1.837.616: The Real Reason Hitler Never Invaded Switzerland |
| [Mystery in History](https://www.youtube.com/channel/UCLCvsfloZLDyeMG-ytrl1Aw) | 2025-04-09 (1.6 a) | 100+0+ | 7.635.630 | 49.500 | 865.520 | 2.670 | 793.507: 🔴▶ 74 BANNED Circus FREAKS That Actually EXISTED |
| [Nation Of History](https://www.youtube.com/channel/UC-PWOvaz3n-R95-0VeDAw-w) | 2025-04-17 (1.6 a) | 100+0+ | 3.427.789 | 22.500 | 0 | 658 | 279.428: 📷▶ 24 BANNED Circus FREAKS That Actually EXISTED |
| [Past in Pictures](https://www.youtube.com/channel/UCGdiC5iGtycHkcQnQAX_18A) | 2025-11-28 (349 d) | 83+0 | 1.003.421 | 7.970 | 86.253 | 441 | 597.933: 📸▶ 44 BANNED Circus FREAKS That Actually EXISTED |
| [Cloaked History](https://www.youtube.com/channel/UCyTRQd_sRvD7yYBQLL2G66Q) | 2026-03-11 (246 d) | 42+0 | 404.378 | 3.640 | 49.314 | 389 | 235.259: History Lied About Lee’s Surrender |
| [Lens History](https://www.youtube.com/channel/UCiqeKdlWrVmAZCZ3uoJS0qA) | 2025-10-09 (1.1 a) | 79+0 | 394.862 | 1.550 | 549 | 387 | 105.777: 🔴Shocking Photos Of Giant Objects You Won’t Beli |
| [The Union And Confederacy](https://www.youtube.com/channel/UCpLWja8j8frXIspMj1QooVw) | 2026-03-02 (255 d) | 16+0 | 18.948 | 78 | 2.229 | 377 | 7.995: Why Did Grant Choose Confederate Generals as Pal |
| [Shrapnel](https://www.youtube.com/channel/UC--YDb_EJ348d4SucEsglFg) | 2026-11-09 (3 d) | 4+0 | 51 | 0 | 510 | 11 | 45: What the Japanese Heard on the Radio the Day Jap |

### (c) Mesmo nicho (guerra/lugares/história militar), outro formato: dá o teto
| Canal | 1º vídeo (idade) | Vídeos (longos+shorts; + = só os 100 mais novos lidos) | Views | Inscritos | Views/mês | Mediana (longos) | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| [Yarnhub](https://www.youtube.com/channel/UC-f2WBfSCZiu0bOBydjot3w) | 2019-06-17 (7.4 a) | 83+17+ | 967.213.631 | 3.420.000 | 18.655.052 | 5.052.305 | 34.120.458: How a Nighthawk Was Shot Down |
| [Ambrose Discovery](https://www.youtube.com/channel/UCAVxoa11gRHcit9_onvTkMQ) | 2026-07-15 (120 d) | 100+0+ | 28.907.730 | 105.000 | 7.226.932 | 35.311 | 1.104.740: A Drone Flew Over the Ice Wall of Antarctica — W |
| [War Stories](https://www.youtube.com/channel/UC3fOzMSxcmCXZLmAM9vy1IQ) | 2020-07-30 (6.3 a) | 100+0+ | 374.970.870 | 1.370.000 | 6.753.695 | 35.736 | 9.768.713: Afghanistan Uncensored: Rare Footage From The Ba |
| [Top Fives](https://www.youtube.com/channel/UCbAlVnKhbGLK78GsSemQXxw) | 2015-03-28 (11.6 a) | 100+0+ | 1.392.934.819 | 3.180.000 | 6.449.717 | 85.167 | 2.670.082: 10 Places Humans SEALED SHUT |
| [Kings and Generals](https://www.youtube.com/channel/UCMmaBzfCCwZ2KqaBJjkj0fw) | 2016-05-07 (10.5 a) | 49+51+ | 1.106.768.123 | 4.220.000 | 4.835.403 | 277.422 | 1.024.663: War of the Spanish Succession: All Battles and E |
| [Mark Felton Productions](https://www.youtube.com/channel/UCfCKvREB11-fxyotS1ONgww) | 2017-10-27 (9.0 a) | 100+0+ | 1.055.690.319 | 2.440.000 | 4.210.419 | 362.201 | 2.230.720: The Shocking State of Britain's Navy 2026 |
| [Historically](https://www.youtube.com/channel/UCoZd78hRUdxxsuGiABuHF_A) | 2023-04-15 (3.6 a) | 22+61 | 506.149.841 | 1.640.000 | 3.832.486 | 2.468.741 | 10.638.545: The ENTIRE History of ROME [No AI] |
| [Places](https://www.youtube.com/channel/UCIPT_mWxS6QU6KJxLa_aZTA) | 2023-07-17 (3.3 a) | 92+8+ | 87.626.689 | 455.000 | 3.689.253 | 307.574 | 1.587.804: Afghanistan is Now So Much Worse Than You Think. |
| [Timeline - World History Docum](https://www.youtube.com/channel/UC88lvyJe7aHZmcvzvubDFRg) | 2017-01-17 (9.8 a) | 100+0+ | 1.092.521.671 | 5.910.000 | 3.607.454 | 40.367 | 2.341.891: Operation Moshtarak: The Uncensored Truth Of The |
| [History Hit](https://www.youtube.com/channel/UCZwU2G-KVl-P-O-B35chZOQ) | 2008-07-04 (18.4 a) | 100+0+ | 387.089.879 | 2.020.000 | 3.351.859 | 222.731 | 3.402.696: WW2 Historians LOVE Inglourious Basterds |
| [Exploring With Josh](https://www.youtube.com/channel/UCNYsIqBwQyhnNDVf7SXJV9w) | 2013-08-19 (13.2 a) | 100+0+ | 638.293.250 | 4.850.000 | 2.702.921 | 337.915 | 2.185.968: The Ship More Haunted Than the Queen Mary (ft. S |
| [Simple History](https://www.youtube.com/channel/UC510QYlOlKNyhy_zdQxnGYw) | 2014-10-01 (12.1 a) | 21+79+ | 1.714.136.884 | 5.120.000 | 2.574.431 | 343.981 | 1.321.755: Gun Tricks that can give you an Advantage in Com |
| [IT'S HISTORY](https://www.youtube.com/channel/UCzIZ8HrzDgc-pNQDUG6avBA) | 2014-06-20 (12.4 a) | 100+0+ | 173.758.994 | 894.000 | 2.130.238 | 116.066 | 1.008.663: Why This Highway Runs Through Chicago’s Biggest  |
| [Real Time History](https://www.youtube.com/channel/UCB1eDEd1AYG3YrRIJSZzMOQ) | 2021-06-29 (5.4 a) | 81+0 | 131.250.673 | 768.000 | 1.785.054 | 1.215.768 | 7.534.274: Desert Storm: The Gulf War 1990-1991 (Documentar |
| [Battle Guide](https://www.youtube.com/channel/UCq3-NSjXkXI-S_XTbj9bWog) | 2020-07-31 (6.3 a) | 97+3+ | 123.134.240 | 510.000 | 1.625.873 | 462.241 | 4.524.762: Operation Anthropoid: The Most Important Assassi |
| [The History Guy: History Deser](https://www.youtube.com/channel/UC4sEmXUuWIFlxRIFBRV6VXQ) | 2017-01-29 (9.8 a) | 100+0+ | 438.824.407 | 1.650.000 | 1.363.436 | 47.487 | 577.962: The B-32 "Dominator." |
| [HistoryMarche](https://www.youtube.com/channel/UC8MX9ECowgDMTOnFTE8EUJw) | 2017-04-24 (9.6 a) | 96+4+ | 264.068.345 | 1.340.000 | 1.271.074 | 435.962 | 2.335.409: How One Rifle Destroyed the Austrian Empire: Bat |
| [The Operations Room](https://www.youtube.com/channel/UCnZJt7yQw5IztVwe-Dscd-Q) | 2019-04-17 (7.6 a) | 68+32+ | 262.344.468 | 1.450.000 | 1.084.264 | 540.008 | 2.493.336: Battle of Leyte Gulf - Complete Animated Documen |
| [The History Underground](https://www.youtube.com/channel/UCUP4XFMrsJG5_AbG6ZYBVFA) | 2019-05-20 (7.5 a) | 85+15+ | 159.403.183 | 806.000 | 772.411 | 39.625 | 670.810: The Incredible Things American GIs Sent Home Fro |
| [Lost US Towns](https://www.youtube.com/channel/UCtA_cgHrKWtqgBMc3vxlzIQ) | 2026-03-11 (246 d) | 100+0+ | 6.216.191 | 33.100 | 758.072 | 22.535 | 228.517: 11 Infamous American Murder Houses That Are Stil |
| [Agent Flappy](https://www.youtube.com/channel/UCRi2h75k0cAsMin5TYxZJgw) | 2025-06-13 (1.4 a) | 54+6 | 28.354.277 | 152.000 | 586.883 | 264.107 | 7.373.364: Every US President's Death Explained in 21 Minut |
| [Military Heroes](https://www.youtube.com/channel/UCzV8tU9puZ9xHtCJHUvEClw) | 2021-10-05 (5.1 a) | 85+15+ | 59.430.524 | 305.000 | 526.798 | 14.356 | 101.121: Midway, Enterprise and the Pacific War *Marathon |
| [Jared Owen](https://www.youtube.com/channel/UCbsfyGlrjrKQC0gbzK0-EiA) | 2010-04-13 (16.6 a) | 63+37+ | 545.613.840 | 4.450.000 | 502.216 | 4.542.949 | 65.001.096: How does a Tank work? (M1A2 Abrams) |
| [Warlines](https://www.youtube.com/channel/UCAacFG-Z5GuE3FXiqoKIZsA) | 2026-06-24 (141 d) | 100+0+ | 2.326.425 | 6.750 | 494.984 | 10.620 | 133.522: Japan Sent 1,500 Men to Take Milne Bay — 9,458 W |
| [Frontline Echoes - Harold Warf](https://www.youtube.com/channel/UCngI29l4HbFr3pHf8XnRX3g) | 2026-07-25 (110 d) | 58+0 | 1.458.037 | 2.610 | 397.646 | 746 | 426.101: They Opened a Sealed WW2 Tunnel — 12,000 German  |
| [American Battlefield Trust](https://www.youtube.com/channel/UCUfsbWIraXIl7a6HKSJINUg) | 2009-03-20 (17.7 a) | 66+34+ | 134.446.409 | 512.000 | 268.112 | 22.049 | 479.991: The Alamo | Exclusive VIP Tour (2026) |
| [WW2 Wayfinder](https://www.youtube.com/channel/UC-yHzFbop7FHp5le0JYCg-A) | 2022-05-08 (4.5 a) | 7+93+ | 108.380.464 | 259.000 | 255.726 | 47.359 | 425.344: Lost WW2 Locations - Germany 1945 Then and Now ( |
| [Atlas Pro](https://www.youtube.com/channel/UCz1oFxMrgrQ82-276UCOU9w) | 2018-01-07 (8.9 a) | 48+52+ | 154.509.021 | 1.280.000 | 223.155 | 196.840 | 1.415.988: Islands That AREN'T Actually Islands |
| [WW2 Vellob](https://www.youtube.com/channel/UCRYmjTWA-0OOVhRGECFtp7w) | 2025-11-29 (348 d) | 100+0+ | 2.007.201 | 7.110 | 173.034 | 1.050 | 321.423: Germany Lost D-Day in the First Ten Minutes — Be |
| [The Generals’ Oath](https://www.youtube.com/channel/UCbM0ekCWvlBf6buvnP7FvuQ) | 2025-12-31 (316 d) | 47+0 | 1.819.855 | 12.500 | 172.771 | 5.381 | 355.384: What Longstreet Understood About Grant That Lee  |
| [QUANTARA](https://www.youtube.com/channel/UCwO9_KTwY0tUF6lTiT_Okww) | 2025-09-28 (1.1 a) | 100+0+ | 21.067.020 | 48.000 | 24.573 | 378 | 16.921: Ukrainian Drone Footage Russia Tried to DELETE J |
| [ATLAS FILES](https://www.youtube.com/channel/UC_lQ5l82vlF939aNzAoirOw) | 2026-08-03 (101 d) | 40+0 | 9.915 | 44 | 2.945 | 79 | 1.701: The Raid Britain Couldn't Admit Happened |
| [The Intel Report](https://www.youtube.com/channel/UC7Ay_bxnYWSS9ZDPpqAE1RQ) | 2022-09-30 (4.1 a) | 58+2 | 33.298.921 | 280.000 | 0 | 303.605 | 3.123.020: Iwo Jima from the Japanese Infantryman's Perspec |

Resumo por grupo [O]: (a) fórmula exata (< 1 ano, 17 canais): mediana das medianas 813, 8 com vídeo ≥ 100 mil, 3 com mediana ≥ 5 mil · (b1) clones WTS (21): mediana das medianas 28, 0 com vídeo ≥ 100 mil (os 3 são canais de navio ou de outro assunto, não clones puros), mediana de inscritos 3 · (b2) CWFP e parentes (8): ignorar a mediana, o grupo mistura listas de fotos.

**Leituras [I]:**
- **Quem faz bem não é clone do Iwo Jima**: Forgotten Fleet, Ship Tales, Insight Ship e IT'S HISTORY fazem "por que X ainda está lá" com tema **diferente** a cada vídeo (navios de Pearl Harbor, Bismarck, PT-109; cidades dos EUA). Sugere que o motor é **curiosidade de uma pergunta concreta + lugar/objeto famoso dos EUA**, não o título exato do WTS.
- **Clone com título literal fracassa** (mediana 28; o melhor clone literal do Iwo Jima, WW2 Sitrep, tem 910 views; o melhor com outro lugar, Long After The Guns em Wake Island, 6,2 mil) [O]; hipótese: anti-spam do YouTube para conteúdo repetido e canais de 0–3 inscritos sem ritmo.
- **Teto realista de canal novo bom [I]:** Forgotten Fleet e Ship Tales chegam a ~0,9 mi views/mês com 1–15 mil inscritos, **mas** a mediana deles é 10,8 mil e 1,7 mil: a receita vem dos 3–4 hits de 0,5–1,2 mi por canal.
- **Ritmo:** Forgotten Fleet 15 vídeos em 30 d; Ship Tales 23; WTS 11 em 38 d. Quem tem tração posta quase diário [O]. Nosso ritmo humano de 3/semana é menor [I].

## 3. Ângulo "documentos" (Civil War Fine Print)
- **CWFP [O]:** 6 vídeos em 5 dias; longo 1 = 882 mil (14 min, retratos/fotos de época, título "The Pictures of Lincoln's Death You Weren't Supposed to See"); longo 2 = 5 mil ("What Happened to the Man Who Hosted General Lee's Surrender?"); Shorts 5 mil, 11,6 mil, **209 mil** ("They Stripped the Room Where the Civil War Ended") e 3,2 mil. Mediana dos Shorts 8,3 mil.
- **Clones diretos [O]:** The Union And Confederacy (copiou o título do Lincoln em 11/11: 62 views; canal com 16 vídeos e 78 inscritos) e Shrapnel ("Why Weren't You Supposed to See These Pictures of Lincoln's Death?", 7 views). Cloaked History ("History Lied About Lee's Surrender", 235 mil, 3,6 mil inscritos, fev/2026) é parente anterior, mediana 389.
- **Buscas do gênero [O]:** "Photos you weren't supposed to see" devolve compilações antigas (WhoRemembers 4,5 mi, Mystery in History 229 mil) e o clickbait "100+ photos"; "declassified documents" devolve listas de segredos da CIA (Visual Venture 1,07 mi); "the telegram that changed history" devolve Zimmermann (Extra History 662 mil). **Não há** um canal de longos com 1 documento por vídeo além do CWFP [O, na amostra].
- **Leitura [I]:** o CWFP prova que "1 documento/foto + 1 pessoa real" vende; o 2º longo (5 mil) mostra que a **escolha do tema (Lincoln) carrega**. É a mesma lição da fórmula do WTS: o tema pesa mais que o hook.

## 4. Demanda em inglês por tema (34 temas)
Filtro: vídeos ≥ 4 min, não ao vivo, título cita o tema, idioma en; pool de 5 consultas por tema. "Só lugar" tira batalha/ataque/guerra/vlog/documentário de batalha, para medir a demanda pelo **lugar hoje**, que é a do formato. Últimos 12 m = desde 12/11/2025.

| Tema | Vídeos (≥4 min, en) | **Mediana top-10 (bruta)** | Mediana top-10 (só lugar) | ≥100 mil (total) | ≥100 mil (últimos 12 m) | ≥1 mi | Títulos why-can't/still | Nº 1 | Já feito |
|---|---|---|---|---|---|---|---|---|---|
| area 51 | 63 | 6.442.989 | 5.437.592 | 41 | 20 | 19 | 3 | 205.878.859 · I Spent 24 Hours Straight At Area 51 [MrBeast] | militar secreto, não guerra |
| chernobyl | 63 | 6.192.097 | 6.043.544 | 45 | 24 | 32 | 5 | 19.967.823 · The Elephant's Foot - Corpse of Chernobyl [Kyle Hill] | não militar (ref.) |
| alcatraz | 64 | 5.639.742 | 1.349.921 | 35 | 17 | 18 | 0 | 40.223.823 · How to Escape Alcatraz With Basic Engineer [Mark Rober] | prisão (não guerra) |
| hiroshima | 64 | 5.045.534 | 5.045.534 | 35 | 9 | 17 | 1 | 132.340.839 · Hiroshima: Dropping The Bomb - Hiroshima - [BBC Studios] |  |
| midway | 55 | 2.921.535 | 95.921 | 21 | 8 | 6 | 5 | 19.712.227 · The Battle of Midway 1942: Told from the J [Montemayor] |  |
| omaha | 70 | 2.300.374 | 383.228 | 46 | 20 | 13 | 0 | 60.498.809 · June 6, 1944 – The Light of Dawn | History [Best Documentary] | WTS (341 mil + Normandy 119 mil) |
| iwo jima | 67 | 1.865.350 | 784.684 | 39 | 15 | 9 | 14 | 6.134.097 · Terrible Price of Victory -  Battle of Iwo [Real Time History] | WTS (4,5 mi) |
| falklands | 43 | 1.696.618 | 713.668 | 23 | 6 | 10 | 0 | 7.546.644 · The Falklands War: Remembered | The Untold [Timeline - World H] |  |
| okinawa | 46 | 1.652.733 | 74.567 | 25 | 7 | 8 | 0 | 7.977.846 · Rare Uncensored Footage From The Battle Of [Timeline - World H] | WTS (Hacksaw 94 mil) |
| guadalcanal | 60 | 1.389.254 | 282.732 | 29 | 6 | 6 | 0 | 3.423.898 · The Naval Battle of Guadalcanal 1942 - Ani [The Operations Roo] |  |
| pearl harbor | 64 | 1.354.191 | 414.194 | 27 | 20 | 7 | 2 | 9.457.872 · What happened to the USS Arizona? (Pearl H [Jared Owen] |  |
| lincoln | 55 | 1.320.644 | 344.910 | 32 | 7 | 7 | 1 | 16.585.957 · Last Witness to President Abraham Lincoln  [HistoryFlicks4u] |  |
| gettysburg | 70 | 949.636 | 247.338 | 36 | 10 | 3 | 0 | 5.649.761 · History Buffs: Gettysburg [History Buffs] |  |
| diego garcia | 45 | 835.749 | 835.749 | 14 | 6 | 4 | 2 | 3.241.391 · Diego Garcia: The Strategic U.S Military B [Military TV] |  |
| wake | 54 | 714.454 | 103.511 | 13 | 3 | 4 | 5 | 17.347.354 · Wake Island: The Last Stand That Stunned J [Yarnhub] |  |
| bastogne | 57 | 586.052 | 255.928 | 16 | 9 | 4 | 0 | 3.465.382 · Battle of the Bulge: Siege of Bastogne | F [hazards and catast] |  |
| peleliu | 56 | 514.259 | 44.065 | 18 | 3 | 3 | 0 | 1.716.614 · Peleliu 1944: Horror In The Pacific | Full [Kings of Docs] |  |
| cheyenne | 27 | 495.334 | 495.334 | 9 | 1 | 2 | 2 | 3.209.658 · What's really hiding under Cheyenne Mounta [9NEWS] | WTS (4,9 mil, flop) |
| antietam | 70 | 432.469 | 84.427 | 17 | 3 | 3 | 0 | 1.583.783 · Antietam: Animated Battle Map [American Battlefie] |  |
| appomattox | 52 | 389.243 | 105.936 | 12 | 3 | 2 | 0 | 2.939.330 · U.S Grant - Appomattox Lee surrender - His [Scots Grey] |  |
| bikini | 44 | 277.653 | 206.991 | 8 | 1 | 2 | 5 | 2.193.481 · 1946 Report on the Atomic Bomb Test at Bik [Vivid History] |  |
| truk | 48 | 255.128 | 164.020 | 12 | 6 | 2 | 1 | 1.137.811 · The Battle for Truk Attol (Part 1) | Battl [HISTORY] |  |
| fort sumter | 42 | 184.572 | 9.053 | 9 | 4 | 1 | 0 | 1.802.990 · The Civil War: Attack on Fort Sumter | 5-M [PragerU] |  |
| hashima | 42 | 169.770 | 63.037 | 6 | 1 | 0 | 2 | 787.564 · Battleship Island - Hardest Explore Known  [Exploring With Jos] |  |
| pointe du hoc | 28 | 169.574 | 68.004 | 9 | 3 | 0 | 1 | 379.316 · Pointe du Hoc | Liberating France [Johnny Johnson] |  |
| corregidor | 41 | 152.404 | 116.637 | 8 | 1 | 1 | 0 | 1.460.803 · Exploring Corregidor Island for 48 Hours!  [Zarckaroo Vlogs] |  |
| tinian | 49 | 127.517 | 60.246 | 5 | 0 | 1 | 0 | 1.190.612 · Tinian Reborn – Mega Airfield Awakens 80 Y [USA Military Chann] |  |
| north brother | 30 | 123.032 | 56.911 | 5 | 1 | 0 | 12 | 408.453 · Why New York's North Brother Island is Tot [IT'S HISTORY] |  |
| andersonville | 36 | 97.418 | 46.202 | 5 | 1 | 2 | 0 | 1.898.406 · Andersonville: 26 Acres of Civil War Hell  [The History Underg] |  |
| kwajalein | 38 | 55.784 | 40.593 | 2 | 0 | 0 | 0 | 495.350 · Battle of Kwajalein 1944 - Applying Lesson [From the Battlefie] |  |
| camp century | 33 | 51.562 | 51.562 | 4 | 0 | 2 | 0 | 4.514.994 · The U.S. Army's Top Secret Arctic City Und [Bright Enlightenme] |  |
| johnston | 27 | 35.561 | 30.126 | 2 | 0 | 1 | 2 | 1.037.702 · Johnston Atoll, Island of the Cold War [The History Guy: H] |  |
| fort jefferson | 46 | 27.786 | 25.013 | 4 | 1 | 0 | 0 | 237.783 · Dry Tortugas National Park Guide: Getting  [Through My Lens] |  |
| runit | 11 | 2.383 | 2.383 | 2 | 0 | 0 | 1 | 525.805 · Treasure islands in the Pacific - From the [DW Documentary] |  |

**Leituras:**
- **Bruta × "só lugar" [O]:** Midway cai de 2,92 mi para 96 mil, Wake de 714 mil para 104 mil e Guadalcanal de 1,39 mi para 283 mil: quase tudo é documentário de batalha. O formato "lugar hoje" **precisa** de pergunta (acesso/proibição), não só do tema; por isso o hit do WTS foi o único com "Can't Visit".
- **Prova do "why/still" [O]:** títulos com essa forma têm teto alto em Pearl Harbor/navios (Forgotten Fleet 1,16 mi, 777 mil, 583 mil; Ship Tales 943 mil; Insight Ship 469 mil; IT'S HISTORY 313–408 mil em Cheyenne e North Brother).
- **Vagas [O]:** temas com 0 títulos "why can't/still" no top da amostra: Corregidor, Tinian, Okinawa (fora o Hacksaw), Peleliu, Guadalcanal, Kwajalein, Gettysburg, Antietam, Appomattox, Andersonville, Camp Century.
- **Top-10 por demanda bruta (todos os temas, incluindo não-guerra):** Area 51, Chernobyl, Alcatraz, Hiroshima, Midway, Omaha, Iwo Jima, Falklands, Okinawa, Guadalcanal. **Só militares/guerra, excluindo os já feitos pelo WTS:** Hiroshima (5,05 mi bruta, mas é documentário da bomba, não "lugar hoje"; o filtro não a separa), Midway, Falklands, Guadalcanal, Pearl Harbor, Lincoln, Gettysburg, Diego Garcia, Wake, Bastogne.
- **Pesos reais [I]:** a mediana do top-10 de temas gigantes (Area 51, Alcatraz) vem de MrBeast/Mark Rober, não do formato.

## 5. Risco de hit único

| | Vídeos longos | Views totais | % do nº 1 | Mediana | Mediana sem o nº 1 | Média sem o nº 1 | ≥ 25 mil (sem o nº 1) |
|---|---|---|---|---|---|---|---|
| **WTS** (40 dias) | 11 | 5,22 mi | **86,9%** (Iwo Jima 4,54 mi) | 29,7 mil | **29,4 mil** | 68,6 mil | 7 de 10 |
| **WTS sem os 2 maiores** | 9 | 0,35 mi | – | – | 29,2 mil | 38,4 mil | 6 de 9 |
| **CWFP, longos** (5 dias) | 2 | 0,89 mi | 99,4% | 443 mil (n=2) | 5,0 mil (n=1) | – | 0 de 1 |
| **CWFP, todos** (longos + 4 Shorts) | 6 | 1,12 mi | 79,0% | 8,3 mil (Shorts) | 5,0 mil | – | – |
| Clones WTS puros (mediana de 17 canais) | – | – | 52% (mediana do share do nº 1) | 28 | – | – | – |

- **Fatos [O]:** o hit do WTS foi o **vídeo nº 2** (publicado 1 dia depois do 1º), não o nº 1; o tema (Iwo Jima) já tinha 26 vídeos "só lugar" ≥ 100 mil (demanda provada); os outros 10 vídeos do WTS somam 686 mil, e o 3º (Omaha, 341 mil) caiu 13× do hit; o 8º (Normandy, 119 mil) 38×; os 3 vídeos mais recentes (≤ 7 d) ainda estão acumulando (27 mil, 7 mil, 29,7 mil), então a mediana sem o hit é um **piso**.
- **Contra o padrão do relatório de 11/11 [O × I]:** o `entrega-youtube-2026-11/RELATORIO.md` diz "o hit é o vídeo nº 1, sobre tema já provado, e do vídeo 2 em diante as views caem 10–100×". O WTS **cumpre**: tema provado (Iwo Jima 785 mil de mediana, formula com precedente em IT'S HISTORY e Forgotten Fleet) e queda de 13–150× do hit. **Difere** em dois pontos: hit foi o nº 2, e o piso é alto (29 mil de mediana em 10 vídeos, com 3,7 mil inscritos), bem acima da mediana de 28 views dos clones. Interpretação [I]: o canal não é só um bilhete de loteria: a "fórmula geral" (pergunta + lugar dos EUA + 20 min com mapa) entrega ~30 mil por vídeo; o hit é o prêmio.
- **Como usar na decisão [I]:** projetar a nossa versão pelo **piso (~10–30 mil por vídeo)**, não pelas 4,5 mi. Na faixa 10–20% do WTS sem hit (3–6 mil por vídeo) a monetização sai do zero só depois de 1.000 inscritos e 4.000 h. O critério de §3b do playbook (3 vídeos, média ≥ 3 mil em 14 dias ou 1 vídeo ≥ 15 mil) continua adequado.
- **Atenção:** o CWFP tem 5 dias; o 882 mil pode ser o mesmo "bilhete" do WTS (vídeo nº 1/nº 2 que explode, resto cai). Reavaliar em 14 dias.

## 6. Limitações
- Busca por yt-dlp devolve ~30 resultados por consulta; contagens de clones são **pisos**.
- Views/mês de canais com 1 hit superestima (WTS 3,9 mi/mês = 87% de 1 vídeo); para canais antigos é piso (só 100 vídeos).
- Classificação por regex + curadoria minha; idiomas em `IDIOMA.md`.
- Não assisti vídeos novos nesta etapa (etapa 2, anatomia, é de outro job: `pesquisa/lugares-guerra/ANATOMIA.md`).
- RPM e receita não foram recalculados aqui (ver `IDIOMA.md` §RPM e `pesquisa/tendencias/2026-11-12-analise.md`).
