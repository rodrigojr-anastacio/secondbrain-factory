---
name: produzir-video
description: Use quando o Rodrigo pedir um vídeo novo para um canal da fábrica do YouTube (canal + tema, ou o próximo item do backlog.md). Orquestra as skills pesquisa-referencia, embalagem (título + thumb + crivo, antes do roteiro), roteiro, storyboard, voz, imagens, montagem-render, thumbnail, pacote-youtube e qa em 3 execuções curtas do Claude Code via tools/claude_run.sh, com teto de custo, saldo pré-pago, status em youtube.videos e relatório final.
---

# produzir-video (orquestradora)

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug`. Python: `tools/.venv/bin/python`.
Procedimento completo: `playbooks/produzir-video.md` (seção "Execução econômica" no topo). As etapas estão em `skills/<nome>/SKILL.md`.
O orquestrador (Hermes, Claude Code ou outro) **planeja, dispara e confere**; o trabalho pesado roda no `claude -p` via `tools/claude_run.sh`.

## Antes de agir
0. **Primeiro a bíblia do canal** (caixinha): `canais/<slug>/biblia/README.md` (canal-modelo e "o que NÃO fazer aqui") e **toda** a `canais/<slug>/biblia/` (roteiro, título, thumb, visual, voz). A bíblia **prevalece** sobre `conhecimento/` (só regras gerais). Nunca aplique padrão de outro canal.
1. Leia `MAPA.md`, `AGENTS.md` e as regras gerais de `conhecimento/` (`anti-padroes.md` sobretudo).
2. Leia `canais/<slug>/canal.yaml` e `canais/<slug>/backlog.md`.
   **Calendário e backlog vivo (14/11/2026):** os temas e a ordem vêm da tabela `youtube.backlog` (espelho na seção "Backlog vivo" do `backlog.md`, gerada; `tools/rotinas/backlog.py listar|calendario`). Calendário: 4 vídeos por canal por semana (seg, qua, sex + sáb ou dom alternados; `youtube.calendario_semanas`). A produção normal é **noturna e automática** (`tools/rotinas/noturna.py`, 20:00 na véspera de cada publicação: pega o 1º item agendado, cria vídeo/pasta/briefs e enfileira e1+e2). Vídeo avulso fora disso: registre o tema com `backlog.py add … --status em_producao --data <publicação>` para não colidir com a noite, e lembre que a fila só inicia jobs na janela 20–07 (use `fila.sh add … --agora` se o Rodrigo pedir já).
3. Confira o saldo: `psql -d vida -c "SELECT * FROM financas.saldo_pre_pago"`. Se não cobrir o teto (Fish para voz; OpenAI/fal para imagens), **pare e pergunte ao Rodrigo** (dinheiro é decisão dele).
4. Diga ao Rodrigo, em 1–2 linhas, o plano e o tempo estimado (um vídeo de 17 min leva ~2–4 h: imagens ~25 min, render ~30–60 min).

## Etapa 0: brief (no próprio orquestrador, curta)
Siga a skill `pesquisa-referencia`: referência com `tools/watch.py`, linha em `youtube.videos` (anote o `<id>`), pasta `$V` e `$V/BRIEF.md` com **teto de custo em US$**. Sem `BRIEF.md` com teto, não dispare nada pago.

## Etapa 0b: embalagem + crivo (todo vídeo novo desde 14/11/2026, antes do roteiro)
Ordem nova (decisão do Rodrigo, 14/11/2026): **pesquisa-referencia → embalagem + crivo → roteiro → hook → storyboard → voz → imagens → render.** Siga a skill `embalagem` (`skills/embalagem/SKILL.md`): pesquisa real no YouTube, 2 títulos (T1/T2) + 1 conceito de thumb + a promessa, em `$V/EMBALAGEM.md`; um revisor independente (Task separado, `skills/embalagem/CRIVO.md`) grava `$V/CRIVO.md`.
- **Portão = só o crivo** (o Rodrigo não aprova cada embalagem). Reprovado → reescreve e passa de novo, **máx. 3 rodadas**; ainda reprovado → `$V/BLOQUEIO.md` e o vídeo para.
- Sem `CRIVO.md` aprovado, **não comece o roteiro**; a etapa 1 do lote só grava `ETAPA1-PRONTA.md` com `CRIVO.md` aprovado.
- Não vale para vídeos feitos, agendados ou com etapa 1 já concluída.

## Execuções
**Padrão (lotes, desde 13/11/2026):** cada vídeo entra na fila em 2 etapas: `tools/fila.sh add <nome>-e1 <brief-ETAPA1>` (Opus: pesquisa, **embalagem + crivo**, roteiro, fatos, storyboard; grava `ETAPA1-PRONTA.md` só com `CRIVO.md` aprovado) e `tools/fila.sh add <nome>-e2 <brief-ETAPA2> --depende-de <nome>-e1` (Sonnet: voz, imagens, montagem, render, QA, entrega). Modelo de brief (com a embalagem): `~/workspace/referencias/BRIEF-lote-MODELO-ETAPA1.md` e `BRIEF-lote-MODELO-ETAPA2.md`. O timer dispara, retoma e mede.

**Avulso (um vídeo, fora da fila):** as 3 execuções abaixo, uma por vez, em background, timeout longo.
Para cada etapa, escreva o briefing `$V/.prompt-<etapa>.md` com: objetivo; **"leia primeiro `canais/<slug>/biblia/` (caminho absoluto); ela prevalece sobre `conhecimento/`; não use padrão de outro canal"** e as 3–5 regras da bíblia que mais pesam nesta etapa; "siga `skills/<a>/SKILL.md` e `skills/<b>/SKILL.md`" (caminhos absolutos); id do vídeo; teto restante; critérios de pronto; restrições (um processo de imagem por pasta, um render por vez, não publicar, não ler `~/.segredos/`); e "escreva `ETAPA<n>.md` e commite".

| # | `--etapa` | Modelo | Skills | Sai quando |
|---|---|---|---|---|
| 1 | `roteiro-storyboard` | opus | `embalagem` (+ crivo em Task separado), `roteiro`, `storyboard` | `EMBALAGEM.md` + `CRIVO.md` aprovado (senão `BLOQUEIO.md` e para), `SCRIPT.md`, `blocos.json`, `cenas.json`, `STORYBOARD.md`, `storyboard.json`, `ETAPA1.md` |
| 2 | `producao` | sonnet | `voz`, `imagens`, `thumbnail` (só a base `high`, do conceito aprovado em `EMBALAGEM.md`) | `audio/` e `imagens/` completos, `thumb-var/`, `ETAPA2.md` |
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
- `youtube.videos.status`: `ideia` (etapa 0) → `roteiro` (1) → `producao` (2) → `qa` (3) → `pronto` (QA aprovado). Atualize sempre com `atualizado_em=now()`. No historia-ptbr, `biblia_versao` marca a bíblia de roteiro do vídeo (`'v1'` = 001–005, `'v2'` = 006+; gravada na etapa 0/roteiro) para o comparativo do `canais/historia-ptbr/biblia/README.md`. `publicado` só depois que o Rodrigo publicar (aí grave `youtube_id`, `publicado_em`, título no ar e atualize `backlog.md`).

## Relatório final (ao Rodrigo, curto)
- Título, duração e caminhos de `out/`; T1/T2 e a promessa do `EMBALAGEM.md` (rodada em que o crivo aprovou) e onde o vídeo a paga. O vídeo vai para o Drive (`tools/entregar_drive.sh`); pelo chat, só a thumb e o contact sheet.
- Custo: `SELECT * FROM financas.custo_por_video WHERE id=<id>` (BRL) + soma em US$ do `financas.consumo` + Claude equivalente; comparação com o teto.
- Resultado do QA (números), pendências e o checklist de publicação de `pacote-youtube` (sintético = sim, não é para crianças, 3 thumbs no "Testar e comparar").

## Loop de melhoria
1. **Avaliar:** cada etapa passou nos critérios da própria skill? Quantas rodadas o crivo da embalagem pediu? O QA confirmou a promessa paga (timestamp) e a thumb no conceito? O QA confirmou que o vídeo **segue a bíblia do canal**? Custo ≤ teto? Quantas rodadas de correção? Tempo por etapa (`youtube.execucoes_claude.duracao_s`, turnos).
2. **Corrigir:** até 2 rodadas por etapa; o resto vira pendência no relatório e no `QA.md`.
3. **Registrar:** aprendizado de formato/estilo na **bíblia do canal** (`canais/<slug>/biblia/`); custos reais do vídeo e erros de ferramenta/processo em `conhecimento/anti-padroes.md`; ajustes de procedimento em `playbooks/produzir-video.md` e nas skills; tudo com **data e fonte**; sem dado = **Hipótese** (o Métricas confirma depois de 3–7 dias com `playbooks/revisar-metricas.md`).
4. **Commitar:** `git status` (sem mídia nem segredo) → `git add` dos textos → `git commit -m "<canal>/<NNN>: pronto para publicar (MM:SS, US$ X)"`.
