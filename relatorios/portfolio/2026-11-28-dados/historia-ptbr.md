# historia-ptbr ("História em minutos"): continuar, encerrar ou adaptar? (28/11/2026)

Só análise. Nada foi mudado no canal, backlog, bíblia, banco, fila ou timers. Custo pago: US$ 0 (yt-dlp via WARP e algumas unidades da Data API para enriquecer 38 vídeos).
**Fontes:** `youtube.analytics_video_dia` e `analytics_trafego` (Analytics API, dados até 25/11), `youtube.alcance_diario` (impressões e CTR pela Reporting API, até 26/11), `youtube.studio_video` (exports de 09, 14 e 20/11), `youtube.metricas_video` (snapshot de 28/11), `analytics_retencao`, `financas.consumo`, `youtube.reembalagem`. Mercado: yt-dlp via WARP (listas de 11 canais e 32 buscas "este ano por views") e `videos.list`/`channels.list`. Brutos em `brutos-historia/`.
**Limites:** a Data API devolve só o título A do "Testar e comparar", e o CTR é o agregado das variantes. Vídeos de 21–25/11 têm poucos dias de dados. Os títulos que aparecem pelo WARP vêm traduzidos para o inglês: usei os títulos em pt do banco e da `reembalagem`. A coluna `youtube.videos.publicado_em` está desatualizada (vários vídeos no ar estão sem data), então usei o 1º dia com views.

---

## 0. Resposta curta
- **Os números:** 15 vídeos no ar em 26 dias, **2.088 views, 21 inscritos e 128 h assistidas**. O canal gastou **US$ 126,77 (R$ 729)** em geração, ou **US$ 0,061 por view e US$ 6,04 por inscrito**. O dossie-es gastou R$ 798 e tem 78.248 views: **35× mais eficiente por view**. O lotr-fr gastou R$ 3 e tem 28 mil views.
- **Diagnóstico:** o canal **não passa no teste de lançamento**. Desde o 11, o YouTube mostra cada vídeo novo a 400–2.500 pessoas nas primeiras 48 h. Os títulos-pergunta da v2 tiveram **CTR de 0,2–2,3%** nesse teste, e a distribuição para no dia seguinte. É o mesmo portão de ~2% que o diagnóstico do dossie-es achou. Os títulos-fórmula da v1 ("A história INTEIRA de X") ficaram em 4–5,8% em 7 dias, mas receberam pouca impressão. A retenção também é fraca: a 5% do vídeo, 55–70% da audiência continua (dossie-es: 81%); na metade, 22–43% (dossie-es: 57%).
- **Mercado:** em pt, o molde "história inteira de país" é **loteria de um hit por canal**. O clone homônimo "História em minutos" (6 mil inscritos) fez Rússia 275 mil e França 206 mil; os outros 9 vídeos ficaram abaixo de 26 mil, e ele já mudou para atualidade. A Crônicas de Ferro fez Irã 1,54 mi, depois Etiópia 8 mil e "Irã proibido" 5 mil, e mudou para "vida medieval". Três clones de 10/2026 estão mortos (2–1.760 views). Até o canal-modelo em inglês (History in Minutes, 24 mil inscritos) caiu para 2–3 mil views nos uploads de novembro.
- **Recomendação:** **parar a série de países hoje** (sai da noturna) e **adaptar** o canal com um teste curto e com prazo: "como era viver / você não sobreviveria", com bonequinhos e o Brasil no centro. São **4 vídeos, 1 por semana**. Se até **10/01/2027** nenhum fizer ≥ 3.000 views em 7 d com CTR ≥ 4% no lançamento, **encerra** (o canal fica no ar, sem produção).

---

## 1. Diagnóstico

