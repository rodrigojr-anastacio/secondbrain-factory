# historia-ptbr v3: Brasil × mundo no formato "como era viver / você no passado" (pt, 2026) · 28/11/2026

Pedido do Rodrigo (28/11): "não quero ser tão nichado; o novo olhar (você no passado) não precisa ser do Brasil; **confirmar com dados**". Custo pago US$ 0. Nada foi para o banco.

## Método
- **Busca nova e balanceada:** 36 termos, **18 de tema brasileiro × 18 de tema mundial**, no mesmo molde ("como era a vida/viver em X", "e se você vivesse…"), filtro do YouTube **"este ano"** (2026), 30 resultados por termo, `yt-dlp` via WARP (`brasil-x-mundo/termos.tsv`, `busca.py`, `busca.json`). Views, duração, idioma e inscritos pela Data API (`videos.list`/`channels.list`, token readonly; ~40 unidades). 1.009 IDs, 996 vídeos, 613 canais.
- **Filtro do formato:** pt, publicado em 2026, ≥ 5 min, título com marcador do formato (como era / assim era / um dia / sobreviv / você / sua vida / vida de… / ANO:), **canal < 1 mi de inscritos** (tira History Brasil, Canal Top10 etc., que distorcem e não são concorrentes alcançáveis).
- **Triangulação:** o corpus de 846 vídeos de `PT-TITULOS-DEMANDA.md` (12 meses), que tinha **viés pró-Brasil** (2/3 das buscas eram de temas brasileiros), unido à busca nova: **1.097 vídeos** no formato.
- **Classes pelo título:** **BR-histórico** (Brasil até ~1950), **BR-recente** (nostalgia anos 50–2000, ditadura, desastres "instantes antes": outro formato, fora do nosso molde de bonequinhos) e **MUNDO**. Lista classificada: `brasil-x-mundo/videos-classificados.csv`. Scripts: `analise2.py`, `analise3.py`.

## 1. Resultado geral (1.097 vídeos no formato, pt, 2026)
| classe | vídeos | canais | mediana | p75 | ≥ 100 mil | canal < 50 mil com ≥ 100 mil | mediana do top 10 |
|---|---|---|---|---|---|---|---|
| **MUNDO** | 651 | 258 | **3.373** | **25.159** | **70** (11%) | **33** | **702.641** |
| BR-histórico | 362 | 138 | 1.865 | 15.276 | 42 (12%) | 27 | 434.848 |
| BR-recente (nostalgia/ditadura) | 84 | 19 | 17.218 | 106.707 | 22 (26%) | 22 | 654.030 |

Só a busca balanceada nova (18 × 18 termos): MUNDO mediana 999 / top 10 585 mil; BR-histórico mediana 1.768 / top 10 435 mil. No corpus antigo (12 meses): MUNDO 6.076 × BR-histórico 2.928.
**Leitura:** a mediana fica no mesmo patamar (empate técnico, depende da amostra), mas **o teto e a quantidade de hits são do mundo**: 70 × 42 vídeos ≥ 100 mil, top 10 com 703 mil × 435 mil, e o mundo tem quase o dobro de canais disputando sem saturar a mediana.

## 2. No NOSSO formato (2ª pessoa: "você", "sua vida")
| classe | vídeos | mediana | ≥ 100 mil | maiores |
|---|---|---|---|---|
| **MUNDO** | 88 | **4.944** | **11** (12%) | Banquete de Elizabeth I 590.720; Taverna medieval 554.536; Farol 251.190; higiene 1348 209.063; "Você não sobreviveria nem 1 hora na Grécia Antiga" 173.563; "7 dias no tempo das cavernas" 171.047 |
| BR-histórico | 43 | **643** | 4 (9%) | **soldado brasileiro na 2ª Guerra 395.594**; lugares de SP 379.091; tropeiro 1820 130.414; **pracinha 123.367**; o resto fica em 7–10 mil |

