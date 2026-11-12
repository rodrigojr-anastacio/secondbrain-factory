# IDIOMA: em que língua abrir o canal de "lugares / arquivos de guerra" (Where They Stood, Civil War Fine Print)

Data: 2026-11-12 · Agente: Tendências (etapa 3 do `playbooks/novo-canal.md`) · Dados: `idioma/dados/` (busca_idi.jsonl, demanda_idioma.json, matriz.json), `idioma/scripts/`, `idioma/voz/` · Concorrência detalhada: `CONCORRENCIA.md`.
Legenda: **[O]** observado (busca do YouTube via yt-dlp + WARP, YouTube Data API) · **[I]** inferido/estimativa (faixas). Modelo de referência: `pesquisa/archive-in-minutes/IDIOMA.md`.

---

## Resumo executivo

**Recomendação: inglês (en), com espanhol (es) em 2º como versão do mesmo conteúdo.** O en vence a matriz (**7.70** contra 6.15 do es) e vence também com pesos iguais (7.6) e com RPM 30%/demanda 20% (7.70). Mas **o en passa raspando pela trava de concorrência** (nota 3; a trava é ≤ 2), então a recomendação tem uma condição, explicada abaixo.

| Idioma | Nota | Situação |
|---|---|---|
| **en** | **7.70** | **1º**, com condição: não repetir o tema dos clones (Iwo Jima) e revisar a trava se os clones passarem a diversificar |
| **es** | **6.15** | **2º** (versão do conteúdo en + pauta local); sem prova do formato em es |
| ja | 6.05 | empate técnico com es/pt, mas **inoperável** (ninguém lê/revisa japonês; demanda é pelo ponto de vista japonês) |
| pt | 5.95 | 3º; RPM mais baixo, vaga real |
| fr | 5.65 | demanda ≈ 1/10 do en; sem clones |
| it, de, pl, tr | 5.10 / 5.05 / 4.35 / 3.60 | demanda fraca; de com risco §86a |
| ru | 3.85 | **eliminado pela trava de RPM** (sem anúncios) |

**Por que o en ganha, em 5 linhas:**
1. **Demanda [O]:** mediana do top-10 dos 4 temas de guerra de **1,84 mi** (es 787 mil, pt 497 mil, fr 66 mil, de 52 mil) e **64** vídeos de 2026 acima de 100 mil só nesses 4 temas (es 16, pt 9, fr 4, de 3). O formato só tem **prova** em en (WTS 4,54 mi; Forgotten Fleet 1,16 mi; Ship Tales 943 mil).
2. **RPM [I]:** US$ 4–8 (história/documentário) contra US$ 1–3,2 do es e US$ 1–2,8 do pt: **3–4× por view**.
3. **Concorrência [O]:** 21 clones do WTS em 5 semanas (17 puros), mediana de 28 views; os dois canais de navios com tração (Forgotten Fleet, Ship Tales) fazem outro assunto. Em es/pt/fr/de há **1–4 clones por idioma**, todos com ≤ 3,6 mil views no melhor título.
4. **Viabilidade [I]:** o en é o idioma em que o Rodrigo revisa e há 46 vozes Fish listadas; a pesquisa e o material (fotos de arquivo dos EUA) são em en.
5. **O tema natural é dos EUA** (Iwo Jima, Pearl Harbor, Omaha, Midway): a audiência dessas buscas é en (e ja, no caso de Iwo Jima). Em es/pt o **mesmo tema rende 1/3 a 1/10** (Iwo Jima: en 1,43 mi, es 155 mil, pt 87 mil de mediana), e não existe título-fórmula com tração em es/pt/de/fr.