### 1.1 Vídeo a vídeo
Views em 48 h e em 7 d pela Analytics API (desde o 1º dia com views). O total é o snapshot de 28/11. "% visto" é a média ponderada. CTR 48 h e CTR 7 d vêm da Reporting API (impressões entre parênteses); "CTR Studio" é o último export (só até 20/11). Na Analytics API, "Navegação" aparece como `SUBSCRIBER` (início e feed de inscrições).

| nº | título (pt; atual quando foi reembalado) | v | 1º dia | 48 h | 7 d | total | insc. | % visto (duração média) | CTR 48 h (imp.) | CTR 7 d (imp.) | CTR Studio | fonte dominante | custo US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 001 | Persas, romanos, árabes: por que o Egito NUNCA sumiu? (antes: "A história INTEIRA do Egito em 17 minutos") | v1 | 03/11 | 29 | 191 | **569** | 6 | 40,2% (6:50) | 1,7% (353) | **5,8%** (1.243) | 5,58% | Navegação 55%, Sugerido 39% | 10,33 |
| 002 | 5.000 ANOS de Índia em 19 minutos | v1 | 03/11 | 28 | 163 | **297** | 3 | 40,9% (7:57) | 1,8% (667) | 4,2% (1.523) | 3,99% | Sugerido 57%, Navegação 37% | 9,90 |
| 003 | Por que a Pérsia virou Irã e NUNCA virou árabe? | v1 | 07/11 | 7 | 23 | 42 | 1 | 38,3% (6:54) | 0% (24) | 4,5% (134) | 4,88% | Sugerido | 23,78 |
| 004 | 3.000 ANOS de China em 16 minutos | v1 | 08/11 | 7 | **318** | **437** | 4 | 36,4% (5:54) | 7,7% (39) | 4,9% (1.774) | 4,09% | Navegação 67% | 11,00 |
| 005 | O país que ganhou nome de MERCADORIA (Brasil) | v1 | 09/11 | 26 | 82 | 127 | 4 | 42,0% (7:17) | 5,1% (117) | 3,8% (607) | 3,60% | Sugerido 56% | 11,44 |
| 006 | Roma pagou resgate aos bárbaros. Como virou dona do mundo? | v2 | 12/11 | 1 | 3 | **3** | 0 | (só o dono) | 3,3% (30) | 1,4% (74) | 1,33% | — (**nunca foi testado**) | 9,48 |
| 007 | Chamaram um VIKING para reinar. Como a Rússia ficou gigante? | v2 | 13/11 | 19 | 39 | 103 | 1 | 32,6% (5:28) | 9,6% (94) | **7,4%** (229) | 7,49% | Sugerido 58% | 10,14 |
| 008 | A história INTEIRA da França em 15 minutos | v2 | 15/11 | 12 | 22 | 29 | 1 | 43,9% (6:42) | 2,5% (79) | 2,1% (190) | 2,63% | misto | 9,23 |
| 009 | A história INTEIRA da Alemanha em 17 minutos | v2 | 16/11 | 19 | 39 | 65 | 0 | 33,5% (5:49) | 2,9% (138) | 3,5% (286) | 3,36% | Navegação 58% | 11,76 |
| 010 | O Japão COPIAVA todo mundo. Por que ninguém o conquistava? | v2 | 18/11 | 1 | 12 | 18 | 0 | 13,4% (2:04) | 0% (15) | 2,7% (74) | — | — | 1,15 |
| 011 | Os EUA prometeram o que NÃO cumpriam. Como viraram potência? | v2 | 20/11 | 12 | 13 | 13 | 0 | 25,5% (4:01) | **0,6%** (653) | 0,7% (692) | — | Sugerido | 2,85 |
| 012 | A fronteira de Portugal é QUASE a mesma desde 1297. Como? | v2 | 21/11 | **147** | 203 | **209** | 0 | 26,6% (4:22) | 2,3% (**1.999**) | 2,35% (2.256) | — | Navegação 65% | 0,71 |
| 013 | A URSS chegou ao ESPAÇO. Por que faltava comida? | v2 | 23/11 | 4 | 4 | **4** | 0 | 5,8% | **0,2%** (428) | 0,2% (444) | — | — | 1,26 |
| 014 | A Inglaterra IMPORTAVA reis. Como mandou em 1/4 do mundo? | v2 | 25/11 | 64 (1 d) | — | 167 | 0 | 33,2% (5:36) | **1,3%** (**2.488**) | — | — | Navegação | 1,39 |
| 016 | A Espanha juntou meio mundo. Por que não juntava a si mesma? | v2 | ~27/11 | — | — | 5 | — | — | — | — | — | — | 0,53 |
| 017 | Cuba adoçava o MUNDO. Por que dependia de um país só? | v2 | privado | — | — | 0 | — | — | — | — | — | — | 4,73 |
| 015 | A Argentina já foi RICA. Por que apagou 13 zeros da moeda? | v2 | não subiu | — | — | — | — | — | — | — | — | — | 7,11 |

