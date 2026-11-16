# Thumbs extra D/E · 004-pearl-harbor · 16/11/2026

Pedido direto do Rodrigo (16/11): 2 thumbs de padrão diferente das A/B/C ("uma pegada que mostre o avião, a ilha, explosão"). Sem crivo formal; autoavaliação a 320×180 em `comparativo.jpg`. Vídeo, títulos e pacote **não** mudaram.

| Thumb | Padrão | Texto | Título que casa | Por que difere das A/B/C |
|---|---|---|---|---|
| **D** `thumb-D.jpg` | `cena-acao` / panorama aéreo | **7:55 AM** + selo RESTRICTED | A: "Why Are There Still Bullet Holes at Pearl Harbor?" (a thumb mostra a manhã que fez os buracos; a hora é a do cap. "7:55") | A/B/C = muro claro em close + crateras, sem ação. D = vista aérea: battleship row ao lado de Ford Island, explosão laranja com coluna de fumaça e um bombardeiro mergulhando em primeiro plano, mar turquesa |
| **E** `thumb-E.jpg` | `cena-acao` / ângulo baixo | **NEVER FIXED** + selo RESTRICTED | B: "The Pearl Harbor Wall Tourists Aren't Allowed to See" (a thumb mostra o muro sendo metralhado; o texto diz que as marcas ficaram) | Avião enorme vindo para a câmera (~45% do quadro), rajada batendo no quartel art déco, hangar explodindo. Herói = avião + fogo, não o muro parado |

**Autoavaliação 320×180:** D: "7:55 AM" e explosão legíveis; navios pequenos, mas a leitura (ataque aéreo no porto) é imediata. E: a mais forte das 5 (1 foco, contraste alto). As duas diferem de verdade das A/B/C (cena de ação × objeto parado) e entre si (aérea × ângulo baixo). Não refiz.

**Bases:** `fal-ai/nano-banana` via `tools/img_fal.py` (estilo do `canal.yaml`), prompts em `cenas-extra.json` e `cenas-extra-r2.json`; sem texto na base, texto em `compor.py` (Anton `#FDD505`, contorno tinta). Usadas: **D4** (recortada em 16:9 dentro do conteúdo: o nano-banana desenhou moldura branca) e **E1**. Descartadas: D1/D2 (moldura branca + disco vermelho nas asas), D3 (o `estilo_prompt` "cutaway" do canal venceu e saiu um corte sem cena), E2 (convés; boa reserva). Sem cadáver, sem pessoa, sem bandeira/sol nascente. Nota: os círculos ciano nas asas do E1 não são insígnia histórica (licença de ilustração).

**Aprendizado (Hipótese):** o `estilo_prompt` do canal (cutaway) atrapalha cena de ação; nano-banana deu moldura em 3 de 6.

**Custo:** US$ 0,239 (6 imagens nano-banana, real pelo uso do endpoint), registrado em `financas.consumo` com `ref_id` 42.
