# Revisão nativa ES: 009 Gestapo

Leitura 1: editor mexicano (neutro, "tú", público MX/US/AR). Leitura 2: editor espanhol (ES). Escopo: idioma, fala/TTS, sensibilidade (tema nazista), ritmo para quem só ouve. Fatos: só os que saltaram à vista (seção final); a checagem de fatos formal é da etapa de SOURCES.

## Nota geral: 7,5 / 10

O texto está limpo, seco e bem construído. Quase não há calcos grosseiros do português; os problemas concentram-se em (a) um fato falso na ponte do Eichmann, (b) palavras ambíguas só para o ouvido ("presa", "banco", "colonias", "ejecutan"), (c) vocabulário de perpetrador ("método", "operación", "el miedo eficaz", "sus presos") e (d) 6 a 8 frases longas demais para o Fish. Corrigido isso, sobe para 9.

## Mudanças obrigatórias (resumo)

1. **N045**: "Fue el primero... en Sudamérica" é falso (Priebke chegou à Argentina em 1948, antes de Eichmann). Trocar por "No fue el único. Ni el último."
2. **N050**: "Lo ejecutan" lê-se como "o matam". Usar "La aplican".
3. **N029 / N086 / N061**: ambiguidade só de ouvido: "presa" (= represa), "banco" (= bank), "casa de colonias" (no México, colonia = bairro).
4. **N063**: "operación" e "la colonia" usam o léxico do perpetrador; usar "redada" e "hogar infantil".
5. **N016, N049, N051, N004, N093, N072, N041, N042**: vocabulário de perpetrador/eufemismo ("método", "miedo eficaz", "aplica esa lección", "sus presos", "cliente", "se ocupa de los judíos", "deportación" sem explicar).
6. **N064**: "Casi todos los niños" está errado se for verdade que nenhum dos 44 voltou (verificar em SOURCES); no mínimo trocar por "Ninguno sobrevive".
7. **N059 / N065**: "lo que condenó a Barbie fue un papel" e "la prueba central" exageram (o julgamento teve dezenas de testemunhas). Suavizar.
8. **N089**: "Según la justicia y la prensa" sem fonte clara; atribuir a "investigaciones periodísticas y testimonios".
9. **N054, N081, N092, N016**: vírgula antes de "y" / vírgula entre sujeito e verbo.
10. **Frases longas (N039, N075, N079, N084, N100 e outras da tabela)**: dividir como sugerido.
11. **Glossário do Fish** (seção própria): aplicar só no texto enviado à voz.

## Tabela de correções

Legenda: **[OBR]** obrigatória, **[REC]** recomendada. "Sugestão" está pronta para colar em `roteiro.py` (números por extenso mantidos).

