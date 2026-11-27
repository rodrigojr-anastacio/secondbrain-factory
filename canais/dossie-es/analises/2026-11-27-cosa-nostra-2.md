# Dossier en Minutos: "Cosa Nostra 2", histórias que o 004 só tocou (27/11/2026)

**Só proposta**: backlog, bíblia e vídeos não foram mexidos. Custo pago: US$ 0 (Data API readonly, ~4.000 unidades; yt-dlp via WARP).
**Pedido do Rodrigo:** "Ainda tem conteúdo para outra história não contada da Cosa Nostra? Uma história específica que não abordamos no primeiro vídeo."
**Complementa** `2026-11-27-bolha-opcoes.md` (job irmão), que já cobriu a Cosa Nostra **americana** (Cinco Familias, Murder Inc., Outfit, Cuba/Lansky) e descartou Luciano, Lansky e Maxiproceso/Falcone. Aqui o foco é a **Sicília**.
**Fontes:** `videos/004-cosa-nostra/SCRIPT.md` e `entrega/legendas.srt` (tempo de tela por capítulo); `youtube.analytics_trafego_detalhe` (leitura de 25/11); Data API `search.list` (12 meses e todo o período, `relevanceLanguage=es`, ≥ 5 min) + `videos.list` para datas; yt-dlp `ytsearch20` via WARP (14 buscas); catálogos dos vizinhos (`2026-11-27-bolha-dados/catalogos.json`) + catálogo completo do canal **Historia de la Mafia** (es, 53 vídeos, faz exatamente "deep dives" da Cosa Nostra desde 2026). Os brutos ficaram fora do git (`~/cache/tmp/cosa2/`), como pede o brief.
**Ressalva de demanda:** Biographics (Mori) e The History Guy (Petrosino) são canais em inglês com título dublado em es: as views são globais, não prova de público em es.

## 1. Resposta curta
**Sim, há pelo menos 2 histórias sicilianas com material para 13 expedientes que o 004 não contou:** (1) **Provenzano e os corleoneses**, o chefe que ninguém viu por 43 anos (o 004 nunca diz o nome dele) e (2) **Calvi, Sindona e o Banco do Vaticano**, a mafia siciliana dentro das finanças da Igreja (0 s no 004). Uma 3ª, **Messina Denaro e os atentados de 1993**, é boa, mas tem pouco documentário longo em es e encosta no fim da 1ª.

