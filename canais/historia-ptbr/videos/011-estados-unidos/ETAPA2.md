# ETAPA 2 · historia-ptbr/011 Estados Unidos (youtube.videos id 44) · 16/11/2026

**Resultado:** `entrega/video.mp4` **15:48** (947,9 s), 1080p30, **−15,2 LUFS**, pico −4,3 dBFS, **0 telas pretas**, 0 silêncios > 1,5 s, 21 cortes no 1º minuto, 19,5 cortes/min. Pode ir ao ar: **qua ou sex**. Drive: não subido (a rotina noturna sobe a partir de `entrega/`).

## Custo (financas.consumo, ref_id 44; teto US$ 8): ≈ US$ 2,85
Fish drama-3 US$ 0,15 (incl. 3 tomadas do hook) · **fal US$ 2,07** · Runpod US$ 0,33 (7 partes; 1 Pod perdido por timeout do comando, US$ 0,03) · pré-QA Anthropic US$ 0,30. Codex US$ 0.
- fal alto porque a **cota do Codex acabou** (usage_limit_reached; 5 h 54%, semana 16%) na refação de 38 imagens: 16 imagens + 4 bases de thumb + 5 refeitas pelo `img_fal.py`. **US$ 0,18 perdidos:** `img_codex.py` com fallback fal cobrou 4 bases de thumb mas devolveu "fal também falhou" sem salvar os arquivos (bug a investigar; rodei `img_fal.py` direto).

## Imagens: Codex × fallback
248 do storyboard (+4 bases de thumb): **~215 pelo Codex**, **~33 pelo fal** (cota). Lote-prova de 6 aprovado. Prancha completa em 6 grades (`qa/pranchas/`) pegou **vazamento de estilo das refs do Egito** em ~38 imagens (faraó, turbante, pirâmide, palmeira, coroa, "guia" de capacete safári) e bandeiras (inclusive Confederada no mapa da Guerra Civil I137): refeitas com sufixo `strictly the United States… NO turbans/crowns/palm/pyramids/flags` (aplicado direto em `cenas.json`; o `roteiro.py` NÃO tem esse sufixo: se regerar `cenas.json`, reaplicar). Depois do pré-QA, refeitas I111 (tribunal com colunas gregas), I113 (cherokees com turbante), I120 (sino com ornamento/inscrição), I169 (skyline com arranha-céu em Ellis), I238 (cheque com texto inventado → papel em branco com faixa vermelha). I215 (V do "Duplo V") trocado por dois chevrons dourados (o Codex/fal desenhava "W"). Sem corpos, sangue, correntes nem símbolos nos planos graves (1619, remoção cherokee, Guerra Civil, 1941–45).

## Voz
Fish drama-3, 1 chamada por bloco, 66 blocos, ~US$ 0,13. Grafias do `FALA` sem troca. Whisper bruto mín 80% (13 blocos < 93%, nomes), média 96,6%; **fonético mín 95,1%, média 99,4%**; nenhuma tag falada. Hook: 4 tomadas, melhor combinação `abcaaa` (repetição 0,10 × 0,12 da tomada única). **Incidente:** timeout de leitura do Fish no N030 gravou mp3 de 0 byte no cache (o `tts_fish.py` não detecta); achei com `ffmpeg -f null`, apaguei arquivo e cache e regerei. **Ouvir os nomes antes de publicar** (ninguém ouviu): Rótchester, Frédérik Dâglas, Djêimstáun, Sicóia, Tcherokí, Guétisburg, Uóng Quim Árk, Ténessi, Rári Bârn, Rôusvelt.

## Pré-QA (120 stills, Claude Sonnet com visão)
1ª rodada: 1 bloqueante (cheque I238 com texto inventado, refeito), 10 altos. Corrigidos: I111, I113, I120, I169, I238 (acima). **Falsos positivos / aceitos:** mapas estilizados (costa/Flórida/Luisiana aproximadas, estilo cartoon; rótulos no código corretos), bandeira britânica em I-rei (é a do rei), cartola/anacronismos de estilo, cena do smartphone (I196, gag simbólica planejada, agora em cenário colonial), "carro dos anos 1950" no cap. 8 (intencional), cabeças marrons no jornal negro (I-98, intencional), sino com gaivota/anacronismo de figurino (I-Q10), placas de capítulo sobre a cena (layout padrão). Não rodei 2ª rodada completa (refiz só as 5 imagens).

