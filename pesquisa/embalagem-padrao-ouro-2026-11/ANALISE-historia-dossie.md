# Embalagem dos grandes canais de HISTÓRIA e DOSSIÊ: título + thumb (17/11/2026)

Corpus: `corpus/<canal>.csv` (top + recentes, ×med = views ÷ mediana dos últimos 30 longos), mosaicos normal e 160×90, thumbs individuais.
História (9): OverSimplified (OS), History Matters (HM), Kings and Generals (KG), **History in Minutes (HiM, nosso molde)**, CountryCorns (CC), Nerdologia (pt), Brasil Paralelo (BP, pt), Atlas del Tiempo (es), Academia Play (AP, es). Dossiê (4): **Archive in Minutes (AiM, nosso molde)**, Fern, LEMMiNO, Barely Sociable (BS).
Contas em python (`~/cache/tmp/emb/cls.py`); a classificação de thumbs é visual, feita por mim (aprox.).

**Ressalvas (ler antes dos números)**
- **Viés de seleção:** o corpus é top + recentes, então as medianas de ×med por estrutura saem infladas. Compare as estruturas entre si, não com 1,0.
- **Idade:** nos canais pequenos, os vídeos de novembro têm de 1 a 10 dias, e o ×med baixo deles é em parte só idade. Nos moldes, comparei também views/dia e vídeos com ≥ 15 dias.
- **Brasil Paralelo** saiu das estatísticas de título: lives e notícia política com ×med de 13 a 627 distorcem tudo. Entra só como exemplo de thumb.
- A thumb gravada para "The ENTIRE History of the Cuban Missile Crisis" (AiM) é a de **GULAG**: ou houve troca no canal, ou o dado está errado. Não usei esse par título × thumb.

---

## 1. TÍTULO

### 1.1 Estrutura × desempenho (sem BP; n = nº de títulos)
| Estrutura | História n · med ×med · hits≥1,5 / flops<0,7 | Dossiê n · med ×med · hits / flops |
|---|---|---|
| Rótulo de tema ("WW2 - OverSimplified", "LA MASONERÍA") | 91 · 1,37 · 40/17 | 26 · 1,17 · 6/5 |
| Fórmula "ENTIRE/TODA la Historia… in N Minutes" | 39 · **1,81** · 22/7 | 28 · 0,94 · 11/12 (só AiM) |
| "Why/Por qué…?" | 37 · 1,19 · 8/4 (quase tudo HM) | 4 · 1,76 · 2/0 |
| Pergunta/lacuna ("¿Qué es el fascismo?") | 8 · 1,42 · 4/3 | — |
| "The X that/who" / "O país que" | 6 · 1,57 · 3/0 | 4 · **1,92** · 4/0 |
| "How X…" | 6 · 0,96 · 1/1 | 6 · 1,46 · 3/1 |
| Paradoxo/afirmação estranha ("Rome Never Really Fell") | 6 · **0,58** · 1/3 | — |
| Superlativo/número extremo | 5 · 2,04 · 4/1 | 10 · 1,71 · 6/0 |
| Mistério/caso ("The Vanishing of…", "Hunt for…") | 2 · 1,13 | 26 · **1,64** · 16/1 |
| Contraste de destinos (rico × pobre) | 2 (AP "¿Por qué CUBA es tan POBRE?" 3,47×; "¿Por qué Suiza es tan rica?" 1,03×) | — |
| Investigação "I investigated…" | 0 | 0 |

