# ETAPA 2 PRONTA: Em Relevo 003, A Grande Seca de 1877 (13/11/2026)

`youtube.videos` id 34 → `pronto`. **Duração 10:45 (644,9 s)**, 1920×1080 30 fps, AAC −14,0 LUFS (pico −1,4 dBFS, LRA 2,1), **0 telas pretas**, 0 silêncios > 1,5 s, 3 cortes no 1º minuto (câmera contínua + transições).
Entrega em `entrega/`: `video.mp4`, `legendas.srt`, `thumb-A/B/C.jpg` (1280×720, < 100 KB), `pacote/youtube.txt` (3 títulos pareados, descrição com capítulos, fontes, créditos de foto/música). **Não subi nada ao Drive nem ao YouTube.**

## O que foi feito
- **Gancho do próximo vídeo removido** (regra 13/11): b47 agora "manda para a família no sertão / se inscreve no canal, para entender o clima do Brasil"; storyboard sem card de próximo.
- **Voz** ElevenLabs (mesma do 002, hook 1,36×, resto 1,1×): 47 blocos, Whisper × roteiro 0,969 (bloco a bloco) e 0,973 no vídeo final; nenhuma tag falada; divergências são grafia do Whisper (Camocim, Quixadá, Dnócs). Plano: 12.664 → 15.827 caracteres usados (sobram ~22,8 mil para o 004).
- **Visual** (`remotion/src/LongoV3.jsx` + `Novos.jsx`, `shared/build_cues.py`): mapa 3D com relevo real (A satélite / B editorial), rios de retirantes (setas com fluxo, ilustrativo), régua de chuva 1849–2018 com 1877/1878, anel de meses, estimativas 150–500 mil, relevo de calor do Pacífico dez/1877 e out/2026, montanhas Niño 3.4, globo 1877/2026, ferrovias, Açude do Cedro enchendo, rota até o Acre (Acre muda de cor em 1903), campos de 1932, semiárido, Monitor de Secas, linha do tempo de secas, 6 telas de papel de arquivo. 20 fotos reais com licença; **sem linha de crédito na tela** (créditos só na descrição).
- **Pré-QA:** 120 stills + `preqa_visual.py` (US$ 0,34): 18 "bloqueantes", quase todos falsos positivos (picos das transições whip/nuvem e o fundo navy atrás de globo/régua, igual ao longo-02). Defeitos reais corrigidos: fotos cobertas pelo papel, cunha preta na foto da transposição, globo apontando para a África no lugar da China/Pacífico, números de mortos antes da menção, texto cortado em "7 campos", rótulos no gráfico de chuva.
- **Render Runpod:** 1ª tentativa (A4500) reprovou o quadro 15 (textura satélite em faixas, SSIM 0,57, estável); 2ª (3090) ficou 22 min sem SSH e foi derrubada; 3ª (A4000) ok: 11 blocos, SSIM mín. 0,985, 19.347 quadros. Pods destruídos (conta com 0). Custo Runpod ≈ US$ 0,14.

## Custos
Voz: plano ElevenLabs (3.163 caracteres no contador do plano; o roteiro tem ~10 mil, a contagem da API é menor com v3). Runpod ≈ US$ 0,14; pré-QA US$ 0,34. **Total em dinheiro ≈ US$ 0,5 (teto US$ 3).**

## Para conferir (timestamps da `legendas.srt`)
- 0:27: "Dia dos Mil Mortos" (b16, papel sépia com 1.004).
- 5:30: Sinimbu, "Divina Providência" (b26, citação + carimbo).
- 6:35: "última joia da Coroa" com carimbo SEM DOCUMENTO (b31).
- 7:16: Acre vira Brasil em 1903 (b33).

## Pendências / avisos
- Fotos de retirantes (J. A. Corrêa) só em 221–400 px: entram como cartes pequenas, sem zoom; se o Rodrigo baixar à mão as originais em alta (Brasiliana), trocar.
- b41 (96% do NE em seca): número da imprensa citando o Monitor de Secas; não conferi na geometria (a tela mostra o Monitor de set/2026 sem recalcular a %).
- Monitor de Secas de outubro sai ~20/11; se o vídeo for publicado depois, vale atualizar.
- Rotas dos retirantes, trilhos e rota marítima são traçados aproximados (dito na descrição).
- Faixa horizontal de fundo atrás de globo/régua/diorama: estilo herdado do longo-02 (aprovado lá).
