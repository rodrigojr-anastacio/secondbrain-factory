# Canal de CLIMA EXTREMO / FENÔMENOS: potencial (08/11/2026)

Pedido do Rodrigo (08/11): "Por que tantos tornados no Sul?" tem cara de hit; que canal sustenta isso com continuidade? Formato: imagens e vídeos reais + motion (mapa 3D, contadores; `pesquisa/estilo-mapa-relevo-3d/PADRAO.md`).
Método: `playbooks/novo-canal.md`, etapas 1–3b (sem blueprint, sem canal criado). Custo: **US$ 0**. Cota da Data API: **~250 de 2.000 unidades**. [O] = observado nos dados; [I] = inferido; **Hipótese** = sem dado.

## Resumo executivo
| | |
|---|---|
| **Decisão** | **TESTAR** (3 vídeos longos + Shorts, com fase 1 de amostra antes) |
| **Guarda-chuva** | **Clima extremo e desastres explicados no mapa 3D**: 3 tipos de episódio, (Q) quente "o que está acontecendo em X", (E) evergreen "por que X acontece aqui" e (R) desastre real reconstruído minuto a minuto no mapa |
| **Idioma** | **en** (matriz 7,75 × es 6,40 × pt 6,30; vence nas 3 sensibilidades). 2º: **pt como versão** dos episódios sobre o Brasil e dos Shorts quentes |
| **Piloto** | "Why Is Brazil Suddenly Getting So Many Tornadoes?" (versão pt: "Por que o Brasil virou terra de tornados?") |
| **Risco principal** | Imagem real de terceiros (TV e vídeo viral) → Content ID e "conteúdo reutilizado" no YPP. Em 2º lugar, a efemeridade: o pico de notícia dura de 1 a 2 semanas |
| **Regra de imagens** | O mapa 3D e os gráficos são nossos e formam a base do vídeo. Material real só de fonte com licença explícita (NASA/NOAA/GOES, Copernicus, Wikimedia por arquivo, IBGE/INMET) ou com autorização por escrito, sempre com crédito na tela. **Nunca** TV nem vídeo viral sem licença |

Números-chave [O]:
- Busca "tornado" no YouTube BR: média 19 em 5 anos (Trends, gprop=youtube), hoje 36 → é interesse que fica, não só notícia.
- "Tornado brasil" (web): picos em nov/2025 (100) e nov/2026 (59). A temporada se repete (set–nov).
- O El Niño está no maior nível de busca em 5 anos no BR (59 → 29 na escala de 5 anos).
- Canais novos de desastre (1º vídeo entre 2025 e 2026) fazem de **1 a 6 milhões de views/mês**: The Last Day (en, jul/2026) 3,6 mi/mês; Um Documentário (pt, abr/2026) 5,9 mi; Nature Khauf (hi, jul/2026) 5,4 mi; Disasters Explained (en, nov/2025) 1,0 mi; SkyWhisper e Dark Horizon (en) ~1,1 mi cada.

## 1. Demanda: agora × evergreen
**Busca do YouTube (yt-dlp via WARP; mediana das views do top-10 por relevância; vídeos ≥ 100 mil no ano e no mês)** [O]. Dados em `dados/demanda.json`.
| Idioma | Consulta | Mediana top-10 | ≥100 mil no ano | ≥100 mil no mês |
|---|---|---|---|---|
| en | how tornadoes form | 3,7 mi | 21 | 5 |
| en | strongest tornado ever recorded | 1,8 mi | 29 | 3 |
| en | natural disaster documentary | 940 mil | 31 | 19 |
| en | tornadoes in brazil | 69 mil | 28 | 18 |
| es | fenómenos naturales explicados | 2,6 mi | 21 | 2 |
| es | tornado en brasil | 130 mil | 33 | 20 |
| pt | fenômenos naturais impressionantes | 2,0 mi | 14 | 4 |
| pt | maiores desastres naturais da história | 1,1 mi | 13 | 0 |
| pt | tornado santa catarina | 202 mil | 29 | **24** |
| pt | tornados no brasil | 131 mil | 31 | 15 |
| pt | por que tantos tornados no brasil | 42 mil | 20 | 2 |
| fr / de | comment se forme une tornade / Tornado Brasilien | 69 mil / 126 mil | 7 / 28 | 2 / 8 |

