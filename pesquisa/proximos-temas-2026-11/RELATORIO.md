# Próximos temas: historia-ptbr (006, 007) e dossie-es (005, 006), 09/11/2026

Brief: `~/workspace/referencias/BRIEF-proximos-temas-2026-11.md`. Só pesquisa: nenhuma pasta de vídeo, linha em `youtube.videos` nem roteiro. Custo R$ 0; cota da Data API **223 unidades** (201 de enriquecimento + 22 de concorrentes); buscas e listagens via yt-dlp + WARP.

## Resposta curta

| Canal | Ordem | Tema | Título de trabalho | Número principal [O] | Hook (cena real) |
|---|---|---|---|---|---|
| historia-ptbr | **006** | **Roma** | A história INTEIRA de Roma em N minutos | Maior demanda pt entre os candidatos: **mediana top-10 (12 m) 544 mil**, 21 vídeos > 100 mil em 12 m; porta aberta (5 canais < 12 m com hit, ex. 3,3 mil insc. → 425 mil) | 390 a.C., Breno joga a espada na balança: "**Ai dos vencidos**" |
| historia-ptbr | **007** | **Rússia** | A história INTEIRA da Rússia em N minutos | Prova no molde **em pt**: clone "História em minutos" (canal de 08/2026, 5 mil insc.) fez **235 mil em 21 dias**, ~120× o Japão do mesmo canal (2 mil) | 862, os eslavos chamam os varegues: "Nossa terra é grande e rica, mas não há ordem nela" |
| dossie-es | **005** | **KGB** | TODA la historia de la KGB en N minutos | Molde aquecido agora: Te lo Pinto "La HISTORIA COMPLETA de la KGB" **196 mil em 10 dias**; Atlas KGB 41 mil + CIA vs KGB 52 mil; puxa sessão de CIA/Mossad/FBI | Londres, 1978: a picada do guarda-chuva em Georgi Markov |
| dossie-es | **006** | **Masones** | TODA la historia de los Masones en N minutos | **Mediana top-10 (12 m) 430 mil**, 6 vídeos recentes (< 90 d) > 100 mil, ninguém com tração no molde; porta aberta (canal de 08/2026, 4 mil insc., 167 mil + 161 mil) | 1826, Batavia (NY): William Morgan ameaça publicar os segredos e some para sempre |

Reservas: historia-ptbr **Japão** (008); dossie-es **Templarios** (007) e **Inquisición** (008).

---

## Método
- **Busca** (`scripts/buscar.py`): 240 consultas yt-dlp via WARP (24 temas pt × 2–4 consultas; 28 temas es × 1–3), cada uma em 2 ordens: relevância (40 resultados) e "este ano por views" (`sp=CAMSAggF`). 9.065 linhas, 6.384 vídeos únicos.
- **Enriquecimento** (`scripts/enriquecer.py`): `videos.list` + `channels.list` (título original, data, idioma do áudio, duração, canal: data de criação e inscritos).
- **Demanda** (`scripts/analisar.py` → `dados/demanda.json`): o vídeo conta para (idioma, tema) se o idioma (áudio ou título) for pt/es, o título citar o tema, durar ≥ 4 min e não for ficção/jogo/música. Em **pt**, também é preciso ter sinal de história no título ("história", "império", "antigo", "guerra", "rei", data…) e não ser ruído (Copa 2026, vlog de viagem, podcast/cortes, notícia). Sem esse filtro, "Argentina", "Japão" e "Espanha" vinham dominados pela Copa do Mundo 2026 (CazéTV 8 mi) e "Israel" por vlogs bíblicos. Em **es** (organizações) só o filtro de ruído.
  - **Med. 12 m** = mediana de views dos 10 mais vistos publicados desde 09/11/2025. **>100k 12 m** = quantos passaram de 100 mil nesse período. **Rec.** = publicados desde 11/08/2026 (< 90 dias) com > 100 mil.
  - **Porta** = canais criados há < 12 meses com vídeo do tema > 100 mil em 12 m (idade = criação do canal, não 1º vídeo; conferi o tema de cada um).
