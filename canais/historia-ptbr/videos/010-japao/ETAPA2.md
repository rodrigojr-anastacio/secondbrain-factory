# ETAPA 2 · historia-ptbr/010 Japão (youtube.videos id 40) · 14/11/2026

**Resultado:** `entrega/video.mp4` **15:23** (922,9 s), 1080p30, **−15,3 LUFS**, pico −4,2 dBFS, **0 telas pretas**, 0 silêncios > 1,5 s, 21 cortes no 1º minuto, 20 cortes/min. 2.006 palavras (~130 ppm). Título A sem "N minutos" (duração só na descrição).

## Custo (financas.consumo, ref_id 40)
Fish drama-3 US$ 0,69 (11.350 B + 3 tomadas do hook) · fal US$ 0,09 (2 imagens de fallback) · Runpod US$ 0,51 (4 partes; 1 Pod perdido por envio falho, ~US$ 0,28) · pré-QA Anthropic US$ 0,39. **fal+Fish = US$ 0,78; total ≈ US$ 1,68 (teto 8).**

## Imagens: Codex × fallback
233 imagens pelo Codex (218 do storyboard + 10 refeitas + 5 bases de thumb), **2 pelo fallback fal** (falha do Codex, 1 em cada lote de 25), 0 faltando. ~6,4 min por lote de 25 (3 em paralelo), ~1 h 20 no total. Cota Plus ao fim: 5 h 42%, semana 8% (`tools/codex_uso.sh 1`: 236 imagens Codex, fal US$ 0,23 no dia incluindo outros vídeos).
Refeitas (12 incluindo as de risco): **I003, I182, I191, I205** (bandeira/sol vermelho apareceram mesmo sem pedir: Hinomaru e Sol Nascente em I003/I191, bandeiras em I182/I205) e **I046, I048, I049, I066, I171, I189, I194, I195** (as refs de estilo vêm do Egito: o Codex pôs faraó, turbante, coroa, deserto e ruínas gregas em cenas do Japão: Amaterasu, espelho-espada-joia, imperadores, carta, guia de terno, vigília, relógio, cúpula de Hiroshima). Correção: prompt com `NJ` (cenário no Japão, sem faraó/turbante/coroa/pirâmide/deserto) + `SEMBAND`/`SEMSOL` e "nobody in the picture" em objetos. Prancha de 218 conferida em 8 grades (`qa/pranchas/`): I184–I200 (1910–1945) sem símbolo, bandeira, corpo ou sangue.

## Voz
Fish drama-3, 1 chamada por bloco, 63 blocos, grafias do `FALA` (Cublai Cã, camicáze, Iamáto, Amaterássu, Quióto, Murassáki Xikíbu, Guêndji, Rakáta, Takaxíma, Taneguaxíma, Tokugáua, Méthiu Péri, Mêidji, Iokorráma, Kassáto Máru, Pérl Rárbor, Iroxíma) **sem nenhuma troca**. Whisper bruto mín 86,7% (13 blocos < 93%, nomes), média 96,9%; **fonético mín 96,6%, média 99,5%**; nenhuma tag falada. Hook: 4 tomadas de N001–N006, melhor combinação `dbcadc`. **Ouvir os nomes antes de publicar** (ninguém ouviu).
Cap. 9 (N050–N055): `[serious]` no N050; conferir de ouvido N051 (Nanquim) e N053 (bombas).

## Pré-QA (118 stills, Claude Sonnet com visão)
**0 bloqueantes**, 13 altos, 24 médios, 29 baixos. Corrigidos: rótulos de mapa (JAPÃO sobre a Coreia em `map_china_japan`, CHINA sobre a Coreia em `map_japan_sea` → COREIA) e "IMPÉRIO DO JAPÃO, 1932" × selo 1910 (rótulo sem ano), imagens com faraó/turbante (acima). Falsos positivos anotados: ferraria com arcabuzes no hook (I017, antecipa o "copiar", intencional), canhoneio de Guerra do Ópio com casacas britânicas (I160, é o assunto), uniforme de Perry em estilo cartoon, placas de ano em fade, castelo branco em cenas medievais (estilo), Torre de Tóquio + castelo + Fuji em 1964 (simbólico). Não rodei a 2ª rodada (sem bloqueante).

## Render
Runpod em 4 partes (0–6921, 6922–13843, 13844–20765, 20766–27687; SSIM de prova 1,000, de blocos ≥ 0,997) + concat com `mix.wav` AAC 192k; 27.686 de 27.688 quadros (−2, sem efeito visível). Trilha: pad de Lá + koto (Karplus-Strong, escala *in* de Lá) com sopro de shakuhachi até o cap. 6; piano suave esparso em Lá eólio depois, sem sino nem marcha. Armadilha: o 1º Pod levou 384 s para o SSH e o envio falhou (Pod destruído, US$ 0,28); a 2ª tentativa foi normal. Bundle com `mix.wav` mudo de 2 s (sem os wavs grandes).

## QA (item 6b) — timestamps conferidos na `legendas.srt`
- "Foi só sorte?" **0:35**; "esse país vivia **copiando** os vizinhos" **0:41**; pergunta central "como um país que copiava todo mundo passou quase setecentos anos sem que ninguém o conquistasse?" **0:46–0:54** (≤ 0:50 de início, ok); "O mar era o muro do Japão… um dia esse muro vai falhar" 0:55; "Guarde esse vento" 1:03.
- "Foi só sorte?" respondido em **6:05–6:23** (Takashima, "o mar dava tempo"); "**Nesse dia, o mar parou de proteger o Japão**" **9:46**; "Sorte foi uma noite" 15:03.
- Thumb final = conceito do EMBALAGEM (bonequinho com tocha no muro, olhar por cima do ombro, tufão no alto à direita, "SÓ SORTE?" + "1281", sem sol vermelho/Fuji/castelo/mapa). A = T1, B = T2 (mesma arte com enquadramento fechado), C = "FOI O VENTO?" (expressão de grito). Legibilidade 320×180 ok (`thumbs/prancha-celular.jpg`).

## Entrega
`entrega/`: video.mp4, legendas.srt, thumb-A/B/C.jpg, pacote/youtube.txt. **Drive: enviado** (`Youtube/História em minutos/010-japao/`, 567 MiB). Data de publicação: `youtube.backlog` diz qua 18/11.

## Trechos para conferir
0:28–0:35 kamikaze/"foi só sorte" · 5:37 muro de pedra · 9:46 "o mar parou de proteger" · 12:09 "o país que ninguém conquistava agora conquistava os vizinhos" · Nanquim e bombas (cap. 9, ~12:30–13:20).

## Pendências
Ouvir os nomes japoneses. Posição dos rótulos de mapa passa pelo pan do Ken Burns: `map_1905` ficou sobre o mar da Coreia (aceitável).
