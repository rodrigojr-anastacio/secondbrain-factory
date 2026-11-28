# Dossier en Minutos: teste do formato "cómo era vivir / formar parte de" (1 vídeo por semana), proposta fase 1 (28/11/2026)

Brief: `~/workspace/referencias/BRIEF-dossie-formato-como-era-vivir.md` (ideia do Rodrigo, 28/11). **Só proposta.** Bíblia, backlog, agenda de 28/11–01/12 ('Ndrangheta, Mafia rusa, ODESSA, 5 Familias), banco e fila ficaram como estavam. Custo pago: US$ 0.
**Fontes (28/11/2026):** 56 buscas do YouTube via yt-dlp + WARP, ordenadas por views e filtradas para uploads de 2026 (44 em es, 12 em en: "cómo era vivir en…", "así era…", "un día en la vida de…", "tu vida en cada nivel…", "no sobrevivirías…", "cómo funcionaba X por dentro"…). Isso deu 897 vídeos, com views, data, duração e canal tirados da Data API (`videos.list`/`channels.list`, token readonly do dossie-es, ~40 unidades, sem `search.list`). Pela mesma API, a mediana dos últimos 20 vídeos longos de 28 canais do formato (≈ 120 unidades), para calcular "×med" = views ÷ mediana do canal. O autocomplete do YouTube (es/MX) veio pelo WARP. Brutos e scripts ficaram fora do git, em `~/cache/tmp/cev/` (`coleta.py`, `stats.py`, `canais.py`, `busca.json`, `stats.json`, `canais.json`). Também li `analises/2026-11-27-diagnostico.md`, `…-bolha-opcoes.md`, `…-cosa-nostra-2.md`, a bíblia e `canais/historia-ptbr/v3-proposta/` (anatomia do formato em pt/en).
**Limite:** nenhum vídeo do formato foi transcrito nesta fase. A manada de cada tema (`manada.py`, detector, crivo de ângulo) fica para a embalagem/roteiro de cada vídeo, como manda a bíblia.

---

## 0. Resposta curta
- **Há demanda, mas em es ela tem dono, e o dono é o nosso vizinho.** Em 2026, o "Tu vida en cada nivel/rango de X" do **Te lo Pinto** (615 mil inscritos, mediana 99,5 mil) fez Mafia Italiana 1,38 mi (13,9×), CIA 1,21 mi (12×), Yakuza 1,27 mi (12,7×) e Templario 2,33 mi (23×). Canais pequenos repetem a fórmula com folga: Dolor Pintado, Sinaloa 238 mil (22×); Tu Vida Como (2 mil inscritos), narco 333 mil (23×); POV Rangos (1,8 mil inscritos), KGB 68 mil (4,5×). Desde novembro, o Te lo Pinto também entrou no **nosso** molde ("Toda la Historia del Mossad Resumida" 517 mil; "La HISTORIA COMPLETA de las SS en Minutos" 198 mil). Ou seja, o público do "por dentro" e o nosso já são o mesmo bairro.
- **Onde há espaço:** o "rango" é uma escada animada, genérica e fictícia, sem data nem documento. Ninguém em es faz "**uma época, um lugar, um recluta de verdade, em expedientes**". A busca (autocomplete) puxa **regime/época** ("cómo era vivir en la unión soviética / en la URSS", "cómo era Cuba antes de 1959 / en 1958", "cómo era vivir en la Alemania oriental"). O sugerido puxa **máfia por dentro**.
- **Recomendação:** testar 3 vídeos, um por semana, no **slot de terça à noite** (publicação sex/sáb), a partir de **08/12**: **Cosa Nostra (Sicília anos 70)** → **La Habana 1957 (a máfia dos cassinos)** → **KGB (ser um "ilegal")**. Critério: CTR ≥ 4% no sugerido em 48 h em 2 de 3 **e** 7 d ≥ 1,5× a mediana dos 3 vídeos-padrão da mesma semana. Corte antecipado se os 2 primeiros ficarem < 2%.

---

## 1. Demanda (vídeos de 2026)

### 1a. Espanhol: o que existe e quanto faz
| padrão | exemplos reais 2026 (views · data · ×mediana do canal) | leitura |
|---|---|---|
| **"Tu vida en cada nivel/rango de [org]"** | Te lo Pinto: [Mafia Italiana](https://youtu.be/fc-GrwCeQzY) 1.381.488 · 16/05 · 13,9×; [Cómo es Ser Cada Rango de la Yakuza](https://youtu.be/aN_Wl0RYbbQ) 1.265.210 · 08/02 · 12,7×; [CIA](https://youtu.be/Z28eE95EYNQ) 1.211.754 · 03/04 · 12×; [Templario](https://youtu.be/G7VYGchTvjs) 2.326.337 · 29/05 · 23×; [Mafia rusa](https://youtu.be/kGtGYEKwjL8) 448.173 · 4,5×; [MI6](https://youtu.be/sgATwpm7sF4) 215.015 · 2,2×; [Mafia albanesa](https://youtu.be/VhAZ27bfq-E) 191.118 · 1,9×. Dolor Pintado "Cómo Se Siente Ser Cada Rango del Cártel de Sinaloa" 237.593 (22×). [Tu Vida Como Narco En Cada Nivel](https://youtu.be/tZEnllApKug) 332.783 (canal de 2,2 mil inscritos, 23×). POV Rangos (criado 09/2026, 1,8 mil): [KGB](https://youtu.be/TIh8QUZtWxQ) 68.515 (4,5×), Cártel 62.909, CIA 61.475, Mafia 32.086, Yakuza 18.923 | O formato que mais rende no bairro. **Tem dono** (Te lo Pinto) e já mostra fadiga nos clones: o POV Rangos caiu para ~1–2 mil por vídeo em novembro. **Não copiar o título.** |
| **"Cómo funciona X por dentro"** | Te lo Pinto [Así Funciona la KGB Desde Dentro](https://youtu.be/by7uTDjSx7Y) 354.039 · 30/10 · 3,6×; [Así Funcionaba por Dentro la Policía Nazi del Tercer Reich](https://youtu.be/oWkkPoYFC5o) 300.481 · 04/11 · 3,0× | Mesmo dono, versão documental de 36–43 min. Prova o tema KGB/Gestapo "por dentro" em es. |
| **"Así era la vida real de un X (no como en las películas)"** | Tercios de Tinta (criado 25/10/2026, 3,3 mil inscritos): [soldado estadounidense](https://youtu.be/0YyeY3NAfTQ) 520.499 (29×); [soldado español en Rusia (División Azul)](https://youtu.be/fQ5jTGYwSIk) 81.218 (4,5×); [soldado alemán](https://youtu.be/djo68vjgvNE) 69.594 (3,9×) | **Outlier de canal novo e pequeno**: 1 época + 1 papel + "de verdade". É o mais perto do que propomos. |
| **"¿Qué se sentía ser…?" / "¿Cómo lo vivieron…?"** | Historia Militar (mediana 21 mil): [¿Qué se SENTÍA ser un SOLDADO de las SS?](https://youtu.be/EdrwT1QTSbM) 307.318 (14,6×); [Desde el punto de vista nazi: ¿cómo lo vivieron los soldados alemanes?](https://youtu.be/vjzGlwdFlqg) 402.823 (19×); [Así VIVÍAN en Berlín después de la muerte de Hitler](https://youtu.be/ZbQwTQaZb8k) 1.292.586 (61×) | O "vivir" num canal de história militar com o nosso público (homens 45+) vai 15–60× acima da mediana. |
| **"Así era (vivir en) [lugar] antes de…"** (reconstrução IA) | Reimaginando Pasados (mediana 18,5 mil): [Así Era La Noche De Lujo En La Habana Antes De La Revolución](https://youtu.be/5hA3VrAFiYk) 388.524 (21×); "Así Era Vivir En Las Calles De La Habana…" 103.249 (5,6×); mas "Así la Mafia Estadounidense Convirtió La Habana en un Imperio de Casinos" 20.276 (1,1×). ElDiaQue [Así Era Cuba Antes de Fidel](https://youtu.be/NhjKz5AVuqI) 236.092. Gabriel Herrera "Así era 'VIVIR' en el primer campo de concentración nazi (Dachau)" 592.925 (2,1×) | Lugar + época vende. A palavra "mafia" no título da Habana **não** ajudou: o que puxa é "vivir / noche de lujo / antes de". |
| **"Por qué no sobrevivirías como X"** | Atlax (22,7 mil): "…como Premio del Guerrero (Imperio Azteca)" 279.452 (6,5×); La Vida Victoriana "1880: Por qué no sobrevivirías a un día como sirvienta" 656.553 (27×); Rose Bennet "El régimen de Stalin: ¿habrías sobrevivido?" 533.844 | Funciona em es, mas os temas são sexuais/tabus (Atlax, como o Bernard em en) ou cotidiano antigo. **Fora do nosso tom.** |
| **Regimes "cómo era vivir en"** | URSS: Te lo Pinto "¿Sobrevivirías un Año en la Unión Soviética?" 262.169 (2,6×); El Caminante "Así era la vida en un crucero soviético" 207.107 (2,7×). Alemania Oriental/Stasi: Rose Bennet "El MURO de BERLÍN era Peor de lo que Imaginabas" 465.143; AndyGM "La historia real de la Stasi" 59.631; "Tu vida en cada rango de la Stasi" (SIGILO) 621 | URSS tem busca; Stasi segue fraca em es (a bíblia já dizia isso: 10× menos que em en). |

**Autocomplete (es/MX, 28/11):** "cómo era vivir en **la unión soviética** / **la urss**", "cómo era **cuba antes de 1959** / **en los años 50** / **en 1958** / antes del comunismo", "cómo era vivir en **la alemania oriental**", "cómo era ser un soldado en la segunda guerra mundial". **"Cómo era vivir en la mafia" não aparece** (só "cómo era la mafia"). Leitura: **máfia "por dentro" vive do sugerido/navegação**, que é o caminho do Dossier (o diagnóstico de 27/11 mostra que quase tudo nosso vem de sugerido). **Regime/época tem busca**, o que é um bônus.

### 1b. Inglês (referência)
- Ranks: Hypothetically "Your Life as Every Rank in the Italian Mafia" 3,03 mi (12/2025, 11,5×) e Yakuza 1,92 mi (7,3×); The Life Outline (criado 01/2026) Mexican Cartel 7,56 mi, MS-13 3,64 mi, Bratva 818 mil; POVrank (criado 03/2026): Medellín 1,05 mi, Mafia 594 mil, Yakuza 499 mil, **KGB 337 mil**, Stasi 110 mil, SS 57 mil; POV Tales (7,8 mil inscritos) "CIA Black Ops Rank" 2,53 mi (2.700×).
- Testemunho: Soft White Underbelly "A Day in the Life of a Gambino Family Mobster" 435 mil; Franzese "What Do Mobsters Actually Do All Day?" 1,68 mi; ex-espião ilegal da KGB **Jack Barsky** no Raj Shamani 1,92 mi.
- "Why you wouldn't survive": Fossil 13,6 mi; o resto é pré-história e ficção. Em temas de regime, é fraco ("…in the Soviet Union" med top-10 16 mil).

### 1c. Manada e outliers: o que isso diz
1. O formato "por dentro" é o que **mais cresce no nosso bairro** em 2026, e os canais pequenos que acertam o tema passam de 4× a 30× a própria mediana (Tercios de Tinta, Tu Vida Como, POV Rangos no início, Dolor Pintado).
2. **Os temas campeões são exatamente os nossos:** mafia italiana, yakuza, KGB, CIA, SS/Gestapo, templários. Os narcos rendem ainda mais, mas ficam na bolha onde o Medellín morreu (0,54%, diagnóstico de 27/11).
3. A manada é **fictícia e escalonada** (rango 1 → rango 10, "você", sem data, sem fonte) ou **reconstrução IA de lugar**. Nenhum vídeo em es ancora a 2ª pessoa num **ano, num lugar e num recluta documentado**. Esse é o ângulo do Dossier.
4. **Risco de fadiga:** os clones de ranks em es caíram para 1–2 mil por vídeo em ~6 semanas (POV Rangos, Mr. Billy). A forma "escada" não é o diferencial; o expediente é.

---

## 2. A versão "Dossier" do formato (sem descaracterizar)

### 2a. A ideia em 1 linha
**"EXPEDIENTE DE INGRESO":** o espectador recebe a ficha de entrada numa organização, **num ano e num lugar exatos**. Cada expediente é uma etapa da vida lá dentro (entrada → juramento → regras → dinheiro → rotina → castigo → saída), contada em **2ª pessoa ("tú")** e **provada pelo documento ou pelo depoimento de um recluta real**, que é o fio do vídeo.

### 2b. Esqueleto (8 passos)
| # | bloco | o que faz | duração | exemplo (Cosa Nostra, Sicília anos 70) |
|---|---|---|---|---|
| 0 | **Hook (cena física, 2ª pessoa)** | data + lugar → **tu** numa cena com objeto → desfecho seco → "Este es el expediente de lo que era formar parte de X" → promessa em 1 linha ("de la puerta de entrada a las dos únicas salidas") | 20–30 s | "Catania, 1962. Un hombre que conoces desde niño te presenta a otro con cuatro palabras: 'Questo è la stessa cosa'. Desde ese momento, esas palabras son tu único documento. […] Este es el expediente de lo que era formar parte de la mafia siciliana. Y de las dos únicas maneras de salir." |
| 1 | **EXPEDIENTE 1: El Reclutamiento** | quem escolhe, por que você, quanto tempo te observam | 60–80 s | a regra da apresentação por um terceiro (Calderone, Buscetta: atribuído) |
| 2 | **EXPEDIENTE 2: La Prueba** | o primeiro serviço / o teste de confiança | 60–80 s | o "avvicinato" que faz favores durante anos antes de entrar |
| 3 | **EXPEDIENTE 3: El Juramento** | o rito como **objeto** (nunca o mesmo objeto do vídeo "TODA la historia" do tema) | 60–80 s | o rito contado **pelo testemunho de Vitale ou de Calderone** (o santinho de Buscetta já é o hook do 004: aqui ele sai) |
| 4 | **EXPEDIENTE 4: Las Reglas** | um **documento real** com as regras | 60–90 s | o "decálogo" achado no esconderijo dos Lo Piccolo (2007), lido contra a vida dos anos 70 |
| 5 | **EXPEDIENTE 5: El Dinero** | quanto ganhava, de onde vinha, números exatos | 60–80 s | a "mesada" da família, o pizzo, o que Calderone conta sobre dinheiro |
| 6 | **EXPEDIENTE 6: Un Día Cualquiera** | rotina, casa, família, o que se podia dizer à mulher | 60–80 s | **(CTA da HQ antes deste bloco; CTA de inscrição no fim do 6 ou do 7, ~60%)** |
| 7 | **EXPEDIENTE 7: La Falta** | o que acontecia a quem quebrava regra (sugerido por tinta e sombra, sem violência explícita nem vocabulário de glamour) | 60–80 s | a guerra de 1981–82 vista de dentro: as regras deixam de valer |
| 8 | **EXPEDIENTE 8: La Salida** + **Cierre** | as únicas saídas (cárcere/colaboração ou sumir) com o caso real; volta ao objeto do hook + aforismo + "Y tú, ¿habrías dicho que sí?" | 90–120 s | o destino de Vitale (1984) e a fuga de Calderone (1986); cierre "Las Cuatro Palabras" |

Total: hook + 8–10 expedientes + cierre, **11–13 min** (~1.650–1.850 palavras, WPS 2,38).

### 2c. O que muda × o roteiro padrão do canal
| | padrão (bíblia `roteiro.md`) | "expediente de ingreso" |
|---|---|---|
| Tempo | a história **inteira** (fundação → queda), 11–14 expedientes cronológicos | **uma época** (1 ano ou 1 década) e **um lugar**; 8–10 expedientes por **etapa de vida** (sequência fixa, reutilizável) |
| Ponto de vista | narrador seco em 3ª pessoa | **2ª pessoa (tú)** nas cenas, **mais um recluta documentado** que volta em todos os expedientes como prova ("Calderone lo hizo así en 1962") |
| Hook | anedota + "Esta es TODA la historia de X" | cena física **em que o espectador está** + "Este es el expediente de lo que era formar parte de X" |
| Título | "TODA la historia…" / "SIGLA: aposto" / "Cómo…" | "Así era formar parte de [explicador]…", "Cómo te reclutaba X…", "Las N reglas de X…" (sem "TODA la historia"; explicador nas primeiras 5 palavras, regra de 24 e 27/11) |
| Visual | pasta parda, máquina de escrever, carimbos | o mesmo, mais **um objeto recorrente: a ficha de ingresso** preenchida a cada expediente (NOMBRE · PADRINO · JURAMENTO · SUELDO · FALTAS · SALIDA), com carimbos "ACEPTADO" e, no fim, "BAJA" |
| O que NÃO muda | tom seco, sem humor (diferente do historia-ptbr v3: nada de bruxa, HUD de mortes, piada); fatos com fonte; ângulo América Latina quando houver; CTA fixo a ~60%; políticas do YouTube | — |

### 2d. Regras novas que o formato exige (propostas para a bíblia, se o teste passar)
1. **A 2ª pessoa nunca executa violência.** "Tú" entra, jura, recebe, vê e foge. A violência acontece ao redor e fora de quadro. É a regra do "vocabulário de perpetrador" (007, 010) aplicada ao formato: sem glamour, sem "ganhar respeito matando".
2. **Todo detalhe da vida em 2ª pessoa tem fonte** (depoimento, sentença, documento). Detalhe genérico sem fonte vira "según los arrepentidos…" ou sai. O formato atrai cena de filme (lição do 004 e do 005).
3. **Não canibalizar o "TODA la historia" do tema:** nenhum objeto, hook ou cena usado no vídeo antigo do mesmo tema; recorte de época que o vídeo antigo só atravessa em 1 expediente.
4. **Nunca o título "Tu vida en cada rango/nivel de…"** (marca do Te lo Pinto, saturado nos clones).

---

## 3. Seis temas candidatos (dentro da bolha), com 3 pares título+thumb
Ordem = demanda × adjacência aos vencedores (Cosa Nostra, KGB, SS/Gestapo) × chance de ângulo próprio. Os títulos não usam muerte/asesinato. Thumbs com ícone do país e o explicador (regras de 23, 24 e 27/11), em 3 padrões visuais: **A** documento-evidência · **B** objeto-símbolo · **C** cena com o "tú" de costas.

### 1. Mafia siciliana: formar parte de una familia (Sicília, 1962–1984), **recomendado nº 1**
- **Evidência:** Te lo Pinto "Mafia Italiana" 1,38 mi (13,9×); Hypothetically 3,03 mi (11,5×); POVrank 594 mil (10,9×); Baldy POV 310 mil (6×). Contra: Historia Incomprendida "Así era la vida según cada rango de la mafia italiana de 1950 a 1970" 95 mil (1,2×, canal de 4,5 mi inscritos), o que mostra que o "así era" sem gancho concreto não basta.
- **Recluta-fio:** Antonino Calderone (Catania; o livro-depoimento *Gli uomini del disonore*, 1992, com Pino Arlacchi) + Leonardo Vitale (o 1º arrependido, 1973, declarado louco, morto em 1984). Atribuição sempre aos depoimentos.
- **× 004 "TODA la historia de la Cosa Nostra":** o 004 cobre 130 anos e usa o santinho de Buscetta (hook), o Restaurante, o Hotel, o Búnker e a Autopista. Aqui não entra nenhum desses objetos: só a vida **dentro** de uma família nos anos 60–80. Buscetta, no máximo, como nome.
- **× agenda:** Provenzano (05/12) e Calvi (07/12) são biografias. Ver o slot no §4 para não juntar 3 sicilianos na mesma semana.

| par | título | thumb |
|---|---|---|
| A | **Así era formar parte de la MAFIA SICILIANA (Sicilia, 1962)** | ficha de ingresso amarelada com foto 3×4 de um rapaz, campo "PADRINO" preenchido à máquina, carimbo vermelho "ACEPTADO"; ao fundo, ruela siciliana com varal e igreja barroca |
| B | **Cómo te reclutaba la mafia siciliana: las 4 palabras que te hacían "hombre de honor"** | só a mão de um homem de terno estendida, anel no dedo, sobre mesa de mármore; "LA STESSA COSA" à máquina; sello "MAFIA · SICILIA" |
| C | **Las reglas de la Cosa Nostra, y lo que pasaba si rompías una** | homem jovem de costas (o "tú") diante de três homens sentados à sombra, Etna ao fundo; texto "10 REGLAS" + carimbo "MAFIA SICILIANA" |

### 2. La Habana, 1957: trabajar para la mafia de los casinos, **recomendado nº 2**
- **Evidência:** Reimaginando Pasados "Así Era La Noche De Lujo En La Habana Antes De La Revolución" 388.524 (21×); ElDiaQue "Así Era Cuba Antes de Fidel" 236.092; Cuba sin Cascabel "Fidel y Batista Eran Socios" 149.722 (8 mil inscritos); Relato Mafioso "La Historia Prohibida de la MAFIA CUBANA" 308 mil (2025). Autocomplete: "cómo era cuba antes de 1959 / en los años 50 / en 1958". Contra: "Así la Mafia Estadounidense Convirtió La Habana en un Imperio de Casinos" 20 mil (1,1×). **Lição:** vender a **vida/noite**, não o "império da máfia".
- **Recluta-fio:** um crupiê/empregado do Riviera ou do Tropicana (a escolher na pesquisa, com fonte: memórias de ex-funcionários, T. J. English *Havana Nocturne*, relatórios de Kefauver), e Lansky como patrão ausente. O "tú" é cubano: **ângulo América Latina total**, que nenhum clone tem.
- **× vídeos nossos:** o 004 tem 1 expediente "El Hotel" (Havana 1946, conferência). Aqui é 1955–59, o cassino por dentro até a noite de 01/01/1959. Liga Cosa Nostra ↔ Guerra Fría LatAm (as duas fontes de sugerido, `bolha-opcoes` §1).
- **Risco:** é mais lugar/época do que organização (a bíblia avisa contra país como tema). O fio "trabajar **para la mafia**" segura a organização.

| par | título | thumb |
|---|---|---|
| A | **Así era trabajar para la MAFIA en La Habana de 1957** | crachá/ficha de empregado do cassino com carimbo "CASINO · HABANA 1957", fichas de roleta espalhadas, neon do Malecón ao fundo |
| B | **La Habana antes de 1959: la mafia que era dueña de las noches de Cuba** | roleta parada no zero, charuto aceso, bandeira cubana refletida no verniz; texto "MAFIA EN CUBA" |
| C | **Cómo la mafia contrataba cubanos para sus casinos (y qué pasó el 1 de enero de 1959)** | crupiê de costas diante da mesa vazia, porta do cassino arrombada, palmeiras; carimbo "01·01·1959" |

### 3. KGB: ser un espía "ilegal" (1970–1985), **recomendado nº 3**
- **Evidência:** Te lo Pinto "Así Funciona la KGB Desde Dentro" 354.039 (3,6×); POV Rangos "Tu Vida en Cada Rango de la KGB" 68.515 (4,5×, canal de 2 meses); POVrank (en) 337 mil (6,2×); Jack Barsky (ex-ilegal) 1,92 mi no Raj Shamani (en); Ecos de la URSS "Así entrenaba el KGB a sus agentes" 42,6 mil (canal de 1 mil inscritos). Autocomplete forte para "vivir en la URSS". **A KGB é a nossa maior fonte de sugerido** (1.973 views mandadas à Cosa Nostra em 28 dias).
- **Recluta-fio:** Jack Barsky (Albrecht Dittrich), recrutado em 1970 na RDA, treinado em Moscou e ilegal nos EUA até 1988 (memória *Deep Undercover*, 2017; entrevista ao *60 Minutes*, 2015). Sem nada que o 005 já tenha usado.
- **× 005 "TODA la historia de la KGB" e 015 GRU:** o 005 usa Markov, Feklisov, Oswald no México, Mitrokhin e Gordievski; o 015 tem o fio "latinoamericanos fabricados". Aqui ficam **proibidos** todos esses nomes e o fio do passaporte latino. É a formação e a vida dupla de um ilegal: a escola, a "lenda", o rádio, a mulher que não sabe, a ordem de voltar.

| par | título | thumb |
|---|---|---|
| A | **Así era convertirse en espía de la KGB** | ficha com foto, "NOMBRE FALSO" riscado e reescrito, carimbo "КГБ · APROBADO"; foice e martelo pálido ao fundo |
| B | **Cómo la KGB fabricaba un espía: 3 años para olvidar quién eras** | certidão de nascimento ocidental em branco sobre mesa, rádio de ondas curtas, estrela vermelha; texto "KGB" grande |
| C | **El espía soviético que vivió 10 años en Estados Unidos sin que su esposa lo supiera** | homem de costas na cozinha de casa americana, rádio escondido na prateleira, Kremlin refletido na janela; sello "KGB" |

### 4. Yakuza: entrar en el Yamaguchi-gumi (Kobe/Osaka, 1980–1992)
- **Evidência:** Te lo Pinto "Cómo es Ser Cada Rango de la Yakuza" 1.265.210 (12,7×); Hypothetically 1,92 mi (7,3×); POVrank 499 mil (9,1×); Level 8 "Los 8 Rangos más peligrosos de los Yakuza" 138.892 (12,7×). Contra: POV Rangos Yakuza 18,9 mil (1,2×).
- **Recluta-fio:** o depoimento do ex-yakuza de *Confessions of a Yakuza* (Junichi Saga, 1989) e/ou Shoko Tendo (*Yakuza Moon*, filha de yakuza). O arco: sakazuki, oyabun-kobun, irezumi, yubitsume, a guerra Yama-Ichi (1985) e a lei de 1992 como "saída".
- **× 014 Yakuza** (fio "trabajaba para el poder", 1919→2021; hook Itami): aqui não entra política nem Itami; é a vida de um kobun numa década. **Risco:** o 014 precisa ser reenviado (o arquivo no ar é o do GRU, diagnóstico de 27/11), e 2 Yakuzas perto um do outro canibalizam. Fica para **depois** do reupload.

| par | título | thumb |
|---|---|---|
| A | **Así era entrar en la YAKUZA, la mafia japonesa (Kobe, 1985)** | ficha com caracteres 山口組, carimbo vermelho redondo (hanko) "ACEPTADO", lanternas ao fundo |
| B | **Cómo la mafia japonesa te convertía en "hijo" del jefe: la copa de sake** | duas taças de sake sobre tatame, katana embainhada, sol nascente; texto "YAKUZA" no pincel (Yuji Boku) |
| C | **Las reglas de la Yakuza, y por qué te cortabas un dedo** | costas tatuadas (irezumi) de um jovem diante de um altar xintoísta; carimbo "MAFIA JAPONESA" |

### 5. Vivir vigilado por la Gestapo: el vecino que te denunciaba (Alemania, 1939–1943)
- **Evidência:** Te lo Pinto "Así Funcionaba por Dentro la Policía Nazi del Tercer Reich" 300.481 (3,0×); Historia Militar "Desde el punto de vista nazi: ¿cómo lo vivieron…?" 402.823 (19×) e "Así VIVÍAN en Berlín después de la muerte de Hitler" 1,29 mi (61×); Gabriel Herrera "Así era 'VIVIR' en… Dachau" 593 mil. A Gestapo do Archivo en Minutos é a **fonte nº 1 de sugerido** do canal.
- **Ângulo:** o "tú" é um **cidadão comum** (nunca um SS: a 2ª pessoa como perpetrador fere a regra 2d-1 e a política do YouTube). A base são os arquivos de Würzburg/Düsseldorf estudados por Robert Gellately: a maioria dos casos começava em denúncia de vizinhos. Hook físico: o rádio coberto por um cobertor para ouvir a BBC (decreto de 01/09/1939 contra ouvir emissoras estrangeiras).
- **× 009 Gestapo** (Barbie, Sudamérica) **e Archive Gestapo** (hook da piada da viúva): fica proibida a anedota da piada denunciada. O foco é o cotidiano do denunciado, e o que fica é o rádio, a carta, o vizinho.

| par | título | thumb |
|---|---|---|
| A | **Así era vivir vigilado por la GESTAPO, la policía secreta de Hitler** | ficha de denúncia datilografada com carimbo da águia e "DENUNCIA", nome riscado; janela com cortina entreaberta |
| B | **Si escuchabas esta radio, tu vecino podía denunciarte: Alemania, 1939** | rádio Volksempfänger coberto por um cobertor, luz fraca; texto "GESTAPO" |
| C | **Cómo la Gestapo vigilaba a 80 millones con tan pocos agentes** (o "tú" como alvo) | homem de costas no corredor do prédio, sombra de chapéu na porta, olho mágico; carimbo "1939" |
**Risco:** a tese "poucos agentes, muitos denunciantes" é a do Archive Gestapo ("how a small police force watched 80 million"). No par C, só usar se a embalagem provar que não colide; senão, sai.

### 6. Stasi: cómo te convertían en informante (Berlín Oriental, 1985)
- **Evidência (fraca em es):** Rose Bennet "El MURO de BERLÍN era Peor de lo que Imaginabas" 465.143; AndyGM "La historia real de la Stasi" 59.631; POVrank (en) 110 mil (2,0×); SLICE (en) 227 mil. Autocomplete: "cómo era vivir en la alemania oriental". Archive in Minutes Stasi 175 mil (en), Atlas del Tiempo 8,8 mil (es).
- **Ângulo:** a 2ª pessoa recrutada como IM: a "Verpflichtungserklärung" assinada, o codinome, os potes de cheiro, a Zersetzung, e o dia de 1992 em que você lê o próprio arquivo. América Latina no cierre: Honecker morreu em Santiago (1994).
- **× vídeos nossos:** não temos Stasi. Zero canibalização, mas a demanda em es é a mais baixa da lista: só depois de o formato provar.

| par | título | thumb |
|---|---|---|
| A | **Así era ser informante de la STASI, la policía secreta de Alemania Oriental** | formulário de compromisso assinado com o carimbo da Stasi, codinome à máquina; Muro e torre ao fundo |
| B | **Cómo la policía secreta de Alemania Oriental convertía a tus amigos en espías** | pote de vidro com pano dentro (amostra de cheiro), etiqueta com nome; texto "STASI" |
| C | **Berlín Oriental, 1985: firmaste un papel y te convertiste en espía de tu familia** | jovem de costas à mesa, caneta na mão, oficial à sombra; sello "STASI · 1985" |

### Fora da lista (com o porquê)
| tema | por quê |
|---|---|
| Cártel (Medellín/Sinaloa) "por dentro" | é o que mais rende no formato (Dolor Pintado 2,4 mi; El Perezoso 1,46 mi), mas é a **bolha narco** onde o Medellín morreu (0,54%) e onde o Te lo Pinto/El Perezoso são gigantes. Volta só se o formato passar |
| Ser soldado das SS em 2ª pessoa | demanda alta (Historia Militar 307 mil), mas põe o espectador como perpetrador (regra 2d-1, política do YouTube). Se for feito, só em 3ª pessoa |
| Templarios "por dentro" | Te lo Pinto 2,33 mi, mas o nosso 011 nem foi testado na bolha (82 impressões, diagnóstico de 27/11). Reserva para depois |
| Coreia do Norte | demanda enorme (3–4 mi), mas é atualidade e país, não organização histórica |

---

## 4. Desenho do teste

### 4a. Slot e calendário
- **Slot: terça à noite** (a noturna produz sáb/dom/seg/ter; ter → janela de publicação sex/sáb). Assim o vídeo do formato sai **≥ 48 h** depois dos outros da semana e é testado limpo (ajuste 6 do diagnóstico).
- **3 vídeos**, 1 por semana, **trocando o item de terça** (decisão do Rodrigo; nada foi mexido):

| semana | noite | hoje está agendado | proposta | publicação sugerida |
|---|---|---|---|---|
| 05–08/12 | ter **08/12** | Tríadas (56) | **#1 Mafia siciliana "expediente de ingreso"**; Tríadas vai para a seg 07/12 e Calvi (62) passa para a semana de 12/12, para não haver 3 vídeos sicilianos numa semana (Provenzano 05/12 já é um) | sex 11 ou sáb 12/12 |
| 12–15/12 | ter **15/12** | (a definir pelo backlog) | **#2 La Habana 1957** | sex 18 ou sáb 19/12 |
| 19–22/12 | ter **22/12** | (a definir) | **#3 KGB ilegal** (ou Yakuza, se o 014 já tiver sido reenviado e medido) | sáb 26/12 (Natal: comparar só com os controles da mesma semana) |

- **Leitura final:** 7 dias após o #3, por volta de **02/01/2027**. **Corte antecipado:** 48 h após o #2 (~20/12).
- Os outros 3 vídeos de cada semana são o **controle** (molde padrão, mesma semana, mesma onda).
- Produção: e1 Opus / e2 Sonnet como sempre; a embalagem passa pelo crivo, e o roteiro pelo detector e pelo crivo de ângulo. O e1 de cada um precisa de um **brief de formato** com o esqueleto do §2b e as regras do §2d (anexo ao `BRIEF-lote-*-ETAPA1`), enquanto a bíblia não muda.

### 4b. Métricas (por vídeo)
| métrica | fonte | meta "passa" | por quê |
|---|---|---|---|
| **CTR no sugerido nas 1ªs 48 h** (≥ 1.000 impressões) | Reporting API → `youtube.alcance_diario` (origem sugerido) | **≥ 4%** (morte < 2%) | é o portão comprovado (SS 6,4%, Gestapo 4,2% cresceram; Medellín 0,54%, Núremberg 1,6% morreram) |
| **Views em 7 d** ÷ mediana dos 3 controles da semana | `metricas_video` / Studio | **≥ 1,5×** | mede o ganho do formato, descontando a onda |
| **Retenção:** a 5% do vídeo e % médio visto | `analytics_retencao`, `analytics_video_dia` | ≥ 85% a 5% e ≥ 45% médio (canal: 48,6–66%) | a 2ª pessoa não pode custar retenção |
| **Fatia nova de público:** % de views de **não inscritos** e % do sugerido vindo de vídeos **fora** do nosso canal/clones (ex.: Te lo Pinto, POV/rangos, reconstruções de época) | `analytics_publico` (subscribedStatus), `analytics_trafego_detalhe` (detalhe_canal); Studio "novos × recorrentes" | não inscritos ≥ controles **e** ≥ 20% do sugerido vindo de vizinhos novos | é o objetivo do Rodrigo: "pegar outra fatia de público" |
| **Inscritos por 1.000 views** | Studio / `analytics_video_dia.inscritos_ganhos` | ≥ 4,0 (canal ~3,6) | o formato em 2ª pessoa promete ser mais "pessoal" |

### 4c. Critério
- **Sucesso (vira 1 vídeo/semana fixo + seção nova na bíblia):** CTR ≥ 4% em **2 de 3** **e** pelo menos um destes: (a) 1 vídeo ≥ 1,5× a mediana dos controles em 7 d; (b) média de inscritos/1.000 ≥ 4,0; (c) sugerido vindo de vizinhos novos ≥ 20% em 2 de 3.
- **Parcial (fica como "tema-reserva", sem slot fixo):** CTR passa, mas as views ficam abaixo dos controles. O formato embala bem e não traz público novo.
- **Corte antecipado:** #1 e #2 com CTR < 2% sobre ≥ 1.000 impressões → cancela o #3 e devolve a terça ao molde padrão.
- **Corte final:** 0–1 de 3 passam → formato arquivado nesta proposta; aprendizado (o que falhou: título, tema ou 2ª pessoa) vai para a bíblia como Hipótese derrubada.
- **Em todos:** regra das 48 h (CTR < 2% → trocar thumb no 2º dia) e conferência pós-upload (duração **e** 1ª frase), como no diagnóstico de 27/11.

### 4d. Custo
O mesmo de um Dossier padrão (~R$ 45–50: voz Fish ~US$ 1, imagens pelo Codex US$ 0, render Runpod centavos). Não há gasto novo: o teste só troca o tema de 3 noites que já existiriam.

---

## 5. Para o Rodrigo decidir
1. Aprovar o formato "expediente de ingreso" (§2) como teste de 3 vídeos.
2. Aprovar os 3 temas e a ordem (Mafia siciliana → La Habana 1957 → KGB ilegal) e o slot de terça a partir de 08/12, com a troca Tríadas ↔ Calvi da semana de 05/12.
3. Se aprovar: mudar o backlog (`tools/rotinas/backlog.py`) e gerar o brief de formato para o e1 de 08/12, antes de sáb 05/12 (o e1 sobe na noite de terça).
