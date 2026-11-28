# Em Relevo: como otimizar a retenção (28/11/2026)

Estudo para o formato atual (mapa 3D/satélite animado + fotos/vídeos reais + narração ElevenLabs + trilha), **sem mudar o formato**. Base: 002 `FeSLzHvlkbo` (12:10, 59% de retenção média) contra 7 vídeos de clima/desastre de 2026 (4 gringos, 3 brasileiros). Custo pago: US$ 0 (yt-dlp e Whisper via WARP, 360p; vídeos apagados depois).

**Como medi.** Cortes = `ffmpeg select='gt(scene,0.3)'`. Como motion contínuo quase não tem corte seco, há também **mudanças visuais/min** (diferença média entre quadros a 2 fps em 64×36 > 0,05) e **% de tela parada** (diferença < 0,003). Tipo de visual = 1 quadro a cada 10 s (15 s nos vídeos de mais de 21 min), classificado a olho nas grades de `frames/`. Hook = Whisper dos primeiros 45 s; meio e fim = legenda automática. Números de todos os vídeos em `metricas-videos.json`.
**Limite:** a curva de retenção dos concorrentes não é pública. Do lado deles temos as views (sucesso), não a retenção. Toda ligação "técnica → retenção" vem da nossa curva ou fica como **Hipótese**. O 002 tem só ~163 views: cada espectador vale ~0,6 pt na curva, então quedas de 2–3 pts são ruído. Só valem as quedas grandes e as inclinações longas.

## 1. Amostra de canais
Mediana de views e duração típica dos 30 últimos vídeos longos (yt-dlp, views arredondadas pelo YouTube).

| Canal | Idioma | Inscritos | Mediana de views | Duração típica | Vídeo analisado (views) |
|---|---|---|---|---|---|
| The Last Day | en | 37,7 mil | 155 mil | 19 min | Nepal's 2026 Disaster Explained (5,3 mi) |
| RealLifeLore | en | 7,9 mi | 1,2 mi | 32 min | Why The Nepal Flood Was WAY Scarier… (2,4 mi) |
| UnderTheHeadline | en | 16,6 mil | 39 mil | 14 min | Nepal Floods 2026 Explained (4,1 mi) |
| El Mecanismo | es | 51,9 mil | 110 mil | 12 min | ¿Por qué este Súper Niño es el más peligroso? (2,3 mi) |
| CanalSingularidade | pt | 12,5 mil | 1,4 mi (2 vídeos) | 11 min | O Pacífico está PARTINDO o BRASIL em DOIS (2,2 mi em 4 dias) |
| Sou curioso?! | pt | 11,7 mil | 239 mil | 25 min | O El Niño de 2026 NÃO é o que você pensa (1,1 mi) |
| Cosmos Brutal | pt | 844 | 1 mil | 11 min | O SUPER El Niño visto do espaço (100 mil) |
| *(ref.)* Olá, Ciência! | pt | 2,65 mi | 450 mil | 14 min | O impacto real do Super El Niño na sua vida (1,4 mi; não analisado) |

Observação: o Singularidade e o El Mecanismo usam o **mesmo molde de roteiro** (mesmo "aviso honesto: super não é termo oficial", a mesma promessa da "Terra que gira mais devagar" paga no fim, a mesma frase de fecho e o mesmo CTA "com dados e não com medo"). Provavelmente é o mesmo produtor. Isso faz dele um molde que já deu certo duas vezes, em pt e em es.

