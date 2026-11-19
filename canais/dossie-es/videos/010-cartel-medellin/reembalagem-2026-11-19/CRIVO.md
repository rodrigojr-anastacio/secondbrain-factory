# Crivo reembalagem dossie-es/010 · rodada 3 · 19/11/2026

Revisor novo (não li crivo/, crivo-r*.md antigos nem o CRIVO.md anterior). Régua: `skills/embalagem/CRIVO.md` (itens 0–8, por par) + `pesquisa/embalagem-padrao-ouro-2026-11/RUBRICA.md` (Par A) + `PADRAO-OURO.md`.

**Conferido:**
- `videos.list` (8 ids, 19/11/2026): HXh7hScrcY8 45.471 · 22/01/2026 · Reino Criminal; 3Ph2nDSHqww 563.917 · 10/09/2025 · Relato Mafioso; dPb-LPhtjDA 284.238 · 25/07/2026 · Relato Mafioso; ytn6MrDjhkw 61.065 · 11/11/2026 · Mafia Files; zfpkt1vYtOA 1.259.595 · 16/05/2026 · Our History; bSOi7FEjcyw 3.400.229 · 17/11/2024 · Mighty Monk; 4lgYd6q6OcA 324.051 · 16/08/2026 · Fugitivos de la Ley; FEIWbZZL7CI 1.623.087 · 09/10/2026 · Nat Geo en Español. Todos batem com a proposta (diferença < 0,1%).
- Medianas: os 3 json + recálculo próprio (playlistItems + videos.list, 30 longos ≥ 180 s): Relato Mafioso 36.407 (igual), Fugitivos de la Ley 51.791 (json 51.754, ok).
- Colisão: 2 buscas yt-dlp via WARP ("el papel que pablo escobar quería destruir", "pablo escobar tratado 1979 extradición"): nenhum título com "papel" + Escobar; só a nossa própria entrada (XYhZGpBGjQ0, "Cómo el Cártel de Medellín tomó de rehén a todo un país", 45 views). Estrutura no `refs.csv`: 12 títulos "El/La [X] que (Pablo) Escobar [verbo]" no tema.
- Caracteres (python): A 50 · B 41 · C 42.
- Fato do título: SOURCES.md linha 9 ("Tratado assinado em Washington em 14/09/1979 (governo Turbay)", ColombiaCheck, Semana, El Espectador) e SCRIPT.md N007. Confere.
- Pagamento: `out/legendas.srt` (timestamps abaixo) e SCRIPT.md.
- Imagens olhadas com Read: grade-tema-no-ar-160, grade-tema-A3-160/-320, maquetes/A3-maquete.jpg, grade-tema-B2-320, grade-tema-C-320, rosto-ilustrado-320, e as 3 thumbs de referência do padrão de thumb do Par A lado a lado (thumbs/zfpkt1vYtOA, bSOi7FEjcyw, 4lgYd6q6OcA).
- Bíblia (README, titulo.md, thumb.md), canal.yaml, identidade.md, `conhecimento/politicas-youtube.md`, `conhecimento/titulos.md`.

## Par A: REPROVADO (rubrica 74/100, 1 ponto abaixo do corte) — "El papel de 1979 que Pablo Escobar quería destruir" + Thumb A (padrão `rosto-emocao`)

**0 Assunto em < 1 s: ok.** O rosto de Escobar (cabelo crespo + bigode) se reconhece na maquete mesmo a 160×90, e "Pablo Escobar" está nas palavras 6–7 de um título de 50 caracteres.

