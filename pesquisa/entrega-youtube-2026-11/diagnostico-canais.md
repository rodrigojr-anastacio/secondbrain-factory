# Diagnóstico dos canais (11/11/2026): por que o Em Relevo não recebe impressões

Só leitura: Data API (223 unidades), YouTube Analytics API, yt-dlp via WARP. Nada foi alterado no YouTube, no banco, em `canais/` nem em `tools/`. Dados brutos (sem token): `dados/diagnostico.json`.
Legenda: **[O]** observado na API/página · **[I]** inferido.

## Suspeitos para as 7 impressões do Em Relevo (do mais provável ao menos provável)

| # | Suspeito | Evidência | Como testar |
|---|---|---|---|
| 1 | **Canal reaproveitado "frio" e com histórico de outro tema**: o YouTube não tem com quem testar o vídeo (sem audiência-semente, canal sem tópico) | [O] 0 views de Navegação (home) e 0 de Sugeridos; só 2 de Busca. [O] `topicDetails` do canal vazio (os outros têm Knowledge/Society). [O] Histórico: 746 views na vida toda, pico em abr/2026 (381) e mai/2026 (154), depois 7–9 por mês. [O] Os 6 inscritos vieram do conteúdo antigo. [I] O historia-ptbr também é reaproveitado (2023), mas estava **limpo** (0 vídeos, 2 views) e recebeu home e sugeridos desde o 1º vídeo | Studio: tema e público dos vídeos antigos (Conteúdo, filtro Visibilidade); Analytics > Público (inscritos interessados em quê?); comparar impressões das primeiras 48 h do Egito (historia) com as do vídeo 1 |
| 2 | **Restrição ou aviso no próprio canal** (strike, aviso de diretrizes ou "conteúdo reutilizado" herdado da fase antiga), que limita a distribuição | [I] Uma queda brusca depois do pico de abr–mai/2026 combina com isso, mas a API não mostra avisos. [O] `longUploadsStatus=allowed` (telefone verificado), canal público, `madeForKids=false` | Studio > Configurações > Canal > **Qualificação de recursos** ("Status e recursos") e Studio > **Monetização**; e-mails do YouTube Studio na conta |
| 3 | **Tema de notícia ou tragédia** (tornados com vítimas): na busca e na home o YouTube dá prioridade a fontes de autoridade (CNN, emissoras) em notícia de última hora | [O] search.list (região BR, pt) com o título exato: o vídeo 1 **não aparece no top 50**; o vídeo 2 aparece em 33º. [O] yt-dlp: título exato → vídeo 1 em 2º, vídeo 2 em 1º; "tornados sul do brasil", "7 tornados em 6 dias…", "super el niño brasil verão" → **fora do top 20**. [O] O top da busca é de canais grandes ou de notícia. [O] A única busca registrada que trouxe view foi "o que está acontecendo no brasil" | Studio > Analytics do vídeo 1 > Alcance > Fontes de tráfego > Pesquisa no YouTube; comparar com o vídeo 2 (El Niño é menos "tragédia") depois de 48 h e 7 dias |
| 4 | **Reivindicação de direitos autorais (Content ID ou manual) no vídeo 1** (33 trechos de outros youtubers) | [O] Para quem não é dono, a API mostra `licensedContent=false`, sem `regionRestriction` e sem `contentRating`; reivindicações só aparecem no Studio. [O] O vídeo 2 não tem trecho de vídeo de terceiros (só fotos CC/domínio público). [I] Uma reivindicação costuma tirar a monetização, não as impressões, a menos que bloqueie | Studio > Conteúdo > coluna **Restrições** do vídeo 1 (passe o mouse: "Reivindicação de direitos autorais"); detalhes do vídeo > Direitos autorais |
| 5 | **Título publicado genérico e diferente do planejado** | [O] O vídeo 1 foi ao ar como "**O que está acontecendo com o clima no Sul do Brasil?**" (G26KHotlMIw), sem a palavra "tornado", e não como "7 tornados em 6 dias…". [O] Tags e descrição falam de tornado. [I] Isso pesa na busca, mas não explica 0 impressões na home | Studio > Analytics do vídeo > CTR das impressões; buscar de novo daqui a 7 dias |
| 6 | Metadados de idioma e legenda | [O] Idioma do título e da descrição = **pt-PT** nos dois vídeos (áudio pt-BR); o vídeo 1 **não tem legenda enviada** (`caption=false`); o vídeo 2 tem legenda pt-BR. [O] O historia-ptbr tem pt-PT no Egito e na Índia e mesmo assim recebe tráfego, então isso **não é o diferencial** | Studio > Detalhes do vídeo > Idioma e legendas |
| 7 | Descrição com 22 links (vídeo 1) | [O] 4.120 caracteres e 22 URLs (créditos de outros vídeos do YouTube). Nos outros canais: 0–3 links. [I] É pouco provável que conte como spam | Nenhum teste direto; observar o vídeo 2 (0 links) |
| ✗ | Feito para crianças / restrição de idade / bloqueio por região / Shorts / ao vivo | **Descartados** [O]: `madeForKids=false` (canal e vídeos), `contentRating` vazio, `age_limit=0`, sem `regionRestriction`, `availability=public`, `live_status=not_live`, embed liberado. (`selfDeclaredMadeForKids` só aparece para o dono: confirmar no Studio) | Studio > Configurações > Canal > Configurações avançadas |