**A condição (trava de concorrência):** a nota 3 em concorrência é um **julgamento** e é a nota que decide. Contra a trava (≤ 2): há **21 canais** copiando o WTS em 5 semanas e 3 canais de navios com tração. A favor de 3: (i) os 17 clones puros têm mediana de 28 views e nenhum passa de 5 mil de mediana; (ii) **todos copiam o mesmo título do Iwo Jima** (14 títulos da mesma pergunta sobre Iwo Jima) e a demanda "só lugar" tem dezenas de temas sem nenhum título "why can't you visit" (Corregidor, Tinian, Peleliu, Guadalcanal, Okinawa, Diego Garcia com 1 clone de 0 views); (iii) são **4–5× menos** que os 91 clones do Archive in Minutes que derrubaram o en lá. **Se a trava valesse** (nota ≤ 2), o en sai e o es vence (6.15), com pt e fr atrás. **Gatilho para revisar [I]:** ≥ 10 clones novos **com temas diferentes do Iwo Jima** em 2 semanas, ou algum clone com mediana ≥ 5 mil.

**Decisões do Rodrigo:** aprovar en (com a condição acima) e o es como 2º idioma; escolher a voz en (candidatas em §6); aprovar o piloto (temas sugeridos em `CONCORRENCIA.md` §4 e na resposta ao orquestrador).

---

## 1. Método
- **Buscas [O]:** 162 consultas sem cota (yt-dlp via WARP), 30 resultados cada, em 10 idiomas (en, es, pt, fr, de + exploratórios it, pl, ja, ru, tr). Por idioma: **5 temas escritos nativamente** (Iwo Jima, Pearl Harbor, Omaha/Normandia, Hiroshima, Área 51) em 2 ordens (relevância e "este ano por views"), **2–3 fórmulas traduzidas** em 2 ordens (relevância e data de envio) e **0–3 temas locais** (es: Malvinas, Guerra Civil Espanhola, Chaco; pt: Monte Castelo/FEB, Paraguai, Canudos; fr: Verdun, Maginot, Zona Vermelha; de: Atlântico-Wall, Peenemünde, Lost Places; it: Linha Gótica).
- **Filtros:** ≥ 4 min, não ao vivo, idioma do vídeo = idioma da busca (áudio/língua declarada, senão script/palavras-chave) e título cita o tema (regex nativa). `videos.list` em 6.381 ids (132 un.). **Área 51 foi tirada das medianas de "guerra"** (é demanda de MrBeast/ET, não do formato).
- **Fórmulas traduzidas:** en "why can't you visit Iwo Jima" · es "¿por qué no puedes visitar Iwo Jima?" · pt "por que você não pode visitar Iwo Jima" · fr "pourquoi on ne peut pas visiter Iwo Jima" · de "Warum darf man Iwo Jima nicht besuchen" (+ "what's still under Pearl Harbor" e "Midway" traduzidas).
- **Limites:** top-30 por consulta, não o universo; as medianas de de/it/pl/tr têm poucos vídeos (n pequeno); a nota é minha, as faixas de RPM são **[I]**.

## 2. Demanda por idioma [O]

| Idioma | Mediana do top-10 (4 temas de guerra, n ≥ 5) | Vídeos ≥ 100 mil em 2026 (4 temas) | Títulos-fórmula desde 27/09 | Mediana / máx. das views deles | RPM do nicho (faixa) |
|---|---|---|---|---|---|
| en inglês | 1.838.577 | 64 | 20 (18 canais) | 54 / 4.535.929 | US$ 4–8 |
| es espanhol | 787.336 | 16 | 3 (3 canais) | 74 / 115 | US$ 1–3,2 |
| pt português | 497.323 | 9 | 4 (4 canais) | 451 / 3.601 | US$ 1–2,8 |
| fr francês | 65.821 | 4 | 0 (0 canais) | 0 / 0 | US$ 2–5,6 |
| de alemão | 52.219 | 3 | 1 (1 canais) | 111 / 111 | US$ 2,4–8 (hip.) |
| it italiano | 42.557 | 3 | 0 (0 canais) | 0 / 0 | US$ 1,6–4,8 (hip.) |
| pl polonês | 56.808 | 2 | 0 (0 canais) | 0 / 0 | US$ 0,8–3,2 (hip.) |
| ja japonês | 1.100.346 | 42 | 0 (0 canais) | 0 / 0 | US$ 2,4–7,2 (hip.) |
| ru russo | 538.091 | 4 | 0 (0 canais) | 0 / 0 | ~0 (sem anúncios) |
| tr turco | 5.477 | 0 | 0 (0 canais) | 0 / 0 | US$ 0,4–2 (hip.) |

