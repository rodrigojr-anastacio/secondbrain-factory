---
name: thumbnail
description: Use para criar as thumbnails de um vídeo da fábrica do YouTube (ou analisar thumbs de referência) - 3 thumbs A/B/C, uma por conceito aprovado no EMBALAGEM.md (3 padrões visuais diferentes, desde 16/11/2026), ilustração-base por conceito, texto composto no código (src/Thumbnail.jsx no Remotion), para o "Testar e comparar", e out/thumbnail.jpg com menos de 2 MB.
---

# thumbnail: 3 conceitos → 3 bases → texto no código → thumb-A/B/C + out/thumbnail.jpg

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`. Python: `tools/.venv/bin/python`.
Procedimento-base: `playbooks/produzir-video.md` §7. Modelo recomendado: **sonnet** (etapa `thumbnail`, normalmente dentro de `producao` + `montagem-render`).

## Antes de agir
0. **Primeiro a bíblia do canal** (caixinha): `canais/<slug>/biblia/README.md` (canal-modelo e "o que NÃO fazer aqui") e `biblia/thumb.md` (template do canal, CTR medido, thumbs no ar) e `biblia/titulo.md`. A bíblia **prevalece** sobre `conhecimento/` (só regras gerais). Nunca aplique padrão de outro canal.
1. Veja as thumbs no ar **do mesmo canal** em `conhecimento/thumbnails/<slug>-*.jpg` (a galeria; a análise está na bíblia).
2. Regras gerais: `conhecimento/thumbnails/README.md` e `conhecimento/anti-padroes.md`.
3. Leia o bloco `visual` do `canal.yaml`.
4. **Leia `$V/EMBALAGEM.md` (seções Pares A/B/C e Thumb A, B, C), `$V/embalagem/variantes.json` e `$V/CRIVO.md`**: desde 16/11/2026 (Rodrigo) são **3 thumbs realmente diferentes**, uma por conceito aprovado no crivo, cada uma de um padrão visual (`padrao_thumb`): composição, elemento dominante e tipo de texto distintos, pareadas a T1/T2/T3. Não invente conceito novo e **não** faça 3 variações do mesmo (o erro de antes: Em Relevo seca 1877, 3× mapa escuro + número). Vídeo antigo com só 1 conceito no `EMBALAGEM.md` (antes de 16/11): 3 variações dele, como era.
4b. Leia `$V/BRIEF.md` (teto) e a thumb da referência (`pesquisa/tendencias/assets/<data>/<id>/thumb.jpg`, se houver).
5. Modelo: o `src/Thumbnail.jsx` do **vídeo anterior do mesmo canal** (nunca o template de outro canal).

## Passos
1. **Bases (1 por conceito):** escreva `$V/thumb-cenas.json` (formato de `cenas.json`) com **3 cenas, `thumb-A`, `thumb-B`, `thumb-C`**, cada uma com o **seu** prompt e composição tirados da seção "Thumb A/B/C" do `EMBALAGEM.md` (elemento dominante, enquadramento, fundo e cores da bíblia, área livre para o texto, **sem texto** na imagem). Nada de reaproveitar a mesma base com outro corte: são 3 imagens de padrões diferentes. Conceito sem IA (Em Relevo: mapa/satélite/foto real com licença; `numero-estatistica` em fundo do canal; `documento-evidencia` de acervo) não gasta geração: monte no `Thumbnail.jsx` com o material.
   - **Gerador = o do `canal.yaml`** (`visual.gerador`) e confira `financas.saldo_pre_pago` antes:
     - `codex` (`historia-ptbr` desde 14/11/2026; `dossie-es` desde 23/11/2026, teste no MKUltra): US$ 0, fallback automático do `visual.gerador_fallback` (`gemini` nos dois desde 23/11/2026, `tools/img_gemini.py`, ~US$ 0,05/base; aceita `--tamanho`): `tools/.venv/bin/python tools/img_codex.py <slug> $V/thumb-cenas.json $V/thumb-var --video <id> --paralelo 3 --tamanho 1536x864` (base maior que 1280×720 para o recorte do `Thumbnail.jsx`; qualidade fixa). Pode gerar até 2 bases por conceito e escolher.
     - demais: `tools/.venv/bin/python tools/img_openai.py <slug> $V/thumb-cenas.json $V/thumb-var --video <id> --qualidade high` (~US$ 0,22 cada) ou `img_fal.py` com o modelo do canal, **1 base por conceito**.
   - **Teto (16/11/2026):** custo extra máximo por vídeo = o de **2 ilustrações-base a mais** do que a thumb única de antes (ou seja, 3 bases pagas no total; refação só dentro do teto do `BRIEF.md`).
2. **Texto no código:** ajuste `src/Thumbnail.jsx` no template da `biblia/thumb.md` (fontes e cores do canal) para aceitar as 3 composições (prop `variante: "A"|"B"|"C"` com base, texto e posição de cada conceito; tipo de texto diferente em cada uma, como aprovado) e renderize um still por thumb:
   `export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH; cd $V && npx remotion still src/index.jsx Thumbnail thumb-var/final/A.png --props='{"variante":"A"}'` (idem B, C; props em `thumb-variacoes.json`).
3. Converta para JPG < 2 MB: `ffmpeg -y -i thumb-var/final/A.png -q:v 3 thumb-var/final/A.jpg` (idem B, C) e copie para `entrega/thumb-A.jpg`, `thumb-B.jpg`, `thumb-C.jpg`. A principal (`out/thumbnail.jpg`, `entrega/thumbnail.jpg`) = a do padrão que lidera o placar do canal (`tools/.venv/bin/python tools/rotinas/embalagem_variantes.py placar --canal <slug>`), ou A se não houver resultado ainda.
4. Atualize `$V/embalagem/variantes.json` com `"thumb_arquivo": "entrega/thumb-<letra>.jpg"` (o `pacote-youtube` regrava no banco).
5. Para Tendências (análise de referência): descreva o padrão (eixo do vocabulário, lugar, texto, contraste, cor) e registre na `biblia/thumb.md` do canal que usa esse formato, como **Hipótese** até haver CTR.

## Critérios de pronto (avaliar)
- Gere uma prévia em 320x180 das 3 lado a lado (`ffmpeg -i A.jpg -i B.jpg -i C.jpg -filter_complex "[0]scale=320:180[a];[1]scale=320:180[b];[2]scale=320:180[c];[a][b][c]hstack=3" prev-abc.jpg`) e olhe: cada texto lê no celular? **As 3 parecem 3 vídeos diferentes** (composição, elemento dominante, tipo de texto)? Se duas parecem variações uma da outra, refaça a que se afastou do conceito.
- **Cada thumb bate com o seu conceito do `EMBALAGEM.md`** (Thumb A/B/C: composição, foco, texto, padrão); se a arte obrigou a mudar algo, registre em `ETAPA*.md` o quê e por quê (sem fundir dois conceitos no mesmo padrão).
- Segue o template da `biblia/thumb.md` e nada da lista "O que NÃO fazer aqui" (ex.: nada de pôster de expediente no historia-ptbr).
- O lugar é reconhecível e **fiel** ao tema (nada de lugar real no lugar de fictício; nada de pintura que não representa o lugar).
- Nenhum texto escrito pela IA na base.
- `thumb-var/final/A/B/C.jpg`, `entrega/thumb-A/B/C.jpg` e `out/thumbnail.jpg` em JPG, 1280x720, < 2 MB; `embalagem/variantes.json` com `thumb_arquivo`.
- Custo registrado (`--video <id>`), dentro do teto do vídeo e no máx. 2 bases pagas a mais que a thumb única de antes.

## Loop de melhoria
1. **Avaliar:** confira cada critério na prévia 320x180 (`prev-abc.jpg`, as 3 lado a lado).
2. **Corrigir:** até 2 rodadas (texto maior, recorte, nova base). Resto = pendência no `ETAPA3.md`.
3. **Registrar:** os 3 padrões usados (eixos) e o porquê em **`canais/<slug>/biblia/thumb.md`** como **Hipótese**; o vencedor do "Testar e comparar" entra em `youtube.embalagem_variantes` (Métricas) (o CTR vem depois, pelo Métricas: o Rodrigo lê no Studio). Ao publicar, copie (`cp`) a thumb no ar para a galeria `conhecimento/thumbnails/<canal>-<video>.jpg` (< 500 KB) e ponha a linha na tabela do `conhecimento/thumbnails/README.md`.
4. **Commitar:** `git add $V/src/Thumbnail.jsx $V/thumb-variacoes.json $V/thumb-cenas.json canais/<slug>/biblia/thumb.md` e
   `git commit -m "<canal>/<NNN>: thumbs A/B/C (<eixoA>/<eixoB>/<eixoC>)"`.
