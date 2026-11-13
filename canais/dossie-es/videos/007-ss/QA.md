# QA · dossie-es 007 · TODA la historia de las SS en 14 minutos (13/11/2026)

**Aprovado.** `tools/qa.sh` + `tools/qa_voz_blocos.py` + pré-QA visual (`PREQA-visual.md`, 99 quadros, 2 rodadas) + revisão visual minha (7 folhas de contato das 188 imagens, zoom em uniformes, stills do mapa, contact sheet do vídeo, 3 thumbs).

| Item | Resultado |
|---|---|
| Arquivo | `out/video.mp4` 1920×1080, 30 fps, H.264 + AAC 48 kHz estéreo, 868,6 s (**14:29**), 472 MB |
| Render | Runpod em 2 faixas (0–6599 RTX 3090; 6600–26058 RTX A4000), conferência densa SSIM ok, nº de quadros conferido; 1ª tentativa morta pelo timeout do meu comando (Pod destruído) e 1 Pod lento (SSH 324 s) estourou o limite: US$ 0,18 no total |
| Áudio | −15,2 LUFS, LRA 3,5, pico −4,0 dBFS; 0 silêncios > 1,5 s |
| Telas pretas | 0 |
| Ritmo | 287 planos, média 3,03 s, 19,8 cortes/min (build); detector de cena: 16 no 1º minuto |
| Hook | 31,5 s (alvo ≤ 35 s) |
| Voz (Whisper small, por bloco) | 91 blocos, média **95,6%**, mín. 84,0%. Os 23 abaixo de 93% são grafia: "SS"/"SA" ouvidos como "s s", "ses", "la csa"; Röhm → "Rom", Wewelsburg, Einsatzgruppen → "ansas grupen", Babi Yar → "Bobby Jar", Wannsee → "Juan c", Auschwitz, Oradour, Bremervörde, Priebke → "Priepke", Embu. Nenhuma frase faltando, nenhuma tag falada. Teste prévio: "SS" e "ese ese" saem iguais (2,4 s) |
| Imagens | 188 + 3 thumbs, **0 recusas** do filtro; moldura/faixa em 50 (27%), todas recortadas (≥ 62% da largura) + 3 margens à mão |
| Refeitas (21) | **saudação nazista** num plano de oficiais (I077); braço erguido do Röhm (I049); **águia/emblema** em quepe ou peito (I074, I106, I115, I121, thumb-A, thumb-C) e manga com emblema (I078); braçadeira com marca (I151); texto inventado (I161 "PASSPORT/TICKET", I168 "LÍNEA 60", I172 "1983", I107 números); rostos de "emoji" na multidão (I007); bandeira com símbolo (I029); quepes com águia nos generais (I051); bandeira e broche no Priebke (I180); Heydrich careca (I078 2×); vinheta em fundo branco (I181) |
| Mapa | `map_ruta` (Génova → Buenos Aires; Asunción, São Paulo, Santiago, La Paz), pinos no código, conferidos nos stills |
| Thumbs | A/B/C 1280×720, 132–196 KB; aba "EXPEDIENTE Nº 007", sello "1925–1945"; sem símbolo nazista |

## Para ouvir (Rodrigo; timestamps conferidos na `legendas.srt`)
0:00 hook (Bertioga) · 2:28 "Bad Wiessee / Röhm" · 5:05 "Wewelsburg" · **5:48 "Septiembre de 1939"** (o Whisper ouviu "September": confira se não saiu em inglês) · 6:20 "Babi Yar" · 7:02 "Wannsee" · 10:14 "Bremervörde" · 12:46 "Erich Priebke".

## Observações (ficaram)
- Pré-QA, 2ª rodada: 0 bloqueante; "altos" restantes tratados (I081 com faixa preta à esquerda recortado; I172 refeito) ou aceitos: rabisco numa placa ao fundo em Bariloche (ilegível) e bandeira da Cruz Vermelha no navio em Génova (faz parte da narração).
- Braçadeiras vermelhas **lisas** aparecem em alguns planos de multidão/guardas (sem símbolo): mantidas.
- I152 (médico britânico ao lado de Himmler no chão) é de longe e sem sangue.
