# Teste: cenas do Dossier direto na Gemini API (AI Studio) — 23/11/2026

**Resultado: BLOQUEADO, nenhuma imagem gerada, US$ 0 gasto.** A chave de teste (`~/.segredos/gemini-teste.env`) é de um projeto **sem faturamento (Free Tier)**, e a Gemini API **não tem free tier para imagem** (limite 0). `canal.yaml`, bíblia, `tools/` e pipeline não foram alterados.

## O que aconteceu
| Chamada | Resposta |
|---|---|
| `gemini-2.5-flash-image` (A), 6 cenas, `generateContent` | **HTTP 429** `RESOURCE_EXHAUSTED`: `generate_content_free_tier_requests, limit: 0` (por minuto e por dia) e `free_tier_input_token_count, limit: 0`; "Please retry in 18h56m" |
| `gemini-3.1-flash-image` (B), 6 cenas | idem (429, free tier, limite 0) |
| `gemini-nano-banana-2.1` e `gemini-3.1-flash-lite-image` (sonda de 1 chamada) | idem |
| Batch (`batchGenerateContent`, nano-banana-2.1, 1 pedido) | **HTTP 400 `FAILED_PRECONDITION`** ("Precondition check failed"): Batch exige projeto pago |
| `models.list` | funciona e lista os modelos de imagem (por isso parecia ok: listar não exige faturamento) |

Cada cena tentou 4× com espera crescente (15/30/45/60 s, ~151 s por cena): 24 respostas 429 por modelo, todas por cota free tier = 0, não por limite de taxa de conta paga. Logs: `A-2.5-flash-image/gemini_log.jsonl`, `B-3.1-flash-image/gemini_log.jsonl`, `A.log`, `B.log`.

Observação lateral: `gemini-2.5-flash` (texto) responde 404 "no longer available to new users" → o projeto é tratado como **usuário novo**; o `gemini-2.5-flash-image` ainda aceita chamadas (a doc o marca como legado, desligamento em 15/03/2027).

## O que o Rodrigo precisa fazer (2 min)
No AI Studio (https://aistudio.google.com/apikey → projeto da chave → "Set up billing"), **ativar o faturamento** (conta de faturamento do Google Cloud com cartão) do projeto da chave, ou criar já o projeto próprio do Dossier com faturamento e gerar a chave nele. Depois é só rodar de novo (comandos abaixo); o protótipo está pronto.

## Como rodar quando o faturamento estiver ativo (teto ~US$ 1)
```
cd canais/dossie-es/testes/gemini-2026-11-23
set -a; . ~/.segredos/gemini-teste.env; set +a
P=~/workspace/fabrica-youtube/tools/.venv/bin/python
rm -rf A-* B-*        # logs desta tentativa
$P gemini_img.py padrao gemini-2.5-flash-image cenas-amostra.json A-2.5-flash-image          # ~US$ 0,24
$P gemini_img.py padrao gemini-3.1-flash-image cenas-amostra.json B-3.1-flash-image --size 1K # ~US$ 0,40
$P gemini_img.py padrao gemini-nano-banana-2.1 cenas-amostra.json C-nb21 --size 1K --thinking minimal  # ~US$ 0,20 (opcional)
$P gemini_img.py batch  <melhor> cenas-amostra.json batch-<melhor> --size 1K --espera-min 40   # ~US$ 0,10–0,12
```
Depois: `checa_imagens.py` (de `videos/015-gru/tools/`) nas pastas, grade `comparativo.jpg` (fal × A × B × Codex) e os números no fim deste arquivo.

## Protótipo `gemini_img.py` (pronto, não testado com imagem real)
- REST `v1beta/models/<m>:generateContent`, header `x-goog-api-key` (chave nunca impressa nem gravada), `responseModalities: ["IMAGE"]`, `imageConfig.aspectRatio "16:9"` + `imageSize "1K"` (exceto 2.5-flash-image, que não aceita tamanho), `thinkingConfig` opcional.
- Prompt = prompt da cena + `visual.estilo_prompt` do `canal.yaml` (mesmo contrato do `img_fal.py`); `--refs` (até 3) inline como referência de estilo com instrução antes do prompt.
- Detecta bloqueio (`promptFeedback.blockReason`, `finishReason` sem imagem) e imagem preta/vazia; reescala para 1536×864 JPEG; mede tempo; custo por imagem = `usageMetadata` × preço oficial.
- Batch: pedidos inline com `metadata.key` = id da cena, poll a cada 60 s até `--espera-min`, salva `batch_resumo.json`.

## Preços oficiais (aistudio.google.com/docs/pricing, lido em 23/11/2026) e projeção para ~200 imagens/vídeo
| Modelo | US$/img padrão | US$/img Batch | 200 img padrão | 200 img Batch |
|---|---|---|---|---|
| `gemini-2.5-flash-image` (= nano-banana da fal) | 0,039 | 0,0195 | 7,80 | 3,90 |
| `gemini-3.1-flash-image` (Nano Banana 2) 1K | 0,067 | sem Batch listado | 13,40 | — |
| `gemini-nano-banana-2.1` 1K | 0,0336 (+ thinking a US$ 7,50/M) | 0,0168 | 6,72 | 3,36 |
| `gemini-3.1-flash-lite-image` 1K | 0,0336 | 0,0168 | 6,72 | 3,36 |
| fal nano-banana (hoje) | 0,039 | — | 7,80 | — |
| Codex (Plus) | 0 | — | 0 | — |

## Recomendação (provisória, sem imagem para comparar)
1. Ativar faturamento no projeto (decisão do Rodrigo) e rodar o teste acima (~US$ 1).
2. Expectativa: **2.5-flash-image** dá o mesmo visual da fal pelo mesmo preço (é o mesmo modelo) e em **Batch** sai pela metade (~US$ 3,90/vídeo); o **nano-banana-2.1** é o candidato mais barato e mais novo (~US$ 3,36/vídeo em Batch), mas precisa provar que segura a paleta dessaturada da bíblia. O 3.1-flash-image (NB2) custa ~1,7× a fal e não tem Batch: só vale se a qualidade for muito superior.
3. Se aprovar: `tools/img_gemini.py` com o mesmo contrato do `img_fal.py` (trava por pasta, custo em `financas.consumo` com fornecedor "Google Gemini API"), `visual.gerador: gemini` + `gerador_fallback: codex`, e modo Batch para a etapa 2 noturna (submete tudo de uma vez, poll; o Batch promete até 24 h, então precisa de fallback padrão se não voltar em ~1 h).

## Custo deste teste
US$ 0 (todas as chamadas recusadas antes da geração; nada registrado em `financas.consumo`).
