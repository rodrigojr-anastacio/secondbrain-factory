# GTA 6: pesquisa de oportunidade para um teste no canal em inglês (Clearance Required) — 20/11/2026

## Resumo (10 linhas)
1. **Lançamento confirmado:** GTA 6 saiu em **19/11/2026**, só para PS5 e Xbox Series. A Sensor Tower estima **US$ 2,36 bi e ~24,6 mi de cópias no dia 1**, contra ~US$ 0,8 bi do GTA V em 2013. A Take-Two ainda não divulgou número oficial. Metacritic **99**.
2. **O que está bombando** é jogar e rosto: IShowSpeed 35,8 mi em 5 h, Techno Gamerz 18,9 mi, CarryMinati 17,4 mi, walkthroughs de 3–9 mi, IGN Review 8 mi. Isso não é para nós.
3. **Faceless funciona na cauda:** "GTA 6's development explained in 8 minutes" (Continue Anyway, **1,9 mil inscritos**) tem **1,31 mi em 17 dias (133× a mediana do canal)**. "Rockstar Turned Real Miami Into Vice City" (Project VI, 6,1 mil inscritos) tem **405 mil (109×)**. "Why GTA 6 Took 13 Years" (Andrés Delgado, 3,7 mil inscritos) tem **34 mil em 5 dias (114×)**.
4. **Mas a mediana do faceless é ruim:** nos últimos 30 dias, os explicativos de história/hype têm mediana de **117 views** (122 vídeos) e os de lugares reais, **77 views** (165 vídeos). Só 13–14% passam de 5× a mediana do canal. É loteria com cauda gorda.
5. **Saturação:** pelo menos **222 uploads "GTA 6" hoje** e **29 na última hora**. A busca do YouTube tem teto, então são pisos. A fórmula "Rockstar Turned Miami Into Vice City" já tem **25 vídeos em 60 dias** e "Why GTA 6 Took 13 Years" tem **6 ou mais**.
6. **Vida útil boa no ângulo explicativo:** GTA 5 "in real life" / lugares reais seguem rendendo anos depois (Mythpat 31 mi, SD1ONE 3,2 mi, Gamology 3,4 mi). No GTA 6, os explicativos de história/hype com mais de 180 dias têm mediana de **68 mil** (n = 20).
7. **Riscos:**
   - Content ID / DMCA da Take-Two em trailer, gameplay, vazamento, spoiler e até em imagem de IA "GTA 6" falsa. Nosso pipeline não usa footage: o risco fica baixo se não imitarmos personagem nem arte-chave.
   - Logo oficial proibido; "GTA 6" escrito é uso nominativo.
   - Política de conteúdo inautêntico do YPP para notícia lida por voz sintética.
8. **Brechas para nós:**
   - (A) **o negócio por trás do hype:** 13 anos → US$ 2,4 bi em 1 dia, com números e linha do tempo;
   - (B) **a Flórida real por trás do mapa de Leonida:** região por região, com foto livre (NPS, LoC, DVIDS) e mapa 2D. É a ponte com "lugares".
   - Lore/"Florida Man" sozinho não se sustenta (mediana de 42 views, nenhum vídeo com 100 mil): entra como capítulo do B.
9. **Recomendação: FAZER 1 teste agora**, ângulo **B** (mais nosso e mais perene), com o **A** como 2º, se o B passar de ~5 mil views em 72 h. Usar o **Clearance como está** (220 views e 0 inscritos no total: o custo de "sujar" o nicho é quase zero); só renomear se o teste pegar.
10. **Janela:** produzir hoje ou amanhã e **publicar até dom 22/11**. Depois de ~26/11 (Thanksgiving/Black Friday e GTA Online) o pico do lançamento já passou e sobra só a cauda de busca.

Teto: **US$ 0** gasto (nada de imagem ou voz). Cota do YouTube: **~2.170 unidades** (videos/channels/playlistItems, sem `search.list`). Dados: `corpus.csv` (1.926 vídeos), `dados/` (brutos), `mosaico.jpg` / `mosaico-320.jpg`, `scripts/`.

---

