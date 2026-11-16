# QA · dossie-es 009 La Gestapo (15/11/2026)
| Item | Resultado |
|---|---|
| Render | 14:05 (845,4 s), 1920×1080 30 fps H.264+AAC, −15,1 LUFS, pico −4,2 dBFS, 0 telas pretas, 0 silêncios > 1,5 s; Runpod em 4 faixas, SSIM mín 0,994 |
| Voz | Fish s2.1-pro por frase, US$ 0,18; Whisper × `blocos-voz.json`: média 94,7%; abaixo de 93% só por grafia de nome (Whisper escreve "Heinrich Miller", "Lyon"); "las SS" (respelling "ese ese" saía "la cesar", voltou a "SS"); nenhuma tag falada |
| Promessa (EMBALAGEM) | hook La Paz 1983 → Altmann → Montluc → Barbie 0:00–0:27; frase-âncora "Esta es TODA la historia de la Gestapo" em **0:27,8**; "sótano" em 0:58; "El Barco" (Sudamérica) em 3:29 (`legendas.srt`) |
| Thumb | A/B/C = casaco de couro vazio + "GESTAPO" + sello 1983 (C: "LA PAZ 1983") + aba Nº 009; sem pessoa/insígnia; lê a 320×180. A↔T1, B↔T2, C↔variação |
| Imagens | 187 (nano-banana, US$ 7,44 + 15 refeitas US$ 0,6); moldura/faixa em 44 recortadas; refeitas por texto inventado: I002 I005 I025 I031 I051 I065 I077 I106 I121 I128 I138 I140 I148 I181 I182 |
| Pré-QA | 2 rodadas: 8 bloqueantes → 0; restantes: mapas (falso positivo do modelo; pinos conferidos em still), texto discreto de fundo |
| Bug achado | cartão de capítulo dizia "LA INQUISICIÓN · Nº 008" (copiado do 008) → corrigido, vídeo re-renderizado |
| Custo | fal 8,04 + Fish 0,18 + Runpod 0,25 + pré-QA API 0,83 ≈ **US$ 9,3** (teto 12) |
Pendências menores: texto de fundo ilegível pequeno em alguns planos (calendário no hook `old_young`); "IBM" legível numa máquina de escrever (I11x).
