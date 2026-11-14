# ETAPA 2 · historia-ptbr/009 Alemanha (youtube.videos id 37) · 13/11/2026

**Resultado:** `entrega/video.mp4` **17:22** (1042 s), 1080p30, −15,2 LUFS, pico −4,3 dBFS, 0 telas pretas, 0 silêncios > 1,5 s, 21 cortes no 1º minuto. Checklist v2: obrigatórios ok; ritmo ~126 ppm (2.179 palavras), abaixo de 140–145 (mesma Hipótese conhecida do drama-3 do 008). Duração > 17:00 mas < 17:30; título A diz "17 minutos" (arredondado).

## Custo (financas.consumo, ref_id 37)
fal US$ 10,57 (215 imagens + 7 refeitas + 1 mapa + 6 bases de thumb, ~US$ 0,046 cada) · Fish drama-3 US$ 0,81 (vídeo 12.902 bytes + 3 tomadas do hook) · Runpod ~US$ 0,43 (RTX 3090/A4500; inclui 4 Pods perdidos por SSH/upload travado e 1 máquina sem SSH por 19 min) · pré-QA Anthropic US$ 0,57 (2 rodadas). **fal+Fish = US$ 11,4 (teto 14).**

## Voz
Fish drama-3, 1 chamada por bloco, 64 blocos, nenhuma troca no `FALA`. Whisper bruto mín 82,9% (N041, nomes), média 98,0%; **fonético mín 97,4%, média 99,6%**. Nomes (Guête, Chíler, Vítenberg, Rúr, Bénts, Báier) saem como o Whisper entende "Gett/Tiller", "Wittenberg", "Bentz", "Bayer": ouvir antes de publicar. Hook: 3 tomadas extras de N001–N006, melhor combinação `cbabcc` (repetição melódica 0,11). Cap. 9 (N050–N054) sem tom dramático extra; conferir o Holocausto (N053, 14:23) de ouvido.

## Imagens
Lote-prova de 6 (I006, I071, I061, I082, I190, I174): I006 (águia no capacete) e I082 (carta com letras) refeitas; depois as 209 restantes em 5 lotes. Plano de 1919–1945 (I157–I189) conferido na prancha: nenhuma suástica, águia, bandeira, braçadeira ou corpo; Hitler em nenhum plano. Refeitas pelo pré-QA (texto inventado/estilo): I070 (pergaminho), I077 (cartaz na porta), I163 (etiquetas de preço), I168 (néon), I156 (rosto parecido com ditador), I150 (galeão/romanos num porto de 1890), I127 (bandeira), I142 (países escritos no mapa de 1871). Mapas sem letras; rótulos no `src/labels.jsx`.

## Pré-QA
175 stills (a cada 10 s + mapas + cartões + capítulos), 120 analisados: rodada 1 = 1 bloqueante (pergaminho com texto, corrigido), rodada 2 = **0 bloqueantes**, 7 altos, 34 médios. Falsos positivos anotados: tricórnios na cena de 1618 (I108/cena do feno, estilo), bandeira preto-vermelho-dourado no parlamento de 1849 (correta), Reichstag/castelo em "dois caminhos" (simbólico), Q51 margem de mapa (pan do Ken Burns), supermercado de 1990 (é a analogia do Brasil), Q108 rótulos do mapa 1949 (pan; ajustados para OCIDENTAL/ORIENTAL), faixa de mapa "Império Alemão" (simplificação do mapa).

## Render
Runpod em 6 partes (0–5209, 5210–10419, 10420–15629, 15630–20839, 20840–26049, 26050–31258; provas SSIM ≥ 0,996) + concat com `mix.wav` AAC 192k. Trilha: Lá eólio, alaúde sintetizado até o cap. 6 e cravo depois (não fiz o piano esparso dos caps. 8–9 da sugestão: sem marcha, mas sem troca de timbre).
Armadilhas: (1) o `public/audio/` (390 MB de wav) no bundle trava o upload ao Pod: no bundle deixei só um `mix.wav` mudo de 2 s (a composição tem `<Audio>` e o 404 derruba o render); (2) `render_runpod.sh` espera `espera_vps` (qualquer remotion de outro job) antes dos stills: usei cópia sem a espera (`tools/render_runpod_local009.sh`), os stills já estavam em cache; (3) tempo de boot do Pod passa de 10 min às vezes: scripts em segundo plano com acompanhamento em primeiro plano.

## Trechos para conferir (timestamps da legendas.srt)
- 0:00 hook (Versalhes) e 0:28 Goethe e Schiller (pronúncia)
- 4:12 Martinho Lutero · 9:13 Bismarck
- 13:08 Hitler como nome falado ("Rítler" no FALA) · 14:08 seis milhões / 14:23 "É o Holocausto" (tom sóbrio)

## Pendências
Ouvir os nomes e o cap. 9 antes de publicar. Título A: "17 minutos" (real 17:22).
