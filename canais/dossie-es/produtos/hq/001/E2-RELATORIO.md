# Expedientes Secretos #1: etapa 2 (24/11/2026)

Decisão do Rodrigo (24/11, ~11:30): imagens pela fal, de dia (a janela do Codex é do vídeo da noite). Teto US$ 15.

## Imagens
| etapa | geradas | refeitas | obs. |
|---|---|---|---|
| teste de estilo | 4 nano-banana-2.1/edit + 2 gpt-image-2/edit | – | gpt-image-2 escolhido (casa com as págs. do Codex) |
| folhas de personagem | 8 | 0 | `arte-001/folhas/` |
| capas das histórias | 2 | 0 | KG01, KC01 |
| quadros | 133 | 2 | C1603 (filtro de imagem preta: prompt suavizado), C1401 (avião errado: pedido U-2 pelo formato) |
| wallpapers | 4 (W03–W06) | 0 | W01/W02 da amostra v3 |
| pôsteres (ajuste do Rodrigo) | 2 (A mural, C cartaz) | 0 | PO01 não gerado (era quase a capa) |

QA de todas as imagens em pranchas (personagem, texto, moldura, insígnia, época): 0 molduras, 0 suásticas (a Cruz de Ferro do G1505 sai sem símbolo no centro), sem gore.

## Custo (fal.ai, real pelo uso do endpoint)
- Total: **US$ 9,54** (`financas.consumo`, notas `dossie-hq-001 …`; inclui testes US$ 0,33 e ajuste de US$ 0,24 de uso que entrou atrasado entre lotes).
- Por imagem: 16:9 US$ 0,053 · 2:3 US$ 0,062 · 1:1 US$ 0,073 · A3 US$ 0,12–0,14.
- Saldo fal: US$ 52,42 → 42,99 (inclui o que outros jobs gastaram no período).

## Diagramação
- `autolayout.py` reposiciona balões/legendas/onomatopeias olhando a arte; 7 ajustes manuais no roteiro (dict no texto) e 1 `foco`.
- Página final: CTA de inscrição + QR (`qr-canal.png`, URL fixa do canal) + link clicável (anotação no PDF).
- "TU PÓSTER" mostra a miniatura do pôster C (padrão até o Rodrigo escolher).

## Pacote (`001/pacote/`, fora do git)
- `Expedientes-Secretos-1.pdf`: 42 páginas, 6×9 pol. (1600×2400 px/pág.), 23 MB, link clicável na p. 41.
- Pôsteres A3 300 dpi (3508×4961), png + pdf: A e C, com e sem título.
- 6 wallpapers (3 celular 1440×3120, 3 desktop 3840×2160) com marca discreta.
- `Expedientes-Secretos-1.zip` (48 MB): PDF + pôster escolhido (padrão C) + 6 wallpapers + LEEME.txt.
- Prévias ≤ 1 MB em `001/previas/`.

## Como refazer
```
tools/.venv/bin/python canais/dossie-es/produtos/hq/001/tools/rodar_fal.py --ordem 1,2,3,5   # imagens (pula as que existem)
tools/.venv/bin/python canais/dossie-es/produtos/hq/001/montar.py --pdf                       # rascunho com balões automáticos
tools/.venv/bin/python canais/dossie-es/produtos/hq/001/tools/extras_pacote.py # QR, pôsteres, wallpapers, miniatura
tools/.venv/bin/python canais/dossie-es/produtos/hq/001/tools/pacote.py   # PDF final (41 pp, 2 pôsteres no zip), prévias, zip
```
