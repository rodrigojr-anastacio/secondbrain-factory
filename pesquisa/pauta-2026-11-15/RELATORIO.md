# Pauta de domingo 15/11 e segunda 16/11/2026 (4 canais)

Feito em 13/11/2026, ~10h. Só pesquisa: nada foi produzido, gerado nem alterado em `canais/`, `tools/` ou no banco. Custo em dinheiro: US$ 0 (yt-dlp e RSS via WARP, sem cota da API).
Legenda: **[O]** observado (views lidas em 13/11) · **[I, conferir]** fato histórico a confirmar com fonte no roteiro · **Hipótese** = sem dado.
Fontes: `dados/refs-2026-11-13.json` (últimos ~60 vídeos de 25 canais; data = RSS do canal, só os 15 mais recentes têm data), `dados/busca*.json` (busca no YouTube, top 20 por consulta), banco `vida` (`youtube.videos`, `videos_contador`, `studio_ultimo`, `analytics_trafego`), `~/workspace/relatorios/metricas/2026-11-13.md`. Scripts em `scripts/`.

## Resumo
| Canal | Dom 15/11 | Seg 16/11 |
|---|---|---|
| História em minutos | **França** (reserva: Portugal) | **Alemanha** (reserva: Japão) |
| Dossier en Minutos | **Las SS** (reserva: Gestapo) | **La Inquisición** (reserva: Templarios) |
| Em Relevo | **Grande Seca de 1877** (reserva: queimadas) | **Furacão Catarina** (reserva: granizo/temporais no Sul) |
| Clearance Required | **Bikini Atoll** (reserva: Guadalcanal) | **Gettysburg (fotos)** (reserva: Tarawa) |

## Status conferido (13/11 ~09h50; Data API/`videos_contador` e oEmbed)
- historia-ptbr: 6 públicos. **Rússia ainda privada** (agendada para 13/11 10:30; oEmbed 403 às 09:52).
- dossie-es: 5 públicos. **Masones privado** (agendado para 13/11 18:00). Obs.: o `youtube.videos` id 14 (KGB, "pronto", sem ID) é duplicata do id 18 publicado: só registro, não mexi.
- Em Relevo: El Niño (12/11) e Sul (11/11) públicos; no YouTube o El Niño aparece como "El Niño 2026: em março é que..." (teste A/B, título diferente do banco).
- Clearance: Midway público desde 13/11; no ar aparece "What's Still Under the Water at Midway?" (braço B do teste).
- **Sem dado:** impressões/CTR pela Reporting API (ainda não saiu nenhum relatório); só existe o export do Studio de 09/11 (`studio_ultimo`). Em Relevo e Clearance ainda sem Analytics.

---

## 1. História em minutos (`historia-ptbr`, molde History in Minutes)

**Nossos números [O]:** Egito 361 views (920 impressões, CTR 4,0%, 45% visualizado) e Índia 219 (1.273 impr., 3,7%, 42%) são os únicos que andaram; China 65 (19,6% de retenção), Brasil 39, Irã 16, Roma 2 (2 dias). Tráfego: 43% sugeridos, e quem mais nos sugere é um vídeo de clone pt com o **mesmo tema** ("A HISTÓRIA INTEIRA do Brasil em 13 minutos", History Easy Guide: 146 views para nós).
**Aprendizado que mudou a escolha:** nossas views vêm de vídeo sugerido ao lado de um vídeo com o mesmo tema que já roda, e só os temas com hit grande na referência (Egito, Índia) trouxeram impressões. Por isso entram **França** (clone pt com 184 mil agora) e **Alemanha** (Genius com 256 mil agora), e Japão/Coreia caem (os lançamentos novos da HiM com eles estão fracos).

