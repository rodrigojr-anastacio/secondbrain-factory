# Pôsteres próprios da #1 (ajuste do Rodrigo, 24/11/2026)

Fora de `cenas-*.json`/`visual/` porque o `montar.py` apaga e regera aqueles. Gerados uma vez cada (1ª tentativa aprovada):

```
# A = mural do espião (gpt-image-2/edit com refs de estilo + folha do Juan), US$ 0,14
tools/.venv/bin/python canais/dossie-es/produtos/hq/src/gerar_fal.py --modelo openai/gpt-image-2/edit --orient retrato dossie-es \
  canais/dossie-es/produtos/hq/001/posteres/cenas-poster-a.json canais/dossie-es/produtos/hq/arte-001/posteres \
  --visual canais/dossie-es/produtos/hq/001/posteres/visual-poster-a.yaml --tamanho 2336x3296 --notas "dossie-hq-001 poster-a"
# C = cartaz vintage (gpt-image-2 texto→imagem, sem refs: estilo próprio de cartaz), US$ 0,12
tools/.venv/bin/python canais/dossie-es/produtos/hq/src/gerar_fal.py --modelo openai/gpt-image-2 --orient retrato dossie-es \
  canais/dossie-es/produtos/hq/001/posteres/cenas-poster-c.json canais/dossie-es/produtos/hq/arte-001/posteres \
  --visual canais/dossie-es/produtos/hq/001/posteres/visual-poster-c.yaml --tamanho 2336x3296 --notas "dossie-hq-001 poster-c"
```
A3 300 dpi (com e sem título): `001/tools/extras_pacote.py --so posteres`.
