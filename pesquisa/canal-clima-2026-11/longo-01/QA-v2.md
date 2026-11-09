# QA v2: longo 01 do canal de clima (08/11/2026)

O que mudou na v2: voz ElevenLabs v3 "Fernanda" (antes Kokoro) e texto sem "caixinhas". A edição é a mesma da v1, re-sincronizada com a nova narração. Saídas em `qa/` (fora do git): `qa-v2.txt`, `transcricao-v2.json`, `voz_diff-v2.txt`; conferência da voz bloco a bloco em `work/confere_voz_v2.txt`.

## Critérios objetivos
| Item | Medido | OK? |
|---|---|---|
| Duração | **10:22** (v1: 11:19; a voz nova é mais rápida) | ✅ |
| Formato | 1920×1080, 30 fps, H.264 + AAC 48 kHz | ✅ |
| Loudness | **−14,1 LUFS**, pico −1,3 dBFS, LRA 2,1 | ✅ |
| Telas pretas ≥ 0,2 s | **0** | ✅ |
| Silêncios > 1,5 s | **0** | ✅ |
| Whisper (small) × roteiro, vídeo final | **97,1%** ponderado (números normalizados: "250 km" = "duzentos e cinquenta quilômetros") | ✅ |
| Blocos < 95% | 8 de 51. Todos são grafia do Whisper e não erro de fala: "Chanchere" (Xanxerê), "elninho" (El Niño), "FES2" (F2), "amete o sul" (MetSul), "cepo" (CEP), "40199" escrito como número, gênero do número ("dois mil casas"). Erros de fala de verdade foram refeitos antes da junção (ver abaixo) | ⚠️ aceitável |
| Tags faladas | **0** (nenhum "serious/curious/intrigued" no Whisper de nenhum bloco) | ✅ |
| Perguntas com entonação | **10 de 10** transcritas com "?" (v1: 6 de 10) | ✅ |
| "caixa/caixinha" na fala e na tela | **0** (roteiro, blocos, cues, capítulos). Abas: "PERGUNTA 1/3 · POR QUÊ", "PERGUNTA 2/3 · RISCO", "PERGUNTA 3/3 · ATÉ ONDE" | ✅ |
| Legenda `.srt` | 244 cartões tirados das palavras do Whisper; tempos das perguntas conferidos contra o Whisper do vídeo final (diferença < 0,3 s) | ✅ |
| Capítulos | 11, em ordem desde 0:00 (`PUBLICAR.md`) | ✅ |
| Material real na tela | 41% (258 s de 622 s), os mesmos 33 trechos de vídeo e 14 imagens | ✅ |
| Custo em dinheiro | US$ 0 (`financas.consumo` id 140: assinatura ElevenLabs já lançada no id 51) | ✅ |

## Retakes da voz (v3 erra palavra às vezes; refeito o bloco)
| Bloco | Problema no 1º take | Resultado |
|---|---|---|
| b03 | "Santa Augusto" | take 2 correto |
| b15 | "arrasou" no lugar de "arrasa" | take 2 correto |
| b17 | testado de novo; o take 1 era o melhor | take 1 mantido |
| b20 | "o Araciaba" (Guaraciaba) | take 2 correto |
| b06 | 3ª pergunta saiu sem entonação de pergunta | take 2: as 3 com "?" |
| b36 | "E o aquecimento global" sem pergunta | take 3 |
| b42 | engoliu o "a"; o take 2 inventou uma palavra ("Exposure") no começo | take 3 correto |

## Conferência visual
Stills da pergunta (0:31), das 3 perguntas (0:40), do "Mas antes" (0:47–0:52) e das abas 1/3, 2/3, 3/3 (4:37, 7:14, 8:10) em `work/v2-chk.jpg`; contact sheet `out/contact-sheet-v2.jpg`. Sem quadro quebrado, sem sobreposição nova. O cartão "A PERGUNTA" agora diz "O que está acontecendo no Sul do Brasil? Por que tantos eventos dessa magnitude?" e fica até a 1ª das 3 perguntas.

## Pendências (para o Rodrigo ouvir)
1. **Ritmo do hook:** com atempo de 1,3× o hook ficou em **144 pal/min**, abaixo do resto (173 pal/min a 1,2×), porque o v3 faz pausas dramáticas nas 6 perguntas e nas tags `[serious]`. Se quiser o hook mais corrido, o ajuste é só no `monta_audio_v2.py` (atempo 1,4 no hook), sem gastar crédito, mas exige refazer o render.
2. Trilha e SFX: a mesma mixagem da v1, só re-sincronizada.
3. Continuam valendo as pendências 3–5 do `QA.md` da v1 (mapa vazio em 2–4 s, trechos de origem menos clara, reconferir El Niño em 12/11).
