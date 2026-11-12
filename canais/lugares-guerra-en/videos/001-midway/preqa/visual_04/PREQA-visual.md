# Pré-QA visual automático

- Alvo: `canais/lugares-guerra-en/videos/001-midway/preqa/grade_04_6m02-8m05.jpg` · 1 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.012 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 1 · médio 2 · baixo 3
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| — | Q01 `grade_04_6m02-8m05.jpg` | alto | valor_errado | P073 (Número): o texto "41 → 6 TORPEDO BOMBERS IN → BACK" é confuso e a seta repetida dificulta a leitura. P074 mostra "15 / 15 PLANES LOST" sobre a foto, e esse dado conflita com o 41→6 anterior (Torpedo Squadron 8 teve 15 aviões). Os números precisam de conferência. |
| — | Q01 `grade_04_6m02-8m05.jpg` | medio | elemento_fora | P071 (Mapa2D): o mapa é só fundo azul com linhas e rótulos, sem terra nem contexto geográfico. Ao contrário da bíblia (terra areia, Natural Earth), parece placeholder. Os rótulos "TORPEDO SQUADRONS" e "JAPANESE CARRIERS" ficam encavalados perto das linhas. |
| — | Q01 `grade_04_6m02-8m05.jpg` | medio | outro | Repetição: vários planos marcados REUSO (P069, P078, P087, P090, P091) e as mesmas fotos aéreas do Kaga/Hiryu aparecem em P076, P078, P082, P083, P087. Também P079 e P081 mostram o mesmo céu. Isso enfraquece o ritmo. |

3 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Quadros

Q01=grade_04_6m02-8m05.jpg