## 2. Comparativo por vídeo
| Vídeo | Dur. | Cortes/min (0–30 s / 30 s–2 min / meio / fim) | Plano médio | Mudanças visuais/min (0–30 s / 30 s–2 min / meio / fim) | Tela parada | Mapa+motion / vídeo real / foto / gráfico-texto | Troca de tipo a cada | Pessoas na tela |
|---|---|---|---|---|---|---|---|---|
| **002 Em Relevo** | 12:10 | 0 / 0 / 0,5 / 1,0 | 91 s* | **30 / 10 / 11,5 / 13** | 4% | 48 / **0** / 18 (12 de chão + 6 satélite) / 34 | ~16 s; mas blocos de 45–100 s (diorama, régua) | ~3% |
| 005 Em Relevo | 9:48 | 4 / 3,3 / 2,1 / 5,1 | 16 s | 26 / 16 / 14,5 / 12 | 6% | 54 / 0 / 8 / 37 | ~15 s | ~2% |
| The Last Day | 19:19 | 6 / 14,7 / 12,1 / 13,9 | 4,6 s | 68 / 30 / 35 / 30 | 20% | 9 / **84** / 0 / 7 | ~30 s (o plano troca a cada 4,6 s) | ~40% |
| RealLifeLore | 30:10 | 2 / 3,3 / 2,2 / 1,9 | 26 s | 6 / 49 / 30 / 34 | 10% | 23 (Google Earth 3D com trajeto) / 63 / 0 / 5 (+9 de patrocínio) | ~50 s | ~25% |
| UnderTheHeadline | 12:31 | 0 / 0,7 / 0 / 0,6 | 150 s* | 50 / 10 / 8 / 4 | 75% | 28 (maquete de relevo "AI simulation" + mapa) / 3 / 0 / 69 (cartões de texto) | ~20 s | 0 |
| El Mecanismo | 11:31 | 0 / 0 / 0 / 0 | — * | 28 / 2,7 / 7,5 / 7 | 65% | 45 / 7 / 0 / 48 | ~15–20 s | ~1% |
| Singularidade | 10:45 | 0 / 0 / 0 / 0 | — * | 8 / 1,3 / 4 / 2 | 55% | 55 / 0 / 0 / 45 | ~15–20 s | 0 |
| Sou curioso?! | 25:48 | 14 / 14 / 15 / 15 | 4,0 s | 24 / 35 / 33 / 36 | 3% | 50 (2D chapado) / 45 / 0 / 5 | ~15–20 s | ~10% |
| Cosmos Brutal | 19:33 | 0 / 0 / 0 / 0,1 | — * | 4 / 5 / 3 / 4 | 75% | 40 / 0 / 25 (foto com Ken Burns) / 35 | ~20–30 s | ~3% |

\* Motion contínuo: o detector de corte seco não enxerga as transições. Para esses vídeos, vale a coluna de mudanças visuais.

