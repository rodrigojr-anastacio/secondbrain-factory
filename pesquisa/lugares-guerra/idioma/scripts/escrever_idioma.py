import json, os, statistics as st
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); R = os.path.dirname(BASE)
DI = json.load(open(BASE + "/dados/demanda_idioma.json")); MX = json.load(open(BASE + "/dados/matriz.json"))
def k(n): return f"{int(n):,}".replace(",", ".")
W = {"en": "inglês", "es": "espanhol", "pt": "português", "fr": "francês", "de": "alemão", "it": "italiano", "pl": "polonês", "ja": "japonês", "ru": "russo", "tr": "turco"}
RPM = {"en": "US$ 4–8", "es": "US$ 1–3,2", "pt": "US$ 1–2,8", "fr": "US$ 2–5,6", "de": "US$ 2,4–8 (hip.)", "it": "US$ 1,6–4,8 (hip.)", "pl": "US$ 0,8–3,2 (hip.)", "ja": "US$ 2,4–7,2 (hip.)", "ru": "~0 (sem anúncios)", "tr": "US$ 0,4–2 (hip.)"}
def war4(l):
    t = [v for kk, v in DI[l]["temas"].items() if "51" not in kk]
    meds = [v["top10_med"] for v in t if v["n"] >= 5]
    return (int(st.median(meds)) if meds else 0, sum(v["gt100k_2026"] for v in t), sum(v["n"] for v in t))
rows = []
for l in W:
    m, g, n = war4(l); f = DI[l]["formula"]
    rows.append(f'| {l} {W[l]} | {k(m)} | {g} | {f["n_clones_desde_0927"]} ({f["canais_clones"]} canais) | {k(f["mediana_clones"])} / {k(f["max_clone"])} | {RPM[l]} |')
T1 = "| Idioma | Mediana do top-10 (4 temas de guerra, n ≥ 5) | Vídeos ≥ 100 mil em 2026 (4 temas) | Títulos-fórmula desde 27/09 | Mediana / máx. das views deles | RPM do nicho (faixa) |\n|---|---|---|---|---|---|\n" + "\n".join(rows)
rows = []
for l in W:
    d = DI[l]; c = [f'{t[:22]}: {k(v["top10_med"])} ({v["gt100k_2026"]})' for t, v in d["temas"].items()]
    rows.append(f"| {l} | " + " · ".join(c) + " |")
T2 = "| Idioma | Mediana top-10 por tema nativo (vídeos ≥ 100 mil em 2026) |\n|---|---|\n" + "\n".join(rows)
T3 = "| Idioma | Demanda 30% | Concorrência 25% | RPM 20% | Viabilidade 15% | Risco 10% | **Nota** | Pesos iguais | RPM 30/dem 20 | Trava |\n|---|---|---|---|---|---|---|---|---|---|\n"
for l, v in sorted(MX.items(), key=lambda x: -x[1]["base"]):
    T3 += f'| **{l}** | {v["D"]} | {v["C"]} | {v["R"]} | {v["V"]} | {v["K"]} | **{v["base"]:.2f}** | {v["iguais"]:.1f} | {v["rpm30"]:.2f} | {v["trava"] or "-"} |\n'
