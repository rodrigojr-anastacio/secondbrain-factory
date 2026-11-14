# Gap: História em minutos (historia-ptbr) × referências (14/11/2026)

Pergunta do Rodrigo: "nossos vídeos não vão para frente e os deles vão. Onde está o gap?"
Base: `pesquisa/benchmark-2026-11-14/` (90 d das referências), banco `vida` (só leitura: analytics até 11/11, Studio até 08/11, Reporting de 10/11, tráfego detalhado lido hoje), YouTube Data API (9 unidades: `videos.list` e `channels.list` dos nossos), 2 hooks transcritos hoje, mosaicos em `mosaicos/`.
**[O]** observado · **[I]** inferido · **Hipótese** = amostra pequena ou sem dado direto. Custo: US$ 0.

## Os 3 gaps mais prováveis (por impacto)
1. **Tema escolhido pela demanda em inglês, não pela demanda em pt, e chegando 2–4 semanas depois de quem já fez em pt.** Em pt, no mesmo molde: Egito 2,7 mil, Índia 4,1 mil, Japão 2,3 mil (clone 08/2026); os hits em pt são Rússia 254 mil, França 188 mil, Ucrânia 25 mil, 1ª Guerra 237 mil, 2ª Guerra 107 mil e Roma 73 mil. Nossos 5 primeiros (Egito, Índia, Irã, China, Brasil) vieram do HiM/Genius em inglês. Os 4 provados em pt (Rússia, França, Roma, Brasil) saíram 13–25 dias depois do vídeo pt que pegou. [O] demanda · [I] efeito do atraso.
2. **A embalagem é cópia literal de 10+ canais pt, então o YouTube não tem por que preferir a nossa.** O título do Brasil é **idêntico** ao do História Inteira ("A História INTEIRA do Brasil em 17 Minutos"); o de Roma é o do HEG com outro N. O nome do canal, "História em minutos", é **o mesmo** do clone 08/2026 (5,6 mil inscritos) e de mais 5 canais. Nosso canal está **sem descrição** e sem palavras-chave. As thumbs alternam 4 estilos em 7 vídeos. [O] fatos · Hipótese quanto ao efeito.
3. **O YouTube faz um teste minúsculo e não amplia.** São ~100–900 impressões por vídeo. Quando mostra, o CTR é bom (Egito: 776 impressões e **7,1%** em 10/11). O sugerido vem de 2 canais pt pequenos (HEG e História Inteira), não do aglomerado grande (Genius e o clone pt da Rússia/França). Sem um vídeo nosso colado num vídeo pt que esteja subindo **agora**, ninguém amplia. [O] números · [I] mecanismo.

**Ajuste nº 1:** escolher o tema pelo vídeo **em pt** que está subindo **nesta semana** (≥ 2 mil views/dia, ≤ 7 dias no ar, no HEG, no clone 08/2026 ou no História Inteira), publicar em **≤ 5 dias** e não usar o título literal deles (usar o braço B de tensão como principal). Já dá para aplicar: o HEG publicou "Revolução Francesa" (14/11) e "Napoleão" (11/11), e a nossa França sai em 15/11. O título B da França deve puxar a Revolução e o rei (ver §2).

---

## 1. Assunto
| Nosso | Saiu | Mesmo tema em pt (antes de nós) | Mesmo tema em en |
|---|---|---|---|
| Egito 380 | 03/11 | clone 08 2,7 mil (13/10); HEG 5,2 mil (10/11, depois) | HiM 571 mil |
| Índia 251 | 03/11 | clone 08 4,1 mil (09/10) | HiM 641 mil |
| Irã 23 | 06/11 | nenhum | HiM 91 mil |
| China 148 | 08/11 | clone 10c 73 | Genius 553 mil |
| Brasil 53 | 09/11 | HEG 22 mil (27/10); História Inteira 896 (31/10) | — |
| Roma 2 (3 d) | 11/11 | HEG **73 mil** (27/10) | Genius 397 mil |
| Rússia 17 (1 d) | 13/11 | clone 08 **254 mil** (19/10) | Genius 3 mil (12/11); HiM 44 mil |
| França | 15/11 | clone 08 **188 mil** (23/10); HEG Rev. Francesa (14/11) | — |
| Alemanha | 16/11 | HEG 2ª Guerra 107 mil (02/11) | Genius 271 mil (26/10) |

