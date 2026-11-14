# Reembalagem historia-ptbr (pesquisador B): Irã, Rússia, Roma (14/11/2026)

Escopo: 003 Irã, 007 Rússia e 006 Roma. Egito, Índia, China e Brasil estão em `historia-ptbr-A.md`.
Método: yt-dlp `ytsearch` via WARP (13 buscas, 0 cota) + `videos.list`/`channels.list`/`playlistItems` (~150 unidades). **`search.list` gastos: 0.** A mediana de cada canal vem dos últimos ≤ 30 longos (> 3 min). Janela: ≤ ~400 d. As exceções mais antigas estão marcadas.
Dados: `dados/historia-ptbr/B-busca-enriquecida.csv` (270 vídeos), `B-referencias.csv` (as 40 citadas, com mediana e "acima?"), `B-medianas-canais.json`, `raw/B-ytsearch-*.jsonl`, `thumbs/B-*.jpg`, scripts em `scripts/B-*.py`. Mosaicos (a nossa thumb no 1º quadro): `mosaicos/historia-ptbr-003-ira.jpg`, `-007-russia.jpg`, `-006-roma.jpg`.
**Bíblia (`biblia/titulo.md`) conferida:** mantém "A história INTEIRA de X em N minutos" como fórmula A e libera título-pergunta/tensão como braço B. Por isso "em N minutos" aparece só nos títulos que seguem a fórmula.
**Títulos no ar hoje (videos.list, 14/11):** Irã = "A história **COMPLETA** do Irã (Pérsia) em 18 minutos" (o brief e o banco dizem INTEIRA); Rússia e Roma = "A história INTEIRA de X em 17 minutos". **Colisão confirmada:** o de Roma só muda o N em relação ao HEG "A HISTÓRIA INTEIRA de Roma em 12 minutos" (73 mil) e ao clone 10/2026b "A HISTÓRIA COMPLETA de Roma em 12 Minutos".

---

## 1. Padrões do nicho (pt-BR, história de país/império)

