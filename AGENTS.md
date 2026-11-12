# Fábrica de conteúdo do YouTube

Esteira de produção de vídeos para vários canais do Rodrigo, hoje 2 e no plano 10–15. Este arquivo é o manual para **qualquer agente** que opere a fábrica (Hermes, Claude Code ou outro no futuro): tudo o que é necessário para operar está aqui, nos playbooks e em `conhecimento/`, não na memória de um agente específico.

A pasta é o repositório git **cerebro-fabrica**: todos os agentes leem e escrevem nela. Comece pelo `MAPA.md` (o que existe e onde, o que fica fora do git e a regra de commit).

## Estrutura
```
fabrica-youtube/
├── AGENTS.md            ← este manual
├── MAPA.md              ← mapa do repo: onde está cada coisa, quem lê/escreve, o que fica fora do git
├── conhecimento/        ← só REGRAS GERAIS (valem para qualquer canal), com data e fonte
│   ├── hooks.md, titulos.md, roteiros.md, anti-padroes.md (ferramentas, processo, custos por vídeo)
│   └── thumbnails/      ← galeria das thumbs no ar (<canal>-<video>.jpg, < 500 KB) + regras gerais
├── skills/<nome>/SKILL.md ← 10 skills do Produtor + novo-canal (Agent Skills; symlink em ~/.claude/skills e ~/.hermes/skills/fabrica-youtube) + README.md (mapa)
├── playbooks/           ← procedimentos (siga-os; melhore-os)
│   ├── produzir-video.md
│   ├── garimpo-tendencias.md
│   ├── palavras-chave.md (qua: termos em alta → sugestões)
│   ├── revisar-metricas.md
│   └── novo-canal.md    ← avaliar nicho e montar canal novo (skill novo-canal)
├── tools/               ← comandos determinísticos (Python em tools/.venv)
│   ├── report.py  métricas e retenção (YouTube Data + Analytics API). Impressões/CTR vêm pela Reporting API (`reporting.py`, 1–2 dias de atraso; tempo real só no Studio)
│   ├── analytics_completo.py  tudo da Analytics API por vídeo/dia (retenção, tráfego e detalhe, público) → `youtube.analytics_*`; relatório em `~/workspace/relatorios/metricas/`; timer a cada 3 dias
│   ├── trends.py  garimpo de canais novos com tração
│   ├── keywords.py palavras-chave em alta (autocomplete via WARP + validação ≤ 2.500 un.) → youtube.palavras_chave
│   ├── watch.py   "assiste" vídeos: hook transcrito, frames, ritmo, anúncios (via WARP)
│   ├── transcrever.py transcrição Whisper de um vídeo do YouTube (via WARP)
│   ├── tts_fish.py narração Fish Audio com a voz do canal; registra o custo em financas.consumo
│   ├── img_openai.py / img_fal.py imagens no estilo do canal; registram o custo em financas.consumo; trava por pasta (.img.lock)
│   ├── claude_run.py / .sh uma etapa do Claude Code por vídeo (claude -p): modelo por etapa, trava, custo em youtube.execucoes_claude
│   ├── db.py, _paths.py, _trava.py, db/ (schemas e seed), rotinas/diaria.sh (coleta + backup)
│   └── auth.py    login OAuth de um canal (feito pelo Rodrigo)
├── canais/<slug>/
│   ├── canal.yaml       ← configuração técnica do canal (idioma, voz, gerador, estilo_prompt, token…)
│   ├── biblia/          ← A CAIXINHA DO CANAL: README (canal-modelo + o que NÃO fazer aqui), roteiro.md,
│   │                      titulo.md, thumb.md, visual.md, voz.md. Prevalece sobre conhecimento/
│   ├── estilo.md        ← só índice para biblia/
│   ├── backlog.md       ← fila de ideias com status
│   └── videos/NNN-slug/ ← um projeto por vídeo (brief, roteiro, fontes, código Remotion, out/, QA)
└── pesquisa/
    ├── trend_seeds.txt, trends_state.json, keyword_seeds.yaml
    ├── palavras-chave/  ← relatórios da rotina de palavras-chave
    └── tendencias/      ← relatórios do garimpo e assets/ dos vídeos assistidos
```
Python: `~/workspace/fabrica-youtube/tools/.venv/bin/python`. Rode os scripts a partir de `tools/`.

