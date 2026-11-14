# Playbook — produzir um vídeo

Orquestrador (Hermes) planeja, delega e confere; o Claude Code implementa. **Antes de começar, leia a bíblia do canal** (`canais/<slug>/biblia/`: README, roteiro, título, thumb, visual, voz) e o `canal.yaml`. A bíblia **prevalece** sobre este playbook e sobre `conhecimento/` em tudo o que for formato (estrutura, hook, título, thumb, visual, voz); aqui fica o procedimento comum. **Nunca aplique o padrão de um canal em outro** (`conhecimento/anti-padroes.md` §8). As skills que executam cada etapa estão em `skills/` (orquestradora: `skills/produzir-video/SKILL.md`).

## Execução econômica: 3 chamadas curtas do Claude Code
O vídeo **não** roda numa sessão só. São 3 execuções de `tools/claude_run.py` (wrapper de `claude -p --output-format json`), cada uma com um briefing próprio (`.prompt-<etapa>.md` na pasta do vídeo), em background e com timeout longo:

| # | Etapa (`--etapa`) | Modelo | Cobre |
|---|---|---|---|
| 1 | `roteiro-storyboard` | opus | §1, §1b (embalagem + crivo), §2 e storyboard: `roteiro.py` → `SCRIPT.md`, `blocos.json`, `cenas.json`, `STORYBOARD.md`, `storyboard.json` |
| 2 | `producao` | sonnet | §3–4: voz (`tts_fish.py`) + imagens (`img_openai.py`) + thumb-base |
| 3 | `montagem-render` | sonnet | §5–7: `build.py`, render, QA (`QA.md`), thumbnail final e `out/youtube.txt` |

```bash
cd ~/workspace/fabrica-youtube
V=canais/historia-ptbr/videos/003-tema; ID=5          # ID = youtube.videos.id
mkdir -p $V/logs
nohup tools/claude_run.sh --video $ID --etapa roteiro-storyboard --cwd $V \
  --prompt-file $V/.prompt-roteiro.md --timeout 5400 > $V/logs/claude-roteiro.out 2>&1 &
tools/claude_run.sh --video $ID --etapa producao --cwd $V --prompt-file $V/.prompt-producao.md --dry-run   # confere antes
```
- **Modelo:** opus em `roteiro`, `storyboard` e `roteiro-storyboard`; sonnet no resto. `--modelo` sobrescreve (só com motivo).
- **Trava:** uma execução por vídeo+etapa (`~/.cache/fabrica/locks/claude-<video>-<etapa>.lock`). Se já estiver rodando, a 2ª sai com aviso e código 3, sem chamar o Claude. Não "tente de novo em paralelo".
- **Saída:** texto final no stdout, resumo (turnos, tokens, custo) no stderr e JSON bruto em `<pasta>/logs/claude-<etapa>-<data>.json`. Código ≠ 0 = erro ou timeout.
- **Custo:** cada chamada vira uma linha em `youtube.execucoes_claude`; por vídeo: `SELECT * FROM youtube.custo_claude_por_video WHERE video_id = <id>;`. O `custo_usd_equivalente` é preço de lista (no plano Max não é cobrança real; serve para comparar etapas e modelos). Testes usam `--etapa teste`, que a view ignora.
- Se uma etapa falhar, corrija o briefing e rode **a mesma etapa** de novo (no máximo 2 rodadas); não junte etapas para "ganhar tempo".

## Como acionar o Produtor (sob demanda, sem cron)
- **Hermes desktop:** perfil `produtor`, ou peça ao default, que delega ao `produtor`.
- **Claude Code:** `cd ~/workspace/fabrica-youtube && claude`, e peça o subagente `produtor` (`agentes-claude/produtor.md`) ou a skill `produzir-video`.
- **Headless:** `tools/claude_run.sh --video <id> --etapa <etapa> ...`, uma etapa por vez (acima). As rotinas agendadas (métricas, tendências) estão em `tools/rotinas/README.md`.

## 0. Pasta do vídeo
`canais/<slug>/videos/NNN-slug/`, com numeração sequencial por canal. Copie o setup Remotion do vídeo mais recente do mesmo canal, sem node_modules, e rode `npm install`.

