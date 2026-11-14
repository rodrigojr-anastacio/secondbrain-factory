# Reembalagem historia-ptbr (pesquisador A): Egito, Índia, China, Brasil (14/11/2026)

Base: yt-dlp via WARP (106 buscas, 0 cota) + Data API só leitura (`videos.list`, `channels.list`, `playlistItems`: ~190 unidades; **0 `search.list`**). Medianas: últimos ≤ 30 uploads longos (> 3 min, ≥ 3 dias) de cada canal. Janela das referências: ≤ 400 dias. Dados em `dados/historia-ptbr/A-*` (`A-refs.csv` = tabela-mestre com link, inscritos, views, data, v/i, mediana e "acima?"). Mosaicos: `mosaicos/historia-ptbr-00N-<tema>.jpg` (1º quadro amarelo = a nossa thumb no ar; azul = acima da mediana do canal; cinza = não).
**[O]** observado · **[I]** inferido · **Hipótese** = sem medição.

## 0. Leitura curta
- **[O] O título atual é o dos clones.** O nosso "A história INTEIRA do Brasil em 17 minutos" é idêntico ao do História Inteira (`WcXwgbvbKMY`). A thumb do Brasil também é praticamente a mesma: Pedro I + baía do Rio + "BRASIL 1500–2026" (`mosaicos/historia-ptbr-005-brasil.jpg`, último quadro). Egito, China e Índia usam o painel claro "NOME + ANO–2026" do HiM/Genius. Em pt, os hits do tema usam **luz quente, personagem grande (50–70% da altura) e 2–3 palavras**.
- **[O] A demanda pt destes 4 temas no molde "história inteira" é baixa.** O clone pt de 08/2026 fez 2,7 mil (Egito) e 4,1 mil (Índia); o HEG fez 5,2 mil no Egito. Os grandes em pt são de recorte: queda do Egito 1,45 mi; Ditadura 2,2 mi; família real 773 mil; a tumba de Qin 755 mil. **[I]** A embalagem nova pode subir o CTR, mas o teto de impressões continua sendo do tema.
- **Proposta de sistema:** o braço A de todo vídeo vira **"N ANOS de X em N minutos"**. Ele tem evidência em pt, mantém o "em N minutos" da bíblia e deixa de ser idêntico aos clones. O braço B é um título de tensão ancorado num fato do 1º minuto. A thumb é de bonequinho, com luz quente e 1 foco.
  - **Desvio da bíblia** (`titulo.md`, fórmula "A história INTEIRA de X em N minutos"): troco "A história INTEIRA de X" por "N ANOS de X", mantendo "em N minutos" e a palavra de destaque em caixa alta. Motivo: o gap 2 mostrou o título idêntico ao de 10+ canais pt, e o padrão "N anos em N minutos" tem 3 hits pt acima da mediana (§1).

## 1. Padrões do nicho (pt, história; en como apoio)
Comprimento: mediana de **57 caracteres** antes do "|" nos 43 títulos pt acima da mediana. 21 de 43 têm número, 10 são pergunta e 14 têm uma palavra em CAIXA ALTA. [O]

