# Proposta de encaixe do padrão ouro (17/11/2026) — NÃO APLICADA

Só proposta. Nada abaixo foi alterado. Depois da aprovação do Rodrigo (item a item ou em bloco), **outro job** aplica, com commit por arquivo. Base: `PADRAO-OURO.md`, `RUBRICA.md`, `AUDITORIA.md`.

## 1. `skills/embalagem/CRIVO.md` (o portão)
1. **Somar a rubrica de 100 pontos aos 8 itens atuais**, sem tirar nenhum. Os itens 1 (evidência), 2 (promessa cumprível), 6 (regras/bíblia) e 8 (3 thumbs diferentes) viram **portões** (sim/não). Os itens 3, 4, 5 e 7 passam a ser medidos pelos 10 critérios da `RUBRICA.md` (T1–T5, H1–H4, P1).
2. **Regra de aprovação por par:** total ≥ 75, nenhum critério < 6, T2/H1/P1 ≥ 7. O vídeo segue com os 3 pares aprovados (como hoje). Ficha por par no formato da `RUBRICA.md`.
3. **Teste da grade obrigatório:** o revisor monta a maquete de cada thumb (ou a descrição em prévia de código, se ainda não houver arte) na posição linha 2 × coluna 2 de uma grade 4×3 com 11 concorrentes do tema, a 160×90 e a 320×180 (`pesquisa/embalagem-padrao-ouro-2026-11/scripts/grade.py`, que vira `skills/embalagem/scripts/grade.py`). Sem grade, H2 e H4 ficam em no máximo 6 (reprova).
4. **Calibração:** "consigo apontar um hit do corpus que faz isso melhor? se sim, −2 a −3"; nota 10 só com comparação explícita com um hit ≥ 1,5× do corpus (`corpus.csv`).

## 2. `skills/embalagem/SKILL.md`
1. **Passo 0 novo, "teste da ideia"** (Galloway): antes da pesquisa, escrever em 1 linha o sujeito concreto e o que está em jogo. Se não houver, voltar ao backlog (não gastar a etapa).
2. **Passo 5 (proposta), regras do padrão ouro:** título 30–50 caracteres (teto duro 65, salvo fórmula da bíblia com tema-ímã), sem parênteses e sem aposto explicativo; sujeito nomeado no lugar de categoria; sem pergunta sim/não; sem série/episódio/notícia crua. Thumb com texto de **tipo diferente do título**: veredito, juízo, nome escondido ou palavra da estrutura; **nunca** a sigla/nome do país/tema que já está no título (hoje 100% dos nossos moldes repetem).
3. **Fórmula da bíblia só com tema-ímã**, medido no `refs.csv` (≥ 3 vídeos do tema no nicho acima de 2× a mediana do canal deles). Tema médio usa estrutura de tensão do catálogo (`PADRAO-OURO.md` §1.4).
4. **Escrever 10–15 títulos candidatos** e escolher 3 (Galloway/Colin & Samir sugerem ~30; hoje sai direto com 3), registrando os descartados numa linha cada no `EMBALAGEM.md`.
5. Modelo do `EMBALAGEM.md`: acrescentar a ficha da rubrica (autoavaliação) por par e o caminho das grades.

## 3. `skills/thumbnail/SKILL.md`
1. Critério de pronto novo: **grade 4×3 com 11 concorrentes do tema** a 160×90 com cada thumb final (A/B/C), olhada antes de entregar; se a nossa não for a 1ª ou 2ª que o olho pega, refazer (até 2 rodadas, como hoje).
2. Elemento dominante ≥ 25% da área (mapas e objetos) ou ≥ 40% (personagem); altura de letra ≥ 12% da altura da thumb; contorno/sombra no texto.
3. "Congelar o instante antes do desfecho" e expressão contida (não careta) entram no prompt-base de cada conceito.

## 4. `conhecimento/titulos.md` e `conhecimento/thumbnails/README.md`
- Nova seção "Padrão ouro (17/11/2026)" com as 5 + 5 regras, **cada uma com 1 exemplo e o link** (`PADRAO-OURO.md`), e o achado de que a estrutura de título normalizada por canal não ganha sozinha (índice 0,94–1,07): a estrutura é assinatura, o sujeito e o que está em jogo fazem o hit.
- Corrigir a regra antiga "a thumb leva 2–3 palavras e o resto fica no título" para "0–3 palavras **de outro tipo** (veredito/juízo/nome escondido/palavra da estrutura)".
- Acrescentar a leitura do CTR do YouTube (metade dos vídeos entre 2% e 10%, cai com mais impressões; comparar só entre os nossos e por fonte de tráfego) e que o "Testar e comparar" decide por tempo de exibição.
- Lacuna registrada como **Hipótese**: não há fonte de peso sobre mapa/objeto/número em thumb de canal educacional; medir com o placar `youtube.padrao_thumb_placar`.

