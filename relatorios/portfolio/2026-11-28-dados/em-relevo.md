# Em Relevo: diagnóstico de portfólio e "perspectiva certa" (28/11/2026)

Só análise. Não mudei canal, backlog, bíblia, banco, timers nem vídeos. Custo pago: US$ 0 (yt-dlp via WARP + Data API só `videos/channels/playlistItems.list`, ~150 unidades).
**Fontes:** `youtube.videos`, `metricas_video` (snapshots até 28/11), `analytics_trafego` / `analytics_trafego_detalhe` / `analytics_retencao` / `analytics_video_dia` (Analytics API até 25/11), `alcance_diario` (Reporting API, impressões e CTR até 26/11), `studio_video` (só 1 export, de 14/11, com 2 vídeos), `financas.consumo` e `financas.lancamentos`. Mercado: 84 buscas yt-dlp via WARP (pt/en/es, por relevância e "este ano por views") + uploads de 34 canais concorrentes (Data API, 28/11). Brutos de trabalho em `~/cache/tmp/emr/` (fora do git).
**Pergunta do Rodrigo:** "O Em Relevo eu ainda acredito que pode ser bom, é bom conteúdo, talvez estejamos olhando da perspectiva errada."

## Resumo (10 linhas)
1. **Números:** 5 vídeos no ar, **406 views**, 3 inscritos, 25 h de exibição, **4.213 impressões em 17 dias** e CTR ponderado de **2,2%**. Pago do bolso: ~US$ 2,5 + ElevenLabs R$ 6,14, ou seja, ~R$ 20. O dinheiro não é o problema. O que custou foi a fila da fábrica e a cota do Max.
2. **O problema não é o conteúdo.** A retenção do El Niño é de 59% num vídeo de 12 min (relativa 0,5–0,66), boa para o tamanho. O problema vem **antes do play**: o YouTube quase não testou o canal (4 mil impressões no total, contra ~5 mil por vídeo na 1ª semana dos que pegaram no Dossier). E onde testou, o clique foi baixo: Seca 1877 teve **0,99% em 1.814 impressões no sugerido**, e isso encerrou o teste.
3. **Tema sem vizinho = vídeo sem público.** Seca 1877 e El Niño 1983 foram sugeridos ao lado de "Brasil Urgente", Felipe Neto e política: o YouTube não sabia para quem mostrar. **O único vídeo com tração (El Niño 2026, 163 views, +140 na última semana, sem nada novo publicado)** foi sugerido ao lado de notícias de El Niño (O POVO 29 views, BBC Brasil 27, Cosmos Brutal 10), com CTR de 3,2% no sugerido.
4. **A prova mais dura:** na mesma semana, o Cosmos Brutal (844 inscritos) postou "O SUPER El Niño Visto do Espaço: o Que Vai Acontecer com o Brasil" e fez **100 mil views (93× a mediana dele)**. O nosso El Niño, do dia seguinte, tem 163. Tema igual e canal igualmente pequeno: a diferença é a **embalagem** (pergunta sim/não × urgência com data; thumb escura e abstrata, "SÓ 2 °C?", × globo saturado e "DEZEMBRO CRÍTICO").
5. **A perspectiva errada:** o canal foi pensado a partir **do que sabemos fazer** (relevo 3D real, dado NASA, tom de serviço, desastre histórico). O espectador clica numa **pergunta sobre algo que ele já está acompanhando agora**. O mapa 3D real deixou de ser diferencial na hora do clique: desde out/2026, os clones usam relevo 3D (de IA) nas thumbs, mais saturado que o nosso (mosaico na §2.4).
6. **A perspectiva certa, pelos dados:** "o mapa é o meio, não a promessa". O vídeo precisa entrar numa **corrente de audiência que já existe**, como o Dossier fez com a Cosa Nostra. Para o Em Relevo, a única corrente que já nos testou e deu clique é o **Super El Niño 2026–27**. É o maior tema de clima em pt agora (19 vídeos ≥ 100 mil no ano; canais de 3–6 vídeos fizeram 1,1–2,2 mi em out–nov), e o pico vai de dezembro a fevereiro, ou seja, tem prazo.
7. **Hipóteses:** (i) evento extremo: funciona, mas só com 24–72 h de entrega; o El Niño é a exceção, sazonal e previsível. (ii) "Por que o estado X é assim": a demanda existe, mas a onda pt de out/2026 já está saturada (Explica no Mapa caiu de ~1 mi para 2 mil por vídeo em 5 semanas). (iii) en/es: melhor teto e RPM; o El Mecanismo (es) é o modelo mais próximo do Em Relevo que está crescendo, mas seria um canal novo. (iv) Shorts: evidência fraca. (v) engenharia sobre o relevo: boa, mas é outro canal.
8. **Recomendação: (c) ADAPTAR com prazo e corte.** Temporada "Super El Niño no mapa": reembalar o 002 (US$ 0) e fazer **4 vídeos novos até 31/12/2026**, todos sobre o El Niño no Brasil, com embalagem de urgência e lugar (§4).
9. **Critério:** CTR ≥ 3,5% nas primeiras ~1.000 impressões do sugerido em ≥ 2 dos 4, **e** 1 vídeo ≥ 10 mil views em 14 dias **ou** média ≥ 3 mil em 14 dias. Corte antecipado: se os 2 primeiros tiverem CTR < 2% com ≥ 1.000 impressões, encerra. **Se não bater até 15/01/2027, encerra de vez** (sem nova pausa) e o motor 3D vai para um canal es/en.
10. **Pendências achadas (não mexi):** (a) o título no ar do 004 (`2WH4ducITO0`) é literalmente "O El Niño causou seca no Nordeste e..." (truncado, conferir no Studio); (b) a Seca 1877 segue no ar com "**matou** 500 mil" no título, contra a política da bíblia; (c) o espelho do backlog ainda mostra o Granizo agendado para hoje (28/11), mas o canal está fora da fábrica noturna desde 17/11 (`~/.config/fabrica/noturna.env`); (d) 006 Caraguatatuba (pronto) e 007 Vendavais PR (roteiro) estão parados.

