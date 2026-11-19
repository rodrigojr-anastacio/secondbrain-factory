# ETAPA 1 PRONTA · dossie-es/012-mi6 · El MI6 · 18/11/2026
`youtube.videos` id 51 · status `roteiro` · custo pago da etapa 1: US$ 0 · detalhes em `ETAPA1.md`.

## Ângulo, detector e crivos
- **Ângulo:** a história inteira do MI6 contada pelos papéis que ele fabricou, vazou ou fez sumir, com o miolo nas Américas (BSC 1940–41) — `ANGULO.md`.
- **Detector de cópia:** `SIMILARIDADE.md` **6/100** (ok).
- **Crivo de ângulo:** **APROVADO na r1** (`CRIVO-ANGULO.md`; 10 de 12 expedientes fora da manada = 83%).
- **Crivo da embalagem:** **APROVADO na r3** (6 de 6; `CRIVO.md`; r1 reprovou T2, Thumb B e Thumb C; r2 reprovou a Thumb B). Pares registrados em `youtube.embalagem_variantes` (`embalagem/variantes.json`).

## Os 3 pares aprovados (A = T1, B = T2, C = T3)
| par | título | padrão do título | thumb (padrão) | texto da thumb |
|---|---|---|---|---|
| A | MI6: el plan nazi para Sudamérica que nadie escribió en Berlín | SIGLA: aposto com lacuna | máquina de escrever dos anos 40 sozinha no escuro, cone de luz forte, sem sigla (`objeto-simbolo`, controle) | NUEVA YORK |
| B | Cómo el MI6 engañó a un presidente, a un país y a sí mismo | Cómo + organização + verbo concreto + alvo | **TESTE "personagem do tema"**: rosto de Roosevelt (~45% da altura) aos microfones de rádio, na mão a folha do discurso com uma linha riscada em vermelho (`rosto-emocao`) | ¿SABÍA? (cor papel sobre carimbo vermelho) |
| C | El Complot Nazi que Nunca Existió \| Expedientes Secretos del MI6 | [Caso concreto] \| plural de operações | o mapa forjado da América do Sul em 5 blocos claro/escuro alternados, pena terminando uma fronteira em vermelho (`mapa-lugar`) | 14 → 5 |

## A promessa e onde o roteiro a paga
- **Promessa:** "Toda la historia del MI6 contada por los papeles que fabricó, filtró o hizo desaparecer, empezando por el plan nazi para Sudamérica que Roosevelt anunció por radio en 1941 y que, según los historiadores, salió de una oficina británica en Nueva York."
- **Hook N001–N004 (0:00–0:36 estimado):** Roosevelt por rádio, "mapa secreto, hecho en Alemania", 14 países → 5 estados vasallos, Panamá (N002, 0:08 = "14 → 5" da Thumb C); "Berlín lo llama falsificación. Según los historiadores, lo era: el mapa salió de una oficina británica en Nueva York" (N003, 0:21–0:29); frase-âncora **"Esta es TODA la historia del MI6. Y de los papeles con que movió el mundo."** (N004, 0:29–0:36).
- **T2:** "un presidente" = hook + N036 "¿Lo sabía Roosevelt?" (6:44, paga o "¿SABÍA?"); "un país" = N018 "Un país votó con un papel falso sobre la mesa" (3:12) e a Bolívia (exp. 6, 5:13); "a sí mismo" = N048 Philby "engañado por dentro" (9:21) e N062 Chilcot (12:23).
- **T3:** N037 "No hay rastro de ese complot nazi para Sudamérica: según los historiadores, nunca existió" (7:01). **T1/Thumb A:** BSC em Nova York (exp. 4, 3:23) e a máquina de escrever feita para imitar a de Belmonte (N032, 5:47).
- Tempos estimados a WPS 2,38; o QA confere na `legendas.srt` (real ~1–3% acima).

## O que a etapa 2 precisa saber
- **3 thumbs, uma por conceito** (A, B, C acima; prompts prontos em `THUMBS` do `roteiro.py` → ids `thumb-A/B/C` no `cenas.json`); A/B/C = T1/T2/T3. Textos no `src/Thumbnail.jsx` (ainda é o do 011: refazer, **sem sigla** nas 3, aba "EXPEDIENTE Nº 012"). Condições do crivo: A com cone de luz forte (folha = ponto mais claro); B com microfones pequenos/escuros e traço vermelho sem escorrer (não parecer sangue), rosto reconhecível; C com blocos claro/escuro alternados e glifo "→" na fonte (senão SVG). No `youtube.txt`, anotar "teste personagem do tema (Thumb B)".
- **Roteiro:** 1.922 palavras, 67 blocos, ~13:34 estimados (hook 35,7 s). **Storyboard:** 263 planos, 191 imagens + 3 thumbs (194), reuso 35,8% depois de 3:00. Custo previsto ~US$ 8,6 (teto US$ 12).
- **Voz:** respelling só no `blocos-voz.json` (lista em `ETAPA1.md`: MI6/MI5, BSC, Estación M, Ordzhonikidze, Exocet, Joe K, Maschwitz).
- **Código do 011 a trocar:** `src/labels.jsx` (pinos dos mapas `map_14`, `map_americas`, `map_atlantic`, `map_south` com "ISLAS MALVINAS"), `src/Thumbnail.jsx`; `src/Video.jsx` já diz "DOSSIER · EL MI6 · Nº 012". Grep "011|TEMPLARIOS" antes do 1º render.
- **Imagens:** conferir com zoom suástica/águia (Berlim, cruzador soviético, arquivos capturados), letras inventadas (cartas, relatórios, aviões LATI/Condor, passaportes), geografia do mapa forjado, rosto de Roosevelt.

## Pendências
- Rascunho riscado de Roosevelt (N036): fonte = Cull citado pela Mental Floss (livro não aberto); o roteiro deixa a dúvida em aberto.
- Hook 35,7 s estimado: se a voz real passar de 36 s, encurtar N002 ("Uno incluye el canal de Panamá" → "Uno, con el canal de Panamá"), sem tirar nada do que a EMBALAGEM obriga.
