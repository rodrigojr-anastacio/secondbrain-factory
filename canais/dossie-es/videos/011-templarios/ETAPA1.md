# Etapa 1 · dossie-es/011-templarios · 17/11/2026 (Opus)

## Resumo
- **Ângulo:** a ordem contada pela Coroa de Aragão; fio = o castelo de Monzón (recebido em 1143, berço do rei-menino Jaime I em 1214–1217, último reduto sitiado pelo neto dele em 1308–1309, depois dos Hospitalários). `ANGULO.md`.
- **Embalagem:** crivo r3 APROVADO (r1 3/6, r2 4/6). `EMBALAGEM.md`, `CRIVO.md`, `embalagem/crivo-r*.md`.
- **Roteiro:** 1.840 palavras, 67 blocos, hook + 12 expedientes + cierre, **~13:00 estimados** (WPS 2,38; o canal costuma sair 1,5–3% acima: ~13:15–13:25). Hook = 35,0 s (5 blocos, 80 palavras).
- **Detector de cópia:** **11/100** (máx. Imperios y Misterios 10,9; clone History Condensed 6,2). `SIMILARIDADE.md`.
- **Crivo de ângulo:** r1 REPROVADO (cota 33–42%, abertura 2→4 igual à do Imperios) → reescrita (testamento comprimido; exp. 7 abre na ordem de Jaime II; exp. 8 abre em Monzón; expediente novo "La Roca", Peñíscola/papa Luna) → **r2 APROVADO** (6 de 12 próprios = 50%; +2 parciais). Depois do r2, ajustes não bloqueantes sugeridos pelo revisor: exp. 11 abre na cena do papa Luna, saiu o desmentido da maldição (igual ao clone), fundação com os votos ante o patriarca.
- **Checagem de fatos + revisão nativa** (subagente Sonnet): 31 itens, todos aplicados ou justificados (lista no fim do `SOURCES.md`).
- **Storyboard:** 252 planos, **198 imagens novas + 3 bases de thumb = 201** no `cenas.json`, reuso 21,4% (28,3% depois de 3:00; 0% antes), 23 cortes no 1º minuto, 14 rótulos de nome, 0 avisos. Custo previsto: ~201 × ~US$ 0,04 ≈ US$ 8 + refações (~25% de moldura, recorte grátis) + voz ~US$ 0,2 + Runpod ~US$ 0,2 → **~US$ 9–10 ≤ teto US$ 12**.

## Promessa e onde é paga (tempos estimados no `storyboard.json`)
| âncora (EMBALAGEM) | bloco | tempo estimado | teto |
|---|---|---|---|
| "Monzón, reino de Aragón, mayo de mil trescientos nueve" (T3, Thumb C) | N001 | 0:00–0:04 | 0:04 |
| "…llevan meses asediando este castillo. Dentro resisten, en armas, los últimos templarios del reino" (T1, T3, Thumb C) | N002 | 0:04–0:12 | 0:14 |
| "…la orden crió a un niño huérfano: el abuelo de este rey" (T1, Thumb A) | N003 | 0:12–0:20 | 0:22 |
| "Tres años y medio después, un concilio en Tarragona los declara inocentes. Ya no queda orden que salvar" (T2, Thumb B) | N004 | 0:20–0:29 | 0:29 |
| "Esta es TODA la historia de los Templarios. Y de cómo terminó en Aragón" | N005 | 0:29–0:35 | 0:35 |
| El Testamento (Bayona 1131) + Gerona/Monzón | N014–N016 | 2:07–2:48 | 2:45 / 4:30 |
| El Niño (T1 por inteiro: Muret, Montfort, Monzón, "dos años y medio") | N022–N027 | 3:42–4:46 | 5:30 |
| "Volvemos a Monzón" + El Asedio (paga o hook; Chalamera citada, ressalva do crivo r3) | N038–N042 | 6:53–7:44 | — |
| Tarragona, 4/11/1312 (T2 por inteiro) | N047 | 8:45 | 10:00 |
| Cierre volta a Monzón e ao menino | N063–N067 | 12:06–12:59 | — |
"¿HEREJES?" (Thumb C): acusação de heresia em N035 (6:06) e o cerco em N039. Coroa+manto (Thumb A) no storyboard em N003, N021, N027, N039, N064; pergaminho com selos (Thumb B) em N004, N047, N064; trabuco contra a lua (Thumb C) em N001, N038, N041, N065.

## Checklist da bíblia (`biblia/roteiro.md`)
- [x] Hook ≤ 35 s com anedota própria (Monzón 1309, o neto e o avô; não está em nenhum vídeo da manada), desfecho seco ("Se rinden… Ya no queda orden que salvar") e "Esta es TODA la historia de los Templarios".
- [x] 12 expedientes de ~40–80 s, cada um cena/objeto datado com título falado; o fim de cada um puxa o próximo.
- [x] Anedota paga (exp. 8 "El Asedio", logo depois do CTA, "volvemos a Monzón"); cierre volta ao objeto do hook (o castelo) + aforismo + pergunta.
- [x] Toda acusação atribuída ("la orden de arresto los acusaba de herejía"); lenda não afirmada; ângulo América Latina presente (exp. 12, a bandeira de Cristo no Brasil, Caminha).
- [x] Revisão nativa feita; nenhuma palavra em português na narração ("Belén", não "Belém"; nomes próprios portugueses mantidos).
- [x] Ângulo próprio: `SIMILARIDADE.md` 11 < 30; `CRIVO-ANGULO.md` APROVADO (r2); 6 de 12 expedientes fora da manada (lista no `SOURCES.md`).

## Pendências / avisos para a etapa 2
- **Código copiado do 010:** trocar em `src/Video.jsx` os textos fixos ("CÁRTEL DE MEDELLÍN · Nº 010" → "LOS TEMPLARIOS · Nº 011") e refazer `src/labels.jsx` (pinos do 010!): mapas `map_iberia` (Monzón, Barcelona, Gerona, Bayona, Calatrava, Mallorca, Valencia, Miravet, Tarragona, Peñíscola), `map_holyland` (Jerusalén, Acre) e `map_atlantic` (Lisboa, Brasil). Fazer o grep do nome/número do vídeo anterior antes do 1º render (lição 009). `THUMBS` e prompts das 3 bases já no `roteiro.py`.
- **Pronúncia (Fish):** conferir "Monzón", "Montredón", "Saguardia", "Chalamera", "Peñíscola", "Caminha" ("Camiña"), "Cabral", "Grañena", "Jacques de Molay"; romanos já por extenso.
- **Imagens:** temas de risco = cruz vermelha (ok, não é insígnia extremista) e uniformes medievais com brasões inventados; pedir "no flags with symbols" (já nos prompts de batalha); fogueira de Molay só como fumaça distante (N048), sem figuras. Personagens "resembling" (Jaime I/II, Molay, Bento XIII, Cabral) conferir com visão.
- **Thumbnail:** ressalvas do crivo (A: manto em parte na sombra, sello longe da sigla; B: madeira ≥ 30% e selos grandes, sem letras legíveis; C: lua clara atrás do trabuco, legível a 320×180, nada que pareça forca).
- [PENDENTE] não usados na narração: dia 24/05/1309, comendador de Monzón, início exato do cerco, nº de presos, resposta de Jaime II a Filipe IV, cruz nas velas de Cabral.
