# Roteiro v2: historia-ptbr (molde History in Minutes)

> **⚠️ v2 vale a partir do 006; vídeos 001–005 seguem a v1 em [`roteiro-v1.md`](roteiro-v1.md).** Aprovada pelo Rodrigo em 07/11/2026 para comparar desempenho: **v1 = 001 Egito, 002 Índia, 003 Irã, 004 China, 005 Brasil** × **v2 = 006 em diante** (como comparar: `README.md`). O 005 Brasil foi escrito com a v1 e o QA dele continua julgando pela v1.

Regra de canal: **prevalece** sobre `conhecimento/roteiros.md` e `conhecimento/hooks.md`. Toda entrada leva data e fonte; sem dado = **Hipótese**.
Base da v2: `pesquisa/roteiro-historia-2026-11/RELATORIO.md` (07/11/2026: 18 transcrições completas de 6 canais, métricas de texto com `metricas_texto.py`, comparação com os nossos 001–004). Abaixo, "§" = seção do relatório. Base que continua da v1: HiM "Iran" (`videos/003-ira/ref/him-iran-XVwr1Rm_9jc.txt`) e o feedback do Rodrigo de 04/11 (`roteiro-v1.md`).
Checklist mensurável: `python3 canais/historia-ptbr/tools/checklist_roteiro_v2.py canais/historia-ptbr/videos/NNN-slug` (seção final).

---

## O que não muda (essência do molde)
- **Narrativa contínua, não fichas.** O vídeo é uma história só, que dá vontade de continuar ouvindo. Cada era nasce da anterior e causa a próxima. Se der para trocar dois capítulos de lugar sem quebrar nada, o roteiro está errado. Feedback do Rodrigo no 003 v1 (04/11/2026): "não tem cara de história, falta conexão entre as partes"; "parece que o cara tá lendo corrido, e não contando uma história".
- **Nada de capítulo-objeto** do Archive in Minutes (é do `dossie-es`; ver `README.md`).
- **8–10 eras cronológicas**, das origens até hoje, com título-frase na placa "CAPÍTULO N" ("O rio que fez um país", "O Céu muda de ideia"), não falado como palavra solta.
- **Fio condutor** nomeado (o Nilo, a monção, o Mandato do Céu, o cavalo de Dario) e **fecho que paga o hook**.
- **Anedota humana forte na abertura** quando ela é a porta do fio condutor (o cavalo de Dario, o elixir de Qin). É o que já fazíamos bem (§4, "manter").
- Bonequinhos de cabeça redonda, narrador que **conta**: isso é visual/voz, mas o texto tem de dar cena para eles.

## A ideia central da v2
Na v1, o fio condutor era um **objeto que reaparece** e o espectador ficava **de fora**, ouvindo sobre reis. Na v2, o fio é **a resposta a uma pergunta sendo montada**, cada era é um **problema que gera o próximo** e o espectador **entra na cena**. Motivo: o histórico "4000 Years of Chinese History" do Breakdown with paint é quase o nosso 004 (mesma abertura, Shang, Mandato do Céu), texto correto, 0,0 "você", sem humor, sem cena, e fez **557 views** (§3). Esse é o risco do molde v1.

---

## As 12 regras da v2

### 1. Pergunta central como pergunta, até ~0:50 (ideal 0:30), com algo em jogo
"Essa é a história inteira de X" vem **depois** da pergunta, nunca no lugar dela. A pergunta tem de terminar em "?" e ser declarada no `roteiro.py` (linha `Pergunta central: …?` no topo do `SCRIPT.md`) e no `ETAPA1.md`.
- *Por quê:* sem pergunta, o espectador não sabe o que está esperando; com ela, cada era vira uma peça.
- *Evidência:* todos do grupo A fazem a pergunta entre 0:14 e 0:56 (Crayon Wolf 0:14, Grande Depressão 0:14, Singapura 0:32, ArchLang hit 0:46, Ink 0:56); o nosso Irã afirma aos 0:51 e só pergunta aos 1:25 (§2.7, §4a). Egito (hook 0:49) **41% assistido** × Índia (hook 2:21) **26%** em `metricas_video` de 07/11 (**Hipótese**, 91 e 59 views).

