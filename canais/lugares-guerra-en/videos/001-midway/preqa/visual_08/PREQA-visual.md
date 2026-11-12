# Pré-QA visual automático

- Alvo: `canais/lugares-guerra-en/videos/001-midway/preqa/grade_08_14m04-16m03.jpg` · 1 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.016 · `tools/preqa_visual.py`
- Resultado: **REPROVADO (há bloqueante)** · bloqueante 1 · alto 2 · médio 3 · baixo 2
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| — | Q01 `grade_08_14m04-16m03.jpg` | bloqueante | texto_encavalado | P170 (Mapa2D): rótulos 'KAGA (WRECK)', 'AKAGI (WRECK)' e 'YORKTOWN (WRECK)' se sobrepõem no centro do mapa, ficando ilegíveis. Os pontos estão quase colados. |
| — | Q01 `grade_08_14m04-16m03.jpg` | alto | fundo/faixa | P170 (Mapa2D): fundo é só azul-escuro chapado, sem terra nem linha de costa. O mapa fica vazio e não se lê como mapa (contraria o Natural Earth areia/mar da bíblia). |
| — | Q01 `grade_08_14m04-16m03.jpg` | alto | valor_errado | P176: o número '5,100 M / DEEPEST DIVES' aparece sobre foto do Kaga de c. 1936, sem relação com o conteúdo, e a legenda 'DEEPEST DIVES' está espremida abaixo do número. Também há inconsistência entre 5.400 m (P173) e 5.100 m. |
| — | Q01 `grade_08_14m04-16m03.jpg` | medio | elemento_fora | P172: o número '3 MILES' com a legenda 'DOWN · YORKTOWN, 1998' sobrepõe a ficha/canto inferior direito da foto. A legenda pequena fica espremida e a data '1998' contradiz a foto de 1942 e o contexto. |
| — | Q01 `grade_08_14m04-16m03.jpg` | medio | legenda | P164, P168 e P171 (DocGrifo): a ficha escura cobre parte do texto do documento e, no P164, a ficha fica sobre o parágrafo, atrapalhando a leitura. No P168 o marca-texto está fraco, só em 'root cause is not immediately evident'. |
| — | Q01 `grade_08_14m04-16m03.jpg` | medio | outro | P174, P175, P176 e P177: o mesmo porta-aviões (Akagi/Kaga) em fotos P&B muito parecidas se repete em planos curtos (P174 e P177 são praticamente a mesma imagem). Os planos Cartela P173 e P175 também são quase idênticos (DEPTH PROFILE, sem gráfico real) e vazios. |

2 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Quadros

Q01=grade_08_14m04-16m03.jpg
