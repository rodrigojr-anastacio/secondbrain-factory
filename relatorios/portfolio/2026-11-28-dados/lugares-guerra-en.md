# Clearance Required (lugares-guerra-en): flopou? Continuar? (28/11/2026)

Só análise: nada mudou no canal, no backlog, na bíblia, no banco nem nos timers. Custo pago: US$ 0.
**Fontes:** `youtube.metricas_video` (snapshots até 28/11), `youtube.alcance_diario` (Reporting API: impressões e CTR, até 26/11), `analytics_trafego`, `analytics_retencao` e `analytics_publico` (Analytics API, até ~25/11), `youtube.studio_video` (só 1 export, do Midway, 1 dia), `financas.consumo`, `ops.fila_jobs` (custo equivalente do Claude), yt-dlp via WARP em 28/11 (9 canais × 30 vídeos + 19 buscas com filtro "este ano" por views). Brutos do mercado em `~/cache/tmp/clr-mercado/` (fora do git).

**Resposta curta:** sim, flopou, e o problema aparece já no 1º sinal: **ninguém clica**. O YouTube mostrou os 5 vídeos (4.622 impressões), o CTR foi **1,6%** (Dossier na mesma fase: 2,6–5,2%) e a distribuição de cada um foi cortada em 2–4 dias. A retenção também é fraca (27–40% de vídeos de 15–17 min). O subnicho ("lugar de guerra americano que você não pode visitar") também perdeu força: o próprio canal-modelo está caindo. Recomendo **encerrar o formato**, usar o Tarawa (já pronto, custo zero) como último teste e liberar a vaga do en para um canal novo.

---

## 1. Diagnóstico

### 1.1 Por vídeo
| # | título (no lançamento) | publicado | views 48 h | 7 d | total (28/11) | impressões (Reporting) | CTR | média vista / % visto | fonte de tráfego (views) | custo pago US$* |
|---|---|---|---|---|---|---|---|---|---|---|
| 001 | Why Can't You Visit Midway Atoll? | 13/11 | 13 | 13 | 18 | 379 (Studio 1 d: 323) | 2,11% (Studio 2,17%) | 5:23 / 31,8% | sugerido 7 · busca 5 · outros 3 | 1,96 (+1,04 API) |
| 002 | Why Can't You Visit Bikini Atoll? | 14/11 | 50 | 49 | 52 | 1.576 | **1,14%** | 6:23 / 39,8% | sugerido 27 · busca 21 | 0,71 (+0,86) |
| 003 | The Gettysburg Photos You Weren't Supposed to See | 15/11 | 29 | 118 | 122 | 1.281 | 2,19% | 4:29 / 29,7% | **navegação (home) 88** · sugerido 22 · busca 6 | 0,44 (+0,13) |
| 004 | Why Are There Still Bullet Holes at Pearl Harbor? | 16/11 | 22 | 45 | 47 | 912 | 1,64% | 4:06 / 27,2% | navegação 19 · sugerido 18 · busca 6 | 1,02 (+0,06) |
| 006 | Chernobyl Burned for Days Before the World Knew | 21/11 | 12 | 16 | 16 | 474 | 1,48% | 6:24 / 38,6% | sugerido 6 · busca 5 · outros 5 | 1,04 (+0,63) |
| 005 | Why Is America Digging Up Japanese Soldiers on Tarawa? | **não publicado** (pronto) | — | — | — | — | — | — | — | 0,50 (+0,06) |
| | **Total** | | | | **255** | **4.622** | **1,64%** | | 0 inscritos, 0 comentários, 0 likes | **5,74** (+2,78 API) |

\* Pago = Fish + fal + Runpod (inclui a amostra do Chernobyl, US$ 0,07). Entre parênteses, os créditos da API Anthropic (vêm com o Max). O Claude Code das etapas soma **US$ 75 equivalentes** (preço de lista, `ops.fila_jobs`, sem o 001), pagos dentro do Max fixo. O gasto real em dinheiro foi pequeno; o custo de verdade é a capacidade (noites, cota do Max) que não foi para o Dossier.
**Países:** só os EUA aparecem (149 das 255 views, 58%); o resto fica abaixo do limite de privacidade da API. **Dispositivo:** celular 107, computador 84, **TV 48** (público mais velho, típico de documentário de guerra).

