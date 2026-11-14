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

## Embalagem antes do roteiro (14/11/2026)
Todo vídeo novo passa pela skill `embalagem` + crivo independente (`skills/embalagem/`) **antes** do roteiro; o hook paga a promessa. A thumb nasce do conceito aprovado no crivo; a skill `thumbnail` só executa a arte. Fonte: decisão do Rodrigo, 14/11/2026; base `pesquisa/reembalagem-2026-11-14/padroes.md` e `PROPOSTAS.md` (seção dossie-es).

### Padrões de thumb medidos (Hipótese (reembalagem 14/11/2026, CTR a medir); o CTR nosso conhecido é 2,3% no Mossad, 5.521 impressões, gap 3 do `pesquisa/gap-2026-11-14/RELATORIO.md`)
- **H2, objeto do caso dominante, sem rosto, 0–3 palavras:** [GUtFyu4d9bE](https://youtu.be/GUtFyu4d9bE) (MiG-21 sozinho no quadro) 158.385 · 20/12/2025 · 49,2×; [gutXBSXvOTk](https://youtu.be/gutXBSXvOTk) (MiG visto de cima, "EL ROBO DEL MIG-21") 124.662 · 08/10/2025 · 17,2×. Apoio com rosto ocupando metade: [ppoG_Te4Jpo](https://youtu.be/ppoG_Te4Jpo) 10,2×; [8HFYVHt42Jo](https://youtu.be/8HFYVHt42Jo) 142.869 · 29/09/2026 · 4,5×. Objeto banal **sem nenhum rosto** = **Hipótese** de A/B.
- **H3, retrato tipo ficha policial do chefe real** (máfia, só se o rosto for conhecido): [Corleone…](https://youtu.be/3M6xlSqu1cQ) 645.075 · 02/11/2025 · 9,1×; [Vito Genovese…](https://youtu.be/Q3gRYpKRubw) 172.779 · 30/06/2026 · ~6,0×.
- **H1, rosto famoso ilustrado + sigla gigante:** só refs em inglês (Archive CIA 216.418 e KGB 247.099). Contra direto: Archive FBI (Hoover cartoon) 16.479, 0,3×.

### O que NÃO funciona neste canal
- **Rosto de Hoover** (no ar e no Archive FBI que flopou) e **rosto desconhecido ilustrado** (Buscetta jovem, Cosa Nostra v1, reprovado); **próceres + pergunta** (Masones v1, mesma ideia do Historiador Nocturno, 190 mil).
- **Thumb com muitos elementos:** KGB v1 com 6 (mão, guarda-chuva, lupa, bolinha, ponte, Big Ben).
- **Thumb que repete o título:** guarda-chuva + "LONDRES 1978" + KGB = os 3 substantivos do T2 (KGB v1); "ROBADO" × "Robaron" (FBI v1).
- **Sello que lê junto com a sigla:** "CIA" + "FALSA" vira "CIA FALSA".
- **Agente inventado + faixa pequena** ("EL PARAGUAS", "EL JURAMENTO") somem a 320×180.
- **Castro + caixa de puros** (CIA v1): não casava com o caso do título e os puros valem uma frase (7:19).

### Lições adaptadas a vídeo novo (PROPOSTAS.md (b), 14/11/2026)
- Thumb H2: o **objeto do caso dominante** (o caso que o título nomeia e o roteiro paga cedo), 1 foco, sello de lacuna de uma palavra que não repete o título nem lê junto com a sigla.
- Objeto banal sem rosto é **Hipótese**: medir no "Testar e comparar" e registrar aqui o CTR.
- Conferir a base de perto: o nano-banana escreve código de cor no canto e pode pôr gotas vermelhas (parecem sangue); pedir "absolutely NO red color, no blood".