| Bloco | Original | Problema | Sugestão |
|---|---|---|---|
| N003 [REC] | Días después, lo expulsan a Francia. | Incoerente com N092 (o avião o deixa na Guiana Francesa). | Días después, lo expulsan del país, rumbo a Francia. |
| N004 [OBR] | Lo encierran en Lyon, en la cárcel de Montluc. Allí, cuarenta años antes, él encerraba a sus presos. | "sus presos": ponto de vista de quem prendeu; "él encerraba" atribui a Barbie o ato direto. | Lo encierran en Lyon, en la cárcel de Montluc. Allí, cuarenta años antes, la Gestapo encerraba a sus víctimas. |
| N005 [REC] | En Lyon no lo llamaban Altmann. Lo llamaban Klaus Barbie, jefe de la Gestapo. | Imprecisão: era chefe da Gestapo **em Lyon**; "lo llamaban" soa a apelido. | En Francia no era Altmann. Era Klaus Barbie, jefe de la Gestapo en Lyon. |
| N010 [REC] | No hace falta un juez. Tras el incendio del Reichstag, en febrero, un decreto permite la llamada custodia protectora. | Frase 2 com 17 palavras; "no hace falta" adota o ponto de vista de quem prende. | Ningún juez interviene. En febrero, tras el incendio del Reichstag, un decreto permite la llamada custodia protectora. |
| N011 [REC] | Es decir: encerrar a cualquiera sin cargos, sin abogado y sin fecha de salida. | "cualquiera" amplia demais; "Es decir:" seco mas ok. | Es decir: encerrar a un sospechoso sin cargos, sin abogado y sin fecha de salida. |
| N012 [REC] | En unos meses, decenas de miles de opositores, sobre todo comunistas y socialistas, pasan por sótanos, cuarteles y los primeros campos. | 21 palavras, difícil de ouvir; o número é do conjunto da repressão de 1933, não só da Gestapo. | En unos meses, decenas de miles de opositores pasan por sótanos, cuarteles y los primeros campos. Sobre todo, comunistas y socialistas. |
| N013 [OBR] | Pero esa policía es de Göring. Y otro hombre la quiere: el que sabe guardar fichas. | Para o ouvido são dois homens (outro hombre + el que guarda fichas); "sabe guardar fichas" soa a elogio de competência. | Pero esa policía es de Göring. Y Himmler la quiere. Con ella, quiere un fichero. |
| N014 [REC] | Göring cede la Gestapo a Heinrich Himmler, el jefe de las SS. | Ok; "el jefe" repete artigo, sem erro. | Göring cede la Gestapo a Heinrich Himmler, jefe de las SS. |
| N015 [REC] | Al frente pone a su número dos, Reinhard Heydrich, de treinta años, que venía del servicio de inteligencia de las SS. | 19 palavras; "venía del" impreciso. | Al frente pone a su número dos: Reinhard Heydrich, de treinta años. Dirigía el servicio de inteligencia de las SS. |
| N016 [OBR] | Su método es el papel. Cada opositor, cada sospechoso, cada rumor, termina en una ficha. | "Su método" = elogio de eficácia; vírgula entre sujeito e verbo; concordância. | Su herramienta es el papel. Cada opositor, cada sospechoso y cada rumor terminan en una ficha. |
| N017 [REC] | ...una ley prusiana decide que ningún tribunal puede revisar las órdenes de la Gestapo. | "decide": uma lei não decide (calco). | En febrero de mil novecientos treinta y seis, una ley prusiana dispone que ningún tribunal puede revisar las órdenes de la Gestapo. |
| N019 [REC] | ...un detective de Múnich que había pasado años persiguiendo comunistas. | "detective" é americanismo/ficção; em ES/MX soa a novela policial. | El trabajo diario queda en manos de Heinrich Müller, un policía de Múnich. Había pasado años persiguiendo comunistas. |
| N021 [REC] | La oficina de la Gestapo tiene veintidós funcionarios para casi un millón de habitantes. | 22 palavras; "casi un millón" parece inflado (Gellately fala em ~840 mil na Baixa Francônia: verificar). "funcionarios" inclui secretárias. | Würzburg, Baviera, mil novecientos treinta y siete. La Gestapo local tiene veintidós funcionarios. Deben vigilar a unos ochocientos mil habitantes. |
| N022 [REC] | ...El historiador Robert Gellately los estudió uno por uno. | "uno por uno" exagera (estudou uma amostra grande). | Muchos expedientes de esa oficina sobrevivieron. El historiador Robert Gellately los estudió a fondo. |
| N023 [REC] | Descubrió que muchos casos no empezaban con un espía. Empezaban con una carta o una visita: un ciudadano que denunciaba a otro. | 2ª frase com 16 palavras. | Descubrió que muchos casos no empezaban con un espía. Empezaban con una carta o una visita. Un ciudadano denunciaba a otro. |
| N025 [REC] | Una ley de diciembre de mil novecientos treinta y cuatro castiga hasta un comentario contra el régimen. | "hasta" ambíguo ao ouvido. | Una ley de diciembre de mil novecientos treinta y cuatro castiga incluso un comentario contra el régimen. |
| N027 [OBR] | No hacía falta vigilar a todos. Bastaba con que todos se vigilaran entre sí. | Generalização sem atribuição (a tese de Gellately é debatida); "no hacía falta" adota o ponto de vista da polícia; "todos... todos". | Según Gellately, no hacía falta vigilar a todos: muchos ciudadanos vigilaban a sus vecinos. |
| N028 [REC] | Y a veces, los presos llegaban de mucho más lejos. En barco, desde Sudamérica. | "los presos" no plural: o capítulo é sobre uma só mulher. | Y a veces, una presa llegaba de mucho más lejos. En barco, desde Sudamérica. |
| N029 [OBR] | La policía brasileña sube a una presa a un barco alemán, el La Coruña. | "una presa" = também represa/presa de caça; "sube a... a" confuso; "el La Coruña" estranho. | La policía brasileña embarca a una prisionera en un vapor alemán, el La Coruña. |
| N031 [REC] | Había llegado a Brasil con el líder comunista Luís Carlos Prestes, para preparar el levantamiento de mil novecientos treinta y cinco, que fracasó. | 24 palavras; grafia portuguesa "Luís". | Había llegado a Brasil con el líder comunista Luis Carlos Prestes. Preparaban el levantamiento de mil novecientos treinta y cinco. Fracasó. |
| N032 [OBR] | El gobierno de Getúlio Vargas decide entregarla a Alemania. El Supremo Tribunal Federal rechaza el recurso para salvarla. | "el recurso" é vago; termo exato é habeas corpus; "Getúlio" com acento pt. | El gobierno de Getulio Vargas decide entregarla a Alemania. El Supremo Tribunal Federal rechaza el hábeas corpus que pedía impedirlo. |
| N033 [REC] | Según el biógrafo Fernando Morais, la policía de Filinto Müller y la Gestapo intercambiaban información sobre los comunistas. | 20 palavras; Müller repete o sobrenome de Heinrich Müller (confusão para quem ouve). | Según el biógrafo Fernando Morais, la policía de Río y la Gestapo intercambiaban información sobre los comunistas. La policía de Río estaba bajo el mando de Filinto Müller. |
| N035 [REC] | A los catorce meses, la abuela consigue llevársela. Olga nunca sale. | "la abuela": de quem?; "nunca sale" ambíguo. | A los catorce meses, la abuela paterna consigue llevársela. Olga no vuelve a ser libre. |
| N036 [OBR] | En mil novecientos cuarenta y dos es asesinada con gas en Bernburg, uno de los centros de exterminio del régimen. | "centro de exterminio" evoca os campos da Shoah; Bernburg era centro de "eutanásia" nazista (T4/14f13): impreciso. | En mil novecientos cuarenta y dos la asesinan con gas en Bernburg. Era un centro donde el régimen mataba a enfermos y a presos. |
| N037 [OBR] | Para entonces, la Gestapo ya no era solo una policía. Era una oficina con alcance en todo un continente. | "oficina con alcance" = calco do inglês (reach) e falso amigo; salta a 1942 e o capítulo seguinte volta a 1939. | Pronto, la Gestapo dejará de ser solo una policía alemana. Pasará a ser pieza de una maquinaria que abarca toda Europa. |
| N038 [REC] | La guerra lleva tres semanas. | De 1 a 27 de setembro são casi cuatro semanas. | La guerra lleva casi un mes. |
| N039 [OBR] | Himmler une la Gestapo, la policía criminal y el servicio de inteligencia de las SS en un solo organismo: la Oficina Central de Seguridad del Reich. La dirige Heydrich. | 1ª frase com ~27 palavras: impossível de ouvir. | Himmler junta tres cuerpos en uno solo. La Gestapo, la policía criminal y el servicio de inteligencia de las SS. Nace la Oficina Central de Seguridad del Reich. La dirige Heydrich. |
| N041 [OBR] | Dentro, una sección pequeña, la IV B4, se ocupa de los judíos. La dirige Adolf Eichmann. | "se ocupa de los judíos" = eufemismo burocrático; "IV B4" o TTS lê "I V B cuatro". | Dentro, una sección pequeña, la cuatro be cuatro, organiza la persecución de los judíos. La dirige Adolf Eichmann. |
| N042 [OBR] | Desde ahí se organizan las listas y los trenes de la deportación de los judíos de Europa. | "deportación" é eufemismo: ouvinte pode não entender que era para a morte. | Desde ahí se organizan las listas y los trenes. Llevan a los judíos de Europa a los campos de exterminio. |
| N044 [REC] | Vive diez años en Argentina, hasta que el Mossad lo atrapa en mil novecientos sesenta. Esa operación ya está en nuestro expediente del Mossad. | 2ª frase com 15 palavras e repetição "Mossad"; "atrapa" é coloquial. | Vive diez años en Argentina, hasta que el Mossad lo captura en mil novecientos sesenta. Esa operación ya la contamos en nuestro expediente del Mossad. |
| N045 [OBR] | Fue el primero de los hombres de la Gestapo en Sudamérica. No el último. | **Fato falso:** Priebke chegou à Argentina em 1948, antes do Eichmann (1950). | No fue el único hombre de la Gestapo en Sudamérica. Ni el último. |
| N046 [REC] | Por orden de Hitler, el mariscal Wilhelm Keitel firma el decreto Noche y Niebla. | 21 palavras no bloco, ok se for dividido. | Siete de diciembre de mil novecientos cuarenta y uno. Por orden de Hitler, el mariscal Wilhelm Keitel firma el decreto Noche y Niebla. |
| N047 [REC] | En Francia, Bélgica y Holanda, los sospechosos de resistencia son llevados en secreto a Alemania. | "sospechosos de resistencia" é calco; o decreto valia para mais países. | En Francia, Bélgica, Holanda y otros países ocupados, los sospechosos de pertenecer a la resistencia son llevados en secreto a Alemania. |
| N049 [OBR] | Keitel lo escribe: el miedo eficaz se logra cuando la familia no sabe qué pasó con el detenido. | "miedo eficaz" e "se logra" = a voz do perpetrador e calco ("is achieved"); parece aprovação do cálculo. | La propia orden de Keitel explica su lógica: sembrar el terror. Que la familia no sepa qué pasó con el detenido. |
| N050 [OBR] | Lo ejecutan la Gestapo y la policía de seguridad. Según los historiadores, unas siete mil personas desaparecen así. | "ejecutan" = também "matam": ambíguo ao ouvido e erra o sentido. | La aplican la Gestapo y la policía de seguridad. Según los historiadores, unas siete mil personas desaparecen así. |
| N051 [OBR] | En una ciudad francesa, un oficial de veintinueve años aplica esa lección. | "aplica esa lección" = adota o ponto de vista de quem aprende com o decreto (e soa a mérito). | En una ciudad francesa, un oficial de veintinueve años usa esa misma lógica del terror. |
| N052 [REC] | ...Los alemanes ocupan el sur de Francia. La Gestapo se instala en el Hotel Terminus, junto a la estación. | 1ª frase do bloco ok; só marcar que o capítulo tem 3 frases seguidas longas. | El Hotel. Lyon, noviembre de mil novecientos cuarenta y dos. Los alemanes ocupan el sur de Francia. La Gestapo se instala en el Hotel Terminus, junto a la estación. |
| N053 [REC] | Al frente de su sección cuatro está Klaus Barbie. | "su sección cuatro" sem referente claro. | La sección cuatro, la de la Gestapo, queda a cargo de Klaus Barbie. |
| N054 [OBR] | Había entrado en el servicio de inteligencia de las SS en mil novecientos treinta y cinco, y pasado por Ámsterdam persiguiendo a judíos y opositores. | Vírgula antes de "y"; auxiliar elidido soa estranho; 22 palavras. | Había entrado en el servicio de inteligencia de las SS en mil novecientos treinta y cinco. Antes de Lyon, estuvo en Ámsterdam, donde persiguió a judíos y opositores. |
| N055 [REC] | En Lyon persigue a la Resistencia. El veintiuno de junio de mil novecientos cuarenta y tres, sus hombres irrumpen en una casa de Caluire. | "sus hombres" possessivo; ok mas 24 palavras. | En Lyon persigue a la Resistencia. El veintiuno de junio de mil novecientos cuarenta y tres, agentes a sus órdenes irrumpen en una casa de Caluire. |
| N057 [OBR] | Moulin muere semanas después tras los interrogatorios, sin dar un solo nombre. | "interrogatorios" é o eufemismo da própria Gestapo; foram duas semanas, não "semanas". | Moulin muere dos semanas después, a consecuencia de las torturas. No dio ningún nombre. |
| N058 [OBR] | Según los testimonios reunidos para su juicio, Barbie dirigía los interrogatorios en persona. Los sobrevivientes lo llamaron el Carnicero de Lyon. | De novo "interrogatorios" (eufemismo). | Según los testimonios reunidos para su juicio, Barbie torturaba en persona a los detenidos. Los sobrevivientes lo llamaron el Carnicero de Lyon. |
| N059 [OBR] | Si te gustan estos expedientes, suscríbete. Porque lo que condenó a Barbie no fue un interrogatorio. Fue un papel. | "Porque" não se liga ao CTA; afirmação exagerada (foram dezenas de testemunhas); "interrogatorio" de novo. | Si te gustan estos expedientes, suscríbete. Y una de las pruebas más importantes contra Barbie no fue un testigo. Fue un papel. |
| N060 [REC] | Izieu, un pueblo en las montañas al este de Lyon. Seis de abril de mil novecientos cuarenta y cuatro, por la mañana. | "montañas" exagera (estribações do Bugey). | Izieu, un pueblo al este de Lyon, al pie de las montañas. Seis de abril de mil novecientos cuarenta y cuatro, por la mañana. |
| N061 [OBR] | En una casa de colonias viven escondidos niños judíos. | "casa de colonias": en MX colonia = barrio (ouvinte entende "casa de barrios"). | En un hogar infantil viven escondidos niños judíos. |
| N062 [REC] | Llegan camiones. Se llevan a cuarenta y cuatro niños y a siete adultos. | Falta o agente: "se llevan" apaga quem prende. | Llegan camiones. Son agentes de la Gestapo de Lyon. Se llevan a cuarenta y cuatro niños y a siete adultos. |
| N063 [OBR] | Esa noche, Barbie firma un télex para París. Informa de la operación contra la colonia de Izieu. | "operación" e "colonia" = linguagem do perpetrador; "esa noche" sem fonte. | Ese mismo día, Barbie firma un télex para París. Informa de la redada en el hogar infantil de Izieu. |
| N064 [OBR] | Casi todos los niños son deportados a Auschwitz y asesinados. De los adultos, sobrevive una mujer. | Se nenhum dos 44 sobreviveu (verificar SOURCES), "casi todos" subestima; Zlatin e 2 adolescentes foram para a Estônia, não Auschwitz. | Los niños son deportados, casi todos a Auschwitz. Ninguno sobrevive. De los siete adultos, sobrevive solo una mujer. |
| N065 [REC] | El télex queda en los archivos. Décadas después, será la prueba central contra él. | "la prueba central" exagera, e N095 diz que "está entre las pruebas". | El télex queda en los archivos. Décadas después, será una de las pruebas centrales contra él. |
| N066 [REC] | Pero primero, la Gestapo tiene que perder la guerra. | "Pero primero" = calco de "But first". | Pero antes, la Gestapo tiene que perder la guerra. |
| N067 [REC] | Primavera de mil novecientos cuarenta y cinco. En toda Alemania, las oficinas de la Gestapo queman sus archivos. | "primavera" é outono para AR; "oficinas" = sedes. | Abril de mil novecientos cuarenta y cinco. En toda Alemania, la Gestapo quema sus archivos. |
| N068 [REC] | En los últimos días, sus agentes asesinan a presos en sus propias cárceles. | "sus... sus propias" repetido. | En los últimos días, agentes de la Gestapo asesinan a presos en las cárceles de la propia policía. |
| N069 [REC] | Himmler se envenena tras ser capturado por los británicos. Heinrich Müller desaparece en Berlín y nunca lo encuentran. | "se envenena" é eufemismo; "nunca lo encuentran" afirma mais do que se sabe (há cova disputada). | Himmler se suicida con cianuro tras ser capturado por los británicos. Heinrich Müller desaparece en Berlín. Su destino sigue sin aclararse. |
| N070 [REC] | ...el tribunal internacional declara a la Gestapo organización criminal. | Nome incompleto. | En Núremberg, en mil novecientos cuarenta y seis, el Tribunal Militar Internacional declara a la Gestapo organización criminal. |
| N071 [REC] | ...Muchos vuelven a ser policías en Alemania Occidental. | Afirmação sem atribuição. | Pero condenar a una organización no es juzgar a sus hombres. La mayoría nunca pisa un tribunal. Según los historiadores, muchos vuelven a ser policías en Alemania Occidental. |
| N072 [OBR] | Y algunos encuentran un cliente nuevo: los Estados Unidos. | "cliente" normaliza (óptica comercial); acusação ao governo sem atribuição (a atribuição vem em N075, depois). | Y a algunos, el Ejército de Estados Unidos les ofrece trabajo. |
| N075 [OBR] | Según un informe del Departamento de Justicia de Estados Unidos, de mil novecientos ochenta y tres, sus agentes lo protegieron, ocultaron a Francia dónde estaba y lo ayudaron a escapar. | 28 palavras; "sus agentes" ambíguo; vírgulas. | Un informe del Departamento de Justicia de Estados Unidos, de mil novecientos ochenta y tres, lo reconoce. Agentes del Ejército lo protegieron. Ocultaron a Francia su paradero. Y lo ayudaron a escapar. |
| N076 [REC] | En mil novecientos cincuenta y uno, le consiguen documentos con otro nombre. | Sujeito oculto. | En mil novecientos cincuenta y uno, esos mismos agentes le consiguen papeles con otro nombre. |
| N079 [OBR] | El paso lo arregla en Roma un sacerdote croata, Krunoslav Draganović, que ya había sacado de Europa a otros fugitivos. Es la llamada ruta de las ratas. | 22 palavras; "arregla" em MX = consertar. | El viaje lo organiza en Roma un sacerdote croata, Krunoslav Draganović. Ya había ayudado a escapar de Europa a otros fugitivos. Es la llamada ruta de las ratas. |
| N080 [REC] | De Buenos Aires sigue a Bolivia. | "sigue a" é calco. | De Buenos Aires viaja a Bolivia. En mil novecientos cincuenta y siete recibe la nacionalidad boliviana. |
| N081 [OBR] | Tiene un aserradero, luego una naviera, y trato con ministros y generales. | Vírgula antes de "y"; "tiene... trato" soa a história de sucesso. | Monta un aserradero y, años después, una naviera. Se relaciona con ministros y generales, bajo un nombre falso. |
| N082 [REC] | Según investigaciones posteriores, asesoró a los servicios de seguridad de varios gobiernos militares. | Fonte vaga. | Según investigaciones posteriores, asesoró a los servicios de seguridad de varios gobiernos militares. Esa es la versión de periodistas y de la justicia francesa. |
| N083 [OBR] | Durante veinte años, nadie en Bolivia pregunta por su pasado. Hasta que alguien en Europa compara dos fotos. | "nadie" é falso (houve quem soubesse); "alguien" impreciso. | Durante veinte años, casi nadie pregunta por su pasado. Hasta que, en Europa, una pareja compara dos fotos. |
| N084 [OBR] | ...Beate y Serge Klarsfeld, una pareja que persigue a criminales nazis, consiguen una foto reciente de Klaus Altmann. | 21 palavras; "persigue" é o verbo da perseguição nazista: confunde. | La Foto. Mil novecientos setenta y uno. Beate y Serge Klarsfeld buscan criminales nazis. Consiguen una foto reciente de Klaus Altmann. |
| N085 [REC] | La comparan con las del oficial de Lyon. | "las" sem antecedente. | La comparan con las fotos del oficial de Lyon. Para los expertos que la examinan, es el mismo hombre. |
| N086 [OBR] | Beate viaja a Bolivia. En mil novecientos setenta y dos se encadena a un banco en el centro de La Paz para exigir que lo entreguen. | "banco" ao ouvido = instituição financeira. | Beate viaja a Bolivia. En mil novecientos setenta y dos se encadena a un banco de plaza, en el centro de La Paz. Exige que entreguen a Altmann a Francia. |
| N087 [REC] | El gobierno del general Hugo Banzer se niega. | Falta contexto (ditadura). | El régimen militar del general Hugo Banzer se niega. |
| N088 [REC] | «Yo he olvidado. Si ellos no han olvidado, es asunto suyo». | Pretérito perfecto composto é de Espanha; em LatAm "olvidé". Confirmar que é tradução fiel da fonte. | A un periodista le dice: «Yo ya olvidé. Si ellos no olvidaron, es problema suyo». |
| N089 [OBR] | En mil novecientos ochenta, un golpe lleva al poder al general Luis García Meza. Según la justicia y la prensa, Altmann ayudó a organizar a los paramilitares del golpe. | "la justicia" sem fonte clara. | En mil novecientos ochenta, un golpe militar lleva al poder al general Luis García Meza. Según investigaciones periodísticas y testimonios posteriores, Altmann ayudó a organizar a los paramilitares del golpe. |
| N091 [REC] | El nuevo gobierno detiene a Altmann por la deuda. | "la deuda" ainda não foi apresentada neste ponto. | El nuevo gobierno detiene a Altmann por aquella deuda con el Estado. |
| N092 [OBR] | El cuatro de febrero lo expulsa del país. Un avión lo deja en la Guayana Francesa, y de ahí lo llevan a Lyon. | Vírgula antes de "y"; sujeito de "expulsa" ausente. | El cuatro de febrero, el gobierno lo expulsa del país. Un avión lo deja en la Guayana Francesa y de ahí lo llevan a Lyon. |
| N093 [OBR] | Vuelve a Montluc, la cárcel donde la Gestapo encerraba a sus presos en mil novecientos cuarenta y tres. | "sus presos" (ver N004). | Vuelve a Montluc, la misma cárcel donde la Gestapo encerró a sus víctimas en mil novecientos cuarenta y tres. |
| N095 [REC] | Mayo de mil novecientos ochenta y siete. Juicio en Lyon. Durante semanas declaran sobrevivientes. El télex de Izieu está entre las pruebas. | Ok; acrescentar sobreviventes e famílias para equilibrar o "papel". | Mayo de mil novecientos ochenta y siete. Juicio en Lyon. Durante semanas declaran sobrevivientes y familiares de las víctimas. El télex de Izieu está entre las pruebas. |
| N098 [REC] | Un equipo de la televisión estadounidense aborda en la calle a un anciano. | "la televisión estadounidense" vago; "aborda" ok. | Un equipo de televisión de Estados Unidos aborda en la calle a un anciano. |
| N099 [REC] | Es Erich Priebke, de ochenta años. Hace décadas que vive allí y preside la asociación que dirige el colegio alemán de la ciudad. | 2ª frase com 20 palavras. | Es Erich Priebke, de ochenta años. Hace décadas que vive allí. Preside la asociación que dirige el colegio alemán de la ciudad. |
| N100 [OBR] | En mil novecientos cuarenta y cuatro era capitán de la policía de seguridad de las SS en Roma, en la oficina de la calle Tasso que los romanos llamaban la Gestapo. | 29 palavras; "oficina" = sede. | En mil novecientos cuarenta y cuatro, era capitán de la policía de seguridad de las SS en Roma. Trabajaba en la sede de la calle Tasso. Los romanos la llamaban la Gestapo. |
| N101 [OBR] | Ante la cámara admite que participó en la masacre de las Fosas Ardeatinas: trescientos treinta y cinco civiles fusilados como represalia. | "civiles" impreciso (muitos eram presos e militares); "como represalia" sem explicar adota o enquadramento nazista. | Ante la cámara admite que participó en la matanza de las Fosas Ardeatinas. Trescientos treinta y cinco hombres, fusilados en represalia por un atentado partisano. |
| N102 [REC] | ...Muere en Roma en dos mil trece, con cien años. | "con cien años" é calco. | Argentina lo extradita a Italia en mil novecientos noventa y cinco. Lo condenan a cadena perpetua, que cumple en arresto domiciliario. Muere en Roma en dos mil trece, a los cien años. |
| N103 [REC] | Hombres de la Gestapo vivieron décadas en Sudamérica. A uno de ellos, al final, lo atrapó una deuda. | Simplifica: a dívida foi o motivo legal; Priebke era da polícia de segurança (SD/Sipo). | Hombres de la Gestapo y de su policía de seguridad vivieron décadas en Sudamérica. A uno de ellos, al final, lo detuvo una deuda. |
| N104 [REC] | A Klaus Altmann lo detuvieron por deberle dinero al Estado boliviano. | Passado, enquanto o resto é presente histórico. | A Klaus Altmann lo detienen por deberle dinero al Estado boliviano. |
| N105 [OBR] | Francia le cobró la otra cuenta: la de Lyon y la de Izieu. | "cobrar la cuenta" trivializa o assassinato de crianças ao transformá-lo em dívida. | Pero la cuenta pendiente era otra. Francia lo juzgó por Lyon y por Izieu. |
| N106 [OBR] | La Gestapo nunca tuvo muchos agentes. Tuvo vecinos que hablaban. Y después, gobiernos que callaban. | Generaliza "gobiernos que callaban" (EUA protegeu ativamente; outros olharam para o lado) e não atribui. | La Gestapo nunca tuvo muchos agentes. Tuvo vecinos que hablaban. Y después, algunos gobiernos que protegieron o miraron hacia otro lado. |
| N107 [REC] | ¿Cuál de estos expedientes te sorprendió más? | "sorprendió" é leve para vítimas. | Y tú, ¿sabías que hombres de la Gestapo vivieron décadas en Sudamérica? ¿Cuál de estos expedientes te marcó más? Déjalo en los comentarios. |