Retenção pela curva da Analytics (`audiencia_ratio`, última leitura em 28/11): a 5% do vídeo, Irã 69,7, Egito 67,8, Inglaterra 65,4, Índia 64,7, Portugal 64,0, Brasil/Alemanha 61,5, China 59,9, Rússia 57,1 e França 54,6. Na metade do vídeo: 22–43% (Portugal, o pior, com 21,8%). No **dossie-es**, a média é **80,7% a 5% e 57,3% na metade**.

### 1.2 v1 × v2
| | v1 (001–005) | v2 (006–017) |
|---|---|---|
| vídeos no ar com ≥ 7 d | 5 | 6 (006–011) |
| views em 7 d (mediana) | **163** | **17** |
| total (mediana) | **297** | 24 (006–011) |
| CTR 7 d (mediana) | **4,5%** | 2,4% (os títulos-pergunta de 011/013/014 ficaram em 0,2–1,3%) |
| % visto (média) | 39,6% | 25–44% (Japão 13%, URSS 6%) |
| custo médio | US$ 13,29 (fal + OpenAI) | US$ 1,0–2,9 desde o 010 (Codex) |

**A v2 rendeu pior em views, CTR e retenção.** O roteiro v2 não melhorou o % visto: França teve 43,9%, mas Rússia 32,6% e Alemanha 33,5%. O tema pesa mais, mas a diferença maior está na embalagem.

### 1.3 O que separa os que andaram dos que morreram
1. **O título decide o teste das 48 h, e o título-pergunta provocativo perde.** Os títulos-fórmula e os de "N ANOS de X" (Egito, Índia, China) chegaram a 4–5,8% de CTR. Os títulos-pergunta com "promessa negativa" ("prometeram o que NÃO cumpriam", "por que faltava comida", "importava reis") ficaram em **0,2–1,3% sobre 430–2.500 impressões**. A distribuição parou no 2º dia, mesmo padrão de Medellín, Núremberg e Yakuza no dossie-es. A exceção é a Rússia ("Chamaram um VIKING…", 7,4%): nome concreto e cena, sem acusação. **Leitura:** pergunta com fato concreto e positivo funciona; pergunta com paradoxo abstrato ou crítica a um país não funciona.
2. **Tema: civilização antiga e grande > país europeu moderno.** Egito, China e Índia têm a maior demanda pt e en (History in Minutes en: Egito 636 mil, Índia 660 mil; Genius: Irã 1,0 mi). França, Alemanha, EUA, URSS e Japão são temas com dono (Genius) e sem sessão com o que já temos.
3. **Ninguém mostrou Roma.** Foram 74 impressões em 7 dias, e o vídeo saiu 1 dia antes da Rússia. Ele não morreu pela embalagem: o YouTube nem testou. Lançar dois vídeos colados divide o teste.
4. **Duração:** todos têm 15–19 min, então a duração não explica a diferença. **Data:** os 3 que "andaram" são da 1ª semana e cresceram devagar (Egito 29 → 191 views entre 48 h e 7 d; China 7 → 318) pela navegação de um canal novo. Nos vídeos de novembro, o YouTube testa mais (2 mil impressões) e corta mais rápido.
5. **O canal não converte inscrito:** 21 em 2.088 views (1%). Do 008 em diante, quase todos os vídeos ficaram com 0–1 inscrito. Não há vínculo com o espectador.