- **[O]** Em pt, as civilizações antigas e a Ásia flopam no molde (Egito, Índia, Japão, Austrália: 2–4 mil). O que roda é potência europeia ou moderna com gancho no presente (Rússia, França, Ucrânia) e as guerras mundiais. Pela busca, Roma tem a maior demanda pt (mediana top-10 de 544 mil; `pesquisa/proximos-temas-2026-11/`).
- **[I]** Quando chegamos 2–4 semanas depois, o público pt do tema já assistiu a um vídeo de 37 min ou de 12 min com 70–250 mil views. Nosso vídeo vira "mais um igual", não o próximo vídeo natural.
- **Anomalia [O]:** Roma tem **2 views em 3 dias**, abaixo até do Irã (23) e da Rússia em 1 dia (17). Não é "feito para crianças" nem restrição (conferido na API: `madeForKids` falso, público, sem bloqueio de região). **Pedir ao Rodrigo as impressões de Roma no Studio** (Alcance): se estiver perto de 0, a suspeita é duplicata do título do HEG (Hipótese).
- **Ajuste:** seguir o mapa de demanda **pt**. A prova em en sozinha não basta (Egito e Índia: 570–640 mil em en e 3–4 mil em pt).

## 2. Título
| Tema | Nosso (no ar) | Deles | Views |
|---|---|---|---|
| Brasil | A história INTEIRA do Brasil em 17 minutos | História Inteira: "A História INTEIRA do Brasil em 17 Minutos" | 896 (**idêntico**) |
| Roma | A história INTEIRA de Roma em 17 minutos | HEG: "A HISTÓRIA INTEIRA de Roma em 12 minutos" | 73 mil |
| Rússia | A história INTEIRA da Rússia em 17 minutos | clone: "Toda a história da Rússia em 37 minutos" | 254 mil |
| França | A história INTEIRA da França em 15 minutos | clone: "Toda a história da França em 38 minutos" | 188 mil |
| Egito | A história INTEIRA do Egito em 17 minutos | HiM: "The ENTIRE History of Egypt in 17 Minutes" | 571 mil |
| Irã | A história COMPLETA do Irã (Pérsia) em 18 minutos | HiM: "Persia Never Died. It Just Changed Its Name." | 91 mil |
| China | A história INTEIRA da China em 16 minutos | HiM: "How Water Decided Who Ruled China for 4,000 Years" | 58 mil |

- **[O]** Os hits em pt usam a fórmula pura, igual à nossa (41–43 caracteres, "em N minutos"). Então o formato do título **não** é o gap. O gap é ele ser **indistinguível**: na aba de sugeridos do Egito aparecem 8 títulos "A história INTEIRA/COMPLETA/TODA de X" de 6 canais pt diferentes, além dos nossos.
- **[O] Inconsistências:** a Índia usa "COMPLETA" e o Irã está no ar como "COMPLETA … (Pérsia)" (no banco, "INTEIRA"). Os 4 primeiros vídeos têm o idioma dos metadados como **pt-PT** (o áudio é pt-BR).
- **[O] Política:** o título B da França ("Por que a França **matou** o rei…") usa uma palavra que `politicas-youtube.md` manda trocar ("matou" → "derrubou/levou").
- **Ajuste: 3 títulos reescritos** (≤ 60 caracteres, sem as palavras proibidas, padrões de tensão da `titulo.md`; o "A história INTEIRA de X em N minutos" fica como braço A):
  1. França (sai 15/11, braço B): **"Por que a França derrubou o rei e nunca viveu sem um?"**, que puxa o aglomerado Revolução/Napoleão do HEG.
  2. Estados Unidos (tema novo): **"Como 13 colônias viraram a maior potência do mundo?"**
  3. Portugal (tema novo): **"Como um país minúsculo dividiu o mundo ao meio?"** (Tordesilhas, 1494)
  - Extra para a Alemanha (16/11): **"Perdeu 2 guerras e virou a maior economia da Europa. Como?"** (57 caracteres).

## 3. Thumb (`mosaicos/mosaico-historia-ptbr.jpg` e `-celular.jpg`)
Comparação [O] (linhas amarelas = nossas, azuis = deles, mesmo tema na mesma coluna):
| | Nossas | Hits deles em pt (clone Rússia/França, HEG Roma) |
|---|---|---|
| Personagem | bonequinho branco de cabeça redonda, em geral ≤ 35% da altura (exceção: Irã) | **rosto humano grande** (Putin, Macron) ou bonequinho de louros, 50–80% da altura |
| Cor/luz | céu azul-claro, dia, pastel (6 de 9) | **escuro e quente**: fogo, fumaça, pôr do sol, vermelho e laranja |
| O que promete | "passado ilustrado, didático" | **crise e presente** (cidade pegando fogo + líder de hoje = "como chegamos aqui") |
| Palavras | 1–2 + datas (ok) | 1 nome + datas (ou "A HISTÓRIA INTEIRA") |
| A 320×180 | o nome do país lê bem; nas "Bonecos" (Roma, Rússia), os personagens viram manchas brancas e a frase em 2 linhas fica pequena | nome e rosto leem; o fogo destaca no feed |
| Consistência | 4 famílias em 7 vídeos (panorama, Gandhi recortado, conflito ×, cena de bonecos) | Genius e clone: **100% o mesmo molde**, hit e flop iguais |

