# Anatomia do canal-base: historia-ptbr v3 ("como era viver / você não sobreviveria")

Coleta: **28/11/2026**. Fontes: busca `yt-dlp ytsearch30` via WARP (13 termos: "you wouldn't survive", "what life was like in", "a day in the life of a medieval peasant", "how long would you survive in", "how long you'd last", "your life as a medieval"…), YouTube Data API (`channels.list`, `playlistItems`, `videos.list`; ~60 unidades, sem `search.list`), thumbs e quadros automáticos do YouTube (`hq1/2/3.jpg` = 25/50/75% do vídeo). Custo pago: US$ 0.

> **Atualização 28/11/2026 (tarde): transcrições obtidas.** As 8 legendas automáticas em inglês estão em `ref/manada-<id>.txt` (com marcas [m:ss]); status em `canal-base.json`. A §3 e a §6 foram **refeitas com medidas reais** (palavras/min, "you"/min, números/min, tempos do hook, transições, CTA, fecho). Legenda de marcas: **[MEDIDO]** = confirmado na transcrição; **[CORRIGIDO]** = o que era inferido pelos quadros e estava errado ou incompleto. Contagens de piadas são **estimativa por amostragem** (2 min por vídeo), não contagem exaustiva. Cortes/min continuam sem medida (exigem `watch.py` com vídeo).
>
> *Nota original (manhã), mantida como histórico:* o YouTube está pedindo login ("Sign in to confirm you're not a bot") a **qualquer** pedido de player, legenda ou áudio pelo IP do WARP e pelo IP direto da VPS. Testei 6 player clients do yt-dlp, a API de transcrição interna (`get_transcript`: FAILED_PRECONDITION), Invidious/Piped e sites de transcrição: todos barrados. O mesmo bloqueio aparece em `pesquisa/tendencias/2026-11-28-oportunidades-canais.md`. Consequência: **`watch.py` e `manada.py transcrever` falharam; não há transcrições em `ref/` ainda.** O `ref/manada.json` está pronto com os 8 vídeos-alvo. Quando o YouTube liberar (ou com cookies, decisão do Rodrigo), basta rodar, de `tools/`:
> `TMPDIR=$HOME/cache/tmp .venv/bin/python manada.py transcrever ../canais/historia-ptbr/v3-proposta/ref --ids 2T-1x3F6buE,nT63DYpslws,mZ5zynsMHVc,rRr21F21hGU,tJ_YsbihfU0,r4PcWgRFFF0,IPjDANjdNX0,nAWpLtG-kNs`
> e `.venv/bin/python watch.py 2T-1x3F6buE nT63DYpslws mZ5zynsMHVc` (para medir palavras/min e cortes/min, que **ficam sem medida** abaixo).
> A anatomia foi medida pelos **capítulos oficiais** (tempos exatos), descrições, títulos, durações, quadros a 25/50/75% e thumbs. Os quadros e thumbs estão em `pesquisa/tendencias/assets/2026-11-28/canal-base-historia-ptbr/`.

---

## 1. Candidatos

Mediana = views dos últimos 20 uploads com mais de 3 min. "6 m" = uploads longos de 28/05 a 28/11/2026.

| canal | criado | inscritos | views totais | vídeos | mediana últ. 20 | cadência | duração típica | estilo visual | 2ª pessoa? | top 2025–26 (views · data) |
|---|---|---|---|---|---|---|---|---|---|---|
| **Chat History** | 07/2022 | **1,15 mi** | 138,5 mi | 102 | **1,28 mi** | ~1,5/mês (17 em 2026) | 18–24 min (série "Survive": 8–16 min) | **bonequinho de cabeça redonda** (2D chapado) colado sobre foto/3D/IA + memes; selo "[NO AI]" | **sim** (série "Why You Wouldn't Survive…", "you" o tempo todo; listas de 2026 também falam com "você") | Wrong History Facts 3,58 mi (06/25) · Deadliest Snipers 3,57 mi (02/25) · Victorian Fashion KILLED 2,49 mi (02/26) · Roman Empire (Survive) 2,40 mi (01/25) · Miserable Jobs 2,28 mi (09/26) |
| **Bernard** | 05/2025 | 404 mil | 46,3 mi | 95 | 312 mil | ~4,7/mês | 19–22 min | palito com cabeça desenhada (2D, rosto caricato), cenários pintados | sim pelo formato ("Why It Sucks to Be…", a vida da pessoa do nascimento à morte); transcrito em 28/11: 14,7 "you"/min (§3.12) | Shared Wife (Tibet) 1,93 mi (08/26) · Joy Woman (Aztec) 1,78 mi (07/26) · Empress (Ming) 2,77 mi (12/25) · Breeding Slave (Rome) 2,24 mi (05/26) · Married to Brother (Egypt) 611 mil (10/26) |
| Fossil | 03/2026 | 60,7 mil | 26,6 mi | 17 | 78 mil | ~2/mês | 16–19 min | **CG/IA realista** (paisagem, bichos, neandertal fotográfico) | sim ("How Long You'd Last…") | **Every Prehistoric Era 13,6 mi (08/26)** · Orcas 4,44 mi (10/26) · Polar Bear 3,14 mi (10/26) · How Fast You'd Die… Ocean 2,27 mi (11/26) |
| Lost Legacy | 11/2024 | 241 mil | 31,9 mi | 51 | 210 mil | ~2,5/mês | 9–11 min | ilustração 2D desenhada à mão, branco + texto manuscrito | sim ("Your Life as a…") | Concubine 4,60 mi (06/25) · Medieval Torturer 3,69 mi (07/25) · Geisha 2,68 mi (05/25) · North Korean 1,75 mi (02/26) · Vestal Virgin 935 mil (05/26) |
| Weird History (Ranker) | 06/2017 | 4,74 mi | 744 mi | 1.175 | 92 mil | ~10/mês | 12–14 min + compilações | stock/pintura realista + IA | não (3ª pessoa: "What Life Was Like…") | Mayflower 1,33 mi (09/26); clássicos antigos: Medieval Castles 6,95 mi |
| Simple History | 10/2014 | 5,12 mi | 1,72 bi | 1.442 | 316 mil | ~4/mês | 9–10 min | 2D vetorial | não; hoje virou armas/militar | Gun Tricks 1,35 mi (09/26) |
| MedievalMadness | 08/2021 | 509 mil | 65,8 mi | 295 | 45 mil | ~4,5/mês | 12–16 min | stock/IA | às vezes ("You'd Literally Last 30 Seconds…" 494 mil) | Worst Medieval Period to Be Born 936 mil (06/26) |
| Lot and Ledger | 10/2026 | 2,5 mil | 0,55 mi | 7 | 63 mil | 7 em 3 semanas | 21–26 min | 2D estilo Bernard | sim ("Why You Wouldn't SURVIVE as…") | Peace Bride 176 mil (11/26) — clone de Bernard, prova que o molde replica |

