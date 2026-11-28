# Backlog v3 (proposta, 28/11/2026): historia-ptbr "como era viver"

> **Aguarda aprovação do Rodrigo. NÃO carregado em `youtube.backlog`** de propósito: o status pedido ("vivo") não existe no banco (só `proposto/agendado/...`) e todo item `proposto` do historia-ptbr é **agendado automaticamente** pelo `backlog.py agendar` (rotina `tudo`, seg/qui, e o planejar da noturna), porque o `historia-ptbr` continua em `CANAIS=` do `~/.config/fabrica/noturna.env`. Carregar agora poria temas v3 na produção noturna antes da aprovação. Quando ele aprovar: `tools/.venv/bin/python tools/rotinas/backlog.py importar canais/historia-ptbr/v3-proposta/temas-candidatos.json --canal historia-ptbr --fonte "historia v3 proposta 28/11"` (só os 12 abaixo; os 4 de reserva ficam fora) ou `add` um a um.

Fontes e método: `v3-proposta/PT-TITULOS-DEMANDA.md` (846 vídeos pt de 12 meses, coleta 28/11/2026, Data API) e `v3-proposta/TEMAS-CANDIDATOS.md` (manada, ângulo e evidências de cada tema; `temas-candidatos.json` estruturado). Notas 1–10: D = demanda, E = encaixe (bonequinhos, 2ª pessoa, Brasil, políticas), U = urgência; nota = (D×E×U)^(1/3).

## Os 4 do teste (ordem de produção, 1 por semana, nunca dois colados)

