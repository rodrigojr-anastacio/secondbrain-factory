---
name: montagem-render
description: Use quando voz e imagens de um vídeo da fábrica do YouTube estiverem prontas para montar a timeline (build.py com tempos reais, trilha com ducking, .srt e capítulos) e renderizar em Remotion o out/video.mp4 1080p30 numa GPU do Runpod (tools/render_runpod.sh; VPS só como fallback).
---

# montagem-render: áudio + imagens + storyboard → out/video.mp4

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`.
Procedimento-base: `playbooks/produzir-video.md` §4–5 (sobretudo "Ambiente" e "Tempos reais"). Modelo recomendado: **sonnet** (etapa `montagem-render`).

## Antes de agir
0. **Primeiro a bíblia do canal** (caixinha): `canais/<slug>/biblia/README.md` (canal-modelo e "o que NÃO fazer aqui") e `biblia/visual.md` (texto na tela, placas de capítulo, créditos, HUD, ritmo, trilha) e `biblia/voz.md` (pausas entre blocos). A bíblia **prevalece** sobre `conhecimento/` (só regras gerais). Nunca aplique padrão de outro canal.
1. Leia `canais/<slug>/canal.yaml`.
2. Leia `conhecimento/anti-padroes.md` (narração corrida, texto sobreposto, versão do Telegram) e `conhecimento/erros-qa.md` (erros já pegos + **checklist de pré-render**).
3. Leia `$V/BRIEF.md` (duração-alvo), `$V/ETAPA2.md` e confira que `$V/audio/` e `$V/imagens/` estão completos.
4. Modelo de código: `tools/{build.py,render.sh}` e `src/{Video.jsx,index.jsx,labels.jsx}` do **vídeo anterior do mesmo canal** (historia-ptbr: `videos/002-india/`; dossie-es: `videos/001-cia/`). Nunca copie o template visual de outro canal.

## Passos
1. **Ambiente:** `export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH`; `cd $V && npm install` se faltar `node_modules`. O Remotion não serve symlinks em `public/`: use hard links (`ln`, sem `-s`).
2. **Montagem:** `cd $V && ~/workspace/fabrica-youtube/tools/.venv/bin/python tools/build.py`. Ele apara o silêncio de cada bloco, aplica pausas de 0,35 s (mesmo assunto), 0,9 s (`ideia`) e 1,5 s (capítulo), gera trilha com ducking, `src/timeline.json`, `out/legendas.srt`, `qa/capitulos.json` e imprime duração e nº de planos.
3. Confira o JSON impresso (duração × meta; `plano_min_s` ≥ ~1,5 s) antes de renderizar.
4. **Pré-QA obrigatório antes do render do vídeo** (na VPS; `node tools/remotion_stills.cjs <dir> <bundle> <Composição> <saída> swangle 0.5 q1,q2,…` faz todos os stills com um navegador só) (Em Relevo 002, 10/11/2026: ~8 h de render perdidas por fundo errado atrás do mapa, que uma varredura teria pego em minutos):
   - renderize **stills a cada ~10 s** do vídeo e **em toda troca de cena/estilo** (`npx remotion still`, um por vez, baixa resolução serve), monte uma **grade** (contact sheet) e confira cada quadro contra o **checklist de pré-render** de [`conhecimento/erros-qa.md`](../../conhecimento/erros-qa.md);
   - **pré-QA visual automático (obrigatório, desde 12/11/2026):** com os stills em `$V/preqa/` (nome `<quadro>.png`, saída do `remotion_stills.cjs`), rode
     `tools/.venv/bin/python tools/preqa_visual.py $V --video <id>` (a partir da raiz do repo; `--fps` se não for 30). Ele manda os quadros ao Claude Sonnet com visão (chave `~/.segredos/anthropic/qa.env`, créditos da API) com o checklist de `erros-qa.md`, grava `$V/PREQA-visual.md` (+ `.json`) com tempo e severidade e **sai ≠ 0 se houver bloqueante**: não renderize com bloqueante aberto (corrija, refaça os stills do trecho e rode de novo; falso positivo = anote no `ETAPA3.md` e siga). Custo ~US$ 0,002/quadro (~US$ 0,15–0,25 por vídeo de 12 min), gravado em `financas.consumo` com o vídeo. Ele **não substitui o seu olho na grade**: os dois juntos;
   - corrija e refaça os stills dos trechos afetados; só então renderize tudo;
   - **vale de novo sempre que código ou estilo mudar no meio** (nova cena 3D, novo componente, troca de fundo/mapa): refaça a varredura inteira, não só o trecho mexido;
   - registre no `ETAPA3.md` quantos stills e o que a grade pegou; o que pegar vira entrada em `erros-qa.md`.
5. **Render: TODO render de vídeo vai para a GPU do Runpod** (decisão do Rodrigo, 11/11/2026): vídeo inteiro, partes, refações de slot, clipes. Na VPS ficam só stills, thumbs, grades do pré-QA e testes de segundos (o boot do Pod, ~1–3 min, custaria mais que o render).
   ```
   cd ~/workspace/fabrica-youtube
   VIDEO=<id> PROJETO=<canal> AUDIO=$V/public/audio/mix.wav ENTRY=src/index.jsx \
     tools/render_runpod.sh $V <Composição> $V/out/video.mp4 [a-b] > $V/logs/render_gpu.log 2>&1
   ```
   - Espere `RENDER_OK` no log. Vídeo de 12 min: ~15–25 min no total (stills de referência na VPS ~8 s cada + Pod ~10–15 min), **US$ 0,05–0,20**, custo gravado sozinho em `financas.consumo` com `VIDEO`.
   - O script já faz: bundle, stills de referência na VPS a cada 10 s (`AMOSTRA_S`), Pod com GPU (lista em ordem, Community → Secure, repete a cada 1 min), **prova** de quadros no Pod antes, render em blocos de 60 s, **conferência densa** de cada bloco contra a VPS (refaz o bloco reprovado), junta, confere nº de quadros, põe o áudio e **destrói o Pod sempre** (confere pela API). Opções no cabeçalho do script: `AUDIO` (obrigatório, ou `MUDO=1`: render mudo + `mix.wav` em AAC 192k, igual ao `render.sh juntar`; áudio dentro da composição não é suportado), `AUDIO_AF` (filtro, ex. loudnorm do Em Relevo), `PROVAS`, `CONC`, `BLOCO_S`, `REFS=<dir>` (guarda os stills de referência: refação não refaz os ~8–10 min de stills na VPS).
   - Passe em `PROVAS` quadros das cenas 3D/pesadas (relevo, globo, satélite): é onde a GPU já errou sem dar erro.
   - **Render pesado na VPS derrubou a VPS (12/11/2026, Clearance 001):** Chrome do Remotion ~2,5 GB + jobs + Hermes encheram os 8 GB e o OOM killer matou a sessão do orquestrador e o job. Antes de cair para a VPS: tente o trecho de novo no Runpod em faixas menores (`BLOCO_S` menor) e **ache a mídia que quebra** (imagem gigante, vídeo com codec/GOP ruim) e corrija. Se ainda assim for VPS: `--concurrency=1`, faixas ≤ 900 quadros, nada mais pesado rodando (`free -h` com ≥ 3 GB disponíveis).
   - **Fallback na VPS** só se o script sair com **4** (sem GPU após ~30 min), **2** (prova reprovada em 2 máquinas) ou **3** (bloco reprovado após refazer 2×): `tools/render.sh` do vídeo, um por vez (2 vCPU, ~15–30 min por 8 min de vídeo; vídeo com 3D: horas). Antes, confira que não há outro render: `pgrep -af "^node .*remotion (render|still)"` (ancorado em `^node`, erro real no dossie-es/002, 05/11/2026; laço pronto em `canais/dossie-es/videos/002-mossad/tools/espera_render.sh`).
   - Nunca `--chrome-mode=chrome-for-testing` (some o 3D) e nunca desligue as conferências: GPUs iguais já renderizaram diferente sem erro ([`erros-qa.md`](../../conhecimento/erros-qa.md), 11/11/2026).
   - Referência e medições: `pesquisa/render-gpu-2026-11/RELATORIO.md`; imagem do Pod: `tools/render-gpu-image/`.
6. Versão de revisão para o Telegram (≤ 45 MB, 720p) só se o Rodrigo pedir; **nunca** suba essa versão no YouTube.
7. Status: `psql -d vida -c "UPDATE youtube.videos SET status='qa', duracao_s=<s>, atualizado_em=now() WHERE id=<id>"`.

## Critérios de pronto (avaliar)
Rode `cd $V && bash tools/qa.sh` (specs, contact sheet, cortes no 1º minuto, telas pretas, loudness, silêncios):
- Duração bate com o N do título/meta do BRIEF (±30 s).
- 1920x1080, 30 fps, H.264 + AAC.
- Loudness integrada ~-15 LUFS, pico < -1 dBTP; voz acima da trilha.
- 0 telas pretas ≥ 0,2 s; 0 silêncios > 1,5 s fora de capítulo; ≥ ~21 cortes no 1º minuto.
- **Pré-QA feito** (grade de stills conferida contra o checklist de `erros-qa.md` **e** `tools/preqa_visual.py` sem bloqueante aberto, `$V/PREQA-visual.md`) antes do render completo.
- Texto na tela, placas e trilha no padrão da `biblia/visual.md` do canal.
- `.srt` e capítulos gerados. Relatório em `$V/ETAPA3.md`.

## Loop de melhoria
1. **Avaliar:** compare a saída do `qa.sh` com cada critério acima.
2. **Corrigir:** até 2 rodadas (ajustar `build.py`/ducking/plano e re-render no Runpod; trecho com `[a-b]`). Re-render custa minutos e centavos, mas refaça o pré-QA do que mudou. Resto = pendência no `ETAPA3.md`.
3. **Registrar:** ajuste de edição/ritmo/texto na tela do canal em **`canais/<slug>/biblia/visual.md`**; erro de ambiente/render (vale para todos) em `conhecimento/anti-padroes.md`; erro visual/de tela pego (no pré-QA ou depois) em `conhecimento/erros-qa.md` (e no playbook §5 se mudar procedimento). Sempre com **data e fonte**; sem dado = **Hipótese**.
4. **Commitar:** `git add $V/tools/build.py $V/tools/render.sh $V/src/*.jsx $V/ETAPA3.md` (sem mídia; `src/timeline.json` só se pequeno) e
   `git commit -m "<canal>/<NNN>: render 1080p (MM:SS, -15 LUFS)"`.