---

## 1. Diagnóstico

### 1.1 Por vídeo
Views 48 h / 7 d pelo snapshot diário mais próximo (`metricas_video`). Impressões e CTR da Reporting API (`alcance_diario`, "basic" = todas as origens; "sug." = vídeos sugeridos), até 26/11. O Studio só tem o export de 14/11 (001: 184 imp, 2,72%; 002: 179 imp, 1,68%); **falta export do Studio para 003–005**. Retenção = % visto médio no último snapshot. Custo = `financas.consumo` por `ref_id` (a API Anthropic vem dos créditos incluídos no Max; a ElevenLabs é plano mensal de R$ 6,14, sem rateio por vídeo).

| nº | título no ar (Data API 28/11) | publicado | 48 h | 7 d | total | impressões · CTR (sug.) | % visto (média de tempo) | de onde vieram as views | custo USD |
|---|---|---|---|---|---|---|---|---|---|
| 001 | O que está acontecendo com o clima no Sul do Brasil? | 11/11 | 15 | 18 | 58 | 262 · **5,34%** (sug. 189 · 3,70%) | 40% (4:12 de 10:23) | busca 26 (termos irrelevantes: "espectro de brocken no rio grande" 6, "aeroporto de maringá" 1), sugerido 21 (8 do nosso 002), WhatsApp 5 | ~0 registrado |
| 002 | El Niño 2026 vai ser o mais forte da história? | 12/11 | 14 | 20 | **163** | 595 · 3,19% (sug. 537 · **3,17%**) | **59%** (7:10 de 12:10) | **sugerido 120**: O POVO "El Niño deve atingir pico na virada do ano" 29, BBC Brasil 27, Cosmos Brutal 10, Ruptura do Povo 8 | 1,07 (Runpod) |
| 003 | Por que quase ninguém fala da seca que **matou** 500 mil brasileiros? | 15/11 | 27 | 28 | 31 | **1.832 · 1,04%** (sug. 1.814 · **0,99%**) | 33% (3:35 de 10:45) | sugerido 24, todos de 1 view, ao lado de vídeos sem relação (Tim Lopes, BNDES, Felipe Neto, política) | 0,48 |
| 004 | **"O El Niño causou seca no Nordeste e..."** (truncado no ar) | 16/11 | 19 | 19 | 24 | 487 · 2,67% (sug. 461 · 2,17%) | 44% (4:26 de 10:07) | sugerido 19 (Brasil Urgente "corpo em geladeira" 2, Rodoanel 2, Coisa de roça…) | 0,92 |
| 005 | Por que a chuva da SERRA alagou PORTO ALEGRE? | 18/11 | 52 | 123 | 130 | 1.037 · 2,60% (sug. 844 · 2,01%; navegação 175 · 5,14%) | 41% (3:59 de 9:49) | navegação/home 73–77, sugerido 46 (MetSul, Puchalski, Chão do Sul, nosso 002), busca 5 | 0,79 |
| **Total** | | | | | **406** (canal 401) | **4.213 · ~2,2%** | | 25 h de exibição; +3 inscritos | **~3,3** (Runpod 1,82 + créditos API 1,44) |