- **Concorrentes no molde** (`scripts/concorrentes.py` → `dados/concorrentes.json`): todos os uploads de 17 canais (pt: Crônicas de Ferro, História na Marra, 4 clones "História em Minutos", Era Humana; en: Genius History, History in Minutes, CountryCorns, Archive in Minutes, Spies in Minutes; es: Atlas del Tiempo, Te lo Pinto, Archivos en Minutos, Mapa del Ayer, Aprendes Mientras Duermes).
- **Limitações:** a busca do YouTube via WARP é uma amostra (não o universo); temas com nome ambíguo (Rússia/Ucrânia × guerra atual; Israel × Bíblia; Portugal × "em português") têm mediana contaminada mesmo com filtro; o filtro de pt é conservador e derruba alguns vídeos válidos (ex. Rússia: a mediana filtrada de 53 mil subestima, já que o hit no molde existe). Por isso a decisão cruza 3 fontes: demanda de busca, prova no molde e porta.

[O] = dado medido nesta pesquisa (09/11/2026) ou no banco. **Hipótese** = inferência sem dado direto.

---

## 1. historia-ptbr (pt-BR, países/impérios, molde History in Minutes)

**Ponto de partida [O]** (`youtube.studio_video`, 12/10–08/11): Egito 920 impressões / CTR 4,02% / 44,9% visualizado; Índia 1.273 / 3,69% / 42,2%; Irã 41 / 4,88%. O CTR e a retenção estão ok; falta **impressão**. O tema precisa trazer busca e navegação (sugeridos) em pt.

### Tabela

