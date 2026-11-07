# Roteiro do historia-ptbr: o que os canais de referência fazem e nós não (07/11/2026)

Pedido do Rodrigo: o roteiro "ainda não está redondo". Método: 18 vídeos transcritos **completos** (Whisper small, `transcricoes/`), números da Data API (07/11, ~25 unidades), métricas de texto (`metricas_texto.py` → `metricas_texto.txt`) e comparação com os nossos 4 roteiros (`videos/00{1..4}/SCRIPT.md`) e com a `biblia/roteiro.md`. Custo: R$ 0.
Arquivos: `levantar.py` (lista canais/vídeos → `canais.json`), `lote.py` (transcrição), `metricas_texto.py`.

---

## 1. Vídeos analisados

| Canal (inscritos) | Vídeo | ID | Views | Idade | Dur. | Views/insc. |
|---|---|---|---|---|---|---|
| **A** Ink Explainer (164 mil) | What Did Ancient Humans Actually Do All Day? | `49_Ph2q6uIM` | 18,4 mi | 77 d | 11:13 | 112× |
| | What Did Ancient Humans Do When It Rained All Week? | `SD7XyG2wd1k` | 1,99 mi | 126 d | 11:37 | 12× |
| **A** Kelevin (302 mil) | Ancient Myths That Turned Out To Be True | `ngprAYfRrnY` | 4,17 mi | 51 d | 16:12 | 14× |
| | The Full Story Of Greek Mythology In 15 Minutes | `t7zjiFULuUc` | 847 mil | 21 d | 15:06 | 2,8× |
| | The Entire History Of Ancient Egypt in Under 20 Minutes | `FnXS0VOhX1I` | 568 mil | 523 d | 19:52 | 1,9× |
| **A** Crayon Capital (298 mil) | The Wolf of Wall Street Scam Explained Like You're 5 | `HawmGu7oNrc` | 4,29 mi | 399 d | 16:33 | 14× |
| | The Great Depression Explained Like You're 5 | `LuEcoqizj0o` | 3,00 mi | 448 d | 16:29 | 10× |
| | The Man Who Built Singapore in One Generation | `y51JjcymEAY` | 1,18 mi | 315 d | 16:09 | 4× |
| **B** História na Marra (16,4 mil) | Como a dinastia MAIS PODEROSA da Europa perdeu tudo | `ARDA87ONohc` | 150 mil | 25 d | 24:57 | 9,2× |
| | A Unificação Italiana | `S8yKeHDpgOg` | 131 mil | 427 d | 8:07 | 8× |
| | A História COMPLETA da Macedônia | `VAaop-wsneQ` | 92 mil | 13 d | 36:17 | 5,6× |
| **C** ArchLang (70 mil) | **HIT** Why Civilizations Collapse (And Why We Are Next) | `yV-Cwcy8K6A` | **1,13 mi** | 185 d | 12:31 | 16× |
| | How Did Ancient Egypt Survive for 3,000 Years? | `J1ARuhEH0zI` | 397 | 62 d | 18:06 | 0,006× |
| | Why Every Revolution Eats Its Own Children | `APoNEKs9d-4` | 966 | 17 d | 23:28 | 0,01× |
| **C** Breakdown with paint (25) | Nepal Was Hit by a 30-Foot Wall of Water (3 dias **antes** do hit) | `cHwDK968qCQ` | 547 | 66 d | 12:12 | — |
| | **HIT** China-Nepal Floods Were Impossible to Outrun — Research Reveals Why | `cjIvXfkF1S0` | **17,8 mil** | 63 d | 10:03 | — |
| | A Glacier Collapsed in Nepal — Then Disaster Hit China | `5d-KSO2BVGM` | 90 | 60 d | 12:12 | — |
| | 4000 Years of Chinese History Explained in 20 Minutes | `J-wZ1HfirTo` | 557 | 46 d | 20:05 | — |
| **Nós** | Egito (`g847Td0Plsk`) / Índia (`MV5SSjoccqE`) | — | 91 / 59 | 4 d | 17:00 / 19:27 | % assistido **41% / 26%** |

