# Teste de estilo visual: dossie-ptbr (2026-11-04)

Custo: **US$ 0,79** em fal.ai (`financas.consumo` ids 24–27, `ref_id` = 6, o vídeo piloto KGB). Teto do brief: US$ 3.
Cenas: `cenas-estilo.json` (5 cenas do piloto: ponte de Waterloo 1978, Lubyanka 1918, mapa, arquivista, base de thumb). Estilo: `visual.estilo_prompt` do `canal.yaml`. Seed 7.
As imagens ficam fora do git (`testes/estilo-*/`, `grade-estilo.jpg`, `grade-nano-16x9.jpg`).

| Modelo | US$/img | Saída | Avaliação (visão) |
|---|---|---|---|
| `fal-ai/flux-pro/v1.1` | 0,040 | 1024×576 | Pintura realista, **não** é quadrinho de tinta; resolução baixa para o Ken Burns (ver `anti-padroes.md` #1); o mapa saiu com pinos errados. Thumb bonita. |
| `fal-ai/recraft/v3/text-to-image` | 0,040 | 1820×1024 | Quase fotografia, ignora o "ink illustration"; inventou texto no mapa ("MBC"). A resolução é a melhor. |
| `fal-ai/nano-banana` (1:1) | 0,039 | 1024×1024 | O traço certo, mas quadrado: o `img_fal.py` mandava só `image_size`. |
| **`fal-ai/nano-banana` (16:9)** | 0,039 | **1344×768** | **Escolhido.** Graphic novel com contorno grosso, paleta azul-ardósia/sépia com vermelho pontual, rostos adultos e época correta (Routemaster + St Paul's; Lubyanka amarela com guardas de couro). Defeitos: (1) o mapa veio com 2 oficiais em volta; (2) a thumb tem letreiro falso no prédio. |
| `fal-ai/imagen4/preview/fast` | 0,020 | — | **HTTP 404** em todas (endpoint mudou; o id na tabela de preços do `img_fal.py` está velho). Sem custo. |
| `gpt-image-2` medium (OpenAI) | ~0,042 | — | **"You have no credits remaining"**: o saldo real da OpenAI está zerado em 2026-11-04 (o banco mostra −US$ 9,87). Sem custo. |

## Decisões
- `canal.yaml`: `gerador: fal`, `modelo: fal-ai/nano-banana`.
- `tools/img_fal.py`: com `tamanho: landscape_16_9`, manda também `aspect_ratio: "16:9"` (sem isso o nano-banana sai 1:1).
- Para mapas, o prompt precisa dizer "top-down flat map only, no people, no hands, no table". Para a thumb, "no signage, no lettering on buildings". Os rótulos e o texto vão sempre no código (Remotion).
- **Hipótese:** 1344×768 aguenta um zoom de até ~1,15× em 1080p sem virar borrão. Confira a nitidez (variância do Laplaciano, como no QA do Egito) no 1º render; se reprovar, use o recraft só nos planos com zoom maior ou faça upscale.