**Leitura do número:** [O] o vídeo 1 tem 2 views, as duas de Busca, ambas no celular, de não inscritos, com **0 minutos assistidos** (saída imediata). [I] As 7 impressões não indicam problema de CTR: o problema é de **distribuição**, porque o YouTube quase não mostrou o vídeo. As ~11 impressões do vídeo 2 em poucas horas ainda não dizem nada; a janela útil é de 48 h a 7 dias.

## 1. Quem é quem

| Canal | channel_id | handle | criado | país | inscr. | views (públ.) | vídeos públ. |
|---|---|---|---|---|---|---|---|
| historia-ptbr | UCpw08sVZG1QZp-3spPcwWxQ | @historiaem-min | 01/08/2023 | BR | 10 | 527 | 6 |
| dossie-es | UCVCYqeuCwTWC7Lqez_qeWRA | @dossierenminutos | 04/11/2026 | BR | 2 | 321 | 5 |
| lotr-fr | UCAtDNhMNd7EDuFHswOpx9EQ | @legardiendevalinor | 29/12/2023 | — | 292 | 28.167 | 7 |
| **Em Relevo** | **UCKoQhYctv1sAwTM0Rl1H9SA** | **@emrelevobr** | 13/01/2024 | BR | 6 | 2 | 2 |
| (homônimo) Em Relevo | UCwSVU81y3l-H-EHGR8Yv9cQ | @emrelevo | 25/06/2026 | — | 2 | 90 | 2 |

- [O] O token `rodrigo-pessoal` (canal "Rodrigo", UC3nq…, 0 vídeos públicos e 6 Shorts "Bigfoot" não listados de 2025) **consegue ler o Analytics do Em Relevo**, então a conta Google é dona/gerente do canal. Pela Data API, `mine=true` só devolve o canal "Rodrigo", e por isso não dá para ver os vídeos privados do Em Relevo.
- [O] O homônimo @emrelevo tem a descrição "Um número, um mapa, um porquê… dado do IBGE vira mapa em relevo" (2 vídeos de 06/10/2026, cat. 22). [I] Pode ser outro projeto do próprio Rodrigo ou de outra pessoa; de qualquer forma, ele divide a busca pela marca "Em Relevo". **Perguntar.**
- IDs sem dono no banco: [O] `3TwMYoxnF4k` = Rússia (historia, privado, agendado para 13/11 10:30 BRT); `DBLonwmeQ7c` = Masones (dossie, privado, agendado para 13/11 18:00 BRT); `I_ehrH5Yrak` = KGB (dossie, público 11/11); `fkltw3XwQ0E` = Roma (historia, público 11/11); `gmA0LkJqf_U` = Cosa Nostra (dossie, público 09/11). `jpCpnhSxo7A`, `s-D5Sk7prJI` e `z8bBpEV3V4Q` **não voltam na API** ([I] foram apagados; coletados só em 02–03/11, quando havia token apenas de historia-ptbr e lotr-fr, então vieram de um desses dois).
- [I] O banco está atrasado: em `youtube.videos`, Roma, Rússia, KGB, Masones, Cosa Nostra e Em Relevo 2 estão sem `youtube_id`/status, e falta o vídeo 1 do Em Relevo. A tabela `canais` está sem o channel_id do Em Relevo. Não alterei nada (só leitura).

