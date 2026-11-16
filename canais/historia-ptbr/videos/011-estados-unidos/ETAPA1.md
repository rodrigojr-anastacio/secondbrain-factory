# ETAPA 1 · historia-ptbr/011 Estados Unidos · youtube.videos id 44 · 16/11/2026

Execução: job `lote-historia-011-estados-unidos-e1` (Opus), brief `~/workspace/referencias/BRIEF-lote-historia-011-estados-unidos-ETAPA1.md`. Custo pago: **US$ 0** (detector usou tradução Haiku com cache, ~US$ 0,01 em créditos da API).

## Passos
1. **pesquisa-referencia** → `BRIEF.md` (referência de forma: Genius History `tn2ehtuk1Gk`, 583.705 views; 12 fatos de fontes próprias; teto US$ 8). `watch.py` não rodou: a legenda completa veio do `manada.py` (forma estudada na transcrição).
2. **ângulo** → `ANGULO.md`: 6 vídeos transcritos (Fun History 12 mi, Knowledgia 4 mi, Impérios AD 1,9 mi, Genius 584 mil, BBC Brasil 546 mil, Legados 97 mil); consenso = "ninguém queria a América do Norte"/Colombo→Roanoke→chá→Luisiana→…→1991. **Ângulo escolhido: a promessa cobrada** (a frase de 1776 cobrada por cada geração; cada cobrança obriga o país a deixar mais gente entrar).
3. **embalagem + crivo** → `EMBALAGEM.md`, `CRIVO.md`: r1 reprovou só a Thumb B (pergaminho rasgado); r2 reprovou só a âncora da Thumb B nas Obrigações (contrariava o NPS); **r3 APROVADO 6/6**. Pares registrados em `youtube.embalagem_variantes`.
4. **roteiro** → `roteiro.py` (fonte única), `SCRIPT.md`, `blocos.json`, `SOURCES.md`. 2.008 palavras, 66 blocos, hook + 10 capítulos + fecho, ~16:04 estimados (126 ppm).
4b. **detector de cópia**: **1/100** (máx. Fun History 1,1; Genius 1,0) → `SIMILARIDADE.md`. **Crivo de ângulo r1: APROVADO** (`CRIVO-ANGULO.md`, 18/19 cenas próprias = 95%). Ajuste recomendado pelo revisor aplicado depois do parecer: a abertura do cap. 9 (mulheres/fábricas, sequência do Genius 10:15–11:06) virou a cena própria de A. Philip Randolph e a Ordem 8802 (1941); detector re-rodado: 1/100; checklist re-rodado: APROVADO. Cota agora 19/19.
5. **storyboard** → `cenas.json` (248 imagens), `STORYBOARD.md`, `storyboard.json` (308 planos, reuso 0% até 3:00 e 24,6% depois, 23 cortes no 1º min, 2 rótulos).

## Checklist do roteiro v2 (`checklist_roteiro_v2.py`, 130 ppm, sem voz)
```
 nº status   item                                                 valor                                  alvo
  1 PASSA    Pergunta central declarada ("Pergunta central:" no S declarada no SCRIPT/BRIEF              declarada
  1 PASSA    Pergunta central (como pergunta) até ~0:50           0:34 em N004                           ≤ 0:50
  2 PASSA    Pergunta volta em voz alta (fora do hook)            5× ['N018', 'N034', 'N044', 'N060', 'N ≥ 3 (fecho responde)
  3 PASSA    Conectivos de virada /100 palavras                   1.74 (35)                              ≥ 1,5
  3 PASSA    Capítulo fecha com o problema da próxima era         10/10                                  todos
  3 PASSA    Nenhum capítulo abre com sucessão seca               0 []                                   0
  5 ok       Capítulo abrindo com data (ficha, não cena)          0 []                                   ≤ 2
  4 PASSA    "Você/imagine" /100 palavras                         1.05 (21)                              ≥ 1,0
  4 PASSA    Capítulo com ponte para o espectador                 10/10                                  todos
  7 PASSA    "Guarde isso" no vídeo                               1                                      ≤ 2
  8 PASSA    Hook até o capítulo 1                                1:13                                   0:60–1:15
  8 PASSA    Promessa em lista                                    nenhuma                                ≤ 2
  9 ok       Falas curtas de personagem                           2                                      1–2+
 10 ok       Ritmo (palavras/min com pausas)                      sem voz ainda                          140–145 (Hipótese)
 10 ok       Palavras por frase (média)                           11.1                                   ≤ 12,5; 5–8 nas viradas
 10 ok       Palavras no roteiro                                  2008                                   ~2.250 p/ 16 min a 140 ppm
 11 PASSA    Fecho (do início do Fecho ao fim)                    0:44                                   ≤ 0:45
  5 MANUAL   1 cena (lugar, pessoa, momento) por capítulo antes d ler                                    todos
  6 MANUAL   Humor seco a cada ~40–60 s, sobre o fato             ler                                    ~15–20 tiradas
  0 MANUAL   Teste da troca + fio condutor ≥ 3 capítulos + loops  ler                                    sim

Resultado: APROVADO
```
Manuais: 1 cena (lugar, pessoa, momento) abre cada capítulo (Jamestown, quarto de Jefferson, Convenção fechada, gráfica cherokee, sino/Seneca Falls, Gettysburg, Centenário, Casa Branca 1917, Randolph 1941, parecer de 1952/King 1963). Humor seco ~1 por minuto fora das eras graves ("elas lembraram dele", "tente explicar essa matemática", "uma coisa muito americana: processaram", o orador de 2 horas, "a liberdade veio cobrar", a carta da mãe, "produto de exportação"); sem humor na remoção cherokee, na Guerra Civil e em Pearl Harbor. Teste da troca: cada era nasce do problema da anterior (impostos → frase → contas → terra → abolição → guerra → lei → imigrantes → voto → guerra → vitrine). Loops: "guarde a pergunta de Douglass" (N006) pago em N065; sino (N005) pago em N030–N031; peças da resposta N018, N034, N060; potência N044, N056; fecho N064–N066.

## Pendências
- Grafias de voz da lista `FALA` não testadas no Fish.
- `src/` e `tools/` copiados do 010: trocar ids/caminhos/composição (etapa 2).
