# Nicho C: consumo/produtos perigosos e "a verdade sobre o que você compra" (28/11/2026)

Duas fórmulas diferentes no mesmo nicho:
- **C1 "Deadliest/Most Dangerous X Ever Sold"**: histórico de recalls, proibições e acidentes por categoria (doces, snacks, brinquedos). É evergreen e global.
- **C2 "Marcas do país X" ("STOP buying these 10 milk brands (only 5 are real milk)", "Former <rede> employees warn…")**: ranking de marcas reais de supermercado de um país.

Dados observados vêm de yt-dlp + WARP (busca), Data API (~60 unidades usadas) e thumbs no i.ytimg. **Limite:** o `watch.py` falhou nos 3 vídeos (o IP do WARP caiu em "Sign in to confirm you're not a bot", LOGIN_REQUIRED, testado com 4 player clients). Por isso não há hook transcrito nem frames. O formato abaixo sai de títulos, descrições, capítulos e thumbs. O mosaico das thumbs está em `~/cache/oport/C/mosaico.jpg` (fora do repo).

---

## 1. Canais da regra de ouro (1º vídeo ≥ 28/07/2026, até ~20 vídeos)

### C1: Deadliest X Ever Sold
| Canal | Idioma | 1º vídeo | Vídeos | Views | Inscr. | Views/mês | Mediana | Melhor vídeo | Duração | Cadência |
|---|---|---|---|---|---|---|---|---|---|---|
| [Steve Talks Food](https://www.youtube.com/channel/UCQUd_Lz--kVbKefuk7dsKMA) | en (US) | 21/10 | 9 | 12,29 mi | 21,9 mil | 9,87 mi | **606 mil** | [The Deadliest Candy Ever Sold](https://youtu.be/3Ika6QR1TPE): 6,02 mi | 17 min | ~2/semana |
| [ToyAutopsy](https://www.youtube.com/channel/UCHdyAlYLqscSgXyR9Rf4e7Q) | en | 08/11 | 10 | 1,36 mi | 2,1 mil | 2,61 mi | 61 mil | [Deadliest Squishy and Fidget Toys Ever Sold](https://youtu.be/PZxGZWeoNXE): 1,05 mi | 23 min | ~3/semana |
| [Jose Velasquez](https://www.youtube.com/channel/UC11Hnbj2ETTvWo1rbNk95BA) | es (CO) | 19/10 | 4 | 791 mil | 1,8 mil | 610 mil | 204 mil | [Ranking de Los Snacks más LETALES de la Historia](https://youtu.be/UllcjuqeCTQ): 404 mil | 11 min | irregular |

Contexto (não conta como sinal, é a demanda/originador):
- **[Crunchy History](https://www.youtube.com/channel/UCnNkV9ZvjGaPfk_QnfR8fDA)** (JP, desde 02/2025, 178 vídeos, 32,6 mi views, 97 mil inscritos) é o **originador** da fórmula: [The Most Dangerous Candy Ever Made](https://youtu.be/Q5lp2HzPb0s) (751 mil), Snacks (769 mil), Halloween Candy (796 mil), Fast Food (668 mil), Energy Drinks (550 mil). Os títulos aparecem traduzidos em es/fr na busca, ou seja, ele **já tem faixa de áudio dublada**.
- Os títulos do Steve Talks Food copiam os do Crunchy um a um (Candy, Snacks, Fast Food, Halloween Candy, Energy Drinks) e mesmo assim fizeram 12 mi em 38 dias.
- Clones novos em es estão no zero: [Numero de Lote](https://www.youtube.com/channel/UCc-uALLlMbBKbf-lKtN5Tag) (4 vídeos, 316 views) e [Lote Mortal](https://www.youtube.com/channel/UCZbQjMvqOALcgipNZ1sv1qg) (49 vídeos, 50 mil views).

**Saturação C1:** en tem 2 novos com tração, mais o originador e alguns pequenos. es tem 1 novo com tração e 2 clones mortos. pt, fr e de não têm nenhum canal novo com tração.

### C2: Marcas do país X (só a amostra de nov/2026: 22 dos 25 candidatos passam na regra)
| Canal | Idioma/país-alvo | País do dono | 1º vídeo | Vídeos | Views | Inscr. | Mediana | Melhor vídeo |
|---|---|---|---|---|---|---|---|---|
| [Kassen Shock](https://www.youtube.com/channel/UCkIXQzbcrXNGu2Vjb8My07Q) | de/DE | BA | 15/10 | 19 | 3,36 mi | 6,1 mil | 160 mil | [Ehemalige EDEKA-Mitarbeiter WARNEN…](https://youtu.be/pnJ2Ynxc4Vk) 510 mil |
| [Alerta Chile](https://www.youtube.com/channel/UCpVTgE0QupcGAY1TNJc7mtQ) | es/CL | **BR** | 12/11 | 8 | 2,83 mi | 11,8 mil | 233 mil | [7 Aguas Embotelladas Que SOLO la GENTE TONTA Compra en CHILE](https://youtu.be/ZIZYGGB7eiA) 916 mil |
| [Worth the Bite?](https://www.youtube.com/channel/UCFlfnfJbi8TJPpHJ9GREPFg) | en/ZA | **BR** | 28/10 | 17 | 2,64 mi | 12 mil | 44 mil | 8 Canned Sardine Brands… South Africa: 981 mil |
| [FoodFacts South Africa](https://www.youtube.com/channel/UCmyrCp5XxLTL-_m0bbeNVew) | en/ZA | **BR** | 05/11 | 14 | 1,81 mi | 10,4 mil | 11 mil | 6 Coffee Brands to AVOID in SA: 1,2 mi |
| [Changuito Inteligente](https://www.youtube.com/channel/UC7iWa20lG-ifRVrYcfhaA6g) | es/AR | AR | 08/11 | 8 | 1,59 mi | 6,9 mil | 145 mil | [EVITA Estas 7 Marcas de CERVEZA en Argentina](https://youtu.be/EAXWidHOMB8) 746 mil |
| [México súper](https://www.youtube.com/channel/UCARI7sr757xaThUWYvW5rlw) | es/MX | **BR** | 19/11 | 10 | 1,52 mi | 1,8 mil | 2,4 mil | 20 alimentos… Bodega Aurrera: 1,46 mi |
| [Kiwi Products Uncovered](https://www.youtube.com/channel/UCFpu3-gzPKDR6sAIzAJ165A) | en/NZ | NZ | 08/11 | 12 | 1,39 mi | 10,8 mil | 85 mil | [STOP Buying These 10 NZ MILK BRANDS](https://youtu.be/UfK3YCOpcuU) 325 mil |
| [South Africa Products](https://www.youtube.com/channel/UCU8quHfqvnFpI5D1XOA3ZYQ) | en/ZA | **BR** | 08/11 | 15 | 1,02 mi | 3,9 mil | 30 mil | [Former Pick n Pay Employees…](https://youtu.be/18ZmqmJ7OCI) 389 mil |
| [UK Food Facts](https://www.youtube.com/channel/UCrs8ihKGMLO-xAq9-_SIUrQ) | en/GB | GB | 06/11 | 7 | 946 mil | 4 mil | 44 mil | We Investigated 8 UK Jams: 508 mil |
| [Singapore Products](https://www.youtube.com/channel/UChYG7Gx3H5lsv552OUotaog) | en/SG | **BR** | 08/11 | 14 | 837 mil | 2,6 mil | 11 mil | 9 Coffee Brands in Singapore: 267 mil |
| [Food Uncovered PH](https://www.youtube.com/channel/UCypWr8STanzWs9Yk50CeyDg) | en+es/PH | **BR** | 11/11 | 14 | 821 mil | 1,6 mil | 2,9 mil | STOP Buying These 10 MILK BRANDS in the Philippines: 567 mil |
| Mais 8 iguais | ZA, IE, MY, SG, GB | quase todos **BR** | 04–24/11 | 3–15 | 0,2–0,65 mi | | | Best & Worst SA, Worth the Rand?, Read the Label SA, Ireland Products, Malaysia Brands (handle `@visiondelmundotv`, canal reaproveitado), Singapore Food Exposed, Shop Audit UK, Canada Food 2050 |

Os canais maiores e mais antigos da mesma fórmula já estão em **pt-BR**: [Leia o Rótulo](https://www.youtube.com/channel/UCDSyquS9jTE9zJaHg8A7rEQ) (desde 11/07, 69 vídeos, 9,0 mi; [Paçoca](https://youtu.be/qpfBPBR9KA0) 1,09 mi) e [Detetive do Prato](https://www.youtube.com/channel/UCSxC_FHx-VVxUX5FyuALTbQ) (desde 06/2026, 104 vídeos, 11,8 mi). Em de: [Lebensmittel-Wissen](https://www.youtube.com/channel/UC_ySAQwYbqtWCkP-7TGk-Fg) (06/2025, 124 vídeos; Butter 1,27 mi). Em fr: [L'Envers du Rayon](https://www.youtube.com/channel/UCG5vKXc9GBtBulvq188cfEQ) (18/10, 23 vídeos, 1,84 mi; Whiskys 493 mil).

**Saturação C2 (observado):** ≥ 25 canais abertos só em out–nov/2026, em todos os 5 idiomas. A maioria tem dono marcado como **Brasil**. Os títulos são idênticos com o país trocado (sardinha, manteiga, leite, café copiados entre ZA, SG, MY, PH e IE). Vários vídeos aparecem como colaboração "X and 2 more" entre canais da mesma rede. É uma **fazenda de canais**.

## 2. Formato observado

**C1 (Steve Talks Food / ToyAutopsy / Crunchy):**
- **Título:** "The Deadliest [categoria] Ever Sold", sem número e sem país.
- **Thumb:** fundo escuro, 3 produtos reais renderizados no centro, **uma palavra minúscula com ponto final** em cima ("poison.", "banned.", "burned.") e rótulos flutuando ("toxic?", "choking hazard", "illegal"). **ToyAutopsy e Steve Talks Food usam o mesmo molde de thumb**, o que é forte indício de mesmo dono ou mesma agência (Hipótese: o visual é observado, a ligação não). O Crunchy usa outro molde: grade de produtos em fundo branco, com legenda curta em cada um ("ARSENIC POISON", "RADIOACTIVE CHOCOLATE").
- **Hook** (proxy pela descrição, porque a transcrição foi bloqueada): *"From fake Sour Patch Kids that got toddlers high, to a candy that burned a hole through a boy's tongue… this is the deadliest candy ever sold."* No ToyAutopsy: *"Would you squeeze a cube that can go past 200 degrees? Kids found out you can put one in the microwave, and burn centers are seeing them now."*
- **Estrutura:** contagem de 8–10 produtos, ~1,5 min cada, nos capítulos (Gobstopper → Black Licorice → Warheads → Stoney Patch → Bradford Humbugs → … → Konjac Jelly Cups). Duração de 14–27 min.
- **Produção:**
  - ToyAutopsy declara usar **clipes de telejornal** (CBS, NBC, WGN, Consumer Reports…) "for commentary", ou seja, fair use de notícia mais narração.
  - Steve Talks Food: capítulos e thumbs indicam imagem de produto mais narração (Hipótese: não deu para ver os frames).
  - Não há sinal de rosto. Não dá para afirmar se a voz é sintética.

**C2 (rede de países):**
- **Título:** "STOP Buying These 10 [país] MILK BRANDS (Only 5 Are ACTUALLY Real Milk)" ou "Former [rede] Employees WARN You Not to Buy These 12 Items".
- **Thumb:** falso telejornal ("BREAKING NEWS / THIS IS SHOCKING!", "EILMELDUNG / DAS IST SCHOCKIEREND!", "ESCÁNDALO DEL AGUA"), com **"ex-funcionária" gerada por IA** e logo real da rede (Pick n Pay, EDEKA) ou fábrica de IA com embalagem real da marca. O molde é idêntico em ZA, NZ e DE (observado no mosaico).
- **Descrição:** "I investigated every major milk brand…, who actually owns them…". A estrutura é contagem regressiva das "ruins" e depois das "reais". 15–30 min.

## 3. Mesma fórmula por idioma (buscas reais, nov/2026)
| Idioma | C1 Deadliest X | C2 Marcas do país |
|---|---|---|
| en | Ocupado, mas cresce: originador mais 2 novos (6,0 mi, 2,85 mi, 1,39 mi, 1,05 mi neste ano) | **Saturado** (≥ 18 canais novos, rede BR) |
| es | **Meio aberto:** Jose Velasquez 404 mil com 4 vídeos; DeiK (canal grande) [Las 10 Golosinas Más Peligrosas](https://youtu.be/awI79r3KyUM) 627 mil; clones nativos com ~300 views. A dublagem do Crunchy aparece no topo | Saturado (CL, AR, MX, CO, PH; "Detetive do Prato" fazendo es) |
| pt | **Vazio:** "os doces mais perigosos já vendidos" tem topo de 978 views; o resto é React/teste com crianças | **Saturado** (Leia o Rótulo, Detetive do Prato, Raio-X do Consumo, Consumidor Exposto, Portugal Sem Embalagem…) |
| fr | Coberto pela dublagem do Crunchy (751–796 mil no topo); nada nativo | L'Envers du Rayon mais clones de marcas canadenses |
| de | Vazio (topo de 16 mil, react) | Saturado (Kassen Shock, Lebensmittel-Wissen, PreisRadar, Lebensmittel Enthüllt…) |

## 4. RPM e receita (estimativa)
- **Comida/consumo, ref. EUA:** RPM de US$ 1,50–4 ([1of10](https://www.1of10.com/blog/youtube-cpm-rpm-by-niche/)); mediana de US$ 2,25 (IQR 1,50–3,11, amostra pequena) em 300 canais ([AIR 2026](https://air.io/en/air-data-findings/how-much-does-youtube-really-pay-in-2026-real-rpm-data-from-300-channels)); faixa otimista de US$ 6–12 para público dos EUA ([Fluxnote](https://fluxnote.io/guides/youtube-rpm-by-niche-usa-2026)). O país do público pesa mais que o idioma ([Dynamoi](https://dynamoi.com/data/youtube-adsense-rpm.html), [Wild & Free Tools](https://www.wildandfreetools.com/blog/youtube-rpm-by-country/)).
- **en (EUA/UK/AU):** US$ 2–5. **es LatAm:** US$ 0,4–1,2. **pt-BR:** US$ 0,5–1,2. **de:** US$ 3–6. **fr:** US$ 1,5–3 (Hipótese derivada das fontes acima).
- **C2 mira países de RPM baixo** (ZA, PH, MY, MX): ~US$ 0,3–1. Isso explica o modelo de fazenda: volume em vez de valor.
- **Cenário conservador, C1 em en:** 8 vídeos/mês × mediana de 30–50 mil views (abaixo do ToyAutopsy, que tem 61 mil) = 240–400 mil views/mês × US$ 3 ≈ **US$ 700–1.200/mês** depois de 2–3 meses. **Pessimista** (mediana de 10 mil): ~US$ 250/mês. Se acertar um hit no nível do Steve (6 mi), um único vídeo rende ~US$ 15–25 mil.

## 5. Produção na fábrica
- **Visual:** ilustrações de produto geradas (Codex, US$ 0, 60–80 imagens) em estilo "still life" escuro, mais cartelas de recall e manchetes recriadas no código (Remotion), mais mapa ou linha do tempo. **Sem clipe de telejornal** (o ToyAutopsy vive de fair use; para nós é risco de Content ID ou claim). Voz Fish em en (~US$ 1) e 15–18 min. **Custo/vídeo ≈ US$ 1,5–3** (Fish + Runpod + fallback fal de até ~20 imagens).
- **Riscos:**
  - **Inautêntico/repetitivo (política de 15/07/2025):** o C2 é o alvo clássico (títulos-molde trocando o país, dezenas de canais da mesma rede, thumbs de "funcionária" falsa). O C1 fica mais seguro se cada vídeo tiver pesquisa própria (CPSC, FDA, Health Canada, recalls da UE/RAPEX) e roteiro narrativo, não lista seca.
  - **Difamação/marcas:** no C2 o risco é alto, porque afirma que "só 5 são leite de verdade" sobre marcas vivas, com logo e "ex-funcionário" inventado. No C1 o risco é médio-baixo, porque fala de recall documentado e histórico. Regra para nós: só fato com fonte oficial e linguagem "was recalled/banned", sem afirmar que um produto atual faz mal.
  - **Saúde/YMYL:** moderado. Contar casos e recalls passa; dar conselho de saúde ("não coma X") deve ser evitado.
  - **Imagem de produto real:** gerar embalagem idêntica com logo é risco de marca e o gerador erra letras. Preferir embalagem "parecida"/genérica, com o nome em texto no código.
- **Produto:** fraco no C1. No C2 caberia um "guia de rótulos" ou planilha, mas o C2 está descartado. Afiliado da Amazon (versões seguras/brinquedos) é Hipótese, com receita baixa.

## 6. Temas iniciais (C1, en) com evidência
| # | Tema | Evidência (vídeo: views) |
|---|---|---|
| 1 | Candy | [Steve](https://youtu.be/3Ika6QR1TPE) 6,02 mi; [Crunchy](https://youtu.be/Q5lp2HzPb0s) 751 mil |
| 2 | Snacks | [Steve](https://youtu.be/30jxZ2CMUHc) 2,85 mi; [Crunchy](https://youtu.be/S2iWgkDI_gM) 769 mil |
| 3 | Fast food items | [Steve](https://youtu.be/GgmUXIcYshE) 1,39 mi; [Crunchy](https://youtu.be/YOhtKhCv4nA) 668 mil |
| 4 | Squishy/fidget toys | [ToyAutopsy](https://youtu.be/PZxGZWeoNXE) 1,05 mi |
| 5 | Halloween/Christmas candy & toys (sazonal) | [Steve](https://youtu.be/RoGHkzmOcF0) 804 mil; [Crunchy](https://youtu.be/3y3u3aIWy_4) 796 mil |
| 6 | Breakfast cereals | [Steve](https://youtu.be/GI_cNBkEc-E) 606 mil |
| 7 | Energy drinks | [Crunchy](https://youtu.be/tOzFw04h_Co) 550 mil; [Steve](https://youtu.be/dJgzkkeBoyk) 374 mil |
| 8 | Foods people still eat | [Crunchy](https://youtu.be/ch2e4U41d6Y) 411 mil |
| 9 | Sodas | [Crunchy](https://youtu.be/AgSt-HjAraI) 303 mil |
| 10 | Toys for children / household products (ângulo nosso: kits de química dos anos 50, uranium lab) | [Crunchy toys](https://youtu.be/bEzHN6CNrIo) 166 mil; [Household](https://youtu.be/b_323BXv5D0) 167 mil |

Para fugir da manada (temas que ainda não vi feitos): Kitchen Gadgets, Baby Products, Diet Pills (YMYL: cuidado), Cosmetics, Christmas Lights/Decorations.

**Títulos-modelo:** "The Deadliest Christmas Toys Ever Sold" · "The Most Dangerous Kitchen Gadgets Ever Sold" · "The Deadliest Baby Products Ever Sold".

**Thumb:** fundo preto com vinheta, 3 produtos "parecidos" em still life com um efeito de perigo (fumaça, rachadura, brilho tóxico), uma palavra minúscula grande ("recalled.", "radioactive.") e 2–3 etiquetas tortas "banned?" / "toxic". É o padrão que funciona no Steve e no ToyAutopsy. Variante B no molde Crunchy: grade de 8 produtos com legenda curta cada.

## 7. Veredito
- **C2 "marcas do país X" → DESCARTAR.**
  - **Observado:** ≥ 25 clones em 5 idiomas em 6 semanas, rede de donos BR, títulos idênticos com o país trocado, thumbs de "funcionária" IA com logo real.
  - **Estimativa:** RPM de US$ 0,3–1 nos países-alvo e alto risco de difamação e de desmonetização por conteúdo inautêntico.
- **C1 "Deadliest X Ever Sold" → TESTAR em en** (3–4 vídeos; teste de estilo ≤ US$ 3).
  - **Observado:** Steve Talks Food fez **12,3 mi em 38 dias com 9 vídeos (mediana de 606 mil)** copiando o originador, e ToyAutopsy abriu uma subcategoria (brinquedos) com 1,05 mi no 10º vídeo.
  - **Estimativa:** en paga 3–5× o es e o tema é evergreen e de recall documentado (risco controlável).
  - **Contra:** o originador Crunchy já dubla para es/fr, a concorrência em en cresce e o formato é fácil de clonar.
  - **es fica como 2º idioma** (Jose Velasquez com mediana de 204 mil em 4 vídeos; nativos fracos), de preferência como **faixa de áudio dublada** do canal en, não canal separado. pt e de estão vazios em C1, mas o sinal de demanda é fraco (Hipótese).