**Retenção (curva da Analytics API, 25/11):**
- **002 El Niño:** 88% aos 5%, 56% na metade, 46% no fim. Retenção relativa 0,52–0,66: está **acima** de vídeos do mesmo tamanho.
- **005 Porto Alegre:** 68% aos 5% do vídeo (~30 s), ou seja, **perde 32% no hook**.
- **003 Seca:** perde 39% aos 5%, com relativa 0,19 até os 10%.
- **001 Sul:** perde 26% aos 5%, com relativa ~0,4.

Amostras pequenas (24–163 views), mas o desenho bate: quando o tema tem público (El Niño), o conteúdo segura.

### 1.2 Embalagem, distribuição, tema ou retenção?
| causa | evidência | veredito |
|---|---|---|
| **Distribuição (o YouTube não testou)** | 4.213 impressões em 5 vídeos e 17 dias. No Dossier, os vídeos que pegaram tiveram 2,6–5 mil impressões **por vídeo** na 1ª semana (`canais/dossie-es/analises/2026-11-27-diagnostico.md` §2) | **Sintoma**, não causa: o teste é pequeno porque o canal não tem vizinhança e o CTR do 1º lote foi baixo |
| **Tema sem vizinho** | 003 e 004 (desastre histórico) caíram ao lado de vídeos aleatórios; 002 (tema do momento) caiu ao lado de notícias de El Niño e é o único que cresce sozinho (20 → 163 views entre 21 e 28/11) | **Causa principal** |
| **Embalagem** | CTR no sugerido: 0,99% (003), 2,0–2,2% (004, 005), 3,2% (002); no Dossier, abaixo de 2% encerra o teste e os vencedores ficaram em 4–7%. Mesmo tema, mesma semana: Cosmos Brutal fez 100 mil e nós 163. O 003 tem "matou" no título; o 004 está truncado; o 002 é pergunta sim/não (a própria bíblia diz que "esgota a curiosidade") | **Causa principal** (junto com o tema) |
| **Retenção** | 002: 59%, bom. Hooks de 003/005 perdem 32–39% em 30 s | **Secundária**: conserta-se no roteiro, mas não explica 400 views |

**Total gasto × resultado:** ~R$ 20 do bolso (Runpod, fal, Fish, ElevenLabs) + ~US$ 2,4 de créditos de API, para 406 views, ~R$ 0,05/view. O custo real é **oportunidade**: 7 vídeos em produção (5 no ar, 006 pronto e 007 com roteiro), cada um com etapa 1 em Opus e etapa 2 em Sonnet na cota do Max, que o Dossier (o canal que dá resultado) também usa. O lado bom: o Em Relevo **não usa Codex** (zero IA de imagem), então não disputa a janela de imagens da noite.

**A amostra de 5 basta?** Para julgar o **formato** (mapa 3D + dado + narração), não: 4 mil impressões é pouco e houve 4 variáveis mudando ao mesmo tempo (voz, thumb, título, tipo de episódio). Para julgar a **escolha de temas** (desastre histórico/evergreen sem corrente de audiência), sim: 3 de 3 nesse tipo ficaram sem vizinho e com CTR ≤ 2,7%. E a meta de DESCARTAR do RELATORIO de 08/11 já foi batida: média < 1,5 mil, nenhum > 5 mil e CTR < 2% no 003.

---

## 2. Mercado

