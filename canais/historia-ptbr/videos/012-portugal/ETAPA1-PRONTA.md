# ETAPA 1 PRONTA · historia-ptbr/012-portugal · 17/11/2026
Vídeo `youtube.videos` id 48 · `CRIVO.md` APROVADO (embalagem, rodada 2) · `CRIVO-ANGULO.md` APROVADO (rodada 2) · pares registrados em `youtube.embalagem_variantes`.

## Ângulo
**A linha:** a fronteira luso-espanhola, quase a mesma desde 1297, como fio da história inteira; o único trecho que cedeu (Olivença, 1801, ~cem marcos nunca postos) abre e fecha o vídeo. Detector de cópia: **1/100** (`SIMILARIDADE.md`). Crivo de ângulo: **aprovado na r2** (r1 reprovou as aberturas dos caps. 1 e 6, reescritas).

## Os 3 pares aprovados (crivo r2; r1 reprovou T3, Thumb B e Thumb C)
| par | título | padrão do título | thumb (padrão) | texto da thumb |
|---|---|---|---|---|
| A | "A fronteira de Portugal é QUASE a mesma desde 1297. Como?" (57) | afirmação estranha + pergunta | `rosto-emocao`: fiscal bonequinho espantado, mão na cabeça, ao lado da fila de marcos de pedra com um **buraco grande no 1º plano**; cidade branca do outro lado do rio | "CADÊ?" |
| B | "Como uma LINHA protegeu Portugal (até o dia em que cedeu)" (57) | Como [coisa concreta] [verbo] [lugar] (virada) | `objeto-simbolo`: marco de granito prismático (topo em pirâmide), três-quartos, **P** e **E** compostos no código, cravado sobre uma linha de marcos/muro que corta os morros; de dia, sem halo | "700 ANOS" |
| C | "Por que Portugal ainda existe? A resposta tem 1.200 KM" (54) | pergunta + "A resposta tem…" | `mapa-lugar` (escala): silhuetas reais na mesma escala, Pernambuco (verde) e Portugal (ouro) lado a lado, Espanha enorme cinza-escuro colada a Portugal; bonequinho minúsculo de braços cruzados sobre Portugal; pergaminho claro, sem setas | "PERNAMBUCO É MAIOR" |
A = T1, B = T2, C = T3. Detalhes de composição, prompts e referências em `EMBALAGEM.md`.

## Promessa e onde o roteiro a paga
Promessa: como um país menor que Pernambuco segurou quase a mesma fronteira com a Espanha por setecentos anos, e onde, e por que, ela cedeu uma única vez.
- **0:00–0:30 (N001):** "São mil e duzentos quilômetros de fronteira, marcados com pedras numeradas." (paga o "1.200 KM" do T3 e a Thumb B)
- **~0:10–0:43 (N002–N004):** os marcos pulam do 801 para o nada diante de Olivença; 1801; "quase a mesma desde 1297" (paga T1, Thumb A, onde do T2).
- **~0:43 (N005):** pergunta central "Como um país menor que Pernambuco segurou a mesma fronteira com a Espanha por setecentos anos?" + "por que, justamente aqui, ela cedeu?" (paga Thumb C: o storyboard põe o mapa de escala nesse bloco).
- **~3:48–4:40 (N017–N020):** Alcanizes 1297, Fernando IV com 11 anos, frase-âncora "Setecentos anos depois, quase toda a linha continua onde aquele menino a assinou." (T1, Thumb B).
- **~11:40–12:50 (N045–N048):** Guerra das Laranjas, Badajoz, Viena, "Lembra dos marcos que faltam? Olhe de novo: é aqui." (por que cedeu: T2).
- **~10:00–11:00 (N040–N043)** e **~15:20 (N058)**: Elvas e as cancelas de 1995; **fecho ~16:00 (N061–N062):** "A resposta tem mil e duzentos quilômetros, e gente em cima deles…" e os cem marcos em 2026 (T2: a linha protegeu porque havia gente segurando-a; T3 respondido).
Tempos estimados a 128 ppm; o QA confere na `legendas.srt`.

## O que a etapa 2 precisa saber
- **Roteiro:** 63 blocos, 2.138 palavras, ~16:43 estimados (alvo ≤ 17:00; o título não leva "em N minutos"). Voz Fish drama-3 (`canal.yaml`), 1 chamada por bloco; grafias para a voz em `FALA` do `roteiro.py` (Godói, Jerônimos, Andêiro…); conferir pronúncia de Alcanizes, Riba-Côa, Olivença, Calecute, Túnis, Valença, Tui.
- **Storyboard:** 329 planos, **216 imagens** (`cenas.json`), reuso 43% depois de 3:00, 0 avisos. Codex (`img_codex.py`) com fallback fal; teto US$ 8 → não deixar o lote inteiro cair no fal (216 × 0,046 ≈ US$ 9,9). Os prompts já levam `IBER` (sem pirâmide/palmeira/faraó: vazamento das refs do Egito, `biblia/visual.md` 010/011), `SEMBAND`, `SEMTXT`, `GUERRA`; conferir a prancha inteira antes do pré-QA.
- **Composto no código:** `escala_pe_pt_es` (N005 e N061) com contornos reais na mesma escala (Natural Earth `~/cache/nasa/ne_50m_admin_0_countries.geojson` + malha do IBGE de Pernambuco; Portugal continental), o mesmo asset da Thumb C; rótulos de mapa em `src/labels.jsx` (o `labels.jsx` copiado é do 011: refazer para os mapas deste vídeo). Os cartões de data (`card`) e os 21 rótulos `@@` estão no storyboard.
- **3 thumbs, uma por conceito** (A, B, C acima), nunca 3 variações; texto, letras P/E e silhuetas no código. Antes da Thumb B, conferir numa foto real se os marcos da raia trazem "P" e "E" (acréscimo do crivo r2); a linha é de 1297, os marcos numerados são de 1864–1926: nunca dizer nem mostrar que as pedras têm 700 anos.
- Trilha: escala sugerida modo frígio/fado (guitarra portuguesa sintetizada), Ré menor.
- Olivença com neutralidade (posição de cada governo); 1383, guerras, Salazar/Franco e guerra colonial sem imagem gráfica.

## Pendências (não bloqueiam)
- N057: conferir no QA a assinatura espanhola no mesmo 12/06/1985 (CVCE).
- Godoy/laranjas é tradição ("diz a tradição" no texto).
- Fernando IV corrigido para 11 anos (BRIEF/EMBALAGEM diziam 12).
