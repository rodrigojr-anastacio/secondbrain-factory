# Thumbs reais · lugares-guerra-en/006-chernobyl · 21/11/2026

**Pedido do Rodrigo (21/11/2026):** "Nada a ver essas thumbs... quero uma que tenha alguma imagem real de Chernobyl, máscara de gás, algo assim." As thumbs gráficas da embalagem (`thumbs/final/A/B/C`: cartões flip "67 HOURS", mapa com sapato, roda-gigante dividida) foram **reprovadas** por ele. Estas substituem as 3 no "Testar e comparar".

**Desvio da bíblia (declarado):** `biblia/thumb.md` pede base **ilustrada** (corte, gpt-image-2). Aqui a base é **foto real** do Wikimedia Commons, dessaturada, com só o amarelo-radiação mantido em cor: desvio porque o **Rodrigo pediu foto real em 21/11/2026**. Mantidos da bíblia: Anton amarelo `#FDD505` com contorno preto grosso, 1 foco, texto que complementa o título e o selo "RESTRICTED".

## As 3 thumbs
| par | título | thumb | foto-base | padrão | texto |
|---|---|---|---|---|---|
| A | Chernobyl Burned for Days Before the World Knew | `thumb-A.jpg` | máscara de gás pendurada numa sala de aula da escola de Pripyat (close dominante, ~50% do quadro) | `numero-estatistica` (número gigante + objeto) | "67 HOURS" |
| B | Why Was Chernobyl's Alarm First Raised in Sweden? | `thumb-B.jpg` | dosímetro Terra-P amarelo em mão na zona de exclusão, usina ao fundo | `objeto-simbolo` (o detector como herói) | "ON A SHOE" + bandeira sueca |
| C | The Bus Order Pripyat Wasn't Told About | `thumb-C.jpg` | roda-gigante do parque de Pripyat em contra-plongée | `mapa-lugar` (o lugar-ícone: monumento da cidade abandonada) | "TEMPORARY" (entre aspas: a palavra do anúncio da rádio) |

Verdade do texto (`../FATOS.md`): 67 h = AZ-5 01:23:40 de 26/04 → TASS 21:00 de 28/04 (67 h 36 min, arredondado para baixo); Forsmark: o sapato emprestado de um colega foi ao detector (F26); a evacuação foi anunciada como "temporária" (rádio de Pripyat, 27/04).

## Créditos das fotos (licença conferida na página do arquivo, 21/11/2026)
| thumb | arquivo no Commons | autor | licença | data da foto |
|---|---|---|---|---|
| A | [File:Pripyat School (38365893852).jpg](https://commons.wikimedia.org/wiki/File:Pripyat_School_(38365893852).jpg) | Jorge Franganillo | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0) | 04/11/2017 |
| B | [File:Dosimeter measuring radiation in the Chernobyl Exclusion Zone.jpg](https://commons.wikimedia.org/wiki/File:Dosimeter_measuring_radiation_in_the_Chernobyl_Exclusion_Zone.jpg) | Jennifer Boyer | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0) | 14/06/2011 |
| C | [File:Ferris Wheel at Pripyat Ghost Town - Chernobyl Exclusion Zone - Northern Ukraine - 03 (27099701655).jpg](https://commons.wikimedia.org/wiki/File:Ferris_Wheel_at_Pripyat_Ghost_Town_-_Chernobyl_Exclusion_Zone_-_Northern_Ukraine_-_03_(27099701655).jpg) | Adam Jones | [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0) | 18/05/2016 |

Modificações (exigência CC): recorte 16:9, dessaturação/contraste/grão/vinheta, texto e selo sobrepostos. As thumbs derivadas da foto CC BY-SA (C) ficam sob CC BY-SA 2.0. Conferido: sem marca d'água, sem Getty/AP/Reuters, nada da série da HBO, sem vítimas/pacientes/corpos.

**Atribuição para a descrição** (bloco "Thumbnail photo:" acrescentado ao fim de `../entrega/pacote/youtube.txt`):
> Thumbnail photo: A: Jorge Franganillo (CC BY 2.0); B: Jennifer Boyer (CC BY 2.0); C: Adam Jones (CC BY-SA 2.0), via Wikimedia Commons; cropped, color-graded, text added.

## Processo
- Busca no Commons (API) → 22 candidatas em `fontes/` (`fontes/meta.json`: autor, licença, página); contatos em `contato.jpg` e `contato2.jpg`. Downloads pelo `thumb.php` em tamanho padrão (o original direto deu 429 no upload.wikimedia).
- Composição: `compose.py` (PIL; texto e selo no código). Reproduzir: `tools/.venv/bin/python canais/lugares-guerra-en/videos/006-chernobyl/thumbs-reais/compose.py`.
- Prancha 320×180 / 160×90 no meio de 15 thumbs do tema: `prancha.jpg`.
- Crivo independente: `crivo-r1.md` (A e C APROVADOS; B REPROVADO: reator cinza com guindaste repetia a thumb mais vista do tema e tinha 2 focos → B refeita com o dosímetro; selo "RESTRICTED" acrescentado nas 3), `crivo-r2.md`.
- Custo: **US$ 0** (fotos CC do Commons, composição local).