| Vídeo | Hook literal (0–30 s) e cena física | Como segura o meio | Som | CTA de inscrição | Fecho |
|---|---|---|---|---|---|
| **002** | "Manaus, 9 de outubro. A fumaça das queimadas fecha escolas… 200 microgramas… A OMS recomenda no máximo 15. / Dionísio Cerqueira, 581 mm / Peru, +5,5 °C." Cena física **só na fala**: na tela, satélite MODIS e números | 4 perguntas numeradas (barra); "mas tem um detalhe que quase ninguém conta"; régua de recordes ao vivo | trilha constante (piso −32 dB), 0,16 silêncio/min, SFX nas transições | só no fim (11:59) | volta ao hook + "manda para quem…" |
| The Last Day | "At 8:37 in the morning on August 26th, 2026, a wall of ice the size of a small mountain let go… more than 900 people were dead… a valley… simply did not exist anymore." Na tela, o **vídeo de CCTV** da onda | crônica minuto a minuto; "The Second Threat" (7:28, ~39%) abre um novo perigo; pessoas em ~40% dos quadros | cama de música e ambiente densa (piso −27,5 dB), 0 silêncios | nenhum | imagem aberta: "a new lake is quietly filling… waiting" |
| RealLifeLore | "Some of the most terrifying footage… the internet has ever seen… a surveillance camera captured… a towering wall of water…" (vídeo real) | escalada "scarier than you think"; contrafactual "se tivesse sido 6–8 h depois…" (23:06); mapa 3D com o trajeto da água entre os vídeos | música baixa, 0,8 silêncio/min | patrocínio no fim (27:51) | patrocínio |
| UnderTheHeadline | "At 37 minutes past 8… a mountain… came apart… This is exactly how that happened, and why most of what was published in the first 24 hours was wrong." + contrato "estabelecido / em disputa / ninguém sabe" | **contagem numerada "Six stages… Stage one… Stage six"**; "Here's the thing that should actually…"; bloco final "What nobody knows yet" | quase seco (piso −48,7 dB), **4,7 pausas/min** | nenhum (só "thank you for watching") | "vou atualizar isto" |
| El Mecanismo | "El 21 de septiembre el Pacífico marcó una cifra que nadie había visto nunca… 3,11 °C… en 1998… apareció un lago de 145 km… en uno de los desiertos más secos." | **loop adiado no hook:** "puede hacer que la Tierra gire más despacio… Suena a exageración. No lo es. **Llegaremos a eso**", pago aos 9:05 (79%); "Si te quedaras aquí, pensarías que esto es un problema de playas. Pero…" | seco, 0,35 silêncio/min | **0:54, dentro do hook:** "si te gusta entender estas cosas con datos y no con miedo, suscríbete" + 11:13 | frase-tese + pedido para compartilhar "con alguien que viva cerca de la costa o de un río grande" |
| Singularidade | "Em outubro de 2023 o rio Negro em Manaus chegou ao nível mais baixo… barcos encalhados… botos mortos… Em 1983, Blumenau debaixo d'água… a mesma origem… o que está se formando lá agora é maior." | mesmo loop adiado ("**no final eu vou te mostrar o efeito mais estranho de todos… dá para medir no relógio**", 0:48 → pago aos ~8:20, 78%); "super" respondido já em **1:30**; "mas tem um detalhe que quase ninguém conta" | seco, piso −48,7 dB | **3:48 (35%), como ponte:** "se você gosta de entender com dados e não com medo, se inscreve… porque é a partir daqui que o Brasil entra na história" + no fim | "compartilhe com alguém que mora perto de um rio grande, no Sul ou na Amazônia" |
| Sou curioso?! | "19 de setembro de 2026… 5 mil km, maior que do Oiapoque ao Chuí, 3° acima… energia suficiente para **mudar o preço do frango no seu mercado, a cor da sua conta de luz e os casos de dengue na sua cidade**." | "aposto que você ia responder… não está errado, mas está pequeno"; **5 "paradas" numeradas** (9:06–16:13); "Lembra da…?" (callbacks); 1,3 "você"/min | música constante, piso −40 dB | nenhum explícito | "se você chegou até aqui, já sabe mais que quem fala na TV" |
| Cosmos Brutal | "Neste exato momento, uma faixa do Pacífico quase duas vezes maior que o Brasil… 2,47 °C… o recorde era de 1982. E 1982 terminou em tragédia." | capítulos-pergunta; região por região; "vai ter apagão?" | música constante | só no fim (19:22) | "o que fazer" (alertas por CEP) + CTA |

**O que se repete nos 7:**
1. Hook com **hora/data exata + uma cena física** (onda, lago no deserto, rio seco, frango mais caro) e o **tamanho da consequência** (900 mortos; "o vale deixou de existir") em ≤ 30 s.
2. Até ~1 min, **uma promessa que só se paga no fim** (Tierra más lenta, "seis estágios", "o que ninguém sabe ainda", "5 paradas").
3. A **pergunta do título** começa a ser respondida cedo ("super" em 1:05–1:30), mas a **última peça fica para o fim**.
4. O ritmo de cortes **não é** o que separa: há hits com 13–15 cortes/min (Last Day, Sou curioso) e hits com tela parada 55–75% do tempo (Singularidade, El Mecanismo, UnderTheHeadline). O que todos têm é **texto/visual novo a cada ~15–20 s** e roteiro com loops.

## 3. A curva do 002 (leitura de 28/11/2026, `youtube.analytics_retencao`; t = ratio × 730 s)
Retenção relativa (contra vídeos parecidos do YouTube): **0,39–0,57 nos primeiros 10%**, ~0,52 no meio e **0,60–0,77 do minuto 8 ao fim**. Ou seja: começamos abaixo da média e terminamos acima.