**1 Evidência: título ok · thumb ok com ressalva.**
- Título ("El/La [X] que Pablo Escobar [verbo]"): Reino Criminal 45.471 ÷ 1.092 = 41,6× (22/01/2026) e Relato Mafioso "La Muerte que…" 284.238 ÷ 36.407 = 7,8× (25/07/2026). As duas estão dentro de 400 dias e acima da mediana. O 3Ph2nDSHqww tem 435 dias (fora da janela) e o ytn6MrDjhkw é apoio em inglês. **Contra-evidência que a proposta não mostrou:** o maior canal da estrutura no tema, Mafia e Historia, fica abaixo da mediana com ela: "El NARCO que tenía MÁS DINERO que Pablo Escobar" 0,7×, "El ÚNICO hombre al que Pablo Escobar RESPETABA" 0,4×, "El NARCO al que Pablo Escobar llamaba PATRÓN" 0,1×. A estrutura não garante nada sozinha.
- Thumb: **a proposta descreve errado 2 das 3 referências.** Mighty Monk (bSOi7FEjcyw) é colagem de **fotos** P&B com Escobar segurando uma **arma** e dinheiro queimando: não é ilustração nem rosto único. Na Fugitivos de la Ley (4lgYd6q6OcA), o rosto dominante é **outro homem**; Escobar aparece pequeno, ao fundo em vermelho ("¿PEOR QUE ESCOBAR?"). Só a Our History (zfpkt1vYtOA, 1.259.595 ÷ 43.244 = 29,1×) tem o rosto de Escobar dominante em acabamento pintado. O padrão declarado (`rosto-emocao`, rosto de Escobar dominante) passa com a 2ª referência que eu medi: Nat Geo en Español FEIWbZZL7CI, 1.623.087 · 09/10/2026 · 7,1×, rosto dominante (foto). O apoio do traço ilustrado no molde é o Archive CIA/KGB (bíblia `thumb.md` H1). Passa, mas o "ilustrado" tem só 1 referência real no tema.

**2 Promessa paga: ok.**
- 0:20–0:24 "se firmó el tratado que sus captores querían destruir": é a frase do título, mas dita sobre os captores, não sobre Escobar.
- 0:28–0:33: o cartel e a guerra "por una sola palabra: extradición".
- 0:35–0:45 "El Tratado. Washington, catorce de septiembre de mil novecientos setenta y nueve… firman un tratado de extradición": o papel de 1979 aparece no 1º minuto.
- 2:24–2:35: Escobar entra no grupo ("le falta una cosa: que el tratado nunca los alcance").
- 3:40–3:51: o trato "a cambio de que no haya extradición".
- 4:23–4:30 "La palabra ya no es un papel en Washington. Es un vuelo que sale de Bogotá.": o roteiro junta literalmente "papel" e "avião", ou seja, o título e a thumb.
- 5:30 a lei cai; 11:09 a Constituição proíbe a extradição; 13:33–13:40 o fecho volta ao "tratado firmado durante el gobierno de su padre".

Ressalva: o nome de Escobar só se liga ao tratado aos 2:24. No 1º minuto ele está implícito no "Cártel de Medellín". Aceitável.

**3 Par como peça só: ok.** O título traz o objeto (papel de 1979) e a vontade de destruí-lo; a thumb traz o homem e a ameaça (um avião passando por cima dele). Nenhuma ideia se repete; o nome é o mesmo, o que o item 0 permite. A extradição não é dita em nenhum dos dois. Ambiguidade: para o público do tema, avião + Escobar lê primeiro como **avioneta da cocaína**, não como voo da extradição. O par não se contradiz, mas a pergunta conjunta fica mais frouxa.

**4 Celular: ok.**
- Na grade a 160×90 o avião vermelho e o rosto se leem, e esta é a única thumb monocromática e sem texto.
- 1 foco (o rosto) + 1 apoio (o avião).
- Risco na arte final: com a "metade direita do rosto na sombra" sobre o fundo ardósia, o contorno do rosto pode sumir. Além disso, vermelho `#B3261E` sobre ardósia `#2E3A46` tem ~1,1–1,5:1 de luminância (mesma lição da 012 MI6 na bíblia). A asa que sai do rosto e entra no ardósia lê só pela diferença de cor.

**5 Diferenciação: título ok · thumb ok.**
- Título: nenhum título com "papel" + Escobar. A estrutura aparece 12 vezes no tema, mas o X de todas é uma pessoa ou uma morte; o nosso é um objeto.
- Thumb: não copia nenhuma, mas o assunto é o de todas (12 de 12 com o rosto de Escobar).

