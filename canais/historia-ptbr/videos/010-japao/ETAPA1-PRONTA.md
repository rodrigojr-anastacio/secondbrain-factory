# ETAPA 1 PRONTA · historia-ptbr/010 Japão · youtube.videos id 40 · 14/11/2026

Pasta: `canais/historia-ptbr/videos/010-japao/` · `youtube.videos` id **40** (`status='roteiro'`, `biblia_versao='v2'`). Etapa 1 (Opus) concluída: pesquisa, **embalagem aprovada no crivo (r2)**, roteiro v2 com checagem de fatos (checklist APROVADO), storyboard e `cenas.json`. **Nada de voz, imagem ou render foi gerado. Custo pago da etapa 1: US$ 0.**

## Embalagem aprovada (CRIVO.md, rodada 2 de 3)
- **T1 (título A):** "O Japão COPIAVA todo mundo. Por que ninguém o conquistava?" (58 car.; padrão "afirmação estranha + pergunta"; = pergunta central)
- **T2 (título B):** "Como o MAR protegeu o Japão (até o dia em que parou)" (52 car.; padrão "Como [agente] [verbo] [lugar]")
- **3º título (C, variação):** sugestão do crivo: "O Japão COPIAVA todo mundo. Por que ninguém conseguia conquistá-lo?"
- **Thumb (conceito):** 1 bonequinho de cabeça redonda grande (peito para cima, ~60% da altura), à esquerda do centro, em cima de um muro baixo de pedras na praia, à noite, segurando uma tocha e olhando **por cima do ombro** para o mar, rosto em ¾ visível, olhos arregalados e boca aberta (espanto + alívio); quimono escuro, coque simples, **sem** armadura de filme. No alto à direita, o **tufão**: ondas enormes, céu negro-azulado com raio, juncos **pequenos** tombando (não podem virar 2º foco), sem bandeira nem letra. Tocha laranja quente × mar azul frio. Texto no código: "**SÓ SORTE?**" (Libre Caslon 700, "SÓ" ouro #F7C21B + "SORTE?" branco) embaixo à direita sobre degradê escuro + pílula amarela "**1281**" no topo ao centro. Sem sol vermelho, Fuji, castelo, mapa ou nome do país (é o que todo o mosaico faz).
- r1 reprovou só o T2 antigo ("Japão: a ilha que aprendia com todos e não obedecia a ninguém").

## Promessa e onde o roteiro a paga (tempos estimados; conferir na `legendas.srt`)
- **Promessa:** como um país que copiava tudo de fora passou quase setecentos anos sem que nenhum invasor o conquistasse, e o que aconteceu quando a porta cedeu.
- **Hook:** N001–N003 (0:00–0:36) "você" no muro de pedra, 1281, frota de Kublai Khan, tufão, *kamikaze* → N004 (0:36) "Foi só sorte?" + "esse país vivia copiando os vizinhos" → **N005 (0:44) pergunta central** → N006 (0:56) "O mar era o muro do Japão… um dia esse muro vai falhar" + "Essa é a história inteira do Japão" + "Guarde esse vento" → cap. 1 em ~1:09.
- **T2 (o mar):** N006 0:56 · N027 6:38 ("o mar dava tempo") · N036 9:13 ("a distância do mar deixava fazer isso sem castigo") · **N040 10:04 ("Nesse dia, o mar parou de proteger o Japão")** · N055 13:45 ("os americanos chegam pelo mar") · N062 fecho.
- **"Só sorte?" respondido:** N026–N027 (6:23–6:38, Takashima). Peças da resposta: N015 (3:25), N027 (6:38), N036 (9:13). Vento pago: N052 (13:01). Fecho N061–N063 (15:20–16:02): "Sorte foi uma noite. O resto foi escolha."

## Números
| Item | Valor |
|---|---|
| Palavras / blocos | 2.006 / 63 (hook + 10 capítulos + fecho) |
| Duração estimada | ~16:00 (gerador 16:02 a 126 ppm; ritmo real 006–009 → ~15:40–16:10) |
| Checklist v2 | **APROVADO** (pergunta 0:44, volta 6×, conectivos 1,65, "você" 1,40, ponte 10/10, 1 "guarde", cap. 1 em 1:05, fecho 0:40; ritmo só depois da voz) |
| Imagens planejadas | **218** únicas (307 planos; reuso 0% até 3:00, 36,8% depois; 24 cortes no 1º min; 19 rótulos) + bases da thumb |
| Voz | `texto` = 11.350 bytes ≈ US$ 0,57 por passada no drama-3 (US$ 50/M bytes) |

## O que a etapa 2 precisa saber
1. **Código:** `src/` e `tools/` foram copiados do 009 e ainda têm caminhos/ids do 009 (`tools/render_parte.sh`, `render_resto.sh`: `009-alemanha`, `VIDEO=37`; trilha em Lá eólio no `build.py`). Troque para `010-japao` / `VIDEO=40` e escolha a escala da região (sugestão: pentatônica japonesa *in* ou *yo*, timbre de koto/shakuhachi sintetizado; caps. 7–8 com metais/piano ocidental; cap. 9 piano esparso, sem marcha).
2. **Imagens pelo Codex** (`canal.yaml` `gerador: codex`, fallback fal automático), um processo só, `--video 40`. **Lote-prova de 6:** I001 `wall_dusk` (samurais no muro: sem chifres, sem sol vermelho), I006 `kublai_throne` (rosto cartoon), I041 `kofun_aerial` (monte em fechadura, sem prédios), I083 `kyoto_palace` (Heian sem castelo/pagoda chinesa), I133 `dejima_aerial` (ilha em leque, sem bandeira), I153 `black_ships` (4 navios, 2 a vapor, sem bandeira). **Conferir um a um os planos de 1910–1945 (I184–I200)**: nenhum sol nascente, bandeira, insígnia, letra, sangue ou corpo (constante `SEMSIMB`). Outros de risco: Nara/Sui (I062, I072: pagoda só onde pedido), samurais (`SAM12`: sem armadura de filme), Perry (I155), Meiji (I166), Edo (I147: Fuji ao fundo ok, sem prédio ocidental), Tóquio hoje (I212: néon sem letras), estádio de 1964 (I204: sem anéis/logos), `amaterasu` I046 (sem disco solar como símbolo).
3. **Voz:** drama-3, 1 chamada por bloco. Teste de nomes antes (lista `FALA` do `roteiro.py`, grafias NÃO testadas): Kublai Khan → "Cublai Cã", kamikaze → "camicáze", jomon → "djômon", Yamato → "Iamáto", Amaterasu → "Amaterássu", Quioto → "Quióto", Murasaki Shikibu → "Murassáki Xikíbu", Genji → "Guêndji", Hakata → "Rakáta", Takashima → "Takaxíma", Tanegashima → "Taneguaxíma", Oda Nobunaga → "Ôda Nobunága", Tokugawa → "Tokugáua", Matthew Perry → "Méthiu Péri", Meiji → "Mêidji", Yokohama → "Iokorráma", Kasato Maru → "Kassáto Máru", Pearl Harbor → "Pérl Rárbor", Hiroshima → "Iroxíma". Conferir também Sekigahara, Tokugawa Ieyasu (só no rótulo), Nagasaki, Edo, "pan". Troque no `FALA` e rode `python3 roteiro.py` (nunca edite `blocos.json` à mão).
4. **Tom do cap. 9 (N050–N055):** `[serious]` no N050; nenhuma tirada; N051 (Nanquim) e N053 (bombas) sóbrios.
5. **Thumb:** a partir do conceito acima (skill `thumbnail`); A/B do "Testar e comparar" = T1/T2 com a mesma arte; C = variação só de texto ("SORTE?" / "FOI O VENTO?"), expressão ou enquadramento, **nunca outro conceito**. Os 3 estilos da bíblia partem deste conceito.
6. **Pacote:** título A = T1, B = T2, C = variação; duração na descrição (os títulos não têm "em N minutos"); sem palavras proibidas; sem menção a IA; fontes de `SOURCES.md`.
7. **QA:** conferir na `legendas.srt` pergunta ≤ 0:50, "Foi só sorte?" no hook, "copiando" antes de 1:00, "o mar parou de proteger" (cap. 7), e a thumb final contra o conceito.
8. **Teto US$ 8:** voz ~0,6–1,2 (com tomadas e teste de nomes) + Codex US$ 0 (fallback fal US$ 0,046/img se precisar) + render Runpod ~0,2. Folga para ~120 imagens no fallback.
9. **Neutralidade:** fecha no Japão de hoje com 1 frase (população: ~29% com 65+); nada de política atual; sem anúncio de próximo vídeo.

## Pendências
- Grafias de voz e posições dos rótulos (`src/labels.jsx`) não conferidas (dependem de voz/imagens).
- Data de publicação: `youtube.backlog` diz qua 18/11 (confirmado pelo Rodrigo em 14/11, segundo o `motivo`); o brief dizia "em aberto".
