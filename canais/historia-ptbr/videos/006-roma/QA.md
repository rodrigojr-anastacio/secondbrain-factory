# QA · historia-ptbr/006 Roma (id 13) · 09/11/2026 · bíblia de roteiro v2

## Render (`tools/qa.sh`)
- `out/video.mp4`: **17:29** (1049,2 s), 1920×1080, 30 fps, h264 + AAC 48 kHz; 502 MB.
- Áudio: **−15,2 LUFS**, LRA 3,7, pico −4,1 dBFS. 0 silêncios > 1,5 s. **0 telas pretas.**
- 336 planos (média 3,12 s; 2,23–4,07 s), **24 cortes no 1º minuto**, 32 cartões de data, 13 rótulos de nome, 8 mapas com rótulos no código (stills em `qa/stills/`; "ROMA" do mapa de Cartago reposicionado antes do render).
- Contact sheet (`out/contact-sheet.jpg`): bonequinhos de cabeça redonda em todos os frames, sem moldura.

## Voz
- drama-3, 1 chamada por bloco; **cobrança confirmada a US$ 10/M** (crédito 47,357765 → 47,330855 para 2.691 bytes, sem outro job gerando).
- Whisper por bloco: bruto mín 89,3% (cortes "a Nibau", "da Núvio", "a correntada"); **fonético mín 97,9%, média 99,8%** (`tools/qa_fonetico.py`, `qa/voz_fonetico.json`). 0 tags faladas.
- Hook: melhor tomada por bloco entre 4 (`qa/hook/ESCOLHA.txt`): repetição melódica **0,09** nos 60 s.

## Imagens
- 192 + 3 refeitas + 6 bases de thumb, nano-banana-2.1/edit + refs. Lote-prova de 6 aprovado na 1ª tomada. 0 pretas, 0 molduras.
- Refeitas: I016 (pergaminho com letras inventadas → "only one big drawing… the rest blank"), I171 e I186 (**Constantinopla com minaretes otomanos** em 330 e antes de 1453 → "no minarets, no mosques").

## Checklist roteiro v2 (tempos reais da legenda)
```
Checklist roteiro v2 · 006-roma · bíblia v2 · tempos: legendas.srt (tempos reais)
Pergunta central (declarada no SCRIPT/BRIEF): Como uma cidade que pagou resgate aos bárbaros virou a dona do mundo e, oitocentos anos depois, virou a vencida?
 nº status   item                                                 valor                                  alvo
  1 PASSA    Pergunta central declarada ("Pergunta central:" no S declarada no SCRIPT/BRIEF              declarada
  1 PASSA    Pergunta central (como pergunta) até ~0:50           0:48 em N005                           ≤ 0:50
  2 PASSA    Pergunta volta em voz alta (fora do hook)            5× ['N021', 'N034', 'N050', 'N061', 'N ≥ 3 (fecho responde)
  3 PASSA    Conectivos de virada /100 palavras                   1.57 (35)                              ≥ 1,5
  3 PASSA    Capítulo fecha com o problema da próxima era         10/10                                  todos
  3 PASSA    Nenhum capítulo abre com sucessão seca               0 []                                   0
  5 ok       Capítulo abrindo com data (ficha, não cena)          0 []                                   ≤ 2
  4 PASSA    "Você/imagine" /100 palavras                         1.03 (23)                              ≥ 1,0
  4 PASSA    Capítulo com ponte para o espectador                 10/10                                  todos
  7 PASSA    "Guarde isso" no vídeo                               1                                      ≤ 2
  8 PASSA    Hook até o capítulo 1                                1:11                                   0:60–1:15
  8 PASSA    Promessa em lista                                    nenhuma                                ≤ 2
  9 ok       Falas curtas de personagem                           4                                      1–2+
 10 REPROVA  Ritmo (palavras/min com pausas)                      128 ppm em 17:27                       140–145 (Hipótese)
 10 ok       Palavras por frase (média)                           10.2                                   ≤ 12,5; 5–8 nas viradas
 10 ok       Palavras no roteiro                                  2230                                   ~2.250 p/ 16 min a 140 ppm
 11 PASSA    Fecho (do início do Fecho ao fim)                    0:43                                   ≤ 0:45
  5 MANUAL   1 cena (lugar, pessoa, momento) por capítulo antes d ler                                    todos
  6 MANUAL   Humor seco a cada ~40–60 s, sobre o fato             ler                                    ~15–20 tiradas
  0 MANUAL   Teste da troca + fio condutor ≥ 3 capítulos + loops  ler                                    sim

Resultado: REPROVADO em 1 item(ns)
```
- Único reprovado: **ritmo 128 ppm** (alvo 140–145, Hipótese; a bíblia diz que não bloqueia o 006 com o desvio anotado). Os gaps menores (0,25/0,6/1,2 s) ganharam só ~1 s por minuto: o drama-3 tem ~23% de silêncio dentro dos blocos. Para chegar a 140 ppm, o caminho é texto mais curto, não gap.
- Manuais: cena por capítulo ✔, humor ~1/min ✔, teste da troca ✔, todo loop pago ✔ (espada na balança: hook → era 2 → era 4 → era 10 → fecho), fatos com fonte em `SOURCES.md` ✔.
- Duração 17:29 passa ~0:30 do teto de 17 da bíblia (o brief aceitava 15–18). Título com N = 17.