| # | tema | título candidato | thumb | evidência principal | D/E/U | nota |
|---|---|---|---|---|---|---|
| 1 | Rio de Janeiro, 1808: a corte chega e confisca as casas ("PR" na porta) | Rio, 1808: Pintaram "PR" na Sua Porta e a Corte Ficou com a Sua Casa | Bonequinho carioca de pijama na calçada com a trouxa, porta da casa com "P.R." pintado em vermelho, nobre de peruca entrando com malas. Texto: "PONHA-SE NA RUA". | [YouTube (videos.list 28/11/2026): 790.439 views, canal de 109 mil inscritos, 03/2026](https://youtu.be/qWPL11MOzOg) | 9/10/5 | 7.7 |
| 2 | Um dia inteiro como camponês (servo) na Idade Média, 1300 | Você Acordou Camponês em 1300: 24 Horas e Metade do Pão É do Senhor | Bonequinho com foice e cara de sono, senhor feudal gordo arrancando metade do pão da mão dele, moinho ao fundo. Texto: "METADE É DELE". | [YouTube: 801.270 views (castelo, mesmo público), 04/2026](https://youtu.be/2dqGsuQrxeM) | 9/9/3 | 6.2 |
| 3 | Inverno de 1944–45: pracinha brasileiro na neve dos Apeninos | Inverno de 1944: Você é um Pracinha Brasileiro na Neve da Itália | Bonequinho de capacete da FEB tremendo, enterrado até os joelhos na neve, com uma xícara de café que congelou. Seta "VOCÊ". Texto: "−20 °C". | [YouTube: 643.946 views, canal de 10,4 mil inscritos, cartoon "VOCÊ" (08/2025)](https://youtu.be/Xt67z9COves) | 9/9/7 | 8.3 |
| 4 | Brasil pré-histórico: humanos contra a megafauna (preguiça gigante, tigre-dentes-de-sabre) | Brasil, 12.000 Anos Atrás: Você Contra uma Preguiça de 4 Toneladas | Bonequinho minúsculo com lança de pedra olhando para cima, preguiça-gigante em pé (6 m) na frente, Lagoa Santa ao fundo. Texto: "VOCÊ x 4 TONELADAS". | [YouTube (en): 13.609.510 views, Fossil, "How Long You'd Last in Every Prehistoric Era" (08/2026)](https://youtu.be/nAWpLtG-kNs) | 9/10/4 | 7.1 |

## Os outros 8 (fila depois do teste, pela nota)

| # | tema | título candidato | thumb | evidência principal | D/E/U | nota |
|---|---|---|---|---|---|---|
| 5 | Viagem na frota de Cabral, 1500 (44 dias até o Brasil) | Você Embarcou na Caravela de Cabral: 44 Dias de Biscoito com Bicho Até o Brasil | Bonequinho verde de enjoo agarrado ao mastro, segurando um biscoito com larvas, mar bravo, nau ao fundo. Texto: "44 DIAS". | [YouTube: 333.863 views, 06/2026](https://youtu.be/YKBqL9GUydg) | 8/10/4 | 6.8 |
| 6 | Alistado na legião romana: 25 anos de serviço | Você Foi Alistado na Legião Romana: 25 Anos, 30 km por Dia e Proibido Casar | Bonequinho legionário suado carregando uma mochila gigante num pau (a "mula de Mário"), centurião gritando. Texto: "25 ANOS". | [YouTube (en): 887.433 views, Hypothetically, "What It Was Like to be Every Roman Army Rank" (02/2026)](https://youtu.be/0n5xG4epnY0) | 8/10/3 | 6.2 |
| 7 | Um mês como tropeiro, do Sul a Sorocaba, 1820 | Um Mês Como Tropeiro em 1820: 40 Mulas, Feijão e Lama Até Sorocaba | Bonequinho de chapéu e poncho atolado na lama puxando uma mula que se recusa a andar, caldeirão de feijão tropeiro. Texto: "40 MULAS". | [YouTube: 130.414 views, canal de 11,1 mil inscritos (mediana do canal 2.210), 05/2026](https://youtu.be/fUXPYGQto4A) | 6/10/3 | 5.6 |
| 8 | Corrida do ouro em Minas Gerais, 1700–1730 | Minas, 1720: Você Achou Ouro e Mesmo Assim Passou Fome | Bonequinho magro segurando uma pepita enorme, barriga roncando, vendedor com uma galinha e etiqueta de preço absurdo. Texto: "RICO E COM FOME". | [YouTube (en): 991.421 views, Good Enough, "The Luckiest Men of the Gold Rush" (07/2025)](https://youtu.be/Tz9OteThE6Y) | 7/10/3 | 5.9 |
| 9 | Imigrante italiano no cafezal paulista, 1888–1900 | 1888: Você Trocou a Itália por um Cafezal em São Paulo | Bonequinho de chapéu e mala de papelão no porto de Santos, olhando um cafezal sem fim; fazendeiro com caderneta. Texto: "ITÁLIA → CAFEZAL". | [YouTube: 283.964 views, 05/2026](https://youtu.be/Rq-wtvKcIrE) | 7/9/3 | 5.7 |
| 10 | Sertão de 1930: um vaqueiro no caminho de Lampião | Sertão, 1930: Um Dia de Vaqueiro no Caminho de Lampião | Bonequinho de gibão e chapéu de couro na caatinga seca, olhando para trás; ao longe, o bando de chapéus de meia-lua. Texto: "ELE VEM AÍ". | [YouTube: 1.280.321 views, canal de 2,85 mil inscritos, 11/2026](https://youtu.be/q6Y5GW2qZ9U) | 8/7/6 | 7.0 |
| 11 | A vida a bordo de um navio pirata, 1715 (Era de Ouro) | Você Entrou num Navio Pirata em 1715 e Ganhou Direito a Voto | Bonequinho de tapa-olho levantando a mão numa votação no convés, capitão de chapéu fazendo cara feia. Texto: "PIRATA VOTAVA". | [YouTube (en): 715.461 views, Hypothetically, "What It Was Like to be Every Pirate Rank" (01/2026)](https://youtu.be/S9LXiTUygos) | 8/9/3 | 6.0 |
| 12 | Cinco meses de inverno numa casa comprida viking | Você Passou o Inverno Viking: 5 Meses Trancado com a Família e as Vacas | Bonequinho espremido entre uma vaca e a família ao redor do fogo na casa comprida, neve até o telhado, cara de quem não aguenta mais. Texto: "COM AS VACAS". | [YouTube: 566.207 views, canal de 6,2 mil inscritos (04/2026)](https://youtu.be/_xrAcsfZyE8) | 8/9/4 | 6.6 |

**Amostra do nº 1 (Rio, 1808):** `v3-proposta/amostra-001-rio-1808/` (o título da amostra foi refinado para "Rio, 1808: Escreveram "P.R." na Sua Porta e Você Tinha 24 Horas Para Sair").

## Reservas (fora dos 12)

- **Os piores empregos do Brasil colonial e imperial (tigre, aguadeiro, sangrador, acendedor de lampião)**: Os Piores Empregos do Brasil Colonial (o Nº 1 Carregava Barril de Esgoto na Cabeça) (D/E/U 8/7/3). Fora por encaixe/política ou demanda sem ponte com o Brasil.
- **Seringueiro na Amazônia, 1900 (o ciclo da borracha)**: Amazônia, 1900: Você Virou Seringueiro e a Dívida Só Crescia (D/E/U 6/9/3). Fora por encaixe/política ou demanda sem ponte com o Brasil.
- **Operário da Grande Pirâmide de Gizé, 2560 a.C.**: Você Foi Convocado Para Construir a Pirâmide e o Salário Era Cerveja (D/E/U 8/10/3). Fora por encaixe/política ou demanda sem ponte com o Brasil.
- **A peste chega à sua vila, 1348**: 1348: A Peste Chegou à Sua Vila e o Remédio Era Cheirar Flores (D/E/U 8/7/4). Fora por encaixe/política ou demanda sem ponte com o Brasil.

## Por que esta ordem
- **1 Rio 1808**: Brasil forte, 790 mil no tema, porta aberta (ninguém contou pelo carioca despejado), objeto perfeito para thumb (P.R. na porta).
- **2 Camponês 1300**: 1ª sugestão do autocomplete ("como era viver na idade média"), público universal grande; fugimos da manada do castelo pela roça.
- **3 Pracinha 1944**: o vídeo mais parecido com o nosso formato já provou (Confluxo, cartoon "VOCÊ", 644 mil); aniversário de Monte Castelo em 21/02.
- **4 Brasil há 12 mil anos**: maior formato do ano em en (Fossil 13,6 mi), quase vazio em pt; testa um 3º público (ciência/animais) com a variante "eras" da bíblia.
Os 4 cobrem 4 públicos diferentes (Brasil colonial, medieval universal, guerra/Brasil séc. XX, pré-história): se um passar, sabemos qual veio.