| Trecho | Audiência | Δ | Na tela | Na narração | Leitura |
|---|---|---|---|---|---|
| 0:00–0:15 | 102 → 98% | −4 | satélite MODIS de Manaus, contador 196 µg/m³ | b01 Manaus | o hook segura |
| 0:15–0:44 | 98 → 86% | −12 | SC 581 mm, Peru +5,6 °C; **crossfade A→B com câmera parada (0:29,8–0:36,2)** | b02–b05: "3 notícias… mesmo nome… é o Super El Niño?" | perda normal de hook |
| **0:44–1:42** | **86 → 70%** | **−16** | barra das 4 perguntas; push-in na nuvem; **câmera parada para crossfade (1:02,2–1:15,3)**; maquete do Pacífico | **b06 "Isso nos leva às seguintes perguntas…" (lista de 4) → b07 "Mas antes, é preciso entender uma coisa… começa a 10 mil km daqui" → b08 "Imagine o Pacífico como uma piscina"** | **pior trecho do vídeo**: cardápio + adiamento + aula abstrata; mudanças visuais caem de 30 para 10/min |
| 1:57–2:41 | 70 → 62% | −8 | diorama em corte, setas de Walker, gangorra | b09–b12: alísios, ar que sobe e desce | 2 min de mecanismo sem consequência |
| **2:41–5:43** | **62 → 59%** | **−3 em 3 min** | pescadores (sépia), Niño 3.4, foto do Peru, **régua de montanhas crescendo ao vivo**, véu coral, mostrador 70–83% | b13–b20: "é super?", "já passou 82 e 97", "**mas tem um detalhe que quase ninguém conta**", termômetro novo, "Pode virar? Pode." | **segura**: disputa de recorde, uma pergunta aberta, revelações em degraus |
| 5:43–6:05 | 59 → 56% | −3 | prancha "SUPER É APELIDO" | **b21 responde a pergunta do título** ("super é apelido… o termo técnico é muito forte"); b22 | a promessa do título fecha aos 42% do vídeo |
| 6:05–8:02 | 56 → 54,5% | −1,5 | UFs tingidas, Roraima antes × depois, brigadistas, Manaus | b23–b27: "o que muda na minha região?", Norte | segura bem |
| 8:02–8:24 | 54,5 → 52,5% | −2 | régua do rio Negro | b28 "Mas atenção, não é a seca de 2023 se repetindo" | ruído / nuance |
| **8:24–9:37** | **52,5 → 51,5%** | **−1** | Nordeste, reservatórios, Muçum, tornados, 1983 em sépia, Porto Alegre 2024 (5 fotos) | b29–b37: seca, "**vai faltar luz?**", Sul, 1983, 2024 | **segura**: consequência concreta + fotos de chão + pergunta do espectador |
| 9:37–10:06 | 51,5 → 48,5% | −3 | globo inteiro, coral branqueado | **b38 "O mundo" (sai do Brasil) + b39 "A última pergunta"** | desvio + anúncio de fim |
| 10:06–10:57 | 48,5 → 48,5% | 0 | barras por trimestre, La Niña | b40–b43 "até quando" | segura |
| 10:57–11:26 | 48,5 → 44,6% | −4 | **quadro de cortiça "O QUE FAZER" (o 3D sai)** | b44–b46 SMS 40199, PFF2, água | utilidade em lista = sinal de fim |
| 11:26–12:10 | 44,6 → 46,5% | +2 | continente ao entardecer, CTA | b47–b48 | quem fica até aqui fica até o fim (relativa 0,77) |

**Resumo:** o hook funciona (86% em 0:44). **Quem mata é a ponte de 0:44 a 2:41: −24 pts em 2 min, ~44% de toda a perda do vídeo; até 2:41 já se foram ~70% da perda.** Depois, a curva só cai ~1 pt/min, com degraus em três sinais de fecho: título respondido (5:43), "a última pergunta" (9:50) e cortiça (11:00).
**005 (Porto Alegre, 9:48):** 100 → 68% em 29 s e 52% em 59 s. Os primeiros 18 s são mapa + cilindro (a 1ª foto do alagamento entra aos 20 s), com 6 números em 30 s (266 mm, 3× o recorde, 5,35 m, 1941, 160 mil, 184 mortos) e a resposta antecipada aos 20 s ("a chuva mais pesada caiu na Serra; quem afundou foi Porto Alegre"). Mudanças visuais no hook: 26/min, ou seja, ritmo não faltou. **Hipótese:** faltou cena de chão e sobrou número para um público que viveu a enchente.

