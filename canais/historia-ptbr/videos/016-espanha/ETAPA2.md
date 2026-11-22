# ETAPA 2 · historia-ptbr/016 Espanha (youtube.videos id 59) · 21–22/11/2026

**Resultado:** `entrega/video.mp4` **17:21,9** (1041,9 s), 1080p30 H.264+AAC, **−15,3 LUFS**, pico −4,3 dBFS, **0 telas pretas**, 22 cortes no 1º minuto, 19,2 cortes/min (334 planos). 3 thumbs + `entrega/pacote/youtube.txt`. Drive: não subido (a rotina noturna sobe a partir de `entrega/`). `youtube.videos` 59 = `pronto`; pares A/B/C em `youtube.embalagem_variantes`.

## Custo (financas.consumo, ref 59; teto US$ 8): ≈ US$ 0,53
Fish drama-3 US$ 0,155 (70 blocos + 3 tomadas do hook) · pré-QA Anthropic US$ 0,27 · Runpod US$ 0,10 (1 Pod RTX 3090, 31.257 quadros, 18 blocos sem refação) · Codex US$ 0 (207 cenas + 3 bases de thumb, 0 fallback fal; cota 5 h 43%, semana 7%).

## Manada / detector
Retentativa da transcrição da manada na etapa 2: YouTube ainda bloqueia (yt-dlp falha em todos os 7 ids). Detector segue **1/100** (só 2 refs locais); crivo de ângulo r1 aprovado com o conferível. Pendência: reconferir quando o WARP liberar.

## Voz
Whisper fonético mín **95,3%**, média 99,4%; nenhuma tag falada; 0 mp3 vazio. Hook: 4 tomadas, melhor combinação `bacbdd` (repetição 0,07; únicas 0,10–0,22). Ouvir os nomes antes de publicar (ninguém ouviu).

## Imagens e pré-QA
207 (I044 refeita). Prancha em 7 grades: sem vazamento egípcio, sem bandeira atual. Pré-QA (120 stills): bloqueante 0, alto 4. Corrigido: I044 (chegada em 711 vinha com Alhambra/arcos de ferradura → prompt visigodo, original em `qa/rejeitadas/`). Aceitos: Q07 (guarda de 1841 com uniforme da época: correto), Q84 (placa do mapa ok). Cartões de data movidos no `storyboard.json`: 1824 → plano 252 (Ayacucho), 1931 → plano 293; rodar `roteiro.py` de novo desfaz. Ressalva baixa: I007/I008 (Roma de 1469) mostram cúpula ao fundo; I128/I193 trazem a senyera catalã (legítima nas épocas).

## Render
Runpod, 1 comando, 31.257 quadros = esperado, conferência SSIM aprovada em todos os blocos, Pod destruído (0 na conta). Trilha: cordas dedilhadas + pad em Ré frígio (herdada do 014).

## QA (6b/6c): timestamps na `legendas.srt`
- `SIMILARIDADE.md` 1/100; `CRIVO-ANGULO.md` APROVADO (r1); `CRIVO.md` APROVADO (r3). Roteiro não mudou.
- **Promessa paga:** "cada lado fica com a sua lei, a sua alfândega, a sua moeda" **0:29**; pergunta central "por que a Espanha juntou meio mundo antes de conseguir juntar a si mesma?" **0:41**; "o rei foi rei das Espanhas, no plural: uma pilha de coroas numa cabeça só" **0:47–0:52** (Thumb A); "a última alfândega de dentro só caiu em 1841" **0:55** (T2/Thumb B); "essa é a história inteira da Espanha" **1:01**. Cena da alfândega **3:45**; "o império que ainda não era um país" **7:43** (T3). Tudo ≤ 1:00 exceto o "inteira" (1:01).
- **Thumbs** (`thumbs/compose.py`, bases Codex sem letras, texto no código): A rosto-emocao "REI DAS / ESPANHAS" (ouro); B conflito-xvy "CASTELA × NAVARRA" (boina escura, como o crivo exigiu); C objeto-simbolo coroa costurada + pílula "1469". Leem a 320×180 (`thumbs/prancha-celular.jpg`), 3 padrões diferentes, cada uma = seu conceito; A=T1, B=T2, C=T3 (títulos sem ajuste de N). Desvio: na A o rei ocupa ~50% da altura (crivo pediu ≥ 35%: ok) e a pilha tem 4–5 coroas legíveis.

## Pendências (não bloqueiam)
Ouvir nomes; reconferir manada/detector; duração 17:22 (brief mirava 15–17 min, título sem N).
