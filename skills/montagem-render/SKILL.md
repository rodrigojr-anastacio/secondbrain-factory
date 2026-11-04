---
name: montagem-render
description: Use quando voz e imagens de um vídeo da fábrica do YouTube estiverem prontas para montar a timeline (build.py com tempos reais, trilha com ducking, .srt e capítulos) e renderizar em Remotion o out/video.mp4 1080p30, um render por vez.
---

# montagem-render: áudio + imagens + storyboard → out/video.mp4

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`.
Procedimento-base: `playbooks/produzir-video.md` §4–5 (sobretudo "Ambiente" e "Tempos reais"). Modelo recomendado: **sonnet** (etapa `montagem-render`).

## Antes de agir
1. Leia `canais/<slug>/estilo.md` (texto na tela, créditos, HUD) e `canais/<slug>/canal.yaml`.
2. Leia `conhecimento/roteiros.md` (ritmo, capítulos) e `conhecimento/anti-padroes.md` (narração corrida, texto sobreposto, versão do Telegram).
3. Leia `$V/BRIEF.md` (duração-alvo), `$V/ETAPA2.md` e confira que `$V/audio/` e `$V/imagens/` estão completos.
4. Modelo de código: `canais/historia-ptbr/videos/002-india/tools/{build.py,render.sh}` e `src/{Video.jsx,index.jsx,labels.jsx}`.

## Passos
1. **Ambiente:** `export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH`; `cd $V && npm install` se faltar `node_modules`. O Remotion não serve symlinks em `public/`: use hard links (`ln`, sem `-s`).
2. **Montagem:** `cd $V && ~/workspace/fabrica-youtube/tools/.venv/bin/python tools/build.py`. Ele apara o silêncio de cada bloco, aplica pausas de 0,35 s (mesmo assunto), 0,9 s (`ideia`) e 1,5 s (capítulo), gera trilha com ducking, `src/timeline.json`, `out/legendas.srt`, `qa/capitulos.json` e imprime duração e nº de planos.
3. Confira o JSON impresso (duração × meta; `plano_min_s` ≥ ~1,5 s) antes de renderizar.
4. **Render** (um por vez; 2 vCPU, ~15–30 min por 8 min de vídeo):
   `cd $V && mkdir -p logs && nohup tools/render.sh > logs/render.log 2>&1 &` e espere `RENDER_OK` no log (ajuste o id da composição no `render.sh`).
   Antes, confira que não há outro render: `pgrep -af "remotion render"`.
5. Versão de revisão para o Telegram (≤ 45 MB, 720p) só se o Rodrigo pedir; **nunca** suba essa versão no YouTube.
6. Status: `psql -d vida -c "UPDATE youtube.videos SET status='qa', duracao_s=<s>, atualizado_em=now() WHERE id=<id>"`.

## Critérios de pronto (avaliar)
Rode `cd $V && bash tools/qa.sh` (specs, contact sheet, cortes no 1º minuto, telas pretas, loudness, silêncios):
- Duração bate com o N do título/meta do BRIEF (±30 s).
- 1920x1080, 30 fps, H.264 + AAC.
- Loudness integrada ~-15 LUFS, pico < -1 dBTP; voz acima da trilha.
- 0 telas pretas ≥ 0,2 s; 0 silêncios > 1,5 s fora de capítulo; ≥ ~21 cortes no 1º minuto.
- `.srt` e capítulos gerados. Relatório em `$V/ETAPA3.md`.

## Loop de melhoria
1. **Avaliar:** compare a saída do `qa.sh` com cada critério acima.
2. **Corrigir:** até 2 rodadas (ajustar `build.py`/ducking/plano e re-render). Re-render custa 15–30 min: junte as correções antes. Resto = pendência no `ETAPA3.md`.
3. **Registrar:** erro de ambiente/render ou ajuste de áudio que resolveu em `conhecimento/anti-padroes.md` (e no playbook §5 se mudar procedimento), com **data e fonte**; sem dado = **Hipótese**.
4. **Commitar:** `git add $V/tools/build.py $V/tools/render.sh $V/src/*.jsx $V/ETAPA3.md` (sem mídia; `src/timeline.json` só se pequeno) e
   `git commit -m "<canal>/<NNN>: render 1080p (MM:SS, -15 LUFS)"`.
