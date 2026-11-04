# Fábrica do YouTube (cerebro-fabrica) para o Claude Code

Responda em português do Brasil. Comece pelo `MAPA.md` (o que existe, onde, quem escreve, regra de commit); o manual completo é o `AGENTS.md`, importado abaixo.

@AGENTS.md

## Subagentes (fonte em `agentes-claude/`; ativos quando ligados em `.claude/agents/`, ex.: `ln -s ../agentes-claude .claude/agents`)
- `produtor`: produz um vídeo do backlog/tema até o pacote em `out/` (usa as skills abaixo e `tools/claude_run.sh`).
- `tendencias`: garimpo de canais novos com tração e padrões (`playbooks/garimpo-tendencias.md`).
- `metricas`: relatório semanal por canal, custos e ajustes (`playbooks/revisar-metricas.md`).
São os mesmos papéis dos perfis Hermes (`~/.hermes/profiles/<p>/SOUL.md`).

## Skills (`skills/<nome>/SKILL.md`, symlink em `~/.claude/skills/` e `~/.hermes/skills/`)
`produzir-video` (orquestradora), `pesquisa-referencia`, `roteiro`, `storyboard`, `voz`, `imagens`, `montagem-render`, `thumbnail`, `pacote-youtube`, `qa`. Mapa e critérios em `skills/README.md`.

## Rotinas (systemd user, sem depender do Hermes)
`tools/rotinas/`: `diaria.sh` (06:30), `metricas.sh` (seg 08:15) e `tendencias.sh` (seg/qui 09:30). Veja `tools/rotinas/README.md`.

## Regras que não podem falhar
- **Segredos** em `~/.segredos/`: nunca imprima, copie, mova nem commite. Rode `git status` antes de commitar.
- **`~/workspace/cerebro-rodrigo` não é deste repo** e não é dos especialistas: não leia nem escreva lá.
- **Custo:** toda geração paga com `--video <id>` e dentro do teto do `BRIEF.md`; confira `financas.saldo_pre_pago`. Claude Code headless sempre via `tools/claude_run.sh` (trava + registro em `youtube.execucoes_claude`). Gastar dinheiro, contas e publicar são decisões do Rodrigo.
- Todo aprendizado vai para `conhecimento/` com data e fonte (ou como **Hipótese**) e vira commit descritivo.
