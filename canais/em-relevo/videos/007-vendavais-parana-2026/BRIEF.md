# BRIEF · Em Relevo 007 · vendavais no Paraná de 20/11/2026 · 21/11/2026

`youtube.videos` **id 58** (em-relevo, nº 7). Pasta `canais/em-relevo/videos/007-vendavais-parana-2026/`. Pedido do Rodrigo (21/11): "ontem, dia 20 de novembro, rolou uns vendavais novamente aqui no Paraná (Foz, Maringá, Cascavel…), seria legal colocar esse". Brief do lote: `~/workspace/referencias/BRIEF-lote-relevo-007-vendavais-parana-2026.md`. **Etapa 1 só até a aprovação do Rodrigo** (`APROVACAO.md`); etapa 2 não é enfileirada por este job.

## Tema e tipo
Tipo **(Q) quente amarrado a (E) evergreen** (bíblia README: três tipos; "por que X acontece em Y"). Gancho = o temporal de 20/11; pergunta duradoura = **por que o temporal entra pelo oeste/sudoeste do Paraná (e por que voltou tanto em novembro de 2026)**. Desvio consciente da Hipótese "0 Q : 3 E/R até o 1º hit" do README: pedido do Rodrigo, e o vídeo é escrito para valer depois da semana (o 20/11 é o caso, a pergunta é perene). Fica na lista de decisões do `APROVACAO.md`.

## Título de trabalho
"Por que o temporal entra pelo OESTE do PARANÁ?" (fórmula "Por que [LUGAR] [anomalia]?", `biblia/titulo.md`). O título real sai do `EMBALAGEM.md` aprovado no crivo.

## Bíblia do canal (`canais/em-relevo/biblia/`) — as 3 regras que mais pesam aqui
1. **Notícia e depoimento são a manada; o mapa que explica é nosso** (`roteiro.md`, Forma × Conteúdo). Nada de minuto a minuto de TV, nada de imagem de TV/RPC/Globo, nada de vídeo viral (Content ID).
2. **Sem vítima, sem "morte" no título/descrição/tags**; foco em telhado, árvore, poste, radar e satélite (`README.md`, O que NÃO fazer). Neste evento não houve vítima fatal registrada no PR até 21/11 (E2/S).
3. **Não repetir o nosso 001** (`bG6-E4qjXYc`, "O que está acontecendo com o clima no Sul do Brasil?"): ele já explicou o corredor (Amazônia + jato de baixos níveis + Andes + frente fria + cisalhamento + supercélula), o "2º lugar do mundo", a escala Fujita e o El Niño. Aqui isso vira no máximo 1 frase de recapitulação com convite ao 001 (puxar para vídeo publicado pode; `README.md`).

## Duração e tamanho
`canal.yaml`: 10–11 min, 1.700–1.900 palavras, ≤ 10.500 caracteres no TTS, 38–44 blocos. Alvo: **~1.750 palavras, ~10 min**.

## Referência (forma, não conteúdo)
- **Forma do canal** (já medida na bíblia): hook com lugar + data + hora + número (Um Documentário "Era 11 de março de 2011, duas e quarenta e seis da tarde…"; The Last Day "At 8.37 in the morning…"; RELATORIO de 08/11) → pergunta do título até ~0:40 → "a resposta está no mapa" → 4–6 capítulos → A RESPOSTA → fecho útil.
- **Referência de formato do tema** (explicativo no mapa, pt): Além do Mapa "Tem Algo Estranho Acontecendo no Sul do Brasil" (`x_xE2HyxQE0`, 80,4 mil, 06/11/2026, 14:20, 46,9× a mediana de 1.716; capítulos: Andes e choque de massas, Xanxerê, ciclones, corredor, Chapecó, El Niño, "o endereço do choque"). Usada só como prova de demanda e de forma (pergunta geográfica + mapa); o conteúdo dela é o consenso que **não** fazemos.
- **Pendência:** `watch.py`/transcrição barrados — desde 21/11 ~22h o YouTube responde "Sign in to confirm you're not a bot" a qualquer pedido de player/legenda pelo WARP (testados 5 player clients; o mesmo bloqueio registrado no `historia-ptbr/016`). A busca funciona. Ver `ANGULO.md`.