## 4. Melhorias para o nosso formato (em ordem de impacto)
| # | Melhoria | Por quê (número) | Como implementar | Evidência |
|---|---|---|---|---|
| 1 | **Cortar a ponte: nada de cardápio, nada de "mas antes".** Da pergunta do título vai-se direto à 1ª peça da resposta. As 4 perguntas ficam só na barra visual, sem leitura. | 0:44–1:42 = −16 pts (b06 lista + b07 "mas antes" + b08 "imagine"); relativa 0,39–0,57; Singularidade e El Mecanismo respondem "super?" em 1:05–1:30, nós em 4:52 | **roteiro:** proibir "isso nos leva às seguintes perguntas", "mas antes, é preciso entender", lista falada de capítulos; a 1ª resposta parcial com número tem de vir até 1:30; crivo de roteiro confere | dado nosso |
| 2 | **Loop adiado no hook:** a consequência mais estranha ou mais pessoal, prometida até 0:50 ("no fim eu mostro…") e paga no último minuto e meio | os 2 hits pt/es do tema usam isso (0:48 → 78–79%); nosso fim tem relativa 0,77, então quem chega ao fim gosta, e a promessa leva mais gente até lá | **roteiro:** campo `loop_adiado` no `roteiro.py` (frase de promessa + bloco do pagamento); A RESPOSTA paga o loop; o crivo confere promessa ↔ pagamento | Hipótese, com evidência forte de concorrente |
| 3 | **Câmera nunca parada nos 2 primeiros minutos;** troca A↔B no corte (whip/push), sem crossfade parado antes de 2:00 | mudanças visuais 30/min no hook → **10/min de 0:30 a 2:00**, justamente onde caem 16 pts; os 2 crossfades parados estão em 0:29,8–0:36,2 e 1:02,2–1:15,3 | **storyboard/Remotion:** em `estilo_v2.json`, trocas antes de 2:00 só `no corte`; regra na bíblia visual: "0:30–2:00 com algo novo a cada ≤ 3 s" | dado nosso (correlação) |
| 4 | **Mecanismo em ≤ 60–75 s, depois da 1ª revelação e amarrado a uma consequência** ("por isso Manaus fecha escolas") | diorama 1:57–2:41 = −8 pts; o bloco da disputa de recorde segurou 3 min a −1 pt/min | **roteiro:** bloco "o que é" com teto de ~150 palavras, depois do número-recorde; cada etapa do mecanismo cita um lugar do hook | dado nosso |
| 5 | **Não fechar o título antes de ~75%:** quando uma pergunta fecha, abre-se a próxima na mesma frase ("…isso ele já é. Mas o número que vai pesar no seu verão não é esse.") | b21 respondeu o título aos 42% → −3 pts em 22 s, o degrau mais íngreme fora da ponte | **roteiro:** mapa de loops no `ROTEIRO.md` (abre/fecha por bloco); o veredito final do título vai para A RESPOSTA | dado nosso (fraco: n pequeno) |
| 6 | **Cena de chão real no hook:** ≥ 2 imagens de chão com pessoas/consequência nos primeiros 15 s (foto ou vídeo real), o satélite vem depois | 002: hook só com satélite e número; 005: 1ª foto aos 20 s e −32% em 29 s; Last Day e RLL abrem com o vídeo real do evento; pessoas na tela: 002 ~3%, Last Day ~40% | **storyboard:** slot obrigatório `hook_chao` (Agência Brasil CC BY, Commons, governos; vídeo curto de NASA/NOAA/Defesa Civil se a licença for clara); **Remotion:** foto grande 1240 px já existe | Hipótese |
| 7 | **Consequência para o espectador ("você") no hook e em cada capítulo** (bolso, casa, cidade, conta de luz, alerta) | trechos que seguraram = consequência concreta (8:24–9:37 −1 pt; "vai faltar luz?"); "você" por minuto: 002 0,3; Singularidade 1,2; Sou curioso 1,3 ("preço do frango… conta de luz… dengue" aos 0:41) | **roteiro:** checklist "1 consequência pessoal até 0:30 e 1 por capítulo" | dado nosso + concorrentes |
| 8 | **Não anunciar o fim:** sem "a última pergunta", sem desvio para "o mundo" no fim, e o "o que fazer" vira 1 frase dentro de cada região (ou ≤ 15 s com o 3D vivo) | b38/b39 −3 pts em 30 s; cortiça −4 pts em 30 s | **roteiro + storyboard:** a cortiça sai do fim (ou dura ≤ 15 s sobre o mapa); o "mundo" entra antes do bloco do Brasil ou sai | dado nosso (fraco) |
| 9 | **CTA de inscrição no meio, como ponte** (~30–35%, logo antes do bloco "sua região"): "se você gosta de entender clima com dados e não com medo, se inscreve, porque agora o mapa chega na sua região" | Singularidade 3:48, El Mecanismo 0:54; o nosso só vem aos 11:59, quando restam 46% | **roteiro:** bloco fixo `cta_ponte`; **Remotion:** botão "inscrever" de 2 s sobre o mapa | Hipótese (efeito em inscritos, não na retenção) |
| 10 | **Imagem real a cada ≤ 60–90 s, com vídeo real curto quando houver licença** | 002: 0% de vídeo real, fotos de chão 12%, intervalos de 107 s (0:28–2:15) e 184 s (3:16–6:20); mas o trecho de 184 s segurou por causa da história | **storyboard:** checagem automática de "maior intervalo sem imagem real"; GOES/NASA SVS (domínio público) como vídeo real de clima | Hipótese (média) |
| 11 | **Respiro sonoro antes da revelação:** 0,5–1 s sem trilha antes do número-chave | 002: 0,16 pausa/min e trilha sempre ligada; UnderTheHeadline 4,7 pausas/min | **áudio:** `mix_audio.py` com "duck a zero" nos cues marcados `revela` | Hipótese (baixa) |