### Títulos
| # | Padrão | Exemplos reais (views · data · acima da mediana do canal?) | Leitura |
|---|---|---|---|
| T-A | **Fórmula "Toda a história / A HISTÓRIA INTEIRA de X em N min"** | Crônicas de Ferro [Irã](https://youtu.be/uEDDMWJ04Vo) 1,48 mi · 12/03/26 · sim (52 mil); clone pt [Rússia](https://youtu.be/aMld6kMmcm4) 254 mil · 19/10/26 · sim (2,4 mil); HEG [Roma](https://youtu.be/XyulPwDw1CE) 73 mil · 28/10/26 · sim (5,5 mil); Historiadores contam [Irã](https://youtu.be/_fsuhnrBYGI) 30 mil · 11/03/26 · sim (3 mil) | Só funciona para quem chega **primeiro** ou na onda de notícia (o Irã de março/26, com a guerra). Ela virou commodity: há 10+ canais com o mesmo título. |
| T-B | **Pergunta de transformação do nome/identidade** ("Por que a Pérsia virou Irã?") | Histórias Milenares [POR QUE A PÉRSIA MUDOU SEU NOME PARA IRÃ](https://youtu.be/jvM3cR235yw) 294 mil · 19/04/26 · sim (41 mil); Explore o Mundo [Como a Pérsia "se tornou" o Irã?](https://youtu.be/-UxuSFveBN8) 222 mil · 10/03/26 · sim (124); Além do Mapa [Por Que a Pérsia Desapareceu…](https://youtu.be/LwC-YJMsYuY) 62,5 mil · 04/03/26 · sim (2,7 mil); Brasil Paralelo [ENTENDA POR QUE A PÉRSIA PASSOU A SE CHAMAR IRÃ](https://youtu.be/3mwAf9TW1MU) 61,9 mil · 11/03/26 · sim (12,8 mil) | É a pergunta que o público pt já faz. **Saturada:** 8 cópias literais tiveram 1–180 views (Linha do Tempo 5, Tempo em Movimento 6, InsiderCuts 50). Só a pergunta não basta: precisa de um 2º gancho. |
| T-C | **"Como [X] virou/se tornou o maior … do mundo?"** (ascensão) | Pablo Soncini [A História de Roma: Como se Tornou o Maior Império do Mundo?](https://youtu.be/XyX7Y-xyhyg) 508 mil · 23/11/25 · sim (2,4 mil); Além do Mapa [Como a Rússia ficou tão grande? A resposta é um animal](https://youtu.be/wMFP6PadPmQ) 28,4 mil · 07/10/26 · sim (2,7 mil); Epopeia [… como Roma conquistou o mundo e por que caiu](https://youtu.be/US27NANBd2g) 30,4 mil · 05/11/26 · sim (20,9 mil) | A pergunta crua flopa (Fronteiras do Mundo "Como a Rússia se tornou o maior país do mundo" 1 view; Noviterra 272). Rende quando traz um **2º elemento-surpresa** ("a resposta é um animal"). |
| T-D | **Queda/virada** ("Como o maior império caiu / o fim de") | Mundos Reimaginados [Como o Maior Império do Mundo Desmoronou em 5 Dias](https://youtu.be/3hfd_Y50QoM) 484 mil · 28/05/26 · sim (116 mil); Histórias Romanas [A QUEDA DE ROMA: O DIA em Que o IMPÉRIO ROMANO Acabou de Vez!](https://youtu.be/cM9084oMpXc) 189 mil · 04/04/26 · sim (62 mil); Arquivos do Velho Mundo [O Fim do Império Romano (476 d.C.)](https://youtu.be/RDmf1C7xXv0) 432 mil · 15/04/26 · sim (476); HEG [Eles Dominavam o Mundo… e Caíram Assim](https://youtu.be/ctiKJmt4Pws) 10,9 mil · 06/11/26 · sim (5,5 mil) | É perda/medo: o gatilho mais forte em Roma. |
| T-E | **Recorte "De A a B" / "N anos"** + escopo | HQ [Pérsia: 4000 Anos de História do Império Antigo ao Irã Moderno](https://youtu.be/dTIFl2db3As) 281 mil · 17/02/26 · sim (13,6 mil); HQ [Rússia: 1.200 Anos de Conquistas…](https://youtu.be/GN-ybIXIpww) 203 mil · 26/03/26 · sim; HQ [753 a.C. Império Romano – Da Fundação à Queda…](https://youtu.be/sLyfGzpuIGY) 204 mil · 09/01/26 · sim; Pablo Soncini "(Da Fundação ao Império)" 508 mil · sim. Apoio en: Echoes [5000 Years… From Cyrus the Great to Ali Khamenei](https://youtu.be/_cc_sdKBh14) 2,1 mi · 26/03/26 · sim (455) | Mantém a promessa de "história inteira" sem ser idêntico aos clones: as duas pontas são nomes que o público reconhece. |

Comprimento: os títulos que rendem têm de 39 a 85 caracteres. Os curtos são fórmula (T-A); os de pergunta, 45–60. Afirmação e pergunta aparecem juntas nos mais diferenciados ("Como a Rússia ficou tão grande? A resposta é um animal").

### Thumbs (ver os 3 mosaicos + `thumbs/B-*.jpg`)
| # | Padrão | Exemplos (views · acima da mediana?) | Como conversa com o título |
|---|---|---|---|
| H-1 | **Antes × depois em tela dividida** (antigo à esquerda × moderno à direita, rachadura no meio) + 1 pergunta curta | Brasil Paralelo [POR QUE MUDOU?](https://youtu.be/3mwAf9TW1MU) (Ciro × Khamenei) 61,9 mil · sim; Tinocando [IMPERADOR LOUCO](https://youtu.be/nOCIGkJlGII) (busto de Nero × rosto atual) 663 mil · sim; en: Animated History [1279 · 2026 HOW?](https://youtu.be/pBJpDpMqigw) 1,27 mi · sim; Echoes "FROM CYRUS TO KHAMENEI" 2,1 mi · sim. Contra-exemplo: Fatos Desconhecidos (rosto dividido) 215 mil, **abaixo** da mediana dele (237 mil) | A thumb mostra as duas pontas e o título pergunta o meio. |
| H-2 | **Mapa gigante aceso + figura pequena/1 pergunta** | Além do Mapa [RÚSSIA GIGANTE. POR QUÊ?](https://youtu.be/wMFP6PadPmQ) 28,4 mil · sim; Versed [NÃO É UM PAÍS](https://youtu.be/T6f2gWo9kS0) 33,9 mil · sim; Histórias Milenares (mapa com "Pérsia" riscado) 294 mil · sim; en: Ziro [Russia](https://youtu.be/piAKzRm1i_c) 367 mil · sim | O tamanho vira a pergunta, sem texto longo. |
| H-3 | **1 personagem grande com emoção forte + ruína/fogo, quente e escuro** | Histórias Romanas [O FIM DE ROMA](https://youtu.be/cM9084oMpXc) (imperador abatido, ruínas, céu de tempestade) 189 mil · sim; HEG [1 TIRO E O MUNDO EXPLODIU](https://youtu.be/IdvlTEQ72r8) (bonequinho de cabeça redonda espantado) 237 mil · sim; en: Historically [Rome](https://youtu.be/EHLI2WZUtXs) (**bonequinho de cabeça redonda chorando**, o nosso traço) 10,7 mi · sim | Emoção + objeto, e o título explica o porquê. **Não copiar** os corpos com olhos em X do Historically (política). |
| H-4 | **Líder atual + cidade em chamas + NOME + datas** | clone pt [Rússia](https://youtu.be/aMld6kMmcm4) 254 mil · sim; Ziro 367 mil · sim; Explore o Mundo [IRAN](https://youtu.be/-UxuSFveBN8) (Khamenei + letras em fogo) 222 mil · sim | É o molde dos clones (gap 2). **Não usar**: seria cópia, e os nossos vídeos não são sobre o líder atual. |

Regras que saem daqui: (1) o turbante preto com barba branca é o atalho visual do Irã em 6 de 9 thumbs (`mosaicos/historia-ptbr-003-ira.jpg`); (2) nas thumbs que rendem há 1–3 palavras, quase sempre pergunta ("POR QUE MUDOU?", "HOW?", "POR QUÊ?"); (3) as de Roma que mais rendem são escuras e de perda, enquanto as claras e didáticas (Epopeia, HEG) ficam perto da mediana.

---

## 2. Por vídeo

### 003 Irã · `GkzMbsB0iH0`
**Atual:** "A história COMPLETA do Irã (Pérsia) em 18 minutos" (no ar) · 166 impr · CTR 6,0% · retenção 51% · thumb COROA × TURBANTE.

**Top referências (mesmo tema)**
| Vídeo | Canal | Inscritos | Views | Data | v/i | > mediana? |
|---|---|---|---|---|---|---|
| [Toda a história do Irã em 20 minutos](https://youtu.be/uEDDMWJ04Vo) | Crônicas de Ferro | 32,3 mil | 1.484.763 | 12/03/26 | 46 | sim (52 mil) |
| [POR QUE A PÉRSIA MUDOU SEU NOME PARA IRÃ](https://youtu.be/jvM3cR235yw) | Histórias Milenares | 69,7 mil | 294.166 | 19/04/26 | 4,2 | sim (41 mil) |
| [Pérsia: 4000 Anos de História…](https://youtu.be/dTIFl2db3As) | História do Mundo em HQ | 30 mil | 280.657 | 17/02/26 | 9,4 | sim (13,6 mil) |
| [Como a Pérsia "se tornou" o Irã?](https://youtu.be/-UxuSFveBN8) | Explore o Mundo | 6,6 mil | 222.147 | 10/03/26 | 34 | sim (124) |
| [A história do Irã: como chegamos até aqui?](https://youtu.be/oaa1SDG0U0Q) | Brasil Paralelo | 5,38 mi | 194.520 | 28/03/26 | 0,04 | sim (12,8 mil) |
| [Por Que a Pérsia Desapareceu…](https://youtu.be/LwC-YJMsYuY) | Além do Mapa | 2 mil | 62.529 | 04/03/26 | 31 | sim (2,7 mil) |
| [ENTENDA POR QUE A PÉRSIA PASSOU A SE CHAMAR IRÃ](https://youtu.be/3mwAf9TW1MU) | Brasil Paralelo | 5,38 mi | 61.880 | 11/03/26 | 0,01 | sim |
| apoio en: [The ENTIRE History of Iran in 11 Minutes](https://youtu.be/XO1-4FH1X1I) | Genius History | 41,9 mil | 963.343 | 04/07/26 | 23 | sim (99 mil) |
Quase tudo nasceu na onda da guerra de mar–abr/2026. Hoje o tema é perene no pt: a pergunta "Pérsia → Irã" segue sendo buscada (há clones de 08 e 11/2026).

**O que entregamos de verdade (legendas.srt conferida)**
- **00:00–00:43**, o cavalo de Dario: "Ao nascer do sol… o dono do cavalo que relinchar primeiro vira rei" (00:13) e "Um império escolhido, literalmente, por um cavalo" (00:43).
- **00:54–01:00**, a tese (paga no 1º minuto): "Um país invadido por gregos, árabes, mongóis e turcos, e que, toda vez, acabou ensinando os invasores a viver como persas."
- **02:52–03:12**, Pérsia × Irã: "a terra dos árias: o Irã" / "E por que o mundo diz Pérsia? Porque é um apelido grego… Pars" / "um rei vai pedir ao mundo que largue o apelido". Pago em **12:22–12:31**: "O mundo agora devia dizer Irã, e não Pérsia."
- **03:14–03:31**, Ciro: "Ele se chamava Ciro… deixou cada povo com seus deuses e sua língua."
- **07:25–07:39**, "Mas o Irã não virou árabe. Egito, Síria e Iraque passaram a falar árabe… ficou com a própria língua. Por quê?" (resposta: o caixão de Ferdowsi, **08:31–08:46**, "Era a língua.")
- **09:36**, "O Irã não venceu os mongóis… ele os digeriu."
- **13:53–14:18**, Khomeini: "De novo, um turbante enfrentou uma coroa" (14:01). **15:03**, Khamenei; **16:15–16:30**, Mojtaba: "Uma revolução feita contra a monarquia hereditária acabou passando o poder de pai para filho."
- **17:46**, "Exércitos conquistam o Irã… e a língua do Irã conquista os exércitos."

**Proposta**
- **Título 1, "Por que a Pérsia virou Irã e nunca virou árabe?"** (47 caracteres). Padrão **T-B, pergunta de transformação**, com um 2º gancho que os clones não têm ("nunca virou árabe"). Refs: Histórias Milenares 294 mil (19/04/26, sim) e Além do Mapa 62,5 mil (04/03/26, sim); também Brasil Paralelo 61,9 mil e Explore o Mundo 222 mil. Pago em 00:54 (tese, 1º minuto), 02:59–03:12 (o nome), 07:25–07:39 (não virou árabe) e 12:27.
- **Título 2, "De Ciro aos aiatolás: a história INTEIRA do Irã em 18 minutos"** (61 caracteres). Padrão **T-E, recorte De A a B + fórmula da bíblia**. Refs: HQ "Pérsia: 4000 Anos… do Império Antigo ao Irã Moderno" 281 mil (17/02/26, sim) e Crônicas de Ferro "Toda a história do Irã em 20 minutos" 1,48 mi (12/03/26, sim); apoio en: Echoes "From Cyrus the Great to Ali Khamenei" 2,1 mi. Pago em 03:14 (Ciro) e 13:53–16:21 (Khomeini, Khamenei, Mojtaba). Não é cópia: nenhum título pt usa "De Ciro aos aiatolás".
- **Thumb, "MESMO PAÍS?" (antes × depois, padrão H-1)**
  - Cena: tela dividida por uma rachadura branca e luminosa, um pouco à direita do centro. À esquerda, fundo ouro com colunas de Persépolis e um rei aquemênida bonequinho (coroa ameada de ouro, barba preta quadrada, manto roxo) com ar sereno. À direita, fundo vermelho-escuro com nuvens e um clérigo bonequinho de turbante preto e barba branca, carrancudo. Os dois se olham de lado, ocupando ~60% da altura.
  - Texto: "MESMO PAÍS?" embaixo, em Libre Caslon 700 ("MESMO" em ouro #F7C21B, "PAÍS?" em branco) sobre degradê escuro, + pílula amarela pequena "559 a.C. · 2026" no topo, ao centro.
  - Promete: as duas pontas de 2.500 anos parecem dois mundos, e a pergunta é o que liga uma à outra. Com o T1, a thumb não repete "Pérsia/Irã" e mostra os dois lados da troca de nome. Com o T2, mostra Ciro e o aiatolá, e o texto pergunta em vez de repetir.
  - Pagamento: 00:51–01:00 ("Essa é a história inteira do Irã… ensinando os invasores a viver como persas") e o fecho 17:23–17:32 ("o nome sumiu e voltou, a coroa caiu para o turbante… e a língua de Ferdowsi segue viva").
  - **Custo zero:** a base já existe (`canais/historia-ptbr/videos/003-ira/v2-amostras/thumbs/base/c1-persia-ira-a.png`, exatamente essa composição); falta só compor o texto novo no lugar de "PÉRSIA → IRÃ" (que repetiria o T1).
  - Refs de thumb: Brasil Paralelo "POR QUE MUDOU?" (Ciro × Khamenei, 61,9 mil, sim) e Tinocando "IMPERADOR LOUCO" (dividida, 663 mil, sim); en: Animated History "1279 · 2026 HOW?" 1,27 mi (sim).
  - Manter COROA × TURBANTE (6,0%) como controle no "Testar e comparar".

### 007 Rússia · `3TwMYoxnF4k`
**Atual:** "A história INTEIRA da Rússia em 17 minutos" · 73 impr · CTR 9,6% · retenção 42% · thumb "UM VIKING NO TRONO?" + 862. O CTR é o maior do canal, mas a amostra é minúscula (~7 cliques). O gargalo é impressão, não clique.

**Top referências**
| Vídeo | Canal | Inscritos | Views | Data | v/i | > mediana? |
|---|---|---|---|---|---|---|
| [Toda a história da Rússia em 37 minutos](https://youtu.be/aMld6kMmcm4) | clone pt "História em minutos" | 5,6 mil | 254.232 | 19/10/26 | 46 | sim (2,4 mil) |
| [Como o Maior Império do Mundo Desmoronou em 5 Dias: A Revolução Russa](https://youtu.be/3hfd_Y50QoM) | Mundos Reimaginados | 109 mil | 483.969 | 28/05/26 | 4,4 | sim (116 mil) |
| [Rússia: 1.200 Anos de Conquistas, Guerras e Poder…](https://youtu.be/GN-ybIXIpww) | História do Mundo em HQ | 30 mil | 203.146 | 26/03/26 | 6,8 | sim (13,6 mil) |
| [Por que a Rússia é formada por 21 países diferentes](https://youtu.be/T6f2gWo9kS0) | Versed em Português | 13,6 mil | 33.935 | 07/02/26 | 2,5 | sim (1,2 mil) |
| [Como a Rússia ficou tão grande? A resposta é um animal](https://youtu.be/wMFP6PadPmQ) | Além do Mapa | 2 mil | 28.400 | 07/10/26 | 14 | sim (2,7 mil) |
| [Este Video Vai Mudar Sua Visão… Russia](https://youtu.be/BF9AD91W2u4) | GeoDocs | 258 mil | 1.634.295 | 11/10/25 | 6,3 | sim (669 mil) |
| apoio en: [1500 Years of Russian History in 27 Minutes](https://youtu.be/pBJpDpMqigw) | Animated History | 102 mil | 1.265.775 | 12/06/26 | 12 | sim (555 mil) |
| apoio en: [The Entire History of Russia in 16 Minutes](https://youtu.be/vbfuDfw0_eA) | Historiq | 6,3 mil | 455.114 | 03/10/26 | 73 | sim (2,1 mil) |
Contra-sinal: Genius "The ENTIRE History of Russia in 23 Minutes" tinha 3,2 mil em 2 dias (abaixo do piso dele), e o HiM "Russia: The Biggest Country…" está na mediana. A Rússia em en já saturou; em pt, o clone levou o pico.

**O que entregamos de verdade**
- **00:13–00:25**, o pedido aos vikings: "Nossa terra é grande e rica, mas não há ordem nela. Venham reinar sobre nós." **00:27**: "Um condomínio contratando síndico viking."
- **00:45–00:56**, a pergunta (1º minuto): "como uma terra que precisou chamar estrangeiros para pôr ordem nela virou o maior país do mundo, e por que essa ordem sempre custou tão caro?"
- **01:10–01:17**, "uma planície enorme, sem montanha, sem muralha natural" (a 1ª pista da resposta).
- **05:53–06:12**, "a defesa que parecia funcionar era avançar até o próximo rio… quando você empurra a fronteira, ganha um vizinho novo."
- **07:01–07:22**, Sibéria: "Em mil seiscentos e trinta e nove, eles chegam ao oceano Pacífico: o norte da Ásia inteiro em menos de sessenta anos."
- **11:55**, "O inverno levou a fama, mas quem venceu foi a distância."
- **15:50–16:12**, "a bandeira vermelha desce do Kremlin… A Rússia continua sendo o maior país do mundo" / "grande e rica, mas sem ordem."
- O vídeo **termina em 1991** (não tem Putin): não prometer o presente.

**Proposta**
- **Título 1, "Pediram um rei viking. Como viraram o maior país do mundo?"** (58 caracteres). Padrão **T-C, ascensão "como virou o maior do mundo"**, com o 2º elemento-surpresa (o viking) na frente, como o "a resposta é um animal" do Além do Mapa. Refs: Pablo Soncini "Como se Tornou o Maior Império do Mundo?" 508 mil (23/11/25, sim) e Além do Mapa "Como a Rússia ficou tão grande?…" 28,4 mil (07/10/26, sim). Pago em 00:13–00:56 (pedido + pergunta) e nas 3 "peças da resposta" (05:49, 08:43, 15:23) até 16:18.
- **Título 2, "Dos vikings à bandeira vermelha: a Rússia INTEIRA em 17 minutos"** (63 caracteres). Padrão **T-E, recorte De A a B + fórmula**. Refs: HQ "Rússia: 1.200 Anos de Conquistas…" 203 mil (26/03/26, sim) e clone pt "Toda a história da Rússia em 37 minutos" 254 mil (19/10/26, sim) para a fórmula; também Pablo Soncini "(Da Fundação ao Império)" 508 mil. Pago em 00:19 (varegues) e 15:50 (bandeira vermelha desce do Kremlin). É diferente do clone (que não usa recorte) e não promete Putin.
- **Thumb, "TUDO ISSO?" (mapa gigante + viking pequeno, padrão H-2)**
  - Cena: à direita e no céu (~65% da arte), o mapa da Rússia aceso em vermelho-escuro com borda dourada brilhante, sem nomes nem letras, com 2–3 faixas de tom mostrando o avanço para leste (Moscou → Sibéria → Pacífico).
  - Embaixo, à esquerda (~40% da altura), o viking bonequinho de cabeça redonda (capacete, barba ruiva, o mesmo do 007) num barquinho no rio, olhando para cima de boca aberta e apontando o mapa. Fundo de céu de inverno ao entardecer (azul-noite e laranja), quente contra frio.
  - Texto: "TUDO ISSO?" em Libre Caslon 700 ouro, no canto superior esquerdo (o céu livre), + pílula amarela "862 → 1991".
  - Promete: o contraste entre um barco viking e 1/8 da Terra; a lacuna é o "como". Com o T1, o título diz o viking e a thumb mostra o tamanho, sem repetir "maior país". Com o T2, a thumb dá a escala que o título só nomeia.
  - Pagamento: 00:45–00:51 (pergunta), 07:12–07:18 (chegam ao Pacífico) e 15:59 (continua o maior país do mundo).
  - Refs de thumb: Além do Mapa "RÚSSIA GIGANTE. POR QUÊ?" 28,4 mil (sim) e Versed "NÃO É UM PAÍS" (mapa) 33,9 mil (sim); en: Ziro (mapa + figura) 367 mil (sim) e Animated History (mapa dividido + "HOW?") 1,27 mi (sim).
  - Dentro da bíblia: mapa-império aceso + bonequinho já é o 3º estilo aprovado (Irã v3). Base nova: 1 tomada nano-banana (~US$ 0,05) se o Rodrigo aprovar; aqui não foi gerada.
  - **Manter "UM VIKING NO TRONO?" (9,6%) como controle.** Ela casa com o T2; o T1 já fala do viking.

### 006 Roma · `fkltw3XwQ0E`
**Atual:** "A história INTEIRA de Roma em 17 minutos" · 45 impr · CTR 2,2% · retenção 61% (a melhor do canal) · thumb "ROMA HUMILHADA" + 390 a.C. É o caso típico da aula: retenção alta e CTR baixo, ou seja, a embalagem errou. Além disso, o título colide com o HEG (73 mil) e com o clone 10/2026b.

**Top referências**
| Vídeo | Canal | Inscritos | Views | Data | v/i | > mediana? |
|---|---|---|---|---|---|---|
| [O mito que resume a história de Roma](https://youtu.be/Mp8ATV9LLt8) | Estranha História | 1,27 mi | 587.039 | 12/08/26 | 0,46 | sim (341 mil) |
| [A História de Roma: Como se Tornou o Maior Império do Mundo?](https://youtu.be/XyX7Y-xyhyg) | Pablo Soncini | 33,4 mil | 507.584 | 23/11/25 | 15 | sim (2,4 mil) |
| [O Fim do Império Romano (476 d.C.)](https://youtu.be/RDmf1C7xXv0) | Arquivos do Velho Mundo | 3,3 mil | 432.072 | 15/04/26 | 133 | sim (476) |
| [753 a.C. Império Romano – Da Fundação à Queda…](https://youtu.be/sLyfGzpuIGY) | História do Mundo em HQ | 30 mil | 203.678 | 09/01/26 | 6,8 | sim (13,6 mil) |
| [A QUEDA DE ROMA: O DIA em Que o IMPÉRIO ROMANO Acabou de Vez!](https://youtu.be/cM9084oMpXc) | Histórias Romanas | 295 mil | 189.497 | 04/04/26 | 0,64 | sim (62 mil) |
| [A HISTÓRIA INTEIRA de Roma em 12 minutos](https://youtu.be/XyulPwDw1CE) | History Easy Guide | 3 mil | 73.304 | 28/10/26 | 25 | sim (5,5 mil) |
| [IMPÉRIO ROMANO: a história completa de como Roma conquistou o mundo e por que caiu](https://youtu.be/US27NANBd2g) | Epopeia | 2,3 mil | 30.430 | 05/11/26 | 13 | sim (20,9 mil) |
| apoio en: [The ENTIRE History of ROME in 12 Minutes](https://youtu.be/kHCamT4zfH4) | Genius History | 41,9 mil | 396.901 | 26/08/26 | 9,5 | sim (99 mil) |
Contra-sinal: HiM "Rome Never Really Fell" 21 mil, abaixo da mediana dele (44 mil). O "não caiu" de verdade não puxa; o que puxa é **queda** e **ascensão**.

**O que entregamos de verdade**
- **00:00–00:32**, Roma em chamas e o resgate: "Os gauleses topam ir embora… por mil libras de ouro" (00:16); Breno "joga em cima da balança e diz: ai dos vencidos" (00:25–00:32).
- **00:49–00:56**, a pergunta (1º minuto): "como uma cidade que pagou resgate aos bárbaros virou a dona do mundo e, oitocentos anos depois, virou a vencida?"
- **04:47–04:53**, a 1ª peça: "Roma não cresceu porque esmagava os vencidos. Cresceu porque fazia deles romanos."
- **05:57–06:14**, Aníbal: "atravessa os Alpes com um exército e dezenas de elefantes. Elefantes. Na neve."
- **09:41–09:56**, César no Rubicão: "a sorte está lançada."
- **15:27–15:44**, o pagamento do loop: "Então Roma faz o que tinha feito com Breno: paga resgate. Cinco mil libras de ouro, cinco vezes o de Breno… e três mil libras de pimenta."
- **15:45–16:00**, "os godos entram e saqueiam a cidade por três dias… foi tomada a cidade que tinha tomado o mundo inteiro."
- **16:20**, "E a cidade do ai dos vencidos agora era a vencida."

**Proposta**
- **Título 1, "Roma pagou resgate aos bárbaros. Como virou dona do mundo?"** (58 caracteres). Padrão **T-C, ascensão**, aberto com o fato paradoxal (= pergunta central do roteiro). Refs: Pablo Soncini "Como se Tornou o Maior Império do Mundo?" 508 mil (23/11/25, sim) e Epopeia "…como Roma conquistou o mundo e por que caiu" 30,4 mil (05/11/26, sim). Pago em 00:16–00:56 (resgate + pergunta) e 04:47–04:53 (a 1ª peça da resposta).
- **Título 2, "A cidade que tomou o mundo foi tomada: como Roma caiu?"** (54 caracteres). Padrão **T-D, queda/perda**. Refs: Histórias Romanas "A QUEDA DE ROMA: O DIA em Que o IMPÉRIO ROMANO Acabou de Vez!" 189 mil (04/04/26, sim) e Arquivos do Velho Mundo "O Fim do Império Romano (476 d.C.)" 432 mil (15/04/26, sim); também Mundos Reimaginados "Como o Maior Império do Mundo Desmoronou" 484 mil. A frase vem da própria narração (São Jerônimo, 16:00). A pergunta é feita aos 00:49–00:56 e paga em 15:27–16:24. **Atenção:** a queda ocupa só os 2 últimos minutos. Quem vem pela queda precisa ser segurado pelo loop do 1º minuto ("virou a vencida?"). Risco de retenção menor que no T1: medir.
- **Thumb, "DE NOVO?" (personagem com emoção + objeto do loop, padrão H-3, quente e escuro)**
  - Cena: em primeiro plano, à esquerda (~55% da altura), um senador romano bonequinho de cabeça redonda (toga branca com faixa vermelha, coroa de louros torta), olhos marejados e boca tremendo, empurrando sacos de ouro e um saco de pimenta para o prato de uma **balança de bronze** (o objeto-símbolo do vídeo).
  - À direita, atrás, a silhueta de um rei godo bonequinho de braços cruzados, rindo, e Roma ao entardecer com fumaça laranja sobre o Coliseu e os telhados. Sem fogo em pessoas, sem corpos, sem sangue.
  - Texto: "DE NOVO?" em Libre Caslon 700 (ouro, contorno preto) no canto superior direito, + pílula amarela "390 a.C. → 410".
  - Promete: Roma pagando resgate pela 2ª vez. A lacuna é a 1ª vez e como a dona do mundo voltou a isso. Com o T1, a thumb mostra a balança do resgate e pergunta "de novo?", que leva ao fim. Com o T2, mostra a cidade tomada, mas não diz como.
  - Pagamento: 00:16–00:32 (1º resgate, 1º minuto) e 15:33–15:37 ("Então Roma faz o que tinha feito com Breno: paga resgate").
  - Refs de thumb: Histórias Romanas "O FIM DE ROMA" (imperador abatido, ruínas, tempestade) 189 mil (sim) e HEG "1 TIRO E O MUNDO EXPLODIU" (bonequinho espantado, quente) 237 mil (sim); en: Historically (bonequinho de cabeça redonda chorando) 10,7 mi (sim).
  - **Por que trocar a atual:** "ROMA HUMILHADA" mostra o fato do 1º minuto **sem lacuna** (ela já responde), de dia e clara, como as Epopeia/HEG que ficam perto da mediana; a 320 px os bonecos viram manchas (gap §3). "DE NOVO?" deixa a pergunta aberta e é escura/quente como os hits de Roma. Base nova: 1 tomada (~US$ 0,05), não gerada.

---

## 3. Checagem das regras duras (todas as 6 propostas e as 3 thumbs)
- ≤ 100 caracteres: 47, 61, 58, 63, 58, 54. Sem morte/morreu/morto/assassinado/massacre/chacina/chocante/perturbador; thumbs sem sangue, cadáver ou caveira.
- "em N minutos" só nos dois títulos T-E (fórmula A da bíblia), com N = duração real (Irã 17:59 → 18; Rússia 16:45 → 17).
- Nenhum é cópia literal: o T-B do Irã acrescenta "nunca virou árabe"; os T-E usam pontas que nenhum título pt usa; nenhuma thumb usa líder atual + fogo (molde dos clones).
- Thumbs com ≤ 2 palavras + pílula de datas, 1 foco cada. A legibilidade a 320 px precisa ser conferida na composição. A do Irã pode ser composta já, com custo zero.
- Bíblia: bonequinhos de cabeça redonda nas 3. Nenhum desvio.

## 4. Lições para os próximos vídeos do canal (Hipótese, com a evidência acima)
1. **Pergunta crua de tema é commodity em pt:** "Como a Pérsia virou Irã?" e "Como a Rússia ficou tão grande?" têm cópias com 1–300 views. O que rende traz um **2º elemento-surpresa** no título ("a resposta é um animal"; aqui, "nunca virou árabe", "pediram um rei viking", "pagou resgate").
2. **A pergunta central do roteiro v2 já é um título pronto** (Roma e Rússia): use-a encurtada como braço principal e deixe a fórmula como braço com recorte "De A a B".
3. **Thumb com lacuna, não com resposta:** "ROMA HUMILHADA" (2,2%) responde; "UM VIKING NO TRONO?" (9,6%) pergunta. A amostra é pequena, mas bate com H-1 a H-3.
4. **Antes × depois e mapa gigante** são os 2 moldes de thumb com mais prova no nicho pt fora do molde dos clones (líder atual + fogo). Os dois cabem nos bonequinhos.
