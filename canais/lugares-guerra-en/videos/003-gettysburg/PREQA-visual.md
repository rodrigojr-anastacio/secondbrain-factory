# Pré-QA visual automático

- Alvo: `canais/lugares-guerra-en/videos/003-gettysburg/preqa` · 9 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.036 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 0 · médio 3 · baixo 1
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| — | Q07 `grade_r_07.jpg` | medio | texto_cortado | 12:19 P148 Cartela: a citação "THE WORLD WILL LITTLE NOTE, NOR LONG RE" termina com cursor no meio da palavra. Provavelmente é animação de digitação, mas confirmar que o texto completo aparece antes do corte. |
| — | Q04 `grade_r_04.jpg` | medio | outro | 6:15 P077 Mapa2D: o rótulo "TRENTON" e o ponto vizinho se sobrepõem, e o texto fica pequeno e quase ilegível. O selo SCHEMATIC está no canto. |
| — | Q02 `grade_r_02.jpg` | medio | texto_encavalado | 1:45 P023 Mapa2D: os rótulos HARRISBURG, GETTYSBURG, WASHINGTON, FREDERICKSBURG e o título "LEE MARCHES NORTH" ficam amontoados e se sobrepõem. A leitura é difícil. |

1 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q09 (grade_r_09.jpg): faixa preta na borda base: 27% do quadro
- Q09 (grade_r_09.jpg): faixa preta na borda direita: 33% do quadro

## Quadros

Q01=grade_r_01.jpg, Q02=grade_r_02.jpg, Q03=grade_r_03.jpg, Q04=grade_r_04.jpg, Q05=grade_r_05.jpg, Q06=grade_r_06.jpg, Q07=grade_r_07.jpg, Q08=grade_r_08.jpg, Q09=grade_r_09.jpg
