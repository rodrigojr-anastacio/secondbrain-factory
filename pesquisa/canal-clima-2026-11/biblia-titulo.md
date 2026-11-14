# Título: Em Relevo (clima/geografia/mapa, pt-BR; referências pt e en)

Prevalece sobre `conhecimento/titulos.md`. Método: `conhecimento/titulos.md` §Método (12/11/2026).

## Padrões das referências (12/11/2026)
Fonte: yt-dlp via WARP, views de 12/11/2026 (últimos ~80 vídeos) de Mundo Entrópico, Chão do Sul, Mapa Verso, GeoDocs, Geografía con Geoff, Geography Effect, Astrum Earth, The Last Day, SkyWhisper e Disasters Explained (os de `dados/canais_nicho.json`). Brutos em `../padroes-titulos-2026-11-12.md`. O yt-dlp devolveu em inglês os títulos do Mundo Entrópico: confira o original em pt antes de copiar.

| Padrão | Exemplo real | Views | Canal |
|---|---|---|---|
| Por que [lugar] é tão ESQUECIDO / quase ninguém mora em X? | Why is the coast of Piauí so FORGOTTEN? | 2,3 mi | Mundo Entrópico |
| idem (es) | Por Qué Nadie Vive en Esta Enorme Parte de la Costa de África | 3,7 mi | Geografía con Geoff |
| idem (pt, vizinhos) | Why do so few Brazilians live on the coast of Paraná? · …in Roraima? | 1,4 mi · 705 mil | Mundo Entrópico |
| Why is there NO [coisa óbvia] between A and B? / Why are there two X? | Why is there NO bridge between AMAPÁ and the rest of BRAZIL? | 433 mil | Mundo Entrópico |
| Por que [lugar] não é parte de [onde deveria]? (es) | La Extraña Isla Británica que No Es Parte del Reino Unido | 1,2 mi | Geografía con Geoff |
| The X That Changed Science / Shouldn't Exist | The Tornado That Shouldn't Exist – El Reno 2013 · The Underwater Lakes That Shouldn't Exist | 1,1 mi · 4,1 mi | SkyWhisper · Astrum Earth |
| What They Found / Scientists Found … in X | What They Found In the Deepest Place on Earth | 13 mi | Astrum Earth |
| What would happen if [extremo]? | What would happen If the Moon Crashed Into Earth? | 2,0 mi | The Last Day |
| [Evento 2026] Explained: [o que aconteceu] | Nepal's 2026 Disaster Explained: The Glacier That Wiped Out a Valley | 5,2 mi | The Last Day |
| Every [fenômeno] Explained | Every Tornado Type Explained | 3,2 mi | Disasters Explained |
| Why [país] Is Sitting On / The Real Reason … | Why Canada Is Sitting On the Most Valuable Land In Human History | 1,2 mi | Geography Effect |

**Os 5–6 que mais rendem:** (1) "Por que [lugar] é tão esquecido/vazio?" (mapa, os mais perto do nosso formato: 1,4–3,7 mi); (2) "What They Found / Scientists Found in X" (Astrum, 5–13 mi, mas é canal de 504 mil inscritos); (3) "The X That Shouldn't Exist / Changed Science"; (4) "[Evento do ano] Explained" (quente, 5,2 mi); (5) "What would happen if …"; (6) "Every X Explained" (mas é fórmula saturada: clones < 9 mil, ver RELATORIO §2).
**O que têm em comum:** mostram uma **anomalia concreta** (um vazio no mapa, algo que "não devia existir", o lugar mais profundo) e **não dizem a causa**. Os que respondem ("Will Be the Strongest In Living Memory") rendem menos que os que abrem o buraco.

**Regra (12/11/2026): 3 títulos de 3 padrões diferentes, cada um com uma thumb; nunca entregar a resposta.** Ex. tornado: A "Por que o Brasil tem tantos tornados e quase ninguém fala?" (1) · B "O tornado que não devia existir no Sul do Brasil" (3) · C "O que o tornado de Chapecó mostrou" (4, ajustar).