## 1. O que está bombando agora (en, 7–30 dias)
**Método.** 92 buscas no yt-dlp via WARP: 46 temas × (relevância + filtro de data "este ano"), em 5 grupos (geral, lugares, hype, lore, gta5). Encontraram 1.926 vídeos e 1.326 canais. Os números vêm de `videos.list` e `channels.list`. A mediana de cada canal (1.051 canais) é a dos últimos 50 uploads com mais de 180 s e pelo menos 3 dias de idade. O formato foi classificado pelo título (`scripts/analisar.py`; "outro" = não classificado, em geral gameplay de canal grande).

> Cuidado com o "×mediana" de canal minúsculo: um canal de 300 inscritos com mediana de 100 views vira "×4.000" com um único hit. Por isso também filtrei por views absolutas (≥ 5 mil).

### Top por views/dia (últimos 7 dias, en, longos): todos exigem jogar ou rosto
| Vídeo | Canal (inscritos) | Views | Idade | ×med | Formato |
|---|---|---|---|---|---|
| PLAYING GTA 6 RIGHT NOW | IShowSpeed (63 mi) | 35,8 mi | 5 h | 10× | live |
| MY FIRST DAY IN VICE CITY | Techno Gamerz (53,8 mi) | 18,9 mi | 1,2 d | 1,7× | gameplay |
| CARRYMINATI PLAYS GTA VI | CarryisLive (12,9 mi) | 17,4 mi | 1,9 d | 18× | live |
| GTA 6 Walkthrough Part 1 (No Commentary) | MKIceAndFire (4,8 mi) | 9,5 mi | 2,0 d | 40× | walkthrough |
| GTA 6 Review | IGN (20 mi) | 8,0 mi | 2,3 d | — | review |
| GTA 6 – Stealing a Jet From the Military Base | TmarTn2 (5,7 mi) | 7,5 mi | 2,0 d | 19× | gameplay |
| GTA 6 – Before You Buy | gameranx (8,7 mi) | 5,7 mi | 2,1 d | 6,7× | review |
| GTA 6 Good Ending (Jason & Lucia Survive) | MELOO (388 mil) | 1,1 mi | 8 h | 62× | spoiler |
| GTA VI vs GTA V – Physics and Details | Betaz (234 mil) | 1,6 mi | 1,3 d | 6× | comparação com gameplay |

**Por formato (30 dias, en, longos, n = 910):**

| Formato | n | Mediana de views | Mediana de views/dia | % ≥ 5× |
|---|---|---|---|---|
| jogar/rosto | 238 | 63 mil | 34 mil | 26% |
| "outro" (gameplay de canal grande) | 166 | 74 mil | 33 mil | 23% |
| news | 34 | 57 mil | 13 mil | 12% |
| explicativo/lista (exige footage) | 185 | 24 mil | 4,7 mil | 26% |
| **história/hype (faceless)** | 122 | **117** | 27 | 13% |
| **lugares reais** | 165 | **77** | 17 | 14% |

**Leitura [I]:** a demanda está no jogo em si (jogar, ver, decidir se compra). O explicativo faceless tem muita oferta de canal pequeno e mediana de quase zero. Só a cauda de cima paga.

## 2. Brechas para um canal faceless pequeno (dados)
Canais com menos de 250 mil inscritos, ≥ 5× a mediana, ≥ 5 mil views e até 30 dias: **80 vídeos**. Por formato: explicativo/lista 29, jogar 17, lugares-reais 15, outro 14, história/hype 3, news 2. Mosaico (linhas 4–6) em `mosaico.jpg`.

### Ângulo B: os lugares reais por trás de Leonida/Vice City (ponte com o Clearance)
| Vídeo | Canal (inscritos) | Views | Idade | ×med |
|---|---|---|---|---|
| Rockstar Turned Real Miami Into Vice City for GTA 6 | Project VI (6,1 mil) | 405 mil | 23 d | 109× |
| GTA 6 Is Taking Over Miami in Real Life | Jonny Costa (1,3 mil) | 288 mil | 16 d | 50× |
| Rockstar Turned Miami Into Vice City For GTA 6! | Joel Franco (56 mil) | 561 mil | 28 d | 24× |
| GTA 6 in Real Life: Rockstar Turned Miami Into Vice City | Jose Salas (6,3 mil) | 62 mil | 9 d | 124× |
| GTA 6 Map vs Real Life: All 6 Regions Matched to Florida | QuickMind Gaming (227) | 11 mil | 12 d | 24× |
| Rockstar Transformed Miami into Real Life GTA 6 Vice City | TmarTn2 (5,7 mi) | 1,31 mi | 20 d | — |

