# Amostras de voz: hook B01 do piloto Midway (youtube.videos id 30), 12/11/2026

Texto: hook B01 (~115 palavras), "CV" escrito "C-V". Loudness normalizado a ~-16 LUFS, mono. Scripts: `gerar.py` (gera e registra custo), `qa.py` (Whisper small.en + LUFS). mp3 fora do git.

| arquivo | motor / voz / modelo | dur | ppm | Whisper | custo amostra | custo/vídeo (~16.500 car.) | impressão |
|---|---|---|---|---|---|---|---|
| **A-fish-adrian.mp3** | Fish, Adrian (bf322df2), s2.1-pro, por frase + 0,32 s | 48,5 s | 126 | 99,0% | US$ 0,0175 | ~US$ 0,25 | tags oficiais "deep, slow, measured, serious, dramatic": a mais grave e solene, mas lenta demais (126 ppm) e tende ao dramático; precisaria de speed ~1,15 |
| **B-fish-ethan.mp3** | Fish, Ethan (536d3a5e), s2.1-pro, por frase + 0,32 s | 40,4 s | 152 | 100% | US$ 0,0175 | ~US$ 0,25 | tags "calm, authoritative, documentary": ritmo exato (152 ppm), narrador que conta; menos grave que Adrian |
| **C-elevenlabs-brian.mp3** | ElevenLabs, Brian (nPczCjzI, premade), eleven_multilingual_v2, speed 0,95 | 40,6 s | 151 | 97,6% | 0 marginal (Starter; 276 caracteres do plano) | 0 marginal enquanto couber no plano (16,5k de 38,6k/mês, ~2 vídeos/mês); acima disso ~US$ 3–4 (estimativa, plano Creator) | grave e cálido, americano, "comforting"; mais radiofônico/suave; errou "Akagi" ("a Kagi") |
| **D-eleven-adam.mp3** | ElevenLabs, Adam (premade, americano), multilingual_v2, speed 0,95 | 43,1 s | 142 | 99,0% | 0 marginal (589 car. do plano) | 0 no plano (16,5k car./vídeo); idem Brian | "dominant, firm": firme e direto, mais "locutor de trailer" que Brian; Akagi certo |
| **E-eleven-bill.mp3** | ElevenLabs, Bill (premade, americano maduro), idem | 46,7 s | 131 | 99,0% | idem | idem | "wise, mature": o mais velho e solene; lento (131 ppm); Akagi quase ("Akaji" no Whisper, ouvir) |
| **F-eleven-flint.mp3** | ElevenLabs, Flint (voz profissional da biblioteca, americano idoso), idem | 46,4 s | 132 | 98,1% | idem | idem | "commanding, husky": a mais grave e áspera, narrador de documentário de guerra; lento; Akagi certo |
| **G-eleven-george-uk.mp3** | ElevenLabs, George (premade, **britânico**), idem | 43,1 s | 142 | 96,1% | idem | idem | "warm storyteller": britânico caloroso, tipo BBC; "Akagi" saiu "Arcagi" no Whisper (ouvir) |
| **H-eleven-daniel-uk.mp3** | ElevenLabs, Daniel (premade, **britânico**), idem | 46,3 s | 132 | 100% | idem | idem | "steady broadcaster": locutor BBC formal e limpo; Akagi certo; nenhum erro no Whisper |
| extra-fish-adrian-bloco.mp3 | Adrian, bloco inteiro | 44,1 s | 139 | 97,1% | US$ 0,0175 | idem | um pouco mais fluido, porém "It's Admiral..." saiu "Its" (Whisper) |
| extra-fish-ethan-bloco.mp3 | Ethan, bloco inteiro | 39,2 s | 156 | 100% | US$ 0,0175 | idem | quase igual ao por frase; entonação mais corrida |

**Modelo cobrado (Fish):** crédito 46,97813 → 46,94315 = US$ 0,0350 para 2.332 bytes = US$ 15/M bytes, a tarifa do s2.1-pro. Confirmado, sem queda para outro modelo.
**Custo real gasto:** US$ 0,035 (Fish, 4 gerações, lançado em `financas.consumo`, ref_id 30) + ElevenLabs US$ 0 marginal (276 car. do plano Starter, lançado com custo 0). Total: **US$ 0,035** (teto 0,50).

Todos pronunciam Soryu/Hiryu/Kaga certo no Whisper; os números saem por extenso ("ninety-two"). O Whisper escreve em algarismos nas B/C, o que é normal e não indica erro. Só o Brian errou "Akagi". "C-V" foi lido como "CV(s)" por todos.

## Recomendação
**B (Ethan, Fish s2.1-pro, por frase).** Segue a bíblia (documental, calmo, conta), no ritmo-alvo de 150 ppm, 100% no Whisper, custo ~US$ 0,25/vídeo e o fluxo já existente (`tts_fish.py`, registro de custo). O Brian é a alternativa mais "grave", mas custa cota do plano e errou o nome japonês. O Adrian é o mais solene, porém lento e dramático.