### Onde estamos fora do padrão (`youtube.videos`)
- "O que está acontecendo com o clima no Sul do Brasil?" é o molde "What is HAPPENING to SANTA CATARINA?!" (Mundo Entrópico, 443 mil: mediano), vago e sem anomalia concreta. Melhor: nomear a coisa estranha (padrão 1 ou 3).
- "El Niño 2026 vai ser o mais forte da história?" é pergunta sim/não, sem lugar nem anomalia (a referência Astrum, 2,4 mi, afirma o fato, e o Jubilut fez 5,9 mi com "o que esperar?"). Sem padrão da tabela; trocar por "Por que… / O que ninguém mostra sobre o El Niño no mapa".

## Políticas do YouTube (14/11/2026, `conhecimento/politicas-youtube.md`)
Em Relevo (sem pasta em `canais/`; esta é a bíblia de título/thumb): título, descrição e tags **sem** morte/morreu/morto/assassinado e sinônimos chocantes ("matou 500 mil" vira "500 mil vítimas" ou sai); thumb sem foto real de morto/vítima em destaque (use mapa, satélite, gráfico, lugar hoje); fotos de acervo de vítimas/retirantes só como contexto distante, nunca close; `youtube.txt` sem menção a IA/voz sintética (padrão em `conhecimento/politicas-youtube.md`).

## Thumbs da reembalagem 14/11/2026 (teste aprovado pelo Rodrigo): fundo navy, 1 objeto-herói. **Hipótese (teste aprovado 14/11/2026)**, medir CTR
`pesquisa/reembalagem-2026-11-14/thumbs/emrelevo.py` (custo US$ 0, 100% dados reais, sem IA de imagem): El Niño = língua de anomalia ≥ 2 °C da NOAA OISST (08/11) em laranja/vermelho sobre oceano navy, termômetro grosso cravado no Niño 3.4, seta amarela até o Brasil em coral, "SÓ 2 °C?"; Sul = Cone Sul oblíquo com Andes como parede de cume branco, fita ciano (rio de umidade) colada à encosta até o Sul em coral, sem ponta de seta, "CULPA DOS ANDES?". Fundo escuro em vez do bege/polaroid (conceitos em `pesquisa/reembalagem-2026-11-14/PROPOSTAS.md`). Geração por homografia em PIL (sem cartopy/matplotlib).

## Embalagem antes do roteiro (14/11/2026)
Todo vídeo novo passa pela skill `embalagem` + crivo independente (`skills/embalagem/`) **antes** do roteiro; o hook paga a promessa. Fonte: decisão do Rodrigo, 14/11/2026; base `pesquisa/reembalagem-2026-11-14/padroes.md` e `PROPOSTAS.md` (seção Em Relevo). Esta bíblia cobre título e thumb (não há `biblia-thumb.md`). Views e datas de 14/11/2026; "×med" = views ÷ mediana real do canal da referência. Sem dado de CTR nosso: tudo **Hipótese (reembalagem 14/11/2026, CTR a medir)**.