## Recursos fora da fábrica
- **Segredos:** `~/.segredos/` (permissão 600). Tokens do YouTube em `~/.segredos/youtube/tokens/<canal>.json`. Nunca imprima, copie ou commite.
- **Voz Kokoro (local, grátis):** `~/tts/venv-kokoro/bin/python`; exemplo em `~/tts/gen_kokoro.py`.
- **Proxy WARP:** `socks5://127.0.0.1:40000`, para tudo que acessa o YouTube como usuário (assistir, baixar, abrir a página). O YouTube bloqueia o IP da VPS.
- **Navegador:** Chromium do Hermes (bibliotecas do sistema instaladas). Para o YouTube, use o proxy WARP.
- **Render: todo render de vídeo vai para uma GPU alugada no Runpod** (`tools/render_runpod.sh`; decisão do Rodrigo, 11/11/2026): vídeo inteiro, partes, refações e clipes. Vídeo de 12 min com 3D: ~5–10 min de render, ~US$ 0,05–0,20, contra ~10 h na VPS. O script confere quadros contra stills da VPS antes e depois, destrói o Pod sempre e grava o custo em `financas.consumo` (`VIDEO=<id>`). Chave em `~/.segredos/runpod/api_key`; imagem do Pod em `tools/render-gpu-image/` (ghcr). Procedimento na skill `montagem-render`.
- **CPU da VPS:** 2 vCPU. Na VPS ficam só stills, thumbs, grades do pré-QA e testes de segundos. Ela é **fallback** do render se não houver GPU após ~30 min ou se a conferência reprovar 2× (aí um render por vez; ~15–30 min por 8 min de vídeo, horas com 3D).

## Regras da fábrica
1. **Cada canal é uma caixinha.** A identidade de formato de cada canal (estrutura de roteiro, hook, título, thumb, visual, voz) está na **bíblia** `canais/<slug>/biblia/`, e ela **prevalece** sobre `conhecimento/`. Antes de qualquer etapa, leia **primeiro** a bíblia do canal (README + o arquivo da etapa). **Nunca aplique padrão de outro canal**, nem copie roteiro/código de vídeo de outro canal como modelo. Erro real que motivou a regra: os capítulos-objeto do Archive in Minutes (molde do `dossie-es`) usados no Irã do `historia-ptbr`, que modela o History in Minutes (04/11/2026; `conhecimento/anti-padroes.md` §8). O `estilo.md` é só um índice para a bíblia (decisão de 04/11/2026: assim nenhum link antigo quebra e não há dois lugares com regra).
2. **Todo vídeo novo** é uma pasta em `canais/<slug>/videos/NNN-slug/` e segue `playbooks/produzir-video.md`.
3. **Leia a bíblia do canal e depois `conhecimento/` antes de produzir.** **Registre o que aprender, sempre com data e fonte** (sem dado = **Hipótese**):
   - aprendizado de um vídeo (hook que funcionou, padrão de thumb, CTR, retenção, voz, estilo de imagem) vai para a **bíblia do canal dele**;
   - só sobe para `conhecimento/` o que for **comprovadamente geral** (vale para qualquer canal: armadilha de ferramenta, custo, processo, como medir). Na dúvida, fica na bíblia;
   - o que mudar um procedimento vai no playbook/skill. Depois, **faça um commit descritivo** (git como memória). A fábrica deve sobreviver a uma troca de agente.
4. **Decisões do Rodrigo** (publicar, gastar dinheiro, criar ou entrar em contas) são dele. Prepare tudo e peça.
5. Cota da API do YouTube: 10 mil unidades por dia para todos os canais; `search.list` custa 100.

