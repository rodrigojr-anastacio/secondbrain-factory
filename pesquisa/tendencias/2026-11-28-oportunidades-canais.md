# Oportunidades de canal novo fora da bolha (28/11/2026)

Brief: `~/workspace/referencias/BRIEF-tendencias-oportunidades-canais.md`. Só pesquisa e recomendação: nenhum canal criado e nada mudou em fábrica, backlog, timers ou banco. Custo pago: **US$ 0**. Cota da Data API: cerca de 2,5 mil unidades, sem nenhum `search.list`.

**Método**
- **Varredura ampla.** Foram 300 buscas: 46 nichos × 5 idiomas (en, es, pt, fr, de) e mais 70 buscas focadas (a lista está em `2026-11-28-oportunidades/q_all.tsv` e `q2.tsv`). A descoberta foi grátis, pela busca do YouTube via yt-dlp + WARP ("este mês", ordenado por views). O enriquecimento custou cerca de 2 unidades por canal (`scan.py`). Resultado: **883 canais com ≤ 30 vídeos e 508 dentro da regra de ouro** (1º vídeo ≥ 28/07/2026, ≤ 20 vídeos). Estão em `2026-11-28-oportunidades/canais-novos.csv`.
- **7 aprofundamentos em paralelo**, um por aglomerado. Os relatórios completos, com tabelas, links, 10 temas e riscos, estão em `2026-11-28-oportunidades/`:
  - A: novelas narradas
  - B: negócios e tech
  - C: consumo perigoso
  - D: animais e pré-história
  - E: público sênior
  - F: engenharia e formatos programáticos
  - G: reavaliação do que já foi pelo Telegram
- **Conferência própria na API em 28/11** dos números dos canais de referência: Thomas Becker, Steve Talks Food, Colossal Feats, Anatomía de un Hackeo, StickBait, PENNY, CEOzoned e Crunchy History. Bateram com os relatórios.