## 5. Bíblias (estilo mantido; só a régua muda)
### historia-ptbr (`biblia/titulo.md`, `thumb.md`)
- **Título:** a fórmula "A história INTEIRA de X em N minutos" só com civilização-ímã **e** sem colisão (HiM: Egito 10,2×, Índia 11,1×; com tema médio, 0,05–0,75×). França e Alemanha, que saíram na fórmula pura em 15–16/11, seriam reprovadas em T1/T4.
- **Thumb:** sair da "pegada HiM clara" (panorama + NOME + datas): ela repete o título (P1 = 3) e a 160×90 vira cartão-postal igual aos concorrentes. Manter como **no máximo 1 das 3** e só quando o título não tiver o nome do país. Priorizar: duelo cara a cara (`conflito-xvy`, o COROA × TURBANTE), personagem com emoção + objeto do hook com o desfecho pendente, mapa aceso único (o "TUDO ISSO?", 9,6%).
- Texto da thumb: veredito/pergunta curta que **completa** ("DE NOVO?", "SÓ SORTE?"), nunca o nome do país.

### dossie-es (`biblia/titulo.md`, `thumb.md`)
- **Título:** sigla/organização temida de 1 palavra (molde AiM: SS, Gestapo, KGB, CIA, MI6 3–9×; eventos 0,5–0,7×); sem aposto explicativo; ≤ 50 caracteres. Estruturas do nicho com quase nenhum flop: caso/caçada ("La cacería de…"), "El/La X que…" (Fern "The Only Nazi Hitler Feared" 2,75×), duelo "vs" (Atlas "CIA vs KGB" 78×).
- **Thumb:** a SIGLA gigante na thumb repete o título (P1 média 2,9, abaixo do mínimo em 8 de 8 no ar; `AUDITORIA.md`). Proposta: quando o título já traz a sigla, a thumb leva **o sello de lacuna como texto principal** e a sigla sai ou fica pequena na aba "EXPEDIENTE"; testar 1 das 3 **escura/noturna** com objeto íntimo (o maior hit do AiM, SS 8,8×, é a única escura do top claro deles).

### em-relevo (`biblia/titulo.md`, `thumb.md`)
- **Título:** 32–50 caracteres, sem parênteses e sem reticências soltas; lugar brasileiro reconhecível + ameaça/ausência/perda ("Por que o BRASIL não tem…" 4,88×; "Por que [desastre] foi MUITO pior do que parece" 1,88×); nada de pergunta sim/não sobre recorde.
- **Thumb:** testar o **relevo claro e saturado** (mar turquesa, terra verde/bege, como a RealLifeLore em 10/10 thumbs) com **1 região em cor de alerta** + camada de tensão (seta convergindo, linha que corta, antes×depois, escala humana "CIDADE"). Região-alvo ≥ 25% da área. Mantém a regra de no máximo 1 mapa escuro.

### lugares-guerra-en (pausado)
- Só registro: "Why Can't You Visit X?" é estrutura provada (Iwo Jima 4,5 mi), mas o CTR 1,8% com 1.448 impressões sugere thumb fraca; aplicar a rubrica quando o canal voltar.

## 6. Medição (Métricas)
- Gravar a nota da rubrica de cada par em `youtube.embalagem_variantes.notas` (ou coluna nova `nota_rubrica`, decisão do job que aplicar) para, com o CTR e o "Testar e comparar", calibrar a régua: é o "eval automático do crivo" que `conhecimento/titulos.md` deixou para depois.
- Reavaliar a rubrica em 30 dias (≥ 12 vídeos novos com ≥ 1.000 impressões cada): se nota e CTR não andarem juntos, ajustar pesos.

## O que precisa de aprovação do Rodrigo
1. Rubrica de 100 pontos como parte do crivo (itens 1 e 2 acima).
2. Regras novas de título (30–50, sem parênteses/aposto, fórmula só com tema-ímã).
3. Thumb nunca repete a sigla/nome do título (muda o layout-assinatura do dossie-es e a pegada HiM do historia-ptbr).
4. Em Relevo: teste do relevo claro + 1 alerta.
5. Os antes×depois (`ANTES-DEPOIS.md`), um a um: aplicar ou não nos vídeos no ar (reembalagem é decisão dele; a troca é manual no Studio).