Mediana do top-10 e vídeos ≥ 100 mil de 2026, por tema nativo (Área 51 só para referência; **atenção ao n**: de Pearl Harbor tem 1 vídeo e pl/tr Pearl Harbor 0, então 19,8 mi e 0 não valem; a coluna anterior só usa temas com n ≥ 5). Na tabela anterior, a linha "en" conta só títulos nos 5 temas buscados (18 canais); o mapa completo tem 21 clones em `CONCORRENCIA.md`:

| Idioma | Mediana top-10 por tema nativo (vídeos ≥ 100 mil em 2026) |
|---|---|
| en | Iwo Jima: 1.430.244 (18) · Pearl Harbor: 5.480.647 (17) · Omaha Beach Normandy: 2.246.911 (18) · Hiroshima: 1.064.295 (11) · Area 51: 4.545.927 (11) |
| es | Iwo Jima: 155.214 (5) · Pearl Harbor: 447.733 (3) · Playa Omaha Normandía: 1.126.939 (5) · Hiroshima: 1.533.384 (3) · Área 51: 2.595.038 (6) |
| pt | Iwo Jima: 87.191 (1) · Pearl Harbor: 415.522 (0) · Praia de Omaha Normand: 579.125 (3) · Hiroshima: 1.162.401 (5) · Área 51: 1.878.676 (7) |
| fr | Iwo Jima: 14.281 (0) · Pearl Harbor: 75.031 (2) · plage d'Omaha Normandi: 56.611 (0) · Hiroshima: 1.364.986 (2) · Zone 51: 4.123 (0) |
| de | Iwo Jima: 989 (0) · Pearl Harbor: 19.832.700 (0) · Omaha Beach Normandie: 52.219 (1) · Hiroshima: 188.450 (2) · Area 51: 920.158 (0) |
| it | Iwo Jima: 11.501 (0) · Pearl Harbor: 47.963 (1) · spiaggia di Omaha Norm: 37.151 (1) · Hiroshima: 124.031 (1) · Area 51: 128.105 (2) |
| pl | Iwo Jima: 28.747 (0) · Pearl Harbor: 0 (0) · Normandia Omaha: 1.058 (1) · Hiroszima: 112.558 (1) · Strefa 51: 69.110 (1) |
| ja | 硫黄島: 1.271.546 (13) · 真珠湾: 929.146 (9) · ノルマンディー オマハビーチ: 643.278 (1) · 広島 原爆: 1.611.683 (19) · エリア51: 475.499 (3) |
| ru | Иводзима: 11.530 (0) · Перл-Харбор: 1.064.652 (3) · Нормандия Омаха: 846 (0) · Хиросима: 2.231.013 (1) · Зона 51: 300.694 (2) |
| tr | Iwo Jima: 160.064 (0) · Pearl Harbor: 0 (0) · Normandiya Omaha: 5.477 (0) · Hiroşima: 0 (0) |

