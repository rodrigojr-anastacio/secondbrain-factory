# Em Relevo: reembalagem (título + thumb), 14/11/2026

Pesquisador: Fase 1 + Fase 2 (sem crivo). **Custo: US$ 0. `search.list`: 0** (19 buscas yt-dlp via WARP + `videos.list`/`channels.list`/`playlistItems`, cerca de 60 unidades).
Dados: `dados/em-relevo/` (`busca/*.jsonl`, `busca-enriquecida.json`, `busca-extra.json`, `medianas-canais.json` com a mediana dos últimos ≤ 30 longos de cada canal, `referencias.csv`, `nossos.json`, `scripts/`). Mosaicos: `mosaicos/em-relevo-sul.jpg` e `mosaicos/em-relevo-el-nino.jpg` (a nossa thumb atual fica no 1º quadro).
Views de 14/11/2026. "×med" = views ÷ mediana dos longos do canal (> 1 = acima da mediana). Janela ≤ 400 dias, exceto onde marcado.
**Versões conferidas:** Sul no ar = v2 (YouTube 10:23 = `video-v2.mp4` 10:22) → `longo-01/out/legendas-v2.srt`. El Niño no ar = 12:10 = `longo-02/out/video.mp4` (729,9 s) → `longo-02/out/legendas.srt` (o slot do boletim de 12/11 tem duração fixa, então os tempos valem).

---

## 1. Padrões do nicho (clima/geografia do Brasil, pt)

