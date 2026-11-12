# Pré-QA visual automático

- Alvo: `canais/lugares-guerra-en/videos/001-midway/preqa/grade_08_14m04-16m03.jpg` · 1 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.024 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 1 · médio 3 · baixo 2
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| — | Q01 `grade_08_14m04-16m03.jpg` | alto | texto_cortado | P173 e P175 (Cartela): o título no topo ('KAGA · ~5,400 M (17,700 FT) · OCT 2019' e 'ROV DIVES BELOW 5,100 M · SEP 2023') está cortado pela borda superior do quadro, com metade das letras fora de vista. |
| — | Q01 `grade_08_14m04-16m03.jpg` | medio | elemento_fora | P173/P175: a legenda 'YORKTOWN · ~3 MI' e o rótulo do perfil ficam sobre o fundo de areia/mar, e o ponto de Akagi fica na borda direita. Os marcadores ficam apertados, com pouca margem. |
| — | Q01 `grade_08_14m04-16m03.jpg` | medio | valor_errado | P172: o Número '3 MILES' com 'DOWN: YORKTOWN WRECK, FOUND 1998' tapa o canto da foto. O número fica sobre a ficha e os textos ficam apertados e pouco legíveis. |
| — | Q01 `grade_08_14m04-16m03.jpg` | medio | legenda | P164 e P168: a Ficha cobre parte do texto do documento, e o recorte do DocGrifo corta palavras nas bordas esquerda e direita. Pode ser simulação do storyboard, mas atrapalha a leitura da linha. |

2 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Quadros

Q01=grade_08_14m04-16m03.jpg
