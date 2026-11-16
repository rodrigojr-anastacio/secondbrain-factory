# Checagem bloco a bloco: Em Relevo 005 (enchente de maio/2024, Porto Alegre)

15/11/2026, etapa 1. Itens F* em `FATOS.md`; N1-N8 = fatos novos desta checagem (abaixo). Resultado: **24 OK · 16 AJUSTAR · 0 CORTAR** (40 blocos). Nenhum bloco precisa sair; os ajustes são de precisão (atribuição, estado dos rios, nível da lagoa, números de obras). `shared/roteiro.py` NÃO foi editado: as substituições estão na seção "Correções a aplicar".

## Fatos novos (verificados em 15/11/2026; incluir no FATOS.md)
- **N1 Meteorologia:** MetSul/Embrapa/Climatempo: massa de ar quente e seca persistente sobre o centro do Brasil (bloqueio atmosférico, início técnico em 22/04) canalizando umidade amazônica para o RS; sistemas frontais estacionários sobre o estado; INMET: sistema frontal "semi-estacionário" no centro do RS. INMET (nota do 1º ano) diz só "combinação de diversos fatores meteorológicos". SEGUNDO X.
- **N2 Lagoa dos Patos:** pico em 16/05 em Pelotas (~3 m, acima dos 2,88 m de 1941) e em Rio Grande (2,77 m); bairros alagados em Pelotas (Balsa, Simões Lopes, Laranjal) e Rio Grande; prefeitura de Pelotas cita alagamentos em São Lourenço, Rio Grande, São José do Norte e Pelotas (sem lista de bairros de SLS). SEGUNDO X.
- **N3 Dique do Sarandi:** reportagens: dique atrás da Fiergs "rompeu" em 04/05 (sábado) e a água extravasou; prefeito: "voltou a passar água por cima do dique" (03/05). Prefeitura demoliu casas para reconstruir o dique; cota emergencial de 5,5 m a partir de 26/11/2024. Ebap 10 = maior casa de bombas do Sarandi. SEGUNDO X / PRIMÁRIA (prefeitura).
- **N4 30% do território:** confirmado na página "Porto Alegre Forte" (prefeitura, maio/2025): 30% do território atingido, ~160 mil pessoas, ~93 mil domicílios. Sem confirmação independente: atribuir à prefeitura.
- **N5 Aeroporto:** "completamente alagado" (Olhar Digital); fechado de 03/05 a 21/10 (F49).
- **N6 Altitude:** Caxias do Sul ~817 m (guias, não IBGE; outras fontes ~760 m) → só "uns 800 m" e só para Caxias/serra.
- **N7 Comportas em concreto:** prefeitura/DMAE: das 14 comportas de 2024, oito foram extintas com estruturas permanentes em concreto armado (3, 5, 7, 8, 9, 10, 13, 14); 1, 2, 4, 6 seguem móveis e modernizadas (11 e 12 novas no Cais Mauá, teste em jul/2026); muro com revisão estrutural (revista da prefeitura, ago/2026). PRIMÁRIA (municipal).
- **N8 SMS 40199:** enviar o CEP por SMS ao 40199 (gratuito); página do Governo do RS e Defesa Civil. Desde dez/2024 também há alerta por tela e som sem cadastro (Canaltech). PRIMÁRIA.