## 2. Configuração do canal (channels.list)

| Campo | historia | dossie | lotr | Em Relevo |
|---|---|---|---|---|
| madeForKids (canal) | false | (vazio) | false | false |
| privacyStatus / isLinked | público / sim | público / sim | público / sim | público / sim |
| longUploadsStatus | allowed | allowed | allowed | allowed |
| país (snippet/branding) | BR | BR | — | BR |
| defaultLanguage do canal | — | — | — | — |
| keywords do canal | — | — | — | — |
| topicDetails | Knowledge | Knowledge, Politics, Society… | Knowledge, Entertainment | **vazio** |
| monetização | não | não | não | não |
| contentOwnerDetails | — | — | — | — |

[O] Na configuração, a única diferença do Em Relevo é o `topicDetails` vazio ([I] o YouTube ainda não classificou o canal, o que combina com o suspeito 1).

## 3. Vídeos (videos.list), configuração por canal

| | historia (7) | dossie (6) | lotr (10) | Em Relevo (2) |
|---|---|---|---|---|
| categoria | 27 Educação | 27 | 1 Filmes (1 antigo em 22) | 27 |
| idioma título / áudio | pt-PT (antigos) e pt-BR (novos) / pt-BR | es / es | fr (2 em pt-PT) / fr | **pt-PT / pt-BR** |
| legenda enviada | todas | todas | nenhuma | **v1 não**, v2 sim |
| licença / embed / stats públicas | youtube / sim / sim | igual | igual | igual |
| licensedContent / regionRestriction / ytRating | false / — / — | igual | igual | igual |
| madeForKids | false | false | false | false (selfDeclared oculto) |
| definição | hd | hd | hd | hd |
| tags | 18–23 | 15–21 | 30 | 19 / 16 |
| descrição (caracteres / links) | 976–2.606 / 0 | 1.916–3.021 / 0–3 | 0–1.621 / 0 | **4.120 / 22** · 2.419 / 0 |
| traduções de título | en-US, es-US | es | fr, en-US | pt-PT, es-US, en-US / en-US, pt-PT |

### Em Relevo: vídeos públicos
| ID | Publicado (BRT) | Título no ar | Dur. | Views | Legenda | Observação |
|---|---|---|---|---|---|---|
| G26KHotlMIw | 09/11 10:10 | O que está acontecendo com o clima no Sul do Brasil? | 10:23 | 2 | não | 33 trechos de outros youtubers, 10 capítulos |
| YqNMNhFCPpM | 11/11 12:15 | Super El Niño: o que ele vai fazer com o Brasil neste verão? | 12:10 | 1 | pt-BR | só fotos CC/domínio público, 12 capítulos |

- [O] Na página (yt-dlp): `age_limit 0`, `availability public`, categoria Education, `language pt-BR`, legendas automáticas disponíveis. Sem sinal de aviso ou restrição.
- [O] Pela WARP (IP fora do BR), o vídeo 2 aparece na busca com o título em inglês ("Super El Niño: what will it do to Brazil this summer?"), por causa da tradução en-US.

### Outros canais: referência de views (11/11)
historia: Egito 325 · Índia 184 · Brasil 27 · China 25 · Irã 10 · Roma 0 (hoje) · Rússia privado. dossie: Mossad 299 · CIA 58 · FBI 29 · KGB 4 (hoje) · Cosa Nostra 3 · Masones privado. lotr: Orcs 16.303 · Frodon 7.153 · Anneau 1.979 · Nazgûl 1.745 · Moria 526 · Legolas 412 · Villes (2026) 63 · 3 não listados.

## 4. Tráfego (Analytics, 01–11/11)

| Fonte | historia | dossie | Em Relevo |
|---|---|---|---|
| Navegação (home/inscrições) | **174** | 21 | **0** |
| Sugeridos | **169** | **205** | **0** |
| Busca no YouTube | 19 | 23 | 2 |
| Outras | 19 | 32 | 1 (playlist, 04/11) |
| País | BR 100% | ES, AR, MX, CL, CO | (sem dado) |

