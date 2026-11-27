# CTA de inscrição do Dossier en Minutos · 27/11/2026

Decisão do Rodrigo (27/11/2026, não mude sem pedido dele). Regra na bíblia: `../../biblia/roteiro.md` (Estrutura, item 6) e `../../biblia/visual.md` (Botão SUSCRÍBETE). **Não é o CTA da HQ** (`../LEIA.md`), que continua igual.

- **Frase fixa**, falada pelo narrador do canal como bloco normal do roteiro: "Si te está gustando este expediente, suscríbete. Así nos ayudas a seguir investigando y contando historias como esta." (`TEXTO` em `inscricao.py`).
- **Lugar:** último bloco de um expediente forte, ~60% (55–70%), ≥ 2 min do CTA da HQ (~37,5%). Um só por vídeo.
- **Botão** "SUSCRÍBETE" animado no canto superior direito enquanto a frase toca (`BotonSuscribete.jsx`), com clique e sininho.

## O que tem aqui
| arquivo | o quê | git? |
|---|---|---|
| `inscricao.py` | texto, regras e os 3 comandos (`roteiro`, `montar`, `qa`) | sim |
| `BotonSuscribete.jsx` | componente Remotion do botão (fonte única; o `montar` copia para `src/` do vídeo) | sim |
| `tools/amostra.py`, `tools/render_amostra.sh` | amostra de ~23 s a partir do 016 (pelo mesmo caminho da produção) | sim |
| `voz/dossie-cta-inscricao.json`, `voz/palavras.json` | entrada do Fish da amostra e tempos por palavra (Whisper) | sim |
| `voz/v1/INSCRICAO.mp3` | voz da amostra (Fish s2.1-pro, "Dio Historias", 1,0×, `--por-frase` como na produção; Whisper 100%) | não |
| `amostra.mp4`, `amostra-frames.jpg` | amostra e prévia (20 quadros) | não (Drive: `Youtube/Dossier en Minutos/_amostras/cta-inscricao/`) |

## Na esteira (vídeo novo, `V = canais/dossie-es/videos/NNN-slug`)
1. **Roteiro** (etapa 1): no `roteiro.py`,
   ```python
   import sys; sys.path.insert(0, str(Path.home() / "workspace/fabrica-youtube/canais/dossie-es/cta/inscricao"))
   from inscricao import TEXTO as CTA_INSCRICAO
   b("<re-hook que fecha o expediente e abre o próximo>", ...)
   b(CTA_INSCRICAO, "<chave de reuso>#<enq>", "<chave de reuso>#<enq>", ideia=True)   # último bloco do expediente
   cap("N. ...")
   ```
   Depois de `python3 roteiro.py`: `tools/.venv/bin/python canais/dossie-es/cta/inscricao/inscricao.py roteiro $V` → APROVADO (cole no `ETAPA1.md`). Reprovado: ele lista os lugares válidos ("depois de N0xx (capítulo) ~61%"); mova o bloco para lá. Estimativa com WPS 2,38 e o CTA da HQ encaixado; no 016 deu 62,3% contra 62,2% real.
2. **Voz:** nada especial (o bloco vai com os outros; não ponha a frase no glossário de pronúncia).
3. **Montagem** (etapa 2): depois do `tools/build.py` e **antes do render**:
   `tools/.venv/bin/python canais/dossie-es/cta/inscricao/inscricao.py montar $V` → põe `inscricao` na `src/timeline.json` (entra 0,2 s antes da fala, clique no "-críbe-" pelo Whisper do `audio/<bloco>.mp3`, sai 0,4 s depois), copia `BotonSuscribete.jsx` para `src/`, liga o `Video.jsx` (import + `<Sequence>` antes do `<Audio … mix.wav>`; idempotente), soma clique + sininho ao `public/audio/mix.wav` (uma vez por `mix.wav`) e grava `qa/cta-inscricao.json`. Código 1 = fora de 55–70% ou a < 120 s da HQ. **Rodou o `build.py` de novo? Rode o `montar` de novo** (o build reescreve timeline e mix).
4. **QA:** depois do render: `tools/.venv/bin/python canais/dossie-es/cta/inscricao/inscricao.py qa $V` → Whisper da frase (≥ 85% das palavras), posição 55–70%, ≥ 120 s do CTA da HQ e botão visível (quadro antes do clique: vermelho e papel na área do botão) → `qa/cta-inscricao-qa.json` e `qa/cta-inscricao.jpg` (olhe o quadro). Código 1 = reprovado.

## Amostra (27/11/2026)
`tools/.venv/bin/python canais/dossie-es/cta/inscricao/tools/amostra.py && canais/dossie-es/cta/inscricao/tools/render_amostra.sh` (render na VPS, ~2 min, `$TMPDIR/cta-inscricao-amostra`). 016-mkultra 8:26–8:47 (fim do Expediente 8 "La Silla": "Ese mismo mes, un informe del inspector general…"), a frase (7,6 s) sobre 2 planos de reuso do capítulo (I126, I128) com o botão e o cartão do Expediente 9 "La Selva". QA da amostra: Whisper 100%, botão visível (vermelho 18,6%, papel 35,2%; quadros sem botão: 0%), −15,3 LUFS.

## Custo
Voz da amostra: 1 geração Fish, 119 bytes = **US$ 0,0018** (`financas.consumo`, nota `dossie-cta-inscricao.json`, sem `ref_id`). Imagens novas: zero. Nos vídeos, a frase sai na voz do vídeo (~US$ 0,002 a mais por vídeo).