**Hits recentes sobre o clima no Brasil (últimos 90 dias)** [O]:
| Views | Data | Canal (inscritos) | Título | Tipo |
|---|---|---|---|---|
| 5,9 mi | 27/08 | Paulo Jubilut (3,9 mi) | Super EL NIÑO NO BRASIL: o que esperar? | longo, explicativo |
| 1,1 mi | 12/09 | Global Weather Network (64 mil, **en**) | BRAZIL HIT by Powerful Storms… | longo, notícia |
| 794 mil | 15/08 | Ciência Todo Dia (7,9 mi) | por que tantos TORNADOS estão acontecendo no BRASIL? | Short |
| 773 mil | 07/09 | Capital Financeiro | É assim que o Super EL NIÑO vai atingir cada estado | longo |
| 757 mil | 20/09 | MetSul (322 mil) | Grave onda de tempestades e tornados no Sul | longo, notícia |
| 588 mil | 24/10 | Chão do Sul (4,6 mil, canal novo) | Por que a Região Sul é o OPOSTO das outras regiões? | longo, mapa |
| 515 mil | 04/11 | Natureza em Fúria (93 mil) | Chapecó (SC)! TORNADO destrói aeroporto | longo, reupload |
| 402 mil | 30/10 | Mundo Entrópico (65 mil) | O que está ACONTECENDO com SANTA CATARINA?! | longo, mapa |

**Autocomplete** [O] (`dados/autocomplete.json`): "tornado em chapecó / maringá / santo augusto / curitiba", "ciclone bomba", "el niño 2026", "o que está acontecendo com o clima no brasil", "maiores desastres naturais do brasil", "tragédia de brumadinho / vargas 1999 / mariana", "enchente no nepal" (em pt, es e en: o desastre do Nepal de 26/08/2026 é o evento global do ano). Em en: "disaster explained" (aberfan, challenger, chernobyl, "every disaster explained") e "strongest hurricane ever recorded".

**Pico de notícia × interesse que fica** [O] + [I]:
- O termo exato da notícia ("tornado santa catarina") vai de 0 a 18 e volta a ~0 em 2 semanas (Trends web).
- O tema-mãe fica: "tornado" no YouTube BR nunca cai abaixo de ~20; "how tornadoes form" e "strongest tornado" acumulam milhões anos depois.
- As crises brasileiras se repetem por estação: ciclone (jun–set; pico jul/2023), enchente (mai/2024), tornado (set–nov; 2025 e 2026), El Niño (2026).
- **Conclusão [I]:** o vídeo quente rende na semana. O canal vive do evergreen e da reconstrução, e o quente serve de isca para a descoberta.

