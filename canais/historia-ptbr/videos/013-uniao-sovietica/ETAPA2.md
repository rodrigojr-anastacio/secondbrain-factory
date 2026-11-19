# ETAPA 2 · historia-ptbr/013 União Soviética (youtube.videos id 50) · 18–19/11/2026

**Resultado:** `entrega/video.mp4` **15:40** (939,65 s), 1080p30 H.264 + AAC, **−15,4 LUFS**, pico −4,3 dBFS, **0 telas pretas**, 0 silêncios > 1,5 s, 18 cortes detectados no 1º minuto (o storyboard planeja 23; o detector não vê troca entre imagens parecidas), 20,1 planos/min. 3 thumbs + `pacote/youtube.txt`. Drive: não subido (a rotina noturna sobe a partir de `entrega/`). Pode ir ao ar: dom ou seg.

## Custo (financas.consumo, ref_id 50; teto US$ 8): ≈ US$ 1,22
Runpod US$ 0,81 (16 partes de 1.800 quadros; 2 tentativas perdidas por timeout do comando durante o upload do bundle, Pod destruído nas duas) · Fish drama-3 US$ 0,14 (72 blocos + 3 tomadas extras do hook) · pré-QA Anthropic US$ 0,27 · Codex US$ 0 (199 + 17 refeitas + 3 bases de thumb, 0 fallback fal; cota 5 h 10%, semana 28%).

## Voz
Whisper bruto mín 85,2% (nomes/números); **fonético mín 95,3%, média 99,5%**; nenhuma tag falada. Hook: 4 tomadas, melhor combinação `aaaccb` (repetição 0,13 × 0,17 da tomada única). Nenhum mp3 de 0 byte. Ouvir os nomes antes de publicar (ninguém ouviu): Iéltsin, Kossíguin, Gorbatchóv, Novotcherkásk, Riazã, Larionóv, Húver, avóska.

## Imagens: 199, todas pelo Codex
Prancha em 8 grades: vazamento das refs do Egito/Índia (turbante, faraó, palmeira, deserto) nas cenas simbólicas sem sufixo anti-vazamento: I013, I034, I053, I062, I063, I076, I077, I091, I097, I133, I147, I156, I157, I162, I164, I171, I188 refeitas com sufixo `NO turbans/pharaoh/palm…` e cenário russo (aplicado direto em `cenas.json`; originais em `qa/rejeitadas/`). Refeitas conferidas na prancha `qa/pranchas/refeitas.jpg`; I076/I097/I164 ainda mostram uma bandeirinha vermelha pequena ao fundo (aceito; não é foice e martelo). A I180 (lanchonete) tem toldo listrado vermelho/amarelo sem logotipo nem arcos. "2 + 2 = 5" (I073/I074) saiu certo pelo Codex, sem composição no código.

## Pré-QA (120 stills de 10 s + cartões e capítulos; 131 quadros)
Bloqueante 0, alto 3, médio 24, baixo 33. Os 3 "altos" são aceitos: Q39 (São Basílio ao fundo de vila em Moscou, plausível), Q80 (cena de 1972 com silos e locomotiva americanos: é o trigo dos EUA, intencional), Q106 (Torre de TV de Berlim em cena de 1990: já existia desde 1969).

## Render
Runpod em 16 partes (0–1799 … 27000–28189), todas com quadros = esperado e SSIM aprovada; concat + `mix.wav` AAC 192k. ffprobe: 28.187 quadros lidos × 28.190 esperados (3 quadros, 0,1 s, na junção, sem efeito visível). Armadilha repetida: o upload do bundle ao Pod às vezes passa de 5 min e o timeout de 560 s do comando mata a parte; basta repetir (Pod é destruído). Trilha: cordas dedilhadas tipo balalaika + pad em Ré menor (caps. 1–7) e sintetizador frio de serras desafinadas (caps. 8–10 e fecho).

## QA (6b/6c): timestamps conferidos na `legendas.srt`
- Detector de cópia **2/100** (`SIMILARIDADE.md`); `CRIVO-ANGULO.md` APROVADO (r3); `CRIVO.md` APROVADO (r3). Roteiro não mudou na etapa 2 (detector não repetido).
- **Promessa paga:** frase-âncora "De manhã, o controle de missão da NASA… À tarde, um supermercado… nem o Politburo tem essa escolha" **0:10–0:21** (T1, Thumb A); "cerca de trinta mil pessoas enfrentam a fila de uma lanchonete americana" **0:24** (Thumb C); "o país do Sputnik comprava trigo do exterior desde sessenta e três" **0:34** (T3); pergunta central "como o país que chegou primeiro ao espaço não conseguia encher uma prateleira?" **0:42**; "Essa é a história inteira da União Soviética" **0:48**; "E ela começa com uma promessa de pão" **0:51** (T2); avoska **4:56** (Thumb B; volta em 11:04 e 14:30); trigo do Canadá em 1963 **9:28**; Praça Púchkin **13:18–13:24**; fecho a partir de **14:59**.
- **Thumbs** (`thumbs/compose.py`; bases Codex sem letras, texto e pílula no código): A `rosto-emocao` Iéltsin pasmo no supermercado, "NEM O POLITBURO" + "1989"; B `objeto-simbolo` avoska vazia à direita, "VAI QUE…" à esquerda; C `numero-estatistica` "30 MIL / NA FILA" + fila na neve de Moscou. As 3 leem a 320×180 (`thumbs/prancha-celular.jpg`) e são 3 padrões diferentes. A = T1, B = T2, C = T3; pares gravados em `youtube.embalagem_variantes`. Observação do crivo r3 (testar "30 MIL" × "30.000"): ficou "30 MIL", 3 palavras, legível. Na base da C aparece a Catedral de São Basílio/Kremlin ao fundo (com as torres do Kremlin; sem bandeira nem foice e martelo); B é o 3º objeto-símbolo seguido no canal (acompanhar no placar).

## Pendências (não bloqueiam)
N002 "À tarde" (ordem JSC → Randalls; horário não está na fonte), N059 (Sukhanov de segunda mão), N066 e N069 (datas 02/04/1991 e 02/01/1992 não conferidas no QA). Ouvir os nomes. Nenhum ajuste de bíblia necessário além da lição abaixo.

## Lição (vai para a bíblia visual)
Cenas simbólicas/objeto (sem personagem de época nem lugar no prompt) puxam as refs do Egito mesmo com 'no turbans' ausente: **todo prompt do `cenas.json` precisa do sufixo anti-vazamento + cenário russo**, não só as cenas de época. Sugestão ao `storyboard`: gerar o sufixo para 100% das cenas.
