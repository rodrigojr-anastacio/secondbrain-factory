# Teste: cenas do Dossier direto na Gemini API (AI Studio) — 23/11/2026 (2ª tentativa)

**Resultado: `gemini-nano-banana-2.1` em modo padrão é o melhor (6/6, sem moldura, sem letras, estilo e paleta do canal). Batch funcionou, mas levou 34,8 min e bloqueou 4/6 no filtro.** Custo do teste: **US$ 0,78** (teto US$ 1), lançado em `financas.consumo` (fornecedor "Google Gemini API", 4 linhas). `canal.yaml`, bíblia, `tools/` e pipeline não foram alterados.

A 1ª tentativa (manhã) parou em `BLOQUEIO.md` (projeto Free Tier, limite 0). Esta usou `~/.segredos/gemini.env` (projeto com faturamento). Mesmas 6 cenas da amostra Codex (`cenas-amostra.json`, do `videos/015-gru/cenas.json`), prompt da cena + `visual.estilo_prompt` do `canal.yaml`, **sem refs** (o Dossier não usa refs no fal: `fal-ai/nano-banana` texto→imagem), 16:9.

Grade: `comparativo.jpg` (fal original × A × B × C nano-banana-2.1 × Codex; jpg fora do git, fica na VPS).

## Números
| Modelo (modo) | Chamadas | OK | IMAGE_SAFETY | Moldura/faixa (detector) | Letras | s/img | US$/img ok | 200 img/vídeo |
|---|---|---|---|---|---|---|---|---|
| A `gemini-2.5-flash-image` (= nano-banana da fal) | 8 (6 + 2 retries) | 5/6 | 3 (I002 1×, I056 2×) | **3/5** (I001, I012 moldura clara; I115 faixa preta) | "PASSPORT" no I008 | 7,8 | 0,039 | ~US$ 7,80 + ~20% refação |
| B `gemini-3.1-flash-image` 1K | 8 (6 + 2) | 4/6 | 4 (I002 2×, I056, I001 1×) | 0 | não | 13,6 | 0,069 | ~US$ 13,70 + muitos bloqueios |
| **C `gemini-nano-banana-2.1` 1K** | 6 | **6/6** | 0 | 0 | não (só rabiscos ilegíveis) | 19,7 | **0,045** (≈0,034 imagem + thinking) | **~US$ 8,90** |
| C em **Batch** | 6 | 2/6 | **4** (I001, I002, I008, I056) | 0 | não | 34,8 min o lote | 0,021 | ~US$ 4,30 (se não bloqueasse) |
| fal nano-banana (hoje) | — | — | — | ~15–25% moldura | às vezes | — | 0,039 | US$ 7,80 |
| Codex (Plus) | — | 6/6 | — | — | não | ~60–90 | 0 | 0 |

Sem nenhum 429 (paralelo 2, nenhum limite de taxa encontrado). Bloqueio falhado custa ~US$ 0,0001 (só o prompt).

## Leitura visual (comparativo.jpg)
- **A (2.5-flash-image):** idêntico ao fal (é o mesmo modelo): traço limpo, paleta certa, mas repete os defeitos conhecidos: moldura/letterbox em metade das imagens e texto inventado ("PASSPORT"). Bloqueia retrato de pessoa real (Gurevich) e a van com antena.
- **B (3.1-flash-image / NB2):** quando sai, é bonito e detalhado, mas bloqueia demais (I001 rua de Bruxelas 1941 e I002 bloqueados na 1ª; I056 sempre) e custa 1,7× a fal. Descartado.
- **C (nano-banana-2.1):** o mais próximo da bíblia (tinta preta forte, slate/oliva/sépia, vermelho pontual), mais detalhe de época que o fal, enquadramento cheio sem moldura, mapa I012 limpo. Ficou um pouco mais "ilustração detalhada/escura" que o fal (menos chapado) e na linha do Codex. Passou todas as cenas no modo padrão, inclusive I056 e o retrato do I002.
- **Batch com o mesmo modelo e o mesmo prompt bloqueou 4/6**: o filtro no Batch parece mais rígido (ou sem o thinking dinâmico que ajusta o prompt). Hipótese, 1 lote só.

## Recomendação
1. **Trocar a fal por `gemini-nano-banana-2.1` em modo padrão (1K, 16:9)** para o Dossier: ~US$ 0,045/img ≈ **US$ 9/vídeo de 200 imagens**, ~20 s/img (paralelo 4 → ~17 min por vídeo), sem moldura e sem letras nesta amostra (economiza o recorte e as refações do fal). Testar `--thinking minimal` no 1º lote real (pode cair para ~US$ 0,034/img = US$ 6,70).
2. **Batch não vale agora:** metade do preço, mas 35 min para 6 imagens e 4/6 bloqueadas. Se for testado de novo, só como 1º passo noturno com fallback automático: o que vier bloqueado/atrasado vai para o modo padrão.
3. Pipeline (decisão do Rodrigo, não feito aqui): `tools/img_gemini.py` com o mesmo contrato do `img_fal.py` (lê `canal.yaml`, trava `.img.lock` por pasta, pula prontas, custo em `financas.consumo` com fornecedor "Google Gemini API" e `ref_id` do vídeo, via `usageMetadata`), `visual.gerador: gemini` + `modelo: gemini-nano-banana-2.1` + `gerador_fallback: codex`; em IMAGE_SAFETY, tentar 1× de novo e depois cair no Codex. Detector `checa_imagens.py` continua no fim. Criar o projeto/chave próprios do Dossier (o Rodrigo).
4. Preço oficial lido em 23/11/2026 (aistudio.google.com/docs/pricing): 2.5-flash-image US$ 0,039/img (Batch 0,0195); 3.1-flash-image 1K US$ 0,067 (+ entrada); nano-banana-2.1 1K US$ 0,0336/img + thinking a US$ 7,50/M (Batch metade).

## Como reproduzir
```
cd canais/dossie-es/testes/gemini-2026-11-23
set -a; . ~/.segredos/gemini.env; set +a
P=~/workspace/fabrica-youtube/tools/.venv/bin/python
$P gemini_img.py padrao gemini-nano-banana-2.1 cenas-amostra.json C-nano-banana-2.1 --size 1K
$P gemini_img.py batch  gemini-nano-banana-2.1 cenas-amostra.json batch-nano-banana-2.1 --size 1K --espera-min 40
# retomar lote já criado: --nome batches/<id>
$P ../../videos/015-gru/tools/checa_imagens.py C-nano-banana-2.1
```
Logs por imagem (uso, custo, tempo, erro): `*/gemini_log.jsonl`; lote: `batch-nano-banana-2.1/batch_resumo.json`.
