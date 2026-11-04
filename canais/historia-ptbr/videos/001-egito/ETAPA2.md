# Etapa 2: voz, imagens, montagem, render e pacote

**Título final:** A HISTÓRIA COMPLETA do Egito em 16 minutos · `youtube.videos` id 3 → `status='pronto'`, `duracao_s=955`

| Item | Valor |
|---|---|
| Duração | 954,5 s (15:54) |
| Imagens únicas | **205** = 204 no vídeo + `thumb-base` (medium) |
| Planos | 294 (média de 3,25 s); 90 reusos (30,6% no total, 38,5% depois dos 3 min, 0% antes) |
| Custo (financas.consumo, ref_id=3) | **OpenAI US$ 1,46** (R$ 8,49) · **Fish Audio US$ 0,20** (R$ 1,17) · total direto R$ 9,66; com rateio do fixo, `custo_por_video` = R$ 30,39 |

## O que foi feito
1. **Roteiro (decisões do manager):** 85 `[break]` removidos (ficaram 15, nas viradas fortes), `[long-break]` e `[emphasis]` mantidos. +25 imagens no `roteiro.py` (dict `EXTRA`, nos blocos com mais reuso depois dos 3 min). Datas do GEM (1º/11/2025) e da GERD (9/9/2025) confirmadas na Wikipedia; o texto ficou com o ano, e o SOURCES.md foi atualizado. `.tmp/` apagada.
2. **Voz:** Fish s2.1-pro, 106 blocos. `tools/build.py` apara o silêncio de cada bloco, encadeia (0,16 s entre blocos, 0,5 s antes de capítulo) e reescala os planos de cada bloco pela duração real.
3. **Imagens:** gpt-image-2 low (thumb em medium), sem nenhuma regeração.
4. **Remotion** (`src/`): Ken Burns ou pan por enquadramento do storyboard; corte seco dentro do bloco e crossfade de 5 frames entre blocos; cartões de data, placas de capítulo e rótulos de mapa (`src/labels.jsx`) em Libre Caslon; sem legenda. Trilha original sintetizada no código (pad em escala hijaz, drone e dedilhado Karplus-Strong), com ducking, e mix final em -15 LUFS.
5. **Render:** `tools/render.sh` (concurrency 2, ~20 min, mais o 2-pass da versão Telegram). QA em `QA.md`.
6. **Pacote:** `out/video.mp4`, `out/video-telegram.mp4`, `out/thumbnail.jpg`, `out/legendas.srt`, `out/youtube.txt`, `out/contact-sheet.jpg`.

Para refazer: `python3 roteiro.py` → `…/tools/.venv/bin/python tools/build.py` → `tools/render.sh` → `tools/qa.sh`.

## Pendências
- **Publicação (Rodrigo):** idioma pt-BR, "conteúdo alterado ou sintético" = sim, "não é para crianças". Suba o `video.mp4`, nunca a versão do Telegram.
- Custo da 1ª leva de imagens (165) é **estimado**: a execução foi interrompida pelo limite de tempo antes de gravar o custo; lancei 165 × o custo médio da 2ª leva (US$ 0,0069/imagem). Confira no painel da OpenAI, se quiser precisão.
- Anacronismos menores de bandeira em 2 imagens (1922 e 1952); veja o QA.md. Se incomodar, são 2 regerações de ~US$ 0,01.
