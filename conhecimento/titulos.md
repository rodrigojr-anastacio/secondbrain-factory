# Títulos: regras gerais

> **Regras gerais. Regra de canal está em `canais/<slug>/biblia/` e sempre prevalece.** A fórmula de título de cada canal, com dados, está em `canais/<slug>/biblia/titulo.md`: `historia-ptbr` = "A história INTEIRA de X em N minutos"; `dossie-es` = "TODA la historia de <organización> en N minutos"; `lotr-fr` = pergunta curiosa.

**Como atualizar:** **Tendências** (títulos que viralizam lá fora), **Métricas** (views, % assistido e o CTR do Studio que o Rodrigo passar) e **feedback do Rodrigo**. Padrão de um canal vai para a bíblia dele. Cada entrada leva **data e fonte**; sem dado = **Hipótese**. Commit descritivo.

Última revisão: 2026-11-04 (caixinhas por canal: fórmulas e dados por canal movidos para as bíblias).


> **Lente de apoio (não é regra):** antes de propor, passe a ideia pelas 5 condições de decisão por atalho em `conhecimento/decisao-do-clique.md` (09/11/2026).
---

## Regras gerais
**Faça**
- **Uma fórmula fixa por canal**, escrita na bíblia, e use sempre a mesma: a repetição gera reconhecimento na grade. Caso Genius History: com temas genéricos fazia ~5 mil views; ao adotar a fórmula "The ENTIRE History of X in N Minutes", foi para 70 mil–900 mil por vídeo. **A fórmula é a tendência.** [`pesquisa/tendencias/2026-11-02.md`; playbooks/garimpo-tendencias.md]
- Se o título tem **N minutos, N = duração real arredondada**; se a duração mudar, troque o N no título, na descrição e no banco. [ETAPA2.md e ETAPA3.md historia-ptbr 001]
- Título e thumb são uma dupla: a thumb leva 2–3 palavras e o resto fica no título; não repita o título inteiro na arte.
- Título ≤ 100 caracteres, no idioma do canal.
- Teste de título (alternativa A/B) só dentro da fórmula do próprio canal.

**Não faça**
- Não use a fórmula de outro canal (ver bíblia de cada um).
- Não republique nem troque título sem registrar em `youtube.videos` e no `backlog.md` do canal (em 04/11 o banco ainda guardava o ID morto do Egito). [`conhecimento/anti-padroes.md` §6]

## Referência de mercado (geral)
- "The ENTIRE History of X in N Minutes" é a fórmula dominante do garimpo de 2026-11-02: Archive in Minutes (1º vídeo em 2026-10-14, 17 vídeos, 1,55 milhão de views), CountryCorns (Israel 1,14 milhão), History in Minutes, Genius History. Ela é usada por **dois** canais nossos, cada um com seu X (país × organização) e seu idioma. [`pesquisa/tendencias/2026-11-02.md`; `youtube.assistidos`]
- **Hipótese:** o tema decide mais que o título dentro da mesma fórmula (Archive: organizações famosas, mediana 146 mil, × eventos/estados, 38 mil). [LEVANTAMENTO archive-in-minutes §2a]

## O que saiu daqui em 2026-11-04 (e para onde foi)
- "INTEIRA" × "COMPLETA" (Egito republicado, Índia) e a fórmula do historia-ptbr → `canais/historia-ptbr/biblia/titulo.md`.
- Tabela "pergunta curiosa × biografia" do lotr-fr → `canais/lotr-fr/biblia/titulo.md`.
- Fórmula "TODA la historia…" e temas que performam no Archive → `canais/dossie-es/biblia/titulo.md`.

## Regra do Rodrigo (12/11/2026): sempre 3 títulos, com gatilhos diferentes
Todo vídeo sai com **3 títulos** para o "Testar e comparar", cada um com um **gatilho emocional diferente**, não 3 perguntas parecidas. Combinar entre:
- **Curiosidade/pergunta:** "Why Can't You Visit Midway Atoll?"
- **Afirmação/prova:** "7 tornados em 6 dias no Sul do Brasil. Isso não é normal"
- **Promessa/utilidade com prazo:** "El Niño 2026: o que muda na sua região até março"
- **Lacuna com reticências:** "Super El Niño: ele vai fazer isso com o Brasil neste verão..."
- **Choque/número, proibido/segredo, perda/medo, contraste antes×depois.**
Cada título casa com uma das 3 thumbs (o Rodrigo testa pares título+thumb). Fonte: Rodrigo, 12/11/2026, nos A/B do Em Relevo 001/002.

## Políticas do YouTube (14/11/2026, Rodrigo)
Título, descrição e tags **sem** morte/morreu/morto/assassinado/assassinato (es: muerte/murió/muerto/asesinado/asesinato; en: death/died/dead/killed/murdered/assassinated/murder) nem sinônimos chocantes (massacre, chacina, "chocante", "perturbador", "nojento"). Os exemplos de referência abaixo que contêm essas palavras (ex.: "Lincoln's Death") são só dados de mercado: **não copie a palavra**. Detalhe e substituições: `conhecimento/politicas-youtube.md`.

## Método (12/11/2026): título se modela das referências, não se inventa
Regra do Rodrigo: "o que manda é o cara clicar: thumb boa + título bom". Antes de escrever título, **puxe os títulos das referências do canal com views** (`youtube.garimpo_videos` ou yt-dlp) e use os padrões que mais renderam. Título bom **mostra algo estranho/proibido/escondido e não entrega a resposta** (abre um loop). Título que já responde ("The Ships Are Still Down There", "Now the Birds Own It") **não gera clique**.

Exemplo de tabela de padrões (Where They Stood + Civil War Fine Print, 12/11/2026):
| Padrão | Exemplo real | Views |
|---|---|---|
| Why Can't You Visit X? | Why Can't You Visit Iwo Jima? | 4,5 mi |
| The X You Weren't Supposed to See | The Pictures of Lincoln's Death You Weren't Supposed to See | 879 mil |
| What's Still Under/In X? | What's Still Under the Water at Omaha Beach? | 340 mil |
| Why Is [país] Still Digging Up X? | Why Is America Still Digging Up Normandy? | 119 mil |
| What Happened to the Real X? | What Happened To The Real Hacksaw Ridge? | 94 mil |
| Why Is There a [coisa estranha] in [lugar]? | Why Is There a Japanese Submarine in Alaska? | 33 mil |
Palavras-gatilho recorrentes: **still**, **can't**, **weren't supposed to**, **real**, coisa concreta e estranha (submarino, 400 nukes, B-52 num lago).
Cada bíblia de canal deve ter a **sua** tabela de padrões das referências (atualizar a cada garimpo). Os 3 títulos do "Testar e comparar" saem de 3 padrões diferentes da tabela, cada um pareado com uma thumb.