Leitura:
- **História:** a fórmula ganha no agregado, mas só quando o tema é enorme. OverSimplified, Academia Play e Nerdologia vivem de **rótulo puro de tema grande**, sem gancho nenhum no título. O paradoxo esperto foi a pior estrutura em História (HiM: "Rome Never Really Fell" 0,38×, "Russia: The Biggest Country That Never Had Enough People" 0,75×).
- **Dossiê:** mistério/caso e "The X who" quase não têm flop (17 de 30 viraram hit, só 1 flop). A fórmula do AiM tem tantos flops quanto hits: com ela, quem decide é o **tema**.
- **Palavras de poder** (sem BP, n · med): "más/most" 14 · 1,6–3,8, 0 flop · "vs" 13 · 2,11 · "secret/secreto" 17 · 1,7 · "myster*" 13 · 1,66 · "all battles/full" 2,75 · "hunt" 2,57. As fracas: "never" 0,75 · "biggest" 0,75 · subtítulo com "|" 0,88. O "ENTIRE" sozinho dá med 1,00 (15 hits, 15 flops): a palavra não salva tema fraco.

### 1.2 Tamanho (n_chars, mediana)
| Grupo | Top | Recentes < 1× | Hits ≥ 1,5 | Flops < 0,7 |
|---|---|---|---|---|
| História | 54 | 55 | 54,5 | 55 |
| Dossiê | **40** | 46 | **38,5** | **53** |
| Todos | 49,5 | 53,5 | 48 | 54,5 |

Por canal, hit × flop: **AiM 45 × 67**, Nerdologia 46 × 65, Fern 35 × 45, AP 41,5 × 49, OS 42 × 46. Em História o tamanho não separa nada, porque HM e KG colocam um sufixo longo fixo ("(Short Animated Documentary)", "DOCUMENTARY"). Em Dossiê, título curto = tema conhecido. Título longo quase sempre traz um aposto que explica o tema ("the OSS, **the Spies Before the CIA**"), e o aposto denuncia que o público não conhece o assunto.

### 1.3 pt/es × en
- **es (Atlas, AP):** "TODA la Historia de X en N Minutos | subtítulo-promessa" (Atlas: 75 a 100 caracteres; mediana dos hits 82,5). Usa CAIXA ALTA numa palavra-chave ("Los JUICIOS de NÚREMBERG", "¿Por qué CUBA es tan POBRE?") e emoji de bandeira (AP). O espanhol tolera título longo; o en dos grandes de dossiê, não.
- **pt (Nerdologia):** o título é um rótulo descritivo ("A compra do Alasca da Rússia pelos EUA") e **o gancho vai para a thumb** ("DE QUEM É O ALASCA?"). O BP usa CAIXA ALTA e pergunta de notícia.
- **en:** frase nominal curta, "The [superlativo] X" / "The X Who" (Fern, med 35 caracteres), ou fórmula com tema icônico (AiM/HiM).

---

## 2. THUMB (top 10 por canal; CC = 4; 114 thumbs sem BP)

