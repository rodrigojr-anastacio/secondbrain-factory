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
