# Nicho E: público 50+/60+ (benefícios, nostalgia, saúde, homens 50+)

28/11/2026. Analista de Tendências. **[O]** = observado (API/yt-dlp/descrição/thumb), **[E]** = estimativa, **[H]** = hipótese.
Base: `canais-novos.csv` + varredura nova de 30 buscas em 6 idiomas (`~/cache/oport/E/mes.json`, 434 vídeos ≥ 40 mil, 316 canais, 37 na regra de ouro) + 25 buscas de saturação "este mês" (`~/cache/oport/E/sat.out`). Custo: US$ 0, cerca de 120 unidades da Data API.
**Limite de hoje:** o `watch.py` falhou nos 4 vídeos (`LOGIN_REQUIRED`: o YouTube pediu login ao WARP). Não houve transcrição nem frames. O formato abaixo vem de **thumb + descrição + capítulos [O]**. Ritmo de corte e estilo do vídeo inteiro ficam como **[H]**.

## Veredito curto
| Sub-fórmula | Decisão | Idioma | Por quê |
|---|---|---|---|
| **(1) Benefícios/aposentadoria por país** | **TESTAR (principal)** | **de** (2º: fr) | Melhor par RPM × concorrência: Thomas Becker tem 2,4 mi em 6 semanas com mediana de 79 mil. O en está saturado de fazendas e o produto (checklist/PDF) é natural. |
| (2) Nostalgia "coisas dos anos 60/70" | TESTAR (secundária, baixo risco) | fr (2º: es) | Demanda real e risco baixo. O fr está quase vazio, mas fica perto da bolha "como era viver" (decisão do historia-ptbr de 28/11). |
| (3) Saúde 60+ | **DESCARTAR** | — | YMYL alto, cheio de "Dr." fictícios com mediana de 100 a 600 views. Sem médico real não há como competir. |
| Psicologia masculina 50+ (extra) | Só contexto | en | 8+ canais novos em 6 semanas, molde muito copiado. |

---

## 1. Canais da regra de ouro (1º vídeo ≥ 28/07/2026, ≤ 20 vídeos) [O]
vm = views/mês estimadas (total ÷ idade × 30). Mediana só de vídeos > 3 min.

