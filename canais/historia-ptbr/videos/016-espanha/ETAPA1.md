# ETAPA 1 · historia-ptbr/016-espanha · 21/11/2026 (Opus)
`youtube.videos` id 59 · bíblia v2 · custo pago da etapa: US$ 0 (detector sem tradução: refs em pt).

## Resumo
- **Ângulo** (`ANGULO.md`): "a costura": o casamento de 1469 junta coroas, não países; o Novo Mundo é de Castela e o império adia a costura; quando o dinheiro aperta, Madri costura à força (1624–1640, 1707–1717) e cada costura deixa alguém de fora (foros bascos/navarros, a América de Cádis, nacionalismos acelerados por 1898) até a costura assinada de 1978. Descartados: "dominou o mundo e perdeu tudo" (tese da manada + colisão com clones pt) e "península-encruzilhada" (fio do Academia Play).
- **Embalagem** aprovada no crivo **r3** (r1: Thumb A vendia a tese da manada + ref de título fora do padrão; T2 "até 1717" falso → r2: T2 "até 1841" mas Thumb B "CASTELA × ARAGÃO" contradizia → r3: "CASTELA × NAVARRA").
- **Roteiro**: 2.219 palavras, 70 blocos, hook + 10 eras + fecho; estimativa 17:41 a 126 ppm (pelo ritmo real dos 011–014, ~130 ppm, ≈ 17:05). Fio: a costura; pergunta volta 4× (N030, N044, N056, N068). "Guarde" único: o plural "Espanhas" (pago em N033 e N066/N069).
- **Promessa paga:** N003 (~0:25) "junta duas coroas… não dois países: lei, alfândega, moeda"; N004 (~0:41) pergunta central; N005 (~0:50) "rei das Espanhas, no plural, uma pilha de coroas" + "a última alfândega de dentro só caiu em 1841". T2: cena da alfândega no cap. 3 (N018, ~3:45), 1717 em N049 (~11:19), 1841 em N057–N058 (~13:31–13:44). T3: "o império que ainda não era um país" em N035 (~7:48).
- **Detector** (`SIMILARIDADE.md`): **1/100** — só contra as 2 transcrições locais de vizinhos (Espanha × Portugal): o YouTube bloqueou player/legendas pelo WARP a noite toda (22:00–23:20; 9 player clients, IPv4/IPv6, ~40 tentativas). **Crivo de ângulo: APROVADO na r1** (19/19 cenas próprias contra o conferível; 15/19 = 79% na conta conservadora), com a condição de reconferir quando o bloqueio cair (abaixo).
- **Storyboard**: 334 planos, 206 imagens, 22 cortes no 1º min, reuso 38% (47% após 3:00), 22 rótulos, 0 avisos. Prompts ancorados na Espanha (CAS/ARA/NAV/AND/…), sem bandeiras (cancela preta e branca), Franco só como silhueta sem insígnia.

## Checklist v2 (saída do `checklist_roteiro_v2.py`)
```
Checklist roteiro v2 · 016-espanha · bíblia v2 · tempos: estimado a 130 ppm (sem voz)
Pergunta central (declarada no SCRIPT/BRIEF): Por que a Espanha juntou meio mundo antes de conseguir juntar a si mesma?
 nº status   item                                                 valor                                  alvo
  1 PASSA    Pergunta central declarada ("Pergunta central:" no S declarada no SCRIPT/BRIEF              declarada
  1 PASSA    Pergunta central (como pergunta) até ~0:50           0:39 em N004                           ≤ 0:50
  2 PASSA    Pergunta volta em voz alta (fora do hook)            4× ['N030', 'N044', 'N056', 'N068']    ≥ 3 (fecho responde)
  3 PASSA    Conectivos de virada /100 palavras                   2.16 (48)                              ≥ 1,5
  3 PASSA    Capítulo fecha com o problema da próxima era         10/10                                  todos
  3 PASSA    Nenhum capítulo abre com sucessão seca               0 []                                   0
  5 ok       Capítulo abrindo com data (ficha, não cena)          0 []                                   ≤ 2
  4 PASSA    "Você/imagine" /100 palavras                         1.13 (25)                              ≥ 1,0
  4 PASSA    Capítulo com ponte para o espectador                 10/10                                  todos
  7 PASSA    "Guarde isso" no vídeo                               1                                      ≤ 2
  8 PASSA    Hook até o capítulo 1                                1:12                                   0:60–1:15
  8 PASSA    Promessa em lista                                    nenhuma                                ≤ 2
  9 ok       Falas curtas de personagem                           2                                      1–2+
 10 ok       Ritmo (palavras/min com pausas)                      sem voz ainda                          140–145 (Hipótese)
 10 ok       Palavras por frase (média)                           12.5                                   ≤ 12,5; 5–8 nas viradas
 10 ok       Palavras no roteiro                                  2219                                   ~2.250 p/ 16 min a 140 ppm
 11 PASSA    Fecho (do início do Fecho ao fim)                    0:41                                   ≤ 0:45
  5 MANUAL   1 cena (lugar, pessoa, momento) por capítulo antes d ler                                    todos
  6 MANUAL   Humor seco a cada ~40–60 s, sobre o fato             ler                                    ~15–20 tiradas
  0 MANUAL   Teste da troca + fio condutor ≥ 3 capítulos + loops  ler                                    sim

Resultado: APROVADO
```
Manuais: 1 cena por capítulo antes dos fatos (Recaredo 589, Fernando I 1065, o mercador na alfândega, a Casa de Contratação, Carlos nas Astúrias, o memorial de Olivares, o decreto de 1707, Cádis 1812, o fiscal do Ebro, Macià 1931) ✔; humor seco (pastel em maravedis, "um ano, dois troféus", o condomínio, "238 anos de fila", "dois botões soltos", papa morto) ~12 tiradas, algo abaixo da meta de 15–20 (aceito; Hipótese de dosagem); teste da troca ✔ (cada era abre com o problema da anterior); fio em 10/10 capítulos; loops pagos ✔.

## Pendências
1. **Manada sem transcrição (bloqueio do YouTube no WARP).** Quando liberar: `tools/manada.py transcrever ref --ids 90H1JvKT5tI,zlssmpPrJkA,KFe9zlQNuSs,1PAEeroCy9w,rjhIzemLdos,1xmLTdlTLTE,Gwm7eF4NG0A` → rodar de novo `tools/similaridade_roteiro.py` → atualizar a coluna "na manada?" do `SOURCES.md`. ≥ 18 em alguma referência: crivo de ângulo r2 só nos blocos apontados; ≥ 30: reprova (BLOQUEIO com "ângulo"). Ver `ETAPA1-PRONTA.md`.
2. Cartões de data em N055 ("1824", bloco começa em 1814) e N063 ("1931") caem no 1º plano do bloco: na montagem, mover o cartão para o plano da cena que ele data (lição do 014).
3. Sugestão opcional do crivo de ângulo: em N021, a Concordia de Segovia (1475) como cena.