## Pronúncia para o Fish (glossário)

Aplicar **só no texto enviado à voz** (substituição por regex no `blocos.json` → `tts_fish.py`); o roteiro e as legendas ficam com a grafia correta. Regra: grafia hispânica, acento onde cai a tônica, "j" para o /x/ alemão.

| Texto do roteiro | Texto para a voz | Obs. |
|---|---|---|
| Geheime Staatspolizei | Gue-jái-me Shtáats-po-li-tsái | dividir em sílabas se o Fish engolir |
| Gestapo | Gestapo | já sai bem |
| Prinz Albrecht | Prints Álbrejt | |
| Reichstag | Ráiksstag | |
| Reich | Raik | em "Oficina Central de Seguridad del Reich" |
| Göring | Guéring | sem "ö": evita "Goring" |
| Himmler | Jímler | evita "Imler" |
| Heydrich | Jáidrik | |
| Reinhard | Ráinjart | |
| Heinrich | Háinrik | |
| Müller (Gestapo e Filinto) | Míler | |
| Hitler | Hítler | deixar; o espanhol lê "Ítler" e está certo |
| Keitel | Káitel | |
| Wilhelm | Vílhelm | |
| Eichmann | Áikman | |
| Klement | Klémen | |
| Mossad | Mosád | evita tônica no "Mó" |
| Würzburg | Vúrtsburk | |
| Gellately | Yélatli | |
| Bernburg | Bérnburk | |
| La Coruña | La Coruña | ok |
| Benário | Benario | grafia espanhola |
| Luís Carlos Prestes | Luis Carlos Préstes | |
| Getúlio | Jetúlio | |
| Filinto | Filínto | |
| Lyon | Lión | |
| Montluc | Monlúk | |
| Caluire | Kaluír | |
| Jean Moulin | Yan Mulán | |
| De Gaulle | De Gol | |
| Izieu | Isié | com "s" (sem "z" de Espanha) |
| Barbie | Bárbie | deixar; esperado em espanhol |
| Altmann | Áltman | |
| Auschwitz | Áushvits | |
| IV B4 (já mudado no texto) | cuatro be cuatro | |
| las SS | las ese ese | |
| Krunoslav Draganović | Krunóslav Draganóvich | |
| Klarsfeld | Klársfelt | |
| Serge | Sérj | |
| Beate | Beáte | |
| Banzer | Bánser | em AR/MX; deixar |
| García Meza | García Meza | ok |
| Priebke | Príbke | |
| Erich | Érik | |
| Bariloche | Bariloche | ok |
| Ardeatinas | Ardeatinas | ok |
| télex | téleks | |
| Núremberg | Núremberg | ok |

