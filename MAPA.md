# MAPA do cerebro-fabrica

Este repositório (`~/workspace/fabrica-youtube`, repo git **cerebro-fabrica**) é a memória portável da fábrica de vídeos. Qualquer agente (Hermes estrategista, Produtor de vídeo, Tendências, Métricas, Claude Code ou um substituto) começa por aqui: lê este mapa, depois o `AGENTS.md` e, antes de produzir, o `conhecimento/`.

## Quem lê e quem escreve
| Repositório | Quem lê | Quem escreve |
|---|---|---|
| **cerebro-fabrica** (este) | todos os agentes | **todos os agentes**: playbooks, `conhecimento/`, canais, backlog, tools e skills |
| **cerebro-rodrigo** (`~/workspace/cerebro-rodrigo`) | só o estrategista | **só o estrategista** (perfil, decisões, inbox e domínios da vida). Os especialistas não leem nem escrevem lá |
| Postgres `vida` (`psql -d vida`) | todos | cada tool grava o que é dela (ver abaixo) |

## O que existe e onde
| Caminho | O que é |
|---|---|
| `AGENTS.md` | manual da fábrica: estrutura, regras, banco e custos |
| `MAPA.md` | este mapa |
| `conhecimento/` | **base viva do que aprendemos**, com data e fonte: `hooks.md`, `titulos.md`, `roteiros.md`, `anti-padroes.md` (com os custos por vídeo) e `thumbnails/` (thumbs no ar + `README.md` com o CTR) |
| `skills/<nome>/SKILL.md` | skills do Produtor (Agent Skills, valem no Hermes e no Claude Code via symlink): `produzir-video` (orquestradora), `pesquisa-referencia`, `roteiro`, `storyboard`, `voz`, `imagens`, `thumbnail`, `montagem-render`, `pacote-youtube`, `qa` e `novo-canal` (canal novo); índice e instalação em `skills/README.md` |
| `playbooks/` | procedimentos: `produzir-video.md` (a esteira), `garimpo-tendencias.md` (seg/qui), `revisar-metricas.md` e **`novo-canal.md`** (avaliar um nicho e montar um canal novo: concorrência, anatomia, decisão, blueprint e teste de estilo; skill `novo-canal`) |
| `tools/` | comandos determinísticos em Python (`tools/.venv/bin/python`): `tts_fish.py` (voz Fish + custo), `img_openai.py` e `img_fal.py` (imagens + custo), `watch.py` (assiste referências via WARP), `trends.py` (garimpo), `report.py` (métricas, `--coletar`, `--retencao`), `transcrever.py` (Whisper de um vídeo do YouTube), `claude_run.py`/`claude_run.sh` (roda uma etapa do Claude Code por vídeo com trava e custo em `youtube.execucoes_claude`), `auth.py` (OAuth, feito pelo Rodrigo), `db.py`, `_paths.py` e `_trava.py` (conexão, caminhos e trava por pasta das tools de imagem), `db/schema_youtube.sql`, `db/schema_execucoes_claude.sql` e `db/seed.sql`, `rotinas/` (systemd user, sem Hermes: `diaria.sh` coleta + backup às 06:30; `metricas.sh` seg 08:15; `tendencias.sh` seg/qui 09:30; prompts em `rotinas/prompts/`, units em `rotinas/systemd/`, guia em `rotinas/README.md`) |
| `CLAUDE.md`, `agentes-claude/` | entrada do Claude Code (importa o `AGENTS.md`) e os subagentes `produtor`, `tendencias` e `metricas` (mesmos papéis dos perfis Hermes) |
| `~/workspace/relatorios/<rotina>/` | fora do repo: relatório completo e resumo executivo de cada rotina (o resumo vai ao Telegram por `hermes send`, sem LLM) |
| `canais/<slug>/` | `canal.yaml` (identidade, voz, visual), `estilo.md` (padrão e aprendizados do canal), `backlog.md` (fila e publicados) |
| `canais/<slug>/videos/NNN-slug/` | um projeto por vídeo: `BRIEF.md`, `roteiro.py` (fonte única), `SCRIPT.md`, `SOURCES.md`, `STORYBOARD.md`, `blocos.json`, `cenas.json`, `ETAPA*.md` (relatório de cada execução), `QA.md`, `BLOQUEIO.md` (quando trava), código Remotion em `src/`, `tools/` do vídeo (`build.py`, `render.sh`, `qa.sh`) |
| `pesquisa/` | `trend_seeds.txt`, `trends_state.json`, `tendencias/<data>.md/.json/-analise.md` e `<slug>/` (levantamento de nicho: `LEVANTAMENTO.md`, `dados.json`, `thumbs/` fora do git), ex.: `archive-in-minutes/` |

