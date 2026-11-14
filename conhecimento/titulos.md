# Títulos: regras gerais

> **Regras gerais. Regra de canal está em `canais/<slug>/biblia/` e sempre prevalece.** A fórmula de título de cada canal, com dados, está em `canais/<slug>/biblia/titulo.md` (`historia-ptbr`, `dossie-es`, `lotr-fr`, `lugares-guerra-en`; Em Relevo em `pesquisa/canal-clima-2026-11/biblia-titulo.md`). A fórmula fica na bíblia e muda com dado; a etapa de **embalagem** (skill `embalagem`, 14/11/2026) mede a colisão da fórmula com os clones no tema antes de usá-la (ex.: "A história INTEIRA de X" e "TODA la historia de X" só onde o tema ainda não existe nela). `lotr-fr` = pergunta curiosa.

**Como atualizar:** **Tendências** (títulos que viralizam lá fora), **Métricas** (views, % assistido e o CTR do Studio que o Rodrigo passar) e **feedback do Rodrigo**. Padrão de um canal vai para a bíblia dele. Cada entrada leva **data e fonte**; sem dado = **Hipótese**. Commit descritivo.

Última revisão: 2026-11-14 (embalagem + crivo; antes, 2026-11-04: caixinhas por canal, fórmulas e dados por canal movidos para as bíblias).


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

## Embalagem + crivo (14/11/2026)
Todo vídeo novo passa por `skills/embalagem/` (2 títulos + 1 conceito de thumb + promessa, com pesquisa real no YouTube) e por um crivo independente (`skills/embalagem/CRIVO.md`) **antes do roteiro** (decisão do Rodrigo, 14/11/2026). Na reembalagem dos 15 vídeos publicados o crivo reprovou 19 de 45 elementos na r1 e aprovou 45 de 45 na r2 (`pesquisa/reembalagem-2026-11-14/PROPOSTAS.md`). Só entra aqui o que apareceu em **2+ canais**; o resto fica na bíblia do canal.
- **A promessa do título é paga cedo e sustentada pelo vídeo inteiro.** Reprovaram: título de um caso só num vídeo de vários (dossie-es: MiG ~80 s de 13:43, Paraguas ~75 s), curiosidade resolvida em segundos (historia-ptbr: Cleópatra × iPhone, 6 s), promessa paga só no fim (historia-ptbr: "como Roma caiu", queda aos 12:47) e subtítulo que o vídeo não paga (dossie-es: "Los Archivos Secretos de Hoover", ~15 s). Em Relevo teve a mesma ressalva (pagamento do T2 em 4:12 e 5:02). A promessa vira obrigação escrita para o roteiro. [`PROPOSTAS.md` (a) e (b)]
- **Colisão de fórmula com clones no mesmo tema** conta como cópia: o N diferente não diferencia. historia-ptbr: "N anos em N minutos" colidiu no Egito (7 títulos) e no Brasil (7); dossie-es: "TODA la Historia… | subtítulo" fica na mediana onde o Atlas já fez o tema (CIA 1.055). Medir a colisão (yt-dlp via WARP) antes de fechar o título. [`pesquisa/reembalagem-2026-11-14/padroes.md`; `pesquisa/gap-2026-11-14/RELATORIO.md` gap 2]
- **Referências medidas, não de olho:** ≥ 2 vídeos reais com o mesmo padrão, mesmo nicho e idioma, ≤ ~400 d, **acima da mediana real** do canal deles (últimos 50 uploads via `playlistItems` + `videos.list`; o script `skills/embalagem/scripts/pesquisa_embalagem.py` calcula). As medianas "de olho" da r1 erraram em vários canais. [`padroes.md`, cabeçalho]
- **Título e thumb são uma dupla que cria uma pergunta**: a thumb não repete palavra do título (reprovações em historia-ptbr: Rússia e Irã; dossie-es: KGB e FBI). Detalhe em `conhecimento/thumbnails/README.md`.
- **Notícia, pergunta crua de tema e promessa vaga** saem do título nos 3 canais da reembalagem (pergunta crua é commodity em pt; "o detalhe que ninguém conta" no Em Relevo; "Lo que NO te contaron" no dossie-es). Entra um 2º elemento concreto (objeto, agente, anomalia).

### Próximo passo (não implementado)
**Eval automático do crivo da embalagem:** usar o histórico `embalagem/crivo-r*.md` (e `EMBALAGEM-r*.md`) + o CTR/retenção do Studio dos vídeos publicados para calibrar a régua do crivo. Decisão do Rodrigo de 14/11/2026: deixar para um segundo momento.