**Este é o número que decide:** em 2ª pessoa, **mundo tem mediana 7,7× maior** (4.944 × 643). No Brasil, a 2ª pessoa só provou um tema: **o pracinha da FEB** (395 mil + 124 mil, e o Confluxo com 644 mil em 08/2025). O canal "Vida Brasileira TV" fez a série "Por que você não sobreviveria… no Brasil" e, fora o tropeiro (130 mil), ficou em 9–15 mil.

## 3. Termo a termo (só vídeos no formato, canal < 1 mi)
**Brasil (18 termos):** a demanda brasileira forte é **cidade antiga / Império em tour de reconstrução IA**, não ofício nem sobrevivência:
- fortes: São Paulo antigamente (mediana 242.296), Brasil Império (121.733), Rio de Janeiro antigo (109.168), Brasil em 1900 (100.095), imigrantes (32.083), Brasil colonial (18.025);
- fracos: indígenas antes de 1500 (3.726), bandeirante (2.016), seringueiro (1.768), tropeiro (1.553), pré-histórico (1.503), caravela para o Brasil (1.153), ouro de Minas (1.068), Canudos (703), **Rio 1808 (551)**, cangaço (372), "e se você vivesse no Brasil colonial" (142), pracinha (75 na busca genérica; a prova dele está nos títulos em 2ª pessoa, §2).
- **Os temas brasileiros do backlog anterior (tropeiro, ouro, seringueiro, Lampião, caravela de Cabral) estão quase todos na metade fraca.**

**Mundo (18 termos):**
- fortes: **Idade Média (68.885; 41% ≥ 100 mil)**, Egito antigo (9.100), 2ª Guerra (8.426), Velho Oeste (5.015), Londres vitoriana (4.611), pré-história (2.206, p75 148 mil), vikings (1.845, 25% ≥ 100 mil);
- fracos em pt: União Soviética (950), Grécia (686), grandes navegações (545), Japão feudal (406), Roma "genérica" (335), Revolução Francesa (277), peste (207 no termo genérico, mas 608 mil / 416 mil / 209 mil nos vídeos do tema), astecas (137), pirata (101), trincheiras da 1ª Guerra (73).
- Japão, Revolução Francesa, piratas e 1ª Guerra **não têm demanda em pt** em 2026 (estão fora do backlog). Roma só entra com recorte de papel (legionário: 228 mil num canal de 1,4 mil inscritos).

## 4. Conclusão: quanto do backlog deve ser Brasil
- **Não há prêmio por ser brasileiro**: na média, BR-histórico ≈ mundo; no nosso formato (2ª pessoa) o mundo rende 7,7× mais na mediana e tem 70 × 42 hits.
- **Brasil entra só onde o tema bate a mediana do mundo com prova própria:** pracinha (2ª pessoa provada 3×), Rio 1808 (vizinho do Império/Rio antigo, os termos BR mais fortes; tema com hit de 790 mil) e Brasil pré-histórico (Zoomundo 900 mil; público de animais, universal).
- **Resposta: 3 de 12 (25%) Brasil, 9 de 12 (75%) mundo; no teste, 1 de 4.** Cidade-nostalgia (SP 1900, anos 70/80/90, ditadura) é forte, mas é outro formato (tour IA realista, 20–30 min, sem bonequinho/humor) e a ditadura é tema político: fica fora.
- **Rio 1808 sai do teste**: o termo do tema tem mediana 551 e a única 2ª pessoa do Rio imperial fez 7 mil. Continua como **amostra de formato** (roteiro, crivo, similaridade valem para qualquer tema) e é o 1º depois do teste.

## Limites
- A busca do YouTube personaliza pouco via WARP, mas a ordem muda de um dia para o outro; os números são retrato de 28/11/2026.
- Classe pelo título (regex): títulos sem nome de lugar brasileiro caem em MUNDO (ex.: "Como os humanos antigos sobreviviam no calor extremo"). Erro pequeno nas duas direções; os top 20 de MUNDO e BR-histórico da busca nova foram conferidos à mão.
- Views de vídeo não são busca: medem o que o algoritmo distribuiu, que é o que importa para um canal pequeno.
