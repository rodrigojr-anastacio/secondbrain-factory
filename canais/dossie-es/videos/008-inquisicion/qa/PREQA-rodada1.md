# Pré-QA visual automático

- Alvo: `canais/dossie-es/videos/008-inquisicion/preqa` · 120 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.287 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 12 · médio 36 · baixo 24
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:01 | Q01 `30.png` | medio | anacronismo | A catedral e a praça parecem coloniais, estilo Lima. Os chapéus de feltro de abas largas da multidão em primeiro plano parecem do séc. XIX. Em dúvida entre estilo e erro de época/lugar, registro como médio. |
| 0:11 | Q04 `330.png` | alto | anacronismo | A multidão usa tricórnios, casacas e vestidos do séc. XVIII, com casas de estilo anglo-colonial e telhados com mansardas. Não combina com a Inquisição espanhola nem com a praça com catedral dos quadros anteriores. A lona gigante voando também destoa da cena. |
| 0:39 | Q08 `1171.png` | medio | texto_inventado | A página do manuscrito aberto à direita tem rabiscos e símbolos que simulam escrita inventada pela IA. O texto está pequeno, mas dá para ver. |
| 1:21 | Q16 `2430.png` | medio | fundo/faixa | O sinal automático acusa faixa uniforme de 5% no topo (RGB 155,130,90). A olho nu o céu âmbar parece um degradê contínuo da cena, sem emenda visível. Na dúvida entre céu liso e faixa chapada, vale conferir a borda superior antes do render. |
| 1:21 | Q16 `2430.png` | medio | anacronismo | Roma em 1478 aparece com cúpula e fachada barroca (igreja ao centro) que só existiriam um século depois, junto de ruínas romanas. Há dúvida entre licença artística e anacronismo de arquitetura. |
| 2:01 | Q19 `3630.png` | medio | fundo/faixa | Faixa chapada cinza-esverdeada (RGB 55,60,58) no topo, em cerca de 4% do quadro, acima da Giralda e do guindaste. Pode ser céu liso ou vinheta da cena, mas lê como faixa de cor diferente. Na dúvida entre estilo e defeito, registro como médio. |
| 2:02 | Q20 `3649.png` | medio | fundo/faixa | Mesma faixa chapada cinza-esverdeada no topo, em cerca de 4% do quadro, atrás da cena. Pode ser céu liso intencional, mas parece uma faixa. Dúvida entre estilo e defeito. |
| 2:02 | Q21 `3662.png` | medio | fundo/faixa | Faixa chapada cinza-esverdeada no topo, em cerca de 4% do quadro. Pode ser céu liso ou vinheta, mas o limite com a ilustração fica visível. Dúvida entre estilo e defeito. |
| 2:11 | Q22 `3930.png` | alto | texto_inventado | O pergaminho no púlpito tem escrita cursiva ilegível inventada pela IA, com dois pequenos selos ou brasões desenhados. A letra falsa está bem visível no centro do quadro. O texto deveria vir do código ou ficar em branco. |
| 2:11 | Q22 `3930.png` | alto | anacronismo | O personagem em primeiro plano, atrás do púlpito, veste terno moderno com camisa branca e punhos, o que destoa da Espanha do século XV. Os figurantes ao fundo usam roupas de época incerta, com botões e gola alta. |
| 3:11 | Q29 `5730.png` | medio | anacronismo | O escrivão usa casaco de botões, camisa de colarinho e óculos redondos, o que lembra o século XIX e não o século XV/XVI. A pena está mal apoiada na mão. Dúvida: pode ser estilo, mas a roupa parece fora de época. |
| 3:41 | Q31 `6630.png` | alto | anacronismo | Cena de museu/galeria com damas em vestidos vitorianos/eduardianos, cavalheiros de cartola e vitrines com aparelhos de vidro e latão. É época errada para a Inquisição espanhola; só serve se a narração tratar de um museu moderno ou do século XIX. Há ainda um candelabro de parede estranho entre as janelas. |
| 4:41 | Q39 `8430.png` | medio | anacronismo | Muitas bandeirinhas vermelhas e amarelas nas torres e mastros, com brasões e listras inventados. Podem ser heráldica fora de época ou lugar. O porto tem vários símbolos pequenos que não dá para verificar. |
| 4:44 | Q40 `8519.png` | medio | valor_errado | Mapa com geografia duvidosa: o ponto 'ITALIA' fica no Adriático, perto da costa dálmata, e não na península italiana. 'IMPERIO OTOMANO' fica no leste da Anatólia. Há também manchas vermelhas soltas no deserto (Irã e Arábia) que parecem artefatos de textura. |
| 5:11 | Q46 `9330.png` | medio | elemento_fora | Coluna de fumaça e fogo enorme no centro da praça, com multidão embaixo. Dúvida: pode sugerir uma fogueira/auto de fé em grande escala, e o contexto pede que não haja figuras nas chamas. Não dá para ver figuras no fogo, mas vale conferir a intenção da cena. As casas têm telhado vermelho de tom muito saturado, destoando da paleta dessaturada. |
| 5:21 | Q47 `9630.png` | medio | anacronismo | Os quatro homens indígenas vestem túnicas brancas com capuz/manto parecidos entre si, e o pergaminho que um deles segura traz glifos inventados. O glifo é plausível como códice, mas é texto falso bem visível. Também há figuras de monstros nos tapetes ao fundo, de estilo duvidoso. |
| 5:31 | Q48 `9930.png` | medio | anacronismo | Há um cocar de penas vermelho ao fundo, entre os fiéis, no meio de uma missa cristã. Pode ser anacronismo/estereótipo, pois cocar de pena nessa cena é duvidoso. As túnicas brancas com faixa verde estampada são uniformes demais. Registrado por dúvida entre estilo e defeito. |
| 5:41 | Q49 `10230.png` | medio | anacronismo | Cena de rua com cesteiros e figuras de roupas variadas diante de uma igreja barroca de cúpula; o contexto (Espanha ou colônia) é ambíguo e a fachada barroca pode ser anacrônica para o período da Inquisição, mas é discutível. |
| 6:18 | Q54 `11353.png` | medio | texto_inventado | A placa na parede ao fundo traz um brasão com pseudo-letras ilegíveis, e o ano '1572' está escrito pela IA na parede. O texto parece plausível, mas é texto inventado pela IA e não vem do código. |
| 6:54 | Q63 `12424.png` | medio | fundo/faixa | No mapa da América do Sul há uma borda clara/bege ao redor do continente (halo de costa) e a textura do mar é diferente da dos mapas anteriores. Pode ser estilo intencional, mas parece uma faixa chapada ao longo da costa; na dúvida, conferir. |
| 6:58 | Q64 `12547.png` | medio | fundo/faixa | Mesmo halo bege claro contornando a costa da América do Sul, parecido com uma faixa chapada. Pode ser estilo, mas vale conferir. |
| 7:01 | Q65 `12630.png` | medio | anacronismo | Soldados no forte com tricórnios/chapéus e casacas azuis com faixa vermelha parecem uniformes do século XVIII, e os navios têm bandeirolas vermelhas sem identificação. Pode destoar da época da Inquisição (Cartagena, séculos XVI-XVII). Na dúvida entre estilo e erro. |
| 7:21 | Q67 `13230.png` | medio | anacronismo | O homem à esquerda usa casaca com botões, colete e gola de renda de estilo século XVIII, e o outro usa chapéu largo e batina. A roupa é mais tardia que a da Inquisição do início do século XVII. Dúvida de época. |
| 7:39 | Q69 `13764.png` | medio | elemento_fora | Placa 'EXPEDIENTE 10' com o carimbo 'CLASIFICADO' cobre a maior parte da cena, e o carimbo está colado na borda superior direita da placa. Possível inconsistência entre 'Nº 008' e 'Expediente 10' (numeração diferente). Legibilidade OK. |
| 7:59 | Q72 `14361.png` | alto | texto_inventado | O crucifixo na mão do padre tem uma etiqueta/texto minúsculo ilegível ('1611'?) escrito pela IA. Há também '1611' gravado no pilar à direita, que pode ser intencional, mas é texto dentro da imagem e não veio do código. |
| 8:11 | Q74 `14730.png` | alto | texto_inventado | O manuscrito aberto no centro da mesa tem linhas de escrita cursiva ilegível e falsa, inventada pela IA, bem visível no papel iluminado pela vela. |
| 8:44 | Q77 `15715.png` | medio | fundo/faixa | Faixa lisa cinza-ardósia no topo, cerca de 17% do quadro, acima do domo de São Pedro. Parece céu liso intencional (escurecido pela vinheta), mas o corte reto na altura dos telhados dá a impressão de faixa chapada. Se for céu da cena, está ok. Conferir se não é um bloco de cor sólida colado. |
| 8:44 | Q78 `15728.png` | medio | fundo/faixa | Mesma faixa uniforme cinza-ardósia no topo (cerca de 17%), atrás do domo. Provavelmente céu liso da cena, mas há dúvida sobre ser faixa chapada, pois o degradê é quase nulo e a transição para os telhados é reta. |
| 9:11 | Q81 `16530.png` | medio | anacronismo | Praça com arquitetura barroca/neoclássica (colunata, cúpulas) e fogueira com fumaça. Na dúvida entre estilo e defeito: a arquitetura parece mais Roma do século XVII que a Espanha. As chamas não têm figuras, então não é erro grave. Há também uma faixa vertical clara na borda direita, na altura do prédio. |
| 9:21 | Q82 `16830.png` | medio | anacronismo | Juízes com barretes e vestes vermelhas de cardeais, em salão rotunda. Na dúvida: pode ser leitura intencional do tribunal, mas fica mais próximo de cardeais do Vaticano do que de inquisidores espanhóis. A tapeçaria à esquerda tem desenho ornamental que parece pseudo-mapa. |
| 9:31 | Q83 `17130.png` | alto | anacronismo | Papa em vestes brancas modernas falando num púlpito com microfone de haste, com plateia de terno moderno em primeiro plano. Anacronismo claro numa cena da Inquisição. |
| 9:41 | Q84 `17430.png` | medio | anacronismo | Praça com catedral de estilo colonial hispano-americano (tipo Lima) e multidão densa. Pode estar correto para o contexto, mas a fachada azul chapada e os prédios laterais parecem mais modernos. Ao fundo, textura repetida da multidão pode causar leitura confusa. |
| 10:11 | Q89 `18330.png` | alto | anacronismo | O soldado veste uniforme azul-acinzentado de gola alta, com peitoral de metal e botões, do século XIX. Não combina com a Inquisição espanhola. O homem com o avental e a bolsa com cruz vermelha também lembra o século XIX e cruza com o símbolo da Cruz Vermelha, criada em 1863. |
| 10:21 | Q90 `18630.png` | medio | anacronismo | Os homens de preto usam colarinhos de renda brancos e casacas do século XVII. Os soldados usam elmos com penacho vermelho e armaduras do século XVI. A mistura de épocas é discutível. Há dúvida entre estilo e erro. |
| 10:31 | Q91 `18930.png` | alto | anacronismo | Os soldados carregam baús e vestem casacas verdes com faixas vermelhas, bicornes e chapéus de oficial. Os uniformes parecem do século XVIII ou XIX, e não da época da Inquisição. A arquitetura é colonial hispano-americana, com balcão de madeira, e não espanhola. |
| 11:01 | Q94 `19830.png` | medio | anacronismo | O professor usa casaca e gravata do século XIX, e as crianças usam roupas camponesas. As roupas destoam da época da Inquisição. Há dúvida entre estilo e erro. |
| 11:10 | Q95 `20113.png` | medio | anacronismo | A multidão ao fundo usa roupas do século XIX, com coletes, faixas vermelhas e toucas. A catedral é gótica. A época destoa da Inquisição. Há dúvida entre estilo e erro. |
| 11:17 | Q98 `20309.png` | medio | texto_inventado | O quadro-negro atrás do professor tem rabiscos pseudo-escritos feitos pela IA (letras e símbolos ilegíveis). Estão discretos e em giz apagado, então é pouco visível. |
| 11:47 | Q101 `21213.png` | medio | anacronismo | A bandeira à esquerda tem emblema circular inventado, e há outra bandeira à direita. Em um vídeo sobre a Inquisição, o contexto de Hidalgo (México, 1810) pode ser um lugar/época fora do tema. Na dúvida, conferir se a bandeira é aceitável. |
| 11:51 | Q102 `21330.png` | medio | anacronismo | A bandeira rasgada no alto à esquerda tem emblema circular inventado, não identificável. É um detalhe pequeno, mas pode ser lido como bandeira falsa. |
| 12:21 | Q105 `22230.png` | alto | anacronismo | O fundo da placa de capítulo mostra uma ponte de pedra sobre um rio, com prédios haussmannianos de estilo parisiense do século XIX e bondes. Não combina com a Inquisição espanhola nem com Madri. É o lugar real errado. |
| 12:22 | Q106 `22245.png` | alto | anacronismo | O mesmo fundo parisiense de século XIX atrás da placa 'EL ARCHIVO' (ponte, prédios de estilo haussmanniano). A arquitetura e o lugar não combinam com o tema. |
| 12:22 | Q107 `22257.png` | alto | anacronismo | O fundo parisiense (ponte, prédios de estilo XIX, barco no canto inferior direito) aparece de novo, com torres de igreja tipo Notre-Dame ao fundo. Lugar e época errados para a Inquisição espanhola. |
| 12:31 | Q109 `22530.png` | medio | outro | Há uma sobreposição fantasma semitransparente sobre as pilhas de livros (uma silhueta com mão e formas de outra cena). Pode ser um crossfade entre cenas, mas parece uma dupla exposição suja. Confirmar se é só transição. |
| 13:01 | Q111 `23430.png` | medio | texto_inventado | As páginas do livro aberto têm tabelas com manuscrito pseudo-legível, uma letra falsa gerada pela IA. É um texto de baixa legibilidade e discreto, tolerável como textura, mas ainda é texto inventado. |
| 13:03 | Q112 `23491.png` | medio | valor_errado | No mapa, o rótulo 'CHILE' aponta para um ponto na costa. É o único rótulo de país entre cidades (Cartagena, Quito, Lima, Río de la Plata), o que é inconsistente. A região do 'Río de la Plata' também está posicionada no interior do estuário, um pouco deslocada. |
| 13:06 | Q113 `23578.png` | medio | valor_errado | O rótulo "CHILE" é um país, enquanto os outros são cidades (Cartagena, Quito, Lima). O ponto fica na costa, na altura de Santiago, mas o rótulo não corresponde ao tipo dos demais. Além disso, o ponto "RÍO DE LA PLATA" cai em terra, no interior, e não no estuário. |
| 13:41 | Q118 `24630.png` | medio | texto_inventado | Os livros pendurados no pescoço do homem trazem escrita falsa e ilegível, feita pela IA. Está bem visível nas páginas, mas é manuscrito decorativo e não ocupa o centro da cena. Também aparecem manchas vermelhas, que talvez sejam sangue, sobre o sambenito amarelo. |