Mediana do canal (vídeos > 1 min): Ink 301 mil · Kelevin 301 mil · Crayon 445 mil · História na Marra 24 mil (últimos 10: 36 mil) · ArchLang 570 · Breakdown 552.
Quem é de quem (pedido do brief): `yV-Cwcy8K6A` = **ArchLang**; `cjIvXfkF1S0` = **Breakdown with paint**.

**Métricas de texto** (por 100 palavras; "você" = you/your / você/seu/sua/imagine; conectivo = but/then/so/because… / mas/então/só que/porque…):

| | ppm | palavras/frase | perguntas/min | "você" /100 | conectivos /100 |
|---|---|---|---|---|---|
| Ink (2) | 208–225 | 11,5–13 | 0,5–0,6 | **2,5–3,8** | 1,7–2,3 |
| Crayon (3) | 148–152 | **7,5–9** | 0,7–**2,3** | 0,7–1,3 | 1,9–2,2 |
| Kelevin (3) | 209–228 | 10,6–16,8 | 0,7–1,0 | 0,6–1,0 | 1,4–2,3 |
| História na Marra (3, pt) | 137–176 | 14,6–17 | 0,1–0,25 | 0,6–0,95 | **1,2–2,5** |
| ArchLang hit / fracos | 151 / 158–162 | 10,6 / 12,5–12,9 | 0,2–0,5 | 0,7–0,8 | 1,5–1,8 |
| Breakdown China (fraco) | 146 | 8,2 | 0,4 | **0,0** | 2,0 |
| **Nós (001–004, pt)** | **129–136** | 11–12,6 | 0,5–0,9 | **0,1–0,26** | **0,4–0,9** |

---

## 2. O que se repete nos que vão bem

1. **O espectador entra na história.** Ink abre com o despertador *dele* ("This morning, a machine screamed at you", 0:00) e põe-no dentro da cena ("Next to you, someone is drilling tiny holes", 5:27). ArchLang hit: "Hey, you! Yes, you! The one living in a functioning society…" (0:00) e "why we are next" no título. Crayon: "You woke up rich, then went to bed broke" (0:01). Usam "você" 3–15× mais que nós.
2. **Uma pergunta só, que volta.** História na Marra (Habsburgo) abre com o fim (1918, a abdicação), pergunta "como uma família que passou séculos acumulando tronos chegou a esse ponto?" (1:30), chama o vídeo de "investigação/caso" e volta a ela no fim ("vamos voltar lá pra pergunta inicial", 22:48), **reenquadrando** a pergunta ("talvez a pergunta correta nunca tenha sido como desapareceram…", 24:26). Ink empilha 3 perguntas da mesma dúvida ("where did all of your time go?", 1:02). Até o ArchLang Egito (fraco em views) faz isso bem: "the first reason… the second reason… the third reason Egypt survived" pagas no fecho.
3. **Motor problema → solução → novo problema.** "But the Shang had a problem… The Zhou had an answer" (Breakdown China, 1:51). "Mas olhar para o mapa também revela uma fraqueza: aquilo não era um país" (HnM, 8:14). ArchLang hit: cada capítulo é um elo da mesma corrente (economia → governo → clima → invasores → "the invasion is rarely the cause, it's the consequence", 10:01). Em pt, a HnM usa **2–3× mais conectivos** (mas/só que/então/porque) do que nós.
4. **Voz com humor e opinião.** Kelevin: piada a cada 10–15 s ("Good game, Egypt", 19:35; "No way that would ever come back to bite them", 7:47). Crayon: micro-diálogos encenados ("Gentlemen, please. One crisis at a time." 0:26). ArchLang: sarcasmo ("which historians named with refreshing honesty", 3:09). HnM em pt: coloquial ("parecia uma pizza cortada em 12 pedaços", "a verdadeira treta", 0:36–1:03).
5. **Cena em vez de ficha.** Ink descreve uma tarde no acampamento antes de dar a prova (conchas de 70 mil anos); Crayon dramatiza Raffles chegando ao pântano. A prova vem *depois* da cena e a serviço da pergunta ("And this isn't a guess…", Ink 5:36).
6. **Poucos loops explícitos.** "Remember/lembra" aparece 0–2× por vídeo (só o Kelevin Grécia tem 4, como piada recorrente). Nós usamos **"guarde" 4–6×** (Índia 6, Irã 6, China 4).
7. **Pergunta central cedo.** Wolf 0:14, Grande Depressão 0:14, Singapura 0:32, ArchLang hit 0:46, Ink 0:56 (ArchLang em forma de tese, não de pergunta). Exceção: HnM (1:30), mas a primeira frase já diz "hoje a gente vai investigar como…" (0:00).
8. **Fecho curto.** Kelevin: "All right, that's everything" (19:44). ArchLang hit: punchline em 30 s. HnM: reenquadra a pergunta e acaba.