## 1. Brief (`BRIEF.md`)
- Tema, título de trabalho, duração-alvo, idioma, fórmula do canal.
- **Modelo de referência** (vídeo que performou, do **canal-modelo da bíblia** ou do mesmo formato): estrutura, hook, duração. Modele a estrutura; nunca traduza ou copie o texto.
- Use `tools/watch.py <ID>` na referência para ter o hook real e os frames.
- Critérios de pronto e restrições do canal.

## 1b. Embalagem + crivo (antes do roteiro; desde 14/11/2026)
Título (T1/T2) + conceito de thumb + promessa com pesquisa real no YouTube, avaliados por crivo independente: `skills/embalagem/SKILL.md` e `CRIVO.md`. Saída `EMBALAGEM.md` + `CRIVO.md`; reprovado 3× = `BLOQUEIO.md`. O portão é só o crivo (o Rodrigo não aprova cada embalagem). O roteiro abaixo paga a promessa no hook/1º minuto.

## 2. Roteiro (`SCRIPT.md` + `SOURCES.md`)
- **Estrutura, hook, capítulos, transições, fecho e tamanho: `canais/<slug>/biblia/roteiro.md`** (cada canal tem a sua; ex.: historia-ptbr = narrativa contínua em eras ligadas; dossie-es = expedientes encadeados; lotr-fr = do familiar à pergunta com payoff no fim).
- Comum a todos: **abra um loop** no hook e pague; fecho com payoff e pergunta para os comentários; palavras pela tabela "Tamanho" da bíblia (ritmo medido da voz do canal). Um bloco = um arquivo de áudio.
- Fatos com fonte. Estimativa é dita como estimativa. Fato não confirmado leva `[PENDENTE]` e uma versão sem o fato, que é a que se usa se ele não for confirmado. **Não trave por isso.**

## 3. Voz
Use o motor e a voz do `canal.yaml`, com o tom, as pausas e as tags da `biblia/voz.md` do canal. Não use Piper nem Edge TTS.
- **Fish** (`motor: fish`): `tools/.venv/bin/python tools/tts_fish.py <canal> <blocos.json> <pasta> --video <id>`. Ele usa a voz, o modelo e a velocidade do canal e registra o custo no vídeo.
  Direção no texto: `[break]` entre ideias, `[long-break]` antes de revelações, `[emphasis]` antes da palavra-chave do hook e tom no início da frase (`[determined]`, `[soft tone]`, `[slightly sad]`). No máximo 3 marcações por frase; não exagere. Tags de tom do s2.1-pro que funcionam e não são lidas: `[curious]`, `[serious]`, `[amazed]`, `[warm]`, `[slightly dramatic]`.
- **Imagens (`img_openai.py`):** rode lotes grandes com `nohup … > log &` e acompanhe pela contagem de arquivos (o log só aparece no fim, e o custo só é gravado no fim: se a execução for interrompida, o custo daquele lote se perde). Em `medium`, 204 imagens levaram ~25 min e custaram ~US$ 11,3 (US$ 0,055/imagem); a thumb em `high` custa ~US$ 0,22.
- **Não rode 2 `img_openai.py` em paralelo na mesma pasta** (ex.: a lista invertida para acelerar): cada um calcula os pendentes só no início, e eles regeram o que o outro já fez quando se cruzam (no 002 foram 27 gerações em dobro, ~US$ 1). Se precisar de velocidade, use `--paralelo 8` num processo só. Desde 04/11/2026 o `img_openai.py` e o `img_fal.py` travam a pasta (`<pasta>/.img.lock`; o 2º processo sai com aviso, código 3) e re-checam cada id logo antes da chamada paga. Com `insufficient_quota`/"no credits", o script segue registrando falhas: pare, escreva `BLOQUEIO.md` e cubra as faltas com reuso.
- **Kokoro** (`motor: kokoro`): `~/tts/venv-kokoro/bin/python` (exemplo em `~/tts/gen_kokoro.py`), sem custo.