| Tema | Med. 12 m [O] | >100k 12 m / Rec. [O] | No molde em pt (views) [O] | Molde en (views) [O] | Porta [O] | Sessão com o que já temos | Risco | Roteiro na v2 | Nota |
|---|---|---|---|---|---|---|---|---|---|
| **Roma** | **543.936** | **21 / 3** | History Easy Guide "A HISTÓRIA INTEIRA de Roma em 12 min" 24,9 mil (10/2026); História na Marra "COMPLETA do Império Romano" (74 min) 17,7 mil em 1 dia; clones 47–168 | Genius 385 mil; HiM 21 mil | **aberta**: 5 canais < 12 m (Um Documentário 742 mil; Arquivos do Velho Mundo, 3,3 mil insc., 425 mil; Biografias Irrelevantes 348 mil) | **Egito** (Cleópatra, César, Augusto; Egito = celeiro de Roma); Irã (partos/sassânidas) | baixo | fácil: problema→solução→problema natural (cidade → república → império → crise → queda); muitas cenas famosas | **9,5** |
| **Rússia** | 52.716 (filtro derruba guerra/podcast; sem filtro 631 mil) | 4 / 2 | **clone "História em minutos" (08/2026, 5.050 insc.): "Toda a história da Rússia em 37 minutos" 235.160 em 21 dias**; Atlas do Tempo/outros < 3 mil | HiM 43 mil | **aberta** (o próprio clone) | China (mongóis), Irã (guerras russo-persas), Ucrânia depois | médio: guerra atual (comentários polarizados; fechar na queda da URSS + 1 frase) | fácil: fio "terra enorme × ordem" (ver hook); eras com virada clara (mongóis, Ivã, Pedro, 1917, 1991) | **8,5** |
| Japão | 137.619 | 6 / 1 | clone "História em minutos": **1.970** (mesmo canal que fez 235 mil com a Rússia); História do Mundo (05/2026, 11 mil insc.) "A História do Japão Inteiro" 106 mil (08/2026); Dormindo com História 75 mil | **Genius 869 mil**; CountryCorns 116 mil | aberta (História do Mundo, Guerra de Impérios) | **China** (004) | baixo | fácil: fio "fechar × abrir para o mundo"; hook do *kamikaze* de 1281 | **8** (reserva 008) |
| Portugal | 159.400 | 6 / 1 | Sociedade Épica 25,7 mil; HQ 25,3 mil; clone 8 | — | parcial (Civilizações Explicadas, 21 mil insc., Inês de Castro 366 mil) | **Brasil** (005) | baixo | fácil | 7 |
| Ucrânia | 332.859 (quase tudo guerra atual) | 7 / 1 | clone 25 mil; outro clone 1,7 mil | HiM 179 mil | fechada para história (porta = mercenários na guerra) | Rússia | **alto** (guerra em curso) | difícil sem tomar lado | 5 |
| Alemanha | 178.137 | 8 / 1 | História do Mundo em HQ 127 mil (03/2026) | Genius 183 mil | fechada | — | médio (nazismo no meio) | médio | 6,5 |
| Estados Unidos | 71.405 | 4 / 1 | Legados da História "em 11 Minutos" 96,7 mil | Genius 421 mil | parcial | Brasil | baixo | fácil | 6 |
| Grécia | 82.198 | 3 / 0 | Reinos Esquecidos 126 mil (2025); Era Humana 86,6 mil; HnM "Atenas vs Esparta" 61,7 mil, "Macedônia" 98 mil; clone 49 | Kelevin "Greek Mythology" 847 mil (mitologia, não país) | aberta (Reconstrução do Passado) | Roma, Egito, Irã | baixo | médio (antiga demais: "até hoje" fica fraco) | 6 |
| Mongóis | 53.196 | 3 / 1 | ~1 mil | — | parcial | China, Irã, Rússia | baixo | fácil (curto) | 5 |
| Império Otomano | 19.103 | 0 / 0 | 2,2 mil | — | fechada | Irã | baixo | médio | 4 |
| Império Britânico | 26.623 | 3 / 0 | < 2 mil | Genius 230 mil | fechada | Índia, Egito | baixo | médio | 4 |
| Israel | 350.225 (vlogs bíblicos) | 9 / 1 | Total History 70 mil (10/2026) | CountryCorns 1,14 mi; Genius 78 mil | — | Egito, Irã | **alto** (conflito atual) | difícil | 4 |
| *França (dado sugere)* | 17.398 (busca) | 2 / 1 | **clone "História em minutos" 167.450 em 17 dias**; Depois do Poder 27 mil | — | aberta (clone) | — | baixo | fácil | 7,5 |

Também medidos (med. 12 m): Itália 208 mil (ruído: pizza, F1), Coreia 43 mil, Espanha 24 mil, Bizâncio 22 mil, México/astecas 20 mil, Cartago 20 mil, Vikings 10 mil, Incas 4 mil. Canal clássico que domina o "A História de X" em pt no acumulado: Impérios AD (Israel 3,3 mi, EUA 1,9 mi, Inglaterra 1,4 mi, Otomano 894 mil) e Canal Nostalgia (Japão 11,8 mi): porta fechada no acumulado, mas sem vídeo novo no molde curto.

### Leitura
1. **Roma é o tema com mais demanda de busca em pt** entre os candidatos (544 mil de mediana, 21 vídeos acima de 100 mil em 12 meses) e **a porta está aberta** para canal pequeno (Arquivos do Velho Mundo, criado em 04/2026, 3,3 mil inscritos, 425 mil num vídeo sobre a queda de Roma) [O]. O molde curto em pt ainda não tem dono: o melhor "A HISTÓRIA INTEIRA de Roma" tem 24,9 mil [O]. Liga com o Egito (Cleópatra, César, Augusto), o vídeo com melhor retenção do canal.
2. **Rússia tem a prova mais limpa do molde em pt.** O mesmo canal novo publicou Rússia (235 mil), França (167 mil), Ucrânia (25 mil), Índia (3,5 mil), Egito (2,4 mil) e Japão (2 mil) em 3 semanas, no mesmo formato [O]: o tema explica 100× de diferença dentro do canal. A busca filtrada subestima a Rússia porque quase tudo com "Rússia" no título em 2026 é guerra/podcast. **Hipótese:** o público pt de "história inteira" navega (sugeridos) por Rússia/França mais do que pesquisa.
3. **Japão** tem demanda e porta (História do Mundo 106 mil), mas o mesmo clone que fez 235 mil com a Rússia fez **2 mil** com o Japão [O]. Fica como reserva (008), com sessão forte com a China.
4. **Descartados por enquanto:** Ucrânia e Israel (demanda é da guerra atual: risco de anúncio e de polarização, sem porta para história); Otomano e Britânico (pt quase sem demanda recente: 19–27 mil); Mongóis (53 mil). Portugal fica na fila para puxar sessão do Brasil (demanda média, 159 mil).

