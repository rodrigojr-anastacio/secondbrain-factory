---
name: qa
description: Use antes de entregar um vídeo da fábrica do YouTube ao Rodrigo (ou para auditar um já publicado) - roda o QA objetivo do render (qa.sh, contact sheet, blackdetect, loudness), compara voz × roteiro com Whisper, confere fidelidade das cenas nomeadas e pacote, e escreve QA.md com no máximo 2 rodadas de correção.
---

# qa: out/ completo → QA.md

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`.
Procedimento-base: checklist de `playbooks/produzir-video.md` §6 e §7. Modelo recomendado: **sonnet** (dentro da etapa `montagem-render`, ou etapa `qa`).

## Antes de agir
0. **Primeiro a bíblia do canal** (caixinha): `canais/<slug>/biblia/README.md` (canal-modelo e "o que NÃO fazer aqui") e **todos** os arquivos de `canais/<slug>/biblia/` (roteiro, título, thumb, visual, voz): é contra eles que o vídeo é julgado. A bíblia **prevalece** sobre `conhecimento/` (só regras gerais). Nunca aplique padrão de outro canal.
1. Regras gerais: todo `conhecimento/` (sobretudo `anti-padroes.md`).
2. Leia `canais/<slug>/canal.yaml`.
3. Leia `$V/BRIEF.md` (meta e critérios de pronto), `$V/ETAPA*.md` e o `QA.md` do vídeo anterior do canal (formato).
4. Ferramentas do vídeo: `$V/tools/qa.sh`, `$V/tools/transcrever.py`, `$V/tools/compara_voz.py` (copie de `canais/historia-ptbr/videos/002-india/tools/` se faltar).

## Passos
1. **Render:** `cd $V && bash tools/qa.sh | tee qa/qa.txt` (specs, `out/contact-sheet.jpg` de 20 frames, cortes no 1º min, telas pretas, loudness, silêncios).
2. **Voz × roteiro:** `cd $V && ~/workspace/fabrica-youtube/tools/.venv/bin/python tools/transcrever.py` (gera `qa/transcricao.json`) e depois `python3 tools/compara_voz.py` (gera `qa/voz_diff.txt`).
3. **Visual:** olhe só o `out/contact-sheet.jpg` e **1 frame de cada cena com nome próprio** (extraia com `ffmpeg -ss <t> -i out/video.mp4 -frames:v 1`, tempos em `src/timeline.json`), montados numa grade única. Nada de revisar frame a frame.
4. **Legenda:** 3 pontos (início, meio, fim) do `.srt` batem com a fala.
5. **Pacote:** valide `out/youtube.txt` e `out/thumbnail.jpg` pelos critérios da skill `pacote-youtube`.
6. **Segue a bíblia do canal?** (obrigatório) Confira o vídeo contra cada arquivo de `canais/<slug>/biblia/`:
   - **roteiro:** o checklist de `biblia/roteiro.md` item por item, lendo o `SCRIPT.md` (ex.: historia-ptbr = eras ligadas, nenhum capítulo-objeto, teste da troca; dossie-es = expedientes encadeados, hook ≤ 35 s);
     - **historia-ptbr: v2 vale a partir do 006; vídeos 001–005 seguem a v1 em `biblia/roteiro-v1.md`** (julgue o 005 e anteriores pela v1). Em vídeo ≥ 006, rode o checklist v2 com os tempos reais da legenda: `python3 ~/workspace/fabrica-youtube/canais/historia-ptbr/tools/checklist_roteiro_v2.py $V` (usa `out/legendas.srt`), cole a saída no `QA.md` e confira `biblia_versao='v2'` em `youtube.videos`. Item obrigatório reprovado = roteiro reprovado (volta à skill `roteiro`), exceto o ritmo 140–145 ppm, que é Hipótese: anote o desvio sem reprovar. Não vale para outros canais;
   - **título** na fórmula de `biblia/titulo.md`; **thumb** no template de `biblia/thumb.md`; **visual** (contact sheet) com a identidade de `biblia/visual.md`; **voz** = a de `biblia/voz.md`;
   - nada da lista "O que NÃO fazer aqui" do `biblia/README.md`. Qualquer item de outro canal = **reprovado**, volta para a skill culpada.
7. Escreva `$V/QA.md`: checklist marcado com números, problemas, correções feitas, pendências. Status: `UPDATE youtube.videos SET status='qa'` durante; `pronto` quando aprovado.

## Critérios de aprovação (objetivos)
- [ ] Duração = meta (± 30 s) e = N do título.
- [ ] 1080p30 H.264/AAC; ~-15 LUFS; pico < -1 dBTP; voz acima da trilha.
- [ ] 0 telas pretas ≥ 0,2 s; 0 silêncios > 1,5 s fora de capítulo; ≥ ~21 cortes no 1º minuto.
- [ ] Whisper × roteiro ≥ ~93% no total e sem bloco com frase faltando ou tag falada.
- [ ] Cenas nomeadas fiéis; nenhum lugar real no lugar de fictício; nenhum frame de filme; nada cortado/sobreposto; nenhum texto gerado pela IA; um HUD por vez.
- [ ] `.srt` sincronizada; capítulos em ordem desde 0:00; thumb JPG < 2 MB.
- [ ] **Segue a bíblia do canal** (roteiro, título, thumb, visual, voz) e nada de "O que NÃO fazer aqui"; resultado de cada arquivo anotado.
- [ ] Custo total ≤ teto: `psql -d vida -c "SELECT * FROM financas.custo_por_video WHERE id=<id>"`.

## Loop de melhoria
1. **Avaliar:** marque cada item com o número medido.
2. **Corrigir:** **no máximo 2 rodadas** (devolva à skill da etapa culpada: `voz`, `imagens`, `montagem-render`...). O que sobrar vai como pendência no `QA.md` e no relatório.
3. **Registrar:** erro de formato/estilo do canal vira entrada na **bíblia do canal** (`canais/<slug>/biblia/<arquivo>.md`); erro de ferramenta, processo ou custo (vale para todos) vai para `conhecimento/anti-padroes.md` (o que, quanto custou, como evitar). Sempre com **data e fonte** (`QA.md <canal>/<NNN>`); sem dado = **Hipótese**. Se mudar procedimento, ajuste o playbook.
4. **Commitar:** `git add $V/QA.md` (+ bíblia/conhecimento tocados) e
   `git commit -m "<canal>/<NNN>: QA aprovado (Whisper X%, -15 LUFS, 0 pretas)"` (ou "QA com N pendências").