## 2. Guarda-chuvas e continuidade
Canais com uploads analisados via API (`dados/canais_nicho.json`; views/mês = views ÷ idade × 30 se o canal tem < 1 ano, senão os últimos 90 dias ÷ 3).
| Guarda-chuva | Exemplos (idioma, 1º vídeo, inscritos, views/mês, mediana dos longos) | Sustenta 50+? | Leitura |
|---|---|---|---|
| **A. Clima/fenômeno explicado** ("por que X acontece") | Disasters Explained (en, nov/25, 29 mil, 1,0 mi, 35 mil; animação 2D vetorial); Astrum Earth (en, mar/25, 504 mil, 7,3 mi); PBS Terra (en, 2,4 mi); Te lo Pinto (es, 598 mil, 6,5 mi); Ciência Todo Dia (pt, Shorts) | sim | Evergreen, RPM bom. O "every tornado type" virou fórmula (DisasterLab, The Escalist e Clima Indomável copiam com mediana < 9 mil) |
| **B. Desastre real reconstruído** ("o dia em que…", minuto a minuto) | The Last Day (en, jul/26, 36 mil, 3,6 mi); SkyWhisper (en, fev/26, 1,1 mi, mediana 219 mil); Dark Horizon (en, dez/25, 1,1 mi); DisastersUncovered (en, 0,9 mi); Um Documentário (pt, abr/26, 124 mil, 5,9 mi, vídeos de ~65 min); AntigamenteBR (pt, ago/26, 1,2 mi); Nature Khauf (hi, 5,4 mi) | sim (centenas de desastres) | **O guarda-chuva mais quente de 2026.** Quase todos usam vídeo fotorrealista de IA (Um Documentário, The Last Day) ou footage de TV (SkyWhisper, com logo da ABC News) |
| **C. Notícia do tempo** (reupload + narração) | Natureza em Fúria (pt, 2,6 mi/mês, mediana 23 mil); Brasil em Alerta (pt, 2,5 mi); Global Weather Network (en, 100 longos em 90 dias, mediana 7,5 mil); dezenas de canais de IA criados em set–out/2026 (Sky Alert, Clima24, Clima em Alerta, Weather Latino: mediana < 1 mil) | sim, mas | **Descartar.** Saturado de canais de IA, todo o material é de terceiros (risco de YPP) e efêmero |
| **D. Brasil explicado por mapas** | Mundo Entrópico (pt, 65 mil, mapa de satélite + cards); Chão do Sul, Explica no Mapa e Além do Mapa (**todos de out/2026**, 1,7–4,3 mi/mês nas primeiras semanas); Geografía con Geoff (es, 2,8 mi/mês) | sim | Explosão de clones em pt neste mês. O clima aqui é só uma fatia |
| E. "E se…" climático | The Last Day ("What if the Moon crashed", 2 mi) | parcial | RPM baixo ("what if" 1,5–4) |
| F. Compilado "captado em câmera" | Mega Fatos, Catástrofe X (mediana 3 mil) | — | Reuso puro: fora |

Instagram/TikTok: a referência **@relevo.ia** (Willian Cardoso) não tem canal achado no YouTube (`forHandle` @relevo.ia / @relevoia / @relevo vazios; o @williancardoso tem 22 inscritos e talvez não seja o mesmo dono). O post de referência (tornados em SC, 04/11) teve ~213 mil curtidas (`PADRAO.md`). **Hipótese:** o formato vertical de mapa 3D está forte no Instagram e quase vazio no YouTube longo. Não medi o TikTok (sem acesso).

**Recomendação: A + B no mesmo canal, com o mapa 3D como assinatura.** Os concorrentes de B usam vídeo de IA fotorrealista ou footage de TV; os de A usam animação 2D. Ninguém do levantamento faz **maquete 3D com dados, contadores e fotos reais creditadas** [O, nos 10 vídeos assistidos e nos 48 canais]. O formato também vale para o quente (Q), porque o mapa é o mesmo.