- **[O]** As nossas versões "pegada HiM" (Egito, China, Brasil, França, Alemanha) são quase cópias das deles. No feed pt, a diferença entre as duas é só a luz (a nossa é mais clara e mais infantil).
- **[I]** O CTR quando a thumb aparece (4–7%) mostra que ela não espanta ninguém. O problema é que ela não **destaca** nem cria identidade (decisão do clique: "excesso de informação" com 10 thumbs iguais).
- **Brief de thumb (próximo vídeo; exemplo: Estados Unidos, estilo 2 "pegada HiM" escurecida). Hipótese, medir no "Testar e comparar":** bonequinho de cabeça redonda **grande** (do peito para cima, ~55% da altura, à esquerda, contorno de adesivo) com expressão tensa, olhando para a câmera, com casaca e chapéu de época (Washington); ao fundo, o Capitólio e Nova York **ao entardecer, com fumaça e brasas** (paleta laranja/vermelho/azul-noite, sem cadáver nem sangue); "EUA" em serifa gigante **branca com contorno escuro** no canto superior direito + "1776 – 2026" em pílula amarela. Nenhuma outra palavra. Braço de controle: a mesma composição de dia (a atual). **Manter o mesmo molde em 2 das 3 thumbs** de todo vídeo para criar consistência.

## 4. Hook (primeiros 60 s)
| Vídeo | Abre com | Promessa/pergunta | Palavras/60 s | Concretude |
|---|---|---|---|---|
| Clone pt Rússia (254 mil) | "Põe o dedo num mapa…", **você** atravessa 2 mil km de planície | contradição aos 0:49: "deveria se sentir seguro… mas" | 170 | alta (mapa, Minsk, Volga, 11 fusos) |
| HEG 1ª Guerra (237 mil) | data + cena: motorista erra o caminho, 2 tiros | "Essa é a história inteira" aos 0:37 + paradoxo ("não resolveu nada") | 138 | alta |
| HiM Egito (571 mil) | "olhe o Egito do céu à noite" (transcrição ruim, `ref-him-egito`) | rio × país, ~0:25 | ~215 | alta |
| Nós Egito (380) | "não é um país que tem um rio" (= HiM) | pergunta aos **0:32** | 148 | alta |
| Nós Índia (251) | Índia vista do espaço em maio × setembro | "Essa é…" só aos 2:21 (v1) | 162 | alta |
| Nós China (148) | 210 a.C., Qin e o elixir | "Essa é a história inteira" aos 0:42 | 128 | alta |
| Nós Rússia (17) | "**Oitocentos e sessenta e dois.**" | pergunta dupla e longa, de 0:41 a 0:56 | 135 | média (abre com data seca) |

- **Retenção [O]:** o Egito tem 79% aos ~31 s, 64% aos 1:42 e 50% em 30% do vídeo; a Índia, 74%, 55% e 43%. A média do canal é de 42% (7,5 min por view), na faixa de canal saudável (Hipótese). **O hook não é o gap principal.** As curvas dos v2 (Roma, Rússia) ainda não têm amostra.
- **[I]** Os hooks dos hits em pt põem o espectador **no mapa e no presente** antes do passado (o clone liga a planície à insegurança de hoje). Os nossos v2 abrem numa data distante.
- **Ajuste (reescrita sugerida, EUA):** "Pegue um mapa de 1776: treze colônias espremidas no litoral, sem exército de verdade, devendo até a pólvora. Hoje, esse país gasta com defesa mais que os nove seguintes juntos. Como?" (conferir o número no SIPRI antes do roteiro). Regra: **a 1ª frase é uma imagem que o espectador vê (mapa, céu, você) e conecta com hoje**; a data vem depois.

## 5. Duração e formato
- **[O]** Hits com 12, 13, 17, 20, 21, 37 e 38 min. O clone pt faz 30–38 min, o HEG 10–21 e o Genius 12–23; os nossos têm 15–19. **Duração não é gap**: manter os 15–17 da bíblia.
- **[O]** O HEG soma 14 Shorts em 17 d; nós, 0. **Hipótese:** Short do hook ("Cleópatra viveu mais perto do iPhone…") como porta de entrada. Fica para avaliar, não é prioridade.

