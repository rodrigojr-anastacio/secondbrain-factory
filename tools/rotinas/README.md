# Rotinas da fábrica (systemd user, sem depender do Hermes)

| Rotina | Timer | Script | O que faz |
|---|---|---|---|
| diária | `fabrica-diaria.timer` (todo dia 06:30) | `diaria.sh` | coleta de métricas (`report.py --coletar`), backup do banco e `git-diario.sh` (commit + push dos cérebros). Sem IA |
| métricas | `fabrica-metricas.timer` (seg 08:15) | `metricas.sh` | relatório semanal por canal, custos, 3 ajustes por canal, Hipóteses confirmadas/derrubadas |
| tendências | `fabrica-tendencias.timer` (seg e qui 09:30) | `tendencias.sh` | garimpo (`playbooks/garimpo-tendencias.md`): trends.py, watch.py, 3 fórmulas, INVESTIR/TESTAR/DESCARTAR; depois o garimpo em lote (`tools/garimpo_batch.py`, Batch API) |
| palavras-chave | `fabrica-palavras-chave.timer` (qua 09:30) | `palavras-chave.sh` | `playbooks/palavras-chave.md`: keywords.py (autocomplete via WARP + 20 termos validados, ≤ 2.500 un. de cota) → top 5 temas por canal, padrões de título, até 3 ideias de canal novo. Só sugere |
| analytics completo | `fabrica-analytics.timer` (dias 1,4,7… do mês, 07:10; pedido do Rodrigo: a cada 3 dias) | `../analytics_completo.py` | tudo da Analytics API por canal/vídeo desde o 1º vídeo (dia, retenção, origem e detalhe de tráfego, público, receita se houver) + baixa a Reporting API (impressões/CTR) → `youtube.analytics_*`/`alcance_diario`; relatório em `~/workspace/relatorios/metricas/`. Sem IA, sem Telegram. Na mão: `systemctl --user start fabrica-analytics.service` |

## Motor: Claude pela API (desde 12/11/2026), fora da cota do Max
- O Rodrigo recebe **US$ 100/mês de créditos da API Anthropic** junto com o Max (valem para API, Agent SDK, Managed Agents e Playground; **não** para sessões do Claude Code). As rotinas automáticas usam esses créditos: `_rotina_claude.sh` chama **`rotina_api.py`** (Agent SDK em Python: mesmas ferramentas do Claude Code, mesmo prompt, mesmo cwd, `bypassPermissions`, CLAUDE.md do projeto carregado) com a chave `~/.segredos/anthropic/rotinas.env`, passada só ao processo filho. O script confere no `init` que a autenticação é a chave (`apiKeySource=ANTHROPIC_API_KEY`) e aborta se não for.
- **Modelo e orçamento por execução:** tendências sonnet (US$ 4), palavras-chave sonnet (US$ 3), métricas sonnet (US$ 1,5); `MODELO=` e `ORCAMENTO=` sobrescrevem. Teto mensal do grupo rotinas+garimpo: **US$ 65** (`tools/anthropic_api.py`; a rotina não começa se o gasto do mês + orçamento passar).
- **Falha da API** (rede, 401/429/5xx, orçamento, teto): a rotina grava o erro no resumo, manda no Telegram e **não chama `claude -p` sozinha**. Na mão, para comparar ou com a API fora: `MOTOR=claude-code tools/rotinas/<rotina>.sh` (cota do Max, via `claude_run.sh`).
- **Custo real** em `financas.consumo` (fornecedor `Anthropic API`, servico `rotina:<rotina>`) e uma linha em `youtube.execucoes_claude` (modelo `api:<modelo>`). Saldo do mês: `select * from financas.saldo_pre_pago where fornecedor='Anthropic API'` (o crédito de US$ 100 é lançado todo mês em `financas.lancamentos`, `valor_brl` 0).
- **Estimativa (12/11/2026, Sonnet 5.5 a US$ 2/10 por MTok):** métricas ~US$ 0,20–0,40, tendências ~US$ 0,15 (teste) a ~0,60 (completo), palavras-chave ~US$ 0,50 por execução → **~US$ 8–12/mês** nas rotinas; garimpo em lote ~US$ 0,5–1,1 por rodada → ~US$ 5–10/mês. Total ~US$ 15–20 de US$ 65.
- **Garimpo em lote (Batch API, 50% mais barata):** no modo completo, `tendencias.sh` roda `tools/garimpo_batch.py` depois do agente: analisa até 300 vídeos ainda não analisados de `youtube.garimpo_videos` (canais não descartados, sem Shorts; título, números, thumb, hook transcrito e frames do watch.py quando houver) com Sonnet em lote, espera até 40 min (`BATCH_ESPERA`; se não terminar, fica em `pesquisa/tendencias/batch/pendente.json` e a próxima rodada coleta), grava `pesquisa/tendencias/batch/<data>-<lote>.jsonl`, a síntese `pesquisa/tendencias/<data>-batch.md` e uma seção datada em `conhecimento/padroes-garimpo.md`, commita esses arquivos e põe uma linha no resumo do Telegram. 1ª rodada (12/11/2026): 164 vídeos, US$ 0,75 o lote + US$ 0,36 a síntese. `BATCH=1` liga também no `--teste`.

## Como funcionam `metricas.sh`, `tendencias.sh` e `palavras-chave.sh`
- Os três chamam `_rotina_claude.sh <rotina>`, que monta o prompt de `prompts/<rotina>.md` (troca `{{DATA}}`, `{{MODO}}`, `{{RELATORIO}}`, `{{RESUMO}}`) e roda `rotina_api.py --rotina <rotina>` (seção acima; trava anti-duplicação compartilhada com o `claude_run`, registro em `youtube.execucoes_claude` e `financas.consumo`). Até 11/11/2026 rodavam `tools/claude_run.sh --etapa <rotina>` (claude -p, cota do Max).
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
systemctl --user enable --now fabrica-analytics.timer fabrica-metricas.timer fabrica-tendencias.timer fabrica-palavras-chave.timer
```

## Testes pela API (12/11/2026)
- `metricas.sh --teste --sem-telegram` (unidade transitória `systemd-run --user`): 65 s, 12 turnos, **US$ 0,19** reais (`execucoes_claude` id 16), relatório e resumo em `relatorios/metricas/2026-11-12-teste*`, nada commitado.
- `tendencias.sh --teste --sem-telegram`: 27 s, **US$ 0,14** (reaproveitou o completo do dia), resumo com `MEDIA:` ok.
- `garimpo_batch.py`: lote de 166 vídeos terminou em < 9 min; 164 ok, 2 erros (thumb sem download: na próxima rodada vão sem a URL).

## Testes (04/11/2026, ainda com claude -p)
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
