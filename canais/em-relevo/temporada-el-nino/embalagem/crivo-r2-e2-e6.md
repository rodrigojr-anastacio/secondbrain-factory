# Crivo em-relevo/temporada-el-nino (E2–E6 + ordem) · rodada 2 · 28/11/2026
Revisor novo (não li `crivo-r1-*` nem `EMBALAGEM-r1.md`). Escopo: E2, E3, E4, E5, E6 e "Ordem de produção e amarração". Fora: 002, E1, E7.
Conferido: videos.list de 22 ids (ke75BeTAm4w, LXQmVHzwhSU, RbVr7tI0B8g, Xt0sjkwxn4E, obG4EMWkCcA, ZSBraswH1To, yXozuH1WBV0, rMCMsa2hNBQ, yH9O9lmsS-g, B30ERcYSZho, 2i3vU4voCI8, DtODLz7niM0, 753EunXU8LM, YHODkOqUwNc, F0ZQH22Jzpg, Kvj7-dthfPI, OhSbHSI5Urc, NwI-KXTC8as, JSk7yLFyKFo, E8mEep7jN0k, xpBOF8FXXHM, GnEXgEaYz1M): **todas as views batem com o alegado (±2%)**; múltiplos conferidos no `refs.csv` (obG4/ZSBr/xpBO fora do csv, múltiplo da bíblia). Mosaicos `mosaico-outliers.jpg` e `mosaico-sugerido.jpg`; `MERCADO.md`; bíblia (README, titulo, thumb); `politicas-youtube.md`; fonte do dado de União da Vitória (`videos/002-el-nino-2026/shared/roteiro.py` b36 e `build_cues.py`).

**Problema transversal (item 1):** em quase todos os vídeos a "Demanda" prova o **tema**, não o **padrão do título**. Títulos no padrão da bíblia ("Por que [LUGAR] [anomalia]" — xpBOF8FXXHM 973.270 hoje; "O/A [coisa] que [faz]" — obG4EMWkCcA 705.477, ZSBraswH1To 114.847) passam por herança; os outros padrões (afirmação + lugar + tempo, "X, não Y", "o que … ensina", "o mapa do…") vieram **sem nenhuma referência**. Thumbs: aceito a evidência da bíblia (`thumb.md`) para `mapa-lugar`, `cena-acao`, `antes-depois` (006) e `documento-evidencia` (007, GOES), como Hipótese.

---
## E2 — Rio Iguaçu · REPROVADO (0 de 3)
**Erro de fato que derruba a promessa inteira:** a proposta diz "régua de União da Vitória (Defesa Civil PR: 2,5 → 10,42 m **em out/2026**, no 002 b36)". O b36 do 002 é **julho de 1983** ("Em 1983 … o rio Iguaçu, em União da Vitória, saiu de 2 metros e meio para mais de 10 metros"; pino "UNIÃO DA VITÓRIA · PR · JULHO DE 1983" em `build_cues.py`). Não há no repo **nenhum** dado de 2026 do Iguaçu em União da Vitória. E **2014 não foi El Niño** (a cheia de jun/2014 foi com ENSO neutro), logo "1983, 1992, 2014, 2026 — em todo El Niño forte" é falso. O `refs.csv` (542 vídeos) não tem **nenhum** vídeo com "Iguaçu/União da Vitória": demanda do lugar = 0; a demanda citada é RS/Sul genérico.

### Par A: REPROVADO — "Por que o El Niño enche o rio Iguaçu: o mapa de 1983 a 2026" + Thumb A (`mapa-lugar`)
0 ok (Iguaçu no início) · 0b n/a · 1 título ok (padrão da bíblia) · thumb ok (bíblia) · **2 falha**: "a 2026" sem nenhum dado de cheia do Iguaçu em 2026; a frase-âncora das Obrigações usa o número de 1983 como se fosse 2026 · 3 ok ("DE NOVO?" complementa) · 4 ok imaginado · 5 ok · 6 ok (59 car.) · **8 falha**: gêmea da E4-A (bacia em relevo claro + rio ciano + mancha IMERG azul + pergunta de 2 palavras), publicadas em semanas seguidas · 7 talvez (lugar sem demanda medida).
Correção: buscar a régua real de 2026 (ANA/SIMEPAR, estação União da Vitória) **antes** de manter "2026"; se não houve cheia relevante, o vídeo é "por que o Iguaçu enche no El Niño" com 1983/1992/2015-16 (conferir) e o 2026 vira a chuva IMERG. Thumb A: tirar a mancha IMERG azul ou mudar o herói (ex.: o cânion/planalto em corte lateral) para não ser gêmea da E4-A.