Notas de voz:
- Os números por extenso já estão certos; manter.
- Evitar travessão e parênteses no texto da voz.
- Depois de gerar, conferir com Whisper o nome "Gestapo" e "Klaus Barbie" (se o Fish disser "Barbi" duas sílabas curtas está certo).
- "Moulin" e "De Gaulle" têm alto risco de leitura em inglês; testar um bloco de amostra antes do lote.

## Sensibilidade (tema nazista)

**Vocabulário de perpetrador encontrado** (sempre trocar):

| Termo | Onde | Troca |
|---|---|---|
| "método" | N016 | "herramienta" |
| "el miedo eficaz se logra" | N049 | falar de "terror" e atribuir à ordem |
| "aplica esa lección" | N051 | "usa esa misma lógica del terror" |
| "operación" / "colonia" | N063 | "redada" / "hogar infantil" |
| "interrogatorios" | N057, N058, N059 | "torturas" / "torturaba" |
| "sus presos", "sus hombres", "sus agentes" | N004, N055, N068, N093 | "sus víctimas", "agentes a sus órdenes" |
| "se ocupa de los judíos" | N041 | "organiza la persecución de los judíos" |
| "deportación" | N042 | explicar: "llevan a los judíos a los campos de exterminio" |
| "cliente" | N072 | "les ofrece trabajo" |
| "cobrar la cuenta" | N105 | "juzgó por Lyon y por Izieu" |
| "ejecutan" | N050 | "aplican" (ambiguidade) |
| "fusilados como represalia" | N101 | "en represalia por un atentado partisano" |

