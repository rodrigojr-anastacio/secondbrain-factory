# Fábrica de conteúdo do YouTube

Esteira de produção de vídeos para vários canais do Rodrigo, hoje 2 e no plano 10–15. Este arquivo é o manual para **qualquer agente** que opere a fábrica (Hermes, Claude Code ou outro no futuro): tudo o que é necessário para operar está aqui, nos playbooks e em `conhecimento/`, não na memória de um agente específico.

A pasta é o repositório git **cerebro-fabrica**: todos os agentes leem e escrevem nela. Comece pelo `MAPA.md` (o que existe e onde, o que fica fora do git e a regra de commit).

## Estrutura
```
fabrica-youtube/
├── AGENTS.md            ← este manual
├── MAPA.md              ← mapa do repo: onde está cada coisa, quem lê/escreve, o que fica fora do git
├── conhecimento/        ← base viva do que aprendemos (com data e fonte)
│   ├── hooks.md, titulos.md, roteiros.md, anti-padroes.md (inclui custos por vídeo)
│   └── thumbnails/      ← thumbs no ar (<canal>-<video>.jpg, < 500 KB) + README com o CTR
├── skills/README.md     ← mapa das skills do Produtor de vídeo (Fase 2, ainda não implementadas)
├── playbooks/           ← procedimentos (siga-os; melhore-os)
│   ├── produzir-video.md
│   ├── garimpo-tendencias.md
│   └── revisar-metricas.md
├── tools/               ← comandos determinísticos (Python em tools/.venv)
│   ├── report.py  métricas e retenção (YouTube Data + Analytics API; sem CTR, que só existe no Studio)
│   ├── trends.py  garimpo de canais novos com tração
│   ├── watch.py   "assiste" vídeos: hook transcrito, frames, ritmo, anúncios (via WARP)
│   ├── transcrever.py transcrição Whisper de um vídeo do YouTube (via WARP)
│   ├── tts_fish.py narração Fish Audio com a voz do canal; registra o custo em financas.consumo
│   ├── img_openai.py / img_fal.py imagens no estilo do canal; registram o custo em financas.consumo; trava por pasta (.img.lock)
│   ├── claude_run.py / .sh uma etapa do Claude Code por vídeo (claude -p): modelo por etapa, trava, custo em youtube.execucoes_claude
│   ├── db.py, _paths.py, _trava.py, db/ (schemas e seed), rotinas/diaria.sh (coleta + backup)
│   └── auth.py    login OAuth de um canal (feito pelo Rodrigo)
├── canais/<slug>/
│   ├── canal.yaml       ← identidade e configuração do canal (idioma, voz, fórmula, token…)
│   ├── estilo.md        ← padrão visual e editorial do canal
│   ├── backlog.md       ← fila de ideias com status
│   └── videos/NNN-slug/ ← um projeto por vídeo (brief, roteiro, fontes, código Remotion, out/, QA)
└── pesquisa/
    ├── trend_seeds.txt, trends_state.json
    └── tendencias/      ← relatórios do garimpo e assets/ dos vídeos assistidos
```
Python: `~/workspace/fabrica-youtube/tools/.venv/bin/python`. Rode os scripts a partir de `tools/`.

## Recursos fora da fábrica
- **Segredos:** `~/.segredos/` (permissão 600). Tokens do YouTube em `~/.segredos/youtube/tokens/<canal>.json`. Nunca imprima, copie ou commite.
- **Voz Kokoro (local, grátis):** `~/tts/venv-kokoro/bin/python`; exemplo em `~/tts/gen_kokoro.py`.
- **Proxy WARP:** `socks5://127.0.0.1:40000`, para tudo que acessa o YouTube como usuário (assistir, baixar, abrir a página). O YouTube bloqueia o IP da VPS.
- **Navegador:** Chromium do Hermes (bibliotecas do sistema instaladas). Para o YouTube, use o proxy WARP.
- **CPU:** a VPS tem 2 vCPU. Um render de ~8 min leva ~15–30 min, então **um render por vez**.