### 2. A pergunta volta em voz alta ≥ 3 vezes, e o fecho responde e reenquadra
Mais ou menos a cada 4–5 min: "e aqui está a primeira peça da resposta…", "lembra da pergunta? Ela acabou de ficar mais difícil". O fecho **responde** e, se der, **reenquadra** ("talvez a pergunta certa nunca tenha sido…"). As eras continuam cronológicas e ligadas: não são "3 razões" soltas.
- *Evidência:* História na Marra (Habsburgo, 150 mil views): pergunta aos 1:30, volta aos 22:48 ("vamos voltar lá pra pergunta inicial"), reenquadra aos 24:26; ArchLang Egito paga "a primeira, a segunda, a terceira razão" no fecho (§2.2).

### 3. Motor de cada era: problema → solução → novo problema
Cada capítulo **termina com o problema** que a próxima era vai tentar resolver e **abre** com esse problema ou com a cena dele. Proibido abrir capítulo com sucessão seca ("Quem assumiu foi…", "Dessa revolta saiu…", "Quem pegou o trono foi…"). Meta: **≥ 1,5 conectivo de virada por 100 palavras** (mas, só que, então, porque, aí, acontece que, o problema).
- *Por quê:* é o que dá "cara de história" medível; o "mas… então…" que a v1 pedia, agora com número.
- *Evidência:* "But the Shang had a problem… The Zhou had an answer" (Breakdown China, 1:51); "Mas olhar para o mapa também revela uma fraqueza: aquilo não era um país" (HnM, 8:14). Conectivos/100: HnM (pt) **1,2–2,5**, Crayon 1,9–2,2, Ink 1,7–2,3; **nós 0,4–0,9** (§1, §2.3, §4c).
- Ferramentas de ligação que continuam valendo (HiM Irã, v1): causa → consequência explícita ("That one contract shapes everything that follows", 11:46); frase-ponte que vira o jogo ("Isfahan is half the world. / Then half the world fell apart.", 10:18); desmontar o mito ("Here is the problem. It is not.", 3:43).

### 4. Ponha o espectador na cena: "você/imagine" ≥ 1 por 100 palavras + 1 ponte por capítulo
~20 por vídeo: "imagine que você é…", "se você chegasse aqui…", "olhe para…", "tente isso com…". Em cada capítulo, **uma ponte com a vida de quem ouve** (o qanat × o encanamento do seu prédio; o imposto de Dario × o seu IR; o algodão × a camiseta que você está usando).
- *Evidência:* "você" por 100 palavras: Ink **2,5–3,8** (18,4 mi views), Crayon 0,7–1,3, HnM 0,6–0,95; **nós 0,1–0,26**. O hit do ArchLang (1,13 mi) é o único dos 3 vídeos dele com "você" no título ("And Why We Are Next") e abre com "Hey, you!" (§1, §2.1, §3).
- O checklist conta você/vocês/imagine/pense/repare/olhe/tente/te; **não** conta "seu/sua" (em pt quase sempre é "dele"; o relatório contava, então os nossos números da v1 ficam um pouco menores na ferramenta nova).

### 5. Cena antes dos fatos (1 por capítulo)
Abra cada era com **4–6 frases no presente**: um lugar, uma pessoa, um momento. Depois, **no máximo 3 fatos** que provam ou explicam a cena. Curiosidade que não serve à pergunta **sai** (ex.: elamitas e a escrita decifrada em 2022, no Irã).
- *Evidência:* Ink descreve a tarde no acampamento antes da prova ("And this isn't a guess…", 5:36); Crayon dramatiza Raffles no pântano; o Breakdown China, só fato, fez 557 (§2.5, §3, §4d). **Hipótese** quanto ao efeito na retenção.

### 6. Humor seco do narrador a cada ~40–60 s
Ironia, anacronismo, "spoiler: não durou", sempre **sobre o fato**, sem gíria forçada nem meme. Começar com ~1 por minuto e medir.
- *Evidência:* Kelevin, uma tirada a cada 10–15 s ("Good game, Egypt", 19:35); ArchLang ("which historians named with refreshing honesty", 3:09); HnM em pt ("parecia uma pizza cortada em 12 pedaços"). O nosso melhor momento do Irã é desse tipo: "uns gregos teimosos" (N023) (§2.4, §4f). **Hipótese** de dosagem.

