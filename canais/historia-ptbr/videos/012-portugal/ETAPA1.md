# ETAPA 1 · historia-ptbr/012-portugal · 17/11/2026
Vídeo id 48 · bíblia de roteiro v2 · ângulo "a linha" (ANGULO.md).

## Resumo
- **Manada:** 11 transcrições (`ref/`): DGP, Impérios AD p1/p2, OSP, This Is History, Merrick, Mundos Reimaginados, Total History, Prisma, H1, Impérios e Lendas (1373). O ângulo candidato do backlog (1807, "fugir para o mar") e um 2º ângulo ("a fatura" do aliado inglês, com hook em Churchill/1943) foram **descartados por serem manada** (Mundos Reimaginados; Impérios e Lendas `vk5QX98PpcI`).
- **Embalagem:** crivo r1 reprovou T3 ("o país que DEVIA ter virado Espanha" = consenso Prisma), Thumb B (marco arredondado lia como lápide) e Thumb C (antes-depois de Elvas pagava só aos 9/14 min); **r2 APROVADO 6/6**.
- **Roteiro:** 2.138 palavras, ~16:43 a 128 ppm (estimador do roteiro.py: 17:10 a 126 ppm). Hook até 1:08; pergunta central aos ~0:43 (N005); fecho ~0:40.
- **Detector de cópia:** 1/100 (máx. `vk5QX98PpcI` 1,1). **Crivo de ângulo:** r1 REPROVADO (cap. 1 abria em São Mamede e cap. 6 em Sebastião/nevoeiro = cenas da manada) → reescrita (cap. 1 em Valença–Tui; cap. 6 em Tomar + alfândega da raia 1582/1591) → **r2 APROVADO** (14/19 cenas próprias = 74%).
- **Fio condutor:** a linha. Peças da resposta: 1297 (assinada no papel quando houve chance, N020), 1383 (gente, N027), 1494 (a disputa vai para o mar, N033), "a pergunta fica mais difícil" (1580, N035), Elvas (N043), onde cedeu (1801, N048), fecho (N061–N062). Loop "guarde" (os marcos que faltam): aberto em N006, pago em N048 e N062.
- **Correção de fato:** Fernando IV tinha **11** anos em 1297 (BRIEF/EMBALAGEM diziam 12; corrigido em todos).

## Checklist v2 (estimado a 130 ppm, sem voz)
```
Checklist roteiro v2 · 012-portugal · bíblia v2 · tempos: estimado a 130 ppm (sem voz)
Pergunta central (declarada no SCRIPT/BRIEF): Como um país menor que Pernambuco segurou a mesma fronteira com a Espanha por setecentos anos?
 nº status   item                                                 valor                                  alvo
  1 PASSA    Pergunta central declarada ("Pergunta central:" no S declarada no SCRIPT/BRIEF              declarada
  1 PASSA    Pergunta central (como pergunta) até ~0:50           0:42 em N005                           ≤ 0:50
  2 PASSA    Pergunta volta em voz alta (fora do hook)            6× ['N020', 'N027', 'N033', 'N035', 'N ≥ 3 (fecho responde)
  3 PASSA    Conectivos de virada /100 palavras                   1.78 (38)                              ≥ 1,5
  3 PASSA    Capítulo fecha com o problema da próxima era         10/10                                  todos
  3 PASSA    Nenhum capítulo abre com sucessão seca               0 []                                   0
  5 ok       Capítulo abrindo com data (ficha, não cena)          0 []                                   ≤ 2
  4 PASSA    "Você/imagine" /100 palavras                         1.03 (22)                              ≥ 1,0
  4 PASSA    Capítulo com ponte para o espectador                 10/10                                  todos
  7 PASSA    "Guarde isso" no vídeo                               1                                      ≤ 2
  8 PASSA    Hook até o capítulo 1                                1:07                                   0:60–1:15
  8 PASSA    Promessa em lista                                    nenhuma                                ≤ 2
  9 ok       Falas curtas de personagem                           4                                      1–2+
 10 ok       Ritmo (palavras/min com pausas)                      sem voz ainda                          140–145 (Hipótese)
 10 ok       Palavras por frase (média)                           11.7                                   ≤ 12,5; 5–8 nas viradas
 10 ok       Palavras no roteiro                                  2138                                   ~2.250 p/ 16 min a 140 ppm
 11 PASSA    Fecho (do início do Fecho ao fim)                    0:40                                   ≤ 0:45
  5 MANUAL   1 cena (lugar, pessoa, momento) por capítulo antes d ler                                    todos
  6 MANUAL   Humor seco a cada ~40–60 s, sobre o fato             ler                                    ~15–20 tiradas
  0 MANUAL   Teste da troca + fio condutor ≥ 3 capítulos + loops  ler                                    sim

Resultado: APROVADO
```
Manuais: 1 cena por capítulo antes dos fatos (Valença–Tui, Porto 1147, Alcanizes, Lisboa 1383, "se por terra não dá", Tomar, Lisboa 1640/Elvas, Alentejo 1801, século XX/Lisboa 1939, Lisboa 1974/Jerónimos/raia 1995) ✔; humor seco (~1/min: "o primeiro inimigo era da família", "Literalmente: não tem mais para onde ir", "O Mestre estava ótimo", "boato no grupo da família", "o que Portugal sabe fazer melhor: discute a linha", "nome de fruta", "a fruta saiu cara", "quem percebe é o telefone") ✔; teste da troca: cada era nasce do problema da anterior ✔.

## Storyboard
329 planos, 216 imagens novas (Codex; fallback fal), reuso 34,3% total / 43,1% depois de 3:00 / 0% antes; plano médio 3,13 s; 24 cortes no 1º minuto; 21 rótulos; 0 avisos de validação.
Custo previsto (etapa 2): Codex US$ 0; se tudo caísse no fallback fal, 216 × US$ 0,046 ≈ US$ 9,9 (acima do teto de US$ 8): **não** deixar o lote inteiro ir para o fal sem conferir (pare em ~150 imagens fal e registre).

## Pendências (não bloqueiam)
- `escala_pe_pt_es` (N005, N061) e Thumb C: compor no código com contornos reais (Natural Earth `~/cache/nasa/ne_50m_admin_0_countries.geojson` + malha IBGE de Pernambuco), mesma escala; o prompt do cenas.json é só fallback.
- Thumb B: conferir numa foto real se os marcos luso-espanhóis trazem "P" e "E" antes de compor (crivo r2).
- N057: Espanha assinando no mesmo 12/06/1985 (CVCE) — conferir no QA.
- Godoy/laranjas: só "diz a tradição" (sem fonte primária).
