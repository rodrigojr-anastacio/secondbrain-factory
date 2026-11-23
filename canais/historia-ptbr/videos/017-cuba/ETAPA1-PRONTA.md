# ETAPA1-PRONTA · historia-ptbr/017-cuba · 22/11/2026
`youtube.videos` id 61 · pasta `canais/historia-ptbr/videos/017-cuba/` · pode ir ao ar seg ou qua (o Rodrigo escolhe).

## Ângulo (1 linha)
**Quem compra, manda:** cada comprador de Cuba (a Coroa, os EUA, a URSS, a Venezuela) garantiu o preço cobrando uma cláusula, e cada cláusula só deixava uma saída: outro gigante.

## Portões
- `CRIVO.md` (embalagem): **APROVADO na r3** (r1: T2 "padrinho" e Thumb C "ilha com colher"; r2: T2 "trocou os EUA pela URSS").
- `SIMILARIDADE.md`: **2/100** (ok; cópia ≥ 30).
- `CRIVO-ANGULO.md`: **APROVADO na r3** (r1: respostas do meio = tese do Riqueza e Ruína + 1762/Arango do HistoDarias; r2: N020, fecho "escolhia de quem", 2002 sem fonte).
- Checklist v2: APROVADO (pergunta 0:44, volta 3×, conectivos 1,76, "você" 1,11, ponte 10/10, 1 "guarde", cap. 1 em 1:07, fecho 0:43).

## Os 3 pares aprovados (A = T1, B = T2, C = T3)
| par | título | padrão do título | thumb (padrão) | texto da thumb |
|---|---|---|---|---|
| A | Cuba adoçava o MUNDO. Por que dependia de um país só? | afirmação estranha + pergunta | `rosto-emocao`: guajiro de chapéu de palha e guayabera, sorriso amarelo de pânico, sentado numa pilha de sacos de açúcar no cais de Havana, oferecendo um saco; cargueiro indo embora e farol do Morro ao fundo | "SEM COMPRADOR" |
| B | Por que Cuba só trocava de COMPRADOR? E o que cobravam? | pergunta de transformação + 2º gancho | `numero-estatistica`: "5×" gigante em ouro à esquerda (o maior elemento, **sem caixa em volta**, para não lembrar o 016-C) + 1 saco de açúcar com etiqueta de preço dourada em branco, estrelinha num triângulo vermelho bordado, fundo vermelho liso | "5× O PREÇO" |
| C | Cuba: como o AÇÚCAR decidiu quem mandava na ilha | Como [agente] [verbo] [lugar] | `mapa-lugar`: ilha de Cuba em cartoon (canaviais, chaminés), horizontal e centrada no mar azul, amarrada pela cintura por uma corda grossa **com contorno preto** que sobe esticada para fora do quadro; sem bandeira, sem mão, sem seta | (nenhum) |
Prompts-base de cada thumb: `EMBALAGEM.md` (seções Thumb A/B/C). **3 artes, uma por conceito**; texto composto no código.

## Promessa e onde o roteiro paga
- Promessa: por que Cuba sempre dependeu de um país só para comprar o que produz, e o que cada comprador cobrou.
- Pago no hook: "setecentas mil toneladas ficam sem comprador" **N002 ~0:18–0:23** (Thumb A) → Moscou se oferece para comprar as mesmas **~0:24–0:29** (T2) → "quase cinco vezes o preço do mercado" **N003 ~0:30–0:35** (Thumb B) → os 4 compradores e "nenhum cobrou só em dinheiro" **~0:35–0:46** → pergunta central **N004 ~0:46–0:55**. "Cinco vezes" desenvolvido no cap. 9 (**~13:05**); as 700 mil voltam no cap. 7 (**~10:48**) e no fecho (**~16:54**).
- QA: conferir esses tempos na `legendas.srt` real.

## O que a etapa 2 precisa saber
- Roteiro: 63 blocos, 2.159 palavras (~16:30–17:15). Storyboard: 325 planos, **206 imagens** (`cenas.json`), reuso 45,6% após 3:00, 0 avisos. Rótulos e cartões de data no código (`@@` e `card=` no `roteiro.py`).
- Imagens pelo Codex (`canal.yaml`); prompts já ancorados (sem bandeira de nenhum país, palmeira só a palma real cubana, `NAO_EG`). Conferir a prancha completa antes do pré-QA (vazamento das refs do Egito).
- Voz drama-3; pronúncias no `FALA` do `roteiro.py`. Trilha sintetizada com cor caribenha (tres/clave), sem samples.
- Teto US$ 8: Codex = US$ 0; se cair no fallback fal para tudo (206 × 0,046 ≈ US$ 9,5) estoura: gerar no fal só o que faltar.
- Entrega em `entrega/` (sem `entregar_drive.sh`/rclone): video.mp4, legendas.srt, thumb-A/B/C.jpg, thumbnail.jpg, pacote/youtube.txt com os 3 pares e o padrão de cada um.

## Pendências
- Duração real pode passar de 17 min (016: 2.212 palavras → 17:22): se > 17:30, cortar N015/N019/N044 (passagens). Título sem "em N minutos", então o N não muda nada no título.
- 2026 (N059) com fonte CRS IN12650 + S&P Global: frase neutra, não ampliar.
