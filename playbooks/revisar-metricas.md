# Playbook — revisar métricas de um canal ou vídeo

1. `tools/.venv/bin/python tools/report.py <canal>`: resumo e últimos 10 vídeos.
2. `tools/.venv/bin/python tools/report.py <canal> --retencao <ID>`: curva de retenção. O Analytics atrasa 1–3 dias.
3. O CTR da thumbnail não existe na API. Se for essencial, peça o número do YouTube Studio ao Rodrigo.
4. Compare com os outros vídeos do canal: % assistido, duração média, inscritos por mil views.
5. Conclua com **o que manter e o que mudar no próximo vídeo**, e registre o aprendizado na **bíblia do canal** (`canais/<slug>/biblia/`: CTR em `thumb.md`, título em `titulo.md`, retenção do hook e por capítulo em `roteiro.md`), com data e fonte, confirmando ou derrubando as Hipóteses de lá. Só vai para `conhecimento/` o que valer para qualquer canal.
