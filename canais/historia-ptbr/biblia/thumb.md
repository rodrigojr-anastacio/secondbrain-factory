# Thumbnail: historia-ptbr

Regra de canal: **prevalece** sobre `conhecimento/thumbnails/README.md` (regras gerais e o procedimento de arquivar a thumb no ar). As thumbs publicadas ficam na galeria `conhecimento/thumbnails/historia-ptbr-*.jpg`.

## PADRÃO DE ENTREGA a partir do 005 (decisão do Rodrigo, 06/11/2026)
Todo vídeo novo do historia-ptbr entrega **3 thumbs, uma em cada estilo**, para o "Testar e comparar" (modelo: `videos/004-china/entrega/thumbs-v2/` e `compose_v2.py`; detalhes de cada estilo na seção "Teste de 3 estilos" abaixo):
1. **Bonecos:** bonequinho(s) de cabeça redonda grande(s) com emoção forte + objeto/cena-chave do hook, 1–2 palavras (pergunta ou conflito) + datas em pílula. O conflito cara a cara (COROA × TURBANTE) é uma das formas válidas deste estilo.
2. **Pegada History in Minutes:** panorama claro com 4–6 marcos + nosso bonequinho grande em pé à esquerda com contorno de adesivo + NOME do país em serifa preta gigante e "ANO – 2026" no céu livre.
3. **Terceiro estilo, diferente dos dois:** o que tiver mais chance de CTR para o tema (no 004: close dramático e escuro do mistério do vídeo, "NUNCA ABERTO"). Justifique a escolha em 2 linhas no `LEIA.md` das thumbs.
Arquivos: `entrega/thumb-1-bonecos.jpg`, `thumb-2-him.jpg`, `thumb-3-<estilo>.jpg` + `LEIA.md`. Continua **Hipótese** até o CTR: quando o Rodrigo trouxer os números do Studio, registre o estilo vencedor aqui e ajuste o padrão.

## Estado em 04/11/2026: o padrão atual NÃO está funcionando
- **CTR do Egito e da Índia abaixo de 2%** (Rodrigo, `~/workspace/referencias/BRIEF-historia-003-v2.md`, 04/11/2026; janela não informada). Os dois seguem o mesmo padrão (lugar panorâmico + nome gigante + datas). "O padrão precisa mudar."
- Nenhuma das 3 thumbs do 003 v1 "gera curiosidade de clique" (mesma fonte).
- Em teste: 4 conceitos novos no job `historia-003-v2` (`videos/003-ira/v2-amostras/thumbs/`). **Aprovado em 05/11: o conflito cara a cara (abaixo).**

