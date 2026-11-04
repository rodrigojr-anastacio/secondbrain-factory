# Etapa 3: v2 (os 3 ajustes do Rodrigo)

**Título final:** A HISTÓRIA COMPLETA do Egito em 17 minutos · `youtube.videos` id 3 → `status='pronto'`, `duracao_s=1020`

A v1 está preservada em `out-v1/`, `audio-v1/`, `imagens-v1/` e `qa-v1/` (com a voz, a timeline e o QA da v1).

## O que mudou
1. **Imagens em `medium`:** as 204 imagens do vídeo foram geradas de novo em `medium`, sem nenhuma `low`, com 0 falhas. Os prompts de 1922 (`independence_1922`, I180) e de 1952 (`nasser_crowd`, I182) agora pedem a bandeira verde com crescente e 3 estrelas, e as duas saíram corretas.
2. **Narração com respiro:**
   - **Roteiro:** 73 blocos editados no `roteiro.py`. Há 50 `[break]` nas viradas de ideia (eram 15) e 59 tags de tom no início das frases-chave (`[curious]`, `[serious]`, `[amazed]`, `[warm]`, `[slightly dramatic]`), no máximo 1 por frase. O texto falado não mudou.
   - **Marcação de ideia nova:** o conjunto `IDEIA` no `roteiro.py` vira `"ideia": true` no `blocos.json` e marca 51 blocos.
   - **Voz:** gerada de novo no Fish (s2.1-pro). As tags não são lidas em voz alta (conferido no Whisper).
   - **`tools/build.py`:** encadeia os blocos com 0,35 s entre blocos do mesmo assunto, 0,9 s antes de ideia nova e 1,5 s antes de capítulo. O corte do fim de cada frase ficou menos agressivo (cauda de 0,15 s, limiar -45 dB). O regex de tags agora pega qualquer `[tag]`. Os links de `public/img` são refeitos quando apontam para outra versão.
   - **Resultado:** a pausa média real entre blocos foi de 0,33 s para 0,90 s (1,10 s nas viradas de ideia e 1,70 s antes de capítulo).
3. **Thumbnail:** a `thumb-base` foi gerada de novo em `high`, com a mesma composição (ilustração à esquerda, céu e areia livres à direita). O "EGITO" e o "5000 a.C. – 2026" foram compostos de novo pelo `src/Thumbnail.jsx`.
4. **Build → render → QA** rodaram de novo, sem legenda na tela. O `QA.md` agora traz a comparação v1 × v2, e `tools/compara_v1v2.py` é novo. O `out/youtube.txt` está com o título e os capítulos novos.

**Nova duração:** 1020,3 s (**17:00**), contra 15:54 da v1.

## Custo da v2 (financas.consumo, ref_id = 3, ids 10–12)
| Fornecedor | Item | US$ | R$ |
|---|---|---|---|
| OpenAI | 204 imagens medium | 8,55 | 49,84 |
| OpenAI | thumb-base high | 0,17 | 0,97 |
| Fish Audio | narração (14.266 bytes) | 0,21 | 1,25 |
| **Total v2** | | **8,93** | **52,06** |

O script estimou US$ 11,53 para a OpenAI. Os valores acima já vêm calibrados pelo saldo real da conta (fator 0,756, ajuste feito no banco às 21:40), então a v2 ficou dentro do teto de US$ 15. Com a v1, o vídeo soma R$ 59,65 de custo direto (R$ 80,38 com o rateio do fixo, em `custo_por_video`).

Para refazer: `python3 roteiro.py` → `…/tools/.venv/bin/python …/tools/img_openai.py historia-ptbr cenas.json imagens --video 3 --qualidade medium` → `…/tools/tts_fish.py historia-ptbr blocos.json audio --video 3` → `…/tools/.venv/bin/python tools/build.py` → `tools/render.sh` → `tools/qa.sh` → `tools/compara_v1v2.py`.

## Pendências
- **Publicação (Rodrigo):** suba `out/video.mp4` (nunca a versão do Telegram) e `out/thumbnail.jpg`, com o texto de `out/youtube.txt`. Marque idioma pt-BR, "conteúdo alterado ou sintético = sim" e "não é para crianças".
- **Saldo da OpenAI no banco está desatualizado:** a view `financas.saldo_pre_pago` mostra US$ 0,05, porque só há US$ 10 de recarga lançada, mas a nota da calibração indica um saldo real de ~US$ 8,71 na conta. Falta lançar a(s) recarga(s) que faltam em `financas.lancamentos` (decisão/dado do Rodrigo). Com ~US$ 8,7 de saldo real, cabe cerca de 1 vídeo novo em `medium`.
- **`youtube.videos.publicado_em`** do id 3 está em 2026-11-03, com `status='pronto'`. Se for a data planejada, ok; se não, limpe o campo. Não mexi nele.
- **Ritmo do hook:** o 1º minuto ficou com 21 planos (eram 23) por causa das pausas novas. Se quiser mais cortes, são +2 imagens no `EXTRA` do hook (~US$ 0,08).
