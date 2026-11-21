# ETAPA 1 PRONTA · historia-ptbr/014-inglaterra · 20/11/2026
Vídeo `youtube.videos` id 52 · `CRIVO.md` APROVADO (embalagem, rodada 3) · `CRIVO-ANGULO.md` APROVADO (rodada 1) · pares registrados em `youtube.embalagem_variantes`.

## Ângulo
**A coroa que vem de fora:** seis vezes a coroa inglesa foi para alguém de fora; cada rei de fora chegou precisando dos ingleses e pagou com um pedaço de poder escrito no papel; o papel virou Parlamento, crédito (Banco da Inglaterra, 1694), frota e império. Detector de cópia: **2/100** (`SIMILARIDADE.md`). Crivo de ângulo: **aprovado na r1** (80% → 85% de cenas próprias depois da troca recomendada no cap. 6).

## Os 3 pares aprovados (crivo r3; r1 reprovou Thumbs A e B + obrigações; r2 reprovou a Thumb A)
| par | título | padrão do título | thumb (padrão) | texto da thumb |
|---|---|---|---|---|
| A | "A Inglaterra IMPORTAVA reis. Como mandou em 1/4 do mundo?" (57) | afirmação estranha + pergunta | `rosto-emocao` (controle): Jaime VI bonequinho, barba ruiva curta, **manta xadrez** vermelha e verde no ombro, **sem chapéu**, pondo a coroa inglesa na própria cabeça, sorriso malicioso e sobrancelha erguida, close ≥ 60% da altura; fundo diurno com a Torre de Londres (Tâmisa discreto); ninguém mais | "MINHA!" (ouro, contorno escuro grosso) |
| B | "Como reis de FORA deixaram a Inglaterra mais forte" (50) | Como [agente concreto] [verbo] [lugar] | `cena-acao`: coroação de Natal de 1066 na abadia românica; Guilherme grande no trono, mãos de um bispo baixando a coroa, ele vira a cabeça assustado para a porta por onde entra luz laranja de fogo e fumaça; sem sangue | "NATAL DE 1066" (rótulo branco, rodapé esquerdo) |
| C | "Inglaterra, o país que dava a COROA a estrangeiros" (50) | O país que + fato estranho | `documento-evidencia`: pergaminho comprido (Declaração de Direitos, 1689) em diagonal sobre mesa escura, linhas ilegíveis, uma linha circulada em vermelho com seta; rei pequeno de peruca escura com a pena, suando; coroa pequena na ponta | "O PREÇO" (marcador vermelho grosso, ≥ 18% da altura) |
A = T1, B = T2, C = T3. Prompts, composição e referências em `EMBALAGEM.md` (Thumbs A/B/C). Ressalva do crivo r3: Jaime **não** se coroou sozinho (foi o arcebispo Whitgift, 25/07/1603): licença só na thumb; o roteiro não diz isso.

## Promessa e onde o roteiro a paga
Promessa: como a Inglaterra entregou a coroa a gente de fora seis vezes, e como o preço cobrado de cada rei estrangeiro virou a força que mandou em um quarto do mundo.
- **~0:12–0:26 (N002):** frase-âncora "o rei da Inglaterra agora é um escocês. O vizinho da guerra de sempre." (T1, Thumb A)
- **~0:26 (N003):** pergunta central "Como um país que vivia buscando rei lá fora acabou mandando em um quarto do mundo?"
- **~0:37–0:54 (N004):** "Um dinamarquês e um normando tomaram a coroa à força; o normando, coroado num Natal em que a vizinhança pegava fogo. Um francês, um holandês e um alemão a receberam." (T2/T3, Thumb B)
- **~0:54–1:05 (N005):** "E cada um pagou um preço. Um deles teve de aceitar, por escrito, que não cobraria um centavo de imposto sem pedir licença." (Thumb C)
- **Cap. 2 (~2:37–3:59, N013–N015):** a coroação de Natal com o fogo (Thumb B).
- **Cap. 3 (~4:37–5:31, N022–N024):** 1º preço (Magna Carta; Montfort chama as cidades) + "primeira peça da resposta".
- **Cap. 6 (~8:25, N038–N039):** o escocês em Londres; os Comuns recusam "Grã-Bretanha".
- **Cap. 7 (~10:12–11:58, N044–N049):** estandarte de 1688; a Declaração lida antes da coroa (Thumb C); Banco da Inglaterra; "segunda peça".
- **Cap. 9 (~14:21, N058):** "perto de um quarto das terras do mundo" (T1); "terceira peça" em N061.
- **Fecho (~16:56, N068–N070):** a resposta (papel → crédito → frota → império) + reenquadra ("o rei já não era quem mandava").
Tempos estimados a 2,1 palavras/s (o real deve sair ~4% mais curto); o QA confere na `legendas.srt`.

## O que a etapa 2 precisa saber
- **Roteiro:** 70 blocos, 2.212 palavras, ~17:00 reais (ritmo dos 011–013, ~130 ppm). Se a voz passar de 17:15, avise no ETAPA2 (não corte texto sem rodar o checklist). Voz Fish drama-3 (`canal.yaml`), 1 chamada por bloco; grafias para a voz em `FALA` do `roteiro.py` (Róbert Kéri, Rítchmond, Canúto, scái/égue/náife, Uéstminster, Hêistings, Le Mã, Simón de Monfór, Calê, Lâncaster, Iórque, Túdor, Orânge, Uólpol, Bulônhe, Trafalgár, Uíndsor, Uóchinton, Djón Rêmpden, Bâkinghamxer); conferir também Edimburgo, Ruão, Hanôver, Brittany/Bretanha, Whitehall (não falado), Elizabeth.
- **Storyboard:** 333 planos, **202 imagens** (`cenas.json`), reuso 39% (49% depois de 3:00), 0 avisos, 28 rótulos `@@` + cartões de data no código. Codex (`img_codex.py`) com fallback fal; teto US$ 8 → não deixar o lote inteiro cair no fal (202 × 0,046 ≈ US$ 9,3). Todos os prompts levam âncora de cenário + `NAO_EG` (anti-vazamento das refs do Egito), `SEMTXT`; documentos com `PAPEL` (linhas ilegíveis); `SEMBAND` (sem bandeiras/brasões). Conferir na prancha: abadia de 1066 **românica** (sem agulhas góticas); Westminster de 2023 gótica; nada de Tower Bridge/Big Ben antes do séc. XIX; turbante só nas 2 cenas da Índia (I180/I189, permitido).
- **3 thumbs, uma por conceito** (A, B, C acima), nunca 3 variações; texto no código. Thumb A: Tâmisa discreto (não lembrar o rio do 007-1).
- Trilha: sugestão Ré dórico com alaúde/flauta doce sintetizados (caps. 1–5) → cravo (caps. 6–8) → cordas/metais suaves (caps. 9–10).
- Sensíveis: execução de Carlos I (1649) só com a Banqueting House e o cadafalso vazio; fomes da Índia/Irlanda com objetos (cestos/tigelas vazias) e multidão com dignidade; batalhas sem combate em cena.

## Pendências (não bloqueiam)
- Estandarte de 1688: texto exato não confirmado ("segundo os relatos"; imagem sem letras).
- Jorge I fora do gabinete: data incerta ("com o tempo").
- Regra 9 (falas em discurso direto): só aviso.
