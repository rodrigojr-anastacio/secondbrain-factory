# Fatos com fonte: Em Relevo 006, Caraguatatuba 1967 × São Sebastião 2023 (Serra do Mar)

Coleta em 16/11/2026 (WebSearch/WebFetch; PDFs lidos: Cruz 1975 na RBG/IBGE, livre-docência de B. C. Vieira USP 2022/24, relatório Kobiyama/GADRI 2023, IBGE 2018, Pesquisa FAPESP 326) + cálculo próprio do relevo (`shared/perfil_escarpa.py` → `dados/perfis.json`) e chuva NASA (`dados/nasa/litoral-2023.json`).
Grau: **C** = fonte primária/acadêmica lida · **S** = só secundária (narrar com "segundo…") · **D** = divergente (versões listadas) · **P** = cálculo próprio. Coluna "manada?" = aparece em alguma transcrição de `ref/manada-*.txt` (ver `ANGULO.md`).

## Fontes principais
- **[CRUZ]** Olga Cruz, "A serra do Mar e o litoral na área de Caraguatatuba – SP. Contribuição à geomorfologia litorânea tropical", *Revista Brasileira de Geografia* 37(2), 1975 (tese USP; IBGE, licença CC BY 4.0 declarada pela revista). https://rbg.ibge.gov.br/index.php/rbg/article/view/1161/858
- **[VIEIRA]** Bianca C. Vieira, tese de livre-docência, FFLCH/USP, 2022 (pub. 2024). https://teses.usp.br/teses/disponiveis/8/630/tde-03062024-122514/publico/2022_BiancaCarvalhoVieira1.pdf
- **[DIAS17]** Dias, Dias & Vieira, *Revista do Departamento de Geografia* (USP), 2017. https://revistas.usp.br/rdg/article/download/132714/129865/257869
- **[ISL20]** Dias, Vieira & Gramani, ISL 2020. https://www.issmge.org/uploads/publications/105/106/ISL2020-66.pdf
- **[GADRI]** M. Kobiyama, relatório GADRI 2023 (São Sebastião, fev/2023; dados CEMADEN). https://gadri.net/events/Kobiyama%20%28GADRI-report%202023%29-Sao%20Sebastiao-2023-Fev.pdf
- **[FAPESP]** Pesquisa FAPESP 326 (mar/2023), "Chuva no litoral". https://revistapesquisa.fapesp.br/wp-content/uploads/2023/03/050-053_chuva-no-litoral-cie_326.pdf
- **[NASA-EO]** NASA Earth Observatory, "Landslides in São Paulo, Brazil", 04/03/2023 (Landsat 9 29/10/2022 × Landsat 8 26/02/2023; domínio público). https://science.nasa.gov/earth/earth-observatory/landslides-in-sao-paulo-brazil-151051/
- **[IBGE18]** IBGE/CEMADEN, *População em áreas de risco no Brasil* (2018, Censo 2010), apêndice 3. https://biblioteca.ibge.gov.br/visualizacao/livros/liv101589.pdf
- **[IBGE22]** IBGE Cidades, Censo 2022. https://www.ibge.gov.br/cidades-e-estados/sp/caraguatatuba.html
- **[SGB]** Carta de suscetibilidade a movimentos gravitacionais de massa e inundação, Caraguatatuba (SGB/CPRM). https://rigeo.sgb.gov.br/handle/doc/19381 ; São Sebastião (maio/2017): https://rigeo.sgb.gov.br/bitstream/doc/23448/1/sao_sebastiao.pdf
- **[TT]** AWS Terrain Tiles (terrarium z12; SRTM/ETOPO), perfis calculados em `shared/perfil_escarpa.py`.