Não mexer: o hook com 3 lugares, data e número (0:44 com 86%), a disputa de recorde em 3D (segurou 3 min), as fotos de chão nas regiões e o fecho que volta ao hook (relativa 0,77).

## 5. Esqueleto de retenção (10–13 min) para a bíblia
| Tempo | O que acontece | Visual dominante | Loops / CTA |
|---|---|---|---|
| 0:00–0:15 | Lugar + data + cena física com pessoas ("Manaus, 9 de outubro: escolas fechadas pela fumaça") + o número que choca | **foto/vídeo real de chão** → mapa A com pino | — |
| 0:15–0:35 | 2º e 3º lugares (contraste) + "mesmo nome" + **consequência para você** | mapa A em movimento contínuo, contador | abre a pergunta do título |
| 0:35–0:50 | pergunta do título + **loop adiado** ("e no fim eu mostro por que…") | troca A→B **no corte**, barra de capítulos **sem narração** | loop adiado aberto |
| 0:50–1:30 | **1ª peça da resposta** com número forte (o recorde, já) | dado em 3D (relevo de calor, régua) | "mas tem um detalhe…" (loop curto) |
| 1:30–2:45 | mecanismo em ≤ 75 s, cada passo amarrado a um lugar do hook | diorama/globo com câmera em movimento; 1 foto real | fecha o loop curto, abre "então ele é o maior?" |
| 2:45–4:30 | disputa/revelação em degraus (recordes, termômetro novo, probabilidade) | régua 3D crescendo ao vivo + 1–2 fotos | "pode virar? pode…" (não fechar) |
| ~4:00 | **CTA ponte** (1 frase + botão de 2 s) | sobre o mapa | "agora o mapa chega na sua região" |
| 4:30–9:00 | região por região: cada uma com consequência concreta + foto de chão + 1 pergunta do espectador ("vai faltar luz?"); o "o que fazer" de cada região em 1 frase | B com tintas e pinos, troca A↔B a cada ~20 s, foto de chão a cada ≤ 60–90 s | cada região fecha uma pergunta e abre a próxima |
| 9:00–10:30 | o tempo (até quando / histórico: 1983, 2024) | arquivo sépia, satélite, barras | sem "última pergunta" |
| 10:30–11:30 | **A RESPOSTA:** veredito do título + **pagamento do loop adiado** | volta ao mapa A do hook, 3 pinos | fecha tudo |
| 11:30–12:10 | "manda para quem mora em…" + inscrição | continente ao entardecer | CTA final curto |

## 6. Frames
`frames/`: `<vídeo>-grade1..3.jpg` (1 quadro a cada 10–15 s, com o tempo no canto) e `<vídeo>-hook30s.jpg` (1 quadro a cada 2 s nos primeiros 30 s) de 002, 005, The Last Day, RealLifeLore, UnderTheHeadline, El Mecanismo, Singularidade, Sou curioso?! e Cosmos Brutal. Comparação mais útil: `002-em-relevo-hook30s.jpg` × `en-thelastday-hook30s.jpg` (satélite e número × vídeo de chão).
