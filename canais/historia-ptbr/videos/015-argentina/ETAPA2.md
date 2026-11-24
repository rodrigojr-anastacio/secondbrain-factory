# ETAPA 2 · historia-ptbr/015 Argentina (youtube.videos id 56) · 23/11/2026

**Resultado:** `entrega/video.mp4` **17:03** (1023,4 s), 1080p30 H.264+AAC, **−15,2 LUFS**, pico −4,3 dBFS, **0 telas pretas**, 22 cortes no 1º minuto, 19,8 cortes/min (338 planos). 3 thumbs A/B/C (`entrega/thumb-*.jpg`, `thumbnail.jpg` = A), `entrega/legendas.srt`, `contact-sheet.jpg`, `pacote/youtube.txt`. Drive: não subido (a rotina noturna sobe). `youtube.videos` 56 = `pronto`; pares A/B/C em `youtube.embalagem_variantes`.

## Custo (financas.consumo, ref 56; teto US$ 8): ≈ US$ 7,12
Gemini (fallback) US$ 6,42 · Fish drama-3 US$ 0,15 (registrado a US$ 10/M; o crédito real cai a ~US$ 50/M, então o gasto real da voz é ~US$ 0,7: conferir o saldo Fish) · Anthropic (pré-QA) US$ 0,29 · Runpod US$ 0,26 · Codex US$ 0.

## Voz
64 blocos, 12.589 bytes. Whisper fonético mín **93,8%** (N054), média 99,1%; os ≤ 95% (N012 "Bêring", N054 "1º/4ª") são artefato do Whisper (números/ordinais), nenhuma tag falada. Hook: 4 tomadas, melhor combinação `daccbd` (repetição 0,08; tomadas únicas 0,14–0,20) instalada sobre N001–N006. Ouvir os nomes (Rosas, Urquiza, Bordabehere, Cobos, Milei: o Whisper ouviu "Ravier Milleille") antes de publicar: ninguém ouviu.

## Imagens
204/204. Codex 65 (I001–I080 aprox.) até a cota `imagegen` acabar na 80ª; o resto (124) + 3 bases de thumb pelo fallback **Gemini** (US$ 6,42 no total). Primeira rodada do fallback parou no `--teto 4` que eu passei (41 faltaram); refeita com `--teto 2.3`. Pranchas conferidas a olho (`qa/prancha0-3.jpg`): estilo do canal, sem letras, sem vazamento de Egito/turbante.

## Pré-QA
103 stills (a cada 10 s). `PREQA-visual.md`: bloqueante 0, alto 2 (Q22 3:30 e Q77 12:40: crossfade/fade de placa nos stills, falso positivo), médio 14, baixo 32. Médio de interesse: Q44 (7:10, 1899) com carro preto que lembra Ford T (anacronismo leve, não refeito).

## Render
Runpod, 4 partes (0–10199 4090; 10200–20399 3090; 20400–25499 3090; 25500–30700 L4), `render_partes.sh juntar`; SSIM 480p mín 0,993 na 1ª parte, 0 refeitos, Pods destruídos (0 na conta). Runpod ≈ US$ 0,26. Trilha: pad/violão sintetizado em Lá menor (herdou o código do 014 com notas trocadas).

## QA (6b/6c): timestamps na `legendas.srt`
- `SIMILARIDADE.md` 1/100; `CRIVO-ANGULO.md` APROVADO (r3); `CRIVO.md` APROVADO (r5). Roteiro não mudou.
- **Promessa paga:** frase-âncora "em vinte e dois anos, a Argentina trocou de dinheiro quatro vezes e apagou treze zeros" **0:22–0:29** (T1, T3, Thumb A/C) → "já esteve entre os mais ricos do mundo" **0:29** → pergunta central "quem pagou por esses treze zeros?" **0:36** → "quem paga a conta" **0:47** → "Quem fica com esse dinheiro, manda" **0:54** (T2). Tudo ≤ 1:00. IAPI/"Quem paga?" (Thumb B) em **9:35–10:05**; o 13º zero em 12:37; a pergunta volta em 16:24.
- Thumbs (`thumbs/compose.py`, bases sem letras, texto e cinta "1.000.000" no código; 3 padrões, cada uma = seu conceito; A=T1, B=T2, C=T3; `thumbs/prancha-celular.jpg`): A rosto-emoção "VALE NADA"; B conflito X×Y "QUEM PAGA?" + pílula 1946 (Obelisco inteiro, Sol de Maio visível, conta central; diferente da 016-B: fundos de lugar, texto pergunta, sem boina); C número-estatística "13 ZEROS".

## Pendências (não bloqueiam)
Ouvir os nomes; 22 cortes no 1º minuto (meta < 21); cota do Codex acabou cedo (Gemini cobriu 60% das imagens: ver custo); thumb B: o Sol de Maio ficou à esquerda no alto, sem tocar o produtor, mas legível; conferir lado a lado com 016-B no celular.