24 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q06 (0:31): faixa uniforme na borda topo: 8% do quadro, cor RGB(41,50,52)
- Q07 (0:32): faixa uniforme na borda topo: 8% do quadro, cor RGB(40,50,52)
- Q16 (1:21): faixa uniforme na borda topo: 5% do quadro, cor RGB(155,130,90)
- Q19 (2:01): faixa uniforme na borda topo: 4% do quadro, cor RGB(55,60,58)
- Q20 (2:02): faixa uniforme na borda topo: 4% do quadro, cor RGB(55,60,58)
- Q21 (2:02): faixa uniforme na borda topo: 4% do quadro, cor RGB(55,60,58)
- Q25 (2:41): faixa uniforme na borda topo: 3% do quadro, cor RGB(77,100,103)
- Q36 (4:23): faixa uniforme na borda topo: 5% do quadro, cor RGB(49,54,53)
- Q37 (4:23): faixa uniforme na borda topo: 5% do quadro, cor RGB(49,55,54)
- Q42 (5:01): faixa uniforme na borda topo: 4% do quadro, cor RGB(47,58,64)
- Q43 (5:02): faixa uniforme na borda topo: 6% do quadro, cor RGB(44,54,59)
- Q44 (5:03): faixa uniforme na borda topo: 7% do quadro, cor RGB(44,54,59)
- Q51 (5:57): faixa uniforme na borda topo: 21% do quadro, cor RGB(55,64,67)
- Q52 (5:57): faixa uniforme na borda topo: 21% do quadro, cor RGB(55,63,67)
- Q77 (8:44): faixa uniforme na borda topo: 17% do quadro, cor RGB(43,52,56)
- Q78 (8:44): faixa uniforme na borda topo: 17% do quadro, cor RGB(43,52,56)
- Q85 (9:44): faixa uniforme na borda topo: 13% do quadro, cor RGB(38,47,51)
- Q105 (12:21): faixa uniforme na borda topo: 17% do quadro, cor RGB(46,53,56)
- Q106 (12:22): faixa uniforme na borda topo: 17% do quadro, cor RGB(46,53,56)
- Q107 (12:22): faixa uniforme na borda topo: 13% do quadro, cor RGB(47,55,58)