### Recomendação historia-ptbr

**006: Roma.** *A história INTEIRA de Roma em N minutos* (braço B do teste de título, `biblia/titulo.md`: "Como uma aldeia virou dona do mundo, e por que ela caiu?").
- **Hook (≤ 45 s, cena real):** 390 a.C. Os gauleses de Breno tomaram Roma; os romanos aceitam pagar mil libras de ouro para eles irem embora. Na pesagem, os romanos reclamam que os pesos são falsos. Breno tira a espada e joga em cima da balança: "*Vae victis*. Ai dos vencidos." Fontes: Tito Lívio, *Ab Urbe Condita* 5.48; Plutarco, *Vida de Camilo* 28. (Detalhe dos pesos e da espada: Lívio; a historicidade do saque de 390 é aceita, os diálogos são tradição: dizer "conta Lívio".)
- **Pergunta central:** "Como uma cidade que pagou resgate a bárbaros virou a dona do mundo e, oitocentos anos depois, foi ela a vencida?"
- **Fio condutor:** a balança/"ai dos vencidos": Roma aprende a regra (Cartago 146 a.C.: "Cartago deve ser destruída"), vira a mão que pesa, e o loop fecha em 410 (Alarico saqueia Roma) e 476. **Ponte com o espectador:** o calendário de julho/agosto, o latim no português, a estrada.
- **Dificuldade v2:** baixa. Cada era tem problema herdado claro (reis → república; Cartago; crise da república → César; império grande demais → divisão → queda). Cuidado: muita coisa conhecida, então cortar curiosidades (regra 5) e não passar de 17 min.

**007: Rússia.** *A história INTEIRA da Rússia em N minutos* (braço B: "Por que o maior país do mundo sempre quer mais?").
- **Hook:** 862. Tribos eslavas e finesas brigam entre si; na *Crônica dos Tempos Passados* (Crônica de Nestor, c. 1113, ano 6370), mandam dizer aos varegues (vikings) do outro lado do mar: "Nossa terra é grande e rica, mas não há ordem nela. Venham reinar sobre nós." Rurik vem. Fonte: *Povest' vremennykh let*, entrada de 862 (trad. Cross & Sherbowitz-Wetzor, 1953). (É lenda de fundação contada pelos próprios russos: dizer "segundo a crônica".)
- **Pergunta central:** "Por que um país tão grande vive chamando um homem forte para pôr ordem nele?"
- **Fio condutor:** "grande e rica, mas sem ordem": a frase volta com os mongóis, Ivã, Pedro, 1917, 1991. Mini-hook de capítulo: Vladimir escolhendo religião em 987 ("beber é a alegria da Rus", mesma crônica).
- **Risco:** guerra atual. Fechar em ~1991–2000 com uma frase neutra; nada de mapa de front; sem tomar lado. **Dificuldade v2:** baixa (eras com virada forte e cena: Kiev queimada, Ivã, Pedro raspando barbas, Tsarskoye/1917, 1991).

**O que medir nos dois (vs. Egito/Índia):** impressões no dia 7 (meta > 2× os ~1 mil do Egito/Índia), % de tráfego "Pesquisa do YouTube" × "Vídeos sugeridos" (Studio), CTR ≥ 3,7% e % visualizado ≥ 42%. Se Roma trouxer impressões por busca e a Rússia por sugeridos, a Hipótese do item 2 se confirma.

