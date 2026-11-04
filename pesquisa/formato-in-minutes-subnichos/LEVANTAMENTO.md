# LEVANTAMENTO: o formato "ENTIRE History of X in N Minutes" em outros nichos

Data: 2026-11-04 · Brief: `~/workspace/referencias/BRIEF-subnichos-formato.md` · Agente: Tendências (Claude Code, Opus).
Legenda: **[O]** = observado (API do YouTube, yt-dlp, frames, transcrição) · **[I]** = inferido ou estimativa (sempre em faixa).
Artefatos nesta pasta: `dados/` (busca bruta, estatísticas, tabela), `scripts/` (como reproduzir), `thumbs/` (18 thumbs de exemplo, < 150 KB cada), `assets/<id>/` (hook.txt, info.json, frames dos 7 vídeos assistidos).

---

## Resumo executivo

**Recomendação: TESTAR em pt-BR o subnicho "Negócios": empresas, marcas, tecnologia e dinheiro.** Fórmula: "A história INTEIRA da <marca> em N minutos", com 9–20 min, quadrinho de IA, capítulos-cena e hook "origem improvável × gigante de hoje". Se o Rodrigo só quiser abrir **um** canal novo agora, eu escolheria este em vez do `dossie-ptbr`, pelos motivos da seção 5. **Guerras específicas** podem ir para o `historia-ptbr` sem canal novo. **Cidades brasileiras** ficam como 3ª opção, porque a janela em pt já está fechando.

- **O formato funciona fora da manada [O].** Achei vídeos no molde exato com tração em empresas, tecnologia, guerras específicas, cidades, religião, crime e dinheiro. Exemplos: CEOzoned (Coca-Cola 338 mil em 25 dias), Unknown Frequencies (2ª Guerra 2,12 mi), Geschichte. Lebt. (Hamburgo 493 mil, 23 vídeos de cidades) e Problema de Rico, **em pt-BR** ("A HISTÓRIA INTEIRA do DINHEIRO em 15 minutos", 524 mil).
- **Em inglês, "empresas" já virou corrida do ouro [O].** Achei 487 canais com títulos "The ENTIRE History of <empresa>". Desses, 292 foram criados a partir de 07/2026, e só **2** passaram de 100 mil views: CEOzoned e Built On You. Há pelo menos 15 canais chamados "Built On …" criados em 10/2026. É a mesma onda de clones que o job paralelo viu no Archive (14 clones em 3 semanas).
- **Em pt-BR, o template do Archive aplicado a empresas não existe [O].** Os canais pt-BR de empresas usam outros formatos, como documentário (Curioso Mercado: Odebrecht 1,0 mi, 3corações 713 mil) ou "HISTÓRIA COMPLETA DA MARCA" com fotos (Raphael H. Alves: Phebo 846 mil). O único vídeo pt no molde exato é o do dinheiro, com 524 mil views, **2,8 vezes** o 2º melhor vídeo do mesmo canal (184 mil).
- **Números de negócio [I].** O RPM de negócios e finanças é o mais alto da tabela (US$ 6–12 em inglês; em pt-BR, ×0,25–0,35, ou seja, US$ 1,5–4,2). Com 10–20% das views da CEOzoned (119–238 mil por mês), a nossa versão pt-BR renderia **US$ 180–1.000 por mês** depois do YPP. Pela mesma conta, o `dossie-ptbr` fica em US$ 280–1.560, mas tem mais risco de anúncio limitado (nazismo e violência).

**Números-chave**
| | |
|---|---|
| Buscas | **703 buscas via yt-dlp + WARP** (en/pt/es/fr/de; 0 unidade de cota), **20.123 resultados** [O] |
| Cota da API gasta | ~**1.170 unidades**, só em `videos.list`, `channels.list` e `playlistItems.list` (1 unidade cada). **Nenhuma `search.list`** [O] |
| Vídeos com título no formato | 5.051 vídeos de **3.501 canais** (regex de título, bruto) [O] |
| Canais com vídeo ≥ 100 mil no formato (últimos 18 meses) | 269, dos quais **215 fora da manada** (países, impérios, serviços secretos) [O] |
| **Canais mapeados e detalhados** (uploads completos, ritmo, % no formato) | **61** em 13 subnichos (tabela da seção 2) [O] |
| Vídeos assistidos (watch.py) | **7**: Coca-Cola, Amazon, Vietnã (en), Vietnã (es), Hamburgo, Belém e Dinheiro (pt) [O] |

**Top 3 (detalhe na seção 4)**
| # | Subnicho | Nota (máx. 30) | Prova principal [O] |
|---|---|---|---|
| 1 | **Negócios: empresas, marcas, tecnologia e dinheiro** | **27** | CEOzoned: 1,15 mi em 29 dias, 10 de 10 vídeos no formato, mediana de 81 mil. Built On You: 884 mil em 30 dias, mediana de 91 mil. Smart Code Studios (IA): 279 mil em 14 dias. pt: Dinheiro 524 mil |
| 2 | **Guerras e conflitos específicos** | **24** | Unknown Frequencies: 2ª Guerra 2,12 mi, Vietnã 955 mil, 1ª Guerra 744 mil, Guerra Fria 582 mil. Historia en Minutos (es): 930 mil em 49 dias. Chronofold: Afeganistão 536 mil (canal com 2 vídeos) |
| 3 | **Cidades e regiões (história local)** | **24** | Geschichte. Lebt. (de): 23 vídeos no formato, mediana de 141 mil, ~813 mil/mês. Majestic: Londres 3,27 mi. pt: Paraná no Tempo, ~811 mil/mês em 69 dias; Ruínas Vivas: "Toda a história de Belém em 22 minutos", 167 mil |

**Decisão sugerida (do Rodrigo):** aprovar 3 pilotos de Negócios pt-BR (Coca-Cola, NVIDIA e o dinheiro/Plano Real), com teto de ~US$ 9 por vídeo. Critério para INVESTIR, igual ao do job paralelo: média ≥ 3 mil views por vídeo ou 1 vídeo ≥ 15 mil, com % assistido ≥ 35%, em 14 dias.

---

## 1. Método

1. **Busca ampla, sem cota [O].** Fiz 399 buscas `ytsearch30:` e com o filtro "este ano, por views" (`sp=CAMSAggF`) via yt-dlp no proxy WARP (`scripts/buscar.py`). Foram 17 subnichos × 5–14 tópicos, em en, com amostras em pt/es e títulos genéricos em en/pt/es/fr/de. Depois vieram **230 buscas dirigidas** a vídeos recentes, deste ano e deste mês (`scripts/buscar2.py`), e **74 buscas de concorrência em pt/es** (`scripts/buscar_ptes.py`).
2. **Filtro de formato [O].** O regex de título está em `scripts/agregar.py` e `scripts/classificar.py`. Ele classifica a força do título assim:
   - **alto** = "ENTIRE/COMPLETA/TODA la historia/ganze Geschichte de X" **+** "em N minutos";
   - **médio** = só a primeira parte, ou "rise and fall" + N minutos;
   - **baixo** = só "em N minutos" ou só "rise and fall".
   Os países, impérios, serviços secretos e regimes ficam marcados como **manada** (`MANADA` em `classificar.py`).
3. **Estatísticas em lote [O].** `videos.list` e `channels.list` cobriram os 5.051 vídeos e os 3.501 canais (`scripts/enriquecer.py`). Para 61 canais escolhidos à mão (`dados/curadoria.tsv`), baixei até 300 uploads com `playlistItems` + `videos.list` e calculei idade real, ritmo, % no formato e mediana (`scripts/canais_detalhe.py`).
4. **Assistir [O].** Chamei o `tools/watch.py` por `scripts/assistir.py`, com os assets nesta pasta. Os frames e as thumbs foram analisados com visão.
5. **Concorrência [O/I].** `scripts/concorrencia.py` conta, por subnicho, os canais com título "alto" fora da manada e quantos deles passaram de 50 mil. Além da busca dirigida em pt/es, foram contados os canais criados a partir de 07/2026.

