# QA · dossie-es 004 · TODA la historia de la Cosa Nostra en 15 minutos (05/11/2026)

**Aprovado.** `tools/qa.sh` + `tools/qa_voz_blocos.py` + revisão visual (5 folhas de contato das 204 imagens, 2 mapas renderizados, contact sheet do vídeo, 3 thumbs).

| Item | Resultado |
|---|---|
| Arquivo | `out/video.mp4` 1920×1080, 30 fps, H.264 + AAC 48 kHz estéreo, 872,3 s (14:32), 384 MB |
| Áudio | −15,3 LUFS, LRA 3,8, pico −3,6 dBFS; 0 silêncios > 1,5 s |
| Telas pretas | 0 |
| Ritmo | 279 planos, média de 3,13 s, 19,2 cortes/min (storyboard); o detector de cena conta 16 no 1º minuto (planos escuros do hook) |
| Hook | 31,7 s (alvo ≤ 35 s) |
| Voz (Whisper small, por bloco) | 83 blocos, média **96,5%**, mín. 82,9%. Os 16 abaixo de 93% são grafia de nome italiano na transcrição (Buscetta→"Busetta", Masseria, Castellammare, Vizzini, Grand Hotel et des Palmes, Inzerillo, Badalamenti, Ucciardone, Riina→"Rina", Morvillo, Schifani, Borsellino, Messina Denaro) e "prestanombres"/"autobomba" juntos. Nenhuma tag falada |
| Imagens | 204 + 3 thumbs, **0 recusas** do filtro; 44 com moldura/faixa (21%) recortadas; 4 refeitas: I018 (mapa da Sicília com uma 2ª Sicília inventada), I164 (letreiro "LUIGI'S PIZZA"), I132 (manchete com letras falsas), I200 (recorte cortou a cabeça do Riina) |
| Mapas | `map_sicily` (Palermo, Corleone, Gangi) e `map_atlantic` (Nueva York, La Habana, Nápoles → La Habana), pinos no código, posições medidas com grade e conferidas no still |
| Thumbs | A/B/C 1280×720, 166–187 KB; aba "EXPEDIENTE Nº 004", sello "1860–1993"; nenhuma arma |

## Para ouvir (Rodrigo; timestamps conferidos na `legendas.srt`)
0:19 "Tommaso Buscetta" (sai "Buseta", à espanhola) · 3:52 "Masseria" / 3:55 "Castellammare" · 7:08 "Grand Hotel et des Palmes" · 9:13 "Inzerillo" · 11:13 "Badalamenti" · 11:45 "Ucciardone" · 12:59 "Schifani" · 14:11 "Messina Denaro".

## Observações (ficaram)
- O avental do padeiro (expediente 2) tem "GIUSEPPE'S BAKERY" pequeno; o jornal do Petrosino tem "The New York Gazette". Inglês plausível de época, sem erro.
- O mapa da Sicília tem manchas vermelhas pequenas no relevo (parecem marcas); os pinos do código se distinguem.