## Banco de dados (Postgres `vida`, esquema `youtube`)
Acesso local sem senha, como o usuário do sistema: `psql -d vida`, ou `tools/db.py` em Python. O esquema está em `tools/db/schema_youtube.sql` (idempotente).
| Tabela | O que guarda | Quem grava |
|---|---|---|
| `canais` | nossos canais (slug = pasta em `canais/`) | manual / agente |
| `videos` | esteira: cada vídeo nosso e o status (ideia → roteiro → producao → qa → pronto → publicado); `biblia_versao` = versão da bíblia de roteiro do vídeo (historia-ptbr: v1 = 001–005, v2 = 006+; comparativo em `canais/historia-ptbr/biblia/README.md`) | **o agente: atualize ao avançar uma etapa e, ao publicar ou republicar, grave `youtube_id`, `publicado_em` e o título no ar** |
| `metricas_canal`, `metricas_video` | snapshot diário dos nossos canais e vídeos | `report.py --coletar` (rotina diária) |
| `garimpo_execucoes`, `garimpo_canais`, `garimpo_snapshots`, `garimpo_videos` | garimpo de tendências e histórico de crescimento | `trends.py` |
| `assistidos` | vídeos analisados (hook, cortes por minuto, anúncios, assets) | `watch.py` |
| `palavras_chave` | termos e padrões de busca por semana (data, idioma, termo, origem autocomplete/titulo, destino sugerido, mediana top-10, recentes > 100 mil, no molde, score, tendência novo/subindo/estavel/caindo; idade dos canais pelo 1º vídeo; origens `exploracao_*` do módulo de Exploração fora do nosso nicho); view `palavras_chave_ultima`; DDL em `tools/db/schema_palavras_chave.sql` | `keywords.py` |
| `canais_idade` | cache do 1º vídeo público de cada canal (idade do canal = 1º vídeo, não criação; DDL em `tools/db/schema_palavras_chave.sql`) | `keywords.py` |
| view `garimpo_crescimento` | crescimento de views de cada canal garimpado entre execuções | — |
| `execucoes_claude` | cada chamada do Claude Code: vídeo, etapa, modelo, sessão, duração, turnos, tokens, `custo_usd_equivalente`, erro e resumo do resultado (DDL em `tools/db/schema_execucoes_claude.sql`) | `tools/claude_run.py` |
| view `custo_claude_por_video` | soma por vídeo e etapa (ignora `etapa = 'teste'` e as rotinas sem vídeo) | — |
- Na análise do garimpo, grave a fórmula e a decisão em `garimpo_canais.formula` e `garimpo_canais.decisao` (investir | testar | descartar).
- Arquivos continuam sendo a saída de mídia e texto longo. O banco é a fonte para consultas, histórico e números.
- Rotinas (systemd user, independentes do Hermes; guia em `tools/rotinas/README.md`): `diaria.sh` (06:30, coleta + backup em `~/backups/vida`, 14 dias), `metricas.sh` (seg 08:15), `tendencias.sh` (seg/qui 09:30) e `palavras-chave.sh` (qua 09:30, `playbooks/palavras-chave.md`; só sugere, não edita backlog nem bíblia). As três últimas rodam `claude -p` via `claude_run.py` (etapas `metricas`/`tendencias`/`palavras-chave`, sem vídeo), gravam em `~/workspace/relatorios/<rotina>/` e mandam o resumo no Telegram.
- Subagentes do Claude Code: `agentes-claude/` (`produtor`, `tendencias`, `metricas`); entrada em `CLAUDE.md`. Todos leem a bíblia do canal primeiro; a skill `qa` reprova vídeo que não segue a bíblia do canal.

## Custos
- Toda geração paga (TTS, imagens etc.) deve registrar o custo em `financas.consumo`, com `ref_id` = `youtube.videos.id` do vídeo. O `tts_fish.py --video <id>` já faz isso.
- Antes de produzir um vídeo, crie a linha dele em `youtube.videos` para ter o id. Consulte o custo em `financas.custo_por_video`.
- Saldo de crédito pré-pago (Fish, OpenAI, fal.ai): `SELECT * FROM financas.saldo_pre_pago`. O da OpenAI só é confiável se todas as recargas estiverem lançadas em `financas.lancamentos`; em 04/11/2026 estava negativo por falta de lançamento.
- Os custos reais por vídeo e os erros que custaram dinheiro estão em `conhecimento/anti-padroes.md`.
- Claude Code: rode cada etapa via `tools/claude_run.py --video <id> --etapa <etapa>` (opus em roteiro/storyboard, sonnet no resto). O uso fica em `youtube.execucoes_claude` / `youtube.custo_claude_por_video` (preço de lista equivalente; o Claude Max real entra no rateio fixo).

## Execução headless (`claude -p`)
Em `-p` o fim do turno é o fim da execução: nunca termine com subagente, shell ou processo em segundo plano pendente (o harness mata tudo). Task e comandos longos em primeiro plano; tudo concluído, commitado e com push antes da resposta final, ou `BLOQUEIO.md`. Regra global em `~/.claude/CLAUDE.md`; `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0` fica no settings e nos wrappers.
