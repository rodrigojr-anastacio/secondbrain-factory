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