### 2.1 Por canal
| Canal | Elemento dominante | Focos | Texto (palavras; repete/completa) | Paleta | Tensão / emoção | 160×90 |
|---|---|---|---|---|---|---|
| OS | 2 personagens cartoon cara a cara sobre mapa vermelho×azul | 2–3 | tema + marca + nº da parte; repete | saturada, escura | sobrancelha de raiva, duelo | ótima ("WW2") |
| HM | bonequinho em bloco + mapa com bandeiras | 2 | 4–7 palavras, a pergunta do título reescrita; 2 completam com "THIS" apontando para o mapa | chapada, média | pergunta + território em disputa | média (texto longo) |
| KG | pintura de 2 comandantes cara a cara, ou mapa com setas de exército | 2–3 | tema + datas; repete (1 completa: "MILITARY MASTERPIECE") | quente, escura | duelo | média (carregada) |
| **HiM** | líder (6) ou panorama (4) em traço de tinta; NOME + datas | 1–2 | 1–2 palavras + datas; repete 10/10 | **clara, céu azul 10/10** | fogo e fumaça em 4 (Ucrânia, Rússia, Israel, Coreia) | nome legível; resto vira "cartão-postal" |
| CC | líder chibi com raiva, apontando; "THE HISTORY OF / ISRAEL" amarelo enorme | 1–2 | 3–4 palavras + datas; repete | vermelho-pôr-do-sol, alto contraste | raiva + dedo apontado + mísseis | ótima |
| Nerdologia | rosto real (foto/ator) + colagem de arquivo | 1–3 | 2–4 palavras; **completa 5/10** ("REALMENTE O PRIMEIRO?") | sépia escura | olhar para a câmera, pergunta | boa |
| Atlas (es) | agente(s) de braços cruzados; "CIA vs KGB" | 2 | 2–3 palavras + datas; repete | sépia/papel velho | duelo "vs" | boa |
| AP (es) | colagem ilustrada densa + mão desenhando | 4+ | 1–4 palavras; repete | saturada | multidão de personagens | média |
| **AiM** | 1 vilão/agente de meio corpo segurando objeto (anel, carta, envelope, pasta, cachimbo, telefone) | 1–2 | 1–2 palavras + datas; repete 10/10 | clara (9/10); **a SS é escura, e é o maior hit** | objeto-documento; Beria arrastado por guardas (medo) | nome legível |
| Fern | rosto real ou render 3D + círculo/seta/mira vermelha | 1–2 | 0–3 palavras; **completa 6/10**, repete 1, sem texto 3 | escura + vermelho | alvo, mira, alfinete no mapa, rota vermelha | ótima |
| LEMMiNO | 1 objeto-símbolo minimalista (cigarra, avião, faca na cartola, OVNI) | **1** | sem texto 8/10 | escura, degradê, 5/16 com acento vermelho | objeto ameaçado/ameaçador | ótima (silhueta) |
| BS | 1 objeto/ícone sobre preto (camelo, livro, telefone, pílula com caveira) | 1 | 0–4 palavras; completa 3, repete 3, sem texto 4 | preto + vermelho/branco | "MISSING SINCE 2004?", "WHO IS HE?" | ótima |

### 2.2 Frequências (114 thumbs)
| Elemento dominante | n | % |
|---|---|---|
| Personagem ilustrado (cartoon, pintura, traço) | ~66 | 58% (todo o grupo "história" + AiM/Atlas) |
| Objeto/símbolo isolado | ~22 | 19% (LEMMiNO, BS, 3D da Fern) |
| Rosto real (foto) | ~16 | 14% (Nerdologia, Fern) |
| Panorama/cena sem personagem | ~5 | 4% (HiM: Egito, Irã, China, Roma) |
| Mapa como elemento principal | ~3 | 3% (KG; o mapa aparece como fundo em OS e HM) |

- **Focos:** 1–2 em ~80%. Só AP e KG passam de 3.
- **Texto:** repete o título 82 (72%) · completa 17 (15%) · sem texto 15 (13%).
- **Palavras na thumb:** as "in Minutes" (HiM/AiM/Atlas) usam 1–2 palavras + datas; OS, 2–4 + marca; HM, 4–7; dossiê grande, 0–3.
- **Paleta:** escura em OS, KG, CC, Nerdologia, Fern, LEMMiNO e BS. **Clara só em HiM e AiM (e HM, chapada).** Os nossos dois moldes são os únicos de fundo claro tipo céu.

