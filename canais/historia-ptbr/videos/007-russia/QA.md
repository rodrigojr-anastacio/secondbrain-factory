# QA · historia-ptbr/007 Rússia (id 16) · 09/11/2026 · bíblia de roteiro v2

## Render (`tools/qa.sh`)
- `out/video.mp4`: **16:47** (1007,0 s), 1920×1080, 30 fps, h264 + AAC 48 kHz; 470 MB. Render em 6 partes (+1 refeita), um por vez (esperando o render do Masones).
- Áudio: **−15,2 LUFS**, LRA 3,6, pico −4,3 dBFS. 0 silêncios > 1,5 s. **0 telas pretas.**
- 324 planos (média 3,11 s; 2,1–4,0 s), **24 planos no 1º minuto** (detector de cena: 18, porque Ken Burns em imagens parecidas não conta), 38 cartões de data, 16 rótulos de nome, 12 mapas com rótulos no código (stills em `qa/stills/`; "MAR BÁLTICO" saiu de baixo do cartão de data e "PACÍFICO" da borda antes do render).
- Contact sheet (`out/contact-sheet.jpg`): bonequinhos de cabeça redonda em todos os frames, sem moldura.

## Voz
- drama-3 por bloco, cobrança US$ 10/M confirmada. Whisper fonético mín 95,1%, média 99,1% (`qa/voz_fonetico.json`); 0 tags faladas. Hook: take3, repetição melódica 0,10.

## Imagens
- 198 + 7 refeitas + 8 bases de thumb, nano-banana-2.1/edit + refs. Lote-prova de 6 aprovado com 1 erro (Santa Sofia). 0 pretas, 0 molduras.
- Refeitas: **I058/I061 Santa Sofia em 988 com os medalhões de caligrafia árabe** (que só entram depois de 1453), mesmo pedindo "no Islamic decoration": saiu certo ao **não nomear "Hagia Sophia"** e descrever "Byzantine Christian cathedral… only Christian mosaics, no round medallions, no green discs, no Arabic writing"; o I061 só saiu limpo como close dos enviados com um anjo de mosaico atrás. **I171** (Palácio de Inverno, 1917) com bandeira tricolor francesa e uniformes da Revolução Francesa → "Russian revolutionary soldiers in grey greatcoats… no tricolor flags". **I172** calendário com "OCTOBER/NOVEMBER" em inglês e chapéu bicorne → páginas só com quadrados. **I192** mapa dos 15 países coloriu a Ásia inteira e pôs figuras de turbante → "only the territory of the former Soviet Union is colored… no people". **I095** (fronteira de Moscou, séc. XV) com soldado de **gorro soviético com estrela vermelha** → "15th century… no stars, no modern uniforms" (visto só no contact sheet do render; parte 3 renderizada de novo).

## Checklist roteiro v2 (tempos reais da legenda)
```
Checklist roteiro v2 · 007-russia · bíblia v2 · tempos: legendas.srt (tempos reais)
Pergunta central (declarada no SCRIPT/BRIEF): Como uma terra que precisou chamar estrangeiros para pôr ordem nela virou o maior país do mundo, e por que essa ordem sempre custou tão caro?
 nº status   item                                                 valor                                  alvo
  1 PASSA    Pergunta central declarada ("Pergunta central:" no S declarada no SCRIPT/BRIEF              declarada
  1 PASSA    Pergunta central (como pergunta) até ~0:50           0:41 em N005                           ≤ 0:50
  2 PASSA    Pergunta volta em voz alta (fora do hook)            4× ['N025', 'N037', 'N053', 'N065']    ≥ 3 (fecho responde)
  3 PASSA    Conectivos de virada /100 palavras                   1.92 (41)                              ≥ 1,5
  3 PASSA    Capítulo fecha com o problema da próxima era         10/10                                  todos
  3 PASSA    Nenhum capítulo abre com sucessão seca               0 []                                   0
  5 ok       Capítulo abrindo com data (ficha, não cena)          0 []                                   ≤ 2
  4 PASSA    "Você/imagine" /100 palavras                         1.17 (25)                              ≥ 1,0
  4 PASSA    Capítulo com ponte para o espectador                 10/10                                  todos
  7 PASSA    "Guarde isso" no vídeo                               1                                      ≤ 2
  8 PASSA    Hook até o capítulo 1                                1:10                                   0:60–1:15
  8 PASSA    Promessa em lista                                    nenhuma                                ≤ 2
  9 ok       Falas curtas de personagem                           2                                      1–2+
 10 REPROVA  Ritmo (palavras/min com pausas)                      128 ppm em 16:44                       140–145 (Hipótese)
 10 ok       Palavras por frase (média)                           11.6                                   ≤ 12,5; 5–8 nas viradas
 10 ok       Palavras no roteiro                                  2140                                   ~2.250 p/ 16 min a 140 ppm
 11 PASSA    Fecho (do início do Fecho ao fim)                    0:38                                   ≤ 0:45
  5 MANUAL   1 cena (lugar, pessoa, momento) por capítulo antes d ler                                    todos
  6 MANUAL   Humor seco a cada ~40–60 s, sobre o fato             ler                                    ~15–20 tiradas
  0 MANUAL   Teste da troca + fio condutor ≥ 3 capítulos + loops  ler                                    sim

Resultado: REPROVADO em 1 item(ns)
```
- Único reprovado: **ritmo 128 ppm** (alvo 140–145, Hipótese; mesmo resultado do 006). O orçamento pelo ritmo real funcionou: 2.140 palavras → 16:47 (o 006, com 2.230, deu 17:29).
- Manuais: cena no presente abrindo as 10 eras (Riazan no gelo, margem do Ugra, coroação de 1547, vulcão no Peru, estaleiro holandês, Petersburgo de 1762, Crimeia com navios a vapor…) ✔; humor seco ~1/min (síndico viking, "tente isso com o seu carro", Kalita/condomínio, Ugra, "ninguém desconfia… ou todo mundo finge", comprovante da barba, "ela não reconheceu", Revolução de Outubro em novembro) ✔; teste da troca ✔; fio condutor em 4 capítulos + fecho ✔; fatos com fonte em `SOURCES.md` ✔.
- Neutralidade: termina em 1991 + 1 frase neutra; Ucrânia só como berço comum da Rus de Kiev e na fome de 1932–33.