### 2.1 Canais (uploads via Data API, 28/11; mediana dos vídeos > 3 min)
| idioma | canal | 1º vídeo | inscritos | mediana longos 12 m | mediana 7–21 d → 22–45 d | views de vídeos publicados em 30 d | leitura |
|---|---|---|---|---|---|---|---|
| pt | **O Mundo e Tudo ao Redor** | 14/10/2026 | 31,6 mil | 107.785 | 105 mil → 207 mil | 7,48 mi | "e se/por que" Terra + espaço; últimos 5 vídeos com 6–24 mil (esfriando) |
| pt | **Explica no Mapa** | 24/10/2026 | 20,2 mil | 34.640 | 62 mil → 30 mil | 4,21 mi | 59 vídeos em 35 dias. Começou com "Por que existem dois Mato Grosso?" (1,17 mi) e caiu para **2 mil–57 views** na última semana |
| pt | Chão do Sul | 24/10/2026 | 9,9 mil | 18.713 | **8,5 mil** → 97 mil | 218 mil | 1º vídeo com 972 mil; caindo |
| pt | O Mapa Não Mente | (canal de 2021, novo formato em out/2026) | 31,9 mil | 1.796 | 1,4 mil → 4,1 mil | 1,43 mi (1 hit de 661 mil) | clone em queda; postou hoje "Tsunami no Rio: até onde a água chegaria?" (8 views) |
| pt | Mundo Entrópico | 13/01/2025 | 67,7 mil | 36.135 | 62 mil → 62 mil | 1,09 mi | o dono antigo continua estável |
| pt | Capital Financeiro | antigo | 510 mil | 311.573 | 259 mil → 281 mil | 1,63 mi | "Por que nenhum outro estado é como o RS" 1,38 mi (4,4×) |
| pt | Um Documentário | 11/04/2026 | 144 mil | 643.275 | 812 mil → 981 mil | 2,60 mi | desastre reconstruído de 60+ min (Miyako 8,3 mi) |
| pt | Natureza em Fúria / MetSul | antigos | 96 mil / 323 mil | 38 mil / 90 mil | estável | 3,5 mi / 2,2 mi | notícia de clima (formato proibido para nós: TV/flagrante) |
| pt | Mapa Verso | 28/10/2025 | 144 mil | (Shorts) mediana **229 mil** | — | 195 mil | Shorts "E se o Brasil invadisse X" (17,6 mi): ficção de guerra, não é o nosso formato |
| es | **El Mecanismo** | canal de 2012, formato novo em jun/2026 | 51,9 mil | 30.999 | **365 mil** → 41 mil (91–180 d: 4 mil) | **4,03 mi** | **o mais parecido com o Em Relevo que está crescendo**: "¿Qué hay detrás de las inundaciones de Nepal?" 3,36 mi; "¿Por qué este Súper Niño es el más peligroso?" 2,27 mi; "¿Por qué las represas no pueden frenar al río Paraná?" 1,06 mi (24,8×); "Terremoto en Perú…" 517 mil (21/11) |
| es | Geografía con Geoff | antigo | 150 mil | 116.195 | 59 mil → 69 mil | 712 mil | "Por qué nadie vive en…" 3,8–4,0 mi |
| es | Del Plano al Hierro | 27/10/2026 | 4,6 mil | 57.753 | 52 mil → 570 mil | 1,24 mi | engenharia no relevo: "¿Por qué Argentina hizo un túnel y no un puente?" 973 mil |
| es | La Otra Cara del Mapa / Mundo Olvidado | 2025 / ago 2026 | 26,7 mil / 16,6 mil | 28 mil / 7,8 mil | estável / **816** | — | Uruguai 3,0 mi e 1,5 mi; clones em queda |
| en | Geography By Geoff | antigo | 1,13 mi | 668.030 | 369 mil → 728 mil | 3,54 mi | "Why almost NOBODY lives on Australia's west coast" 11,4 mi |
| en | The Last Day | 10/07/2026 | 37,7 mil | 155.855 | 17 mil → 225 mil (46–90 d: 918 mil) | 455 mil | "Nepal's 2026 Disaster Explained" 5,3 mi |
| en | UnderTheHeadline | 28/08/2026 | 16,6 mil | 39.871 | — | 0 | o **1º vídeo** (Nepal, 1 dia depois da enchente) fez 4,1 mi; depois, mediana de 40 mil |
| en | Geography Effect | 19/02/2026 | 34,2 mil | 57.639 | 96 mil → 101 mil (46–90 d: 235 mil) | 1,14 mi | "Why Canada is sitting on…" 1,29 mi |
| en | Disasters Explained | 15/11/2025 | 30,7 mil | 35.355 | 12 mil → 144 mil | 525 mil | "Every Tornado Type Explained" 3,6 mi |
| en | RealLifeLore / Astrum Earth / Practical Eng. / Wendover | antigos | 0,5–7,9 mi | 1,1–1,3 mi | — | 3–4 mi cada | donos; "Why the Nepal flood was WAY scarier" (RLL) 2,37 mi |

**Quem cresceu em 2026:** em pt, a onda "Brasil explicado no mapa" de out/2026 (Explica no Mapa, Chão do Sul, O Mapa Não Mente, O Mundo e Tudo ao Redor) **já está no fim**: todos caem de 5× a 50× do 1º mês para o último vídeo. Em es, cresceram El Mecanismo (ciência da Terra com gancho de evento) e Del Plano al Hierro (engenharia). Em en, cresceram os canais de evento explicado (The Last Day, UnderTheHeadline) e Geography Effect.

