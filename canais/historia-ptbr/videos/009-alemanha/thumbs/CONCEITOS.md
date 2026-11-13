# Títulos e thumbs · 009 Alemanha (etapa 1, 13/11/2026; bases e composição ficam para a etapa 2)

Regras: `biblia/titulo.md` (3 títulos de 3 padrões, pareados com 3 thumbs, nunca entregar a resposta; ≤ 60 caracteres) e `biblia/thumb.md` (padrão de entrega do 005: bonecos · HiM · 3º estilo). Prompts das 6 bases em `cenas-thumbs.json` (2 tomadas por conceito, nano-banana-2.1/edit + refs, ~US$ 0,28); texto composto em PIL copiando `../008-franca/thumbs/compose.py`.

## Os 3 pares (título ↔ thumb)
| Braço | Título | Padrão (referência) | Thumb | Texto na arte |
|---|---|---|---|---|
| **A** | A história INTEIRA da Alemanha em 17 minutos | 1 · "The ENTIRE History of [país] in N Minutes" (Genius History Alemanha 260 mil) | `thumb-2-him.jpg` · panorama claro (Portão de Brandemburgo, catedral de Colônia, Reno com castelo e vinhedos, Neuschwanstein e os Alpes, cidade enxaimel) + bonequinho Bismarck com o capacete de ponta debaixo do braço e contorno de adesivo | **ALEMANHA** + "9 – 2026" (ano 9 = Teutoburgo, onde o roteiro começa; alternativa "843 – 2026") |
| **B** | Por que a Alemanha levou 1.000 anos para virar um país? | pergunta = pergunta central (teste v2 do `titulo.md`; padrão "Why Did [A] Unite While [B] Stayed Divided?", Ziro 41 mil) | `thumb-1-bonecos.jpg` · cena do hook: Guilherme I emburrado de braços cruzados no Salão dos Espelhos, oficiais de capacete de ponta erguendo espadas, criado francês horrorizado espiando atrás da porta dourada | **NASCEU AQUI?** + "1871" |
| **C** | Alemanha: a maior potência que nunca teve fronteira | 6 · "[País]: The [Superlativo] Country That Never Had [falta]" (HiM Rússia 43 mil) | `thumb-3-alemaoxalemao.jpg` · conflito cara a cara (o COROA × TURBANTE aprovado em 05/11): policial ocidental × guarda oriental, testa contra testa através do Muro de Berlim, raio amarelo | **ALEMÃO × ALEMÃO** + "1961" |

- **N = duração real arredondada.** Estimativa pelo ritmo real dos 006–008 (~128–131 ppm): 2.179 palavras ≈ 16:40–17:00. A etapa 2 troca o "17" se o render der outro número (título, descrição e banco). Se passar de 17:30, avise no relatório (bíblia: não passar de 17).
- Nenhum título entrega a resposta (a resposta é "a língua uniu cedo, o poder ficou em pedaços; o país nasceu pela guerra e a fronteira só parou com uma assinatura em 1990").
- Caracteres: A 44, B 56, C 51. Sem "em N minutos" no B e no C: a duração vai na descrição.
- O título C da pauta ("Alemanha: a maior potência da Europa que nunca teve fronteira fixa", 66) foi encurtado para caber nos 60.

## Por que o 3º estilo (conflito cara a cara no Muro)
É o único estilo que o Rodrigo aprovou de olho (COROA × TURBANTE, 05/11). O conflito "alemão contra alemão" é a imagem mais forte da pergunta do vídeo (onde fica a Alemanha?), é paradoxo puro (lacuna de informação) e é **seguro para anúncios**: nada de 1933–45 na thumb.

## Cuidados para as bases e a política de anúncios
- **Nenhuma thumb com nazismo, suástica, águia, braçadeira ou uniforme da Wehrmacht/SS** (brief do lote). Capacete de ponta (*Pickelhaube*) é imperial (1871) e pode; peça "no eagles, no emblems" (a águia imperial vira ruído e pode ser lida como símbolo).
- "ONE single continuous scene… no split panels" no 1 e no 3 (o 007 saiu com emenda de painel).
- Muro: "no weapons pointed" (a cena é de raiva, não de tiro); uniformes sem insígnias.
- HiM: se o céu livre vier com < 45% da altura, empurrar a cena para baixo e completar o topo com o degradê (truque do Irã v3). Neuschwanstein e a catedral de Colônia sem letras.
