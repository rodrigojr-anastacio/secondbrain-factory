# Cakto: Expedientes Secretos #1 (24/11/2026)

Plataforma de venda trocada de Hotmart (conta presa na troca CNPJ→CPF) para **Cakto** (decisão do Rodrigo, 24/11).
- Produto `a67561b3-0ad2-43f1-b0d0-e2088002363a`, US$ 4,99, pagamento único. Checkout: https://pay.cakto.com.br/vt3xj9m
- Entrega: Cakto Members V3, área `d0f0a873-1343-4815-85ea-ab8356edf143` (e-book PDF + aulas Pósteres e Fondos com materiais; arquivos sobem só pelo painel).
- API: chave em `~/.segredos/cakto.env` (nunca no git). Token: POST /public_api/token/.
- Checkout personalizado por `checkout_config.py` (PUT /public_api/products/{id}/checkouts/1367330/).

## Lições do checkout por API
- `layout` só aceita [12], [8,4], [4,8], [4,4,4] (7/5 quebrou tudo).
- `image.width` é em **pixels** (100 = miniatura).
- `settings` vazio faz o formulário de pagamento sumir: mandar o tema completo (copiado do exemplo da doc).
- Imagens precisam de URL pública: 3 prévias de baixa resolução em Drive `produtos/checkout-publico/` (link público, via lh3.googleusercontent.com/d/ID).
- Rollback: PUT com `"config": null` volta ao checkout padrão.
