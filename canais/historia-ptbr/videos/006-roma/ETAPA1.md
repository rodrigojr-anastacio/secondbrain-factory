# ETAPA 1 · roteiro + voz · historia-ptbr/006 Roma (id 13) · 09/11/2026

Pergunta central: Como uma cidade que pagou resgate aos bárbaros virou a dona do mundo e, oitocentos anos depois, virou a vencida?

- 2.224 palavras, 65 blocos, hook + 10 eras + fecho. Fio: a balança do "ai dos vencidos" (estrutura no `BRIEF.md`).
- Loops: a espada na balança (hook → era 2 → era 4 "a espada era de Roma" → era 10 resgate de Alarico → fecho, flores na espada); "peças da resposta" (eras 3, 8, 10); "lembra da nossa pergunta?" (era 5); resgate (Breno → piratas de César → Alarico 408).
- Checagem de fatos: `SOURCES.md`. Correções antes da voz: (1) "até ganhar" → "arrancaram a cidadania" (Guerra Social: Roma venceu no campo e cedeu); (2) gauleses "descem dos Alpes" → "do norte" (os sênones já estavam no norte da Itália); (3) "os gauleses de Breno falam francês" → "a terra dos gauleses de Breno fala francês". Lendas marcadas no texto: Rômulo e Remo, Camilo, a frase de Breno ("conta Tito Lívio"), o sinal de Constantino ("diz ter visto").
- Voz: drama-3, 1 chamada por bloco. Teste de nomes (5 blocos): "Tito Lívio" saía "título livre" no Whisper → reescrito "o historiador Tito Lívio… ele era romano". Hook: 4 tomadas, melhor combinação por bloco = repetição melódica **0,09** nos 60 s (só a tomada 1: 0,19). Whisper bruto: mín 89,3% (cortes de palavra: "a Nibau", "da Núvio"); **fonético mín 97,9%, média 99,8%** (`tools/qa_fonetico.py`).
- **Cobrança drama-3 confirmada**: crédito 47,357765 → 47,330855 para 2.691 bytes = US$ 10,0/M (sem o job da KGB gerando no intervalo). Total voz US$ 0,156.
- Teste dos gaps (regra 10): hook N001–N008 com 0,35/0,9/1,5 s = 101,5 s (128 ppm, repetição 0,21); com 0,25/0,6/1,2 s = 100,5 s (129 ppm, 0,15). Os gaps quase não pesam: o drama-3 tem ~23% de silêncio dentro dos blocos. Adotados os gaps novos no `build.py`.

## Checklist v2 (estimado a 130 ppm, antes da voz)
```
Checklist roteiro v2 · 006-roma · bíblia v2 · tempos: estimado a 130 ppm (sem voz)
Pergunta central (declarada no SCRIPT/BRIEF): Como uma cidade que pagou resgate aos bárbaros virou a dona do mundo e, oitocentos anos depois, virou a vencida?
 nº status   item                                                 valor                                  alvo
  1 PASSA    Pergunta central declarada ("Pergunta central:" no S declarada no SCRIPT/BRIEF              declarada
  1 PASSA    Pergunta central (como pergunta) até ~0:50           0:47 em N005                           ≤ 0:50
  2 PASSA    Pergunta volta em voz alta (fora do hook)            5× ['N021', 'N034', 'N050', 'N061', 'N ≥ 3 (fecho responde)
  3 PASSA    Conectivos de virada /100 palavras                   1.57 (35)                              ≥ 1,5
  3 PASSA    Capítulo fecha com o problema da próxima era         10/10                                  todos
  3 PASSA    Nenhum capítulo abre com sucessão seca               0 []                                   0
  5 ok       Capítulo abrindo com data (ficha, não cena)          0 []                                   ≤ 2
  4 PASSA    "Você/imagine" /100 palavras                         1.03 (23)                              ≥ 1,0
  4 PASSA    Capítulo com ponte para o espectador                 10/10                                  todos
  7 PASSA    "Guarde isso" no vídeo                               1                                      ≤ 2
  8 PASSA    Hook até o capítulo 1                                1:10                                   0:60–1:15
  8 PASSA    Promessa em lista                                    nenhuma                                ≤ 2
  9 ok       Falas curtas de personagem                           4                                      1–2+
 10 ok       Ritmo (palavras/min com pausas)                      sem voz ainda                          140–145 (Hipótese)
 10 ok       Palavras por frase (média)                           10.2                                   ≤ 12,5; 5–8 nas viradas
 10 ok       Palavras no roteiro                                  2230                                   ~2.250 p/ 16 min a 140 ppm
 11 PASSA    Fecho (do início do Fecho ao fim)                    0:44                                   ≤ 0:45
  5 MANUAL   1 cena (lugar, pessoa, momento) por capítulo antes d ler                                    todos
  6 MANUAL   Humor seco a cada ~40–60 s, sobre o fato             ler                                    ~15–20 tiradas
  0 MANUAL   Teste da troca + fio condutor ≥ 3 capítulos + loops  ler                                    sim

Resultado: APROVADO
```
Manuais: cena no presente abrindo as 10 eras (brejo, greve, muralha, praia do navio copiado, sítio vendido, piratas, Alexandria, legionário na Britânia, horta de repolhos, margem do Danúbio); humor seco ~1/min (Lívio era romano, sapo e mosquito, "remando no seco", "Elefantes. Na neve.", sal inventado, pernas de banco, piratas, Shakespeare, imposto de herança, repolhos, tabelamento dos anos 80, pimenta); teste da troca ok (cada era nasce do problema da anterior).