### Par B: REPROVADO — "O rio do Paraná que sobe 8 metros em todo Super El Niño" + Thumb B (`cena-acao`)
0 meio-falha ("rio do Paraná" confunde com o rio Paraná; Iguaçu não aparece) · 1 título ok (O/A [coisa] que [faz]) · thumb ok · **2 falha**: "8 metros" = 10,42 − 2,5 de **1983**; "em todo Super El Niño" sem dado de 1997-98, 2015-16 nem 2026 · 3 ok · 5 ok · 6 ok (55 car.) · 8 ok · foto de 2014 vendida como Super El Niño = foto errada para o caso (bíblia, granizo).
Correção: nomear o rio ("O rio Iguaçu…") e trocar "8 metros em todo Super El Niño" por um fato com régua conferida (ex.: "…que subiu 8 metros no El Niño de 1983" ou o número real de 2026); foto só de cheia em ano de El Niño, com data.

### Par C: REPROVADO — "Super El Niño: por que o oeste do Paraná foi o lugar mais chuvoso do Brasil" + Thumb C (`documento-evidencia`)
0 ok · 1 **título falha** (padrão "Por que + recorde local" sem referência) · **2 falha**: o máximo (868 mm em −24,75/−52,55) fica na bacia do **Piquiri/Ivaí**, ~80–100 km ao norte do Iguaçu, e "o lugar mais chuvoso do Brasil" não está demonstrado para o país inteiro (o cabeçalho mostra o máximo do recorte PR/MS/SP/MG); não há arquivo com esse cálculo no repo · **3 falha**: vende recorde de chuva no oeste do PR, não o Iguaçu de União da Vitória · **8 falha**: A e C dominadas pela mesma mancha IMERG sobre o PR com contorno; diferem só em 3D × plano e no texto · canibaliza a Obrigação 3 do E1 (oeste do PR encharcado pago até 1:30) · 6 ok (75 car.).
Correção: refazer o C sobre o Iguaçu (ex.: `documento-evidencia` GOES-19 IR de uma noite de temporal sobre a bacia, lição 007) e só usar "mais chuvoso do Brasil" com o cálculo IMERG do Brasil inteiro salvo na pasta.

Obrigações E2: **erradas** (frase-âncora com número de 1983 como 2026).
Par com mais chance de CTR ≥ 6% (depois de corrigido): **B** (foto real grande de rio sobre a cidade, sem texto, destoa dos globos do mosaico).

---
## E3 — Roraima × Manaus · REPROVADO (0 de 3)
Ciência: Boa Vista fica a ~2,8° N, estação seca ~dez–mar, e o El Niño agrava (1998, 2024): **certo**. Mas "Roraima seca **primeiro**" é falso **para este próprio El Niño**: o nosso 002 abre com Manaus coberta de fumaça em 09/10/2026; a seca da Amazônia central vem antes (set–nov) e Roraima vem depois (dez–mar). O ângulo verdadeiro é "Roraima seca **quando** o resto da Amazônia chove" (contrapé), que a própria promessa escreve.

### Par A: REPROVADO — "Por que Roraima seca primeiro quando chega o Super El Niño" + Thumb A (`mapa-lugar`)
0 ok · 1 ok (bíblia) · **2 falha** ("primeiro" contradiz o 002 e o calendário) · 3 ok ("ACIMA DO EQUADOR" é pista física nova e verdadeira, boa) · 4 risco: 3 palavras/16 letras a 320; testar · 5 ok · 6 ok (58 car.) · 8 ok.
Correção: T1 → "Por que Roraima seca justamente quando o resto da Amazônia chove" (≈ 64 car., mesmo padrão, verdadeiro). Thumb mantida.

### Par B: REPROVADO — "Super El Niño: o rio Branco de Boa Vista já está abaixo do normal" + Thumb B (`antes-depois`)
0 meio (Boa Vista ok; thumb sem identificador) · **1 título falha** (padrão sem referência) · **6 falha**: é notícia no título ("já está abaixo do normal"), que a bíblia veta (`titulo.md`, "Notícia sai do título"); o "abaixo do normal" ainda depende de série ANA não anexada · thumb: nov/2025 × nov/2026 no início da seca pode não mostrar diferença a 320 (há portão e plano B: ok) · 6 car. ok (65).
Correção: título no padrão da bíblia com lugar + anomalia, sem manchete (ex.: "O rio de Boa Vista que encolhe quando o Pacífico esquenta"), com a série ANA na pasta.

