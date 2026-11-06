# RELATÓRIO · historia-ptbr/004 · "A história INTEIRA da China em 16 minutos" (youtube.videos id 10)

Job: `~/workspace/referencias/BRIEF-historia-004-china.md` (05/11/2026). Executor: Claude Code (Opus), uma sessão `claude -p`. Nada foi publicado nem enviado ao Telegram. **Entregue no Drive** em `Youtube/História em minutos/004-china/`.

## Entrega (`entrega/`)
- `video.mp4`: **16:14**, 1080p30, −15,3 LUFS, 0 telas pretas. Hook de **1:16**.
- `legendas.srt`; 3 thumbs (1280×720, < 250 KB); `pacote.md` (título, descrição, 12 capítulos, fontes, tags, checklist).

## Decisões
1. **Referências** assistidas e transcritas (`ref/`): HiM China (`EOA5-VFVI-g`, 55 mil, 16:58) e Animated History (`wuhnBi8jNl0`, 1,17 mi, 25:56). O HiM gasta 2:50 em pré-história e só chega aos Shang aos 4:16; o Animated tem 25 min com merchan. Nossa estrutura começa no 1º segundo com uma pessoa (Qin Shi Huang) e chega aos Shang em 1:16.
2. **Hook = anedota do elixir de Qin Shi Huang** (molde HiM: anedota → "Essa é a história inteira da China: o país que morreu mais vezes do que qualquer outro… e sempre voltou. Como?" → promessa → "Guarde essa ideia, e esse túmulo fechado"). Pago no fecho: o túmulo continua fechado, a dinastia de dez mil gerações durou quinze anos, mas a ideia de uma China só sobreviveu; pergunta para os comentários: "abria o túmulo ou deixava fechado?".
3. **Fio condutor: o Mandato do Céu** ("o Céu dá o direito de mandar… e pode tirar"), retomado em cada queda: Zhou, Qin, Turbantes Amarelos ("o Céu azul está morto"), Wu Zetian, a cheia de 1344, 1644, o Reino **Celestial** dos Taiping, 1911 ("pela última vez"), Tangshan e Mao (1976) e o fecho. Fio secundário: a máquina que sobrevive às famílias (escrita, um centro, a prova), "o segredo da China" contra Roma.
4. **Tamanho:** 2.093 palavras (do rascunho de 2.492, cortado em 2 rodadas antes da voz) → 970 s de voz → 16:14.
5. **Nomes chineses:** o `roteiro.py` agora gera duas grafias por bloco: `texto` (fonética, vai ao Fish: "Tchin Chi Ruang", "Djou", "Dju Iuan-djang"…) e `tela` (grafia correta, vai para legenda e SCRIPT). O `build.py` usa `tela` nas legendas. O Whisper transcreveu "Qin", "Zhu Yuanzhang" e "Xiaoping": a pronúncia saiu perto do nome real.
6. **Voz:** Fish drama-3, clone do Rodrigo, 1 chamada por bloco, gaps 0,35/0,9/1,5 s. **Cobrança confirmada no drama-3**: crédito 48,01653 → 47,91747 = US$ 0,09906 = 9.906 bytes × US$ 10/M (no s2.1-pro seriam US$ 0,149). Whisper fonético 99,4% de média.
7. **Imagens:** nano-banana-2.1/edit + 3 refs do canal; lote-prova de 6 (multidão, mapa, imperador com nome, Confúcio, túmulo, Muralha) aprovado na 1ª tomada com a regra "round-white-head cartoon…"; 215 imagens, 8 refeitas (ver `QA.md`).
8. **Trilha:** a mesma síntese do 003, trocada para a **pentatônica chinesa** (modo gong em Ré, timbre de guzheng).
9. **Thumbs** (padrão COROA × TURBANTE): 1 IMPERADOR × MORTE "210 a.C." (Qin com as pílulas × a morte, exército de barro e rios de mercúrio; principal), 2 DRAGÃO × CANHONEIRA "1839" (oficial Qing × capitão britânico com o baú de ópio), 3 IMPERADOR × MONGOL "1279".

## Correções de fatos (checagem antes da voz, `SOURCES.md`)
1. "Quatro anos depois, a China estava em revolta" → **"Um ano depois"** (Chen Sheng, 209 a.C.; quatro anos é a queda).
2. Pílulas de mercúrio ditas como tratamento, **sem afirmar** que causaram a morte.
3. Cortados por contestados: os 460 estudiosos enterrados vivos, "8 mil soldados, cada um com um rosto diferente", os 36 milhões da revolta de An Lushan.
4. Shenzhen = "cidade pequena", não "vila de pescadores" (mito).
5. A imagem da Chang'e 6 saía com astronautas e com a Terra no céu do lado oculto: refeita como sonda robótica sem Terra.

## Custo direto (financas.consumo, ref_id 10)
| Etapa | US$ |
|---|---|
| Voz drama-3 (hook + teste de nomes, vídeo inteiro, 1 bloco regerado) | 0,12 |
| Lote-prova (6) | 0,28 |
| Lote inteiro (209) | 9,59 |
| Refeitas (8) | 0,37 |
| Bases das thumbs (6) | 0,28 |
| **Total** | **US$ 10,63** (teto US$ 14) |
Custo do fal medido pela API de uso por endpoint (US$ 0,0459/img), não pela queda do saldo.

## Ferramentas mudadas (só na pasta do vídeo)
- `roteiro.py`: camada `FALA` (grafia de voz × de tela). `tools/build.py`: legendas pela grafia de tela; trilha pentatônica. `tools/qa_fonetico.py`: compara com as duas grafias. `tools/espera_render.sh`: espera ancorada em `^node`. Nenhuma tool de `tools/` da fábrica foi alterada.

## Para o Rodrigo
- Ouvir os nomes difíceis (timestamps conferidos na `legendas.srt`): Ying Zheng **4:05**, Sima Qian **4:53**, Wu Zetian **7:19**, Zhu Yuanzhang **9:19**, Zheng He **9:42**, Puyi **12:08**, Deng Xiaoping **14:03**, Xi Jinping **14:54**, Qin Shi Huang **15:31**.
- Teste do hook: anotar a retenção aos 30 s e 60 s no Studio (hook de 1:16 com anedota; comparar com o cavalo de Dario do Irã).
- Publicar é decisão sua; checklist no `pacote.md`.
