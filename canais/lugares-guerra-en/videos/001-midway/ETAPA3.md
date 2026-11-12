# ETAPA 3 (montagem, render, QA, pacote): 001-midway — 12/11/2026

## Resultado
| Item | Valor |
|---|---|
| Vídeo | `out/video.mp4` 1920x1080 30 fps H.264 + AAC 192k, **16:57** (30.497 quadros) |
| Loudness | **−15,0 LUFS**, pico −2,6 dBFS (mix com loudnorm −15 + 1,2 dB no AAC) |
| Telas pretas ≥ 0,2 s | **0** (blackdetect) · silêncios > 1,5 s: 0 |
| Cortes no 1º min (scene > 0,3) | 11: muitos cortes são DocGrifo/zoom (sem troca brusca); o canal mede troca de tipo de tela |
| Whisper (ETAPA2) | média 98,7%, mín. 92,1% (falso alerta de normalização) |
| Pré-QA | 231 stills (1 por plano + fim de cada grifo), 10 grades no olho + `preqa_visual.py` 2 rodadas: 0 bloqueante; altos corrigidos |
| Custo da fase 2 | **US$ 1,55** (voz 0,23 · pré-QA API 0,97 · Runpod 0,36 incl. Pod órfão estimado) — teto US$ 6 |

## Montagem
- `tools/build.py`: voz aparada e encadeada (0,35/0,9/1,5 s), corte de cada plano na 1ª palavra do `em` pelo tempo do Whisper (−0,12 s), grifo sincronizado com a leitura da frase do documento, trechos de filme cortados em `public/clips/` (sem áudio, na velocidade, **todos < 7 s**, máx. 6,87 s, regra do Ford), imagens reduzidas em `public/img/`, mapas 2D projetados do Natural Earth 50m, trilha própria sintetizada (pad modal + piano raro, sem percussão) com ducking, SFX de papel/máquina só no grifo, `out/legendas.srt` pelas palavras do Whisper, `qa/capitulos.json`.
- `src/componentes.jsx`: KenBurns, Filme, DocGrifo (página → zoom → grifo; Ficha sai antes do zoom; região recortada quando a página tem foto de terceiro), Número, Mapa2D, Cartela SCHEMATIC, PerfilProfundidade, EntaoAgora, Card.
- **Sem crédito em tela** (Rodrigo, 12/11): Ficha com 1 linha (data · lugar ou pessoa); créditos completos só no `youtube.txt`. Regra gravada na `biblia/visual.md`.
- Mudanças de storyboard nesta etapa: fotos de Nimitz (NH 62674) e Cannon (USMC) entraram; Gay girado (a foto está de lado na ficha do NARA); Clipper sem a borda do scan; grifos da EO 199-A e do chumbo refinados; Número "PAGE ESTIMATE" → "JAPANESE LOSSES · NIMITZ'S ESTIMATE"; notas internas "(not Miniclier)/(Cannon not shown)" fora; P086/P087 trocados de trecho (caíam no fade para preto do filme).

## Render (o que quebrava no bloco 12)
- 1ª tentativa no Runpod: blocos 11/12 (≈ 11:00–13:00) morriam em ~40 s, sem log. Causa: **memória**. Os DocGrifo de capturas .gov de 3.840 px ampliam para elementos de ~7.000×5.200 px com `filter: contrast()` + `box-shadow` borrada: cada aba do Chrome rasteriza uma superfície de ~145 MB; com 8 abas o contêiner estourava e a sessão SSH morria junto (por isso sem mensagem). Na VPS o mesmo trecho + vídeos em **/tmp, que é tmpfs (RAM)**, levou ao OOM killer.
- Correção sem mudar o visual: contraste 1,06 "assado" nas imagens dos documentos (`*.c106.jpg`, mesma fórmula do CSS; SSIM 0,988–0,9999 contra as referências), sombra só quando a página cabe na tela, cache do OffthreadVideo limitado a 1 GB e concorrência 4 (`RFLAGS`, opção nova do `tools/render_runpod.sh`).
- Depois disso: Runpod 9450–15449, 15450–21599 e 21600–30496 sem falha (SSIM 480p mín. 0,970). Reaproveitados 0–9449 renderizados antes na VPS (contagem de quadros exata e SSIM ≥ 0,92 contra as referências, diferenças só de compressão em quadros com textura). Partes e junção em `~/render-midway/` (disco), nunca em /tmp.
- Incidente: um render ficou órfão quando o comando estourou o tempo da ferramenta; o Pod foi apagado pela API (custo estimado lançado). Renders longos agora como unidade `systemd-run --user`.

## Pacote (`out/`, fora do git)
Títulos A/B/C aprovados pelo Rodrigo, pareados com as thumbs A/B/C: A "Why Can't You Visit Midway Atoll?", B "What's Still Under the Water at Midway?", C "The Midway Report You Weren't Supposed to Read". `thumbnail.jpg` = A. Capítulos (20): 0:00 The page Nimitz stamped SECRET · 0:42 The island you can't land on · 1:09 The last man who was there · 2:07 A wire, a fleet and an airline · 3:09 The fake water message · 4:09 June 4, 1942 · 4:57 The director on the rooftop · 5:44 Torpedo Squadron Eight · 6:28 Five minutes · 7:16 Line (c) · 8:16 The base that stayed · 8:54 Executive Order 13022 · 9:46 The paint · 10:30 The money · 11:21 The hangar · 12:17 The tsunami · 12:49 Wisdom · 13:30 The strangest thing on Midway · 14:26 Three miles down · 15:24 So why can't you visit?

## Para o Rodrigo conferir
- 3:02 Cannon (foto nova) · 4:10 Nimitz no bunker (foto nova) · 6:21 George Gay (foto girada) · 6:40 porta-aviões no lugar dos SBDs "10:20".
- 9:40 "~300 VISITORS A YEAR (UNTIL 2012)" na tela sem estar na fala (fonte: audiência de 2014): manter ou tirar.
- 13:30 albatrozes filmados em 1942 sob frases no presente (decisão dele, da ETAPA1).