### 1.2 Teve impressão e não teve clique (embalagem)
Impressões por dia (Reporting): cada vídeo recebeu **um lote de teste de 400–1.600 impressões nos primeiros 2–4 dias**, com CTR de 0,5–2,5%, e depois caiu para < 10 impressões/dia:
- Bikini: 721 → 573 → 188 → 28 → ~7/dia (CTR 1,8% → 0,7% → 0,5%).
- Gettysburg: 462 → 197 → 307 → 279 → ~4/dia (o melhor: 2,2–3,0%, o único com 88 views pela home).
- Pearl Harbor: 529 → 228 → 61 → 45 → 36 → ~2/dia.
- Por origem, somando todos: **sugerido 3.394 impressões a 1,33%**, busca 646 a 1,86%, navegação 574 a 3,14%. Na busca, o Bikini teve **0,27%** em 367 impressões: perde para os vídeos grandes do mesmo tema.

É o mesmo mecanismo do diagnóstico do Dossier (27/11): **com CTR < 2% no teste do sugerido, a distribuição acaba**. Lá, os 3 vídeos com 0,5–1,6% morreram, e os que passaram de 4% cresceram. No Clearance, **0 de 5 vídeos chegaram a 2,5%**. Na mesma fase (7 primeiros dias), o Dossier teve CTR de 3,0% (CIA), 2,6% (Mossad), 3,8% (FBI), 4,0% (Cosa Nostra), 4,4% (SS), 5,2% (Inquisición) e 3,8% (Gestapo). Ou seja: não é falta de distribuição, porque o YouTube testou todos. **Quem viu a thumb e o título não quis clicar.** O critério da própria PROPOSTA ("< 1 mil impressões = problema de distribuição") vale para 3 dos 5, mas só porque a distribuição foi cortada depois do clique ruim.

### 1.3 Retenção
- % médio visto entre 27% e 40% em vídeos de 15–17 min (4–6,5 min de média). O Dossier fica em 48–66% com 13–14 min.
- A retenção relativa (contra vídeos do mesmo tamanho) na metade do vídeo ficou em 0,15–0,34 em 4 dos 5 (o Pearl Harbor, com 0,84, é ruído: são 6 pessoas). Fica **abaixo da média do YouTube**. Perda forte no começo: só 50–65% da audiência continua a 5–10% do vídeo (no Dossier, 85–87% a 5%).
- **Ressalva:** são 13 a 50 espectadores por vídeo, então a curva tem muito ruído. Mas o padrão é igual nos 5 e vai no mesmo sentido do CTR.

### 1.4 Amostra: 5 vídeos bastam para declarar flop?
- **Pelas views, ainda não:** canal novo costuma passar os primeiros 5–10 vídeos com < 100 views. O hit do Dossier foi o **4º vídeo** (Cosa Nostra), e ele explodiu só no **10º dia** (55 views em 7 d → 1.732 no 11º dia → 48 mil hoje).
- **Pelo sinal que antecede o hit, sim:** a Cosa Nostra tinha **CTR de 3,9–7,9%** em cada pequeno lote de impressões antes de explodir. Todos os primeiros vídeos do Dossier passaram de 2,6%. O Clearance não teve **nenhum** vídeo com esse sinal, e os 5 estão parados há 7–15 dias com < 10 impressões/dia. Nenhum mostra a cauda que a Cosa Nostra mostrava.
- **O critério que nós mesmos escrevemos já foi atingido:** a PROPOSTA (12/11) dizia "PARAR: média < 1,5 mil e nenhum > 5 mil depois do 3º vídeo". Hoje a média é **51 views** e o máximo é **122**.
- **YPP:** o canal tem ~21 h de exibição. Precisa de 4.000 h. Nesse ritmo, não chega.

---

## 2. Mercado (en, últimos 12 meses; yt-dlp via WARP em 28/11)

### 2.1 O subnicho que motivou o canal ("Why can't you visit / What's still at" de guerra americana)
| canal | vídeos lidos | mediana | mediana dos 10 últimos | duração mediana | leitura |
|---|---|---|---|---|---|
| Where They Stood (modelo) | 17 | 30 mil | **18,5 mil** | 23 min | os 4 mais novos: **6,3 mil · 900 · 23 mil · 13 mil**. Iwo Jima (4,8 mi) e Pearl Harbor (325 mil) carregam o canal, e a tendência é de queda |
| Civil War Fine Print (2º modelo) | 6 | 6,7 mil | 6,7 mil | 15 min | 1,4 mi no Lincoln. Depois disso: 604, 1 mil, 4 mil, 9,3 mil, 82 mil. **Foi um hit único** |
| Forgotten Fleet | 30 | 9,9 mil | 16,5 mil | 16 min | navios; mais novos: 1,1 mil, 3,6 mil, 24 mil, 8,9 mil |
| Ship Tales | 30 | 2,5 mil | 9,8 mil | 17 min | navios |
| Hollow Cairn | 17 | **771** | 557 | 31 min | Guerra Civil/cemitérios, formato parecido com o nosso. Exemplo do que acontece quando o formato não engata |
| 21 clones do Iwo Jima (12/11) | — | **28** | — | — | `pesquisa/lugares-guerra/CONCORRENCIA.md` |

