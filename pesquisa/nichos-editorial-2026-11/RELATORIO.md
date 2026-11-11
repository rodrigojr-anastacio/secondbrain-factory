# Nichos para canais "editoriais" (material real + motion), 11/11/2026

Brief: `~/workspace/referencias/BRIEF-nichos-editorial.md`. Método: avaliação do `playbooks/novo-canal.md` (etapas 1–3b, sem blueprint). Custo: **US$ 0**. Cota da Data API: **~860 de 3.000 unidades** (só `videos`/`channels`/`playlistItems`; nenhuma `search.list`).
**[O]** = observado nos dados. **[I]** = inferido. **Hipótese** = sem dado.

## Resumo
| # | Nicho | Idioma | O número que justifica [O] | Referência |
|---|---|---|---|---|
| **1** | **Economia explicada com dados** ("por que X ficou rico e Y não", crises, moedas) | **en** | 28 canais com < 12 meses e longo ≥ 100 mil. TSCS: **3,1 mi views/mês** com 4 longos (mediana 605 mil). RPM é o mais alto da tabela | TSCS, Fortune of Nations Animated, Geography Effect |
| **2** | **Engenharia: "como foi construído / por que não cai"** | **en** (pt como versão) | "how does this bridge work": mediana top-10 de **2,6 mi**. Em es, o Sapiens Explica (o formato editorial exato) fez **1,6 mi/mês** com 12 vídeos | Sapiens Explica (es), Practical Engineering, Geo By Blaise |
| **3** | **Máquinas e arquivo: militar/naval/Guerra Fria, "how it actually worked"** | **en** | 210 longos ≥ 100 mil no ano. War Machine Anatomy (filme da Marinha + manual, **tudo domínio público**) fez 175 mil no 1º mês | War Machine Anatomy, Giants in Motion, Mustard |

- **Descarte mais importante: natureza/animais com stock grátis.** A demanda é a maior da tabela (mediana de 1,05 mi em en), mas o material livre não sustenta 50 vídeos. Os canais novos que crescem usam footage de origem não declarada ou IA. Banco genérico + narração é o perfil exato que a política de "conteúdo reutilizado/inautêntico" pune.
- **O que os dados mostram:** dos 12 hits recentes que assisti, só 4 usam material real com licença clara (Sapiens Explica, War Machine Anatomy, Colors of Our History, Geography Effect com stock). Os outros usam IA fotorrealista (Giants in Motion, Ocean Chronicler, CienciaX) ou são 100% motion (Fortune of Nations, Reconstructed, TSCS). [O] **O formato "arquivo público + motion" está pouco ocupado; a demanda é que não falta.**
- **Custo por vídeo:** fica entre **US$ 0,10 e 3,50 (R$ 0,50–20)**:
  - render na GPU: US$ 0,05–0,08;
  - voz: Kokoro de graça, ou ElevenLabs a ~US$ 1–3 (Hipótese);
  - imagens: US$ 0 se vierem só de fonte livre.

## 1. Tabela-resumo (notas de 0 a 5; concorrência e risco: 5 = pouca/baixo)
Demanda = mediana das medianas do top-10 das buscas centrais em en, com o nº de longos ≥ 100 mil publicados nos últimos 90 dias. Porta = canais criados há < 12 meses com longo ≥ 100 mil no nicho (proxy pela data de criação; o 1º vídeo foi conferido nos canais da seção 2). Dados: `dados/demanda_resumo.txt`.

