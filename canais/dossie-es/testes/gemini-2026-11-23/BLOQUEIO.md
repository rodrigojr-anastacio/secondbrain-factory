# BLOQUEIO (23/11/2026): chave Gemini de teste sem faturamento

A chave em `~/.segredos/gemini-teste.env` é de um projeto **Free Tier**: todos os modelos de imagem respondem 429 com `free_tier_requests limit: 0`, e o Batch responde 400 `FAILED_PRECONDITION`. A Gemini API não tem free tier para imagem.

**Ação do Rodrigo:** ativar o faturamento do projeto da chave no AI Studio ("Set up billing") ou criar o projeto próprio do Dossier já com faturamento. Depois, rodar de novo o brief `referencias/BRIEF-teste-gemini-api-dossie.md` (protótipo e comandos prontos em `TESTE.md`). Custo até aqui: US$ 0.