Leitura: o subnicho vive de **hits únicos em lugares-ícone** (Iwo Jima, Pearl Harbor, Lincoln). Quem chegou primeiro hoje tem mediana de 1 a 20 mil, em queda. O "sinal de mercado" de 12/11 (WTS 5,2 mi em 40 dias) era, na prática, **1 vídeo**. A PROPOSTA já via esse risco ("hit único").

### 2.2 O nicho largo ("forbidden places / exclusion zones / abandoned military / restricted areas")
A demanda é enorme. Medianas do top-25 das buscas com filtro "este ano": "forbidden places" 931 mil, "abandoned military base" 1,6 mi, "chernobyl exclusion zone" 1,06 mi, "exclusion zone" 234 mil, "off limits island" 74 mil. **Mas quem ganha são 3 formatos que nós não fazemos:**
1. **Criador no local** (o maior pedaço): JeremyXplores (mediana 466 mil, 40–70 min; "I Got Access To Chernobyl's Most Radioactive Room!" 3,4 mi), Drew Binsky, Ruhi Cenet, Brent Rivera ("Surviving the Deadliest Islands that are Forbidden to Visit!" 19,6 mi), Exploring With Josh, KREOSAN. É impossível para a fábrica.
2. **Lista/compilação animada:** The Paint Explainer (mediana 369 mil, ~13 min, estilo pintado; "Most Guarded Places on Earth You Can't Visit" 2,4 mi), Earthyphus ("Every Forbidden Island You're Not Allowed to Visit" 1,0 mi, 7 min), Paintify ("Every Unexplored Place on Earth" 1,6 mi), Placeologist (62 min, 1,5 mi).
3. **Explicador curioso e de tema largo (não só guerra, não só EUA), 11–16 min:** TheDanocracy (mediana 32 mil; "Why Chernobyl Still Can't Be Fixed" 6,2 mi; "Area 51 Was Never Hiding Aliens…" 3,3 mi), Park Vibes (mediana 37 mil; "What's Hidden on Hawaii's Forbidden Island?" 1,3 mi; "What's Hidden In Florida's Radioactive Pyramids?" 193 mil).

**Formato vencedor no faceless:** 11–15 min (não 16–20), uma pergunta de curiosidade larga ("What's hidden…", "Why … still can't…"), visual ilustrado/estilizado ou filmagem de drone/estoque, voz com energia. O nosso formato (foto de arquivo + documento grifado + voz calma, 16 min, só guerra americana) é o mais "de museu" do nicho. O CTR de 1,6% confirma isso.
**Saturação:** alta no topo (criadores e listas). No subnicho de guerra americana, há poucos canais grandes e muitos clones mortos.

### 2.3 RPM
**Hipótese** (sem dado próprio; nenhum canal da fábrica é monetizado e `analytics_receita` está vazia): história/documentário em en, US$ 4–8 (`playbooks/garimpo-tendencias.md`). Público com TV e EUA puxa para cima. Na prática, isso não importa: com 255 views e 21 h, a receita é zero e o YPP está longe.

### 2.4 E o molde Dossier em inglês?
**Não.** O en foi **eliminado pela trava de concorrência** na matriz de 04/11 (`pesquisa/archive-in-minutes/IDIOMA.md`: 91 clones; só os 2 primeiros passam de 5 mil de mediana). O Dossier deu certo em es porque chegou **primeiro em es**. Em en ele seria o 92º clone do **próprio original**: Archive in Minutes (mediana 47 mil; os 10 últimos 26,5 mil, com vídeos novos de 3,5–7,5 mil: até o dono está cansando). Na busca "entire history secret police", o Archive aparece com Gestapo 485 mil e MI6 332 mil, ao lado de Into the Shadows (1,1 mi) e de documentários de TV. Seria disputar com o dono, no idioma dele, um molde que já está cansando.

---