### 2.2 Demanda por busca (yt-dlp via WARP, top 20; "12 m" = publicados de 28/11/2025 a 28/11/2026, longos > 3 min)
| idioma | consulta | longos 12 m ≥ 100 mil | exemplos (views, data, canal) |
|---|---|---|---|
| pt | "el niño 2026 brasil" | **19 de 19** ("este ano") / 10 de 20 (relevância) | Jubilut "Super El Niño no Brasil: o que esperar?" 5,94 mi; Manual do Mundo 3,66 mi; **CanalSingularidade "O Pacífico está PARTINDO o BRASIL em DOIS" 2,20 mi em 4 dias (24/11; o canal tem 3 vídeos)**; Sou curioso?! "O El Niño de 2026 NÃO é o que você pensa" 1,10 mi (4,6×, 6 vídeos); BBC Brasil 1,47 mi (8,7×); Fatos Desconhecidos 1,15 mi (6,6×); **Cosmos Brutal 100 mil (93×, 844 inscritos, 11/11)** |
| pt | "por que ninguém mora" | 19/20 | Canal Top10 "Por que quase ninguém mora no Uruguai?" 1,63 mi; Explica no Mapa litoral SP 1,04 mi (26/10) |
| pt | "por que o sul do brasil" | 5 de 8 (relevância) | Chão do Sul 972 mil (24/10); Capital Financeiro 1,30 mi (2023) |
| pt | "terremoto no brasil" / "tsunami no brasil" | 4 / 2 (relevância, longos) | Fatos Desconhecidos "Super terremoto pode atingir o Brasil" 481 mil |
| pt | "seca no nordeste explicada" / "enchente explicada" | 1 / 1 | quase nada: **desastre "explicado" sem gancho atual não puxa em pt** |
| pt | "relevo do brasil" / "mapa 3d brasil" | 0 (aula) / 2 | ninguém busca "relevo"; o 3D não é demanda, é estilo |
| en | "why nobody lives here" | 19/19 | Geoff 11,4 mi / 3,95 mi / 2,69 mi |
| en | "flood explained" / "disaster explained 2026" | 18/18 / 12/12 | Nepal: FRANCE 24 8,2 mi, The Last Day 5,3 mi, UnderTheHeadline 4,1 mi (todos ≤ 8 dias após o evento) |
| en | "what if dam failed" | 16/19 | Zem TV 2,86 mi; Practical Eng. Teton 1,24 mi; B1M Colômbia 1,01 mi |
| es | "por qué nadie vive aquí" | 16/20 | Geoff es 4,0 / 3,8 mi; La Otra Cara del Mapa Uruguai 3,0 mi |
| es | "desastre explicado" | 18/19 | El Mecanismo Nepal 3,36 mi; Pecas Explica 966 mil |
| es | "por qué méxico" / "por qué argentina" | 20/20 / 20/20 | Sapiens Explica "¿Qué hay debajo de la Ciudad de México?" 1,06 mi; El Mecanismo Paraná 1,06 mi; Del Plano al Hierro 973 mil |
| en/pt | "3d map shorts terrain" / "mapa 3d relevo shorts" | 0 / 0 | Shorts de relevo não aparecem como demanda de busca |

O filtro "este ano por views" mistura vídeos fora do tema (futebol em "por que são paulo", Reed Timmer em "tornado no brasil"). Usei esses números só onde os 5 primeiros eram do tema, conferidos à mão.

### 2.3 RPM por idioma [Hipótese]
Faixas da fábrica (`playbooks/garimpo-tendencias.md`; `pesquisa/archive-in-minutes/IDIOMA.md` §7; `pesquisa/canal-clima-2026-11/RELATORIO.md` §3), sem dado nosso, porque nenhum canal está monetizado:

| idioma | geografia/educação | clima/desastre (marca menos segura) |
|---|---|---|
| en | US$ 4–8 (até 10 em economia) | US$ 3–8 |
| es | US$ 1–3,2 | idem |
| pt | US$ 1–2,8 | US$ ~1–2 |

**Ordem de grandeza do que pt rende, mesmo com sucesso:** 100 mil views/mês ≈ US$ 100–280/mês. YPP: 1.000 inscritos + 4.000 h; hoje temos 3 inscritos e 25 h.

### 2.4 Embalagem: nós × quem pegou (thumbs de 28/11)
- **El Niño:**
  - Cosmos Brutal "DEZEMBRO CRÍTICO": globo de satélite com o Pacífico em brasa e data de urgência; 100 mil views.
  - JeanGrafia "7 TORNADOS em 6 DIAS": rosto, número e Brasil rachado; 146 mil.
  - CanalSingularidade "O PIOR VEM AGORA": continente em lava; 2,2 mi.
  - **Nosso** "SÓ 2 °C?": mapa plano escuro e termômetro; 163 views.
