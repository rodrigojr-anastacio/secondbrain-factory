# Teste de estilo es (CIA): dossie-es (2026-11-04)

Complementa `ESTILO.md` (teste original de 04/11, feito para o piloto KGB em pt, que escolheu o `fal-ai/nano-banana`). Objetivo: confirmar o estilo nas cenas do piloto es (América Latina, EUA anos 50–60) e comparar com o `fal-ai/flux/dev`, que o `historia-ptbr` 003 passou a usar porque a OpenAI está sem crédito.

Custo: **US$ 0,384** em fal.ai (6 × 0,039 nano-banana + 6 × 0,025 flux/dev), em `financas.consumo` com `ref_id` = 7 (piloto CIA). Cenas: `cenas-es-cia.json` (seed 11). Imagens e grades fora do git: `es-cia-nano-banana/`, `es-cia-flux-dev/`, `grade-es-nano.jpg`, `grade-es-flux.jpg`.

| Cena | nano-banana (1344×768) | flux/dev (1024×576) |
|---|---|---|
| C1 rádio, Guatemala 1954 | Família em volta do rádio, vulcão na janela e crucifixo; traço de tinta certo. | Bom clima, mas os rostos são jovens e repetidos, e o traço é de pôster. |
| C2 Langley | Prédio branco modernista, sedãs pretos e homens de chapéu. Ótimo. | Fotográfico, com carros dos anos 70 e bandeira. Época errada. |
| C3 mapa das Américas | Limpo e sem texto, mas os **pinos caíram no México, na Colômbia e no Brasil** (pedi Guatemala, Cuba e Chile) e aparece a borda de uma mesa. | **Inventou texto** ("ROCA", "CLORA"); recorte errado. |
| C4 Bahía de Cochinos | Desembarque, barco em chamas e avião. Ótimo. | Bom, mas com menos gente e menos tensão. |
| C5 escritório anos 50 | Diretor de cachimbo, luminária verde e persianas. Ótimo. | Bom, com cara de capa de revista. |
| C6 base de thumb | Agente de fedora à esquerda, com pasta e selo vermelho; metade direita de céu livre. **Pronta para o layout.** | Agente de perfil, olhando para fora do quadro, sem espaço limpo para o título. |

## Decisões
- Fica o **`fal-ai/nano-banana`**: estilo coerente com o teste anterior, resolução maior e nenhum texto inventado.
- **Mapas:** nenhum modelo acerta a posição dos pinos. O prompt do mapa leva "no pins, no markers" e os pinos e setas são **desenhados no código** (Remotion) sobre a base. Acrescentar "flat scan of the map only, no table, no frame".
- Rostos de pessoas reais (Dulles, Árbenz, Castro): gerar como "a man resembling a 1950s official" e conferir com visão; nunca usar foto.