Canais hoje (`youtube.canais`, 2026-11-04):
- `historia-ptbr`: **História em minutos** (pt-BR). Publicados: Egito (`g847Td0Plsk`) e Índia (`MV5SSjoccqE`).
- `lotr-fr`: **Le Gardien de Valinor** (fr). Publicado: cidades da Terra-média (`87BdomKxa-M`); 000-piloto-sam arquivado.
- `dossie-ptbr`: **Dossiê em Minutos** (nome provisório, pt-BR), em preparação desde 2026-11-04: história INTEIRA de organizações (KGB, Gestapo, CIA…). Piloto KGB (`youtube.videos` id 6) com roteiro pronto, aguardando o OK do Rodrigo; canal ainda não criado no YouTube. Levantamento em `pesquisa/archive-in-minutes/LEVANTAMENTO.md`.

## Banco (Postgres `vida`)
- `youtube`:
  - `canais`, `videos` (esteira e status; **o agente atualiza a cada etapa**);
  - `metricas_canal` e `metricas_video` (gravados por `report.py --coletar`, sem CTR, que só existe no Studio);
  - `assistidos` (gravado por `watch.py`);
  - `garimpo_*` (gravado por `trends.py`);
  - `execucoes_claude` (gravado por `claude_run.py`: modelo, turnos, tokens e custo equivalente de cada chamada do Claude Code) e a view `custo_claude_por_video`.
- `financas` (SQL em `~/workspace/_db/schema_financas.sql`):
  - `consumo`: uso pago por vídeo, com `ref_tipo='youtube.video'` e `ref_id` = `youtube.videos.id`; as tools gravam sozinhas com `--video <id>`;
  - `lancamentos`: recargas e assinaturas;
  - views `custo_por_video`, `saldo_pre_pago`, `custo_mensal` e `resumo_mensal`.
- Segredos **não** ficam no banco nem aqui: estão em `~/.segredos/` (fora do repo).

## Como rodar a esteira (resumo)
O procedimento completo está em `playbooks/produzir-video.md`. A skill `skills/produzir-video/SKILL.md` orquestra a esteira etapa por etapa.
1. Leia o `canal.yaml`, o `estilo.md` e o **`conhecimento/`**. Crie a linha em `youtube.videos` (para ter o id) e a pasta `canais/<slug>/videos/NNN-slug/`, copiando o setup do vídeo anterior sem `node_modules`.
2. Escreva o `BRIEF.md` com a referência (`tools/watch.py <ID>`), a meta de duração e o teto de custo.
3. Roteiro: edite o `roteiro.py` e rode `python3 roteiro.py`. Ele gera `SCRIPT.md`, `blocos.json`, `cenas.json` e `STORYBOARD.md`.
4. Gere a voz com `tools/tts_fish.py <canal> blocos.json audio --video <id>`.
5. Gere as imagens com `tools/img_openai.py <canal> cenas.json imagens --video <id> --qualidade medium`, **um processo só** e com `nohup`. Antes, confira `financas.saldo_pre_pago`.
6. Monte e renderize: `tools/.venv/bin/python tools/build.py` → `tools/render.sh` (um render por vez; 2 vCPU).
7. QA: `tools/qa.sh` (+ `compara_voz.py`) → `QA.md`.
8. Monte o pacote em `out/` (`video.mp4`, `thumbnail.jpg`, `legendas.srt`, `youtube.txt`). **A publicação é do Rodrigo.**
9. Depois de publicar, atualize `youtube.videos` (`youtube_id`, `status`, `publicado_em`) e o `backlog.md`, copie a thumb no ar para `conhecimento/thumbnails/` e, após 3–7 dias, rode `playbooks/revisar-metricas.md`.

## O que fica fora do git (`.gitignore`)
- **Mídia:** mp4, mov, wav, mp3, png, jpg, webp, srt etc. A exceção é `conhecimento/**` (thumbs < 500 KB).
- **Pastas de saída e mídia:** `out/`, `out-*/`, `imagens/`, `audio/`, `ref/`, `dl/`, `build/`, `public/`, `thumb-var/`, `thumbs-v2/`, `qa/`, `qa-*/`, `logs/`, `pesquisa/tendencias/assets/`.
- **Dependências:** `node_modules/`, `.venv/`, caches e `*.log`.
- **Segredos:** `.env*`, `*secret*`, `*credential*`, `*token*.json`, `tokens/`, `*.pem`, `*.key` e `~/.segredos` (que fica fora da pasta).
- **Atenção:** `out/`, `qa/` e `qa-v1/` também guardam texto útil (`youtube.txt`, `description.txt`, `QA-v1.md`, `out/QA.md` das cidades) que **não vai para o git**. O que importa desses arquivos deve ser resumido em `conhecimento/` ou no `ETAPA*.md` do vídeo.

## Regra de commit (git como memória)
- **A cada aprendizado ou decisão, faça um commit descritivo**, dizendo o quê e por quê. Exemplos:
  - `conhecimento/titulos: Egito republicado como "INTEIRA" (oEmbed 04/11)`
  - `playbooks/produzir-video: trava contra 2 img_openai em paralelo`
- Todo aprendizado entra em `conhecimento/` (ou no `estilo.md` do canal) **com data e fonte**. O que não tem dado fica marcado como **Hipótese**.
- O push é diário (`~/workspace/_infra/git-diario.sh`, que só faz push se o remote existir). Nunca commite mídia pesada nem segredo: antes do commit, rode `git status` e confira.