### 1.4 Dinheiro × resultado
| | historia-ptbr | dossie-es | lotr-fr |
|---|---|---|---|
| gasto em geração (R$) | **729** | 798 | 3 |
| views | 2.088 | 78.248 | 28.435 |
| inscritos | 21 | 285 | 291 |
| R$ por view | **0,35** | 0,010 | 0,0001 |
| R$ por inscrito | **34,7** | 2,8 | 0,01 |

- Gasto por fornecedor (historia-ptbr): fal R$ 534, OpenAI R$ 112, Gemini R$ 38, Runpod R$ 25, Fish R$ 20. Desde o 010 (Codex), o custo direto caiu para **~US$ 1–3 por vídeo**. O Argentina custou US$ 7 por causa do fallback pago.
- **O custo que mais pesa agora não é o dinheiro.** É a **cota do Claude Max** (etapa 1 em Opus para cada vídeo), a **janela do Codex** (o História espera o Dossier todas as noites) e o **tempo do Rodrigo** para subir 4 vídeos por semana. Os três são compartilhados com o dossie-es, que rende 35× mais.
- **Monetização:** o YPP pede 1.000 inscritos e 4.000 h em 12 meses. O canal tem **21 inscritos e 128 h**. No ritmo atual (~0,8 inscrito/dia), seriam ~3 anos.

---

## 2. Mercado

### 2.1 pt-BR, molde "história inteira de país/império"
| canal | criado / inscritos | vídeos do molde (views) | leitura |
|---|---|---|---|
| **História em minutos** (homônimo, UCuquAW2…) | 08/2026 · 6.070 | **Rússia 275 mil**, **França 206 mil**, Ucrânia 26 mil, Índia 5,7 mil, Egito 3 mil, Japão 2,9 mil, Austrália 2,9 mil, Amazon 809 | 2 hits em 13 vídeos; depois mudou para atualidade BR (Maduro 946, furacão 784) |
| **Crônicas de Ferro** | 03/2026 · 32,5 mil | **Irã 1,54 mi** (03/2026); Etiópia 8,4 mil; "Irã país proibido" 5,1 mil | 1 hit; mudou para "vida medieval / você não sobreviveria" (209 mil, 197 mil, 65 mil, 52 mil) |
| História em Minutos (clones 10/2026 a/b/c) | 10/2026 · 0–17 | 2 a 1.760 views | mortos |
| Histórias Milenares | 2023 · 70,5 mil | "EGITO ANTIGO: A História Completa em 20 Minutos" 442 mil (05/2026) | canal médio, tema top |
| Era Humana | — | documentários longos (Civilizações Antigas 528 mil, Mitologia Grega 658 mil, Grécia 90 mil) | outro formato (2–3 h) |
| **nós** | 11/2026 · 21 | máx. 569 | — |

- Demanda por tema (pesquisa de 09/11, `pesquisa/proximos-temas-2026-11/`): Roma 544 mil de mediana do top-10 em 12 m, Portugal 159 mil, Japão 138 mil, Alemanha 178 mil, Otomano 19 mil, Vikings 10 mil, México 20 mil. **Ucrânia, México e Otomano**, os próximos agendados no backlog, estão entre os de menor demanda ou de maior risco nessa própria pesquisa.
- **O formato tem teto em pt?** Não tem teto de demanda: um hit chega a 0,2–1,5 mi. O que existe é um **teto de previsibilidade**: nos 4 canais pt do molde, **3 de ~37 vídeos passaram de 100 mil; a mediana por canal vai de dezenas a ~3 mil views**. Cada canal acerta 1–2 temas (Irã, Rússia, França) e não sustenta o resto. Os dois que acertaram abandonaram o molde em semanas. **Hipótese:** o público pt clica no país "quente" (guerra, Copa, notícia), não no formato. Por isso ninguém vira canal com o formato.

