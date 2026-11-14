---
name: pacote-youtube
description: Use quando o vídeo da fábrica do YouTube estiver renderizado para montar o pacote de publicação em out/ - youtube.txt com título, descrição (gancho + CTA), capítulos em ordem crescente desde 0:00, fontes, créditos, tags e categoria - e o lembrete do que o Rodrigo marca ao publicar.
---

# pacote-youtube: out/youtube.txt + checklist de publicação

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`.
Procedimento-base: `playbooks/produzir-video.md` §7. Modelo recomendado: **sonnet** (dentro da etapa `montagem-render`).

## Antes de agir
0. **Primeiro a bíblia do canal** (caixinha): `canais/<slug>/biblia/README.md` (canal-modelo e "o que NÃO fazer aqui") e `biblia/titulo.md` (fórmula do título do canal, título B, nota da descrição). A bíblia **prevalece** sobre `conhecimento/` (só regras gerais). Nunca aplique padrão de outro canal.
1. Regras gerais: `conhecimento/titulos.md` (N = duração) e `conhecimento/roteiros.md` (capítulos fora de ordem já aconteceram).
2. Leia `conhecimento/anti-padroes.md`.
3. Leia `canais/<slug>/canal.yaml` (idioma).
4. Leia `$V/BRIEF.md`, `$V/SOURCES.md`, `$V/qa/capitulos.json` (gerado pelo `build.py`) e `$V/out/legendas.srt`.
5. Modelo: o `out/youtube.txt` do **vídeo anterior do mesmo canal** (fora do git; leia se existir).

## Passos
1. Pegue a duração real: `ffprobe -v error -show_entries format=duration -of csv=p=0 $V/out/video.mp4`. O **N do título** é essa duração arredondada em minutos.
2. Escreva `$V/out/youtube.txt` com as seções:
   - **Título** (fórmula da `biblia/titulo.md`; ≤ 100 caracteres) e 2 alternativas com gatilhos diferentes, **dentro da mesma fórmula** (3 títulos para o "Testar e comparar").
   - **Descrição:** 2 linhas de gancho (não repetir o título), CTA de comentário (a pergunta do fecho do roteiro), capítulos, fontes resumidas de `SOURCES.md`, créditos de imagem/música, nota de voz sintética.
   - **Capítulos:** de `qa/capitulos.json`, formato `M:SS Título`, começando em `0:00`, em ordem crescente, ≥ 3 capítulos de ≥ 10 s; confira cada tempo pela legenda.
   - **Tags** (10–15, idioma do canal), **categoria** (Educação) e idioma do vídeo.
3. No fim do arquivo, o lembrete para o Rodrigo: idioma do vídeo; **"conteúdo alterado ou sintético" = sim**; "não é para crianças"; subir as 3 thumbs e os **3 títulos com gatilhos diferentes** (ver `conhecimento/titulos.md`, regra de 12/11) no "Testar e comparar"; usar o mp4 1080p (nunca o do Telegram).
4. Copie também o essencial (título e capítulos) para `$V/ETAPA3.md`, porque `out/` fica fora do git.
5. **Entrega final no Google Drive do Rodrigo** (não no Mac): monte `entrega/` e rode `tools/entregar_drive.sh <canal_slug> <NNN-slug>` → `Youtube/<nome do canal>/<NNN-slug>/` (nome vem do `canal.yaml`; só copia, nunca apaga). Logos/capas: `tools/entregar_drive.sh <canal_slug> identidade`. Usa rclone (remote `gdrive`); se faltar, veja `BLOQUEIO-drive.md`. O conector claude.ai Drive só serve para arquivos de texto pequenos (binário passaria pelo contexto do modelo).

## Critérios de pronto (avaliar)
Valide com um one-liner Python sobre `out/youtube.txt`:
- Capítulos em ordem estritamente crescente, o primeiro `0:00`, o último < duração.
- N do título = duração arredondada (± 1 min); título na fórmula da bíblia do canal e no idioma do canal.
- Título ≤ 100 caracteres; descrição com CTA e nota de voz sintética; fontes presentes.
- Arquivos do pacote presentes: `out/video.mp4`, `out/thumbnail.jpg` (< 2 MB), `out/legendas.srt`, `out/youtube.txt`.

## Loop de melhoria
1. **Avaliar:** rode a validação e o checklist acima.
2. **Corrigir:** até 2 rodadas; resto = pendência no `ETAPA3.md`.
3. **Registrar:** fórmula de título/descrição nova em **`canais/<slug>/biblia/titulo.md`** como **Hipótese** (o Métricas confirma com views/CTR depois), com **data e fonte**.
4. **Commitar:** `git add $V/ETAPA3.md` (+ conhecimento; `out/` não vai ao git) e
   `git commit -m "<canal>/<NNN>: pacote YouTube (título, N capítulos)"`.
5. Status: `psql -d vida -c "UPDATE youtube.videos SET status='pronto', titulo='<título final>', atualizado_em=now() WHERE id=<id>"` (só depois do QA aprovado). **A publicação é sempre do Rodrigo.**