## 1. O relevo (a parede)
| ID | Fato | Número | Fonte | Grau | manada? | Frase segura |
|---|---|---|---|---|---|---|
| R1 | Perfil centro de Caraguatatuba → serra (vale do Santo Antônio): ~750 m a 7,5 km da praia; topo ~865 m a ~10,7 km | 750–865 m | [TT] `dados/perfis.json` | P | não | "Da praia à borda do planalto, uns oitocentos metros de subida em menos de dez quilômetros" |
| R2 | Perfil Morro do Cruzeiro → crista: 700 m a 5,7 km da praia; topo ~835 m a 9,3 km; trechos de ~30° | 700 m / 5,7 km | [TT] | P | não | "Setecentos metros de altura a menos de seis quilômetros do mar" |
| R3 | Perfil Barra do Sahy (São Sebastião) → crista: ~685 m a ~5,4 km; topo 724 m a ~9,2 km; trechos de ~36° | 685 m / 5,4 km | [TT] | P | não | "Em São Sebastião, o mesmo degrau: quase setecentos metros a cinco quilômetros e meio da praia" |
| R4 | Borda do planalto em 750–900 m acima de Caraguatatuba; serra de Juqueriquerê > 1.300 m | 750–900 m | [CRUZ] | C | não | "A borda do planalto fica entre setecentos e cinquenta e novecentos metros" |
| R5 | Município de 0 a 1.318 m; ~60% acima de 200 m; encostas de 15–40° | 1.318 m | [VIEIRA] p. 62 | C | não | — |
| R6 | A escarpa nasceu de falhamento junto à atual plataforma e recuou por erosão (idade do rifte: Cretáceo Sup.–Paleógeno, divergente) | — | Almeida & Carneiro 1998 (RBGeoc 28(2)) via resumos | S | não | "A serra é a borda de um bloco que se partiu há dezenas de milhões de anos e vem recuando desde então" (sem número de idade) |
| R7 | Bacia do Rio Santo Antônio ~30 km² (Cruz) / ~32 km² (CEMADEN); 54,3% com declive > 40% | 30 km²; 54% | [CRUZ] p. 136; Nery/CEMADEN | C | não | "Mais da metade da bacia tem declive acima de quarenta por cento" |

## 2. A chuva que a serra fabrica
| ID | Fato | Número | Fonte | Grau | manada? | Frase segura |
|---|---|---|---|---|---|---|
| C1 | Efeito orográfico da escarpa; média anual > 2.000 mm em Caraguatatuba | >2.000 mm/ano | [VIEIRA] | C | mecanismo sim (ToXu, Dossiê: sem número); número não | "O ar úmido do mar bate na parede, sobe, esfria e despeja" |
| C2 | 2023: o vento de superfície "interagiu com o relevo da serra do Mar" e reforçou a chuva; frente fria + ciclone pequeno entre Ubatuba e Paraty; oceano ~1 °C acima do normal; nuvens "ancoradas" por horas | ~1 °C | [FAPESP] (Pedro L. S. Dias, IAG-USP) | C | não | atribuir ao IAG-USP |
| C3 | 18–19/02/2023, 24 h (CEMADEN): Bertioga 682–683 mm (Praia de Guaratuba), São Sebastião 626–627 mm (Barra do Una), Guarujá 388, Ilhabela 337, Ubatuba 335, **Caraguatatuba 234 mm** | 683 / 627 / 234 | [GADRI] tab. 2; [FAPESP] | C | 600/680 de passagem no ToXu; 234 não | "Seiscentos e oitenta e três milímetros em vinte e quatro horas em Bertioga" |
| C4 | Bertioga: 273 mm em 2 h e > 400 mm em 6 h na noite de 18/02/2023; média de fevereiro na região ~225 mm | 273 / 400 / 225 | [GADRI] | C | não | "Em seis horas, quase dois meses de chuva" (400 ÷ 225 ≈ 1,8) |
| C5 | Recorde nacional de chuva em 24 h, acima de Petrópolis 2022 (534,4 mm) | — | [GADRI] | C | não | "o maior acumulado em vinte e quatro horas já registrado no país, segundo o CEMADEN" |
| C6 | Estações acima da serra (Mogi, São Luiz do Paraitinga) com no máximo ~60 mm em 2023 | ~60 mm | trabalho SBGFA 2024 (só resumo) | S | não | só se confirmar; senão usar o contraste Bertioga × Caraguatatuba (C3) |
| C7 | Satélite NASA IMERG (células de ~10 km) estimou no máximo ~109 mm em terra no litoral em 18–19/02/2023 | 109 mm | `dados/nasa/litoral-2023.json` | P | não | "O satélite, que enxerga em quadrados de dez quilômetros, quase não viu: a chuva caiu numa faixa estreita, colada na serra" (opcional) |
| C8 | 1967: chuva desde o dia 16; forte a partir das 18 h do dia 17; posto da Light/fazenda: 115,0 mm (17) + 420,0 mm (18) com pluviômetro transbordado; 851 mm no mês (posto da fazenda) e 945,6 mm (posto Light de Caraguatatuba) | ≥535 mm/2 d | [CRUZ] p. 103 | C | ToXu dá 260 + 324,8 ≈ 585; AntigamenteBR "meio metro" | "Mais de quinhentos milímetros em dois dias, num mês de quase novecentos e cinquenta" |
| C9 | 586 mm em 48 h (17–18/03/1967) é a cifra mais citada (atribuída a Cruz) | 586 | [ISL20], [DIAS17] | D | ToXu (585) | não usar o 586 como cena principal |
| C10 | Postos DAEE E2-042/043: só 245 mm em 17–18/03 — a chuva variou muito de um vale a outro | 245 | [VIEIRA] p. 62 | C | não | "Num posto a poucos quilômetros, o pluviômetro marcou menos da metade" |

