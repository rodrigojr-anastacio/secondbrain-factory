# ETAPA 1 PRONTA · historia-ptbr/013-uniao-sovietica · 18/11/2026
Vídeo `youtube.videos` id 50 · `CRIVO.md` APROVADO (embalagem, rodada 3) · `CRIVO-ANGULO.md` APROVADO (rodada 3) · pares registrados em `youtube.embalagem_variantes`.

## Ângulo
**A prateleira e o Plano:** a prateleira era sempre o próximo plano; quando virava urgência, ou a pressa comia a semente, ou alguém de fora enchia (Hoover 1921 → Canadá 1963 → EUA 1972/1975 → reserva de Berlim 1990). Detector de cópia: **2/100** (`SIMILARIDADE.md`). Crivo de ângulo: **aprovado na r3** (r1 reprovou a tese, igual à do vídeo es `q3iSdrIQy_4`; r2 reprovou os elos no petróleo; reescritos).

## Os 3 pares aprovados (crivo r3; r1 reprovou Thumb C + obrigações, r2 reprovou Thumb C)
| par | título | padrão do título | thumb (padrão) | texto da thumb |
|---|---|---|---|---|
| A | "A URSS chegou ao ESPAÇO. Por que faltava comida?" (48) | afirmação estranha + pergunta | `rosto-emocao`: Iéltsin bonequinho (cabelo branco penteado para trás, terno cinza, gravata vermelha) pasmo, mãos no rosto, num corredor de supermercado americano de 1989 transbordando de produtos sem marca; terço superior direito mais simples | “NEM O POLITBURO” (citação) + pílula "1989" |
| B | "Como o PÃO explica a União Soviética inteira" (44) | Como [coisa concreta] [verbo] [lugar] | `objeto-simbolo`: avoska (sacola de rede, cordão creme grosso) vazia, enorme, em 1º plano no terço direito, diante de prateleiras de madeira vazias sob luz fluorescente esverdeada; sem personagem | "VAI QUE…" à esquerda, com contorno |
| C | "URSS: o país que pôs o 1º homem no espaço e COMPRAVA trigo" (58) | O país que + fato estranho | `numero-estatistica`: "30 MIL" gigante em ouro + "NA FILA" em branco à esquerda; à direita, noite de neve em Moscou com uma fila de bonequinhos em diagonal (tamanho médio, legível) até uma porta de loja iluminada | "30 MIL / NA FILA" |
A = T1, B = T2, C = T3. Prompts, composição e referências em `EMBALAGEM.md` (Thumbs A/B/C).

## Promessa e onde o roteiro a paga
Promessa: por que o país que chegou primeiro ao espaço passou setenta anos sem conseguir encher a prateleira, da promessa de pão de 1917 à fila de 1990, plano por plano.
- **~0:10–0:25 (N002):** frase-âncora "De manhã, o controle de missão da NASA… À tarde, um supermercado. E ele diz: nem o Politburo tem essa escolha." (T1, Thumb A)
- **~0:25–0:41 (N003):** ~30 mil pessoas na fila de uma lanchonete americana em Moscou num só dia (Thumb C) + "o país do Sputnik comprava trigo do exterior desde sessenta e três" (T3).
- **~0:41 (N004):** pergunta central "Como o país que chegou primeiro ao espaço não conseguia encher uma prateleira?"
- **~0:49 (N005) e cap. 1 (0:57–2:23):** "começa com uma promessa de pão" → paz, terra e pão, requisição, fome do Volga e a sopa de Hoover (T2). Pão/grão em todo capítulo.
- **~5:00 (N024):** a avoska, "vai que" (Thumb B); volta em N051, N067 e no fecho.
- **~9:06–9:58 (N042–N046):** Gagarin + 1ª compra de trigo do Canadá em 1963 (T3).
- **~13:18 (N059) e 13:46 (N061):** volta de Houston; Praça Púchkin, 31/01/1990 (Thumb C de novo).
- **Fecho ~15:56 (N070–N072):** a resposta (as 3 peças) + "quem decide o que vai na sua sacola" + Praça Púchkin em 2022.
Tempos estimados a 2,1 palavras/s; o QA confere na `legendas.srt`.

## O que a etapa 2 precisa saber
- **Roteiro:** 72 blocos, ~2.040 palavras, ~16:20 estimados (alvo ≤ 17:00; o título não leva "em N minutos"). Voz Fish drama-3 (`canal.yaml`), 1 chamada por bloco; grafias para a voz em `FALA` do `roteiro.py` (Khruchóv, Kossíguin, Gorbatchóv, Novotcherkásk, Riazã, Larionóv, Gósplan, avóska, Hérbert Húver); conferir pronúncia de Iéltsin, Púchkin, Liberman, Kharkov, Pravda, Volga, Urais, Leningrado.
- **Storyboard:** 315 planos, **199 imagens** (`cenas.json`), reuso 46% depois de 3:00, 0 avisos, 17 rótulos `@@` + cartões de data no código. Codex (`img_codex.py`) com fallback fal; teto US$ 8 → não deixar o lote inteiro cair no fal (199 × 0,046 ≈ US$ 9,2). Prompts levam `URSS`/`EUA89` (anti-vazamento das refs do Egito), `SEMTXT`, `SEMBAND` (sem bandeira, foice e martelo, estrela vermelha), `GUERRA`, `COMIDA` (embalagens sem marca). Conferir a prancha inteira antes do pré-QA: Kremlin sem estrelas vermelhas; tanques sem estrela; o cartaz "2 + 2 = 5" (I0xx `poster_225`) é a única imagem com caracteres pedidos (se o Codex errar, compor o "2 + 2 = 5" no código sobre um cartaz em branco).
- **Marca:** a lanchonete de 1990/2022 **sem logotipo, sem arcos dourados, sem "McDonald's" escrito** (nem na imagem nem no `youtube.txt`: lá, "lanchonete americana"/"McDonald's" só se o pacote julgar necessário na descrição factual).
- **3 thumbs, uma por conceito** (A, B, C acima), nunca 3 variações; texto, número e pílula no código. Observações do crivo r3: na maquete 320×180, testar "30 MIL" × "30.000" (manter ≤ 3 palavras); B é o 3º objeto-símbolo seguido no canal (acompanhar no placar).
- Trilha: escala sugerida Ré menor natural/eólio com timbre de balalaica/acordeão sintetizado (caps. 1–4) e sintetizador frio anos 80 (caps. 8–10).
- Fomes (1921, 1932–33, 1946–47) e Novocherkassk: sem corpo, sem sangue, sem tiro em cena (prompts já pedem praça vazia, cozinha vazia, tigelas vazias).

## Pendências (não bloqueiam)
- N002 "À tarde": ordem dos relatos (JSC e depois Randalls); horário exato não está na fonte.
- N059: citação do assessor Sukhanov é de segunda mão.
- N066 (02/04/1991) e N069 (02/01/1992): conferir no QA.
