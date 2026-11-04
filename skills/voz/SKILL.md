---
name: voz
description: Use para gerar a narração de um vídeo da fábrica do YouTube a partir do blocos.json - Fish Audio (tools/tts_fish.py, pago, com custo por vídeo) ou Kokoro local conforme o canal.yaml - e conferir com Whisper, bloco a bloco, que nenhuma frase faltou e nenhuma tag foi falada.
---

# voz: blocos.json → audio/<id>.mp3

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`. Python: `tools/.venv/bin/python`.
Procedimento-base: `playbooks/produzir-video.md` §3. Modelo recomendado: **sonnet** (etapa `voz` ou `producao`).

## Antes de agir
1. Leia `canais/<slug>/canal.yaml` (bloco `voz`: `motor`, `voz`, `modelo`, `velocidade`) e `canais/<slug>/estilo.md`.
2. Leia `conhecimento/anti-padroes.md` (narração corrida, Fish cortando frase curta depois de `[break]`) e `conhecimento/hooks.md`.
3. Leia `$V/BRIEF.md` (teto) e confira que `$V/blocos.json` é o gerado pela versão final do `roteiro.py`.
4. Saldo: `psql -d vida -c "SELECT * FROM financas.saldo_pre_pago WHERE fornecedor='Fish Audio'"`. Sem saldo para o vídeo (~US$ 0,7 num de 17 min) = pare e escreva `$V/BLOQUEIO.md`.

## Passos
1. **Fish** (`motor: fish`), da raiz do repo:
   `tools/.venv/bin/python tools/tts_fish.py <slug> $V/blocos.json $V/audio --video <id>`
   (usa voz, modelo e velocidade do canal; grava o custo em `financas.consumo`; gera um mp3 por bloco).
   **Kokoro** (`motor: kokoro`, sem custo): `~/tts/venv-kokoro/bin/python`, seguindo `~/tts/gen_kokoro.py`. Nunca Piper nem Edge TTS.
2. A tool **regera todos os blocos** da entrada (e cobra todos). Para refazer só os ruins, crie `$V/blocos-refazer.json` com apenas esses blocos (mesmo formato) e rode o mesmo comando com ele.
3. **QA por bloco:** transcreva os mp3 com Whisper (modelo em `canais/historia-ptbr/videos/002-india/tools/transcrever.py`; o faster-whisper do venv falha ao abrir arquivo: decodifique com ffmpeg para numpy) e compare com o texto do bloco sem tags (lógica de `canais/historia-ptbr/videos/002-india/tools/compara_voz.py`).
4. Status: `psql -d vida -c "UPDATE youtube.videos SET status='producao', atualizado_em=now() WHERE id=<id>"`.

## Critérios de pronto (avaliar)
- 1 mp3 por bloco de `blocos.json`, nenhum vazio (`ls $V/audio | wc -l` = nº de blocos).
- Concordância Whisper × roteiro ≥ ~93% **em cada bloco**; nenhuma tag (`[break]`, `[emphasis]`...) falada; nenhuma frase faltando no fim de bloco.
- Custo registrado: `psql -d vida -c "SELECT * FROM financas.custo_por_video WHERE id=<id>"` (ou `financas.consumo` com `ref_id=<id>`), dentro do teto.
- Relatório da etapa em `$V/ETAPA2.md` (blocos, duração total do áudio, custo, blocos regerados).

## Loop de melhoria
1. **Avaliar:** liste a % por bloco; marque os < 93% e o motivo (tag falada, corte, palavra trocada).
2. **Corrigir:** até 2 rodadas: ajuste o texto do bloco no `roteiro.py` (ex.: juntar frase curta, trocar tag), rode `python3 roteiro.py` e regenere só os afetados via `blocos-refazer.json`. Resto = pendência no `ETAPA2.md`.
3. **Registrar:** comportamento novo do motor (tag que é lida, corte, velocidade) em `conhecimento/anti-padroes.md` e no `estilo.md` do canal, com **data e fonte** (bloco e vídeo); sem medição = **Hipótese**.
4. **Commitar:** `git add $V/ETAPA2.md $V/roteiro.py $V/blocos.json` (+ conhecimento; áudio fica fora do git) e
   `git commit -m "<canal>/<NNN>: voz Fish (B blocos, US$ X, Whisper min Y%)"`.