- [O] Em Relevo em novembro: 3 views (todas no celular, de não inscritos, na página de exibição). A view de **04/11** veio de playlist **antes** de existir vídeo público ([I] um vídeo antigo privado ou não listado dentro de uma playlist, ou o próprio dono).
- [O] Impressões e CTR **não vêm pela API** (`videoThumbnailImpressions` → erro 400 nos 3 canais). Retenção do vídeo 1: sem dado (volume baixo).

## 5. Histórico do canal reaproveitado (Analytics, por mês)

| Período | Views | Min. assistidos | Inscritos +/− |
|---|---|---|---|
| jan–fev/2024 | 7 | 15 | 0 |
| out–dez/2024 | 18 | 40 | 0 |
| 2025 (10 meses com view) | 40 | 67 | 0 |
| jan–mar/2026 | 67 | 251 | +2 |
| **abr/2026** | **381** | **1.278** | +3 |
| mai/2026 | 154 | 423 | +3 / −1 |
| jun–out/2026 | 76 | 178 | −1 |
| **Vida toda** | **746** | — | **+8 / −2** |

- [O] Hoje nenhum vídeo antigo é público (`videoCount` = 2, os dois novos), e o relatório por vídeo de 2024–2025 vem **vazio**. [I] Os vídeos antigos foram apagados ou estão privados. Título, tema e data do último upload antigo **não aparecem na API**; precisa do Studio.

## 6. O que pedir ao Rodrigo no YouTube Studio (canal Em Relevo)

1. **Conteúdo > Vídeos** (sem filtro de visibilidade): print da lista inteira com as colunas **Visibilidade, Restrições, Data, Visualizações**. Mostra os antigos privados (título, tema, data do último upload) e se há "Reivindicação de direitos autorais" ou "Restrição de idade".
2. Vídeo 1 > **Detalhes > Direitos autorais / Verificações**: há reivindicação? De quem? Bloqueia ou só monetiza?
3. **Configurações > Canal > Configurações avançadas**: público ("Não é feito para crianças"), país e status de conteúdo alterado/sintético. **Configurações > Canal > Qualificação de recursos**: status e recursos (avisos, strikes, recursos intermediários e avançados).
4. **Monetização**: status do canal, ou aviso de "conteúdo reutilizado" da fase antiga.
5. **Analytics > Alcance** (vídeo 1 e vídeo 2, 48 h e 7 dias): Impressões, CTR das impressões, "Como os espectadores encontram seus vídeos" e **"Origens de tráfego de impressões"** (onde as 7 impressões apareceram: busca? home?). Fazer o mesmo no **Egito (historia)** nas primeiras 48 h, para comparar.
6. **Analytics > Alcance > Fontes de tráfego: Pesquisa no YouTube**: os termos (vídeo 1).
7. **Analytics > Engajamento**: retenção dos primeiros 30 s (vídeo 1 e vídeo 2) e duração média.
8. **Analytics > Público**: "O que seu público assiste" e "Canais que seu público assiste" (mostra se o público antigo é de outro tema).
9. **Analytics > Avançado** (desde o início): visualizações por vídeo, para recuperar a lista dos antigos e as views de abr–mai/2026.
10. Confirmar: o canal homônimo **@emrelevo** (UCwSVU…) também é dele?
11. Se ele quiser, rodar `tools/auth.py em-relevo` escolhendo o canal Em Relevo, para a API ler os privados e entrar na coleta diária (decisão dele; login feito por ele).

## 7. Conclusão provisória
- [O] A configuração técnica do Em Relevo é praticamente igual à dos canais que recebem tráfego (não é feito para crianças, sem restrição, categoria 27, público, BR). O que difere: **0 tráfego de home e de sugeridos**, canal sem tópico, histórico de outro conteúdo apagado, vídeo 1 com trechos de terceiros e sem legenda, título genérico em tema de notícia.
- [I] A hipótese mais provável é a soma de 1 + 3: um canal sem sinal de audiência para clima, estreando com notícia de tragédia, onde o YouTube favorece fontes de autoridade. Os itens 2 e 4 (aviso no canal, reivindicação) se resolvem em 2 minutos no Studio (itens 1–4 da seção 6) e precisam ser descartados antes de qualquer decisão, como abrir um canal novo.
- Teste natural: o **vídeo 2** (sem trecho de terceiros, legendado, tema menos "breaking"). Se em 48 h–7 dias ele também não passar de algumas dezenas de impressões sem home e sem sugeridos, o problema é o canal (1 ou 2), não o vídeo 1.