- **Brasil no mapa:**
  - Explica no Mapa "POR QUE DOIS?": MT/MS sobre relevo 3D claro; 1,17 mi.
  - Chão do Sul "O SUL É OUTRO PAÍS": recorte 3D do relevo com geodos; 972 mil.

  **A nossa "assinatura" (recorte de relevo 3D) já é a linguagem dos clones**, com cores mais vivas e fundo claro. As nossas thumbs são escuras e abstratas.
- Os títulos que pegaram têm **urgência/tempo** ("Dezembro crítico", "pico na virada do ano", "está partindo"), **o Brasil como sujeito** e nada de pergunta sim/não. O "vai ser o mais forte da história?" é o anti-padrão que a própria `biblia/titulo.md` já lista.

### 2.5 As hipóteses, com evidência
| hipótese | a favor | contra | veredito |
|---|---|---|---|
| **(i) gancho de evento extremo** em vez de evergreen | Os maiores hits de 2026 no nicho são evento explicado logo depois do fato (Nepal: The Last Day 5,3 mi e UnderTheHeadline 4,1 mi em ≤ 8 dias, El Mecanismo 3,36 mi em 1 dia; RealLifeLore 2,37 mi em ~3 semanas). O nosso único vídeo com tração é do tema do momento. Em es, o El Mecanismo cresceu de 4 mil para 365 mil de mediana com esse gancho | Exige entrega em 24–72 h; a fábrica produz em noites fixas (sáb–ter) com ~1 dia de pipeline. O Rodrigo recusou a r1 de 17/11 por "parecer notícia". Em pt, notícia de clima é TV/flagrante (Content ID). Evento ruim (mortes) pede cuidado | **Confirmada, com 1 exceção viável:** o **Super El Niño** é um "evento" de meses, previsível, com pico em dez–fev. Dá para planejar sem correr. Evento aleatório (terremoto, enchente) só com um modo "quente" que a fábrica não tem |
| **(ii) "por que o Brasil/estado X é assim"** (geografia explica economia/história) | Demanda grande (19/20 ≥ 100 mil em "por que ninguém mora"); Capital Financeiro e Mundo Entrópico estáveis | A onda pt de out/2026 está saturada: Explica no Mapa caiu de 1 mi para 2 mil em 5 semanas; Chão do Sul de 972 mil para 8,5 mil; O Mapa Não Mente para 1,4 mil. Os clones já usam relevo 3D na thumb. Entraríamos como o enésimo | **Demanda real, janela fechando.** Não como eixo; dá para usar 1 tema por mês quando houver um ângulo de relevo que ninguém fez |
| **(iii) mesmo formato em en/es com tema global** | en/es têm teto e RPM melhores (en 3–4× pt). O El Mecanismo (es) é quase o Em Relevo em espanhol e cresce agora. O RELATORIO de 08/11 já recomendava en (matriz 7,75 × pt 6,30); o canal saiu em pt mesmo assim. Regra do Rodrigo: en → es → pt | É **canal novo** (o Em Relevo tem só 3 inscritos de patrimônio, então mudar de idioma custa pouco, mas exige decisão, voz e revisão). Em en, a concorrência é forte (RealLifeLore, Practical Eng., The Last Day). Não temos prova de que a nossa embalagem ganha clique nesse nicho, em nenhum idioma | **Melhor destino de longo prazo, mas não agora.** Primeiro provar que acertamos a embalagem com o tema que já nos testou. Se a temporada El Niño funcionar, o passo seguinte é a versão es, no modelo do El Mecanismo |
| **(iv) Shorts de mapas 3D** | Mapa Verso: mediana de 229 mil em Shorts; @relevo.ia com 213 mil curtidas no Instagram | Os Shorts que explodem são ficção de guerra ("E se o Brasil invadisse a Noruega"), outro produto. "3d map shorts" não aparece como demanda; O Mapa Não Mente tem Shorts com ~2 mil. RPM de Shorts em pt é quase zero e a conversão para longo é fraca | **Fraca.** Não justifica fila |
| **(v-a) "e se / pergunta grande"** (O Mundo e Tudo ao Redor) | OMTR: mediana de 108 mil, 7,5 mi em 30 dias. Itaipu: 1 vídeo pt com 103× (Fivertix) | O OMTR já esfria (últimos com 6–24 mil) e é muito de espaço. Clones já entram nas ideias da r2 (O Mapa Não Mente "Tsunami no Rio" hoje). O Rodrigo pausou o canal com essas candidatas na mesa | **Bom para 1 vídeo de reserva** (Itaipu), não como linha |
| **(v-b) engenharia contra o relevo** (por que não cai / como foi construído) | es: Del Plano al Hierro (4,6 mil inscritos) com 973 mil; Sapiens Explica com 1,06 mi; nichos-editorial (11/11) pôs engenharia como nicho #2 | Muda a promessa do canal; na prática é o canal #2 do `pesquisa/nichos-editorial-2026-11/RELATORIO.md` | **Destino do motor 3D se o Em Relevo encerrar** |

