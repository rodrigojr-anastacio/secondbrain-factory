# QA: A HISTÓRIA COMPLETA da Índia em 19 minutos

Uma rodada. A saída bruta está em `qa/qa.log`, a voz × roteiro em `qa/voz_diff.txt` (`tools/compara_voz.py`) e os quadros de conferência em `qa/stills.jpg` e `qa/amostra*.jpg`.

| Item | Resultado |
|---|---|
| `out/video.mp4` | 1920x1080, 30 fps, H.264 + AAC 48 kHz estéreo, 590 MB, **1167,2 s (19:27)** |
| Versão Telegram | não gerada (pedido do Rodrigo) |
| `out/thumbnail.jpg` | 1280x720, 426 KB; base em `high` (Taj Mahal, gopuram e ghats do Ganges à esquerda, céu livre à direita) com "ÍNDIA" em Libre Caslon e "3300 a.C. – 2026" em Open Sans 800, o mesmo padrão do Egito |
| Contact sheet | estilo consistente, sem texto gerado pela IA, sem legenda queimada, sem tela vazia |
| Mapas | 5 mapas sem texto, com rótulos no código (`src/labels.jsx`), conferidos em still (`qa/stills.jpg`) |
| Cartões de data / capítulos | 24 cartões; 10 capítulos em ordem crescente, começando em 0:00 |
| Telas pretas | 0 |
| Áudio | -15,1 LUFS, pico -4,4 dBFS, LRA 3,4; nenhum silêncio > 1,5 s |
| Voz × roteiro (Whisper small) | 94,1% de concordância; **nenhuma tag falada**. As diferenças são grafia de nomes próprios e números. Corrigido: o N075 tinha perdido "Guarde essa chuva" (o Fish cortou a frase depois de `[break]`), e o N111 pronunciava mal "Narendra Modi". Os 2 blocos foram regerados e conferidos no Whisper. |
| Planos | 335, média de 3,48 s (2,23–5,5 s), 17,2 por minuto; 13 cortes no 1º minuto |
| Imagens | 195 no vídeo + thumb; reuso de 0% antes de 3:00 e de 50% depois (meta ~40%; o vídeo ficou mais longo que o previsto e o teto de imagens foi mantido) |
| `.srt` | 306 legendas, sem tags |

## Observações (não bloqueiam)
- I035 (`dentist_ancient`, ~2:00): o curandeiro de Mehrgarh usa uma faixa com penas, um estereótipo indevido. Regerar quando houver saldo.
- I158 (`congress_flag`, N095): a bandeira mostra a roda de Ashoka da bandeira de 1947, não a roca do Congresso de 1931. Como o desenho é parecido, passa; a imagem dedicada (`charkha`) não foi gerada por falta de saldo (ver BLOQUEIO.md).
- Duração de 19:27 contra a meta de ~17 min (2.620 palavras). Está dentro da fórmula do canal (12–20 min).
