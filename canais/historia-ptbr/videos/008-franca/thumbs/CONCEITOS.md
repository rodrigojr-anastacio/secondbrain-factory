# Títulos e thumbs · 008 França (etapa 1, 13/11/2026; bases e composição ficam para a etapa 2)

Regras: `biblia/titulo.md` (3 títulos de 3 padrões, pareados com 3 thumbs, nunca entregar a resposta; ≤ 60 caracteres) e `biblia/thumb.md` (padrão de entrega do 005: bonecos · HiM · 3º estilo). Prompts das 6 bases em `cenas-thumbs.json` (2 tomadas por conceito, nano-banana-2.1/edit + refs, ~US$ 0,28); texto composto em PIL copiando `007-russia/thumbs/compose.py` (fontes do `003-ira/v2-amostras/thumbs/base/compose.py`).

## Os 3 pares (título ↔ thumb)
| Braço | Título | Padrão (referência) | Thumb | Texto na arte |
|---|---|---|---|---|
| **A** | A história INTEIRA da França em 16 minutos | 1 · "The ENTIRE History of [país] in N Minutes" (HiM Egito 563 mil) | `thumb-2-him.jpg` · panorama claro (Torre Eiffel, Notre-Dame, Versalhes, Mont-Saint-Michel, castelo do Loire, vinhedos) + bonequinho Luís XIV de peruca e salto vermelho com contorno de adesivo | **FRANÇA** + "486 – 2026" (ano-símbolo = Clóvis/Soissons, regra do 005) |
| **B** | Por que a França matou o rei e nunca viveu sem um? | pergunta = pergunta central (teste v2 do `titulo.md`; tensão aberta como "Why Did A… While B…") | `thumb-3-reixpovo.jpg` · conflito cara a cara (o COROA × TURBANTE aprovado em 05/11): Luís XVI de coroa × revolucionário de barrete vermelho, testa contra testa, raio amarelo, guilhotina ao fundo | **REI × POVO** + "1793" |
| **C** | Como um machado decidiu quem manda na França | 5 · "How [X] Decided Who Ruled [país] for N Years" (HiM China 57 mil) | `thumb-1-bonecos.jpg` · Clóvis furioso com o machado erguido, o vaso de ouro amassado no chão, o guerreiro encolhido | **POR UM VASO?** + "486" |

- **N = duração real arredondada** (estimativa 15:30–16:00 pelo orçamento de ~2.000 palavras a ~128 ppm): a etapa 2 troca o "16" se o render der outro número (título, descrição e banco).
- Nenhum título entrega a resposta (a resposta é "a máquina do Estado continuou procurando alguém para o trono").
- B tem 51 caracteres, C 44, A 42. Sem "em N minutos" no B e no C: a duração vai na descrição.
- **Reservas da pauta (não usados):** "A Gália nunca morreu. Só mudou de nome." (padrão 7, HiM Irã 91 mil): o nosso roteiro não é sobre a Gália sobreviver, seria promessa que o vídeo não cumpre; "Por que a França se uniu e a Alemanha ficou dividida por 1.000 anos?" (Ziro 41 mil): bom para a sessão com a Alemanha de segunda, mas o vídeo só toca nisso em Verdun 843/1871; fica como braço extra se o B perder.

## Por que o 3º estilo (conflito cara a cara)
É o único estilo que o Rodrigo aprovou de olho (COROA × TURBANTE, 05/11) e o tema tem o conflito mais famoso da história da França (rei × povo, 1793), que é o centro da pergunta do vídeo. Lacuna: o título B pergunta "por quê"; a thumb mostra o choque.

## Cuidados para as bases (aprendizados de 005–007 na `biblia/thumb.md` e `visual.md`)
- "ONE single continuous scene… no split panels" no 1 e no 3 (o 007 saiu com emenda de painel).
- Coroa de Luís XVI: o nano-banana desenha coroa europeia, aqui é a certa. Barrete vermelho sem cocar tricolor escrito; "no flags".
- HiM: se o céu livre vier com < 45% da altura, empurrar a cena para baixo e completar o topo com o degradê (truque do Irã v3).
- "No blood, no gore" no 1 e no 3 (machado e guilhotina).