### (1) Benefícios / aposentadoria
| Canal | Idioma | 1º vídeo | Vídeos | Views | Inscr. | vm | Mediana | Melhor vídeo | Dur. | Cadência |
|---|---|---|---|---|---|---|---|---|---|---|
| [Thomas Becker](https://www.youtube.com/channel/UCHBOEwxgRE2da7Lrc6IeSjA) | de | 17/10 | 14 | 2,40 mi | 6,1 mil | 1,72 mi | **79 mil** | [Vor 1967 geboren? 4 Renten-Änderungen…](https://youtu.be/OtLL-E3Lnec) 941 mil | 12–20 min | diária (14 em 15 dias, depois parou em 01/11) |
| [Rentenblick](https://www.youtube.com/channel/UCY5i7n_I1chn0xdRr-jJcCA) | de | 30/10* | 15 | 543 mil | 3,4 mil | 569 mil | 8,9 mil | [Ihr Bankkonto wird gesperrt, wenn Sie sterben…](https://youtu.be/CoS8lnG7kiM) 212 mil | 11–16 min | dia sim, dia não |
| [Clever im Alter](https://www.youtube.com/channel/UCZpv5mQhAZLyHLuwbft-yIQ) | de | 01/11 | 12 | 361 mil | 4,0 mil | 417 mil | 4,6 mil | [Rentenreform 2027: Alle Änderungen…](https://youtu.be/knryb4uv0GQ) 232 mil | 14 min | ~3/semana |
| [Retraite & Droits](https://www.youtube.com/channel/UCysF_GFoCU4rO7xPA6BQY4w) | fr | 19/10* | 17 | 942 mil | 8,1 mil | 708 mil | 10,9 mil | [RETRAITÉS 60+ : RÉCLAMEZ CES AIDES CACHÉES…](https://youtu.be/8NzkgR67ZSo) 386 mil | 15–30 min | dia sim, dia não |
| [Retraite Direct](https://www.youtube.com/channel/UC7wfiZ1wemjp-qtI_ywJcjw) | fr | 30/10 | 21 (>20) | 373 mil | 1,1 mil | 400 mil | 2,5 mil | [Retraite : 7 démarches avant le 31 décembre](https://youtu.be/quTxspFTibI) 174 mil | 10 min | diária |
| [Pensión Informada](https://www.youtube.com/channel/UCYzu__TmsX1tvySSwOOieJg) | es-MX | 03/11 | 25 (>20) | 1,26 mi | 10 mil | 1,53 mi | 2,4 mil | [¡URGENTE pensionados IMSS e ISSSTE! Desde el 1 de DICIEMBRE…](https://youtu.be/2MmlJ5xS5tw) 902 mil | 13 min | 1+/dia |
| [Gonzalo – Finanzas Personales](https://www.youtube.com/channel/UCXibL6R8-9ckLUrCpBJXzqA) | es-ES | 22/10 | 16 | 966 mil | 3,0 mil | 784 mil | 29 mil | [Tu PENSIÓN en 2027 según quién gane…](https://youtu.be/_oW2awi41gk) 367 mil | 11 min | 3/semana |
| [Daniel Novak](https://www.youtube.com/channel/UCpIqRNzsRHgOnzNWnogEfSQ) | en-US | 29/10 | 14 | 342 mil | 1,2 mil | 346 mil | 324 | [Social Security Just Changed for Anyone Born Before 1966…](https://youtu.be/v8h_vdArVgg) 299 mil | 16 min | diária |
| [The Harbor](https://www.youtube.com/channel/UCOl_g-N1Hseu9D1avMvAdcw) | en-US | 24/10 | 19 | 457 mil | 803 | 394 mil | 257 | [BREAKING: Congress Just Voted to Erase "Full Retirement Age"…](https://youtu.be/B4tpoUmzEmU) 218 mil (**provável desinformação**) | 14 min | diária |
| [José Aposenta Brasil](https://www.youtube.com/channel/UCh_U3EjyVSxGxlzjOn9SOlw) | pt-BR | 28/10 | 17 | 379 mil | 2,8 mil | 370 mil | 984 | Alugar ou comprar casa depois dos 60, 149 mil | 20 min | diária |

\* O 1º upload dos dois é um vídeo **em inglês fora do tema** (jardim em estacionamento; xadrez siciliano): canal comprado ou reaproveitado [O].
Fora da regra, mas com tração: The Nest Egg Decoded (en, 26 vídeos, 2,6 mi), Pensioners First UK (30 vídeos, mediana 489), Alex Explains (22, mediana 110), Pensioni 24 (it, 23 vídeos, 405 mil).

### (2) Nostalgia
| Canal | Idioma | 1º vídeo | Vídeos | Views | Inscr. | vm | Mediana | Melhor vídeo | Dur. |
|---|---|---|---|---|---|---|---|---|---|
| [Kohleofen & Kaffeemühle](https://www.youtube.com/channel/UC_CN_vgVYhIMAQgXcVCyknQ) | de | 15/10 | 16 | 835 mil | 2,2 mil | 574 mil | 11,7 mil | [Deutschland früher: 20 Dinge der 60er, die nur noch Ältere verstehen](https://youtu.be/H0wiiH7lMDQ) 531 mil | 10–35 min |
| [Old Grafters](https://www.youtube.com/channel/UCdDykiRZAKy-RNKw5Jes9jQ) | en-GB | 16/11 | 7 | 542 mil | 1,4 mil | 1,40 mi | **60 mil** | [What Went On at Every 1970s British Building Site…](https://youtu.be/cG_EixxswIA) 312 mil | 15–18 min |
| [Lost American Christmas](https://www.youtube.com/channel/UCndeMPkyAR2HU2uYDcWuW9g) | en-US | 22/10 | 16 | 855 mil | 2,8 mil | 701 mil | 27 mil | 25 FORGOTTEN Things Every 1960s American Christmas Had…, 289 mil | 40 min |
| [Our Parents' Britain](https://www.youtube.com/channel/UCOidH_6d_lxhCYb-q2q4obg) | en-GB | 13/11 | 7 | 216 mil | 813 | 442 mil | 12,5 mil | 25 Things Every 1960s British Mum Did… Banned Now, 135 mil | 19 min |
| [Rerun Lane](https://www.youtube.com/channel/UCu8OH99n74zy4JIo6mjpEHw) | en-US | 13/11 | 14 | 272 mil | 1,1 mil | 561 mil | 7,5 mil | Everyday Things From 1970s America…, 81 mil | 11 min |
| [3 Hours of Growing Up in America](https://www.youtube.com/channel/UCnNx-w98Kdx7oeCKUSCxzHw) | en | 29/10 | 10 | 201 mil | 1,0 mil | 220 mil | 22 mil | 100 Things… Poor in 1960s/70s (3 HOURS), 44 mil | 185 min |
| [Dominiverso](https://www.youtube.com/channel/UCORRPsAc9cDR_b8AGa-YU3Q) | es (RD) | 06/11 | 12 | 237 mil | 528 | 328 mil | 11 mil | 20 PRODUCTOS… República Dominicana… Años 70, 121 mil | 37 min |
| [Así Éramos de Verdad](https://www.youtube.com/channel/UC_fVrwXh7b1_ZsryfX4Ypng) | es-ES | 01/08 | 18 | 437 mil | 965 | 111 mil | 10 mil | España en 1975: por qué el domingo era sagrado, 114 mil | 22 min |
| [Die Motorradjahre](https://www.youtube.com/channel/UCMJ42Ra3yBZYp0kSJFGKlzw) | de | 08/10 | 8 | 496 mil | 1,1 mil | 296 mil | 20 mil | Die Motorradkultur der 70er Jahre…, 275 mil | 20 min |
| [Note di Nostalgia](https://www.youtube.com/channel/UCHGPTzOkGX1pJUEREN-PboQ) | it | 30/10 | 8 | 291 mil | 592 | 313 mil | 16 mil | I 10 Gruppi Italiani… Anni '60, 202 mil | 23 min |
| [MÉMOIRE RETROUVÉE](https://www.youtube.com/channel/UCX4dDj7Ok1yht0gyE0hcfHg) | fr | 22/11 | **1** | 77 mil | 207 | — | 77 mil | [Grandir en France dans les années 60 et 70…](https://youtu.be/rMdOwLxz55U) 77 mil em 6 dias | 12 min |

Na janela, mas com > 20 vídeos (sinal forte de demanda): **[Cuando México Fabricaba de Todo](https://www.youtube.com/channel/UCtWtk6_Ph2EoHamCiI00lSg)** (es-MX, criado em 27/07, 79 vídeos, **9,86 mi**, mediana dos últimos 50 = 38 mil, "30 MODAS EMBLEMÁTICAS DE LOS 80S…" 2,26 mi), **[La España que Fuimos · Años 50](https://www.youtube.com/channel/UCEz8r-1a0G1ZqQwN0EjgL4g)** (es-ES, criado em 31/10, 27 vídeos, 1,57 mi, [No teníamos nada: la vida en un pueblo de 1950](https://youtu.be/90mHCmJq8EI) 685 mil, país do canal = DE), [Memória Desbloqueada](https://www.youtube.com/channel/UC5YQ52VqREna8ivc8acsKeQ) (pt-BR, 24 vídeos, **4,1 mi**, ["Como Era a Vida no Brasil em 1975?"](https://youtu.be/fpBXVH13P6k) 1,0 mi), [Quando Brasil fabricava tudo](https://www.youtube.com/channel/UCQWIynbncrfRhfPzZF8y9tQ) (50 vídeos, 1,88 mi), Main Street Years (en, 26, 1,0 mi), Lost American TV Nights (21, 790 mil), Canada Rewind (23, 578 mil).

### (3) Saúde 60+
| Canal | Idioma | 1º vídeo | Vídeos | Views | vm | Mediana | Melhor vídeo |
|---|---|---|---|---|---|---|---|
| [Liesa Harte, M.D.](https://www.youtube.com/channel/UCQspUu3C3ZvWgL9pQ99wkYg) | en | 11/10 | 20 | 3,45 mi | 2,17 mi | 24,7 mil | [6 Hidden Triggers of Sudden Decline After 70](https://youtu.be/AQ4NxjUCL5w) 1,81 mi |
| [Tim Dyrdin](https://www.youtube.com/channel/UCzQIjWmkC8OTpbUrLuHPI8Q) | en | 03/11 | 17 | 1,26 mi | 1,54 mi | **1,3 mil** | [This Incredibly Common Vitamin Raises Cancer Risk by 82%](https://youtu.be/mZM70XttBHU) 803 mil |
| [Dr. Franklin Senior Health](https://www.youtube.com/channel/UCPjG4ZRBkiO1y_vHlnj8jIg) | en | 27/09 | 9 | 1,12 mi | 548 mil | 4,8 mil | He Died In His Sleep From Doing This…, 637 mil (128 mil inscritos com 9 vídeos: estranho) |
| Senior Mobility | en | 16/10 | 15 | 479 mil | 339 mil | 15 mil | exercício na cama, 122 mil |
| Despensa de la Abuela | es-CL | 29/10 | 10 | 399 mil | 404 mil | 3,3 mil | ¿Más de 60? 20 alimentos baratos…, 223 mil |
| Arte de la Longevidad, Dr. Marco Mayor, Fuerza Después de los 60 | es | 09–11/2026 | 5–17 | 220–340 mil | — | 188–16 mil | — |
Fora da regra (> 20 vídeos), todos de 10/2026: Secretos de la Longevidad (3,5 mi, **mediana 4 mil**), Sabiduría y Salud 60+ (2,5 mi, **mediana 2,4 mil**, 1 vídeo de 2,08 mi), Dr. Álvaro Valdés (mediana 510), Dr. Cale "Médico Senior" (mediana 134), Dr. Elias (395), Dr. Tomás Aranda (590), Pablo Hernández Senior (501), Dr Bertrand · Bien Vieillir (fr, mediana 3,1 mil), Dr. Lorenz Falkenberg (de).

### Saturação: canais novos (desde 08/2026) por idioma [O]
| Sub-fórmula | en | es | pt | fr | de |
|---|---|---|---|---|---|
| Benefícios | **≥ 9** (fazendas, mediana < 1 mil) | 4–5 (MX + ES) | 1–2 (+ advogados antigos fortes) | **2** | **3** |
| Nostalgia | **≥ 10** | 5–6 | 4 | **1–2** | 4 (só 1 com tração constante) |
| Saúde 60+ | ≥ 6 | **≥ 12** ("Dr." fictícios) | 3 | 1–2 | 2–3 |

---

## 2. Formato observado
### (1) Benefícios: **mesmo dono em fr e de (sinal forte)** [O]
Retraite & Droits (fr) e Rentenblick (de) publicam a **mesma pauta traduzida, quase no mesmo dia**:
- "Votre Compte Bancaire Est Bloqué à Votre Décès — Sauf Si Vous Remplissez Ce Formulaire Gratuit" (28/10) = "Ihr Bankkonto wird gesperrt, wenn Sie sterben — außer Sie füllen dieses kostenlose Formular aus" (03/11);
- "RETRAITÉS 60+ : RÉCLAMEZ CES AIDES CACHÉES…" = "RENTNER 60+: Beantragen Sie diese versteckten Hilfen…";
- "ARRÊTEZ DE PAYER CES 5 FACTURES" = "HÖRT AUF, DIESE 5 RECHNUNGEN ZU ZAHLEN"; "4 démarches avant le décès de votre conjoint" = "4 Dinge regeln, bevor Ihr Ehepartner stirbt"; "Prendre l'avion après 60 ans ? 7 avantages" = "Fliegen ab 60? 7 versteckte Vorteile".

Thomas Becker (de) tem "Neue A7- und Autobahn-Regeln", "EZB-Warnung" e "Fliegen ab 50"; o Retraite & Droits tem "A7 et autoroutes" e "Banque de France avertit". Ou é a mesma operação, ou é um molde copiado. Em en, o "Born Before 1966/1967" aparece em Daniel Novak, Pensioners First UK, Epic Real Estate (3,8 mi) e Wise Flys. Ou seja: **é uma fórmula multilíngue em escala**, e o en já foi tomado.
- **Título:** gatilho de grupo + perda + urgência: "Vor 1967 geboren?", "RETRAITÉS 60+", "…bevor es zu spät ist", "Gute Nachricht für Rentner: 3 Zahlungen…", "Die Regierung warnt alle Rentner…".
- **Thumb [O]:** faixa amarela/preta com texto grande + **rosto real de político** (Macron, Merz, gerados ou recortados) + bandeira + documentos oficiais (formulário de aposentadoria, Carte Vitale), ou um "especialista" de terno (Rentenblick) com seta para o "KONTOFORMULAR". O Thomas Becker põe a lista de grupos de ano na própria thumb ("Gruppe 1 (1959 & früher)…").
- **Hook (da descrição, que espelha a abertura) [O]:** Becker: *"Nehmen Sie Ihre Renteninformation und schauen Sie auf Ihr Geburtsjahr. 2027 teilt genau dieses Jahr die Menschen… in vier Gruppen."* Retraite & Droits: *"Vous avez 60 ans ou plus ? De l'argent vous attend peut-être déjà dans le système, et personne ne viendra vous prévenir."*
- **Estrutura [O]:** lista numerada (3–12 itens), com valor em € de 2026, quem tem direito e a "démarche exacte"/o formulário para cada um. Capítulos na descrição; fecho com "à partager en famille".
- **Visual [H]** (frames indisponíveis hoje): slideshow de imagens IA fotorrealistas + cartões de texto/valores. **Duração:** 11–27 min.
- **Monetização extra [O]:** Thomas Becker vende "persönlicher Renten-Check + Rentenfahrplan als PDF" (renteundgeld.de). **Isso valida o produto.**

### (2) Nostalgia [O]
- **Título:** "Deutschland früher: 20 Dinge der 60er, die nur noch Ältere verstehen" / "SOLO LOS QUE VIVIERON EN LOS 80S RECUERDAN ESTOS 30 OBJETOS…" / "Como Era a Vida no Brasil em 1975?" / "…(You'd Be Sacked for It Now)". O padrão é **número + década + "só quem viveu"/"proibido hoje"**, ou "Como era a vida em [ano]".
- **Thumb:** foto IA **fotorrealista "de época"** (menina com leiteira em rua alemã; menino mexicano com pião), com 2–4 palavras gigantes ("20 DINGE DER 60ER", "ASÍ ERA EN LOS 60s", "SACKED FOR IT NOW").
- **Hook (descrição):** Old Grafters: *"Monday morning, February 1973. Frost on the scaffold boards, a mixer that won't start, and a fire already going in an old oil drum."* (cena sensorial). Kohleofen: lista do que vai aparecer (Wählscheibentelefon, Milchkanne, Testbild…).
- **Estrutura:** contagem de 15–30 itens com capítulos de ~30 s; CTA "qual número trouxe lembranças? comente", que gera **pauta vinda dos comentários** (o Old Grafters já fez "What We Left Out… (You Told Us)").
- **Duração:** de 10–17 min (de/en-GB) a 25–35 min (es/pt). Cuando México cita fontes (Archivo General de la Nación).
- **Sinal ruim [O]:** Kohleofen teve 1 vídeo de 531 mil e depois caiu: os últimos 4 têm 627–2.806 views. A tração depende de "acertar a década/objeto" (vídeo-loteria).

### (3) Saúde 60+ [O]
- Molde "Doctor Explains / Un UROLOGUE RÉVÈLE / ¿Tienes más de 60? 7 errores con los huevos que envenenan…": medo + alimento/remédio + idade.
- **Liesa Harte:** a thumb mostra uma mulher fotorrealista de jaleco ("FINE… THEN NOT"). Existe uma médica de família real com esse nome nos diretórios ([Zocdoc](https://www.zocdoc.com/doctor/liesa-harte-md-408802?LocIdent=206438), [IFM](https://www.ifm.org/practitioners/liesa-harte-md/)), mas o canal foi criado em 2023, só começou a postar em 10/2026, tem país = PT e vende toolkit de US$ 27 na stan.store. **Não deu para confirmar se o rosto/voz é avatar IA** (sem frames hoje). Seja como for, o modelo depende de **credencial médica**, que não temos.
- Em es, os "Dr. X, Médico Senior", com mediana de 100–600 views e 22–30 vídeos em 5 semanas, são fazendas de persona médica fictícia.

### Extra: homens 50+ [O]
[Men After 50](https://www.youtube.com/channel/UCjr_qN5gPwtzIYrSMJMuPXw) (en, 14/11, 11 vídeos, 818 mil, mediana 21,7 mil, [Why Men Over 50 Cut Everyone Off](https://youtu.be/MPS2OCRRB2c) 367 mil): **cartum 2D** (homem grisalho de traço grosso) + **história fictícia declarada** ("Ray, 61, is alone at a diner counter…"; *"fictional characters in an original illustrative story"*) que explica a "psicologia". O formato é bom e produzível, mas há ≥ 8 clones em 6 semanas (Life After 60 With Gus, Gentleman After 60, The Desire Blueprint, Capital Underworld, Leverage Doctrine, Marcello Rossi, Mia Relationship Talks…).

---

## 3. Mesma fórmula nos 5 idiomas (busca "este mês", vídeos > 3 min, top 60) [O]
| Busca | ≥ 100 mil (canais) | ≥ 500 mil | Leitura |
|---|---|---|---|
| en "social security changes 2027" | 20 (13) | 6 | demanda enorme, dono antigo (Epic Real Estate 3,8 mi) + fazendas |
| es "pensionados IMSS cambios" | 6 (5) | 1 | títulos idênticos em 3 canais ("¡URGENTE pensionados IMSS e ISSSTE! Desde el 1 de DICIEMBRE…") = clones |
| pt "aposentados INSS 2027 novidades" | 9 (6) | 1 | dominado por advogados com rosto (Victor Leon, 697 mil) |
| fr "retraite décembre 2026 changements" | **0** | 0 | top: 72 mil (canadense), 22 mil Retraite & Droits: **aberto, mas a demanda via busca é menor** |
| de "Rente Dezember 2026" | 1 (Finanzfluss 193 mil) | 0 | aberto; a demanda vem por recomendação (Becker 941 mil) |
| en "1970s nostalgia" | 26 (24) | 4 | saturado |
| es "cosas de los años 70 que desaparecieron" | 3 (2) | 0 | concentrado em Cuando México + Memoria Vintage (CH, 206 vídeos, 16,5 mi) |
| pt "como era a vida nos anos 70" | 12 (9) | 2 | muita demanda, puxada por canais es e Memória Desbloqueada |
| fr "la vie dans les années 60" | 1 | 0 | quase vazio: MÉMOIRE RETROUVÉE 77 mil com 1 vídeo; La France Quotidienne d'Avant (desde 03/2026, mediana 5 mil, 380 mil no melhor) |
| de "so war das Leben in den 60er Jahren" / "DDR Alltag früher" | 0 / 0 | 0 | quase vazio pela busca, mas Kohleofen fez 531 mil |
| en "seniors over 60 health tips" | 25 (21) | 4 | saturado |
| es "mayores de 60 alimentos" | 3 | 1 | saturado de fazendas com mediana baixa |
| de "ab 60 Ernährung Senioren" | 0 | 0 | top: 27 mil |

**Idioma aberto:** benefícios → **de** (sobretudo) e **fr**. Nostalgia → **fr** e **de** (oferta pequena, mas a demanda via busca também é menor); es tem a maior demanda, porém com clones e RPM baixo.

## 4. RPM e receita [E]
Fontes divergem até 2×, então use a ordem de grandeza. Tabela da fábrica (`playbooks/garimpo-tendencias.md`: finanças en US$ 6–12; fatores pt 0,25–0,35×, es 0,25–0,4×, fr 0,5–0,7×). Para finanças/aposentadoria 60+ nos EUA: US$ 25–45 em finanças pessoais e US$ 33–50 em Medicare/seguros, com pico em nov/dez ([fluxnote, US RPM by niche 2026](https://fluxnote.io/guides/us-youtube-rpm-by-niche-2026); [fluxnote finance 2026](https://fluxnote.io/guides/youtube-rpm-finance-niche-2026), blogs de fornecedor, otimistas). Por país: DE/FR acima de ES e muito acima de MX/BR ([Dynamoi, 11/2025–11/2026, amostra de música](https://dynamoi.com/data/youtube-adsense-rpm.html): US 4,66 · ES 1,32 · DE 1,19 · FR 1,03 · MX 0,23; [Fluxnote por país](https://fluxnote.io/guides/youtube-rpm-by-country): DE 3–8, FR 4–6,5, ES 3–5,5, BR 0,8–3, MX 0,8–2,5).

| | en (US/UK) | de | fr | es (ES/MX) | pt-BR |
|---|---|---|---|---|---|
| Benefícios/aposentadoria | 8–25 | **5–12** | 4–9 | 1–4 (ES) / 0,5–1,5 (MX) | 0,8–2 |
| Nostalgia 60+ | 3–7 | 2–5 | 2–4 | 0,6–2 | 0,5–1,5 |
| Saúde 60+ | 6–15 | 4–9 | 3–7 | 0,6–2 | 0,5–1,5 |

**Receita de referência:** Thomas Becker, 1,72 mi views/mês × US$ 5–12 ≈ **US$ 8,6–20 mil/mês** [E]. Retraite & Droits, 708 mil × US$ 4–9 ≈ US$ 2,8–6,4 mil/mês [E].
**Nossa versão (de, cenário conservador = 10–20% do Becker = 170–340 mil views/mês):** US$ 0,9–4 mil/mês de AdSense [E], mais o produto. Cenário pessimista (mediana tipo Rentenblick, ~9 mil × 12 vídeos/mês ≈ 110 mil views): **~US$ 550–1.300/mês** [E].

## 5. Produção na fábrica
| | Benefícios (de) | Nostalgia (fr) | Saúde |
|---|---|---|---|
| Visual | stills IA "documentário" (casal idoso na cozinha com o Rentenbescheid, banco, Finanzamt) + **infográficos no Remotion** (valores, prazos, grupos por ano, formulário) | foto IA "de época" por item (40–60 imagens) + cartão numerado | — |
| Voz | Fish de (voz masculina madura, calma) | Fish fr (voz calorosa, 55+) | — |
| Duração | 12–16 min | 12–18 min | — |
| Custo/vídeo [E] | ~US$ 1–3 (Fish ~1 + Codex US$ 0; fal de reserva ~US$ 2) | ~US$ 1–3 | — |
| Esforço extra | **checagem factual obrigatória** em fontes oficiais (Deutsche Rentenversicherung, BMF, Verbraucherzentrale) e revisão por quem lê alemão | fidelidade de época (objetos franceses reais; o fal inventa letras) | — |

**Riscos de política**
- **Inautêntico/repetitivo (15/07/2025):** a fórmula "mesma pauta traduzida em 4 idiomas, slideshow + narração" é exatamente o exemplo de "narrated slideshows with minimal variation" ([Search Engine Journal](https://searchenginejournal.com/youtube-targets-mass-produced-content-in-monetization-update/550337/), [TechRepublic](https://techrepublic.com/article/news-youtube-ai-video-monetization-rules)). Mitigação: dado oficial do ano, exemplo calculado, infográfico próprio, sem template de texto idêntico entre vídeos.
- **Metadados enganosos / alarmismo:** "Die Regierung warnt…", "BREAKING: Congress Just Voted…" (provável falso). Isso vira strike de spam/práticas enganosas e afasta anunciante. Regra nossa: **sem urgência falsa**, só mudança com fonte e data.
- **Pessoas reais:** thumbs com Merz/Macron sintéticos exigem divulgação de conteúdo alterado realista e abrem a remoção por simulação de pessoa identificável ([YouTube Help](https://support.google.com/youtube/answer/14328491)). **Não usar rostos reais.**
- **YMYL financeiro:** é informação geral, não consultoria. Pôr disclaimer e evitar "faça X com seu dinheiro" individual [H: no RDG alemão, informar é ok, aconselhar caso a caso não].
- **Saúde:** política de desinformação médica + persona "Dr." fictícia = risco de remoção e de dano real. **Descartado.**
- **Produto:** benefícios → "Renten-Check 2027" (PDF + planilha: datas, formulários, checklist de Zuschüsse) a € 9–19. Validado pelo Becker [O]. [H] A Cakto pode não servir bem ao cliente alemão (checkout em €, IVA/UE); avaliar Digistore24/Gumroad. Nostalgia → produto fraco (álbum/quiz imprimível [H]).

## 6. Temas iniciais (benefícios, de) com evidência [O]
| # | Tema | Evidência |
|---|---|---|
| 1 | Custos que o aposentado deixa de pagar em 2027 (Rundfunkbeitrag-Befreiung, Zuzahlungsbefreiung, Grundsteuer-Hilfe…) | Becker "12 Kosten, die Rentner 2026 NICHT MEHR zahlen müssen" 673 mil; Rentenblick "5 Rechnungen" 6 mil |
| 2 | O que muda na aposentadoria em 2027 por ano de nascimento (1959–1967) | Becker [941 mil](https://youtu.be/OtLL-E3Lnec) / 62 mil; Rentenblick "vor 1966 geboren… ab Januar 2027" 58 mil |
| 3 | Conta bloqueada depois da morte: procuração "über den Tod hinaus" e Oder-Konto | Rentenblick [212 mil](https://youtu.be/CoS8lnG7kiM); fr equivalente 1 mil |
| 4 | 3 pagamentos que poucos aposentados pedem (Wohngeld, Grundrente-Zuschlag, Grundsicherung) | Rentenblick 92 mil; fr "AIDES CACHÉES" 386 mil |
| 5 | O que ninguém pode tirar de você depois dos 60 (Schonvermögen, Pfändungsschutz) | Rentenblick 93 mil |
| 6 | O que todo aposentado precisa fazer em novembro/dezembro (prazos, Steuer) | Becker 119 mil; Finanzfluss "Dezember 2026: Fristen" 193 mil |
| 7 | Rente mit 63: quando cada ano de nascimento pode sair (Abschlag freikaufen) | Becker 56 mil |
| 8 | Imposto sobre a aposentadoria 2027: quem passa a pagar | Rentenblick "STEUER 2027…" 21 mil; Becker "NETTO-Rente" 97 mil |
| 9 | Reforma da previdência 2027 explicada (Rentenpaket, Mütterrente III, Aktivrente) | Clever im Alter [232 mil](https://youtu.be/knryb4uv0GQ) |
| 10 | Quanto deixar no banco depois dos 65 (Einlagensicherung, sem alarmismo) | Rentenblick "Nach 65 nie mehr als DIESEN BETRAG" 10 mil; fr "Montant EXACT à garder à la banque" 71 mil; Becker "EZB Warnung" 137 mil |

**3 títulos-modelo (de):**
1. "Jahrgang 1959 bis 1967: Was sich 2027 an Ihrer Rente wirklich ändert"
2. "9 Kosten, die Rentner 2027 nicht mehr zahlen müssen (mit Antrag)"
3. "Konto nach dem Tod gesperrt? Dieses kostenlose Bankformular schützt Ihre Familie"

**Conceito de thumb:** bloco amarelo com texto preto grosso (2–4 palavras: "JAHRGANG 1959–67") + chips de ano/€ + ilustração IA de casal 65+ à mesa com o Rentenbescheid e um carimbo vermelho "2027". **Sem político, sem bandeira com rosto, sem "Regierung warnt".**

**Nostalgia (fr), se testar em paralelo:** "Grandir en France dans les années 60 : 20 choses que seuls les plus de 65 ans connaissent" (MÉMOIRE RETROUVÉE 77 mil com 1 vídeo); "10 goûters/jouets des années 70…" (La France Quotidienne 380 mil); "Le chantier/l'usine dans les années 70 (aujourd'hui interdit)" (Old Grafters en-GB 312 mil); "La vie dans un village français en 1955" (España que Fuimos 685 mil); "Noël dans les années 60" (Lost American Christmas 289 mil; Kohleofen Weihnachten 5,5 mil = sazonal fraco em de).

## 7. Veredito
**TESTAR, sub-fórmula (1) Benefícios/aposentadoria, em alemão** (fr como 2º idioma da mesma pauta, se o de der certo).
1. **[O]** É a única sub-fórmula em que canal novo com ≤ 15 vídeos chegou a **mediana de 79 mil** (Thomas Becker, 2,4 mi em 6 semanas) num idioma com só 3 canais novos. Em en, as ≥ 9 fazendas de Social Security têm mediana < 1 mil.
2. **[E]** O RPM de/fr de finanças 60+ (US$ 4–12) é de 3 a 10× o de es-MX/pt-BR, e há produto validado (o concorrente já vende "Renten-Check" em PDF).
3. **Condição:** checagem factual em fonte oficial + revisor em alemão + nada de urgência falsa ou rosto real. Sem isso, vira mais um clone do operador fr/de/en (sinal [O]: mesma pauta traduzida nos 3 idiomas) e fica exposto à política de conteúdo inautêntico. Teste sugerido: 6 vídeos em 3 semanas; decidir pela mediana (≥ 5 mil = seguir).

Nostalgia: **TESTAR só se o Rodrigo quiser risco baixo**, em fr. Ela encosta na bolha "como era viver" já decidida para o historia-ptbr. Saúde 60+: **DESCARTAR**.