### Par C: REPROVADO — "Roraima, não Manaus: onde o Super El Niño começa na Amazônia" + Thumb C (`cena-acao`)
**1 título falha** (sem referência para "X, não Y") · **2 falha**: "começa" é falso (ver acima) e **desmente o 002** (Manaus) que está no ar e é a porta da playlist · 3 ok · foto: fogo de 2024 sob título de 2026 = foto genérica vendida como o caso (bíblia) se não houver foto do El Niño atual; risco · 6 ok (60).
Correção: tirar "não Manaus"/"começa"; ex.: "Roraima: a parte da Amazônia que pega fogo no verão do El Niño" (ou outro padrão com 2 referências); foto com data e legenda LUGAR · DATA.

Obrigações E3: suficientes depois de trocar "por que primeiro" por "por que ao contrário".
Par com mais chance: **A** corrigido (lugar concreto + "ACIMA DO EQUADOR" é a melhor lacuna do bloco). Demanda pt é moderada (CNN 59.875; TV A Crítica 18.462): CTR ≥ 6% é improvável aqui.

---
## E4 — Vai faltar luz? · REPROVADO (1 de 3)
Ciência/geografia: **o Iguaçu deságua no Paraná abaixo de Itaipu** (na tríplice fronteira); a água do Iguaçu não passa por Itaipu. Itaipu recebe o Paraná de cima (Grande, Paranaíba, Tietê, Paranapanema, Ivaí, Piquiri). Demanda do tema é **baixa** (`MERCADO.md`: 10 vídeos, só notícia/sobrevivencialismo).

### Par A: REPROVADO — "Vai faltar luz no Brasil com o Super El Niño?" `[MANTIDO]` + Thumb A `mapa-lugar` `[REESCRITO]`
0 ok · 1 título ok com ressalva (DtODLz7niM0 77.591, 22×; 753EunXU8LM 317.668, mas é Sacani, que o MERCADO diz não replicável; pergunta sim/não é o que a bíblia diz render menos) · **2 falha na thumb**: "Paraná/Iguaçu até Itaipu, o rio terminando na barragem" é geograficamente errado · 3 ok ("SOBRANDO?" × "vai faltar?" é a melhor tensão do bloco) · **8 falha**: gêmea da E2-A (ver E2) · 6 ok (45).
Correção: bacia do **Paraná acima de Itaipu** (ou o Iguaçu terminando nas usinas dele, Salto Caxias/Segredo) e herói diferente da E2-A (ex.: a barragem em 3D com o lago cheio, sem mancha IMERG).

### Par B: REPROVADO — "A conta de luz e o Super El Niño: o que os reservatórios mostram" + Thumb B (`documento-evidencia`)
1 título fraco (Primo Rico 1.331.030, 2,9×; Perini 1.099.498, 5,2×: "consequência econômica", canais com rosto; nenhum "conta de luz") · **3 falha**: "E A CONTA?" repete a ideia do título · thumb: bandeira de dezembro não confirmada e **sem plano B** (bandeira verde mata o conceito); bandeira + mapa = 2 focos · 6 ok (64).
Correção: texto que não repita "conta" (ex.: "QUAL COR?" se a bandeira for amarela/vermelha) e plano B escrito para bandeira verde (ex.: `documento-evidencia` com o gráfico ONS da energia armazenada Sul × Norte).

### Par C: APROVADO — "Por que o El Niño faz Itaipu verter e seca usinas do Norte" + Thumb C (`cena-acao`)
0 ok (Itaipu no título e vertedouro icônico na foto) · 1 ok (padrão da bíblia; `cena-acao` da bíblia) · 2 ok **com condição**: provar o "faz verter" com 2015-16 e 2023 (vertedouro aberto em El Niño) e dados ONS de 2026; foto com licença livre conferida (Itaipu Binacional não é CC por padrão: preferir Commons) · 3 ok · 4 ok (herói único, branco sobre verde) · 5 ok · 6 ok (58) · 7 sim: foto real espetacular no meio de globos e rostos · 8 ok vs A, mas atenção: Itaipu não pode ser o herói também da A (mesmo herói, outro ângulo = mesma thumb).
Obrigações E4: vagas em "número do ONS do dia": dizer qual (energia armazenada % por subsistema, data).
Par com mais chance: **C**.