| Nicho | Demanda en [O] | Porta en/es [O] | Concor. no formato | RPM | Material livre | Risco | Encaixe | **Nota /35** |
|---|---|---|---|---|---|---|---|---|
| **Economia com dados** | 353 mil · 102 | 28 / 10 | 3 | 5 | 4 | 4 | 5 | **30** |
| **Engenharia/megaestruturas** | 932 mil · 76 | 14 / 22 | 3 | 5 | 3 | 5 | 5 | **29** |
| **Militar/naval/Guerra Fria (arquivo)** | 675 mil · 84 | 18 / 11 | 3 | 4 | 5 | 3 | 4 | **27** (+ séc. XX) |
| Espaço (NASA/ESA) | 1,44 mi · 83 | 21 / 26 | 2 | 3 | 5 | 4 | 4 | 27 |
| Oceano profundo | 3,38 mi · 55 | 15 / 8 | 4 | 3 | 4 | 4 | 4 | 27 → Em Relevo |
| Desastres e clima | 571 mil · 56 | 18 / 13 | 3 | 3 | 4 | 3 | 5 | 26 → Em Relevo |
| Acidentes aéreos/industriais (NTSB/CSB) | 357 mil · 54 | 13 / 6 | 2 | 4 | 4 | 2 | 3 | 24 |
| Escala/comparações | 2,46 mi · 74 | 10 / 3 | 2 | 2 | 5 | 4 | 4 | 24 → recurso, não canal |
| Geopolítica | 421 mil · 29 | 5 / 2 | 2 | 4 | 3 | 2 | 5 | 23 |
| Cidades/"por que ninguém mora aqui" | 276 mil · 28 | 7 / 1 (pt: 4) | 2 | 2 | 3 | 4 | 5 | 23 → Em Relevo |
| Séc. XX/arquivo (Prelinger, NARA) | 462 mil · 31 | 11 / 7 | 3 | 3 | 5 | 3 | 3 | 23 → junta com o #3 |
| Natureza/animais (stock) | 1,05 mi · 71 | 17 / 5 | 2 | 3 | **1** | 4 | 2 | **21** ✗ |
| True crime/mistério | 913 mil · 69 | 13 / 6 | 2 | 4 | **1** | **1** | 1 | **18** ✗ |

Critérios:
- **Concorrência no formato:** quem já faz material real + motion bem feito.
- **RPM:** faixa pública do nicho.
- **Material livre:** 5 = dá para fazer 50 vídeos só com domínio público ou licença livre.
- **Risco:** anúncio limitado + "reutilizado/inautêntico".
- **Encaixe:** reaproveita Remotion, mapa 3D e GPU, e permite 3 vídeos/semana com Shorts.

