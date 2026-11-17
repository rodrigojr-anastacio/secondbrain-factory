# Embalagem dos grandes canais de geografia / Terra / ciência explicativa (17/11/2026)

Canais: RealLifeLore (RLL, en), Wendover (en), Geography Now (GN, en), O Mundo e Tudo ao Redor (OM, pt), VisualPolitik (VP, es), Ciência Todo Dia (CTD, pt).
Fonte: `corpus/<canal>.csv` + mosaicos (normal e 160×90) + 16 thumbs "recente" abaixo da mediana vistas uma a uma. Classificação feita à mão, contas em Python (o script ficou fora do repo).
Formato dos exemplos: "título" · canal · views · ×med.

**Ressalvas do dado**
- **GN:** a mediana_30 (25 mil) está poluída por lives e arrecadações (pai doente), então o ×med dele fica inflado (12–70×). Uso o GN só para padrão visual e ordem relativa, e ele fica de fora das medianas de ×med juntando canais.
- **OM:** canal de 24 mil inscritos, os 17 vídeos são dos últimos 34 dias. Os de 11 a 15/11 têm 2 a 6 dias, então ×med < 0,2 ali ainda não é flop certo. Os de 18 a 26/10 (≥ 22 dias) são.
- **VP:** os "recentes" ruins têm 0 a 9 dias. Pesam pouco.
- Não temos o CTR dos outros. ×med mistura CTR com tema e alcance.

## 1. Títulos

### 1.1 Estrutura × desempenho (top 25 de cada canal; OM = 17; n = 142)
| Estrutura | n | ×med mediano (sem GN) | Quem usa |
|---|---|---|---|
| Notícia quente (fato + desdobramento) | 20 | 1,91 | VP 15 |
| Por que / Why | 19 | 1,76 | RLL 7, Wend 4, CTD 4, OM 3 |
| Como / How (origem, deterioração) | 18 | **2,10** | Wend 10, RLL 5 |
| Rótulo / "explicado" / "The X of Y" | 17 | 1,51 | GN 8, Wend 7 |
| Ameaça / futuro ("brink", "will change… forever", "a punto de") | 16 | 1,87 | VP 9, RLL 4 |
| Afirmação estranha / paradoxo | 16 | **2,39** | CTD 7, GN 5 |
| Lacuna / segredo / "ninguém" / "hidden" | 12 | 1,94 | RLL 5, GN 4, CTD 3 |
| E se? / sobreviveria? | 9 | **1,00** | OM 8 |
| Superlativo (pior, mais, newest, only) | 8 | **2,61** | GN, RLL, CTD |
| Outra (efeito em você, utilidade) | 5 | 3,5 (CTD Vape/Bets) | CTD 3 |
| Contraste A×B / "vs" | 2 | 1,22 | Wend, GN |

O padrão de cada canal:
- **RLL:** Why/How quase sempre com um **adjetivo extremo** dentro (Absurdly, Endless, Most Divided, 100x Larger, WAY Scarier). Na prática é estrutura + superlativo.
- **Wendover:** "How X Got So Terrible/Bad" é o topo absoluto (3,49 e 2,98).
- **CTD:** paradoxo curto com 2 palavras em CAPS.
- **VP:** "NOMBRE + VERBO fuerte: desdobramento" com 5 CAPS.
- **OM:** "E se…?" e "Por que…?" com 1 palavra em CAPS.

Leitura: superlativo e paradoxo rendem mais. O "E se?" é a estrutura **mais instável**: dá 2,67× e dá 0,21× no mesmo canal.

### 1.2 Tamanho (n_chars, sem o "@VisualPolitik" e sem as lives)
| Canal | Mediana top | Hits ≥ 1,5× | Abaixo de 1× |
|---|---|---|---|
| RLL | 47 | 47 | 44 |
| Wendover | 34 | **29,5** | 33 |
| OM (pt) | 51 | **48** | **57,5** |
| VP (es) | 65 | 65 | 76 |
| CTD (pt) | 32 | 32 | 35 |

- O título ruim é igual ou **mais longo** que o bom em 4 de 5 canais.
- Em pt, a faixa boa é **32–50 caracteres**.
- Palavras: Wend/CTD/GN usam 6, RLL 8, OM 10, VP 11.

