# QA · dossie-es/015 El GRU · 23/11/2026
- Render Runpod (RTX 3090 Community, 2ª tentativa: os 2 Pods 4090 Community não subiram IP em 15 min), 24.837 quadros, SSIM 480p mín. 0,9896, 0 blocos refeitos. 1920x1080 30 fps H.264+AAC, **13:48 (827,9 s)**.
- Loudness −15,2 LUFS, pico −3,4 dBFS; 0 telas pretas; 0 silêncios > 1,5 s; 21 planos no 1º minuto (detector de cena do ffmpeg conta 15).
- Voz: Whisper média 96,0%, mín. 82,3% (N026); os 17 blocos < 93% são grafia de nomes/siglas (Todt, De Graaf, Penkovski, KGB, GRU "ge erre u"); nenhuma tag falada. Conferir de ouvido "Vincente" (Whisper ouviu "Vicente") e "huye" (N016).
- Pré-QA visual: 1ª rodada 3 bloqueantes (I009 e I046 com faixa, I140 texto inventado) → refeitos (I001, I009, I046, I120 togas, I140, I144, I146 logo Apple, I151, I131, I145) → 2ª rodada 0 bloqueante, 9 altos (letreiros pequenos inventados em fachadas e mapas estimados; aceitos).
- 6b `SIMILARIDADE.md` 2/100 (< 30) ✔ · 6c `CRIVO-ANGULO.md` r2 APROVADO ✔.
- **Promessa paga (legendas.srt):** uruguaio Vincente Sierra 0:03; frase-âncora "Esta es TODA la historia del GRU" 0:28 e "Putin lo esperaría en la pista" 0:41; "20 años de gulag" 3:48 (≤ 4:30 ✔); Kolóbova 8:11 (≤ 9:30 ✔); "nunca tuvo hijos" 8:59; Vnukovo/Putin recebe na pista 11:00–11:41 (42 s, ≥ 40 ✔; começa ≤ 11:15 ✔); registro tardio 12:23.
- Thumbs: A matrioska + GRU + GULAG (objeto-simbolo), B Putin aperta a mão + ¿BRASILEÑO? (cena-acao), C passaportes + MRZ no código + NUNCA NACIERON (documento-evidencia): 3 composições distintas; A/B/C = T1/T2/T3.
- Custo (financas.consumo, vídeo 62): fal US$ 8,20 · Fish 0,17 · Runpod 0,26 · Anthropic API (pré-QA) 0,61 = ~US$ 9,2 (teto 12). Pendência: a 1ª tentativa de render perdeu ~US$ 0,19 em 2 Pods sem IP.
- Pendências: ouvido em nomes; pins dos mapas estimados (conferir Nápoles, Paris, Cidade do México); ETAPA1 pedia "La Pista" no exp. 12, ficou no 11.

## Título e capítulos (out/ fica fora do git)
T1 (A): El Empresario Uruguayo que Espiaba para Moscú | Expedientes Secretos del GRU · B: GRU: la fábrica rusa de latinoamericanos · C: Cómo el GRU convirtió a sus espías en uruguayos, peruanos y brasileños.
Capítulos: 0:00, 0:47, 1:39, 2:38, 3:34, 4:13, 5:16, 6:19, 7:13, 8:23, 9:11, 10:20, 11:42, 12:53 (ver `tools/pacote.py`).
Lição: Pod Community 4090 sem IP 2× → usar `GPUS` sem 4090 e `REFS=` para não refazer stills.