### Padrões de título medidos
- **"Por que [LUGAR] é/tem [anomalia]?"** (lugar como sujeito, sem dar a causa): [Por que a Região Sul é o OPOSTO das outras regiões do Brasil?](https://youtu.be/xpBOF8FXXHM) 736.562 · 24/10/2026 · 15,4× (mediana frágil, 8 vídeos); [Por que Existem Duas Guianas?…](https://youtu.be/it5Vsv851Rc) 512.180 · 11/09/2026 · 14,3×.
- **"O/A [coisa concreta] que [faz algo]"** (o objeto aparece, a causa não): [O EF5 de Smithville: O Tornado que Arrancou o Asfalto](https://youtu.be/obG4EMWkCcA) 651.512 · 30/05/2026 · 3,6×; [O Estado ISOLADO que pode MUDAR o FUTURO do Brasil](https://youtu.be/ZSBraswH1To) 114.189 · 20/05/2026 · 3,2×.
- **Contraste Norte × Sul + "por que":** [SUPER EL NIÑO 2026: por que o Norte vai SECAR e o Sul vai AFOGAR](https://youtu.be/GnEXgEaYz1M) 149.915 · 22/05/2026 · 6,2×; [O El Niño RACHOU o Brasil ao meio!](https://youtu.be/BpIY4ex2u6E) 142.907 · 10/11/2026 · 5,9×.

### Padrões de thumb medidos
- **Pergunta curta (2–3 palavras, branco + amarelo) sobre mapa escuro com 1 região destacada:** [it5Vsv851Rc](https://youtu.be/it5Vsv851Rc) ("POR QUE?") 14,3×; [O que está ACONTECENDO com SANTA CATARINA?!](https://youtu.be/CMHf4Cqpcrs) 447.720 · 30/10/2026 · 12,5×.
- **Anomalia do Pacífico em tela cheia + 2–3 palavras:** [Super EL NIÑO NO BRASIL: o que esperar?](https://youtu.be/BAf4EYZ1AGk) 5.930.950 · 27/08/2026 · 27,9×; [O VERDADEIRO IMPACTO DO SUPER EL NIÑO NA SUA VIDA](https://youtu.be/IGgMxhMxHao) 1.462.609 · 27/07/2026 · 3,3×.
- **Número grande sobre mapa escuro:** BpIY4ex2u6E ("7 TORNADOS em 6 DIAS") 5,9×; [O CORREDOR DE TORNADOS NO BRASIL: 524 Casos Confirmados](https://youtu.be/TfTiDfsKK04) 56.483 · 13/09/2026 · 3,2×.
- **Bloco 3D do lugar / o invisível tornado visível:** xpBOF8FXXHM (bloco 3D + seta amarela) 15,4×; [Tem um oceano escondido no Sul do Brasil que ninguém vê](https://youtu.be/pm0Pgr5BlqA) 86.922 · 25/10/2026 · 1,8×.

### O que NÃO funciona neste canal
- **Notícia no título** ("7 tornados…", "tornado em Chapecó"): 18 dos 25 primeiros da busca são TV ou flagrante.
- **Molde genérico sem objeto** ("O detalhe que quase ninguém conta sobre o Super El Niño…"): promessa vaga e desencontrada da thumb; reprovado na r1 (El Niño T2).
- **Pergunta sim/não sobre recorde** ("vai ser o mais forte da história?"): esgota a curiosidade.
- **"O pior ainda vem":** perto da mediana (1,0–1,4×).
- **Thumb com 3+ focos:** língua + fumaça + chuva + relevo ("VEM DAQUI", El Niño v1); 6 elementos com o Sul a ~15% da altura ("NÃO É AZAR", Sul v1). Ambas reprovadas na r1.
- **Pintar o Pacífico inteiro de vermelho:** 5 das 12 thumbs do tema já fazem isso.
- **Continente de satélite + Sul vermelho + funil:** é a composição do Além do Mapa (06/11).
- **Bege + polaroid pequeno:** as nossas eram as únicas claras da grade e somem a 320×180.

### As 5 lições, adaptadas a vídeo novo (PROPOSTAS.md (b), 14/11/2026)
1. Notícia sai do título: lugar + anomalia concreta, sem dar a causa (a TV domina o "7 tornados").
2. Nomear o objeto concreto do achado (termômetro, rio invisível), nunca "o detalhe que ninguém conta".
3. Thumb escura com 1 herói (região, língua quente ou fluxo) e pergunta de 2–3 palavras; fugir do Pacífico inteiro vermelho e do "Sul vermelho + funil".
4. Se o pagamento estiver no meio do vídeo, o capítulo leva o termo do título (no Sul, o "rio" só aparecia aos 48%).
5. Prévia de 320×180 ao lado dos concorrentes antes de aprovar; e o hook já abre a pergunta do título (os 4 hooks do canal repetiam a moldura de aula, gap 5 de `pesquisa/gap-2026-11-14/RELATORIO.md`).