## Regras da fábrica
1. **Cada canal tem identidade própria** (`canal.yaml` + `estilo.md`). Nunca misture o estilo de um canal no outro.
2. **Todo vídeo novo** é uma pasta em `canais/<slug>/videos/NNN-slug/` e segue `playbooks/produzir-video.md`.
3. **Leia `conhecimento/` antes de produzir** (hooks, títulos, roteiros, anti-padrões e thumbnails). **Registre lá o que aprender** (hook que funcionou, erro de render, padrão de thumb, métrica que explica um resultado), sempre **com data e fonte**, e marque como **Hipótese** o que não tiver dado. O que for específico de um canal vai também no `estilo.md` dele, e o que mudar um procedimento vai no playbook. Depois, **faça um commit descritivo** (git como memória). A fábrica deve sobreviver a uma troca de agente.
4. **Decisões do Rodrigo** (publicar, gastar dinheiro, criar ou entrar em contas) são dele. Prepare tudo e peça.
5. Cota da API do YouTube: 10 mil unidades por dia para todos os canais; `search.list` custa 100.

## Banco de dados (Postgres `vida`, esquema `youtube`)
Acesso local sem senha, como o usuário do sistema: `psql -d vida`, ou `tools/db.py` em Python. O esquema está em `tools/db/schema_youtube.sql` (idempotente).
| Tabela | O que guarda | Quem grava |
|---|---|---|
| `canais` | nossos canais (slug = pasta em `canais/`) | manual / agente |
| `videos` | esteira: cada vídeo nosso e o status (ideia → roteiro → producao → qa → pronto → publicado) | **o agente: atualize ao avançar uma etapa e, ao publicar ou republicar, grave `youtube_id`, `publicado_em` e o título no ar** |
| `metricas_canal`, `metricas_video` | snapshot diário dos nossos canais e vídeos | `report.py --coletar` (rotina diária) |
| `garimpo_execucoes`, `garimpo_canais`, `garimpo_snapshots`, `garimpo_videos` | garimpo de tendências e histórico de crescimento | `trends.py` |
| `assistidos` | vídeos analisados (hook, cortes por minuto, anúncios, assets) | `watch.py` |
| view `garimpo_crescimento` | crescimento de views de cada canal garimpado entre execuções | — |
| `execucoes_claude` | cada chamada do Claude Code: vídeo, etapa, modelo, sessão, duração, turnos, tokens, `custo_usd_equivalente`, erro e resumo do resultado (DDL em `tools/db/schema_execucoes_claude.sql`) | `tools/claude_run.py` |
| view `custo_claude_por_video` | soma por vídeo e etapa (ignora `etapa = 'teste'` e as rotinas sem vídeo) | — |
- Na análise do garimpo, grave a fórmula e a decisão em `garimpo_canais.formula` e `garimpo_canais.decisao` (investir | testar | descartar).
- Arquivos continuam sendo a saída de mídia e texto longo. O banco é a fonte para consultas, histórico e números.
- Rotinas (systemd user, independentes do Hermes; guia em `tools/rotinas/README.md`): `diaria.sh` (06:30, coleta + backup em `~/backups/vida`, 14 dias), `metricas.sh` (seg 08:15) e `tendencias.sh` (seg/qui 09:30). As duas últimas rodam `claude -p` via `claude_run.py` (etapas `metricas`/`tendencias`, sem vídeo), gravam em `~/workspace/relatorios/<rotina>/` e mandam o resumo no Telegram.
- Subagentes do Claude Code: `agentes-claude/` (`produtor`, `tendencias`, `metricas`); entrada em `CLAUDE.md`.

## Custos
- Toda geração paga (TTS, imagens etc.) deve registrar o custo em `financas.consumo`, com `ref_id` = `youtube.videos.id` do vídeo. O `tts_fish.py --video <id>` já faz isso.
- Antes de produzir um vídeo, crie a linha dele em `youtube.videos` para ter o id. Consulte o custo em `financas.custo_por_video`.
- Saldo de crédito pré-pago (Fish, OpenAI, fal.ai): `SELECT * FROM financas.saldo_pre_pago`. O da OpenAI só é confiável se todas as recargas estiverem lançadas em `financas.lancamentos`; em 04/11/2026 estava negativo por falta de lançamento.
- Os custos reais por vídeo e os erros que custaram dinheiro estão em `conhecimento/anti-padroes.md`.
- Claude Code: rode cada etapa via `tools/claude_run.py --video <id> --etapa <etapa>` (opus em roteiro/storyboard, sonnet no resto). O uso fica em `youtube.execucoes_claude` / `youtube.custo_claude_por_video` (preço de lista equivalente; o Claude Max real entra no rateio fixo).
