# QA: Em Relevo, vídeo 2 (Super El Niño 2026) — 10/11/2026

| Item | Medido | OK? |
|---|---|---|
| Duração | **12:10** (729,9 s) | ✅ |
| Formato | 1920×1080, 30 fps, H.264 + AAC 48 kHz | ✅ |
| Loudness | **−14,0 LUFS**, pico −1,4 dBFS, LRA 2,2 | ✅ |
| Telas pretas ≥ 0,2 s | **0** | ✅ |
| Silêncios > 1,5 s | **0** | ✅ |
| Whisper (small) × roteiro, vídeo final | **96,8%** ponderado. Piores (b32 87%, b06/b15/b36/b41/b45 92%) são grafia do Whisper ("El Ninho", "Mussum", "Lagiado", "Itajaia Sul", "Inmete", "SEP"), não erro de fala | ✅ |
| Voz | ElevenLabs v3 "Fernanda"; 8 retakes (b03, b41, b45, b46, b37×2, b42×2); "faz portas" (b46) e "recebemos" (b45) corrigidos; tags faladas: 0 | ✅ |
| Ritmo | hook 174 pal/min, resto 174 (pendência do vídeo 1 resolvida: hook não fica mais lento) | ✅ |
| Perguntas com entonação | 15 de 17 com "?" no Whisper; b37 e b42 ("E depois?") o Whisper não marca em 3 takes — ouvir | ⚠️ |
| Créditos | toda foto/imagem de terceiros com legenda + crédito na tela (polaroid/cortiça) e na descrição (`PUBLICAR.md`, `FONTES-E-LICENCAS.md`) | ✅ |
| Material real na tela | 41% do tempo (fotos, satélite e relevo com dado real OISST) | ✅ |
| Legenda `.srt` | `out/legendas.srt`, cartões das palavras do Whisper | ✅ |
| Capítulos | 12, desde 0:00, crescentes (`PUBLICAR.md`) | ✅ |
| Custo | US$ 0 (`financas.consumo` 182: 5.255 créditos da assinatura) | ✅ |

## Conferência visual
4 baterias de stills (`work/grade1..5.jpg`) + contact sheet `out/contact-sheet.jpg`. Corrigidos na 1ª rodada: relevo do Peru alto demais; listras no mar do Pacífico (z-fighting); diorama baixo; setas de Walker atrás do diorama; termômetro e mostrador por cima da caixa de perguntas; data do relevo vazando para a régua; Sul fora do quadro no mapa de previsão; focos em grade regular; caixa compacta poluindo a tela (agora some em 5 s).

## Pendências
1. Ouvir b37 (9:22) e b42 (10:37) para a entonação de pergunta.
2. Régua de montanhas: no 1º segundo as montanhas aparecem baixas com "0,00" antes de crescer (2:58–3:00); é a animação, mas dá para esconder o número abaixo de 0,1 se incomodar.
3. Atualização de 12/11 (`ATUALIZAR-12-11.md`).
