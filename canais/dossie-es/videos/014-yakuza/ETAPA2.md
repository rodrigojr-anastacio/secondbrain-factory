# ETAPA 2 · dossie-es 014 La Yakuza (21/11/2026)
Voz Fish (65 blocos, US$ 0,17), 201 imagens (198 + 3 bases de thumb; ~US$ 8,3 com 19 refeitas pós pré-QA), build 13:25 (260 planos, 19,4 cortes/min), pré-QA (95 quadros, 4 bloqueantes → 0), render Runpod (RTX 3090/4090, ~US$ 0,5 somando 1 tentativa perdida no limite de 10 min + testes), QA, thumbs A/B/C, pacote, `entrega/` (sem Drive). `youtube.videos` id 57 = `pronto`.
- **Promessa paga:** 0:14,8–0:23,2 (oficinas/emblema/cartões com nome; "no era delito") e frase-âncora 0:25,0–0:37,1.
- Imagens: 59 com moldura/faixa recortadas; I027, I035, I129 com 422 do fal (prompt reescrito, só no `cenas.json`); I027, I049, I065, I074, I079, I089, I108, I113, I131, I133, I144, I162, I166, I187 refeitas após o pré-QA (I074 e I133 gerados de novo: o recorte estragou). Originais em `imagens-orig/`.
- Mapa: só `japan_map:N054` (pino TOKIO) no `labels.jsx`.
- **Lição de render:** comando em primeiro plano > 10 min vira background e é morto aos 10 min (perdeu 1 render). Faça `run_in_background` com `timeout` alto e espere em laços de `sleep` no mesmo turno, ou divida em faixas; `npm ci` na pasta do vídeo é necessário (node_modules é limpo).
- Pendências: reconferir Supremo no caso Nomura antes de publicar; conferir de ouvido os nomes dos blocos < 93%.
