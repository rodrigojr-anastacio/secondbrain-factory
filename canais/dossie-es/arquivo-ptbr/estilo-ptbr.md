# Estilo: Dossiê em Minutos (dossie-ptbr)

Base: `pesquisa/archive-in-minutes/LEVANTAMENTO.md` (2026-11-04). Modelo: Archive in Minutes. A **identidade é nossa** (o "dossiê"); nunca copie a thumb, o hook ou o texto deles. Este canal **não** usa o bonequinho nem o papiro do `historia-ptbr`.

## Fórmula
- **Título:** "A história INTEIRA da <organização> em N minutos". INTEIRA em caixa alta; N = duração real arredondada; X com 1–3 palavras, de preferência sigla famosa (KGB, CIA, SS, Stasi). [Archive: organizações famosas com mediana de 146 mil × eventos com 38 mil]
- **Duração:** 10–16 min (alvo 13). ~1.750 palavras para 13 min no nosso ritmo (~135 palavras/min com pausas). Acima de ~17 min, não.
- **Temas:** organizações temidas e famosas primeiro. Ângulo Brasil/lusófono só com fato real e fonte.

## Roteiro
1. **Hook de 15–25 s (molde anedota):** data + lugar → cena humana concreta em 2–4 frases curtas, no presente → desfecho seco ou reviravolta → "Esta é a história INTEIRA da X" → promessa ou pergunta em 1 linha. Sem "olá", sem vinheta, sem pedir inscrição.
   - Use uma anedota **diferente** da usada pelo Archive e pelos clones (eles repetem Eichmann no Mossad e Putin em Dresden na KGB).
2. **Fichas (capítulos-objeto):** 10–14 capítulos de 40–80 s, em ordem cronológica, com o título "FICHA N: O <OBJETO>" (ex.: "FICHA 4: O PICADOR DE GELO"). Cada ficha é uma cena ou objeto datado; os números são exatos, com fonte.
3. **Fecho:** volta ao objeto do hook (loop pago) e liga ao presente, com 1 pergunta para os comentários.
4. **Tom:** presente histórico, factual, seco, quase sem adjetivo; o horror vem do fato. Condenação clara de crimes; contexto das vítimas. Fato incerto é dito como incerto ("segundo um ex-general da própria KGB…").

## Visual
- **Imagens:** `fal-ai/nano-banana` 16:9 (1344×768) no `estilo_prompt` do `canal.yaml`: graphic novel em tinta, contorno grosso, paleta azul-ardósia/oliva/sépia/carvão com **vermelho pontual**. Rostos adultos e época correta (uniformes, carros, prédios). Teste em `testes/ESTILO.md`.
- **Ritmo:** ~18–20 planos/min no 1º minuto e ~15–17 depois. Reuso de 0% nos 3 primeiros minutos e de ~35% depois. ~170 imagens para 13 min (~US$ 6,60).
- **Texto na tela (no código, nunca na IA):**
  - rótulo de cena em letra de máquina de escrever (Special Elite ou Courier Prime) sobre tira de papel `#E9DFC9`, com sublinhado ou carimbo vermelho `#B3261E` ("LONDRES, 1978");
  - cartão de ficha: pasta parda + "FICHA 3" + título em caixa alta + carimbo "CONFIDENCIAL";
  - mapas: papel bege sem rótulos (prompt "no people, no hands"), pino e seta vermelhos animados.
- **Proibido:** suástica, runas SS e insígnias extremistas em destaque (o prompt já exclui); sangue e cadáveres; fotos de arquivo e trechos de filme (Content ID); legenda queimada.
- **Trilha:** original, sintetizada no código (drone grave + pulso), sob a voz a −33 dB; mix em −15 LUFS. SFX discretos: máquina de escrever no rótulo, carimbo na ficha.

## Thumbnail
- Layout "pôster de dossiê": personagem-ícone em meio corpo à **esquerda** (chefe ou agente arquetípico, com objeto na mão) + cenário reconhecível + **SIGLA gigante** (Bebas Neue ou Oswald 700, preta, sombra chapada) à direita + **carimbo vermelho inclinado com o período** ("1917–1991") + **aba de pasta parda** no canto superior direito com o número da ficha do canal ("DOSSIÊ Nº 001"). Essa aba é a nossa assinatura na grade.
- Base em nano-banana com "right half empty, no signage, no lettering"; texto composto em `src/Thumbnail.jsx`. 3 variações para o "Testar e comparar".

## Voz
- Fish s2.1-pro, voz **diferente** da do `historia-ptbr` (escolha do Rodrigo): masculina, grave, sóbria, sem sotaque marcado. Velocidade 1.0. Regras de pausa iguais às do `historia-ptbr` (0,35/0,9/1,5 s; `conhecimento/anti-padroes.md` #2). Tags dominantes: `[serious]` e `[slightly dramatic]`.

## Políticas (ver LEVANTAMENTO §3d)
- Conteúdo educacional/documental com contexto (EDSA). Nada que glorifique.
- Descrição com fontes (livros e arquivos) e a nota "Narração com voz sintética; ilustrações geradas por IA a partir de pesquisa histórica".
- Cadência humana (2–3/semana), roteiro original: nunca template em massa (política de conteúdo inautêntico do YPP).
