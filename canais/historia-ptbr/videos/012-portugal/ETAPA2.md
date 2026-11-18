# ETAPA 2 · historia-ptbr/012 Portugal (youtube.videos id 48) · 17/11/2026

**Resultado:** `entrega/video.mp4` **16:30** (989,8 s), 1080p30, **−15,2 LUFS**, pico −4,3 dBFS, **0 telas pretas**, 0 silêncios > 1,5 s, 21 cortes no 1º minuto, 19,9 cortes/min. 3 thumbs + `pacote/youtube.txt`. Drive: não subido (a rotina noturna sobe a partir de `entrega/`). Pode ir ao ar: sex ou sáb (1º/12 = Restauração: publicar antes).

## Custo (financas.consumo, ref_id 48; teto US$ 8): ≈ US$ 0,71
Fish drama-3 US$ 0,15 (63 blocos + 3 tomadas do hook) · Runpod US$ 0,23 (10 partes; parte 8 pedida 3× por Pod lento/timeout do comando, rendida em 2 metades) · pré-QA Anthropic US$ 0,29 · fal US$ 0,046 (**fallback do Codex cobrou a I005 e não salvou o arquivo**, bug já conhecido do 011; a I005 saiu na repetição pelo Codex). Codex US$ 0.

## Voz
Whisper bruto mín 88,5% (nomes/números); **fonético mín 94,1%, média 99,2%**; nenhuma tag falada. Hook: 4 tomadas, melhor combinação `aaaacb` (repetição 0,15 × 0,18 da tomada única). Nenhum mp3 de 0 byte. Ouvir os nomes antes de publicar (ninguém ouviu): Alcanizes, Riba-Côa, Olivença, Calecute, Valença/Tui.

## Imagens: 216 + 13 refeitas, todas pelo Codex (cota 5 h 37%, semana 22%)
Prancha em 9 grades pegou vazamento das refs do Egito (faraó, turbante, moeda egípcia) em I018, I020, I096, I099, I132, I151, I181, I210, I214: refeitas com sufixo `NO turbans/pharaoh…` (aplicado direto em `cenas.json`; `roteiro.py` não tem o sufixo). Depois do pré-QA, refeitas I054 (colagem de 3 painéis com emendas e barco a motor → cena única), I094 (chapéus anacrônicos), I098 (palmeiras), I131 (flor-de-lis). **I019 = mapa de escala composto no código** (`thumbs/escala.py`: Natural Earth + IBGE UF 26, projeção sinusoidal equivalente; áreas PE 98,7 mil, PT continental 88 mil, ES continental 495 mil km², ES/PT 5,6×) com rótulos em `labels.jsx`.

## Pré-QA (120 stills)
Bloqueante 0, alto 9, médio 25. Corrigidos: rótulo PORTUGAL sobre a Espanha (movido para baixo da forma), I054, I094, I098, I131. **Falsos positivos/aceitos:** "Pernambuco fora de posição" (é comparação de escala, de propósito); mapas estilizados (Tordesilhas mostra as Américas com contorno moderno; linha no meio do Atlântico = 370 léguas); araras e ouro em I125 (Colombo volta, 1493); bonde/figurino em I188 (Lisboa 1910); Torre Eiffel em I201 (operários em Paris, anos 1960); placa de capítulo sobre a cena (layout padrão); cartão de ano sobre cena de época (padrão do canal).

## Render
Runpod em 10 partes (0–3599 … 25200–26999, 27000–28799, 28800–29693), todas com quadros = esperado e SSIM aprovada; concat + `mix.wav` AAC 192k (ffprobe: 29.692 quadros lidos × 29.694 esperados: 2 quadros de diferença na junção, 0,07 s, sem efeito visível). **Armadilha repetida:** parte de 3.600 quadros às vezes passa de 280–590 s em GPU lenta (RTX 3090/4090 Community); dividir em 1.800. Trilha: guitarra portuguesa sintetizada + pad em Ré frígio (cap. 8 em diante, notas mais raras).

## QA (6b/6c) — timestamps conferidos na `legendas.srt`
- Detector de cópia **1/100** (`SIMILARIDADE.md`); `CRIVO-ANGULO.md` APROVADO (r2); `CRIVO.md` APROVADO (r2). Roteiro não mudou na etapa 2 (detector não repetido).
- **Promessa paga:** "São mil e duzentos quilômetros de fronteira, marcados com pedras numeradas" **0:01** (T3 e Thumb B); Olivença **0:21**; "A Espanha governa Olivença desde 1801" **0:30**; "a linha é quase a mesma desde 1297" **0:38** (T1, Thumb A); pergunta central ("como um país menor que Pernambuco… por setecentos anos?") **0:46,6–0:54,9** (mapa de escala na tela; um pouco depois do "~0:50" do EMBALAGEM, dentro de 1:00); "e por que, justamente aqui, ela cedeu?" **0:54,9**; "Essa é a história inteira" **0:58**; frase-âncora "Setecentos anos depois… onde aquele menino a assinou" **4:30**; "Lembra dos marcos que faltam?" **12:23**; fecho a partir de 15:48.
- **Thumbs** (`thumbs/compose.py`; bases Codex, silhuetas e letras no código): A `rosto-emocao` guarda espantado + buraco, "CADÊ?"; B `objeto-simbolo` marco de granito com P | E gravados, "700 ANOS"; C `mapa-lugar` silhuetas na mesma escala + bonequinho recortado, "PERNAMBUCO É MAIOR". As 3 leem a 320×180 (`thumbs/prancha-celular.jpg`) e são 3 padrões diferentes. A = T1, B = T2, C = T3; pares gravados em `youtube.embalagem_variantes`. **Não conferi numa foto real se os marcos da raia trazem "P" e "E"** (acréscimo do crivo r2): conferir antes de publicar a Thumb B; se não trazem, trocar as letras. A linha é de 1297; os marcos, de 1864–1926: nenhuma peça diz que a pedra tem 700 anos.

## Pendências
N057: assinatura espanhola do mesmo 12/06/1985 (CVCE). Ouvir os nomes. `img_codex.py`: fallback fal cobra e não salva. Sufixo anti-Egito no `roteiro.py`.