## Bloco a bloco
| Bloco | Status | Afirmação verificada | Fonte | Observação |
|---|---|---|---|---|
| b01 | OK | Caxias 266 mm em 02/05; "quase três vezes o recorde anterior" (266,2/94,4 = 2,8) | F24 (INMET, relido: "maior desde 1961, superando 94,4 mm em 27/05/2017") | PRIMÁRIA. "Recorde anterior" = marca anterior na série do INMET. |
| b02 | OK | 5,35 m; 3 dias depois (02→05/05); "a cem km" (96,5 km em linha reta); mais alto que 1941 (4,76); frase-âncora | F1, F7, F22, F31 | Frase-âncora defensável: Caxias 919,1 mm e Veranópolis 951,2 mm em maio vs. Porto Alegre 564,8 mm. A fala já diz no b04 que a capital teve chuva recorde. Risco: "quem afundou foi Porto Alegre" não é exclusivo (o vale do Taquari também); o b12 cobre isso. Mantida (contrato). |
| b03 | OK | ~160 mil atingidos (prefeitura); rodoviária e aeroporto alagados; 184 mortos (Defesa Civil) | F44, F47, F49, F50 | F44: "30% / 160.210" confirmado na página "Porto Alegre Forte" da prefeitura. Aeroporto "alagado" confirmado por imprensa (Olhar Digital), não está no FATOS: incluir como N5. Balanço de 184 mortos é de 24/04/2025 (não dizer "na época"). |
| b04 | OK | 564,8 mm, maior total mensal desde 1916 ("chuva recorde") | F25 (INMET relido: "maior valor mensal desde 1916") | PRIMÁRIA. |
| b05 | AJUSTAR | Gravataí não nasce na serra nem no centro/planalto (nasce perto do litoral norte) | F16 | Frase corrigida abaixo. Os 5 rios continuam todos citados. |
| b06 | OK | Guaíba oficialmente lago; rio × lago em debate; "quase um terço"; só uma saída | F18, F15 | Sem "estuário" (FORA no FATOS); a obrigação mencionava estuário como exemplo, não como exigência literal. "Quase um terço" cumpre a ressalva do crivo. |
| b07 | OK | Frente fria estacionária + bloqueio (massa de ar quente e seca no centro do país) + umidade amazônica | F53 + N1 (MetSul, Embrapa, Climatempo, INMET: "semi-estacionário") | Atribuído a "meteorologistas", sem número. Fica OK. |
| b08 | OK | >420 mm em média, 24/04-04/05 (11 dias); "uns três meses de chuva" | F23 (WWA) | "Uns três meses" é conta nossa (420 mm ÷ ~130-140 mm/mês; RS ~1.500-1.700 mm/ano); defensável, vago. Se o crivo/QA pedir fonte, trocar por "mais de um quarto do que costuma chover num ano inteiro". |
| b09 | AJUSTAR | Caxias 707 mm de 1 a 13/05 OK; Santa Maria 213,6 mm em 01/05: "maior já registrado num dia nessa estação em 112 anos" | F24 (INMET relido) | Precisar que é recorde da estação. |
| b10 | AJUSTAR | "Os rios não estavam vazios" afirma estado dos rios antes de 24/04; o FATOS marca isso NÃO CONFIRMADO (só a sequência de cheias de set e nov/2023 é fato) | F11-F14 | Troca por frase que só afirma a sequência de cheias. "3ª grande cheia em 8 meses" fica (contagem própria declarada no F14). |
| b11 | AJUSTAR | "Planalto gaúcho a uns 800 m": generalização; só Caxias tem número (817 m citado por imprensa/guias, ~760 m em outras) | N6 | Trocar por "a serra, onde fica Caxias do Sul". "Porto Alegre quase no nível do mar" OK. |
| b12 | AJUSTAR | 33,7 m em Lajeado (02/05, quinta) OK; "recorde de 1941" contradiz o b10 (em set/2023 o rio já passou 1941) | F27, F28 | Trocar "recorde" por "marca". "Cidades inteiras do vale debaixo d'água": notório (Muçum, Roca Sales, Lajeado), sem item no FATOS: adicionar F-novo na etapa 2 se o crivo pedir. |
| b13 | OK | Taquari deságua no Jacuí; Jacuí corre para leste | F16, F19 | Geografia. |
| b14 | OK | 251 municípios ("mais de 250"); ~85 mil km²; ~30% do estado | F15, F16 | Cumpre "quase um terço"/30%, não "um terço" seco. |
| b15 | OK | Jacuí recebe Taquari; Caí, Sinos, Gravataí; todos no Guaíba | F16 |  |
| b16 | AJUSTAR | ~500 km² OK (468-496); "uns dois metros de fundura, em média" vem de estudo de 1988, SEGUNDO X; frase segura do FATOS é "poucos metros" | F17 | Seguir a frase segura. |
| b17 | AJUSTAR | 1.200 m³/s é a vazão MÉDIA de saída (DMAE), não "dias normais"; "passaram muito das maiores vazões já medidas" OK (1,4-2,3×) | F19, F20 | Trocar "Em dias normais" por "Em média". |
| b18 | OK | Taquari e Caí 02/05 (quinta); Sinos 04/05 (sábado); Jacuí 05/05 (domingo, em Rio Pardo); Guaíba pico 05/05 de madrugada (~05h30) | F30, F31, F1 | IPH/RBRH, PRIMÁRIA. Datas e dias da semana conferidos (2/5/2024 = quinta). |
| b19 | OK | Síntese (sem número novo) | F15-F31 |  |
| b20 | OK | Guaíba deságua ao sul na Lagoa dos Patos; saída única | F21 |  |
| b21 | OK | Laguna ~250 km, ligada ao mar; saída em Rio Grande entre molhes | F21 |  |
| b22 | OK | Síntese: quase 1/3 do estado → lago raso → 250 km → gargalo | F15, F21 |  |
| b23 | OK | Vento sul segura o Guaíba; até ~50 cm; atribuído ao IPH/UFRGS; não afirma que causou o pico | F32, F33 | Cumpre o limite do F33. |
| b24 | AJUSTAR | Lagoa: picos em 16 e 27/05 (FURG), ou seja 11 dias (não 14) após o pico do Guaíba; "alagou bairros" confirmado só para Pelotas e Rio Grande (SLS: alagamentos em geral); Guaíba ~1 mês acima da cota OK | F35, F6, N2 | Trocar por "meados de maio" e "causou alagamentos". |
| b25 | AJUSTAR | 1941 ~4,7 m OK (4,67-4,76); "mais de um mês para baixar": a fonte diz que só voltou a 3 m depois de mais de um mês (DW via imprensa) | F7, FATOS §11 | Precisar. "Porto Alegre sabia que podia acontecer" é editorial com base em 1941: OK. |
| b26 | OK | Projeto do DNOS de 1943; obras principais nos anos 70; 68 km de diques, 14 comportas, 23 casas de bombas | F37, F38 | Fonte municipal (DMAE). |
| b27 | OK | Como funciona o sistema (diques, comportas, bombas) | F37 | Descrição geral; "portões de aço" é o que o DMAE descreve (comportas metálicas); baixo risco. |
| b28 | OK | Comporta perto da Sertório rompeu em 03/05; água entrou na zona norte (Navegantes) | F40 | Sem horário. |
| b29 | AJUSTAR | 19 das 23 paradas foi em 06/05 (dia seguinte ao pico de 05/05), não "no pico"; "por algumas delas o Guaíba entrou": consenso "casas de bombas inundadas" | F41, F43 | Trocar "No pico" por "No dia seguinte ao pico". |
| b30 | AJUSTAR | Dique do Sarandi: reportagens dizem "rompeu"/"extravasou" (prefeito: "voltou a passar água por cima do dique"); "venceu o dique em pontos baixos" não é o que as fontes dizem; 26 mil = dado da plataforma da prefeitura, SEGUNDO X (o F42 avisa para não dar o número de desabrigados) | F42, F45, N3 | Trocar por "o dique rompeu" e atribuir os 26 mil à prefeitura (como "pessoas atingidas", não desabrigados). |
| b31 | AJUSTAR | "A água não passou por cima do muro da Mauá" está como fato seco; o FATOS (F43) manda atribuir ("por cima" = NÃO CONFIRMADO; consenso das fontes lidas). 4,5 m vs 6 m atribuído ao WWA ("teria") OK | F39, F43 | Adicionar "pelo que apontam os relatos técnicos". Não diz que passou por cima (item 2 do contrato: OK). Observação: a frase fala do muro, e o b30 diz que o dique do Sarandi rompeu; as duas afirmações são compatíveis. |
| b32 | AJUSTAR | "Com o Guaíba acima dos cinco metros a defesa não segurou" sugere que só falhou acima de 5 m, mas o b31 diz que começou a falhar perto de 4,5 m (e a comporta 14 rompeu em 03/05, antes do pico) | F39, F40, F43 | Reescrever sem ligar a falha a um nível. Atribuições das três causas OK. |
| b33 | OK | Mercado Público 1,5 m (placa, 08/05); bairros; ~30% do território (prefeitura) | F48, F45, F44 | "Cerca de 30%" atribuído à prefeitura; página oficial confirmada (N4). Não dizer "um terço". |
| b34 | OK | Transição | — |  |
| b35 | AJUSTAR | "Os rios já vinham de duas cheias" repete o b10 e implica rios cheios antes (NÃO CONFIRMADO); "cheias chegaram quase juntas": picos entre 02 e 05/05, OK | F11-F14, F30 | Trocar por "a região já tinha passado por duas grandes cheias em oito meses". |
| b36 | AJUSTAR | "A defesa cedeu antes do limite para o qual foi feita" dito como fato; a origem é o WWA ("reportedly") | F39 | Atribuir ao WWA, com "teria". |
| b37 | OK | WWA: chance mais que dobrou; chuva 6-9% mais intensa; El Niño sozinho "comparably large" | F51, F52 | Palavras do WWA preservadas. |
| b38 | OK | Sem previsão de nova enchente; "não volta em data marcada, ninguém consegue prever"; geografia não muda | fecho editorial | Item 3 do contrato: OK (nada prevê enchente). |
| b39 | AJUSTAR | "Prefeitura anunciou fechar parte das comportas com concreto": confirmado, mas o dado exato é oito das 14 comportas trocadas por estruturas de concreto armado (3, 5, 7, 8, 9, 10, 13, 14), obra de 2024-2026 (anúncios do DMAE a partir de dez/2024); "obras nos diques e casas de bombas": confirmado para o dique do Sarandi (elevação de cota, 2024-2025); casas de bombas não confirmado. SMS 40199 com CEP: confirmado (estado.rs.gov.br) | N7, N8 | Trocar a 1ª frase. SMS fica como está. |
| b40 | OK | CTA para o vídeo do clima do Sul (bG6-E4qjXYc, publicado); sem gancho de próximo vídeo | canal | Item 5 do contrato: OK. Etapa 2/pacote: conferir que bG6-E4qjXYc segue público. |