---
## E5 — Sertão · REPROVADO (1 de 3)
### Par A: REPROVADO — "Super El Niño: a faixa de chuva que não chega ao Sertão em 2027" + Thumb A (`mapa-lugar`)
0 ok · 1 ok (O/A [coisa] que [faz], bíblia) · **2/6 falha**: afirma previsão como certeza ("não chega … em 2027"); o efeito do El Niño na quadra é probabilístico e depende do Atlântico (bíblia: probabilidade como probabilidade); a thumb usa imagem de **2016** sob título de 2027 (dado passado vendido como previsão) · 3 ok ("PAROU AQUI") · 6 car. ok (63).
Correção: "Super El Niño: a faixa de chuva que pode não chegar ao Sertão" (ou "…que foge do Sertão quando o Pacífico esquenta") e a imagem rotulada como climatologia/composição de El Niño, não 2027.

### Par B: APROVADO `[MANTIDO]` — "Por que o Sertão fica sem chuva quando o Pacífico esquenta" + Thumb B (`cena-acao`, açude, "E 2027?")
0 ok · 3 ok · 6 ok (58) · 8 ok, **desde que** a C perca o ano (ver C).

### Par C: REPROVADO — "O Sertão e o Super El Niño: o que a quadra chuvosa de 2016 ensina" + Thumb C (`documento-evidencia`, "2016")
**1 título falha** (padrão "o que X ensina" sem referência; molde vago) · 2 ok (2016 foi seca no CE) · **teto violado**: "2016" (C) + "E 2027?" (B) = ano em 2 das 3 thumbs · 3 ok · 8 ok vs A · 6 ok (65).
Correção: tirar o ano da thumb C (texto-lacuna sem número) e dar 2 referências ao padrão do título, ou trocar por padrão da bíblia (ex.: "Por que o Sertão secou em 2016 com o último Super El Niño").
Obrigações E5: suficientes.
Par com mais chance: **B** (foto real de açude, lugar no título; já aprovado).

---
## E6 — Calor do verão · REPROVADO (0 de 3)
Ciência: Sudeste/Centro-Oeste mais quentes no verão de El Niño: certo (mecanismo: frentes frias param no Sul). Demanda (notícia) alta: O POVO 423.115, CNN 223.678.

### Par A: REPROVADO — "Por que o Super El Niño esquenta o verão de São Paulo a Goiás" + Thumb A (`mapa-lugar`)
0 ok · 1 ok (bíblia) · 2 ok · **3 falha**: "MAIS QUENTE" repete a ideia de "esquenta" · thumb: MODIS LST **absoluto** no verão pinta lavouras e cidades de vermelho por igual (sem mensagem a 320); tem de ser **anomalia** · 6 ok (61).
Correção: texto com pista física nova e verdadeira, ex.: "SEM FRENTE FRIA?"; camada = anomalia de temperatura (LST ou ERA5), não valor absoluto.

### Par B: REPROVADO — "O mapa do calor do Super El Niño: onde o Brasil vai esquentar mais" + Thumb B (`cena-acao`, termômetro de rua)
**1 título falha** (sem referência; existia: Capital Financeiro "É assim que o Super El Niño vai atingir cada estado do Brasil" 972 mil, no mosaico, não citada nem conferida) · "vai esquentar mais" afirma previsão (usar a de probabilidade do INMET/CPTEC) · **6 falha**: termômetro isolado é `objeto-simbolo` que a bíblia manda **evitar**, e o termômetro de rua é o clichê da TV ("parecer notícia") · "45 °C?" condicional · 6 car. ok (66).
Correção: outra imagem (ex.: foto real grande de um lugar reconhecível de SP/Goiânia sob névoa de calor, sem termômetro) ou `numero-estatistica` sobre foto se sair recorde INMET; título com a referência conferida e "pode esquentar".

