# CountryCorns: dissecação (referência indicada pelo Rodrigo)

Data: 2026-11-04 · Autor: Claude Code (Opus), brief `~/workspace/referencias/BRIEF-countrycorns.md`
Fontes: `yt-dlp` via WARP (lista do canal e metadados por vídeo, 04/11 ~17h), garimpo `pesquisa/tendencias/2026-11-02.json` e `youtube.garimpo_videos` (02/11 17:40), transcrição Whisper `small` dos 5 vídeos inteiros (`dados/<id>/transcricao.txt`), detecção de cortes ffmpeg (`scene > 0,3`, `dados/<id>/cortes.json`), frames em `frames/`.
Legenda: **[O]** = observado (dado, transcrição ou frame) · **[I]** = inferido (interpretação minha, sem prova).

---

## Resumo executivo

1. **O canal que "bombou" não é o canal do humor.** [O] As thumbs de Israel, Japão e Iron Dome têm o logo **"HISTORY TAB"**: o canal mudou de nome e de formato. Os 3 vídeos que deram 1,39 mi de views são **documentários sérios**, sem nenhuma piada, com arte pintada/ilustrada. O formato com **humor e "países-milho"** (estilo countryballs) estreou na Coreia em **01/11** e tem **347 views em 3 dias** (116/dia).
2. **O canal está parado.** [O] De 02/11 para 04/11 ganhou **+343 views no total** (Israel +323, de 1.142.277 para 1.142.600). Os inscritos seguem em ~7,5 mil. O pico de Israel já passou (média de 30 mil/dia na vida, mas ~160/dia agora).
3. **O hook com humor da Coreia é bom roteiro, mas ainda não tem prova de resultado.** [O] Esquete de 8 s com os dois países-personagem ("Bro, come visit. We have K-pop, fried chicken and fast internet." / "We have a very big parade again every week."), virada séria em 7 s ("Same people, same language, same history… two countries that are still technically at war"), pergunta e "Let's go back, way back" aos 17 s. [I] O fracasso inicial pode ser da troca de formato e de público (os inscritos vieram por documentário sério sobre Israel), não do humor em si.
4. **O que dá para levar:** a técnica do "botão" cômico (piada de 2–6 palavras no fim de uma frase factual, ~1,6 por minuto), a esquete curta de abertura, a personificação de reinos com 3 traços e o silêncio cômico nos trechos trágicos. São regras que cabem no nosso tom e na nossa esteira (seção 6).
5. **Recomendação:** testar o humor no `historia-ptbr` como **camada** sobre a fórmula que já funciona ("A história INTEIRA de X em N minutos" + hook de paradoxo), **não** como troca de formato. Um vídeo de teste e medir a retenção aos 30 s contra o Egito e a Índia. **Hipótese**, sem dado nosso.

---

## 1. Levantamento do canal

Canal `UCKWRnsyYbPFgWclCF0_yOTw`, criado em 19/09/2026, país RS (Sérvia) [O, garimpo]. Descrição atual: *"History, but make it corn. Every country is a little corn character…"* [O]. Tags do vídeo da Coreia incluem `bulgariancb`, `countryballs`, `polandball` [O]: o formato novo mira o público dos canais de countryballs.