### 1.3 Palavras de poder e forma
- **Hits ≥ 1,5× (122 títulos) × abaixo de 1× (33):**
  - "explained/explicado": 10 × 0.
  - Superlativos (worst, peor, pior, mortal, newest, only, most): 14 × 1.
  - "hidden/secret/real reason": 5 × 0.
  - "…" de suspense: 6 × 0.
  - **Parênteses: 1 × 6.**
  - "você": 3% × 9%.
  - "Why" puro: 10% × 18%: o Why sem adjetivo extremo não segura.
- **CAPS:** o pt e o es usam CAPS na palavra-objeto (OM 1, CTD 2, VP 5 por título). O en não usa (RLL e Wend: 0), com uma exceção pontual: "WAY Scarier".
- **pt × en:** o pt pergunta mais (CTD 13 de 25 títulos com "?", OM 12 de 17; RLL 1 de 25, Wend 0 de 25). O en afirma ("Why Myanmar is Dying"). O es grita com a notícia.
- **"Brasil" no título funciona quando é uma ausência ou um paradoxo:** "Por que o BRASIL não tem BOMBAS ATÔMICAS ?" · CTD · 2,93 mi · 4,88× e "Por que o BRASIL não tem TRENS?" · 2,14×. Quando é utilidade ou cenário, falha: "Vale a pena ter CARRO HÍBRIDO no BRASIL" · 0,32 mi · 0,53×.

## 2. Thumbs (top 10 de cada canal, 60 thumbs)

| Canal | Elemento dominante | Focos | Palavras na thumb (mediana) | Destaque | Paleta |
|---|---|---|---|---|---|
| RLL | **mapa em relevo 3D** 10/10 (+ navios, pins, 1 meme) | 1–2 | 3 (0–5) | setas ou círculo 6/10, cor de alerta 8/10 | mar turquesa, relevo verde/bege, **vermelho** na região-alvo, caixa preta com letra branca/amarela sublinhada |
| Wendover | **foto real / objeto** 8/10, mapa 1/10 | 1–2 | 4 | logo fixo, faixa laranja no canto | foto saturada + caixa preta |
| GN | **rosto** 10/10 + mapa recortado ou bandeira | 2 | 0 | seta/círculo 2/10, silhueta + "?" 2/10 | fundo preto, contorno branco |
| OM (pt) | **render CGI realista** da Terra/espaço 10/10 | 1 | 2 | 1 seta, 1 split | escuro + 1 cor quente, letra branca enorme no topo |
| VP (es) | **rosto de político** 10/10 | 1–2 | 3 | faixa de papel rasgado, 2ª linha em vermelho | escuro, branco + vermelho |
| CTD (pt) | **rosto** 10/10 + objeto do tema | 2 | 0–1 (sem texto em 6/10) | tarja vermelha sobre o rosto 2/10 | ultrassaturada |

**Totais nas 60 thumbs:**
- Rosto ou personagem: 31 (GN, VP, CTD e 1 meme da RLL).
- Mapa dominante: 17 (RLL 10, GN ~6 junto com rosto, Wend 1).
- Foto real de objeto: 8 (Wend).
- Render da Terra/espaço: 10 (OM).
- Texto com ≤ 4 palavras: 54/60. Nenhuma thumb tem frase longa.

**Estado incompleto ou tensão** aparece em quase todas as top da RLL: navios cercando (Venezuela), pins cercando (Irã), "WHY?" em cima do rico × pobre (Itália), região "em branco" circulada (Saara Ocidental).

**A 160×90:**
- RLL e OM continuam legíveis: 1 bloco de texto grande e 1 mancha de cor.
- Wendover lê pelo texto.
- GN e CTD leem pelo rosto.
- Falham no tamanho pequeno: foco minúsculo (o círculo de "Why 600,000 People Live On This Rock…" some) e labels pequenos (Wendover Taiwan).

### 2.1 Como o mapa vira emoção (o que separa a RLL de um mapa escolar)
1. **Uma região em cor de alerta sobre relevo neutro.** "Why the Iron Curtain Still Keeps Germany Divided" · RLL · 3,09 mi · 2,49×: a Alemanha Oriental em vermelho com foice e martelo, 0 palavras.
2. **Antes × depois em tela dividida.** "The Best-Run Dictatorship in History: Singapore" · RLL · 4,03 mi · 3,25×: BROKE 1965 × CRAZY RICH 2025. A Wendover faz o mesmo nos caminhões 1970/2025 (3,49×) e a CTD no vape 1920/2025 (4,69×).
3. **Comparação de tamanho.**
   - "How Rwanda is Conquering Their 100x Larger Neighbor" · RLL · 2,64 mi · 2,13×: Ruanda minúsculo e brilhando em vermelho, setas entrando no Congo gigante azul.
   - "A que distância do TON 618 você sobreviveria?" · OM · 0,80 mi · 2,31×: 600 × 10 ANOS-LUZ.
