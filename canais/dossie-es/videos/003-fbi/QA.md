# QA · dossie-es 003 · TODA la historia del FBI en 13 minutos (05/11/2026)

**Aprovado.** `tools/qa.sh` + `tools/qa_voz_blocos.py` + revisão visual (4 folhas de contato de 183 imagens, thumbs e 2 mapas renderizados).

| Item | Resultado |
|---|---|
| Arquivo | `out/video.mp4` 1920×1080, 30 fps, H.264 + AAC 48 kHz estéreo, 796,6 s (13:17), 333 MB |
| Áudio | −15,2 LUFS, LRA 3,4, pico −3,7 dBFS; 0 silêncios > 1,5 s |
| Telas pretas | 0 |
| Ritmo | 259 planos, média de 3,08 s, 19,5 cortes/min (storyboard); o detector de cena (> 0,3) conta 13 no 1º minuto porque os planos escuros do hook são parecidos |
| Hook | 31,0 s (alvo ≤ 35 s) |
| Voz (Whisper small, por bloco) | 80 blocos, média **97,6%**, mín. 83,3%. Os 8 abaixo de 93% são só grafia de nome na transcrição: Pensilvania/Muhammad (N001), Hoover→"Huber" (N015, N058), Sebold (N026), "del Eje"→"de leje" (N033), COINTELPRO→"cointel pro" (N042), "a sí" (N054), Hanssen (N072). Nenhuma tag falada |
| Imagens | 186 geradas; 48 com moldura/faixa preta (26%) recortadas; 4 com margem branca lateral recortadas com `tools/recorta_branco.py` (novo); 8 refeitas (letreiro "ROXY PALACE" inventado no Biograph, texto espelhado numa porta, braçadeira vermelha num uniforme, estilo/recorte quebrado em 4) |
| Mapas | `map_latam` (México, Rio, Buenos Aires, Santiago) e `map_mexico` (Guadalajara → Washington, Michoacán): pinos no código, conferidos com grade e no frame renderizado; o México e Santiago foram corrigidos depois do 1º still |
| Thumbs | A/B/C 1280×720, 138–185 KB, legíveis; aba "EXPEDIENTE Nº 003", sello "1908–2001" |

## Para ouvir (Rodrigo)
- 0:08–0:10 "Muhammad Ali" (Whisper: "Mujamed") e 0:23–0:25 "del FBI" (conferir se a sigla sai "efe-be-i").
- 3:57 "Sebold", 4:17 "Fritz Duquesne", 5:45 "Apalachin", 6:35 "COINTELPRO", 11:35 "Hanssen", 12:05 "Ramón García".

## Observações
- Uma imagem a ~11:55 (agentes do FBI no parque, prisão de Hanssen) saiu com faixas vermelhas nas mangas; sem símbolo, ficou.
- I103 (policial de Apalachin) tem uma placa "HOTEL GRAND" ao fundo, pequena; ficou.
