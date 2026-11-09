# Thumbnail: lotr-fr

Regra de canal: **prevalece** sobre `conhecimento/thumbnails/README.md`. Thumbs publicadas na galeria `conhecimento/thumbnails/lotr-fr-*.jpg`.

## Padrão
- A cidade/lugar nomeado tem de ser **aquele** lugar, fiel a Tolkien, em pintura a óleo romântica, com a **pergunta curta em letras grandes** (2 linhas, contraste alto). Texto no código.
- Nada de texto pequeno em várias linhas; nada de pintura real que não representa o lugar.

## Thumbs (análise movida de `conhecimento/thumbnails/README.md`, 2026-11-04)
### lotr-fr-001-maiores-cidades.jpg (no ar)
- Vídeo: "Quelles étaient les plus grandes villes de la Terre du Milieu ?" · `87BdomKxa-M` · `youtube.videos` id 2 · publicado em 2026-11-02.
- Origem: `videos/001-maiores-cidades/thumbs-v2/final/A.jpg` (prompt "A-minas-tirith" em `thumbs-v2.json`, gpt-image-2, 2026-11-03; `financas.consumo` id 13, US$ 0,50 pelas variações A/B/C). SSIM 0,979 com a pública (2026-11-04).
- Tem: Minas Tirith em pintura a óleo romântica (sete níveis, torre branca, luz dourada) à esquerda; céu escuro à direita com "LA PLUS GRANDE" em branco e "VILLE ?" enorme em amarelo.
- **Hipótese:** a cidade mais conhecida, fiel ao livro, + pergunta curta de 2 linhas com contraste alto. **CTR: sem dado** desde a troca. Views: 11 → 36 → 54 (2026-11-02 → 11-04); não dá para atribuir a alta à troca sem o CTR do Studio.
### lotr-fr-001-maiores-cidades-v1-substituida.jpg (o que não funcionou)
- Origem: `videos/001-maiores-cidades/out/thumbnail.png` (3,2 MB), reduzida para JPEG 1280×720 (127 KB). Thumb do pacote original (2026-11-01).
- Tem: "The Course of Empire: The Consummation" de Thomas Cole (domínio público), faixa escura à esquerda e 4 linhas de texto ("LA PLUS GRANDE / VILLE / DE LA TERRE DU MILIEU ? / GONDOLIN · KHAZAD-DÛM · OSGILIATH · ???").
- **CTR medido: 1,7%** (Rodrigo, via `~/workspace/referencias/BRIEF-fase1.md`, 2026-11-04; janela não informada).
- **Hipótese** do porquê: texto pequeno em 4 linhas (ilegível no celular); pintura real/alegórica que não comunica "Terra-média"; contraste baixo (bege e marrom). Trocada pela variação A em 2026-11-03.

## Pendências
- CTR do Studio da variação A (e a janela). Registrar se o "Testar e comparar" A × B × C foi usado e qual venceu.

## Métricas 2026-11-09
- Thumb A: views 11 → 36 → 54 → 61 e **estagnadas em 61 de 05 a 09/11**, 0 inscritos. Não há sinal de ganho a atribuir à troca; **CTR do Studio ainda pendente** (continua Hipótese). Fonte: `youtube.metricas_video`; `pesquisa/metricas/2026-11-09.md`.
