# Título: historia-ptbr

Regra de canal: **prevalece** sobre `conhecimento/titulos.md`. Data e fonte em toda entrada; sem dado = **Hipótese**.

## Fórmula
- **"A história INTEIRA de X em N minutos"**: decisão do Rodrigo no `BRIEF-historia-003.md` (04/11/2026), INTEIRA e não COMPLETA. A palavra de destaque em **caixa alta**, como o "ENTIRE" da referência. [canal.yaml; títulos em `youtube.assistidos`]
- **N = duração real arredondada.** Se a duração mudar (v2), troque o N no título, na descrição e no banco. A v1 do Egito era "em 16 minutos" (15:54) e virou 17:00 com as pausas novas. [ETAPA2.md e ETAPA3.md 001]
- X = país, império ou civilização (nunca organização: isso é do `dossie-es`).
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
