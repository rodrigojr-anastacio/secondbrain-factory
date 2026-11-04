# Storyboard V2 — piloto de Sam e Frodo

**Status: implementado, revisado e renderizado em 2026-10-31. Tempos alinhados aos inícios de frase em `out/lotr-pilot-v2-fr.srt`; MP4 final: `out/lotr-pilot-v2-fr.mp4`.**

## Direção

- 60 s, 16:9, ensaio de lore sem rosto; roteiro e narração atuais permanecem iguais.
- 18 batidas visuais (corte médio de ~3,3 s), cada uma começando no início da frase correspondente no SRT; a última vai de 00:51.98 a 01:00.
- Linguagem: mapa ilustrado com rota revelada por máscara, papel/grão, tipografia cinética, zooms de ênfase e parallax 2.5D; nada de tomadas genéricas de natureza como imagem principal.
- Visuais: foto licenciada de Bag End/Hobbiton, fan art licenciada de um hobbit e elementos originais em SVG (mapa esquemático, Livro Vermelho, Anel genérico, silhueta de navio e figuras). Sem cenas de filmes nem ilustrações oficiais.

## Sequência (textos de tela em francês)

| # | Tempo | Âncora da narração | Visual e movimento | Texto de tela |
|---:|:---:|---|---|---|
| 1 | 00:00–00:02.24 | “Frodon part vers l’Ouest” | Foto de Bag End surge por uma máscara circular; um pequeno navio original cruza a tela para oeste; mapa e foto em camadas 2.5D. | **FRODON PART…** |
| 2 | 00:02.24–00:05.30 | “Sam, lui, rentre dans la Comté. Il retrouve Rosie” | Match-cut do navio para a porta redonda; câmera faz push-in na foto de Hobbiton; silhueta original de Sam entra pela trilha. | **SAM RENTRE** / **DANS LA COMTÉ** |
| 3 | 00:05.30–00:09.60 | Fan art de Sam inteira, numa moldura; a moldura e o fundo fazem parallax sutil, sem recortar, recolorir ou apagar a assinatura da arte. Ícones originais de família e livro entram no ritmo das palavras. | **ROSIE · LES ENFANTS · LE LIVRE** |
| 4 | 00:09.60–00:12.18 | “Des années plus tard, après la mort de Rosie” | O Livro Vermelho original abre; folhas passam com uma máscara; luz e cor da Comté mudam de estação. | **DES ANNÉES PLUS TARD** |
| 5 | 00:12.18–00:16.00 | “Sam confie le livre à Elanor et rejoint les Havres Gris” | Livro passa entre duas silhuetas; linha dourada começa no mapa e avança em direção à costa. | **ELANOR** → **HAVRES GRIS** |
| 6 | 00:16.00–00:19.20 | “Pourquoi ? La tradition…” | Breve impacto tipográfico sobre papel; a palavra abre uma janela de máscara para o mapa da rota. | **POURQUOI ?** |
| 7 | 00:19.20–00:21.78 | “le dernier Porteur de l’Anneau à prendre la mer” | Mapa esquemático original, sem copiar o mapa oficial: rota desenhada, marcador de anel e carimbo animado no destino. | **LE DERNIER PORTEUR** |
| 8 | 00:21.78–00:24.48 | “Sam aussi a porté l’Anneau, brièvement” | Anel dourado original gira e atravessa a composição; um traço de luz circunda a figura de hobbit e desaparece. | **SAM AUSSI A PORTÉ L’ANNEAU** / **BRIÈVEMENT** |
| 9 | 00:24.48–00:26.80 | “Son départ fait écho à celui de Frodon” | Tela dividida em dois trajetos/embarcações originais; os movimentos se espelham e depois se afastam. | **UN DÉPART EN ÉCHO** |
| 10 | 00:26.80–00:28.92 | “mais le récit ne raconte pas leurs retrouvailles” | Página do livro fecha parcialmente; a rota se interrompe antes de unir os dois pontos; interrogação aparece por revelação. | **PAS DE RETROUVAILLES RACONTÉES** |
| 11 | 00:28.92–00:32.68 | “partir vers Aman ne rend pas un Hobbit immortel” | Costa original em camadas; o anel se desfaz em reflexos na água, em vez de uma explosão ou efeito mágico genérico. | **AMAN ≠ IMMORTALITÉ** |
| 12 | 00:32.68–00:35.20 | “les mortels autorisés à y séjourner…” | Linha do tempo avança, mas para antes do símbolo de infinito; palavra destacada no tempo da fala. | **SÉJOUR LIMITÉ** |
| 13 | 00:35.20–00:38.56 | “…n’y restent que pour un temps limité” | A linha volta e some sob uma textura de papel; partículas suaves levam o olhar para o oeste. | **PAS POUR TOUJOURS** |
| 14 | 00:38.56–00:42.52 | “L’Ouest offre la paix et la guérison…” | Horizonte costeiro original, camadas de névoa e luz que se move; palavras entram uma por vez. | **PAIX** · **GUÉRISON** |
| 15 | 00:42.52–00:45.14 | “…pas l’éternité. Alors, Sam a-t-il revu Frodon ?” | Zoom de mapa até a costa; a rota some na névoa e deixa a pergunta em primeiro plano. | **SAM A-T-IL REVU FRODON ?** |
| 16 | 00:45.14–00:47.86 | “Le livre laisse la question ouverte” | O Livro Vermelho abre numa página sem resposta; uma linha manuscrita termina em reticências. | **LE LIVRE LAISSE LA QUESTION OUVERTE** |
| 17 | 00:47.86–00:51.98 | “Sam… prend… la route de l’Ouest” | Silhueta de Sam com o livreto embarca; câmera recua enquanto o navio atravessa a linha do horizonte. | **IL PREND À SON TOUR LA ROUTE DE L’OUEST** |
| 18 | 00:51.98–01:00 | Encerramento sem nova narração | Horizonte e anel se apagam para uma cartela limpa; movimento final de câmera e ícone de comentário. | **ET VOUS, VOUS IMAGINEZ LEURS RETROUVAILLES ?** |

## Montagem e áudio propostos

- Legendas palavra por palavra, animadas e sincronizadas pelos timestamps do Whisper; texto corrigido contra o roteiro antes de renderizar (por exemplo, `Comté`, `Rosie`, `Havres Gris`, `Aman`, `Hobbit`).
- Ken Burns em todas as fotos; parallax 2.5D onde houver camadas suficientes; revelações por máscara, grão e papel como camada comum.
- Cinzel nos títulos e Cormorant Garamond nos textos secundários/legendas; tamanhos e áreas seguras próprios para 1080p.
- Whoosh nos cortes de mapa, virada de página no Livro Vermelho, impacto leve no “Pourquoi ?” e som de mar/vento nas pausas. Trilha instrumental licenciada ou original, com ducking sob a narração.
- Narração e roteiro ficam intocados; o mix e a montagem são refeitos.

## Imagens e licenças

- Foto de Bag End/Hobbiton: imagem de local real, licenciada CC BY 4.0; incluir autoria e licença nos créditos.
- Desenho de hobbit: fan art licenciada CC BY-SA 4.0; não é frame nem ilustração oficial. Se não quiser a obrigação de share-alike para adaptações dessa arte, substituí-la por uma silhueta original.
- Mapa, navio, anel, Livro Vermelho, silhuetas e texturas serão arte vetorial original para este vídeo. Manter `ASSET_CREDITS.md` atualizado.