### 30 ideias (en; Q = quente, E = evergreen, R = reconstrução; ✓ = tem evidência de demanda nos dados)
1. Why Is Brazil Suddenly Getting So Many Tornadoes? (Q, piloto) ✓
2. South America Has a Tornado Alley — Almost Nobody Knows (E) ✓
3. The Super El Niño of 2026, Explained on One Map (Q) ✓ (5,9 mi no Jubilut; El Niño no topo do Trends)
4. Nepal 2026: The Ice Wall That Erased a Valley, Minute by Minute (R/Q) ✓ (5,2 mi na The Last Day)
5. Every Tornado Type, Explained on a 3D Map (E) ✓ (3 mi; fórmula concorrida, então só com ângulo próprio)
6. El Reno 2013: The Widest Tornado Ever Recorded (R) ✓ (16,9 mi TornadoTRX; 1,1 mi SkyWhisper)
7. Joplin 2011: 38 Minutes That Destroyed a City (R) ✓ (3,3 mi)
8. The Rio Grande do Sul Floods: How a State Went Underwater (R) ✓ ("enchente rio grande do sul" com 32 vídeos ≥ 100 mil no ano)
9. Valencia's DANA: The Flood That Came From a Clear Sky (R) ✓ (2,6 mi El Confidencial)
10. Hurricane Katrina: How New Orleans Was Built to Flood (R) ✓ (1,8 mi Dark Horizon; 2 mi Practical Engineering)
11. What Is a "Bomb Cyclone"? (E) ✓ ("ciclone bomba" no autocomplete)
12. The Strongest Hurricanes Ever Recorded, Mapped (E) ✓ (autocomplete)
13. Why the US Gets 75% of the World's Tornadoes (E) ✓ (2,2 mi Vox)
14. Tornado Alley Is Moving East (E) ✓ (3 mi PBS Terra)
15. The 1967 Landslide That Swallowed a Brazilian Town (Caraguatatuba) (R) ✓ (2 mi AntigamenteBR, pt)
16. Black Frost 1975: The Night Brazil Lost Its Coffee (R) ✓ (410 mil AntigamenteBR)
17. Brumadinho: The Dam That Buried a Town in Seconds (R) ✓ (autocomplete; 5,3 mi em barragens no Refúgio Mental) — sensível
18. The 2004 Indian Ocean Tsunami, Wave by Wave (R) ✓ (Um Documentário 2,5 mi Aceh)
19. Tōhoku 2011: Why Japan's Sea Walls Failed (R) ✓ (6,4 mi Miyako)
20. Yungay 1970: The Town Buried by a Mountain in 3 Minutes (R) ✓ (5,3 mi)
21. Why Southern Brazil Has the Wildest Weather in the Country (E) ✓ (588 mil Chão do Sul)
22. Hail the Size of Oranges: Why Southern Brazil Gets It (E/Q) ✓ (granizo 633 mil Natureza em Fúria)
23. The Day Texas Hit 60 °C in a Thunderstorm (Heat Burst) (R) ✓ (5,1 mi Swegle)
24. Lytton 2021: The Town That Hit 49.6 °C and Burned (R) — Hipótese
25. Why Argentina and Brazil Get the World's Biggest Thunderstorms (E) — Hipótese (literatura científica: sistemas convectivos da Bacia do Prata)
26. The Tri-State Tornado of 1925: 219 Miles on the Ground (R) — Hipótese (tema clássico)
27. Hurricane Catarina 2004: The South Atlantic's First Hurricane (R, Brasil) — Hipótese (curiosidade forte em en)
28. The Atmospheric River That Could Drown California (E) — Hipótese
29. Is the Weather Really Getting More Extreme? What the Data Says (E) ✓ ("why is the weather so extreme": 27 vídeos ≥ 100 mil no ano)
30. The Next 30 Days of Severe Weather Season in South America (Q, sazonal) — Hipótese

## 3. Idioma (matriz do playbook; ordem en → es → pt → fr → de)
Notas de 0 a 10. Concorrência: nota alta = pouca concorrência. RPM do nicho "desastres/documentário" 3–8 em en × fator do idioma (pt 0,25–0,35, es 0,25–0,4, fr 0,5–0,7, de ~0,8–1 [I]).
| Idioma | Demanda 30% | Concorrência 25% | RPM 20% | Viabilidade 15% | Risco 10% | **Total** | Pesos iguais | RPM 30 / Dem 20 |
|---|---|---|---|---|---|---|---|---|
| **en** | 10 | 4 | 10 | 7 | 7 | **7,75** | 7,6 | 7,75 |
| es | 7 | 7 | 4 | 7 | 7 | 6,40 | 6,4 | 6,10 |
| pt | 7 | 6 | 3 | 10 | 6 | 6,30 | 6,4 | 5,90 |
| fr | 5 | 7 | 6 | 6 | 7 | 6,05 | 6,2 | 6,15 |
| de | 5 | 6 | 8 | 4 | 6 | 5,80 | 5,8 | 6,10 |
Critérios: **demanda** = medianas e hits acima. **Concorrência**: en tem dono forte (Max Velocity, Ryan Hall, TornadoTRX) e enxame de canais novos de desastre, então 4, mas não chega à trava de ≤ 2 porque ninguém faz mapa 3D. pt tem a notícia saturada e o "explicado" aberto. **Viabilidade**: pt = fontes locais e revisão do Rodrigo; en = fábrica já escreve nativo, voz Fish en. **Risco**: pt tem desastre próximo, com vítimas e política climática no pós-eleição de 2026. Travas: nenhuma.

