# Teste a seco: embalagem com 3 thumbs de padrões diferentes (16/11/2026)

Pedido do Rodrigo (16/11): 3 propostas de thumb realmente diferentes por vídeo. Teste da skill `embalagem` nova, só texto (US$ 0; ~119 unidades da Data API, 0 `search.list`), sem linha no banco.
Tema: Em Relevo, backlog id 28, "Granizo e as tempestades gigantes da Bacia do Prata". Pasta: `granizo/` (BRIEF.md de teste com 7 fatos conferidos, EMBALAGEM.md r2, embalagem/EMBALAGEM-r1.md, crivo-r1.md, crivo-r2.md, variantes.json).

## r1 (crivo: REPROVADO 3 de 6)
| par | título | thumb | crivo |
|---|---|---|---|
| A | Por que as tempestades MAIS FORTES do mundo nascem ao lado do Brasil? | `mapa-lugar`: satélite GOES-19 real, "SÓ UMA NUVEM?" | T1 ok · thumb ok |
| B | Os EUA têm a FAMA, mas os temporais mais intensos da Terra são sul-americanos | `objeto-simbolo`: pedra de granizo cortada em 3D, "TAMANHO REAL" | T2 reprovado (padrão sem evidência) · thumb reprovada (sem referência do padrão; rótulo enganoso) |
| C | A NUVEM que fabricou uma pedra de gelo de 23 cm | `numero-estatistica`: "−90 °C" com régua de altitude | T3 ok · thumb reprovada (**repete a grade do canal**: número gigante) |

## r2 (crivo: REPROVADO 4 de 6)
| par | título | thumb | crivo |
|---|---|---|---|
| A | (mantido) | (mantido) | ok |
| B | AMAZÔNIA tem mais CHUVA, mas a ARGENTINA tem as tempestades mais FORTES: por quê? | `conflito-xvy`: gota × pedra de granizo, raio no meio, "ÁGUA × GELO" | T2 ok (no limite) · thumb reprovada (fotos citadas não servem; "ÁGUA" repete "CHUVA") |
| C | (mantido) | `cena-acao`: supercélula real de San Luis (CC BY-SA), sem texto | thumb reprovada (**mesmo herói da A**: a nuvem; foto genérica vendida como o caso) |
Obrigações: faltou fonte para o lado amazônico do "por quê?".

## Conclusão
- A regra nova funciona: o item 8 do crivo pegou as duas formas de "variação disfarçada" (número gigante igual às vizinhas; a mesma nuvem de outro ângulo).
- O teste parou na r2 por ser a seco (a r3 fica para a produção de verdade, que refaz a embalagem na noite do vídeo).
- Ajustes na skill vindos do teste: pareamento (formar pares e depois numerar), evidência de nicho amplo para os 2 padrões de exploração, comparação com a grade do próprio canal, Em Relevo sem `canal.yaml` (acervo do `PADRAO.md`), ids de `--nossos`, thumb sem texto, armadilhas novas.
- Pendências de script (não corrigidas): `pesquisa_embalagem.py thumbs --ids` ignora sem aviso ids fora do `refs.csv`; `enriquecer` só calcula mediana dos 15 primeiros por views; `--nossos` não confere o canal.
