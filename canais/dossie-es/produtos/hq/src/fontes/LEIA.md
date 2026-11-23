# Fontes do mangá (fora do git: *.ttf no .gitignore)

| Fonte | Uso | Licença | De onde |
|---|---|---|---|
| Bangers | onomatopeias, título da capa | SIL OFL 1.1 (`OFL-Bangers.txt`) | https://raw.githubusercontent.com/google/fonts/main/ofl/bangers/Bangers-Regular.ttf |
| Comic Neue Bold / Bold Italic | balões e legendas | SIL OFL 1.1 (`OFL-ComicNeue.txt`) | https://raw.githubusercontent.com/google/fonts/main/ofl/comicneue/ |
| Bebas Neue | cabeçalho, carimbos, rodapé | SIL OFL 1.1 | `canais/dossie-es/identidade/fontes/` |
| Special Elite | texto de carta/documento | Apache 2.0 | `canais/dossie-es/identidade/fontes/` |

Todas cobrem ¿¡ÁÉÍÓÚÑÜ«»— (conferido com fontTools em 23/11/2026). OFL permite embutir no PDF vendido.
**Anime Ace (Blambot): não usar.** A licença grátis da Blambot só cobre uso não comercial ou criador independente sob as condições do site; não foi conferida, e a OFL já resolve.

Para baixar de novo:
```bash
cd canais/dossie-es/produtos/manga/src/fontes
for f in bangers/Bangers-Regular.ttf comicneue/ComicNeue-Bold.ttf comicneue/ComicNeue-BoldItalic.ttf comicneue/ComicNeue-Regular.ttf; do
  curl -sSfLO "https://raw.githubusercontent.com/google/fonts/main/ofl/$f"; done
cp ../../../../identidade/fontes/*.ttf .
```
