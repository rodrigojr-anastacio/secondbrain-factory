# Pré-QA visual automático

- Alvo: `canais/lugares-guerra-en/videos/001-midway/preqa/grade_01_0m00-2m00.jpg` · 1 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.024 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 2 · médio 4 · baixo 2
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| — | Q01 `grade_01_0m00-2m00.jpg` | alto | texto_encavalado | P001: a ficha (caixa escura inferior) cobre o fim do texto do documento, e as linhas 'Enclosures' ficam cortadas e sobrepostas pela ficha. |
| — | Q01 `grade_01_0m00-2m00.jpg` | alto | elemento_fora | P009 Mapa2D: o rótulo 'HONOLULU' está cortado pela borda direita e atrás do selo '~40 PEOPLE LIVE THERE', que se sobrepõe ao ponto do mapa. O mapa está muito vazio, sem terra visível (areia), e a linha sai do quadro. |
| — | Q01 `grade_01_0m00-2m00.jpg` | medio | texto_cortado | P003 e P005: a ficha inferior cobre trechos do documento e o texto sai cortado pela borda do quadro, ainda que isso seja zoom DocGrifo intencional. Na P005 o marca-texto amarelo fica colado na ficha, o que prejudica a leitura. |
| — | Q01 `grade_01_0m00-2m00.jpg` | medio | valor_errado | P006: a conta '92 + 215 = 307' é mostrada com ênfase, mas o valor de 92 não aparece em nenhum outro lugar do storyboard e a contagem oficial parece incongruente com o documento (215). Conferir os dados. |
| — | Q01 `grade_01_0m00-2m00.jpg` | medio | elemento_fora | P012: o selo '1956 BANDED' no canto inferior direito se sobrepõe à imagem do albatroz e fica muito colado à borda. P016 e P017: os números (103 LAST KNOWN SURVIVOR) cobrem parte da imagem. |
| — | Q01 `grade_01_0m00-2m00.jpg` | medio | anacronismo | P014 e P021: documentos de página web moderna (captura de tela) usados como DocGrifo, texto minúsculo e ilegível em P021, com ficha sobre o texto em P014. Legibilidade fraca. |

2 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Quadros

Q01=grade_01_0m00-2m00.jpg