## Quadros

Q01=0:01, Q02=0:02, Q03=0:02, Q04=0:11, Q05=0:21, Q06=0:31, Q07=0:32, Q08=0:39, Q09=0:41, Q10=0:51, Q11=0:55, Q12=1:01, Q13=1:15, Q14=1:18, Q15=1:19, Q16=1:21, Q17=1:31, Q18=1:41, Q19=2:01, Q20=2:02, Q21=2:02, Q22=2:11, Q23=2:21, Q24=2:31, Q25=2:41, Q26=2:50, Q27=2:51, Q28=3:01, Q29=3:11, Q30=3:31, Q31=3:41, Q32=3:43, Q33=3:51, Q34=4:01, Q35=4:11, Q36=4:23, Q37=4:23, Q38=4:31, Q39=4:41, Q40=4:44, Q41=4:59, Q42=5:01, Q43=5:02, Q44=5:03, Q45=5:06, Q46=5:11, Q47=5:21, Q48=5:31, Q49=5:41, Q50=5:51, Q51=5:57, Q52=5:57, Q53=6:11, Q54=6:18, Q55=6:21, Q56=6:31, Q57=6:36, Q58=6:38, Q59=6:41, Q60=6:43, Q61=6:43, Q62=6:51, Q63=6:54, Q64=6:58, Q65=7:01, Q66=7:11, Q67=7:21, Q68=7:31, Q69=7:39, Q70=7:41, Q71=7:51, Q72=7:59, Q73=8:01, Q74=8:11, Q75=8:21, Q76=8:41, Q77=8:44, Q78=8:44, Q79=8:51, Q80=8:51, Q81=9:11, Q82=9:21, Q83=9:31, Q84=9:41, Q85=9:44, Q86=9:51, Q87=10:01, Q88=10:05, Q89=10:11, Q90=10:21, Q91=10:31, Q92=10:41, Q93=10:51, Q94=11:01, Q95=11:10, Q96=11:11, Q97=11:11, Q98=11:17, Q99=11:31, Q100=11:41, Q101=11:47, Q102=11:51, Q103=11:58, Q104=12:11, Q105=12:21, Q106=12:22, Q107=12:22, Q108=12:28, Q109=12:31, Q110=12:51, Q111=13:01, Q112=13:03, Q113=13:06, Q114=13:11, Q115=13:21, Q116=13:34, Q117=13:34, Q118=13:41, Q119=13:51, Q120=14:01
