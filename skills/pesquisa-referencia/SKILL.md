---
name: pesquisa-referencia
description: Use ao iniciar um vídeo novo da fábrica do YouTube (ou ao estudar um concorrente) para escolher e "assistir" o vídeo de referência, criar a linha em youtube.videos, a pasta do vídeo e escrever o BRIEF.md com hook real, duração-alvo e teto de custo. Também serve ao Tendências para analisar referências.
---

# pesquisa-referencia: referência + BRIEF.md

Raiz do repo: `~/workspace/fabrica-youtube` (todos os caminhos abaixo são relativos a ela). Python: `tools/.venv/bin/python`.
Procedimento-base: `playbooks/produzir-video.md` §0–1.

## Antes de agir
0. **Primeiro a bíblia do canal** (caixinha): `canais/<slug>/biblia/README.md` (canal-modelo e "o que NÃO fazer aqui") e toda a `biblia/` (sobretudo `roteiro.md` e `titulo.md`: canal-modelo, fórmula, duração). A bíblia **prevalece** sobre `conhecimento/` (só regras gerais). Nunca aplique padrão de outro canal.
1. Leia `MAPA.md`, `canais/<slug>/canal.yaml` e `canais/<slug>/backlog.md`.
2. Regras gerais: `conhecimento/titulos.md`, `conhecimento/hooks.md`, `conhecimento/roteiros.md` e `conhecimento/anti-padroes.md`.
3. Veja o que já foi garimpado: o relatório mais recente em `pesquisa/tendencias/*-analise.md` e
   `psql -d vida -c "SELECT video_id, titulo, canal, duracao_s, cortes_por_min, analisado_em FROM youtube.assistidos ORDER BY analisado_em DESC LIMIT 20"`.

## Passos
1. **Escolha a referência:** um vídeo que performou, **do canal-modelo da bíblia** (ou de um canal com o mesmo formato), com a mesma fórmula do canal. Referência de outro formato (ex.: Archive in Minutes para o historia-ptbr) não serve de molde de estrutura. Registre views, idade e duração (tração = views/idade).
2. **Assista:** `tools/.venv/bin/python tools/watch.py <YOUTUBE_ID>` (via WARP; grava em `youtube.assistidos` e em `pesquisa/tendencias/assets/<data>/<id>/`: hook transcrito, frames, ritmo, anúncios).
   Se for remodelar a estrutura inteira, transcreva: `tools/.venv/bin/python tools/transcrever.py <YOUTUBE_ID> <pasta-do-video>/ref/transcricao.txt [idioma]`.
3. **Crie a linha do vídeo** (o id é usado em todo custo):
   ```sql
   INSERT INTO youtube.videos (canal_slug, numero, titulo, status, pasta)
   VALUES ('<slug>', <N>, '<título de trabalho>', 'ideia', 'canais/<slug>/videos/<NNN-slug>') RETURNING id;
   ```
   **historia-ptbr ≥ 006:** grave também a versão da bíblia de roteiro: `UPDATE youtube.videos SET biblia_versao='v2' WHERE id=<id>` (001–005 = `'v1'`; ver `canais/historia-ptbr/biblia/README.md`). No `BRIEF.md`, a pergunta central candidata e as regras da v2 de `biblia/roteiro.md`.
4. **Crie a pasta** `canais/<slug>/videos/NNN-slug/` copiando o setup do vídeo mais recente do mesmo canal **sem** `node_modules`, `out/`, `audio/`, `imagens/` (ex.: `rsync -a --exclude node_modules --exclude out --exclude audio --exclude imagens --exclude qa --exclude logs <anterior>/ <novo>/`). Não copie BRIEF/SCRIPT/ETAPA do anterior.
5. **Escreva `BRIEF.md`** com: tema; título de trabalho (fórmula de `biblia/titulo.md`); duração-alvo e nº de palavras (tabela "Tamanho" de `biblia/roteiro.md`); **link para a bíblia do canal** (`canais/<slug>/biblia/`) e as 3 regras dela que mais importam neste tema; idioma; referência (ID, views, idade, duração, hook real transcrito, estrutura em capítulos, cortes/min); fio condutor e loops candidatos; **teto de custo em US$** (voz + imagens + thumb; base real em `conhecimento/anti-padroes.md`); critérios de pronto e restrições do canal.
6. Atualize `canais/<slug>/backlog.md` (item em produção).

**Próximo passo obrigatório (desde 14/11/2026):** a skill `embalagem` (título + thumb + crivo) roda **antes** do roteiro, a partir deste BRIEF. Por isso o BRIEF precisa trazer as **fontes** principais e os fatos fortes do tema (a promessa da embalagem tem de ser cumprível com eles). O título de trabalho aqui é provisório: o título real sai do `EMBALAGEM.md` aprovado.

## Critérios de pronto (avaliar)
- A referência tem tração comprovada (views/idade anotados) e é da mesma fórmula.
- O hook real da referência está transcrito no BRIEF (não traduzido para uso; só para modelar).
- Título de trabalho sem as palavras proibidas (morte/morreu/assassinado e equivalentes; `conhecimento/politicas-youtube.md`), e a pauta não depende de foto/vídeo real de cadáver (se depender, descarte ou mude o ângulo).
- Título de trabalho segue a fórmula de `canais/<slug>/biblia/titulo.md`; a referência é do canal-modelo da bíblia.
- Duração-alvo, nº de palavras e **teto de custo** explícitos.
- Fontes principais e 3–6 fatos/casos fortes listados (matéria-prima da promessa da `embalagem`).
- `youtube.videos` tem a linha (id anotado no topo do BRIEF) e a pasta existe sem `node_modules` copiado.

## Loop de melhoria
1. **Avaliar:** confira cada critério acima; marque o que falhou.
2. **Corrigir:** no máximo 2 rodadas (ex.: trocar a referência por uma com mais tração). O que sobrar vira pendência no BRIEF.
3. **Registrar:** padrão novo de hook/título/estrutura visto na referência vai para a **bíblia do canal que usa esse formato** (`canais/<slug>/biblia/roteiro.md` ou `titulo.md`) com **data e fonte** (ID do vídeo); só vai para `conhecimento/` se valer para qualquer canal. Sem dado próprio de retenção/CTR, marque **Hipótese**.
4. **Commitar:** `git add <arquivos tocados>` (só texto; mídia fica fora do git) e
   `git commit -m "<canal>/<NNN>: BRIEF com referência <ID> e teto US$ X"` (aprendizado em commit próprio: `<canal>/biblia: ...`).
