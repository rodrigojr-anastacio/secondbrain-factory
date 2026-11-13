# RELATÓRIO 002-bikini — "Why Can't You Visit Bikini Atoll?" (youtube.videos id 32) — 13/11/2026

| Item | Valor |
|---|---|
| Vídeo | `entrega/video.mp4` 1920×1080 30 fps H.264 + AAC 192k, **16:04** (28.934 quadros), render Runpod RTX 3090 (16 blocos, 0 refeitos, SSIM 480p mín. 0,964) |
| Loudness | **−15,0 LUFS**, pico −2,1 dBFS (loudnorm −15 no mix + 1,3 dB no AAC) |
| Telas pretas ≥ 0,2 s / silêncios > 1,5 s | **0 / 0** |
| Whisper (voz × texto, 68 blocos) | média **98,4%**, mín. 90,1% (B12c: grafias "Rongalap/Uturik/Rongarik"; B15b/B19c: números por extenso × "$"); nenhuma frase faltando |
| Pré-QA visual | 209 stills Remotion, 2 rodadas `preqa_visual.py`: r1 1 bloqueante + 12 altos (mapa do fallout encavalado, fichas truncadas, faixa preta por crop errado, Número ambíguo) → corrigidos; **r2: 0 bloqueante, 0 alto** (13 médios de estilo; margens de telecine cortadas 2% depois) |
| Roteiro | 2.549 palavras, 21 seções, 3 plantas pagas (167 → 5.400; Saratoga; coco); 13 documentos grifados, 64 trechos de filme, 2 então × agora, 5 mapas, 0 imagem IA no corpo, 90,7% material real |
| Custo | **US$ 1,57** (pré-QA API 0,86 · thumbs fal 0,39 · voz Fish 0,23 confirmada como s2.1-pro pelo crédito 46,41086 → 46,18672 · Runpod 0,09). Teto US$ 6 |

## Correções de fatos (pauta → vídeo)
- "Everything is in God's hands": **sem fonte primária, não usado**. A resposta de Juda é a registrada pela Marinha ("…kindness and benefit to all mankind, my people will be pleased to go elsewhere"), em Cartela "QUOTED".
- Wyatt não pediu a ilha "for the good of mankind": quem buscava o "good of mankind" eram os cientistas com a bomba; o pedido foi "sacrifice your island for the welfare of all men".
- "Ainda não voltaram" → "still can't go home to stay": ~140 voltaram (1972–78) e foram retirados de novo em ago/1978.
- O filme da "reunião" é reencenação (NARA 428-NPC-18008, 06/03/1946); a reunião real foi num domingo, 10/02/1946 (data via Weisgall, que cita registros da Marinha).
- Wyatt aparece de cáqui claro, sentado num tronco (não "de branco").
- Able: "between 1,500 and 2,000 feet off target" (DNA 6032F; o NPS diz 710 jardas).
- Nagato: a fonte diz que lá se recebeu o sinal do sucesso de Pearl Harbor (não que a ordem de ataque saiu dele).

## Para o Rodrigo conferir (tempos da legendas.srt)
- **0:00–0:46** hook: o filme da reencenação + a página do DNA com os 167.
- **3:28–3:42** as falas de Wyatt e Juda em Cartela "QUOTED" (citação de registro, não documento).
- **13:53** os 3 Helldivers + 1 Avenger ainda no hangar do Saratoga (o "3º segredo").
- **15:33** a claquete da Marinha aparece de propósito sob "By one account, it took seven takes" (o "seven takes" é de fonte secundária, atribuído).

## Licenças (amarelos)
Filmes NARA 428-NPC/111-DD marcados "Restricted - Possibly" em lote (material bruto da Marinha/Exército, mesmo caso do Midway); páginas BNL e LLNL (laboratórios do DOE operados por contratadas) mostradas como evidência, LLNL só no recorte de texto; Sentinel-2 com crédito na descrição. Detalhes: `licencas.md`.

## Entrega
`entrega/`: video.mp4, legendas.srt, thumb-A/B/C.jpg (+ thumbnail.jpg = A), `pacote/youtube.txt` (3 títulos pareados, descrição, capítulos, fontes, créditos, tags). **Não subido ao Drive** (regra do lote).