---

## 2. dossie-es (es, organizações/serviços secretos, molde Archive in Minutes)

**Ponto de partida [O]** (`youtube.studio_video`): Mossad **5.521 impressões**, CTR 2,32%, 48,2% visualizado; CIA 633 impressões, 2,21%, 47,1%. No mesmo período, o Atlas del Tiempo tem Mossad 72,7 mil (01/11) e CIA só 956 (07/11, depois do nosso) [O]. **Hipótese:** o nosso volume de impressões acompanha a força do tema no molde em es (somos sugeridos ao lado do Atlas/Te lo Pinto); 2 vídeos não provam.

**Mudança no mercado desde 04/11 [O]:**
- **Te lo Pinto** (599 mil insc.) entrou no formato "HISTORIA COMPLETA": KGB 196 mil (30/10), Gestapo 120 mil (04/11). É o concorrente grande no nosso molde em es.
- **Atlas del Tiempo** virou fábrica de serviços secretos: KGB 41 mil, CIA vs KGB 52 mil, Gestapo 11 mil, Stasi 7 mil, SS 3,7 mil, MI6 vs KGB 3,7 mil, Beria 709, CIA 956, Vaticano 2 mil.
- **Clones novos com o nosso ângulo América Latina**, sem tração: "Archivos en Minutos" (07/2026, 1 insc.): Stasi 45, Che 3, **Operación Cóndor** 2; "Mapa del Ayer" (0 insc.): **Operación Cóndor** 2, DINA 0, Nazis en Argentina 0, Cartel de Medellín 0.

### Tabela

