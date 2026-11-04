---
name: thumbnail
description: Use para criar a thumbnail de um vídeo da fábrica do YouTube (ou analisar thumbs de referência) - ilustração-base em high, texto composto no código (src/Thumbnail.jsx no Remotion), 3 variações para o "Testar e comparar" e out/thumbnail.jpg com menos de 2 MB.
---

# thumbnail: base high + texto no código → out/thumbnail.jpg + 3 variações

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`. Python: `tools/.venv/bin/python`.
Procedimento-base: `playbooks/produzir-video.md` §7. Modelo recomendado: **sonnet** (etapa `thumbnail`, normalmente dentro de `producao` + `montagem-render`).

## Antes de agir
1. Leia `conhecimento/thumbnails/README.md` (regras, CTR medido, thumbs no ar) e veja as thumbs em `conhecimento/thumbnails/*.jpg` do mesmo canal.
2. Leia `conhecimento/titulos.md` e `conhecimento/anti-padroes.md`.
3. Leia `canais/<slug>/estilo.md` (fontes, identidade) e o bloco `visual` do `canal.yaml`.
4. Leia `$V/BRIEF.md` (título, teto) e a thumb da referência (`pesquisa/tendencias/assets/<data>/<id>/thumb.jpg`, se houver).
5. Modelo: `canais/historia-ptbr/videos/002-india/src/Thumbnail.jsx` e `thumb-variacoes.json`.

## Passos
1. **Base:** escreva 1–3 cenas de thumb num json no formato de `cenas.json` (ex.: `$V/thumb-cenas.json`, prompt do lugar reconhecível, área livre para o texto, sem texto) e gere em `high`:
   `tools/.venv/bin/python tools/img_openai.py <slug> $V/thumb-cenas.json $V/thumb-var --video <id> --qualidade high` (~US$ 0,22 cada; confira `financas.saldo_pre_pago` antes).
2. **Texto no código:** ajuste `src/Thumbnail.jsx` (nome do lugar enorme, 2–3 palavras; selo curto) e renderize um still por variação:
   `export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH; cd $V && npx remotion still src/index.jsx Thumbnail thumb-var/final/v1.png` (props/variações como no `thumb-variacoes.json` do 002).
3. Converta para JPG < 2 MB: `ffmpeg -y -i thumb-var/final/v1.png -q:v 3 thumb-var/final/v1.jpg`. Escolha a principal e copie para `out/thumbnail.jpg`.
4. Para Tendências (análise de referência): descreva o padrão (lugar, texto, contraste, cor) e registre em `conhecimento/thumbnails/README.md` como **Hipótese** até haver CTR.

## Critérios de pronto (avaliar)
- Gere uma prévia em 320x180 (`ffmpeg -i v1.jpg -vf scale=320:180 prev.jpg`) e olhe: o nome lê no tamanho de celular? (2–3 palavras na arte).
- O lugar é reconhecível e **fiel** ao tema (nada de lugar real no lugar de fictício; nada de pintura que não representa o lugar).
- Nenhum texto escrito pela IA na base.
- 3 variações em `thumb-var/final/` e `out/thumbnail.jpg` em JPG, 1280x720, < 2 MB.
- Custo registrado (`--video <id>`) e dentro do teto.

## Loop de melhoria
1. **Avaliar:** confira cada critério na prévia 320x180 (uma imagem com as 3 lado a lado via `ffmpeg ... hstack`).
2. **Corrigir:** até 2 rodadas (texto maior, recorte, nova base). Resto = pendência no `ETAPA3.md`.
3. **Registrar:** o padrão usado e o porquê em `conhecimento/thumbnails/README.md` como **Hipótese** (o CTR vem depois, pelo Métricas: o Rodrigo lê no Studio). Ao publicar, copie (`cp`) a thumb no ar para `conhecimento/thumbnails/<canal>-<video>.jpg` (< 500 KB).
4. **Commitar:** `git add $V/src/Thumbnail.jsx $V/thumb-variacoes.json $V/thumb-cenas.json conhecimento/thumbnails/README.md` e
   `git commit -m "<canal>/<NNN>: thumbnail (3 variações, base high)"`.
