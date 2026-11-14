# Título: historia-ptbr

Regra de canal: **prevalece** sobre `conhecimento/titulos.md`. Data e fonte em toda entrada; sem dado = **Hipótese**.

## Fórmula
- **"A história INTEIRA de X em N minutos"**: decisão do Rodrigo no `BRIEF-historia-003.md` (04/11/2026), INTEIRA e não COMPLETA. A palavra de destaque em **caixa alta**, como o "ENTIRE" da referência. [canal.yaml; títulos em `youtube.assistidos`]
- **N = duração real arredondada.** Se a duração mudar (v2), troque o N no título, na descrição e no banco. A v1 do Egito era "em 16 minutos" (15:54) e virou 17:00 com as pausas novas. [ETAPA2.md e ETAPA3.md 001]
- X = país, império ou civilização (nunca organização: isso é do `dossie-es`).
- **Nuance (14/11/2026):** a fórmula vale **só onde o tema ainda não existe nela** no feed pt. Na reembalagem, "N anos de X em N minutos" colidiu no Egito (Atlas das Eras 70.238 views + 6 clones) e no Brasil (Atlas das Eras, Canal Nostalgia e mais 5) e passou na Índia e na China; 10+ canais pt usam "A história INTEIRA/COMPLETA de X em N minutos". Antes de fechar o título, a etapa de embalagem mede a colisão (yt-dlp); se colidir, usa outro padrão. [`pesquisa/reembalagem-2026-11-14/padroes.md` e `PROPOSTAS.md` (b) lição 3; `pesquisa/gap-2026-11-14/RELATORIO.md` gap 2]
- Título e thumb são uma dupla: a thumb não repete o título inteiro (ver `thumb.md`).

## TESTE (Hipótese, desde 07/11/2026, vídeos v2 ≥ 006): título-pergunta alinhado à pergunta central
O padrão **continua** "A história INTEIRA de X em N minutos". Nos vídeos da bíblia de roteiro v2, teste um **título em forma de pergunta ou ameaça igual à pergunta central do roteiro** (regra 1 de `roteiro.md`) como alternativa no "Testar e comparar" de título do Studio.
- *Por quê:* nos dois pares hit × fracos do relatório, **tema + título** explicam a maior parte da diferença; o hit do ArchLang (1,13 mi) é o único com o espectador em jogo no título ("Why Civilizations Collapse (And Why We Are **Next**)"), o hit do Breakdown (17,8 mil) é o único com curiosidade ("Impossible to Outrun — Research Reveals Why"), e a HnM põe a pergunta do vídeo no título ("Como a dinastia MAIS PODEROSA da Europa perdeu tudo", 150 mil). [`pesquisa/roteiro-historia-2026-11/RELATORIO.md` §3 e §5, 07/11/2026] Com CTR < 2% nos nossos, título/thumb seguem sendo a alavanca nº 1.
- **Como alternar** (Studio → vídeo → Título → "Testar e comparar", até 3 títulos; se o teste de título não estiver liberado, troque o título no dia 7 e compare 7 dias antes × 7 depois):
  - **A (padrão):** "A história INTEIRA do Irã em 18 minutos"
  - **B (pergunta = pergunta central):** "Quem escolhe quem governa o Irã? A história INTEIRA" / "Como o Irã sobreviveu a todos os impérios?"
  - **C (ameaça/curiosidade, opcional):** "O país que TODO império tentou engolir (e falhou)"
  - Regras: a pergunta do título é a mesma (ou o resumo) da `Pergunta central:` do `SCRIPT.md`; a palavra de destaque em caixa alta; ≤ 60 caracteres; a thumb não repete o título; se B não trouxer "em N minutos", a duração vai na descrição.
- **Registrar** no `youtube.videos.notas` qual título venceu e o CTR/views de cada braço (o Rodrigo lê no Studio) e aqui, com data. Só vira padrão com ≥ 3 vídeos em que B vença A.

## "INTEIRA" × "COMPLETA" (fatos)
- Os briefs e pacotes do 001/002 usavam "A HISTÓRIA COMPLETA". O Egito saiu em 2026-11-03 como `s-D5Sk7prJI` ("A HISTÓRIA COMPLETA do Egito em 17 minutos"), sumiu do ar e foi **republicado** como `g847Td0Plsk` "A história INTEIRA do Egito em 17 minutos". A Índia está no ar como `MV5SSjoccqE` "A HISTÓRIA COMPLETA da Índia em 19 minutos". [oEmbed via WARP e `youtube.metricas_canal`, 2026-11-04]
- **Hipótese:** "INTEIRA" está mais perto do gatilho da referência ("The ENTIRE History of…"). Sem dado para comparar (vídeos com 1 dia em 04/11). Comparar depois de 7 dias (views, CTR do Studio, % assistido), lembrando que o tema também muda.

