# Skills do Produtor de vídeo

Skills do especialista **Produtor de vídeo** (`~/workspace/referencias/PLANO-ARQUITETURA.md`, itens 9 e 11), implementadas em 2026-11-04. Cada uma é uma pasta `skills/<nome>/SKILL.md` no formato padrão de Agent Skills (frontmatter YAML com `name` e `description`, que diz **quando** usar; corpo em markdown) e funciona igual no **Hermes** e no **Claude Code**. Elas apontam para `playbooks/produzir-video.md` e para as `tools/` reais, sem duplicar o procedimento.

## Índice
| Skill | Arquivo | Etapa do `claude_run` |
|---|---|---|
| produzir-video (orquestradora) | [`produzir-video/SKILL.md`](produzir-video/SKILL.md) | dispara as 3 abaixo |
| pesquisa-referencia | [`pesquisa-referencia/SKILL.md`](pesquisa-referencia/SKILL.md) | etapa 0 (no orquestrador) |
| roteiro | [`roteiro/SKILL.md`](roteiro/SKILL.md) | 1 `roteiro-storyboard` (opus) |
| storyboard | [`storyboard/SKILL.md`](storyboard/SKILL.md) | 1 `roteiro-storyboard` (opus) |
| voz | [`voz/SKILL.md`](voz/SKILL.md) | 2 `producao` (sonnet) |
| imagens | [`imagens/SKILL.md`](imagens/SKILL.md) | 2 `producao` (sonnet) |
| thumbnail | [`thumbnail/SKILL.md`](thumbnail/SKILL.md) | 2 (base) e 3 (final) |
| montagem-render | [`montagem-render/SKILL.md`](montagem-render/SKILL.md) | 3 `montagem-render` (sonnet) |
| pacote-youtube | [`pacote-youtube/SKILL.md`](pacote-youtube/SKILL.md) | 3 `montagem-render` (sonnet) |
| qa | [`qa/SKILL.md`](qa/SKILL.md) | 3 `montagem-render` (sonnet) |
| novo-canal (fora da esteira) | [`novo-canal/SKILL.md`](novo-canal/SKILL.md) | antes do 1º vídeo de um canal; procedimento em `playbooks/novo-canal.md` (Tendências + orquestrador, opus) |

## Como instalar (symlinks, nunca cópia: a fonte é este repo)
```bash
F=~/workspace/fabrica-youtube/skills
S="produzir-video pesquisa-referencia roteiro storyboard voz imagens thumbnail montagem-render pacote-youtube qa novo-canal"
# Claude Code (usuário): ~/.claude/skills/<nome>
mkdir -p ~/.claude/skills; for s in $S; do ln -sfn $F/$s ~/.claude/skills/$s; done
# Hermes (default): categoria fabrica-youtube
mkdir -p ~/.hermes/skills/fabrica-youtube; for s in $S; do ln -sfn $F/$s ~/.hermes/skills/fabrica-youtube/$s; done
# Perfis Hermes: produtor (todas), tendencias (pesquisa-referencia, thumbnail), metricas (qa, pacote-youtube)
for s in $S; do ln -sfn $F/$s ~/.hermes/profiles/produtor/skills/fabrica-youtube/$s; done   # após mkdir -p
```
Conferir: `hermes skills list | grep fabrica-youtube` e `hermes -p produtor skills list | grep fabrica-youtube`; no Claude Code, as skills aparecem pelo nome (ex.: `/produzir-video`). Skill nova = pasta nova aqui + os mesmos symlinks.

**Base de erros do QA:** [`conhecimento/erros-qa.md`](../conhecimento/erros-qa.md) (toda reprovação vira entrada; checklist de pré-render, obrigatório antes do render de vídeo, ver `montagem-render`).

**Render:** todo render de vídeo vai para uma GPU do Runpod com `tools/render_runpod.sh` (decisão do Rodrigo, 11/11/2026; prova + conferência densa contra stills da VPS, Pod destruído sempre, custo em `financas.consumo`). A VPS só faz stills, thumbs, grades do pré-QA e testes de segundos, e é fallback se o script sair com 2/3/4.