### 7. No máximo 2 "guarde isso" por vídeo
O do hook + 1. Os outros callbacks entram **sem anúncio** ("lembra do cavalo?"). O loop principal é a pergunta (regra 2).
- *Evidência:* referências 0–2 "remember/lembra" por vídeo; nós 4–6 "guarde" (Índia 6, Irã 6, China 4) (§2.6, §4e).

### 8. Hook curto: anedota ≤ 45 s → pergunta → "essa é a história" → corpo
Promessa em lista com **no máximo 2 itens** (ou nenhuma); os itens que sobrarem viram mini-hooks dos capítulos deles. **Capítulo 1 entre 1:00 e 1:15** (v1: 1:16–1:32).
- *Evidência:* Wolf, Grande Depressão e Singapura (Crayon, 1,2–4,3 mi) não têm lista, só a pergunta; Índia com hook de 2:21 = 26% assistido (§4g). Sem pedido de inscrição no hook: é o único defeito claro do ArchLang "Revolução" (966 views, CTA aos 1:00) (§3).

### 9. 1–2 falas curtas de personagem nas cenas-chave
Discurso direto, dito pelo narrador, curto ("Senhores, por favor. Uma crise de cada vez."). Uma voz só: escreva com o verbo antes ("Dario olha para o cavalariço e diz: faça acontecer.") para o drama-3 marcar a mudança.
- *Evidência:* Crayon, micro-diálogos encenados nos 3 vídeos (1,2–4,3 mi) (§2.4). **Hipótese:** testar no drama-3 se soa natural com uma voz só.

### 10. Ritmo: ~140–145 palavras/min e frases curtas nas viradas
Viradas com **5–8 palavras** ("Então o Céu mudou de ideia."); o resto alternando frase longa com vírgula de respiração e pergunta. Média ≤ 12,5 palavras por frase.
- *Evidência:* a referência mais lenta é a HnM (pt, voz humana), **137–176 ppm**; nós **129–136** com o drama-3 e as pausas (§1, §4h). **Hipótese.**
- **Como chegar lá sem mudar a voz aprovada:** a voz é a do `voz.md` (drama-3 por bloco). O ganho vem de (a) frases mais curtas e menos blocos de uma frase só e (b) testar no 006 gaps menores no `build.py` (0,35/0,9/1,5 s → ~0,25/0,6/1,2 s), medindo os 60 s iniciais antes do vídeo inteiro (`videos/003-ira/v2-amostras/voz/medir.py`). Até medir, **escreva com o ritmo real**: ~128 ppm → 16 min ≈ **2.050 palavras**; se os gaps menores derem ~140 ppm, 16 min ≈ 2.250.

### 11. Fecho ≤ 45 s depois do payoff
Responde a pergunta, reenquadra, pergunta para os comentários e **acaba**. Sem resumão das eras.
- *Evidência:* Kelevin ("All right, that's everything", 19:44); ArchLang hit (punchline em 30 s); HnM (reenquadra e acaba) (§2.8). China 004: fecho de 0:51.

### 12. Checklist mensurável (abaixo), rodado pela skill `roteiro` e pela `qa`

---

## Estrutura v2 (esqueleto)
1. **Hook (≤ 1:15 até o cap. 1):** anedota-porta no presente (≤ 45 s, com o espectador dentro: "imagine que você…") → **pergunta central** (≤ 0:50) → "Essa é a história inteira de X" → no máximo 2 itens de promessa (ou nenhum) → 1 "guarde" (opcional) → o **problema** que abre a era 1.
2. **Corpo: 8–10 eras.** Cada uma: problema herdado → **cena** (4–6 frases, presente) → ≤ 3 fatos → solução → **novo problema** (gancho). Em cada era: 1 ponte com o espectador, 1 tirada seca, conectivos. A cada ~4–5 min, a pergunta volta em voz alta ("primeira peça da resposta…").
3. **Fecho (≤ 45 s):** paga o loop do hook, responde, reenquadra, pergunta para os comentários.

## Exemplo: hook do Irã reescrito na v2 (§6 do relatório)
Original (003 v2, v1): 203 palavras, 1 "guarde", 0 "você", "Essa é a história" aos 0:51, pergunta aos 1:25, cap. 1 aos 1:32. Reescrito: ~155 palavras, pergunta aos ~0:50, cap. 1 aos ~1:13 (números = regras acima).