txt = f"""# IDIOMA: em que língua abrir o canal de "lugares / arquivos de guerra" (Where They Stood, Civil War Fine Print)

Data: 2026-11-12 · Agente: Tendências (etapa 3 do `playbooks/novo-canal.md`) · Dados: `idioma/dados/` (busca_idi.jsonl, demanda_idioma.json, matriz.json), `idioma/scripts/`, `idioma/voz/` · Concorrência detalhada: `CONCORRENCIA.md`.
Legenda: **[O]** observado (busca do YouTube via yt-dlp + WARP, YouTube Data API) · **[I]** inferido/estimativa (faixas). Modelo de referência: `pesquisa/archive-in-minutes/IDIOMA.md`.

---

## Resumo executivo

**Recomendação: inglês (en), com espanhol (es) em 2º como versão do mesmo conteúdo.** O en vence a matriz (**{MX['en']['base']:.2f}** contra {MX['es']['base']:.2f} do es) e vence também com pesos iguais ({MX['en']['iguais']:.1f}) e com RPM 30%/demanda 20% ({MX['en']['rpm30']:.2f}). Mas **o en passa raspando pela trava de concorrência** (nota 3; a trava é ≤ 2), então a recomendação tem uma condição, explicada abaixo.

| Idioma | Nota | Situação |
|---|---|---|
| **en** | **{MX['en']['base']:.2f}** | **1º**, com condição: não repetir o tema dos clones (Iwo Jima) e revisar a trava se os clones passarem a diversificar |
| **es** | **{MX['es']['base']:.2f}** | **2º** (versão do conteúdo en + pauta local); sem prova do formato em es |
| ja | {MX['ja']['base']:.2f} | empate técnico com es/pt, mas **inoperável** (ninguém lê/revisa japonês; demanda é pelo ponto de vista japonês) |
| pt | {MX['pt']['base']:.2f} | 3º; RPM mais baixo, vaga real |
| fr | {MX['fr']['base']:.2f} | demanda ≈ 1/10 do en; sem clones |
| it, de, pl, tr | {MX['it']['base']:.2f} / {MX['de']['base']:.2f} / {MX['pl']['base']:.2f} / {MX['tr']['base']:.2f} | demanda fraca; de com risco §86a |
| ru | {MX['ru']['base']:.2f} | **eliminado pela trava de RPM** (sem anúncios) |

**Por que o en ganha, em 5 linhas:**
1. **Demanda [O]:** mediana do top-10 dos 4 temas de guerra de **1,84 mi** (es 787 mil, pt 497 mil, fr 66 mil, de 52 mil) e **64** vídeos de 2026 acima de 100 mil só nesses 4 temas (es 16, pt 9, fr 4, de 3). O formato só tem **prova** em en (WTS 4,54 mi; Forgotten Fleet 1,16 mi; Ship Tales 943 mil).
2. **RPM [I]:** US$ 4–8 (história/documentário) contra US$ 1–3,2 do es e US$ 1–2,8 do pt: **3–4× por view**.
3. **Concorrência [O]:** 21 clones do WTS em 5 semanas ({17} puros), mediana de 28 views; os dois canais de navios com tração (Forgotten Fleet, Ship Tales) fazem outro assunto. Em es/pt/fr/de há **1–4 clones por idioma**, todos com ≤ 3,6 mil views no melhor título.
4. **Viabilidade [I]:** o en é o idioma em que o Rodrigo revisa e há 46 vozes Fish listadas; a pesquisa e o material (fotos de arquivo dos EUA) são em en.
5. **O tema natural é dos EUA** (Iwo Jima, Pearl Harbor, Omaha, Midway): a audiência dessas buscas é en (e ja, no caso de Iwo Jima). Em es/pt o **mesmo tema rende 1/3 a 1/10** (Iwo Jima: en 1,43 mi, es 155 mil, pt 87 mil de mediana), e não existe título-fórmula com tração em es/pt/de/fr.

**A condição (trava de concorrência):** a nota 3 em concorrência é um **julgamento** e é a nota que decide. Contra a trava (≤ 2): há **21 canais** copiando o WTS em 5 semanas e 3 canais de navios com tração. A favor de 3: (i) os 17 clones puros têm mediana de 28 views e nenhum passa de 5 mil de mediana; (ii) **todos copiam o mesmo título do Iwo Jima** (14 títulos da mesma pergunta sobre Iwo Jima) e a demanda "só lugar" tem dezenas de temas sem nenhum título "why can't you visit" (Corregidor, Tinian, Peleliu, Guadalcanal, Okinawa, Diego Garcia com 1 clone de 0 views); (iii) são **4–5× menos** que os 91 clones do Archive in Minutes que derrubaram o en lá. **Se a trava valesse** (nota ≤ 2), o en sai e o es vence ({MX['es']['base']:.2f}), com pt e fr atrás. **Gatilho para revisar [I]:** ≥ 10 clones novos **com temas diferentes do Iwo Jima** em 2 semanas, ou algum clone com mediana ≥ 5 mil.

**Decisões do Rodrigo:** aprovar en (com a condição acima) e o es como 2º idioma; escolher a voz en (candidatas em §6); aprovar o piloto (temas sugeridos em `CONCORRENCIA.md` §4 e na resposta ao orquestrador).

---

## 1. Método
- **Buscas [O]:** 162 consultas sem cota (yt-dlp via WARP), 30 resultados cada, em 10 idiomas (en, es, pt, fr, de + exploratórios it, pl, ja, ru, tr). Por idioma: **5 temas escritos nativamente** (Iwo Jima, Pearl Harbor, Omaha/Normandia, Hiroshima, Área 51) em 2 ordens (relevância e "este ano por views"), **2–3 fórmulas traduzidas** em 2 ordens (relevância e data de envio) e **0–3 temas locais** (es: Malvinas, Guerra Civil Espanhola, Chaco; pt: Monte Castelo/FEB, Paraguai, Canudos; fr: Verdun, Maginot, Zona Vermelha; de: Atlântico-Wall, Peenemünde, Lost Places; it: Linha Gótica).
- **Filtros:** ≥ 4 min, não ao vivo, idioma do vídeo = idioma da busca (áudio/língua declarada, senão script/palavras-chave) e título cita o tema (regex nativa). `videos.list` em 6.381 ids (132 un.). **Área 51 foi tirada das medianas de "guerra"** (é demanda de MrBeast/ET, não do formato).
- **Fórmulas traduzidas:** en "why can't you visit Iwo Jima" · es "¿por qué no puedes visitar Iwo Jima?" · pt "por que você não pode visitar Iwo Jima" · fr "pourquoi on ne peut pas visiter Iwo Jima" · de "Warum darf man Iwo Jima nicht besuchen" (+ "what's still under Pearl Harbor" e "Midway" traduzidas).
- **Limites:** top-30 por consulta, não o universo; as medianas de de/it/pl/tr têm poucos vídeos (n pequeno); a nota é minha, as faixas de RPM são **[I]**.

## 2. Demanda por idioma [O]

{T1}

Mediana do top-10 e vídeos ≥ 100 mil de 2026, por tema nativo (Área 51 só para referência; **atenção ao n**: de Pearl Harbor tem 1 vídeo e pl/tr Pearl Harbor 0, então 19,8 mi e 0 não valem; a coluna anterior só usa temas com n ≥ 5). Na tabela anterior, a linha "en" conta só títulos nos 5 temas buscados (18 canais); o mapa completo tem 21 clones em `CONCORRENCIA.md`:

{T2}

- **O tema perde força fora do en [O]:** Iwo Jima (en 1,43 mi → es 155 mil → pt 87 mil → fr 14 mil → de 1 mil). O lugar que gerou o hit do WTS **não é demanda es/pt**; Omaha (es 1,13 mi, pt 579 mil) e Hiroshima (es 1,53 mi, pt 1,16 mi) sim, mas como documentário de evento, sem a pergunta "por que não pode visitar".
- **Prova do formato [O]:** só em en (WTS 4,54 mi; Omaha 341 mil; Forgotten Fleet; Ship Tales). Em es o maior título-fórmula de 2026 tem **115 views**, em pt **3,6 mil**, em de **111**, em fr/it **nenhum**. Os "por que NUNCA sacarán o USS Arizona" (es: Titanes Olvidados 380 views, Bajo Cubierta 26), "Onde estão hoje os 8 encouraçados" (pt: Fantasmas do Oceano 1,5 mil, Colossos do Mar 3,6 mil), fr (L'Empire des Machines 39) e de (truter 101) parecem **traduções/adaptações do Forgotten Fleet e do Ship Tales** [I], todas de outubro/novembro de 2026.
- **ja [O]:** demanda grande (mediana 1,10 mi; 42 vídeos ≥ 100 mil em 2026, Iwo Jima 1,27 mi), mas é ponto de vista japonês (Hiroshima 1,61 mi, Pearl Harbor 929 mil, yukkuri e TV), e **0** títulos-fórmula de lugar. [I] RPM ~US$ 2,4–7,2.
- **ru [O]:** Pearl Harbor 1,06 mi e Hiroshima 2,23 mi, mas Iwo Jima 11,5 mil e a trava de RPM elimina (anúncios suspensos para a Rússia em 2022; [I], conhecimento da política, não reconsultado hoje).

## 3. Concorrência por idioma (clones da fórmula)
- **en [O]:** 21 canais do molde WTS ({17} puros de 27/09 em diante; mediana das medianas 28 views; melhor clone literal do Iwo Jima 910 views; melhor clone com outro lugar 6,2 mil) + 3 canais de navios com tração (Forgotten Fleet, Ship Tales, Insight Ship) + IT'S HISTORY. **Dono forte**: WTS (3,7 mil inscritos, 4,54 mi no hit). Nota **3** (limítrofe).
- **es [O]:** 3 canais copiando o título do Iwo Jima (El Origen del Presente 115 views, Lo Que Aún Queda X 74, Actualidadmilitar 58) + 2 traduzindo os navios; todos de out/nov 2026. Nota **7**.
- **pt [O]:** 4 títulos-fórmula (GuerraDocumentada 24 views; Fantasmas do Oceano 878–1,5 mil; Colossos do Mar 3,6 mil; Ainda Está Lá 9,5 mil nos naufrágios de Midway). Nota **8**.
- **fr [O]:** 0 clones diretos (1 tradução de navio). Nota **10**; **[I]** vazio também pode ser falta de demanda (a demanda fr é 1/30 da en).
- **de [O]:** 1 clone (Cain Brown, 111 views) + Akte Ernstfall e Zwei Seiten des Krieges em formato diferente. Nota 9.
- **it/pl/tr/ja/ru:** 0 clones; nota 7–9, sem demanda pelo formato (ja: demanda grande em outro formato).

## 4. RPM [I]
Faixa do nicho história/documentário (`playbooks/garimpo-tendencias.md`: en US$ 4–8) × fator do idioma: **es 0,25–0,4×, pt 0,25–0,35×, fr 0,5–0,7×** (tabela da fábrica). Para **de, it, pl, ja, tr** não há fator na fábrica; usei os do `archive-in-minutes/IDIOMA.md` (de ≈ 0,6–1×; it ≈ 0,4–0,6×) e **hipóteses** para ja (0,6–0,9×), pl (0,2–0,4×) e tr (0,1–0,25×). Guerra com imagens violentas pode ter anúncio limitado em qualquer idioma (reduz a faixa; sem dado próprio). A receita por view em es/pt é **~1/3 da en**; para igualar a receita do en, o es precisaria de **3–4× as views**, o que a demanda (1/2 a 1/3 da en) não entrega.

## 5. Matriz (pesos 30/25/20/15/10)

{T3}
**Critério de cada nota [I]:**
- **Demanda:** mediana do top-10 dos 4 temas de guerra e vídeos ≥ 100 mil em 2026 (tabela §2), com 10 = en. es 6 (787 mil; 16) e pt 4,5 (497 mil; 9), com desconto de 0,5 por **não haver prova do formato**; ja 7 (1,10 mi; 42, mas de ponto de vista japonês); ru 4; fr 2; de/it/pl 1,5; tr 0,5.
- **Concorrência (10 = vazio; 0 = dono + dezenas de clones):** en 3 (21 clones + 3 canais fortes em outro tema), es 7, pt 8, ja 7 (TV e yukkuri fortes, sem prova do formato), ru 8, fr 10, de/it/pl/tr 9.
- **RPM:** en 10; de 8; ja 7; fr e it 6; es 4; pl 3; pt 2,5; tr 2; ru 0.
- **Viabilidade:** pt 10 (o Rodrigo lê, voz clone dele no `historia-ptbr`); en 9 e es 8 (ele lê; vozes Fish nativas); fr 5 (não revisa); it 4; de/pl/ru 3; ja/tr 2.
- **Risco:** 6 padrão (arquivo de guerra, anúncio limitado possível, direitos de imagens de arquivo); de 3 (§86a StGB com material da 2ª Guerra); ja 5; tr 5; ru 2.
- **Travas:** concorrência ≤ 2 ou RPM ≤ 1. **ru cai (RPM 0)**. **en fica a 1 ponto da trava** (nota 3).
- **Desempate (< 0,3):** en → es → pt → fr → de. es ({MX['es']['base']:.2f}), ja ({MX['ja']['base']:.2f}) e pt ({MX['pt']['base']:.2f}) ficam a menos de 0,3 entre si: a ordem da preferência deixa **es em 2º e pt em 3º**; ja fica fora por inviabilidade operacional.

**Sensibilidade [O]:** com **pesos iguais** e com **RPM 30%/demanda 20%** o **vencedor não muda (en)**. O **2º** muda: com pesos iguais es e pt empatam (6,2) e vence o es pela ordem; com RPM 30% fr e ja (6,05) passam o es ({MX['es']['rpm30']:.2f}) por ≤ 0,1 (empate técnico, a ordem mantém o es). Ou seja, o 2º é **instável** (empate entre es, fr e pt); o 1º não.

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
"""
open(R + "/IDIOMA.md", "w").write(txt); print(len(txt))