### Título
| # | Padrão | Referências reais (views · data · ×med) | Nota |
|---|---|---|---|
| T-A | **"Por que [LUGAR] é/tem [anomalia]?"**, lugar como sujeito, 1–2 palavras em CAIXA ALTA | [Chão do Sul "Por que a Região Sul é o OPOSTO…"](https://youtu.be/xpBOF8FXXHM) 736 mil · 24/10 · 15,4× · [Mundo Entrópico "Por que Existem Duas Guianas?…"](https://youtu.be/it5Vsv851Rc) 512 mil · 11/09 · 13,0× · [ME "Por que o RIO GRANDE DO SUL Vai Começar a ENCOLHER?"](https://youtu.be/EGVFIQtvflg) 259 mil · 23/10 · 6,6× | 44–61 car.; pergunta sem resposta; o veio mais forte em pt |
| T-B | **"O/A [coisa concreta, escondida ou invisível] que [faz algo] no [lugar]"** | [Chão do Sul "Tem um oceano escondido no Sul do Brasil que ninguém vê"](https://youtu.be/pm0Pgr5BlqA) 87 mil · 25/10 · 1,8× · [Natureza Sinistra "O EF5 de Smithville: O Tornado que Arrancou o Asfalto"](https://youtu.be/obG4EMWkCcA) 651 mil · 30/05 · 3,6× · [Um Documentário "…Yungay: A cidade soterrada por uma montanha em três minutos"](https://youtu.be/GtUfbKNR_vA) 5,3 mi · 18/08 · 6,3× | objeto que o espectador "vê" pelo título; não diz a causa |
| T-C | **"[X] NÃO é o que você pensa" / "o que ninguém percebe/conta"** | [Sou curioso?! "O El Niño de 2026 NÃO é o Que Você Pensa"](https://youtu.be/gkkqmtbOwmE) 1,1 mi · 06/10 · 4,9× · [ME "O Nordeste Não É O Que Você Pensa..."](https://youtu.be/31bbFdLrWaQ) 104 mil · 28/08 · 2,7× · apoio en: [Secrets of the Universe "Nobody Realizes What El Niño Is About To Do…"](https://youtu.be/G27YUk3pVw8) 2,3 mi · 24/10 · 23,9× | promete corrigir uma ideia; precisa de um "detalhe" real no vídeo |
| T-D | **Contraste Norte × Sul (o Brasil partido)** | [Prof. JeanGrafia "SUPER EL NIÑO 2026: por que o Norte vai SECAR e o Sul vai AFOGAR"](https://youtu.be/GnEXgEaYz1M) 150 mil · 22/05 · 6,2× · [JeanGrafia "O El Niño RACHOU o Brasil ao meio!"](https://youtu.be/BpIY4ex2u6E) 143 mil · 10/11 · 5,9× · (T-A "OPOSTO" 736 mil é o mesmo gatilho de contraste) | 2 imagens opostas no mesmo país |
| T-E | **Impacto em você / "o Brasil inteiro vai sentir"** | [Olá, Ciência! "O VERDADEIRO IMPACTO DO SUPER EL NIÑO NA SUA VIDA"](https://youtu.be/IGgMxhMxHao) 1,5 mi · 27/07 · 3,3× · [Refúgio Cortes "O BRASIL INTEIRO VAI SENTIR"](https://youtu.be/C82XkHQNL4g) 1,3 mi · 19/10 · 16,1× · [Jubilut "Super EL NIÑO NO BRASIL: o que esperar?"](https://youtu.be/BAf4EYZ1AGk) 5,9 mi · 27/08 · 27,9× | o canal grande domina; difícil de vencer |
| T-F | "O pior ainda vem / quando acabar começa o problema" | [Sou curioso?! "O El Niño de 2026 vai ACABAR. E aí começa o PROBLEMA!"](https://youtu.be/CCRYhINqJ3A) 311 mil · 02/11 · 1,4× · [Fatos Desconhecidos "A pior parte do El Niño de 2026 ainda NÃO CHEGOU..."](https://youtu.be/6Wtb6MMWRZc) 244 mil · 29/10 · 1,0× | fraco (perto da mediana) |
| T-G | "[Tipos/formatos] … Explicados" | [Professor Vulcano "Os Formatos de Tornados Mais INSANOS Explicados"](https://youtu.be/7GE2xL75W7Q) 828 mil · 22/05 · 15,1× · [Vulcano "Os Tipos de Tornados MAIS RAROS Explicados em 8 Minutos"](https://youtu.be/2QKUupSi4Bg) 634 mil · 15/05 · 11,6× | não serve aos nossos 2 (não são catálogo) |
| — | Pergunta sim/não sobre recorde (o nosso título do El Niño) | [SpaceCast "O EL NIÑO MAIS FORTE DA HISTÓRIA? SACANI EXPLICA!"](https://youtu.be/5445iKrArbY) 72 mil · 3,8× (só 4 longos no canal: mediana frágil) · a afirmação rende mais: [StarTalk "The Biggest El Niño in Recorded History"](https://youtu.be/mgPN8B-B7tg) 5,5 mi · 5,1× | o recorde vira "sim/não" e esgota a curiosidade |

**Comum aos que rendem [O]:** 40–70 caracteres; lugar ou fenômeno reconhecível + **uma anomalia concreta** (oposto, encolher, oceano escondido, asfalto arrancado); 1–3 palavras em CAIXA ALTA; **nenhum dá a causa**. Notícia ("7 tornados…", "tornado em Chapecó") fica com TV e canais grandes: nos 25 primeiros da busca "tornado santa catarina", 18 são TV ou flagrante.

### Thumb
| # | Padrão | Referências (views · ×med) | Para nós |
|---|---|---|---|
| H-1 | **Região acesa (vermelho) no mapa escuro + seta + 2–4 palavras de ameaça/pergunta** | [ME SC "UM COLAPSO INEVITÁVEL?"](https://youtu.be/CMHf4Cqpcrs) 447 mil · 11,4× · [Além do Mapa "NINGUÉM ESPERAVA POR ISSO"](https://youtu.be/x_xE2HyxQE0) (América do Sul, Sul em vermelho, tornado em cima) 64 mil · 11,1× · [PBS Terra "DEADLIER?"](https://youtu.be/5UTQ4KrtVGc) (faixa vermelha do corredor nos EUA + seta) 3,0 mi · 3,7× · [Rogerdautry "524 TORNADOS"](https://youtu.be/TfTiDfsKK04) (mapa de focos) 56 mil · 3,2× | **sim**: é mapa, a nossa linguagem |
| H-2 | **Bloco 3D recortado no lugar, o invisível tornado visível, fundo escuro/satélite, seta amarela** | [Chão do Sul "O SUL É OUTRO PAÍS"](https://youtu.be/xpBOF8FXXHM) 736 mil · 15,4× · [Chão do Sul "MAIOR DO QUE 03 PAÍSES"](https://youtu.be/pm0Pgr5BlqA) (aquífero azul brilhando sob o bloco) 87 mil · 1,8× | **sim**: é literalmente "Em Relevo" |
| H-3 | **Mapa de anomalia do mar (língua vermelha no Pacífico) em tela cheia + 2–3 palavras** | [Jubilut "OUTUBRO JÁ ERA"](https://youtu.be/BAf4EYZ1AGk) 5,9 mi · 27,9× · [Olá, Ciência! "JÁ ERA"](https://youtu.be/IGgMxhMxHao) 1,5 mi · 3,3× · [Sou curioso?! "NEM A CIÊNCIA ESPERAVA"](https://youtu.be/gkkqmtbOwmE) 1,1 mi · 4,9× | **sim** para o El Niño (temos o OISST da NOAA no vídeo) |
| H-4 | **Brasil em 2 cores opostas (laranja seco × azul água/tempestade)** | [JeanGrafia "BRASIL RACHADO"](https://youtu.be/GnEXgEaYz1M) 150 mil · 6,2× · [100% Atômico](https://youtu.be/vXAT5va1NXI) (Brasil vermelho/azul com alertas) 546 mil · 52,3× · [Cosmos Oculto](https://youtu.be/ypzxfNnCVio) (mapa azul/vermelho + rosto) 1,5 mi (canal de Shorts: ×med não comparável) | sim, sem copiar a "rachadura" |
| H-5 | Foto escura de tornado/supercélula + texto enorme | [Canal Vilão "NOVA AMEAÇA"](https://youtu.be/_-eh-KSyaLU) 127 mil · 4,6× · [Arquivo da Tragédia "O CÉU MUDOU EM MINUTOS"](https://youtu.be/v7xUCFOQdxM) 90 mil · 119,6× · [Natureza Sinistra "OS TORNADOS DO INVERNO DE 2026"](https://youtu.be/h04CSUPoKX0) 413 mil · 2,3× | só se a foto for licenciada e do Sul |
| H-6 | Rosto expressivo + mapa | Cosmos Oculto, 100% Atômico, Refúgio Cortes, JeanGrafia, StarTalk | **não** (canal sem rosto; fora da bíblia) |

**Comum [O]:** fundo escuro ou saturado (nenhum bege); **1 objeto-herói** (região, bloco, língua de calor); 2–4 palavras brancas/amarelas com contorno; seta em 6 dos 12 do mosaico do Sul. O texto **ameaça ou pergunta** e não repete o título. As nossas duas (bege + polaroid pequeno) são as únicas claras da grade (ver mosaicos).

---

## 2. Vídeo: Sul do Brasil (`bG6-E4qjXYc`)
**Atual:** "O que está acontecendo com o clima no Sul do Brasil?" · 184 impressões · CTR 2,7% · retenção 49% (Studio, 28 d até 13/11). 10:23. Thumb: "7 TORNADOS EM 6 DIAS" sobre papel bege + polaroid de Chapecó.

### Top referências do mesmo tema (≤ 400 d, longos)
| Vídeo | Canal (inscritos) | Views | Data | v/i | ×med |
|---|---|---|---|---|---|
| [Tornado Alley Is MOVING and That's a HUGE Problem](https://youtu.be/5UTQ4KrtVGc) (en) | PBS Terra (1,05 mi) | 2.978.613 | 30/04/26 | 2,8 | 3,7 ✔ |
| [Os Formatos de Tornados Mais INSANOS Explicados](https://youtu.be/7GE2xL75W7Q) | Professor Vulcano (28,9 mil) | 828.480 | 22/05/26 | 28,7 | 15,1 ✔ |
| [Por que a Região Sul é o OPOSTO…](https://youtu.be/xpBOF8FXXHM) (veio de lugar) | Chão do Sul (6,6 mil) | 735.720 | 24/10/26 | 111 | 15,4 ✔ |
| [O EF5 de Smithville: O Tornado que Arrancou o Asfalto](https://youtu.be/obG4EMWkCcA) | Natureza Sinistra (59,9 mil) | 651.478 | 30/05/26 | 10,9 | 3,6 ✔ |
| [OS TORNADOS DO INVERNO DE 2026 \| Brasil](https://youtu.be/h04CSUPoKX0) | Natureza Sinistra | 412.817 | 12/09/26 | 6,9 | 2,3 ✔ |
| [JH: Brasil tem o 2º maior corredor de tornados do mundo…](https://youtu.be/9w1f8S44OpY) (4 min) | g1 (2,77 mi) | 282.857 | 10/08/26 | 0,1 | 20,8 ✔ |
| [O F4 de Rio Bonito do Iguaçu e o SURTO de tornados no SUL](https://youtu.be/j0aoIeu8Q3E) | Natureza Sinistra | 204.491 | 21/11/25 | 3,4 | 1,1 ✔ |
| [Em 20 minutos, Santa Catarina virou um cenário de guerra](https://youtu.be/_-eh-KSyaLU) | Canal Vilão (235 mil) | 126.967 | 05/11/26 | 0,5 | 4,6 ✔ |
| [Tem Algo Estranho Acontecendo no Sul do Brasil](https://youtu.be/x_xE2HyxQE0) (clone de mapa) | Além do Mapa (5,1 mil) | 64.264 | 06/11/26 | 12,5 | 11,1 ✔ |
| [O CORREDOR DE TORNADOS NO BRASIL: 524 Casos Confirmados](https://youtu.be/TfTiDfsKK04) | Prof. Rogerdautry (80,1 mil) | 56.483 | 13/09/26 | 0,7 | 3,2 ✔ |
Leitura: o "porquê" evergreen (corredor, formação) rende o ano todo (Vulcano em maio, PBS em abril, g1 em agosto); a semana de novembro foi da TV. O "corredor de tornados" é termo que o público já conhece (g1, Rogerdautry, PBS "Tornado Alley").

### O que o vídeo entrega (conferido em `legendas-v2.srt`)
1. **0:00–0:29** Maringá F2 (0:02), Chapecó "o maior evento climático em 50 anos" (0:16), Santo Augusto (0:20), "7 tornados confirmados em 6 dias." (0:26). **0:39** "Por que isso está acontecendo?" ← a promessa do porquê aparece no 1º minuto.
2. **3:13–3:15** "Isso é inédito?" / "A resposta curta é: não."
3. **4:18–4:28** "O que não muda é o mapa. A faixa entre o norte da Argentina, o Paraguai, o Uruguai e o Sul do Brasil é considerada por pesquisadores a 2ª região mais propícia a tornados do mundo, depois dos Estados Unidos." ← paga o Título 1.
4. **4:39–5:02** "Comece pela Amazônia…" → jato de baixos níveis → "No caminho, existe uma parede: a Cordilheira dos Andes." (4:51) → **"É como um rio invisível de umidade."** (5:02) ← paga o Título 2 e a thumb.
5. **5:56–6:08** "a maioria das supercélulas não gera tornado… a ciência ainda não entende totalmente."
6. **6:16** "Poucos lugares do planeta juntam esses 4 ingredientes como o Sul do Brasil."
7. **8:32–8:39** "O Brasil nunca teve um F5 confirmado. Mas a região já teve: San Justo…"; **8:58** "O pior cenário… é um tornado forte sobre uma cidade grande."
8. **9:58–10:12** "Não é um mistério, nem um castigo… Os tornados sempre estiveram aqui. Agora, estamos vendo cada um deles."

### Proposta
**Título 1 (T-A, "Por que [LUGAR] é [anomalia]?"):**
> **Por que o SUL do Brasil fica no 2º maior corredor de TORNADOS do mundo?** (71 car.)
- Padrão: Chão do Sul "Por que a Região Sul é o OPOSTO…" 736 mil, 24/10/26, 15,4× · ME "Por que o RIO GRANDE DO SUL Vai Começar a ENCOLHER?" 259 mil, 23/10/26, 6,6× (+ ME "Por que Existem Duas Guianas?" 512 mil, 13,0×). Tema: g1 "2º maior corredor" 283 mil (20,8×).
- Pago em 4:18–4:28 (frase exata acima); a pergunta do porquê já aparece em 0:39. "Fica no" é de propósito: o vídeo diz que a **faixa** (Sul + Argentina + Paraguai + Uruguai) é a 2ª região, não o Sul sozinho.
- Busca: "por que o sul do brasil" tem mediana de 173 mil no top-15 (gap). "Corredor de tornados" é o termo do g1 e do PBS.

**Título 2 (T-B, "O [coisa invisível] que [faz algo] no [lugar]"):**
> **O rio invisível que alimenta os TORNADOS do Sul do Brasil** (57 car.)
- Padrão: Chão do Sul "Tem um oceano escondido no Sul do Brasil que ninguém vê" 87 mil, 25/10/26, 1,8× · Natureza Sinistra "O Tornado que Arrancou o Asfalto" 651 mil, 30/05/26, 3,6× (+ Um Documentário "A cidade soterrada por uma montanha em três minutos" 5,3 mi, 6,3×).
- Pago em 5:02 ("É como um rio invisível de umidade"), com o caminho Amazônia → Andes → Sul em 4:39–5:02. Não dá a causa (não diz Amazônia nem Andes).
- Risco: o pagamento cai aos 5 min. Até lá, o hook de 0:00–0:29 mostra os tornados do Sul (a 2ª metade do título) e 0:39 promete o porquê. Sugestão sem re-render: renomear o capítulo "4:35 Pergunta 1: por que acontece aqui" para "4:35 O rio invisível e a parede dos Andes", para quem pula pelos capítulos.

**Thumb (1 conceito; padrões H-1 + H-2):**
- **Cena:** bloco 3D da América do Sul visto de sudeste, levemente inclinado, sobre **fundo navy escuro (#1F2A44) / oceano de satélite escuro**. Os **Andes erguidos como uma parede** marrom com cume branco à esquerda. A Amazônia em verde-escuro no alto.
- **Objeto-símbolo:** uma **fita luminosa ciano/branca** (o "rio invisível") que sai da Amazônia, desce colada aos Andes e termina no Sul. **PR/SC/RS acesos em coral (#E8505B)**, recortados em bloco com a lateral mostrando as camadas (a nossa assinatura). Sobre SC/RS, uma **supercélula com funil** modelada em 3D (escura, com base girando). Sem foto: as fotos que temos com licença são dos EUA ou de terceiros, e foto de outro lugar quebra a fidelidade.
- **Sem personagem/rosto** (canal sem rosto). A "expressão" vem da ameaça: o funil tocando o Sul aceso.
- **Texto (2–3 palavras):** **"NÃO É AZAR"**, em Anton branco com "AZAR" em amarelo, contorno preto grosso, no **terço superior direito** (sobre o Atlântico escuro, longe do bloco). A própria fita faz o papel da seta.
- **O que promete:** existe uma causa geográfica visível no mapa, e não é acaso.
- **Conversa com os títulos sem repetir:** com o T1 ("por que fica no 2º maior corredor?"), a thumb mostra que há um mecanismo e nega o acaso. Com o T2 ("rio invisível"), ela torna o invisível visível, e o texto acrescenta a negação em vez de repetir "rio". Nenhuma palavra do título aparece na arte.
- **Pago em:** 4:39–5:02 (o rio e a parede), 6:16 ("Poucos lugares do planeta juntam esses 4 ingredientes"), 9:58 ("Não é um mistério, nem um castigo").
- **Referências de thumb:** [Chão do Sul "O SUL É OUTRO PAÍS"](https://youtu.be/xpBOF8FXXHM) (bloco 3D do Sul em fundo escuro + seta amarela) 736 mil, 15,4× · [Chão do Sul "MAIOR DO QUE 03 PAÍSES"](https://youtu.be/pm0Pgr5BlqA) (o invisível, aquífero azul, brilhando sob o bloco) 87 mil, 1,8× · [Além do Mapa "NINGUÉM ESPERAVA POR ISSO"](https://youtu.be/x_xE2HyxQE0) (Sul em vermelho com funil em cima) 64 mil, 11,1× · [PBS Terra "DEADLIER?"](https://youtu.be/5UTQ4KrtVGc) (faixa vermelha do corredor + seta) 3,0 mi, 3,7×.
- **Diferenciação:** o Chão do Sul brilha a água **embaixo** do bloco; nós brilhamos o ar **por cima**, ao longo dos Andes. O Além do Mapa usa mapa chapado e foto-ilustração; nós usamos relevo com a parede andina. Texto e frase próprios.
- **320×180:** 1 foco (o Sul coral com o funil) + 3 palavras curtas. A fita precisa de largura ≥ 4% da altura para não sumir; conferir na prévia ao lado do ME e do Chão do Sul.
- **Desvio da bíblia:** fundo navy/satélite escuro e sem papel bege nem polaroid, **porque** nas 12 referências medidas nenhuma thumb que rende é clara. As nossas 2 bege são as únicas claras da grade (mosaico) e o gap 2 mostra que elas somem a 320×180. Ficam da bíblia: a paleta (navy, coral), a fonte Anton e o relevo 3D, que passa a ser o herói.

---

## 3. Vídeo: El Niño 2026 (`FeSLzHvlkbo`)
**Atual:** "El Niño 2026 vai ser o mais forte da história?" · 179 impressões · CTR 1,7% · retenção 62% (Studio, 28 d até 13/11). 12:10. Thumb: "É SUPER?" + "EL NIÑO 2026" sobre papel bege + polaroid do Pacífico.

### Top referências do mesmo tema (≤ 400 d, longos)
| Vídeo | Canal (inscritos) | Views | Data | v/i | ×med |
|---|---|---|---|---|---|
| [Super EL NIÑO NO BRASIL: o que esperar?](https://youtu.be/BAf4EYZ1AGk) | Paulo Jubilut (3,85 mi) | 5.930.950 | 27/08/26 | 1,5 | 27,9 ✔ |
| [The Biggest El Niño in Recorded History](https://youtu.be/mgPN8B-B7tg) (en) | StarTalk (6,03 mi) | 5.500.995 | 09/10/26 | 0,9 | 5,1 ✔ |
| [O QUE É esse TAL de EL NIÑO? ENTENDA TUDO…](https://youtu.be/tWhcTTC-pyw) | Manual do Mundo (20,6 mi) | 3.464.308 | 08/08/26 | 0,2 | 3,0 ✔ |
| [This Super El Niño Will Be the Strongest In Living Memory](https://youtu.be/_b_sGbjSVZQ) (en) | Astrum Earth (506 mil) | 2.437.499 | 08/06/26 | 4,8 | 2,0 ✔ |
| [EL NIÑO: O FENÔMENO QUE PODE MUDAR O BRASIL!](https://youtu.be/ypzxfNnCVio) | Cosmos Oculto (26,2 mil) | 1.485.292 | 07/11/26 | 56,7 | outlier (canal de Shorts) |
| [O VERDADEIRO IMPACTO DO SUPER EL NIÑO NA SUA VIDA](https://youtu.be/IGgMxhMxHao) | Olá, Ciência! (2,65 mi) | 1.462.431 | 27/07/26 | 0,6 | 3,3 ✔ |
| ["O BRASIL INTEIRO VAI SENTIR": OS EFEITOS DO SUPER EL NIÑO](https://youtu.be/C82XkHQNL4g) | Refúgio Cortes (43,4 mil) | 1.316.253 | 19/10/26 | 30,3 | 16,1 ✔ |
| [O El Niño de 2026 NÃO é o Que Você Pensa](https://youtu.be/gkkqmtbOwmE) | Sou curioso?! (11,4 mil) | 1.100.112 | 06/10/26 | 96,5 | 4,9 ✔ |
| [SUPER EL NIÑO ASSUSTADOR — O BRASIL PODE SOFRER MAIS…](https://youtu.be/vXAT5va1NXI) | 100% Atômico (70,8 mil) | 545.690 | 07/11/26 | 7,7 | 52,3 ✔ |
| [O El Niño de 2026 vai ACABAR. E aí começa o PROBLEMA!](https://youtu.be/CCRYhINqJ3A) | Sou curioso?! | 310.653 | 02/11/26 | 27,3 | 1,4 ✔ |
| [SUPER EL NIÑO 2026: por que o Norte vai SECAR e o Sul vai AFOGAR](https://youtu.be/GnEXgEaYz1M) | Prof. JeanGrafia (718 mil) | 149.915 | 22/05/26 | 0,2 | 6,2 ✔ |
| [O El Niño RACHOU o Brasil ao meio!](https://youtu.be/BpIY4ex2u6E) | Prof. JeanGrafia | 142.803 | 10/11/26 | 0,2 | 5,9 ✔ |
Leitura: o "o que é / o que esperar" é dos gigantes (Jubilut, Manual do Mundo, JH). Os pequenos que estouram (Sou curioso?! 11 mil inscritos → 1,1 mi; Refúgio 43 mil → 1,3 mi) entraram por um **ângulo**: "não é o que você pensa" ou "o Brasil inteiro vai sentir". Ninguém do top usa pergunta de sim/não sobre o recorde. Atenção: o JeanGrafia (10/11) usou "7 TORNADOS em 6 DIAS" na thumb, o mesmo texto da nossa do Sul.

### O que o vídeo entrega (conferido em `legendas.srt`)
1. **0:00–0:10** "Manaus, 9 de outubro. A fumaça das queimadas fecha escolas…"; **0:13–0:19** Dionísio Cerqueira (SC), 581 mm, "Mais de meio metro de água em um mês"; **0:22** mar do Peru 5,5 °C acima do normal.
2. **0:28–0:35** "Fumaça no Norte. Água demais no Sul. Mar quente no Pacífico. Parecem 3 notícias diferentes. Mas têm o mesmo nome." ← paga o Título 1 no 1º minuto.
3. **0:55–0:57** "O El Niño não começa no Brasil. Começa a mais de 10 mil quilômetros daqui, no meio do oceano." ← paga a thumb ("VEM DAQUI") no 1º minuto.
4. **3:30–3:36** pelo termômetro tradicional, "já passou o de 82 e o de 97" e está "a pouco mais de 1 décimo de grau do recorde de 2015".
5. **3:45** "Mas tem um detalhe que quase ninguém conta." → **3:59** "a NOAA… passou a usar um termômetro novo" → **4:12–4:29** "com esse termômetro, a história muda… O de 2026 está, hoje, em 2 graus… Mas ainda não é o maior da história." ← paga o Título 2.
6. **4:54–4:59** "Super é um apelido da imprensa. Nenhuma agência oficial usa essa palavra. O termo técnico é muito forte."; **5:12** "O El Niño não é causado pelo aquecimento global."
7. **5:33–5:57** o mecanismo: o ar desce sobre a Amazônia e o norte do Nordeste ("Menos chuva"); "No Sul acontece o contrário… Mais chuva." ← o porquê do Título 1. **8:06** "E chegamos ao Sul, onde o El Niño mais pesa"; **8:09** Taquari inunda Muçum, Encantado, Estrela e Lajeado.
8. **9:31–9:35** a enchente de 2024 "veio quando ele já estava perdendo força… o perigo não termina junto com o pico"; **10:06–10:09** pico "até dezembro, no máximo em janeiro. Bem no meio do nosso verão."

### Proposta
**Título 1 (T-D, contraste Norte × Sul, com imagem concreta):**
> **FUMAÇA no Norte, ENCHENTE no Sul: por que o El Niño faz isso com o Brasil?** (74 car.)
- Padrão: JeanGrafia "SUPER EL NIÑO 2026: por que o Norte vai SECAR e o Sul vai AFOGAR" 150 mil, 22/05/26, 6,2× · JeanGrafia "O El Niño RACHOU o Brasil ao meio!" 143 mil, 10/11/26, 5,9× (mesmo gatilho de contraste: Chão do Sul "…o OPOSTO…" 736 mil, 15,4×). As 2 referências diretas são do mesmo canal. Se o crivo exigir 2 canais, a 2ª é o Chão do Sul (contraste regional, mesmo nicho e idioma).
- Pago em 0:00–0:35 (as 3 imagens e "têm o mesmo nome"); o porquê em 5:33–5:57; a enchente em 8:09.
- Diferenciação: abre pelas **imagens** (fumaça/enchente), não pelos verbos do JeanGrafia (secar/afogar) nem por "rachou". O lugar é o sujeito, como pede o gap 1.

**Título 2 (T-C, "o que ninguém conta / não é o que você pensa"):**
> **O detalhe que quase ninguém conta sobre o Super El Niño de 2026** (63 car.)
- Padrão: Sou curioso?! "O El Niño de 2026 NÃO é o Que Você Pensa" 1,1 mi, 06/10/26, 4,9× · ME "O Nordeste Não É O Que Você Pensa..." 104 mil, 28/08/26, 2,7× (apoio en: "Nobody Realizes What El Niño Is About To Do…" 2,3 mi, 23,9×; e Chão do Sul "…que ninguém vê" 87 mil, 1,8×).
- Pago em 3:45: a frase "Mas tem um detalhe que quase ninguém conta" está **literalmente** no vídeo, e o detalhe (o termômetro novo da NOAA, que muda o recorde) vem em 3:59–4:29. Reforço em 4:54 ("Super é um apelido da imprensa"). "Super El Niño" fica no título porque é o termo buscado (Jubilut 5,9 mi; tags).
- Risco: o pagamento cai aos 3:45. Em 0:36 o hook já pergunta "esse é mesmo o tal Super El Niño?", o que segura a expectativa. Não copia o "NÃO é o que você pensa" (frase e estrutura diferentes).

**Thumb (1 conceito; padrões H-3 + H-4):**
- **Cena:** relevo 3D da América do Sul em tela cheia, visto **do Pacífico** (câmera a oeste, baixa), sobre fundo navy escuro. O **Pacífico** à esquerda pintado com a anomalia real da NOAA OISST (a mesma do vídeo): uma **língua vermelho-laranja** que corre pelo Equador e bate na costa do Peru.
- **O Brasil em 2 estados:** o **Norte** (Amazônia) sob uma névoa cinza-marrom de fumaça com brilho laranja de focos; o **Sul** (PR/SC/RS) em azul-escuro, com chuva e rios cheios brilhando. A transição é gradual (sem a "rachadura" do JeanGrafia).
- **Objeto-símbolo:** **seta amarela grossa** saindo da língua quente do Pacífico em direção ao Brasil.
- **Sem personagem/rosto.**
- **Texto (2 palavras):** **"VEM DAQUI"**, Anton branco, contorno preto, no **terço superior esquerdo**, sobre o Pacífico, logo acima da origem da seta.
- **O que promete:** o que acontece no Brasil tem origem num ponto do oceano que a thumb mostra.
- **Conversa com os títulos sem repetir:** o T1 nomeia os 2 efeitos (fumaça, enchente) e a thumb mostra a **origem**; juntos fazem a pergunta "como o mar do Peru faz isso aqui?". O T2 promete um detalhe escondido, e a thumb aponta para o lugar onde ele está (o Pacífico, onde a NOAA mede o termômetro novo). Nenhuma palavra do título aparece na arte.
- **Pago em:** 0:55–0:57 ("O El Niño não começa no Brasil. Começa a mais de 10 mil quilômetros daqui, no meio do oceano"); a gangorra em 1:46–2:11.
- **Referências de thumb:** [Jubilut "OUTUBRO JÁ ERA"](https://youtu.be/BAf4EYZ1AGk) (mapa de anomalia em tela cheia + 2 palavras) 5,9 mi, 27,9× · [Olá, Ciência! "JÁ ERA"](https://youtu.be/IGgMxhMxHao) 1,5 mi, 3,3× · [Sou curioso?! "NEM A CIÊNCIA ESPERAVA"](https://youtu.be/gkkqmtbOwmE) 1,1 mi, 4,9× · [JeanGrafia "BRASIL RACHADO"](https://youtu.be/GnEXgEaYz1M) (Brasil laranja × azul) 150 mil, 6,2× · [100% Atômico](https://youtu.be/vXAT5va1NXI) (Brasil vermelho/azul + setas) 546 mil, 52,3×.
- **Diferenciação:** os 3 do H-3 são mapas chapados vistos de cima; o nosso é **relevo 3D visto do Pacífico, com a seta da causa** (os Andes no meio do caminho). O H-4 do JeanGrafia é um Brasil rachado com professor; o nosso não tem rosto nem rachadura.
- **320×180:** 1 foco (a língua vermelha + a seta) + 2 palavras. O vermelho sobre o navy é o contraste mais forte da grade. Conferir que a fumaça do Norte não vire um borrão (subir a saturação do laranja dos focos).
- **Desvio da bíblia:** o mesmo do Sul (fundo escuro, sem papel nem polaroid), **porque** a nossa thumb atual já traz o mapa de anomalia certo, mas num polaroid pequeno sobre bege. Os 3 maiores do tema (5,9 mi, 1,5 mi e 1,1 mi) usam esse mesmo mapa **em tela cheia**.

---

## Observações para o orquestrador
- **Notícia → evergreen:** os 2 títulos do Sul tiram a semana (7 tornados) do título. O vídeo continua honesto: os primeiros 3 min são a semana e o porquê vem em 4:18–6:19. Por isso a dica do capítulo 4:35.
- **El Niño tem prazo:** o tema morre por volta de abr–mai/2027 (fim previsto em 10:20). O T2 sobrevive melhor ao boletim; o T1 vale enquanto houver fumaça e chuva (nov–mar).
- Nenhuma proposta usa morte/morreu/morto/matou nem "em N minutos" (a bíblia do Em Relevo não usa duração no título).
- A mediana do Cosmos Oculto (1,4 mil) é de um canal de Shorts: o "1.050×" dele não serve de evidência e ficou fora das propostas.