**Definições [I].**
- **Views/mês (vida)** = views do canal ÷ idade × 30.
- **Views/mês recente** = views dos vídeos publicados nos últimos 90 dias ÷ (min(90, idade) / 30). Subestima a cauda dos vídeos antigos.
- **Monetização:** "provável" = elegível (≥ 1.000 inscritos e ≥ 4.000 h estimadas em 12 meses, com 40% de retenção) **e** anúncios na página ou canal grande. "Elegível, não confirmado" = só elegível. Os anúncios na página são indício, não prova.

---

## 2. Tabela de canais por subnicho

Gerada por `scripts/tabela.py` (também em `dados/canais_tabela.md` e `dados/canais_detalhe.csv`). "Idade" é a do 1º vídeo; quando aparece "(criação)", o canal tem mais de 300 uploads e a idade é a da criação do canal. "Vídeos (longos/formato)" = total (vídeos > 3 min / vídeos com título "alto" ou "médio" no formato). A **semelhança** foi avaliada à mão (título + visual + duração).

#### Negócios: empresas e marcas
| Canal | Idioma | Idade | Vídeos (longos/formato) | Views | Inscritos | Views/mês vida [I] | Views/mês recente [I] | Últimos 30 d (vídeos · views) | Mediana no formato | Monetização [I] | Semelhança | Melhor vídeo [O] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [CEOzoned](https://www.youtube.com/channel/UCxDgDZTADoIDno8KD8kiGgQ) | en | 29 d | 10 (10/10) | 1,15 mi | 12 mil | 1,19 mi | 1,22 mi | 10 · 1,18 mi | 81 mil | provável | **alto** | The ENTIRE History of Coca-Cola in 11 Minutes: 338 mil (25 d, 11 min) |
| [Built On You](https://www.youtube.com/channel/UC8p5EKG8jlsL2R2bvr2fZ3g) | en (IN) | 30 d | 8 (8/8) | 884 mil | 14 mil | 884 mil | 928 mil | 8 · 928 mil | 91 mil | elegível, não confirmado (sem anúncio na página) | **alto** | The ENTIRE History of Amazon in 20 Minutes: 371 mil (30 d, 20 min) |
| [Michael Girdley](https://www.youtube.com/channel/UC-mfn4ibOC5ewLcpmgl0C4g) | en/de | > 4 anos | 604 (198/0) | 81,5 mi | 388 mil | 1,70 mi | 4,86 mi | 27 · 3,53 mi | — | provável | baixo ("rise and fall", rosto) | Rise & fall of Topgolf: 1,65 mi. Em alemão: "Aufstieg und Fall von KFC", 638 mil |
| [FINAiUS](https://www.youtube.com/channel/UCGBoWe1mzCvbbqDNncmxm8A) | en | 6 anos | 88 (67/3) | 72,0 mi | 803 mil | 943 mil | 946 mil | 3 · 1,02 mi | 553 mil | provável | médio (40–70 min) | Rockefeller 799 mil; Warren Buffett 553 mil; House of Morgan 438 mil |
| [Crayon Capital](https://www.youtube.com/channel/UCP9RPj_BG0vit2TNM7LuRxA) | en | 560 d | 33 (33/1) | 24,7 mi | 297 mil | 1,32 mi | 865 mil | 3 · 1,48 mi | 545 mil | provável | médio ("Explained Like You're 5") | The ENTIRE History of Elon Musk ELI5: 544 mil |
| [Curioso Mercado](https://www.youtube.com/channel/UCoSeSFNhnG5D7fxqSa6kl9w) | **pt** | > 6 anos | 747 (121/1) | 63,2 mi | 468 mil | 786 mil | 865 mil | 27 · 531 mil | — | provável | baixo (documentário) | 3corações 713 mil; Ascensão e Queda da Odebrecht 1,0 mi |
| [Raphael H. Alves](https://www.youtube.com/channel/UCxN_ktrbqsHHddgKIr5EawQ) | **pt**/en | 5,5 anos | 191 (187/139) | 12,4 mi | 107 mil | 185 mil | 68 mil | 0 · 0 | 31 mil | provável | médio (fotos, sem N min) | A HISTÓRIA COMPLETA DA MARCA PHEBO: 846 mil |

#### Negócios: tecnologia e dinheiro
| Canal | Idioma | Idade | Vídeos (longos/formato) | Views | Inscritos | Views/mês vida [I] | Views/mês recente [I] | Últimos 30 d | Mediana no formato | Monetização [I] | Semelhança | Melhor vídeo [O] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Smart Code Studios](https://www.youtube.com/channel/UC6bTDmQmnGLm1oyM9tuNj5Q) | en (TR) | 21 d | 15 (5/3) | 394 mil | 3 mil | 564 mil | 567 mil | 15 · 397 mil | 110 mil | elegível, não confirmado | **alto** | The ENTIRE History of AI in 16 Minutes: 279 mil (14 d); Internet 110 mil |
| [Problema de Rico](https://www.youtube.com/channel/UCl593fFEYTFbF_tW-3DQtOg) | **pt** (BR) | 158 d | 24 (24/1) | 1,30 mi | 11 mil | 247 mil | 190 mil | 4 · 36 mil | 524 mil (1 vídeo) | provável (anúncio na página) | médio (título alto; apresentador) | **A HISTÓRIA INTEIRA do DINHEIRO em 15 minutos: 524 mil** (137 d) |
| [Casual Economics](https://www.youtube.com/channel/UCo7FvfMJeTRhO-d7xT8IZlg) | en | 2,6 anos | 11 | 5,77 mi | 94 mil | 182 mil | 19 mil | 0 | — | elegível, não confirmado | médio | The Great Depression in 12 Minutes: 3,15 mi |
| [Your T V](https://www.youtube.com/channel/UClr9YyTruhUbMIX4IV6q9LA) | en | 560 d | 46 (40/1) | 363 mil | 2 mil | 19 mil | 112 mil | 7 · 3 mil | 326 mil | elegível, não confirmado | baixo | The Complete History of Electricity: 326 mil |
| [Unsolved Concept](https://www.youtube.com/channel/UCKT5s-RcwDchlvWDJZlbsfg) | en | 110 d | 39 (39/3) | 343 mil | 2 mil | 93 mil | 110 mil | 5 · 930 | 701 | elegível, não confirmado | baixo | The Complete History of Photography: 275 mil |
| [SciMath](https://www.youtube.com/channel/UCE9VetCQNNKvSQZJ73J1fEA) | en | 305 d | 61 (49/1) | 140 mil | 2 mil | 14 mil | 9 mil | 22 · 11 mil | 82 mil | elegível, não confirmado | médio | The Entire History of Mathematics in 10 Minutes: 82 mil |
| [Bub Explains](https://www.youtube.com/channel/UCuDUP15RMVaHsZ-ln9SyYqg) | en | 318 d | 71 (71/9) | 6,99 mi | 104 mil | 659 mil | 205 mil | 10 · 156 mil | 21 mil | provável | baixo ("for sleep", 2–5 h) | Computer Science (For Sleep) 182 mil |

#### Guerras e conflitos específicos
| Canal | Idioma | Idade | Vídeos (longos/formato) | Views | Inscritos | Views/mês vida [I] | Views/mês recente [I] | Últimos 30 d | Mediana no formato | Monetização [I] | Semelhança | Melhor vídeo [O] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Unknown Frequencies](https://www.youtube.com/channel/UCm1yxl_4qMbStLHpHQu6xWg) | en | 259 d | 23 (23/6) | 12,4 mi | 90 mil | 1,43 mi | 1,20 mi | 2 · 144 mil | **663 mil** | provável (anúncios + patrocínio Freecash) | **alto** | The ENTIRE History of WW2 Explained: 2,12 mi; Vietnam 955 mil; WW1 744 mil; Cold War 582 mil |
| [Historia en Minutos](https://www.youtube.com/channel/UC9-Evc7Dd9vENeN9zYiOe0g) | **es** (VN) | 49 d | 19 (19/19) | 930 mil | 2 mil | 570 mil | 572 mil | 10 · 31 mil | 3 mil | provável (anúncio na página; elegível pelas horas) | **alto** | Stalingrado ("batalla más mortífera") 273 mil; Vietnã 211 mil; 2ª Guerra 175 mil; 1ª Guerra 108 mil; Guerra Fria 101 mil |
| [Chronofold](https://www.youtube.com/channel/UCN87LLx0N_ZZ9BZBegN1WXA) | en | 59 d | 2 (2/2) | 536 mil | 2 mil | 273 mil | 274 mil | 1 · 4 mil | 270 mil | elegível, não confirmado | **alto** (template Archive) | The ENTIRE History of Afghanistan in 15 Minutes: 536 mil |
| [Agent Flappy](https://www.youtube.com/channel/UCRi2h75k0cAsMin5TYxZJgw) | en | 508 d | 59 (53/2) | 27,9 mi | 151 mil | 1,65 mi | 673 mil | 7 · 531 mil | 125 mil | provável | médio ("X Explained in N Minutes") | American Civil War in 24 Minutes 1,30 mi; WW2 in 31 Minutes 979 mil |

#### Cidades e regiões
| Canal | Idioma | Idade | Vídeos (longos/formato) | Views | Inscritos | Views/mês vida [I] | Views/mês recente [I] | Últimos 30 d | Mediana no formato | Monetização [I] | Semelhança | Melhor vídeo [O] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Geschichte. Lebt.](https://www.youtube.com/channel/UCAfTvAbVljmMPdiTezwLsBA) | **de** | 252 d | 53 (53/23) | 5,15 mi | 19 mil | 613 mil | 813 mil | 5 · 436 mil | **141 mil** | provável | **alto** | Hamburgo 493 mil; Stuttgart 322 mil; Suíça 301 mil; Hannover 295 mil; Frankfurt e Colônia 271 mil |
| [Paraná no Tempo](https://www.youtube.com/channel/UCma5HC_QRIlAtW68ojuLhiQ) | **pt** | 69 d | 65 (65/0) | 1,86 mi | 4 mil | 808 mil | 811 mil | 33 · 356 mil | — | elegível, não confirmado | médio ("A História de Curitiba (1693–2026)") | Assim Era Viver em Cascavel em 1950: 511 mil; Curitiba 314 mil |
| [Thomas Relives History](https://www.youtube.com/channel/UCeaJ37P2B1QUGgsI0RyFugw) | en | 268 d | 119 (119/11) | 7,37 mi | 34 mil | 825 mil | 680 mil | 18 · 137 mil | 19 mil | elegível, não confirmado | médio | The Entire History of the Las Vegas Strip in 20 Minutes: 681 mil |
| [América Restaurada](https://www.youtube.com/channel/UCKMwzlUw9EPTKzdLNNnvmLA) | es | 299 d | 61 (61/8) | 5,50 mi | 30 mil | 551 mil | 501 mil | 9 · 431 mil | 84 mil | elegível, não confirmado | médio | Lima en 28 minutos 299 mil; Bogotá 218 mil; Medellín 187 mil |
| [Chronopolis](https://www.youtube.com/channel/UCMb5_vNt4-b0z8a0IoPZgwg) | es | 18 d | 16 (3/3) | 183 mil | 458 | 304 mil | 315 mil | 16 · 189 mil | 65 mil | não elegível | **alto** | Toda la historia de Bilbao en 34 minutos: 71 mil (11 d) |
| [Geschichte Ewig](https://www.youtube.com/channel/UChOdVN_mX2tuXKkJkmy6Qng) | de | 56 d | 24 (24/22) | 424 mil | 1 mil | 227 mil | 230 mil | 7 · 69 mil | 5 mil | elegível, não confirmado | **alto** | Bremen 116 mil (clone do Geschichte. Lebt.) |
| [Zeitspiegel](https://www.youtube.com/channel/UCCKSBXioxWS_qpg7HBnZSLA) | de | 25 d | 17 (17/13) | 165 mil | 1 mil | 198 mil | 215 mil | 18 · 179 mil | 2 mil | elegível, não confirmado | **alto** | Silésia 68 mil (8 d) |
| [Ruínas Vivas](https://www.youtube.com/channel/UC3nu9mDjXt7aN3pq4OPm_gA) | **pt** | 67 d | 10 (10/0*) | 300 mil | 2 mil | 134 mil | 134 mil | 5 · 45 mil | — | provável (anúncio na página) | **alto** | **Toda a história de Belém em 22 minutos: 167 mil**; Rio 87 mil; Manaus 40 mil; São Paulo 2 mil |
| [O Reconstrutor](https://www.youtube.com/channel/UCB7rlyp-wetVadf3JvDzOeg) | **pt** | 183 d | 12 (12/2) | 1,54 mi | 12 mil | 252 mil | 78 mil | 2 · 3 mil | 68 mil | elegível, não confirmado | médio (reconstrução IA) | Primeira favela do Brasil 406 mil; A História Completa da Rocinha em 23 minutos 135 mil |
| [Vozes do Brasil Antigo](https://www.youtube.com/channel/UCbFSC7U8N9Mji2X-yQWhsCg) | **pt** | 106 d | 73 (71/2) | 253 mil | 948 | 72 mil | 82 mil | 25 · 21 mil | 695 | não elegível | médio | Rondonópolis 77 mil; Londrina 74 mil |
| [Majestic Studios](https://www.youtube.com/channel/UC0ra0vN_iF5AwwU7G8q79rw) | en/fr | 593 d | 93 (20/11) | 85,9 mi | 239 mil | 4,34 mi (maior parte em Shorts) | 98 mil | 1 · 9 mil | 537 mil | provável | **alto** | London in 24 Minutes 3,27 mi; Paris 1,61 mi; York 1,08 mi; desacelerou (1 vídeo em 30 d) |
| [Живые Руины](https://www.youtube.com/channel/UCNG3zXlo1UU0CLWMjfWyAfw) | ru | 158 d | 28 | 1,91 mi | 9 mil | 362 mil | 211 mil | 7 · 286 mil | — | elegível, não confirmado | médio | Toda a história de Roma em 34 minutos: 469 mil |
| [timewarp cities](https://www.youtube.com/channel/UCpr1JAIc49gu9-FAlO4uAKw) | en | 320 d | 130 | 6,71 mi | 61 mil | 629 mil | 448 mil | 29 · 534 mil | 3 mil | elegível, não confirmado | médio (timelapse) | New York 0 to 2026: 1,26 mi |
| [Ancient Human Explains](https://www.youtube.com/channel/UCylm2WD1qMqRWSprZO86TqQ) | en/es | 117 d | 44 (44/17) | 670 mil | 4 mil | 172 mil | 13 mil | 17 · 31 mil | 781 | elegível, não confirmado | **alto** | Babilônia 519 mil (1 hit) |
| [ZeitreiseGeschichte](https://www.youtube.com/channel/UCbVkWWc_TvsjghxeSRfM4GQ) | de | 104 d | 36 (36/19) | 148 mil | 281 | 43 mil | 49 mil | 12 · 4 mil | 552 | não elegível | **alto** | Mainz in 11 Minuten 115 mil (1 hit) |
| [Reconstruindo Histórias](https://www.youtube.com/channel/UCzRmKxy0TUeGOyRRJa6tOQA) | **pt** | 280 d | 29 (27/9) | 251 mil | 3 mil | 27 mil | 621 | 0 | 3 mil | elegível, não confirmado | médio | A História Completa de Londres em 10 minutos: 91 mil; parado |

\* "Toda a história de" não estava no regex da classificação; os títulos do Ruínas Vivas estão no molde exato [O].

#### Religiões e Bíblia
| Canal | Idioma | Idade | Vídeos (longos/formato) | Views | Inscritos | Views/mês vida [I] | Views/mês recente [I] | Mediana no formato | Monetização [I] | Semelhança | Melhor vídeo [O] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [Más Allá De Los Versos](https://www.youtube.com/channel/UCTh7iuVVHEDnPHxBkaOGHtA) | es | ~3 anos | 302 (300/14) | 142 mi | 1,32 mi | 4,03 mi | 4,19 mi | 301 mil | provável | médio (30–130 min) | Antigo Testamento em 37 Minutos 804 mil; Profetas 1,01 mi |
| [Bible Origins](https://www.youtube.com/channel/UCT0LgtVR1_IpR4joNHz7A7w) | en (NG) | 393 d | 196 | 26,3 mi | 260 mil | 2,01 mi | 1,58 mi | 29 mil | provável | baixo | Old Testament in 35 Minutes 552 mil |
| [Historias de Tiempos Bíblicos](https://www.youtube.com/channel/UCkhrGrkOI67PL8RR5L3nbtQ) | es (MX) | 102 d | 70 (70/13) | 2,08 mi | 10 mil | 611 mil | 476 mil | 4 mil | elegível, não confirmado | médio | La Historia Completa de Nínive en 30 Minutos: 326 mil |
| [Historia Explicada](https://www.youtube.com/channel/UCQ7rpXb-OypGlZQ3zEkMaHQ) | es | 200 d | 66 (54/5) | 2,15 mi | 34 mil | 323 mil | 499 mil | 18 mil | elegível, não confirmado | **alto** | Christianity in 20 Minutes 48 mil (o canal mistura temas) |
| [A História do Cristianismo](https://www.youtube.com/channel/UCQCWo5JanDIuwkkt3K5K_ug) | **pt** | 6 d | 5 (5/3) | 89 mil | 774 | — | 469 mil (6 d, não confiável) | 7 mil | não elegível | **alto** | A História Completa da Reforma Protestante em 28 Minutos: 80 mil (6 d) |
| [Crayon History](https://www.youtube.com/channel/UClh_pKGDqGOVg1QgSC7MRZQ) | en | 45 d | 9 (9/9) | 109 mil | 695 | 72 mil | 73 mil | 4 mil | não elegível | **alto** | The ENTIRE History of Vatican in 14 Minutes: 67 mil |
| [Mystères du Coran](https://www.youtube.com/channel/UCfgFTfPi0rPXhbc0tvk4Seg) | fr | 338 d | 31 (28/7) | 2,17 mi | 51 mil | 193 mil | 0 (parado) | 92 mil | elegível, não confirmado | médio | L'Histoire Complète de l'Islam en 60 Minutes: 338 mil |

#### Commodities, comida e produtos
| Canal | Idioma | Idade | Vídeos | Views | Inscritos | Views/mês vida [I] | Views/mês recente [I] | Mediana no formato | Monetização [I] | Semelhança | Melhor vídeo [O] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [Historia Del Comercio](https://www.youtube.com/channel/UC6_DCl4fmfIArOb8eHelhjw) | es (ES) | 124 d | 33 | 8,18 mi | 37 mil | **1,98 mi** | 1,38 mi | 84 mil | elegível, não confirmado | médio (45–58 min) | Comércio de escravos 1,59 mi; Milho 1,13 mi; Café 816 mil; Azeite 744 mil; Ouro 374 mil |
| [FooDiscover](https://www.youtube.com/channel/UCddXepURe7TTkRWrQXwwrgw) | en | 468 d | 89 | 13,7 mi | 75 mil | 880 mil | 0 (parado) | 64 mil | elegível, não confirmado | médio ("Every X Explained") | Entire History of Pizza in 7 Minutes 64 mil |
| [Origem Do Sabor](https://www.youtube.com/channel/UCNM_sc4hujnOLcdKqtGrNKQ) | **pt** | 91 d | 14 (14/14) | 7 mil | 93 | 2 mil | 2 mil | 247 | não elegível | médio (33 min) | **Tentativa pt que não pegou:** A História Completa Do Whisky 1,9 mil |

#### Crime, drogas e cartéis
| Canal | Idioma | Idade | Vídeos | Views | Inscritos | Views/mês vida [I] | Views/mês recente [I] | Mediana no formato | Monetização [I] | Semelhança | Melhor vídeo [O] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [20 Minute Professor](https://www.youtube.com/channel/UCFJep9lyCuYox50lqZVZxGg) | en | 217 d | 16 (16/5) | 2,07 mi | 22 mil | 286 mil | 74 mil | 7 mil | elegível, não confirmado | **alto** | The Entire History of Drugs in 23 Minutes: 736 mil |
| [Señor Mafia](https://www.youtube.com/channel/UClNOxngKfUDBKoZcSJwu2cA) | es (dono BR) | 102 d | 45 (42/40) | 498 mil | 1 mil | 147 mil | 58 mil | 1 mil | elegível, não confirmado | **alto** | La Historia Completa del Cártel de Sinaloa en 26 Minutos: 316 mil; El Chapo 112 mil; o resto < 8 mil |
| [Historiador de Medianoche](https://www.youtube.com/channel/UCzyOwVV52TTEK36v3aSfvtg) | es | 350 d | 10 | 2,17 mi | 31 mil | 186 mil | 0 (parado) | 982 mil | elegível, não confirmado | baixo ("para dormir", 85–116 min) | Historia Completa de la COCAÍNA: 1,05 mi |

#### Esportes, games, dinastias, cultura pop, música (formato parecido, menos prioritários)
| Canal | Subnicho | Idioma | Idade | Views | Inscritos | Views/mês recente [I] | Semelhança | Melhor vídeo [O] |
|---|---|---|---|---|---|---|---|---|
| [SoccerJM](https://www.youtube.com/channel/UCxoMacohzH2P3rmISlhnuDQ) | esportes | **pt** | > 10 anos | 347 mi | 1,13 mi | 2,11 mi | médio | A História COMPLETA da Copa do Mundo de 2010/2018/2014: 5,0/4,9/4,0 mi (usa imagens de jogo) |
| [Iso Jack](https://www.youtube.com/channel/UCuytlKDYS0Yn9cbaRrTvtMQ) | esportes | en | 641 d | 6,14 mi | 20 mil | 45 mil | médio | The ENTIRE History of Basketball: 210 mil |
| [Football ALL STARS](https://www.youtube.com/channel/UCWWJOnuHC7csfhYfTSqCJRQ) | esportes | en | ~3 anos | 29,2 mi | 48 mil | 316 mil | baixo | The Complete History of the World Cup: 139 mil |
| [Porão do OrdJogos](https://www.youtube.com/channel/UCchiGNf6U_TZPE15Lq3nSag) | games | **pt** | 724 d | 19,2 mi | 196 mil | 791 mil | médio | A lore completa de RESIDENT EVIL: 701 mil; The complete history of Valve in 50 minutes: 186 mil |
| [CRG Explains](https://www.youtube.com/channel/UCEy85baRPPw7Ls5HkMv8uRA) | games | en | 361 d | 13,8 mi | 30 mil | 91 mil | médio | The Entire History Of Browser Games: 963 mil |
| [NeverKnowsBest](https://www.youtube.com/channel/UC1fKT0wuhchtclPqpdWEnHw) | games | en | > 8 anos | 52,0 mi | 376 mil | 236 mil | baixo (2–3 h) | The Entire History of RPGs: 4,63 mi |
| [Old Money Dynasty](https://www.youtube.com/channel/UCufvVan2COV7M3FX5dPdlHA) | dinastias | en | 420 d | 13,3 mi | 99 mil | 143 mil | baixo | The Entire History of The Ringling Bros Circus In 38 Minutes: 38 mil |
| [TragicRoyals](https://www.youtube.com/channel/UC3xUMk_zFjfvGhxiPVwwnoQ) | dinastias | en | — | 1,38 mi | 9 mil | 0 | médio | The Entire History of the House of Rothschild: 1,16 mi |
| [Wallace](https://www.youtube.com/channel/UCWMmoNQsNKlXC5KofNO2w_g) | cultura pop | en | 669 d | 41,1 mi | 226 mil | 1,32 mi | médio | The ENTIRE History of the Green Lanterns: 1,80 mi; Sith 532 mil |
| [Turtoon](https://www.youtube.com/channel/UCRlhdrMmdBFxriEV3gEfa_g) | cultura pop | fr/en | ~3 anos | 39,8 mi | 270 mil | 586 mil | baixo (usa trechos dos desenhos) | L'histoire COMPLETE de Ninjago en 30 minutes: 2,09 mi |
| [Alexcalibur01](https://www.youtube.com/channel/UCW3e0xAI87-fWytVGlij64Q) | cultura pop | en/fr | > 10 anos | 45,6 mi | 69 mil | 2,57 mi | baixo | The COMPLETE History of WOLVERINE in 47 minutes: 137 mil |
| [Mark The Hammer](https://www.youtube.com/channel/UCYcXk-yEg9LgyAPm7mpIs-g) | música | en | > 20 anos | 196 mi | 670 mil | 670 mil | baixo (humor) | The whole history of PUNK… told TERRIBLY |

Referência da manada: [Archive in Minutes](https://www.youtube.com/channel/UCFp0Rk-ad8JD78Qw9nEJ29w): 20 dias, 19 vídeos no formato, 1,95 mi de views, ~2,9 mi/mês [O/I]. O detalhe está no levantamento paralelo.

---

## 3. Subnichos com tração e concorrência

### 3a. Tração × concorrência (fora da manada, títulos "alto", publicados nos últimos 365 dias) [O]
| Subnicho | Vídeos no molde | Canais | Canais com algum vídeo ≥ 50 mil | Vídeos ≥ 100 mil | Mediana de views | Canais criados desde 07/2026 (≥ 100 mil) |
|---|---|---|---|---|---|---|
| Empresas e marcas | 643 | 431 | 3 | 9 | **47** | 292 (2) |
| Tecnologia | 303 | 234 | 9 | 10 | 65 | 145 (3) |
| Cidades | 279 | 222 | 9 | 8 | 149 | 74 (0*) |
| Guerras específicas | 58 | 54 | 3 | 3 | 44 | 33 (1) |
| Religiões | 50 | 40 | 4 | 2 | 279 | 21 (0) |
| Finanças e dinheiro | 62 | 54 | 1 | 1 | 91 | 33 (0) |
| Crime e máfia | 56 | 50 | 1 | 1 | 63 | 30 (1) |
| Comida e bebida | 46 | 36 | 2 | 1 | 21 | 19 (0) |
| Esportes | 27 | 22 | 0 | 0 | 146 | 10 (0) |

\* A classificação por palavra-chave não pega nomes de cidades alemãs no genitivo (Hamburgs, Bremens), então os de cidades estão subcontados. Fonte: `dados/concorrencia.json`. A amostra depende das buscas: empresas teve mais tópicos buscados, mas a proporção de acerto, e não o total, é o que importa aqui.

**Leitura [I].**
- O formato **já foi "descoberto" pela indústria de canais faceless em empresas e tecnologia**. A taxa de acerto é de ~1% (2 em 292 canais novos). Em inglês, entrar nesses subnichos agora é ser o 293º.
- Guerras, religiões e cidades têm **menos tentativas** e acerto relativo maior (5–10% dos canais com algum vídeo ≥ 50 mil).
- Em **pt-BR**, a concorrência no molde exato é de 0–4 canais por subnicho (ver 3b).

### 3b. Concorrência em pt-BR (buscas `buscar_ptes.py`, 74 consultas) [O]
| Subnicho | Canais pt no molde exato (cartoon/IA + "INTEIRA/COMPLETA em N min") | Quem domina a busca em pt | Leitura [I] |
|---|---|---|---|
| Empresas/marcas | **0**. Problema de Rico fez o dinheiro com apresentador | Curioso Mercado (documentário), Raphael H. Alves (fotos), O Primo Rico | **Janela aberta**; demanda provada em pt (dinheiro 524 mil, Odebrecht 1,0 mi, 3corações 713 mil, Phebo 846 mil) |
| Tecnologia | 0 | Ciência Todo Dia, Universo Curioso (universo/Terra em N min, 450–730 mil) | Aberta; demanda pt de ciência existe |
| Guerras | 0 em narrativa cartoon. Em es: Historia en Minutos (49 d), Memorias de Pez, Infonimados | Débora Aladim (resumos escolares, 3–5 mi), Descomplica | Aberta no formato; o público pt busca guerra como **resumo escolar** |
| Cidades | **4 canais novos em 3 meses**: Paraná no Tempo, Ruínas Vivas, Vozes do Brasil Antigo, O Reconstrutor | os mesmos | **Fechando**; cidades médias do Sul e do Centro-Oeste rendem (Cascavel 511 mil, Curitiba 314 mil) |
| Religiões | A História do Cristianismo (6 d, 80 mil) | Escola do Discípulo (5,7 mi), Caminhos da Bíblia, Desmistificando as Escrituras | Concorrida |
| Crime | Dossiê Criminal (PCC 275 mil) | Jovem Pan (PCC 3,2 mi), Fatos Desconhecidos | Demanda enorme, risco de política alto |
| Commodities | Origem Do Sabor (**fracassou**: 14 vídeos, mediana de 247) | — | Sem prova em pt |
| Esportes | SoccerJM (Copas 4–5 mi, com imagens de jogo) | SoccerJM | Dominado; depende de imagens de jogo (Content ID) |

### 3c. Vídeos assistidos: o que muda no hook, no título e na thumb

| ID | Canal (subnicho) | Título | Duração | Views | Cortes/min no início | Anúncios na página |
|---|---|---|---|---|---|---|
| _OuJBX6Q4Cc | CEOzoned (empresas) | The ENTIRE History of Coca-Cola in 11 Minutes | 11:01 | 338 mil | 12 | sim |
| jOo8wSIeGus | Built On You (empresas) | The ENTIRE History of Amazon in 20 Minutes | 20:00 | 371 mil | **30** | não |
| 5n_KfzZcN3s | Problema de Rico (dinheiro, **pt**) | A HISTÓRIA INTEIRA do DINHEIRO em 15 minutos | 15 min | 524 mil | 9 | sim |
| 79PHRzE9pDU | Unknown Frequencies (guerras) | The ENTIRE History of The Vietnam War Explained | 18:06 | 955 mil | 11 | sim |
| ZUhaoT8mj7I | Historia en Minutos (guerras, es) | Toda la Historia de la Guerra de Vietnam Explicada | 23:33 | 211 mil | 6 | sim |
| Bdaenq7PCGg | Geschichte. Lebt. (cidades, de) | Die ganze Geschichte Hamburgs in 19 Minuten (K.I. Rekonstruktion) | 19:06 | 493 mil | 13 | sim |
| m4Pd0TuDKWo | Ruínas Vivas (cidades, **pt**) | Toda a história de Belém em 22 minutos — a única porta da Amazônia | 22 min | 167 mil | 7 | sim |

#### Negócios (empresas, tecnologia e dinheiro)
- **Hook (transcrição real, Coca-Cola) [O]:** "Every day, around 2 billion servings of one drink are poured somewhere on Earth. It started as a failed medicine, invented by a wounded soldier who was addicted to morphine. In its first year, it lost money. Today, it is one of the most recognized brands on the planet. This is the entire history of Coca-Cola."
  - Técnica [I]: **escala de hoje → origem improvável e humana → fracasso inicial → "isto é a história inteira"**, em 16 s. A anedota é o **fundador**, não uma vítima.
- **Hook (Amazon) [O]:** "Open the tracking page on an Amazon order tonight, and you won't see a store. You'll see a dot… Amazon is not a store that has warehouses. Amazon is a warehouse that grew a store." Em seguida vêm a escala ("valued at about $438 million… Today, it takes in that much money in less than five hours") e a lista de quem morreu ("Borders is gone. Circuit City is gone. Sears… Amazon is still here").
  - É **a mesma reformulação-paradoxo do nosso Egito** ("não é um país que tem um rio; é um rio com um país em volta") e o mesmo "todos sumiram; ele continua aqui" [O, comparando com `conhecimento/hooks.md`].
- **Hook (Dinheiro, pt) [O]:** "Se você ainda tem dinheiro físico com você, pega uma nota aí e olha bem para ela… E você já se perguntou por quê? … A resposta é uma palavra só, confiança." Depois vêm a promessa de duração ("em 15 minutos") e o loop para o final ("vou te mostrar o capítulo mais doido de todos: o Brasil teve 8 moedas diferentes").
  - Técnica: **objeto na mão do espectador + pergunta + ângulo Brasil guardado para o fim**.
- **Título [O]:** idêntico ao do Archive: "The ENTIRE History of <Marca> in N Minutes", com ENTIRE em caixa alta e N = duração. A marca tem 1–2 palavras. As durações são 9–14 min (CEOzoned) e ~20 min (Built On You). Os hits têm uma **marca de consumo ou um bilionário famoso** (Coca-Cola, Amazon, SpaceX, Elon Musk, Toyota). Marcas que o público usa mas que não têm uma "história de origem" conhecida ficam mais fracas (Instagram 4 mil, Facebook 28 mil, Apple 22 mil na CEOzoned).
- **Thumb [O]:** **cópia exata do template do Archive** (`thumbs/empresas-*.jpg`): fundador ou CEO em meio corpo à esquerda, de braços cruzados e com contorno laranja; cenário de fábrica, armazém ou HQ ao fundo; **MARCA gigante preta serifada + selo do logo + "AAAA – AAAA"** no canto superior direito; ícones do produto na lateral. A Built On You é igual (Bezos + armazém + "AMAZON 1994 – 2026").
- **Edição [O]:**
  - **CEOzoned:** cartoon de IA com bonecos de **cabeça redonda e branca** (estilo stickman/Oversimplified), cenários pintados e tela dividida. É o nosso estilo do `historia-ptbr`, não o graphic novel do Archive.
  - **Built On You:** o mesmo boneco, com paleta sépia e pastel, rótulos entre aspas na tela ("SECURED & CLOSED", "$438 MILLION") e 30 cortes/min.
  - **Capítulos-fase** ("The origin of Coca-Cola", "Asa Candler builds the brand", "Marketing wars and the New Coke"), mais convencionais que os capítulos-objeto do Archive.

#### Guerras específicas
- **Hook (Unknown Frequencies, Vietnã) [O]:** "The Vietnam War killed an estimated 3 million Vietnamese people and 58,220 Americans. The United States dropped more bombs… than every country dropped in all of World War II combined. America won virtually every major battle and still lost… So how did America get pulled into its longest war, win almost every battle, and still lose everything?" Depois entra um patrocínio (Freecash) aos 55 s.
  - Técnica: **rajada de números + paradoxo + pergunta central**, em ~50 s. Sem anedota pessoal.
- **Hook (Historia en Minutos, es) [O]:** "30 de abril de 1975, Saigón. El ruido de los helicópteros atraviesa el cielo… Pero hay algo profundamente desconcertante en esta escena… ¿Cómo había sido posible?"
  - Técnica: **cena datada de lugar (o fim da guerra) → paradoxo → pergunta → volta 30 anos**. É uma versão "lugar" do hook por anedota.
- **Título [O]:** em inglês, "The ENTIRE History of <guerra> **Explained**", **sem N** no título; o N vai para a thumb ("IN 18 MINUTES"). Em espanhol, "Toda la Historia de la Guerra de X Explicada". As guerras mais famosas rendem 5–20 vezes mais que as de nicho (Vietnã 211 mil × Malvinas 16 mil no mesmo canal).
- **Thumb [O]:** **dois líderes ou soldados frente a frente**, com cara de bravo, sobre **mapa colorido** do conflito, mais "GUERRA X / EM N MINUTOS" em branco com contorno. A Historia en Minutos copia o layout da Unknown Frequencies. Já o Chronofold (Afeganistão) usa o template do Archive (cidade em sépia + "AFGHANISTAN 4000 BC – 2026").
- **Edição [O]:**
  - **Unknown Frequencies:** cartoon desenhado com **mascote fixo** (um soldado-esqueleto), countryballs, números gigantes amarelos na tela ("58,220 AMERICANS", "416 TO 0") e 11 cortes/min.
  - **Historia en Minutos:** cartoon de IA com bonecos de rosto branco, **calendário com a data na tela** ("1963", "LATE 1967", "APR 30, 1975"), mapas com setas e 6 cortes/min.

#### Cidades e regiões
- **Hook (Hamburgo, de) [O]:** "Ihr Name bedeutet Sumpfburg. Sie wurde mehrfach niedergebrannt, von Wikingern geplündert, von Napoleon besetzt und in einer einzigen Sommernacht 1943 zur Hälfte dem Erdboden gleichgemacht. Und sie wurde auf einem gefälschten Dokument gegründet. Das ist die Geschichte von Hamburg."
  - Técnica: **lista de desgraças da cidade numa frase + virada curiosa (fundada com documento falso) + frase do título**, em 17 s.
- **Hook (Belém, pt) [O]:** "Uma cidade europeia, teatro de ópera, largas avenidas… Só que ela não fica na Europa, e sim sobre a própria linha do Equador… Do que vive uma cidade cuja força inteira é ser a única porta?"
  - Técnica: **contraste de lugar + pergunta central**. O texto soa traduzido ("As cidades que foram erguidas… e a uma que, desde o começo, foi posta à porta"), então o canal deve ser de operação estrangeira [I].
- **Título [O]:** "Die ganze Geschichte <Cidade> in N Minuten" e "Toda a história de <Cidade> em N minutos — <subtítulo de identidade>" (em pt, o subtítulo vem depois do travessão: "a única porta da Amazônia", "uma ópera no meio da selva"). Os vídeos são mais longos (17–37 min).
- **Thumb [O]:** **template universal em de/en/pt**: panorama realista de IA da cidade antiga, **NOME gigante** em cima (amarelo, preto ou mármore) e **"ANO → 2026" com seta** embaixo (`thumbs/cidades-*.jpg`). Não tem personagem.
- **Edição [O]:** **fotorrealismo de IA** ("K.I. Rekonstruktion", "AI Reconstruction"), não quadrinho; 7–13 cortes/min, mais lento. O Paraná no Tempo usa a variante "Assim Era Viver em <cidade> em 1950", que deu o maior hit em pt (511 mil).

**Síntese [I].** A **estrutura** (promessa de história completa + N minutos + capítulos + abertura em 15–50 s) se transfere. O **gatilho do hook** muda conforme o nicho:
- **empresas:** origem improvável × gigante de hoje;
- **guerras:** números e paradoxo ("venceu as batalhas e perdeu a guerra");
- **cidades:** desgraças e identidade do lugar;
- **Archive:** vítima humana.

O **visual** também muda: empresas copiam o quadrinho do Archive, guerras usam cartoon com mapa e cidades usam fotorrealismo. No título, empresas e cidades mantêm o N; guerras põem o N na thumb.

---

## 4. Ranking de oportunidades (pt-BR)

Notas de 1 a 5. **Demanda tem peso 2**; nas outras notas, 5 = melhor (concorrência baixa, RPM alto, viabilidade alta, risco baixo). Total máximo de 30.

| # | Subnicho | Demanda (×2) | Concorrência pt | RPM [I] | Viabilidade na pipeline | Risco de política | **Total** |
|---|---|---|---|---|---|---|---|
| 1 | **Negócios: empresas, marcas, tecnologia e dinheiro** | 5 (en: 2 canais de 1 mês com ~1 mi/mês e mediana > 80 mil; pt: dinheiro 524 mil, Odebrecht 1,0 mi) | 3 (pt: 0 no molde; en: onda de ~300 clones) | **5** (US$ 6–12 en → 1,5–4,2 pt) | **5** (o boneco de cabeça redonda e o template de thumb do Archive são o que já fazemos) | 4 (marcas: uso nominativo; evitar difamação e logos como se fossem oficiais) | **27** |
| 2 | **Guerras e conflitos específicos** | 5 (Unknown Frequencies: mediana de 663 mil; Historia en Minutos es: 570 mil/mês em 49 d; Chronofold 536 mil) | 3 (pt: 0 em narrativa cartoon; resumos escolares dominam a busca) | 3 (US$ 4–8 en, com provável corte por violência → 1–2,8 pt) | **5** (mapas + cartoon = `historia-ptbr`) | 3 (violência e eventos sensíveis → anúncio limitado; sem sangue nem símbolos) | **24** |
| 3 | **Cidades e regiões (Brasil e mundo lusófono)** | 5 (de: mediana de 141 mil; pt: Paraná no Tempo ~811 mil/mês em 69 d, Belém 167 mil) | 3 (4 canais pt novos em 3 meses; cada cidade é uma palavra-chave própria) | 2 (história/viagem, público local pt: US$ 1–2,8) | 4 (fotorrealismo de IA é outro estilo; dá com `img_openai`) | **5** (baixo; marcar "conteúdo sintético realista") | **24** |
| 4 | Commodities e produtos que mudaram o mundo (café, açúcar, sal, ouro, milho) | 3 (es: Historia Del Comercio ~1,4–2 mi/mês, mas em vídeos de 45–58 min; pt: Origem Do Sabor fracassou) | 4 | 4 | 5 | 5 | **24** (menos prova em pt) |
| 5 | Religiões e Bíblia | 5 (Más Allá De Los Versos 4,2 mi/mês; Tiempos Bíblicos 476 mil/mês em 102 d; pt: Reforma Protestante 80 mil em 6 d) | 2 (es/pt lotados) | 3 [I: religião sem referência na tabela] | 4 | 3 (tema sensível, comentários, precisão doutrinária) | **22** |
| — | Esportes | 4 (SoccerJM, Copas 4–5 mi) | 2 | 3 | 3 (sem imagens de jogo perde força) | 4 | 20 |
| — | Crime, cartéis e drogas | 4 (Sinaloa 316 mil; Drugs 736 mil; PCC 3,2 mi em pt) | 3 | 2 | 4 | **1** (drogas e crime organizado → anúncio limitado e risco de remoção por glamorização) | 18 → **descartar** |
| — | Cultura pop, lore e games | 5 | 2 | 3 | 2 | 1 (trechos de obras com copyright; "conteúdo reutilizado") | **descartar** |

### Números de negócio (estimativas, em faixa) [I]
| Subnicho | Referência | Receita da referência/mês | Nossa versão pt-BR (10–20% das views) |
|---|---|---|---|
| Negócios | CEOzoned ~1,19 mi/mês × US$ 6–12 | US$ 7,1–14,3 mil (se monetizado) | 119–238 mil views × US$ 1,5–4,2 = **US$ 180–1.000/mês** |
| Guerras | Unknown Frequencies ~1,2 mi/mês × US$ 4–8 | US$ 4,8–9,6 mil (antes de limitação) | 120–240 mil × US$ 1–2,8 = **US$ 120–670/mês** |
| Cidades | Paraná no Tempo (já é pt) ~811 mil/mês × US$ 1–2,8 | US$ 810–2.270 | 81–162 mil × US$ 1–2,8 = **US$ 80–450/mês** |

- YPP: com vídeos de 12–15 min e 40% de retenção, as 4.000 h exigem **~40–50 mil views**, além de 1.000 inscritos.
- **Custo por vídeo na nossa pipeline:** ~US$ 7–9 (Fish ~US$ 0,25 + ~170–200 imagens `medium` a ~US$ 0,042), conforme `conhecimento/anti-padroes.md` (Egito US$ 8,55 em imagens).
- **Monetização das referências:** CEOzoned, Unknown Frequencies, Geschichte. Lebt., Historia en Minutos, Ruínas Vivas e Problema de Rico têm anúncios na página (indício). A Built On You não tem anúncios na página, apesar de elegível pelas horas.

### 10 temas para cada um do top 3 (títulos pt-BR; evidência [O] ou **Hipótese**)

**1. Negócios: "A história INTEIRA da <X> em N minutos"**
| # | Título | Evidência |
|---|---|---|
| 1 | A história INTEIRA da Coca-Cola em 11 minutos | CEOzoned 338 mil em 25 d |
| 2 | A história INTEIRA da Amazon em 15 minutos | Built On You 371 mil em 30 d |
| 3 | A história INTEIRA da NVIDIA em 13 minutos | CEOzoned 135 mil em 20 d; tema quente (IA) |
| 4 | A história INTEIRA do dinheiro no Brasil: do réis ao Pix em 15 minutos | Problema de Rico 524 mil (pt); o loop "8 moedas" foi o gancho dele |
| 5 | A história INTEIRA do ChatGPT em 12 minutos | CEOzoned 155 mil; Smart Code (IA) 279 mil |
| 6 | A história INTEIRA da SpaceX (ou de Elon Musk) em 10 minutos | CEOzoned 237 mil / 233 mil; Crayon Capital 544 mil |
| 7 | A história INTEIRA do McDonald's em 12 minutos | Michael Girdley "Why Nobody's Eating McDonald's" 1,43 mi |
| 8 | A história INTEIRA da Toyota em 14 minutos | Built On You 197 mil em 21 d |
| 9 | A ascensão e a queda da Odebrecht em 15 minutos | Curioso Mercado 1,0 mi (pt). **Cuidado jurídico** (fatos e fontes) |
| 10 | A história INTEIRA da Varig em 13 minutos | **Hipótese** (marca brasileira com "ascensão e queda"; ver Phebo 846 mil e RFFSA 48 mil em pt) |

**2. Guerras específicas: "A história INTEIRA da <guerra> em N minutos"** (pode entrar no `historia-ptbr`)
| # | Título | Evidência |
|---|---|---|
| 1 | A história INTEIRA da Segunda Guerra Mundial em 15 minutos | Unknown Frequencies 2,12 mi; Historia en Minutos es 175 mil; Infonimados es 18,9 mi |
| 2 | A história INTEIRA da Guerra do Vietnã em 15 minutos | 955 mil (en); 211 mil (es); Memorias de Pez 5,2 mi (es) |
| 3 | A história INTEIRA da Primeira Guerra Mundial em 14 minutos | 744 mil (en); 108 mil (es); Débora Aladim 4,9 mi (pt) |
| 4 | Stalingrado: a batalha mais mortal da história em 15 minutos | Historia en Minutos 273 mil (o maior hit do canal) |
| 5 | A história INTEIRA da Guerra Civil Americana em 15 minutos | Agent Flappy 1,30 mi |
| 6 | A história INTEIRA do Afeganistão em 15 minutos | Chronofold 536 mil |
| 7 | A história INTEIRA das Cruzadas em 15 minutos | This Is History 533 mil; Débora Aladim 1,2 mi (pt) |
| 8 | A história INTEIRA da Revolução Americana em 14 minutos | Agent Flappy 506 mil; Matt Reconstructs 1,28 mi |
| 9 | A história INTEIRA da Guerra do Paraguai em 15 minutos | **Hipótese** (ângulo Brasil; maior guerra da América do Sul) |
| 10 | A história INTEIRA da Guerra da Coreia em 13 minutos | **Hipótese** (buscada no garimpo, sem hit no molde) |
- A **Guerra Fria** fica fora daqui, porque é do `dossie-ptbr`: Archive 117 mil, Unknown Frequencies 582 mil.

**3. Cidades: "Toda a história de <cidade> em N minutos"** (ou "A história INTEIRA de…")
| # | Título | Evidência |
|---|---|---|
| 1 | A história INTEIRA do Rio de Janeiro em 20 minutos | Ruínas Vivas 87 mil; O Reconstrutor "primeira favela" 406 mil |
| 2 | A história INTEIRA de Curitiba em 18 minutos | Paraná no Tempo 314 mil |
| 3 | A história INTEIRA de Belém em 18 minutos | Ruínas Vivas 167 mil (concorrente direto) |
| 4 | A história INTEIRA de Cascavel em 15 minutos | Paraná no Tempo "Assim era viver em Cascavel em 1950" 511 mil |
| 5 | A história INTEIRA de Londrina em 15 minutos | Vozes do Brasil Antigo 74 mil; Paraná no Tempo 166 mil |
| 6 | A história INTEIRA de Manaus em 18 minutos | Ruínas Vivas 40 mil |
| 7 | A história INTEIRA de Salvador em 18 minutos | **Hipótese** (1ª capital) |
| 8 | A história INTEIRA de Porto Alegre em 15 minutos | **Hipótese** (o padrão Sul do Paraná no Tempo) |
| 9 | A história INTEIRA de Lisboa em 18 minutos | **Hipótese** (público pt-PT + pt-BR) |
| 10 | A história INTEIRA de Brasília em 12 minutos | **Hipótese** |
- **Atenção [O]:** "Toda a história de São Paulo em 26 minutos" teve só 2 mil views no Ruínas Vivas. Megacidade não é garantia; **cidades médias com orgulho local** renderam mais.

---

## 5. Comparação com a manada (`pesquisa/archive-in-minutes/LEVANTAMENTO.md`) e recomendação consolidada

O job paralelo terminou: o arquivo já existia quando fechei esta análise (04/11, fim da tarde). A recomendação dele é **TESTAR em pt-BR o `dossie-ptbr`** ("A história INTEIRA da <organização> em N minutos", piloto KGB).

| | Manada: organizações (job paralelo) | Subnicho: Negócios (esta ponta) |
|---|---|---|
| Prova em inglês [O] | Archive: ~2,8 mi/mês, mediana de 86 mil, 19 vídeos | CEOzoned + Built On You: ~1 mi/mês cada, medianas de 81–91 mil, com 1 mês de vida |
| Saturação em inglês [O] | 14 clones em 3 semanas, mediana < 1 mil | **~292 canais novos desde 07/2026**, 2 acertos. Mais saturado ainda |
| Prova em pt-BR [O] | Indireta: Fragmentos da História (Hiena da Gestapo 212 mil), Total History | **Direta, no molde exato:** "A HISTÓRIA INTEIRA do DINHEIRO em 15 minutos", 524 mil. Também Odebrecht 1,0 mi, 3corações 713 mil e Phebo 846 mil (outros formatos) |
| Concorrência pt no molde [O] | 0 | 0 |
| RPM [I] | História US$ 4–8, com risco de anúncio limitado (nazismo e violência) | Negócios US$ 6–12, sem esse risco |
| Risco de política [I] | Médio-alto (organizações violentas, nazismo, extremismo; precisa de contexto EDSA) | Baixo-médio (marcas e difamação) |
| Pipeline [O] | Graphic novel com rostos reconhecíveis (Putin, Himmler): um pouco diferente do nosso | **O boneco de cabeça redonda que já usamos** + template de thumb do Archive |
| Receita pt-BR [I] | US$ 280–1.560/mês (cenário 10–20%) | US$ 180–1.000/mês (cenário 10–20%), mas com mais temas perenes e brasileiros (Varig, Odebrecht, Plano Real, Petrobras, Embraer) |
| Fôlego de temas [I] | ~10 organizações fortes; o resto cai para 20–40 mil no próprio Archive | Centenas de marcas, empresas, bilionários e tecnologias; renova com notícias (NVIDIA, OpenAI) |

**Recomendação consolidada [I]: diversificar em vez de dobrar a aposta no mesmo tema.**
1. **Canal novo a TESTAR primeiro: Negócios em pt-BR.** É o mesmo esqueleto da fábrica (fórmula, quadrinho, capítulos, hook curto), com RPM melhor, risco menor, prova direta em pt e catálogo de temas quase infinito. Pilotos: Coca-Cola, NVIDIA e "o dinheiro no Brasil, do réis ao Pix". Critério: o mesmo do job paralelo (média ≥ 3 mil ou 1 vídeo ≥ 15 mil, % assistido ≥ 35%, em 14 dias).
2. **`dossie-ptbr` (organizações):** manter como teste, se o Rodrigo quiser 2 canais em paralelo; o roteiro da KGB já está pronto. Se for só um canal, deixar para depois do teste de Negócios, ou rodar 2–3 organizações (KGB, Mossad, CIA) **dentro do `historia-ptbr`** como experimento barato.
3. **Guerras específicas → `historia-ptbr`, sem canal novo.** É o mesmo público e o mesmo visual. A Unknown Frequencies e a Historia en Minutos mostram que guerras famosas rendem 5–10 vezes mais que países pouco buscados. Priorizar 2ª Guerra, Vietnã e Stalingrado.
4. **Cidades: hipótese para o canal 3**, em pt-BR, com reconstrução fotorrealista e foco em cidades médias e capitais regionais. A janela está fechando (4 canais pt em 3 meses). Decidir em até ~30 dias ou descartar.
5. **Descartar:** crime e drogas (política), cultura pop e lore (copyright) e, em inglês, qualquer subnicho do formato (saturado nas duas pontas).

**Decisões do Rodrigo:** criar ou não o canal de Negócios (nome sugerido: "Empresas em Minutos" ou "Negócio Inteiro"; handles **não** verificados), escolher entre 1 ou 2 canais novos e aprovar o teto de ~US$ 9 por piloto.

---

## 6. Limitações e pendências
- **Sem `search.list`:** toda a descoberta foi feita por yt-dlp (até 25–30 resultados por busca, ordem do YouTube para um usuário anônimo via WARP). Podem faltar canais com títulos fora dos moldes buscados. O WARP funcionou a execução inteira (`warp=on`).
- **Classificação por palavra-chave:** os subnichos da seção 3a vêm de regex no título e erram, por exemplo, em nomes de cidades no genitivo alemão, "[NO AI]" lido como tecnologia e canais que misturam temas. A tabela da seção 2 foi curada à mão.
- **Views/mês** são extrapolações de canais com 3–40 semanas. Não há série histórica: não gravei em `garimpo_*`, para não colidir com o outro job. O "crescimento recente" é a soma das views dos vídeos dos últimos 30 e 90 dias.
- **RPM** vem da tabela do playbook. **Alemão e religião não estão na tabela**; usei ~0,8–1,0× do inglês para alemão e US$ 2–5 para religião, como **Hipótese**. Monetização = indícios (horas estimadas + anúncios na página), não prova.
- **Idade "(criação)":** em canais com mais de 300 uploads, a idade é a da criação do canal, não a do 1º vídeo.
- **watch.py** gravou 7 linhas em `youtube.assistidos` (upsert por `video_id`, tabela do watch, não do garimpo). Os assets ficaram em `assets/` desta pasta. As imagens (`*.jpg`) seguem o `.gitignore`, exceto as thumbs de exemplo, que adicionei com `git add -f` (18 arquivos, < 150 KB cada, ~1,2 MB no total).
- **Dados brutos** grandes (`busca_*.jsonl`, `videos_formato.json`, `canais_api.json`, `canais_detalhe.json`) foram comprimidos com gzip. Para reproduzir: `gunzip dados/*.gz` e depois rodar os scripts na ordem `buscar.py` → `buscar2.py` → `agregar.py` → `enriquecer.py` → `classificar.py` → `canais_detalhe.py` → `concorrencia.py` → `tabela.py`, com `tools/.venv/bin/python -I`.
- **Não editei `conhecimento/`** (regra do brief). Sugestões para o próximo commit de quem cuidar dele:
  - **hooks.md:** "origem improvável × gigante de hoje" (Coca-Cola, 16 s) e "reformulação-paradoxo + todos morreram, ele continua aqui" (Amazon). É a mesma técnica do nosso Egito, validada em outro nicho (Hipótese até termos retenção).
  - **titulos.md:** guerras põem o N na thumb, não no título; cidades usam "Toda a história de X em N minutos — <identidade>".
  - **anti-padroes.md:** "ser o 293º canal de empresas em inglês": 292 canais novos desde 07/2026, com 2 acertos (dados/concorrencia.json, 2026-11-04).
