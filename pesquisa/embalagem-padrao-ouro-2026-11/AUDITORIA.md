# Auditoria das embalagens no ar contra a RUBRICA (17/11/2026)

21 vídeos publicados (historia-ptbr 9, dossie-es 8, Em Relevo 4), par no ar = título ao vivo (videos.list) + thumb no ar (maxres via WARP), cada um testado na grade com 11 concorrentes do tema a 160×90 e 320×180 (`grades/`). CTR = acumulado do `youtube.alcance_diario` até 14/11, que **mistura** a embalagem antiga com a da reembalagem de 14/11 (poucas impressões depois da troca): por vídeo, tudo é **Hipótese**.

## Resumo
| Canal | Vídeos | Nota média /100 | Aprovados (≥ 75, nenhum < 6, T2/H1/P1 ≥ 7) | Pior critério (média) | Defeito recorrente |
|---|---|---|---|---|---|
| historia-ptbr | 9 | **65,0** | 1 (Roma, 84) | T2 lacuna 5,1 · P1 5,8 | título-rótulo/fórmula (Índia, China, França, Alemanha) e thumb que vende outra pergunta |
| dossie-es | 8 | **51,4** | 0 | **P1 2,9** · T2 4,0 | a SIGLA gigante da thumb repete a sigla do título em 8 de 8 (vem do layout da bíblia); título-rótulo "TODA la historia…" |
| Em Relevo | 4 | **54,8** | 0 | T1 concretude e T2 (média 4,25) · H3 ≤ 5 | mapa escuro sem nada em alerta; pergunta vaga ou sim/não |
| **Fábrica** | **21** | **57,9** | **1 de 21** | **P1 + T2** | **título e thumb não formam uma pergunta só: a thumb repete o título (sigla/nome do país) ou vende outra coisa, e o título é rótulo sem lacuna** |

- **Nota × CTR:** dossie-es e Em Relevo andam na mesma direção (Em Relevo 52 → 2,67% e 49 → 1,55%), mas com < 400 impressões. No historia-ptbr a correlação com o CTR acumulado é ~0 (−0,08) porque as impressões são da embalagem antiga; só no dia 14/11 (pós-troca) foi 0,74 em 6 vídeos (1 dia, 1.556 impressões). Recalibrar com 7 dias e ≥ 1.000 impressões por vídeo.
- **Achados urgentes (fora do escopo, sem alterar nada):** (1) Em Relevo 003 está no ar com "matou" no título e "500 MIL" (mortos) na thumb, contra a bíblia e `conhecimento/politicas-youtube.md`; troca mínima sugerida em `ANTES-DEPOIS.md`. (2) O `youtube.txt` da França (historia-ptbr 008) traz "matou" no título B do "Testar e comparar"; não está no ar, mas não pode subir.

## Auditoria de embalagem: historia-ptbr contra a RUBRICA (17/11/2026)

