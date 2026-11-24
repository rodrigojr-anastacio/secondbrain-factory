# BLOQUEIO: saldo da OpenAI zerado (03/11/2026, ~19:45)

A API de imagens respondeu **"You have no credits remaining"** (billing) no fim da geração. As imagens pararam ali, e nenhuma chamada nova foi feita depois.

## Situação
- 196 de 198 imagens foram geradas (195 do vídeo + `thumb-base` em high). Faltaram 2:
  - `charkha` (Gandhi fiando na roca, bloco N095)
  - `journey_lineup` (desfile de personagens da história indiana, bloco N128, o agradecimento final)
- **O vídeo não ficou travado:** troquei as 2 por reuso de imagens que já existiam (N095 usa `congress_flag`; N128 usa `time_tunnel` e `taj`), e o render seguiu. Nenhuma das duas cenas nomeia personagem novo, então a fidelidade não muda.
- Gasto estimado pelo script: US$ 9,43 em 223 gerações (financas.consumo ids 16 e 17). **27 gerações saíram em dobro**: rodei 2 processos em paralelo, cada um numa ponta da lista, e eles se cruzaram no meio. Isso custou ~US$ 1,1 a mais. Pelo fator de calibração do Egito (0,756), o gasto real fica em ~US$ 7,1, dentro do teto de US$ 12.
- `financas.saldo_pre_pago` mostra a OpenAI em **−US$ 9,87**, porque só há US$ 10 de recarga lançados. O saldo real na conta é **zero**.

## O que depende do Rodrigo / manager
1. **Recarregar a OpenAI** e lançar a recarga em `financas.lancamentos`, junto com as recargas anteriores que faltam (veja a ETAPA3 do Egito).
2. **Opcional, depois da recarga (~US$ 0,15 + re-render de ~40 min):** gerar de volta as 2 cenas e regerar a `dentist_ancient` (I035), cujo curandeiro pré-histórico saiu com um cocar de penas, um estereótipo errado. Para isso, devolva os prompts no `roteiro.py` (cuidado: inserir imagem nova renumera os I### seguintes; renomeie os arquivos pela chave, como foi feito na etapa final) ou gere com ids avulsos e troque na timeline.
