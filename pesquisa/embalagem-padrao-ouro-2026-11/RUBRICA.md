# Rubrica do padrão ouro: título + thumb (17/11/2026)

Para o crivo da `embalagem` aplicar **objetivamente** a cada par título+thumb (A↔T1, B↔T2, C↔T3). Base: `PADRAO-OURO.md`, `FONTES-METODO.md` (método com link) e o corpus de 28 canais (`corpus.csv`, `ANALISE-*.md`). Proposta: só entra no `CRIVO.md` depois da aprovação do Rodrigo (`PROPOSTA-ENCAIXE.md`).

## Como pontuar
- 10 critérios, 0–10 cada (total 100). Dê a nota pela âncora mais próxima (10 / 7 / 3 / 0) e escreva **1 linha de porquê**.
- **Aprova o par:** total **≥ 75**, **nenhum critério < 6** e **T2, H1 e P1 ≥ 7** (os 3 que mais separam hit de flop no corpus).
- **Portões eliminatórios** (sim/não, antes da nota; qualquer "não" reprova): políticas (`conhecimento/politicas-youtube.md`), bíblia do canal respeitada, promessa cumprível com fato de fonte no BRIEF e paga no 1º minuto (itens 2 e 6 do `CRIVO.md` atual), ≥ 2 referências medidas por padrão (item 1 atual).
- **Teste da grade é obrigatório para H2 e H4:** monte a nossa thumb (maquete) na posição linha 2 × coluna 2 de uma grade 4×3 com **11 concorrentes do tema** a **160×90** e a **320×180** (`scripts/grade.py <rotulo> <id> <idioma> "<tema>"`; na embalagem, a maquete entra no lugar do id). Olhe as duas com Read antes de dar a nota.

## Título (50)
### T1 · Promessa concreta (0–10)
Pergunta: o título nomeia **uma coisa concreta** (objeto, agente, lugar, número, ação) em vez de um rótulo de tema?
- **10:** um objeto/agente concreto e estranho carrega o título. "Why are there 96 million black balls on this lake?" (Veritasium; ver `FONTES-METODO.md` A8: o mesmo vídeo como "shade balls" não andava). "Como um RIO manteve o Egito vivo por 7.000 anos" (nosso, CTR 5,9%).
- **7:** concreto, mas o objeto é esperado para o tema ("A KGB en 14 minutos: del sótano de Lubianka al piolet de México": concretos bons, mas 3 deles).
- **3:** rótulo de tema ("A história INTEIRA da França em 15 minutos"; "TODA la historia de las SS en 14 minutos").
- **0:** vago/abstrato ("O que está acontecendo com o clima no Sul do Brasil?").

### T2 · Lacuna aberta, resposta guardada (0–10) — mínimo 7
Pergunta: depois de ler, o espectador tem **uma pergunta específica** cuja resposta só o vídeo dá? O título não entrega o desfecho e não é sim/não.
- **10:** tensão nomeada e sem resposta: "Roma pagou resgate aos bárbaros. Como virou dona do mundo?" (contradição + pergunta); "Why didn't Castro try to retake Guantanamo Bay from America?" (History Matters, 2,5 mi, 2,65×, contra "Why did the Treaty of Versailles Fail?", 0,51×: protagonista famoso + o que ele **não** fez).
- **7:** lacuna clara mas genérica ("Por que a Pérsia virou Irã e NUNCA virou árabe?": o 2º elemento salva a pergunta crua).
- **3:** pergunta sim/não ou resposta no título ("El Niño 2026 vai ser o mais forte da história?" — sim/não, CTR 1,55%).
- **0:** nenhuma pergunta (catálogo/aula: "Every X Explained" onde há 20 clones).

### T3 · Simples e curto (0–10)
Pergunta: entende-se de primeira (1 leitura, sem nome que o público não conhece) e cabe no celular?
- **10:** ≤ 50 caracteres e 1 ideia ("Beat Ronaldo, Win $1,000,000": 29; "Why Can't You Visit Bikini Atoll?": 33).
- **7:** 51–65 caracteres ou 2 ideias encadeadas e claras.
- **3:** 66–80 caracteres, ou nome desconhecido como sujeito, ou 3+ itens ("FBI: la Agencia que Espiaba a Su Propio País… Hasta que Abrieron sus Archivos": 77).
- **0:** > 80, ou só entende quem já viu o vídeo.
(Corpus: mediana do título nos hits ≥ 1,5× a mediana do canal = 39 caracteres nos gerais e 38,5 no dossiê, contra 46 e 53 nos flops; `ANALISE-*.md`.)

### T4 · Estrutura provada e fora da manada (0–10)
Pergunta: usa uma estrutura do catálogo do padrão ouro (`PADRAO-OURO.md` §Título) com ≥ 2 hits do nicho acima da mediana **e** não colide com a fórmula dos clones no tema?
- **10:** estrutura com hits medidos no nicho e nenhum título igual no tema ("Chamaram um VIKING para reinar. Como a Rússia ficou gigante?": afirmação estranha + pergunta; CTR 9,6% em 188 impressões).
- **7:** estrutura provada, mas já existe 1–2 vezes no tema.
- **3:** fórmula dos clones onde o tema já existe nela ("A história INTEIRA de X em N minutos" com 10+ canais pt).
- **0:** cópia literal de título de concorrente.

