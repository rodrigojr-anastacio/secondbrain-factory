# Pré-QA visual automático

- Alvo: `canais/lugares-guerra-en/videos/005-tarawa/preqa` · 10 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.057 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 0 · médio 4 · baixo 3
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| — | Q05 `grade_r_05.jpg` | medio | fundo/faixa | Nos P094 (6:46) e P101 (7:17), uma faixa vermelha/branca (a bandeira do caixão) aparece em toda a base do quadro, sobre a ficha. Pode ser só o enquadramento da foto, mas parece uma faixa chapada de cor no rodapé. Conferir. |
| — | Q07 `grade_r_07.jpg` | medio | valor_errado | P146 (11:13) mostra 'Número 1 TEETH' e P149 (11:28) mostra '3 ISOTOPES'. O valor pode estar no início da animação do contador, e 'TEETH' no singular com '1' pode ser texto incompleto. Conferir o valor final. |
| — | Q09 `grade_r_09.jpg` | medio | texto_cortado | P194 e P196 (DocGrifo, 14:54/14:55 e 15:01/15:02): o documento escaneado está cortado pelas bordas direita/esquerda, e a primeira linha aparece cortada no topo. Pode ser zoom intencional do DocGrifo, mas o texto lido fica incompleto. |
| — | Q10 `grade_r_10.jpg` | medio | texto_cortado | P210 e P212 (DocGrifo, 15:59, 16:08 e 16:09): linhas do documento cortadas pela borda direita e pelo topo (primeira linha pela metade). Provavelmente zoom intencional, mas a legibilidade é fraca. |

3 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q10 (grade_r_10.jpg): faixa preta na borda base: 4% do quadro

## Quadros

Q01=grade_r_01.jpg, Q02=grade_r_02.jpg, Q03=grade_r_03.jpg, Q04=grade_r_04.jpg, Q05=grade_r_05.jpg, Q06=grade_r_06.jpg, Q07=grade_r_07.jpg, Q08=grade_r_08.jpg, Q09=grade_r_09.jpg, Q10=grade_r_10.jpg