4. **Cerco ou convergência** (setas e ícones apontando para um ponto).
   - "Why The US & Venezuela Are On The Brink of War" · RLL · 3,89 mi · 3,13×.
   - "How The US & Iran Became Arch-Enemies" · RLL · 3,69 mi · 2,98×.
5. **Linha que corta** (fronteira, rio, barragem ou falha brilhando). "How China's New Mega-Dam Will Change Asia's Map Forever" · RLL · 2,29 mi · 1,84×.
6. **Escala humana × ameaça natural.**
   - "Why The Nepal Flood Was WAY Scarier Than You Think" · RLL · 2,34 mi · 1,88×: "1,500-FT TSUNAMI" em cima de "VILLAGE" com brilho vermelho.
   - "O que aconteceria se um ASTEROIDE caísse no oceano?" · OM · 0,72 mi · 2,08×: o tsunami chegando ao **Rio de Janeiro**.
7. **Lacuna visual** (silhueta preta + "?", ou mancha em branco). "Nobody remembers or cares about this country." · GN · 0,87 mi · 34×.
8. **1 dado como label** ("72M PEOPLE", "EMPTY"). "Why Cambodia & Laos Are Absurdly Empty" · RLL · 2,92 mi · 2,36×.

Isso tudo é feito com o mesmo relevo hipsométrico claro, então a emoção vem da **camada por cima** (cor, seta, split, rótulo), não do mapa.

## 3. Título × thumb (top 10 de cada canal)
| | RLL | Wend | GN | OM | VP | CTD | Total |
|---|---|---|---|---|---|---|---|
| Completa (diz algo que o título não diz) | 5 | 5 | 0 | 4 | 10 | 3 | **27** |
| Repete (mesma palavra ou só rótulo) | 4 | 4 | 0 | 6 | 0 | 1 | 15 |
| Sem texto | 1 | 1 | 10 | 0 | 0 | 6 | 18 |

Nos canais que completam, quase todas as thumbs do topo completam.

**5 bons exemplos de "completa":**
1. "Why This Part of Africa is Erased on Every Map You See" · RLL · 3,34 mi · 2,70×. Thumb: "WHY IS THIS ALWAYS **BLANK**?" + círculo amarelo + setas.
2. "How American Cars Got So Bad" · Wendover · 3,38 mi · 2,98×. Thumb: "THE DOWNFALL OF **DETROIT**" sobre a fábrica em ruínas (dá o lugar e o desfecho).
3. "How the Channel Tunnel Works" · Wendover · 2,35 mi · 2,07×. Thumb: "THE TUNNEL'S **BROKEN PROMISE**" (o título é neutro, a thumb põe o conflito).
4. "A NASA fotografou o LIMITE do universo" · OM · 1,28 mi · 3,70×. Thumb: "**UMA PAREDE**" + astronauta diante do mapa da radiação cósmica de fundo (CMB).
5. "Si BUKELE gana en HAITÍ, su MANO DURA se exportará…" · VP · 2,72 mi · 4,18×. Thumb: "**NO ES UN RESCATE**" (negação que cria dúvida).

Também: "The Best-Run Dictatorship…" com BROKE/CRAZY RICH (3,25×).

**Contraste dentro do OM** (exceção à regra do "completa"):
- As melhores thumbs usam só a **palavra da estrutura** sobre uma imagem forte: "POR QUE?" 5,16×; "E SE?" 2,67× e 2,08×.
- As que completam com **conceito** também vão bem: UMA PAREDE 3,70×; 600 × 10 ANOS-LUZ 2,31×.
- As que mostram **medida ou objeto** vão mal: 26 BILHÕES DE KM 0,54×; 0.000000001s 0,48×; VIAGEM FATAL 0,37×; +65 METROS 0,17× (com 2 dias).

Ou seja: no OM, a medida pura não atrai clique, mesmo quando ela completa o título.