## 3. A pele da serra (o que desliza)
| ID | Fato | Número | Fonte | Grau | manada? | Frase segura |
|---|---|---|---|---|---|---|
| P1 | Escorregamentos translacionais rasos que viram corridas de detritos nos canais saturados | — | [DIAS17]; [ISL20]; Cruz chama de "debris avalanche"; a população dizia "rodar" | C | "escorregamento raso"/"debris flow" sim (ToXu, TV Câmara) | — |
| P2 | Superfície de ruptura a 1–2,5 m de profundidade (contato colúvio/saprolito × solo residual) | 1–2,5 m | De Ploey & Cruz 1979; Furian et al. 1999, em [VIEIRA] | C | ToXu: "um a poucos metros" | "A camada que desce tem de um a dois metros e meio" |
| P3 | Em 1967 a ruptura chegou muitas vezes à rocha sã (manto encharcado) | — | [VIEIRA] | C | não | — |
| P4 | Escorregamentos concentrados em encostas côncavas > 30° | >30° | [DIAS17] | C | ToXu (de passagem) | — |
| P5 | Cruz: as vertentes mais atingidas tinham declive > 40% (~22°); topos aplainados ficaram a salvo; em declive menor, só onde a água se concentra | >40% | [CRUZ] | C | não | — |
| P6 | 81,5% das cicatrizes sobre o Granitoide Caraguatatuba | 81,5% | [DIAS17] | C | não | "Oito em cada dez cicatrizes estão na mesma rocha" |
| P7 | 640 cicatrizes de escorregamento num raio de 7–15 km (fotos aéreas) | 640 | Fúlfaro et al. 1976; De Ploey & Cruz 1979, em [VIEIRA] | C | não ("centenas"/"milhares" sem contagem) | "Seiscentas e quarenta cicatrizes contadas em fotos aéreas" |
| P8 | ~2 milhões de toneladas de material mobilizado | 2 mi t | Petri & Suguio 1971, em [CRUZ] p. 142 | C | não | "Cerca de dois milhões de toneladas" |
| P9 | ~20% da reserva florestal (13.769,6 ha) destruída pelos escorregamentos | 20% | [CRUZ] | C | não | — |
| P10 | Coesão 0–11 kPa; atrito 25,8–36,8° | — | [VIEIRA] | C | não | não narrar números; ideia: "solo quase sem cola" |
| P11 | Gramani (2001): o 18/03 em 4 fases: enchente inicial, escorregamentos, corridas de detritos, enchente por bloqueio | 4 | Gramani 2001, em [VIEIRA]/[ISL20] | C | não | — |
| P12 | Carta de declividade da bacia do Santo Antônio desenhada por Olga Cruz (Fig. 7 do artigo de 1975) | — | [CRUZ] Fig. 7 (CC BY 4.0) | C | não | "A geógrafa Olga Cruz, da USP, mediu a inclinação de cada encosta dessa bacia" |

