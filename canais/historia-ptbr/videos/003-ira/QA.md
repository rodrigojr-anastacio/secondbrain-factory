# QA v2 · 003 Irã (05/11/2026) · APROVADO

Render `out/video.mp4` = `entrega/video.mp4` (`qa/v2-qa.txt`, `out/contact-sheet.jpg`):
- 1081,5 s (18:01), 1920×1080, 30 fps, H.264 + AAC 48 kHz estéreo.
- −15,2 LUFS integrado, LRA 3,6, pico −4,2 dBFS.
- 0 telas pretas (≥ 0,2 s); 0 silêncios > 1,5 s.
- Cortes: 25 planos no 1º minuto pela timeline (o `qa.sh` conta 20 por cena); 350 planos, média de 3,09 s, 19,4 por minuto.
- 32 cartões de data, 96 rótulos, 10 placas de capítulo. Stills de mapas e capítulo em `qa/v2-stills/`.

Voz × roteiro (Whisper small por bloco, `qa/voz_blocos.json` + `qa/voz_blocos_fonetico.json`):
- 90 blocos, 0 tags faladas.
- Bruto: média 96,3%. Fonético: mínimo 96,0%, média 99,5% (≥ 95% em todos).

Imagens (`qa/v2-prancha-1..6.jpg`, `qa/v2-mapas.jpg`):
- 212 únicas + 0 faltando, 0 pretas, 0 molduras.
- Letras: I059 e I199 refeitas. Resíduos menores: I160 ("CONTRACT", palavra real) e letreiros miúdos em I194/I195.
- Bonequinhos de cabeça redonda em todas as cenas com gente.

Bíblia do canal:
- Narrativa contínua, 10 eras com títulos-frase não falados, "mas… então…".
- Loops pagos: cavalo (hook → fecho), paraíso (era 1 → era 9 → fecho), Pars (era 1 → era 3 → era 8), cilindro (era 2 → era 9), tabaco (era 7 → era 9), qanats (era 1 → era 5).
- Sem capítulo-objeto, sem legenda queimada.
- **Fora da meta:** duração de 18:01 (alvo 15–17) e hook de 1:31 (teto de ~90 s). As duas coisas estão registradas na bíblia.