## Falta decidir
- O Rodrigo ouvir A/B/C (e os extras) e escolher; só ouvido julga grave, calmo e sotaque.
- Se quiser mais grave que o Ethan: testar Slax ou Voice DL (reserva), ou o Adrian com `speed` ~1,15 (US$ ~0,02).
- Modo por frase (pausa controlada) ou bloco; Ethan serviu nos dois.
- Gravar a voz escolhida em `canal.yaml` (`voz.voz`) e declarar voz sintética na descrição.

## Rodada 2 (12/11/2026, brief clearance-vozes2): D–H
Pedido: mais vozes na linha do Brian + britânicas, e "Akagi" corrigido. Script `gerar2.py` (mesmo texto, mas "Akagi" → **"Ah-kah-gee"**; todas com stability 0,5, similarity 0,75, speed 0,95). Pronúncia: D, F, H acertam no Whisper; E ("Akaji") e G ("Arcagi") ficam duvidosas, só o ouvido decide. O Brian ficou sem refazer (a grafia fonética resolve sem trocar de modelo).
**Custo:** US$ 0 marginal; 5 × 589 = 2.945 caracteres do plano Starter (contador ~11,5k → ~14,4k de 38.634; passou dos ~2.000 estimados no brief porque o texto tem 589 car., não 276). Lançado em `financas.consumo` (custo 0, ref_id 30). Fish não usado.
**Uso comercial:** o plano Starter inclui licença comercial; vozes premade (Adam, Bill, George, Daniel) valem nele. **Flint** é voz da Voice Library: comercial liberado para quem tem plano pago, mas o autor pode retirá-la; para canal de longo prazo prefira premade. Não confirmei os termos na página do ElevenLabs (sem acesso a ela daqui), só pelo que o plano e a categoria indicam.
**Recomendação curta:** linha Brian → **D (Adam)**, ritmo mais perto dos 150 ppm; mais grave → **F (Flint)** se aceitar a dependência da biblioteca. Britânico → **H (Daniel)**, limpo, 100% no Whisper e premade. Tudo ElevenLabs sai de graça no plano até ~2 vídeos/mês; acima disso o Fish Ethan (B) segue o mais barato por vídeo.

## Rodada 3 (12/11/2026, brief clearance-vozes-fish): I–N, vozes da biblioteca do Fish
Script `gerar3.py` (mesmo hook B01, "Ah-kah-gee", s2.1-pro, por frase + 0,32 s, sem tag de estilo). Busca por `GET /model?sort_by=task_count&language=en&tag=...` (documentary, narrator, deep, british, warm). Descartei clones de celebridade (Elon Musk, Morgan Freeman, David Attenborough, Kurzgesagt, Paddington): risco de direitos/remoção. QA: `QA_GLOB='[I-N]-*' python qa.py`.

| arquivo | voz (id, autor) | sotaque | ppm | Whisper | usos / likes | custo/vídeo | impressão |
|---|---|---|---|---|---|---|---|
| **I-fish-calm-storyteller.mp3** | calm storyteller male (e686ae64, Blazing) | americano | 146 | 99,0% | 221 mil / 444 | ~US$ 0,25 | tags "deep, calm, measured, documentary"; Akagi certo |
| **J-fish-slax.mp3** | Slax (9032b5f2, Bahoz Denli) | americano (velho) | 120 | 96,2% | 556 mil / 824 | ~US$ 0,25 | lento (120 ppm); Whisper leu "Akka. G. K. Ga" e "Kiryu": pronúncia ruim |
| **K-fish-documentary.mp3** | Documentary (c3958f08, Hamo) | americano (velho) | 149 | 98,1% | 122 mil / 132 | ~US$ 0,25 | tags "old, deep, calm, authoritative"; **leu "Twenty-two officers" no lugar de 92** (erro de número, reprovada sem regerar); "Arkagi" |
| **L-fish-deep-godmode.mp3** | Deep (bb742915, Godmode) | americano | 153 | 99,0% | 42 mil / 207 | ~US$ 0,25 | "deep, smooth, calm, storytelling"; ritmo exato, tudo certo no Whisper |
| **M-fish-f1-uk.mp3** | F1 (59b8d12e, Selman Türkoğlu) | britânico | 149 | 97,1% | 52 mil / 145 | ~US$ 0,25 | "British, documentary, authoritative"; "Arkagi"; leu "Now to the math" |
| **N-fish-eldrin-uk.mp3** | Eldrin (6428df0a, Sunny) | britânico RP | 135 | 99,0% | 15 / 1 | ~US$ 0,25 | "deep baritone, RP, deliberate"; Whisper 100% nos nomes e números; mais baixo (-17,9 LUFS); pouquíssimo usado, risco de sumir |

**Modelo cobrado:** crédito 46,94315 → 46,89077 = US$ 0,0524 para 3.492 bytes = US$ 15/M bytes (s2.1-pro). Confirmado. **Custo total da rodada: US$ 0,052** (teto 0,25), lançado em `financas.consumo` (ref_id 30). ElevenLabs não usado.