## 3. Grupo C: o que mudou entre o hit e os fracos (causa provável)

**ArchLang** (mesma voz, mesmo humor, mesmo visual nos 3):
| | Hit (1,13 mi) | Egito (397) | Revolução (966) |
|---|---|---|---|
| Tema | universal + ameaça a **você** ("And Why We Are **Next**") | "como o Egito durou" (de *outros*) | padrão histórico (de *outros*) |
| Hook | "Hey, you!" + padrão ("every civilization… collapsed") em 46 s | quiz "think of the oldest country" + pergunta em 56 s | cena em 2ª pessoa ("you just overthrew the government") + **pedido de like/inscrição em 1:00** |
| Estrutura | 6 capítulos = 6 elos causais da mesma corrente | 3 razões pagas no fecho (bom) | lista de revoluções |
| Duração | **12:31** | 18:06 | 23:28 |
| Causa provável | — | **tema/título**: o texto do Egito é estruturalmente bom (pergunta + razões + "Remember that word: ma'at") e mesmo assim fez 397 | tema/título + duração; o CTA no hook é o único defeito claro de roteiro |
Evidência de que **não foi o roteiro**: 70 mil inscritos vieram do hit e não assistem aos seguintes (0,6–1,4% de views/insc.) → a audiência veio pelo tema "nós somos os próximos", não pela identidade do canal. O mesmo tema do Egito fez 568 mil no Kelevin (tom humorístico, canal com base) e 91 no nosso.

**Breakdown with paint** (3 vídeos do mesmo desastre em 6 dias + 2 históricos):
| | Antes (547) | Hit (17,8 mil) | Depois (90) |
|---|---|---|---|
| Título | "…Here's What Happened" | "…Impossible to Outrun — **Research Reveals Why**" | "…Then Disaster Hit China" |
| 1ª frase | "Some of the most terrifying flood footage…" (bom), mas narração com muletas ("you know", "okay") e data truncada (0:57) | "At first, it looked like a flood. Then researchers… **the numbers changed the story completely**" | "People… began their day like any other" (cronológico, sem pergunta) |
| Prova no hook | não | **68 km/h** aos 0:34 + "what we know / what research suggests / what we don't know" | não |
| Corpo | hipóteses | **investigação**: elimina o terremoto, elimina o lago glacial, chega ao fluxo de detritos | cronologia |
Causa provável: **tema no tempo certo + título de curiosidade** (o hit pegou a notícia no auge; o "depois" chegou com o assunto velho e caiu abaixo do "antes"). O roteiro do hit ajuda (único com virada + número no hook), mas não explica 30×. O histórico "4000 Years of Chinese History" (557) é **quase o nosso China 004**: "China has collapsed so many times… and somehow keeps coming back" → "So how did one civilization survive…?" → os Shang "asked the dead" → Mandato do Céu → Wu Zetian. Texto correto, sem "você" (0,0), sem humor, sem cena: 557 views num canal de 25 inscritos. **Esse é o risco do nosso molde atual.**

## 4. Onde o nosso roteiro difere (trecho nosso × trecho deles)