**Eufemismos nazistas sem explicação:** "custodia protectora" está explicada (N011, bom); "Noche y Niebla" está explicado (N047-N048, bom); "deportación" (N042) e "interrogatorios" não. "Policía de seguridad" e "ruta de las ratas" (N079) são ok no contexto.

**Frases que podem soar a admiração:** N013 ("el que sabe guardar fichas"), N016 ("su método es el papel"), N081 ("Tiene un aserradero, luego una naviera... trato con ministros y generales": parece trajetória de empresário), N020 ("Con tanto poder, uno imagina un ejército de agentes": ok, é crítica ao mito). Todas já com sugestão.

**Acusações a governos e serviços sem atribuição suficiente:**
- EUA: N072 ("cliente nuevo") sem fonte (a fonte só vem em N075) e N094 ok (reconoce y pide disculpas). N075 está bem atribuída; só encurtar.
- Bolívia: N082 ("Según investigaciones posteriores") vago; N089 ("la justicia") sem fonte; N083 ("nadie en Bolivia").
- Brasil: N032 e N033 estão bem (Morais atribuído; STF e hábeas corpus são fatos documentados). Usar "hábeas corpus".
- Argentina: N097 ("Argentina tenía a otro") e N106 ("gobiernos que callaban") insinuam cumplicidade sem fato. Ajustado em N106; N097 pode ficar "Argentina albergaba a otro", ou, melhor, "En Argentina vivía otro".
- Alemania Occidental: N071 sem atribuição ("Según los historiadores").
- Francia, De Gaulle: sem problema.

