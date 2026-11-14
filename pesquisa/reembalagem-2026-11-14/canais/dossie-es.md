# Reembalagem dossie-es (Dossier en Minutos): pesquisa + propostas (14/11/2026)

**Base:** Studio 28 d até 13/11 (CTR do canal 2,8%, retenção 59%). Bíblia `canais/dossie-es/biblia/` (README, titulo.md, thumb.md), `pesquisa/gap-2026-11-14/canais/dossie-es.md`, `pesquisa/benchmark-2026-11-14/dados/videos-90d.csv` (reaproveitado: Archive, Atlas, Te lo Pinto, Archivo Desclasificado, clones).
**Busca nova:** 31 consultas yt-dlp via WARP em es (sem cota): 19 de tema + 12 de ângulo/anedota. Depois `videos.list` + `channels.list` + mediana dos últimos ≤30 uploads longos (≥3 min) de cada canal citado (`playlistItems`). **`search.list`: 0** (~173 unidades de cota no total). Views de 14/11/2026.
**Dados:** `dados/dossie-es/busca-enriquecida.csv` (750 vídeos), `referencias.csv` (os citados, com mediana), `canais-medianas.json`, `busca/*.jsonl`, `thumbs/`, `scripts/`. **Mosaicos:** `mosaicos/dossie-es-<NNN-slug>.jpg` (1º quadro com borda azul = nossa thumb atual).
Legenda: "> med" = views acima da mediana do canal dele (✓/✗). v/i = views/inscritos.

---

## 1. Padrões do nicho (es; en só como apoio)