### 2.3 Como os canais sem rosto criam emoção
1. **Cartoon com raiva:** sobrancelha em V e duelo cara a cara (OS em 8/10, CC, HM).
2. **Marca de alvo vermelha:** círculo, seta, mira, alfinete, rota (Fern 6/10: El Chapo circulado; mira sobre o presidente; alfinete sobre Khamenei; rota vermelha até a casa de El Mencho).
3. **Objeto em perigo ou ameaçador:** faca sobre a cartola (Ripper), pílula com caveira (BS), cogumelo nuclear (Tsar Bomba).
4. **Cidade em chamas:** fumaça e fogo atrás do líder (HiM Ucrânia 3,1×, a única "história" dele com tema não icônico que deu hit).
5. **Linha que divide:** HiM Coreia, com o traço vermelho entre os dois líderes. A ideia é boa, mas a thumb tem 6 dias e não dá para medir.
6. **Duelo "vs":** Atlas "CIA vs KGB" 78×, "KGB vs Mossad" 4,4×.
7. **Documento ou objeto nas mãos do vilão:** AiM (carta da Gestapo, envelope do MI6, pasta da KGB, anel da SS à luz de vela).
8. **Corpo sem rosto:** manequins 3D (Fern ANØM 1,94×, ESCAPE 1,64×) ou silhueta vermelha (LEMMiNO D. B. Cooper 3,83×, JFK 2,42×).
9. **Contraexemplo:** carimbo de documento "USELESS" no Tratado de Versalhes (HM 0,51×). O carimbo sozinho não salva tema de livro didático.

---

## 3. Relação título × thumb
- **Contagem:** repete 72% · completa 15% · sem texto 13%. **Os pequenos e os "in Minutes" repetem 100%. Fern, Nerdologia, BP e BS completam.** Entre os grandes de dossiê (Fern, LEMMiNO, BS), só 6 de 30 repetem.
- **5 bons exemplos de complemento:**
  1. "The Hunt for America's Smartest Killer" · Fern · 13,2 mi · 2,97× → thumb "UNABOMBER" (o título esconde o nome, a thumb revela).
  2. "The Only Nazi Hitler Feared" · Fern · 12,3 mi · 2,75× → "WORSE THAN HITLER?" + rosto de Heydrich ao lado de Hitler.
  3. "The Biggest Nuke in History" · Fern · 11,2 mi · 2,5× → "TSAR BOMBA" + cogumelo visto do espaço.
  4. "Santos Dumont e quem inventou o avião" · Nerdologia · 149 mil · 2,03× → "REALMENTE O PRIMEIRO?".
  5. "A História da Groenlândia e o interesse dos EUA" · Nerdologia · 100 mil · 1,36× → Trump + "GROENLÂNDIA À VENDA?". (Bônus: "Why didn't Germany stop expanding in 1939?" · HM · 1,47 mi · 1,56× → "WHY WASN'T THIS ENOUGH?" com o mapa aceso.)

---

## 4. Hit (≥ 1,5×) × flop (< 0,7×) no mesmo canal

### 4.1 History in Minutes (nosso molde do historia-ptbr)
| Hits | Flops |
|---|---|
| "The ENTIRE History of Egypt in 17 Minutes" · 593 mil · 10,2× (8,8 mil/dia) | "Rome Never Really Fell: The Full Story of Rome" · 22 mil · 0,38× (363/dia) |
| "The ENTIRE History of India, From Harappa to Today, in 16 Minutes" · 647 mil · 11,1× (13,5 mil/dia) | "Israel vs Palestine: Every Line Ever Drawn (1886–2026)" · 20 mil · 0,35× (530/dia) |
| "Why Every Empire Wanted Ukraine (Full History)" · 180 mil · 3,1× | "Russia: The Biggest Country That Never Had Enough People" · 44 mil · 0,75× |
| "Persia Never Died. It Just Changed Its Name." · 92 mil · 1,58× | "The ENTIRE History of Japan: The Country Earthquakes Built" · 2,6 mil em 8 dias (329/dia) |

O que os hits têm e os flops não:
1. **Fórmula literal completa** ("ENTIRE + país + in N Minutes"). As variações espertas sem "in N Minutes" afundaram: Roma, Rússia e Japão ficaram entre 0,05× e 0,75×.
2. **Civilização icônica e antiga, com público enorme** (Egito, Índia). Roma era icônica, mas o título trocou a promessa pelo paradoxo.
3. **Conflito vivo na thumb:** Ucrânia com Zelensky e fogo (3,1×). As thumbs de panorama pacífico são todas iguais entre si a 160×90, e a thumb não é o que separa hit de flop aqui: **o que separa é tema + título**.
4. Paradoxo em História só funcionou uma vez, com nome alternativo conhecido ("Persia/Iran"); depois falhou 2 vezes.