## Referências do molde
- "The ENTIRE History of X in N Minutes" é a fórmula dominante no garimpo de 2026-11-02 (History in Minutes, Genius History, CountryCorns: Israel 1,14 milhão). [`pesquisa/tendencias/2026-11-02.md`]
- Caso Genius History: com temas genéricos fazia ~5 mil views; com a fórmula, 70 mil–900 mil por vídeo. [playbooks/garimpo-tendencias.md]

## Temas
- Países e impérios que performaram nas referências (views em 04/11/2026): China (Animated History 1,17 mi; HiM 55 mil), Roma (Genius History 364 mil), Japão (CountryCorns 115 mil), Rússia (HiM 42 mil), Ucrânia (HiM 178 mil), Império Britânico, Jerusalém. Lista viva em `../backlog.md`.

## Não faça
- N diferente da duração.
- Republicar ou trocar título sem atualizar `youtube.videos` e `../backlog.md` (o banco ficou com o ID morto do Egito até 04/11). [conhecimento/anti-padroes.md §6]
- Fórmula "TODA la historia…"/sigla de organização (é do `dossie-es`) ou pergunta curiosa solta, sem a pergunta central do roteiro (é do `lotr-fr`; o título-pergunta daqui só existe como braço B do teste acima).

## Padrões das referências (12/11/2026)
Fonte: yt-dlp via WARP (views de 12/11/2026, últimos ~80 vídeos de cada canal; o yt-dlp não dá data na lista, mas os canais são de 2026) de History in Minutes (2 canais), Ziro History, CountryCorns/Animated History, Atlas del Tiempo e Fragmentos da História (este é biografia, fora do molde: só serve de contraste). Método em `conhecimento/titulos.md`. Brutos em `pesquisa/padroes-titulos-2026-11-12.md`.

| Padrão | Exemplo real | Views | Canal |
|---|---|---|---|
| The ENTIRE History of [país/império grande] in N Minutes | The ENTIRE History of Israel in 10 Minutes | 1,1 mi | CountryCorns |
| idem, com recorte "From A to B" | The ENTIRE History of India, From Harappa to Today, in 16 Minutes | 637 mil | History in Minutes |
| idem (nosso molde exato) | The ENTIRE History of Egypt in 17 Minutes | 558 mil | History in Minutes |
| Why Did [A] Become Rich While [B] Stayed Poor? | Why Did the U.S. Become Rich While Latin America Stayed Poor? | 297 mil | Ziro History |
| idem, par de países vizinhos | Why South Korea Became Rich While North Korea Stayed Poor | 185 mil | Ziro History |
| Why Every Empire Wanted [X] (Full History) | Why Every Empire Wanted Ukraine (Full History) | 179 mil | History in Minutes |
| [X] Never Died. It Just Changed Its Name. | Persia Never Died. It Just Changed Its Name. (History of Iran) | 91 mil | History in Minutes |
| How [recurso] Decided Who Ruled [X] for N Years | How Water Decided Who Ruled China for 4,000 Years | 57 mil | History in Minutes |
| [País]: The [Superlativo] Country That Never Had [falta] | Russia: The Biggest Country That Never Had Enough People | 43 mil | History in Minutes |
| Why Did [A] Unite While [B] Stayed Divided? | Why Did Russia Unite While Europe Stayed Divided? | 41 mil | Ziro History |

**Os 5–6 que mais rendem:** (1) "ENTIRE History of [país grande]"; (2) "Why Did A … While B Stayed …" (contraste de destinos); (3) "Why Every Empire Wanted X"; (4) "X Never Died. It Just Changed Its Name."; (5) "How [recurso/geografia] Decided …"; (6) "[País]: o maior país que nunca teve …".
**O que têm em comum:** abrem uma **tensão sem fechar** (por que um enriqueceu e o outro não? por que todo império queria isso? como "morreu" e não morreu?). O padrão 1 só funciona com **país de enorme demanda** (Israel, Índia, Egito, Rússia): o tema decide, o título só não atrapalha.

**Leitura honesta:** os padrões 2–9 só aparecem nos canais maiores/melhores do molde (HiM usa o "ENTIRE" nos hits de demanda e o título-pergunta nos temas médios: 43–179 mil). Não dá para separar título de tamanho de canal com esses dados: **Hipótese** até testar.

