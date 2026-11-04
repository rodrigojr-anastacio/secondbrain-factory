# QA · dossie-es 001 · TODA la historia de la CIA en 12 minutos (2026-11-04)

## Render (`tools/qa.sh`)
- `out/video.mp4`: 706,35 s (**11:46**), 1920×1080, 30 fps, H.264 + AAC 48 kHz estéreo, 354 MB.
- Telas pretas ≥ 0,2 s: **0**. Silêncios > 1,5 s: **0**. Loudness: **−15,2 LUFS**, LRA 3,5, pico −4,0 dBFS.
- Cortes no 1º minuto: **23** pela `timeline.json` (o `scene > 0.3` do ffmpeg vê 14, porque não conta os reenquadramentos). Média do vídeo: 20,1 cortes/min, plano médio de 2,98 s (mín. 1,4 s, máx. 5,4 s).
- Texto na tela: 56 rótulos de nome/lugar, 14 fichas "LUGAR Y FECHA", 14 cartões de expediente e 5 mapas com pinos e setas no código. Todos em espanhol.
- Contact sheet em `out/contact-sheet.jpg`; stills de cartões, mapas e thumbs em `qa/stills/`.

## Voz × roteiro (`tools/qa_voz_blocos.py`, Whisper small, es)
- 78 blocos, média de **97,8%**, mínimo de 82,6%. Nenhuma tag falada.
- Os 12 blocos abaixo de 93% são grafias do Whisper, não palavras perdidas: "Mossadec", "Alan Dules", "Sydney", "Armaz", "Rose betle" (Roosevelt le), "sía/silla" (CIA dita como palavra, como se usa na América Latina), "MKI Ultra", "LCD" (LSD com seseo) e "una gente entera" (un agente en Teherán, a conferir de ouvido). Sem bloco a regerar.
- Pronúncias conferidas numa amostra antes do vídeo inteiro: CIA, OSS, U dos e PB Success saíram certos.

## Imagens
- 171 de 171 (168 do vídeo + 3 bases de thumb); **0 faltando, 0 duplicadas**. Reuso planejado de 29% (0% antes de 3:00).
- 4 recusadas pelo filtro do fal (HTTP 422: tanques em Teerã, U-2 atingido, helicóptero atingido, Torres Gêmeas): reescritas com versão mais branda. As Torres viraram os feixes de luz do memorial.
- 43 saíram com **moldura de papel** (o nano-banana desenha um quadro): recortadas sem custo com `tools/recorta_moldura.py` (79–94% da largura, reenquadradas em 1344×768; originais em `imagens-orig/`). `tools/checa_imagens.py` final: 0 suspeitas.
- 2 mapas refeitos: o das Américas cortava o Chile, e o do Irã tinha letras falsas ("CASPARIN SEA"). No novo mapa do Irã ainda sobrou "ACSPRIN SEA", coberto de propósito pelo rótulo "MAR CASPIO".
- Fidelidade: grade revisada imagem a imagem (`qa/grade-*.jpg`). Pendências menores: o U-2 sobre Cuba (I098) parece um bimotor; há textos em inglês dentro da cena em I066 ("DECLASSIFIED") e I075 ("ON AIR").

## Pacote
- `entrega/pacote.md`: título com N = 12 (11:46 arredondado), capítulos em ordem crescente desde 0:00 e iguais aos cartões, fontes e nota de voz sintética e IA. Nenhum texto em português na tela nem na descrição em espanhol.
- 3 thumbs de 157–171 KB (A: agente + Langley; B: rádio + "LA RADIO QUE TUMBÓ UN GOBIERNO"; C: agente + "EN AMÉRICA LATINA").

**Resultado: aprovado.** Uma rodada de correção (molduras, filtro e mapas), feita antes do render.