| # | Nós | Eles |
|---|---|---|
| a. **Pergunta central fraca/tardia** | Irã: "Essa é a história inteira do Irã. Um país invadido por gregos, árabes, mongóis e turcos…" (0:51, afirmação); a pergunta só vem aos 1:25: "E o que esse cavalo tem a ver com o Irã de hoje?" | HnM: "Como uma família que passou séculos acumulando territórios… conseguiu chegar a esse ponto? Para descobrir, vamos analisar esse caso desde o começo." (1:30) e volta a ela em 22:48 |
| b. **Espectador fora** | 1–5 "você" por vídeo; o narrador conta *sobre* reis | Ink: "he asks himself a question you have never once been free enough to ask" (0:22) |
| c. **Sucessão em vez de motor** | China: "Quem pegou o trono foi…", "Dessa revolta saiu…", "Quem assumiu foi…" (abertura dos cap. 4, 7, 10) | Breakdown/HnM: "But the Shang had a problem…", "Só que existe um detalhe importante: o nosso caso não termina em 1700" |
| d. **Ficha de curiosidades** | Irã N012–N013: elamitas, escrita decifrada em 2022 por um arqueólogo francês (não serve à pergunta) | Ink: cena da tarde no acampamento → a prova arqueológica confirma a cena |
| e. **Loops demais** | Irã: guarde o cavalo, a palavra *pairidaêza*, o apelido "Pérsia", o cilindro (4 "guarde" nos primeiros 3 min) | 0–2 por vídeo; o loop principal é a pergunta |
| f. **Sem humor** | tom solene; humor raro ("uns gregos teimosos", N023, é o melhor momento) | Kelevin/ArchLang/Crayon: 2–6 tiradas por minuto |
| g. **Promessa em lista longa** | Irã N007: 4 itens; Índia: hook de 2:21 | Wolf/Depressão/Singapura: zero lista, só a pergunta |
| h. **Ritmo lento** | 129–136 ppm (drama-3 + pausas) | 137–228; a HnM, em pt e com voz humana, 137–176 |

O que já fazemos bem (manter): anedota de abertura forte (cavalo de Dario, elixir de Qin), fio condutor nomeado (Mandato do Céu), fecho que paga o hook, títulos de capítulo em frase. O Egito, com hook de 0:49, tem **41% assistido** contra **26% da Índia** (hook de 2:21) em `youtube.metricas_video` de 07/11 (91 e 59 views: amostra pequena, mas na direção da hipótese do hook curto).

## 5. Mudanças propostas para a `biblia/roteiro.md` (não editei a bíblia)