### Títulos
| # | Padrão (estrutura · gatilho) | Vídeos reais (views · data · > med) |
|---|---|---|
| **T1** | **"TODA la Historia de [org] en N Minutos \| [subtítulo próprio]"**: promessa de completude curta + subtítulo que nomeia o lado temido/escondido. Afirmação, 70–90 car., Title Case | Atlas [Mossad](https://youtu.be/9LyvAHVecwY) 85.994 · 01/11 · ✓ (med 1,4 mil); Atlas [CIA vs KGB](https://youtu.be/dXRO17KlRUw) 100.373 · 02/11 · ✓; Atlas [KGB](https://youtu.be/t0EBZqMWi1o) 44.515 · 28/10 · ✓; Historia Total [Israel](https://youtu.be/POmNWlQfk40) 852.395 · 12/10 · ✓ (med 404); Te lo Pinto [KGB](https://youtu.be/by7uTDjSx7Y) 246.737 · 30/10 · ✓ (med 163 mil) |
| **T2** | **"Cómo [org/sujeito] [verbo concreto] [alvo inesperado]"**: uma operação concreta, sem entregar o desfecho. 55–100 car. | Espía Real [francotirador en el Tigris](https://youtu.be/auxFOGVrS4Q) 393.826 · 29/04 · ✓ (med 21 mil); Espía Real [ejército dentro de Irán](https://youtu.be/BaDDQZEcKH8) 176.468 · 08/05 · ✓; Archivos de la 2ª GM [avión más peligroso de la URSS](https://youtu.be/GUtFyu4d9bE) 158.385 · 20/12/2025 · ✓ (med 4,1 mil); Dossier Global [MiG-21](https://youtu.be/FEV_up1iv2U) 94.321 · 08/11/2025 · ✓ (med 10 mil); Mossad Oculto [Eichmann por un ramo de flores](https://youtu.be/VXBP7zImGgg) 109.113 · 11/10 · ✓ (med 394); El Rastro Criminal [Cómo el FBI capturó a Larry Gene Bell](https://youtu.be/p0Wg9WsEAZ0) 141.889 · 26/05 · ✓ (med 8,9 mil) |
| **T3** | **"[Lugar/Nome] [ano]: la operación/el caso que…"** (cabeçalho de expediente + aposto). É o nosso "dossiê" dito no título | Archivo Desclasificado [Proyecto Azorian: la operación secreta de la CIA…](https://youtu.be/05BXuSKJzlM) 67.641 · 28/10 · ✓ (med 33 mil); [Operación Ajax: el golpe de 1953 en Irán](https://youtu.be/Dzi7wyQRlKw) 56.136 · 06/11 · ✓; [Richard Sorge: el espía que avisó a Stalin…](https://youtu.be/4ZGaCBkQpzY) 129.010 · 27/10 · ✓; [Klaus Fuchs: el espía que entregó la bomba…](https://youtu.be/gCrJYsGI8sE) 59.044 · 05/11 · ✓; Dustmind [Guatemala 1954: La operación secreta de la CIA…](https://youtu.be/_vtKg8FGCmA) 33.150 · 01/11 · ✓ (no limite: med 33.138); El Archivo Secreto [Guatemala 1954: Cómo la CIA derrocó…](https://youtu.be/vuGJBtnCYe0) 18.986 · 07/08 · ✓ (med 5,6 mil) |
| **T4** | **"[Nome]: el [papel] que [ação]"** (pessoa como porta da organização) | World View [Corleone: el Padrino más Poderoso…](https://youtu.be/3M6xlSqu1cQ) 645.075 · 02/11/2025 · ✓ (med 36 mil); Relato Mafioso [Vito Genovese: El Jefe que NADIE…](https://youtu.be/Q3gRYpKRubw) 172.776 · 30/06 · ✓ (med 38 mil); Archivo Desclasificado Sorge e Fuchs (acima) ✓. **Contra-evidência:** Cruzada Hostil [Tommaso Buscetta: El Mafioso que HIZO TEMBLAR…](https://youtu.be/3-8MwLiV9jo) 27.788 · ✗ (med 38 mil) |
| T5 | "Lo que nadie se atreve a contar / La historia oculta / que NO te contaron" | El Canal del Coronel [Mossad](https://youtu.be/CAqIOdWdfvk) 291.845 · ✓; Solo Fonseca [CIA](https://youtu.be/Nc1hreDOwmQ) 1.079.407 · ✓; Historia Incomprendida [Masones](https://youtu.be/mukgvolxlrE) 134.920 · ✓; Tus Noches de Historia [Masones](https://youtu.be/-j2TaRzM7N0) 174.896 · ✓. **Não usei:** já é fórmula gasta dos podcasts e canais grandes, e prometer "lo que nadie cuenta" num vídeo que cita fontes públicas seria exagero |
| T6 | "Así Funciona(ba) por Dentro X" / "Tu Vida en Cada Rango de X" / "X vs Y" | Te lo Pinto [Policía Nazi por dentro](https://youtu.be/oWkkPoYFC5o) 200.151 · ✓; [Sistema del FBI](https://youtu.be/9f7tNIgZsak) 748.692 · ✓; POV Rangos [KGB](https://youtu.be/TIh8QUZtWxQ) 68.137 · ✓; Te lo Pinto [FBI vs CIA](https://youtu.be/kEfEQYeY2I0) 181.669 · ✓. **Não usei:** os nossos 6 vídeos são cronologia por casos, não hierarquia, funcionamento interno nem duelo. A promessa não seria paga (bom para vídeos novos) |

**O que os títulos que funcionam têm em comum:** (1) nomeiam a organização famosa nas primeiras 3 palavras; (2) trazem **um objeto ou um caso concreto** (MiG, Tigris, ramo de flores, submarino) ou um **subtítulo que promete o escondido**; (3) não entregam o desfecho. O clone **Archivo en Minutos** usa o nosso título letra por letra ("La historia COMPLETA del X en N minutos", caixa baixa, sem subtítulo) e tem mediana de 355 views: [Mosad](https://youtu.be/1F7enXW5lvY) 145, [KGB](https://youtu.be/OVTHfwip3CY) 355. Em en, a versão "minute by minute" da operação no **Spies in Minutes** (mediana 12) também não decola: [Eichmann](https://youtu.be/g8gaRXS18q4) 12 views. Ou seja, **o padrão sozinho não carrega**: precisa de tema famoso + objeto concreto + thumb forte.

### Thumbs
| # | Padrão | Vídeos reais (views · > med) |
|---|---|---|
| **H1** | **Rosto real e famoso em ilustração**, meio corpo, com objeto na mão, fundo claro e quente, sigla preta gigante + datas | Archive [CIA (Dulles + cachimbo)](https://youtu.be/sIGKXDi6YY8) 216.211 ✓; Archive [KGB (Putin + pasta)](https://youtu.be/VNJhu4rh6OY) 247.064 ✓; Te lo Pinto [KGB](https://youtu.be/by7uTDjSx7Y) 246.737 ✓; History Exposé [Hoover (foto)](https://youtu.be/470bUPjlKXQ) 292.627 ✓ (med 40 mil). **Contra:** Archive [FBI (Hoover cartoon)](https://youtu.be/gEOavheqCKM) 16.196 ✗ |
| **H2** | **Objeto-símbolo dominante** (o "corpo de delito" do caso) ocupando metade do quadro, 0–4 palavras, luz quente | Archivos de la 2ª GM [MiG-21 + "OPERACIÓN DIAMANTE"](https://youtu.be/GUtFyu4d9bE) 158.385 ✓; Dossier Global [MiG + agente](https://youtu.be/FEV_up1iv2U) 94.321 ✓; Archivo Desclasificado [Azorian (garra/navio)](https://youtu.be/05BXuSKJzlM) 67.641 ✓; en: Mossad Ops [MiG-21 ao pôr do sol](https://youtu.be/60rQZgHqMqE) 905.534 ✓ (med 42 mil) |
| **H3** | **Retrato tipo ficha policial do chefe real** + nome/palavra grande embaixo | World View [Corleone (fichas P&B)](https://youtu.be/3M6xlSqu1cQ) 645.075 ✓; Relato Mafioso [Vito Genovese](https://youtu.be/Q3gRYpKRubw) 172.776 ✓; Mafia Secreta [Riina + juízes](https://youtu.be/l1vOy0zFAdY) 50.429 ✓ (med 2,6 mil) |
| **H4** | **Galeria de rostos históricos reconhecíveis** (próceres, presidentes) + pergunta curta | El Historiador Nocturno [San Martín, Churchill, Bolívar, Juárez + "¿ELLOS CONTROLAN EL MUNDO?"](https://youtu.be/vWyu2T7P038) 190.542 ✓ (med 22 mil); Historia Incomprendida [Washington + pirâmide do dólar](https://youtu.be/mukgvolxlrE) 134.920 ✓; SLICE Historia [CIA: Castro, Kennedy, Pinochet…](https://youtu.be/pOi_lbsm5iE) 344.729 ✓ (med 42 mil) |
| H5 | Duelo: 2 rostos + "VS" | Atlas [CIA vs KGB](https://youtu.be/dXRO17KlRUw) 100.373 ✓; Te lo Pinto [FBI vs CIA](https://youtu.be/kEfEQYeY2I0) 181.669 ✓ (não se aplica aos 6) |

**Comum aos que funcionam (olhado nos mosaicos):** 1 foco que se reconhece em meio segundo (rosto famoso **ou** objeto do caso); fundo claro/quente (céu de fim de tarde, sépia, papel); 1–3 palavras grandes. Já as nossas trazem um agente inventado e faixas pequenas ("EL PARAGUAS", "EL JURAMENTO") que somem a 320×180 (gap §3). **Atenção:** os 3 KGB de referência usam Putin, mas o nosso KGB não fala de Putin. Pôr Putin na thumb seria promessa não paga, por isso não proponho.

**Regra comum às 6 thumbs abaixo (identidade):** graphic novel em tinta com contorno preto, **fundo papel `#E9DFC9` ou céu ocre de fim de tarde** (nada de ardósia dominante nem de céu azul chapado do Archive), sigla em Bebas/Oswald preta sobre área clara, **1 sello vermelho `#B3261E`** inclinado e **aba "EXPEDIENTE Nº 00X" 2× maior** no canto superior direito (assinatura; não conta como texto de leitura). Sem sangue, cadáver, caveira, suástica nem arma apontada.
**Desvio da bíblia (vale para as 6):** o sello deixa de levar o período ("1947–HOY") e passa a levar **1–2 palavras de lacuna**. A bíblia (`thumb.md`) manda o sello com o período, mas a 320×180 a data não promete nada; as referências que rendem usam a palavra para criar a pergunta (gap §3). O período pode ir pequeno dentro da aba. Nas propostas com rosto real que **não é um chefe da organização** (Castro, Buscetta, próceres), há também desvio do "chefe ou agente arquetípico" da bíblia, porque o atalho de "pouco conhecimento prévio" (`decisao-do-clique.md`) pede um rosto conhecido. Nenhuma foto: o rosto é ilustrado em tinta.

---

## 2. Por vídeo

### 002 Mossad · `it37m7pz0hI`
**Atual:** "La historia COMPLETA del Mossad en 14 minutos" · 6.287 impr · CTR 2,6% · ret. 54% · 13:43. Mosaico `mosaicos/dossie-es-002-mossad.jpg`.

**Top referências (mesmo tema)**
| Link | Canal | Inscr. | Views | Data | v/i | > med |
|---|---|---|---|---|---|---|
| [z-0I92HGceY](https://youtu.be/z-0I92HGceY) (podcast) | Tiene Sentido | 1,06 mi | 1.247.811 | 28/09 | 1,18 | ✓ |
| [w__qztgNJME](https://youtu.be/w__qztgNJME) | Solo Fonseca | 1,37 mi | 829.455 | 16/03 | 0,61 | ✓ |
| [voB5-JDMmC8](https://youtu.be/voB5-JDMmC8) venganzas contra nazis en Sudamérica | Der Kommandant | 259 mil | 448.156 | 15/07 | 1,73 | ✓ |
| [auxFOGVrS4Q](https://youtu.be/auxFOGVrS4Q) | Espía Real | 36,7 mil | 393.826 | 29/04 | 10,7 | ✓ |
| [CAqIOdWdfvk](https://youtu.be/CAqIOdWdfvk) | El Canal del Coronel | 994 mil | 291.845 | 23/09 | 0,29 | ✓ |
| [4hPWMjaOw4Q](https://youtu.be/4hPWMjaOw4Q) (en) | Archive in Minutes | 21,5 mil | 272.163 | 27/10 | 12,7 | ✓ |
| [GUtFyu4d9bE](https://youtu.be/GUtFyu4d9bE) avión de la URSS | Archivos de la 2ª GM | 25 mil | 158.385 | 20/12/2025 | 6,3 | ✓ |
| [FEV_up1iv2U](https://youtu.be/FEV_up1iv2U) MiG-21 | Dossier Global | 7,4 mil | 94.321 | 08/11/2025 | 12,8 | ✓ |
| [9LyvAHVecwY](https://youtu.be/9LyvAHVecwY) | Atlas del Tiempo | 1,8 mil | 85.994 | 01/11 | 48,9 | ✓ |
| [60rQZgHqMqE](https://youtu.be/60rQZgHqMqE) (en) MiG-21 | Mossad Ops | 24,7 mil | 905.534 | 25/03 | 36,7 | ✓ |

**O que o vídeo entrega (legendas.srt)**
- **0:00–0:31** "Un piloto de la fuerza aérea iraquí despega en un MiG veintiuno… Y aterriza en Israel… La había planeado el Mossad." (o hook paga o T2 e a thumb em 30 s)
- 1:14 "Durante décadas, Israel ni siquiera publica el nombre de su jefe."
- 2:34–3:16 Eichmann, ônibus 203, San Fernando: "Lo esconden nueve días en una casa alquilada."
- 6:27–7:00 "El MiG… Al aterrizar, el avión recibe un nuevo número: cero cero siete."
- 8:26–9:02 Lillehammer, o garçom confundido: "Israel indemniza a la viuda… sin admitir responsabilidad."
- 11:54–12:05 Vanunu escreve na mão; "Israel, hasta hoy, no confirma ni niega tener armas nucleares."
- 13:03–13:13 "el MiG… Todavía lleva pintado el número cero cero siete."

**Proposta**
- **Título 1 (T1, molde + subtítulo):** **TODA la Historia del Mossad en 14 Minutos | Los Expedientes que Israel Nunca Confirmó** (85 car.). Refs T1: Atlas Mossad 85.994 (01/11, ✓) · Historia Total Israel 852.395 (12/10, ✓). Pago: 1:14, 8:57, 12:05.
- **Título 2 (T2, "Cómo" + operação concreta):** **Cómo el Mossad Hizo Aterrizar un MiG Soviético en Israel** (56 car.). Refs T2: Archivos de la 2ª GM 158.385 (20/12/2025, ✓) · Dossier Global 94.321 (08/11/2025, ✓) · Espía Real 393.826 (29/04, ✓). Mesmo caso, frase diferente: não copia nenhum deles. Pago: 0:00–0:31 e 6:27–7:00.
- **Thumb (H2, objeto dominante):** o **MiG-21 prateado, em tinta**, em diagonal da esquerda para o centro, trem de pouso baixado sobre pista de deserto, ocupando ~55% do quadro; na deriva, **"007"** pintado em preto. Pequeno, ao pé da escada, um piloto de capacete debaixo do braço, de costas (sem rosto). Céu **ocre de fim de tarde** clareando para o papel `#E9DFC9` à direita. Texto: **"MOSSAD"** preto gigante no alto à direita + sello vermelho **"Nº 007"** inclinado (2 palavras). Promete: "por que um caça soviético tem 007 e está em Israel?". Conversa com os títulos: o T2 conta o "como" sem mostrar o número; o T1 fala de expedientes não confirmados e a thumb mostra um deles. Pagamento: 0:00–0:31 e 6:51–6:54 (o "007"), de novo em 13:13. Refs H2: Archivos de la 2ª GM (MiG + "OPERACIÓN DIAMANTE") 158.385 ✓ · Dossier Global (MiG + agente) 94.321 ✓ · Mossad Ops (en, MiG ao pôr do sol) 905.534 ✓. Sem rosto famoso porque o Mossad não tem um que o público de es reconheça; Archive (272 mil) e Atlas (86 mil) também usam agente anônimo. **Não prometer a "espiã sedutora"** do Mossad Ops: o nosso vídeo não fala dela.

### 001 CIA · `Qs-TusYCr-o`
**Atual:** "La historia COMPLETA de la CIA en 12 minutos" · 884 impr · 3,2% · 66% · 11:47. Mosaico `mosaicos/dossie-es-001-cia.jpg`.

| Link | Canal | Inscr. | Views | Data | v/i | > med |
|---|---|---|---|---|---|---|
| [Nc1hreDOwmQ](https://youtu.be/Nc1hreDOwmQ) historia oculta de la CIA | Solo Fonseca | 1,37 mi | 1.079.407 | 14/04 | 0,79 | ✓ |
| [ZvMVySLzdEo](https://youtu.be/ZvMVySLzdEo) CIA… en América Latina | Inna Afinogenova | 742 mil | 651.883 | 29/04 | 0,88 | ✓ |
| [pOi_lbsm5iE](https://youtu.be/pOi_lbsm5iE) guerras ocultas de la CIA | SLICE Historia | 223 mil | 344.729 | 26/09 | 1,55 | ✓ |
| [sIGKXDi6YY8](https://youtu.be/sIGKXDi6YY8) (en) | Archive in Minutes | 21,5 mil | 216.211 | 20/10 | 10,1 | ✓ |
| [dXRO17KlRUw](https://youtu.be/dXRO17KlRUw) CIA vs KGB | Atlas del Tiempo | 1,8 mil | 100.373 | 02/11 | 57,0 | ✓ |
| [BQBOwB_2v5I](https://youtu.be/BQBOwB_2v5I) Guatemala por un plátano | Kin | 149 mil | 85.762 | 08/03 | 0,58 | ✗ (med 227 mil) |
| [_vtKg8FGCmA](https://youtu.be/_vtKg8FGCmA) Guatemala 1954 | Dustmind | 5,5 mil | 33.150 | 01/11 | 6,0 | ✓ (limite) |
| [vuGJBtnCYe0](https://youtu.be/vuGJBtnCYe0) Guatemala 1954 | El Archivo Secreto | 11,5 mil | 18.986 | 07/08 | 1,65 | ✓ |

**O que o vídeo entrega**
- **0:00–0:31** "una radio clandestina anuncia que miles de rebeldes avanzan… Los miles de rebeldes eran menos de quinientos. Y la radio… la operaba la CIA… Y de lo que hizo, una y otra vez, en América Latina." (paga T1 e T2 no 1º minuto)
- 3:37–4:22 PB Success: "la Voz de la Liberación convierte a unos cientos de hombres en un ejército imparable… Guarda esa radio."
- 4:33–5:29 MK Ultra (Dulles aprova em 1953).
- 6:19–6:57 Bahía de Cochinos: "Allen Dulles… deja la CIA ese mismo año."
- **7:05–7:44** "Los Puros… al menos ocho planes… una caja de puros envenenados… Cuba asegura que sobrevivió a más de seiscientos intentos."
- 7:45–8:37 Chile: "hacer que la economía chilena grite."
- 10:55–11:22 Clinton na Guatemala: "fue un error"; o perdão à família de Árbenz.

**Proposta**
- **Título 1 (T1):** **TODA la Historia de la CIA en 12 Minutos | Lo que Hizo en América Latina** (72 car.). Refs T1: Atlas CIA vs KGB 100.373 (02/11, ✓) · Atlas KGB 44.515 (28/10, ✓). Demanda do ângulo AL: Inna Afinogenova 651.883 (✓) · SLICE 344.729 (✓). Pago: 0:31, 3:37, 6:19, 7:05, 7:45, 10:55. **Ressalva:** o clone Mapa del Ayer ("…de la CIA en América Latina en 17 Minutos", canal com 0 inscritos) fez 1 view. O ângulo AL em si ainda não está provado **dentro do molde**.
- **Título 2 (T3, expediente datado):** **Guatemala 1954: la Radio Secreta con la que la CIA Tumbó un Gobierno** (68 car.). Refs T3: Archivo Desclasificado "Operación Ajax: el golpe de 1953 en Irán" 56.136 (06/11, ✓) · "Proyecto Azorian: la operación secreta de la CIA…" 67.641 (28/10, ✓) · El Archivo Secreto "Guatemala 1954: …" 18.986 (✓). O "por una banana" dos concorrentes fica de fora; o nosso objeto é a rádio. Pago: 0:00–0:29 e 3:37–4:22.
- **Thumb (H1, rosto real + objeto):** **Fidel Castro em tinta**, meio corpo à esquerda (40% do quadro), de farda verde-oliva, olhando de lado, desconfiado, segurando **um charuto aceso**; à frente dele, uma **caixa de puros aberta** com uma etiqueta datilografada. Fundo **papel claro com luz de fim de tarde caribenha** (ocre). Texto: **"CIA"** preto gigante à direita + sello vermelho **"OBJETIVO"** carimbado na diagonal, meio por cima da caixa (2 palavras). Promete: "a CIA queria Castro, e o que há nesse charuto?". Conversa: os títulos falam de AL e da rádio da Guatemala; a thumb abre um 2º caso, sem repetir. Juntos dizem: "a CIA fez várias coisas na AL, e esta é uma delas". Pagamento: 6:19–7:44 (Bahía + Puros; fora do 1º minuto, mas o 1º minuto já paga os dois títulos). Refs H1: Archive CIA (Dulles + cachimbo) 216.211 ✓ · SLICE (Castro entre os rostos) 344.729 ✓ · Atlas CIA vs KGB (rosto real) 100.373 ✓. **Por que não Dulles:** seria a thumb do Archive repetida. **Desvio da bíblia:** Castro não é chefe da CIA; entra como rosto reconhecível em AL.

### 003 FBI · `E1Rgm7jbE0g`
**Atual:** "TODA la historia del FBI en 13 minutos" · 566 impr · 4,1% · 52% · 13:17. Mosaico `mosaicos/dossie-es-003-fbi.jpg`.

| Link | Canal | Inscr. | Views | Data | v/i | > med |
|---|---|---|---|---|---|---|
| [z-Be2YeCSPE](https://youtu.be/z-Be2YeCSPE) (série de casos) | Los Archivos del FBI | 537 mil | 1.451.929 | 21/12/2025 | 2,7 | ✓ |
| [9f7tNIgZsak](https://youtu.be/9f7tNIgZsak) sistema del FBI | Te lo Pinto | 603 mil | 748.692 | 07/12/2025 | 1,24 | ✓ |
| [UnblfYBQU9s](https://youtu.be/UnblfYBQU9s) el FBI te caza | Te lo Pinto | 603 mil | 390.432 | 16/09 | 0,65 | ✓ |
| [470bUPjlKXQ](https://youtu.be/470bUPjlKXQ) (en) Hoover | History Exposé | 266 mil | 292.627 | 19/05 | 1,1 | ✓ |
| [kEfEQYeY2I0](https://youtu.be/kEfEQYeY2I0) FBI vs CIA | Te lo Pinto | 603 mil | 181.669 | 05/11 | 0,30 | ✓ |
| [p0Wg9WsEAZ0](https://youtu.be/p0Wg9WsEAZ0) Cómo el FBI capturó… | El Rastro Criminal | 30 mil | 141.889 | 26/05 | 4,7 | ✓ |
| [gEOavheqCKM](https://youtu.be/gEOavheqCKM) (en) | Archive in Minutes | 21,5 mil | 16.196 | 12/11 | 0,75 | ✗ |

**O que o vídeo entrega**
- **0:00–0:27** "ocho personas fuerzan la cerradura de una pequeña oficina vacía. Llenan maletas con todos los documentos… Nunca los atraparán. La oficina era del FBI… Y de los secretos que guardaba en esos archivos." (paga T2 e a thumb em 27 s)
- 1:44–1:48 Hoover copia as fichas da Biblioteca do Congresso: "más de cien mil nombres."
- 2:49–2:51 "Lo nombran de forma interina. Se quedará cuarenta y ocho años."
- 7:23–8:07 a carta anônima a Martin Luther King ("salió del propio FBI").
- 8:19–9:14 os de Media publicam: "COINTELPRO."
- 9:24–9:33 "Su secretaria… destruye sus archivos personales."
- 12:38–12:54 "Ni un solo arresto… En dos mil catorce, varios de ellos cuentan su historia."

**Proposta**
- **Título 1 (T1):** **TODA la Historia del FBI en 13 Minutos | Los Archivos Secretos de Hoover** (72 car.). Refs T1: Atlas Mossad 85.994 (✓) · Atlas KGB 44.515 (✓). Pago: 1:44, 2:49, 9:24. **Ressalva:** o FBI é tema fraco no molde (Archive FBI 16 mil ✗; Atlas FBI vs KGB 1.725). Daí o subtítulo puxar **Hoover**, que é o rosto conhecido (History Exposé 292 mil ✓).
- **Título 2 (T2, "Cómo"):** **Cómo 8 Desconocidos Robaron los Secretos del FBI y Nunca Fueron Atrapados** (73 car.). Refs T2: El Rastro Criminal "Cómo el FBI Capturó a Larry Gene Bell" 141.889 (26/05, ✓) · Espía Real 393.826 (✓) · Mossad Oculto 109.113 (✓). Inverte o padrão (aqui é o FBI quem perde). Pago: 0:10–0:27, 8:19–9:14, 12:38–12:54.
- **Thumb (H1, rosto real + objeto):** **J. Edgar Hoover em tinta**, meio corpo à esquerda, terno escuro, cara fechada e rígida, segurando **uma gaveta de fichário puxada e vazia**; no chão, uma fechadura arrombada e 2–3 fichas soltas. Fundo **papel claro** com a fachada do edifício em traço leve. Texto: **"FBI"** preto gigante à direita + sello vermelho **"ROBADO"** na diagonal sobre a gaveta (2 palavras). Promete: "roubaram os arquivos do homem que fichava todo mundo". Conversa: o T1 diz "arquivos de Hoover", o T2 diz "8 desconhecidos" e a thumb mostra a gaveta vazia, sem repetir as palavras. Pagamento: 0:10–0:27 e 9:24 (os arquivos pessoais destruídos). Refs H1: History Exposé (rosto de Hoover) 292.627 ✓ · Archive CIA (rosto real + objeto) 216.211 ✓ · Archive KGB 247.064 ✓. **Contra:** a thumb cartoon de Hoover do Archive FBI ficou abaixo da mediana (16 mil ✗); a nossa se diferencia por ser tinta realista, ter a gaveta arrombada como foco e o sello "ROBADO" no lugar de "HOOVER'S FILES".

### 005 KGB · `I_ehrH5Yrak`
**Atual:** "La historia COMPLETA de la KGB en 14 minutos" · 162 impr · 3,1% · 73% · 14:06. Mosaico `mosaicos/dossie-es-005-kgb.jpg`.

| Link | Canal | Inscr. | Views | Data | v/i | > med |
|---|---|---|---|---|---|---|
| [Xt6Q9eiFULU](https://youtu.be/Xt6Q9eiFULU) Putin: del KGB al Kremlin | World View | 40,8 mil | 584.096 | 24/10/2025 | 14,3 | ✓ |
| [VNJhu4rh6OY](https://youtu.be/VNJhu4rh6OY) (en) | Archive in Minutes | 21,5 mil | 247.064 | 18/10 | 11,5 | ✓ |
| [by7uTDjSx7Y](https://youtu.be/by7uTDjSx7Y) | Te lo Pinto | 603 mil | 246.737 | 30/10 | 0,41 | ✓ |
| [lSwpe8i3aK4](https://youtu.be/lSwpe8i3aK4) Mossad humilló a la KGB | Ascenso y Ruina | 1,8 mil | 113.855 | 16/12/2025 | 63,6 | ✓ |
| [TIh8QUZtWxQ](https://youtu.be/TIh8QUZtWxQ) rangos de la KGB | POV Rangos | 1,7 mil | 68.137 | 17/09 | 40,6 | ✓ |
| [t0EBZqMWi1o](https://youtu.be/t0EBZqMWi1o) | Atlas del Tiempo | 1,8 mil | 44.515 | 28/10 | 25,3 | ✓ |
| [n9bKoGWe8lQ](https://youtu.be/n9bKoGWe8lQ) secretos de la Lubyanka | Ecos de la URSS | 1,8 mil | 42.570 | 27/08 | 24,1 | ✓ |
| [Wqf2qlyahDA](https://youtu.be/Wqf2qlyahDA) (pt) o caso Markov | Rastro Químico | 31 mil | 55.241 | 14/05 | 1,76 | ✓ |

**O que o vídeo entrega**
- **0:00–0:25** "Londres… junto al puente de Waterloo. Siente un pinchazo en el muslo… un desconocido recoge un paraguas… En su muslo hay una bolita de metal de menos de dos milímetros… Y de cómo aprendió a alcanzar a sus enemigos en cualquier lugar del mundo." (paga T1, T2 e a thumb em 25 s)
- 1:40–1:53 Lubianka: "desde el sótano ya se ve Siberia."
- 3:07–3:55 Trotski em Coyoacán (Ramón Mercader).
- 5:39–6:24 a moeda oca de Brooklyn; troca de Abel por Powers.
- **9:30–10:19** "El Paraguas… probablemente era ricina… Kalugin afirmó… que el veneno salió de un laboratorio de la KGB… Nadie fue condenado jamás."
- 10:56–11:14 Gordievski: a sacola britânica e a fuga no porta-malas.
- 11:54 a estátua de Dzerzhinski arrancada por uma grua.

**Proposta**
- **Título 1 (T1):** **TODA la Historia de la KGB en 14 Minutos | El Brazo que Llegaba a Cualquier País** (80 car.). Refs T1: Atlas KGB 44.515 (28/10, ✓) · Te lo Pinto KGB 246.737 (30/10, ✓). Pago: 0:25 (frase-tese), 3:07 (México), 9:30 (Londres), 13:00 (Chile).
- **Título 2 (T3, caso datado + aposto):** **El Paraguas de Londres: el Caso que Apunta a un Laboratorio de la KGB** (69 car.). Refs T3: Archivo Desclasificado "Richard Sorge: el espía que…" 129.010 (✓) · "Klaus Fuchs: el espía que…" 59.044 (✓), ambos KGB/soviéticos · "Proyecto Azorian: …" 67.641 (✓). Apoio do caso: Rastro Químico (pt) 55.241 ✓. Pago: 0:00–0:23 e 9:30–10:19. Diz "apunta" porque o vídeo atribui a afirmação a Kalugin, sem afirmar como fato.
- **Thumb (H2, objeto dominante):** **guarda-chuva preto fechado** em diagonal, ocupando metade do quadro, empunhado por uma mão de luva preta; a ponta metálica brilha. Ao lado, em detalhe ampliado dentro de um círculo de lupa, a **bolinha de metal**. Fundo: **ponte de Waterloo e o Big Ben** em traço leve, céu de neblina clara de fim de tarde (cinza-pérola + papel), nada escuro. Texto: **"KGB"** preto gigante à direita + sello vermelho **"LONDRES 1978"** (2 palavras). Promete: "o que um guarda-chuva em Londres tem a ver com a KGB?". Conversa: o T2 nomeia o guarda-chuva e a thumb mostra o detalhe (a bolinha) que o título não diz; o T1 promete o alcance mundial e a thumb põe Londres. Pagamento: 0:00–0:23 e 9:42 ("La bolita… tenía dos agujeros diminutos"). Refs H2: Archivos de la 2ª GM 158.385 ✓ · Dossier Global 94.321 ✓ · Archivo Desclasificado Azorian 67.641 ✓. **Desvio consciente do gap:** sem o rosto famoso (Putin) que as 3 referências de KGB usam, porque o vídeo não fala dele (seria a combinação CTR alto + retenção baixa). Sem seringa, sangue nem vítima.

### 004 Cosa Nostra · `gmA0LkJqf_U`
**Atual:** "TODA la historia de la Cosa Nostra en 15 minutos" · 107 impr · 3,7% · 76% · 14:33. Mosaico `mosaicos/dossie-es-004-cosa-nostra.jpg`.

| Link | Canal | Inscr. | Views | Data | v/i | > med |
|---|---|---|---|---|---|---|
| [3M6xlSqu1cQ](https://youtu.be/3M6xlSqu1cQ) Corleone: el Padrino | World View | 40,8 mil | 645.075 | 02/11/2025 | 15,8 | ✓ |
| [Q3gRYpKRubw](https://youtu.be/Q3gRYpKRubw) Vito Genovese | Relato Mafioso | 80,7 mil | 172.776 | 30/06 | 2,1 | ✓ |
| [eDYqrfmLK-g](https://youtu.be/eDYqrfmLK-g) 2ª guerra de Palermo | Historia de la Mafia | 1,7 mil | 127.323 | 17/10 | 74,9 | ✓ |
| [tTbJwCtM2LI](https://youtu.be/tTbJwCtM2LI) La Cosa Nostra Ep. 2 | Free Documentary Esp | 211 mil | 102.429 | 19/06 | 0,49 | ✓ |
| [mfRFUwHoqX0](https://youtu.be/mfRFUwHoqX0) mafia italiana real | Cruzada Hostil | 95 mil | 75.203 | 19/12/2025 | 0,79 | ✓ |
| [l1vOy0zFAdY](https://youtu.be/l1vOy0zFAdY) | Mafia Secreta | 175 | 50.429 | 03/11 | 288 | ✓ |
| [3-8MwLiV9jo](https://youtu.be/3-8MwLiV9jo) Tommaso Buscetta | Cruzada Hostil | 95 mil | 27.788 | 21/08 | 0,29 | ✗ |

**O que o vídeo entrega**
- **0:00–0:28** "sostiene en las manos la estampa de un santo… Jura: si traiciono, que mi carne arda como arde este santo. Se llama Tommaso Buscetta. Cuarenta años después, se lo contará todo a un juez… Y del juramento que la protegió durante un siglo." (paga T1, T2 e a thumb em 28 s)
- 4:01–4:31 Luciano no restaurante de Coney Island; nasce a Comissão.
- 5:48–6:41 Luciano em Havana, os cassinos e Castro.
- 9:54–10:45 "Buscetta rompe su juramento… Cosa Nostra. Nuestra cosa."
- 11:41–12:21 o maxiprocesso: "475 acusados… jaulas de acero."
- 13:33–14:08 "La Estampa… Lo que no resistió fue que uno de los suyos rompiera el juramento."

**Proposta**
- **Título 1 (T1):** **TODA la Historia de la Cosa Nostra en 15 Minutos | El Juramento que la Protegió un Siglo** (88 car.). Refs T1: Atlas Mossad 85.994 (✓) · Historia Total Israel 852.395 (✓). Pago: 0:14–0:28 e 14:03.
- **Título 2 (T4, pessoa + ação):** **Tommaso Buscetta: el Mafioso que Juró Silencio y se lo Contó Todo a un Juez** (75 car.). Refs T4: World View "Corleone: el Padrino más Poderoso…" 645.075 (✓) · Relato Mafioso "Vito Genovese: El Jefe que…" 172.776 (✓). **Diferenciação:** o Cruzada Hostil usou "Tommaso Buscetta: El Mafioso que HIZO TEMBLAR…" e ficou ✗ (27.788). O nosso troca o "temblar" genérico pelo **paradoxo do juramento × a confissão**, que é a frase literal de 0:14–0:20. Pago: 0:14–0:25 e 10:24–10:45.
- **Thumb (H3, retrato do chefe real):** **Buscetta jovem em tinta**, busto de frente no estilo de ficha policial (placa de números na base), olhar fixo e frio. Na mão erguida, **a estampa do santo queimando**: chama laranja, sem sangue. Fundo **papel claro** com Palermo em traço sépia. Texto: **"COSA NOSTRA"** preto à direita + sello vermelho **"TRAIDOR"** (3 palavras). Promete: "quem traiu a máfia, e por que ele segura um santo pegando fogo?". Conversa: o T2 diz o nome e o "contou tudo", e a thumb diz "TRAIDOR" e mostra o juramento; o T1 promete o juramento e a thumb mostra o objeto dele. Pagamento: 0:00–0:20 e 13:33. Refs H3: World View (fichas P&B de Corleone) 645.075 ✓ · Relato Mafioso (retrato de Genovese) 172.776 ✓ · Mafia Secreta (rosto de Riina) 50.429 ✓. **Desvio da bíblia:** Buscetta é delator, não chefe; ele é o protagonista do hook.

### 006 Masones · `DBLonwmeQ7c`
**Atual:** "TODA la historia de los Masones en 14 minutos" · recém-publicado (8 impr) · 14:11. Mosaico `mosaicos/dossie-es-006-masones.jpg`.

| Link | Canal | Inscr. | Views | Data | v/i | > med |
|---|---|---|---|---|---|---|
| [OyQMNlGbwEI](https://youtu.be/OyQMNlGbwEI) LA MASONERÍA | Academia Play | 3,78 mi | 794.808 | 22/04 | 0,21 | ✓ |
| [b_9OXSLJkS8](https://youtu.be/b_9OXSLJkS8) teoría del poder mundial | Magnus Mefisto | 2,24 mi | 422.557 | 13/08 | 0,19 | ✓ |
| [vWyu2T7P038](https://youtu.be/vWyu2T7P038) masones e illuminati | El Historiador Nocturno | 308 mil | 190.542 | 27/11/2025 | 0,62 | ✓ |
| [-j2TaRzM7N0](https://youtu.be/-j2TaRzM7N0) nadie ha explicado bien | Tus Noches de Historia | 4,1 mil | 174.896 | 20/09 | 42,8 | ✓ |
| [mukgvolxlrE](https://youtu.be/mukgvolxlrE) no te contaron | Historia Incomprendida | 4,47 mi | 134.920 | 26/11/2025 | 0,03 | ✓ |
| [mYBAcvwEUnA](https://youtu.be/mYBAcvwEUnA) por dentro | Órdenes Secretas | 5,6 mil | 51.432 | 30/04 | 9,3 | ✓ |

**O que o vídeo entrega**
- **0:00–0:27** "El albañil William Morgan anuncia un libro con los rituales secretos… unos hombres lo suben a la fuerza a un carruaje. Nadie volvió a ver a William Morgan… Y de por qué su secreto despierta sospechas desde hace tres siglos." (paga o T2 em 21 s)
- 3:54–4:15 Washington jura sobre uma Bíblia de loja.
- 4:43–5:38 Barruel e os Iluminados: "Los historiadores no han hallado pruebas de ese complot."
- **5:43–6:35** Logia Lautaro: San Martín, Alvear, O'Higgins; "Simón Bolívar, según la tradición masónica, se había iniciado en una logia de París."
- **6:45–7:45** "El libro sale igual… Y se vende como nunca… Nace el Partido Antimasónico."
- 7:51–8:20 Bolívar proíbe as sociedades secretas.
- 10:45–11:34 a lista da P2 (Massera, López Rega).
- **13:30–13:50** "El secreto de los masones lleva casi trescientos años a la venta."

**Proposta**
- **Título 1 (T1):** **TODA la Historia de los Masones en 14 Minutos | Un Secreto que Lleva 3 Siglos a la Venta** (88 car.). Refs T1: Atlas Mossad 85.994 (✓) · Te lo Pinto KGB 246.737 (✓). Pago: 0:27 e 13:30–13:50 (o vídeo diz "casi trescientos años"; "3 siglos" arredonda e o próprio hook diz "tres siglos").
- **Título 2 (T2, "Cómo"):** **Cómo un Libro de 1826 Puso a Estados Unidos Contra los Masones** (62 car.). Refs T2: Archivos de la 2ª GM 158.385 (✓) · Mossad Oculto 109.113 (✓) · El Rastro Criminal 141.889 (✓). Pago: 0:00–0:21 e 6:45–7:45.
- **Thumb (H4, rostos de próceres):** **Bolívar e San Martín em tinta**, bustos lado a lado à esquerda e ao centro, sérios e olhando para o espectador; entre eles, o **esquadro e compasso dourados** como selo de lacre. Fundo **papel claro** com colunas de templo em traço leve. Texto: **"MASONES"** preto gigante à direita + sello vermelho **"¿LOS PRÓCERES?"** (3 palavras). Promete: "os heróis da independência eram maçons?". O vídeo responde com nuance: a Lautaro copiava ritos, os historiadores divergem, e Bolívar se iniciou e depois fechou as lojas (5:43–6:35 e 7:51–8:20). A pergunta é honesta porque a resposta é "depende", e o vídeo diz isso. Conversa: o T1 (segredo à venda) e o T2 (o livro de 1826) não citam a AL; a thumb traz o ângulo AL da bíblia, e os três juntos dão três portas para o mesmo segredo. Refs H4: El Historiador Nocturno (San Martín, Bolívar, Churchill, Juárez) 190.542 ✓ · Historia Incomprendida (Washington) 134.920 ✓ · SLICE (rostos políticos) 344.729 ✓. **Diferenciação:** o Historiador usa 4 rostos e "¿ELLOS CONTROLAN EL MUNDO?" (teoria da conspiração). A nossa tem 2 rostos, o símbolo e uma pergunta histórica, não conspiratória. **Desvio da bíblia:** próceres não são chefes da ordem; entram pelo ângulo AL e pelo reconhecimento.

---

## 3. Notas para o crivo
- **Duração:** N = duração real arredondada (13:43→14, 11:47→12, 13:17→13, 14:06→14, 14:33→15, 14:11→14). A bíblia mantém o "en N minutos" só no T1; o T2 não leva.
- **Palavras proibidas:** nenhum título nem texto de thumb usa muerte/murió/muerto/asesinado/asesinato/masacre/matanza/sangre (checado por regex). Os títulos de referência com "matar/asesinato" (Espía Real, Genovese) são só dado de mercado; não copiei a palavra.
- **Não é cópia do clone:** o T1 deixa a forma do Archivo en Minutos ("La historia COMPLETA del X en N minutos", caixa baixa, sem subtítulo) e ganha Title Case + subtítulo próprio. Nenhum subtítulo repete o do Atlas ("Más Temido", "Duelo de Espías", "Cambiaron el Siglo XX").
- **Riscos honestos:** (1) o T1 com subtítulo tem evidência forte no Atlas, mas num canal que surfou o Archive 5 dias depois; o efeito pode ser de timing. (2) FBI e Masones são temas mais fracos no molde (FBI: Archive 16 mil ✗); a embalagem melhora o CTR, mas não cria demanda. (3) Thumbs H2 sem rosto (Mossad, KGB) contrariam a recomendação do gap (rosto famoso); justifiquei pela promessa paga. Se o "Testar e comparar" mostrar que perdem, a alternativa é a estátua de Dzerzhinski (KGB, 11:54) e Eichmann de costas no ônibus 203 (Mossad, 2:44).
