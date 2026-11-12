# Título: dossie-es

Regra de canal: **prevalece** sobre `conhecimento/titulos.md`.

## Fórmula
- **"TODA la historia de <la organización> en N minutos"**: TODA em caixa alta; N = duração real arredondada; X com 1–3 palavras, de preferência **sigla famosa** (CIA, KGB, FBI). [canal.yaml; estilo.md de 04/11]
- Título B para o "Testar e comparar": "La historia COMPLETA de X en N minutos".
- **Termo com mais demanda, medido (004, 05/11/2026):** entre os vídeos de história em es (busca yt-dlp, 6 consultas, sem músicas/filmes), "Cosa Nostra" aparece em 24 títulos (mediana top-10 ~451 mil), "Mafia italiana" em 13 (~259 mil) e "Mafia siciliana" em 4 (~90 mil). Para temas com vários nomes, meça assim antes de escolher X.
- Em es, o molde aparece como "TODA la Historia de X en N Minutos" ou "La HISTORIA COMPLETA de X", às vezes com subtítulo ("| El Servicio Secreto Más Temido del Mundo"). [LEVANTAMENTO §2a, O]

## O que performa (Archive in Minutes, en, 2026-11-04)
- **[O]** Organizações de repressão/espionagem com nome famoso: Gestapo 349 mil, SS 317 mil, KGB 236 mil, Mossad 146 mil, CIA 141 mil, Soviet Union 126 mil, Cold War 117 mil, Stasi 114 mil, MI6 109 mil, Beria 86 mil.
- **[O]** Flopa: organização que o público não conhece (NKVD 22 mil, Abwehr 33 mil), evento pontual ou fora do eixo (Titanic 11 mil, Romanovs 36 mil, Barbarossa 34 mil, Berlin Wall 40 mil).
- **[I]** O gatilho é "instituição temida + promessa de completude curta". Mediana de 146 mil (7 organizações famosas) × 38 mil (8 eventos/estados). **O tema decide, não o hook**: o Abwehr usou o mesmo molde de hook e fez 10% das views. [LEVANTAMENTO §2a e §2c; dados.json]
- A ordem dos temas em es **não** é a do Archive: em es, CIA, FBI, Máfia, cartéis, SS e Templários têm muito mais busca que Stasi e MI6 (med. top-10 em es: 18 mil e 16 mil). Ranking em `../backlog.md`.

## Descrição (pacote)
- Em espanhol, com fontes (edições em espanhol quando houver) e a nota "Narración con voz sintética; ilustraciones generadas con IA a partir de investigación histórica." [estilo.md de 04/11]

## Não faça
- País ou império como X (é do `historia-ptbr`); pergunta curiosa (é do `lotr-fr`).
- Título em português ou "INTEIRA".
- N diferente da duração.

## Padrões das referências (12/11/2026)
Fonte: yt-dlp via WARP, views de 12/11/2026 (últimos ~80 vídeos) de Archive in Minutes (27 vídeos), Atlas del Tiempo (es), Historia Total, The Org Files, Classé Secret Défense (fr, entrevistas) e, como público vizinho, Te lo Pinto (explicadores militares/ranks). Brutos em `pesquisa/padroes-titulos-2026-11-12.md`. Nota: o yt-dlp devolveu alguns títulos em inglês (Te lo Pinto, Historia Total): confira o original antes de copiar.

| Padrão | Exemplo real | Views | Canal |
|---|---|---|---|
| The ENTIRE History of [sigla/organização temida] in N Minutes | The ENTIRE History of the SS in 16 Minutes | 653 mil | Archive in Minutes |
| idem | The ENTIRE History of the Gestapo in 12 Minutes | 444 mil | Archive in Minutes |
| idem (nossos temas) | The ENTIRE History of the Mossad / KGB / CIA in 10–13 Minutes | 247 / 245 / 205 mil | Archive in Minutes |
| ENTIRE History of A vs. B \| subtítulo de superlativo | The ENTIRE History of the CIA vs. KGB in 22 Minutes \| The Greatest Spy Duel | 87 mil | Atlas del Tiempo |
| idem + "\| The World's Most Feared …" | The ENTIRE History of the Mossad in 17 Minutes \| The World's Most Feared Secret Service | 82 mil | Atlas del Tiempo |
| Your Life at Every Rank/Level of [grupo] | Your Life in Every Rank of Templar Knight · Your Life at Every Bloods Rank | 2,2 mi · 713 mil | Te lo Pinto |
| All [grupo] Ranks Explained / How the FBI Hunts You at Every Level of Crime | All Russian Mafia Ranks Explained · How the FBI Hunts You… | 438 mil · 387 mil | Te lo Pinto |
| How the [organização] Works From the Inside | How the KGB Works From the Inside | 230 mil | Te lo Pinto |
| [Apelido]: History's Deadliest/Worst … | The Beast of Omaha: History's Deadliest Machine Gunner · The Hyena of Auschwitz | 2,9 mi · 224 mil | Te lo Pinto |
| [Ex-agente]: He Tells Us Everything! / The Hidden Side of the [agência] | Olivier Mas – Former DGSE Agent · The Hidden Side of the CIA: Coups, Espionage… | 95 mil · 55 mil | Classé Secret Défense |

**Os 5–6 que mais rendem** (só o Archive é molde direto; o resto é público vizinho): (1) "ENTIRE History of [organização temida]"; (2) "Your Life at Every Rank of X" (hierarquia de dentro); (3) "[Apelido]: History's Deadliest …" (pessoa/figura monstruosa); (4) "How the X Works From the Inside"; (5) "All X Ranks Explained"; (6) "The Hidden Side of / Former agent tells everything".
**O que têm em comum:** prometem **o lado escondido de uma instituição temida** (por dentro, a hierarquia, o apelido sinistro) e **não contam o que há lá**. O padrão 1 vive do tema: SS/Gestapo/MI6/Mossad/KGB entre 205 e 653 mil; org desconhecida cai a 12–27 mil (Kempeitai, GRU, OSS), e os clones pequenos (The Org Files: KGB 889, Mafia 651) mostram que a fórmula sozinha não carrega. O Atlas del Tiempo (es) ficou em 44–87 mil com o mesmo molde.

**Regra (12/11/2026, Rodrigo): 3 títulos de 3 padrões diferentes, cada um pareado com uma thumb; nunca entregar a resposta.** Ex. KGB: A "TODA la historia de la KGB en 14 minutos" (1) · B "Tu vida en cada rango de la KGB" (2) · C "Cómo funcionaba la KGB por dentro" (4). **Hipótese:** B e C combinam com o "Expediente N" do formato; testar.

### Onde estamos fora do padrão (só registro; Dossier em teste A/B, nenhum título alterado)
- Os 7 títulos são 100% o padrão 1 em es ("TODA/COMPLETA la historia de X en N minutos"), sem o subtítulo de superlativo do Atlas ("| El Servicio Secreto Más Temido del Mundo") e sem testar os padrões 2–4. O padrão 1 vale (temas SS/Gestapo/MI6 nem entraram), mas Mossad 319, CIA 80, FBI 39 views (12/11) com o tema forte indicam que o gargalo é descoberta/thumb, não só a fórmula.
- Temas fora do que renderia: Cosa Nostra/Masones são "evento/tema difuso" (o que flopou no Archive). Faltam SS, Gestapo, MI6, Stasi em es.