Descartados e por quê: **Sam O'Nella** (4,8 mi, mediana 13 mi, mas 1 vídeo em 2026: inativo); **OverSimplified** (último vídeo 01/2025); **History Matters** (8 min, 3ª pessoa, "Why didn't X…"); **toldinstone** (rosto/arqueologia, 3ª pessoa); **The Infographics Show** (15,5 mi, mas generalista: IA, ciência; "What X Does to Your Body (Hour by Hour)" 3,3 mi é útil como fórmula, não como canal-base); **Worlds Before Us / Medieval Times Discovered** (reconstrução IA realista, o oposto do nosso estilo). Em pt não há canal-base forte no formato com bonequinho (ver `relatorios/portfolio/2026-11-28-dados/historia-ptbr.md` §2.3).

## 2. Escolha

### Canal-base: **Chat History** (`UCicVSNyM7PMXEzdoAsTB02w`)
1. **Visual quase idêntico ao nosso:** bonequinhos de cabeça redonda, corpo de cor chapada, olhos de bolinha, sobre fundos reais. É o canal en mais próximo do nosso estilo (e ele mesmo se marca como "stick figure history", na linhagem Sam O'Nella).
2. **Formato exato pedido, em 2ª pessoa:** a série "Why You Wouldn't Survive…" tem 8 vídeos, **mediana ~2,0 mi** (Egito 3,94 mi; Roma 2,40 mi; Grécia 2,35 mi; Japão 2,18 mi; Oregon Trail 1,70 mi; Astecas 1,39 mi; Nuclear 0,99 mi; Salém 0,74 mi), de 8 a 16 min. É a duração que queremos (12–15 min).
3. **Forte em 2026:** 17 vídeos no ano, mediana de **1,27 mi** e nenhum abaixo de 600 mil. O canal ganhou alcance com listas de ~20 min.
4. **Oportunidade:** o dono parou a série "Survive" em 10/2025. O formato foi provado e está sem dono ativo, e ninguém faz em pt com bonequinho.
5. **Temas traduzem para o Brasil:** a série é "era/lugar + perigos do dia a dia". Isso vira "Você não sobreviveria ao Brasil colonial / à corrida do ouro em Minas / ao Rio de 1904 / a uma caravela de 1500".

### Reserva: **Bernard** (`UC_FStSURaDad8-xo6jH1j4Q`)
O canal de 2026 que mais cresceu no gênero: 404 mil inscritos em 18 meses, mediana de 312 mil, 20 min, um vídeo a cada ~6 dias, palito 2D com cabeça desenhada. A estrutura é a **linha da vida** (você nasce → cresce → trabalha → casa → morre como aquele papel). Ela complementa a "escada de perigos" do Chat History para temas de **ofício/papel** ("Por que era horrível ser tropeiro / ama de leite / mineiro em Vila Rica"). **Cuidado:** os temas do Bernard são sexuais ou tabus (esposas, concubinas, escravas). **Não** levar essa temática; levar só o esqueleto. Alternativa de reserva com o mesmo esqueleto e 10 min: Lost Legacy ("Your Life as a…").

Fossil fica como **referência de título**, não como canal-base: "How Long You'd Last in Every X" fez 13,6 mi, mas o visual é CG/IA realista e o tema é pré-história, longe do Brasil.

---

## 3. Anatomia do roteiro (série "Why You Wouldn't Survive…", Chat History), medida nas transcrições

Base: capítulos oficiais + quadros a 25/50/75% (manhã) + **legendas automáticas** em `ref/` (tarde, 28/11/2026). Palavras = texto da legenda sem marcas de tempo e sem [Music]; ppm = palavras ÷ duração total do vídeo (inclui trechos só de música/luta, então a fala real é um pouco mais rápida).

| id | vídeo | views | duração | palavras | ppm | "you"/min | números/min | blocos (capítulos oficiais) |
|---|---|---|---|---|---|---|---|---|
| 2T-1x3F6buE | …in Ancient Egypt (05/2024) | 3.937.449 | 8:27 | 1.550 | **183** | **12,4** | 0,9 | Start of the Journey 0:00 · Childhood 0:40 · Labor 2:55 · Disease 4:57 · War 6:37 |
| nT63DYpslws | …The Roman Empire (01/2025) | 2.397.835 | 15:09 | 2.412 | 159 (¹) | 8,1 | 1,1 | A Witch! 0:00 · You Have Arrived 0:53 · A Worthy Opponent 2:26 · Tummy Rumbles 4:18 · Bad Tummy Rumbles 7:16 · Got The Ick 9:43 · Recruitment 12:04 |
| mZ5zynsMHVc | …in Ancient Greece (09/2024) | 2.350.863 | 11:35 | 2.074 | 179 | 10,4 | 1,0 | Intro 0:00 · Getting Your Bearings 0:34 · Speaky da Greeky 1:49 · Greek Society 3:12 · Workin' and Twerkin' 5:46 · Sickies and Ickies 7:13 · Hitting the Books 9:53 |
| rRr21F21hGU | …FEUDAL JAPAN (10/2024) | 2.184.153 | 12:58 | 2.062 | 159 (¹) | 8,1 | 0,3 | That Dang Witch! 0:00 · Context 0:40 · A Thrilling Battle! 3:03 · Society 4:28 · The Soldier's Life 8:13 · War Time 10:00 |
| tJ_YsbihfU0 | …THE AZTEC EMPIRE (06/2025) | 1.393.072 | 15:52 | 2.747 | 173 | 6,9 | 1,2 | Not Again! 0:00 · Welcome 1:02 · Society 4:36 · Military 7:33 · Slaves 9:57 · Blood for the Sun God 12:43 |
| r4PcWgRFFF0 | The Most Miserable Jobs in History [NO AI] (09/2026) | 2.275.420 | 20:37 | 3.526 | 171 | 3,2 | 2,1 | 4 ofícios: mergulhador de pérolas 0:07 · carrasco 6:41 · menino das portas da mina 11:10 · faroleiro 15:31 |

(¹) Roma e Japão têm ~1 min de luta só com música (2:47–3:47; 3:28–4:12): descontando, a fala corre a ~170 ppm.
**Resumo [MEDIDO]:** série "Survive" fala a **159–183 ppm** (mediana ~173), com **7–12 "you"/min** e só **~1 número/min**. O formato lista de 2026 tem metade do "você" e o dobro de números.

### 3.1 Hook com tempos reais **[MEDIDO; CORRIGIDO]**
A manhã estimou um cold open de 34–62 s. A transcrição mostra que **a premissa inteira é dita em 8 a 17 s de fala**; o resto do primeiro minuto é piada de contexto.

| vídeo | 0–15 s | 15–30 s | 30–60 s | "let's find out" |
|---|---|---|---|---|
| Egito | Sem esquete: "você caiu num buraco de minhoca de uma bruxa e foi parar no Egito; consegue sobreviver?" (tudo em 8 s) | Qual Egito? Escolhe o Novo Império, "o mais documentado, que conveniente" | Piada: "se você chegou até este vídeo, já sobreviveu à infância" → mortalidade infantil 20–50% com barra de vida piscando | 0:08 |
| Roma | Esquete muda: jantar de espaguete, garçom do parmesão ("é só dizer quando") | …o "quando" nunca vem; a bruxa leva você | 0:28 "lá vamos nós de novo com a bruxa"; Roma "na cabeça de todo homem acima de 20" (meme); 0:52 ano 250, crise do século III | (não usa; "let's see what you're capable of") |
| Grécia | 16 s de música (esquete visual) | 0:16 "essa bruxa está virando um problema"; Grécia clássica; trocadilho com Termópilas | Recorte 510–323 a.C. com piadas de data ("Alexandre deixou de ser grande"); "ache um ponto de referência" | 0:32 |
| Japão | 17 s de esquete visual | 0:17 "começo a achar que você gosta de ser sequestrado"; Japão feudal, 1467, início do Sengoku | "Está pronto? Bora ver"; o xogum × imperador explicado com piada | 0:41 |
| Astecas | **Recapitula o final do episódio anterior** (Nuclear: "um apocalipse nuclear e eu morro para um urso") | A bruxa ataca de novo | 0:34 "e o ciclo continua": Império Asteca; 0:49 "Acha que sobrevive? Eles não sobreviveram, então talvez você sim" | 0:49 |
| Lista (empregos) | Título falado + "isso é horrível" | Piada (pérolas × último bolinho do pacote) | Colombo, 1498, Venezuela: o 1º ofício já começou | — |

Padrão real:
- **0–15 s:** esquete do avatar no presente (comendo, dormindo) interrompida pela bruxa, ou a frase-premissa direta (Egito, o mais visto, não tem esquete).
- **15–30 s:** reconhecimento da série ("de novo?", "você gosta de ser sequestrado") + **lugar e ano exatos**.
- **30–60 s:** 1–2 piadas de contexto + a pergunta "consegue sobreviver?" e o fecho em **"let's find out"** (4 de 5). A partir daí, contexto histórico curto (Roma e Japão: ~1 min de "por que esta época é um caos", contado como fofoca, com piada a cada frase).
- O "pior momento da era" é dito **na fala** (crise do século III, guerra de Ōnin, véspera de Cortés).
- **[CORRIGIDO]** O HUD "DEATHS: N" é só visual: **a narração nunca conta mortes**.

### 3.2 Blocos e transições **[MEDIDO; CORRIGIDO]**
Blocos reais (tempos da fala):
- **Egito (5):** infância 0:39 → sociedade 1:56 (risco de ser escravizado, "mas vamos supor que você convence os guardas") → trabalho (fazenda, cheia do Nilo, pirâmide) 2:45 → doença 4:57 → guerra 6:08–8:15.
- **Roma (6):** contexto da crise 0:52 → Coliseu, luta-patrocínio 2:00 → comida, inflação e língua 3:47 → latrina e termas 7:00 → praga de Cipriano 9:40 → recrutamento e godos 11:40–15:01. **Comida, banheiro e doença = 52% do vídeo.**
- **Grécia (5):** chegada e língua 0:39 (gesto mal-entendido → preso e escravizado) → sociedade 3:12 → mina 5:42 → peste 7:05 → educação 9:37–11:27.
- **Japão (6):** contexto Ōnin 0:42 → bandido, luta-patrocínio 2:32 → sociedade 4:28 → camponês, fome e doença 6:31 → recruta e um dia de soldado hora a hora 7:21 → guerra 10:00–12:34.
- **Astecas (6):** fundação de Tenochtitlán 1:02 → língua e captura 3:28 → sociedade, higiene e comida 4:36 → exército e tributo 7:33 → escravidão e crime 9:57 → sacrifício 12:43–15:15.
- Média: **5–6 blocos de ~2 min** (1,1 a 3,5 min). Sempre presentes: **hierarquia** (5/5; eles mesmos zombam: "outra civilização, outro sistema de hierarquia"), **barreira de língua** (5/5), **doença** (5/5; nos Astecas, invertida: a cidade era limpa) e **exército/guerra** (4/5; Grécia termina em educação, como anticlímax).
- **[CORRIGIDO]** A ordem **não** é fixa: o que liga os blocos é **causa → consequência na vida do avatar**, não o contador. Cada bloco termina num acontecimento que empurra você para o próximo: ficou órfão → onde você se encaixa na sociedade; não fala a língua → preso → mina; sobreviveu à peste porque é vacinado → liberto → escola; ficou sem dinheiro → quem está contratando é o exército.
- **Frases-ponte típicas (descritas):** (1) **"falando em…"** ligando a última palavra do bloco ao próximo tema ("falando em mina de ouro, é para lá que você vai"); (2) **necessidade do avatar** ("a bruxa interrompeu seu jantar, então você precisa comer"); (3) **frase cortada** antes do nome da doença ("você com certeza vai pegar algum tipo de—" → corte → bloco de doença; aparece em Roma, Grécia e Astecas); (4) **promoção ou punição** ("o faraó gostou do seu físico: boas qualidades… para um soldado"); (5) **"surpresa: outra civilização, outra hierarquia"**, a autoironia do padrão.
- **Patrocínio vira cena:** em Roma e no Japão a luta muda de ~1 min no 3º minuto é a propaganda (barbeador: "foi por um fio"). O espectador não pula porque é a cena de ação do episódio.

### 3.3 Uso do "você" **[MEDIDO]**
- **6,9 a 12,4 "you"/min** na série (Egito, o mais visto, é o mais alto); 3,2 na lista de empregos (3ª pessoa com "imagine você").
- **Tipos:** (a) **narração em 2ª pessoa no presente**, o mais comum ("você chega", "você nada até a margem"); (b) **imperativo de guia de sobrevivência** ("cuidado com as cobras", "só não prove a água", "levante peso só com as costas"); (c) **hipotético com desfecho provável ruim + "mas vamos supor"** ("com 95% de chance você seria capturado e vendido… mas vamos supor que convence os guardas"); (d) **"você seria…" de classe** ("a não ser que fosse chinês ou japonês, seria pária ou escravizado"); (e) **o narrador fala com o avatar** como um amigo zoando ("seu bobo", "eles não falam espanhol, seu tonto").
- O avatar tem **conhecimento do século XXI** (vacinado, sabe que precisa se lavar, sabe ler letras) e isso vira vantagem e piada.

### 3.4 Ritmo **[MEDIDO]**
- **159–183 ppm** em inglês. Nossa voz pt mede **~128 ppm** (bíblia, tabela Tamanho: 126–136). Conclusão: para o mesmo minuto, levamos **~25% menos palavras**; as piadas visuais precisam carregar parte do humor que eles fazem falando.
- Bloco novo a cada ~2,2 min (capítulos); premissa fechada antes de 0:50.

### 3.5 Humor **[MEDIDO por amostragem]**
- **Frequência:** ~**2,5 a 5 piadas faladas por minuto** (Egito 0:00–2:00: ~10 piadas; Roma 4:18–6:18: ~5; Astecas 9:59–11:59: ~4), ou seja, **uma a cada 12–25 s**, fora as gags visuais. Quase nunca há dois fatos seguidos sem piada: **fato = preparação, piada = fecho da frase**.
- **Tipos:** (1) **vocabulário gamer** (barra de vida, "nível de pesca", "espada de cobre +7", loot, NPC, DLC, respawn, "fogo amigo sempre ligado"); (2) **comparação com o presente** ("ricos no topo, o resto no não-topo: nada mudou"; "olha a Los Angeles de hoje"); (3) **trocadilho e rima** (listas de comida rimadas em Roma e nos Astecas; "grego ático, não grego de porão"); (4) **subversão de expectativa** ("o supervisor premia seu esforço com… mais trabalho pesado"); (5) **meta e autoironia** do narrador ("eu me perdi numa rima", "acima do meu salário de artista pária"); (6) **esquete de voz** inserido (pai: "vendo vídeo de história de novo? Pro quarto"); (7) humor **grosseiro/sexual** frequente (fora da nossa política).
- **Onde caem:** no fim de cada frase factual; um **callback grande** por vídeo (o colega "Be" que perde o braço volta na guerra e mata você; o amigo samurai Hoshi troca de lado) e a gag do patrocínio no 3º minuto.
- **Limite já anotado:** eles fazem piada com escravidão (Grécia: "pelo menos não são mais escravos fedidos"; Astecas: a regra de pisar em fezes para ganhar a liberdade). No Brasil isso **não entra**.

### 3.6 Mortes e reinícios **[CORRIGIDO]**
- A manhã supunha "1 morte por bloco, contador sobe, renasce". **Na fala, mortes explícitas do avatar são raras (1–3 por vídeo)**; quase todas são **sugeridas por elipse**: "e como estamos na Antiguidade, você sabe o que isso significa"; "todos esses sintomas somam um sujeito morto"; "Claudius, acende um fósforo" (explosão de metano, só som); frase cortada.
- **Mecanismo de reinício falado (o que modelar):** o **desfecho provável ruim + "mas vamos supor…"** (Egito 2:38, Grécia 1:34: "agora vamos supor que ele é mais simpático desta vez"). É uma ramificação: o roteiro mostra a morte ou a captura mais provável e volta para a versão "com sorte". Uma vez só, explícito: "tenta de novo… respawn" (Egito 7:39).
- O **HUD visual** (DEATHS, barras de vida) faz a contagem; a narração só dá a deixa.
- **Fecho nem sempre é morte:** Egito = morto pelo colega → "era só um sonho"; Roma = falha cômica no salto com dardo; Grécia = sobrevive, acha algo na biblioteca ("eu disse que sobreviveria"); Japão = incêndio e "você de novo?" (a bruxa volta); Astecas = no altar, **Cortés interrompe** o sacrifício.

### 3.7 Fatos e números **[MEDIDO]**
- **~1 número por minuto** na série (0,3 Japão a 1,2 Astecas): mortalidade infantil 20–50%, 90% eram agricultores, 5.000 mortos por dia na praga de Cipriano, Alexandria −62% entre 249 e 262, 200 mil habitantes em Tenochtitlán, 1/3 da Atenas escravizada, recruta romano 17–23 anos e 1,70 m.
- Os fatos são **poucos, concretos e sempre usados contra você** (o número explica por que você se dá mal). A lista de empregos sobe para 2,1/min (datas, profundidades, toneladas de carvão).

### 3.8 Loops abertos e onde pagam **[MEDIDO]**
| vídeo | loop plantado | paga em |
|---|---|---|
| Egito | colega "Be" perde o braço: "ele vai lembrar disso" (4:18) | Be mata você na guerra (8:06) → "era só um sonho" |
| Roma | "coisa caótica, mas chegamos lá depois" (godos, 1:58) | frente contra os godos (14:03) |
| Roma | a bruxa interrompeu o jantar (0:28) | bloco da comida (4:11) |
| Grécia | "seus pais te vacinaram" (7:24) | único sobrevivente → liberto (9:37) |
| Japão | Hoshi, o colega de treino (8:27) | Hoshi aparece do lado inimigo (12:11) |
| Astecas | "até que…" (1:18), "Cortés está a caminho" (5:35), "por motivos que veremos depois" (8:40) | sacrifício (12:43) e Cortés no altar (15:15) |
| Série | a bruxa | abre e fecha cada episódio; os Astecas abrem com o fim do episódio Nuclear |
- Média: **2–3 loops por vídeo**, plantados no 1º terço e pagos nos últimos 3 min.

### 3.9 CTA **[CORRIGIDO]**
- A manhã supôs bordão falado ("se inscreve ou a bruxa te pega"). **Na fala, o "subscribe" aparece em 2 de 6 vídeos, escondido numa piada de ≤ 2 s:** Egito 2:15 (o faraó "manda e pronto: se inscreve"); Roma 5:41 (no meio da rima do cardápio: "beba vinho aguado, você também devia se inscrever, desculpa, me perdi na rima"). Os outros 4 não pedem nada falando. O bordão "Subscribe or the Witch will get you" é **só da descrição**.
- Sem "deixa o like", sem CTA no fim.

### 3.10 Fecho **[MEDIDO]**
- **Abrupto**: a última cena é a morte, o resgate ou a volta da bruxa, e depois 10–30 s de música. **Nenhum resumo, nenhuma moral**, nenhum "no próximo vídeo". O gancho do próximo é **visual** (a bruxa) e a continuidade entre episódios é feita pela abertura do episódio seguinte.
- A lista de empregos fecha com uma frase seca ("só não deixe a solidão te pegar. É isso.").

### 3.11 Tabela-resumo dos 6 do Chat History

| | Egito | Roma | Grécia | Japão | Astecas | Lista empregos |
|---|---|---|---|---|---|---|
| duração | 8:27 | 15:09 | 11:35 | 12:58 | 15:52 | 20:37 |
| ppm | 183 | 159 (~170 de fala) | 179 | 159 (~170) | 173 | 171 |
| "you"/min | 12,4 | 8,1 | 10,4 | 8,1 | 6,9 | 3,2 |
| números/min | 0,9 | 1,1 | 1,0 | 0,3 | 1,2 | 2,1 |
| premissa dita até | 0:08 | 0:52 | 0:32 | 0:41 | 0:49 | 0:07 |
| esquete de abertura | não | sim (jantar) | sim (visual) | sim (visual) | recap do ep. anterior | não |
| blocos | 5 | 6 | 5 | 6 | 6 | 4 ofícios |
| piadas/min (amostra) | ~5 | ~2,5 | ~4 | ~3 | ~2 | ~2 |
| mortes faladas do avatar | 2 (flecha + colega) | 2–3 (metano, praga, dardo) | 1 (soco) | 0–1 | 0 (salvo) | — (3ª pessoa) |
| reinício "vamos supor" | sim | não | sim | sim ("mesmo que não fosse…") | não | — |
| loops | 1 | 2 | 1 | 1 | 3 | 0 |
| patrocínio como cena | não | sim (~3:05) | não | sim (~3:28) | não | não |
| CTA falado | 2:15 (piada) | 5:41 (rima) | não | não | não | não |
| fecho | "era um sonho" | falha cômica | sobrevive, mistério | bruxa volta | resgate (Cortés) | frase seca |

### 3.12 Bernard e Fossil: o que fazem diferente e vale pegar
**Bernard** (Tibete, 20:24, 166 ppm, **14,7 "you"/min**, ~1 piada/min, 0,7 número/min) não tem perigos nem mortes repetidas: é **uma vida inteira em 2ª pessoa no presente**, do nascimento ("você nasce numa casa de pedra a 4.000 m") à morte aos 41, com **saltos de tempo como transição de bloco** ("passam-se anos, você tem 16"; ~10 saltos), **personagens com nome e diálogo** (os três irmãos), o fato histórico **explicado por um personagem dentro da cena** (o pai explica a herança da terra), um **callback afetivo** plantado aos 2 min e pago aos 9 min (a desculpa dos "monges tibetanos") e um **epílogo emocional** depois da morte (quem chora longe). Vale pegar: saltos de idade como esqueleto para temas de **ofício/papel**, personagens recorrentes com nome e um fecho que comove em vez de cortar. **Fossil** (pré-história, 16:11, 169 ppm, 6,1 "you"/min, **3,6 números/min**, humor raro) abre com **perguntas em sequência** ("e com os dinossauros? e com milípedes de 2,4 m?"), define a **regra do jogo** em 1 frase ("só você, sem ferramentas") e passa **era a era (~16 eras, ~55 s cada)** com uma **ficha fixa** (mapa → ar → temperatura → água → comida/fogo → predador) e um **veredito de tempo** em cada era ("algumas horas", "dias", "semanas", "quase um ano") **+ nota de tier** (S/A/B/C/D), fechando com o ranking melhor/pior em 10 s. Vale pegar: o **cronômetro de sobrevivência** como contador (mede "quanto você durou" sem precisar dizer morte, ótimo para a política do canal) e a **ficha fixa por bloco**, que dá previsibilidade e alta densidade de dado.

---

## 4. Títulos (fórmulas com views reais)

| fórmula | exemplos (views) |
|---|---|
| **"Why You Wouldn't Survive [ERA/LUGAR]"** (lugar às vezes em CAIXA ALTA) | Ancient Egypt 3,94 mi · The Roman Empire 2,40 mi · Ancient Greece 2,35 mi · FEUDAL JAPAN 2,18 mi · THE REAL OREGON TRAIL 1,70 mi · THE AZTEC EMPIRE 1,39 mi |
| **"How Long You'd Last in Every [CONJUNTO]"** (Fossil) | Every Prehistoric Era **13,6 mi** · How Fast You'd Die in Every Prehistoric Ocean 2,27 mi · BeyondTheBlue "…Every Prehistoric Ocean" 3,90 mi · "…Every Planet" 1,19 mi |
| **"Why It Sucks to Be a [PAPEL] (in [ERA/LUGAR])"** (Bernard) | Empress (Ming) 2,77 mi · Shared Wife (Tibet) 1,93 mi · Joy Woman (Aztec) 1,78 mi |
| **"Your Life as a [PAPEL]"** (Lost Legacy) | Concubine 4,60 mi · Medieval Torturer 3,69 mi · Geisha 2,68 mi |
| **"The Most [ADJ] [COISA] in History"** (Chat History, listas de 2026) | Miserable Jobs 2,28 mi · Ridiculous Jobs That No Longer Exist 2,25 mi · One-Sided Wars 2,05 mi |
| **"What X Does to Your Body (Hour by Hour)"** (Infographics) | Lethal Radiation 3,29 mi · Life Sentence (Day 1 to Year 40) 3,97 mi |

Padrões: **2ª pessoa no título** ("You", "Your") + **cenário concreto** (era/lugar ou papel) + **ameaça** (survive / last / die / sucks). Lugar em CAIXA ALTA quando é o substantivo de busca. Nenhum título tem número de anos nem "história inteira".

## 5. Thumbs (6 thumbs top, `thumb_<id>.jpg` em assets)
1. **Egito (3,94 mi):** "YOU ARE **DEAD**" (branco + vermelho com contorno preto) no alto à esquerda; o bonequinho laranja do Fella com cocar egípcio, um Faraó-bonequinho gigante à direita com rosto feio, uma múmia-bonequinho no chão e céu de deserto. Três personagens e muita cor saturada.
2. **Roma (2,40 mi):** "YOU ARE **DEAD.**" ocupando a metade de cima; embaixo, o Fella (cabeça branca, corpo azul) caído de olhos esbugalhados, com o rosto ferido, sobre fundo escuro de pedra. Um personagem só, composição horizontal e alto contraste.
3. **Grécia (2,35 mi):** "YOU ARE / **DEAD**" vermelho gigante à esquerda; à direita, um bonequinho-meme musculoso de rosto "derp", outro bonequinho caído e o Partenon ao fundo, com céu azul.
4. **Japão (2,18 mi):** "FEUDAL / **JAPAN**" (branco + vermelho) à direita; à esquerda, o Fella com bandagem na cabeça, olho roxo, três flechas cravadas e uma katana atravessada. Fundo rosa (Fuji/sakura). A morte aparece no objeto (flechas, katana), não no texto.
5. **Astecas (1,39 mi):** "YOU ARE **DEAD**" no alto; o sacerdote-bonequinho com cocar arranca o coração do Fella, deitado num altar de pedra, e um sol com cara olha do canto. Gore cartunesco (sangue vermelho chapado).
6. **Oregon Trail (1,70 mi):** "**DYSENTERY**" em vermelho com respingo; o bonequinho de boina, apavorado, à esquerda e uma poça vermelha com cabeça verde doente à direita. A palavra-causa da morte é o texto.

Extras (formato lista de 2026): "MISERABLE **JOBS** IN HISTORY" e "**JOBS** THAT NO LONGER EXIST", com um bonequinho grande em close de expressão nojenta/sofrida ocupando 45% da esquerda, texto preto e vermelho em fundo branco e o selo "NO AI" num canto.

Padrões: **1 palavra de sentença** ("DEAD", "DYSENTERY") em vermelho com contorno, **o Fella sempre presente e sempre se dando mal**, 1 objeto da era que mata (flecha, katana, coração, múmia), cenário real/icônico desfocado ao fundo e cores primárias saturadas. O título e a thumb se completam: o título diz o lugar e a thumb diz o desfecho.

---

## 6. Esqueleto modelável v3 (revisado com as transcrições, 28/11/2026)
Esqueleto em palavras nossas. Nenhum texto do canal-base é reaproveitado; dispositivo, avatar, contador e bordões são **nossos** (lista abaixo). Ritmo de palavras: nossa voz mede **~128 ppm** com pausas (bíblia `roteiro.md`, tabela Tamanho: 126–136). Faixa usada: 128–140 ppm.
**Alvo: 13–14 min = 1.700–1.900 palavras** (12 min ≈ 1.550–1.700; 15 min ≈ 1.900–2.100). Não escreva acima de 2.100.

| # | passo | tempo-alvo | palavras | o que acontece |
|---|---|---|---|---|
| 1 | **Arremesso** | 0:00–0:40 | 80–95 | Mini-cena do avatar no presente (≤ 10 s, quase sem fala) interrompida pelo dispositivo nosso → **lugar + ano + "o pior momento"** em 1 frase → regra do jogo ("sem celular, sem vacina, sem dinheiro: dure até X") → pergunta "Quanto tempo você aguenta?" + bordão de largada. Premissa completa **até 0:30**. Cronômetro aparece. |
| 2 | **Chegada: onde você caiu** | 0:40–2:30 | 230–260 | Contexto em ≤ 4 frases, contado como fofoca, com 1 número. 1º obstáculo: língua/aparência/dinheiro → **desfecho provável ruim** (sugerido) → **reinício verbal nosso** ("Rebobina: vamos supor que…"). Planta o **loop 1** (personagem ou objeto que volta no fim). |
| 3 | **Seu degrau** | 2:30–4:30 | 250–280 | A pirâmide social e em que degrau você cai, com fato concreto. **CTA falado aqui (~3 min), 1 frase-piada ≤ 3 s.** Fecha com a consequência que empurra para o trabalho ("e degrau de baixo trabalha"). |
| 4 | **Um dia de trabalho** | 4:30–6:45 | 280–310 | Hora a hora no ofício mais provável para você (engenho, mina, porto, tropa), imperativos de guia ("não olhe para…", "segure assim"). Planta o **loop 2** (colega com nome). |
| 5 | **O corpo: comida, água, sujeira** | 6:45–8:45 | 250–280 | Cardápio, água, banheiro, rua. Gag visual forte. Termina com o **gancho de doença** (nossa versão da frase interrompida). |
| 6 | **Doença e "médico"** | 8:45–10:45 | 250–280 | A epidemia real da época com número (mortos, %) e o tratamento que piora tudo. 2º reinício. Cronômetro dá o salto maior. |
| 7 | **O clímax** | 10:45–13:00 | 280–310 | O maior perigo da era (revolta, recrutamento, naufrágio, guerra). **Pagam os loops 1 e 2.** Morte só sugerida (som, apagão, objeto que cai), nunca mostrada. |
| 8 | **Veredito + gancho** | 13:00–13:45 | 80–100 | Placar do cronômetro ("você durou 11 dias; o recorde da série é…"), 1 frase que vira o olhar para o presente **ou** eco emocional curto (estilo Bernard), e o dispositivo reaparecendo com o destino do próximo episódio. Sem resumo. |
| | **total** | **~13:45** | **1.700–1.915** | |

Regras de adaptação (medidas nas refs e convertidas para a nossa voz):
- **"Você"**: alvo **6–9 por minuto** (refs 7–12 em inglês, com mais palavras por minuto); misture narração no presente, imperativo de guia, "você seria…" e "vamos supor".
- **Humor**: **1 piada falada a cada 25–40 s** (~2/min; as refs fazem 2,5–5/min a 170 ppm) + gag visual em todo plano possível. Fato = preparação, piada = fecho. Escravidão e violência contra pessoas reais: **sério, sem piada**.
- **Números**: **≥ 1,5 por minuto** (acima das refs, que têm 1; é o diferencial de credibilidade, como no Fossil). Todo fato com fonte no `SOURCES.md`.
- **Transições**: cada bloco termina num acontecimento que **causa** o próximo (nunca "agora vamos falar de…"). Pontes válidas: necessidade do avatar, promoção/punição, "falando em…" no máximo 1×.
- **Loops**: 2 por vídeo, plantados até 6:45, pagos no clímax.
- **Reinícios**: 2–3 por vídeo, sempre verbais e sugeridos.
- **Patrocínio** (quando houver): como cena de ação muda de ≤ 60 s perto de 3:00.
- **Título**: "Você não sobreviveria a/ao [LUGAR + ANO]" ou "Quanto tempo você duraria em [CONJUNTO]". **Título, descrição e thumb nunca dizem morte/morreu/morto.**

## 7. NÃO copiar (marcas registradas dos canais-base) e substitutos nossos
Coerentes com bonequinhos de cabeça redonda e com a política: nada de morte gráfica; morte sugerida sem corpo nem sangue; título/descrição sem "morte/morreu/morto". **Não** usar carimbos nem "EXPEDIENTE" (são do `dossie-es`).

| marca deles | por que não | substitutos propostos (escolher 1) |
|---|---|---|
| **A Bruxa** (o dispositivo que arremessa o avatar) | personagem fixo, abre e fecha cada episódio | (a) **o Despachante do Tempo**: bonequinho burocrata com prancheta que chama senha ("senha 1904!") e despacha você; (b) **o elevador que erra o andar** (botões com anos; o painel pisca e abre num século errado); (c) **o celular que "atualiza o sistema"** e reinicia você em outra época (a tela de progresso vira o cronômetro) |
| **O "Fella"** (avatar branco de corpo azul) | avatar-marca deles | (a) **o Turista**: bonequinho de chinelo, bermuda e pochete, sempre fora de lugar; (b) **"Você"** com crachá escrito VOCÊ e boné na cor do canal; (c) **Zé do Presente**, de camiseta com estampa de wi-fi sem sinal |
| **Contador "DEATHS: N"** + barras de vida | HUD-marca e palavra proibida pela política | (a) **cronômetro "VOCÊ DUROU: 3 dias, 4 h"** (casa com o título "Quanto tempo você duraria"); (b) **"TENTATIVAS: N"** com ampulheta que vira a cada reinício; (c) **"SORTE: ●●●○○"**, bolinhas que vão apagando |
| Morte mostrada (thumb "YOU ARE DEAD", flechas cravadas, coração arrancado) | política do canal | (a) avatar **fica cinza e vira estrelinha** que sobe; (b) **apagão de tela** com o som e a placa "TENTE DE NOVO"; (c) **o chinelo do Turista sozinho** no chão. Thumb: 1 palavra-causa ("FEBRE", "CÓLERA", "3 DIAS") |
| "Let's find out" / "Think you could survive?" | bordão de largada deles (4 de 5 vídeos) | (a) **"Cronômetro valendo."**; (b) **"Bora ver quanto você aguenta."**; (c) **"Pega a senha e boa sorte."** (se for o Despachante) |
| "Mas vamos supor…" / "respawn" (reinício) | mecânica genérica, mas o "respawn" gamer é o vocabulário deles | (a) **"Rebobina."** com som de fita VHS voltando; (b) **"Senha nova."** (o Despachante chama de novo); (c) **"Versão com sorte:"** em placa |
| Frase cortada antes da doença ("você vai pegar algum tipo de—") | tique recorrente deles (3 vídeos) | (a) o Turista **espirra** e a tela congela numa placa com o nome da doença; (b) **"Spoiler:"** dito pelo narrador + nome da doença em letreiro de rodoviária; (c) o cronômetro **dispara para frente** sozinho |
| CTA "Subscribe or the Witch will get you" e o "subscribe" escondido em rima/ordem do faraó | bordão e piada de CTA deles | (a) **"Se inscreve antes que o Despachante chame a sua senha."**; (b) **"Inscreva-se: é a única vacina disponível em 1904."** (troca o ano); (c) **"Ativa o sininho; nesta época ninguém te avisava de nada."** |
| Cardápio rimado (Roma, Astecas) | bit recorrente deles | **placa de prato do dia de boteco** ("Prato do dia: farinha. Acompanha: mais farinha") ou o garçom-bonequinho que só tem 1 item |
| Vocabulário gamer (nível de pesca, espada +7, loot, NPC, DLC, "fogo amigo ligado") | identidade de humor deles | humor **de cotidiano brasileiro**: fila, cartório, boleto, Detran, aplicativo de entrega, grupo da família |
| Piadas fixas: "reaction channels" entre os párias, "a peste vem em 3 sabores… e morango", "era só um sonho", patrocínio de barbeador como luta ("foi por um fio") | piadas assinatura | não substituir 1 a 1: cada vídeo cria as suas a partir do tema |
| Humor sexual/grosseiro e piada com escravidão | política do canal e do Brasil | escravidão sempre séria; humor só contra o avatar, o narrador ou a burocracia da época |
| Selo "[NO AI]" | marca deles | não usar selo |
| Bernard: "Why It Sucks to Be…", desculpa dos "monges tibetanos", temas sexuais/tabus | marca e temática | título "Como era ser [papel] em [lugar, ano]"; callback afetivo criado por vídeo |
| Fossil: "you're toast", tiers S/A/B/C/D com a mesma arte | bordão e grafismo | veredito em **dias/horas no cronômetro**; se ranquear, use "nota de 0 a 10 de sobrevivência" em vez de tier |