**Qual "perspectiva certa" os dados sugerem:** parar de vender o **mapa** e o **desastre do passado** e vender a **pergunta urgente que o brasileiro já está acompanhando**, com o mapa como a resposta. Concretamente, hoje: o Super El Niño no Brasil, com urgência de data e lugar. É a perspectiva do espectador, não a do produtor.

---

## 3. Opções
| opção | o que é | prós | contras | custo |
|---|---|---|---|---|
| **(a) encerrar** | arquivar o canal; o motor 3D vai para outro canal | libera fila e cota do Max para o Dossier/História; a meta de DESCARTAR de 08/11 já foi batida | desiste com 4 mil impressões de teste, logo no pico do único tema que deu sinal (El Niño, dez–fev) | 0 |
| **(b) pausar sem custo** (status atual) | nada é produzido; o 002 segue crescendo devagar | zero custo | **é a pior opção:** não decide, não aprende, e a janela do El Niño passa. O backlog vivo segue gerando itens "agendados" que não rodam (Granizo hoje) | 0 em dinheiro; custo de atenção |
| **(c) adaptar** | temporada "Super El Niño no mapa": reembalar o 002 + 4 vídeos até 31/12, embalagem de urgência/lugar, crivo com as thumbs que pegaram como régua | testa exatamente a causa diagnosticada (tema com corrente + embalagem) usando o único sinal que temos; prazo natural (o pico passa em fev); sem Codex; barato | o tema é disputado (Jubilut, BBC, clones), então pede ângulo próprio de mapa/dado; risco de "parecer notícia" (mitigado: "explicado", nunca flagrante); em pt o teto de RPM é baixo mesmo com sucesso | ~US$ 1–2 de Runpod + voz por vídeo (~R$ 10–20) + 4 × (e1 Opus + e2 Sonnet) na cota do Max |
| **(d) manter com metas** | voltar à fábrica noturna com o backlog atual (Granizo, calor, litoral RS, neve, cânions, geada negra) | mantém a cadência | repete a perspectiva que falhou: 4 de 6 temas são evergreen/históricos sem corrente; o Rodrigo já recusou o Granizo | igual a (c), mas sem hipótese nova |

---

## 4. Recomendação: **(c) ADAPTAR — temporada "Super El Niño no mapa", com corte em 15/01/2027**

**Por que não encerrar já:** a amostra não testou o formato, testou temas sem público. O único tema com público deu 59% de retenção e 3,2% de CTR mesmo com embalagem fraca. Canais minúsculos estão fazendo 100 mil–2,2 mi **agora** nesse tema. O teste custa ~R$ 60–80 e termina em 6 semanas, com regra de corte. Se falhar, encerra de verdade.
**Por que não ir direto para es/en:** antes de abrir canal novo, é preciso provar que a nossa embalagem ganha clique nesse nicho. Hoje não temos essa prova em nenhum idioma.

**Como (proposta; nada executado, decisão do Rodrigo):**
1. **Dia 0, US$ 0:** reembalar o 002 no Studio: título de urgência + lugar (ex.: "O Super El Niño vai partir o Brasil em dois em DEZEMBRO?" → passar no crivo) e thumb clara de satélite com o Pacífico quente e 2 palavras de tempo ("DEZEMBRO CRÍTICO" é do Cosmos; o nosso precisa de outra). Corrigir o título truncado do 004 e tirar o "matou" do 003.
2. **4 vídeos novos, 1 por semana, até 31/12** (publicar em ≤ 48 h após a noite de produção). Cada um com:
   - embalagem pelo crivo, tendo como régua as thumbs que pegaram (§2.4: fundo de satélite claro e saturado, Brasil grande, 2–3 palavras com tempo/lugar);
   - hook com cena física nos primeiros 15 s (lição do Dossier);
   - capítulo que paga o título antes de 40%.
3. **Medir** na Reporting API, 48 h e 7 d após cada vídeo: CTR no sugerido nas primeiras ~1.000 impressões, de quem vem o sugerido, views em 14 d.