| Tema | Med. 12 m [O] | >100k 12 m / Rec. [O] | No molde em es (views) [O] | Atlas / Te lo Pinto [O] | Porta [O] | Ângulo América Latina | Risco de anúncio | Sessão | Nota |
|---|---|---|---|---|---|---|---|---|---|
| **KGB** | 126.649 (top total 240 mil) | 6 / **3** | Te lo Pinto 196 mil (10 d); Atlas 41 mil; clone pt 2 | Atlas KGB 41 mil, CIA vs KGB 52 mil; Te lo Pinto 196 mil | parcial (Ascenso y Ruina, 1,8 mil insc., "Mossad que humilló a la KGB" 113 mil) | Trótski/Mercader no México (1940), Cuba, Nicarágua | baixo | **máxima** (CIA, Mossad, FBI) | **8,5** |
| **Masones** | **430.150** (top total 1,18 mi) | 15 / **6** | Aprendes Mientras Duermes 45 mil (70 min); outros < 200 | nenhum (Te lo Pinto "Illuminati" rangos 115 mil) | **aberta**: Tus Noches de Historia (08/2026, 4 mil insc.) 167 mil e 161 mil | **forte**: Logia Lautaro (San Martín, O'Higgins, Alvear, 1812), Juárez, Maximiliano ("Inglaterra y la masonería rompieron Hispanoamérica" 1,15 mi) | baixo–médio (comentários conspiratórios; manter histórico) | nova (sociedades secretas: Templarios, Illuminati, Jesuitas) | **8,5** |
| Templarios | 190.887 (top total 912 mil) | 8 / 1 | Memorias de Pez "en 10 minutos" 1,35 mi (2021); "duerme" 376 mil e 128 mil | Te lo Pinto "Tu vida en cada rango" **2,2 mi** (05/2026) | fechada (as 2 "portas" são filme e música) | fraco | baixo | nova | **7,5** (reserva 007) |
| Inquisición | 129.452 (top total 1,35 mi) | 7 / 2 | **Academia Play "La inquisición en 15 minutos" 4,7 mi** (2018); Memorias de Pez 248 mil | nenhum | aberta (Mundos Reinventados, 14 mil insc., 188 mil; Memoria del Mundo 114 mil) | **forte**: tribunais de Lima, México (1571) e Cartagena | baixo–médio (religião) | Templarios, Jesuitas | **7,5** (reserva 008) |
| Jesuitas | 73.916 | 5 / 0 | nenhum relevante | nenhum | aberta (Imperios en Cenizas, 2,8 mil insc., 248 mil) | forte (missões, expulsão de 1767) | baixo | Inquisición | 6 |
| Opus Dei | 160.351 | 7 / 3 | nenhum | nenhum | fechada | médio (Espanha, México, Chile) | **médio–alto** (organização viva, depoimentos de ex-membros, risco jurídico) | Vaticano | 5 |
| Yakuza | 160.092 | 8 / 3 | "HISTORIA completa" 1,7 mil | Te lo Pinto rangos 1,2 mi | parcial | nenhum | médio (crime, como Cosa Nostra) | Cosa Nostra | 6,5 |
| Illuminati | 132.968 | 5 / 2 | nenhum | Te lo Pinto rangos 115 mil | parcial | fraco | médio (conspiração) | Masones | 5,5 |
| Operación Cóndor | **26.647** | 2 / 1 | **2 clones em 08–09/11** (2 views cada) | nenhum | fechada | máximo | médio (política, ditaduras) | CIA | 3,5 |
| Vaticano | 227.094 (podcasts) | 8 / 1 | nenhum | Atlas 2 mil | fechada | fraco | baixo | — | 4 (é Estado, não organização) |
| ETA | 140.218 | 9 / 3 | Memorias de Pez 645 mil (2018) | nenhum | — | nenhum (Espanha) | **alto** (terrorismo) | — | 3 |

Também medidos (med. 12 m): fuerzas especiales/Navy SEALs 377 mil (Te lo Pinto 5,2 mi: formato "rangos", não "historia completa"), SS 243 mil e Gestapo 103 mil (risco, backlog), KKK 150 mil (risco alto), mafia rusa 87 mil, ninjas 112 mil, Orden de los Asesinos 46 mil, Legión Extranjera 8,5 mil, NKVD/Spetsnaz 8,5 mil, Camorra 8 mil, Stasi 4,7 mil, Rosacruces 3,6 mil, Orden de Malta 1 mil, Guardia Suiza 373, DINA 260, Pinkerton 372.

**Termo do título (regra da `biblia/titulo.md`) [O]:** no pool, "masón/masones" aparece em 68 títulos (mediana top-10 1,09 mi) × "masonería" em 53 (690 mil) → **"los Masones"**. "Templarios" sozinho (91 títulos, 1,15 mi) > "Caballeros Templarios" (31, 232 mil).

### Leitura
1. **KGB primeiro, apesar da concorrência.** A demanda de busca é média (127 mil), mas é o tema mais quente do molde em es agora (Te lo Pinto 196 mil em 10 dias, Atlas 41 mil + 52 mil) e o que mais puxa sessão dos 4 vídeos que já temos [O]. Se a Hipótese das impressões vale (Mossad: Atlas forte → 5,5 mil impressões; CIA: Atlas fraco → 633), a KGB é o melhor tema para ser sugerido ao lado de vídeos grandes. Diferencial: hook do Markov e o expediente de Trótski/Mercader no México, que Atlas e Te lo Pinto não usam como porta (**Hipótese**: não transcrevi os dois; conferir na etapa de referência). Esperar mais custa: a cada semana, mais um clone faz KGB.
2. **Masones é a maior demanda de busca sem risco** da lista do brief (430 mil de mediana, 6 vídeos recentes acima de 100 mil) e **ninguém com tração fez no molde** [O]. A porta está aberta (canal de 2,5 meses com 2 vídeos de 160 mil). Tem o melhor ângulo América Latina (Logia Lautaro e as independências) e inaugura um 2º "cluster" (sociedades secretas) que puxa Templarios, Inquisición, Jesuitas e Illuminati depois.
3. **Templarios** cai para reserva: a demanda é boa no acumulado, mas recente é 1 vídeo > 100 mil e o maior é um "rangos" do Te lo Pinto (2,2 mi), outro formato. **Inquisición** tem o melhor histórico no molde (Academia Play 4,7 mi "en 15 minutos", 2018) e porta aberta: reserva 008.
4. **Operación Cóndor sai da fila:** busca baixa (27 mil) e 2 clones já publicaram no molde em 08–09/11 com 2 views [O]. O ângulo América Latina rende como expediente dentro de CIA/KGB, não como tema próprio.

### Recomendação dossie-es

**005: KGB.** *TODA la historia de la KGB en N minutos* (B: "La historia COMPLETA de la KGB en N minutos"). Roteiro pt de partida: `canais/dossie-es/arquivo-ptbr/001-kgb-ptbr/` (adaptar nativo).
- **Hook (25–35 s):** Londres, 7 de setembro de 1978, ponte de Waterloo. Georgi Markov, dissidente búlgaro da BBC, sente uma picada na coxa; um homem recolhe um guarda-chuva e some num táxi. Quatro dias depois ele está morto; na autópsia, uma esfera de 1,7 mm com ricina. O ex-general da KGB Oleg Kalugin contou depois que a KGB forneceu o veneno e o método ao serviço búlgaro. Fontes: Kalugin, *The First Directorate* (1994); BBC, "Georgi Markov: Death of a dissident" (2008); Metropolitan Police (inquérito reaberto em 2008). Dizer "con ayuda de la KGB" (quem executou foi a DS búlgara).
- **Expediente América Latina:** Coyoacán, 20 de agosto de 1940: Ramón Mercader e o piolet (NKVD, antecessora da KGB). Fontes: Andrew & Mitrokhin, *The Sword and the Shield* (1999); Museo Casa de León Trotsky.

**006: Masones.** *TODA la historia de los Masones en N minutos* (B: "La historia COMPLETA de la Masonería en N minutos").
- **Hook (25–35 s):** Batavia, Nova York, setembro de 1826. William Morgan, pedreiro e ex-maçom, anuncia um livro com os segredos da ordem. Em 12 de setembro é levado da cadeia de Canandaigua numa carruagem e nunca mais é visto. A revolta pública cria o **Partido Antimasónico**, o primeiro "terceiro partido" dos EUA. Fontes: Encyclopaedia Britannica, "Morgan affair"; William Preston Vaughn, *The Antimasonic Party in the United States, 1826–1843* (1983). (Que ele foi morto nunca foi provado: dizer "nunca más fue visto".)
- **Expedientes (ideia):** taberna Goose and Gridiron, Londres, 24/06/1717 (4 lojas fundam a Grande Loja); bula *In eminenti* (1738); Logia Lautaro (Cádiz/Buenos Aires, 1812: San Martín, Alvear); Juárez; P2 na Itália (1981); cierre voltando ao livro de Morgan.
- **Cuidados:** tom de dossiê histórico, sem "dominam o mundo"; símbolos maçônicos ok, sem satanismo/Illuminati na thumb (não dou palpite em thumb além disso: teste A/B rodando).

**O que medir nos dois (vs. Mossad):** impressões no dia 7 (Mossad 5,5 mil), origem do tráfego (sugeridos de quais canais: Te lo Pinto/Atlas na KGB), CTR (Mossad 2,3%) e % visualizado (48%). Masones testa se um tema de **busca** alta sem molde aquecido traz impressões sozinho: se ficar perto da CIA (633), a Hipótese "carona no molde" ganha força e a ordem seguinte prioriza temas que Atlas/Te lo Pinto já aqueceram.

---

## Arquivos
- `scripts/`: `buscar.py`, `enriquecer.py`, `analisar.py`, `concorrentes.py` (rodar nessa ordem; `enriquecer.py` e `concorrentes.py` a partir de `tools/`).
- `dados/`: `busca.jsonl` (bruto), `videos_api.json`, `canais_api.json`, `demanda.json` (tabela por tema com top-10, molde, porta, recentes), `concorrentes.json`.
