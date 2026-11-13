# Voz: historia-ptbr

Regra de canal: **prevalece** sobre `conhecimento/anti-padroes.md` (que guarda só o comportamento geral do Fish e das ferramentas). Configuração em `../canal.yaml` (`voz`).

## Voz do canal
- **Clone pt-BR feito pelo Rodrigo no Fish:** `48613fc675f84984981683d92266e543`, velocidade **1.0** (aprovada; 0,95 soou lento). [canal.yaml]
- **Modelo e técnica desde 05/11/2026 (decisão do Rodrigo, BRIEF-historia-003-v2-fase2):** Fish **`drama-3`**, **1 chamada por bloco** (técnica da amostra B2, `videos/003-ira/v2-amostras/voz/`), temperature/top_p no padrão, tags de tom só onde a emoção muda, gaps de 0,35 s / 0,9 s (ideia nova) / 1,5 s (capítulo) no `build.py`. `tools/tts_fish.py historia-ptbr blocos.json audio --video <id>` já faz isso pelo `canal.yaml` (`modo: bloco`, cache por bloco).
  - **Confirme a cobrança:** com header de modelo errado, o Fish cai calado no s2.1-pro. O `tts_fish.py` mostra o crédito antes e depois. No 003 v2, a queda bateu com bytes × US$ 10/M (promoção até 12/11/2026; depois US$ 50/M, ~US$ 0,65 por vídeo).
  - Medidas do 003 v2 (60 s iniciais): repetição melódica 0,09, queda no fim −2,9 st, faixa de 11 st, F0 de 103 Hz (~1,7 st mais aguda que o s2.1-pro). Whisper: 99,5% em média com chave fonética (o Whisper bruto reprova nomes persas e "xá" = "cha"; use `videos/003-ira/v2-voz/qa_fonetico.py`).
  - Mais lento: ~125–133 ppm (ver `roteiro.md`, Tamanho).
- Tom: narrador contador de história, caloroso e curioso, que **conta** e não lê. Não é o narrador seco de documentário do `dossie-es`.

## Ritmo na bíblia de roteiro v2 (só vídeos ≥ 006; Hipótese desde 07/11/2026)
A `roteiro.md` v2 (regra 10) mira ~140–145 ppm com pausas (hoje 127–129 no drama-3). A voz aprovada **não muda**; o teste do 006 é encurtar os gaps do `build.py` (0,35/0,9/1,5 s → ~0,25/0,6/1,2 s) e medir os 60 s iniciais antes do vídeo inteiro. Registre aqui o resultado. Vídeos 001–005 seguem as pausas abaixo.
- **Resultado do 006 Roma (09/11/2026):** hook N001–N008 com gaps 0,35/0,9/1,5 s = 101,5 s (128 ppm) × 0,25/0,6/1,2 s = 100,5 s (129 ppm); vídeo inteiro com os gaps novos: **128 ppm** (2.230 palavras em 17:27). O drama-3 tem ~23% de silêncio **dentro** dos blocos, então os gaps entre blocos quase não mudam o ritmo. Conclusão (Hipótese): 140 ppm só vem com texto mais enxuto (orçamento de palavras pelo ritmo real, ~128 ppm) ou outro ajuste de voz; os gaps novos ficam (a repetição melódica do hook caiu de 0,21 para 0,15 com eles). [QA.md 006]
- 006: "Tito Lívio" virou "título livre" no Whisper → reescrito "o historiador Tito Lívio… ele era romano" (nome raro dito 1 vez, com contexto). Nomes latinos em forma portuguesa (Cipião, Catão, Odoacro, Augústulo, Caracala) saíram certos sem grafia fonética; o Whisper corta palavras ("a Nibau", "da Núvio"): use a nota fonética (`006-roma/tools/qa_fonetico.py`, sem espaços).
- **007 Rússia (09/11/2026):** o orçamento de palavras pelo ritmo real funcionou: 2.140 palavras = 16:47 (128 ppm de novo). Grafias de voz: **"czar" → "tzar"** (com "czar" o Fish diz algo como "kuzar"/"casar"; com "tzar" o Whisper ouve "Tsar"), "Gorbatchóv" (com "-chóf" saía "Gormachov"), "Ivã", "Riazã", "Kalitá", "Ugrá", "Iermák", "Mínin", "Pojárski", "Románof", "Pugatchóf", "Uainaputina" (Huaynaputina). "Olhe os rios" vira "Olhos rios": evite verbo terminado em vogal antes de "os". Hook: a take3 inteira deu repetição 0,10 (as outras 0,29–0,34): vale gerar 4 tomadas. Whisper fonético mín 95,1%, média 99,1%. [QA.md 007]

## Histórico: estado em 04/11/2026 (resolvido em 05/11 com o drama-3 por bloco)
- Feedback do Rodrigo sobre o 002: "robótica e atropelada". A/B de 11 tomadas do hook do 003 (`videos/003-ira/amostras-voz/LEIA.md`, US$ 0,14): texto reescrito para a fala + `tts_fish.py --por-frase` (0,32 s entre frases) teve a menor repetição melódica (0,09 × 0,14 do jeito do 002); tags de direção e velocidade 0,97 pioraram. O 003 v1 saiu assim (`modo: por_frase`). [conhecimento/anti-padroes.md §2b]
- **Depois de ouvir, o Rodrigo achou a narração do 003 ainda ruim** ("parece que o cara tá lendo corrido, e não contando uma história") e **preferiu a amostra A (`A-atual`)**. Ele quer testar o modelo mais recente do Fish. [BRIEF-historia-003-v2.md, 04/11/2026] Teste em `videos/003-ira/v2-amostras/voz/` (job `historia-003-v2`). **Registre aqui o modelo/técnica aprovados.** Até lá, a decisão "G = por frase" é **Hipótese em xeque**.
- **Hipótese:** parte do "lendo corrido" vem do roteiro em fichas (sem conectores), não só do motor. Roteiro contínuo (`roteiro.md`) primeiro, parâmetro depois. Se ainda soar robótico, regravar a referência do clone (30–60 s naturais com pausas), não mexer em temperature/top_p (sem efeito no A/B).