**Licença (não confirmada na fonte):** os termos do Fish que achei dizem que quem usa serviços pagos tem licença de uso comercial; o plano gratuito é só não comercial. Não achei texto sobre o autor retirar uma voz da biblioteca nem sobre uso comercial de voz de terceiros ([termos](https://fish.audio/pt/terms/), versão de 2024). Risco prático: voz de terceiro pode sumir e o canal perde consistência. Vozes **Fish Official** (Ethan, Adrian) são as seguras. Entre as novas, as de uso alto (Slax 556 mil, Calm storyteller 221 mil) sobrevivem melhor; a Eldrin (15 usos) é a mais frágil. Se o Rodrigo escolher uma de terceiros, vale checar com o suporte do Fish e guardar o áudio de referência/id.

**Recomendação curta vs Brian:** nenhuma Fish iguala o calor do Brian, mas **L (Deep/Godmode)** é a mais próxima: americana, grave, calma, 153 ppm, 99% no Whisper, tudo certo em Akagi e números. **I (Calm storyteller)** é a 2ª (mais calorosa, mais usada). Britânica: **N (Eldrin)** é a melhor de timbre e pronúncia, mas frágil (15 usos); **M (F1)** mais segura em uso, com 2 deslizes. Descartar J (lenta, pronúncia ruim) e K (errou o 92). Só o ouvido decide; se nenhuma convencer, o Ethan (B, oficial) segue o fallback barato.

## Rodada 4 (12/11/2026, brief clearance-vozes-fish2): O–T, "um pouco menos deep que a L"
Script `gerar4.py` (hook B01, "Ah-kah-gee", s2.1-pro, por frase + 0,32 s, sem processamento de tom). Busca `GET /model?sort_by=task_count&language=en&tag=…` (narrator, documentary, storyteller, warm, mature, american, baritone). Gerei 8 candidatas, 2 reprovadas no QA e trocadas (arquivos fora do git). Celebridades (Elon, Michael Jackson, Attenborough, Markiplier) ignoradas. **Sotaque e timbre não são confirmáveis por texto: só o ouvido.**

| arquivo | voz (id, autor) | ppm | Whisper | usos / likes | impressão (tags + QA) |
|---|---|---|---|---|---|
| **O-fish-bii2.mp3** | Bii2 (9d1efa16, Veo Pika) | 140 | 99,0% | 67 mil / 140 | "male, middle-aged, deep, authoritative, professional"; nomes e números certos; -17,9 LUFS |
| **P-fish-narrator-maxn.mp3** | Narrator (0327fdb5, Max N) | 151 | 98,1% | 104 mil / 450 | "young, calm, measured, documentary": ritmo-alvo, nomes certos; tag "young" pode ser mais leve que a L |
| **Q-fish-jjk.mp3** | JJK (d6777f50, Locked Downed) | 122 | 99,0% | 48 mil / 229 | "old, deep, calm, serious, authoritative"; nomes certos; lento |
| **R-fish-heistys-voice.mp3** | Heisty's Voice (3054685d, 4y4xn) | 129 | 97,1% | 147 mil / 673 | "old, narration, deep, clear, authoritative"; nomes certos; um pouco lento |
| **S-fish-w2w.mp3** | w2w (4746f1b4, nixise2572) | 118 | 99,0% | 84 mil / 103 | "middle-aged, narration, conversational"; nomes certos, mas lenta; nome genérico |
| **T-fish-news-reporter.mp3** | News reporter (05aff7ff, Yassine El-Hilaly) | 148 | 95,7% | 39 mil / 107 | "young, serious, measured, authoritative": ritmo bom; Whisper leu "Its … report" (talvez só do Whisper) |

Reprovadas e fora: **Atomic** (96 ppm, errou "Akagi/Soryu/Hiryu"), **WNBA Voiceover** (156 ppm, Whisper leu "$307": leitura de número duvidosa).
**Modelo cobrado (não fechou exato):** saldo do Fish 46,89077 → 46,83839 = US$ 0,0524, mas 4.656 bytes a US$ 15/M (s2.1-pro) dariam US$ 0,0698, valor lançado em `financas.consumo` (ref_id 30). A diferença pode ser atraso do contador de crédito (leitura 8 s depois); não vi sinal de outro modelo, mas **não confirmado**. **Custo da rodada: US$ 0,052–0,070** (teto 0,25).

**Recomendação (2 finalistas):** **P (Narrator, Max N)**: ritmo exato 151 ppm, 104 mil usos, tudo certo; é a mais provável de soar "médio-grave documental" sem ser baixo demais. **O (Bii2)**: "deep, authoritative, middle-aged", 140 ppm, 99%; é a mais próxima do timbre da L em autoridade com o ritmo aceitável. Se nenhuma agradar, L segue a referência de estilo e o Ethan (B, oficial) o fallback. Mesma ressalva de licença/remoção das vozes de terceiros da rodada 3.