### T5 · O que está em jogo (escala, contraste ou transformação) (0–10)
Pergunta: o título mostra **algo grande em jogo** — número extremo, superlativo específico, contraste de destinos (A × B), transformação (X → Y), regra quebrada?
- **10:** "$1 vs $1,000,000,000 Futuristic Tech!" (MrBeast, 235 mi); "Why Did the U.S. Become Rich While Latin America Stayed Poor?" (Ziro, 297 mil); "O país que ganhou nome de MERCADORIA" (nosso, 4,1%).
- **7:** escala implícita ("5.000 ANOS de Índia em 19 minutos": número grande, mas é o número dos clones).
- **3:** nada em jogo, só descrição ("La historia COMPLETA de la CIA en 12 minutos").
- **0:** diminui o tema (anticlímax, "curiosidade rápida").

## Thumb (40)
### H1 · Uma ideia em menos de 1 segundo (0–10) — mínimo 7
Pergunta: descrita em **5 palavras**, a thumb conta uma coisa só? Quantos focos? (Teste da olhada, Galloway; `FONTES-METODO.md` B2–B4.)
- **10:** 1 foco, ≤ 3 elementos, a história lê sem o título: MrBeast "Day 1 → Day 200" (antes × depois do mesmo corpo); nosso "TUDO ISSO?" (só o mapa da Rússia aceso, CTR 9,6%).
- **7:** 1 foco + 1 apoio (personagem + objeto).
- **3:** 2–3 focos competindo ("FBI" escrito 2× + porta + gaveta).
- **0:** 4+ elementos/colagem (Roma v1 com 8 elementos, reprovada em 14/11).

### H2 · Leitura a 160×90 (0–10)
Pergunta: na grade a 160×90, dá para ler o texto e reconhecer o elemento dominante?
- **10:** elemento dominante ≥ 40% da área, silhueta reconhecível, texto ≤ 3 palavras com altura de letra ≥ 12% da altura da thumb, contraste próprio (contorno/sombra).
- **7:** dominante lê; texto lê a 320 mas não a 160.
- **3:** dominante pequeno (< 25% da área) ou de baixo contraste com o fundo (mapa escuro sobre navy).
- **0:** não se entende o que é.

### H3 · Emoção ou tensão (estado incompleto) (0–10)
Pergunta: a imagem mostra um **momento antes do desfecho** (perigo, ameaça, mistério, contraste chocante, rosto/personagem com emoção legível) que faz querer ver o fim?
- **10:** desfecho pendente visível: MrBeast "Would You Risk Drowning for $500,000?" (corda + pedra, rosto tenso); nosso "CHUVA × CANHÃO" (duelo cara a cara).
- **7:** emoção presente mas estática (personagem assustado sem a causa visível).
- **3:** cena bonita/descritiva sem tensão (panorama + nome do país: "FRANÇA 486–2026").
- **0:** neutro/catálogo.
Sem rosto: valem personagem desenhado com expressão (historia-ptbr), objeto em perigo ou fora do lugar (dossie-es), anomalia no mapa/foto real (Em Relevo). Expressão **contida** vence a careta (30 testes do MrBeast, `FONTES-METODO.md` B13).

### H4 · Destaca-se na grade do tema e do canal (0–10)
Pergunta: na grade com 11 concorrentes a 160×90, **a nossa é a que o olho pega primeiro** (ou uma das 2)? E não repete o padrão dominante das vizinhas do próprio canal?
- **10:** única com outra paleta/composição e ainda assim legível; diferente das 3 vizinhas do canal.
- **7:** destaca-se, mas lembra 1–2 concorrentes.
- **3:** faz o que todas fazem (mapa vermelho do Pacífico no El Niño; rosto de Escobar no cartel; panorama + NOME + datas nos países) ou repete a vizinha do canal.
- **0:** some na grade.

## Par (10)
### P1 · Título × thumb: completam, não repetem (0–10) — mínimo 7
Pergunta: thumb e título juntos formam **uma** pergunta, sem repetir palavra nem ideia? (Thomas Frank, `FONTES-METODO.md` A11–A12.)
- **10:** cada um leva metade: título "Roma pagou resgate aos bárbaros. Como virou dona do mundo?" + thumb "DE NOVO?" com senador chorando sob Roma em chamas (a thumb põe a dor, o título o paradoxo). MrBeast "Survive 30 Days Trapped In The Sky" + thumb da cama numa plataforma sobre as nuvens (a thumb mostra o "sky", o título o desafio).
- **7:** completam, mas a thumb ecoa 1 ideia do título.
- **3:** a thumb repete palavra do título (SIGLA da thumb = sigla do título: "CIA" + "La historia de la CIA"; "FRANÇA" + "história da França").
- **0:** prometem coisas diferentes (thumb vende outro vídeo).

## Ficha (o revisor grava assim, por par)
```text
Par A (T1 + Thumb A, padrão `<eixo>`) · portões: políticas ok · bíblia ok · promessa ok · refs ok
T1 x/10 — … | T2 x/10 — … | T3 x/10 (N caracteres) — … | T4 x/10 — … | T5 x/10 — …
H1 x/10 — 5 palavras: "…" | H2 x/10 — grade 160: … | H3 x/10 — … | H4 x/10 — posição do olho: … | P1 x/10 — …
Total xx/100 → APROVADO | REPROVADO (regra: ≥ 75, nenhum < 6, T2/H1/P1 ≥ 7) · correção pedida: …
```

## Calibração (para o revisor não inflar)
- Nota 10 é rara: no corpus, só os hits ≥ 1,5× a mediana do canal ganham 10 em T2/H1/P1. Sem comparação com a grade, H2 e H4 não passam de 6.
- Teste rápido de cada nota: "consigo apontar um hit do corpus que faz isso melhor?" Se sim, tire 2–3 pontos.
- A rubrica mede a **embalagem**, não o tema. Tema fraco (organização desconhecida, país sem demanda) é decisão de pauta (backlog), mas o revisor anota "tema fraco" quando a embalagem 80+ não deve salvar o vídeo.
