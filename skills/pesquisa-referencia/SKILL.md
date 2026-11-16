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
1. **Escolha a referência:** um vídeo que performou, **do canal-modelo da bíblia** (ou de um canal com o mesmo formato), com a mesma fórmula do canal. Referência de outro formato (ex.: Archive in Minutes para o historia-ptbr) não serve de molde de estrutura. Registre views, idade e duração (tração = views/idade). **A referência é molde de FORMA (estrutura, hook, ritmo, transições), nunca de conteúdo:** a ordem dos beats, as anedotas e os números não vêm dela (16/11/2026; passo 7).
2. **Assista:** `tools/.venv/bin/python tools/watch.py <YOUTUBE_ID>` (via WARP; grava em `youtube.assistidos` e em `pesquisa/tendencias/assets/<data>/<id>/`: hook transcrito, frames, ritmo, anúncios).
   A transcrição completa sai no passo 7 (`tools/manada.py transcrever`, junto da manada); use-a para estudar a **forma** (tempo até a promessa, transições, loops, fecho), nunca como roteiro a reescrever.
3. **Crie a linha do vídeo** (o id é usado em todo custo):
   ```sql
   INSERT INTO youtube.videos (canal_slug, numero, titulo, status, pasta)
   VALUES ('<slug>', <N>, '<título de trabalho>', 'ideia', 'canais/<slug>/videos/<NNN-slug>') RETURNING id;
   ```
   **historia-ptbr ≥ 006:** grave também a versão da bíblia de roteiro: `UPDATE youtube.videos SET biblia_versao='v2' WHERE id=<id>` (001–005 = `'v1'`; ver `canais/historia-ptbr/biblia/README.md`). No `BRIEF.md`, a pergunta central candidata e as regras da v2 de `biblia/roteiro.md`.
4. **Crie a pasta** `canais/<slug>/videos/NNN-slug/` copiando o setup do vídeo mais recente do mesmo canal **sem** `node_modules`, `out/`, `audio/`, `imagens/` (ex.: `rsync -a --exclude node_modules --exclude out --exclude audio --exclude imagens --exclude qa --exclude logs <anterior>/ <novo>/`). Não copie BRIEF/SCRIPT/ETAPA do anterior.
5. **Escreva `BRIEF.md`** com: tema; título de trabalho (fórmula de `biblia/titulo.md`); duração-alvo e nº de palavras (tabela "Tamanho" de `biblia/roteiro.md`); **link para a bíblia do canal** (`canais/<slug>/biblia/`) e as 3 regras dela que mais importam neste tema; idioma; referência (ID, views, idade, duração, hook real transcrito, estrutura em capítulos, cortes/min); fio condutor e loops candidatos; **teto de custo em US$** (voz + imagens + thumb; base real em `conhecimento/anti-padroes.md`); critérios de pronto e restrições do canal.
6. Atualize `canais/<slug>/backlog.md` (item em produção).

## Passo 7: ÂNGULO (desde 16/11/2026, todo vídeo novo; antes da embalagem) → `$V/ANGULO.md`
**Por quê (Rodrigo, 16/11/2026):** o 005-brasil saiu quase igual ao History in Minutes (`Vug2cLY3nxk`) e ao clone History Easy Guide (`sD0cIJ8JMYw`), porque a bíblia mandava remodelar a transcrição da referência. Diretriz: *"identificar um tema que tem demanda, mas abordá-lo de outro ângulo, para fugir da manada; mas ter um padrão claro de roteiro que funciona em canais de sucesso."* **Forma** (estrutura, hook, ritmo, transições, loops, fecho) = modelada, seção "Forma (modelada)" da bíblia de roteiro do canal. **Conteúdo e ângulo** (tese, recorte, fio condutor, ordem, anedotas) = nossos, seção "Conteúdo (nosso)".
1. **Levante a manada** (custo zero, só via WARP): os 3–5 vídeos de mais views do tema, em todos os idiomas relevantes (o do canal + en; clones pt/es do molde entram sempre, ex.: History Easy Guide, Archivo en Minutos, The Full Record) e o vídeo do canal-modelo sobre o tema, se existir:
   ```bash
   P=tools/.venv/bin/python
   $P tools/manada.py buscar $V/ref --idioma <idioma do canal>,en "<tema>" "<história de X>" "<entire history of X>" --top 6
   $P tools/manada.py transcrever $V/ref --top 5            # + --ids <id do canal-modelo>,<clone> se não vieram no top
   ```
   Grava `$V/ref/manada.json` e `$V/ref/manada-<id>.txt` (legenda; Whisper só se não houver). `ref/` fica fora do git: o `ANGULO.md` resume o que importa.