## 4. Hit (≥ 1,5×) × flop (< 0,7×) no mesmo canal

**O Mundo e Tudo ao Redor (pt), com atenção especial**
1. **Parênteses matam.** Os 6 títulos com "(…)" têm mediana de 0,26×; os 11 sem parênteses, 1,25×. Nenhum hit tem parênteses.
   - Flops (com ≥ 22 dias): "APOPHIS: o asteroide que mudará TUDO em 2029 (ele está chegando)" · 98 mil · 0,28×; "Como a Voyager 1 ainda FUNCIONA após 49 anos (e nunca bateu em nada)" · 186 mil · 0,54×.
   - Os parênteses também alongam o título: os flops ficam em 57,5 caracteres contra 48 dos hits.
2. **O hit é uma pergunta sobre algo cotidiano que parece impossível na Terra.** "Por que o oceano não ESCOA para dentro da Terra?" · 1,79 mi · 5,16× (com 8 dias). A curiosidade do espaço profundo fica abaixo: "Você conseguiria sobreviver a 1 NANOSSEGUNDO no núcleo do Sol?" · 166 mil · 0,48×.
3. **O "E se?" ganha com ameaça sobre um lugar reconhecível + multidão ou cidade na thumb.** "Quanto tempo você teria se a LUA começasse a cair?" · 0,92 mi · 2,67× (Lua sobre uma avenida com gente filmando). E perde quando é só um objeto no vácuo: "O que acontece com a Terra se a LUA desaparecer?" · 73 mil · 0,21×. Este último repete o tema da Lua 6 dias depois.
4. **O nome técnico como gancho falha; o nome genérico com ameaça funciona.** "APOPHIS…" 0,28× contra "O que aconteceria se um ASTEROIDE caísse no oceano?" 2,08×.
5. **A thumb do hit tem 1–2 palavras de estrutura ou de conceito** ("POR QUE?", "E SE?", "UMA PAREDE"). A do flop mostra a medida ("26 BILHÕES DE KM", "+65 METROS").
   - "Quanto do BRASIL sobraria se todo o gelo derretesse?" (60 mil, 0,17×) tem só 2 dias: ainda não dá para cravar.
   - Mas o tema já rendeu menos em "Como seria a ANTÁRTIDA sem GELO?" · 346 mil · 1,0×.

**RealLifeLore**
- O mesmo molde perde força na 3ª vez:
  - "Why Cambodia & Laos Are Absurdly Empty" · 2,92 mi · 2,36×
  - "Why The US Southeast Coast is Absurdly Empty" · 2,13 mi · 1,71×
  - "Why "Nobody" Lives on the Pacific Northwest Coast" · 1,09 mi · 0,88×. A thumb tem uma faixa fina vermelha + "ALMOST TOTALLY EMPTY": foco fino demais a 160 px.
- Foco minúsculo: "Why 600,000 People Live On This Rock With No Resources" · 1,33 mi · 1,07×. O círculo vermelho é pequeno; título com 54 caracteres.
- Desastre natural que dá certo traz escala humana + "pior do que você pensa": Nepal, 1,88×. O Cascadia (0,98×, 3 dias) usa "THE BIG ONE IS COMING" sem nada humano na imagem.
- Tema fora do canal: "How To Save a Child's Life From Gaza" · 185 mil · 0,15×.

**Wendover**
- A perda ganha da vitória:
  - "How the Trucking Industry Got So Terrible" · 3,95 mi · 3,49×
  - "How American Cars Got So Bad" · 2,98×
  - × "Why Texas Wins" · 556 mil · 0,49× e "Why the Ikea Business Model Wins" · 0,93×.
- A thumb rótulo que repete o título perde: "How Private Equity Ruined American Youth Sports" · 630 mil · 0,56×, com thumb "THE BIG BUSINESS OF YOUTH SPORTS".
- Diagrama desenhado sem foto real nem tensão perde: "Why American Houses Are So Flimsy" · 761 mil · 0,67×.

**Ciência Todo Dia (pt)**
- O Brasil como ausência ganha (bombas 4,88×, trens 2,14×). O Brasil como utilidade perde: "Vale a pena ter CARRO HÍBRIDO no BRASIL" · 0,53×.
- O futuro especulativo sem nada em jogo perde: "Como será a primeira BASE LUNAR?" · 317 mil · 0,53×; "A ISS está com os dias contados" · 290 mil · 0,48×.
- O paradoxo sobre você ganha: "Você pensa ERRADO sobre DOPAMINA" · 2,37×; "A sua TELA não consegue MOSTRAR essa COR" · 1,57×.