1. **Pergunta central como pergunta, até ~0:50 (ideal 0:30), com algo em jogo.** "Essa é a história inteira de X" vem *depois* da pergunta, nunca no lugar dela. *Por quê:* todos os do grupo A fazem a pergunta em 14–56 s; o nosso Irã afirma aos 0:51 e pergunta aos 1:25. *Evidência:* §2.7; Egito 41% × Índia 26% assistido (Hipótese, n pequeno).
2. **A pergunta volta em voz alta pelo menos 3 vezes** (≈ a cada 4–5 min: "e aqui está a primeira peça da resposta…") e o fecho **responde e reenquadra**. O fio condutor passa a ser *a resposta sendo montada*, não só um objeto que reaparece. *Evidência:* HnM 1:30 → 22:48 → 24:26; ArchLang Egito (3 razões pagas). Não são capítulos-objeto: as eras continuam ligadas e cronológicas.
3. **Motor de cada era = problema → solução → novo problema.** Todo capítulo termina com o problema que a próxima era vai tentar resolver; proibido abrir capítulo com "Quem assumiu foi…/Dessa revolta saiu…". Meta: **≥ 1,5 conectivo causal por 100 palavras** (mas, só que, então, porque, o problema é). *Evidência:* HnM 1,2–2,5 em pt; nós 0,4–0,9.
4. **Ponha o espectador na cena: ≥ 1 "você/imagine/se você fosse" por 100 palavras** (~20 por vídeo), com 1 ponte com a vida dele por capítulo (o qanat × o encanamento do prédio; o imposto de Dario × o seu IR). *Evidência:* Ink 2,5–3,8, Crayon 0,7–1,3, HnM 0,6–0,95; nós 0,1–0,26; o hit do ArchLang é o único dos 3 com "você" no título.
5. **Uma cena por capítulo antes dos fatos.** 4–6 frases no presente, um lugar, uma pessoa, um momento; depois no máximo 3 fatos que provam a cena. Curiosidade que não serve à pergunta sai (ex.: elamitas/2022 no Irã). *Evidência:* Ink (cena → prova), Crayon (dramatização); Breakdown China, que é só fato, fez 557. **Hipótese** quanto ao efeito na retenção.
6. **Humor seco do narrador: 1 tirada a cada ~40–60 s**, sempre sobre o fato (ironia, anacronismo, "spoiler: não durou"), sem gíria forçada. *Evidência:* os 3 canais do grupo A e a HnM têm voz opinativa; nosso melhor momento do Irã ("uns gregos teimosos") é desse tipo. **Hipótese** de dosagem: começar com 1/min e medir.
7. **No máximo 2 "guarde isso" por vídeo** (o do hook + 1). Os outros callbacks entram sem anúncio ("lembra do cavalo?"). *Evidência:* referências 0–2; nós 4–6.
8. **Hook: anedota ≤ 45 s → pergunta → "essa é a história" → entrar no corpo; promessa em lista no máximo 2 itens (ou nenhuma).** Alvo ~60–75 s até o capítulo 1 (hoje 1:16–1:32). *Evidência:* Wolf/Depressão/Singapura sem lista; Índia 2:21 = 26% assistido.
9. **Micro-diálogo (1–2 falas curtas) nas cenas-chave**, como discurso direto dito pelo narrador. *Evidência:* Crayon, 3 vídeos com 1,2–4,3 mi. **Hipótese** (precisa testar no drama-3 se soa natural com uma voz só).
10. **Ritmo: frases curtas nas viradas (5–8 palavras) e alvo de ~140–145 ppm**; com o drama-3, encurtar pausas ou o texto (16 min ≈ 2.250 palavras a 140 ppm). *Evidência:* menor ppm entre as referências = 137 (HnM, voz humana); nós 129–136. **Hipótese** (cruzar com `voz.md` antes).
11. **Fecho ≤ 45 s depois do payoff**: responde, reenquadra, pergunta para os comentários e acaba. Sem resumão de eras. *Evidência:* Kelevin, ArchLang hit, HnM.
12. **Checklist novo** (para a skill `roteiro`/`qa`): pergunta até ~0:50 · pergunta repetida ≥ 3× · ≤ 2 "guarde" · "você" ≥ 1/100 · conectivos ≥ 1,5/100 · 1 cena por capítulo · nenhum capítulo abre com sucessão seca. Dá para medir com `metricas_texto.py`.

**Fora do roteiro (para não atribuir ao texto o que é embalagem):** os dois casos do grupo C mostram que **tema + título explicam a maior parte da diferença** (o Egito fez 568 mil no Kelevin, 397 no ArchLang e 91 em nós com roteiros razoáveis nos três). Com CTR < 2%, a thumb/título continuam a alavanca nº 1. Sugestão para a `titulo.md` (testar, Hipótese): título com pergunta/ameaça ao lado do "INTEIRA" ("Como o Irã sobreviveu a todos os impérios?") e a pergunta central do roteiro igual à do título, como faz a HnM ("Como a dinastia MAIS PODEROSA da Europa perdeu tudo").

## 6. Trecho de exemplo: Irã, primeiros ~90 s (original × reescrito)

Original: `videos/003-ira/SCRIPT.md` N001–N011 (na `legendas.srt`: "Essa é a história" aos 0:51, pergunta aos 1:25, capítulo 1 aos 1:32). Fatos iguais aos do `SOURCES.md` do 003; tempos do reescrito estimados a 127 ppm (drama-3).