## Pausas e tags (aprovado até o 002; valem para o encadeamento entre blocos)
- Encadeamento no `build.py`: ~0,35 s entre frases do mesmo assunto, **~0,9 s quando muda de ideia** (`IDEIA` no `roteiro.py` → `"ideia": true`) e **~1,5 s antes de capítulo**; cauda de 0,15 s (limiar −45 dB). Não aparar o silêncio natural do fim das frases de forma agressiva. [ETAPA3.md 001]
- Tags de tom (não são lidas pelo s2.1-pro): `[curious]`, `[serious]`, `[amazed]`, `[warm]`, `[slightly dramatic]`, no máximo 1 por frase, variando ao longo do vídeo. No Egito v2: 59 tags (12 curious, 16 serious, 8 amazed, 12 warm, 11 slightly dramatic). Com a voz por frase: tag só onde a emoção muda (~1 a cada 2–3 blocos). [ETAPA3.md 001; skill roteiro]
- `[break]`/`[long-break]`: no modo por frase, sem `[break]` (a tool já põe 0,32 s); `[long-break]` só antes de revelação. Sem o modo por frase: `[break]` só entre ideias, no máximo ~1 por minuto; excesso de pausas soou "lento e estranho". [estilo.md antigo]
- O Fish **corta a frase curta depois de `[break]` no fim do bloco** ("Guarde essa chuva" sumiu na Índia): feche o bloco com tag de tom em vez de `[break]` e confira com Whisper por bloco. [QA.md 002]

## Nomes estrangeiros (desde 004 China, 05/11/2026)
- O Fish lê como português: "Qin" sai "kin", "Zhou" sai "zou". O `roteiro.py` do 004 tem a lista `FALA` e grava no `blocos.json` duas grafias: `texto` (fonética, vai ao Fish: "Tchin Chi Ruang", "Djou", "Xang", "Dju Iuan-djang", "Djêng Rrâ", "Dâng Chiau-ping", "Rran") e `tela` (grafia correta, usada nas legendas pelo `build.py`). O Whisper transcreveu "Qin", "Zhu Yuanzhang" e "Xiaoping" a partir da grafia fonética. Use exônimo em português quando existir (Nanquim, Pequim). No QA, compare com as duas grafias (`004-china/tools/qa_fonetico.py`). Teste os nomes com 4–5 blocos (US$ 0,02) antes do vídeo inteiro. [RELATORIO.md 004]
- **005 Brasil (07/11/2026):** nomes em português quase não precisam de grafia fonética; só "Kubitchéque", "Nassáu", "Bretôa", "Fórdlândia" e "pê érre" (sigla PR). Palavra que começa por vogal logo depois de outra terminada em vogal some ("jacaré, Ipanema" → Whisper "jacaré e panema"): separe com reticências ("… até Ipanema").

## Repetição melódica do hook: tomadas múltiplas (005 Brasil, 07/11/2026)
- O mesmo texto no drama-3 varia muito entre tomadas: 5 tomadas completas do hook do 005 deram repetição de 0,14 a 0,30 nos 60 s. Escolher a melhor tomada **por bloco** (busca aleatória de ~160 combinações medidas com o `medir.py`) levou a **0,11** (meta ≤ 0,12) por US$ 0,04 a mais. Instale a tomada escolhida copiando o mp3 sobre `audio/N###.mp3` (é hardlink do `blocos-cache`, então o cache passa a guardar a tomada boa). Também ajudou reescrever: pergunta no meio do hook ("O que tem lá dentro?", "E sabe onde ele aparece?") e nenhuma frase-lista curta ("Papagaios, saguis, macacos."). **Hipótese** de processo enquanto o drama-3 estiver barato. [QA.md 005]
- Junção "Djou enfraqueceram" virou "duem fraqueceram": evite nome fonético curto colado em verbo que começa com vogal.

## Não faça
- Voz "Dio Historias"/espanhol neutro (é do `dossie-es`) ou Kokoro `ff_siwis` (é do `lotr-fr`).
- Tags de direção ("[serious, calm]", "[low voice]") e velocidade 0,97 (A/B do 003).

## 008 França (13/11/2026)
- 2.000 palavras = 15:16 (131 ppm, 54 blocos). Whisper fonético mín 92,5%, média 99,1%. Grafias de voz do `FALA` (Suassôn, Rrãns, Verdân, Orleã, Crecí, Azancúr, Calê, Buvíne, Nânt, Notrrí Dâm, Uóterlu, Sedã, Gól, Alézia, Capêto) saíram sem troca; o Whisper ouve "Sua som" e "Hans" para Soissons e Reims (Hipótese: é limite do Whisper, não da voz; ouvir). Hook: 4 tomadas, melhor combinação por bloco = repetição 0,10 (tomadas únicas 0,16–0,30), confirmando a regra do 005. [ETAPA2.md 008]