### Dom 15/11: **França** (recomendação)
- **Por que agora [O]:** clone pt "História em minutos" (5,5 mil insc.) "Toda a história da França em 38 minutos" = **184 mil** (publicado 23/10, 21 dias), o maior vídeo do canal; o resto do canal faz 0,6–4 mil. Busca "história da frança" mediana top-10 853 mil (puxada pela Revolução Francesa). No molde curto em pt, ninguém tem a França (clones: Revolução Francesa 6 views). Risco de anúncio baixo.
- **Hook:** Soissons, 486: um soldado de Clóvis quebra um vaso da Igreja; um ano depois, o rei racha a cabeça dele com o machado na frente da tropa. É assim que começa o país que vai cortar a cabeça do próprio rei 1.300 anos depois ("guarde isso"). [I, conferir: Gregório de Tours, II.27]
- **3 títulos:**
  - A (fórmula/completude): "A história INTEIRA da França em N minutos" (padrão 1, "The ENTIRE History of [país] in N Minutes": Egito 563 mil, HiM)
  - B (contraste de destinos): "Por que a França se uniu e a Alemanha ficou dividida por 1.000 anos?" (padrão "Why Did Russia Unite While Europe Stayed Divided?", Ziro 41 mil; costura com o vídeo de segunda)
  - C (lacuna/"nunca morreu"): "A Gália nunca morreu. Só mudou de nome." (padrão "Persia Never Died. It Just Changed Its Name.", HiM 91 mil)

**Reserva: Portugal**
- **Por que [O]:** busca "história de portugal" mediana top-10 360 mil; sessão natural com o Brasil (005). Mas o nosso Brasil fez 39 views: a sessão não ajuda ainda.
- **Hook:** novembro de 1807: a corte inteira, cerca de 10 mil pessoas, embarca às pressas no Tejo com Junot a um dia de Lisboa; é a única vez que um império europeu muda a capital para a colônia. [I, conferir]
- **Títulos:** A "A história INTEIRA de Portugal em N minutos" (padrão 1) · B "Como o mar decidiu o destino de Portugal por 800 anos" (padrão "How Water Decided Who Ruled China for 4,000 Years", HiM 57 mil) · C "Portugal: o país pequeno que dividiu o mundo ao meio" (padrão "Russia: The Biggest Country That Never Had Enough People", HiM 43 mil)

### Seg 16/11: **Alemanha** (recomendação)
- **Por que agora [O]:** Genius History "The ENTIRE History of Germany in 21 Minutes" = **256 mil** (26/10, 18 dias), o melhor do canal no último mês (Itália 29 mil, Suíça 32 mil, Dinamarca 25 mil no mesmo período). Busca pt "história da alemanha" mediana top-10 1,23 mi; no molde pt só "História do Mundo em HQ" 127 mil (03/2026). Risco médio (nazismo): tratar 1933–45 como 1 era entre várias, sem símbolos na thumb.
- **Hook:** 18/01/1871: a Alemanha nasce **dentro da França**, no Salão dos Espelhos de Versalhes, proclamada por um rei prussiano no palácio do inimigo. Por que um país precisou nascer na casa do vizinho? [I, conferir]
- **3 títulos:**
  - A: "A história INTEIRA da Alemanha em N minutos" (padrão 1; Genius 256 mil)
  - B (pergunta central): "Por que a Alemanha levou 1.000 anos para virar um país?" (padrão "Why Did [A] Unite While [B] Stayed Divided?", Ziro 41 mil)
  - C (superlativo + falta): "Alemanha: a maior potência da Europa que nunca teve fronteira fixa" (padrão "Russia: The Biggest Country That Never Had Enough People", HiM 43 mil)

**Reserva: Japão**
- **Por que [O]:** busca mediana 258 mil; Genius 869 mil (antigo) e CountryCorns 115 mil (01/10). **Contra:** a HiM acabou de lançar "The ENTIRE History of Japan" (09/11) com só 2,2 mil em 4 dias, e o clone pt fez 2,2 mil. Liga com a China (004).
- **Hook:** 1281: a maior frota de invasão do mundo até então, a de Kublai Khan, some numa noite de tufão; o Japão chama o vento de *kamikaze* e acredita por 600 anos que é intocável. [I, conferir]
- **Títulos:** A "A história INTEIRA do Japão em N minutos" (1) · B "Por que o Japão virou potência e a China não?" (padrão "Why South Korea Became Rich While North Korea Stayed Poor", Ziro 185 mil) · C "O país que se trancou por 200 anos (e saiu potência)" (Hipótese: padrão "X Never Died…"/lacuna; sem par exato na tabela)

---

## 2. Dossier en Minutos (`dossie-es`, molde Archive in Minutes)

**Nossos números [O]:** Mossad 356 views (5.521 impressões, CTR 2,3%, 48% visualizado, Studio 09/11), CIA 129 (633 impr.), FBI 89, KGB 33 (2 dias), Cosa Nostra 15. Tráfego: **69% sugeridos**; busca só "mossad" (26).
**Aprendizado que mudou a escolha:** o Mossad teve 9× as impressões da CIA porque saiu quando o Atlas del Tiempo tinha o Mossad bombando (84 mil); Cosa Nostra (tema difuso) parou em 15. Escolher o tema que **os vizinhos estão rodando agora**: hoje são as organizações nazistas, que a bíblia segurava "até ~5 vídeos no ar" (já temos 6).

