# RELATÓRIO · historia-ptbr/005 · "A história INTEIRA do Brasil em 17 minutos" (youtube.videos id 12)

Job: `~/workspace/referencias/BRIEF-historia-005-brasil.md` (07/11/2026). Executor: Claude Code (Opus), uma sessão `claude -p`. Nada publicado nem enviado ao Telegram. **Entregue no Drive** em `Youtube/História em minutos/005-brasil/`.

## Entrega (`entrega/`)
- `video.mp4`: **17:22**, 1080p30, −15,2 LUFS, 0 telas pretas. **Hook de 1:23.**
- `legendas.srt`; 3 thumbs no padrão do 005 (`thumb-1-bonecos.jpg`, `thumb-2-him.jpg`, `thumb-3-fuga.jpg`) + `LEIA.md`; `pacote.md` (título, descrição, 12 capítulos, fontes, tags, checklist).

## Decisões
1. **Referências** (`ref/`): o próprio History in Minutes acabou de publicar "The Entire History of Brazil in 14 Minutes" (`Vug2cLY3nxk`), transcrito; e o pt mais visto no formato narrativo, Fatos Desconhecidos (`DGhYlhftqW8`, 408 mil, 19:38), que é lista de livro didático. O HiM usa a piada do "país do futuro" como fio, mas ela não liga as eras e os povos originários ganham 2 frases. Nós: fio que causa cada era e uma era inteira antes de Cabral.
2. **Hook = a lista de carga da nau Bretoa (1511)**: cinco mil toras de pau-brasil, papagaios, saguis, macacos e dezenas de indígenas escravizados, numa das primeiras menções escritas ao nome Brasil → "Essa é a história inteira do Brasil: como a terra que nasceu numa lista de carga virou um país de mais de duzentos milhões de pessoas" → promessa → "o que vai no navio… e o que fica aqui? Guarde essa lista de carga". **Pago no fecho**: hoje os navios levam soja, minério e petróleo; "brasileiro" deixou de ser o nome de um ofício (quem carregava a madeira) e virou o nome de 213 milhões de pessoas; pergunta: "qual ciclo deixou mais marcas na sua cidade?".
3. **Fio condutor: "o que vai no navio e o que fica aqui"** — escolhido porque é a forma concreta (e narrável) da "riqueza que sai em ciclos" sugerida no brief, e porque gera causa → consequência sozinho: cada carga traz o problema da era seguinte (açúcar → escravidão; ouro → Inglaterra e Inconfidência; 1808 é o navio "no sentido contrário"; café → imigrantes e 1929; "o petróleo é nosso"; a dívida de Brasília e da ditadura; soja e açúcar de novo).
4. **Tamanho:** 2.190 palavras → 1.042,8 s. Título com N = 17.
5. **Voz:** drama-3, 1 chamada por bloco, cobrança conferida no crédito (US$ 0,178 = bytes × US$ 10/M). Whisper fonético: mín 95,3%, média 99,8%. Hook: repetição melódica 0,11 nos 60 s (após reescrever e escolher entre 5 tomadas por bloco).
6. **Imagens:** 221 nano-banana-2.1/edit + refs; lote-prova de 6 aprovado; 13 refeitas por bandeiras anacrônicas e letras inventadas (ver `QA.md`).
7. **Trilha:** a mesma síntese do 004, trocada para o **modo mixolídio de Sol** (o modo da música nordestina), timbre de cordas dedilhadas.
8. **Thumbs:** 1 bonecos "À VENDA?" (o escrivão da Bretoa), 2 HiM "BRASIL 1500 – 2026" (panorama + Pedro I com contorno de adesivo), 3 "O REI FUGIU!" (D. João, 1807). Justificativa no `entrega/LEIA.md`.

## Correções de fatos (checagem antes da voz, `SOURCES.md`)
1. Carga da Bretoa: as fontes divergem (5.008 toras/36 cativos × "cinco mil toros"/"quarenta peças") → "cinco mil toras" e "dezenas de pessoas, a maioria mulheres".
2. "O primeiro documento com o nome Brasil" → "**uma das primeiras vezes** que o nome aparece".
3. "Brasileiro era nome de profissão" → "**diz a explicação mais aceita**" (origem tradicional, contestada por linguistas).
4. "Não corram tanto, vão pensar que estamos fugindo" (D. Maria I) e o conselho de D. João a Pedro: sem fonte primária → "**Conta-se**" / "**Diz a tradição**".
5. Plano Collor: "congelou a poupança de todo mundo" → "congelou o dinheiro das contas e da poupança por dezoito meses".
6. Café c. 1900: "mais da metade do café do mundo" (as estimativas vão de 70 a 80%).
7. Mula e dor de barriga no Ipiranga: "**Pelos relatos**" (padre Belchior e Marcondes; detalhes variam).

## Custo direto (financas.consumo, ref_id 12)
| Etapa | US$ |
|---|---|
| Voz drama-3 (teste de nomes, 5 tomadas do hook, vídeo inteiro) | 0,18 |
| Lote-prova (6) | 0,28 |
| Lote inteiro (216, em 3 partes) | 9,91 |
| Refeitas (13) | 0,60 |
| Bases das thumbs (6) | 0,28 |
| **Total** | **US$ 11,24** (teto US$ 14) |
Saldo depois: fal US$ 43,15; Fish US$ 47,74.

## Ferramentas mudadas (só na pasta do vídeo)
- `tools/build.py`: trilha mixolídia; corrige o tamanho da trilha quando `int(dur*SR)` difere do áudio em 1 amostra (quebrava o build). `src/Video.jsx`/`index.jsx`/`render_partes.sh`: composição `Brasil`. `src/labels.jsx`: rótulos dos 12 mapas. Nenhuma tool de `tools/` da fábrica foi alterada.

## Para o Rodrigo
- **Ouvir os nomes** (timestamps conferidos na `legendas.srt`): Bretoa **0:02**, Marajó **1:34**, "…até Ipanema" **2:07**, Pero Vaz de Caminha **2:35**, Nassau **5:06**, Zumbi **5:45**, Tiradentes **7:02**, Ipiranga **8:53**, Graham Bell **10:50**, Fordlândia **12:54**, Juscelino Kubitschek **14:15**.
- Teste do hook: retenção aos 30 s e 60 s no Studio (hook de 1:23, anedota da Bretoa; comparar com Irã 1:31 e China 1:16).
- Publicar é decisão sua; checklist no `pacote.md`.