**6 Regras: ok (50 caracteres).**
- Nenhuma palavra proibida; nada de arma, sangue, droga ou dinheiro.
- Retrato real (não é cena inventada); o avião é um símbolo gráfico, não um documento falso.
- O desvio da bíblia está declarado e justificado (teste do personagem do tema, pedido do Rodrigo; Archive CIA/KGB H1).
- Paleta da `identidade.md`.

**7/8: ver abaixo.**

**Ficha da RUBRICA**
```text
Par A (T1 + Thumb A, padrão `rosto-emocao`) · portões: políticas ok · bíblia ok (desvio declarado) · promessa ok (0:35–0:45) · refs ok (título 41,6× e 7,8×; thumb 29,1× e 7,1×, ressalva acima)
T1 8/10 — "papel de 1979" é objeto concreto e inesperado no tema (cujos X são pessoas e mortes); "papel" é genérico de propósito, então não chega ao nível das "96 million black balls".
T2 8/10 — pergunta específica (que papel? por que um narco quer destruí-lo?), sem desfecho e sem sim/não; parte do público adivinha "extradição" (efeito Narcos) ou imagina um documento comprometedor qualquer.
T3 10/10 (50 caracteres) — 1 leitura, 1 ideia, nome conhecido.
T4 6/10 — estrutura com hits (41,6× e 7,8×), mas o esqueleto "El X que Pablo Escobar…" já aparece 12× no tema e o maior canal dela fica em 0,1–0,7×; o X-objeto é novo, a estrutura não.
T5 6/10 — "quería destruir" dá conflito, mas o que está em jogo fica escondido: destruir um papel soa como sumir com uma prova (coisa comum), não como guerra contra um país inteiro; nenhuma escala visível.
H1 7/10 — 5 palavras: "Escobar com avião vermelho cruzando"; 1 foco + 1 apoio.
H2 8/10 — grade 160: rosto dominante (≈ 85% da altura na arte final) e silhueta do avião legíveis; sem texto; tira-se 2 pelo risco de a metade do rosto na sombra fundir com o fundo ardósia.
H3 7/10 — expressão contida + ameaça visível (o avião passando por cima), mas é símbolo estático, não um instante antes do desfecho.
H4 6/10 — posição do olho: a 160×90 o olho pega primeiro os textos amarelos (L1C1, L3C1) e a moldura Nat Geo; a nossa é a 3ª–4ª, levada pelo vermelho diagonal. Única ilustrada e monocromática, mas o assunto é o das 11 vizinhas (a rubrica dá 3 para "rosto de Escobar no cartel"); 6 pelo traço e pela paleta realmente únicos.
P1 8/10 — completam sem repetir ideia (o título traz o objeto, a thumb traz a ameaça); a leitura do avião como avioneta da cocaína tira a nota de 9–10.
Total 74/100 → REPROVADO (regra: ≥ 75, nenhum < 6, T2/H1/P1 ≥ 7). Nenhum critério < 6 e T2/H1/P1 ≥ 7: só o total fica 1 ponto abaixo do corte.
```

**Eu clicaria vendo isso entre 11 vídeos do tema no celular?** Pelo título, provavelmente sim: é o único dos 12 que promete uma coisa que eu não sei ("um papel de 1979"), enquanto os outros prometem a captura e o império de sempre. Pela thumb, não: é mais um rosto de Escobar, só que mais apagado (ardósia) do que as fotos quentes ao redor. A resposta honesta para o par é "sim, puxado só pelo título". O total de 74 reflete isso.

**Veredito do Par A: REPROVADO** (74/100; os itens 0–6 do CRIVO passam, o portão da rubrica não).

**Ajustes que levariam a ≥ 75** (para registro e para uma decisão do Rodrigo; esta é a última rodada):
1. **H4 (+1–2):** sair do rosto frontal centrado que as 11 fotos usam.
   - Perfil 3/4 cortado pela borda esquerda, olhando para o avião, com o avião vermelho em silhueta **contornado por um filete papel `#E9DFC9`**, para não depender do vermelho sobre ardósia.
   - Ou trocar o fundo ardósia pela cor papel `#E9DFC9` com o rosto em tinta preta: seria a única thumb clara e sem foto da grade.