> Pérsia, quinhentos e vinte e dois antes de Cristo. Imagine que você é um dos seis nobres que vão escolher o rei do maior império do mundo. *(4)*
> O método: ao nascer do sol, todos saem a cavalo. O cavalo que relinchar primeiro… faz do dono um rei. *(10)*
> Só que Dario tem um cavalariço esperto. Na véspera, ele leva o cavalo até aquele ponto… com uma égua. De manhã, o cavalo passa ali, lembra da noite… e relincha. *(3)*
> Dario vira rei do Egito à Índia, escolhido por um cavalo… e por uma trapaça. Pelo menos segundo Heródoto. Um grego. E grego não era exatamente fã de persa. *(6)*
> Fica a pergunta: **quem escolhe quem governa o Irã?** Gregos, árabes, mongóis, britânicos e americanos vão tentar escolher por ele. E o Irã continua Irã. Como? *(1)*
> *(promessa em lista cortada: 8)*
> Essa é a história inteira do Irã. Guarde esse cavalo: ele volta no final. E tudo começa com um problema menos nobre que um trono. Água. *(7; 3)*

Começo do capítulo 1:
> Olhe para o planalto do Irã: uma tigela de montanhas, deserto no meio, quase nenhuma chuva. Se você chegasse aqui há seis mil anos, a pergunta não seria quem manda. Seria: onde é que eu bebo? *(4, 5)*
> A resposta foi cavar. Túneis de quilômetros, os qanats, inclinados na medida para a água da montanha descer sozinha. Alguns funcionam há mais de dois mil anos. Tente isso com o encanamento do seu prédio. *(4, 6)*
> Onde o túnel acabava, nascia um jardim murado: *pairidaêza*. A palavra viajou pelo grego, pelo latim… e chegou até você como **paraíso**. Só que todo paraíso no deserto tem um problema: os vizinhos também querem. *(7: sem "guarde"; 5: elamitas saem; 3: gancho da próxima era)*

## Tom e escrita (continua da v1, ajustado)
- Narrador que **conta**: presente nas cenas e no hook, passado narrativo no resto. Linguagem falada (`conhecimento/roteiros.md`): frases de 4–14 palavras, vírgula onde se respira, "…" só na virada, nunca 3 frases seguidas abrindo com data.
- Sem "olá, pessoal", vinheta ou pedido de inscrição no hook.
- **Remodelar a transcrição da referência** continua valendo (mesma ordem, beats e números, texto reescrito em pt-BR, ~30% mais curto), **mas passando pelas regras da v2**: trocar a ficha por cena, pôr o "você", cortar a lista do hook. Troque autorreferências do concorrente por equivalente brasileiro do mesmo fato (fome de 1876 na Índia ↔ Grande Seca de 1877 no Ceará).

## Tamanho (com a voz do canal)
| Vídeo | Bíblia | Palavras | Estrutura | Duração | ppm (com pausas) | Fonte |
|---|---|---|---|---|---|---|
| Egito (publicado) | v1 | 2.293 | hook + 8 | 17:00 | ~136 | QA.md 001 |
| Índia (publicado) | v1 | 2.620 | hook + 9 | 19:27 | ~136 | ETAPA-FINAL.md 002 |
| Irã 003 v2 (drama-3) | v1 | 2.282 | hook + 10 + fecho | 18:01 | ~127 | RELATORIO.md 003 v2 |
| China 004 (drama-3) | v1 | 2.093 | hook + 10 + fecho | 16:14 | ~129 | RELATORIO.md 004 |
- Alvo: **15–17 min**. Com o ritmo medido (~128 ppm), 16 min ≈ 2.050 palavras: ~150 no hook, ~185 por era (10 eras), ~90 no fecho (≤ 45 s). O 004 saiu com 2.492 no 1º rascunho: escreva já mirando o orçamento.
- **Hipótese:** 15–17 min seguram tanto quanto as referências; o hit do ArchLang tem 12:31 e os fracos 18–23 min (§3), então **não** passe de 17.

## Histórico e evidências da v1
Fórmula de hook de 6 referências (02/11), hooks do Egito/Índia/Irã/China com tempos e o processo do 004: em [`roteiro-v1.md`](roteiro-v1.md) ("Evidências de hook"). Medir a retenção aos 30/60 s dos vídeos v1 × v2 (`README.md`).