| Vídeo | Publicado | Duração | Views (04/11) | Dias | Views/dia | Δ desde 02/11 | Likes | Coment. | Fase |
|---|---|---|---|---|---|---|---|---|---|
| [The ENTIRE History of Israel in 10 Minutes](https://www.youtube.com/watch?v=ihGK1iyUN1E) | 27/09 | 8:46 | **1.142.600** | 38 | 30.068 | +323 | 5.307 | 832 | History Tab |
| [The Entire History of Japan in 10 Minutes \| Animated History](https://www.youtube.com/watch?v=JKWqT5SiT8w) | 01/10 | 12:00 | 115.546 | 34 | 3.398 | +125 | 806 | 59 | History Tab |
| [The ENTIRE history of Israel's Iron Dome in 10 Minutes](https://www.youtube.com/watch?v=CaZN6e-MESs) | 04/10 | 8:30 | 131.436 | 31 | 4.240 | +140 | 817 | 138 | History Tab |
| [Why Are There Two Koreas? \| The History of Korea](https://www.youtube.com/watch?v=HHIQeJqnkuE) | 01/11 | 10:20 | 347 | 3 | 116 | +106 | 11 | 9 | CountryCorns |
| [Korea Was Free for 5 Minutes…Then Came the Line #shorts](https://www.youtube.com/shorts/rDCe0M8QsXM) | 01/11 | 0:51 | 51 | 3 | 17 | +23 | 3 | 1 | CountryCorns |
| **Total** | | | **1.389.980** | | | **+343** | | | |

- Inscritos: 7.510 em 02/11 (API) → "7,5 mil" em 04/11 (página, valor arredondado) [O].
- 82% das views vêm de um vídeo (Israel) [O]. Hiato de 4 semanas entre Iron Dome (04/10) e Coreia (01/11) [O].
- Israel e Japão terminam prometendo **"part two, coming soon"**, e a parte 2 nunca saiu [O].
- "Views/dia" é a média da vida do vídeo. Pelo Δ de 2 dias, o ritmo **atual** é ~160/dia (Israel), ~60/dia (Japão) e ~70/dia (Iron Dome) [O]. [I] Israel teve um pico de recomendação nas primeiras semanas (tema quente) e morreu.
- Nada foi gravado em `youtube.assistidos`/`garimpo_*` nesta rodada (o brief limita a escrita a esta pasta).

## 2. O hook com humor (Coreia, HHIQeJqnkuE)

### Transcrição dos primeiros 60 s [O]
Tempos por palavra (Whisper `small`, `word_timestamps`):
```
0:00.0  [Coreia do Sul, personagem]  "Bro, come visit. We have K-pop, fried chicken and fast internet."   (até 3,2 s)
0:03.9  [Coreia do Norte, personagem] "We have a very big parade… again… every week."                      (até 7,6 s, pausas longas)
0:08.0  [narrador] Same people, same language, same history for thousands of years. And today, two countries
        that are still technically at war.                                    (texto na tela: TECHNICALLY AT WAR + explosão)
0:15.2  So how did this happen?
0:17.4  Let's go back. Way back. About 4,000 years.          (cartão "THE HISTORY OF KOREA" → "2333 BC")
0:21.3  Korea's origin story starts with a bear and a tiger.   (cartão "CHAPTER 1 · A BEAR, A TIGER AND A KINGDOM")
0:24.0  They both want to become human. The God of the sky gives them a deal: stay in a cave, eat nothing but
        garlic and mugwort, and avoid sunlight. The tiger quits early. Fair enough.
0:35.2  The bear sticks it out and turns into a woman. Her son, Dangun, founds the first Korean kingdom, Gojoseon.
        Tradition dates it to 2333 BC. Is that real history? No. Is it a great flex? Absolutely.
0:48.0  Every October, South Korea still celebrates it as National Foundation Day.
0:54.4  Gojoseon lasted a long time, until a big neighbor showed up. In 108 BC China's Han dynasty conquered it,
        and that sets up a theme you'll see for the rest of this video: Korea is small, its neighbors are big,
        and everyone wants a piece.
```
Frames: `frames/HHIQeJqnkuE/hook_60s_2s.jpg` (1 frame a cada 2 s) e `f001.jpg` (Coreia do Sul de óculos escuros, celular e microfone, em cima do mapa azul; Coreia do Norte de quepe e fuzil em cima do mapa vermelho).

### Que tipo de piada é
- **Esquete de contraste por estereótipo** [O]: dois personagens-país, cada um com uma fala que resume o país em 1 traço (o Sul "influencer" vendendo turismo; o Norte orgulhoso de algo absurdo, as paradas militares). A piada está no **contraste entre as duas falas**, sem explicação. [I] As falas parecem ter voz/entonação de personagem: o tom é mais agudo na fala do Sul (0–1,2 s) e a do Norte vem lenta e seca, com pausas. O medidor de tom é ruidoso por causa da trilha; não dá para afirmar que são vozes diferentes.
- **Timing** [O]: 3,2 s + pausa de 0,7 s + 3,7 s. A segunda fala é a punchline, dita mais devagar ("again… every week") e seguida de silêncio curto antes do narrador.
- **Passagem do humor para a promessa** [O]: o narrador entra **sério**, com 3 repetições ("same people, same language, same history") e o paradoxo ("two countries… still technically at war") com a palavra de impacto na tela. Pergunta central aos 15 s, "let's go back, way back" aos 17 s, título do vídeo na tela aos 16 s, capítulo 1 aos 22 s. **Hook inteiro: ~21 s** (o nosso Egito leva 49 s).
- [I] A esquete faz o trabalho do nosso "paradoxo": mostra o contraste (Sul rico × Norte militarizado) em vez de dizê-lo, e a frase séria seguinte o nomeia.

### Onde o humor reaparece [O]
16 piadas em 10:20 (~1,6 por minuto), quase todas "botões" de 2–6 palavras no fim de uma frase factual:

| Tempo | Piada | Técnica |
|---|---|---|
| 0:00 | esquete Sul × Norte | esquete de contraste |
| 0:33 | "The tiger quits early. Fair enough." | comentário seco |
| 0:44 | "Is that real history? No. Is it a great flex? Absolutely." | pergunta e auto-resposta |
| 1:10 | Goguryeo "big, tough and good with horses"; Baekje "rich, artsy, friends with Japan"; Silla "small, quiet and playing the long game" | personificação em 3 traços |
| 1:48 | "Rule one of invading Goguryeo: don't." | regra cômica |
| 2:04 | "Tang said: great, now it's all ours. Silla said: yeah… no." | diálogo entre países |
| 2:34 | "So, almost unified. Close enough." | botão |
| 2:50 | "Say Goryeo fast… Yep. That's where the name Korea comes from." | jogo com o espectador |
| 3:49 | "Basically a whole country raised by a strict teacher." | analogia cotidiana |
| 4:29 | "Gave his whole country a free education upgrade. Legend behavior." | gíria de internet |
| 6:16 | "Korea was free… for about five minutes." | pausa + virada (vira o título do Short) |
| 6:40 | "It was supposed to be temporary. Spoiler: it wasn't." | spoiler |
| 7:17 | "It was a crazy gamble." | comentário |
| 7:31 | "Then China said: nope." (na tela: NOPE) | diálogo entre países |
| 9:31 | "From space at night you can literally see the difference. The south glows. The north is almost dark." | imagem-punchline (mapa noturno) |
| 10:12 | "History is way more fun when it's corny." | trocadilho de assinatura |

- **Onde NÃO tem humor** [O]: ocupação japonesa (5:50–6:15), mortes da guerra ("Millions died", 8:04), fome no Norte (9:23) e o fecho ("families were split… many never saw each other again"). O humor some nos trechos trágicos e volta com um botão leve logo depois ("free for about five minutes" fecha a ocupação).
- **Visual da piada** [O]: o personagem reage (ponto de exclamação, "!?", gota de suor), a palavra-chave aparece em rótulo amarelo ("SPOILER", "NOPE", "LEGEND") e o mapa muda de cor. Ver `frames/HHIQeJqnkuE/piadas_sheet.jpg`.

## 3. Título, thumb, roteiro e duração

### Título [O]
- Fase History Tab: **"The ENTIRE History of X in 10 Minutes"** nos 3 vídeos, sempre "10" (durações reais de 8:30 a 12:00: o N não bate com a duração). Japão sem caixa alta, com sufixo "| Animated History".
- Coreia: **pergunta "Why Are There Two Koreas?"** + "| The History of Korea". Sem "ENTIRE" e sem "N minutes".
- "Why…?" × "ENTIRE": **não dá para comparar** com estes dados (formato, tema e idade diferentes). O que existe: ENTIRE = 115 mil–1,1 mi; Why = 347 em 3 dias, junto com a troca de formato. [I] A pergunta "Why are there two Koreas?" é o paradoxo do hook virado título (curiosidade que se responde no fim). É o mesmo padrão "Pourquoi…?" do `lotr-fr`.

### Thumb [O] (`frames/thumbs_4.jpg`)
- História Tab: personagem (líder político caricato, samurai, soldado) **apontando para a palavra gigante** amarela (ISRAEL/JAPAN) com "THE HISTORY OF" em cima e datas em pílula vermelha ("1948 – 2026", "14,000 BCE – 2026"); fundo pôr do sol vermelho com o lugar; selo "HISTORY TAB" no canto.
- Coreia: dois personagens-milho **frente a frente** (Norte de quepe e fuzil, com veia de raiva; Sul de óculos escuros), fundo dividido em dois (cerca e torre de vigia × skyline com a N Seoul Tower), raio no meio, "KOREA" gigante amarelo, pílula "ONE KOREA → TWO" e etiqueta "38°N". Conflito visual em 1 olhar.

### Estrutura de roteiro
| | Israel (History Tab) | Japão (History Tab) | Iron Dome (History Tab) | Coreia (CountryCorns) |
|---|---|---|---|---|
| Hook [O] | cena datada (14/05/1948, 4 da tarde, 37 assinaturas) → "somehow, that state is still here. Keep that room in mind" → paradoxo do território → **6 perguntas** → "we have to go back…" aos 3:16 | cena datada (Hiroshima, 6/8/1945, 8h15) → rendição → "within a generation… largest economies" → pergunta aos 52 s → volta aos 1:03 | "imagine a rocket flying toward a crowded city" → "This is Israel's Iron Dome" (13 s) → **pedido de inscrição aos 15 s** → pergunta aos 24 s | esquete 8 s → paradoxo → pergunta aos 15 s → volta aos 17 s |
| Capítulos [O] | sem capítulos na descrição; termina no meio (Cruzadas) com "part two coming soon" | 8 capítulos na descrição; termina em 1868 com "part two coming soon" | 8 capítulos na descrição | sem capítulos na descrição; cartão "CHAPTER 1…" na tela e rótulo "OUTRO" |
| Fio condutor [O] | "keep that room in mind" (não pago no vídeo) | "how did islands become… the Japan we recognize?" (adiado para a parte 2) | tecnologia × ameaça | **"Korea is small, its neighbors are big, everyone wants a piece"** (1:06), pago no fim |
| Fecho [O] | pedido de inscrição para a parte 2 | pergunta + "part two" | resumo + "YouTube Algorithm says you'll like my next video" | **recapitulação cômica em 1 frase** ("a bear-born kingdom that survived the Mongols, beat a samurai invasion with 13 ships, invented its own alphabet and then got split in two by a ruler and a map") → nota emocional (famílias separadas) → pergunta "will they ever reunite?" → "North or South Korea next?" → trocadilho |
| Palavras/min [O] | 128 | 126 | 140 | **156** |
| Duração [O] | 8:46 | 12:00 | 8:30 | 10:20 |

- [I] A Coreia é o roteiro mais redondo dos 4: cobre 4.000 anos em 10 min com loop pago, e não corta a história em "parte 1". Os History Tab vendem "ENTIRE" e entregam meia história.

## 4. Edição

| | Israel | Japão | Iron Dome | Coreia |
|---|---|---|---|---|
| Estilo visual [O] | ilustração pintada realista, tons sépia/pergaminho, mapas em pergaminho | ilustração tipo gravura japonesa, sépia, personagens de rosto simples | quadrinho sépia com bonecos de cabeça redonda (estilo stickman) | **cartoon chapado (countryballs em forma de milho)**, mapas planos de cor sólida, cenários vetoriais |
| Cortes/min (média; 1º min) [O] | 12,3; 12 | 12,2; 4 | 18,7; 17 | **9,7; 10** (pico de 14 nos min 3–4) |
| Texto na tela [O] | rótulos de mapa e linha do tempo | pouco | pouco | **rótulo amarelo em quase todo plano** (data, nome, palavra da piada: SPOILER, NOPE, LEGEND), cartões de capítulo |
| Mapas [O] | pergaminho com setas e exércitos | mapa simples do arquipélago | mapas de cidade | **mapa político de cor chapada com o personagem em cima**; a cor muda conforme o domínio |
| Voz [I] | narrador masculino em inglês, calmo, documental; provável TTS | idem | idem, com o mesmo bordão "A fast reminder guys…" | narrador masculino mais solto, gírias (bro, flex, nope, spoiler), 156 palavras/min; provável TTS; falas de personagem no hook |
| Música/SFX [I] | trilha de fundo constante (a voz nunca cai a silêncio absoluto) | idem | idem | trilha leve + SFX de explosão/pop nos rótulos (visto nos frames) |

- [I] O cortes/min baixo da Coreia engana: os personagens se mexem dentro do plano (reações, piscadas, rótulos que entram), então o olho recebe estímulo novo mais vezes do que o número de cortes indica. O detector de cena só pega troca de plano.
- [I] Três estilos visuais em 4 vídeos: o canal está experimentando, não tem identidade estável.

## 5. Diferença para History in Minutes e Archive in Minutes

| | History in Minutes (Egito, VQPzrVMHWlg) | Archive in Minutes (Gestapo, pbIzG1QvoWs) | CountryCorns (Coreia) |
|---|---|---|---|
| Hook [O] | paradoxo geográfico ("Egypt is a river with a country stuck to its banks") + escala de tempo; ~45 s | anedota humana datada com desfecho cruel (a piada da viúva), 15 s até a promessa | **esquete cômica de 8 s** + paradoxo sério; ~21 s até o capítulo 1 |
| Tom [O] | sério, maravilhado, frases de efeito | sombrio, frio, factual | **leve e irreverente**, gírias de internet; sério nas tragédias |
| Ritmo [O] | ~195 palavras/min, 14 cortes/min no início | 20 cortes/min no início, capítulos de 1–2 palavras ("The stamp", "The cellar") | 156 palavras/min, ~10 cortes/min + animação de personagem |
| Visual [O] | ilustração pintada | quadrinho com contorno grosso + palavra amarela | cartoon chapado com mascotes-país |
| Título [O] | "The ENTIRE History of X in N Minutes" (N = duração real) | idem | "Why…? \| The History of X" |
| Fecho [O] | volta ao presente | volta à cena do começo ("The cellar") | recapitulação cômica + nota emocional + pergunta |

O que CountryCorns faz que os outros dois não fazem: **personagens recorrentes que falam** (países com personalidade), **humor como ritmo** (um botão a cada ~40 s) e a **recapitulação em uma frase** que lista as conquistas como piada. Os outros dois mantêm a voz de documentário do começo ao fim.

## 6. Como aplicar no `historia-ptbr`

### Regras (reaproveitáveis)
1. **Humor é camada, não formato.** Mantenha a fórmula que já está no canal (título "INTEIRA", hook de paradoxo/anedota, capítulos cronológicos). O humor entra como esquete curta na abertura e botões ao longo do texto. Motivo: o único vídeo de humor do CountryCorns ainda não provou nada (347 views), e o público que veio por documentário pode estranhar a troca. **Hipótese.**
2. **Esquete de abertura de até 8 s, com 2 falas e 1 contraste.** Duas "vozes" (dois países, dois momentos do mesmo país, ou governante × conselheiro), uma fala cada; a segunda é a punchline, mais lenta. Logo depois, o narrador entra **sério** com a frase que nomeia o paradoxo. A pergunta central vem até os 20 s, e o hook todo fecha em até ~40 s (nossa regra atual).
3. **Botão de 2–6 palavras no fim de uma frase factual, ~1 a cada 40–60 s** (~15–20 num vídeo de 17 min). Fórmulas que funcionam em pt-BR:
   - **pergunta e auto-resposta:** "É história de verdade? Não. É uma ótima carteirada? Com certeza."
   - **spoiler:** "Era para ser temporário. Spoiler: não foi."
   - **"quase":** "Quase unificado. Quase."
   - **diálogo entre países/impérios:** "A dinastia Tang disse: ótimo, agora é tudo meu. Silla respondeu: então… não."
   - **regra cômica:** "Regra número um para invadir a Rússia: não invada no inverno."
   - **analogia cotidiana:** "Basicamente um país inteiro criado por um professor muito rígido."
   - **personificação em 3 traços:** "Goguryeo: grande, brigão e bom de cavalo. Baekje: rico, artista e amigo do Japão. Silla: pequeno, quieto e jogando a longo prazo."
   Use gíria brasileira com moderação ("deu ruim", "plot twist", "carteirada", "ele achou que era só passar") e **nunca traduza a gíria americana** ("legend behavior" não vira nada natural em pt-BR).
4. **Silêncio cômico nas tragédias.** Nenhuma piada em guerras com mortos, genocídio, escravidão, fome, ocupação ou conflitos em curso, nem no minuto em volta. Depois do trecho trágico, só um botão **leve e sobre a política**, nunca sobre as vítimas ("Livre… por uns cinco minutos").
5. **Feche com recapitulação cômica em 1 frase** (lista de 4 feitos do país, o último inesperado), depois uma nota emocional curta e a pergunta para os comentários (+ "qual país vem depois?").
6. **Fio condutor dito em voz alta no 1º minuto** ("e isso cria um padrão que você vai ver no vídeo inteiro: …") e pago no fim. Já é regra nossa; a Coreia mostra a frase-modelo.
7. **Na esteira:**
   - Fish: a punchline curta **não pode** fechar bloco depois de `[break]` (o Fish corta, ver `conhecimento/hooks.md`). Ponha a pausa **antes** da punchline e a punchline no meio do bloco, ou com tag de tom.
   - Falas da esquete: tag `[playful]`/`[sarcastic]` na mesma voz clonada; uma 2ª voz Fish seria gasto e decisão do Rodrigo.
   - Storyboard: o plano da punchline tem reação do personagem-guia do canal (o "bonequinho" já previsto no `estilo.md`) e, no máximo, 1 palavra de rótulo na tela. Continua sem legenda queimada.
8. **Medir:** 1 vídeo com a camada de humor, comparar a retenção aos 30 s e o % assistido com Egito e Índia (`report.py --retencao`). Só vira regra depois disso.

### 3 aberturas escritas para o backlog (para usar como rascunho, fatos conferidos de memória: revisar no `SOURCES.md`)

**Japão** (~35 s)
> — Japão, 1640: "Estrangeiro? Não, obrigado. Fechado para balanço."
> — Japão, 1870: "Quero ferrovia, fábrica, marinha e um terno igual ao seu. Para ontem."
> [narrador, sério] Em menos de quarenta anos, um país de samurais e espadas virou uma potência industrial que afundou a frota da Rússia. Poucos países no mundo mudaram tão rápido.
> Então como um arquipélago que passou mais de dois séculos com a porta trancada saiu de lá correndo na frente de quase todo mundo?
> Vamos voltar. Bem para trás. Uns dezesseis mil anos, quando quem vivia nessas ilhas já fazia uma coisa que quase ninguém na Terra sabia fazer: panela de barro.

(Fatos a conferir: éditos de reclusão 1633–1639; Restauração Meiji em 1868; primeira ferrovia em 1872; Tsushima em 1905; cerâmica Jōmon ~14000 a.C.)

**Roma** (~35 s)
> Roma começou com dois irmãos criados por uma loba. Um deles matou o outro por causa de um muro.
> É história de verdade? Provavelmente não. É um ótimo trailer do que vinha pela frente? Com certeza.
> [narrador, sério] Uma vila de pastores na beira do Tibre virou dona de todo o Mediterrâneo. E nunca foi embora: está no seu calendário, nas suas leis e na língua que você está ouvindo agora.
> Então como uma vila sem nada de especial conquistou o mundo conhecido… e como alguém conseguiu derrubar isso?
> Nossa história começa em 753 antes de Cristo. Pelo menos é o que os romanos diziam.

(Fatos a conferir: fundação tradicional em 753 a.C.; Rômulo e Remo; calendário juliano → gregoriano; português vem do latim.)

**China** (~35 s)
> — Imperador, os povos do norte estão atacando de novo.
> — Constrói um muro.
> — Construímos. Eles passaram.
> — … Constrói um muro maior.
> [narrador, sério] A China passou quase dois mil anos erguendo muralhas e, mesmo assim, foi conquistada inteira duas vezes: pelos mongóis e pelos manchus. E aqui está a parte estranha: no fim, quem acabou governando à moda chinesa foram os conquistadores.
> Então como um país que caiu tantas vezes continua sendo o mesmo país há mais de três mil anos?
> Vamos voltar uns 3.200 anos, até reis que faziam perguntas aos avós mortos… escrevendo em ossos.

(Fatos a conferir: muralhas desde ~século VII a.C.; dinastia Yuan 1271–1368; Qing 1644–1912; ossos oraculares Shang ~1250–1050 a.C.)

---

## Propostas para conhecimento/ e skills/roteiro
(para o Rodrigo aplicar; não editei fora desta pasta)

**`conhecimento/hooks.md`, nova entrada em Evidências:**
> ### Referência: hook com esquete cômica (CountryCorns, Coreia), 2026-11-04
> Fonte: `pesquisa/countrycorns/ANALISE.md` (Whisper com tempos por palavra; frames).
> Esquete de 8 s com dois países-personagem (Sul: "Bro, come visit. We have K-pop, fried chicken and fast internet." / Norte: "We have a very big parade… again… every week.") → narrador sério com o paradoxo ("two countries that are still technically at war") → pergunta aos 15 s → capítulo 1 aos 22 s.
> - **Sem prova de resultado:** 347 views em 3 dias (04/11). Os vídeos do canal que bombaram (Israel 1,14 mi) são da fase anterior ("History Tab"), sérios e sem humor.
> - **Hipótese:** esquete de ≤ 8 s + paradoxo sério segura tanto quanto o paradoxo sozinho e diferencia o canal. Testar em 1 vídeo do historia-ptbr e medir a retenção aos 30 s.

**`conhecimento/hooks.md`, Regras rápidas, Faça:**
> - (Hipótese, a testar) Abertura com **esquete de até 8 s** (2 falas, 1 contraste), seguida do paradoxo dito sério pelo narrador. Hook inteiro ≤ 40 s. [pesquisa/countrycorns/ANALISE.md]

**`conhecimento/roteiros.md`, Regras rápidas, Faça:**
> - (Hipótese) **Humor como ritmo:** um "botão" de 2–6 palavras no fim de uma frase factual a cada ~40–60 s (pergunta e auto-resposta, "Spoiler: não foi", diálogo entre impérios, personificação em 3 traços, analogia cotidiana). Nenhuma piada em tragédia (guerra com mortos, genocídio, escravidão, fome) nem no minuto em volta. [CountryCorns, Coreia: 16 botões em 10:20; pesquisa/countrycorns/ANALISE.md]
> - **Fecho com recapitulação em 1 frase** (4 feitos do país, o último inesperado) → nota emocional → pergunta + "qual país vem depois?". [idem]

**`conhecimento/roteiros.md`, Não faça:**
> - Não prometa "INTEIRA" e entregue "parte 1": Israel e Japão do History Tab terminam com "part two coming soon", e a parte 2 nunca saiu. [pesquisa/countrycorns/ANALISE.md]

**`conhecimento/titulos.md`, Referências de título:**
> - CountryCorns (2026-11-04): a fase "ENTIRE History of X in 10 Minutes" (N fixo em 10, durações reais de 8:30 a 12:00) fez 115 mil–1,14 mi; o 1º título em pergunta ("Why Are There Two Koreas? | The History of Korea") fez 347 views em 3 dias, junto com a troca de formato. **Sem base** para concluir "Why" × "ENTIRE". Mantemos "INTEIRA" + N real.

**`conhecimento/anti-padroes.md`** (para avisar quem for imitar):
> - **Trocar de formato num canal que cresceu com outro** (CountryCorns: de documentário sério a cartoon cômico) zerou o ritmo: 347 views no 1º vídeo novo. **Hipótese:** o público e o algoritmo do formato antigo não acompanham. Teste formato novo como variação dentro do mesmo estilo.

**`skills/roteiro/SKILL.md`, novo item no checklist do hook e do corpo:**
> - Se o brief pedir humor: esquete de abertura ≤ 8 s (2 falas, tag `[playful]`/`[sarcastic]`, punchline mais lenta), botões de 2–6 palavras a cada ~40–60 s, zero piada em tragédia e recapitulação cômica no fecho. Punchline nunca fecha bloco depois de `[break]` (o Fish corta). Liste os botões no `SCRIPT.md` com o tempo aproximado para o storyboard planejar a reação do personagem-guia.

---

## Arquivos desta pasta
- `dados/flat-videos.json`, `dados/flat-shorts.json`: lista do canal (yt-dlp, 04/11).
- `dados/<id>/meta.json` (título, data, duração, views, likes, comentários, tags, capítulos, descrição), `transcricao.txt` (Whisper `small`, vídeo inteiro), `cortes.json` (cortes por minuto).
- `frames/thumbs_4.jpg` (4 thumbs lado a lado), `frames/<id>/thumb.jpg`, `hook_60s_2s.jpg`, `video_24.jpg`, `f*.jpg`; `frames/HHIQeJqnkuE/piadas_sheet.jpg` e `piadas/` (frames nos momentos de humor).
- Limitações: Whisper `small` erra nomes próprios coreanos (ex.: "go Joe's son" = Gojoseon); a análise de voz (IA × humana, número de vozes) é inferida, sem ouvir; frames em 480p.
