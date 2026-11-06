# Rotinas da fábrica (systemd user, sem depender do Hermes)

| Rotina | Timer | Script | O que faz |
|---|---|---|---|
| diária | `fabrica-diaria.timer` (todo dia 06:30) | `diaria.sh` | coleta de métricas (`report.py --coletar`), backup do banco e `git-diario.sh` (commit + push dos cérebros). Sem IA |
| métricas | `fabrica-metricas.timer` (seg 08:15) | `metricas.sh` | relatório semanal por canal, custos, 3 ajustes por canal, Hipóteses confirmadas/derrubadas |
| tendências | `fabrica-tendencias.timer` (seg e qui 09:30) | `tendencias.sh` | garimpo (`playbooks/garimpo-tendencias.md`): trends.py, watch.py, 3 fórmulas, INVESTIR/TESTAR/DESCARTAR |
| palavras-chave | `fabrica-palavras-chave.timer` (qua 09:30) | `palavras-chave.sh` | `playbooks/palavras-chave.md`: keywords.py (autocomplete via WARP + 20 termos validados, ≤ 2.500 un. de cota) → top 5 temas por canal, padrões de título, até 3 ideias de canal novo. Só sugere |

## Como funcionam `metricas.sh`, `tendencias.sh` e `palavras-chave.sh`
- Os três chamam `_rotina_claude.sh <rotina>`, que monta o prompt de `prompts/<rotina>.md` (troca `{{DATA}}`, `{{MODO}}`, `{{RELATORIO}}`, `{{RESUMO}}`) e roda `tools/claude_run.sh --etapa <rotina>` (sem `--video`, modelo sonnet, trava anti-duplicação e registro em `youtube.execucoes_claude`; `--permission-mode bypassPermissions`).
- Saídas em `~/workspace/relatorios/<rotina>/`: `<data>.md` (relatório completo), `<data>-resumo.txt` (resumo executivo de 5–10 linhas) e `logs/`. O Claude também copia o relatório para `pesquisa/<rotina>/` e commita os aprendizados (na bíblia do canal, `canais/<slug>/biblia/`, ou em `conhecimento/` se forem gerais) (o push vem do `git-diario.sh`).
- **Entrega no Telegram:** `hermes send --to telegram` manda o resumo + o relatório anexado (`MEDIA:`) para o home channel do bot do default. Esse comando usa o token do `~/.hermes/.env` direto, **sem LLM e sem o gateway rodando**. Se o envio falhar, fica só o arquivo em `relatorios/`.
- Opções: `--teste` (tendências: não roda `trends.py`, reaproveita o último garimpo, no máximo 2 vídeos e 1 busca; palavras-chave: `keywords.py --teste`, sem a–z, 3 termos, ≤ 303 un., não grava no banco; arquivos com sufixo `-teste`) e `--sem-telegram`. `TIMEOUT=<s>` muda o limite (padrão 5400 s).
- Rodar na mão: `tools/rotinas/metricas.sh` ou `systemctl --user start fabrica-metricas.service`. Ver: `systemctl --user list-timers | grep fabrica`, `journalctl --user -u fabrica-metricas`.

## Instalação dos timers
Os unit files ficam em `systemd/` (versionados) e são symlinks em `~/.config/systemd/user/`:
```bash
cd ~/workspace/fabrica-youtube/tools/rotinas/systemd
for f in fabrica-*; do ln -sf "$PWD/$f" ~/.config/systemd/user/$f; done
systemctl --user daemon-reload
systemctl --user enable --now fabrica-metricas.timer fabrica-tendencias.timer fabrica-palavras-chave.timer
```

## Testes (04/11/2026)
- `metricas.sh` (completo, via `systemctl --user start`): 68 s, 7 turnos, US$ 0,26 equivalente (`execucoes_claude` id 3), relatório + resumo em `relatorios/metricas/`, commit `88f4a0a`, Telegram ok.
- `tendencias.sh --teste`: 109 s, 17 turnos, US$ 0,40 equivalente (id 4), 2 vídeos assistidos, 0 unidades de cota, commit `d062ccb`, Telegram ok com thumb e hook_sheet anexados. A 1ª execução completa (~4 mil unidades) é a do timer de qui 05/11 09:30.

- `palavras-chave.sh --sem-telegram` (completo, 06/11/2026, unidade transitória `systemd-run --user`): keywords.py 575 s, 837 chamadas de autocomplete sem falha, 20 termos validados, **2.020 unidades** de cota, 10.361 linhas em `youtube.palavras_chave`; relatório em `relatorios/palavras-chave/2026-11-06.md`, commit `31d0d47`. 1ª execução do timer: qua 11/11 09:30.

## Crons do Hermes (perfil default)
- `garimpo-semanal-yt` (seg/qui 09:00): **mantido** até o Rodrigo aprovar a rotina nova; depois pode ser pausado (`hermes cron pause <id>`). Desde 04/11/2026 o provedor do Hermes está em HTTP 429 até ~27/11, então ele não roda de fato.
- `metricas-semanal-yt` (seg 08:00): **pausado** em 04/11/2026, porque duplica `fabrica-metricas.timer` (não apagado; `hermes cron resume <id>` volta).

## Produtor de vídeo (sob demanda, sem cron)
- **Hermes desktop:** abra o perfil `produtor` ou peça ao default ("produza o vídeo X do canal Y"), que delega ao `produtor`.
- **Claude Code interativo:** `cd ~/workspace/fabrica-youtube && claude` e peça para usar o subagente `produtor` (fonte em `agentes-claude/produtor.md`) ou a skill `produzir-video`.
- **Headless (uma etapa por vez):** `tools/claude_run.sh --video <id> --etapa <roteiro|producao|montagem-render|qa|...> --cwd canais/<slug>/videos/NNN-slug --prompt-file BRIEF-ETAPA.md`. Detalhes em `playbooks/produzir-video.md`.
