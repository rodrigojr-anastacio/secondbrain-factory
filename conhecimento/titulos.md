# Títulos: padrões que funcionaram e que não funcionaram

**Como atualizar:** alimentado por **Tendências** (títulos que viralizam lá fora, de `pesquisa/tendencias/`), **Métricas** (views, % assistido e, quando o Rodrigo passar, CTR do YouTube Studio) e **feedback do Rodrigo**. Cada entrada leva **data e fonte**. Sem dado, marque **Hipótese**. Depois de editar, faça commit descritivo.

Última revisão: 2026-11-04 (base inicial, Fase 1).

---

## Regras rápidas

**Faça**
- historia-ptbr: siga a fórmula da referência, "A HISTÓRIA COMPLETA de X em N minutos" ou "A história INTEIRA de X em N minutos", com **N = duração real arredondada**. Se a duração mudar (v2), troque o N no título, na descrição e no banco. [canal.yaml historia-ptbr; ETAPA3.md 001]
- A palavra de destaque vai em **caixa alta** ("COMPLETA"/"INTEIRA"), como o "ENTIRE" da referência. [títulos das referências em `youtube.assistidos`]
- lotr-fr: título em **pergunta curiosa** ("Pourquoi…?", "Que s'est-il passé…?", "Quelles étaient…?"). [canal.yaml lotr-fr; estilo.md lotr-fr]
- Mantenha o título coerente com a thumb: a thumb leva 2–3 palavras (o lugar), e o resto fica no título. [estilo.md historia-ptbr]

**Não faça**
- Não deixe o N do título diferente da duração: a v1 do Egito era "em 16 minutos" (15:54) e, com as pausas novas, virou 17:00; o título teve de mudar. [ETAPA2.md e ETAPA3.md 001]
- Não republique trocando o título sem registrar no banco e no backlog: hoje `youtube.videos` (id 3) ainda guarda o título "COMPLETA" e o ID antigo `s-D5Sk7prJI`, que está indisponível. [consulta de 2026-11-04]

---

## "INTEIRA" × "COMPLETA" (historia-ptbr)

**O que aconteceu (fatos):**
- Todos os briefs e pacotes usam **"A HISTÓRIA COMPLETA"**. [BRIEF.md 001 e 002; out/youtube.txt 001 e 002; canal.yaml]
- O Egito foi publicado em 2026-11-03 como `s-D5Sk7prJI` com "A HISTÓRIA COMPLETA do Egito em 17 minutos" (`youtube.videos` id 3). Em 2026-11-03, o vídeo tinha 0 views (`youtube.metricas_video`). Em 2026-11-04, esse ID **não aparece mais** na coleta e o oEmbed público responde como indisponível.
- Em 2026-11-04, o canal tem 2 vídeos (`youtube.metricas_canal`, UCpw08sVZG1QZp-3spPcwWxQ). Pelo oEmbed público (consultado via WARP em 2026-11-04), eles são:
  - `g847Td0Plsk`: **"A história INTEIRA do Egito em 17 minutos"**, com 6 views;
  - `MV5SSjoccqE`: **"A HISTÓRIA COMPLETA da Índia em 19 minutos"**, com 17 views.
- Ou seja, o Egito foi **republicado com "INTEIRA"** (tradução literal do "ENTIRE" da referência), e a Índia saiu com "COMPLETA".

**O que ainda não sabemos:**
- **Hipótese:** "INTEIRA" está mais perto do gatilho da referência ("The ENTIRE History of…"). Não há registro escrito do motivo da troca nem do autor (Rodrigo?). Pergunte e registre aqui.
- **Sem dado** para comparar: os 2 vídeos têm 1 dia, views de um dígito ou dois, sem CTR e sem retenção. Compare depois de 7 dias (views, CTR do Studio e % assistido), lembrando que o tema também muda (Egito × Índia).

## Referências de título (Tendências)
Fonte: `pesquisa/tendencias/2026-11-02.md` e `youtube.assistidos` (2026-11-02).
- "The ENTIRE History of X in N Minutes" é a fórmula dominante: Archive in Minutes (1º vídeo em 2026-10-14, 17 vídeos, 1,55 milhão de views; Gestapo 310 mil, KGB 234 mil, SS 196 mil) e CountryCorns (Israel 1,14 milhão).
- Caso Genius History: com temas genéricos fazia ~5 mil views; ao adotar a fórmula, foi para 70 mil–900 mil por vídeo. Lição: **a fórmula é a tendência**. [playbooks/garimpo-tendencias.md]

## lotr-fr: pergunta curiosa × biografia
Fonte: `youtube.metricas_video` em 2026-11-04 (títulos pelo oEmbed público em 2026-11-04; duração ≈ média assistida ÷ % assistido).

| Título | Views | ~Duração | % assistido |
|---|---|---|---|
| Que s'est il passé avec les orcs après que l'Anneau a été détruit | 16.301 | ~15 min | 33,99% |
| Pourquoi Frodon a-t-il dû quitter la Terre du Milieu ? | 7.096 | ~8,5 min | 48,19% |
| L'histoire de l'anneau de pouvoir | 1.979 | ~7,7 min | 47,06% |
| L'histoire complète des Nazgûl \| J.R.R Tolkien | 1.741 | ~8,8 min | 48,23% |
| L'Histoire De La Moria (Khazad-Dûm) - Le royaume des nains | 526 | ~12,9 min | 43,71% |
| L'histoire complète de Legolas | 408 | ~15,3 min | 41,31% |
| Les voyages complets de Legolas | 80 | ~15,3 min | 30,00% |
| **Quelles étaient les plus grandes villes de la Terre du Milieu ?** (nosso 001) | 54 | 8,3 min | 49,74% |

- Fato: os vídeos de ~8 min retêm ~47–50%; os de ~13–15 min, 30–44%. [mesma consulta; estilo.md lotr-fr]
- Fato: o maior volume de views é de um título em pergunta ("Que s'est il passé…", 16 mil), apesar da retenção de 34%.
- **Hipótese:** pergunta curiosa + ~8 min é a melhor combinação para o canal. Os dados de views misturam idade dos vídeos e algoritmo; não é causal.
- A ideia do backlog "L'HISTOIRE COMPLÈTE de Númenor" (fórmula do historia-ptbr) ainda **não foi testada**. [backlog.md lotr-fr]
