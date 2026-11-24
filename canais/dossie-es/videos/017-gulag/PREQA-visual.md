# Pré-QA visual automático

- Alvo: `canais/dossie-es/videos/017-gulag/preqa` · 101 quadros · modelo `claude-sonnet-5-5` · custo US$ 0.221 · `tools/preqa_visual.py`
- Resultado: **sem bloqueante** · bloqueante 0 · alto 1 · médio 19 · baixo 32
- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.

| Tempo | Quadro | Severidade | Categoria | Problema |
|---|---|---|---|---|
| 0:02 | Q01 `60.png` | medio | anacronismo | Monumento a Colombo de Barcelona com porto e cargueiro; é lugar real, o que pode ser intencional. A faixa inferior sinalizada pelo detector é só água lisa da cena, sem defeito. Na dúvida, conferir se o lugar bate com o roteiro (Gulag na URSS). |
| 0:32 | Q05 `960.png` | medio | texto_inventado | Livro-razão aberto com linhas de escrita pseudo-cirílica ilegível inventada pela IA nas duas páginas. Está pequeno e dá textura de documento, mas é letra falsa. |
| 0:42 | Q07 `1260.png` | medio | texto_inventado | Documento com texto borrado e carimbo vermelho ilegível, além de etiquetas nas pastas com rabiscos pseudo-escritos (canto esquerdo e pasta central). Borrão intencional, mas o título do papel e as etiquetas parecem letras falsas. |
| 1:36 | Q13 `2882.png` | medio | elemento_fora | A placa de título "EXPEDIENTE 2 / EL LIBRO" cobre o centro da cena e o carimbo "CLASIFICADO" vaza para fora da placa, sobrepondo-se ao fundo e à borda do cartão. Provavelmente é design intencional, mas a sobreposição do carimbo no canto superior direito merece conferência. |
| 2:12 | Q17 `3960.png` | medio | anacronismo | O trabalhador sorri de forma plácida e posada, com uma insígnia vermelha no ombro, em um canteiro de obras do Gulag. A insígnia pode ser um uniforme/insígnia inventado e destoa do tom do tema. Na dúvida entre estilo e defeito, registro como médio. |
| 3:42 | Q28 `6660.png` | medio | texto_inventado | As folhas de papel na mesa têm linhas de texto falso/ilegível escritas pela IA (cabeçalho e parágrafos). Estão pequenas e em segundo plano, mas dá para notar de perto. |
| 4:22 | Q33 `7860.png` | medio | texto_inventado | A folha de cima tem linhas de rabisco que imitam escrita e uma tabela com garranchos ilegíveis. É texto falso gerado pela IA, mas fica pequeno, borrado e em segundo plano, então parece mais textura do que texto legível. |
| 4:42 | Q35 `8460.png` | medio | texto_inventado | No caderno aberto, as colunas ao lado das grades têm garranchos que imitam escrita, e no canto inferior direito há uma marca ilegível. A grade com ✓ e ✗ é desenhada, não glifo de fonte. Por ser rabisco claramente ilegível, é mais textura do que texto falso, mas vale registrar. |
| 4:52 | Q36 `8760.png` | medio | valor_errado | O mapa da Rússia/URSS mostra poucos pontos vermelhos (3), e o quadro seguinte tem mais (7). Pode ser animação progressiva dos marcadores, mas confirme que está intencional. Também há risco de rótulo falso: o mapa não mostra texto visível, o que é bom. |
| 5:08 | Q40 `9244.png` | medio | outro | A placa de capítulo mistura espanhol ("EXPEDIENTE 5", "CLASIFICADO", "LOS MARINEROS") com "DOSSIER · GULAG · Nº 017". O carimbo "CLASIFICADO" vermelho passa da borda superior direita da placa e invade a imagem. Possivelmente intencional como carimbo, mas confira o encaixe. O porto ao fundo parece europeu (prédios), não soviético do Gulag, o que pode ser lugar errado. |
| 5:42 | Q44 `10260.png` | medio | anacronismo | A cena de Istambul mostra o Bósforo com minaretes e mesquitas, o que combina com o lugar. Porém o céu tem uma faixa de cor ligeiramente diferente no topo (sinal automático, 4% do quadro, RGB 87,107,117). Parece apenas o gradiente do céu, mas vale conferir se há faixa chapada na borda superior. |
| 5:52 | Q45 `10560.png` | medio | anacronismo | Na fila de homens, o chapéu de pele (ushanka) do centro parece ter uma estrela vermelha pequena, o que é plausível para a URSS. Dúvida de estilo: a placa/brasão na pilastra do portão é pequena e ilegível, sem texto legível. |
| 8:01 | Q61 `14430.png` | medio | valor_errado | O rótulo 'KRASNI BOR' é bem legível, mas fica sobre uma área de terra do mapa. A geografia lembra a região de São Petersburgo/Neva, então vale confirmar se a localização de Krasni Bor está correta. O quadro Q62 repete o mesmo mapa com pequeno deslocamento, provavelmente um zoom. |
| 8:58 | Q68 `16143.png` | medio | elemento_fora | A placa de capítulo 'LA EMBAJADA' cobre boa parte da cena de rua e o carimbo 'CLASIFICADO' invade a borda superior da placa. Parece intencional (estilo dossiê), mas o título e o carimbo ocupam o centro e atrapalham um pouco a leitura. Dúvida entre estilo e defeito. |
| 10:22 | Q78 `18660.png` | medio | texto_inventado | Linha de texto riscada com vermelho no centro do documento tem rabiscos pseudo-escritos ilegíveis. Pode ser intencional (texto censurado/rasurado); dúvida entre estilo e defeito. |
| 11:22 | Q85 `20460.png` | medio | anacronismo | À esquerda aparece um monumento em coluna alta com estátua no topo, parecido com o Monumento a Colombo de Barcelona. Num episódio do Gulag, é um lugar real reconhecível que parece fora de contexto. Dúvida entre cenário e erro de lugar. |
| 11:52 | Q88 `21360.png` | alto | anacronismo | Os carros são sedãs dos anos 60/70, parecidos com o SEAT 124, e a avenida lembra a Gran Vía de Madri. Para a entrevista de um dossiê do Gulag, o carro e o cenário podem destoar da época e do lugar. Verificar a época da cena. |
| 11:52 | Q89 `21364.png` | medio | anacronismo | A cena de rua mostra carros tipo SEAT 124/Lada dos anos 70 e prédios de Madri, enquanto a placa diz "Dossier · GULAG". Há dúvida se a época e o lugar combinam com o tema. A placa de capítulo cobre o centro da imagem, o que é comportamento esperado. |
| 12:22 | Q92 `22260.png` | medio | texto_inventado | A carta no centro tem texto borrado e ilegível escrito pela IA, mais um carimbo vermelho circular vazio. Por estar desfocado, lê-se como detalhe de cena, mas continua sendo texto falso que ocupa boa parte do quadro. |
| 13:32 | Q100 `24360.png` | medio | anacronismo | O homem de costas usa uma jaqueta acolchoada/puffer de estilo moderno, com remendo no cotovelo, numa cena de vilarejo espanhol. A época do vídeo parece anterior (ambientação histórica de espionagem), então pode ser anacronismo. Há dúvida: pode ser estilo de roupa neutro. |

