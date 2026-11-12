# Material público livre por tema: lugares e arquivos de guerra americanos

Levantamento de 12/11/2026, feito com APIs públicas gratuitas (custo US$ 0). Os dados brutos estão em `material.json` e os scripts em `scripts/`. Para refazer: `contar.py` → `candidatos.py` → `commons_busca.py` → `itens_chave.py` → `juntar.py` → `secao_temas.py`.

## Resumo executivo

**Regra do canal:** a pauta nasce do material. Este é o ranking dos temas pela nota "material farto e livre" (0–5). A nota junta a época (fotos e filmes da NARA, fotos do NHHC, arquivos da LoC no Commons) e o "hoje" (DVIDS e categorias do Commons), mais um ajuste manual explicado na tabela.

| # | Tema | Nota | Por quê, em uma linha |
|---|---|---|---|
| 1 | Nevada Test Site | 5 | 22 mil fotos NNSA/DOE na NARA, filmes do DOE no IA, visitas guiadas mensais |
| 2 | Pearl Harbor / USS Arizona | 5 | O maior acervo de todos. O risco é não ser original |
| 3 | Okinawa (1945) | 5 | 4.800 fotos e 880 filmes na NARA, e o "hoje" DVIDS mais forte (bases ativas) |
| 4 | Iwo Jima | 5 | 2.400 fotos e 620 filmes na NARA, *To the Shores of Iwo Jima*, DVIDS. O concorrente já fez |
| 5 | Guadalcanal | 5 | 1.450 fotos na NARA, 419 no NHHC, DVIDS (DPAA) |
| 6 | Gettysburg | 4.5 | LoC (Gardner/O'Sullivan) e NPS. Sem filme, só foto |
| 7 | Antietam | 4.5 | Fotos de Gardner (LoC) e NPS |
| 8 | Bikini / Crossroads | 4.5 | Filmes oficiais e 270 rolos na NARA. O "hoje" é fraco |
| 9 | Peleliu | 4.5 | *Fury in the Pacific*, 152 filmes na NARA, DVIDS |
| 10 | Kwajalein | 4 | 830 fotos na NARA e DVIDS do Reagan Test Site |
| 11 | Fort Sumter | 4 | LoC (868 no Commons) e NPS |
| 12 | Midway Atoll | 4 | Filmes de John Ford, 80-G em ~6.000 px, USFWS em PD (o melhor "então × agora") |
| 13 | Tinian | 4 | 509th/Enola Gay, *The Last Bomb*, DVIDS forte em North Field |
| 14 | Hanford / B Reactor | 4 | DOE e NPS (Manhattan Project NHP) |
| 15 | Omaha / Pointe du Hoc | 4 | Signal Corps, USCG, NPC, DVIDS. A iconografia famosa é IWM ou Capa/Magnum (NÃO usar) |

**Os 4 candidatos a piloto, só pelo material:**

| Candidato | Itens concretos | Então × agora | Doc legível | "Hoje" livre | Veredito |
|---|---|---|---|---|---|
| **Midway Atoll** | **25** | 2 pares fortes (hangar 1942 × 2022; aérea 1941 × ISS) | Relatório CINCPAC (Nimitz), track chart | USFWS + DVIDS + NASA, tudo PD | **Melhor em material** |
| **Tinian** | **24** | 2 pares (poço da bomba 1945 × 2020; desembarque 1944 × 2012) | Relatório de captura; notas do copiloto do Enola Gay | DVIDS forte, PD | 2º, muito perto |
| **Bikini Atoll** | **20** | 1 par (frota 1946 × Landsat 2001) | Relatório final do JCS sobre Crossroads | Fraco: Landsat e relatório NPS de 1991 | Época excelente, "hoje" pobre |
| **Corregidor** | **21** | 1 par (Malinta 1942 × 2011, CC BY) | Mapas SWPA D+1…D+13 | Quase tudo CC BY / CC BY-SA | Funciona, mas dá mais trabalho de crédito |

**Fontes que pedem cuidado:**
- **IWM:** proibido (licença grátis só não comercial).
- **AP/Rosenthal:** contestado. Fora da thumb.
- **Commons CC BY-SA:** share-alike. Usar isolado, com crédito, ou evitar.
- **Internet Archive:** a licença declarada é do uploader. Há filme de Hollywood pirata lá (ex.: *Birdman of Alcatraz*, *Gettysburg* de 1993).
- **Prelinger/Periscope Film:** versões HD com dono. Risco de Content ID.
- **NARA "Restricted - Possibly"/"Undetermined":** conferir. Inclui cinejornais comerciais doados.
- **Fotos japonesas de época** (Hashima, rendição de Corregidor): sem PD automático nos EUA.

**Fontes que não deu para contar a partir da VPS:**
- **loc.gov / Chronicling America:** Cloudflare 403, inclusive via WARP e WebFetch.
- **DVIDS:** a busca web está atrás de um WAF e a API exige `api_key` (gratuita, com cadastro; pedir ao Rodrigo se quiser contagem real).
- **Smithsonian:** a DEMO_KEY dá 10 requisições por hora, então só os candidatos foram contados.
- **No lugar delas:** contei os arquivos do Commons cuja fonte é `dvidshub` ou `loc.gov`. Isso mede a presença e subestima o acervo real.

## Método e limites (leia antes de comparar números)

- **NARA:** usei o endpoint público do catálogo (`catalog.archives.gov/proxy/records/search`), só itens **online**, com agregação por tipo. A API v2 oficial exige `x-api-key`. O proxy aceita `limit` de 1, 10, 20, 50 ou 100 (outros valores devolvem HTML). Com várias frases, os números são a soma frase a frase, ou seja, um teto que pode duplicar. Os números "textual" são inflados por fichas individuais (fichas de serviço, logbooks, censo). Por isso a nota usa fotos e filmes, não textos.
- **Commons:**
  - "cat." = arquivos diretos mais subcategorias de 1 nível das categorias do tema.
  - "DVIDS" e "LoC" = busca por frase com `insource:dvidshub` / `insource:"loc.gov"`.
  - Frases genéricas pegam ruído: "Iwo Jima" pega o navio USS Iwo Jima, "Antietam" o USS Antietam, "Truk" pega "truck".
- **Internet Archive:** contei `title/subject/description`, mediatype movies, image ou texts. A contagem inclui uploads de terceiros com copyright. Os itens-chave usam só coleções de governo, cinejornal e Prelinger.
- **NHHC:** é a busca JSON do site, sem frase exata. Os totais de termos genéricos ("Area 51", "Camp Century") são ruído. "NHHC fotos" usa o filtro `docType=photograph`.
- **Resolução conferida em 3 amostras da NARA** (pasta `amostras/`, fora do git):
  - 80-G-414423: 5855×4882.
  - 127-GR-131-88112: 6315×5030.
  - Mapa SWPA de Corregidor: 6752×6019.
  - Conclusão: as séries 80-G, 127-GR e cartográficas digitalizadas vêm em ~6.000 px.

## Licença por fonte

| Fonte | Licença | Crédito exigido | Risco | Prova (página oficial) |
|---|---|---|---|---|
| **NARA** | Obra federal = PD. Doações podem ter restrição. Vale o campo *Use Restriction* do registro | Não exigido; praxe "National Archives" | Baixo se **Unrestricted**. "Restricted - Possibly"/"Undetermined" = conferir (cinejornais comerciais, doações) | [archives.gov/global-pages/privacy.html](https://www.archives.gov/global-pages/privacy.html) ("Generally, materials produced by Federal agencies are in the public domain"); [campo Use Restriction](https://www.archives.gov/research/catalog/lcdrg/elements/use.html) |
| **Library of Congress** | Por coleção e item. A LoC em geral não é dona. "No known restrictions" ≠ garantia de PD | A linha de crédito do registro | Médio. Conferir o *Rights Advisory* de cada item | [loc.gov/legal](https://www.loc.gov/legal/) ("we generally do not own the rights…") |
| **DVIDS** | "In general, all content on DVIDS is in the Public Domain". Vale o rodapé de cada item | Byline (pedido), sem sugerir endosso | Baixo a médio: música de terceiros em vídeos, itens de contratados | [dvidshub.net/about/faq](https://www.dvidshub.net/about/faq); [about/copyright](https://www.dvidshub.net/about/copyright) |
| **NHHC** | Maioria PD. As exceções vêm marcadas | "Naval History and Heritage Command" (NH); 80-G = "National Archives" | Baixo. "Courtesy of" = doação, conferir | [history.navy.mil/our-collections/photography.html](https://www.history.navy.mil/our-collections/photography.html) ("Most of the photos… are in the public domain") |
| **NPS** | PD salvo indicação | "National Park Service" (pedido) | Baixo. Fotos creditadas a terceiros; o logo da flecha é protegido | [nps.gov/aboutus/disclaimer.htm](https://www.nps.gov/aboutus/disclaimer.htm) |
| **USFWS** | PD o que a FWS produz | "USFWS / fotógrafo" | Baixo. Conferir o campo de direitos | [fws.gov/disclaimer](https://www.fws.gov/disclaimer) |
| **Wikimedia Commons** | **Por arquivo** | CC BY/BY-SA: autor + licença + link | **CC BY-SA**: share-alike (o vídeo pode herdar). Evitar ou usar isolado e inalterado. Os metadados às vezes erram: conferir na fonte | [Commons:Reusing content outside Wikimedia](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia) |
| **Internet Archive** | O upload **não** muda os direitos. A licença é declarada pelo uploader | A da fonte original | Alto fora de item de governo | [archive.org/about/terms.php](https://archive.org/about/terms.php) |
| **Prelinger** | Só itens com marca PD/CC0. A Getty vende 19 mil clipes da coleção | Opcional | Content ID das versões Getty | [panix.com/~footage/prelarch.html](https://www.panix.com/~footage/prelarch.html) ("DO NOT ASSUME that all Prelinger Archives films are in the public domain") |
| **Smithsonian Open Access** | **CC0** só nos itens com o ícone | Não exigido | Baixo nos CC0 | [si.edu/termsofuse](https://www.si.edu/termsofuse); [si.edu/openaccess](https://www.si.edu/openaccess) |
| **Chronicling America** | Jornais com mais de 95 anos = PD; os mais novos "acredita-se PD" | Sugerido (LoC + jornal) | Baixo antes de 1931. Fotos de agência e quadrinhos nas edições mais novas | [rights-and-access](https://www.loc.gov/collections/chronicling-america/about-this-collection/rights-and-access/) |
| **Governo do Japão / GSI** | GSI: Public Data License 1.0. Ministérios: Standard Terms v2.0 (**uso comercial permitido**) | **Obrigatório**: "Source: GSI website (URL)" + "edited" | Médio. Resultados de levantamento (Survey Act) e logos ficam fora | [gsi.go.jp/ENGLISH/page_e30286.html](https://www.gsi.go.jp/ENGLISH/page_e30286.html); [cao.go.jp/en/notice-e.html](https://www.cao.go.jp/en/notice-e.html) |
| **Imperial War Museums** | Licença grátis **só não comercial** | © IWM (nº) | **PROIBIDO** em canal monetizado | [iwm.org.uk/corporate/policies/copyright](https://www.iwm.org.uk/corporate/policies/copyright) |
| **AP / Rosenthal (Iwo Jima)** | O Commons trata como PD nos EUA (registro não renovado). **Contestado**: a Getty vende, e há nota da LoC citando autorização da AP | "Joe Rosenthal / Associated Press" | Médio. Nunca na thumb. Alternativas: 1ª bandeira de Lowery (USMC) e filme de Genaust (USMC) | [Commons, arquivo](https://commons.wikimedia.org/wiki/File:Raising_the_Flag_on_Iwo_Jima,_larger_-_edit1.jpg) |
| **USGS / Landsat / NASA** | PD. Insígnia e logo da NASA são protegidos | "Landsat image courtesy of the U.S. Geological Survey" / "NASA" | Baixo | [Landsat FAQ](https://www.usgs.gov/faqs/are-there-any-restrictions-use-or-redistribution-landsat-data); [USGS copyrights](https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits); [NASA images](https://www.nasa.gov/nasa-brand-center/images-and-media/) |
| **USAF / USMC / Army** | Informação pública / PD salvo indicação (17 USC 105) | Pedido | Material de terceiros publicado nos sites | [af.mil/Disclaimer](https://www.af.mil/Disclaimer/); [usmcu.edu](https://www.usmcu.edu/Home/Privacy-Security-Policy/); [army.mil/terms](https://www.army.mil/terms) |
| **YouTube Content ID** | Dá para contestar por PD, mas o reclamante decide (30 dias) e pode escalar para takedown | — | Reclamação em filme PD reenviado por terceiros | [support.google.com/youtube/answer/2797454](https://support.google.com/youtube/answer/2797454) |

Observações:
- O USMC History Division publica no Flickr com CC BY 2.0, mesmo sendo obra de governo. O vídeo de referência de Iwo Jima credita assim, e convém fazer igual.
- Os cinejornais **Universal Newsreel** da NARA (ex.: `gov.archives.arc.39053`) foram doados com os direitos liberados ao público. Mesmo assim, confira o *Use Restriction* do registro.
- Páginas que o site oficial bloqueou com 403 (LoC, SI, IWM, af.mil, usmcu) foram conferidas no Wayback Machine.

## Tema × contagens × nota

Contagens de 12/11/2026. Teto por soma de frases; leia "Método e limites".

| # | Tema | Nota | NARA fotos | NARA filmes | NHHC fotos | IA filmes | Commons cat. | Commons DVIDS | Commons LoC | Ajuste manual |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Nevada Test Site | **5** | 22125 | 8 | 4 | 86 | 2047 | 0 | 257 |  |
| 2 | Pearl Harbor / USS Arizona | **5** | 3782 | 390 | 1980 | 8189 | 2295 | 4850 | 2799 |  |
| 3 | Okinawa (1945) | **5** | 4796 | 881 | 546 | 4425 | 674 | 29955 | 23 |  |
| 4 | Iwo Jima | **5** | 2403 | 619 | 527 | 1142 | 1266 | 3618 | 50 |  |
| 5 | Guadalcanal | **5** | 1451 | 147 | 419 | 885 | 1782 | 633 | 120 |  |
| 6 | Gettysburg | **4.5** | 1209 | 18 | 9 | 5316 | 812 | 384 | 2462 |  |
| 7 | Antietam (Gardner) | **4.5** | 253 | 12 | 51 | 896 | 683 | 268 | 1366 |  |
| 8 | Bikini Atoll / Operation Crossroads | **4.5** | 179 | 273 | 98 | 146 | 346 | 4 | 7 | +0.5: filmes oficiais de Crossroads (PD) e 1.268 imagens no Smithsonian; hoje: Landsat PD + relatorio NPS 1991 dos naufragios |
| 9 | Peleliu | **4.5** | 466 | 152 | 44 | 95 | 348 | 2716 | 0 |  |
| 10 | Kwajalein | **4** | 830 | 87 | 185 | 138 | 331 | 979 | 10 |  |
| 11 | Fort Sumter | **4** | 51 | 0 | 32 | 132 | 1089 | 8 | 868 |  |
| 12 | Midway Atoll | **4** | 573 | 40 | 401 | 312 | 455 | 280 | 4 | +0.5: filme de John Ford (PD) + 80-G em ~6000 px + fotos USFWS PD do lugar hoje (hangar, baterias, pistas) |
| 13 | Tinian | **4** | 545 | 65 | 96 | 154 | 301 | 313 | 12 | +0.5: 509th/Enola Gay (PD) + DVIDS forte em North Field hoje (Forager, Cope North) |
| 14 | Hanford / B Reactor | **4** | 351 | 5 | 4 | 541 | 941 | 44 | 385 |  |
| 15 | Omaha Beach / Pointe du Hoc | **4** | 334 | 22 | 119 | 523 | 927 | 1593 | 0 |  |
| 16 | Enewetak / Runit Dome | **3.5** | 798 | 87 | 69 | 113 | 199 | 24 | 0 | +0.5: filmes DOE/AEC de Ivy Mike (gov.doe.*, PD) + fotos DOE do Runit Dome; contagem por frase subestima |
| 17 | Aleutians (Attu/Kiska) | **3.5** | 567 | 90 | 113 | 226 | 347 | 43 | 28 |  |
| 18 | Appomattox | **3.5** | 180 | 3 | 0 | 1328 | 488 | 21 | 711 |  |
| 19 | Corregidor | **3.5** | 401 | 84 | 99 | 212 | 362 | 694 | 10 | -0.5: periodo bom, mas o 'hoje' e quase todo CC BY / CC BY-SA no Commons; DVIDS fraco (o proxy pega nomes de unidades) |
| 20 | Lincoln assassination / Ford's Theatre | **3.5** | 307 | 4 | 8 | 403 | 902 | 2 | 226 |  |
| 21 | Alcatraz | **3.5** | 216 | 14 | 11 | 4192 | 1141 | 24 | 145 |  |
| 22 | Trinity Site | **3.5** | 35 | 1 | 3 | 84 | 338 | 12 | 117 | +1: pouco no NARA por frase, mas LANL/DOE/Army: fotos e filme Trinity PD e muito conhecidos; open house anual (fotos DVIDS/White Sands) |
| 23 | Mittelwerk (Dora) | **3** | 3025 | 8 | 0 | 81 | 163 | 0 | 10 | -0.5: fotos NARA vem do campo Dora/Nordhausen (tema sensivel, atrocidade); interior da fabrica: pouco |
| 24 | Wake Island | **3** | 309 | 32 | 106 | 431 | 239 | 253 | 132 |  |
| 25 | Fort Jefferson (Dry Tortugas) | **3** | 491 | 2 | 20 | 18 | 712 | 1 | 98 |  |
| 26 | Diego Garcia | **3** | 488 | 0 | 6 | 581 | 1441 | 3822 | 5 | -1: 3.800 fotos DVIDS de base ativa, mas pouca historia de guerra em arquivo; acesso de imagem da base e controlado |
| 27 | Truk Lagoon | **2.5** | 262 | 42 | 81 | 480 | 105 | 13 | 3 |  |
| 28 | Andersonville | **2.5** | 45 | 0 | 1 | 189 | 737 | 0 | 179 |  |
| 29 | Johnston Atoll | **2** | 501 | 10 | 23 | 64 | 90 | 0 | 1 |  |
| 30 | Cheyenne Mountain | **2** | 91 | 4 | 0 | 74 | 124 | 513 | 31 |  |
| 31 | Camp Century (Project Iceworm) | **1.5** | 8 | 4 | 16 | 21 | 8 | 0 | 0 | +0.5: pouco volume, mas o filme do Exercito 'Camp Century' / The Big Picture e fotos do Army sao PD e unicos |
| 32 | Hashima (Battleship Island) | **1** | 3 | 0 | 0 | 15 | 336 | 0 | 0 | -0.5: material de epoca e japones (sem PD automatico); quase nada em arquivo dos EUA; hoje so CC BY/BY-SA; nao e lugar de guerra americano |
| 33 | Area 51 | **0.5** | 12 | 5 | 182 | 933 | 173 | 4 | 0 | -1.5: quase sem material oficial liberado (fotos CIA/USGS esparsas); contagem do IA/NHHC e ruido |
| 34 | Chernobyl (contraste, nao EUA) | **0** | 16 | 4 | 0 | 3548 | 670 | 1 | 0 | -3: nao e EUA; material sovietico/ucraniano sem PD claro; so contraste |

O Smithsonian (imagens online, sem filtro CC0) só foi contado nos candidatos: Bikini 1.268, Tinian 609, Corregidor 109, Iwo Jima 97, Midway 11.

## Itens-chave por tema (3–5, com URL)

Os filmes de governo vêm em geral do IA, mas a cópia de referência para provar a licença é a da NARA, DOE ou DoD. As fotos "atuais" vêm do DVIDS via Commons. A lista é automática e filtrada à mão, então confira cada item antes de usar.

**Nevada Test Site** (nota 5) - atual livre: sim: NNSA/DOE (PD), Landsat; visitas guiadas mensais
- [Nuclear Test Film - Operation Teapot (1955, DOE)](https://archive.org/details/gov.doe.0800017) - Internet Archive, filme de governo
- [Grable event, Operation Upshot-Knothole (1953)](https://commons.wikimedia.org/wiki/File:Nuclear_artillery_test_Grable_Event_-_Part_of_Operation_Upshot-Knothole.jpg) - Wikimedia Commons, PD
- [SURVEILLANCE SENSORS EXP, NEVADA TEST SITE](https://catalog.archives.gov/id/75454201) - NARA; Unrestricted (obra federal)
- [K-26354 Operation Upshot, Knothole Grable Event](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/Other/K-26354.html) - NHHC; PD salvo indicacao

**Pearl Harbor / USS Arizona** (nota 5) - atual livre: sim: NPS + DVIDS muito forte
- [December 7th (1943, John Ford/Gregg Toland, versao longa)](https://archive.org/details/gov.archives.arc.40099.bl) - Internet Archive, filme de governo
- [News Parade: Bombing of Pearl Harbor](https://archive.org/details/NewsPara1942) - Internet Archive; cc/licenses/publicdomain/; 1942
- [Pearl Harbor](https://archive.org/details/PearlHarbor) - Internet Archive; cc/licenses/publicdomain/
- [80-G-32792 Pearl Harbor Attack](https://www.history.navy.mil/our-collections/photography/wars-and-events/world-war-ii/pearl-harbor-raid/overall-views-of-the-pearl-harbor-attack/80-G-32792.html) - NHHC; PD salvo indicacao

**Okinawa (1945)** (nota 5) - atual livre: sim: DVIDS muito forte (bases atuais)
- [Rubble of the walls of Shuri castle, 1945](https://commons.wikimedia.org/wiki/File:Rubble_of_the_walls_of_Shuri_castle,_1945_01.jpg) - Wikimedia Commons, PD
- [Okinawa: Bastion in the Pacific](https://archive.org/details/gov.archives.111-tv-423) - Internet Archive; cc/licenses/publicdomain/
- [Landings On Okinawa, 1945/04/09](https://archive.org/details/1945-04-09_Landings_On_Okinawa) - Internet Archive; cc/licenses/publicdomain/; 1945
- [World War II – Okinawa](https://catalog.archives.gov/id/74252368) - NARA; Unrestricted (obra federal)
- [NH 104963 Mouth of the Bishi River, Okinawa](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/NH-104000/NH-104963.html) - NHHC; PD salvo indicacao

**Iwo Jima** (nota 5) - atual livre: sim: DVIDS (cerimonias anuais Reunion of Honor, USMC), GSI Japao (PDL 1.0, credito)
- [To the Shores of Iwo Jima (1945, USN/USMC/USCG)](https://archive.org/details/ToTheShoresOfIwoJima) - Internet Archive, filme de governo
- [3rd Marines, Combat On Iwo Jima D+7 Feb 26 1945](https://archive.org/details/NPC-8550) - Internet Archive; cc/publicdomain/mark/1.0/; 1945
- [MARINES RAISE FLAG OVER IWO JIMA (ETC.)](https://archive.org/details/gov.archives.arc.39054) - Internet Archive; cc/publicdomain/zero/1.0/; 1945
- [Photo: Iwo Jima Flag](https://www.history.navy.mil/research/archives/digital-exhibits-highlights/iwo-jima/photo--iwo-jima-flag.html) - NHHC; PD salvo indicacao

**Guadalcanal** (nota 5) - atual livre: sim: DVIDS (DPAA, aniversarios)
- [Guadalcanal Washday](https://catalog.archives.gov/id/100378079) - NARA; Unrestricted (obra federal)
- [80-G-39209 Guadalcanal Campaign](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nara-series/80-g/80-G-30000/80-g-39209-guadalcanal-campaign.html) - NHHC; PD salvo indicacao
- [DPAA Hosts Repatriation Ceremony on Guadalcanal (8611465).jpg](https://commons.wikimedia.org/wiki/File:DPAA_Hosts_Repatriation_Ceremony_on_Guadalcanal_(8611465).jpg) - DVIDS via Commons (atual); Public domain; 6554x4374

**Gettysburg** (nota 4.5) - atual livre: sim: NPS (PD) + DVIDS (staff rides)
- [Army staff ride to Gettysburg 150711-Z-DL064-042.jpg](https://commons.wikimedia.org/wiki/File:Army_staff_ride_to_Gettysburg_150711-Z-DL064-042.jpg) - DVIDS via Commons (atual); Public domain; 3981x2644

**Antietam (Gardner)** (nota 4.5) - atual livre: sim: NPS (PD)
- [Antietam: Confederate dead by a fence on the Hagerstown road (Gardner, 1862, LOC)](https://commons.wikimedia.org/wiki/File:Antietam,_Md._Confederate_dead_by_a_fence_on_the_Hagerstown_road_LOC_cwpb.01097.jpg) - Wikimedia Commons, PD
- [ROYAL NAVY AIR OPERATIONS ABOARD USS ANTIETAM](https://archive.org/details/428-npc-1982) - Internet Archive; ; 1953

**Bikini Atoll / Operation Crossroads** (nota 4.5) - atual livre: fraco: Landsat (PD), relatorio NPS 1991 dos naufragios (PD); fotos de mergulho atuais sao CC BY-SA/privadas
- [Nuclear Test Film - Project Crossroads (DOE)](https://archive.org/details/gov.doe.0800002) - Internet Archive, filme de governo
- [Operation Crossroads (Part I)](https://archive.org/details/Operatio1946) - Internet Archive; cc/licenses/publicdomain/; 1946
- [Operation Crossroads (Part II)](https://archive.org/details/Operatio1946_2) - Internet Archive; cc/licenses/publicdomain/; 1946
- [Progress of the shock wave from the Test Able explosion at Bikini Atoll, Operation Crossro](https://catalog.archives.gov/id/22118342) - NARA; Unrestricted (obra federal)
- [80-G-K-20268 Bikini Atoll A-Bomb Tests, 1946](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/80-G-K-20000/80-G-K-20268.html) - NHHC; PD salvo indicacao

**Peleliu** (nota 4.5) - atual livre: sim: DVIDS (DPAA, obras do porto 2020s)
- [Fury in the Pacific (1945, Army/Navy/USMC)](https://archive.org/details/MN-5051J) - Internet Archive, filme de governo
- [Navajos at Peleliu](https://catalog.archives.gov/id/100385918) - NARA; Unrestricted (obra federal)
- [Palau Government, DoD host public meeting on Peleliu South Dock rehabilitation, improvemen](https://commons.wikimedia.org/wiki/File:Palau_Government,_DoD_host_public_meeting_on_Peleliu_South_Dock_rehabilitation,_improvements_(9256376).jpg) - DVIDS via Commons (atual); Public domain; 7596x5066

**Kwajalein** (nota 4) - atual livre: sim: DVIDS (Reagan Test Site, US Army Garrison Kwajalein)
- [Wounded Marines; Dead Japs; Wreckage On Kwajalein Atoll, Marshall Islands; German Prisoner](https://archive.org/details/NPC-1475) - Internet Archive; cc/publicdomain/mark/1.0/; 1944
- [Marines Land On Kwajalein Atoll; Mosquito Control, Funafuti Island](https://archive.org/details/NPC-1474) - Internet Archive; cc/publicdomain/mark/1.0/; 1944
- [USMC 73903-D Kwajalein Operation, 1944](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/USMC-73000/USMC-73903-D.html) - NHHC; PD salvo indicacao

**Fort Sumter** (nota 4) - atual livre: sim: NPS (PD)
- [NH 73744 Bombardment of Fort Sumter, Charleston Harbor](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/NH-73000/NH-73744.html) - NHHC; PD salvo indicacao
- [South Carolina honors Carolina Day 140628-Z-HU793-024.jpg](https://commons.wikimedia.org/wiki/File:South_Carolina_honors_Carolina_Day_140628-Z-HU793-024.jpg) - DVIDS via Commons (atual); Public domain; 2880x1920

**Midway Atoll** (nota 4) - atual livre: sim: USFWS (PD) + DVIDS + ISS/NASA; acesso civil fechado = imagens de governo sao quase as unicas
- [Torpedo Squadron 8 (1942, John Ford, USN)](https://archive.org/details/torpedo_squadron8) - Internet Archive, filme de governo
- [BATTLE OF MIDWAY](https://archive.org/details/gov.archives.arc.13196) - Internet Archive; cc/licenses/publicdomain/; 1942
- [Battle of Midway](https://archive.org/details/gov.archives.arc.65422.b) - Internet Archive; cc/publicdomain/zero/1.0/; 1942
- [80-G-451086 Midway Atoll](https://www.history.navy.mil/our-collections/photography/wars-and-events/world-war-ii/midway/80-G-451086.html) - NHHC; PD salvo indicacao
- [83rd Anniversary of the Battle of Midway at the U S Navy Memorial (9086177).jpg](https://commons.wikimedia.org/wiki/File:83rd_Anniversary_of_the_Battle_of_Midway_at_the_U_S_Navy_Memorial_(9086177).jpg) - DVIDS via Commons (atual); Public domain; 6132x4088

**Tinian** (nota 4) - atual livre: sim: DVIDS forte (Forager, Cope North, North Field, poco da bomba)
- [The Last Bomb (1945, AAF)](https://archive.org/details/gov.archives.arc.65631) - Internet Archive, filme de governo
- [Bombardment Of Guam & Tinian; Naval Activity Of Saipan & Tinian, 07/29/1944](https://archive.org/details/NPC-4888) - Internet Archive; cc/publicdomain/mark/1.0/; 1944
- [USS Birmingham Takes On Ammo; Japanese Air Attack; Bombardment Of Tinian, 07/08/1944](https://archive.org/details/NPC-4851) - Internet Archive; cc/publicdomain/mark/1.0/; 1944
- [World War II – Tinian](https://catalog.archives.gov/id/74254234) - NARA; Unrestricted (obra federal)
- [Tinian Landings Photo Gallery](https://www.history.navy.mil/browse-by-topic/wars-conflicts-and-operations/world-war-ii/1944/guam-tinian/tinian-gallery.html) - NHHC; PD salvo indicacao

**Hanford / B Reactor** (nota 4) - atual livre: sim: DOE/NPS Manhattan Project NHP (PD)
- [Hanford B-Reactor Area, 2 jun 1944](https://commons.wikimedia.org/wiki/File:Hanford_B-Reactor_Area_1944.jpg) - Wikimedia Commons, PD
- [Hanford Science Forum](https://archive.org/details/HanfordS1957) - Internet Archive; cc/licenses/publicdomain/; 1957
- [Wings Over Hanford](https://archive.org/details/0308_Wings_Over_Hanford_09_00_46_00) - Internet Archive; 

**Omaha Beach / Pointe du Hoc** (nota 4) - atual livre: sim: DVIDS (aniversarios do Dia D), ABMC
- [Coastal Gun Batteries (Pointe du Hoc) Dead Germans; USS Texas (BB-35) Normandy, 1944](https://archive.org/details/NPC-15351) - Internet Archive; cc/publicdomain/mark/1.0/; 1944
- [Invasion, Fox-Green Beachhead, Omaha Beach, France ; Convoys And Loading Lcts, Omaha Beach](https://archive.org/details/111-adc-1470) - Internet Archive; ; 1944
- [Omaha Beach](https://catalog.archives.gov/id/176888428) - NARA; Unrestricted (obra federal)
- [KN-18450 &amp;quot;Storm, Omaha Beach&amp;quot;](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nara-series/kn-series/KN-10000/KN-18450.html) - NHHC; PD salvo indicacao

**Enewetak / Runit Dome** (nota 3.5) - atual livre: parcial: DOE/LLNL (Runit Dome), Landsat; DVIDS raro
- [Operation Ivy (1952, Ivy Mike) - copia do DOE](https://archive.org/details/gov.doe.0800012) - Internet Archive, filme de governo
- [Battle of Eniwetok: Aerial Of Raids In Engebi & Parry Islands, 3/6/1944](https://archive.org/details/NPC-1724) - Internet Archive; cc/publicdomain/mark/1.0/; 1944
- [GSAP Gun Camera Views Of Raids On Eniwetok Atoll By Planes From The USS Cowpens (CVL-25), ](https://archive.org/details/NPC-1598) - Internet Archive; cc/publicdomain/mark/1.0/; 1944
- [For EPG (Enewetak Proving Ground) Recruiting Program Information](https://catalog.archives.gov/id/26464915) - NARA; Unrestricted (obra federal)

**Aleutians (Attu/Kiska)** (nota 3.5) - atual livre: parcial: NPS (Aleutian WWII NHA), USFWS (Alaska Maritime NWR)
- [Report from the Aleutians (1943, John Huston, Army)](https://archive.org/details/gov.dod.dimoc.20347) - Internet Archive, filme de governo
- [ALLIES TAKE KISKA (ETC.)](https://archive.org/details/gov.archives.arc.38974) - Internet Archive; cc/publicdomain/zero/1.0/; 1943
- [80-G-65977 Attu Operation, May 1943](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/80-G-65000/80-G-65977.html) - NHHC; PD salvo indicacao

**Appomattox** (nota 3.5) - atual livre: sim: NPS (PD)
- [McLean house, Appomattox, 1865 (LOC), 7500x6311](https://commons.wikimedia.org/wiki/File:Appomattox_Court_House,_Virginia._McLean_house_LOC_cwpb.01395.jpg) - Wikimedia Commons, PD

**Corregidor** (nota 3.5) - atual livre: parcial: DVIDS raro (Balikatan); o resto e CC BY / CC BY-SA no Commons
- [Appointment in Tokyo (1945, Army)](https://archive.org/details/gov.dod.dimoc.20379) - Internet Archive, filme de governo
- [U.S. TROOPS RETURN TO CORREGIDOR (ETC)](https://archive.org/details/gov.archives.arc.39053) - Internet Archive; cc/publicdomain/zero/1.0/; 1945
- [NH 122202 Corregidor and Cabala from the west](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/NH-122000/NH-122202.html) - NHHC; PD salvo indicacao

**Lincoln assassination / Ford's Theatre** (nota 3.5) - atual livre: sim: NPS Ford's Theatre (PD)
- [Execution of the Lincoln assassins (Gardner, 7 jul 1865), 6902x5425](https://commons.wikimedia.org/wiki/File:Execution_Lincoln_assassins.jpg) - Wikimedia Commons, PD
- [NH 48120 The Accused Conspirators in the Assassination of Abraham Lincoln](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/NH-48000/NH-48120.html) - NHHC; PD salvo indicacao

**Alcatraz** (nota 3.5) - atual livre: sim: NPS (PD) + DVIDS
- [CA - Alcatraz](https://catalog.archives.gov/id/45708587) - NARA; Unrestricted (obra federal)

**Trinity Site** (nota 3.5) - atual livre: sim: DVIDS / White Sands Missile Range (open house anual)
- [Nuclear Test Film - Trinity Shot (1945, DOE)](https://archive.org/details/gov.doe.0800001) - Internet Archive, filme de governo
- [WSMR holds Trinity Site open house 061016-A-IT218-0002.jpg](https://commons.wikimedia.org/wiki/File:WSMR_holds_Trinity_Site_open_house_061016-A-IT218-0002.jpg) - DVIDS via Commons (atual); Public domain; 4288x2848

**Mittelwerk (Dora)** (nota 3) - atual livre: fraco: memorial alemao (licencas alemas); quase nada PD
- [Mittelwerk V-2 complex tunnel (1945)](https://commons.wikimedia.org/wiki/File:Mittelwerk_V-2_complex_tunnel.jpg) - Wikimedia Commons, PD

**Wake Island** (nota 3) - atual livre: parcial: DVIDS (USAF/PACAF), USFWS; base fechada
- [USMC-17673 (Wake, USMC Archives)](https://commons.wikimedia.org/wiki/File:USMC-17673.jpg) - Wikimedia Commons, PD
- [Newsreel: U.S. Navy Attack On Wake Island](https://archive.org/details/NPC-2687d) - Internet Archive; cc/publicdomain/mark/1.0/; 1943
- [USMC 498166 Last Man Off Wake Island Returns](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nara-series/usmc-series/usmc-400000/usmc-498166-last-man-off-wake-island-returns.html) - NHHC; PD salvo indicacao

**Fort Jefferson (Dry Tortugas)** (nota 3) - atual livre: sim: NPS (PD)
- [Fort Jefferson, Dry Tortugas (aerea, PD)](https://commons.wikimedia.org/wiki/File:Fort-Jefferson_Dry-Tortugas.jpg) - Wikimedia Commons, PD

**Diego Garcia** (nota 3) - atual livre: sim: DVIDS forte (base ativa)
- [STS050-48-021 - STS-050 - Earth observation views of Diego Garcia atoll, Indian Ocean.](https://catalog.archives.gov/id/22712837) - NARA; Unrestricted (obra federal)
- [K-91000 Diego Garcia, Chagos Islands.](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/Other/K-91000.html) - NHHC; PD salvo indicacao

**Truk Lagoon** (nota 2.5) - atual livre: fraco: NOAA/NPS esparso; mergulho = privado
- [Japanese shipping under attack in Truk Lagoon, 17 Feb 1944 (Hailstone)](https://commons.wikimedia.org/wiki/File:Japanese_shipping_under_attack_in_Truk_Lagoon_during_Operation_Hailstone,_17_February_1944_(80-G-215151).jpg) - Wikimedia Commons, PD
- [USN Planes In Combat; Strafing Japanese AKs, CL, DD, & Installations, Truk WW2](https://archive.org/details/NPC-1636) - Internet Archive; cc/publicdomain/mark/1.0/
- [We Blast Truk, Jap Fortress, 1944/03/30](https://archive.org/details/1944-03-30_We_Blast_Truk_Jap_Fortress) - Internet Archive; cc/licenses/publicdomain/; 1944
- [80-G-218604 Raid on Truk, February 1944](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/80-G-218000/80-G-218604.html) - NHHC; PD salvo indicacao

**Andersonville** (nota 2.5) - atual livre: sim: NPS (PD)
- [Andersonville Prison, July 1864 (LOC), 4024x5367](https://commons.wikimedia.org/wiki/File:Andersonville_Prison,_Georgia_in_July_1864._LOC_gvhs01.vhs00039.jpg) - Wikimedia Commons, PD
- [NH 85080-KN Andersonville Prison, Georgia](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/NH-85000/NH-85080-KN.html) - NHHC; PD salvo indicacao

**Johnston Atoll** (nota 2) - atual livre: parcial: USFWS (refugio), DoD/JACADS; pouco recente
- [Starfish Prime Interim Report by Commander JTF-8 (1962)](https://archive.org/details/StarfishPrimeInterimReportByCommanderJTF8) - Internet Archive, filme de governo
- [Johnston Atoll Chemical Agent Disposal System, Nov 1990](https://commons.wikimedia.org/wiki/File:Johnston_Atoll_Chemical_Agent_Disposal_System_Nov_1990.JPEG) - Wikimedia Commons, PD
- [PRESIDENT NIXON'S VISIT, JOHNSTON ISLAND, July 23-24, 1969](https://archive.org/details/gov.archives.arc.71184) - Internet Archive; cc/licenses/publicdomain/

**Cheyenne Mountain** (nota 2) - atual livre: parcial: DVIDS (Space Force/NORAD), acesso controlado
- [Cheyenne Mountain 20-ton blast door closing (USAF, 2012)](https://commons.wikimedia.org/wiki/File:121025-F-ZZ000-001_Cheyenne_Mountain_20-ton_blast_door_closing.jpg) - Wikimedia Commons, PD

**Camp Century (Project Iceworm)** (nota 1.5) - atual livre: fraco: so imagens NASA/USGS do gelo e estudos (PD)
- [The Big Picture: Camp Century (Army)](https://archive.org/details/big-picture-camp-century) - Internet Archive, filme de governo
- [Camp Century trench construction (1960)](https://commons.wikimedia.org/wiki/File:Camp_Century_trench_construction.png) - Wikimedia Commons, PD
- [Camp Century revisited - a pictorial view, June 1969 (USACE, PDF)](https://commons.wikimedia.org/wiki/File:Camp_Century_revisited-_A_pictorial_view_-_June_1969_-_USACE-p266001coll1-3499.pdf) - Wikimedia Commons, PD
- [UNITED STATES ARMY RESEARCH AND DEVELOPMENT - PROGRESS REPORT NUMBER SIX - CAMP CENTURY](https://archive.org/details/gov.dod.dimoc.26064) - Internet Archive; cc/publicdomain/zero/1.0/; 1964

**Hashima (Battleship Island)** (nota 1) - atual livre: nao (so CC BY/BY-SA de turistas; governo do Japao com credito)

**Area 51** (nota 0.5) - atual livre: nao (so satelite USGS/Landsat)
- [Area 51, 28 Aug 1968 (satelite, PD)](https://commons.wikimedia.org/wiki/File:Area_51_28_August_1968_2.jpg) - Wikimedia Commons, PD

**Chernobyl (contraste, nao EUA)** (nota 0) - atual livre: nao (nao e EUA)

## Os 4 candidatos: itens concretos para 15–20 min

Legenda: **E** = então (época), **H** = hoje, **D** = documento legível, **⇄** = par então × agora. A resolução vem do Commons ou de amostra baixada. "PD" = obra do governo dos EUA.

### Midway Atoll: 25 itens (o melhor em material)

| # | Item | Tipo | Licença | Resolução | URL |
|---|---|---|---|---|---|
| 1 | *The Battle of Midway* (John Ford, 1942, USN), filme colorido | E filme | PD (cópia NARA via FedFlix) | — | https://archive.org/details/gov.archives.arc.13196 |
| 2 | *Torpedo Squadron 8* (John Ford, 1942, USN) | E filme | PD (USN) | — | https://archive.org/details/torpedo_squadron8 |
| 3 | NARA 428-NPC-21953 "Battle of Midway MN-1433", mp4 | E filme | Undetermined: conferir | — | https://catalog.archives.gov/id/81714 |
| 4 | NARA 342-USAF-16985 "Battle of Midway" (AAF) | E filme | Restricted-Possibly na NARA; cópia CC0 no IA | — | https://catalog.archives.gov/id/65422 · https://archive.org/details/gov.archives.arc.65422.b |
| 5 | NARA 428-NPC-22080 "John Ford footage simulating Battle of Midway" (bastidor: Ford **encenou** parte) | E filme | Undetermined | — | https://catalog.archives.gov/id/81737 |
| 6 | Vista aérea de Midway, 24 nov 1941 (80-G-451086) ⇄ #22 | E foto | PD | 4500×4797 | https://commons.wikimedia.org/wiki/File:Aerial_view_of_Midway_Atoll_on_24_November_1941_(80-G-451086).jpg · https://www.history.navy.mil/our-collections/photography/wars-and-events/world-war-ii/midway/80-G-451086.html |
| 7 | Midway em abril de 1945, Sand e Eastern Island (80-G-345452) | E foto | PD | — | https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/80-G-345000/80-G-345452.html |
| 8 | Hangar de hidroaviões danificado, 4 jun 1942 ⇄ #19 | E foto | PD | 5717×4448 | https://commons.wikimedia.org/wiki/File:Damaged_Midway_seaplane_hangar_1942.jpg |
| 9 | USS Yorktown atingido por torpedo, 4 jun 1942 | E foto | PD | 5660×4467 | https://commons.wikimedia.org/wiki/File:USS_Yorktown_(CV-5)_is_hit_by_a_torpedo_on_4_June_1942.jpg |
| 10 | NARA 80-G-414423 "Bombing of USS Yorktown" | E foto | Unrestricted | 5855×4882 (amostra) | https://catalog.archives.gov/id/221949041 |
| 11 | Porta-aviões Hiryu em chamas, 5 jun 1942 (NH 73064 / 73065) | E foto | PD | 3846×2473 | https://commons.wikimedia.org/wiki/File:Japanese_aircraft_carrier_Hiryu_burning_on_5_June_1942_(NH_73064).jpg · https://commons.wikimedia.org/wiki/File:Japanese_aircraft_carrier_Hiryu_adrift_and_burning_on_5_June_1942_(NH_73065).jpg |
| 12 | B-17 decolando de Eastern Island (USAF-22635-AC) ⇄ #24 | E foto | PD | — | https://www.history.navy.mil/our-collections/photography/wars-and-events/world-war-ii/midway/USAF-22635-AC.html |
| 13 | Ataque de B-17 à frota japonesa, 4 jun 1942, 431st Bomb Sq (342-FH) | E foto | Unrestricted | — | https://catalog.archives.gov/id/204977034 |
| 14 | Alferes George Gay, único sobrevivente do VT-8, no hospital (80-G-17678) | E foto | Unrestricted | tif | https://catalog.archives.gov/id/505632509 |
| 15 | Prisioneiros japoneses do Hiryu desembarcando (80-G-79984-28) | E foto | PD | — | https://www.history.navy.mil/our-collections/photography/wars-and-events/world-war-ii/midway/80-G-79984-28.html |
| 16 | **D** "Battle of Midway Track Chart" (RG 38) | D mapa | Unrestricted | 45 MB | https://catalog.archives.gov/id/152914619 |
| 17 | **D** CINCPAC (Nimitz) "Battle of Midway" report, Enc A–F, e 2º relatório suplementar (datilografado, legível para o "grifo") | D texto | Unrestricted | — | https://catalog.archives.gov/id/133919628 · https://catalog.archives.gov/id/133944571 |
| 18 | Ficha NHL "WWII Facilities at Midway" (NPS): mapa das instalações | D texto | Restricted-Possibly (texto NPS = PD; fotos internas: conferir) | PDF 86 MB | https://catalog.archives.gov/id/131518784 |
| 19 | Hangar de hidroaviões **desabando**, 2022 (USFWS) ⇄ #8 | H foto | PD | 3264×2448 | https://commons.wikimedia.org/wiki/File:Midway_seaplane_hangar_collapse_(51840796056).jpg |
| 20 | Bateria A, canhão de 5 pol., Sand Island, 2015 (levantamento federal) | H foto | PD | 4608×3456 | https://commons.wikimedia.org/wiki/File:Figure_39-_Battery_A,_5-Inch_Gun_Position_(Property_No._S-9),_Midway_Atoll,_Sand_Island_(April_15,_2015)_(25493712483).jpg |
| 21 | Casamata de concreto S-6, 2015 | H foto | PD | 4608×3310 | https://commons.wikimedia.org/wiki/File:Figure_33-_Concrete_Pillbox_(Property_No._S-6),_Midway_Atoll,_Sand_Island_(April_15,_2015)_(26070231756).jpg |
| 22 | Midway visto da ISS, 2001 (ISS002-E-8828) ⇄ #6 | H foto | PD (NASA) | 3060×2092 | https://commons.wikimedia.org/wiki/File:ISS002-E-8828_-_View_of_the_Midway_Atoll.jpg |
| 23 | 80ª comemoração da batalha em Midway, 2022 (USFWS) | H foto | PD | 6000×4000 | https://commons.wikimedia.org/wiki/File:80th_Commemoration_of_the_Battle_of_Midway_(52219380854).jpg |
| 24 | Pista abandonada de Eastern Island, 2015 (Forest & Kim Starr) ⇄ #12 | H foto | **CC BY 3.0 US** (crédito) | 3456×4608 | https://commons.wikimedia.org/wiki/File:Starr-150402-0687-Poa_annua-habit_on_abandoned_runway-Northeast_Eastern_Island-Midway_Atoll_(25180587621).jpg |
| 25 | "Historic Canon at Midway Atoll NWR" (USFWS, NARA 022-DP) | H foto | Unrestricted | — | https://catalog.archives.gov/id/166702978 |

Extra para o roteiro: jornal *Evening Star* (Washington) de 7 jun 1942, em Chronicling America. A URL padrão é `https://www.loc.gov/item/sn83045462/1942-06-07/ed-1/`. **Não verificada**, porque a LoC bloqueia a VPS (o título sn83045462 já foi usado no canal de referência).

### Tinian: 24 itens

| # | Item | Tipo | Licença | Resolução | URL |
|---|---|---|---|---|---|
| 1 | *The Last Bomb* (1945, AAF: B-29 das Marianas sobre o Japão) | E filme | PD | — | https://archive.org/details/gov.archives.arc.65631 |
| 2 | *The Marianas Operation* (documentário USMC: Saipan, Tinian, Guam) | E filme | PD mark (USMC) | — | https://archive.org/details/TheMarianasOperation |
| 3 | NARA 428-NPC-6056 "Construction activity on Tinian airfield" | E filme | Undetermined | — | https://catalog.archives.gov/id/77758 |
| 4 | NARA 428-NPC-5506 "Scenes of land action on Tinian" | E filme | Undetermined | — | https://catalog.archives.gov/id/77522 |
| 5 | *Inside the Enola Gay* (DOE, NARA) | E filme | PD mark | — | https://archive.org/details/InsideEnolaGay |
| 6 | Fuzileiros descendo de LVT na praia, 24 jul 1944 (USMC 88112) ⇄ #23 | E foto | Unrestricted | 6315×5030 (amostra) | https://catalog.archives.gov/id/74254234 · https://commons.wikimedia.org/wiki/File:USMC_88112_Marines_demount_from_an_LVT_on_Tinian.tif |
| 7 | Série NARA 127-GR "World War II – Tinian" (dezenas de fotos USMC) | E fotos | Unrestricted | ~6000 px | https://catalog.archives.gov/id/74254228 (ex.) |
| 8 | Galeria NHHC "Tinian Landings" | E fotos | PD | — | https://www.history.navy.mil/browse-by-topic/wars-conflicts-and-operations/world-war-ii/1944/guam-tinian/tinian-gallery.html |
| 9 | Carregamento da Little Boy no B-29, 5 ago 1945 (NARA 77-BT) ⇄ #20 | E foto | PD | 3675×2563 | https://commons.wikimedia.org/wiki/File:Loading_of_the_Little_Boy_nuclear_bomb_into_the_Boeing_B-29_on_Tinian,_Mariana_Island,_5_August_1945_(76048611).jpg |
| 10 | A Little Boy no carrinho, ago 1945 | E foto | PD | 2354×2618 | https://commons.wikimedia.org/wiki/File:Atombombe_Little_Boy_2.jpg |
| 11 | Tripulação do Enola Gay | E foto | PD | 3668×2787 | https://commons.wikimedia.org/wiki/File:Crew_of_the_Enola_Gay.jpg |
| 12 | Quartel-general do 509th Composite Group em Tinian (342-FH) | E foto | Unrestricted | — | https://catalog.archives.gov/id/204976343 |
| 13 | Briefing do 509th em Tinian (342-FH) | E foto | Unrestricted | — | https://catalog.archives.gov/id/204974377 |
| 14 | Campos de pouso de Tinian, 1945, vista N→S ⇄ #21 | E foto | PD | 1302×985 | https://commons.wikimedia.org/wiki/File:Tinian_Airfields_1945_Looking_North_To_South.jpg |
| 15 | B-29 do 505th BG em North Field, jul 1945 | E foto | PD | 933×496 (baixa) | https://commons.wikimedia.org/wiki/File:505th_Bombardment_Group_B-29s_North_Field_Tinian_July_1945.jpg |
| 16 | **D** Carta "Saipan-Tinian Area" (RG 38) | D mapa | Unrestricted | 7,7 MB | https://catalog.archives.gov/id/55302628 |
| 17 | **D** "Tinian: Port Plan and Berthing Diagram" | D mapa | Unrestricted | — | https://catalog.archives.gov/id/502849426 |
| 18 | **D** "Commander Tinian Island – Report of Capture and Occupation of Tinian" (datilografado) | D texto | Unrestricted | — | https://catalog.archives.gov/id/78605496 |
| 19 | **D** "Notes of Captain Robert Lewis, Co-Pilot of the Enola Gay" (manuscrito; efeito grifo forte) | D texto | Unrestricted na NARA (manuscrito privado: citar a NARA) | — | https://catalog.archives.gov/id/22349277 |
| 20 | Generais JASDF e USAF no poço de carga nº 1 da bomba, North Field, 2020 ⇄ #9 | H foto | PD (DVIDS) | 4654×2909 | https://commons.wikimedia.org/wiki/File:JASDF_and_USAF_generals_at_No.1_atomic_bomb_loading_pit,_North_Field,_Tinian_during_Cope_North_2020.jpg |
| 21 | Lançamento aéreo recuperado em North Field, Cope North 2022 ⇄ #14 | H foto | PD | 8256×5504 | https://commons.wikimedia.org/wiki/File:Recovering_airdrop_on_North_Field,_Tinian_during_Cope_North_2022.jpg |
| 22 | CH-47 e UH-60 em North Field, Forager 21 | H foto | PD | 5577×3718 | https://commons.wikimedia.org/wiki/File:CH-47s_and_UH-60_at_North_Field,_Tinian_during_Forager_21.jpg |
| 23 | "Historic landing begins", Forager Fury 2012: fuzileiros desembarcando de novo em Tinian ⇄ #6 | H foto | PD | ~4752×3168 | https://commons.wikimedia.org/wiki/File:Historic_landing_begins_Forager_Fury_2012_121128-M-RQ061-003.jpg |
| 24 | Ficha NHL "Tinian Landing Beaches, Ushi Point Field, North Field" (NPS) | D/H texto | Restricted-Possibly (texto NPS = PD) | PDF | https://catalog.archives.gov/id/131518067 |

### Corregidor: 21 itens

| # | Item | Tipo | Licença | Resolução | URL |
|---|---|---|---|---|---|
| 1 | *Appointment in Tokyo* (1945, Army: queda e retomada das Filipinas) | E filme | PD (DoD) | — | https://archive.org/details/gov.dod.dimoc.20379 |
| 2 | "U.S. Troops Return to Corregidor" (cinejornal Universal, fev 1945) | E filme | CC0/PD (Universal Newsreel na NARA) | — | https://archive.org/details/gov.archives.arc.39053 |
| 3 | NARA 428-NPC-8836 e 8837 "Bombardment of Corregidor" | E filme | **Unrestricted** | — | https://catalog.archives.gov/id/78626 · https://catalog.archives.gov/id/78627 |
| 4 | NARA 428-NPC-8781 "Invasion of Corregidor" | E filme | Unrestricted | — | https://catalog.archives.gov/id/78608 |
| 5 | Lateral nº 12 do túnel Malinta durante o cerco, 1942 (SC 249636) ⇄ #19 | E foto | PD | — | https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/SC-249000/SC-249636.html |
| 6 | MacArthur e Sutherland no QG do túnel Malinta, mar 1942 | E foto | PD | 6156×4828 | https://commons.wikimedia.org/wiki/File:MacArthur_and_Sutherland_s265357.jpg |
| 7 | Paraquedistas descendo sobre Corregidor, 16 fev 1945 (SC 201368) | E foto | PD | 3993×5136 | https://commons.wikimedia.org/wiki/File:SC_201368_-_American_paratroopers_float_down_upon_Corregidor,_P.I.,_during_the_Allied_invasion_of_the_island._16_February,_1945._(53005697169).jpg |
| 8 | Paraquedistas pousando em Corregidor (342-FH) | E foto | Unrestricted | — | https://catalog.archives.gov/id/204951307 |
| 9 | Fort Mills, Corregidor (111-SC-97414-1) | E foto | Unrestricted | — | https://catalog.archives.gov/id/329575844 |
| 10 | Malinta Hill (342-FH-3A30054) | E foto | Unrestricted | — | https://catalog.archives.gov/id/204949186 |
| 11 | Face norte com os canhões em caverna, sob fogo do USS Phoenix (NH 122203) | E foto | PD | — | https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/NH-122000/NH-122203.html |
| 12 | LCS-8 dando apoio enquanto C-47 lançam paraquedistas (80-G-273351) | E foto | PD | — | https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/80-G-273000/80-G-273351.html |
| 13 | Doca de Corregidor olhando para Bataan, anos 1940 (NH 44658) | E foto | PD | — | https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/NH-44000/NH-44658.html |
| 14 | Rendição americana, mai 1942 (foto **japonesa**) | E foto | ⚠ Commons diz PD; status nos EUA incerto (URAA). Evitar ou usar com nota | 1024×644 | https://commons.wikimedia.org/wiki/File:Americans_Surrender_Bataan.jpg |
| 15 | **D** "Roads and Trails, Corregidor Island" (SWPA) | D mapa | Unrestricted | — | https://catalog.archives.gov/id/157669542 |
| 16 | **D** Mapas de situação D+1, D+2, D+3… D+13 da retomada (SWPA): sequência animável | D mapa | Unrestricted | 6752×6019 (amostra) | https://catalog.archives.gov/id/157669554 (D+1) · https://catalog.archives.gov/id/157669544 (D+13) |
| 17 | **D** Diário do 1º Ten. Frank J. Sauter (prisioneiro de guerra) | D texto | Unrestricted | — | https://catalog.archives.gov/id/12448564 |
| 18 | Marco histórico na entrada do túnel Malinta (DoD, 1997) | H foto | PD | 2893×1948 | https://catalog.archives.gov/id/6494909 |
| 19 | Túnel Malinta hoje, 2011 ⇄ #5 | H foto | **CC BY 2.0** (crédito) | 3008×2000 | https://commons.wikimedia.org/wiki/File:Malinta_Tunnel_(6948577310).jpg |
| 20 | Bateria Hearn, vista moderna | H foto | PD | 1500×1176 | https://commons.wikimedia.org/wiki/File:Battery_Hearn,_Corregidor_Island_(modern_view).jpg |
| 21 | Fuzileiros dos EUA em Corregidor no Balikatan 2009 / Pacific War Memorial | H foto | PD / CC BY 2.0 | 1280×853 / 3008×2000 | https://commons.wikimedia.org/wiki/File:USMC-090425-M-7590G-004.jpg · https://commons.wikimedia.org/wiki/File:Pacific_War_Memorial_(6940586861).jpg |

### Bikini Atoll / Operation Crossroads: 20 itens

| # | Item | Tipo | Licença | Resolução | URL |
|---|---|---|---|---|---|
| 1 | *Operation Crossroads*, partes I e II (filme oficial da Marinha, 1946/49) | E filme | PD (Prelinger: preferir a cópia NARA/DOE por causa do Content ID) | — | https://archive.org/details/Operatio1946 · https://archive.org/details/Operatio1946_2 |
| 2 | *Nuclear Test Film – Project Crossroads* (DOE) | E filme | PD | — | https://archive.org/details/gov.doe.0800002 |
| 3 | NARA 428-NPC-18258 "Operation Crossroads" (série com dezenas de rolos 428-NPC-187xx–189xx) | E filme | Undetermined | mp4 | https://catalog.archives.gov/id/80964 |
| 4 | Cinejornal Universal "First Pictures Atomic Blast!", 8 jul 1946 | E filme | PD (Universal Newsreel) | — | https://archive.org/details/1946-07-08_First_Pictures_Atomic_Blast |
| 5 | NARA 111-DD-278-69 "Bikini Atoll… being cleaned up so islanders can return" (1969) | E/H filme | Restricted-Possibly (Army): conferir | — | https://catalog.archives.gov/id/102043796 |
| 6 | Explosão Baker, 25 jul 1946 (coluna e nuvem de Wilson) | E foto | PD | 5137×2696 | https://commons.wikimedia.org/wiki/File:Operation_Crossroads_Baker_Edit.jpg |
| 7 | Nuvem do teste Able, 1 jul 1946 (NH 85804-KN) | E foto | PD | 4579×5776 | https://commons.wikimedia.org/wiki/File:Able_test_atomic_bomb_cloud_on_1_July_1946_(NH_85804-KN).jpg |
| 8 | Marinheiros assistindo à nuvem Able do USS Fall River (80-G-627452) | E foto | PD | — | https://commons.wikimedia.org/wiki/File:Sailors_watch_the_Able_test_atomic_bomb_cloud_from_USS_Fall_River_(CA-131),_1_July_1946_(80-G-627452).jpg |
| 9 | Vista aérea colorida da frota-alvo na laguna, jul 1946 (80-G-K-20268) ⇄ #19 | E foto | PD | — | https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/80-G-K-20000/80-G-K-20268.html |
| 10 | Baker visto do USS Mt. McKinley (80-G-627521) | E foto | PD | — | https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/80-G-627000/80-G-627521.html |
| 11 | Dano no submarino USS Skate (80-G-627500) | E foto | PD | — | https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/80-G-627000/80-G-627500.html |
| 12 | Jornalistas vendo o USS Independence destruído (80-G-627512) | E foto | PD | — | https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/80-G-627000/80-G-627512.html |
| 13 | Série NARA 374-ANT "Project 18 – Operation Crossroads" (detonação e atividades) | E fotos | Unrestricted | — | https://catalog.archives.gov/id/146763012 |
| 14 | Avanço da onda de choque do teste Able (434-LB) | E foto | Unrestricted | — | https://catalog.archives.gov/id/22118342 |
| 15 | Smithsonian: 1.268 imagens com "Operation Crossroads"/Bikini (filtrar CC0) | E fotos | CC0 nos marcados | — | https://www.si.edu/search/collection-images?edan_q=%22Operation%20Crossroads%22 (busca; conferir o ícone CC0) |
| 16 | **D** Cartas de campo "Bikini Atoll, Northeastern Part" e "Eastern Part" (RG 37) | D mapa | Unrestricted | 6,4 MB | https://catalog.archives.gov/id/152774653 · https://catalog.archives.gov/id/152774657 |
| 17 | **D** "The Evaluation of the Atomic Bomb as a Military Weapon – Final Report" (JCS, Biblioteca Truman) | D texto | Unrestricted | — | https://catalog.archives.gov/id/310989451 |
| 18 | **D/H** *The Archeology of the Atomic Bomb* (NPS, 1991: fotos submarinas do Saratoga, Nagato etc.) | D/H relatório | PD (NPS) | PDF | https://commons.wikimedia.org/wiki/File:The_Archeology_of_the_Atomic_Bomb,_National_Park_Service,_Santa_Fe,_New_Mexico,_1991_by_Delgado,_James_P.,_et_al._-_NNPS_903_D160_-38840-pg0000.pdf |
| 19 | Bikini por Landsat 7, 14 jan 2001 (cratera Bravo visível) ⇄ #9 | H satélite | PD (USGS) | 3096×1952 | https://commons.wikimedia.org/wiki/File:Bikini_Atoll_2001-01-14,_Landsat_7_ETM%2B.png |
| 20 | Bikini Atoll, 2017 (satélite, altíssima resolução) | H satélite | **CC BY 2.0** (crédito) | 15182×15482 | https://commons.wikimedia.org/wiki/File:Bikini_Atoll,_Marshall_Islands_(35055478541).jpg |

**Lacuna do Bikini:** falta foto atual em terra (as ilhas, as casas abandonadas, o mergulho nos naufrágios). As fotos de mergulho são CC BY-SA ou privadas. Saídas possíveis: Landsat/Sentinel recente (Sentinel exige o crédito "contains modified Copernicus Sentinel data") e relatórios DOE/LLNL do Marshall Islands Program (PD, a conferir).

**Recomendação de material:**
- **Midway**: tem o filme de época mais famoso (Ford, PD), os pares então × agora mais fortes, documento datilografado do Nimitz e "hoje" 100% PD (USFWS). E o acesso é fechado ao público, o que casa com o "Why can't you visit".
- **Tinian** fica em 2º, com o gancho atômico e o DVIDS forte. Opção de piloto equivalente.

## Regras práticas para o canal

1. **Um `licencas.md` por vídeo** (em `videos/NNN-slug/`), com uma linha por item usado: id interno do clipe, URL da página oficial (NARA `catalog.archives.gov/id/…`, NHHC, DVIDS, arquivo do Commons), id da fonte (80-G-…, NH …, 428-NPC-…, VIRIN do DVIDS), licença como está na página, crédito exigido e data de acesso. Para Commons CC BY, anotar também autor e versão da licença. Guardar um print ou PDF da página só para itens CC ou de status duvidoso (fica fora do git, junto da mídia).
2. **Baixe da fonte oficial, não do reupload.** Filme: a cópia da NARA (`catalog.archives.gov/medialz/...mp4`), do DOE ou do DVIDS, não a da Periscope Film ou do YouTube. Isso facilita provar a origem e evita versões remasterizadas que têm dono.
3. **Crédito:**
   - Na descrição, sempre o bloco "SOURCES & CREDITS", no molde do vídeo de referência de Iwo Jima: filmes por título e órgão, "via the Internet Archive" quando for o caso, "U.S. government works are in the public domain", e a lista dos CC BY com autor, link e licença.
   - Na tela, crédito curto em todo CC BY/BY-SA e em todo material do governo do Japão (GSI: "Source: GSI, edited").
   - Para PD, o crédito na tela é opcional. Use "National Archives" / "U.S. Navy" quando ajudar a credibilidade ("documento que você não devia ver").
4. **Nunca usar:**
   - IWM (não comercial).
   - Trecho de TV, documentário de terceiros ou vídeo de outro YouTuber.
   - Getty, AP Images, Magnum (ex.: fotos do Dia D de Robert Capa), Corbis/Bettmann, Alamy.
   - **Colorizações modernas**: a cor é obra nova com copyright, ex.: "Operation Crossroads Baker in color" no Commons, de 2009. Prefira o P&B original ou colorize você mesmo.
   - Cinejornal comercial pós-1929 que não seja Universal (Paramount, Fox Movietone, Hearst/Pathé).
   - Filme de Hollywood "no IA", ainda que marcado PD.
   - Música e narração originais de terceiros por cima de filme PD.
   - Foto de agência sem prova de PD.
   - Fotos japonesas de época sem conferir.
5. **Faixas de risco:**
   - **Verde**: NARA "Unrestricted", NHHC sem "courtesy", DVIDS com rodapé PD, NPS, USFWS, USGS, NASA, Smithsonian CC0.
   - **Amarelo**: NARA "Restricted - Possibly"/"Undetermined" (assista e confira se há trecho de cinejornal comercial), Commons CC BY, governo do Japão com crédito, Rosenthal.
   - **Vermelho**: o resto.
6. **Content ID em filme PD:**
   - Espere reclamações (agregadores de "stock footage" registram filmes PD).
   - Antes de publicar, não use as primeiras e últimas cartelas de quem reenviou e prefira a cópia NARA/DOE.
   - Se vier reclamação: (a) confira na lista do `licencas.md` qual clipe é; (b) conteste no YouTube Studio como "domínio público" ([guia do YouTube](https://support.google.com/youtube/answer/2797454)), citando a URL e o id da NARA ("U.S. Navy film, 1942, work of the U.S. Government, 17 U.S.C. §105; source: National Archives identifier …"); (c) o reclamante tem 30 dias, e se ele mantiver, avalie recorrer ou cortar o trecho (recorrer arrisca um strike se virar takedown).
   - Não conteste no impulso: disputa abusiva é penalizada.
7. **Material atual** (o "hoje" do lugar), em ordem de preferência: DVIDS (PD, alta resolução), NPS/USFWS, NASA/USGS (ISS, Landsat), governo do Japão com crédito, Commons CC BY (com crédito), e por último CC BY-SA isolado. Tema sem nenhum "hoje" livre (ex.: Area 51, Hashima) não vira pauta, ou vira só com satélite e mapa desenhado.
8. **Antes de fechar a pauta**, confira: (a) ≥ 1 filme de época PD; (b) ≥ 15 fotos de época em ≥ 3.000 px; (c) ≥ 1 documento legível; (d) ≥ 5 imagens atuais livres; (e) ≥ 1 par então × agora. Midway, Tinian e Bikini passam. Corregidor passa no limite (o "hoje" é CC BY).
