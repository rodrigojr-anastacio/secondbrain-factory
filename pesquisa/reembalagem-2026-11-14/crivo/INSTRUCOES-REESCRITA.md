# Reescrita única (rodada 2) — reembalagem 14/11/2026

Você reescreve as propostas reprovadas no crivo rodada 1. **Só há uma reescrita**: o que reprovar de novo sai da lista. Responda em pt-BR. Repo `~/workspace/fabrica-youtube`. Tudo em primeiro plano. Siga ainda as regras de `pesquisa/reembalagem-2026-11-14/INSTRUCOES-PESQUISA.md` (custo zero, WARP, sem `search.list` além de no máx. 2 por vídeo, sem imagem paga, sem commit, só escrever em `pesquisa/reembalagem-2026-11-14/`).

Para cada vídeo do seu prompt:
1. Leia `crivo/entrada/<nome>.md` (proposta original) e `crivo/<nome>-r1.md` (parecer do revisor).
2. Reescreva **só os elementos reprovados** (Título 1, Título 2 e/ou Thumb), atendendo à "Correção pedida" ou a uma alternativa melhor com evidência. Elementos aprovados: mantenha, aplicando os "ajustes obrigatórios"/ressalvas que o revisor marcou.
3. Corrija a evidência: **medianas reais** dos canais (últimos ~30–50 uploads via `playlistItems` + `videos.list`), ≥ 2 referências reais do mesmo padrão, no mesmo nicho/idioma, acima da mediana do canal delas, com link, views e data conferidos por `videos.list`. Se não achar 2 referências legítimas para um padrão, troque de padrão.
4. Confira cada timestamp na `legendas.srt` (cite a frase). Promessa paga cedo, de preferência no 1º minuto; não prometa o vídeo inteiro sobre algo que ocupa 1 minuto.
5. Mantenha **1 conceito de thumb** que case com os **dois** títulos (não repete nenhum deles; juntos criam pergunta), legível a 320×180 (≤ 3 palavras, 1 foco). Regras de `conhecimento/politicas-youtube.md`, ≤ 100 caracteres (e o teto da bíblia do canal, se houver), sem cópia de fórmula de clone/referência no mesmo tema.
6. Grave `crivo/entrada/<nome>-v2.md` **autossuficiente** (o revisor da rodada 2 é outra pessoa e só lerá este arquivo, a legenda e o mosaico): atual (título, impressões, CTR, retenção), Título 1, Título 2, Thumb, cada um com padrão + referências (tabela: link, canal, views, data, mediana real do canal, ×mediana) + pagamento (timestamp + frase) + marcação `[MANTIDO]` ou `[REESCRITO: motivo da reprovação r1 → o que mudou]`. Inclua a evidência do padrão de thumb e qualquer "desvio da bíblia: … porque …".

Resposta final: 1 linha por vídeo com os títulos finais e o texto da thumb.