## 6. Canal e consistência
- **[O]** Nome "História em minutos" e handle `@historiaem-min`: há o clone 08/2026 com o **mesmo nome** (5,6 mil inscritos, dono dos hits pt), "A HISTORIA EM MINUTOS" (32 mil) e ≥ 5 clones "História em Minutos" de 10/2026. Nosso termo de busca nº 1 é "história em minutos" (15 views): provavelmente gente procurando o clone.
- **[O]** O canal foi criado em 2023, está **sem descrição** e sem palavras-chave, tem 14 inscritos e 7 longos em 11 dias (~4,5 por semana, mais que o clone, com 2,25, e que o Genius, com 1,5).
- **[O]** Os horários variam de 09:00 a 20:42. O Genius publica sempre às 09:30.
- **Ajuste:** preencher a descrição do canal com o tema (história inteira de países e impérios, em pt-BR, toda semana) e as palavras-chave; corrigir o idioma dos metadados para pt-BR nos 4 primeiros vídeos; fixar um horário. **Hipótese:** um nome/handle distinguível (decisão do Rodrigo; mudar nome tem custo de reconhecimento quase nulo com 14 inscritos).

## 7. Tráfego
- **[O]** Página inicial/feed 47% (rótulo SUBSCRIBER na API), sugeridos 44%, busca 4%. Termos de busca irrelevantes ("chaves 1979", "jovem pan").
- **[O]** Quem nos sugere: **HEG Brasil 252 views** (relatório de 14/11; na leitura de hoje, 96 delas no Egito, não no Brasil), HEG Roma 64, História Inteira Brasil 58. Depois vêm os nossos próprios vídeos (Egito → Brasil 8, Egito → China 3). Do Genius: **0**; do clone 08/2026: 4 (o Egito dele).
- **[I]** Estamos no "satélite" do HEG e do História Inteira (canais de 3 mil e 42 inscritos), não no aglomerado que gera os 250 mil. O sugerido nos acha por **título igual**, não por tema igual (o Egito foi sugerido por um vídeo do Brasil).
- **[O]** Impressões: Egito 920 e Índia 1.273 (Studio até 08/11); o canal inteiro teve 1.124 em 10/11, com CTR de 6,3%. O teto é de impressões, não de clique.

## O que NÃO é gap (manter)
- **CTR** (4–7%) e **retenção** (42%; Egito 79% aos 30 s): a embalagem e o vídeo funcionam quando aparecem.
- **Ritmo** (~4,5 por semana): já é maior que o dos canais que deram certo.
- **Duração** de 15–17 min e **narrativa contínua v2**: os hits têm 12–38 min. O roteiro v2 passa no checklist (Roma 13/14, Rússia 13/14).
- **A fórmula A** do título: os hits pt a usam. Ela fica como braço A, sem ser o único.
- **Bonequinhos de cabeça redonda**: o HEG, com o mesmo estilo, fez 237 mil. Não é o traço que trava.

## 5 temas para o backlog (demanda medida)
| Tema | Evidência [O] | Risco | Nota |
|---|---|---|---|
| **Estados Unidos** | Genius 541 mil (09/10); pt "Legados da História em 11 min" 96,7 mil; Cronista de Bolso já nos sugere | baixo | sessão com o Brasil |
| **União Soviética** | Archive en 227 mil (17/10); Te lo Pinto (es) "¿Sobrevivirías en la URSS?" 258 mil; **ninguém no molde pt** | médio (política; fechar em 1991) | sessão com Rússia e Alemanha; é Estado, não organização |
| **Portugal** | mediana pt 12 m 159 mil; Sociedade Épica 25,7 mil; o HEG Brasil já nos manda tráfego | baixo | sessão com o Brasil |
| **Grécia** | mediana pt 12 m 82 mil; HnM Macedônia 98 mil; HEG Esparta 6,7 mil | baixo | sessão com Roma, Egito e Irã |
| **1ª Guerra Mundial** (fora da bíblia: **só com OK do Rodrigo**) | HEG 237 mil (pt, 28/10), 2ª Guerra 107 mil | médio (guerra; sem as palavras proibidas) | maior prova pt do molde |
Evitar: Japão (flop em 3 canais), Austrália em pt, Ucrânia e Israel (guerra atual; regra do backlog).

## Mosaicos
- `mosaicos/mosaico-historia-ptbr.jpg`: as 9 nossas (amarelo) sobre as 9 deles no mesmo tema (azul). Os hits pt são escuros e quentes, com rosto grande; as nossas são claras, com bonequinho pequeno, e as "pegada HiM" quase copiam as deles.
- `mosaicos/mosaico-historia-ptbr-celular.jpg`: o mesmo a 320×180. O nome do país lê nas duas; nas nossas "Bonecos" (Roma, Rússia), os personagens viram manchas brancas e a frase de 2 linhas fica pequena.

Arquivos: transcrições `dados/historia-ptbr/ref-clonept-russia-aMld6kMmcm4.txt`, `ref-heg-1guerra-IdvlTEQ72r8.txt` (+ HiM Egito já existente); thumbs em `dados/historia-ptbr/thumbs/`; script `scripts/historia-ptbr-mosaico.py`.