**Regra (12/11/2026, Rodrigo): 3 títulos de 3 padrões diferentes, cada um pareado com uma thumb; nunca entregar a resposta.** Para o Irã, por ex.: A "A história INTEIRA do Irã em 18 minutos" (padrão 1) · B "A Pérsia nunca sumiu. Só mudou de nome." (padrão 7) [corrigido em 14/11/2026: o exemplo original usava "morreu", palavra proibida em `conhecimento/politicas-youtube.md`; pendência (c) de `pesquisa/reembalagem-2026-11-14/PROPOSTAS.md`. As linhas da tabela acima com "Never Died" são título de mercado em inglês, só dado: não copiar a palavra] · C "Por que todo império quis o Irã?" (padrão 6).

### Onde estamos fora do padrão (títulos no ar, `youtube.videos`; só registro, nenhum alterado)
- Os 7 títulos usam só o padrão 1 ("A história INTEIRA de X em N minutos", com "COMPLETA" na Índia). É o padrão certo, mas é o **único**: nunca testamos os de tensão (Why A… while B…, Never died, Every empire wanted), que rendem nos temas médios. Egito 343 e Índia 197 views vs. 558–637 mil na referência: o título é igual; a diferença está em canal novo e thumb (não nos títulos).
- Temas fora do que a referência prova: Brasil, Roma, Irã. Pedem o padrão 3/7 (tensão) em vez do "ENTIRE" puro, que depende de demanda do país.

## Políticas do YouTube (14/11/2026, `conhecimento/politicas-youtube.md`)
Título (e os 3 do "Testar e comparar"), descrição e tags **sem** morte/morreu/morto/assassinado/assassinato (es: muerte/murió/muerto/asesinado/asesinato; en: death/died/dead/killed/murdered/assassinated/murder) nem massacre/chacina/"chocante"/"perturbador"/"nojento". Troque por vítimas, baixas, atentado, golpe, caso. Na narração pode, com contexto factual.

## Embalagem antes do roteiro (14/11/2026)
Todo vídeo novo passa pela skill `embalagem` + crivo independente (`skills/embalagem/`) **antes** do roteiro; o hook paga a promessa (a pergunta central do roteiro v2). Fonte: decisão do Rodrigo, 14/11/2026; base `pesquisa/reembalagem-2026-11-14/padroes.md` e `PROPOSTAS.md` (seção historia-ptbr). Views e datas de 14/11/2026; "×med" = views ÷ mediana real do canal da referência.