## Regras comuns a todas as skills
1. **Caixinha do canal primeiro.** Antes de agir, leia `canais/<slug>/biblia/README.md` e o arquivo da bíblia da etapa (`roteiro.md`, `titulo.md`, `thumb.md`, `visual.md`, `voz.md`); depois o `canal.yaml` e as **regras gerais** de `conhecimento/` (`anti-padroes.md` vale para todas). **A bíblia prevalece** sobre `conhecimento/`.
   - **Nunca aplique padrão de outro canal** (estrutura, hook, título, thumb, visual, voz), nem copie código/roteiro de vídeo de outro canal como modelo. Erro real: capítulos-objeto do Archive (dossie-es) no Irã do historia-ptbr, 04/11/2026 (`conhecimento/anti-padroes.md` §8).
   - O `estilo.md` do canal é só um índice para a bíblia.
2. **Uma execução curta por skill** (o vídeo não roda numa sessão só). Modelo sugerido: Opus no roteiro e no storyboard; Sonnet em imagens, voz, Remotion, render e QA. [PLANO, item 11]
3. Toda geração paga usa `--video <youtube.videos.id>` (o custo vai para `financas.consumo`) e respeita o **teto do BRIEF**. Antes de gerar, confira `financas.saldo_pre_pago`.
4. Ao terminar, a skill atualiza `youtube.videos.status` e escreve o relatório da etapa (`ETAPA*.md`).
5. **Loop "avaliar e sugerir melhoria"** (obrigatório no fim de cada skill):
   - **Avaliar:** compare a saída com os critérios da skill (tabela abaixo), com a bíblia do canal e com as regras gerais de `conhecimento/`. Use números (duração, nitidez, % de concordância do Whisper, custo), não impressão.
   - **Corrigir:** se falhar, refaça no máximo 2 rodadas. O que sobrar vira pendência no relatório.
   - **Sugerir:** escreva no relatório 1–3 melhorias para a próxima vez. Aprendizado de um vídeo vai para a **bíblia do canal dele** (`canais/<slug>/biblia/`), **com data e fonte**, e commit descritivo. Só sobe para `conhecimento/` o que for **comprovadamente geral** (vale para qualquer canal: ferramenta, custo, processo, medição). Sem dado = **Hipótese**.
   - Depois de publicar, o especialista de **Métricas** fecha o loop: confirma ou derruba as hipóteses com views, retenção e CTR.

