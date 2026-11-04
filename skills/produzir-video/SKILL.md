---
name: produzir-video
description: Use quando o Rodrigo pedir um vídeo novo para um canal da fábrica do YouTube (canal + tema, ou o próximo item do backlog.md). Orquestra as skills pesquisa-referencia, roteiro, storyboard, voz, imagens, montagem-render, thumbnail, pacote-youtube e qa em 3 execuções curtas do Claude Code via tools/claude_run.sh, com teto de custo, saldo pré-pago, status em youtube.videos e relatório final.
---

# produzir-video (orquestradora)

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug`. Python: `tools/.venv/bin/python`.
Procedimento completo: `playbooks/produzir-video.md` (seção "Execução econômica" no topo). As etapas estão em `skills/<nome>/SKILL.md`.
O orquestrador (Hermes, Claude Code ou outro) **planeja, dispara e confere**; o trabalho pesado roda no `claude -p` via `tools/claude_run.sh`.

## Antes de agir
1. Leia `MAPA.md`, `AGENTS.md` e **todo** `conhecimento/` (`hooks.md`, `titulos.md`, `roteiros.md`, `anti-padroes.md`, `thumbnails/README.md`).
2. Leia `canais/<slug>/canal.yaml`, `canais/<slug>/estilo.md` e `canais/<slug>/backlog.md`.
3. Confira o saldo: `psql -d vida -c "SELECT * FROM financas.saldo_pre_pago"`. Se não cobrir o teto (Fish para voz; OpenAI/fal para imagens), **pare e pergunte ao Rodrigo** (dinheiro é decisão dele).
4. Diga ao Rodrigo, em 1–2 linhas, o plano e o tempo estimado (um vídeo de 17 min leva ~2–4 h: imagens ~25 min, render ~30–60 min).

## Etapa 0: brief (no próprio orquestrador, curta)
Siga a skill `pesquisa-referencia`: referência com `tools/watch.py`, linha em `youtube.videos` (anote o `<id>`), pasta `$V` e `$V/BRIEF.md` com **teto de custo em US$**. Sem `BRIEF.md` com teto, não dispare nada pago.

## As 3 execuções (uma por vez, em background, timeout longo)
Para cada etapa, escreva o briefing `$V/.prompt-<etapa>.md` com: objetivo; "siga `skills/<a>/SKILL.md` e `skills/<b>/SKILL.md`" (caminhos absolutos); id do vídeo; teto restante; critérios de pronto; restrições (um processo de imagem por pasta, um render por vez, não publicar, não ler `~/.segredos/`); e "escreva `ETAPA<n>.md` e commite".

| # | `--etapa` | Modelo | Skills | Sai quando |
|---|---|---|---|---|
| 1 | `roteiro-storyboard` | opus | `roteiro`, `storyboard` | `SCRIPT.md`, `blocos.json`, `cenas.json`, `STORYBOARD.md`, `storyboard.json`, `ETAPA1.md` |
| 2 | `producao` | sonnet | `voz`, `imagens`, `thumbnail` (só a base `high`) | `audio/` e `imagens/` completos, `thumb-var/`, `ETAPA2.md` |
| 3 | `montagem-render` | sonnet | `montagem-render`, `thumbnail` (final), `pacote-youtube`, `qa` | `out/video.mp4`, `out/thumbnail.jpg`, `out/legendas.srt`, `out/youtube.txt`, `QA.md`, `ETAPA3.md` |

```bash
cd ~/workspace/fabrica-youtube; mkdir -p $V/logs
tools/claude_run.sh --video <id> --etapa roteiro-storyboard --cwd $V --prompt-file $V/.prompt-roteiro-storyboard.md --dry-run
nohup tools/claude_run.sh --video <id> --etapa roteiro-storyboard --cwd $V \
  --prompt-file $V/.prompt-roteiro-storyboard.md --timeout 5400 > $V/logs/claude-roteiro-storyboard.out 2>&1 &
```
- O modelo sai da etapa (opus/sonnet); só use `--modelo` com motivo. Código 3 = trava ocupada (já está rodando): **não** dispare outra.
- Entre etapas, confira só o relatório (`ETAPA<n>.md` + fim de `logs/claude-<etapa>.out`) e os critérios da skill; nada de revisar arquivo por arquivo.
- Etapa falhou ou ficou incompleta: corrija o briefing e rode **a mesma etapa** de novo (máx. 2 rodadas). Não junte etapas.

## Tetos e status
- Antes das etapas 2 e 3, some o gasto: `psql -d vida -c "SELECT fornecedor, sum(custo) FROM financas.consumo WHERE ref_tipo='youtube.video' AND ref_id=<id> GROUP BY 1"`. Se a previsão passar do teto do BRIEF, **pare e pergunte**.
- Claude Code (preço de lista, não cobrança no Max): `SELECT * FROM youtube.custo_claude_por_video WHERE video_id=<id>;`.
- `youtube.videos.status`: `ideia` (etapa 0) → `roteiro` (1) → `producao` (2) → `qa` (3) → `pronto` (QA aprovado). Atualize sempre com `atualizado_em=now()`. `publicado` só depois que o Rodrigo publicar (aí grave `youtube_id`, `publicado_em`, título no ar e atualize `backlog.md`).

## Relatório final (ao Rodrigo, curto)
- Título, duração, caminhos de `out/` (no Telegram, anexe com `MEDIA:/caminho` a thumb e o contact sheet; o mp4 1080p fica na VPS).
- Custo: `SELECT * FROM financas.custo_por_video WHERE id=<id>` (BRL) + soma em US$ do `financas.consumo` + Claude equivalente; comparação com o teto.
- Resultado do QA (números), pendências e o checklist de publicação de `pacote-youtube` (sintético = sim, não é para crianças, 3 thumbs no "Testar e comparar").

## Loop de melhoria
1. **Avaliar:** cada etapa passou nos critérios da própria skill? Custo ≤ teto? Quantas rodadas de correção? Tempo por etapa (`youtube.execucoes_claude.duracao_s`, turnos).
2. **Corrigir:** até 2 rodadas por etapa; o resto vira pendência no relatório e no `QA.md`.
3. **Registrar:** custos reais do vídeo em `conhecimento/anti-padroes.md` (seção de custos), erros novos lá também, ajustes de procedimento em `playbooks/produzir-video.md` e nas skills; tudo com **data e fonte**; sem dado = **Hipótese** (o Métricas confirma depois de 3–7 dias com `playbooks/revisar-metricas.md`).
4. **Commitar:** `git status` (sem mídia nem segredo) → `git add` dos textos → `git commit -m "<canal>/<NNN>: pronto para publicar (MM:SS, US$ X)"`.