2. **T5 (+1):** deixar à vista o tamanho da guerra sem dizer "extradição", mantendo ≤ 55 caracteres e sem repetir o "guerra a una PALABRA" do Par C. Ex.: "El papel de 1979 por el que Escobar desafió a un país" (52 caracteres; conferir colisão com o Par B, "todo un país").
3. **Arte:** a metade na sombra do rosto precisa de uma luz de recorte (rim light em papel) no contorno direito, ou o rosto funde com o fundo a 160×90.
4. **Proposta:** corrigir a descrição das referências de thumb (Mighty Monk = colagem de fotos com arma; Fugitivos = outro homem dominante) e registrar a contra-evidência da Mafia e Historia (0,1–0,7×).

## Par B (MANTIDO): continua APROVADO — "Cómo Escobar tomó de rehén a todo un país" + Thumb B (`cena-acao`)
- **0 Assunto: ok.** "Escobar" é a 2ª palavra do título; a thumb sozinha (helicóptero + fazenda) não identifica o assunto, mas o título identifica.
- **3 Par: ok.** "rehén" no título, "¿RESCATE?" na thumb: a pergunta é quem era refém e o que aconteceu (pago em 0:05–0:20, 7:40–8:46, 9:26, 11:09–11:45). Não conflita com o Par A novo, e os 3 continuam vendendo a mesma guerra.
- **6 Regras: ok (41 caracteres).** Nenhuma palavra proibida; sem arma nem atirador (condição da arte mantida). Os sequestros ficam com os Extraditables no vídeo, e o título fala do país como refém.
- **8 Thumbs diferentes: ok.** 5 palavras: "helicóptero baixando sobre fazenda escondida". É a única diurna, de paisagem e sem rosto (grade-tema-B2-320).

## Par C (MANTIDO): continua APROVADO — "Escobar le declaró la guerra a una PALABRA" + Thumb C (`documento-evidencia`)
- **0 Assunto: ok.** "Escobar" é a 1ª palavra.
- **3 Par: ok.** O título esconde a palavra e a thumb mostra a palavra sendo riscada (o nome escondido, Fern "UNABOMBER"); é pago literalmente em 0:28–0:33. Não conflita com o Par A. O "papel" do A e a folha do C nunca aparecem juntos no "Testar e comparar" (cada título sai com a sua thumb).
- **6 Regras: ok (42 caracteres).** Nenhuma palavra proibida; fonte e paleta do canal.
- **8 Thumbs diferentes: ok.** 5 palavras: "a palavra sendo riscada a caneta". A única de papel claro com tipografia (grade-tema-C-320).

## Diferenciação entre as 3 thumbs: ok
- A: "rosto em tinta, avião vermelho" (retrato, sem texto).
- B: "helicóptero diurno sobre fazenda" (paisagem, palavra-pergunta).
- C: "folha datilografada, palavra riscada" (documento, o nome escondido).

Elemento dominante, composição e tipo de texto são distintos nas 3. A e B fogem do padrão "objeto + sello" do canal. Não há `variantes.json` (é reembalagem de vídeo no ar, não embalagem nova): o item não se aplica. Cuidado já registrado: não pôr a C ao lado da Thumb B do 011 ("TARRAGONA").

## Veredito: 2 de 3 pares aprovados — rodada 3 de 3
- Par A: REPROVADO — 74/100 (corte 75; T4 6, T5 6, H4 6). Corrigir a H4 (sair do rosto frontal centrado; avião com filete papel ou fundo papel) e a T5 (deixar à vista que a guerra é contra um país), e corrigir a descrição das referências de thumb (Mighty Monk e Fugitivos não são "rosto de Escobar ilustrado dominante").
- Par B: APROVADO (mantido; itens 0/3/6/8 ok, 41 caracteres).
- Par C: APROVADO (mantido; itens 0/3/6/8 ok, 42 caracteres).