---

## v1 → v2: o que mudou
| Ponto | v1 (001–005) | v2 (006+) | Evidência |
|---|---|---|---|
| Pergunta central | depois de "Essa é a história" (Irã 1:25) | pergunta com "?" até ~0:50, declarada | grupo A 0:14–0:56 |
| Fio condutor | objeto que reaparece | a resposta sendo montada; pergunta volta ≥ 3× | HnM 1:30 → 22:48 → 24:26 |
| Ligação das eras | "mas… então…" sem meta | problema → solução → novo problema; ≥ 1,5 conectivo/100; sem sucessão seca | HnM 1,2–2,5 × nós 0,4–0,9 |
| Espectador | fora ("sobre" reis) | ≥ 1 "você/imagine"/100 + 1 ponte por capítulo | Ink 2,5–3,8 × nós 0,1–0,26 |
| Capítulo | mini-hook + fatos | cena (4–6 frases) antes de ≤ 3 fatos | Ink, Crayon; Breakdown China 557 |
| Humor | ocasional | tirada seca a cada ~40–60 s | Kelevin, ArchLang, HnM |
| "Guarde isso" | 4–6 | ≤ 2 | refs 0–2 |
| Hook | 40–60 s (teto 90), promessa 3–5 itens; real 1:16–2:21 | anedota ≤ 45 s, promessa ≤ 2, cap. 1 em 1:00–1:15 | Crayon sem lista; Índia 26% |
| Falas | nenhuma | 1–2 falas curtas de personagem | Crayon (Hipótese no drama-3) |
| Ritmo | ~127–136 ppm | ~140–145 ppm, viradas de 5–8 palavras | HnM 137–176 (Hipótese) |
| Fecho | paga o loop + pergunta (China 0:51) | ≤ 45 s, responde e reenquadra, sem resumo | Kelevin, ArchLang, HnM |
| Checklist | 6 itens lidos | `checklist_roteiro_v2.py` (medido) + 3 manuais | — |

## Checklist do roteiro v2 (só vídeos ≥ 006; a skill `roteiro` e a `qa` conferem)
Rode `python3 canais/historia-ptbr/tools/checklist_roteiro_v2.py canais/historia-ptbr/videos/NNN-slug` (antes da voz estima tempos a 130 ppm; com `out/legendas.srt` usa os tempos reais). Cole a saída no `ETAPA1.md` (roteiro) e no `QA.md` (qa). Código 1 = reprovou.
- [ ] `Pergunta central: …?` declarada no `SCRIPT.md`; dita como pergunta até ~0:50 (regra 1).
- [ ] Pergunta volta ≥ 3× fora do hook; fecho responde e reenquadra (2).
- [ ] Conectivos ≥ 1,5/100; todo capítulo fecha com o problema da próxima era; nenhum abre com sucessão seca (3).
- [ ] "Você/imagine" ≥ 1/100 e ponte em todo capítulo (4).
- [ ] ≤ 2 "guarde" (7). Cap. 1 entre 1:00 e 1:15; promessa ≤ 2 itens (8).
- [ ] Ritmo 140–145 ppm depois da voz (10; Hipótese, não bloqueia o 006 se o resto passar e o desvio estiver anotado). Fecho ≤ 45 s (11).
- [ ] Aviso (não bloqueia): 1–2 falas de personagem (9); ≤ 2 capítulos abrindo com data; média ≤ 12,5 palavras/frase.
- [ ] **Manual:** 1 cena por capítulo antes dos fatos (5); humor seco a cada ~40–60 s (6); teste da troca, fio condutor em ≥ 3 capítulos, todo loop pago; todo fato com fonte em `SOURCES.md`.
- **Resultado de referência no 004 China (v1, 07/11/2026):** reprova em 12 itens obrigatórios: pergunta não declarada, volta 1× (alvo 3), conectivos 0,91, 4/10 capítulos fecham com problema, 3 aberturas de sucessão seca (caps. 4, 7 e 10), "você" 0,19 e ponte em 2/10 capítulos, 4 "guarde", cap. 1 aos 1:17, promessa de ~3 itens, 129 ppm, fecho de 0:51. Passa: pergunta aos 0:42. É o retrato do que a v2 corrige.