2. **Mapeie o consenso da manada** (leia as transcrições inteiras): hook de cada um, a sequência de beats, as anedotas e os números que **2+ vídeos repetem**, o fio condutor de cada um. Esse consenso é o que o nosso roteiro **não** pode ser.
3. **Proponha 2–3 ângulos próprios** (tese, recorte ou fio condutor que nenhum vídeo da manada usa), cada um: (a) paga a demanda do tema (quem busca "história do Brasil" fica satisfeito), (b) cabe na **forma** da bíblia do canal (historia-ptbr: pergunta central + eras ligadas; dossie-es: anedota-hook + expedientes; Clearance: lugar fechado + documentos; Em Relevo: pergunta + mapa), (c) tem material de **fontes próprias** (livros, artigos, enciclopédias, arquivos, dados oficiais), não de transcrição. Escolha **1** com justificativa. O ângulo do `youtube.backlog.angulo` (rotina de backlog) é ponto de partida e passa pelo mesmo teste.
4. **Escreva `$V/ANGULO.md`** (modelo abaixo). A skill `embalagem` lê o `ANGULO.md`: a promessa vende o ângulo escolhido; o roteiro o executa e o `tools/similaridade_roteiro.py` confere no fim da etapa 1.

```markdown
# Ângulo <canal>/<NNN-slug> · <data>
## A manada (vídeos transcritos)
| id | canal | views | idioma | hook (1 linha) | fio condutor |
## Consenso da manada (o que NÃO fazer)
- Hook repetido: … · Sequência de beats comum: … · Anedotas/números que 2+ repetem: … (lista; o roteiro pode citar um fato obrigatório do tema, mas não como cena principal nem na mesma ordem)
## Ângulos propostos
1. <tese/recorte/fio> — paga a demanda porque … · cabe na forma porque … · fontes: … · ninguém da manada faz porque …
2. …
## Escolhido: <n> — justificativa
## Anedotas e dados próprios previstos (fora da manada) — meta da bíblia do canal (ex.: ≥ 40%)
| anedota/dado | fonte primária/secundária | aparece em alguma transcrição? (não) |
## Ordem prevista dos capítulos (≠ da manada) e onde o ângulo aparece no hook
```

**Próximo passo obrigatório (desde 14/11/2026):** a skill `embalagem` (título + thumb + crivo) roda **antes** do roteiro, a partir deste BRIEF. Por isso o BRIEF precisa trazer as **fontes** principais e os fatos fortes do tema (a promessa da embalagem tem de ser cumprível com eles). O título de trabalho aqui é provisório: o título real sai do `EMBALAGEM.md` aprovado.

## Critérios de pronto (avaliar)
- A referência tem tração comprovada (views/idade anotados) e é da mesma fórmula.
- O hook real da referência está transcrito no BRIEF (não traduzido para uso; só para modelar).
- Título de trabalho sem as palavras proibidas (morte/morreu/assassinado e equivalentes; `conhecimento/politicas-youtube.md`), e a pauta não depende de foto/vídeo real de cadáver (se depender, descarte ou mude o ângulo).
- Título de trabalho segue a fórmula de `canais/<slug>/biblia/titulo.md`; a referência é do canal-modelo da bíblia.
- Duração-alvo, nº de palavras e **teto de custo** explícitos.
- Fontes principais e 3–6 fatos/casos fortes listados (matéria-prima da promessa da `embalagem`), **de fontes próprias** (livro, artigo, enciclopédia, arquivo, dado oficial), nunca de transcrição de concorrente.
- `ANGULO.md` com a manada transcrita (3–5 vídeos), o consenso mapeado, 2–3 ângulos e o escolhido, com a lista de anedotas próprias que bate a cota da bíblia do canal.
- `youtube.videos` tem a linha (id anotado no topo do BRIEF) e a pasta existe sem `node_modules` copiado.

## Loop de melhoria
1. **Avaliar:** confira cada critério acima; marque o que falhou.
2. **Corrigir:** no máximo 2 rodadas (ex.: trocar a referência por uma com mais tração). O que sobrar vira pendência no BRIEF.
3. **Registrar:** padrão novo de hook/título/estrutura visto na referência vai para a **bíblia do canal que usa esse formato** (`canais/<slug>/biblia/roteiro.md` ou `titulo.md`) com **data e fonte** (ID do vídeo); só vai para `conhecimento/` se valer para qualquer canal. Sem dado próprio de retenção/CTR, marque **Hipótese**.
4. **Commitar:** `git add <arquivos tocados>` (só texto; mídia fica fora do git) e
   `git commit -m "<canal>/<NNN>: BRIEF com referência <ID> e teto US$ X"` (aprendizado em commit próprio: `<canal>/biblia: ...`).