### 2.2 O mesmo formato em outros idiomas
- **en:** o modelo existe e vale muito, mas tem dono e está esfriando. **History in Minutes** (09/2026, 24 mil inscritos): Egito 636 mil, Índia 660 mil, Ucrânia 181 mil, Pérsia 92 mil, China 58 mil; mas Japão 3,2 mil, Coreia 2,5 mil e Judaísmo 2,4 mil (09–27/11). **Genius History** (48,5 mil): Irã 1,0 mi, Roma 419 mil, Alemanha 356 mil (10/2026), Itália 49 mil, Rússia 14 mil. **VLAD – Meditative History** (02/2026): Irã 3,3 mi. **Historically**: Roma 11 mi. Levar o molde para en seria o "16º clone" (trava de concorrência ≤ 2 do `playbooks/novo-canal.md`), e a fábrica já tem o lugares-guerra-en com 0 inscritos.
- **es:** não achei prova do molde de país. O Atlas del Tiempo fez "TODA la Historia de Canadá" 898 e Afeganistão 65, enquanto a audiência de história em es vai para organizações (CIA×KGB 117 mil, Mossad 89 mil), ou seja, para o território do **nosso dossie-es**. Levar o historia-ptbr para es competiria com o próprio canal irmão.

### 2.3 O nicho vizinho que está crescendo em pt: "como era viver / você não sobreviveria"
Vídeos de 2026 em pt (`videos.list`, 28/11):
| vídeo | canal (criado · inscritos) | views |
|---|---|---|
| Por que o Brasil fala português enquanto toda América do Sul fala espanhol? (07/2026) | Revelando Brasil (11/2025 · **6,5 mil**) | **807.574** |
| Como Era a Vida em um Castelo Medieval no Ano de 1200 (04/2026) | Reconstrução Histórica (2021 · 71 mil) | 801.270 |
| O Dia em que Portugal se Mudou para o Brasil (03/2026) | Mundos Reimaginados (01/2026 · 109 mil) | 790.391 |
| Por Que Você Não Sobreviveria ao Banquete Real da Rainha Elizabeth I (06/2026) | Reconstrução Histórica | 590.720 |
| Como os Vikings Sobreviviam a −40 °C no Subsolo (04/2026) | Era Viking (12/2025 · **6,2 mil**) | 566.207 |
| Assim Era a Vida Dentro de uma Fazenda no Brasil Colonial em 1800 (05/2026) | Reconstrução Histórica | 507.275 |
| Como foram os primeiros dias sem Escravidão no Brasil em 1888 (03/2026) | Nostalgia BRASIL (01/2026 · 21 mil) | 385.439 |
| Assim Era a Vida Dentro de uma Caravela Rumo ao Brasil em 1500 (06/2026) | Reconstrução do Passado (03/2026 · 70 mil) | 333.863 |
| COMO era SOBREVIVER ao INVERNO na IDADE MÉDIA (02/2026) | Durma no Passado (11/2025 · 20 mil) | 333.416 |
| O Último Dia de Serviço de um Soldado Romano (10/2026) | fatos simples (04/2025 · **1,4 mil**) | 227.769 |
| A Vida Cotidiana na Roma Antiga em 117 d.C. (03/2026) | História em Reconstrução (10/2025 · **3,7 mil**) | 217.679 |
| Por que você não sobreviveria à higiene da Idade Média em 1348? (03/2026) | Crônicas de Ferro (32,5 mil) | 209.063 |
| COMO ERA A VIDA REAL NOS CASTELOS MEDIEVAIS (09/2026) | História do Amanhã (**408** inscritos) | 200.706 |
| 1315: Sem Água Potável, Sem Geladeira – Comer na Idade Média (04/2026) | Mistérios Medievais (03/2026 · **2,7 mil**) | 195.917 |