## 3. Opções
| | o quê | prós | contras | custo |
|---|---|---|---|---|
| **(a) Encerrar** | sem vídeo novo; canal fica como está (ou é apagado) | libera noites, Max e atenção para o Dossier e para um canal com evidência | perde a pequena chance de cauda (não há sinal dela) | US$ 0 |
| **(b) Pausar sem custo** (é o estado desde 17/11) | nada é produzido; o canal fica parado | reversível | pausa sem critério vira zumbi: o backlog ainda mostra 6 temas "agendados" (Runit 28/11…), só barrados pelo `noturna.env` | US$ 0 |
| **(c) Adaptar** | mudar para "explicador curioso de lugares restritos", tema largo (nuclear, militar, ilhas, zonas de exclusão no mundo), 11–13 min, visual ilustrado (Codex, US$ 0) + arquivo, títulos "What's Hidden…/Why … Still Can't…" | a demanda do nicho largo é real (Danocracy, Park Vibes, Paint Explainer) | é, na prática, um **canal novo**, contra concorrentes fortes; nosso CTR em en não foi provado em nada; tira capacidade do Dossier | ~US$ 1–2 pagos + ~US$ 15 equivalentes de Claude por vídeo; teste de 4 vídeos ≈ US$ 6 + 4 noites |
| **(d) Manter com metas** | volta à noturna no formato atual | nenhum | 5 de 5 com CTR < 2,5% e o subnicho caindo: mais vídeos iguais repetem o resultado | ~US$ 1 pago + ~US$ 15 equivalentes por vídeo, 4 noites/semana |
| (c') Dossier em inglês | molde Archive em en | — | trava de concorrência (dono + 91 clones) | — |

Temas de exemplo para (c), caso o Tarawa passe (evidência em en):
1. **Runit Dome / Enewetak**: ABC News In-depth "Concrete Dome… Toxic Timebomb" **9,42 mi** (backlog vivo, id 36).
2. **Fort Drum, o "encouraçado de concreto"**: Calum "Fort Drum: America's Unsinkable 'Concrete Battleship'" **4,68 mi** (backlog, id 39).
3. **Area 51 / Tonopah**: TheDanocracy "Area 51 Was Never Hiding Aliens. It Was Hiding Something Worse." **3,32 mi**; EWU Bodycam "What's Behind Area 51's Gates" 1,71 mi (busca 28/11).
4. **Kaho'olawe**: Vox "How Native Hawaiians fought the US Navy, and won" **1,01 mi**; Park Vibes "This Forbidden Hawaiian Island is Quietly Coming Back to Life" 86 mil.
5. **Florida's radioactive "pyramids" (fosfogesso)**: Park Vibes **193 mil** (mediana do canal 37 mil, 5,2×); ou **Diego Garcia** (mediana top-10 "só lugar" **836 mil**, 12 vídeos ≥ 100 mil; `CONCORRENCIA.md` §4).

---

## 4. Recomendação: encerrar o formato Clearance, com 1 último teste grátis (Tarawa)

1. **Nenhuma produção nova no formato atual.** O Clearance sai da noturna de vez, e não "pausado enquanto repensa". Os 6 itens "agendados" do backlog vivo devem ser descartados ou arquivados (decisão do Rodrigo; esta análise não mexeu em nada).
2. **Subir o 005 Tarawa**, que já está pronto e não custa nada, como último dado, com a regra das 48 h do Dossier: se o CTR ficar < 2% nas primeiras ~1.000 impressões, trocar a thumb 1 vez (A/B/C já existem).
3. **Critério (até 14/12/2026, 14 dias depois de publicar):** o Tarawa precisa de **CTR ≥ 3% em ≥ 1.000 impressões** OU **≥ 1.000 views em 14 dias**. 
   - **Passou:** abrir um teste da opção (c) com **4 vídeos** (temas acima, 11–13 min, ilustrado). Meta: **média ≥ 2 mil views em 14 dias ou 1 vídeo ≥ 10 mil, com CTR ≥ 3%**. Sem isso, encerra.
   - **Não passou** (o mais provável, pelos 5 anteriores): **encerra**. O canal fica como casca parada (custo zero; pode ser reaproveitado sem histórico ruim relevante, como já se pensou para o teste do GTA 6) e a vaga do en volta para o `playbooks/novo-canal.md`, a partir de um achado do garimpo com **vantagem de chegar primeiro**. Foi isso que fez o Dossier funcionar. Esse caminho é melhor que salvar um molde que chegou depois do pico.
4. **Por quê:** a capacidade da fábrica é limitada (noites, cota do Max) e o Dossier, que tem CTR de 3,5–4%, rende mais por noite do que qualquer vídeo do Clearance. O dinheiro gasto aqui foi pequeno (US$ 5,74 pagos), então o prejuízo não justifica seguir nem justifica correr para apagar. O que pesa é a falta de sinal: 0 de 5 vídeos no CTR mínimo.

**Limites:** CTR do Studio só existe para o Midway (1 dia). Os dados de impressão vêm da Reporting API (até 26/11), e o Studio pode diferir um pouco. Não sabemos qual variante do "Testar e comparar" ganhou (a Data API devolve só o título A). A retenção tem n de 13 a 50 pessoas por vídeo. As medianas do mercado vêm do top-25/30 das buscas e dos 30 últimos uploads (amostra, não o universo), e as views do yt-dlp em modo flat são arredondadas.