- **O tema perde força fora do en [O]:** Iwo Jima (en 1,43 mi → es 155 mil → pt 87 mil → fr 14 mil → de 1 mil). O lugar que gerou o hit do WTS **não é demanda es/pt**; Omaha (es 1,13 mi, pt 579 mil) e Hiroshima (es 1,53 mi, pt 1,16 mi) sim, mas como documentário de evento, sem a pergunta "por que não pode visitar".
- **Prova do formato [O]:** só em en (WTS 4,54 mi; Omaha 341 mil; Forgotten Fleet; Ship Tales). Em es o maior título-fórmula de 2026 tem **115 views**, em pt **3,6 mil**, em de **111**, em fr/it **nenhum**. Os "por que NUNCA sacarán o USS Arizona" (es: Titanes Olvidados 380 views, Bajo Cubierta 26), "Onde estão hoje os 8 encouraçados" (pt: Fantasmas do Oceano 1,5 mil, Colossos do Mar 3,6 mil), fr (L'Empire des Machines 39) e de (truter 101) parecem **traduções/adaptações do Forgotten Fleet e do Ship Tales** [I], todas de outubro/novembro de 2026.
- **ja [O]:** demanda grande (mediana 1,10 mi; 42 vídeos ≥ 100 mil em 2026, Iwo Jima 1,27 mi), mas é ponto de vista japonês (Hiroshima 1,61 mi, Pearl Harbor 929 mil, yukkuri e TV), e **0** títulos-fórmula de lugar. [I] RPM ~US$ 2,4–7,2.
- **ru [O]:** Pearl Harbor 1,06 mi e Hiroshima 2,23 mi, mas Iwo Jima 11,5 mil e a trava de RPM elimina (anúncios suspensos para a Rússia em 2022; [I], conhecimento da política, não reconsultado hoje).

## 3. Concorrência por idioma (clones da fórmula)
- **en [O]:** 21 canais do molde WTS (17 puros de 27/09 em diante; mediana das medianas 28 views; melhor clone literal do Iwo Jima 910 views; melhor clone com outro lugar 6,2 mil) + 3 canais de navios com tração (Forgotten Fleet, Ship Tales, Insight Ship) + IT'S HISTORY. **Dono forte**: WTS (3,7 mil inscritos, 4,54 mi no hit). Nota **3** (limítrofe).
- **es [O]:** 3 canais copiando o título do Iwo Jima (El Origen del Presente 115 views, Lo Que Aún Queda X 74, Actualidadmilitar 58) + 2 traduzindo os navios; todos de out/nov 2026. Nota **7**.
- **pt [O]:** 4 títulos-fórmula (GuerraDocumentada 24 views; Fantasmas do Oceano 878–1,5 mil; Colossos do Mar 3,6 mil; Ainda Está Lá 9,5 mil nos naufrágios de Midway). Nota **8**.
- **fr [O]:** 0 clones diretos (1 tradução de navio). Nota **10**; **[I]** vazio também pode ser falta de demanda (a demanda fr é 1/30 da en).
- **de [O]:** 1 clone (Cain Brown, 111 views) + Akte Ernstfall e Zwei Seiten des Krieges em formato diferente. Nota 9.
- **it/pl/tr/ja/ru:** 0 clones; nota 7–9, sem demanda pelo formato (ja: demanda grande em outro formato).

## 4. RPM [I]
Faixa do nicho história/documentário (`playbooks/garimpo-tendencias.md`: en US$ 4–8) × fator do idioma: **es 0,25–0,4×, pt 0,25–0,35×, fr 0,5–0,7×** (tabela da fábrica). Para **de, it, pl, ja, tr** não há fator na fábrica; usei os do `archive-in-minutes/IDIOMA.md` (de ≈ 0,6–1×; it ≈ 0,4–0,6×) e **hipóteses** para ja (0,6–0,9×), pl (0,2–0,4×) e tr (0,1–0,25×). Guerra com imagens violentas pode ter anúncio limitado em qualquer idioma (reduz a faixa; sem dado próprio). A receita por view em es/pt é **~1/3 da en**; para igualar a receita do en, o es precisaria de **3–4× as views**, o que a demanda (1/2 a 1/3 da en) não entrega.

## 5. Matriz (pesos 30/25/20/15/10)

| Idioma | Demanda 30% | Concorrência 25% | RPM 20% | Viabilidade 15% | Risco 10% | **Nota** | Pesos iguais | RPM 30/dem 20 | Trava |
|---|---|---|---|---|---|---|---|---|---|
| **en** | 10 | 3 | 10 | 9 | 6 | **7.70** | 7.6 | 7.70 | - |
| **es** | 6 | 7 | 4 | 8 | 6 | **6.15** | 6.2 | 5.95 | - |
| **ja** | 7 | 7 | 7 | 2 | 5 | **6.05** | 5.6 | 6.05 | - |
| **pt** | 4.5 | 8 | 2.5 | 10 | 6 | **5.95** | 6.2 | 5.75 | - |
| **fr** | 2 | 10 | 6 | 5 | 6 | **5.65** | 5.8 | 6.05 | - |
| **it** | 1.5 | 9 | 6 | 4 | 6 | **5.10** | 5.3 | 5.55 | - |
| **de** | 1.5 | 9 | 8 | 3 | 3 | **5.05** | 4.9 | 5.70 | - |
| **pl** | 1.5 | 9 | 3 | 3 | 6 | **4.35** | 4.5 | 4.50 | - |
| **ru** | 4 | 8 | 0 | 3 | 2 | **3.85** | 3.4 | 3.45 | RPM |
| **tr** | 0.5 | 9 | 2 | 2 | 5 | **3.60** | 3.7 | 3.75 | - |

**Critério de cada nota [I]:**
- **Demanda:** mediana do top-10 dos 4 temas de guerra e vídeos ≥ 100 mil em 2026 (tabela §2), com 10 = en. es 6 (787 mil; 16) e pt 4,5 (497 mil; 9), com desconto de 0,5 por **não haver prova do formato**; ja 7 (1,10 mi; 42, mas de ponto de vista japonês); ru 4; fr 2; de/it/pl 1,5; tr 0,5.
- **Concorrência (10 = vazio; 0 = dono + dezenas de clones):** en 3 (21 clones + 3 canais fortes em outro tema), es 7, pt 8, ja 7 (TV e yukkuri fortes, sem prova do formato), ru 8, fr 10, de/it/pl/tr 9.
- **RPM:** en 10; de 8; ja 7; fr e it 6; es 4; pl 3; pt 2,5; tr 2; ru 0.
- **Viabilidade:** pt 10 (o Rodrigo lê, voz clone dele no `historia-ptbr`); en 9 e es 8 (ele lê; vozes Fish nativas); fr 5 (não revisa); it 4; de/pl/ru 3; ja/tr 2.
- **Risco:** 6 padrão (arquivo de guerra, anúncio limitado possível, direitos de imagens de arquivo); de 3 (§86a StGB com material da 2ª Guerra); ja 5; tr 5; ru 2.
- **Travas:** concorrência ≤ 2 ou RPM ≤ 1. **ru cai (RPM 0)**. **en fica a 1 ponto da trava** (nota 3).
- **Desempate (< 0,3):** en → es → pt → fr → de. es (6.15), ja (6.05) e pt (5.95) ficam a menos de 0,3 entre si: a ordem da preferência deixa **es em 2º e pt em 3º**; ja fica fora por inviabilidade operacional.

**Sensibilidade [O]:** com **pesos iguais** e com **RPM 30%/demanda 20%** o **vencedor não muda (en)**. O **2º** muda: com pesos iguais es e pt empatam (6,2) e vence o es pela ordem; com RPM 30% fr e ja (6,05) passam o es (5.95) por ≤ 0,1 (empate técnico, a ordem mantém o es). Ou seja, o 2º é **instável** (empate entre es, fr e pt); o 1º não.

## 6. Viabilidade: vozes e revisão
- **Fish [O]:** vozes públicas listadas por idioma com `idioma/scripts/fish_vozes.py` (0 custo): en 46, es 53, pt 50, fr 53, de 57 (`idioma/voz/fish_<idioma>.json`).
- **Amostra de voz não gerada (custo US$ 0,00).** O `tools/tts_fish.py` exige canal e registra custo por `--video`, e o canal/piloto ainda não existem; as vozes en listadas têm muitos modelos de personagem. Sem decisão do Rodrigo, não vale gastar.
- **Candidatas en para narração documental [I] (testar no piloto, 3 vozes, ≤ US$ 0,50; nenhuma testada):** **Adrian** (`bf322df2096a46f18c579d0baa36f41d`, "steady and reliable narrator", tags narration/deep/slow, 1,17 mi de usos), **Ethan** (`536d3a5e000945adb7038665781a4aca`, "curious explainer", educational/professional, 722 mil), **Slax** (`c5f56a6cc2ec4fa8920cb4c5889a3fb7`, "clear, precise, measured narration", 1,6 mi) e, como reserva, **Voice DL** (`1936333080804be19655c6749b2ae7b2`, calm/deep). **Evitar** modelos de pessoas reais ou personagens (ex.: "Elon Musk (Noise reduction)", Markiplier, locutor Smash Bros): risco de impersonação e de marca. Não repetir a voz do Dossier en Minutos (es: `ac594943…`) nem o clone do `historia-ptbr`.
- **es (2º idioma):** reaproveitar a lista es do Dossier (`pesquisa/archive-in-minutes/idioma/voz/`) e escolher voz diferente da do `dossie-es`; o Rodrigo lê espanhol.
- **Revisão:** Rodrigo lê en/es/pt; fr, de, ja, ru, it, pl, tr ficariam só com Whisper + LLM.
- **Imagens/mapas:** sem idioma (o texto vai no código), como nos outros canais. Material: fotos de arquivo do governo dos EUA (NARA, Library of Congress, DVIDS), que é domínio público em geral; conferir licença caso a caso (DVIDS e fotos japonesas/britânicas não são automaticamente PD).

## 7. Es/pt: o tema "guerras dos EUA" tem demanda nativa?
- **Parcialmente [O].** Para documentário de evento sim (Omaha es 1,13 mi/pt 579 mil, Hiroshima es 1,53 mi/pt 1,16 mi, Pearl Harbor es 448 mil/pt 416 mil de mediana), mas **para a pergunta de acesso/proibição não** (maior título-fórmula 115 views em es, 3,6 mil em pt), e **Iwo Jima**, o lugar do hit, rende 155 mil (es) e 87 mil (pt).
- **Pauta local [O/I]:** mediana do top-10 dos temas locais: es **1,26 mi** (Chaco 871 mil–2,26 mi; Malvinas "campos minados": **10 views**, ninguém fez), pt **1,38 mi** (Guerra do Paraguai 2,6–9,0 mi; Canudos 648 mil em out/2026; Monte Castelo 408 mil), de 1,32 mi (Westwall, Lost Places), fr 380 mil (Verdun; "zona vermelha" 1,6–18 mil). Ou seja, **es/pt têm demanda por guerra local em documentário clássico**, mas a pergunta "lugar proibido hoje" (Malvinas minadas, Zona Vermelha, Westwall) não tem prova em nenhum idioma.
- **Consequência [I]:** a versão es seria **reescrita nativa do conteúdo en** (Pearl Harbor, Omaha, Hiroshima, Diego Garcia) **mais 1 em cada 3–4 vídeos com pauta local** (Malvinas, Chaco, Guerra Civil), a testar. Em pt, o mesmo com Paraguai/Canudos/FEB. **Hipótese:** o formato "lugar proibido" em es/pt só funciona com lugar local, não com Iwo Jima.

## 8. Recomendação final
1. **Canal en**, slug sugerido `lugares-guerra-en` ou nome do nicho + idioma (a decidir pelo orquestrador), **com temas diferentes do Iwo Jima**; o piloto e o backlog saem de `CONCORRENCIA.md` §4 (candidatos: Diego Garcia, Pearl Harbor/navios, Midway).
2. **2º idioma: es**, só **depois** de 3 vídeos en e com critério numérico (ex.: média ≥ 3 mil em 14 dias ou 1 vídeo ≥ 15 mil), como **versão** do mesmo conteúdo + 1 pauta local a cada 3–4 vídeos.
3. **Não** abrir pt/fr/de por ora.
4. **Reavaliar a trava do en** em 2 semanas com o gatilho de §resumo.

## 9. Limitações
- Medianas de de/it/pl/tr/ru com n pequeno (de Pearl Harbor n=1; tr, n=2). A matriz usa o 4-temas de guerra com n ≥ 5.
- A língua do vídeo foi inferida pelo áudio/língua declarada ou por palavras: pode errar em títulos curtos.
- Nenhum idioma teve **dado próprio** de RPM (o `historia-ptbr` e o `lotr-fr` não monetizam); faixas são de referência.
- O WTS (40 dias) e o CWFP (5 dias) são muito novos: a recomendação é sobre **o mercado de hoje**, sujeita à janela que os clones fecharem.
