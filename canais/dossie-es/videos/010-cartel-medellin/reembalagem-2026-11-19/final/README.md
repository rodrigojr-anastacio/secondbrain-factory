# Thumbs finais da reembalagem do 010 (19/11/2026)

Pares aprovados pelo Rodrigo (crivo r3: B e C). Títulos exatos em `TITULOS.txt`.

| Par | Título | Thumb |
|---|---|---|
| C (principal) | Escobar le declaró la guerra a una PALABRA | `thumb-C.jpg` |
| B | Cómo Escobar tomó de rehén a todo un país | `thumb-B.jpg` |

- Bases nano-banana (`img_fal.py --video 45`): `bases/B2.jpg` (B) e `bases/C4.jpg` (C, 2ª tomada: C1/C2 vieram com a folha em retrato, estreita demais para a palavra). Prompts em `cenas-thumbs*.json`. Custo: 6 imagens, US$ 0,24.
- Todo o texto é composto no código (`compose.py`): "EXTRADICIÓN", as linhas datilografadas, o risco vermelho que termina na ponta da pena, o sello "¿RESCATE?" e a aba "EXPEDIENTE Nº 010". Na C, a mão da base foi deslocada para a direita e a folha foi estendida no código, para a palavra caber grande.
- O que foi conferido contra as condições do crivo:
  - C: folha creme sobre mesa escura; "EXTRADICIÓN" em datilografia pesada, fonte de 145 px (20% da altura; maiúsculas com 100 px, 14%, igual à maquete aprovada); ponta da pena visível no fim do risco; sem rosto, sigla ou carimbo.
  - B: de dia, helicóptero verde-escuro ocupando ~45% do quadro (caixa com o rotor) sobre céu claro; casa antioquenha com telhado de barro e encosta de café/bananeira; sem atirador nem arma (só se adivinha o piloto na cabine, invisível a 160×90); letra do sello com 95 px (13,2%, condição ≥ 12%).
  - Nas duas: sem moldura, sem letras inventadas, sem código de cor no canto e nenhum vermelho que pareça sangue (na B, só o telhado; na C, só o risco).
- `prancha.jpg`: a thumb no ar, a C e a B, cada uma no centro da grade com as 11 do tema, a 320×180 e a 160×90. Nas duas grades a nossa é a única sem rosto: a C é a única folha clara com tipografia, e a B a única de céu e paisagem.
- Pendências:
  - `youtube.embalagem_variantes` não foi registrado: `embalagem_variantes.py registrar` exige A, B e C, e esta reembalagem tem só B e C. O `variantes.json` está pronto (origem `reembalagem`).
  - Crivo r2 da B: se a Thumb C antiga (fazenda + "¿RESCATE?") já rodou no "Testar e comparar", conferir no Studio a fatia dela.
- Drive: `Youtube/Dossier en Minutos/010-cartel-medellin/reembalagem/` (thumb-C, thumb-B, TITULOS.txt).
