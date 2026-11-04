# QA: A HISTÓRIA COMPLETA do Egito em 16 minutos

Rodada única (nada reprovado; nenhuma correção pós-render necessária). Saída bruta em `qa/qa.log`.

| Item | Resultado |
|---|---|
| Duração | **954,5 s (15:54)** → N = 16 no título |
| `out/video.mp4` | 1920x1080, 30 fps, H.264 + AAC 48 kHz estéreo, 434 MB |
| `out/video-telegram.mp4` | 1280x720, 30 fps, H.264 + AAC, 44,0 MB (≤ 45 MB) |
| `out/thumbnail.jpg` | 1280x720, 384 KB; fórmula da referência (ilustração à esquerda, céu livre à direita, "EGITO" em Libre Caslon preta, "5000 a.C. – 2026" em Open Sans ExtraBold) |
| Contact sheet | `out/contact-sheet.jpg` (20 frames): estilo consistente, sem texto gerado pela IA, sem legenda, sem tela vazia (1 frame caiu no meio de um crossfade de 5 frames, o que é normal) |
| Ritmo | 294 planos, média de 3,25 s (1,6–4,6 s), 18,5 planos/min na timeline; o scene detect do ffmpeg (limiar 0,3) achou **15 cortes no 1º minuto** (alguns cortes entre imagens de paleta parecida ficam abaixo do limiar) ✅ |
| Imagem × narração (6 pontos) | ✅ Paleta de Narmer (2:34) · Kadesh com cartão 1274 a.C. (7:13) · Pedra de Roseta (12:03) · abertura do Canal de Suez (12:49) · GERD com cartão 2025 em "é uma represa" (15:00) · Pirâmide de Degraus (3:19). Frames em `qa/sync.jpg`, falas em `qa/sync.txt` |
| Legenda queimada | **nenhuma** (só cartões de data, placas de capítulo e rótulos de mapa, todos em serifa e feitos no código) |
| Telas pretas | 0 (blackdetect ≥ 0,2 s) |
| Áudio | -15,2 LUFS integrado, pico -4,4 dBFS, LRA 2,9; nenhum silêncio > 1,5 s; trilha original gerada no código com ducking sob a voz (-33 dB sob a voz) |
| Voz limpa | Transcrição Whisper (small) × roteiro: 93,5% de concordância; as diferenças são só números por extenso ("3200 antes de Cristo" → "3 200 a.C.") e grafia de nomes próprios. Nada faltando, nada repetido, sem cortes ou glitches |
| Pausas | 15 `[break]`, 6 `[long-break]`, 1 `[emphasis]`; ritmo médio de 150 palavras/min |
| Capítulos | 9, em ordem crescente, começando em 0:00, com tempos da timeline real (`qa/capitulos.json`) |
| `.srt` | 258 legendas, geradas dos tempos reais de cada bloco |

## Observações (não bloqueiam)
- Pequenos anacronismos de bandeira: a bandeira atual do Egito (vermelho-branco-preto) aparece nas cenas de 1922 (`independence_1922`) e de 1952 (`nasser_crowd`); a da época era verde com crescente. Nada de texto na imagem.
- `nile_space_night` (1º plano) saiu como vista diurna do Nilo, não como satélite noturno: o estilo do canal ("céu azul") prevaleceu. Combina com a fala ("um rio com um país em volta").
- O mapa do império (`map_empire`) veio como colagem de mapa com quadrinhos laterais; os rótulos (Egito, Síria, Núbia, Mediterrâneo) estão no lugar certo.