### Dom 15/11: **Las SS** (recomendação)
- **Por que agora [O]:** Archive in Minutes "The ENTIRE History of the SS in 16 Minutes" = **667 mil** (RSS 29/10, 15 dias), o maior do molde; Te lo Pinto "The COMPLETE History of the SS" 47 mil em 2 dias (11/11); Atlas "SS | Hitler's Black Guard" 4,1 mil. Busca es "historia de las SS" mediana top-10 **816 mil** (SLICE 2,9 mi; Der Kommandant 2,3 mi). Ninguém em es no molde curto.
- **Cuidados (bíblia):** sem runas nem suástica na thumb e nas imagens; tom de vítimas e julgamento (fecha em Nuremberg).
- **Hook:** 1929: Himmler, um ex-granjeiro de galinhas, herda uma guarda de ~280 homens; 15 anos depois ela tem quase um milhão e manda nos campos. Expediente 1: o granjeiro. [I, conferir]
- **3 títulos:**
  - A (fórmula): "TODA la historia de las SS en N minutos" (padrão 1: Archive SS 667 mil)
  - B (por dentro): "Cómo funcionaban las SS por dentro" (padrão "How the KGB Works From the Inside", Te lo Pinto 238 mil; o mesmo canal fez "Así Funcionaba por Dentro la Policía Nazi" 187 mil em 9 dias)
  - C (apelido sinistro): "La Orden Negra: el ejército más temido de Hitler" (padrão "[Apelido]: History's Deadliest…", Te lo Pinto 2,9 mi; subtítulo do Atlas "Hitler's Black Guard")

**Reserva: la Gestapo**
- **Por que [O]:** Te lo Pinto (es) "Así Funcionaba por Dentro la Policía Nazi del Tercer Reich" **187 mil** (04/11, 9 dias); Archive Gestapo 444 mil; busca es mediana 181 mil (menor que SS). Atlas Gestapo 12 mil.
- **Hook:** a polícia mais temida da Europa tinha poucos agentes por cidade; quem fazia o trabalho eram as cartas de denúncia dos vizinhos (estudo de Würzburg, Gellately). [I, conferir]
- **Títulos:** A "TODA la historia de la Gestapo en N minutos" (1) · B "Cómo funcionaba la Gestapo por dentro" (4) · C "TODA la historia de la Gestapo | La policía secreta más temida de Hitler" (subtítulo de superlativo do Atlas, "Mossad… | The World's Most Feared Secret Service" 84 mil)
- Se a SS for no domingo, a Gestapo fica para a outra semana (dois nazistas seguidos aumentam o risco de anúncio limitado: Hipótese).

### Seg 16/11: **La Inquisición** (recomendação)
- **Por que [O]:** é o tema com o **melhor histórico no molde exato em es**: Academia Play "La inquisición en 15 minutos" **4,7 mi** (2018); busca es mediana top-10 386 mil (2,2 mi e 1,9 mi entre os top). Ninguém fez no molde em 2026 (Archive/Atlas não têm). Ângulo América Latina forte: tribunais de Lima (1570), México (1571) e Cartagena (1610). Risco baixo–médio (religião). Muda de cluster depois da SS. **Contra:** é Hipótese que puxe sugeridos (nenhum vizinho rodando o tema agora).
- **Hook:** 11/04/1649, Cidade do México: o maior auto de fé da América, com 109 réus e uma multidão nas praças; a Inquisição tinha chegado ao Novo Mundo 78 anos antes. [I, conferir números]
- **3 títulos:**
  - A: "TODA la historia de la Inquisición en N minutos" (padrão 1; Academia Play 4,7 mi com "en 15 minutos")
  - B (hierarquia por dentro): "Tu vida en cada rango de la Inquisición" (padrão "Your Life in Every Rank of Templar Knight", Te lo Pinto 2,2 mi: familiar, notario, calificador, inquisidor)
  - C (lado escondido): "El lado oculto de la Inquisición en América" (padrão "The Hidden Side of the CIA", Classé Secret Défense 55 mil)