## 2. O que o 004 já contou (tempo de tela, de `legendas.srt`; total 14:30)
| capítulo do 004 | início | tela |
|---|---|---|
| Hook (Buscetta e a estampa) | 0:00 | 32 s |
| 1 El Nombre (origem, Sangiorgi) | 0:32 | 65 s |
| 2 El Detective (Petrosino) | 1:37 | 64 s |
| 3 El Prefecto (Mori) | 2:41 | 55 s |
| 4 El Restaurante (Masseria, Luciano, Comisión) | 3:35 | 71 s |
| 5 El Puerto (Normandie, Husky, Don Calò) | 4:47 | 60 s |
| 6 El Hotel (Havana) | 5:47 | 76 s |
| 7 Las Reuniones (Hotel des Palmes, Apalachin) | 7:03 | 48 s |
| 8 El Cemento (saque de Palermo, Ciaculli) | 7:52 | 60 s |
| 9 La Guerra (corleoneses, Bontade, Dalla Chiesa) | 8:51 | 62 s |
| 10 El Arrepentido (Buscetta) | 9:53 | 57 s |
| 11 La Pizzería (Pizza Connection) | 10:50 | 50 s |
| 12 El Búnker (Maxiproceso) | 11:40 | 53 s |
| 13 La Autopista (Capaci, D'Amelio) | 12:33 | 60 s |
| Cierre (prisão do Riina; Messina Denaro em 1 frase) | 13:33 | 57 s |

**Nunca citados:** Bernardo Provenzano, Michele Navarra, Luciano Liggio, Salvatore Giuliano/Portella della Ginestra, Sindona/Calvi/Banco Ambrosiano, Peppino Impastato, os atentados de 1993 (Florença, Roma, Milão), a "trattativa" Estado-máfia, o menino Di Matteo.

## 3. Histórias candidatas (do 004 e de fora)
Demanda = vídeos documentais/históricos sobre o tema (views · canal · data; × = múltiplo da mediana do canal quando conhecida).

| # | história | no 004 | o que haveria de novo | demanda real | manada | título candidato | thumb (texto) | risco |
|---|---|---|---|---|---|---|---|---|
| 1 | **Provenzano e os corleoneses** ("o fantasma de Corleone") | 0 s com o nome; contexto em La Guerra (62 s) + prisão do Riina (~25 s) ≈ **10% do 004** | Corleone 1948–58 (Navarra, o médico-chefe; Liggio; o sindicalista Placido Rizzotto); "Binnu u tratturi"; 43 anos foragido; os **pizzini** datilografados; a suspeita de que entregou o Riina em 1993; a prisão em 11/04/2006 num casebre de pastor a 2 km de Corleone (ricota, chicória, máquina de escrever); os herdeiros até Messina Denaro | Cruzada Hostil "BERNARDO PROVENZANO: Nadie conoció su rostro durante 43 años" **144 mil** (01/2024, 2,2×); Historia de la Mafia "Sin teléfono y escondido durante 43 años: así cayó Provenzano" **27 mil** (18/11/2026, ~5×); World View "Corleone: el Padrino más Poderoso…" **650 mil** (11/2025); Historia de la Mafia "Segunda Guerra de Palermo" **131 mil** (10/2026, ~25×); Relato Mafioso Riina 76 mil (12/2025, 2,6×); Pioneros "Cómo RIINA y PROVENZANO ganaron…" 25 mil (01/2026, ~12×) | manada = **o homem dos 43 anos e a prisão de 2006** (todos abrem nisso); quase ninguém em es conta os pizzini como sistema de governo nem o Corleone de 1948–58 | **"PROVENZANO: el jefe de la mafia siciliana que nadie vio en 43 años"** (alt.: "CORLEONE: el pueblo real de la mafia siciliana") | objeto: Olivetti com um pizzino dobrado sobre mesa de casebre, colinas de Corleone pela janela; "PROVENZANO" + sello "43 AÑOS" | baixo de repeteco; médio de manada (o "43 anos" é de todo mundo: o hook precisa ser outra cena física, ex.: a sacola de roupa limpa que a polícia seguiu até o casebre) |
| 2 | **Calvi, Sindona e o Banco do Vaticano** | **0 s** | Sindona lava o dinheiro da heroína (Gambino/Inzerillo), compra um banco em Nova York, finge o próprio sequestro (1979) e morre com café envenenado na prisão (1986); Calvi, o "banquero de Dios", o IOR e a loja P2; 18/06/1982, enforcado sob a Blackfriars Bridge com tijolos nos bolsos; o processo de 2007 contra Pippo Calò (absolvido) | Lord Draugr "El Banco Ambrosiano y la Logia Masónica que Controlaba Italia" **909 mil** (12/2023); Mil Millones "El Banco de Dios" **144 mil** (10/2026); Secretos Históricos "Banco Vaticano: Mafia…" 99 mil (09/2025); El Historiador Nocturno 56 mil (03/2026); em canal de máfia, Historia de la Mafia "La sangrienta caída del banquero de Dios" 5,4 mil (11/2026, ~1×) | manada = **Vaticano/maçonaria**, com a máfia como figurante; ninguém em es conta pelo lado da **Cosa Nostra** (de onde vinha o dinheiro e quem cobrou a dívida) | **"El banquero de la mafia siciliana que apareció colgado en Londres"** (alt.: "La mafia siciliana, el Vaticano y el banquero de Dios") | ponte de Londres ao amanhecer, maleta aberta com tijolos e notas, sem corpo; "BANCO DE DIOS" + sello "¿SUICIDIO?" | médio: a máfia é coprotagonista; a autoria da morte do Calvi **não foi provada** (tudo com "según la fiscalía"); tema financeiro precisa de objetos concretos em cada expediente |
| 3 | **Messina Denaro e os atentados de 1993** ("o último padrinho") | **1 frase (~6 s)** no cierre | Depois de Capaci, a máfia ataca o **patrimônio**: bombas na Via dei Georgofili (Uffizi, Florença), em Milão e nas igrejas de Roma (1993); o sequestro do menino Di Matteo (só citado, sem detalhe); 30 anos foragido; 16/01/2023, preso numa clínica de Palermo como "Andrea Bonafede" durante a quimioterapia; morre em 09/2023 | The Wild Project "LA CAÍDA DEL CAPO… MESSINA DENARO" 189 mil (02/2023, clipe de 7 min); El Comercio 129 mil (notícia); CHV 31 mil (05/2026). **Documentário longo em es: quase nenhum.** Em italiano: Rai 3 1,08 mi, Mappe Criminali 590 mil | manada = **notícia da prisão**; o fio 1993 → 2023 quase não existe em es | **"MESSINA DENARO: el último jefe de la mafia siciliana, 30 años escondido"** | porta de clínica com o gorro de lã e os óculos escuros dele, carabinieri; "EL ÚLTIMO PADRINO" + sello "2023" | médio: história recente (cheira a notícia, não a arquivo); o Di Matteo é sensível para a política; se fizer o nº 1, os dois se encostam em 1993–2006 |
| 4 | Mussolini contra a máfia (Cesare Mori) | El Prefecto, **55 s** (Gangi já mostrado) | 1924: Mussolini em Piana dei Greci humilhado pelo prefeito-mafioso Cuccia; os poderes de Mori; o processo de 1927–28; por que a "vitória" virou mentira; a ponte com 1943 | Biographics 163 mil (02/2022, **canal en dublado**); Leander Auditore "¿Cómo Italia (Mussolini) destruyó a la Mafia en 5 años?" 70 mil (08/2023, 7 min); o resto ≤ 1 mil | quase não há manada em es | "Cuando Mussolini le declaró la guerra a la mafia siciliana" | camisa negra e a coppola lado a lado, cerco a Gangi; "MUSSOLINI vs MAFIA" | médio: o 004 já gastou o melhor (Gangi); demanda em es fraca; liga com a bolha fascismo (SS/Gestapo), o que é bom |
| 5 | Petrosino e a Mano Negra | El Detective, **64 s** (com o clímax) | o "crime do barril" de 1903 (Morello), a Italian Squad, a traição do jornal, o álibi de Cascio Ferro | The History Guy 349 mil (2018, **canal en dublado**); lahistoriaentera 35 mil (11/2026); Cascio Ferro 16 mil (2024) | pouca em es | "El policía que la mafia siciliana mató en Palermo" | barril no cais de NY, lampião da Piazza Marina; sello "1909" | alto: o 004 já contou o fim; é mais Nova York do que Sicília |
| 6 | Sicília 1943: Luciano, Don Calò e o desembarque | El Puerto, **~45 s** | a Operação Husky pelo lado da máfia; o mito do lenço amarelo; os prefeitos mafiosos da AMGOT | Husky genérico 1,03 mi (Real Time History); com o ângulo da máfia: 60 mil (clipe de jogo), 16 mil, 11 mil | — | "¿La mafia siciliana ayudó a invadir Sicilia en 1943?" | — | alto: repeteco + história contestada; o irmão já descartou Luciano |
| 7 | Salvatore Giuliano e Portella della Ginestra (1947) | **0 s** | o bandido-separatista, o massacre do 1º de maio, o café envenenado do primo Pisciotta | em es ≤ 21 mil (Sitdownnews, dublado); em italiano 2,2 mi (filme) | — | "El bandido que la mafia siciliana usó y luego traicionó" | — | demanda fraca em es; Giuliano não é Cosa Nostra (é bandido usado por ela) |
| 8 | Buscetta, "o chefe dos dois mundos" | hook + El Arrepentido + Búnker ≈ **1:50** | a vida no Brasil, as plásticas, a tortura de 1972 | Free Documentary "La Cosa Nostra Ep. 2" 105 mil (06/2026); o resto é italiano | — | — | — | **alto**: é o fio do 004 inteiro |
| 9 | Falcone, Borsellino e o Maxiproceso | Búnker + Autopista ≈ **1:53** | a agenda vermelha, a "trattativa" | **máx. 3,4 mil em es em 12 meses** (Historia de la Mafia: 3,3 mil e 1,8 mil) | — | — | — | descartar (repeteco e demanda) |
| 10 | Hotel des Palmes / Pizza Connection | Reuniones + Pizzería ≈ **1:38** | a rota da heroína Sicília → Nova York | Historia de la Mafia "Pizza Connection" 13 mil (11/2026, ~2,5×) | — | — | — | médio-alto de repeteco; fraco sozinho |
| — | Cosa Nostra americana | — | coberta pelo job irmão (Cinco Familias, 3º da recomendação dele) | — | — | — | — | não repetir aqui |

## 4. Um 2º vídeo da mesma máfia seria sugerido ao lado do 004?
**Provavelmente sim, mas a vizinhança do 004 não é "máfia".** (Hipótese, com estes dados.)

**Nossos dados (leitura de 25/11):**
- O 004 vive de sugeridos e navegação: RELATED_VIDEO 9.029, navegação/inscritos 4.691 e **busca 39** views na série da Analytics API. Ninguém chega a ele pesquisando "cosa nostra". Ou seja, a demanda de busca do tema pesa menos que a semelhança com o 004.
- Quem **manda** público para o 004: KGB (1.973), SS (993), Gestapo e Mossad do Archivo en Minutos, Guerra Fría LatAm. **Nenhum vídeo de máfia.**
- Para onde o público do 004 **vai** (nossos vídeos que recebem sugerido dele): KGB 1.635, SS 651, Gestapo 259, Inquisición 258, FBI 201; Medellín (a única "máfia") só **12**.
- Leitura: o YouTube vê o 004 como "história de organização temida do séc. XX". Um 2º vídeo **com "mafia siciliana"/"Cosa Nostra" no título, do mesmo canal, no mesmo formato** tende a ser testado na página do 004 (é o vizinho mais parecido que existe). Mas o Medellín mostra que só "máfia" não basta: o 2º vídeo precisa parecer **arquivo histórico** (objetos, datas, Estado), não true crime de capo nem notícia.

**Evidência nos canais do nicho (sequências e deep dives):**
| caso | resultado | leitura |
|---|---|---|
| Vida de un Gángster "El Mafioso que inspiró a Vito Corleone" Parte 1 → Parte 2 | 506 mil → **80 mil** (0,16×) | "Parte 2" do mesmo assunto perde ~85% |
| Pioneros "10 finales brutales de capos" → "PARTE 2" | 74 mil → 45 mil (0,6×) | continuação declarada perde, mas menos |
| lahistoriaentera "Historia de la Mafia" ep. 02 → ep. 03 | 35 mil → 11 mil | série numerada decai |
| **Historia de la Mafia** (es, mediana ~5 mil, só Cosa Nostra) | Segunda Guerra de Palermo **131 mil**; Provenzano **27 mil**; 1ª guerra/Ciaculli 16 mil; Pizza Connection 13 mil; Calvi 5,4 mil; Falcone 3,3 e 1,8 mil | deep dive **de episódio siciliano com personagem forte** funciona como vídeo independente; Falcone não |
| Cruzada Hostil (mediana 64 mil) | panorama "Sangrienta historia de la Cosa Nostra" 261 mil; Provenzano 144 mil; corleoneses 61 mil | o 2º vídeo da mesma máfia rendeu acima da mediana quando era **um personagem/caso**, não outro panorama |
| Relato Mafioso (mediana 30 mil) | "Así nació la mafia siciliana" 150 mil; Riina 76 mil | idem: panorama primeiro, caso depois, os dois acima da mediana |

**Regras que saem disso:** (1) nunca "Parte 2", "Cosa Nostra 2" nem "lo que no te contamos" no título; o 2º vídeo tem de se vender sozinho a quem nunca viu o 004; (2) nome do caso no começo + "mafia siciliana" no aposto, para o algoritmo ligar ao 004 e o espectador entender em 1 s; (3) personagem/caso com objeto concreto, não outro panorama; (4) no lançamento, **trocar a tela final do 004** (hoje aponta para CIA/FBI) para o vídeo novo e fazer o cierre do novo apontar para o 004. É o melhor jeito de levar parte dos 25 mil espectadores do 004 até ele (tela final é editável depois de publicar; decisão do Rodrigo).

## 5. Recomendação (ranqueada)
| ordem | história | por quê | cuidado |
|---|---|---|---|
| **1** | **Provenzano e os corleoneses** | maior demanda sustentada entre os temas sicilianos (144 mil, 131 mil, 650 mil para Corleone) e acima da mediana nos **4** canais que fizeram; o 004 não diz o nome dele (repetição ~10%, só como contexto); expedientes cheios de objeto (pizzini, Olivetti, ricota, casebre, carteira falsa); é a continuação natural do cierre do 004 ("el hombre que llevaba 24 años escondido") sem ser "Parte 2" | começar em Corleone 1948, não em 1981; a guerra de 1981–83 e a prisão do Riina em no máximo 1 expediente cada; hook com cena física que não seja o "43 anos" da manada |
| **2** | **Calvi, Sindona e o Banco do Vaticano** | **0 s no 004**, demanda grande em es (909 mil, 144 mil, 99 mil) e encosta em **dois** vizinhos nossos que já recebem tráfego da bolha: Masones (P2) e Inquisición (Igreja, 258 views vindas do 004). Liga máfia ↔ instituição, que é o que a bolha premia (`bolha-opcoes.md` §1) | título com "mafia siciliana" para não cair na bolha "Vaticano/conspiração"; morte do Calvi sempre "según la fiscalía"; sem corpo na thumb |
| 3 (reserva) | **Messina Denaro e 1993** | fecha a linha do tempo (1993 → 2023) e é a promessa literal do cierre do 004 ("su último gran prófugo") | pouca prova de demanda longa em es; se o nº 1 sair, espere ver se ele passa no teste do sugerido (≥ 2%) antes de fazer o 3º; Di Matteo só citado |

- **Não recomendo:** Buscetta, Falcone/Maxiproceso, Pizza Connection, Hotel des Palmes e Sicília 1943 (repetição alta no 004 e/ou demanda < 15 mil em es); Petrosino e Mori só como expediente dentro de outro vídeo.
- **Ordem com o plano do irmão:** o título proposto para a 'Ndrangheta (28/11) já cita a Cosa Nostra. Para não lançar 3 máfias italianas seguidas, encaixar o **Provenzano depois da Mafia rusa** e com ~48 h entre os lançamentos (diagnóstico de 27/11, ajuste 6). Se o Rodrigo quiser só **um** 2º vídeo da Cosa Nostra agora: Provenzano.
- **Como medir:** CTR no sugerido nas primeiras 48 h ≥ 2,5% e participação do 004 nas fontes de sugerido do novo (meta: o 004 entre as 3 primeiras fontes em 7 dias). Se o 004 não aparecer como fonte, a hipótese "mesma máfia = mesma vizinhança" cai.