### Padrões de título medidos (Hipótese (reembalagem 14/11/2026, CTR a medir): nenhum tem CTR nosso)
- **"Como [força/coisa concreta] [construiu/decidiu/derrubou/manteve] [lugar]"** (padrão 5 da bíblia): [O Império do Café: Como o Grão Construiu o Brasil Moderno](https://youtu.be/p0t7j7ish_E) 548.427 · 02/04/2026 · 6,4×; [A Peste Negra — Como uma bactéria derrubou a Europa medieval](https://youtu.be/rI1FNSy-75A) 606.866 · 10/02/2026 · 445× (canal pequeno).
- **"Por que [X] NUNCA [Y]?"** (só se for a pergunta central): [POR QUE ROMA NUNCA CONQUISTOU A ÍNDIA?](https://youtu.be/guiOxLd8X3M) 126.614 · 04/05/2026 · 4,1×; [Por que nunca entramos na maior tumba da Terra?](https://youtu.be/NCr1f_SUsLk) 754.669 · 01/03/2026 · 4,8×.
- **Afirmação estranha + pergunta:** [A China Esteve na Frente por 700 Anos. Então Por Que a Grã-Bretanha…](https://youtu.be/As5HdY_D-uI) 77.373 · 19/10/2026 · 2,1× (1,3× nos longos); [Mente Primata](https://youtu.be/kZ3YWuGWF0k) 396.452 · 04/10/2026 (nicho vizinho).
- **Pergunta de transformação + 2º gancho:** [POR QUE A PÉRSIA MUDOU SEU NOME PARA IRÃ…](https://youtu.be/jvM3cR235yw) 294.166 · 19/04/2026 · 7,2×; [Por Que a Pérsia Desapareceu — E em Seu Lugar Surgiu o Irã?](https://youtu.be/LwC-YJMsYuY) 62.529 · 04/03/2026.
- **Ascensão "Como [X] virou [o maior]?" com fato-surpresa:** [Como a Rússia ficou tão grande? A resposta é um animal…](https://youtu.be/wMFP6PadPmQ) 28.400 · 07/10/2026 · 27,2×; [A História de Roma: Como se Tornou o Maior Império do Mundo?](https://youtu.be/XyX7Y-xyhyg) 507.608 · 23/11/2025 · 11,9×.
- **Arco "subida + queda" / "De A a B":** [A Queda do Império Romano…](https://youtu.be/58Um0ZXSXx4) 288.553 · 15/05/2026 · 16,5×; [753 a.C. Império Romano - Da Fundação à Queda…](https://youtu.be/sLyfGzpuIGY) 203.687 · 09/01/2026 · 8,1×. Ressalva: refs fortes são documentários de 1h24–1h40; efeito em 17 min é Hipótese.
- **"O país que + fato estranho":** [IUGOSLÁVIA, O PAÍS QUE FOI APAGADO DA HISTÓRIA…](https://youtu.be/xuJ_ZVj7NS8) 168.837 · 02/12/2025 · 10,7×; [Dentro do País Que Não Deveria Existir…](https://youtu.be/fat8O0Ijc10) 1.246.159 · 28/06/2026 · 2,4× (nicho vizinho).
- **"[Lugar]: a terra que [contradiz o esperado]":** [Cuba: A Ilha Proibida Que Nenhum Império Conseguiu Apagar](https://youtu.be/iHEsS5GbpK4) 16.557 · 19/05/2026 · 13,8×; [A Terra Que Roma Nunca Conseguiu Conquistar](https://youtu.be/WTAjmGoUZFg) 15.724 · 28/09/2025 · 6,3×.
- **"N mil anos de X em N minutos"** só onde o tema não tem a fórmula: [IDADE MÉDIA: 1000 ANOS EM 78 MINUTOS](https://youtu.be/52TY3RdXIaM) 33.734 · 07/11/2026 · 38×; [História da igreja: 2.000 anos em 25 minutos](https://youtu.be/kPQz9fouO0Q) 119.145 · 22/10/2026 (nicho vizinho). Contra: Canal Nostalgia "CHINA / 5 MIL ANOS…" 1.430.851, abaixo da mediana dos longos.

### O que NÃO funciona neste canal
- **Fórmula dos clones** "A história INTEIRA/COMPLETA de X em N minutos": nosso Brasil era idêntico ao do História Inteira ([WcXwgbvbKMY](https://youtu.be/WcXwgbvbKMY)); o de Roma só mudava o N do HEG.
- **"N anos em N minutos" onde o tema já tem a fórmula:** Egito (Atlas das Eras [alBh1Urra80](https://youtu.be/alBh1Urra80) 70.238 + 6 clones) e Brasil (Atlas das Eras + Canal Nostalgia + 5). Trocar o N não diferencia.
- **Pergunta crua de tema:** 8 cópias de "Por que a Pérsia virou Irã" com 1–180 views; "Como a Rússia se tornou o maior país do mundo" com 1 view.
- **Moldura "sobreviveu a todos os impérios":** clone com 11 views; HiM "Korea Survived Every Empire" 1,4 mil.
- **Título-pergunta que não é a pergunta central** ou que se resolve em segundos: Egito T2 "Cleópatra × iPhone" (6 s) e China T2 "túmulo de Qin" (~35 s de 16 min) foram reprovados pelo crivo r1 (CTR alto, retenção baixa).
- **Prometer só a queda num vídeo de ascensão:** Roma T2 "…como Roma caiu?" (queda só aos 12:47), reprovado na r1; "Rome Never Really Fell" fica abaixo da mediana.
- **Título sem o nome do país** quando o gargalo é impressão (Rússia v1: "Pediram um rei viking…", reprovado, com viking + tamanho repetidos na thumb).
- **Fórmula de data repetida na thumb:** Brasil T1 "500 ANOS de Brasil em 17 minutos" colidia com 7 clones e repetia as datas da thumb (reprovado na r1).

### As 5 lições, adaptadas a vídeo novo (PROPOSTAS.md (b), 14/11/2026)
1. Título-pergunta só se for a pergunta central do roteiro v2 (≤ 60 caracteres), respondida pelo vídeo inteiro. Curiosidade de segundos ou loop secundário dá CTR alto com retenção baixa.
2. A pergunta crua de tema é commodity em pt: leva um 2º elemento-surpresa ("nunca virou árabe", o viking, o resgate).
3. Antes de fechar o título, buscar colisão no tema (yt-dlp). A fórmula "N anos em N minutos" e "A história INTEIRA" só entram se o tema ainda não existe nela.
4. "Como [agente concreto] [verbo] [lugar]" (padrão do canal-modelo) tem prova em pt; a pergunta central do roteiro v2 já é um título pronto.
5. Se o gargalo for impressão, o nome do país vai no título; a thumb leva a lacuna (ver `thumb.md`).
