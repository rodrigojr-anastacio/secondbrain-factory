# QA do visual v2 (fase 2): Em Relevo 002 — 10/11/2026

Render `LongoV2` (mistura A/B de `shared/estilo_v2.json` + fotos grandes) em `out/video.mp4`; o anterior ficou em `out/video-v1.mp4` (fora do git).

| Item | Medido | OK? |
|---|---|---|
| Duração | **729,87 s (12:10)**, 21.896 quadros, **igual ao v1** (729,87 s, 21.896 quadros) | ✅ |
| Formato | 1920×1080, 30 fps, H.264 (crf 18) + AAC 48 kHz; 441 MB (o satélite tem mais detalhe que o papel) | ✅ |
| Loudness | **−14,0 LUFS**, pico −1,4 dBFS, LRA 2,2 (mesmo mix e mesma cadeia do v1) | ✅ |
| Telas pretas ≥ 0,2 s | **0** | ✅ |
| Silêncios > 1,5 s | **0** | ✅ |
| Contact sheet | `out/contact-sheet.jpg` (20 quadros) | ✅ |
| Transições A↔B | 14 trocas conferidas quadro a quadro (`qa/v2/transicoes.jpg` → `visual-v2/f2/transicoes.jpg`): 11 no corte de câmera, 3 crossfades de 1,6–1,8 s com a câmera parada; nenhuma pisca no meio de movimento | ✅ |
| Rótulos e números sobre o satélite | rótulos de mapa com texto claro + sombra; UFs tingidas (Roraima/Amapá 6:58), "OCEANO PACÍFICO", alísios, Niño 3.4, pinos do fecho legíveis no A; trechos de dado ficaram no B | ✅ |
| Crédito do mapa | rodapé direito em todo quadro com 3D, troca com a textura (A: `MAPA: NASA BLUE MARBLE · RELEVO: NOAA ETOPO 2022 · LIMITES: IBGE / NATURAL EARTH`; B: `RELEVO: NOAA ETOPO 2022 · COR: NASA BLUE MARBLE · RIOS E LIMITES: NATURAL EARTH / IBGE`); no crossfade um some antes de o outro entrar (sem texto sobreposto) | ✅ |
| Crédito das fotos | as 14 imagens de terceiros + o card do vídeo anterior em quadro grande com legenda e crédito dentro da foto; as 2 fotos da cortiça entram grandes por 3,6 s e pousam no quadro com crédito | ✅ |
| Barra das 4 perguntas | 4 estados ativos conferidos (1:05, 2:52, 5:29, 10:03) + final (11:55): grade de 4 colunas iguais, gap 34 px, texto quebra dentro do card, "▶ AGORA" vira etiqueta acima do card; nenhum card encavala | ✅ |
| Pacífico | textura 85°E–50°W × 45°S–65°N: sem faixa escura no topo | ✅ |
| "Acende Andes" (0:23–0:37) | brilho coral na crista do relevo real (> ~2.300 m, a oeste de 63°W) | ✅ |

## Rodada 1 de correção (feita)
- **Faixa bege no topo** nas cenas de câmera baixa (diorama 1:17–2:00, globo 2:07–2:24 e 9:39–10:00, régua 3:16–3:45 e 4:12–5:07): onde o 3D não tem geometria aparecia o fundo do quadro `#B9A47F` (no v1 era igual ao papel, por isso não se via). O fundo agora acompanha o navy do estilo. 48 blocos re-renderizados; detector de faixa bege no vídeo final: 0 quadros.
- Foto grande sob número grande (ex.: 0:24 "+5,6 °C"): a foto desce para y 215 e fica em 1150 px (60%).

## Observações (não bloqueiam)
- O render levou **~10,7 h** somando os comandos (o 1º passe ~8,4 h; o refazer de 48 blocos foi mais lento porque o host da VPS estava tomando ~53% da CPU, "steal"). Trechos mais pesados: 9:20–9:40 (enchente de 2024), 10:00–11:04 e o fecho 11:40–12:10 (~3–5 s/quadro).
- O relevo de calor do hook/fecho (placa vermelha do mar quente na costa do Peru) é o mesmo do v1.
- Pendências do QA v1 continuam valendo (entonação de b37/b42; "0,00" das montanhas no 1º segundo da régua).

## Para conferir (tempos conferidos na `out/legendas.srt`)
- **0:29–0:33** crossfade A→B em "Fumaça no Norte. Água demais no Sul…" e os Andes acesos.
- **1:13–1:15** crossfade A→B no Pacífico ("Da América do Sul em direção à Indonésia").
- **5:29** barra das perguntas com a 3 ativa (o caso que encavalava).
- **6:19** Norte em satélite ("Comece pelo Norte.") e 6:20 as duas imagens de Boa Vista lado a lado.
- **11:17** foto de Rio do Sul grande na cortiça.
