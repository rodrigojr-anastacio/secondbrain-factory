# QA · historia-ptbr/005 · Brasil (07/11/2026)

## Render (`tools/qa.sh`)
- `out/video.mp4` = `entrega/video.mp4`: **17:22,8** (1042,8 s), 1920×1080, 30 fps, h264 + AAC 48 kHz estéreo, 512 MB.
- Áudio: **−15,2 LUFS**, LRA 3,7, pico −4,3 dBFS. 0 silêncios > 1,5 s. **0 telas pretas.**
- Cortes no 1º minuto: 19 pela detecção de cena (> 0,3) e 21 planos na timeline (crossfades suaves não contam); 349 planos, média 2,99 s (20,1/min).
- Render em 5 partes (`tools/render_partes.sh`, cada < 9 min, espera ancorada em `^node .*remotion`). A última parte parou no quadro 31.283 de 31.286 (2 quadros da cauda de silêncio; sem efeito).
- Contact sheet (`out/contact-sheet.jpg`) e stills de mapas/cartões/placa (`qa/stills/prancha.jpg`) conferidos.

## Voz
- Fish **drama-3**, clone do Rodrigo, 1 chamada por bloco, 101 blocos. **Cobrança confirmada**: crédito 47,91668 → 47,73857 = US$ 0,17811 = 17.811 bytes × US$ 10/M (no s2.1-pro seriam US$ 0,27).
- Whisper por bloco (`tools/qa_voz_blocos.py` + `qa_fonetico.py`): **mín 95,3%, média 99,8%**, 0 blocos abaixo de 95%, 0 tags faladas. As diferenças do Whisper bruto são grafia ("Álvaro Escabral", "tira dentes", "naubretoa").
- Hook (0:00–1:23): 60 s iniciais com **repetição melódica 0,11** (hook inteiro 0,12). A 1ª tomada deu 0,15–0,16; reescrevi o texto (pergunta "O que tem lá dentro?", "E sabe onde ele aparece?", menos frases-lista) e gerei 5 tomadas por bloco, escolhendo a combinação de menor repetição (US$ 0,04 a mais). Ver `qa/hook/`.
- Teste de nomes antes do vídeo inteiro: Bretoa, Marajó, Ipanema, Caminha, Nassau, PR, Graham Bell, Fordlândia, Kubitschek. "Ipanema" sumia colado em "jacaré" ("jacaré e panema") → texto mudou para "mandioca, jacaré, pipoca… até Ipanema".

## Imagens
- 221 imagens nano-banana-2.1/edit + 3 refs do canal (US$ 0,0459/img). Lote-prova de 6 (aldeia tupi, chegada de africanos escravizados, mapa de Tordesilhas, D. João no Rio, engenho, D. Maria na carruagem) aprovado; só o prompt dos tupis mudou (tiras de penas "de filme" → cabelo em cuia, pintura corporal e colares, "no feather headbands").
- Pranchas `qa/prancha-1..8.jpg`: 0 pretas, 0 molduras (detector de bordas + olho), mapas sem letras.
- **13 refeitas** (`imagens-descartadas/`): bandeira francesa tricolor em 1555–1567 (I074, I075, I077), bandeira republicana do Brasil em 1870 e 1888 (I155, I161), bandeiras em palanque (I200), placas com letras inventadas ("Lisboa" I118, "BANK" I210, "ORANGE JUICE" I219, letreiros I170, ideogramas falsos I175), padaria medieval em 1993 (I212), reis medievais em volta da moeda do real (I214). Todas certas na 2ª tomada.
- Representação: indígenas e africanos com o mesmo bonequinho de cabeça redonda do canal, roupas e contexto de época, cenas de dor sem violência explícita; nenhum estereótipo de cocar nas cenas tupis refeitas (os povos diversos de I035 usam cocares, que são adorno real de vários povos).

## Roteiro × bíblia
- Hook 1:23 (≤ 90 s) com pergunta central e promessa; 10 eras com título-frase só na placa; fecho paga a lista de carga e faz pergunta.
- Teste da troca: cada era nasce da anterior (pau-brasil não basta → açúcar → escravidão → holandeses levam o açúcar → precisa de ouro → ouro some/Napoleão → Corte → Independência → café/abolição → República do café → 1929 → Vargas → JK/dívida → 1964 → inflação → real → hoje).
- Fio condutor "o que vai no navio e o que fica" dito em voz alta no hook, era 2, era 5 ("o navio veio no sentido contrário"), era 9 ("o petróleo é nosso"), era 10 e fecho. Todos os "guarde" pagos.
- Recorte político atual: 1 frase neutra ("presidentes de esquerda, de centro e de direita, e dois impeachments. E a democracia seguiu de pé.").
- 2.190 palavras → 17:22 (a estimativa do `roteiro.py` deu 17:33; ver aprendizado na bíblia).