- **Porta aberta:** 6 canais com menos de 7 mil inscritos fizeram 196–808 mil views em 2026. Em en, o formato é gigante (Fossil "How Long You'd Last in Every Prehistoric Era" 13,6 mi).
- **Risco:** boa parte é "reconstrução com IA" realista em massa (Reconstrução Histórica: 284 vídeos; Histories of Humanity: 218 em 9 meses). O nicho está enchendo. O diferencial possível é o **bonequinho em 2ª pessoa com humor** ("você"), que nenhum desses usa, e o **Brasil** como tema, que en e es não fazem.

### 2.4 RPM
- **Hipótese:** pt-BR, história: **US$ 1–2,8 por mil views** (tabela da fábrica, `pesquisa/archive-in-minutes/IDIOMA.md` §7: história en US$ 4–8 × fator pt 0,25–0,35; fontes públicas divergentes; público ~87% BR). Não há dado nosso: nenhum canal da fábrica monetiza.
- Na prática, 100 mil views por mês em pt dariam ~US$ 100–280 por mês. Com o mesmo esforço em es, a faixa é US$ 1–3,2; em en, US$ 4–8.

---

## 3. Opções
| opção | o que é | prós | contras | custo |
|---|---|---|---|---|
| **(a) Encerrar** | tirar da noturna, não produzir mais, deixar os vídeos no ar | libera a cota do Max, a janela do Codex e o tempo do Rodrigo para o dossie-es; zero risco | desiste do único canal pt e dos ativos (estilo, voz, pipeline); os vídeos no ar seguem rendendo ~70–100 views por dia sem esforço | US$ 0 |
| **(b) Pausar sem custo** | sai da noturna; publicar só o que já está pronto (Cuba privado, Argentina) e esperar | US$ 0; mantém a opção aberta | nada muda nos números: o problema é o formato, não a cadência; "pausa" costuma virar abandono sem decisão | US$ 0 |
| **(c) Adaptar** (recomendada) | mesmo canal, bonequinhos e voz, outro ângulo: "como era viver / você não sobreviveria", Brasil no centro; nome novo (o atual colide com o clone de 6 mil inscritos) | nicho em alta em pt com porta aberta (6 canais < 7 mil inscritos com 200–800 mil); o bonequinho em 2ª pessoa se diferencia da enxurrada de "reconstrução IA"; o Brasil é um fosso que en e es não atravessam; custo baixo com o Codex | segue sendo pt (RPM baixo); o nicho está enchendo de IA em massa; exige bíblia nova (roteiro em 2ª pessoa, hook de cena física); vídeos sobre escravidão e morte esbarram nas políticas do canal | ~US$ 1–3 por vídeo + cota do Max; teste de 4 vídeos ≈ US$ 10 |
| **(c') Levar o molde para en/es** | canal novo do formato "história de país" | RPM maior | en: concorrência com dono (History in Minutes, Genius, VLAD) e o próprio modelo esfriando; es: sem prova do molde de país, e o público de história em es já é do dossie-es | novo canal (bloqueado pela trava de concorrência) |
| **(d) Manter com metas** | seguir 4 vídeos por semana, títulos-fórmula de volta, só civilizações grandes | os títulos-fórmula tinham CTR de 4–5,8% | 15 vídeos sem hit; o mercado pt mostra que o molde é loteria; os temas agendados (Ucrânia, México, Otomano) são justamente os de baixa demanda ou alto risco; consome Max e Codex todas as noites | ~US$ 4–12 por semana + Max |

---

## 4. Recomendação: adaptar com prazo curto e matar se não pegar

**Hoje:** a série "história de país" sai da produção noturna. As noites 28/11–06/12 (Ucrânia, México, Otomano, Grécia, Vikings, Itália) não são produzidas. Decisão do Rodrigo: nada foi mudado.

**Teste:** 4 vídeos de "Como era viver / Você não sobreviveria a…", com bonequinhos em 2ª pessoa ("você acorda em 1500…"), hook de cena física nos primeiros 15 s (a lição do dossie-es), título de **fato concreto** (nada de pergunta-paradoxo) e 12–15 min. **1 vídeo por semana**, nunca dois colados, porque cada um precisa do seu teste de 48 h. O nome do canal precisa mudar antes (decisão dele).

**Critério de sucesso (tudo pela Reporting e pela Analytics API):**
- **Passa** se pelo menos 1 dos 4 fizer **≥ 3.000 views em 7 d** com **CTR ≥ 4% nas primeiras ~1.000 impressões**, e a mediana dos 4 ficar em **≥ 800 views em 7 d** (hoje: 163 na v1 e 17 na v2).
- **Encerra** se até **10/01/2027** (4 vídeos) não chegar lá: o canal fica no ar e a produção para.
- **Se passar,** a próxima meta é **300 inscritos até 28/02/2027**. Se não chegar, encerra também.

**5 temas de exemplo, com demanda real em pt (2026):**
| # | tema (título de trabalho) | evidência |
|---|---|---|
| 1 | Você não sobreviveria à viagem de caravela até o Brasil em 1500 | Reconstrução do Passado, caravela rumo ao Brasil, **333.863** (06/2026); Histories of Humanity, navio de guerra de 1600, 114.652 |
| 2 | Como era viver no Rio quando a corte portuguesa chegou (1808) | Mundos Reimaginados, "O Dia em que Portugal se Mudou para o Brasil", **790.391** (03/2026) |
| 3 | Você não sobreviveria a um inverno na Idade Média | Durma no Passado **333.416** (20 mil inscritos); Era Viking −40 °C **566.207** (6,2 mil inscritos); Crônicas de Ferro, castelos que não congelavam, 197.181 |
| 4 | Um dia na vida de um soldado romano | fatos simples **227.769** (1,4 mil inscritos, 10/2026); História em Reconstrução, Roma em 117 d.C., 217.679 e soldado 101.349 (3,7 mil inscritos) |
| 5 | Por que o Brasil fala português e o resto da América do Sul fala espanhol (versão "como era viver" nas fronteiras de 1750) | Revelando Brasil **807.574** (6,5 mil inscritos, 07/2026) |

Reservas: banquete/higiene (Reconstrução Histórica 590.720; Crônicas de Ferro 209.063; Mistérios Medievais 195.917, 2,7 mil inscritos). Temas sobre escravidão (fazenda de 1800, 507 mil; 1888, 385 mil) têm demanda, mas pedem muito cuidado com as políticas e com o tom dos bonequinhos: ficam fora do teste.

**Por que não encerrar já:** o custo marginal é baixo (US$ 1–3 por vídeo), existe um nicho vizinho com prova clara e porta aberta, e o canal tem ativos prontos. **Por que não manter:** 15 vídeos, 2.088 views e nenhum hit. O mercado pt mostra que o molde de país é loteria, e quem acertou também abandonou. **Pior caso do teste:** ~US$ 10 e 4 etapas de Max em 6 semanas, e a decisão de encerrar fica tomada com número.

### Ações gratuitas paralelas (opcionais)
- Cuba (privado) e Argentina (não subiu) já estão pagos. Publicar os dois **com título-fórmula** ("A história INTEIRA de X em N minutos"), em semanas sem o teste, serve de controle grátis da hipótese de que o título-pergunta derruba o CTR.
- Atualizar `youtube.videos.publicado_em` dos vídeos no ar (008–014, 016 estão sem data): a query de comparação v1 × v2 da bíblia ignora esses vídeos.
