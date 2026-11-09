# QA · dossie-es 006 · TODA la historia de los Masones en 14 minutos (09/11/2026)

**Aprovado.** `tools/qa.sh` + `tools/qa_voz_blocos.py` + revisão visual (4 folhas de contato das 198 imagens, still do mapa, contact sheet do vídeo, 3 thumbs).

| Item | Resultado |
|---|---|
| Arquivo | `out/video.mp4` 1920×1080, 30 fps, H.264 + AAC 48 kHz estéreo, 850,3 s (14:10), 377 MB |
| Áudio | −15,2 LUFS, LRA 3,8, pico −3,5 dBFS; 0 silêncios > 1,5 s |
| Telas pretas | 0 |
| Ritmo | 284 planos, média de 2,99 s, 20 cortes/min (build); o detector de cena conta 18 no 1º minuto |
| Hook | 31,2 s (alvo ≤ 35 s) |
| Voz (Whisper small, por bloco) | 88 blocos, média **97,2%**, mín. 81,8%. Os 14 abaixo de 93% são grafia de nome (Mainwaring, Ashmolean, Sayer, In eminenti, Wirt, Sáenz, Vaughan, Jakim Boor/Jakín, Massera), "logias" ouvido como "lojas" e "la masonería" como "l'amazonería" (junção), e "primero de marzo" normalizado pelo Whisper como "1 de marzo". Nenhuma tag falada |
| Imagens | 198 + 3 thumbs, **0 recusas** do filtro; 58 suspeitas de moldura/faixa (29%): 49 recortadas, 7 falsos positivos (cenas escuras ou vinheta intencional); 5 refeitas + 1 falha repetida reescrita: I010 e I096 (recorte ≤ 56%), I191 (colagem em fundo bege, recorte 64%), I061 (calendário com dias em inglês), I167 (envelope "TOP SECRET"), I152 (falha 2×) |
| Mapa | `map_lautaro` (Londres → Buenos Aires, Cádiz, Santiago), pinos no código, conferidos num still do render (1 ajuste em Londres) |
| Thumbs | A/B/C 1280×720, 152–213 KB; aba "EXPEDIENTE Nº 006", sello "1717–HOY" |

## Para ouvir (Rodrigo; timestamps conferidos na `legendas.srt`)
0:10 "Canandaigua" · 1:05 "William Schaw" · 1:35 "Henry Mainwaring" · 1:50 "Ashmolean" · 2:32 "Anthony Sayer" · 3:14 "In eminenti" · 4:43 "Augustin Barruel" · 5:02 "Adam Weishaupt" · 8:03 "Manuela Sáenz" · 8:25 "yorkinos / Joel Poinsett" · 9:21 "Diana Vaughan" · 10:17 "Jakim Boor" · 10:45 "Castiglion Fibocchi / Licio Gelli" · 12:00 "Blackfriars" · 12:32 "Pippo Calò".

## Observações (ficaram)
- I105 (mapa) é um planisfério inteiro, não só o Atlântico; os pinos ficam legíveis.
- I139 (sombra do "farsante") tem cartazes com rostos e letras ilegíveis; plausível.
- I066 ("Gran Arquitecto") é um círculo sobre fundo preto (vinheta intencional, não moldura).
