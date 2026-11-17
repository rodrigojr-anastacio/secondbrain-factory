# ETAPA 2 PRONTA: Em Relevo 006, Caraguatatuba 1967 × São Sebastião 2023 (17/11/2026)

`youtube.videos` id 47 → `pronto`. **Duração 9:40 (580,5 s)**, 1920×1080 30 fps, AAC −14,8 LUFS (pico −1,3 dBFS, LRA 2,1), 0 telas pretas, 0 silêncios > 1,5 s. Só **1 corte brusco no 1º minuto** (o motor é de câmera contínua e peças que entram a cada 2–3 s; o `qa.sh` só conta cortes de cena). Entrega em `entrega/` (video.mp4 308 MB, legendas.srt, thumb-A/B/C.jpg, thumbnail.jpg = A, pacote/youtube.txt). Nada no Drive nem no YouTube.

**Promessa paga (legendas.srt):** frase-âncora "Não foi azar: a receita está no relevo." em **0:27,1–0:29,5** (≤ 0:30); "casca de terra de 1 a 2 metros e meio" em **0:52,4** (≤ 1:05); aba "3 · A CASCA DA SERRA" em 3:57 (≤ 4:30); Landsat antes × depois em 7:09–7:30 (≤ 7:30). A thumb A/B/C = T1/T2/T3 (UMA PAREDE? · UMA NOITE · sem texto), 3 padrões diferentes (mapa-lugar, antes-depois, cena-acao); registradas em `youtube.embalagem_variantes`.

## O que mudou em relação ao plano da etapa 1 (decisões do job)
1. **Voz = Fish #NATASHA drama-3 (reserva do `canal.yaml`), não ElevenLabs.** A chave `~/.segredos/elevenlabs/api_key` devolveu 401 "Invalid API key" em 17/11 00:40 (sem acesso à conta; **Rodrigo: conferir/renovar a chave**). Tags do v3 removidas; hook 1,36×, corpo 1,08× (`shared/gera_voz_fish.py`, `monta_audio_v2.py` com `VOZ=fish`). Whisper × roteiro 0,975. Custo US$ 0,096 (≈ 9,6 mil bytes a US$ 10/M, promo).
2. **b32 reescrito** (versão segura do brief, voz regravada só dele): "a carta do SGB… marca as encostas de alta suscetibilidade… e é ao pé delas que está a cidade". A carta do SGB (PDF 34 MB) **não foi convertida/mostrada** (sem pdftoppm/PyMuPDF e sem verificação da classificação); a tela mostra a declividade > 40% do SRTM com a legenda "BASE DA CARTA DO SGB, NÃO REPRODUZIDA". `roteiro.py`/`ROTEIRO.md` atualizados; detector de cópia reexecutado: 3/100.
3. **Motor 2D novo (`Longo6.jsx` + `Cenas6.jsx`), não o 3D do 005.** Mapa litoral norte A (satélite sintético: cor por altura + sombra do SRTM; **não é foto**) e B (editorial navy), câmera contínua, colunas de chuva, camadas (IMERG, declive, cicatrizes ilustrativas), blocos 3D cortados desenhados em SVG a partir do perfil real (`dados/perfis.json`, `blocos3d.json`, exagero 2,5× e selo ILUSTRATIVO), fotos grandes, carta de Olga Cruz, pluviômetros, esquema da casca, fases, lama, cards sóbrios, cortiça, final. Máscara terra/mar da NASA GIBS (o Terrarium tem ruído no mar). Cicatrizes e rios do mapa são esquemáticos (rios: só a linha do perfil do vale; sem OSM).
4. Fade-out final removido (o último quadro escuro reprovava no SSIM, 0,42, estável nas 2 GPUs).

## Render
Runpod, 6 partes de 3.000 quadros, SSIM 480p mín. 0,986; provas ≥ 0,9995; 17.414 quadros. Parte 5 perdeu 2 Pods sem SSH (≈ 16 min cada) até uma A4000 subir. Pods destruídos (API: 0). Custo ≈ US$ 0,10. Áudio: mix.wav inteiro com compressor + loudnorm, aplicado uma vez na junção.
**Custo total: ver `financas.custo_por_video` (voz 0,10 + 2 rodadas de pré-QA ≈ 0,54 + Runpod ≈ 0,10; teto 3).

## Pré-QA
97 stills a cada 6 s × 2 rodadas (`PREQA-visual.md`, última: 1 bloqueante = texto de tela sobre os rótulos do pluviômetro, corrigido e conferido em still; restam falsos positivos de valor animado/crossfade). Corrigido: câmera saindo da imagem (faixa navy), tags de b05 sem relação com a foto, rótulos sobre a legenda, painéis sobrepostos.

## Pendências / para o Rodrigo
- Chave ElevenLabs (401). Se quiser a Fernanda, regravar a voz e remontar (`mix6.py` + render).
- Carta do SGB não usada; termo de uso da carta de Olga Cruz (CC BY 4.0 declarado pela revista) como no brief.
- "Contagens da época… perto de 500" (b31) sem fonte primária oficial; origem da escarpa (b11) em resumos de Almeida & Carneiro.
- Mapa A é sintético (altura+sombra); blocos 3D, cicatrizes e fratura são ilustrativos (selo na tela).
- Thumb A: bloco com exagero ~4,2× (marcado ILUSTRATIVO); thumb C escurece o canto do galho.
