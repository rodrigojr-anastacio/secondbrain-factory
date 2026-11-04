# ETAPA 3: montagem, render, thumbs, pacote e QA · 003 Irã (youtube.videos id 5)

04/11/2026. QA aprovado (detalhes e pendências em `QA.md`). Entrega em `entrega/` (mp4, 3 thumbs, `pacote.md`, `legendas.srt`, `amostras-voz/`); mídia fora do git.

## Números
- **Duração 918,4 s = 15:18** (título "A história INTEIRA do Irã em 15 minutos"). 1920x1080, 30 fps, H.264 CRF 20 + AAC 192k, 262 MB.
- **Cortes:** 24 no 1º minuto (timeline), média 20,2/min; 309 planos (2,97 s em média).
- **Rótulos:** 143 (46%), 33 cartões de data, 17 placas de capítulo.
- **Loudness:** -15,1 LUFS, LRA 3,4, pico de amostra -4,4 dBFS. **Telas pretas 0, silêncios > 1,5 s: 0.**
- **Whisper × roteiro:** 95,4% no total, 0 tags faladas (`compara_voz.py` agora normaliza números e "a.C.").
- **Tempos:** build 33 s; render 24 min (27.552 frames, 2 vCPU); QA: qa.sh 1 min 8 s, transcrição 1 min 28 s.
- **Custo:** nenhum gasto pago nesta etapa. Total do vídeo (`financas.consumo`, ref_id 5): fal US$ 11,54 (R$ 67,55) + Fish US$ 0,38 (R$ 2,22) = **R$ 69,77** (teto R$ 80). `financas.custo_por_video` não tem linha para o id 5 (view vazia).

## Pacote (copiado de `out/youtube.txt`)
Título: **A história INTEIRA do Irã em 15 minutos**. Capítulos: 0:00 Introdução · 0:32 O Túnel · 1:35 O Nome · 2:05 O Cilindro · 2:58 O Cavalo · 3:49 As Colunas · 4:31 A Flecha · 5:04 A Rocha · 5:48 O Moinho · 6:32 O Poema · 7:57 A Água · 8:40 O Menino · 9:30 O Tabaco · 10:20 O Poço · 11:41 As Fitas · 13:08 O Lenço · 13:49 O Filho · 14:27 A Caravana.
Thumbs: A = `thumb-base` (fórmula do canal), B = guia espantado (Isfahan), C = Ciro; "IRÃ" em Libre Caslon 700 e selo de datas "4200 a.C. – 2026" em amarelo-ouro #F2B705 (Open Sans 800), tudo composto em `src/Thumbnail.jsx` (props `base`, `variante`).

## Problemas e improvisos
1. `tools/build.py` falhou na trilha (`ValueError: operands could not be broadcast`): o laço do dedilhado incrementava o passo depois da checagem e passava do fim do áudio. Corrigi com `break`.
2. O rótulo (NameTag) colidia com a placa de capítulo (still do frame 1075). Agora o rótulo espera a placa sair; os 3 stills de teste (data, capítulo + rótulo, rótulo longo) passaram.
3. O `qa.sh` conta 15 cortes no 1º minuto (detector de cena) contra 24 da timeline; o detector não vê reenquadramentos da mesma imagem. Usei a timeline como número oficial.
4. A thumb B saiu com o til do "Ã" colado no topo; reduzi o tamanho/posição e regerei.
5. O render roda em segundo plano (`nohup`), mas o turno só terminou depois dele (esperei com `tail --pid` em primeiro plano, sem encerrar antes).
6. A view `financas.custo_por_video` não mostra o id 5.

## Melhorias sugeridas
1. `qa.sh`: contar cortes pela `timeline.json` (ou por diferença de frames) em vez de `scene>0.3`; e mostrar o true peak (hoje só o pico de amostra).
2. `build.py` da esteira: o mesmo `break` na trilha; e o rótulo vs. placa de capítulo no `Video.jsx` modelo; `compara_voz.py` padrão com normalização de números.
3. Recarregar a OpenAI e regerar `thumb-base` em `high` antes de publicar; e registrar em `conhecimento/anti-padroes.md` o erro do rótulo e do build (não mexi em `conhecimento/` nesta etapa).