**Contra-balanço de vítimas:** o roteiro tem boas cenas de vítimas (Olga, Izieu). Dois ajustes: N064 deixa claro que "ninguno sobrevive", e N095 inclui familiares. O cierre (N105-N107) deve terminar em vítimas e responsabilidade, não em ironia ("cobró la cuenta"; "atrapó una deuda").

## Fatos a checar na etapa de SOURCES (não alterados aqui)

1. **N045**: Priebke chegou à Argentina em 1948 (antes do Eichmann). Já corrigido na sugestão.
2. **N064**: composição dos deportados de Izieu (44 crianças, 7 adultos; Zlatin e 2 adolescentes fuzilados na Estônia; só uma adulta sobrevive; nenhuma criança).
3. **N021**: população de Würzburg/Baixa Francônia (~840 mil?) e número exato de funcionários na Gellately.
4. **N036**: Bernburg era centro de "eutanásia"/14f13; checar descrição.
5. **N005 / N053**: Barbie era chefe da Seção IV (Gestapo) do Sipo-SD de Lyon, não "da Gestapo" em geral.
6. **N057**: Moulin morreu em 8 de julho de 1943, a bordo de um trem; Barbie não foi condenado pela morte dele (prescrição): manter "según testimonios".
7. **N065 / N095**: peso do télex no julgamento (dezenas de testemunhas; sentença por crimes contra a humanidade).
8. **N088**: citação de Altmann: confirmar texto e fonte ("Yo he olvidado...").
9. **N089**: papel de Altmann no golpe de 1980 e a fonte (jornalística x judicial).
10. **N101**: perfil das 335 vítimas (civis, presos políticos, 75 judeus, alguns militares).
11. **N012**: "decenas de miles" refere-se ao conjunto da repressão de 1933, não só à Gestapo.
