# Skills do Produtor de vídeo: mapa (Fase 2, ainda NÃO implementadas)

Este é o plano das skills do especialista **Produtor de vídeo** (`~/workspace/referencias/PLANO-ARQUITETURA.md`, itens 9 e 11). Hoje a esteira roda pelo `playbooks/produzir-video.md` e pelas tools. Cada skill abaixo vai virar uma pasta `skills/<nome>/` com `SKILL.md` quando for implementada.

## Regras comuns a todas as skills
1. **Antes de agir, leia** o `canal.yaml`, o `estilo.md` do canal e os arquivos de `conhecimento/` indicados na skill. `conhecimento/anti-padroes.md` vale para **todas**.
2. **Uma execução curta por skill** (o vídeo não roda numa sessão só). Modelo sugerido: Opus no roteiro e no storyboard; Sonnet em imagens, voz, Remotion, render e QA. [PLANO, item 11]
3. Toda geração paga usa `--video <youtube.videos.id>` (o custo vai para `financas.consumo`) e respeita o **teto do BRIEF**. Antes de gerar, confira `financas.saldo_pre_pago`.
4. Ao terminar, a skill atualiza `youtube.videos.status` e escreve o relatório da etapa (`ETAPA*.md`).
5. **Loop "avaliar e sugerir melhoria"** (obrigatório no fim de cada skill):
   - **Avaliar:** compare a saída com os critérios da skill (tabela abaixo) e com o que o `conhecimento/` diz. Use números (duração, nitidez, % de concordância do Whisper, custo), não impressão.
   - **Corrigir:** se falhar, refaça no máximo 2 rodadas. O que sobrar vira pendência no relatório.
   - **Sugerir:** escreva no relatório 1–3 melhorias para a próxima vez. Se a melhoria for um aprendizado comprovado, registre em `conhecimento/` (ou no `estilo.md`) **com data e fonte** e faça commit descritivo. Se ainda não tiver dado, registre como **Hipótese**.
   - Depois de publicar, o especialista de **Métricas** fecha o loop: confirma ou derruba as hipóteses com views, retenção e CTR.

## Mapa
| Skill | Entrada | Saída | Ferramentas | Lê em `conhecimento/` | Critérios para avaliar |
|---|---|---|---|---|---|
| **pesquisa-referencia** | tema; canal; `pesquisa/tendencias/` e `youtube.assistidos` | `BRIEF.md` (referência, hook real, duração-alvo, teto de custo); linha em `youtube.videos` | `tools/watch.py`, `tools/transcrever.py`, `psql` | `titulos.md`, `hooks.md`, `roteiros.md` | a referência tem tração (views/idade); a fórmula do título está definida; o teto de custo está explícito |
| **roteiro** | `BRIEF.md`; transcrição da referência | `roteiro.py` (fonte única) → `SCRIPT.md`, `blocos.json` (com `ideia`), `SOURCES.md` | Python; Whisper (para a referência) | `hooks.md`, `roteiros.md`, `titulos.md` | hook ≤ ~45 s; ~2.250–2.300 palavras para 17 min (historia-ptbr); loops pagos; fatos com fonte; `[PENDENTE]` com alternativa |
| **storyboard** | `roteiro.py`/`blocos.json` | `STORYBOARD.md`, `storyboard.json`, `cenas.json` (prompts só de conteúdo) | `roteiro.py` (validação) | `anti-padroes.md` (reuso, fidelidade), `roteiros.md` | plano a cada 2–4 s (~17/min); reuso de 0% antes de 3:00 e ~40% depois; nenhum enquadramento repetido em < 60 s; nº de imagens dentro do teto |
| **voz** | `blocos.json` | `audio/<id>.mp3` por bloco | `tools/tts_fish.py --video` (Fish s2.1-pro) ou Kokoro (lotr-fr) | `anti-padroes.md` (narração corrida, Fish cortando frase) | Whisper × roteiro ≥ ~93% **por bloco**; nenhuma tag falada; nenhuma frase faltando |
| **imagens** | `cenas.json` | `imagens/*.jpg` | `tools/img_openai.py --qualidade medium` (ou `img_fal.py`), `nohup` | `anti-padroes.md` (low, duplicação, saldo) | **trava anti-duplicação**: um processo por pasta, sem paralelo cruzado; 0 imagens faltando; custo ≤ teto; nada de texto gerado pela IA |
| **montagem-render** | áudio, imagens, `storyboard.json` | `out/video.mp4` (1080p30), timeline, `.srt`, capítulos | `tools/build.py` do vídeo (pausas de 0,35/0,9/1,5 s), Remotion, `tools/render.sh` (um render por vez) | `roteiros.md`, `anti-padroes.md` | duração bate com o N do título; -15 LUFS; voz acima da trilha; 0 telas pretas |
| **thumbnail** | ilustração-base (`high`); título | 3 variações em `thumb-var/final/` + `out/thumbnail.jpg` (< 2 MB) | `img_openai.py`/`img_fal.py`; texto composto no código (`src/Thumbnail.jsx`) | `thumbnails/README.md`, `titulos.md` | nome legível no celular (2–3 palavras); lugar reconhecível; fiel ao tema; 3 variações para o "Testar e comparar" |
| **pacote-youtube** | timeline, capítulos, `SOURCES.md` | `out/youtube.txt` (título, descrição com gancho e CTA, capítulos, fontes, tags, categoria) | Python | `titulos.md`, `hooks.md` | capítulos em ordem crescente a partir de 0:00; N do título = duração; nota de voz sintética |
| **qa** | `out/` completo | `QA.md` (+ `qa/` com contact sheet, sync e Whisper) | `tools/qa.sh`, `compara_voz.py`, ffmpeg (blackdetect, loudnorm), Whisper | todos, sobretudo `anti-padroes.md` | checklist do `playbooks/produzir-video.md` §6; no máximo 2 rodadas de correção |
| **produzir-video** (orquestradora) | pedido (canal + tema) ou item do `backlog.md` | vídeo pronto para o Rodrigo publicar; `youtube.videos` em `pronto`; relatório com custo (`financas.custo_por_video`) | chama as 9 skills acima em ordem, cada uma numa execução curta | `conhecimento/` inteiro (lê antes de começar) | cada etapa passou no próprio critério; custo ≤ teto; pendências listadas; aprendizados registrados e commitados |

## Depois de publicar (fora do Produtor)
- O **Métricas** roda `playbooks/revisar-metricas.md`, pede o CTR ao Rodrigo e atualiza `conhecimento/thumbnails/README.md`, `titulos.md` e `hooks.md`.
- O **Tendências** alimenta `hooks.md`, `titulos.md` e `thumbnails/` com o que viraliza lá fora.
