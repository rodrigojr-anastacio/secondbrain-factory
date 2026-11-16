# Storyboard: Em Relevo 004 (1983, El Niño: enchente no Sul × seca no sertão)

Etapa 1 (13/11/2026). Fonte: `shared/storyboard.py` → `shared/storyboard.json`, `shared/cenas.json` e a tabela completa em `work/storyboard-tabela.md` (fora do git; regenere com `python3 shared/storyboard.py`). Duração estimada **~10:35** (A 263 s · B 333 s · arquivo 38 s); 15 fotos/imagens distintas; **zero imagem de IA**.

## Linguagem visual (mesma do longo-03, visual v2/LongoV3)
- **A = satélite** (Blue Marble + relevo ETOPO) para lugar e impacto; **B = relevo editorial** para dado e rótulo; **arquivo** = papel sépia com tipografia (sem foto de época: não existe foto livre de 1983).
- Ritmo 2–4 s por evento visual; cada mídia tem `gatilho` = palavra falada onde entra (o build_cues da etapa 2 amarra ao Whisper).
- Legenda na tela só com LUGAR · O QUE · ANO. **Foto de outro ano sempre com o ano real**; nunca escrever 1983 em foto que não é de 1983. Créditos só na descrição.

## Peças novas (em ordem de prioridade; se faltar tempo, simplifique de baixo para cima)
1. **Tela partida do Brasil** (b05, b17, b31, b40, thumb A): diagonal Sul azul-água × sertão coral, um relógio "1983" no meio. É a assinatura do vídeo.
2. **Régua de nível cravada no rio** (b01, b02, b39): régua vertical 3D com a água subindo (dados reais de `dados/iguacu-uv-1982-83.json`) e um plano de água que cobre a várzea de União da Vitória no nível de 10,42 m (b01, b12). Simplificação: régua 2D ao lado do mapa.
3. **Hidrograma em relevo** (b09–b11, b29): a série diária vira uma serra de água azul que cresce; em b29, a onda RONI coral sobreposta na mesma linha do tempo (o Pacífico desce enquanto o rio sobe). Simplificação: gráfico de linha do componente "régua de montanhas".
4. **Antes × depois Landsat 1983** (b13): cortina entre `landsat4-uv-19830703-par.jpg` e `landsat4-uv-19830804-par.jpg` (mesma janela). Tratar cores para ficarem comparáveis (água azul, vegetação verde-escura); em 04/08 há nuvem sobre a cidade: enquadrar a várzea a sudeste (canto inferior direito), que aparece larga e clara.
5. **Anéis de meses** (b07, b27, b30, b36): anel de 12 meses (componente do longo-03) e um anel de 24 meses (ano 1 + ano 2) para o "guarde isso".
6. **Fita do jato subtropical** (b28): fita de vento em altitude, frentes presas sob ela, "H" de bloqueio. Simplificação: setas.
7. Régua de montanhas de Mombaça (b18) e RONI (b25): componente existente.

## Mapa de mídias por bloco (resumo; detalhe em `shared/storyboard.json`)
| Bloco | Mídia | Legenda na tela |
|---|---|---|
| b01 | landsat4-uv-19830703-par.jpg (2 s antes do 3D) | UNIÃO DA VITÓRIA · LANDSAT 4 · 3 JUL 1983 |
| b02 | blumenau-aerea-2010.jpg | BLUMENAU · CENTRO E RIO ITAJAÍ-AÇU · 2010 |
| b03 | acude-seco-santa-quiteria-ce-2018.jpg | AÇUDE SECO · SANTA QUITÉRIA (CE) · 2018 |
| b04 | retirantes-pernambuco-slide-janjao-sem-data.jpg | RETIRANTES · PERNAMBUCO · FOTO DE ACERVO (SEM DATA) |
| b08 | uniao-da-vitoria-vista-aerea-2009.jpg | UNIÃO DA VITÓRIA · RIO IGUAÇU · 2009 |
| b12 | porto-uniao-centro-2014.jpg | PONTE SOBRE O IGUAÇU · UNIÃO DA VITÓRIA E PORTO UNIÃO · 2014 |
| b13 | landsat 03/07 → 04/08/1983 | 3 JUL 1983 · RIO 4,94 M → 4 AGO 1983 · RIO 7,42 M |
| b14 | blumenau-rio-itajai-acu-2006.jpg | BLUMENAU · RIO ITAJAÍ-AÇU EM ESTIAGEM · 2006 |
| b16 | (opcional) blumenau-enchente-2008-exercito-NAO-1983.jpg | BLUMENAU · ENCHENTE DE 2008 |
| b19 | acude-coremas-seco-2017.jpg | AÇUDE DE COREMAS (PB) · SECA · 2017 |
| b20 | sertao-caatinga-arido-2013.jpg | SERTÃO · CAATINGA NA ESTIAGEM · 2013 |
| b25 | elnino-1982-83-anomalia-temp-pacifico-jan1983.jpg | PACÍFICO · JAN 1983 |
| b28 | noaa-cpc-elnino-impactos-globais-jun-ago.jpg | NOAA · IMPACTOS DO EL NIÑO · JUN–AGO |
| b32 | uniao-da-vitoria-rio-iguacu-helicoptero-2016.jpg | UNIÃO DA VITÓRIA · RIO IGUAÇU · 2016 |
| b38 | sobradinho-represa-seca-2015.jpg | SOBRADINHO (BA) · RESERVATÓRIO BAIXO · 2015 |

Licenças, autores e páginas: `pesquisa/FOTOS.md` / `pesquisa/fotos.json`. Atenção: `retirantes-pernambuco-…` (Centro de Memória Unicamp) — conferir o texto exato da licença na página antes de publicar (FOTOS.md registra CC BY-SA 4.0 com template de domínio público GLAM); `blumenau-centro-rio-itajai-acu-2012.jpg` e `blumenau-ponte-de-ferro-2012.jpg` (marca d'água) **não** foram usadas.

## Sensibilidade
- Nenhuma foto de vítima. A seca é contada com dado, mapa e tipografia; o único rosto é o slide de retirantes sem data (b04), em quadro médio, sem zoom em pessoa.
- b22 não mostra número de mortos (não há número confiável).
- Fotos de enchente de outros anos só como opcional e com o ano na legenda (b16).
