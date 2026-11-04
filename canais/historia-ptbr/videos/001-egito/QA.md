# QA v2: A HISTÓRIA COMPLETA do Egito em 17 minutos

Rodada única, sem nada reprovado. A saída bruta está em `qa/qa.log` e a comparação em `qa/v1v2.json` (`tools/compara_v1v2.py`). O QA da v1 ficou em `qa-v1/QA-v1.md`.

## v1 × v2
| Item | v1 | v2 |
|---|---|---|
| Duração | 954,5 s (15:54) | **1020,3 s (17:00)**, então N = 17 no título |
| Pausa média real entre blocos (voz → voz) | 0,33 s | **0,90 s** |
| ↳ mesmo assunto (46 viradas) | 0,30 s | 0,55 s (0,35 s de encadeamento + cauda natural) |
| ↳ ideia nova (51) | 0,30 s | **1,10 s** |
| ↳ antes de capítulo (8) | 0,64 s | **1,70 s** |
| `[break]` / tags de tom | 15 / 0 | 50 / 59 (curious 12, serious 16, amazed 8, warm 12, slightly dramatic 11) |
| Imagens | 204 em `low` + thumb `medium` | 204 em **`medium`** + thumb **`high`** |
| Nitidez no zoom máximo (`detalhe-centro`, 1,68x, I185 represa) | 132,6 | 146,1 (variância do Laplaciano, recorte 1:1 do centro) |
| Nitidez média em 8 planos reenquadrados (1,4–1,68x) | 182,6 | **265,5 (+45%)** |
| Cortes no 1º min (scene > 0,3) / planos na timeline | 15 / 23 | 13 / 21 |

As imagens da v2 são gerações novas, então o conteúdo de cada plano muda um pouco e a métrica é ruidosa de plano a plano (2 dos 8 planos caíram). No olho, o recorte 1:1 em `qa/nitidez.jpg` (v1 em cima, v2 embaixo) mostra textura de tijolo e concreto que na v1 era borrão.

## Checagens padrão
| Item | Resultado |
|---|---|
| `out/video.mp4` | 1920x1080, 30 fps, H.264 + AAC 48 kHz estéreo, 531 MB |
| `out/video-telegram.mp4` | 1280x720, H.264 + AAC, 44,1 MB (≤ 45 MB) |
| `out/thumbnail.jpg` | 1280x720; base nova em `high` com a mesma composição (ilustração à esquerda, céu e areia livres à direita), "EGITO" em Libre Caslon e "5000 a.C. – 2026" em Open Sans ExtraBold, como na v1 |
| Contact sheet (`out/contact-sheet.jpg`) | estilo consistente, sem texto gerado pela IA, sem legenda na tela, sem tela vazia |
| Bandeiras | I180 (1922) e I182 (1952, Nasser) agora com a bandeira verde de crescente e 3 estrelas (`qa/bandeiras.jpg`) |
| Telas pretas | 0 |
| Áudio | -15,2 LUFS, pico -4,4 dBFS, LRA 3,4; nenhum silêncio > 1,5 s |
| Voz (Whisper small × roteiro) | 93,0% de concordância (v1: 93,5%). As diferenças são só números ("3200 antes de Cristo" → "3 200 a.C.", "cento e quarenta e seis" → "146"). **Nenhuma tag de tom foi falada**, nada faltando, nada repetido |
| Planos | 295, média de 3,46 s (1,73–5,13 s), 17,3 por minuto |
| Capítulos | 9, em ordem crescente, começando em 0:00 (`qa/capitulos.json`), já atualizados em `out/youtube.txt` |
| `.srt` | 258 legendas, sem tags |

## Observações (não bloqueiam)
- O 1º minuto ficou com 2 planos a menos (21 contra 23), porque as pausas do hook alongaram os planos. Está no limite inferior do ritmo do canal. Se incomodar, dá para acrescentar 2 imagens no `EXTRA` do hook (~US$ 0,08).
- O plano mais longo tem 5,1 s (antes eram 4,6 s); continua com movimento de câmera.
