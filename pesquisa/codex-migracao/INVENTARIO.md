# Inventário: onde a fábrica gera imagem e o que migrar para o Codex (14/11/2026)

Só relatório (nada foi mudado fora do historia-ptbr). Fonte dos números: `financas.consumo` (até 14/11/2026 15:30), `grep` no repo e `canal.yaml` de cada canal.

## Resumo
- **US$ 171 gastos em imagem até hoje** (~R$ 1.015); US$ 85 só nos últimos 7 dias. 99% é cena de vídeo: historia-ptbr US$ 103,7 (fal 84,3 + OpenAI 19,4) e dossie-es US$ 65,0.
- O historia-ptbr já migrou (Codex + reserva fal): economia esperada **~US$ 9–11 por vídeo** (média atual US$ 11,32/vídeo em imagens, 9 vídeos).
- O próximo candidato de peso é o **dossie-es** (US$ 8,10/vídeo, 8 vídeos), mas só depois de uma rodada de prompt fechado (o teste de 14/11 reprovou: paleta quente, contexto inventado, sangue). O resto é miúdo (< US$ 4 no total).

## Onde se gera imagem hoje
| Onde | Ferramenta | Gasto até 14/11 | Migrar para o Codex? |
|---|---|---|---|
| Cenas do **historia-ptbr** (`skills/imagens`) | `img_codex.py` desde 14/11 (antes `img_fal.py` nano-banana-2.1/edit e `img_openai.py`) | US$ 103,7 (2.818 imgs) | **Feito** (14/11). Acompanhar cota com `tools/codex_uso.sh`. |
| Thumbs do historia-ptbr (`skills/thumbnail`) | `img_codex.py` desde 14/11 | US$ 3,81 (84 bases) | **Feito** (14/11). |
| Cenas do **dossie-es** | `img_fal.py` nano-banana | US$ 65,0 (1.637 imgs) | **Depois**, com amostra de 10 cenas com prompt fechado ("only…, no people, muted slate/olive/sepia palette, no blood") aprovada pelo Rodrigo. Economia ~US$ 8/vídeo. Atenção: mesma cota Plus do historia (2 vídeos/semana do historia + 2 do dossie ≈ 800 imagens/semana; a cota semanal ainda não foi medida). |
| Thumbs do dossie-es | `img_fal.py` | US$ 3,23 (79) | Junto com as cenas (mesma decisão de estilo). |
| **Identidade** (logo/capa): `canais/historia-ptbr/identidade/tools/gerar.py`, `canais/dossie-es/identidade/tools/gerar.py`, `pesquisa/canal-clima-2026-11/identidade/tools/gerar.py` | fal (chamada direta) | US$ 1,15 | Sim, quando houver canal novo: baixo risco, texto já vai no código. Economia irrelevante (~US$ 0,50 por canal). |
| **Testes de estilo / amostras / bancadas** (`canais/*/testes/`, `v2-amostras/`, `playbooks/novo-canal.md` com teto US$ 3) | fal / OpenAI | ~US$ 3,6 (lugares-guerra-en 1,76; dossie-ptbr 0,79; lotr-fr 0,50; em-relevo 0,39; outros) | Sim, como **1ª opção para canal novo** (US$ 0), mantendo uma amostra no fal para comparação. Exige que o `novo-canal` saiba do Codex. |
| **lugares-guerra-en** (proposta, `gerador: fal`) | fal | US$ 1,76 | Decidir junto com o estilo do canal, se ele sair do papel. |
| **lotr-fr** (pintura a óleo) | OpenAI (gpt-image) | US$ 0,50 | Candidato natural (o Codex usa o mesmo gpt-image), mas canal parado: só com amostra. |
| **Em Relevo** | sem IA (mapa 3D + satélite + dados) | US$ 0,39 (identidade) | **Não** (geografia inventada; teste de 14/11). |
| **Reembalagem** (`tools/rotinas/reembalagem.py`, sáb 02:00) | não gera imagem (thumb só descrita) | US$ 0 | Se um dia passar a gerar a thumb proposta, o Codex é o caminho natural (US$ 0) para canais com `gerador: codex`. |
| Pré-QA visual, garimpo, métricas | não geram imagem (só leem) | — | — |

## Riscos para acompanhar antes de ampliar
1. **Cota única** do ChatGPT Plus para tudo (Codex de imagem + uso pessoal do Rodrigo no ChatGPT). Indicativo: ~500 imagens por janela de 5 h; semanal desconhecida (1% após ~34 execuções). Medir com 2–3 vídeos do historia antes de pôr o dossie.
2. **Bloqueio/uso automatizado**: o login é pessoal; se a OpenAI restringir, o fallback fal cobre (o `img_codex.py` cai sozinho e grava `codex_limite`/`codex_erro`).
3. **Tempo**: ~1 h por vídeo de 200 imagens contra ~25 min no fal; com 2 canais no Codex e jobs em paralelo, o gargalo vira a fila.
4. **Fidelidade de época**: o gerador inventa marcos e contexto (Torre Eiffel em 1870); manter pranchas e pré-QA.