**Legenda:** **[O]** = observado (API, busca, thumbs, descrições); **[E]** = estimativa ou Hipótese. RPM sempre em faixa. Fontes: [AIR Media-Tech 2026](https://air.io/en/air-data-findings/which-youtube-niche-makes-the-most-money-in-2026-ranked-by-real-rpm-and-cpm), [vidIQ](https://www.vidiq.com/blog/post/most-profitable-youtube-niches), [Dynamoi por país](https://dynamoi.com/data/youtube-adsense-rpm.html), [FluxNote por país](https://fluxnote.io/guides/youtube-rpm-by-country), consultadas em 28/11/2026. Elas divergem até 2×, então use a ordem de grandeza.

**Limitação de hoje:** o YouTube passou a pedir login ("Sign in to confirm you're not a bot") para **abrir vídeos** pelo IP do WARP. A busca continua funcionando. Por isso não houve hook transcrito nem frames neste estudo. O formato veio de thumbs, descrições, capítulos e 3 quadros automáticos por vídeo. **Isso também deve afetar `watch.py`, `manada.py` e `transcrever.py` da fábrica**: fica para o orquestrador ver (cookies ou outra saída).

---

## 0. Resposta curta

| # | Ideia (nome provisório) | Idioma | Oportunidade em 1 linha | Veredito |
|---|---|---|---|---|
| 1 | **Renten-Kompass**: aposentadoria e benefícios explicados | **de** (2º: fr) | Canal de 6 semanas com mediana de **79 mil** (Thomas Becker, 2,4 mi), só 3 canais novos em de, RPM de US$ 5–12 e produto (PDF) já validado pelo concorrente | **TESTAR (prioridade)** |
| 2 | **Recalled.**: "The Deadliest X Ever Sold" | **en** | Steve Talks Food: **12,3 mi em 38 dias, 9 vídeos, mediana de 606 mil**, com a fórmula de recall histórico. pt, fr e de vazios | **TESTAR** |
| 3 | **One of One**: a máquina única do mundo | **en** | Colossal Feats: **4,45 mi com 10 vídeos, mediana de 227 mil**. Em en há poucos canais nessa fórmula (es está lotado por uma rede). Risco baixo | **TESTAR** |
| 4 | **Anatomía del Golpe**: hacks e golpes cripto | **es** | Anatomía de un Hackeo: **5 vídeos, mediana de 508 mil**, casos reais e perenes. É a única ideia perto do que já fazemos (tom investigativo) | **TESTAR** |
| 5 | **Caso Real**: terror de caso real animado | **es** | StickBait: 2,56 mi em 7 dias, cauda de 15–100 mil por vídeo. Em es ninguém faz o formato curto de um caso por vídeo. RPM baixo | **TESTAR (barato, por último)** |

**Top 1, Renten-Kompass (de):** é o melhor par RPM × concorrência de toda a varredura. Em alemão, benefícios de aposentadoria pagam de 3 a 10× o es e o pt, e o en está tomado por fazendas de Social Security com mediana abaixo de 1 mil. O produto vem junto, porque o concorrente já vende um "Renten-Check" em PDF. Condição: checagem em fonte oficial e revisão do alemão, porque o Rodrigo não lê a língua.

**Achado transversal mais importante [O]:** a **CEOzoned** foi **desmonetizada por "conteúdo inautêntico e repetitivo"** e a apelação foi negada, por volta de 27/11. O canal tinha 4,95 mi de views e fazia cartoon de IA + "The ENTIRE History of X" + vídeos quase diários ([vídeo do dono](https://www.youtube.com/watch?v=m7Otbjj1eUs)). É a política de 15/07/2025 aplicada ao nosso tipo de produção. Por isso, todas as 5 ideias pressupõem 3 coisas:
- cadência de 1–3 vídeos por semana, não um por dia;
- pesquisa própria com fonte na descrição;
- diagramas ou infográficos próprios no Remotion, sem template de texto idêntico entre vídeos.

Canal que vira fazenda é o que está sendo cortado.

---

## 1. O que o mercado mostra (aglomerados da regra de ouro, 28/11) [O]

| Aglomerado | Canais novos com tração (exemplos) | Idiomas lotados | Idioma aberto | Leitura |
|---|---|---|---|---|
| Novelas narradas com IA ("abuelo del rancho", "billionaire disguised") | Abuelos de Mi Vida (16 vídeos em 13 dias, 9,95 mi, med 522 mil), Corações da Roça (7 mi, med 721 mil), Fate Comes Back (17,9 mi) | en ~50, es ~41, pt ~19, fr ~17 | nenhum (de e it sem público) | Maior volume do YouTube agora, mas é fazenda e cai em 4–8 semanas → **descartar** |
| What-if em 2ª pessoa / "crush" | E Se? (pt, 8,2 mi), MrCoolBoy (fr, 3,7 mi), Zack Mils (en, 5,9 mi) | 60+ clones em en, pt, fr, es e de | — | Saturado, público adolescente → **descartar** |
| Negócios, tech e cripto narrados | Paper Billions (en, 6,6 mi), Anatomía de un Hackeo (es, med 508 mil), Se Lo Buscaron (es) | en ~20 (+ app que fabrica o molde) | es (formato hack), fr | → **ideia 4** |
| Consumo perigoso | Steve Talks Food (en, 12,3 mi), ToyAutopsy (en, 1,4 mi); rede "marcas do país X" (25+ canais) | "marcas do país X" em todos os idiomas | "Deadliest Ever Sold" em pt, fr e de | → **ideia 2** (só recall histórico) |
| Aposentadoria e benefícios 60+ | Thomas Becker (de, 2,4 mi, med 79 mil), Retraite & Droits (fr), Rentenblick (de) | en (Social Security) | **de, fr** | → **ideia 1** |
| Engenharia: "a máquina X" | Proezas Aéreas e Prodigios de Ingeniería (es, med 152 mil e 87 mil, mesmo dono provável), Colossal Feats (en) | es (uma rede que dubla em todos os idiomas) | **en**, de (demanda baixa) | → **ideia 3** |
| Pré-história: "fera × era" / "quanto duraria hoje" | Era Swap (en, med 138 mil), MUNDO FOSIL (es, 2,3 mi) | en (Fossil 26,6 mi) | es, fr | Reserva (RPM baixo, risco "made for kids") |
| Terror animado | StickBait (en, 2,6 mi em 7 dias); dezenas em hindi/bengali | en genérico (gigantes antigos) | **es** (caso real curto) | → **ideia 5** |
| Documentário de vida selvagem com vídeo IA | Ali Wildlife Hunt (10,3 mi em 4 vídeos), Amazing Wild Animals (7,6 mi) | redes multilíngues | — | Vídeo IA a US$ 55–90/vídeo + "slop" → **descartar** |
| Futebol explicado (es/pt) | Gol a Gol, Lógica do Fut, Cancha Allstars (med 111–191 mil) | — | — | Só contexto: RPM baixo e direito de imagem de jogador |

O CSV mostra ainda, sem aprofundar: celebridades ("How every celebrity… died", agandite 1,7 mi), sobrevivência em bonecos ("1 Year Locked in a Target"), "Every Tornado Type Explained" (Ink Frame, 1,2 mi) e recaps de anime e filme (direitos).

---

## 2. As 5 ideias

### 1) Renten-Kompass: aposentadoria, benefícios e direitos 60+ (de) · **TESTAR (prioridade)**
- **Promessa:** "o que muda no seu dinheiro de aposentado e o que você tem direito a pedir, com fonte oficial e formulário". Lista numerada com o valor em € de 2026–27, quem tem direito e como pedir. **12–16 min.**
- **Por que de, pela matriz:** en está saturado (≥ 9 canais novos de Social Security, todos com mediana < 1 mil) [O]. es-MX e pt pagam US$ 0,5–2 e estão cheios de clones e de advogados com rosto [O/E]. de tem só 3 canais novos, e o melhor tem mediana de 79 mil [O]. RPM estimado: **de US$ 5–12**, fr US$ 4–9 [E]. A ordem en → es cede aqui porque o RPM e a concorrência de de ganham com folga. **fr é o 2º idioma, com a mesma pauta.**
- **Referências [O]:**
  - [Thomas Becker](https://www.youtube.com/channel/UCHBOEwxgRE2da7Lrc6IeSjA): de, 1º vídeo em 17/10, 14 vídeos, 2,40 mi views, 6,1 mil inscritos, mediana de 79 mil; melhor vídeo: ["Vor 1967 geboren? 4 Renten-Änderungen…"](https://youtu.be/OtLL-E3Lnec) com 941 mil. Vende "Renten-Check" em PDF.
  - [Rentenblick](https://www.youtube.com/channel/UCY5i7n_I1chn0xdRr-jJcCA): de, desde 30/10, 15 vídeos, 543 mil; ["Konto nach dem Tod gesperrt"](https://youtu.be/CoS8lnG7kiM) com 212 mil.
  - Retraite & Droits: fr, desde 19/10, 17 vídeos, 942 mil; "AIDES CACHÉES" com 386 mil. **É o mesmo dono do Rentenblick** (pauta traduzida quase no mesmo dia), ou seja, a fórmula já é multilíngue.
- **10 temas, com evidência:**
  1. Custos que o aposentado deixa de pagar em 2027 (Becker, 673 mil)
  2. O que muda em 2027 por ano de nascimento, 1959–67 (Becker, 941 mil)
  3. Conta bloqueada depois da morte: procuração e Oder-Konto (Rentenblick, 212 mil)
  4. 3 pagamentos que poucos pedem: Wohngeld, Grundrente-Zuschlag, Grundsicherung (Rentenblick 92 mil; fr 386 mil)
  5. O que ninguém pode tirar de você depois dos 60: Schonvermögen (93 mil)
  6. Prazos de dezembro (Finanzfluss, 193 mil)
  7. Rente mit 63 por ano de nascimento (56 mil)
  8. Imposto sobre a aposentadoria em 2027 (Becker "NETTO-Rente", 97 mil)
  9. Reforma da previdência 2027 explicada (Clever im Alter, 232 mil)
  10. Quanto deixar no banco depois dos 65, sem alarmismo (Becker "EZB", 137 mil)
- **Títulos-modelo:**
  - "Jahrgang 1959 bis 1967: Was sich 2027 an Ihrer Rente wirklich ändert"
  - "9 Kosten, die Rentner 2027 nicht mehr zahlen müssen (mit Antrag)"
  - "Konto nach dem Tod gesperrt? Dieses kostenlose Bankformular schützt Ihre Familie"
- **Thumb:** bloco amarelo com texto preto grosso ("JAHRGANG 1959–67") + chips de ano e € + ilustração IA de casal 65+ à mesa com a carta da Rentenversicherung e um carimbo vermelho "2027". **Sem rosto de político e sem "Regierung warnt".**
- **Custo por vídeo [E]:** US$ 1–3, com voz Fish em alemão (voz madura e calma), Codex e infográficos no Remotion. O custo real está na checagem: fonte oficial (Deutsche Rentenversicherung, BMF, Verbraucherzentrale) e revisão do alemão (tradução reversa + uma 2ª IA revisora; o ideal é um revisor nativo pago por vídeo, decisão do Rodrigo).
- **RPM e potencial [E]:** US$ 5–12. Cenário conservador, com 10–20% do Becker: **US$ 0,9–4 mil/mês** de AdSense. Cenário pessimista: US$ 550–1.300/mês. Mais o produto "Renten-Check 2027" (PDF + planilha, € 9–19). A Cakto pode não servir para cliente alemão (euro, IVA da UE); avaliar Digistore24 ou Gumroad.
- **Riscos:**
  - YMYL financeiro: informar sim, aconselhar caso a caso não; usar disclaimer.
  - Urgência falsa vira spam ou "metadados enganosos".
  - Rosto sintético de político é proibido.
  - Conteúdo inautêntico: a rede fr/de já faz slideshow traduzido. A nossa diferença tem de ser a conta feita na tela e a fonte citada.
- **Teste:** 6 vídeos em 3 semanas; segue se a mediana passar de 5 mil. Detalhes em `2026-11-28-oportunidades/E-senior.md`.

### 2) Recalled.: "The Deadliest X Ever Sold" (en) · **TESTAR**
- **Promessa:** a história de produtos de consumo que mataram, queimaram ou envenenaram e foram recolhidos ou banidos. Contagem de 8–10 produtos, com ~1,5 min de história de recall para cada um. **15–18 min.**
- **Por que en:** é a 1ª opção da matriz, com demanda enorme e RPM de US$ 2–5 [E], e só 2 canais novos com tração [O]. Em es, o Jose Velasquez faz mediana de 204 mil com 4 vídeos; es pode vir depois como **faixa de áudio dublada** no mesmo canal.
- **Referências [O]:**
  - [Steve Talks Food](https://www.youtube.com/channel/UCQUd_Lz--kVbKefuk7dsKMA): 1º vídeo em 21/10, 9 vídeos, 12,29 mi, 21,9 mil inscritos, mediana de 606 mil; ["The Deadliest Candy Ever Sold"](https://youtu.be/3Ika6QR1TPE) com 6,02 mi.
  - [ToyAutopsy](https://www.youtube.com/channel/UCHdyAlYLqscSgXyR9Rf4e7Q): desde 08/11, 10 vídeos, 1,36 mi; "Deadliest Squishy and Fidget Toys" com 1,05 mi. Mesmo molde de thumb do Steve (mesmo dono? Hipótese).
  - [Crunchy History](https://www.youtube.com/channel/UCnNkV9ZvjGaPfk_QnfR8fDA): originador da fórmula, de 2025, 178 vídeos, 32,6 mi, mediana de 98 mil. **É só contexto: canal antigo.**
- **10 temas, com evidência:**
  1. Candy (6,02 mi)
  2. Snacks (2,85 mi)
  3. Fast food (1,39 mi)
  4. Squishy/fidget toys (1,05 mi)
  5. Halloween/Christmas, sazonal (804 mil / 796 mil)
  6. Cereals (606 mil)
  7. Energy drinks (550 mil)
  8. "Foods people still eat" (411 mil)
  9. Sodas (303 mil)
  10. Brinquedos e química dos anos 50, como o kit com urânio (166 mil)

  Temas ainda não feitos, para sair da manada: Kitchen Gadgets, Baby Products, Cosmetics e Christmas Lights.
- **Títulos-modelo:**
  - "The Deadliest Christmas Toys Ever Sold"
  - "The Most Dangerous Kitchen Gadgets Ever Sold"
  - "The Deadliest Baby Products Ever Sold"
- **Thumb:** fundo preto com vinheta e 3 produtos "parecidos" (sem logo real) em still life, com fumaça, rachadura ou brilho tóxico. Uma palavra minúscula com ponto ("recalled.") e 2–3 etiquetas tortas ("banned?", "toxic").
- **Custo por vídeo [E]:** US$ 1,5–3. Ilustrações de produto pelo Codex, cartelas de recall e manchetes recriadas no Remotion, voz Fish. **Sem clipe de telejornal**, que é o que o ToyAutopsy usa (risco de Content ID).
- **RPM e potencial [E]:** US$ 2–5. Com 8 vídeos/mês e mediana de 30–50 mil: **US$ 700–1.200/mês**. Um hit do nível do Steve (6 mi) rende US$ 15–25 mil num vídeo só. Produto fraco: no máximo afiliados.
- **Riscos:**
  - O formato é fácil de clonar, e o originador já dubla para es e fr.
  - Marca: falar só de recall documentado (CPSC, FDA, RAPEX), com linguagem "was recalled", e nunca dizer que um produto atual faz mal.
  - Evitar conselho de saúde.
- **Detalhes:** `2026-11-28-oportunidades/C-consumo-perigoso.md`. A variante "marcas do país X" está descartada (ver §3).

### 3) One of One: a máquina, o avião ou o objeto único do mundo (en) · **TESTAR**
- **Promessa:** um objeto real e colossal por vídeo: escala comparada a humanos, como funciona, quem consegue fabricar e por que não existe outro igual. Narração calma, **18–22 min**.
- **Por que en [O]:** na busca "biggest machine in the world" deste mês há só 5 vídeos acima de 100 mil, contra 16 em "la máquina más grande del mundo", onde es já está tomado por uma rede (Prodigios, Proezas e Ingeniería Monumental) que dubla para todos os idiomas. RPM estimado em en: US$ 4–8, contra US$ 1–2,5 em es [E].
- **Referências [O]:**
  - [Colossal Feats](https://www.youtube.com/channel/UC_iZHiSZPWNWv2U9vxVpTFg): en, 1º vídeo em 30/10, 10 vídeos, 4,45 mi, 11,5 mil inscritos, mediana de 227 mil; "Life Inside the World's Biggest Passenger Plane: 17 Hours…" com 2,49 mi.
  - [Proezas Aéreas](https://www.youtube.com/channel/UC_k66mGLal3zMqoJ98Jb9eQ): es, desde 14/10, 15 vídeos, 3,13 mi, mediana de 152 mil.
  - [Prodigios de Ingeniería](https://www.youtube.com/channel/UCXE3rfqNAs1CDIQY8E8AI6g): es, desde 13/10, 15 vídeos, 3,01 mi, mediana de 87 mil; "El motor más grande del mundo" com 830 mil.
- **10 temas, com evidência:**
  1. Motor marítimo de 2.300 t (830 mil / 657 mil)
  2. Concorde minuto a minuto (667 mil)
  3. Mi-26, o helicóptero que carregou um mamute (577 mil)
  4. Bulldozer Komatsu D575A (484 mil / 544 mil)
  5. Máquina EUV da ASML (436 mil)
  6. 17 h dentro do A380 (2,49 mi)
  7. Road train australiano (2,33 mi)
  8. Escavadeira Bagger 293 (132 mil em de)
  9. Kharkovchanka, a casa soviética sobre esteiras da Antártida (234 mil)
  10. Depressão de Qattara: o mar que o Egito quis criar com bombas atômicas (448 mil)
- **Títulos-modelo:**
  - "The World's Biggest Engine: A Grown Man Can Stand Inside One Cylinder"
  - "Only One Was Ever Built: The Machine That Ate a Mountain a Day"
  - "The Plane That Landed Before It Took Off: The Concorde Minute by Minute"
- **Thumb:** a máquina em vista 3/4 contra o céu, com pessoas e caminhões minúsculos para dar escala, luz dourada, sem texto (no máximo "2,300 T"). Um único objeto.
- **Custo por vídeo [E]:** US$ 1,5–3. Fotos de domínio público ou CC (Wikimedia, DVIDS, NASA) com Ken Burns, cortes técnicos e escala no Remotion, 20–30 recriações pelo Codex, voz Fish. O gargalo é o roteiro e a curadoria de licenças.
- **RPM e potencial [E]:** US$ 4–8. Cenário conservador: **US$ 750–1.000/mês**. Teto, no nível do Prodigios: ~US$ 10 mil/mês. Produto secundário: pôster "50 maiores máquinas em escala", afiliados (LEGO Technic, maquetes). Depois, a alavanca é a faixa de áudio multi-idioma, que a concorrência já usa.
- **Riscos (baixos):** atribuição CC BY-SA, aviso de "sem afiliação" com fabricante e nada de manchete falsa de tecno-nacionalismo (o tipo France Orbit ou Singapore Tech, que tem mediana menor e risco de "enganoso"). É documentário, mas fora de história/dossiê/mapas. Detalhes em `F-engenharia-programaticos.md`.

### 4) Anatomía del Golpe: hacks, golpes tech e cripto contados como thriller (es) · **TESTAR**
- **Promessa:** um caso real por vídeo (Lazarus/Binance, ANOM, WannaCry, Sabu, Mitnick): quem fez, como funcionou em nível conceitual (sem tutorial), como pegaram e o que muda para você. **20–28 min.**
- **Por que es [O/E]:** en está saturado (~20 canais novos e um app vendendo o molde). Em es, o formato "hack" tem só 3–4 jogadores sérios, e o melhor tem mediana de 508 mil. A matriz deu es 6,70, fr 6,35, de 6,10 e pt 5,95 (B-negocios-tech §7). **fr é o 2º idioma.**
- **Referências [O]:**
  - [Anatomía de un Hackeo](https://www.youtube.com/channel/UCOBpyosb-HzAVw4RDRbAaJQ): es-ES, desde 17/10, 5 vídeos, 3,57 mi, 24,7 mil inscritos, mediana de 508 mil; "700 IAs de OpenAI… hackearon Hugging Face" com 1,44 mi (caso real, de julho de 2026).
  - [Se Lo Buscaron](https://www.youtube.com/channel/UCM8TnNuTR8B0gswpWklvFhg): es-MX, 14 vídeos, 2,19 mi, mediana de 113 mil.
  - [UMSATZ.](https://www.youtube.com/channel/UCpEAV9XkHR52qchIEMY_oWA): de, 16 vídeos; "Wie ein 18-Jähriger 65.000.000 $ stahl" com 200 mil.
- **10 temas, com evidência:**
  1. Lazarus: como a Coreia do Norte rouba (1,1 mi; Gloam 2,58 mi)
  2. Agentes da OpenAI × Hugging Face (1,44 mi)
  3. ANOM/Trojan Shield (508 mil)
  4. Marcus Hutchins e o WannaCry (912 mil)
  5. Sabu e o fim do Anonymous (701 mil)
  6. Kevin Mitnick (977 mil)
  7. Stuxnet (265 mil)
  8. Carbanak, US$ 1 bi de 100 bancos (201 mil)
  9. KyberSwap, o garoto de 18 anos (200 mil em de, sem versão es)
  10. SIM swap de US$ 24 mi, caso Terpin (74 mil)
- **Títulos-modelo:**
  - "Así robó Corea del Norte 6.300 millones a Binance en 20 minutos | Documental"
  - "El hacker de 22 años que salvó internet… y después lo arrestó el FBI"
  - "El FBI creó su propia app para narcos y leyó 27 millones de mensajes"
- **Thumb:** fundo escuro de interface ou terminal, 1 objeto-símbolo (cofre, celular, silhueta de capuz), 2–3 palavras grandes com destaque amarelo ou vermelho, círculo num detalhe e selo "DOCUMENTAL".
- **Custo por vídeo [E]:** US$ 1,5–4. Interface editorial no Remotion (~70%) e 40–60 imagens Codex, voz Fish es-ES.
- **RPM e potencial [E]:** US$ 1,5–4 (es-ES puxa para cima). Cenário conservador: **US$ 390–2.000/mês**. Produto: guia "Cómo no perder tus cripto" (US$ 7–15) e newsletter com patrocínio de segurança ou VPN.
- **Riscos:**
  - Pessoas reais: escrever "acusado" e evitar casos que são só alegação.
  - Nada de tutorial de hack nem de previsão de preço.
  - **É a única das 5 perto do `dossie-es`** (mesmo idioma, tom investigativo). Separar visual (interface escura × HQ em tinta) e tema (dinheiro e tech × organizações). Alternativa mais barata: 1 caso (Lazarus) como EXPEDIENTE dentro do Dossier antes de abrir canal. Detalhes em `B-negocios-tech.md`.

### 5) Caso Real: terror de caso real, animado em 8 min (es) · **TESTAR (barato, por último)**
- **Promessa:** um caso famoso da cultura hispânica por vídeo (Vallecas, Isla de las Muñecas, La Llorona com origem documentada, Casa Matusita), contado como relato. Hook com resultado + regra de sobrevivência nos 15 s, 12 capítulos nomeados, **8 min.**
- **Por que es [O]:** no formato curto de um caso por vídeo não há ninguém em es (os grandes são antigos e longos, de 47–77 min), e a demanda pelos casos é de milhões (Expediente Vallecas 2,13 mi). en genérico está fechado pelos gigantes antigos.
- **Referências [O]:**
  - [StickBait](https://www.youtube.com/channel/UC1ToRh47YtHWFQuqDhEix-g): en, desde 21/11, 13 vídeos, 2,38 mi, 7,7 mil inscritos, mediana de 50 mil. O hit de 1,9 mi era uma história **já viral antes** (5,6 mi em outro canal), então o que pesa é escolher casos famosos.
  - Arándano 13: es, antigo, animados com 0,7–0,9 mi. Só contexto.
  - Skull Bat e Ajana Atanka: hi/bn, 5–6 mi com 15–19 vídeos. Prova de demanda do gênero animado.
- **10 temas:**
  1. Vallecas (2,1 mi)
  2. Isla de las Muñecas (549 mil)
  3. La Llorona (176 mil–5,2 mi)
  4. Charro Negro (236 mil)
  5. Casa Matusita, Lima
  6. Argentina paranormal (802 mil)
  7. Hospital abandonado (1,8 mi)
  8. O casamento jinn do Kuwait em es (5,6 mi em en/hi)
  9. KKN Desa Penari (64 mil)
  10. "La familia que demandó a un jinn" (267 mil)

  Os temas sem número precisam de checagem na embalagem.
- **Títulos-modelo:**
  - "Jugaron a la ouija en el colegio… 6 meses después ella murió | Caso real (Vallecas, 1991)"
  - "Le pagaron por cuidar la isla… las muñecas se movían de noche | Caso real (Xochimilco)"
  - "Una niña se sentó en su coche… y no llegó a la siguiente curva | Historia real animada (Sevilla)"
- **Thumb:** personagem com medo à esquerda, ameaça à direita, pista circulada em vermelho, 2–4 palavras amarelas e selo "CASO REAL · país/ano".
- **Custo por vídeo [E]:** US$ 1–3, com bonecos 2D (60–80 imagens Codex) e Fish com 2–3 vozes. Usa a família visual de bonequinhos, mas o nicho é outro.
- **RPM e potencial [E]:** US$ 0,7–1,5. Cenário conservador: **US$ 60–360/mês**. É o mais fraco em dinheiro e só vale por ser barato e ter espaço aberto. Produto fraco.
- **Riscos:** família viva (Vallecas): narrar o relato público com fonte, sem acusar. Evitar teologia. Um caso por vídeo, sem cadência diária. Detalhes em `G-telegram-reavaliado.md` §2.

### Reservas (não entram no top 5, mas ficam no radar)
- **Pré-história "fera × era / quanto duraria hoje" (es):** MUNDO FOSIL tem 2,31 mi e mediana de 61 mil; Era Swap (en) tem mediana de 138 mil e é feito com imagem estática + cronômetro, a ~US$ 1–1,5 por vídeo. Contra: RPM de US$ 1–2, risco de "made for kids" e clones traduzidos ao pé da letra em 4 idiomas. Ver `D-animais-prehistoria.md`.
- **Economia "Explained Like You're 5" com planilha (en, ou pt pelo produto da Cakto):** PENNY tem 22 vídeos desde 16/10, 2,16 mi e um hit de 1,16 mi, mas **mediana de 19 mil** [O]. É o subnicho onde a planilha cabe com naturalidade, mas a tração é de 1 hit só e o visual é o mesmo da CEOzoned. Hipótese: precisa de uma rodada da skill `novo-canal`.
- **Nostalgia "20 coisas dos anos 60 que só quem viveu sabe" (fr):** quase vazio em fr (MÉMOIRE RETROUVÉE fez 77 mil com 1 vídeo), mas é vídeo-loteria e encosta no "como era viver" do historia-ptbr.

---

## 3. O que NÃO recomendo, e por quê

| Oportunidade | Origem | Por que não |
|---|---|---|
| **Novelas narradas com IA** ("abuelo humillado", "billionaire disguised") | varredura 28/11 | Demanda gigante, mas são ~50 clones em en, ~41 em es e ~19 em pt; fr está ocupado e de e it não têm público. O ciclo é de 4–8 semanas (NYS Movie foi de 5,4 mi para ~5 mil). Os vídeos de 60–90 min pedem 180–300 imagens (US$ 15–40 por vídeo) com RPM es de 0,6–1,8. É o exemplo literal da política de inautêntico ("narrated stories with superficial differences") |
| **Desastres "What Navy Divers Found"** (Hadalogy) | Telegram 23 e 26/11 | Continua com 1 hit só (os 2 vídeos do Challenger = 98% das views), tema já explorado (1,14 mi em outro canal, 460 mil em es). O 5º vídeo fez 640 views. **Muda de TESTAR para DESCARTAR** |
| **"The ENTIRE History of [marca]" + produto** | radar 24/11 | **CEOzoned desmonetizada por inautêntico** (apelação negada). Só "McDonald's" tem 8 clones; The Entire War parou; Ethos posta 50 min/dia para 4–19 mil. **DESCARTAR o molde**; o lado "produto" migra para a reserva PENNY |
| **What-if em 2ª pessoa / "crush"** (What1fy, Zack Mils) | Telegram 26/11 | 60+ clones em 6 semanas nos 5 idiomas, dublagem automática ocupando o resto, público adolescente (RPM US$ 1,5–4 em en) |
| **True crime reencenado** (The Black File, DOCS 187) | Telegram 23/11 | Esfriou (últimos vídeos com 1–55 mil), já tem clone ("RED DOCS 187") e trata de pessoas reais condenadas: risco de difamação e de política |
| **Nils History / história longa** | Telegram 23/11 | Tem apresentador e cartões de papel, não dá para copiar, e está dentro da bolha. Os títulos agora destacam "(NO AI)" |
| **Born in Lore** (What If You Were Born as [personagem de game]) | Telegram 23/11 | 100% IP de terceiros (Call of Duty etc.) |
| **"Marcas do país X"** ("STOP buying these 10 milk brands") | varredura 28/11 | Fazenda de 25+ canais, quase todos de donos brasileiros, com títulos idênticos trocando o país. Usa thumb de falso telejornal com "ex-funcionária" IA e logo real (difamação). Os países-alvo pagam US$ 0,3–1 |
| **Vida selvagem com vídeo IA realista** (Ali Wildlife Hunt, Amazing Wild Animals) | varredura 28/11 | Exige vídeo IA (~US$ 55–90 por vídeo), compete com redes multilíngues e é "slop" exposto à política |
| **Xadrez programático "Chess, But…"** | varredura 28/11 | Daria para gerar quase de graça (python-chess + Stockfish + Remotion), mas são 8 clones em 18 dias, depende de comédia e tem RPM de US$ 1,5–3 |
| **Saúde 60+ / "Doctor explains"** | varredura 28/11 | YMYL alto, cheio de "Dr." fictício (mediana 100–600 views em es). Sem credencial médica real não dá para competir com segurança |
| **Tecno-nacionalismo** ("La France vient de trouver un carburant…", "Singapore just…") | varredura 28/11 | Manchete enganosa, mediana menor que a dos objetos reais e risco de "metadados enganosos" |

---

## 4. Próximos passos sugeridos (decisão do Rodrigo; nada foi executado)
1. **Escolher 1–2 ideias para a fase 1** (`playbooks/novo-canal.md`, amostras antes de gastar). Sugestão: **Renten-Kompass (de)** + **Recalled. (en)** ou **One of One (en)**. As duas en usam a mesma esteira documental e são de risco baixo.
2. Para o Renten-Kompass, antes do piloto: definir como revisar o alemão e checar se a Cakto atende cliente na UE.
3. **Desbloquear o acesso a vídeos via WARP.** O YouTube pede login desde 28/11, o que afeta `watch.py`, `manada.py` e `transcrever.py`. Talvez com cookies de uma conta descartável; é decisão do Rodrigo, porque envolve conta.
4. Todas as ideias: cadência de 1–3 vídeos por semana, fonte na descrição e diagramas próprios. O caso CEOzoned mostra que é aí que a desmonetização bate.

## Anexos
- `2026-11-28-oportunidades/canais-novos.csv`: 883 canais (508 na regra de ouro), com número de vídeos, views, inscritos, mediana, views/mês, melhor vídeo, títulos e por qual busca cada um foi achado.
- `2026-11-28-oportunidades/A-novelas-narradas.md`, `B-negocios-tech.md`, `C-consumo-perigoso.md`, `D-animais-prehistoria.md`, `E-senior.md`, `F-engenharia-programaticos.md`, `G-telegram-reavaliado.md`: os aprofundamentos, com tabelas por idioma, links e fontes de RPM.
- `2026-11-28-oportunidades/scan.py`, `q_all.tsv`, `q2.tsv`: o scanner reutilizável e as buscas usadas.
