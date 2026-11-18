# ETAPA 1 PRONTA · dossie-es/011-templarios (vídeo id 49) · 17/11/2026

**Crivo da embalagem:** APROVADO na rodada **r3** (r1 3/6, r2 4/6). **Crivo de ângulo:** APROVADO na rodada **r2**. **Detector de cópia:** **11/100**.
**Ângulo (1 linha):** a história inteira dos Templários contada pela Coroa de Aragão, com o castelo de Monzón como fio (o rei-menino criado ali em 1214 e o neto dele sitiando-o em 1309).

## Os 3 pares aprovados (A = T1, B = T2, C = T3)
| par | título | padrão do título | thumb (padrão) | texto da thumb |
|---|---|---|---|---|
| A | Cómo los templarios criaron a un rey… y su nieto los asedió | Cómo + agente + verbo concreto + alvo | coroa de criança sobre o manto templário dobrado, fundo ardósia (`objeto-simbolo`, controle) | sigla TEMPLARIOS + sello HUÉRFANO + aba EXPEDIENTE Nº 011 |
| B | TEMPLARIOS: declarados inocentes cuando la orden ya no existía | SIGLA: aposto com lacuna | sentença em pergaminho com fileira de 6 selos pendentes, luz de vela (`documento-evidencia`) | TARRAGONA |
| C | Monzón, 1309: los últimos templarios en armas | [Lugar], [año]: aposto com o objeto do caso | trabuco em silhueta contra a lua cheia diante do castelo no rochedo, noite azul (`cena-acao`) | ¿HEREJES? |
Registradas em `youtube.embalagem_variantes` (`embalagem_variantes.py registrar --video 49`); `youtube.videos.titulo` = T1.

## Promessa e onde o roteiro a paga
"TODA la historia de los Templarios contada desde la Corona de Aragón: la orden que crió a un rey niño acaba sitiada por el nieto de ese rey en el mismo castillo, como los últimos templarios en armas del reino, y es declarada inocente en Tarragona cuando ya no existía."
- Hook N001–N005 (0:00–0:35): Monzón 1309 (≤ 0:04), cerco e "los últimos templarios del reino" (≤ 0:12), o menino órfão avô do rei (≤ 0:20), Tarragona inocentes (≤ 0:29), "Esta es TODA la historia…" (0:35).
- T1 por inteiro: exp. 5 "El Niño" (N022–N027, ~3:42–4:46); T3: exp. 8 "El Asedio" (N039–N042, ~6:56–7:44, Monzón y Chalamera); T2: exp. 9 "El Concilio", Tarragona em N047 (~8:45). Cierre volta a Monzón (~12:06).

## O que a etapa 2 precisa saber
- 1.840 palavras, 67 blocos, ~13:00 estimados (provável 13:15–13:25 na voz). 252 planos, **201 imagens** no `cenas.json` (198 + 3 bases de thumb `thumb-A/B/C`), reuso 28% depois de 3:00. Custo previsto ~US$ 9–10 (teto US$ 12).
- **3 thumbs, uma por conceito** (A/B/C acima; prompts em `THUMBS` no `roteiro.py`; texto no `Thumbnail.jsx`); nunca 3 variações. Ressalvas do crivo: A manto em parte na sombra e sello longe da sigla; B madeira ≥ 30% e selos grandes, sem letras; C lua clara atrás do trabuco, legível a 320×180, nada que pareça forca.
- `src/Video.jsx` e `src/labels.jsx` vieram do 010: trocar textos fixos e pinos (mapas `map_iberia`, `map_holyland`, `map_atlantic`). Detalhes em `ETAPA1.md` § Pendências.
- Pacote: A = T1, B = T2, C = T3 com o padrão de cada par; capítulos "0:00 El Asedio de Monzón", "El Testamento", "El Niño", "El Concilio" nos pontos de pagamento.

## Pendências
Nenhuma que bloqueie. [PENDENTE] fora da narração: dia 24/05/1309, comendador de Monzón, início exato do cerco, nº de presos, resposta de Jaime II a Filipe IV, cruz nas velas de Cabral.