## Fontes principais e fatos fortes (matéria-prima da promessa) — detalhe em `pesquisa/FATOS.md`
1. **O rastro de uma tarde (dado nosso, N1/N2 sobre E4):** os picos de vento de 14 estações do Simepar caem numa reta sudoeste → nordeste (r² 0,98): Capanema 13h45 (81,7) → Cascavel 16h15 → Campo Mourão 17h45 → Maringá 18h45 → Londrina 19h30 → Cornélio Procópio 20h15 (98,3, o maior do dia): ~430 km em ~7 h, ~70 km/h.
2. **Dois tornados F1 no caminho** (Foz ~15h, Manoel Ribas ~18h; E2) e **353.849 imóveis sem energia às 20h02** (E5).
3. **O satélite viu nascer a oeste** (E1 previsão: baixa pressão sobre o Paraguai; E9 GOES-19: às 9h o aglomerado já estava a oeste/sudoeste do PR; às 20h uma faixa atravessando o estado).
4. **De onde vem:** a leste dos Andes estão as tempestades mais intensas do planeta (C1, NASA/TRMM) e complexos de tempestade tão frequentes quanto nos EUA (C2); o sudoeste do PR está no setor de mais tornados do Sul (C3).
5. **O relevo:** o Paraná é uma escada inclinada para oeste: ~120 m em Foz, ~800 m em Cascavel (R1), Primeiro Planalto e Serra do Mar a leste (R2, R3) — o oeste é a ponta baixa e quente, a primeira que a tempestade encontra.
6. **"Novamente":** Rio Bonito do Iguaçu, 07/11/2025, F4, trilha de 75 km de oeste para leste, supercélula a ~80 km/h (B1); Maringá F2 em 02/11/2026 (B2); 493,1 mil sem luz em 07/11/2026 (B4); 20/11 — três grandes temporais em 20 dias; chuva de 1–20/11 ~+61% acima do esperado (N3), calor de 35 °C (B6) e El Niño muito forte (B7).

## Fio condutor e loops
Fio: **a linha das rajadas** — começa como pontos no mapa (hook), vira reta (cap. 1), estica-se para trás até o Paraguai (cap. 2), deita sobre a escada do relevo (cap. 3), ganha as trilhas de 2025–2026 por cima (cap. 4) e fica mais grossa em novembro (cap. 5). Loops: "por que o oeste primeiro?" (aberto no hook, pago no cap. 2–3), "por que de novo?" (aberto no hook, pago no cap. 4–5), "por que de noite no norte?" (aberto no cap. 1, pago no cap. 3 com a velocidade).

## Teto de custo (etapa 2)
Voz ElevenLabs (plano mensal; ~10 mil caracteres) ou reserva Fish #NATASHA drama-3 (~US$ 1); imagens US$ 0 (mapa 3D, satélite NOAA/NASA, fotos CC0); thumbs US$ 0 (código); render Runpod ~US$ 0,05–0,20. **Teto US$ 3.** Etapa 1: US$ 0 (Data API ~25 unidades, `search.list` 0).

## Critérios de pronto / restrições
- Fatos do bloco E reconferidos em fonte primária antes da voz (o que não confirmar vira "segundo o Simepar" ou sai).
- Nenhuma imagem de TV; foto da AEN só CC0 conferida na legenda; Commons com licença por arquivo; GOES/IMERG com crédito na descrição.
- Sem número de vítimas em destaque; Rio Bonito citado pelo rastro (laudo, satélite), não pela tragédia.
- Sem gancho de próximo vídeo; CTA pode puxar o 001 (`bG6-E4qjXYc`).