**Reserva: los Templarios**
- **Por que [O]:** busca es mediana 372 mil; Memorias de Pez "en 10 minutos" 1,35 mi (2021); Te lo Pinto "Tu vida en cada rango de caballero templario" 2,2 mi. Recente > 100 mil: só 1. Fica melhor depois do resultado dos Masones (publica hoje 18:00): se o cluster "sociedades" trouxer impressões, sobe.
- **Hook:** sexta-feira, 13/10/1307, ao amanhecer: os agentes do rei da França abrem ordens seladas e prendem todos os templários do reino no mesmo dia. [I, conferir]
- **Títulos:** A "TODA la historia de los Templarios en N minutos" (1) · B "Tu vida en cada rango de los Templarios" (2) · C "Cómo funcionaban los Templarios por dentro" (4)

---

## 3. Em Relevo (`em-relevo`, clima/geografia em mapa 3D, pt)

**Nossos números [O]:** Sul (11/11) 15 views; El Niño (12/11) 6 views; sem Analytics ainda. Canal anterior (@emrelevobr) tinha 0 impressão de Início/Sugeridos, só busca (memória de 11/11); o @canalemrelevo é de 11/11.
**Aprendizado que mudou a escolha:** canal novo sem navegação vive de **busca perene**: troquei o tema quente de notícia (queimadas, Rio Negro) por temas com busca que não cai e com hit provado. E os dois títulos no ar são sim/não ou vagos (fora da tabela da bíblia): os 3 títulos abaixo nomeiam uma anomalia e não dão a resposta.
**Série do g1 (JH) sobre El Niño [O]:** "JH: série especial explica o fenômeno El Niño" 827 mil; Fantástico "El Niño é o culpado pelas tempestades e vendavais?" 630 mil; Previsão "El Niño bate recorde" 378 mil. Não achei os episódios separados pela busca (a lista do g1 não veio no top 20): ângulo que puxa é "culpado pelas tempestades" e "recorde". Uso abaixo.

### Dom 15/11: **A Grande Seca de 1877, reconstruída no mapa** (recomendação)
- **Por que agora [O]:** continuação natural do vídeo 2 (o El Niño de 2026 é comparado ao de 1877–78). Terra em Choque "El Niño de 1877 Está Voltando? A Seca Que Devastou Brasil, Índia e China" **569 mil**; Canal Nostalgia "O dia em que o Brasil secou" 1,67 mi; BBC News Brasil "A tragédia esquecida que dizimou brasileiros…" 226 mil (e o vídeo da BBC sobre o El Niño de 1877 tinha 932 mil em 8 dias em 09/11, memória). Busca "grande seca 1877" é baixa (mediana 10 mil): o tema vive de título/thumb, mas é perene e casa com o pico do El Niño (dez–jan).
- **Hook:** 1878: Fortaleza, uma cidade de ~25 mil pessoas, recebe mais de 100 mil retirantes em poucos meses; no mapa, o sertão inteiro anda para o litoral. [I, conferir]
- **3 títulos:**
  - A (esquecido): "Por que quase ninguém fala da seca que matou 500 mil brasileiros?" (padrões "Why is the coast of Piauí so FORGOTTEN?", Mundo Entrópico 2,3 mi, e "Why Nobody Talks About the Ozone Hole Anymore", Astrum 1,6 mi) [número a conferir]
  - B (mudou tudo): "A seca que mudou o mapa do Brasil" (padrão "The Tornado That Changed Science", Astrum 4,9 mi)
  - C (evento explicado + medo atual): "O El Niño de 1877 vai se repetir em 2026?" (padrão Terra em Choque "El Niño de 1877 Está Voltando?", 569 mil; perda/medo)

**Reserva: queimadas (ideia do Rodrigo)**
- **Por que [O]:** pico de notícia em outubro: CNN "Manaus pede socorro após fumaça…" 403 mil; Jovem Pan 118 mil; Band "Rio Negro tem pior seca da história". Mas a busca no YouTube é baixa (mediana 17–42 mil) e o pico passou; com o canal só em busca, é aposta pior agora. **Hipótese:** volta forte se houver nova onda de fumaça no Sudeste.
- **Hook:** em outubro, o ar de Manaus ficou entre os piores do planeta por dias, e o fogo começou a 300 km da cidade. [I, conferir]
- **Títulos:** A "Por que a fumaça da Amazônia chega na sua cidade?" (padrão 1, por que + lugar) · B "O fogo que não devia existir na floresta mais úmida do mundo" (padrão "Shouldn't Exist", Astrum 4,1 mi) · C "Queimadas 2026 explicadas: o mapa do fogo mês a mês" (padrão "[Evento 2026] Explained", The Last Day 5,2 mi)

