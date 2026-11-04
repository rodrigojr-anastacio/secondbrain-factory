# Títulos: regras gerais

> **Regras gerais. Regra de canal está em `canais/<slug>/biblia/` e sempre prevalece.** A fórmula de título de cada canal, com dados, está em `canais/<slug>/biblia/titulo.md`: `historia-ptbr` = "A história INTEIRA de X em N minutos"; `dossie-es` = "TODA la historia de <organización> en N minutos"; `lotr-fr` = pergunta curiosa.

**Como atualizar:** **Tendências** (títulos que viralizam lá fora), **Métricas** (views, % assistido e o CTR do Studio que o Rodrigo passar) e **feedback do Rodrigo**. Padrão de um canal vai para a bíblia dele. Cada entrada leva **data e fonte**; sem dado = **Hipótese**. Commit descritivo.

Última revisão: 2026-11-04 (caixinhas por canal: fórmulas e dados por canal movidos para as bíblias).

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