## 4. Visual
- Siga a `biblia/visual.md` do canal (identidade das imagens, ritmo, reuso, texto na tela). Troque de visual a cada ~4–8 s, com Ken Burns ou parallax em imagens paradas.
- **Fidelidade:** a cena que nomeia um lugar ou personagem precisa mostrar **aquele** lugar ou personagem de forma crível. Nunca use um lugar real reconhecível no lugar de um fictício (erro já cometido: o Mont-Saint-Michel como Minas Tirith).
- **Não desenhe cidades ou personagens "por código"** (blocos e formas simples): fica amador. Use ilustração ou pintura real (domínio público, Google com crédito ou imagem gerada por IA no estilo do canal).
- Proibido usar frames de filmes ou séries (Content ID).
- **Texto na tela:** legenda embaixo e, no máximo, palavras-chave. Nunca repita a mesma frase em título grande e legenda ao mesmo tempo. Um único "placar" ou HUD por vez; nada sobreposto.
- Crédito pequeno no canto, com a lista completa na descrição.

## 5. Implementação e render (Claude Code)
- Divida em etapas (roteiro → produção → render/QA) com `tools/claude_run.py` (ver "Execução econômica" no topo) para não estourar o limite de turnos de uma sessão.
- **Ambiente (aprendido no Egito, 11/2026):** o Node fica em `~/.hermes/tools/node-26.12.1-linux-x64/bin` (não está no PATH). O Remotion não serve arquivos de `public/` que sejam symlinks: use hard links. Com `"type": "commonjs"` no package.json, módulos com `export` precisam ser `.jsx`. Jobs longos (geração de imagens, render) rodam com `nohup` e um marcador no log (`RENDER_OK`); o `img_openai.py` só grava o custo no fim, então, se ele for interrompido, lance o custo à mão. O faster-whisper do venv falha ao abrir arquivo (PyAV); decodifique com ffmpeg para numpy e passe o array.
- **Tempos reais:** reescale os planos de cada bloco pela duração real do áudio (apare o silêncio de cada bloco; ~0,15 s entre blocos e ~0,5 s antes de capítulo). Modelo pronto em `canais/historia-ptbr/videos/001-egito/tools/build.py` (voz, trilha gerada no código com ducking, timeline, .srt e capítulos).
- Render principal em 1080p30, mais uma versão de até 45 MB (720p) só para revisão no Telegram. **Nunca suba no YouTube a versão do Telegram.**

## 6. QA (o orquestrador confere antes de entregar) → `QA.md`
- [ ] A duração bate com a meta
- [ ] Contact sheet de ~20 frames, mais 1 frame de **cada** cena com nome: imagem fiel, nenhum lugar real, nenhum frame de filme, nada cortado ou sobreposto, nenhuma tela vazia
- [ ] Voz sempre acima da música, sem clipping
- [ ] Voz × roteiro: transcreva com Whisper e compare (palavras faltando ou repetidas). Modelo em `canais/historia-ptbr/videos/001-egito/tools/{transcrever.py,qa.sh}`
- [ ] Legenda (.srt) sincronizada
- [ ] **Segue a bíblia do canal** (roteiro, título, thumb, visual, voz) e nada de "O que NÃO fazer aqui" do `biblia/README.md`
- [ ] Máximo de 2 rodadas de correção com o Claude Code; o que sobrar vai como pendência

## 7. Pacote de publicação (`out/`)
- `video.mp4` (1080p), `thumbnail.jpg` (**JPG com menos de 2 MB**), `legendas.srt`, `youtube.txt`.
- `youtube.txt`: título na fórmula da `biblia/titulo.md`; descrição curta com gancho, CTA de comentário, **capítulos em ordem crescente começando em 0:00** (confira os tempos pela legenda), fontes e créditos resumidos; tags.
- Lembre o Rodrigo ao publicar: idioma do vídeo, **"conteúdo alterado ou sintético" = sim** (voz sintética), "não é para crianças".
- A publicação é sempre do Rodrigo.

## 8. Depois de publicar
Registre o vídeo no `backlog.md` como publicado (data e ID). Copie a thumb no ar para `conhecimento/thumbnails/<canal>-<video>.jpg` e analise-a na `biblia/thumb.md`. Após 3–7 dias, rode `playbooks/revisar-metricas.md`. Aprendizados do vídeo vão para a **bíblia do canal**; só o que for geral sobe para `conhecimento/`.