### Títulos
| # | Padrão | Exemplos reais (views · data · acima da mediana do canal?) | Gatilho |
|---|---|---|---|
| T1 | **"N mil anos (de X) em N minutos"** | [Histórias Épicas da Bíblia "6000 Anos em 30 Minutos: A História da Bíblia Completa"](https://youtu.be/HCzD29KIlo4) 1,97 mi · 13/12/2025 · sim (med. 358 mil) · [Atlas das Eras "3.000 Anos em 25 Minutos: Toda a História do Egito Antigo"](https://youtu.be/alBh1Urra80) 70 mil em 9 dias · 05/11/2026 · sim (med. 281) · [ElHistorian "IDADE MÉDIA: 1000 ANOS EM 78 MINUTOS"](https://youtu.be/52TY3RdXIaM) 33,6 mil · 07/11/2026 · sim (med. 949) · en: [Animated History "4000 Years of Chinese History in 25 Minutes"](https://youtu.be/wuhnBi8jNl0) 1,2 mi · sim | escala + custo baixo (decisão do clique: "pouco em jogo"). Contra-exemplo: Canal Nostalgia "CHINA / 5 MIL ANOS DE HISTÓRIA EM 1 HORA" 1,43 mi, **abaixo** da mediana dele (1,54 mi) |
| T2 | **"Por que + fato contraintuitivo/proibido?"** | [Fatos Desconhecidos "Por que nunca entramos na maior tumba da Terra?"](https://youtu.be/NCr1f_SUsLk) 755 mil · 01/03/2026 · sim (244 mil) · [Reconstrutória "Por que você não sobreviveria 24 horas no Egito Antigo…"](https://youtu.be/7MDyiuw9wYI) 664 mil · 07/03 · sim (6,9 mil) · [Soldado Preto e Branco "Por que Hollywood PROIBIU a história do Brasil na 2ª Guerra?"](https://youtu.be/RH30MX3g5Rg) 548 mil · 12/01 · sim (1,2 mil) · [Mente Primata "Por que 300 mil anos quase nada mudou…"](https://youtu.be/kZ3YWuGWF0k) 396 mil · 04/10 · sim (994) · [História do Mundo "Por Que China e Japão São Tão Rivais?"](https://youtu.be/tzfbDkQx7Hw) 258 mil · 04/07 · sim · [Histórias Romanas "POR QUE ROMA NUNCA CONQUISTOU A ÍNDIA?"](https://youtu.be/guiOxLd8X3M) 127 mil · 04/05 · sim (62 mil) | lacuna. Contra-exemplos: Estranha História "Por que o Sudão tem mais pirâmides…" 301 mil e Capital Financeiro 273 mil (os dois abaixo da mediana) |
| T3 | **"Como [algo concreto] [construiu/tornou] [X]"** | [Mundos Reimaginados "O Império do Café: Como o Grão Construiu o Brasil Moderno"](https://youtu.be/p0t7j7ish_E) 548 mil · 02/04 · sim (116 mil) · [Pablo Soncini "A História de Roma: Como se Tornou o Maior Império do Mundo?"](https://youtu.be/XyX7Y-xyhyg) 508 mil · 23/11/2025 · sim (2,4 mil) · [O Diário de Titus Valério "Como Começou a Ditadura Militar no Brasil?"](https://youtu.be/UfGD0lqHObI) 2,2 mi · 04/08 · sim (65 mil) · en (origem): HiM "How Water Decided Who Ruled China…" 57,6 mil (= mediana, não conta) | causa escondida |
| T4 | **"O Dia em que + fato improvável"** | [Mundos Reimaginados "O Dia em que o Povo Venceu o Império…"](https://youtu.be/QTjecFwrzbs) 1,01 mi · 24/04 · sim · [Mundos Reimaginados "O Dia em que Portugal se Mudou para o Brasil"](https://youtu.be/qWPL11MOzOg) 773 mil · 16/03 · sim · [Toda História em Minutos "O Dia em Que o Brasil Acordou Império e Dormiu República"](https://youtu.be/CExWqlfYHkU) 1,3 mil · 04/10 · sim (244; v/i 52) | cena única |
| T5 | **Afirmação estranha + virada/pergunta** | [Por Quê, Hein? "A China Esteve na Frente por 700 Anos. Então Por Que a Grã-Bretanha se Industrializou Primeiro?"](https://youtu.be/As5HdY_D-uI) 77 mil · 19/10 · sim (49 mil) · [Mente Primata "Por que 300 mil anos quase nada mudou. Aí, há uns 10 mil anos, tudo disparou. Por quê?"](https://youtu.be/kZ3YWuGWF0k) 396 mil · sim · [Passado Implacável "DOM PEDRO II foi Expulso do Brasil em uma Única Noite…"](https://youtu.be/iCiM_67Vj7w) 108 mil · 07/05 · sim (460) | contraste |
| T6 | "A Queda / O Fim de X" | [Um Documentário "A QUEDA DO ANTIGO EGITO…"](https://youtu.be/apCvzsTn1qY) 1,45 mi · sim (837 mil) · [História do Mundo "O Fim do Antigo Egito…"](https://youtu.be/dPfV5_tDCzo) 376 mil · sim · [Pelas Mãos do Tempo "A Queda do Antigo Egito…"](https://youtu.be/VCnluiYBm70) 153 mil · sim | perda. **Não usar no Egito:** o nosso vídeo é sobre sobreviver, não sobre a queda |
| T7 | Fórmula "história COMPLETA/INTEIRA em N min" (+ recorte "Dos A a B") | [Histórias Milenares "EGITO ANTIGO: A História Completa em 20 Minutos \| Dos Faraós a Cleópatra"](https://youtu.be/GPt6u5mj74E) 439 mil · sim · [Reconstrutória "A História COMPLETA do Egito Antigo em 15 Minutos"](https://youtu.be/nqX6vUmUNkA) 397 mil · sim · [Crônicas de Ferro "Toda a história do Irã em 20 minutos"](https://youtu.be/uEDDMWJ04Vo) 1,48 mi · sim | é a nossa atual; **saturada por clones** (História Inteira, HEG, 5+ "História em Minutos") |

A evitar [O]: os títulos-isca dos concorrentes ("Tumba de Qin Shi Huang **foi aberta** após mil anos", que é falso; "o que descobriu mudou tudo") e as palavras proibidas ("chocante" etc.). A moldura "sobreviveu a todos os impérios" flopou em 2 canais (clone "Como o Egito perdeu tudo (mas sobreviveu a todos os impérios)?", 11 views; HiM "Korea Survived Every Empire…", 1,4 mil).

### Thumbs
| # | Padrão | Exemplos reais (acima da mediana) | Como conversa com o título |
|---|---|---|---|
| TH-A | **Personagem grande (50–70% da altura) + monumento ao entardecer (ouro/laranja) + 2–3 palavras douradas** | Histórias Milenares Egito 439 mil ("EGITO / DA ORIGEM À QUEDA", faraó + Cleópatra) · História do Mundo 376 mil ("FIM DO EGITO") · História do Mundo 240 mil ("EGITO DE CLEÓPATRA", rosto em close) · Pelas Mãos do Tempo 153 mil ("A QUEDA DO EGITO") · Atlas das Eras 70 mil ("3.000 ANOS EM 15 MINUTOS") · Foca na História 51 mil ("GRANDES DINASTIAS CHINESAS") | a palavra da arte é o ângulo; o título dá o tema |
| TH-B | **Ano gigante como herói + personagem/cena** | Mundos Reimaginados 773 mil ("1808 RIO DE JANEIRO") e 1,01 mi ("1835: CABANAGEM") · Titus Valério 2,2 mi ("DITADURA MILITAR 1964–1985") · Além da História 49 mil ("DESCOBERTA DO BRASIL 1500–1600") | data concreta = cena única |
| TH-C | **Pergunta curta em caixa alta + personagem/cena** | Histórias Romanas 127 mil ("POR QUE ROMA PAROU AQUI?") · Por Quê, Hein? 77 mil ("POR QUE NÃO CHINA?", **bonequinhos de cabeça redonda iguais aos nossos**) · en: Animated History 1,2 mi ("HOW?") | a thumb pergunta; o título dá o contexto |
| TH-D | **Mistério: porta/tumba fechada + figura pequena com medo + frase de alerta, fundo escuro** | Fatos Desconhecidos 755 mil (porta de bronze + "OS ARQUEÓLOGOS ESTÃO COM MEDO!") · Vestígios Ocultos 54 mil (tumba de Qin; texto com palavra proibida) | lacuna pura |
| TH-E | **Duelo/split A × B (dois lados, dois tempos)** | História do Mundo 258 mil ("CHINA VS JAPÃO", 2 guerreiros cara a cara) · Por Quê, Hein? 77 mil (bonecos chineses × britânicos) · Titus Valério 2,2 mi (2 rostos + bandeira) · en: Animated History 1,2 mi ("221BC \| 2026", Qin × Xi) | conflito com zero processamento (é o nosso COROA × TURBANTE) |
| TH-F | Painel claro "NOME + ANO–2026" + figura em pé (HiM/Genius) | Genius China 553 mil, HiM Índia 641 mil (en, sim) | em pt, **clones idênticos** (História Inteira, HEG, clone 08/2026): é a nossa atual e não se distingue |

## 2. Por vídeo

### 001 Egito: "A história INTEIRA do Egito em 17 minutos"
**2.826 impressões · CTR 5,8% · retenção 46%** (17:01) · mosaico `mosaicos/historia-ptbr-001-egito.jpg`

| Referência | Canal | Inscr. | Views | Data | v/i | > mediana? |
|---|---|---|---|---|---|---|
| [apCvzsTn1qY](https://youtu.be/apCvzsTn1qY) A QUEDA DO ANTIGO EGITO | Um Documentário | 131 mil | 1,45 mi | 04/07/26 | 11,0 | sim (837 mil) |
| [7MDyiuw9wYI](https://youtu.be/7MDyiuw9wYI) Por que você não sobreviveria… | Reconstrutória | 15 mil | 664 mil | 07/03/26 | 44,2 | sim (6,9 mil) |
| [yvWJVYTlIK0](https://youtu.be/yvWJVYTlIK0) A História do EGITO é muito mais ESTRANHA… | Cortes Sabedoria | 129 mil | 575 mil | 23/08/26 | 4,5 | sim (89 mil) |
| [GPt6u5mj74E](https://youtu.be/GPt6u5mj74E) …Completa em 20 Minutos \| Dos Faraós a Cleópatra | Histórias Milenares | 69,7 mil | 439 mil | 03/05/26 | 6,3 | sim (41 mil) |
| [nqX6vUmUNkA](https://youtu.be/nqX6vUmUNkA) A História COMPLETA do Egito Antigo em 15 Minutos | Reconstrutória | 15 mil | 397 mil | 05/04/26 | 26,5 | sim |
| [dPfV5_tDCzo](https://youtu.be/dPfV5_tDCzo) O Fim do Antigo Egito | História do Mundo | 17,8 mil | 376 mil | 17/05/26 | 21,1 | sim (18 mil) |
| [1LImwJdMRaA](https://youtu.be/1LImwJdMRaA) Egito de Cleópatra | História do Mundo | 17,8 mil | 240 mil | 16/09/26 | 13,5 | sim |
| [alBh1Urra80](https://youtu.be/alBh1Urra80) 3.000 Anos em 25 Minutos… | Atlas das Eras | 635 | 70 mil | 05/11/26 | 110 | sim (281) |
| [y_JlppsyFok](https://youtu.be/y_JlppsyFok) Toda a história completa do Egito em 39 min | clone pt 08/2026 | 5,6 mil | 2,7 mil | 13/10/26 | 0,5 | sim (2,4 mil) |
| en [VQPzrVMHWlg](https://youtu.be/VQPzrVMHWlg) The ENTIRE History of Egypt in 17 Minutes | History in Minutes | 20,5 mil | 571 mil | 11/09/26 | 27,9 | sim (58 mil) |

**O que o vídeo entrega (legendas.srt conferida):**
- 0:00 "O Egito não é um país que tem um rio. É um rio com um país em volta."
- **0:16** "Cleópatra viveu mais perto do iPhone do que dos homens que ergueram a Grande Pirâmide."
- **0:32–0:41** "como um país invadido por persas, gregos, romanos, árabes, turcos e britânicos continuou sendo o Egito? / Em menos de vinte minutos, sete mil anos."
- 3:56–4:07 Grande Pirâmide, "por volta de 2560 antes de Cristo… Cento e quarenta e seis metros".
- 4:14–4:30 sem escravos chicoteados: "equipes pagas em pão e cerveja… 'os Bêbados de Miquerinos'".
- 8:24 "É a primeira greve registrada da história."
- 10:10 "Em 30 antes de Cristo, Otaviano venceu, Cleópatra morreu…"
- 15:56–16:00 "O maior medo do Egito hoje não é um exército. / É uma represa." (loop aberto aos 0:44)

**Proposta**
- **Título 1, padrão T1 ("N anos em N minutos"):** **"7.000 ANOS de Egito em 17 minutos"** (33 caracteres). Referências: Atlas das Eras, "3.000 Anos em 25 Minutos: Toda a História do Egito Antigo" (70 mil, 05/11/2026, acima da mediana); Histórias Épicas da Bíblia, "6000 Anos em 30 Minutos…" (1,97 mi, 13/12/2025, acima). É pago aos **0:41** ("sete mil anos" em menos de vinte minutos). Não copia o clone.
- **Título 2, padrão T2 ("Por que + fato contraintuitivo"):** **"Por que Cleópatra viveu mais perto do iPhone que das PIRÂMIDES?"** (63 caracteres). Referências: Fatos Desconhecidos, "Por que nunca entramos na maior tumba da Terra?" (755 mil, 01/03/2026, acima); Reconstrutória, "Por que você não sobreviveria 24 horas no Egito Antigo…" (664 mil, 07/03/2026, acima). A promessa é dita aos **0:16** e provada pela linha do tempo do vídeo: pirâmide aos 3:56 (2560 a.C.), Cleópatra aos 10:10 (30 a.C.). Cleópatra e as pirâmides são atalhos conhecidos ("pouco conhecimento prévio").
- **Thumb, padrão TH-A (personagem grande ao entardecer + 2–3 palavras):**
  - Cena: Cleópatra em bonequinho de cabeça redonda (franja preta, coroa de ouro com a naja, delineado), do peito para cima, à **direita** (~60% da altura). Ela olha por cima do ombro, boca aberta de espanto.
  - Fundo: à esquerda, a Grande Pirâmide **gasta**, com a Esfinge meio enterrada na areia, ao pôr do sol (ouro e laranja, céu violeta).
  - Texto: pílula amarela no topo "2560 a.C. · 30 a.C."; embaixo à esquerda, "**JÁ ERA ANTIGA**" em Libre Caslon (JÁ ERA em ouro, ANTIGA em branco) sobre degradê escuro.
  - Promessa: para a própria Cleópatra, a pirâmide já era uma antiguidade (lacuna de tempo).
  - Com os títulos: com o T1, a thumb mostra **por que** 7.000 anos é muito; com o T2, ela mostra só a metade "pirâmide" da comparação, sem repetir "iPhone". Os dois juntos criam a pergunta "como assim?".
  - Pago aos 0:16 e aos 3:56/10:10.
  - Referências de thumb (TH-A): História do Mundo "EGITO DE CLEÓPATRA" (240 mil, 16/09/2026, acima); Histórias Milenares "EGITO / DA ORIGEM À QUEDA" (439 mil, 03/05/2026, acima); Pelas Mãos do Tempo "A QUEDA DO EGITO" (153 mil, acima).
  - Bíblia: bonequinho mantido; a luz quente é a correção do gap 3 (não fere a bíblia).

### 002 Índia: "A HISTÓRIA COMPLETA da Índia em 19 minutos"
**2.281 impressões · CTR 4,3% · retenção 41%** (19:28) · mosaico `mosaicos/historia-ptbr-002-india.jpg`

| Referência | Canal | Inscr. | Views | Data | v/i | > mediana? |
|---|---|---|---|---|---|---|
| [z4FQoGlOKUQ](https://youtu.be/z4FQoGlOKUQ) HINDUÍSMO: A Religião Mais Antiga do Mundo | Zodiaco | 40,3 mil | 238 mil | 13/09/26 | 5,9 | sim (22 mil) |
| [guiOxLd8X3M](https://youtu.be/guiOxLd8X3M) POR QUE ROMA NUNCA CONQUISTOU A ÍNDIA? | Histórias Romanas | 295 mil | 127 mil | 04/05/26 | 0,43 | sim (62 mil) |
| [CMMgNPVqU5k](https://youtu.be/CMMgNPVqU5k) Índia: 5000 Anos de História… | História do Mundo em HQ | 30 mil | 39,7 mil | 12/02/26 | 1,3 | sim (15 mil) |
| [DKsoFxY3evU](https://youtu.be/DKsoFxY3evU) Por que o Mapa da Índia está Errado? | EconoSimples | 247 mil | 38,5 mil | 07/12/25 | 0,16 | sim (37 mil) |
| [088WI1DJHac](https://youtu.be/088WI1DJHac) Como surgiu a Primeira MULTINACIONAL… | Curioso Mercado | 469 mil | 20,7 mil | 26/08/26 | 0,04 | sim (13 mil) |
| [zMemC8hSMO8](https://youtu.be/zMemC8hSMO8) Índia: Da Civilização do Indo à Potência Global | Atlas de Impérios e Civilizações | 5,7 mil | 5,7 mil | 30/05/26 | 1,0 | sim (1,9 mil) |
| [aTMlPlcAzns](https://youtu.be/aTMlPlcAzns) Toda a história completa da Índia em 28 min | clone pt 08/2026 | 5,6 mil | 4,1 mil | 09/10/26 | 0,7 | sim |
| en [p9IIGdg91fE](https://youtu.be/p9IIGdg91fE) The ENTIRE History of India, From Harappa to Today… | History in Minutes | 20,5 mil | 641 mil | 30/09/26 | 31,3 | sim |
| en [lsnVzqwSjtk](https://youtu.be/lsnVzqwSjtk) Why IS India Like That? | Volksgeist | 931 mil | 1,24 mi | 19/09/26 | 1,3 | sim (1,23 mi) |
| en [3zHMKPpSHWA](https://youtu.be/3zHMKPpSHWA) How did the British Colonize India? (bonecos) | Barely Accurate | 25 mil | 579 mil | 12/02/26 | 23 | = mediana |

[O] Em pt, quase não há "história da Índia" que rode: os que rodam são recorte (religião, Roma × Índia, mapa). É o tema com menos prova pt dos 4.

**O que o vídeo entrega:**
- **0:23–0:44** "No meio do caminho, chegou um vento… / A Índia não é um país que tem uma monção. / A Índia é uma monção que fez crescer um país."
- 1:52 "De uma batalha decidida por uma tempestade, de uma empresa com exército próprio…"; 2:06 "…e de um vento que decidia quem governava."
- 3:16–3:27 dentistas de Mehrgarh, "a odontologia mais antiga conhecida".
- 4:10–4:30 tijolos de Harappa viraram lastro de ferrovia: "Uma das cidades mais antigas da Ásia foi parar debaixo dos trens."
- 7:23–7:33 o zero: "A Índia fez do nada um número."
- 10:00 "A Índia foi construída em volta de um vento." / 10:23 "Monção boa enchia o tesouro. Monção ruim esvaziava."
- **10:52–11:14** Plassey: "caiu uma tempestade de monção… Os britânicos cobriram a pólvora com lonas. Os artilheiros do nababo, não… Uma empresa tinha acabado de tomar Bengala."
- 12:19–12:26 o Koh-i-Noor "está numa coroa britânica, na Torre de Londres".

**Proposta**
- **Título 1, padrão T1:** **"5.000 ANOS de Índia em 19 minutos"** (33 caracteres). Referências: Histórias Épicas da Bíblia, "6000 Anos em 30 Minutos…" (1,97 mi, acima); ElHistorian, "IDADE MÉDIA: 1000 ANOS EM 78 MINUTOS" (33,6 mil, 07/11/2026, acima). Os dois canais pt de Índia que rodaram acima da mediana também usam "5000 Anos" (HQ 39,7 mil; Atlas 5,7 mil). É pago aos 3:38 (cidades do Indo, 3300 a.C.) até 17:28 (hoje).
- **Título 2, padrão T3 ("Como [algo concreto] construiu/decidiu X"):** **"Como um VENTO decidiu quem mandava na Índia"** (43 caracteres). Referências: Mundos Reimaginados, "O Império do Café: Como o Grão Construiu o Brasil Moderno" (548 mil, 02/04/2026, acima); Pablo Soncini, "A História de Roma: Como se Tornou o Maior Império do Mundo?" (508 mil, 23/11/2025, acima). É pago no **1º minuto** (0:23–0:44), retomado aos 2:06 e aos 10:00–10:30, com a prova aos 10:52 (Plassey). É a tese do roteiro, não isca.
- **Thumb, padrão TH-E (duelo, o nosso conflito cara a cara COROA × TURBANTE):**
  - Cena: à esquerda, o bonequinho Robert Clive (casaca vermelha, tricórnio), sorriso de canto, seco debaixo de uma lona esticada sobre os canhões. À direita, o artilheiro do nababo (turbante), boca aberta de raiva, encharcado, com o canhão pingando e soltando fumacinha molhada. Os dois do peito para cima, testa contra testa.
  - Céu: a nuvem de monção, preta e gigante, despeja chuva **só no lado direito**; o raio amarelo do template fica no meio.
  - Texto: pílula "1757" no topo; embaixo, "**CHUVA × CANHÃO**" (CHUVA em ouro, × e CANHÃO em branco).
  - Promessa: uma batalha decidida pelo tempo.
  - Com os títulos: com o T2, ela é a prova concreta do "vento" sem repetir a palavra; com o T1, ela é a cena-isca dentro dos 5.000 anos.
  - Pago aos 1:52 (anúncio) e aos 10:52–11:14.
  - Referências (TH-E): História do Mundo "CHINA VS JAPÃO" (258 mil, 04/07/2026, acima); Por Quê, Hein? (bonecos China × Grã-Bretanha, 77 mil, 19/10/2026, acima). A Barely Accurate (redcoats × turbantes em bonecos, 579 mil) bate na mediana e entra só como imagem de apoio.
  - Sem sangue nem feridos: o canhão só "falha".

### 004 China: "A história INTEIRA da China em 16 minutos"
**691 impressões · CTR 6,1% · retenção 38%** (16:15) · mosaico `mosaicos/historia-ptbr-004-china.jpg`

| Referência | Canal | Inscr. | Views | Data | v/i | > mediana? |
|---|---|---|---|---|---|---|
| [NCr1f_SUsLk](https://youtu.be/NCr1f_SUsLk) Por que nunca entramos na maior tumba da Terra? (Qin) | Fatos Desconhecidos | 23 mi | 755 mil | 01/03/26 | 0,03 | sim (244 mil) |
| [SYsIldcDB_w](https://youtu.be/SYsIldcDB_w) Albert Lin digitalizou o Exército de Terracota… | Além do Véu Cósmico | 1,4 mil | 287 mil | 28/10/26 | 206 | sim (1 mil); thumb com "chocante" |
| [tzfbDkQx7Hw](https://youtu.be/tzfbDkQx7Hw) Por Que China e Japão São Tão Rivais? | História do Mundo | 11,4 mil | 258 mil | 04/07/26 | 22,6 | sim (740) |
| [As5HdY_D-uI](https://youtu.be/As5HdY_D-uI) A China Esteve na Frente por 700 Anos. Então Por Que… | Por Quê, Hein? | 14,5 mil | 77 mil | 19/10/26 | 5,3 | sim (49 mil) |
| [78iv9U6GV6c](https://youtu.be/78iv9U6GV6c) Tumba de Qin Shi Huang foi aberta… (falso) | Vestígios Ocultos | 10,3 mil | 54 mil | 06/03/26 | 5,3 | sim (13 mil) |
| [12n3uoyIbvQ](https://youtu.be/12n3uoyIbvQ) A História das GRANDES DINASTIAS da China | Foca na História | 1,51 mi | 51 mil | 02/05/26 | 0,03 | sim (5,2 mil) |
| [GSFdoWs0NYo](https://youtu.be/GSFdoWs0NYo) …Têm Medo de Abrir o Mausoléu de Qin | Vodar | 95,5 mil | 50 mil | 17/10/26 | 0,5 | não (212 mil) |
| [deEXaVt3EgE](https://youtu.be/deEXaVt3EgE) CHINA / 5 MIL ANOS DE HISTÓRIA EM 1 HORA | Canal Nostalgia | 15,2 mi | 1,43 mi | 17/10/26 | 0,09 | não (1,54 mi) |
| en [wuhnBi8jNl0](https://youtu.be/wuhnBi8jNl0) 4000 Years of Chinese History in 25 Minutes | Animated History | 102 mil | 1,2 mi | 28/08/26 | 11,8 | sim (555 mil) |
| en [Fbz4QYZ5XrI](https://youtu.be/Fbz4QYZ5XrI) The ENTIRE History of China in 20 Minutes | Genius History | 41,9 mil | 553 mil | 06/10/26 | 13,2 | sim (104 mil) |
| en [fXuWQg7uJKg](https://youtu.be/fXuWQg7uJKg) The ENTIRE History of CHINA [No AI] (cartum de cabeça redonda) | Historically | 1,65 mi | 9,06 mi | 03/09/26 | 5,5 | sim |

[O] O túmulo de Qin é o recorte chinês que mais roda em pt (755 mil). É exatamente o loop do nosso hook.

**O que o vídeo entrega:**
- **0:00–0:26** "O homem mais poderoso da Terra está morrendo… e ele tem um plano para não morrer… viver para sempre… pílulas… de mercúrio."
- **0:35** "E o túmulo dele, guardado por um exército de barro… ninguém abriu até hoje."
- 0:45 "o país que morreu mais vezes do que qualquer outro… e sempre voltou."
- 2:59–3:27 o Mandato do Céu: "todo mundo usou essa brecha, por três mil anos".
- **4:53–5:07** "um túmulo que… tinha rios de mercúrio. / E isso pode não ser lenda: o solo em cima tem mercúrio muito acima do normal. / O exército de barro só apareceu em 1974."
- 7:31–7:36 Wu Zetian, "a única mulher a fazer isso na história da China".
- 13:24–13:28 "Era Puyi. / O último Filho do Céu agora era jardineiro."
- **15:20–15:30** "E aquele túmulo? Continua fechado. / Os arqueólogos preferem esperar: ninguém sabe preservar o que tem lá dentro… e tem o mercúrio."

**Proposta**
- **Título 1, padrão T1:** **"3.000 ANOS de China em 16 minutos"** (33 caracteres). Referências: Histórias Épicas da Bíblia, "6000 Anos em 30 Minutos…" (1,97 mi, acima); Atlas das Eras, "3.000 Anos em 25 Minutos…" (70 mil, 05/11/2026, acima); apoio en: Animated History "4000 Years of Chinese History in 25 Minutes" (1,2 mi, acima). É pago aos 3:27 e aos 15:55 ("três mil anos"). Não é o "5 MIL ANOS EM 1 HORA" do Canal Nostalgia (número, duração e ordem diferentes).
- **Título 2, padrão T2:** **"Por que NINGUÉM abriu o túmulo do 1º imperador da China?"** (55 caracteres). Referências: Fatos Desconhecidos, "Por que nunca entramos na maior tumba da Terra?" (755 mil, 01/03/2026, acima; mesmo assunto, frase diferente); Soldado Preto e Branco, "Por que Hollywood PROIBIU…" (548 mil, 12/01/2026, acima). É pago aos **0:35** (pergunta), aos 4:53–5:07 (mercúrio) e aos 15:20–15:30 (resposta). O loop cruza o vídeo inteiro: ajuda a retenção, não a derruba.
- **Thumb, padrão TH-C (pergunta curta + personagem):**
  - Cena: o bonequinho Qin Shi Huang (coroa de contas, barba), do peito para cima, à esquerda (~60%), suando de medo. Na mão estendida, uma **esfera prateada brilhante** de mercúrio. Atrás dele, o exército de terracota na penumbra, com luz de tocha laranja.
  - Texto: "**IMORTAL?**" em ouro no canto livre da direita, embaixo; pílula "210 a.C." no topo.
  - Promessa: o homem que quis viver para sempre.
  - Com os títulos: com o T2, o túmulo **é dele**, o que dá uma 2ª lacuna (o que tem lá dentro?), sem repetir "túmulo"; com o T1, é o rosto-isca da China.
  - Pago aos **0:03–0:26**.
  - A base já existe: `videos/004-china/entrega/thumbs-v2/thumb-4-bonecos.jpg` (custo zero; só conferir que é a que vai no "Testar e comparar").
  - Referências (TH-C): Histórias Romanas "POR QUE ROMA PAROU AQUI?" (127 mil, 04/05/2026, acima); Por Quê, Hein? "POR QUE NÃO CHINA?" (bonecos, 77 mil, 19/10/2026, acima).
  - Alternativa com mais prova de tema, para o 3º braço: TH-D, a porta (`thumb-6-tumulo.jpg`), na linha do Fatos Desconhecidos (755 mil). Ela casa com o T1, mas repete o T2.

### 005 Brasil: "A história INTEIRA do Brasil em 17 minutos"
**383 impressões · CTR 3,7% · retenção 42%** (17:23) · mosaico `mosaicos/historia-ptbr-005-brasil.jpg`

| Referência | Canal | Inscr. | Views | Data | v/i | > mediana? |
|---|---|---|---|---|---|---|
| [UfGD0lqHObI](https://youtu.be/UfGD0lqHObI) Como Começou a Ditadura Militar no Brasil? | O Diário de Titus Valério | 25,1 mil | 2,22 mi | 04/08/26 | 88 | sim (65 mil) |
| [QTjecFwrzbs](https://youtu.be/QTjecFwrzbs) O Dia em que o Povo Venceu o Império… | Mundos Reimaginados | 109 mil | 1,01 mi | 24/04/26 | 9,3 | sim (116 mil) |
| [qWPL11MOzOg](https://youtu.be/qWPL11MOzOg) O Dia em que Portugal se Mudou para o Brasil | Mundos Reimaginados | 109 mil | 773 mil | 16/03/26 | 7,1 | sim |
| [p0t7j7ish_E](https://youtu.be/p0t7j7ish_E) O Império do Café: Como o Grão Construiu… | Mundos Reimaginados | 109 mil | 548 mil | 02/04/26 | 5,0 | sim |
| [RH30MX3g5Rg](https://youtu.be/RH30MX3g5Rg) Por que Hollywood PROIBIU a história do Brasil… | Soldado Preto e Branco | 14,9 mil | 548 mil | 12/01/26 | 36,8 | sim (1,2 mil) |
| [s63x3TssYnI](https://youtu.be/s63x3TssYnI) Pedro Álvares Cabral: A Verdadeira Viagem… | Arquivo da Tragédia | 6,1 mil | 322 mil | 28/06/26 | 52,9 | sim (751) |
| [jPkK_uwJXJs](https://youtu.be/jPkK_uwJXJs) Pedro Álvares Cabral: O Acaso que Criou o Brasil | Histórias que Todos Ouvem Até o Fim | 9,9 mil | 221 mil | 02/01/26 | 22,3 | sim (1,5 mil) |
| [iCiM_67Vj7w](https://youtu.be/iCiM_67Vj7w) DOM PEDRO II foi Expulso… em uma Única Noite | Passado Implacável | 3,6 mil | 108 mil | 07/05/26 | 30,3 | sim (460) |
| [sD0cIJ8JMYw](https://youtu.be/sD0cIJ8JMYw) A HISTÓRIA INTEIRA do Brasil em 13 minutos | History Easy Guide | 3 mil | 22,2 mil | 27/10/26 | 7,5 | sim (6,7 mil) |
| [WcXwgbvbKMY](https://youtu.be/WcXwgbvbKMY) A História INTEIRA do Brasil em 17 Minutos (**= o nosso**) | História Inteira | 42 | 913 | 31/10/26 | 21,7 | sim (563) |
| en [EpkMOT35IQ8](https://youtu.be/EpkMOT35IQ8) The Empire of Brazil | Extra History | 4,63 mi | 479 mil | 06/06/26 | 0,1 | sim (284 mil) |

**O que o vídeo entrega:**
- **0:00–0:35** "Portugal, 1511. Um navio chamado Bretoa… alguém anota tudo o que vem no porão… Essa é uma das primeiras vezes que o nome Brasil aparece num documento. / E sabe onde ele aparece? / Numa lista de carga."
- 0:52 "como a terra que nasceu numa lista de carga virou um país de mais de duzentos milhões de pessoas."
- **1:12–1:15** "a pergunta vai ser a mesma: o que vai no navio… e o que fica aqui?" (refrão)
- 3:07–3:13 "brasileiro" era nome de ofício, "como ferreiro ou marinheiro".
- 7:22–7:46 a família real foge de Napoleão; "o Rio de Janeiro virou a capital de um império europeu. É o único caso conhecido…"
- 9:05–9:06 o Grito: "ele estava numa mula, e com uma dor de barriga daquelas."
- 11:43–11:49 "Dom Pedro morreu em Paris… com um travesseiro de terra do Brasil no caixão."
- **16:39** "Quinhentos anos depois, os navios saem cheios de soja, minério e petróleo." / 16:53 "Brasileiro já não é o nome de quem carrega a madeira dos outros."

**Proposta**
- **Título 1, padrão T1:** **"500 ANOS de Brasil em 17 minutos"** (32 caracteres). Referências: Histórias Épicas da Bíblia, "6000 Anos em 30 Minutos…" (1,97 mi, acima); ElHistorian, "IDADE MÉDIA: 1000 ANOS EM 78 MINUTOS" (33,6 mil, acima). É pago aos 0:52–1:00 e aos **16:39** ("Quinhentos anos depois"). Tira o título idêntico ao do História Inteira.
- **Título 2, padrão T5 (afirmação estranha + pergunta):** **"O Brasil nasceu numa LISTA DE CARGA. O que ia no navio?"** (55 caracteres). Referências: Por Quê, Hein?, "A China Esteve na Frente por 700 Anos. Então Por Que…" (77 mil, 19/10/2026, acima); Mente Primata, "Por que 300 mil anos quase nada mudou. Aí… Por quê?" (396 mil, 04/10/2026, acima). É pago aos **0:00–0:35**; a pergunta é o refrão do roteiro (1:15 e 16:48). Não entrega a resposta. Evitei "O Dia em que Portugal se mudou…" para não copiar o Mundos Reimaginados.
- **Thumb, padrão TH-E (split de dois tempos):**
  - Cena: um quadro dividido por uma diagonal amarela (o raio do template). À esquerda, **1511**: a nau portuguesa com toras vermelhas de pau-brasil empilhadas no convés e um papagaio, à luz quente de fim de tarde. À direita, **2026**: um navio graneleiro moderno carregado de soja e minério, com o porto à noite e luzes laranja.
  - No centro, na frente: um bonequinho brasileiro de hoje (capacete de estivador e prancheta), do peito para cima (~55%), olhando de um navio para o outro, intrigado.
  - Texto: pílulas "1511" à esquerda e "2026" à direita; embaixo, "**MESMO NAVIO?**" (MESMO em ouro, NAVIO? em branco).
  - Promessa: 500 anos com a mesma lógica.
  - Com os títulos: com o T1, ela visualiza os 500 anos; com o T2, ela mostra "o navio" sem repetir "lista de carga".
  - Pago aos 0:00–0:35, 1:15 e 16:39.
  - Sem pessoas escravizadas nem sofrimento na arte (a lista real tinha; a thumb mostra só madeira e bicho).
  - Referências (TH-E): Titus Valério (2 rostos + "1964–1985", 2,2 mi, 04/08/2026, acima); História do Mundo "CHINA VS JAPÃO" (258 mil, acima); apoio en: Animated History "221BC | 2026" (1,2 mi, acima).
  - Substitui a atual (Pedro I + Rio), que é quase igual à do História Inteira.

## 3. Resumo para o crivo
| Vídeo | Título 1 (T1) | Título 2 | Thumb | Pago em |
|---|---|---|---|---|
| Egito | 7.000 ANOS de Egito em 17 minutos | Por que Cleópatra viveu mais perto do iPhone que das PIRÂMIDES? (T2) | Cleópatra × pirâmide gasta, "JÁ ERA ANTIGA" (TH-A) | 0:16, 0:41 |
| Índia | 5.000 ANOS de Índia em 19 minutos | Como um VENTO decidiu quem mandava na Índia (T3) | Clive × artilheiro sob a monção, "CHUVA × CANHÃO" (TH-E) | 0:23–0:44, 10:52 |
| China | 3.000 ANOS de China em 16 minutos | Por que NINGUÉM abriu o túmulo do 1º imperador da China? (T2) | Qin com a esfera de mercúrio, "IMORTAL?" (TH-C; base pronta) | 0:03–0:35, 15:20 |
| Brasil | 500 ANOS de Brasil em 17 minutos | O Brasil nasceu numa LISTA DE CARGA. O que ia no navio? (T5) | Nau 1511 × graneleiro 2026, "MESMO NAVIO?" (TH-E) | 0:00–0:35, 16:39 |

Checagem: todos ≤ 63 caracteres; nenhum usa morte/morreu/morto/assassin*/massacre/chacina/chocante/perturbador; nenhum é cópia literal de clone; "em N minutos" mantido só no braço A (bíblia), com N = duração real (17:01, 19:28, 16:15, 17:23).

## Limitações
- O CTR e o tráfego das referências não são públicos: "acima da mediana" é views contra a mediana dos ≤ 30 longos recentes do próprio canal.
- Em pt, a Índia tem pouca referência de tema. Lá, o padrão vale mais pela estrutura (T3 e TH-E) do que pelo assunto.
- O yt-dlp devolve títulos traduzidos automaticamente; usei os títulos originais da `videos.list`.
- Não sei quais thumbs/títulos já estão no "Testar e comparar" do Studio: o hqdefault mostra só a arte padrão. Antes de subir, conferir se a `thumb-4-bonecos` da China já está em teste.
