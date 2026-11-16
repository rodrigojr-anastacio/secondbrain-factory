# Voz de reserva do Em Relevo: amostras Fish (16/11/2026)

**Por quê:** o canal usa ElevenLabs "Fernanda" (`eleven_v3`, plano de 38.634 caracteres/mês, reset dia 08). Se o plano acabar no meio de uma noite, não há voz Fish escolhida (`biblia/voz.md`). Isto são **só amostras**: o `canal.yaml` não mudou.

**Ouvir no celular:** `todas.mp3` (6:52): "Referência: Fernanda" e depois "Amostra A" … "Amostra F" (rótulos falados com Kokoro, grátis). Cada amostra também está solta (`A-…mp3` etc.).

**Trecho:** o mesmo para todas, do `005-enchente-porto-alegre-2024`: hook b01–b04 (Caxias → Guaíba 5,35 m → 160 mil atingidos → "A resposta está no mapa") + a transição do capítulo 3, b20 ("Se entra tanta água, por que ela não vai logo embora?…"). Texto = `fala` do `shared/blocos.json` (sem as tags do v3). A referência é a Fernanda recortada da `audio/narracao.wav` do 005 (0:00–0:45 e 4:33–4:41, conferido com Whisper).

**Ritmo casado:** o Rodrigo achou as Fish de 08/11 lentas. Aqui cada voz foi gerada no ritmo natural (speed 1,0) e depois acelerada com `atempo` (ffmpeg) até a duração da Fernanda no mesmo trecho (limite 1,5×). A própria Fernanda do 005 já leva 1,36× no hook e 1,1× no corpo. Assim a comparação fica só de timbre e entonação. Loudness −16 LUFS em todas.

| Letra | Arquivo | Voz no Fish (id) | Modelo | Natural (pal/min, hook/trans.) | atempo aplicado | Whisper | Impressão (medida, não de ouvido) |
|---|---|---|---|---|---|---|---|
| REF | `REF-fernanda-eleven-v3.mp3` | Fernanda, ElevenLabs `7iqXtOF3wl3pomwXFY7G` | eleven_v3 | (já com 1,36/1,1) | — | — | a voz atual, para comparar |
| A | `A-fish-energica-drama3.mp3` | "Putinha 1" (o nome no Fish é esse) `1573caa3d6444e16a28eab1f094e1416` | drama-3 | 117 / 133 | 1,50 / 1,31 | 0,994 / 1,00 | a mais lenta e pausada de natural: mesmo no limite de 1,5× ficou 6 s mais longa. Descrição "energética, clara, profissional". A mais usada (73 mil usos) |
| B | `B-fish-documental-drama3.mp3` | "Caine (Brazilian Portuguese)" `8f50c4c145e44ec280fb759b32934890` | drama-3 | 142 / 148 | 1,42 / 1,17 | 1,00 / 1,00 | texto perfeito, mas o Whisper não pôs "?" na pergunta do hook (pode ter entonação fraca: ouvir em "Então, como a chuva da serra…") |
| C | `C-fish-natasha-drama3.mp3` | "#NATASHA" `e8bccb7beecd46c6a1c64813e0238fa9` | drama-3 | **163 / 176** | 1,24 / 1,00 | 0,994 / 1,00 | **a mais rápida de natural, mais perto da Fernanda; precisou de menos atempo** e as duas perguntas saíram com "?". Minha aposta para reserva |
| D | `D-fish-jovem-clara-drama3.mp3` | "Voz feminina" `5b5a485751824c1993e210602cee16cb` | drama-3 | 138 / 138 | 1,46 / 1,26 | 0,994 / 1,00 | jovem e "brilhante" (perfil de anúncio). Pode soar publicitária demais para desastre |
| E | `E-fish-masculina-drama3.mp3` | "Narrador de Historias e Ciências" `0ba1afd27db44eb2b4cb27fd331b93aa` | drama-3 | 145 / 154 | 1,39 / 1,12 | 1,00 / 1,00 | masculina, de contraste: narrador educativo, calmo. 44 mil usos |
| F | `F-fish-natasha-s21pro.mp3` | #NATASHA (a C) | s2.1-pro | 178 / 198 | 1,14 / 1,00 | 0,978 / 0,939 | mais barata e rápida, mas **soltou um ruído ("oh, oh, oh…", segundo o Whisper) entre o b03 e o b04** e a pergunta da transição saiu sem "?". drama-3 > s2.1-pro nesta voz |

Nenhuma é clone de celebridade nem de personagem de dublagem (regra das rodadas de clearance de 12/11/2026). Ficaram de fora, sem repetir: as 5 femininas e a `1d8cb595…` de 08/11 (`pesquisa/canal-clima-2026-11/voz-fish/`), além de vozes com nome de famosa ou de personagem (Camila Fabri, Ana Castela, Katherine Pierce, Nico Robin…). **Ressalva:** vozes de terceiros no Fish podem sumir da biblioteca. Se uma virar a reserva, vale clonar uma voz própria ou guardar o id e uma amostra.

**Whisper:** faster-whisper small, números normalizados (`shared/normaliza_pt.py` do 005). Todas leram o texto inteiro. As pequenas perdas são grafia ("há 100 km" no lugar de "a 100 km").

**Custo real: US$ 0,064** (teto US$ 1). drama-3: 4.915 bytes, US$ 0,0492. O crédito do Fish caiu de 44,941615 para 44,892465, ou seja, **o drama-3 ainda é cobrado a US$ 10/M** (preço da promoção), não aos US$ 50/M do `tts_fish.py`. s2.1-pro: 983 bytes, US$ 0,0147 (crédito 44,892465 → 44,87772, confere). Os dois valores estão em `financas.consumo` (ids 455 e 456, projeto `em-relevo`, sem `ref_id`). O 455 foi corrigido para o valor cobrado de fato.

**Se uma delas virar a reserva:** no `canal.yaml`, `voz.motor: fish`, `voz: <id>`, `modelo: drama-3`, e o `tts_fish.py` já serve, com `--bloco` e atempo no `monta_audio_v2.py` como hoje. As tags `[serious]/[curious]` do v3 **não** valem no Fish: tirar do `fala_tts` ou trocar pelas do drama-3. Antes disso, teste um vídeo inteiro (Whisper por bloco).

**Arquivos:** `gerar.py` (Fish, com cache em `brutos/` e custo), `qa.py` (Whisper → `qa.json`), `rotulos.py` (Kokoro), `monta.py` (corte da Fernanda, atempo casado, `todas.mp3`; `monta.json` traz os fatores). `brutos/` e `todas.mp3` (6,6 MB) ficam fora do git.
