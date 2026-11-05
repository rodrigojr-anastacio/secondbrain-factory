# QA · dossie-es 002 · TODA la historia del Mossad en 14 minutos (2026-11-05)

## Render (`tools/qa.sh`)
- `out/video.mp4`: 822,7 s (**13:43**), 1920×1080, 30 fps, H.264 + AAC 48 kHz estéreo, 343 MB.
- Telas pretas ≥ 0,2 s: **0**. Silêncios > 1,5 s: **0**. Loudness: **−15,2 LUFS**, LRA 3,6, pico −3,7 dBFS.
- Cortes: 26 no 1º minuto pela `timeline.json` (o `scene > 0.3` do ffmpeg vê 18, porque não conta os reenquadramentos); média de 20,4 por minuto, plano médio de 2,94 s (mín. 1,9 s, máx. 4,5 s).
- Texto na tela: 48 rótulos, 15 fichas "LUGAR Y FECHA", 14 cartões de expediente e 4 mapas com pinos e setas no código (Oriente Médio, América do Sul, Europa, mar Vermelho), conferidos em still (`qa/mapas-final.jpg`). Tudo em espanhol.
- Contact sheet em `out/contact-sheet.jpg`.
- Hook de 40 s (a bíblia pede 25–35 s): ficou acima do alvo em 5 s.

## Voz × roteiro (`tools/qa_voz_blocos.py`, Whisper small, es)
- 85 blocos, média de **96,4%**, mínimo de 82,8%. Nenhuma tag falada.
- Os 18 blocos abaixo de 93% são grafias de nomes no Whisper, não palavras perdidas: "Vengurion" (Ben-Gurión), "Reuben Chilog" (Shiloaj), "Knesset", "Herbert Cuckooers/Cúcurz" (Cukurs), "Marge" (Marjeh), "Walswajter" (Zuaiter), "C. Samir" (Zvi Zamir), "Marguán" (Marwan), "May Ramit" (Meir Amit), "Had-Serim" (Hatzerim), "Kippur", "aterrisa" (seseo), "se ha pedido a Ekman" (se apellida Eichmann). Nenhum bloco a regerar.
- A conferir de ouvido (10 s): N012 ("El muchacho se apellida Eichmann", ~1:45) e N028 (1ª menção de "Herberts Cukurs", ~4:32), que o Whisper ouviu como "Cuckooers".

## Imagens
- 198 de 198 (195 do vídeo + 3 bases de thumb); **0 faltando, 0 duplicadas**. Reuso de 30% (0% antes de 3:00).
- **0 recusas** do filtro do fal (os prompts de violência foram escritos "de longe e sem corpo" desde o início).
- **51 com moldura** (27%): 30 de papel claro e 21 com **faixa preta** (letterbox, novidade deste lote), recortadas sem custo (`tools/recorta_moldura.py`; originais em `imagens-orig/`). O detector (`tools/checa_imagens.py`) passou a pegar a faixa preta também. Falsos positivos deixados como estão: I015 (céu claro) e thumb-A.
- 3 refeitas: I155 (saiu em medalhão redondo), I143 (moldura vertical que o recorte não salvava) e thumb-C (bandeira alemã inventada na cauda do MiG).
- Pendências menores: a porta da casa de Shangrilá (I095) parece medieval demais; em I016 o nano-banana escreveu "Egypt", coberto de propósito pelo rótulo EGIPTO.

## Pacote
- `entrega/pacote.md`: título com N = 14 (13:43 arredondado), capítulos em ordem crescente desde 0:00 e iguais aos cartões, fontes, nota de voz sintética e IA, tradução pt-BR.
- 3 thumbs de 81–140 KB (A: agente + MiG; B: o homem da calle Garibaldi + "LO ENCONTRÓ UN CIEGO"; C: o MiG + "EL MIG ROBADO").

**Resultado: aprovado.** Uma rodada de correção (molduras e 3 imagens refeitas, rótulos dos mapas reposicionados), antes do render.