**VisualPolitik** (flops com 0 a 3 dias, peso baixo)
- Rosto pouco conhecido + número técnico rende menos: "EEUU sabía que 51 SISTEMAS de su CONTROL AÉREO no aguantaban…" · 0,38×.
- Rosto famoso + negação rende mais: "NO ES UN RESCATE" (Bukele), 4,18×.

## 5. O que passa direto para o Em Relevo (mapa 3D real, dados, sem rosto e sem IA de cena)

O Em Relevo já está na família visual da RLL e da OM (mapa + 1–3 palavras). Os modelos certos são **RLL (mapa) + OM/CTD (título pt)**, não GN/CTD/VP (rosto). Hoje o CTR está em 1,5–2,7%. As diferenças em relação à RLL estão abaixo, como regras.

**Regras de thumb de mapa que gera clique**
1. **Relevo claro e saturado, não escuro.** A RLL usa mar turquesa e relevo verde/bege iluminado. As nossas 4 thumbs são marrom/azul-escuro e perdem contraste a 160 px. Testar a mesma base com hipsometria clara.
2. **Uma única região em cor de alerta** (vermelho ou laranja saturado) sobre o resto neutro ou dessaturado. Nada de duas manchas de mesma força (exemplo de referência: Alemanha Oriental, 2,49×).
3. **O mapa precisa de uma camada de tensão:**
   - seta convergindo;
   - linha que corta brilhando (frente fria, rio, falha);
   - círculo em lugar "vazio";
   - split antes × depois (por exemplo, a mesma represa em 2 datas).

   Sem conflito, é mapa escolar.
4. **Comparação de tamanho quando houver número:** a área queimada ou alagada sobreposta a um estado ou país conhecido ("Rwanda 100x", 2,13×; "600 × 10 ANOS-LUZ", 2,31×). É o jeito sem rosto de dar escala.
5. **Escala humana dentro do mapa:** 1 label "CIDADE" ou "VILA" em brilho vermelho sob a ameaça ("1,500-FT TSUNAMI / VILLAGE", 1,88×). Substitui o rosto.
6. **Texto: 1–4 palavras que completam o título, nunca repetem.** Caixa preta com letra branca e 1 palavra amarela sublinhada (RLL) ou bloco branco enorme no topo (OM). O número só entra se for **o** dado chocante e não estiver no título.
7. **Foco legível a 160 px:** a região-alvo ocupa ≥ 25% da área. Faixa costeira fina ou ilha minúscula não funciona (0,88× e 1,07× na RLL).
8. **Foto real em split com o mapa** é o substituto honesto do "personagem": rua alagada, açude seco, satélite antes/depois (Singapura, 3,25×; caminhões, 3,49×).
9. **Lacuna visual:** silhueta do estado ou região em preto + "?", ou mancha "em branco" circulada (GN 34×; Saara Ocidental, 2,70×). Serve para "a parte do Brasil que ninguém vê".

**Regras de título (pt-BR)**
- 32–50 caracteres; **sem parênteses**; 1–2 palavras em CAPS na palavra-objeto (padrão OM/CTD).
- Estruturas com evidência:
  - "Por que o Brasil não tem X?" (4,88× / 2,14×);
  - "Por que [região] é absurdamente vazia/seca?" (2,36×);
  - "Por que [desastre] foi MUITO pior do que parece" (1,88×);
  - "Como [lugar/sistema] ficou tão ruim" (3,49× / 2,98×);
  - "A parte do Brasil que ninguém mostra no mapa" (2,70×; GN 70×);
  - "O que está escondido sob [lugar]" (2,10×).
- Evitar:
  - "E se…?" puro sobre objeto no vácuo;
  - nome técnico como gancho ("APOPHIS", "El Niño 2026" sem ameaça concreta);
  - "como será…" no futuro sem nada em jogo;
  - utilidade ("vale a pena…");
  - repetir a fórmula de um hit 3× em seguida.
- Ameaça sobre lugar brasileiro reconhecível (Rio, uma capital, o Nordeste) + escala visível: é o que fez o tsunami no Rio (2,08×) e a Lua sobre a cidade (2,67×) baterem a média do OM.