Régua: `RUBRICA.md` (10 critérios de 0 a 10; aprova com total ≥ 75, nenhum critério < 6 e T2, H1 e P1 ≥ 7). Avaliei o par **no ar**: o título ao vivo (`corpus/nossos.csv`) com a thumb no ar (`thumbs/nossos/historia-ptbr-*.jpg`). Olhei as duas grades de cada vídeo (`grades/historia-00N-160.jpg` e `-320.jpg`, a nossa na linha 2 × coluna 2, entre 11 concorrentes do tema).
Portões: nenhum título ao vivo tem palavra proibida e nenhuma thumb mostra sangue ou morto. Todas seguem a bíblia (bonequinhos, Libre Caslon + Open Sans, ouro #F7C21B). A exceção parcial é o 007, só com mapa e sem personagem, desvio que a bíblia já registra como 3º estilo. **010 Japão (`PjJZHj9Smr8`): indisponível, fora da auditoria.**
Achado lateral: o `youtube.txt` do 008 traz no braço B do "Testar e comparar" o título "Por que a França **matou** o rei e nunca viveu sem um?". "Matou" é palavra proibida (`conhecimento/politicas-youtube.md`). Não está no ar, mas não pode subir.

### Fichas

**001 Egito** · "Como um RIO manteve o Egito vivo por 7.000 anos" (47 caracteres) + Cleópatra surpresa, pirâmide lisa e Esfinge, "JÁ ERA ANTIGA", pílula "2560 a.C. · 30 a.C."
T1 9: um agente concreto e estranho (o rio) carrega o título. | T2 7: o "como?" é claro, mas genérico. | T3 10: 47 caracteres, 1 ideia. | T4 8: o "Como [agente] [verbo] [lugar]" é provado e não está na grade. | T5 8: 7.000 anos e "vivo" mostram escala.
H1 7: em 5 palavras, "Cleópatra espantada diante da pirâmide antiga"; 1 foco + pirâmide, com colunas e Esfinge sobrando. | H2 7: o rosto lê a 160; o texto lê, mas "ANTIGA" branco sobre areia clara perde contraste. | H3 7: o espanto está lá, mas a causa é intelectual. | H4 4: na grade há mais 3 Cleópatras e 5 pirâmides em tom quente; a nossa é mais uma. | P1 6: a thumb vende "Cleópatra está mais perto de nós que das pirâmides" e não o rio; só ecoa a ideia de tempo.
**Total 73 → REPROVADO** (abaixo de 75; H4 e P1 abaixo do mínimo) · Defeito: thumb igual à grade (Cleópatra + pirâmide) e desligada do rio do título.

**002 Índia** · "5.000 ANOS de Índia em 19 minutos" (33) + duelo CHUVA × CANHÃO, 1757
T1 3: rótulo com número. | T2 2: não há pergunta, é catálogo. | T3 10: 33 caracteres. | T4 5: é a fórmula dos clones (Knowledgia "A HISTÓRIA DA ÍNDIA em 12 minutos", BTN "A História COMPLETA da Índia"). | T5 7: número grande, mas é o número dos clones.
H1 8: "britânico seco contra indiano encharcado", 1 foco (o duelo). | H2 9: os 2 rostos e as 2 palavras leem a 160. | H3 9: duelo com a causa visível (chuva × pólvora). | H4 7: é a única ilustração da grade, mas repete o molde duelo + raio do Irã, o vizinho no canal. | P1 5: "5.000 anos" e "chuva × canhão" prometem coisas diferentes; a batalha só aparece aos 10:42.
**Total 65 → REPROVADO** (T1, T2 e P1 abaixo do mínimo) · Defeito: título-rótulo sem lacuna em cima de uma das melhores thumbs do canal.

**003 Irã** · "Por que a Pérsia virou Irã e NUNCA virou árabe?" (47) + COROA × TURBANTE, 1891 · 1979
T1 7: nomes concretos, mas esperados. | T2 7: o 2º elemento ("nunca virou árabe") salva a pergunta crua. | T3 8: 47 caracteres, 2 ideias encadeadas. | T4 6: "Por que a Pérsia virou Irã" tem 8 cópias em pt, e a grade traz "Por qué Persia cambió su nombre a Irán". | T5 7: há transformação e regra quebrada.
H1 7: duelo, mas a multidão vermelha e os azulejos carregam o fundo. | H2 8: lê bem a 160. | H3 9: raiva cara a cara. | H4 6: a grade tem 2 fotos de Khomeini e a nossa repete o molde da Índia. | P1 4: o título pergunta sobre nome e identidade; a thumb vende a revolução de 1979, outra pergunta.
**Total 69 → REPROVADO** (P1) · Defeito: o título pergunta uma coisa e a thumb vende outra.

**004 China** · "3.000 ANOS de China em 16 minutos" (33) + Qin com medo segurando a esfera de mercúrio, "IMORTAL?", 210 a.C.
T1 3: rótulo. | T2 2: sem pergunta. | T3 10: 33 caracteres. | T4 5: fórmula de clone (BP "5000 ANOS EM 1 HORA" está na própria grade). | T5 6: o número é menor que o do concorrente ao lado (3.000 × 5.000).
H1 7: imperador + esfera, com o exército de barro de apoio. | H2 7: a thumb é escura; o rosto e "IMORTAL?" leem, a esfera fica pequena. | H3 8: medo diante da pílula, desfecho pendente. | H4 7: única ilustração entre fotos de Mao e Xi em vermelho. | P1 7: "IMORTAL?" completa sem repetir, mas o título não faz pergunta nenhuma.
**Total 62 → REPROVADO** (T1 e T2) · Defeito: título-rótulo; a lacuna só existe na thumb.

**005 Brasil** · "O país que ganhou nome de MERCADORIA" (36) + diagonal escrivão 1511 × engenheiro de mina 2026, "NADA MUDOU?"
T1 8: a mercadoria é concreta e estranha. | T2 6: o brasileiro adivinha "pau-brasil" e a lacuna se fecha sozinha. | T3 10: 36 caracteres. | T4 9: "O país que + fato estranho" é provado (Iugoslávia 10,7×) e não está na grade. | T5 9: há contraste de destino.
H1 5: 2 cenas + 2 personagens + navio, toras, escavadeira: 2 focos competindo. | H2 7: os rostos e o texto leem; as cenas viram ruído. | H3 7: os dois em choque, mas sem desfecho pendente. | H4 8: único cartoon numa grade de fotos de políticos. | P1 8: mercadoria em 1511 e minério em 2026 completam ("ainda somos mercadoria?").
**Total 77 → REPROVADO** (H1 = 5) · Defeito: thumb com 2 focos e o nome "Brasil" fora do título.

**006 Roma** · "Roma pagou resgate aos bárbaros. Como virou dona do mundo?" (58) + senador chorando diante de Roma em chamas, "DE NOVO?", 410
T1 8: resgate e bárbaros são concretos. | T2 9: contradição + pergunta. | T3 7: 58 caracteres. | T4 9: afirmação estranha + pergunta, nada igual na grade. | T5 9: da humilhação ao domínio do mundo.
H1 8: senador + Coliseu em chamas (foco + apoio). | H2 9: rosto e "DE NOVO?" grandes. | H3 9: desespero com a causa visível. | H4 7: destaca-se pelo rosto, mas a grade tem 2 Romas laranja em fogo. | P1 9: a thumb põe a dor, o título o paradoxo.
**Total 84 → APROVADO** · Defeito menor: título acima de 50 caracteres.

**007 Rússia** · "Chamaram um VIKING para reinar. Como a Rússia ficou gigante?" (60) + só o mapa da Rússia aceso em vermelho, "TUDO ISSO?"
T1 9: o viking é estranho e concreto. | T2 9: afirmação estranha + pergunta. | T3 7: 60 caracteres. | T4 8: estrutura nossa, mas a grade tem "Como a Rússia ficou tão GRANDE?". | T5 8: de pequeno a gigante.
H1 9: 1 foco. | H2 9: mapa ≥ 50% da área, vermelho sobre azul-marinho. | H3 6: o contraste de escala é chocante, mas não há personagem nem emoção. | H4 5: a grade é toda vermelha (Revolução Russa) e "O maior país do mundo" mostra o mesmo mapa vermelho. | P1 7: "TUDO ISSO?" ecoa o "gigante" do título.
**Total 77 → REPROVADO** (H4 = 5) · Defeito: mapa vermelho na grade mais vermelha do canal. Mesmo assim é o maior CTR (9,57%, 188 impressões).

**008 França** · "A história INTEIRA da França em 15 minutos" (42) + Luís XIV com contorno de adesivo, panorama de 5 marcos, "FRANÇA 486 – 2026"
T1 3: rótulo. | T2 2: catálogo. | T3 10: 42 caracteres. | T4 3: fórmula dos clones (Memorias de Pez "La historia de FRANCIA en 16 minutos" está na grade). | T5 3: nada em jogo.
H1 3: boneco + 5 marcos + nome + datas. | H2 6: "FRANÇA" lê; o panorama vira mancha. | H3 2: boneco neutro em cartão-postal. | H4 2: gêmea de "Maravilhas da FRANÇA" (panorama claro + nome) e igual à vizinha Alemanha. | P1 3: "FRANÇA" repete o título.
**Total 37 → REPROVADO** · Defeito: pegada HiM pura (panorama + NOME + datas), o padrão que a própria bíblia diz não funcionar (CTR < 2% no Egito v1).

**009 Alemanha** · "A história INTEIRA da Alemanha em 17 minutos" (44) + boneco com capacete de ponta, Portão de Brandemburgo, Colônia e Reno, "ALEMANHA 9 – 2026"
T1 3 | T2 2 | T3 10 | T4 4: fórmula dos clones, mas sem igual na grade. | T5 3.
H1 3: panorama. | H2 6: o nome lê, o resto não. | H3 2: boneco sorrindo, sem tensão. | H4 5: é a única clara numa grade escura de Hitler e 2ª Guerra (bom), mas repete a vizinha França. | P1 3: "ALEMANHA" repete o título.
**Total 41 → REPROVADO** · Defeito: o mesmo da França. O roteiro tem uma lacuna pronta que não foi usada (Goethe: "Alemanha? Mas onde fica?", aos 0:37).

### Tabela-resumo
| Vídeo | Título no ar | CTR % (impressões) | Total /100 | Aprovado? | Principal defeito |
|---|---|---|---|---|---|
| 001 Egito | Como um RIO manteve o Egito vivo por 7.000 anos | 5,84 (5.858) | 73 | não | thumb igual à grade e desligada do rio (H4, P1) |
| 002 Índia | 5.000 ANOS de Índia em 19 minutos | 4,19 (4.872) | 65 | não | título-rótulo sem lacuna (T1, T2) |
| 003 Irã | Por que a Pérsia virou Irã e NUNCA virou árabe? | 5,08 (472) | 69 | não | thumb vende outra pergunta (P1 4) |
| 004 China | 3.000 ANOS de China em 16 minutos | 4,74 (3.542) | 62 | não | título-rótulo (T2 2) |
| 005 Brasil | O país que ganhou nome de MERCADORIA | 4,14 (1.064) | 77 | não | thumb com 2 focos (H1 5) |
| 006 Roma | Roma pagou resgate aos bárbaros. Como virou dona do mundo? | 2,00 (100) | 84 | **sim** | 58 caracteres (T3 7) |
| 007 Rússia | Chamaram um VIKING para reinar. Como a Rússia ficou gigante? | 9,57 (188) | 77 | não | mapa vermelho some na grade vermelha (H4 5) |
| 008 França | A história INTEIRA da França em 15 minutos | s/d (0) | 37 | não | panorama + NOME + datas, que repete o título |
| 009 Alemanha | A história INTEIRA da Alemanha em 17 minutos | s/d (0) | 41 | não | idem 008 |
| 010 Japão | indisponível | — | — | — | — |

**Média do canal: 65/100. Aprovado: 1 de 9 (Roma).** Título 33,1/50, thumb 26,1/40, par 5,8/10.

| Critério | T1 | T2 | T3 | T4 | T5 | H1 | H2 | H3 | H4 | P1 |
|---|---|---|---|---|---|---|---|---|---|---|
| Média | 5,9 | **5,1** | 9,1 | 6,3 | 6,7 | 6,3 | 7,6 | 6,6 | **5,7** | **5,8** |

**Defeito mais recorrente:** o título e a thumb não formam uma pergunta só. T2 < 7 em 5 vídeos (002, 004, 005, 008, 009) e P1 < 7 em 5 (001, 002, 003, 008, 009). A raiz é que **4 dos 9 títulos no ar ainda são fórmula/rótulo** (Índia, China, França, Alemanha), sem lacuna; nos que têm lacuna, a thumb às vezes vende outro trecho do vídeo (Egito, Irã). Em 3º lugar vem o H4: a nossa thumb some na grade ou repete a vizinha do canal (001, 007, 008, 009). O T3 é o ponto forte (média 9,1).

### A nota bate com o CTR?
- **Com o CTR acumulado, não.** Para os 7 vídeos com dado, a correlação entre nota e CTR é Pearson −0,08 e Spearman −0,23; só nos 5 com ≥ 400 impressões (001–005), Pearson 0,10. O motivo é a mistura: em `alcance_diario`, a maioria das impressões de 001 a 005 é **anterior** à reembalagem de 14/11, com outro título e outra thumb (Egito 97%, Índia 94%, Irã e Brasil 72%, China 39%), e a rubrica avalia o par de hoje. O 006 (84 pontos, 2,0%) tem 100 impressões e o 007 (77 pontos, 9,57%), 188: ruído.
- **No único dia depois da troca (14/11, `youtube.alcance_diario`, fonte `channel_reach_basic_a1`, 1.556 impressões, dia misto):** Pearson 0,74 e Spearman 0,81 em 6 vídeos. Brasil (77) foi a 5,37%, Rússia (77) 9,52%, Egito (73) 5,10%, China (62) 3,91%, Irã (69) 2,99%, Índia (65) 2,04%. A direção bate (a nota baixa do título-rótulo da Índia e da China acompanha o CTR que caiu depois da troca), mas é **Hipótese**: 1 dia, 21 a 1.074 impressões por vídeo, e a China pesa 69% do total.
- **Leitura honesta:** a rubrica ainda não está validada pelo nosso CTR. Para medir de verdade, falta janela limpa pós-14/11 (≥ 7 dias e ≥ 1.000 impressões por vídeo, pela Reporting API, que atrasa 1–2 dias). Até lá vale o `PADRAO-OURO.md` §5: o historia-ptbr já está na faixa normal de CTR (2–10%), e o gargalo é impressão, que título-rótulo de tema médio não resolve.


## Auditoria de embalagem no ar: dossie-es (Dossier en Minutos), 17/11/2026

Régua: `RUBRICA.md` (10 critérios 0–10; aprova com ≥ 75, nenhum < 6 e T2/H1/P1 ≥ 7). Par auditado = **título ao vivo** (`corpus/nossos.csv`) + **thumb no ar** (`thumbs/nossos/dossie-es-*.jpg`), olhadas na grade do tema a 160×90 e a 320×180 (`grades/dossie-00N-*.jpg`, a nossa na linha 2 × coluna 2, 11 concorrentes em `-refs.json`). Estilo julgado pela bíblia (`canais/dossie-es/biblia/`): todas as 8 respeitam traço, paleta e aba; o que se mede aqui é qualidade da embalagem.

**Portões:** políticas ok nos 8 (nenhuma palavra proibida, nenhum sangue/insígnia). Bíblia ok nos 8. Promessa: conferida só em 002 e 008 (Tarefa 2); no 002, o "nombre de su jefe" é pago em **1:14** (fora do 1º minuto; o MiG do hook é pago em 0:00–0:31).
**Ressalva de CTR:** acumulado de `alcance_diario`; em 001–006 mistura a embalagem antiga (até 14/11) e a nova, e a maior parte das impressões é da antiga (Mossad: 2,3% em 5.521 impressões já antes da reembalagem, `pesquisa/gap-2026-11-14/RELATORIO.md`). 006–008 têm 0–66 impressões: sem leitura.

### Fichas

**001 CIA** · "Cómo la CIA Quiso Controlar América Latina: de Guatemala a Chile" (64) · thumb: microfone de rádio na selva + sello FALSA + CIA gigante
T1 6 — Guatemala/Chile concretos, mas "controlar América Latina" é o esperado do tema | T2 5 — "cómo" genérico; o público já supõe a resposta (golpes) | T3 6 — 64 caracteres e 4 nomes | T4 6 — "Cómo + org + verbo" provado, mas o ângulo CIA-narcotráfico/LatAm já existe na grade (Intervenciones Gringas 3,0 mi) | T5 7 — escala continental
H1 7 — "microfone falso na selva" (1 foco + sigla) | H2 7 — microfone e CIA leem a 160; FALSA só a 320 | H3 5 — objeto parado, mistério fraco | H4 6 — única clara entre 11 fotos escuras/vermelhas, mas é o mesmo layout das 7 vizinhas do canal | P1 3 — **CIA da thumb = CIA do título**; FALSA não conversa com "controlar"
**Total 58 → REPROVADO** (T2, H3, P1) · defeito: sigla repetida e lacuna genérica.

**002 Mossad** · "Mossad: el Servicio Secreto que Ocultaba hasta el Nombre de su Jefe" (67) · thumb: MiG 007 pousado no deserto + sello FUGA + MOSSAD
T1 7 — "nombre de su jefe" é concreto e estranho | T2 7 — curiosidade clara (por quê?) | T3 4 — 67 caracteres | T4 5 — "SIGLA: el servicio secreto…" colide com 2 vizinhos ("MOSSAD: El brazo invisible", "MOSSAD: O Serviço Secreto Mais Temido") | T5 6 — o "hasta" sugere segredo extremo
H1 7 — "caça roubado no deserto" | H2 6 — avião cinza-claro sobre bege: baixo contraste a 160 | H3 5 — avião parado, desfecho já aconteceu | H4 6 — grade é 8/11 bandeira azul/silhueta escura; a nossa se separa, mas lembra o cartoon claro da col. 1 e as vizinhas do canal | P1 2 — **sigla repetida e a thumb vende outro caso** (o MiG) que o título não cita
**Total 55 → REPROVADO** (P1, T3) · defeito: título e thumb prometem coisas diferentes + sigla repetida.

**003 FBI** · "FBI: la Agencia que Espiaba a Su Propio País… Hasta que Abrieron sus Archivos" (77) · thumb: porta arrombada, lanterna, arquivo, "FBI" 2× + ¿QUIÉNES?
T1 6 — "espiaba a su propio país" é ação concreta | T2 6 — "hasta que" abre, mas o essencial já está dito | T3 3 — 77 caracteres, 2 orações | T4 4 — "Archivos" + FBI = marca do programa de TV que domina a grade ("Los Archivos del FBI") | T5 7 — contraste: o vigia vigiando o próprio país
H1 3 — FBI escrito 2× + porta + gaveta + lanterna (exemplo da âncora 3) | H2 6 — FBI lê; a cena da porta embaralha a 160 | H3 7 — instante do arrombamento | H4 7 — única ilustrada entre 11 frames de TV; o "FBI" preto lembra o selo "los archivos del FBI" das vizinhas | P1 4 — FBI 3× (título + 2 na thumb); ¿QUIÉNES? completa o "abrieron"
**Total 53 → REPROVADO** (H1, T3, P1) · defeito: FBI escrito duas vezes na thumb e título de 77 caracteres.

**004 Cosa Nostra** · "TODA la Historia de la Cosa Nostra en 15 Minutos" (48) · thumb: mãos rasgando estampa de santo em chamas + TRAIDOR + COSA NOSTRA
T1 3 — rótulo de tema | T2 2 — nenhuma pergunta | T3 9 — 48 caracteres, 1 ideia | T4 5 — fórmula sem colisão literal no tema em es, mas tema difuso (flop típico no Archive) | T5 3 — só descrição
H1 7 — "juramento do santo queimando" | H2 6 — mãos médias, bege sobre bege; TRAIDOR pequeno | H3 7 — juramento em chamas = tensão | H4 6 — única clara entre fichas policiais P&B; layout igual ao das vizinhas | P1 3 — COSA NOSTRA repete o título
**Total 51 → REPROVADO** (T1, T2, T5, P1) · defeito: título-rótulo sem lacuna.

**005 KGB** · "La KGB en 14 Minutos: del Sótano de Lubianka al Piolet de México" (64) · thumb: guarda-chuva com a bolinha + SIN CULPABLE + KGB
T1 7 — concretos bons, mas 3 (âncora 7 da própria rubrica) | T2 6 — "de A a B" abre o percurso, sem tensão nomeada | T3 5 — 64 caracteres, 3+ itens | T4 6 — "ORG: de A a B" com prova fraca; sem colisão na grade | T5 6 — o piolet sugere o desfecho grande
H1 7 — "guarda-chuva-arma" | H2 5 — objeto fino em diagonal vira um risco a 160 | H3 6 — arma apontada + lacuna "sin culpable" | H4 6 — única minimalista clara entre cartazes soviéticos vermelhos; igual às vizinhas | P1 3 — KGB repetida e o guarda-chuva (Londres) é um 3º caso que o título não cita
**Total 57 → REPROVADO** (P1, H2, T3) · defeito: thumb e título nomeiam casos diferentes + sigla repetida.

**006 Masones** · "TODA la Historia de los Masones en 14 Minutos" (45) · thumb: livro lacrado com esquadro-compasso + RITUALES + MASONES
T1 3 — rótulo | T2 2 — nenhuma pergunta | T3 9 — 45 caracteres | T4 4 — tema saturado de "historia/origen/quiénes son" (Academia Play "LA MASONERÍA" 797 mil) | T5 3 — nada em jogo
H1 7 — "livro secreto lacrado" | H2 7 — livro grande (~45%) e MASONES leem | H3 4 — livro fechado, parado | H4 5 — grade é olho/compasso dourado e rostos; a nossa é clara mas morna, e igual às vizinhas | P1 3 — MASONES repete
**Total 47 → REPROVADO** · defeito: título-rótulo + thumb sem tensão.

**007 SS** · "TODA la historia de las SS en 14 minutos" (40) · thumb (layout pôster antigo): velho de óculos escuros na praia com passaporte + LAS SS + sello 1925–1945 + "NUNCA LO ATRAPARON"
T1 3 — rótulo (exemplo da âncora 3) | T2 2 — nenhuma pergunta | T3 9 — 40 caracteres | T4 5 — fórmula; em es a grade é "Dentro de las SS" ×3 (sem colisão literal) | T5 3 — só descrição
H1 5 — personagem + 3 blocos de texto | H2 6 — rosto e LAS SS leem; período e "NUNCA LO ATRAPARON" só a 320 | H3 6 — fugitivo impune = tensão, mas parada | H4 7 — única clara/tropical entre capacetes e uniformes; repete o pôster do 008 | P1 3 — LAS SS + período repetem o "toda la historia"
**Total 49 → REPROVADO** · defeito: rótulo de tema + 4 textos na thumb. (Tema-ímã: Archive SS 8,8×; é onde a embalagem mais desperdiça.)

**008 Inquisición** · "TODA la historia de la Inquisición en 14 minutos" (48) · thumb (pôster antigo): inquisidor com pergaminho lacrado + INQUISICIÓN + sello 1478–1834
T1 3 — rótulo | T2 2 — nenhuma pergunta | T3 9 — 48 caracteres | T4 3 — **colisão direta**: Academia Play "La inquisición en 15 minutos" (4,7 mi) na mesma grade | T5 3 — só descrição
H1 5 — personagem + objeto + 2 textos | H2 5 — hábito preto sobre parede cinza: baixo contraste a 160 | H3 5 — rosto severo, nada pendente | H4 4 — cinza no meio de 11 coloridas; o pôster com período repete o 007 | P1 2 — INQUISICIÓN + período = o título reescrito
**Total 41 → REPROVADO** · defeito: fórmula colidindo com hit de 4,7 mi + thumb que repete o título.

### Resumo
| Vídeo | Título (caracteres) | CTR % (impressões) | Total/100 | Aprovado? | Principal defeito |
|---|---|---|---|---|---|
| 001 CIA | Cómo la CIA Quiso Controlar América Latina… (64) | 3,33 (1.862) | 58 | não | CIA na thumb e no título; lacuna genérica |
| 002 Mossad | Mossad: el Servicio Secreto que Ocultaba… (67) | 2,73 (12.726) | 55 | não | thumb vende o MiG, título o chefe; sigla repetida |
| 003 FBI | FBI: la Agencia que Espiaba… (77) | 3,91 (1.280) | 53 | não | FBI 3×; título longo; 3 focos |
| 004 Cosa Nostra | TODA la Historia de la Cosa Nostra… (48) | 3,01 (266) | 51 | não | rótulo sem lacuna; sigla repetida |
| 005 KGB | La KGB en 14 Minutos: del Sótano… (64) | 3,03 (330) | 57 | não | 3 casos diferentes entre título e thumb; objeto fino |
| 006 Masones | TODA la Historia de los Masones… (45) | 0,00 (66) | 47 | não | rótulo + thumb sem tensão |
| 007 SS | TODA la historia de las SS… (40) | 0,00 (14) | 49 | não | rótulo + 4 textos na thumb |
| 008 Inquisición | TODA la historia de la Inquisición… (48) | — (0) | 41 | não | colide com Academia Play 4,7 mi; thumb = título |

**Média do canal: 51,4/100** (0 de 8 aprovados; o mínimo para aprovar é 75).
**Média por critério:** T1 4,8 · T2 4,0 · T3 6,8 · T4 4,8 · T5 4,8 · H1 6,0 · H2 6,0 · H3 5,6 · H4 5,9 · **P1 2,9**.

**Defeito mais recorrente: P1, 8 de 8. A SIGLA gigante da thumb repete a sigla/nome do título em todos** (CIA, MOSSAD, FBI ×2, COSA NOSTRA, KGB, MASONES, LAS SS, INQUISICIÓN). É a regra do layout da bíblia ("SIGLA gigante à direita"), herdada do Archive, e é justamente onde os grandes de dossiê ganham (Fern/LEMMiNO/BS repetem em 6 de 30, `ANALISE-historia-dossie.md` §3). Em 2 casos (002, 005) é pior: além de repetir, a thumb mostra um caso que o título não cita. Segundo defeito: **T2** (4,0): 4 títulos são rótulo sem pergunta ("TODA la historia…") e os outros 4 abrem lacunas genéricas ou longas. Terceiro: **H4 do canal**: as 8 thumbs têm o mesmo esqueleto (objeto/personagem à esquerda, sigla à direita, sello, aba) e na página do canal viram uma só.

**A nota bate com o CTR?** Em parte, com ressalva forte. Notas de 51 a 58 e CTRs de 2,7% a 3,9%: tudo na mesma faixa baixa, o que é coerente (nenhuma embalagem excepcional, nenhuma desastrosa). O pior CTR com volume (Mossad 2,73% em 12,7 mil impressões) tem o pior P1 (2), mas a maior parte dessas impressões é da embalagem anterior a 14/11 (já 2,3%). O FBI tem o melhor CTR (3,91%) com nota 53: o que a nota não captura é que, numa grade de frames de TV, ele é a única ilustração (H4 7) e o instante do arrombamento (H3 7). Com 1.280 impressões, isso ainda é ruído. 006–008 (0–66 impressões) não podem confirmar nem derrubar nada. **Hipótese** até o "Testar e comparar" e ≥ 1.000 impressões por embalagem nova.


## Auditoria de embalagem: Em Relevo (17/11/2026)

Régua: `RUBRICA.md` (10 critérios 0–10; aprova com total ≥ 75, nenhum < 6 e T2/H1/P1 ≥ 7; portões antes). Par auditado = **título ao vivo + thumb no ar** (`corpus/nossos.csv`, `thumbs/nossos/em-relevo-*.jpg`). H2/H4 dados olhando `grades/relevo-00N-160.jpg` e `-320.jpg` (nossa thumb na linha 2 × coluna 2, entre 11 concorrentes de `relevo-00N-refs.json`). Bíblia do canal (`canais/em-relevo/biblia/`) manda no estilo.

### 001 · Sul / tornados
Título: "O que está acontecendo com o clima no Sul do Brasil?" (52) · Thumb: Andes rosados + fita ciano de umidade sobre satélite escuro, "CULPA DOS ANDES?" · CTR 2,67% (374 impr., mistura a thumb bege/polaroid de antes de 14/11).
Portões: políticas ok · bíblia ok · promessa ok (hook 0:00–0:29) · refs: o título é o exemplo **0** da própria rubrica.

| Crit. | Nota | Porquê |
|---|---|---|
| T1 | 0 | É literalmente a âncora 0 da rubrica: "clima no Sul" é rótulo vago, sem objeto. |
| T2 | 3 | Pergunta genérica; não aponta nenhuma anomalia que só o vídeo explica. |
| T3 | 7 | 52 caracteres, 1 ideia. |
| T4 | 5 | Molde Mundo Entrópico ("O que está ACONTECENDO com…"), mas sem a palavra-objeto em caixa alta; a grade tem "Por que tornados e ciclones estão atingindo o Centro-Sul" (Brasil Urgente). |
| T5 | 3 | Nada em jogo no título (nem número, nem contraste). |
| H1 | 7 | "Andes guiam rio de umidade": 1 foco (fita) + texto. |
| H2 | 7 | A 160 a fita ciano e "ANDES?" leem; o satélite escuro tira contraste do resto. |
| H3 | 5 | "Culpa" sugere suspeito, mas não há desfecho pendente visível (o Sul nem aparece em alerta). |
| H4 | 7 | Única com mapa entre 10 fotos de tempestade/TV e 1 rosto; lembra o satélite escuro do ciclone (Brasil Urgente). |
| P1 | 8 | Título pergunta, thumb aponta o suspeito; não repetem palavra. |
| **Total** | **52** | **REPROVADO** (T1 0, T2 3). Defeito: título vago sem anomalia concreta; a thumb é boa e está sendo desperdiçada. |

### 002 · El Niño 2026
Título: "El Niño 2026 vai ser o mais forte da história?" (46) · Thumb: termômetro + língua vermelha do Pacífico + seta amarela + Brasil vermelho sobre navy, "SÓ 2 °C?" · CTR 1,55% (388 impr.; pior do canal com impressões).
Portões: políticas ok · bíblia ok (é a "língua quente real" do controle) · promessa ok (responde em 4:12–5:03) · refs: a bíblia já marca este título como fora do padrão (`titulo.md`).

| Crit. | Nota | Porquê |
|---|---|---|
| T1 | 4 | "El Niño 2026" é nome técnico como gancho, igual aos 11 do tema; sem lugar nem objeto. |
| T2 | 3 | Sim/não sobre recorde (âncora 3 da rubrica); o vídeo responde "ainda não" e esvazia. |
| T3 | 9 | 46 caracteres, 1 ideia. |
| T4 | 3 | Fórmula dos clones: "mais devastador da história" (Cortes ICL), "vai piorar", "vem aí?". |
| T5 | 6 | Superlativo existe, mas é o superlativo genérico do tema. |
| H1 | 4 | 4 elementos competindo (termômetro, língua, seta, Brasil) + texto. |
| H2 | 6 | "SÓ 2 °C?" e a mancha vermelha leem a 160; termômetro e seta viram ruído no navy. |
| H3 | 5 | "Só 2 °C" insinua desproporção, mas a imagem é diagrama, sem estado pendente. |
| H4 | 3 | Faz o que 6 dos 11 fazem (Pacífico/Brasil vermelho-laranja: Jubilut, "JÁ ERA?", BBC, Fatos, Top10, MetSul). |
| P1 | 6 | Não repetem palavra, mas título (recorde) e thumb (2 °C) puxam para lados diferentes. |
| **Total** | **49** | **REPROVADO** (T2 3, H1 4, P1 6, T4/H4 3). Defeito: pergunta sim/não + thumb igual à grade do tema. |

### 003 · Seca de 1877
Título: "Por que quase ninguém fala da seca que matou 500 mil brasileiros?" (65) · Thumb: mapa escuro do Nordeste em vermelho-terra + polaroid "CEARÁ · 1878" + "500 MIL ESQUECIDOS" · sem impressões no CSV (Rodrigo: 0,8% nas primeiras horas, 16/11).
Portões: **bíblia NÃO** (título com "matou", proibido em `README.md`/`titulo.md`; número de mortos na thumb, proibido em `README.md`) · políticas: risco · promessa ok · refs ok ("esquecido", Mundo Entrópico 2,3 mi).

| Crit. | Nota | Porquê |
|---|---|---|
| T1 | 7 | Seca + 500 mil é concreto, mas esperado no tema. |
| T2 | 7 | Lacuna clara (por que o esquecimento?), porém genérica. |
| T3 | 7 | 65 caracteres (teto da faixa 7). |
| T4 | 6 | Estrutura provada, mas colide com "A tragédia esquecida…" (BBC) e "…o Império Fingiu Não Ver" (Brasil Trágico) na grade. |
| T5 | 8 | Escala forte (500 mil). |
| H1 | 6 | Número + polaroid + mapa: 2 focos. |
| H2 | 6 | "500 MIL" lê a 160; polaroid some; mapa escuro sem contraste. |
| H3 | 4 | Número estático; nada pendente. |
| H4 | 5 | Único mapa entre retirantes sépia/IA, mas na mesma paleta marrom-vermelha da grade e repete a vizinha do canal (mapa escuro + número, 9 de 11 em 16/11). |
| P1 | 3 | "500 MIL" da thumb repete o "500 mil" do título. |
| **Total** | **59** | **REPROVADO** (portão bíblia; P1 3). Defeito: "matou" no título e número de vítimas na thumb (corrigir já, independente do CTR). |

### 004 · El Niño 1983
Título: "O El Niño causou seca no Nordeste e..." (38) · Thumb: "MESMO ANO" gigante branco à esquerda, Brasil escuro com Nordeste laranja, etiquetas "SECA" (vermelha) e "ENCHENTE" (azul), caixa "1983" · sem impressões.
Portões: políticas ok · bíblia ok · promessa ok (seca + enchente em 1983) · refs: fraco (reticências: 6 hits × 0 flops só em en; `ANALISE-geografia.md` §1.3).

| Crit. | Nota | Porquê |
|---|---|---|
| T1 | 6 | El Niño + seca + Nordeste concretos, mas esperados; sem o ano, parece notícia de 2026. |
| T2 | 5 | A lacuna é formal: "e..." soa como título cortado, não como pergunta específica. |
| T3 | 7 | 38 caracteres, mas a frase truncada exige 2ª leitura. |
| T4 | 6 | Reticências de suspense sem hit medido em pt no nicho; não colide com a grade. |
| T5 | 5 | O contraste seca × enchente está escondido (só aparece na thumb). |
| H1 | 5 | Texto + mapa + 3 etiquetas (SECA, ENCHENTE, 1983). |
| H2 | 7 | "MESMO ANO" lê muito bem a 160; mapa escuro e etiquetas somem. |
| H3 | 5 | O paradoxo existe, mas está em etiquetas pequenas; mapa sem anomalia visível. |
| H4 | 6 | Única sem brilho vermelho do Pacífico entre 5 línguas quentes e 5 rostos; o bloco de texto lembra "DEZEMBRO CRÍTICO" e repete o mapa escuro do canal. |
| P1 | 7 | A thumb paga as reticências ("MESMO ANO" + ENCHENTE); ecoa "SECA". |
| **Total** | **59** | **REPROVADO** (T2 5, H1 5). Defeito: reticências no lugar de lacuna; o paradoxo bom ficou só na thumb e em etiquetas pequenas. |

### Resumo
| Vídeo | Título no ar | CTR % (impr.) | Total/100 | Aprovado? | Principal defeito |
|---|---|---|---|---|---|
| 001 Sul | O que está acontecendo com o clima no Sul do Brasil? | 2,67 (374)* | 52 | Não | título vago, sem anomalia (T1 0) |
| 002 El Niño 2026 | El Niño 2026 vai ser o mais forte da história? | 1,55 (388)* | 49 | Não | sim/não + thumb igual à grade (Pacífico vermelho) |
| 003 Seca 1877 | Por que quase ninguém fala da seca que matou 500 mil brasileiros? | s/d (0,8% nas 1ªs horas, Rodrigo) | 59 | Não (portão) | "matou" + número de vítimas na thumb; thumb repete o título |
| 004 El Niño 1983 | O El Niño causou seca no Nordeste e... | s/d | 59 | Não | reticências no lugar de lacuna; 3 etiquetas pequenas |

\* CTR acumulado; inclui a thumb bege/polaroid de antes da reembalagem de 14/11.

**Nota média do canal: 54,75/100** (0 de 4 aprovados).

| T1 | T2 | T3 | T4 | T5 | H1 | H2 | H3 | H4 | P1 |
|---|---|---|---|---|---|---|---|---|---|
| 4,25 | 4,50 | 7,50 | 5,00 | 5,50 | 5,50 | 6,50 | **4,75** | 5,25 | 6,00 |

**Defeito mais recorrente:** thumb em **mapa escuro (navy/marrom) sem camada de tensão**: 4 de 4, com H3 ≤ 5 em todas (nenhuma região em alerta sobre relevo claro, nenhum estado pendente; `ANALISE-geografia.md` §5, regras 1–3). No título, **lacuna fraca** (T2 < 7 em 3 de 4) e **sem objeto concreto** (T1 médio 4,25). O que está bom: tamanho (T3 7,5) e o par título × thumb não repetir palavra (exceto 003).

**Nota × CTR:** a ordem bate nos 2 com dado (001: 52 → 2,67%; 002: 49 → 1,55%), e todos abaixo de 60 combinam com o canal abaixo da faixa normal (meta de 4% da bíblia). Ressalva: < 400 impressões por vídeo, CTR misturando duas embalagens no 001/002 e nada no 003/004: **Hipótese**, não prova. Reavaliar com ≥ 5.000 impressões (regra da bíblia, `README.md`).

**Urgente fora do ranking:** o 003 viola a bíblia no ar ("matou" no título, número de vítimas na thumb). Troca mínima sugerida: "A seca de 1877 levou 500 mil. Por que ninguém lembra?" (53) e thumb sem "500 MIL" (decisão do Rodrigo).