## Render
Runpod em 7 partes (0–7108, 7109–10708, 10709–14308, 14309–17908, 17909–21508, 21509–25108, 25109–28435), todas com quadros = esperado e conferência SSIM aprovada; concat + `mix.wav` AAC 192k. Trilha: pad de Sol + violão/banjo (Karplus-Strong brilhante, pentatônica maior de Sol) com rabeca nos caps. 1–7, piano suave esparso em Sol eólio do cap. 8 em diante. **Armadilha:** parte de 4 blocos (7.109 quadros) passa de 10 min com Pod lento (A5000 ~170 s por bloco de 60 s) e o `timeout` do comando matou o render (Pod destruído pelo trap, US$ 0,03); partes de 2 blocos (3.600 quadros) cabem sempre.

## QA (item 6b/6c) — timestamps conferidos na `legendas.srt`
- Detector de cópia: **1/100** (`SIMILARIDADE.md`); `CRIVO-ANGULO.md` **APROVADO** (r1); `CRIVO.md` APROVADO (r3).
- **Promessa paga:** Douglass e "o que é, para o escravo, o seu Quatro de Julho?" **0:17–0:29** (Thumb A); pergunta central ("…potência do mundo?") termina **0:46** (≤ 0:50); sino "já está rachado e mudo" **0:48**; "Guarde a pergunta de Douglass" **1:03**; frase "todos os homens são criados iguais" 2:39 (T2); **"E aqui está a primeira peça da resposta" 3:40** (≤ 4:00; a promessa é paga a partir daí e confirmada em 14:57 "lembra da nossa pergunta?" / 15:01 "A frase não fez dos Estados Unidos uma potência sozinha…"); sino batizado 6:38 "ele rachou" / 6:41 "calou para sempre" (Thumb B); "a outra metade da nossa pergunta, a potência" 9:57; fecho 15:01–15:45 (≈ 45 s), 1 frase sobre os 250 anos (15:24), sem anúncio de próximo vídeo.
- **Thumbs** (`thumbs/compose.py`, bases por `img_fal.py`: cota Codex esgotada): A `rosto-emocao` = Douglass (cabeleira escura) apontando para a festa na janela, "IGUAIS?"; B `objeto-simbolo` = Sino rachado aceso em ouro, fundo preto, "LIBERDADE", bronze sem letras; C `antes-depois` = Independence Hall 1776 sépia | 2026 entre arranha-céus, divisão no código, "1776" "2026". As 3 parecem 3 vídeos diferentes e leem a 320×180 (`thumbs/prancha-celular.jpg`). A = T1, B = T2, C = T3; pares gravados em `youtube.embalagem_variantes`.

## Entrega
`entrega/`: video.mp4, legendas.srt, thumb-A/B/C.jpg, thumbnail.jpg (= A), pacote/youtube.txt. Capítulos conferidos (crescentes, 0:00 a 15:01).

## Trechos para conferir
0:17–0:50 hook · 3:40 primeira peça · 6:38 sino · 7:52 cap. 6 (87 anos, Gettysburg) · 12:05 cap. 9 (Randolph/Pearl Harbor) · 13:32 cap. 10 (cheque, King) · rótulos de mapa (posição não conferida além do pré-QA).

## Pendências
Ouvir os nomes (voz). `img_codex.py`: fallback fal cobra e não salva (investigar). `tts_fish.py`: validar mp3 > 0 byte após timeout. `roteiro.py` precisa receber o sufixo "strictly the United States…" para novos regenerados; refs de estilo vêm do Egito e vazam elementos egípcios em vídeos de outros países (já visto no 010).
