---
name: pacote-youtube
description: Use quando o vídeo da fábrica do YouTube estiver renderizado para montar o pacote de publicação em out/ - youtube.txt com título, descrição (gancho + CTA), capítulos em ordem crescente desde 0:00, fontes, créditos, tags e categoria - e o lembrete do que o Rodrigo marca ao publicar.
---

# pacote-youtube: out/youtube.txt + checklist de publicação

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`.
Procedimento-base: `playbooks/produzir-video.md` §7. Modelo recomendado: **sonnet** (dentro da etapa `montagem-render`).

## Antes de agir
1. Leia `conhecimento/titulos.md` (fórmula, "INTEIRA" × "COMPLETA", N = duração) e `conhecimento/hooks.md`.
2. Leia `conhecimento/anti-padroes.md` e `conhecimento/roteiros.md` (capítulos fora de ordem já aconteceram).
3. Leia `canais/<slug>/canal.yaml` (idioma, fórmula de título) e `canais/<slug>/estilo.md`.
4. Leia `$V/BRIEF.md`, `$V/SOURCES.md`, `$V/qa/capitulos.json` (gerado pelo `build.py`) e `$V/out/legendas.srt`.
5. Modelo: `canais/historia-ptbr/videos/002-india/out/youtube.txt` (fora do git; leia se existir).

## Passos
1. Pegue a duração real: `ffprobe -v error -show_entries format=duration -of csv=p=0 $V/out/video.mp4`. O **N do título** é essa duração arredondada em minutos.
2. Escreva `$V/out/youtube.txt` com as seções:
   - **Título** (fórmula do canal; ≤ 100 caracteres) e 1–2 alternativas para teste.
   - **Descrição:** 2 linhas de gancho (não repetir o título), CTA de comentário (a pergunta do fecho do roteiro), capítulos, fontes resumidas de `SOURCES.md`, créditos de imagem/música, nota de voz sintética.
   - **Capítulos:** de `qa/capitulos.json`, formato `M:SS Título`, começando em `0:00`, em ordem crescente, ≥ 3 capítulos de ≥ 10 s; confira cada tempo pela legenda.
   - **Tags** (10–15, idioma do canal), **categoria** (Educação) e idioma do vídeo.
3. No fim do arquivo, o lembrete para o Rodrigo: idioma do vídeo; **"conteúdo alterado ou sintético" = sim**; "não é para crianças"; subir as 3 thumbs no "Testar e comparar"; usar o mp4 1080p (nunca o do Telegram).
4. Copie também o essencial (título e capítulos) para `$V/ETAPA3.md`, porque `out/` fica fora do git.

## Critérios de pronto (avaliar)
Valide com um one-liner Python sobre `out/youtube.txt`:
- Capítulos em ordem estritamente crescente, o primeiro `0:00`, o último < duração.
- N do título = duração arredondada (± 1 min).
- Título ≤ 100 caracteres; descrição com CTA e nota de voz sintética; fontes presentes.
- Arquivos do pacote presentes: `out/video.mp4`, `out/thumbnail.jpg` (< 2 MB), `out/legendas.srt`, `out/youtube.txt`.

## Loop de melhoria
1. **Avaliar:** rode a validação e o checklist acima.
2. **Corrigir:** até 2 rodadas; resto = pendência no `ETAPA3.md`.
3. **Registrar:** fórmula de título/descrição nova em `conhecimento/titulos.md` como **Hipótese** (o Métricas confirma com views/CTR depois), com **data e fonte**.
4. **Commitar:** `git add $V/ETAPA3.md` (+ conhecimento; `out/` não vai ao git) e
   `git commit -m "<canal>/<NNN>: pacote YouTube (título, N capítulos)"`.
5. Status: `psql -d vida -c "UPDATE youtube.videos SET status='pronto', titulo='<título final>', atualizado_em=now() WHERE id=<id>"` (só depois do QA aprovado). **A publicação é sempre do Rodrigo.**