## 4. O caminho até a cidade (1967 contado pelo mapa)
| ID | Fato | Número | Fonte | Grau | manada? | Frase segura |
|---|---|---|---|---|---|---|
| K1 | 18/03/1967: barreiras desde a manhã; às 13 h, morros do Cruzeiro e do Jaraguá; às 16h30, frente no vale do Santo Antônio; chuva parou na madrugada do 19 | 13 h; 16h30 | [CRUZ] p. 103 | C | horários e morros sim (AntigamenteBR, Dossiê) | só como marcação no mapa, sem minuto a minuto |
| K2 | Todos os vales da bacia foram atingidos; rios: Santo Antônio, Guaxinduba, Ribeirão da Aldeia, Pau d'Alho, Massaguaçu, Canivetal… | — | [CRUZ]; Dias et al. 2020 | C | Santo Antônio sim; os outros não | — |
| K3 | O Santo Antônio alargou de 10–20 m para 60–80 m | ×4 | [CRUZ] | C | não | "O rio ficou quatro vezes mais largo" |
| K4 | Lama até 0,80 m nas ruas; "dezenas de milhares de troncos", alguns com > 1 m de diâmetro | 0,8 m | [CRUZ] | C | troncos sim (genérico) | lama 80 cm = nosso |
| K5 | Ponte principal deslocada; Cruz: se não tivesse sido, "a cidade inteira teria sido inundada"; Tamoios "desapareceu na sua maior parte", precipícios > 100 m | — | [CRUZ] p. 103–104 | C | ponte/estrada sim (consenso) | só de passagem |
| K6 | Vítimas: 120 (Cruz 1974) a ~450–487 (IPT/imprensa; contagem da época); "436 oficial" na imprensa | 120–487 | [VIEIRA], [GADRI], imprensa | D | 436 = consenso | "O número nunca fechou: de cento e vinte, na conta da geógrafa, a quase quinhentos na contagem da época" (sem "morte" em título/descrição) |
| K7 | Em 1967 a maior parte da planície era fazenda, o que reduziu os danos | — | Dias et al. 2020, via [ISL20]/[VIEIRA] | C | não | — |
| K8 | População: 15.073 (1970, agregador) → 134.873 (Censo 2022) | ×9 | [IBGE22]; 1970 S | C/S | 130–134 mil sim (TV Câmara, Factum) | "Hoje são quase cento e trinta e cinco mil moradores" |
| K9 | Serra das Araras (RJ), 22–23/01/1967: 225 mm em 4 h | — | [CRUZ] p. 103 | C | ToXu (de passagem) | opcional |

## 5. 2023: a mesma receita
| ID | Fato | Número | Fonte | Grau | manada? | Frase segura |
|---|---|---|---|---|---|---|
| S1 | 65 vítimas (64 em São Sebastião + 1 em Ubatuba); 1.815 desabrigados e 2.251 desalojados | 65 | [GADRI] | C | ToXu "mais de 60" de passagem | "sessenta e cinco vidas" (só narração) |
| S2 | Landsat antes (29/10/2022) × depois (26/02/2023): encostas entre Juquehy/Jaqueí e Praia da Baleia cheias de cicatrizes | — | [NASA-EO] | C | não | "O satélite Landsat fotografou as mesmas encostas antes e depois" |
| S3 | NASA (Emberson): "áreas com concentração tão densa de escorregamentos são bem incomuns, mas não sem precedente" | — | [NASA-EO] | C | não | citação traduzida com atribuição |
| S4 | Inventário: ~1.000 pontos de escorregamento (USP IAG/IGc) / 571 (outro critério) | D | imprensa/artigos | S/D | não | "centenas de deslizamentos" |
| S5 | Vila Sahy: ocupação dos anos 1980; concentrou a maioria das vítimas | — | imprensa | S | não | — |
| S6 | IPT 2018 (São Sebastião): 161 moradias em risco alto; 52 setores (16 alto, 36 médio); a Vila Sahy estava em médio | — | imprensa sobre relatório IPT (Correio Braziliense 2023) | S | não | "segundo reportagens sobre um relatório do IPT de 2018" |
| S7 | Distância Barra do Sahy → centro de Caraguatatuba ≈ 33 km em linha reta | ~33 km | cálculo próprio (coord.) | P | não | "a uns trinta e cinco quilômetros" |

## 6. O mapa de hoje (fecho útil)
| ID | Fato | Número | Fonte | Grau | manada? | Frase segura |
|---|---|---|---|---|---|---|
| M1 | Cartas de suscetibilidade do SGB para Caraguatatuba e São Sebastião (encostas de alta suscetibilidade a deslizamento e as planícies de inundação) | — | [SGB] | C | "mapa de risco" genérico de passagem | "O Serviço Geológico do Brasil já mapeou onde a serra é mais suscetível" |
| M2 | IBGE/CEMADEN 2018 (Censo 2010): Caraguatatuba com 3.006 pessoas em 19 áreas de risco mapeadas; Ubatuba 4.678 em 50 | 3.006 | [IBGE18] | C | não | "Em dois mil e dez, o IBGE contou cerca de três mil moradores de Caraguatatuba dentro de áreas de risco mapeadas" |
| M3 | SMS 40199: cadastro de CEP para alertas da Defesa Civil | 40199 | Defesa Civil (serviço) | C | não | — |

## Cota de dados próprios (bíblia ≥ 40%)
Fora de todas as transcrições: R1–R5, R7, C2–C5, C7, C10, P6–P10, P12, K3, K4 (lama), K7, S2, S3, S6, S7, M1 (específico), M2 → ver contagem por cena no `SOURCES.md`/`ETAPA1.md`.
