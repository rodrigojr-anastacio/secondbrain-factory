# ETAPA 2 PRONTA: Em Relevo 004, 1983 (13/11/2026)

`youtube.videos` id 38 → `pronto`. **Duração 10:07 (606,9 s)**, 1920×1080 30 fps, AAC −14,0 LUFS (pico −1,4 dBFS, LRA 2,0), **0 telas pretas**, 0 silêncios > 1,5 s, 6 cortes no 1º minuto. Entrega local em `entrega/` (video.mp4, legendas.srt, thumb-A/B/C.jpg, pacote/youtube.txt). **Nada no Drive nem no YouTube.**

- **Voz** ElevenLabs (hook 1,36× b01–b06, resto 1,1×): 42 blocos, 3.480 caracteres do plano (sobram ~18,4 mil); Whisper × roteiro 0,963 (bloco a bloco) e 0,965 no vídeo; divergências = grafia do Whisper (NOAA→"NOA", El Niño→"Uninho", Iguaçu).
- **Visual**: LongoV3 + `Novos4.jsx` (tela partida por tintas de UF, régua 3D e 2D, hidrograma da ANA com onda RONI, antes×depois Landsat com cortina, chuva anual de Mombaça, anel de 24 meses, mostrador ~60%). Landsat de 3/7 e 4/8 reprocessados com estiramento COMUM (`tools/landsat_par.py`) e cortados para tirar a cunha preta; as listras verticais são do sensor MSS.
- **Pré-QA**: 126 stills + `preqa_visual.py` (2 rodadas, US$ ~0,64): 6 "bloqueantes" restantes = falsos positivos do estilo (faixa navy atrás de globo/Pacífico/montanhas, igual ao 003; animações no 1º quadro). Corrigidos: cilindro da régua cortado, rótulos do hidrograma e das barras de Mombaça encavalados, cartões × legenda, foto cobrindo manchete (b04), caixas das perguntas cobrindo cartões.
- **Render Runpod**: 1ª tentativa estourou meu timeout de 10 min (Pod destruído); 2ª: pod sem SSH 16 min (US$ 0,24, derrubado), 3090 ok: 10 blocos, SSIM mín. 0,983, 18.207 quadros. Custo Runpod ≈ US$ 0,28 (+ ~US$ 0,1 da 1ª). Pods meus destruídos.
- **Custo total em dinheiro ≈ US$ 1,1** (teto 3): Runpod ~0,4 + pré-QA ~0,64; voz no plano.

## Para conferir (timestamps da `legendas.srt`)
- 0:06 "No dia 18, ele chegou a 10,42 metros" (régua 3D + número).
- 2:50–2:55 Landsat antes × depois (cortina; nuvem sobre a cidade em 4/8, várzea alagada à direita).
- 3:53 "Em 83, 366. Menos da metade" (gráfico de Mombaça).
- 6:48 "Guarde isso. Vai importar em 2026." (anel de 24 meses).

## Pendências
- Licença do slide "Retirantes" (Unicamp, b20): conferir na página (FONTES-E-LICENCAS.md); se houver dúvida, tirar.
- Foto de Blumenau 2008 (b16) é de outro ano (legenda tem o ano).
- Faixa navy atrás do Pacífico/globo: estilo herdado do 002/003.
- Marcos "Retirantes/rotas" e rios do mapa são traçados aproximados (dito na descrição).