## Pontos específicos pedidos
1. **Frase-âncora** ("A chuva mais pesada caiu na serra. Quem afundou foi Porto Alegre."): defensável. INMET: Caxias 919,1 mm em maio e 707,2 mm de 1 a 13/05; Veranópolis 951,2 mm; Porto Alegre 564,8 mm (maior mês desde 1916, mas ~40% abaixo). O b04 diz em seguida que a capital também teve chuva recorde. Ressalva: "serra" é simplificação (a chuva também foi forte no centro; o b09 e o b19 dizem "serra e centro do estado").
2. **Água por cima do muro:** nenhum trecho diz isso (b31 nega, com atribuição após a correção). O b30 diz que o dique do Sarandi rompeu, o que não contradiz.
3. **Nova enchente:** nenhum trecho prevê (b38 diz que ninguém consegue prever; b39 só fala de alerta e obras).
4. **"Quase um terço"/30%:** b06, b22, b35 dizem "quase um terço" ("quase 1/3" na tela); b14 diz "uns trinta por cento"; b33 "cerca de trinta por cento" (território da capital, outro dado). Nenhum "um terço" seco.
5. **Gancho de próximo vídeo:** nenhum; b40 só remete ao vídeo publicado do clima do Sul.

## Correções a aplicar (substituições exatas; fala = `\n` entre linhas, tela = ` | `)
**b05**
- fala: `Da serra e do centro do estado descem rios: o Jacuí, o Taquari, o Caí, o Sinos, o Gravataí.` → `Da serra, do planalto e do centro do estado vêm os rios: o Jacuí, o Taquari, o Caí, o Sinos e, perto da capital, o Gravataí.`
- tela: `Da serra e do centro do estado descem rios: | o Jacuí, o Taquari, o Caí, o Sinos, o Gravataí.` → `Da serra, do planalto e do centro do estado vêm os rios: | o Jacuí, o Taquari, o Caí, o Sinos e, perto da capital, o Gravataí.`
**b09**
- fala: `teve num único dia a maior chuva em cento e doze anos.` → `teve, num único dia, a maior chuva já registrada ali em cento e doze anos.`
- tela: `teve num único dia a maior chuva em 112 anos.` → `teve, num único dia, a maior chuva já registrada ali em 112 anos.`
**b10**
- fala: `E os rios não estavam vazios.` → `E não era a primeira cheia grande.`
- tela: `E os rios não estavam vazios.` → `E não era a primeira cheia grande.`
**b11**
- fala: `O planalto gaúcho fica a uns oitocentos metros de altitude.` → `A serra gaúcha, onde fica Caxias do Sul, está a uns oitocentos metros de altitude.`
- tela: `O planalto gaúcho fica a uns 800 metros de altitude.` → `A serra gaúcha, onde fica Caxias do Sul, está a uns 800 metros de altitude.`
**b12**
- fala: `Mais de três metros acima do recorde de mil novecentos e quarenta e um.` → `Mais de três metros acima da marca de mil novecentos e quarenta e um.`
- tela: `Mais de 3 metros acima do recorde de 1941.` → `Mais de 3 metros acima da marca de 1941.`
**b16**
- fala: `mas só uns dois metros de fundura, em média.` → `mas só uns poucos metros de fundura.`
- tela: `mas só uns 2 metros de fundura, em média.` → `mas só uns poucos metros de fundura.`
**b17**
- fala: `Em dias normais, o Guaíba despeja` → `Em média, o Guaíba despeja`
- tela: `Em dias normais, o Guaíba despeja` → `Em média, o Guaíba despeja`
**b24**
- fala: `só chegou ao pico duas semanas depois, e alagou bairros de Pelotas, São Lourenço do Sul e Rio Grande.` → `só chegou ao pico em meados de maio, e causou alagamentos em Pelotas, São Lourenço do Sul e Rio Grande.`
- tela: `só chegou ao pico duas semanas depois, | e alagou bairros de Pelotas, São Lourenço do Sul e Rio Grande.` → `só chegou ao pico em meados de maio, | e causou alagamentos em Pelotas, São Lourenço do Sul e Rio Grande.`
**b25**
- fala: `e levou mais de um mês para baixar.` → `e levou mais de um mês para voltar aos três metros.`
- tela: `e levou mais de um mês para baixar.` → `e levou mais de um mês para voltar aos 3 metros.`
**b29**
- fala: `No pico, dezenove das vinte e três estavam paradas` → `No dia seguinte ao pico, dezenove das vinte e três estavam paradas`
- tela: `No pico, 19 das 23 estavam paradas` → `No dia seguinte ao pico, 19 das 23 estavam paradas`
**b30**
- fala: `a água venceu o dique em pontos baixos, e a casa de bombas número dez foi inundada.` → `o dique rompeu, e a casa de bombas número dez foi inundada.`
- tela: `a água venceu o dique em pontos baixos,` → `o dique rompeu,`
**b30**
- fala: `cerca de vinte e seis mil pessoas.` → `cerca de vinte e seis mil pessoas, segundo a prefeitura.`
- tela: `cerca de 26 mil pessoas.` → `cerca de 26 mil pessoas, segundo a prefeitura.`
**b31**
- fala: `E um detalhe importante: a água não passou` → `E um detalhe importante: pelo que apontam os relatos técnicos, a água não passou`
- tela: `E um detalhe importante: a água não passou` → `E um detalhe importante: pelo que apontam os relatos técnicos, a água não passou`
**b32**
- fala: `O fato é que, com o Guaíba acima dos cinco metros, a defesa feita depois de quarenta e um não segurou.` → `O fato é que a defesa feita depois de mil novecentos e quarenta e um não segurou essa cheia, que passou dos cinco metros.`
- tela: `O fato é que, com o Guaíba acima dos 5 metros, | a defesa feita depois de 1941 não segurou.` → `O fato é que a defesa feita depois de 1941 | não segurou essa cheia, que passou dos 5 metros.`
**b35**
- fala: `Porque os rios já vinham de duas cheias.` → `Porque a região já tinha passado por duas grandes cheias em oito meses.`
- tela: `Porque os rios já vinham de duas cheias.` → `Porque a região já tinha passado por duas grandes cheias em 8 meses.`
**b36**
- fala: `E porque, quando a água subiu, a defesa da cidade cedeu nos pontos fracos antes do limite para o qual foi feita.` → `E porque, segundo o estudo do World Weather Attribution, a defesa da cidade teria cedido nos pontos fracos antes do limite para o qual foi feita.`
- tela: `E porque, quando a água subiu, |` → `E porque, segundo o estudo do World Weather Attribution, |`
**b36**
- tela: `a defesa da cidade cedeu nos pontos fracos |` → `a defesa da cidade teria cedido nos pontos fracos |`
**b39**
- fala: `a prefeitura anunciou o fechamento de parte das comportas com concreto e obras nos diques e nas casas de bombas.` → `a prefeitura fechou para sempre oito das catorze comportas do muro, trocadas por concreto, reformou as outras e reforçou o dique do Sarandi.`
- tela: `a prefeitura anunciou o fechamento de parte das comportas com concreto | e obras nos diques e nas casas de bombas.` → `a prefeitura fechou para sempre oito das 14 comportas do muro, trocadas por concreto, | reformou as outras e reforçou o dique do Sarandi.`