**RPM (fontes públicas, faixas; Hipótese até termos o nosso):**
- Educação e ciência: mediana medida de **US$ 10,22** (AIR, 300 canais; intervalo interquartil de 2,3 a 19,5).
- Finanças e negócios: US$ 8–35.
- História e documentário: ~US$ 6–14.
- Ciência explicada: US$ 4–10.
- Fator por idioma: es ~0,25–0,4 do en (América Latina com CPM de US$ 2–8; Espanha com RPM médio de ~US$ 2,1), pt ~0,25–0,35, fr ~0,5–0,7, de ~0,8–1.
- Fontes: [air.io](https://air.io/en/air-data-findings/how-much-does-youtube-really-pay-in-2026-real-rpm-data-from-300-channels), [outlierkit](https://outlierkit.com/resources/youtube-rpm-benchmarks/), [fluxnote](https://fluxnote.io/blog/youtube-rpm-by-niche-2026), [fluxnote LatAm](https://fluxnote.io/guides/youtube-earnings-latin-america-2026).

## 2. Top 3

### #1 Economia explicada com dados (en): **TESTAR**
**Fórmula:** "Why did <país> get rich/stay poor?", "What just happened to <economia>?" e "Why <moeda> keeps collapsing". Duração de 12–20 min. Gráficos editoriais nossos sobre mapa 3D, com foto ou vídeo real esmaecido no fundo.

**Matriz de idioma** (demanda 30, concorrência 25, RPM 20, viabilidade 15, risco 10):
| Idioma | Dem | Conc | RPM | Viab | Risco | **Total** | Pesos iguais | RPM 30/Dem 20 |
|---|---|---|---|---|---|---|---|---|
| **en** | 9 | 5 | 10 | 7 | 7 | **7,70** | 7,6 | 7,80 |
| es | 7 | 7 | 4 | 7 | 7 | 6,40 | 6,4 | 6,10 |
| fr | 5 | 7 | 6 | 5 | 7 | 5,90 | 6,0 | 6,00 |
| pt | 4 | 6 | 3 | 10 | 6 | 5,40 | 5,8 | 5,30 |
| de | 2 | 7 | 8 | 4 | 7 | 5,25 | 5,6 | 5,85 |

- Notas de demanda [O]:
  - en: mediana de 353 mil, 195 longos ≥ 100 mil no ano;
  - es: 386 mil e 100;
  - pt: 162 mil e 56;
  - de: "warum ist dieses Land so arm" com mediana de 14 mil.
- **Por que o en ganha:** o RPM é ~3× o de es e há 28 canais novos com hit. Não há trava em nenhum idioma.
- **2º idioma: es como versão.** Em es há poucos canais no formato (Curiosito, Dinero Dibujado) e "por qué este país es tan rico" tem mediana de 624 mil.

**Referências [O]:**
| Canal | 1º vídeo | Views/mês | Mediana longos | Formato |
|---|---|---|---|---|
| TSCS | 16/10/2026 | 3,1 mi | 605 mil (4 longos) | gráfico editorial + foto ("WTF Just Happened to Indonesia?", 1,4 mi) |
| Fortune of Nations Animated | 02/10/2026 | 2,1 mi | 14 mil | mapa ilustrado; "Why Did the US Get Rich But Latin America Never Did?" 1,8 mi |
| Geography Effect | 19/02/2026 | 1,2 mi | 169 mil (90 d) | stock + mapa satélite + gráfico; "Why Oil Ruins Almost Every Country…" |
| Economics Explained (teto) | antigo | 4,3 mi | 552 mil | stock + gráfico |

**Diferencial nosso:**
- mapa 3D com o dado **em cima do relevo** (rotas de comércio, minas, rios), o que nenhum dos quatro faz;
- ângulo América Latina/Brasil, que é curiosidade para o público en (o hit do Fortune of Nations é justamente EUA × América Latina);
- fontes na tela.

**5 ideias:**
1. Why Argentina Keeps Going Broke: 9 Defaults on One Map
2. How Brazil Killed Hyperinflation: The Plano Real Explained
3. Why Bolivia Sits on the World's Lithium and Stays Poor
4. Why Norway Got Rich From Oil and Venezuela Didn't
5. How the Panama Canal Became a Country's Whole Economy

**Material:**
- dados: Banco Mundial (CC BY 4.0), FMI, Our World in Data (CC BY), FRED (conferir série a série; algumas são de terceiros);
- mapas: Natural Earth (domínio público), luzes noturnas da NASA Earth Observatory (PD), Copernicus;
- imagens: Library of Congress (PD), Wikimedia por arquivo, Pexels/Pixabay para o b-roll;
- filmes antigos de economia: Prelinger (Internet Archive).
- **Dá 50 vídeos?** Sim: a base é dado + mapa, que são nossos.

**Riscos:** política (Venezuela, Argentina) → tom de dado, sem partido. O b-roll genérico de banco fica abaixo de 30% do tempo.
**Testar primeiro:** a ideia 1 (Argentina) **e** a 2 (Plano Real; também rende a versão pt para o Em Relevo ou Shorts).

### #2 Engenharia: "como foi construído / por que não cai" (en, pt como versão): **TESTAR**
**Fórmula** (modelo Sapiens Explica): foto de arquivo creditada → esquema 3D da estrutura (o mesmo motor do mapa 3D) → trecho do documento técnico original com grifo → o evento que a pôs à prova (terremoto, cheia). Duração de 12–15 min.

**Matriz de idioma:**
| Idioma | Dem | Conc | RPM | Viab | Risco | **Total** | Pesos iguais | RPM 30/Dem 20 |
|---|---|---|---|---|---|---|---|---|
| **en** | 10 | 3 | 9 | 6 | 9 | **7,35** | 7,4 | 7,25 |
| pt | 5 | 8 | 3 | 10 | 9 | 6,50 | 7,0 | 6,30 |
| es | 6 | 7 | 4 | 7 | 9 | 6,30 | 6,6 | 6,10 |
| fr | 4 | 7 | 6 | 5 | 9 | 5,80 | 6,2 | 6,00 |
| de | 2 | 7 | 8 | 4 | 9 | 5,35 | 6,0 | 5,95 |

- Demanda [O]:
  - en: "how does this bridge work" 2,6 mi, "engineering explained" 1,26 mi, 180 longos ≥ 100 mil no ano;
  - pt: "por que não cai" 509 mil, com **20** longos ≥ 100 mil em 90 dias;
  - es: "por qué no se cae" 325 mil, 19 em 90 dias.
- **en ganha, mas a concorrência é 3:** Practical Engineering, The B1M, Real Engineering e Megaprojects são donos fortes. Não chega à trava porque a busca é enorme e os canais novos entram (Geo By Blaise, ponte chinesa, 3,3 mi; canal de mar/2026).
- **pt saiu em 2º, à frente de es [I]:** quase não há concorrente editorial em pt (Sobre o Passado: Cristo Redentor 335 mil com 7 vídeos). Como o RPM do pt é baixo, ele entra como versão.

**Referências [O]:**
- Sapiens Explica (es, 1º vídeo em 11/09/2026): 12 vídeos, mediana de 113 mil, 1,6 mi/mês. "¿Qué hay debajo de la Torre Latinoamericana?" 973 mil.
- CONSTRUCTUM (es): "Cómo se construyeron las Torres Gemelas" 3,2 mi.
- Echo. (fr): "Voici comment la Tour Eiffel a vraiment été construite" 977 mil.
- Practical Engineering (en, teto): mediana de 1,7 mi.
- Os es CienciaX (2,7 mi/mês) e Escala Global usam IA. **Não são o nosso formato, mas provam a demanda.**

**Diferencial nosso:**
- esquema 3D com dado real (cota, carga, nível da água) e o documento técnico na tela, o que exige pesquisa e não se faz com IA;
- estruturas latino-americanas pouco cobertas em en (Itaipu, Rio-Niterói, Canal do Panamá).

**5 ideias:**
1. Why Hoover Dam Hasn't Cracked in 90 Years
2. How the Golden Gate Survives Earthquakes
3. Why Mexico City Is Sinking 50 cm a Year
4. Itaipu: How Two Countries Built One Dam
5. How the Panama Canal Lifts Ships Over a Mountain

**Material:**
- **HAER/HABS da Library of Congress** (domínio público; desenhos medidos e fotos de Hoover, Golden Gate, Brooklyn Bridge);
- USBR e USACE (PD), patentes (PD);
- Prelinger, com filmes de obra dos anos 1930–60;
- fotos do Canal do Panamá de antes de 1930 (PD por idade, conferir);
- Wikimedia por arquivo;
- para estruturas fora dos EUA: Wikimedia + **pedido de licença por e-mail** (Itaipu Binacional e prefeituras costumam liberar com crédito; Hipótese).
- **Dá 50 vídeos?** Sim para os EUA e as estruturas antigas; fora disso o material fica mais apertado.

**Riscos:**
- esforço de esquema 3D por vídeo (o maior dos três): mitigar com uma biblioteca de peças (bloco de solo, água, pilar, cabo);
- não usar Google Earth/Maps (a licença limita).

**Testar primeiro:** a ideia 1 (material 100% PD) e a 4 (ângulo BR, que vira versão pt).

### #3 Máquinas e arquivo: militar/naval/Guerra Fria, "how it actually worked" (en): **TESTAR**
**Fórmula:** "How <máquina> actually worked". Filme de treinamento ou arquivo do governo dos EUA + diagrama do manual animado + corte 3D nosso. Duração de 15–25 min. Absorve "século XX com arquivo" (corrida espacial, Guerra Fria) sem misturar com o `dossie-es` (que é organização/serviço secreto em capítulos-EXPEDIENTE) nem com o `historia-ptbr`.

**Matriz de idioma:**
| Idioma | Dem | Conc | RPM | Viab | Risco | **Total** | Pesos iguais | RPM 30/Dem 20 |
|---|---|---|---|---|---|---|---|---|
| **en** | 9 | 5 | 7 | 9 | 6 | **7,30** | 7,2 | 7,10 |
| fr | 4 | 7 | 6 | 5 | 6 | 5,50 | 5,6 | 5,70 |
| es | 5 | 7 | 3 | 6 | 6 | 5,35 | 5,4 | 4,95 |
| pt | 4 | 7 | 3 | 7 | 6 | 5,20 | 5,4 | 4,90 |
| de | 2 | 7 | 8 | 4 | 4 | 4,95 | 5,0 | 5,55 |

- Demanda [O]:
  - en: "nuclear submarine explained" 2,25 mi, "aircraft carrier explained" 1,42 mi, "military documentary" 1,14 mi, 84 longos ≥ 100 mil em 90 dias;
  - es/pt/fr: medianas de 117–266 mil.
- **en ganha folgado.** O material está em inglês e é do governo dos EUA, o que eleva a viabilidade. Em de, o risco é maior (§86a no material da 2ª Guerra).

**Referências [O]:**
- War Machine Anatomy (1º vídeo em 14/10/2026): 9 longos, mediana de 28 mil, 426 mil/mês; filme da Marinha + manual.
- Giants in Motion (12/10/2026): 1,5 mi/mês, IA.
- The Colors of Our History: arquivo colorizado, 1,2 mi.
- Exploded Works: submarino em 3D, 201 mil.
- Teto: Mustard (mediana de 6,4 mi, mas 1 vídeo por trimestre) e Real Engineering.

**Diferencial nosso:** arquivo PD **com narração e análise** (não só arquivo restaurado), diagrama de manual animado e o mapa 3D da operação.

**5 ideias:**
1. Project Iceworm: The Secret Nuclear City Under Greenland's Ice
2. How the SR-71 Outran Every Missile Fired at It
3. Operation Crossroads: Nuking a Fleet on Purpose
4. How an Aircraft Carrier Stops a Jet in Two Seconds
5. The Mechanical Computer That Aimed a Battleship

**Material:**
- **DVIDS** (o FAQ diz que, em geral, o conteúdo é domínio público; conferir a etiqueta de cada clipe: [FAQ](https://dvidshub.net/about/faq));
- NARA (filmes do governo, PD);
- Naval History and Heritage Command (fotos PD);
- NASA (SR-71 do Dryden, PD);
- filme do Exército "Camp Century" (PD);
- manuais da Marinha dos EUA (PD, ex.: *Naval Ordnance and Gunnery*);
- **não usar:** Imperial War Museum (licença não comercial) nem trechos de documentário de TV.
- **Dá 50 vídeos?** Sim: é o nicho com mais material PD de todos.

**Riscos:**
- anúncio limitado em cena de combate e morte → foco em máquina e engenharia, sem cena gráfica;
- **o arquivo PD pode levar claim de terceiros** que reenviaram o mesmo filme (há relato de vídeo com material DVIDS desmonetizado: [Ryan McBeth](https://ryanmcbeth.substack.com/p/youtube-demonetized-my-air-assault)) → `licencas.md` com o link da fonte oficial e disputa pronta.

**Testar primeiro:** a ideia 1 (Camp Century é PD e pouco coberto) e a 4 (DVIDS).

### Critério para os três (igual ao do Em Relevo, adaptado)
3 longos + 6 Shorts em 30 dias.
- **INVESTIR:** média ≥ 5 mil views em 14 dias **ou** 1 vídeo ≥ 30 mil, com ≥ 40% assistido e CTR ≥ 4%.
- **DESCARTAR:** média < 1,5 mil e nenhum vídeo > 5 mil.

## 3. Descartar
| Nicho | Por quê [O]/[I] |
|---|---|
| **Natureza/animais com stock** | O material livre (Pexels/Pixabay) é genérico e não cobre comportamento animal em 50 vídeos. Os canais que crescem (GaiaDocs 4,3 mi/mês; Nature's Tether, com mediana de 1,7 mil fora dos hits) usam footage de origem não declarada. É o perfil de "reutilizado" |
| **True crime/mistério** | O nicho vive de bodycam/interrogatório de terceiros (Red File, DOCS 187, Miranda Interrogations) e de material sem licença livre. O anúncio fica limitado por violência. Não há como fazer "arquivo público + motion" |
| **Acidentes aéreos (agora)** | Corrida do ouro do Learjet: 6+ canais criados em out/2026 (Reconstructed, Rewynd3D, TALEYE, reci, Fault Lines, SEGUNDO A SEGUNDO 3D). É efêmero, tem morte e tem dono forte (Mentour Pilot, mediana de 1,1 mi). **Reavaliar em 6 meses** com o ângulo industrial (animações da CSB, PD; USCSB com mediana de 589 mil) |
| **Escala/comparações** | A demanda é enorme (mediana de 2,5 mi en, 6,4 mi es), mas é público infantil (RPM baixo) e o formato é só 3D, sem material real. **Usar como recurso** dentro dos outros canais e nos Shorts |
| **Geopolítica pura** | Johnny Harris e RealLifeLore donos (medianas de 1,4–3,7 mi), risco político alto. A parte econômica entra no #1 |
| **Espaço (por enquanto)** | O melhor material do mundo (NASA, PD), mas en/es estão inundados de "James Webb just found…" feito com IA (Cosmicus com 81 longos em 90 dias; Proof). **Fica como 4º.** Se um dos três falhar, es é o caminho (Astrovía: 105 mil inscritos desde fev/2026, mediana de 288 mil nos 90 dias) |

## 4. O Em Relevo (pt-BR) pode absorver sem canal novo
- **Desastres e clima:** já é o núcleo do canal.
- **"Por que ninguém mora em <lugar>?" / geografia do Brasil:** Explica no Mapa (pt, 18 dias) fez 5,1 mi/mês; Mundo Entrópico tem mediana de 57 mil. É o mesmo mapa 3D. O pt está cheio de clones desde out/2026, então só com o relevo 3D como diferencial.
- **Obras contra o relevo** (Serra do Mar/Imigrantes, Itaipu, transposição do São Francisco, Rio-Niterói): "por que não cai" em pt teve 20 longos ≥ 100 mil em 90 dias. Também servem de **versão pt dos episódios do #2.**
- **Oceano e batimetria em 3D** (Fossa das Marianas, plataforma continental, pré-sal): a demanda é a maior da tabela (en 3,4 mi; pt 511 mil) e o material é da NOAA Ocean Exploration (PD) + GEBCO. Fica fora dos três canais novos porque cabe direto no mapa do Em Relevo.
- **Não absorver:** economia, militar e espaço. Mudariam a promessa do canal ("o Brasil e o planeta em relevo").

## 5. Regras de material e monetização (valem para os três)
- **≥ 70% do tempo de tela em material nosso** (gráfico, mapa, esquema 3D, documento grifado); o material real entra citado, com crédito na tela e `licencas.md` por vídeo (regra do Em Relevo, `pesquisa/canal-clima-2026-11/RELATORIO.md` §4).
- Desde 15/07/2025, a política de "repetitivo" do YPP chama-se **"inautêntico"** e mira produção em massa. O que torna o vídeo transformador: roteiro próprio com tese, narração, dado e mapa nossos, e nunca um clipe longo sem análise. Cadência de 3/semana **por canal**, não 3/dia.
- **Nunca:** TV, trecho de documentário ou filme, vídeo viral sem licença, IWM, Google Earth.
- PD não evita o Content ID de terceiros: guarde o link da fonte oficial de cada clipe para a disputa.

## 6. Encaixe com a fábrica
- **Os três reaproveitam:** Remotion + mapa 3D + render na GPU (Runpod, ~5 min por vídeo de 12 min), voz Kokoro/ElevenLabs en e roteiro em Opus.
- **Esforço por canal:**
  - #1: gráficos e mapas, componentes reutilizáveis, **o mais barato de escalar**;
  - #3: pesquisa de arquivo (DVIDS/NARA) e corte 3D;
  - #2: esquema 3D por estrutura, **o mais caro** (biblioteca de peças primeiro).
- **Shorts:** 2–3 por longo (um número ou uma comparação de escala por Short).
- **Cadência realista:** 3/semana num canal novo só depois do teste. No teste, 1 longo/semana por canal, para não brigar com os 3 canais atuais.

## Limitações
- O RPM é faixa pública, não dado nosso.
- "Porta aberta" usa a data de criação como proxy. Canais com 2–4 semanas (TSCS, STRABO, War Machine Anatomy) têm views/mês infladas pelo arranque.
- A busca do YouTube personaliza pouco via WARP, mas a mediana top-10 oscila com a consulta. Por isso uso 5–9 consultas por nicho em en e 2–4 por idioma.
- Assisti a 12 vídeos (sem ver o TikTok/Instagram). A licença de cada fonte deve ser conferida arquivo a arquivo antes de produzir.

## Arquivos
- `scripts/`:
  - `buscar.py`: 753 consultas yt-dlp via WARP, 0 cota;
  - `enriquecer.py`: Data API;
  - `demanda.py`;
  - `canais.py`: 72 canais com uploads;
  - `gravar_garimpo.py`: 23 canais gravados em `youtube.garimpo_canais` com `formula`/`decisao`.
  - Para rodar de novo, faça `gunzip dados/*.gz` antes.
- `dados/`: `busca.jsonl.gz` (13.497 resultados), `videos_api.json.gz` (10.652), `canais_api.json.gz` (6.591), `canais_nicho.json`, `demanda.json`, `demanda_consultas.json`, `demanda_resumo.txt`.
- Vídeos assistidos (assets fora do git, em `pesquisa/tendencias/assets/2026-11-11/`): vgGjB22MAqA (Giants in Motion, IA), GD7x6sXMnNI (Fortune of Nations, mapa motion), OlCQZbYGVtk (Astrovía, NASA/CGI), s7WaBHkgjL0 (Reconstructed, 3D branco), xInAqXmBSxQ (Sapiens Explica, arquivo + esquema 3D), t5tForUF5tg (Colors of Our History, arquivo colorizado), 21-G0C_bXYI (TSCS, gráficos editoriais), _7UOP44SWkU (Geography Effect, stock + mapa), dBl2w_R7e-s (Ocean Chronicler, IA), bSdMIWLgsX0 (CienciaX, IA), j2d3N06nJ5A (Cimientos de Lujo, motion + vídeo real), Jos1uve7idI (War Machine Anatomy, arquivo da Marinha + manual).
- Hooks literais [O]:
  - Sapiens: "La mitad del peso de la Torre Latinoamericana la sostiene el agua";
  - War Machine Anatomy: "The armor-piercing shell for an American 16-inch battleship gun weighs 2,700 pounds";
  - Fortune of Nations: "In January, silver hit the highest price in its history, and the mountain that once produced nearly half of all the silver on Earth isn't in a rich country";
  - TSCS: "On Friday, Indonesia's stock market had its worst day since 1998".
  - Padrão: **número concreto + paradoxo** nos primeiros 10 s.