## Padrão novo aprovado em 05/11/2026: CONFLITO CARA A CARA ("COROA × TURBANTE")
O Rodrigo gostou da pegada da thumb-3 da fase 1 (`videos/003-ira/v2-amostras/thumbs/thumb-3.jpg`). Template (003 v2, `videos/003-ira/v2-thumbs/compose_v2.py`):
- **Dois bonequinhos de cabeça redonda, grandes (do peito para cima), testa contra testa, com emoção forte (raiva, boca aberta gritando)**, um de cada lado; os dois no mesmo traço (no 1º teste o clérigo saía semi-realista).
- **Raio amarelo** entre os rostos; fundo dividido (o mundo de cada lado: azulejos × multidão, penhasco × escudos romanos, poços de petróleo × tanques).
- **Datas em pílula amarela** (Open Sans 800) no topo, ao centro: a lacuna ("1891 · 1979", "260 d.C.", "1953").
- **Duas palavras grandes embaixo** em Libre Caslon 700 sobre degradê escuro: a 1ª em ouro (#F7C21B), "×" branco, a 2ª em branco. O título dá o "história INTEIRA"; a thumb vende o conflito.
- Base: nano-banana-2.1/edit + refs do canal, 2 tomadas por conceito (US$ 0,046 cada), texto composto em PIL (fontes em `videos/003-ira/v2-amostras/thumbs/base/fonts/`).
- Irã v2: 1 COROA × TURBANTE (principal), 2 PÉRSIA × ROMA (Shapur × Valeriano), 3 PETRÓLEO × CIA (Mossadegh × agente). **Hipótese** até o CTR do "Testar e comparar": registre aqui o vencedor e o CTR de cada uma.
- Para o próximo país, escolha 3 pares de conflito do próprio roteiro (personagem × personagem, ou povo × povo).
- China 004 (05/11/2026): 1 **IMPERADOR × MORTE** "210 a.C." (Qin com as pílulas × a morte encapuzada, exército de barro × rios de mercúrio; principal, casa com o hook), 2 **DRAGÃO × CANHONEIRA** "1839" (oficial Qing × capitão britânico com o baú de ópio), 3 **IMPERADOR × MONGOL** "1279". As 6 bases saíram boas na 1ª tomada (US$ 0,046 cada); palavra longa (CANHONEIRA) cabe com a fonte a 86 px, legível a 320 px. **Hipótese** até o "Testar e comparar".

## Teste de 3 estilos fora do COROA × TURBANTE (004 China, 06/11/2026): **Hipótese**, medir CTR
Pedido do Rodrigo: 3 estilos diferentes para o "Testar e comparar" (`videos/004-china/entrega/thumbs-v2/`, código `thumbs-v2/compose_v2.py`, US$ 0,37):
- **4 Bonecos, emoção + objeto-chave:** 1 bonequinho grande (do peito para cima) com medo, segurando o objeto do hook brilhando (pílula de mercúrio), e o exército de barro encarando; 1 palavra-pergunta em ouro ("IMORTAL?") no canto livre + datas em pílula. Nano-banana desenhou "pill" como **cápsula moderna**; pedir "round spherical silver ball… NOT a capsule" (sai uma esfera grande, tipo bola de cristal).
- **5 Pegada HiM:** padrão do canal-modelo (8 thumbs baixadas em 06/11/2026; Índia 618 mil, Egito 468 mil, Ucrânia 178 mil): ilustração diurna clara, panorama aéreo com 4–6 marcos do país, **pessoa grande em pé à esquerda com contorno de adesivo** (nas 3 mais vistas), céu livre no canto superior direito com **NOME em serifa preta gigante + "ANO – 2026" em sans preta**, selo pequeno ao lado do nome, sem degradê escuro nem emoção. A nossa usa o bonequinho Qin no lugar da pessoa e não usa o selo deles. Lembrete: o Egito 001 copiou só o panorama (sem pessoa) e teve CTR < 2%.
- **6 Close dramático do mistério:** cena escura, porta de bronze do túmulo fechado com mercúrio prateado vazando, arqueólogo bonequinho recuando com tocha; "NUNCA ABERTO" (ouro + branco) + "2.200 ANOS". Escolhido por pagar o loop do vídeo ("ninguém abriu até hoje") e ser lacuna de informação pura; o escuro destoa do feed claro dos concorrentes. Estátuas de terracota saem com rosto semi-realista (são estátuas, aceitável, mas pequenas e na sombra).
- **Registre aqui o vencedor e o CTR das 6 thumbs da China** (1–3 COROA × TURBANTE e 4–6) quando o Rodrigo ler no Studio.

## Irã v3 (07/11/2026): HiM fiel ao print + TRAPAÇA? + mapa. **Hipótese**, medir CTR
`videos/003-ira/entrega/thumbs-v3/` (US$ 0,28; 6 bases nano-banana-2.1/edit, todas usáveis na 1ª tomada, 0 molduras):
- **HiM fiel ao print (sem boneco):** a Praça Naqsh-e Jahan saiu ótima (cúpula azul, minaretes, Ali Qapu, espelho d'água), mas mesmo pedindo "upper right 45% plain sky" o céu veio com só ~30% da altura. Solução no código: empurrar a cena ~110 px para baixo e completar o topo com o degradê do céu (esticar a faixa de céu deixa emenda nos minaretes/cúpula). Ano inicial = o mais antigo que o roteiro cobre (4200 a.C., Susa).
- **Bonecos com a cena do hook:** Dario piscando + cavalo relinchando com linhas de som + nobres apontando + cavalariço com a égua e o dedo na boca: o nano-banana montou a cena inteira certo nas 2 tomadas. Palavra-pergunta de acusação ("TRAPAÇA?") em vez de conflito ×.
- **Mapa-império aceso em ouro** (3º estilo): a geografia sai aproximada (aceitável em cartoon) e sem letras quando o prompt diz "no country names, no labels". Rei grande de braços abertos sobre o mapa lê bem a 320 px.

## Brasil 005 (07/11/2026): 1º vídeo no padrão de entrega. **Hipótese**, medir CTR
`videos/005-brasil/entrega/` (US$ 0,28; 6 bases, 1 descartada por faixa/moldura lateral): 1 **bonecos** "À VENDA?" + "1511" (o escrivão da Bretoa em choque com a lista de carga, toras vermelhas, papagaio, sagui); 2 **HiM** "BRASIL" + "1500 – 2026" (baía do Rio, Ouro Preto, Amazônia, Brasília + bonequinho Pedro I com espada e contorno de adesivo; o céu livre saiu certo na 1ª tomada, sem o `mais_ceu`); 3 **ação cômica/lacuna** "O REI FUGIU!" + "1807" (D. João correndo para o navio com a coroa, Napoleão no morro, tempestade). Ano da HiM = o ano-símbolo do país (1500), não o mais antigo do roteiro. Código `videos/005-brasil/thumbs/compose.py`.

## O que manter (vale até haver dado contra)
## Roma 006 (09/11/2026). **Hipótese**, medir CTR
`videos/006-roma/entrega/` (US$ 0,28; 6 bases, as 6 usáveis; 1 com emenda lateral descartada): 1 **bonecos** "ROMA HUMILHADA" + "390 a.C." (Breno rindo com a espada na balança de ouro, senador em desespero); 2 **HiM** "ROMA" + "753 a.C. – 476" (Coliseu, Fórum, Panteão, aqueduto + general de louros com contorno de adesivo); 3 **queda** "ROMA CAIU!" + "410" (Alarico com a águia, Roma em chamas, senador pagando resgate). Código `videos/006-roma/thumbs/compose.py`.

## Rússia 007 (09/11/2026). **Hipótese**, medir CTR
`videos/007-russia/entrega/` (US$ 0,37; 8 bases): 1 **bonecos** "UM VIKING / NO TRONO?" + "862" (o príncipe viking rindo com a coroa oferecida pelo ancião eslavo nervoso, aldeões brigando atrás); 2 **HiM** "RÚSSIA" + "862 – 2026" (inverno claro: São Basílio, Kremlin, Palácio de Inverno, trem na neve + Pedro, o Grande, com contorno de adesivo); 3 **mito** "O INVERNO / VENCEU?" + "1812" (Napoleão congelando, General Inverno de neve soprando, Moscou em chamas). As 2 tomadas do 3º saíram com **emenda de painel** no terço direito (o pedido "RIGHT 38% darker and simpler" virou outro quadro): pedir "ONE single continuous scene… no split panels, no divider line: on the RIGHT side the same plain simply continues". Código `videos/007-russia/thumbs/compose.py`.

- Texto **sempre composto no código** (`src/Thumbnail.jsx`), nunca escrito pela IA. Hoje: Libre Caslon 700 + Open Sans 800. [BRIEF.md 001; QA.md 001]
- No máximo 2–3 palavras na arte, legíveis em 320×180; o resto vai no título. [estilo.md antigo]
- Base em qualidade alta (`high` no gpt-image-2) e **3 variações** para o "Testar e comparar".
- Direção do Rodrigo (até o 002): inspirada na referência, mas com **identidade nossa**: personagem-guia (o bonequinho do canal) reagindo ao lugar/época; assinatura de tempo (selo com o período, sempre no mesmo canto e na mesma cor); cor de destaque fixa do canal (amarelo-ouro ou laranja). [estilo.md antigo]
- **Hipótese (04/11):** falta curiosidade (lacuna de informação, conflito, rosto com emoção). Panorama bonito + nome do país não cria pergunta.

## Thumbs no ar (análise movida de `conhecimento/thumbnails/README.md`, 2026-11-04)
### historia-ptbr-001-egito.jpg
- Vídeo: "A história INTEIRA do Egito em 17 minutos" · `g847Td0Plsk` · `youtube.videos` id 3. Origem: `videos/001-egito/out/thumbnail.jpg` (v2, base `high`); SSIM 0,996 com a pública (2026-11-04).
- Tem: panorama do Nilo com pirâmides, Esfinge, templos e barcos à esquerda; céu e deserto livres à direita; "EGITO" em serifa preta enorme e "5000 a.C. – 2026" em sans negrito. É a fórmula da referência VQPzrVMHWlg (417 mil views).
- Não tem a "identidade nossa" (personagem-guia, cor de destaque). **CTR < 2%** (Rodrigo, 04/11). Views: 6 em 2026-11-04.
### historia-ptbr-002-india.jpg
- Vídeo: "A HISTÓRIA COMPLETA da Índia em 19 minutos" · `MV5SSjoccqE` · id 4. Origem: `videos/002-india/thumb-var/final/E-gandhi.jpg`; SSIM 0,984 com a pública. A thumb do pacote (`out/thumbnail.jpg`, panorama) **não** é a que está no ar.
- Tem: "pop-out" com Gandhi em cartoon, grande, à esquerda, saindo de uma moldura com o Taj Mahal ao pôr do sol; fundo laranja-açafrão; "ÍNDIA" em serifa branca com contorno e "3300 a.C. – 2026" em amarelo. fal.ai (`thumb-variacoes.json`; `financas.consumo` ids 19–20, US$ 0,13). Existe a variação `D-imperador.jpg`.
- O traço do Gandhi é diferente dos bonequinhos de cabeça redonda. **CTR < 2%** (Rodrigo, 04/11). Views: 17 em 2026-11-04. Sem registro de "Testar e comparar" D × E.

## Não faça
- Layout "pôster de expediente" (personagem à esquerda + SIGLA gigante + sello rojo + aba de pasta): é do `dossie-es`.
- Pintura a óleo romântica com pergunta: é do `lotr-fr`.
- Texto pequeno em várias linhas.

## Políticas do YouTube (14/11/2026, `conhecimento/politicas-youtube.md`)
Thumb sem foto real de morto, sem sangue/ferimento/caveira e sem as palavras proibidas no texto. Em IA: bonequinhos sem sangue, ferimento ou cadáver; guerra sugerida por objeto, bandeira, silhueta.

## Reembalagem 14/11/2026 (teste aprovado pelo Rodrigo): 1 foco + lacuna, sem nome de país. **Hipótese (teste aprovado 14/11/2026)**, medir CTR
7 thumbs novas (`videos/NNN/reembalagem-2026-11-14/thumb-nova.jpg`; código `pesquisa/reembalagem-2026-11-14/thumbs/compose.py`; conceitos e referências em `pesquisa/reembalagem-2026-11-14/PROPOSTAS.md`): 2 a 3 palavras-pergunta em Libre Caslon (1ª em ouro) sobre degradê escuro, no máximo 1 pílula de data, **1 foco por lado e sem panorama**: Egito (Cleópatra grande + pirâmide lisa "JÁ ERA ANTIGA"), Índia (duelo "CHUVA × CANHÃO"), Irã ("MESMO PAÍS?"), China ("IMORTAL?"), Brasil (diagonal "NADA MUDOU?", 1511 × 2026), Roma (senador chorando "DE NOVO?"), Rússia (só o mapa aceso, sem personagem, "TUDO ISSO?": desvio pequeno da bíblia, vale o 3º estilo "mapa-império aceso"). Aprendizado de ferramenta: nano-banana-2.1/edit acerta personagem + cenário com pedido de "RIGHT x% simple/dark"; para o Brasil, 2 bases separadas (1511 e 2026) e a diagonal no código (reposicione cada base na tela antes de cortar).
