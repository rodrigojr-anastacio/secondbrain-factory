# QA · dossie-es 005 · TODA la historia de la KGB en 14 minutos (09/11/2026)

**Aprovado.** `tools/qa.sh` + `tools/qa_voz_blocos.py` + revisão visual (4 folhas de contato das 200 imagens, mapa renderizado, contact sheet do vídeo, 3 thumbs).

| Item | Resultado |
|---|---|
| Arquivo | `out/video.mp4` 1920×1080, 30 fps, H.264 + AAC 48 kHz estéreo, 845,3 s (14:05), 351 MB |
| Áudio | −15,3 LUFS, LRA 3,5, pico −3,7 dBFS; 0 silêncios > 1,5 s |
| Telas pretas | 0 |
| Ritmo | 287 planos, média de 2,95 s, 20,4 cortes/min (build); o detector de cena conta 17 no 1º minuto (planos escuros) |
| Hook | 30,1 s (alvo ≤ 35 s) |
| Voz (Whisper small, por bloco) | 87 blocos, média **97,2%**, mín. 79,2%. Os 16 abaixo de 93% são grafia de nome na transcrição (Cheká→"Checa", Lubianka→"Lubianca", Yezhov→"Jezov/Yeshiov", Lavrenti Beria, Trotski→"Trotsky", Feklisov, Scali, Sájarov, Zhivkov→"Sivkov", Gordievski, Kriuchkov, Dzerzhinski, Mitrojin), "OGPU" como "O GPU" e "00447" que o Whisper ouve como número. Nenhuma tag falada |
| Imagens | 200 (197 + 3 thumbs), **0 recusas** do filtro; 50 suspeitas de moldura/faixa (25%): 46 recortadas, 4 falsos positivos (cenas escuras) restaurados; 5 refeitas: I061 e I147 (moldura enorme, recorte < 60%), I100 (pasta com "PROJECT NIGHTHAWK"), I162 (avião com "BRITISH AIRWAYS"), I151 (luz "ON AIR") |
| Mapa | `map_world` (Moscú → Santiago, La Habana, Ciudad de México), pinos no código; posições conferidas no frame do render (2 ajustes: a grade da imagem não bate com o enquadramento do Ken Burns) |
| Thumbs | A/B/C 1280×720, 178–191 KB; aba "EXPEDIENTE Nº 005", sello "1917–1991" |

## Para ouvir (Rodrigo; timestamps conferidos na `legendas.srt`)
0:15 "Georgi Markov" · 0:51 "Félix Dzerzhinski" · 2:17 "Nikolái Yezhov" · 3:22 "David Alfaro Siqueiros" · 3:48 "Ramón Mercader" · 6:43 "Alexandr Feklisov" · 7:47 "Oleg Nechiporenko" · 9:41 "Zhivkov" · 10:33 "Oleg Gordievski" · 11:34 "Vladímir Kriuchkov" · 12:23 "Vasili Mitrojin".

## Observações (ficaram)
- I150 (Markov no estúdio da BBC, expediente 11) tem uma placa "ON AIR" pequena; I030 (decreto do Terror Vermelho) tem pseudocirílico ilegível. Plausível de época; não refeito.
- O mapa é um planisfério de papel antigo com borda rasgada (estilo, não moldura).
- La Habana ficou ~1 cm a oeste da ponta de Cuba no frame; legível e plausível.