### Par C: REPROVADO — "Super El Niño: por que a serra fica fresca e a cidade ferve" + Thumb C (`antes-depois`)
**2/3 falha**: serra fresca × cidade quente é altitude e ilha de calor, **não é efeito do El Niño**; o par vende outra promessa com "Super El Niño:" de prefixo · conceito indefinido ("dia × noite **ou** cidade × serra") · "CIDADE × SERRA" repete o título · 1 sem referência · 6 ok (59).
Correção: par preso ao mecanismo do El Niño (ex.: "A frente fria que não chega a São Paulo no verão do El Niño" + antes-depois de um verão normal × verão de 2015-16 em anomalia).
Obrigações E6: suficientes.
Par com mais chance: **A** corrigido.

---
## Diferenciação entre thumbs (item 8)
- E2: A "relevo bacia, mancha azul, pergunta" / B "foto cheia, sem texto" / C "mapa plano chuva PR, número" → **A×C falha** (mesma mancha IMERG no PR).
- E3: A "relevo RR, Equador, 3 palavras" / B "satélite rio, 2025×2026" / C "foto fumaça, sem texto" → ok.
- E4: A "bacia ciano até barragem, pergunta" / B "bandeira tarifária grande, pergunta" / C "foto vertedouro, sem texto" → ok internamente; **A gêmea da E2-A**.
- E5: A "relevo NE, faixa nuvens, PAROU" / B "foto açude, E 2027?" / C "mapa plano chuva NE, 2016" → ok no eixo; **teto de ano violado**.
- E6: A "relevo SE/CO, calor, 2 palavras" / B "foto termômetro, número?" / C "LST lado a lado, X × Y" → ok no eixo; B em padrão evitado.
- Temporada: as 5 thumbs A são a mesma fórmula (região em relevo claro + mancha de dado + contorno + 1–3 palavras). Como família é aceitável, mas então B e C de cada vídeo têm de fugir dela, e duas A da mesma bacia não podem sair em semanas vizinhas. Teto da playlist (1 globo, 1 Brasil laranja×azul) respeitado em E2–E6.

## Ordem de produção e amarração: REPROVADA
A troca para o Sul na primavera (E2) e o calor/Sertão no verão está certa na ciência, mas a ordem ainda canibaliza: o E2-C vende o "oeste do PR encharcado" que o E1 paga até 1:30 na mesma semana; E2 e E4 usam a mesma bacia/Itaipu e a mesma thumb A em semanas seguidas; e o E3 ("Roraima, não Manaus", "primeiro") desmente o 002, que é a porta da playlist. Faltam datas reais (sem. 1 = qual dia?), e o E5 na semana 3 sai antes da previsão da Funceme (meados de jan.): a ressalva das Obrigações resolve, mas o E5 renderia mais logo depois dela. Sugestão: E2 e E4 em semanas não vizinhas (ou E4 sobre as usinas do Norte/Sudeste, deixando o Paraná só no E2), E2 sem o recorde do oeste do PR, E3 vendido como "contrapé" de Manaus (com card para o 002), E5 trocado de lugar com o E6 se a semana 3 cair antes de 15/01.

## Veredito: REPROVADO — rodada 2 de 3
| vídeo | pares | reprovados (elemento a corrigir) |
|---|---|---|
| E2 | 0/3 | **todos**: régua 2,5→10,42 m é de 1983, não 2026; 2014 não é El Niño; A: tirar "2026" sem dado + desgemear da E4-A; B: nomear o Iguaçu e trocar "8 m em todo Super El Niño" por fato conferido; C: máximo fora da bacia e "mais chuvoso do Brasil" sem prova, gêmea da A, canibaliza E1 |
| E3 | 0/3 | A: "primeiro" → "quando o resto da Amazônia chove"; B: notícia no título + sem referência; C: "não Manaus/começa" desmente o 002 + sem referência |
| E4 | 1/3 (C ok) | A: Iguaçu não chega a Itaipu + gêmea da E2-A; B: "E A CONTA?" repete título, sem plano B para bandeira verde |
| E5 | 1/3 (B ok) | A: previsão como certeza + imagem de 2016 sob "2027"; C: ano na thumb (teto) + título sem referência |
| E6 | 0/3 | A: "MAIS QUENTE" repete o título, LST absoluto; B: termômetro (objeto-símbolo evitado, clichê de TV) + título sem referência; C: serra×cidade não é El Niño |

Par com mais chance de CTR ≥ ~6% (depois de corrigido): E2-B · E3-A · E4-C · E5-B · E6-A. Todos **Hipótese**; o E3 e o E4 têm demanda pt baixa/moderada e dificilmente chegam a 6%.