### Seg 16/11: **Furacão Catarina (2004)** (recomendação)
- **Por que [O]:** pergunta perene com busca alta: Manual do Mundo "Por que não tem furacão no Brasil?" **2,58 mi**; Climatempo "Aquilo era um furacão: Catarina 10 anos" 581 mil; busca mediana top-10 235 mil. Perfeito para o mapa 3D (imagem de satélite NOAA de domínio público). Casa com o vídeo 1 (Sul) e com o "culpado pelas tempestades" do Fantástico. Não depende de notícia.
- **Hook:** 28/03/2004: os meteorologistas brasileiros diziam "ciclone extratropical", os americanos viam um olho perfeito no satélite; o Atlântico Sul não tinha furacão, até aquela noite. [I, conferir]
- **3 títulos:**
  - A (anomalia): "O furacão que não devia existir no Brasil" (padrão "The Tornado That Shouldn't Exist", SkyWhisper 1,1 mi)
  - B (pergunta): "Por que o Brasil (quase) nunca tem furacão?" (padrão "Why is there NO bridge between AMAPÁ…", Mundo Entrópico 433 mil; Manual do Mundo 2,58 mi)
  - C (lacuna/medo): "E se o Catarina voltar com o El Niño?" (padrão "What would happen if…", The Last Day 2,0 mi)

**Reserva: granizo e temporais no Sul (temporada nov–dez)**
- **Por que [O]:** notícia constante agora: Adriel Tavares "madrugada turbulenta no Sul: tornado, granizo e chuva" 487 mil; UOL granizo no RS 318 mil; busca mediana 118 mil. Risco: repete o vídeo 1 (Sul).
- **Hook:** pedras de granizo do tamanho de laranjas furam telhados no RS, e o motivo está a 3 mil km, nos Andes. [I, conferir]
- **Títulos:** A "Por que o Sul do Brasil tem o granizo mais violento do país?" (1) · B "As tempestades que não deviam existir no Sul" (3) · C "O que o El Niño vai fazer com o Sul até março" (promessa com prazo, regra do Rodrigo 12/11)

---

## 4. Clearance Required (`lugares-guerra-en`, molde Where They Stood / Civil War Fine Print)

**Nossos números [O]:** Midway, 7 views em poucas horas (13/11); sem Analytics. Não há dado nosso para decidir.
**Aprendizado (das referências, não nosso):** nas últimas 4 semanas do WTS, "still/digging" (Normandy 127 mil) e lugar ícone ganham; "Can't" com lugar obscuro fica em 5–32 mil (Cheyenne 4,9 mil, Rocket Mountain 32 mil). E o 2º molde (documento) está quente: CWFP "The Pictures of Lincoln's Death You Weren't Supposed to See" passou de 882 mil (12/11) para **1,0 mi** em 13/11, num canal de 3,7 mil inscritos. Por isso Gettysburg (documento) entra já na segunda.
**Regra:** só material público (NARA, NHHC, LoC, DVIDS, NPS, DOE), sem 3D.

### Dom 15/11: **Bikini Atoll** (recomendação; backlog #2)
- **Por que [O]:** busca "bikini atoll" mediana top-10 **888 mil** (VICE 3,66 mi; Vivid History 1946 Report 2,2 mi; OceanX 1,36 mi); só lugar 207 mil (backlog). Nenhum dono do ângulo "lugar hoje/por que não pode ir". Material nota 4,5 (filmes oficiais da Operação Crossroads, PD; relatório do JCS). Tema nuclear alterna com o Pacífico do Midway.
- **Hook:** março de 1946: um comodoro da Marinha pede a 167 moradores que deixem a ilha "pelo bem da humanidade"; 80 anos depois, eles ainda não voltaram. [I, conferir]
- **3 títulos:**
  - A: "Why Can't You Visit Bikini Atoll?" (padrão "Why Can't You Visit X?", Iwo Jima 4,5 mi)
  - B: "What's Still Under the Water at Bikini Atoll?" (padrão "What's Still Under the Water at Omaha Beach?", 344 mil)
  - C: "Why Is There an Aircraft Carrier at the Bottom of Bikini?" (padrão "Why Is There a Japanese Submarine in Alaska?", 32 mil; USS Saratoga afundado em 1946 [I, conferir])