**Critério de sucesso (tudo até 15/01/2027, 14 dias depois do 4º vídeo):**
- **Continua (e abre a versão es no modelo do El Mecanismo):** CTR no sugerido ≥ 3,5% em ≥ 2 dos 4 vídeos novos **e** (1 vídeo ≥ 10 mil views em 14 dias **ou** média ≥ 3 mil views em 14 dias).
- **Corte antecipado:** se os 2 primeiros tiverem CTR < 2% com ≥ 1.000 impressões cada, encerra no 2º vídeo.
- **Encerra:** se não bater o critério em 15/01/2027. Sem nova pausa: arquivar o canal, apagar os itens do backlog vivo e levar o motor 3D (Remotion + relevo real + Runpod) para o candidato en/es de engenharia ou economia (`pesquisa/nichos-editorial-2026-11/`).

### 5 temas de exemplo (com evidência de demanda, 28/11)
| # | tema (título provisório, vai ao crivo) | evidência | nosso ângulo de mapa |
|---|---|---|---|
| 1 | **Onde o Super El Niño bate primeiro no Brasil (dez–jan)** | O POVO "El Niño deve atingir pico na virada do ano" 423 mil (24/11) e é a 1ª fonte do nosso sugerido; Cosmos Brutal "O que vai acontecer com o Brasil" 100 mil (93×, 11/11); Olá, Ciência! "O verdadeiro impacto do Super El Niño na sua vida" 1,49 mi (3,9×) | anomalia NOAA/IMERG sobre o relevo, semana a semana, até o município |
| 2 | **Por que o El Niño seca o Norte e afoga o Sul** | CanalSingularidade "O Pacífico está PARTINDO o BRASIL em DOIS" 2,20 mi (24/11; 3 vídeos no canal); JeanGrafia "por que o Norte vai SECAR e o Sul vai AFOGAR" 150 mil (5,5×) e "O El Niño RACHOU o Brasil ao meio!" 146 mil (5,3×, 10/11) | o jato e os Andes em 3D (a "culpa dos Andes" que já temos do 005), com chuva real do IMERG |
| 3 | **Toda vez que veio um Super El Niño, isto aconteceu com o Brasil (1983, 1998, 2015)** | O Primo Rico "Toda vez que aconteceu, o Brasil quebrou" 1,33 mi (2,9×); BBC Brasil "como o fenômeno se tornou um desastre global" 1,47 mi (8,7×, 01/11) | reaproveita o material do 004 (1983); os 3 anos lado a lado no mapa |
| 4 | **O calor do verão do Super El Niño, no mapa** (já no backlog, id 29) | Band "Inmet emite alerta de calor extremo para 8 estados" 337 mil (26/09); Fatos Desconhecidos "El Niño pode acabar com o Brasil" 1,15 mi (6,6×) | temperatura de superfície (MODIS LST) sobre as cidades; por que o relevo muda o calor |
| 5 | **O El Niño de 2026 não é o que você pensa: o que o satélite mostra** | Sou curioso?! "O El Niño de 2026 NÃO é o que você pensa" 1,10 mi (4,6×; 6 vídeos no canal); StarTalk "The biggest El Niño in recorded history" 5,5 mi (en) | só dado de satélite NASA/NOAA em 3D, a nossa vantagem real (sem IA) |

**Riscos:**
- Tema disputado: colisão de título/thumb com Jubilut, BBC e clones. O crivo tem que ler o `refs.csv` inteiro (lição do 005).
- "Parecer notícia": "explicado", nunca flagrante; nada de imagem de TV.
- Alarmismo: probabilidade com fonte NOAA/CPC (regra da bíblia).
- O tema esfria depois de fevereiro: o prazo de 15/01 já conta com isso.

---

## Limitações
- Analytics até 25/11, Reporting até 26/11, Studio só de 14/11 (sem CTR do Studio para 003–005). Não sei qual variante do "Testar e comparar" está no ar: a Data API devolve o título A, o que pode explicar o truncado do 004, mas é preciso conferir.
- Retenção e tráfego com 24–163 views por vídeo: são direções, não conclusões.
- A buscas "este ano por views" do yt-dlp misturam vídeos fora do tema; usei só as que conferi à mão.
- RPM é **Hipótese** (faixas da fábrica, nenhum canal nosso monetizado).
- "×mediana" usa os últimos 50 uploads de cada canal.
- Custo do Claude por vídeo não está em `youtube.execucoes_claude` (0 linhas do Em Relevo); só a cota do Max, sem medida.