## Mapa
| Skill | Entrada | Saída | Ferramentas | Lê (bíblia do canal primeiro; depois `conhecimento/`) | Critérios para avaliar |
|---|---|---|---|---|---|
| **pesquisa-referencia** | tema; canal; `pesquisa/tendencias/` e `youtube.assistidos` | `BRIEF.md` (referência, hook real, duração-alvo, teto de custo); linha em `youtube.videos` | `tools/watch.py`, `tools/transcrever.py`, `psql` | `biblia/` inteira (canal-modelo, fórmula) → `titulos.md`, `hooks.md`, `roteiros.md` | a referência tem tração (views/idade); a fórmula do título está definida; o teto de custo está explícito |
| **roteiro** | `BRIEF.md`; transcrição da referência | `roteiro.py` (fonte única) → `SCRIPT.md`, `blocos.json` (com `ideia`), `SOURCES.md` | Python; Whisper (para a referência) | `biblia/roteiro.md` → `roteiros.md`, `hooks.md` | checklist de `biblia/roteiro.md`; tamanho da bíblia; loops pagos; fatos com fonte; `[PENDENTE]` com alternativa |
| **storyboard** | `roteiro.py`/`blocos.json` | `STORYBOARD.md`, `storyboard.json`, `cenas.json` (prompts só de conteúdo) | `roteiro.py` (validação) | `biblia/visual.md` → `anti-padroes.md` (reuso, fidelidade) | ritmo e reuso da bíblia; 0% de reuso antes de 3:00; nenhum enquadramento repetido em < 60 s; nº de imagens dentro do teto |
| **voz** | `blocos.json` | `audio/<id>.mp3` por bloco | `tools/tts_fish.py --video` (Fish s2.1-pro) ou Kokoro (lotr-fr) | `biblia/voz.md` → `anti-padroes.md` (narração corrida, Fish cortando frase) | Whisper × roteiro ≥ ~93% **por bloco**; nenhuma tag falada; nenhuma frase faltando |
| **imagens** | `cenas.json` | `imagens/*.jpg` | `tools/img_openai.py --qualidade medium` (ou `img_fal.py`), `nohup` | `biblia/visual.md` → `anti-padroes.md` (low, duplicação, saldo) | identidade da bíblia; **trava anti-duplicação**: um processo por pasta, sem paralelo cruzado; 0 imagens faltando; custo ≤ teto; nada de texto gerado pela IA |
| **montagem-render** | áudio, imagens, `storyboard.json` | `out/video.mp4` (1080p30), timeline, `.srt`, capítulos | `tools/build.py` do vídeo (pausas de 0,35/0,9/1,5 s), Remotion, `tools/render_runpod.sh` (GPU Runpod; fallback `tools/render.sh` na VPS) | `biblia/visual.md`, `biblia/voz.md` → `anti-padroes.md` | duração bate com o N do título; -15 LUFS; voz acima da trilha; 0 telas pretas |
| **thumbnail** | ilustração-base (`high`); título | 3 variações em `thumb-var/final/` + `out/thumbnail.jpg` (< 2 MB) | `img_openai.py`/`img_fal.py`; texto composto no código (`src/Thumbnail.jsx`) | `biblia/thumb.md`, `biblia/titulo.md` → `thumbnails/README.md` | template da bíblia; nome legível no celular (2–3 palavras); lugar reconhecível; fiel ao tema; 3 variações para o "Testar e comparar" |
| **pacote-youtube** | timeline, capítulos, `SOURCES.md` | `out/youtube.txt` (título, descrição com gancho e CTA, capítulos, fontes, tags, categoria) | Python | `biblia/titulo.md` → `titulos.md` | título na fórmula da bíblia; capítulos em ordem crescente a partir de 0:00; N do título = duração; nota de voz sintética |
| **qa** | `out/` completo | `QA.md` (+ `qa/` com contact sheet, sync e Whisper) | `tools/qa.sh`, `compara_voz.py`, ffmpeg (blackdetect, loudnorm), Whisper | `biblia/` inteira → `conhecimento/` (sobretudo `anti-padroes.md`) | **segue a bíblia do canal?** (roteiro, título, thumb, visual, voz); checklist do `playbooks/produzir-video.md` §6; no máximo 2 rodadas de correção |
| **novo-canal** | canal de referência ou nicho | `pesquisa/<slug>/LEVANTAMENTO.md` (decisão) + `canais/<slug>/` (canal.yaml, **`biblia/` completa**, estilo.md-índice, backlog de 20, identidade, piloto, teste de estilo) | `tools/watch.py`, API do YouTube (≤ ~15 buscas), `tools/img_fal.py --video` (≤ US$ 3) | todos | ≥ 30 canais e clones contados; ≥ 6 vídeos de ≥ 3 canais; observado × inferido; decisão com critério numérico; handles conferidos; gasto ≤ US$ 3 no banco |
| **produzir-video** (orquestradora) | pedido (canal + tema) ou item do `backlog.md` | vídeo pronto para o Rodrigo publicar; `youtube.videos` em `pronto`; relatório com custo (`financas.custo_por_video`) | chama as 9 skills acima em ordem, cada uma numa execução curta | `biblia/` inteira do canal, depois `conhecimento/` | cada etapa passou no próprio critério; custo ≤ teto; pendências listadas; aprendizados registrados e commitados |

## Depois de publicar (fora do Produtor)
- O **Métricas** roda `playbooks/revisar-metricas.md`, pede o CTR ao Rodrigo e atualiza a **bíblia do canal** (`thumb.md`, `titulo.md`, `roteiro.md`); só o que for geral vai para `conhecimento/`.
- O **Tendências** registra o padrão de um formato na bíblia do canal que usa esse formato (ou no `LEVANTAMENTO` de um nicho novo); só o que for geral vai para `conhecimento/`.