**Reserva: Guadalcanal (backlog #5)**
- **Por que [O]:** aniversário da Batalha Naval de Guadalcanal (12–15/11/1942); busca mediana 254 mil ("Ghostly Remains of Guadalcanal" 723 mil); só lugar 283 mil; 0 título why/still (vaga). Material nota 5.
- **Hook:** o aeroporto onde você pousa em Honiara é a pista pela qual 60 mil homens morreram; a baía ao lado tem tantos navios no fundo que ganhou o nome de Iron Bottom Sound. [I, conferir]
- **Títulos:** A "What's Still Buried on Guadalcanal?" (B do molde) · B "Why Is Guadalcanal Still Full of Unexploded Bombs?" (padrão "Why Is Laos Still Full of American Bombs?" — atenção: esse fez só 1,6 mil) · C "Why Is There a Fleet at the Bottom of Iron Bottom Sound?" (padrão "Why Is There a [coisa] in [lugar]?")

### Seg 16/11: **Gettysburg: as fotos** (recomendação; backlog #3, molde documento)
- **Por que agora [O]:** CWFP Lincoln **1,0 mi** em 6 dias com o molde "You Weren't Supposed to See"; busca "gettysburg" mediana 171 mil (American Battlefield Trust 5,2 mi); "fotos da Guerra Civil" 1,2–2,2 mi (Unhinged Past, The Secret). Aniversário do Discurso de Gettysburg em **19/11** (quinta): publicar na segunda pega a semana. Fotos de Gardner/O'Sullivan (1863) são PD na LoC.
- **Hook:** julho de 1863: Alexander Gardner arrasta um soldado confederado morto por ~40 jardas até uma rocha para uma foto melhor; levou 112 anos para alguém perceber (Frassanito, 1975). [I, conferir]
- **3 títulos:**
  - A: "The Gettysburg Photos You Weren't Supposed to See" (padrão "The Pictures of Lincoln's Death You Weren't Supposed to See", 1,0 mi)
  - B: "Why Is the Same Dead Soldier in Two Gettysburg Photos?" (padrão "Why Is There a [coisa estranha] in [lugar]?", 32 mil)
  - C: "What Happened to the Real 'Harvest of Death'?" (padrão "What Happened To The Real Hacksaw Ridge?", 94 mil)
- Cuidado: o "weren't supposed to see" tem de ser pago no vídeo (foto encenada, corpo movido, foto que o público de 1863 não viu): conferir na pesquisa.

**Reserva: Tarawa (fora do backlog; Hipótese de material)**
- **Por que [O]:** aniversário da batalha 20–23/11/1943; WUSA9 "Missing WWII heroes found buried under a parking lot in Tarawa" **462 mil**; HISTORY 641 mil; Real Time History 593 mil; busca mediana 55 mil. Padrão do WTS "Why Is America Still Digging Up Normandy?" 127 mil (mas "…Germany?" 8 mil). Material **não avaliado** (indício: filme "With the Marines at Tarawa", 1944, do governo dos EUA; escavações da DPAA no DVIDS): avaliar a nota antes de produzir.
- **Hook:** em 2019, sob um estacionamento em Betio, uma equipe achou 22 fuzileiros enterrados desde 1943. [I, conferir]
- **Títulos:** A "Why Is America Still Digging Up Tarawa?" (padrão Normandy 127 mil) · B "What's Still Buried Under Tarawa?" (What's Still Under) · C "The Tarawa Film You Weren't Supposed to See" (documento; só se a pesquisa achar o corte censurado [I, conferir])

---

## Limitações
- Views lidas uma vez (13/11, manhã); o yt-dlp devolve títulos traduzidos automaticamente para o inglês em alguns canais (Mundo Entrópico, Atlas, Te lo Pinto, os nossos): confira o original antes de copiar um título.
- Data de publicação só para os ~15 vídeos mais recentes de cada canal (RSS). O "29/10" da SS do Archive vem do RSS; o canal começou em 14/10.
- Alguns vídeos aparecem com 0 views na lista (Genius: Japão, China, EUA; Chão do Sul; HiM Israel): **sem dado**, não zero de verdade.
- Busca no YouTube via WARP é amostra (top 20), não o universo. Impressões/CTR atuais: **sem dado** (Reporting API ainda vazia).
- Prazo: os 8 vídeos precisam ser produzidos até dom/seg; a Inquisição, Gettysburg (molde documento) e Tarawa (material não avaliado) são os que pedem mais pesquisa.
