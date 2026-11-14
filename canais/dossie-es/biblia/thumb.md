# Thumbnail: dossie-es

Regra de canal: **prevalece** sobre `conhecimento/thumbnails/README.md`. Ainda sem thumb no ar (0 vídeos em 2026-11-04).

## Layout "pôster de expediente" (nosso)
- Personagem-ícone em meio corpo à **esquerda** (chefe ou agente arquetípico, com **objeto na mão** que conta o tema) + cenário reconhecível + **SIGLA gigante** (Bebas Neue ou Oswald 700, preta) à direita + **sello rojo inclinado com o período** ("1947–HOY") + **aba de pasta parda** no canto superior direito com "EXPEDIENTE Nº 001". A aba é a nossa assinatura na grade. [estilo.md de 04/11; identidade.md]
- Base em `fal-ai/nano-banana` com "right half empty, no signage, no lettering"; texto em `src/Thumbnail.jsx`. 3 variações para o "Testar e comparar". No teste de estilo es, a base C6 (agente de fedora à esquerda, pasta e selo vermelho, metade direita livre) saiu "pronta para o layout". [testes/ESTILO-es.md]
- Cores: azul-ardósia `#2E3A46`, papel `#E9DFC9`, rojo sello `#B3261E`, tinta `#1A1A1A`. [identidade.md]

## Referência (não copiar)
- **[O] Archive (19 de 19 thumbs):** personagem à esquerda (Himmler, Putin, Dulles, agente de fedora), cenário reconhecível (Lubyanka, Wewelsburg), nome em caixa alta gigante preto no canto superior direito, período "AAAA – AAAA" e ícone-selo redondo; céu azul chapado; contorno preto de quadrinho; nenhuma suástica visível; objeto na mão conta o tema (anel de caveira, carta, pasta com estrela, cachimbo). Atlas del Tiempo e Te lo Pinto (es) copiam o template. [LEVANTAMENTO §2b; mosaico `pesquisa/archive-in-minutes/thumbs/`]
- **[I]** "Pôster de filme" com 1 rosto, 1 palavra e 1 data: reconhecível na grade e legível no celular. A nossa diferença é a pasta/aba + sello.

## Não faça
- Bonequinho de cabeça redonda, panorama com nome de país, papiro (é do `historia-ptbr`).
- Suástica, runas SS e insígnias extremistas; armas na thumb de cartel. Texto em português.
- Copiar a composição exata do Archive (céu azul chapado + selo redondo).

## Políticas do YouTube (14/11/2026, `conhecimento/politicas-youtube.md`)
Thumb sem foto real de morto, sem sangue/ferimento/caveira e sem as palavras proibidas no texto. Em IA: ilustração sem corpo em destaque, sangue, ferimento ou caveira.

## Reembalagem 14/11/2026 (teste aprovado pelo Rodrigo): objeto do caso + sello de lacuna. **Hipótese (teste aprovado 14/11/2026)**, medir CTR
6 thumbs novas (`videos/NNN/reembalagem-2026-11-14/thumb-nova.jpg`; `pesquisa/reembalagem-2026-11-14/thumbs/compose.py`; conceitos em `pesquisa/reembalagem-2026-11-14/PROPOSTAS.md`): **sem personagem**, o **objeto do caso** em tinta ocupando ~55% à esquerda (microfone da CIA, MiG 007, porta arrombada do FBI, estampa de santo em chamas, bolinha do guarda-chuva da KGB, livro de Morgan), SIGLA preta à direita, **sello com uma palavra de lacuna sobre o objeto** (FALSA, FUGA, ¿QUIÉNES?, TRAIDOR, SIN CULPABLE, RITUALES; menor que a sigla e sem alinhar com ela) e aba "EXPEDIENTE Nº". Desvios aprovados: objeto no lugar do personagem e sello de lacuna no lugar do período. Armadilhas: o nano-banana escreve o código de cor ("#E9DFC9") no canto da base (KGB e Masones: refaça ou use a outra tomada) e pôs gotas vermelhas (parecem sangue) na porta do FBI: peça "absolutely NO red color, no blood" e olhe a base de perto; emenda vertical entre ilustração e papel liso se resolve com degradê (`feather` no compose.py).
