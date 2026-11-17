# ETAPA1-PRONTA · dossie-es/010-cartel-medellin (youtube.videos id 45) · 16/11/2026

**Ângulo:** o Cártel de Medellín contado pelo Estado e pelos reféns: a guerra de 12 anos por uma palavra, extradição (1979 → 1991 → 1997).
**Detector de cópia:** 11/100 (ok) · **Crivo de ângulo:** APROVADO na r2 (1 reescrita) · **Crivo da embalagem:** APROVADO na r3 (6/6).

## Os 3 pares aprovados (registrados em `youtube.embalagem_variantes`)
| par | título | padrão do título | thumb (padrão) | texto da thumb |
|---|---|---|---|---|
| A | TODA la Historia del Cártel de Medellín en 14 Minutos \| Su Guerra contra la Extradición | TODA la Historia… \| subtítulo (controle) | algemas de aço abertas em close sobre mesa escura, fundo ardósia, sigla em cor papel (`objeto-simbolo`) | MEDELLÍN + sello INTOCABLES |
| B | CÁRTEL DE MEDELLÍN: La guerra por una sola palabra | NOMBRE: aposto com lacuna | página datilografada ocupando o quadro, uma palavra sob tarja preta, sem carimbo (`documento-evidencia`) | ART. 35 |
| C | Cómo el Cártel de Medellín tomó de rehén a todo un país | Cómo + org + verbo + alvo | de dia, helicópteros sobre a fazenda branca na montanha de Antioquia, de longe, sem armas (`cena-acao`) | ¿RESCATE? (sello com fundo papel) |

## Promessa e onde o roteiro a paga
"TODA la historia del Cártel de Medellín contada desde el otro lado (el Estado y los rehenes): la guerra de doce años que le hizo a Colombia por una sola palabra, extradición, y lo que costó."
- Frase-âncora no bloco **N006 (0:24–0:35)**; exp. 1 "El Tratado" **0:35–1:28** (T1 e lacuna do T2).
- Reféns (T3): exp. 7 (6:31, atentados) e exp. 8–9 (**7:46–9:58**). "¿RESCATE?" (C): exp. 9 (9:00–9:58).
- "ART. 35" (B): **N064 ~10:59** (texto exato) + placar 51–13–5. Algemas/"INTOCABLES" (A): N008 ~0:44, exp. 4, exp. 6 (Lehder) e **N068 ~11:30**.

## O que a etapa 2 precisa saber
- 3 thumbs, **uma por conceito** (A/B/C = T1/T2/T3), prompts em `THUMBS` do `roteiro.py` (thumb-A/B/C no fim do `cenas.json`); texto todo no `src/Thumbnail.jsx`. Ressalvas do crivo: A com aço bem brilhante e sigla clara legível a 320×180; B com a folha ocupando quase tudo (sem mesa que lembre a A) e "ART. 35" em fonte pesada ≥ 1/5 da altura; C com a casa ≥ 1/3 da altura e o sello com fundo papel. Nada de rosto de Escobar.
- 1.967 palavras, ~13:54 estimados (real provável ~14:10): título "en 14 Minutos" se a voz confirmar.
- 204 imagens em `cenas.json` (201 de vídeo + 3 thumbs), custo previsto ~US$ 8,4 de US$ 12.
- **Trocar textos fixos do 009** em `src/Video.jsx` ("DOSSIER · LA GESTAPO · Nº 009"), `Thumbnail.jsx` e `labels.jsx` (único mapa: `map_caribe`, Medellín/Bogotá/Miami).
- Pronúncia a conferir: MAS, DAS, ELN, Criptón, Focine, delegatario.

## Pendências
- Nenhuma que bloqueie. N003 com 1 plano de 3 s (aviso do validador, aceito).