### 4.2 Archive in Minutes (nosso molde do dossie-es), só vídeos com ≥ 15 dias
| Hits (views/dia) | Flops (views/dia) |
|---|---|
| "…of the SS in 16 Minutes" · 734 mil · 8,8× (38,6 mil) | "If You Don't Understand the NKVD, You Don't Understand Stalin's Terror" · 26 mil · 0,31× (1,0 mil) |
| "…of the Gestapo in 12 Minutes" · 464 mil · 5,6× (21,1 mil) | "…of the Berlin Wall in 16 Minutes" · 50 mil · 0,6× (1,6 mil) |
| "…of MI6 in 11 Minutes" · 303 mil · 3,6× · "…Mossad" 3,7× · "…KGB" 3,0× · "…CIA" 2,8× | "…of Operation Barbarossa in 10 Minutes" · 43 mil · 0,52× (1,9 mil) |
| "…of Beria in 15 Minutes" · 206 mil · 2,5× | "…of the Cuban Missile Crisis in 11 Minutes" · 60 mil · 0,72× |

O que os hits têm:
1. **Uma organização secreta ou temida, de 1 palavra ou sigla famosa** (SS, Gestapo, KGB, CIA, MI6, Mossad, Stasi): 7 de 7 acima de 2×. **Eventos** (Muro, Barbarossa, Crise dos Mísseis) ficaram entre 0,5× e 0,7×.
2. **Fórmula intacta:** a única vez em que fugiu dela (NKVD) deu o pior resultado (0,31×).
3. **Nada de aposto:** os títulos de novembro que precisam explicar o tema ("the OSS, the Spies Before the CIA", "the GRU, Russia's Military Spies", "the Securitate, the Secret Police Worse Than the Stasi") ficam em 3,3–5,9 mil/dia. Na mesma idade, "the FBI" fez 8,5 mil/dia.
4. **Thumb:** o maior hit (SS) é a única thumb noturna e escura do top, com um objeto íntimo (anel à luz de vela). Personagem que segura documento (Gestapo, KGB, CIA) se repete nos hits.
5. **Espelho em espanhol:** o Atlas del Tiempo copiou o formato e confirma. Com o mesmo layout sépia, "TODA la Historia de la CIA vs. KGB" deu 112 mil · 78× e "del Mossad" 89 mil · 62×, contra "de Egipto" 0,83×, "de Canadá" 0,62× e "de Afganistán" 0,59×. **Espiões e "vs" vencem; país, no dossiê, não.**

### 4.3 Outros canais
| Canal | Hit | Flop | Diferença |
|---|---|---|---|
| OS | "WW2 - OverSimplified (Part 1)" · 105,9 mi · 2,64× | "The Second Punic War - OverSimplified (Part 1)" · 20,8 mi · 0,52× | tema universal × tema de nicho; Parte 1 > Parte 2 sempre (WW2 P2 1,7×) |
| HM | "Why didn't Castro try to retake Guantanamo Bay from America?" · 2,5 mi · 2,65× | "Why did the Treaty of Versailles Fail?" · 485 mil · 0,51× | contrafactual com protagonista famoso ("why didn't X…") × pergunta de prova escolar |
| KG | "American Revolution 1775-1783 - All Battles…" · 1,39 mi · 3,69× | "Medieval Horror Stories" · 109 mil · 0,29× (19 dias) | escopo épico e completo × rótulo vago fora da marca |
| Fern | "How an FBI Agent Infiltrated the KKK" · 16 mi · 3,58× | "The Stoner Kids Dealing Guns to the Army" · 2,6 mi · 0,58× | 1 pessoa concreta + inimigo conhecido × grupo difuso; a thumb do flop (bonecos azuis/vermelhos) não tem rosto nem alvo |
| LEMMiNO | "Cicada 3301: An Internet Mystery" · 43 mi · 6,72× | "Top 10 Facts - Space [Part 8]" · 3,1 mi · 0,48× | caso nomeado sem solução × lista genérica |
| BS | "The Dark Side Of The Silk Road" · 13,7 mi · 6,31× | "The Informant's Gambit - A Darknet Mystery" · 1 mi · 0,46× | lugar ou objeto conhecido + "dark side" × trocadilho abstrato (e thumb de xadrez) |
| AP | "¿Qué es el fascismo?" · 2,1 mi · 8,33× | "¿Siempre hemos «farmeado aura»?" · 45 mil · 0,18× | tema-ismo enorme em 20 caracteres × gíria do momento; **os 2 flops trazem o rosto do apresentador na thumb**, e os 16 do top são ilustração |
| Nerdologia | "Ainda Estou Aqui e a vida de Rubens Paiva" · 337 mil · 4,59× | "Neville Page… \| Nerdologia 09" · 4,8 mil · 0,07× | gancho de cultura pop do momento × entrevista/podcast |