32 item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).

## Sinais automáticos (PIL, sem IA)

- Q01 (0:02): faixa uniforme na borda base: 12% do quadro, cor RGB(71,88,96)
- Q02 (0:12): faixa uniforme na borda topo: 6% do quadro, cor RGB(82,97,102)
- Q20 (2:42): faixa uniforme na borda topo: 9% do quadro, cor RGB(55,63,66)
- Q21 (2:42): faixa uniforme na borda topo: 8% do quadro, cor RGB(55,63,66)
- Q44 (5:42): faixa uniforme na borda topo: 4% do quadro, cor RGB(87,107,117)
- Q51 (6:37): faixa uniforme na borda topo: 3% do quadro, cor RGB(65,75,80)
- Q56 (7:22): faixa uniforme na borda topo: 7% do quadro, cor RGB(71,92,106)
- Q75 (9:59): faixa uniforme na borda topo: 13% do quadro, cor RGB(59,66,69)
- Q77 (10:12): faixa uniforme na borda topo: 7% do quadro, cor RGB(73,100,113)
- Q81 (10:51): faixa uniforme na borda topo: 9% do quadro, cor RGB(45,57,64)
- Q82 (10:52): faixa uniforme na borda topo: 11% do quadro, cor RGB(45,57,64)
- Q87 (11:42): faixa uniforme na borda topo: 4% do quadro, cor RGB(127,149,156)

## Quadros

Q01=0:02, Q02=0:12, Q03=0:22, Q04=0:27, Q05=0:32, Q06=0:38, Q07=0:42, Q08=0:52, Q09=1:02, Q10=1:12, Q11=1:22, Q12=1:32, Q13=1:36, Q14=1:42, Q15=1:52, Q16=2:02, Q17=2:12, Q18=2:22, Q19=2:32, Q20=2:42, Q21=2:42, Q22=2:50, Q23=2:52, Q24=3:02, Q25=3:12, Q26=3:22, Q27=3:32, Q28=3:42, Q29=3:52, Q30=3:52, Q31=4:02, Q32=4:12, Q33=4:22, Q34=4:32, Q35=4:42, Q36=4:52, Q37=4:53, Q38=4:56, Q39=5:02, Q40=5:08, Q41=5:12, Q42=5:22, Q43=5:32, Q44=5:42, Q45=5:52, Q46=6:02, Q47=6:08, Q48=6:12, Q49=6:22, Q50=6:32, Q51=6:37, Q52=6:42, Q53=6:52, Q54=7:02, Q55=7:12, Q56=7:22, Q57=7:32, Q58=7:42, Q59=7:47, Q60=7:52, Q61=8:01, Q62=8:02, Q63=8:12, Q64=8:22, Q65=8:32, Q66=8:42, Q67=8:52, Q68=8:58, Q69=9:02, Q70=9:12, Q71=9:22, Q72=9:32, Q73=9:42, Q74=9:52, Q75=9:59, Q76=10:02, Q77=10:12, Q78=10:22, Q79=10:32, Q80=10:42, Q81=10:51, Q82=10:52, Q83=11:02, Q84=11:12, Q85=11:22, Q86=11:32, Q87=11:42, Q88=11:52, Q89=11:52, Q90=12:02, Q91=12:12, Q92=12:22, Q93=12:32, Q94=12:42, Q95=12:52, Q96=12:55, Q97=13:02, Q98=13:12, Q99=13:22, Q100=13:32, Q101=13:42
