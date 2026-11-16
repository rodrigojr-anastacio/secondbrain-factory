# Pré-QA visual automático

- Alvo: `canais/lugares-guerra-en/videos/004-pearl-harbor/preqa` · 9 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.056 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 0 · médio 5 · baixo 6
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| — | Q02 `grade_r_02.jpg` | medio | texto_cortado | P028 DocGrifo (1:50): o título do formulário ('...w to Complete National Register Fo') aparece cortado pela borda esquerda e direita no topo. Pode ser o zoom intencional do DocGrifo, mas o texto cortado fica no alto do quadro. |
| — | Q04 `grade_r_04.jpg` | medio | texto_encavalado | P080 e P081 (5:50, 5:52, 6:01): o selo '1985 NATIONAL HISTORIC LANDMARK' e o selo '81' ficam por cima do texto do documento e da foto, cobrindo parte do cabeçalho do formulário ('...ete applicable...'). Atrapalha a leitura de forma discreta. |
| — | Q08 `grade_r_08.jpg` | medio | outro | P177 KenBurns (14:10): foto de época com contraste estourado (preto e branco chapado, quase sem meios-tons), ficando distinta das outras fotos de arquivo. Pode ser efeito de transição/tratamento; na dúvida entre estilo e defeito. |
| — | Q05 `grade_r_05.jpg` | medio | texto_cortado | P110 KenBurns (8:17): o texto da vitrine ('7 DECEMBER 1941') fica cortado no topo da imagem pelo zoom, e em P109 (8:14) o título 'THE HICKAM FLAG' encosta na borda superior. Parece ser enquadramento da foto real, não texto da tela. |
| — | Q09 `grade_r_09.jpg` | medio | anacronismo | No quadro P187 a bandeira exibida ("THE HICKAM FLAG - 7 DECEMBER 1941") tem o tamanho e o enquadramento cortados nas bordas, e a foto tem reflexos de vitrine. Em dúvida entre estilo e defeito: a bandeira de 48 estrelas é coerente com 1941, então não há anacronismo claro. |

6 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Quadros

Q01=grade_r_01.jpg, Q02=grade_r_02.jpg, Q03=grade_r_03.jpg, Q04=grade_r_04.jpg, Q05=grade_r_05.jpg, Q06=grade_r_06.jpg, Q07=grade_r_07.jpg, Q08=grade_r_08.jpg, Q09=grade_r_09.jpg