- **[O]** O sucesso recente do "Miami virou Vice City" é sobre **o marketing no mundo real**: Câmara de Miami Beach aprovando campanha, Miami Heat "Vice City", carro misterioso de US$ 643 mil. É mais pauta de notícia do que o mapa. O Project VI usa TV local (CBS Miami) e cenas do jogo, cortadas a 25 por minuto (watch.py).
- **[O]** O "mapa × Flórida real" (região por região) está **pouco explorado e com números modestos**: QuickMind 11 mil; Sixth State "The Whole GTA 6 Map Explained" com 5,4 mil (268×, canal de 308 inscritos).
- **[O]** A vida útil é a melhor do tema: no GTA 5, "in real life" / lugares reais somam 31 mi (Mythpat), 3,4 mi (Gamology), 3,2 mi (SD1ONE). No GTA 6, "Visiting GTA 6 Trailer Locations In Real Life!" (Joel Franco) tem 1,53 mi em 3 anos e "All GTA 6 Real Life Florida Man References" (TmarTn2) tem 1,07 mi.
- **Fatos com fonte (subagente de pesquisa):**
  - As 6 regiões oficiais são Vice City, Leonida Keys, Grassrivers, Port Gellhorn, Ambrosia e Mount Kalaga ([rockstargames.com/VI](https://www.rockstargames.com/VI/only-in-leonida)). Lucia esteve na Leonida Penitentiary; Jason serviu no Exército.
  - A correspondência com lugares reais é da imprensa, não da Rockstar ([GTABoom](https://www.gtaboom.com/real-world-regions-behind-gta-6-trailer-2-4844)): Miami; Florida Keys/Overseas Highway (Key Lento = Key Largo); Everglades; Panama City/Panhandle; Clewiston e o cinturão do açúcar do Lake Okeechobee; Apalaches.
  - A Rockstar fez viagens de pesquisa com policiais na Flórida ([Dexerto](https://www.dexerto.com/gta/rockstar-joined-gang-members-and-cops-for-gta-6-research-trips-in-florida-3415508/)).
  - O trailer 1 recria **9 vídeos virais reais da Flórida**: jacaré na piscina (2019), twerk na MacArthur Causeway (2017), jacaré no Walmart (2013), mulher com dois martelos (2020) e outros ([Know Your Meme](https://knowyourmeme.com/editorials/in-the-media/every-reference-to-real-life-videos-in-the-grand-theft-auto-vi-trailer)).
  - **Base militar no jogo × Homestead ARB / NAS Key West = só especulação de fã. Não vender como fato.** "Alligator Alcatraz": nenhuma ligação na imprensa.
- **Material livre:**
  - Everglades: imagens do NPS ([nps.gov](https://www.nps.gov/ever/learn/photosmultimedia/imagesforpublication.htm)).
  - Seven Mile Bridge: HAER FL-2 na Library of Congress ([loc.gov](https://www.loc.gov/item/fl0293)).
  - Miami Beach Art Deco: HABS ([loc.gov](https://loc.gov/pictures/item/fl0160/)) e Carol Highsmith.
  - NAS Key West ([DVIDS](https://dvidshub.net/image/2535519/naval-air-station-key-wests-fleming-key-left-sigsbee-park-top-and-trumbo-point-annexes)) e Homestead ARB ([DVIDS](https://www.dvidshub.net/image/9570374/patriot-forge-26)).
  - Conferir a licença item por item na produção.

### Ângulo A: a história do hype / o negócio
| Vídeo | Canal (inscritos) | Views | Idade | ×med |
|---|---|---|---|---|
| GTA 6's development explained in 8 minutes | Continue Anyway (1,9 mil) | 1,31 mi | 17 d | 133× |
| How I'd Explain the GTA 6 Hype to a Normie | Scumbucket (1,2 mil) | 1,38 mi | 28 d | enorme (canal minúsculo) |
| Inside the Engine Behind GTA VI | Speclizer (61 mil) | 1,02 mi | 10 d | 35× |
| GTA 6's Billion-Dollar Hype Machine | CNBC (4,2 mi) | 1,05 mi | 5 d | — |
| The Hunt for the Biggest GTA 6 Leaker | Mors Mutual Insurance (640 mil) | 327 mil | 5 d | — |
| 13 Years of GTA 6 Development Explained | Saukko505 (24,5 mil) | 51 mil | 7 d | — |
| Why GTA 6 Took 13 Years | Andrés Delgado (3,7 mil) | 34 mil | 5 d | 114× |

- **[O]** Os 3 vistos com watch.py são faceless:
  - Continue Anyway: colagem com mascote sobre gameplay do GTA 5, ano no canto, 9 cortes/min, hook "Rob Nelson … research trip to Miami".
  - Andrés Delgado: hook de número ("$800 million in a single day … a teenager on bail … TV streaming stick"), 8 cortes/min.
  - Scumbucket: perguntas em série, "to understand GTA 6 you need to understand GTA 5".
- **[O]** "Why GTA 6 Took 13 Years" tem **6 ou mais** vídeos em 60 dias e mediana do grupo de **164 views**: fórmula gasta. O ângulo **número/negócio** (o dia de US$ 2,4 bi, ~3× o GTA V) é novo de ontem e só os canais de notícia (CNN, CNBC, BBC) o cobriram.
- **Fatos com fonte:**
  - Desenvolvimento confirmado em 04/02/2022 ([Game Informer](https://gameinformer.com/2022/02/04/rockstar-confirms-the-next-grand-theft-auto-game-is-in-active-development)).
  - Vazamento de set/2022: ~90 clipes, Arion Kurtaj/Lapsus$, internação indefinida em dez/2023, custo de US$ 5 mi segundo a Rockstar ([BleepingComputer](https://www.bleepingcomputer.com/news/security/lapsus-hacker-behind-gta-6-leak-gets-indefinite-hospital-sentence/amp/)).
  - Trailer 1 (dez/2023): ~93 mi de views em 24 h no YouTube ([TweakTown](https://www.tweaktown.com/news/105101/grand-theft-auto-6-trailer-2-fails-to-beat-the-world-record-set-by-1/index.html)).
  - Trailer 2 (mai/2025): 475 mi somando plataformas, número da própria Rockstar ([VGC](https://www.videogameschronicle.com/news/at-nearly-half-a-billion-views-rockstar-says-gta-6s-new-trailer-is-the-biggest-video-launch-of-all-time)).
  - Adiamentos: 2025 → 26/05/2026 → 19/11/2026 ([PC Gamer](https://www.pcgamer.com/games/action/grand-theft-auto-6-is-delayed-to-november-these-extra-months-will-allow-us-to-finish-the-game-with-the-level-of-polish-you-have-come-to-expect-and-deserve)).
  - Custo nunca divulgado: US$ 1–1,5 bi pelos analistas, US$ 2–3 bi em boatos ([NME](https://www.nme.com/news/gaming-news/grand-theft-auto-6-cost-development-billion-rockstar-3937967), [Destructoid](https://destructoid.com/why-the-rumored-2-billion-gta-6-budget-is-quite-unlikely-to-be-real)).
  - Vendas do dia 1: Sensor Tower, estimativa ([Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/gta-6-just-sold-estimated-150701356.html), [Deadline](https://deadline.com/2026/11/gta-6-sales-launch-day-surge-videogame-1237229514/)).

### Lore / casos reais (Jason e Lucia, Florida Man)
- **[O]** "florida man|meme" em 60 dias: 30 vídeos, mediana de **42 views**, **nenhum** com 100 mil. Jason/Lucia rende só com gameplay ou spoiler (finais).
- **Fatos:** "Bonnie e Clyde" vem da reportagem da Bloomberg (Schreier, jul/2022) e nunca foi confirmado pela Rockstar ([TechRadar](https://techradar.com/news/gta-6-will-feature-a-female-protagonist-as-part-of-a-bonnie-and-clyde-pair)). Não achei casal real da Flórida como modelo.
- **Decisão [I]:** não vale como vídeo próprio. Os 9 memes reais do trailer entram como capítulo do B.

### Vida útil (o que segue rendendo depois do pico)
- GTA 5 com mais de 1 ano, mediana por formato no corpus (há viés de busca, porque a relevância favorece os grandes): lugares reais **538 mil** (n = 26), explicativo **1,37 mi** (n = 16), história/hype **1,52 mi** (n = 6).
- GTA 6 com mais de 180 dias (vídeos de antes do lançamento): história/hype **68 mil** (n = 20), lugares reais **42 mil** (n = 24).
- **[I]** O B tem mais cauda longa: busca "GTA 6 real life" / "Leonida vs Florida" por anos, como no GTA 5. O A pega mais pico agora e envelhece quando sair o número oficial (mas pode ser atualizado no título).

## 3. Riscos
| Risco | Nível | Detalhe e mitigação |
|---|---|---|
| **Direitos / Content ID** | médio → baixo no nosso pipeline | A política da Rockstar (atualizada em 10/01/2025) tolera uso **não comercial**. Monetizar com material do jogo fica fora. Proíbe vazamento e spoiler mesmo depois do lançamento ([Insider Gaming](https://insider-gaming.com/rockstar-might-dmca-gta-6-spoilers/)). A Take-Two derrubou em massa o vazamento de 2022 ([VGC](https://videogameschronicle.com/news/take-two-strikes-gta-6-leaked-footage-seemingly-confirming-legitimacy)), um mapa recriado ([PC Gamer](https://www.pcgamer.com/games/grand-theft-auto/playable-gta-6-map-nuked-without-warning-by-take-two-lawyers-my-guess-is-that-the-map-was-probably-a-little-too-accurate)) e **imagens de IA "GTA 6" falsas** em 2026 ([Notebookcheck](https://www.notebookcheck.net/GTA-6-trailer-3-release-anticipated-as-Take-Two-targets-fake-AI-generated-leaks.1351256.0.html)). **Mitigação:** zero trailer, gameplay, áudio, logo, arte-chave, vazamento e spoiler; imagem gerada genérica de Flórida/Miami (sem Jason/Lucia nem pôster); mapa 2D **nosso** da Flórida real, sem redesenhar o mapa do jogo. |
| **Marca no título/thumb** | baixo | "GTA 6" escrito = uso nominativo ([Nominative use](https://en.wikipedia.org/wiki/Nominative_use)). Proibido o logo "grand theft auto VI" e qualquer coisa que pareça oficial. |
| **Conteúdo inautêntico (YPP)** | médio para o canal inteiro | Voz sintética lendo notícia é o alvo da regra de jul/2025 ([Ajuda](https://support.google.com/youtube/answer/1311392)). Precisa de análise original (o mapa × a Flórida real com fotos e mapas nossos; o negócio com números comparados) e nunca virar série de notícias por template. |
| **Saturação** | alto | ≥ 29 uploads/hora e ≥ 222 hoje (pisos). "Miami → Vice City": 25 vídeos/60 d; "Took 13 Years": 6+. Não usar essas fórmulas. |
| **Prazo do pico** | médio | Views/dia do faceless que pegou: Continue Anyway com 77 mil/dia ao longo de 17 dias (cauda longa já antes do lançamento). Com 1 noite de produção, o vídeo sai em 21–22/11, ainda na semana do lançamento. Depois de ~26/11 sobra a cauda de busca. |
| **Mudar o nicho do Clearance** | baixo | Hoje: 4 vídeos, **220 views no total, 0 inscritos** (Studio 14/11: CTR 2,17% no Midway). Não há audiência a perder. Mas, se o GTA pegar, o algoritmo passa a tratar o canal como de games, e os de guerra (e o Tarawa, id 46, pronto e não publicado) tendem a ir pior nele. |
| **Thumb sem arte oficial** | médio | 30 de 30 thumbs do mosaico usam arte oficial ou cena do jogo com o logo. A nossa vai destoar (bom para diferenciação), mas precisa de "GTA 6" escrito grande para o assunto ser identificado em < 1 s (CRIVO item 0). |
| **Fato fraco** | médio | Base militar e prisão reais, casal real: especulação de fã. Só entra com "fans think…" ou fica fora. Vendas = estimativa da Sensor Tower: dizer "estimated". |

**Visual viável com o nosso pipeline (sem footage):**
- **B:** fotos livres reais (NPS Everglades, LoC Seven Mile Bridge/Art Deco, DVIDS Key West/Homestead, Commons PD) + mapa 2D da Flórida com as 6 regiões + cortes ilustrados genéricos "neon Miami".
- **A:** linha do tempo, números grandes, gráfico GTA V × GTA 6, colagem gerada (servidor, calendário, pilha de dinheiro), capturas de manchete reescritas no código (não print de site).
- Os dois cabem em imagem gerada + texto no código e não exigem jogar.

## 4. Recomendação
**FAZER 1 teste**, barato (~R$ 50 na esteira normal), no **Clearance como está**: mesmo nome e banner, sem mexer na bíblia agora. Renomear (ex.: algo de "real places behind…") ou abrir canal novo **só se** o teste passar de ~5 mil views em 72 h ou de 20 mil em 7 dias. Canal novo agora custaria a janela: criação e OAuth são do Rodrigo, e um canal sem histórico de nada não ganha nada sobre um quase vazio.

**Ordem:** B primeiro (mais nosso, ponte com "lugares", cauda longa, risco de direitos menor); A como 2º, de preferência quando a Take-Two publicar o número oficial (gancho novo).

### Ângulo B: a Flórida real por trás do mapa
- **Títulos:**
  - **"The Real Florida Hidden Inside GTA 6's Map"** (42 caracteres)
  - **"Where GTA 6 Really Takes Place (Region by Region)"** (49)
- **Thumb (`antes-depois`):** à esquerda, foto real aérea da Seven Mile Bridge ou de Miami Beach (PD); à direita, a mesma cena em ilustração neon rosa/turquesa, cortada por uma linha diagonal. Texto: "GTA 6" grande, branco com contorno, no alto; uma etiqueta amarela "REAL" sobre a metade da foto. Sem logo e sem personagem.
- **Duração:** 12–14 min.
- **O que pegar de referência:**
  - QuickMind ("All 6 Regions Matched to Florida": a estrutura região por região, mas com foto real e nosso mapa 2D);
  - Project VI (o gancho do mundo real: Miami Beach aprovando campanha);
  - Know Your Meme (os 9 virais reais do trailer, como capítulo).
- **Fora:** a fórmula "Rockstar Turned Miami Into Vice City" e o "Visiting… in real life" (exige estar lá).

### Ângulo A: o negócio por trás do hype
- **Títulos:**
  - **"How GTA 6 Made $2.4 Billion in One Day"** (38 caracteres)
  - **"GTA 6: The 13-Year Bet That Paid Off in 24 Hours"** (48)
- **Thumb (`numero-estatistica`):** "13 YEARS → 1 DAY" em amarelo, número gigante; fundo de skyline neon de Miami ao pôr do sol com uma pilha de dinheiro crescendo como gráfico; etiqueta "GTA 6" branca no canto. O título dá o valor e a thumb dá o tempo (não repete a ideia).
- **Duração:** 10–12 min.
- **O que pegar de referência:**
  - Continue Anyway ("explained in 8 minutes": ritmo, ano no canto, colagem);
  - o hook de número do Andrés Delgado (US$ 800 mi de 2013 → silêncio → vazamento);
  - o recorte de negócio do CNBC.
- **Fora:** o título "Why GTA 6 Took 13 Years" (6+ clones).
- Valor sempre como "estimated" (Sensor Tower) até a Take-Two confirmar. Se o número oficial sair maior, atualizar o título.

**Janela:** produzir **hoje à noite ou sáb 21/11** (`fila.sh add … --agora` ou a noite de sábado) e **publicar sáb 21 ou dom 22/11, ~12:00–15:00 ET**. O A pode sair depois do anúncio oficial da Take-Two (provavelmente na próxima semana).

**Decisões do Rodrigo:** fazer ou não; usar o Clearance; produzir fora do calendário (`--agora`); publicar.

---
Arquivos:
- `corpus.csv`: 1.926 vídeos com views, views/h, views/d, ×mediana, formato, grupo e query;
- `dados/`: `busca.jsonl`, `videos.json`, `canais.json`, `medianas.json`, `analise.json` e `sat-*.json` (saturação);
- `mosaico.jpg` (1600 px, < 1 MB) e `mosaico-320.jpg`;
- `scripts/` (buscar, enriquecer, medianas, analisar, mosaico);
- watch.py de 4 referências em `pesquisa/tendencias/assets/2026-11-20/` (tUyjmeDG3Rw, 3FcWitnBFoo, KLS08czkBfw, JQEulR8gOsE).
