# ETAPA 2 · historia-ptbr/017 Cuba (youtube.videos id 61) · 22–23/11/2026

**Resultado:** `entrega/video.mp4` **16:40** (1000,0 s), 1080p30 H.264+AAC, **−15,2 LUFS**, pico −4,2 dBFS, **0 telas pretas**, 19 cortes no 1º minuto (016 teve 22), 19,5 cortes/min (325 planos). 3 thumbs A/B/C + `entrega/pacote/youtube.txt`. Drive: não subido (rotina noturna). `youtube.videos` 61 = `pronto`; pares A/B/C em `youtube.embalagem_variantes`.

## Custo (financas.consumo, ref 61; teto US$ 8): ≈ US$ 4,73
Fish drama-3 US$ 0,154 · pré-QA Anthropic US$ 0,26 · Runpod US$ 0,35 (4 Pods perdidos, ver abaixo) · fal US$ 3,97 · Codex US$ 0.

## Voz
63 blocos, Whisper fonético mín **96,6%**, média 99,5%, nenhuma tag falada. Hook: 4 tomadas, escolhida a `dddddd` (repetição 0,08; as outras 0,13–0,22) instalada sobre N001–N006. Ouvir os nomes (Jesús del Monte, Khrushchev, Mikoyan) antes de publicar: ninguém ouviu.

## Imagens
206 imagens (Codex 146, fal 60). Cota `imagegen_premium` do Codex esgotou na 40ª imagem (22/11 21:33, reset 23:29); o fallback automático gastou US$ 1,3 e depois cobri 60 com `img_fal.py` (US$ 2,77) enquanto esperava o reset; as demais 106 saíram no Codex após o reset. Resumo: I001–I040 Codex, I041–I100 fal (60), I101–I206 Codex (106).
**Vazamento do Egito (a armadilha prevista):** cenas abstratas (balança, mão com contrato, rei com cesta, mesa com moedas, correia de produtos, maço com cadeado, lupa no contrato) vieram com turbante/faraó/bazar árabe porque os prompts sem cenário não levavam o `NAO_EG`. 8 refeitas (I011, I012, I102, I120, I174, I176, I177, I205) com fundo creme + roupa de época + NO turbans; originais em `qa/rejeitadas/`. `cenas.json` foi corrigido à mão (roteiro.py também só para I011/I012; rodar `roteiro.py` de novo desfaz as outras 6).

## Pré-QA
100 stills (a cada 10 s). `PREQA-visual.md`: bloqueante 0, alto 1 (Q33, 5:25: "imagem fantasma" = crossfade entre planos, falso positivo), médio 19, baixo 28. Prancha completa conferida a olho antes.

## Render
**Runpod falhou 4×** (2 rodadas: A: 3090 Community ×2, B: 4090 Community ×2): SSH com timeout ou Pod sem IP em 15 min, "prova reprovou 2 máquinas" (código 2), ~US$ 0,35 perdidos, Pods destruídos (0 na conta). Fallback VPS autorizado pelo procedimento: arte 2D, **~19 fps** (5.000 quadros em 4 min 20 s), 4 partes (0–4999, 5000–13999, 14000–22999, 23000–30000), `render_partes.sh juntar`; 30.001 quadros. Sem a conferência SSIM do script (só pré-QA + qa.sh). Memória OK (RAM 1,3 GB usados).

## QA (6b/6c): timestamps na `legendas.srt`
- `SIMILARIDADE.md` 2/100; `CRIVO-ANGULO.md` APROVADO (r3); `CRIVO.md` APROVADO (r3). Roteiro não mudou.
- **Promessa paga:** "setecentas mil toneladas ficam sem comprador" **0:18–0:23** (Thumb A) → "Moscou se oferece para comprar exatamente essas setecentas mil" **0:26** (T2) → "quase cinco vezes o preço do mercado" **0:32–0:36** (Thumb B) → "nenhum comprador de Cuba cobrou só em dinheiro" **0:36–0:41** → pergunta central **0:48–0:54** → "essa é a história inteira de Cuba" **0:54**. Tudo ≤ 1:00. As 700 mil voltam em 10:37 e 16:18.
- Thumbs (`thumbs/compose.py`, bases Codex sem letras, texto no código; 3 padrões, cada uma = seu conceito; A=T1, B=T2, C=T3, títulos sem N): A rosto-emoção "SEM COMPRADOR"; B "5× O PREÇO" sobre vermelho; C ilha amarrada por corda, sem texto (`thumbs/prancha-celular.jpg`).

## Pendências (não bloqueiam)
Ouvir nomes; 19 cortes no 1º minuto (< 21); Runpod instável na noite de 22/11 (investigar se foi a conta/host); dois navios de vela no lugar do "cargueiro" na thumb A (cena de 1960 num navio antigo: aceitável na thumb, não é imagem do vídeo).