**Diferenças que se repetem (3–5):**
1. **Tema conhecido > título esperto.** Em todos os canais, o flop tem tema menor ou mais obscuro, não fórmula pior.
2. **Concretude:** 1 pessoa, 1 organização ou 1 objeto nomeado (Castro, KKK, Silk Road, SS) × categoria difusa (teens, horror stories, wars).
3. **Título curto no dossiê:** hits com 38,5 caracteres × flops com 53. O aposto explicativo é sinal de flop.
4. **Conflito embutido:** "vs", "didn't", caçada, mira. Os flops descrevem; os hits colocam alguém contra alguém.
5. **Quebrar a fórmula da casa custa caro** nos canais de fórmula (AiM com NKVD 0,31×; HiM com Roma 0,38×).

---

## 5. O que separa os GRANDES (OS, Fern, LEMMiNO, KG) dos "in Minutes" pequenos
| Eixo | Grandes | HiM / AiM / Atlas / CC |
|---|---|---|
| Thumb a 160×90 | 1 ideia visual que se reconhece na hora (LEMMiNO e Fern com 1 foco; OS com duelo de rostos) | NOME + datas + panorama/figura em pé; a 160 vira uma grade de cartões-postais iguais |
| Emoção | raiva, alvo, ameaça, mistério (paleta escura, vermelho) | expressão neutra, céu claro; emoção só quando há fogo (Ucrânia) ou medo (Beria) |
| Título × thumb | Fern, LEMMiNO e BS completam ou omitem o texto (24 de 30) | repetem 100% (o nome do tema 2×) |
| Variedade | cada thumb tem um conceito próprio (Fern: mira, alfinete, 3D, foto) | molde idêntico em série: bom para marca, ruim para destacar o vídeo |
| Identidade | OS e KG também repetem o tema, mas compensam com marca forte (o personagem OS, o logo KG) e temas gigantes | marca ainda fraca: o tema precisa carregar tudo, por isso o tema decide 10× × 0,3× |
| Escopo do título | promessa de história concreta ("How an FBI Agent Infiltrated the KKK") ou caso famoso | promessa de completude ("ENTIRE… in N Minutes"), que funciona só com tema-ímã |

**Lição prática para nós:** manter a fórmula literal nos moldes (é o que performa neles) e ganhar dos grandes na **thumb**. Os ajustes:
- tema-ímã (espiões e polícia secreta no dossiê; civilização icônica ou conflito vivo na história);
- thumb com 1 foco emocional (escura ou com fogo, ameaça, objeto-documento na mão);
- o texto da thumb completa em vez de repetir quando o título já diz o tema (ex.: título "TODA la Historia del Mossad…" + thumb "LOS MÁS TEMIDOS");
- "vs" quando houver duelo real.
