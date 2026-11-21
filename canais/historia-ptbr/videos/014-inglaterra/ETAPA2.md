# ETAPA 2 · historia-ptbr/014 Inglaterra (youtube.videos id 52) · 20–21/11/2026

**Resultado:** `entrega/video.mp4` **16:54** (1013,8 s), 1080p30 H.264 + AAC, **−15,1 LUFS**, pico −4,2 dBFS, **0 telas pretas**, 0 silêncios > 1,5 s, 22 cortes no 1º minuto, 19,7 cortes/min (333 planos). 3 thumbs + `pacote/youtube.txt`. Drive: não subido (a rotina noturna sobe a partir de `entrega/`). `youtube.videos` id 52 = `pronto`. Pares A/B/C gravados em `youtube.embalagem_variantes`.

## Custo (financas.consumo, ref_id 52; teto US$ 8): ≈ US$ 1,39
Runpod US$ 0,91 (17 partes de 1.800 quadros; várias tentativas perdidas por timeout de 570 s do comando durante o upload do bundle nas partes 09, 11 e 13; Pod sempre destruído) · Fish drama-3 US$ 0,15 (70 blocos + 3 tomadas do hook) · pré-QA Anthropic US$ 0,28 · Codex US$ 0 (202 + 8 refeitas + 3 bases de thumb, 0 fallback fal; cota 5 h 44%, semana 35%).

## Voz
Whisper bruto mín 81,2%; **fonético mín 93,6% (N040, "Hampden"), média 99,3%**; nenhuma tag falada; nenhum mp3 de 0 byte. Hook: 4 tomadas, melhor combinação `bbbacb` (repetição 0,05; tomadas únicas 0,14–0,22). Duração 16:54 (< 17:15). Ouvir os nomes antes de publicar (ninguém ouviu): Hampden (N040), Hitchman/Richmond (N001), Rique IV (N028), Oranjo (N045), Montfort, Canuto, Whitehall.

## Imagens: 202, todas pelo Codex
Prancha em 7 grades. Pré-QA apontou Parlamento neogótico/Big Ben, cúpula de St Paul's e ponte de pedra em cenas de 1362, 1399, 1604, 1638, 1640, 1649, 1660 e na cena-guia I141: **I099, I105, I128, I135, I136, I140, I141, I142 refeitas** com "NO Big Ben, NO clock tower, NO neo-Gothic Palace of Westminster, NO domed cathedral, NO stone arch bridge… só Torre de Londres, igreja gótica e casas de madeira" (aplicado em `cenas.json`; originais em `qa/rejeitadas/`; prancha `qa/pranchas/refeitas.jpg`, todas sem anacronismo). Cartões de data movidos no `storyboard.json`: 1805 foi para o plano de Trafalgar (I175) e 1922 para o mapa-múndi (I012). Como editei os JSONs direto, rodar `roteiro.py` de novo desfaz isso. Turbante só em I180/I189 (Índia, permitido).

## Pré-QA (120 stills de 10 s + cartões e capítulos)
Primeira passada: bloqueante 1 (cartão 1805 sobre a cena-estádio), alto 13. Corrigidos os anacronismos e os cartões acima; o "alto" Q06 (I019, 1688, tricórnio e canhão no hook) e Q15 (crossfade de I052) são aceitos (1688 correto; transição). Pré-QA não foi repetido depois das correções (stills refeitos conferidos na prancha).

## Render
Runpod em 17 partes (0–1799 … 28800–30413), todas com quadros = esperado e SSIM aprovada; concat + `mix.wav` AAC 192k. Trilha: alaúde sintetizado + pad em Ré dórico (ajuste do gerador do 013: escala dórica; **não** trocou para cravo/cordas nos caps. 6–10: só notas longas depois do cap. 9, como no 013).

## QA (6b/6c): timestamps conferidos na `legendas.srt`
- Detector de cópia **2/100** (`SIMILARIDADE.md`); `CRIVO-ANGULO.md` APROVADO (r1); `CRIVO.md` APROVADO (r3). Roteiro não mudou na etapa 2 (detector não repetido).
- **Promessa paga:** "o rei da Inglaterra agora é um escocês. O vizinho da guerra de sempre" **0:19–0:25** (T1, Thumb A); pergunta central "como um país que vivia buscando rei lá fora acabou mandando em um quarto do mundo?" **0:27**; "Um dinamarquês e um normando tomaram a coroa à força; o normando, coroado num Natal em que a vizinhança pegava fogo. Um francês, um holandês e um alemão a receberam" **0:36–0:49** (T2/T3, Thumb B); "E cada um pagou um preço… não cobraria um centavo de imposto sem pedir licença" **0:49–0:59** (Thumb C); "Essa é a história inteira da Inglaterra" **0:59**. Natal de 1066 no cap. 2 a partir de **~2:30** (bloco N013); "Segunda peça" **11:15**; "Terceira peça" **14:22**; "perto de um quarto das terras" **~13:50**. Tudo ≤ 1:00, como o EMBALAGEM exige.
- **Thumbs** (`thumbs/compose.py`; bases Codex sem letras, texto no código): A `rosto-emocao` Jaime VI de manta xadrez pondo a coroa, Torre de Londres, "MINHA!" ouro; B `cena-acao` coroação de Natal de 1066 com fogo pela porta, "NATAL DE 1066" em branco no rodapé; C `documento-evidencia` pergaminho com linha circulada, rei de peruca suando, "O PREÇO" vermelho em marcador (≥ 18% da altura). As 3 leem a 320×180 (`thumbs/prancha-celular.jpg`), são 3 padrões diferentes e cada uma é o seu conceito. A = T1, B = T2, C = T3 (títulos sem ajuste de N: a duração só aparece na descrição). Licença visual: Jaime não se coroou (foi Whitgift, 25/07/1603); o roteiro não diz isso.

## Pendências (não bloqueiam)
Ouvir os nomes (acima); estandarte de 1688 ("segundo os relatos", sem texto); Jorge I "com o tempo"; regra 9 (sem fala direta). Thumb B: o rei aparece de cabelo castanho (bonequinho sem barba), aceito.

## Lição (vai para a bíblia visual)
Cenas de interior de Londres medieval/Tudor com janela para o rio puxam Parlamento neogótico, Big Ben e a cúpula de St Paul's mesmo com "strictly London of the time": **o sufixo anti-vazamento deve incluir "NO Big Ben, NO clock tower, NO neo-Gothic Palace of Westminster, NO domed cathedral, NO stone arch bridge" e descrever o skyline da época** em todo prompt com janela/rio antes de 1700.
