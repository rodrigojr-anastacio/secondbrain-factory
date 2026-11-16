# Render do piloto clima pt (08/11/2026)

## Medidas (VPS 2 vCPU, WebGL por software `--gl=swangle`, `--concurrency=2`, 1080p, 30 fps)
| Parte | Quadros | Shorts 1080×1920 | Longo 1920×1080 |
|---|---|---|---|
| 0 | 0–599 | 397 s | 387 s |
| 1 | 600–1199 | 367 s | 354 s |
| 2 | 1200–1774 | 334 s | 341 s |
| **Total** | 1.775 | **18 min 18 s** | **18 min 02 s** |
- **~0,61 s por quadro** em média: 0,66 na parte 0 (planos fechados com polaroid de vídeo) e 0,58 no resto. É **~45% mais rápido** que o teste lotr-fr (1,1 s/quadro).
- **Projeção para um vídeo de 12 min** (21.600 quadros): **~3 h 40 min** de render, em 36 partes de 600 quadros (~6 min cada), um render por vez.
- Arquivos: 42 MB cada (CRF 18).

## O que deixou mais leve sem perder o visual
- Mapa **extrudado da malha do IBGE** (ExtrudeGeometry, sem bisel) no lugar do terreno procedural de 127 mil vértices do teste lotr.
- Sombra **1024** com `PCFShadowMap` (no lotr: 2048 + PCFSoft).
- Divisas municipais como `LineSegments` de 1 px (20 mil pontos, custo desprezível).
- Camadas 2D (número, legenda, polaroid, caixinhas, manchete) em React por cima do canvas.
- Trechos reais pré-recortados em 960×720 a 30 fps, mudos (`OffthreadVideo` só decodifica o necessário).
- Render `--muted`. O áudio (narração + SFX sintetizados + loudnorm) entra no `ffmpeg` da junção.
- **Próximo ganho (Hipótese, não medido):** renderizar o canvas 3D a 0,75× e escalar, ou trocar o fundo para a mesa sem `fog`.

## Como refazer
```
cd pesquisa/canal-clima-2026-11/piloto-pt
# dados (grátis): malhas IBGE em dados/ (no git) + Natural Earth 50 m (dados/ne110.json, fora do git: baixar de
# raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson) → shared/geo.json
python3 shared/prep_geo.py
# voz Kokoro (grátis) + junção com pausas + alinhamento Whisper
~/tts/venv-kokoro/bin/python shared/gera_voz.py pf_dora 1.1 work/voz
~/tts/venv-kokoro/bin/python shared/monta_audio.py 1.05      # → audio/narracao.wav + shared/tempos.json
~/workspace/fabrica-youtube/tools/.venv/bin/python shared/alinha.py   # → shared/whisper.json (faster-whisper)
python3 shared/build_cues.py                                   # → shared/cues.json (fonte única das duas Compositions)
~/tts/venv-kokoro/bin/python shared/mix_audio.py               # → audio/mix.wav (narração + SFX + drone)
shared/cortar_clipes.sh                                        # trechos reais (dl/ via yt-dlp + WARP) → remotion/public/clips
cd remotion && cp -al ../../../../canais/lotr-fr/testes/motion-3d/remotion/node_modules . # ou npm install
ln -f ../audio/narracao.wav public/ && cp ../../../../canais/lotr-fr/testes/motion-3d/shared/fonts/*.ttf public/fonts/  # + PlayfairDisplay-Italic
cd .. && shared/render.sh Shorts out/shorts.mp4 && shared/render.sh Longo out/longo-amostra.mp4
# capa: npx remotion still Capa ../out/capa.jpg --frame=705 --gl=swangle
```
- Compositions em `remotion/src/Root.jsx`: `Shorts` (vertical, deixa ~15% livres embaixo e à direita para a UI), `Longo` (16:9: polaroid na lateral direita, caixinhas em linha, barra de fontes centralizada) e `Capa`.
- `shared/render.sh <Comp> <saida> [0|1|2|junta]`: renderiza uma parte por vez (espera `pgrep -af "^node .*remotion (render|still)"` ficar vazio) e registra o tempo em `work/render-tempos.txt`.
- Para trocar um trecho real, basta renderizar a parte afetada (0 = 0–20 s; 1 = 20–40 s; 2 = 40–59 s) e rodar `junta`.