Efeito em tempo/TTS: sem mudança material (todas as trocas têm tamanho parecido; b39 +10 palavras, b36 +6). Refazer `fala_tts` dos blocos alterados com as tags v3 do bloco (a primeira linha mantém a tag).

## Checklist do contrato (EMBALAGEM.md, Obrigações; CRIVO.md) com os tempos estimados
- [x] Frase-âncora antes de ~0:30: termina no fim do b02 ≈ 0:23 (b02 começa em 0:10.5; 6 primeiros blocos a 1,3×).
- [x] 5 rios (b05, ~0:44) + "lago" e "quase um terço" + "só tem uma saída" (b06, ~0:54-1:11): perto de 1:00 (b06 ocupa 0:54 a ~1:10; folga curta, aceitável).
- [x] Capítulo do funil até ~4:00 (limite, não folga): o T2 (o lago recebe a água de ~30% do estado) está pago em b14-b17 (bacia 85 mil km², 30%, rios, Guaíba raso, vazões), de 3:00 a ~4:00; Taquari 33,7 m em b12 (2:34). Os blocos b18-b19 (a onda de cheia em dias, síntese) terminam em ~4:33 (b20 começa em 4:33). Dentro do contrato por 0:30 de margem de leitura; se a voz real passar de ~4:15 no fim do b19, encurtar o b19 (é síntese) em vez de cortar o b18.
- [x] Comporta/casas de bombas até ~8:00: b28 em 6:25.4, b29 em 6:34.2.
- [x] Ressalva do crivo: "quase um terço"/"cerca de 30%" na narração (sem "um terço" seco).
- [x] Fecho junta as camadas (b35-b36: chuva recorde + cheias anteriores + funil + saída lenta + defesa que cedeu) e atribuição WWA com as palavras certas (b37).
- [x] Sem previsão de nova enchente; sem "Isso nos leva às seguintes perguntas"; sem gancho de próximo vídeo.
- [x] A água não passou por cima do muro (b31, após ajuste atribui).
- [x] Várias falhas, nenhuma causa única (b28-b32, três causas atribuídas no b32).
- [ ] Pendente na etapa 2/QA: conferir na `legendas.srt` os tempos reais da frase-âncora (<0:30), 5 rios + "lago" + "quase um terço" (~1:00), funil (~4:00) e defesa (~8:00).
Duração total estimada: 9:46.3.