**Hook**
| Original (003 v2): 203 palavras, 1 "guarde", 0 "você", cap. 1 aos 1:32 | Reescrito: ~155 palavras, pergunta aos ~0:50, cap. 1 aos ~1:13 (mudanças nº) |
|---|---|
| Pérsia, quinhentos e vinte e dois antes de Cristo. Seis nobres têm um problema: quem vai governar o maior império do mundo? A solução é… estranha. | Pérsia, quinhentos e vinte e dois antes de Cristo. Imagine que você é um dos seis nobres que vão escolher o rei do maior império do mundo. *(4)* |
| Ao nascer do sol, os seis vão sair a cavalo, e o dono do cavalo que relinchar primeiro vira rei. | O método: ao nascer do sol, todos saem a cavalo. O cavalo que relinchar primeiro… faz do dono um rei. *(10)* |
| Um deles se chama Dario, e Dario tem um cavalariço esperto. Na noite anterior, ele leva o cavalo até aquele lugar exato, junto com uma égua. De manhã, o cavalo passa por ali, sente o cheiro… e relincha. | Só que Dario tem um cavalariço esperto. Na véspera, ele leva o cavalo até aquele ponto… com uma égua. De manhã, o cavalo passa ali, lembra da noite… e relincha. *(3)* |
| Dario vira rei de um império que ia do Egito até a fronteira da Índia. Um império escolhido, literalmente, por um cavalo. Pelo menos, é assim que Heródoto conta. | Dario vira rei do Egito à Índia, escolhido por um cavalo… e por uma trapaça. Pelo menos segundo Heródoto. Um grego. E grego não era exatamente fã de persa. *(6)* |
| Essa é a história inteira do Irã. Um país invadido por gregos, árabes, mongóis e turcos, e que, toda vez, acabou ensinando os invasores a viver como persas. | Fica a pergunta: **quem escolhe quem governa o Irã?** Gregos, árabes, mongóis, britânicos e americanos vão tentar escolher por ele. E o Irã continua Irã. Como? *(1)* |
| No caminho, tem um rei que devolvia os deuses dos vencidos, um imperador romano capturado vivo, o caixão de um poeta que salvou uma língua… e um contrato de tabaco que derrubou uma coroa, oitenta e oito anos antes de derrubar outra. | *(cortado: 8, promessa em lista)* |
| E o que esse cavalo tem a ver com o Irã de hoje? Guarde esse cavalo. Ele volta no final. | Essa é a história inteira do Irã. Guarde esse cavalo: ele volta no final. E tudo começa com um problema menos nobre que um trono. Água. *(7; 3: o problema que abre a era)* |

**Começo do capítulo 1**
| Original (N009–N011) | Reescrito |
|---|---|
| Mas, antes de qualquer rei, alguém precisou achar água. O planalto do Irã é uma tigela de montanhas, com deserto no meio e pouca chuva. Como é que se vive aqui? | Olhe para o planalto do Irã: uma tigela de montanhas, deserto no meio, quase nenhuma chuva. Se você chegasse aqui há seis mil anos, a pergunta não seria quem manda. Seria: onde é que eu bebo? *(4, 5)* |
| Os antigos persas foram buscar a água embaixo da terra. São os qanats, túneis de quilômetros, tão bem inclinados que a água da montanha desce sozinha. Alguns correm há mais de dois mil anos. | A resposta foi cavar. Túneis de quilômetros, os qanats, inclinados na medida para a água da montanha descer sozinha. Alguns funcionam há mais de dois mil anos. Tente isso com o encanamento do seu prédio. *(4, 6)* |
| Onde o túnel terminava, a água virava um jardim murado, que em persa antigo se chamava pairidaêza. Guarde essa palavra. Ela passou pelo grego, passou pelo latim… e chegou ao português como paraíso. *(depois: elamitas e a escrita decifrada em 2022; "Guarde isso" sobre o nome Pérsia)* | Onde o túnel acabava, nascia um jardim murado: *pairidaêza*. A palavra viajou pelo grego, pelo latim… e chegou até você como **paraíso**. Só que todo paraíso no deserto tem um problema: os vizinhos também querem. *(7: sem "guarde"; 5: elamitas saem; 3: gancho da próxima era)* |

Saldo: hook 25% mais curto, pergunta de verdade 35 s mais cedo, 1 "guarde" no lugar de 2 até os 2:10 (o 3º, sobre o nome Pérsia, vem aos 3:06), "você" de 0 para 5. Perde-se a lista de promessas (o imperador romano e o contrato de tabaco viram mini-hooks dos capítulos deles). Antes de adotar, gerar estes 60–90 s no drama-3 e medir a repetição melódica (`v2-amostras/voz/medir.py`), como manda a `biblia/roteiro.md`.