**Por que o en ganha:** demanda evergreen 5–20× maior e RPM ~3× o de pt. O tema Brasil não é desvantagem: "tornadoes in brazil" teve 18 vídeos ≥ 100 mil no último mês em en, e o Global Weather Network fez 1,1 mi com tempestades no Brasil. "South America's tornado alley" é **curiosidade** para o público en.
**Honestidade sobre o pt:** o vídeo dos tornados do Sul rende mais **agora** em pt (24 vídeos ≥ 100 mil no mês só em "tornado santa catarina"). Mas o RPM de pt num nicho de desastre fica em ~US$ 1–2, e o pt "Brasil por mapas" está tomado por clones desde out/2026. Por isso pt entra como **versão** dos episódios brasileiros (reescrita nativa + voz; as imagens não têm idioma) e como Shorts quentes, não como canal principal.

## 4. Imagens e vídeos reais: direitos e monetização (regra prática)
| Fonte | Status | Como usar |
|---|---|---|
| NASA, NOAA, NWS/SPC, GOES-16/19 (o GOES-East cobre a América do Sul), NASA Worldview | domínio público (governo dos EUA) | livre; crédito "NASA/NOAA"; sem logo nem sugestão de endosso |
| Copernicus Sentinel-1/2, ERA5, DEM | licença livre da UE | aviso obrigatório "Contains modified Copernicus Sentinel data 2026" ([licença](https://ads.atmosphere.copernicus.eu/licences/ec-sentinel)); ótimo para o antes/depois do rastro do tornado |
| IBGE (malhas GeoJSON), INMET (dados e estações), Cemaden | dados públicos | citar a fonte; o mapa é desenhado por nós |
| Agência Brasil (EBC) | era CC BY 3.0 BR; a Wikimedia aponta mudança para o conteúdo posterior a 23/02/2017 ([template](https://download.osmand.net/wiki/Template:Ag%C3%AAncia_Brasil)) | **conferir a licença foto por foto**; crédito "Fotógrafo/Agência Brasil" |
| Defesa Civil SC/RS/PR, bombeiros (CBMSC) | foto de órgão público **não** é domínio público no Brasil (Lei 9.610) | usar só com autorização por e-mail (costuma ser liberada com crédito) — Hipótese |
| Wikimedia Commons | depende de cada arquivo | conferir a licença; CC BY/BY-SA = crédito (+ link na descrição) |
| Vídeo de morador ou storm chaser (ex.: Lucas Moura, Brazil Storm Chaser) | do autor | **licença por escrito** (e-mail guardado na pasta do vídeo) |
| Vídeo de TV (Globo, RBS, NSC, Record, CNN), vídeo viral (Jukin, ViralHog, Newsflare) | Content ID ativo | **nunca**; 1 claim tira a receita, 3 strikes derrubam o canal |
| Manchetes | citação | recriar o recorte com o nosso tipo (veículo + data + 1 frase), sem print da página |

- **Uso justo:** o fair use é defesa dos EUA *depois* do claim. Não impede o Content ID automático e é caso a caso. No Brasil, o art. 46 da Lei 9.610 só permite citar trechos curtos para crítica ou estudo, com a fonte. **Não dá para construir o canal sobre isso.**
- **YPP:** a política de "conteúdo reutilizado" segue valendo. Desde 15/07/2025, a de "repetitivo" chama-se "inautêntico" e mira conteúdo produzido em massa; pode desmonetizar o **canal inteiro** ([ppc.land](https://ppc.land/youtube-clarifies-inauthentic-content-policy-changes/), [The Print](https://theprint.in/world/youtube-cracks-down-on-inauthentic-content-with-monetisation-policy-update-what-new-guidelines-say/2691562)). Natureza em Fúria (reupload com tarja "BREAKING NEWS") e SkyWhisper (footage da ABC) estão monetizados hoje [O, anúncios na página], mas é o perfil exato que a política mira.
- **Como o motion transforma:** em todo plano o mapa 3D, os dados e a narração são nossos, e a foto real entra como **polaroid citada**, não como o plano inteiro.
- **Regra da fábrica:**
  - ≥ 70% do tempo de tela em material próprio (mapa, gráfico, contador, objeto 3D);
  - material real só da tabela verde, com crédito na tela e na descrição;
  - `licencas.md` por vídeo com cada arquivo, a fonte, a licença e o e-mail de autorização;
  - zero TV e zero viral.

## 5. Efemeridade e sensibilidade
- **Vítimas:**
  - tom de serviço, nunca de espetáculo;
  - nada de "URGENTE / BREAKING" falso;
  - sem rosto de vítima nem número de mortos na thumb;
  - fecho útil, com os alertas da Defesa Civil (SMS 40199) e o que fazer.
- **Desinformação:**
  - vídeo velho circula como se fosse de agora [O: o Portal RBV desmentiu um vídeo "de Chapecó" com 422 mil views];
  - só usar imagem com origem conferida;
  - tornado só "confirmado" com laudo da Defesa Civil/MetSul/PREVOTS;
  - os números de casas afetadas variam conforme a data (4.441 a 5.893): citar a data do balanço.
- **Política climática:** separar o que é dado (El Niño forte, recorde de detecção) do que é tendência de longo prazo (atribuição ao aquecimento só com artigo científico); sem partido.
- **Credibilidade:**
  - barra de fontes fixa no rodapé (vem do `PADRAO.md`);
  - SOURCES por fato (MetSul, INMET, Climatempo, PREVOTS, NOAA/CPC, artigos);
  - descrição com links.
- **Efemeridade:** o Q precisa sair em ≤ 72 h. Para isso: template de mapa por região pronto e componentes reutilizáveis; o roteiro é a parte mais lenta. O canal não depende do Q (proporção sugerida 1 Q : 2 E/R).

## 6. Produção
- **Encaixe com o mapa 3D:** total, é o mesmo mundo do teste (`canais/lotr-fr/testes/motion-3d/COMPARATIVO.md`). Custo de CPU: ~1,1 s/quadro.
- **Duração recomendada:** **10–12 min** nos longos [O: Disasters Explained 11 min em média; reconstruções en de 16 a 22 min; Um Documentário ~65 min]. Com ~50% do tempo em 3D e o resto em 2D/fotos (render rápido): 12 min ≈ 10.800 quadros 3D ≈ **3,3 h** de render por vídeo, em partes ≤ 10 min (Hipótese: sombra 1024 e terreno mais leve podem cortar de 30 a 50%).
- **Shorts como alavanca:** sim [O: Short do Ciência Todo Dia com 794 mil; "entender.brasil" com 1,2 mi em Short de furacão]. 2–3 Shorts por longo (cenas 3D re-enquadradas na vertical, ~45 s ≈ 25 min de render cada). Os Shorts quentes em pt são a ponte para a versão pt.
- **Ritmo viável:**
  - **1 longo por semana + 2–3 Shorts** no teste, com a VPS dividida com os outros canais (um render por vez);
  - 2 longos por semana só com GPU por hora ou com otimização medida.
- **Custo direto estimado:** ~US$ 2–5 por vídeo (voz Fish en; quase nada de imagem de IA) — Hipótese, a medir.
- **O que falta montar:**
  1. malhas do IBGE (estados/municípios) + Natural Earth (mundo) + DEM Copernicus/SRTM para o relevo;
  2. leitor de imagem GOES/Worldview e Sentinel-2 (antes/depois);
  3. base de tornados: PREVOTS (América do Sul) e NOAA SPC Storm Events (EUA, domínio público);
  4. componentes Remotion: contador, pino, fio, polaroid, recorte de manchete, barra de fontes, legenda de máquina de escrever;
  5. `licencas.md` + checagem de licença na skill `qa`.

## 7. Decisão: **TESTAR**
**Por que não INVESTIR:** o estilo 3D ainda não foi aprovado em vídeo de verdade (fase 1), o render é caro na VPS e o en tem concorrência forte. **Por que não DESCARTAR:** a demanda evergreen é enorme, o guarda-chuva B explodiu em 2026 e a assinatura 3D + fontes reais nos diferencia de todos os 48 canais vistos.

**Piloto: "Why Is Brazil Suddenly Getting So Many Tornadoes?"** (en, ~11 min; versão pt "Por que o Brasil virou terra de tornados?")
- **Hook (próprio, não o "2 tornados em 18 minutos" do @relevo.ia):** "On November 4th, a passenger jet had just landed in Chapecó, in southern Brazil. Its instruments read seventy knots. Minutes later, the airport terminal's glass walls were gone. Brazil isn't supposed to have tornadoes. In 2025 it recorded ninety-two." A câmera sai da pista e revela o mapa do Sul, e o contador sobe 0 → 92.
- **Capítulos:**
  1. *Chapecó, 10:30* — o evento no mapa 3D: tornado em Chapecó e, ~18 min depois, Xanxerê; aeroporto e casas afetadas, com a data do balanço.
  2. *The Other Tornado Alley* — o corredor da Bacia do Prata (norte do RS, oeste de SC, sudoeste do PR): Andes + jato de baixos níveis vindo da Amazônia + frentes frias, em camadas 3D.
  3. *Are There Really More?* — 92 em 2025 (recorde), 81 até julho de 2026; viés de detecção (celular, PREVOTS, radares) × aumento real.
  4. *The El Niño Factor* — El Niño forte com pico previsto para out–dez/2026 (NOAA/CPC); 7 tornados em 6 dias (2–7/11).
  5. *A Pattern, Not a Fluke* — ciclones de 2023, enchente do RS em 2024, Rio Bonito do Iguaçu (nov/2025), F4 de Piraí do Sul (ago/2026); a escala dos eventos no mesmo mapa.
  6. *What Comes Next* — temporada até dezembro; como funciona o alerta; o que fazer.
- **Fontes de imagem permitidas:**
  - GOES-19 (NOAA, domínio público) do sistema em 04/11;
  - Sentinel-2 antes/depois de Chapecó (Copernicus);
  - malhas IBGE + DEM;
  - fotos da Defesa Civil SC/CBMSC **com autorização**;
  - Agência Brasil conferida foto a foto;
  - manchetes recriadas (CNN Brasil, Climatempo, Band) com data.
- **Fontes de texto:** [Climatempo (El Niño × tornados, nov/2026)](https://www.climatempo.com.br/noticia/el-nino/relacao-do-el-nino-com-os-tornados-no-sul-do-brasil-no-inicio-de-novembro-de-2026), [Agrolink (temporada histórica)](https://www.agrolink.com.br/noticias/por-que-o-sul-do-brasil-vive-temporada-historica-de-tornados-em-2026_518021.html), [Poder360 (Chapecó/Xanxerê)](https://www.poder360.com.br/poder-brasil/tornados-atingem-duas-cidades-de-sc-durante-temporais-no-sul/), [CNN Brasil (5 tornados em 1 semana)](https://www.cnnbrasil.com.br/nacional/sul/cinco-tornados-atingem-a-regiao-sul-do-brasil-em-menos-de-uma-semana/), [Wikipédia: tornados na América do Sul em 2026](https://pt.wikipedia.org/wiki/Lista_de_tornados_na_Am%C3%A9rica_do_Sul_em_2026) (números a conferir no PREVOTS/MetSul antes do roteiro).

**Antes da fase 2 (regra 7):** amostra de ~20–30 s do capítulo 1 no estilo 3D (Remotion, custo US$ 0) para o Rodrigo aprovar.

**O que medir (3 longos + 6 Shorts em 30 dias):**
| Métrica | INVESTIR | DESCARTAR |
|---|---|---|
| Views do longo em 14 dias | média ≥ 5 mil **ou** 1 vídeo ≥ 30 mil | média < 1,5 mil e nenhum > 5 mil |
| % assistido (longo 10–12 min) | ≥ 40% | < 25% |
| CTR (Studio) | ≥ 4% | < 2% |
| Shorts | 1 ≥ 100 mil | todos < 5 mil |
| Render por vídeo | ≤ 4 h | > 6 h sem saída (GPU) |
Também comparar Q × E × R (qual tipo segura melhor) e o piloto en × a versão pt.

## Limitações
- Views/mês de canal com 2–3 semanas de vida (Explica no Mapa, Além do Mapa, Chão do Sul) são infladas pelo arranque.
- Os números de mês e ano da busca incluem Shorts e edits; as tabelas de canais separam longos (> 3 min) de Shorts.
- RPM é faixa de referência do playbook, não dado de canal.
- Instagram/TikTok não medidos (sem acesso); a licença atual da Agência Brasil não foi confirmada na fonte primária.
- `youtube.garimpo_canais` não foi gravado (o brief limita o job a esta pasta). Gravar quando o Rodrigo decidir.

## Arquivos
- `dados/busca.jsonl`: 53 consultas × 3 ordens, 3.508 resultados.
- `dados/videos_api.json` (2.426 vídeos) e `dados/canais_api.json` (1.519 canais).
- `dados/canais_nicho.json`: 48 canais com uploads, mediana e cadência.
- `dados/canais_ranking.txt`, `dados/demanda.json`, `dados/autocomplete.json`.
- `dados/gtrends.json` (web) e `dados/gtrends_youtube.json`.
- `scripts/`: buscar, enriquecer, demanda, canais, autocomplete, gtrends.
- Vídeos assistidos (`tools/watch.py`, assets fora do git em `pesquisa/tendencias/assets/2026-11-08/`): CMHf4Cqpcrs (Mundo Entrópico), TaPes6ajs7Q (Natureza em Fúria), 31X-FKRZA2o (Ciência Todo Dia), ZVgiR9yIcGo (Um Documentário), wsYvujpyi28 (AntigamenteBR), xpBOF8FXXHM (Chão do Sul), eJf9VSZ2Ch4 (Disasters Explained), vfIaNeGVaVo (The Last Day), dLzMzsfPj-k (SkyWhisper, hit) e EEZU2b2kwLg (SkyWhisper, flop).
- Hooks literais [O]:
  - Um Documentário: "Era 11 de março de 2011, duas e quarenta e seis da tarde… Em menos de 40 minutos, uma das mais antigas comunidades pesqueiras do Japão será apagada";
  - The Last Day: "At 8.37 in the morning on August 26th, 2026, a wall of ice, the size of a small mountain, let go";
  - Disasters Explained: "Most people think every tornado looks the same. They don't";
  - Ciência Todo Dia: "Existe uma crença popular de que tornados não acontecem no Brasil, mas isso é absolutamente falso".
- Padrão [O]: o hook é data + hora + número, e a promessa vem "minuto a minuto".
